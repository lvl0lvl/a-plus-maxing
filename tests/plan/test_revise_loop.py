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
from scripts.plan.orchestrate import ENERGY_BOUNCE_UNRESOLVED
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
    _bpmh_store,
    _compound_authors,
    _conflict_authors,
    _liaison,
    _nutrition,
    _recon,
    _selective_liaison,
)
from tests.plan.test_adjudicate import _envelope, _override_record
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
    """A RAW-VERDICT producer that runs BOTH gate callables and returns `{judge, review}`.

    The ADR-0028-T1 GATE producer (OQ-2): ONE callable drives the two gates with DIFFERENT native
    signatures and returns their RAW verdicts — it composes NO disposition (the driver's
    `compose_disposition` maps `judge.verdict`->`accept`, `review.passed`->`safety_passed`, and
    DERIVES `revise_domains` from the quality verdict). The `revise_domains=` keyword is retained for
    call-site compatibility but is now INERT: the real `_revise_domains` derivation over the
    assembled plan localizes the target (an empty in-scope domain localizes to itself; a
    dimension-level miss fans to all run-set domains), reproducing what the hand-shaped override
    named. Records each producer dispatch for the EXACT-count pin.
    """
    calls = []

    def producer(assembled_plan):
        calls.append(assembled_plan)
        return {"judge": quality_wrapper(assembled_plan), "review": safety_wrapper(assembled_plan)}

    producer.calls = calls
    return producer


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

    # ADR-0028-T1: the producer returns RAW `{judge, review}` verdicts; the driver composes via
    # `compose_disposition` then applies `safety_passed is True`. The fail-closed surface now spans
    # the raw-VERDICT family — an ACCEPT judge with a review that does not boolean-True-`passed` (an
    # explicit-False / None / absent-key / non-bool / non-dict / None review), plus a whole-verdict
    # malformed shape (non-dict / None) and a raised producer — each composes to a not-`True`
    # `safety_passed` (or throws) -> SAFETY_BLOCKED. A loop reading only `passed is False` would fall
    # through the ambiguous cases and SURFACE -> RED.
    _accept = {"verdict": ACCEPT, "dimensions": {}, "deductions": []}
    ambiguous_gates = (
        lambda p: {"judge": _accept, "review": {"passed": False, "findings": []}},  # explicit False
        lambda p: {"judge": _accept, "review": {"passed": None, "findings": []}},   # None
        lambda p: {"judge": _accept, "review": {"findings": []}},                   # absent key
        lambda p: {"judge": _accept, "review": {"passed": "ok", "findings": []}},   # non-bool
        lambda p: {"judge": _accept, "review": {"passed": 1, "findings": []}},      # truthy non-bool
        lambda p: {"judge": _accept, "review": ["not", "a", "dict"]},               # non-dict review
        lambda p: ["not", "a", "dict"],                                             # non-dict verdicts
        _raising_gate,                                                              # the producer raised
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

    # a producer that runs the quality judge but composes NO safety tier (the review is absent —
    # the raw verdicts carry an ACCEPT judge but no `review`, so `compose_disposition` fail-closes
    # `safety_passed` to not-True). The no-safety-tier case under the raw-verdict wire.
    def no_safety_tier_gate(assembled_plan):
        return {"judge": {"verdict": ACCEPT, "dimensions": {}, "deductions": []}}  # no review

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
        # the RAW-VERDICT producer: the standing-block review's `passed: False` composes to
        # `safety_passed=False` -> terminal SAFETY_BLOCKED (the driver never reaches the revise leg).
        return {"judge": quality_wrapper(assembled_plan), "review": safety_wrapper(assembled_plan)}

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
        # the RAW-VERDICT producer: a clean ACCEPT judge but a review that does NOT pass (a finding)
        # -> `compose_disposition` yields `accept=True, safety_passed=False` -> terminal
        # SAFETY_BLOCKED before any re-author (safety precedes the quality REVISE branch in `drive`).
        verdict = quality_judge(assembled_plan, _FixedJudgeClient(_clean_scores()))
        return {"judge": verdict, "review": {"passed": False, "findings": [
            {"id": "cumulative-stimulant-load", "concern": "exceeds the safe ceiling",
             "severity": "high"}], "lenses": ("medical-safety-reviewer", "health-edge-case-reviewer")}}

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
        # the RAW-VERDICT producer: workout's empty section drives the real quality structural
        # REVISE, and `compose_disposition._revise_domains` LOCALIZES the target to the empty
        # workout domain ONLY — the filled-but-held supplements domain is never an empty-domain
        # structural target, so the real derivation reproduces "revise workout, never supplements".
        return {"judge": quality_wrapper(assembled_plan), "review": safety_wrapper(assembled_plan)}

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

    # the MUTANT compose: it tries to launder the held domain by naming it a revise target every
    # pass (ADR-0028-T1: the disposition is composed in `drive` via `compose`, so the mutant lives at
    # the compose seam, not the producer). The producer returns inert raw verdicts; the mutant
    # `compose` ignores them and names the held supplements domain a revise target.
    def relaundering_producer(assembled_plan):
        return {"judge": {"verdict": REVISE, "dimensions": {}, "deductions": []}, "review": {}}

    def relaundering_compose(verdicts, assembled_plan):
        return {"accept": False, "safety_passed": True, "revise_domains": ["supplements"]}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        gate_dispatch=relaundering_producer, compose=relaundering_compose, adjudicator=liaison,
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
        # the RAW-VERDICT producer: supplements' empty pass-1 section drives the real quality
        # structural REVISE, and `_revise_domains` localizes the target to the empty supplements
        # domain (peptides is filled) — reproducing the "revise supplements" target.
        return {"judge": quality_wrapper(assembled_plan), "review": safety_wrapper(assembled_plan)}

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

    # a safety-blocking producer: an ACCEPT judge + a not-passing review (a finding) -> the driver
    # composes `safety_passed=False` -> the loop halts SAFETY_BLOCKED, 0 plans.
    def blocking_gate(assembled_plan):
        return {"judge": {"verdict": ACCEPT, "dimensions": {}, "deductions": []},
                "review": {"passed": False, "findings": [{"id": "x", "concern": "y",
                           "severity": "high"}], "lenses": ("medical-safety-reviewer",
                           "health-edge-case-reviewer")}}

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

    # a mutant `compose` that REVISEs (never accepts) naming a domain not in `_ROLE_OF_DOMAIN` / the
    # run set (ADR-0028-T1: the out-of-run-set disposition can only arise at the compose seam — the
    # real `compose_disposition` never escapes the run-set, so the mutant is injected there).
    def unknown_revise_producer(assembled_plan):
        return {"judge": {"verdict": REVISE, "dimensions": {}, "deductions": []}, "review": {}}

    def unknown_revise_compose(verdicts, assembled_plan):
        return {"accept": False, "safety_passed": True, "revise_domains": ("not-a-domain",)}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",),
        gate_dispatch=unknown_revise_producer, compose=unknown_revise_compose,
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


# ===============================================================================
# ADR-0028-T2: the REAUTHOR / ADJUDICATOR throw / replay-memo mechanism
# ===============================================================================
#
# REAUTHOR (the energy-bounce re-author) and ADJUDICATOR (the held-finding medical-liaison) fire
# DEEP INSIDE the byte-frozen `orchestrate.generate_plans`, NOT in `drive`'s frame, so they cannot
# become direct yields. They invert by THROW / REPLAY-MEMOIZATION: the memo-cache callable the
# driver forwards into `run_generation` raises a `BaseException`-subclass sentinel on a cache MISS;
# the sentinel unwinds THROUGH the frozen engine (its only catch is the narrow `except ModelCallError`)
# up to `drive`, which catches it, yields the typed `REAUTHOR` / `ADJUDICATOR` request, caches the
# `.send()`'d envelope, and RE-DRIVES the pass over a FRESH scratch store. The replay round hits the
# cache and the engine proceeds unchanged. Charge-on-cache-miss-only (the existing `_charging` wrap).
#
# All fixture-driven, 0 live spend.


# --- Cycle 1: the BaseException sentinel + non-swallowable proof + no-fork release-grep ---


def test_replay_sentinel_is_baseexception_not_exception():
    # AC-8 (sentinel non-swallowable, the type contract): the replay sentinel is a `BaseException`
    # subclass and NOT an `Exception` subclass — so neither the engine's `except ModelCallError`
    # nor `drive`'s GATE-yield fail-closed wrap (`except Exception: disposition = None`) can absorb
    # it. A sentinel re-typed to `Exception` would be swallowed -> this test goes RED.
    from scripts.plan.plan_driver import _ReplayNeeded

    assert issubclass(_ReplayNeeded, BaseException)
    assert not issubclass(_ReplayNeeded, Exception)


def test_replay_sentinel_unwinds_through_except_exception():
    # AC-8 (the live proof site): a `try/except Exception` around a sentinel-raising call (the exact
    # shape of `drive`'s GATE-yield fail-closed wrap, `except DispatchCapExceeded: raise` then
    # `except Exception: disposition = None`) does NOT catch the sentinel — it unwinds to a
    # `BaseException` handler. A loop reading only `except Exception` would turn the sentinel into a
    # SAFETY_BLOCKED swallow; the sentinel must propagate to `drive`'s replay handler.
    from scripts.plan.plan_driver import _ReplayNeeded, REAUTHOR

    def raises_sentinel():
        raise _ReplayNeeded(REAUTHOR, ("reauthor", "workout", 450), ("workout", {"x": 1}))

    swallowed = False
    propagated = False
    try:
        try:
            raises_sentinel()
        except Exception:  # noqa: BLE001 — the shape of `drive`'s GATE-yield fail-closed wrap
            swallowed = True
    except _ReplayNeeded:
        propagated = True

    assert swallowed is False, "the `except Exception` swallowed the replay sentinel (swallowable)"
    assert propagated is True, "the replay sentinel did not unwind to a BaseException handler"


def test_replay_sentinel_carries_kind_and_key():
    # the sentinel carries the dispatch CLASS (REAUTHOR / ADJUDICATOR) so `drive`'s catch knows which
    # typed request to yield, the memo KEY it was raised for so `drive` knows which cache slot the
    # `.send()`'d envelope fills, and the de-identified PAYLOAD the typed request carries. Named
    # attributes, not positional tuples passed with no doc.
    from scripts.plan.plan_driver import _ReplayNeeded, ADJUDICATOR

    key = ("adjudicator", "supplements", "additive-ae", "additive-ae:class:bleeding-risk")
    payload = {"finding_id": "additive-ae:class:bleeding-risk", "held_domain": "supplements"}
    sentinel = _ReplayNeeded(ADJUDICATOR, key, payload)

    assert sentinel.kind == ADJUDICATOR
    assert sentinel.key == key
    assert sentinel.payload == payload


def test_no_fork_adjudication_release_not_rederived_in_consumer_or_driver():
    # NO-FORK release-grep (the crown-jewel consumer axis): the adjudication RELEASE — the
    # `outcome == "cleared"` expression AND the CRITICAL / H1-H2 non-overridable check — stays in
    # `orchestrate.adjudicate`; the consumer (`plan_orchestrator.py`) and the driver
    # (`plan_driver.py`) re-derive NEITHER. The adjudicator memo-callable returns ONLY the raw
    # liaison envelope. A re-derivation in either file is the forked-safety-loop failure vector
    # ADR-0028 rejects -> RED. Targets EXECUTABLE control flow: comments + docstrings are stripped
    # before counting (a token surviving in prose is not a fork).
    import ast

    for path in ("scripts/plan/plan_orchestrator.py", "scripts/plan/plan_driver.py"):
        source = Path(path).read_text(encoding="utf-8")
        tree = ast.parse(source)
        # collect every string-literal (docstrings live as Constant nodes) line span, then read the
        # source lines OUTSIDE those spans + with `#`-comments stripped — the executable surface.
        docstring_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if hasattr(node, "end_lineno"):
                    docstring_lines.update(range(node.lineno, node.end_lineno + 1))
        executable = []
        for i, line in enumerate(source.splitlines(), start=1):
            if i in docstring_lines:
                continue
            code = line.split("#", 1)[0]
            executable.append(code)
        executable_src = "\n".join(executable)
        assert 'outcome == "cleared"' not in executable_src, (
            f"{path} re-derives the adjudication release (`outcome == \"cleared\"`) — a forked "
            f"safety loop; the release stays in orchestrate.adjudicate"
        )
        assert "outcome == 'cleared'" not in executable_src, (
            f"{path} re-derives the adjudication release — a forked safety loop"
        )
        # the CRITICAL / non-overridable re-derivation guard (the H1-H2 non-overridable check)
        assert "non_overridable" not in executable_src, (
            f"{path} re-derives the CRITICAL / H1-H2 non-overridable check — a forked safety loop; "
            f"it stays in orchestrate.adjudicate"
        )


# --- Cycle 2: REAUTHOR throw -> yield -> cache -> replay + REAUTHOR fail-closed hold ---


def _bounce_authors(workout_cost, *, ceiling=450):
    """A workout over the sustainable ceiling + a nutrition budget that does NOT sustain.

    `energy_budget.sustains is False` with a workout `energy_cost_kcal > ceiling` forces a REAL
    energy bounce ([orchestrate.py:546-565]) — the engine calls `reauthor("workout", {ceiling})`.
    """
    return {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=workout_cost),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": ceiling},
        ),
    }


