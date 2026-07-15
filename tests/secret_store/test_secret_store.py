"""Tests for scripts.secret_store — the cross-platform secret-store abstraction.

$0 mock build (ADR-0047-T1): the per-OS keyring backends are SYNTHETIC injected fakes
(no live keychain, no live socket). Every fixture value is synthetic (no real secret /
PII). The fallback file is only ever written to a `tmp_path` via the injected
fallback-path seam — never the real in-tree instance-local default.
"""

import json
import logging
import os
import re
import stat
import subprocess
import traceback
from inspect import signature
from pathlib import Path

import pytest
from keyring.errors import KeyringLocked, PasswordDeleteError

from scripts import secret_store
from scripts.secret_store import KeyStoreError, delete_secret, get_secret, set_secret

_REPO_ROOT = Path(__file__).resolve().parents[2]

# Three NAMED, distinct OS-native backend fakes (AC-1 / F-I: three identifiable fakes,
# not one seam standing in for three).
_OS_BACKEND_NAMES = [
    "macOS Keychain",
    "Windows Credential Manager",
    "Linux Secret Service",
]


class _OSKeyringFake:
    """An AVAILABLE OS-native keyring fake: stores (service, username) -> value in a dict.

    Mirrors real keyring semantics: `get_password` returns None on a miss (an available
    miss — no raise); `delete_password` of an absent item raises PasswordDeleteError (the
    available-but-absent signal the module treats as idempotent). `interactive=True`
    simulates a backend that prompts on each access, driving the prompt spy > 0 (the AC-2
    RED-capability witness).
    """

    def __init__(self, name, interactive=False):
        self.name = name
        self._store = {}
        self.prompts = 0
        self._interactive = interactive

    def _note_prompt(self):
        if self._interactive:
            self.prompts += 1

    def get_password(self, service, username):
        self._note_prompt()
        return self._store.get((service, username))

    def set_password(self, service, username, value):
        self._note_prompt()
        self._store[(service, username)] = value

    def delete_password(self, service, username):
        self._note_prompt()
        if (service, username) not in self._store:
            raise PasswordDeleteError("not found")
        del self._store[(service, username)]


class _RaisingBackend:
    """A SYMMETRICALLY-unavailable keyring fake: raises KeyringLocked on get/set/delete.

    Models a locked/prompting/blocking backend. Unavailability is symmetric (it raises on
    BOTH get and set), and the delete raise is an unavailability class (KeyringLocked, a
    KeyringError that is NOT a PasswordDeleteError) so the module surfaces it fail-loud
    (AC-16), distinct from the available-but-absent idempotent case.
    """

    def get_password(self, service, username):
        raise KeyringLocked("locked")

    def set_password(self, service, username, value):
        raise KeyringLocked("locked")

    def delete_password(self, service, username):
        raise KeyringLocked("locked")


def _read_fb(path):
    """Read the on-disk fallback JSON directly (test-side inspection of residue)."""
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else {}


def _install_fallback_spy(monkeypatch):
    """Count every fallback-tier read (the fallback-seam spy). Returns the counter."""
    counter = {"n": 0}
    real = secret_store._fallback_lookup

    def spy(path, service):
        counter["n"] += 1
        return real(path, service)

    monkeypatch.setattr(secret_store, "_fallback_lookup", spy)
    return counter


def _raise_io(*args, **kwargs):
    raise OSError("simulated fallback write failure")


def _norm_doc():
    """The module docstring, lowercased with runs of whitespace collapsed to one space.

    Docstring assertions match on wording, not on incidental line wrapping.
    """
    return re.sub(r"\s+", " ", (secret_store.__doc__ or "").lower())


# ------------------------------ Cycle 1: the abstraction ------------------------------


@pytest.mark.parametrize("backend_name", _OS_BACKEND_NAMES)
def test_roundtrip_per_os_backend(tmp_path, backend_name):
    """AC-1: set->get recovers the value byte-for-byte on each named OS backend."""
    backend = _OSKeyringFake(backend_name)
    fp = tmp_path / "fb.json"
    set_secret("api", "sk-test-AA00/byte+exact=value", backend=backend, fallback_path=fp)
    assert get_secret("api", backend=backend, fallback_path=fp) == "sk-test-AA00/byte+exact=value"


