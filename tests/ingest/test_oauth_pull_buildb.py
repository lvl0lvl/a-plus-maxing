"""Tests for the Build-B API-pull sources (oura / garmin / google-health) + their cloud adapters.

Extends the Build-A `test_oauth_pull.py` fixture style across the three sources Build B adds on the
shared OAuth/fetch layer (all $0, fixture-only, no real network / keychain / token — the http and
credential seams are injected, exactly as `key_source.resolve(keychain_runner=...)` injects its own).
Per source, the design's falsification probes at the fetch-layer grain:

- P1  fetch -> stage -> `ingest.run` lands the correct per-stream readings; a re-run appends 0 dup.
- P2  a missing / expired / malformed credential FAILS CLOSED: `fetch` raises, writes 0 staged bytes,
      leaves the store untouched, and never leaks the credential value into the error text.
- P4  an inbound-only wire-scan: only the vendor host(s) are contacted, a store sentinel never leaves,
      and the no-train model client is never even constructed.

Garmin ALSO carries the OAuth 1.0a HMAC-SHA1 signing suite: a KNOWN-ANSWER vector (the canonical X /
Twitter worked example, whose base string + signature are externally documented) plus a mutation-reds
control, so a bug in the signature-base-string construction turns the vector RED (design §10.2).
"""

import json
import types
from urllib.parse import parse_qs, urlparse

import pytest

from scripts.store import store

from test_oauth_pull import _PagingHttp, _RecordingHttp, _resp

# --- per-source fixture credentials (synthetic; never a real token) ---

# Oura / Google refresh via the shared OAuth-2.0 `access_token`, whose refresh grant needs the client
# id/secret, so the keychain payload is a JSON blob (not a bare token).
_OAUTH2_CRED = json.dumps({"refresh_token": "fixture-refresh", "client_id": "cid", "client_secret": "csec"})
# Garmin OAuth 1.0a needs all four parts to sign each request.
_GARMIN_CRED = json.dumps({"consumer_key": "ck", "consumer_secret": "cs",
                           "token": "tk", "token_secret": "ts"})
_TOKEN_OK = {"access_token": "fixture-access-token", "token_type": "bearer", "expires_in": 3600}


def _cred(payload):
    """A credential-reader seam returning a fixed payload for any source (or None to simulate absence)."""
    return lambda source: payload


# --- Oura fixtures ---


def _oura_routes(token=_TOKEN_OK):
    """The happy-path Oura route table for a one-day pull (the `data` envelope, top-level readings)."""
    return {
        "oauth/token": (200, token),
        "daily_sleep": (200, {"data": [{"day": "2026-07-10", "score": 82}], "next_token": None}),
        "daily_readiness": (200, {"data": [{"day": "2026-07-10", "score": 76}], "next_token": None}),
        "daily_activity": (200, {"data": [{"day": "2026-07-10", "score": 88}], "next_token": None}),
        "/sleep?": (200, {"data": [{"day": "2026-07-10", "average_hrv": 58, "average_heart_rate": 49}],
                          "next_token": None}),
        "/sleep": (200, {"data": [{"day": "2026-07-10", "average_hrv": 58, "average_heart_rate": 49}],
                         "next_token": None}),
    }


_OURA_EXPECTED = {"sleep": 82, "readiness": 76, "activity": 88, "hrv": 58, "rhr": 49}


# --- Garmin fixtures ---


def _garmin_routes():
    """The happy-path Garmin route table (top-level JSON-array summaries, `calendarDate` day)."""
    return {
        "/dailies": (200, [{"calendarDate": "2026-07-10",
                            "restingHeartRateInBeatsPerMinute": 48, "averageStressLevel": 30}]),
        "/hrv": (200, [{"calendarDate": "2026-07-10", "lastNightAvg": 61}]),
        "/sleeps": (200, [{"calendarDate": "2026-07-10", "overallSleepScore": 79}]),
        "/epochs": (200, [{"calendarDate": "2026-07-10", "activeKilocalories": 540}]),
    }


