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

from scripts.serve import capture, extract
from scripts.store import keying, store

# Mirror test_extract.py: an absent identity config (fresh-clone posture) so the
# extractor write path's free-text PII scan runs the value classes with empty identity
# detection — the de-identified wired values below carry no PII, so they land in the store.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


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
        {"goal-domains": "Workout;Nutrition", "hard-limits": "no overhead pressing"},
        root=store_root, scaffold_root=tmp_path / "scaffold",
    )
    gd = store.read("goal-domains", root=store_root)
    hl = store.read("hard-limits", root=store_root)
    assert len(gd) == 1 and gd[0]["value"] == "Workout;Nutrition"
    assert len(hl) == 1 and hl[0]["value"] == "no overhead pressing"
    # Cross-read negative: hard-limits' value never appears under goal-domains, vice versa.
    assert all("overhead" not in str(r["value"]) for r in gd), "hard-limits leaked into goal-domains"
    assert all("Workout" not in str(r["value"]) for r in hl), "goal-domains leaked into hard-limits"


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


# =========================================================================== #
# ADR-0017-T1 — the SAME four categories on the EXTRACTOR write path
# (extract.persist_extraction -> capture.persist_capture -> store.append). The
# extractor REUSES persist_capture (0 forked store-write logic), so the battery
# proves the extractor write path inherits the store's collision/dedupe guarantees.
# =========================================================================== #


def _extract_persist(proposal, store_root, scaffold_root):
    """Route a crafted extraction proposal through the extractor's only store path."""
    return extract.persist_extraction(
        proposal, turn_text="t", root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )


# --------------------------------------------------------------------------- #
# Category 1 — cross-stream namespace collision (extractor write path)
# --------------------------------------------------------------------------- #


def test_extractor_write_to_one_token_never_cross_reads_as_another(tmp_path):
    """Cat-1 (extractor): an extractor write to `goal-domains` never reads back as `hard-limits`.

    A crafted proposal captures two DISTINCT wired tokens via the extractor's gate path;
    each token's `store.read` returns ONLY its own value — a read for token X never
    returns token Y's value (the S41 cross-stream fabrication case, on the extractor path).
    """
    store_root = tmp_path / "store"
    _extract_persist(
        {"goal-domains": "Workout;Nutrition", "hard-limits": "no overhead pressing"},
        store_root, tmp_path / "scaffold",
    )
    gd = store.read("goal-domains", root=store_root)
    hl = store.read("hard-limits", root=store_root)
    assert len(gd) == 1 and gd[0]["value"] == "Workout;Nutrition"
    assert len(hl) == 1 and hl[0]["value"] == "no overhead pressing"
    assert all("overhead" not in str(r["value"]) for r in gd), "hard-limits leaked into goal-domains"
    assert all("Workout" not in str(r["value"]) for r in hl), "goal-domains leaked into hard-limits"


# --------------------------------------------------------------------------- #
# Category 2 — same-timepoint dedupe / idempotency (extractor write path)
# --------------------------------------------------------------------------- #


def test_extractor_two_distinct_tokens_same_call_both_persist(tmp_path):
    """Cat-2 (extractor): two distinct tokens in one extractor call both persist.

    Two distinct items written by one extractor proposal have DIFFERENT
    `(item, timepoint, source)` identities (different item), so both persist — the
    dedupe is keyed on the full identity, not the timepoint alone.
    """
    store_root = tmp_path / "store"
    _extract_persist(
        {"goal-domains": "Workout", "recovery-status-band": "moderate"},
        store_root, tmp_path / "scaffold",
    )
    assert store.read("goal-domains", root=store_root)[0]["value"] == "Workout"
    assert store.read("recovery-status-band", root=store_root)[0]["value"] == "moderate"


