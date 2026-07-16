"""Unit tests for key_source.store — the in-app keychain WRITE path (Profile screen).

store() writes the no-train API key into the same `a-plus-maxing-api-key` keychain item
resolve() reads, via an injectable writer seam so no real keychain or key is touched.
Crown-jewel constraint (NFR-3, the repo is PUBLIC): the key value never lands in a log, a
returned value, or an exception message; an empty key is rejected before any write. The
fixture key is synthetic.
"""

import pytest

from scripts import secret_store
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


def test_default_writer_delegates_to_secret_store_set_secret(monkeypatch):
    """SF-4a/AC-1: the DEFAULT keychain_writer delegates to secret_store.set_secret (exact service+key).

    Migrated from the removed `security add-generic-password` ARGV test — the direct shell-out is gone,
    so the writer's contract is now delegation to the abstraction. SF-1 service-keyed: the exact
    `a-plus-maxing-api-key` service is asserted so a transposition reds.
    """
    seen = {}

    def _spy_set(service, value):
        seen["service"] = service
        seen["value"] = value

    monkeypatch.setattr(secret_store, "set_secret", _spy_set)
    key_source._keychain_writer(_SYNTHETIC_KEY)
    assert seen == {"service": "a-plus-maxing-api-key", "value": _SYNTHETIC_KEY}


def test_store_default_writer_translates_error_class(monkeypatch):
    """AC-8/F2: the DEFAULT writer translates secret_store.KeyStoreError -> key_source.KeyStoreError.

    server.py:976 catches key_source.KeyStoreError; the sibling secret_store.KeyStoreError is NOT a
    subclass, so a naive delegate that let it escape would leave a /settings/key write failure uncaught
    (a production regression). Drives the DEFAULT writer (not an injected fake — the factory-bypass
    mandate). RED-capable: a default that propagates secret_store.KeyStoreError -> pytest.raises reds.
    The message is CONSTANT and carries no key value.
    """
    def _boom(service, value):
        raise secret_store.KeyStoreError("secret-store write failed")

    monkeypatch.setattr(secret_store, "set_secret", _boom)
    with pytest.raises(key_source.KeyStoreError) as exc:
        key_source.store(_SYNTHETIC_KEY)
    assert _SYNTHETIC_KEY not in str(exc.value)
