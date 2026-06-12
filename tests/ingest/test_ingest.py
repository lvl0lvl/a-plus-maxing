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


def _scan_text(text, pattern):
    """Count regex matches in a single string (the scan's core, testable in isolation)."""
    return len(re.compile(pattern).findall(text))


def _scan_ingest(pattern):
    """Count regex matches across every *.py file under scripts/ingest/.

    Pure-Python stand-in for `rg <pattern> scripts/ingest/` (rg is a non-exec
    shim here). Returns the total match count over file contents.
    """
    total = 0
    for py in sorted(INGEST_DIR.glob("*.py")):
        total += _scan_text(py.read_text(), pattern)
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


# --- TEST-001/002: positive controls — prove the scan mechanisms can turn red ---


def test_key_def_scan_detects_planted_token():
    """TEST-001: the `def .*key` scan returns >0 against a planted key def.

    Proves the crit-3 `_key_def_count() == 0` assertion is not vacuous: the same
    regex applied to a fixture string carrying `def make_key` detects it. If the
    regex could never match, the `=0` assertion over scripts/ingest/ would be
    meaningless.
    """
    assert _scan_text("def make_key(reading):\n    return ()", r"def .*key") > 0


def test_model_token_scan_detects_planted_token():
    """TEST-002: the model/API-client scan returns >0 against planted tokens.

    Proves the crit-5 Half-B `_model_token_count() == 0` assertion is not vacuous:
    the same token pattern applied to a fixture string carrying `import openai`
    and a `.messages.create` call shape detects them.
    """
    planted = "import openai\nclient.messages.create(model='x')\n"
    assert _scan_text(planted, _MODEL_TOKEN_PATTERN) > 0


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
    import subprocess

    from scripts.guard import egress_guard
    from scripts.ingest import ingest

    # Sandbox-availability precondition: egress_guard.run is fail-closed (returns
    # falsy when OS isolation cannot be applied), so where sandbox-exec is not
    # invocable the truthy assertion would FAIL, not skip. Mirror the store AC-4
    # precondition (tests/store/test_store.py::test_append_read_zero_egress) and
    # skip when isolation can't be set up — keep the truthy assertion where it can.
    if subprocess.run(
        ["/usr/bin/sandbox-exec", "-p", "(version 1)(allow default)", "/usr/bin/true"],
        capture_output=True,
    ).returncode != 0:
        pytest.skip("sandbox-exec not invocable — zero-egress isolation unavailable")

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


# --- TEST-003: AC-6 delta — distinguish "deduped at store" from "pre-filtered" ---


def test_run_routes_every_reading_store_dedupes(tmp_path, store_root, monkeypatch):
    """TEST-003: run issues exactly len(export) append calls; the store dedupes.

    A store.append call-count spy proves run does NOT pre-filter duplicates: it
    routes EVERY reading (including the two same-identity duplicates) to the
    store, and the store is what collapses them to one line. RED if run grew a
    private pre-dedupe (call count would drop below len(export)).
    """
    from scripts.ingest import ingest

    export_rows = [
        _reading("hrv", "2026-01-01T08:00", "oura", 55),
        _reading("hrv", "2026-01-01T08:00", "oura", 99),  # same identity, dropped at store
        _reading("hrv", "2026-01-02T08:00", "oura", 58),
    ]
    export = tmp_path / "export.ndjson"
    _write_export(export, export_rows)

    real_append = store.append
    calls = {"n": 0}

    def _spy(item, reading, root=store.DEFAULT_ROOT):
        calls["n"] += 1
        return real_append(item, reading, root=root)

    monkeypatch.setattr(store, "append", _spy)
    ingest.run(_ListAdapter("oura"), export, root=store_root)

    # Every reading routed to the store (no ingest pre-filter)...
    assert calls["n"] == len(export_rows)
    # ...and the STORE deduped the same-identity pair to one stored line.
    assert len(store.read("hrv", root=store_root)) == 2


# --- TEST-005: import_csv input validation ---


def test_import_csv_missing_required_column_raises_nothing_written(tmp_path, store_root):
    """TEST-005: a row missing a required column raises ValueError, writes nothing.

    The header omits `source`, so every row is missing it. import_csv validates
    before any write, so it raises and the store stays empty (no partial import).
    """
    from scripts.ingest import ingest

    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("item,timepoint,value\nhrv,2026-01-01T08:00,55\n")

    with pytest.raises(ValueError):
        ingest.import_csv(csv_path, root=store_root)
    assert store.read("hrv", root=store_root) == []


