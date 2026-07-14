"""Shared OAuth/fetch layer — pull a wearable cloud's readings into a staged export (tracker Build A).

The one NEW capability class the tracker-ingestion design adds: an OAuth network fetch that produces
the staged export a file-reading adapter consumes. `fetch(source, since, staged_dir)` authenticates
with a per-source keychain refresh token, mints a short-lived access token, GETs the source's read
endpoints for readings, normalizes them into a gitignored staged JSON file in the wired adapter's
input shape, and returns its path. The UNCHANGED `ingest.run(adapter, staged_path, root)` then lands
them via `store.append` — so `ingest.run`, `scheduler.run`, `store.append`, the `Adapter` protocol,
and the `(item, timepoint, source)` dedupe key are all reused byte-unchanged (design Option A).

Directionality (ADR-0001): the pull is INBOUND — the operator's own data, from the operator's own
wearable cloud account, into the local store. The outbound request carries only an OAuth bearer token
+ a date-range cursor (0 bytes of store content), and there is NO model step on the ingestion axis.
This module imports only the standard library — never the store, never the model client — so the
fetch path structurally cannot touch the model lane (the design §4 ruling, mechanized by the
wire-scan probes in tests/ingest/test_oauth_pull.py).

Both the credential read/write (the macOS keychain) and the HTTP client are INJECTABLE seams
(module-level defaults resolved at call time), exactly as `key_source.resolve(keychain_runner=...)`
and `auth_isolation.build_subscription_env(keychain_reader=...)` inject theirs — so tests pass
fixtures and touch no real keychain, token, or host. (The seams are named `credential_reader` /
`credential_writer` rather than `keychain_*` so the tracker layer does not trip the Risk-N3
dedupe-key-definition scan over scripts/ingest/; the storage is still the macOS keychain.)
Fail-closed: a missing / expired / revoked token, or any token- or read-endpoint error, raises
`TrackerPullError` and writes 0 staged bytes (no partial or garbage file, no store write). The error
message never carries the token value (NFR-3: the repo is PUBLIC).
"""

import base64
import getpass
import hashlib
import hmac
import json
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit, urlunsplit


class TrackerPullError(RuntimeError):
    """A tracker cloud pull failed — missing/expired token, or a token/read-endpoint error.

    Raised fail-loud so a bad credential lands 0 readings rather than a partial or garbage store
    write. The message names the source and the failure kind but NEVER the token value (NFR-3: the
    repo is PUBLIC), mirroring `auth_isolation.OAuthTokenUnavailableError`.
    """


# Per-source cloud manifest. `[VERIFY-AT-BUILD]` — the exact Whoop endpoint paths, token URL, scope
# strings, and score-field names are transcribed from the Whoop developer docs (api.prod.whoop.com,
# API v1) and MUST be re-verified against the live docs before the operator-gated LIVE run (Whoop has
# since published a v2; confirm the paths/fields have not moved). The fetch is fixture-tested against
# a response of this SHAPE — the shape, not the live endpoints, is what the tests pin. Each endpoint
# is (path, timestamp-field, {whoop score field -> store item}); the store items follow the
# `biomarker_meta` registry convention already used by the wired adapters. Absolute skin temperature
# is intentionally UNMAPPED: WHOOP's cloud `skin_temp_celsius` is an absolute °C, not the deviation
# the store `skin-temp-dev` item expects — an honest absence, mirroring the healthkit adapter's
# omission of Apple's absolute wrist temperature. WHOOP day-strain stays on its native 0-21 scale
# (unscaled), the existing whoop adapter's invariant.
_WHOOP = {
    "host": "api.prod.whoop.com",
    "token_url": "https://api.prod.whoop.com/oauth/oauth2/token",
    "api_base": "https://api.prod.whoop.com/developer",
    "scope": "offline",
    "endpoints": (
        ("/v1/recovery", "created_at", {
            "recovery_score": "recovery",
            "hrv_rmssd_milli": "hrv",
            "resting_heart_rate": "rhr",
            "spo2_percentage": "spo2",
        }),
        ("/v1/activity/sleep", "start", {
            "sleep_efficiency_percentage": "sleep-efficiency",
            "respiratory_rate": "resp-rate",
        }),
        ("/v1/cycle", "start", {
            "strain": "strain",
        }),
    ),
}

