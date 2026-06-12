"""Tests for scripts/store/plan_schema.py — plan-content / plan-tracking schemas.

The schemas write THROUGH scripts/store/store.py (append/correct/read) and the
keying.py Line Field Set; they define no second key, reimplement no store I/O,
and reuse loop_schema's content-tag derivation. This suite asserts the writer
validation tables, the append/correct split (the silent-drop boundary — RED if
`record_plan` ever gains overwrite behavior), the two published absence states,
latest-appended-wins resolution, the `{"taken": []}` vs no-snapshot distinction,
and the store-adversarial checklist batteries (cross-stream, dedupe-collision,
correction; the mutation battery ran RED during the build — see the per-test
docstrings naming their mutation).
"""

import pytest

from scripts.store import loop_schema, plan_schema, store


def _workout_plan():
    """A minimal valid workout plan document."""
    return {
        "exercises": [
            {"name": "Bench Press", "sets": 3, "load": "185 lb", "reps": 8},
            {"name": "Squat", "sets": 4},
        ]
    }


def _nutrition_plan():
    """A minimal valid nutrition plan document."""
    return {
        "calorie_goal": 2800,
        "macros": {"protein": 180, "carbs": 300, "fat": 80},
        "meals": [{"name": "Breakfast", "contents": "eggs, oats", "kcal": 650}],
    }


def _supplements_plan():
    """A minimal valid supplements plan document."""
    return {"items": [{"name": "Creatine", "dose": "5 g", "timing": "AM"}]}


def _peptides_plan():
    """A minimal valid peptides plan document."""
    return {"compound": "bpc-157", "dose": "250 mcg", "route": "subq"}


_VALID_PLANS = {
    "workout": _workout_plan,
    "nutrition": _nutrition_plan,
    "supplements": _supplements_plan,
    "peptides": _peptides_plan,
}


# --- writer validation: domains, dates, specialist ---


