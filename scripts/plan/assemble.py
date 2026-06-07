"""Multi-domain plan composer — the one task that reasons over the router summary.

`assemble` reasons ONLY over the `router.summarize` name-addressable summary (the V1
PII trust boundary — 0 raw PII) plus an injected roster of stubbed specialists. It
routes each in-scope goal-domain to its roster specialist and composes the outputs
into one attributed document, running EVERY emitted claim through the SAME four filters
over ONE canonical claim set (the single-composition-pass guarantee, Security MED-3):
attribution, sourcing-completeness, population-mismatch (metadata-keyed off the rec's
evidence-grounding category), and the FAIL-CLOSED, CLASS-AWARE HALT filter (metadata-
keyed off the rec's intervention-class). Each section also surfaces >=1 operator-
specific input read BY FIELD NAME from the summary (per-section personalization).

The roster seam is injectable so tests supply a stubbed registry: a dict
`{domain: specialist}` where each specialist is a callable
`specialist(domain, summary) -> {"specialist": name, "recommendations": [...]}` (or a
thin-library signal `{"thin_library": True, ...}`). A domain absent from the roster is
the no-specialist coverage-gap-by-absence case. `assemble` calls no `store.read`, opens
no operator NDJSON, and imports no live specialist deployment — its only operator-state
source is the summary.
"""

# Evidence-grounding categories that require a population-mismatch flag (crit 3).
GROUNDING_NEEDS_FLAG = ("animal", "in-vitro")

# The single shared coverage-gap disclosure shape — used by the thin-library (crit 4),
# the no-specialist (crit 5), and the empty-output (Security LOW 5-4) paths. One
# definition, never divergent copies.
THIN_LIBRARY_GAP = "thin-library"
NO_SPECIALIST_GAP = "no-specialist"
EMPTY_OUTPUT_GAP = "no-recommendations"

# The four filters every emitted claim transits over the one canonical claim set
# (Security MED-3 single-claim-set transit invariant).
FILTERS = ("attribution", "sourcing", "population-mismatch", "halt")

# Operator-state field names surfaced for per-section personalization (crit 8). Read
# BY FIELD NAME from the name-addressable summary — never raw PII.
_PERSONALIZATION_FIELDS = (
    "goal-targets",
    "goal-priority-order",
    "active-issue-class",
    "recovery-status-band",
    "hard-limits",
)


def _personalize(summary):
    """Surface >=1 operator-specific input from the summary for a section (crit 8).

    Reads operator inputs BY FIELD NAME from the name-addressable summary so each
    section reflects the operator's stated goals / current state / hard limits. A
    section reflecting 0 operator inputs is the crit-8 failing-capable anti-target.
    """
    surfaced = {f: summary.get(f) for f in _PERSONALIZATION_FIELDS}
    return {k: v for k, v in surfaced.items() if v is not None}


def _coverage_gap(domain, kind, personalization, specialist_name=None):
    """Build the shared coverage-gap disclosure for a domain with no recommendations.

    Args:
        domain (str): The in-scope goal-domain rendered as a gap.
        kind (str): THIN_LIBRARY_GAP or NO_SPECIALIST_GAP.
        personalization (dict): The per-section operator inputs surfaced from the summary.
        specialist_name (str, optional): The thin-library specialist, if any.

    Returns:
        (dict) A section carrying the gap disclosure, 0 recommendation-shaped
        entries, and a surfaced operator input — never a fabricated regimen.
    """
    return {
        "domain": domain,
        "specialist": specialist_name,
        "coverage_gap": kind,
        "disclosure": (
            f"Coverage gap ({kind}) for {domain}: no vetted recommendation can be "
            f"made — this is disclosed, not filled with a fabricated regimen."
        ),
        "recommendations": [],
        "personalization": personalization,
    }


def _is_cross_domain(rec):
    """A claim sourced by no single specialist (a composition-bug cross-domain claim)."""
    return bool(rec.get("cross_domain"))


def _is_complete(rec):
    """crit 2: a rec carries source + tier + reversibility; every number carries
    units + a reference range."""
    if not (rec.get("source") and rec.get("confidence_tier") and rec.get("reversibility")):
        return False
    for number in rec.get("numbers", []):
        if not (number.get("units") and number.get("reference_range")):
            return False
    return True


