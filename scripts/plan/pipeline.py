"""The GENERATE-leg production caller -- the `/generate-plan` invocation seam.

`design/vision.md`: the system "closes the loop -- plan -> act -> measure -> adjust". This module
wires the GENERATE leg end-to-end: `orchestrate.generate_plans` runs the reconciled multi-domain
pass (compute every domain's candidate -> reconcile across domains -> adjudicate any held finding
-> record the survivors), and `orchestrate.collate_doctor_visit_queue` collates the adjudicated
safety findings into the `dvq::queue`. Until this seam, `generate_plans` had NO production caller --
the cross-domain terminal was wired + unit-tested but never invoked end-to-end. This is the
INV-CORE-CAPABILITY pattern applied to the orchestrator terminal: `generate_plan` is `assemble`'s
production caller; `run_generation` is `generate_plans` + `collate`'s.

Runtime A (`vault/design/plan-generation-pipeline-v1.md`): the orchestrator dispatches each
plan-domain specialist (the `/generate-plan` skill, full profiles inlined), captures their output
into `authors`, and calls this. The `reauthor` + `adjudicator` hooks are the orchestrator's LIVE
re-dispatch seams -- a second personal-trainer dispatch for an energy bounce; a medical-liaison
dispatch for a held finding -- forwarded UNCHANGED to `generate_plans`. The plan + safety reasoning
is the specialists'/liaison's, never invented here; this seam is the wiring + the collation, and
records nothing the reconciler + the gates did not pass.

REUSE only: calls `orchestrate.generate_plans` + `orchestrate.collate_doctor_visit_queue` -- it
defines no store key, records no plan directly, and leaves the reconciler + the safety gates
unchanged.
"""

from scripts.plan import orchestrate


def run_generation(authors, store_read, root, *, plan_date, on_date=None, gates=None,
                   reauthor=None, adjudicator=None):
    """Run the reconciled multi-domain GENERATE pass + collate the doctor-visit queue (one pass).

    The closed loop's GENERATE leg end-to-end: records the reconciled plans (`plan::<domain>`, only
    the domains the reconciler + the safety gates passed) AND the adjudicated safety findings
    (`dvq::queue`). The `reauthor`/`adjudicator` hooks are forwarded to `generate_plans` verbatim --
    a bounced workout with no fuelable re-author is HELD (never an un-fuelable load), and a held
    additive-AE / cross-domain-conflict / Rx-BPMH finding records only when `adjudicate` releases it
    (the safety floor is reused, never bypassed).

    Args:
        authors (dict): domain -> the captured author envelope, for the `PLAN_DOMAINS` to run (1-4).
        store_read (Callable): The store read surface, instance-root pre-bound (the
            `router.summarize` caller contract).
        root (str | Path): The store root the plans + the queue are recorded into.
        plan_date (str): The plans' YYYY-MM-DD date.
        on_date (str, optional): The doctor-visit-queue collation date. Defaults to `plan_date`
            (the queue reflects the generation date unless the caller dates the collation apart).
        gates (dict, optional): Per-domain safety inputs (`clearance_granted`, `red_s_lea_screen`)
            forwarded to every domain's `compute_plan`. Defaults to all-conservative.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook (runtime A: a second
            personal-trainer dispatch), forwarded to `generate_plans`.
        adjudicator (Callable, optional): The held-finding medical-liaison dispatch hook, forwarded
            to `generate_plans` (the SAME gate releases/holds across all three held axes).

    Returns:
        (dict) The `generate_plans` return -- `results` (domain -> result record), `reconciliation`
        (the reconcile report), `reauthored` (bool), `adjudication`, `conflict_adjudications`,
        `rx_bpmh_adjudications` -- plus `dvq_entries` (the doctor-visit-queue entries collated this
        run, in collation order; `[]` when no finding reached the gate).
    """
    result = orchestrate.generate_plans(
        authors, store_read, root, plan_date=plan_date, gates=gates,
        reauthor=reauthor, adjudicator=adjudicator,
    )
    dvq_entries = orchestrate.collate_doctor_visit_queue(result, on_date or plan_date, root)
    return {**result, "dvq_entries": dvq_entries}
