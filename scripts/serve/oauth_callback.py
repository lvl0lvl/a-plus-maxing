"""App-mediated OAuth-2.0 authorization-code flow with a one-shot `127.0.0.1` PKCE callback (ADR-0048-T2).

`start_connect(source, config=...)` mints a PKCE verifier/challenge + a `state` CSRF nonce, binds a
one-shot loopback listener on an ephemeral port, and opens the vendor's authorize URL. When the vendor
redirects the browser back to the listener, the callback validates `state`, exchanges the `code` for a
short-lived token set, and writes the OAuth **refresh_token** — in the per-CLIENT-TYPE shape
`scripts.ingest.oauth_pull._parse_credentials` consumes — through the ONE extracted
`store_oauth_credential` helper into the SAME `a-plus-maxing-<source>-oauth` keychain item the reader
reads. A confidential vendor (Whoop) stores the `{refresh_token, client_id, client_secret}` blob the
refresh grant forwards; a PKCE-public vendor (Google) stores the bare refresh token.

Egress boundary (ADR-0001 / ADR-0048 D7): the serve layer is egress-free BY CONSTRUCTION (the
`test_serve_no_egress` guard family bans every outbound HTTP client under `scripts/serve/`), so the one
outbound leg — the code→token exchange — is DELEGATED to `oauth_pull.exchange_authorization_code` in
the egress-permitted ingest layer (behind the same host-locked no-follow opener), and this module
imports NO outbound client. The authorize URL is a serve-side URL builder (no outbound call). This is
an INBOUND connect — the operator authorizes access to their own wearable cloud; the only outbound
hosts are the vendor's own authorize + token endpoints. The module imports no `scripts.store` symbol
and opens no no-train model lane, so the connect path structurally cannot touch the store or the model
(the D7 wire-scan in tests/serve/test_oauth_callback.py mechanizes that guarantee — captured at the
ingest-layer exchange opener, the OAuth sibling of the ADR-0049-T1 D2 scan).

Fail-closed everywhere (the repo is PUBLIC, NFR-3): a state mismatch, a non-2xx or redirecting token
endpoint, a network error, or a keychain-write failure writes 0 credentials and echoes NONE of the
auth `code`, `code_verifier`, or `client_secret` on any surface (the browser response or stderr). All
secrets live only in memory for the one-shot match — never persisted, never logged.
"""

import base64
import hashlib
import http.server
import json
import secrets
import threading
import urllib.parse
import webbrowser

from scripts.serve.alpha_config import ClientType

# The single loopback-bind site (mirrors server.py `_LOOPBACK`): the callback listener is
# off-machine-unreachable by construction, never `0.0.0.0`/a routable interface.
_LOOPBACK = "127.0.0.1"

# The one-shot listener's accept-poll granularity: `handle_request` returns after this many seconds
# with no request so the run-loop can observe a teardown request (a stop flag) between polls.
_ACCEPT_POLL_S = 0.25

# The source key space (`oauth_pull._MANIFESTS`) and the alpha_config VENDOR key space differ only on
# Google (source `google-health` ↔ vendor `google`); write in the SOURCE key, look up the client
# type / client_id in the mapped VENDOR key (AR-003).
_SOURCE_TO_VENDOR = {
    "whoop": "whoop",
    "oura": "oura",
    "garmin": "garmin",
    "google-health": "google",
}

# Only an OAuth-2.0-authorization-code client is one-click-servable (AR-004): a confidential client
# (shared secret) or a PKCE-public client. PAT (oura) + EXCLUDED_FROM_ONE_CLICK (garmin OAuth-1.0a) +
# an unmapped MANUAL vendor are rejected at the connect-start route.
_SERVABLE_CLIENT_TYPES = frozenset({ClientType.CONFIDENTIAL, ClientType.PKCE_PUBLIC})

# [VERIFY-AT-BUILD] the per-vendor OAuth-2.0 AUTHORIZE endpoints, keyed by the alpha_config vendor
# name. oauth_pull's manifests carry each vendor's TOKEN url (reused for the exchange); the authorize
# url has no home there, so the one-click connect flow carries it. Transcribed from each vendor's
# OAuth docs and re-verified at the LIVE dev-app registration (bead a-plus-maxing-m8ia) — only the
# servable vendors need one.
_AUTHORIZE_ENDPOINTS = {
    "whoop": "https://api.prod.whoop.com/oauth/oauth2/auth",
    "google": "https://accounts.google.com/o/oauth2/v2/auth",
}

# The constant browser-facing message on EVERY callback path (success + error) — echoes no secret.
_BROWSER_MESSAGE = (
    "<!doctype html><title>a+maxing</title>"
    "<p>You can close this tab and return to a+maxing.</p>"
)


class OAuthWriteError(RuntimeError):
    """A connect credential write was rejected before it reached the secret store."""


class UnknownSourceError(OAuthWriteError):
    """The write source is not a wired OAuth-pull source (fail-closed; maps to a 400)."""