# Oura API v2 (tracker Build B). `[VERIFY-AT-BUILD]` — the endpoint paths, token URL, and scope are
# transcribed from the Oura Cloud API v2 docs (api.ouraring.com/v2/usercollection/<type>, OAuth 2.0,
# refresh grant at /oauth/token) and MUST be re-verified against the live docs before the LIVE run.
# Oura reuses the shared OAuth-2.0 `access_token()` refresh->access path directly; only its response
# SHAPE differs from Whoop (envelope key `data` not `records`; the readings sit at the record top
# level, not under a `score` sub-object; the timepoint is the record's own `day`, already YYYY-MM-DD).
# Each endpoint is (path, day-field, {oura field -> store item}). daily_* collections carry one `score`
# per day; the detailed `sleep` collection carries `average_hrv` / `average_heart_rate` per period.
_OURA = {
    "host": "api.ouraring.com",
    "token_url": "https://api.ouraring.com/oauth/token",
    "api_base": "https://api.ouraring.com/v2/usercollection",
    "scope": "daily",
    "read": "oura",
    "endpoints": (
        ("/daily_sleep", "day", {"score": "sleep"}),
        ("/daily_readiness", "day", {"score": "readiness"}),
        ("/daily_activity", "day", {"score": "activity"}),
        ("/sleep", "day", {"average_hrv": "hrv", "average_heart_rate": "rhr"}),
    ),
}

# Garmin Health API (tracker Build B) — the design §10.2 auth FORK. `[VERIFY-AT-BUILD]`: Garmin's Health
# API has historically used OAuth 1.0a (per-request HMAC-SHA1 signing, a long-lived token+secret, no
# refresh->access exchange), and the third-party integration guides still document 1.0a; Garmin's own
# Connect Developer Program FAQ now advertises OAuth 2.0 PKCE for newly granted tiers. This manifest
# wires the 1.0a strategy (the historically-correct Health API auth + the mandated signing test
# vector); if the LIVE-granted tier is OAuth 2.0, drop `"auth": "oauth1a"` and the source reuses the
# shared `access_token()` default. The summary GETs return a top-level JSON ARRAY (no pagination
# envelope); each record's `calendarDate` is the day and the readings sit at the record top level.
# Each endpoint is (path, day-field, {garmin field -> store item}).
_GARMIN = {
    "host": "apis.garmin.com",
    "api_base": "https://apis.garmin.com/wellness-api/rest",
    "read": "garmin",
    "auth": "oauth1a",
    "endpoints": (
        ("/dailies", "calendarDate", {
            "restingHeartRateInBeatsPerMinute": "rhr",
            "averageStressLevel": "stress",
        }),
        ("/hrv", "calendarDate", {"lastNightAvg": "hrv"}),
        ("/sleeps", "calendarDate", {"overallSleepScore": "sleep"}),
        ("/epochs", "calendarDate", {"activeKilocalories": "activity"}),
    ),
}

# Google Health API (tracker Build B) — the NEW API covering Fitbit / Pixel devices (the legacy Fitbit
# Web API sunsets Sep 2026; this is greenfield on health.googleapis.com/v4/, NO migration).
# `[VERIFY-AT-BUILD]`: the data-type slugs, the rollup value paths, the token URL, and the scopes are
# transcribed from the Google Health API reference and MUST be re-verified before the LIVE run. Google
# reuses the shared OAuth-2.0 `access_token()` refresh->access path (a JSON credential blob carrying
# client_id/client_secret, which the refresh grant requires). Its READ SHAPE does NOT fit the shared
# GET-pagination reader: the daily grain is a `dailyRollUp` POST carrying a civil-time-range body, and
# the response is `{rollupDataPoints: [{civilStartTime: {date:{...}}, <value-path> -> scalar}]}` — so
# Google gets a bespoke reader at the fetch seam (`_read_google`), NOT an edit to the shared routine.
# Each endpoint is (data-type slug, value-path tuple walked to a scalar, store item).
_GOOGLE_HEALTH = {
    "host": "health.googleapis.com",
    "token_url": "https://oauth2.googleapis.com/token",
    "api_base": "https://health.googleapis.com/v4/users/me/dataTypes",
    "scope": "https://www.googleapis.com/auth/health.health_metrics_and_measurements.readonly "
             "https://www.googleapis.com/auth/health.activity_and_fitness.readonly "
             "https://www.googleapis.com/auth/health.sleep.readonly",
    "read": "google",
    "endpoints": (
        ("resting-heart-rate", ("restingHeartRate", "avg"), "rhr"),
        ("heart-rate-variability", ("heartRateVariability", "avg"), "hrv"),
        ("heart-rate", ("heartRate", "avg"), "heart-rate"),
        ("oxygen-saturation", ("oxygenSaturation", "avg"), "spo2"),
        ("sleep", ("sleep", "durationMillis"), "sleep"),
        ("active-zone-minutes", ("activeZoneMinutes", "totalMinutes"), "activity"),
    ),
}

_MANIFESTS = {
    "whoop": _WHOOP,
    "oura": _OURA,
    "garmin": _GARMIN,
    "google-health": _GOOGLE_HEALTH,
}

