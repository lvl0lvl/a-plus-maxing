"""Tests for the tracker-pull orchestration entry `pull.main` (tracker-ingestion Build A).

`pull.main` is the NEW caller of the UNCHANGED `scheduler.run`: it builds the `exports` map (fetch
each wired API-pull source to a staged file + scan the Apple-Health watched folder) under the
runner store lock, then calls `scheduler.run(exports, root)`. Covers:
- P1/P3 end-to-end: a fixture Whoop pull + a dropped Apple-Health export both land; a re-run appends 0.
- P3 (watched folder): the newest export in the watched dir is picked up via the UNCHANGED healthkit
  adapter; a re-drop of the same export is a no-op (idempotent).
- fail-closed decoupling: a Whoop auth failure lands 0 Whoop readings (loud) but the watched folder
  still lands (one expired token never blocks the Apple path).
- the runner store lock: a busy tick defers (0 fetch, 0 store write).
- P4 (store-content): no store byte leaves over the fetch path under a recording seam.
- the frozen seam stays byte-unchanged (the six + ingest.run + scheduler.run + the Adapter protocol).

The network + keychain seams are the module-level `oauth_pull` seams, monkeypatched to fixtures so
no test touches a real host, keychain, or token.
"""

import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import pytest

from conftest import hk_record, write_healthkit_export as _write_healthkit_export

from scripts.store import store

from test_oauth_pull import _RecordingHttp, _fake_keychain, _whoop_routes

REPO_ROOT = Path(__file__).resolve().parents[2]

# The frozen spine the build must NOT edit (numstat == 0 vs the fork point). Extends the ADR-0003
# gate (ingest.py/adapter.py/scheduler.py) to also cover the <always-frozen> six store/plan files.
FROZEN_PATHS = (
    "scripts/store/store.py",
    "scripts/store/keying.py",
    "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    "scripts/plan/router.py",
    "scripts/ingest/ingest.py",
    "scripts/ingest/scheduler.py",
    "scripts/ingest/adapter.py",
)


def _hk_rhr(day, value):
    """One HealthKit resting-HR <Record> dict for a day (a real Apple export sample)."""
    return hk_record("HKQuantityTypeIdentifierRestingHeartRate", f"{day} 06:00:00 -0500", value)


def _drop_healthkit_export(watched_root, records):
    """Write a fixture Apple Health export.xml into the watched folder (the operator-Shortcut drop)."""
    hk_dir = Path(watched_root) / "healthkit"
    hk_dir.mkdir(parents=True, exist_ok=True)
    export = hk_dir / "export.xml"
    _write_healthkit_export(export, records)
    return export


def _inject_whoop_seams(monkeypatch, http=None):
    """Point the module-level oauth_pull seams at fixtures (fetch resolves them at call time).

    A WHOOP-ONLY credential: since Build B `_API_PULL_SOURCES` also wires oura / garmin / google-health,
    `pull.main` now attempts all four each tick. This fixture supplies a token only for whoop, so the
    other three fail closed PRE-NETWORK (0 outbound calls) — the integration tests exercise the whoop
    path unchanged, and the added sources contribute 0 calls (which keeps the wire-scan host set exact
    and proves an unconfigured source never dials out).
    """
    from scripts.ingest import oauth_pull

    http = http if http is not None else _RecordingHttp(_whoop_routes())
    monkeypatch.setattr(oauth_pull, "_read_oauth_credential",
                        lambda source: "fixture-refresh-token" if source == "whoop" else None)
    monkeypatch.setattr(oauth_pull, "_http", http)
    return http


# --- P1 + P3 end-to-end: a Whoop pull + a watched-folder drop both land; a re-run appends 0 ---


def test_pull_lands_whoop_and_watched_healthkit(tmp_path, monkeypatch):
    """P1/P3: one tick fetches Whoop AND ingests a dropped Apple export; both stores populate."""
    from scripts.ingest import pull

    _inject_whoop_seams(monkeypatch)
    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])

    rc = pull.main(["--root", str(store_root), "--watched-root", str(watched)])
    assert rc == 0

    # Whoop landed (the fetch->stage->ingest path) ...
    assert store.read("recovery", root=store_root)[0]["value"] == 66
    assert store.read("recovery", root=store_root)[0]["source"] == "whoop"
    # ... and the watched Apple export landed via the UNCHANGED healthkit adapter. Whoop ALSO writes
    # an rhr on the same day (from resting_heart_rate); source is in the dedupe key, so both persist —
    # filter by source to assert the healthkit landing specifically.
    hk_rhr = [r for r in store.read("rhr", root=store_root) if r["source"] == "healthkit"]
    assert len(hk_rhr) == 1
    assert hk_rhr[0]["value"] == 48.0


