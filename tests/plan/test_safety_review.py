"""Multi-agent whole-plan SAFETY review (`scripts/plan/safety_review.py`, ADR-0024-T1).

`review_plan` is the `/review-pr`-style multi-lens SAFETY review over the WHOLE assembled
plan. It dispatches >=2 independent safety lenses (`medical-safety-reviewer`,
`health-edge-case-reviewer`, the `medical-liaison` as a whole-plan reviewer — all present in
`.claude/agents/`) over the COMPOSED multi-domain plan (the `run_generation`-shaped result),
synthesizes + blind-triages their findings into one deduped set, reads the already-adjudicated
per-finding hold set off the result to EXCLUDE it (no double-gate, no gap), and returns the
synthesized finding set as the gate verdict (the legitimate findings that drive a revise / a
block). It is the ADDITIVE whole-plan layer — it WRAPS, does not replace, the inner per-finding
`adjudicate` gate (which adjudicates individual held findings, never the assembled whole). It is
the callable ADR-0022-T2 wires as the orchestrator's `gate_dispatch=` SAFETY gate. These pin:

  - AC-1: the review dispatches >=2 independent safety lenses over the COMPOSED whole plan (each
    dispatch payload IS the assembled plan object, not a per-finding fragment) and produces a
    synthesized, blind-triaged finding set; an overlapping finding flagged by two lenses collapses
    to ONE (the blind-triage dedupe — Risk R3);
  - AC-5: the test module runs against mock lens clients (0 live-API calls) — no `ModelClient` /
    `_ClaudeNoTrainBackend` is ever constructed;
  - AC-2 (Cycle 2): the seeded-emergent-issue falsification — a cumulative-cross-domain-load issue
    the inner gate raises 0 holds for is caught (drives a revise/block); a SAFE plan PASSES (the
    non-tautological positive control);
  - AC-3 (Cycle 2): no-double-gate/no-gap — an already-adjudicated per-finding hold is not
    re-adjudicated to a conflicting disposition, and no inner-gate hold is silently dropped;
  - AC-4 (Cycle 2): the review adds no override path of its own.

Every lens dispatch is a mock/fixture; no test hits a live API, and the test tree carries 0 real
operator PII (synthetic tokens only).
"""

from pathlib import Path

from scripts.model.client import ModelClient
from scripts.plan import safety_review
from scripts.plan.orchestrate import generate_plans, reconcile
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
from tests.plan.test_orchestrate import _compound_authors, _nutrition, _recon

# The independent safety lenses the review dispatches over the COMPOSED whole plan (the AC-1
# lens-identity oracle); each is a real `.claude/agents/<lens>/agent.md` (verified present).
_LENSES = ("medical-safety-reviewer", "health-edge-case-reviewer", "medical-liaison")
_AGENTS_ROOT = Path(".claude/agents")


# --- fixtures ------------------------------------------------------------------


class _RecordingLensDispatch:
    """A lens-dispatch seam that returns a pre-mapped finding envelope per lens.

    Records every `(lens, prompt, assembled_plan)` call so the test can inspect the dispatch
    payload (AC-1: the payload IS the composed whole plan) and the dispatch prompt (the inlined
    lens profile). Mirrors the `_RecordingDispatch` / `_FixedEnvelopeClient` fixture-seam pattern
    — the fixture stand-in for a live agent dispatch, so the review runs with 0 live spend.

    Attributes:
        findings_by_lens (dict): lens -> the list of finding dicts that lens emits.
    """

    def __init__(self, findings_by_lens):
        self.findings_by_lens = findings_by_lens
        self.calls = []

    def __call__(self, lens, prompt, assembled_plan):
        self.calls.append({"lens": lens, "prompt": prompt, "assembled_plan": assembled_plan})
        return self.findings_by_lens.get(lens, [])


def _no_findings_dispatch():
    """A lens dispatch where every lens emits 0 findings (the clean / SAFE-plan case)."""
    return _RecordingLensDispatch({lens: [] for lens in _LENSES})


def _assembled_safe_plan(tmp_path):
    """A clean four-domain assembled plan (no inner hold) — the SAFE positive-control input.

    Built through the real inner engine (`generate_plans`) so the review reviews the genuine
    `run_generation`-shaped result (`results` + `reconciliation` + the adjudication records).
    """
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(_supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"),
        "peptides": _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
    }
    return generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)


# --- AC-1: >=2 independent lenses over the COMPOSED whole plan -------------------


