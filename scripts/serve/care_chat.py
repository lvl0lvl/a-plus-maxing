"""Profile-aware Care Assistant conversation (the continuous post-unlock care chat).

Distinct from `chat.dispatch_turn` (the PRE-unlock intake elicitation, which carries only the
de-identified gap-set and extracts facts). This is the POST-unlock care conversation: it re-reads the
de-identified `router.summarize` profile server-side each turn and carries it as context, so the Care
Assistant reasons over the operator's FULL (de-identified) profile and the conversation stays coherent
— the care-review clarifying questions are the conversation's opening turns, carried back in
`conversation`, so a reply continues them instead of restarting.

Boundary (ADR-0016): ONE `converse` call over the no-train lane, carrying the de-identified profile
(0 raw PII — `router.summarize` de-identifies) + the live conversation (the operator's own words, the
SAME egress class `chat.dispatch_turn` already sends over the no-train lane) + the current turn, and
NOTHING else. The profile is SERVER-derived each turn (the client never supplies it), so a client
cannot inject a forged profile.

Store-write: the care agent WRITES the facts the operator states back to the store through the EXACT
SAME gated path the intake chat uses — `extract.persist_extraction` -> `capture.persist_capture` — so a
model-proposed fact is de-identified BY DATA CLASS by the gate (a raw value under a wired token routes
record-only; the free-text PII scan backstops), NEVER a new store path or a new egress. The model
PROPOSES, the gate DISPOSES; the receipt reports what ACTUALLY LANDED. The extraction coverage/quality
is the model's job (runtime, the same as the intake extractor); this module supplies the gated wiring.
"""

import functools
import json

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.serve import extract
from scripts.store import store


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


def _care_messages(summary, conversation, turn_text, *, weight_display=None, weight_pref=None):
    """Build the care-conversation converse payload: de-id profile context + conversation + turn.

    Mirrors `chat._model_messages`'s API-valid shape (every entry role ∈ {user, assistant}, string
    content) but the index-0 context is the FULL de-identified profile (`router.summarize`) rather than
    the intake gap-set — so the Care Assistant reasons over the whole profile. The optional
    `weight_display` (both units) + `weight_pref` (the operator's chosen unit) are added so the
    assistant talks weight in the operator's unit, not kg-only. A malformed conversation entry (not a
    `{role, content}` dict) is SKIPPED, never char-splatted into the payload.
    """
    context = {"task": "care-conversation", "profile": summary}
    if weight_display:
        context["operator_weight"] = weight_display
    if weight_pref:
        context["operator_weight_unit"] = weight_pref
    messages = [{"role": "user", "content": json.dumps(context, sort_keys=True)}]
    if isinstance(conversation, list):
        for turn in conversation:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": turn_text})
    return messages


def respond(turn_text, conversation, *, client, store_root=None, scaffold_root=None, identity_config=None):
    """Run one Care Assistant conversation turn over the de-identified profile; reply + gated capture.

    Re-reads the de-identified `router.summarize` profile server-side (server-authoritative — the client
    never supplies the profile), builds the converse payload (profile context + conversation + turn),
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
    if identity_config is not None:
        summary = router.summarize(store_read, identity_config=identity_config)
    else:
        summary = router.summarize(store_read)
    messages = _care_messages(
        summary, conversation, turn_text,
        weight_display=_weight_display(summary),
        weight_pref=_weight_unit_preference(scaffold_root),
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
    return {"reply": result.get("reply"), "receipt": receipt}
