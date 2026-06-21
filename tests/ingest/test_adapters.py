"""Tests for the four per-source ingestion adapters (ADR-0003-T2).

Covers AC-1..AC-7: HealthKit + Oura mapping (AC-1/AC-2), the Garmin 0-shared-
routine-edit extensibility proof + functional import (AC-3/AC-4), the Whoop wired
read-only-SQLite adapter (ADR-0011 D2 v2) + its store-adversarial battery
(replacing the former registered-but-unwired scaffold), and the simulated
format-rename re-validation 0-edit proof on a distinct baseline (AC-6). Every store write
goes to a tmp_path-based root via the `store_root` fixture so no test touches
the real `vault/store/`.

The two 0-edit proofs (AC-3, AC-6) diff the shared routine
(`scripts/ingest/ingest.py` + `scripts/ingest/adapter.py`) against two DISTINCT
committed-tree baselines built by `_baseline_ref`; see that function for the
fork-point/distinctness rationale.
"""

import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import pytest

from conftest import hk_record, write_healthkit_export as _write_healthkit_export

from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_ROUTINE_PATHS = ("scripts/ingest/ingest.py", "scripts/ingest/adapter.py")
# ADR-0013-T3 / ADR-0003-T2: the three shared-routine files the zip-awareness must NOT touch
# (the zip extraction lives in the adapter, never the shared routine — recipe AC-5).
SHARED_ROUTINE_PATHS_FULL = (
    "scripts/ingest/ingest.py",
    "scripts/ingest/adapter.py",
    "scripts/ingest/scheduler.py",
)


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


def test_healthkit_maps_export_xml_to_store(tmp_path, store_root):
    """AC-1: the HealthKit adapter maps the REAL Apple Health export.xml into field-set readings.

    Builds a real-shape export.xml, runs it through the UNCHANGED ingest.run, and asserts each mapped
    HK type lands on its OWN (item, day, "healthkit") stream with the CORRECT value — pinning the
    value per stream REDs a transposed type->item map (the S41 fabricated-biomarker class). spo2's
    0-1 fraction is scaled ×100 to the store's percent.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapter import Adapter
    from scripts.ingest.adapters import healthkit

    adapter = healthkit.HealthKitAdapter()
    assert isinstance(adapter, Adapter)  # exposes the frozen contract surface
    assert adapter.source_tag() == "healthkit"

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-01-01 08:00:00 -0500", "value": "55"},
        {"type": "HKQuantityTypeIdentifierRestingHeartRate",
         "startDate": "2026-01-01 06:00:00 -0500", "value": "48"},
        {"type": "HKQuantityTypeIdentifierRespiratoryRate",
         "startDate": "2026-01-01 03:00:00 -0500", "value": "14.2"},
        {"type": "HKQuantityTypeIdentifierOxygenSaturation",
         "startDate": "2026-01-01 03:00:00 -0500", "value": "0.97"},
    ])
    ingest.run(adapter, export, root=store_root)

    expected = {"hrv": 55.0, "rhr": 48.0, "resp-rate": 14.2, "spo2": 97.0}  # spo2 = 0.97 * 100
    for item, value in expected.items():
        readings = store.read(item, root=store_root)
        assert len(readings) == 1, item
        assert readings[0]["value"] == value, item
        assert readings[0]["timepoint"] == "2026-01-01"
        assert readings[0]["source"] == "healthkit"
        assert set(readings[0]) >= set(store.keying.LINE_FIELDS)


def test_healthkit_aggregates_raw_samples_to_daily_mean(tmp_path, store_root):
    """AC-2: Apple's RAW per-sample records aggregate to ONE daily-MEAN reading per (item, day).

    Apple records many samples a day; the adapter rolls them up to one value per (item, day) — the
    granularity difference from Whoop's pre-aggregated DB. Two HRV samples on one day -> one reading
    carrying their mean; a regression that yielded a reading PER sample (no aggregation) would red
    this (len 2 -> 1, and the value would not be the mean).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-01-02 02:00:00 -0500", "value": "50"},
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-01-02 08:00:00 -0500", "value": "60"},
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1                            # one daily reading, not one per sample
    assert hrv[0]["timepoint"] == "2026-01-02"
    assert hrv[0]["value"] == 55.0                  # mean(50, 60)


def test_healthkit_unmapped_type_yields_no_reading(tmp_path, store_root):
    """An unmapped HK type (e.g. step count) yields no reading — only the mapped metrics import."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        {"type": "HKQuantityTypeIdentifierStepCount",
         "startDate": "2026-01-03 08:00:00 -0500", "value": "8000"},
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-01-03 08:00:00 -0500", "value": "57"},
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    assert len(store.read("hrv", root=store_root)) == 1
    assert store.read("steps", root=store_root) == []   # the unmapped type wrote nothing


@pytest.mark.parametrize("make_bad", ["missing", "not-xml"])
def test_healthkit_read_fails_loud_on_bad_export(tmp_path, make_bad):
    """A missing file and a non-XML file each RAISE (never silently import nothing).

    read_readings is a generator, so the raise fires on consumption — list(...) forces it.
    """
    from scripts.ingest.adapters import healthkit

    if make_bad == "missing":
        path = tmp_path / "nope.xml"
    else:  # not-xml: a file that is not valid XML
        path = tmp_path / "junk.xml"
        path.write_text("this is not xml at all <<<")

    with pytest.raises((OSError, ET.ParseError)):
        list(healthkit.HealthKitAdapter().read_readings(path))


# --- Store-adversarial battery on the healthkit path (docs/checklists/store-adversarial-tests.md) ---


def _hk_hrv(day, value):
    """One HealthKit HRV `<Record>` dict for the given day (08:00 sample)."""
    return hk_record("HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
                     f"{day} 08:00:00 -0500", value)


def test_healthkit_cross_stream_no_collision(tmp_path, store_root):
    """Adversarial (1: cross-stream): an hrv read never returns an rhr value (S41 namespacing)."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        _hk_hrv("2026-03-01", "58"),
        {"type": "HKQuantityTypeIdentifierRestingHeartRate",
         "startDate": "2026-03-01 06:00:00 -0500", "value": "52"},
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    assert [r["value"] for r in store.read("hrv", root=store_root)] == [58.0]
    assert [r["value"] for r in store.read("rhr", root=store_root)] == [52.0]
    assert all(r["item"] == "hrv" for r in store.read("hrv", root=store_root))