_GARMIN_EXPECTED = {"rhr": 48, "stress": 30, "hrv": 61, "sleep": 79, "activity": 540}


# --- Google Health fixtures ---


def _g_point(day, value_key, inner_key, value):
    """One Google `dailyRollUp` rollup point: a civil day + a nested value path to a scalar."""
    return {"civilStartTime": {"date": {"year": 2026, "month": 7, "day": day}},
            value_key: {inner_key: value}}


def _google_routes(token=_TOKEN_OK):
    """The happy-path Google route table (the `dailyRollUp` POST, `rollupDataPoints` envelope)."""
    return {
        "oauth2.googleapis.com/token": (200, token),
        "resting-heart-rate": (200, {"rollupDataPoints": [_g_point(10, "restingHeartRate", "avg", 47)]}),
        "heart-rate-variability": (200, {"rollupDataPoints": [_g_point(10, "heartRateVariability", "avg", 62)]}),
        "dataTypes/heart-rate/": (200, {"rollupDataPoints": [_g_point(10, "heartRate", "avg", 58)]}),
        "oxygen-saturation": (200, {"rollupDataPoints": [_g_point(10, "oxygenSaturation", "avg", 97)]}),
        "dataTypes/sleep/": (200, {"rollupDataPoints": [_g_point(10, "sleep", "durationMillis", 27000000)]}),
        "active-zone-minutes": (200, {"rollupDataPoints": [_g_point(10, "activeZoneMinutes", "totalMinutes", 42)]}),
    }


_GOOGLE_EXPECTED = {"rhr": 47, "hrv": 62, "heart-rate": 58, "spo2": 97,
                    "sleep": 27000000, "activity": 42}


# A per-source table: (source, adapter import path + class, routes factory, credential, expected map,
# vendor hosts, staged day). Drives the P1/P2/P4 probes uniformly across the three sources.
_SOURCES = {
    "oura": (("oura_cloud", "OuraCloudAdapter"), _oura_routes, _OAUTH2_CRED, _OURA_EXPECTED,
             {"api.ouraring.com"}),
    "garmin": (("garmin_cloud", "GarminCloudAdapter"), _garmin_routes, _GARMIN_CRED, _GARMIN_EXPECTED,
               {"apis.garmin.com"}),
    "google-health": (("google_health_cloud", "GoogleHealthCloudAdapter"), _google_routes,
                      _OAUTH2_CRED, _GOOGLE_EXPECTED, {"oauth2.googleapis.com", "health.googleapis.com"}),
}


def _adapter(source):
    """Instantiate the wired cloud adapter for a source."""
    import importlib

    module_name, class_name = _SOURCES[source][0]
    module = importlib.import_module(f"scripts.ingest.adapters.{module_name}")
    return getattr(module, class_name)()


# --- P1: fetch -> stage -> ingest.run lands the correct readings + idempotent re-run ---


@pytest.mark.parametrize("source", list(_SOURCES))
def test_fetch_stages_and_ingest_lands_correct_readings(source, tmp_path):
    """P1: a fixture credential + fixture API response stage the delta; `ingest.run` lands each stream.

    Pins the per-stream value (a transposed field->item map would red one of these), the day-keyed
    timepoint, and the device-specific source. The top functional probe extended across the fetch
    boundary, for each Build-B source's distinct response shape.
    """
    from scripts.ingest import oauth_pull
    from scripts.ingest.adapter import Adapter

    _, routes, cred, expected, _hosts = _SOURCES[source]
    http = _RecordingHttp(routes())
    staged = oauth_pull.fetch(source, since="2026-07-01", staged_dir=tmp_path,
                              credential_reader=_cred(cred), http=http)
    assert staged.exists()

    adapter = _adapter(source)
    assert isinstance(adapter, Adapter)          # conforms to the frozen contract surface
    assert adapter.source_tag() == source

    store_root = tmp_path / "store"
    from scripts.ingest import ingest
    ingest.run(adapter, staged, root=store_root)

    for item, value in expected.items():
        readings = store.read(item, root=store_root)
        assert len(readings) == 1, item
        assert readings[0]["value"] == value, item
        assert readings[0]["timepoint"] == "2026-07-10", item
        assert readings[0]["source"] == source, item
        assert set(readings[0]) >= set(store.keying.LINE_FIELDS), item


