"""Cross-domain plan orchestrator + reconciler — the step-4 integration terminal function.

The `/generate-plan` orchestrator's reconciliation job (design
`vault/design/plan-generation-pipeline-v1.md` decision 4: "two terminal functions, not
one") — find overlaps, bounce plans back, integrate — kept DISTINCT from the medical-liaison
clinical safety adjudication (`scripts/plan/adjudicate.py`), which the orchestrator invokes as
the terminal gate over a held additive-AE finding.

Under runtime A the orchestrator dispatches each plan-domain author, captures their output,
computes each domain's candidate plan via `generate_plan.compute_plan` (no record yet),
reconciles across domains, then records the reconciled set via `record_plan`. Recording is
held until after reconciliation so a cross-domain check can stop an unsafe / un-fuelable plan
from ever being written. The five cross-domain behaviors in this slice:

  1. RED-S/LEA cross-domain short-circuit (pipeline Phase 0.5): the nutritionist's
     critical-floor screen short-circuits ALL energy-deficit content — nutrition AND workout —
     to clinical-care routing. The single-domain veto already holds nutrition; the reconciler
     extends it to also hold the energy-prescribing workout plan.
  2. The nutrition->workout energy BOUNCE (Phase 2 joint constraint): the nutritionist is
     dispatched WITH the workout plan's energy cost and returns an energy-budget verdict; when
     the verdict says the load is unsustainable (`sustains` is False), the reconciler bounces
     the workout and the orchestrator re-authors it ONCE under the sustainable-energy ceiling.
     The re-authored plan is recorded only if its load honors the ceiling; otherwise the
     workout is HELD (never an un-fuelable load — the honest no-plan state).
  3. Cross-domain OVERLAP detection + author-CONFLICT adjudication (the step-4 integration):
     an intervention identity surfacing in 2+ domains is surfaced in the report (detect-only). An
     author-declared cross-domain conflict is surfaced AND HOLDS the declaring (`from`) domain
     pending the liaison gate (`cfaj`) — the safe default, like behavior 4; `generate_plans` routes
     each conflict-held domain to `adjudicate`, and a content-valid override releases it.
  4. Supplement<->peptide additive-AE screen (pipeline Phase 3, the compound band): each
     compound passes its single-domain filters, but their COMBINATION is not presumed safe
     ("component tolerability does not compose to combination safety" — peptide-specialist
     Rule 7). Bidirectional: a SHARED author-declared additive-AE class, or an author-declared
     pairwise interaction naming the other compound, is an additive-AE finding — surfaced in the
     report AND holding the SUPPLEMENT (the side that finalizes last against the settled compound
     surface) from recording: the honest no-stack state, never an un-screened additive-AE
     combination written. The medical-liaison terminal gate (`adjudicate`) then adjudicates the
     held finding: a content-valid override releases the supplement, a non-overridable / invalid
     adjudication leaves it held.
  5. Supplement<->Rx BPMH screen (pipeline Phase 4, the medical-liaison's marquee watchlist check —
     `rxbp`): each compound-bearing domain (supplements AND peptides) whose author-declared additive-AE
     classes intersect the operator's PRESENT Rx-interaction classes — read de-identified through the
     `router.summarize` PII boundary (the curated `rx-interaction-classes` field, never raw drug names)
     — is HELD pending the liaison gate (`adjudicate`, the SAME gate), the safe default. The hold is
     tracked in its OWN set (`rx_bpmh_held`), independent of the other holds; each concern clears on its
     own. No pharmacology DB enters the orchestrator: the drug-name -> interaction-class de-identification
     is an operator/liaison CURATION step at the store layer.

The reconciliation report is RETURNED (not persisted — no new store stream); plans are
recorded via the existing `record_plan` (the store-adversarial battery surface is unchanged).
"""

from scripts.plan import router
from scripts.plan.adjudicate import adjudicate
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.store import plan_schema, queue_schema

# Reconciler hold reasons: a candidate computed a plan, but a cross-domain check holds it from
# recording — the honest no-plan state, never an unsafe / un-fuelable plan on the dashboard.
ENERGY_BOUNCE_HELD = "energy-bounce-held"  # bounced, and no re-author hook was available
ENERGY_BOUNCE_UNRESOLVED = "energy-bounce-unresolved"  # the re-author did not honor the ceiling
RED_S_LEA_CROSS_DOMAIN = RED_S_LEA_CLINICAL_ROUTING  # the nutrition screen short-circuits workout
ADDITIVE_AE_HELD = "additive-ae-held"  # supplement<->peptide additive-AE risk holds the supplement
CONFLICT_HELD = "cross-domain-conflict-held"  # an author-declared cross-domain conflict holds the declarer
RX_BPMH_HELD = "rx-bpmh-held"  # a compound's additive-AE class stacks against an operator Rx-interaction class


