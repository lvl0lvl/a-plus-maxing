"""Additive biomarker-trend mirror — populate the `biomarker::` namespace the router trend feed reads.

A landed reading whose item is a REGISTERED-polarity biomarker (`biomarker_meta.METADATA` with a
non-None `good_direction`) is ALSO recorded into the `biomarker::<marker>` namespace via the
EXISTING `loop_schema.record_biomarker` (a frozen store writer, CALLED not re-implemented). That
namespace is what `router`'s `recent-trend-direction` feed reads; without this mirror an
ingested/confirmed reading landed only under its bare item name, never trended, and never reached
the plan (the dead-feed gap). The mirror is purely additive — the bare land is unchanged; the
`biomarker::` dedupe is `record_biomarker`'s own `(item, timepoint, source)` identity. Only the
de-identified marker NAME + numeric value cross — the same coarse trend the dashboard reads.

This is the ONE mirror rule shared by BOTH serve-layer land paths — the confirmed-extraction land
(`confirm.land_confirmed`) and the wearable/adapter land (`route.route_upload`) — so the two cannot
silently diverge on which markers mirror or how the canonical key is derived.
"""

from scripts.store import biomarker_meta, loop_schema


def mirror_registered(readings, root):
    """Mirror each registered-polarity biomarker reading into the `biomarker::` trend namespace.

    Skips a reading whose item is not a registered marker or is registered without a polarity
    (`good_direction` None) — only a polarity marker feeds `recent-trend-direction`. Normalizes the
    item to the registry's canonical key (prefix-stripped, lowercased) so the mirror lands under the
    exact `biomarker::<marker>` the feed reads. Idempotent via `record_biomarker`'s own dedupe.

    Args:
        readings (iterable): Landed Line-Field-Set readings (each carries `item`/`timepoint`/`value`).
        root (str | Path): The store root the mirror writes into.
    """
    for reading in readings:
        meta = biomarker_meta.get(reading["item"])
        if meta is not None and meta["good_direction"] is not None:
            marker = biomarker_meta._strip_prefix(reading["item"]).lower()
            loop_schema.record_biomarker(marker, reading["timepoint"], reading["value"], root)
