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

Large-change hold acts (ADR-0040): `confirm_large_change(changed_domains, rationale)`
builds the operator confirm-PROMPT payload for a materially-large plan swap the loop has
HELD — it names the changed domains + the rationale, neither holding nor releasing.
`confirm_plan_change(domain, plan_date, decision, root)` is the terminal release act:
it applies the operator's explicit confirm/decline of a held re-gen — flipping the
`plan-confirm::` pointer via `plan_confirm.set_decision` and firing the deferred
`_post_promote_tailoring` seam ONCE over the union of confirmed held domains on a
pending->confirmed transition, or GC'ing a stale pending to `declined` (with no tailoring)
on a decline or a late confirm. Same validate-then-act shape as `land_confirmed`; adds no
store key, second sink, or dedupe identity.
"""

import datetime
import logging

from scripts.ingest import ingest
from scripts.serve import biomarker_mirror
from scripts.store import plan_confirm, plan_schema, store
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
    """Build the operator confirm-PROMPT payload for a materially-large plan swap (ADR-0036-T4 → ADR-0040).

    The plan loop calls this when a re-gen's change magnitude reaches the pinned threshold. Under
    ADR-0040 that swap is HELD: `plan_loop.regenerate` marks every promoted domain `pending` before it
    returns, so the read-side skip (T2) resolves the held re-gen `NO_PLAN_TODAY` — it does NOT stand and
    is not tailored/egressed until an explicit operator confirm (`confirm_plan_change`). This function
    neither holds nor releases; it names the changed domains + the rationale so the OQ-5 confirm UX can
    PROMPT the operator to confirm or decline the held swap — the returned dict is that prompt payload,
    no longer a "swap-already-landed" notice. Mirrors `land_confirmed`'s validate-then-act precedent:
    validates the request shape — a non-empty list of changed domain tokens plus a non-empty rationale —
    and returns a thin prompt receipt. Adds NO store key, NO second sink, NO dedupe identity.

    Args:
        changed_domains (list): The domain tokens whose standing plan the held re-gen swaps.
        rationale (str): The plain-language what-changed summary surfaced in the confirm prompt.

    Returns:
        (dict) `{"large_change_advisory": [changed domain tokens], "rationale": str}` — a thin
        confirm-prompt receipt of the held swap, mirroring `land_confirmed`'s receipt shape.
    """
    if (not isinstance(changed_domains, list) or not changed_domains
            or not all(isinstance(domain, str) and domain for domain in changed_domains)):
        raise ValueError(
            "large-change advisory requires a non-empty list of changed domain tokens"
        )
    if not isinstance(rationale, str) or not rationale:
        raise ValueError("large-change advisory requires a non-empty rationale")
    return {"large_change_advisory": list(changed_domains), "rationale": rationale}


def confirm_plan_change(domain, plan_date, decision, *, root, tailor_client=None):
    """Apply the operator's explicit confirm/decline of a held large plan re-gen (ADR-0040-T4).

    The terminal release act of the large-change HOLD, mirroring `land_confirmed`'s
    validate-then-act shape. Validates the request shape fail-loud BEFORE any act — `domain`
    is a `plan_schema.PLAN_DOMAINS` member, `plan_date` is a real YYYY-MM-DD string, and
    `decision` is enum-validated against T1's `plan_confirm.DECISION_CONFIRMED` /
    `DECISION_DECLINED` (a present-but-invalid token like `"approved"` raises `ValueError`,
    NO default-allow `else`, so an unvalidated token can never flip the pointer to confirmed
    and egress a tailored section). On an in-window `confirmed` (`plan_date >= today`) it flips
    the `pending` pointer via `plan_confirm.set_decision` — but ONLY on the pending->`confirmed`
    TRANSITION (a repeat confirm of an already-`confirmed` domain short-circuits to a no-op, so
    the metered tailoring fires at most once), then fires the deferred `plan_loop`
    `_post_promote_tailoring` seam ONCE over the UNION of every currently-`confirmed` held domain
    for that `plan_date` (the fresh replace-not-accrete render would otherwise clobber a prior
    confirmed domain's section). On `declined` — OR a late confirm where `plan_date < today` — it
    GC's the stale pending to `declined` and fires no tailoring, so no unconfirmed re-gen ever
    stands. Resolves a `None` root to `store.DEFAULT_ROOT` (the operator-entry build's None
    store_root). Adds no store key / second sink / dedupe identity — the pointer write is T1's
    `set_decision` via the unchanged `store.correct`.

    Args:
        domain (str): The plan domain (a `plan_schema.PLAN_DOMAINS` member).
        plan_date (str): The held plan's YYYY-MM-DD date.
        decision (str): `"confirmed"` or `"declined"`.
        root (str | Path | None): The store root; None resolves to `store.DEFAULT_ROOT`.
        tailor_client (optional): The care-lane presentation client; None keeps the tailoring
            seam a pass-through (0 spend).

    Returns:
        (dict) `{"domain": str, "decision": str}` — a thin receipt of the resulting decision.

    Raises:
        ValueError: An unknown domain, a malformed `plan_date`, or a decision token outside
            {"confirmed", "declined"} — validated fail-loud before any act. Also PROPAGATES the
            `ValueError` `plan_confirm.set_decision` raises when no pointer is stored for
            `(domain, plan_date)` (a forged / stale confirm of a never-marked date); the serve
            route degrades that to a 400, but a future OQ-5 programmatic caller sees it raise.
    """
    if domain not in plan_schema.PLAN_DOMAINS:
        raise ValueError(f"confirm-plan-change: unknown domain {domain!r}")
    try:
        plan_day = datetime.date.fromisoformat(plan_date)
    except (TypeError, ValueError):
        raise ValueError(f"confirm-plan-change: plan_date must be YYYY-MM-DD, got {plan_date!r}")
    if decision not in (plan_confirm.DECISION_CONFIRMED, plan_confirm.DECISION_DECLINED):
        raise ValueError(
            f"confirm-plan-change: decision must be "
            f"{plan_confirm.DECISION_CONFIRMED!r} | {plan_confirm.DECISION_DECLINED!r}, "
            f"got {decision!r}"
        )
    store_root = root if root is not None else store.DEFAULT_ROOT

    # Decline, or a late confirm (plan_date < today): GC the stale pending to declined and fire NO
    # tailoring — the held reading never stands (AC-3 fail-closed + AC-4 late-confirm refusal).
    if decision == plan_confirm.DECISION_DECLINED or plan_day < datetime.date.today():
        plan_confirm.set_decision(domain, plan_date, plan_confirm.DECISION_DECLINED, store_root)
        return {"domain": domain, "decision": plan_confirm.DECISION_DECLINED}

    # An in-window confirm: fire the metered tailoring ONLY on the pending->confirmed transition, so
    # a repeat confirm of an already-confirmed domain is a no-op (converse-count == 1 across confirms).
    if plan_confirm.decision_for(domain, plan_date, store_root) == plan_confirm.DECISION_CONFIRMED:
        return {"domain": domain, "decision": plan_confirm.DECISION_CONFIRMED}
    plan_confirm.set_decision(domain, plan_date, plan_confirm.DECISION_CONFIRMED, store_root)

    # Re-render the fresh (replace-not-accrete) care-lane tailored block over the UNION of every
    # currently-confirmed held domain for this plan_date, so a per-domain confirm never clobbers a
    # prior confirmed domain's section (Architect F2). The flip above MUST precede this fire — the
    # tailoring emit-gate applies `filter_confirmed`, so a still-pending domain would be dropped.
    confirmed_union = {
        confirmed_domain: plan_schema.read_plan(confirmed_domain, plan_date, store_root)["plan"]
        for confirmed_domain in plan_schema.PLAN_DOMAINS
        if plan_confirm.decision_for(confirmed_domain, plan_date, store_root)
        == plan_confirm.DECISION_CONFIRMED
    }
    # Lazy function-scope import: the confirm.py -> plan_loop edge reverses plan_loop's own lazy
    # plan_loop -> confirm edge (`regenerate`), so a module-level import would cycle (Architect F3).
    from scripts.serve import plan_loop
    plan_loop._post_promote_tailoring(
        confirmed_union, store_root, tailor_client=tailor_client, plan_date=plan_date
    )
    return {"domain": domain, "decision": plan_confirm.DECISION_CONFIRMED}
