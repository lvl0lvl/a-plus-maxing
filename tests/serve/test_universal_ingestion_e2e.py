"""End-to-end universal-ingestion proof + the four ADR-0030 falsification probes (ADR-0030-T5).

This is the terminal Wave-4 integration gate: a synthetic any-format upload produces an
operator-CONFIRMED LANDED reading through the SERVED `/upload` -> `/confirm-extraction`
path — not just a working extraction call and not the honest no-data state. It composes the
already-built backend chain end-to-end (this task adds NO production code):

    synthetic unrecognized-format file
      -> POST /upload (multipart)
      -> route.route_upload's unrecognized-format branch (ADR-0030-T2)
      -> client.extract_readings (the no-train lane, ADR-0030-T1; MOCKED at the
         ADR-0015 ModelClient(backend=...) seam — no live API, no key, 0 spend)
      -> the /upload JSON review payload `{"readings": [...]}` (ADR-0030-T3; lands 0)
      -> POST /confirm-extraction `{"readings": [...]}` (Content-Type: application/json — the
         CSRF gate) -> confirm.land_confirmed -> the UNCHANGED ingest.manual_entry/store.append
      -> a LANDED confirmed reading, readable via store.read_all.

Two load-bearing test properties:
  (a) NON-TAUTOLOGICAL: the headline asserts the landed `store.read_all` readings TRACE to the
      fixture's extracted `(item, value)` (the confirmed fixture subset EQUALS the landed
      readings), and a DIFFERENT fixture -> DIFFERENT landed readings — proving the landed data
      is the mock's parse, never a hardcoded constant. A failing-capable negative control proves
      the headline goes RED on the honest no-data state: it NEVER asserts merely "the store is
      non-empty". The non-tautology is demonstrated out-of-band by deliberate mechanism
      mutations (land disabled -> headline RED; /upload auto-lands -> confirm-gate RED;
      empty-extraction fabricates -> negative-control RED) recorded in the task report.
  (b) MOCK-TESTABLE: the model client is a fixture backend injected at the ADR-0015 seam, so the
      run is deterministic + CI-runnable with no network and no key (0 live key resolution).

The four ADR-0030 falsification probes, composed end-to-end:
  - AC-3 crown-jewel file-egress (structural/mock): the file content reaches ONLY the mock
    extract lane; no other sink (store/dna) received the raw bytes; scripts/serve/ carries 0
    outbound client and the single model-client import lives only under scripts/model/.
  - AC-4 confirm-gate: the store is empty after /upload and BEFORE /confirm-extraction; a
    reading lands ONLY after the confirm POST.
  - AC-5 fail-closed: an extraction failure surfaces 0 fabricated readings and the store stays
    empty (the /upload handler degrades the thread; nothing lands).
  - AC-6 OQ-5 residue: no TRACKED file (outside the gitignored dropzone prefixes read from
    .gitignore) carries the synthetic raw-file token; the staged temp file is discarded.

Honest coverage ceiling (NOT a falsifiable build criterion, ADR-0030 Rationale): a DNA *report*
PDF yields the lab's STATED findings as Line-Field-Set readings, not the raw genotype table that
`dna.land` validates — the universal lane extracts reported readings, it is not a second DNA
genotype parser. The LIVE universal-ingestion run (real key + real file + real spend, the
OS-egress-guard LIVE form of the crown-jewel probe) is OQ-1, the operator-gated checkpoint AFTER
this build, NOT a CI gate — no skipif variant is collected here.
"""

import http.client
import json
import subprocess
import threading
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

from scripts.model.client import ModelClient
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"

# The synthetic fixture readings — distinct items/timepoints/values so the latest-wins
# (item, timepoint, source) store identity never collapses two, and so fixture A and fixture B
# yield provably DIFFERENT landed sets (the non-constant proof). Each carries the full
# keying.LINE_FIELDS set so confirm.land_confirmed's all-or-nothing conformance check passes.
READINGS_A = (
    {"item": "ferritin", "timepoint": "2026-05-01", "source": "labreport", "value": "120"},
    {"item": "vitamin_d", "timepoint": "2026-05-01", "source": "labreport", "value": "44"},
)
READINGS_B = (
    {"item": "glucose_fasting", "timepoint": "2026-05-02", "source": "labreport", "value": "92"},
    {"item": "hdl", "timepoint": "2026-05-02", "source": "labreport", "value": "58"},
)

