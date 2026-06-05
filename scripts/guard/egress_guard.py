"""OS-level no-network egress guard (ADR-0001-T0 selected mechanism).

`run(operation)` executes a zero-arg operation under an OS-enforced no-network
sandbox covering the whole process tree, and returns a value that is truthy when
no outbound network call was observed anywhere in the invocation, falsy when an
outbound call surfaced or the isolation could not be established (fail-closed /
default-deny). The deny is enforced by the OS, so a child process that tries to
egress fails the same way (Security HIGH-1) — not a watcher's hook coverage.

Per-OS binding chosen at run time by `platform.system()` (one mechanism, OS-
dispatched — not an implementer menu):
- macOS (Darwin): `sandbox_init` with `(version 1)(allow default)(deny network*)`.
- Linux: an offline network namespace (`unshare(CLONE_NEWUSER|CLONE_NEWNET)`).

A Python closure cannot be transported into a `sandbox-exec` subprocess, so the
isolation is applied in-process inside a forked child that then calls `operation`:
child exits clean under deny-network -> truthy; the operation raised (its blocked
network op surfaced) or the isolation could not be applied -> falsy.
"""

import ctypes
import ctypes.util
import os
import platform

# macOS sandbox profile: allow everything, then deny all network operations.
# Proven (store AC-4) to block socket.connect while allowing local file I/O.
_DARWIN_PROFILE = b"(version 1)(allow default)(deny network*)"

# CLONE flags for the Linux offline-namespace binding (unprivileged user + net
# namespace; the new net namespace has only loopback, so no route off-host).
_CLONE_NEWUSER = 0x10000000
_CLONE_NEWNET = 0x40000000

_CHILD_CLEAN = 0  # operation completed with no egress -> pass
_CHILD_RAISED = 17  # operation raised (blocked egress surfaced) -> fail


def _apply_isolation():
    """Place the current process under an OS-enforced no-network sandbox.

    Raises:
        RuntimeError: The OS binding could not be established (drives fail-closed).
    """
    system = platform.system()
    if system == "Darwin":
        _apply_darwin_sandbox()
    elif system == "Linux":
        _apply_linux_namespace()
    else:
        raise RuntimeError(f"no OS-level network-isolation binding for {system}")


def _apply_darwin_sandbox():
    """Apply the macOS deny-network sandbox profile to this process."""
    libname = ctypes.util.find_library("sandbox")
    if libname is None:
        raise RuntimeError("libsandbox not found")
    lib = ctypes.CDLL(libname)
    lib.sandbox_init.restype = ctypes.c_int
    lib.sandbox_init.argtypes = [
        ctypes.c_char_p,
        ctypes.c_uint64,
        ctypes.POINTER(ctypes.c_char_p),
    ]
    errbuf = ctypes.c_char_p()
    rc = lib.sandbox_init(_DARWIN_PROFILE, 0, ctypes.byref(errbuf))
    if rc != 0:
        message = errbuf.value
        lib.sandbox_free_error(errbuf)
        raise RuntimeError(f"sandbox_init failed (rc={rc}): {message!r}")


def _apply_linux_namespace():
    """Enter an unprivileged user+network namespace with no off-host route."""
    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    if libc.unshare(_CLONE_NEWUSER | _CLONE_NEWNET) != 0:
        err = ctypes.get_errno()
        raise RuntimeError(f"unshare failed (errno={err})")


def run(operation):
    """Run a zero-arg operation under an OS-level no-network sandbox.

    Args:
        operation (Callable): The operation to run (zero-arg). It may wrap a
            multi-step sequence in one closure; egress anywhere within the
            invocation, in-process or from a spawned child, surfaces as a fail.

    Returns:
        (bool) True when the operation completed with no outbound network call
        observed across the whole invocation; False when an outbound call
        surfaced or the OS isolation could not be established (fail-closed).

    Notes:
        The truthy/falsy result reflects whether the operation surfaced an error;
        the OS sandbox blocks the actual egress regardless, so an operation that
        catches its own blocked-egress error is reported clean but no data left
        the host.
    """
    try:
        pid = os.fork()
    except OSError:
        return False
    if pid == 0:
        code = _CHILD_RAISED
        try:
            _apply_isolation()
            operation()
            code = _CHILD_CLEAN
        except SystemExit as exc:
            code = _CHILD_CLEAN if exc.code in (0, None) else _CHILD_RAISED
        except BaseException:
            code = _CHILD_RAISED
        finally:
            os._exit(code)

    _, status = os.waitpid(pid, 0)
    return os.WIFEXITED(status) and os.WEXITSTATUS(status) == _CHILD_CLEAN
