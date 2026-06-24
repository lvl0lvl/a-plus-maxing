"""Tests for the single bounded revise loop composing both gates (ADR-0022-T2 — the keystone).

`scripts.plan.plan_orchestrator.run_orchestrated` finally INVOKES the `gate_dispatch=` seam
that has been HELD (resolved + charge-wrapped, never called) since ADR-0022-T1, and composes
both Wave-3 gates (`quality_judge` + `safety_review`) into ONE bounded revise loop: after the
inner engine assembles the plan, run BOTH gates over the `run_generation` result through the
composed `gate_dispatch` callable → on a quality REVISE (with safety passing) re-DISPATCH the
REVISE-targeted domain(s) through the orchestrator's `dispatch` seam (the same seam that built
the initial `authors`, NOT the energy-bounce `reauthor` hook — MF-1) + re-run the inner engine
+ re-run BOTH gates → bounded cap N=3 → on non-convergence HALT to honest no-plan. The safety
disposition is FAIL-CLOSED: `safety_passed is True` is the ONLY surface path; a `False` / absent
/ ambiguous / un-composed safety verdict is TERMINAL `SAFETY_BLOCKED`. INV-CRITICAL-NON-OVERRIDABLE:
a seeded CRITICAL / H1-H2 inner hold surfaces 0 plans via ANY revise pass.

These pin:
  - AC-4: both UNDERLYING gate CALLABLES (`quality_judge.quality_judge` AND `safety_review.review_plan`)
    run each pass — spied via recording wrappers, not the composed seam (MF-2);
  - AC-1: a clearable quality miss converges within <=3 passes; the recorded plan is the
    re-authored (pass-2) content, differing from the pre-revise plan (a real re-author, not a
    judge flip — MF-1);
  - Security HIGH-1: an ambiguous / malformed / None / absent-key safety disposition fail-closes
    to `SAFETY_BLOCKED` (the only surface path is `safety_passed is True`);
  - Security HIGH-2: the autonomous loop entered with a no-op / absent gate (no whole-plan safety
    tier composed) → `SAFETY_BLOCKED`, 0 unreviewed plan;
  - the EXACT composed-gate count (1 on a clean single pass, N+1 over N revise passes — SF-4);
  - AC-3 (Cycle 3): a non-converging quality miss HALTS at N=3 (re-dispatch == 3, NOT 4);
  - AC-2 (Cycle 4): a standing safety block is terminal — 0 plans, never revise-past;
  - AC-5 (Cycle 5): a seeded CRITICAL/H1-H2 inner hold is never surfaced/re-dispatched by the loop;
  - the full runtime-stage-order E2E (Cycle 6): de-id IN → orchestrate/assemble → {judge || safety}
    → revise loop → store-mediated `reemit_maintained` (render-then-`reinsert_out`); 0 live spend,
    0 real PII, the synthetic identity token in the gitignored artifact and absent from store/tracked.

Every client/dispatch is a mock/fixture; no test hits a live API, and the test tree carries 0 real
operator PII (synthetic tokens only).
"""

import datetime
import json
import os
import subprocess
from pathlib import Path

from scripts.plan.dispatch_budget import DISPATCH_CAP_EXCEEDED
from scripts.plan.plan_orchestrator import (
    PROMOTE_FAILED,
    REVISE_EXHAUSTED,
    SAFETY_BLOCKED,
    run_orchestrated,
)
from scripts.plan.quality_judge import ACCEPT, REVISE, quality_judge
from scripts.plan.safety_review import review_plan
from scripts.store import store

# --- fixture import block (the loop's own suite re-imports the sibling fixtures) ---
from tests.plan.test_deid_in import (
    SYNTHETIC_LAB,
    SYNTHETIC_NAME,
    _FixedDeidClient,
    _raw_intake,
)
from tests.plan.test_generate_plan import (
    PLAN_DATE,
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _peptide_rec,
    _seed_store,
    _supplement_rec,
    _workout_rec,
)
from tests.plan.test_orchestrate import (
    _SUPP_CONFLICT,
    _conflict_authors,
    _liaison,
    _nutrition,
    _recon,
)
from tests.plan.test_adjudicate import _override_record
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)
from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
from tests.plan.test_safety_review import _RecordingLensDispatch, _no_findings_dispatch


# --- composite-gate helpers ----------------------------------------------------


def _recording_quality(scores):
    """A recording wrapper around `quality_judge.quality_judge` (the MF-2 two-callable spy).

    Records every assembled plan it scores so a test asserts the QUALITY callable FIRED per pass
    (its `.calls` non-empty), distinct from the composed `gate_dispatch` (which a single-call spy
    cannot tell apart). Returns the native quality verdict.
    """
    judge_client = _FixedJudgeClient(scores)
    calls = []

    def wrapper(assembled_plan):
        verdict = quality_judge(assembled_plan, judge_client)
        calls.append(verdict)
        return verdict

    wrapper.calls = calls
    return wrapper


def _recording_safety(lens_dispatch):
    """A recording wrapper around `safety_review.review_plan` (the MF-2 two-callable spy).

    Records every assembled plan it reviews so a test asserts the SAFETY callable FIRED per pass
    (its `.calls` non-empty). Returns the native safety verdict (`passed` / `findings`).
    """
    calls = []

    def wrapper(assembled_plan):
        verdict = review_plan(assembled_plan, lens_dispatch)
        calls.append(verdict)
        return verdict

    wrapper.calls = calls
    return wrapper


