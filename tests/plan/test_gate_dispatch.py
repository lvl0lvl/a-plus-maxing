"""Tests for the composed `gate_dispatch` adapter (ADR-0026-T2).

`scripts.plan.gate_dispatch.compose_gate_dispatch(judge_client, review_dispatch, *, lenses)`
returns the single-arg `gate_dispatch(assembled_plan) -> disposition` callable the ADR-0026-T1
shared driver (`plan_driver.drive`) consumes via its `gate_dispatch=` seam. Over the assembled
`run_generation` result it runs BOTH built gate callables — `quality_judge` (the QUALITY gate) AND
`review_plan` (the SAFETY gate) — and maps their native shapes into EXACTLY the 3-key disposition
`{accept, safety_passed, revise_domains}` the driver's single-disposition read consumes. These pin:

  - AC-1: a clean accept-band judge + a 0-finding review emits the EXACT 3 keys
    `{accept: True, safety_passed: True, revise_domains: []}` — no more, no fewer;
  - AC-2 (NON-TAUTOLOGICAL): a REVISE + passing review derives `revise_domains` per the rule — a
    STRUCTURAL (empty-domain) deduction localizes to the SPECIFIC domain via the assembled result's
    section; a DIMENSION-level below-band deduction maps to ALL run-set domains (never `[]`);
  - AC-3: a not-passed review (>=1 finding) forces `safety_passed: False` regardless of the judge;
  - AC-4: a malformed composite (raised / non-dict judge / missing key) never surfaces
    `safety_passed: True` (fail-closed) — 0 such dispositions over the malformed family;
  - AC-5: BOTH gates run (judge dispatch >=1 AND review lens dispatch >=2);
  - AC-6: `revise_domains` is always a subset of the run's domains (no out-of-run-set target);
  - QA-4 (the T1<->T2 composer-driver seam): the REAL composer output, fed into `plan_driver`'s
    disposition-read path, promotes >=1 plan on an accept fixture and halts SAFETY_BLOCKED (0 plans)
    on a malformed fixture.

Every judge client / review dispatch is a fixture mock; no test hits a live API, and the test tree
carries 0 real operator PII (synthetic band/class tokens only).
"""

import tempfile

from scripts.plan import assemble
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.plan.plan_orchestrator import SAFETY_BLOCKED, run_orchestrated
from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.store import store

from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
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
from tests.plan.test_orchestrate import _nutrition, _recon
from tests.plan.test_plan_orchestrator import _RecordingDispatch, _deid_summary, _sustaining_authors
from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
from tests.plan.test_safety_review import _RecordingLensDispatch, _no_findings_dispatch

_DIMENSIONS = ("followability", "coherence", "internal consistency", "completeness")
_EXACT_3_KEYS = {"accept", "safety_passed", "revise_domains"}


# --- fixtures: assembled run_generation results ---------------------------------


def _assembled_clean_plan(tmp_path):
    """A clean four-domain `run_generation`-shaped result (no defect) — the ACCEPT input.

    Built through the real inner engine so the composer scores the genuine
    `{"results": {domain: {...}}}` shape both gate callables consume.
    """
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
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"
        ),
    }
    from scripts.plan import pipeline

    return pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE)


def _assembled_empty_domain_plan(tmp_path):
    """A `run_generation`-shaped result whose peptides domain is an empty coverage-gap section.

    The STRUCTURAL (empty-domain) defect localizes to ONE plan domain (peptides) via
    `results["peptides"]["section"]` — the localizing case for AC-2(a). The other three domains
    record cleanly, so the only revise target the rule derives is peptides.
    """
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
        # 0 recommendations -> the real `assemble` EMPTY_OUTPUT_GAP coverage-gap section
        "peptides": {"specialist": "peptide-specialist", "recommendations": []},
    }
    from scripts.plan import pipeline

    return pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE)


def _below_band_scores(dimension):
    """A judge-score map clean on every dimension EXCEPT `dimension` (a DIMENSION-level miss)."""
    scores = dict(_clean_scores())
    scores[dimension] = 4  # below the ACCEPT_MIN_BAND (9) -> a dimension-level deduction
    return scores


# === Cycle 1: AC-1 (exact-3-key) + AC-2 (REVISE derivation) + AC-3 (not-passed dominates) ===