def _kind_recording_gate(quality_wrapper, safety_wrapper, *, kinds_seen):
    """A clean composing gate that also records the request-kind SEQUENCE the driver yielded.

    The driver yields AUTHOR / REAUTHOR / ADJUDICATOR / GATE typed requests; only the GATE reaches
    a producer, but a REAUTHOR/ADJUDICATOR fired BETWEEN the AUTHOR and the GATE means by the time
    the producer is called the inner engine has already run (and replayed), so recording the
    producer-call moment alongside the cache state is the in-band check. AC-1 asserts the yielded
    `kind` sequence contains a REAUTHOR between the AUTHOR and the GATE — captured by the
    consumer-side kind spy (`_kind_spy_run`), not here. This gate is just the clean PASS.
    """
    def producer(assembled_plan):
        kinds_seen.append("GATE")
        return {"judge": quality_wrapper(assembled_plan), "review": safety_wrapper(assembled_plan)}

    producer.calls = kinds_seen
    return producer


def _kind_spy_run(monkeypatch, **run_kwargs):
    """Run `run_orchestrated`, recording the SEQUENCE of `Request.kind` values the driver yielded.

    Wraps `plan_driver.drive` so each yielded `Request.kind` is appended to a list — the in-band
    proof that a REAUTHOR was yielded BETWEEN the AUTHOR and the GATE (the throw/replay fired). 0
    live spend (the run is fully fixture-driven).
    """
    from scripts.plan import plan_driver

    kinds = []
    real_drive = plan_driver.drive

    def spying_drive(*args, **kwargs):
        gen = real_drive(*args, **kwargs)
        sent = None
        try:
            while True:
                request = gen.send(sent)
                kinds.append(request.kind)
                sent = yield request
        except StopIteration as done:
            return done.value

    monkeypatch.setattr(plan_driver, "drive", spying_drive)
    out = run_orchestrated(**run_kwargs)
    return out, kinds


