"""No-egress proof over the POST `/upload` request dispatch (ADR-0013-T5).

PROVES the upload->ingest->re-render request path is egress-free, by running the
production POST `/upload` dispatch (stage -> route -> re-render, over a `tmp_path`
store) INSIDE a zero-arg closure passed to the OS-level egress guard
`egress_guard.run`. The guard is the TEST HARNESS, never a per-request production
wrapper: it FORKS a child that applies the OS no-network sandbox, runs the closure,
and `os._exit`s — `run` returns ONLY a bool to the parent
(scripts/guard/egress_guard.py:82,102-119). The re-rendered HTML produced in the
child never crosses back, so the guard cannot wrap the production handler (which must
return a response). The production server is egress-free BY CONSTRUCTION (it makes no
outbound calls) — Half C proves it with a grep that `scripts/serve/` imports no
outbound HTTP client.

Three falsifiable halves (ADR-0013 Confirmation-2 / Falsification-2; the ADR-0001
"0 outbound calls carrying store content" boundary on the new network surface):
- Half A: the REAL dispatch over a `tmp_path` store is egress-clean (truthy) AND the
  store-write side-effects persist on disk (the readings landed) — meaningful, not a
  no-op closure.
- Half B (failing-capable): an INJECTED outbound call into the dispatch closure drives
  `egress_guard.run` to FAIL (falsy) — proving the guard intercepts the request code
  path, so the truthy Half-A result is attributable to the sandbox, not an offline host.
- Half C: `scripts/serve/` imports 0 outbound HTTP clients — egress-free by
  construction (NOT by a production `egress_guard.run` wrap, which is impossible here).
"""

import io
import platform
import socket
from email.message import Message
from pathlib import Path

import pytest

from scripts.guard.egress_guard import run
from scripts.serve.server import IntakeRequestHandler
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

DARWIN_ONLY = pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="OS-level isolation binding is exercised on the host OS (Darwin here)",
)

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"

# The outbound-client surface an egress path would carry at import time. The grep
# (Half C) reds the moment any of these appears in `scripts/serve/`.
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)


def _require_network():
    """Skip unless a direct unguarded connect succeeds — so a falsy run is the sandbox.

    Mirrors the egress-guard suite's negative control: attributes the egress-deny
    fail direction to the OS sandbox, not to an offline host.
    """
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3).close()
    except OSError:
        pytest.skip("no network — egress deny not exercisable")


def _healthkit_xml_bytes(*, day="2026-05-01", value="55"):
    """Return a minimal Apple-Health `export.xml` carrying one HRV record."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
        f' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        f' startDate="{day} 08:00:00 -0500" value="{value}"/>\n'
        '</HealthData>\n'
    ).encode()


def _multipart_upload(filename, payload):
    """Build a single-file multipart/form-data body for the `export` field."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="export"; filename="{filename}"\r\n\r\n').encode()
    out += payload
    out += b"\r\n"
    out += f"--{BOUNDARY}--\r\n".encode()
    return bytes(out)


def _build_post_handler(store_root, dna_root, body):
    """Instantiate the production POST `/upload` handler over tmp roots + a request body.

    Bypasses `BaseHTTPRequestHandler.__init__`'s socket-bound setup so the test drives
    the EXACT production `do_POST` dispatch (stage -> route -> re-render) in-process,
    over a `tmp_path` store — no listening socket (the closure runs inside the
    no-network sandbox, where no socket is reachable). The handler reads `rfile`/
    `headers`/`path` and writes `wfile` exactly as the live server does.
    """
    bound = type("BoundIntakeRequestHandler", (IntakeRequestHandler,),
                 {"store_root": store_root, "dna_root": dna_root})
    handler = bound.__new__(bound)
    handler.path = "/upload"
    handler.command = "POST"
    handler.requestline = "POST /upload HTTP/1.1"
    handler.request_version = "HTTP/1.1"
    headers = Message()
    headers["Content-Type"] = f"multipart/form-data; boundary={BOUNDARY}"
    headers["Content-Length"] = str(len(body))
    handler.headers = headers
    handler.rfile = io.BytesIO(body)
    handler.wfile = io.BytesIO()
    return handler


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 / AC-2: failing-capable 0-egress proof over the real dispatch
# --------------------------------------------------------------------------- #