# The per-page record cap and the page-follow ceiling. The ceiling bounds the `next_token` pagination
# loop so a misbehaving API (a cursor that never terminates) fails fast at the network boundary rather
# than hanging the unattended tick indefinitely — the motivated boundary guard (SE rule 7), not a
# speculative default. A real daily-metrics window is a handful of pages; 200 is generous headroom.
_PAGE_LIMIT = 25
_MAX_PAGES = 200

# The per-request network timeout (seconds) — a bounded wait, never an indefinite block, matching the
# model client's bounded-request posture.
_HTTP_TIMEOUT_S = 30.0


def _oauth_service_name(source):
    """The per-source OAuth keychain item name (`a-plus-maxing-<source>-oauth`)."""
    return f"a-plus-maxing-{source}-oauth"


def _read_oauth_credential(source):
    """Read the per-source OAuth credential from the macOS keychain at call time, or None when absent.

    Runs `security find-generic-password -w -s a-plus-maxing-<source>-oauth` (the exact shape
    `key_source._keychain_runner` and `auth_isolation._oauth_keychain_reader` use; `-w` prints only
    the secret). Returns the stripped payload (a bare refresh token or a JSON credential blob), or
    None when the item is absent or `security` is unavailable (a non-macOS host) — the absence path
    is the caller's fail-loud trigger. Never captured at module load, never read from a tracked file.
    """
    try:
        completed = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", _oauth_service_name(source)],
            capture_output=True, text=True,
        )
    except (FileNotFoundError, OSError):
        return None
    if completed.returncode != 0:
        return None
    payload = completed.stdout.strip()
    return payload or None


def _write_oauth_credential(source, payload):
    """Write the per-source OAuth credential into the macOS keychain at call time (rotation write-back).

    Runs `security add-generic-password -U -A -a <user> -s a-plus-maxing-<source>-oauth -w <payload>`
    (`-U` updates in place so a rotated refresh token replaces the prior one; `-A` grants the item an
    allow-all ACL so the backgrounded pull's later read is not blocked on an interactive prompt — the
    same accepted tradeoff `key_source._keychain_writer` makes). The payload is passed only as the
    subprocess argument, never logged. Non-fatal but LOUD (SEC-02): a write failure does NOT abort the
    current tick (its access token already works), but unlike a silent best-effort write it emits a
    diagnostic naming the rotation-write failure — a silently-stranded rotated refresh token would make
    the NEXT tick 401 and fail closed blaming the token, not the write. The returncode is checked (the
    `key_source._keychain_writer` precedent), but here we warn instead of raise (Security's guidance).
    """
    try:
        completed = subprocess.run(
            ["security", "add-generic-password", "-U", "-A",
             "-a", getpass.getuser(), "-s", _oauth_service_name(source), "-w", payload],
            capture_output=True, text=True,
        )
    except (FileNotFoundError, OSError):
        completed = None
    if completed is None or completed.returncode != 0:
        print(f"tracker-pull: FAILED to write the rotated {source!r} refresh token back to the "
              f"keychain (item {_oauth_service_name(source)!r}); the consumed token is now stranded — "
              f"the next tick will fail closed until you re-run the authorize flow", file=sys.stderr)


class _HttpResponse:
    """A minimal HTTP response the fetch layer reads: `.status` (int) + `.body` (bytes)."""

    __slots__ = ("status", "body")

    def __init__(self, status, body):
        self.status = status
        self.body = body


