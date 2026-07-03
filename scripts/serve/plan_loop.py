"""The automated plan-evolution loop's front-door binding (ADR-0036-T1).

`regenerate(root, *, dispatch, deid_client, plan_date=None, trigger=None)` is the loop's ONE
entry into the FULL-COMPOSITION front door. It drives `plan_orchestrator.run_orchestrated`
with a REAL composed gate producer injected, so `run_orchestrated`'s `loop_enabled` path is
taken: the run enters the ONE shared driver (`plan_driver.drive`), composes the gate verdicts
via `gate_dispatch.compose_disposition`, applies the fail-closed `safety_passed is True` surface
gate, and runs the five `orchestrate` cross-domain holds (energy bounce, additive-AE,
cross-domain-conflict, Rx-BPMH, the medical-liaison adjudication gate).

The anti-degradation guard (the load-bearing deliverable): this module reaches the screened-only
single-press plan route on 0 paths, issues 0 bare cross-domain-reconciler calls that bypass the
driver, and references the per-domain re-plan leg on 0 paths — every evolved plan runs the SAME
composed safety gate + cross-domain reconciler the first plan ran, so a re-gen after the first can
never record un-reconciled (ADR-0036 finding-A safety parity). The guard is grep-checkable: this
module names none of those legs' symbols.

The loop is a SINGLE subscription-agent dispatch: ONE `dispatch` seam answers every agent class
(each plan-domain specialist, the quality judge, each safety lens), routed by its first argument.
`regenerate` composes the gate producer over that seam via `gate_dispatch.compose_gate_dispatch`
(the quality judge wrapped as `_JudgeClient`, the safety lenses dispatched directly — they share
the `(name, prompt, context)` call shape). It records nothing itself and opens no new store stream:
the inner engine's `record_plan`/promote is the only writer, so the driver's `SAFETY_BLOCKED` /
held-result outcome flows back to the caller untouched (a faithful pass-through — the loop adds no
bypass). Reasoning is the dispatched agents' (runtime A), never invented here.

Synthetic-only until real operator data is ingested (operator-gated): the raw plan-intake is the
current operator state read from `root`; the injected `deid_client` de-identifies it at the
crown-jewel `deid_in` boundary before any specialist dispatch.
"""

import datetime
import functools

from scripts.plan import plan_orchestrator, router
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.store import biomarker_meta, plan_schema, store

# The judge role slug the loop dispatches the QUALITY gate through the unified subscription seam.
_JUDGE_ROLE = "quality-judge"