@pytest.mark.parametrize("backend_name", _OS_BACKEND_NAMES)
def test_unattended_roundtrip_zero_prompts(tmp_path, backend_name):
    """AC-2: an unattended round-trip completes with the prompt spy at 0, per backend."""
    backend = _OSKeyringFake(backend_name)
    fp = tmp_path / "fb.json"
    set_secret("api", "unattended-value", backend=backend, fallback_path=fp)
    assert get_secret("api", backend=backend, fallback_path=fp) == "unattended-value"
    assert backend.prompts == 0


def test_raising_backend_routes_to_fallback(tmp_path):
    """AC-8: symmetric unavailability routes set to the fallback and get recovers it."""
    fp = tmp_path / "fb.json"
    backend = _RaisingBackend()
    set_secret("svc", "recover-me", backend=backend, fallback_path=fp)
    assert _read_fb(fp).get("svc") == "recover-me"
    assert get_secret("svc", backend=backend, fallback_path=fp) == "recover-me"


def test_fallback_engages_iff_keyring_unavailable(tmp_path, monkeypatch):
    """AC-3: 0 fallback reads when keyring available+present; fallback serves when down."""
    fp = tmp_path / "fb.json"
    backend = _OSKeyringFake("macOS Keychain")
    set_secret("svc", "keyring-value", backend=backend, fallback_path=fp)
    # Seed a DIFFERENT fallback value so an erroneous fallback read would be observable.
    secret_store._fallback_write(fp, "svc", "FALLBACK_SHOULD_NOT_BE_READ")

    counter = _install_fallback_spy(monkeypatch)
    assert get_secret("svc", backend=backend, fallback_path=fp) == "keyring-value"
    assert counter["n"] == 0  # keyring available+present -> 0 fallback reads

    counter["n"] = 0
    assert (
        get_secret("svc", backend=_RaisingBackend(), fallback_path=fp)
        == "FALLBACK_SHOULD_NOT_BE_READ"
    )
    assert counter["n"] >= 1  # symmetric unavailability -> fallback serves


def test_available_miss_no_fallback_resurrection(tmp_path, monkeypatch):
    """AC-9: an available keyring that MISSES returns None with 0 fallback reads."""
    fp = tmp_path / "fb.json"
    backend = _OSKeyringFake("Linux Secret Service")  # available, but secret absent
    secret_store._fallback_write(fp, "svc", "STALE_SHOULD_NOT_RESURRECT")

    counter = _install_fallback_spy(monkeypatch)
    assert get_secret("svc", backend=backend, fallback_path=fp) is None
    assert counter["n"] == 0  # no stale-fallback resurrection on an available miss


def test_delete_secret(tmp_path):
    """AC-10: delete clears BOTH tiers; delete-when-absent is idempotent (no error)."""
    fp = tmp_path / "fb.json"
    backend = _OSKeyringFake("Windows Credential Manager")
    set_secret("svc", "v", backend=backend, fallback_path=fp)
    delete_secret("svc", backend=backend, fallback_path=fp)
    assert get_secret("svc", backend=backend, fallback_path=fp) is None
    # Idempotent: delete-when-absent raises nothing (PasswordDeleteError swallowed).
    delete_secret("svc", backend=backend, fallback_path=fp)
    # Clears the FALLBACK tier too: seed a residue via an outage, available-delete clears it.
    set_secret("svc2", "resid", backend=_RaisingBackend(), fallback_path=fp)
    assert _read_fb(fp).get("svc2") == "resid"
    delete_secret("svc2", backend=backend, fallback_path=fp)
    assert "svc2" not in _read_fb(fp)
    assert get_secret("svc2", backend=_RaisingBackend(), fallback_path=fp) is None


def test_no_homegrown_crypto_honest_transform():
    """AC-11: the docstring is honest (permission-gated, not encrypted) + no crypto dep."""
    doc = _norm_doc()
    assert "permission" in doc  # owner-only permission-gated
    assert "not cryptographically encrypted" in doc  # honest disclaimer
    assert "env" in doc  # env-var-extractable
    assert "encrypted at rest" not in doc  # no bare unqualified strength claim

    reqs_raw = (_REPO_ROOT / "requirements.txt").read_text()
    crypto = {
        "cryptography", "pycrypto", "pycryptodome", "pynacl", "nacl",
        "fernet", "cryptodome", "rsa", "pyaes", "pyca",
    }
    for line in reqs_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[><=!~ ]", line)[0].strip().lower()
        assert name not in crypto, f"unexpected crypto dependency in manifest: {name}"