def test_dispatches_at_least_two_lenses_over_the_composed_whole(tmp_path):
    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _no_findings_dispatch()

    safety_review.review_plan(assembled, dispatch)

    # (a) >=2 lens dispatches fired over the whole-plan input
    assert len(dispatch.calls) >= 2, "fewer than 2 independent safety lenses dispatched"
    # (b) the dispatched lenses are the independent ones (the verified `.claude/agents/` set)
    dispatched = {call["lens"] for call in dispatch.calls}
    assert dispatched == set(_LENSES), f"unexpected lens roster: {dispatched}"
    # (c) each dispatch payload IS the ASSEMBLED multi-domain plan object (the composed whole),
    #     not a per-finding fragment.
    for call in dispatch.calls:
        assert call["assembled_plan"] is assembled, "a lens was dispatched a non-whole-plan payload"


def test_each_lens_dispatch_inlines_full_lens_profile(tmp_path):
    # AC-1 (the role-inlining oracle, INV-ROLE-INLINING): each dispatch prompt inlines the lens's
    # FULL profile verbatim, read live from `.claude/agents/<lens>/agent.md`. Fails (not vacuously)
    # if the review inlined an empty / nonexistent path.
    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _no_findings_dispatch()

    safety_review.review_plan(assembled, dispatch)

    by_lens = {call["lens"]: call["prompt"] for call in dispatch.calls}
    for lens in _LENSES:
        profile_text = (_AGENTS_ROOT / lens / "agent.md").read_text(encoding="utf-8")
        assert profile_text in by_lens[lens], f"{lens} profile not inlined in its dispatch prompt"
        assert "## Identity" in by_lens[lens], f"{lens} prompt missing the Identity marker"


def test_role_inlining_is_not_vacuous_on_a_real_lens_profile():
    # Failing-capable proof for AC-1's role-inlining: the lens profile text is non-trivial, so the
    # `in` assertion above cannot pass on an empty inline.
    profile_text = (_AGENTS_ROOT / "medical-safety-reviewer" / "agent.md").read_text(encoding="utf-8")
    assert len(profile_text) > 200
    assert "## Identity" in profile_text


def test_returns_a_synthesized_finding_set_not_per_lens_raw(tmp_path):
    # AC-1 (c): the return carries a SINGLE synthesized, blind-triaged finding set (a deduped
    # collection), not the per-lens raw output keyed by lens.
    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _no_findings_dispatch()

    verdict = safety_review.review_plan(assembled, dispatch)

    assert "findings" in verdict, "verdict missing the synthesized findings collection"
    assert isinstance(verdict["findings"], list), "the synthesized finding set must be one list"
    # a clean plan with 0 lens findings synthesizes to an empty set (no fabricated placeholder)
    assert verdict["findings"] == []


# --- AC-1 (blind-triage dedupe — Risk R3) ---------------------------------------


def test_overlapping_finding_collapses_to_one(tmp_path):
    # Risk R3: two lenses emit the SAME emergent concern (same dedupe key); the blind-triage
    # collapses them to ONE finding in the synthesized set. A non-deduped set (two copies) turns
    # this RED.
    assembled = _assembled_safe_plan(tmp_path)
    overlapping = {
        "id": "cumulative-stimulant-load",
        "concern": "cumulative stimulant load summed across four domains exceeds the safe ceiling",
        "severity": "high",
    }
    dispatch = _RecordingLensDispatch({
        "medical-safety-reviewer": [dict(overlapping)],
        "health-edge-case-reviewer": [dict(overlapping)],  # the SAME concern, flagged twice
        "medical-liaison": [],
    })

    verdict = safety_review.review_plan(assembled, dispatch)

    ids = [f["id"] for f in verdict["findings"]]
    assert ids.count("cumulative-stimulant-load") == 1, "blind-triage did not dedupe the overlap"
    assert len(verdict["findings"]) == 1


def test_distinct_findings_are_both_kept(tmp_path):
    # The dedupe collapses only OVERLAPPING findings — two DISTINCT concerns both survive (the
    # dedupe is not a collapse-everything sink).
    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _RecordingLensDispatch({
        "medical-safety-reviewer": [{"id": "stimulant-load", "concern": "stimulant", "severity": "high"}],
        "health-edge-case-reviewer": [{"id": "hepatic-load", "concern": "hepatic", "severity": "high"}],
        "medical-liaison": [],
    })

    verdict = safety_review.review_plan(assembled, dispatch)

    assert {f["id"] for f in verdict["findings"]} == {"stimulant-load", "hepatic-load"}


# --- AC-5: 0 live-API calls (mock lens clients only) ----------------------------


def test_no_live_backend_constructed(tmp_path, monkeypatch):
    # AC-5: the review runs over the injected mock dispatch only — it constructs no `ModelClient`
    # and thus no `_ClaudeNoTrainBackend`. A `ModelClient.__init__` spy confirms 0 self-constructed
    # clients (a live no-train backend is never instantiated -> 0 live spend).
    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _no_findings_dispatch()

    safety_review.review_plan(assembled, dispatch)

    assert instantiations == [], "the review constructed a ModelClient (must use only injected mocks)"