def _compound_identities(candidate):
    """The compound identities a candidate plan contributes to overlap detection.

    Supplements contribute each item `name`; peptides contribute the single `compound`. Other
    domains contribute none — workout exercises and nutrition meals are not the cross-compound
    interventions overlap detection concerns. Identities are lowercased + whitespace-stripped
    for case/spacing-insensitive matching.

    Args:
        candidate (dict): A `compute_plan` result.

    Returns:
        (list) The normalized intervention identities (possibly empty).
    """
    plan = candidate.get("plan")
    if not isinstance(plan, dict):
        return []
    names = []
    if candidate.get("domain") == "supplements":
        for item in plan.get("items", []):
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                names.append(item["name"])
    elif candidate.get("domain") == "peptides":
        compound = plan.get("compound")
        if isinstance(compound, str):
            names.append(compound)
    return [n.strip().lower() for n in names if n.strip()]


def _ae_profile(candidate):
    """The author-declared additive-AE profile a compound candidate contributes to the screen.

    The compound author declares it in the `reconciliation` envelope (lifted into the candidate
    `meta` by `compute_plan`): `ae_profile.additive_classes` is the list of AE-class tokens the
    compound contributes (the supplement/peptide specialists' own vocabulary — `bleeding-risk`,
    `serotonergic`, `hepatotoxicity`, `malignancy-risk`, `cyp3a4-pgp`, …), and
    `ae_profile.interactions` is the list of author-declared pairwise interactions. A candidate
    that declared none — or a present-but-malformed declaration (an `ae_profile` that is not a
    dict; `additive_classes`/`interactions` of the wrong type) — contributes an EMPTY profile
    (no finding). This is the deliberate trusted-author contract: the screen reads the structured
    declaration the careful specialist authored, and a malformed one is treated as no declaration
    rather than guessed at. The contract shape is documented in
    `docs/plan-generation/author-dispatch-process.md`; tightening this to fail-loud is a deferred
    hardening candidate (the liaison gate adjudicates the held finding, not the declaration's shape).

    Args:
        candidate (dict): A `compute_plan` result.

    Returns:
        (dict) The `ae_profile` dict, or `{}` when none was declared (or it was malformed).
    """
    profile = (candidate.get("meta") or {}).get("ae_profile")
    return profile if isinstance(profile, dict) else {}


def _normalized_ae_classes(profile):
    """The normalized `additive_classes` token set from an `ae_profile` (lowercased, stripped)."""
    classes = profile.get("additive_classes")
    if not isinstance(classes, list):
        return set()
    return {c.strip().lower() for c in classes if isinstance(c, str) and c.strip()}


def _declared_interaction_findings(profile, declaring_domain, other_identities):
    """The declaring domain's interactions that NAME the other compound (the identity-match path).

    A pairwise interaction fires only when its `with` resolves to one of the other compound's
    identities (the specific compound, not a class — the shared-class path covers class-level
    additivity). Normalized for case/spacing-insensitive matching, mirroring the overlap check.

    Args:
        profile (dict): The declaring domain's `ae_profile`.
        declaring_domain (str): The domain that declared the interactions (the authoritative
            `from`, pinned by the orchestrator so an author-supplied `from` cannot shadow it).
        other_identities (set): The other compound's normalized identities.

    Returns:
        (list) One finding per matched interaction.
    """
    findings = []
    interactions = profile.get("interactions")
    if not isinstance(interactions, list):
        return findings
    for interaction in interactions:
        if not isinstance(interaction, dict):
            continue
        target = interaction.get("with")
        if isinstance(target, str) and target.strip().lower() in other_identities:
            findings.append({
                "kind": "declared-interaction", "from": declaring_domain,
                "with": target.strip().lower(), "mechanism": interaction.get("mechanism"),
                "severity": interaction.get("severity"),
            })
    return findings


def _additive_ae_findings(supplement, peptide):
    """The supplement<->peptide additive-AE findings (the Phase-3 compound-band screen).

    Bidirectional, two detection paths: (a) a SHARED additive-AE class both compounds declare —
    additive in combination even though each cleared its single-domain filters; (b) an
    author-declared pairwise interaction (from either side) that names the other compound. Pure
    over the two candidates; the orchestrator holds the supplement when this is non-empty.

    Args:
        supplement (dict): The supplements `compute_plan` candidate (a recorded plan).
        peptide (dict): The peptides `compute_plan` candidate (a recorded plan).

    Returns:
        (list) The additive-AE findings (empty when the combination is clean).
    """
    supp_profile = _ae_profile(supplement)
    pep_profile = _ae_profile(peptide)
    findings = []
    for ae_class in sorted(_normalized_ae_classes(supp_profile) & _normalized_ae_classes(pep_profile)):
        findings.append({"kind": "shared-class", "ae_class": ae_class,
                         "between": ["peptides", "supplements"]})
    supp_identities = set(_compound_identities(supplement))
    pep_identities = set(_compound_identities(peptide))
    findings.extend(_declared_interaction_findings(supp_profile, "supplements", pep_identities))
    findings.extend(_declared_interaction_findings(pep_profile, "peptides", supp_identities))
    return findings