# HALT dispositions, the value `_halt_disposition` returns.
HALT_CLEAR = "clear"                       # no contradiction; the rec is emitted actionable
HALT_VIOLATION = "violation"               # determinate contradiction; strike
HALT_INDETERMINATE = "indeterminate"       # status cannot be established; strike fail-closed


def _prohibited_classes(summary):
    """Derive the prohibited intervention-classes from the operator's hard limit(s).

    Class-aware (Security HIGH-2): keys off the limit's prohibited CLASS so a member
    expressed in different terms than the limit text is caught, not only a literal
    restatement. The map is the operator-stated-limit → intervention-class binding.
    """
    raw = (summary.get("hard-limits") or "").lower()
    classes = set()
    if "stimulant" in raw:
        classes.add("stimulant")
    if "overhead" in raw or "pressing" in raw:
        classes.add("overhead-pressing")
    if "fasting" in raw:
        classes.add("fasting")
    return classes


def _limit_is_recognized(summary, prohibited_classes):
    """Whether the stated hard-limit phrase maps to at least one known prohibited class.

    An UNrecognized phrase (a limit present but mapping to no known class) makes every
    rec's prohibited-class status indeterminate — the fail-closed trigger (Security
    MED 5-2(b)). No hard limit at all is NOT indeterminate (nothing to clear against).
    """
    return bool(prohibited_classes)


def _halt_disposition(rec, summary, prohibited_classes):
    """crit 9 (fail-closed): classify a rec against the operator's hard limit(s).

    Returns HALT_CLEAR / HALT_VIOLATION / HALT_INDETERMINATE.

    Detection forms, all load-bearing:
      (i)  DIRECT/literal — the rec's claim restates the limit's subject text.
      (ii) CLASS-AWARE — the rec's `category` metadata is a member of the limit's
           prohibited class, even in different terms (a string-match HALT misses this).
      (iii) FAIL-CLOSED (Security MED 5-2) — when a hard limit is PRESENT and the rec's
            prohibited-class status is INDETERMINATE — the rec's `category` is
            missing/None (a), OR the limit phrase maps to no known prohibited class
            (b) — default to SUPPRESS, not emit. Determinacy, not default-allow.
    """
    limit_text = (summary.get("hard-limits") or "").strip()
    if not limit_text:
        return HALT_CLEAR  # no stated limit — nothing to clear against

    claim = (rec.get("claim") or "").lower()
    # (i) literal/direct contradiction: the rec restates the hard-limit subject.
    subject = limit_text.lower().replace("no ", "", 1).strip()
    if subject and subject in claim:
        return HALT_VIOLATION
    # (ii) class-aware: the rec's intervention-class is in the prohibited set.
    category = rec.get("category")
    if category in prohibited_classes:
        return HALT_VIOLATION
    # (iii) fail-closed on indeterminate status: missing category OR unrecognized limit.
    if category is None or not _limit_is_recognized(summary, prohibited_classes):
        return HALT_INDETERMINATE
    return HALT_CLEAR


def _strike(claim, summary, indeterminate=False):
    """Fail-closed HALT disposition: strike the actionable regimen, never ship it.

    Default OMIT-with-disclosure — the violating rec's actionable content is
    SUPPRESSED/STRUCK (not merely annotated): its actionable numbers/dosing are
    removed and an explicit contradiction disposition names the violated hard limit.
    The constrained FLAG exception likewise strikes the actionable content; it is
    never shipped actionable. When `indeterminate`, the rec is suppressed because its
    prohibited-class status could not be established (fail-closed for safety), not
    because a determinate contradiction was proven.
    """
    claim["actionable_content_struck"] = True
    claim.pop("numbers", None)  # the actionable regimen content is removed
    if indeterminate:
        claim["indeterminate_class_suppressed"] = True
        claim["contradiction_disposition"] = (
            f"Suppressed (fail-closed): prohibited-class status against the stated "
            f"hard limit ({summary.get('hard-limits')!r}) is indeterminate. "
            f"Actionable content suppressed for safety."
        )
    else:
        claim["contradiction_disposition"] = (
            f"Struck: contradicts the stated hard limit "
            f"({summary.get('hard-limits')!r}). Actionable content suppressed."
        )
    return claim


