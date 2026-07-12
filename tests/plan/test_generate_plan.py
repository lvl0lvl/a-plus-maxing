"""Tests for the plan-generation production caller (the PF-S63-02 core-capability proof).

`generate_plan` is `assemble`'s production caller: it derives the summary from the store,
runs one captured author output through `assemble`'s four safety filters for a domain,
translates the surviving recommendations into the `plan_schema` domain plan, and records
it via `record_plan` (the store write the dashboard plan zone reads). These tests pin:

  - the wired path records a workout plan from an author envelope (happy path);
  - the LOAD-BEARING safety gates — the clearance gate (no load prescription without a
    clinician clearance) and the HALT struck-rec exclusion — each mutation-proven RED;
  - the honest no-plan states (thin-library / no recommendations / all-struck record
    NOTHING, never a fabricated regimen);
  - fail-loud on a schema-nonconformant translated plan;
  - the store-adversarial battery (docs/checklists/store-adversarial-tests.md) at the
    generate_plan write boundary — cross-stream isolation, dedupe idempotency, dedupe-key
    boundary, changed-value no-op; and
  - the production path end-to-end (a real store -> generate_plan -> rendered dashboard).
"""

import functools
import subprocess
from pathlib import Path

import pytest

from scripts.generate import generate
from scripts.model.client import ModelCallError, ModelClient
from scripts.plan import context_assembler, router
from scripts.plan.assemble import THIN_LIBRARY_GAP
from scripts.plan.generate_plan import (
    AUTHOR_CALL_FAILED,
    RED_S_LEA_CLINICAL_ROUTING,
    compute_plan,
    generate_plan,
)
from scripts.store import keying, store

PLAN_DATE = "2026-06-18"


# --- fixtures ------------------------------------------------------------------


def _seed_store(root, **overrides):
    """Seed PII-free operator-state items into a real temp store; return a bound reader.

    Backs the pass-through Summary Field-Set fields `summarize` reads. `overrides` replace
    individual field values. Returns a `store.read` pre-bound to `root` (the summarize
    caller contract).
    """
    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    fields.update(overrides)
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": PLAN_DATE, "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _workout_rec(name, sets, *, claim=None, load=None, **rec_extra):
    """A complete workout recommendation (universal contract + workout payload)."""
    payload = {"name": name, "sets": sets, "reps": "8-12", "detail": "controlled tempo"}
    if load is not None:
        payload["load"] = load
    rec = {
        "claim": claim or f"perform {name.lower()} to rebuild a movement base",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": payload,
    }
    rec.update(rec_extra)
    return rec


def _author(*recs, specialist="personal-trainer"):
    """A captured author envelope carrying `recs`."""
    return {"specialist": specialist, "recommendations": list(recs)}


# --- happy path ----------------------------------------------------------------


def test_records_workout_plan_from_author(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3), _workout_rec("Bodyweight RDL", 3))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["specialist"] == "personal-trainer"
    names = [ex["name"] for ex in result["plan"]["exercises"]]
    assert names == ["Goblet squat", "Bodyweight RDL"]
    # the plan is in the store, attributed to the author
    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["source"] == "plan::personal-trainer"


def test_summary_is_the_only_operator_state_source(tmp_path):
    # crit-7/8 at the caller boundary: the section surfaces operator inputs read by field
    # name from the summary (the 0-raw-PII boundary), not from any other source.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    author = _author(_workout_rec("Goblet squat", 3))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    personalization = result["section"]["personalization"]
    assert personalization.get("hard-limits") == "no fasting"
    assert personalization.get("goal-targets") == "return to pre-Jan-2026 loading"


# --- clearance gate (load-bearing; mutation-proven) ----------------------------


def test_clearance_gate_strips_load_by_default(tmp_path):
    # Default-deny: a load prescription is dropped when no clinician clearance is granted.
    # MUTATION: if `_to_workout_plan` stops popping `load`, this assertion goes RED.
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3, load="60% 1RM"))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert "load" not in result["plan"]["exercises"][0]


def test_clearance_granted_keeps_load(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Back squat", 3, load="70% 1RM"))

    result = generate_plan(
        "workout", author, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"clearance_granted": True},
    )

    assert result["plan"]["exercises"][0]["load"] == "70% 1RM"


# --- HALT struck-rec exclusion (load-bearing; mutation-proven) ------------------


def test_struck_rec_excluded_from_plan(tmp_path):
    # hard-limits "no overhead pressing"; a rec asserting an overhead press is struck by
    # assemble's HALT filter and must NOT be lifted back into a prescribed exercise.
    # MUTATION: if `_surviving` stops filtering struck claims, the struck exercise appears.
    store_read = _seed_store(tmp_path)  # hard-limits = "no overhead pressing"
    author = _author(
        _workout_rec("Goblet squat", 3),
        _workout_rec(
            "Overhead press", 3,
            claim="perform overhead pressing for shoulder strength",
            category="overhead-pressing",
        ),
    )

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    names = [ex["name"] for ex in result["plan"]["exercises"]]
    assert names == ["Goblet squat"]