def test_healthkit_rerun_appends_zero_duplicates(tmp_path, store_root):
    """Adversarial (2: same-key dedupe): re-running the same export appends 0 duplicate lines."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [_hk_hrv("2026-03-02", "58"), _hk_hrv("2026-03-03", "60")])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)
    first = len(store.read("hrv", root=store_root))
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)   # identical re-run
    assert first == 2
    assert len(store.read("hrv", root=store_root)) - first == 0


def test_healthkit_distinct_days_both_persist(tmp_path, store_root):
    """Adversarial (2/4: same-key + keying mutation): two hrv readings on distinct days persist.

    A mutation mapping every sample to one constant timepoint would collide the two days on
    (item, timepoint, source) and silently drop one — this REDs (len 2 -> 1).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [_hk_hrv("2026-03-04", "55"), _hk_hrv("2026-03-05", "62")])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert {r["timepoint"] for r in hrv} == {"2026-03-04", "2026-03-05"}
    assert len(hrv) == 2


def test_healthkit_same_identity_changed_value_drops_second(tmp_path, store_root):
    """Adversarial (3: dedupe-key boundary — value): same (item, day, source), new value -> second
    write dropped, first value wins (value is EXCLUDED from the dedupe key)."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export1 = tmp_path / "export1.xml"
    _write_healthkit_export(export1, [_hk_hrv("2026-03-06", "55")])
    ingest.run(healthkit.HealthKitAdapter(), export1, root=store_root)

    export2 = tmp_path / "export2.xml"   # same day, recomputed value
    _write_healthkit_export(export2, [_hk_hrv("2026-03-06", "80")])
    ingest.run(healthkit.HealthKitAdapter(), export2, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1            # same identity -> second dropped
    assert hrv[0]["value"] == 55.0  # first stored value wins


def test_healthkit_distinct_source_from_whoop_does_not_collide(tmp_path, store_root):
    """Adversarial (3: dedupe-key boundary — source): a HealthKit hrv and a Whoop hrv at the same
    (item, day) BOTH persist; `source` distinguishes device provenance.

    This is WHY the adapter emits source="healthkit" (device-specific) not a shared "wearable" tag —
    a shared tag would collide the two and silently drop one (the S41 dropped-reading class). It also
    demonstrates the operator can run Apple Health and Whoop side by side (the answer to 'instead of
    Whoop' is to provide a HealthKit export; the sources never collide).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit, whoop

    hk = tmp_path / "export.xml"
    _write_healthkit_export(hk, [_hk_hrv("2026-03-07", "58")])
    ingest.run(healthkit.HealthKitAdapter(), hk, root=store_root)

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-03-07", "avgHrv": 61.0}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 2
    assert {r["source"] for r in hrv} == {"healthkit", "whoop"}


# --- healthkit boundary / realism coverage (QA Tier-2) ---


def test_healthkit_parses_nested_children_records(tmp_path, store_root):
    """The REAL Apple shape: a <Record> with NESTED children still maps on the Record's own attributes.

    Real Apple exports nest children inside a Record (MetadataEntry, HeartRateVariabilityMetadataList ->
    InstantaneousBeatsPerMinute); the `_write_healthkit_export` fixture emits only flat Records, so this
    pins the nested case. A regression in the iterparse/clear interaction (reading a child's attrs, or
    clearing on the wrong event) would red here — the value must be the Record's 55, never the nested bpm.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    export.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
        ' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Apple Watch"'
        ' startDate="2026-04-01 08:00:00 -0500" endDate="2026-04-01 08:00:00 -0500" value="55">\n'
        '  <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="0"/>\n'
        '  <HeartRateVariabilityMetadataList>\n'
        '   <InstantaneousBeatsPerMinute bpm="62" time="08:00:00.00"/>\n'
        '  </HeartRateVariabilityMetadataList>\n'
        ' </Record>\n'
        ' <Record type="HKQuantityTypeIdentifierRestingHeartRate" sourceName="Apple Watch"'
        ' startDate="2026-04-01 06:00:00 -0500" endDate="2026-04-01 06:00:00 -0500" value="48"/>\n'
        '</HealthData>\n'
    )
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1 and hrv[0]["value"] == 55.0   # the Record's attr, NOT the nested bpm="62"
    assert len(store.read("rhr", root=store_root)) == 1


def test_healthkit_skips_record_missing_startdate_or_value(tmp_path, store_root):
    """A Record missing startDate OR value is SKIPPED (honest absence — the guard), not fabricated."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    export.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData>\n'
        ' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" value="55"/>\n'           # no startDate
        ' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        ' startDate="2026-04-02 08:00:00 -0500"/>\n'                                                # no value
        ' <Record type="HKQuantityTypeIdentifierRestingHeartRate"'
        ' startDate="2026-04-02 06:00:00 -0500" value="48"/>\n'
        '</HealthData>\n'
    )
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    assert store.read("hrv", root=store_root) == []          # both incomplete hrv records skipped
    assert len(store.read("rhr", root=store_root)) == 1      # the complete record imported


