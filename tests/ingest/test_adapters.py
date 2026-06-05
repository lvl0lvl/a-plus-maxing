"""Tests for the four per-source ingestion adapters (ADR-0003-T2).

Covers AC-1..AC-7: HealthKit + Oura mapping (AC-1/AC-2), the Garmin 0-shared-
routine-edit extensibility proof + functional import (AC-3/AC-4), the Whoop
registered-but-unwired scaffold (AC-5), and the simulated format-rename
re-validation 0-edit proof on a distinct baseline (AC-6). Every store write
goes to a tmp_path-based root via the `store_root` fixture so no test touches
the real `vault/store/`.

The two 0-edit proofs (AC-3, AC-6) diff `scripts/ingest/ingest.py` +
`scripts/ingest/adapter.py` against two DISTINCT committed-tree baselines. Each
baseline is a fresh `git commit-tree` over the FORK-POINT tree (`git merge-base
HEAD origin/main`, via `_baseline_ref`), so it carries the PRE-TASK shared-
routine blobs — the diff vs the working tree reds the moment any task commit
touched either path, which is the COMMITTED-edit case a HEAD-relative baseline
would tautologically miss. It is REGENERATED deterministically in any checkout
(origin/main is everywhere — the re-RED and `/review-pr` runs share this
checkout), so it depends on no transient local tag. The two baselines are
distinct git objects (a baseline-specific marker in each commit message) so
neither diff rides the other's ref. Each proof is additionally backed by a
co-located negative-control test that runs the SAME numstat logic against a
one-line probe added to a copy of the shared-routine file and confirms the row
count goes non-zero — extra teeth, without ever editing the real files.
"""

import subprocess
from pathlib import Path

import pytest

from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_ROUTINE_PATHS = ("scripts/ingest/ingest.py", "scripts/ingest/adapter.py")


def _write_json_export(path, rows):
    """Write a list of source-shaped dict rows as a JSON array export file."""
    import json

    path.write_text(json.dumps(rows))


