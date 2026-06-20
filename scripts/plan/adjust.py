"""The ADJUST leg of the closed loop (plan -> act -> measure -> ADJUST).

`design/vision.md`: the system "closes the loop -- plan -> act -> measure -> adjust", so each
plan is backed by what actually happened. The plan leg records `plan::<domain>`
(`generate_plan`), the measure leg records the tracking snapshot (`track.record_tracking`),
and the read-back joins them into the plan-vs-actual view (`track.resolve_plan_progress`).
This module wires the LAST leg: the domain-specific PROGRESSION -- re-authoring an ADJUSTED
plan from the progress (de-load / advance / hold).

Runtime A (the pipeline's interactive agent-dispatch model, `vault/design/
plan-generation-pipeline-v1.md`): the de-load/advance REASONING is the domain SPECIALIST'S,
authored at dispatch over the plan-vs-actual progress -- it is NOT computed here (the
progression is a clinical/coaching judgment, never invented in `scripts/`). This module is the
production caller that (a) reads the progress for the honest "nothing to progress from"
boundary, and (b) records the specialist's adjusted author output via the SAME `generate_plan`
path -- so `assemble`'s four safety filters + the workout clearance gate apply to the re-plan
EXACTLY as to the initial plan (the safety floor is never bypassed on adjust). The orchestrator
dispatches the specialist with the progress (`docs/plan-generation/adjust-dispatch-process.md`)
and feeds the captured output here.

Adjusting requires BOTH a prior plan AND a tracking snapshot (the tracked actual): no prior
plan is generate, not adjust; a plan with no tracking is no actual to progress from. Either
absent -> records nothing and returns the honest no-progress-to-adjust boundary, never a
fabricated adjustment. The adjusted plan records as a NEW dated plan (`adjust_date`) -- the
prior plan + tracking are immutable history, and `resolve_plan_progress` at the new date reads
the adjusted prescription.

REUSE only: this module reads `track.resolve_plan_progress` and records via
`generate_plan.generate_plan` -- it defines no store key, records no plan directly, and leaves
the plan/tracking streams + the safety filters unchanged. Writers raise only ValueError.
"""

from scripts.plan import generate_plan as gp
from scripts.plan import track
from scripts.store import plan_schema

# Adjust result states. The progression records only when there is progress to adjust FROM (a
# prior plan AND a tracking snapshot); the adjusted plan then rides `generate_plan`'s full
# recording path, so a struck / coverage-gap / no-actionable re-plan surfaces generate_plan's
# own `reason` rather than a fabricated adjustment.
ADJUSTED = "adjusted"
NO_PLAN_TO_ADJUST_FROM = "no-plan-to-adjust-from"
NO_TRACKING_TO_ADJUST_FROM = "no-tracking-to-adjust-from"


def adjust_plan(domain, author_output, store_read, root, *, prior_date, adjust_date, gates=None):
    """Re-author + record an ADJUSTED plan from the plan-vs-actual progress (the ADJUST leg).

    Reads the prior plan-vs-actual progress (`track.resolve_plan_progress` at `prior_date`) for
    the honest "nothing to progress from" boundary -- adjusting requires BOTH a prior plan AND a
    tracking snapshot, else there is no progress to adjust from. When progress exists, records the
    specialist's ADJUSTED `author_output` (the de-load/advance reasoning the specialist authored
    at dispatch over the progress) via the REUSED `generate_plan` as a NEW dated plan for
    `adjust_date` -- the same path the initial plan took, so the four `assemble` safety filters +
    the workout clearance gate apply to the re-plan too (a struck / coverage-gap / no-actionable
    adjusted plan records nothing and surfaces generate_plan's `reason`, never a bypassed floor).

    Args:
        domain (str): A `plan_schema.TRACKED_DOMAINS` member (workout / nutrition / supplements --
            peptide progression is not this surface; peptide tracking is the watch-out stream).
        author_output (dict): The captured ADJUSTED author envelope -- `{"specialist": slug,
            "recommendations": [...]}` or the thin-library sentinel (the same contract
            `generate_plan` consumes). The specialist authored it at dispatch over the progress.
        store_read (Callable): The store read surface, instance-root pre-bound (the
            `router.summarize` caller contract).
        root (str | Path): The store root the adjusted plan is recorded into.
        prior_date (str): The YYYY-MM-DD date of the plan whose progress is being adjusted FROM
            (the date `resolve_plan_progress` reads the plan + tracking at).
        adjust_date (str): The YYYY-MM-DD date the adjusted plan is recorded UNDER (the new
            prescription's date; typically forward of `prior_date`).
        gates (dict, optional): Per-domain safety inputs forwarded to `generate_plan`
            (`clearance_granted`, `red_s_lea_screen`). Defaults to all-conservative.

    Returns:
        (dict) A result record: `domain`, `prior_date`, `adjust_date`, `state` (`adjusted` |
        `no-plan-to-adjust-from` | `no-tracking-to-adjust-from` | a `generate_plan` reason when
        the adjusted plan was filtered out), `adjusted` (bool -- whether a plan was recorded),
        `plan` (the recorded adjusted plan dict | None), `reason` (the generate_plan reason |
        None), and `adjusted_from` (the prior plan + tracking + plan_date + specialist the
        progression adjusted from -- the provenance, never None on the record path).

    Raises:
        ValueError: An untracked domain (always). And -- ONLY on the record path (progress exists)
            -- a `record_plan` rejection of the adjusted plan (a schema-nonconformant translated
            plan, or omitted attribution), surfaced loud by `generate_plan`, never silently dropped.
    """
    if domain not in plan_schema.TRACKED_DOMAINS:
        raise ValueError(
            f"untracked plan domain {domain!r}; known: {plan_schema.TRACKED_DOMAINS}"
        )
    progress = track.resolve_plan_progress(domain, prior_date, root)

    def result(state, adjusted, plan, reason):
        return {
            "domain": domain, "prior_date": prior_date, "adjust_date": adjust_date,
            "state": state, "adjusted": adjusted, "plan": plan, "reason": reason,
            "adjusted_from": {
                "plan": progress["plan"], "tracking": progress["tracking"],
                "plan_date": progress["plan_date"], "specialist": progress["specialist"],
            },
        }

    # The honest "nothing to progress from" boundary, deciding the full has_plan x has_tracking
    # domain: no prior plan -> generate, not adjust; a plan with no tracking -> the operator has
    # not logged, so there is no tracked actual to progress from. Either absent records nothing.
    if not progress["has_plan"]:
        return result(NO_PLAN_TO_ADJUST_FROM, False, None, None)
    if not progress["has_tracking"]:
        return result(NO_TRACKING_TO_ADJUST_FROM, False, None, None)

    # Progress exists -> record the specialist's ADJUSTED output via the SAME generate_plan path
    # (the safety floor applies to the re-plan exactly as to the initial plan).
    gp_result = gp.generate_plan(
        domain, author_output, store_read, root, plan_date=adjust_date, gates=gates
    )
    state = ADJUSTED if gp_result["recorded"] else gp_result["reason"]
    return result(state, gp_result["recorded"], gp_result["plan"], gp_result["reason"])
