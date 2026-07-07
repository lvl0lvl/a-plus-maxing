"""The subscription-sub-agent dispatch seam + the pre-scrub session-factory refusal (ADR-0039-T1).

`build_dispatch(session)` adapts an injected subscription SESSION into the unified
`dispatch(name, prompt, context) -> author envelope` seam the built plan loop consumes
(`plan_orchestrator.py:148`): it routes each specialist / judge / lens call through the session as
a subscription sub-agent and returns the author envelope. It reads no store, de-identifies nothing,
and re-hosts no loop logic — the already-de-identified `(name, prompt, context)` tuple is routed to
the session as-is (the de-id-IN happens INSIDE the loop, upstream of this seam).

The DEFAULT (non-injected) production session factory stays disabled-by-default (SEC-04):
`default_session_factory` raises `SubscriptionEnvNotScrubbed` while the runtime scrubbed-env marker
is absent (the scrub unapplied). Once the marker is set (the ADR-0039-T2 auth env-scrub enabled at
the operator-gated live-enable), it builds the scrubbed session env via
`auth_isolation.build_subscription_env` — dropping a stray `ANTHROPIC_API_KEY`, setting
`CLAUDE_CODE_OAUTH_TOKEN` from the keychain — and hands it to the session-spawn seam, so the session
PROCESS env authenticates via the subscription OAuth token, not the metered API. Gating on that
runtime-detectable marker (Architect-F2 — NOT "T2 not yet merged") let ADR-0039-T2 lift the T1 AC-9
refusal with no edit to the T1 refusal test (it always exercises the scrub-absent path). The
concrete subscription backend behind the spawn seam (ADR-0039 OQ-1 — `claude -p` vs the Agent SDK)
is pinned at the operator-gated live-enable; construction is inert (construct ≠ dispatch), and tests
inject fake keychain / spawn seams so no real keychain or session is touched.

Module import performs 0 side effects (0 `signal` / de-id / dispatch) — importing the seam arms
nothing.
"""

import os

from scripts.runner.auth_isolation import build_subscription_env

# The runtime marker gating the default factory: its presence is the "scrub enabled" predicate, set
# at the operator-gated live-enable (off by default — SEC-04, disabled-by-default). A
# runtime-detectable condition the T1 refusal test controls (it deletes the marker), so T2 lifts the
# refusal on the marker-present path with no edit to the T1 test. `build_subscription_env` returns a
# COPY and never sets this in `os.environ` (AC-3: it must not mutate the env, so the de-id client's
# keychain resolution stays intact).
SUBSCRIPTION_ENV_SCRUBBED_MARKER = "A_PLUS_MAXING_SUBSCRIPTION_ENV_SCRUBBED"


class SubscriptionEnvNotScrubbed(RuntimeError):
    """The subscription auth env-scrub marker is unset — refusing to build a live session (SEC-04)."""


def build_dispatch(session):
    """Adapt a subscription session into the built loop's unified dispatch seam.

    Returns the `dispatch(name, prompt, context) -> author envelope` seam
    (`plan_orchestrator.py:148`): each specialist / judge / lens call is routed through `session`
    as a subscription sub-agent, and the session's author envelope is returned unaltered. Routes
    the already-de-identified tuple only — reads no store, de-identifies nothing, re-hosts no loop
    logic.

    Args:
        session (Callable): The subscription session, `session(name, prompt, context) -> envelope`
            (a real Agent-SDK-backed session in production, a fixture recording session in tests).

    Returns:
        (Callable) The `dispatch(name, prompt, context)` seam the built loop consumes.
    """
    def dispatch(name, prompt, context):
        return session(name, prompt, context)

    return dispatch


def _subscription_env_scrubbed():
    """Whether the ADR-0039-T2 subscription auth env-scrub has been applied (the runtime marker)."""
    return os.environ.get(SUBSCRIPTION_ENV_SCRUBBED_MARKER) == "1"


class SubscriptionSessionNotLive(RuntimeError):
    """A live subscription dispatch was attempted before the OQ-1 backend is pinned (ADR-0039)."""