def test_accept_passing_emits_exact_3_keys(tmp_path):
    # AC-1: a clean accept-band judge + a 0-finding review emits EXACTLY
    # `{accept: True, safety_passed: True, revise_domains: []}`. The key SET is asserted exactly —
    # a richer shape (an extra key) would break the driver's single-disposition read (OQ-2).
    assembled = _assembled_clean_plan(tmp_path)
    gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())

    disposition = gate(assembled)

    assert set(disposition.keys()) == _EXACT_3_KEYS, f"not the exact 3 keys: {set(disposition)}"
    assert disposition["accept"] is True
    assert disposition["safety_passed"] is True
    assert disposition["revise_domains"] == []


def test_revise_structural_deduction_localizes_to_specific_domain(tmp_path):
    # AC-2(a) NON-TAUTOLOGICAL: a STRUCTURAL (empty-domain) deduction localizes to the SPECIFIC
    # plan domain (peptides) the assembled result's section names — NOT all domains, NOT `[]`. The
    # clean judge scores all-9 but the empty in-scope domain forces a structural REVISE.
    assembled = _assembled_empty_domain_plan(tmp_path)
    gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())

    disposition = gate(assembled)

    assert set(disposition.keys()) == _EXACT_3_KEYS
    assert disposition["accept"] is False, "the empty in-scope domain did not force a REVISE"
    assert disposition["safety_passed"] is True
    assert disposition["revise_domains"] == ["peptides"], (
        f"the structural deduction did not localize to peptides: {disposition['revise_domains']}"
    )


def test_revise_dimension_deduction_targets_all_run_set_domains(tmp_path):
    # AC-2(b) NON-TAUTOLOGICAL: a DIMENSION-level below-band deduction (a low followability score
    # with no localizing section) maps to ALL run-set domains (the conservative re-author fallback),
    # NEVER `[]`. This proves the derivation is the rule, not a localize-or-collapse-to-empty heuristic.
    assembled = _assembled_clean_plan(tmp_path)
    run_domains = set(assembled["results"].keys())
    gate = compose_gate_dispatch(
        _FixedJudgeClient(_below_band_scores("followability")), _no_findings_dispatch()
    )

    disposition = gate(assembled)

    assert disposition["accept"] is False, "the below-band followability score did not force a REVISE"
    assert disposition["safety_passed"] is True
    assert set(disposition["revise_domains"]) == run_domains, (
        f"a non-localizing dimension deduction did not target all run-set domains: "
        f"{disposition['revise_domains']}"
    )
    assert disposition["revise_domains"] != [], "the autonomous-revise leg collapsed to []"


def test_revise_passing_populates_revise_domains(tmp_path):
    # AC-2 (the checklist oracle): a REVISE with a passing review carries `accept: False`,
    # `safety_passed: True`, a NON-EMPTY `revise_domains`, and names run-set domains only.
    assembled = _assembled_empty_domain_plan(tmp_path)
    run_domains = set(assembled["results"].keys())
    gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())

    disposition = gate(assembled)

    assert disposition["accept"] is False
    assert disposition["safety_passed"] is True
    assert disposition["revise_domains"], "the REVISE disposition carried no revise_domains"
    assert set(disposition["revise_domains"]) <= run_domains, "revise_domains names a non-run-set domain"


def test_not_passed_review_forces_safety_false(tmp_path):
    # AC-3: a review returning >=1 finding (`passed: False`) forces `safety_passed: False`
    # regardless of the judge verdict (safety dominates). A clean ACCEPT judge cannot override it.
    assembled = _assembled_clean_plan(tmp_path)
    finding_dispatch = _RecordingLensDispatch({
        "medical-safety-reviewer": [{
            "id": "cumulative-stimulant-load",
            "concern": "cumulative stimulant load exceeds the safe ceiling",
            "severity": "high",
        }],
        "health-edge-case-reviewer": [],
        "medical-liaison": [],
    })
    gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), finding_dispatch)

    disposition = gate(assembled)

    assert set(disposition.keys()) == _EXACT_3_KEYS
    assert disposition["accept"] is True, "the clean judge should still ACCEPT on quality"
    assert disposition["safety_passed"] is False, "a not-passed review did not force safety_passed False"


# === Cycle 2: AC-4 (fail-closed-on-malformed) ===================================


