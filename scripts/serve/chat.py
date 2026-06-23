"""De-identified store-grounded question strategy (ADR-0015-T2).

`plan_next_turn(summary, covered_domains, declined_domains) -> TurnIntent` is the
STRATEGY half of the conversational-intake hybrid: code owns the de-identified gap-set
+ `domain_done` / `intake_complete`; the model (ADR-0016-T1's per-turn dispatch, added
to this same module later) owns phrasing within the gap set. The strategy reads operator
state ONLY through the de-identified `router.summarize` mapping passed in — never the raw
transcript, never the gitignored scaffold (reading raw would cross the crown-jewel PII
boundary). It returns token NAMES, domain names, and booleans (0 raw operator string).

`domain_done` is STORE-grounded + explicit-decline (never a turn count, never a
model-supplied flag — the PF-S87-01 anti-gap): a domain is done when EVERY
`SUMMARY_FIELD_SET` token mapped to it is PRESENT in `summary` (`router.py:411,416` — a
field absent from the summary dict had no backing store readings = not yet captured) OR
the operator declined it. A chat-covered domain whose ADR-0019 token is NOT yet minted
(no mapped `SUMMARY_FIELD_SET` token at all) reports "captured-for-record, not-planned"
(`record_only`) and is NEVER `domain_done` vacuously (Design CONCERN-1).
"""

import functools

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.plan.router import SUMMARY_FIELD_SET
from scripts.serve import extract
from scripts.serve.capture import WIRED_TOKENS
from scripts.store import store

# Chat-covered-domain -> the SUMMARY_FIELD_SET tokens that feed the planner for that
# domain (the design §3.2 integration contract, Form/Chat domain→token table). This is
# the STRUCTURAL grouping (which token belongs to which chat domain); WHICH of these
# tokens are actually live is computed below against the real `SUMMARY_FIELD_SET`, so the
# active map cannot drift from what `summarize` / `capture` mint. A future ADR-0019 token
# added to `SUMMARY_FIELD_SET` joins its domain's tuple here in the same reviewed batch.
#
# At this task's time only the `goals` and `training` tokens are minted; the
# nutrition/supplements/peptides domains have NO minted token (their ADR-0019 tokens are
# Wave B), so they resolve to the empty mapped set -> the CONCERN-1 record-only state.
_DOMAIN_TOKEN_GROUPING = {
    "goals": ("goal-domains", "goal-targets", "goal-priority-order", "hard-limits"),
    "training": ("recovery-status-band", "active-issue-class"),
    "nutrition": (),
    "supplements": (),
    "peptides": (),
}

# The ACTIVE domain -> token map: each grouping tuple filtered to live
# `SUMMARY_FIELD_SET` membership. A token named in the grouping but absent from the
# field set is dropped here (and tripped at load below), so the strategy's gap-set is
# derived from the live surface, never a hand-copied literal. A domain whose active
# tuple is empty is a record-only (unminted) domain — CONCERN-1.
_DOMAIN_TOKENS = {
    domain: tuple(t for t in tokens if t in SUMMARY_FIELD_SET)
    for domain, tokens in _DOMAIN_TOKEN_GROUPING.items()
}

# The chat-covered domain set — the control-surface universe `covered_domains` /
# `declined_domains` / `target_domain` members must come from (AC-5 fail-loud bound).
CHAT_DOMAINS = frozenset(_DOMAIN_TOKEN_GROUPING)

# Change-control tripwire (mirrors router.py / capture.py disjointness asserts): every
# token a domain maps to a LIVE field-set member must trace to one the capture surface
# can actually mint — a wired token or the `active-issue-class` derivation — so a future
# grouping edit naming a non-mintable token reds at import, not silently at runtime.
_MINTABLE_TOKENS = set(WIRED_TOKENS) | {"active-issue-class"}
assert all(
    set(tokens) <= _MINTABLE_TOKENS for tokens in _DOMAIN_TOKENS.values()
), (
    "chat._DOMAIN_TOKENS maps a domain to a SUMMARY_FIELD_SET token the capture surface "
    "cannot mint — re-ground the domain grouping against WIRED_TOKENS / the derivations"
)


