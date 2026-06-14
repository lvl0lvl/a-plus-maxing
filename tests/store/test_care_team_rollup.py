"""Tests for scripts/store/care_team_rollup.py — the zone-5 freshness read-model.

`care_team_rollup` is a READ-MODEL over the store readings (no write path, no new
keyed stream), so the store-adversarial battery's write-side categories
(same-timepoint dedupe, dedupe-key boundary) do not apply — there is no dedupe
identity to collide. The two applicable categories ARE exercised, plus the
read-model's own boundary analogue:

  * cross-stream isolation — a reading routes to AT MOST ONE specialist by its
    stream prefix / calendar category; no namespace leak (`test_cross_stream_*`).
  * 30/60-day threshold boundary — the freshness bands keyed at exactly 30 and 60
    days (`test_freshness_band_boundaries`).
  * mutation-style verification — the threshold + mapping tests FAIL when the
    rule is broken; the per-test docstrings name the mutation. Both mutations
    were run RED during the build (CURRENT_MAX_DAYS=999 reds the band test; a
    removed `plan::workout` prefix reds the cross-stream + mapping tests) and
    reverted.

Timepoints are reduced to their nominal calendar date via the house parser, so
the tests mix the date-only (plan/calendar) and full-datetime (loop) forms the
real streams use.
"""
import datetime

import pytest

from scripts.store import calendar_schema, care_team_rollup, loop_schema, store

_TODAY = datetime.date(2026, 6, 10)


def _day(n):
    """The ISO date `n` days before _TODAY (date-only form, plan/calendar style)."""
    return (_TODAY - datetime.timedelta(days=n)).isoformat()


def _dt(n):
    """The full-datetime timepoint `n` days before _TODAY (loop-stream style)."""
    return f"{_day(n)}T00:00:00+00:00"


def _r(item, timepoint, value=1):
    """A store reading dict, the shape `store.read_all` returns."""
    return {"item": item, "timepoint": timepoint, "source": "t", "value": value}


# --- mapping: each mapped stream routes to its owning specialist ---

@pytest.mark.parametrize("item, slug", [
    ("plan::workout", "personal-trainer"),
    ("plan-track::workout", "personal-trainer"),
    ("plan::nutrition", "nutritionist"),
    ("plan::supplements", "supplement-specialist"),
    ("plan::peptides", "peptide-specialist"),
    ("watch-out::sides", "peptide-specialist"),
    ("panel::cbc", "labs-specialist"),
    ("biomarker::ldl", "labs-specialist"),
    ("feedback::physician-feedback", "medical-liaison"),
])
def test_each_mapped_stream_routes_to_its_specialist(item, slug):
    """The specialist→stream mapping (decision 2026-06-13): a reading under each
    mapped prefix attributes to exactly that specialist.

    Mutation-RED: removing the prefix from `SPECIALIST_STREAMS[slug]` drops the
    specialist from the result — reds this test."""
    rollup = care_team_rollup.resolve_rollup([_r(item, _day(0))], _TODAY)
    assert rollup == {slug: {"state": "current", "days": 0}}


@pytest.mark.parametrize("category, slug", [
    ("training", "personal-trainer"),
    ("lab-draw", "labs-specialist"),
    ("appointment", "medical-liaison"),
    ("check-in", "medical-liaison"),
])
def test_calendar_event_routes_by_category(category, slug):
    """A `calendar::events` reading attributes by its value category, not a prefix.

    Mutation-RED: re-pointing a category in `SPECIALIST_STREAMS` reds this."""
    reading = _r("calendar::events", _day(2), value={"category": category, "label": "x"})
    rollup = care_team_rollup.resolve_rollup([reading], _TODAY)
    assert rollup == {slug: {"state": "current", "days": 2}}


# --- freshness bands: the 30/60-day thresholds ---

@pytest.mark.parametrize("days_ago, state", [
    (0, "current"), (30, "current"),      # <= 30 -> current
    (31, "stale"), (60, "stale"),          # 31..60 -> stale
    (61, "dormant"), (400, "dormant"),     # > 60 -> dormant
])
def test_freshness_band_boundaries(days_ago, state):
    """The 30/60-day band edges (decision 2026-06-13 Decision 2). days = today -
    latest; 30 is still current, 31 is stale, 60 is still stale, 61 is dormant.

    Mutation-RED: widening CURRENT_MAX_DAYS (e.g. to 999) reads 31/60/61 as
    `current` — reds the stale/dormant rows. Run RED in build, reverted."""
    rollup = care_team_rollup.resolve_rollup([_r("plan::workout", _day(days_ago))], _TODAY)
    assert rollup["personal-trainer"] == {"state": state, "days": days_ago}


