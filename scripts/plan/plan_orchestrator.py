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
import tempfile
from pathlib import Path

from scripts.plan import pipeline
from scripts.plan.deid_in import deid_in
from scripts.plan.dispatch_budget import (
    DEFAULT_DISPATCH_CAP,
    DispatchBudget,
    DispatchCapExceeded,
)
from scripts.store import store

# domain -> the role whose full profile the dispatch prompt inlines (INV-ROLE-INLINING). The
# plan-domain specialists live under `.claude/agents/<role>/agent.md` (verified present); a
# nonexistent path would inline empty and make the role-inlining contract vacuous, so the live
# profile is read at dispatch time and a missing one fails loud (FileNotFoundError).
_ROLE_OF_DOMAIN = {
    "workout": "personal-trainer",
    "nutrition": "nutritionist",
    "supplements": "supplement-specialist",
    "peptides": "peptide-specialist",
}

# The default plan domains an unattended run generates (all four `PLAN_DOMAINS`); a caller
# narrows via `domains=`.
DEFAULT_DOMAINS = ("workout", "nutrition", "supplements", "peptides")

# The honest no-plan reason when the de-id-IN boundary returns the sentinel: there is no
# de-identified summary, so the orchestrator halts and dispatches nothing. Mirrors the de-id
# sentinel's vocabulary (the honest-no-plan states share a shape).
DEID_HALTED = "deid-halted"

# The bounded revise loop's reason vocabulary (ADR-0022-T2), same kebab-string family as
# `DEID_HALTED` / `dispatch_budget.DISPATCH_CAP_EXCEEDED`. SAFETY_BLOCKED is the TERMINAL
# fail-closed halt (a non-positive safety disposition — `safety_passed` not boolean-True);
# REVISE_EXHAUSTED is the bounded-cap halt (a non-converging quality miss past `revise_cap`).
SAFETY_BLOCKED = "safety-blocked"
REVISE_EXHAUSTED = "revise-exhausted"

# The honest no-plan reason when promoting the surfaced pass's plan rows from the scratch store
# into `root` fails mid-write (an OSError on a `store.append`). Same kebab-string family; the
# promote is guarded so a write failure fails closed (honest no-plan, the real store NOT left
# partial) rather than escaping uncaught with a half-promoted plan set.
PROMOTE_FAILED = "promote-failed"

# The bounded revise cap (dispositions #2: N=3 fixed at build-plan time). A named module constant
# (NOT a hard-coded literal at the loop site), mirroring `dispatch_budget.DEFAULT_DISPATCH_CAP`;
# `run_orchestrated`'s `revise_cap` keyword defaults to it so the bound is configurable + testable.
DEFAULT_REVISE_CAP = 3

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

        # The AUTONOMOUS bounded revise loop (ADR-0022-T2). The inner engine writes plan::/dvq:: as
        # it generates, BEFORE the whole-plan gate runs — so each pass writes to an ISOLATED scratch
        # store, and the surviving plans are PROMOTED into `root` ONLY when the gates surface them.
        # A SAFETY_BLOCKED / REVISE_EXHAUSTED halt promotes nothing, so a blocked plan never reaches
        # the rendered store (`reemit_maintained` reads `root`) — the fail-closed surface. Operator
        # state is still read from the real root through the pre-bound `store_read`; only the inner
        # engine's WRITES are redirected (the inner engine stays byte-unchanged).
        with tempfile.TemporaryDirectory(prefix="aplus-revise-") as scratch_parent:
            revise_count = 0
            authors = _dispatch_domains(domains, summary, gates, dispatch, budget)
            scratch = Path(scratch_parent) / "pass-0"
            result = pipeline.run_generation(
                authors, store_read, scratch, plan_date=plan_date, on_date=on_date, gates=gates,
                reauthor=reauthor, adjudicator=adjudicator,
            )
            while True:
                disposition = _safe_gate(gate_dispatch, result)
                # SAFETY GATE (the only surface path is a positive boolean-True safety assertion).
                # `False` / `None` / absent / non-bool / non-dict / a raised gate -> TERMINAL
                # SAFETY_BLOCKED: never re-authored, never looped, never overridden (AC-2, R2, HIGH-1).
                if not (isinstance(disposition, dict) and disposition.get("safety_passed") is True):
                    return _honest_no_plan(SAFETY_BLOCKED, dispatch_count=budget.count)
                # QUALITY: an ACCEPT with safety passing surfaces the plan — PROMOTE the survivors
                # from the scratch store into `root` and return (AC-1, AC-4). A write OSError
                # mid-promote fails CLOSED to honest no-plan (the real store is not left surfacing
                # a half-promoted plan set) rather than escaping uncaught (SEC-01).
                if disposition.get("accept") is True:
                    try:
                        _promote_plans(scratch, root)
                    except OSError:
                        return _honest_no_plan(PROMOTE_FAILED, dispatch_count=budget.count)
                    return {**result, "dispatch_count": budget.count}
                # A quality REVISE with safety passing: bounded re-author. Halt at `revise_cap`
                # without convergence (AC-3, R1 — the count of re-dispatch passes is capped exactly).
                if revise_count >= revise_cap:
                    return _honest_no_plan(REVISE_EXHAUSTED, dispatch_count=budget.count)
                # Re-dispatch ONLY the REVISE-targeted domains (an inner non-overridably-held domain
                # is never a revise TARGET — AC-5/R3; the loop re-authors only the quality-flagged
                # domains the composed disposition names). Re-running with the SAME authors is
                # store-idempotent (identical result, no convergence), so the per-domain `authors` is
                # REBUILT from a fresh specialist dispatch (the same `dispatch` seam — MF-1).
                revise_domains = disposition.get("revise_domains") or []
                # An unknown / out-of-run-set revise TARGET is a malformed disposition: route it to
                # the same TERMINAL fail-closed halt the loop already takes for a non-dict / absent-key
                # safety disposition, rather than letting an unguarded `_ROLE_OF_DOMAIN[domain]`
                # KeyError escape uncaught (BUG-01/API-02). The composed gate must only ever name a
                # domain this run is generating.
                if any(d not in _ROLE_OF_DOMAIN or d not in domains for d in revise_domains):
                    return _honest_no_plan(SAFETY_BLOCKED, dispatch_count=budget.count)
                authors.update(_dispatch_domains(revise_domains, summary, gates, dispatch, budget))
                revise_count += 1
                scratch = Path(scratch_parent) / f"pass-{revise_count}"
                result = pipeline.run_generation(
                    authors, store_read, scratch, plan_date=plan_date, on_date=on_date, gates=gates,
                    reauthor=reauthor, adjudicator=adjudicator,
                )
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


