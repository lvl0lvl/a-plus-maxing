"""The cadence runner driver — one signal(CADENCE_TRIGGER) tick over the built plan loop (ADR-0039-T1).

`run(root, *, dispatch_factory, deid_client, tailor_client=None, plan_date=None)` is the scheduled
tick's driver: it obtains a subscription session from the injectable `dispatch_factory`, builds the
dispatch seam via `subscription_dispatch.build_dispatch(session)`, and drives the ALREADY-BUILT loop
through its SINGLE entry `plan_loop.signal(root, trigger=plan_loop.CADENCE_TRIGGER, dispatch=...,
deid_client=...)` EXACTLY ONCE, returning the loop's receipt unchanged. The raw `store.read_all` read
and the ADR-0027 de-id-IN de-identification run INSIDE `plan_loop.signal` in Python — never in the
driver's or the top-level subscription session's transmitted context — so the de-id-IN call is the
sole receiver of raw store content and the dispatch payloads carry only the de-identified summary.

EXTEND-NOT-REBUILD (SEC-03 governance floor): the driver supplies seams and re-hosts none of the
loop. The debounce, the fail-closed gate composition, the cross-domain holds, and the loop's pinned
constants all stay inside the built loop; the driver names none of their symbols and touches no file
under `scripts/serve/` / `scripts/plan/` / `scripts/store/`. Its loop-facing import surface is
`scripts.serve.plan_loop` (for the entry + the trigger label) plus `scripts.runner.subscription_dispatch`
and the sibling `scripts.runner.store_lock` advisory lock (ADR-0039-T4), which serializes the tick's single
read -> regenerate -> promote critical section runner-to-runner; a busy tick defers (0 re-gen, 0 store write).
Its only other imports are `main()`'s entry-point plumbing: `pathlib.Path` + `scripts.store.store` (for the
repo-anchored `DEFAULT_ROOT`) and the ADR-0027 de-id `scripts.model.client.ModelClient` that `main()` constructs.

Ships DISABLED BY DEFAULT: importing arms nothing (0 signal / de-id / dispatch on import — the
`__main__` guard keeps `main()` off the import path), and the default subscription-session factory
refuses pre-scrub (SEC-04; ADR-0039-T2 lifts it by wiring the auth env-scrub).

`main(argv=None)` is the production `python -m scripts.runner.cadence_runner` entry the T3 scheduler's
launchd plist targets (ProgramArguments): it resolves the repo-anchored store root, constructs the
ADR-0027 de-id `ModelClient` (construction is 0-spend — spend is metered only on `.deidentify()`), and
calls `run` with `subscription_dispatch`'s default session factory. `main` itself constructs no
subscription session and spends nothing: the session is built only when `run` invokes that factory,
which refuses pre-scrub.
"""

from pathlib import Path

from scripts.model.client import ModelClient
from scripts.serve.intake_aggregate import AggregatingDeidClient
from scripts.serve import plan_loop
from scripts.store import store

from scripts.runner import store_lock, subscription_dispatch


def run(root, *, dispatch_factory, deid_client, tailor_client=None, plan_date=None):
    """Drive one cadence tick through the built loop's single signal entry and return its receipt.

    Obtains a subscription session from `dispatch_factory`, builds the dispatch seam via
    `subscription_dispatch.build_dispatch(session)`, and calls `plan_loop.signal(root,
    trigger=plan_loop.CADENCE_TRIGGER, dispatch=..., deid_client=..., ...)` EXACTLY ONCE, returning
    the loop's receipt unaltered. The raw read + the de-id-IN de-identification run INSIDE
    `plan_loop.signal` (never here), so the de-id-IN call is the sole receiver of raw store content.

    Args:
        root (str | Path): The store root the derived state is read from and the re-gen records into.
        dispatch_factory (Callable): A zero-arg factory returning the subscription session
            (`session(name, prompt, context) -> author envelope`). The production default
            (`subscription_dispatch.default_session_factory`) refuses pre-scrub (SEC-04); tests inject
            a fixture session factory.
        deid_client: The ADR-0027 de-id model client for the crown-jewel de-id-IN boundary (a real
            `ModelClient`, or a fixture mock).
        tailor_client (optional): The care-lane presentation client forwarded to the loop's
            post-promote tailoring seam. None -> pass-through (0 tailoring spend).
        plan_date (str, optional): The plans' YYYY-MM-DD date. None -> today's ISO date (in the loop).

    The single `plan_loop.signal` critical section runs inside `store_lock.cadence_lock(root)` (the
    ADR-0039-T4 advisory lock): when a concurrent runner tick already holds the lock this tick DEFERS —
    it returns a `lock-busy` receipt WITHOUT calling `signal` (0 re-gen, 0 store write) and catches up on
    the next tick. The lock releases in a `finally` on every exit (including an exception raised inside
    the critical section), so a crashed tick frees the lock and does not wedge the schedule.

    Returns:
        (dict) The `plan_loop.signal` receipt unchanged (the re-gen result on a gate-pass, else a
        no-op / hold+prompt receipt), OR a `{"regenerated": False, "deferred": True, ...,
        "reason": "lock-busy"}` deferred receipt when a concurrent tick held the lock.
    """
    with store_lock.cadence_lock(root) as acquired:
        if not acquired:
            return {"regenerated": False, "deferred": True,
                    "trigger": plan_loop.CADENCE_TRIGGER, "reason": "lock-busy"}
        session = dispatch_factory()
        dispatch = subscription_dispatch.build_dispatch(session)
        return plan_loop.signal(
            root, trigger=plan_loop.CADENCE_TRIGGER, dispatch=dispatch, deid_client=deid_client,
            tailor_client=tailor_client, plan_date=plan_date,
        )


def _resolved_store_root():
    """The repo-anchored store root, resolved cwd-independently for the launchd-scheduled entry.

    The runner is invoked by the T3 launchd schedule, whose working directory is not the repo, so the
    default relative `store.DEFAULT_ROOT` cannot be trusted. Anchor it at the resolved repo root
    (`scripts/runner/cadence_runner.py` -> `scripts/runner` -> `scripts` -> repo root).
    """
    return Path(__file__).resolve().parents[2] / store.DEFAULT_ROOT


def main(argv=None):
    """The production `python -m scripts.runner.cadence_runner` entry (the launchd -> module -> run() path).

    Resolves the repo-anchored store root, constructs the ADR-0027 de-id `ModelClient` (0-spend at
    construct — spend is metered only on `.deidentify()`), and calls `run` with
    `subscription_dispatch`'s DEFAULT session factory. `main` constructs no subscription session and
    spends nothing: the session is built only when `run` invokes the factory, which refuses pre-scrub
    (SEC-04). Runs only as the module entry (the `__main__` guard below), never on import.

    Args:
        argv (list, optional): Unused CLI args (the scheduled tick takes none); accepted for the
            standard module-entry shape.
    """
    root = _resolved_store_root()
    # AggregatingDeidClient: collapse the high-cardinality wearable timeseries in the raw intake
    # BEFORE the metered de-id call — a real intake is ~131K Opus tokens, MOST of it raw
    # RHR/HRV/SpO2 points the model would crunch into a trend; aggregation cuts that ~30x on a
    # real intake (a ~10-100x reduction depending on timeseries density) — and normalise the
    # model's non-string output to the string shape the plan-composition consumers expect
    # (bead 940o). 0-spend at construct; the frozen engine is untouched.
    deid_client = AggregatingDeidClient(ModelClient())
    return run(root, dispatch_factory=subscription_dispatch.default_session_factory,
               deid_client=deid_client)


if __name__ == "__main__":
    main()