def test_healthkit_fails_loud_on_non_numeric_value(tmp_path):
    """A non-numeric value on a MAPPED record raises (record-level fail-loud, distinct from a bad file).

    A future refactor wrapping float() in a try/except would silently drop corrupt samples — this REDs.
    """
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    export.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData>\n'
        ' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        ' startDate="2026-04-03 08:00:00 -0500" value="not-a-number"/>\n'
        '</HealthData>\n'
    )
    with pytest.raises(ValueError):
        list(healthkit.HealthKitAdapter().read_readings(export))


def test_healthkit_empty_export_yields_nothing(tmp_path, store_root):
    """An empty-but-valid export (no Records) yields 0 readings and does NOT raise (the absence complement
    of the fail-loud-on-bad-file test)."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    export.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<HealthData></HealthData>\n')
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)
    assert store.read("hrv", root=store_root) == []


def test_healthkit_spo2_sub_percent_rounds_to_two_decimals(tmp_path, store_root):
    """spo2 sub-percent precision: 0.976 -> 97.6 (round to 2 decimals after ×100). The clean 0.97 map
    case cannot catch a rounding regression (0.97×100=97.0 is already clean); this sub-percent case can."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        {"type": "HKQuantityTypeIdentifierOxygenSaturation",
         "startDate": "2026-04-04 03:00:00 -0500", "value": "0.976"},
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)
    assert store.read("spo2", root=store_root)[0]["value"] == 97.6


def test_healthkit_daily_mean_rounds_to_two_decimals(tmp_path, store_root):
    """A non-terminating daily mean on a NON-spo2 metric is stored rounded to 2 decimals (ADR-0012 D2).

    Three hrv samples 50/51/53 mean to 51.333333…; the stored value must be 51.33. The spo2 case
    cannot catch this — 0.976×100 is exact in IEEE-754 — so this pins the round() on a metric whose
    raw mean has >2 decimals. Removing `round(...)` stores 51.333333333333336 and REDs this.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        _hk_hrv("2026-04-06", "50"), _hk_hrv("2026-04-06", "51"), _hk_hrv("2026-04-06", "53"),
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)
    assert store.read("hrv", root=store_root)[0]["value"] == 51.33


def test_healthkit_two_metrics_same_day_aggregate_independently(tmp_path, store_root):
    """Two DIFFERENT metrics with two samples each on ONE day produce two INDEPENDENT daily means — the
    per-(item, day) accumulator key. A regression keying on day-only (dropping item) would average across
    metrics (hrv contaminated by rhr) and red this."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    hrv_t = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"
    rhr_t = "HKQuantityTypeIdentifierRestingHeartRate"
    export = tmp_path / "export.xml"
    _write_healthkit_export(export, [
        {"type": hrv_t, "startDate": "2026-04-05 02:00:00 -0500", "value": "50"},
        {"type": hrv_t, "startDate": "2026-04-05 08:00:00 -0500", "value": "60"},
        {"type": rhr_t, "startDate": "2026-04-05 03:00:00 -0500", "value": "46"},
        {"type": rhr_t, "startDate": "2026-04-05 09:00:00 -0500", "value": "50"},
    ])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)

    assert store.read("hrv", root=store_root)[0]["value"] == 55.0   # mean(50,60) — not contaminated by rhr
    assert store.read("rhr", root=store_root)[0]["value"] == 48.0   # mean(46,50)


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
    (empty output). `pre-garmin` is the `_baseline_ref` baseline (see that function
    for the fork-point/distinctness rationale). An unchanged path emits NO numstat
    row, so the pass condition is an EMPTY row list, NOT a literal "0" token. The
    Garmin source was added by creating ONE adapter module; ingest.py + adapter.py
    are untouched, so the diff is empty. The gate's teeth are proven by
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


def test_zero_edit_gate_reds_on_committed_routine_edit(tmp_path):
    """The MAIN 0-edit gate (_numstat_rows over the real _baseline_ref) turns RED on a
    COMMITTED shared-routine edit. A _baseline_ref that resolved to HEAD's tree would
    report EMPTY here (HEAD == working tree both carry the edit) and this test would
    FAIL — so it catches the exact tautology a HEAD-relative baseline would reintroduce.
    Uses a committed probe (an uncommitted working-tree edit is caught by any baseline
    and would not distinguish a tautological baseline)."""
    ingest = REPO_ROOT / "scripts" / "ingest" / "ingest.py"
    original = ingest.read_text()
    committed = False
    try:
        ingest.write_text(original + "\n# falsifiability probe\n")
        subprocess.run(["git", "add", str(ingest)], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "test probe: 0-edit falsifiability"],
                       cwd=REPO_ROOT, check=True)
        committed = True
        rows = _numstat_rows(_baseline_ref("committed-falsifiability-probe"), SHARED_ROUTINE_PATHS)
        assert any(r.endswith("scripts/ingest/ingest.py") for r in rows), rows
    finally:
        if committed:
            subprocess.run(["git", "reset", "-q", "--mixed", "HEAD^"], cwd=REPO_ROOT, check=True)
        ingest.write_text(original)
        subprocess.run(["git", "checkout", "--", str(ingest)], cwd=REPO_ROOT, check=True)