def test_secret_value_never_leaks(tmp_path, monkeypatch, caplog):
    """AC-12: a forced failure leaks the secret into 0 logs + 0 str(exc)/traceback."""
    sentinel = "SENTINEL_LEAK_CANARY_9f3a2b"
    monkeypatch.setattr(secret_store, "_write_fallback_file", _raise_io)
    caplog.set_level(logging.DEBUG)
    with pytest.raises(KeyStoreError) as excinfo:
        set_secret("svc", sentinel, backend=_RaisingBackend(), fallback_path=tmp_path / "fb.json")
    assert sentinel not in str(excinfo.value)
    assert sentinel not in "".join(traceback.format_exception(excinfo.value))
    for record in caplog.records:
        assert sentinel not in record.getMessage()
        assert sentinel not in str(record.args or "")


def test_total_failure_fails_loud(tmp_path, monkeypatch):
    """AC-12: keyring unavailable AND fallback write fails -> KeyStoreError fail-loud."""
    monkeypatch.setattr(secret_store, "_write_fallback_file", _raise_io)
    with pytest.raises(KeyStoreError):
        set_secret("svc", "v", backend=_RaisingBackend(), fallback_path=tmp_path / "fb.json")


def test_fallback_file_mode_0600(tmp_path, monkeypatch):
    """AC-13: the fallback file is created ATOMICALLY with mode 0600 (no chmod window)."""
    fp = tmp_path / "fb.json"
    created_modes = []
    real_os_open = os.open

    def spy_open(path, flags, mode=0o777, **kwargs):
        if os.fspath(path) == os.fspath(fp):
            created_modes.append(mode)
        return real_os_open(path, flags, mode, **kwargs)

    monkeypatch.setattr(os, "open", spy_open)
    old_umask = os.umask(0)  # most permissive -> a plain open('w') would show group/world bits
    try:
        set_secret("svc", "v", backend=_RaisingBackend(), fallback_path=fp)
    finally:
        os.umask(old_umask)

    assert fp.exists()
    mode = stat.S_IMODE(os.stat(fp).st_mode)
    assert mode == 0o600, f"expected 0600, got {oct(mode)}"
    assert not (mode & 0o077), "group/world bits are set on the fallback file"
    # At-creation proof: the file was created via os.open with mode 0o600, not open('w')+chmod.
    assert 0o600 in created_modes, "fallback file not created atomically with mode 0600"


def test_fallback_env_var_fixed_prefix(tmp_path, monkeypatch):
    """AC-14: the env fallback uses a FIXED-PREFIX key, never a raw service passthrough."""
    fp = tmp_path / "empty.json"  # absent -> file tier empty, so the env branch is reached
    env_key = f"{secret_store._FALLBACK_ENV_PREFIX}_PATH"
    monkeypatch.delenv(env_key, raising=False)
    assert os.environ.get("PATH")  # a real env var named exactly like the service

    # A raw os.environ[service] passthrough would return the real PATH; it must not.
    result = get_secret("PATH", backend=_RaisingBackend(), fallback_path=fp)
    assert result != os.environ["PATH"]
    assert result is None  # no fixed-prefix env set -> None

    monkeypatch.setenv(env_key, "injected-fallback-secret")
    assert (
        get_secret("PATH", backend=_RaisingBackend(), fallback_path=fp)
        == "injected-fallback-secret"
    )