def test_pull_rerun_appends_zero(tmp_path, monkeypatch):
    """P1/P3 idempotency: a second identical tick appends 0 new lines to either stream."""
    from scripts.ingest import pull

    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])
    argv = ["--root", str(store_root), "--watched-root", str(watched)]

    _inject_whoop_seams(monkeypatch)
    pull.main(argv)
    first_recovery = len(store.read("recovery", root=store_root))
    first_rhr = len(store.read("rhr", root=store_root))

    _inject_whoop_seams(monkeypatch)      # a fresh recording seam, same fixture data
    pull.main(argv)
    assert len(store.read("recovery", root=store_root)) - first_recovery == 0
    assert len(store.read("rhr", root=store_root)) - first_rhr == 0


# --- P3: the watched-folder scan ---


def test_scan_watched_folder_picks_newest_export(tmp_path):
    """P3: the scan returns the newest export in `<watched_root>/healthkit/`, else None."""
    from scripts.ingest import pull

    watched = tmp_path / "inbox"
    assert pull._scan_watched_folder(watched) is None        # empty / absent -> None

    hk_dir = watched / "healthkit"
    hk_dir.mkdir(parents=True)
    older = hk_dir / "export-old.xml"
    newer = hk_dir / "export-new.xml"
    _write_healthkit_export(older, [_hk_rhr("2026-07-01", "50")])
    _write_healthkit_export(newer, [_hk_rhr("2026-07-10", "48")])
    import os
    import time
    now = time.time()
    os.utime(older, (now - 100, now - 100))
    os.utime(newer, (now, now))

    assert pull._scan_watched_folder(watched) == newer       # newest by mtime


def test_watched_folder_redrop_is_idempotent(tmp_path, monkeypatch):
    """P3: re-dropping the same (or an overlapping) Apple export appends 0 new lines.

    Apple exports are full cumulative dumps; the healthkit daily-mean -> (item, day, "healthkit")
    dedup makes a re-drop a safe no-op.
    """
    from scripts.ingest import pull

    _inject_whoop_seams(monkeypatch)
    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    argv = ["--root", str(store_root), "--watched-root", str(watched)]

    def _healthkit_rhr_count():
        # Filter by source: whoop also writes an rhr, so count only the healthkit (watched) readings.
        return len([r for r in store.read("rhr", root=store_root) if r["source"] == "healthkit"])

    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])
    pull.main(argv)
    first = _healthkit_rhr_count()

    # An overlapping re-drop (the same day, plus a new day) appends only the new day.
    _inject_whoop_seams(monkeypatch)
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48"), _hk_rhr("2026-07-11", "49")])
    pull.main(argv)
    after = _healthkit_rhr_count()
    assert first == 1
    assert after - first == 1        # only the new day, not a duplicate of the re-dropped one


# --- fail-closed decoupling: a Whoop auth failure never blocks the Apple path ---


def test_whoop_auth_failure_still_lands_watched_healthkit(tmp_path, monkeypatch, capsys):
    """A missing Whoop token lands 0 Whoop readings (loud) but the watched Apple export still lands."""
    from scripts.ingest import oauth_pull, pull

    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])

    # No refresh token -> the Whoop fetch raises TrackerPullError inside pull.main.
    monkeypatch.setattr(oauth_pull, "_read_oauth_credential", _fake_keychain(token=None))
    monkeypatch.setattr(oauth_pull, "_http", _RecordingHttp(_whoop_routes()))

    rc = pull.main(["--root", str(store_root), "--watched-root", str(watched)])
    assert rc == 0

    assert [r for r in store.read_all(store_root) if r["source"] == "whoop"] == []   # 0 Whoop
    assert len(store.read("rhr", root=store_root)) == 1                              # Apple landed
    err = capsys.readouterr().err
    assert "whoop" in err.lower()      # loud: a diagnostic named the failed source


# --- the runner store lock: a busy tick defers ---


