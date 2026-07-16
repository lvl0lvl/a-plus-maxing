"""Route tests for GET /settings/trackers + POST /settings/tracker — per-source OAuth token writes.

The N-per-source companion to `/settings/key` (ADR-0048-T3): a loopback POST writes a per-source
tracker OAuth token through `scripts.secret_store` into the SAME `a-plus-maxing-<source>-oauth`
item `scripts.ingest.oauth_pull`'s default reader reads, and a GET reports per-source connected
booleans only — never a token value. The new secret-write surface carries `_save_key`'s ADR-0013
posture: the `application/json` CSRF gate (415 BEFORE any write), the 16-KiB body ceiling (413),
and the BUG-001 shape guards — plus a fail-closed source-validation gate `_save_key` has no
concept of.

Crown-jewel constraint (NFR-3, the repo is PUBLIC): the token never appears in any response body.
`secret_store` is dict-mocked over a shared service->value dict (the T3 $0-mock form from
`tests/ingest/test_oauth_pull.py`) so no real keyring / network / token is touched, with a
SYNTHETIC token fixture deliberately not shaped like a real OAuth token.
"""

import http.client
import json
import re
import subprocess
import threading
from pathlib import Path

from scripts.serve import server as serve_server

REPO_ROOT = Path(__file__).resolve().parents[2]

# A non-secret fixture deliberately NOT shaped like a real OAuth token and short enough that the
# AC-4 value-shape scan below cannot self-match this file's own definition line (the
# `test_settings_key.py` non-self-matching precedent).
_SYNTHETIC_TOKEN = "synthetic-oauth-token"


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

    Drives the reject branches the json `_request` helper cannot reach: a non-`application/json`
    Content-Type (CSRF), a non-numeric Content-Length, and an over-ceiling declared length
    (`content_length` overrides the true byte length). Mirrors `test_settings_key.py::_raw_post`.
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


def _mock_secret_store(monkeypatch, initial=None):
    """Monkeypatch secret_store.get_secret/set_secret over a shared service->value dict; return it.

    The T3 $0-mock form: both the server's write (`secret_store.set_secret`) and the Wave-2 reader
    (`oauth_pull._read_oauth_credential` -> `secret_store.get_secret`) resolve the SAME patched
    functions over one dict (they share the `scripts.secret_store` module object), so a route write
    and the reader's read hit the same service item end to end. No real keyring is touched.
    """
    import scripts.secret_store as secret_store

    store = dict(initial or {})
    monkeypatch.setattr(secret_store, "set_secret",
                        lambda service, value: store.__setitem__(service, value))
    monkeypatch.setattr(secret_store, "get_secret", lambda service: store.get(service))
    return store


# --- AC-1a: the per-source POST writes through secret_store into the EXACT service item -----------


