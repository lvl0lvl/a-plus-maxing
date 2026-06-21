"""Loopback-only intake HTTP server skeleton (ADR-0013-T1).

`build_server(port)` constructs a stdlib `http.server.ThreadingHTTPServer` bound to
`("127.0.0.1", port)` ONLY — never `0.0.0.0`/`""`/a routable interface (ADR-0013
Confirmation 1: the first network surface the system opens, off-machine-unreachable
by construction). The bind literal lives in exactly one place (`_LOOPBACK`) so the
downstream tasks (`ADR-0013-T2`/`T4`) extend the handler without re-specifying the
bind.

The handler serves GET `/` with the existing intake wizard — the body IS
`generate.run('intake')`'s rendered HTML (the server adds a transport, not a new
wizard); a non-`/` GET returns 404. `ADR-0013-T4` adds `do_POST` for `/upload` to
THIS handler; `ADR-0013-T5` wraps the request dispatch in `egress_guard.run` (the
import here keeps that wrap point ready). Stopping is `srv.shutdown()` +
`srv.server_close()`, the clean operator-stop path that frees the listener.
"""

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


def _render_intake():
    """Return the intake wizard HTML — the GET `/` body (no new markup added).

    Drives `generate.run('intake')` (which renders the wizard from the live store +
    dropzone load-state) and reads the produced file's text. The server is glue: the
    body is exactly the rendered wizard.
    """
    from scripts.generate.generate import run as generate_run

    return generate_run("intake").read_text()


class IntakeRequestHandler(BaseHTTPRequestHandler):
    """Serve the intake wizard at GET `/`; 404 every other route.

    The published handler `ADR-0013-T2`/`T4` extend (`do_POST` for `/upload` lands
    in `ADR-0013-T4`). GET `/` writes HTTP 200 + the `generate.run('intake')` body;
    any other path 404s — the server publishes exactly the GET `/` route, never a
    directory listing.
    """

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = _render_intake().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        """Silence the default per-request stderr access log."""


def build_server(port):
    """Construct the loopback-bound intake server on `port`.

    Args:
        port (int): The TCP port to bind on loopback; 0 picks an ephemeral port.

    Returns:
        (ThreadingHTTPServer) A server bound to ("127.0.0.1", port) with the
        published `IntakeRequestHandler`. Stop it with `srv.shutdown()` +
        `srv.server_close()`.
    """
    return ThreadingHTTPServer((_LOOPBACK, port), IntakeRequestHandler)
