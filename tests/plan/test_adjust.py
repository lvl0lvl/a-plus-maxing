"""Tests for the ADJUST leg (the progression production caller, `scripts/plan/adjust.py`).

Pins the closed loop's adjust leg through the production path: the full
plan -> measure -> read-back -> ADJUST loop (generate_plan -> record_tracking ->
resolve_plan_progress -> adjust_plan records the specialist's adjusted output as a
new dated plan), the honest "nothing to progress from" boundary (the has_plan x
has_tracking value domain), the safety-floor-applies-to-the-re-plan guarantee (the
adjusted plan rides generate_plan, so the clearance gate + assemble's filters are
NOT bypassed on adjust), the adjusted_from provenance, and the store-surface
battery (cross-stream isolation, dedupe/idempotent, mutation). The de-load/advance
reasoning is the SPECIALIST'S (here a fixture author output; the real-agent
progression is exercised by a live personal-trainer dispatch, documented in the PR).
"""

import pytest

from scripts.plan import adjust, generate_plan as gp, track
from scripts.store import plan_schema, store
from tests.plan.test_generate_plan import (
    _author, _seed_store, _workout_rec,
    _nutrition_target_rec, _nutrition_meal_rec, _supplement_rec,
)

_PRIOR = "2026-06-18"
_ADJUST = "2026-06-25"


def _store_read(root):
    """The single-arg store reader generate_plan/router.summarize consume."""
    return lambda item: store.read(item, root=root)


def _wk_tracking(**over):
    """A workout tracking snapshot (the actual the operator logged)."""
    return {"elapsed_min": 45, "volume_lb": 5000, "sets_done": {"Goblet squat": 2}, **over}


def _seed_plan_and_tracking(root, *, plan_date=_PRIOR):
    """plan -> act -> measure: record an initial workout plan + a tracking snapshot."""
    gp.generate_plan(
        "workout", _author(_workout_rec("Goblet squat", 3)), _store_read(root), root,
        plan_date=plan_date, gates={"clearance_granted": False})
    track.record_tracking("workout", _wk_tracking(), plan_date, root)


def _adjusted(name="Box squat", **payload_over):
    """A captured ADJUSTED author output (the specialist's de-load, here a fixture)."""
    return _author(_workout_rec(name, 2, claim=f"de-load to {name.lower()} after missed sets",
                                detail="regress + drop a set", **payload_over))


# --- the closed loop (the marquee E2E) -------------------------------------

def test_closed_loop_plan_measure_adjust(tmp_path):
    """plan -> track -> resolve -> ADJUST: the specialist's adjusted plan records anew."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    progress = track.resolve_plan_progress("workout", _PRIOR, root)
    assert progress["has_plan"] and progress["has_tracking"]   # there IS progress to adjust from

    result = adjust.adjust_plan("workout", _adjusted("Box squat"), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.ADJUSTED and result["adjusted"] is True
    assert result["plan"]["exercises"][0]["name"] == "Box squat"
    # the adjusted plan is now the plan dated adjust_date (the new prescription)
    after = track.resolve_plan_progress("workout", _ADJUST, root)
    assert after["has_plan"] and after["plan"]["exercises"][0]["name"] == "Box squat"
    # MUTATION proof: with NO prior plan there is nothing to adjust from, so the SAME adjusted
    # output records nothing — the recording is caused by the progress, not the call alone.
    empty = tmp_path / "empty"
    _seed_store(empty)
    none = adjust.adjust_plan("workout", _adjusted("Box squat"), _store_read(empty), empty,
                              prior_date=_PRIOR, adjust_date=_ADJUST)
    assert none["adjusted"] is False and none["state"] == adjust.NO_PLAN_TO_ADJUST_FROM


# --- the honest boundary (the has_plan x has_tracking value domain) ---------

def test_no_plan_to_adjust_from_records_nothing(tmp_path):
    """No prior plan -> no-plan-to-adjust-from (generate, not adjust); records nothing."""
    root = tmp_path / "store"
    _seed_store(root)
    result = adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.NO_PLAN_TO_ADJUST_FROM and result["adjusted"] is False
    assert result["plan"] is None
    # nothing recorded at either date — no fabricated adjustment
    assert track.resolve_plan_progress("workout", _ADJUST, root)["has_plan"] is False
    assert track.resolve_plan_progress("workout", _PRIOR, root)["has_plan"] is False


def test_no_tracking_to_adjust_from_records_nothing(tmp_path):
    """A prior plan but no tracking -> no-tracking-to-adjust-from; records nothing."""
    root = tmp_path / "store"
    _seed_store(root)
    gp.generate_plan("workout", _author(_workout_rec("Goblet squat", 3)), _store_read(root),
                     root, plan_date=_PRIOR, gates={"clearance_granted": False})
    result = adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.NO_TRACKING_TO_ADJUST_FROM and result["adjusted"] is False
    assert track.resolve_plan_progress("workout", _ADJUST, root)["has_plan"] is False


# --- the safety floor is NOT bypassed on the re-plan -----------------------

def test_clearance_gate_applies_to_the_replan(tmp_path):
    """The adjusted workout plan rides generate_plan, so the load gate drops `load` on it too."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    result = adjust.adjust_plan(
        "workout", _adjusted("Front squat", load="70% 1RM"), _store_read(root), root,
        prior_date=_PRIOR, adjust_date=_ADJUST, gates={"clearance_granted": False})
    assert result["adjusted"] is True
    # the un-cleared load prescription is dropped on the re-plan exactly as on the initial plan
    assert all("load" not in ex for ex in result["plan"]["exercises"])


