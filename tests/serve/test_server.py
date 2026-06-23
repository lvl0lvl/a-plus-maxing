"""Route + lifecycle tests for the loopback-only intake server (ADR-0013-T1, ADR-0013-T4).

AC-2: GET `/` against the running handler returns HTTP 200 + the intake wizard
HTML (the `generate.run('intake')` body), proved by the wizard title string in the
body — not a directory listing. A non-`/` GET returns 404. AC-4: the operator-stop
lifecycle closes the listener cleanly (a fresh bind to the freed port succeeds),
and `main` reads no stdin.

ADR-0013-T4 adds the POST `/upload` handler E2E coverage: a POST of a synthetic
`export.xml` (AC-1), an Apple-Health `.zip` (AC-3), and a 23andMe DNA `.zip` (AC-2)
each chains stage -> route -> re-render — the upload lands via the UNCHANGED
`ingest.run`/`dna.land` seam and the response re-renders the wizard reflecting the
new load-state. The intake-only assertion (AC-5 / Risk Falsification-3): a GET for a
dashboard/report artifact path 404s and `scripts/serve/` carries 0 artifact-serving
route. The 0-shared-routine-edit proof (AC-6) lives in `test_route.py`.
"""

import http.client
import io
import socket
import subprocess
import sys
import threading
import zipfile
from pathlib import Path

from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# The intake wizard title (vault/design/templates/intake.py render() <title>) the
# GET `/` body must carry — proves the route serves the wizard, not a dir listing.
WIZARD_TITLE = "A+ Maxing — Build your plan"

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"

# A synthetic 23andMe-format genotype table (the dna.land validator shape).
_DNA_HEADER = ["# rsid\tchromosome\tposition\tgenotype"]
_DNA_ROWS = [
    "rs4477212\t1\t82154\tAA",
    "rs3094315\t1\t752566\tAG",
    "rs3131972\t1\t752721\tGG",
]


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _healthkit_xml_bytes(*, day="2026-05-01", value="55"):
    """Return a minimal Apple-Health `export.xml` carrying one HRV record."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
        f' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        f' startDate="{day} 08:00:00 -0500" value="{value}"/>\n'
        '</HealthData>\n'
    ).encode()


def _apple_health_zip_bytes(xml_bytes):
    """Return an Apple-Health export `.zip` (export.xml under a dir + macOS noise)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("apple_health_export/", b"")
        zf.writestr("__MACOSX/._export.xml", b"resource-fork")
        zf.writestr("apple_health_export/export.xml", xml_bytes)
    return buf.getvalue()


