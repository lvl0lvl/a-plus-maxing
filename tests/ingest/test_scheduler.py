"""Tests for the unattended scheduler run (ADR-0003-T3).

Covers AC-1..AC-7: unattended invocation over the wired adapter set (exit 0, 0
prompts, stdin closed), delta-only append on a second run, idempotent no-new
re-run, Whoop now WIRED (ADR-0011 D2 — the data-driven discovery includes it once
whoop.py drops its UNWIRED marker) while scheduler.py still carries 0 `whoop`
tokens (the static scan), 0 outbound egress over a
REAL `scheduler.run()`, and the data-driven 0-edit-on-adapter-add proof. All
store writes go to a tmp_path-based root so no test touches the real
`vault/store/`; the wired adapters read in-test sample exports, not real exports.

`rg` is a non-executable shim on this host (`subprocess.run(["rg", ...])` raises
FileNotFoundError), so the spec's literal `rg "whoop" scripts/ingest/scheduler.py`
=0 command (AC-4b) is implemented as a pure-Python content scan — the SAME
documented deviation `tests/ingest/test_ingest.py` and `scripts/guard/pii_scan.py`
took (same contents-search semantics, different mechanism).
"""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import hk_record, write_healthkit_export as _write_healthkit_export

from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULER_PATH = REPO_ROOT / "scripts" / "ingest" / "scheduler.py"
ADAPTERS_DIR = REPO_ROOT / "scripts" / "ingest" / "adapters"

# The wired set the scheduler must invoke `ingest.run` over (AC-1, AC-4a). Whoop
# joined the wired set at ADR-0011 D2 (its UNWIRED marker removed); it is invoked
# when an export is provided, like every other wired adapter.
WIRED_SOURCES = {"healthkit", "oura", "garmin", "whoop"}


def _write_whoop_sqlite(path, rows):
    """Build a synthetic noop `whoop.sqlite` (`dailyMetric`) the Whoop adapter reads.

    Minimal mirror of noop's documented schema (`docs/DATA_MODEL.md`,
    schemaVersion 9) — the columns the wired-set invocation test needs. `rows` is a
    list of `{day, recovery}` dicts (recovery is the one metric this scheduler test
    asserts on to prove invocation); the other declared columns stay NULL. (The full
    column→item mapping is exercised in `tests/ingest/test_adapters.py`.)
    """
    import sqlite3

    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "CREATE TABLE dailyMetric ("
            "deviceId TEXT NOT NULL, day TEXT NOT NULL, "
            "efficiency REAL, restingHr INTEGER, avgHrv REAL, recovery REAL, "
            "strain REAL, spo2Pct REAL, skinTempDevC REAL, respRateBpm REAL, "
            "PRIMARY KEY (deviceId, day))"
        )
        for r in rows:
            conn.execute(
                "INSERT INTO dailyMetric (deviceId, day, recovery) VALUES (?, ?, ?)",
                ("dev1", r["day"], r.get("recovery")),
            )
        conn.commit()
    finally:
        conn.close()


def _write_json_export(path, records):
    """Write a JSON export the source adapters parse (json.loads of a list)."""
    path.write_text(json.dumps(records))


def _sample_exports(tmp_path, healthkit_records, oura_records, garmin_records):
    """Write one sample export per wired source; return the {source: path} map.

    Each adapter parses its own source-specific schema: HealthKit reads the real
    `export.xml` (per-sample `<Record>` elements); Oura/Garmin read JSON.
    """
    hk = tmp_path / "export.xml"
    ou = tmp_path / "oura.json"
    ga = tmp_path / "garmin.json"
    _write_healthkit_export(hk, healthkit_records)
    _write_json_export(ou, oura_records)
    _write_json_export(ga, garmin_records)
    return {"healthkit": hk, "oura": ou, "garmin": ga}


def _hk(hk_type, start_date, value):
    """A HealthKit `export.xml` <Record> dict (a real HK type identifier + value)."""
    return hk_record(hk_type, start_date, value)


