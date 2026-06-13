"""Tests for scripts/store/goal_schema.py — the goal-progress store schema.

The schema writes THROUGH scripts/store/store.py (append/correct/read) and the
keying.py Line Field Set; it defines no second key, reimplements no store I/O,
and reuses loop_schema's reading constructor. This suite asserts the writer
validation table, the read-derived direction-agnostic percent (clamped 0-100),
latest-snapshot-wins resolution, the append/correct split (the silent-drop
boundary — RED if `record_goal` ever gains overwrite behavior), and the
store-adversarial checklist batteries (cross-stream isolation, same-key
dedupe / dedupe-key boundary, correction). The mutation battery ran RED during
the build — see the per-test docstrings naming the mutation that turns each red.
"""

import pytest

from scripts.store import goal_schema, loop_schema, store


def _goal(label="Bench 1RM", baseline=225, current=250, target=275, unit="lb"):
    """A minimal valid goal document (an increase goal at 50% by default)."""
    return {
        "label": label,
        "baseline": baseline,
        "current": current,
        "target": target,
        "unit": unit,
    }


# --- writer validation: slug, date, value schema ---


def test_record_goal_empty_slug_raises(tmp_path):
    with pytest.raises(ValueError):
        goal_schema.record_goal("", _goal(), "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_date", ["2026-6-10", "06-10-2026", "2026-13-01", "soon", ""])