class _RaisingJudgeClient:
    """A judge client whose `judge` RAISES (a lens/model dispatch failed mid-review)."""

    def judge(self, payload):
        raise RuntimeError("judge client dispatch failed")


class _NonDictJudgeClient:
    """A judge client returning a non-dict (a malformed/degraded model response)."""

    def judge(self, payload):
        return ["followability"]


class _RaisingReviewDispatch:
    """A review lens dispatch that RAISES (a safety lens dispatch failed mid-review)."""

    def __call__(self, lens, prompt, assembled_plan):
        raise RuntimeError("safety lens dispatch failed mid-review")


def _safety_passed_true_count(dispositions):
    """Count dispositions whose `safety_passed` is boolean-True (the AC-4 floor: must be 0)."""
    return sum(
        1 for d in dispositions
        if isinstance(d, dict) and d.get("safety_passed") is True
    )


def test_malformed_composite_never_safety_passed_true(tmp_path):
    # AC-4 (fail-LOUD arm): across the malformed-composite family — a judge that RAISES, a review
    # dispatch that RAISES, a non-dict judge return — each gate RAISES (quality_judge / the dispatch
    # raises BEFORE the composer's `safety_passed` assignment), so this test pins the RAISE → caught →
    # 0-safety_passed-True propagation (in production `plan_driver._safe_gate` catches the raise to
    # None → SAFETY_BLOCKED). Count of `safety_passed is True` over the malformed family == 0. The
    # `safety_passed` ASSIGNMENT line itself (a non-raising malformed review) is guarded by
    # `test_malformed_missing_passed_key_never_safety_passed_true` below, not by this fail-loud arm.
    assembled = _assembled_clean_plan(tmp_path)

    malformed_gates = (
        compose_gate_dispatch(_RaisingJudgeClient(), _no_findings_dispatch()),
        compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _RaisingReviewDispatch()),
        compose_gate_dispatch(_NonDictJudgeClient(), _no_findings_dispatch()),
    )

    dispositions = []
    for gate in malformed_gates:
        try:
            dispositions.append(gate(assembled))
        except Exception:
            # a raised composer is the fail-closed contract (plan_driver._safe_gate catches it to
            # None -> SAFETY_BLOCKED) — it surfaces 0 safety_passed-True dispositions, AC-4-satisfying.
            dispositions.append(None)

    assert _safety_passed_true_count(dispositions) == 0, (
        "a malformed composite surfaced safety_passed is True (the silent-PASS the gate prevents)"
    )


def test_malformed_missing_passed_key_never_safety_passed_true(tmp_path):
    # AC-4 (missing-key arm): a review result missing the `passed` key must NOT yield
    # `safety_passed: True`. Inject the malformed review at the composer's review seam via a review
    # callable whose composed `review_plan` result is post-processed to drop `passed` — modeled here
    # by a composer built with a review step that returns a no-`passed` dict.
    assembled = _assembled_clean_plan(tmp_path)
    gate = compose_gate_dispatch(
        _FixedJudgeClient(_clean_scores()),
        _no_findings_dispatch(),
        _review=lambda plan, dispatch, *, lenses: {"findings": [], "lenses": tuple(lenses)},
    )

    disposition = gate(assembled)

    assert not (isinstance(disposition, dict) and disposition.get("safety_passed") is True), (
        "a review result missing the `passed` key surfaced safety_passed True"
    )


# === Cycle 3: AC-5 (both gates run) + AC-6 (revise_domains subset of run-set) ===


class _SpyJudgeClient:
    """A judge client wrapping a fixed score map and counting every `.judge` dispatch."""

    def __init__(self, scores):
        self.scores = scores
        self.calls = 0

    def judge(self, payload):
        self.calls += 1
        return dict(self.scores)


def test_both_gates_run_judge_ge1_review_ge2_lenses(tmp_path):
    # AC-5: the composer runs BOTH gates over the assembled result — the judge dispatch count >= 1
    # AND the review lens dispatch count >= 2 (the >=2-lens contract; DEFAULT_LENSES is 3). A
    # composer that silently dropped the safety gate, or ran a single lens, goes RED.
    assembled = _assembled_clean_plan(tmp_path)
    judge_client = _SpyJudgeClient(_clean_scores())
    review_dispatch = _no_findings_dispatch()
    gate = compose_gate_dispatch(judge_client, review_dispatch)

    gate(assembled)

    assert judge_client.calls >= 1, "the QUALITY gate (judge) did not fire"
    assert len(review_dispatch.calls) >= 2, (
        f"the SAFETY gate ran fewer than 2 lenses: {len(review_dispatch.calls)}"
    )
    # the dispatched lenses are the >=2-lens DEFAULT_LENSES roster
    assert {c["lens"] for c in review_dispatch.calls} == set(DEFAULT_LENSES)