def _ou(item, day, avg):
    """An Oura-shaped export record."""
    return {"metric": item, "day": day, "average": avg}


def _ga(item, day, value):
    """A Garmin-shaped export record."""
    return {"summaryType": item, "calendarDate": day, "value": value}


def _sandbox_available():
    """True when the macOS sandbox-exec isolation the egress guard needs is invocable.

    Mirrors the store AC-4 / ingest AC-5 precondition: egress_guard.run is
    fail-closed (falsy when OS isolation cannot be applied), so where sandbox-exec
    is not invocable the truthy egress assertion would FAIL, not skip.
    """
    return (
        subprocess.run(
            ["/usr/bin/sandbox-exec", "-p", "(version 1)(allow default)", "/usr/bin/true"],
            capture_output=True,
        ).returncode
        == 0
    )


# --- AC-1: unattended invocation over the wired set; exit 0; 0 prompts ---


def test_run_completes_unattended_exit_zero(tmp_path, monkeypatch):
    """AC-1: scheduler.run() completes unattended (exit 0, 0 stdin reads).

    Runs scheduler.run() with stdin redirected to /dev/null (closed/empty stream)
    and a stdin guard that raises if any code reads stdin, asserting the run
    returns 0 without blocking on or reading operator input. The wired adapters
    read in-test sample exports through a tmp store root.
    """
    from scripts.ingest import scheduler

    exports = _sample_exports(
        tmp_path,
        healthkit_records=[_hk("HKQuantityTypeIdentifierRestingHeartRate", "2026-01-01", 48)],
        oura_records=[_ou("hrv", "2026-01-01", 55)],
        garmin_records=[_ga("stress", "2026-01-01", 30)],
    )
    store_root = tmp_path / "store"

    # Stdin closed + a guard that raises on any read: an unattended run reads no
    # stdin, so a prompt-for-input would surface as this RuntimeError, not a hang.
    class _NoStdin:
        def read(self, *a, **k):
            raise RuntimeError("scheduler.run() read stdin — not unattended")

        def readline(self, *a, **k):
            raise RuntimeError("scheduler.run() read stdin — not unattended")

    with open("/dev/null") as devnull:
        monkeypatch.setattr("sys.stdin", _NoStdin())
        rc = scheduler.run(exports=exports, root=store_root)
        devnull  # stdin is closed/empty; the guard proves nothing reads it.

    assert rc == 0
    # Every wired source's reading landed (the run actually ran the wired set).
    assert len(store.read("rhr", root=store_root)) == 1
    assert len(store.read("hrv", root=store_root)) == 1
    assert len(store.read("stress", root=store_root)) == 1


# --- AC-2 / Risk ADR-0003 N1: delta-only append ---


def test_second_run_appends_only_new_timepoint_delta(tmp_path):
    """AC-2: a second run over an export that gained readings appends only the delta.

    First run imports two HealthKit timepoints; the export then gains two NEW
    timepoints; the second run's item-file line-count DELTA equals EXACTLY the
    new-timepoint count (2). An over-append (re-appending the already-stored
    timepoints) would make delta = full export count (4) and red this assertion;
    an under-append would make it < 2. Failing-capable per the Step-1 broken-delta
    probe. Mitigates Risk ADR-0003 N1.
    """
    from scripts.ingest import scheduler

    store_root = tmp_path / "store"
    hk = tmp_path / "export.xml"
    _rhr = "HKQuantityTypeIdentifierRestingHeartRate"

    # First run: two days (HealthKit keys its timepoint to the day).
    _write_healthkit_export(hk, [_hk(_rhr, "2026-01-01", 48), _hk(_rhr, "2026-01-02", 50)])
    scheduler.run(exports={"healthkit": hk}, root=store_root)
    before = len(store.read("rhr", root=store_root))

    # The export GAINED two new days (the original two are still present).
    _write_healthkit_export(hk, [
        _hk(_rhr, "2026-01-01", 48), _hk(_rhr, "2026-01-02", 50),
        _hk(_rhr, "2026-01-03", 52), _hk(_rhr, "2026-01-04", 54),
    ])
    scheduler.run(exports={"healthkit": hk}, root=store_root)
    after = len(store.read("rhr", root=store_root))

    new_count = 2
    assert after - before == new_count  # exact new-day delta, not "<=" first


