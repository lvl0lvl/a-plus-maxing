"""Operator-confirm-before-land sink-caller for model-extracted readings (ADR-0030-T3).

`land_confirmed(readings, *, root)` lands each operator-confirmed reading through the
UNCHANGED `ingest.manual_entry` sink (which writes via the single store-append path) — the
SAME disposes-after-gate shape as `capture.persist_capture`. The operator-confirm IS the
gate: this module adds NO second sink, NO second gate, and NO second dedupe identity. It
makes 0 model call (imports no model client), adds 0 direct store write, and defines no
key of its own — the `(item, timepoint, source)` dedupe AND the uniform missing-field
rejection are INHERITED from the unchanged sink. A confirmed reading missing any
Line-Field-Set field lands nothing (the sink raises `ValueError`).
"""

from scripts.ingest import ingest


def land_confirmed(readings, *, root):
    """Land each operator-confirmed reading through the unchanged manual-entry sink.

    Iterates the operator-confirmed readings and lands each via the UNCHANGED
    `ingest.manual_entry(item, reading, root)`. The dedupe (a re-confirm of an already-landed
    reading appends 0 duplicate lines) and the uniform missing-field rejection (a reading
    short any Line-Field-Set field raises `ValueError` and lands nothing) are inherited from
    the sink — this caller adds no key/gate of its own. The reading's own `item` is passed
    (None when absent), so a reading missing `item` fails closed through the sink's uniform
    `ValueError` rather than a raw `KeyError`. Returns a thin receipt of the landed item
    tokens, mirroring `capture.persist_capture`'s shape.

    Args:
        readings (list): The operator-confirmed Line-Field-Set reading dicts.
        root (str | Path): The store root the confirmed readings land into.

    Returns:
        (dict) `{"store": [landed item tokens]}` — a thin receipt of what landed.
    """
    landed = []
    for reading in readings:
        ingest.manual_entry(reading.get("item"), reading, root=root)
        landed.append(reading["item"])
    return {"store": landed}