class TurnIntent:
    """The de-identified next-turn intent the question loop drives (frozen contract).

    Carries token NAMES, domain names, and booleans only — 0 raw operator string. The
    consumer (`ADR-0016-T1`'s per-turn dispatch) reads `target_domain` to pick the next
    question and `missing_fields` to bound the gap; `intake_complete` ends the loop.

    Attributes:
        target_domain (str | None): The next open planner-feeding chat domain to ask
            about, or None when no askable gap remains.
        missing_fields (tuple): The `target_domain`'s SUMMARY_FIELD_SET tokens not yet
            present in `summary` (`⊆ SUMMARY_FIELD_SET`); empty when no domain remains.
        domain_done (bool): The loop's done-verdict — True only when no open gap remains
            AND at least one covered domain reached a genuine planner-feeding done;
            never True for a purely record-only resolution (the CONCERN-1 anti-gap).
        intake_complete (bool): Whether no askable gap remains — the loop may terminate.
            Can be True while `domain_done` is False when the only covered domains are
            record-only (resolved-for-record, never silently dropped).
        record_only (tuple): The covered chat domains captured-for-record but not
            planner-feeding (no minted SUMMARY_FIELD_SET token) — CONCERN-1.
    """

    __slots__ = (
        "target_domain", "missing_fields", "domain_done", "intake_complete",
        "record_only",
    )

    def __init__(
        self, target_domain, missing_fields, domain_done, intake_complete, record_only,
    ):
        self.target_domain = target_domain
        self.missing_fields = missing_fields
        self.domain_done = domain_done
        self.intake_complete = intake_complete
        self.record_only = record_only


class MalformedControlError(ValueError):
    """A control input outside the chat-covered contract (fail-loud, never silent)."""


def _missing_fields(summary, domain):
    """The domain's live SUMMARY_FIELD_SET tokens absent from the de-identified summary.

    A token is "present" iff it is a key of `summary` (`router.summarize` omits a field
    whose backing store item had no readings — `router.py:411,416`). The result is a
    subset of `SUMMARY_FIELD_SET` (token names only, 0 raw operator string).
    """
    return tuple(t for t in _DOMAIN_TOKENS[domain] if t not in summary)


def plan_next_turn(summary, covered_domains, declined_domains):
    """Compute the de-identified next-turn gap-set from the store-grounded summary.

    Reads operator-capture state ONLY through the de-identified `summary` mapping (the
    `router.summarize` output the caller binds to the instance root and passes in) — no
    raw transcript, no scaffold, no model call. Per covered chat domain it computes the
    `missing_fields` gap (its live SUMMARY_FIELD_SET tokens absent from `summary`) and
    `domain_done` = no missing tokens OR declined — store-grounded + explicit-decline,
    NEVER a turn count or a model say-so flag (the PF-S87-01 anti-gap). A covered domain
    with NO minted SUMMARY_FIELD_SET token is record-only (captured-for-record,
    not-planned) and never counts toward `domain_done` vacuously (CONCERN-1).
    `target_domain` is the next not-done planner-feeding domain; `intake_complete` is
    true only when every covered domain is done (captured, declined, or record-only).

    Args:
        summary (dict): The de-identified `router.summarize` mapping (field name ->
            de-identified token). A field absent from it had no backing store readings.
        covered_domains (set): The chat domains touched this session (⊆ CHAT_DOMAINS).
        declined_domains (set): The chat domains the operator explicitly declined
            (⊆ covered_domains).

    Returns:
        (TurnIntent) The de-identified next-turn intent (token/domain names + booleans).

    Raises:
        MalformedControlError: When `summary` is not a dict, a covered/declined member
            is outside CHAT_DOMAINS, or `declined_domains ⊄ covered_domains` — fail-loud,
            never a silent corruption of loop termination.
    """
    if not isinstance(summary, dict):
        raise MalformedControlError(
            f"plan_next_turn: summary must be a dict, got {type(summary).__name__}"
        )
    covered = set(covered_domains)
    declined = set(declined_domains)
    out_of_set = (covered | declined) - CHAT_DOMAINS
    if out_of_set:
        raise MalformedControlError(
            f"plan_next_turn: domain(s) {sorted(out_of_set)} outside the chat-covered "
            f"set {sorted(CHAT_DOMAINS)}"
        )
    if not declined <= covered:
        raise MalformedControlError(
            f"plan_next_turn: declined_domains {sorted(declined - covered)} not a "
            f"subset of covered_domains"
        )

    # A record-only domain has no minted planner-feeding token: it is captured for the
    # operator's record but cannot be `domain_done` (CONCERN-1) and is not asked again.
    record_only = tuple(
        sorted(d for d in covered if not _DOMAIN_TOKENS[d] and d not in declined)
    )
    record_only_set = set(record_only)

    # The planner-feeding domains (a minted token mapped) that are NOT yet done: every
    # mapped token present, or declined, closes a domain. A record-only domain is never
    # a target (nothing to ask) and never gates `domain_done`.
    open_domains = sorted(
        d for d in covered
        if d not in declined
        and d not in record_only_set
        and _missing_fields(summary, d)
    )
    target_domain = open_domains[0] if open_domains else None
    missing_fields = _missing_fields(summary, target_domain) if target_domain else ()

    # A planner-feeding domain is GENUINELY done when it is covered, planner-feeding (a
    # minted token mapped), not open, and not record-only — captured to completion or
    # explicitly declined. CONCERN-1: a record-only (unminted) domain is NEVER counted
    # here, so it can never make `domain_done` true vacuously.
    genuinely_done = any(
        d not in open_domains and d not in record_only_set
        for d in covered
    )

    # `domain_done` describes the loop's done-verdict: True only when there is no open
    # gap AND at least one covered domain reached a genuine planner-feeding done — never
    # for a purely record-only resolution (the PF-S87-01 anti-gap). `intake_complete`
    # ends the loop when no askable gap remains (record-only domains are resolved for the
    # record, not silently dropped); it can be True while `domain_done` is False when the
    # only covered domains are record-only.
    intake_complete = not open_domains
    domain_done = not open_domains and genuinely_done

    return TurnIntent(
        target_domain=target_domain,
        missing_fields=missing_fields,
        domain_done=domain_done,
        intake_complete=intake_complete,
        record_only=record_only,
    )


