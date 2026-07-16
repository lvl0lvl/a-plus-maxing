"""The subscription-session auth env-scrub tests (ADR-0039-T2).

Drives `auth_isolation.build_subscription_env` + the wired
`subscription_dispatch.default_session_factory` over injected fake keychain / env / session seams
— 0 live-API spend, 0 real secret, 0 real keychain, 0 real session. The fixture OAuth token AND
the SEC-02 positive-control are ASSEMBLED AT RUNTIME FROM FRAGMENTS (`"sk-ant-" + "oat-" + ...`) so
no verbatim OAuth-token-value substring is ever written to this tracked file; else the AC-5
token-VALUE tree-scan would self-match once this file is committed and go permanently RED (the
SEC-02 time-bomb the recipe forbids). The token-VALUE regex literal below carries a trailing
character class, so the regex does not match its own source text either.
"""

import inspect
import os
import re
import subprocess
from pathlib import Path

import pytest

from scripts import secret_store
from scripts.model import key_source
from scripts.runner import auth_isolation, subscription_dispatch

# tests/runner/test_auth_isolation.py -> tests -> <repo root>; anchors the git tree-scan cwd.
REPO_ROOT = Path(__file__).resolve().parents[2]

# Fragment-assembled at runtime: no verbatim OAuth-token-value substring lands in this file (SEC-02).
# The assembled runtime VALUE lives only in memory (a Python str), never on the tracked tree.
_FIXTURE_OAUTH_TOKEN = "sk-ant-" + "oat-" + "FIXTURE0000"

# The token-VALUE secret pattern (ADR-0039-T2 AC-5 / SEC-02). The trailing "[A-Za-z0-9_-]+" is not
# satisfied by the "[" that follows "oat" in this very literal, so the pattern does not self-match.
_TOKEN_VALUE_PATTERN = re.compile(r"sk-ant-oat[A-Za-z0-9_-]+")


# =====================================================================================
# Cycle 1 — build_subscription_env: env-scrub + keychain read + fail-loud + no-token-on-tree
# =====================================================================================


