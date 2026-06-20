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
from tests.plan.test_generate_plan import _author, _seed_store, _workout_rec

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