@pytest.mark.parametrize("source", list(_SOURCES))
def test_fetch_rerun_appends_zero_duplicates(source, tmp_path):
    """P1 (idempotency): a second fetch+ingest over the same window appends 0 duplicate lines.

    Idempotent on the inherited (item, day, source) key across the fetch boundary — the store dedupe
    holds even though a fresh staged file is written each run.
    """
    from scripts.ingest import ingest, oauth_pull

    _, routes, cred, expected, _hosts = _SOURCES[source]
    store_root = tmp_path / "store"
    adapter = _adapter(source)
    probe_item = next(iter(expected))

    for _ in range(2):
        http = _RecordingHttp(routes())
        staged = oauth_pull.fetch(source, since=None, staged_dir=tmp_path,
                                  credential_reader=_cred(cred), http=http)
        ingest.run(adapter, staged, root=store_root)

    assert len(store.read(probe_item, root=store_root)) == 1   # one day, not two after the re-run


def test_wider_window_still_lands_zero_duplicates(tmp_path):
    """delta-since is an optimization, not a correctness dependency (design §8.5), across sources.

    A first pull lands the day; a second pull over an OVERLAPPING wider window lands 0 duplicates —
    correctness rests on the store key, not on `since` precision. Exercised on Oura (paginated GET).
    """
    from scripts.ingest import ingest, oauth_pull
    from scripts.ingest.adapters import oura_cloud

    store_root = tmp_path / "store"
    adapter = oura_cloud.OuraCloudAdapter()

    ingest.run(adapter, oauth_pull.fetch("oura", since="2026-07-10", staged_dir=tmp_path,
                                         credential_reader=_cred(_OAUTH2_CRED),
                                         http=_RecordingHttp(_oura_routes())), root=store_root)
    before = len(store.read("sleep", root=store_root))
    ingest.run(adapter, oauth_pull.fetch("oura", since="2026-01-01", staged_dir=tmp_path,
                                         credential_reader=_cred(_OAUTH2_CRED),
                                         http=_RecordingHttp(_oura_routes())), root=store_root)
    after = len(store.read("sleep", root=store_root))

    assert before == 1
    assert after - before == 0


# --- P2: fail-closed on a missing / expired / malformed credential ---


@pytest.mark.parametrize("source", list(_SOURCES))
def test_fetch_fails_closed_on_missing_credential(source, tmp_path):
    """P2: no credential in the keychain -> `fetch` raises + writes 0 staged bytes, store unchanged.

    The missing-credential guard short-circuits BEFORE any network call (`http.calls == []`) — the
    non-tautological proof the guard is load-bearing: were it removed, the fetch would dial out and
    `http.calls` would be non-empty.
    """
    from scripts.ingest import oauth_pull

    _, routes, _cred_unused, _expected, _hosts = _SOURCES[source]
    store_root = tmp_path / "store"
    http = _RecordingHttp(routes())

    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch(source, since=None, staged_dir=tmp_path,
                         credential_reader=_cred(None), http=http)

    assert list(tmp_path.glob("*.json")) == []      # no partial staged file
    assert http.calls == []                          # never reached the network (guard is load-bearing)
    assert store.read_all(store_root) == []          # the store is untouched


def test_oura_fails_closed_on_expired_token(tmp_path):
    """P2 (OAuth-2.0 token path): a 401 from Oura's token endpoint -> raise + 0 staged bytes."""
    from scripts.ingest import oauth_pull

    routes = _oura_routes()
    routes["oauth/token"] = (401, {"error": "invalid_grant"})
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("oura", since=None, staged_dir=tmp_path,
                         credential_reader=_cred(_OAUTH2_CRED), http=_RecordingHttp(routes))
    assert list(tmp_path.glob("*.json")) == []


