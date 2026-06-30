"""Operator-confirm-before-land sink-caller for model-extracted readings (ADR-0030-T3).

`land_confirmed(readings, *, root)` lands the operator-confirmed readings through the
UNCHANGED `ingest.manual_entry` sink (which writes via the single store-append path) — the
SAME disposes-after-gate shape as `capture.persist_capture`. The operator-confirm IS the
gate: this module adds NO second sink, NO second gate, and NO second dedupe identity. It
makes 0 model call (imports no model client); the `(item, timepoint, source)` dedupe is
INHERITED from the unchanged sink.

Biomarker-trend mirror (additive): a landed reading whose item is a REGISTERED-polarity
biomarker (`biomarker_meta.METADATA` with a non-None `good_direction`) is ALSO recorded into
the `biomarker::<marker>` namespace via the EXISTING `loop_schema.record_biomarker` (called,
never re-implemented — a frozen store writer). That namespace is what the router's
`recent-trend-direction` feed reads; without this mirror a confirmed lab value landed only
under its bare item name, never trended, and never reached the plan author (the dead-feed
gap). The mirror is purely additive — the bare manual_entry land is unchanged, and the
biomarker:: dedupe is `record_biomarker`'s own `(item, timepoint, source)` identity. Only the
de-identified marker NAME + numeric value cross — the same coarse trend the dashboard reads.

The landing is ALL-OR-NOTHING (mirroring `ingest.import_csv`'s validate-then-write
precedent): the whole batch is validated against the SHARED conformance check
(`keying.is_conformant` — REUSED, never a second key) BEFORE the first land, so a mixed
valid+invalid batch lands NOTHING (no valid-prefix-lands-then-raises partial). A
non-conformant reading raises `ValueError` before any reading is written.
"""

from scripts.ingest import ingest
from scripts.store import biomarker_meta, loop_schema, store
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
    A landed reading whose item is a REGISTERED-polarity biomarker is ADDITIONALLY mirrored
    into the `biomarker::<marker>` namespace via the existing `loop_schema.record_biomarker`
    (the frozen store writer, called not re-implemented), so a confirmed lab value trends and
    reaches the router's `recent-trend-direction` feed — additive, the bare land is unchanged.
    Returns a thin receipt of the landed item tokens, mirroring `capture.persist_capture`'s
    shape.

    Args:
        readings (list): The operator-confirmed Line-Field-Set reading dicts.
        root (str | Path | None): The store root the confirmed readings land into; None
            resolves to `store.DEFAULT_ROOT` (the operator-entry build passes no store_root).

    Returns:
        (dict) `{"store": [landed item tokens]}` — a thin receipt of what landed.
    """
    for reading in readings:
        if not isinstance(reading, dict) or not is_conformant(reading):
            raise ValueError(
                "confirmed reading missing a required Line-Field-Set field; "
                "the whole batch is rejected (nothing lands)"
            )
    # Resolve a None root to the production default, mirroring `route_upload` and
    # `capture.persist_capture`: the operator-entry build (`scripts/serve/__main__`)
    # constructs the handler with no store_root (None), and an EXPLICIT None overrides the
    # sink's own `root=store.DEFAULT_ROOT` default — so without this `store._item_path(item,
    # None)` raises `TypeError` and the confirmed readings never land in production.
    store_root = root if root is not None else store.DEFAULT_ROOT
    landed = []
    for reading in readings:
        ingest.manual_entry(reading["item"], reading, root=store_root)
        landed.append(reading["item"])
        # Additive biomarker-trend mirror: a registered-polarity marker is ALSO recorded into
        # the biomarker:: namespace the router's recent-trend-direction feed reads (the bare
        # manual_entry land above never populated it, so a lab value never trended -> never
        # reached the plan). Normalize to the registry's canonical marker key (prefix-stripped,
        # lowercased) so the mirror lands under the exact `biomarker::<marker>` the feed reads.
        meta = biomarker_meta.get(reading["item"])
        if meta is not None and meta["good_direction"] is not None:
            marker = biomarker_meta._strip_prefix(reading["item"]).lower()
            loop_schema.record_biomarker(
                marker, reading["timepoint"], reading["value"], store_root
            )
    return {"store": landed}
