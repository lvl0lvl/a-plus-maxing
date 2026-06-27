"""Unit tests for key_source.store — the in-app keychain WRITE path (Profile screen).

store() writes the no-train API key into the same `a-plus-maxing-api-key` keychain item
resolve() reads, via an injectable writer seam so no real keychain or key is touched.
Crown-jewel constraint (NFR-3, the repo is PUBLIC): the key value never lands in a log, a
returned value, or an exception message; an empty key is rejected before any write. The
fixture key is synthetic.
"""

import pytest

from scripts.model import key_source

# A non-secret fixture that is deliberately NOT shaped like a real key (no `sk-ant-…`
# prefix) so the NFR-3 tracked-tree key-literal scan stays comprehensive over test files.
_SYNTHETIC_KEY = "synthetic-test-key-store-fixture"


def test_store_passes_stripped_key_to_writer():
    """store() hands the stripped key to the injected keychain writer exactly once."""
    seen = []
    key_source.store("  " + _SYNTHETIC_KEY + "  ", keychain_writer=seen.append)
    assert seen == [_SYNTHETIC_KEY]


def test_store_rejects_empty_key_without_writing():
    """An empty/blank/None key raises ValueError and the writer is never called."""
    seen = []
    for blank in ("", "   ", None):
        with pytest.raises(ValueError):
            key_source.store(blank, keychain_writer=seen.append)
    assert seen == []


def test_store_error_message_never_carries_the_key():
    """A write failure surfaces with a constant message that does not leak the key value."""
    def boom(_key):
        raise key_source.KeyStoreError("Could not store the key in the macOS keychain.")

    with pytest.raises(key_source.KeyStoreError) as exc:
        key_source.store(_SYNTHETIC_KEY, keychain_writer=boom)
    assert _SYNTHETIC_KEY not in str(exc.value)


def test_keychain_writer_invokes_security_add_and_fails_loud_on_nonzero(monkeypatch):
    """_keychain_writer runs `security add-generic-password -U ... -w <key>`; nonzero raises."""
    calls = {}

    class _Ok:
        returncode = 0

    def fake_run(argv, **_kw):
        calls["argv"] = argv
        return _Ok()

    monkeypatch.setattr(key_source.subprocess, "run", fake_run)
    key_source._keychain_writer(_SYNTHETIC_KEY)
    argv = calls["argv"]
    assert argv[:3] == ["security", "add-generic-password", "-U"]
    assert "-s" in argv and key_source._KEYCHAIN_SERVICE in argv
    assert argv[-2:] == ["-w", _SYNTHETIC_KEY]  # the key is the -w value, not logged

    class _Fail:
        returncode = 1

    monkeypatch.setattr(key_source.subprocess, "run", lambda *_a, **_k: _Fail())
    with pytest.raises(key_source.KeyStoreError):
        key_source._keychain_writer(_SYNTHETIC_KEY)
