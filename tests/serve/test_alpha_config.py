"""Tests for the out-of-band alpha-config loader + the D5 shared-key provisioning bridge.

The alpha build distributes shared vendor OAuth credentials (`client_id`/`client_secret`
per confidential-client vendor) + an optional shared Anthropic key OUT OF BAND — a config
file on a path named by an env var, OUTSIDE the repo tree, never a tracked file (D4/D5:
the shared secrets are global-revoke credentials on a PUBLIC repo). The loader reads it;
the D5 bridge exports the shared Anthropic key onto the env-first key path ONLY when no
bring-your-own key resolves (0 clobber).

Crown-jewel constraints under test:
  * out-of-band ONLY — an in-repo config path RAISES, case-folded so an APFS case-variant
    (`A-PLUS-MAXING/...`) cannot slip past a lexical `is_relative_to` (SEC-1);
  * 0 tracked secret — a value-shape scan over `git ls-files` finds 0 real-length keys;
  * 0 BYO clobber — the bridge acts ONLY on `KeyUnavailableError`, so a BYO key (env-first
    or keychain) is never overwritten (the shared key is the DEFAULT, not an override);
  * 0 secret leak — no secret value reaches an exception string or a log record.

Every fixture is SYNTHETIC (short `sk-ant-test-…` / a synthetic `client_secret`, never a
real secret) and lives on `tmp_path` OUTSIDE the repo tree. ALL env control is via pytest
`monkeypatch` (there is no `tests/serve/conftest.py`), so a process-global export cannot
leak into the whole-suite baseline. The bridge's `resolve` seam is injected as
`partial(key_source.resolve, keychain_runner=<empty>)` — the env-first branch stays REAL
(so the no-BYO `KeyUnavailableError` is genuine, not a stipulated fake), only the macOS
keychain shell-out is faked. No model call is made (`anthropic` stays absent).
"""

import json
import logging
import os
import re
import subprocess
from functools import partial
from pathlib import Path

import pytest

from scripts.model import key_source
from scripts.serve import alpha_config

REPO_ROOT = Path(__file__).resolve().parents[2]

# --- Synthetic fixtures (AC-3-safe: never match the value-shape secret scan) --------------
# Shared Anthropic key + a DISTINCT bring-your-own key (QA-F3 — a shared==byo pair makes the
# no-clobber assertion vacuous). Both are short (< 20 chars after `sk-ant-`), so the AC-3
# `sk-ant-[A-Za-z0-9_-]{20,}` value-scan does NOT match them (they are not real-length keys).
_SHARED_KEY = "sk-ant-test-shared"
_BYO_KEY = "sk-ant-test-byo"
# A synthetic confidential-vendor secret — 20 chars, not key-shaped, and this UPPERCASE var
# name is not the lowercase `client_secret` label the value-scan keys on, so it is scan-safe.
_WHOOP_CLIENT_ID = "whoop-id-fixture"
_WHOOP_CLIENT_SECRET = "whoop-secret-fixture"
# A no-leak sentinel — distinctive, not `sk-ant-`-shaped, so it is scan-safe even in source.
_SENTINEL = "SENTINEL-leak-probe"


def _empty_keychain():
    """A keychain seam that finds no key — so `resolve` falls through to its env-first tier."""
    return None


# --------------------------------------------------------------------------- #
# AC-1 — out-of-band load + unset -> EMPTY
# --------------------------------------------------------------------------- #


def test_loads_from_out_of_band_env_path(tmp_path, monkeypatch):
    """AC-1: a config on an out-of-tree path named by the env var loads creds + shared key."""
    cfg_file = tmp_path / "alpha.json"
    cfg_file.write_text(json.dumps({
        "shared_api_key": _SHARED_KEY,
        "vendors": {"whoop": {"client_id": _WHOOP_CLIENT_ID, "client_secret": _WHOOP_CLIENT_SECRET}},
    }))
    monkeypatch.setenv(alpha_config.ALPHA_CONFIG_ENV, str(cfg_file))

    config = alpha_config.load_alpha_config()

    assert config.shared_api_key == _SHARED_KEY
    assert config.vendors["whoop"].client_id == _WHOOP_CLIENT_ID
    assert config.vendors["whoop"].client_secret == _WHOOP_CLIENT_SECRET


