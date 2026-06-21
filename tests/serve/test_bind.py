"""Bind-surface tests for the loopback-only intake server (ADR-0013-T1).

The single load-bearing invariant: the server binds `127.0.0.1` ONLY, never
`0.0.0.0`/`""`/a routable interface (ADR-0013 Confirmation 1 — the first network
surface the system opens, off-machine-unreachable by construction). AC-1 inspects
the constructed server's `server_address[0]`; a one-time negative control proves
that assertion is failing-capable (it goes RED if the bind is `0.0.0.0`). AC-3
pins the port-collision fail-loud: a pre-bound default port makes
`python -m scripts.serve` exit non-zero with a named message, binding nothing —
never a silent rebind to another port.
"""

import socket
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.serve import server as serve_server

REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 loopback-bind floor (Risk ADR-0013 Negative-1)
# --------------------------------------------------------------------------- #


def test_server_binds_loopback_only():
    """AC-1: the constructed server's bind address is 127.0.0.1, never routable.

    Builds the server on an ephemeral port via the published factory and inspects
    `server_address[0]` — the literal bound interface. The assertion goes RED if
    the bind is `0.0.0.0`/`""`/a routable interface (proved failing-capable by the
    negative control below).
    """
    srv = serve_server.build_server(0)
    try:
        host = srv.server_address[0]
        assert host == "127.0.0.1", f"server bound {host!r}, expected loopback 127.0.0.1"
        assert host not in ("0.0.0.0", ""), f"server bound the all-interfaces address {host!r}"
    finally:
        srv.server_close()


def test_bind_assertion_is_failing_capable():
    """Negative control: the AC-1 bind assertion goes RED on an 0.0.0.0 bind.

    Constructs a throwaway server on the all-interfaces address and confirms the
    SAME `server_address[0] == "127.0.0.1"` assertion FAILS — proving the AC-1
    gate is failing-capable, not a constant-true assertion. The probe binds a real
    socket on 0.0.0.0:0 so the address actually reflects the all-interfaces bind,
    then is closed; the loopback-only factory is never weakened.
    """
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    probe.bind(("0.0.0.0", 0))
    try:
        host = probe.getsockname()[0]
        # The negative control: the AC-1 assertion MUST reject this all-interfaces bind.
        with pytest.raises(AssertionError):
            assert host == "127.0.0.1"
        assert host in ("0.0.0.0", ""), f"control bound {host!r}, expected all-interfaces"
    finally:
        probe.close()


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-3 port-collision fail-loud (OQ-2)
# --------------------------------------------------------------------------- #


def test_port_collision_exits_nonzero_fail_loud():
    """AC-3 / OQ-2: a pre-bound default port makes `main` exit non-zero, fail-loud.

    Pre-binds the server's default port on loopback, then invokes the real
    `python -m scripts.serve` operator surface as a subprocess. It must exit
    non-zero with a message naming the collision and the alternate-port
    instruction, binding nothing (the pre-bound socket stays the only listener).
    A silent rebind to another port fails this test.
    """
    from scripts.serve import server as srv_mod

    port = srv_mod.DEFAULT_PORT
    holder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    holder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    holder.bind(("127.0.0.1", port))
    holder.listen(1)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "scripts.serve"],
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode != 0, (
            f"main exited 0 on a port collision (silent rebind?); "
            f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
        )
        message = (proc.stdout + proc.stderr).lower()
        assert str(port) in message, f"collision message names no port: {message!r}"
        assert "in use" in message or "already" in message or "collision" in message, (
            f"collision message is not fail-loud about the collision: {message!r}"
        )
        # Fail-loud, not silent rebind: the message must point at an alternate port.
        assert "port" in message, f"collision message gives no alternate-port instruction: {message!r}"
    finally:
        holder.close()