def _additive_ae_safety_finding(findings):
    """The `safety_finding` the orchestrator routes to the medical-liaison for a held additive-AE.

    Distills the reconciler's additive-AE findings into the held-finding the liaison adjudicates
    (`scripts/plan/adjudicate.py`): a deterministic `finding_id` (so the liaison envelope can echo
    it) and a `caution` the override record must reproduce verbatim. The held domain is always the
    supplement (the side the screen holds).

    Args:
        findings (list): The reconciler's `report["additive_ae"]` findings (non-empty).

    Returns:
        (dict) `finding_id`, `source`, `held_domain`, `caution`, and the raw `findings`.
    """
    shared = sorted(f["ae_class"] for f in findings if f.get("kind") == "shared-class")
    interactions = sorted(
        f"{f['from']}->{f['with']}" for f in findings if f.get("kind") == "declared-interaction"
    )
    tokens = [f"class:{c}" for c in shared] + [f"interaction:{i}" for i in interactions]
    parts = []
    if shared:
        parts.append("shared additive-AE classes: " + ", ".join(shared))
    if interactions:
        parts.append("author-declared interactions: " + ", ".join(interactions))
    caution = "Supplement<->peptide additive adverse-event risk (" + "; ".join(parts) + ")"
    return {
        "finding_id": "additive-ae:" + ";".join(tokens),
        "source": "additive-ae", "held_domain": "supplements",
        "caution": caution, "findings": findings,
    }


def _conflict_safety_finding(from_domain, conflicts):
    """The `safety_finding` the orchestrator routes to the liaison for a held cross-domain conflict.

    Distills the declaring domain's author-declared conflicts (the `report["conflicts"]` entries with
    this `from`) into the held-finding the liaison adjudicates (`scripts/plan/adjudicate.py`): a
    deterministic `finding_id` (so the liaison envelope can echo it) and a `caution` the override
    record must reproduce verbatim. The held domain is the declaring (`from`) domain.

    Args:
        from_domain (str): The declaring domain whose plan is held.
        conflicts (list): That domain's conflict entries (`{with_domain, with, reason, from}`).

    Returns:
        (dict) `finding_id`, `source`, `held_domain`, `caution`, and the raw `conflicts`.
    """
    # Order the entries by (with_domain, with) so BOTH the finding_id tokens AND the caution detail
    # share one deterministic ordering — the caution must reproduce verbatim through the liaison, so an
    # order-stable caution keeps it regenerable. A malformed entry (no string `with`) is dropped from
    # the routing surface (trusted-author-malformed-is-inert, mirroring `_ae_profile`), never emitted
    # as a `None/None` token; it still rides the raw `conflicts` for the record.
    routable = sorted(
        (c for c in conflicts if isinstance(c.get("with"), str)),
        key=lambda c: (str(c.get("with_domain")), c.get("with")),
    )
    tokens = [f"{c.get('with_domain')}/{c['with']}" for c in routable]
    detail = "; ".join(f"{c['with']} ({c.get('with_domain')}) — {c.get('reason')}" for c in routable)
    return {
        "finding_id": "conflict:" + from_domain + ":" + ";".join(tokens),
        "source": "cross-domain-conflict", "held_domain": from_domain,
        "caution": f"Author-declared cross-domain conflict from {from_domain}: {detail}",
        "conflicts": conflicts,
    }


def _rx_bpmh_matched_classes(candidate, operator_rx_classes):
    """A compound's declared additive-AE classes that stack against the operator's present Rx classes.

    The supplement<->Rx BPMH screen (rxbp): a compound declares its additive-AE classes
    (`ae_profile.additive_classes`, the same canonical vocabulary the additive-AE screen uses); the
    operator's present medication interaction CLASSES come from the de-identified `rx-interaction-classes`
    summary field (operator/liaison-curated — never raw drug names). Their intersection is the BPMH
    finding: a supplement contributing `bleeding-risk` while the operator is on a `bleeding-risk`-class
    medication is the antithrombotic-stacking watchlist case. Pure over the candidate + the operator
    class set.

    Args:
        candidate (dict): A compound `compute_plan` candidate (supplements or peptides).
        operator_rx_classes (set): The operator's present Rx-interaction-class tokens (normalized).

    Returns:
        (set) The matched (shared) class tokens — empty when the compound is clean against the BPMH surface.
    """
    return _normalized_ae_classes(_ae_profile(candidate)) & set(operator_rx_classes)


