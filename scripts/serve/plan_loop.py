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

from scripts.plan import plan_orchestrator
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.store import store

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