def test_fallback_write_through_clear(tmp_path):
    """AC-15: a keyring-available set/delete clears stale fallback FILE residue (SEC-04)."""
    fp = tmp_path / "fb.json"
    raising = _RaisingBackend()
    available = _OSKeyringFake("macOS Keychain")

    # (1) outage: set v1 -> fallback file
    set_secret("svc", "v1", backend=raising, fallback_path=fp)
    assert _read_fb(fp).get("svc") == "v1"
    # (2) recover: available set v2 -> keyring AND clears the v1 residue
    set_secret("svc", "v2", backend=available, fallback_path=fp)
    assert "svc" not in _read_fb(fp)
    # (3) later outage: get reads the fallback, finds no v1 -> None (never stale v1)
    assert get_secret("svc", backend=raising, fallback_path=fp) is None

    # A keyring-available DELETE likewise clears fallback residue.
    set_secret("svc3", "resid", backend=raising, fallback_path=fp)
    assert _read_fb(fp).get("svc3") == "resid"
    delete_secret("svc3", backend=available, fallback_path=fp)
    assert "svc3" not in _read_fb(fp)


def test_delete_raising_backend_fail_loud(tmp_path):
    """AC-16: delete under symmetric unavailability clears fallback THEN raises fail-loud."""
    fp = tmp_path / "fb.json"
    raising = _RaisingBackend()
    set_secret("svc", "residue", backend=raising, fallback_path=fp)
    assert _read_fb(fp).get("svc") == "residue"

    with pytest.raises(KeyStoreError):
        delete_secret("svc", backend=raising, fallback_path=fp)

    # The fallback residue is cleared UNCONDITIONALLY despite the surfaced keyring failure.
    assert "svc" not in _read_fb(fp)
    assert get_secret("svc", backend=raising, fallback_path=fp) is None


def test_keyring_declared():
    """AC-4: keyring is declared in the requirements manifest (first third-party dep)."""
    reqs = (_REPO_ROOT / "requirements.txt").read_text()
    assert "keyring" in reqs


# ---------------------- Cycle 2: at-rest placement + frozen-six ----------------------


def test_fallback_file_gitignored():
    """AC-5: the module-sourced fallback path is gitignored, in-tree, outside scripts/store/."""
    default_path = secret_store._FALLBACK_PATH
    # The injectable seam DEFAULT equals the module constant (the path set_secret writes),
    # so the path checked here is the one the un-injected module actually writes to.
    for fn in (get_secret, set_secret, delete_secret):
        assert signature(fn).parameters["fallback_path"].default == default_path
    # In-tree: an out-of-tree default would make `git check-ignore` FATAL-128 (F1).
    assert default_path.is_relative_to(_REPO_ROOT)
    assert "scripts/store" not in default_path.as_posix()  # outside the frozen-six store dir
    rel = default_path.relative_to(_REPO_ROOT)

    checked = subprocess.run(
        ["git", "check-ignore", str(rel)], cwd=_REPO_ROOT, capture_output=True, text=True
    )
    assert checked.returncode == 0, f"fallback path not gitignored: {rel} (rc={checked.returncode})"

    listed = subprocess.run(
        ["git", "ls-files", str(rel)], cwd=_REPO_ROOT, capture_output=True, text=True
    )
    assert listed.stdout.strip() == "", f"fallback file is tracked: {listed.stdout}"


def test_docstring_documents_fallback_threat_model():
    """AC-5: the docstring documents the complete fallback threat model (OQ-2 / SEC-06)."""
    doc = _norm_doc()
    assert "keyring" in doc and ("prefer" in doc or "primary" in doc)  # keyring preferred
    assert "unavailable" in doc  # fallback engages only when keyring is unavailable
    assert "extract" in doc and "weaker" in doc  # env-var extractability -> weaker at rest
    assert "disk" in doc or "backup" in doc  # positive threat model (stolen disk-image/backup)
    assert "prompt" in doc and "downgrade" in doc  # prompt-induced downgrade note
    assert "git" in doc  # public-repo gitignored-working-tree threat (git add -f / gitignored)
    assert "hook" in doc  # block-pii-commit / pre-push-pii-scan backstop


def test_frozen_six_numstat_empty():
    """AC-6: the ADR-0032 frozen-six stay byte-frozen vs the FIXED fork-point (PF-S133-03)."""
    fork_point = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
    six = [
        "scripts/store/store.py",
        "scripts/store/keying.py",
        "scripts/plan/pipeline.py",
        "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py",
        "scripts/plan/router.py",
    ]
    result = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", *six],
        cwd=_REPO_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "", f"frozen-six changed:\n{result.stdout}"
