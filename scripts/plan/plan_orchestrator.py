"""The programmatic subscription orchestrator — the autonomous drive layer over the inner engine.

`run_orchestrated` is the programmatic runtime surface that SUPERSEDES the S68 interactive
`/generate-plan` session: it takes the raw operator plan-intake, runs it through the Wave-1
`deid_in` crown-jewel boundary, dispatches each plan-domain specialist programmatically (the
full role profile inlined verbatim per INV-ROLE-INLINING) over the de-identified summary, and
drives the existing `pipeline.run_generation` seam (compute -> reconcile -> adjudicate ->
record). It WRAPS the inner engine verbatim — it re-authors nothing in `orchestrate` /
`pipeline` / `assemble` / `generate_plan` / `adjudicate` / `router`: the plan + safety reasoning
is the dispatched specialists' / liaison's (runtime A), never invented here. This module is the
wiring + the dispatch loop + the de-id halt, and records nothing the inner engine did not.

On a `deid_in` honest-no-plan sentinel (`{"deidentified": False, ...}`) it HALTS to honest
no-plan and dispatches nothing — never a dispatch over a non-summary. It NEVER bypasses the
inner safety gate: a held additive-AE / cross-domain-conflict / Rx-BPMH finding records only
when `adjudicate` (forwarded through `run_generation`'s `adjudicator` hook) releases it.

It ALSO owns the orchestrator's control surface, so it exposes an injectable GATE-DISPATCH SEAM
(`gate_dispatch=`, default a no-op that dispatches nothing). The Wave-3 quality judge
(ADR-0023-T1) and safety review (ADR-0024-T1) wire their real post-generation gates into this
seam; ADR-0020-T2 injects a recording spy here for the outage gate-idle (0-dispatch) assertion.
This task builds ONLY the seam + its inert default, NEVER the gates. `gate_dispatch` is DISTINCT
from `run_generation`'s `gates=` per-domain safety-inputs dict (`clearance_granted` /
`red_s_lea_screen` to `compute_plan`): `gate_dispatch=` is the post-generation gate-dispatch hook
this task adds, `gates=` is the per-domain compute input this callable also forwards.

The revise loop (ADR-0022-T2) is a LATER task and is explicitly OUT of scope here.

The aggregate-dispatch CAP (ADR-0022-T3) IS wired here: `run_orchestrated` instruments the
per-plan aggregate dispatch count across the three dispatch classes (specialist, gate, revise) via
a `DispatchBudget` charged BEFORE each dispatch, and fails closed when a `dispatch_cap` would be
exceeded — halting to the honest no-plan state (the `DEID_HALTED` shape, extended with
`dispatch_count`), recording 0 plans past the cap, dispatching nothing further. The cap is a
configurable keyword parameter defaulting to the named `dispatch_budget.DEFAULT_DISPATCH_CAP` (an
operator/billing fact confirmed downstream), never a hard-coded literal. On the normal path the
final count is surfaced in the result (`dispatch_count`). The revise-class accrual (ADR-0022-T2,
Wave 4) is charged at THIS forward by wrapping the `reauthor`/`adjudicator` hooks, leaving the
inner engine byte-unchanged.
"""

import json
from pathlib import Path

from scripts.plan import pipeline, plan_driver
from scripts.plan.deid_in import deid_in
from scripts.plan.dispatch_budget import (
    DEFAULT_DISPATCH_CAP,
    DispatchBudget,
    DispatchCapExceeded,
)

# The revise-loop control flow + its helpers + reason vocabulary live in the ONE shared driver
# (`plan_driver`, ADR-0026-T1) — `run_orchestrated` DRIVES it, never re-hosts it (the no-fork crown
# jewel). Re-exported here so the established imports
# (`from scripts.plan.plan_orchestrator import SAFETY_BLOCKED, ...`) keep their public surface.
# `_ROLE_OF_DOMAIN` is imported (not re-defined): the SINGLE definition is in `plan_driver` (the
# no-fork crown jewel — it hosts the membership guard that reads it). Imported here for
# `_dispatch_domains`' role-slug VALUE lookup (`_ROLE_OF_DOMAIN[domain]` -> the profile read at
# dispatch time, a missing one failing loud). The orchestrator already imports `plan_driver`, so this
# adds no cycle. The plan-domain specialists live under `.claude/agents/<role>/agent.md` (verified
# present); a nonexistent path would inline empty and make the role-inlining contract vacuous.
from scripts.plan.plan_driver import (  # noqa: F401  (re-export of the driver's public surface)
    DEFAULT_REVISE_CAP,
    PROMOTE_FAILED,
    REVISE_EXHAUSTED,
    SAFETY_BLOCKED,
    _honest_no_plan,
    _ROLE_OF_DOMAIN,
)

