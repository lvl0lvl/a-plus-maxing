"""Tests for the shared OAuth/fetch layer + the Whoop cloud adapter (tracker-ingestion Build A).

Covers the design's falsification probes at the fetch-layer grain (all $0, fixture-only, no
real network / keychain / token):
- P1 fetch -> stage -> `ingest.run` lands the correct readings; a re-run appends 0 duplicates.
- P2 a missing / expired / invalid token FAILS CLOSED: `fetch` raises and writes 0 staged bytes,
  the store is unchanged.
- P4 an inbound-only wire-scan: only the vendor host is contacted, the outbound payload is only
  the OAuth token + date-range params (0 store-content bytes; the model lane is never hit).
- delta-since is an optimization, not a correctness dependency (a wider window still lands 0 dup).
- refresh-token rotation is written back to the keychain seam.

The network client and the credential reader/writer are INJECTED seams (fixtures), exactly as
`key_source.resolve(keychain_runner=...)` and `auth_isolation.build_subscription_env(keychain_reader=...)`
inject theirs — so no test touches a real keychain, token, or host.
"""

import json
import types
from urllib.parse import parse_qs, urlparse

import pytest

from scripts.store import store


# --- fixture seams (no real keychain / network) ---


def _resp(status, payload):
    """A duck-typed HTTP response the fetch layer reads (`.status` + `.body` bytes)."""
    body = json.dumps(payload).encode() if not isinstance(payload, (bytes, bytearray)) else payload
    return types.SimpleNamespace(status=status, body=body)


class _RecordingHttp:
    """A fake HTTP seam: records every call and returns a canned response per URL path.

    `routes` maps a URL-path substring -> a `(status, payload)` the seam returns for a request
    whose URL contains it. The token POST and each read GET are matched by path. Every call is
    appended to `.calls` (method / url / headers / body) so a wire-scan can assert what left.
    """

    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def __call__(self, method, url, *, headers=None, body=None, timeout=None):
        self.calls.append(
            {"method": method, "url": url, "headers": dict(headers or {}), "body": body}
        )
        for needle, (status, payload) in self.routes.items():
            if needle in url:
                return _resp(status, payload)
        raise AssertionError(f"unexpected URL in test seam: {url}")


# A fixture Whoop token response + one record per read endpoint, on one day.
_TOKEN_OK = {"access_token": "fixture-access-token", "token_type": "bearer", "expires_in": 3600}
_RECOVERY_ONE = {
    "records": [
        {
            "created_at": "2026-07-10T09:00:00.000Z",
            "score": {
                "recovery_score": 66,
                "hrv_rmssd_milli": 55.0,
                "resting_heart_rate": 48,
                "spo2_percentage": 97.0,
            },
        }
    ],
    "next_token": None,
}
_SLEEP_ONE = {
    "records": [
        {"start": "2026-07-10T23:30:00.000Z",
         "score": {"sleep_efficiency_percentage": 88.0, "respiratory_rate": 14.2}}
    ],
    "next_token": None,
}
_CYCLE_ONE = {
    "records": [{"start": "2026-07-10T04:00:00.000Z", "score": {"strain": 12.3}}],
    "next_token": None,
}


def _whoop_routes(token=_TOKEN_OK, recovery=_RECOVERY_ONE, sleep=_SLEEP_ONE, cycle=_CYCLE_ONE):
    """The standard happy-path route table for a one-day Whoop pull."""
    return {
        "oauth2/token": (200, token),
        "recovery": (200, recovery),
        "sleep": (200, sleep),
        "cycle": (200, cycle),
    }


def _fake_keychain(token="fixture-refresh-token"):
    """A keychain reader seam returning a fixed refresh token (or None to simulate absence)."""
    return lambda source: token


# --- P1: fetch -> stage -> ingest.run lands the correct readings + idempotent re-run ---


def test_fetch_stages_and_ingest_lands_correct_readings(tmp_path):
    """P1: a fixture token + fixture Whoop response stage the delta; `ingest.run` lands each stream.

    Pins the per-stream value (a transposed field->item map would red one of these), the day-keyed
    timepoint, and source="whoop". This is the top functional probe, extended across the fetch
    boundary (the analog of test_whoop_rerun_appends_zero_duplicates + the value-pinning adapter
    tests).
    """
    from scripts.ingest import ingest, oauth_pull
    from scripts.ingest.adapter import Adapter
    from scripts.ingest.adapters import whoop_cloud

    http = _RecordingHttp(_whoop_routes())
    staged = oauth_pull.fetch(
        "whoop", since=None, staged_dir=tmp_path,
        credential_reader=_fake_keychain(), http=http,
    )
    assert staged.exists()

    adapter = whoop_cloud.WhoopCloudAdapter()
    assert isinstance(adapter, Adapter)          # conforms to the frozen contract surface
    assert adapter.source_tag() == "whoop"

    store_root = tmp_path / "store"
    ingest.run(adapter, staged, root=store_root)

    expected = {
        "recovery": 66, "hrv": 55.0, "rhr": 48, "spo2": 97.0,
        "sleep-efficiency": 88.0, "resp-rate": 14.2, "strain": 12.3,
    }
    for item, value in expected.items():
        readings = store.read(item, root=store_root)
        assert len(readings) == 1, item
        assert readings[0]["value"] == value, item
        assert readings[0]["timepoint"] == "2026-07-10", item
        assert readings[0]["source"] == "whoop", item
        assert set(readings[0]) >= set(store.keying.LINE_FIELDS), item


