"""D7 crown-jewel + PKCE authorization-code callback tests for `scripts.serve.oauth_callback`.

The OAuth sibling of the ADR-0049-T1 D2 wire-scan: an app-mediated authorization-code flow whose
one-shot `127.0.0.1` listener exchanges the vendor `code` for a **refresh_token** (in the per-vendor
shape `oauth_pull._parse_credentials` consumes) behind a fail-closed no-follow opener, and writes it
through the ONE extracted `store_oauth_credential` helper into the SAME `a-plus-maxing-<source>-oauth`
item the reader reads. Every leg runs through the REAL injectable opener against REAL loopback fixture
servers (a token endpoint, an attacker/redirect host); the D7 scan is captured at the TRUE HTTP wire
(`opener.open(request)`) over the FULL request and each family is RED-gated by a self-invalidating
mutation on the REAL opener (the D2 gold standard). $0 — no live network / model / OAuth; monkeypatch
+ loopback fixtures only.
"""

import ast
import base64
import hashlib
import http.client
import http.server
import json
import socket
import threading
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest

from scripts.ingest import oauth_pull
from scripts.serve import oauth_callback
from scripts.serve.alpha_config import (
    DEFAULT_CLIENT_TYPES, AlphaConfig, ClientType, VendorCredential)

REPO_ROOT = Path(__file__).resolve().parents[2]

# A store-content sentinel + synthetic secrets, deliberately NOT shaped like real OAuth values and
# short enough that the tracked-tree scans cannot self-match this file's own definition line.
STORE_SENTINEL = "STORE-CONTENT-SENTINEL-xyz"
_CODE_SENTINEL = "auth-code-sentinel"
_VERIFIER_SENTINEL = "verifier-sentinel-xyz"
_CLIENT_SECRET = "whoop-secret-sentinel"
_WHOOP_CID = "whoop-client-id"
_GOOGLE_CID = "google-client-id"


# --------------------------------------------------------------------------------------------------
# Fixtures: loopback token/attacker servers, a recording opener, a mocked secret store.
# --------------------------------------------------------------------------------------------------


