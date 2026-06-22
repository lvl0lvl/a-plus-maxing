"""The runtime key source — resolves the no-train API key at call time, never tracked.

`resolve()` fetches the no-train API key from a SET env var (`APLUS_NOTRAIN_API_KEY`) or,
as a fallback, a macOS-keychain `security find-generic-password` command — AT CALL TIME,
never captured at module load and never read from a tracked file. An absent key raises
`KeyUnavailableError` fail-loud, naming the env var + the `keychain-setup.md` runbook.

This mirrors the project's runtime-config-resolution discipline (`pii_scan`'s gitignored
identity config is resolved at call time, never tracked): no API-key literal ever lands in
the repo (NFR-3 — the repo is PUBLIC). The client's default backend calls `resolve()` at
call time, so the key is fetched at runtime, never imported from a constant.
"""

import os
import subprocess

ENV_VAR = "APLUS_NOTRAIN_API_KEY"

# The keychain item the runbook stores the key under (`keychain-setup.md`). The service
# name is a label, not a secret — the key VALUE lives only in the keychain at runtime.
_KEYCHAIN_SERVICE = "aplus-notrain-api-key"

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
