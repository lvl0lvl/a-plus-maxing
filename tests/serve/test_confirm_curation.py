"""POST /confirm-curation tests — the confirm-when-unsure meds-curation write-back route (T10/xwbe).

The care-review leg-2 curation (`care_review._curate_meds`) surfaces a confirm-when-unsure
question when it cannot classify the operator's meds with confidence, writing 0
`rx-interaction-classes` until the operator confirms. `care_review.confirm_curation` persists the
operator-confirmed de-identified class tokens — but until this task it had NO server route, so the
front-end confirm loop could not post the confirmation back. This route wires it:
POST `/confirm-curation` reads a JSON `{"classes": [...]}` body and CALLS the UNCHANGED
`care_review.confirm_curation(classes, store_root=...)` — no second sink, no second gate; the
operator-confirm IS the gate (mirroring `/confirm-extraction`'s disposes-after-gate shape).

MOCK/FIXTURE-tested at 0 live spend: every test drives the route over a temp store root; the
persisted token is a de-identified CLASS string (never a raw drug name). No live API, no key, no
non-loopback socket. The route makes 0 model call — `confirm_curation` writes the confirmed
scalar through the unchanged `store.append`.
"""

import http.client
import io
import json
import threading
from email.message import Message
from pathlib import Path

from scripts.plan import router
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _server(tmp_path):
    """Build a loopback server over a tmp store root (no client — the route makes 0 model call)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
    )
    return srv, srv.server_address[1]


def _post_confirm_curation(port, payload, *, content_type="application/json"):
    """POST a JSON `/confirm-curation` body; return (status, parsed-or-raw response)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps(payload).encode("utf-8") if isinstance(payload, (dict, list)) else payload
    conn.request("POST", "/confirm-curation", body=body, headers={"Content-Type": content_type})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    try:
        return resp.status, json.loads(text)
    except json.JSONDecodeError:
        return resp.status, text


def _drive_confirm_curation_inproc(store_root, *, content_type, content_length, body):
    """Drive `_do_confirm_curation` in-process (no socket) for the deterministic 413 path.

    Bypasses `BaseHTTPRequestHandler.__init__`'s socket setup so an oversize Content-Length
    with a tiny rfile has no connection-reset race (mirrors
    `test_extract_confirm._drive_confirm_inproc`).
    """
    bound = type("BoundIntakeRequestHandler", (serve_server.IntakeRequestHandler,),
                 {"store_root": store_root})
    handler = bound.__new__(bound)
    handler.path = "/confirm-curation"
    handler.command = "POST"
    handler.requestline = "POST /confirm-curation HTTP/1.1"
    handler.request_version = "HTTP/1.1"
    headers = Message()
    headers["Content-Type"] = content_type
    headers["Content-Length"] = str(content_length)
    handler.headers = headers
    handler.rfile = io.BytesIO(body)
    handler.wfile = io.BytesIO()
    handler._do_confirm_curation()
    return handler.wfile.getvalue()


def _rx_reading_values(store_root):
    """The persisted `rx-interaction-classes` values (the planner-input class tokens)."""
    return [r["value"] for r in store.read(router.RX_INTERACTION_CLASS_FIELD, root=store_root)]


# --------------------------------------------------------------------------- #
# Confirm loop: the operator-confirmed class token persists as the planner input
# --------------------------------------------------------------------------- #