def _rx_bpmh_safety_finding(held_domain, matched_classes):
    """The `safety_finding` the orchestrator routes to the liaison for a held supplement<->Rx BPMH finding.

    Distills the matched BPMH classes into the held-finding the liaison adjudicates
    (`scripts/plan/adjudicate.py`): a deterministic `finding_id` (so the liaison envelope can echo it) and
    a `caution` the override record must reproduce verbatim. The held domain is the compound domain whose
    declared class stacked against the operator's medication surface.

    Args:
        held_domain (str): The compound domain whose plan is held (supplements or peptides).
        matched_classes (set): The shared additive-AE / Rx-interaction class tokens (non-empty).

    Returns:
        (dict) `finding_id`, `source`, `held_domain`, `caution`, and the matched `classes`.
    """
    classes = sorted(matched_classes)
    detail = ", ".join(classes)
    return {
        "finding_id": "rx-bpmh:" + held_domain + ":" + ";".join(classes),
        "source": "rx-bpmh", "held_domain": held_domain,
        "caution": (
            f"Supplement<->Rx BPMH interaction: {held_domain} contributes additive-AE class(es) "
            f"{detail} that stack against the operator's present medication interaction class(es) {detail}"
        ),
        "classes": classes,
    }


def reconcile(candidates, *, operator_rx_classes=frozenset()):
    """Cross-domain reconciliation over the computed candidates (no recording).

    Pure over `candidates` (domain -> `compute_plan` result). Produces the reconciliation
    report plus the HOLD directives the orchestrator applies before recording (the energy
    bounce is RETURNED as a directive for the orchestrator to re-author, not applied as a hold
    here). See the module docstring for the five behaviors.

    Args:
        candidates (dict): domain -> `compute_plan` result, for the domains in this pass.
        operator_rx_classes (set, optional): The operator's present Rx-interaction-class tokens
            (from the de-identified `rx-interaction-classes` summary field — never raw drug names).
            Drives the supplement<->Rx BPMH screen (behavior 5, rxbp). Defaults to empty (no
            medication surface, no BPMH hold — the backward-compatible no-Rx default).

    Returns:
        (dict) `report` (`red_s_lea_cross_domain` bool, `bounce` dict | None, `overlaps` list,
        `conflicts` list, `additive_ae` list, `rx_bpmh` list); `holds` (domain -> hold reason —
        workout under a RED-S/LEA short-circuit, supplements under an additive-AE finding; the
        bounce-driven holds are applied by `generate_plans`); `conflict_held` (list of declaring
        domains held by an author-declared cross-domain conflict); and `rx_bpmh_held` (list of
        compound domains held by a supplement<->Rx BPMH finding). `conflict_held` and `rx_bpmh_held`
        are tracked INDEPENDENTLY of `holds` and of each other, so a domain can carry several
        concurrent concerns (an additive-AE hold AND a conflict AND a BPMH match), each cleared on
        its own — clearing one never releases a domain whose other concern is still open.
    """
    report = {"red_s_lea_cross_domain": False, "bounce": None, "overlaps": [],
              "conflicts": [], "additive_ae": [], "rx_bpmh": []}
    holds = {}
    conflict_held = []  # declaring domains held by an author-conflict — INDEPENDENT of `holds`
    rx_bpmh_held = []  # compound domains held by a supplement<->Rx BPMH match — INDEPENDENT of both

    nutrition = candidates.get("nutrition")
    workout = candidates.get("workout")
    workout_has_plan = workout is not None and workout.get("plan") is not None

    # 1. RED-S/LEA cross-domain short-circuit: a tripped nutrition critical-floor screen holds
    #    the energy-prescribing workout plan too (the screen short-circuits workout AND nutrition).
    if nutrition is not None and nutrition.get("reason") == RED_S_LEA_CLINICAL_ROUTING:
        report["red_s_lea_cross_domain"] = True
        if workout_has_plan:
            holds["workout"] = RED_S_LEA_CROSS_DOMAIN

    # 2. Energy bounce: nutrition's verdict says the load is unsustainable. Skip if the workout
    #    was already short-circuited above (a held plan has nothing to bounce).
    if "workout" not in holds and nutrition is not None and workout_has_plan:
        budget = (nutrition.get("meta") or {}).get("energy_budget")
        if isinstance(budget, dict) and budget.get("sustains") is False:
            report["bounce"] = {
                "target": "workout",
                "reason": "energy-budget-unsustainable",
                "sustainable_training_kcal": budget.get("sustainable_training_kcal"),
                "workout_cost_kcal": (workout.get("meta") or {}).get("energy_cost_kcal"),
            }

    # 3. Overlap detection: a compound identity surfacing in 2+ DISTINCT domains. Domains are
    #    deduped (a set) so a within-domain duplicate is not a false self-overlap, and so the entry
    #    aggregates to one record per identity (future-proof if a 3rd compound-bearing domain lands).
    seen = {}
    for domain, cand in candidates.items():
        for ident in _compound_identities(cand):
            seen.setdefault(ident, set()).add(domain)
    for ident, domains in seen.items():
        if len(domains) >= 2:
            report["overlaps"].append({"intervention": ident, "domains": sorted(domains)})

    # Author-declared cross-domain conflicts (cfaj): surfaced in the report AND the declaring domain
    # is HELD pending the liaison gate — the safe default (a flagged cross-domain conflict is not
    # shipped un-adjudicated), mirroring the additive-AE supplement hold. The orchestrator's `from`
    # (the declaring domain) is authoritative — spread LAST so an author-supplied `from` cannot shadow
    # the real source domain. The conflict hold is tracked in its OWN set (`conflict_held`), INDEPENDENT
    # of `holds`: a domain can carry both an additive-AE/RED-S-LEA/bounce hold AND a conflict, and each
    # concern must clear on its own — clearing one (e.g. an additive-AE override) must NOT release a
    # domain whose distinct conflict is still open. `generate_plans` adjudicates each conflict-held
    # domain; a content-valid override removes it from `conflict_held`; a domain records only when it is
    # in NEITHER `holds` NOR `conflict_held`.
    for domain, cand in candidates.items():
        domain_conflicts = (cand.get("meta") or {}).get("conflicts") or []
        for conflict in domain_conflicts:
            report["conflicts"].append({**conflict, "from": domain})
        if domain_conflicts and cand.get("plan") is not None:
            conflict_held.append(domain)

    # 4. Supplement<->peptide additive-AE screen (pipeline Phase 3): runs only when BOTH a
    #    supplement and a peptide candidate carry a plan (no recommended compound, no additive
    #    risk in THIS pass). A shared additive-AE class or an author-declared pairwise interaction
    #    holds the SUPPLEMENT (it finalizes last against the settled compound surface) — the honest
    #    no-stack state. `generate_plans` then routes the held finding to the liaison gate
    #    (`adjudicate`). The supplement<->Rx axis is the separate behavior 5 below (`rxbp`).
    supplement = candidates.get("supplements")
    peptide = candidates.get("peptides")
    if (
        supplement is not None and supplement.get("plan") is not None
        and peptide is not None and peptide.get("plan") is not None
    ):
        findings = _additive_ae_findings(supplement, peptide)
        if findings:
            report["additive_ae"] = findings
            holds["supplements"] = ADDITIVE_AE_HELD

    # 5. Supplement<->Rx BPMH screen (rxbp, pipeline Phase 4 — the medical-liaison's marquee
    #    watchlist check). Each compound-bearing domain (supplements AND peptides — the screen is
    #    symmetric; a peptide stacking with an operator anticoagulant is the same watchlist case as a
    #    supplement) whose declared additive-AE classes intersect the operator's PRESENT Rx-interaction
    #    classes is HELD pending the liaison gate — the safe default (a flagged medication-stacking
    #    interaction is not shipped un-adjudicated), mirroring the additive-AE supplement hold. The hold
    #    is tracked in its OWN set (`rx_bpmh_held`), INDEPENDENT of `holds` AND `conflict_held`: a compound
    #    can carry a BPMH match alongside an additive-AE hold and/or a conflict, and each concern clears on
    #    its own. `generate_plans` adjudicates each via the SAME gate; a content-valid override clears it.
    for domain in ("supplements", "peptides"):
        cand = candidates.get(domain)
        if cand is None or cand.get("plan") is None:
            continue
        matched = _rx_bpmh_matched_classes(cand, operator_rx_classes)
        if matched:
            report["rx_bpmh"].append({"held_domain": domain, "classes": sorted(matched)})
            rx_bpmh_held.append(domain)

    return {"report": report, "holds": holds, "conflict_held": conflict_held,
            "rx_bpmh_held": rx_bpmh_held}