class _ScrubbedSubscriptionSession:
    """An inert subscription session bound to a scrubbed process env (ADR-0039-T2).

    Construction fires 0 live calls — it only binds the scrubbed env (no `ANTHROPIC_API_KEY`,
    `CLAUDE_CODE_OAUTH_TOKEN` set) for the session subprocess, mirroring
    `_ClaudeNoTrainBackend._client()`'s lazy-at-call-time posture (construct ≠ dispatch). The
    concrete subscription backend (ADR-0039 OQ-1 — `claude -p` vs the Agent SDK, evaluated on
    top-level raw-PII containment, unsettled in this build) is pinned at the operator-gated
    live-enable, so a live dispatch fail-louds here rather than fabricate a backend or run the
    session unauthenticated.

    Attributes:
        env (dict): The scrubbed process env the session subprocess authenticates under.
    """

    def __init__(self, env):
        self.env = env

    def __call__(self, name, prompt, context):
        raise SubscriptionSessionNotLive(
            "the concrete subscription-session backend (ADR-0039 OQ-1: `claude -p` vs the Agent "
            "SDK) is pinned at the operator-gated live-enable; no live subscription dispatch is "
            "wired in this build")


def _spawn_subscription_session(env):
    """The default session-spawn seam: bind the scrubbed env onto an inert subscription session.

    Construction is INERT (0 live calls) — the live dispatch backend is deferred (ADR-0039 OQ-1,
    see `_ScrubbedSubscriptionSession`). Injected with a spy/stub in tests so no real session
    spawns (0 live spend).

    Args:
        env (Mapping): The scrubbed process env (from `build_subscription_env`).

    Returns:
        (Callable) The subscription session, `session(name, prompt, context) -> envelope`.
    """
    return _ScrubbedSubscriptionSession(env)


def default_session_factory(*, keychain_reader=None, session_spawn=None):
    """The production (non-injected) subscription-session factory — refuses pre-scrub (SEC-04).

    Raises `SubscriptionEnvNotScrubbed` while the ADR-0039-T2 auth env-scrub is unapplied (the
    scrubbed-env marker absent) — a live subscription session is not constructible before the scrub
    is enabled (disabled-by-default). Once the marker is set (the scrub enabled at the operator-gated
    live-enable), it builds the scrubbed session env via `auth_isolation.build_subscription_env`
    (drop a stray `ANTHROPIC_API_KEY`, set `CLAUDE_CODE_OAUTH_TOKEN` from the keychain) and hands it
    to the session-spawn seam — so the session PROCESS env authenticates via the subscription OAuth
    token, not the metered API. This LIFTS the T1 AC-9 pre-scrub refusal (that test always exercises
    the scrub-absent path, so the lift needs no edit to it).

    Args:
        keychain_reader (Callable, optional): The OAuth-token keychain read seam handed to
            `build_subscription_env`; defaults to its own keychain read. Injected in tests.
        session_spawn (Callable, optional): The session-spawn seam — takes the scrubbed env, returns
            the subscription session. Defaults to the inert `_spawn_subscription_session`; injected
            in tests so no real session spawns (construct ≠ dispatch — 0 live spend).

    Returns:
        (Callable) The subscription session, `session(name, prompt, context) -> envelope`.
    """
    if not _subscription_env_scrubbed():
        raise SubscriptionEnvNotScrubbed(
            f"the subscription auth env-scrub marker {SUBSCRIPTION_ENV_SCRUBBED_MARKER!r} is unset "
            "— refusing to construct a live subscription session (SEC-04). `build_subscription_env` "
            "IS wired (it runs once the marker is present); the gate is the MARKER, not a missing "
            "scrub. The marker is set at the operator-gated live-enable after the env-scrub is "
            "applied (bead r3vw); it is deliberately unset while the runner is disabled by default.")
    base_env = dict(os.environ)
    scrubbed_env = (
        build_subscription_env(base_env)
        if keychain_reader is None
        else build_subscription_env(base_env, keychain_reader=keychain_reader)
    )
    spawn = session_spawn if session_spawn is not None else _spawn_subscription_session
    return spawn(scrubbed_env)
