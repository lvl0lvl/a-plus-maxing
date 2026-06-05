"""Tests for the shared ingestion routine + adapter interface (ADR-0003-T1).

Covers AC-1..AC-7: adapter-interface conformance, single-invocation import,
idempotent re-run, single-shared-key dedupe, manual-entry/CSV fallback,
new-timepoint delta, and the dual-mechanism no-model-step proof. All store
writes go to a tmp_path-based root via the `store_root` fixture so no test
touches the real `vault/store/`.
"""

import re
from pathlib import Path

import pytest

from scripts.store import keying, store

INGEST_DIR = Path(__file__).resolve().parents[2] / "scripts" / "ingest"


def _reading(item, timepoint, source, value):
    """Build a Line-Field-Set reading dict (keying.LINE_FIELDS field names)."""
    return {"item": item, "timepoint": timepoint, "source": source, "value": value}


class _ListAdapter:
    """Minimal in-test adapter conforming to the published export contract.

    Implements the frozen named contract: `source_tag` (zero-arg source-identity
    accessor) + `read_readings(export_file)` (one-arg, yields Line-Field-Set
    readings). The export_file is a JSON-lines file of readings (the adapter's
    own per-source parsing concern); the contract only fixes the return shape.
    """

    def __init__(self, source):
        self._source = source

    def source_tag(self):
        return self._source

    def read_readings(self, export_file):
        import json

        for line in Path(export_file).read_text().splitlines():
            if line.strip():
                yield json.loads(line)


def _write_export(path, readings):
    """Write readings as JSON-lines to an export file for _ListAdapter."""
    import json

    path.write_text("".join(json.dumps(r) + "\n" for r in readings))


@pytest.fixture
def store_root(tmp_path):
    """A tmp store root so tests never write the real `vault/store/`."""
    return tmp_path / "store"


# --- Cycle 1: adapter interface (AC-1 prerequisite) ---


def test_adapter_interface_conformance(tmp_path):
    """A conforming adapter exposes source_tag() + read_readings(export_file)."""
    from scripts.ingest import adapter

    export = tmp_path / "export.ndjson"
    rows = [_reading("hrv", "2026-01-01T08:00", "oura", 55)]
    _write_export(export, rows)

    a = _ListAdapter("oura")
    # The contract surface: zero-arg source identity + one-arg readings iterable.
    assert a.source_tag() == "oura"
    got = list(a.read_readings(export))
    assert got == rows
    # adapter.py exists and names the frozen contract surface (so ADR-0003-T2's
    # adapters import the stable names). Touches the module to bind the import.
    assert hasattr(adapter, "Adapter") or hasattr(adapter, "SOURCE_TAG_ATTR")


# --- Pure-Python content scans over scripts/ingest/ ---
# `rg` is a non-executable shim on this host (subprocess.run(["rg",...]) raises
# FileNotFoundError), so the recipe's crit-3 `rg "def .*key"`=0 and crit-5 Half-B
# model/API-client scans are implemented in pure Python — the SAME documented
# deviation scripts/guard/pii_scan.py took (same contents-search semantics,
# different mechanism). Drift #2 in the task brief.


def _scan_ingest(pattern):
    """Count regex matches across every *.py file under scripts/ingest/.

    Pure-Python stand-in for `rg <pattern> scripts/ingest/` (rg is a non-exec
    shim here). Returns the total match count over file contents.
    """
    rx = re.compile(pattern)
    total = 0
    for py in sorted(INGEST_DIR.glob("*.py")):
        total += len(rx.findall(py.read_text()))
    return total


def _key_def_count():
    """crit-3 scan: count `def .*key` definitions under scripts/ingest/ (expect 0)."""
    return _scan_ingest(r"def .*key")


# The model/API-client token set from the ADR-0001-T0 spike's "No-Raw-Reading-To-
# Model Rule" section (read scoped per the Context Load List — NOT a narrower
# invented set): model/network client imports + the *.create call shapes.
_MODEL_TOKEN_PATTERN = (
    r"import (anthropic|openai|voyageai|requests|httpx)"
    r"|\.(messages|chat|embeddings)\.create"
)