def test_record_plan_unknown_domain_raises_and_writes_nothing(tmp_path):
    """A domain outside PLAN_DOMAINS ValueErrors; the store stays empty."""
    with pytest.raises(ValueError, match="cardio"):
        plan_schema.record_plan("cardio", _workout_plan(), "2026-06-10", "coach", tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_date", [
    "06/10/2026",            # wrong shape
    "2026-6-1",              # unpadded
    "2026-06-10T00:00:00+00:00",  # datetime, not date-only
    "2026-02-30",            # not a real calendar date
    "",                      # empty
    None,                    # not a str
])
def test_record_plan_malformed_date_raises(tmp_path, bad_date):
    """A non-YYYY-MM-DD plan_date ValueErrors — date equality IS today-resolution."""
    with pytest.raises(ValueError):
        plan_schema.record_plan("workout", _workout_plan(), bad_date, "coach", tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_specialist", ["", None, 7])
def test_record_plan_empty_specialist_raises(tmp_path, bad_specialist):
    """An empty/non-str specialist ValueErrors — attribution is required (D1)."""
    with pytest.raises(ValueError, match="specialist"):
        plan_schema.record_plan(
            "workout", _workout_plan(), "2026-06-10", bad_specialist, tmp_path
        )


def test_record_plan_tracking_untracked_domain_raises(tmp_path):
    """Peptide tracking IS the watch-out stream: "peptides" is not trackable here."""
    with pytest.raises(ValueError, match="peptides"):
        plan_schema.record_plan_tracking("peptides", {"taken": []}, "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


def test_record_plan_tracking_malformed_date_raises(tmp_path):
    """The tracking writer runs the same date boundary check as the plan writer."""
    with pytest.raises(ValueError):
        plan_schema.record_plan_tracking("workout", {}, "2026-13-01", tmp_path)


# --- writer validation: per-domain schema tables ---

# (domain, mutate(plan) -> broken plan) for every required-field removal and a
# mistype per table. Built from the valid fixtures so a fixture drift fails here.
_PLAN_BREAKS = [
    ("workout", lambda p: {k: v for k, v in p.items() if k != "exercises"}),
    ("workout", lambda p: p | {"exercises": []}),
    ("workout", lambda p: p | {"exercises": "bench"}),
    ("workout", lambda p: p | {"exercises": [{"sets": 3}]}),                 # no name
    ("workout", lambda p: p | {"exercises": [{"name": "", "sets": 3}]}),     # empty name
    ("workout", lambda p: p | {"exercises": [{"name": "Bench", "sets": 0}]}),
    ("workout", lambda p: p | {"exercises": [{"name": "Bench", "sets": 101}]}),  # above ceiling
    ("workout", lambda p: p | {"exercises": [{"name": "Bench", "sets": True}]}),
    ("workout", lambda p: p | {"exercises": [{"name": "Bench"}]}),           # no sets
    ("workout", lambda p: p | {"exercises": [
        {"name": "Bench", "sets": 3}, {"name": "Bench", "sets": 2}]}),       # duplicate name
    ("workout", lambda p: p | {"exercises": [{"name": "Bench", "sets": 3, "load": 185}]}),
    ("workout", lambda p: p | {"exercises": [{"name": "Bench", "sets": 3, "reps": 1.5}]}),
    ("nutrition", lambda p: {k: v for k, v in p.items() if k != "calorie_goal"}),
    ("nutrition", lambda p: p | {"calorie_goal": 0}),
    ("nutrition", lambda p: p | {"calorie_goal": "2800"}),
    ("nutrition", lambda p: {k: v for k, v in p.items() if k != "macros"}),
    ("nutrition", lambda p: p | {"macros": {"protein": 180, "carbs": 300}}),  # fat missing
    ("nutrition", lambda p: p | {"macros": {"protein": 180, "carbs": 300, "fat": 0}}),
    ("nutrition", lambda p: {k: v for k, v in p.items() if k != "meals"}),
    ("nutrition", lambda p: p | {"meals": []}),
    ("nutrition", lambda p: p | {"meals": [{"kcal": 650}]}),                 # no name
    ("nutrition", lambda p: p | {"meals": [{"name": "Lunch", "kcal": "650"}]}),
    ("nutrition", lambda p: p | {"meals": [{"name": "Lunch"}, {"name": "Lunch"}]}),  # duplicate name
    ("nutrition", lambda p: p | {"water_l": 0}),
    ("supplements", lambda p: {k: v for k, v in p.items() if k != "items"}),
    ("supplements", lambda p: p | {"items": []}),
    ("supplements", lambda p: p | {"items": [{"dose": "5 g"}]}),             # no name
    ("supplements", lambda p: p | {"items": [{"name": "Creatine"}]}),        # no dose
    ("supplements", lambda p: p | {"items": [{"name": "Creatine", "dose": 5}]}),
    ("supplements", lambda p: p | {"items": [
        {"name": "Creatine", "dose": "5 g"}, {"name": "Creatine", "dose": "10 g"}]}),  # duplicate name
    ("peptides", lambda p: {k: v for k, v in p.items() if k != "compound"}),
    ("peptides", lambda p: p | {"compound": ""}),
    ("peptides", lambda p: {k: v for k, v in p.items() if k != "dose"}),
    ("peptides", lambda p: {k: v for k, v in p.items() if k != "route"}),
    ("peptides", lambda p: p | {"cycle_week": 0}),
    ("peptides", lambda p: p | {"cycle_length_weeks": "8"}),
    ("peptides", lambda p: p | {"tags": ["a", 1]}),
    ("peptides", lambda p: p | {"evidence": 7}),
]


@pytest.mark.parametrize("domain, mutate", _PLAN_BREAKS)
def test_record_plan_schema_violation_raises(tmp_path, domain, mutate):
    """Each missing/mistyped required field (and mistyped optional) ValueErrors."""
    with pytest.raises(ValueError):
        plan_schema.record_plan(
            domain, mutate(_VALID_PLANS[domain]()), "2026-06-10", "coach", tmp_path
        )
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("domain", plan_schema.PLAN_DOMAINS)
def test_record_plan_valid_document_round_trips(tmp_path, domain):
    """A valid plan stores exactly one reading: item/timepoint/source/value."""
    plan = _VALID_PLANS[domain]()
    plan_schema.record_plan(domain, plan, "2026-06-10", "coach", tmp_path)
    readings = store.read(f"plan::{domain}", root=tmp_path)
    assert readings == [{
        "item": f"plan::{domain}", "timepoint": "2026-06-10",
        "source": "plan::coach", "value": plan,
    }]


def test_record_plan_extra_keys_permitted_and_preserved(tmp_path):
    """Unknown extra keys pass validation and persist verbatim (D2 seam)."""
    plan = _workout_plan() | {"focus": "hypertrophy", "rpe_cap": 9}
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    assert plan_schema.read_plan("workout", "2026-06-10", tmp_path)["plan"] == plan


_TRACKING_BREAKS = [
    ("workout", {"elapsed_min": "42"}),
    ("workout", {"elapsed_min": -1}),
    ("workout", {"volume_lb": True}),
    ("workout", {"volume_lb": -0.5}),
    ("workout", {"sets_done": {"Bench": -1}}),
    ("workout", {"sets_done": {"Bench": "2"}}),
    ("workout", {"sets_done": ["Bench"]}),
    ("workout", {"heart_rate_bpm": -1}),
    ("workout", {"steps": 1.5}),
    ("workout", {"steps": -1}),
    ("workout", {"kcal_burned": "520"}),
    ("workout", {"kcal_burned": -1}),
    ("workout", {"exercise_min": None}),
    ("workout", {"exercise_min": -1}),
    ("nutrition", {"food_kcal": "1450"}),
    ("nutrition", {"food_kcal": -1}),
    ("nutrition", {"exercise_kcal": 1.5}),
    ("nutrition", {"exercise_kcal": -1}),
    ("nutrition", {"macros_g": {"protein": "120"}}),
    ("nutrition", {"macros_g": {"protein": -50}}),  # negative grams rejected
    ("nutrition", {"macros_g": {"protien": 120}}),  # typo'd macro key rejected
    ("nutrition", {"meals_logged": "Breakfast"}),
    ("nutrition", {"water_l": "1.5"}),
    ("nutrition", {"water_l": -0.1}),
    ("supplements", {}),                       # taken is REQUIRED
    ("supplements", {"taken": "Creatine"}),
    ("supplements", {"taken": [1]}),
]


@pytest.mark.parametrize("domain, tracking", _TRACKING_BREAKS)
def test_record_plan_tracking_schema_violation_raises(tmp_path, domain, tracking):
    """Each mistyped known tracking field (and a missing `taken`) ValueErrors."""
    with pytest.raises(ValueError):
        plan_schema.record_plan_tracking(domain, tracking, "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


def test_record_plan_tracking_extra_keys_permitted(tmp_path):
    """Unknown extra tracking keys pass validation and persist verbatim (D2 seam)."""
    snapshot = {"taken": ["Creatine"], "mood": "good"}
    plan_schema.record_plan_tracking("supplements", snapshot, "2026-06-10", tmp_path)
    assert plan_schema.read_plan_tracking("supplements", "2026-06-10", tmp_path) == snapshot


# --- append/correct split: the silent-drop boundary ---


def test_rerecord_changed_value_is_dedupe_noop(tmp_path):
    """Re-recording a CHANGED plan for a stored identity leaves the read unchanged.

    The silent-drop boundary (checklist category 2/3): the dedupe identity
    excludes value, so the second write is dropped — the normal record path
    NEVER overrides a stored plan. Mutation check: rewiring `record_plan` to
    overwrite (e.g. through `store.correct`) turns this RED.
    """
    first = _workout_plan()
    plan_schema.record_plan("workout", first, "2026-06-10", "coach", tmp_path)
    changed = {"exercises": [{"name": "Deadlift", "sets": 5}]}
    plan_schema.record_plan("workout", changed, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["plan"] == first, "a re-record must never silently overwrite"
    assert len(store.read("plan::workout", root=tmp_path)) == 1


def test_correct_plan_changes_the_read(tmp_path):
    """correct_plan supersedes: the read resolves to the corrected value."""
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    corrected = {"exercises": [{"name": "Deadlift", "sets": 5}]}
    plan_schema.correct_plan("workout", corrected, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["plan"] == corrected
    assert resolved["specialist"] == "coach"


def test_correct_plan_keeps_audit_trail_and_rerun_appends_nothing(tmp_path):
    """A correction appends (audit trail intact); re-running it appends 0 lines."""
    path = tmp_path / "plan::workout.ndjson"
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    corrected = {"exercises": [{"name": "Deadlift", "sets": 5}]}
    plan_schema.correct_plan("workout", corrected, "2026-06-10", "coach", tmp_path)
    assert len(path.read_text().splitlines()) == 2, "the superseded line stays on disk"
    plan_schema.correct_plan("workout", corrected, "2026-06-10", "coach", tmp_path)
    assert len(path.read_text().splitlines()) == 2, "an idempotent re-correction appends 0"


def test_correct_plan_unstored_identity_raises(tmp_path):
    """Correcting a never-stored (domain, date, specialist) fails loud."""
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    for date, specialist in (
        ("2026-06-11", "coach"),     # different date
        ("2026-06-10", "trainer"),   # different specialist
    ):
        with pytest.raises(ValueError):
            plan_schema.correct_plan("workout", _workout_plan(), date, specialist, tmp_path)
    with pytest.raises(ValueError):
        plan_schema.correct_plan("nutrition", _nutrition_plan(), "2026-06-10", "coach", tmp_path)


def test_correction_never_surfaces_in_another_stream(tmp_path):
    """A plan correction leaves the same-named tracking stream untouched (checklist 3)."""
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    snapshot = {"elapsed_min": 42}
    plan_schema.record_plan_tracking("workout", snapshot, "2026-06-10", tmp_path)
    corrected = {"exercises": [{"name": "Deadlift", "sets": 5}]}
    plan_schema.correct_plan("workout", corrected, "2026-06-10", "coach", tmp_path)
    assert plan_schema.read_plan_tracking("workout", "2026-06-10", tmp_path) == snapshot
    assert plan_schema.read_plan("workout", "2026-06-10", tmp_path)["plan"] == corrected


# --- dedupe-key boundary: each field's contribution (checklist 3) ---


def test_dedupe_boundary_single_field_difference_does_not_collide(tmp_path):
    """A different date OR specialist persists alongside; same key collides.

    Mutation check: widening the dedupe key to include value (both same-key
    plans persist) or dropping the source from the identity (the second
    specialist's plan vanishes) turns this RED.
    """
    base = _workout_plan()
    plan_schema.record_plan("workout", base, "2026-06-10", "coach", tmp_path)
    other_day = {"exercises": [{"name": "Row", "sets": 3}]}
    plan_schema.record_plan("workout", other_day, "2026-06-11", "coach", tmp_path)
    other_specialist = {"exercises": [{"name": "Press", "sets": 2}]}
    plan_schema.record_plan("workout", other_specialist, "2026-06-10", "trainer", tmp_path)
    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 3, "single-field-differing identities all persist"
    # Same key + different value collides: the second write was dropped above
    # (test_rerecord_changed_value_is_dedupe_noop); identical re-entry is a no-op:
    plan_schema.record_plan("workout", base, "2026-06-10", "coach", tmp_path)
    assert len(store.read("plan::workout", root=tmp_path)) == 3


def test_tracking_same_day_distinct_snapshots_both_persist(tmp_path):
    """Two distinct same-day snapshots BOTH persist (content-tagged sources).

    The S41 dedupe-drop class (checklist category 2). Mutation check: replacing
    the content tag with a constant source turns this RED (the second snapshot
    would be dropped and the read would return the first).
    """
    plan_schema.record_plan_tracking("workout", {"elapsed_min": 20}, "2026-06-10", tmp_path)
    plan_schema.record_plan_tracking("workout", {"elapsed_min": 42}, "2026-06-10", tmp_path)
    readings = store.read("plan-track::workout", root=tmp_path)
    assert len(readings) == 2, "distinct same-day snapshots must both persist"
    assert plan_schema.read_plan_tracking("workout", "2026-06-10", tmp_path) == {
        "elapsed_min": 42
    }, "the latest-appended snapshot wins the read"


def test_tracking_identical_reentry_is_idempotent(tmp_path):
    """An identical snapshot re-entry appends nothing (same content tag)."""
    plan_schema.record_plan_tracking("workout", {"elapsed_min": 42}, "2026-06-10", tmp_path)
    plan_schema.record_plan_tracking("workout", {"elapsed_min": 42}, "2026-06-10", tmp_path)
    assert len(store.read("plan-track::workout", root=tmp_path)) == 1


def test_tracking_sources_reuse_loop_schema_content_tag(tmp_path):
    """The tracking source IS loop_schema's content-tag derivation — no second one.

    Mutation check: re-implementing the tag with a different hash/truncation in
    plan_schema turns this RED.
    """
    snapshot = {"elapsed_min": 42}
    plan_schema.record_plan_tracking("workout", snapshot, "2026-06-10", tmp_path)
    [reading] = store.read("plan-track::workout", root=tmp_path)
    assert reading["source"] == loop_schema._content_tag("plan-track::", snapshot)


# --- cross-stream namespace isolation (checklist 1) ---


def test_cross_stream_shared_name_never_cross_reads(tmp_path):
    """A bare name shared across plan / tracking / biomarker streams stays disjoint.

    The S41 fabricated-value class: a plan read must never return tracking or
    biomarker content (and vice versa). Mutation check: dropping either prefix
    constant turns this RED.
    """
    plan = _workout_plan()
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    snapshot = {"elapsed_min": 42}
    plan_schema.record_plan_tracking("workout", snapshot, "2026-06-10", tmp_path)
    loop_schema.record_biomarker("workout", "2026-06-10", 7, tmp_path)

    assert plan_schema.read_plan("workout", "2026-06-10", tmp_path)["plan"] == plan
    assert plan_schema.read_plan_tracking("workout", "2026-06-10", tmp_path) == snapshot
    biomarker = loop_schema.read_biomarker("workout", root=tmp_path)
    assert [r["value"] for r in biomarker["timepoints"]] == [7]
    assert sorted(store.items(root=tmp_path)) == [
        "biomarker::workout", "plan-track::workout", "plan::workout",
    ]


# --- published absence states + resolution ---


def test_resolve_plan_empty_reads_no_plan():
    """Zero readings resolve to the no-plan state with every slot None."""
    assert plan_schema.resolve_plan([], "2026-06-10") == {
        "state": plan_schema.NO_PLAN, "plan": None,
        "specialist": None, "plan_date": None,
    }


def test_resolve_plan_other_dates_reads_no_plan_today(tmp_path):
    """Plans on file but none dated today resolve to no-plan-today + max date."""
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-08", "coach", tmp_path)
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Row", "sets": 3}]},
        "2026-06-09", "coach", tmp_path,
    )
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved == {
        "state": plan_schema.NO_PLAN_TODAY, "plan": None,
        "specialist": None, "plan_date": "2026-06-09",
    }


def test_resolve_plan_today_carries_value_and_attribution(tmp_path):
    """A today-dated plan resolves to its value + the source minus `plan::`."""
    plan = _workout_plan()
    plan_schema.record_plan("workout", plan, "2026-06-10", "strength-coach", tmp_path)
    assert plan_schema.read_plan("workout", "2026-06-10", tmp_path) == {
        "state": None, "plan": plan,
        "specialist": "strength-coach", "plan_date": "2026-06-10",
    }


def test_resolve_plan_same_date_latest_appended_wins(tmp_path):
    """Two same-date plans from different specialists: the last appended wins."""
    first = _workout_plan()
    plan_schema.record_plan("workout", first, "2026-06-10", "coach", tmp_path)
    second = {"exercises": [{"name": "Row", "sets": 3}]}
    plan_schema.record_plan("workout", second, "2026-06-10", "trainer", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["plan"] == second
    assert resolved["specialist"] == "trainer"


def test_readers_never_raise_on_absence(tmp_path):
    """An empty store reads the absence states, never an exception."""
    assert plan_schema.read_plan("peptides", "2026-06-10", tmp_path)["state"] == (
        plan_schema.NO_PLAN
    )
    assert plan_schema.read_plan_tracking("nutrition", "2026-06-10", tmp_path) is None


def test_read_plan_unknown_domain_raises(tmp_path):
    """The domain-keyed readers reject an unknown domain (not an absence case)."""
    with pytest.raises(ValueError, match="cardio"):
        plan_schema.read_plan("cardio", "2026-06-10", tmp_path)
    with pytest.raises(ValueError, match="peptides"):
        plan_schema.read_plan_tracking("peptides", "2026-06-10", tmp_path)


def test_tracking_other_day_snapshot_resolves_none(tmp_path):
    """A snapshot dated yesterday resolves None for today — never carried forward."""
    plan_schema.record_plan_tracking("workout", {"elapsed_min": 42}, "2026-06-09", tmp_path)
    assert plan_schema.read_plan_tracking("workout", "2026-06-10", tmp_path) is None


def test_supplements_empty_taken_distinct_from_no_snapshot(tmp_path):
    """`{"taken": []}` reads as the explicit none-taken snapshot, not None."""
    assert plan_schema.read_plan_tracking("supplements", "2026-06-10", tmp_path) is None
    plan_schema.record_plan_tracking("supplements", {"taken": []}, "2026-06-10", tmp_path)
    assert plan_schema.read_plan_tracking("supplements", "2026-06-10", tmp_path) == {
        "taken": []
    }
