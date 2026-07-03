"""Profile-aware Care Assistant conversation (the continuous post-unlock care chat).

Distinct from `chat.dispatch_turn` (the PRE-unlock intake elicitation). This is the POST-unlock care
conversation, and it is the operator's OWN private agent: it re-reads the operator's FULL profile
server-side each turn (`_care_profile`) — the operator's actual peptide / supplement / diet / training
/ injury detail, plus demographics / goals / genetics — so it reasons over the real specifics, not
coarse bands. The care-review clarifying questions are the conversation's opening turns, carried back
in `conversation`, so a reply continues them instead of restarting.

Privacy boundary (operator-directed): the de-identification line is the care -> SPECIALIST / plan
hand-off (`router.dispatch`), NOT the operator -> care-agent link. The care agent is private, so it
sees the operator's real health detail; only PURE IDENTITY stays stripped (legal name, exact DOB,
contact, address) — `_care_profile` is built on `router.summarize`, which is identity-safe by
construction (disjoint from the named-excluded identity PII), then enriched with the raw health
free-text. The one `converse` call carries this profile + the live conversation (the operator's own
words, already the no-train egress class) + the current turn. The profile is SERVER-derived each turn
(the client never supplies it), so a client cannot inject a forged profile. The plan/specialist path
(`summarize` -> `dispatch`) stays de-identified — unchanged.

Store-write: the care agent WRITES the facts the operator states back to the store through the EXACT
SAME gated path the intake chat uses — `extract.persist_extraction` -> `capture.persist_capture` — so a
model-proposed fact is de-identified BY DATA CLASS by the gate (a raw value under a wired token routes
record-only; the free-text PII scan backstops), NEVER a new store path or a new egress. The model
PROPOSES, the gate DISPOSES; the receipt reports what ACTUALLY LANDED. The extraction coverage/quality
is the model's job (runtime, the same as the intake extractor); this module supplies the gated wiring.
"""

import functools
import json
import logging

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.serve import extract
from scripts.store import store

# The field tokens the care turn's structured `extraction` may use (mapped to a plain-language
# description + allowed values). Supplied in the CONTEXT so the model knows WHICH facts to capture and
# in what shape; `capture.persist_capture` re-validates every one server-side (a bounded value out of
# its enum, or a raw value under a wired token, routes record-only — the model only PROPOSES). These
# are the capture FORM-FIELD names `persist_capture` routes by. `recovery-status-band` is the field
# the plan pipeline currently blocks on.
_EXTRACTABLE_FIELDS = {
    "recovery-status-band": "the operator's current recovery/readiness — EXACTLY one of: low, moderate, high",
    "training-experience": "years of training experience (a whole number)",
    "goal-priority-order": "the operator's stated ordering of goal priorities (free text)",
    "goal-targets": "the operator's stated goal/outcome targets (free text)",
    "hard-limits": "hard limits or things to strictly avoid (free text)",
    "nutrition-detail": "diet / nutrition specifics the operator states (free text)",
    "supplement-stack": "supplements + doses the operator states (free text)",
    "peptide-stack": "peptides + doses the operator states (free text)",
    "training-detail": "training split / days / volume specifics (free text)",
    "train-around": "injuries or issues to train around (free text)",
}

# A standing context note so the agent knows the conversation is durable (it was answering "I can't
# save" — false: the system auto-persists every turn to the conversation vault and restores it on
# reload, so the earlier turns it sees ARE the full, permanent history).
_PERSISTENCE_NOTE = (
    "This conversation is automatically saved and restored when the operator reloads — the earlier "
    "turns you are shown are the full, durable history, so never tell the operator you cannot save it."
)


def _weight_display(summary):
    """A human-readable weight in BOTH units from the de-id `bodyweight-band` kg value (or None).

    The de-id summary carries `bodyweight-band` = `"<kg>;<trend>"` (the canonical kilograms + trend);
    the operator may think in pounds, so the care context presents BOTH (`"238 lb (108 kg)"`) — no new
    raw data (the kg is already in the band). Lets the assistant talk weight in the operator's unit
    even when their explicit preference was captured before it was stored.
    """
    band = summary.get("bodyweight-band")
    if not band:
        return None
    try:
        kg = float(str(band).split(";")[0].strip())
    except (ValueError, TypeError):
        return None
    return f"{round(kg / 0.453592)} lb ({round(kg)} kg)"


def _weight_unit_preference(scaffold_root):
    """The operator's chosen weight unit ('pounds'/'kilograms') from the latest capture, or None.

    Read from the record-only scaffold `bodyweight-unit` (a display preference, not PII — `lbs`/`kg`),
    so the assistant LEADS with the operator's unit. None when unrecorded (older intake); the context
    then still carries both units via `_weight_display`, so the assistant is never kg-only.
    """
    from pathlib import Path

    from scripts.serve.capture import DEFAULT_SCAFFOLD_ROOT

    root = Path(scaffold_root) if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT
    if not root.exists():
        return None
    captures = sorted(root.glob("capture-*.json"))
    if not captures:
        return None
    try:
        data = json.loads(captures[-1].read_text())
    except (OSError, ValueError):
        return None
    unit = data.get("bodyweight-unit") if isinstance(data, dict) else None
    return {"lbs": "pounds", "kg": "kilograms"}.get(unit)


