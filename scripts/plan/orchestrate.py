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
from ever being written. The four cross-domain behaviors in this slice:

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
  3. Cross-domain OVERLAP detection (the step-4 integration): an intervention identity
     surfacing in 2+ domains (a compound recommended as both a supplement and a peptide) is
     surfaced in the reconciliation report, alongside any author-declared cross-domain
     conflict. This pass DETECTS + REPORTS; adjudicating the conflict axis through the liaison
     gate is the beaded follow-on `cfaj` (this slice closes the additive-AE axis, behavior 4).
  4. Supplement<->peptide additive-AE screen (pipeline Phase 3, the compound band): each
     compound passes its single-domain filters, but their COMBINATION is not presumed safe
     ("component tolerability does not compose to combination safety" — peptide-specialist
     Rule 7). Bidirectional: a SHARED author-declared additive-AE class, or an author-declared
     pairwise interaction naming the other compound, is an additive-AE finding — surfaced in the
     report AND holding the SUPPLEMENT (the side that finalizes last against the settled compound
     surface) from recording: the honest no-stack state, never an un-screened additive-AE
     combination written. The medical-liaison terminal gate (`adjudicate`) then adjudicates the
     held finding: a content-valid override releases the supplement, a non-overridable / invalid
     adjudication leaves it held. The supplement<->Rx axis is the beaded follow-on `rxbp`.

The reconciliation report is RETURNED (not persisted — no new store stream); plans are
recorded via the existing `record_plan` (the store-adversarial battery surface is unchanged).
"""

from scripts.plan.adjudicate import adjudicate
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.store import plan_schema

# Reconciler hold reasons: a candidate computed a plan, but a cross-domain check holds it from
# recording — the honest no-plan state, never an unsafe / un-fuelable plan on the dashboard.
ENERGY_BOUNCE_HELD = "energy-bounce-held"  # bounced, and no re-author hook was available
ENERGY_BOUNCE_UNRESOLVED = "energy-bounce-unresolved"  # the re-author did not honor the ceiling
RED_S_LEA_CROSS_DOMAIN = RED_S_LEA_CLINICAL_ROUTING  # the nutrition screen short-circuits workout
ADDITIVE_AE_HELD = "additive-ae-held"  # supplement<->peptide additive-AE risk holds the supplement


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


def reconcile(candidates):
    """Cross-domain reconciliation over the computed candidates (no recording).

    Pure over `candidates` (domain -> `compute_plan` result). Produces the reconciliation
    report plus the HOLD directives the orchestrator applies before recording (the energy
    bounce is RETURNED as a directive for the orchestrator to re-author, not applied as a hold
    here). See the module docstring for the four behaviors.

    Args:
        candidates (dict): domain -> `compute_plan` result, for the domains in this pass.

    Returns:
        (dict) `report` (`red_s_lea_cross_domain` bool, `bounce` dict | None, `overlaps` list,
        `conflicts` list, `additive_ae` list) and `holds` (domain -> hold reason — workout under
        a RED-S/LEA short-circuit, supplements under an additive-AE finding; the bounce-driven
        holds are applied by `generate_plans`).
    """
    report = {"red_s_lea_cross_domain": False, "bounce": None, "overlaps": [],
              "conflicts": [], "additive_ae": []}
    holds = {}

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

    # author-declared cross-domain conflicts: surfaced, not adjudicated (the conflict-axis follow-on
    # `cfaj` routes these through the liaison gate). The orchestrator's `from` (the declaring domain)
    # is authoritative — it is spread LAST so an
    # author-supplied `from` in the conflict dict cannot shadow the real source domain.
    for domain, cand in candidates.items():
        for conflict in (cand.get("meta") or {}).get("conflicts") or []:
            report["conflicts"].append({**conflict, "from": domain})

    # 4. Supplement<->peptide additive-AE screen (pipeline Phase 3): runs only when BOTH a
    #    supplement and a peptide candidate carry a plan (no recommended compound, no additive
    #    risk in THIS pass). A shared additive-AE class or an author-declared pairwise interaction
    #    holds the SUPPLEMENT (it finalizes last against the settled compound surface) — the honest
    #    no-stack state. `generate_plans` then routes the held finding to the liaison gate
    #    (`adjudicate`); the supplement<->Rx axis is the beaded follow-on `rxbp`.
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

    return {"report": report, "holds": holds}


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
    records the surviving plans via `record_plan`. When a supplement is held under an additive-AE
    finding and an `adjudicator` is provided, the medical-liaison terminal gate (`adjudicate`)
    adjudicates the held finding: a content-valid override RELEASES the hold (the supplement
    records); a non-overridable / invalid / absent adjudication leaves it HELD.

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
            — the medical-liaison dispatch hook for a held additive-AE finding (runtime A: a real
            `medical-liaison` dispatch, full profile inlined). The envelope is validated by
            `adjudicate`; a content-valid HIGH/MEDIUM override releases the supplement hold, a
            CRITICAL/H1-H2 auto-block or any invalid/absent envelope leaves the block standing. When
            absent, a held additive-AE supplement stays held — the safe no-stack default.

    Returns:
        (dict) `results` (domain -> result record, the `generate_plan` shape), `reconciliation`
        (the `reconcile` report), `reauthored` (bool — a bounce re-author ran), and `adjudication`
        (the `adjudicate` outcome for a held additive-AE finding, or `None` when none ran).
    """
    gates = gates or {}
    candidates = {
        domain: compute_plan(domain, author_output, store_read, gates=gates)
        for domain, author_output in authors.items()
    }

    outcome = reconcile(candidates)
    report = outcome["report"]
    holds = dict(outcome["holds"])
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

    results = {}
    for domain, candidate in candidates.items():
        hold_reason = holds.get(domain)
        if hold_reason is not None:
            results[domain] = _held_result(candidate, hold_reason)
        else:
            results[domain] = _recorded_result(candidate, plan_date, root)

    return {"results": results, "reconciliation": report, "reauthored": reauthored,
            "adjudication": adjudication}
