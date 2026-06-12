"""Explicit operator value-correction entry over the store primitive (bead 1vi).

`manual_correction(item, reading)` is the ingest-layer surface of the
superseding-append correction: it appends the corrected reading as a new line
for an already-stored `(item, timepoint, source)` via `store.correct`, and
every store read resolves that identity to the corrected value (latest-wins).
Any future edit layer bottoms out here — ADR-0004 zero-script artifacts cannot
host editing.

This entry lives in its OWN module, not in `ingest.py`: the ADR-0003-T2 0-edit
gates (`tests/ingest/test_adapters.py` AC-3/AC-6) pin the shared import routine
(`ingest.py` + `adapter.py`) byte-identical to the branch fork point, and the
correction entry is not part of the adapter-import surface they freeze. Same
single-sink discipline as that routine: the only write is the store primitive —
no raw NDJSON write, no second dedupe key, no model step (ADR-0001
No-Raw-Reading-To-Model Rule).
"""

from scripts.store import store


def manual_correction(item, reading, root=store.DEFAULT_ROOT):
    """Supersede one already-stored reading's value via `store.correct`.

    Where `manual_entry` inherits `store.append`'s dedupe (a re-entered value
    for a stored `(item, timepoint, source)` is dropped), this path appends the
    corrected reading as a superseding line, and every store read resolves the
    identity to it. The prior line stays on disk — the audit trail is
    append-only, never mutated or deleted.

    The `item` argument must equal `reading["item"]`; a mismatch raises
    `ValueError` (the same divergence guard as `manual_entry`), a missing
    `item` raises the uniform missing-field `ValueError`, and an identity that
    was never stored raises `ValueError` out of `store.correct` — a mistyped
    correction fails loud rather than silently creating a new series point.

    Args:
        item (str): The item identifier (names the item's store file). Must
            equal `reading["item"]`.
        reading (dict): The superseding reading carrying every Line Field Set
            field; its `(item, timepoint, source)` must already be stored.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Raises:
        ValueError: The `item` argument disagrees with `reading["item"]`, the
            reading is missing a required Line Field Set field, or no stored
            reading carries its `(item, timepoint, source)` identity.
    """
    if "item" not in reading:
        raise ValueError(
            f"reading missing required field(s); needs {store.keying.LINE_FIELDS}"
        )
    if reading["item"] != item:
        raise ValueError(
            f"item {item!r} disagrees with reading item {reading['item']!r}"
        )
    store.correct(reading["item"], reading, root=root)