def test_import_csv_extra_column_row_rejected_no_null_field(tmp_path, store_root):
    """TEST-005: an extra-column (ragged) row is rejected, not stored with a "null" field.

    csv.DictReader groups surplus columns under the None key; import_csv rejects
    that row with ValueError instead of silently storing a `"null"` field. Nothing
    is written.
    """
    from scripts.ingest import ingest

    csv_path = tmp_path / "ragged.csv"
    # Header has 4 columns; the row has 5 -> surplus lands under the None key.
    csv_path.write_text(
        "item,timepoint,source,value\n"
        "hrv,2026-01-01T08:00,csv,55,EXTRA\n"
    )

    with pytest.raises(ValueError):
        ingest.import_csv(csv_path, root=store_root)
    stored = store.read("hrv", root=store_root)
    assert stored == []
    # The surplus value never became a stored field (no "null"/None key leaked).
    for r in stored:
        assert "null" not in r and None not in r


def test_import_csv_header_only_writes_nothing(tmp_path, store_root):
    """TEST-005: a header-only / empty CSV leaves the store empty without crashing."""
    from scripts.ingest import ingest

    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("item,timepoint,source,value\n")

    ingest.import_csv(csv_path, root=store_root)  # must not raise
    assert store.read("hrv", root=store_root) == []


# --- TEST-006: cross-mechanism same-identity dedupe (value excluded from key) ---


def test_cross_mechanism_same_identity_first_write_wins(tmp_path, store_root):
    """TEST-006: adapter then CSV, same (item,timepoint,source), different value.

    The FIRST write (adapter, value 55) wins for NORMAL ingest; the CSV
    re-entry (62) is dropped because the dedupe key is (item, timepoint,
    source) only — value is excluded (ADR-0002 keying property). This pins the
    documented dedupe-on-identity behavior across the two write mechanisms.
    Since bead 1vi a value CORRECTION is an explicit `manual_correction` /
    `store.correct` superseding append — never a normal-path re-entry, which
    stays a no-op exactly as pinned here.
    """
    from scripts.ingest import ingest

    export = tmp_path / "export.ndjson"
    _write_export(export, [_reading("hrv", "2026-01-01T08:00", "oura", 55)])
    ingest.run(_ListAdapter("oura"), export, root=store_root)

    # SAME identity, different value, via the OTHER mechanism (CSV).
    csv_path = tmp_path / "correction.csv"
    csv_path.write_text(
        "item,timepoint,source,value\n"
        "hrv,2026-01-01T08:00,oura,62\n"
    )
    ingest.import_csv(csv_path, root=store_root)

    stored = store.read("hrv", root=store_root)
    assert len(stored) == 1
    # value 55 (the first write) survived; the CSV "62" re-entry was dropped —
    # the known ADR-0002 keying property: value is excluded from the dedupe key.
    # An intended correction goes through the explicit manual_correction path.
    assert stored[0]["value"] == 55


# --- TEST-007: uniform ValueError for a non-conformant adapter reading ---


@pytest.mark.parametrize("missing", sorted(keying.LINE_FIELDS))
def test_run_non_conformant_reading_raises_value_error(tmp_path, store_root, missing):
    """TEST-007: a reading missing ANY field (incl. item) raises ValueError from run.

    Per fix C, the missing-field failure is uniform: a missing `item` raises
    ValueError just like every other missing field (not a bare KeyError).
    """
    from scripts.ingest import ingest

    reading = _reading("hrv", "2026-01-01T08:00", "oura", 55)
    del reading[missing]
    export = tmp_path / "export.ndjson"
    _write_export(export, [reading])

    with pytest.raises(ValueError):
        ingest.run(_ListAdapter("oura"), export, root=store_root)


# --- TEST-008: persisted source matches the adapter's emitted reading source ---


def test_persisted_source_matches_emitted_reading_source(tmp_path, store_root):
    """TEST-008: the stored `source` is the reading's own `source`, not source_tag.

    run does NOT stamp source from the adapter's source_tag identity declaration —
    readings self-carry `source`. Here the adapter's source_tag ("oura-tag")
    differs from the reading's source field ("oura-reading"); the persisted line
    carries the READING's source, proving run reads it off the reading, not the
    adapter accessor.
    """
    from scripts.ingest import ingest

    class _DivergentAdapter(_ListAdapter):
        def source_tag(self):
            return "oura-tag"  # identity declaration, NOT stamped onto readings

    export = tmp_path / "export.ndjson"
    _write_export(export, [_reading("hrv", "2026-01-01T08:00", "oura-reading", 55)])
    ingest.run(_DivergentAdapter("oura-tag"), export, root=store_root)

    stored = store.read("hrv", root=store_root)
    assert len(stored) == 1
    assert stored[0]["source"] == "oura-reading"


# --- SEC-001: a traversing/absolute item writes NOTHING outside the store root ---