def _composing_gate(quality_wrapper, safety_wrapper, *, revise_domains=()):
    """A composite `gate_dispatch` that runs BOTH gate callables and returns one disposition.

    The orchestrator-owned composite seam (Architect C-1): ONE callable drives the two gates with
    DIFFERENT native signatures, composing `accept` (from the quality verdict's ACCEPT/REVISE) and
    `safety_passed` (from the safety verdict's `passed` bool). On a quality REVISE it carries the
    `revise_domains` the loop re-authors. Records each composed dispatch for the EXACT-count pin.
    """
    calls = []

    def gate(assembled_plan):
        calls.append(assembled_plan)
        q = quality_wrapper(assembled_plan)
        s = safety_wrapper(assembled_plan)
        accept = q["verdict"] == ACCEPT
        disposition = {"accept": accept, "safety_passed": s["passed"]}
        if not accept:
            disposition["revise_domains"] = list(revise_domains)
        return disposition

    gate.calls = calls
    return gate


def _clean_composing_gate(*, revise_domains=()):
    """A composite gate over a clean judge + a no-findings safety dispatch (both PASS)."""
    return _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=revise_domains,
    )


# ===============================================================================
# Cycle 1: the loop composition (both gates each pass) + the seam fires LIVE
# ===============================================================================


# --- AC-4: BOTH underlying gate callables run each pass (MF-2 two-callable spy) ---


def test_both_gates_run_each_pass(tmp_path):
    # AC-4 / MF-2: a clean run surfaces a plan AND fires BOTH underlying callables over the
    # assembled `run_generation` result. Spy the TWO callables (not the composed seam — a single
    # composed spy sees ONE call regardless). A composition that silently dropped the safety gate
    # leaves the safety wrapper's `.calls` empty -> RED.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    quality_wrapper = _recording_quality(_clean_scores())
    safety_wrapper = _recording_safety(_no_findings_dispatch())
    gate = _composing_gate(quality_wrapper, safety_wrapper)

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
    )

    # a plan was surfaced (both gates passed)
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    # BOTH underlying callables fired over the assembled result (per pass)
    assert quality_wrapper.calls, "the QUALITY callable did not fire"
    assert safety_wrapper.calls, "the SAFETY callable did not fire (a dropped safety gate)"


def test_exact_composed_gate_count_single_pass(tmp_path):
    # SF-4: the composed `gate_dispatch` fires EXACTLY ONCE over the assembled result on a clean
    # single-pass run (not just >= 1). An off-by-one or a dropped-gate REDs.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    gate = _clean_composing_gate()

    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
    )

    assert len(gate.calls) == 1, f"clean single-pass composed-gate count != 1: {len(gate.calls)}"


def test_ambiguous_safety_disposition_fail_closed(tmp_path):
    # Security HIGH-1 (the load-bearing fail-closed probe): the ONLY surface path is
    # `safety_passed is True`. A malformed / None / absent-key / non-bool / non-dict / raised
    # safety disposition halts to `SAFETY_BLOCKED`, 0 plans. A loop that reads only
    # `safety_passed is False` would fall through the ambiguous cases and SURFACE the plan -> RED.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    def _raising_gate(assembled_plan):
        raise RuntimeError("safety lens dispatch failed mid-review")

    ambiguous_gates = (
        lambda assembled_plan: {"accept": True, "safety_passed": False},   # explicit False
        lambda assembled_plan: {"accept": True, "safety_passed": None},    # None
        lambda assembled_plan: {"accept": True},                            # absent key
        lambda assembled_plan: {"accept": True, "safety_passed": "ok"},    # non-bool
        lambda assembled_plan: {"accept": True, "safety_passed": 1},       # truthy non-bool
        lambda assembled_plan: ["not", "a", "dict"],                        # non-dict result
        lambda assembled_plan: None,                                        # None result
        _raising_gate,                                                      # the gate raised
    )

    for i, gate in enumerate(ambiguous_gates):
        root = tmp_path / f"case-{i}"
        case_store_read = _seed_store(root)
        dispatch = _RecordingDispatch(_sustaining_authors())
        out = run_orchestrated(
            _raw_intake(), deid_client, dispatch, case_store_read, root,
            plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
        )
        assert out["reason"] == SAFETY_BLOCKED, f"ambiguous disposition surfaced (not SAFETY_BLOCKED): {gate}"
        assert out["results"] == {}, "an ambiguous-safety run surfaced a plan"
        for domain in ("workout", "nutrition"):
            assert store.read(f"plan::{domain}", root=root) == []


def test_autonomous_loop_requires_real_gate(tmp_path):
    # Security HIGH-2: the autonomous revise-loop entered with a no-op / absent gate (no real
    # whole-plan safety tier composed — no `safety_passed is True`) → `SAFETY_BLOCKED`, 0 plans.
    # DISTINCT from the legacy Wave-2 non-loop default path (gate_dispatch is None), where the
    # inner adjudicate gate is the floor and a plan surfaces.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # a gate that is PROVIDED but composes NO safety tier (the no-op / absent-tier case)
    def no_safety_tier_gate(assembled_plan):
        return {"accept": True}  # no safety_passed asserted

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=no_safety_tier_gate,
    )

    assert out["reason"] == SAFETY_BLOCKED
    assert out["results"] == {}, "the autonomous loop surfaced an unreviewed plan"
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=tmp_path) == []


# --- AC-1 (Cycle 1 slice): a clearable quality miss converges (real re-author) ---


def _empty_workout_envelope():
    """A workout author envelope with 0 recommendations → an empty in-scope coverage-gap section."""
    return {"specialist": "personal-trainer", "recommendations": []}


def _filled_workout_envelope():
    """A workout author envelope with a real recommendation → a filled in-scope section."""
    return _author(_workout_rec("Goblet squat", 3))