def test_fetch_rerun_appends_zero_duplicates(tmp_path):
    """P1 (idempotency): a second fetch+ingest over the same window appends 0 duplicate lines.

    Idempotent on the inherited (item, day, "whoop") key across the fetch boundary — the store
    dedupe holds even though a fresh staged file is written each run.
    """
    from scripts.ingest import ingest, oauth_pull
    from scripts.ingest.adapters import whoop_cloud

    store_root = tmp_path / "store"
    adapter = whoop_cloud.WhoopCloudAdapter()

    for _ in range(2):
        http = _RecordingHttp(_whoop_routes())
        staged = oauth_pull.fetch(
            "whoop", since=None, staged_dir=tmp_path,
            credential_reader=_fake_keychain(), http=http,
        )
        ingest.run(adapter, staged, root=store_root)

    assert len(store.read("recovery", root=store_root)) == 1  # one day, not two after the re-run


def test_wider_window_still_lands_zero_duplicates(tmp_path):
    """delta-since is an optimization, not a correctness dependency (design §8.5).

    A first pull lands the day; a second pull over an OVERLAPPING wider window (same records)
    lands 0 duplicates — correctness rests on the store key, not on `since` precision.
    """
    from scripts.ingest import ingest, oauth_pull
    from scripts.ingest.adapters import whoop_cloud

    store_root = tmp_path / "store"
    adapter = whoop_cloud.WhoopCloudAdapter()

    http1 = _RecordingHttp(_whoop_routes())
    ingest.run(adapter, oauth_pull.fetch("whoop", since="2026-07-10", staged_dir=tmp_path,
                                         credential_reader=_fake_keychain(), http=http1),
               root=store_root)
    before = len(store.read("recovery", root=store_root))

    # Re-pull with a WIDER (earlier) since -> the same record is re-fetched; the store dedups it.
    http2 = _RecordingHttp(_whoop_routes())
    ingest.run(adapter, oauth_pull.fetch("whoop", since="2026-01-01", staged_dir=tmp_path,
                                         credential_reader=_fake_keychain(), http=http2),
               root=store_root)
    after = len(store.read("recovery", root=store_root))

    assert before == 1
    assert after - before == 0


# --- P2: fail-closed on a missing / expired / invalid token ---


def test_fetch_fails_closed_on_missing_token(tmp_path):
    """P2: no refresh token in the keychain -> `fetch` raises + writes 0 staged bytes, store unchanged."""
    from scripts.ingest import oauth_pull

    store_root = tmp_path / "store"
    # A recording http that would fail the test if contacted — a missing token must short-circuit
    # BEFORE any network call.
    http = _RecordingHttp(_whoop_routes())

    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(token=None), http=http)

    assert list(tmp_path.glob("*.json")) == []      # no partial staged file
    assert http.calls == []                          # never reached the network
    assert store.read_all(store_root) == []          # the store is untouched


def test_fetch_fails_closed_on_expired_token(tmp_path):
    """P2: the token endpoint returns 401 (expired/revoked refresh) -> raise + 0 staged bytes."""
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (401, {"error": "invalid_grant"})
    http = _RecordingHttp(routes)

    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=http)

    assert list(tmp_path.glob("*.json")) == []      # no partial staged file after a token failure


def test_fetch_fails_closed_on_read_endpoint_error(tmp_path):
    """P2 (read path): a read endpoint 500 -> raise + 0 staged bytes (no partial file lands)."""
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["recovery"] = (500, {"error": "server_error"})
    http = _RecordingHttp(routes)

    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=http)

    assert list(tmp_path.glob("*.json")) == []


def test_tracker_pull_error_message_carries_no_token(tmp_path):
    """The fail-closed error message never carries the refresh/access token value (NFR-3, PUBLIC repo)."""
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (401, {"error": "invalid_grant"})
    http = _RecordingHttp(routes)
    with pytest.raises(oauth_pull.TrackerPullError) as exc:
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(token="SECRET-REFRESH-abc123"), http=http)
    assert "SECRET-REFRESH-abc123" not in str(exc.value)