@pytest.mark.parametrize("bad_item", ["../escaped/x", "/tmp/abs", "a/b"])
def test_store_append_rejects_unsafe_item(tmp_path, bad_item):
    """SEC-001: store.append rejects a traversing/absolute/multi-segment item.

    The defended boundary is "the resolved store path escapes the root": a `..`
    traversal, an absolute path, or a multi-segment `a/b` all resolve outside the
    root's direct children and are rejected. (An empty item resolves to
    `root/.ndjson` — a hidden file INSIDE the root, not an escape — so it is not in
    this set; SEC-001 is path-escape, not degenerate-name, validation.)
    """
    reading = {
        "item": bad_item,
        "timepoint": "2026-01-01T08:00",
        "source": "manual",
        "value": 1,
    }
    with pytest.raises(ValueError):
        store.append(bad_item, reading, root=tmp_path / "store")


def test_import_csv_rejects_traversing_item_writes_nothing(tmp_path):
    """SEC-001: a traversing CSV `item` raises and writes nothing outside the root."""
    from scripts.ingest import ingest

    root = tmp_path / "store"
    outside = tmp_path / "escaped"  # sibling of the store root the item targets
    csv_path = tmp_path / "evil.csv"
    csv_path.write_text(
        "item,timepoint,source,value\n"
        "../escaped/pwn,2026-01-01T08:00,csv,1\n"
    )

    with pytest.raises(ValueError):
        ingest.import_csv(csv_path, root=root)
    # Nothing was written anywhere outside the store root.
    assert not outside.exists()
    assert not (tmp_path / "escaped").exists()


def test_manual_entry_rejects_traversing_item_writes_nothing(tmp_path):
    """SEC-001: a traversing manual_entry `item` raises and writes nothing outside."""
    from scripts.ingest import ingest

    root = tmp_path / "store"
    reading = {
        "item": "../escaped/pwn",
        "timepoint": "2026-01-01T08:00",
        "source": "manual",
        "value": 1,
    }
    with pytest.raises(ValueError):
        ingest.manual_entry("../escaped/pwn", reading, root=root)
    assert not (tmp_path / "escaped").exists()


# --- bead 1vi: the explicit correction entry point (correction.manual_correction) ---


def test_manual_correction_supersedes_cross_mechanism_value(tmp_path, store_root):
    """Adapter ingest then an EXPLICIT correction: the corrected value reads back.

    The TEST-006 counterpart: where the normal CSV re-entry is dropped
    (first-write-wins for normal ingest, unchanged), the explicit
    `correction.manual_correction` path appends a superseding line — the read
    resolves to the corrected value, and the original line stays on disk
    (audit trail). The entry lives in its own module, NOT in ingest.py: the
    AC-3/AC-6 0-edit gates pin the shared routine at the branch fork point.
    """
    from scripts.ingest import correction, ingest

    export = tmp_path / "export.ndjson"
    _write_export(export, [_reading("hrv", "2026-01-01T08:00", "oura", 55)])
    ingest.run(_ListAdapter("oura"), export, root=store_root)

    correction.manual_correction(
        "hrv", _reading("hrv", "2026-01-01T08:00", "oura", 62), root=store_root
    )

    stored = store.read("hrv", root=store_root)
    assert len(stored) == 1
    assert stored[0]["value"] == 62
    lines = (store_root / "hrv.ndjson").read_text().splitlines()
    assert len([ln for ln in lines if ln.strip()]) == 2


def test_manual_correction_item_mismatch_raises(tmp_path, store_root):
    """The item argument must equal reading["item"], exactly like manual_entry."""
    from scripts.ingest import correction

    reading = _reading("hrv", "2026-01-01T08:00", "oura", 55)
    store.append("hrv", reading, root=store_root)

    corrected = _reading("hrv", "2026-01-01T08:00", "oura", 62)
    with pytest.raises(ValueError):
        correction.manual_correction("rhr", corrected, root=store_root)
    assert store.read("hrv", root=store_root)[0]["value"] == 55


def test_manual_correction_missing_item_raises(store_root):
    """A reading without `item` raises the uniform missing-field ValueError."""
    from scripts.ingest import correction

    corrected = _reading("hrv", "2026-01-01T08:00", "oura", 62)
    del corrected["item"]
    with pytest.raises(ValueError):
        correction.manual_correction("hrv", corrected, root=store_root)


def test_manual_correction_unstored_identity_raises(store_root):
    """A correction whose identity was never stored propagates store.correct's raise."""
    from scripts.ingest import correction

    with pytest.raises(ValueError):
        correction.manual_correction(
            "hrv", _reading("hrv", "2026-01-01T08:00", "oura", 62), root=store_root
        )