def _model_token_count():
    """crit-5 Half-B scan: count model/API-client tokens under scripts/ingest/."""
    return _scan_ingest(_MODEL_TOKEN_PATTERN)


# --- Cycle 2: shared routine — import, idempotent re-run, single-shared-key dedupe ---


def test_run_imports_export_in_one_call(tmp_path, store_root):
    """AC-1: ingest.run brings every export reading into the store in one call."""
    from scripts.ingest import ingest

    rows = [
        _reading("hrv", "2026-01-01T08:00", "oura", 55),
        _reading("hrv", "2026-01-02T08:00", "oura", 58),
        _reading("rhr", "2026-01-01T08:00", "oura", 48),
    ]
    export = tmp_path / "export.ndjson"
    _write_export(export, rows)

    ingest.run(_ListAdapter("oura"), export, root=store_root)

    stored = store.read("hrv", root=store_root) + store.read("rhr", root=store_root)
    # Exact count: a dropped or duplicated reading turns this red.
    assert len(stored) == len(rows)
    assert {(r["item"], r["timepoint"], r["value"]) for r in stored} == {
        (r["item"], r["timepoint"], r["value"]) for r in rows
    }


def test_rerun_appends_zero_duplicates(tmp_path, store_root):
    """AC-2: re-running over an already-stored export appends 0 duplicate lines."""
    from scripts.ingest import ingest

    rows = [
        _reading("hrv", "2026-01-01T08:00", "oura", 55),
        _reading("hrv", "2026-01-02T08:00", "oura", 58),
    ]
    export = tmp_path / "export.ndjson"
    _write_export(export, rows)
    adapter = _ListAdapter("oura")

    ingest.run(adapter, export, root=store_root)
    first = len(store.read("hrv", root=store_root))
    ingest.run(adapter, export, root=store_root)
    second = len(store.read("hrv", root=store_root))

    assert first == len(rows)
    assert second == first  # unchanged on the second run (exact, not "<=")


def test_dedupe_uses_shared_keying(tmp_path, store_root):
    """AC-3 / Risk N3: no second key under scripts/ingest/, dedupe via keying.py.

    Half (a): the pure-Python `def .*key` scan over scripts/ingest/ returns 0.
    Half (b): two readings keying.dedupe_key maps to the SAME identity dedupe to
    one stored line through ingest.run (so the routine dedupes via the imported
    key, not a private copy).
    """
    from scripts.ingest import ingest

    # Half (a): no independent key function defined under scripts/ingest/.
    assert _key_def_count() == 0

    # Half (b): same (item, timepoint, source) -> one stored line; different value
    # would be the SECOND reading the shared key collapses.
    r1 = _reading("hrv", "2026-01-01T08:00", "oura", 55)
    r2 = _reading("hrv", "2026-01-01T08:00", "oura", 99)
    assert keying.dedupe_key(r1) == keying.dedupe_key(r2)  # shared key collapses them
    export = tmp_path / "export.ndjson"
    _write_export(export, [r1, r2])

    ingest.run(_ListAdapter("oura"), export, root=store_root)
    assert len(store.read("hrv", root=store_root)) == 1


def test_imported_readings_round_trip_through_store(tmp_path, store_root):
    """Risk N2 inherited: readings land via store.append (round-trip via store.read).

    Proves the routine writes through store.append (inheriting field-set
    rejection), not a raw NDJSON write that would re-open the N2 no-schema hole.
    """
    from scripts.ingest import ingest

    rows = [_reading("hrv", "2026-01-01T08:00", "oura", 55)]
    export = tmp_path / "export.ndjson"
    _write_export(export, rows)

    ingest.run(_ListAdapter("oura"), export, root=store_root)
    stored = store.read("hrv", root=store_root)
    assert stored == rows  # conformant readings round-trip through the store path


# --- Cycle 3: manual-entry/CSV fallback, new-timepoint delta, no-model-step ---


