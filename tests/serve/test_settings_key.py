"""Route tests for GET/POST /settings/key — in-app API-key save (Profile screen, loopback).

The Profile screen lets the operator store their no-train API key without a terminal: a
loopback POST writes it to the OS keychain (key_source.store) and a GET reports ONLY
whether a key resolves — never the value. Crown-jewel constraint (NFR-3, the repo is
PUBLIC): the key never appears in any response body. Tests inject the key_store /
key_resolver seams so no real keychain or key is touched, with a synthetic fixture key.
"""

import http.client
import json
import os
import threading

from scripts.model import key_source
from scripts.serve import server as serve_server

# A non-secret fixture deliberately NOT shaped like a real key (no `sk-ant-…` prefix) so
# the NFR-3 tracked-tree key-literal scan stays comprehensive over test files.
_SYNTHETIC_KEY = "synthetic-test-key-route-fixture"


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _request(port, method, path, body=None):
    """Issue one HTTP request to the loopback server; return (status, response_text)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    headers = {"Content-Type": "application/json"} if body is not None else {}
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _raw_post(port, path, body_bytes, *, content_type="application/json", content_length=None):
    """POST raw bytes with an explicit Content-Type/Content-Length; return (status, text).

    Lets a test drive the reject branches the json `_request` helper cannot reach: a
    non-`application/json` Content-Type, a non-numeric Content-Length, and an over-ceiling
    declared length (`content_length` overrides the true byte length).
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.putrequest("POST", path, skip_host=False, skip_accept_encoding=True)
    if content_type is not None:
        conn.putheader("Content-Type", content_type)
    conn.putheader("Content-Length", content_length if content_length is not None else str(len(body_bytes)))
    conn.endheaders()
    conn.send(body_bytes)
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def test_status_reports_connected_when_a_key_resolves():
    """GET /settings/key returns {connected:true} when a key resolves — never the value."""
    srv = serve_server.build_server(0, key_resolver=lambda: _SYNTHETIC_KEY)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/key")
        assert status == 200
        assert json.loads(text) == {"connected": True}
        assert _SYNTHETIC_KEY not in text
    finally:
        srv.shutdown()
        srv.server_close()


def test_status_reports_disconnected_when_no_key():
    """GET /settings/key returns {connected:false} when the resolver raises KeyUnavailable."""
    def _absent():
        raise key_source.KeyUnavailableError("none")

    srv = serve_server.build_server(0, key_resolver=_absent)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/key")
        assert status == 200
        assert json.loads(text) == {"connected": False}
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_saves_key_via_injected_store_and_never_echoes_it():
    """POST /settings/key stores the key via the injected seam; the response carries no key.

    Also pins the immediate-resolvability behavior: a successful save sets the key in the
    process env (env-var first) so the chat works right after Save without a keychain read.
    The test saves and restores `ANTHROPIC_API_KEY` itself — that var gates live 0-spend, so
    leaking it across tests is the isolation defect this guards against.
    """
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    prior_env = os.environ.get(key_source.ENV_VAR)
    try:
        status, text = _request(port, "POST", "/settings/key",
                                json.dumps({"api_key": _SYNTHETIC_KEY}))
        assert status == 200
        assert json.loads(text) == {"ok": True, "connected": True}
        assert saved == [_SYNTHETIC_KEY]   # the key reached the store seam...
        assert _SYNTHETIC_KEY not in text  # ...but never the response body
        # The just-saved key is resolvable in THIS process immediately (env-var first):
        # assert it so deleting that line fails closed rather than passing silently.
        assert os.environ.get(key_source.ENV_VAR) == _SYNTHETIC_KEY
    finally:
        srv.shutdown()
        srv.server_close()
        if prior_env is None:
            os.environ.pop(key_source.ENV_VAR, None)
        else:
            os.environ[key_source.ENV_VAR] = prior_env


def test_post_empty_key_is_rejected_without_storing():
    """POST /settings/key with a blank key returns 400 and the store seam is never called."""
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/key", json.dumps({"api_key": "  "}))
        assert status == 400
        assert saved == []
        assert json.loads(text)["ok"] is False
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_store_failure_returns_500_without_leaking_key():
    """A keychain write failure returns 500 with a constant message — never the key value."""
    def _boom(_key):
        raise key_source.KeyStoreError("Could not store the key in the macOS keychain.")

    srv = serve_server.build_server(0, key_store=_boom)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/key",
                                json.dumps({"api_key": _SYNTHETIC_KEY}))
        assert status == 500
        assert json.loads(text)["ok"] is False
        assert _SYNTHETIC_KEY not in text
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_non_object_json_body_is_400_not_a_dropped_connection():
    """A top-level non-object JSON body returns 400 — never an uncaught AttributeError.

    `123`/`[]`/`"x"`/`true`/`null` are valid JSON but have no `.get`; the handler must
    answer 400 (a readable response), not drop the request thread (the client would see
    RemoteDisconnected). Getting a status back at all proves the connection was not dropped.
    """
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for bad in ("123", "[]", '"x"', "true", "null"):
            status, text = _request(port, "POST", "/settings/key", bad)
            assert status == 400, f"{bad!r} returned {status}, expected 400 (not a dropped connection)"
            assert json.loads(text)["ok"] is False
        assert saved == []  # no malformed body ever reached the store seam
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_non_json_content_type_is_rejected_without_storing():
    """A non-application/json Content-Type is refused (415) so a cross-site simple POST
    (text/plain, no CORS preflight) cannot drive the secret-write route."""
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _raw_post(
            port, "/settings/key",
            json.dumps({"api_key": _SYNTHETIC_KEY}).encode("utf-8"),
            content_type="text/plain",
        )
        assert status == 415
        assert saved == []  # the key never reached the store seam
        assert _SYNTHETIC_KEY not in text
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_non_numeric_content_length_is_400_not_dropped():
    """A non-numeric Content-Length returns 400, not a dropped connection."""
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _raw_post(port, "/settings/key", b"", content_length="not-a-number")
        assert status == 400
        assert saved == []
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_oversize_body_is_413_without_storing():
    """A declared Content-Length over the 16 KiB ceiling is refused 413 before the body is
    read — the store seam is never called."""
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _raw_post(
            port, "/settings/key", b"x",
            content_length=str(serve_server._SETTINGS_MAX_BYTES + 1),
        )
        assert status == 413
        assert saved == []
    finally:
        srv.shutdown()
        srv.server_close()