def test_clearable_quality_miss_converges_within_n(tmp_path):
    # AC-1: a quality miss (pass-1 empty workout section) the per-domain RE-DISPATCH CLEARS within
    # <=3 passes → a plan surfaces, both gate callables re-run each pass, and the recorded plan is
    # the pass-2 (re-authored) content, DIFFERING from the pre-revise plan (a real re-author, not a
    # judge flip over identical content — the tautology MF-1 forbids).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    # pass-1 workout is EMPTY (quality-defective); the re-dispatch returns a FILLED workout.
    dispatch = _RecordingDispatch({"workout": _empty_workout_envelope()})

    def reissuing_dispatch(domain, prompt, summary):
        dispatch.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        # the re-dispatch (2nd call for workout) returns the FILLED envelope; the 1st is empty.
        n = len([c for c in dispatch.calls if c["domain"] == domain])
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    quality_wrapper = _recording_quality(_clean_scores())
    safety_wrapper = _recording_safety(_no_findings_dispatch())
    gate = _composing_gate(quality_wrapper, safety_wrapper, revise_domains=("workout",))

    out = run_orchestrated(
        _raw_intake(), deid_client, reissuing_dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    # converged within <=3 passes: a plan surfaced
    assert out["results"]["workout"]["recorded"] is True
    rows = store.read("plan::workout", root=tmp_path)
    assert rows != [], "no plan surfaced past the clearable quality miss"
    # the recorded plan is the re-authored (filled) content, NOT the empty pass-1 plan
    recorded_plan = rows[-1]["value"]
    assert recorded_plan.get("exercises"), "the recorded plan is the empty pre-revise content (no real re-author)"
    assert any(ex.get("name") == "Goblet squat" for ex in recorded_plan["exercises"])
    # both callables re-ran each pass (>= 2 passes here: the miss + the converged re-run)
    assert len(quality_wrapper.calls) >= 2
    assert len(safety_wrapper.calls) >= 2
    # the dispatch SEAM was re-issued for workout (MF-1: NOT the reauthor hook)
    workout_dispatches = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_dispatches) == 2, "the dispatch seam was not re-issued exactly once on the revise"