def test_reauthor_throws_yields_caches_replays(tmp_path, monkeypatch):
    # AC-1 (REAUTHOR throw -> yield -> cache -> replay): a real energy bounce
    # (`energy_budget.sustains is False` + over-ceiling workout) -> the memo `reauthor` callable
    # raises the sentinel on the cache-miss pass -> `drive` yields a REAUTHOR request -> the consumer
    # `.send()`s a re-author envelope -> `drive` caches it (keyed `reauthor:(domain, constraint)`)
    # and re-drives over a FRESH scratch store -> the replay hits the cache and the pass completes.
    # Assert the yielded `kind` sequence contains a REAUTHOR BETWEEN the AUTHOR and the GATE.
    from scripts.plan import plan_driver

    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_bounce_authors(workout_cost=900, ceiling=450))
    gate = _clean_composing_gate()

    reauthor_calls = []

    def reauthor(domain, constraint):
        reauthor_calls.append((domain, constraint))
        # the re-dispatched personal-trainer returns a reduced session UNDER the ceiling (fuelable)
        return _recon(_author(_workout_rec("Light goblet squat", 2)), energy_cost_kcal=400)

    out, kinds = _kind_spy_run(
        monkeypatch,
        raw_intake=_raw_intake(), deid_client=deid_client, dispatch=dispatch,
        store_read=store_read, root=tmp_path, plan_date=PLAN_DATE,
        domains=("workout", "nutrition"), gate_dispatch=gate, reauthor=reauthor,
    )

    # the energy bounce fired and the re-author hook was dispatched EXACTLY ONCE (the cache miss)
    assert reauthor_calls == [("workout", {"sustainable_training_kcal": 450})], reauthor_calls
    # the yielded kind sequence carries a REAUTHOR BETWEEN the first AUTHOR and the first GATE
    assert plan_driver.REAUTHOR in kinds, f"no REAUTHOR was yielded: {kinds}"
    first_author = kinds.index(plan_driver.AUTHOR)
    first_gate = kinds.index(plan_driver.GATE)
    first_reauthor = kinds.index(plan_driver.REAUTHOR)
    assert first_author < first_reauthor < first_gate, f"REAUTHOR not between AUTHOR and GATE: {kinds}"
    # the replay completed and the FUELABLE re-authored workout surfaced (the cache hit on replay)
    assert out["results"]["workout"]["recorded"] is True
    recorded = store.read("plan::workout", root=tmp_path)
    assert recorded != [], "the replay did not surface the re-authored workout"
    assert recorded[-1]["value"]["exercises"][0]["name"] == "Light goblet squat"


