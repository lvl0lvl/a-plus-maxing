"""Tests for scripts/store/queue_schema.py — the doctor-visit-queue store schema.

The schema writes THROUGH scripts/store/store.py (append/read) and the keying.py Line Field Set;
it defines no second key and reimplements no store I/O. This suite carries the mandatory
store-adversarial battery (docs/checklists/store-adversarial-tests.md): cross-stream namespace
collision, same-timepoint dedupe, dedupe-key boundary, and a mutation-style test that ran RED
during the build (the per-test docstrings name the mutation). Plus the writer boundary guards,
the cumulative latest-per-finding resolution, and the severity ranking.
"""

import pytest

from scripts.store import plan_schema, queue_schema, store


def _entry(finding_id, *, band=None, non_overridable=False, **extra):
    """A minimal queue entry carrying the required finding_id + the severity-rank signals."""
    return {"finding_id": finding_id, "composite_band": band,
            "non_overridable": non_overridable, "caution": "c", **extra}


# --- writer boundary guards ----------------------------------------------------


@pytest.mark.parametrize("bad_date", ["not-a-date", "2026-13-01", "2026-06-31", "", "20260619"])
def test_record_malformed_date_raises_and_writes_nothing(tmp_path, bad_date):
    with pytest.raises(ValueError) as exc:
        queue_schema.record_doctor_visit_queue_entry(_entry("rx-bpmh:x"), bad_date, tmp_path)
    assert "date" in str(exc.value)
    assert store.items(root=tmp_path) == []


@pytest.mark.parametrize("bad_entry", [{}, {"finding_id": ""}, {"finding_id": "   "},
                                        {"finding_id": None}, {"finding_id": 5}])
def test_record_missing_finding_id_raises_and_writes_nothing(tmp_path, bad_entry):
    with pytest.raises(ValueError) as exc:
        queue_schema.record_doctor_visit_queue_entry(bad_entry, "2026-06-19", tmp_path)
    assert "finding_id" in str(exc.value)
    assert store.items(root=tmp_path) == []


def test_round_trip_and_extras_preserved(tmp_path):
    e = _entry("rx-bpmh:supplements:bleeding-risk", band="HIGH", grade={"certainty": "moderate"})
    queue_schema.record_doctor_visit_queue_entry(e, "2026-06-19", tmp_path)
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert len(queue) == 1
    assert queue[0]["finding_id"] == "rx-bpmh:supplements:bleeding-risk"
    assert queue[0]["grade"] == {"certainty": "moderate"}  # entries open on extras (liaison annotation)


def test_empty_queue_is_empty_list(tmp_path):
    assert queue_schema.read_doctor_visit_queue(tmp_path) == []  # absence, never an invented entry


# --- severity ranking ----------------------------------------------------------


