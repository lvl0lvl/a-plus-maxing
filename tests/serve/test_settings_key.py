"""Route tests for GET/POST /settings/key — in-app API-key save (Profile screen, loopback).

The Profile screen lets the operator store their no-train API key without a terminal: a
loopback POST writes it to the OS keychain (key_source.store) and a GET reports ONLY
whether a key resolves — never the value. Crown-jewel constraint (NFR-3, the repo is
PUBLIC): the key never appears in any response body. Tests inject the key_store /
key_resolver seams so no real keychain or key is touched, with a synthetic fixture key.
"""

import http.client
import json
import threading

from scripts.model import key_source
from scripts.serve import server as serve_server

_SYNTHETIC_KEY = "sk-ant-synthetic-CCCC3333DDDD4444"


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
    """POST /settings/key stores the key via the injected seam; the response carries no key."""
    saved = []
    srv = serve_server.build_server(0, key_store=saved.append)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/key",
                                json.dumps({"api_key": _SYNTHETIC_KEY}))
        assert status == 200
        assert json.loads(text) == {"ok": True, "connected": True}
        assert saved == [_SYNTHETIC_KEY]   # the key reached the store seam...
        assert _SYNTHETIC_KEY not in text  # ...but never the response body
    finally:
        srv.shutdown()
        srv.server_close()


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