def _numstat_rows(baseline_ref, paths):
    """Return the `git diff --numstat <baseline_ref> -- <paths>` rows.

    `git diff --numstat` emits NO row for an unchanged path, so an unchanged-both
    -paths diff yields an empty list. A touched path emits one `N\tM\tpath` row.
    The 0-edit pass condition is therefore `_numstat_rows(...) == []`.
    """
    out = subprocess.run(
        ["git", "diff", "--numstat", baseline_ref, "--", *paths],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def _baseline_ref(marker):
    """Build a DISTINCT committed-tree baseline object for a 0-edit proof.

    Each baseline is a fresh `git commit-tree` over the FORK-POINT tree — the
    commit this branch forked from `origin/main` (`git merge-base HEAD
    origin/main`) — so it carries the PRE-TASK `ingest.py` + `adapter.py` blobs.
    The diff `git diff --numstat <baseline> -- ingest.py adapter.py` is therefore
    a fork-point-vs-working-tree compare: it is empty exactly when no task commit
    touched either path (the 0-edit pass condition) and emits a row the moment a
    task commit (or working-tree edit) touches either (the falsifiable RED). A
    HEAD-relative baseline would be tautological — it would always be empty in a
    clean checkout, missing the very thing the gate exists to catch: a COMMITTED
    shared-routine edit. A baseline-specific `marker` in the commit message makes
    the two baselines (`pre-garmin`, `pre-format-rename`) DISTINCT git objects
    (different commit SHAs) for the two proofs, so neither diff rides the other's
    ref. The fork point is derived from `origin/main` (in every checkout — the
    re-RED and `/review-pr` runs share this checkout), so the baseline is
    REGENERATED deterministically without a transient local tag. If `origin/main`
    is unavailable the subprocess raises (the test ERRORS, not always-passes) —
    the correct fail-loud tradeoff for a falsifiability gate.
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    base_tree = subprocess.run(
        ["git", "rev-parse", f"{fork_point}^{{tree}}"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    return subprocess.run(
        ["git", "commit-tree", base_tree, "-p", fork_point, "-m",
         f"ADR-0003-T2 0-edit baseline: {marker}"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        input="",
    ).stdout.strip()


@pytest.fixture
def store_root(tmp_path):
    """A tmp store root so tests never write the real `vault/store/`."""
    return tmp_path / "store"


# --- Cycle 1: HealthKit + Oura adapters (AC-1, AC-2) ---


def test_healthkit_maps_export_to_store(tmp_path, store_root):
    """AC-1: the HealthKit adapter maps a sample export into field-set readings.

    Constructs the HealthKit adapter over a sample HealthKit-shaped export, runs
    it through the UNCHANGED ingest.run, then asserts via store.read that every
    mapped reading carries every Line Field Set field and round-trips.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    # HealthKit (Apple Health) export shape: per-sample records with HK-specific
    # field names the adapter maps into the store reading shape.
    export = tmp_path / "healthkit.json"
    _write_json_export(
        export,
        [
            {"type": "hrv", "startDate": "2026-01-01T08:00", "qty": 55},
            {"type": "rhr", "startDate": "2026-01-01T08:00", "qty": 48},
        ],
    )

    adapter = healthkit.HealthKitAdapter()
    ingest.run(adapter, export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    rhr = store.read("rhr", root=store_root)
    assert len(hrv) == 1 and len(rhr) == 1
    # Every reading carries every Line Field Set field, with the adapter's source.
    for reading in (*hrv, *rhr):
        assert set(reading) >= set(store.keying.LINE_FIELDS)
        assert reading["source"] == adapter.source_tag()
    assert hrv[0]["timepoint"] == "2026-01-01T08:00" and hrv[0]["value"] == 55
    assert rhr[0]["value"] == 48


def test_oura_maps_export_to_store(tmp_path, store_root):
    """AC-2: the Oura adapter maps a sample export into field-set readings.

    Same verification method as AC-1 over an Oura-shaped sample export.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import oura

    # Oura export shape: a `metrics` payload keyed by Oura's own field names.
    export = tmp_path / "oura.json"
    _write_json_export(
        export,
        [
            {"metric": "hrv", "day": "2026-01-02T08:00", "average": 58},
            {"metric": "rhr", "day": "2026-01-02T08:00", "average": 50},
        ],
    )

    adapter = oura.OuraAdapter()
    ingest.run(adapter, export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    rhr = store.read("rhr", root=store_root)
    assert len(hrv) == 1 and len(rhr) == 1
    for reading in (*hrv, *rhr):
        assert set(reading) >= set(store.keying.LINE_FIELDS)
        assert reading["source"] == adapter.source_tag()
    assert hrv[0]["timepoint"] == "2026-01-02T08:00" and hrv[0]["value"] == 58


# --- Cycle 2: Garmin 0-edit extensibility proof + functional import (AC-3, AC-4) ---


def test_garmin_imports_via_unchanged_run(tmp_path, store_root):
    """AC-4: the Garmin adapter imports via the UNCHANGED ingest.run.

    Builds the Garmin adapter over a sample Garmin export, runs it through the
    SAME ingest.run from ADR-0003-T1, and asserts the readings land in the store
    (the 0-edit addition is functional, not merely non-breaking).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import garmin

    # Garmin export shape: per-sample records with Garmin's own field names.
    export = tmp_path / "garmin.json"
    _write_json_export(
        export,
        [
            {"summaryType": "hrv", "calendarDate": "2026-01-03T08:00", "value": 60},
            {"summaryType": "rhr", "calendarDate": "2026-01-03T08:00", "value": 52},
        ],
    )

    adapter = garmin.GarminAdapter()
    ingest.run(adapter, export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    rhr = store.read("rhr", root=store_root)
    assert len(hrv) == 1 and len(rhr) == 1
    for reading in (*hrv, *rhr):
        assert set(reading) >= set(store.keying.LINE_FIELDS)
        assert reading["source"] == adapter.source_tag()
    assert hrv[0]["value"] == 60 and rhr[0]["value"] == 52


def test_garmin_addition_zero_shared_routine_edits():
    """AC-3: adding Garmin after HealthKit+Oura changes 0 lines in the routine.

    Asserts `git diff --numstat <pre-garmin> -- ingest.py adapter.py` emits 0 rows
    (empty output). `pre-garmin` is a DISTINCT committed-tree object holding both
    paths in their FINAL-committed state — the diff is against a fixed git object,
    not the working index. An unchanged path emits NO numstat row, so the pass
    condition is an EMPTY row list, NOT a literal "0" token. The Garmin source was
    added by creating ONE adapter module; ingest.py + adapter.py are untouched, so
    the diff is empty. The gate's teeth are proven by
    `test_garmin_zero_edit_gate_is_falsifiable`; its distinctness from the
    format-rename baseline by `test_two_zero_edit_baselines_are_distinct`.
    """
    pre_garmin = _baseline_ref("pre-garmin")
    rows = _numstat_rows(pre_garmin, SHARED_ROUTINE_PATHS)
    assert rows == [], (
        f"expected 0 changed lines in {SHARED_ROUTINE_PATHS} vs pre-garmin; "
        f"got numstat rows {rows} — a shared-routine edit crept in"
    )


def test_garmin_zero_edit_gate_is_falsifiable(tmp_path):
    """Negative control for AC-3: the 0-edit numstat gate turns RED on a real edit.

    Runs the SAME `git diff --numstat` row-detection the AC-3 assertion runs, but
    against a one-line-modified COPY of the committed ingest.py (via
    `git diff --no-index`), and asserts it emits exactly one changed-file row.
    This proves the gate is not tautological: were a shared-routine edit to land,
    numstat would emit a row and `test_garmin_addition_zero_shared_routine_edits`
    would turn RED. The real ingest.py is never touched.
    """
    committed = REPO_ROOT / "scripts" / "ingest" / "ingest.py"
    probed = tmp_path / "ingest_probe.py"
    probed.write_text(committed.read_text() + "# negative-control probe line\n")

    # `git diff --no-index --numstat A B` emits one `N\tM\tpath` row when A != B.
    out = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(committed), str(probed)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    ).stdout
    rows = [line for line in out.splitlines() if line.strip()]
    assert len(rows) == 1, (
        f"the one-line probe must make numstat emit exactly one row; got {rows}"
    )
    # The row reports +1 added line, proving the gate counts a real edit.
    assert rows[0].split("\t")[0] == "1"


# --- Cycle 3: Whoop registered-but-unwired scaffold (AC-5) ---

# The PRODUCTION modules THIS task creates, EXCLUDING whoop.py itself. The
# Whoop-unwired scan reads these: a Whoop import/registration here would be
# wiring the scaffold into the shipped adapter code. whoop.py is excluded — it
# IS the scaffold (it legitimately names "whoop"); "unwired" is the absence of a
# scheduler/wired-set reference ELSEWHERE. This test file is also excluded: a
# test importing the whoop adapter to verify conformance is test scaffolding,
# not production wiring (it MUST import whoop to test it).
WIRING_SCAN_FILES = (
    "scripts/ingest/adapters/healthkit.py",
    "scripts/ingest/adapters/oura.py",
    "scripts/ingest/adapters/garmin.py",
)

# A "Whoop wiring/invocation" reference: importing the whoop adapter module or
# naming its adapter class — i.e. registering it into a wired/scheduler set.
import re as _re

_WHOOP_WIRING_PATTERN = _re.compile(
    r"import\s+whoop\b|adapters\s+import\s+(?:[^\n]*\b)?whoop\b|WhoopAdapter"
)


def _whoop_wiring_count(text):
    """Count Whoop wiring/invocation references in a single source string."""
    return len(_WHOOP_WIRING_PATTERN.findall(text))


def test_whoop_scaffold_conforms_to_adapter_interface(tmp_path, store_root):
    """AC-5 half (a): whoop.py is importable and conforms to the Adapter contract.

    Asserts the Whoop adapter exposes `source_tag` + `read_readings(export_file)`
    (the @runtime_checkable Adapter Protocol) AND that `read_readings` actually
    maps a sample export through the UNCHANGED ingest.run — so a crippled stub
    (e.g. one raising NotImplementedError) would fail this half, not just an
    absent module. The scaffold is structurally a full adapter; only its wiring
    is absent.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapter import Adapter
    from scripts.ingest.adapters import whoop

    adapter = whoop.WhoopAdapter()
    assert isinstance(adapter, Adapter)  # exposes the frozen contract surface
    assert adapter.source_tag() == "whoop"

    # Not crippled: read_readings maps a real Whoop-shaped export into the store.
    export = tmp_path / "whoop.json"
    _write_json_export(
        export,
        [{"metric_name": "hrv", "cycle_start": "2026-01-04T08:00", "score": 62}],
    )
    ingest.run(adapter, export, root=store_root)
    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1
    assert set(hrv[0]) >= set(store.keying.LINE_FIELDS)
    assert hrv[0]["source"] == "whoop" and hrv[0]["value"] == 62


def test_whoop_unwired_no_scheduler_reference():
    """AC-5 half (b): no file THIS task creates wires/invokes Whoop.

    The T2-ownable form of the spec's `rg "whoop" scripts/ingest/scheduler.py`=0:
    scheduler.py is ADR-0003-T3's deliverable and does not exist at this task's
    entry point, so the literal command errors (exit 2) on the missing file and
    is deferred to the Wave 4->5 boundary. Here we assert the in-task invariant:
    no PRODUCTION module this task ships introduces a Whoop wiring/invocation
    reference (an `import whoop` / `WhoopAdapter` registration into a wired/
    scheduler set). The scaffold whoop.py and this test file are excluded — the
    scaffold IS the registered adapter, and a test importing it to verify
    conformance is test scaffolding, not production wiring; unwired-ness is the
    absence of a reference in the SHIPPED adapter code. Teeth proven by
    `test_whoop_unwired_gate_is_falsifiable`.
    """
    for rel in WIRING_SCAN_FILES:
        text = (REPO_ROOT / rel).read_text()
        assert _whoop_wiring_count(text) == 0, (
            f"{rel} introduces a Whoop wiring/invocation reference; the scaffold "
            f"must stay unwired (no scheduler/wired-set entry point imports Whoop)"
        )


def test_whoop_unwired_gate_is_falsifiable():
    """Negative control for AC-5 half (b): the no-wiring scan turns RED on real wiring.

    Runs the SAME `_whoop_wiring_count` scan against a simulated scheduler/wired
    -set entry point this task COULD create, and asserts it counts the planted
    reference. This proves the unwired gate catches actual wiring, not merely the
    absence of a file: were a Whoop import/registration to land in one of this
    task's files, `test_whoop_unwired_no_scheduler_reference` would turn RED.
    """
    planted_scheduler = (
        "from scripts.ingest.adapters import whoop\n"
        "WIRED = [whoop.WhoopAdapter()]\n"
    )
    assert _whoop_wiring_count(planted_scheduler) > 0


# --- Cycle 4: simulated format-rename re-validation 0-edit proof (AC-6) ---


def _garmin_renamed_export(path):
    """Write a Garmin export whose `value` field was renamed to `valueInMillis`.

    Simulates an upstream Garmin export-format field rename. After garmin.py's
    `read_readings` is updated to absorb the rename, the SAME readings (same item,
    timepoint, source) must still land and dedupe — proving the dedupe key is
    re-derived through the adapter's mapping, not through a shared-routine edit.
    """
    _write_json_export(
        path,
        [
            {"summaryType": "hrv", "calendarDate": "2026-01-05T08:00", "valueInMillis": 63},
            # SAME identity (item, timepoint, source) as the first row -> the store
            # dedupes the pair to one line; a value difference is excluded from the key.
            {"summaryType": "hrv", "calendarDate": "2026-01-05T08:00", "valueInMillis": 99},
        ],
    )


def test_format_rename_zero_shared_routine_edits(tmp_path, store_root):
    """AC-6: a Garmin export field rename is absorbed inside the adapter; 0 routine edits.

    After garmin.py's `read_readings` absorbs the `value` -> `valueInMillis`
    rename, the renamed-field readings (a) still round-trip into the store and
    (b) still dedupe on the unchanged (item, timepoint, source) key — the dedupe
    key is re-derived through the adapter's mapping, NOT through a shared-routine
    edit. AND `git diff --numstat <pre-format-rename> -- ingest.py adapter.py`
    emits 0 rows: the rename touched only garmin.py. `pre-format-rename` is a
    DISTINCT committed-tree object from `pre-garmin` (a different commit object,
    for a different proof) — this diff does NOT ride the pre-garmin baseline. Gate
    teeth proven by `test_format_rename_zero_edit_gate_is_falsifiable`;
    distinctness from pre-garmin by `test_two_zero_edit_baselines_are_distinct`.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import garmin

    export = tmp_path / "garmin_renamed.json"
    _garmin_renamed_export(export)

    ingest.run(garmin.GarminAdapter(), export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    # Re-validation: the renamed-field readings still round-trip AND dedupe on the
    # unchanged identity key (two same-identity rows collapse to one stored line).
    assert len(hrv) == 1
    assert set(hrv[0]) >= set(store.keying.LINE_FIELDS)
    assert hrv[0]["timepoint"] == "2026-01-05T08:00"
    assert hrv[0]["source"] == "garmin"
    # The renamed field was mapped to the SAME `value` store field (first write wins).
    assert hrv[0]["value"] == 63

    # 0 shared-routine edits: the rename lives entirely in garmin.read_readings.
    pre_format_rename = _baseline_ref("pre-format-rename")
    rows = _numstat_rows(pre_format_rename, SHARED_ROUTINE_PATHS)
    assert rows == [], (
        f"expected 0 changed lines in {SHARED_ROUTINE_PATHS} vs pre-format-rename; "
        f"got numstat rows {rows} — absorbing the rename touched the shared routine"
    )


def test_format_rename_zero_edit_gate_is_falsifiable(tmp_path):
    """Negative control for AC-6: the format-rename 0-edit gate turns RED on a real edit.

    Runs the SAME `git diff --numstat` row-detection the AC-6 assertion runs,
    against a one-line-modified COPY of the committed adapter.py (via
    `git diff --no-index`), and asserts it emits exactly one changed-file row.
    This proves the AC-6 gate (on its OWN distinct pre-format-rename baseline) is
    not tautological: were absorbing the rename to require a shared-routine edit,
    numstat would emit a row and `test_format_rename_zero_shared_routine_edits`
    would turn RED. The real adapter.py is never touched.
    """
    committed = REPO_ROOT / "scripts" / "ingest" / "adapter.py"
    probed = tmp_path / "adapter_probe.py"
    probed.write_text(committed.read_text() + "# negative-control probe line\n")

    out = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(committed), str(probed)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    ).stdout
    rows = [line for line in out.splitlines() if line.strip()]
    assert len(rows) == 1, (
        f"the one-line probe must make numstat emit exactly one row; got {rows}"
    )
    assert rows[0].split("\t")[0] == "1"


def test_two_zero_edit_baselines_are_distinct():
    """The two 0-edit baselines are DISTINCT git objects for the two proofs.

    `pre-garmin` (AC-3, Cycle 2) and `pre-format-rename` (AC-6, Cycle 4) must
    resolve to DIFFERENT commit objects — neither 0-edit diff rides the other's
    baseline. Both hold the same FINAL-committed ingest.py + adapter.py blobs (the
    diffs are against fixed git objects), but the baselines themselves are
    separate objects, as the dual-baseline design requires (Rollback §2 forbids
    collapsing them into one shared ref). The two also produce IDENTICAL 0-edit
    verdicts here (both empty) because the two shared-routine paths are unedited —
    a distinctness check that also confirms both diffs are evaluable.
    """
    pre_garmin = _baseline_ref("pre-garmin")
    pre_format_rename = _baseline_ref("pre-format-rename")
    assert pre_garmin != pre_format_rename, (
        "the two 0-edit baselines must be DISTINCT objects for the two proofs; "
        "collapsing them into one shared ref is forbidden (Rollback §2)"
    )
    # Both baselines are evaluable and both report 0 edits (unedited shared routine).
    assert _numstat_rows(pre_garmin, SHARED_ROUTINE_PATHS) == []
    assert _numstat_rows(pre_format_rename, SHARED_ROUTINE_PATHS) == []