# === Cycle 2: seeded-emergent-issue falsification + no-double-gate/no-gap + no-override-path ===


def _assembled_emergent_unsafe_plan(tmp_path):
    """A four-domain assembled plan carrying a cumulative-cross-domain-load issue the inner gate is
    BLIND to (`reconcile` -> 0 holds).

    The emergent issue: a cumulative stimulant load summed across the workout + nutrition +
    supplement + peptide domains. The seed is chosen so NO per-finding screen fires:
      - the supplement and peptide declare DISJOINT additive-AE classes (`stimulant` vs
        `growth-factor`) -> no SHARED-class additive-AE hold, and no author-declared pairwise
        interaction -> no declared-interaction hold (the supplement<->peptide pairwise screen is
        blind);
      - `_seed_store` seeds NO `rx-interaction-classes`, so the operator's present Rx-class set is
        empty -> no supplement<->Rx BPMH hold;
      - no author-declared cross-domain conflict -> no conflict hold;
      - the nutrition budget sustains the workout -> no energy bounce / RED-S short-circuit.
    The cumulative stimulant load is emergent ONLY when the four domains are read together — exactly
    the class the whole-plan review owns and the per-finding gate cannot see.
    """
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("HIIT intervals", 8)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(),
            _nutrition_meal_rec("Pre-workout", contents="strong coffee + energy gel", kcal=200),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _recon(
            _author(_supplement_rec("Caffeine + synephrine", "300 mg"),
                    specialist="supplement-specialist"),
            ae_profile={"additive_classes": ["stimulant"]},  # disjoint from the peptide's class
        ),
        "peptides": _recon(
            _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
            ae_profile={"additive_classes": ["growth-factor"]},  # disjoint -> no shared-class hold
        ),
    }
    return generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)


# --- AC-2 (LOAD-BEARING falsification — Risk R1): seeded-emergent-issue probe -----


def test_inner_gate_is_blind_to_the_seeded_emergent_issue(tmp_path):
    # The non-tautology proof: `reconcile` over the seeded candidates raises 0 holds — the inner
    # per-finding gate genuinely sees nothing. If this seed DID produce a hold, the "emergent"
    # framing would be false (the inner gate would already own it). The four-domain candidate set
    # is built by `generate_plans` internally; here we reconcile the same candidate shapes directly.
    from scripts.plan.generate_plan import compute_plan

    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _recon(
            _author(_supplement_rec("Caffeine + synephrine", "300 mg"),
                    specialist="supplement-specialist"),
            ae_profile={"additive_classes": ["stimulant"]},
        ),
        "peptides": _recon(
            _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
            ae_profile={"additive_classes": ["growth-factor"]},
        ),
    }
    candidates = {d: compute_plan(d, a, store_read) for d, a in authors.items()}

    outcome = reconcile(candidates)  # operator_rx_classes defaults empty (no seeded Rx classes)

    assert outcome["holds"] == {}, "the inner gate raised a hold (the seed is not emergent)"
    assert outcome["conflict_held"] == []
    assert outcome["rx_bpmh_held"] == []
    assert outcome["report"]["additive_ae"] == []  # no pairwise additive-AE finding


def test_seeded_emergent_unsafe_plan_is_caught(tmp_path):
    # AC-2 (Risk R1): the review over the emergent-unsafe assembled plan, with lens mocks that (as
    # the lenses would) flag the cumulative stimulant load, surfaces a non-empty finding set / a
    # blocking verdict — count of seeded emergent-unsafe plans surfaced un-flagged = 0. A review
    # that returned an empty/PASS verdict here turns this RED.
    assembled = _assembled_emergent_unsafe_plan(tmp_path)
    dispatch = _RecordingLensDispatch({
        "medical-safety-reviewer": [{
            "id": "cumulative-stimulant-load",
            "concern": "cumulative stimulant load (workout + caffeine meal + supplement) exceeds the safe ceiling",
            "severity": "high",
        }],
        "health-edge-case-reviewer": [],
        "medical-liaison": [],
    })

    verdict = safety_review.review_plan(assembled, dispatch)

    assert verdict["findings"], "the seeded emergent-unsafe plan was surfaced un-flagged"
    assert verdict["passed"] is False, "the verdict did not drive a revise/block on the unsafe plan"


def test_safe_plan_positive_control_passes(tmp_path):
    # AC-2 POSITIVE CONTROL (non-tautological): a SAFE assembled plan (no cumulative-load issue; the
    # lens mocks emit 0 findings) PASSES — the review does NOT over-block a clean plan. Without this
    # control, "non-empty verdict" could pass on a review that blocks every plan unconditionally.
    assembled = _assembled_safe_plan(tmp_path)
    dispatch = _no_findings_dispatch()

    verdict = safety_review.review_plan(assembled, dispatch)

    assert verdict["findings"] == [], "the review over-blocked a clean plan"
    assert verdict["passed"] is True