@DARWIN_ONLY
def test_real_upload_dispatch_is_egress_clean_with_side_effects(tmp_path):
    """AC-1 / Half A: the real upload->ingest->re-render dispatch is egress-clean.

    Runs the PRODUCTION POST `/upload` dispatch (stage -> route -> re-render) over a
    `tmp_path` store inside ONE zero-arg closure, passes it to `egress_guard.run`, and
    asserts truthy (0 outbound calls across the whole dispatch). Then asserts the
    store-write side-effects PERSIST on disk under `tmp_path` (the HRV reading landed
    via the unchanged `ingest.run`) — so the truthy result is meaningful, not a closure
    that did nothing. The closure does the write in the guard's forked child; the test
    re-reads the disk store in the PARENT after the guarded run, mirroring the
    production re-render's read-from-disk pattern (the guard returns only a bool).
    """
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"
    body = _multipart_upload("export.xml", _healthkit_xml_bytes(value="55"))

    def real_dispatch():
        # The production stage -> route -> re-render request handler, over tmp roots.
        _build_post_handler(store_root, dna_root, body).do_POST()

    assert run(real_dispatch), "the real upload->ingest->re-render dispatch was not egress-clean"

    # The side-effects persist on disk: the readings actually landed (not a no-op).
    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1 and hrv[0]["source"] == "healthkit", (
        "the guarded dispatch did not land the HRV reading — the egress-clean result is vacuous"
    )
    assert hrv[0]["value"] == 55.0


@DARWIN_ONLY
def test_injected_outbound_call_drives_the_guard_to_fail(tmp_path):
    """AC-2 / Half B (failing-capable): an injected outbound call flips the guard to FAIL.

    Wraps a dispatch that performs the real upload->ingest->re-render AND THEN makes
    ONE injected outbound `socket.create_connection`, and asserts `egress_guard.run`
    returns falsy. This proves the guard intercepts the request code path (it is not a
    guard that always passes), so Half A's truthy result is attributable to the OS
    sandbox, not an offline host. `_require_network` mirrors the egress-guard suite's
    negative control so the fail direction is the sandbox, not a dead network.
    """
    _require_network()
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"
    body = _multipart_upload("export.xml", _healthkit_xml_bytes(value="55"))

    def dispatch_with_injected_egress():
        _build_post_handler(store_root, dna_root, body).do_POST()
        # Injected outbound call into the request path — a real network attempt the
        # OS-level guard surfaces (not a mocked stub the guard never sees).
        socket.create_connection(("1.1.1.1", 53), timeout=3)

    assert not run(dispatch_with_injected_egress), (
        "an injected outbound call did NOT flip the guard to FAIL — the guard is not "
        "failing-capable over the request path (proves nothing)"
    )


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-3: production egress-free by construction (grep proof)
# --------------------------------------------------------------------------- #


def test_serve_layer_imports_no_outbound_client():
    """AC-3 / Half C: `scripts/serve/` carries 0 outbound HTTP clients.

    The production server makes no outbound calls — it is egress-free BY CONSTRUCTION,
    NOT by an `egress_guard.run` production wrap (which is impossible: the guard's
    forked child's re-rendered response never returns to the parent handler). Asserts
    no module under `scripts/serve/` imports/uses an outbound client
    (`socket.create_connection`, `urllib.request`, `http.client`, `requests`, `httpx`).
    Reds the moment a future task sneaks an outbound import into the serve layer — the
    standing guard against an egress path appearing on the network surface.
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    for py in serve_dir.glob("*.py"):
        src = py.read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, (
                f"{py.name} references an outbound client ({marker!r}) — the serve "
                f"layer must be egress-free by construction (no outbound calls)"
            )