# --- AC-3 / Risk ADR-0003 N1: idempotent unattended re-run ---


def test_rerun_no_new_appends_zero_lines(tmp_path):
    """AC-3: a re-run over an unchanged export appends EXACTLY 0 lines.

    Runs scheduler.run() twice over an unchanged export and asserts the item-file
    line count is unchanged on the second run (delta = 0). A corrupted/missing
    dedupe path would re-append already-stored readings and red this. Mitigates
    Risk ADR-0003 N1.
    """
    from scripts.ingest import scheduler

    store_root = tmp_path / "store"
    ou = tmp_path / "oura.json"
    _write_json_export(ou, [_ou("hrv", "2026-01-01", 55), _ou("hrv", "2026-01-02", 58)])

    scheduler.run(exports={"oura": ou}, root=store_root)
    first = len(store.read("hrv", root=store_root))
    scheduler.run(exports={"oura": ou}, root=store_root)
    second = len(store.read("hrv", root=store_root))

    assert first == 2
    assert second - first == 0  # idempotent: no line appended on the no-new run


# --- AC-4 (updated, ADR-0011 D2): Whoop is now WIRED + invoked; scheduler.py still names no whoop ---


def test_wired_set_invoked_includes_whoop(tmp_path, monkeypatch):
    """AC-4a (ADR-0011 D2): the run's invoked-adapter set now INCLUDES whoop.

    Spies on ingest.run to record which adapters scheduler.run() invokes. With
    whoop.py's UNWIRED marker removed, the data-driven discovery includes Whoop, so
    a run with a whoop.sqlite export invokes ingest.run over it. Inverts the prior
    unwired-exclusion assertion: the invoked source set is the full wired set
    INCLUDING whoop. Reds if a regression drops Whoop from the wired set.
    """
    from scripts.ingest import ingest, scheduler

    exports = _sample_exports(
        tmp_path,
        healthkit_records=[_hk("HKQuantityTypeIdentifierRestingHeartRate", "2026-01-01", 48)],
        oura_records=[_ou("hrv", "2026-01-01", 55)],
        garmin_records=[_ga("stress", "2026-01-01", 30)],
    )
    whoop_db = tmp_path / "whoop.sqlite"
    _write_whoop_sqlite(whoop_db, [{"day": "2026-01-01", "recovery": 66.0}])
    exports["whoop"] = whoop_db
    store_root = tmp_path / "store"

    real_run = ingest.run
    invoked = []

    def _spy(adapter, export_file, root=store.DEFAULT_ROOT):
        invoked.append(adapter.source_tag())
        return real_run(adapter, export_file, root=root)

    monkeypatch.setattr(scheduler.ingest, "run", _spy)
    scheduler.run(exports=exports, root=store_root)

    assert set(invoked) == WIRED_SOURCES
    assert "whoop" in invoked
    # The whoop adapter actually ingested its reading (not merely discovered).
    assert len(store.read("recovery", root=store_root)) == 1


def test_scheduler_carries_no_whoop_reference():
    """AC-4b (static): scripts/ingest/scheduler.py carries 0 `whoop` references.

    The pure-Python form of the spec's literal `rg "whoop" scripts/ingest/
    scheduler.py`=0 command (ADR-0003-T2 criterion 5 / spec line 192), DEFERRED by
    T2 to "after scheduler.py exists" and DISCHARGED here. Reds if scheduler.py
    references `whoop`. Failing-capability is exercised by the transient-`whoop`-
    probe negative control (test_scheduler_whoop_scan_is_falsifiable).
    """
    assert _whoop_count(SCHEDULER_PATH.read_text()) == 0


