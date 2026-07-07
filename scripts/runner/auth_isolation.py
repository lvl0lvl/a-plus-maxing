"""The subscription-session auth env-scrub (ADR-0039-T2).

`build_subscription_env(base_env)` returns a COPY of the parent env with the full
metered/cloud-routing surface (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_USE_BEDROCK`,
`CLAUDE_CODE_USE_VERTEX`, `ANTHROPIC_BASE_URL` — the `_METERED_ROUTING_ENV_VARS` set) dropped and
`CLAUDE_CODE_OAUTH_TOKEN` set from the macOS keychain — so a scheduled subscription session
authenticates via the subscription OAuth token, not metered or cloud credentials. Claude Code's auth
precedence ranks EACH of those vars ABOVE the subscription OAuth token, so a stray one would silently
bill the metered API — or route the session to Bedrock/Vertex cloud credentials, bypassing both the
API key and the OAuth token — instead of the subscription (ADR-0039 Consequences-Negative-3, the
VERIFIED auth-precedence footgun).

It returns a COPY and never mutates the caller's mapping or `os.environ`, so the de-id
`ModelClient` — which resolves `ANTHROPIC_API_KEY` first, then the `a-plus-maxing-api-key` keychain
item, at call time in the DRIVER's own process (`key_source.resolve`) — is unaffected: the
subscription session's OAuth auth AND the de-id client's keychain auth hold simultaneously.

The OAuth token is read from a NEW `a-plus-maxing-oauth-token` keychain item at call time, mirroring
`key_source._keychain_runner`'s `security find-generic-password -w -s <service>` shape — never
captured at module load, never written to a tracked file. `scripts/guard/pii_scan.py` is an
operator-PII scanner with NO secret pattern, so a leaked token value in a tracked file would pass
the PII hooks CLEAN (SEC-02); the control is that the token stays keychain-held, off the tracked
tree (NFR-3: the repo is PUBLIC). An absent token raises `OAuthTokenUnavailableError` fail-loud,
never an env that would run the session unauthenticated.
"""

import subprocess

# Claude Code's subscription OAuth env var (the `claude setup-token` output). Setting it in the
# session's process env — with the metered-API key dropped — makes the session authenticate via the
# subscription rather than the metered API.
OAUTH_ENV_VAR = "CLAUDE_CODE_OAUTH_TOKEN"

# The metered/cloud-routing env vars dropped from the subscription session's env — one home for the
# drop-set. Claude Code ranks EACH above the subscription OAuth token, so a stray value would bill the
# metered API (ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL) or route the session to
# Bedrock / Vertex cloud credentials (CLAUDE_CODE_USE_BEDROCK / CLAUDE_CODE_USE_VERTEX) — bypassing
# the OAuth token entirely (SEC-01).
_METERED_ROUTING_ENV_VARS = frozenset({
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "ANTHROPIC_BASE_URL",
})

# The OAuth token's keychain item — a project label DISTINCT from `a-plus-maxing-api-key` (the
# no-train API key `key_source` owns). The service NAME is a label; the token VALUE lives only in
# the keychain at runtime, never a tracked file.
_KEYCHAIN_SERVICE = "a-plus-maxing-oauth-token"

_RUNBOOK = "scripts/model/keychain-setup.md"


class OAuthTokenUnavailableError(RuntimeError):
    """The subscription OAuth token could not be resolved from the keychain.

    Raised fail-loud when the keychain yields no token, naming the env var + the runbook so the
    operator knows how to set it. The scrub never silently returns an env without the token — a
    silent unauthenticated session is a worse failure than a loud stop. The message is CONSTANT and
    never carries the token value (NFR-3: the repo is PUBLIC).
    """


def _oauth_keychain_reader():
    """Fetch the subscription OAuth token from the macOS keychain at call time, or None when absent.

    Runs `security find-generic-password -w -s a-plus-maxing-oauth-token` (mirroring
    `key_source._keychain_runner`; the `-w` flag prints only the password). Returns the stripped
    token, or None when the item is absent or `security` is unavailable (a non-macOS host) — the
    absence path is the caller's fail-loud trigger.
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
    token = completed.stdout.strip()
    return token or None


def build_subscription_env(base_env, *, keychain_reader=_oauth_keychain_reader):
    """Return a scrubbed COPY of base_env for the subscription session's process env.

    Drops every `_METERED_ROUTING_ENV_VARS` var (the metered-API + cloud-routing surface Claude Code
    ranks ABOVE the subscription OAuth token — so no stray value can bill the metered API or route to
    Bedrock/Vertex cloud credentials) and sets `CLAUDE_CODE_OAUTH_TOKEN` from the keychain at call
    time, preserving every other key. Returns a COPY — never mutates the caller's mapping or
    `os.environ`, so the driver-process de-id `ModelClient` still resolves the `a-plus-maxing-api-key`
    keychain item.

    Args:
        base_env (Mapping): The parent env to scrub (typically a copy of `os.environ`).
        keychain_reader (Callable, optional): The OAuth-token keychain read seam (returns the token
            str or None). Defaults to the macOS `security` read of `a-plus-maxing-oauth-token`;
            injected in tests so no real keychain or token is touched.

    Returns:
        (dict) A copy of base_env with every `_METERED_ROUTING_ENV_VARS` var removed and
        `CLAUDE_CODE_OAUTH_TOKEN` set.

    Raises:
        OAuthTokenUnavailableError: When the keychain yields no token — fail-loud, naming
            `CLAUDE_CODE_OAUTH_TOKEN` + the runbook, never an unauthenticated env.
    """
    token = keychain_reader()
    token = token.strip() if token else token
    if not token:
        raise OAuthTokenUnavailableError(
            f"No subscription OAuth token found. Store the {OAUTH_ENV_VAR} token in the macOS "
            f"keychain per the {_RUNBOOK} runbook (service '{_KEYCHAIN_SERVICE}')."
        )
    scrubbed = dict(base_env)
    for var in _METERED_ROUTING_ENV_VARS:
        scrubbed.pop(var, None)
    scrubbed[OAUTH_ENV_VAR] = token
    return scrubbed