# The default plan domains an unattended run generates (all four `PLAN_DOMAINS`); a caller
# narrows via `domains=`.
DEFAULT_DOMAINS = ("workout", "nutrition", "supplements", "peptides")

# The honest no-plan reason when the de-id-IN boundary returns the sentinel: there is no
# de-identified summary, so the orchestrator halts and dispatches nothing. Mirrors the de-id
# sentinel's vocabulary (the honest-no-plan states share a shape). This halt is the CONSUMER's
# (it precedes the driver — the driver is never entered on the sentinel); the bounded-revise
# vocabulary (SAFETY_BLOCKED / REVISE_EXHAUSTED / PROMOTE_FAILED / DEFAULT_REVISE_CAP) lives with
# the driver and is re-exported above.
DEID_HALTED = "deid-halted"

_AGENTS_ROOT = Path(".claude/agents")


def _role_profile(role):
    """Read a role's full profile verbatim from `.claude/agents/<role>/agent.md`.

    The INV-ROLE-INLINING source for the plan-domain specialists. A missing profile fails loud
    (the dispatch must inline a real profile, never an empty path that makes the contract vacuous).

    Args:
        role (str): The role slug (e.g. "personal-trainer").

    Returns:
        (str) The profile file's full text.
    """
    return (_AGENTS_ROOT / role / "agent.md").read_text(encoding="utf-8")


def _dispatch_prompt(role, summary, gates):
    """Build a specialist dispatch prompt: the full role profile + the de-identified summary.

    Inlines the role's full profile verbatim (INV-ROLE-INLINING) ahead of the de-identified
    operator summary + the active gates — the dispatch payload carries the de-identified summary
    only (0 raw-PII), since the orchestrator only ever has the `deid_in` summary, never the raw
    intake, at this point.

    Args:
        role (str): The dispatched role slug.
        summary (dict): The de-identified operator summary (the dispatch's only operator-state).
        gates (dict): The active per-domain safety inputs.

    Returns:
        (str) The dispatch prompt.
    """
    profile = _role_profile(role)
    return (
        f"{profile}\n\n"
        "## De-identified operator summary (the ONLY operator-state source — 0 raw PII)\n\n"
        f"{json.dumps(summary, default=str)}\n\n"
        "## Active gates\n\n"
        f"{json.dumps(gates, default=str)}\n"
    )


