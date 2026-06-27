"""Operator-confirm-before-land tests for the extracted-readings surface (ADR-0030-T3).

T2 extended `route_upload` so an unrecognized-format upload routes through the no-train
`client.extract_readings` and RETURNS the extracted readings WITHOUT landing them. T3
wires the server end: POST `/upload` surfaces the extracted readings as a JSON review
payload (it lands 0), and a NEW POST `/confirm-extraction` lands ONLY the operator-
confirmed subset through `scripts/serve/confirm.py`'s `land_confirmed` — a CALLER of the
UNCHANGED `ingest.manual_entry`/`store.append` sink (NOT a second sink, NOT a second gate,
NOT a second dedupe key; the operator-confirm IS the gate), the SAME disposes-after-gate
pattern as `capture.persist_capture`.

Cycle 1 (unit) — `confirm.land_confirmed`: AC-2 (lands the confirmed subset), AC-3
(SINK-CALLER: no model client / no keying of its own + a re-confirm appends 0 duplicates,
dedupe INHERITED from `store.append`), AC-4 (FAIL-CLOSED: a reading missing a Line-Field-Set
field lands nothing). Cycle 2 — `/upload` surfaces the discriminated extraction result as a
JSON review payload and lands 0 (AC-1), threading the injected client; the two forward-notes
the Wave-2 reviewers surfaced (a failed extraction degrades without dropping the thread; a
heterogeneous multi-file upload aggregates honestly). Cycle 3 — POST `/confirm-extraction`:
AC-2 (land only the confirmed subset), AC-4 (route-level fail-closed), AC-5 (thread survival),
AC-6 (route-table single-egress).

MOCK/FIXTURE-tested at 0 live spend: every served-handler test injects a mock no-train
client at the `build_server(client=…)` seam over temp store roots; `land_confirmed` is
driven over a temp store. No live API, no key, no non-loopback socket.
"""

import http.client
import json
import threading
from pathlib import Path

from scripts.model.client import ModelCallError
from scripts.serve import confirm
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"

# A Line-Field-Set-conformant canned readings payload (what the mock client returns for an
# unrecognized-format upload). Mirrors test_route.py's T2 canned readings.
_CANNED_READINGS = [
    {"item": "ferritin", "timepoint": "2026-05-01", "source": "labs", "value": "120"},
    {"item": "vitamin-d", "timepoint": "2026-05-01", "source": "labs", "value": "44"},
]

# The outbound-client surface an egress path would carry at import time (mirrors
# test_serve_no_egress.py's marker list) — the AC-6 single-egress re-check.
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)


class _ExtractClient:
    """A mock no-train model client whose `extract_readings` returns canned readings (0 spend).

    Records each `(file_content, media_type)` it receives and returns a canned Line-Field-Set
    readings list — no live API, no key, no network socket.

    Attributes:
        calls (list): The `(file_content, media_type)` tuples `extract_readings` saw.
    """

    def __init__(self, readings=None):
        self._readings = list(_CANNED_READINGS if readings is None else readings)
        self.calls = []

    def extract_readings(self, file_content, media_type):
        self.calls.append((file_content, media_type))
        return list(self._readings)


class _RaisingExtractClient:
    """A mock client whose `extract_readings` raises `ModelCallError` (a failed extraction)."""

    def __init__(self):
        self.calls = []

    def extract_readings(self, file_content, media_type):
        self.calls.append((file_content, media_type))
        raise ModelCallError("extraction failed")


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _server_with_extract(tmp_path, client):
    """Build a loopback server over tmp roots + an injected mock extract client (0 spend)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=client,
    )
    return srv, srv.server_address[1]


def _healthkit_xml_bytes(*, day="2026-05-01", value="55"):
    """Return a minimal Apple-Health `export.xml` carrying one HRV record (a recognized format)."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
        f' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        f' startDate="{day} 08:00:00 -0500" value="{value}"/>\n'
        '</HealthData>\n'
    ).encode()


def _file_part(filename, payload):
    """Build one multipart file part (name=export, given filename + payload bytes)."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="export"; filename="{filename}"\r\n\r\n').encode()
    out += payload
    out += b"\r\n"
    return bytes(out)


def _multipart_upload(parts):
    """Build a multipart/form-data body from a list of (filename, payload) file parts."""
    body = bytearray()
    for filename, payload in parts:
        body += _file_part(filename, payload)
    body += f"--{BOUNDARY}--\r\n".encode()
    return bytes(body)


def _post_upload(port, parts):
    """POST a multipart upload (one or more file parts) to `/upload`; return (status, raw text)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/upload", body=_multipart_upload(parts),
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _post_confirm(port, payload):
    """POST a JSON `/confirm-extraction` body; return (status, parsed-or-raw response)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps(payload).encode("utf-8") if isinstance(payload, (dict, list)) else payload
    conn.request("POST", "/confirm-extraction", body=body,
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    try:
        return resp.status, json.loads(text)
    except json.JSONDecodeError:
        return resp.status, text


def _parse_json(text):
    """Parse a response body as JSON, or return None if it is not JSON."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------- #