def test_google_fails_closed_on_read_endpoint_error(tmp_path):
    """P2 (read path): a 500 from a Google rollup read -> raise + 0 staged bytes (no partial file)."""
    from scripts.ingest import oauth_pull

    routes = _google_routes()
    routes["resting-heart-rate"] = (500, {"error": "server_error"})
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("google-health", since=None, staged_dir=tmp_path,
                         credential_reader=_cred(_OAUTH2_CRED), http=_RecordingHttp(routes))
    assert list(tmp_path.glob("*.json")) == []


def test_garmin_fails_closed_on_incomplete_oauth1_credential(tmp_path):
    """P2 (Garmin 1.0a): a credential missing a part -> raise + 0 staged bytes + 0 network calls.

    A partial 1.0a credential cannot produce a valid signature, so it fails closed like a missing
    token rather than dialing out with a bad signature.
    """
    from scripts.ingest import oauth_pull

    partial = json.dumps({"consumer_key": "ck", "consumer_secret": "cs", "token": "tk"})  # no token_secret
    http = _RecordingHttp(_garmin_routes())
    with pytest.raises(oauth_pull.TrackerPullError):
        oauth_pull.fetch("garmin", since=None, staged_dir=tmp_path,
                         credential_reader=_cred(partial), http=http)
    assert list(tmp_path.glob("*.json")) == []
    assert http.calls == []


@pytest.mark.parametrize("source,cred", [("oura", _OAUTH2_CRED), ("google-health", _OAUTH2_CRED)])
def test_fetch_error_message_carries_no_token(source, cred, tmp_path):
    """The fail-closed error never carries the refresh/access token value (NFR-3, the repo is PUBLIC)."""
    from scripts.ingest import oauth_pull

    secret_cred = json.dumps({"refresh_token": "SECRET-REFRESH-abc123", "client_id": "c", "client_secret": "x"})
    routes = _oura_routes() if source == "oura" else _google_routes()
    key = "oauth/token" if source == "oura" else "oauth2.googleapis.com/token"
    routes[key] = (401, {"error": "invalid_grant"})
    with pytest.raises(oauth_pull.TrackerPullError) as exc:
        oauth_pull.fetch(source, since=None, staged_dir=tmp_path,
                         credential_reader=_cred(secret_cred), http=_RecordingHttp(routes))
    assert "SECRET-REFRESH-abc123" not in str(exc.value)


# --- P4: inbound-only wire-scan (the crown-jewel privacy probe) ---


@pytest.mark.parametrize("source", list(_SOURCES))
def test_fetch_wire_scan_inbound_only(source, tmp_path, monkeypatch):
    """P4: only the vendor host(s) are contacted, a store sentinel never leaves, model lane never built.

    Pre-seeds the store with a distinctive sentinel, runs the fetch under a recording seam, and asserts
    (a) every outbound host is a vendor host (never api.anthropic.com), (b) the sentinel appears in no
    outbound url/header/body, (c) the no-train model client is never even constructed (a stronger proof
    than the host set alone). Mechanizes the §4 inbound-only ruling for each Build-B source.
    """
    from scripts.ingest import oauth_pull
    from scripts.model.client import ModelClient

    _, routes, cred, _expected, hosts = _SOURCES[source]

    def _no_model(*a, **k):
        raise AssertionError("the fetch path constructed the model client — not inbound-only")

    monkeypatch.setattr(ModelClient, "__init__", _no_model)

    store_root = tmp_path / "store"
    sentinel = "SENTINEL-919283.777"
    store.append("hrv", {"item": "hrv", "timepoint": "2026-05-01",
                         "source": source, "value": sentinel}, root=store_root)

    http = _RecordingHttp(routes())
    oauth_pull.fetch(source, since="2026-07-01", staged_dir=tmp_path,
                     credential_reader=_cred(cred), http=http)

    assert http.calls, "the fetch must make at least one outbound call"
    seen_hosts = {urlparse(c["url"]).hostname for c in http.calls}
    assert seen_hosts == hosts, seen_hosts                 # only the vendor host(s); never the model lane
    for c in http.calls:
        blob = json.dumps({"u": c["url"], "h": c["headers"],
                           "b": c["body"].decode() if isinstance(c["body"], (bytes, bytearray)) else c["body"]})
        assert sentinel not in blob                        # 0 store content in any outbound request


