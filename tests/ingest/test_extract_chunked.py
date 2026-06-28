"""Tests for the chunk + aggregate + dedupe + honest-partial extraction front (ADR-0031-T2).

`scripts.ingest.extract_chunked.extract_all(text, client)` is the local-extraction front that
takes already-extracted document TEXT plus an injected model client and:

  - splits the text into bounded line-boundary chunks with overlap;
  - calls `client.extract_readings(chunk, "text/plain")` once per chunk (the crown-jewel
    text-only path — never a raw-binary/document block);
  - aggregates the UNION of every chunk's readings, deduped through the UNCHANGED
    `keying.dedupe_key` (the single source of truth — no second key);
  - returns `{"readings": [...], "complete": bool, "note": str | None}` — the HONEST
    too-large/partial signal (never a silent empty list on an over-budget document).

Every test injects a per-call RECORDING mock (records each call's (content, media_type) and
returns a distinct per-call batch, or raises on a designated call) — 0 live spend, no key, no
network. The mock is NOT `tests/model/test_client.py::_FixtureBackend` (which returns the same
result on every call and so cannot vary per chunk).
"""

from pathlib import Path

import pytest

from scripts.ingest import extract_chunked
from scripts.ingest.extract_chunked import (
    _CHUNK_CHARS,
    _MAX_CHUNKS,
    extract_all,
)
from scripts.model.client import ModelCallError
from scripts.store.keying import dedupe_key


# --- recording mock + fixtures -------------------------------------------------


class _RecordingClient:
    """A per-call recording mock model client — records each call, returns a scripted batch.

    Records every `extract_readings(content, media_type)` call's `(content, media_type)` into
    `self.calls`, then returns the next per-call result: `scripts[call_index]` when a `scripts`
    list is given, else `default_factory(call_index)`. A result that is an `Exception` is RAISED
    on that call (the fail-closed script). Never a live API call.

    Attributes:
        scripts (list | None): Per-call results indexed by call number (a reading list or an
            Exception to raise); None defers to `default_factory`.
        default_factory (callable | None): `(call_index) -> list` generating a distinct per-call
            batch when `scripts` is None.
        calls (list): The recorded `(content, media_type)` tuples, one per call.
    """

    def __init__(self, scripts=None, default_factory=None):
        self.scripts = scripts
        self.default_factory = default_factory
        self.calls = []

    def extract_readings(self, content, media_type):
        idx = len(self.calls)
        self.calls.append((content, media_type))
        result = self.scripts[idx] if self.scripts is not None else self.default_factory(idx)
        if isinstance(result, Exception):
            raise result
        return result


def _reading(item, value="v", timepoint="2026-01-15", source="quest-labs"):
    """A well-formed Line-Field-Set reading (item, timepoint, source, value)."""
    return {"item": item, "timepoint": timepoint, "source": source, "value": value}


