"""Tests for scripts/store/store.py — local NDJSON append/read library."""

import json
import os
import socket
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from scripts.store import keying, store

REPO_ROOT = Path(__file__).resolve().parents[2]


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


def test_append_preserves_prior_timepoint(tmp_path):
    """AC-1: after append(T1) then append(T2), read returns exactly both."""
    store.append("rhr", _reading("2026-06-01T08:00:00+00:00", 55), root=tmp_path)
    store.append("rhr", _reading("2026-06-02T08:00:00+00:00", 58), root=tmp_path)

    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 2
    timepoints = {r["timepoint"] for r in readings}
    assert timepoints == {
        "2026-06-01T08:00:00+00:00",
        "2026-06-02T08:00:00+00:00",
    }


def test_read_orders_by_timepoint(tmp_path):
    """AC-2: read returns readings strictly ascending by timepoint."""
    t1 = "2026-06-01T08:00:00+00:00"
    t2 = "2026-06-02T08:00:00+00:00"
    t3 = "2026-06-03T08:00:00+00:00"
    # Append strictly shuffled: T3, T1, T2.
    store.append("rhr", _reading(t3), root=tmp_path)
    store.append("rhr", _reading(t1), root=tmp_path)
    store.append("rhr", _reading(t2), root=tmp_path)

    got = [r["timepoint"] for r in store.read("rhr", root=tmp_path)]
    assert got == [t1, t2, t3]


def test_reappend_same_reading_no_new_line(tmp_path):
    """AC-3: re-appending the same reading leaves line count unchanged."""
    reading = _reading("2026-06-01T08:00:00+00:00", 55)
    store.append("rhr", reading, root=tmp_path)
    store.append("rhr", reading, root=tmp_path)
    assert _line_count(tmp_path) == 1


@pytest.mark.parametrize("missing", sorted(keying.LINE_FIELDS))
def test_append_missing_field_raises_no_line(tmp_path, missing):
    """AC-5 (Risk N2): append raises on any missing field; writes 0 lines."""
    reading = _reading("2026-06-01T08:00:00+00:00", 55)
    del reading[missing]

    before = _line_count(tmp_path)
    with pytest.raises(ValueError):
        store.append("rhr", reading, root=tmp_path)
    assert _line_count(tmp_path) == before


def test_append_read_zero_egress(tmp_path):
    """AC-4 (D1->D2): a real append->read under sandbox-exec deny-network.

    The store path is run inside an OS-level no-network sandbox (the ADR-0001-T0
    egress-capture mechanism). If the real append+read made any outbound network
    call it would fail under the sandbox; exit 0 is evidence of 0 outbound calls.
    A 0-login assertion is enforced statically: store.py imports no auth/network
    client.
    """
    if subprocess.run(
        ["/usr/bin/sandbox-exec", "-p", "(version 1)(allow default)", "/usr/bin/true"],
        capture_output=True,
    ).returncode != 0:
        pytest.fail("sandbox-exec not invocable — AC-4 BLOCKED, not skipped")

    # Network-presence precondition: a direct unguarded connect must SUCCEED, else
    # the deny-direction control below is not exercisable (attribute exit-0 to the
    # sandbox, not to an offline host).
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3).close()
    except OSError:
        pytest.skip("no network — AC-4 deny-direction not exercisable")

    profile = "(version 1)(allow default)(deny network*)"

    # Fail-direction control: an outbound connect under the SAME deny profile must
    # exit NON-zero — proving the deny is load-bearing, not a vacuous pass.
    fail_driver = tmp_path / "fail_driver.py"
    fail_driver.write_text(
        "import socket; socket.create_connection(('1.1.1.1', 53), timeout=3)\n"
    )
    fail_result = subprocess.run(
        ["/usr/bin/sandbox-exec", "-p", profile, sys.executable, str(fail_driver)],
        capture_output=True,
        text=True,
    )
    assert fail_result.returncode != 0, (fail_result.stdout, fail_result.stderr)

    store_root = tmp_path / "store"
    driver = tmp_path / "driver.py"
    driver.write_text(
        textwrap.dedent(
            f"""
            import sys
            sys.path.insert(0, {str(REPO_ROOT)!r})
            from scripts.store import store

            root = {str(store_root)!r}
            store.append("rhr", {{
                "item": "rhr",
                "timepoint": "2026-06-01T08:00:00+00:00",
                "source": "manual",
                "value": 55,
            }}, root=root)
            readings = store.read("rhr", root=root)
            assert len(readings) == 1, readings
            print("OK")
            """
        )
    )

    result = subprocess.run(
        ["/usr/bin/sandbox-exec", "-p", profile, sys.executable, str(driver)],
        capture_output=True,
        text=True,
    )
    # Exit 0 == the real append+read completed with no route off-host == 0
    # outbound network calls carrying store content.
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "OK" in result.stdout

    # 0 login step: the store source imports no auth / network / model client
    # and makes no login/auth call. Matched on import/call signatures (not bare
    # prose substrings) so the assertion turns red on a real client, not a word.
    src = (REPO_ROOT / "scripts" / "store" / "store.py").read_text()
    for client in ("anthropic", "openai", "voyageai", "requests", "httpx", "urllib", "socket"):
        assert f"import {client}" not in src
        assert f"from {client}" not in src
    for call in (".login(", ".authenticate(", ".auth("):
        assert call not in src


