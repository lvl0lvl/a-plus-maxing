"""The per-plan dispatch budget — the autonomous loop's fail-closed aggregate-dispatch cap.

`run_orchestrated` (the autonomous drive layer) issues three dispatch classes per plan run: the N
plan-domain specialist dispatches, each post-generation gate dispatch (`gate_dispatch=`), and each
revise-loop re-author / adjudicator dispatch (ADR-0022-T2, Wave 4). An unbounded
generate -> judge -> safety-review -> revise loop, re-run as data arrives, can exceed the
subscription rate/usage ceiling the cost case rests on, with no fail-closed stop (ADR-0022 OQ-4).

`DispatchBudget` is the standalone accrual + cap mechanism the orchestrator wires into that
dispatch path: a configurable integer cap (a constructor parameter defaulting to the named
module-level `DEFAULT_DISPATCH_CAP`, NOT a hard-coded literal at the increment site) and a running
count starting at zero. `charge()` is called BEFORE each dispatch is issued: it increments the
count and, when the post-increment count would exceed the cap, raises `DispatchCapExceeded`
carrying the count reached — so the over-budget dispatch is never issued (fail-fast at the
boundary). `count` surfaces the current tally on both the normal and the halt paths.

The cap NUMBER is an operator/billing fact confirmed at the operator-present live-run checkpoint
downstream; this module is the MECHANISM only — no provider/ceiling lookup. It owns no store key,
performs no I/O, and dispatches nothing itself; the orchestrator owns the dispatch path and calls
this before each dispatch. `DISPATCH_CAP_EXCEEDED` mirrors the honest-no-plan reason vocabulary
(`deid_in.DEID_CALL_FAILED`, `plan_orchestrator.DEID_HALTED`) so the orchestrator's cap halt shares
the existing honest-no-plan shape.
"""

# The honest no-plan reason the cap-exceed halt surfaces — same kebab-string vocabulary as the
# de-id sentinel (`deid_in.DEID_CALL_FAILED` / `plan_orchestrator.DEID_HALTED`), so the
# orchestrator's cap halt reuses the existing honest-no-plan shape rather than a divergent one.
DISPATCH_CAP_EXCEEDED = "dispatch-cap-exceeded"

# The named module-level sane default the `DispatchBudget` constructor falls back to when no cap is
# passed — a documented ceiling well above a single normal run's tally (4 specialists + their gate
# + a bounded N=3 revise loop's re-author passes stay comfortably under it), so omitting the cap is
# the no-cap-pressure default. It is a PARAMETER, never a hard-coded literal at the increment site;
# the operator/billing ceiling is confirmed at the downstream live-run checkpoint.
DEFAULT_DISPATCH_CAP = 64


class DispatchCapExceeded(Exception):
    """The fail-closed halt signal: a charge would push the dispatch count past the cap.

    Raised by `DispatchBudget.charge` AT the over-budget increment, before the dispatch is issued,
    so the over-budget call is never made. Carries the count reached and the cap so the
    orchestrator surfaces the honest no-plan state (the `dispatch_count` in the halt result).

    Attributes:
        count (int): The dispatch count reached (the over-budget charge's post-increment value).
        cap (int): The configured cap the count exceeded.
        reason (str): The honest no-plan reason token (`DISPATCH_CAP_EXCEEDED`).
    """

    def __init__(self, count, cap):
        self.count = count
        self.cap = cap
        self.reason = DISPATCH_CAP_EXCEEDED
        super().__init__(
            f"dispatch budget exceeded: count {count} > cap {cap}"
        )


class DispatchBudget:
    """A per-plan dispatch counter with a configurable fail-closed cap.

    Counts the orchestrator's aggregate dispatches (specialist + gate + revise) and fails closed
    when a charge would exceed the cap — the over-budget dispatch is never issued. The cap is a
    constructor parameter defaulting to the named module-level `DEFAULT_DISPATCH_CAP`; the count
    is readable on both the normal and the halt paths.

    Attributes:
        cap (int): The configured dispatch cap (defaults to `DEFAULT_DISPATCH_CAP`).
        count (int): The running dispatch count, starting at zero.
    """

    def __init__(self, cap=DEFAULT_DISPATCH_CAP):
        self.cap = cap
        self.count = 0

    def charge(self):
        """Account for one dispatch about to be issued; fail closed when it would exceed the cap.

        Call BEFORE each dispatch. Increments the count and, when the post-increment count exceeds
        the cap, raises `DispatchCapExceeded` carrying the count reached — so the over-budget
        dispatch is never issued. Under the cap, returns the new count.

        Returns:
            (int) The post-increment dispatch count (when under the cap).
        """
        self.count += 1
        if self.count > self.cap:
            raise DispatchCapExceeded(self.count, self.cap)
        return self.count