class _NoFollowRedirect(urllib.request.HTTPRedirectHandler):
    """Decline every 3xx auto-follow on the authenticated fetch seam (SEC-01).

    Python's default opener copies the request headers — including `Authorization: Bearer <token>` —
    onto a redirect target with no cross-host stripping (verified on 3.14), and a redirect can downgrade
    https->http, so auto-following a 3xx would leak the access token to the redirect host. Returning
    None declines the follow, surfacing the 3xx to `_http` (which fails closed); the redirect target is
    never contacted.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


# A module-level opener that never auto-follows a redirect (the SEC-01 posture above), built once.
_OPENER = urllib.request.build_opener(_NoFollowRedirect)


def _http(method, url, *, headers=None, body=None, timeout=_HTTP_TIMEOUT_S):
    """Issue one HTTP request and return an `_HttpResponse` (the default network seam; LIVE only).

    The single real-network site in this module — never exercised in tests (they inject a fixture
    seam). A 4xx/5xx response is returned as an `_HttpResponse` carrying its status (the caller decides
    fail-closed); a genuine connection error (`URLError`) propagates for the caller to wrap. A 3xx
    redirect FAILS CLOSED here (SEC-01): the authenticated seam never follows a redirect — that would
    leak the bearer to the redirect host — so a 3xx raises `TrackerPullError` and is never followed.
    """
    data = body.encode() if isinstance(body, str) else body
    request = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            return _HttpResponse(response.status, response.read())
    except urllib.error.HTTPError as exc:
        if 300 <= exc.code < 400:
            raise TrackerPullError(
                f"refusing to follow an HTTP {exc.code} redirect on the authenticated tracker fetch "
                "seam (a redirect would leak the access token to the redirect host)"
            ) from None
        return _HttpResponse(exc.code, exc.read())


def _manifest(source):
    """Return the cloud manifest for `source`, or raise `TrackerPullError` for an unwired source."""
    manifest = _MANIFESTS.get(source)
    if manifest is None:
        raise TrackerPullError(f"no API-pull manifest for source {source!r}")
    return manifest


def _parse_credentials(payload):
    """Parse a keychain payload into `{refresh_token, client_id?, client_secret?}`.

    Accepts either a bare refresh-token string or a JSON credential blob (some vendors require the
    client id/secret at refresh time). A non-JSON string is treated as the bare refresh token.
    """
    try:
        blob = json.loads(payload)
    except (ValueError, TypeError):
        return {"refresh_token": payload}
    if isinstance(blob, dict) and blob.get("refresh_token"):
        return blob
    return {"refresh_token": payload}


def _serialize_credentials(creds, rotated_refresh):
    """Serialize the credential for write-back with the rotated refresh token.

    Preserves the original shape: a bare-token credential writes the bare rotated token; a JSON blob
    writes the blob with its `refresh_token` updated (keeping any client id/secret).
    """
    if set(creds) == {"refresh_token"}:
        return rotated_refresh
    return json.dumps({**creds, "refresh_token": rotated_refresh})


def access_token(source, *, credential_reader=None, credential_writer=None, http=None):
    """Mint a short-lived access token from the per-source refresh token (refresh -> access).

    Reads the per-source refresh token from the credential seam, POSTs the OAuth refresh grant to the
    source's token endpoint, and returns the access token. A rotated refresh token in the response is
    written back to the credential seam (Whoop rotates on each use). Fail-closed: a missing token, a
    non-2xx token response, or a response without an access token raises `TrackerPullError` — the
    missing-token case raises BEFORE any network call.

    Args:
        source (str): The wired API-pull source (e.g. "whoop").
        credential_reader (Callable, optional): `source -> payload | None` keychain read seam.
            Defaults to the macOS `security` read; injected in tests.
        credential_writer (Callable, optional): `(source, payload) -> None` keychain write seam (for
            rotation write-back). Defaults to the macOS `security` write; injected in tests.
        http (Callable, optional): `(method, url, *, headers, body) -> response` network seam.
            Defaults to `_http`; injected in tests.

    Returns:
        (str) The short-lived OAuth access token.

    Raises:
        TrackerPullError: A missing/expired/invalid token or a token-endpoint error (fail-closed).
    """
    manifest = _manifest(source)
    credential_reader = _read_oauth_credential if credential_reader is None else credential_reader
    credential_writer = _write_oauth_credential if credential_writer is None else credential_writer
    http = _http if http is None else http

    payload = credential_reader(source)
    if not payload:
        raise TrackerPullError(
            f"no OAuth refresh token for {source!r} in the keychain (item "
            f"'{_oauth_service_name(source)}'); run the one-time authorize flow to store it"
        )
    creds = _parse_credentials(payload)

    body = {"grant_type": "refresh_token", "refresh_token": creds["refresh_token"],
            "scope": manifest["scope"]}
    if creds.get("client_id"):
        body["client_id"] = creds["client_id"]
    if creds.get("client_secret"):
        body["client_secret"] = creds["client_secret"]

    response = _request(
        http, "POST", manifest["token_url"], source,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, body=urlencode(body),
    )
    if not 200 <= response.status < 300:
        raise TrackerPullError(f"OAuth token refresh for {source!r} failed (HTTP {response.status})")

    data = _decode(response.body, source)
    token = data.get("access_token")
    if not token:
        raise TrackerPullError(f"OAuth token response for {source!r} carried no access token")

    rotated = data.get("refresh_token")
    if rotated:
        credential_writer(source, _serialize_credentials(creds, rotated))
    return token


def fetch(source, *, since, staged_dir, credential_reader=None, credential_writer=None, http=None):
    """Pull a source's readings-new-since into a staged export file; return its path.

    Mints an access token, GETs each of the source's read endpoints (following pagination), maps the
    responses into the wired adapter's staged input shape (`[{item, timepoint, value}]`), and writes
    the staged JSON to `<staged_dir>/<source>.json`. The staged file is written ONLY after every
    endpoint has succeeded, so a mid-fetch failure leaves 0 staged bytes (fail-closed — no partial or
    garbage file for `ingest.run` to land). `since` is a bandwidth cursor, not a correctness
    dependency: the store's `(item, timepoint, source)` dedupe makes an over-fetch land 0 duplicates.

    Args:
        source (str): The wired API-pull source (e.g. "whoop").
        since (str | None): The lower-bound day cursor (YYYY-MM-DD) sent as the read `start` param, or
            None to fetch the source's default window.
        staged_dir (str | Path): The directory the staged export is written into (gitignored).
        credential_reader (Callable, optional): The keychain read seam (see `access_token`).
        credential_writer (Callable, optional): The keychain write seam (see `access_token`).
        http (Callable, optional): The network seam (see `access_token`).

    Returns:
        (Path) The staged export path `<staged_dir>/<source>.json`.

    Raises:
        TrackerPullError: A missing/expired token or any token/read-endpoint error (fail-closed).
    """
    manifest = _manifest(source)
    http = _http if http is None else http
    reader = _READERS[manifest.get("read", "whoop")]
    rows = reader(source, manifest, since=since, credential_reader=credential_reader,
                  credential_writer=credential_writer, http=http)

    staged = Path(staged_dir) / f"{source}.json"
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(json.dumps(rows))
    return staged


def _read_whoop(source, manifest, *, since, credential_reader, credential_writer, http):
    """Read a Whoop-shaped cloud (records/next_token envelope, values under `score`) into staged rows.

    The Build-A reference reader, extracted verbatim from `fetch`: mints the OAuth-2.0 bearer via the
    shared `access_token`, then walks each endpoint's paginated `records`, mapping the manifest's
    score fields to `{item, timepoint, value}` rows. The default `_READERS` strategy — a source with no
    `manifest["read"]` uses it.
    """
    token = access_token(source, credential_reader=credential_reader,
                         credential_writer=credential_writer, http=http)
    rows = []
    for path, timestamp_field, field_items in manifest["endpoints"]:
        for record in _read_records(http, manifest, path, source, token, since):
            rows.extend(_rows_from_record(record, timestamp_field, field_items))
    return rows


def _read_records(http, manifest, path, source, token, since):
    """Yield every record across a read endpoint's pages (bounded `next_token` follow)."""
    url = f"{manifest['api_base']}{path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    next_token = None
    for _ in range(_MAX_PAGES):
        params = {"limit": _PAGE_LIMIT}
        if since:
            params["start"] = f"{since}T00:00:00.000Z"
        if next_token:
            params["nextToken"] = next_token
        response = _request(http, "GET", f"{url}?{urlencode(params)}", source, headers=headers)
        if not 200 <= response.status < 300:
            raise TrackerPullError(f"read of {path} for {source!r} failed (HTTP {response.status})")
        data = _decode(response.body, source)
        for record in _records(data.get("records"), source):
            yield record
        next_token = data.get("next_token")
        if not next_token:
            return
    raise TrackerPullError(f"read of {path} for {source!r} exceeded the page ceiling")