def test_record_goal_malformed_date_raises(tmp_path, bad_date):
    with pytest.raises(ValueError):
        goal_schema.record_goal("bench-1rm", _goal(), bad_date, tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize(
    "mutate",
    [
        lambda g: g.pop("label"),                  # missing required label
        lambda g: g.update(label=""),              # empty label
        lambda g: g.update(label=5),               # non-str label
        lambda g: g.pop("target"),                 # missing required target
        lambda g: g.update(current="lots"),        # non-number current
        lambda g: g.update(baseline=True),         # bool is not a number
        lambda g: g.update(unit=5),                # non-str unit
    ],
)
def test_record_goal_schema_violation_raises(tmp_path, mutate):
    goal = _goal()
    mutate(goal)
    with pytest.raises(ValueError):
        goal_schema.record_goal("bench-1rm", goal, "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


def test_record_goal_baseline_equals_target_raises(tmp_path):
    """No progress span to measure across — and the percent would be undefined."""
    with pytest.raises(ValueError):
        goal_schema.record_goal(
            "at-target", _goal(baseline=12, current=12, target=12), "2026-06-10", tmp_path
        )
    assert store.items(root=tmp_path) == []


def test_record_goal_valid_round_trips(tmp_path):
    goal_schema.record_goal("bench-1rm", _goal(), "2026-06-10", tmp_path)
    resolved = goal_schema.read_goal("bench-1rm", tmp_path)
    assert resolved["label"] == "Bench 1RM"
    assert resolved["percent"] == 50.0
    assert (resolved["baseline"], resolved["current"], resolved["target"]) == (225, 250, 275)
    assert resolved["unit"] == "lb"
    assert resolved["on_date"] == "2026-06-10"


def test_record_goal_extra_keys_permitted_and_preserved(tmp_path):
    """Open on extras (the ADR-0006-T2 forward-compat seam): unknown keys persist."""
    goal = _goal()
    goal["note"] = "stretch goal"
    goal_schema.record_goal("bench-1rm", goal, "2026-06-10", tmp_path)
    [reading] = store.read("goal::bench-1rm", root=tmp_path)
    assert reading["value"]["note"] == "stretch goal"


def test_record_goal_unit_optional(tmp_path):
    goal = _goal()
    del goal["unit"]
    goal_schema.record_goal("hrv", goal, "2026-06-10", tmp_path)
    assert goal_schema.read_goal("hrv", tmp_path)["unit"] is None


# --- read-derived percent: direction-agnostic, clamped ---


def test_percent_increase_and_decrease_are_direction_agnostic(tmp_path):
    """An increase goal and a decrease goal both halfway across read 50%."""
    goal_schema.record_goal(
        "bench", _goal(baseline=225, current=250, target=275), "2026-06-10", tmp_path
    )
    goal_schema.record_goal(
        "fat", _goal(label="Body fat", baseline=18, current=15, target=12, unit="%"),
        "2026-06-10", tmp_path,
    )
    assert goal_schema.read_goal("bench", tmp_path)["percent"] == 50.0
    assert goal_schema.read_goal("fat", tmp_path)["percent"] == 50.0


def test_percent_clamps_to_floor_and_ceiling(tmp_path):
    """A regression past baseline reads 0% (never negative); overshoot reads 100%."""
    goal_schema.record_goal(
        "regress", _goal(baseline=100, current=90, target=150, unit=""), "2026-06-10", tmp_path
    )
    goal_schema.record_goal(
        "over", _goal(baseline=100, current=200, target=150, unit=""), "2026-06-10", tmp_path
    )
    assert goal_schema.read_goal("regress", tmp_path)["percent"] == 0.0
    assert goal_schema.read_goal("over", tmp_path)["percent"] == 100.0


def test_percent_never_rounds_up_to_a_false_complete():
    """99.95% reads 99.9 (no fabricated "100%"); 100 shows only at true completion.

    The ADR-0009 no-fabricated-completion edge: a sub-completion fraction must not
    round up to a full bar / "100%". Overshoot and true completion still read 100.
    """
    assert goal_schema._percent(0, 0.9995, 1) == 99.9    # 99.95% must NOT read 100
    assert goal_schema._percent(0, 1.0, 1) == 100.0      # true completion
    assert goal_schema._percent(0, 1.5, 1) == 100.0      # overshoot
    assert goal_schema._percent(0, 0.0001, 1) == 0.0     # ~0 reads 0


def test_resolve_goal_latest_snapshot_wins_order_independent():
    """The max-timepoint snapshot wins regardless of list order (not positional)."""
    readings = [
        {"item": "goal::g", "timepoint": "2026-06-08", "source": "goal-progress",
         "value": _goal(current=275)},   # later date, 100%
        {"item": "goal::g", "timepoint": "2026-06-01", "source": "goal-progress",
         "value": _goal(current=250)},   # earlier date, 50% — listed AFTER the later one
    ]
    assert goal_schema.resolve_goal(readings)["percent"] == 100.0
    assert goal_schema.resolve_goal(readings)["on_date"] == "2026-06-08"


def test_resolve_goal_empty_reads_none():
    assert goal_schema.resolve_goal([]) is None


# --- append/correct split (the silent-drop boundary, checklist 2/3) ---


def test_rerecord_changed_value_is_dedupe_noop(tmp_path):
    """A same (slug, date) re-record with a CHANGED value is dropped, not overwritten.

    Mutation check: giving `record_goal` overwrite behavior (e.g. routing it
    through `store.correct`) turns this RED — the 999 current would win.
    """
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    goal_schema.record_goal("bench", _goal(current=999), "2026-06-10", tmp_path)
    assert len(store.read("goal::bench", root=tmp_path)) == 1
    assert goal_schema.read_goal("bench", tmp_path)["current"] == 250


def test_correct_goal_changes_the_read(tmp_path):
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    goal_schema.correct_goal("bench", _goal(current=260), "2026-06-10", tmp_path)
    assert goal_schema.read_goal("bench", tmp_path)["current"] == 260
    assert goal_schema.read_goal("bench", tmp_path)["percent"] == 70.0


def test_correct_goal_keeps_audit_trail_and_rerun_appends_nothing(tmp_path):
    """A correction appends a superseding line (audit trail); a re-run appends 0."""
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    goal_schema.correct_goal("bench", _goal(current=260), "2026-06-10", tmp_path)
    assert len(store._read_lines(store._item_path("goal::bench", tmp_path))) == 2
    goal_schema.correct_goal("bench", _goal(current=260), "2026-06-10", tmp_path)
    assert len(store._read_lines(store._item_path("goal::bench", tmp_path))) == 2


def test_correct_goal_unstored_identity_raises(tmp_path):
    """Correcting a never-stored (slug, date) fails loud (no silent new point)."""
    with pytest.raises(ValueError):
        goal_schema.correct_goal("bench", _goal(), "2026-06-10", tmp_path)


# --- dedupe-key boundary: each field's contribution (checklist 3) ---


def test_dedupe_boundary_single_field_difference_does_not_collide(tmp_path):
    """A different date persists alongside; a same (slug, date) re-record collides.

    Mutation check: dropping the TIMEPOINT from the dedupe identity collapses the
    two dated snapshots into one — turns this RED. (The VALUE field's contribution
    is covered by `test_rerecord_changed_value_is_dedupe_noop`; the SOURCE field's
    by `test_dedupe_source_field_contributes_to_identity` — the goal writer's
    constant source means this test alone cannot exercise those two fields.)
    """
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    goal_schema.record_goal("bench", _goal(current=260), "2026-06-11", tmp_path)
    assert len(store.read("goal::bench", root=tmp_path)) == 2
    # Same (slug, date) again — collides, dropped (the silent-drop boundary):
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    assert len(store.read("goal::bench", root=tmp_path)) == 2


def test_dedupe_source_field_contributes_to_identity(tmp_path):
    """Two readings sharing (item, timepoint) but differing SOURCE both persist.

    The goal writer hardcodes the source (one snapshot per slug+date), so this
    drives `store.append` directly to prove the source field's contribution to
    the `(item, timepoint, source)` dedupe identity (checklist category 3 — the
    field `record_goal` cannot vary). Mutation check: dropping `source` from
    `keying.DEDUPE_FIELDS` collapses the two to one — turns this RED.
    """
    item = "goal::bench"
    store.append(item, loop_schema._reading(item, "2026-06-10", "src-a", _goal(current=250)), root=tmp_path)
    store.append(item, loop_schema._reading(item, "2026-06-10", "src-b", _goal(current=260)), root=tmp_path)
    assert len(store.read(item, root=tmp_path)) == 2


def test_distinct_slugs_same_date_both_persist(tmp_path):
    """Two distinct goals on the same date are distinct items — neither is lost.

    The S41 dedupe-drop class, goal-shaped (checklist category 2): goals key one
    snapshot per slug+date, so distinctness is per-slug. Mutation check: collapsing
    the per-slug item id to a constant would drop the second goal.
    """
    goal_schema.record_goal("bench", _goal(), "2026-06-10", tmp_path)
    goal_schema.record_goal("squat", _goal(label="Squat 1RM"), "2026-06-10", tmp_path)
    assert sorted(store.items(root=tmp_path)) == ["goal::bench", "goal::squat"]
    assert goal_schema.read_goal("bench", tmp_path)["label"] == "Bench 1RM"
    assert goal_schema.read_goal("squat", tmp_path)["label"] == "Squat 1RM"


# --- cross-stream namespace isolation (checklist 1) ---


def test_cross_stream_shared_name_never_cross_reads(tmp_path):
    """A bare name shared across goal / biomarker / panel streams stays disjoint.

    The S41 fabricated-value class: a goal read must never return biomarker or
    panel content (and vice versa). Mutation check: dropping the `goal::` prefix
    constant turns this RED (the goal would collide with the biomarker stream).
    """
    goal_schema.record_goal("ferritin", _goal(label="Ferritin goal"), "2026-06-10", tmp_path)
    loop_schema.record_biomarker("ferritin", "2026-06-10", 80, tmp_path)
    loop_schema.record_pending_panel("ferritin", "2026-06-10", tmp_path)

    assert goal_schema.read_goal("ferritin", tmp_path)["label"] == "Ferritin goal"
    biomarker = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert [r["value"] for r in biomarker["timepoints"]] == [80]
    assert sorted(store.items(root=tmp_path)) == [
        "biomarker::ferritin", "goal::ferritin", "panel::ferritin",
    ]


def test_correction_never_surfaces_in_another_stream(tmp_path):
    """A goal correction stays in the goal stream — never bleeds into biomarker.

    Mutation check: dropping the `goal::` prefix turns this RED (the correction
    would target/append into the biomarker item).
    """
    goal_schema.record_goal("ferritin", _goal(label="Ferritin goal", current=250), "2026-06-10", tmp_path)
    loop_schema.record_biomarker("ferritin", "2026-06-10", 80, tmp_path)
    goal_schema.correct_goal("ferritin", _goal(label="Ferritin goal", current=260), "2026-06-10", tmp_path)
    assert goal_schema.read_goal("ferritin", tmp_path)["current"] == 260
    biomarker = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert [r["value"] for r in biomarker["timepoints"]] == [80]


# --- enumeration ---


def test_read_goals_enumerates_in_slug_order_and_skips_other_streams(tmp_path):
    goal_schema.record_goal("squat", _goal(label="Squat 1RM"), "2026-06-10", tmp_path)
    goal_schema.record_goal("bench", _goal(label="Bench 1RM"), "2026-06-10", tmp_path)
    loop_schema.record_biomarker("bench", "2026-06-10", 5, tmp_path)
    slugs = [slug for slug, _ in goal_schema.read_goals(tmp_path)]
    assert slugs == ["bench", "squat"]