def test_exact_composed_gate_count_two_passes(tmp_path):
    # SF-4: N revise passes → N+1 composed-gate calls. One revise pass (the converged miss above)
    # → exactly 2 composed dispatches (1 initial + 1 re-run).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch({"workout": _empty_workout_envelope()})

    def reissuing_dispatch(domain, prompt, summary):
        dispatch.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        n = len([c for c in dispatch.calls if c["domain"] == domain])
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    run_orchestrated(
        _raw_intake(), deid_client, reissuing_dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    assert len(gate.calls) == 2, f"one-revise composed-gate count != 2 (N+1): {len(gate.calls)}"


# ===============================================================================
# Cycle 2: the quality-REVISE re-trigger (defective -> re-author -> converge)
# ===============================================================================


def test_revise_redispatches_and_reruns(tmp_path):
    # AC-1 (the re-trigger, full): the per-domain quality re-dispatch is the `dispatch` SEAM
    # re-issued (MF-1: NOT `reauthor`, the energy-bounce hook). Seed a quality-defective workout
    # (an empty in-scope section). The loop REBUILDS the `authors` dict from a FRESH `dispatch`
    # re-issue (re-running with the SAME authors is store-idempotent — no convergence); the
    # re-authored plan that clears the defect surfaces. Convergence is non-tautological: pass-1 and
    # pass-2 envelopes are STRUCTURALLY DISTINCT, and the recorded content equals the pass-2
    # (re-authored) content and DIFFERS from the pre-revise plan (a judge flip over identical
    # content would NOT satisfy it).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    dispatch = _RecordingDispatch({"workout": _empty_workout_envelope()})

    def reissuing_dispatch(domain, prompt, summary):
        dispatch.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        n = len([c for c in dispatch.calls if c["domain"] == domain])
        # pass-1 envelope is EMPTY (the quality defect); the re-dispatch returns the FILLED one —
        # structurally distinct (a filled in-scope section where pass-1 was empty).
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, reissuing_dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    # the `dispatch` seam was RE-ISSUED for the REVISE-targeted domain (a SECOND call for workout)
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 2, "the dispatch seam was not re-issued for the REVISE domain"
    # the surfaced/recorded plan is the pass-2 (re-authored) content — a REAL re-author
    assert out["results"]["workout"]["recorded"] is True
    rows = store.read("plan::workout", root=tmp_path)
    recorded_plan = rows[-1]["value"]
    assert recorded_plan.get("exercises"), "recorded plan is the empty pre-revise content (no re-author)"
    # and it DIFFERS from the pre-revise (empty) plan — the pass-1 plan had no exercises
    assert recorded_plan != {"exercises": []}
    assert any(ex.get("name") == "Goblet squat" for ex in recorded_plan["exercises"])


def test_revise_uses_dispatch_seam_not_reauthor(tmp_path):
    # MF-1 (the SEAM, not the hook): the quality re-author goes through the `dispatch` seam, NEVER
    # the energy-bounce `reauthor` hook. Inject a `reauthor` SPY and assert it is NEVER called on a
    # quality REVISE (the energy bounce did not fire; the re-author is the dispatch seam). A loop
    # that mistakenly drove `reauthor` for the quality re-author turns this RED.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    dispatch = _RecordingDispatch({"workout": _empty_workout_envelope()})

    def reissuing_dispatch(domain, prompt, summary):
        dispatch.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        n = len([c for c in dispatch.calls if c["domain"] == domain])
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    reauthor_calls = []

    def reauthor_spy(domain, constraint):
        reauthor_calls.append((domain, constraint))
        return None

    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    run_orchestrated(
        _raw_intake(), deid_client, reissuing_dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate, reauthor=reauthor_spy,
    )

    # the quality re-author is the `dispatch` seam re-issue, NOT the energy-bounce `reauthor` hook
    assert reauthor_calls == [], "the quality re-author drove the energy-bounce `reauthor` hook (MF-1 violated)"
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 2, "the dispatch seam was not re-issued for the REVISE domain"


# ===============================================================================
# Cycle 3: the N=3 bounded halt (non-converging -> 0 plans past N)
# ===============================================================================


def _counting_dispatch(envelope_for):
    """A dispatch seam returning `envelope_for(domain, nth_call)` and counting per-domain calls.

    `envelope_for(domain, n)` returns the envelope for the n-th (1-based) call to `domain`, so a
    fixture controls whether a re-dispatch CLEARS the defect (a filled envelope) or never does
    (always empty). Records every call on `.calls` for the EXACT re-dispatch-count pin.
    """
    calls = []

    def dispatch(domain, prompt, summary):
        calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        n = len([c for c in calls if c["domain"] == domain])
        return envelope_for(domain, n)

    dispatch.calls = calls
    return dispatch


def test_non_converging_halts_at_n3_zero_plans(tmp_path):
    # AC-3 / Risk R1 (the bounded-revise probe): a NON-converging quality miss (the workout stays
    # empty on EVERY re-dispatch, the judge returns REVISE every pass) HALTS at `revise_cap = 3`
    # and surfaces 0 plans. The honest no-plan family shape: `reason == REVISE_EXHAUSTED`,
    # `results == {}`, 0 `plan::<domain>` in the store. EXACT re-dispatch count (SF-5): the
    # per-domain `dispatch` re-issue fired EXACTLY 3 times (== 3, NOT 4 — the cap must not allow a
    # 4th re-author). Count of plans past N=3 = 0.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    # the workout NEVER clears — every dispatch (initial + every re-dispatch) returns an empty section
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    gate = _composing_gate(
        _recording_quality(_clean_scores()),  # the structural floor REVISEs the empty section every pass
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    assert out["reason"] == REVISE_EXHAUSTED, f"non-converging miss did not halt REVISE_EXHAUSTED: {out['reason']}"
    assert out["results"] == {}, "a non-converging miss surfaced a plan"
    assert store.read("plan::workout", root=tmp_path) == []
    # the dispatch seam re-issued EXACTLY 3 times (== revise_cap), NOT 4 (the initial call + 3 re-dispatches)
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 1 + 3, f"re-dispatch count != 3 (initial + 3): got {len(workout_calls) - 1} re-dispatches"


def test_converges_on_pass_3_positive_control(tmp_path):
    # AC-3 POSITIVE CONTROL (failing-capable proof): the SAME shape that CONVERGES on the 3rd gate
    # evaluation (cap=3 ALLOWS it) surfaces a plan AND re-dispatches EXACTLY 2 times (the 2
    # re-authors that precede the converged pass-3 result) — so the halt above is the CAP, not the
    # seed being unbuildable, and the exact counts pin the loop boundary.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    # the workout clears on the 3rd dispatch (initial empty, re-dispatch-1 empty, re-dispatch-2 filled)
    dispatch = _counting_dispatch(
        lambda domain, n: _filled_workout_envelope() if n >= 3 else _empty_workout_envelope()
    )
    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    # converged within the cap: a plan surfaced
    assert out["results"]["workout"]["recorded"] is True
    assert store.read("plan::workout", root=tmp_path) != []
    # EXACTLY 2 re-dispatches preceded the converged pass-3 result (initial + 2 re-dispatches = 3 calls)
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 1 + 2, f"converged re-dispatch count != 2: got {len(workout_calls) - 1}"


def test_revise_cap_is_configurable(tmp_path):
    # the bound is a configurable `revise_cap` (defaulting to DEFAULT_REVISE_CAP = 3), so a tighter
    # cap halts sooner — a non-converging miss at `revise_cap=1` re-dispatches EXACTLY 1 time.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate, revise_cap=1,
    )

    assert out["reason"] == REVISE_EXHAUSTED
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 1 + 1, "revise_cap=1 did not bound re-dispatch to exactly 1"


# ===============================================================================
# Cycle 4: the SAFETY-terminal (standing safety block -> halt, 0 plans, never revise-past)
# ===============================================================================


def _standing_block_safety():
    """A safety wrapper that returns `passed: False` with a finding on EVERY pass (re-fires)."""
    def wrapper(assembled_plan):
        return {
            "findings": [{"id": "cumulative-stimulant-load", "concern": "exceeds the safe ceiling",
                          "severity": "high"}],
            "passed": False,
            "lenses": ("medical-safety-reviewer", "health-edge-case-reviewer"),
        }

    wrapper.calls = []
    return wrapper


def test_standing_safety_block_is_terminal_zero_plans(tmp_path):
    # AC-2 / Risk R2 (the standing-safety-block-terminal probe): a safety review returning
    # `passed: False` with a finding that RE-FIRES every pass -> the loop HALTS, surfaces 0 plans,
    # and NEVER re-authors past it. `reason == SAFETY_BLOCKED`, `results == {}`, 0 `plan::` in
    # store, AND the `dispatch` SEAM was re-issued 0 times past the initial pass (SF-1 — one initial
    # call per domain, no second call; the re-author callable is the dispatch seam, NOT `reauthor`).
    # The safety block is TERMINAL — no revise pass is attempted past it (DISTINCT from a quality
    # REVISE, which DOES re-dispatch). The negative assertion: count of plans surfaced past a
    # standing safety block = 0.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    # the quality gate would even REVISE (the workout is empty), but SAFETY is checked FIRST and is
    # standing-blocked — so the loop must halt on safety, never reach the quality re-author.
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    quality_wrapper = _recording_quality(_clean_scores())
    safety_wrapper = _standing_block_safety()

    def gate(assembled_plan):
        q = quality_wrapper(assembled_plan)
        s = safety_wrapper(assembled_plan)
        return {"accept": q["verdict"] == ACCEPT, "safety_passed": s["passed"],
                "revise_domains": ["workout"]}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    assert out["reason"] == SAFETY_BLOCKED, f"standing safety block did not halt SAFETY_BLOCKED: {out['reason']}"
    assert out["results"] == {}, "a standing-safety-blocked run surfaced a plan"
    assert store.read("plan::workout", root=tmp_path) == []
    # the dispatch seam was NOT re-issued past the initial pass — 0 quality re-authors past the block
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 1, f"the loop re-authored past a standing safety block: {len(workout_calls)} dispatches"


def test_safety_block_precedes_quality_revise(tmp_path):
    # AC-2 (the precedence): a plan that is BOTH quality-defective AND safety-blocked halts on
    # SAFETY (terminal), never re-authored. The safety check precedes the quality REVISE branch, so
    # a `passed: False` short-circuits BEFORE the re-author. A loop that treated `passed: False`
    # like a quality REVISE would re-author -> RED (the dispatch count would exceed 1).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _counting_dispatch(lambda domain, n: _filled_workout_envelope())

    # quality ACCEPTs (filled plan) but safety BLOCKS — proving the safety terminal is independent
    # of the quality verdict and precedes any re-author.
    def gate(assembled_plan):
        review_plan(assembled_plan, _no_findings_dispatch())  # exercise the callable shape
        return {"accept": True, "safety_passed": False}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    assert out["reason"] == SAFETY_BLOCKED
    assert out["results"] == {}
    assert store.read("plan::workout", root=tmp_path) == []
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    assert len(workout_calls) == 1, "the loop re-authored despite a standing safety block"


# ===============================================================================
# Cycle 5: INV-CRITICAL-NON-OVERRIDABLE (seeded CRITICAL/H1-H2 -> 0 plans via ANY pass)
# ===============================================================================


def _crit5_dispatch(authors_map):
    """A dispatch seam over a fixed authors map, recording per-domain calls (the MF-3 count spy)."""
    calls = []

    def dispatch(domain, prompt, summary):
        calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        return authors_map[domain]

    dispatch.calls = calls
    return dispatch


def test_critical_non_overridable_never_surfaced_via_revise(tmp_path):
    # AC-5 / Risk R3 (the seeded CRITICAL/H1-H2 non-overridable probe): a held inner finding (the
    # cross-domain-conflict hold on SUPPLEMENTS) routed to a CRITICAL liaison WITH an override
    # record present (the override-path-built-for-a-non-overridable-finding shape). The loop is
    # driven INTO a REVISE pass (a SEPARATE quality-defective workout domain is the revise TARGET),
    # so the loop's `revise_domains` selection is genuinely exercised — and the held supplements
    # domain is NEVER among the re-dispatched. Two assertions, both required:
    #   (C-2) RECORD-SUPPRESSION (per-domain, NOT a loop halt): the held domain's
    #         `results[domain]["recorded"] is False` and `store.read("plan::<domain>") == []`.
    #   (MF-3) RE-AUTHOR-TARGETING negative (the laundering path is real — a held domain still
    #         carries a `section`, so the quality gate CAN emit REVISE targeting it): the held
    #         domain's per-domain RE-DISPATCH count == 0 (the `dispatch` seam NOT re-issued for the
    #         non-overridably-held domain), distinct from `recorded == False`. This catches a loop
    #         variant that re-dispatched ALL held (recorded-False) domains (the laundering mutant).
    deid_client = _FixedDeidClient(_deid_summary())
    store_read = _seed_store(tmp_path)

    # the inner CRITICAL hold on supplements (with an override record present — the laundering shape)
    liaison = _liaison("CRITICAL", override=_override_record("CRITICAL"))

    # supplements declares the conflict (CRITICAL-held throughout); peptides is the clean compound;
    # workout is the SEPARATE quality-defective revise TARGET (empty pass-1 -> filled re-dispatch).
    supp = _recon(_author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
                  conflicts=_SUPP_CONFLICT)
    pep = _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist")

    calls = []

    def dispatch(domain, prompt, summary):
        calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        if domain == "supplements":
            return supp
        if domain == "peptides":
            return pep
        # workout: empty pass-1 (the quality defect), filled on the re-dispatch
        n = len([c for c in calls if c["domain"] == "workout"])
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    # the gate REVISEs (targeting ONLY workout) until workout is filled, then ACCEPTs — the held
    # supplements domain is NEVER a revise target. The loop is genuinely driven through a re-author
    # pass, so the `revise_domains` selection is exercised (not short-circuited by an immediate ACCEPT).
    quality_wrapper = _recording_quality(_clean_scores())
    safety_wrapper = _recording_safety(_no_findings_dispatch())

    def gate(assembled_plan):
        q = quality_wrapper(assembled_plan)
        s = safety_wrapper(assembled_plan)
        # workout's empty section drives the quality structural REVISE on pass-1
        accept = q["verdict"] == ACCEPT
        disposition = {"accept": accept, "safety_passed": s["passed"]}
        if not accept:
            disposition["revise_domains"] = ["workout"]  # the held supplements is NEVER targeted
        return disposition

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "supplements", "peptides"),
        gate_dispatch=gate, adjudicator=liaison,
    )

    # the loop WAS driven through a revise pass (workout re-dispatched) — the selection ran
    workout_dispatches = [c for c in calls if c["domain"] == "workout"]
    assert len(workout_dispatches) == 2, "the loop did not enter a revise pass (selection not exercised)"
    # (C-2) RECORD-SUPPRESSION: the held domain records nothing (per-domain, NOT a loop halt)
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []
    # the inner gate's non-overridable disposition held it
    assert out["results"]["supplements"]["reason"] is not None
    # (MF-3) RE-AUTHOR-TARGETING negative: the held domain was re-dispatched 0 times (one initial
    # call only) — distinct from `recorded == False`. A loop that re-dispatched all held domains
    # would re-issue supplements here -> RED (the laundering mutant is caught by THIS assertion).
    supp_dispatches = [c for c in calls if c["domain"] == "supplements"]
    assert len(supp_dispatches) == 1, f"the held domain was re-dispatched {len(supp_dispatches) - 1} times (laundering)"


