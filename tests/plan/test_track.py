"""Tests for scripts/plan/track.py — the measure + adjust-read-back legs of the closed loop.

`record_tracking` is the production caller for `plan_schema.record_plan_tracking` (the no-production-
caller gap); `resolve_plan_progress` joins a domain's plan + tracking into the plan-vs-actual view.
This suite covers the no-plan-to-track honest boundary (mutation-proven), the recorded path, the
read-back absence states, the store-adversarial battery for the new write/read surface (cross-stream
isolation, dedupe, mutation), and the closed-loop E2E through the existing `generate_plan` path.
"""

import pytest

from scripts.plan.track import (
    NO_PLAN_TO_TRACK,
    RECORDED,
    record_tracking,
    resolve_plan_progress,
)
from scripts.store import plan_schema, store
from tests.plan.test_generate_plan import _author, _seed_store, _workout_rec


def _workout_plan():
    return {"exercises": [{"name": "Squat", "sets": 3, "load": "185 lb", "reps": 8}]}


def _wk_tracking(**over):
    return {"elapsed_min": 45, "volume_lb": 5000, "sets_done": {"Squat": 3}, **over}


def _seed_plan(root, domain="workout", date="2026-06-19", plan=None, specialist="personal-trainer"):
    plan_schema.record_plan(domain, plan or _workout_plan(), date, specialist, root)


# --- AC1: the measure production caller -----------------------------------------


def test_record_tracking_no_plan_to_track_records_nothing(tmp_path):
    # CORE honest boundary (mutation surface): a domain with NO recorded plan has nothing to have been
    # done — tracking it would fabricate an adherence surface. record_tracking records nothing.
    # Removing the plan-existence gate would record here -> this test goes RED (the mutation proof).
    r = record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)
    assert r["state"] == NO_PLAN_TO_TRACK
    assert r["recorded"] is False
    assert r["plan_date"] is None
    assert plan_schema.read_plan_tracking("workout", "2026-06-19", tmp_path) is None  # nothing written


def test_record_tracking_records_against_existing_plan(tmp_path):
    _seed_plan(tmp_path)
    r = record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)
    assert r["state"] == RECORDED and r["recorded"] is True
    assert r["plan_date"] == "2026-06-19"
    snap = plan_schema.read_plan_tracking("workout", "2026-06-19", tmp_path)
    assert snap["volume_lb"] == 5000  # the snapshot landed


def test_record_tracking_untracked_domain_raises(tmp_path):
    # peptides is a PLAN domain but NOT a tracked domain (peptide tracking IS the watch-out stream).
    with pytest.raises(ValueError) as exc:
        record_tracking("peptides", {"taken": []}, "2026-06-19", tmp_path)
    assert "untracked" in str(exc.value)
    assert store.items(root=tmp_path) == []


def test_record_tracking_malformed_snapshot_raises_loud(tmp_path):
    # A malformed snapshot fails loud through record_plan_tracking (never a silent drop).
    _seed_plan(tmp_path)
    with pytest.raises(ValueError):
        record_tracking("workout", {"volume_lb": -5}, "2026-06-19", tmp_path)  # negative -> rejected
    assert plan_schema.read_plan_tracking("workout", "2026-06-19", tmp_path) is None


# --- AC2: the adjust read-back (plan-vs-actual join) -----------------------------


def test_progress_pairs_plan_and_tracking(tmp_path):
    _seed_plan(tmp_path)
    record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)
    prog = resolve_plan_progress("workout", "2026-06-19", tmp_path)
    assert prog["has_plan"] is True and prog["has_tracking"] is True
    assert prog["plan"]["exercises"][0]["name"] == "Squat"  # the prescription
    assert prog["tracking"]["volume_lb"] == 5000  # the actual
    assert prog["specialist"] == "personal-trainer"
    assert prog["plan_date"] == "2026-06-19"


def test_progress_no_plan_is_honest_absence(tmp_path):
    prog = resolve_plan_progress("workout", "2026-06-19", tmp_path)
    assert prog["has_plan"] is False and prog["has_tracking"] is False
    assert prog["plan"] is None and prog["tracking"] is None  # never an invented plan/snapshot