def test_all_recs_struck_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(
        _workout_rec(
            "Overhead press", 3,
            claim="perform overhead pressing for shoulder strength",
            category="overhead-pressing",
        ),
    )

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-actionable-recommendation"
    assert store.read("plan::workout", root=tmp_path) == []


# --- honest no-plan states -----------------------------------------------------


def test_thin_library_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = {"specialist": "personal-trainer", "thin_library": True}

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == THIN_LIBRARY_GAP
    assert store.read("plan::workout", root=tmp_path) == []


def test_empty_recommendations_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author()  # zero recommendations

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-recommendations"
    assert store.read("plan::workout", root=tmp_path) == []


# --- fail-loud + routing -------------------------------------------------------


def test_unknown_domain_raises(tmp_path):
    store_read = _seed_store(tmp_path)
    with pytest.raises(KeyError):
        generate_plan("cardio", _author(), store_read, tmp_path, plan_date=PLAN_DATE)


def test_payload_missing_required_field_raises_loud(tmp_path):
    # A translator emitting a schema-nonconformant plan must fail LOUD at record_plan,
    # never silently drop. Here the payload omits the required `sets`.
    store_read = _seed_store(tmp_path)
    bad = _workout_rec("Goblet squat", 3)
    del bad["payload"]["sets"]
    author = _author(bad)

    with pytest.raises(ValueError):
        generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)
    assert store.read("plan::workout", root=tmp_path) == []


# --- store-adversarial battery (docs/checklists/store-adversarial-tests.md) -----


def test_cross_stream_isolation(tmp_path):
    # 1. Cross-stream collision: a workout write lands ONLY in plan::workout; no other
    #    plan stream is written, and reading another plan domain returns nothing.
    store_read = _seed_store(tmp_path)
    generate_plan("workout", _author(_workout_rec("Goblet squat", 3)),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    items = store.items(root=tmp_path)
    plan_items = [i for i in items if i.startswith("plan::")]
    assert plan_items == ["plan::workout"]
    for other in ("nutrition", "supplements", "peptides"):
        assert store.read(f"plan::{other}", root=tmp_path) == []


def test_dedupe_idempotent_rerun(tmp_path):
    # 2. Same-key idempotency: re-running with the same (domain, date, specialist) + value
    #    appends 0 lines (store dedupe), never a silent duplicate.
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3))
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::workout", root=tmp_path)) == 1


