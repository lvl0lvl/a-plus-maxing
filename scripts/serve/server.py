"""Loopback-only intake HTTP server (ADR-0013-T1 skeleton + ADR-0013-T4 upload route).

`build_server(port)` constructs a stdlib `http.server.ThreadingHTTPServer` bound to
`("127.0.0.1", port)` ONLY — never `0.0.0.0`/`""`/a routable interface (ADR-0013
Confirmation 1: the first network surface the system opens, off-machine-unreachable
by construction). The bind literal lives in exactly one place (`_LOOPBACK`) so the
downstream tasks extend the handler without re-specifying the bind.

The handler serves GET `/` with the existing intake wizard — the body IS
`generate.run('intake')`'s rendered HTML (the server adds a transport, not a new
wizard); a non-`/` GET returns 404. POST `/upload` (ADR-0013-T4) is a thin chain:
stage the multipart body (`multipart.stage_uploads`, ADR-0013-T2) -> route the
staged file into the UNCHANGED `ingest.run`/`dna.land` seam (`route.route_upload`)
-> re-render the wizard via `generate.run('intake')` reflecting the new load-state.
The server serves NO generated artifact live — intake-only (ADR-0013 Falsification 3;
the route table is exactly {GET `/`, POST `/upload`}). `ADR-0013-T5` wraps the request
dispatch in `egress_guard.run` (the import here keeps that wrap point ready). Stopping
is `srv.shutdown()` + `srv.server_close()`, the clean operator-stop path.
"""

import io
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# The single loopback-bind site. Changing this away from 127.0.0.1 breaks the
# ADR-0013-T1 criterion-1 structural assertion + the off-machine-unreachable
# guarantee — non-negotiable (ADR-0013 Falsification 1).
_LOOPBACK = "127.0.0.1"

# The default operator port for `python -m scripts.serve` (OQ-2 fail-loud names it).
DEFAULT_PORT = 8765

# The egress guard is imported so the server-start path is guard-ready: ADR-0013-T5
# wraps the request dispatch in egress_guard.run; the wrap point exists from here.
from scripts.guard.egress_guard import run as _egress_run  # noqa: E402,F401


def _render_intake(*, store_root=None, dna_root=None):
    """Return the intake wizard HTML — the GET `/` body and the POST re-render body.

    Drives `generate.run('intake')` (which RE-READS the live store + dropzone
    load-state, so a re-render after an upload reflects the just-landed readings/files)
    and reads the produced file's text. The server is glue: the body is exactly the
    rendered wizard. `store_root`/`dna_root` are the test-seam roots the POST handler
    ingested into; None falls through to `generate.run`'s production defaults.
    """
    from scripts.generate.generate import run as generate_run

    return generate_run("intake", _root=store_root, _dna_root=dna_root).read_text()


class IntakeRequestHandler(BaseHTTPRequestHandler):
    """Serve the intake wizard at GET `/`; stage->route->re-render at POST `/upload`.

    GET `/` writes HTTP 200 + the `generate.run('intake')` body; any other GET 404s.
    POST `/upload` stages the multipart body, routes the staged file into the unchanged
    `ingest.run`/`dna.land` seam, and re-renders the wizard reflecting the new
    load-state. Any other POST 404s — the route table is intake-only {GET `/`, POST
    `/upload`}, never a directory listing or an artifact-serving route.

    Attributes:
        store_root: The time-series store root the POST handler ingests into and
            re-renders from (None -> the production `vault/store/` default).
        dna_root: The DNA dropzone the POST handler lands DNA into and re-renders from
            (None -> the production `vault/dna/raw/` default).
    """

    store_root = None
    dna_root = None

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self._write_html(200, _render_intake(store_root=self.store_root, dna_root=self.dna_root))

    def do_POST(self):
        if self.path != "/upload":
            self.send_error(404)
            return
        from scripts.serve import route
        from scripts.serve.multipart import stage_uploads

        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)

        with tempfile.TemporaryDirectory() as staging:
            staged = stage_uploads(self.headers.get("Content-Type"), io.BytesIO(body), staging)
            files = staged["files"]
            store_root = self.store_root
            dna_root = self.dna_root
            try:
                for file_part in files:
                    route.route_upload(file_part["path"], root=store_root, dna_root=dna_root)
            except (SystemExit, ValueError):
                # An ambiguous/unknown extension (`_detect_source` raises SystemExit) or a
                # fail-loud landing rejection (`dna.land`/the adapter raise ValueError) must
                # NOT kill the request handler: re-render the wizard so the operator can
                # pick a source / re-upload, rather than dropping the connection.
                self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))
                return

        # Re-render reflecting the new load-state (the store/dropzone were just written).
        self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))

    def _write_html(self, status, html):
        """Write an HTTP response with the HTML body (the single response-write site)."""
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        """Silence the default per-request stderr access log."""


def build_server(port, *, store_root=None, dna_root=None):
    """Construct the loopback-bound intake server on `port`.

    The POST `/upload` handler ingests into `store_root`/`dna_root` and re-renders the
    wizard from them; both default to None, which falls through to the production
    `vault/store/` / `vault/dna/raw/` defaults (so the operator entry `python -m
    scripts.serve` serves the real instance). Tests bind tmp roots so the E2E never
    touches the real store/dropzone.

    Args:
        port (int): The TCP port to bind on loopback; 0 picks an ephemeral port.
        store_root (str | Path, optional): The store root the POST handler ingests into.
        dna_root (str | Path, optional): The DNA dropzone the POST handler lands into.

    Returns:
        (ThreadingHTTPServer) A server bound to ("127.0.0.1", port). Stop it with
        `srv.shutdown()` + `srv.server_close()`.
    """
    handler = type("BoundIntakeRequestHandler", (IntakeRequestHandler,),
                   {"store_root": store_root, "dna_root": dna_root})
    return ThreadingHTTPServer((_LOOPBACK, port), handler)
