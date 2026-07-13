"""The daily deterministic monitoring pass hosted in the built ADR-0039 runner (ADR-0045-T3, TERMINAL).

`run(root, *, observations, <injected seams>, plan_date=None)` is the scheduled DAILY tick's driver:
it reads the standing ADR-0044 comprehensive plan version, HOSTS ADR-0045-T2's
`tiered_executor.execute_monitoring_day` over that version's compiled `monitoring_config` + the day's
observations, and — INSIDE the ADR-0039-T4 runner-to-runner advisory lock — records Tier-1 bounded
auto-applies and enforces real cross-domain reconciliation holds. It is the TERMINAL node on the
monitoring loop (`0045-T1 -> 0045-T2 -> 0045-T3`); no downstream consumer.

The daily pass is where ADR-0045-T2's three deferred executor seams get WIRED — the runner OWNS
supplying the REAL ones:

  - **0n3t (PF-S134-02, the fail-closed one-way door):** it builds a REAL composed `gate_dispatch` via
    `gate_dispatch.compose_gate_dispatch(...)` and injects it UNCONDITIONALLY, so a Tier-2 re-plan
    routes THROUGH the composition (`run_orchestrated`(loop_enabled) -> `plan_driver.drive` ->
    `gate_dispatch.compose_disposition` -> the fail-closed `safety_passed is True` surface), never the
    executor's `gate_dispatch=None` default (which the WAVE5-01 guard silently fail-closes to a Tier-4
    hold, masking a fail-open wiring bug).
  - **evvs:** it binds `plan_date` to the STANDING version's date, so the Tier-4 `mark_pending` pointer
    lands on the timepoint `plan_model._standing_versions` resolves by date-equality (a naive tick-date
    binding lands the pointer on the wrong timepoint and the held version STANDS — fail-open).
  - **u20d:** on a Tier-3 cross-domain-seam routing it reconciles the standing version's REAL
    `domain_programs` (candidates carrying `cross_domain_seams` under `PROGRAM_KEY`, the shape
    `orchestrate._cross_domain_seams` reads), NOT the executor's degenerate `{"plan": None}` stub, and
    ENFORCES the resulting holds via `plan_confirm.mark_pending`.

The load-bearing property is DETERMINISM ON A NO-EVENT DAY: when no observed signal crosses a material
threshold, the pass makes 0 model calls + 0 metered de-id-IN calls — it Tier-1 auto-applies the
certified bounded adjustments deterministically (recording them into the model) and nothing else.
Reading the model and building the composed-gate closure are 0-spend; the gate closure is invoked only
on a Tier-2 re-plan.

Store surface (EXTEND-NOT-REBUILD, SEC-03): the daily pass's ONLY store writes are the EXISTING
`plan_confirm.mark_pending` (Tier-4 + enforced cross-domain holds, the `plan-confirm::` stream) +
`plan_model.record_plan_version` (Tier-1 bounded-adjustment recording, the `plan-model::` stream) —
both ride keying's unchanged `(item, timepoint, source)` identity. It defines NO new store key/stream
and calls no other `store.append` / `store.correct`; it re-implements neither the executor's routing,
the compiler's grammar, the driver's revise loop, nor the reconciler's holds.

Concurrency (S1): the store-writing section runs inside `store_lock.cadence_lock(root)` (the same lock
the weekly `cadence_runner` uses). On a BUSY acquire (a concurrent weekly/daily tick holds it) the
driver DEFERS — 0 store writes, a `lock-busy` deferred receipt — catching up next tick, so a concurrent
weekly `store.append` can never lost-update-clobber the daily Tier-4 pending pointer. The lock releases
in a `finally` on every exit (crash-safe).

Ships DISABLED BY DEFAULT: importing arms nothing (0 tick / model / de-id on import — every effect
lives inside a function). The daily-interval schedule targeting this module and the LIVE seam wiring
(the real de-id `ModelClient`, the specialist dispatch, the gate's judge/review clients) are the
operator-gated LIVE-wiring follow-up (bead `a-plus-maxing-glzi`), NOT this build — the `main()` entry
fails loud rather than arming a partial live pass.
"""

import datetime

from scripts.plan import gate_dispatch, orchestrate, safety_review, tiered_executor
from scripts.plan.assemble import PROGRAM_KEY
from scripts.store import plan_confirm, plan_model

from scripts.runner import store_lock

# The version key under which a Tier-1 auto-apply's bounded adjustment is annotated when the recording
# is re-affirmed into the model (disposition #22) — an open-on-extras value key, so it round-trips
# through `record_plan_version` -> `store.append` without a new validate-required element.
_ADJUSTMENTS = "adjustments"