# --- Cycle 3: Whoop wired read-only-SQLite adapter (ADR-0011 D2 v2) ---
#
# The former registered-but-unwired JSON scaffold (`{metric_name,cycle_start,
# score}` — a fabricated shape matching no real noop/WHOOP artifact, ADR-0011) is
# replaced by an adapter that reads noop's documented on-device SQLite
# (`docs/DATA_MODEL.md` `dailyMetric`, schemaVersion 9). These tests build a
# synthetic `whoop.sqlite` matching that schema so the adapter exercises its real
# read path, then run the store-adversarial battery
# (`docs/checklists/store-adversarial-tests.md`) over the whoop write path.


def _write_whoop_sqlite(path, rows):
    """Build a synthetic noop `whoop.sqlite` with a `dailyMetric` table + rows.

    Mirrors noop's documented schema (`docs/DATA_MODEL.md`, schemaVersion 9): one
    row per calendar `day`, every metric column nullable. `rows` is a list of
    dicts keyed by the `dailyMetric` columns the adapter reads
    (`day` + recovery/strain/avgHrv/restingHr/efficiency/spo2Pct/respRateBpm/
    skinTempDevC); an omitted column defaults to NULL. Building the real schema
    (not a stand-in shape) keeps the test exercising the adapter's actual SQL read.
    """
    import sqlite3

    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "CREATE TABLE dailyMetric ("
            "deviceId TEXT NOT NULL, day TEXT NOT NULL, "
            "totalSleepMin REAL, efficiency REAL, deepMin REAL, remMin REAL, "
            "lightMin REAL, disturbances INTEGER, restingHr INTEGER, avgHrv REAL, "
            "recovery REAL, strain REAL, exerciseCount INTEGER, spo2Pct REAL, "
            "skinTempDevC REAL, respRateBpm REAL, "
            "PRIMARY KEY (deviceId, day))"
        )
        cols = (
            "deviceId", "day", "recovery", "strain", "avgHrv", "restingHr",
            "efficiency", "spo2Pct", "respRateBpm", "skinTempDevC",
        )
        for r in rows:
            values = [r.get("deviceId", "dev1"), r["day"]] + [r.get(c) for c in cols[2:]]
            placeholders = ", ".join("?" for _ in values)
            conn.execute(
                f"INSERT INTO dailyMetric ({', '.join(cols)}) VALUES ({placeholders})",
                values,
            )
        conn.commit()
    finally:
        conn.close()


def test_whoop_reads_daily_metric_from_readonly_sqlite(tmp_path, store_root):
    """ADR-0011 D2: the Whoop adapter maps noop's `dailyMetric` into field-set readings.

    Builds a synthetic noop `whoop.sqlite` (documented schema), runs it through the
    UNCHANGED ingest.run, and asserts each non-null metric lands on its own
    (item, day, "whoop") stream carrying every Line Field Set field. Conforms to
    the @runtime_checkable Adapter contract.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapter import Adapter
    from scripts.ingest.adapters import whoop

    adapter = whoop.WhoopAdapter()
    assert isinstance(adapter, Adapter)  # exposes the frozen contract surface
    assert adapter.source_tag() == "whoop"

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(
        db,
        [
            {
                "day": "2026-02-01", "recovery": 66.0, "strain": 14.5, "avgHrv": 58.0,
                "restingHr": 52, "efficiency": 91.0, "spo2Pct": 97.0,
                "respRateBpm": 14.2, "skinTempDevC": -0.3,
            }
        ],
    )
    ingest.run(adapter, db, root=store_root)

    recovery = store.read("recovery", root=store_root)
    hrv = store.read("hrv", root=store_root)
    assert len(recovery) == 1 and len(hrv) == 1
    for reading in (*recovery, *hrv):
        assert set(reading) >= set(store.keying.LINE_FIELDS)
        assert reading["source"] == "whoop"
        assert reading["timepoint"] == "2026-02-01"
    # Each column maps to its OWN item stream carrying the CORRECT value. Pinning
    # the value per stream (not just presence) REDs a transposed column->item
    # mapping (e.g. spo2Pct<->respRateBpm), which would land a wrong physiological
    # value on the wrong stream — the S41 fabricated-biomarker class.
    expected = {
        "recovery": 66.0, "strain": 14.5, "hrv": 58.0, "rhr": 52,
        "sleep-efficiency": 91.0, "spo2": 97.0, "resp-rate": 14.2,
        "skin-temp-dev": -0.3,
    }
    for item, value in expected.items():
        readings = store.read(item, root=store_root)
        assert len(readings) == 1, item
        assert readings[0]["value"] == value, item


def test_whoop_strain_stays_on_0_to_21_scale(tmp_path, store_root):
    """AC2 (mutation guard): strain is carried through on WHOOP's 0-21 scale.

    A 0-100 render of Day Strain is ~5x wrong (ADR-0011; noop's
    `dayStrainToEffortScale = 100/21`). This pins the raw 0-21 value end-to-end: a
    fixture strain of 14.5 must store as 14.5, NOT rescaled to ~69 (14.5*100/21) or
    ~3.0 (14.5*21/100). Were `read_readings` to rescale strain, this REDs (the
    deliberate-break mutation for the value-mapping surface).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-02-02", "strain": 14.5}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    strain = store.read("strain", root=store_root)
    assert len(strain) == 1
    assert strain[0]["value"] == 14.5  # 0-21 scale, unscaled