class _JudgeClient:
    """Adapt the unified subscription dispatch into the quality gate's `.judge(payload)` seam.

    The quality gate calls `judge_client.judge(payload)`; the loop's ONE dispatch seam answers every
    agent class, so the judge is that seam addressed by `_JUDGE_ROLE`. This is the thin adapter that
    lets `compose_gate_dispatch` bind the judge to the same subscription dispatch the specialists +
    lenses use.

    Attributes:
        dispatch (Callable): The unified subscription-agent dispatch seam.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch

    def judge(self, payload):
        """Return the per-dimension score map by dispatching the quality judge over the seam."""
        return self.dispatch(_JUDGE_ROLE, "", payload)


def _read_raw_intake(root):
    """The current operator plan-intake the de-id boundary de-identifies (the loop re-reads live).

    The loop re-generates from the operator's CURRENT stored state, so the raw intake is that state
    read live from `root`. The crown-jewel `deid_in` boundary (inside `run_orchestrated`) de-identifies
    it through the injected `deid_client` before any specialist sees it — the loop hands the boundary
    the raw state, never a specialist.

    Args:
        root (str | Path): The store root.

    Returns:
        (dict) The raw operator plan-intake.
    """
    return {"operator_state": store.read_all(root)}


def regenerate(root, *, dispatch, deid_client, plan_date=None, trigger=None):
    """Drive the loop's re-gen through the full-composition front door and return the run result.

    Reads the current raw plan-intake for `root`, resolves `plan_date` to today's ISO date when
    `None`, composes the gate producer over the unified `dispatch` seam, and drives
    `plan_orchestrator.run_orchestrated` with that producer injected so the `loop_enabled` driver
    path is taken. Returns the `run_orchestrated` result unaltered (its recorded-survivors shape,
    or its honest-no-plan / `SAFETY_BLOCKED` shape). Never calls the screened-only route or the
    per-domain re-plan leg; never bypasses `plan_driver.drive`; records nothing itself.

    Args:
        root (str | Path): The store root the plans + the queue are recorded into.
        dispatch (Callable): The unified subscription-agent dispatch seam,
            `dispatch(name, prompt, context)` — a plan-domain name returns that domain's author
            envelope, `_JUDGE_ROLE` returns the quality score map, a safety-lens name returns that
            lens's findings. A real subscription agent in production; a fixture mock in tests.
        deid_client: The injected de-id model client for the crown-jewel `deid_in` boundary (a real
            `ModelClient`, or a fixture mock).
        plan_date (str, optional): The plans' YYYY-MM-DD date. `None` -> today's ISO date.
        trigger (str, optional): The cadence/manual trigger label (carried for the downstream
            debounce/rationale seams; not consumed here).

    Returns:
        (dict) The `run_orchestrated` result (recorded survivors + reconciliation + dvq_entries),
        or its honest-no-plan / `SAFETY_BLOCKED` shape on a blocked/held run.
    """
    plan_date = plan_date or datetime.date.today().isoformat()
    raw_intake = _read_raw_intake(root)
    store_read = functools.partial(store.read, root=root)
    gate_producer = compose_gate_dispatch(_JudgeClient(dispatch), dispatch)
    return plan_orchestrator.run_orchestrated(
        raw_intake, deid_client, dispatch, store_read, root,
        plan_date=plan_date, gate_dispatch=gate_producer,
    )


# --- ADR-0036-T2: the shared debounce gate + three-trigger convergence ----------------
#
# The three real trigger surfaces — a wearable/lab `biomarker::` write-event (route.py /
# confirm.py), the weekly cadence tick, and a care-chat free-text capture (care_chat.py) —
# converge on the ONE debounced entry `signal`, so no trigger reaches `regenerate` un-debounced.
# A whole-plan front-door re-gen is materially more expensive than a per-domain patch
# (ADR-0036 Consequences-Negative-1), so a re-gen fires only when the pinned min-interval has
# elapsed AND the `biomarker::` window carries a sustained directional signal; a free-text trigger
# is additionally rate-limited. The debounce state introduces ZERO new store stream (OQ-5): the
# last-re-gen date is DERIVED from the dated `plan::` history via `plan_schema.resolve_plan`, and
# the window is a query over the existing `biomarker::` series via the router trend feed — no
# `loop::`/`debounce::`/`regen-marker::` item, no `store.append` of a marker.

# The trigger labels the three surfaces pass into the single debounced entry.
CADENCE_TRIGGER = "cadence"
DATA_EVENT_TRIGGER = "biomarker-write"
FREE_TEXT_TRIGGER = "free-text"

# Pinned debounce parameters (ADR-0036 OQ-1) — fixed module constants, not runtime defaults.
# The weekly floor between ANY two re-gens (aligns with the weekly cadence trigger, bounds the
# whole-plan re-gen cost, Consequences-Negative-1); derived from the dated `plan::` history.
MIN_REGEN_INTERVAL_DAYS = 7
# The sustained window's minimum readings — REUSES the existing honest-absence n>=3 guardrail
# (`biomarker_meta.PROJECTION_MIN_TIMEPOINTS`), one constant with one home, never a second literal.
SUSTAINED_WINDOW_MIN_READINGS = biomarker_meta.PROJECTION_MIN_TIMEPOINTS
# The >= n readings must span at least this many days to count as sustained (not a same-day cluster).
SUSTAINED_WINDOW_SPAN_DAYS = 7
# The directional-consistency bar: the window's worst-wins registered-polarity trend
# (`router._recent_trend_direction`) must be one of these — a real directional signal, not `flat`.
SUSTAINED_TREND_DIRECTIONS = ("improving", "regressing")
# The additional bound on the care-chat trigger: at most one free-text re-gen per this many hours.
FREE_TEXT_RATE_LIMIT_HOURS = 24


def _date_of(timepoint):
    """The calendar date of a store timepoint (a date-only or a full-ISO string)."""
    return datetime.date.fromisoformat(str(timepoint).split("T", 1)[0])


def _last_regen_date(store_read, on_date):
    """The latest on-file `plan::` date across `PLAN_DOMAINS` — the derived last-re-gen date, or None.

    Reads each domain's `plan::<domain>` series through `plan_schema.resolve_plan` (the dated read):
    a domain with a plan resolves to its plan date, the max of which is the last time ANY plan was
    generated. Zero on-file plans resolve to None (no prior re-gen to debounce against).
    """
    dates = []
    for domain in plan_schema.PLAN_DOMAINS:
        resolved = plan_schema.resolve_plan(store_read(f"plan::{domain}"), on_date)
        if resolved["plan_date"] is not None:
            dates.append(resolved["plan_date"])
    return max(dates) if dates else None


def _sustained_signal(store_read):
    """Whether the `biomarker::` window carries a sustained directional signal.

    Two conjuncts: (a) the worst-wins registered-polarity trend over the feed is directional (one of
    `SUSTAINED_TREND_DIRECTIONS`, not `flat`), reusing `router._recent_trend_direction` — no parallel
    trend derivation; and (b) at least one feed stream carries >= `SUSTAINED_WINDOW_MIN_READINGS`
    distinct timepoints spanning >= `SUSTAINED_WINDOW_SPAN_DAYS` (a sustained series, never a single
    reading or a same-day cluster). A single new reading fails both — the debounce holds.
    """
    if router._recent_trend_direction(store_read) not in SUSTAINED_TREND_DIRECTIONS:
        return False
    for stream in router._POLARITY_FEED:
        dates = sorted({_date_of(r["timepoint"]) for r in store_read(stream)})
        if (len(dates) >= SUSTAINED_WINDOW_MIN_READINGS
                and (dates[-1] - dates[0]).days >= SUSTAINED_WINDOW_SPAN_DAYS):
            return True
    return False


def _should_regenerate(store_read, *, trigger, on_date):
    """Whether a trigger passes the shared debounce gate — pure over the derived read state.

    True only when the min-interval has elapsed since the derived last-re-gen date AND the
    `biomarker::` window carries a sustained directional signal; a `free-text` trigger ALSO enforces
    the 24h free-text rate limit against the same derived last-re-gen date. Reads state — never writes.
    """
    last = _last_regen_date(store_read, on_date)
    if last is not None:
        elapsed_days = (_date_of(on_date) - _date_of(last)).days
        if elapsed_days < MIN_REGEN_INTERVAL_DAYS:
            return False
        if trigger == FREE_TEXT_TRIGGER and elapsed_days * 24 < FREE_TEXT_RATE_LIMIT_HOURS:
            return False
    return _sustained_signal(store_read)


def signal(root, *, trigger, dispatch=None, deid_client=None, plan_date=None):
    """The ONE debounced entry every trigger kind calls; re-generate only when the gate passes.

    Runs the shared debounce predicate over DERIVED state (last-re-gen date from the dated `plan::`
    history; sustained-signal window over the `biomarker::` series). On pass it invokes T1's
    `regenerate(...)` exactly once and returns its re-gen receipt — it NEVER bypasses `regenerate`
    (the T1 front-door binding stays the sole path to the driver) and NEVER writes a store record.
    On a cadence trigger with no window signal it returns a hold+prompt payload (a `log_prompt` flag,
    0 new plans). On a debounced drop (inside window / inside min interval / over the free-text rate
    limit) it returns a no-op receipt with 0 new plans. The production server->trigger-site threading
    of the loop `dispatch`/`deid_client` seams is ADR-0036-T4; absent seams, a gate-pass is a no-op
    (`seams-unwired`) rather than a bare re-gen — the trigger sites notify additively either way.

    Args:
        root (str | Path): The store root the derived state is read from and the re-gen records into.
        trigger (str): The trigger label — `CADENCE_TRIGGER`, `DATA_EVENT_TRIGGER`, or
            `FREE_TEXT_TRIGGER`.
        dispatch (Callable, optional): The unified subscription-agent dispatch seam forwarded to
            `regenerate` on a gate-pass. None at a not-yet-wired production trigger site.
        deid_client (optional): The de-id model client forwarded to `regenerate`. None as above.
        plan_date (str, optional): The plans' YYYY-MM-DD date. None -> today's ISO date.

    Returns:
        (dict) The `regenerate` result on a gate-pass with seams present, else a no-op / hold+prompt
        receipt: `{"regenerated": bool, "log_prompt": bool, "trigger": str, "reason": str}`.
    """
    plan_date = plan_date or datetime.date.today().isoformat()
    root = root if root is not None else store.DEFAULT_ROOT
    store_read = functools.partial(store.read, root=root)
    if _should_regenerate(store_read, trigger=trigger, on_date=plan_date):
        if dispatch is not None and deid_client is not None:
            return regenerate(root, dispatch=dispatch, deid_client=deid_client,
                              plan_date=plan_date, trigger=trigger)
        return {"regenerated": False, "log_prompt": False, "trigger": trigger,
                "reason": "seams-unwired"}
    if trigger == CADENCE_TRIGGER and not _sustained_signal(store_read):
        return {"regenerated": False, "log_prompt": True, "trigger": trigger,
                "reason": "absent-signal-hold"}
    return {"regenerated": False, "log_prompt": False, "trigger": trigger, "reason": "debounced"}