# The serve-layer outbound-client markers the crown-jewel static grep forbids (mirrors
# tests/serve/test_serve_no_egress.py::test_serve_layer_imports_no_outbound_client).
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)


class _FixtureBackend:
    """A mock extract backend: records the file bytes it received, returns scripted readings.

    Injected at the ADR-0015 `ModelClient(backend=...)` seam so the E2E exercises the REAL
    served /upload -> extract branch -> /confirm-extraction -> land path with only the model
    backend mocked (no live API, no key). `extract_calls` records every `(file_content,
    media_type)` so the crown-jewel probe can prove the raw file reached ONLY this lane.

    Attributes:
        readings (tuple): The scripted Line-Field-Set readings each call returns.
        extract_calls (list): The recorded `(file_content, media_type)` of every call.
    """

    def __init__(self, readings):
        self.readings = readings
        self.extract_calls = []

    def extract_readings(self, file_content, media_type):
        self.extract_calls.append((file_content, media_type))
        return [dict(r) for r in self.readings]


class _FailBackend:
    """A mock extract backend driving a fail-closed mode (the AC-5 failure injection).

    Each mode forces `ModelClient.extract_readings` to its typed `ModelCallError` fail-closed
    raise (a raised backend error, an empty `{}`, a truthy non-list, or a field-short reading
    list), which the /upload handler catches and degrades — surfacing 0 fabricated readings.

    Attributes:
        mode (str): One of "raise" / "empty_dict" / "non_list_truthy" / "field_short_list".
        extract_calls (list): The recorded calls, proving the lane was actually exercised.
    """

    def __init__(self, mode):
        self.mode = mode
        self.extract_calls = []

    def extract_readings(self, file_content, media_type):
        self.extract_calls.append((file_content, media_type))
        if self.mode == "raise":
            raise RuntimeError("synthetic extraction failure")
        if self.mode == "empty_dict":
            return {}
        if self.mode == "non_list_truthy":
            return {"item": "x", "timepoint": "t", "source": "s", "value": "v"}
        if self.mode == "field_short_list":
            return [{"item": "ferritin"}]
        raise AssertionError(f"unknown fail mode {self.mode}")


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


@contextmanager
def _running_server(root_base, backend):
    """Yield the loopback port of a running server over tmp roots + the mock client.

    Binds an EPHEMERAL loopback port (`build_server(0)`) over tmp store/dna/scaffold roots
    under `root_base` and a `ModelClient` over `backend`, so the E2E never touches the real
    vault and never makes a live API call. Shuts the listener down cleanly on exit.
    """
    srv = serve_server.build_server(
        0,
        store_root=root_base / "store",
        dna_root=root_base / "dna",
        scaffold_root=root_base / "scaffold",
        client=ModelClient(backend=backend),
    )
    _serve_in_thread(srv)
    try:
        yield srv.server_address[1]
    finally:
        srv.shutdown()
        srv.server_close()


def _raw_token():
    """Return a per-run-unique raw-file token (NOT a tracked literal).

    Generated at runtime so it appears in NO tracked file by construction — the OQ-5 residue
    scan for this token is a true 0-hit guard, not a self-match against this test's source.
    """
    return f"APLUS_E2E_RAWTOKEN_{uuid.uuid4().hex}"


def _fixture_bytes(token):
    """Build a synthetic unrecognized-format file body carrying the raw-file token."""
    return (
        f"SYNTHETIC LAB REPORT -- {token}\n"
        "Ferritin 120 ng/mL\nVitamin D 44 ng/mL\n"
    ).encode("utf-8")


def _multipart_upload(filename, payload):
    """Build a single-file multipart/form-data body for the `export` field."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="export"; filename="{filename}"\r\n\r\n').encode()
    out += payload
    out += b"\r\n"
    out += f"--{BOUNDARY}--\r\n".encode()
    return bytes(out)


def _post_upload(port, filename, payload):
    """POST a multipart file to `/upload`; return (status, base_content_type, parsed-or-raw body).

    The body is the parsed JSON review payload when the response is application/json (an
    unrecognized-format upload that surfaced readings), else the raw HTML text (the honest
    no-data / fail-closed re-render). Returning the content-type lets a caller distinguish the
    two without guessing.
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = _multipart_upload(filename, payload)
    conn.request(
        "POST", "/upload", body=body,
        headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"},
    )
    resp = conn.getresponse()
    ctype = (resp.getheader("Content-Type") or "").split(";", 1)[0].strip().lower()
    text = resp.read().decode("utf-8")
    conn.close()
    if ctype == "application/json":
        return resp.status, ctype, json.loads(text)
    return resp.status, ctype, text