def test_busy_lock_defers_without_fetch_or_write(tmp_path, monkeypatch):
    """A held cadence lock makes the tick defer: 0 fetch, 0 store write, exit 0 (busy catches up next)."""
    from scripts.ingest import oauth_pull, pull
    from scripts.runner import store_lock

    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])

    called = []
    monkeypatch.setattr(oauth_pull, "fetch",
                        lambda *a, **k: called.append(1) or (_ for _ in ()).throw(AssertionError))

    with store_lock.cadence_lock(store_root) as acquired:
        assert acquired            # the test holds the lock
        rc = pull.main(["--root", str(store_root), "--watched-root", str(watched)])

    assert rc == 0
    assert called == []                             # fetch never ran under a busy lock
    assert store.read_all(store_root) == []         # nothing landed (deferred to the next tick)


# --- P4: 0 store-content bytes leave over the whole pull path ---


def test_pull_wire_scan_no_store_content_outbound(tmp_path, monkeypatch):
    """P4: a store sentinel + the fetch path -> only the vendor host, 0 store bytes, 0 model-lane calls."""
    from scripts.ingest import pull
    from scripts.model.client import ModelClient

    # 0 model-lane calls (ADR-0001 inbound-only): the pull path must never even CONSTRUCT the model
    # client. A construction during the tick reds here — a stronger proof than the host assertion alone.
    def _no_model(*a, **k):
        raise AssertionError("the pull path constructed the model client — not inbound-only")

    monkeypatch.setattr(ModelClient, "__init__", _no_model)

    store_root = tmp_path / "store"
    watched = tmp_path / "inbox"
    sentinel = "SENTINEL-4471-xyz"
    store.append("hrv", {"item": "hrv", "timepoint": "2026-05-01",
                         "source": "whoop", "value": sentinel}, root=store_root)
    _drop_healthkit_export(watched, [_hk_rhr("2026-07-10", "48")])

    http = _inject_whoop_seams(monkeypatch)
    pull.main(["--root", str(store_root), "--watched-root", str(watched)])

    hosts = {urlparse(c["url"]).hostname for c in http.calls}
    assert hosts == {"api.prod.whoop.com"}          # only the vendor host, never the model lane
    for c in http.calls:
        blob = json.dumps({k: (v.decode() if isinstance(v, (bytes, bytearray)) else v)
                           for k, v in c.items()})
        assert sentinel not in blob                 # 0 store content in any outbound request


# --- the tracker-pull is disabled by default (operator-gated LIVE; the build arms nothing) ---


def test_tracker_pull_label_is_registered_disabled_by_default():
    """A distinct tracker-pull label exists but the build arms no OS-timer entry (PF-S63-02 posture)."""
    from scripts.ingest import pull

    assert pull.TRACKER_PULL_LABEL == "com.aplusmaxing.tracker-pull"
    # The module arms nothing on import: no launchctl / crontab / enable call in the module source.
    src = Path(pull.__file__).read_text()
    for token in ("launchctl", "StartCalendarInterval", "crontab", ".rendered.plist"):
        assert token not in src, token


# --- the frozen spine stays byte-unchanged (EXTEND-not-rebuild) ---


def _numstat_rows(baseline_ref, paths):
    """The `git diff --numstat <baseline_ref> -- <paths>` rows (empty == 0 edits)."""
    out = subprocess.run(
        ["git", "diff", "--numstat", baseline_ref, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def _baseline_ref(marker):
    """A fork-point committed-tree baseline (this branch's merge-base with origin/main).

    The diff `git diff --numstat <baseline> -- <FROZEN_PATHS>` is empty exactly when no task commit
    touched any frozen path (the 0-edit pass), and emits a row the moment one does (the falsifiable
    RED). A HEAD-relative baseline would be tautological. Mirrors test_adapters.py's `_baseline_ref`.
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
        ["git", "commit-tree", base_tree, "-p", fork_point, "-m", f"tracker-pull 0-edit baseline: {marker}"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True, input="",
    ).stdout.strip()


def test_frozen_seam_zero_edit():
    """The build edits 0 lines of the frozen spine (the six + ingest.run + scheduler.run + Adapter)."""
    rows = _numstat_rows(_baseline_ref("frozen-seam"), FROZEN_PATHS)
    assert rows == [], rows


def test_frozen_seam_zero_edit_is_falsifiable(tmp_path):
    """Negative control: the numstat gate turns RED on a one-line edit to a frozen file (not vacuous)."""
    committed = REPO_ROOT / "scripts" / "store" / "store.py"
    probed = tmp_path / "store_probe.py"
    probed.write_text(committed.read_text() + "# negative-control probe line\n")
    out = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(committed), str(probed)],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    rows = [line for line in out.splitlines() if line.strip()]
    assert len(rows) == 1 and rows[0].split("\t")[0] == "1"
