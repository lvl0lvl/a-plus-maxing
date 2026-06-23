"""The runtime key source — resolves the no-train API key at call time, never tracked.

`resolve()` fetches the no-train API key from a SET env var (`ANTHROPIC_API_KEY` — the
anthropic SDK's native var AND the operator's documented injection var) or, as a fallback,
a macOS-keychain `security find-generic-password` command against the `quant-primary-api`
keychain item — AT CALL TIME, never captured at module load and never read from a tracked
file. An absent key raises `KeyUnavailableError` fail-loud, naming the env var + the
`keychain-setup.md` runbook.

This mirrors the project's runtime-config-resolution discipline (`pii_scan`'s gitignored
identity config is resolved at call time, never tracked): no API-key literal ever lands in
the repo (NFR-3 — the repo is PUBLIC). The client's default backend calls `resolve()` at
call time, so the key is fetched at runtime, never imported from a constant.
"""

import os
import subprocess

# The anthropic SDK's native var AND the operator's documented runtime-injection var
# (S90 directive: `export ANTHROPIC_API_KEY=$(security find-generic-password -s
# "quant-primary-api" -w)`). Reading it directly means the operator's existing shell
# export resolves with no extra setup.
ENV_VAR = "ANTHROPIC_API_KEY"

# The keychain item the runbook stores the key under (`keychain-setup.md`). The service
# name is a label, not a secret — the key VALUE lives only in the keychain at runtime.
# Matches the operator's existing keychain item (`quant-primary-api`), so the keychain
# fallback resolves the same key the operator already injects via the env var.
_KEYCHAIN_SERVICE = "quant-primary-api"

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