# --- S3: atomic-stage + empty-delta robustness guarantees ---


def test_fetch_empty_delta_stages_empty_lands_nothing(tmp_path):
    """S3(a): an empty delta (every endpoint returns `records: []`) stages `[]`, lands nothing, no crash.

    No fabricated rows, no spurious store write — a tick with no new readings is a clean no-op.
    """
    from scripts.ingest import ingest, oauth_pull
    from scripts.ingest.adapters import whoop_cloud

    empty = {"records": [], "next_token": None}
    http = _RecordingHttp(_whoop_routes(recovery=empty, sleep=empty, cycle=empty))
    staged = oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                              credential_reader=_fake_keychain(), http=http)
    assert staged.exists()
    assert json.loads(staged.read_text()) == []          # staged an empty array (no fabricated rows)

    store_root = tmp_path / "store"
    ingest.run(whoop_cloud.WhoopCloudAdapter(), staged, root=store_root)
    assert store.read_all(store_root) == []               # nothing landed; no spurious store write


def test_fetch_mid_pagination_failure_is_atomic(tmp_path):
    """S3(b): a page-2 HTTP 500 mid-fetch raises + writes 0 staged bytes + leaves the store untouched.

    The atomic-stage guarantee: `fetch` writes the staged file only after every endpoint+page has
    succeeded, so a mid-pagination failure leaves no partial file for `ingest.run` to land.
    """
    from scripts.ingest import oauth_pull

    store_root = tmp_path / "store"

    class _FailPage2Http:
        def __call__(self, method, url, *, headers=None, body=None, timeout=None):
            if "oauth2/token" in url:
                return _resp(200, _TOKEN_OK)
            if parse_qs(urlparse(url).query).get("nextToken") == ["CUR"]:
                return _resp(500, {"error": "server_error"})            # page 2 fails mid-pagination
            return _resp(200, {"records": [{"created_at": "2026-07-10T00:00:00Z",
                                            "score": {"recovery_score": 66}}], "next_token": "CUR"})

    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=_FailPage2Http())

    assert list(tmp_path.glob("*.json")) == []            # 0 staged bytes (no partial file lands)
    assert store.read_all(store_root) == []               # the store is untouched


# --- BUG-1: the `_records` null-vs-malformed semantics at the fetch-layer grain ---


def test_fetch_null_collection_is_empty_delta_not_error(tmp_path):
    """BUG-1 semantic: a present-but-null collection (`{"records": null}`) is the common "no data in the
    window" steady state -> an EMPTY delta (stages [], lands 0), NOT an error.

    REDs if the null coercion is muted (null -> raise/crash instead of an empty delta).
    """
    from scripts.ingest import oauth_pull

    null_env = {"records": None, "next_token": None}
    http = _RecordingHttp(_whoop_routes(recovery=null_env, sleep=null_env, cycle=null_env))
    staged = oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                              credential_reader=_fake_keychain(), http=http)
    assert json.loads(staged.read_text()) == []          # empty delta — no fabricated rows, no raise


def test_fetch_malformed_record_element_fails_closed(tmp_path):
    """BUG-1 semantic: a non-dict record element (`{"records": ["x"]}`) is a genuinely malformed shape ->
    fail closed with `TrackerPullError` + 0 staged bytes (mirroring `_decode_list`), distinct from the
    null "no data" envelope.

    REDs if the element-dict guard is muted (the element then hits `record.get(...)` and surfaces a
    non-TrackerPullError, which `pytest.raises(TrackerPullError)` does not catch).
    """
    from scripts.ingest import oauth_pull

    bad = {"records": ["x"], "next_token": None}         # a non-dict record element
    http = _RecordingHttp(_whoop_routes(recovery=bad))
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=http)
    assert list(tmp_path.glob("*.json")) == []           # 0 staged bytes (atomic fail-closed)


# --- S1: multi-page pagination (the page-follow was untested; single-page fixtures hid it) ---


class _PagingHttp:
    """A 2-page read seam: serves `page1` until a request carries `cursor_param=cursor`, then `page2`.

    Records every call so a test can assert both pages' records land AND the cursor was forwarded to
    the page-2 request — the coverage single-page fixtures could not provide.
    """

    def __init__(self, page1, page2, *, cursor_param, cursor):
        self.page1, self.page2 = page1, page2
        self.cursor_param, self.cursor = cursor_param, cursor
        self.calls = []

    def __call__(self, method, url, *, headers=None, body=None, timeout=None):
        self.calls.append({"method": method, "url": url, "headers": dict(headers or {}), "body": body})
        qs = parse_qs(urlparse(url).query)
        page = self.page2 if qs.get(self.cursor_param) == [self.cursor] else self.page1
        return _resp(200, page)