def test_replan_with_no_actionable_recommendation_records_nothing(tmp_path):
    """An adjusted output with no usable payload -> generate_plan's reason; records nothing."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    empty_author = {"specialist": "personal-trainer", "recommendations": [
        {"claim": "hold the current block", "source": "coach note", "confidence_tier": "established",
         "reversibility": "n/a", "category": "training"}]}  # no payload -> nothing to translate
    result = adjust.adjust_plan("workout", empty_author, _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["adjusted"] is False
    assert result["state"] == "no-actionable-recommendation"   # generate_plan's reason, surfaced


def test_adjusted_from_carries_the_prior_plan_and_tracking(tmp_path):
    """The result records WHAT it adjusted from (the prior prescription + the tracked actual)."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    result = adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    src = result["adjusted_from"]
    assert src["plan"]["exercises"][0]["name"] == "Goblet squat"   # the prior prescription
    assert src["tracking"]["sets_done"] == {"Goblet squat": 2}     # the tracked actual
    assert src["plan_date"] == _PRIOR and src["specialist"] == "personal-trainer"


def test_untracked_domain_raises(tmp_path):
    """Peptides is not a tracked domain (tracking is the watch-out stream) -> ValueError."""
    with pytest.raises(ValueError, match="peptides"):
        adjust.adjust_plan("peptides", _author(), _store_read(tmp_path), tmp_path,
                           prior_date=_PRIOR, adjust_date=_ADJUST)


# --- store-surface adversarial battery -------------------------------------

def test_adversarial_cross_stream_isolation(tmp_path):
    """Adjusting workout reads + writes ONLY workout's plan; another domain never crosses in."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    # a supplements plan dated the SAME prior date — a different domain stream
    plan_schema.record_plan("supplements", {"items": [{"name": "Creatine", "dose": "5 g"}]},
                            _PRIOR, "supplement-specialist", root)
    result = adjust.adjust_plan("workout", _adjusted("Box squat"), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    # the workout adjust reads the WORKOUT plan (exercises), never the supplements plan (items)
    assert "exercises" in result["adjusted_from"]["plan"]
    assert "items" not in result["adjusted_from"]["plan"]
    assert result["plan"]["exercises"][0]["name"] == "Box squat"
    # the supplements stream is untouched by the workout adjust
    assert plan_schema.read_plan("supplements", _PRIOR, root)["plan"]["items"][0]["name"] == "Creatine"


def test_adversarial_idempotent_then_supersede(tmp_path):
    """Same adjusted output at the same adjust_date is idempotent; a later date supersedes."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    adjust.adjust_plan("workout", _adjusted("Box squat"), _store_read(root), root,
                       prior_date=_PRIOR, adjust_date=_ADJUST)
    adjust.adjust_plan("workout", _adjusted("Box squat"), _store_read(root), root,
                       prior_date=_PRIOR, adjust_date=_ADJUST)   # identical, same date -> idempotent
    readings = store.read("plan::workout", root=root)
    at_adjust = [r for r in readings if r["timepoint"] == _ADJUST]
    assert len(at_adjust) == 1   # the identical same-date re-adjust did not duplicate
    # a later re-adjust supersedes (latest dated plan wins at its date)
    _seed_plan_and_tracking(root, plan_date=_ADJUST)   # act+measure on the adjusted block
    adjust.adjust_plan("workout", _adjusted("Hack squat"), _store_read(root), root,
                       prior_date=_ADJUST, adjust_date="2026-07-02")
    assert track.resolve_plan_progress("workout", "2026-07-02", root)["plan"]["exercises"][0]["name"] == "Hack squat"


