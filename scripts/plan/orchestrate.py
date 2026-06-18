"""Cross-domain plan orchestrator + reconciler — the step-4 integration terminal function.

The `/generate-plan` orchestrator's reconciliation job (design
`vault/design/plan-generation-pipeline-v1.md` decision 4: "two terminal functions, not
one") — find overlaps, bounce plans back, integrate — kept DISTINCT from the medical-liaison
clinical safety adjudication (the deferred S73 slice).

Under runtime A the orchestrator dispatches each plan-domain author, captures their output,
computes each domain's candidate plan via `generate_plan.compute_plan` (no record yet),
reconciles across domains, then records the reconciled set via `record_plan`. Recording is
held until after reconciliation so a cross-domain check can stop an unsafe / un-fuelable plan
from ever being written. The three cross-domain behaviors in this slice:

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
     conflict. V1 DETECTS + REPORTS; the additive-AE screen and the medical-liaison
     contradiction adjudication are the S73 compound-safety slice, not this one.

The reconciliation report is RETURNED (not persisted — no new store stream); plans are
recorded via the existing `record_plan` (the store-adversarial battery surface is unchanged).
"""

from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.store import plan_schema

# Reconciler hold reasons: a candidate computed a plan, but a cross-domain check holds it from
# recording — the honest no-plan state, never an unsafe / un-fuelable plan on the dashboard.
ENERGY_BOUNCE_HELD = "energy-bounce-held"  # bounced, and no re-author hook was available
ENERGY_BOUNCE_UNRESOLVED = "energy-bounce-unresolved"  # the re-author did not honor the ceiling
RED_S_LEA_CROSS_DOMAIN = RED_S_LEA_CLINICAL_ROUTING  # the nutrition screen short-circuits workout


def _intervention_identities(candidate):
    """The intervention identities a candidate plan contributes to overlap detection.

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


def reconcile(candidates):
    """Cross-domain reconciliation over the computed candidates (no recording).

    Pure over `candidates` (domain -> `compute_plan` result). Produces the reconciliation
    report plus the HOLD directives the orchestrator applies before recording (the energy
    bounce is RETURNED as a directive for the orchestrator to re-author, not applied as a hold
    here). See the module docstring for the three behaviors.

    Args:
        candidates (dict): domain -> `compute_plan` result, for the domains in this pass.

    Returns:
        (dict) `report` (`red_s_lea_cross_domain` bool, `bounce` dict | None, `overlaps` list,
        `conflicts` list) and `holds` (domain -> hold reason — workout under a RED-S/LEA
        short-circuit; the bounce-driven holds are applied by `generate_plans`).
    """
    report = {"red_s_lea_cross_domain": False, "bounce": None, "overlaps": [], "conflicts": []}
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

    # 3. Overlap detection across the intervention-bearing domains.
    seen = {}
    for domain, cand in candidates.items():
        for ident in _intervention_identities(cand):
            seen.setdefault(ident, []).append(domain)
    for ident, domains in seen.items():
        if len(domains) >= 2:
            report["overlaps"].append({"intervention": ident, "domains": sorted(domains)})

    # author-declared cross-domain conflicts: surfaced, not adjudicated (the S73 liaison gate).
    for domain, cand in candidates.items():
        for conflict in (cand.get("meta") or {}).get("conflicts") or []:
            report["conflicts"].append({"from": domain, **conflict})

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


def generate_plans(authors, store_read, root, *, plan_date, gates=None, reauthor=None):
    """Run all provided plan-domain authors as one reconciled pass and record the result.

    The `/generate-plan` orchestrator (runtime A): computes each domain's candidate via
    `compute_plan`, reconciles across domains (the RED-S/LEA cross-domain short-circuit + the
    nutrition->workout energy bounce + overlap detection), applies a single bounce re-author
    when the energy budget is unsustainable, and records the surviving plans via `record_plan`.

    Args:
        authors (dict): domain -> the captured author envelope, for the domains to run (1-4).
        store_read (Callable): The store read surface, instance-root pre-bound.
        root (str | Path): The store root the plans are recorded into.
        plan_date (str): The plans' YYYY-MM-DD date.
        gates (dict, optional): Per-domain safety inputs (`clearance_granted`, `red_s_lea_screen`)
            passed to every domain's `compute_plan`. Defaults to all-conservative.
        reauthor (Callable, optional): `reauthor(domain, constraint) -> author envelope` — the
            orchestrator's re-dispatch hook for an energy-bounced workout (runtime A: a second
            personal-trainer dispatch under the `{"sustainable_training_kcal": ceiling}`
            constraint). When absent, a bounced workout is HELD (not recorded), never shipped as
            an un-fuelable load.

    Returns:
        (dict) `results` (domain -> result record, the `generate_plan` shape), `reconciliation`
        (the `reconcile` report), and `reauthored` (bool — a bounce re-author ran).
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
            # The re-author must bring the session load under the sustainable ceiling; if it
            # produced no plan, gave no cost, or stayed over the ceiling, hold (don't record).
            if (
                new_candidate.get("plan") is None
                or ceiling is None
                or new_cost is None
                or new_cost > ceiling
            ):
                holds["workout"] = ENERGY_BOUNCE_UNRESOLVED
        else:
            holds["workout"] = ENERGY_BOUNCE_HELD

    results = {}
    for domain, candidate in candidates.items():
        hold_reason = holds.get(domain)
        if hold_reason is not None:
            results[domain] = _held_result(candidate, hold_reason)
        else:
            results[domain] = _recorded_result(candidate, plan_date, root)

    return {"results": results, "reconciliation": report, "reauthored": reauthored}