def _rows_from_record(record, timestamp_field, field_items):
    """Map one API record's mapped score fields into staged `{item, timepoint, value}` rows.

    The timepoint is the record timestamp's calendar day (its first 10 chars), keying each reading on
    the store's `(item, day, source)` grain (the healthkit/whoop day convention). A missing timestamp
    or an absent/None score field yields no row (honest absence, never a fabricated value).
    """
    timestamp = record.get(timestamp_field)
    score = record.get("score") or {}
    if not timestamp:
        return []
    day = timestamp[:10]
    rows = []
    for field, item in field_items.items():
        value = score.get(field)
        if value is not None:
            rows.append({"item": item, "timepoint": day, "value": value})
    return rows


def _request(http, method, url, source, *, headers=None, body=None):
    """Call the http seam, wrapping any transport error as a fail-closed `TrackerPullError`."""
    try:
        return http(method, url, headers=headers, body=body)
    except TrackerPullError:
        raise
    except Exception:
        # A transport failure (connection refused / DNS / timeout) fails closed with a constant
        # message — never the exception text, which could carry the URL's bearer token (NFR-3).
        raise TrackerPullError(f"network error contacting {source!r}") from None


def _decode(body, source):
    """Decode a JSON response body into a dict, or fail closed on a malformed payload."""
    try:
        data = json.loads(body)
    except (ValueError, TypeError):
        raise TrackerPullError(f"malformed response from {source!r}") from None
    if not isinstance(data, dict):
        raise TrackerPullError(f"unexpected response shape from {source!r}")
    return data