def _s256(verifier):
    """The RFC-7636 S256 code challenge for `verifier` (base64url(SHA256(verifier)), no padding)."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


class _TokenEndpoint:
    """A loopback OAuth token endpoint: records the exchange request, optionally validates PKCE.

    Configurable: `response` (the JSON token body on success), `status`, an `expected_challenge`
    (rejects a code_verifier whose S256 != it with 400), and a `redirect_to` (responds 302 to that
    host — the AC-4 attacker case). Records every received request's parsed form params in `.received`.
    """

    def __init__(self, *, response=None, status=200, expected_challenge=None, redirect_to=None):
        self.response = response or {"access_token": "AT", "refresh_token": "RT-refresh"}
        self.status = status
        self.expected_challenge = expected_challenge
        self.redirect_to = redirect_to
        self.received = []
        endpoint = self

        class _Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length).decode("utf-8") if length else ""
                params = {k: v[0] for k, v in parse_qs(raw).items()}
                endpoint.received.append(params)
                if endpoint.redirect_to is not None:
                    self.send_response(302)
                    self.send_header("Location", endpoint.redirect_to)
                    self.end_headers()
                    return
                if endpoint.expected_challenge is not None:
                    verifier = params.get("code_verifier", "")
                    if _s256(verifier) != endpoint.expected_challenge:
                        self.send_response(400)
                        self.end_headers()
                        return
                body = json.dumps(endpoint.response).encode("utf-8")
                self.send_response(endpoint.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self._server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def url(self):
        host, port = self._server.socket.getsockname()[:2]
        return f"http://127.0.0.1:{port}/token"

    @property
    def netloc(self):
        return urlsplit(self.url).netloc

    def close(self):
        self._server.shutdown()
        self._server.server_close()


class _AttackerEndpoint:
    """A loopback host that MUST never be contacted — records a connection count per handled request."""

    def __init__(self):
        self.connections = 0
        endpoint = self

        class _Handler(http.server.BaseHTTPRequestHandler):
            def _seen(self):
                endpoint.connections += 1
                body = b'{"access_token": "PWNED", "refresh_token": "PWNED"}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            do_GET = _seen
            do_POST = _seen

            def log_message(self, *args):
                pass

        self._server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def url(self):
        host, port = self._server.socket.getsockname()[:2]
        return f"http://127.0.0.1:{port}/attacker"

    @property
    def netloc(self):
        return urlsplit(self.url).netloc

    def close(self):
        self._server.shutdown()
        self._server.server_close()


class _RecordingOpener:
    """Wraps the real no-follow opener, recording the FULL outbound request at `opener.open`."""

    def __init__(self, inner, recorder):
        self._inner = inner
        self._recorder = recorder

    def open(self, request, **kwargs):
        self._recorder.append({
            "full_url": request.full_url,
            "headers": dict(request.header_items()),
            "data": request.data,
        })
        return self._inner.open(request, **kwargs)


class _MutantOpener:
    """A self-invalidating mutation on the REAL opener path: runs `on_open(request)` then delegates."""

    def __init__(self, inner, on_open):
        self._inner = inner
        self._on_open = on_open

    def open(self, request, **kwargs):
        self._on_open(request)
        return self._inner.open(request, **kwargs)


def _mock_secret_store(monkeypatch, initial=None):
    """Monkeypatch secret_store.get_secret/set_secret over a shared service->value dict; return it.

    The T3 $0-mock form: the shared-helper write and the `oauth_pull` reader resolve the SAME patched
    functions over one dict, so a callback write and a reader round-trip hit the same item end to end.
    """
    import scripts.secret_store as secret_store

    store = dict(initial or {})
    monkeypatch.setattr(secret_store, "set_secret",
                        lambda service, value: store.__setitem__(service, value))
    monkeypatch.setattr(secret_store, "get_secret", lambda service: store.get(service))
    return store


def _config(**vendors):
    """Build an AlphaConfig fixture: `_config(whoop=(cid, secret), google=(cid, None))` etc."""
    creds = {name: VendorCredential(client_id=cid, client_secret=sec)
             for name, (cid, sec) in vendors.items()}
    return AlphaConfig(vendors=creds, shared_api_key=None, client_types=dict(DEFAULT_CLIENT_TYPES))


def _install_store_read_spy(monkeypatch):
    """Module-level spy over store.read/read_all/items — catches a store read via ANY handle."""
    import scripts.store.store as store

    counter = {"n": 0}

    def _spy(*args, **kwargs):
        counter["n"] += 1
        return []

    monkeypatch.setattr(store, "read", _spy)
    monkeypatch.setattr(store, "read_all", _spy)
    monkeypatch.setattr(store, "items", _spy)
    return counter


def _install_model_lane_spy(monkeypatch):
    """Count no-train model-lane opens: a call-counting fake over `_ClaudeNoTrainBackend`."""
    import scripts.model.client as client

    counter = {"n": 0}

    class _CountingBackend:
        def __init__(self, *args, **kwargs):
            counter["n"] += 1

        def _client(self):
            counter["n"] += 1

    monkeypatch.setattr(client, "_ClaudeNoTrainBackend", _CountingBackend)
    return counter


def _drive_callback(handle, *, state, code=_CODE_SENTINEL):
    """Act as the browser: GET the one-shot listener's redirect_uri with `code`+`state`, then join.

    Returns the callback's HTTP response body text (the browser-facing surface AC-8 scans).
    """
    host, port = handle.address[:2]
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    query = urlencode({"code": code, "state": state})
    conn.request("GET", f"/?{query}")
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    # The write + response both complete before getresponse() returns (the handler writes then
    # responds then marks-served); a short join lets the one-shot teardown settle without a long wait
    # when a mutant keeps the listener alive.
    handle.thread.join(2)
    return text


def _authorize_query(url):
    """Parse the authorize URL's query into a flat dict (the browser_open recorder captured it)."""
    return {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}


# --------------------------------------------------------------------------------------------------
# AC-1: PKCE exchange + write the refresh_token via the shared helper; the reader round-trip.
# --------------------------------------------------------------------------------------------------


def test_ac1_confidential_exchange_writes_blob_and_reader_round_trips(monkeypatch):
    """whoop (CONFIDENTIAL): a matching callback exchanges + writes the {refresh,client_id,secret} blob;
    the written value drives the PRODUCTION reader (`oauth_pull._parse_credentials` + `access_token`)."""
    from scripts.ingest import oauth_pull

    store = _mock_secret_store(monkeypatch)
    token = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT-whoop"})
    browser = []
    records = []
    opener = _RecordingOpener(oauth_pull._OPENER, records)
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=opener, browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        token.expected_challenge = q["code_challenge"]  # the endpoint now validates S256(verifier)
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()

    # the refresh_token blob landed in the EXACT reader item
    assert set(store) == {"a-plus-maxing-whoop-oauth"}
    written = store["a-plus-maxing-whoop-oauth"]
    parsed = oauth_pull._parse_credentials(written)
    assert parsed["refresh_token"] == "RT-whoop"          # the REFRESH token, not the access token
    assert parsed["client_id"] == _WHOOP_CID
    assert parsed["client_secret"] == _CLIENT_SECRET

    # drive the PRODUCTION consumer: the value yields a usable refresh grant forwarding id+secret
    grant = {}

    def _http(method, url, *, headers=None, body=None):
        grant.update({k: v[0] for k, v in parse_qs(body).items()})
        return oauth_pull._HttpResponse(200, b'{"access_token": "fresh"}')

    oauth_pull.access_token("whoop", credential_reader=lambda s: written,
                            credential_writer=lambda s, p: None, http=_http)
    assert grant["grant_type"] == "refresh_token"
    assert grant["refresh_token"] == "RT-whoop"
    assert grant["client_id"] == _WHOOP_CID
    assert grant["client_secret"] == _CLIENT_SECRET


