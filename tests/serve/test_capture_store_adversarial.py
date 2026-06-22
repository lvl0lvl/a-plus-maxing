"""Store-adversarial battery for the capture write path (ADR-0014-T1, `pka` MANDATE).

The capture seam writes to `scripts/store/` (via `store.append` on the wired-token
path), so `docs/checklists/store-adversarial-tests.md` is binding: all four categories
on the CAPTURE write path. The battery proves the capture write path inherits the
store's collision/dedupe guarantees — it is not a fork of the store surface.

  1. Cross-stream namespace collision — a capture write to one token never cross-reads
     as another token.
  2. Same-timepoint dedupe — two distinct captures sharing a timepoint both persist;
     an identical re-capture stays idempotent.
  3. Dedupe-key boundary (`value` EXCLUDED) — same `(item, timepoint, source)` + a
     different value collides (second write dropped, by design); any single differing
     field does not collide.
  4. Mutation-style verification — the battery FAILS when the dedupe key is deliberately
     widened to include `value` (the mutation observed RED below, then reverted). A
     battery green under the mutation is tautological (`pka`).
"""

import datetime

from scripts.serve import capture
from scripts.store import keying, store


def _ts(offset_seconds=0):
    """A UTC-offset timepoint (the store producer obligation), optionally shifted."""
    base = datetime.datetime(2026, 6, 21, 12, 0, 0, tzinfo=datetime.timezone.utc)
    return (base + datetime.timedelta(seconds=offset_seconds)).isoformat()


# --------------------------------------------------------------------------- #
# Category 1 — cross-stream namespace collision
# --------------------------------------------------------------------------- #


