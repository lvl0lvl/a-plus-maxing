"""Tests for the runtime key source (ADR-0015-T1, AC-5).

`scripts.model.key_source.resolve()` fetches the no-train API key at RUNTIME — from a set
env var or a macOS-keychain `security find-generic-password` command — and NEVER from a
tracked file. An absent key raises fail-loud, naming the env var + the `keychain-setup.md`
runbook. These tests pin:

  - a SET env var resolves at call time;
  - the keychain command is the fallback when the env var is unset;
  - an UNSET key (env unset + keychain empty) raises fail-loud naming how to set it;
  - `resolve()` opens NO tracked file;
  - the tracked tree carries 0 API-key literal (the repo is PUBLIC, NFR-3).

The key tests use a SET env var or an injected fake keychain runner — never a live API,
never a real key.
"""

import subprocess

import pytest

from scripts.model import key_source
from scripts.model.key_source import ENV_VAR, KeyUnavailableError, resolve


def test_env_var_is_the_anthropic_native_var():
    """ADR-0015 S90: the env var is `ANTHROPIC_API_KEY` (the anthropic SDK + operator var).

    The operator's documented runtime injection sets `ANTHROPIC_API_KEY` from the
    `a-plus-maxing-api-key` keychain item. Reds if the env var is renamed away from the
    anthropic-native / operator-documented name.
    """
    assert ENV_VAR == "ANTHROPIC_API_KEY"
    assert key_source._KEYCHAIN_SERVICE == "a-plus-maxing-api-key"


# --- AC-5: a set env var resolves at call time --------------------------------


def test_resolve_reads_set_env_var(monkeypatch):
    """AC-5: a SET env var is read at call time and returned."""
    monkeypatch.setenv(ENV_VAR, "env-provided-test-token")

    assert resolve() == "env-provided-test-token"


def test_resolve_reads_env_var_at_call_time_not_import_time(monkeypatch):
    """AC-5: the key is fetched at CALL time (set after import still resolves)."""
    monkeypatch.delenv(ENV_VAR, raising=False)
    monkeypatch.setenv(ENV_VAR, "set-after-import")

    assert resolve() == "set-after-import"


# --- AC-5: the keychain command is the fallback --------------------------------


def test_resolve_falls_back_to_keychain_command(monkeypatch):
    """AC-5: with the env var unset, `resolve` runs the keychain fetch command."""
    monkeypatch.delenv(ENV_VAR, raising=False)
    calls = []

    def _fake_keychain_runner():
        calls.append(True)
        return "keychain-provided-token"

    assert resolve(keychain_runner=_fake_keychain_runner) == "keychain-provided-token"
    assert calls == [True], "the keychain runner was not called at call time"


# --- AC-5: an UNSET key raises fail-loud ---------------------------------------


def test_resolve_raises_fail_loud_when_key_absent(monkeypatch):
    """AC-5: env unset + keychain empty raises fail-loud naming how to set it."""
    monkeypatch.delenv(ENV_VAR, raising=False)

    with pytest.raises(KeyUnavailableError) as excinfo:
        resolve(keychain_runner=lambda: None)

    message = str(excinfo.value)
    assert ENV_VAR in message, "fail-loud message must name the env var"
    assert "ANTHROPIC_API_KEY" in message, "fail-loud message must name ANTHROPIC_API_KEY"
    assert "a-plus-maxing-api-key" in message, "fail-loud message must name the keychain item"
    assert "keychain-setup.md" in message, "fail-loud message must name the runbook"


def test_resolve_does_not_silently_return_a_default(monkeypatch):
    """AC-5: an absent key never silently returns a default/empty (would let a keyless call proceed)."""
    monkeypatch.delenv(ENV_VAR, raising=False)

    returned = "UNSET"
    try:
        returned = resolve(keychain_runner=lambda: "")
    except KeyUnavailableError:
        returned = "RAISED"
    assert returned == "RAISED", "an absent key returned a default instead of raising"


# --- AC-5: resolve opens no tracked file ---------------------------------------


def test_resolve_opens_no_tracked_file(monkeypatch):
    """AC-5: `resolve` reads NO tracked file — the only sources are env + keychain."""
    monkeypatch.setenv(ENV_VAR, "env-token")

    opened = []
    real_open = open

    def _tracking_open(path, *args, **kwargs):
        opened.append(str(path))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", _tracking_open)
    resolve()

    assert opened == [], f"resolve opened a file: {opened}"


# --- AC-5: 0 API-key literal in the tracked tree -------------------------------


def test_no_api_key_literal_in_tracked_tree():
    """AC-5: `rg` over the tracked tree finds 0 API-key literal (the repo is PUBLIC)."""
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    # Exclude this test file and the recipe/build-plan docs, which legitimately carry the
    # rg PATTERN string itself (not a key) as the gate definition.
    excluded = {
        "tests/model/test_key_source.py",
        "docs/task-plan/ADR-0015-T1.md",
        "docs/build-plan/build-plan-conversational-intake.md",
    }
    targets = [
        f
        for f in tracked
        if f and not f.startswith(".venv") and f not in excluded
    ]
    result = subprocess.run(
        ["rg", "-n", r"sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{40,}", *targets],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        "an API-key literal is in the tracked tree (PUBLIC repo):\n" + result.stdout
    )
