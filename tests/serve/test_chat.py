"""E2E + dispatch tests for the POST `/chat` egress seam (ADR-0016-T1).

The `/chat` route is a SIBLING on the UNCHANGED loopback `ThreadingHTTPServer`
(`("127.0.0.1", port)`); the per-turn dispatch in `scripts/serve/chat.py` chains
`plan_next_turn` -> `client.converse` -> `extract_facts` -> `persist_capture` -> the
per-turn receipt, over a MOCK client (no live API). The acceptance coverage:

- AC-1 (loopback sibling route): the `_LOOPBACK` bind literal is byte-unchanged (0 binds
  to `0.0.0.0`/`""`) and `/chat` is served by the same loopback server (the route table
  is {GET `/`, POST `/upload`, POST `/chat`}).
- AC-2 (one turn in/out): a POST `/chat` over a mock client returns the assistant reply +
  the per-turn capture receipt (`{"store":[...],"scaffold":[...]}`) + the intake progress.
- AC-4 (per-turn extraction, CONCERN-2): turn-1's landed facts are visible to turn-2's
  `missing_fields` (the extractor ran each turn), and no session-spanning raw transcript
  surface is held.
- AC-5 (fail-closed turn): each failure mode (failed/timed-out/rate-limited/empty) yields a
  degraded turn that surfaces the failure + degrades toward the form, fabricating no reply,
  no fact, and writing nothing to the store on that turn.
- AC-6 (thread survival): a malformed `/chat` body / a model-client exception yields a
  degraded response, not a dropped connection (mirrors `/upload`'s catch-and-re-render).
"""

import http.client
import json
import threading
from pathlib import Path

from scripts.model.client import ModelCallError
from scripts.serve import chat
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


class _ReplyBackend:
    """A mock converse backend that records its `messages` and returns a scripted result.

    Captures every `converse(messages)` payload into `self.calls` (the no-egress test
    inspects what the model call carried) and returns a fixed `{"reply", "extraction"}`.
    """

    def __init__(self, reply="ok", extraction=None):
        self.reply = reply
        self.extraction = {} if extraction is None else extraction
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        return {"reply": self.reply, "extraction": dict(self.extraction)}


class _RaisingBackend:
    """A mock converse backend that raises ModelCallError (the failed-call modes)."""

    def __init__(self, message="backend failed"):
        self.message = message
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        raise ModelCallError(self.message)


class _EmptyReplyBackend:
    """A mock backend whose successful call returns an empty reply (the empty failure mode).

    `ModelClient.converse` raises `ModelCallError` on a falsy `reply`, so this drives the
    empty-result fail-closed branch through the real client shape-check.
    """

    def __init__(self):
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        return {"reply": "", "extraction": {}}


def _server_with_chat(tmp_path, backend):
    """Build a loopback server whose `/chat` dispatch uses a tmp store + a mock client.

    Points the handler's store/scaffold roots at tmp dirs and injects a mock model
    client (over the given backend) so the E2E never touches the real store and never
    makes a live API call.
    """
    from scripts.model.client import ModelClient

    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=ModelClient(backend=backend),
    )
    return srv, srv.server_address[1]