def test_whoop_skips_null_metrics(tmp_path, store_root):
    """A NULL `dailyMetric` column yields no reading (honest absence, no fabricated value)."""
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    # Only recovery present this day; the other seven mapped columns are NULL.
    _write_whoop_sqlite(db, [{"day": "2026-02-03", "recovery": 70.0}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    assert len(store.read("recovery", root=store_root)) == 1
    assert store.read("strain", root=store_root) == []
    assert store.read("hrv", root=store_root) == []


def test_whoop_retains_honest_zero_values(tmp_path, store_root):
    """A legitimate 0 metric is RETAINED — the skip is `value is None`, not falsy.

    A zero-strain rest day or a 0.0 skin-temp deviation are real readings, not
    absences. Pins that the NULL-skip discriminates None from a falsy 0: a
    `if not value:` regression would silently DROP honest zeros (the S41
    dropped-reading class) — this REDs under that mutation.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-02-12", "strain": 0, "skinTempDevC": 0.0}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    strain = store.read("strain", root=store_root)
    skin = store.read("skin-temp-dev", root=store_root)
    assert len(strain) == 1 and strain[0]["value"] == 0
    assert len(skin) == 1 and skin[0]["value"] == 0.0


@pytest.mark.parametrize("make_bad", ["missing", "not-sqlite", "no-table"])
def test_whoop_read_fails_loud_on_bad_db(tmp_path, make_bad):
    """The documented fail-loud paths RAISE (never silently import nothing).

    A missing file, a non-SQLite file, and a SQLite DB without `dailyMetric` each
    raise rather than yielding 0 readings. `read_readings` is a generator, so the
    raise fires on consumption — `list(...)` forces it. Guards the docstring's
    fail-loud contract against a future swallow-everything refactor.
    """
    import sqlite3

    from scripts.ingest.adapters import whoop

    if make_bad == "missing":
        path = tmp_path / "nope.sqlite"
    elif make_bad == "not-sqlite":
        path = tmp_path / "junk.sqlite"
        path.write_bytes(b"not a sqlite file at all")
    else:  # no-table: a valid sqlite DB lacking the dailyMetric table
        path = tmp_path / "empty.sqlite"
        conn = sqlite3.connect(path)
        conn.execute("CREATE TABLE other (x INTEGER)")
        conn.commit()
        conn.close()

    with pytest.raises(sqlite3.Error):
        list(whoop.WhoopAdapter().read_readings(path))


def test_whoop_read_is_readonly_does_not_mutate_db(tmp_path, store_root):
    """The adapter opens noop's DB read-only — the source file is byte-identical after.

    `mode=ro` opens O_RDONLY, so the import path cannot write noop's `whoop.sqlite`
    (ADR-0011 license path (a): parse a file the operator owns; the read is one-way).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-02-04", "recovery": 60.0}])
    before = db.read_bytes()
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)
    assert db.read_bytes() == before  # source DB unchanged by the read


# --- Store-adversarial battery on the whoop path (docs/checklists/store-adversarial-tests.md) ---


def test_whoop_cross_stream_no_collision(tmp_path, store_root):
    """Adversarial (1: cross-stream): a recovery read never returns a strain value.

    recovery and strain share a day but are distinct items; store.read("recovery")
    returns only recovery, store.read("strain") only strain — the cross-stream
    namespacing the S41 fabricated-biomarker case exists to prevent, exercised over
    the whoop write path.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-02-05", "recovery": 66.0, "strain": 14.5}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    recovery = store.read("recovery", root=store_root)
    strain = store.read("strain", root=store_root)
    assert [r["value"] for r in recovery] == [66.0]
    assert [r["value"] for r in strain] == [14.5]
    assert all(r["item"] == "recovery" for r in recovery)
    assert all(r["item"] == "strain" for r in strain)


def test_whoop_rerun_appends_zero_duplicates(tmp_path, store_root):
    """Adversarial (2: same-key dedupe): re-running the same DB appends 0 duplicate lines.

    Idempotent on the (item, day, "whoop") key — a second ingest over the unchanged
    DB adds nothing (inherited from store.append's shared-key dedupe).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(
        db,
        [{"day": "2026-02-06", "recovery": 66.0}, {"day": "2026-02-07", "recovery": 70.0}],
    )
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)
    first = len(store.read("recovery", root=store_root))
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)
    second = len(store.read("recovery", root=store_root))
    assert first == 2
    assert second - first == 0