class EmptyCredentialError(OAuthWriteError):
    """The credential value is empty/whitespace-only after strip (fail-closed; maps to a 400)."""


def store_oauth_credential(source, value):
    """Write the per-source OAuth credential through `secret_store` — the ONE validated writer.

    The shared write path `_save_tracker_token` and the authorization-code callback both call:
    exact-membership source validation (against the wired manifest set, read at call time so a
    monkeypatched set is honored) -> strip / empty-reject -> `secret_store.set_secret` into the
    `_oauth_service_name(source)` item the reader reads. A single validated writer closes the
    service-name-injection surface (an unvalidated source could write an arbitrary keyring item).

    Args:
        source (str): The wired OAuth-pull source (`whoop`, `google-health`, ...).
        value (str): The credential to store (a bare refresh token or a JSON credential blob).

    Raises:
        UnknownSourceError: `source` is not in the wired manifest set.
        EmptyCredentialError: `value` is empty or whitespace-only.
        secret_store.KeyStoreError: The keychain write failed (or could not clear stale residue —
            so a failure must NOT be read as "unstored" with certainty).
    """
    from scripts import secret_store
    from scripts.ingest import oauth_pull

    if source not in oauth_pull._MANIFESTS:
        raise UnknownSourceError(source)
    value = value.strip()
    if not value:
        raise EmptyCredentialError(source)
    secret_store.set_secret(oauth_pull._oauth_service_name(source), value)


def servable_vendor(source, config):
    """Return the mapped vendor if `source` is authorization-code-servable under `config`, else None.

    Servable iff the source maps to a vendor whose `config.client_type` is CONFIDENTIAL or
    PKCE_PUBLIC (AR-004) AND the config carries that vendor's `client_id` (AR-006: an empty/partial
    config degrades to non-servable rather than emitting an authorize URL with a None client_id).

    Args:
        source (str): The OAuth-pull source key.
        config (AlphaConfig): The loaded alpha config (the canonical client-type + client_id record).

    Returns:
        (str | None) The mapped vendor name when servable, else None.
    """
    vendor = _SOURCE_TO_VENDOR.get(source)
    if vendor is None:
        return None
    if config.client_type(vendor) not in _SERVABLE_CLIENT_TYPES:
        return None
    cred = config.vendors.get(vendor)
    if cred is None or not cred.client_id:
        return None
    return vendor


def _pkce_pair():
    """Mint an RFC-7636 (`code_verifier`, S256 `code_challenge`) pair from a CSPRNG.

    `secrets.token_urlsafe(48)` yields ~64 url-safe chars (>= the 43-char verifier floor); the
    challenge is base64url(SHA256(verifier)) with padding stripped (the S256 method).
    """
    verifier = secrets.token_urlsafe(48)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def _build_authorize_url(endpoint, *, client_id, redirect_uri, state, challenge, scope):
    """Build the vendor authorize URL carrying the PKCE challenge + state + the loopback redirect_uri."""
    query = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if scope:
        query["scope"] = scope
    return endpoint + "?" + urllib.parse.urlencode(query)


def _credential_value(client_type, refresh_token, client_id, client_secret):
    """The per-CLIENT-TYPE stored shape the reader consumes (contract §B).

    CONFIDENTIAL stores the `{refresh_token, client_id, client_secret}` blob the refresh grant
    forwards; PKCE_PUBLIC stores the bare refresh token (a public client refreshes without a secret).
    """
    if client_type is ClientType.CONFIDENTIAL:
        return json.dumps({"refresh_token": refresh_token, "client_id": client_id,
                           "client_secret": client_secret})
    return refresh_token