def test_manual_entry_and_csv_land_in_same_store(tmp_path, store_root):
    """AC-4: manual_entry + import_csv land readings alongside adapter imports.

    All three write paths (run, manual_entry, import_csv) reach the SAME per-item
    store files through store.append.
    """
    from scripts.ingest import ingest

    # An adapter import first, so the fallback readings must land alongside it.
    export = tmp_path / "export.ndjson"
    _write_export(export, [_reading("hrv", "2026-01-01T08:00", "oura", 55)])
    ingest.run(_ListAdapter("oura"), export, root=store_root)

    # manual_entry: one operator-supplied reading for the same item.
    ingest.manual_entry(
        "hrv", _reading("hrv", "2026-01-02T08:00", "manual", 60), root=store_root
    )

    # import_csv: a small CSV of readings (Line Field Set columns).
    csv_path = tmp_path / "readings.csv"
    csv_path.write_text(
        "item,timepoint,source,value\n"
        "hrv,2026-01-03T08:00,csv,62\n"
        "weight,2026-01-03T08:00,csv,180\n"
    )
    ingest.import_csv(csv_path, root=store_root)

    hrv = store.read("hrv", root=store_root)
    weight = store.read("weight", root=store_root)
    # Adapter + manual + CSV readings coexist in the same hrv item file.
    assert {(r["timepoint"], r["source"]) for r in hrv} == {
        ("2026-01-01T08:00", "oura"),
        ("2026-01-02T08:00", "manual"),
        ("2026-01-03T08:00", "csv"),
    }
    assert {(r["timepoint"], r["source"]) for r in weight} == {
        ("2026-01-03T08:00", "csv")
    }


def test_run_appends_only_new_timepoint_delta(tmp_path, store_root):
    """AC-6: an export of stored + new timepoints appends only the new-timepoint delta.

    Pre-store a subset of an export's timepoints, run over the full export, and
    assert the line-count DELTA EQUALS the new-timepoint count (exact). A probe
    that re-appends already-stored timepoints (delta = full export count) reds
    this assertion — see the AC-6 broken-delta negative control in the report.
    """
    from scripts.ingest import ingest

    full = [
        _reading("hrv", "2026-01-01T08:00", "oura", 55),  # pre-stored
        _reading("hrv", "2026-01-02T08:00", "oura", 58),  # pre-stored
        _reading("hrv", "2026-01-03T08:00", "oura", 60),  # new
        _reading("hrv", "2026-01-04T08:00", "oura", 61),  # new
    ]
    new_count = 2

    # Pre-store the first two timepoints (the "already-stored" subset).
    pre_export = tmp_path / "pre.ndjson"
    _write_export(pre_export, full[:2])
    ingest.run(_ListAdapter("oura"), pre_export, root=store_root)
    before = len(store.read("hrv", root=store_root))

    # Run over the FULL export (stored + new timepoints).
    full_export = tmp_path / "full.ndjson"
    _write_export(full_export, full)
    ingest.run(_ListAdapter("oura"), full_export, root=store_root)
    after = len(store.read("hrv", root=store_root))

    assert after - before == new_count  # exact new-timepoint delta


def test_ingest_run_zero_egress(tmp_path):
    """AC-5 Half A: a real ingest.run under egress_guard.run is truthy (0 egress).

    Wraps a REAL ingest.run (adapter + tmp export + tmp store root, all closed
    over) in ONE zero-arg closure passed to egress_guard.run. egress_guard forks
    + OS-isolates the child, runs the closure there, and returns truthy iff 0
    outbound calls surfaced across the whole invocation.
    """
    from scripts.guard import egress_guard
    from scripts.ingest import ingest

    export = tmp_path / "export.ndjson"
    _write_export(export, [_reading("hrv", "2026-01-01T08:00", "oura", 55)])
    store_root = tmp_path / "store"

    def operation():
        ingest.run(_ListAdapter("oura"), export, root=store_root)

    assert egress_guard.run(operation)


def test_no_model_step_static_scan():
    """AC-5 Half B: 0 model/API-client tokens under scripts/ingest/.

    Pure-Python stand-in for `rg <model-token-set> scripts/ingest/`=0. The token
    set is the ADR-0001-T0 spike's No-Raw-Reading-To-Model Rule set (imports +
    *.create call shapes) — not an invented narrower set. Failing-capability is
    proven by the crit-5 Half-B negative control in the report.
    """
    assert _model_token_count() == 0