def test_severity_rank_non_overridable_then_high_then_medium(tmp_path):
    # A non-overridable auto-block (CRITICAL/H1-H2 — the warfarin watchlist class) leads; HIGH; MEDIUM.
    queue_schema.record_doctor_visit_queue_entry(_entry("a:medium", band="MEDIUM"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("c:crit", band="CRITICAL", non_overridable=True), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("b:high", band="HIGH"), "2026-06-19", tmp_path)
    ranked = queue_schema.read_doctor_visit_queue(tmp_path)
    assert [e["finding_id"] for e in ranked] == ["c:crit", "b:high", "a:medium"]


def test_severity_rank_unknown_band_last_and_deterministic(tmp_path):
    # A None/unknown band ranks after the known bands; ties within a tier break by finding_id.
    queue_schema.record_doctor_visit_queue_entry(_entry("z:unknown", band=None), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("m:high", band="HIGH"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("a:high", band="HIGH"), "2026-06-19", tmp_path)
    ranked = queue_schema.read_doctor_visit_queue(tmp_path)
    assert [e["finding_id"] for e in ranked] == ["a:high", "m:high", "z:unknown"]  # high tier sorted, unknown last


def test_cumulative_latest_record_per_finding_wins(tmp_path):
    # The queue is cumulative across dates; a finding re-collated on a LATER date supersedes its
    # earlier entry (the latest record per finding_id wins on resolve).
    queue_schema.record_doctor_visit_queue_entry(_entry("f:1", band="MEDIUM", outcome="block-stands"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("f:1", band="MEDIUM", outcome="cleared-with-override"), "2026-06-20", tmp_path)
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert len(queue) == 1  # one finding, latest record
    assert queue[0]["outcome"] == "cleared-with-override"  # the 06-20 record supersedes the 06-19 one


# --- store-adversarial battery (docs/checklists/store-adversarial-tests.md) -----


def test_adversarial_cross_stream_namespace_collision(tmp_path):
    # CATEGORY 1: a read for the queue must never return another stream's value. `dvq::queue` and a
    # `plan::workout` document sharing a date do not cross-read (the S41 read_panel fabricated-value
    # class — stream namespacing exists because that escaped to Tier-3).
    queue_schema.record_doctor_visit_queue_entry(_entry("rx-bpmh:x", band="HIGH"), "2026-06-19", tmp_path)
    plan_schema.record_plan("workout", {"exercises": [{"name": "Squat", "sets": 3}]},
                            "2026-06-19", "personal-trainer", tmp_path)
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert len(queue) == 1 and queue[0]["finding_id"] == "rx-bpmh:x"  # only the queue entry
    assert "exercises" not in queue[0]  # the plan document never crossed into the queue read
    # and the reverse: the plan read never returns the queue entry
    assert "rx-bpmh" not in str(store.read("plan::workout", root=tmp_path))


def test_adversarial_same_timepoint_distinct_persist_and_idempotent(tmp_path):
    # CATEGORY 2: two DISTINCT findings at the same date both persist (distinct finding_id = distinct
    # source); an IDENTICAL re-record at the same date is an idempotent no-op (the S41 carry-forward
    # dropped-contraindication class — both-must-persist is the safety property).
    queue_schema.record_doctor_visit_queue_entry(_entry("finding:a", band="HIGH"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("finding:b", band="HIGH"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("finding:a", band="HIGH"), "2026-06-19", tmp_path)  # dup
    raw = store.read("dvq::queue", root=tmp_path)
    assert len(raw) == 2  # both distinct findings persisted; the duplicate dropped
    assert {r["source"] for r in raw} == {"finding:a", "finding:b"}


def test_adversarial_dedupe_key_boundary_each_field(tmp_path):
    # CATEGORY 3: the dedupe identity is (item, timepoint, source=finding_id); value is EXCLUDED.
    # Same key + DIFFERENT value collides on normal ingest (second dropped, by design); ANY single
    # field differing does not collide.
    queue_schema.record_doctor_visit_queue_entry(_entry("f:1", band="HIGH", caution="first"), "2026-06-19", tmp_path)
    # same (item, date, finding_id), different value -> dropped (dedupe excludes value)
    queue_schema.record_doctor_visit_queue_entry(_entry("f:1", band="HIGH", caution="SECOND"), "2026-06-19", tmp_path)
    assert len(store.read("dvq::queue", root=tmp_path)) == 1
    assert store.read("dvq::queue", root=tmp_path)[0]["value"]["caution"] == "first"  # first wins, not overwritten
    # differing finding_id (source) -> persists
    queue_schema.record_doctor_visit_queue_entry(_entry("f:2", band="HIGH"), "2026-06-19", tmp_path)
    # differing timepoint -> persists
    queue_schema.record_doctor_visit_queue_entry(_entry("f:1", band="HIGH"), "2026-06-20", tmp_path)
    assert len(store.read("dvq::queue", root=tmp_path)) == 3


def test_adversarial_mutation_constant_source_collapses_distinct_findings(tmp_path, monkeypatch):
    # CATEGORY 4 (mutation-style): break the keying — record under a CONSTANT source instead of the
    # per-finding finding_id. Distinct findings then collide on (item, date, constant) and the second
    # is dropped. The distinct-persist property goes RED under the mutation, proving the battery is
    # non-tautological (a green battery under this mutation would not test the keying at all).
    real_reading = queue_schema._reading

    def _broken_reading(item, timepoint, source, value):
        return real_reading(item, timepoint, "CONSTANT", value)  # collapse all sources

    monkeypatch.setattr(queue_schema, "_reading", _broken_reading)
    queue_schema.record_doctor_visit_queue_entry(_entry("finding:a", band="HIGH"), "2026-06-19", tmp_path)
    queue_schema.record_doctor_visit_queue_entry(_entry("finding:b", band="HIGH"), "2026-06-19", tmp_path)
    raw = store.read("dvq::queue", root=tmp_path)
    assert len(raw) == 1  # MUTATION RED: the two distinct findings collapsed to one under the constant source