def test_critical_non_overridable_red_against_a_relaunder_mutant(tmp_path):
    # AC-5 RED-against-a-mutant: demonstrate the probe goes RED against a loop VARIANT that treats
    # the inner non-overridable hold as a quality-REVISE target (re-dispatches the held domain). The
    # mutant is modeled here as a composite gate that NAMES the held domain in `revise_domains` AND
    # never accepts — the loop then re-dispatches the held supplements domain (its re-dispatch count
    # > 1), but the inner gate STILL holds it (re-fires every re-run) so it STILL records nothing.
    # This proves: the per-domain re-dispatch-count assertion (MF-3) is what catches the laundering
    # attempt, NOT `recorded == False` (which holds even for the mutant — the C-2/MF-3 distinction).
    authors = _conflict_authors(supp_conflicts=_SUPP_CONFLICT)
    dispatch = _crit5_dispatch(authors)
    deid_client = _FixedDeidClient(_deid_summary())
    store_read = _seed_store(tmp_path)
    liaison = _liaison("CRITICAL", override=_override_record("CRITICAL"))

    # the MUTANT gate: it tries to launder the held domain by naming it a revise target every pass.
    def relaundering_gate(assembled_plan):
        return {"accept": False, "safety_passed": True, "revise_domains": ["supplements"]}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        gate_dispatch=relaundering_gate, adjudicator=liaison,
    )

    # the loop re-dispatched the held domain (the mutant's laundering attempt) — MORE than once
    supp_dispatches = [c for c in dispatch.calls if c["domain"] == "supplements"]
    assert len(supp_dispatches) > 1, "the mutant did not re-dispatch the held domain (probe has no teeth)"
    # the MF-3 count assertion (== 1) WOULD go RED on this mutant -> the probe catches laundering.
    # CRUCIALLY: even the mutant NEVER surfaces the held domain — the inner gate re-fires every pass.
    assert out["results"] == {} or out["results"].get("supplements", {}).get("recorded") is False
    assert store.read("plan::supplements", root=tmp_path) == [], "the loop LAUNDERED a non-overridable hold"