def test_extractor_identical_recapture_same_timepoint_is_idempotent(tmp_path, monkeypatch):
    """Cat-2 (extractor): an identical re-capture at the same (item, timepoint, source) is a no-op.

    Drives the EXTRACTOR path (`extract.persist_extraction` -> the gate -> `store.append`),
    not `store.append` directly: two `persist_extraction` calls of the SAME proposal, with
    the gate's timepoint pinned (`capture._now` -> a fixed stamp) so both produce the same
    `(item, timepoint, source="intake")` identity. The second is a dedupe no-op, so the
    store holds one line — the extractor path inherits `store.append`'s idempotent dedupe.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _extract_persist({"goal-domains": "Workout"}, store_root, tmp_path / "scaffold")
    _extract_persist({"goal-domains": "Workout"}, store_root, tmp_path / "scaffold")  # identical re-capture
    assert len(store.read("goal-domains", root=store_root)) == 1, (
        "an identical re-capture on the extractor write path duplicated the line"
    )


# --------------------------------------------------------------------------- #
# Category 3 — dedupe-key boundary (value EXCLUDED) (extractor write path)
# --------------------------------------------------------------------------- #


def test_extractor_same_identity_different_value_collides_second_dropped(tmp_path, monkeypatch):
    """Cat-3 (extractor): same (item, timepoint, source) + a DIFFERENT value collides (second dropped).

    Drives the EXTRACTOR path (`extract.persist_extraction` -> the gate -> `store.append`),
    not `store.append` directly: two `persist_extraction` calls at the SAME pinned
    timepoint (`capture._now` fixed) under the same token with DIFFERENT values. `value`
    is EXCLUDED from the dedupe identity, so the second write is DROPPED (the S41
    dropped-contraindication safety case, on the extractor path) and the first value
    stands.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _extract_persist({"hard-limits": "no pressing"}, store_root, tmp_path / "scaffold")
    _extract_persist({"hard-limits": "DIFFERENT"}, store_root, tmp_path / "scaffold")
    readings = store.read("hard-limits", root=store_root)
    assert len(readings) == 1, "a same-identity different-value second write was not dropped"
    assert readings[0]["value"] == "no pressing", "the second write wrongly overrode the first value"


def test_extractor_any_single_differing_identity_field_does_not_collide(tmp_path, monkeypatch):
    """Cat-3 (extractor): a differing item OR timepoint does NOT collide (both persist).

    Drives the EXTRACTOR path (`extract.persist_extraction` -> the gate -> `store.append`),
    not `store.append` directly. Two identity fields the extractor path can vary —
    `timepoint` (the gate's `capture._now`) and `item` (the proposal token) — each yield a
    distinct identity, so both readings persist; none is silently ignored. (`source` is
    NOT varied here: the gate fixes `source="intake"` for every extractor write, so a
    source-variation is not reachable through this path — its contribution to the dedupe
    key is held by the direct-store Cat-3 battery above.)
    """
    store_root = tmp_path / "store"
    # Differing timepoint -> distinct identity -> both persist (same token, two pinned stamps).
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    _extract_persist({"goal-targets": "v"}, store_root, tmp_path / "scaffold")
    monkeypatch.setattr(capture, "_now", lambda: _ts(60))
    _extract_persist({"goal-targets": "v"}, store_root, tmp_path / "scaffold")
    assert len(store.read("goal-targets", root=store_root)) == 2, "a differing timepoint wrongly collided"
    # Differing item -> a different store file entirely (its own stream).
    _extract_persist({"hard-limits": "v"}, store_root, tmp_path / "scaffold")
    assert len(store.read("hard-limits", root=store_root)) == 1, "a differing item did not write its own stream"


# --------------------------------------------------------------------------- #
# Category 4 — mutation-style verification (extractor write path; observed RED, reverted)
# --------------------------------------------------------------------------- #