def test_adversarial_mutation_records_via_generate_plan(tmp_path):
    """Mutation proof: the adjusted plan is recorded through generate_plan/record_plan.

    With progress present the adjusted exercise lands in plan::workout at adjust_date; the
    assertion fails if adjust_plan ever stops recording (the boundary path records nothing,
    so the presence of the adjusted plan is caused by the record, not the call frame).
    """
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    adjust.adjust_plan("workout", _adjusted("Distinctive-mutation-lift"), _store_read(root),
                       root, prior_date=_PRIOR, adjust_date=_ADJUST)
    readings = store.read("plan::workout", root=root)
    names = [ex["name"] for r in readings if r["timepoint"] == _ADJUST
             for ex in r["value"]["exercises"]]
    assert "Distinctive-mutation-lift" in names


# --- the forward-date gate (the same-date dedupe-drop misreport) ------------

def test_non_forward_adjust_date_raises(tmp_path):
    """adjust_date must be AFTER prior_date: a same-date/earlier date would dedupe-drop the
    adjusted plan against the prior plan's store identity while reporting `adjusted` — fail loud."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    with pytest.raises(ValueError, match="must be AFTER"):   # same date -> store-identity collision
        adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                           prior_date=_PRIOR, adjust_date=_PRIOR)
    with pytest.raises(ValueError, match="must be AFTER"):   # earlier than the prior block
        adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                           prior_date=_PRIOR, adjust_date="2026-06-10")
    with pytest.raises(ValueError):                          # a malformed date fails loud too
        adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                           prior_date=_PRIOR, adjust_date="not-a-date")
    # the prior plan is untouched by the rejected adjusts (no silent overwrite)
    assert track.resolve_plan_progress("workout", _PRIOR, root)["plan"]["exercises"][0]["name"] == "Goblet squat"


# --- the safety floor on the re-plan: the nutrition half --------------------

def test_red_s_lea_veto_applies_to_the_nutrition_replan(tmp_path):
    """The nutrition RED-S/LEA critical-floor veto fires on the ADJUST re-plan (floor not bypassed)."""
    root = tmp_path / "store"
    _seed_store(root)
    plan_schema.record_plan(
        "nutrition", {"calorie_goal": 2600, "macros": {"protein": 190, "carbs": 250, "fat": 80},
                      "meals": [{"name": "Breakfast", "kcal": 650}]}, _PRIOR, "nutritionist", root)
    track.record_tracking("nutrition", {"food_kcal": 2550}, _PRIOR, root)
    nut_adjusted = _author(
        _nutrition_target_rec(calorie_goal=2400, protein=180, carbs=230, fat=70),
        _nutrition_meal_rec("Breakfast", kcal=600), specialist="nutritionist")
    result = adjust.adjust_plan("nutrition", nut_adjusted, _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST,
                                gates={"red_s_lea_screen": "tripped"})
    assert result["adjusted"] is False
    assert result["state"] == gp.RED_S_LEA_CLINICAL_ROUTING   # the floor fired on the re-plan, no plan recorded
    assert track.resolve_plan_progress("nutrition", _ADJUST, root)["has_plan"] is False


# --- the adjust leg on a non-workout TRACKED domain -------------------------

def test_supplements_closed_loop_adjust(tmp_path):
    """The adjust leg works for supplements (a non-workout TRACKED domain)."""
    root = tmp_path / "store"
    _seed_store(root)
    plan_schema.record_plan("supplements", {"items": [{"name": "Creatine", "dose": "5 g"}]},
                            _PRIOR, "supplement-specialist", root)
    track.record_tracking("supplements", {"taken": ["Creatine"]}, _PRIOR, root)
    supp_adjusted = _author(_supplement_rec("Creatine", "5 g"), _supplement_rec("Citrulline", "6 g"),
                            specialist="supplement-specialist")
    result = adjust.adjust_plan("supplements", supp_adjusted, _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.ADJUSTED and result["adjusted"] is True
    assert "Citrulline" in [i["name"] for i in result["plan"]["items"]]   # the specialist's addition recorded


# --- the record path fails loud on a schema-nonconformant adjusted plan -----

def test_record_path_raises_on_schema_nonconformant_adjusted_plan(tmp_path):
    """A schema-nonconformant adjusted plan raises ValueError on the record path (never silently dropped)."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    bad = _author(_workout_rec("Box squat", 999))   # sets=999 violates the plan_schema 1..100 ceiling
    with pytest.raises(ValueError):
        adjust.adjust_plan("workout", bad, _store_read(root), root,
                           prior_date=_PRIOR, adjust_date=_ADJUST, gates={"clearance_granted": False})