def _post_chat(port, payload):
    """POST a JSON `/chat` turn body; return (status, parsed-or-raw response)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps(payload).encode("utf-8") if isinstance(payload, (dict, list)) else payload
    conn.request("POST", "/chat", body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    try:
        return resp.status, json.loads(text)
    except json.JSONDecodeError:
        return resp.status, text


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 / AC-2 / AC-4
# --------------------------------------------------------------------------- #


def test_loopback_bind_literal_is_byte_unchanged():
    """AC-1: the `_LOOPBACK` bind literal is `127.0.0.1`; 0 binds to `0.0.0.0`/`""`.

    The `/chat` route is a sibling on the SAME loopback server — it adds no new bind.
    Reds if the literal changes or a routable/wildcard bind appears in `server.py`.
    """
    assert serve_server._LOOPBACK == "127.0.0.1"
    src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    # The bind is `(_LOOPBACK, port)` only — no wildcard/routable literal anywhere.
    assert 'ThreadingHTTPServer((_LOOPBACK, port)' in src
    for routable in ('"0.0.0.0"', "'0.0.0.0'", 'ThreadingHTTPServer((""', "(('',"):
        assert routable not in src, f"a routable/wildcard bind {routable!r} appeared"


def test_chat_is_a_sibling_route_on_the_same_loopback_server(tmp_path):
    """AC-1: POST `/chat` is served by the SAME loopback server; the route table grew.

    The handler is one `ThreadingHTTPServer` bound to ("127.0.0.1", port); GET `/` and
    POST `/upload` still answer, and POST `/chat` now answers (not 404) on the same port.
    """
    backend = _ReplyBackend(reply="hello")
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        assert srv.server_address[0] == "127.0.0.1"
        # GET `/` still serves the wizard (the route table did not lose a route).
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        assert conn.getresponse().status == 200
        conn.close()
        # POST `/chat` answers on the same port — not a 404 (the route was added).
        status, _ = _post_chat(port, {"turn": "hi", "conversation": [], "covered_domains": []})
        assert status == 200
    finally:
        srv.shutdown()
        srv.server_close()


def test_chat_turn_returns_reply_receipt_and_progress(tmp_path):
    """AC-2: one POST `/chat` returns assistant reply + capture receipt + progress.

    Over a mock client whose extraction proposes one wired token, the response carries
    (a) the assistant reply text, (b) the `persist_capture` `{"store","scaffold"}` receipt
    reflecting what landed, and (c) the intake-progress state (the `plan_next_turn` intent).
    """
    backend = _ReplyBackend(reply="got it", extraction={"recovery-status-band": "moderate"})
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(
            port, {"turn": "recovery is moderate", "conversation": [],
                   "covered_domains": ["training"]}
        )
        assert status == 200
        assert resp["reply"] == "got it"
        assert "receipt" in resp and "store" in resp["receipt"] and "scaffold" in resp["receipt"]
        # The wired token actually landed in the store (the receipt is not vacuous).
        assert "recovery-status-band" in resp["receipt"]["store"]
        assert "progress" in resp
        landed = store.read("recovery-status-band", root=tmp_path / "store")
        assert len(landed) == 1 and landed[0]["value"] == "moderate"
    finally:
        srv.shutdown()
        srv.server_close()


def test_per_turn_extraction_makes_turn1_facts_visible_to_turn2(tmp_path):
    """AC-4/CONCERN-2: turn-1's landed facts shrink turn-2's `missing_fields`.

    Turn-1's mock extraction lands `recovery-status-band`; turn-2's `plan_next_turn`
    (run per turn over the de-identified summary) no longer lists `recovery-status-band`
    as missing for the `training` domain — proving the extractor ran each turn and the
    next-turn gap-set is computed against what LANDED in the store, not the transcript.
    """
    backend = _ReplyBackend(reply="noted", extraction={"recovery-status-band": "moderate"})
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        # Turn 1: nothing landed yet -> recovery-status-band is missing for `training`.
        _, t1 = _post_chat(
            port, {"turn": "let's talk training", "conversation": [],
                   "covered_domains": ["training"]}
        )
        assert "recovery-status-band" in t1["progress"]["missing_fields"]
        # Turn 2: the same domain — the fact landed in turn 1, so it is no longer missing.
        backend.extraction = {}  # turn-2 proposes nothing new
        _, t2 = _post_chat(
            port, {"turn": "what next", "conversation": [{"role": "user", "content": "hi"}],
                   "covered_domains": ["training"]}
        )
        assert "recovery-status-band" not in t2["progress"]["missing_fields"]
    finally:
        srv.shutdown()
        srv.server_close()


def test_dispatch_holds_no_session_spanning_raw_transcript(tmp_path):
    """AC-4/CONCERN-2: the dispatch holds no module-level raw-transcript surface.

    The transcript residency is one turn — the dispatch consumes the conversation passed
    in per call and keeps no session-spanning raw-transcript accumulator on the module or
    the handler class. Reds if a `_transcript`/`_history`/`_session` mutable buffer appears.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "chat.py").read_text()
    for accumulator in ("_TRANSCRIPT", "_HISTORY", "_SESSION_TRANSCRIPT", "_transcript_log"):
        assert accumulator not in src, (
            f"chat.py holds a session-spanning raw-transcript surface ({accumulator!r}) — "
            f"the transcript residency must be one turn (CONCERN-2)"
        )


# --------------------------------------------------------------------------- #
# Cycle 3 — AC-5 / AC-6
# --------------------------------------------------------------------------- #


def test_failed_model_call_returns_a_degraded_turn_with_no_store_write(tmp_path):
    """AC-5: a failed/timed-out/rate-limited model call -> a degraded turn, 0 store write.

    Each failure mode raises `ModelCallError`. The dispatch returns a degraded turn that
    (a) surfaces the failure + degrades toward the demographic form, (b) fabricates no
    assistant reply, (c) fabricates no extracted fact, (d) writes NOTHING to the store.
    """
    for message in ("call failed", "timed out", "rate limited"):
        backend = _RaisingBackend(message)
        srv, port = _server_with_chat(tmp_path, backend)
        _serve_in_thread(srv)
        try:
            status, resp = _post_chat(
                port, {"turn": "hello", "conversation": [], "covered_domains": ["training"]}
            )
            assert status == 200
            assert resp["degraded"] is True, f"{message}: not marked degraded"
            assert resp.get("reply") in (None, ""), f"{message}: fabricated an assistant reply"
            # The receipt landed nothing — no fabricated fact, no store write on this turn.
            assert resp["receipt"]["store"] == [], f"{message}: wrote a fact on a failed turn"
            # The honest degrade surfaces the failure + the demographic-form fallback.
            assert resp.get("degrade_to") == "form", f"{message}: did not degrade toward the form"
        finally:
            srv.shutdown()
            srv.server_close()
        # No store item materialized for this failure mode.
        assert store.read("recovery-status-band", root=tmp_path / "store") == []