def test_extractor_widening_dedupe_to_include_value_breaks_collision(monkeypatch):
    """Cat-4 (mutation, extractor): widen the dedupe key to include `value` -> Cat-3 breaks.

    Drives the EXTRACTOR path (`extract.persist_extraction` -> the gate -> `store.append`),
    not `store.append` directly: with the gate's timepoint pinned (`capture._now` fixed)
    so two extractor writes share a `(item, timepoint, source)`, deliberately MUTATE the
    store's dedupe identity to include `value` and re-run the Cat-3 same-identity-collision
    scenario. Under the widened key the second (different-value) write is NO LONGER a
    dedupe no-op — both lines persist. This proves the extractor-path Cat-3 test is
    non-tautological: it genuinely depends on `value` being EXCLUDED AND on the extractor
    path itself (it would pass identically only because `persist_extraction` drives the
    gate). monkeypatch reverts both mutations at teardown.

    Observed-RED record: under the widened key `len(readings)` becomes 2 (the second
    write is no longer a dedupe no-op) — the exact assertion
    `test_extractor_same_identity_different_value_collides_second_dropped` makes
    (`len == 1`) would RED.
    """
    def _widened_key(reading):
        return tuple(reading[f] for f in ("item", "timepoint", "source", "value"))

    monkeypatch.setattr(keying, "dedupe_key", _widened_key)
    monkeypatch.setattr(capture, "_now", lambda: _ts())

    import tempfile
    from pathlib import Path
    store_root = Path(tempfile.mkdtemp()) / "store"
    scaffold_root = Path(tempfile.mkdtemp()) / "scaffold"
    _extract_persist({"hard-limits": "no pressing"}, store_root, scaffold_root)
    _extract_persist({"hard-limits": "DIFFERENT"}, store_root, scaffold_root)
    readings = store.read("hard-limits", root=store_root)
    assert len(readings) == 2, (
        "the dedupe-widening mutation did not change behavior — the extractor-path Cat-3 "
        "test is tautological (it would pass even with a broken dedupe key)"
    )


# =========================================================================== #
# ADR-0018-T1 — the SAME four categories on the Step-1 DEMOGRAPHIC write paths.
# The demographic capture (sex-for-dosing / bodyweight-band / equipment-access-class
# pass-through tokens + the birth-year -> date-of-birth raw source) reuses
# `persist_capture` -> `store.append` (0 forked store-write logic), so the battery proves
# the demographic write paths inherit the store's collision/dedupe guarantees. The `pka`
# MANDATE: all four categories on the NEW demographic write paths, category 4 observed RED.
# =========================================================================== #


def _persist(fields, store_root, scaffold_root):
    """Route demographic fields through the capture seam's only store path."""
    return capture.persist_capture(
        fields, root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )


# --------------------------------------------------------------------------- #
# Category 1 — cross-stream namespace collision (demographic write paths)
# --------------------------------------------------------------------------- #


def test_demographic_write_to_one_token_never_cross_reads_as_another(tmp_path):
    """Cat-1 (demographic): a write to `sex-for-dosing` never reads back as `bodyweight-band`.

    Capture two DISTINCT demographic tokens with distinct values; each token's `store.read`
    returns ONLY its own value — a read for token X never returns token Y's value. Uses the
    REAL demographic token names (not a synthetic placeholder), so it proves the actual
    write paths. Also asserts the birth-year `date-of-birth` raw source does not cross-read
    as a demographic token.
    """
    store_root = tmp_path / "store"
    _persist(
        {"sex-for-dosing": "male", "bodyweight-band": "80-90kg",
         "equipment-access-class": "full-home-gym", "date-of-birth": "1986"},
        store_root, tmp_path / "scaffold",
    )
    sex = store.read("sex-for-dosing", root=store_root)
    bw = store.read("bodyweight-band", root=store_root)
    eq = store.read("equipment-access-class", root=store_root)
    dob = store.read("date-of-birth", root=store_root)
    assert len(sex) == 1 and sex[0]["value"] == "male"
    assert len(bw) == 1 and bw[0]["value"] == "80-90kg"
    assert len(eq) == 1 and eq[0]["value"] == "full-home-gym"
    assert len(dob) == 1 and dob[0]["value"] == "1986"
    # Cross-read negatives: no token's value appears under another token's stream.
    assert all("80-90kg" not in str(r["value"]) for r in sex), "bodyweight-band leaked into sex-for-dosing"
    assert all("male" not in str(r["value"]) for r in bw), "sex-for-dosing leaked into bodyweight-band"
    assert all("1986" not in str(r["value"]) for r in eq), "date-of-birth leaked into equipment-access-class"
    # The raw date-of-birth source is its OWN stream, never a demographic token's.
    for token in ("sex-for-dosing", "bodyweight-band", "equipment-access-class"):
        assert all("1986" not in str(r["value"]) for r in store.read(token, root=store_root)), (
            f"the raw date-of-birth value leaked into the {token!r} token stream"
        )


