"""Tests for scripts/store/calendar_schema.py — the calendar-event store schema.

Writes THROUGH store.py (append) on the keying.py Line Field Set, content-tagged
(the plan-track pattern); defines no second key, reuses loop_schema's reading +
content-tag. Asserts writer validation, date-grouped resolution, the same-date
distinct-events / idempotent-re-entry split, and the store-adversarial battery
(cross-stream isolation, content-tag dedupe, dedupe-key boundary). The mutation
battery ran RED during the build — see the per-test docstrings naming the mutation.
"""

import pytest

from scripts.store import calendar_schema, loop_schema, store


def _ev(category="lab-draw", label="Fasting panel"):
    """The event value dict, in record_event's field order (for content-tag parity)."""
    return {"category": category, "label": label}


# --- writer validation ---


@pytest.mark.parametrize("bad_cat", ["bogus", "", "Training", "lab_draw"])
def test_record_event_unknown_category_raises(tmp_path, bad_cat):
    """Only the four signed categories are accepted (each is also a pill tint name)."""
    with pytest.raises(ValueError):
        calendar_schema.record_event(bad_cat, "x", "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_label", ["", 5, None])
def test_record_event_bad_label_raises(tmp_path, bad_label):
    with pytest.raises(ValueError):
        calendar_schema.record_event("training", bad_label, "2026-06-10", tmp_path)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_date", ["2026-6-10", "06-10-2026", "2026-13-01", "soon", ""])
def test_record_event_malformed_date_raises(tmp_path, bad_date):
    """Date-only by contract: the render matches on date.isoformat(), so a bad date
    would silently never land in a cell — rejected at the writer."""
    with pytest.raises(ValueError):
        calendar_schema.record_event("training", "x", bad_date, tmp_path)
    assert store.items(root=tmp_path) == []


def test_record_event_round_trips_grouped_by_date(tmp_path):
    calendar_schema.record_event("lab-draw", "Fasting panel", "2026-06-10", tmp_path)
    calendar_schema.record_event("training", "Lower body", "2026-06-12", tmp_path)
    assert calendar_schema.read_events(tmp_path) == {
        "2026-06-10": [{"category": "lab-draw", "label": "Fasting panel"}],
        "2026-06-12": [{"category": "training", "label": "Lower body"}],
    }


def test_all_four_categories_accepted(tmp_path):
    for i, cat in enumerate(calendar_schema.EVENT_CATEGORIES):
        calendar_schema.record_event(cat, f"event {i}", "2026-06-10", tmp_path)
    assert len(calendar_schema.read_events(tmp_path)["2026-06-10"]) == 4


def test_resolve_events_empty_is_empty_dict():
    assert calendar_schema.resolve_events([]) == {}


# --- same-date distinct vs idempotent (checklist category 2) ---


def test_same_date_distinct_events_both_persist(tmp_path):
    """Two DISTINCT same-date events both persist (content-tagged sources).

    The S41 dedupe-drop class. Mutation check: replacing the content tag with a
    constant source turns this RED — the second event collides on the
    (item, timepoint, source) identity and is dropped.
    """
    calendar_schema.record_event("lab-draw", "Fasting panel", "2026-06-10", tmp_path)
    calendar_schema.record_event("appointment", "Dr. Smith", "2026-06-10", tmp_path)
    assert len(store.read("calendar::events", root=tmp_path)) == 2
    assert len(calendar_schema.read_events(tmp_path)["2026-06-10"]) == 2


def test_identical_reentry_is_idempotent(tmp_path):
    """An identical event re-entry (same category+label+date) appends nothing."""
    calendar_schema.record_event("training", "Lower body", "2026-06-12", tmp_path)
    calendar_schema.record_event("training", "Lower body", "2026-06-12", tmp_path)
    assert len(store.read("calendar::events", root=tmp_path)) == 1


def test_same_event_distinct_dates_both_persist(tmp_path):
    """The timepoint field contributes to the identity: same event, two dates persist.

    Mutation check: dropping the timepoint from the dedupe identity collapses the
    two to one — turns this RED.
    """
    calendar_schema.record_event("training", "Lower body", "2026-06-10", tmp_path)
    calendar_schema.record_event("training", "Lower body", "2026-06-12", tmp_path)
    assert len(store.read("calendar::events", root=tmp_path)) == 2
    assert set(calendar_schema.read_events(tmp_path)) == {"2026-06-10", "2026-06-12"}


# --- content-tag derivation (checklist category 3) ---


def test_event_source_is_loop_schema_content_tag(tmp_path):
    """The event source IS loop_schema's content-tag derivation — no second one.

    Mutation check: re-implementing the tag with a different hash/truncation in
    calendar_schema turns this RED.
    """
    calendar_schema.record_event("training", "Lower body", "2026-06-12", tmp_path)
    [reading] = store.read("calendar::events", root=tmp_path)
    assert reading["source"] == loop_schema._content_tag("calendar::", _ev("training", "Lower body"))


# --- cross-stream namespace isolation (checklist category 1) ---


def test_cross_stream_shared_name_never_cross_reads(tmp_path):
    """A bare name shared across the calendar + biomarker streams stays disjoint.

    The S41 fabricated-value class: a calendar read must never return biomarker
    content (and vice versa). Mutation check: dropping the `calendar::` prefix
    (the item becomes `events`) turns this RED — the items set no longer carries
    `calendar::events`.
    """
    calendar_schema.record_event("lab-draw", "Fasting panel", "2026-06-10", tmp_path)
    loop_schema.record_biomarker("events", "2026-06-10", 5, tmp_path)
    assert calendar_schema.read_events(tmp_path) == {
        "2026-06-10": [{"category": "lab-draw", "label": "Fasting panel"}]
    }
    biomarker = loop_schema.read_biomarker("events", root=tmp_path)
    assert [r["value"] for r in biomarker["timepoints"]] == [5]
    assert sorted(store.items(root=tmp_path)) == ["biomarker::events", "calendar::events"]