def _progress(intent):
    """The intake-progress state for the turn receipt — token/domain names + booleans only.

    A de-identified view of the `TurnIntent` (0 raw operator string): the consumer
    (`ADR-0017-T2`) reads `target_domain`/`missing_fields` to drive the next question and
    `intake_complete`/`domain_done` to end the loop.
    """
    return {
        "target_domain": intent.target_domain,
        "missing_fields": list(intent.missing_fields),
        "domain_done": intent.domain_done,
        "intake_complete": intent.intake_complete,
        "record_only": list(intent.record_only),
    }


def _model_messages(conversation, turn_text, intent):
    """Build the `converse` payload: the live conversation (raw) + the de-identified context.

    The single-egress-class boundary (NFR-1, ADR-0016 Falsification: any raw egress OTHER
    than the live conversation is release-blocking): the payload carries the live
    conversation turns (raw — the operator authored them this session) plus a de-identified
    CONTEXT turn, and NOTHING ELSE. The context is the `TurnIntent` STRUCTURE — token NAMES
    (`missing_fields`), domain NAMES (`target_domain`/`record_only`), and booleans — NEVER
    a raw store VALUE. The `router.summarize` mapping passes RAW free-text through for its
    free-text fields (`goal-targets`/`goal-priority-order`/`hard-limits` — `router.py:417`),
    so the raw summary values are deliberately NOT placed on the wire; only the gap-set
    NAMES the model needs to phrase the next question are. 0 store-reading content, 0 other
    operator's transcript.

    Args:
        conversation (list): The live conversation turns (`{"role", "content"}`), raw.
        turn_text (str): The current operator turn (appended as the latest user turn).
        intent (TurnIntent): The de-identified next-turn intent (names + booleans only).

    Returns:
        (list) The `converse` messages: the de-identified context turn, the prior
        conversation, then the current operator turn.
    """
    context = {
        "target_domain": intent.target_domain,
        "missing_fields": list(intent.missing_fields),
        "record_only": list(intent.record_only),
        "domain_done": intent.domain_done,
        "intake_complete": intent.intake_complete,
    }
    messages = [{"role": "system", "content": context}]
    messages.extend(conversation)
    messages.append({"role": "user", "content": turn_text})
    return messages