def test_unset_env_var_empty_config(monkeypatch):
    """AC-1: env var unset -> an EMPTY config (0 vendor creds AND no shared key), NO exception.

    Emptiness is asserted (QA-F5): a loader that RAISED or returned a POPULATED config on the
    unset path would RED here — connect must degrade to per-vendor manual/skip, not fail.
    """
    monkeypatch.delenv(alpha_config.ALPHA_CONFIG_ENV, raising=False)

    config = alpha_config.load_alpha_config()

    assert config.vendors == {}
    assert config.shared_api_key is None


# --------------------------------------------------------------------------- #
# AC-2 — per-vendor client-type data-driven, via a SEAM
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("vendor,expected", [
    ("whoop", alpha_config.ClientType.CONFIDENTIAL),          # HARD-grounded: ≥Whoop confidential
    ("google", alpha_config.ClientType.PKCE_PUBLIC),          # OQ-5 placeholder (no secret)
    ("oura", alpha_config.ClientType.PAT),                    # grounded PAT paste fast-path
    ("garmin", alpha_config.ClientType.EXCLUDED_FROM_ONE_CLICK),  # HARD-grounded: OAuth-1.0a
])
def test_per_vendor_client_type_data_driven(vendor, expected, monkeypatch):
    """AC-2: the client-type map is DATA-DRIVEN through a seam, not a per-vendor code branch.

    The grounded default set resolves each vendor's type; EXTENDING the table via the
    `client_types` override seam resolves a synthetic vendor a hardcoded if-chain would
    ignore (-> RED); a vendor ABSENT from the map defaults to MANUAL, not a raise (AR-005).
    """
    monkeypatch.delenv(alpha_config.ALPHA_CONFIG_ENV, raising=False)
    config = alpha_config.load_alpha_config()
    assert config.client_type(vendor) == expected

    # EXTEND the table via the seam: a synthetic vendor resolves (falsifies a hardcoded map).
    extended = {**alpha_config.DEFAULT_CLIENT_TYPES, "synthvendor": alpha_config.ClientType.CONFIDENTIAL}
    seamed = alpha_config.load_alpha_config(client_types=extended)
    assert seamed.client_type("synthvendor") == alpha_config.ClientType.CONFIDENTIAL

    # A vendor NOT in the map degrades to per-vendor-manual (AR-005), never a raise.
    assert config.client_type("no-such-vendor") == alpha_config.ClientType.MANUAL


# --------------------------------------------------------------------------- #
# AC-3 — tracked-secret-scan == 0 (VALUE-shape, not the bare identifier)
# --------------------------------------------------------------------------- #

# The house VALUE-shape key pattern (tests/model/test_key_source.py:141 — 0 hits clean,
# matches a real ~100-char key) + a LABELED-context client_secret value pattern. NOT the bare
# `sk-ant-`/`client_secret` identifier (37 hits) nor a bare `{32,}` (2170 hits) — AR-002/QA-F1.
_KEY_VALUE_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")
_SECRET_VALUE_RE = re.compile(r"""client_secret['"]?\s*[:=]\s*['"]?[A-Za-z0-9/+=_-]{32,}""")


def test_no_tracked_secret():
    """AC-3: `git ls-files` scanned by a VALUE-shape secret pattern finds 0 hits (repo is PUBLIC).

    The never-git-add `tmp_path`-only fixture discipline is the PRIMARY control; this value
    scan is the backstop. Positive controls pin the regex is live (a real-length value matches,
    a short synthetic fixture does not) — so a broken always-miss scan cannot pass silently.
    """
    # Positive controls: the pattern MUST match a real-length value and NOT the short fixtures.
    assert _KEY_VALUE_RE.search("sk-ant-" + "A" * 30), "the key value-scan is broken (matches nothing)"
    assert not _KEY_VALUE_RE.search(_SHARED_KEY), "the key value-scan wrongly matches a short synthetic fixture"
    assert _SECRET_VALUE_RE.search('client_secret = "' + "a" * 40 + '"'), "the client_secret value-scan is broken"
    assert not _SECRET_VALUE_RE.search('client_secret = "%s"' % _WHOOP_CLIENT_SECRET), "the secret scan wrongly matches a short fixture"

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hits = []
    for rel in tracked:
        if not rel:
            continue
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if _KEY_VALUE_RE.search(text) or _SECRET_VALUE_RE.search(text):
            hits.append(rel)
    assert hits == [], f"a value-shape secret is in the tracked tree (PUBLIC repo): {hits}"


