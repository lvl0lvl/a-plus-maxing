"""Route + lifecycle tests for the loopback-only server (ADR-0013-T1, ADR-0013-T4, ADR-0029-T1).

AC-2: GET `/` against the running handler returns HTTP 200 + the served app-shell SPA
HTML (the `generate.run('app')` body — re-pointed from the intake wizard at ADR-0029-T1),
proved by the SPA nav marker in the body — not a directory listing. A non-`/` GET returns
404. AC-4: the operator-stop lifecycle closes the listener cleanly (a fresh bind to the
freed port succeeds), and `main` reads no stdin.

ADR-0013-T4 adds the POST `/upload` handler E2E coverage: a POST of a synthetic
`export.xml` (AC-1), an Apple-Health `.zip` (AC-3), and a 23andMe DNA `.zip` (AC-2)
each chains stage -> route -> re-render — the upload lands via the UNCHANGED
`ingest.run`/`dna.land` seam and the response re-renders the app shell reflecting the
new load-state (its Upload Documents cards). The no-artifact-route assertion (AC-5 / Risk
Falsification-3): a GET for a dashboard/report artifact path 404s and `scripts/serve/`
carries 0 artifact-serving route. The 0-shared-routine-edit proof (AC-6) lives in `test_route.py`.
"""

import http.client
import io
import json
import socket
import subprocess
import sys
import threading
import zipfile
from pathlib import Path

from scripts.ingest.pdf_extract import PdfExtractError
from scripts.serve import route
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# A served-body marker UNIQUE to the served app shell — its "Chat with Team" nav button
# (vault/design/templates/app_shell.py, ADR-0029-T1). The intake wizard has no such nav,
# so this distinguishes the SPA served body from the old wizard <title>; the re-render
# tests assert it to prove GET `/` (and the POST re-render) serves the SPA, not a dir listing.
SPA_NAV_MARKER = "Chat with Team"

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


# The ten directly-captured elements the ADR-0033-0035-T6 first-run completeness gate requires
# present for `generate.run('app')` to serve the UNLOCKED platform shell (where the Upload
# Documents doc-cards live, inside `#screen-team`). The seven profile tokens: `date-of-birth`
# -> `training-age-band`, `bodyweight-kg` -> `bodyweight-band`, and five PII-free pass-through
# tokens; plus the three `safety-screen::*` answered markers. An UPLOAD does not complete a
# profile, so a POST re-render whose store lacks these serves the locked Create-Profile body.
_COMPLETE_PROFILE = {
    "date-of-birth": "1986-04-12",
    "bodyweight-kg": "82",
    "sex-for-dosing": "male",
    "equipment-access-class": "full-home-gym",
    "goal-domains": "Workout;Nutrition",
    "goal-targets": "Build strength and improve sleep",
    "goal-priority-order": "Workout, Nutrition, Supplements",
    "safety-screen::exercise-safety": "no",
    "safety-screen::phq2": "no",
    "safety-screen::apnea": "no",
}


def _seed_complete_profile(root, *, timepoint="2026-06-01T00:00:00+00:00", source="intake"):
    """Seed the ten required elements so the POST re-render unlocks the platform shell (T6 gate)."""
    for item, value in _COMPLETE_PROFILE.items():
        store.append(
            item, {"item": item, "timepoint": timepoint, "source": source, "value": value}, root=root,
        )


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
# Cycle 1 — AC-2 GET `/` serves the app shell (re-pointed from the wizard, ADR-0029-T1)
# --------------------------------------------------------------------------- #