# --------------------------------------------------------------------------- #
# Category 2 — same-timepoint dedupe / idempotency (demographic write paths)
# --------------------------------------------------------------------------- #


def test_two_distinct_demographic_tokens_same_timepoint_both_persist(tmp_path, monkeypatch):
    """Cat-2 (demographic): two distinct demographic tokens at the SAME timepoint both persist.

    Drives the capture path with the timepoint pinned (`capture._now` fixed) so two distinct
    demographic tokens share a timepoint. They have DIFFERENT `(item, timepoint, source)`
    identities (different item), so both persist — keyed on the full identity, not timepoint.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"sex-for-dosing": "male", "equipment-access-class": "full-home-gym"},
             store_root, tmp_path / "scaffold")
    assert store.read("sex-for-dosing", root=store_root)[0]["value"] == "male"
    assert store.read("equipment-access-class", root=store_root)[0]["value"] == "full-home-gym"


def test_identical_demographic_recapture_same_timepoint_is_idempotent(tmp_path, monkeypatch):
    """Cat-2 (demographic): an identical demographic re-capture at a pinned timepoint is a no-op.

    Two `persist_capture` calls of the SAME demographic token, with `capture._now` pinned so
    both produce the same `(item, timepoint, source="intake")` identity. The second is a
    dedupe no-op — the demographic path inherits `store.append`'s idempotent dedupe (a
    double-submit never duplicates the line).
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"bodyweight-band": "80-90kg"}, store_root, tmp_path / "scaffold")
    _persist({"bodyweight-band": "80-90kg"}, store_root, tmp_path / "scaffold")  # identical re-capture
    assert len(store.read("bodyweight-band", root=store_root)) == 1, (
        "an identical demographic re-capture duplicated the line"
    )


# --------------------------------------------------------------------------- #
# Category 3 — dedupe-key boundary (value EXCLUDED) (demographic write paths)
# --------------------------------------------------------------------------- #


