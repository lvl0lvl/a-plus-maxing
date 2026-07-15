"""Cross-platform secret store: an OS-native keyring primary with a file/env fallback tier.

Exposes `get_secret` / `set_secret` / `delete_secret` over a single injectable keyring
backend seam (default: the OS-native `keyring` backend). The fallback tier engages when a
keyring operation RAISES (symmetrically on both get and set) — the backend is
locked/unavailable, or an unattended interactive prompt cannot be answered and so raises or
blocks then times out. A prompt that SUCCEEDS interactively returns its value and is served
from the keyring, NOT the fallback. On a raise the operation falls back to a per-instance
file (the read/write round-trip target) plus a fixed-prefix environment variable (read-only
operator injection).

The single `service` argument maps onto the keyring `(service_name, username)` pair using
`getpass.getuser()` as the username — set-side parity with `scripts.model.key_source`'s
`add-generic-password -a <user>` account, so a key this project's own writer stored round-
trips. `get_secret` returns the stored secret or None when absent (None-on-absent parity
with `key_source._keychain_runner`, so downstream default seams re-point onto it without a
chain rewrite).

At-rest transform (honest naming): the fallback file is protected ONLY by owner-only
filesystem permissions (mode 0600, applied atomically at creation) and is NOT
cryptographically encrypted — its key material is extractable by the file owner and via the
fixed-prefix env var, so the fallback tier is weaker at rest than the OS keyring. No home-
grown cipher is used; base64/hex, where present, is a byte-safe ENCODING only, never
labelled as encryption. Secret VALUES never enter a log record, an exception message, or a
traceback: failures raise a constant-message `KeyStoreError` (the repo is PUBLIC).

Fallback threat model (OQ-2 / SEC-06):
- Keyring is PREFERRED; the fallback tier engages ONLY when a keyring operation is
  unavailable — i.e. it RAISES (the backend is locked, or an unattended interactive prompt
  cannot be answered and so raises or blocks then times out). That unanswerable prompt is
  the prompt-induced DOWNGRADE to the weaker fallback, because the backgrounded server
  cannot answer an interactive keychain prompt; a prompt that SUCCEEDS is served from the
  keyring, not the fallback. (Whether the real OS keyring prompts or returns unattended
  without prompting is validated only in a LIVE run — bead a-plus-maxing-m8ia; the mock
  build proves the routing logic, not the live backend's unattended behavior.)
- WHERE the key material lives: the fallback FILE is a per-instance dotfile in the repo's
  gitignored working tree (`.secret-store-fallback.json`); the read-only fixed-prefix env
  var is the other injection point. Both are env-var-EXTRACTABLE by the file owner, which is
  why the fallback is WEAKER at rest than the OS keyring (no OS-guarded secret enclave).
- What it DOES protect (the positive model): a stolen disk-image or backup taken while the
  live process environment is absent — the 0600 owner-only file is not group/world-readable
  and the fixed-prefix env var is not captured in a cold backup. What it does NOT
  meaningfully protect: the near-zero-benefit co-resident case where an attacker already
  holds both the live env AND the file (either yields the secret directly).
- PUBLIC-repo gitignored-working-tree threat: the fallback file sits in the PUBLIC repo's
  gitignored working tree, so an ignore-bypassing `git add -f` (or a tool that bypasses
  `.gitignore`) could stage it; the block-pii-commit / pre-push-pii-scan HOOKS are the
  backstop that keeps the secret from ever reaching a commit or a push.
"""

import getpass
import json
import os
import re
import tempfile
from pathlib import Path

import keyring
from keyring.errors import PasswordDeleteError

# The single injectable keyring backend seam's default: the live OS-native `keyring`
# backend. Tests substitute per-OS fakes, a prompt-detection spy, and a symmetric
# raising/prompting fake through this seam, so no real keychain is ever touched.
_DEFAULT_BACKEND = keyring

# The fallback tier's real at-rest location: an IN-TREE, per-instance, gitignored dotfile
# (inside the repo working tree, following the vault/store dropzone convention), so
# `git check-ignore` can resolve it — an out-of-tree path fatals. Injected to a tmp_path in
# tests; this default is never written during the build.
_FALLBACK_PATH = Path(__file__).resolve().parents[2] / ".secret-store-fallback.json"

# The fixed sanitized prefix for the read-only env fallback key: <PREFIX>_<sanitized
# service>. Never a raw `service` passthrough (SEC-08: get_secret("PATH") must not read the
# real PATH env var).
_FALLBACK_ENV_PREFIX = "APLUS_SECRET_FALLBACK"

