"""Single-egress-class proof over the POST `/chat` dispatch (ADR-0016-T1, the crown jewel).

The ONLY model egress is via `scripts/model/`; the `/chat` dispatch makes 0 outbound
calls OF ITS OWN, and the model payload to `converse` carries ONLY the live conversation
(raw) + the de-identified `summarize` context — 0 store-reading content, 0 other
operator's transcript (NFR-1; ADR-0016 Falsification: any raw egress OTHER than the live
conversation is release-blocking).

Two falsifiable halves:
- Half A (no outbound client in the serve layer): `scripts/serve/` imports/uses 0 outbound
  HTTP client (`socket.create_connection`, `urllib`, `http.client`, `requests`, `httpx`) —
  the dispatch's only model egress is the `client.converse` call into `scripts/model/`.
  Mirrors `test_serve_no_egress.py::test_serve_layer_imports_no_outbound_client`.
- Half B (de-identified-context-only payload): over a recording MOCK client, the payload the
  dispatch hands `converse` carries NONE of the seeded raw store values — only the live
  conversation turns + the de-identified `summarize` token mapping (token NAMES, not raw
  operator strings). The negative control (`test_payload_leak_negative_control`) proves the
  assertion is failing-capable: a payload that DID carry a raw store value trips it.
"""

import json
from pathlib import Path

from scripts.model.client import ModelClient
from scripts.serve import chat
from scripts.store import keying, store

REPO_ROOT = Path(__file__).resolve().parents[2]

# The outbound-client surface an egress path would carry at import time (mirrors
# test_serve_no_egress.py). The grep reds the moment any appears in scripts/serve/.
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)

# A raw store VALUE seeded into the instance — the kind of content that must NEVER appear
# in the model payload (only its de-identified token NAME may, via the summary mapping).
_RAW_STORE_VALUE = "add ten pounds to my squat by autumn"


class _RecordingBackend:
    """A mock converse backend that records the exact `messages` payload it was handed."""

    def __init__(self):
        self.last_messages = None

    def converse(self, messages):
        self.last_messages = messages
        return {"reply": "noted", "extraction": {}}


def _seed_raw_store_value(store_root):
    """Append one raw free-text reading under a wired free-text token (`goal-targets`)."""
    store.append(
        "goal-targets",
        {f: None for f in keying.LINE_FIELDS}
        | {"item": "goal-targets", "timepoint": "2026-06-22",
           "source": "intake", "value": _RAW_STORE_VALUE},
        root=store_root,
    )


def _payload_blob(messages):
    """Flatten the converse `messages` payload to one searchable string."""
    return json.dumps(messages, default=str)


# --------------------------------------------------------------------------- #
# Half A — AC-3: the serve layer carries 0 outbound HTTP client (by construction)
# --------------------------------------------------------------------------- #


def test_serve_layer_carries_no_outbound_client_for_chat():
    """AC-3/Half A: `scripts/serve/` imports 0 outbound HTTP client.

    The `/chat` dispatch's only model egress is `client.converse` into `scripts/model/`;
    the serve layer makes no outbound call of its own. Reds the moment a future edit sneaks
    an outbound import into the serve layer (the standing single-egress-class guard).
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, (
                f"{py.name} references an outbound client ({marker!r}) — the `/chat` "
                f"dispatch's only model egress must be via scripts/model/ (NFR-1)"
            )


# --------------------------------------------------------------------------- #
# Half B — AC-3: the model payload is de-identified-context-only (0 store content)
# --------------------------------------------------------------------------- #


def test_model_payload_carries_no_raw_store_content(tmp_path):
    """AC-3: the `converse` payload carries 0 raw store content / 0 other transcript.

    Seeds a raw store value, runs one dispatch turn over a recording mock client, and
    asserts the payload the dispatch handed `converse` does NOT contain the raw store value
    — only the live conversation (raw) + the de-identified `summarize` token mapping (token
    NAMES). The de-identified token NAME `goal-targets` may appear (it is a field name, not
    raw content); the raw VALUE must not.
    """
    store_root = tmp_path / "store"
    _seed_raw_store_value(store_root)
    backend = _RecordingBackend()

    receipt = chat.dispatch_turn(
        "tell me about my goals", [{"role": "user", "content": "hi"}], ["goals"], [],
        client=ModelClient(backend=backend),
        store_root=store_root, scaffold_root=tmp_path / "scaffold",
    )
    assert receipt["degraded"] is False
    blob = _payload_blob(backend.last_messages)
    # The de-identified-context-only boundary: the raw store value is NOT in the payload.
    assert _RAW_STORE_VALUE not in blob, (
        "the model payload carried a raw store value — the single-egress-class boundary "
        "is breached (ADR-0016 Falsification: any raw egress other than the live "
        "conversation is release-blocking)"
    )
    # The live conversation (raw) IS in the payload (the payload is not empty/vacuous).
    assert "hi" in blob and "tell me about my goals" in blob


def test_payload_leak_negative_control(tmp_path):
    """AC-3 negative control: the de-identified-context-only assertion is failing-capable.

    A payload that DID carry the raw store value trips the assertion — proving the
    `test_model_payload_carries_no_raw_store_content` check can turn RED when the boundary
    is breached (it is not a tautology). This simulates a leak by injecting the raw store
    value into a payload blob and asserting the same membership check fires.
    """
    leaked_messages = [
        {"role": "system", "content": {"raw_store_dump": _RAW_STORE_VALUE}},
        {"role": "user", "content": "hi"},
    ]
    blob = _payload_blob(leaked_messages)
    # The SAME check the positive test runs — here it MUST find the leak (RED-when-broken).
    assert _RAW_STORE_VALUE in blob, (
        "the negative control did not reproduce a leak — the boundary check would be a "
        "tautology if it could never go red"
    )