def _safe_gate(gate_dispatch, result):
    """Invoke the composed gate over the assembled result; a raised gate reads as ambiguous.

    The FAIL-CLOSED safety contract (Security HIGH-1): a gate that RAISES (a lens dispatch failed
    mid-review, a malformed composition) is an ambiguous safety disposition, not a surface path —
    it returns `None` so the loop's `safety_passed is True` check routes it to `SAFETY_BLOCKED`.
    `DispatchCapExceeded` is re-raised (it is the budget halt, not a gate ambiguity), propagating
    to the run's cap-halt handler.

    Args:
        gate_dispatch (Callable): The charge-wrapped composed gate.
        result (dict): The assembled `run_generation` result to gate.

    Returns:
        (Any) The gate's composed disposition, or `None` when the gate raised (the ambiguous /
        fail-closed case).
    """
    try:
        return gate_dispatch(result)
    except DispatchCapExceeded:
        raise
    except Exception:
        return None


def _honest_no_plan(reason, *, dispatch_count, deidentified=True, **extra):
    """The shared honest-no-plan return shape for every halt path (0 plans surfaced).

    The single shape the de-id-sentinel, dispatch-cap, safety-blocked, and revise-exhausted halts
    all return — `{"deidentified", "reason", "results": {}, "dvq_entries": [], "dispatch_count"}`
    — so the divergent halt builders share one definition. `extra` carries a path-specific field
    (the de-id sentinel's `deid`).

    Args:
        reason (str): The halt reason token (a kebab-string from the reason vocabulary).
        dispatch_count (int): The aggregate dispatch count reached at the halt.
        deidentified (bool, optional): The de-id state — False only on the de-id-sentinel halt.

    Returns:
        (dict) The honest no-plan state.
    """
    return {
        "deidentified": deidentified,
        "reason": reason,
        "results": {},
        "dvq_entries": [],
        "dispatch_count": dispatch_count,
        **extra,
    }


def _promote_plans(scratch_root, root):
    """Promote the surfaced pass's `plan::` / `dvq::` rows from the scratch store into `root`.

    The autonomous loop drives the inner engine against an ISOLATED scratch store each pass (the
    inner engine writes plan rows as it generates, BEFORE the whole-plan gate runs), so a blocked
    plan never touches the rendered `root`. When the gates SURFACE a plan, its survivors are
    promoted here: each `plan::` / `dvq::` row the inner engine wrote into `scratch_root` is
    appended to `root` through the SAME `store.append` surface (inheriting the store-keying
    `(item, timepoint, source)` dedupe — a re-promoted identical row is idempotent). The operator
    state already lives in `root`; only the inner engine's generated plan / queue streams promote.

    EVERY read completes BEFORE any write: the `(item, reading)` pairs are collected from the
    scratch store first, then appended into `root`. And the affected `root` item files are
    snapshotted (their prior on-disk bytes, or absence) before the first append, so a write
    OSError mid-append RESTORES each touched file to its pre-promote state before re-raising —
    the real store is never left with a half-promoted plan set (the caller's guard then routes
    the re-raise to a `PROMOTE_FAILED` honest no-plan halt). SEC-01.

    Args:
        scratch_root (str | Path): The surfaced pass's scratch store root.
        root (str | Path): The real store root the surfaced plans promote into.
    """
    pairs = []
    for item in store.items(scratch_root):
        if not (item.startswith("plan::") or item.startswith("dvq::")):
            continue
        for reading in store.read(item, root=scratch_root):
            pairs.append((item, reading))

    # Snapshot the pre-promote on-disk state of every item file this promote will touch, so a
    # mid-append OSError can roll the real store back to where it was (no half-promoted set).
    affected = {store._item_path(item, root) for item, _ in pairs}
    snapshot = {p: (p.read_bytes() if p.exists() else None) for p in affected}
    try:
        for item, reading in pairs:
            store.append(item, reading, root=root)
    except OSError:
        for path, prior in snapshot.items():
            if prior is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(prior)
        raise