def test_read_oura_records_follows_pagination(tmp_path):
    """S1: `_read_oura_records` follows Oura's `next_token` across pages — both pages' records land and
    the cursor is forwarded to the page-2 request. REDs if the page-follow is muted (only page 1)."""
    from scripts.ingest import oauth_pull

    page1 = {"data": [{"day": "2026-07-10", "score": 82}], "next_token": "OCURSOR"}
    page2 = {"data": [{"day": "2026-07-11", "score": 84}], "next_token": None}
    http = _PagingHttp(page1, page2, cursor_param="next_token", cursor="OCURSOR")
    headers = {"Authorization": "Bearer tok", "Accept": "application/json"}

    records = list(oauth_pull._read_oura_records(http, oauth_pull._OURA, "/daily_sleep", "oura",
                                                 headers, None))
    assert [r["day"] for r in records] == ["2026-07-10", "2026-07-11"]               # BOTH pages
    assert any("next_token=OCURSOR" in c["url"] for c in http.calls)                 # cursor -> page 2


def test_oura_read_carries_only_bearer_and_whitelisted_params(tmp_path):
    """P4 (a/d) for Oura: reads carry a Bearer header + only the delta cursor / paging params, no body."""
    from scripts.ingest import oauth_pull

    http = _RecordingHttp(_oura_routes())
    oauth_pull.fetch("oura", since="2026-07-01", staged_dir=tmp_path,
                     credential_reader=_cred(_OAUTH2_CRED), http=http)

    read_calls = [c for c in http.calls if "oauth/token" not in c["url"]]
    assert read_calls
    for c in read_calls:
        assert c["method"] == "GET"
        assert c["body"] in (None, b"", "")
        assert c["headers"].get("Authorization", "").startswith("Bearer ")
        qs = set(parse_qs(urlparse(c["url"]).query))
        assert qs.issubset({"start_date", "end_date", "next_token"})


# --- Garmin OAuth 1.0a signing: the KNOWN-ANSWER vector + a mutation-reds control (design §10.2) ---

# The canonical X / Twitter OAuth 1.0a worked example — its signature base string AND resulting
# HMAC-SHA1 signature are externally documented, so this is a genuine known-answer vector (not a
# tautology): a bug in percent-encoding, parameter sorting, or base-string joining reds it.
_TW_PARAMS = {
    "status": "Hello Ladies + Gentlemen, a signed OAuth request!",
    "include_entities": "true",
    "oauth_consumer_key": "xvz1evFS4wEEPTGEFPHBog",
    "oauth_nonce": "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg",
    "oauth_signature_method": "HMAC-SHA1",
    "oauth_timestamp": "1318622958",
    "oauth_token": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
    "oauth_version": "1.0",
}
_TW_URL = "https://api.twitter.com/1.1/statuses/update.json"
_TW_CONSUMER_SECRET = "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw"
_TW_TOKEN_SECRET = "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
_TW_BASE_STRING = (
    "POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fupdate.json&"
    "include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26"
    "oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26"
    "oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26"
    "oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26"
    "oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520"
    "a%2520signed%2520OAuth%2520request%2521"
)
_TW_SIGNATURE = "hCtSmYh+iHYCEqBWrE7C7hYmtUk="