def test_read_records_follows_whoop_pagination():
    """S1: `_read_records` follows Whoop's `next_token` across pages — both pages' records land and the
    cursor is forwarded to the page-2 request. REDs if the page-follow is muted (only page 1 lands)."""
    from scripts.ingest import oauth_pull

    page1 = {"records": [{"created_at": "2026-07-10T09:00:00.000Z", "score": {"recovery_score": 66}}],
             "next_token": "CURSOR-2"}
    page2 = {"records": [{"created_at": "2026-07-11T09:00:00.000Z", "score": {"recovery_score": 70}}],
             "next_token": None}
    http = _PagingHttp(page1, page2, cursor_param="nextToken", cursor="CURSOR-2")

    records = list(oauth_pull._read_records(http, oauth_pull._WHOOP, "/v1/recovery", "whoop", "tok", None))
    assert [r["created_at"][:10] for r in records] == ["2026-07-10", "2026-07-11"]   # BOTH pages
    forwarded = [c for c in http.calls if "nextToken=CURSOR-2" in c["url"]]
    assert len(forwarded) == 1                                                       # cursor -> page 2


def test_read_records_raises_on_never_terminating_cursor():
    """S1: a cursor that never terminates hits the `_MAX_PAGES` ceiling and fails fast (never hangs)."""
    from scripts.ingest import oauth_pull

    class _InfiniteHttp:
        def __init__(self):
            self.calls = 0

        def __call__(self, method, url, *, headers=None, body=None, timeout=None):
            self.calls += 1
            return _resp(200, {"records": [{"created_at": "2026-07-10T00:00:00Z", "score": {}}],
                               "next_token": "ALWAYS-MORE"})

    http = _InfiniteHttp()
    with pytest.raises(oauth_pull.TrackerPullError):
        list(oauth_pull._read_records(http, oauth_pull._WHOOP, "/v1/recovery", "whoop", "tok", None))
    assert http.calls == oauth_pull._MAX_PAGES      # stopped at the ceiling, bounded (did not hang)


# --- P4: inbound-only wire-scan (the crown-jewel privacy probe) ---


def test_fetch_wire_scan_contacts_only_vendor_host(tmp_path):
    """P4 (c): every outbound request goes to the Whoop vendor host — 0 other hosts, 0 model lane."""
    from scripts.ingest import oauth_pull

    http = _RecordingHttp(_whoop_routes())
    oauth_pull.fetch("whoop", since="2026-07-01", staged_dir=tmp_path,
                     credential_reader=_fake_keychain(), http=http)

    assert http.calls, "the fetch must make at least the token + one read call"
    hosts = {urlparse(c["url"]).hostname for c in http.calls}
    assert hosts == {"api.prod.whoop.com"}, hosts   # only the vendor host; never api.anthropic.com


def test_fetch_wire_scan_outbound_payload_is_only_token_and_params(tmp_path):
    """P4 (a/d): the outbound payload is only the OAuth token + date-range params (0 store content).

    The token POST body carries ONLY the OAuth refresh-grant fields; each read GET carries a Bearer
    header + the since/limit query params and NO body. Mechanizes the §4 ruling that the pull ships
    a credential + a cursor, never store content.
    """
    from scripts.ingest import oauth_pull

    http = _RecordingHttp(_whoop_routes())
    oauth_pull.fetch("whoop", since="2026-07-01", staged_dir=tmp_path,
                     credential_reader=_fake_keychain(), http=http)

    token_calls = [c for c in http.calls if "oauth2/token" in c["url"]]
    read_calls = [c for c in http.calls if "oauth2/token" not in c["url"]]
    assert len(token_calls) == 1
    assert token_calls[0]["method"] == "POST"

    # The token body is form-urlencoded OAuth fields only — no key outside the refresh-grant set.
    token_body = token_calls[0]["body"]
    token_body = token_body.decode() if isinstance(token_body, (bytes, bytearray)) else token_body
    allowed = {"grant_type", "refresh_token", "client_id", "client_secret", "scope"}
    assert set(parse_qs(token_body)).issubset(allowed)

    # Each read GET carries the Bearer access token + query params only, and NO request body.
    assert read_calls, "the fetch must issue read GETs"
    for c in read_calls:
        assert c["method"] == "GET"
        assert c["body"] in (None, b"", "")
        auth = c["headers"].get("Authorization", "")
        assert auth.startswith("Bearer ")
        # The read carries only whitelisted query params (the delta cursor + paging), never PII.
        qs = set(parse_qs(urlparse(c["url"]).query))
        assert qs.issubset({"start", "end", "limit", "nextToken"})