def _age_display(summary):
    """The operator's CHRONOLOGICAL age from the (legacy-misnamed) `training-age-band` token, or None.

    `training-age-band` holds the exact chronological age in years derived from the operator's birth
    year — NOT lifting experience, despite the token name. The name misled the assistant into asking
    whether 55 was age or training years; presenting it clearly as the operator's age removes that.
    """
    band = summary.get("training-age-band")
    if band is None:
        return None
    age = str(band).split(";")[0].strip()
    return f"{age} years" if age else None


# The operator's raw intake health free-text, mapped to a clear care-facing label. These are the
# named-excluded raw sources `summarize` collapses to coarse bands FOR THE SPECIALIST hand-off; the
# care agent is the operator's OWN agent, so it reads the SPECIFICS the operator entered — the
# peptides, supplement, diet, training, and injury detail — not the vague bands.
_CARE_HEALTH_DETAIL = {
    "nutrition": "raw-nutrition-free-text",
    "supplements": "raw-supplement-free-text",
    "peptides": "raw-peptide-free-text",
    "training": "raw-training-detail-free-text",
    "injuries": "raw-symptom-free-text",
}


def _scaffold_record(scaffold_root):
    """Merge the operator's record-only scaffold captures into one `{field: latest value}` dict.

    The gitignored scaffold holds record-only intake data the operator entered — MEDICATIONS
    (`rx-interaction-classes`, deliberately routed record-only because raw drug names are never
    de-identified for the specialist path), plus sleep, alcohol, smoker status, equipment detail,
    race, occupation. NONE of it is pure identity (legal name / exact DOB / contact / address route
    to the named-excluded store, not here), so the operator's OWN private care agent reads it. The
    latest non-empty value wins per field across captures.
    """
    import json
    from pathlib import Path

    from scripts.serve.capture import DEFAULT_SCAFFOLD_ROOT

    root = Path(scaffold_root) if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT
    if not root.exists():
        return {}
    merged = {}
    for path in sorted(root.glob("capture-*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            for key, value in data.items():
                if value:
                    merged[key] = value
    return merged


def _care_profile(store_read, *, scaffold_root=None, identity_config=None):
    """The FULL care-facing profile: the identity-safe summary PLUS the operator's raw health detail.

    The de-identification boundary is the care -> SPECIALIST / plan hand-off (`router.dispatch`), NOT
    the operator -> care-agent link. The care agent is the operator's OWN private agent, so it reads
    the operator's ACTUAL detail — the peptide / supplement / diet / training / injury free-text they
    entered at intake — instead of the coarse specialist-facing bands. Built ON TOP of
    `router.summarize`, which is identity-safe BY CONSTRUCTION (its output is disjoint from the
    named-excluded identity PII — legal name, exact DOB, contact, address never appear; only the
    derived age / weight / sex / equipment / goals / genetics / rx-classes do), then ENRICHED with the
    raw health free-text under `health_detail`. So the agent sees the operator's real specifics while
    pure identity stays stripped, and the specialist/plan path stays de-identified.
    """
    if identity_config is not None:
        profile = dict(router.summarize(store_read, identity_config=identity_config))
    else:
        profile = dict(router.summarize(store_read))
    detail = {}
    for label, item in _CARE_HEALTH_DETAIL.items():
        rows = store_read(item)
        if rows and rows[-1].get("value"):
            detail[label] = rows[-1]["value"]
    if detail:
        profile["health_detail"] = detail
    # Record-only scaffold data (medications + sleep/alcohol/smoker/equipment/race/occupation): the
    # operator's OWN agent reads it — none of it is pure identity. Medications get an explicit label so
    # the agent treats them as meds, not the (empty) de-identified `rx-interaction-classes` summary
    # token; the rest is surfaced under `record` as additional profile context.
    record = _scaffold_record(scaffold_root)
    meds = record.pop("rx-interaction-classes", None)
    if meds:
        profile.setdefault("health_detail", {})["medications"] = meds
    if record:
        profile["record"] = record
    return profile


def _care_messages(profile, conversation, turn_text, *, weight_display=None, weight_pref=None, age_display=None):
    """Build the care-conversation converse payload: the operator's FULL profile + conversation + turn.

    Mirrors `chat._model_messages`'s API-valid shape (every entry role ∈ {user, assistant}, string
    content) but the index-0 context is the operator's FULL care profile (`_care_profile`: the
    identity-safe demographics/goals/genetics + the raw `health_detail`) — so the Care Assistant
    reasons over the operator's actual specifics, not coarse bands. The optional `weight_display` (both
    units) + `weight_pref` (the operator's chosen unit) are added so the assistant talks weight in the
    operator's unit, not kg-only. A malformed conversation entry (not a `{role, content}` dict) is
    SKIPPED, never char-splatted into the payload.
    """
    context = {
        "task": "care-conversation",
        "profile": profile,
        "extractable_fields": _EXTRACTABLE_FIELDS,
        "notes": _PERSISTENCE_NOTE,
    }
    if weight_display:
        context["operator_weight"] = weight_display
    if weight_pref:
        context["operator_weight_unit"] = weight_pref
    if age_display:
        context["operator_age"] = age_display
        # The profile token `training-age-band` is a LEGACY NAME that holds chronological age, not
        # lifting experience — state it so the assistant does not re-ask age-vs-training-years.
        context["profile_glossary"] = {
            "training-age-band": "the operator's chronological age in years (NOT training experience)"
        }
    messages = [{"role": "user", "content": json.dumps(context, sort_keys=True)}]
    if isinstance(conversation, list):
        for turn in conversation:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": turn_text})
    return messages


def respond(turn_text, conversation, *, client, store_root=None, scaffold_root=None, identity_config=None,
            loop_dispatch=None, loop_deid_client=None):
    """Run one Care Assistant conversation turn over the operator's FULL profile; reply + gated capture.

    Re-reads the operator's full care profile server-side (`_care_profile`: identity-safe demographics /
    goals / genetics + the raw health detail; server-authoritative — the client never supplies it),
    builds the converse payload (profile context + conversation + turn),
    makes the ONE no-train model call, and returns `{"reply", "receipt"}`. The care agent WRITES the
    facts it extracted from the operator's turn through the SAME gate the intake chat uses
    (`extract.persist_extraction` -> `capture.persist_capture`): a proposed fact is de-identified by its
    data class, a raw value under a wired token routes record-only, and the receipt reports what actually
    landed. Fail-closed on a failed/empty call (`ModelCallError`) -> an honest degraded reply with an
    empty receipt, 0 fabrication, 0 store write.

    Args:
        turn_text (str): The operator's raw turn this round.
        conversation (list): The prior live conversation turns (`{"role", "content"}`), incl. the
            care-review opening questions the client carried back.
        client: A model client exposing `converse(messages) -> {"reply", "extraction"}` that raises
            `ModelCallError` on a failed/empty call (the one no-train model boundary).
        store_root (str | Path, optional): The instance store root the de-id profile is read from AND
            the gate appends wired tokens into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the gate writes
            record-only values under.
        identity_config (str | Path, optional): The instance operator-identity token config threaded
            into `router.summarize`'s 8j6 PII gate AND the capture gate's free-text PII scan.

    Returns:
        (dict) `{"reply": <assistant reply>, "receipt": {"store", "scaffold", "dropped"}}`, or the
        fail-closed `{"reply": None, "receipt": empty, "degraded": True, "reason": ...}` on a failure.
    """
    store_read = functools.partial(store.read, root=store_root) if store_root is not None else store.read
    profile = _care_profile(store_read, scaffold_root=scaffold_root, identity_config=identity_config)
    messages = _care_messages(
        profile, conversation, turn_text,
        weight_display=_weight_display(profile),
        weight_pref=_weight_unit_preference(scaffold_root),
        age_display=_age_display(profile),
    )
    try:
        result = client.converse(messages)
    except ModelCallError as exc:
        return {"reply": None, "receipt": {"store": [], "scaffold": [], "dropped": []},
                "degraded": True, "reason": str(exc)}
    # Store-write through the SAME gate the intake chat uses: the care agent's proposed facts route
    # through `capture.persist_capture` (de-identify by data class), never a direct/second store path.
    receipt = extract.persist_extraction(
        result.get("extraction"), turn_text, root=store_root,
        scaffold_root=scaffold_root, identity_config=identity_config,
    )
    # A free-text capture completion: notify the plan loop's ONE debounced entry (ADR-0036-T2). Fires
    # only on this non-degraded branch (skipped on the fail-closed `ModelCallError` degrade above).
    # The notify carries only the derived trigger label — never the raw `turn_text` (the finding-C
    # boundary; the debounce reads DERIVED store state). Loop seams threaded by the caller; production
    # server->site threading is ADR-0036-T4. Additive — the `{"reply", "receipt"}` return is unchanged.
    from scripts.serve import plan_loop
    try:
        plan_loop.signal(store_root, trigger=plan_loop.FREE_TEXT_TRIGGER,
                         dispatch=loop_dispatch, deid_client=loop_deid_client)
    except Exception:
        # Fail-open: the loop notify is additive — a derivation/re-gen raise must never break the
        # primary care-chat reply (the capture already persisted; the `{"reply", "receipt"}` return
        # is the contract).
        logging.exception("plan-loop signal failed after care-chat capture (additive; reply unaffected)")
    return {"reply": result.get("reply"), "receipt": receipt}
