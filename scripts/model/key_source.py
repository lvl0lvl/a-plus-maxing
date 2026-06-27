"""The runtime key source — resolves the no-train API key at call time, never tracked.

`resolve()` fetches the no-train API key from a SET env var (`ANTHROPIC_API_KEY` — the
anthropic SDK's native var AND the operator's documented injection var) or, as a fallback,
a macOS-keychain `security find-generic-password` command against the `a-plus-maxing-api-key`
keychain item — AT CALL TIME, never captured at module load and never read from a tracked
file. An absent key raises `KeyUnavailableError` fail-loud, naming the env var + the
`keychain-setup.md` runbook.

This mirrors the project's runtime-config-resolution discipline (`pii_scan`'s gitignored
identity config is resolved at call time, never tracked): no API-key literal ever lands in
the repo (NFR-3 — the repo is PUBLIC). The client's default backend calls `resolve()` at
call time, so the key is fetched at runtime, never imported from a constant.
"""

import getpass
import os
import subprocess

# The anthropic SDK's native var AND the operator's documented runtime-injection var
# (S90 directive: `export ANTHROPIC_API_KEY=$(security find-generic-password -s
# "a-plus-maxing-api-key" -w)`). Reading it directly means the operator's existing shell
# export resolves with no extra setup.
ENV_VAR = "ANTHROPIC_API_KEY"

# This project's keychain item — the in-app Profile save (POST /settings/key, via
# `store()`) writes the key here and `resolve()` reads it here, so an in-app paste is
# picked up on the next call with no terminal step. The service name is a project label,
# not a secret — the key VALUE lives only in the keychain at runtime (`keychain-setup.md`).
_KEYCHAIN_SERVICE = "a-plus-maxing-api-key"

_RUNBOOK = "scripts/model/keychain-setup.md"


class KeyUnavailableError(RuntimeError):
    """The no-train API key could not be resolved from any runtime source.

    Raised fail-loud when neither the env var nor the keychain yields a key, naming the
    env var + the runbook so the operator knows how to set it. The key source never
    silently returns a default/empty (that would let a keyless call proceed).
    """


def _keychain_runner():
    """Fetch the key from the macOS keychain at call time, or None when absent.

    Runs `security find-generic-password -w -s <service>` (the `-w` flag prints only the
    password). Returns the stripped key, or None when the item is absent or `security` is
    unavailable (a non-macOS host) — the absence path is the caller's fail-loud trigger.
    """
    try:
        completed = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", _KEYCHAIN_SERVICE],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError):
        return None
    if completed.returncode != 0:
        return None
    key = completed.stdout.strip()
    return key or None


def resolve(keychain_runner=_keychain_runner):
    """Resolve the no-train API key at call time from the env var or the keychain.

    Args:
        keychain_runner (Callable, optional): The keychain fetch seam (returns the key or
            None). Defaults to the macOS `security` command; injected in tests so no real
            keychain or key is touched.

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

    Raised fail-loud when the keychain write returns non-zero or `security` is
    unavailable. The message is CONSTANT and never carries the key value — a store
    failure must not leak the secret into a traceback (NFR-3: the repo is PUBLIC).
    """


def _keychain_writer(key):
    """Write the key into the macOS login keychain at call time (fail-loud on error).

    Runs `security add-generic-password -U -A -a <user> -s <service> -w <key>` (`-U`
    updates the existing item, so an in-app save rotates in place; `-A` grants the item
    an allow-all ACL so the backgrounded server's later `find-generic-password -w` read
    is not blocked on an interactive keychain-access prompt it cannot answer — the
    accepted tradeoff for the in-app key flow on a local single-operator machine). Raises
    `KeyStoreError` on a
    non-zero exit or an unavailable `security` binary (a non-macOS host). The key VALUE
    is passed only as the subprocess argument — never logged, echoed, or written to a
    file; on failure the constant-message error carries no key.

    Args:
        key (str): The no-train API key to store.
    """
    try:
        completed = subprocess.run(
            ["security", "add-generic-password", "-U", "-A",
             "-a", getpass.getuser(), "-s", _KEYCHAIN_SERVICE, "-w", key],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError):
        raise KeyStoreError(
            f"Could not store the key — the macOS keychain is unavailable on this host "
            f"(set the {ENV_VAR} env var instead, per {_RUNBOOK})."
        ) from None
    if completed.returncode != 0:
        raise KeyStoreError("Could not store the key in the macOS keychain.") from None


def store(key, *, keychain_writer=_keychain_writer):
    """Store the no-train API key in the macOS keychain at call time.

    Writes the key into the same `a-plus-maxing-api-key` item `resolve()` reads, so an
    in-app save (the Profile screen's POST `/settings/key`) is picked up by the next
    runtime `resolve()` with no shell command. The key is written ONLY to the OS
    keychain — never to a tracked file, a log, or a returned value (NFR-3: the repo is
    PUBLIC). An empty/blank key is rejected before any write.

    Args:
        key (str): The no-train API key to store.
        keychain_writer (Callable, optional): The keychain write seam (takes the key).
            Defaults to the macOS `security add-generic-password` command; injected in
            tests so no real keychain or key is touched.

    Raises:
        ValueError: When the key is empty/blank — constant message, no key value.
        KeyStoreError: When the keychain write fails.
    """
    key = (key or "").strip()
    if not key:
        raise ValueError("Refusing to store an empty API key.")
    keychain_writer(key)