def test_fetch_never_carries_a_store_sentinel_outbound(tmp_path):
    """P4 (a): a distinctive value pre-seeded in the store never appears in any outbound byte.

    Non-tautological: the store holds a sentinel reading; the fetch path runs; the sentinel appears
    in no outbound url / header / body. Proves the fetch is inbound-only even in the presence of
    store content (the fetch never reads the store — this pins that it stays that way).
    """
    from scripts.ingest import oauth_pull

    store_root = tmp_path / "store"
    sentinel = "SENTINEL-919283.777"
    store.append("hrv", {"item": "hrv", "timepoint": "2026-05-01",
                         "source": "whoop", "value": sentinel}, root=store_root)

    http = _RecordingHttp(_whoop_routes())
    oauth_pull.fetch("whoop", since="2026-07-01", staged_dir=tmp_path,
                     credential_reader=_fake_keychain(), http=http)

    for c in http.calls:
        blob = json.dumps({"u": c["url"], "h": c["headers"],
                           "b": c["body"].decode() if isinstance(c["body"], (bytes, bytearray)) else c["body"]})
        assert sentinel not in blob


# --- refresh-token rotation write-back ---


def test_access_token_writes_rotated_refresh_back_to_keychain(tmp_path):
    """A rotated refresh token in the token response is written back to the keychain seam.

    Whoop rotates the refresh token on each use; the layer persists the new one so the next run
    authenticates. Mirrors `key_source.store`'s keychain write path.
    """
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (200, {**_TOKEN_OK, "refresh_token": "rotated-refresh-token"})
    http = _RecordingHttp(routes)

    written = {}
    token = oauth_pull.access_token(
        "whoop",
        credential_reader=_fake_keychain(token="old-refresh-token"),
        credential_writer=lambda source, payload: written.__setitem__(source, payload),
        http=http,
    )
    assert token == "fixture-access-token"
    assert "rotated-refresh-token" in written["whoop"]     # the new refresh token was persisted


def test_access_token_no_rotation_writes_nothing(tmp_path):
    """A token response WITHOUT a new refresh token writes nothing back (no spurious keychain write)."""
    from scripts.ingest import oauth_pull

    http = _RecordingHttp(_whoop_routes())          # _TOKEN_OK carries no refresh_token
    written = {}
    oauth_pull.access_token(
        "whoop",
        credential_reader=_fake_keychain(token="old-refresh-token"),
        credential_writer=lambda source, payload: written.__setitem__(source, payload),
        http=http,
    )
    assert written == {}


# --- SEC-02: a failed rotation write-back is loud + non-fatal (never a silent stranded token) ---


def test_rotation_write_failure_is_loud_and_non_fatal(monkeypatch, capsys):
    """SEC-02: a `secret_store` write failure emits a LOUD diagnostic and does NOT raise.

    Unlike `key_source._keychain_writer` (which TRANSLATES the `secret_store.KeyStoreError` to a raise),
    the rotation write is non-fatal — the current tick already holds its access token — but it must be
    loud: a silent failure would leave the consumed refresh token unpersisted and the NEXT tick 401s,
    blaming the token rather than the write. The diagnostic is SOFTENED (AR-003): `secret_store.set_secret`
    raises the same `KeyStoreError` for two conditions this writer cannot tell apart (the token persisted
    nowhere vs the token WAS persisted and only stale fallback residue could not be cleared — the SEC-04
    clear-fail), so it must NOT assert stranding as a certainty. No real keyring is touched (the
    module-object `oauth_pull.secret_store.set_secret` is stubbed).
    """
    from scripts.ingest import oauth_pull

    def _boom(service, value):
        raise oauth_pull.secret_store.KeyStoreError("store write failed")

    monkeypatch.setattr(oauth_pull.secret_store, "set_secret", _boom)
    oauth_pull._write_oauth_credential("whoop", "rotated-token-payload")   # must NOT raise

    err = capsys.readouterr().err.lower()
    assert "whoop" in err and "keychain" in err        # loud + names the source + the store surface
    assert "stranded" not in err                       # softened: no false "stranded" certainty (AR-003)
    assert "will fail closed" not in err               # softened: no false "will fail closed" certainty


def test_rotation_write_success_is_silent(monkeypatch, capsys):
    """A successful `secret_store` write-back emits no diagnostic (no spurious warning on the happy path)."""
    from scripts.ingest import oauth_pull

    monkeypatch.setattr(oauth_pull.secret_store, "set_secret", lambda service, value: None)
    oauth_pull._write_oauth_credential("whoop", "rotated-token-payload")
    assert capsys.readouterr().err == ""