def test_garmin_oauth1_base_string_matches_known_vector():
    """The OAuth 1.0a signature base string equals the externally-documented X / Twitter base string."""
    from scripts.ingest import oauth_pull

    assert oauth_pull._oauth1_base_string("POST", _TW_URL, _TW_PARAMS) == _TW_BASE_STRING


def test_garmin_oauth1_signature_matches_known_vector():
    """The OAuth 1.0a HMAC-SHA1 signature equals the documented X / Twitter value (known-answer)."""
    from scripts.ingest import oauth_pull

    sig = oauth_pull._oauth1_signature("POST", _TW_URL, _TW_PARAMS,
                                       _TW_CONSUMER_SECRET, _TW_TOKEN_SECRET)
    assert sig == _TW_SIGNATURE


def test_garmin_oauth1_base_string_mutation_reds_the_signature():
    """Mutation control: a one-token change to the base-string inputs changes the signature.

    Proves the known-answer assertion is failing-capable, not vacuous: flipping the HTTP method (a
    base-string component) yields a signature != the documented value, so a base-string construction
    bug would break the vector.
    """
    from scripts.ingest import oauth_pull

    mutated = oauth_pull._oauth1_signature("GET", _TW_URL, _TW_PARAMS,   # POST -> GET
                                           _TW_CONSUMER_SECRET, _TW_TOKEN_SECRET)
    assert mutated != _TW_SIGNATURE


def test_garmin_fetch_signs_every_read_with_the_verified_signer(tmp_path, monkeypatch):
    """The Garmin fetch signs every read with a deterministic OAuth 1.0a header from the verified signer.

    Pins a fixed nonce+timestamp (so the signature is deterministic), fetches, and asserts each read's
    `Authorization: OAuth ...` header embeds exactly the `oauth_signature` the (Twitter-anchored)
    `_oauth1_signature` computes for that request — so the fetch path wires the verified signer and a
    base-string bug in the fetch path reds here too.
    """
    from scripts.ingest import oauth_pull

    monkeypatch.setattr(oauth_pull, "_oauth1_nonce", lambda: "fixednonce")
    monkeypatch.setattr(oauth_pull, "_oauth1_timestamp", lambda: "1700000000")

    http = _RecordingHttp(_garmin_routes())
    oauth_pull.fetch("garmin", since=None, staged_dir=tmp_path,
                     credential_reader=_cred(_GARMIN_CRED), http=http)

    creds = {"consumer_key": "ck", "consumer_secret": "cs", "token": "tk", "token_secret": "ts"}
    oauth_params = {
        "oauth_consumer_key": "ck", "oauth_token": "tk", "oauth_signature_method": "HMAC-SHA1",
        "oauth_version": "1.0", "oauth_nonce": "fixednonce", "oauth_timestamp": "1700000000",
    }
    assert http.calls
    for c in http.calls:
        auth = c["headers"].get("Authorization", "")
        assert auth.startswith("OAuth ")
        base_url = c["url"].split("?", 1)[0]
        expected_sig = oauth_pull._oauth1_signature("GET", base_url, oauth_params,
                                                    creds["consumer_secret"], creds["token_secret"])
        assert f'oauth_signature="{oauth_pull._percent_encode(expected_sig)}"' in auth


def test_garmin_wire_scan_never_leaks_secret_outbound(tmp_path):
    """P4 (Garmin): the consumer/token SECRETS never appear in any outbound byte (only the signature).

    OAuth 1.0a signs with the secrets but transmits only the derived signature + the public oauth_*
    params. Distinctive secret values make the substring check meaningful: a signer that mistakenly
    emitted a secret would surface it here.
    """
    from scripts.ingest import oauth_pull

    cred = json.dumps({"consumer_key": "ck", "consumer_secret": "CONSUMER-SECRET-zzz",
                       "token": "tk", "token_secret": "TOKEN-SECRET-qqq"})
    http = _RecordingHttp(_garmin_routes())
    oauth_pull.fetch("garmin", since=None, staged_dir=tmp_path,
                     credential_reader=_cred(cred), http=http)

    assert http.calls
    for c in http.calls:
        blob = json.dumps({"u": c["url"], "h": c["headers"],
                           "b": c["body"].decode() if isinstance(c["body"], (bytes, bytearray)) else c["body"]})
        assert "CONSUMER-SECRET-zzz" not in blob
        assert "TOKEN-SECRET-qqq" not in blob