def test_dedupe_key_boundary_specialist_and_date(tmp_path):
    # 3. Dedupe-key boundary: a differing source (specialist) OR timepoint (date) is a
    #    distinct identity — both persist; they do not collide.
    store_read = _seed_store(tmp_path)
    rec = _workout_rec("Goblet squat", 3)
    generate_plan("workout", _author(rec, specialist="personal-trainer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(rec, specialist="health-implementer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(rec, specialist="personal-trainer"),
                  store_read, tmp_path, plan_date="2026-06-19")

    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 3


def test_changed_value_same_identity_is_noop(tmp_path):
    # 3 (cont.) value is EXCLUDED from the dedupe identity: a re-record with a CHANGED plan
    #    at the same (domain, date, specialist) is dropped (a revision goes via correct_plan,
    #    never a silent overwrite). The first value still reads current.
    store_read = _seed_store(tmp_path)
    generate_plan("workout", _author(_workout_rec("Goblet squat", 3)),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(_workout_rec("Bulgarian split squat", 4)),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["value"]["exercises"][0]["name"] == "Goblet squat"


# --- production path end-to-end (integration-verification mandate) -------------


def test_end_to_end_renders_on_dashboard(tmp_path):
    import datetime

    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3), _workout_rec("Bodyweight RDL", 3))
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run(
        "dashboard", _root=tmp_path, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    html = out.read_text(encoding="utf-8")
    assert "Goblet squat" in html
    assert "Bodyweight RDL" in html
    assert "personal-trainer" in html


# --- nutrition / supplements / peptides recommendation builders ----------------


def _nutrition_target_rec(*, calorie_goal=2400, protein=180, carbs=240, fat=70,
                          water_l=None, claim=None, **rec_extra):
    """A nutrition day-target recommendation (calorie + macro + optional water payload)."""
    payload = {
        "calorie_goal": calorie_goal,
        "macros": {"protein": protein, "carbs": carbs, "fat": fat},
    }
    if water_l is not None:
        payload["water_l"] = water_l
    rec = {
        "claim": claim or "set energy and protein at maintenance to support training recovery",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": payload,
    }
    rec.update(rec_extra)
    return rec


def _nutrition_meal_rec(name, *, contents=None, kcal=None, claim=None, **rec_extra):
    """A nutrition single-meal recommendation (its payload carries one `meal`)."""
    meal = {"name": name}
    if contents is not None:
        meal["contents"] = contents
    if kcal is not None:
        meal["kcal"] = kcal
    rec = {
        "claim": claim or f"distribute protein across the day with {name.lower()}",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": {"meal": meal},
    }
    rec.update(rec_extra)
    return rec


def _supplement_rec(name, dose, *, timing=None, claim=None, **rec_extra):
    """A supplement item recommendation (payload is one {name, dose, timing?})."""
    payload = {"name": name, "dose": dose}
    if timing is not None:
        payload["timing"] = timing
    rec = {
        "claim": claim or f"supplement {name.lower()} at {dose} to close a documented gap",
        "source": "Examine.com creatine monograph 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "supplementation",
        "payload": payload,
    }
    rec.update(rec_extra)
    return rec


def _peptide_rec(compound, dose, route, *, cycle_week=None, cycle_length_weeks=None,
                 tags=None, evidence=None, claim=None, **rec_extra):
    """A peptide single-compound regimen recommendation."""
    payload = {"compound": compound, "dose": dose, "route": route}
    if cycle_week is not None:
        payload["cycle_week"] = cycle_week
    if cycle_length_weeks is not None:
        payload["cycle_length_weeks"] = cycle_length_weeks
    if tags is not None:
        payload["tags"] = tags
    if evidence is not None:
        payload["evidence"] = evidence
    rec = {
        "claim": claim or f"run {compound} at {dose} {route} for localized tissue support",
        "source": "vault/library/peptides/bpc-157 research-report 2026",
        "confidence_tier": "experimental",
        "reversibility": "reversible on discontinuation",
        "category": "peptide-therapy",
        "payload": payload,
    }
    rec.update(rec_extra)
    return rec


# --- nutrition: aggregation + the RED-S/LEA critical-floor gate -----------------


def test_records_nutrition_plan_aggregates_recs(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(
        _nutrition_target_rec(calorie_goal=2600, protein=190, carbs=250, fat=80, water_l=3.0),
        _nutrition_meal_rec("Breakfast", contents="eggs, oats, berries", kcal=650),
        _nutrition_meal_rec("Lunch", contents="chicken, rice, greens", kcal=800),
        specialist="nutritionist",
    )

    result = generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["specialist"] == "nutritionist"
    plan = result["plan"]
    assert plan["calorie_goal"] == 2600
    assert plan["macros"] == {"protein": 190, "carbs": 250, "fat": 80}
    assert plan["water_l"] == 3.0
    assert [m["name"] for m in plan["meals"]] == ["Breakfast", "Lunch"]
    readings = store.read("plan::nutrition", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["source"] == "plan::nutritionist"


def test_nutrition_red_s_lea_gate_short_circuits(tmp_path):
    # The owned Phase-0.5 RED-S/LEA screen: when tripped, NO energy plan is recorded
    # (the honest clinical-routing state) even though the author returned a full plan.
    # MUTATION: if the _DOMAIN_GATES veto is removed, the plan records -> recorded True.
    store_read = _seed_store(tmp_path)
    author = _author(
        _nutrition_target_rec(), _nutrition_meal_rec("Breakfast"), specialist="nutritionist",
    )

    result = generate_plan(
        "nutrition", author, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"red_s_lea_screen": "tripped"},
    )

    assert result["recorded"] is False
    assert result["reason"] == RED_S_LEA_CLINICAL_ROUTING
    assert store.read("plan::nutrition", root=tmp_path) == []


def test_nutrition_red_s_lea_clear_records_plan(tmp_path):
    # Control for the gate: a clear screen (default) records the plan, so the gate trip —
    # not an absent plan — is what blocks recording (the mutation pair).
    store_read = _seed_store(tmp_path)
    author = _author(
        _nutrition_target_rec(), _nutrition_meal_rec("Breakfast"), specialist="nutritionist",
    )

    result = generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert len(store.read("plan::nutrition", root=tmp_path)) == 1


def test_nutrition_red_s_lea_gate_true_value_also_trips(tmp_path):
    # The gate accepts both the boolean True and "tripped" — cover the True branch.
    store_read = _seed_store(tmp_path)
    author = _author(
        _nutrition_target_rec(), _nutrition_meal_rec("Breakfast"), specialist="nutritionist",
    )

    result = generate_plan(
        "nutrition", author, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"red_s_lea_screen": True},
    )

    assert result["recorded"] is False
    assert result["reason"] == RED_S_LEA_CLINICAL_ROUTING
    assert store.read("plan::nutrition", root=tmp_path) == []


def test_nutrition_struck_meal_excluded(tmp_path):
    # A meal rec struck by the class-aware HALT (category in the prohibited set) is
    # excluded from the aggregated meals, never lifted back in.
    # MUTATION: if _surviving stops filtering struck claims, the struck meal appears.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    author = _author(
        _nutrition_target_rec(),
        _nutrition_meal_rec("Breakfast"),
        _nutrition_meal_rec("Fasting window", category="fasting",
                            claim="schedule a fasting window to cut calories"),
        specialist="nutritionist",
    )

    result = generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert [m["name"] for m in result["plan"]["meals"]] == ["Breakfast"]