def test_progress_plan_without_tracking_is_plan_only(tmp_path):
    _seed_plan(tmp_path)  # plan, but the operator has not logged tracking yet
    prog = resolve_plan_progress("workout", "2026-06-19", tmp_path)
    assert prog["has_plan"] is True and prog["has_tracking"] is False
    assert prog["plan"] is not None and prog["tracking"] is None  # plan-only, no fabricated snapshot


def test_progress_untracked_domain_raises(tmp_path):
    with pytest.raises(ValueError):
        resolve_plan_progress("peptides", "2026-06-19", tmp_path)


# --- AC3: store-adversarial battery for the new write/read surface ---------------


def test_adversarial_cross_stream_isolation(tmp_path):
    # CATEGORY 1: the measure write + the progress read are DOMAIN-SCOPED — workout's tracking/progress
    # never returns nutrition's plan or tracking, and vice versa (the S41 read_panel fabricated-value
    # class). Seed distinct plans + tracking for two domains; assert no cross-read in either direction.
    _seed_plan(tmp_path, domain="workout", plan={"exercises": [{"name": "Squat", "sets": 3}]})
    _seed_plan(tmp_path, domain="nutrition", specialist="nutritionist",
               plan={"calorie_goal": 2600, "macros": {"protein": 180, "carbs": 300, "fat": 80},
                     "meals": [{"name": "Breakfast", "contents": "eggs", "kcal": 650}]})
    record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)
    record_tracking("nutrition", {"food_kcal": 2550}, "2026-06-19", tmp_path)
    wk = resolve_plan_progress("workout", "2026-06-19", tmp_path)
    nut = resolve_plan_progress("nutrition", "2026-06-19", tmp_path)
    assert "exercises" in wk["plan"] and "calorie_goal" not in wk["plan"]  # workout sees only workout's plan
    assert wk["tracking"]["volume_lb"] == 5000 and "food_kcal" not in wk["tracking"]  # only workout's tracking
    assert "calorie_goal" in nut["plan"] and "exercises" not in nut["plan"]  # nutrition sees only nutrition's
    assert nut["tracking"]["food_kcal"] == 2550 and "volume_lb" not in nut["tracking"]


def test_adversarial_same_snapshot_idempotent_distinct_persist(tmp_path):
    # CATEGORY 2/3: an identical re-record at the same date is an idempotent no-op (content-tag dedupe);
    # a DISTINCT same-date snapshot persists (both readings present, the latest wins on resolve).
    _seed_plan(tmp_path)
    record_tracking("workout", _wk_tracking(volume_lb=5000), "2026-06-19", tmp_path)
    record_tracking("workout", _wk_tracking(volume_lb=5000), "2026-06-19", tmp_path)  # identical -> no-op
    assert len(store.read("plan-track::workout", root=tmp_path)) == 1
    record_tracking("workout", _wk_tracking(volume_lb=5200), "2026-06-19", tmp_path)  # distinct -> persists
    raw = store.read("plan-track::workout", root=tmp_path)
    assert len(raw) == 2  # both distinct snapshots stored
    assert resolve_plan_progress("workout", "2026-06-19", tmp_path)["tracking"]["volume_lb"] == 5200  # latest wins


def test_adversarial_mutation_no_plan_gate_is_load_bearing(tmp_path, monkeypatch):
    # CATEGORY 4 (mutation-style): break the plan-existence gate — force read_plan to always report a
    # plan present — and a no-plan domain would then record tracking against a non-existent plan
    # (fabricated adherence). The no-plan-to-track boundary goes RED under the mutation, proving the
    # gate is load-bearing, not tautological.
    monkeypatch.setattr(
        plan_schema, "read_plan",
        lambda domain, on_date, root: {"state": None, "plan": {}, "specialist": "x", "plan_date": on_date},
    )
    r = record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)  # no real plan seeded
    assert r["state"] == RECORDED  # MUTATION: the gate is bypassed -> it records against a phantom plan
    assert plan_schema.read_plan_tracking("workout", "2026-06-19", tmp_path) is not None


# --- AC4: the closed-loop E2E through the production path ------------------------


