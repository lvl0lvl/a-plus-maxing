"""Tests for scripts/guard/egress_guard.py — OS-level no-network egress guard.

The guard runs a zero-arg callable under an OS-enforced no-network sandbox over
the whole process tree (macOS: sandbox_init deny-network; Linux: offline netns).
`run` is truthy when the callable completed with no outbound network call
observed anywhere in its invocation, falsy when an outbound call surfaced or the
isolation could not be established (fail-closed). The fail-direction tests are
first-class RED targets: a no-op guard that always passes must fail them.
"""

import platform
import socket
import subprocess
import sys

import pytest

from scripts.guard import egress_guard
from scripts.guard.egress_guard import run

DARWIN_ONLY = pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="OS-level isolation binding is exercised on the host OS (Darwin here)",
)


def _local_only(tmp_path):
    """A callable that performs only local file I/O — the AC-1 pass direction."""
    target = tmp_path / "scratch.txt"

    def op():
        target.write_text("local")
        assert target.read_text() == "local"

    return op


@DARWIN_ONLY
def test_run_passes_on_local_only(tmp_path):
    """AC-1 pass: run is truthy when the callable only reads a temp file."""
    assert run(_local_only(tmp_path))


@DARWIN_ONLY
def test_run_fails_on_in_process_egress():
    """AC-1 in-process fail: an outbound socket connect surfaces as falsy."""

    def egress():
        socket.create_connection(("1.1.1.1", 53), timeout=3)

    assert not run(egress)


@DARWIN_ONLY
def test_run_fails_on_subprocess_egress():
    """AC-1 out-of-process fail (Security HIGH-1): a child that connects out.

    The child inherits the parent's network deny, so check=True raises and run
    is falsy — proving the sandbox covers spawned children, not just the parent.
    """

    def child_egress():
        subprocess.run(
            [
                sys.executable,
                "-c",
                "import socket; socket.create_connection(('1.1.1.1',53),timeout=3)",
            ],
            check=True,
        )

    assert not run(child_egress)


@DARWIN_ONLY
def test_run_fails_closed_when_isolation_unestablishable(monkeypatch):
    """Fail-closed (Security HIGH-1): isolation cannot be applied -> falsy.

    Forces the in-child isolation-apply step to raise. The guard must default-
    deny (falsy), never pass when it could not actually observe egress.
    """

    def boom():
        raise RuntimeError("isolation binding unavailable")

    monkeypatch.setattr(egress_guard, "_apply_isolation", boom)

    assert not run(lambda: None)


@DARWIN_ONLY
def test_run_observes_egress_anywhere_in_multistep_closure(tmp_path):
    """Multi-step closure (Architect F1): one closure, two ops, egress at step 2.

    Models ADR-0002-T1's append->read: a single zero-arg closure performing two
    operations in sequence where the second egresses. run must be falsy because
    observation spans the entire callable invocation, not a single call.
    """
    target = tmp_path / "scratch.txt"

    def two_steps():
        target.write_text("step1")  # local I/O — fine
        socket.create_connection(("1.1.1.1", 53), timeout=3)  # egress — must fail

    assert not run(two_steps)


def test_run_returns_truthy_or_falsy_not_exit_code(tmp_path):
    """Return shape (Architect F2): truthy-on-pass satisfies the consumer idiom.

    `sys.exit(0 if run(...) else 1)` requires truthy-on-pass; an exit-code int
    (0=pass) would be falsy-on-pass and invert. This asserts the pass result is
    truthy (host-OS only — a no-network isolation must be establishable).
    """
    if platform.system() != "Darwin":
        pytest.skip("pass-direction truthiness exercised on the host OS")
    result = run(_local_only(tmp_path))
    assert result  # truthy on pass, satisfying sys.exit(0 if run(...) else 1)


@pytest.mark.skipif(
    platform.system() != "Linux",
    reason="Linux offline-namespace binding only executes on Linux",
)
def test_run_linux_binding_smoke(tmp_path):
    """Linux clonability: the offline-namespace binding passes local-only there.

    Skipped on Darwin (this host); guards the Linux binding so a clone onto Linux
    has coverage without failing the suite on macOS.
    """
    assert run(_local_only(tmp_path))