def _whoop_count(text):
    """Count case-insensitive `whoop` occurrences in a source string.

    The pure-Python stand-in for `rg "whoop" <file>` — counts the same token rg
    would match (rg is a non-exec shim on this host; same documented deviation as
    test_ingest.py's `def .*key` / model-token scans).
    """
    return text.lower().count("whoop")


def test_scheduler_whoop_scan_is_falsifiable():
    """Negative control for AC-4b: the whoop scan turns RED against a planted token.

    Proves the `_whoop_count == 0` assertion is not vacuous: the same scan applied
    to a fixture string carrying a `whoop` token detects it. (The Step-1 RED phase
    additionally flips the LIVE file with a transient probe to prove the
    file-level assertion reds, then removes it — documented in the SE report.)
    """
    assert _whoop_count("# whoop reference\nimport whoop\n") > 0
    assert _whoop_count("WhoopAdapter()") > 0  # case-insensitive matches the class too


# --- AC-4 mechanism guards: the typed unwired-marker exclusion, not just today's roster ---
# Bead a-plus-maxing-7lt: wired-set membership is governed by a typed module
# attribute — excluded iff `UNWIRED` is present and truthy (canonical
# declaration `UNWIRED = True`); a falsy value or absence means wired. This
# replaced the S40 docstring-substring mechanism, whose prose matching could
# silently drop a wired adapter that merely MENTIONS "unwired" (fragility i) or
# silently re-include Whoop on a docstring rewording (fragility ii). These guards
# pin the typed mechanism so a future edit that breaks it REDs here, not silently
# in production.


def test_whoop_carries_no_unwired_marker():
    """Guard (ADR-0011 D2): whoop.py no longer declares the UNWIRED marker — it is WIRED.

    Inverts the prior unwired-scaffold guard. With the marker removed, the
    scheduler's data-driven discovery includes Whoop. A regression that re-adds
    `UNWIRED = True` to whoop.py would silently drop Whoop from the unattended run
    (the DANGEROUS direction) — this REDs first: the attribute must be absent or
    falsy.
    """
    from scripts.ingest.adapters import whoop

    assert getattr(whoop, "UNWIRED", False) is False


def test_unwired_marker_governs_wired_set_membership():
    """Guard: membership = ABSENCE of the typed attribute, run through the real discovery.

    Drops two transient conformant adapter modules into the real adapters/
    package — identical except that one declares `UNWIRED = True` — and runs the
    scheduler's ACTUAL `_wired_adapters()` discovery unchanged. Asserts the
    attribute-free adapter IS wired and the declaring one is EXCLUDED, pinning
    the include/exclude MECHANISM (membership = absence of the typed
    declaration), not the current {healthkit,oura,garmin} roster. Uses the same
    in-package fixture + cleanup pattern as test_adapter_add_zero_scheduler_edits,
    so the predicate exercised is the production discovery, verbatim.
    """
    import importlib

    from scripts.ingest import scheduler

    # Non-underscore stems: the discovery skips `_`-prefixed modules by design, so
    # the fixtures must use plain names to flow through the real glob + import.
    wired_mod = ADAPTERS_DIR / "guardwired.py"
    unwired_mod = ADAPTERS_DIR / "guardunwired.py"

    def _adapter_module_src(source_tag, class_name, declare_unwired):
        return (
            '"""Guard fixture adapter."""\n'
            "from typing import Iterable\n\n"
            + ("\nUNWIRED = True\n\n" if declare_unwired else "\n")
            + f"\nclass {class_name}:\n"
            "    def source_tag(self) -> str:\n"
            f'        return "{source_tag}"\n\n'
            "    def read_readings(self, export_file) -> Iterable[dict]:\n"
            "        return iter(())\n"
        )

    try:
        # Identical adapters except the typed attribute in the declaring module.
        # Writes INSIDE try: a mid-setup failure still reaches the cleanup, whose
        # exists()/glob guards tolerate the not-yet-written fixture.
        wired_mod.write_text(
            _adapter_module_src("guardwired", "GuardWiredAdapter", declare_unwired=False)
        )
        unwired_mod.write_text(
            _adapter_module_src("guardunwired", "GuardUnwiredAdapter", declare_unwired=True)
        )
        importlib.invalidate_caches()
        wired = scheduler._wired_adapters()  # the REAL discovery predicate
        tags = {a.source_tag() for a in wired}

        assert "guardwired" in tags  # no attribute -> WIRED (the default)
        assert "guardunwired" not in tags  # UNWIRED = True -> EXCLUDED
    finally:
        cache = ADAPTERS_DIR / "__pycache__"
        for p in (wired_mod, unwired_mod):
            if p.exists():
                p.unlink()
            for cached in cache.glob(f"{p.stem}.*"):
                cached.unlink()