def _degraded_turn(reason):
    """The fail-closed degraded turn: no reply, no fact, no store write (NFR-2).

    A failed/timed-out/rate-limited/empty model call returns this — the failure is
    surfaced honestly, the operator degrades toward the demographic form, and NOTHING is
    fabricated or written. The empty receipt is the proof the turn wrote nothing.
    """
    return {
        "reply": None,
        "receipt": {"store": [], "scaffold": [], "dropped": []},
        "progress": None,
        "degraded": True,
        "degrade_to": "form",
        "reason": reason,
    }


def dispatch_turn(turn_text, conversation, covered_domains, declined_domains, *,
                  client, store_root=None, scaffold_root=None, identity_config=None):
    """Run one `/chat` turn: plan -> converse -> extract -> persist -> per-turn receipt.

    The thin per-turn chain (ADR-0016-T1): build the de-identified `router.summarize`
    context over the instance-bound store read, plan the gap-set (`plan_next_turn`), make
    the ONE outbound model call (`client.converse`, the only egress — carrying the live
    conversation raw + the de-identified context, 0 store content), validate the model's
    extraction proposal and route the well-formed facts through the UNCHANGED gate via the
    shared `extract.persist_extraction` helper (`..., identity_config=...` — the `/chat`
    half of the H-2 dual-call-site wiring), and return the per-turn receipt (assistant
    reply + the `persist_extraction` `{store,scaffold,dropped}` receipt + the de-identified
    progress). The extractor runs EACH
    turn, so the next-turn gap-set is computed against what LANDED in the store, not the
    model's claim (CONCERN-2). A failed/empty model call (the client's `ModelCallError`)
    returns the fail-closed degraded turn: no reply, no fact, 0 store write (NFR-2).

    Args:
        turn_text (str): The operator's raw turn this round.
        conversation (list): The prior live conversation turns (`{"role", "content"}`).
        covered_domains (set | list): The chat domains touched this session.
        declined_domains (set | list): The chat domains the operator declined.
        client: A model client exposing `converse(messages) -> {"reply", "extraction"}`
            that raises `ModelCallError` on a failed/empty call (the one model boundary).
        store_root (str | Path, optional): The instance store root the summary reads from
            and the capture gate appends wired tokens into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the gate
            writes record-only values under.
        identity_config (str | Path, optional): The instance operator-identity token config
            threaded into the capture gate's PII scan (the H-2 instance config).

    Returns:
        (dict) The per-turn receipt: `{"reply", "receipt": {"store","scaffold","dropped"},
        "progress", "degraded": False}`, or the fail-closed degraded turn on a model
        failure (`{"reply": None, "receipt": empty, "degraded": True, "degrade_to":
        "form", ...}`).

    Raises:
        MalformedControlError: A control input outside the chat-covered contract
            (`plan_next_turn`'s fail-loud) — the caller catches it for thread survival.
    """
    store_read = (
        functools.partial(store.read, root=store_root) if store_root is not None
        else store.read
    )
    if identity_config is not None:
        summary = router.summarize(store_read, identity_config=identity_config)
    else:
        summary = router.summarize(store_read)
    intent = plan_next_turn(summary, covered_domains, declined_domains)

    messages = _model_messages(conversation, turn_text, intent)
    try:
        result = client.converse(messages)
    except ModelCallError as exc:
        # Fail-closed (NFR-2): no fabricated reply/fact, no store write on this turn.
        return _degraded_turn(str(exc))

    # The extractor runs THIS turn over the model's proposal; the well-formed facts route
    # UNCHANGED through the capture gate (which de-identifies by data class). Calling the
    # shared `extract.persist_extraction` helper (validate -> route -> {store,scaffold,
    # dropped} receipt) instead of re-implementing the chain keeps the `/chat` path from
    # drifting if the helper's routing changes; it threads identity_config — the H-2
    # dual-call-site wiring (NOTE-ARCH-1).
    receipt = extract.persist_extraction(
        result["extraction"], turn_text, root=store_root, scaffold_root=scaffold_root,
        identity_config=identity_config,
    )
    return {
        "reply": result["reply"],
        "receipt": receipt,
        "progress": _progress(intent),
        "degraded": False,
    }
