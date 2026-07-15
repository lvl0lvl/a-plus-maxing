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


class _RecordingAvailableBackend(_OSKeyringFake):
    """An AVAILABLE OS fake that records whether delete_password was invoked (FIX-1b)."""

    def __init__(self, name="Recording Backend"):
        super().__init__(name)
        self.delete_called = False

    def delete_password(self, service, username):
        self.delete_called = True
        return super().delete_password(service, username)


class _WriteFailingHandle:
    """Proxy over a real file handle whose `.write` raises — simulates a torn write (FIX-2).

    Everything but `write` (fileno / flush / context-manager close) delegates to the real
    handle, so the atomic writer opens + fchmods the temp normally, then fails on the payload
    write; the `with` block's exit still closes the real fd.
    """

    def __init__(self, real):
        self._real = real

    def write(self, *args, **kwargs):
        raise OSError("simulated torn write (ENOSPC)")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return self._real.__exit__(*exc)

    def __getattr__(self, name):
        return getattr(self._real, name)


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
    """AC-13: the fallback file is created ATOMICALLY at mode 0600 (no world-readable window).

    The atomic writer stages the payload in a temp sibling created via tempfile.mkstemp (which
    opens at mode 0600) and os.replaces it into place, so the fallback file is never
    group/world-readable at the process umask — there is no open('w')-then-chmod window.
    Reconciled for FIX-2: the at-creation proof now inspects the atomic temp sibling's open
    mode rather than an os.open on the final path (mkstemp opens the temp, then os.replace).
    """
    fp = tmp_path / "fb.json"
    created_modes = []
    real_os_open = os.open

    def spy_open(path, flags, mode=0o777, **kwargs):
        # Record the creation mode of the atomic temp sibling(s) staged for this fallback file.
        if os.path.basename(os.fspath(path)).startswith(fp.name):
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
    # At-creation proof: every temp sibling was opened at mode 0600, never world-readable.
    assert created_modes, "no atomic temp sibling was created for the fallback file"
    assert all(m == 0o600 for m in created_modes), f"temp created world-readable: {created_modes}"


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


# ------------- Tier-2 review hardening: corrupt-file + symlink + prompt-spy -------------


def test_corrupt_fallback_file_set_on_available_keyring(tmp_path):
    """LOW-2: a corrupt fallback file must not brick set on an AVAILABLE keyring.

    set_secret's write-through-clear reads the fallback file OUTSIDE any guard; a corrupt
    file would raise JSONDecodeError out of the public API even though the keyring write
    already succeeded. A corrupt fallback is treated as empty, so the set completes.
    """
    fp = tmp_path / "fb.json"
    fp.write_text("{ this is not valid json ::::")  # corrupt/hostile fallback file
    backend = _OSKeyringFake("macOS Keychain")  # available keyring
    set_secret("svc", "v", backend=backend, fallback_path=fp)  # must not raise
    assert get_secret("svc", backend=backend, fallback_path=fp) == "v"


def test_corrupt_fallback_file_get_under_outage(tmp_path, monkeypatch):
    """LOW-2: get under keyring outage returns None on a corrupt fallback file (no raise).

    A corrupt file must be treated as empty (-> None), never surface JSONDecodeError —
    whose .doc attribute carries the raw file bytes — out of the public API.
    """
    fp = tmp_path / "fb.json"
    fp.write_text("}{ not json")
    monkeypatch.delenv(f"{secret_store._FALLBACK_ENV_PREFIX}_SVC", raising=False)
    assert get_secret("svc", backend=_RaisingBackend(), fallback_path=fp) is None


def test_fallback_file_mode_reasserted_on_rewrite(tmp_path):
    """LOW-1: a rewrite over a pre-existing looser-mode fallback file yields mode 0600.

    The atomic writer replaces the target with a fresh temp inode created at mode 0600 (and
    fchmod'd 0600 for parity), so a pre-existing 0644 file's mode does not survive the rewrite —
    the result is owner-only 0600 regardless of the prior mode.
    """
    fp = tmp_path / "fb.json"
    fp.write_text("{}")
    os.chmod(fp, 0o644)
    assert stat.S_IMODE(os.stat(fp).st_mode) == 0o644  # precondition: looser mode
    set_secret("svc", "v", backend=_RaisingBackend(), fallback_path=fp)
    assert stat.S_IMODE(os.stat(fp).st_mode) == 0o600


def test_fallback_symlink_not_followed(tmp_path):
    """LOW-1: a symlink at the fallback path never has the secret written through it.

    The atomic writer stages the secret in a fresh temp inode and os.replaces it over the
    fallback path, so a symlink pre-placed there is REMOVED and replaced by a regular owner-only
    file — its target is never written through. (The prior in-place O_NOFOLLOW open instead
    REJECTED the symlink with a raise; the atomic rewrite replaces it, but the same
    no-write-through-symlink security property holds — reconciled for the FIX-2 atomic write.)
    """
    target = tmp_path / "attacker_target.json"
    target.write_text("ORIGINAL_UNTOUCHED")
    link = tmp_path / "fb.json"
    link.symlink_to(target)

    set_secret("svc", "secret-value", backend=_RaisingBackend(), fallback_path=link)

    # The symlink target is NEVER written through: its original content is intact.
    assert target.read_text() == "ORIGINAL_UNTOUCHED"
    # The fallback path is now a REGULAR owner-only 0600 file (the symlink was replaced).
    assert not link.is_symlink()
    assert stat.S_IMODE(os.stat(link).st_mode) == 0o600
    # The secret round-trips from the fresh inode (written to the temp, not the target).
    assert get_secret("svc", backend=_RaisingBackend(), fallback_path=link) == "secret-value"