def test_post_writes_token_to_exact_service_item(monkeypatch):
    """POST /settings/tracker writes the token into `a-plus-maxing-<source>-oauth` and echoes no value.

    The exact-service assert is load-bearing: a service-string transposition (or a transforming
    derivation) writes a DIFFERENT key and REDs. The response carries `{ok, connected}` only.
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 200
        assert json.loads(text) == {"ok": True, "connected": True}
        assert store == {"a-plus-maxing-whoop-oauth": _SYNTHETIC_TOKEN}  # exact service item
        assert _SYNTHETIC_TOKEN not in text  # the token never reaches the response body
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-1b: the status GET reports per-source connected booleans only -----------------------------


def test_status_reports_per_source_connected_booleans(monkeypatch):
    """GET /settings/trackers reports {sources: {<source>: bool}} over the wired set — never a value.

    The response's source-key set == the manifest key set (not just whoop), whoop flips false->true
    across a write, and no token value appears in the body.
    """
    from scripts.ingest import oauth_pull

    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/trackers")
        assert status == 200
        before = json.loads(text)
        assert set(before["sources"]) == set(oauth_pull._MANIFESTS)  # whole wired set, data-driven
        assert before["sources"]["whoop"] is False

        status, _ = _request(port, "POST", "/settings/tracker",
                             json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 200

        status, text = _request(port, "GET", "/settings/trackers")
        after = json.loads(text)
        assert after["sources"]["whoop"] is True
        assert after["sources"]["oura"] is False  # a different source stays disconnected
        assert _SYNTHETIC_TOKEN not in text  # the status surface carries booleans only
    finally:
        srv.shutdown()


def test_status_get_tolerates_a_query_string(monkeypatch):
    """GET /settings/trackers?v=2 is served (dispatch matches the query-stripped path — AR-009).

    A cache-busting query on the status poll must still route; RED if the GET dispatch matches
    raw `self.path` instead of the query-stripped `path` var the sibling /settings/key GET uses.
    """
    _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/trackers?v=2")
        assert status == 200
        assert "sources" in json.loads(text)
    finally:
        srv.shutdown()
        srv.server_close()


# --- SF-1: the wired set is request-time + data-driven; the service string is derived, not copied --


def test_wired_set_is_request_time_data_driven(monkeypatch):
    """A hyphenated synthetic source added to the manifest is reported + writable at the exact item.

    REDs BOTH a hand-copied wired set (the synthetic source would be rejected/absent) AND a
    transforming service-name derivation (a hyphen sanitized to `_` writes the wrong item). Requires
    the handler to read the wired set + derive the service name at REQUEST time (function-local
    import), which R2/R4 mandate.
    """
    from scripts.ingest import oauth_pull

    store = _mock_secret_store(monkeypatch)
    monkeypatch.setattr(oauth_pull, "_MANIFESTS",
                        {**oauth_pull._MANIFESTS, "synth-vendor": {"host": "synth.example", "endpoints": ()}})
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/trackers")
        assert status == 200
        assert "synth-vendor" in json.loads(text)["sources"]  # request-time set, not a hand-copied list

        status, _ = _request(port, "POST", "/settings/tracker",
                             json.dumps({"source": "synth-vendor", "token": _SYNTHETIC_TOKEN}))
        assert status == 200
        # The hyphen survives verbatim into the service item — a sanitizing derivation REDs here.
        assert store == {"a-plus-maxing-synth-vendor-oauth": _SYNTHETIC_TOKEN}
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-1b whitespace-status (AR-004): effective presence, not raw get_secret truthiness -----------


def test_status_whitespace_stored_value_reports_false(monkeypatch):
    """A whitespace-only stored value reports `false` — the reader's EFFECTIVE presence.

    RED-capable: a raw `get_secret(...)` truthiness presence would report the whitespace value as
    connected, while the pull (which strips) sees None. `_read_oauth_credential(...) is not None`
    matches what the pull will actually see.
    """
    store = _mock_secret_store(monkeypatch, {"a-plus-maxing-whoop-oauth": "   "})
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "GET", "/settings/trackers")
        assert status == 200
        assert json.loads(text)["sources"]["whoop"] is False
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-2: an over-ceiling body is refused 413 BEFORE any write -----------------------------------


def test_oversize_body_is_413_without_writing(monkeypatch):
    """A declared Content-Length over the 16-KiB ceiling is refused 413 before the body is read.

    The store dict is UNTOUCHED (the before-write half is the load-bearing assert) — the same
    16-KiB `_SETTINGS_MAX_BYTES` constant `_save_key` uses, no new constant.
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _raw_post(port, "/settings/tracker", b"x",
                              content_length=str(serve_server._SETTINGS_MAX_BYTES + 1))
        assert status == 413
        assert store == {}  # nothing reached the secret store
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-3: a token round-trips route-write -> oauth_pull's default reader, same store item ---------


