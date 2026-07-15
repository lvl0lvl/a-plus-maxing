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
_DELETE_FAIL_MSG = "Could not delete the secret: the keyring backend is unavailable."


class KeyStoreError(RuntimeError):
    """A secret-store write or delete failed fail-loud.

    Raised when a set reaches neither tier (keyring unavailable AND the fallback write
    failed) or when a delete cannot reach an unavailable keyring. The message is CONSTANT
    and never carries the secret value — a failure must not leak the secret into a
    traceback (the repo is PUBLIC).
    """


def _username():
    return getpass.getuser()


def _sanitize(service):
    """Map a service label onto an env-var-safe token: uppercase, non-alphanumeric -> _."""
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
        return json.loads(p.read_text())
    except (OSError, ValueError):
        # A corrupt or unreadable fallback file is not a valid secret store: treat it as
        # empty instead of raising JSONDecodeError (whose .doc carries the raw file bytes)
        # out of the public API and bricking the secret path on an available keyring (LOW-2).
        return {}


def _write_fallback_file(path, data):
    """Write the fallback map to `path` with owner-only mode 0600, reject a symlink target.

    Creates the file via `os.open(..., O_CREAT | O_WRONLY | O_TRUNC | O_NOFOLLOW, 0o600)`, so
    the restrictive mode is set by the creating syscall — there is no `open('w')`-then-`chmod`
    window in which the file is group/world-readable at the process umask (F9 / SEC-07).
    O_NOFOLLOW rejects a symlink pre-placed at `path` (the write raises rather than following
    it to an attacker-chosen target); `fchmod(fd, 0o600)` re-asserts owner-only mode on the
    REWRITE path too, where O_CREAT's mode argument is ignored on a pre-existing file (LOW-1).
    """
    payload = json.dumps(data)
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as handle:
        os.fchmod(handle.fileno(), 0o600)
        handle.write(payload)


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

    Reads the OS-native keyring via the injected backend seam. Reads the file/env fallback
    IFF the keyring raises on the get; on an AVAILABLE keyring that merely misses (secret
    absent) it returns None WITHOUT reading the fallback — no stale-fallback resurrection
    (SEC-04). On symmetric unavailability the fallback FILE wins, then the fixed-prefix env.
    """
    try:
        return backend.get_password(service, _username())
    except Exception:
        return _fallback_lookup(fallback_path, service)


def set_secret(service, value, *, backend=_DEFAULT_BACKEND, fallback_path=_FALLBACK_PATH):
    """Store `value` under `service` via the keyring, or the fallback FILE when unavailable.

    Uses `getpass.getuser()` as the keyring username. When the backend is unavailable
    (raises/prompts/blocks) the value is persisted to the fallback FILE; when the fallback
    write ALSO fails the call raises `KeyStoreError` fail-loud. When the keyring IS
    available the write succeeds AND any stale fallback FILE residue for `service` is
    cleared (write-through-clear — SEC-04). The fixed-prefix env var is read-only operator
    injection and is never written here.
    """
    try:
        backend.set_password(service, _username(), value)
    except Exception:
        try:
            _fallback_write(fallback_path, service, value)
        except Exception:
            raise KeyStoreError(_STORE_FAIL_MSG) from None
        return
    _fallback_clear(fallback_path, service)


def delete_secret(service, *, backend=_DEFAULT_BACKEND, fallback_path=_FALLBACK_PATH):
    """Remove any stored secret for `service` from BOTH tiers.

    The fallback FILE residue is cleared UNCONDITIONALLY; the keyring entry is removed when
    the keyring is available (idempotent on an available-but-absent keyring — no error).
    When the keyring is unavailable/raising the call is FAIL-LOUD: it clears the fallback,
    then surfaces the keyring failure as `KeyStoreError`, never silently leaving a keyring
    value to resurrect on recovery (AC-16).
    """
    _fallback_clear(fallback_path, service)
    try:
        backend.delete_password(service, _username())
    except PasswordDeleteError:
        return
    except Exception:
        raise KeyStoreError(_DELETE_FAIL_MSG) from None
