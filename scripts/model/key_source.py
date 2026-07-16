"""The runtime key source — resolves the no-train API key at call time, never tracked.

`resolve()` fetches the no-train API key from a SET env var (`ANTHROPIC_API_KEY` — the
anthropic SDK's native var AND the operator's documented injection var) or, as a fallback,
the `secret_store` abstraction (OS-native keyring primary + a file/env fallback tier) for
the `a-plus-maxing-api-key` item — AT CALL TIME, never captured at module load and never
read from a tracked file. An absent key raises `KeyUnavailableError` fail-loud, naming the
env var + the `keychain-setup.md` runbook.

This mirrors the project's runtime-config-resolution discipline (`pii_scan`'s gitignored
identity config is resolved at call time, never tracked): no API-key literal ever lands in
the repo (NFR-3 — the repo is PUBLIC). The client's default backend calls `resolve()` at
call time, so the key is fetched at runtime, never imported from a constant.
"""

import os

from scripts import secret_store

# The anthropic SDK's native var AND the operator's documented runtime-injection var
# (S90 directive: `export ANTHROPIC_API_KEY=$(security find-generic-password -s
# "a-plus-maxing-api-key" -w)`). Reading it directly means the operator's existing shell
# export resolves with no extra setup.
ENV_VAR = "ANTHROPIC_API_KEY"

# This project's keychain item — the in-app Profile save (POST /settings/key, via
# `store()`) writes the key here and `resolve()` reads it here, so an in-app paste is
# picked up on the next call with no terminal step. The service name is a project label,
# not a secret — the key VALUE lives in the OS keychain (or the gitignored owner-only
# `secret_store` fallback when the keyring is unavailable), never a tracked file (`keychain-setup.md`).
_KEYCHAIN_SERVICE = "a-plus-maxing-api-key"

_RUNBOOK = "scripts/model/keychain-setup.md"


class KeyUnavailableError(RuntimeError):
    """The no-train API key could not be resolved from any runtime source.

    Raised fail-loud when neither the env var nor the keychain yields a key, naming the
    env var + the runbook so the operator knows how to set it. The key source never
    silently returns a default/empty (that would let a keyless call proceed).
    """


def _keychain_runner():
    """Fetch the key from the secret store at call time, or None when absent/blank.

    Delegates to `secret_store.get_secret(<service>)` (None-on-absent) — the OS-native keyring
    with the file/env fallback tier — replacing the former direct `security` shell-out. The read
    is bound to `getpass.getuser()` inside `secret_store` (set-side parity with this project's own
    writer's account), so an out-of-band-account credential won't resolve — the live-run check is
    bead a-plus-maxing-m8ia. The value is stripped and a blank/whitespace-only value collapses to
    None (an out-of-band `security add-generic-password` write can carry a trailing newline), so the
    absence path (None) stays the caller's fail-loud trigger rather than a padded or blank key.
    """
    value = secret_store.get_secret(_KEYCHAIN_SERVICE)
    if not value:
        return None
    return value.strip() or None


def resolve(keychain_runner=_keychain_runner):
    """Resolve the no-train API key at call time from the env var or the keychain.

    Args:
        keychain_runner (Callable, optional): The credential fetch seam (returns the key or
            None). Defaults to `secret_store.get_secret`; injected in tests so no real
            keyring or key is touched.

    Returns:
        (str) The resolved no-train API key.

    Raises:
        KeyUnavailableError: When neither the env var nor the keychain yields a key —
            fail-loud, naming the env var + the runbook.
    """
    env_key = os.environ.get(ENV_VAR)
    if env_key:
        return env_key

    keychain_key = keychain_runner()
    if keychain_key:
        return keychain_key

    raise KeyUnavailableError(
        f"No no-train API key found. Set the {ENV_VAR} env var, or store the key in the "
        f"macOS keychain per the {_RUNBOOK} runbook (service '{_KEYCHAIN_SERVICE}')."
    )


class KeyStoreError(RuntimeError):
    """Storing the no-train API key in the keychain failed.

    Raised fail-loud when the `secret_store` write fails (the sibling
    `secret_store.KeyStoreError` is translated to this class, so callers keep catching
    `key_source.KeyStoreError`). The message is CONSTANT and never carries the key value —
    a store failure must not leak the secret into a traceback (NFR-3: the repo is PUBLIC).
    """


def _keychain_writer(key):
    """Store the key in the secret store at call time (fail-loud, error-class-translated).

    Delegates to `secret_store.set_secret(<service>, key)` — the OS-native keyring with the
    file/env fallback tier — replacing the former direct `security add-generic-password` shell-out.
    The write is bound to `getpass.getuser()` inside `secret_store`, matching the read account (the
    live-run check is bead a-plus-maxing-m8ia). `secret_store` raises the sibling
    `secret_store.KeyStoreError` on failure; this TRANSLATES it to `key_source.KeyStoreError` (the
    class `server.py`'s `/settings/key` catch depends on) with a CONSTANT message that never carries
    the key value — a store failure must not leak the secret into a traceback (NFR-3: the repo is
    PUBLIC). NOTE: `set_secret` also raises on a SUCCESSFUL keyring write whose stale fallback-tier
    residue could not be cleared (the deliberate SEC-04 fail-loud), so a raised `KeyStoreError` does
    NOT guarantee the key is unstored. The former shell-out's `-A` allow-all-ACL (fix 7c793432, so a
    backgrounded server never blocked on a keychain prompt) is intentionally superseded by the
    `secret_store` keyring write; whether the backgrounded-read path stays unblocked without it is
    deferred to the operator-present live run (bead a-plus-maxing-m8ia).

    Args:
        key (str): The no-train API key to store.
    """
    try:
        secret_store.set_secret(_KEYCHAIN_SERVICE, key)
    except secret_store.KeyStoreError:
        raise KeyStoreError("Could not store the key in the macOS keychain.") from None


def store(key, *, keychain_writer=_keychain_writer):
    """Store the no-train API key in the secret store at call time.

    Writes the key into the same `a-plus-maxing-api-key` item `resolve()` reads, so an
    in-app save (the Profile screen's POST `/settings/key`) is picked up by the next
    runtime `resolve()` with no shell command. The key is written to the `secret_store`
    abstraction (the OS keyring, or — when the keyring is unavailable — its gitignored
    owner-only file/env fallback) — never to a TRACKED file, a log, or a returned value
    (NFR-3: the repo is PUBLIC). An empty/blank key is rejected before any write.

    Args:
        key (str): The no-train API key to store.
        keychain_writer (Callable, optional): The credential write seam (takes the key).
            Defaults to `secret_store.set_secret`; injected in tests so no real keyring
            or key is touched.

    Raises:
        ValueError: When the key is empty/blank — constant message, no key value.
        KeyStoreError: When the secret-store write fails — OR when the key was written but stale
            fallback-tier residue could not be cleared (so it does not guarantee the key is unstored).
    """
    key = (key or "").strip()
    if not key:
        raise ValueError("Refusing to store an empty API key.")
    keychain_writer(key)