def test_get_root_returns_200_with_spa_html():
    """AC-2: GET `/` returns HTTP 200 and the body carries the SPA served surface.

    Runs the real server on an ephemeral loopback port in a fixture thread and
    issues a GET `/` with http.client. The 200 body must contain the SPA nav marker
    — proving GET `/` serves the app-shell HTML produced by `generate.run('app')`
    (re-pointed from the intake wizard, ADR-0029-T1), not a directory listing.
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
        assert SPA_NAV_MARKER in body, "GET / body does not carry the SPA nav marker (not the served app shell?)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_get_non_root_returns_404():
    """AC-2 boundary: a non-`/` GET returns 404 (the server serves only the app shell).

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
    # Seed a complete profile so the POST re-render unlocks the platform shell where the Upload
    # doc-cards live (post-T6 gate); an incomplete store would serve the locked Create-Profile body.
    _seed_complete_profile(tmp_path / "store")
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
        assert SPA_NAV_MARKER in body, "response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "response is not the re-rendered SPA served body"
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
    # Seed a complete profile so the POST re-render unlocks the platform shell where the DNA
    # doc-card renders (post-T6 gate). Snapshot the store immediately AFTER seeding / BEFORE the
    # DNA upload: the "DNA contributes zero time-series readings" invariant is now asserted against
    # this seeded baseline, since unlocking requires store data and global emptiness no longer holds.
    _seed_complete_profile(tmp_path / "store")
    store_before_dna = store.read_all(tmp_path / "store")
    srv, port = _server_with_roots(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_upload(port, "23andme_export.zip", _dna_zip_bytes())
        assert status == 200, f"POST /upload returned {status}, expected 200"

        landed = list((tmp_path / "dna").glob("*.txt"))
        assert landed and landed[0].name == "genome_v5.txt", "the DNA zip did not land via dna.land"
        # TRUE intent (rewritten from the pre-T6 `== []`): the DNA zip lands ONLY as a file under
        # dna_root and writes NO time-series reading — the store is byte-identical to the pre-upload
        # profile baseline. RED-capable: a DNA upload that wrote a reading would add an element to
        # read_all, so `after != store_before_dna` and this equality reds (the same failure the old
        # `== []` caught, re-expressed against the non-empty seeded baseline).
        assert store.read_all(tmp_path / "store") == store_before_dna, (
            "the DNA zip wrongly wrote a time-series reading into the store (it must land only as a dropzone file)"
        )

        assert SPA_NAV_MARKER in body, "response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the unknown-file response is not the re-rendered SPA served body"

        # The handler is still alive: a follow-up GET / still serves the wizard.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        follow = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 200 and SPA_NAV_MARKER in follow, "the handler died after the unknown-file POST"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# Wave-A review FIX-1/FIX-2 — handler robustness + bounded-memory oversize reject
# --------------------------------------------------------------------------- #


def _still_alive(port):
    """Return True if a follow-up GET / on `port` still serves the app shell (handler alive)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/")
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()
    return resp.status == 200 and SPA_NAV_MARKER in body


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
        assert SPA_NAV_MARKER in body, "the garbage-xml response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the not-a-zip response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the bad-Content-Length response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the 413 body is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the 413 body is not the re-rendered SPA served body"
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
    # Seed a complete profile so the POST re-render unlocks the platform shell where the Upload
    # doc-cards live (post-T6 gate); an incomplete store would serve the locked Create-Profile body.
    _seed_complete_profile(tmp_path / "store")
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
        assert SPA_NAV_MARKER in text, "response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in text, "response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in text, "the no-file response is not the re-rendered SPA served body"

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
        assert SPA_NAV_MARKER in text, "the unterminated-body response is not the re-rendered SPA served body"
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
    re-renders the served app shell via `generate.run('app')` (re-pointed at ADR-0029-T1).
    Asserts the tokens landed tagged source:"intake" AND the 200 response is the served SPA.
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

        assert SPA_NAV_MARKER in body, "the capture response is not the re-rendered SPA served body"
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
        assert SPA_NAV_MARKER in body, "the record-only capture response is not the re-rendered SPA served body"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# ADR-0014-T1 Cycle 4 — Step-6 handoff (AC-5 / Risk Falsification-3)
# --------------------------------------------------------------------------- #


# RETIRED (ADR-0029-T1, AC-7 class b): the wizard-presentation-specific
# `test_post_step6_is_a_generate_plan_handoff_not_in_app_generation` POSTed `step:"6"`
# (a wizard-only submit) and asserted the wizard's `/generate-plan` Step-6 handoff body —
# a surface the served SPA does not have (the SPA's plan generation is the Plan screen's
# "Generate plan →", driven by T4/T5, not an in-app wizard handoff). It is RETIRED rather
# than marker-swapped (a marker swap that still POSTed `step:"6"` while claiming to test the
# wizard handoff is the tautological dead-wizard test AC-7 forbids). Its non-presentation
# coverage survives: the `step:"6"` submit still captures + strips `step`
# (`test_post_step6_step_control_field_never_lands_in_the_record`, below) and the serve
# layer does 0 in-app generation (`test_serve_layer_has_no_in_app_plan_generation_call`).


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


def test_serve_layer_delegates_plan_generation_no_reimplementation():
    """The serve layer generates plans by DELEGATING to the frozen plan engine — it re-implements none.

    The POST `/generate-plan` route (the in-app plan-engine trigger) gathers each domain's author
    envelope then CALLS the frozen cross-domain orchestrator `orchestrate.generate_plans` (which runs
    the supplement<->peptide additive-AE screen + the other cross-domain holds before recording) — it
    re-implements no `assemble` (the safety-filter pass), so the serve layer never forks the safety
    pipeline the frozen `scripts/plan/*` owns. The delegation is asserted positively (server.py
    references `generate_plans` + `orchestrate`) so this is not vacuous. Reds if the serve layer ever
    re-implements the assembler, OR if the delegation to the frozen orchestrator is removed (the
    cross-domain-safety bypass the TEST1 review finding flagged).
    SUPERSEDES the pre-PR `test_serve_layer_has_no_in_app_plan_generation_call`: the serve layer NOW
    does in-app generation (the operator's "Generate plan" press), via delegation to the FROZEN
    orchestrator (NOT a per-domain `generate_plan` loop, which bypassed the cross-domain reconciler),
    not re-implementation.
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        assert "assemble" not in src, (
            f"{py.name} references plan assembly — the serve layer must DELEGATE to the frozen "
            f"plan engine, never re-implement assemble"
        )
    server_src = (serve_dir / "server.py").read_text()
    assert "generate_plans" in server_src and "orchestrate" in server_src, (
        "server.py no longer delegates to the frozen cross-domain orchestrator "
        "(orchestrate.generate_plans) — the in-app plan trigger bypasses the cross-domain safety screen"
    )


# --------------------------------------------------------------------------- #
# ADR-0031-T4 — /upload surfaces the honest-partial signal (partial/notes) + F1
#   AC-4 partial surfaced; F1 empty-but-partial emits the JSON signal (NOT the
#   silent HTML re-render); AC-4 complete -> partial:false; PdfExtractError
#   thread-survival fold-in; the route-table re-assertion (GREEN by construction)
# --------------------------------------------------------------------------- #

# A Line-Field-Set-conformant canned readings payload (what the route extract path returns).
_CANNED_READINGS = [
    {"item": "ferritin", "timepoint": "2026-05-01", "source": "labs", "value": "120"},
    {"item": "vitamin-d", "timepoint": "2026-05-01", "source": "labs", "value": "44"},
]


class _StubClient:
    """A no-op mock model client (the route extract path is stubbed; the client is never called)."""

    def extract_readings(self, file_content, media_type):
        return []


def _server_with_client(tmp_path, client):
    """Build a loopback server over tmp roots + an injected mock client (0 spend)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=client,
    )
    return srv, srv.server_address[1]


def _post_upload_ct(port, filename, payload):
    """POST a multipart upload to `/upload`; return (status, base-content-type, body text)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = _multipart_upload(filename, payload)
    conn.request("POST", "/upload", body=body,
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    ctype = (resp.getheader("Content-Type") or "").split(";", 1)[0].strip().lower()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, ctype, text


def test_upload_pdf_partial_signal_surfaced(tmp_path, monkeypatch):
    """AC-4: a partial PDF extraction surfaces `partial: true` + the note in the /upload payload.

    Stubs the route extract path to return a partial signal (`complete=False` + a note); the
    /upload response must be a JSON review payload carrying the extracted readings, `partial: true`,
    and the note in `notes`. STUBS pdf_extract.extract_text + extract_chunked.extract_all so the
    test drives server.py's surfacing logic at 0 real-pdftotext cost.
    """
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "some extracted text")
    monkeypatch.setattr(
        route.extract_chunked, "extract_all",
        lambda text, c: {"readings": _CANNED_READINGS, "complete": False, "note": "document too large"},
    )
    srv, port = _server_with_client(tmp_path, _StubClient())
    _serve_in_thread(srv)
    try:
        status, ctype, body = _post_upload_ct(port, "labs.pdf", b"%PDF-1.4 body")
        assert status == 200 and ctype == "application/json", "a partial PDF extraction must surface a JSON review payload"
        payload = json.loads(body)
        assert payload["readings"] == _CANNED_READINGS, f"the review payload did not carry the readings: {payload}"
        assert payload["partial"] is True, f"a partial extraction was not flagged partial: {payload}"
        assert "document too large" in payload["notes"], f"the partial note was not surfaced: {payload}"
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_partial_empty_surfaces_signal_not_silent_rerender(tmp_path, monkeypatch):
    """F1 (load-bearing): `extracted == []` + `partial == True` emits the honest signal, NOT silence.

    The route extract path returns `{readings: [], complete: False, note: <note>}` (a too-dense /
    over-budget PDF that yielded no readings within budget). The /upload handler must emit the
    honest-signal JSON payload (`partial: true`, notes non-empty, `readings: []`) — NOT fall through
    to the silent "no new data" app-shell HTML re-render. Failing-capable: the pre-fix `if extracted:`
    gate is False on `[]` and falls through to the HTML re-render (the SPA_NAV_MARKER body).
    """
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "some extracted text")
    monkeypatch.setattr(
        route.extract_chunked, "extract_all",
        lambda text, c: {"readings": [], "complete": False, "note": "document too large to extract within budget"},
    )
    srv, port = _server_with_client(tmp_path, _StubClient())
    _serve_in_thread(srv)
    try:
        status, ctype, body = _post_upload_ct(port, "labs.pdf", b"%PDF-1.4 body")
        assert status == 200, f"the empty-but-partial upload returned {status}, expected 200"
        assert ctype == "application/json", "F1: an empty-but-partial extraction must emit the JSON honest signal"
        assert SPA_NAV_MARKER not in body, "F1: the silent app-shell HTML re-render was served instead of the honest signal"
        payload = json.loads(body)
        assert payload["readings"] == [], f"the empty-but-partial payload should carry no readings: {payload}"
        assert payload["partial"] is True, f"the empty-but-partial signal was not flagged partial: {payload}"
        assert payload["notes"] and "document too large to extract within budget" in payload["notes"], (
            f"the empty-but-partial note was not surfaced: {payload}"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_complete_extraction_partial_false(tmp_path, monkeypatch):
    """AC-4: a complete PDF extraction surfaces `partial: false` and empty `notes`.

    The route extract path returns `{readings: <canned>, complete: True, note: None}`; the
    /upload JSON payload must carry `partial: false` and `notes: []` (a complete extraction is
    not flagged partial).
    """
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "some extracted text")
    monkeypatch.setattr(
        route.extract_chunked, "extract_all",
        lambda text, c: {"readings": _CANNED_READINGS, "complete": True, "note": None},
    )
    srv, port = _server_with_client(tmp_path, _StubClient())
    _serve_in_thread(srv)
    try:
        status, ctype, body = _post_upload_ct(port, "labs.pdf", b"%PDF-1.4 body")
        assert status == 200 and ctype == "application/json", "a complete PDF extraction surfaces a JSON review payload"
        payload = json.loads(body)
        assert payload["readings"] == _CANNED_READINGS, f"the review payload did not carry the readings: {payload}"
        assert payload["partial"] is False, f"a complete extraction was wrongly flagged partial: {payload}"
        assert payload["notes"] == [], f"a complete extraction surfaced a note: {payload}"
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_pdf_extract_failure_degrades_no_drop(tmp_path, monkeypatch):
    """A total local-extraction failure (`PdfExtractError`) degrades the thread, never drops it.

    Monkeypatches pdf_extract.extract_text to raise `PdfExtractError` (T1's fail-loud raise on
    total failure). The /upload handler must degrade gracefully — a re-rendered response (not a
    dropped connection / 5xx), 0 fabricated/landed readings, and a still-alive handler (a follow-up
    GET / still serves the SPA). Failing-capable: pre-fix `PdfExtractError` is not in the catch
    tuple -> uncaught -> the request thread drops.
    """
    def _raise(path):
        raise PdfExtractError("total extraction failure")

    monkeypatch.setattr(route.pdf_extract, "extract_text", _raise)
    srv, port = _server_with_client(tmp_path, _StubClient())
    _serve_in_thread(srv)
    try:
        status, ctype, body = _post_upload_ct(port, "labs.pdf", b"%PDF-1.4 body")
        assert status in (200, 400), f"a PdfExtractError returned {status} (dropped thread / 5xx?)"
        assert ctype != "application/json", "a failed extraction surfaced a JSON readings payload (fabricated?)"
        assert SPA_NAV_MARKER in body, "a failed extraction did not degrade to the app-shell re-render"
        assert store.read_all(tmp_path / "store") == [], "a failed extraction landed a reading"
        assert _still_alive(port), "the handler died after a PdfExtractError (thread dropped)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_upload_route_table_unchanged(tmp_path):
    """The route table + the loopback bind are byte-unchanged — T4 adds no route/bind.

    An unknown POST still 404s and GET / still serves the SPA (the dispatch did not gain/lose a
    route), and the `_LOOPBACK = "127.0.0.1"` bind literal is byte-unchanged. A STANDING
    re-assertion — GREEN by construction.
    """
    srv, port = _server_with_client(tmp_path, _StubClient())
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/not-a-route", body=b"", headers={"Content-Type": "application/json"})
        unk = conn.getresponse()
        unk.read()
        conn.close()
        assert unk.status == 404, f"an unknown POST returned {unk.status}, expected 404"
        assert _still_alive(port), "GET / stopped serving the SPA (a route was lost)"
    finally:
        srv.shutdown()
        srv.server_close()

    src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    assert '_LOOPBACK = "127.0.0.1"' in src, "the loopback bind literal changed (T4 must not touch the bind)"


# --------------------------------------------------------------------------- #
# POST /generate-plan — the in-app plan-engine trigger: author + record a plan for
# each plan domain over the stored data via the unchanged generate_plan caller, then
# answer the re-rendered Plan zone + per-domain outcomes. Fixture-driven, 0 live spend
# (a mock no-train author client injected at the seam — no key, no API call).
# --------------------------------------------------------------------------- #

import datetime

from scripts.model.client import ModelCallError
from scripts.plan import orchestrate
from scripts.plan.generate_plan import AUTHOR_CALL_FAILED
from scripts.store import keying, plan_schema


class _MockAuthorClient:
    """A mock no-train author client: per-domain envelope (or raise) for author(domain, summary).

    Mirrors the `ModelClient.author(domain, summary)` seam `generate_plan` calls — 0 live API,
    0 key. `raise_for` maps a domain to an exception instance the author raises for that domain
    (drives the per-domain degrade / resilience paths).
    """

    def __init__(self, envelopes, *, raise_for=None):
        self._envelopes = envelopes
        self._raise_for = raise_for or {}
        self.calls = []

    def author(self, domain, summary):
        self.calls.append(domain)
        if domain in self._raise_for:
            raise self._raise_for[domain]
        return self._envelopes[domain]


def _rec(claim, category, source, payload):
    """A complete, HALT-clearing universal recommendation (the assemble survival contract)."""
    return {
        "claim": claim, "source": source, "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation", "category": category,
        "payload": payload,
    }


def _domain_envelopes(*, workout_name="Goblet squat"):
    """One surviving per-domain author envelope each (proven-shape recs from test_generate_plan)."""
    return {
        "workout": {"specialist": "personal-trainer", "recommendations": [
            _rec(f"rebuild a movement base with {workout_name.lower()}", "training",
                 "ACSM resistance-training guidelines 2024",
                 {"name": workout_name, "sets": 3, "reps": "8-12", "detail": "controlled tempo"})]},
        "nutrition": {"specialist": "nutritionist", "recommendations": [
            _rec("set energy and protein at maintenance to support recovery", "nutrition",
                 "ISSN position stand on protein and exercise 2017",
                 {"calorie_goal": 2600, "macros": {"protein": 190, "carbs": 250, "fat": 80}}),
            _rec("distribute protein across the day with breakfast", "nutrition",
                 "ISSN position stand on protein and exercise 2017",
                 {"meal": {"name": "Breakfast", "contents": "eggs, oats, berries", "kcal": 650}})]},
        "supplements": {"specialist": "supplement-specialist", "recommendations": [
            _rec("supplement creatine to close a documented gap", "supplementation",
                 "Examine.com creatine monograph 2024",
                 {"name": "Creatine monohydrate", "dose": "5 g", "timing": "daily"})]},
        "peptides": {"specialist": "peptide-specialist", "recommendations": [
            _rec("run bpc-157 for localized tissue support", "peptide-therapy",
                 "vault/library/peptides/bpc-157 research-report 2026",
                 {"compound": "BPC-157", "dose": "250 mcg", "route": "subcutaneous"})]},
    }


def _seed_summary_store(store_root):
    """Seed the PII-free operator-state items `router.summarize` reads (hard-limits benign)."""
    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": "2026-06-18", "source": "intake", "value": value},
            root=store_root,
        )