def test_ac1_pkce_public_exchange_writes_bare_refresh_token(monkeypatch):
    """google-health (PKCE_PUBLIC): the bare refresh_token is stored (no secret); the reader parses it."""
    from scripts.ingest import oauth_pull

    store = _mock_secret_store(monkeypatch)
    token = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT-google"})
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "google-health", config=_config(google=(_GOOGLE_CID, None)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        token.expected_challenge = q["code_challenge"]
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()

    assert set(store) == {"a-plus-maxing-google-health-oauth"}
    written = store["a-plus-maxing-google-health-oauth"]
    assert written == "RT-google"                                   # bare refresh token, no secret
    assert oauth_pull._parse_credentials(written) == {"refresh_token": "RT-google"}


def test_ac1_falsifier_pkce_mismatch_writes_nothing(monkeypatch):
    """A token endpoint rejecting a mismatched verifier (400) → the exchange fails-closed, 0 writes."""
    store = _mock_secret_store(monkeypatch)
    # expected_challenge set to a value the real verifier can NEVER match → the endpoint 400s
    token = _TokenEndpoint(expected_challenge="a-challenge-the-real-verifier-will-not-match")
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()
    assert store == {}, "a rejected (non-2xx) exchange must write nothing"


def test_ac1_wrong_value_guard_drives_real_write_and_excludes_access_token(monkeypatch):
    """Wrong-value guard driving the REAL production write: a token response with a DISTINCT
    access_token sentinel → production stores the REFRESH token; the reader round-trip carries the
    refresh sentinel and the access sentinel appears NOWHERE. Would RED if production stored the
    access token (the earlier hand-built assert never drove the write, so it could not — Sec-LOW-2)."""
    from scripts.ingest import oauth_pull

    store = _mock_secret_store(monkeypatch)
    token = _TokenEndpoint(response={"access_token": "ACCESS-SENTINEL", "refresh_token": "REFRESH-SENTINEL"})
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        token.expected_challenge = q["code_challenge"]
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()

    written = store["a-plus-maxing-whoop-oauth"]
    assert "ACCESS-SENTINEL" not in written, "the access token was stored (production wrong-value bug)"
    assert oauth_pull._parse_credentials(written)["refresh_token"] == "REFRESH-SENTINEL"


# --------------------------------------------------------------------------------------------------
# AC-2: loopback-only bind (the REAL bound socket).
# --------------------------------------------------------------------------------------------------


def _assert_loopback(sockname):
    """Assert a real bound address is loopback (127.0.0.1 / ::1), never 0.0.0.0 / a routable host."""
    host = sockname[0]
    assert host in ("127.0.0.1", "::1"), f"listener bound a non-loopback address: {host!r}"


def test_ac2_listener_binds_loopback(monkeypatch):
    """The one-shot listener's REAL bound socket is loopback (`getsockname`, not a config value)."""
    _mock_secret_store(monkeypatch)
    handle = oauth_callback.start_connect(
        "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
        opener=_RecordingOpener(oauth_pull._OPENER, []), browser_open=lambda url: None,
        authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint="http://127.0.0.1:1/token",
    )
    try:
        _assert_loopback(handle.server.socket.getsockname())      # the REAL bound socket
        assert oauth_callback._LOOPBACK == "127.0.0.1"            # the single bind literal
    finally:
        handle.close()


def test_ac2_falsifier_zero_zero_zero_zero_reds():
    """Falsifier: a 0.0.0.0 bound address REDs the loopback assertion (no real 0.0.0.0 bind needed)."""
    with pytest.raises(AssertionError, match="non-loopback"):
        _assert_loopback(("0.0.0.0", 1234))


# --------------------------------------------------------------------------------------------------
# AC-3: state/CSRF mismatch → 0 writes; matching state → the path is live.
# --------------------------------------------------------------------------------------------------


def test_ac3_state_mismatch_writes_nothing(monkeypatch):
    """A callback whose `state` != the issued value → the exchange never runs (0 writes)."""
    store = _mock_secret_store(monkeypatch)
    token = _TokenEndpoint()
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []), browser_open=lambda url: None,
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        _drive_callback(handle, state="not-the-issued-state")
    finally:
        token.close()
    assert store == {}, "a state-mismatched callback must write nothing"
    assert token.received == [], "the exchange must not run on a state mismatch"