def test_whoop_distinct_days_both_persist(tmp_path, store_root):
    """Adversarial (2/4: same-key + mutation): two recovery readings on distinct days persist.

    Distinct (item, day) identities must NOT dedupe-collapse — the complement of
    the idempotent re-run. This is also the keying mutation guard for the whoop
    path: were `read_readings` to map every row to one constant timepoint, the two
    days would collide on (item, timepoint, source) and one would silently drop,
    reding this assertion (len 2 -> 1).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(
        db,
        [{"day": "2026-02-08", "recovery": 60.0}, {"day": "2026-02-09", "recovery": 75.0}],
    )
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)
    recovery = store.read("recovery", root=store_root)
    assert {r["timepoint"] for r in recovery} == {"2026-02-08", "2026-02-09"}
    assert len(recovery) == 2


def test_whoop_same_identity_changed_value_drops_second(tmp_path, store_root):
    """Adversarial (3: dedupe-key boundary — value): same (item, day, source), new value
    -> second write dropped, first value wins (value is EXCLUDED from the key).

    noop upserts `dailyMetric` (latest value wins on-device), so a day's recovery
    can change between runs; on normal ingest the store keeps the FIRST stored
    value (a real revision uses store.correct, ADR-0002 v1.4). Pins that `value`
    is not part of the dedupe identity. A mutation widening the key to include
    `value` would keep BOTH (len 2) and red this.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import whoop

    db1 = tmp_path / "whoop1.sqlite"
    _write_whoop_sqlite(db1, [{"day": "2026-02-10", "recovery": 60.0}])
    ingest.run(whoop.WhoopAdapter(), db1, root=store_root)

    db2 = tmp_path / "whoop2.sqlite"  # same day, recomputed value
    _write_whoop_sqlite(db2, [{"day": "2026-02-10", "recovery": 80.0}])
    ingest.run(whoop.WhoopAdapter(), db2, root=store_root)

    recovery = store.read("recovery", root=store_root)
    assert len(recovery) == 1  # same identity -> second dropped
    assert recovery[0]["value"] == 60.0  # first stored value wins


def test_whoop_distinct_source_from_other_wearable_does_not_collide(tmp_path, store_root):
    """Adversarial (3: dedupe-key boundary — source): a Whoop hrv and an Oura hrv at the
    same (item, day) BOTH persist; `source` distinguishes device provenance.

    This is exactly WHY the adapter emits source="whoop" (device-specific) rather
    than a shared "wearable" tag — a shared tag would collide the two on
    (item, day, source) and silently drop one (the S41 dropped-reading class).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import oura, whoop

    db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(db, [{"day": "2026-02-11", "avgHrv": 58.0}])
    ingest.run(whoop.WhoopAdapter(), db, root=store_root)

    oura_export = tmp_path / "oura.json"
    _write_json_export(oura_export, [{"metric": "hrv", "day": "2026-02-11", "average": 61}])
    ingest.run(oura.OuraAdapter(), oura_export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 2
    assert {r["source"] for r in hrv} == {"whoop", "oura"}


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
    emits 0 rows: the rename touched only garmin.py. `pre-format-rename` is the
    `_baseline_ref` baseline, distinct from `pre-garmin` (see that function for the
    fork-point/distinctness rationale). Gate teeth proven by
    `test_format_rename_zero_edit_gate_is_falsifiable`; distinctness from
    pre-garmin by `test_two_zero_edit_baselines_are_distinct`.
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


# --- Cross-source dedupe complement (keying.DEDUPE_FIELDS includes source) ---


def test_cross_source_same_item_timepoint_does_not_dedupe(tmp_path, store_root):
    """Two readings with the SAME item+timepoint but DIFFERENT source do NOT dedupe.

    The dedupe identity is (item, timepoint, source) — `source` is part of
    `keying.DEDUPE_FIELDS` and is the field each adapter uniquely supplies. Running
    HealthKit (`hrv@T`) then Oura (`hrv@T`) through the SAME store_root keeps BOTH
    readings: the differing source gives them distinct identities. This is the
    complement of the same-source dedupe proof and reds if `source` were dropped
    from the dedupe key (the two would then collapse to one).
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit, oura

    # HealthKit keys its timepoint to the DAY; the Oura fixture uses the same date so the two land
    # on the SAME (item, timepoint) and the test exercises source-distinguishes-identity.
    hk_export = tmp_path / "export.xml"
    _write_healthkit_export(hk_export, [_hk_hrv("2026-01-06", "55")])
    oura_export = tmp_path / "oura.json"
    _write_json_export(oura_export, [{"metric": "hrv", "day": "2026-01-06", "average": 58}])

    ingest.run(healthkit.HealthKitAdapter(), hk_export, root=store_root)
    ingest.run(oura.OuraAdapter(), oura_export, root=store_root)

    hrv = store.read("hrv", root=store_root)
    # Both readings survive: same item+timepoint, distinct source -> distinct identity.
    assert len(hrv) == 2
    assert {r["source"] for r in hrv} == {"healthkit", "oura"}


# --- SEC-001 over the adapter path: an unsafe mapped item writes nothing outside ---


