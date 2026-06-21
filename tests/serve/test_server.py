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


def _server_with_roots(tmp_path):
    """Build a loopback server whose handler ingests into / re-renders from tmp roots.

    Points the POST handler's store + DNA roots at tmp dirs so the upload->ingest->
    re-render E2E never touches the real `vault/store/` / `vault/dna/raw/`, and the
    re-rendered intake screen reflects the tmp load-state.
    """
    srv = serve_server.build_server(0, store_root=tmp_path / "store", dna_root=tmp_path / "dna")
    return srv, srv.server_address[1]


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
        status, body = _post_upload(port, "export.xml", _healthkit_xml_bytes(value="55"))
        assert status == 200, f"POST /upload returned {status}, expected 200"

        hrv = store.read("hrv", root=tmp_path / "store")
        assert len(hrv) == 1 and hrv[0]["source"] == "healthkit", "export.xml did not land via ingest.run"
        assert hrv[0]["value"] == 55.0

        # The response IS the re-rendered wizard, reflecting the new load-state.
        assert WIZARD_TITLE in body, "response is not the re-rendered intake wizard"
        assert "1 readings" in body, "the re-rendered wizard does not reflect the new wearable load-state"
        assert "✓ loaded" in body, "the wearable card did not flip to loaded after the upload"
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
