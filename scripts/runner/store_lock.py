"""Runner-owned advisory lock over the cadence read -> regenerate -> promote critical section (ADR-0039-T4).

`cadence_lock(root)` is a context manager over `<root>/.cadence-runner.lock` acquired non-blocking with
`fcntl.flock(LOCK_EX | LOCK_NB)`. It serializes runner-to-RUNNER cadence ticks on the read-regenerate-promote
critical section so two concurrent scheduled ticks on the same gitignored store never interleave a lost or
torn re-gen (ADR-0039 OQ-7). It yields an ACQUIRED outcome (`True`) on a free lock and a BUSY outcome
(`False`) on a held lock — the non-blocking acquire never waits and never corrupts the store; a busy tick
defers and catches up on the next tick. The lock is released (the fd closed) in a `finally` on EVERY exit —
normal, busy, or exception — so a crashed critical section frees the lock and the next tick re-fires
(ADR-0039 OQ-8 crash-release).

flock is associated with the OPEN FILE DESCRIPTION, not the process, so two `cadence_lock(root)` contexts
each `open()`-ing the lock on their own fd contend even within one process/thread (the deterministic
in-process mutual exclusion). POSIX byte-range locks (`fcntl.lockf`) are per-process and would NOT contend
in-process — flock is the required primitive here, not lockf.

Runner-to-SERVER is NOT locked: a concurrent server write during the runner's raw `store.read_all` cannot
tear the read because every store write lands atomically per file (`store._write_atomic` -> `os.replace`) —
the reader sees the whole old or the whole new file, never a half-written one (accept-stale-snapshot). The
lock adds no store record, defines no store key, adds no store item id; it lives OUTSIDE the frozen store,
as a gitignored runtime lock file under `vault/store/`.
"""

import contextlib
import fcntl
import os
from pathlib import Path

# The lock file name — a direct child of the store root, covered by the gitignored `vault/store/`.
_LOCK_FILENAME = ".cadence-runner.lock"


@contextlib.contextmanager
def cadence_lock(root):
    """Advisory runner-to-runner lock over `<root>/.cadence-runner.lock`; yield acquired/busy.

    Opens (creating if absent) the lock file under `root` and acquires it non-blocking with
    `fcntl.flock(LOCK_EX | LOCK_NB)`. Yields `True` when the lock is free (the caller enters the
    critical section) and `False` when another tick holds it (the caller defers) — never blocks and
    never corrupts the store. Closes the fd in a `finally` on every exit — normal, busy, or exception —
    releasing the flock so a crashed critical section frees the lock for the next tick.

    Args:
        root (str | Path): The store root; the lock file is `<root>/.cadence-runner.lock`.

    Yields:
        (bool) True when the lock was acquired (enter the critical section), False when another runner
        tick holds it (defer to the next tick).
    """
    path = Path(root) / _LOCK_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            yield False
            return
        yield True
    finally:
        os.close(fd)
