"""Runner store-concurrency advisory lock + crash-semantics debounce invariant (ADR-0039-T4).

The runner-owned advisory lock (`scripts/runner/store_lock.py`) serializes runner-to-RUNNER cadence
ticks on the read -> regenerate -> promote critical section (ADR-0039 OQ-7), and the crashed-run
debounce invariant (OQ-8) rests on the DERIVED debounce marker (`plan_loop._last_regen_date`, the max
`plan::` date across `PLAN_DOMAINS`), never a stored marker. These tests fire the whole chain over the
SAME debounce-passing scratch fixtures the T1 runner tests reuse (`tests/serve/test_plan_loop_regen`),
at 0 live spend and 0 real operator PII (synthetic tokens only).

The four-part store-adversarial battery (`docs/checklists/store-adversarial-tests.md`, bead `pka`) runs
over the runner's read/promote + lock surface: (a) cross-stream namespace disjointness, (b) same-key /
same-timepoint dedupe, (c) dedupe-key boundary (0 new keying in the runner), (d) the mutation battery —
removing the `fcntl.flock` acquire makes `test_lock_mutual_exclusion` go RED (run, observe, revert; the
mutation is NEVER committed). A battery green under the flock removal is tautological and fails AC-7.
"""

import functools
import hashlib
import json
import subprocess
import threading
from pathlib import Path

import pytest

from scripts.serve import plan_loop
from scripts.store import plan_schema, store

from scripts.runner import cadence_runner, store_lock

from tests.serve.test_plan_loop_regen import (
    _ON_DATE,
    _REGRESSING,
    _SummarizeDeid,
    _TrendDispatch,
    _regen_root,
)

# tests/runner/test_store_concurrency.py -> tests -> <repo root>; anchors the git numstat/check-ignore.
REPO_ROOT = Path(__file__).resolve().parents[2]

# The gitignored runtime lock file name (a direct child of the store root; covered by `vault/store/`).
_LOCK_FILENAME = ".cadence-runner.lock"


def _store_digest(root):
    """A content digest of every `*.ndjson` under `root` — a byte-unchanged witness for the store."""
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(Path(root).glob("*.ndjson"))
    }


# =====================================================================================
# AC-1 / AC-2 — the advisory-lock mutual exclusion + busy-tick defer (OQ-7) ------------
# =====================================================================================


def test_lock_mutual_exclusion(tmp_path):
    # AC-1 (OQ-7): two cadence_lock(root) acquisitions on the SAME root never both hold. fcntl.flock is
    # associated with the OPEN FILE DESCRIPTION, so a second cadence_lock nested inside an outer-held one
    # (each open()-ing the lock on its OWN fd) contends `LOCK_EX | LOCK_NB` deterministically in-process
    # (no thread-race) -> BUSY. Count of overlapping critical sections == 0 (peak == 1).
    # This is the AC-7(d) mutation target: removing the flock acquire lets `inner` acquire -> RED.
    root = tmp_path / "excl"
    root.mkdir()
    concurrently_in_section = 0
    peak = 0
    with store_lock.cadence_lock(root) as outer:
        assert outer is True, "the first cadence_lock did not acquire a free lock"
        concurrently_in_section += 1
        peak = max(peak, concurrently_in_section)
        with store_lock.cadence_lock(root) as inner:
            assert inner is False, (
                "a second cadence_lock under a held one acquired the lock — mutual exclusion is broken "
                "(the flock acquire is absent, or a per-process lockf/byte-range lock was used, which "
                "does NOT contend in-process — the recipe's footgun)"
            )
            if inner:  # only under the broken/mutated lock — records the overlap the assertion caught
                concurrently_in_section += 1
                peak = max(peak, concurrently_in_section)
        concurrently_in_section -= 1
    assert peak == 1, f"overlapping critical sections observed (peak={peak}); want exactly 1 (0 overlap)"
    # release proven: after the outer critical section exits, a fresh acquire succeeds
    with store_lock.cadence_lock(root) as reacquired:
        assert reacquired is True, "the lock did not release after the outer critical section exited"


