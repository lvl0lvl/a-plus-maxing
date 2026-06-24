"""Tests for the post-assembly plan-quality judge (ADR-0023-T1).

`scripts.plan.quality_judge.quality_judge(assembled_plan, judge_client)` is the QUALITY
gate the orchestrator's `gate_dispatch=` seam dispatches over the assembled plan, between
generation and surfacing. It is a producer-independent callable: it scores the assembled
plan dict (`{"sections": [...]}`, the `assemble`/`run_generation` output) against the
maintained `vault/design/plan-quality-rubric.md` rubric (followability / coherence /
internal consistency / completeness) via an INJECTED judge client (a real model client in
production, a fixture mock here — 0 live spend), and returns an ACCEPT / REVISE verdict the
gate seam reads. It WRAPS the assembled output; it edits no inner-engine module. These pin:

  - AC-1: the judge is a producer-independent callable that FIRES when injected through the
    orchestrator's existing `gate_dispatch=` seam keyword (dispatch-count >=1), scoring the
    `run_generation`-shaped assembled plan and returning an ACCEPT/REVISE verdict;
  - AC-2: the judge input/dispatch payload EXCLUDES the specialists' self-assessments and
    the orchestrator's notes (producer-independence — the assembled plan + the rubric only);
  - AC-3 (the load-bearing falsification): a SEEDED-quality-defect plan (contradictory
    cross-section targets OR an empty/incoherent in-scope coverage-gap section, the latter
    DERIVED from `assemble._coverage_gap`'s real shape) gets a quality-defect verdict — 0
    seeded-defective plans surfaced with ACCEPT;
  - AC-4: `vault/design/plan-quality-rubric.md` exists with the four named dimensions;
  - AC-5: a clean assembled-plan fixture scored against a mock judge client yields ACCEPT;
  - QUALITY-vs-SAFETY: the judge scores quality only — it has no clinical-safety hold path
    (that is ADR-0024-T1's safety gate, a distinct gate on the same seam).

Every judge client is a fixture mock; no test hits a live API, and the test tree carries 0
real operator PII (synthetic band/class tokens only).
"""

from pathlib import Path

from scripts.plan import assemble
from scripts.plan.plan_orchestrator import run_orchestrated
from scripts.plan.quality_judge import ACCEPT, REVISE, quality_judge
from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import PLAN_DATE, _seed_store
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)

RUBRIC_PATH = Path("vault/design/plan-quality-rubric.md")

# The four rubric dimensions the judge scores against (AC-4 oracle).
_DIMENSIONS = ("followability", "coherence", "internal consistency", "completeness")


# --- fixtures ------------------------------------------------------------------


class _FixedJudgeClient:
    """A judge client that returns a fixed per-dimension score map.

    Mirrors `_FixedDeidClient` (the captured-output fixture-seam idiom) for the judge seam:
    `judge(payload)` returns the captured per-dimension scores. It RECORDS every payload it
    is handed so a test can inspect what the judge passed it (AC-2: producer-independence —
    the payload carries the assembled plan + the rubric only, never the producer's
    self-assessment). 0 live spend.

    Attributes:
        scores (dict): The per-dimension scores the mock returns (dimension -> 0-10).
    """

    def __init__(self, scores):
        self.scores = scores
        self.payloads = []

    def judge(self, payload):
        self.payloads.append(payload)
        return dict(self.scores)


def _clean_scores():
    """A clean per-dimension score map (every dimension at the 9-10 ACCEPT band)."""
    return {dim: 9 for dim in _DIMENSIONS}


def _clean_plan():
    """A well-formed assembled plan: two non-empty, internally-consistent sections."""
    return {
        "sections": [
            {
                "domain": "workout",
                "specialist": "personal-trainer",
                "recommendations": [
                    {"claim": "Goblet squat 3x8", "target": "lower-body strength"},
                ],
                "personalization": {"goal-targets": "strength"},
            },
            {
                "domain": "nutrition",
                "specialist": "nutritionist",
                "recommendations": [
                    {"claim": "Protein 1.6 g/kg", "target": "muscle protein synthesis"},
                ],
                "personalization": {"goal-targets": "strength"},
            },
        ]
    }


