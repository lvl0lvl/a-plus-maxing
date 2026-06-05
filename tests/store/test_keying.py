"""Tests for scripts/store/keying.py — the single key + field-set definition."""

import subprocess
from pathlib import Path

import pytest

from scripts.store import keying

REPO_ROOT = Path(__file__).resolve().parents[2]

# The Line Field Set fixed by the ADR-0002-T0 spike.
EXPECTED_FIELDS = {"item", "timepoint", "source", "value"}


def _reading():
    """Return a reading carrying every Line Field Set field."""
    return {
        "item": "fasting-glucose",
        "timepoint": "2026-06-01T08:00:00+00:00",
        "source": "manual",
        "value": 92,
    }


def test_line_field_set_is_the_spike_contract():
    """keying exposes the exact Line Field Set field names from the spike."""
    assert set(keying.LINE_FIELDS) == EXPECTED_FIELDS


def test_dedupe_key_is_item_timepoint_source():
    """The dedupe identity is the (item, timepoint, source) tuple."""
    reading = _reading()
    assert keying.dedupe_key(reading) == (
        reading["item"],
        reading["timepoint"],
        reading["source"],
    )


def test_dedupe_key_excludes_value():
    """value is not part of reading identity — two values, same key."""
    a = _reading()
    b = _reading()
    b["value"] = 200
    assert keying.dedupe_key(a) == keying.dedupe_key(b)


def test_complete_reading_is_conformant():
    """A reading with every required field reports conformant."""
    assert keying.is_conformant(_reading()) is True


@pytest.mark.parametrize("missing", sorted(EXPECTED_FIELDS))
def test_missing_field_is_not_conformant(missing):
    """A reading missing any single required field reports non-conformant."""
    reading = _reading()
    del reading[missing]
    assert keying.is_conformant(reading) is False


def test_vault_store_is_gitignored():
    """`.gitignore` carries a vault/store/ entry and the path is ignored."""
    gitignore = (REPO_ROOT / ".gitignore").read_text()
    assert "vault/store/" in gitignore

    result = subprocess.run(
        ["git", "check-ignore", "vault/store/fasting-glucose.ndjson"],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    assert result.returncode == 0