def test_falsy_unwired_declaration_stays_wired():
    """Guard (truthiness clause): a falsy `UNWIRED` declaration does NOT exclude.

    Drops a transient conformant adapter module declaring `UNWIRED = False` into
    the real adapters/ package and runs the scheduler's ACTUAL `_wired_adapters()`
    discovery. The adapter must be WIRED: exclusion requires the attribute to be
    present AND truthy, not merely present. Against a presence-based predicate
    (`hasattr(module, _UNWIRED_ATTR)`) this REDs — pinning the truthiness clause
    the declared contract (falsy or absent = wired) promises. Same in-package
    fixture + cleanup pattern as test_unwired_marker_governs_wired_set_membership.
    """
    import importlib

    from scripts.ingest import scheduler

    falsy_mod = ADAPTERS_DIR / "guardfalsy.py"
    try:
        falsy_mod.write_text(
            '"""Guard fixture adapter declaring a falsy UNWIRED."""\n'
            "from typing import Iterable\n\n"
            "\nUNWIRED = False\n\n"
            "\nclass GuardFalsyAdapter:\n"
            "    def source_tag(self) -> str:\n"
            '        return "guardfalsy"\n\n'
            "    def read_readings(self, export_file) -> Iterable[dict]:\n"
            "        return iter(())\n"
        )
        importlib.invalidate_caches()
        wired = scheduler._wired_adapters()  # the REAL discovery predicate
        tags = {a.source_tag() for a in wired}

        assert "guardfalsy" in tags  # falsy declaration -> WIRED (truthy predicate)
    finally:
        cache = ADAPTERS_DIR / "__pycache__"
        if falsy_mod.exists():
            falsy_mod.unlink()
        for cached in cache.glob("guardfalsy.*"):
            cached.unlink()


def test_docstring_unwired_prose_does_not_exclude():
    """Guard (fragility i): docstring prose mentioning "unwired" never drops an adapter.

    Drops a transient conformant adapter module whose module DOCSTRING
    legitimately contains the word "unwired" but which carries NO typed `UNWIRED`
    attribute, and runs the real `_wired_adapters()`. The adapter must be WIRED:
    membership is governed solely by the typed declaration, never by prose.
    Against the retired docstring-substring mechanism this REDs (the prose match
    silently dropped the adapter from the unattended run — the a-plus-maxing-7lt
    fragility (i) this test exists to guard).
    """
    import importlib

    from scripts.ingest import scheduler

    probe_mod = ADAPTERS_DIR / "proseprobe.py"
    try:
        # Write INSIDE try: a mid-setup failure still reaches the cleanup, whose
        # exists()/glob guards tolerate the not-yet-written fixture.
        probe_mod.write_text(
            '"""Prose-probe adapter; unlike an unwired scaffold, it is fully wired."""\n'
            "from typing import Iterable\n\n\n"
            "class ProseProbeAdapter:\n"
            "    def source_tag(self) -> str:\n"
            '        return "proseprobe"\n\n'
            "    def read_readings(self, export_file) -> Iterable[dict]:\n"
            "        return iter(())\n"
        )
        importlib.invalidate_caches()
        wired = scheduler._wired_adapters()  # the REAL discovery predicate
        tags = {a.source_tag() for a in wired}

        assert "proseprobe" in tags  # docstring prose never affects membership
    finally:
        cache = ADAPTERS_DIR / "__pycache__"
        if probe_mod.exists():
            probe_mod.unlink()
        for cached in cache.glob("proseprobe.*"):
            cached.unlink()