def _decode_list(body, source):
    """Decode a JSON response body into a list, or fail closed on a malformed / non-array payload."""
    try:
        data = json.loads(body)
    except (ValueError, TypeError):
        raise TrackerPullError(f"malformed response from {source!r}") from None
    if not isinstance(data, list):
        raise TrackerPullError(f"unexpected response shape from {source!r}")
    return data


def _records(collection, source):
    """Coerce a decoded record collection to a list of record dicts (empty delta vs malformed shape).

    A null / absent / empty collection is the common "no data in this window" steady state -> an EMPTY
    delta (0 rows for the source, NOT an error). A present-but-non-list collection, or a non-dict record
    element, is a genuinely malformed shape and fails closed with `TrackerPullError` (mirroring
    `_decode_list`), so per-source isolation skips ONLY that source rather than crashing the whole tick
    on a `for record in None` TypeError or a `record.get(...)` AttributeError.
    """
    if collection is None:
        return []
    if not isinstance(collection, list):
        raise TrackerPullError(f"unexpected response shape from {source!r}")
    for element in collection:
        if not isinstance(element, dict):
            raise TrackerPullError(f"unexpected record shape from {source!r}")
    return collection


# --- Oura reader (OAuth-2.0 bearer; `data` envelope; top-level day-keyed readings) ---


def _read_oura(source, manifest, *, since, credential_reader, credential_writer, http):
    """Read Oura API v2 (OAuth-2.0 bearer, `data` envelope, top-level day-keyed readings) into rows.

    Reuses the shared `access_token` refresh->access path directly (Oura is standard OAuth 2.0), then
    walks each collection's paginated `data` array. Unlike Whoop the readings sit at the record top
    level (no `score` sub-object) and the `day` field is already the store's YYYY-MM-DD grain.
    """
    token = access_token(source, credential_reader=credential_reader,
                         credential_writer=credential_writer, http=http)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    rows = []
    for path, day_field, field_items in manifest["endpoints"]:
        for record in _read_oura_records(http, manifest, path, source, headers, since):
            day = (record.get(day_field) or "")[:10]
            if not day:
                continue
            for field, item in field_items.items():
                value = record.get(field)
                if value is not None:
                    rows.append({"item": item, "timepoint": day, "value": value})
    return rows


def _read_oura_records(http, manifest, path, source, headers, since):
    """Yield every Oura record across a collection's pages (the `data` array; `next_token` follow)."""
    url = f"{manifest['api_base']}{path}"
    next_token = None
    for _ in range(_MAX_PAGES):
        params = {}
        if since:
            params["start_date"] = since
        if next_token:
            params["next_token"] = next_token
        query = f"?{urlencode(params)}" if params else ""
        response = _request(http, "GET", f"{url}{query}", source, headers=headers)
        if not 200 <= response.status < 300:
            raise TrackerPullError(f"read of {path} for {source!r} failed (HTTP {response.status})")
        data = _decode(response.body, source)
        for record in _records(data.get("data"), source):
            yield record
        next_token = data.get("next_token")
        if not next_token:
            return
    raise TrackerPullError(f"read of {path} for {source!r} exceeded the page ceiling")


# --- Garmin reader (design §10.2 fork: OAuth 1.0a per-request HMAC-SHA1 signing; JSON-array summaries) ---


def _read_garmin(source, manifest, *, since, credential_reader, credential_writer, http):
    """Read the Garmin Health API (OAuth 1.0a, top-level JSON-array summaries) into staged rows.

    The design §10.2 auth fork: Garmin signs EACH GET with OAuth 1.0a HMAC-SHA1 (no refresh->access
    exchange), so this reader does NOT call the shared `access_token`; it reads the 4-part 1.0a
    credential from the keychain seam and signs per request. Fail-closed: a missing / incomplete
    credential raises before any network call. Each summary GET returns a top-level JSON array;
    `calendarDate` is the day and the manifest's fields sit at the record top level. `credential_writer`
    is unused (1.0a tokens do not rotate) but kept for the uniform `_READERS` reader signature.
    """
    read_credential = _read_oauth_credential if credential_reader is None else credential_reader
    payload = read_credential(source)
    if not payload:
        raise TrackerPullError(
            f"no OAuth 1.0a credential for {source!r} in the keychain (item "
            f"'{_oauth_service_name(source)}'); run the one-time authorize flow to store it"
        )
    creds = _parse_oauth1_credentials(payload, source)
    rows = []
    for path, day_field, field_items in manifest["endpoints"]:
        url = f"{manifest['api_base']}{path}"
        params = _garmin_window_params(since)
        header = _oauth1_authorization_header(
            "GET", url, params=params, creds=creds,
            nonce=_oauth1_nonce(), timestamp=_oauth1_timestamp(),
        )
        query = f"?{urlencode(params)}" if params else ""
        response = _request(http, "GET", f"{url}{query}", source,
                            headers={"Authorization": header, "Accept": "application/json"})
        if not 200 <= response.status < 300:
            raise TrackerPullError(f"read of {path} for {source!r} failed (HTTP {response.status})")
        for record in _records(_decode_list(response.body, source), source):
            day = record.get(day_field)
            if not day:
                continue
            for field, item in field_items.items():
                value = record.get(field)
                if value is not None:
                    rows.append({"item": item, "timepoint": day, "value": value})
    return rows