def test_read_skips_malformed_line_and_warns(tmp_path, capfd):
    """Read tolerates a torn line: skip it, warn on STORE-SKIP:, return the rest."""
    path = _item_file(tmp_path)
    good = _reading("2026-06-01T08:00:00+00:00", 55)
    # Line 1 good, line 2 torn (truncated JSON object).
    path.write_text(json.dumps(good) + "\n" + '{"item": "rhr"\n')

    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 1
    assert readings[0]["timepoint"] == "2026-06-01T08:00:00+00:00"

    err = capfd.readouterr().err
    assert f"STORE-SKIP: {path}:2" in err


def test_append_survives_preexisting_malformed_line(tmp_path):
    """A pre-existing torn line no longer bricks append; both good readings survive."""
    path = _item_file(tmp_path)
    good = _reading("2026-06-01T08:00:00+00:00", 55)
    path.write_text(json.dumps(good) + "\n" + "not json\n")

    new = _reading("2026-06-02T08:00:00+00:00", 58)
    store.append("rhr", new, root=tmp_path)  # must not raise

    timepoints = {r["timepoint"] for r in store.read("rhr", root=tmp_path)}
    assert timepoints == {
        "2026-06-01T08:00:00+00:00",
        "2026-06-02T08:00:00+00:00",
    }


def test_append_is_atomic_on_write_failure(tmp_path, monkeypatch):
    """A crash mid-write leaves the prior file intact — no torn line.

    Proves atomicity by simulating a crash *after* some bytes have been written but
    before the write completes. File writes are not atomic, so we wrap the file
    handle's `write` to land a partial line and then raise. We wrap whichever open
    the production code uses for writing — `Path.open` (old "a"-mode append) and
    `os.fdopen` (temp+replace) — and only for write modes, so the dedupe read
    (`Path.open("r")` via read_text) is untouched. Under the old append the partial
    bytes hit the real item file directly, tearing it (RED). Under temp+replace the
    partial bytes hit a temp file that is never os.replace'd onto the original, so
    the item file is byte-for-byte unchanged (GREEN).
    """
    prior = _reading("2026-06-01T08:00:00+00:00", 55)
    store.append("rhr", prior, root=tmp_path)
    before = _item_file(tmp_path).read_text()

    def _tear(fh):
        real_write = fh.write

        def _partial_then_raise(data):
            real_write(data[: len(data) // 2 or 1])  # land a partial line
            raise OSError("simulated crash mid-write")

        fh.write = _partial_then_raise
        return fh

    orig_path_open = type(tmp_path).open
    orig_fdopen = os.fdopen

    def _torn_path_open(self, mode="r", *a, **k):
        fh = orig_path_open(self, mode, *a, **k)
        return _tear(fh) if any(c in mode for c in "aw+x") else fh

    def _torn_fdopen(fd, mode="r", *a, **k):
        fh = orig_fdopen(fd, mode, *a, **k)
        return _tear(fh) if any(c in mode for c in "aw+x") else fh

    # Patch only across the append; post-assertions need a working read/write path.
    # The old "a"-mode append writes via Path.open; temp+replace writes via
    # os.fdopen — wrapping both makes one test red the old path and green the new.
    with monkeypatch.context() as mp:
        mp.setattr(type(tmp_path), "open", _torn_path_open)
        mp.setattr(os, "fdopen", _torn_fdopen)
        with pytest.raises(OSError):
            store.append("rhr", _reading("2026-06-02T08:00:00+00:00", 58), root=tmp_path)

    # File unchanged: same bytes, exactly one prior reading, no torn line.
    after = _item_file(tmp_path).read_text()
    assert after == before
    readings = store.read("rhr", root=tmp_path)
    assert len(readings) == 1
    assert readings[0]["timepoint"] == "2026-06-01T08:00:00+00:00"
    for ln in after.splitlines():
        if ln.strip():
            json.loads(ln)  # every non-blank line parses — no partial line