def test_closed_loop_e2e_plan_measure_progress(tmp_path):
    # plan -> measure -> adjust-read: record a plan via the EXISTING generate_plan production path,
    # record_tracking what was actually done against it, then resolve_plan_progress shows plan-vs-actual.
    from scripts.plan.generate_plan import generate_plan
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3))
    res = generate_plan("workout", author, store_read, tmp_path, plan_date="2026-06-19")
    assert res["recorded"] is True  # the plan leg recorded a real plan through the production path

    measured = record_tracking("workout", _wk_tracking(elapsed_min=50), "2026-06-19", tmp_path)
    assert measured["recorded"] is True  # the measure leg recorded against that plan

    prog = resolve_plan_progress("workout", "2026-06-19", tmp_path)  # the adjust read-back
    assert prog["has_plan"] and prog["has_tracking"]  # the loop closed: plan + actual paired
    assert prog["tracking"]["elapsed_min"] == 50
    assert prog["plan"] is not None


# --- Tier-2: the NO_PLAN_TODAY seam + gate-precedence + append-order coverage -----


def test_record_tracking_no_plan_today_is_no_plan_to_track(tmp_path):
    # Tier-2 (plan-integrity SF-1 / QA): a plan on file but NOT dated on_date (NO_PLAN_TODAY) is NOT a
    # plan to track against on_date — tracking is same-date (no carry-forward). Recording today's
    # adherence against an off-date plan would attribute it to a plan that did not govern today.
    _seed_plan(tmp_path, date="2026-06-15")  # plan dated earlier than the tracking date
    r = record_tracking("workout", _wk_tracking(), "2026-06-19", tmp_path)
    assert r["state"] == NO_PLAN_TO_TRACK and r["recorded"] is False
    assert r["plan_date"] is None
    assert plan_schema.read_plan_tracking("workout", "2026-06-19", tmp_path) is None  # nothing recorded


def test_progress_no_plan_today_has_plan_false_no_contradiction(tmp_path):
    # Tier-2: NO_PLAN_TODAY (a plan dated 06-15, progress for 06-19) -> has_plan False with plan None
    # (no has_plan-True-but-plan-None contradiction); plan_date carries the latest on-file date.
    _seed_plan(tmp_path, date="2026-06-15")
    prog = resolve_plan_progress("workout", "2026-06-19", tmp_path)
    assert prog["has_plan"] is False  # no plan FOR 06-19
    assert prog["plan"] is None  # consistent: has_plan False <-> plan None
    assert prog["plan_date"] == "2026-06-15"  # informational: a plan exists on file, just not for the date


def test_record_tracking_no_plan_gate_precedes_snapshot_validation(tmp_path):
    # Tier-2 (QA): gate precedence — a malformed snapshot for a domain with NO plan for the date returns
    # the no-plan-to-track boundary (records nothing), it does NOT raise. There is no plan to track
    # against, so the snapshot is never validated. (Contrast: malformed WITH a plan raises — covered above.)
    r = record_tracking("workout", {"volume_lb": -5}, "2026-06-19", tmp_path)  # no plan seeded + malformed
    assert r["state"] == NO_PLAN_TO_TRACK and r["recorded"] is False


def test_record_tracking_latest_of_three_same_date_snapshots_wins(tmp_path):
    # Tier-2 (QA): append-order latest-wins beyond N=2 — three distinct same-date snapshots, the latest
    # appended resolves through the progress join (exercises resolve_tracking's reversed-scan past N=2).
    _seed_plan(tmp_path)
    for vol in (5000, 5200, 5400):
        record_tracking("workout", _wk_tracking(volume_lb=vol), "2026-06-19", tmp_path)
    assert len(store.read("plan-track::workout", root=tmp_path)) == 3  # all three distinct persisted
    assert resolve_plan_progress("workout", "2026-06-19", tmp_path)["tracking"]["volume_lb"] == 5400


def test_record_tracking_supplements_domain(tmp_path):
    # Tier-2 (QA domain parity): the supplements tracked domain records + reads back like workout.
    _seed_plan(tmp_path, domain="supplements",
               plan={"items": [{"name": "Creatine", "dose": "5 g"}]}, specialist="supplement-specialist")
    r = record_tracking("supplements", {"taken": ["Creatine"]}, "2026-06-19", tmp_path)
    assert r["state"] == RECORDED
    prog = resolve_plan_progress("supplements", "2026-06-19", tmp_path)
    assert prog["has_plan"] and prog["tracking"]["taken"] == ["Creatine"]