def test_nutrition_struck_target_records_nothing(tmp_path):
    # If the energy-target rec is struck, there is no calorie_goal among survivors -> no
    # valid plan -> records nothing. The safety property: a struck energy prescription
    # cannot ship a partial plan.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    author = _author(
        _nutrition_target_rec(category="fasting", claim="cut to an aggressive fasting deficit"),
        _nutrition_meal_rec("Breakfast"),
        specialist="nutritionist",
    )

    result = generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-actionable-recommendation"
    assert store.read("plan::nutrition", root=tmp_path) == []


def test_nutrition_no_meals_records_nothing(tmp_path):
    # Targets present but no meal survives -> incomplete -> the honest no-plan state.
    store_read = _seed_store(tmp_path)
    author = _author(_nutrition_target_rec(), specialist="nutritionist")

    result = generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-actionable-recommendation"
    assert store.read("plan::nutrition", root=tmp_path) == []


def test_nutrition_malformed_macros_raises_loud(tmp_path):
    # A present-but-malformed macros (missing `fat`) passes through to record_plan, which
    # fails LOUD -> never silently dropped.
    store_read = _seed_store(tmp_path)
    bad_target = _nutrition_target_rec()
    del bad_target["payload"]["macros"]["fat"]
    author = _author(bad_target, _nutrition_meal_rec("Breakfast"), specialist="nutritionist")

    with pytest.raises(ValueError):
        generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)
    assert store.read("plan::nutrition", root=tmp_path) == []


# --- supplements: 1 rec -> 1 item -----------------------------------------------


def test_records_supplements_plan_from_recs(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(
        _supplement_rec("Creatine monohydrate", "5 g", timing="daily"),
        _supplement_rec("Vitamin D3", "2000 IU", timing="morning"),
        specialist="supplement-specialist",
    )

    result = generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["specialist"] == "supplement-specialist"
    assert [i["name"] for i in result["plan"]["items"]] == [
        "Creatine monohydrate", "Vitamin D3",
    ]
    readings = store.read("plan::supplements", root=tmp_path)
    assert readings[-1]["source"] == "plan::supplement-specialist"


def test_supplements_struck_item_excluded(tmp_path):
    # A supplement struck by the class-aware HALT (category in the prohibited set) is
    # excluded; the surviving items still record.
    # MUTATION: if _surviving stops filtering, the struck stimulant item appears.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no stimulant"})
    author = _author(
        _supplement_rec("Creatine monohydrate", "5 g"),
        _supplement_rec("High-dose caffeine", "400 mg", category="stimulant",
                        claim="take a stimulant pre-load for output"),
        specialist="supplement-specialist",
    )

    result = generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert [i["name"] for i in result["plan"]["items"]] == ["Creatine monohydrate"]


def test_supplements_all_struck_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path, **{"hard-limits": "no stimulant"})
    author = _author(
        _supplement_rec("High-dose caffeine", "400 mg", category="stimulant",
                        claim="take a stimulant pre-load for output"),
        specialist="supplement-specialist",
    )

    result = generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-actionable-recommendation"
    assert store.read("plan::supplements", root=tmp_path) == []


def test_supplements_malformed_payload_raises_loud(tmp_path):
    # A present-but-malformed item (missing required `dose`) passes through to record_plan,
    # which fails LOUD -> never silently dropped.
    store_read = _seed_store(tmp_path)
    bad = _supplement_rec("Creatine monohydrate", "5 g")
    del bad["payload"]["dose"]
    author = _author(bad, specialist="supplement-specialist")

    with pytest.raises(ValueError):
        generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)
    assert store.read("plan::supplements", root=tmp_path) == []


# --- peptides: single-compound regimen ------------------------------------------


def test_records_peptides_plan_single_compound(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(
        _peptide_rec("BPC-157", "250 mcg", "subcutaneous",
                     cycle_week=1, cycle_length_weeks=4, tags=["healing"]),
        specialist="peptide-specialist",
    )

    result = generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["specialist"] == "peptide-specialist"
    assert result["plan"]["compound"] == "BPC-157"
    assert result["plan"]["route"] == "subcutaneous"
    readings = store.read("plan::peptides", root=tmp_path)
    assert readings[-1]["source"] == "plan::peptide-specialist"


def test_peptides_takes_first_surviving_compound(tmp_path):
    # V1 records ONE compound; the first surviving recommendation is the regimen. A struck
    # leading rec is skipped to the next surviving one (proves _surviving filtering).
    # MUTATION: if _surviving stops filtering, the struck compound would be recorded.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    author = _author(
        _peptide_rec("FastMimetic", "1 mg", "oral", category="fasting",
                     claim="use a fasting protocol to extend the deficit"),
        _peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
        specialist="peptide-specialist",
    )

    result = generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["plan"]["compound"] == "BPC-157"