def _post_confirm(port, readings):
    """POST the operator-confirmed subset to `/confirm-extraction`; return (status, parsed body).

    Sends `{"readings": [...]}` with `Content-Type: application/json` — the CSRF gate the route
    requires (a text/plain POST is rejected 415 before the body is parsed).
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps({"readings": readings}).encode("utf-8")
    conn.request(
        "POST", "/confirm-extraction", body=body,
        headers={"Content-Type": "application/json"},
    )
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, json.loads(text)


def _tuples(readings):
    """Return the order-independent set of (item, timepoint, source, value) tuples."""
    return {(r["item"], r["timepoint"], r["source"], r["value"]) for r in readings}


def _offered_readings(ctype, body):
    """Return the readings the /upload response offered for review (empty for the no-data state)."""
    if ctype == "application/json" and isinstance(body, dict):
        return body.get("readings", [])
    return []


def _upload_confirm_land(root_base, backend, token=None):
    """Drive the full served upload -> confirm -> land E2E; return the landed store readings.

    POSTs a synthetic unrecognized-format file to /upload, confirms whatever readings were
    surfaced, and returns `store.read_all(root_base / "store")`. With nothing surfaced (the
    no-data state) it confirms nothing and returns the empty store.
    """
    with _running_server(root_base, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(token or _raw_token()))
        assert status == 200
        offered = _offered_readings(ctype, body)
        if offered:
            _post_confirm(port, offered)
    return store.read_all(root_base / "store")


# --------------------------------------------------------------------------- #
# AC-1 / AC-4 / AC-8 — the headline non-tautological land + the confirm-gate + mock-tested
# --------------------------------------------------------------------------- #


def test_headline_synthetic_upload_confirm_lands_traced_reading(tmp_path):
    """AC-1 + AC-4: a synthetic upload -> /upload -> /confirm-extraction lands a TRACED reading.

    NON-TAUTOLOGICAL: the landed `store.read_all` readings EQUAL the confirmed fixture subset
    (the fixture's `(item, value)` appear in the store) — never merely "the store is non-empty".
    Woven AC-4 confirm-gate: the store is empty immediately after /upload and BEFORE
    /confirm-extraction; the reading lands ONLY after the confirm POST.
    """
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(_raw_token()))
        assert status == 200
        assert ctype == "application/json", "an unrecognized-format upload surfaces a JSON review payload"
        offered = body["readings"]
        # The review payload carries the extracted readings for operator review.
        assert _tuples(offered) == _tuples(READINGS_A)
        # AC-4 confirm-gate: nothing has landed before the confirm POST.
        assert store.read_all(tmp_path / "store") == []

        cstatus, cbody = _post_confirm(port, offered)
        assert cstatus == 200
        assert set(cbody["landed"]) == {r["item"] for r in READINGS_A}

        landed = store.read_all(tmp_path / "store")
    # Content-traceable: the landed readings EQUAL the confirmed fixture subset.
    assert _tuples(landed) == _tuples(READINGS_A)
    # The explicit (item, value) trace the AC names.
    assert {(r["item"], r["value"]) for r in landed} == {(r["item"], r["value"]) for r in READINGS_A}


def test_different_fixture_yields_different_landed_readings(tmp_path):
    """AC-1 (non-constant): a DIFFERENT fixture -> DIFFERENT landed readings (B != A).

    Proves the landed readings are the mock's parse of the fixture, not a hardcoded constant —
    a constant mechanism would land the same readings for both fixtures.
    """
    landed_a = _upload_confirm_land(tmp_path / "a", _FixtureBackend(READINGS_A))
    landed_b = _upload_confirm_land(tmp_path / "b", _FixtureBackend(READINGS_B))

    assert _tuples(landed_a) == _tuples(READINGS_A)
    assert _tuples(landed_b) == _tuples(READINGS_B)
    assert _tuples(landed_a) != _tuples(landed_b), "landed readings must track the fixture, not a constant"


def test_confirm_gate_store_empty_until_confirm(tmp_path):
    """AC-4 confirm-gate / confirm-bypass: a model-extracted reading lands ONLY after confirm.

    The /upload response carries the readings for review and lands 0; the store is empty if the
    confirm step is bypassed; a reading is readable from the store ONLY after the
    /confirm-extraction POST.
    """
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(_raw_token()))
        assert status == 200 and ctype == "application/json"
        assert body["readings"], "the /upload body carries the extracted readings for review"
        # Confirm bypassed -> 0 land.
        assert store.read_all(tmp_path / "store") == []

        _post_confirm(port, body["readings"])
        assert len(store.read_all(tmp_path / "store")) == len(READINGS_A)


def test_mock_tested_no_live_call_no_key_resolution(tmp_path, monkeypatch):
    """AC-8: the E2E runs over the mock seam with 0 live key-gated calls (no network, no key).

    Spies `key_source.resolve` (the live backend's only key gate); the full upload -> confirm ->
    land E2E lands the fixture readings via the mock, and the spy records 0 calls — the live lane
    is never touched. Proves the run is deterministic + CI-runnable with no key / 0 spend.
    """
    calls = []

    def _spy_resolve(*args, **kwargs):
        calls.append((args, kwargs))
        return "FAKE-KEY-NEVER-USED"

    monkeypatch.setattr("scripts.model.key_source.resolve", _spy_resolve)

    backend = _FixtureBackend(READINGS_A)
    landed = _upload_confirm_land(tmp_path, backend)

    assert _tuples(landed) == _tuples(READINGS_A), "the extract lane ran via the mock"
    assert backend.extract_calls, "the mock backend actually received the file"
    assert calls == [], "no live key resolution occurred (0 live spend)"


# --------------------------------------------------------------------------- #
# AC-2 — the failing-capable negative control (honest no-data, not constant-pass)
# --------------------------------------------------------------------------- #


def test_negative_control_operator_confirms_none_lands_nothing(tmp_path):
    """AC-2 (a): the operator confirms NONE of the surfaced readings -> 0 land.

    Drives the SAME pipeline; readings ARE surfaced for review, but the confirm POST sends an
    empty subset, so nothing lands — proving AC-1's land assertion goes RED with no usable land.
    """
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(_raw_token()))
        assert status == 200 and ctype == "application/json"
        assert body["readings"], "readings were surfaced for review"

        cstatus, cbody = _post_confirm(port, [])
        assert cstatus == 200
        assert cbody["landed"] == []
        assert store.read_all(tmp_path / "store") == []


def test_negative_control_empty_extraction_is_honest_no_data(tmp_path):
    """AC-2 (b): an empty-extraction (blank document) -> honest empty state, NOT a fabricated reading.

    The mock returns `[]` (a blank/empty document); the /upload response offers 0 readings for
    review and the store stays empty — proving the empty-extraction case is the honest no-data
    state, never a fabricated reading. The mock WAS invoked (the lane ran, it just had nothing).
    """
    backend = _FixtureBackend(())
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(_raw_token()))
        assert status == 200
        assert _offered_readings(ctype, body) == [], "an empty extraction offers no fabricated reading"
        assert store.read_all(tmp_path / "store") == []
    assert backend.extract_calls, "the extract lane was exercised (not a silent no-op)"


# --------------------------------------------------------------------------- #
# AC-3 — the crown-jewel file-egress probe (structural + mock-recording)
# --------------------------------------------------------------------------- #


def test_crown_jewel_file_reaches_only_the_mock_extract_lane(tmp_path):
    """AC-3 (mock-recording): the raw file content reaches ONLY the mock extract lane.

    The mock records the file bytes it received (the no-train lane got them); no other sink
    (store/dna/scaffold) carries the raw-file token, and the landed store readings carry only
    the structured (item, value) — never the raw file bytes.
    """
    token = _raw_token()
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(token))
        assert status == 200 and ctype == "application/json"
        _post_confirm(port, body["readings"])

    # The file content reached the mock extract lane.
    assert backend.extract_calls, "the mock extract lane never received the file"
    received = b"".join(
        fc if isinstance(fc, bytes) else str(fc).encode() for fc, _mt in backend.extract_calls
    )
    assert token.encode() in received, "the raw file bytes did not reach the mock extract lane"

    # No OTHER sink received the raw file bytes (the tmp instance roots carry no token).
    for root in (tmp_path / "store", tmp_path / "dna", tmp_path / "scaffold"):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                assert token not in p.read_text(errors="ignore"), f"{p} carries the raw file token"

    # The landed readings carry only the structured (item, value), never the raw file bytes.
    landed = store.read_all(tmp_path / "store")
    assert _tuples(landed) == _tuples(READINGS_A)
    assert all(token not in str(r) for r in landed)


def test_crown_jewel_serve_layer_imports_no_outbound_client():
    """AC-3 (static): scripts/serve/ carries 0 outbound clients (egress-free by construction)."""
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, (
                f"{py.name} references an outbound client ({marker!r}) — the serve layer must "
                f"be egress-free by construction"
            )


def test_crown_jewel_single_model_client_import_seam():
    """AC-3 (static): every model-client import lives ONLY inside scripts/model/."""
    result = subprocess.run(
        [
            "rg", "-n",
            r"anthropic|openai|\.messages\.create|httpx|requests",
            "scripts/", "--glob", "!scripts/model/**",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 1, (
        "model-client import leaked outside scripts/model/:\n" + result.stdout
    )


# --------------------------------------------------------------------------- #
# AC-5 — the fail-closed probe (a failed extraction fabricates nothing)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("mode", ["raise", "empty_dict", "non_list_truthy", "field_short_list"])
def test_fail_closed_extraction_failure_lands_nothing(tmp_path, mode):
    """AC-5: an extraction failure surfaces 0 fabricated readings and the store stays empty.

    Each fail mode forces `ModelClient.extract_readings` to its typed `ModelCallError`; the
    /upload handler catches it and degrades the thread (HTTP 200 re-render, no JSON readings
    payload), and nothing lands. A failed extraction never fabricates a reading.
    """
    backend = _FailBackend(mode)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _fixture_bytes(_raw_token()))
        # Thread survived (not a dropped connection) and offered no JSON readings payload.
        assert status == 200
        assert ctype != "application/json"
        assert _offered_readings(ctype, body) == []
        assert store.read_all(tmp_path / "store") == []
    assert backend.extract_calls, "the extraction was actually attempted (the failure was the model lane)"


# --------------------------------------------------------------------------- #
# AC-6 — the OQ-5 local-residue probe (no raw file on a tracked path)
# --------------------------------------------------------------------------- #


def _gitignore_dropzones():
    """Return the raw-data dropzone prefixes from .gitignore (the residue-scan exemption set).

    Reads the block under the "raw personal data dropzones" comment — the `vault/...` prefixes
    git ignores — so the exemption is derived from .gitignore, never a hardcoded path list.
    """
    lines = (REPO_ROOT / ".gitignore").read_text().splitlines()
    prefixes = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            collecting = "raw personal data dropzones" in stripped
            continue
        if collecting and stripped.startswith("vault/"):
            prefixes.append(stripped)
    return prefixes


def _is_gitignored(prefix):
    """Return True if `prefix` is genuinely git-ignored (the exemption is real, not assumed)."""
    probe = prefix.rstrip("/") + "/probe"
    result = subprocess.run(["git", "check-ignore", "-q", probe], cwd=REPO_ROOT)
    return result.returncode == 0


def test_oq5_no_raw_file_residue_in_tracked_tree(tmp_path):
    """AC-6: no TRACKED file carries the synthetic raw-file token; the staged temp file is discarded.

    Drives the full E2E with a per-run-unique raw-file token, then scans every TRACKED file
    (`git ls-files`, which respects .gitignore) for the token -> 0 hits. The dropzone exemption
    set is read from .gitignore and confirmed genuinely ignored, so a future dropzone change
    cannot silently weaken the scan. The tmp instance roots carry no token either (the raw
    upload lived only in memory / the discarded OS-temp staged path).
    """
    token = _raw_token()
    _upload_confirm_land(tmp_path, _FixtureBackend(READINGS_A), token=token)

    dropzones = _gitignore_dropzones()
    assert dropzones, "the .gitignore dropzone exemption set is non-empty"
    for prefix in dropzones:
        assert _is_gitignored(prefix), f"dropzone {prefix} is no longer git-ignored — exemption weakened"

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True
    ).stdout.splitlines()
    hits = []
    for rel in tracked:
        if not rel:
            continue
        path = REPO_ROOT / rel
        try:
            if token in path.read_text(errors="ignore"):
                hits.append(rel)
        except OSError:
            continue
    assert hits == [], f"the raw-file token leaked into tracked files: {hits}"

    for root in (tmp_path / "store", tmp_path / "dna", tmp_path / "scaffold"):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                assert token not in p.read_text(errors="ignore"), f"{p} carries the raw file token"