def _dna_zip_bytes():
    """Return a synthetic 23andMe export `.zip` carrying a genotype `.txt` member."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("__MACOSX/._junk", "resource fork")
        zf.writestr("genome_v5.txt", "\n".join([*_DNA_HEADER, *_DNA_ROWS]) + "\n")
    return buf.getvalue()


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
    """POST a multipart upload to `/upload` on the running server; return (status, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = _multipart_upload(filename, payload)
    conn.request("POST", "/upload", body=body,
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _file_part(filename, payload):
    """Build one multipart file part (name=export, given filename + payload bytes)."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="export"; filename="{filename}"\r\n\r\n').encode()
    out += payload
    out += b"\r\n"
    return bytes(out)


def _post_raw(port, body):
    """POST a raw multipart body to `/upload`; return (status, response_text)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/upload", body=body,
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _server_with_roots(tmp_path):
    """Build a loopback server whose handler ingests into / re-renders from tmp roots.

    Points the POST handler's store + DNA + scaffold roots at tmp dirs so the
    upload->ingest->re-render and form-submit->capture->re-render E2Es never touch the
    real `vault/store/` / `vault/dna/raw/` / `vault/scaffold/filled/`, and the
    re-rendered intake screen reflects the tmp load-state.
    """
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
    )
    return srv, srv.server_address[1]


def _field_part(name, value):
    """Build one multipart NON-FILE form-field part (no filename= -> staged in `fields`)."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="{name}"\r\n\r\n').encode()
    out += value.encode("utf-8")
    out += b"\r\n"
    return bytes(out)


def _multipart_fields(fields):
    """Build a multipart/form-data body carrying only plain form fields (no files)."""
    body = bytearray()
    for name, value in fields.items():
        body += _field_part(name, value)
    body += f"--{BOUNDARY}--\r\n".encode()
    return bytes(body)


def _post_fields(port, fields):
    """POST a fields-only multipart capture to `/upload`; return (status, body)."""
    return _post_raw(port, _multipart_fields(fields))


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-2 GET `/` serves the wizard
# --------------------------------------------------------------------------- #


def test_get_root_returns_200_with_wizard_html():
    """AC-2: GET `/` returns HTTP 200 and the body carries the wizard title.

    Runs the real server on an ephemeral loopback port in a fixture thread and
    issues a GET `/` with http.client. The 200 body must contain the intake
    wizard's title string — proving GET `/` serves the wizard HTML produced by
    `generate.run('intake')`, not a directory listing.
    """
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 200, f"GET / returned {resp.status}, expected 200"
        assert WIZARD_TITLE in body, "GET / body does not carry the wizard title (not the wizard?)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_get_non_root_returns_404():
    """AC-2 boundary: a non-`/` GET returns 404 (the server serves only the wizard).

    A request to a path other than `/` must 404 — the server publishes exactly the
    GET `/` route, never a directory listing or an arbitrary-path file server.
    """
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/not-a-route")
        resp = conn.getresponse()
        resp.read()
        conn.close()
        assert resp.status == 404, f"GET /not-a-route returned {resp.status}, expected 404"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-4 operator-stop closes the listener; reads no stdin
# --------------------------------------------------------------------------- #


def test_operator_stop_closes_the_listener():
    """AC-4: stopping the server frees the port — a fresh bind to it then succeeds.

    Starts the server in-process on an ephemeral port, stops it via the clean stop
    path (shutdown + server_close), then asserts the listener is closed: a fresh
    socket can bind the freed port. A server with no clean-stop path holds the port
    and this fresh bind raises OSError.
    """
    srv = serve_server.build_server(0)
    port = srv.server_address[1]
    thread = _serve_in_thread(srv)

    # Clean operator-stop: shutdown the serve loop and close the listening socket.
    srv.shutdown()
    srv.server_close()
    thread.join(timeout=10)
    assert not thread.is_alive(), "serve loop did not stop after shutdown()"

    # The listener is closed: the freed port can be bound afresh.
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind(("127.0.0.1", port))
    finally:
        probe.close()


def test_main_reads_no_stdin():
    """AC-4: `main` reads no stdin — the operator surface never blocks on input.

    Runs `python -m scripts.serve` as a subprocess with stdin closed and an
    immediate interrupt (SIGINT) so it does not serve indefinitely. A run that
    read stdin would behave differently with /dev/null stdin; we assert the
    process started serving (or cleanly stopped) without a stdin-read error and
    that it exits on the interrupt rather than hanging. The timeout guards a hang.
    """
    import signal
    import time

    proc = subprocess.Popen(
        [sys.executable, "-m", "scripts.serve"],
        cwd=str(REPO_ROOT),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        # Give it a moment to bind + start serving (it must not block on stdin).
        time.sleep(1.5)
        assert proc.poll() is None, (
            "server exited before the interrupt — it did not serve "
            "(did it block/fail on stdin?)"
        )
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise AssertionError("server did not stop on SIGINT (hung)")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)


# --------------------------------------------------------------------------- #
# ADR-0013-T4 Cycle 2 — POST `/upload`: stage -> route -> re-render
# --------------------------------------------------------------------------- #


def test_post_export_xml_lands_readings_and_rerenders(tmp_path):
    """AC-1 (E2E): POST `export.xml` -> unchanged `ingest.run` + re-rendered wizard.

    POSTs a synthetic `export.xml` to `/upload`; the handler stages it, routes it
    into `ingest.run` (healthkit), and re-renders the wizard via `generate.run('intake')`.
    Asserts the HRV reading landed under the tmp store root AND the 200 response body
    is the re-rendered wizard reflecting the new load-state (the wearable card now shows
    the loaded count, not "Not linked").
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        # A distinctive raw value (won't collide incidentally with markup/dates) so the
        # no-leak negative assertion below is meaningful.
        status, body = _post_upload(port, "export.xml", _healthkit_xml_bytes(value="83.7"))
        assert status == 200, f"POST /upload returned {status}, expected 200"

        hrv = store.read("hrv", root=tmp_path / "store")
        assert len(hrv) == 1 and hrv[0]["source"] == "healthkit", "export.xml did not land via ingest.run"
        assert hrv[0]["value"] == 83.7

        # The response IS the re-rendered wizard, reflecting the new load-state.
        assert WIZARD_TITLE in body, "response is not the re-rendered intake wizard"
        assert "1 readings" in body, "the re-rendered wizard does not reflect the new wearable load-state"
        assert "✓ loaded" in body, "the wearable card did not flip to loaded after the upload"

        # Negative (no-leak): the re-render shows the COUNT + item + range (asserted
        # above), but NEVER the raw reading value — the wizard is counts-only.
        assert "83.7" not in body, "the re-rendered wizard leaked the raw HRV reading value (counts-only broken)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_apple_health_zip_lands_via_healthkit_adapter(tmp_path):
    """AC-3 (E2E): POST an Apple-Health `.zip` -> healthkit `ingest.run` via the zip-aware adapter.

    POSTs a synthetic Apple-Health `.zip` (NOT a pre-extracted xml). The route passes
    the zip AS-IS into `ingest.run` via the zip-aware healthkit adapter (ADR-0013-T3),
    which extracts `export.xml` internally — the handler adds no extraction. Asserts
    `store.read` returns the healthkit-mapped readings from the zip's inner xml.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        zip_bytes = _apple_health_zip_bytes(_healthkit_xml_bytes(day="2026-05-02", value="60"))
        status, body = _post_upload(port, "apple_health_export.zip", zip_bytes)
        assert status == 200, f"POST /upload returned {status}, expected 200"

        hrv = store.read("hrv", root=tmp_path / "store")
        assert len(hrv) == 1 and hrv[0]["source"] == "healthkit", "the zip did not land via the healthkit adapter"
        assert hrv[0]["value"] == 60.0 and hrv[0]["timepoint"] == "2026-05-02"

        # The DNA dropzone stayed empty — the Apple-Health zip routed to healthkit, not dna.
        dna_root = tmp_path / "dna"
        assert not (dna_root.exists() and list(dna_root.glob("*"))), "Apple-Health zip wrongly landed in the DNA dropzone"
        assert WIZARD_TITLE in body, "response is not the re-rendered intake wizard"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_dna_zip_lands_via_dna_land_and_rerenders(tmp_path):
    """AC-2 (E2E): POST a 23andMe `.zip` -> unchanged `dna.land` + re-rendered wizard.

    POSTs a synthetic 23andMe `.zip`; the route content-branches it to `dna.land`,
    which lands the genotype `.txt` under the tmp DNA root. Asserts the landed file
    appears under the DNA root, the store stays empty (DNA is not a time-series
    reading), and the response re-renders the wizard with the DNA card loaded.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_upload(port, "23andme_export.zip", _dna_zip_bytes())
        assert status == 200, f"POST /upload returned {status}, expected 200"

        landed = list((tmp_path / "dna").glob("*.txt"))
        assert landed and landed[0].name == "genome_v5.txt", "the DNA zip did not land via dna.land"
        assert store.read_all(tmp_path / "store") == [], "the DNA zip wrongly wrote into the time-series store"

        assert WIZARD_TITLE in body, "response is not the re-rendered intake wizard"
        assert "genome_v5.txt" in body, "the re-rendered wizard does not reflect the landed DNA file"

        # Negative (no-leak): the re-render names the landed FILE only — never a genotype
        # row or an rsid token. (Split the rsid literal so this test file carries none.)
        assert "rs" + "4477212" not in body, "the re-rendered wizard leaked an rsid token (no-leak broken)"
        assert "\t" not in body, "the re-rendered wizard leaked a tab-separated genotype row (no-leak broken)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_unknown_file_rerenders_with_message_no_crash(tmp_path):
    """A POST of an ambiguous/unknown file re-renders with a message — no crash/SystemExit.

    A `.json` upload is ambiguous (oura|garmin) so the CLI's `_detect_source` raises
    SystemExit; a `.bin` is unrecognized. The handler must catch the detection failure
    and re-render the wizard with a clear "pick a source" message rather than letting
    SystemExit kill the request handler (the handler stays responsive: a second request
    still succeeds).
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_upload(port, "mystery.json", b'[{"x": 1}]')
        # The request completes (no dropped connection / 500 from an uncaught SystemExit).
        assert status in (200, 400), f"unknown-file POST returned {status}, expected a rendered 200/400"
        assert WIZARD_TITLE in body, "the unknown-file response is not the re-rendered wizard"

        # The handler is still alive: a follow-up GET / still serves the wizard.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        follow = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 200 and WIZARD_TITLE in follow, "the handler died after the unknown-file POST"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# Wave-A review FIX-1/FIX-2 — handler robustness + bounded-memory oversize reject
# --------------------------------------------------------------------------- #


def _still_alive(port):
    """Return True if a follow-up GET / on `port` still serves the wizard (handler alive)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/")
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()
    return resp.status == 200 and WIZARD_TITLE in body


def test_post_garbage_export_xml_rerenders_no_crash(tmp_path):
    """FIX-1: a garbage `export.xml` (ParseError, NOT ValueError) re-renders, handler alive.

    A malformed `export.xml` makes the healthkit adapter's `iterparse` raise
    `xml.etree.ElementTree.ParseError` — NOT a ValueError, so the old catch missed it
    and the request thread died (dropped connection + stack trace to stderr). The
    handler must catch it, re-render the wizard (200), and stay responsive.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_upload(port, "export.xml", b"this is not valid xml <<<")
        assert status == 200, f"garbage export.xml returned {status}, expected a re-rendered 200"
        assert WIZARD_TITLE in body, "the garbage-xml response is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after the garbage-xml POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_not_really_a_zip_rerenders_no_crash(tmp_path):
    """FIX-1: a `.zip` that is not a zip (BadZipFile, NOT ValueError) re-renders, alive.

    A `.zip` upload whose bytes are not a zip makes the route's content-branch raise
    `zipfile.BadZipFile` — NOT a ValueError. The handler must catch it, re-render the
    wizard (200), and stay responsive rather than dropping the connection.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_upload(port, "fake.zip", b"PK this looks like a zip but is not")
        assert status == 200, f"not-a-zip returned {status}, expected a re-rendered 200"
        assert WIZARD_TITLE in body, "the not-a-zip response is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after the not-a-zip POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_non_numeric_content_length_rerenders_no_crash(tmp_path):
    """FIX-1: a non-numeric Content-Length re-renders rather than dropping the connection.

    The Content-Length parse (`int(...)`) used to sit OUTSIDE the guarded block, so a
    non-numeric value raised `ValueError` BEFORE the try and killed the request thread.
    The parse is now guarded: a garbage Content-Length re-renders the wizard (400) and
    the handler stays alive.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.putrequest("POST", "/upload")
        conn.putheader("Content-Type", f"multipart/form-data; boundary={BOUNDARY}")
        conn.putheader("Content-Length", "not-a-number")
        conn.endheaders()
        conn.send(b"")
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 400, f"non-numeric Content-Length returned {resp.status}, expected 400"
        assert WIZARD_TITLE in body, "the bad-Content-Length response is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after a non-numeric Content-Length POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_oversize_content_length_413_without_reading_body(tmp_path):
    """FIX-2: an over-ceiling Content-Length is refused with 413 BEFORE the body is read.

    Declares a Content-Length above `MAX_REQUEST_BYTES` but sends only a tiny body. If
    the handler read `length` bytes it would block waiting for ~520 MiB that never
    arrives (the request would hang/time out). A prompt 413 proves the reject happens on
    the header, before the body materializes in RAM — the bounded-memory guarantee. The
    handler stays alive.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        declared = serve_server.MAX_REQUEST_BYTES + 1
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.putrequest("POST", "/upload")
        conn.putheader("Content-Type", f"multipart/form-data; boundary={BOUNDARY}")
        conn.putheader("Content-Length", str(declared))
        conn.endheaders()
        # Send only a tiny body — far less than the declared length. A handler that read
        # `declared` bytes would block here; the 413 must come back without that read.
        conn.send(b"--" + BOUNDARY.encode() + b"\r\n")
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 413, f"oversize Content-Length returned {resp.status}, expected 413"
        assert WIZARD_TITLE in body, "the 413 body is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after the oversize-Content-Length POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_oversize_streamed_body_413_bounded_memory(tmp_path, monkeypatch):
    """FIX-2: a part exceeding the per-file ceiling is refused mid-stream (bounded RAM).

    With a small injected per-file ceiling, a body modestly above it must trip
    `multipart._stage_file`'s mid-stream ceiling (UploadTooLarge) and surface as 413 —
    proving the length-bounded reader hands the parser a STREAM so the per-file ceiling
    fires, rather than `rfile.read(length)` materializing the whole body first. Driving
    the ceiling small keeps this test off a 512 MiB fixture (FIX-5 sibling rationale).
    """
    from scripts.serve import multipart

    monkeypatch.setattr(multipart, "MAX_UPLOAD_BYTES", 4096)
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        oversize = b"A" * (4096 + 2048)  # over the injected per-file ceiling, tiny in RAM
        status, body = _post_upload(port, "export.zip", oversize)
        assert status == 413, f"over-per-file-ceiling body returned {status}, expected 413"
        assert WIZARD_TITLE in body, "the 413 body is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after the oversize-body POST"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# ADR-0013-T4 Cycle 3 — intake-only (AC-5 / Risk Falsification-3)
# --------------------------------------------------------------------------- #


def test_get_dashboard_artifact_path_404s(tmp_path):
    """AC-5 / Risk Falsification-3: a GET for a dashboard/report artifact path 404s.

    The server is intake-only — it serves NO generated artifact live. A GET for a
    dashboard/report artifact path returns 404 (no artifact route exists). Falsifiable:
    this reds the moment an artifact-serving route is added (the negative control below
    proves the assertion is failing-capable).
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        for artifact_path in ("/dashboard.html", "/report.html", "/artifacts/dashboard.html"):
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
            conn.request("GET", artifact_path)
            resp = conn.getresponse()
            resp.read()
            conn.close()
            assert resp.status == 404, f"GET {artifact_path} returned {resp.status}, expected 404 (intake-only)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_serve_layer_has_no_artifact_serving_route():
    """AC-5: `scripts/serve/` carries 0 dashboard/report artifact-serving route.

    The route table is intake-only {GET `/`, POST `/upload`}. The serve layer
    references no `generate.run('dashboard')`/`'report'` and no artifact-serving GET —
    `generate.run('intake')` (the re-render) is the only generate call. Reds if an
    artifact-serving route is added.
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        assert "generate.run('dashboard')" not in src and 'generate.run("dashboard")' not in src, (
            f"{py.name} serves the dashboard artifact (intake-only broken)"
        )
        assert "run('dashboard')" not in src and 'run("dashboard")' not in src, (
            f"{py.name} renders the dashboard artifact (intake-only broken)"
        )
        assert "run('report')" not in src and 'run("report")' not in src, (
            f"{py.name} renders the report artifact (intake-only broken)"
        )


# --------------------------------------------------------------------------- #
# Review FIX-A/FIX-B/FIX-C — collision-safe staging, no-file submit, inner ValueError
# --------------------------------------------------------------------------- #


def test_post_dual_upload_export_and_dna_both_land(tmp_path):
    """COV-2 (FIX-A): a dual upload (export.xml + 23andMe .zip) lands BOTH in one POST.

    POSTs ONE request carrying an `export.xml` (HRV) AND a 23andMe `.zip` (genotype).
    Both must land: the HRV reading in the store AND the genotype in the DNA dropzone,
    and the re-render reflects both. The realistic dual-upload coexistence case the
    server-loop iterates over every staged file part.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        body = bytearray()
        body += _file_part("export.xml", _healthkit_xml_bytes(day="2026-05-05", value="71.5"))
        body += _file_part("23andme_export.zip", _dna_zip_bytes())
        body += f"--{BOUNDARY}--\r\n".encode()
        status, text = _post_raw(port, bytes(body))
        assert status == 200, f"dual-upload POST returned {status}, expected 200"

        # The export.xml part landed an HRV reading in the store.
        hrv = store.read("hrv", root=tmp_path / "store")
        assert len(hrv) == 1 and hrv[0]["value"] == 71.5, "the export.xml part did not land"
        # The DNA-zip part landed a genotype file in the DNA dropzone.
        landed = list((tmp_path / "dna").glob("*.txt"))
        assert landed and landed[0].name == "genome_v5.txt", "the DNA zip part did not land"

        # The re-render reflects both load-states.
        assert WIZARD_TITLE in text, "response is not the re-rendered intake wizard"
        assert "1 readings" in text, "the re-render does not reflect the landed HRV reading"
        assert "genome_v5.txt" in text, "the re-render does not reflect the landed DNA file"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_two_same_basename_parts_both_land_in_store(tmp_path):
    """COV-2 (FIX-A, E2E failing-capable): two SAME-basename file parts both ingest.

    POSTs two file parts BOTH named `export.xml` (the on-disk collision), carrying
    DIFFERENT days. Both must ingest via the unchanged seam — the store carries TWO
    readings (one per day). Failing-capable: revert the per-part-unique staged path
    and the second part overwrites the first on disk, so only ONE day's reading lands
    and this assertion reds on the silently-lost first upload.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        body = bytearray()
        body += _file_part("export.xml", _healthkit_xml_bytes(day="2026-05-06", value="51"))
        body += _file_part("export.xml", _healthkit_xml_bytes(day="2026-05-07", value="52"))
        body += f"--{BOUNDARY}--\r\n".encode()
        status, text = _post_raw(port, bytes(body))
        assert status == 200, f"two-same-basename POST returned {status}, expected 200"

        hrv = store.read("hrv", root=tmp_path / "store")
        days = sorted(r["timepoint"] for r in hrv)
        assert days == ["2026-05-06", "2026-05-07"], (
            f"both same-basename parts did not land (first upload lost?): got {days}"
        )
        assert WIZARD_TITLE in text, "response is not the re-rendered intake wizard"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_collision_basename_parts_both_persist_on_disk(tmp_path):
    """COV-2 (FIX-A, direct): two parts with the SAME basename stage to distinct paths.

    Hits the exact collision the fix targets: two file parts both named `export.xml`.
    Staged under per-part-unique paths, both bodies persist on disk. Asserts both
    distinct payloads survived staging (the second did not overwrite the first).
    Failing-capable: revert the per-part prefix and the second part overwrites the
    first on disk — only one payload survives and this assertion reds.
    """
    import io

    from scripts.serve.multipart import stage_uploads

    body = bytearray()
    body += _file_part("export.xml", b"FIRST-payload-bytes")
    body += _file_part("export.xml", b"SECOND-payload-bytes")
    body += f"--{BOUNDARY}--\r\n".encode()

    result = stage_uploads(f"multipart/form-data; boundary={BOUNDARY}", io.BytesIO(bytes(body)), tmp_path)
    assert len(result["files"]) == 2, "expected two staged file parts"
    paths = [Path(f["path"]) for f in result["files"]]
    assert paths[0] != paths[1], "two same-basename parts staged to the SAME path (collision)"
    contents = {p.read_bytes() for p in paths}
    assert contents == {b"FIRST-payload-bytes", b"SECOND-payload-bytes"}, (
        "a same-basename part overwrote the other on disk (first upload silently lost)"
    )


def test_post_no_file_chosen_not_staged(tmp_path):
    """FIX-B: a part with filename="" (no file chosen) is NOT staged as a file.

    A browser submitting the upload form with no file chosen sends a part with
    `filename=""`. The old `if "filename" in params` treated it as a file part and
    staged a zero-byte `upload`. The handler must treat it as a non-file: 200
    re-render, handler stays alive, and no reading/file landed.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        body = bytearray()
        body += f"--{BOUNDARY}\r\n".encode()
        body += b'Content-Disposition: form-data; name="export"; filename=""\r\n\r\n'
        body += b"\r\n"
        body += f"--{BOUNDARY}--\r\n".encode()
        status, text = _post_raw(port, bytes(body))
        assert status == 200, f"no-file submit returned {status}, expected 200"
        assert WIZARD_TITLE in text, "the no-file response is not the re-rendered wizard"

        # Nothing was staged/ingested — the store and dropzone stay empty.
        assert store.read_all(tmp_path / "store") == [], "a no-file submit wrongly wrote into the store"
        dna_root = tmp_path / "dna"
        assert not (dna_root.exists() and list(dna_root.glob("*"))), "a no-file submit wrongly wrote a DNA file"
        assert _still_alive(port), "the handler died after a no-file submit"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_unterminated_multipart_body_rerenders_no_crash(tmp_path):
    """COV-1 (FIX-C): a multipart body missing the closing `--BOUNDARY--` re-renders, alive.

    A file part with NO closing terminator makes `stage_uploads` raise the INNER
    `ValueError("malformed multipart body ...")` (distinct from the OUTER non-numeric
    Content-Length ValueError). The handler's inner `except (..., ValueError, ...)` arm
    must catch it, re-render the wizard (200), and keep the handler responsive — a
    follow-up GET / still 200s. Coverage-only; no production change.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        # A file part with NO closing `--BOUNDARY--` terminator: the parser streams the
        # part body looking for the next boundary, hits EOF, and raises the inner ValueError.
        body = _file_part("export.xml", _healthkit_xml_bytes())  # no trailing close delimiter
        status, text = _post_raw(port, body)
        assert status == 200, f"unterminated body returned {status}, expected a re-rendered 200"
        assert WIZARD_TITLE in text, "the unterminated-body response is not the re-rendered wizard"
        assert _still_alive(port), "the handler died after an unterminated multipart body"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# ADR-0014-T1 Cycle 2 — form-submit POST: stage -> capture -> re-render
# --------------------------------------------------------------------------- #


def test_post_capture_fields_land_wired_tokens_and_rerenders(tmp_path):
    """AC-1 (E2E): a form-submit POST lands the wired tokens via store.append + re-renders.

    POSTs a multipart body whose parts are plain `fields` (no filename= -> they decode
    into `staged["fields"]`): a Step-2 `goal-domains` + `hard-limits` capture. The
    handler routes them through `capture.persist_capture` into the tmp store, then
    re-renders the wizard via `generate.run('intake')`. Asserts the tokens landed
    tagged source:"intake" AND the 200 response is the re-rendered wizard.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_fields(port, {
            "goal-domains": "Workout;Nutrition",
            "hard-limits": "no overhead pressing",
        })
        assert status == 200, f"capture POST returned {status}, expected 200"

        gd = store.read("goal-domains", root=tmp_path / "store")
        assert len(gd) == 1 and gd[0]["source"] == "intake", "goal-domains did not land via capture.persist_capture"
        assert gd[0]["value"] == "Workout;Nutrition"
        hl = store.read("hard-limits", root=tmp_path / "store")
        assert hl and hl[0]["value"] == "no overhead pressing", "hard-limits did not land"

        assert WIZARD_TITLE in body, "the capture response is not the re-rendered wizard"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_capture_record_only_lands_in_scaffold_not_store(tmp_path):
    """AC-2 / Risk Negative-2 (E2E two-surface negative placement): record-only -> scaffold ONLY.

    POSTs a record-only capture (an arbitrary record-only field + the FIX-A record-only
    `rx-interaction-classes` form field). Both land under the tmp `scaffold_root` AND
    `store.read(<any SUMMARY_FIELD_SET token>)` does NOT carry that record-only value (the
    negative assertion — the project assert-placement mandate). Iterates every field-set
    token. (NOTE ADR-0019-T1: the former `supplement-stack` example here is now a WIRED raw
    source — it writes the `raw-supplement-free-text` named-excluded store item, no longer
    record-only — so this test uses genuinely-record-only fields to keep proving the path.)
    """
    from scripts.plan.router import SUMMARY_FIELD_SET

    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_fields(port, {
            "favorite-color": "mediterranean high protein",
            "rx-interaction-classes": "creatine monohydrate 5g",
        })
        assert status == 200, f"record-only capture POST returned {status}, expected 200"

        # Positive: the values landed under the scaffold root.
        scaffold_root = tmp_path / "scaffold"
        scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
        assert "mediterranean" in scaffold_text, "the favorite-color record-only value did not land in the scaffold"
        assert "creatine" in scaffold_text, "the rx record-only value did not land in the scaffold"

        # Negative (load-bearing): NO field-set store item carries a record-only value.
        for token in SUMMARY_FIELD_SET:
            for reading in store.read(token, root=tmp_path / "store"):
                v = str(reading["value"])
                assert "mediterranean" not in v and "creatine" not in v, (
                    f"a record-only value leaked into the {token!r} field-set store item"
                )
        assert WIZARD_TITLE in body, "the record-only capture response is not the re-rendered wizard"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# ADR-0014-T1 Cycle 4 — Step-6 handoff (AC-5 / Risk Falsification-3)
# --------------------------------------------------------------------------- #


def test_post_step6_is_a_generate_plan_handoff_not_in_app_generation(tmp_path):
    """AC-5 / Risk Falsification-3: the Step-6 submit is a /generate-plan handoff, 0 generation.

    The Step-6 "Save & open plan generation" submit persists any still-transient
    inputs and returns the HANDOFF state: a readiness summary + the instruction to
    run `/generate-plan` (the agent path), NOT a generated plan. The handler performs
    0 in-app generation.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_fields(port, {
            "goal-domains": "Workout",
            "step": "6",  # the Step-6 "Save & open plan generation" submit
        })
        assert status == 200, f"Step-6 submit returned {status}, expected 200"
        # The response instructs the operator to run /generate-plan (the handoff), and
        # is the re-rendered wizard — never a generated plan artifact.
        assert "/generate-plan" in body, "the Step-6 response does not instruct the /generate-plan handoff"
        assert WIZARD_TITLE in body, "the Step-6 response is not the re-rendered wizard"
        # Still-transient inputs were persisted via the same capture path.
        assert store.read("goal-domains", root=tmp_path / "store"), "the Step-6 submit did not persist the inputs"
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_step6_step_control_field_never_lands_in_the_record(tmp_path):
    """FIX-E1: the `step` control field is stripped — it never lands in the operator record.

    The Step-6 submit carries a `step=6` control field that selects the handoff re-render.
    The handler pops it (`fields.pop("step")`) so it never reaches `persist_capture` as a
    stray record-only scaffold value. Assert the tmp scaffold carries no `"step"` key/value
    after a Step-6 submit. Failing-capable: drop the `fields.pop("step")` and `step` lands
    in the scaffold record, reddening this.
    """
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        # A record-only field forces a scaffold write so a leaked `step` would appear there.
        status, _ = _post_fields(port, {
            "dietary-pattern": "high protein",
            "step": "6",
        })
        assert status == 200, f"Step-6 submit returned {status}, expected 200"

        scaffold_root = tmp_path / "scaffold"
        scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
        assert "dietary-pattern" in scaffold_text, "the record-only field did not land (no scaffold written)"
        assert '"step"' not in scaffold_text, "the `step` control field leaked into the operator record"
    finally:
        srv.shutdown()
        srv.server_close()


def test_serve_layer_has_no_in_app_plan_generation_call():
    """AC-5 / Risk Falsification-3: scripts/serve/ carries 0 assemble/plan-generation call.

    Step 6 is a `/generate-plan` HANDOFF; the serve layer adds no in-app plan
    generation. Assert no `assemble` import/call and no plan-generation reference in
    scripts/serve/. Reds if an in-app generation call is added (the negative control
    in the recipe: temporarily add an assemble call -> this reds).
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        assert "assemble" not in src, (
            f"{py.name} references plan assembly — Step 6 is a /generate-plan handoff, 0 in-app generation"
        )
        assert "orchestrator" not in src, (
            f"{py.name} references the plan orchestrator — no in-app generation in the serve layer"
        )