def test_peptides_takes_first_of_multiple_surviving(tmp_path):
    # V1 records ONE compound — when MORE than one rec survives, the first is the regimen
    # (multi-compound stacks are the deferred compound-band). MUTATION: a translator that
    # merged/accumulated survivors instead of taking the first would fail this.
    store_read = _seed_store(tmp_path)
    author = _author(
        _peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
        _peptide_rec("TB-500", "2 mg", "subcutaneous"),
        specialist="peptide-specialist",
    )

    result = generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["plan"]["compound"] == "BPC-157"
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_peptides_empty_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(specialist="peptide-specialist")

    result = generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-recommendations"
    assert store.read("plan::peptides", root=tmp_path) == []


def test_peptides_malformed_payload_raises_loud(tmp_path):
    # A present-but-malformed regimen (missing required `compound`) passes through to
    # record_plan, which fails LOUD -> never silently dropped.
    store_read = _seed_store(tmp_path)
    bad = _peptide_rec("BPC-157", "250 mcg", "subcutaneous")
    del bad["payload"]["compound"]
    author = _author(bad, specialist="peptide-specialist")

    with pytest.raises(ValueError):
        generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)
    assert store.read("plan::peptides", root=tmp_path) == []


# --- store-adversarial battery across the new domains ---------------------------