def _held_result(candidate, reason):
    """A not-recorded result for a candidate a cross-domain hold suppressed."""
    return {
        "domain": candidate.get("domain"), "specialist": candidate.get("specialist"),
        "recorded": False, "plan": None, "section": candidate.get("section"), "reason": reason,
    }


def _recorded_result(candidate, plan_date, root):
    """Record a candidate's plan (if any) via `record_plan` and return its result record."""
    plan = candidate.get("plan")
    recorded = plan is not None
    if recorded:
        plan_schema.record_plan(
            candidate["domain"], plan, plan_date, candidate["specialist"], root
        )
    return {
        "domain": candidate.get("domain"), "specialist": candidate.get("specialist"),
        "recorded": recorded, "plan": plan, "section": candidate.get("section"),
        "reason": candidate.get("reason"),
    }


def generate_plans(authors, store_read, root, *, plan_date, gates=None, reauthor=None,
                   adjudicator=None):
    """Run all provided plan-domain authors as one reconciled pass and record the result.

    The `/generate-plan` orchestrator (runtime A): computes each domain's candidate via
    `compute_plan`, reconciles across domains (the RED-S/LEA cross-domain short-circuit + the
    nutrition->workout energy bounce + overlap detection + the supplement<->peptide additive-AE
    screen), applies a single bounce re-author when the energy budget is unsustainable, and
    records the surviving plans via `record_plan`. When a domain is held — under an additive-AE
    finding (supplements) OR an author-declared cross-domain conflict (`cfaj`, the declaring domain) —
    and an `adjudicator` is provided, the medical-liaison terminal gate (`adjudicate`) adjudicates the
    held finding: a content-valid override RELEASES the hold (the domain records); a non-overridable /
    invalid / absent adjudication leaves it HELD. Both axes reuse the SAME gate.

    Args:
        authors (dict): domain -> the captured author envelope, for the domains to run (1-4).
        store_read (Callable): The store read surface, instance-root pre-bound.
        root (str | Path): The store root the plans are recorded into.
        plan_date (str): The plans' YYYY-MM-DD date.
        gates (dict, optional): Per-domain safety inputs (`clearance_granted`, `red_s_lea_screen`)
            passed to every domain's `compute_plan`. Defaults to all-conservative.
        reauthor (Callable, optional): `reauthor(domain, constraint) -> author envelope | None` —
            the orchestrator's re-dispatch hook for an energy-bounced workout (runtime A: a second
            personal-trainer dispatch). `domain` is always `"workout"` in V1; `constraint` is
            `{"sustainable_training_kcal": <ceiling int>}`. The returned envelope MUST carry
            `reconciliation.energy_cost_kcal` for the ceiling check to pass — an envelope that omits
            it (or returns `None`, or whose cost still exceeds the ceiling) is held
            `energy-bounce-unresolved` (the safe no-plan state, not an error). When `reauthor` is
            absent, a bounced workout is held `energy-bounce-held` — never shipped as an un-fuelable
            load.
        adjudicator (Callable, optional): `adjudicator(safety_finding) -> liaison envelope | None`
            — the medical-liaison dispatch hook for a held finding (runtime A: a real `medical-liaison`
            dispatch, full profile inlined), called for the additive-AE finding, for each conflict-held
            domain's finding, AND for each supplement<->Rx BPMH-held compound's finding. The envelope is
            validated by `adjudicate`; a content-valid HIGH/MEDIUM override releases that domain's hold,
            a CRITICAL/H1-H2 auto-block or any invalid/absent envelope leaves it held. When absent, a
            held domain stays held — the safe default. All three axes reuse the SAME gate.

    Returns:
        (dict) `results` (domain -> result record, the `generate_plan` shape), `reconciliation`
        (the `reconcile` report), `reauthored` (bool — a bounce re-author ran), `adjudication`
        (the `adjudicate` outcome for a held additive-AE finding, or `None`),
        `conflict_adjudications` (declaring-domain -> `adjudicate` outcome for each conflict-held
        domain; `{}` when none ran), and `rx_bpmh_adjudications` (compound-domain -> `adjudicate`
        outcome for each supplement<->Rx BPMH-held domain; `{}` when none ran).
    """
    gates = gates or {}
    candidates = {
        domain: compute_plan(domain, author_output, store_read, gates=gates)
        for domain, author_output in authors.items()
    }

    # The operator's present Rx-interaction classes (de-identified, curated in the store; never raw
    # drug names) drive the supplement<->Rx BPMH screen. Derived once from the summary — the same
    # operator state every domain's `compute_plan` reads, so this is the canonical single read.
    operator_rx_classes = router.rx_interaction_class_set(router.summarize(store_read))

    outcome = reconcile(candidates, operator_rx_classes=operator_rx_classes)
    report = outcome["report"]
    holds = dict(outcome["holds"])
    conflict_held = set(outcome["conflict_held"])  # tracked independently of `holds`
    rx_bpmh_held = set(outcome["rx_bpmh_held"])  # tracked independently of `holds` and `conflict_held`
    reauthored = False

    bounce = report["bounce"]
    if bounce is not None:
        ceiling = bounce.get("sustainable_training_kcal")
        if reauthor is not None:
            new_output = reauthor("workout", {"sustainable_training_kcal": ceiling})
            new_candidate = compute_plan("workout", new_output, store_read, gates=gates)
            candidates["workout"] = new_candidate
            reauthored = True
            new_cost = (new_candidate.get("meta") or {}).get("energy_cost_kcal")
            # Hold (don't record) unless the re-author is provably fuelable. Two distinct hold
            # cases: (a) MALFORMED — no plan, or the bounce directive / re-author gave no ceiling
            # or no cost, so fuelability cannot be proven; (b) OVER-CEILING — `new_cost > ceiling`.
            # A held workout is the honest no-plan state, never an un-fuelable load on the dashboard.
            if (
                new_candidate.get("plan") is None
                or ceiling is None
                or new_cost is None
                or new_cost > ceiling
            ):
                holds["workout"] = ENERGY_BOUNCE_UNRESOLVED
        else:
            holds["workout"] = ENERGY_BOUNCE_HELD

    # Medical-liaison terminal adjudication (pipeline Phase 4): the additive-AE screen HOLDS the
    # supplement; the liaison adjudicates the held finding. A content-valid HIGH/MEDIUM override
    # RELEASES the hold (the supplement records); a CRITICAL/H1-H2 auto-block or an invalid/absent
    # adjudication leaves the block standing. The override record rides the returned `adjudication`,
    # not a new store stream. When no adjudicator is wired the supplement stays held (the safe
    # no-stack default — the S73 behavior).
    adjudication = None
    if holds.get("supplements") == ADDITIVE_AE_HELD and adjudicator is not None:
        safety_finding = _additive_ae_safety_finding(report["additive_ae"])
        adjudication = adjudicate(safety_finding, adjudicator(safety_finding))
        if adjudication["outcome"] == "cleared":
            del holds["supplements"]

    # Conflict adjudication (cfaj, pipeline Phase 4): each domain in the INDEPENDENT `conflict_held`
    # set is routed to the SAME liaison gate — INCLUDING a domain that ALSO carries a `holds` reason
    # (e.g. an additive-AE-held supplement that ALSO declared a distinct conflict). A content-valid
    # override clears the conflict (drops it from `conflict_held`); a non-overridable / invalid / absent
    # adjudication leaves the conflict open. Because `conflict_held` is independent of `holds`, clearing
    # one concern never releases a domain whose OTHER concern is still open — a domain records only when
    # it is in NEITHER set. When no adjudicator is wired, a conflict-held domain stays held (the safe
    # default). One adjudication per declaring domain (its conflicts aggregated into one safety_finding).
    conflict_adjudications = {}
    if adjudicator is not None:
        for domain in sorted(conflict_held):
            domain_conflicts = [c for c in report["conflicts"] if c.get("from") == domain]
            safety_finding = _conflict_safety_finding(domain, domain_conflicts)
            adjudication_outcome = adjudicate(safety_finding, adjudicator(safety_finding))
            conflict_adjudications[domain] = adjudication_outcome
            if adjudication_outcome["outcome"] == "cleared":
                conflict_held.discard(domain)

    # Supplement<->Rx BPMH adjudication (rxbp, pipeline Phase 4): each compound domain in the INDEPENDENT
    # `rx_bpmh_held` set is routed to the SAME liaison gate — INCLUDING a compound that ALSO carries a
    # `holds` reason (an additive-AE-held supplement) AND/OR an open conflict. A content-valid override
    # clears the BPMH concern (drops it from `rx_bpmh_held`); a non-overridable / invalid / absent
    # adjudication leaves it open. Because `rx_bpmh_held` is independent of the other two sets, clearing
    # one concern never releases a domain whose OTHER concern is still open — a domain records only when it
    # is in NONE of the three. When no adjudicator is wired, a BPMH-held domain stays held (the safe
    # default). One adjudication per held compound domain (its matched classes aggregated into one finding).
    rx_bpmh_adjudications = {}
    if adjudicator is not None:
        for domain in sorted(rx_bpmh_held):
            matched = next(f["classes"] for f in report["rx_bpmh"] if f["held_domain"] == domain)
            safety_finding = _rx_bpmh_safety_finding(domain, matched)
            adjudication_outcome = adjudicate(safety_finding, adjudicator(safety_finding))
            rx_bpmh_adjudications[domain] = adjudication_outcome
            if adjudication_outcome["outcome"] == "cleared":
                rx_bpmh_held.discard(domain)

    # A domain records only when it is in NONE of `holds` / `conflict_held` / `rx_bpmh_held`. A `holds`
    # reason takes the result's `reason`; otherwise an open conflict (CONFLICT_HELD) or BPMH match
    # (RX_BPMH_HELD) holds it — each an independent concern, any one of which suppresses recording.
    results = {}
    for domain, candidate in candidates.items():
        hold_reason = holds.get(domain)
        if hold_reason is None and domain in conflict_held:
            hold_reason = CONFLICT_HELD
        if hold_reason is None and domain in rx_bpmh_held:
            hold_reason = RX_BPMH_HELD
        if hold_reason is not None:
            results[domain] = _held_result(candidate, hold_reason)
        else:
            results[domain] = _recorded_result(candidate, plan_date, root)

    return {"results": results, "reconciliation": report, "reauthored": reauthored,
            "adjudication": adjudication, "conflict_adjudications": conflict_adjudications,
            "rx_bpmh_adjudications": rx_bpmh_adjudications}