def test_empty_model_result_fails_closed(tmp_path):
    """AC-5: an empty result from a successful call fails closed (no reply/fact/write)."""
    backend = _EmptyReplyBackend()
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(
            port, {"turn": "hello", "conversation": [], "covered_domains": ["training"]}
        )
        assert status == 200
        assert resp["degraded"] is True
        assert resp.get("reply") in (None, "")
        assert resp["receipt"]["store"] == []
    finally:
        srv.shutdown()
        srv.server_close()


def test_malformed_body_does_not_drop_the_thread(tmp_path):
    """AC-6: a malformed `/chat` body -> a degraded response, not a dropped connection.

    Mirrors `/upload`'s catch-and-re-render: a non-JSON body is caught and answered with a
    degraded response (the connection is not killed), and the server survives to serve the
    next request.
    """
    backend = _ReplyBackend(reply="ok")
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(port, b"not json at all{{{")
        assert status in (200, 400), "the malformed body dropped the connection"
        if isinstance(resp, dict):
            assert resp.get("degraded") is True
        # The server survived — a well-formed request still answers on the same port.
        ok_status, ok_resp = _post_chat(
            port, {"turn": "hi", "conversation": [], "covered_domains": []}
        )
        assert ok_status == 200 and ok_resp["reply"] == "ok"
    finally:
        srv.shutdown()
        srv.server_close()


def test_model_client_exception_does_not_drop_the_thread(tmp_path):
    """AC-6: a model-client exception -> a degraded response; the thread survives."""
    backend = _RaisingBackend("boom")
    srv, port = _server_with_chat(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(
            port, {"turn": "hi", "conversation": [], "covered_domains": []}
        )
        assert status == 200
        assert resp["degraded"] is True
        # The server survived the model-client exception.
        ok_status, _ = _post_chat(port, {"turn": "again", "conversation": [], "covered_domains": []})
        assert ok_status == 200
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# H-2 — the /chat dispatch threads identity_config behaviorally (QA F1)
# --------------------------------------------------------------------------- #


_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def test_dispatch_identity_config_round_trip_changes_detection(tmp_path):
    """H-2/QA F1: the `/chat` dispatch threads `identity_config` so an operator-identity
    value routes record-only WITH the config and lands WITHOUT it.

    The structural seam test alone passes even if `dispatch_turn` drops `identity_config=`
    from the persist call (QA F1: 0 failures). This BEHAVIORAL round-trip mirrors the
    `/upload` `test_identity_config_round_trip_changes_detection`: a model-emitted
    operator-identity value under a free-text wired token routes record-only WHEN an
    instance `identity_config` listing that name is threaded, and LANDS in the model-bound
    token WHEN it is the empty/absent baseline. Same value, same dispatch — only the
    threaded config differs, so the test reds if the dispatch drops `identity_config`.
    """
    from scripts.model.client import ModelClient

    identity_cfg = tmp_path / "operator-identity.txt"
    identity_cfg.write_text("Walter McGivney\n")
    value = "add 10 lb to squat; ask Walter McGivney before changing the program"
    backend = _ReplyBackend(reply="noted", extraction={"goal-targets": value})
    client = ModelClient(backend=backend)

    # WITH the instance config threaded: the name is detected -> record-only to scaffold.
    store_with = tmp_path / "store-with"
    scaffold_with = tmp_path / "scaffold-with"
    chat.dispatch_turn(
        "let's set goals", [], ["goals"], [],
        client=client, store_root=store_with, scaffold_root=scaffold_with,
        identity_config=str(identity_cfg),
    )
    assert store.read("goal-targets", root=store_with) == [], (
        "an operator-identity value reached the model-bound token WITH identity_config threaded"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_with.rglob("*") if p.is_file())
    assert "McGivney" in scaffold_text, "the identity value did not route record-only WITH the config"

    # WITHOUT it (the empty-detection baseline): identity detection is empty, so the value
    # lands in the model-bound token — the no-op baseline the threading changes. If the
    # dispatch drops identity_config, BOTH legs use empty detection and the WITH-config
    # record-only assertion above reds.
    store_without = tmp_path / "store-without"
    chat.dispatch_turn(
        "let's set goals", [], ["goals"], [],
        client=client, store_root=store_without, scaffold_root=tmp_path / "scaffold-without",
        identity_config=_ABSENT_IDENTITY,
    )
    landed = store.read("goal-targets", root=store_without)
    assert landed and "McGivney" in landed[0]["value"], (
        "the empty-detection baseline did not land the value — the round-trip proves nothing"
    )