def run_orchestrated(raw_intake, deid_client, dispatch, store_read, root, *, plan_date,
                     domains=DEFAULT_DOMAINS, on_date=None, gates=None, gate_dispatch=None,
                     reauthor=None, adjudicator=None, dispatch_cap=DEFAULT_DISPATCH_CAP,
                     revise_cap=DEFAULT_REVISE_CAP):
    """Drive the autonomous GENERATE pass: de-id IN -> dispatch specialists -> the inner engine.

    The programmatic runtime surface (runtime A): (1) calls `deid_in(raw_intake, deid_client)`
    for the de-identified summary; (2) HALTS to honest no-plan with 0 dispatches when `deid_in`
    returns the `{"deidentified": False}` sentinel — never a dispatch over a non-summary;
    (3) otherwise, for each requested domain, builds a dispatch prompt inlining the domain's full
    role profile verbatim (INV-ROLE-INLINING) over the de-identified summary + the active gates,
    issues it through the injected `dispatch` seam, and captures each author envelope into
    `authors`; (4) drives `pipeline.run_generation(authors, ...)` and returns its result. The
    inner engine records the survivors via `record_plan`; the orchestrator records nothing
    directly, opens no new store stream, and never bypasses the inner safety gate (a held finding
    records only when `adjudicate` — forwarded through `adjudicator` — releases it).

    Args:
        raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).
        deid_client: The injected de-id model client (a real `ModelClient`, or a fixture mock).
        dispatch (Callable): The programmatic specialist-dispatch seam,
            `dispatch(domain, prompt, summary) -> author envelope`. A real agent dispatch in
            production; a fixture-author mock in tests (so the orchestrator runs with 0 live spend).
        store_read (Callable): The store read surface, instance-root pre-bound.
        root (str | Path): The store root the plans + the queue are recorded into.
        plan_date (str): The plans' YYYY-MM-DD date.
        domains (tuple, optional): The plan domains to generate. Defaults to all four
            `PLAN_DOMAINS`.
        on_date (str, optional): The doctor-visit-queue collation date. Forwarded to
            `run_generation` (defaults there to `plan_date`).
        gates (dict, optional): Per-domain safety inputs (`clearance_granted`, `red_s_lea_screen`)
            forwarded to `run_generation` (the per-domain `compute_plan` input). DISTINCT from
            `gate_dispatch`. Defaults to all-conservative.
        gate_dispatch (Callable, optional): The injectable GATE-DISPATCH SEAM — the Wave-3 /
            ADR-0020-T2 attachment point. Default `None` -> a no-op that dispatches nothing; this
            task builds ONLY the seam + its inert default, never the gates (those are Wave-3).
            ADR-0023-T1 / ADR-0024-T1 wire real post-generation gates here; ADR-0020-T2 injects a
            recording spy here for the outage gate-idle (0-dispatch) assertion. DISTINCT from
            `gates=`.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook, forwarded to
            `run_generation` verbatim.
        adjudicator (Callable, optional): The held-finding medical-liaison dispatch hook,
            forwarded to `run_generation` verbatim (the inner safety gate — never bypassed).
        dispatch_cap (int, optional): The fail-closed aggregate-dispatch cap (ADR-0022-T3) — the
            max dispatches a single run may issue across all three dispatch classes (specialist +
            gate + revise). Defaults to the named `dispatch_budget.DEFAULT_DISPATCH_CAP` (the
            no-cap-pressure default; the operator/billing ceiling is confirmed downstream), never a
            hard-coded literal. When a charge would exceed it, the run HALTS to honest no-plan
            before the over-budget dispatch is issued.
        revise_cap (int, optional): The bounded revise-loop cap (ADR-0022-T2) — the max per-domain
            quality re-dispatch passes the loop attempts before halting to honest no-plan
            (`REVISE_EXHAUSTED`). Defaults to the named `DEFAULT_REVISE_CAP` (3, fixed at
            build-plan time); configurable so the bound is testable. ONLY consulted on the
            autonomous loop path (when a real `gate_dispatch` is injected).

    Returns:
        (dict) On a successful run, the `run_generation` result (`results`, `reconciliation`,
        `reauthored`, `adjudication`, `conflict_adjudications`, `rx_bpmh_adjudications`,
        `dvq_entries`) plus `dispatch_count` (the aggregate dispatches this run issued). On the
        de-id sentinel halt, the honest no-plan state `{"deidentified": False, "reason":
        DEID_HALTED, "results": {}, "dvq_entries": [], "deid": <the sentinel>, "dispatch_count":
        0}` — 0 dispatches issued, `run_generation` never called (`dispatch_count` is surfaced
        on every path so the revise loop reads it uniformly). On the dispatch-cap halt, the honest no-plan state
        `{"deidentified": True, "reason": DISPATCH_CAP_EXCEEDED, "results": {}, "dvq_entries": [],
        "dispatch_count": <count reached>}` — 0 plans recorded past the cap, the over-budget
        dispatch never issued.
    """
    gates = gates or {}
    # The per-plan dispatch budget (ADR-0022-T3): charged BEFORE each dispatch across all three
    # dispatch classes (specialist + gate + revise). When a charge would exceed `dispatch_cap` it
    # raises `DispatchCapExceeded` (fail-closed — the over-budget dispatch is never issued); the
    # caught halt surfaces the honest no-plan state + the count reached.
    budget = DispatchBudget(cap=dispatch_cap)
    # Whether a REAL composed gate was injected — the autonomous loop entry signal (Security
    # HIGH-2). A provided `gate_dispatch` enters the bounded revise loop (the autonomous posture:
    # `safety_passed is True` the only surface path, never a default-allow). The DEFAULT (None ->
    # the no-op) leaves the LEGACY Wave-2 non-loop path, where the inner per-finding `adjudicate`
    # gate is the always-on floor and a plan surfaces after one inner pass.
    loop_enabled = gate_dispatch is not None
    # The seam is HELD here (the control-surface hook ADR-0023-T1 / ADR-0024-T1 wire real gates
    # into, ADR-0020-T2 spies). Its DEFAULT is a no-op that dispatches nothing. The gate + the
    # revise hooks are wrapped to CHARGE the budget on every real invocation, so each gate / revise
    # dispatch accrues at this orchestrator forward (the inner engine stays byte-unchanged — the
    # accrual is here, not in `pipeline`/`orchestrate`).
    gate_dispatch = gate_dispatch if gate_dispatch is not None else _noop_gate_dispatch
    gate_dispatch = _charging(gate_dispatch, budget)
    reauthor = _charging(reauthor, budget) if reauthor is not None else None
    adjudicator = _charging(adjudicator, budget) if adjudicator is not None else None

    summary = deid_in(raw_intake, deid_client)
    # Honest no-plan halt: the de-id boundary returned the sentinel ({"deidentified": False}), so
    # there is no de-identified summary. Dispatch nothing, call no inner engine, return honest
    # no-plan — never a dispatch over a non-summary (the spec CORE CHANGE).
    if summary.get("deidentified") is False:
        # 0 dispatches issued — surfaced uniformly with the other paths.
        return _honest_no_plan(DEID_HALTED, dispatch_count=0, deidentified=False, deid=summary)

    try:
        # The LEGACY Wave-2 non-loop path (no real gate composed): dispatch the specialists, drive
        # the inner engine ONCE writing directly to `root`, and surface — the inner per-finding
        # `adjudicate` gate is the always-on floor (Wave-2 backward-compat, Security HIGH-2).
        if not loop_enabled:
            authors = _dispatch_domains(domains, summary, gates, dispatch, budget)
            result = pipeline.run_generation(
                authors, store_read, root, plan_date=plan_date, on_date=on_date, gates=gates,
                reauthor=reauthor, adjudicator=adjudicator,
            )
            return {**result, "dispatch_count": budget.count}

        # The AUTONOMOUS bounded revise loop (ADR-0022-T2) is the ONE shared control-inversion driver
        # (`plan_driver.drive`, ADR-0026-T1) — `run_orchestrated` DRIVES it, never re-hosts the loop
        # (the no-fork crown jewel). The driver owns the scratch-store lifecycle, the gate->branch->
        # re-dispatch sequencing, the `safety_passed is True` surface gate, the bounded cap, and the
        # scratch-and-promote; it YIELDS a `(domains, summary, gates)` dispatch-request for each pass,
        # and this consumer SENDS back the captured authors (its `dispatch` seam, charging the budget
        # per specialist dispatch — MF-1). Operator state is still read from the real root through the
        # pre-bound `store_read`; only the inner engine's WRITES are redirected to the driver's
        # scratch (the inner engine stays byte-unchanged). The cap's `DispatchCapExceeded` (raised by
        # `_dispatch_domains`' charge or the charge-wrapped gate) propagates out to the halt below.
        driver = plan_driver.drive(
            summary, domains, store_read, root, plan_date=plan_date, gates=gates,
            gate_dispatch=gate_dispatch, on_date=on_date, reauthor=reauthor,
            adjudicator=adjudicator, budget=budget, revise_cap=revise_cap,
        )
        request = next(driver)
        while True:
            # The per-`kind` fulfilment switch over the typed drive-request (ADR-0028-T1). The
            # driver yields a `Request(kind, payload)`; the consumer fulfils each kind and `.send()`s
            # the RAW fulfilment back — it builds NO disposition (composition stays in `drive`'s ONE
            # `compose_gate_dispatch` call; the surface gate stays in `drive`). An unrecognized kind
            # FAILS CLOSED to honest no-plan (Negative-1: never default-allow an un-handled kind).
            thrown = None
            if request.kind == plan_driver.AUTHOR:
                req_domains, req_summary, req_gates = request.payload
                fulfilment = _dispatch_domains(req_domains, req_summary, req_gates, dispatch, budget)
            elif request.kind == plan_driver.GATE:
                # The GATE request carries `(assembled_plan, gate)` — the consumer invokes the
                # charge-wrapped composed gate over the assembled plan and sends back the RAW
                # disposition. A gate that RAISES is THROWN INTO the driver, whose GATE-yield
                # fail-closed wrap reads it as ambiguous -> SAFETY_BLOCKED (the surface gate stays in
                # `drive`). `DispatchCapExceeded` is the budget halt, not a gate ambiguity — it
                # propagates to this consumer's cap-halt handler, never thrown into the driver.
                assembled_plan, gate = request.payload
                try:
                    fulfilment = gate(assembled_plan)
                except DispatchCapExceeded:
                    raise
                except Exception as gate_error:
                    thrown = gate_error
            else:
                # Negative-1 fail-closed: an unrecognized request kind surfaces 0 plans (honest
                # no-plan), never a default-allow that would let an un-handled kind pass silently.
                return _honest_no_plan(SAFETY_BLOCKED, dispatch_count=budget.count)
            try:
                if thrown is not None:
                    request = driver.throw(thrown)
                else:
                    request = driver.send(fulfilment)
            except StopIteration as done:
                return done.value
    except DispatchCapExceeded as exceeded:
        # Fail-closed halt: a charge would exceed the cap, so the over-budget dispatch was never
        # issued. Return the honest no-plan state (the DEID_HALTED shape, extended with
        # `dispatch_count`) — 0 plans recorded past the cap, dispatch nothing further.
        return _honest_no_plan(exceeded.reason, dispatch_count=exceeded.count)