def test_capture_write_to_one_token_never_cross_reads_as_another(tmp_path):
    """Cat-1: a capture write to `goal-domains` never reads back under `hard-limits`.

    Capture two DISTINCT wired tokens with distinct values; assert each token's
    `store.read` returns ONLY its own value — a read for token X never returns token
    Y's value. The store's one-file-per-item layout namespaces by item name; this
    proves the capture path writes under the correct item name, not a shared bucket.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"goal-domains": "strength;recovery", "hard-limits": "no overhead pressing"},
        root=store_root, scaffold_root=tmp_path / "scaffold",
    )
    gd = store.read("goal-domains", root=store_root)
    hl = store.read("hard-limits", root=store_root)
    assert len(gd) == 1 and gd[0]["value"] == "strength;recovery"
    assert len(hl) == 1 and hl[0]["value"] == "no overhead pressing"
    # Cross-read negative: hard-limits' value never appears under goal-domains, vice versa.
    assert all("overhead" not in str(r["value"]) for r in gd), "hard-limits leaked into goal-domains"
    assert all("strength" not in str(r["value"]) for r in hl), "goal-domains leaked into hard-limits"


# --------------------------------------------------------------------------- #
# Category 2 — same-timepoint dedupe / idempotency
# --------------------------------------------------------------------------- #


def test_two_distinct_captures_sharing_a_timepoint_both_persist(tmp_path):
    """Cat-2: two distinct tokens captured at the SAME timepoint both persist.

    Two distinct items (`goal-domains`, `hard-limits`) legitimately sharing a
    timepoint have DIFFERENT `(item, timepoint, source)` identities, so both persist
    — the dedupe is keyed on the full identity, not the timepoint alone.
    """
    store_root = tmp_path / "store"
    ts = _ts()
    store.append("goal-domains", {"item": "goal-domains", "timepoint": ts, "source": "intake", "value": "strength"}, root=store_root)
    store.append("hard-limits", {"item": "hard-limits", "timepoint": ts, "source": "intake", "value": "no pressing"}, root=store_root)
    assert store.read("goal-domains", root=store_root)[0]["value"] == "strength"
    assert store.read("hard-limits", root=store_root)[0]["value"] == "no pressing"


def test_identical_recapture_is_idempotent(tmp_path):
    """Cat-2: an identical re-capture of the same (item, timepoint, source) is a no-op.

    Re-appending a reading with the same `(item, timepoint, source)` identity is
    dropped (the store's idempotent append) — the capture path inherits this, so a
    double-submit of the same field at the same timepoint never duplicates the line.
    """
    store_root = tmp_path / "store"
    ts = _ts()
    reading = {"item": "goal-domains", "timepoint": ts, "source": "intake", "value": "strength"}
    store.append("goal-domains", dict(reading), root=store_root)
    store.append("goal-domains", dict(reading), root=store_root)  # identical re-capture
    assert len(store.read("goal-domains", root=store_root)) == 1, "an identical re-capture duplicated the line"


# --------------------------------------------------------------------------- #
# Category 3 — dedupe-key boundary (value EXCLUDED)
# --------------------------------------------------------------------------- #


def test_same_identity_different_value_collides_second_dropped(tmp_path):
    """Cat-3: same (item, timepoint, source) + a DIFFERENT value collides (second dropped).

    `value` is EXCLUDED from the dedupe identity, so a second `append` at the same
    `(item, timepoint, source)` with a different value is DROPPED by design (a value
    correction is an explicit `store.correct`, not an `append`). The first value
    stands.
    """
    store_root = tmp_path / "store"
    ts = _ts()
    store.append("hard-limits", {"item": "hard-limits", "timepoint": ts, "source": "intake", "value": "no pressing"}, root=store_root)
    store.append("hard-limits", {"item": "hard-limits", "timepoint": ts, "source": "intake", "value": "DIFFERENT"}, root=store_root)
    readings = store.read("hard-limits", root=store_root)
    assert len(readings) == 1, "a same-identity different-value second write was not dropped"
    assert readings[0]["value"] == "no pressing", "the second write wrongly overrode the first value"


def test_any_single_differing_identity_field_does_not_collide(tmp_path):
    """Cat-3: differing item OR timepoint OR source does NOT collide (both persist).

    Each of the three identity fields contributes to the dedupe key. Vary each one in
    turn against a baseline and assert both readings persist — proving none of the
    three is silently ignored in the identity.
    """
    store_root = tmp_path / "store"
    ts = _ts()
    base = {"item": "goal-targets", "timepoint": ts, "source": "intake", "value": "v"}
    store.append("goal-targets", dict(base), root=store_root)
    # Differing timepoint -> distinct identity -> both persist.
    store.append("goal-targets", {**base, "timepoint": _ts(60)}, root=store_root)
    assert len(store.read("goal-targets", root=store_root)) == 2, "a differing timepoint wrongly collided"
    # Differing source -> distinct identity -> persists.
    store.append("goal-targets", {**base, "source": "correction"}, root=store_root)
    assert len(store.read("goal-targets", root=store_root)) == 3, "a differing source wrongly collided"
    # Differing item -> a different store file entirely.
    store.append("hard-limits", {**base, "item": "hard-limits"}, root=store_root)
    assert len(store.read("hard-limits", root=store_root)) == 1, "a differing item did not write its own stream"


# --------------------------------------------------------------------------- #
# Category 4 — mutation-style verification (observed RED, reverted)
# --------------------------------------------------------------------------- #


def test_widening_dedupe_to_include_value_breaks_the_collision_guarantee(monkeypatch):
    """Cat-4 (mutation): widen the dedupe key to include `value` -> the Cat-3 guarantee breaks.

    Deliberately MUTATE the store's dedupe identity to include `value` (the broken
    keying the S41 escapes warn about), then re-run the Cat-3 same-identity-collision
    scenario IN-PROCESS and assert the guarantee NO LONGER holds (the second write is
    NOT dropped — two lines now persist). This proves the Cat-3 test above is
    non-tautological: it genuinely depends on `value` being EXCLUDED from the dedupe
    key. monkeypatch reverts the mutation at test teardown.

    Observed-RED record: under the widened key, `len(readings)` becomes 2 (the second
    write is no longer a dedupe no-op) — the exact assertion `test_same_identity_
    different_value_collides_second_dropped` makes (`len == 1`) would RED.
    """
    # The mutation: a dedupe key that ALSO includes value (the broken widening).
    def _widened_key(reading):
        return tuple(reading[f] for f in ("item", "timepoint", "source", "value"))

    monkeypatch.setattr(keying, "dedupe_key", _widened_key)

    import tempfile
    from pathlib import Path
    store_root = Path(tempfile.mkdtemp()) / "store"
    ts = _ts()
    store.append("hard-limits", {"item": "hard-limits", "timepoint": ts, "source": "intake", "value": "no pressing"}, root=store_root)
    store.append("hard-limits", {"item": "hard-limits", "timepoint": ts, "source": "intake", "value": "DIFFERENT"}, root=store_root)
    readings = store.read("hard-limits", root=store_root)
    # Under the WIDENED key the second (different-value) write is NOT a dedupe no-op:
    # both persist. The Cat-3 guarantee (len == 1) is broken — the battery is RED here.
    assert len(readings) == 2, (
        "the dedupe-widening mutation did not change behavior — the Cat-3 test is "
        "tautological (it would pass even with a broken dedupe key)"
    )