def test_four_domain_cross_stream_isolation(tmp_path):
    # Each domain's plan lands ONLY in its own plan:: stream; no cross-contamination.
    store_read = _seed_store(tmp_path)
    generate_plan("workout", _author(_workout_rec("Goblet squat", 3)),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("nutrition",
                  _author(_nutrition_target_rec(), _nutrition_meal_rec("Breakfast"),
                          specialist="nutritionist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("supplements",
                  _author(_supplement_rec("Creatine monohydrate", "5 g"),
                          specialist="supplement-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("peptides",
                  _author(_peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
                          specialist="peptide-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    plan_items = sorted(i for i in store.items(root=tmp_path) if i.startswith("plan::"))
    assert plan_items == [
        "plan::nutrition", "plan::peptides", "plan::supplements", "plan::workout",
    ]
    for domain in ("workout", "nutrition", "supplements", "peptides"):
        assert len(store.read(f"plan::{domain}", root=tmp_path)) == 1


def test_nutrition_dedupe_idempotent_rerun(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_nutrition_target_rec(), _nutrition_meal_rec("Breakfast"),
                     specialist="nutritionist")
    generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::nutrition", root=tmp_path)) == 1


def test_nutrition_changed_value_same_identity_is_noop(tmp_path):
    # value is EXCLUDED from the dedupe identity: a re-record with a CHANGED plan at the
    # same (domain, date, specialist) is dropped; the first value still reads current.
    store_read = _seed_store(tmp_path)
    generate_plan("nutrition",
                  _author(_nutrition_target_rec(calorie_goal=2400),
                          _nutrition_meal_rec("Breakfast"), specialist="nutritionist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("nutrition",
                  _author(_nutrition_target_rec(calorie_goal=3000),
                          _nutrition_meal_rec("Brunch"), specialist="nutritionist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    readings = store.read("plan::nutrition", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["value"]["calorie_goal"] == 2400


def test_nutrition_dedupe_key_boundary_specialist_and_date(tmp_path):
    store_read = _seed_store(tmp_path)
    target = _nutrition_target_rec()
    meal = _nutrition_meal_rec("Breakfast")
    generate_plan("nutrition", _author(target, meal, specialist="nutritionist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("nutrition", _author(target, meal, specialist="health-implementer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("nutrition", _author(target, meal, specialist="nutritionist"),
                  store_read, tmp_path, plan_date="2026-06-19")

    assert len(store.read("plan::nutrition", root=tmp_path)) == 3


def test_supplements_dedupe_idempotent_rerun(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_supplement_rec("Creatine monohydrate", "5 g"),
                     specialist="supplement-specialist")
    generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_supplements_changed_value_same_identity_is_noop(tmp_path):
    store_read = _seed_store(tmp_path)
    generate_plan("supplements",
                  _author(_supplement_rec("Creatine monohydrate", "5 g"),
                          specialist="supplement-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("supplements",
                  _author(_supplement_rec("Magnesium glycinate", "300 mg"),
                          specialist="supplement-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    readings = store.read("plan::supplements", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["value"]["items"][0]["name"] == "Creatine monohydrate"


def test_supplements_dedupe_key_boundary_specialist_and_date(tmp_path):
    store_read = _seed_store(tmp_path)
    rec = _supplement_rec("Creatine monohydrate", "5 g")
    generate_plan("supplements", _author(rec, specialist="supplement-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("supplements", _author(rec, specialist="health-implementer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("supplements", _author(rec, specialist="supplement-specialist"),
                  store_read, tmp_path, plan_date="2026-06-19")

    assert len(store.read("plan::supplements", root=tmp_path)) == 3


def test_peptides_dedupe_idempotent_rerun(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
                     specialist="peptide-specialist")
    generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_peptides_changed_value_same_identity_is_noop(tmp_path):
    store_read = _seed_store(tmp_path)
    generate_plan("peptides",
                  _author(_peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
                          specialist="peptide-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("peptides",
                  _author(_peptide_rec("TB-500", "2 mg", "subcutaneous"),
                          specialist="peptide-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    readings = store.read("plan::peptides", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["value"]["compound"] == "BPC-157"


def test_peptides_dedupe_key_boundary_specialist_and_date(tmp_path):
    store_read = _seed_store(tmp_path)
    rec = _peptide_rec("BPC-157", "250 mcg", "subcutaneous")
    generate_plan("peptides", _author(rec, specialist="peptide-specialist"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("peptides", _author(rec, specialist="health-implementer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("peptides", _author(rec, specialist="peptide-specialist"),
                  store_read, tmp_path, plan_date="2026-06-19")

    assert len(store.read("plan::peptides", root=tmp_path)) == 3


# --- production path end-to-end for the new domains (integration mandate) -------


def test_nutrition_end_to_end_renders_on_dashboard(tmp_path):
    import datetime

    store_read = _seed_store(tmp_path)
    author = _author(
        _nutrition_target_rec(calorie_goal=2600, protein=190),
        _nutrition_meal_rec("Breakfast", contents="eggs, oats, berries"),
        specialist="nutritionist",
    )
    generate_plan("nutrition", author, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run("dashboard", _root=tmp_path, _out_dir=tmp_path,
                       _today=datetime.date.fromisoformat(PLAN_DATE))
    html = out.read_text(encoding="utf-8")
    assert "2600" in html  # the calorie goal renders
    assert "Breakfast" in html
    assert "nutritionist" in html


def test_supplements_end_to_end_renders_on_dashboard(tmp_path):
    import datetime

    store_read = _seed_store(tmp_path)
    author = _author(
        _supplement_rec("Creatine monohydrate", "5 g", timing="daily"),
        specialist="supplement-specialist",
    )
    generate_plan("supplements", author, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run("dashboard", _root=tmp_path, _out_dir=tmp_path,
                       _today=datetime.date.fromisoformat(PLAN_DATE))
    html = out.read_text(encoding="utf-8")
    assert "Creatine monohydrate" in html
    assert "5 g" in html  # the dose renders on the card
    assert "supplement-specialist" in html


def test_peptides_end_to_end_renders_on_dashboard(tmp_path):
    import datetime

    store_read = _seed_store(tmp_path)
    author = _author(
        _peptide_rec("BPC-157", "250 mcg", "subcutaneous", cycle_week=1, cycle_length_weeks=4),
        specialist="peptide-specialist",
    )
    generate_plan("peptides", author, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run("dashboard", _root=tmp_path, _out_dir=tmp_path,
                       _today=datetime.date.fromisoformat(PLAN_DATE))
    html = out.read_text(encoding="utf-8")
    assert "BPC-157" in html
    assert "250 mcg" in html  # the dose renders in the protocol line
    assert "subcutaneous" in html  # the route renders in the protocol line
    assert "peptide-specialist" in html


# --- ADR-0015-T3: wire the plan-author dispatch through the one model client ----
#
# The plan-author envelope is now PRODUCED by a programmatic call through
# scripts/model/client.py's `author(domain, summary)` (the H-1 seam: `_author_callable`,
# NOT router.dispatch). A deterministic MOCK backend is injected into the real ModelClient
# at construction (no live API, no live agent dispatch). A FAILED author call (the typed
# ModelCallError raise) yields the honest no-plan state (recorded == False), never a
# fabricated plan. assemble's filters + the translators + record_plan stay byte-unchanged.

PRE_TASK_HEAD = "3e17b1d8291d86d48441e36177a71f34910fbe57"  # wdhc: 0ecdce60 (a pre-squash working commit) was gc-pruned mid-S132; repointed to the merge-base (== origin/main), a durable reachable base. plan_schema.py is byte-untouched in Wave 3, so the survivors correct_plan + record_plan_tracking stay byte-frozen vs it.
REPO_ROOT = Path(__file__).resolve().parents[2]


class _RecordingBackend:
    """A deterministic author backend that records its (domain, summary) call args.

    Returns `envelope` verbatim from `author(domain, summary)` — no live call. The recorded
    `calls` prove `compute_plan`/`generate_plan` reach the client's `author` with the
    de-identified summary (AC-1, AC-3).
    """

    def __init__(self, envelope):
        self.envelope = envelope
        self.calls = []

    def author(self, domain, summary):
        self.calls.append((domain, summary))
        return self.envelope


class _FailingBackend:
    """A backend whose author always errors — drives the client's ModelCallError raise (AC-4)."""

    def __init__(self):
        self.calls = 0

    def author(self, domain, summary):
        self.calls += 1
        raise RuntimeError("backend author call failed (deterministic test failure)")


def _mock_client(envelope):
    """A real ModelClient over a deterministic recording backend (the seam mock)."""
    backend = _RecordingBackend(envelope)
    return ModelClient(backend=backend), backend


# --- AC-1: the wired author path reaches the client's author -------------------


def test_wired_author_reaches_client(tmp_path):
    # With a mock client injected at the seam, compute_plan/generate_plan produce the
    # envelope BY CALLING client.author(domain, summary) — not a captured-verbatim feed.
    store_read = _seed_store(tmp_path)
    envelope = _author(_workout_rec("Goblet squat", 3), _workout_rec("Bodyweight RDL", 3))
    client, backend = _mock_client(envelope)

    result = generate_plan(
        "workout", None, store_read, tmp_path, plan_date=PLAN_DATE, client=client,
    )

    # the client's author was reached exactly once, for the workout domain
    assert len(backend.calls) == 1
    assert backend.calls[0][0] == "workout"
    # the produced envelope flowed through assemble -> the recorded plan
    assert result["recorded"] is True
    names = [ex["name"] for ex in result["plan"]["exercises"]]
    assert names == ["Goblet squat", "Bodyweight RDL"]


def test_author_callable_source_is_rewired():
    # The verbatim-return feed is re-wired into a client.author call (H-1 / Falsification).
    # MUTATION: if `_author_callable` reverts to returning a captured envelope verbatim
    # (no client.author call), this goes RED.
    src = (REPO_ROOT / "scripts" / "plan" / "generate_plan.py").read_text(encoding="utf-8")
    # isolate the _author_callable body
    start = src.index("def _author_callable(")
    end = src.index("\ndef ", start + 1)
    body = src[start:end]
    assert "client.author(" in body, "the seam closure must call client.author"
    assert "return author_output" not in body, "the captured-verbatim feed must be gone"


# --- AC-2: assemble / translators / record_plan are byte-UNCHANGED -------------


def _git_diff_lines(path):
    out = subprocess.run(
        ["git", "diff", PRE_TASK_HEAD, "--", path],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout


@pytest.mark.skip(
    reason="assemble.py SANCTIONED-SUPERSEDED by ADR-0041-T2 (uniform-program migration); this "
    "single-file byte-freeze vs the pre-task baseline is void. Behavioral guarantor: "
    "tests/plan/test_assemble.py + tests/plan/test_generate_plan_uniform.py. Wave-2 frozen-guard "
    "reconciliation, Architect Option-A ruling (§4)."
)
def test_assemble_byte_unchanged_vs_pretask():
    # The re-wire amends ONLY ADR-0006's dispatch MECHANISM; the four filters + the clearance
    # gate stay byte-identical to the pre-task commit (ADR-0015 Negative-4).
    # NEGATIVE-CONTROL (documented): adding a scratch comment to assemble.py makes this go RED.
    assert _git_diff_lines("scripts/plan/assemble.py") == ""


def _func_src(source_text, name):
    """The source segment of the top-level function `name` in `source_text`, or fail loud."""
    import ast

    for node in ast.parse(source_text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(source_text, node)
    raise AssertionError(f"function {name!r} not found in source")


def test_record_plan_byte_unchanged_vs_pretask():
    # ADR-0040 (AR-007) + ADR-0044-T1: plan_schema.py's sanctioned edits are read_plan's caller-side
    # confirmation-pointer pre-filter (ADR-0040) AND the record-spine supersession (ADR-0044-T1:
    # resolve_plan + record_plan now delegate to scripts.store.plan_model, behavioral guarantor
    # tests/store/test_plan_model.py). The SURVIVORS correct_plan + record_plan_tracking stay
    # byte-frozen. Failing-capable: an edit to either surviving frozen function reds it.
    pre = subprocess.run(
        ["git", "show", f"{PRE_TASK_HEAD}:scripts/store/plan_schema.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    cur = (REPO_ROOT / "scripts" / "store" / "plan_schema.py").read_text()
    # resolve_plan + record_plan CARVED OUT — ADR-0044-T1 record-spine supersession; guarantor
    # tests/store/test_plan_model.py. Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
    for name in ("correct_plan", "record_plan_tracking"):
        assert _func_src(cur, name) == _func_src(pre, name), (
            f"{name} changed vs pre-task — the record-spine survivors must stay byte-frozen "
            "(read_plan's ADR-0040 pre-filter + the ADR-0044-T1 record-spine supersession are sanctioned)"
        )


# --- AC-3: the author payload is the de-identified summary (summary-only) -------


def test_author_payload_is_deidentified_summary(tmp_path):
    # The payload to client.author is context_assembler.assemble_context's identity-stripped
    # record (0 raw operator IDENTITY PII) — this path routes through assemble_context, NOT the
    # superseded router.summarize band, and NOT the /chat raw-egress carve-out.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    envelope = _author(_workout_rec("Goblet squat", 3))
    client, backend = _mock_client(envelope)

    generate_plan("workout", None, store_read, tmp_path, plan_date=PLAN_DATE, client=client)

    domain, summary = backend.calls[0]
    assert summary == context_assembler.assemble_context(store_read)  # the exact record
    # the record carries field-set tokens by name, never raw store internals
    assert summary.get("hard-limits") == "no fasting"


def test_author_payload_routes_through_assemble_context(tmp_path):
    # The front door routes the author payload through assemble_context (the no-DATA-COLLAPSE
    # record), NOT the superseded router.summarize band. Seeds an allowlisted health-substance
    # field (a multi-day split) so assemble_context carries the uncollapsed detail while
    # summarize collapses it to the coarse `training-volume-band`. The payload must carry the
    # substantive detail AND differ from the summarize band — proving the compute_plan summary
    # source is assemble_context, not summarize.
    # MUTATION: reverting compute_plan's `assemble_context(store_read)` to `summarize(store_read)`
    # drops the split (the band has no raw detail) -> both assertions RED.
    split = (
        "Mon: back squat 5x5 at RPE 8, romanian deadlift 4x8; "
        "Wed: bench press 5x5, weighted dip 3x10; "
        "Fri: front squat 4x6, barbell row 4x8"
    )
    store_read = _seed_store(tmp_path, **{"raw-training-detail-free-text": split})
    envelope = _author(_workout_rec("Goblet squat", 3))
    client, backend = _mock_client(envelope)

    generate_plan("workout", None, store_read, tmp_path, plan_date=PLAN_DATE, client=client)

    _, summary = backend.calls[0]
    assert summary.get("raw-training-detail-free-text") == split  # carried UNCOLLAPSED
    assert summary != router.summarize(store_read)  # routed through assemble_context, not the band


# --- AC-4: honest no-plan on a FAILED author call (the typed ModelCallError) ----


def test_failed_author_call_records_nothing(tmp_path):
    # A failed author call (the client's typed ModelCallError raise) yields the honest
    # no-plan state: recorded == False, the honest reason, 0 fabricated plan written.
    # MUTATION: if the failure path fabricates/records any plan, this goes RED.
    store_read = _seed_store(tmp_path)
    client = ModelClient(backend=_FailingBackend())

    result = generate_plan(
        "workout", None, store_read, tmp_path, plan_date=PLAN_DATE, client=client,
    )

    assert result["recorded"] is False
    assert result["plan"] is None
    assert result["reason"] == AUTHOR_CALL_FAILED
    assert store.read("plan::workout", root=tmp_path) == []


def test_failed_author_call_compute_records_nothing(tmp_path):
    # The same fail-closed property at the compute_plan seam (the orchestrator's entry).
    store_read = _seed_store(tmp_path)
    client = ModelClient(backend=_FailingBackend())

    candidate = compute_plan("workout", None, store_read, client=client)

    assert candidate["plan"] is None
    assert candidate["reason"] == AUTHOR_CALL_FAILED


def test_failed_author_raises_modelcallerror_at_client():
    # Ground the typed-raise contract this task routes on: the client raises ModelCallError
    # (ADR-0015-T1's fail-closed boundary) when its backend author fails.
    client = ModelClient(backend=_FailingBackend())
    with pytest.raises(ModelCallError):
        client.author("workout", {})


# --- AC-5: the --self-test shape passes with the programmatic mock-client author -


def test_self_test_passes_with_mock_client_author():
    # The core-capability self-test runs the wired path with the author output produced BY
    # a deterministic mock client at the seam (no live agent dispatch) and returns 0.
    from scripts.plan.generate_plan import _self_test

    assert _self_test() == 0


# --- PR #270: the non-tautological schema <-> record link (the live author schema records) ---


def test_schema_conformant_author_records_a_plan_each_domain(tmp_path):
    """Non-tautological schema<->record: a rec conforming to the LIVE author schema records a plan.

    For each of the four plan domains, an author envelope whose recommendations conform to
    `client._author_output_schema(domain)` (validated via jsonschema, in `.venv`) runs through the
    captured-envelope `generate_plan` path and RECORDS a plan — coupling the structured-output schema
    the live author call constrains to a real recordable plan. Motivated by BUG-03/API-02 (the schema
    is the soft model-side hint; the engine `record_plan` catch is the deferred real fix), this proves
    the tightened schema still admits a recordable, value-valid envelope. Failing-capable: a domain
    whose schema-conformant author no longer records reds the per-domain assertion.
    """
    import jsonschema

    from scripts.model.client import _author_output_schema

    cases = {
        "workout": _author(_workout_rec("Goblet squat", 3, grounding="human")),
        "nutrition": _author(
            _nutrition_target_rec(grounding="human"),
            _nutrition_meal_rec("Breakfast", grounding="human"),
            specialist="nutritionist",
        ),
        "supplements": _author(
            _supplement_rec("Creatine", "5 g", grounding="human"), specialist="supplement-specialist"
        ),
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subcutaneous", grounding="human"),
            specialist="peptide-specialist",
        ),
    }
    for domain, author in cases.items():
        jsonschema.validate(author, _author_output_schema(domain))  # conforms to the LIVE schema
        root = tmp_path / domain
        store_read = _seed_store(root)
        result = generate_plan(domain, author, store_read, root, plan_date=PLAN_DATE)
        assert result["recorded"] is True, (
            f"{domain}: a schema-conformant author did not record ({result['reason']})"
        )


# --- AC-6 closes as the suite pass (Step 8 regression).