def _noop_gate_dispatch(*args, **kwargs):
    """The inert default gate-dispatch seam: dispatches nothing.

    The post-generation gate-dispatch hook's no-op default (AC-7). A normal run with the default
    issues 0 gate dispatches — the seam is the attachment point ADR-0023-T1 / ADR-0024-T1 wire
    real judge / safety-review gates into and ADR-0020-T2 spies for the outage gate-idle
    assertion. This task builds the seam + this inert default ONLY, never the gates.
    """
    return None


def _charging(hook, budget):
    """Wrap a dispatch hook so it CHARGES the budget before each real invocation.

    The gate / revise (`reauthor` / `adjudicator`) dispatch classes fire INSIDE the inner engine
    (`pipeline.run_generation` -> `orchestrate.generate_plans`), but their accrual must happen at
    THIS orchestrator forward, not in the byte-unchanged inner engine. Wrapping the hook charges
    the budget on every invocation BEFORE the wrapped dispatch runs — fail-closed before the
    over-budget gate / revise call is issued (`DispatchCapExceeded` propagates up to the run's
    halt handler). The no-op default gate charges nothing on a normal run (it is never invoked
    past the seam in Wave 2/3), so the count stays the specialist tally on the default path.

    Args:
        hook (Callable): The dispatch hook to charge-wrap (`gate_dispatch` / `reauthor` /
            `adjudicator`).
        budget (DispatchBudget): The per-plan dispatch budget to charge.

    Returns:
        (Callable) The charge-wrapping hook, same call signature as `hook`.
    """
    def charged(*args, **kwargs):
        budget.charge()
        return hook(*args, **kwargs)

    return charged