# Constant fail-loud messages — they never carry the secret value (SEC-03; mirrors
# scripts.model.key_source's constant-message KeyStoreError).
_STORE_FAIL_MSG = "Could not store the secret: keyring unavailable and the fallback write failed."
# Distinct from _STORE_FAIL_MSG: here the keyring write SUCCEEDED and only the stale-residue
# clear failed, so the store-failed wording would be inaccurate (never swallow the clear).
_CLEAR_FAIL_MSG = "Stored the secret in the keyring, but could not clear stale fallback residue."
# Either tier (fallback clear or keyring delete) may fail, so the message is tier-agnostic.
_DELETE_FAIL_MSG = "Could not delete the secret from one or both stores."


class KeyStoreError(RuntimeError):
    """A secret-store write or delete failed fail-loud.

    Raised by set_secret when the keyring is unavailable AND the fallback write failed, or
    when an available-keyring write cannot clear stale fallback residue; and by delete_secret
    when either tier (the fallback clear or the keyring delete) could not be cleared. The
    message is CONSTANT and never carries the secret value — a failure must not leak the
    secret into a traceback (the repo is PUBLIC).
    """


def _username():
    return getpass.getuser()


def _sanitize(service):
    """Map a service label onto an env-var-safe token: uppercase, non-alphanumeric -> _.

    The mapping is non-injective: distinct punctuation-variant services (e.g. "a-b" and "a.b")
    collide onto one <PREFIX>_<TOKEN> env key. The FILE tier keys on the raw service string and
    does not collide, so this only affects the read-only env fallback.
    """
    return re.sub(r"[^A-Z0-9]", "_", service.upper())


def _env_key(service):
    return f"{_FALLBACK_ENV_PREFIX}_{_sanitize(service)}"


def _env_lookup(service):
    return os.environ.get(_env_key(service))


def _read_fallback_file(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text())
        # A valid-JSON NON-dict (e.g. [1,2,3] / 42 / null / "x") is not a secret map: the
        # downstream .get()/in/[svc]= would raise a raw AttributeError/TypeError out of the
        # public API, so treat it as empty too.
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        # A corrupt or unreadable fallback file is not a valid secret store: treat it as
        # empty instead of raising JSONDecodeError (whose .doc carries the raw file bytes)
        # out of the public API and bricking the secret path on an available keyring (LOW-2).
        return {}


def _write_fallback_file(path, data):
    """Write the fallback map to `path` atomically as an owner-only (0600) regular file.

    Mirrors `scripts.store.store._write_atomic`: the payload is written to a fresh temp sibling
    in the SAME directory (`tempfile.mkstemp` creates it O_EXCL | O_NOFOLLOW at mode 0600),
    fsync'd durable, then `os.replace`d over `path` — an atomic rename. A torn write (ENOSPC /
    crash mid-write) therefore leaves the live file's prior content byte-intact, instead of the
    old in-place O_TRUNC writer that emptied it and lost every sibling secret on the next
    read-modify-rewrite. The secret NEVER reaches a symlink pre-placed at `path`: it lives in
    the temp inode, and the rename atomically replaces the symlink itself (the symlink's target
    is untouched), preserving the no-write-through-symlink property the old O_NOFOLLOW open gave
    by rejection. `fchmod` re-asserts owner-only 0600 for explicit parity; on any failure the
    orphan temp is unlinked so no stray secret-bearing sibling is left behind.

    Args:
        path (str | Path): The fallback file path.
        data (dict): The service -> secret map to persist.
    """
    path = Path(path)
    payload = json.dumps(data)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f"{path.name}.", suffix=".tmp")
    try:
        # os.fdopen takes ownership of fd; close fd directly only if it raises first.
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
        # Broader than Exception on purpose: an interrupt mid-write must still unlink the
        # orphan temp so no stray secret-bearing sibling is left behind.
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _fallback_lookup(path, service):
    """Read the fallback tier for `service`: the FILE first, then the fixed-prefix env var.

    The env var is consulted only when the file holds no value for `service` (F6). This is
    the single fallback-read entry point — reached only when the keyring raises on a get.
    """
    file_value = _read_fallback_file(path).get(service)
    if file_value is not None:
        return file_value
    return _env_lookup(service)


def _fallback_write(path, service, value):
    data = _read_fallback_file(path)
    data[service] = value
    _write_fallback_file(path, data)