def test_future_timepoint_clamps_to_current():
    """A future-dated reading (an upcoming scheduled event) reads `current`, days
    clamped at 0 — never a negative age."""
    future = (_TODAY + datetime.timedelta(days=12)).isoformat()
    rollup = care_team_rollup.resolve_rollup([_r("calendar::events", future,
        value={"category": "appointment", "label": "MD"})], _TODAY)
    assert rollup["medical-liaison"] == {"state": "current", "days": 0}


def test_latest_timepoint_wins_across_mixed_formats():
    """A specialist's status comes from its MOST-RECENT mapped timepoint, comparing
    correctly across the date-only (plan) and full-datetime (loop/track) forms."""
    readings = [
        _r("plan::workout", _day(45)),               # date-only, older
        _r("plan-track::workout", _dt(1)),           # datetime, newer -> wins
    ]
    rollup = care_team_rollup.resolve_rollup(readings, _TODAY)
    assert rollup["personal-trainer"] == {"state": "current", "days": 1}


# --- absence: streamless / excluded / empty ---

def test_streamless_and_excluded_streams_yield_no_specialist():
    """A specialist with no mapped reading is ABSENT (the render fills 'no data
    yet'); `goal::` and unprefixed items attribute to no specialist (zone 6 owns
    goals; the hero loop readings are zone 1)."""
    readings = [
        _r("goal::bodyweight", _day(0)),
        _r("bodyweight", _dt(0)),
    ]
    assert care_team_rollup.resolve_rollup(readings, _TODAY) == {}
    assert care_team_rollup.resolve_rollup([], _TODAY) == {}


# --- cross-stream isolation (store-adversarial category 1) ---

def test_cross_stream_no_leak_between_specialists():
    """Distinct streams stay isolated: a nutrition plan attributes to nutritionist
    ONLY (never personal-trainer or labs), and a panel to labs ONLY.

    Mutation-RED: pointing `plan::nutrition` at personal-trainer reds this."""
    readings = [_r("plan::nutrition", _day(3)), _r("panel::cbc", _dt(5))]
    rollup = care_team_rollup.resolve_rollup(readings, _TODAY)
    assert rollup == {
        "nutritionist": {"state": "current", "days": 3},
        "labs-specialist": {"state": "current", "days": 5},
    }


def test_cross_stream_isolation_on_real_store_output(tmp_path):
    """End-to-end over real store output (`store.read_all`): a recorded panel and
    a recorded training event route to labs-specialist and personal-trainer
    respectively, and neither leaks into the other's domain (nutritionist absent —
    no nutrition stream was written)."""
    loop_schema.record_pending_panel("cbc", _dt(4), tmp_path)
    calendar_schema.record_event("training", "Leg day", _day(2), tmp_path)
    rollup = care_team_rollup.resolve_rollup(store.read_all(tmp_path), _TODAY)
    assert rollup == {
        "labs-specialist": {"state": "current", "days": 4},
        "personal-trainer": {"state": "current", "days": 2},
    }


# --- malformed timepoints: the house honest-absence degrade (no crash) ---

@pytest.mark.parametrize("bad_timepoint", ["when it settles", "", None, 5])
def test_unparseable_timepoint_is_skipped_not_crashed(bad_timepoint):
    """An unparseable or non-string timepoint contributes nothing (the same
    honest-absence degrade as `component_set.reading_date`), never a crash — and a
    parseable sibling reading still wins."""
    readings = [
        _r("plan::workout", bad_timepoint),
        _r("plan::workout", _day(10)),
    ]
    rollup = care_team_rollup.resolve_rollup(readings, _TODAY)
    assert rollup["personal-trainer"] == {"state": "current", "days": 10}


def test_all_unparseable_yields_no_specialist():
    """A specialist whose only readings have unparseable timepoints is absent —
    undateable data cannot establish recency, so it degrades to 'no data yet'."""
    assert care_team_rollup.resolve_rollup([_r("plan::workout", "soon")], _TODAY) == {}