def test_reauthor_fail_closed_holds_workout_others_may_surface(tmp_path):
    # AC-5 (REAUTHOR fail-closed shape, per-domain hold — NOT terminal): a malformed re-author
    # envelope (over-ceiling cost) -> the WORKOUT domain stays HELD (`ENERGY_BOUNCE_UNRESOLVED`,
    # records nothing) while OTHER domains MAY surface. Threshold is "workout not recorded", NOT
    # "0 plans". The engine's existing hold branch decides the workout is un-fuelable; the driver
    # only replays with the (malformed) envelope cached.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_bounce_authors(workout_cost=900, ceiling=450))
    gate = _clean_composing_gate()

    def reauthor(domain, constraint):
        # STILL over the ceiling -> the engine holds workout `ENERGY_BOUNCE_UNRESOLVED`
        return _recon(_author(_workout_rec("Still heavy squat", 5)), energy_cost_kcal=800)

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate, reauthor=reauthor,
    )

    # the workout is HELD (per-domain), not recorded — but the run is NOT terminal (not 0 plans)
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_UNRESOLVED
    assert store.read("plan::workout", root=tmp_path) == []
    # the OTHER domain (nutrition) surfaced — the hold is per-domain, not a terminal halt
    assert out["results"]["nutrition"]["recorded"] is True
    assert store.read("plan::nutrition", root=tmp_path) != []