def test_demographic_same_identity_different_value_collides_second_dropped(tmp_path, monkeypatch):
    """Cat-3 (demographic): same (item, timepoint, source) + a DIFFERENT value collides (second dropped).

    Two `persist_capture` calls at the SAME pinned timepoint under the same demographic token
    with DIFFERENT (both in-enum) values. `value` is EXCLUDED from the dedupe identity, so the
    second write is DROPPED (a value correction is an explicit `store.correct`) and the first
    stands. Uses two valid bodyweight bands so the bounded-enum gate is not the thing dropping
    the write — the dedupe is.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"bodyweight-band": "80-90kg"}, store_root, tmp_path / "scaffold")
    _persist({"bodyweight-band": "90-100kg"}, store_root, tmp_path / "scaffold")
    readings = store.read("bodyweight-band", root=store_root)
    assert len(readings) == 1, "a same-identity different-value second write was not dropped"
    assert readings[0]["value"] == "80-90kg", "the second write wrongly overrode the first value"


def test_demographic_any_single_differing_identity_field_does_not_collide(tmp_path, monkeypatch):
    """Cat-3 (demographic): a differing timepoint OR item does NOT collide (both persist).

    The two identity fields the demographic capture path can vary — `timepoint`
    (`capture._now`) and `item` (the demographic token) — each yield a distinct identity, so
    both readings persist; none is silently ignored. (`source` is fixed `"intake"` for every
    capture write, its contribution held by the direct-store Cat-3 battery above.)
    """
    store_root = tmp_path / "store"
    # Differing timepoint -> distinct identity -> both persist (same token, two pinned stamps).
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    _persist({"sex-for-dosing": "male"}, store_root, tmp_path / "scaffold")
    monkeypatch.setattr(capture, "_now", lambda: _ts(60))
    _persist({"sex-for-dosing": "male"}, store_root, tmp_path / "scaffold")
    assert len(store.read("sex-for-dosing", root=store_root)) == 2, "a differing timepoint wrongly collided"
    # Differing item -> a different store file entirely (its own stream).
    _persist({"equipment-access-class": "full-home-gym"}, store_root, tmp_path / "scaffold")
    assert len(store.read("equipment-access-class", root=store_root)) == 1, (
        "a differing demographic item did not write its own stream"
    )


# --------------------------------------------------------------------------- #
# Category 4 — mutation-style verification (demographic write path; observed RED, reverted)
# --------------------------------------------------------------------------- #


def test_demographic_widening_dedupe_to_include_value_breaks_collision(monkeypatch):
    """Cat-4 (mutation, demographic): widen the dedupe key to include `value` -> Cat-3 breaks.

    With the capture timepoint pinned (`capture._now` fixed) so two demographic writes share a
    `(item, timepoint, source)`, deliberately MUTATE the store's dedupe identity to include
    `value` and re-run the Cat-3 same-identity-collision scenario on the demographic path.
    Under the widened key the second (different-value) write is NO LONGER a dedupe no-op —
    both lines persist. This proves the demographic-path Cat-3 test is non-tautological: it
    genuinely depends on `value` being EXCLUDED. monkeypatch reverts both mutations at
    teardown.

    Observed-RED record: under the widened key `len(readings)` becomes 2 (the second write is
    no longer a dedupe no-op) — the exact assertion
    `test_demographic_same_identity_different_value_collides_second_dropped` makes (`len == 1`)
    would RED.
    """
    def _widened_key(reading):
        return tuple(reading[f] for f in ("item", "timepoint", "source", "value"))

    monkeypatch.setattr(keying, "dedupe_key", _widened_key)
    monkeypatch.setattr(capture, "_now", lambda: _ts())

    import tempfile
    from pathlib import Path
    store_root = Path(tempfile.mkdtemp()) / "store"
    scaffold_root = Path(tempfile.mkdtemp()) / "scaffold"
    _persist({"bodyweight-band": "80-90kg"}, store_root, scaffold_root)
    _persist({"bodyweight-band": "90-100kg"}, store_root, scaffold_root)
    readings = store.read("bodyweight-band", root=store_root)
    assert len(readings) == 2, (
        "the dedupe-widening mutation did not change behavior — the demographic-path Cat-3 "
        "test is tautological (it would pass even with a broken dedupe key)"
    )


# =========================================================================== #
# ADR-0019-T1 — the SAME four categories on the chat-sourced rich-domain RAW-SOURCE
# write paths. Each chat field (nutrition-detail / supplement-stack / peptide-stack /
# training-detail) writes its NAMED-EXCLUDED raw source store item
# (raw-nutrition-free-text / raw-supplement-free-text / raw-peptide-free-text /
# raw-training-detail-free-text) via `persist_capture` -> `store.append` (0 forked
# store-write logic), so the battery proves the new write paths inherit the store's
# collision/dedupe guarantees. The `pka` MANDATE: all four categories on the NEW chat
# write paths, category 4 observed RED. (`summarize` derives the coarse band from the
# raw source — the de-identification is proven by the AC-2 output scan in test_router.py;
# this battery is the store-surface guarantee, not the de-identification proof.)
# =========================================================================== #

# (chat form field, named-excluded raw source store item, a realistic raw value).
_CHAT_CASES = (
    ("nutrition-detail", "raw-nutrition-free-text", "mostly chicken rice broccoli, 5 meals"),
    ("supplement-stack", "raw-supplement-free-text", "creatine 5g, whey, omega-3"),
    ("peptide-stack", "raw-peptide-free-text", "BPC-157 250mcg twice daily"),
    ("training-detail", "raw-training-detail-free-text", "PPL 6x/week, heavy squats"),
)


# --------------------------------------------------------------------------- #
# Category 1 — cross-stream namespace collision (chat raw-source write paths)
# --------------------------------------------------------------------------- #


def test_chat_write_to_one_raw_source_never_cross_reads_as_another(tmp_path):
    """Cat-1 (chat): a write to one chat raw source never reads back as another.

    Capture all four DISTINCT chat fields with distinct values; each raw source's
    `store.read` returns ONLY its own value — a read for raw source X never returns raw
    source Y's value. Uses the REAL chat raw-source item names (not a synthetic
    placeholder), so it proves the actual write paths. Also asserts each chat field
    writes its RAW SOURCE, never the derived band token directly.
    """
    from scripts.plan import router

    store_root = tmp_path / "store"
    _persist(
        {field: value for field, _raw, value in _CHAT_CASES},
        store_root, tmp_path / "scaffold",
    )
    by_source = {raw: store.read(raw, root=store_root) for _f, raw, _v in _CHAT_CASES}
    for _field, raw, value in _CHAT_CASES:
        assert len(by_source[raw]) == 1 and by_source[raw][0]["value"] == value, raw
    # Cross-read negatives: no raw source's value appears under another raw source's stream.
    for _field, raw, value in _CHAT_CASES:
        for other_field, other_raw, other_value in _CHAT_CASES:
            if other_raw == raw:
                continue
            assert all(other_value not in str(r["value"]) for r in by_source[raw]), (
                f"{other_raw!r} value leaked into the {raw!r} stream"
            )
    # The derived band tokens are NEVER written directly — only the raw sources.
    for token in ("dietary-pattern-class", "supplement-stack-class", "peptide-use-class",
                  "training-volume-band"):
        assert store.read(token, root=store_root) == [], (
            f"a chat field wrongly wrote the {token!r} band token directly (must be derived)"
        )
        assert token in router.SUMMARY_FIELD_SET  # the band IS a field-set token, just derived


# --------------------------------------------------------------------------- #
# Category 2 — same-timepoint dedupe / idempotency (chat raw-source write paths)
# --------------------------------------------------------------------------- #


def test_two_distinct_chat_raw_sources_same_timepoint_both_persist(tmp_path, monkeypatch):
    """Cat-2 (chat): two distinct chat raw sources at the SAME timepoint both persist.

    Drives the capture path with the timepoint pinned (`capture._now` fixed) so two distinct
    chat raw sources share a timepoint. They have DIFFERENT `(item, timepoint, source)`
    identities (different item), so both persist — keyed on the full identity, not timepoint.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"nutrition-detail": "vegan, 5 meals", "peptide-stack": "BPC-157 250mcg"},
             store_root, tmp_path / "scaffold")
    assert store.read("raw-nutrition-free-text", root=store_root)[0]["value"] == "vegan, 5 meals"
    assert store.read("raw-peptide-free-text", root=store_root)[0]["value"] == "BPC-157 250mcg"