def test_high_override_clearable_domain_is_redispatched_and_records(tmp_path):
    # AC-5 POSITIVE CONTROL (non-tautological): a HIGH/MEDIUM override-CLEARABLE held domain DOES
    # get re-dispatched on a quality REVISE AND records — proving the suppression above is specific
    # to the non-overridable hold, not a blanket "never re-dispatch a held domain". The seed: a
    # conflict-held supplement whose section is quality-defective (empty) the loop re-authors;
    # a content-valid HIGH override clears the inner conflict hold so the re-authored plan records.
    deid_client = _FixedDeidClient(_deid_summary())
    store_read = _seed_store(tmp_path)

    # pass-1 supplements declares a conflict (held) AND has an empty/defective section; the
    # re-dispatch returns a filled supplements envelope (still declaring the conflict, but the
    # HIGH override clears the conflict so it records).
    def _supp_conflict_envelope(recs):
        return _recon(
            {"specialist": "supplement-specialist", "recommendations": recs},
            conflicts=_SUPP_CONFLICT,
        )

    pep = _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist")

    calls = []

    def dispatch(domain, prompt, summary):
        calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        if domain == "peptides":
            return pep
        n = len([c for c in calls if c["domain"] == "supplements"])
        # re-dispatch (2nd call) returns a FILLED supplements section; pass-1 was empty.
        recs = [_supplement_rec("Fish oil", "2 g")] if n >= 2 else []
        return _supp_conflict_envelope(recs)

    quality_wrapper = _recording_quality(_clean_scores())
    safety_wrapper = _recording_safety(_no_findings_dispatch())

    def gate(assembled_plan):
        q = quality_wrapper(assembled_plan)
        s = safety_wrapper(assembled_plan)
        accept = q["verdict"] == ACCEPT
        disposition = {"accept": accept, "safety_passed": s["passed"]}
        if not accept:
            disposition["revise_domains"] = ["supplements"]
        return disposition

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        gate_dispatch=gate,
        adjudicator=_liaison("HIGH", override=_override_record("HIGH")),  # content-valid override
    )

    # the override-clearable domain WAS re-dispatched (the positive control — re-dispatch happened)
    supp_dispatches = [c for c in calls if c["domain"] == "supplements"]
    assert len(supp_dispatches) >= 2, "the override-clearable held domain was not re-dispatched"
    # and it RECORDS (the HIGH override cleared the inner conflict hold)
    assert out["results"]["supplements"]["recorded"] is True
    assert store.read("plan::supplements", root=tmp_path) != []


# ===============================================================================
# Cycle 6: the final runtime-stage-order E2E (the Wave-4 checkpoint)
# ===============================================================================

# The synthetic identity token (no real PII — mirrors the T0-SCANSCOPE hook fixture). The report
# header emits `Patient <initials>`; `reinsert_out` re-inserts the FULL name when the target is
# confirmable-gitignored, so the gitignored artifact carries the full name and the store/tracked
# set never does.
E2E_SYNTH_NAME = "Janet Q Testperson"
E2E_SYNTH_INITIALS = "JQT"


def _e2e_synth_profile(tmp_path):
    """Write a synthetic gitignored operator profile and return its path tuple (reinsert_out seam)."""
    prof = tmp_path / "operator-profile.md"
    prof.write_text(f"# Operator Profile — {E2E_SYNTH_NAME}\n", encoding="utf-8")
    return (prof,)


def _e2e_gitignored_repo(tmp_path):
    """A git repo whose `vault/artifacts/generated/` out-dir is gitignored; return (repo, out_dir).

    `reinsert_out` re-inserts the name only when `git check-ignore <target>` exits 0, so the
    out-dir must be a real gitignored path inside a git repo for the name to land.
    """
    repo = tmp_path / "repo"
    out = repo / "vault" / "artifacts" / "generated"
    out.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
    return repo, out


