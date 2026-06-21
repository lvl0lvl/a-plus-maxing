"""Route + lifecycle tests for the loopback-only intake server (ADR-0013-T1).

AC-2: GET `/` against the running handler returns HTTP 200 + the intake wizard
HTML (the `generate.run('intake')` body), proved by the wizard title string in the
body — not a directory listing. A non-`/` GET returns 404. AC-4: the operator-stop
lifecycle closes the listener cleanly (a fresh bind to the freed port succeeds),
and `main` reads no stdin.
"""

import http.client
import socket
import subprocess
import sys
import threading
from pathlib import Path

from scripts.serve import server as serve_server

REPO_ROOT = Path(__file__).resolve().parents[2]

# The intake wizard title (vault/design/templates/intake.py render() <title>) the
# GET `/` body must carry — proves the route serves the wizard, not a dir listing.
WIZARD_TITLE = "A+ Maxing — Build your plan"


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


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
