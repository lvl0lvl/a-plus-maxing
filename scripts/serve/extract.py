"""Conversation->de-identified-store extractor (ADR-0017-T1; model proposes, gate disposes).

`extract_facts(model_extraction_output, turn_text)` VALIDATES a model extraction
proposal — it never trusts it — into an `ExtractionResult`. The well-formed
`candidate_facts` are then routed UNCHANGED through the EXISTING
`capture.persist_capture` gate by `persist_extraction`, the extractor's ONLY store
path: it makes no direct store write of its own, so a model-emitted raw value under a
wired token routes record-only by the gate's own by-data-class logic, never silently
into a `SUMMARY_FIELD_SET` store item. The proposal is the structured output of the
`ADR-0015-T1` client's `converse(...)`; this module is the first model-output-trusting
surface, so the validation is fail-soft:

- A non-dict / unparseable proposal -> `candidate_facts={}` + `dropped`, writes nothing,
  NEVER raises into the request thread, NEVER fabricates a fact (M-2).
- A partial proposal -> the well-formed entries (a `str` token name -> a scalar value)
  stay in `candidate_facts`, the malformed entries land in `dropped`; each well-formed
  fact is routed INDEPENDENTLY through the gate (M-3). The turn receipt reports what
  ACTUALLY LANDED (the `persist_capture` `{"store": [...], "scaffold": [...]}` receipt)
  PLUS `dropped`, so the next-turn gap-set is computed against the STORE, not the
  model's claim.
- A FAILED extraction call (the client raised / returned the `None` failure sentinel)
  -> zero facts, writes nothing, `failed=True` — distinct from an empty proposal `{}`
  from a SUCCESSFUL call (a turn that captured nothing yet, `failed=False`), a valid
  outcome (M-2 / ADR-0015 fail-closed).
"""

from dataclasses import dataclass, field

from scripts.serve import capture

# A scalar value the gate can route (the store reading's `value` is a scalar). A
# non-scalar value under a token name is a malformed proposal entry -> dropped.
_SCALAR_TYPES = (str, int, float, bool)


@dataclass
class ExtractionResult:
    """The validated outcome of one model extraction proposal (NAMED CONTRACT, ADR-0017-T1).

    Attributes:
        candidate_facts (dict): The well-formed `str token -> scalar value` facts the
            extractor will route through the gate. Empty for a malformed/failed/empty
            proposal.
        declined_domains (set): Domains the model declined to extract this turn (a
            pass-through of the proposal's declared declines; empty when none).
        dropped (list): The names (stringified) of proposal entries dropped as malformed
            — a non-str key, a non-scalar value, or an unparseable proposal.
        failed (bool): True when the extraction CALL failed (client raised / returned the
            `None` sentinel) — distinct from an empty-from-success (`failed=False`).
    """

    candidate_facts: dict = field(default_factory=dict)
    declined_domains: set = field(default_factory=set)
    dropped: list = field(default_factory=list)
    failed: bool = False


def extract_facts(model_extraction_output, turn_text):
    """Validate a model extraction proposal into an `ExtractionResult` (never trusts it).

    A non-dict / unparseable proposal yields `candidate_facts={}` + `dropped`, never
    raises, never fabricates a fact. A partial proposal keeps the well-formed entries
    (str token -> scalar value) and lists the malformed in `dropped`. The `None` failure
    sentinel marks `failed=True` with zero facts; an empty dict from a successful call is
    a valid distinct outcome (`failed=False`).

    Args:
        model_extraction_output (dict | None | Any): The model's structured extraction
            proposal — a `{token: value}` dict, the `None` failure sentinel, or (defended
            against) any other non-dict shape.
        turn_text (str): The operator turn the proposal was extracted from (carried for
            the dispatch's context; not parsed here — the extractor never re-derives facts
            from the raw turn, only validates the model's proposal).

    Returns:
        (ExtractionResult) The validated proposal.
    """
    if model_extraction_output is None:
        # The ADR-0015 fail-closed sentinel: the extraction CALL failed. Zero facts,
        # writes nothing downstream, never a fabricated fact — and marked failed so the
        # dispatch tells it apart from an empty-from-success.
        return ExtractionResult(failed=True)
    if not isinstance(model_extraction_output, dict):
        # Unparseable (a list, a string, a scalar): the whole proposal is dropped. Never
        # coerce it into a fabricated fact — the extractor only validates a dict proposal.
        return ExtractionResult(dropped=[type(model_extraction_output).__name__])

    candidate_facts = {}
    dropped = []
    for name, value in model_extraction_output.items():
        if isinstance(name, str) and isinstance(value, _SCALAR_TYPES):
            candidate_facts[name] = value
        else:
            dropped.append(str(name))

    declined = model_extraction_output.get("declined_domains")
    declined_domains = set(declined) if isinstance(declined, (list, set, tuple)) else set()
    # `declined_domains` is a control key, not a captured fact — strip it from the facts.
    candidate_facts.pop("declined_domains", None)

    return ExtractionResult(
        candidate_facts=candidate_facts,
        declined_domains=declined_domains,
        dropped=dropped,
    )


def persist_extraction(model_extraction_output, turn_text, *, root=None,
                       scaffold_root=None, identity_config=None):
    """Validate a proposal and route the well-formed facts through the gate (only store path).

    Validates via `extract_facts`, then routes the well-formed `candidate_facts`
    UNCHANGED through `capture.persist_capture` (the gate that routes each fact by its
    data class — a raw value under a wired token routes record-only, never into the
    token's store item). This is the extractor's ONLY store path: it makes no direct
    store write of its own. The turn receipt is the `persist_capture`
    `{"store": [...], "scaffold": [...]}` receipt (what ACTUALLY LANDED) plus the
    `dropped` list, so the dispatch computes the next-turn gap-set against the STORE.

    A malformed / failed / empty proposal routes nothing (the gate is handed an empty
    facts dict) — the receipt reports an empty store/scaffold plus `dropped`.

    Args:
        model_extraction_output (dict | None | Any): The model's extraction proposal.
        turn_text (str): The operator turn the proposal was extracted from.
        root (str | Path, optional): The store root the gate appends wired tokens into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the gate
            writes record-only values under.
        identity_config (str | Path, optional): The operator-identity token config the
            gate's free-text PII scan uses (the H-2 instance config).

    Returns:
        (dict) `{"store": [tokens written], "scaffold": [record-only names], "dropped":
        [malformed names]}` — the turn receipt the dispatch re-renders the gap-set against.
    """
    result = extract_facts(model_extraction_output, turn_text)
    receipt = capture.persist_capture(
        result.candidate_facts, root=root, scaffold_root=scaffold_root,
        identity_config=identity_config,
    )
    return {
        "store": receipt["store"],
        "scaffold": receipt["scaffold"],
        "dropped": result.dropped,
    }