def _producer_tainted_plan():
    """A clean plan whose sections ALSO carry producer self-assessment + orchestrator notes.

    The producer-independence anti-target: a faithful judge payload must STRIP these (the
    specialist's `self_assessment` / `self_score` and the orchestrator's `orchestrator_notes`)
    so the judge scores the artifact, not the producer's claim about it (AC-2).
    """
    plan = _clean_plan()
    plan["orchestrator_notes"] = "orchestrator believes this plan is excellent"
    for section in plan["sections"]:
        section["self_assessment"] = "specialist rates this section 10/10"
        section["self_score"] = 10
    return plan


# --- AC-4: the rubric exists with the four named dimensions ---------------------


def test_rubric_has_four_named_dimensions():
    # AC-4: the maintained plan-quality rubric exists and names all four dimensions
    # (followability, coherence, internal consistency, completeness). The judge scores
    # against THIS rubric, so a missing dimension is a missing quality axis.
    assert RUBRIC_PATH.exists(), "the maintained plan-quality rubric does not exist"
    text = RUBRIC_PATH.read_text(encoding="utf-8").lower()
    for dimension in _DIMENSIONS:
        assert dimension in text, f"rubric missing the {dimension!r} dimension"


# --- AC-5: a clean plan scored against a mock judge yields ACCEPT ---------------


def test_clean_plan_scores_accept():
    # AC-5 (partial): a well-formed assembled plan, scored by a clean mock judge, yields an
    # ACCEPT verdict. 0 live calls (the judge client is a fixture mock).
    verdict = quality_judge(_clean_plan(), _FixedJudgeClient(_clean_scores()))
    assert verdict["verdict"] == ACCEPT


# --- AC-2: the judge payload excludes producer self-assessment + orchestrator notes ---


def test_judge_payload_excludes_producer_self_assessment():
    # AC-2 (producer-independence): the payload the judge hands its client carries the
    # assembled plan + the rubric ONLY — never the specialists' self-assessments nor the
    # orchestrator's notes. A judge fed the producer's self-scores cannot be independent.
    client = _FixedJudgeClient(_clean_scores())
    quality_judge(_producer_tainted_plan(), client)

    assert client.payloads, "the judge dispatched no payload to its client"
    import json

    for payload in client.payloads:
        serialized = json.dumps(payload, default=str)
        assert "self_assessment" not in serialized, "payload carried a specialist self-assessment"
        assert "self_score" not in serialized, "payload carried a specialist self-score"
        assert "orchestrator_notes" not in serialized, "payload carried orchestrator notes"


# --- AC-1: the judge fires when injected through the gate_dispatch= seam keyword ---


def test_quality_judge_fires_when_injected_as_gate_dispatch(tmp_path):
    # AC-1: the quality judge is a producer-independent callable shaped to be the
    # orchestrator's `gate_dispatch=` QUALITY gate. Inject it THROUGH the existing Wave-2
    # `gate_dispatch=` seam keyword (a recording spy wrapping the judge, passed as
    # `gate_dispatch=`) and assert it FIRES when invoked (dispatch-count >=1), scoring the
    # `run_generation`-shaped assembled plan and returning an ACCEPT/REVISE verdict. This task
    # does NOT modify `run_orchestrated`'s body to call the seam — the live-gating re-assertion
    # (0 plans surfaced without a verdict, the seam fired in the production loop) is
    # ADR-0022-T2's, Wave 4. Here we assert the judge fires when invoked through the seam.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    judge_client = _FixedJudgeClient(_clean_scores())

    gate_calls = []

    def judge_gate(assembled_plan):
        # the spy wraps the judge: it records the firing and returns the judge's verdict
        verdict = quality_judge(assembled_plan, judge_client)
        gate_calls.append(verdict)
        return verdict

    # the orchestrator ACCEPTS the judge injected through the existing seam keyword and runs
    # to completion (the seam is wired; this task does not invoke it in the body)
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=judge_gate,
    )
    assert "results" in out

    # the judge FIRES when invoked through the seam keyword: scoring the assembled-plan
    # (`{"sections": [...]}`) shape the gate dispatches over, returning an ACCEPT/REVISE
    # verdict (dispatch-count >=1).
    verdict = judge_gate(_clean_plan())
    assert len(gate_calls) >= 1
    assert verdict["verdict"] in (ACCEPT, REVISE)


