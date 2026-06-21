"""`python -m scripts.serve` — the loopback intake server operator entry (ADR-0013-T1).

`main(argv=None)` builds the loopback-bound server on the default port and serves
until the operator stops it (Ctrl-C). It reads no stdin and opens only the single
`127.0.0.1` listener — the browser analog of `scripts.ingest`'s file-load entry, the
one loopback-server carve-out ADR-0013 grants. On a port collision it exits non-zero
fail-loud (naming the collision + the alternate-port instruction), never a silent
rebind to another port (OQ-2) — the operator must learn the URL would change. On
Ctrl-C it stops the listener cleanly so no half-open socket is left behind.
"""

import signal
import sys
import threading

from scripts.serve import server as serve_server


def main(argv=None):
    """Build the loopback server on the default port and serve until stopped.

    On a port collision, exit non-zero with a fail-loud message; on Ctrl-C (SIGINT),
    stop the listener cleanly. `serve_forever` runs on a worker thread so the main
    thread can drive `shutdown()` (which must run off the serving thread).

    Args:
        argv (list, optional): Argument vector; defaults to `sys.argv[1:]`.

    Returns:
        (int) 0 on a clean operator-stop.
    """
    port = serve_server.DEFAULT_PORT
    try:
        srv = serve_server.build_server(port)
    except OSError as exc:
        raise SystemExit(
            f"Port {port} is already in use ({exc}); the intake server did not start. "
            f"Free port {port}, or run with a different port once that option lands. "
            f"No server is listening."
        )

    host, bound_port = srv.server_address
    print(f"Serving the intake wizard at http://{host}:{bound_port}/  (Ctrl-C to stop)")

    stop = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: stop.set())

    worker = threading.Thread(target=srv.serve_forever, daemon=True)
    worker.start()
    try:
        stop.wait()
    finally:
        srv.shutdown()
        srv.server_close()
        worker.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())