# --- S2: the Google rollup reader follows pagination (was single-response, contradicting the docstring) ---


def _google_single_endpoint_manifest():
    """A trimmed one-data-type Google manifest so a pagination test exercises one endpoint cleanly."""
    from scripts.ingest import oauth_pull

    return {**oauth_pull._GOOGLE_HEALTH,
            "endpoints": (("resting-heart-rate", ("restingHeartRate", "avg"), "rhr"),)}


def test_read_google_follows_pagination(tmp_path):
    """S2: `_read_google` follows Google's `nextPageToken` across pages — both pages' points land and
    the cursor is echoed in the page-2 request body. REDs pre-fix (the reader read one response only)."""
    from scripts.ingest import oauth_pull

    calls = []

    def seam(method, url, *, headers=None, body=None, timeout=None):
        calls.append({"url": url, "body": body})
        if "oauth2.googleapis.com/token" in url:
            return _resp(200, _TOKEN_OK)
        if json.loads(body).get("pageToken") == "PGCURSOR":
            return _resp(200, {"rollupDataPoints": [_g_point(11, "restingHeartRate", "avg", 50)]})
        return _resp(200, {"rollupDataPoints": [_g_point(10, "restingHeartRate", "avg", 47)],
                           "nextPageToken": "PGCURSOR"})

    rows = oauth_pull._read_google("google-health", _google_single_endpoint_manifest(), since=None,
                                   credential_reader=_cred(_OAUTH2_CRED), credential_writer=None, http=seam)
    assert [r["timepoint"] for r in rows] == ["2026-07-10", "2026-07-11"]        # BOTH pages
    assert [r["value"] for r in rows] == [47, 50]
    read_bodies = [json.loads(c["body"]) for c in calls if "token" not in c["url"]]
    assert any(b.get("pageToken") == "PGCURSOR" for b in read_bodies)            # cursor -> page 2 body


def test_read_google_single_response_terminates_without_crash(tmp_path):
    """S2: an absent `nextPageToken` terminates after one response (today's behavior is unchanged — no
    spurious page-2 request, no crash)."""
    from scripts.ingest import oauth_pull

    read_urls = []

    def seam(method, url, *, headers=None, body=None, timeout=None):
        if "oauth2.googleapis.com/token" in url:
            return _resp(200, _TOKEN_OK)
        read_urls.append(url)
        return _resp(200, {"rollupDataPoints": [_g_point(10, "restingHeartRate", "avg", 47)]})  # no token

    rows = oauth_pull._read_google("google-health", _google_single_endpoint_manifest(), since=None,
                                   credential_reader=_cred(_OAUTH2_CRED), credential_writer=None, http=seam)
    assert [r["value"] for r in rows] == [47]       # the single page landed
    assert len(read_urls) == 1                      # absent token -> one request, terminates (no change)


# --- TEST-1: honest absence — a null field / missing day yields NO fabricated row (per source) ---


def _oura_single_endpoint_manifest():
    """A trimmed one-collection Oura manifest so an honest-absence test exercises one endpoint cleanly."""
    from scripts.ingest import oauth_pull

    return {**oauth_pull._OURA, "endpoints": (("/daily_sleep", "day", {"score": "sleep"}),)}