# Cycle 1 — confirm.land_confirmed: the sink-caller (AC-2 unit, AC-3, AC-4 unit)
# --------------------------------------------------------------------------- #


def test_land_confirmed_lands_the_confirmed_subset(tmp_path):
    """AC-2 (unit): land_confirmed lands exactly the confirmed readings via the unchanged sink.

    Over a list of conformant Line-Field-Set readings, `store.read_all` carries exactly those
    readings (each traceable to its `(item, value)`), landed through `ingest.manual_entry`.
    """
    root = tmp_path / "store"
    receipt = confirm.land_confirmed(_CANNED_READINGS, root=root)
    landed = store.read_all(root)
    by_item = {r["item"]: r["value"] for r in landed}
    assert by_item == {"ferritin": "120", "vitamin-d": "44"}, (
        f"the confirmed subset did not land exactly: {by_item}"
    )
    assert set(receipt["store"]) == {"ferritin", "vitamin-d"}, (
        f"the receipt does not report the landed item tokens: {receipt}"
    )


def test_confirm_py_imports_no_model_client_no_keying():
    """AC-3 (SINK-CALLER, structural): confirm.py imports no model client + no keying of its own.

    `confirm.py` makes 0 model call (imports no model client / SDK) and references no
    keying/dedupe/direct-store-write of its own — the dedupe + the uniform missing-field
    rejection are INHERITED from the unchanged `store.append` (reached via
    `ingest.manual_entry`). Reds if a model import or a self-owned keying surface appears.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "confirm.py").read_text()
    for marker in ("anthropic", "scripts.model", "ModelClient", "extract_readings"):
        assert marker not in src, f"confirm.py references a model client ({marker!r})"
    for marker in ("store.append(", "dedupe_key", "is_conformant", "import keying", "keying."):
        assert marker not in src, f"confirm.py defines its own keying/dedupe ({marker!r})"


def test_reconfirm_appends_zero_duplicates(tmp_path):
    """AC-3 (dedupe-collision): a re-confirm of the same readings appends 0 duplicate lines.

    The store-adversarial same-key/dedupe-key category, satisfied by REUSE: re-confirming the
    same readings is idempotent — `store.read_all` is unchanged after the second land (the
    `(item, timepoint, source)` dedupe is inherited from `store.append`, not re-implemented).
    """
    root = tmp_path / "store"
    confirm.land_confirmed(_CANNED_READINGS, root=root)
    first = store.read_all(root)
    confirm.land_confirmed(_CANNED_READINGS, root=root)
    second = store.read_all(root)
    assert first == second, "a re-confirm of the same readings appended duplicate lines"
    assert len(second) == 2, f"the re-confirm changed the store line count: {len(second)}"


def test_partial_confirmed_reading_lands_nothing(tmp_path):
    """AC-4 (FAIL-CLOSED, unit): a reading missing a Line-Field-Set field lands nothing.

    A confirmed reading missing a required field (`value`) is rejected by the unchanged sink
    (the uniform `ValueError` from `_store_reading`/`store.append`); 0 readings land —
    `store.read_all == []` afterward.
    """
    import pytest

    root = tmp_path / "store"
    partial = [{"item": "ferritin", "timepoint": "2026-05-01", "source": "labs"}]  # no value
    with pytest.raises(ValueError):
        confirm.land_confirmed(partial, root=root)
    assert store.read_all(root) == [], "a partial reading landed despite the fail-closed sink"


def test_partial_confirmed_reading_missing_item_lands_nothing(tmp_path):
    """AC-4 (FAIL-CLOSED, unit): a reading missing `item` fails closed uniformly (not a KeyError).

    The uniform missing-field rejection covers `item` itself — a reading missing `item` raises
    the same `ValueError` from the unchanged sink (`_store_reading`), never a raw `KeyError`,
    and lands nothing.
    """
    import pytest

    root = tmp_path / "store"
    no_item = [{"timepoint": "2026-05-01", "source": "labs", "value": "120"}]  # no item
    with pytest.raises(ValueError):
        confirm.land_confirmed(no_item, root=root)
    assert store.read_all(root) == [], "a reading missing item landed despite the fail-closed sink"


# --------------------------------------------------------------------------- #
# Cycle 2 — /upload surfaces the discriminated extraction result (lands 0)
# --------------------------------------------------------------------------- #


def test_upload_surfaces_extracted_readings_lands_none(tmp_path):
    """AC-1 (CONFIRM-GATE): POST /upload of an unrecognized format surfaces the readings, lands 0.

    POSTs an unrecognized-format file-only body to `/upload` over a server with an injected
    mock extract client. The response is a JSON review payload carrying the extracted readings
    AND `store.read_all(store_root) == []` immediately after (0 landed — the confirm-gate
    precondition; `/confirm-extraction` is the only landing path).
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, text = _post_upload(port, [("labs.pdf", b"%PDF-1.4 synthetic lab report")])
        assert status == 200, f"POST /upload returned {status}, expected 200"
        payload = _parse_json(text)
        assert payload is not None, "the /upload response is not a JSON review payload"
        assert payload.get("extracted_readings") == _CANNED_READINGS, (
            f"the review payload did not carry the extracted readings: {payload}"
        )
        # The confirm-gate: 0 readings landed before any /confirm-extraction.
        assert store.read_all(tmp_path / "store") == [], (
            "an unconfirmed reading landed at /upload (the confirm-gate is broken)"
        )
        assert len(client.calls) == 1, "the injected client's extract_readings was not called once"
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_failed_extraction_degrades_no_drop(tmp_path):
    """Forward-note 1 (ModelCallError): a failed extraction degrades, never drops the thread.

    With a mock client whose `extract_readings` raises `ModelCallError`, a POST /upload of an
    unrecognized format must degrade gracefully (a re-rendered/answered response, never a
    dropped connection or a 5xx from an uncaught exception), surface 0 fabricated readings,
    land 0, and keep the handler alive (a follow-up GET / still serves the app shell).
    """
    client = _RaisingExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, text = _post_upload(port, [("labs.pdf", b"%PDF-1.4 synthetic lab report")])
        assert status in (200, 400), f"a failed extraction returned {status} (dropped thread?)"
        # No fabricated readings surfaced, none landed.
        payload = _parse_json(text)
        if payload is not None:
            assert not payload.get("extracted_readings"), "a failed extraction fabricated readings"
        assert store.read_all(tmp_path / "store") == [], "a failed extraction landed a reading"
        # The handler survived — a follow-up GET / still serves the app shell.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        follow = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 200 and "Chat with Team" in follow, (
            "the handler died after a failed extraction"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_heterogeneous_recognized_lands_unrecognized_surfaced(tmp_path):
    """Forward-note 2 (heterogeneous upload): recognized lands as today, unrecognized surfaced.

    A single POST mixing a recognized `export.xml` (routes to `ingest.run`, lands) and an
    unrecognized `.pdf` (routes to extraction, surfaced for confirm). The recognized reading
    lands in the store as today; the unrecognized readings collect into the JSON review payload
    and land 0 (they await `/confirm-extraction`).
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, text = _post_upload(port, [
            ("export.xml", _healthkit_xml_bytes(day="2026-05-02", value="58")),
            ("labs.pdf", b"%PDF-1.4 synthetic lab report"),
        ])
        assert status == 200, f"heterogeneous POST returned {status}, expected 200"
        payload = _parse_json(text)
        assert payload is not None and payload.get("extracted_readings") == _CANNED_READINGS, (
            f"the unrecognized readings were not surfaced for confirm: {payload}"
        )
        # The recognized export.xml landed via the unchanged seam.
        hrv = store.read("hrv", root=tmp_path / "store")
        assert len(hrv) == 1 and hrv[0]["value"] == 58.0, "the recognized export.xml did not land"
        # The unrecognized readings landed 0 — only the recognized reading is in the store.
        all_items = {r["item"] for r in store.read_all(tmp_path / "store")}
        assert all_items == {"hrv"}, f"an unrecognized extracted reading auto-landed: {all_items}"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# Cycle 3 — POST /confirm-extraction (land only on confirm + thread survival + route table)
# --------------------------------------------------------------------------- #


def test_confirm_extraction_lands_only_confirmed_subset(tmp_path):
    """AC-2 (LAND ONLY ON CONFIRM): /confirm-extraction lands exactly the confirmed subset.

    POSTs the operator-confirmed subset (one of the two extracted readings) to
    `/confirm-extraction`; the confirmed reading is readable from the store after the POST AND
    the reading the operator did NOT confirm is absent (landed via `confirm.land_confirmed` ->
    the unchanged `store.append`).
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        confirmed = [_CANNED_READINGS[0]]  # the operator confirms ONLY ferritin
        status, resp = _post_confirm(port, {"readings": confirmed})
        assert status == 200, f"/confirm-extraction returned {status}, expected 200"
        landed_items = {r["item"]: r["value"] for r in store.read_all(tmp_path / "store")}
        assert landed_items == {"ferritin": "120"}, (
            f"the confirmed subset did not land exactly (non-confirmed leaked?): {landed_items}"
        )
        assert store.read("vitamin-d", root=tmp_path / "store") == [], (
            "a reading the operator did NOT confirm landed"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_confirm_extraction_partial_reading_lands_nothing(tmp_path):
    """AC-4 (route-level FAIL-CLOSED): a partial confirmed reading is rejected, lands nothing.

    A `/confirm-extraction` body carrying a reading missing a Line-Field-Set field is rejected
    (a degraded confirm response) and 0 readings land — `store.read_all == []` afterward.
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        partial = [{"item": "ferritin", "timepoint": "2026-05-01", "source": "labs"}]  # no value
        status, resp = _post_confirm(port, {"readings": partial})
        assert status != 200, f"a partial reading returned {status}, expected a degraded non-2xx"
        if isinstance(resp, dict):
            assert resp.get("degraded") is True, "the partial-reading response is not marked degraded"
        assert store.read_all(tmp_path / "store") == [], "a partial confirmed reading landed"
    finally:
        srv.shutdown()
        srv.server_close()


def test_malformed_confirm_body_degrades_no_drop(tmp_path):
    """AC-5 (THREAD SURVIVAL): a malformed /confirm-extraction body degrades, never drops the thread.

    A non-JSON body and a wrong-shape JSON body each yield a non-2xx degraded JSON response —
    0 store writes, no dropped thread, no fabricated landed reading — and the server survives
    to answer the next request (mirroring `/chat`'s catch-and-degrade).
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        for bad_body in (b"not json at all{{{", {"wrong": "shape"}):
            status, resp = _post_confirm(port, bad_body)
            assert status != 200, f"a malformed body returned {status} (dropped/accepted?)"
            if isinstance(resp, dict):
                assert resp.get("degraded") is True, f"not marked degraded: {bad_body!r}"
            assert store.read_all(tmp_path / "store") == [], f"a malformed body wrote the store: {bad_body!r}"
        # The server survived — a well-formed confirm still lands on the same port.
        ok_status, _ = _post_confirm(port, {"readings": [_CANNED_READINGS[0]]})
        assert ok_status == 200, "the handler died after malformed /confirm-extraction bodies"
        assert store.read("ferritin", root=tmp_path / "store"), "the post-recovery confirm did not land"
    finally:
        srv.shutdown()
        srv.server_close()


def test_route_table_gains_only_confirm_extraction(tmp_path):
    """AC-6 (ROUTE-TABLE single-egress): exactly one new route; bind + 0-outbound unchanged.

    `/confirm-extraction` answers (not 404) on the same loopback server; GET `/` and POST
    `/upload` still answer; an unknown POST still 404s. The `_LOOPBACK="127.0.0.1"` bind is
    byte-unchanged (0 new bind/port) and `scripts/serve/` carries 0 outbound client (0 new
    outbound class).
    """
    client = _ExtractClient()
    srv, port = _server_with_extract(tmp_path, client)
    _serve_in_thread(srv)
    try:
        # /confirm-extraction answers (a well-formed empty-subset confirm is a 200 receipt).
        status, _ = _post_confirm(port, {"readings": []})
        assert status == 200, f"/confirm-extraction 404'd (not in the dispatch): {status}"
        # GET / still serves the app shell (the route table did not lose a route).
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        get_resp = conn.getresponse()
        get_resp.read()
        conn.close()
        assert get_resp.status == 200, "GET / stopped answering after the new route landed"
        # An unknown POST still 404s.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/not-a-route", body=b"", headers={"Content-Type": "application/json"})
        unk = conn.getresponse()
        unk.read()
        conn.close()
        assert unk.status == 404, f"an unknown POST returned {unk.status}, expected 404"
    finally:
        srv.shutdown()
        srv.server_close()

    # The bind literal is byte-unchanged; the serve layer carries 0 outbound client.
    assert serve_server._LOOPBACK == "127.0.0.1"
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, (
                f"{py.name} references an outbound client ({marker!r}) — 0 new outbound class"
            )