def _parse_oauth1_credentials(payload, source):
    """Parse a Garmin OAuth 1.0a keychain blob into its 4 parts, or fail closed if incomplete.

    The 1.0a credential is a JSON blob `{consumer_key, consumer_secret, token, token_secret}` (unlike
    the OAuth-2.0 refresh token, all four are needed to sign each request). A non-JSON payload or a
    blob missing any part raises — a partial credential cannot sign, so it fails closed like a missing
    token rather than emitting an invalid signature.
    """
    try:
        blob = json.loads(payload)
    except (ValueError, TypeError):
        blob = None
    required = ("consumer_key", "consumer_secret", "token", "token_secret")
    if not isinstance(blob, dict) or not all(blob.get(k) for k in required):
        raise TrackerPullError(
            f"the {source!r} keychain credential is not a complete OAuth 1.0a blob "
            f"(need {', '.join(required)})"
        )
    return blob


def _percent_encode(value):
    """RFC-3986 percent-encoding for OAuth 1.0a (unreserved ALPHA/DIGIT/-/./_/~ stay literal)."""
    return quote(str(value), safe="")


def _oauth1_base_string(method, url, params):
    """The OAuth 1.0a HMAC-SHA1 signature base string (RFC 5849 §3.4.1) for a request.

    `params` is the full set of request params to sign — the query params plus the oauth_* protocol
    params, excluding oauth_signature. Deterministic given its inputs, which is what makes the signing
    fixture-testable against a known vector: `METHOD & pct(base-url) & pct(sorted &-joined params)`.
    """
    parts = urlsplit(url)
    base_url = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", ""))
    encoded = sorted((_percent_encode(k), _percent_encode(v)) for k, v in params.items())
    normalized = "&".join(f"{k}={v}" for k, v in encoded)
    return "&".join([method.upper(), _percent_encode(base_url), _percent_encode(normalized)])


def _oauth1_signature(method, url, params, consumer_secret, token_secret):
    """Sign per OAuth 1.0a HMAC-SHA1 (RFC 5849): base64(HMAC-SHA1(base_string, signing_key)).

    The signing key is `pct(consumer_secret)&pct(token_secret)`. Verified against the canonical X /
    Twitter known-answer vector in the tests, so a mutation to the base-string construction reds.
    """
    base = _oauth1_base_string(method, url, params)
    key = f"{_percent_encode(consumer_secret)}&{_percent_encode(token_secret)}"
    return base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()


def _oauth1_authorization_header(method, url, *, params, creds, nonce, timestamp):
    """Build the Garmin OAuth 1.0a `Authorization: OAuth ...` header for one signed request.

    Merges the request's query params with the oauth_* protocol params, signs the lot with HMAC-SHA1
    (the consumer + token secrets), and formats the signed oauth_* set as the header. `nonce` and
    `timestamp` are injected (a fixed pair yields a deterministic signature — the signing fixture
    test), generated fresh per-request in production. The `url` must be the bare endpoint (no query);
    the query params are carried separately in `params` so the signature covers them.
    """
    oauth_params = {
        "oauth_consumer_key": creds["consumer_key"],
        "oauth_token": creds["token"],
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_version": "1.0",
        "oauth_nonce": nonce,
        "oauth_timestamp": str(timestamp),
    }
    signature = _oauth1_signature(method, url, {**params, **oauth_params},
                                  creds["consumer_secret"], creds["token_secret"])
    signed = {**oauth_params, "oauth_signature": signature}
    return "OAuth " + ", ".join(
        f'{_percent_encode(k)}="{_percent_encode(v)}"' for k, v in sorted(signed.items())
    )