# --- Cycle 3: ADJUDICATOR once-per-held-domain + ADJUDICATOR fail-closed hold ---


def _multi_held_authors():
    """A supp + pep pair that holds additive-AE (supp) + conflict (pep) + rx-bpmh (supp AND pep).

    With the operator on a `bleeding-risk` Rx class (`_bpmh_store(..., "bleeding-risk")`), this forces
    FOUR distinct held findings, each a distinct `(held_domain, source, finding_id)` -> a distinct
    memo key -> one ADJUDICATOR yield per held finding:
      - additive-ae   / supplements / additive-ae:class:bleeding-risk
      - cross-domain-conflict / peptides / conflict:peptides:supplements/fish oil
      - rx-bpmh       / peptides     / rx-bpmh:peptides:bleeding-risk
      - rx-bpmh       / supplements  / rx-bpmh:supplements:bleeding-risk
    """
    return _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]},
                   "conflicts": [{"with_domain": "supplements", "with": "fish oil", "reason": "additive bleeding"}]},
    )


def test_adjudicator_yielded_once_per_held_domain(tmp_path, monkeypatch):
    # AC-2 (ADJUDICATOR yielded once per held domain per pass): a fixture holding additive-AE +
    # cross-domain-conflict + Rx-BPMH (4 distinct held findings) yields exactly ONE ADJUDICATOR
    # request per held finding, each independently memo-keyed by `(held-domain, hold-class,
    # finding_id)`. Assert the count of ADJUDICATOR yields == the number of held findings (4 >= 3).
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_multi_held_authors())
    gate = _clean_composing_gate()

    liaison_findings = []

    def liaison(safety_finding):
        liaison_findings.append((safety_finding["source"], safety_finding["held_domain"]))
        # a content-valid HIGH override that echoes the finding's caution verbatim (the release
        # condition) — so the holds clear and the pass surfaces a plan.
        env = _envelope(band="HIGH", finding_id=safety_finding["finding_id"])
        env["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return env

    out, kinds = _kind_spy_run(
        monkeypatch,
        raw_intake=_raw_intake(), deid_client=deid_client, dispatch=dispatch,
        store_read=store_read, root=tmp_path, plan_date=PLAN_DATE,
        domains=("supplements", "peptides"), gate_dispatch=gate, adjudicator=liaison,
    )

    # exactly one ADJUDICATOR yield per held finding (4 here, >= 3 required by AC-2)
    from scripts.plan import plan_driver
    adjudicator_yields = [k for k in kinds if k == plan_driver.ADJUDICATOR]
    assert len(adjudicator_yields) == 4, f"ADJUDICATOR yields != held findings: {kinds}"
    # each held finding was independently dispatched (distinct (source, held_domain) pairs)
    assert len(set(liaison_findings)) == 4, f"held findings not independently keyed: {liaison_findings}"
    assert ("additive-ae", "supplements") in liaison_findings
    assert ("cross-domain-conflict", "peptides") in liaison_findings
    assert ("rx-bpmh", "supplements") in liaison_findings
    assert ("rx-bpmh", "peptides") in liaison_findings


def test_adjudicator_fail_closed_holds_affected_domain(tmp_path):
    # AC-6 (ADJUDICATOR fail-closed shape, per-domain hold — NOT terminal): a malformed/absent
    # liaison envelope for a held domain -> that AFFECTED held domain stays HELD (the `outcome ==
    # "cleared"` release does NOT fire, records nothing) while OTHER domains MAY surface. Threshold
    # is "affected domain not recorded", NOT "0 plans". A SELECTIVE liaison clears the conflict +
    # rx-bpmh on peptides but returns NO envelope for the additive-AE supplements finding -> the
    # supplements domain stays held; peptides (all concerns cleared) surfaces.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_multi_held_authors())
    gate = _clean_composing_gate()

    # block-stands (no envelope -> the block stands) for the additive-AE finding; clear the conflict
    # + rx-bpmh findings with a content-valid HIGH override (caution echoed). supplements stays held
    # by additive-AE (+ its rx-bpmh, which DOES clear, but additive-AE keeps it held); peptides
    # clears its conflict + rx-bpmh and surfaces. `_selective_liaison` echoes the caution verbatim.
    selective_liaison = _selective_liaison(
        {"cross-domain-conflict": "HIGH", "rx-bpmh": "HIGH"}  # additive-ae unmapped -> None -> held
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        gate_dispatch=gate, adjudicator=selective_liaison,
    )

    # the AFFECTED held domain (supplements, additive-AE block-stands) records nothing — per-domain
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []
    # the OTHER domain (peptides, all concerns cleared) surfaced — NOT a terminal "0 plans" halt
    assert out["results"]["peptides"]["recorded"] is True
    assert store.read("plan::peptides", root=tmp_path) != []


# --- Cycle 4: cache-HIT-proceeds-unchanged + charge-on-miss-only + REPLAY SAFETY ---


def _replay_safety_authors():
    """A 4-domain fixture forcing 1 REAUTHOR + 4 ADJUDICATOR dispatches in one pass.

    workout over the ceiling + nutrition not-sustaining -> a REAUTHOR; supp + pep both bleeding-risk
    + a pep conflict + the operator on a bleeding-risk Rx class -> 4 ADJUDICATOR findings (additive-AE
    supp, conflict pep, rx-bpmh supp, rx-bpmh pep). All clear -> all four domains surface ONE row each.
    """
    from tests.plan.test_generate_plan import _peptide_rec, _supplement_rec

    return {
        "workout": _recon(_author(_workout_rec("Heavy squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
        "supplements": _recon(
            _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
            ae_profile={"additive_classes": ["bleeding-risk"]},
        ),
        "peptides": _recon(
            _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
            ae_profile={"additive_classes": ["bleeding-risk"]},
            conflicts=[{"with_domain": "supplements", "with": "fish oil", "reason": "additive bleeding"}],
        ),
    }


def _clearing_reauthor():
    """A spied energy-bounce re-author returning a fuelable session (records every call)."""
    calls = []

    def reauthor(domain, constraint):
        calls.append((domain, constraint))
        return _recon(_author(_workout_rec("Light goblet squat", 2)), energy_cost_kcal=400)

    reauthor.calls = calls
    return reauthor


def _clearing_liaison():
    """A spied liaison clearing every held finding with a content-valid HIGH override (caution echoed)."""
    calls = []

    def liaison(safety_finding):
        calls.append((safety_finding["source"], safety_finding["held_domain"]))
        env = _envelope(band="HIGH", finding_id=safety_finding["finding_id"])
        env["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return env

    liaison.calls = calls
    return liaison


def test_cache_hit_raises_no_sentinel_on_replay(tmp_path):
    # AC-3 (cache-HIT proceeds unchanged): on the replay rounds, each hook's key is already cached, so
    # the memo callable returns the cached envelope and raises NO sentinel. Spy the raw hooks and
    # assert each is dispatched EXACTLY ONCE (the cache miss) — 0 extra dispatches on the cached
    # replays. A replay that re-raised (re-dispatched) a cached hook would inflate the spy counts.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_replay_safety_authors())
    gate = _clean_composing_gate()
    reauthor = _clearing_reauthor()
    liaison = _clearing_liaison()

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition", "supplements", "peptides"),
        gate_dispatch=gate, reauthor=reauthor, adjudicator=liaison,
    )

    # each raw hook dispatched EXACTLY ONCE — the cached replays raised NO further sentinel (the HIT
    # returned from the memo cache). A double-raise on a cached key would re-dispatch and inflate this.
    assert len(reauthor.calls) == 1, f"reauthor re-dispatched on a cached replay: {reauthor.calls}"
    assert len(liaison.calls) == 4, f"liaison re-dispatched on a cached replay: {liaison.calls}"
    # each finding is a DISTINCT key (one dispatch per held finding, never a cached re-fire)
    assert len(set(liaison.calls)) == 4, f"a held finding fired more than once: {liaison.calls}"
    # the pass surfaced (all four domains recorded)
    for domain in ("workout", "nutrition", "supplements", "peptides"):
        assert out["results"][domain]["recorded"] is True


def test_replay_safety_no_double_charge_no_double_write(tmp_path):
    # AC-7 (REPLAY SAFETY — no-double-charge / no-double-write): a fixture triggering 1 REAUTHOR + 4
    # ADJUDICATOR dispatches (multiple replay rounds) -> `budget.count` AND the promoted `plan::`
    # row-count EQUAL a single synchronous in-process reference of the SAME fixtures (exact equality).
    #
    # REFERENCE (independent, no replay): drive the inner engine ONCE via `pipeline.run_generation`
    # with the hooks returning their envelopes DIRECTLY (no sentinel, one pass) — its promoted-row
    # count per domain is the canonical single-pass write count, and each hook fires exactly once.
    # Then drive the COLD (empty-cache) throw/replay `run_orchestrated` path and assert: each surfacing
    # domain promoted EXACTLY the reference row-count (no replay double-promote), and each hook
    # dispatched EXACTLY once (no charge on a replayed HIT). `budget.count` exceeding the single-pass
    # tally (a HIT was charged) OR the row-count exceeding the reference (a replay double-promoted) -> FAIL.
    from scripts.plan import pipeline

    # --- the independent single-pass reference (no replay; hooks return directly) ---
    ref_root = tmp_path / "reference"
    ref_store_read = _bpmh_store(ref_root, "bleeding-risk")
    ref_reauthor = _clearing_reauthor()
    ref_liaison = _clearing_liaison()
    # the authors the de-id'd run would dispatch (the same fixture envelopes)
    ref_authors = _replay_safety_authors()
    ref_result = pipeline.run_generation(
        ref_authors, ref_store_read, ref_root, plan_date=PLAN_DATE,
        reauthor=ref_reauthor, adjudicator=ref_liaison,
    )
    reference_rows = {d: len(store.read(f"plan::{d}", root=ref_root))
                      for d in ("workout", "nutrition", "supplements", "peptides")}
    reference_hook_dispatches = len(ref_reauthor.calls) + len(ref_liaison.calls)
    assert reference_hook_dispatches == 5, f"reference hook count != 5 (1 reauthor + 4 liaison): {reference_hook_dispatches}"
    assert all(reference_rows[d] == 1 for d in reference_rows), f"reference rows: {reference_rows}"

    # --- the cold throw/replay path (empty cache; the engine raises + replays) ---
    cold_root = tmp_path / "cold"
    cold_store_read = _bpmh_store(cold_root, "bleeding-risk")
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_replay_safety_authors())
    gate = _clean_composing_gate()
    cold_reauthor = _clearing_reauthor()
    cold_liaison = _clearing_liaison()

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, cold_store_read, cold_root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition", "supplements", "peptides"),
        gate_dispatch=gate, reauthor=cold_reauthor, adjudicator=cold_liaison,
    )

    # NO-DOUBLE-WRITE: each surfacing domain promoted EXACTLY the reference row-count (1 each) — the
    # fresh-scratch re-drives discarded their intermediate scratch and promoted only the final pass.
    for domain in ("workout", "nutrition", "supplements", "peptides"):
        cold_rows = len(store.read(f"plan::{domain}", root=cold_root))
        assert cold_rows == reference_rows[domain], (
            f"{domain}: throw/replay promoted {cold_rows} rows != reference {reference_rows[domain]} "
            f"(a replay double-promoted)"
        )
    # NO-DOUBLE-CHARGE: each hook dispatched EXACTLY once (== the reference), so the cap accrued once
    # per cache MISS, never on a replayed HIT.
    cold_hook_dispatches = len(cold_reauthor.calls) + len(cold_liaison.calls)
    assert cold_hook_dispatches == reference_hook_dispatches, (
        f"throw/replay hook dispatches {cold_hook_dispatches} != reference {reference_hook_dispatches} "
        f"(a replayed HIT was charged)"
    )
    # the aggregate dispatch_count equals the single-pass tally: 4 specialists + 1 gate + 1 reauthor +
    # 4 adjudicators = 10 — no HIT inflated the budget.
    assert out["dispatch_count"] == 10, f"throw/replay dispatch_count != single-pass tally 10: {out['dispatch_count']}"