def _queue_specialist(results, domain):
    """The specialist that authored a held domain's plan (the queue entry's source attribution)."""
    return (results.get(domain) or {}).get("specialist")


def _doctor_visit_queue_entry(safety_finding, adjudication, axis, source_specialist):
    """Build one doctor-visit-queue entry from a safety finding + its liaison adjudication.

    Carries the data-layer fields the SBAR handout's flagged-interactions section renders from
    (medical-liaison design §9.4 Background-3): the finding identity + verbatim caution, the held
    compound domain + its source specialist, the adjudication outcome, and the severity signal
    (`non_overridable` + the override record's `composite_band`, or `CRITICAL` for a non-overridable
    auto-block). No clinical verdict; the GRADE annotation is the liaison's to add at its dispatch
    (entries are open on extras).

    Args:
        safety_finding (dict): The reconciler's `safety_finding` (`finding_id` + `caution` + held domain).
        adjudication (dict): The `adjudicate` outcome for that finding.
        axis (str): The finding's axis (`additive-ae` | `cross-domain-conflict` | `rx-bpmh`).
        source_specialist (str | None): The held domain's authoring specialist.

    Returns:
        (dict) The queue entry.
    """
    override = adjudication.get("override_record") or {}
    non_overridable = bool(adjudication.get("non_overridable"))
    band = override.get("composite_band") or ("CRITICAL" if non_overridable else None)
    outcome = "cleared-with-override" if adjudication.get("outcome") == "cleared" else "block-stands"
    return {
        "finding_id": safety_finding["finding_id"],
        "axis": axis,
        "caution": safety_finding["caution"],
        "held_domain": safety_finding["held_domain"],
        "source_specialist": source_specialist,
        "outcome": outcome,
        "non_overridable": non_overridable,
        "composite_band": band,
    }