def test_access_token_completes_when_rotation_write_back_fails(monkeypatch, capsys):
    """SEC-02 integrated: a failed rotation write-back still lets `access_token` return the token.

    The token response rotates the refresh token; the default `secret_store` write-back fails. The current
    operation still completes (the access token is returned) and the failure is surfaced loudly — the
    tick succeeds, the operator is warned the next tick may need re-auth. Exercises the DEFAULT
    `credential_writer` (the migration re-points the write seam at `oauth_pull.secret_store.set_secret`).
    """
    from scripts.ingest import oauth_pull

    def _boom(service, value):
        raise oauth_pull.secret_store.KeyStoreError("store write failed")

    monkeypatch.setattr(oauth_pull.secret_store, "set_secret", _boom)
    routes = _whoop_routes()
    routes["oauth2/token"] = (200, {**_TOKEN_OK, "refresh_token": "rotated-refresh-token"})

    token = oauth_pull.access_token(
        "whoop",
        credential_reader=_fake_keychain(token="old-refresh-token"),
        http=_RecordingHttp(routes),      # credential_writer defaults to the real _write_oauth_credential
    )
    assert token == "fixture-access-token"                 # the operation completed
    assert "whoop" in capsys.readouterr().err.lower()      # ... and the write failure was loud


# --- ADR-0047-T3: the DEFAULT credential seams route through the secret_store abstraction ---


def test_default_seams_route_through_secret_store(monkeypatch):
    """AC-1: the DEFAULT credential seams delegate to `secret_store`, keyed a-plus-maxing-<source>-oauth.

    Pins the EXACT service string, derived from `source` (a whoop read + an oura write) — so a
    transposition or a hardcoded service reds. The default read delegates to `secret_store.get_secret`;
    the default write to `secret_store.set_secret`. No real keyring is touched (both are stubbed).
    """
    from scripts.ingest import oauth_pull

    seen = {}
    monkeypatch.setattr(oauth_pull.secret_store, "get_secret",
                        lambda service: seen.__setitem__("read", service) or "fixture-token")
    monkeypatch.setattr(oauth_pull.secret_store, "set_secret",
                        lambda service, value: seen.__setitem__("write", (service, value)))

    assert oauth_pull._read_oauth_credential("whoop") == "fixture-token"
    assert seen["read"] == "a-plus-maxing-whoop-oauth"

    oauth_pull._write_oauth_credential("oura", "rotated-payload")
    assert seen["write"] == ("a-plus-maxing-oura-oauth", "rotated-payload")


def test_no_security_shellout_in_oauth_pull():
    """AC-3: no `security` shell-out survives in oauth_pull — bare-token grep + import scan, non-vacuous.

    Greps the module SOURCE for the list-form invocation token `(find|add)-generic-password` — which
    matches the actual comma-separated `["security", "find-generic-password", ...]` list literal, NOT
    just docstring prose (the space-form regex only matched prose, so it would go green merely from
    deleting a docstring — the T2 AC-3 defect). Also scans `subprocess.run` and the `import subprocess` /
    `import getpass` lines. A positive control proves the pattern is RED-capable against a planted
    list-form shell-out in perpetuity (mirrors test_ingest.py::test_key_def_scan_detects_planted_token).
    """
    import re
    from pathlib import Path

    from scripts.ingest import oauth_pull

    src = Path(oauth_pull.__file__).read_text()
    assert len(re.findall(r"(find|add)-generic-password", src)) == 0       # list-literal + prose both gone
    assert len(re.findall(r"subprocess\.run", src)) == 0
    assert len(re.findall(r"(?m)^\s*import subprocess", src)) == 0
    assert len(re.findall(r"(?m)^\s*import getpass", src)) == 0

    # Positive control: the bare-token pattern matches a real list-form shell-out (RED-capable forever).
    planted = 'subprocess.run(["security", "find-generic-password", "-w", "-s", svc])'
    assert len(re.findall(r"(find|add)-generic-password", planted)) > 0
    assert len(re.findall(r"subprocess\.run", planted)) > 0


def test_unattended_rotation_roundtrip_through_abstraction(monkeypatch):
    """AC-4: a rotated refresh token written via the default writer round-trips through the abstraction.

    The default `_write_oauth_credential` persists via `secret_store.set_secret`; a later default
    `_read_oauth_credential` recovers it via `secret_store.get_secret` — 0 prompts (structural to the
    shared-dict mock). Proves the unattended rotating-vendor path (Whoop) survives the refactor end to
    end. NOT the real `backend=` kwarg (oauth_pull never threads it) — the module seams are stubbed.
    """
    from scripts.ingest import oauth_pull

    persisted = {}
    monkeypatch.setattr(oauth_pull.secret_store, "set_secret",
                        lambda service, value: persisted.__setitem__(service, value))
    monkeypatch.setattr(oauth_pull.secret_store, "get_secret", lambda service: persisted.get(service))

    oauth_pull._write_oauth_credential("whoop", "rotated-refresh-token")
    assert oauth_pull._read_oauth_credential("whoop") == "rotated-refresh-token"


