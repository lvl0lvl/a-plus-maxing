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

import inspect
import subprocess
from pathlib import Path

import pytest

from scripts import secret_store
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


# --- ADR-0047-T2: key_source routed through the secret-store abstraction --------
#
# The DEFAULT resolve/store seams now route through scripts.secret_store (the ADR-0047-T1
# abstraction) instead of a direct `security` shell-out, KEEPING the seam names, env-first
# order, None-on-absent contract, and the key_source.KeyStoreError write-error class. The
# default-driving tests mock secret_store's module functions ($0, no real keychain).

_ROUNDTRIP_KEY = "adr-0047-t2-roundtrip-fixture"  # synthetic, not sk-ant-shaped
_T2_CONSUMER_FILES = ["scripts/model/key_source.py", "scripts/runner/auth_isolation.py"]
_REPO_ROOT = Path(__file__).resolve().parents[2]


def test_seam_params_unchanged():
    """AC-1: resolve/store keep their keychain_* seam names; an injected fake still overrides."""
    assert "keychain_runner" in inspect.signature(key_source.resolve).parameters
    assert "keychain_writer" in inspect.signature(key_source.store).parameters
    seen = []
    key_source.store(_ROUNDTRIP_KEY, keychain_writer=seen.append)
    assert seen == [_ROUNDTRIP_KEY], "the injected keychain_writer did not override the default"


def test_no_security_shellout():
    """AC-3 (CODE-FORM): 0 list-form `security` shell-outs + 0 `import subprocess` in the consumers."""
    code_form = subprocess.run(
        ["grep", "-rnE", r'\[\s*"security"\s*,\s*"(find|add)-generic-password"', *_T2_CONSUMER_FILES],
        cwd=_REPO_ROOT, capture_output=True, text=True,
    )
    assert code_form.returncode == 1, f"a list-form `security` shell-out survives:\n{code_form.stdout}"
    imports = subprocess.run(
        ["grep", "-rn", "import subprocess", *_T2_CONSUMER_FILES],
        cwd=_REPO_ROOT, capture_output=True, text=True,
    )
    assert imports.returncode == 1, f"a dead `import subprocess` survives in a consumer:\n{imports.stdout}"


def test_consumers_call_secret_store_module_qualified():
    """SF-2: the consumers call `secret_store.<fn>` module-qualified, never `from scripts.secret_store import`.

    A from-import binding would make the AC-5 module-attr spy observe 0 falsely (defeating the
    env-first falsification), so it is gated mechanically.
    """
    from_import = subprocess.run(
        ["grep", "-rn", "from scripts.secret_store import", *_T2_CONSUMER_FILES],
        cwd=_REPO_ROOT, capture_output=True, text=True,
    )
    assert from_import.returncode == 1, (
        "a from-import of secret_store defeats the module-attr spy:\n" + from_import.stdout
    )
    module_qualified = subprocess.run(
        ["grep", "-rnE", r"secret_store\.(get|set)_secret", *_T2_CONSUMER_FILES],
        cwd=_REPO_ROOT, capture_output=True, text=True,
    )
    assert module_qualified.returncode == 0, "the consumers never call secret_store module-qualified (vacuous)"


def test_resolve_env_first_no_abstraction_read(monkeypatch):
    """AC-5: a set ANTHROPIC_API_KEY resolves WITHOUT reading the abstraction (env-first preserved).

    Spies on the secret_store.get_secret MODULE attribute (not an injected keychain_runner, which
    would only re-test the pre-existing env-vs-seam order). RED-capable: reorder resolve to read the
    abstraction before the env check -> the spy count is >= 1.
    """
    monkeypatch.setenv(ENV_VAR, "env-wins-token")
    calls = []
    monkeypatch.setattr(secret_store, "get_secret", lambda service: calls.append(service))
    assert resolve() == "env-wins-token"
    assert calls == [], "resolve read secret_store before the env var (env-first regressed)"


def test_abstraction_roundtrip(monkeypatch):
    """AC-4: store->resolve round-trips through the abstraction; None-on-absent -> fail-loud unchanged.

    SF-1: the mock is SERVICE-KEYED and the api-key default asserts the EXACT service string, so a
    transposition to the oauth-token service reds. RED-capable (absent): a default returning a truthy
    sentinel on absent -> resolve returns it instead of raising -> the KeyUnavailableError assert reds.
    """
    monkeypatch.delenv(ENV_VAR, raising=False)
    vault = {}
    monkeypatch.setattr(secret_store, "set_secret", lambda service, value: vault.__setitem__(service, value))
    monkeypatch.setattr(secret_store, "get_secret", lambda service: vault.get(service))

    key_source.store(_ROUNDTRIP_KEY)
    assert vault == {"a-plus-maxing-api-key": _ROUNDTRIP_KEY}, "store routed to the wrong service"
    assert resolve() == _ROUNDTRIP_KEY, "resolve did not recover the stored key byte-for-byte"

    vault.clear()
    with pytest.raises(KeyUnavailableError):
        resolve()  # secret_store.get_secret None-on-absent -> fail-loud unchanged


def test_resolve_strips_padded_keychain_value(monkeypatch):
    """The default read path strips a padded keychain value (an out-of-band write can carry a newline).

    Drives the DEFAULT `_keychain_runner` via the `secret_store.get_secret` module-attr (not an
    injected runner). RED-capable: drop the strip in `_keychain_runner` -> resolve returns the padded
    value and this assert reds.
    """
    monkeypatch.delenv(ENV_VAR, raising=False)
    monkeypatch.setattr(secret_store, "get_secret", lambda service: "  padded-key  ")
    assert resolve() == "padded-key", "resolve did not strip a padded keychain value"


def test_resolve_fail_loud_on_whitespace_only_keychain_value(monkeypatch):
    """A whitespace-only keychain value collapses to absent -> fail-loud (not a truthy garbage key).

    Drives the DEFAULT `_keychain_runner`. RED-capable: drop the strip/collapse -> resolve returns
    "   " as a truthy key, no KeyUnavailableError is raised, and this `pytest.raises` reds.
    """
    monkeypatch.delenv(ENV_VAR, raising=False)
    monkeypatch.setattr(secret_store, "get_secret", lambda service: "   ")
    with pytest.raises(KeyUnavailableError):
        resolve()


def test_frozen_six_numstat_empty():
    """AC-6: the ADR-0032 frozen-six are byte-frozen vs the fixed fork-point (PF-S133-03)."""
    six = [
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
    ]
    result = subprocess.run(
        ["git", "diff", "--numstat", "3ab1c3abb6c995fbaaadcb179735759e4a61d73d", "--", *six],
        cwd=_REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert result.stdout == "", f"a frozen-six file changed:\n{result.stdout}"
