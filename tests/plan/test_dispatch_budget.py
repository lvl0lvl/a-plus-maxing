"""Tests for the per-plan dispatch budget + the orchestrator's fail-closed cap (ADR-0022-T3).

Two layers, mirroring the recipe's two TDD cycles:

  Cycle 1 -- the standalone counter + cap mechanism (`scripts.plan.dispatch_budget`):
    - AC-1 (unit): the budget accrues a count incremented across every recorded dispatch (the
      specialist / gate / revise dispatch classes are each counted) -- over a known dispatch
      sequence the final count equals the number of dispatches recorded.
    - AC-2 (unit): a cap set BELOW the dispatch tally signals the fail-closed halt BEFORE the
      over-budget dispatch is issued, carrying the count reached; a cap above the tally never
      signals the halt.
    - AC-4 (unit): the count is surfaced (readable) on both the normal-completion path AND the
      cap-exceed halt path -- the count is never silently dropped.
    - Risk gate (ADR-0022 OQ-4): the cap-exceed path is fail-closed (the over-budget dispatch is
      NOT issued; the count-at-halt is surfaced).

  Cycle 2 -- the orchestrator wiring + the configurable two-config proof + the end-to-end halt
  (`scripts.plan.plan_orchestrator.run_orchestrated`), REUSING the orchestrator test fixtures
  (`_RecordingDispatch` / `_FixedDeidClient` / `_deid_summary` / `_sustaining_authors` /
  `_seed_store` / `PLAN_DATE`) so every run is mock-backed with 0 live spend.

The cap NUMBER is an operator/billing fact confirmed downstream; this task builds the MECHANISM
only -- a configurable cap (parameter, not a hard-coded literal at the increment site), proven by
running two configs over the SAME fixture (a low cap that trips vs a high cap that does not).
"""

import pytest

from scripts.plan.dispatch_budget import (
    DISPATCH_CAP_EXCEEDED,
    DEFAULT_DISPATCH_CAP,
    DispatchBudget,
    DispatchCapExceeded,
)
from scripts.plan.plan_orchestrator import run_orchestrated
from scripts.store import store
from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import PLAN_DATE, _seed_store
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)


# === Cycle 1: the standalone counter + cap mechanism ===========================


# --- AC-1: the budget accrues a count across every recorded dispatch ------------


def test_count_accrues_one_per_dispatch():
    # over a known sequence of dispatches, the final count equals the number recorded -- each
    # dispatch class (specialist / gate / revise) is one increment, counted identically.
    budget = DispatchBudget(cap=100)
    assert budget.count == 0
    for _ in range(7):
        budget.charge()
    assert budget.count == 7


def test_count_starts_at_zero():
    budget = DispatchBudget(cap=100)
    assert budget.count == 0


# --- AC-2: a cap below the tally fails closed BEFORE the over-budget dispatch ----


def test_cap_below_tally_signals_halt_before_over_budget_dispatch():
    # a cap of 2 admits exactly 2 dispatches; the 3rd charge -- the over-budget one -- signals the
    # fail-closed halt. The signal fires AT the increment that would exceed, before the dispatch.
    budget = DispatchBudget(cap=2)
    budget.charge()  # 1 -- under cap
    budget.charge()  # 2 -- at cap
    with pytest.raises(DispatchCapExceeded) as exc:
        budget.charge()  # 3 -- would exceed -> fail closed
    # the count reached is carried on the halt signal (the count-at-halt is surfaced)
    assert exc.value.count == 3
    assert exc.value.cap == 2
    assert exc.value.reason == DISPATCH_CAP_EXCEEDED


def test_cap_above_tally_never_signals_halt():
    # a cap comfortably above the tally admits every dispatch -- the halt never fires.
    budget = DispatchBudget(cap=100)
    for _ in range(5):
        budget.charge()
    assert budget.count == 5


def test_over_budget_dispatch_is_not_counted_past_the_cap_more_than_once():
    # fail-closed: once the cap is exceeded the budget refuses further charges (the over-budget
    # call is never issued) -- a second charge re-signals, it does not silently advance the count.
    budget = DispatchBudget(cap=1)
    budget.charge()  # 1 -- at cap
    with pytest.raises(DispatchCapExceeded):
        budget.charge()  # 2 -- exceeds
    with pytest.raises(DispatchCapExceeded):
        budget.charge()  # still exceeds -- fail closed, not a silent pass


# --- AC-4: the count is surfaced on BOTH the normal and the halt paths ----------


def test_count_surfaced_on_normal_path():
    budget = DispatchBudget(cap=10)
    budget.charge()
    budget.charge()
    assert budget.count == 2  # readable mid-run, no halt


def test_count_surfaced_on_halt_path():
    budget = DispatchBudget(cap=1)
    budget.charge()
    try:
        budget.charge()
    except DispatchCapExceeded as exc:
        # the count is readable on the budget AND carried on the signal -- never silently dropped
        assert budget.count == exc.count == 2
    else:  # pragma: no cover - the charge must have raised
        pytest.fail("the over-budget charge did not signal the halt")


# --- the cap is a parameter with a NAMED module-level default (not a literal) ----