def _read_standing(root, as_of):
    """Resolve the standing comprehensive version + its own declared date (evvs), or `(None, None)`.

    Reads the ADR-0044 model via `plan_model.read_plan_version`, honoring the `_standing_versions`
    confirm-hold. A version dated exactly `as_of` is returned directly; otherwise the resolved
    `plan_date` (the latest STANDING version's date) is re-read to fetch the composite. When no version
    stands, returns `(None, None)`.

    Args:
        root (str | Path): The store root.
        as_of (str): The tick's as-of date, YYYY-MM-DD.

    Returns:
        (dict | None) The standing composite plan version, or None when none stands.
        (str | None) That version's declared date, or None.
    """
    resolved = plan_model.read_plan_version(as_of, root)
    version_date = resolved["plan_date"]
    if version_date is None:
        return None, None
    if resolved["version"] is not None:
        return resolved["version"], version_date
    return plan_model.read_plan_version(version_date, root)["version"], version_date


def _record_tier1(routings, version, root):
    """Record each Tier-1 auto-apply's bounded adjustment into the model — 0 pending pointer (AC-4).

    A certified Tier-1 auto-apply is a bounded, single-in-domain deterministic change; the recording is
    ADR-0045-T3's job (the executor emits the directive, writes nothing). Re-affirms the standing
    version into the model with the auto-applied routings annotated, via the EXISTING
    `plan_model.record_plan_version` — NO `plan_confirm.mark_pending`, so the recorded version carries 0
    pending pointer and `read_plan_version` resolves it STANDING (the daily Tier-1 route bypasses the
    weekly `regenerate` magnitude gate entirely, disposition #22). No new store key/stream.

    Args:
        routings (list): The executor's per-event tier-routing records.
        version (Mapping): The standing composite version the day monitored against.
        root (str | Path): The store root.

    Returns:
        (list) The Tier-1 auto-apply routings recorded this pass (possibly empty).
    """
    applied = [r for r in routings if r["tier"] == tiered_executor.TIER_1]
    if not applied:
        return []
    adjusted = dict(version)
    adjusted[_ADJUSTMENTS] = list(version.get(_ADJUSTMENTS, [])) + [
        {"domain": r["domain"], "signal": r["signal"], "tier": r["tier"]} for r in applied
    ]
    plan_model.record_plan_version(adjusted, root)
    return applied


def _enforce_reconcile_holds(routings, domain_programs, plan_date, root):
    """On a Tier-3 cross-domain-seam routing, reconcile REAL candidates and enforce the holds (u20d).

    Reads the standing version's REAL per-domain programs as candidates of the SHAPE
    `orchestrate.reconcile` reads (`{"domain": d, "plan": {PROGRAM_KEY: <the domain program carrying
    cross_domain_seams>}}`) — NOT the executor's degenerate `{"plan": None}` stub (which reads 0 seams
    and enforces NO hold, fail-open) — calls `orchestrate.reconcile`, and enforces the report's
    `holds` / `conflict_held` / `rx_bpmh_held` by `plan_confirm.mark_pending`-ing each held domain at
    the standing version's date. No new store key/stream.

    Args:
        routings (list): The executor's per-event tier-routing records.
        domain_programs (Mapping): The standing version's `{domain: DOMAIN PROGRAM}`.
        plan_date (str): The standing version's date (the pointer timepoint — evvs).
        root (str | Path): The store root.

    Returns:
        (list) The domains held by the reconciliation this pass (sorted; possibly empty).
    """
    if not any(r["tier"] == tiered_executor.TIER_3 for r in routings):
        return []
    candidates = {
        domain: {"domain": domain, "plan": {PROGRAM_KEY: program}}
        for domain, program in domain_programs.items()
    }
    outcome = orchestrate.reconcile(candidates)
    held = set(outcome["holds"]) | set(outcome["conflict_held"]) | set(outcome["rx_bpmh_held"])
    for domain in sorted(held):
        plan_confirm.mark_pending(domain, plan_date, root)
    return sorted(held)


