"""Tests for superseding-append correction + latest-wins reads (bead 1vi).

A corrected value re-entered for an already-stored (item, timepoint, source)
used to dedupe away silently (first-write-wins, pinned by PR #47's TEST-006).
The S51-adjudicated fix keeps ADR-0002's append-only substrate: `store.correct`
APPENDS a superseding line for the stored identity (the prior line stays in the
file — the audit trail is never mutated or deleted), and `store.read` resolves
each identity to its last-appended line (latest-wins, the same most-recent-wins
basis `loop_schema.read_panel` resolves by). Normal ingest is untouched:
`store.append` still drops a re-entered identity, value drift included.
"""

import json
from pathlib import Path

import pytest

from scripts.store import keying, loop_schema, store


def _reading(timepoint, value=100, item="rhr", source="manual"):
    """Build a reading carrying every Line Field Set field."""
    return {
        "item": item,
        "timepoint": timepoint,
        "source": source,
        "value": value,
    }


def _item_file(root, item="rhr"):
    return Path(root) / f"{item}.ndjson"


def _line_count(root, item="rhr"):
    path = _item_file(root, item)
    if not path.exists():
        return 0
    return len([ln for ln in path.read_text().splitlines() if ln.strip()])


T1 = "2026-06-01T08:00:00+00:00"
T2 = "2026-06-02T08:00:00+00:00"


# --------------------------------------------------------------------------- #
# Latest-wins read resolution (independent of the correct() writer: the
# superseded state is hand-crafted on disk, so these turn RED against the
# pre-1vi read even with no correction primitive in the codebase).
# --------------------------------------------------------------------------- #


def test_read_resolves_same_identity_to_last_appended_line(tmp_path):
    """Two stored lines sharing (item, timepoint, source): the later line wins."""
    path = _item_file(tmp_path)
    path.write_text(
        json.dumps(_reading(T1, 55)) + "\n" + json.dumps(_reading(T1, 62)) + "\n"
    )

    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 1
    assert readings[0]["value"] == 62


def test_read_resolution_keeps_neighbor_identities_intact(tmp_path):
    """Resolving one identity never bleeds into a neighboring identity.

    The file holds T1 (later superseded), a T2 neighbor, and the T1 correction.
    The T2 neighbor's value and the reading count must survive untouched.
    """
    path = _item_file(tmp_path)
    path.write_text(
        json.dumps(_reading(T1, 55)) + "\n"
        + json.dumps(_reading(T2, 70)) + "\n"
        + json.dumps(_reading(T1, 62)) + "\n"
    )

    readings = store.read("rhr", root=tmp_path)
    assert [r["timepoint"] for r in readings] == [T1, T2]
    assert [r["value"] for r in readings] == [62, 70]


def test_read_all_resolves_latest_per_identity(tmp_path):
    """read_all inherits the resolution: one reading per identity, latest value."""
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    store.append("hrv", _reading(T1, 80, item="hrv"), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)

    flat = store.read_all(tmp_path)
    assert len(flat) == 2
    by_item = {r["item"]: r["value"] for r in flat}
    assert by_item == {"rhr": 62, "hrv": 80}


# --------------------------------------------------------------------------- #
# The correction primitive: store.correct
# --------------------------------------------------------------------------- #


def test_correct_appends_superseding_line_and_keeps_audit_trail(tmp_path):
    """correct appends DESPITE the dedupe; the original line stays on disk."""
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)

    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 1
    assert readings[0]["value"] == 62

    lines = [json.loads(ln) for ln in _item_file(tmp_path).read_text().splitlines()]
    assert [ln["value"] for ln in lines] == [55, 62]  # append-only audit trail


def test_correction_of_a_correction_latest_wins(tmp_path):
    """The latest of multiple corrections wins; every prior line is retained."""
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)
    store.correct("rhr", _reading(T1, 64), root=tmp_path)

    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 1
    assert readings[0]["value"] == 64
    assert _line_count(tmp_path) == 3