# === Cycle 2: the seeded-defect falsification (REVISE on a defective plan) =======


def _contradictory_targets_plan():
    """A plan whose two sections set MUTUALLY-CONTRADICTORY targets for the same axis.

    The internal-consistency auto-fail: one section's recommendation targets a caloric SURPLUS
    and another targets a caloric DEFICIT for the same operator — a plan the operator cannot
    follow without violating itself. A clean mock judge (all 9s) would rubber-stamp this to
    ACCEPT; the judge's own structural check must catch it (the rubber-stamping falsification).
    """
    return {
        "sections": [
            {
                "domain": "nutrition",
                "specialist": "nutritionist",
                "recommendations": [
                    {"claim": "Eat in a caloric surplus", "target": "caloric-balance: surplus"},
                ],
                "personalization": {"goal-targets": "recomp"},
            },
            {
                "domain": "workout",
                "specialist": "personal-trainer",
                "recommendations": [
                    {"claim": "Eat in a caloric deficit", "target": "caloric-balance: deficit"},
                ],
                "personalization": {"goal-targets": "recomp"},
            },
        ]
    }


def _empty_coverage_gap_plan():
    """A plan whose in-scope domain section is the `assemble._coverage_gap` EMPTY-output shape.

    The completeness/coherence auto-fail, DERIVED FROM `assemble._coverage_gap`'s real emission
    shape (not a hand-spelled dict) — so the falsification exercises a section the judge actually
    receives in production. We pair the real empty-output gap (0 recommendations) with one clean
    section, so the defect is the empty in-scope domain, not an all-empty plan.
    """
    gap = assemble._coverage_gap(
        "peptides", assemble.EMPTY_OUTPUT_GAP, {"goal-targets": "recovery"}, "peptide-specialist"
    )
    return {
        "sections": [
            {
                "domain": "workout",
                "specialist": "personal-trainer",
                "recommendations": [
                    {"claim": "Goblet squat 3x8", "target": "lower-body strength"},
                ],
                "personalization": {"goal-targets": "recovery"},
            },
            gap,
        ]
    }


# --- AC-3 (the load-bearing falsification): 0 seeded-defective plans surfaced ACCEPT ---


def test_seeded_contradictory_targets_not_accepted():
    # AC-3 (i): a plan with mutually-contradictory cross-section targets gets a quality-defect
    # verdict (REVISE), NEVER ACCEPT — even when the mock judge returns all-clean scores. This
    # is the rubber-stamping falsification: weakening it to let a contradictory plan ACCEPT is
    # the exact failure the gate exists to prevent.
    verdict = quality_judge(_contradictory_targets_plan(), _FixedJudgeClient(_clean_scores()))
    assert verdict["verdict"] == REVISE
    assert verdict["verdict"] != ACCEPT
    # the verdict is rubric-anchored: it cites the failing dimension (internal consistency)
    failed_dims = {d["dimension"] for d in verdict["deductions"]}
    assert "internal consistency" in failed_dims


def test_seeded_empty_domain_section_not_accepted():
    # AC-3 (ii): a plan with an empty/incoherent in-scope coverage-gap section (the real
    # `assemble._coverage_gap` empty-output shape) gets a quality-defect verdict (REVISE), never
    # ACCEPT — even with all-clean mock scores. Derived from the real gap shape so a future
    # change to that shape surfaces here.
    verdict = quality_judge(_empty_coverage_gap_plan(), _FixedJudgeClient(_clean_scores()))
    assert verdict["verdict"] == REVISE
    assert verdict["verdict"] != ACCEPT
    # rubric-anchored: an empty in-scope domain is a completeness/coherence defect
    failed_dims = {d["dimension"] for d in verdict["deductions"]}
    assert failed_dims & {"completeness", "coherence"}, "empty-domain defect not rubric-anchored"