# --------------------------------------------------------------------------- #
# AC-4 — in-repo path rejected, CASE-FOLDED (SEC-1 APFS bypass)
# --------------------------------------------------------------------------- #


def test_in_repo_config_path_rejected(tmp_path):
    """AC-4: an in-repo config path RAISES — same-case AND case-variant — out-of-band loads.

    `Path.resolve()` does NOT case-fold on the operator's case-insensitive APFS host, so a
    lexical `is_relative_to` misses an in-tree path with a case-variant segment
    (`A-PLUS-MAXING/...`) that is physically reachable — the SEC-1 bypass. The reject
    case-folds BOTH operands (`str.casefold()` + `is_relative_to`, NOT `os.path.normcase`
    which is a POSIX no-op). It is component-wise, so a sibling sharing a prefix
    (`a-plus-maxing-evil`) is NOT falsely rejected.
    """
    same_case = REPO_ROOT / "scripts" / "serve" / "alpha_secret_fixture.conf"
    case_variant = REPO_ROOT.parent / REPO_ROOT.name.upper() / "scripts" / "serve" / "alpha_secret_fixture.conf"
    sibling = REPO_ROOT.parent / (REPO_ROOT.name + "-evil") / "alpha.json"
    oob = tmp_path / "alpha.json"
    oob.write_text(json.dumps({"vendors": {}, "shared_api_key": None}))

    # A same-case in-tree path is rejected (loaded before any read — the file need not exist).
    with pytest.raises(alpha_config.AlphaConfigError):
        alpha_config.load_alpha_config(str(same_case))
    # The APFS case-variant in-tree path is ALSO rejected (SEC-1 — this is the bypass test).
    with pytest.raises(alpha_config.AlphaConfigError):
        alpha_config.load_alpha_config(str(case_variant))

    # The reject predicate directly: case-variant IS in-repo (True); the sibling-prefix is NOT
    # (False — component-wise, no false positive); a genuine out-of-band path is NOT (False).
    assert alpha_config._within_repo(str(case_variant)) is True
    assert alpha_config._within_repo(str(sibling)) is False
    assert alpha_config._within_repo(str(oob)) is False

    # An out-of-band path loads with no reject.
    config = alpha_config.load_alpha_config(str(oob))
    assert config.shared_api_key is None


# --------------------------------------------------------------------------- #
# AC-5 — D5 provisioning bridge (LOAD-BEARING, HERMETIC, 0 clobber)
# --------------------------------------------------------------------------- #


def test_bridge_provisions_shared_key_when_no_byo(monkeypatch):
    """AC-5: no BYO key -> the bridge exports the shared key so the REAL env-first resolve finds it.

    Hermetic: env via `monkeypatch.delenv` (auto-reverted, cannot leak into the AC-7 baseline);
    the keychain tier faked empty via an injected `partial` so the env-first branch is the
    GENUINE one (the pre-bridge `KeyUnavailableError` is real, not stipulated). Crown-jewel:
    after the bridge, the same real `resolve` returns the shared key instead of raising.
    """
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    resolve = partial(key_source.resolve, keychain_runner=_empty_keychain)
    config = alpha_config.AlphaConfig(vendors={}, shared_api_key=_SHARED_KEY,
                                      client_types=alpha_config.DEFAULT_CLIENT_TYPES)

    # Precondition (genuine, not faked): with no BYO, the REAL env-first resolve raises.
    with pytest.raises(key_source.KeyUnavailableError):
        resolve()

    alpha_config.provision_shared_key(config, resolve=resolve)

    # The shared key is now resolvable via the env-first branch (no keychain write).
    assert resolve() == _SHARED_KEY
    assert os.environ[key_source.ENV_VAR] == _SHARED_KEY


def test_bridge_byo_env_precedence_no_clobber(monkeypatch):
    """AC-5: a BYO key in the env is env-first -> the bridge no-ops -> 0 clobber (env != shared)."""
    monkeypatch.setenv(key_source.ENV_VAR, _BYO_KEY)   # DISTINCT from _SHARED_KEY (QA-F3)
    resolve = partial(key_source.resolve, keychain_runner=_empty_keychain)
    config = alpha_config.AlphaConfig(vendors={}, shared_api_key=_SHARED_KEY,
                                      client_types=alpha_config.DEFAULT_CLIENT_TYPES)

    alpha_config.provision_shared_key(config, resolve=resolve)

    assert os.environ[key_source.ENV_VAR] == _BYO_KEY
    assert os.environ[key_source.ENV_VAR] != _SHARED_KEY   # vacuous unless the values are distinct
    assert resolve() == _BYO_KEY