def test_confirm_curation_persists_confirmed_classes(tmp_path):
    """AC3 (WRITE-BACK): POST /confirm-curation persists the confirmed de-identified class token.

    Posts the operator-confirmed class tokens; the route CALLS the unchanged
    `care_review.confirm_curation` and the normalized `rx-interaction-classes` scalar is readable
    from the store afterward (the planner input), and the receipt reports the confirmed tokens.
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, resp = _post_confirm_curation(port, {"classes": ["CYP3A4-PgP", "statin"]})
        assert status == 200, f"/confirm-curation returned {status}, expected 200"
        assert isinstance(resp, dict) and resp.get("confirmed") == ["cyp3a4-pgp", "statin"], (
            f"the confirm receipt did not report the normalized confirmed tokens: {resp}"
        )
    finally:
        srv.shutdown()
        srv.server_close()
    # The de-identified class scalar persisted as the planner input (via the unchanged store.append).
    assert _rx_reading_values(tmp_path / "store") == ["cyp3a4-pgp;statin"], (
        "the confirmed class token did not persist as the rx-interaction-classes planner input"
    )


def test_confirm_curation_persists_only_class_tokens_never_a_raw_drug(tmp_path):
    """AC3 (crown-jewel): only the posted de-identified CLASS token persists — 0 raw drug string.

    The confirm loop posts CLASS tokens (never a raw drug name); the persisted store scalar carries
    exactly the normalized classes and no raw drug string ever reaches the model-bound item through
    this route (the route CALLS `confirm_curation`, which writes only the joined class scalar).
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_confirm_curation(port, {"classes": ["cyp3a4-pgp"]})
        assert status == 200
    finally:
        srv.shutdown()
        srv.server_close()
    values = _rx_reading_values(tmp_path / "store")
    assert values == ["cyp3a4-pgp"], f"the persisted class token is not the expected scalar: {values}"
    assert "atorvastatin" not in json.dumps(values), "a raw drug string reached the model-bound item"


def test_confirm_curation_empty_classes_persists_nothing(tmp_path):
    """An empty/whitespace-only confirm persists nothing — the honest no-op (no false write)."""
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, resp = _post_confirm_curation(port, {"classes": ["", "   "]})
        assert status == 200, f"an empty confirm returned {status}, expected 200"
        assert resp.get("confirmed") == [], f"an empty confirm reported confirmed tokens: {resp}"
    finally:
        srv.shutdown()
        srv.server_close()
    assert _rx_reading_values(tmp_path / "store") == [], "an empty confirm wrote a store reading"


# --------------------------------------------------------------------------- #
# CSRF gate + bounded memory + thread survival (mirrors /confirm-extraction)
# --------------------------------------------------------------------------- #


def test_confirm_curation_rejects_dob_token_persists_nothing(tmp_path):
    """CROWN-JEWEL (Security F1): a DOB-shaped class token is rejected fail-closed, persists nothing.

    `rx-interaction-classes` is a model-bound `SUMMARY_FIELD_SET` token, and `pii_scan` carries NO
    date detector — so without a value gate on the confirm path a crafted `{"classes":["1986-04-12"]}`
    would persist a full DOB that `summarize`'s 8j6 scan cannot catch, crossing to the no-train
    planner. This route must run the SAME identity/`_DATE_LIKE` gate the auto-persist `_curate_meds`
    path applies (symmetric write-backs). Failing-capable: drop the gate and the DOB persists.
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, resp = _post_confirm_curation(port, {"classes": ["1986-04-12"]})
        assert status == 200, f"a DOB-token confirm returned {status}, expected a 200 honest degrade"
        assert resp.get("confirmed") == [], f"a DOB-shaped class token was confirmed: {resp}"
    finally:
        srv.shutdown()
        srv.server_close()
    assert _rx_reading_values(tmp_path / "store") == [], "a DOB-shaped class token persisted (crown-jewel breach)"


def test_confirm_curation_rejects_identity_bearing_token_batch_fail_closed(tmp_path):
    """CROWN-JEWEL (Security F1): a batch with ANY identity/contact-bearing token persists NOTHING.

    Fail-closed like `_curate_meds`: a batch mixing a clean class token with one carrying operator
    contact (an email) is rejected WHOLE — the clean token does not partial-persist (no leaky prefix),
    mirroring the auto-path's defer-entirely-on-any-dirty-value posture. Failing-capable: a per-token
    drop that kept the clean prefix would red the persists-nothing assertion.
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, resp = _post_confirm_curation(
            port, {"classes": ["statin", "reach me at operator@example.com"]})
        assert status == 200
        assert resp.get("confirmed") == [], f"an identity-bearing batch was confirmed: {resp}"
    finally:
        srv.shutdown()
        srv.server_close()
    assert _rx_reading_values(tmp_path / "store") == [], "an identity-bearing batch persisted a token (fail-open)"