def _compose_claim(rec, specialist_name, summary, prohibited_classes):
    """Run one recommendation through the four canonical filters in one pass.

    attribution → sourcing → population-mismatch → HALT, over the one canonical claim.
    Returns the composed claim (carrying its transit marker), or None if it is
    incomplete (an incomplete recommendation is not emitted complete — crit 2).
    """
    # Filter — sourcing-completeness (crit 2): an incomplete rec is not emitted.
    if not _is_complete(rec):
        return None
    claim = dict(rec)
    # Filter — attribution: every claim traces to exactly one specialist.
    claim["attributed_specialist"] = specialist_name
    # Filter — population-mismatch, metadata-keyed off the grounding category (crit 3).
    if claim.get("grounding") in GROUNDING_NEEDS_FLAG:
        claim["population_mismatch_flag"] = True
    # Filter — fail-closed class-aware HALT (crit 9): strike on a determinate violation
    # OR on indeterminate prohibited-class status (default-deny, not default-allow).
    disposition = _halt_disposition(claim, summary, prohibited_classes)
    if disposition == HALT_VIOLATION:
        _strike(claim, summary)
    elif disposition == HALT_INDETERMINATE:
        _strike(claim, summary, indeterminate=True)
    # Transit marker: this claim passed all four filters over the canonical set.
    claim["filters_transited"] = FILTERS
    return claim


def assemble(goal_set, summary, roster):
    """Compose the attributed multi-domain plan from the router summary + roster.

    Routes each in-scope goal-domain to its roster specialist and composes the outputs
    into one attributed document, running EVERY emitted claim through the SAME four
    filters over ONE canonical claim set: attribution, sourcing-completeness,
    population-mismatch (metadata-keyed), and the fail-closed class-aware HALT filter.
    Each section surfaces >=1 operator-specific input read by field name from the
    summary. Thin-library and no-specialist domains render the shared coverage-gap
    disclosure rather than a fabricated regimen.

    Args:
        goal_set (list): The in-scope goal-domains to compose.
        summary (dict): The `router.summarize` name-addressable operator-state summary
            — `assemble`'s ONLY operator-state source (crit 7). Read by field name.
        roster (dict): The injected specialist registry {domain: specialist callable}.

    Returns:
        (dict) One attributed plan document `{"sections": [...]}` — exactly one
        section per in-scope domain, each naming its specialist and surfacing >=1
        operator input; every recommendation complete + attributed + transit-marked;
        animal/in-vitro recs flagged population-mismatch; thin-library / no-specialist
        domains rendering the shared coverage-gap; 0 cross-domain claims sourced by no
        single specialist; 0 recommendation's actionable content contradicting a stated
        hard limit (struck fail-closed).
    """
    prohibited_classes = _prohibited_classes(summary)
    personalization = _personalize(summary)
    sections = []

    for domain in goal_set:
        specialist = roster.get(domain)

        # crit 5: a domain absent from the roster renders gap-by-absence, never dropped.
        if specialist is None:
            sections.append(_coverage_gap(domain, NO_SPECIALIST_GAP, personalization))
            continue

        output = specialist(domain, summary)
        specialist_name = output.get("specialist")

        # crit 4: thin-library coverage renders the shared gap, never a fabricated regimen.
        if output.get("thin_library"):
            sections.append(
                _coverage_gap(domain, THIN_LIBRARY_GAP, personalization, specialist_name)
            )
            continue

        emitted = []
        for rec in output.get("recommendations", []):
            # crit 6: a cross-domain claim sourced by no single specialist is rejected.
            if _is_cross_domain(rec):
                continue
            claim = _compose_claim(rec, specialist_name, summary, prohibited_classes)
            if claim is not None:
                emitted.append(claim)

        # Security LOW 5-4: a section with no surviving recommendations (none supplied,
        # or all dropped by the sourcing filter) renders the shared coverage-gap
        # disclosure rather than a silent empty section.
        if not emitted:
            sections.append(
                _coverage_gap(domain, EMPTY_OUTPUT_GAP, personalization, specialist_name)
            )
            continue

        sections.append({
            "domain": domain,
            "specialist": specialist_name,
            "recommendations": emitted,
            "personalization": personalization,
        })

    return {"sections": sections}