def test_oura_honest_absence_null_score_and_missing_day():
    """TEST-1 (Oura inline guards): a null `score` and a missing `day` each yield NO row — only the
    present reading lands. REDs when `if value is not None` (a null-score row) or `if not day` (a
    timepoint="" row) is muted.
    """
    from scripts.ingest import oauth_pull

    def seam(method, url, *, headers=None, body=None, timeout=None):
        if "oauth/token" in url:
            return _resp(200, _TOKEN_OK)
        return _resp(200, {"data": [
            {"day": "2026-07-10", "score": 82},        # valid -> sleep 82
            {"day": "2026-07-11", "score": None},       # null score -> no row
            {"score": 90},                              # missing day -> no row
        ], "next_token": None})

    rows = oauth_pull._read_oura("oura", _oura_single_endpoint_manifest(), since=None,
                                 credential_reader=_cred(_OAUTH2_CRED), credential_writer=None, http=seam)
    assert rows == [{"item": "sleep", "timepoint": "2026-07-10", "value": 82}]


def test_garmin_honest_absence_null_field_and_missing_day(tmp_path):
    """TEST-1 (Garmin inline guards): a null field and a missing `calendarDate` each yield NO row — only
    the present reading lands. REDs when `if value is not None` (a null-stress row) or `if not day` (a
    timepoint=None row) is muted.
    """
    from scripts.ingest import oauth_pull

    routes = {
        "/dailies": (200, [
            {"calendarDate": "2026-07-10", "restingHeartRateInBeatsPerMinute": 48,
             "averageStressLevel": None},                                     # rhr present, stress null
            {"restingHeartRateInBeatsPerMinute": 50},                         # missing calendarDate -> no row
        ]),
        "/hrv": (200, []), "/sleeps": (200, []), "/epochs": (200, []),
    }
    staged = oauth_pull.fetch("garmin", since=None, staged_dir=tmp_path,
                              credential_reader=_cred(_GARMIN_CRED), http=_RecordingHttp(routes))
    assert json.loads(staged.read_text()) == [
        {"item": "rhr", "timepoint": "2026-07-10", "value": 48},
    ]


def test_google_honest_absence_null_value_and_missing_day():
    """TEST-1 (Google inline guard): a null value and a missing `civilStartTime` each yield NO row — only
    the present reading lands. REDs when the `if day and value is not None` guard is muted (a value-None
    row or a timepoint-None row appears).
    """
    from scripts.ingest import oauth_pull

    def seam(method, url, *, headers=None, body=None, timeout=None):
        if "oauth2.googleapis.com/token" in url:
            return _resp(200, _TOKEN_OK)
        return _resp(200, {"rollupDataPoints": [
            _g_point(10, "restingHeartRate", "avg", 47),                       # valid -> rhr 47
            {"civilStartTime": {"date": {"year": 2026, "month": 7, "day": 11}},
             "restingHeartRate": {"avg": None}},                              # null value -> no row
            {"restingHeartRate": {"avg": 50}},                               # missing civilStartTime -> no row
        ]})

    rows = oauth_pull._read_google("google-health", _google_single_endpoint_manifest(), since=None,
                                   credential_reader=_cred(_OAUTH2_CRED), credential_writer=None, http=seam)
    assert rows == [{"item": "rhr", "timepoint": "2026-07-10", "value": 47}]


# --- the cloud adapters parse the staged rows (pure file parsers, no network) ---


@pytest.mark.parametrize("source", list(_SOURCES))
def test_cloud_adapter_parses_staged_rows(source, tmp_path):
    """Each Build-B cloud adapter maps the staged {item, timepoint, value} rows to Line-Field-Set readings.

    The adapter owns the source tag (adds `source`), like every wired adapter; it is a pure file parser
    (no network / no OAuth), fixture-testable with a staged file.
    """
    staged = tmp_path / f"{source}.json"
    staged.write_text(json.dumps([
        {"item": "hrv", "timepoint": "2026-07-10", "value": 55.0},
        {"item": "rhr", "timepoint": "2026-07-10", "value": 48},
    ]))

    readings = list(_adapter(source).read_readings(staged))
    assert readings == [
        {"item": "hrv", "timepoint": "2026-07-10", "source": source, "value": 55.0},
        {"item": "rhr", "timepoint": "2026-07-10", "source": source, "value": 48},
    ]