# --- AC-3 (no-double-gate/no-gap — Risk R2) -------------------------------------


def _assembled_with_adjudicated_additive_ae_hold(tmp_path):
    """A four-domain plan carrying ONE already-adjudicated additive-AE per-finding hold.

    A fish-oil + BPC-157 pair both declaring `bleeding-risk` -> the inner additive-AE screen HOLDS
    the supplement; a block-stands (CRITICAL) liaison adjudication is carried on the result's
    `adjudication` record (`finding_id` echoed). The whole-plan review must EXCLUDE this
    already-adjudicated `finding_id` from its own set (no double-gate) — the per-finding gate owns it.
    """
    from tests.plan.test_orchestrate import _liaison

    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    return generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                          adjudicator=_liaison("CRITICAL"))  # block-stands; finding_id on the result


def test_already_adjudicated_per_finding_hold_is_not_re_adjudicated(tmp_path):
    # AC-3 (no double-gate): the additive-AE per-finding hold the inner gate already adjudicated is
    # carried on the result's `adjudication` record. Even when a lens RE-SURFACES that exact
    # finding_id, the review EXCLUDES it (it reads the adjudicated-hold set off the result) — 0
    # re-adjudications of a per-finding hold the inner gate owns. A review that did not exclude it
    # would re-surface the per-finding hold into the whole-plan set -> RED.
    assembled = _assembled_with_adjudicated_additive_ae_hold(tmp_path)
    adjudicated_id = assembled["adjudication"]["finding_id"]
    assert adjudicated_id is not None, "the fixture did not carry an adjudicated additive-AE finding_id"

    dispatch = _RecordingLensDispatch({
        # a lens re-surfaces the SAME per-finding hold the inner gate already adjudicated
        "medical-safety-reviewer": [{"finding_id": adjudicated_id, "id": adjudicated_id,
                                     "concern": "supplement<->peptide bleeding-risk", "severity": "high"}],
        "health-edge-case-reviewer": [],
        "medical-liaison": [],
    })

    verdict = safety_review.review_plan(assembled, dispatch)

    surfaced_ids = {f.get("finding_id") for f in verdict["findings"]}
    assert adjudicated_id not in surfaced_ids, "the review re-surfaced an already-adjudicated per-finding hold"


def test_inner_gate_hold_is_not_silently_dropped_when_distinct(tmp_path):
    # AC-3 (no gap, the other direction): a WHOLE-PLAN finding that is NOT one of the
    # already-adjudicated per-finding holds is NOT dropped on the assumption the inner gate handled
    # it — the exclusion is keyed on the adjudicated finding_ids only, so a genuinely emergent
    # whole-plan finding survives. A review that dropped every finding (over-broad exclusion) -> RED.
    assembled = _assembled_with_adjudicated_additive_ae_hold(tmp_path)
    dispatch = _RecordingLensDispatch({
        "medical-safety-reviewer": [{"id": "emergent-hepatic-load", "finding_id": "whole-plan:hepatic",
                                     "concern": "cumulative hepatic load across domains", "severity": "high"}],
        "health-edge-case-reviewer": [],
        "medical-liaison": [],
    })

    verdict = safety_review.review_plan(assembled, dispatch)

    surfaced_ids = {f.get("finding_id") for f in verdict["findings"]}
    assert "whole-plan:hepatic" in surfaced_ids, "the review silently dropped a distinct emergent finding (a gap)"


# --- AC-4 (inner-gate-untouched / no added override path) -----------------------


def test_review_module_adds_no_override_path():
    # AC-4: the review module adds NO override path of its own — no write to the override-record
    # path, no canonical override literal. `rg`-equivalent over the module source = 0 matches.
    source = (Path("scripts/plan/safety_review.py")).read_text(encoding="utf-8")
    for needle in ("override_record", "OVERRIDE_LITERAL", "operator is overriding a safety block"):
        assert needle not in source, f"the safety review module references an override path: {needle!r}"


def test_review_module_imports_nothing_that_mutates_the_inner_engine():
    # AC-4: the module does not import `adjudicate` / `orchestrate` symbols that WRITE the inner
    # engine. It reads the assembled-plan result + role profiles only. (It legitimately imports the
    # orchestrator's read-only `_role_profile` helper.)
    source = (Path("scripts/plan/safety_review.py")).read_text(encoding="utf-8")
    assert "from scripts.plan.adjudicate import" not in source
    assert "import adjudicate" not in source
    assert "record_plan" not in source
    assert "record_doctor_visit_queue_entry" not in source