def test_token_round_trips_through_oauth_reader(monkeypatch):
    """A token written via the route is recovered by `oauth_pull._read_oauth_credential` — same item.

    Both over the SAME mocked dict, proving the route and the Wave-2 reader share the service item
    end to end (the ADR-0047 store parity the whole feature rests on).
    """
    from scripts.ingest import oauth_pull

    _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _request(port, "POST", "/settings/tracker",
                             json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 200
        assert oauth_pull._read_oauth_credential("whoop") == _SYNTHETIC_TOKEN
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-4: no token-SHAPE literal in the tracked tree (hardened labeled/value-shape scan) ----------

# The house VALUE-shape form (mirrors test_alpha_config.py): a LABELED OAuth2 refresh/access-token
# value-shape, NOT a bare identifier nor a bare `{32,}` catch-all. Deliberately EXCLUDES the
# `oauth_token`/`consumer_secret`/`token_secret` labels the OAuth-1.0a known-answer signing vector
# legitimately carries — this route writes OAuth2 tokens (refresh/access), labeled or bare.
_TOKEN_VALUE_RE = re.compile(
    r"""(?:refresh_token|access_token)["']?\s*[:=]\s*["'][A-Za-z0-9._/+=-]{32,}["']""",
    re.IGNORECASE,
)


def test_no_tracked_token_shape(monkeypatch):
    """After a simulated write, a value-shape token scan over `git ls-files` finds 0 hits (PUBLIC repo).

    The write lands in the in-memory mock (never the tree); this scan is the tree backstop. Positive
    control pins the regex is live (a real-length labeled value matches); the deliberately
    non-self-matching short fixture must NOT match (else the scan hits its own definition and gets
    weakened at GREEN time). The THIS-token leak is covered by the response-surface negatives.
    """
    # Positive controls: the pattern MUST match a real-length labeled value and NOT the short fixture.
    assert _TOKEN_VALUE_RE.search('"refresh_token": "' + "A" * 40 + '"'), "the token value-scan is broken"
    assert not _TOKEN_VALUE_RE.search('token = "%s"' % _SYNTHETIC_TOKEN), "the scan matches a short fixture"

    _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        _request(port, "POST", "/settings/tracker",
                 json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
    finally:
        srv.shutdown()
        srv.server_close()

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hits = []
    for rel in tracked:
        if not rel:
            continue
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if _TOKEN_VALUE_RE.search(text):
            hits.append(rel)
    assert hits == [], f"a value-shape token is in the tracked tree (PUBLIC repo): {hits}"


# --- AC-5 (crown jewel): the application/json CSRF gate refuses a text/plain POST BEFORE any write --


def test_text_plain_post_is_415_before_any_write(monkeypatch):
    """A cross-site CORS-simple `text/plain` POST with a valid JSON body is refused 415 BEFORE a write.

    The untouched-dict negative assertion is what makes "415 before any keychain write" non-vacuous.
    RED-capability: mutate the gate out (accept any content-type) -> the text/plain write proceeds ->
    this REDs (proven by mutation at Tier-1).
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _raw_post(
            port, "/settings/tracker",
            json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}).encode("utf-8"),
            content_type="text/plain",
        )
        assert status == 415
        assert store == {}  # 0 writes — the gate fired before the body was read
        assert _SYNTHETIC_TOKEN not in text
    finally:
        srv.shutdown()
        srv.server_close()


def test_json_charset_content_type_is_accepted(monkeypatch):
    """`application/json; charset=utf-8` passes the CSRF gate (the exact ctype normalization).

    Pins that the gate normalizes the media-type (split `;`, strip, lower) rather than a naive `!=`
    that would false-415 a charset-parametrized header a real browser sends.
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _raw_post(
            port, "/settings/tracker",
            json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}).encode("utf-8"),
            content_type="application/json; charset=utf-8",
        )
        assert status == 200
        assert store == {"a-plus-maxing-whoop-oauth": _SYNTHETIC_TOKEN}
    finally:
        srv.shutdown()
        srv.server_close()


# --- error battery (each 400, dict untouched, RED-capable) ----------------------------------------