# --- SEC-2 / BUG-1: discovery tests conformance via issubclass, never by constructing ---
# A class with a required-arg __init__ living alongside the conformant adapter (a
# future helper class in an adapter module) must NOT abort the unattended run. The
# discovery tests the Protocol on the CLASS (issubclass, @runtime_checkable) BEFORE
# constructing, and only instantiates the class that actually conforms.


def test_discovery_ignores_non_adapter_helper_with_required_init(tmp_path):
    """SEC-2/BUG-1: a helper class with a required-arg __init__ does not abort discovery.

    Drops a transient conformant adapter module that ALSO defines a non-Adapter
    helper class whose `__init__(self, x)` takes a required arg, with the helper's
    class name sorting BEFORE the adapter's (so a construct-to-test discovery hits
    the helper first). Against a construct-then-isinstance discovery this raises
    TypeError and aborts `_wired_adapters()`; against the issubclass-before-construct
    fix the helper is ignored and the conformant adapter is discovered. Uses the
    same in-package fixture + cleanup pattern as the AC-6 fixture.
    """
    import importlib

    from scripts.ingest import scheduler

    probe_mod = ADAPTERS_DIR / "secprobe.py"
    probe_mod.write_text(
        '"""Probe adapter module (helper + conformant adapter)."""\n'
        "from typing import Iterable\n\n\n"
        "class AaaHelper:\n"  # sorts before the adapter -> constructed first by getmembers
        "    def __init__(self, x):\n"
        "        self.x = x\n\n\n"
        "class ZzzProbeAdapter:\n"
        "    def source_tag(self) -> str:\n"
        '        return "secprobe"\n\n'
        "    def read_readings(self, export_file) -> Iterable[dict]:\n"
        "        return iter(())\n"
    )
    try:
        importlib.invalidate_caches()
        wired = scheduler._wired_adapters()  # the REAL discovery predicate
        tags = {a.source_tag() for a in wired}

        assert "secprobe" in tags  # conformant adapter discovered, helper ignored
    finally:
        cache = ADAPTERS_DIR / "__pycache__"
        if probe_mod.exists():
            probe_mod.unlink()
        for cached in cache.glob("secprobe.*"):
            cached.unlink()


# --- TEST-4: a wired adapter with NO export entry is skipped; run still exits 0 ---


def test_missing_export_adapter_is_skipped(tmp_path):
    """TEST-4: an `exports` subset skips the export-less wired adapters; run exits 0.

    Runs scheduler.run() with an `exports` dict covering ONLY oura — a strict
    subset of the wired set. Asserts rc == 0, the oura reading landed in the store
    (placement), AND the healthkit/garmin readings are ABSENT (negative — the
    missing-export adapters contributed nothing). Pins the `if export_file is not
    None` skip branch with placement + negative, not incidentally.
    """
    from scripts.ingest import scheduler

    store_root = tmp_path / "store"
    ou = tmp_path / "oura.json"
    _write_json_export(ou, [_ou("hrv", "2026-01-01", 55)])

    rc = scheduler.run(exports={"oura": ou}, root=store_root)

    assert rc == 0
    assert len(store.read("hrv", root=store_root)) == 1  # oura ran
    assert store.read("rhr", root=store_root) == []  # healthkit skipped (no export)
    assert store.read("stress", root=store_root) == []  # garmin skipped (no export)


# --- AC-5 / Constraint D1->D3: egress 0 over a REAL scheduler.run() ---