def test_busy_tick_defers_no_corruption(tmp_path, monkeypatch):
    # AC-2: a runner tick that finds the lock held DEFERS — it makes 0 plan_loop.signal calls and leaves
    # the store byte-unchanged (0 re-gen, 0 store writes), returning a deferred receipt (catch-up next
    # tick). Failing-capable: a run that ignored the held lock would call signal (re-gen) and change the
    # store digest.
    root = _regen_root(tmp_path, "busy-defer", _REGRESSING)
    signal_calls = []
    real_signal = plan_loop.signal

    def spy(*a, **k):
        signal_calls.append((a, k))
        return real_signal(*a, **k)

    monkeypatch.setattr(plan_loop, "signal", spy)
    before = _store_digest(root)
    with store_lock.cadence_lock(root) as held:
        assert held is True, "the test failed to hold the lock (the busy scenario is void)"
        receipt = cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                                     deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert signal_calls == [], (
        f"a tick that found the lock held still called plan_loop.signal {len(signal_calls)} times"
    )
    assert _store_digest(root) == before, "the deferred (busy) tick mutated the store"
    assert receipt.get("regenerated") is False and receipt.get("reason") == "lock-busy", (
        f"the busy tick did not return a deferred lock-busy receipt: {receipt}"
    )


# =====================================================================================
# AC-3 — accept-stale-snapshot, no torn read (runner<->SERVER, rests on os.replace) ----
# =====================================================================================


def test_accept_stale_snapshot_no_torn_read(tmp_path):
    # AC-3: interleaving the runner's raw read (store.read_all) with a concurrent store.append stream
    # (each write via the frozen _write_atomic -> os.replace) yields 0 torn/partial-line reads. The
    # guarantee rests on the frozen ATOMIC-PER-FILE os.replace, NOT the runner lock (which serializes
    # runner<->runner only; runner<->server is accept-stale-snapshot). Non-vacuity: the interleaved read
    # is PROVEN to overlap — some observed count falls STRICTLY between the initial and final counts.
    root = tmp_path / "stale"
    root.mkdir()
    item = "concurrent-probe"
    initial = 10
    total_appends = 250

    def _reading(n):
        return {"item": item, "timepoint": f"{n:06d}", "source": "probe", "value": n}

    for n in range(initial):
        store.append(item, _reading(n), root=root)
    item_path = root / f"{item}.ndjson"

    observed_counts = []
    torn_lines = []
    done = threading.Event()
    writer_error = []

    def writer():
        # `done` is set in a `finally` so the reader loop below can NEVER hang on a writer crash; any
        # writer exception is captured and re-raised loudly after the join (never a vacuous pass).
        try:
            for n in range(initial, initial + total_appends):
                store.append(item, _reading(n), root=root)
        except BaseException as exc:  # noqa: BLE001 — capture so the reader terminates + the failure surfaces
            writer_error.append(exc)
        finally:
            done.set()

    t = threading.Thread(target=writer)
    t.start()
    # foreground reader loop, interleaved with the concurrent appends
    while not done.is_set():
        snapshot = store.read_all(root)
        observed_counts.append(sum(1 for r in snapshot if r["item"] == item))
        # raw-file torn-line witness: os.replace atomicity => every line is a complete JSON record
        try:
            text = item_path.read_text()
        except FileNotFoundError:
            continue
        for line in text.splitlines():
            if line.strip():
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    torn_lines.append(line)
    t.join(timeout=30)
    assert not t.is_alive(), "the concurrent writer thread did not finish within the timeout (deadlock?)"
    if writer_error:
        raise AssertionError(f"the concurrent writer raised: {writer_error[0]!r}") from writer_error[0]
    # one last read after the writer finished, to pin the final count
    observed_counts.append(sum(1 for r in store.read_all(root) if r["item"] == item))
    final = initial + total_appends

    assert sum(1 for r in store.read_all(root) if r["item"] == item) == final, "not all appends landed"
    assert torn_lines == [], (
        f"a torn/partial line was observed during the interleave (os.replace not atomic?): {torn_lines[:2]}"
    )
    # NON-VACUITY: a genuine concurrent write landed DURING a read (mid-stream count strictly between).
    mid = [c for c in observed_counts if initial < c < final]
    assert mid, (
        f"no interleaved read observed a mid-stream count strictly between {initial} and {final} "
        f"(observed range {min(observed_counts)}..{max(observed_counts)}) — the interleave did not "
        "overlap, so the 0-torn arm would be vacuous"
    )
    # the guarantee rests on the frozen atomic-per-file os.replace, NOT the runner lock:
    assert "os.replace" in (REPO_ROOT / "scripts/store/store.py").read_text(), (
        "store.py no longer uses os.replace — the accept-stale-snapshot guarantee is unfounded"
    )
    assert not (root / _LOCK_FILENAME).exists(), (
        "cadence_lock was engaged on the runner<->server read path (it must serialize runner<->runner only)"
    )