@pytest.mark.parametrize("bad_item", ["../escaped/pwn", "/tmp/abs-pwn", "a/b"])
def test_garmin_traversing_item_raises_writes_nothing(tmp_path, bad_item):
    """SEC-001 on the adapter path: an unsafe `summaryType` raises, writes nothing.

    The adapter maps an export field into `reading["item"]`, so an untrusted
    `summaryType` flows item -> ingest.run -> store.append -> store._item_path,
    which carries the S32 SEC-001 containment guard (resolved store path must be a
    direct child of the root; `..` traversal, an absolute path, and a multi-segment
    `a/b` all escape). Running such an export raises ValueError and leaves nothing
    outside the tmp store_root.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import garmin

    root = tmp_path / "store"
    outside = tmp_path / "escaped"  # sibling of the store root the "../escaped" item targets
    export = tmp_path / "garmin_evil.json"
    _write_json_export(
        export,
        [{"summaryType": bad_item, "calendarDate": "2026-01-07T08:00", "value": 1}],
    )

    with pytest.raises(ValueError):
        ingest.run(garmin.GarminAdapter(), export, root=root)
    # Nothing was written outside the store root (the escape target does not exist).
    assert not outside.exists()


# --- ADR-0013-T3: zip-aware HealthKit adapter (read_readings accepts an Apple Health zip) ---
#
# read_readings now detects an Apple Health export `.zip` (zipfile.is_zipfile),
# extracts its single `*/export.xml` member (streamed, mirroring dna.land), and runs
# the existing iterparse read over it. A raw export.xml reads as today; a zip with no
# export.xml (or a non-zip non-xml) fails loud. The extraction lives ONLY in the
# adapter — ingest.py / adapter.py / scheduler.py are byte-unchanged (AC-5).


def _zip_apple_health_export(zip_path, xml_bytes, *, member="apple_health_export/export.xml",
                             noise=True):
    """Write an Apple-Health-shaped export `.zip` wrapping `xml_bytes` at `member`.

    Mirrors a real Apple export: the `export.xml` lives under a directory member, and
    the zip carries macOS noise (a `__MACOSX/` resource-fork entry + the directory
    entry) the member-locate must skip. When `member` is None, NO `export.xml`-shaped
    member is written (the fail-loud fixture).
    """
    with zipfile.ZipFile(zip_path, "w") as zf:
        if noise:
            zf.writestr("apple_health_export/", b"")               # a directory entry
            zf.writestr("__MACOSX/._export.xml", b"resource-fork") # an Apple resource fork
            zf.writestr("apple_health_export/export_cda.xml", b"<ClinicalDocument/>")  # a sibling
        if member is not None:
            zf.writestr(member, xml_bytes)


# Cycle 1: zip == extracted-xml + raw passthrough + fail-loud (AC-1, AC-2, AC-3)


def test_healthkit_zip_yields_same_readings_as_extracted_xml(tmp_path, store_root):
    """AC-1: read_readings on an Apple-Health zip yields the SAME readings as on its export.xml.

    Builds one synthetic export.xml, then a zip wrapping that SAME xml under
    `apple_health_export/export.xml` (+ __MACOSX noise + a directory entry). The
    reading list read from the zip must equal the reading list read from the raw xml.
    A read that ignored the zip (ran iterparse over the zip's bytes) would raise or
    yield nothing and red this.
    """
    from scripts.ingest.adapters import healthkit

    xml_path = tmp_path / "export.xml"
    _write_healthkit_export(xml_path, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-05-01 08:00:00 -0500", "value": "55"},
        {"type": "HKQuantityTypeIdentifierRestingHeartRate",
         "startDate": "2026-05-01 06:00:00 -0500", "value": "48"},
        {"type": "HKQuantityTypeIdentifierOxygenSaturation",
         "startDate": "2026-05-01 03:00:00 -0500", "value": "0.97"},
    ])
    zip_path = tmp_path / "apple_health_export.zip"
    _zip_apple_health_export(zip_path, xml_path.read_bytes())

    adapter = healthkit.HealthKitAdapter()
    from_xml = list(adapter.read_readings(xml_path))
    from_zip = list(adapter.read_readings(zip_path))
    assert from_zip == from_xml
    # Pin the content too, so an empty-equals-empty pass cannot sneak through.
    assert {r["item"]: r["value"] for r in from_zip} == {"hrv": 55.0, "rhr": 48.0, "spo2": 97.0}


def test_healthkit_zip_ingests_through_run(tmp_path, store_root):
    """AC-1 (store leg): an Apple-Health zip ingests through the UNCHANGED ingest.run.

    The zip flows adapter.read_readings -> ingest.run -> store.append exactly as a
    raw export.xml does; the inner readings land on their (item, day, "healthkit")
    streams. Confirms zip-awareness composes with the unchanged shared routine.
    """
    from scripts.ingest import ingest
    from scripts.ingest.adapters import healthkit

    xml_path = tmp_path / "export.xml"
    _write_healthkit_export(xml_path, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-05-02 08:00:00 -0500", "value": "60"},
    ])
    zip_path = tmp_path / "apple_health_export.zip"
    _zip_apple_health_export(zip_path, xml_path.read_bytes())

    ingest.run(healthkit.HealthKitAdapter(), zip_path, root=store_root)
    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1
    assert hrv[0]["value"] == 60.0 and hrv[0]["timepoint"] == "2026-05-02"
    assert hrv[0]["source"] == "healthkit"


def test_healthkit_raw_xml_reads_as_today(tmp_path, store_root):
    """AC-2: a raw export.xml still reads exactly as today (the non-zip passthrough).

    The dna.land raw-.txt passthrough analog — a pre-extracted export.xml is not a
    zip, so the existing iterparse read runs over it unchanged.
    """
    from scripts.ingest.adapters import healthkit

    xml_path = tmp_path / "export.xml"
    _write_healthkit_export(xml_path, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-05-03 08:00:00 -0500", "value": "57"},
        {"type": "HKQuantityTypeIdentifierRespiratoryRate",
         "startDate": "2026-05-03 03:00:00 -0500", "value": "14.0"},
    ])
    readings = list(healthkit.HealthKitAdapter().read_readings(xml_path))
    assert {r["item"]: r["value"] for r in readings} == {"hrv": 57.0, "resp-rate": 14.0}


def test_healthkit_zip_without_export_xml_fails_loud(tmp_path):
    """AC-3a: a zip with NO `*/export.xml` member raises, naming the missing member.

    The `_genotype_member` fail-loud analog — a zip that is not an Apple Health export
    (no export.xml inside) is not silently imported as nothing.
    """
    from scripts.ingest.adapters import healthkit

    zip_path = tmp_path / "wrong.zip"
    # member=None: no export.xml-shaped member is written (only the noise members).
    _zip_apple_health_export(zip_path, b"", member=None)

    with pytest.raises(ValueError, match="export.xml"):
        list(healthkit.HealthKitAdapter().read_readings(zip_path))


def test_healthkit_non_zip_non_xml_fails_loud(tmp_path):
    """AC-3b: a non-zip non-xml file raises (the existing fail-loud-on-malformed posture).

    Not a zip (so the extraction branch is skipped) and not valid XML (so iterparse
    raises). The fail-loud signal of a misconfigured path / wrong file.
    """
    from scripts.ingest.adapters import healthkit

    junk = tmp_path / "junk.bin"
    junk.write_bytes(b"this is neither a zip nor xml \x00\x01\x02 <<<")

    with pytest.raises((OSError, ET.ParseError, ValueError)):
        list(healthkit.HealthKitAdapter().read_readings(junk))


# Cycle 2: streamed copy + 0-shared-routine-edit proof + dual-entry-point (AC-4, AC-5, AC-6)


def test_healthkit_inner_xml_copy_is_streamed(tmp_path):
    """AC-4 (Risk 07f6): the inner-xml copy is streamed (shutil.copyfileobj), not single-shot.

    The extracted export.xml can be hundreds of MB; the copy must stream it like
    dna.land does. Asserts the adapter source uses `shutil.copyfileobj` and does NOT
    do a single-shot full-member `.read()` of the zip member (which would buffer the
    whole xml in memory).
    """
    src = (REPO_ROOT / "scripts" / "ingest" / "adapters" / "healthkit.py").read_text()
    assert "shutil.copyfileobj" in src, "the inner-xml copy must stream via shutil.copyfileobj"
    # No single-shot full-member read of the zip member: a `member.read()` / `zf.read(` with no
    # size arg would buffer the whole (100s-of-MB) member — the anti-pattern AC-4 forbids.
    assert ".read()" not in src, "no single-shot full-member .read() of the zip member"
    assert "zf.read(" not in src, "no single-shot zf.read() of the whole member"


def test_healthkit_zip_extraction_zero_shared_routine_edits():
    """AC-5: the zip-awareness changes 0 lines in the shared routine (ingest/adapter/scheduler).

    `git diff --numstat <pre-task> -- ingest.py adapter.py scheduler.py` emits 0 rows.
    The fork-point baseline (_baseline_ref) is the pre-task tree, so a COMMITTED edit
    to any of the three would emit a row and red this. healthkit.py is EXCLUDED (it is
    the adapter under edit). The gate's teeth are proven by the negative control below.
    """
    pre_task = _baseline_ref("pre-zip-healthkit")
    rows = _numstat_rows(pre_task, SHARED_ROUTINE_PATHS_FULL)
    assert rows == [], (
        f"expected 0 changed lines in {SHARED_ROUTINE_PATHS_FULL} vs pre-zip-healthkit; "
        f"got numstat rows {rows} — the zip-awareness leaked into the shared routine"
    )


def test_healthkit_zip_zero_edit_gate_is_falsifiable(tmp_path):
    """Negative control for AC-5: the 0-edit numstat gate turns RED on a real shared-routine edit.

    Runs the SAME `git diff --numstat` row-detection against a one-line-modified COPY
    of the committed ingest.py (via `git diff --no-index`) and asserts it emits one
    changed-file row — proving the AC-5 assertion is failing-capable, not tautological.
    The real ingest.py is never touched.
    """
    committed = REPO_ROOT / "scripts" / "ingest" / "ingest.py"
    probed = tmp_path / "ingest_probe.py"
    probed.write_text(committed.read_text() + "# zip-task negative-control probe line\n")

    out = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(committed), str(probed)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    ).stdout
    rows = [line for line in out.splitlines() if line.strip()]
    assert len(rows) == 1, f"the one-line probe must make numstat emit exactly one row; got {rows}"
    assert rows[0].split("\t")[0] == "1"


def test_healthkit_zip_ingests_via_cli_dual_entry_point(tmp_path, monkeypatch):
    """AC-6: an Apple-Health zip ingests via the CLI path (`-m scripts.ingest --source healthkit`).

    Invokes the CLI `main(["<zip>", "--source", "healthkit", "--root", <store>])`
    in-process; the now-zip-aware adapter accepts the zip with NO manual unzip, and
    the inner readings land in the store. This is the dual-entry-point ingestability
    the adapter-layer extraction delivers (vs a serve-layer extraction that would
    leave the CLI needing a manual unzip).
    """
    from scripts.ingest import __main__ as cli

    xml_path = tmp_path / "export.xml"
    _write_healthkit_export(xml_path, [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN",
         "startDate": "2026-05-04 08:00:00 -0500", "value": "62"},
        {"type": "HKQuantityTypeIdentifierRestingHeartRate",
         "startDate": "2026-05-04 06:00:00 -0500", "value": "50"},
    ])
    zip_path = tmp_path / "apple_health_export.zip"
    _zip_apple_health_export(zip_path, xml_path.read_bytes())
    store_dir = tmp_path / "store"

    rc = cli.main([str(zip_path), "--source", "healthkit", "--root", str(store_dir)])
    assert rc == 0
    assert store.read("hrv", root=store_dir)[0]["value"] == 62.0
    assert store.read("rhr", root=store_dir)[0]["value"] == 50.0