def _complete_callback(flow, code):
    """Run the exchange (delegated to the egress-permitted ingest layer) and write the refresh token.

    The outbound token POST lives in `oauth_pull.exchange_authorization_code` (the serve layer is
    egress-free — ADR-0048 D7); this serve-side handler validates the callback, drives that exchange,
    and writes the per-client-type refresh token through the shared helper. Fail-closed throughout.
    """
    from scripts.ingest import oauth_pull

    token = oauth_pull.exchange_authorization_code(
        flow["source"], code, flow["verifier"], flow["redirect_uri"],
        client_id=flow["client_id"], client_secret=flow["client_secret"],
        token_endpoint=flow["token_endpoint"], opener=flow["opener"])
    if token is None:
        flow["outcome"] = "exchange-failed"
        return
    refresh = token.get("refresh_token")
    if not refresh:
        flow["outcome"] = "no-refresh-token"
        return
    value = _credential_value(flow["client_type"], refresh, flow["client_id"], flow["client_secret"])
    try:
        store_oauth_credential(flow["source"], value)
    except Exception:
        # Fail-closed (AC-8): a keychain write failure (KeyStoreError) or any late error records
        # nothing and echoes no secret — the browser sees the same constant message as every path.
        flow["outcome"] = "write-failed"
        return
    flow["outcome"] = "connected"


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handle the single vendor redirect: validate `state`, run the exchange, respond constantly."""

    def do_GET(self):
        flow = self.server.flow
        try:
            params = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
            state = (params.get("state") or [""])[0]
            code = (params.get("code") or [""])[0]
            if not code or state != flow["state"]:
                flow["outcome"] = "state-mismatch"      # the exchange never runs -> 0 writes
            else:
                _complete_callback(flow, code)
        except Exception:
            flow["outcome"] = "error"
        finally:
            self._respond_constant()
            self.server.mark_served()                   # consume the one-shot (any first request)

    def _respond_constant(self):
        """Write the constant browser message — echoes no `code`/`code_verifier`/`client_secret`."""
        body = _BROWSER_MESSAGE.encode("utf-8")
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except OSError:
            pass

    def log_message(self, *args):
        """Silence the default per-request stderr access log (it would echo the callback query)."""


class _OneShotServer(http.server.HTTPServer):
    """A loopback HTTP server that serves EXACTLY one request then tears down (SEC LOW-1 one-shot).

    A polling run-loop (`_run_one_shot`) calls `handle_request` — bounded by `timeout` so it can
    observe a teardown request between polls — until the handler `mark_served`s (the first request,
    accepted OR rejected, consumes the one-shot: a smaller window) or a `close()` sets the stop flag.
    """

    timeout = _ACCEPT_POLL_S

    def __init__(self, address, handler_cls, flow):
        super().__init__(address, handler_cls)
        self.flow = flow
        self._served = threading.Event()
        self._stop = threading.Event()

    def mark_served(self):
        self._served.set()


class _ConnectHandle:
    """A handle to the running one-shot connect flow: its bound address, server, and listener thread."""

    def __init__(self, server, thread):
        self.server = server
        self.thread = thread
        self.address = server.socket.getsockname()   # captured before teardown closes the socket

    def close(self, timeout=5.0):
        """Stop the listener (for a flow that never received its callback) and join the thread."""
        self.server._stop.set()
        self.thread.join(timeout)


def _run_one_shot(server):
    """Serve one request then tear down: poll `handle_request` until served or stopped, then close."""
    try:
        while not server._served.is_set() and not server._stop.is_set():
            server.handle_request()
    finally:
        server.server_close()


def start_connect(source, *, config, opener=None, browser_open=None,
                  authorize_endpoint=None, token_endpoint=None):
    """Bind the one-shot loopback callback listener and open the vendor authorize URL.

    Mints the PKCE verifier/challenge + the `state` nonce, binds a `127.0.0.1` listener on an
    ephemeral port, builds the authorize URL (client_id from `config`, the loopback redirect_uri, the
    S256 challenge, the state, the source's scope), starts the one-shot listener thread, and opens the
    browser. Returns immediately with a handle; the exchange + credential write happen on the listener
    thread when the vendor redirects back. Assumes `source` is servable (the connect-start route gates
    it via `servable_vendor`).

    Args:
        source (str): A servable OAuth-pull source (`whoop` / `google-health`).
        config (AlphaConfig): The client-type + client_id record.
        opener (optional): Forwarded to `oauth_pull.exchange_authorization_code`; None uses the ingest
            layer's fail-closed no-follow `_OPENER`. Injected in tests to capture the exchange at the wire.
        browser_open (Callable, optional): `url -> None` browser opener; defaults to `webbrowser.open`.
        authorize_endpoint (str, optional): The vendor authorize URL; defaults to the per-vendor map.
        token_endpoint (str, optional): The vendor token URL; defaults to the source's manifest.

    Returns:
        (_ConnectHandle) The running flow's handle (bound address + server + thread).
    """
    from scripts.ingest import oauth_pull

    vendor = _SOURCE_TO_VENDOR[source]
    client_type = config.client_type(vendor)
    cred = config.vendors[vendor]
    browser_open = webbrowser.open if browser_open is None else browser_open
    if authorize_endpoint is None:
        authorize_endpoint = _AUTHORIZE_ENDPOINTS[vendor]
    if token_endpoint is None:
        token_endpoint = oauth_pull._MANIFESTS[source]["token_url"]
    scope = oauth_pull._MANIFESTS.get(source, {}).get("scope", "")

    verifier, challenge = _pkce_pair()
    state = secrets.token_urlsafe(32)

    flow = {
        "source": source, "vendor": vendor, "client_type": client_type,
        "client_id": cred.client_id, "client_secret": cred.client_secret,
        "verifier": verifier, "state": state, "opener": opener,
        "token_endpoint": token_endpoint, "outcome": None,
    }
    server = _OneShotServer((_LOOPBACK, 0), _CallbackHandler, flow)
    port = server.socket.getsockname()[1]
    redirect_uri = f"http://{_LOOPBACK}:{port}/"
    flow["redirect_uri"] = redirect_uri

    url = _build_authorize_url(authorize_endpoint, client_id=cred.client_id,
                               redirect_uri=redirect_uri, state=state, challenge=challenge, scope=scope)

    thread = threading.Thread(target=_run_one_shot, args=(server,), daemon=True)
    thread.start()
    browser_open(url)
    return _ConnectHandle(server, thread)