def test_non_object_json_body_is_400(monkeypatch):
    """A top-level non-object JSON body is 400 — never an uncaught AttributeError / dropped thread."""
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for bad in ("123", "[]", '"x"', "true", "null"):
            status, text = _request(port, "POST", "/settings/tracker", bad)
            assert status == 400, f"{bad!r} returned {status}, expected 400 (not a dropped connection)"
            assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_unhashable_source_is_400(monkeypatch):
    """A non-str (UNHASHABLE) `source` is 400 — the isinstance guard, not the membership gate (MF-1).

    `{"source": ["whoop"], ...}`: without the source isinstance guard, `["whoop"] in <set>` raises
    TypeError and drops the request thread. Falsifier: drop the source isinstance -> RED (thread drop).
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": ["whoop"], "token": "tok"}))
        assert status == 400  # a status came back at all -> the thread was not dropped
        assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_absent_source_or_token_is_400(monkeypatch):
    """An ABSENT `source` or `token` key is 400 via `.get` reads — never a KeyError-dropped thread.

    Falsifier (AR-003): subscript `body["source"]`/`body["token"]` instead of `.get` -> KeyError ->
    dropped thread -> RED. Each variant leaves the store untouched.
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for bad in ({"token": "x"}, {"source": "whoop"}):
            status, text = _request(port, "POST", "/settings/tracker", json.dumps(bad))
            assert status == 400, f"{bad!r} returned {status}, expected 400 (not a dropped connection)"
            assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_non_str_token_is_400(monkeypatch):
    """A non-str `token` is 400 (isinstance-guarded), store untouched."""
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "whoop", "token": 123}))
        assert status == 400
        assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_empty_or_blank_token_is_400(monkeypatch):
    """An empty / whitespace-only `token` is 400 (strip+empty-reject), store untouched."""
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for blank in ("", "   ", "\n"):
            status, text = _request(port, "POST", "/settings/tracker",
                                    json.dumps({"source": "whoop", "token": blank}))
            assert status == 400, f"token={blank!r} returned {status}, expected 400"
            assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_unwired_source_is_400(monkeypatch):
    """An unwired / traversal-shaped / case-variant `source` is 400 (EXACT membership, fail-closed).

    `"fitbit"` (unwired), `"../x"` (traversal-shaped), and `"Whoop"` (case-variant — no case-folding,
    sec LOW-1) each miss the wired set -> 400 with the store untouched. The token was in the parsed
    body yet nothing was written to the derived service item.
    """
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        for bad_source in ("fitbit", "../x", "Whoop"):
            status, text = _request(port, "POST", "/settings/tracker",
                                    json.dumps({"source": bad_source, "token": _SYNTHETIC_TOKEN}))
            assert status == 400, f"source={bad_source!r} returned {status}, expected 400"
            assert json.loads(text)["ok"] is False
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_non_numeric_content_length_is_400(monkeypatch):
    """A non-numeric Content-Length is 400, not a dropped connection (a DoS-shaped defect otherwise)."""
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, _ = _raw_post(port, "/settings/tracker", b"", content_length="not-a-number")
        assert status == 400
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_malformed_or_non_utf8_body_is_400(monkeypatch):
    """A malformed-JSON body and a non-UTF-8 body are each 400, store untouched (SF-4)."""
    store = _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/tracker", "{not json")
        assert status == 400
        assert json.loads(text)["ok"] is False

        status, _ = _raw_post(port, "/settings/tracker", b"\xff\xfe",
                              content_type="application/json")
        assert status == 400
        assert store == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_store_failure_returns_500(monkeypatch):
    """A `secret_store.KeyStoreError` on write is 500 with a constant message — never the token."""
    import scripts.secret_store as secret_store

    _mock_secret_store(monkeypatch)

    def _boom(service, value):
        raise secret_store.KeyStoreError("could not store")

    monkeypatch.setattr(secret_store, "set_secret", _boom)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 500
        assert json.loads(text)["ok"] is False
        assert _SYNTHETIC_TOKEN not in text
    finally:
        srv.shutdown()
        srv.server_close()


# --- blanket no-leak (sec LOW-3): the token appears on NO surface where it was in scope -----------


def test_token_value_never_leaks_on_any_surface(monkeypatch):
    """`<token> not in response_text` on the 200-write, the 400 source-reject, AND the 500.

    Each surface parsed the full body (the token was in scope). Pin the invariant on every surface,
    or a future `{token}` interpolation ships green (the sec-w3 LOW-1 precedent).
    """
    import scripts.secret_store as secret_store

    _mock_secret_store(monkeypatch)
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        # 200-write surface
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 200 and _SYNTHETIC_TOKEN not in text

        # 400 source-reject surface (the token was in the parsed body)
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "fitbit", "token": _SYNTHETIC_TOKEN}))
        assert status == 400 and _SYNTHETIC_TOKEN not in text

        # 500 store-failure surface
        def _boom(service, value):
            raise secret_store.KeyStoreError("could not store")

        monkeypatch.setattr(secret_store, "set_secret", _boom)
        status, text = _request(port, "POST", "/settings/tracker",
                                json.dumps({"source": "whoop", "token": _SYNTHETIC_TOKEN}))
        assert status == 500 and _SYNTHETIC_TOKEN not in text
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-6: the frozen ADR-0032 six are byte-frozen vs the FIXED fork-point (PF-S133-03) -----------

_FORK_POINT = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
_FROZEN_SIX = (
    "scripts/store/store.py",
    "scripts/store/keying.py",
    "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    "scripts/plan/router.py",
)


def test_frozen_six_numstat_empty():
    """`git diff --numstat <FIXED fork-point> -- <the six>` prints nothing (never `git merge-base`)."""
    rows = subprocess.run(
        ["git", "diff", "--numstat", _FORK_POINT, "--", *_FROZEN_SIX],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen-six file changed vs the fork point: {changed}"