def test_identical_chat_recapture_same_timepoint_is_idempotent(tmp_path, monkeypatch):
    """Cat-2 (chat): an identical chat re-capture at a pinned timepoint is a no-op.

    Two `persist_capture` calls of the SAME chat field, with `capture._now` pinned so both
    produce the same `(item, timepoint, source="intake")` identity. The second is a dedupe
    no-op — the chat raw-source path inherits `store.append`'s idempotent dedupe (a
    double-submit never duplicates the line).
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"supplement-stack": "creatine 5g"}, store_root, tmp_path / "scaffold")
    _persist({"supplement-stack": "creatine 5g"}, store_root, tmp_path / "scaffold")  # identical
    assert len(store.read("raw-supplement-free-text", root=store_root)) == 1, (
        "an identical chat re-capture duplicated the line"
    )


# --------------------------------------------------------------------------- #
# Category 3 — dedupe-key boundary (value EXCLUDED) (chat raw-source write paths)
# --------------------------------------------------------------------------- #


def test_chat_same_identity_different_value_collides_second_dropped(tmp_path, monkeypatch):
    """Cat-3 (chat): same (item, timepoint, source) + a DIFFERENT value collides (second dropped).

    Two `persist_capture` calls at the SAME pinned timepoint under the same chat field with
    DIFFERENT values. `value` is EXCLUDED from the dedupe identity, so the second write is
    DROPPED (a value correction is an explicit `store.correct`) and the first stands.
    """
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    store_root = tmp_path / "store"
    _persist({"nutrition-detail": "vegan, 5 meals"}, store_root, tmp_path / "scaffold")
    _persist({"nutrition-detail": "omnivore, 3 meals"}, store_root, tmp_path / "scaffold")
    readings = store.read("raw-nutrition-free-text", root=store_root)
    assert len(readings) == 1, "a same-identity different-value second write was not dropped"
    assert readings[0]["value"] == "vegan, 5 meals", "the second write wrongly overrode the first value"


def test_chat_any_single_differing_identity_field_does_not_collide(tmp_path, monkeypatch):
    """Cat-3 (chat): a differing timepoint OR item does NOT collide (both persist).

    The two identity fields the chat capture path can vary — `timepoint` (`capture._now`)
    and `item` (the chat raw source) — each yield a distinct identity, so both readings
    persist; none is silently ignored. (`source` is fixed `"intake"` for every capture
    write, its contribution held by the direct-store Cat-3 battery above.)
    """
    store_root = tmp_path / "store"
    # Differing timepoint -> distinct identity -> both persist (same field, two pinned stamps).
    monkeypatch.setattr(capture, "_now", lambda: _ts())
    _persist({"training-detail": "PPL 6x/week"}, store_root, tmp_path / "scaffold")
    monkeypatch.setattr(capture, "_now", lambda: _ts(60))
    _persist({"training-detail": "PPL 6x/week"}, store_root, tmp_path / "scaffold")
    assert len(store.read("raw-training-detail-free-text", root=store_root)) == 2, (
        "a differing timepoint wrongly collided"
    )
    # Differing item -> a different store file entirely (its own stream).
    _persist({"peptide-stack": "BPC-157 250mcg"}, store_root, tmp_path / "scaffold")
    assert len(store.read("raw-peptide-free-text", root=store_root)) == 1, (
        "a differing chat item did not write its own stream"
    )


# --------------------------------------------------------------------------- #
# Category 4 — mutation-style verification (chat write path; observed RED, reverted)
# --------------------------------------------------------------------------- #


def test_chat_widening_dedupe_to_include_value_breaks_collision(monkeypatch):
    """Cat-4 (mutation, chat): widen the dedupe key to include `value` -> Cat-3 breaks.

    With the capture timepoint pinned (`capture._now` fixed) so two chat writes share a
    `(item, timepoint, source)`, deliberately MUTATE the store's dedupe identity to include
    `value` and re-run the Cat-3 same-identity-collision scenario on the chat raw-source
    path. Under the widened key the second (different-value) write is NO LONGER a dedupe
    no-op — both lines persist. This proves the chat-path Cat-3 test is non-tautological:
    it genuinely depends on `value` being EXCLUDED. monkeypatch reverts both mutations at
    teardown.

    Observed-RED record: under the widened key `len(readings)` becomes 2 (the second write
    is no longer a dedupe no-op) — the exact assertion
    `test_chat_same_identity_different_value_collides_second_dropped` makes (`len == 1`)
    would RED.
    """
    def _widened_key(reading):
        return tuple(reading[f] for f in ("item", "timepoint", "source", "value"))

    monkeypatch.setattr(keying, "dedupe_key", _widened_key)
    monkeypatch.setattr(capture, "_now", lambda: _ts())

    import tempfile
    from pathlib import Path
    store_root = Path(tempfile.mkdtemp()) / "store"
    scaffold_root = Path(tempfile.mkdtemp()) / "scaffold"
    _persist({"nutrition-detail": "vegan, 5 meals"}, store_root, scaffold_root)
    _persist({"nutrition-detail": "omnivore, 3 meals"}, store_root, scaffold_root)
    readings = store.read("raw-nutrition-free-text", root=store_root)
    assert len(readings) == 2, (
        "the dedupe-widening mutation did not change behavior — the chat-path Cat-3 "
        "test is tautological (it would pass even with a broken dedupe key)"
    )