# --- the has_plan x has_tracking value domain: the (no-plan, has-tracking) corner ---

def test_tracking_without_plan_for_date_is_no_plan_to_adjust_from(tmp_path):
    """Tracking present but no plan dated prior_date -> no-plan-to-adjust-from (has_plan checked first)."""
    root = tmp_path / "store"
    # the raw schema writer bypasses record_tracking's no-plan gate -> tracking with no plan-for-date
    plan_schema.record_plan_tracking("workout", _wk_tracking(), _PRIOR, root)
    result = adjust.adjust_plan("workout", _adjusted(), _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.NO_PLAN_TO_ADJUST_FROM and result["adjusted"] is False


# --- the nutrition AGGREGATE translator lands on the adjust path (not just the veto) ---

def test_nutrition_closed_loop_adjust_lands(tmp_path):
    """The nutrition AGGREGATE translator records an adjusted day plan (the happy path, not the veto)."""
    root = tmp_path / "store"
    _seed_store(root)
    plan_schema.record_plan(
        "nutrition", {"calorie_goal": 2600, "macros": {"protein": 190, "carbs": 250, "fat": 80},
                      "meals": [{"name": "Breakfast", "kcal": 650}]}, _PRIOR, "nutritionist", root)
    track.record_tracking("nutrition", {"food_kcal": 2550}, _PRIOR, root)
    nut_adjusted = _author(
        _nutrition_target_rec(calorie_goal=2400, protein=180, carbs=230, fat=70),
        _nutrition_meal_rec("Breakfast", contents="eggs, oats", kcal=600), specialist="nutritionist")
    result = adjust.adjust_plan("nutrition", nut_adjusted, _store_read(root), root,
                                prior_date=_PRIOR, adjust_date=_ADJUST)
    assert result["state"] == adjust.ADJUSTED and result["adjusted"] is True
    plan = result["plan"]
    assert plan["calorie_goal"] == 2400                  # the adjusted target landed (aggregate ran)
    assert plan["macros"]["protein"] == 180
    assert any(m["name"] == "Breakfast" for m in plan["meals"])
    assert track.resolve_plan_progress("nutrition", _ADJUST, root)["plan"]["calorie_goal"] == 2400


# --- the gates=None default-deny holds on the adjust path -------------------

def test_gates_none_default_drops_uncleared_load_on_replan(tmp_path):
    """With gates OMITTED (the all-conservative default), an un-cleared load is still dropped on adjust."""
    root = tmp_path / "store"
    _seed_plan_and_tracking(root)
    result = adjust.adjust_plan(
        "workout", _adjusted("Front squat", load="70% 1RM"), _store_read(root), root,
        prior_date=_PRIOR, adjust_date=_ADJUST)   # gates omitted -> None -> all-conservative default
    assert result["adjusted"] is True
    assert all("load" not in ex for ex in result["plan"]["exercises"])   # default-deny holds on adjust