def test_ac3_matching_state_writes(monkeypatch):
    """Falsifier for AC-3: the matching-state case DOES write (proves the path is live, not dead)."""
    store = _mock_secret_store(monkeypatch)
    token = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT-live"})
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()
    assert store == {"a-plus-maxing-whoop-oauth": json.dumps(
        {"refresh_token": "RT-live", "client_id": _WHOOP_CID, "client_secret": _CLIENT_SECRET})}


# --------------------------------------------------------------------------------------------------
# AC-4: the redirect host is NEVER CONTACTED on the exchange (the real control, not "0 bytes").
# --------------------------------------------------------------------------------------------------


def test_ac4_redirect_host_never_contacted(monkeypatch):
    """A token endpoint 302-ing to an attacker → the no-follow opener aborts: attacker 0 conns, 0 writes."""
    store = _mock_secret_store(monkeypatch)
    attacker = _AttackerEndpoint()
    token = _TokenEndpoint(redirect_to=attacker.url)
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()
        attacker.close()
    assert attacker.connections == 0, "the redirect/attacker host was contacted (redirect followed)"
    assert store == {}, "a redirect abort must write nothing"


def test_ac4_falsifier_following_opener_contacts_attacker(monkeypatch):
    """Falsifier: a DEFAULT (following) opener follows the 302 → the attacker records a connection."""
    _mock_secret_store(monkeypatch)
    attacker = _AttackerEndpoint()
    token = _TokenEndpoint(redirect_to=attacker.url)
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=urllib.request.build_opener(),   # the mutant: follows redirects
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        _drive_callback(handle, state=q["state"])
        with pytest.raises(AssertionError, match="contacted"):
            assert attacker.connections == 0, "the redirect/attacker host was contacted (redirect followed)"
    finally:
        token.close()
        attacker.close()


# --------------------------------------------------------------------------------------------------
# AC-5: one-shot listener — deterministic teardown.
# --------------------------------------------------------------------------------------------------


def _assert_one_shot_torn_down(handle):
    """The listener served one request then tore down: the thread joined + the socket is closed."""
    handle.thread.join(2)
    assert not handle.thread.is_alive(), "the one-shot listener thread did not terminate"
    assert handle.server.socket.fileno() == -1, "the listening socket was not closed"


def test_ac5_one_shot_tears_down_after_one_request(monkeypatch):
    """After accepting exactly one request (even a rejected one) the listener tears down deterministically."""
    _mock_secret_store(monkeypatch)
    token = _TokenEndpoint()
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []), browser_open=lambda url: None,
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        _drive_callback(handle, state="mismatch-still-consumes-the-one-shot")
        _assert_one_shot_torn_down(handle)
    finally:
        token.close()
        handle.close()


def test_ac5_falsifier_re_accept_stays_open(monkeypatch):
    """Falsifier: a listener that never marks itself served re-accepts → the teardown assertion REDs."""
    _mock_secret_store(monkeypatch)
    monkeypatch.setattr(oauth_callback._OneShotServer, "mark_served", lambda self: None)
    token = _TokenEndpoint()
    handle = oauth_callback.start_connect(
        "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
        opener=_RecordingOpener(oauth_pull._OPENER, []), browser_open=lambda url: None,
        authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
    )
    try:
        _drive_callback(handle, state="mismatch")
        with pytest.raises(AssertionError, match="did not terminate|not closed"):
            _assert_one_shot_torn_down(handle)
    finally:
        handle.close()     # sets the stop flag → the poll loop exits
        token.close()


# --------------------------------------------------------------------------------------------------
# AC-6: the D7 crown-jewel wire-scan (D2 gold standard, captured at opener.open(request)).
# --------------------------------------------------------------------------------------------------


def _serialize_outbound(records, authorize_url):
    """The FULL outbound serialization: every recorded exchange request + the authorize URL leg."""
    return json.dumps({"exchange": records, "authorize": authorize_url}, default=str)


def _run_clean_flow(monkeypatch, *, opener_wrap=None, redirect_to=None):
    """Drive whoop auth→callback→exchange; return (records, authorize_url, store, store_spy, model_spy)."""
    store = _mock_secret_store(monkeypatch, {"plan::sentinel": STORE_SENTINEL})
    store_spy = _install_store_read_spy(monkeypatch)
    model_spy = _install_model_lane_spy(monkeypatch)
    token = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT-scan"},
                           redirect_to=redirect_to)
    token_netloc = token.netloc
    records = []
    recording = _RecordingOpener(oauth_pull._OPENER, records)
    opener = opener_wrap(recording) if opener_wrap else recording
    browser = []
    try:
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=opener, browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token.url,
        )
        q = _authorize_query(browser[0])
        if redirect_to is None:
            token.expected_challenge = q["code_challenge"]
        _drive_callback(handle, state=q["state"])
    finally:
        token.close()
    return records, browser[0], store, store_spy, model_spy, token_netloc