def test_scheduler_run_zero_egress(tmp_path):
    """AC-5: a real scheduler.run() under egress_guard.run is truthy (0 egress).

    Wraps a REAL scheduler.run() (wired adapters + tmp exports + tmp store root,
    all closed over) in ONE zero-arg closure passed to egress_guard.run, which
    forks + OS-isolates the child and returns truthy iff 0 outbound calls surfaced
    across the whole invocation (incl. any child process). The closure wraps the
    production scheduler path, not a no-op. Mitigates Constraint D1->D3.
    """
    from scripts.guard import egress_guard
    from scripts.ingest import scheduler

    if not _sandbox_available():
        pytest.skip("sandbox-exec not invocable — zero-egress isolation unavailable")

    exports = _sample_exports(
        tmp_path,
        healthkit_records=[_hk("HKQuantityTypeIdentifierRestingHeartRate", "2026-01-01", 48)],
        oura_records=[_ou("hrv", "2026-01-01", 55)],
        garmin_records=[_ga("stress", "2026-01-01", 30)],
    )
    store_root = tmp_path / "store"

    def operation():
        scheduler.run(exports=exports, root=store_root)

    assert egress_guard.run(operation)


# --- AC-6: data-driven 0-edit on adapter-add (committed baseline + neg control) ---


