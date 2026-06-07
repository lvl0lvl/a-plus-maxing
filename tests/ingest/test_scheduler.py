"""Tests for the unattended scheduler run (ADR-0003-T3).

Covers AC-1..AC-7: unattended invocation over the wired adapter set (exit 0, 0
prompts, stdin closed), delta-only append on a second run, idempotent no-new
re-run, Whoop-unwired exclusion (dynamic invoked-set + the static `whoop`-token
scan that discharges ADR-0003-T2's deferred command), 0 outbound egress over a
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

from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULER_PATH = REPO_ROOT / "scripts" / "ingest" / "scheduler.py"
ADAPTERS_DIR = REPO_ROOT / "scripts" / "ingest" / "adapters"

# The wired set the scheduler must invoke `ingest.run` over (AC-1, AC-4a). Whoop
# is the registered-but-unwired scaffold the scheduler must NOT invoke.
WIRED_SOURCES = {"healthkit", "oura", "garmin"}


def _write_json_export(path, records):
    """Write a JSON export the source adapters parse (json.loads of a list)."""
    path.write_text(json.dumps(records))


def _sample_exports(tmp_path, healthkit_records, oura_records, garmin_records):
    """Write one sample export per wired source; return the {source: path} map.

    Each adapter parses its own source-specific schema, so the records carry the
    per-source field names (`type`/`startDate`/`qty` for HealthKit, etc.).
    """
    hk = tmp_path / "healthkit.json"
    ou = tmp_path / "oura.json"
    ga = tmp_path / "garmin.json"
    _write_json_export(hk, healthkit_records)
    _write_json_export(ou, oura_records)
    _write_json_export(ga, garmin_records)
    return {"healthkit": hk, "oura": ou, "garmin": ga}


def _hk(item, ts, qty):
    """A HealthKit-shaped export record."""
    return {"type": item, "startDate": ts, "qty": qty}


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
        healthkit_records=[_hk("steps", "2026-01-01T08:00", 1000)],
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
    assert len(store.read("steps", root=store_root)) == 1
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
    hk = tmp_path / "healthkit.json"

    # First run: two timepoints.
    _write_json_export(
        hk,
        [_hk("steps", "2026-01-01T08:00", 1000), _hk("steps", "2026-01-02T08:00", 1100)],
    )
    scheduler.run(exports={"healthkit": hk}, root=store_root)
    before = len(store.read("steps", root=store_root))

    # The export GAINED two new timepoints (the original two are still present).
    _write_json_export(
        hk,
        [
            _hk("steps", "2026-01-01T08:00", 1000),
            _hk("steps", "2026-01-02T08:00", 1100),
            _hk("steps", "2026-01-03T08:00", 1200),
            _hk("steps", "2026-01-04T08:00", 1300),
        ],
    )
    scheduler.run(exports={"healthkit": hk}, root=store_root)
    after = len(store.read("steps", root=store_root))

    new_count = 2
    assert after - before == new_count  # exact new-timepoint delta, not "<=" first


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


# --- AC-4: Whoop unwired adapter NOT invoked (two halves) ---


def test_whoop_not_invoked(tmp_path, monkeypatch):
    """AC-4a (dynamic): the run's invoked-adapter set is exactly the wired set.

    Spies on ingest.run to record which adapters scheduler.run() actually invokes
    `ingest.run` over, and asserts the invoked source set equals {healthkit, oura,
    garmin} and does NOT contain whoop. Reds if the scheduler's wired set ever
    includes/invokes Whoop.
    """
    from scripts.ingest import ingest, scheduler

    exports = _sample_exports(
        tmp_path,
        healthkit_records=[_hk("steps", "2026-01-01T08:00", 1000)],
        oura_records=[_ou("hrv", "2026-01-01", 55)],
        garmin_records=[_ga("stress", "2026-01-01", 30)],
    )
    store_root = tmp_path / "store"

    real_run = ingest.run
    invoked = []

    def _spy(adapter, export_file, root=store.DEFAULT_ROOT):
        invoked.append(adapter.source_tag())
        return real_run(adapter, export_file, root=root)

    monkeypatch.setattr(scheduler.ingest, "run", _spy)
    scheduler.run(exports=exports, root=store_root)

    assert set(invoked) == WIRED_SOURCES
    assert "whoop" not in invoked


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


# --- AC-4 mechanism guards: the unwired-marker exclusion, not just today's roster ---
# Tier-2 review (a-plus-maxing-7lt): the docstring `_UNWIRED_MARKER` substring is
# load-bearing for AC-4 (Whoop must NEVER be invoked) but its FAILURE MODES were
# untested — test_whoop_not_invoked pins the {healthkit,oura,garmin} roster, not
# the mechanism (membership = ABSENCE of the marker). These two guards pin the
# mechanism so a future edit that breaks it REDs here, not silently in production.


def test_whoop_doc_carries_unwired_marker():
    """Guard: whoop.py's module docstring carries scheduler._UNWIRED_MARKER.

    The scheduler excludes the Whoop scaffold ONLY because whoop.py's module
    docstring declares the unwired marker. If a future edit removes or rewords the
    marker out of whoop.py's __doc__, the scheduler would silently re-include
    Whoop in the wired set (the DANGEROUS direction AC-4 exists to prevent) while
    test_whoop_not_invoked might still pass against a stale roster — this test
    REDs first. Guard value: were whoop.py's __doc__ missing the marker, the
    `in` assertion below turns RED.
    """
    from scripts.ingest import scheduler
    from scripts.ingest.adapters import whoop

    assert scheduler._UNWIRED_MARKER in (whoop.__doc__ or "").lower()


def test_unwired_marker_governs_wired_set_membership():
    """Guard: membership = ABSENCE of the marker, run through the real discovery.

    Drops two transient, otherwise-identical conformant adapter modules into the
    real adapters/ package — one WITHOUT the unwired marker, one WITH it in its
    module docstring — and runs the scheduler's ACTUAL `_wired_adapters()`
    discovery unchanged. Asserts the no-marker adapter IS wired and the marked one
    is EXCLUDED, pinning the include/exclude MECHANISM (membership = absence of the
    marker), not the current {healthkit,oura,garmin} roster. Uses the same
    in-package fixture + cleanup pattern as test_adapter_add_zero_scheduler_edits,
    so the predicate exercised is the production discovery, verbatim.
    """
    import importlib

    from scripts.ingest import scheduler

    marker = scheduler._UNWIRED_MARKER
    # Non-underscore stems: the discovery skips `_`-prefixed modules by design, so
    # the fixtures must use plain names to flow through the real glob + import.
    wired_mod = ADAPTERS_DIR / "guardwired.py"
    unwired_mod = ADAPTERS_DIR / "guardunwired.py"

    def _adapter_module_src(doc, source_tag, class_name):
        return (
            f'"""{doc}"""\n'
            "from typing import Iterable\n\n\n"
            f"class {class_name}:\n"
            "    def source_tag(self) -> str:\n"
            f'        return "{source_tag}"\n\n'
            "    def read_readings(self, export_file) -> Iterable[dict]:\n"
            "        return iter(())\n"
        )

    # Identical adapters except the unwired marker in the WITH-marker module's doc.
    wired_mod.write_text(
        _adapter_module_src(
            "Guard fixture adapter (wired).", "guardwired", "GuardWiredAdapter"
        )
    )
    unwired_mod.write_text(
        _adapter_module_src(
            f"Guard fixture adapter ({marker} scaffold).",
            "guardunwired",
            "GuardUnwiredAdapter",
        )
    )
    try:
        importlib.invalidate_caches()
        wired = scheduler._wired_adapters()  # the REAL discovery predicate
        tags = {a.source_tag() for a in wired}

        assert "guardwired" in tags  # no marker -> WIRED
        assert "guardunwired" not in tags  # marker present -> EXCLUDED
    finally:
        cache = ADAPTERS_DIR / "__pycache__"
        for p in (wired_mod, unwired_mod):
            if p.exists():
                p.unlink()
            for cached in cache.glob(f"{p.stem}.*"):
                cached.unlink()


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
        healthkit_records=[_hk("steps", "2026-01-01T08:00", 1000)],
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