def _assert_clean_d7(records, authorize_url, store_spy, model_spy, *, vendor_netlocs, attacker=None):
    """The D7 sub-assertions: 0 store bytes / 0 store reads / 0 model calls / vendor-only host."""
    serialized = _serialize_outbound(records, authorize_url)
    assert STORE_SENTINEL not in serialized, "store content crossed to an outbound OAuth request"
    assert store_spy["n"] == 0, "the callback path performed a store read"
    assert model_spy["n"] == 0, "the callback path opened a no-train model-lane call"
    for rec in records:
        assert urlsplit(rec["full_url"]).netloc in vendor_netlocs, "an outbound request left the vendor host"
    assert urlsplit(authorize_url).netloc in vendor_netlocs, "the authorize URL left the vendor host"
    if attacker is not None:
        assert attacker.connections == 0, "an attacker host was contacted"


def test_ac6_d7_clean_direction(monkeypatch):
    """auth→callback→exchange crosses 0 store bytes / 0 store reads / 0 model calls / vendor-only host."""
    records, authorize_url, store, store_spy, model_spy, token_netloc = _run_clean_flow(monkeypatch)
    vendor = {token_netloc, urlsplit("http://127.0.0.1:1/authorize").netloc}
    _assert_clean_d7(records, authorize_url, store_spy, model_spy, vendor_netlocs=vendor)
    assert store == {"plan::sentinel": STORE_SENTINEL,                     # the seed is untouched
                     "a-plus-maxing-whoop-oauth": json.dumps(
                         {"refresh_token": "RT-scan", "client_id": _WHOOP_CID,
                          "client_secret": _CLIENT_SECRET})}
    assert records, "the exchange leg was never captured at opener.open"


