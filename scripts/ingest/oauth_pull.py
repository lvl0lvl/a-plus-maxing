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

import getpass
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode


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

_MANIFESTS = {"whoop": _WHOOP}

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
    subprocess argument, never logged. Best-effort: a write failure is non-fatal (the current token
    still works this run); it is not raised so a keychain-ACL denial cannot abort a successful pull.
    """
    try:
        subprocess.run(
            ["security", "add-generic-password", "-U", "-A",
             "-a", getpass.getuser(), "-s", _oauth_service_name(source), "-w", payload],
            capture_output=True, text=True,
        )
    except (FileNotFoundError, OSError):
        pass


class _HttpResponse:
    """A minimal HTTP response the fetch layer reads: `.status` (int) + `.body` (bytes)."""

    __slots__ = ("status", "body")

    def __init__(self, status, body):
        self.status = status
        self.body = body


def _http(method, url, *, headers=None, body=None, timeout=_HTTP_TIMEOUT_S):
    """Issue one HTTP request and return an `_HttpResponse` (the default network seam; LIVE only).

    The single real-network site in this module — never exercised in tests (they inject a fixture
    seam). A non-2xx HTTP response is returned as an `_HttpResponse` carrying its status (the caller
    decides fail-closed); a genuine connection error (`URLError`) propagates for the caller to wrap.
    """
    data = body.encode() if isinstance(body, str) else body
    request = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return _HttpResponse(response.status, response.read())
    except urllib.error.HTTPError as exc:
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
    token = access_token(source, credential_reader=credential_reader,
                         credential_writer=credential_writer, http=http)

    rows = []
    for path, timestamp_field, field_items in manifest["endpoints"]:
        for record in _read_records(http, manifest, path, source, token, since):
            rows.extend(_rows_from_record(record, timestamp_field, field_items))

    staged = Path(staged_dir) / f"{source}.json"
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(json.dumps(rows))
    return staged


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
        for record in data.get("records", []):
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