def _text_of_chars(n_chars, line_len=80):
    """Build >= n_chars of newline-delimited text in short (<< chunk) lines.

    Short lines (well under `_CHUNK_CHARS`) exercise the line-boundary split path (never the
    degenerate single-long-line hard-split), and the size is expressed RELATIVE to the imported
    module constants so the fixtures survive any OQ-2 retuning (NFR-7) — never a hardcoded count.
    """
    line = ("x" * (line_len - 1)) + "\n"
    return line * ((n_chars // line_len) + 1)


# --- Cycle 1: chunk + per-chunk text-path call + union + keying dedupe + honest signal ---


def test_single_chunk_round_trip_returns_complete_with_readings():
    """AC-1: a one-chunk text → exactly one extract_readings(text, "text/plain") call → complete."""
    text = "line one\nline two\nline three\n"  # << _CHUNK_CHARS → exactly one chunk
    batch = [_reading("HbA1c", "5.4%"), _reading("ALT", "31 U/L")]
    client = _RecordingClient(scripts=[batch])

    result = extract_all(text, client)

    assert len(client.calls) == 1
    assert client.calls[0] == (text, "text/plain")
    assert result == {"readings": batch, "complete": True, "note": None}


def test_every_extract_call_carries_text_plain_media_type():
    """AC-2 (CROWN-JEWEL): every recorded call is "text/plain" over a str chunk of the input."""
    text = _text_of_chars(3 * _CHUNK_CHARS)
    client = _RecordingClient(default_factory=lambda i: [_reading(f"item-{i}")])

    extract_all(text, client)

    assert len(client.calls) >= 3
    for content, media_type in client.calls:
        assert media_type == "text/plain"
        assert isinstance(content, str)
        # a contiguous text/plain chunk of the input — never a constructed binary/document block
        assert content in text


def test_n_chunk_union_aggregates_all_distinct_readings():
    """AC-3 (NON-TAUTOLOGICAL union): N>=3 chunks, distinct reading per chunk → union of all N."""
    text = _text_of_chars(3 * _CHUNK_CHARS)
    client = _RecordingClient(default_factory=lambda i: [_reading(f"item-{i}", value=f"v{i}")])

    result = extract_all(text, client)

    n = len(client.calls)
    assert n >= 3
    assert result["complete"] is True
    assert len(result["readings"]) == n  # every chunk's distinct reading survived (deduped)
    items = {r["item"] for r in result["readings"]}
    assert "item-2" in items  # the chunk-3-only (index 2) reading IS present — 0 dropped
    assert items == {f"item-{i}" for i in range(n)}


def test_distinct_mocks_yield_distinct_aggregates():
    """NON-TAUTOLOGICAL: fixture A → aggregate A, a DIFFERENT fixture B → aggregate B, A != B."""
    text = _text_of_chars(3 * _CHUNK_CHARS)
    client_a = _RecordingClient(default_factory=lambda i: [_reading(f"A-{i}", value=f"a{i}")])
    client_b = _RecordingClient(default_factory=lambda i: [_reading(f"B-{i}", value=f"b{i}")])

    result_a = extract_all(text, client_a)
    result_b = extract_all(text, client_b)

    assert result_a["readings"] != result_b["readings"]
    assert result_a["readings"] and all(r["item"].startswith("A-") for r in result_a["readings"])
    assert result_b["readings"] and all(r["item"].startswith("B-") for r in result_b["readings"])


def test_cross_overlap_duplicate_readings_deduped_via_keying():
    """AC-4: a reading shared across chunks (the overlap region) collapses to ONE via keying."""
    text = _text_of_chars(3 * _CHUNK_CHARS)
    shared = _reading("HbA1c", value="5.4%")
    client = _RecordingClient(
        default_factory=lambda i: [shared, _reading(f"item-{i}", value=f"v{i}")]
    )

    result = extract_all(text, client)
    readings = result["readings"]

    keys = [dedupe_key(r) for r in readings]
    assert len(keys) == len(set(keys))  # 0 duplicate (item, timepoint, source) identities
    assert keys.count(dedupe_key(shared)) == 1  # the cross-chunk shared identity carried ONCE


def test_over_budget_text_returns_incomplete_with_note_and_partial_readings():
    """AC-5 (HONEST signal): over-budget text → complete False + truthy note + NON-empty readings."""
    text = _text_of_chars((_MAX_CHUNKS + 1) * _CHUNK_CHARS)
    client = _RecordingClient(default_factory=lambda i: [_reading(f"item-{i}", value=f"v{i}")])

    result = extract_all(text, client)

    assert result["complete"] is False
    assert result["note"]  # a truthy, non-empty note describing the over-budget condition
    assert result["readings"]  # NON-empty — the partial it DID extract, never a silent []
    assert len(client.calls) == _MAX_CHUNKS  # bounded work — the first _MAX_CHUNKS chunks only


def test_within_budget_text_returns_complete_none_note():
    """AC-5 within-budget: a text within _MAX_CHUNKS → complete True, note None."""
    text = _text_of_chars(2 * _CHUNK_CHARS)
    client = _RecordingClient(default_factory=lambda i: [_reading(f"item-{i}")])

    result = extract_all(text, client)

    assert len(client.calls) <= _MAX_CHUNKS
    assert result["complete"] is True
    assert result["note"] is None


# --- Cycle 2: fail-closed ModelCallError propagation + reuse-keying / no-SDK discipline ---


def test_chunk_model_call_error_propagates_no_fabricated_readings():
    """AC-6 (FAIL-CLOSED): a chunk ModelCallError propagates, never a swallowed partial/false-complete."""
    text = _text_of_chars(3 * _CHUNK_CHARS)

    def factory(i):
        # The SECOND chunk fails — chunk 0 already returned readings, so a swallow-into-partial
        # impl would return them; the propagate-unswallowed contract discards them and raises.
        if i == 1:
            return ModelCallError("backend call failed")
        return [_reading(f"item-{i}")]

    client = _RecordingClient(default_factory=factory)

    with pytest.raises(ModelCallError):
        extract_all(text, client)


def test_extract_chunked_reuses_keying_imports_no_model_sdk():
    """AC-7 (STRUCTURAL): the source reuses keying, defines no second key, imports no model SDK."""
    src = Path(extract_chunked.__file__).read_text()

    # (a) reuses the shared keying surface — both the key and the conformance guard
    assert "dedupe_key" in src
    assert "is_conformant" in src
    assert "keying" in src

    # (b) defines no second dedupe identity (no local key def, no re-typed LINE_FIELDS tuple)
    assert "def dedupe" not in src
    assert "def _dedupe" not in src
    assert "LINE_FIELDS" not in src
    assert '("item", "timepoint", "source"' not in src

    # (c) imports no model-client SDK / outbound network client (the client is injected)
    for marker in (
        "anthropic",
        "socket.create_connection",
        "urllib.request",
        "http.client",
        "requests",
        "httpx",
        "scripts.model.client",
    ):
        assert marker not in src, f"extract_chunked must not reference {marker!r} (client is injected)"