def test_bridge_byo_keychain_precedence_no_clobber(monkeypatch):
    """AC-5: a BYO key in the keychain tier resolves -> the bridge no-ops -> 0 clobber."""
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    resolve = partial(key_source.resolve, keychain_runner=lambda: _BYO_KEY)
    config = alpha_config.AlphaConfig(vendors={}, shared_api_key=_SHARED_KEY,
                                      client_types=alpha_config.DEFAULT_CLIENT_TYPES)

    alpha_config.provision_shared_key(config, resolve=resolve)

    # The keychain BYO resolves (resolve does NOT raise) -> the bridge never exported the shared key.
    assert resolve() == _BYO_KEY
    assert os.environ.get(key_source.ENV_VAR) != _SHARED_KEY


def test_bridge_no_config_key_is_noop(monkeypatch):
    """AC-5: a config with NO shared key -> the bridge is a no-op even with no BYO key."""
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    resolve = partial(key_source.resolve, keychain_runner=_empty_keychain)
    config = alpha_config.AlphaConfig(vendors={}, shared_api_key=None,
                                      client_types=alpha_config.DEFAULT_CLIENT_TYPES)

    alpha_config.provision_shared_key(config, resolve=resolve)

    # Nothing to provision -> the env stays unset -> resolve still raises.
    assert os.environ.get(key_source.ENV_VAR) is None
    with pytest.raises(key_source.KeyUnavailableError):
        resolve()


# --------------------------------------------------------------------------- #
# AC-6 — frozen-six byte-frozen (FIXED fork-point, PF-S133-03)
# --------------------------------------------------------------------------- #

_FORK_POINT = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
_FROZEN_SIX = (
    "scripts/store/store.py",
    "scripts/store/keying.py",
    "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    "scripts/plan/router.py",
)


def test_frozen_six_numstat_empty():
    """AC-6: `git diff --numstat <FIXED fork-point> -- <the six>` prints nothing.

    Uses the FIXED `_FORK_POINT` SHA, NOT `git merge-base` — a merge-base drifts as main
    advances and silently changes what the probe forbids (PF-S133-03). Falsifiable: a
    throwaway edit to any of the six emits a numstat row (proven in an isolated worktree).
    """
    rows = subprocess.run(
        ["git", "diff", "--numstat", _FORK_POINT, "--", *_FROZEN_SIX],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen-six file changed vs the fork point: {changed}"


# --------------------------------------------------------------------------- #
# AC-8 — no secret value leaks into an exception or a log record (SEC-2)
# --------------------------------------------------------------------------- #


def test_secret_value_never_leaks(tmp_path, monkeypatch, caplog):
    """AC-8: a sentinel secret through the loader's + bridge's paths leaks into 0 exceptions/logs.

    The loader's malformed-config failure raises a CONSTANT message (no file content); the
    bridge exports the key onto `os.environ` without logging it. RED-capable: a mutation that
    string-formats the secret into an error/log record surfaces the sentinel here.
    """
    # Loader failure path: a malformed config file that CONTAINS the sentinel value.
    bad = tmp_path / "alpha.json"
    bad.write_text('{"shared_api_key": "' + _SENTINEL + '", NOT-VALID-JSON')
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(alpha_config.AlphaConfigError) as excinfo:
            alpha_config.load_alpha_config(str(bad))
    assert _SENTINEL not in str(excinfo.value), "the loader leaked the secret into its exception"

    # Bridge path: provision with the sentinel as the shared key.
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    resolve = partial(key_source.resolve, keychain_runner=_empty_keychain)
    config = alpha_config.AlphaConfig(vendors={}, shared_api_key=_SENTINEL,
                                      client_types=alpha_config.DEFAULT_CLIENT_TYPES)
    with caplog.at_level(logging.DEBUG):
        alpha_config.provision_shared_key(config, resolve=resolve)

    assert _SENTINEL not in caplog.text, "a secret value reached a log record"
