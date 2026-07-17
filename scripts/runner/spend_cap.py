"""The per-tester cumulative monthly spend cap — a persisted, cross-run dispatch ceiling (ADR-0049-T3).

`SpendCap` maintains a cumulative monthly per-tester dispatch count in a gitignored, instance-local
JSON ledger (keyed by `getpass.getuser()` + `YYYY-MM`) and refuses — SERIALIZED, ATOMIC, fail-closed —
once a `(tester, month)` count would exceed the per-tester monthly ceiling. It is a NEW cumulative
invariant that COMPOSES with (never replaces) the per-run in-memory `dispatch_budget.DispatchBudget`:
the per-run budget bounds a single plan run; this cap bounds a tester's spend across every run in a
calendar month. It is wired into the ADR-0049-T1 metered dispatch factory as an INJECTABLE
consult-before-dispatch seam (`metered_dispatch.build_dispatch(client, *, spend_cap=...)`), default-OFF.

Three load-bearing contracts (the Phase-4 review pinned these):

  - **Exception propagation (C1):** `SpendCapExceeded` SUBCLASSES `dispatch_budget.DispatchCapExceeded`
    so the metered loop's only cap-halt handler (`plan_orchestrator.py:314 except DispatchCapExceeded`)
    catches it and surfaces honest-no-plan when armed — a mirror-not-subclass exception would be
    uncaught and CRASH the run. It carries a DISTINCT reason token (`SPEND_CAP_EXCEEDED`) so the halt
    is distinguishable from the per-run `DISPATCH_CAP_EXCEEDED`.
  - **Fail-closed = CHECK-then-increment (C2):** over a PERSISTED ledger the count is read, checked
    against the ceiling, and only then incremented + persisted — never persist-then-check (which would
    drift the stored count upward on every refused retry, a real over-spend). This DIVERGES from
    `DispatchBudget.charge`'s increment-then-check ordering (safe only for an in-memory, per-run count).
  - **Serialized + atomic + fail-closed-on-corruption (C3):** the armed metered loop runs under
    `ThreadingHTTPServer`, so the read->check->increment->persist critical section is serialized under a
    process-wide `threading.Lock` registry keyed by `ledger_path` (mirroring `confirm.py:_confirm_lock_for`
    — the correct intra-process-threads tool; `store_lock`'s `fcntl.flock LOCK_NB` skip-on-contention
    would DROP a charge). The write is atomic (`mkstemp`->`fchmod(0o600)`->`fsync`->`os.replace`, mirroring
    `secret_store._write_fallback_file`), so a torn write leaves the prior count byte-intact. A
    present-but-corrupt/unreadable/non-dict ledger fails CLOSED (raise — refusing when the count cannot
    be verified is the safe direction for a spend control; recovery = the operator deletes the ledger).
    A missing ledger is count 0 (first run — nobody has spent).

The module imports no `scripts.store` symbol and adds 0 field to the outbound metered payload: the cap
reads/writes ONLY its own ledger file, so the ADR-0049-T1 D2 egress wire-scan stays green.
"""

import getpass
import json
import os
import tempfile
import threading
from datetime import datetime
from pathlib import Path

from scripts.plan import dispatch_budget

# The honest no-plan reason the monthly-cap halt surfaces — DISTINCT from the per-run
# `dispatch_budget.DISPATCH_CAP_EXCEEDED` so the orchestrator's `:314` honest-no-plan distinguishes a
# monthly spend refusal from the per-run dispatch-cap refusal (C1). Same kebab-string vocabulary.
SPEND_CAP_EXCEEDED = "spend-cap-exceeded"

# The named module-level monthly ceiling the `SpendCap` constructor falls back to when no ceiling is
# passed — a documented alpha default well above a normal month's dispatch tally, NOT a hard-coded
# literal at the check site. The operator/billing ceiling is confirmed at the downstream live-run
# checkpoint (mirrors `dispatch_budget.DEFAULT_DISPATCH_CAP`'s posture).
DEFAULT_MONTHLY_CAP = 1000

# The gitignored, in-tree, per-instance ledger's real at-rest location (mirrors
# `secret_store._FALLBACK_PATH`): a repo-root dotfile so `git check-ignore` resolves it. Injected to a
# tmp path in tests; this default is never written during the build.
_DEFAULT_LEDGER_PATH = Path(__file__).resolve().parents[2] / ".spend-cap-ledger.json"

# The process-wide lock registry serializing the charge critical section per ledger path (C3). Mirrors
# `confirm.py:_confirm_lock_for`: the armed loop's concurrent charges are same-process
# `ThreadingHTTPServer` threads, so a `threading.Lock` (not `fcntl.flock`) is the right serializer.
_ledger_locks = {}
_ledger_locks_guard = threading.Lock()


def _ledger_lock_for(ledger_path):
    """Return the process-wide `threading.Lock` serializing charges for one ledger path."""
    key = str(ledger_path)
    with _ledger_locks_guard:
        lock = _ledger_locks.get(key)
        if lock is None:
            lock = _ledger_locks[key] = threading.Lock()
    return lock


