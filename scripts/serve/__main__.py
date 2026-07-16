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

from scripts.model.client import ModelClient
from scripts.runner import metered_dispatch
from scripts.serve import alpha_config
from scripts.serve import server as serve_server
from scripts.serve.intake_aggregate import AggregatingDeidClient


def _data_roots():
    """Optional scratch-store roots for testing, from the `APLUS_DATA_ROOT` env var (non-destructive).

    Set `APLUS_DATA_ROOT=/tmp/aplus-test` to serve the intake/plan flow against a THROWAWAY
    store/dna/scaffold under that base instead of the real `vault/` — so the whole flow (wizard ->
    intake -> unlock -> care review -> care chat -> plan) can be tested repeatedly, and reset by
    deleting the dir, WITHOUT touching the operator's real data. Unset -> the production `vault/`
    defaults (`build_server`'s None roots). To test the RETURNING-operator flow, first copy the real
    store in: `cp -R vault/store $APLUS_DATA_ROOT/store`.
    """
    import os
    from pathlib import Path

    base = os.environ.get("APLUS_DATA_ROOT")
    if not base:
        return {}
    root = Path(base)
    return {"store_root": root / "store", "dna_root": root / "dna", "scaffold_root": root / "scaffold"}


def main(argv=None, *, build=serve_server.build_server, client_factory=ModelClient):
    """Build the loopback server on the default port and serve until stopped.

    Wires the production no-train model client into the server (ADR-0030-T3 factory
    wiring): `client_factory()` constructs a `ModelClient` (lazy — the SDK import + key
    resolve happen at call time, never at construction, so this makes no live call) and
    passes it to `build`, so the operator-entry server's `self.client` is live and a POST
    `/upload` of an unrecognized format extracts via the no-train lane. Tests build the
    server WITHOUT a client (`build_server()` -> `self.client=None`), so an unknown upload
    re-renders rather than making a metered call — extraction is wired here, at the entry
    point, not by a handler self-default.

    Also arms the loop-live metered lane (ADR-0049-T1): the D5 shared-key bridge closes the
    no-BYO key default, and the SAME client is wired as the server's metered `loop_dispatch`
    + `loop_deid_client`, so an in-app `/plan-loop` dispatches specialists on the shared
    `a-plus-maxing-api-key` metered lane (0-spend at construct; metered only when a loop fires).

    On a port collision, exit non-zero with a fail-loud message; on Ctrl-C (SIGINT),
    stop the listener cleanly. `serve_forever` runs on a worker thread so the main
    thread can drive `shutdown()` (which must run off the serving thread).

    Args:
        argv (list, optional): Argument vector; defaults to `sys.argv[1:]`.
        build (Callable, optional): The server factory seam; defaults to
            `serve_server.build_server`. Injectable so a test can assert the wiring
            without binding a socket or making a live call.
        client_factory (Callable, optional): The model-client factory; defaults to
            `ModelClient`. Constructs the no-train client wired into the server.

    Returns:
        (int) 0 on a clean operator-stop.
    """
    port = serve_server.DEFAULT_PORT
    roots = _data_roots()  # optional scratch-store override for safe, repeatable testing
    # Arm the loop-LIVE metered lane at operator start (ADR-0049 D1). The D5 shared-key bridge exports
    # the shared `a-plus-maxing-api-key` onto the env-first key path when no BYO key resolves — a BYO
    # key no-ops it (HIST01: the shared key is the default, never an override) — so the metered lane's
    # `key_source.resolve` returns on the no-BYO default. `load_alpha_config` fails loud on a malformed
    # / in-repo config and `main()` does NOT catch it: crashing loud at operator start is the intended
    # posture (AR-006, no defensive try/except). Never print/log/repr the config or key (bead d1yz —
    # the dataclass repr renders the secret). ONE `client` feeds the server, the metered `loop_dispatch`,
    # and the `loop_deid_client`, so the injectable `client_factory` seam drives the metered lane too
    # (0-spend at construct — the ModelClient backend is lazy; metered only when a loop actually fires),
    # replacing the prior honest-degraded 0-loop posture (bead 3ge1) with a genuinely-live loop.
    alpha_config.provision_shared_key(alpha_config.load_alpha_config())
    client = client_factory()
    try:
        srv = build(
            port, client=client,
            loop_dispatch=metered_dispatch.build_dispatch(client),
            loop_deid_client=AggregatingDeidClient(client),
            **roots,
        )
    except OSError as exc:
        raise SystemExit(
            f"Port {port} is already in use ({exc}); the intake server did not start. "
            f"Free port {port}, or run with a different port once that option lands. "
            f"No server is listening."
        )

    host, bound_port = srv.server_address
    print(f"Serving the intake wizard at http://{host}:{bound_port}/  (Ctrl-C to stop)")
    if roots:
        print(f"  TEST MODE — serving against a scratch store at {roots['store_root'].parent} "
              f"(your real vault/ is untouched; delete that dir to start fresh)")

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
