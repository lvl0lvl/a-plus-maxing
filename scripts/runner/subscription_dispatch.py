"""The subscription-sub-agent dispatch seam + the pre-scrub session-factory refusal (ADR-0039-T1).

`build_dispatch(session)` adapts an injected subscription SESSION into the unified
`dispatch(name, prompt, context) -> author envelope` seam the built plan loop consumes
(`plan_orchestrator.py:148`): it routes each specialist / judge / lens call through the session as
a subscription sub-agent and returns the author envelope. It reads no store, de-identifies nothing,
and re-hosts no loop logic — the already-de-identified `(name, prompt, context)` tuple is routed to
the session as-is (the de-id-IN happens INSIDE the loop, upstream of this seam).

The DEFAULT (non-injected) production session factory refuses to construct a live subscription
session while the ADR-0039-T2 auth env-scrub (`build_subscription_env`) is unapplied (SEC-04,
disabled-by-default): `default_session_factory` raises `SubscriptionEnvNotScrubbed` while the
runtime scrubbed-env marker is absent. Gating the refusal on that runtime-detectable predicate
(Architect-F2 — NOT "T2 not yet merged") lets ADR-0039-T2 lift it by APPLYING the scrub (which
sets the marker) and wiring the real Agent-SDK construction, with no edit to the T1 refusal test
(that test always exercises the scrub-absent path). Tests inject a fixture session; the unscrubbed
production path stays refused.

Module import performs 0 side effects (0 `signal` / de-id / dispatch) — importing the seam arms
nothing.
"""

import os

# The runtime marker the ADR-0039-T2 auth env-scrub (`build_subscription_env`) sets AFTER scrubbing
# the subscription session's environment. Its presence is the "scrub applied" predicate the default
# factory gates its refusal on — a runtime-detectable condition the T1 refusal test controls, so T2
# lifts the refusal by applying the scrub without editing the T1 test.
SUBSCRIPTION_ENV_SCRUBBED_MARKER = "A_PLUS_MAXING_SUBSCRIPTION_ENV_SCRUBBED"


class SubscriptionEnvNotScrubbed(RuntimeError):
    """The subscription auth env-scrub is unapplied — refusing to build a live session (SEC-04)."""


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


def default_session_factory():
    """The production (non-injected) subscription-session factory — refuses pre-scrub (SEC-04).

    Raises `SubscriptionEnvNotScrubbed` while the ADR-0039-T2 auth env-scrub is unapplied (the
    scrubbed-env marker absent) — a live subscription session is not constructible before the scrub
    is wired (disabled-by-default). ADR-0039-T2 lifts the refusal by applying the scrub (which sets
    the marker) and wiring the real Agent-SDK session construction below; the T1 refusal test always
    exercises the scrub-absent path, so the lift needs no edit to it.
    """
    if not _subscription_env_scrubbed():
        raise SubscriptionEnvNotScrubbed(
            "the subscription auth env-scrub (ADR-0039-T2 build_subscription_env) is not applied; "
            "refusing to construct a live subscription session pre-scrub (SEC-04)")
    # Scrub applied: ADR-0039-T2's real Agent-SDK session construction site (unbuilt in T1). Fail
    # loud rather than return a non-session so no live session is ever built before T2 wires it.
    raise SubscriptionEnvNotScrubbed(
        "scrubbed-env subscription session construction is wired by ADR-0039-T2")