class SpendCapExceeded(dispatch_budget.DispatchCapExceeded):
    """The fail-closed halt signal: a charge would push a `(tester, month)` count past the ceiling.

    Subclasses `dispatch_budget.DispatchCapExceeded` (C1) so the metered loop's cap-halt handler
    (`plan_orchestrator.py:314`) catches it and surfaces honest-no-plan when armed. Defines its OWN
    `__init__` that sets the DISTINCT `SPEND_CAP_EXCEEDED` reason token WITHOUT calling the parent
    `__init__(count, cap)` — which would clobber `reason` to `DISPATCH_CAP_EXCEEDED` (AR-3).

    Attributes:
        count (int): The persisted current count (the ceiling on a refusal; 0 on a corrupt ledger).
        cap (None): Base-attr parity with the parent (the ceiling is not surfaced on the exception).
        reason (str): The honest no-plan reason token (`SPEND_CAP_EXCEEDED`).
    """

    def __init__(self, count):
        # Bypass DispatchCapExceeded.__init__ (which sets reason=DISPATCH_CAP_EXCEEDED) via Exception
        # directly, so the distinct SPEND_CAP_EXCEEDED token C1 depends on is preserved (AR-3).
        self.count = count
        self.cap = None
        self.reason = SPEND_CAP_EXCEEDED
        Exception.__init__(self, f"monthly spend cap exceeded: count {count}")


class SpendCap:
    """A pre-bound per-tester monthly dispatch cap over a serialized, atomic, persisted ledger.

    Pre-bound to its tester / ledger / ceiling / clock at construction so the consult is argless
    (`charge()`) — the metered dispatch factory injects one `SpendCap` and every threaded charge goes
    through it. `charge()` reads the current `(tester, month)` count under the ledger lock, refuses
    fail-closed (check-then-increment, C2) past the ceiling, and otherwise increments + atomically
    persists. Reads/writes ONLY the ledger file — never `scripts.store`. All state (ledger path,
    ceiling, tester, clock, lock) is bound private at construction; see `__init__` for the injectable
    seams.
    """

    def __init__(self, *, ledger_path=None, ceiling=DEFAULT_MONTHLY_CAP, tester=None, clock=None):
        """Bind the cap to its ledger / ceiling / tester / clock.

        Args:
            ledger_path (str | Path, optional): The JSON ledger path. Defaults to the gitignored
                repo-root `.spend-cap-ledger.json` (`_DEFAULT_LEDGER_PATH`); injected to a tmp path in
                tests.
            ceiling (int, optional): The per-tester monthly ceiling. Defaults to the named
                `DEFAULT_MONTHLY_CAP`.
            tester (str, optional): The tester identity. Defaults to `getpass.getuser()`.
            clock (Callable, optional): A `() -> datetime` clock (the month key source). Defaults to
                `datetime.now`; injected for the monthly-rollover + concurrency tests.
        """
        self._ledger_path = Path(ledger_path) if ledger_path is not None else _DEFAULT_LEDGER_PATH
        self._ceiling = ceiling
        self._tester = tester if tester is not None else getpass.getuser()
        self._clock = clock if clock is not None else datetime.now
        self._lock = _ledger_lock_for(self._ledger_path)

    def charge(self):
        """Account for one dispatch about to be issued; fail closed past the per-tester monthly ceiling.

        Computes the `(tester, month)` key from `clock()` BEFORE acquiring the charge lock (the month
        is invariant across the microsecond critical section — so a test barrier can align concurrent
        threads at the read without touching the lock, C3/AR-1). Under the lock, reads the current
        count; if `count + 1` would exceed the ceiling raises `SpendCapExceeded(count)` WITHOUT writing
        (check-then-increment, C2); otherwise increments and atomically persists the ledger.

        Returns:
            (int) The post-increment count (when under the ceiling).
        """
        month = self._clock().strftime("%Y-%m")
        key = f"{self._tester}::{month}"
        with self._lock:
            ledger = self._read_ledger()
            count = ledger.get(key, 0)
            if count + 1 > self._ceiling:
                raise SpendCapExceeded(count)
            ledger[key] = count + 1
            self._write_ledger(ledger)
            return ledger[key]

    def _read_ledger(self):
        """Read the ledger map; missing -> empty, corrupt/unreadable/non-dict -> fail CLOSED (raise)."""
        path = self._ledger_path
        if not path.exists():
            return {}  # first run — nobody has spent
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            # The count cannot be verified — refuse (the safe direction for a spend control). Diverges
            # from secret_store's fail-open-to-empty read, which is safe for a secret but unsafe here.
            raise SpendCapExceeded(0)
        if not isinstance(data, dict):
            raise SpendCapExceeded(0)
        return data

    def _write_ledger(self, data):
        """Atomically persist the ledger map owner-only (0o600); mirrors `secret_store._write_fallback_file`.

        Writes to a fresh temp sibling (`mkstemp`, O_EXCL, 0600), `fchmod`s owner-only, `fsync`s durable,
        then `os.replace`s over the path — an atomic rename. A torn write (crash mid-write) leaves the
        live ledger's prior content byte-intact (the temp is never `os.replace`d), instead of the
        torn-write-unsafe bare `open('w')` that would empty it.
        """
        path = self._ledger_path
        payload = json.dumps(data)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f"{path.name}.", suffix=".tmp")
        try:
            try:
                handle = os.fdopen(fd, "w")
            except BaseException:
                os.close(fd)
                raise
            with handle:
                os.fchmod(handle.fileno(), 0o600)
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