def test_zero_seeded_defective_plans_surface_accept():
    # AC-3 (the threshold): across BOTH seeded defect classes, 0 plans surface with ACCEPT.
    for defective in (_contradictory_targets_plan(), _empty_coverage_gap_plan()):
        verdict = quality_judge(defective, _FixedJudgeClient(_clean_scores()))
        assert verdict["verdict"] != ACCEPT, "a seeded-defective plan surfaced with ACCEPT"


# === BUG-01: the structural floor must FIRE on the REAL run_generation result shape ===
#
# The run_generation result (what `run_orchestrated` produces, what `gate_dispatch` receives,
# what `safety_review` already consumes) is shaped `{"results": {domain: {...}}, "reconciliation":
# ..., "adjudication": ...}` with NO top-level "sections" key — the per-domain section data lives
# under `results[domain]["section"]`. A structural floor that greps `plan.get("sections")` no-ops
# on this shape and returns 0 deductions, surfacing a SEEDED-DEFECTIVE plan as ACCEPT (the gate's
# whole purpose, defeated). These pin the floor against the SAME shape `safety_review` scores.


def _run_generation_result_with_empty_domain(tmp_path):
    """A REAL `run_generation`-shaped result whose peptides domain is an empty coverage-gap.

    Built through the actual `pipeline.run_generation` over fixture authors (the same shape
    `safety_review` consumes), with the peptides author returning an envelope carrying 0
    recommendations so its `results["peptides"]["section"]` is the real `assemble`
    EMPTY_OUTPUT_GAP coverage-gap shape — an in-scope domain that surfaced 0 actionable
    recommendations (a followability + completeness auto-fail). The other domains record cleanly.
    """
    from scripts.plan import pipeline
    from tests.plan.test_generate_plan import (
        _author,
        _nutrition_meal_rec,
        _nutrition_target_rec,
        _supplement_rec,
        _workout_rec,
    )
    from tests.plan.test_orchestrate import _nutrition, _recon

    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
        # an envelope with 0 recommendations -> the real `assemble` EMPTY_OUTPUT_GAP section
        # (an in-scope domain that surfaced nothing actionable — the completeness auto-fail).
        "peptides": {"specialist": "peptide-specialist", "recommendations": []},
    }
    return pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE)


def _run_generation_result_with_contradictory_targets():
    """A faithful `run_generation`-shaped result with mutually-contradictory cross-domain targets.

    The per-domain `section` carries the `assemble`-shaped recommendations the structural floor
    walks; two sections assert `caloric-balance: surplus` vs `caloric-balance: deficit` — the
    internal-consistency auto-fail, expressed on the real `{"results": {...}}` shape.
    """
    return {
        "results": {
            "nutrition": {
                "domain": "nutrition", "specialist": "nutritionist", "recorded": True, "plan": {},
                "section": {
                    "domain": "nutrition", "specialist": "nutritionist",
                    "recommendations": [
                        {"claim": "Eat in a caloric surplus", "target": "caloric-balance: surplus"},
                    ],
                },
                "reason": None,
            },
            "workout": {
                "domain": "workout", "specialist": "personal-trainer", "recorded": True, "plan": {},
                "section": {
                    "domain": "workout", "specialist": "personal-trainer",
                    "recommendations": [
                        {"claim": "Eat in a caloric deficit", "target": "caloric-balance: deficit"},
                    ],
                },
                "reason": None,
            },
        },
        "reconciliation": {},
        "adjudication": None,
    }


def test_structural_floor_fires_on_run_generation_result_empty_domain(tmp_path):
    # BUG-01 (i): a REAL run_generation result whose in-scope peptides domain surfaced 0
    # recommendations (the real `assemble` coverage-gap shape under `results[domain]["section"]`)
    # gets a quality-defect verdict (REVISE), NEVER ACCEPT — even with all-clean mock scores. On
    # the current "sections"-only floor this REDs (the floor no-ops on the `{"results": {...}}`
    # shape and surfaces ACCEPT).
    result = _run_generation_result_with_empty_domain(tmp_path)
    assert "results" in result and "sections" not in result, "fixture is not run_generation-shaped"
    verdict = quality_judge(result, _FixedJudgeClient(_clean_scores()))
    assert verdict["verdict"] == REVISE
    assert verdict["verdict"] != ACCEPT, "a seeded-defective run_generation result surfaced ACCEPT"
    failed_dims = {d["dimension"] for d in verdict["deductions"]}
    assert failed_dims & {"completeness", "coherence"}, "empty-domain defect not rubric-anchored"