def test_confirm_curation_text_plain_rejected_415_no_write(tmp_path):
    """CSRF: a text/plain POST is rejected 415 BEFORE the body is parsed, 0 write.

    A cross-site CORS-simple POST (text/plain, no preflight) carrying attacker-chosen classes must
    be rejected 415 — the same CSRF gate `_save_key`/`_do_confirm_extraction` apply — and persist
    NOTHING. Failing-capable: drop the ctype gate and the class lands (the store becomes non-empty).
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_confirm_curation(port, {"classes": ["cyp3a4-pgp"]}, content_type="text/plain")
        assert status == 415, f"a text/plain confirm returned {status}, expected 415"
    finally:
        srv.shutdown()
        srv.server_close()
    assert _rx_reading_values(tmp_path / "store") == [], "a text/plain confirm persisted a class (CSRF bypass)"


def test_confirm_curation_malformed_body_degrades_no_drop(tmp_path):
    """THREAD SURVIVAL: a malformed body degrades to a non-2xx, 0 write, server survives.

    A non-JSON body and a wrong-shape JSON body each yield a non-2xx degraded response, 0 store
    write, no dropped thread — and the server survives to answer a well-formed confirm next
    (mirroring `/chat` / `/confirm-extraction` catch-and-degrade).
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        for bad_body in (b"not json at all{{{", {"wrong": "shape"}):
            status, resp = _post_confirm_curation(port, bad_body)
            assert status != 200, f"a malformed body returned {status} (accepted?): {bad_body!r}"
            if isinstance(resp, dict):
                assert resp.get("degraded") is True, f"not marked degraded: {bad_body!r}"
            assert _rx_reading_values(tmp_path / "store") == [], f"a malformed body wrote the store: {bad_body!r}"
        # The server survived — a well-formed confirm still persists on the same port.
        ok_status, _ = _post_confirm_curation(port, {"classes": ["statin"]})
        assert ok_status == 200, "the handler died after malformed /confirm-curation bodies"
    finally:
        srv.shutdown()
        srv.server_close()
    assert _rx_reading_values(tmp_path / "store") == ["statin"], "the post-recovery confirm did not persist"


def test_confirm_curation_oversize_content_length_413_no_write(tmp_path):
    """BOUNDED MEMORY: an over-ceiling Content-Length is refused 413 BEFORE the body is read.

    Declares a Content-Length above the confirm ceiling while the rfile carries a tiny body; the
    handler answers 413 from the header before reading the body, persisting 0. Driven in-process
    (no socket) so the assertion is deterministic (mirrors the /confirm-extraction 413 test).
    """
    store_root = tmp_path / "store"
    declared = serve_server._CONFIRM_MAX_BYTES + 1
    out = _drive_confirm_curation_inproc(
        store_root, content_type="application/json", content_length=declared, body=b"{}"
    )
    status_line = out.split(b"\r\n", 1)[0]
    assert b"413" in status_line, f"an oversize confirm did not return 413: {status_line!r}"
    assert store.read_all(store_root) == [], "an oversize confirm persisted a reading"


def test_confirm_curation_route_answers_not_404(tmp_path):
    """ROUTE-TABLE: /confirm-curation answers (not 404); GET / + an unknown POST unchanged.

    The new route answers on the same loopback server; GET / still serves the shell; an unknown
    POST still 404s (the route table gained exactly this one route).
    """
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_confirm_curation(port, {"classes": []})
        assert status == 200, f"/confirm-curation 404'd (not in the dispatch): {status}"
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        get_resp = conn.getresponse()
        get_resp.read()
        conn.close()
        assert get_resp.status == 200, "GET / stopped answering after the new route landed"
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/not-a-route", body=b"", headers={"Content-Type": "application/json"})
        unk = conn.getresponse()
        unk.read()
        conn.close()
        assert unk.status == 404, f"an unknown POST returned {unk.status}, expected 404"
    finally:
        srv.shutdown()
        srv.server_close()