def _post_generate_plan(port, *, content_type="application/json"):
    """POST /generate-plan (application/json, the CSRF-gated content-type); return (status, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
    conn.request("POST", "/generate-plan", body=b"{}", headers={"Content-Type": content_type})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _post_confirm_extraction(port, readings):
    """POST /confirm-extraction (application/json) on the running server; return (status, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
    conn.request("POST", "/confirm-extraction", body=json.dumps({"readings": readings}).encode(),
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _resolving_key():
    """A key_resolver that RESOLVES (returns a key) — the connected-Profile state for tests."""
    return "sk-ant-test-key"


def _unavailable_key():
    """A key_resolver that raises KeyUnavailableError — the live-but-keyless production state."""
    from scripts.model import key_source

    raise key_source.KeyUnavailableError("no key set")


def _server_with_author(tmp_path, client, *, key_resolver=_resolving_key):
    """Server over tmp roots + a mock author client + (by default) a key that RESOLVES.

    The default `key_resolver` returns a key so /generate-plan's no-key guard passes and the
    injected mock author runs (the happy / resilience / E2E tests need a resolvable key AND a
    client — the production no-key guard now gates on key availability, not just a None client).
    Pass `key_resolver=_unavailable_key` to exercise the live-but-keyless path.
    """
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=client, key_resolver=key_resolver,
    )
    return srv, srv.server_address[1]


class _FormatAgnosticClient:
    """One mock no-train client for BOTH lanes (0 live API): extract_readings + author.

    `extract_readings` returns a fixed extracted-reading set (the arbitrary-format extraction the
    no-train extract lane yields); `author` ECHOES the de-identified `active-issue-class` the
    summary carries into the workout plan, so the rendered plan is content-traceable to the
    uploaded reading, and records the summary each author call saw. The non-workout domains return
    the thin-library sentinel (an honest no-plan) to keep the E2E focused on the traceable path.
    """

    def __init__(self, extracted):
        self._extracted = list(extracted)
        self.author_summaries = {}

    def extract_readings(self, file_content, media_type):
        return list(self._extracted)

    def author(self, domain, summary):
        self.author_summaries[domain] = summary
        if domain == "workout":
            issue = summary.get("active-issue-class") or "general-issue"
            return {"specialist": "personal-trainer", "recommendations": [
                _rec(f"prioritize a {issue} rehab base before loading", "training",
                     "ACSM resistance-training guidelines 2024",
                     {"name": "Goblet squat", "sets": 3, "reps": "8-12",
                      "detail": f"rehab focus: {issue}"})]}
        return {"specialist": f"{domain}-specialist", "thin_library": True}


def test_generate_plan_records_all_domains_and_renders(tmp_path):
    """E2E happy path: POST /generate-plan records every domain + the re-render is content-traceable.

    Seeds the summary store, injects a MOCK author returning a valid per-domain envelope, then
    POSTs /generate-plan. Asserts: every `plan_schema.PLAN_DOMAINS` domain is RECORDED in the
    store (`plan::<domain>` resolves a plan for today), and the re-rendered Plan zone in the JSON
    reply carries a recommendation TRACEABLE to each mock author's output (a content assertion,
    not merely "a plan exists"). The mock author is reached once per domain — 0 live API / key.
    """
    _seed_summary_store(tmp_path / "store")
    client = _MockAuthorClient(_domain_envelopes())
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"POST /generate-plan returned {status}, expected 200"
        payload = json.loads(body)
        assert payload["need_key"] is False, "a present author client + resolvable key must not report need_key"
        assert payload["results"] == {d: "recorded" for d in plan_schema.PLAN_DOMAINS}, (
            f"not every domain recorded: {payload['results']}"
        )

        # Each domain's plan is RECORDED in the store (resolved for today).
        today = datetime.date.today().isoformat()
        for domain in plan_schema.PLAN_DOMAINS:
            resolved = plan_schema.read_plan(domain, today, tmp_path / "store")
            assert resolved["plan"] is not None, f"{domain} plan was not recorded into the store"

        # Content-traceable: the re-rendered Plan zone carries a recommendation from each author.
        plan_html = payload["plan_html"]
        for token in ("Goblet squat", "Breakfast", "Creatine monohydrate", "BPC-157"):
            assert token in plan_html, f"the re-rendered Plan zone does not carry {token!r}"

        # The author was reached exactly once per domain (no live API, no duplicate calls).
        assert sorted(client.calls) == sorted(plan_schema.PLAN_DOMAINS), (
            f"the author was not reached once per domain: {client.calls}"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_different_author_yields_different_plan(tmp_path):
    """Non-tautological: a DIFFERENT mock author output -> a DIFFERENT rendered plan.

    Runs /generate-plan twice over two isolated stores with two different workout authors; the
    rendered Plan zone reflects EACH author's distinct exercise — A's name appears only in A's
    render and B's only in B's. Proves the render is driven by the author's output, not a fixed
    string baked into the template (the failing-capable A != B control).
    """
    def gen(sub, name):
        root = tmp_path / sub
        _seed_summary_store(root / "store")
        srv, port = _server_with_author(root, _MockAuthorClient(_domain_envelopes(workout_name=name)))
        _serve_in_thread(srv)
        try:
            status, body = _post_generate_plan(port)
            assert status == 200, f"POST /generate-plan returned {status}, expected 200"
            return json.loads(body)["plan_html"]
        finally:
            srv.shutdown()
            srv.server_close()

    a = gen("a", "Goblet squat")
    b = gen("b", "Bulgarian split squat")
    assert "Goblet squat" in a and "Goblet squat" not in b, "author A's exercise leaked / missing"
    assert "Bulgarian split squat" in b and "Bulgarian split squat" not in a, (
        "author B's exercise leaked / missing — the render is not driven by the author output"
    )


def test_generate_plan_no_key_records_nothing(tmp_path):
    """No-key path: client=None -> honest need_key, 0 plans recorded, no crash/500.

    Builds the server WITHOUT an author client (`self.client is None`, the no-key state). POST
    /generate-plan must answer the honest need_key state, record 0 plans (the engine is never
    called), and keep the handler alive — never a crash or a 500.
    """
    _seed_summary_store(tmp_path / "store")
    srv, port = _server_with_roots(tmp_path)  # build_server() -> self.client is None
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"no-key POST /generate-plan returned {status}, expected 200"
        payload = json.loads(body)
        assert payload["need_key"] is True, "a None author client must report need_key"
        assert payload["results"] == {}, "the no-key path must not run the engine for any domain"

        for domain in plan_schema.PLAN_DOMAINS:
            assert store.read(f"plan::{domain}", root=tmp_path / "store") == [], (
                f"the no-key path wrongly recorded a {domain} plan"
            )
        assert _still_alive(port), "the handler died after a no-key /generate-plan POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_one_domain_failure_does_not_abort_run(tmp_path):
    """Per-domain resilience: one domain's failure records the others + surfaces an honest reason.

    Injects an author that RAISES a plain ValueError for nutrition (caught by the route's
    per-domain try/except) and a ModelCallError for peptides (degraded by generate_plan to the
    honest author-call-failed reason). The two healthy domains (workout, supplements) still
    RECORD, the run never aborts (all four domains appear in `results`), and each failing
    domain records nothing while surfacing its honest no-plan reason — not a stack trace, not a
    500, not a silently-dropped run.
    """
    _seed_summary_store(tmp_path / "store")
    client = _MockAuthorClient(_domain_envelopes(), raise_for={
        "nutrition": ValueError("author blew up"),
        "peptides": ModelCallError("backend author failed"),
    })
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"resilience POST /generate-plan returned {status}, expected 200"
        payload = json.loads(body)
        results = payload["results"]

        # The run did NOT abort — all four domains were attempted and reported.
        assert set(results) == set(plan_schema.PLAN_DOMAINS), (
            f"the run aborted on one domain's failure: {results}"
        )
        # The two healthy domains recorded.
        assert results["workout"] == "recorded" and results["supplements"] == "recorded"
        # The raised-ValueError domain records nothing, honest reason surfaced (not a stack trace).
        assert results["nutrition"].startswith("error"), (
            f"nutrition's raised failure was not caught as an honest reason: {results['nutrition']}"
        )
        # The ModelCallError domain degrades to the honest author-call-failed no-plan reason.
        assert results["peptides"] == AUTHOR_CALL_FAILED, (
            f"peptides did not degrade to author-call-failed: {results['peptides']}"
        )

        today = datetime.date.today().isoformat()
        assert plan_schema.read_plan("workout", today, tmp_path / "store")["plan"] is not None
        assert plan_schema.read_plan("supplements", today, tmp_path / "store")["plan"] is not None
        assert store.read("plan::nutrition", root=tmp_path / "store") == [], "nutrition wrongly recorded"
        assert store.read("plan::peptides", root=tmp_path / "store") == [], "peptides wrongly recorded"
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_live_client_but_no_key_returns_need_key(tmp_path):
    """No-key (live client, no key behind it): need_key BEFORE any author call — the production case.

    In production `self.client` is ALWAYS a live ModelClient (never None), so the None-only guard
    never fires for a keyless operator. The route uses the SAME key-availability check the Profile
    status reports (`key_source.resolve` via the `key_resolver` seam): a live client whose key does
    NOT resolve -> need_key:true, 0 plans recorded, and NO author/live call attempted. Failing-
    capable: revert to the `self.client is None`-only guard and this reds (the live client would be
    called and the operator would get four cryptic author-call-failed degrades, not the honest
    need_key).
    """
    _seed_summary_store(tmp_path / "store")
    client = _MockAuthorClient(_domain_envelopes())  # a live (non-None) author client...
    srv, port = _server_with_author(tmp_path, client, key_resolver=_unavailable_key)  # ...no key resolves
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"live-but-keyless POST /generate-plan returned {status}, expected 200"
        payload = json.loads(body)
        assert payload["need_key"] is True, "a live-but-keyless client must report need_key (not None-only)"
        assert payload["results"] == {}, "the keyless path must not run the engine for any domain"
        # The honest need_key is returned BEFORE any author/live call — no spend on a keyless press.
        assert client.calls == [], "the author was called despite no key (a live call was attempted)"
        for domain in plan_schema.PLAN_DOMAINS:
            assert store.read(f"plan::{domain}", root=tmp_path / "store") == [], (
                f"the keyless path wrongly recorded a {domain} plan"
            )
        assert _still_alive(port), "the handler died after a live-but-keyless /generate-plan POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_format_agnostic_upload_feeds_the_plan_e2e(tmp_path):
    """E2E (arbitrary-format-in -> plan-out): an UNRECOGNIZED upload's extracted reading reaches the plan.

    Executes the full format-agnostic chain on ONE server with ONE mock no-train client (both
    lanes, 0 live API): POST /upload of an arbitrary `.xyz` -> the route's no-train extract lane ->
    a `clinical-notes` reading surfaced for confirm (lands 0); POST /confirm-extraction -> the
    reading lands via the UNCHANGED `store.append`; POST /generate-plan -> `router.summarize`
    DERIVES `active-issue-class` from that landed reading -> the author SEES it in its summary ->
    the workout plan ECHOES it. Asserts the reading landed, the author's received summary carries
    the upload-derived class, and the rendered plan is content-traceable to the arbitrary upload
    (`lower-limb-region` present from "knee pain"; an unrelated `upper-limb-region` absent — the
    render is driven by the upload, not baked).

    NOTE (scoping the wiring): the chain is wired only for readings that land under a
    summarize-recognized item name (here `clinical-notes` -> `active-issue-class`). A bare
    biomarker/lab item (e.g. `ferritin`) lands in the store but does NOT reach the author summary
    — see the session finding (summarize is a closed PII-boundary whitelist; the `biomarker::`
    trend feed is fed by no ingestion path). This E2E proves the chain is genuinely end-to-end for
    the recognized-item case, not that every extracted reading reaches the plan.
    """
    _seed_summary_store(tmp_path / "store")
    # The reading the arbitrary-format extraction yields: a medical-history clinical narrative;
    # `router.summarize` derives `active-issue-class` from the `clinical-notes` item.
    extracted = [{
        "item": "clinical-notes", "timepoint": "2026-05-01", "source": "medical",
        "value": "persistent left knee pain limiting deep squats",
    }]
    client = _FormatAgnosticClient(extracted)
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        # 1) Upload an arbitrary made-up format -> the no-train extract lane surfaces the readings
        #    for confirm (lands 0; confirm is the only landing path).
        ustatus, uctype, ubody = _post_upload_ct(port, "history.xyz", b"\x01\x02 arbitrary made-up format bytes")
        assert ustatus == 200 and uctype == "application/json", (
            f"the arbitrary-format upload did not surface a review payload ({ustatus}, {uctype})"
        )
        review = json.loads(ubody)
        assert review["readings"] == extracted, f"the extract lane did not surface the reading: {review}"
        assert store.read("clinical-notes", root=tmp_path / "store") == [], (
            "the upload auto-landed the reading (the confirm gate is broken)"
        )

        # 2) Operator confirms -> the reading lands via the UNCHANGED store.append sink.
        cstatus, _ = _post_confirm_extraction(port, review["readings"])
        assert cstatus == 200, f"confirm-extraction returned {cstatus}, expected 200"
        landed = store.read("clinical-notes", root=tmp_path / "store")
        assert landed and "knee" in str(landed[-1]["value"]), "the confirmed reading did not land in the store"

        # 3) Generate the plan -> summarize includes the landed reading -> the author sees it.
        gstatus, gbody = _post_generate_plan(port)
        assert gstatus == 200, f"generate-plan returned {gstatus}, expected 200"
        payload = json.loads(gbody)
        assert payload["results"]["workout"] == "recorded", f"workout did not record: {payload['results']}"

        # The author's RECEIVED summary carries the class DERIVED from the arbitrary upload —
        # proving the format-agnostic reading reached the author INPUT (not just the store).
        seen = client.author_summaries.get("workout")
        assert seen is not None and seen.get("active-issue-class") == "lower-limb-region", (
            f"the upload-derived reading did not reach the author summary: {seen}"
        )
        # plan-out content-traceable: the rendered plan reflects the upload-derived class, and an
        # unrelated class is ABSENT (the render is driven by the arbitrary upload, not baked).
        assert "lower-limb-region" in payload["plan_html"], "the rendered plan does not reflect the uploaded reading"
        assert "upper-limb-region" not in payload["plan_html"], "an unrelated class leaked (render not upload-driven)"
    finally:
        srv.shutdown()
        srv.server_close()


class _TrendEchoClient:
    """One mock no-train client for BOTH lanes (0 live API): extract_readings + author.

    `extract_readings` returns the fixed lab readings; `author` ECHOES the de-identified
    `recent-trend-direction` the summary carries into the workout plan (so the rendered plan is
    content-traceable to the lab trend), and records the summary it saw. Non-workout domains
    return the thin-library sentinel (an honest no-plan) to keep the E2E on the traceable path.
    """

    def __init__(self, extracted):
        self._extracted = list(extracted)
        self.author_summaries = {}

    def extract_readings(self, file_content, media_type):
        return list(self._extracted)

    def author(self, domain, summary):
        self.author_summaries[domain] = summary
        if domain == "workout":
            trend = summary.get("recent-trend-direction") or "flat"
            return {"specialist": "personal-trainer", "recommendations": [
                _rec(f"address the {trend} marker trend in programming", "training",
                     "ACSM resistance-training guidelines 2024",
                     {"name": "Goblet squat", "sets": 3, "reps": "8-12",
                      "detail": f"recent trend: {trend}"})]}
        return {"specialist": f"{domain}-specialist", "thin_library": True}


def test_format_agnostic_lab_value_moves_the_plan_e2e(tmp_path):
    """E2E (lab-value-in -> plan-out): a confirmed registered biomarker TRENDS and reaches the plan.

    The dead-feed fix, end-to-end: upload an arbitrary `.xyz` -> the no-train extract lane surfaces
    TWO rising LDL readings (a real trend) -> POST /confirm-extraction lands them (bare AND the
    additive `biomarker::ldl` mirror) -> POST /generate-plan -> `router.summarize`'s
    recent-trend-direction goes `regressing` (rising LDL, a down-polarity marker) -> the author
    SEES it in its summary -> the workout plan reflects it. Content-traceable lab-in -> plan-out:
    the rising-LDL trend moves the plan OFF the default `flat`.

    Failing-capable / mutation-proof: drop the `confirm.land_confirmed` biomarker mirror and
    `biomarker::ldl` stays empty, recent-trend-direction reverts to `flat`, and the `regressing`
    assertions red (the exact dead-feed gap this fix closes).
    """
    _seed_summary_store(tmp_path / "store")
    rising_ldl = [
        {"item": "ldl", "timepoint": "2026-04-01", "source": "labs", "value": "90"},
        {"item": "ldl", "timepoint": "2026-05-01", "source": "labs", "value": "140"},
    ]
    client = _TrendEchoClient(rising_ldl)
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        # 1) arbitrary-format upload -> the extract lane surfaces the two LDL readings for confirm.
        ustatus, uctype, ubody = _post_upload_ct(port, "labs.xyz", b"\x01 arbitrary lab export bytes")
        assert ustatus == 200 and uctype == "application/json", (
            f"the arbitrary-format lab upload did not surface a review payload ({ustatus}, {uctype})"
        )
        review = json.loads(ubody)
        assert review["readings"] == rising_ldl, f"the extract lane did not surface the readings: {review}"

        # 2) confirm -> both land bare AND mirror into biomarker::ldl (two timepoints -> a trend).
        cstatus, _ = _post_confirm_extraction(port, review["readings"])
        assert cstatus == 200, f"confirm-extraction returned {cstatus}, expected 200"
        mirrored = store.read("biomarker::ldl", root=tmp_path / "store")
        assert len(mirrored) == 2, (
            f"the confirmed LDL readings did not mirror into the biomarker:: trend feed: {mirrored}"
        )

        # 3) generate-plan -> the rising-LDL trend reaches the author summary + the rendered plan.
        gstatus, gbody = _post_generate_plan(port)
        assert gstatus == 200, f"generate-plan returned {gstatus}, expected 200"
        payload = json.loads(gbody)
        assert payload["results"]["workout"] == "recorded", f"workout did not record: {payload['results']}"
        seen = client.author_summaries.get("workout")
        assert seen is not None and seen.get("recent-trend-direction") == "regressing", (
            f"the lab trend did not reach the author summary (still default flat?): "
            f"{seen and seen.get('recent-trend-direction')}"
        )
        # plan-out content-traceable: the rendered plan carries the lab-driven trend, NOT the default.
        assert "recent trend: regressing" in payload["plan_html"], "the plan does not reflect the lab trend"
        assert "recent trend: flat" not in payload["plan_html"], (
            "the plan still shows the default flat — the lab value did not move it"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def _healthkit_rhr_xml(pairs):
    """Apple-Health export.xml bytes carrying one RestingHeartRate record per (day, value)."""
    rows = "".join(
        f' <Record type="HKQuantityTypeIdentifierRestingHeartRate" startDate="{d} 08:00:00 -0500" value="{v}"/>\n'
        for d, v in pairs
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
            + rows + "</HealthData>\n").encode()


def test_wearable_upload_trend_moves_the_plan_e2e(tmp_path):
    """E2E (wearable-in -> plan-out): a recognized healthkit upload TRENDS and reaches the plan.

    The wearable dead-feed fix, end-to-end: upload a RECOGNIZED Apple-Health export.xml carrying
    rising RHR over two days (a real trend) -> the route's wearable arm auto-lands it via the frozen
    `ingest.run` AND mirrors `biomarker::rhr` (the captured-readings mirror) -> POST /generate-plan
    -> `router.summarize`'s recent-trend-direction goes `regressing` (rising RHR, a down-polarity
    marker) -> the author SEES it in its summary -> the workout plan reflects it. Content-traceable
    wearable-in -> plan-out: the rising-RHR trend moves the plan OFF the default `flat`.

    Failing-capable / mutation-proof: drop the `route_upload` biomarker mirror and `biomarker::rhr`
    stays empty, recent-trend-direction reverts to `flat`, and the `regressing` assertions red (the
    wearable dead-feed gap this fix closes — the operator's dominant data, ~6113 healthkit readings).
    """
    _seed_summary_store(tmp_path / "store")
    client = _TrendEchoClient([])  # the extract lane is unused (a recognized format auto-lands)
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        # 1) recognized wearable upload -> auto-lands via ingest.run AND mirrors the registered marker.
        ustatus, _ = _post_upload(
            port, "export.xml", _healthkit_rhr_xml([("2026-04-01", "50"), ("2026-05-01", "70")])
        )
        assert ustatus == 200, f"wearable upload returned {ustatus}, expected 200"
        mirrored = store.read("biomarker::rhr", root=tmp_path / "store")
        assert len(mirrored) == 2, (
            f"the wearable RHR readings did not mirror into the biomarker:: trend feed: {mirrored}"
        )

        # 2) generate-plan -> the rising-RHR trend reaches the author summary + the rendered plan.
        gstatus, gbody = _post_generate_plan(port)
        assert gstatus == 200, f"generate-plan returned {gstatus}, expected 200"
        payload = json.loads(gbody)
        assert payload["results"]["workout"] == "recorded", f"workout did not record: {payload['results']}"
        seen = client.author_summaries.get("workout")
        assert seen is not None and seen.get("recent-trend-direction") == "regressing", (
            f"the wearable trend did not reach the author summary (still default flat?): "
            f"{seen and seen.get('recent-trend-direction')}"
        )
        # plan-out content-traceable: the rendered plan carries the wearable-driven trend, NOT default.
        assert "recent trend: regressing" in payload["plan_html"], "the plan does not reflect the wearable trend"
        assert "recent trend: flat" not in payload["plan_html"], (
            "the plan still shows the default flat — the wearable value did not move it"
        )
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# PR #274 review fixes — BUG1 (thread survival on author ImportError), SEC1 (CSRF
# content-type gate), TEST1 (cross-domain additive-AE hold), TEST3 (production
# None store_root). Fixture-driven, 0 live spend.
# --------------------------------------------------------------------------- #


class _ImportErrorAuthorClient:
    """A live-shaped client whose author() raises ImportError — the un-installed-SDK pre-live state."""

    def __init__(self):
        self.calls = []

    def author(self, domain, summary):
        self.calls.append(domain)
        raise ImportError("anthropic SDK is not installed")


class _AdditiveAEClient:
    """A mock author declaring a SHARED additive-AE class on BOTH the supplement + the peptide.

    The cross-domain additive-AE screen must HOLD the supplement (the safe no-stack default) rather
    than ship both a supplement and a peptide whose declared additive-AE classes compose. The shared
    class is declared in the envelope's `reconciliation.ae_profile` (lifted into the candidate `meta`
    by compute_plan, read by the orchestrator's screen). Non-compound domains return thin-library.
    """

    def __init__(self):
        self.calls = []

    def author(self, domain, summary):
        self.calls.append(domain)
        ae = {"reconciliation": {"ae_profile": {"additive_classes": ["bleeding-risk"]}}}
        if domain == "supplements":
            return {"specialist": "supplement-specialist", "recommendations": [
                _rec("supplement high-dose fish oil daily", "supplementation",
                     "Examine.com omega-3 monograph 2024",
                     {"name": "High-dose fish oil", "dose": "4 g", "timing": "daily"})], **ae}
        if domain == "peptides":
            return {"specialist": "peptide-specialist", "recommendations": [
                _rec("run bpc-157 for localized tissue support", "peptide-therapy",
                     "vault/library/peptides/bpc-157 research-report 2026",
                     {"compound": "BPC-157", "dose": "250 mcg", "route": "subcutaneous"})], **ae}
        return {"specialist": f"{domain}-specialist", "thin_library": True}


def test_generate_plan_author_importerror_degrades_thread_survives(tmp_path):
    """BUG1 (first-press killer): an author ImportError (un-installed SDK) degrades, never drops the thread.

    The documented pre-live state: the operator connects a key (so `_key_available()` passes) but the
    anthropic SDK is not installed, so `ModelClient.author` -> `_client()` raises ImportError. Without
    a thread-survival guard this escapes all catches and DROPS the request thread (RemoteDisconnected,
    no response). The handler must instead answer an honest degraded response — a 200 with each domain
    surfacing an honest 'model-backend-unavailable' reason, 0 plans recorded — and stay alive.
    Failing-capable: remove the per-domain ImportError catch + the outer guard and this reds (no
    response / a 5xx / a dropped connection).
    """
    _seed_summary_store(tmp_path / "store")
    srv, port = _server_with_author(tmp_path, _ImportErrorAuthorClient())  # resolving key + live-shaped client
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"an author ImportError returned {status} (dropped thread / 5xx?), expected 200"
        payload = json.loads(body)  # a valid JSON response came back -> the thread was NOT dropped
        assert payload["need_key"] is False, "a resolving key must not report need_key"
        assert set(payload["results"]) == set(plan_schema.PLAN_DOMAINS)
        assert all(v == "model-backend-unavailable" for v in payload["results"].values()), payload["results"]
        for domain in plan_schema.PLAN_DOMAINS:
            assert store.read(f"plan::{domain}", root=tmp_path / "store") == [], f"{domain} wrongly recorded"
        assert _still_alive(port), "the handler died after an author ImportError (thread dropped)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_rejects_non_json_content_type_415(tmp_path):
    """SEC1 (CSRF / forced-spend): a non-application/json POST is refused 415 — no spend, no plan.

    `/generate-plan` (like `_save_key` / `_do_confirm_extraction`) gates on Content-Type: a cross-site
    CORS-simple `text/plain` POST is refused 415 BEFORE the no-key check / any author call, so a forged
    cross-site POST cannot drive spend on the operator's key + plan writes (a genuine application/json
    cross-site POST forces a preflight the server never answers). The author is never reached.
    Failing-capable: drop the Content-Type gate and a text/plain POST drives generation.
    """
    _seed_summary_store(tmp_path / "store")
    client = _MockAuthorClient(_domain_envelopes())
    srv, port = _server_with_author(tmp_path, client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_generate_plan(port, content_type="text/plain")
        assert status == 415, f"a text/plain /generate-plan POST returned {status}, expected 415"
        assert client.calls == [], "the author was reached despite the rejected content-type (forced spend)"
        for domain in plan_schema.PLAN_DOMAINS:
            assert store.read(f"plan::{domain}", root=tmp_path / "store") == [], f"{domain} wrongly recorded"
        assert _still_alive(port), "the handler died after a rejected content-type POST"
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_holds_cross_domain_additive_ae_pair(tmp_path):
    """TEST1 (cross-domain safety): a supplement+peptide additive-AE pair is HELD, not both shipped.

    The in-app button runs the FROZEN cross-domain orchestrator (orchestrate.generate_plans), so the
    supplement<->peptide additive-AE screen runs over the per-domain candidates BEFORE recording. Both
    authors declare a SHARED additive-AE class (`bleeding-risk`); the screen HOLDS the supplement (the
    safe no-stack default — no liaison adjudicator is wired in-app to release it). The peptide records;
    the supplement does NOT — proving the in-app path no longer bypasses the cross-domain safety layer.
    Failing-capable: revert the in-app path to the per-domain generate_plan loop and BOTH the supplement
    AND the peptide record (the cross-domain-safety bypass the TEST1 review finding flagged).
    """
    _seed_summary_store(tmp_path / "store")
    srv, port = _server_with_author(tmp_path, _AdditiveAEClient())
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"POST /generate-plan returned {status}, expected 200"
        results = json.loads(body)["results"]
        assert results["peptides"] == "recorded", f"the peptide did not record: {results}"
        assert results["supplements"] == orchestrate.ADDITIVE_AE_HELD, (
            f"the supplement was not held by the additive-AE screen (cross-domain bypass?): {results}"
        )
        today = datetime.date.today().isoformat()
        assert plan_schema.read_plan("peptides", today, tmp_path / "store")["plan"] is not None
        assert store.read("plan::supplements", root=tmp_path / "store") == [], "the held supplement was wrongly recorded"
    finally:
        srv.shutdown()
        srv.server_close()


def test_generate_plan_production_none_store_root_resolves_default(tmp_path, monkeypatch):
    """TEST3 (F1 class): the production None-store_root path resolves to store.DEFAULT_ROOT, no TypeError.

    The operator-entry build (`scripts/serve/__main__`) constructs the server with NO store_root, so
    `_do_generate_plan` runs with `self.store_root is None` and must resolve it to `store.DEFAULT_ROOT`
    (the S99 F1 showstopper class — an explicit None overriding a default and raising TypeError deep in
    the path). Builds the server WITHOUT store_root (+ a resolving key + a mock author), monkeypatches
    `store.DEFAULT_ROOT` to a tmp dir, POSTs /generate-plan, and asserts a coherent 200 (not degraded)
    with plans recorded into the resolved default root.
    """
    from scripts.store import store as store_mod

    default_root = tmp_path / "prod-default-store"
    monkeypatch.setattr(store_mod, "DEFAULT_ROOT", default_root)
    _seed_summary_store(default_root)
    srv = serve_server.build_server(
        0, client=_MockAuthorClient(_domain_envelopes()), key_resolver=_resolving_key,
    )  # no store_root -> the production __main__ shape
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, body = _post_generate_plan(port)
        assert status == 200, f"production None store_root returned {status}, expected 200"
        payload = json.loads(body)
        assert payload.get("degraded") is not True, f"the None store_root path degraded (TypeError?): {payload}"
        assert payload["results"] == {d: "recorded" for d in plan_schema.PLAN_DOMAINS}, payload["results"]
        today = datetime.date.today().isoformat()
        for domain in plan_schema.PLAN_DOMAINS:
            assert plan_schema.read_plan(domain, today, default_root)["plan"] is not None, (
                f"{domain} did not land into the resolved production default root"
            )
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T8 — the final-save care-agent review trigger (the crown-jewel
#   BOTH-legs egress): the review fires + delivers questions in the final-save
#   response (AC-1 E2E), the no-key 0-spend degrade (AC-5 E2E), the material-edit
#   re-trigger (AC-6), no-new-route / no-new-client (AC-7), and the loading-bar +
#   status surface under the Care-Assistant card (spec File Manifest / OQ-4).
#   Recording-mock/string-driven, 0 live spend.
# --------------------------------------------------------------------------- #

# The FORM fields that complete the first-run profile via the capture path (the field NAMES the
# markup submits, routed by data class): seven wired/derived-source tokens + the three
# safety-screen answers (form names `exercise-safety`/`phq2`/`apnea` -> the `safety-screen::*`
# markers). Distinct from `_COMPLETE_PROFILE` (which seeds the STORE ITEM names directly).
_CARE_FORM_FIELDS = {
    "date-of-birth": "1986-04-12",
    "bodyweight-kg": "82",
    "sex-for-dosing": "male",
    "equipment-access-class": "full-home-gym",
    "goal-domains": "Workout;Nutrition",
    "goal-targets": "Build strength and improve sleep",
    "goal-priority-order": "Workout, Nutrition, Supplements",
    "exercise-safety": "no",
    "phq2": "no",
    "apnea": "no",
}


class _CareReviewBackend:
    """A recording converse backend for the care-agent review E2E (0 live API).

    Records each `converse` request into `self.calls`; answers a curation request (the
    `rx-interaction-curation` task marker) with a scripted class proposal and any other request
    with a clarifying question. Distinguishing by request CONTENT (not call index) mirrors a real
    model and keeps the re-trigger assertion order-independent.
    """

    def __init__(self, *, question="What is your top training priority this cycle?",
                 rx_class="cyp3a4-pgp", confident=True):
        self.question = question
        self.rx_class = rx_class
        self.confident = confident
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if "rx-interaction-curation" in json.dumps(messages):
            return {"reply": "Please confirm these interaction classes.",
                    "extraction": [{"rx-interaction-class": self.rx_class,
                                    "confident": self.confident}]}
        return {"reply": self.question, "extraction": []}


def _server_with_care_review(tmp_path, backend, *, key_resolver=_resolving_key):
    """Server over tmp roots + a recording converse client + (by default) a key that RESOLVES."""
    from scripts.model.client import ModelClient

    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=ModelClient(backend=backend),
        key_resolver=key_resolver,
    )
    return srv, srv.server_address[1]


def _clarifying_requests(backend):
    return [c for c in backend.calls if "care-clarifying-review" in json.dumps(c)]


def _curation_requests(backend):
    return [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)]


def test_final_save_fires_care_review_questions_in_response(tmp_path):
    """AC-1 (E2E): a complete-profile final save with a key fires the review + delivers questions."""
    backend = _CareReviewBackend()
    srv, port = _server_with_care_review(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        status, body = _post_fields(port, dict(_CARE_FORM_FIELDS))
        assert status == 200, f"final-save POST returned {status}, expected 200"
        data = json.loads(body)
        assert data.get("deferred") is False, f"a keyed complete-profile save deferred: {data}"
        assert len(data["questions"]) >= 1, "the final-save response carried no clarifying question"
        assert len(_clarifying_requests(backend)) == 1, "the review did not record ONE clarifying request"
    finally:
        srv.shutdown()
        srv.server_close()


def test_final_save_no_key_defers_zero_spend(tmp_path):
    """AC-5 (E2E): a complete-profile final save with NO resolvable key makes 0 model calls."""
    backend = _CareReviewBackend()
    srv, port = _server_with_care_review(tmp_path, backend, key_resolver=_unavailable_key)
    _serve_in_thread(srv)
    try:
        status, body = _post_fields(port, dict(_CARE_FORM_FIELDS))
        assert status == 200, f"keyless final-save POST returned {status}, expected 200"
        assert backend.calls == [], "a keyless final save made a model call (0-spend breach)"
        # Degrades to the existing app-shell HTML re-render — NOT a fabricated question payload.
        assert SPA_NAV_MARKER in body, "the keyless final save is not the honest HTML re-render"
    finally:
        srv.shutdown()
        srv.server_close()


def test_material_my_info_edit_retriggers_review(tmp_path):
    """AC-6: a SECOND /upload form-capture (a med / safety edit, profile staying complete) re-fires."""
    backend = _CareReviewBackend()
    srv, port = _server_with_care_review(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        first = dict(_CARE_FORM_FIELDS)
        first["rx-interaction-classes"] = "atorvastatin 20mg"  # a raw med -> record-only scaffold
        status, _ = _post_fields(port, first)
        assert status == 200, f"first final-save POST returned {status}, expected 200"
        # A material My-Info edit: change a safety answer + a med (the profile stays complete).
        edit = {"apnea": "no", "rx-interaction-classes": "atorvastatin 20mg; metformin 500mg"}
        status, _ = _post_fields(port, edit)
        assert status == 200, f"material-edit POST returned {status}, expected 200"
        assert len(_clarifying_requests(backend)) >= 2, (
            "the material edit did not re-fire the clarifying review (fires only on the "
            "incomplete->complete edge?)"
        )
        assert len(_curation_requests(backend)) >= 2, "the material edit did not re-curate the meds"
    finally:
        srv.shutdown()
        srv.server_close()


def test_care_review_adds_no_route_no_new_client(tmp_path):
    """AC-7: no 8th route, no second ModelClient / SDK import — the review reuses self.client."""
    care_src = (REPO_ROOT / "scripts" / "serve" / "care_review.py").read_text()
    server_src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    # care_review constructs no client and imports no SDK / outbound HTTP client.
    assert "ModelClient(" not in care_src, "care_review constructs a second ModelClient"
    assert "anthropic" not in care_src, "care_review imports the model-client SDK"
    # server.py's ModelClient constructions are the per-route lazy fallbacks only (no-client-injected
    # default): `_do_chat` + `_do_care_chat` = 2. Both are the same `self.client or ModelClient()` shape
    # (the SDK import + key resolve stay lazy inside the backend); T8's care-review adds none.
    assert server_src.count("ModelClient(") == 2, "an unexpected ModelClient construction was added to server.py"
    # T8 (care-review) added NO route — it fires inside the existing /upload final-save path. The
    # POST route branches match on `self.path == "/..."`: /chat, /care-chat, /settings/key,
    # /confirm-extraction, /confirm-curation (T10), /generate-plan = 6. (/care-chat is the post-unlock
    # profile-aware Care Assistant conversation; do_GET matches on a query-stripped local `path` so a
    # cache-bust `/?v=2` URL serves the app rather than 404 — it does not use `self.path ==`.)
    assert 'self.path == "/care-review"' not in server_src, "T8 added a /care-review route"
    assert server_src.count('self.path == "/') == 6, "the POST route-table branch count changed unexpectedly"
    assert '_LOOPBACK = "127.0.0.1"' in server_src, "the loopback bind literal changed"
    # An unknown POST still 404s (the route table is unchanged).
    srv, port = _server_with_care_review(tmp_path, _CareReviewBackend())
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/not-a-route", body=b"", headers={"Content-Type": "application/json"})
        unk = conn.getresponse()
        unk.read()
        conn.close()
        assert unk.status == 404, f"an unknown POST returned {unk.status}, expected 404"
    finally:
        srv.shutdown()
        srv.server_close()


def test_final_save_response_drives_care_assistant_loading_bar_and_status(tmp_path):
    """Spec File Manifest app_view.html / OQ-4 (tied to AC-1): the loading bar + status under the card.

    (a) STRUCTURAL reuse proof — the served SPA carries the `.chat-progress` status element + the
        `.bar`/`.spin` loading-bar surface in the Care-Assistant card region (present on the tree,
        0 new app_view.html markup). (b) BEHAVIORAL wiring — the care-review final-save response
        carries a `progress`/status field (the "what it is doing" text) alongside the >= 1 clarifying
        chat turn, in the per-turn-receipt shape `_progressUpdate` consumes (FAILING-CAPABLE:
        removing the status field reds (b)).
    """
    backend = _CareReviewBackend()
    srv, port = _server_with_care_review(tmp_path, backend)
    _serve_in_thread(srv)
    try:
        # (b) BEHAVIORAL: the final-save response carries a progress/status field + a clarifying turn.
        status, body = _post_fields(port, dict(_CARE_FORM_FIELDS))
        assert status == 200
        data = json.loads(body)
        assert data["questions"], "the care-review response carried no clarifying chat turn"
        assert data["progress"] and data["progress"].get("status"), (
            "the care-review final-save response carries no progress/status field"
        )
        # (a) STRUCTURAL: the served SPA carries the loading-bar/status reuse surface under the card.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        spa = conn.getresponse().read().decode("utf-8")
        conn.close()
        assert "chat-progress" in spa and "Care Assistant" in spa, "the Care-Assistant status surface is absent"
        assert 'class="bar"' in spa and "spin" in spa, "the loading-bar surface is absent under the card"
    finally:
        srv.shutdown()
        srv.server_close()


def test_data_root_env_var_serves_a_scratch_store_for_testing(tmp_path, monkeypatch):
    """`APLUS_DATA_ROOT` threads scratch store/dna/scaffold roots into build_server (safe testing).

    Set the env var and `main` serves against a throwaway store under that base instead of the real
    `vault/`, so the intake/plan flow can be tested repeatedly without touching the operator's data.
    Unset -> no roots (the production `vault/` defaults). Asserted via a spy `build` that captures the
    kwargs and aborts before the serve loop (binds no socket, makes no live call).
    """
    from scripts.serve import __main__ as entry

    # unset -> no roots override (production defaults)
    monkeypatch.delenv("APLUS_DATA_ROOT", raising=False)
    assert entry._data_roots() == {}, "an unset APLUS_DATA_ROOT should yield no roots override"

    # set -> derived scratch roots under the base
    monkeypatch.setenv("APLUS_DATA_ROOT", str(tmp_path / "scratch"))
    roots = entry._data_roots()
    assert roots["store_root"] == tmp_path / "scratch" / "store", f"store_root not under the base: {roots}"
    assert roots["dna_root"] == tmp_path / "scratch" / "dna" and roots["scaffold_root"] == tmp_path / "scratch" / "scaffold"

    captured = {}

    class _Abort(Exception):
        pass

    def _spy_build(port, *, client=None, **kwargs):
        captured.update(kwargs)
        raise _Abort

    try:
        entry.main(build=_spy_build)
    except _Abort:
        pass
    else:
        raise AssertionError("main did not call build (the spy never aborted)")
    assert captured.get("store_root") == tmp_path / "scratch" / "store", (
        "main did not thread the APLUS_DATA_ROOT scratch store into build_server"
    )