# =====================================================================================
# AC-4 / AC-5 — crash advances no marker + re-fire after crash (OQ-8) ------------------
# =====================================================================================


def _crash_before_promote(*args, **kwargs):
    """A record_plan stand-in that RAISES before writing — a mid-re-gen crash before any promote."""
    raise RuntimeError("simulated mid-regen crash before promote")


def test_crash_before_promote_advances_no_marker(tmp_path, monkeypatch):
    # AC-4 (OQ-8): a crash inside regenerate BEFORE the promote (record_plan raises before writing) over a
    # debounce-PASSING store leaves the DERIVED debounce marker unchanged, records 0 new plan::<domain>
    # readings across PLAN_DOMAINS, and writes 0 new ::-prefixed marker item — the crashed run does not
    # consume the weekly window. Failing-capable: the marker is DERIVED (max plan:: date), so it can only
    # stay unchanged if no plan:: reading leaked out of the crashed promote (a clean tick DOES advance it,
    # proven by test_re_fire_after_crash).
    root = _regen_root(tmp_path, "crash-marker", _REGRESSING)
    store_read = functools.partial(store.read, root=root)
    before_marker = plan_loop._last_regen_date(store_read, _ON_DATE)
    before_counts = {d: len(store.read(f"plan::{d}", root=root)) for d in plan_schema.PLAN_DOMAINS}
    before_items = set(store.items(root))

    monkeypatch.setattr(plan_schema, "record_plan", _crash_before_promote)
    with pytest.raises(RuntimeError, match="simulated mid-regen crash before promote"):
        cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                           deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)

    # (i) the derived debounce marker is UNCHANGED
    assert plan_loop._last_regen_date(store_read, _ON_DATE) == before_marker, (
        "the crashed pre-promote tick advanced the derived debounce marker (weekly window consumed)"
    )
    # (ii) 0 new plan::<domain> readings across every PLAN_DOMAINS member (a partial-promote leak)
    after_counts = {d: len(store.read(f"plan::{d}", root=root)) for d in plan_schema.PLAN_DOMAINS}
    assert after_counts == before_counts, f"a plan:: reading leaked from the crashed promote: {after_counts}"
    # (iii) 0 new ::-prefixed marker item ids written by the runner (no separate marker record)
    new_items = set(store.items(root)) - before_items
    assert new_items == set(), f"the crashed runner created new store items: {new_items}"
    assert not any("::" in i for i in new_items), f"the crashed runner wrote a ::-marker item: {new_items}"


def test_re_fire_after_crash(tmp_path, monkeypatch):
    # AC-5: a tick fired AFTER a mid-re-gen crash re-fires — the derived marker was not advanced (AC-4),
    # so with the sustained signal still present the post-crash tick reaches plan_loop.signal (call-count
    # == 1) and re-generates (the marker advances to _ON_DATE). This rests on cadence_lock RELEASING on
    # the crash (its finally closes the fd even on exception): the lock is free after the crashed tick.
    root = _regen_root(tmp_path, "re-fire", _REGRESSING)
    store_read = functools.partial(store.read, root=root)
    before_marker = plan_loop._last_regen_date(store_read, _ON_DATE)

    # tick 1 — crash before promote (record_plan raises, propagating through the wrapped critical section)
    monkeypatch.setattr(plan_schema, "record_plan", _crash_before_promote)
    with pytest.raises(RuntimeError, match="simulated mid-regen crash before promote"):
        cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                           deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    monkeypatch.undo()  # restore the real record_plan for the re-fire

    # crash-release: the lock is FREE after the crashed tick (the finally closed the fd on the exception)
    with store_lock.cadence_lock(root) as acquired:
        assert acquired is True, "the lock was not released after the crashed tick (crash-release failed)"

    # tick 2 (post-crash) — the marker did not advance, so the sustained signal re-fires the re-gen
    signal_calls = []
    real_signal = plan_loop.signal

    def spy(*a, **k):
        signal_calls.append((a, k))
        return real_signal(*a, **k)

    monkeypatch.setattr(plan_loop, "signal", spy)
    cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert len(signal_calls) == 1, (
        f"the post-crash tick reached plan_loop.signal {len(signal_calls)} times, want 1 (no re-fire)"
    )
    # the marker advanced now — proves the re-gen re-fired AND that AC-4's 'unchanged' is non-vacuous
    after_marker = plan_loop._last_regen_date(store_read, _ON_DATE)
    assert after_marker == _ON_DATE, f"the post-crash tick did not re-generate/promote (marker {after_marker})"
    assert after_marker != before_marker, "the marker did not advance on the re-fire (the control is vacuous)"