def test_ac1_stray_api_key_dropped_copy_not_mutated():
    # AC-1: the stray metered-API key is scrubbed from the subscription session's env; unrelated keys
    # survive (non-tautology — a "return OAuth-only dict" reddens); base_env is UNMUTATED (a COPY is
    # returned, so os.environ / the caller's mapping are never edited in place).
    base = {"ANTHROPIC_API_KEY": "sk-stray", "PATH": "/usr/bin", "HOME": "/tmp/x"}
    result = auth_isolation.build_subscription_env(base, keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert "ANTHROPIC_API_KEY" not in result
    assert result["PATH"] == "/usr/bin"
    assert result["HOME"] == "/tmp/x"
    assert base == {"ANTHROPIC_API_KEY": "sk-stray", "PATH": "/usr/bin", "HOME": "/tmp/x"}


@pytest.mark.parametrize("metered_var", sorted(auth_isolation._METERED_ROUTING_ENV_VARS))
def test_metered_routing_var_scrubbed_from_session_env(metered_var):
    # SEC-01: EACH metered/cloud-routing var Claude Code ranks ABOVE the subscription OAuth token is
    # dropped from the built session env. A stray CLAUDE_CODE_USE_BEDROCK / CLAUDE_CODE_USE_VERTEX or
    # ANTHROPIC_{AUTH_TOKEN,BASE_URL} would otherwise route the session to metered/cloud credentials,
    # bypassing both the API key and the OAuth token (the T2-class footgun). Non-tautology guard: an
    # UNRELATED var (PATH) still survives, so a "return OAuth-only dict" that drops everything reddens.
    base = {metered_var: "stray-value", "PATH": "/usr/bin"}
    result = auth_isolation.build_subscription_env(base, keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert metered_var not in result, f"{metered_var} survived the metered/cloud auth scrub (SEC-01)"
    assert result["PATH"] == "/usr/bin", "the scrub dropped an unrelated var (PATH) — over-broad"
    assert result["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN


def test_ac2_oauth_token_set_from_keychain():
    # AC-2: CLAUDE_CODE_OAUTH_TOKEN is set to the value the injected keychain seam returned — the
    # session authenticates via the OAuth token read from the keychain at call time.
    base = {"PATH": "/usr/bin"}
    result = auth_isolation.build_subscription_env(base, keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert result["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN


def test_ac3_deid_client_still_resolves_keychain_under_scrub(monkeypatch):
    # AC-3: the de-id ModelClient is UNAFFECTED by the session scrub. With ANTHROPIC_API_KEY absent
    # from os.environ, key_source.resolve falls through to the keychain (key_source.py:84-86). The
    # mechanism pin: build_subscription_env scrubs a COPY, never os.environ / the caller's mapping,
    # so the driver-process de-id client (which reads os.environ via resolve at call time) still
    # resolves the a-plus-maxing-api-key keychain item.
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert key_source.resolve(keychain_runner=lambda: "kc-api-key") == "kc-api-key"

    base = {"ANTHROPIC_API_KEY": "sk-stray", "PATH": "/usr/bin"}
    env_before = dict(os.environ)
    result = auth_isolation.build_subscription_env(base, keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert dict(os.environ) == env_before, "build_subscription_env mutated os.environ (de-id scrub leak)"
    assert base["ANTHROPIC_API_KEY"] == "sk-stray", "build_subscription_env mutated the caller's mapping"
    assert "ANTHROPIC_API_KEY" not in result
    # both hold simultaneously: the de-id client still resolves the keychain even after the scrub ran.
    assert key_source.resolve(keychain_runner=lambda: "kc-api-key") == "kc-api-key"


def test_ac4_fail_loud_on_absent_token():
    # AC-4: an absent/empty keychain token fails loud (typed error naming CLAUDE_CODE_OAUTH_TOKEN),
    # never an env that would run the session unauthenticated. Failing-capable: a silent fall-through
    # returning an env without the token reddens the pytest.raises.
    base = {"PATH": "/usr/bin"}
    for absent in (lambda: None, lambda: "", lambda: "   "):
        with pytest.raises(auth_isolation.OAuthTokenUnavailableError) as exc:
            auth_isolation.build_subscription_env(base, keychain_reader=absent)
        assert "CLAUDE_CODE_OAUTH_TOKEN" in str(exc.value)


def _scan_targets():
    """Every tracked file (git ls-files) plus the two T2 Create paths (untracked pre-commit).

    Superset of the recipe's `git ls-files` scan: it additionally covers the two new files BEFORE
    they are committed, so a self-match in this test file or auth_isolation.py is caught pre-commit,
    not only after the SEC-02 time-bomb would already be tracked.
    """
    listed = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, cwd=REPO_ROOT, check=True
    )
    targets = {line for line in listed.stdout.splitlines() if line}
    targets.add("scripts/runner/auth_isolation.py")
    targets.add("tests/runner/test_auth_isolation.py")
    return sorted(targets)


def _token_value_hits(rel_paths):
    hits = []
    for rel in rel_paths:
        path = REPO_ROOT / rel
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if _TOKEN_VALUE_PATTERN.search(text):
            hits.append(rel)
    return hits


def test_ac5_no_oauth_token_value_on_the_tracked_tree():
    # AC-5 (SEC-02): the OAuth token is keychain-held at call time, never a tracked literal.
    # (non-vacuity) the pattern MATCHES a runtime-assembled positive-control — proving the 0-hit
    # signal is real, not a dead regex.
    positive_control = "sk-ant-" + "oat-" + "SYNTHETIC0000"
    assert _TOKEN_VALUE_PATTERN.search(positive_control), (
        "the token-VALUE regex fails to match a real token shape — the tree-scan would be vacuous"
    )
    # (a, name-literal) 0 hardcoded token-value literals in scripts/runner/.
    runner_rel = [
        str(p.relative_to(REPO_ROOT))
        for p in sorted((REPO_ROOT / "scripts/runner").glob("*.py"))
    ]
    assert _token_value_hits(runner_rel) == [], "a hardcoded OAuth token value is present in scripts/runner/"
    # (b, whole-tree) 0 token-value hits across the tracked tree (+ the two new files pre-commit).
    assert _token_value_hits(_scan_targets()) == [], "an OAuth token value is present on the tracked tree"


# =====================================================================================
# Cycle 2 — wire the scrub into the session factory (subscription_dispatch Modify)
# =====================================================================================


class _SpySpawn:
    """A stub session-spawn seam: records the env it is handed, returns a fixed stub session.

    0 live spend — construction ≠ dispatch, no live Agent-SDK call fires (a stub is returned).
    """

    def __init__(self, stub):
        self.stub = stub
        self.env = None

    def __call__(self, env):
        self.env = env
        return self.stub


def test_ac6_session_env_carries_the_scrub(monkeypatch):
    # AC-6: subscription_dispatch constructs the session with an env produced by
    # build_subscription_env — a spy over the session-spawn seam asserts the handed env has no
    # ANTHROPIC_API_KEY and a set CLAUDE_CODE_OAUTH_TOKEN. The scrubbed-env marker is set so the
    # default factory proceeds past the SEC-04 gate; the keychain + spawn seams are injected fakes.
    monkeypatch.setenv(subscription_dispatch.SUBSCRIPTION_ENV_SCRUBBED_MARKER, "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-stray")
    spy = _SpySpawn(stub=object())
    subscription_dispatch.default_session_factory(
        keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN, session_spawn=spy)
    assert spy.env is not None, "the session-spawn seam was never handed an env"
    assert "ANTHROPIC_API_KEY" not in spy.env, "a stray ANTHROPIC_API_KEY reached the session env"
    assert spy.env["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN


def test_ac8_scrubbed_factory_constructs_and_drops_stray(monkeypatch):
    # AC-8 (SEC-04): the INVERSE of T1's test_default_session_factory_refuses. With the scrub applied
    # (marker set) the DEFAULT factory under injected fake keychain + spawn seams CONSTRUCTS — it
    # returns the session and does NOT raise (T1 AC-9's pre-scrub refusal is lifted) — AND still
    # drops a stray metered key. 0-spend: the injected spawn seam returns a stub, no live call fires.
    monkeypatch.setenv(subscription_dispatch.SUBSCRIPTION_ENV_SCRUBBED_MARKER, "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-stray")
    stub = object()
    spy = _SpySpawn(stub=stub)
    session = subscription_dispatch.default_session_factory(
        keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN, session_spawn=spy)
    assert session is stub, "the scrubbed factory did not construct/return the session (T1 AC-9 not lifted)"
    assert "ANTHROPIC_API_KEY" not in spy.env, "a stray ANTHROPIC_API_KEY survived into the session env"
    assert spy.env["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN


def test_default_spawn_seam_constructs_inertly_and_dispatch_fail_louds(monkeypatch):
    # The PRODUCTION default spawn seam (no injected session_spawn) constructs INERTLY — construct ≠
    # dispatch, the 0-spend property REFACTOR step 7 pins — returning a scrubbed-env-bound session
    # with no live call, and fail-louds on a live dispatch rather than fabricate a backend or run
    # unauthenticated (ADR-0039 OQ-1 deferred to the operator-gated live-enable). Only the keychain
    # seam is injected, so the real default spawner (_spawn_subscription_session) runs.
    monkeypatch.setenv(subscription_dispatch.SUBSCRIPTION_ENV_SCRUBBED_MARKER, "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-stray")
    session = subscription_dispatch.default_session_factory(keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert "ANTHROPIC_API_KEY" not in session.env
    assert session.env["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN
    with pytest.raises(subscription_dispatch.SubscriptionSessionNotLive):
        session("workout", "PROMPT-TEXT", {"goal-domains": ["strength"]})


# =====================================================================================
# ADR-0047-T2 — the OAuth-token default reader routed through the secret-store abstraction
# =====================================================================================


def test_build_subscription_env_seam_param_unchanged():
    # AC-2: build_subscription_env keeps its keychain_reader seam name; an injected fake still overrides
    # the new secret_store-backed default. RED-capable: a renamed param reds the signature assertion.
    assert "keychain_reader" in inspect.signature(auth_isolation.build_subscription_env).parameters
    result = auth_isolation.build_subscription_env(
        {"PATH": "/usr/bin"}, keychain_reader=lambda: _FIXTURE_OAUTH_TOKEN)
    assert result["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN


def test_oauth_default_reader_routes_through_abstraction(monkeypatch):
    # AC-2/AC-4: the DEFAULT keychain_reader routes through secret_store.get_secret for the EXACT
    # `a-plus-maxing-oauth-token` service (SF-1 service-keyed — a transposition to the api-key service
    # returns None here and reds). None-on-absent -> OAuthTokenUnavailableError unchanged. Drives the
    # DEFAULT reader (no injected seam) so it proves the default itself re-points onto the abstraction.
    seen = []

    def _fake_get(service):
        seen.append(service)
        return _FIXTURE_OAUTH_TOKEN if service == "a-plus-maxing-oauth-token" else None

    monkeypatch.setattr(secret_store, "get_secret", _fake_get)
    result = auth_isolation.build_subscription_env({"PATH": "/usr/bin"})
    assert seen == ["a-plus-maxing-oauth-token"], "the default reader read the wrong keychain service"
    assert result["CLAUDE_CODE_OAUTH_TOKEN"] == _FIXTURE_OAUTH_TOKEN

    monkeypatch.setattr(secret_store, "get_secret", lambda service: None)
    with pytest.raises(auth_isolation.OAuthTokenUnavailableError):
        auth_isolation.build_subscription_env({"PATH": "/usr/bin"})