def test_revise_domains_subset_of_run_set(tmp_path):
    # AC-6: over a fixture whose structural deduction references a KNOWN run-set domain, the derived
    # `revise_domains` names ONLY domains in the run's `domains` set — no out-of-run-set target that
    # would trip the driver's out-of-run-set guard (`plan_driver._ROLE_OF_DOMAIN`/`domains` check).
    assembled = _assembled_empty_domain_plan(tmp_path)
    run_domains = set(assembled["results"].keys())
    gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())

    disposition = gate(assembled)

    assert set(disposition["revise_domains"]) <= run_domains, (
        f"revise_domains escaped the run-set: {disposition['revise_domains']} not subset of {run_domains}"
    )
    # and the all-run-set fallback also stays within the run-set
    fallback_gate = compose_gate_dispatch(
        _FixedJudgeClient(_below_band_scores("coherence")), _no_findings_dispatch()
    )
    fallback = fallback_gate(assembled)
    assert set(fallback["revise_domains"]) <= run_domains


# === Wave-2 checkpoint: the QA-4 composer-driver seam assertion =================


def test_composer_drives_plan_driver_accept_and_malformed(tmp_path):
    # QA-4 (the T1<->T2 seam): feed the REAL composer's output (not a fixture disposition) into
    # `plan_driver`'s disposition-read path (via `run_orchestrated`, the driver's consumer) over
    #   (a) an accept fixture (ACCEPT judge band + 0-finding review) -> the driver promotes >=1 plan;
    #   (b) a malformed fixture (a raised judge) -> the driver halts SAFETY_BLOCKED, 0 plans.
    # A disposition-SHAPE mismatch surfaces HERE (both gate_dispatch.py and plan_driver.py exist at
    # Wave 2), not at the Wave-3 E2E.
    deid_client = _FixedDeidClient(_deid_summary())

    # (a) the accept path: the real composer over a clean judge + a 0-finding review
    accept_root = tmp_path / "accept"
    accept_read = _seed_store(accept_root)
    accept_gate = compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())
    out_accept = run_orchestrated(
        _raw_intake(), deid_client, _RecordingDispatch(_sustaining_authors()), accept_read, accept_root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=accept_gate,
    )
    assert out_accept.get("reason") is None, f"the composer's accept output did not surface a plan: {out_accept.get('reason')}"
    recorded = [d for d, r in out_accept["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1, "the driver promoted 0 plans on the composer's accept disposition"
    assert store.read("plan::workout", root=accept_root) != []

    # (b) the malformed path: the real composer over a RAISING judge -> SAFETY_BLOCKED, 0 plans
    blocked_root = tmp_path / "blocked"
    blocked_read = _seed_store(blocked_root)
    blocked_gate = compose_gate_dispatch(_RaisingJudgeClient(), _no_findings_dispatch())
    out_blocked = run_orchestrated(
        _raw_intake(), deid_client, _RecordingDispatch(_sustaining_authors()), blocked_read, blocked_root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=blocked_gate,
    )
    assert out_blocked["reason"] == SAFETY_BLOCKED, (
        f"the composer's malformed output did not halt SAFETY_BLOCKED: {out_blocked.get('reason')}"
    )
    assert out_blocked["results"] == {}, "a malformed-composite run surfaced a plan"
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=blocked_root) == []


# === AC-7: the suite gate — 0 live calls ========================================


def test_no_live_backend_constructed(tmp_path, monkeypatch):
    # AC-7: the composer runs over the injected fixture judge/review only — it constructs no
    # ModelClient (0 live spend). A ModelClient.__init__ spy confirms 0 self-constructed clients.
    from scripts.model.client import ModelClient

    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    assembled = _assembled_clean_plan(tmp_path)
    compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())(assembled)

    assert instantiations == [], "the composer constructed a ModelClient (must use only injected mocks)"