def test_correct_unstored_identity_raises_and_writes_nothing(tmp_path):
    """A correction for a never-stored identity fails loud (no silent new point).

    A mistyped item/timepoint/source in a correction would otherwise silently
    create a NEW series point instead of correcting the intended one — the same
    silent-failure class bead 1vi exists to kill.
    """
    with pytest.raises(ValueError):
        store.correct("rhr", _reading(T1, 62), root=tmp_path)
    assert _line_count(tmp_path) == 0

    # Stored at T1, but the correction mistypes the timepoint (T2): same failure.
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    with pytest.raises(ValueError):
        store.correct("rhr", _reading(T2, 62), root=tmp_path)
    assert _line_count(tmp_path) == 1


def test_correct_to_already_resolved_value_is_noop(tmp_path):
    """Re-running the same correction appends 0 duplicate lines (FR-4 spirit)."""
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)

    assert _line_count(tmp_path) == 2
    assert store.read("rhr", root=tmp_path)[0]["value"] == 62


@pytest.mark.parametrize("missing", sorted(keying.LINE_FIELDS))
def test_correct_missing_field_raises_no_line(tmp_path, missing):
    """correct rejects a non-conformant reading exactly like append."""
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    corrected = _reading(T1, 62)
    del corrected[missing]

    with pytest.raises(ValueError):
        store.correct("rhr", corrected, root=tmp_path)
    assert _line_count(tmp_path) == 1


def test_correct_rejects_path_escaping_item(tmp_path):
    """correct inherits the store-root path-escape guard."""
    with pytest.raises(ValueError):
        store.correct("../evil", _reading(T1, 62, item="../evil"), root=tmp_path)
    assert not (tmp_path.parent / "evil.ndjson").exists()


# --------------------------------------------------------------------------- #
# The dedupe-drop boundary: normal ingest is UNCHANGED by the correction path
# --------------------------------------------------------------------------- #


def test_append_after_correction_still_drops_same_identity(tmp_path):
    """Normal append never overrides a correction — same-identity re-entries drop.

    Re-appending the ORIGINAL value (a re-ingest) and appending a DIFFERENT
    value (drift through the normal path) are both no-ops: the dedupe identity
    is already stored, so the corrected value stands and the file is unchanged.
    """
    store.append("rhr", _reading(T1, 55), root=tmp_path)
    store.correct("rhr", _reading(T1, 62), root=tmp_path)

    store.append("rhr", _reading(T1, 55), root=tmp_path)  # re-ingest of original
    store.append("rhr", _reading(T1, 99), root=tmp_path)  # drift via normal path

    assert _line_count(tmp_path) == 2
    assert store.read("rhr", root=tmp_path)[0]["value"] == 62


# --------------------------------------------------------------------------- #
# Cross-stream isolation + the loop_schema consumer surface
# --------------------------------------------------------------------------- #


def test_correction_never_surfaces_in_another_stream(tmp_path):
    """Correcting biomarker::ferritin must not touch panel::ferritin.

    The shared name across the disjoint stream namespaces is the collision
    bait: the corrected biomarker value must read corrected, while the panel
    stream keeps its single pending marker and still resolves PENDING.
    """
    loop_schema.record_biomarker("ferritin", T1, 41, tmp_path)
    loop_schema.record_pending_panel("ferritin", T1, tmp_path)

    store.correct(
        "biomarker::ferritin",
        _reading(T1, 44, item="biomarker::ferritin", source="manual"),
        root=tmp_path,
    )

    result = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert result["timepoints"][0]["value"] == 44
    assert loop_schema.read_panel("ferritin", root=tmp_path) == loop_schema.PENDING
    assert _line_count(tmp_path, item="panel::ferritin") == 1


def test_corrected_biomarker_keeps_published_state_and_count(tmp_path):
    """A correction changes the VALUE only: no-prior stays no-prior (1 timepoint).

    Without latest-wins resolution the superseding line would read as a second
    timepoint, silently flipping the published no-prior state to a trend.
    """
    loop_schema.record_biomarker("rhr", T1, 55, tmp_path)
    store.correct(
        "biomarker::rhr",
        _reading(T1, 62, item="biomarker::rhr", source="manual"),
        root=tmp_path,
    )

    result = loop_schema.read_biomarker("rhr", root=tmp_path)
    assert result["state"] == loop_schema.NO_PRIOR
    assert len(result["timepoints"]) == 1
    assert result["timepoints"][0]["value"] == 62