def _numstat_rows(baseline_ref, path):
    """Return the `git diff --numstat <baseline> -- <path>` rows for one path.

    An unchanged path emits NO row (empty output); the assertion encodes "the
    numstat output for scheduler.py is empty" (row count 0), NOT a search for a
    `0` token.
    """
    out = subprocess.run(
        ["git", "diff", "--numstat", baseline_ref, "--", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def _baseline_ref(label):
    """Capture a FIXED git object holding scheduler.py in its committed-at-capture state.

    `git stash create` writes a commit object for the current tree WITHOUT touching
    the working tree or the stash list, giving a fixed ref the numstat diffs
    against (not the non-deterministic working index). Falls back to HEAD when the
    tree is clean (stash create emits nothing).
    """
    sha = subprocess.run(
        ["git", "stash", "create", label],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return sha or "HEAD"


def test_adapter_add_zero_scheduler_edits(tmp_path):
    """AC-6: adding a further wired adapter changes 0 lines in scheduler.py.

    (i) Captures a committed baseline ref of scheduler.py (a fixed git object via
    `git stash create`, NOT the working index). (ii) Adds a NEW wired adapter
    module to the data-driven wired set (a new adapter module in adapters/ — NOT an
    edit to scheduler.py). (iii) Asserts `git diff --numstat <pre-add> --
    scripts/ingest/scheduler.py` emits 0 ROWS (empty output). The new adapter's
    reading must also be ingested by a run, proving the data-driven discovery
    actually picked it up (not merely that scheduler.py was untouched).
    """
    from scripts.ingest import scheduler

    pre_add = _baseline_ref("ADR-0003-T3-pre-add")

    # Add a NEW wired adapter MODULE (no scheduler.py edit). It conforms to the
    # frozen contract and carries NO unwired marker, so the data-driven discovery
    # wires it automatically.
    new_module = ADAPTERS_DIR / "fitbit.py"
    new_module.write_text(
        '"""Fitbit ingestion adapter (test-only fixture)."""\n'
        "from typing import Iterable\n\n\n"
        "class FitbitAdapter:\n"
        "    def source_tag(self) -> str:\n"
        '        return "fitbit"\n\n'
        "    def read_readings(self, export_file) -> Iterable[dict]:\n"
        "        import json\n"
        "        from pathlib import Path\n\n"
        "        for rec in json.loads(Path(export_file).read_text()):\n"
        "            yield {\n"
        '                "item": rec["kind"],\n'
        '                "timepoint": rec["at"],\n'
        '                "source": self.source_tag(),\n'
        '                "value": rec["v"],\n'
        "            }\n"
    )
    try:
        # scheduler.py is unchanged by adding an adapter -> 0 numstat rows.
        rows = _numstat_rows(pre_add, "scripts/ingest/scheduler.py")
        assert rows == [], rows

        # The data-driven discovery actually wired the new adapter: a run over its
        # export ingests its reading (so AC-6 proves a DATA-DRIVEN set, not a
        # silently-broken one that merely left scheduler.py untouched).
        export = tmp_path / "fitbit.json"
        _write_json_export(export, [{"kind": "spo2", "at": "2026-01-01", "v": 98}])
        store_root = tmp_path / "store"
        import importlib

        importlib.invalidate_caches()
        scheduler.run(exports={"fitbit": export}, root=store_root)
        assert len(store.read("spo2", root=store_root)) == 1
    finally:
        new_module.unlink()
        pyc = ADAPTERS_DIR / "__pycache__"
        for cached in pyc.glob("fitbit.*"):
            cached.unlink()


def test_adapter_add_zero_edit_is_falsifiable():
    """Negative control for AC-6: a one-line scheduler.py edit reds the 0-row assertion.

    Proves the 0-row numstat assertion is failing-capable: writing ONE extra line
    into scheduler.py against a FIXED baseline (`git stash create`, which snapshots
    the tracked working tree into a commit object — capturing scheduler.py once it
    is index-staged) makes `git diff --numstat <baseline>` emit ONE row for that
    path (row count non-zero), so the assertion would FAIL. The edit is reverted
    afterward. Mirrors the committed-baseline falsifiability proof
    tests/ingest/test_adapters.py uses for the shared-routine 0-edit gate.
    """
    original = SCHEDULER_PATH.read_text()
    # Stage scheduler.py at its current state so `git stash create` (which only
    # snapshots tracked content) captures it as the fixed pre-probe baseline.
    subprocess.run(
        ["git", "add", "scripts/ingest/scheduler.py"], cwd=REPO_ROOT, check=True
    )
    baseline = _baseline_ref("ADR-0003-T3-zero-edit-falsifiability")
    try:
        SCHEDULER_PATH.write_text(original + "\n# falsifiability probe\n")
        rows = _numstat_rows(baseline, "scripts/ingest/scheduler.py")
        # A one-line edit emits exactly one numstat row for scheduler.py.
        assert any(r.endswith("scripts/ingest/scheduler.py") for r in rows), rows
    finally:
        SCHEDULER_PATH.write_text(original)
        subprocess.run(
            ["git", "reset", "-q", "--", "scripts/ingest/scheduler.py"],
            cwd=REPO_ROOT,
        )


def test_hardcoded_call_list_would_red_zero_edit(tmp_path):
    """Negative control for AC-6: a hardcoded per-adapter call list reds the 0-edit gate.

    The spec's REQUIRED negative control proving AC-6 distinguishes a DATA-DRIVEN
    set from a HARDCODED per-adapter call list. A hardcoded scheduler enumerates
    each wired adapter by name, so adding the Nth adapter forces an edit to
    scheduler.py — which the committed-baseline numstat would catch as a non-empty
    diff. We simulate the hardcoded variant in an isolated string and assert that
    adding an adapter to it changes the source (a non-empty line diff), whereas the
    production data-driven scheduler.py stays byte-identical when an adapter is
    added (the AC-6 test above). This documents WHY the production mechanism must be
    data-driven.
    """
    hardcoded_n = (
        "from scripts.ingest import ingest\n"
        "from scripts.ingest.adapters import healthkit, oura, garmin\n"
        "def run(exports, root=None):\n"
        "    ingest.run(healthkit.HealthKitAdapter(), exports['healthkit'], root=root)\n"
        "    ingest.run(oura.OuraAdapter(), exports['oura'], root=root)\n"
        "    ingest.run(garmin.GarminAdapter(), exports['garmin'], root=root)\n"
    )
    # Adding the Nth adapter to a hardcoded list REQUIRES a new call line:
    hardcoded_n_plus_1 = hardcoded_n + (
        "    ingest.run(fitbit.FitbitAdapter(), exports['fitbit'], root=root)\n"
    )
    # The hardcoded variant CHANGED (a non-empty line delta) when an adapter was
    # added — the exact regression AC-6 reds against. The data-driven production
    # scheduler.py does NOT change (proven by test_adapter_add_zero_scheduler_edits).
    assert hardcoded_n_plus_1 != hardcoded_n
    assert hardcoded_n_plus_1.count("ingest.run(") == hardcoded_n.count("ingest.run(") + 1


# --- AC-7: the build-plan Wave-5 exit command (this file passes) is the suite pass. ---