def test_full_runtime_stage_order_e2e(tmp_path):
    # The full runtime-stage-order path on synthetic fixtures + mock clients:
    #   de-id IN (`deid_in`) -> orchestrate/assemble (`run_orchestrated` -> `run_generation`)
    #   -> {quality judge || safety review} (both wired into `gate_dispatch`) -> revise loop
    #   -> maintained render + de-id OUT (`maintained.reemit_maintained`, render-then-`reinsert_out`).
    # STORE-MEDIATED (SF-2): `reemit_maintained` takes NO `plan` arg — it READS the plan from the
    # STORE (`store.read_all(root)`) where the orchestrator's inner-engine `record_plan` wrote
    # `plan::<domain>`. So: `run_orchestrated(...)` records `plan::<domain>` -> the E2E calls
    # `reemit_maintained(root, _profile_paths, _out_dir, _repo_root)`, which reads those rows and
    # renders. 0 live spend (all clients mock); 0 real PII (synthetic identity token only).
    from scripts.generate import maintained
    from scripts.plan import deid_in as deid_in_mod

    store_root = tmp_path / "store"
    store_read = _seed_store(store_root)  # the pre-bound operator-state reader (real root)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # both Wave-3 gate callables wired LIVE into one composed gate_dispatch (clean -> ACCEPT/PASS)
    gate = _clean_composing_gate()

    # --- de-id IN -> orchestrate/assemble -> {judge || safety} -> revise loop (records the plan) ---
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, store_root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
    )

    # the loop surfaced a plan and the inner engine recorded `plan::<domain>` to the store
    assert "results" in out and out.get("reason") is None
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert recorded, "the E2E surfaced no recorded plan"
    assert store.read("plan::workout", root=store_root) != []

    # --- maintained render + de-id OUT: the DOWNSTREAM store-reading caller (render-then-fill) ---
    repo, out_dir = _e2e_gitignored_repo(tmp_path)
    artifact = maintained.reemit_maintained(
        root=store_root,
        _profile_paths=_e2e_synth_profile(tmp_path),
        _out_dir=out_dir,
        _today=datetime.date.fromisoformat(PLAN_DATE),
        _repo_root=repo,
    )

    # the maintained artifact lands under the gitignored `_out_dir` (the CORRECT location)
    resolved = os.path.realpath(artifact)
    assert resolved.startswith(os.path.realpath(out_dir) + os.sep), "artifact wrote outside the gitignored out-dir"
    rendered = Path(artifact).read_text(encoding="utf-8")

    # CROWN-JEWEL POSITIVE CONTROL (SF-3): the SYNTHETIC name token IS present in the gitignored
    # artifact — proving `reinsert_out` actually re-inserted the name (the `Patient <initials>` ->
    # `Patient <SYNTHETIC_NAME>` substitution ran). Without this, the 0-PII negative below could
    # pass VACUOUSLY when the render wrote no name.
    assert E2E_SYNTH_NAME in rendered, "the synthetic name did not land in the gitignored artifact (reinsert_out mis-wired)"
    assert f"Patient {E2E_SYNTH_INITIALS} ·" not in rendered, "the initials placeholder was not filled"

    # CROWN-JEWEL NEGATIVE (0 real PII): the SYNTHETIC name token is ABSENT from the persisted
    # store + the tracked set (only the gitignored artifact carries it — the store/tracked stay
    # de-identified). The store-read summary carries no identity token.
    persisted = json.dumps(store.read_all(store_root), default=str)
    assert E2E_SYNTH_NAME not in persisted, "the synthetic name leaked into the persisted store"
    assert E2E_SYNTH_INITIALS not in persisted, "an identity token leaked into the persisted store"

    # confirm all stages exist at Wave 4 (all merged: deid_in, run_generation, the two gates,
    # maintained, reinsert_out) — the E2E exercised each through the orchestrator + the caller.
    assert hasattr(deid_in_mod, "deid_in")
    assert callable(quality_judge) and callable(review_plan)
    assert hasattr(maintained, "reemit_maintained")


def test_e2e_blocked_plan_does_not_reach_the_rendered_store(tmp_path):
    # E2E placement (assert correct location, negative against the wrong one): a SAFETY_BLOCKED run
    # records 0 plans, so a downstream `reemit_maintained` over that store renders NO plan content —
    # the blocked plan does NOT land in the rendered store. The fail-closed surface boundary: what
    # `reemit_maintained` reads (`root`) carries 0 plan rows on a blocked run.
    from scripts.generate import maintained

    store_root = tmp_path / "store"
    store_read = _seed_store(store_root)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # a safety-blocking composed gate (passed: False) — the loop halts SAFETY_BLOCKED, 0 plans
    def blocking_gate(assembled_plan):
        return {"accept": True, "safety_passed": False}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, store_root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=blocking_gate,
    )

    assert out["reason"] == SAFETY_BLOCKED
    # 0 plan rows reached the rendered store (the inner engine's writes went to the discarded scratch)
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=store_root) == []
    # a downstream render over that store carries no plan content (the blocked plan is not surfaced)
    repo, out_dir = _e2e_gitignored_repo(tmp_path)
    artifact = maintained.reemit_maintained(
        root=store_root, _profile_paths=_e2e_synth_profile(tmp_path), _out_dir=out_dir,
        _today=datetime.date.fromisoformat(PLAN_DATE), _repo_root=repo,
    )
    rendered = Path(artifact).read_text(encoding="utf-8")
    # the workout exercise the sustaining author would have surfaced is NOT in the render
    assert "Goblet squat" not in rendered, "a SAFETY_BLOCKED plan leaked into the rendered store"


# ===============================================================================
# Cycle 7: the in-loop fail-closed boundary (SEC-01 promote OSError, BUG-01 unknown domain)
# ===============================================================================