def collate_doctor_visit_queue(result, on_date, root):
    """Collate a `generate_plans` result's adjudicated safety findings into the doctor-visit queue.

    The medical-liaison's owned collation surface (design §2.2, §9.4): each safety finding the
    pipeline ADJUDICATED through the liaison gate — the additive-AE finding plus every conflict-held
    and Rx-BPMH-held domain's finding, whether the override CLEARED it or the block STANDS — is
    recorded as a severity-ranked queue entry via `queue_schema.record_doctor_visit_queue_entry`.
    Each finding is rebuilt with the SAME `safety_finding` builders the orchestrator routed to the
    gate (so the queued `finding_id` + `caution` match the adjudicated finding verbatim) and joined
    to its `adjudicate` outcome. A finding that never reached the gate (no adjudicator wired) is not
    queued here — only adjudicated dispositions land in the MD-facing queue. Pure collation: it reads
    the returned `result` and writes ONLY the `dvq::queue` stream (no plan stream touched).

    Args:
        result (dict): A `generate_plans` return value.
        on_date (str): The collation date, YYYY-MM-DD.
        root (str | Path): The store root.

    Returns:
        (list) The queue entries recorded this collation (in collation order, pre-rank).
    """
    report = result["reconciliation"]
    results = result["results"]
    recorded = []

    adjudication = result.get("adjudication")
    if adjudication is not None and report.get("additive_ae"):
        safety_finding = _additive_ae_safety_finding(report["additive_ae"])
        entry = _doctor_visit_queue_entry(
            safety_finding, adjudication, "additive-ae",
            _queue_specialist(results, safety_finding["held_domain"]),
        )
        queue_schema.record_doctor_visit_queue_entry(entry, on_date, root)
        recorded.append(entry)

    for domain, adjudication in result.get("conflict_adjudications", {}).items():
        domain_conflicts = [c for c in report["conflicts"] if c.get("from") == domain]
        safety_finding = _conflict_safety_finding(domain, domain_conflicts)
        entry = _doctor_visit_queue_entry(
            safety_finding, adjudication, "cross-domain-conflict", _queue_specialist(results, domain),
        )
        queue_schema.record_doctor_visit_queue_entry(entry, on_date, root)
        recorded.append(entry)

    for domain, adjudication in result.get("rx_bpmh_adjudications", {}).items():
        matched = next((f["classes"] for f in report["rx_bpmh"] if f["held_domain"] == domain), [])
        safety_finding = _rx_bpmh_safety_finding(domain, matched)
        entry = _doctor_visit_queue_entry(
            safety_finding, adjudication, "rx-bpmh", _queue_specialist(results, domain),
        )
        queue_schema.record_doctor_visit_queue_entry(entry, on_date, root)
        recorded.append(entry)

    return recorded