# =====================================================================================
# AC-6 — no new store stream / no store edit (EXTEND-NOT-REBUILD) ----------------------
# =====================================================================================


def test_no_new_store_stream():
    # AC-6: store_lock.py appends NO store record, defines NO store key, adds NO ::-prefixed item id; the
    # frozen store is byte-unchanged; the lock file is a gitignored runtime artifact under vault/store/.
    src = (REPO_ROOT / "scripts/runner/store_lock.py").read_text()
    assert src.count("store.append") == 0, "store_lock.py appends a store record (must not)"
    assert src.count(".correct(") == 0, "store_lock.py writes a correction record (must not)"
    assert "::" not in src, "store_lock.py introduces a ::-prefixed store item id (must not)"

    out = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", "scripts/store/"],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True,
    )
    assert out.stdout.strip() == "", f"the frozen store changed (EXTEND-NOT-REBUILD violation): {out.stdout!r}"

    ignored = subprocess.run(
        ["git", "check-ignore", "vault/store/.cadence-runner.lock"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert ignored.stdout.strip() == "vault/store/.cadence-runner.lock", (
        "the lock file vault/store/.cadence-runner.lock is not gitignored"
    )


# =====================================================================================
# AC-7 — the four-part store-adversarial battery over the runner read/promote surface --
# =====================================================================================


def test_cross_stream_disjoint(tmp_path):
    # AC-7(a) cross-stream namespace collision: the runner's read (store.read_all / store.read) reuses the
    # frozen stream-namespaced read — a read for one stream never returns another's value. Two streams
    # share the bare name "workout" (plan::workout + a decoy watch-out::workout); the decoy is what makes
    # a namespace-prefix mutation bite.
    root = tmp_path / "xstream"
    root.mkdir()
    plan_schema.record_plan("workout", {"exercises": [{"name": "Squat", "sets": 3}]},
                            "2026-06-18", "personal-trainer", root)
    store.append("watch-out::workout",
                 {"item": "watch-out::workout", "timepoint": "2026-06-18",
                  "source": "decoy", "value": "DECOY-SENTINEL"}, root=root)

    plan_readings = store.read("plan::workout", root=root)
    assert plan_readings, "the plan::workout stream is empty (the disjointness check would be vacuous)"
    assert all(r["item"] == "plan::workout" for r in plan_readings)
    assert not any(r["value"] == "DECOY-SENTINEL" for r in plan_readings), "cross-stream read leaked the decoy"

    allr = store.read_all(root)  # the runner's raw read surface
    plan_vals = [r["value"] for r in allr if r["item"] == "plan::workout"]
    decoy_vals = [r["value"] for r in allr if r["item"] == "watch-out::workout"]
    assert "DECOY-SENTINEL" in decoy_vals, "the decoy stream did not persist (the collision test is void)"
    assert "DECOY-SENTINEL" not in plan_vals, "read_all cross-read the decoy into the plan stream"


def test_same_timepoint_two_sources_persist(tmp_path):
    # AC-7(b) same-timepoint dedupe: the runner's promote reuses the frozen (item, timepoint, source)
    # dedupe — two DISTINCT entries sharing a timepoint (different source) BOTH persist. Exercised through
    # the runner's promote sink (plan_schema.record_plan -> store.append), the call every cadence tick makes.
    root = tmp_path / "two-source"
    root.mkdir()
    plan_schema.record_plan("workout", {"exercises": [{"name": "Squat", "sets": 3}]},
                            "2026-06-18", "personal-trainer", root)
    plan_schema.record_plan("workout", {"exercises": [{"name": "Bench", "sets": 5}]},
                            "2026-06-18", "second-opinion-coach", root)
    same_tp = [r for r in store.read("plan::workout", root=root) if r["timepoint"] == "2026-06-18"]
    assert len(same_tp) == 2, f"two distinct-source plans at one timepoint did not both persist: {len(same_tp)}"
    assert {r["source"] for r in same_tp} == {"plan::personal-trainer", "plan::second-opinion-coach"}


def test_identical_re_entry_idempotent(tmp_path):
    # AC-7(b) idempotency: an identical (item, timepoint, source) re-entry through the runner's promote
    # sink is a 0-line no-op (never a duplicate row).
    root = tmp_path / "idem"
    root.mkdir()
    plan = {"exercises": [{"name": "Squat", "sets": 3}]}
    plan_schema.record_plan("workout", plan, "2026-06-18", "personal-trainer", root)
    first = (root / "plan::workout.ndjson").read_text()
    plan_schema.record_plan("workout", plan, "2026-06-18", "personal-trainer", root)
    assert (root / "plan::workout.ndjson").read_text() == first, "an identical re-entry appended a duplicate line"
    assert len(store.read("plan::workout", root=root)) == 1


def test_re_fired_tick_same_date_no_duplicate_promote(tmp_path):
    # AC-7(b) idempotency over the RUNNER surface (a re-fired tick over the same seeded state): a second
    # cadence tick at the SAME plan_date does not double-write — the derived debounce (min-interval) blocks
    # the same-date re-gen, so every plan::<domain> gains 0 duplicate rows.
    root = _regen_root(tmp_path, "refire-idem", _REGRESSING)
    cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    rows_first = {d: len(store.read(f"plan::{d}", root=root)) for d in plan_schema.PLAN_DOMAINS}
    receipt2 = cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                                  deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    rows_second = {d: len(store.read(f"plan::{d}", root=root)) for d in plan_schema.PLAN_DOMAINS}
    assert rows_second == rows_first, "a same-date re-fired tick double-wrote plan rows"
    assert receipt2.get("regenerated") is False and receipt2.get("reason") == "debounced", (
        f"the same-date re-fire was not debounced: {receipt2}"
    )


def test_no_new_keying_in_runner():
    # AC-7(c) dedupe-key boundary: the runner introduces NO new keying — 0 re-declaration of the frozen
    # (item, timepoint, source) identity. A source-property assertion (the runner reuses store.append /
    # store.read_all; it authors no key).
    src = (REPO_ROOT / "scripts/runner/store_lock.py").read_text()
    for token in ("dedupe_key", "DEDUPE_FIELDS", "LINE_FIELDS", "_DEDUPE_EXCLUDED"):
        assert src.count(token) == 0, f"store_lock.py re-declares store keying ({token})"
    assert "import keying" not in src and "from scripts.store import keying" not in src, (
        "store_lock.py imports the store keying module (it authors no key — reuse via store.append/read)"
    )


# =====================================================================================
# AC-8 — 0 live-API calls on the lock/tick path ---------------------------------------
# =====================================================================================


def test_no_live_backend_on_lock_path(tmp_path, monkeypatch):
    # AC-8: the whole lock + tick path runs over injected mocks only — 0 self-constructed ModelClient
    # (and thus 0 live no-train backend / 0 spend).
    from scripts.model.client import ModelClient

    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *a, **k):
        instantiations.append(self)
        return real_init(self, *a, **k)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)
    root = _regen_root(tmp_path, "no-live", _REGRESSING)
    with store_lock.cadence_lock(root) as acquired:
        assert acquired is True
    cadence_runner.run(root, dispatch_factory=lambda: _TrendDispatch(),
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert instantiations == [], "the lock/tick path constructed a ModelClient (must use injected mocks only)"