def test_default_reader_strips_and_collapses(monkeypatch):
    """AC-4b (F1 strip pin): the default reader strips padding and collapses whitespace-only to None.

    `secret_store.get_secret` returns the stored value VERBATIM (no strip), so `_read_oauth_credential`
    must strip + collapse — else a padded refresh token flows to a 401 refresh and a whitespace-only
    payload becomes a truthy garbage credential that bypasses the fail-closed no-token guard. RED-capable:
    drop the strip -> the padded value is returned / the whitespace-only value is truthy, not None.
    """
    from scripts.ingest import oauth_pull

    monkeypatch.setattr(oauth_pull.secret_store, "get_secret", lambda service: "  padded-token  ")
    assert oauth_pull._read_oauth_credential("whoop") == "padded-token"

    monkeypatch.setattr(oauth_pull.secret_store, "get_secret", lambda service: "   ")
    assert oauth_pull._read_oauth_credential("whoop") is None


# --- TEST-1: honest absence — a null score field / missing timestamp yields NO fabricated row ---


def test_whoop_honest_absence_null_field_and_missing_timestamp(tmp_path):
    """TEST-1: a null score field and a missing-timestamp record each yield NO row (never a fabricated
    `{value: None}` row, never a crash) — only the present field lands.

    REDs when either guard is muted: muting `if value is not None` stages the three null fields as
    value-None rows; muting `if not timestamp` crashes on `None[:10]`.
    """
    from scripts.ingest import oauth_pull

    recovery = {"records": [
        {"created_at": "2026-07-10T09:00:00.000Z",
         "score": {"recovery_score": 66, "hrv_rmssd_milli": None,
                   "resting_heart_rate": None, "spo2_percentage": None}},   # only recovery_score present
        {"score": {"recovery_score": 70}},                                  # missing created_at -> no row
    ], "next_token": None}
    empty = {"records": [], "next_token": None}
    http = _RecordingHttp(_whoop_routes(recovery=recovery, sleep=empty, cycle=empty))
    staged = oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                              credential_reader=_fake_keychain(), http=http)

    assert json.loads(staged.read_text()) == [
        {"item": "recovery", "timepoint": "2026-07-10", "value": 66},
    ]                                                    # the null fields + missing-timestamp record -> 0 rows


# --- TEST-2: a degraded 200 token response fails closed (no access_token / non-dict / non-json body) ---


def test_fetch_fails_closed_on_degraded_200_token_no_access_token(tmp_path):
    """TEST-2: a 200 token response carrying NO access_token fails closed (`if not token: raise`).

    A vendor can return HTTP 200 with an error/degraded body and no token; the layer must NOT proceed
    with a `Bearer None` read. REDs when the guard is muted (the fetch would proceed and stage rows).
    """
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (200, {"error": "temporarily_unavailable"})   # 200, but no access_token
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=_RecordingHttp(routes))
    assert list(tmp_path.glob("*.json")) == []          # 0 staged bytes


def test_fetch_fails_closed_on_degraded_200_token_non_dict_body(tmp_path):
    """TEST-2: a 200 token response whose body is a JSON list (not an object) fails closed in `_decode`.

    REDs when `_decode`'s `if not isinstance(data, dict)` guard is muted (the list body would then hit
    `data.get(...)` and surface a non-TrackerPullError).
    """
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (200, [{"access_token": "x"}])   # 200, but a JSON array, not an object
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=_RecordingHttp(routes))
    assert list(tmp_path.glob("*.json")) == []


def test_fetch_fails_closed_on_degraded_200_token_non_json_body(tmp_path):
    """TEST-2: a 200 token response whose body is not JSON at all fails closed in `_decode` (malformed).

    REDs when `_decode`'s `json.loads` try/except is muted (the ValueError would surface un-wrapped).
    """
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (200, b"<html>gateway timeout</html>")   # 200, but a non-JSON body
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("whoop", since=None, staged_dir=tmp_path,
                         credential_reader=_fake_keychain(), http=_RecordingHttp(routes))
    assert list(tmp_path.glob("*.json")) == []


# --- TEST-3: JSON-blob credential rotation preserves client_id/secret, updates only refresh_token ---