def test_default_cap_is_the_named_module_constant():
    # omitting the cap falls back to the named module-level sane default -- NOT a hard-coded
    # literal at the increment site. The default is well above a single normal run's tally.
    budget = DispatchBudget()
    assert budget.cap == DEFAULT_DISPATCH_CAP
    assert isinstance(DEFAULT_DISPATCH_CAP, int)
    assert DEFAULT_DISPATCH_CAP > 4  # above a single 4-specialist run's specialist tally


# === Cycle 2: orchestrator wiring + configurability proof + end-to-end halt =====


def _run(tmp_path, *, dispatch_cap, domains=("workout", "nutrition")):
    """Run `run_orchestrated` over the mock fixtures with the given cap (0 live spend)."""
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=domains, dispatch_cap=dispatch_cap,
    )
    return out, dispatch


# --- AC-1 (end-to-end): the count == the observed dispatch tally ----------------


def test_count_equals_observed_dispatch_tally_end_to_end(tmp_path):
    # over a synthetic run, the count the orchestrator accrues equals the dispatch tally it
    # observed -- asserted against the OBSERVED count (the recorded specialist dispatches), not a
    # guessed constant. With the no-op gate default + no revise hook, the tally is the N
    # specialist dispatches.
    out, dispatch = _run(tmp_path, dispatch_cap=DEFAULT_DISPATCH_CAP)
    assert out["dispatch_count"] == len(dispatch.calls)
    assert out["dispatch_count"] == 2  # the two requested specialist domains


# --- AC-2 (end-to-end): cap below the tally -> halt, 0 plans past the cap --------


def test_cap_below_tally_halts_records_zero_plans_and_surfaces_count(tmp_path):
    # cap=1 is below the 2-specialist tally: the orchestrator HALTS to honest no-plan, surfaces the
    # count reached, and records 0 plans past the cap (the over-budget specialist is never
    # dispatched, the inner engine is never reached). The positive control below proves the halt is
    # the cap's doing.
    out, dispatch = _run(tmp_path, dispatch_cap=1)
    assert out["reason"] == DISPATCH_CAP_EXCEEDED
    assert out["dispatch_count"] == 2  # the over-budget charge's count is surfaced
    assert out["results"] == {}
    # 0 plans recorded past the cap for EVERY requested domain
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=tmp_path) == []


def test_cap_above_tally_positive_control_records_a_plan(tmp_path):
    # POSITIVE CONTROL (non-tautological): the SAME run with the cap ABOVE the tally DOES record
    # >=1 plan -- so the halt above is the cap's doing, not an unrelated failure.
    out, _ = _run(tmp_path, dispatch_cap=100)
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    assert store.read("plan::workout", root=tmp_path) != []


# --- AC-3 (configurable, two-config proof): same fixture, two caps, DIFFER -------


def test_cap_is_configurable_two_configs_yield_different_outcomes(tmp_path):
    # the non-tautological configurability proof: the SAME fixture run under config-A (cap above
    # the tally) vs config-B (cap below the tally) yields DIFFERENT outcomes. A hard-coded cap
    # would yield the same outcome regardless of the config passed -> this would not DIFFER.
    out_a, _ = _run(tmp_path / "a", dispatch_cap=100)  # config-A: above the tally
    out_b, _ = _run(tmp_path / "b", dispatch_cap=1)    # config-B: below the tally

    # config-A completes normally (records a plan, no cap reason); config-B halts on the cap
    a_recorded = [d for d, r in out_a["results"].items() if r.get("recorded") is True]
    assert len(a_recorded) >= 1
    assert out_a.get("reason") != DISPATCH_CAP_EXCEEDED

    assert out_b["reason"] == DISPATCH_CAP_EXCEEDED
    assert out_b["results"] == {}

    # the two outcomes DIFFER -- the cap is a parameter, not a hard-coded constant
    assert (out_a.get("reason"), bool(a_recorded)) != (out_b.get("reason"), False)


# --- AC-4 (end-to-end): the count is reported on the normal-completion run -------


def test_normal_run_reports_the_count_in_the_result(tmp_path):
    out, dispatch = _run(tmp_path, dispatch_cap=100)
    assert "dispatch_count" in out
    assert out["dispatch_count"] == len(dispatch.calls)


# --- the default-cap path is the unchanged-behavior path (no Wave-2 regression) --


def test_default_cap_omitted_runs_normally_and_records(tmp_path):
    # omitting `dispatch_cap` uses the named module-level default (well above a normal run's
    # tally), so the default path is the unchanged Wave-2 behavior -- a plan still records.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    assert out["dispatch_count"] == 2


# --- API-01: `dispatch_count` is surfaced UNIFORMLY on every halt path -----------


def test_deid_halt_surfaces_dispatch_count_zero(tmp_path):
    # API-01: the de-id sentinel halt issues 0 dispatches, so it surfaces `dispatch_count: 0` —
    # the SAME key the normal + cap-halt paths carry, so the T2 revise loop can read
    # `result["dispatch_count"]` uniformly without a missing-key branch per halt class. A de-id
    # halt missing the key turns this RED.
    from scripts.model.client import ModelCallError

    store_read = _seed_store(tmp_path)
    failing_client = _FixedDeidClient(ModelCallError("backend de-id call failed"))
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), failing_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    assert out["deidentified"] is False
    assert out["dispatch_count"] == 0, "the de-id halt omitted dispatch_count (0 dispatches issued)"
    assert dispatch.calls == []  # 0 dispatches actually issued (the count is accurate)