def test_ac6_structural_no_scripts_store_import():
    """oauth_callback imports no `scripts.store` symbol (the primary 0-store-read guarantee; AST)."""
    source = (REPO_ROOT / "scripts" / "serve" / "oauth_callback.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    package_parts = ["scripts", "serve"]
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                imported.append(node.module or "")
            else:
                anchor = package_parts[: max(0, len(package_parts) - (node.level - 1))]
                if node.module:
                    imported.append(".".join(anchor + [node.module]))
                else:
                    imported += [".".join(anchor + [a.name]) for a in node.names]
    store_imports = [m for m in imported if m == "scripts.store" or m.startswith("scripts.store.")]
    assert store_imports == [], f"oauth_callback must import no scripts.store symbol: {store_imports}"


def test_ac6_mutant_store_content_append_reds(monkeypatch):
    """Mutant (a-content): an opener appending a store byte to the request → the 0-store-content REDs."""
    def _wrap(inner):
        return _MutantOpener(inner, lambda req: setattr(
            req, "data", (req.data or b"") + STORE_SENTINEL.encode()))

    records, authorize_url, _s, store_spy, model_spy, token_netloc = _run_clean_flow(
        monkeypatch, opener_wrap=_wrap)
    vendor = {token_netloc, urlsplit("http://127.0.0.1:1/authorize").netloc}
    with pytest.raises(AssertionError, match="store content crossed"):
        _assert_clean_d7(records, authorize_url, store_spy, model_spy, vendor_netlocs=vendor)


def test_ac6_mutant_store_read_reds(monkeypatch):
    """Mutant (b-read): an opener opening a store.read on the callback path → the 0-store-read spy REDs."""
    import scripts.store.store as store_mod

    def _wrap(inner):
        return _MutantOpener(inner, lambda req: store_mod.read("plan::x", root="/nonexistent"))

    records, authorize_url, _s, store_spy, model_spy, token_netloc = _run_clean_flow(
        monkeypatch, opener_wrap=_wrap)
    vendor = {token_netloc, urlsplit("http://127.0.0.1:1/authorize").netloc}
    with pytest.raises(AssertionError, match="store read"):
        _assert_clean_d7(records, authorize_url, store_spy, model_spy, vendor_netlocs=vendor)


def test_ac6_mutant_vendor_host_reds(monkeypatch):
    """Mutant (c-host): a 302-to-attacker + a following opener → the vendor-only-host assertion REDs."""
    attacker = _AttackerEndpoint()

    def _wrap(inner):
        return urllib.request.build_opener()   # follows redirects — replaces the no-follow opener

    try:
        records, authorize_url, _s, store_spy, model_spy, token_netloc = _run_clean_flow(
            monkeypatch, opener_wrap=_wrap, redirect_to=attacker.url)
        vendor = {token_netloc, urlsplit("http://127.0.0.1:1/authorize").netloc}
        with pytest.raises(AssertionError, match="attacker host was contacted"):
            _assert_clean_d7(records, authorize_url, store_spy, model_spy,
                             vendor_netlocs=vendor, attacker=attacker)
    finally:
        attacker.close()


def test_ac6_mutant_model_lane_reds(monkeypatch):
    """Mutant (d-model): an opener opening a no-train model-lane call → the 0-model-lane assertion REDs."""
    import scripts.model.client as client

    def _wrap(inner):
        return _MutantOpener(inner, lambda req: client._ClaudeNoTrainBackend())

    records, authorize_url, _s, store_spy, model_spy, token_netloc = _run_clean_flow(
        monkeypatch, opener_wrap=_wrap)
    vendor = {token_netloc, urlsplit("http://127.0.0.1:1/authorize").netloc}
    with pytest.raises(AssertionError, match="model-lane"):
        _assert_clean_d7(records, authorize_url, store_spy, model_spy, vendor_netlocs=vendor)


# --------------------------------------------------------------------------------------------------
# AC-8: no secret echo on any path (stderr + the browser response).
# --------------------------------------------------------------------------------------------------


def _assert_no_secret_echo(surfaces, sentinels):
    """No secret sentinel appears on any captured surface (the browser response / stderr)."""
    for surface in surfaces:
        for sentinel in sentinels:
            assert sentinel not in surface, f"a secret sentinel leaked onto a surface: {sentinel!r}"


def _closed_loopback_endpoint():
    """A loopback URL whose port is bound-then-closed → a connection there is refused (a transport error)."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return f"http://127.0.0.1:{port}/token"


def test_ac8_no_secret_echo_on_any_path(monkeypatch, capfd):
    """Success + EVERY error path echoes NONE of code / code_verifier / client_secret, and writes 0
    stderr bytes (AC-8). The six paths: success, non-2xx, no-refresh-token, the 3xx-redirect abort, a
    transport error (unreachable token endpoint), and a KeyStoreError write-fail. Regression guard —
    no production echo exists today; the echo-mutant meta-assertion proves the scan is RED-capable."""
    import scripts.secret_store as secret_store

    # Pin the minted PKCE verifier to a known sentinel so it is scannable on every surface (the
    # verifier is otherwise random). code + client_secret are always in scope for the connect flow.
    monkeypatch.setattr(oauth_callback, "_pkce_pair",
                        lambda: (_VERIFIER_SENTINEL, _s256(_VERIFIER_SENTINEL)))
    sentinels = [_CODE_SENTINEL, _VERIFIER_SENTINEL, _CLIENT_SECRET]

    surfaces = []

    def _drive(token_endpoint, *, set_secret_raises=False):
        _mock_secret_store(monkeypatch)
        if set_secret_raises:
            def _boom(service, value):
                raise secret_store.KeyStoreError("write failed")
            monkeypatch.setattr(secret_store, "set_secret", _boom)
        browser = []
        handle = oauth_callback.start_connect(
            "whoop", config=_config(whoop=(_WHOOP_CID, _CLIENT_SECRET)),
            opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token_endpoint)
        q = _authorize_query(browser[0])
        surfaces.append(_drive_callback(handle, state=q["state"], code=_CODE_SENTINEL))

    success = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT"})
    non_2xx = _TokenEndpoint(status=400, response={"error": "bad"})
    no_refresh = _TokenEndpoint(status=200, response={"no": "refresh"})
    attacker = _AttackerEndpoint()
    redirect = _TokenEndpoint(redirect_to=attacker.url)
    write_fail = _TokenEndpoint(response={"access_token": "AT", "refresh_token": "RT"})
    closers = [success, non_2xx, no_refresh, attacker, redirect, write_fail]
    try:
        _drive(success.url)                             # 1 success
        _drive(non_2xx.url)                             # 2 non-2xx token response
        _drive(no_refresh.url)                          # 3 2xx with no refresh_token
        _drive(redirect.url)                            # 4 the 3xx-redirect abort
        _drive(_closed_loopback_endpoint())             # 5 transport error (unreachable endpoint)
        _drive(write_fail.url, set_secret_raises=True)  # 6 KeyStoreError write-fail
    finally:
        for c in closers:
            c.close()

    out, err = capfd.readouterr()
    surfaces.append(err)
    assert err == "", f"the connect flow wrote to stderr: {err!r}"   # 0 stderr bytes on every path
    _assert_no_secret_echo(surfaces, sentinels)


def test_ac8_falsifier_echo_reds():
    """Falsifier: a surface echoing the secret → the no-echo scan REDs (the assert is RED-capable)."""
    with pytest.raises(AssertionError, match="leaked onto a surface"):
        _assert_no_secret_echo([f"error: {_CLIENT_SECRET}"], [_CLIENT_SECRET])


# --------------------------------------------------------------------------------------------------
# Shared write helper (contract §A) + servability (contract §B).
# --------------------------------------------------------------------------------------------------


def test_store_helper_writes_through_secret_store(monkeypatch):
    """`store_oauth_credential` validates source membership + writes the EXACT reader item."""
    store = _mock_secret_store(monkeypatch)
    oauth_callback.store_oauth_credential("whoop", "  RT-value  ")
    assert store == {"a-plus-maxing-whoop-oauth": "RT-value"}, "the value is stripped + at the exact item"


def test_store_helper_rejects_unknown_source_and_empty(monkeypatch):
    """The helper raises UnknownSourceError (unwired source) + EmptyCredentialError (blank), 0 writes."""
    store = _mock_secret_store(monkeypatch)
    with pytest.raises(oauth_callback.UnknownSourceError):
        oauth_callback.store_oauth_credential("fitbit", "RT")
    with pytest.raises(oauth_callback.EmptyCredentialError):
        oauth_callback.store_oauth_credential("whoop", "   ")
    assert store == {}


def test_servable_vendor_maps_and_gates():
    """servable_vendor maps source→vendor + gates by client type / config presence (AR-003/004/006)."""
    config = _config(whoop=(_WHOOP_CID, _CLIENT_SECRET), google=(_GOOGLE_CID, None))
    assert oauth_callback.servable_vendor("whoop", config) == "whoop"          # CONFIDENTIAL
    assert oauth_callback.servable_vendor("google-health", config) == "google"  # PKCE_PUBLIC + key-map
    assert oauth_callback.servable_vendor("oura", config) is None              # PAT
    assert oauth_callback.servable_vendor("garmin", config) is None            # EXCLUDED
    assert oauth_callback.servable_vendor("fitbit", config) is None            # unmapped
    # AR-006: a servable client type but NO client_id in the config → not servable
    empty = AlphaConfig(vendors={}, shared_api_key=None, client_types=dict(DEFAULT_CLIENT_TYPES))
    assert oauth_callback.servable_vendor("whoop", empty) is None
    # Arch F2: a servable client type + a client_id but NO authorize endpoint (oura marked
    # CONFIDENTIAL) → not servable, so "servable" fully implies "startable" (no start_connect KeyError).
    oura_conf = AlphaConfig(
        vendors={"oura": VendorCredential("oura-cid", "oura-secret")}, shared_api_key=None,
        client_types={**DEFAULT_CLIENT_TYPES, "oura": ClientType.CONFIDENTIAL})
    assert oauth_callback.servable_vendor("oura", oura_conf) is None
    assert "oura" not in oauth_callback._AUTHORIZE_ENDPOINTS   # the precondition that makes it endpoint-less


# --------------------------------------------------------------------------------------------------
# AC-7: the connect-start route (POST /settings/connect) — a new attacker-facing state-changing POST.
# --------------------------------------------------------------------------------------------------


def _serve_in_thread(srv):
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _request(port, method, path, body=None, *, content_type="application/json"):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    headers = {}
    if content_type is not None:
        headers["Content-Type"] = content_type
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


class _RecordingStart:
    """A `connect_start` seam that records calls WITHOUT binding a listener or opening a browser."""

    def __init__(self):
        self.calls = []

    def __call__(self, source, *, config):
        self.calls.append(source)


def _real_start_capturing(browser, handles, token_endpoint="http://127.0.0.1:1/token"):
    """A `connect_start` seam wrapping the REAL start_connect: captures the authorize URL + the handle."""
    def _start(source, *, config):
        handle = oauth_callback.start_connect(
            source, config=config, opener=_RecordingOpener(oauth_pull._OPENER, []),
            browser_open=lambda url: browser.append(url),
            authorize_endpoint="http://127.0.0.1:1/authorize", token_endpoint=token_endpoint)
        handles.append(handle)
        return handle
    return _start


def test_ac7a_non_json_content_type_is_415_before_any_side_effect(monkeypatch):
    """A text/plain AND a no-Content-Type POST to /settings/connect → 415 BEFORE any listener/browser."""
    from scripts.serve import server as serve_server

    recorder = _RecordingStart()
    config = _config(whoop=(_WHOOP_CID, _CLIENT_SECRET))
    srv = serve_server.build_server(0, alpha_config=config, connect_start=recorder)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for ctype in ("text/plain", None):
            status, _ = _request(port, "POST", "/settings/connect",
                                 json.dumps({"source": "whoop"}), content_type=ctype)
            assert status == 415, f"content_type={ctype!r} returned {status}, expected 415"
        assert recorder.calls == [], "start_connect ran despite the 415 gate (a listener/browser fired)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_ac7a_falsifier_side_effect_before_gate_reds():
    """Falsifier: a 415 gate placed AFTER the listener spin-up → start_connect runs → the negative
    no-side-effect assertion REDs (the assertion binds to whether start_connect was reached)."""
    recorder = _RecordingStart()
    recorder("whoop", config=None)   # simulate a gate-after-side-effect mutant reaching start_connect
    with pytest.raises(AssertionError, match="start_connect ran"):
        assert recorder.calls == [], "start_connect ran despite the 415 gate (a listener/browser fired)"


def test_ac7b_non_servable_sources_are_400_without_side_effect(monkeypatch):
    """Each non-servable source → 400, start_connect never called (no listener/browser side effect)."""
    from scripts.serve import server as serve_server

    recorder = _RecordingStart()
    # a config with whoop + google present, so the rejection is by CLIENT TYPE / mapping, not absence
    config = _config(whoop=(_WHOOP_CID, _CLIENT_SECRET), google=(_GOOGLE_CID, None))
    srv = serve_server.build_server(0, alpha_config=config, connect_start=recorder)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for bad in ("garmin", "oura", "fitbit"):     # EXCLUDED / PAT / unmapped(MANUAL)
            status, text = _request(port, "POST", "/settings/connect", json.dumps({"source": bad}))
            assert status == 400, f"source={bad!r} returned {status}, expected 400"
            assert json.loads(text)["ok"] is False
        assert recorder.calls == [], "start_connect ran for a non-servable source"
    finally:
        srv.shutdown()
        srv.server_close()


def test_ac7b_empty_config_missing_client_id_is_400(monkeypatch):
    """AR-006: a servable client type but an empty config (no client_id) → 400, no side effect."""
    from scripts.serve import server as serve_server

    recorder = _RecordingStart()
    empty = AlphaConfig(vendors={}, shared_api_key=None, client_types=dict(DEFAULT_CLIENT_TYPES))
    srv = serve_server.build_server(0, alpha_config=empty, connect_start=recorder)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/connect", json.dumps({"source": "whoop"}))
        assert status == 400
        assert json.loads(text)["ok"] is False
        assert recorder.calls == []
    finally:
        srv.shutdown()
        srv.server_close()


def test_ac7b_endpoint_less_servable_vendor_is_400(monkeypatch):
    """Arch F2: a config marking an endpoint-less mapped vendor (oura) CONFIDENTIAL + a client_id → a
    clean 400, no side effect — the `servable_vendor` authorize-endpoint gate makes "servable" imply
    "startable", so `start_connect` never raises `_AUTHORIZE_ENDPOINTS[vendor]` KeyError → 500."""
    from scripts.serve import server as serve_server

    recorder = _RecordingStart()
    oura_conf = AlphaConfig(
        vendors={"oura": VendorCredential("oura-cid", "oura-secret")}, shared_api_key=None,
        client_types={**DEFAULT_CLIENT_TYPES, "oura": ClientType.CONFIDENTIAL})
    srv = serve_server.build_server(0, alpha_config=oura_conf, connect_start=recorder)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/connect", json.dumps({"source": "oura"}))
        assert status == 400, f"an endpoint-less servable vendor returned {status}, expected a clean 400"
        assert json.loads(text)["ok"] is False
        assert recorder.calls == []
    finally:
        srv.shutdown()
        srv.server_close()


@pytest.mark.parametrize("source,vendor,client_id,has_secret", [
    ("whoop", "whoop", _WHOOP_CID, True),               # CONFIDENTIAL
    ("google-health", "google", _GOOGLE_CID, False),    # PKCE_PUBLIC — exercises the source→vendor map
])
def test_ac7c_happy_path_binds_listener_and_opens_authorize_url(
        monkeypatch, source, vendor, client_id, has_secret):
    """Each servable vendor → 200, a loopback listener bound, the authorize URL carries the mapped
    client_id + challenge + state (the google-health case REDs if the source→vendor map is dropped)."""
    from scripts.serve import server as serve_server

    browser, handles = [], []
    config = _config(whoop=(_WHOOP_CID, _CLIENT_SECRET), google=(_GOOGLE_CID, None))
    srv = serve_server.build_server(0, alpha_config=config,
                                    connect_start=_real_start_capturing(browser, handles))
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/connect", json.dumps({"source": source}))
        assert status == 200, f"servable source {source!r} returned {status}, expected 200"
        assert json.loads(text)["ok"] is True
        assert len(browser) == 1, "the authorize URL was not opened"
        q = _authorize_query(browser[0])
        assert q["client_id"] == client_id, "the authorize URL carried the wrong mapped-vendor client_id"
        assert q["code_challenge"] and q["code_challenge_method"] == "S256"
        assert q["state"]
        assert q["redirect_uri"].startswith("http://127.0.0.1:")
        # a loopback listener was really bound
        assert handles and handles[0].address[0] == "127.0.0.1"
    finally:
        for handle in handles:
            handle.close()
        srv.shutdown()
        srv.server_close()
