"""Operator-confirm-before-land sink-caller for model-extracted readings (ADR-0030-T3).

`land_confirmed(readings, *, root)` lands the operator-confirmed readings through the
UNCHANGED `ingest.manual_entry` sink (which writes via the single store-append path) — the
SAME disposes-after-gate shape as `capture.persist_capture`. The operator-confirm IS the
gate: this module adds NO second sink, NO second gate, and NO second dedupe identity. It
makes 0 model call (imports no model client); the `(item, timepoint, source)` dedupe is
INHERITED from the unchanged sink.

Biomarker-trend mirror (additive): a landed reading whose item is a REGISTERED-polarity
biomarker is ALSO recorded into the `biomarker::<marker>` namespace the router's
`recent-trend-direction` feed reads, via the shared `biomarker_mirror.mirror_registered` (the
ONE mirror rule, also used by the wearable land path `route.route_upload`, so the two cannot
diverge; it CALLS the frozen `loop_schema.record_biomarker`, never re-implements it). Without
this mirror a confirmed lab value landed only under its bare item name, never trended, and
never reached the plan author (the dead-feed gap). The mirror is purely additive — the bare
manual_entry land is unchanged, and the biomarker:: dedupe is `record_biomarker`'s own
`(item, timepoint, source)` identity.

The landing is ALL-OR-NOTHING (mirroring `ingest.import_csv`'s validate-then-write
precedent): the whole batch is validated against the SHARED conformance check
(`keying.is_conformant` — REUSED, never a second key) BEFORE the first land, so a mixed
valid+invalid batch lands NOTHING (no valid-prefix-lands-then-raises partial). A
non-conformant reading raises `ValueError` before any reading is written.
"""

import logging

from scripts.ingest import ingest
from scripts.serve import biomarker_mirror
from scripts.store import store
from scripts.store.keying import is_conformant


def land_confirmed(readings, *, root, loop_dispatch=None, loop_deid_client=None):
    """Land the operator-confirmed readings through the unchanged manual-entry sink.

    Validates the WHOLE batch first — every element must be a `dict` carrying every
    Line-Field-Set field (the shared `keying.is_conformant`, REUSED not re-defined) — and
    raises `ValueError` BEFORE the first land if any reading is non-conformant, so a mixed
    valid+invalid batch lands NOTHING (all-or-nothing, the `ingest.import_csv` precedent).
    It then lands each validated reading via the UNCHANGED `ingest.manual_entry(item,
    reading, root)`; the dedupe (a re-confirm of an already-landed reading appends 0
    duplicate lines) is inherited from the sink — this caller adds no second sink/dedupe key.
    A landed reading whose item is a REGISTERED-polarity biomarker is ADDITIONALLY mirrored
    into the `biomarker::<marker>` namespace via the shared `biomarker_mirror.mirror_registered`
    (the ONE rule, shared with the wearable land path), so a confirmed lab value trends and
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
    # Additive biomarker-trend mirror: a registered-polarity marker is ALSO recorded into the
    # biomarker:: namespace the router's recent-trend-direction feed reads (the bare manual_entry
    # land never populated it, so a lab value never trended -> never reached the plan). The ONE
    # mirror rule, shared with the wearable land path (route.route_upload).
    biomarker_mirror.mirror_registered(readings, store_root)
    # A `biomarker::` write-event: notify the plan loop's ONE debounced entry (ADR-0036-T2).
    # Additive side-effect — the debounce gate decides whether a re-gen fires; the `{"store": landed}`
    # receipt is unchanged. Loop seams threaded by the caller (production wiring is ADR-0036-T4).
    from scripts.serve import plan_loop
    try:
        plan_loop.signal(store_root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                         dispatch=loop_dispatch, deid_client=loop_deid_client)
    except Exception:
        # Fail-open: the loop notify is additive — a derivation/re-gen raise must never break the
        # primary land (the confirmed readings already landed; the `{"store": landed}` receipt is
        # the contract).
        logging.exception("plan-loop signal failed after confirmed land (additive; land unaffected)")
    return {"store": landed}


def confirm_large_change(changed_domains, *, rationale):
    """Emit an ADVISORY that a materially-large plan swap already occurred (ADR-0036-T4).

    The plan loop calls this when a re-gen's change magnitude reaches the pinned threshold. The
    re-gen has ALREADY recorded the new plan — the front-door promote inside `run_orchestrated`
    (the ADR-0032-frozen record path) wrote it, and `plan_schema.resolve_plan` resolves that
    just-written plan as the standing plan. This is therefore an ADVISORY for operator visibility,
    NOT a hold and NOT a rollback: it names the changed domains + the rationale so the operator sees
    that a majority-of-domains swap landed. Nothing here holds, reverts, or persists — the true
    hold-until-confirm is the deferred follow-on ADR-0036-T4b. Mirrors `land_confirmed`'s
    validate-then-act precedent: validates the request shape — a non-empty list of changed domain
    tokens plus a non-empty rationale — and returns a thin advisory receipt. Adds NO store key, NO
    second sink, NO dedupe identity.

    Args:
        changed_domains (list): The domain tokens whose standing plan the re-gen swapped.
        rationale (str): The plain-language what-changed summary surfaced in the advisory.

    Returns:
        (dict) `{"large_change_advisory": [changed domain tokens], "rationale": str}` — a thin
        advisory receipt of the swap that landed, mirroring `land_confirmed`'s receipt shape.
    """
    if (not isinstance(changed_domains, list) or not changed_domains
            or not all(isinstance(domain, str) and domain for domain in changed_domains)):
        raise ValueError(
            "large-change advisory requires a non-empty list of changed domain tokens"
        )
    if not isinstance(rationale, str) or not rationale:
        raise ValueError("large-change advisory requires a non-empty rationale")
    return {"large_change_advisory": list(changed_domains), "rationale": rationale}