def _fallback_clear(path, service):
    """Remove any fallback FILE residue for `service` (a no-op when there is none)."""
    data = _read_fallback_file(path)
    if service not in data:
        return
    del data[service]
    _write_fallback_file(path, data)


def get_secret(service, *, backend=_DEFAULT_BACKEND, fallback_path=_FALLBACK_PATH):
    """Return the stored secret for `service`, or None when no secret is stored.

    Reads the OS-native keyring via the injected backend seam. The file/env fallback is read
    ONLY when the keyring RAISES on the get; an AVAILABLE keyring that merely misses returns
    None WITHOUT reading the fallback, so stale residue is never resurrected (SEC-04). On
    symmetric unavailability the fallback FILE wins, then the fixed-prefix env var.

    Args:
        service (str): The service label whose secret to fetch.
        backend (module, optional): The keyring backend seam; defaults to the OS-native
            `keyring`, injected in tests. Internal affordance.
        fallback_path (str | Path, optional): The fallback file path; defaults to the in-tree
            instance-local dotfile, injected in tests. Internal affordance.

    Returns:
        (str | None) The stored secret, or None when no secret is stored for `service`.
    """
    try:
        return backend.get_password(service, _username())
    except Exception:
        return _fallback_lookup(fallback_path, service)


def set_secret(service, value, *, backend=_DEFAULT_BACKEND, fallback_path=_FALLBACK_PATH):
    """Store `value` under `service` in the keyring, or the fallback FILE when unavailable.

    Uses `getpass.getuser()` as the keyring username. When the keyring RAISES the value is
    persisted to the fallback FILE instead. When the keyring IS available the write succeeds
    AND any stale fallback FILE residue for `service` is cleared (write-through-clear — SEC-04);
    that clear is fail-loud, never swallowed — a swallowed clear would leave stale residue a
    later outage get_secret could serve. The fixed-prefix env var is read-only operator
    injection and is never written here.

    Args:
        service (str): The service label to store under.
        value (str): The secret to store.
        backend (module, optional): The keyring backend seam; defaults to the OS-native
            `keyring`, injected in tests. Internal affordance.
        fallback_path (str | Path, optional): The fallback file path; defaults to the in-tree
            instance-local dotfile, injected in tests. Internal affordance.

    Raises:
        KeyStoreError: When the keyring is unavailable AND the fallback write fails, or when an
            available-keyring write cannot clear stale fallback residue — fail-loud with a
            constant message that never carries the secret value.
    """
    try:
        backend.set_password(service, _username(), value)
    except Exception:
        try:
            _fallback_write(fallback_path, service, value)
        except Exception:
            raise KeyStoreError(_STORE_FAIL_MSG) from None
    else:
        try:
            _fallback_clear(fallback_path, service)
        except Exception:
            raise KeyStoreError(_CLEAR_FAIL_MSG) from None


def delete_secret(service, *, backend=_DEFAULT_BACKEND, fallback_path=_FALLBACK_PATH):
    """Remove any stored secret for `service` from BOTH the keyring and the fallback FILE.

    BOTH tiers are always attempted, regardless of a single-tier failure: a fallback-clear
    failure never skips the keyring delete (which would let the keyring credential survive the
    delete). A keyring delete of an already-absent item is idempotent (no error). The call is
    FAIL-LOUD — if EITHER tier could not be cleared it raises `KeyStoreError`, never silently
    leaving a value to resurrect on recovery (AC-16). The fixed-prefix env var is read-only and
    is not cleared here.

    Args:
        service (str): The service label whose secret to remove.
        backend (module, optional): The keyring backend seam; defaults to the OS-native
            `keyring`, injected in tests. Internal affordance.
        fallback_path (str | Path, optional): The fallback file path; defaults to the in-tree
            instance-local dotfile, injected in tests. Internal affordance.

    Raises:
        KeyStoreError: When either tier could not be cleared — fail-loud with a constant message
            that never carries the secret value.
    """
    fallback_cleared = True
    try:
        _fallback_clear(fallback_path, service)
    except Exception:
        fallback_cleared = False

    keyring_cleared = True
    try:
        backend.delete_password(service, _username())
    except PasswordDeleteError:
        pass  # available-but-absent -> the keyring tier is already clear (idempotent)
    except Exception:
        keyring_cleared = False

    if not (fallback_cleared and keyring_cleared):
        raise KeyStoreError(_DELETE_FAIL_MSG) from None
