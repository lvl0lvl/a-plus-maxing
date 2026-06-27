"""Operator-confirm-before-land sink-caller for model-extracted readings (ADR-0030-T3).

`land_confirmed(readings, *, root)` lands the operator-confirmed readings through the
UNCHANGED `ingest.manual_entry` sink (which writes via the single store-append path) — the
SAME disposes-after-gate shape as `capture.persist_capture`. The operator-confirm IS the
gate: this module adds NO second sink, NO second gate, and NO second dedupe identity. It
makes 0 model call (imports no model client) and adds 0 direct store write — the
`(item, timepoint, source)` dedupe is INHERITED from the unchanged sink.

The landing is ALL-OR-NOTHING (mirroring `ingest.import_csv`'s validate-then-write
precedent): the whole batch is validated against the SHARED conformance check
(`keying.is_conformant` — REUSED, never a second key) BEFORE the first land, so a mixed
valid+invalid batch lands NOTHING (no valid-prefix-lands-then-raises partial). A
non-conformant reading raises `ValueError` before any reading is written.
"""

from scripts.ingest import ingest
from scripts.store.keying import is_conformant


def land_confirmed(readings, *, root):
    """Land the operator-confirmed readings through the unchanged manual-entry sink.

    Validates the WHOLE batch first — every element must be a `dict` carrying every
    Line-Field-Set field (the shared `keying.is_conformant`, REUSED not re-defined) — and
    raises `ValueError` BEFORE the first land if any reading is non-conformant, so a mixed
    valid+invalid batch lands NOTHING (all-or-nothing, the `ingest.import_csv` precedent).
    It then lands each validated reading via the UNCHANGED `ingest.manual_entry(item,
    reading, root)`; the dedupe (a re-confirm of an already-landed reading appends 0
    duplicate lines) is inherited from the sink — this caller adds no second sink/dedupe key.
    Returns a thin receipt of the landed item tokens, mirroring `capture.persist_capture`'s
    shape.

    Args:
        readings (list): The operator-confirmed Line-Field-Set reading dicts.
        root (str | Path): The store root the confirmed readings land into.

    Returns:
        (dict) `{"store": [landed item tokens]}` — a thin receipt of what landed.
    """
    for reading in readings:
        if not isinstance(reading, dict) or not is_conformant(reading):
            raise ValueError(
                "confirmed reading missing a required Line-Field-Set field; "
                "the whole batch is rejected (nothing lands)"
            )
    landed = []
    for reading in readings:
        ingest.manual_entry(reading["item"], reading, root=root)
        landed.append(reading["item"])
    return {"store": landed}