def run(root, *, observations, raw_intake, deid_client, dispatch, store_read, judge_client,
        review_dispatch, lenses=safety_review.DEFAULT_LENSES, reauthor=None, adjudicator=None,
        plan_date=None):
    """Drive one daily deterministic monitoring tick over the standing version and return its receipt.

    Reads the standing comprehensive version, binds `plan_date` to that version's date (evvs), builds
    the REAL composed `gate_dispatch` (0n3t) and — inside `store_lock.cadence_lock(root)` (S1) — hosts
    `execute_monitoring_day`, records Tier-1 auto-applies (AC-4), and enforces real cross-domain
    reconciliation holds (u20d). On a BUSY lock the driver DEFERS (0 store writes, a `lock-busy`
    receipt). On a no-event day the executor makes 0 model + 0 de-id-IN calls (the daily pass adds no
    model/de-id call of its own; the composed-gate closure is 0-spend and is not invoked).

    Args:
        root (str | Path): The store root the standing version is read from and the holds/recording
            record into.
        observations (Mapping): The day's per-signal readings `{signal_name: observed_value}` (the
            executor's contract) — an injected seam (fixture in tests; store-derived in production).
        raw_intake (dict): The raw operator plan-intake a Tier-2 re-plan de-identifies (the de-id-IN
            crown-jewel boundary owns it; forwarded verbatim).
        deid_client: The injected de-id model client a Tier-2 re-plan routes the de-id-IN call through.
        dispatch (Callable): The programmatic specialist-dispatch seam a Tier-2 re-plan consumes.
        store_read (Callable): The store read surface, instance-root pre-bound (forwarded to a Tier-2
            re-plan).
        judge_client: The QUALITY judge client the composed gate binds (a real model client in
            production; a fixture mock in tests — 0 live spend).
        review_dispatch (Callable): The SAFETY lens-dispatch seam the composed gate binds.
        lenses (tuple, optional): The safety-lens roster forwarded to the composed gate. Defaults to
            `safety_review.DEFAULT_LENSES`.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook forwarded to a Tier-2 re-plan.
        adjudicator (Callable, optional): The held-finding medical-liaison hook forwarded to a Tier-2
            re-plan.
        plan_date (str, optional): The tick's as-of date. None -> today's ISO date. The executor's
            `plan_date` is bound to the STANDING version's date regardless (evvs), never this naive value.

    Returns:
        (dict) The daily-pass receipt: on a normal tick `{"deferred": False, "regenerated": True,
        "plan_date": <version date>, "routings": [...], "recorded": [...], "held": [...]}`; on a busy
        lock `{"deferred": True, "regenerated": False, "reason": "lock-busy", "routings": []}`; when no
        version stands, a `no-standing-version` receipt.
    """
    as_of = plan_date if plan_date is not None else datetime.date.today().isoformat()
    version, version_date = _read_standing(root, as_of)
    if version is None:
        return {"deferred": False, "regenerated": False, "reason": "no-standing-version",
                "plan_date": None, "routings": [], "recorded": [], "held": []}

    config = version[plan_model.MONITORING_CONFIG]
    domain_programs = version[plan_model.DOMAIN_PROGRAMS]
    # Build the REAL composed gate UNCONDITIONALLY (0n3t / PF-S134-02) — never the executor's `None`
    # default, which the WAVE5-01 guard fail-closes to a Tier-4 hold, masking a fail-open wiring bug.
    # Building the closure is 0-spend; it is invoked only on a Tier-2 re-plan.
    gate = gate_dispatch.compose_gate_dispatch(judge_client, review_dispatch, lenses=lenses)

    # Steps 4-6 (the executor host + the Tier-4/enforced holds + the Tier-1 recording) are the
    # store-writing critical section (S1): enter it inside the advisory lock, and DEFER on a busy tick.
    with store_lock.cadence_lock(root) as acquired:
        if not acquired:
            return {"deferred": True, "regenerated": False, "reason": "lock-busy", "routings": []}
        result = tiered_executor.execute_monitoring_day(
            config, observations, raw_intake, deid_client, dispatch, store_read, root,
            plan_date=version_date, gate_dispatch=gate, reauthor=reauthor, adjudicator=adjudicator,
        )
        routings = result["routings"]
        recorded = _record_tier1(routings, version, root)
        held = _enforce_reconcile_holds(routings, domain_programs, version_date, root)
        return {"deferred": False, "regenerated": True, "plan_date": version_date,
                "routings": routings, "recorded": recorded, "held": held}


def main(argv=None):
    """The daily-pass module entry — the LIVE-wiring is DEFERRED (bead `a-plus-maxing-glzi`).

    ADR-0045-T3 builds the injected-seam `run` driver + the disabled-by-default label registration
    (`activate.DAILY_MONITOR_LABEL`). The daily-interval schedule targeting this module and the LIVE seam
    wiring (the real de-id `ModelClient`, the specialist dispatch, the composed gate's judge/review
    clients) are the operator-gated LIVE-wiring follow-up (Deviation #2), not this build — so running
    the module directly fails loud rather than arming a partial live pass. Runs only as the module entry
    (the `__main__` guard below), never on import.

    Args:
        argv (list, optional): Unused; accepted for the standard module-entry shape.
    """
    raise NotImplementedError(
        "daily_monitor live-wiring is deferred to bead a-plus-maxing-glzi (operator-gated LIVE run); "
        "ADR-0045-T3 ships the injected-seam run() driver + the disabled-by-default label registration"
    )


if __name__ == "__main__":
    main()
