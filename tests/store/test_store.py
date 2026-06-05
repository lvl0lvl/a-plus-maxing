"""Tests for scripts/store/store.py — local NDJSON append/read library."""

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
    with pytest.raises(Exception):
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

    profile = "(version 1)(allow default)(deny network*)"
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