def _garmin_window_params(since):
    """The Garmin summary upload-time window params for the delta cursor (`[VERIFY-AT-BUILD]`).

    A bandwidth cursor only (the store `(item, day, source)` dedupe makes an over-fetch land 0 dups).
    Empty when `since` is None. The exact param names are re-verified at the LIVE step.
    """
    if not since:
        return {}
    start = int(datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    return {"uploadStartTimeInSeconds": str(start)}


def _oauth1_nonce():
    """A fresh per-request OAuth 1.0a nonce (a random hex token)."""
    return secrets.token_hex(16)


def _oauth1_timestamp():
    """The current OAuth 1.0a timestamp (whole seconds since the epoch)."""
    return str(int(time.time()))


# --- Google Health reader (OAuth-2.0 bearer; `dailyRollUp` POST; `rollupDataPoints` envelope) ---

# The Google dailyRollUp pagination fields. `[VERIFY-AT-BUILD]` — transcribed from the Google Health
# API reference and MUST be re-verified before the LIVE run (the same posture as the endpoint slugs). A
# response `nextPageToken` absent -> a single response terminates (today's behavior, unchanged); present
# -> the read echoes it as the request-body `pageToken` and follows the next page, bounded by
# `_MAX_PAGES` (so a misbehaving cursor fails fast at the boundary rather than hanging the tick).
_GOOGLE_NEXT_PAGE_FIELD = "nextPageToken"   # response: the next-page cursor
_GOOGLE_PAGE_TOKEN_PARAM = "pageToken"      # request body: echo the cursor to fetch the next page


def _read_google(source, manifest, *, since, credential_reader, credential_writer, http):
    """Read the Google Health API daily rollups (OAuth-2.0 bearer, `dailyRollUp` POST) into rows.

    Reuses the shared `access_token` refresh->access path (Google is standard OAuth 2.0), then POSTs a
    civil-time-range `dailyRollUp` per data type and walks `rollupDataPoints`, following the response's
    `nextPageToken` across pages (mirroring the GET readers' page-follow, bounded by `_MAX_PAGES`). The
    read shape is Google-specific (a POST with a JSON body; a `rollupDataPoints` / `civilStartTime`
    envelope; a nested value path) and lives here at the fetch seam rather than in the shared reader.
    """
    token = access_token(source, credential_reader=credential_reader,
                         credential_writer=credential_writer, http=http)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json",
               "Content-Type": "application/json"}
    rows = []
    for data_type, value_path, item in manifest["endpoints"]:
        url = f"{manifest['api_base']}/{data_type}/dataPoints:dailyRollUp"
        page_token = None
        for _ in range(_MAX_PAGES):
            body = json.dumps(_google_rollup_body(since, page_token))
            response = _request(http, "POST", url, source, headers=headers, body=body)
            if not 200 <= response.status < 300:
                raise TrackerPullError(
                    f"read of {data_type} for {source!r} failed (HTTP {response.status})")
            data = _decode(response.body, source)
            for point in _records(data.get("rollupDataPoints"), source):
                day = _google_civil_day(point.get("civilStartTime"))
                value = _walk(point, value_path)
                if day and value is not None:
                    rows.append({"item": item, "timepoint": day, "value": value})
            page_token = data.get(_GOOGLE_NEXT_PAGE_FIELD)
            if not page_token:       # absent cursor -> this data type is done (single-response default)
                break
        else:
            raise TrackerPullError(f"read of {data_type} for {source!r} exceeded the page ceiling")
    return rows


def _google_rollup_body(since, page_token=None):
    """The Google `dailyRollUp` request body: a closed-open civil-day range, window size 1 day.

    `since` (YYYY-MM-DD) is the range start; a None `since` starts from the Unix epoch (a full pull,
    which the store dedupe collapses to the delta). A non-None `page_token` is echoed as the body's
    `pageToken` cursor to fetch the next page. The exact body schema is `[VERIFY-AT-BUILD]`.
    """
    start = since or "1970-01-01"
    year, month, day = (int(part) for part in start.split("-"))
    now = datetime.now(timezone.utc)
    body = {
        "range": {
            "start": {"year": year, "month": month, "day": day},
            "end": {"year": now.year, "month": now.month, "day": now.day},
        },
        "windowSizeDays": 1,
    }
    if page_token:
        body[_GOOGLE_PAGE_TOKEN_PARAM] = page_token
    return body


def _google_civil_day(civil):
    """Map a Google `civilStartTime` (`{date: {year, month, day}}`) to a YYYY-MM-DD string, or None."""
    date = (civil or {}).get("date") or {}
    if not all(key in date for key in ("year", "month", "day")):
        return None
    return f"{date['year']:04d}-{date['month']:02d}-{date['day']:02d}"


def _walk(obj, path):
    """Walk a nested dict along `path` (a key tuple) to a leaf scalar, or None if any hop is absent."""
    for key in path:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


# The per-source read-strategy table (design §10.2 / the Google fetch-seam strategy). `fetch` resolves
# `manifest["read"]` here; a source with no `read` key defaults to the Whoop reader. Adding a source
# with a Whoop-shaped API needs only a manifest entry (no new reader); a source whose API shape differs
# plugs a reader here rather than branching the shared routine.
_READERS = {
    "whoop": _read_whoop,
    "oura": _read_oura,
    "garmin": _read_garmin,
    "google": _read_google,
}