def test_access_token_blob_credential_rotation_preserves_client_fields(tmp_path):
    """TEST-3: rotating a JSON-blob credential (client_id/secret + refresh_token) writes back valid JSON
    that PRESERVES client_id/client_secret and updates ONLY refresh_token (`_serialize_credentials`'s
    blob branch). The bare-token rotation tests never exercise this branch.

    REDs when the blob branch is muted (a bare rotated token would be written back, failing json.loads /
    dropping the client fields).
    """
    from scripts.ingest import oauth_pull

    routes = _whoop_routes()
    routes["oauth2/token"] = (200, {**_TOKEN_OK, "refresh_token": "rotated-refresh-token"})
    blob = json.dumps({"refresh_token": "old-refresh", "client_id": "cid-123", "client_secret": "csec-xyz"})

    written = {}
    token = oauth_pull.access_token(
        "whoop",
        credential_reader=_fake_keychain(token=blob),
        credential_writer=lambda source, payload: written.__setitem__(source, payload),
        http=_RecordingHttp(routes),
    )
    assert token == "fixture-access-token"

    payload = json.loads(written["whoop"])                       # a valid JSON blob was written back
    assert payload["refresh_token"] == "rotated-refresh-token"   # only the refresh token updated
    assert payload["client_id"] == "cid-123"                     # client fields PRESERVED
    assert payload["client_secret"] == "csec-xyz"


# --- the Whoop cloud adapter (the wired "whoop" file-reading parser) ---


# --- SEC-01: the authenticated `_http` seam must not follow a cross-host redirect (bearer leak) ---


def _serve_local(handler_cls):
    """Start a localhost HTTP server on an ephemeral port in a daemon thread; return (server, port)."""
    import http.server
    import socketserver
    import threading

    server = socketserver.TCPServer(("127.0.0.1", 0), handler_cls)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, port


def test_http_refuses_cross_host_redirect_and_never_leaks_bearer():
    """SEC-01: `_http` does NOT follow a 3xx redirect, so the access token never leaks to the target.

    A local 'vendor' returns `302 Location: http://<local-attacker>/leak`; `_http` — carrying an
    `Authorization: Bearer` header — must raise `TrackerPullError` and the attacker must receive 0
    requests (so it never sees the bearer). REDs on the pre-fix default opener, which FOLLOWS the
    redirect and delivers the bearer to the attacker host (urllib 3.14 copies Authorization cross-host).
    $0 — two local sockets, no real network.
    """
    import http.server

    from scripts.ingest import oauth_pull

    attacker_hits = []

    class _Attacker(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            attacker_hits.append({"path": self.path, "auth": self.headers.get("Authorization")})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *a):
            pass

    attacker, attacker_port = _serve_local(_Attacker)

    class _Vendor(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{attacker_port}/leak")
            self.end_headers()

        def log_message(self, *a):
            pass

    vendor, vendor_port = _serve_local(_Vendor)

    try:
        with pytest.raises(oauth_pull.TrackerPullError):
            oauth_pull._http("GET", f"http://127.0.0.1:{vendor_port}/read",
                             headers={"Authorization": "Bearer SECRET-BEARER-xyz"})
        assert attacker_hits == []      # 0 requests to the redirect target; the bearer never left
    finally:
        attacker.shutdown()
        vendor.shutdown()


def test_http_returns_a_direct_2xx_normally():
    """The SEC-01 no-follow opener still serves a direct 2xx (it refuses only redirects, not requests)."""
    import http.server

    from scripts.ingest import oauth_pull

    class _Ok(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok": true}')

        def log_message(self, *a):
            pass

    server, port = _serve_local(_Ok)
    try:
        resp = oauth_pull._http("GET", f"http://127.0.0.1:{port}/read")
        assert resp.status == 200
        assert resp.body == b'{"ok": true}'
    finally:
        server.shutdown()


def test_whoop_cloud_adapter_parses_staged_rows(tmp_path):
    """The whoop_cloud adapter maps the staged {item, timepoint, value} rows to Line-Field-Set readings.

    The adapter owns the source tag (adds source="whoop"), like every wired adapter; it is a pure
    file parser (no network).
    """
    from scripts.ingest.adapters import whoop_cloud

    staged = tmp_path / "whoop.json"
    staged.write_text(json.dumps([
        {"item": "recovery", "timepoint": "2026-07-10", "value": 66},
        {"item": "hrv", "timepoint": "2026-07-10", "value": 55.0},
    ]))

    readings = list(whoop_cloud.WhoopCloudAdapter().read_readings(staged))
    assert readings == [
        {"item": "recovery", "timepoint": "2026-07-10", "source": "whoop", "value": 66},
        {"item": "hrv", "timepoint": "2026-07-10", "source": "whoop", "value": 55.0},
    ]