def test_promote_oserror_fails_closed_no_partial_store(tmp_path, monkeypatch):
    # SEC-01: a mid-promote write OSError (the 2nd `plan::` append of a clean ACCEPT+PASS
    # multi-domain run) must FAIL CLOSED — `run_orchestrated` returns honest no-plan
    # (`PROMOTE_FAILED`), NOT an escaping OSError, and the real store is NOT left with a
    # partial plan set (0 plan rows). On the current code the OSError escapes the try (it
    # catches only `DispatchCapExceeded`) and any first row already appended is a partial root.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    gate = _clean_composing_gate()

    real_append = store.append
    appended = {"n": 0}

    def failing_append(item, reading, root=store.DEFAULT_ROOT):
        # only the promote into the REAL root is failure-injected (the scratch writes the
        # inner engine does are untouched); fail on the 2nd promote-append.
        if str(root) == str(tmp_path) and (item.startswith("plan::") or item.startswith("dvq::")):
            appended["n"] += 1
            if appended["n"] == 2:
                raise OSError("disk full mid-promote")
        return real_append(item, reading, root=root)

    monkeypatch.setattr(store, "append", failing_append)

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
    )

    # the run FAILED CLOSED to honest no-plan, NOT an escaping OSError
    assert out["reason"] == PROMOTE_FAILED, f"promote OSError did not fail closed: {out.get('reason')}"
    assert out["results"] == {}, "a promote-failed run surfaced a plan"
    # the real store is NOT left with a partial plan set (0 plan/dvq rows promoted)
    for item in store.items(root=tmp_path):
        assert not (item.startswith("plan::") or item.startswith("dvq::")), (
            f"a partial plan set was left in the real store: {item}"
        )


def test_unknown_revise_domain_fails_closed(tmp_path):
    # BUG-01/API-02: a gate disposition naming an UNKNOWN `revise_domains` target must FAIL
    # CLOSED — `run_orchestrated` returns honest no-plan (`SAFETY_BLOCKED`, treating an unknown
    # revise target as a malformed disposition), NOT an escaping KeyError out of
    # `_ROLE_OF_DOMAIN[domain]`. On the current code the unguarded `_ROLE_OF_DOMAIN[domain]`
    # raises a KeyError that escapes the try (it catches only `DispatchCapExceeded`).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # a gate that REVISEs (never accepts) naming a domain not in `_ROLE_OF_DOMAIN` / the run set
    def unknown_revise_gate(assembled_plan):
        return {"accept": False, "safety_passed": True, "revise_domains": ("not-a-domain",)}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=unknown_revise_gate,
    )

    assert out["reason"] == SAFETY_BLOCKED, f"unknown revise domain did not fail closed: {out.get('reason')}"
    assert out["results"] == {}, "an unknown-revise-domain run surfaced a plan"
    assert store.read("plan::workout", root=tmp_path) == []


def test_cap_trips_mid_revise_loop(tmp_path):
    # BUG-02: a NON-converging revise loop with a `dispatch_cap` sized to trip MID-revise (enough
    # for the initial specialist + 1 gate but NOT a 2nd revise re-dispatch) halts
    # DISPATCH_CAP_EXCEEDED, 0 plans. The cap×revise-loop interaction (production behavior is
    # correct — this pins it). cap=2: initial workout dispatch (count=1), gate dispatch (count=2),
    # then the revise re-dispatch's charge (count=3 > 2) trips before the over-budget dispatch.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    gate = _composing_gate(
        _recording_quality(_clean_scores()),  # the empty section REVISEs every pass
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate, dispatch_cap=2,
    )

    assert out["reason"] == DISPATCH_CAP_EXCEEDED, f"cap did not trip mid-revise: {out.get('reason')}"
    assert out["dispatch_count"] == 3, f"dispatch_count != cap+1 (the over-budget charge): {out['dispatch_count']}"
    assert out["results"] == {}, "a cap-tripped run surfaced a plan"
    assert store.read("plan::workout", root=tmp_path) == []


def test_converged_revise_surfaces_aggregate_dispatch_count(tmp_path):
    # TEST-01 (re-scoped): `dispatch_count` is asserted on the LOOP converged-revise SUCCESS path
    # (where the count aggregates specialist + gate + revise dispatches), not only the legacy
    # non-loop path. One revise pass that converges: initial workout dispatch (1) + gate (1) +
    # revise re-dispatch (1) + gate (1) = 4 aggregate dispatches.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch({"workout": _empty_workout_envelope()})

    def reissuing_dispatch(domain, prompt, summary):
        dispatch.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        n = len([c for c in dispatch.calls if c["domain"] == domain])
        return _filled_workout_envelope() if n >= 2 else _empty_workout_envelope()

    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, reissuing_dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate,
    )

    # converged + recorded, and dispatch_count is the loop aggregate (specialist + gate + revise)
    assert out["results"]["workout"]["recorded"] is True
    assert "dispatch_count" in out, "the converged-revise success path did not surface dispatch_count"
    # initial specialist(1) + initial gate(1) + revise re-dispatch(1) + re-run gate(1) = 4
    assert out["dispatch_count"] == 4, f"converged-revise aggregate dispatch_count != 4: {out['dispatch_count']}"


def test_deid_halt_short_circuits_before_loop(tmp_path):
    # TEST-02: a `{deidentified: False}` sentinel de-id client short-circuits BEFORE the loop —
    # 0 dispatches (the specialist seam never fires) AND the gate never fires (gate.calls empty),
    # even with a real composing gate injected. The de-id halt precedes any dispatch / gate.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient({"deidentified": False, "reason": "deid-call-failed"})
    dispatch = _RecordingDispatch(_sustaining_authors())
    gate = _clean_composing_gate()

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
    )

    assert out["deidentified"] is False
    assert out["dispatch_count"] == 0
    assert dispatch.calls == [], "a specialist dispatched past the de-id halt"
    assert gate.calls == [], "the gate fired past the de-id halt"