def _dispatch_domains(domains, summary, gates, dispatch, budget):
    """Dispatch each domain's specialist (full profile inlined) and return the authors fragment.

    The single specialist-dispatch shape used by BOTH the initial pass and the bounded revise
    pass (the same `dispatch(domain, prompt, summary)` seam — MF-1, NOT the energy-bounce
    `reauthor` hook). Charges the budget BEFORE each dispatch (fail-closed before the over-budget
    specialist call is issued) and inlines the domain's full role profile over the de-identified
    summary + the active gates (INV-ROLE-INLINING). The orchestrator originates no plan content —
    each envelope is the specialist's (runtime A).

    Args:
        domains (iterable): The plan domains to dispatch.
        summary (dict): The de-identified operator summary (the dispatch's only operator-state).
        gates (dict): The active per-domain safety inputs.
        dispatch (Callable): The programmatic specialist-dispatch seam.
        budget (DispatchBudget): The per-plan dispatch budget, charged before each dispatch.

    Returns:
        (dict) domain -> the captured author envelope for the dispatched domains.
    """
    authors = {}
    for domain in domains:
        budget.charge()
        prompt = _dispatch_prompt(_ROLE_OF_DOMAIN[domain], summary, gates)
        authors[domain] = dispatch(domain, prompt, summary)
    return authors