def test_structural_floor_fires_on_run_generation_result_contradictory_targets():
    # BUG-01 (ii): a run_generation-shaped result with mutually-contradictory cross-section targets
    # gets a quality-defect verdict (REVISE), never ACCEPT — even with all-clean mock scores. REDs
    # on the current "sections"-only floor (which never inspects `results[domain]["section"]`).
    result = _run_generation_result_with_contradictory_targets()
    verdict = quality_judge(result, _FixedJudgeClient(_clean_scores()))
    assert verdict["verdict"] == REVISE
    assert verdict["verdict"] != ACCEPT, "a seeded-defective run_generation result surfaced ACCEPT"
    failed_dims = {d["dimension"] for d in verdict["deductions"]}
    assert "internal consistency" in failed_dims


class _NonMappingJudgeClient:
    """A judge client whose `judge` returns a non-mapping (a malformed model-client output)."""

    def __init__(self, value):
        self.value = value

    def judge(self, payload):
        return self.value


def test_non_mapping_judge_return_fails_loud_at_the_seam():
    # API-03: the judge client must return a `{dimension: number}` mapping. A non-mapping return
    # (a bare list / string / None — a malformed/degraded model response) RAISES at the seam with a
    # clear message, never failing deep in the per-dimension `scores.get(...)` walk or coercing
    # silently. The structural-floor-only deductions must not mask a broken judge client.
    import pytest

    for bad in (["followability"], "9", None, 9):
        with pytest.raises(TypeError, match="mapping"):
            quality_judge(_clean_plan(), _NonMappingJudgeClient(bad))


def test_unrecognizable_plan_shape_fails_loud():
    # BUG-01 (fail-loud guard): a plan carrying NEITHER a recognizable "results" NOR "sections"
    # structure must RAISE, never silently return 0 deductions -> a vacuous ACCEPT. A structural
    # floor that returns [] on an unrecognized shape would rubber-stamp anything.
    import pytest

    for bad in ({"unexpected": "shape"}, {"reconciliation": {}}):
        with pytest.raises((ValueError, KeyError, TypeError)):
            quality_judge(bad, _FixedJudgeClient(_clean_scores()))


# --- the QUALITY-vs-SAFETY distinction (this judge scores quality only) ----------


def test_quality_judge_does_not_screen_clinical_safety():
    # The QUALITY-vs-SAFETY distinction (spec AC framing): the quality judge scores QUALITY
    # (followability/coherence/consistency/completeness), DISTINCT from ADR-0024's clinical-
    # SAFETY review. It has NO hold/adjudicate path: a plan carrying a clinical-safety concern
    # but otherwise quality-clean is NOT held by THIS judge (that is the safety gate's job). The
    # verdict shape carries no safety hold/adjudication field, and a clinically-fraught but
    # quality-clean plan still scores on the quality axes only.
    safety_fraught_plan = {
        "sections": [
            {
                "domain": "peptides",
                "specialist": "peptide-specialist",
                # a clinically-fraught but well-formed, internally-consistent recommendation:
                # quality is clean; clinical safety is the SAFETY gate's concern, not this judge's
                "recommendations": [
                    {"claim": "BPC-157 250mcg subq", "target": "tissue-recovery"},
                ],
                "personalization": {"goal-targets": "recovery"},
            },
        ]
    }
    verdict = quality_judge(safety_fraught_plan, _FixedJudgeClient(_clean_scores()))
    # the judge scores quality only — ACCEPT/REVISE on the quality axes, no safety hold path
    assert verdict["verdict"] in (ACCEPT, REVISE)
    assert "hold" not in verdict, "the quality judge must carry no clinical-safety hold path"
    assert "adjudication" not in verdict, "the quality judge must carry no adjudication path"
    # the deductions (if any) cite only the four quality dimensions, never a safety axis
    for deduction in verdict["deductions"]:
        assert deduction["dimension"] in _DIMENSIONS