def test_prompt_spy_counts_on_interactive_backend(tmp_path):
    """QA-1: the AC-2 prompt spy actually counts — an interactive backend drives prompts>0.

    AC-2 asserts `prompts == 0` with a NON-interactive fake, which is vacuously true. This
    exercises the interactive path (previously dead code) so the spy's RED-capability is
    witnessed: a backend that prompts moves the counter, proving AC-2's 0-assertion tests
    real module behavior rather than an inert spy.
    """
    backend = _OSKeyringFake("macOS Keychain", interactive=True)
    fp = tmp_path / "fb.json"
    set_secret("api", "v", backend=backend, fallback_path=fp)
    get_secret("api", backend=backend, fallback_path=fp)
    assert backend.prompts > 0


# --------------- Tier-3 fix cycle: fallback-tier robustness cluster (PR #352) ---------------


def test_set_available_clear_failure_fails_loud(tmp_path, monkeypatch):
    """FIX-1a: an available-keyring set whose stale-residue clear fails is fail-loud.

    set_secret clears stale fallback residue after a successful keyring write (SEC-04). Pre-fix
    that clear ran OUTSIDE any guard, so a clear-write failure escaped as a raw OSError. The fix
    guards it: the failure surfaces as a constant-message KeyStoreError (never a raw OSError,
    never the secret) and is NOT swallowed — a swallowed clear would silently leave stale
    residue a later outage get_secret could serve.
    """
    fp = tmp_path / "fb.json"
    available = _OSKeyringFake("macOS Keychain")
    secret_store._fallback_write(fp, "svc", "STALE_RESIDUE")  # pre-existing residue
    monkeypatch.setattr(secret_store, "_write_fallback_file", _raise_io)  # clear's write fails

    with pytest.raises(KeyStoreError) as excinfo:
        set_secret("svc", "fresh-secret-value", backend=available, fallback_path=fp)
    assert not isinstance(excinfo.value, OSError)  # not the raw OSError
    assert "fresh-secret-value" not in str(excinfo.value)  # constant message, no secret leak


def test_delete_fallback_clear_failure_still_deletes_keyring(tmp_path, monkeypatch):
    """FIX-1b: a delete whose fallback clear fails STILL attempts the keyring delete, fail-loud.

    Pre-fix delete_secret cleared the fallback FIRST, unconditionally; a clear failure raised a
    raw OSError before backend.delete_password was ever called, so the keyring credential
    survived the delete. The fix attempts BOTH tiers regardless of a single-tier failure, then
    surfaces a constant-message KeyStoreError (never a raw OSError) if either tier failed.
    """
    fp = tmp_path / "fb.json"
    backend = _RecordingAvailableBackend()
    secret_store._fallback_write(fp, "svc", "residue")  # pre-existing residue
    monkeypatch.setattr(secret_store, "_write_fallback_file", _raise_io)  # clear's write fails

    with pytest.raises(KeyStoreError) as excinfo:
        delete_secret("svc", backend=backend, fallback_path=fp)
    assert not isinstance(excinfo.value, OSError)  # not the raw OSError
    assert backend.delete_called, "keyring delete was skipped by a fallback-clear failure"


def test_atomic_write_preserves_siblings_on_torn_write(tmp_path, monkeypatch):
    """FIX-2: a torn fallback write leaves prior sibling secrets intact (atomic temp + replace).

    The pre-fix in-place O_TRUNC writer truncates the live file at open; a write that then fails
    (ENOSPC / crash) empties it, permanently losing every sibling secret on the next
    read-modify-rewrite. The atomic writer stages the payload in a fresh temp sibling and
    os.replaces it, so a failed write leaves the live file's prior content byte-intact.
    """
    fp = tmp_path / "fb.json"
    set_secret("alpha", "a", backend=_RaisingBackend(), fallback_path=fp)  # seed sibling 1
    set_secret("beta", "b", backend=_RaisingBackend(), fallback_path=fp)   # seed sibling 2
    assert _read_fb(fp) == {"alpha": "a", "beta": "b"}

    real_fdopen = os.fdopen

    def torn_fdopen(fd, *a, **k):
        return _WriteFailingHandle(real_fdopen(fd, *a, **k))

    monkeypatch.setattr(os, "fdopen", torn_fdopen)  # the payload write tears mid-way
    with pytest.raises(KeyStoreError):
        set_secret("gamma", "g", backend=_RaisingBackend(), fallback_path=fp)

    # Atomic: the live file still holds alpha+beta; the pre-fix writer would have emptied it.
    raw = fp.read_text()
    survived = json.loads(raw) if raw.strip() else {}
    assert survived == {"alpha": "a", "beta": "b"}


@pytest.mark.parametrize("blob", ["[1, 2, 3]", "42", "null", '"x"'])
def test_non_dict_fallback_file_treated_as_empty(tmp_path, monkeypatch, blob):
    """FIX-3: a valid-JSON non-dict fallback file is treated as empty, never raising out the API.

    json.loads on [1,2,3] / 42 / null / "x" yields a non-dict; the pre-fix .get()/in/[svc]=
    then raise a raw AttributeError/TypeError out of the public API (the corrupt-file guard
    catches only unparseable/OSError). A non-dict file is treated as empty: get returns None
    and set overwrites it and round-trips.
    """
    fp = tmp_path / "fb.json"
    fp.write_text(blob)
    monkeypatch.delenv(f"{secret_store._FALLBACK_ENV_PREFIX}_SVC", raising=False)

    assert get_secret("svc", backend=_RaisingBackend(), fallback_path=fp) is None
    set_secret("svc", "v", backend=_RaisingBackend(), fallback_path=fp)
    assert get_secret("svc", backend=_RaisingBackend(), fallback_path=fp) == "v"
    assert _read_fb(fp) == {"svc": "v"}
