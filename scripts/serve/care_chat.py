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
cannot inject a forged profile. It captures NOTHING — a conversation, not an intake turn; persisting
the operator's answers back into structured store items is a documented follow-on, not this module.
"""

import functools
import json

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.store import store


def _care_messages(summary, conversation, turn_text):
    """Build the care-conversation converse payload: de-id profile context + conversation + turn.

    Mirrors `chat._model_messages`'s API-valid shape (every entry role ∈ {user, assistant}, string
    content) but the index-0 context is the FULL de-identified profile (`router.summarize`) rather than
    the intake gap-set — so the Care Assistant reasons over the whole profile. A malformed conversation
    entry (not a `{role, content}` dict) is SKIPPED, never char-splatted into the payload.
    """
    context = {"task": "care-conversation", "profile": summary}
    messages = [{"role": "user", "content": json.dumps(context, sort_keys=True)}]
    if isinstance(conversation, list):
        for turn in conversation:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": turn_text})
    return messages


def respond(turn_text, conversation, *, client, store_root=None, identity_config=None):
    """Run one Care Assistant conversation turn over the de-identified profile; return the reply.

    Re-reads the de-identified `router.summarize` profile server-side (server-authoritative — the client
    never supplies the profile), builds the converse payload (profile context + conversation + turn),
    makes the ONE no-train model call, and returns `{"reply": ...}`. Fail-closed on a failed/empty call
    (`ModelCallError`) -> an honest degraded reply (`{"reply": None, "degraded": True, "reason": ...}`),
    0 fabrication. Captures nothing — the operator's answer is not written to the store (a follow-on).

    Args:
        turn_text (str): The operator's raw turn this round.
        conversation (list): The prior live conversation turns (`{"role", "content"}`), incl. the
            care-review opening questions the client carried back.
        client: A model client exposing `converse(messages) -> {"reply", ...}` that raises
            `ModelCallError` on a failed/empty call (the one no-train model boundary).
        store_root (str | Path, optional): The instance store root the de-id profile is read from.
        identity_config (str | Path, optional): The instance operator-identity token config threaded
            into `router.summarize`'s 8j6 PII gate.

    Returns:
        (dict) `{"reply": <assistant reply>}`, or the fail-closed `{"reply": None, "degraded": True,
        "reason": ...}` on a model failure.
    """
    store_read = functools.partial(store.read, root=store_root) if store_root is not None else store.read
    if identity_config is not None:
        summary = router.summarize(store_read, identity_config=identity_config)
    else:
        summary = router.summarize(store_read)
    messages = _care_messages(summary, conversation, turn_text)
    try:
        result = client.converse(messages)
    except ModelCallError as exc:
        return {"reply": None, "degraded": True, "reason": str(exc)}
    return {"reply": result.get("reply")}
