"""Conversation->de-identified-store extractor tests (ADR-0017-T1).

`scripts/serve/extract.py`'s `extract_facts` VALIDATES a model extraction proposal
(never trusts it) into `ExtractionResult{candidate_facts, declined_domains, dropped}`,
and `persist_extraction` routes the well-formed `candidate_facts` UNCHANGED through the
EXISTING `capture.persist_capture` gate (the extractor's ONLY store path — it adds no
`store.append` of its own; "model proposes, gate disposes"). The proposal is a crafted
MOCK dict (no live model).

Cycle 1 — AC-1 (gate-at-write: 0 `store.append` in extract.py; the only store path is
`persist_capture`), AC-3/M-2 (malformed input -> empty candidate_facts + dropped, writes
nothing, never raises into the thread, never fabricates a fact), AC-4/M-3 (partial ->
well-formed kept, malformed dropped, the receipt reports what ACTUALLY LANDED so the
next-turn gap-set is computed against the STORE), AC-6 (a FAILED extraction call yields
zero facts vs an empty-from-success — two distinct outcomes).

Cycle 2 — AC-2 (a raw-PII proposal under a wired token routes record-only, NOT the store
item) + the gate-at-write negative control.
"""

import functools
from pathlib import Path

from scripts.plan.router import SUMMARY_FIELD_SET, summarize
from scripts.serve import capture, extract
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# Mirror test_capture.py: an identity config ABSENT on disk so identity-token detection
# is empty (the fresh-clone posture) while value-class patterns (email/phone/postal) run.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def _bound(root):
    """The instance-bound store_read `summarize` requires (recipe caller contract)."""
    return functools.partial(store.read, root=root)


def _summary(root):
    """Run `summarize` over a tmp instance with an absent identity config."""
    return summarize(_bound(root), identity_config=_ABSENT_IDENTITY)


# --------------------------------------------------------------------------- #
# AC-1 — the extractor's ONLY store path is the persist_capture gate
# --------------------------------------------------------------------------- #


def test_extract_module_has_no_store_append():
    """AC-1: scripts/serve/extract.py contains 0 `store.append` (the only store path is the gate).

    The extractor must NOT write the store directly — its sole store path is through
    `capture.persist_capture` (the gate that routes by data class). A direct
    `store.append` in extract.py would bypass the gate; assert the source carries none.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "extract.py").read_text()
    assert "store.append" not in src, (
        "extract.py calls store.append directly — the extractor's only store path must "
        "be capture.persist_capture (the gate); a direct write bypasses it"
    )


def test_persist_extraction_routes_through_the_gate_not_a_direct_write(tmp_path):
    """AC-1: a well-formed proposal lands via `persist_capture`'s receipt, not a direct write.

    Feed a well-formed extraction proposal whose facts are wired de-identified tokens;
    assert they land in the store tagged source:"intake" (proving they went through the
    gate's `store.append`) AND the returned turn receipt carries the `persist_capture`
    `{"store": [...]}` receipt — the extractor's only store path is the gate.
    """
    store_root = tmp_path / "store"
    receipt = extract.persist_extraction(
        {"goal-domains": "Workout;Nutrition", "hard-limits": "no overhead pressing"},
        turn_text="i want to work on strength with no overhead pressing",
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    gd = store.read("goal-domains", root=store_root)
    assert len(gd) == 1 and gd[0]["source"] == "intake", "the fact did not land via the gate's store.append"
    assert gd[0]["value"] == "Workout;Nutrition"
    # The receipt is the persist_capture receipt (what LANDED) plus dropped.
    assert "goal-domains" in receipt["store"] and "hard-limits" in receipt["store"], (
        "the turn receipt does not report the wired tokens persist_capture wrote"
    )
    assert receipt["dropped"] == [], "a well-formed proposal reported dropped fields"


# --------------------------------------------------------------------------- #
# AC-3 / M-2 — malformed input fails soft (empty candidate_facts + dropped)
# --------------------------------------------------------------------------- #


def test_non_dict_proposal_yields_empty_candidate_facts_dropped(tmp_path):
    """AC-3/M-2: a genuinely unparseable proposal -> candidate_facts={}, dropped non-empty.

    A bare string or scalar `model_extraction_output` is unparseable (neither a `{token: value}`
    mapping nor a `[{field, value}]` list): the extractor returns `candidate_facts={}` with the input
    flagged in `dropped`, does NOT raise into the request thread, and writes NOTHING. (A LIST is now a
    valid proposal shape — see `test_list_of_field_value_proposals_normalized`.)
    """
    for bad in ("goal-domains=Workout", 42):
        result = extract.extract_facts(bad, turn_text="anything")
        assert result.candidate_facts == {}, f"an unparseable proposal {bad!r} produced candidate_facts"
        assert result.dropped, f"an unparseable proposal {bad!r} did not report a dropped reason"


def test_list_of_field_value_proposals_normalized(tmp_path):
    """A `[{field, value}]` list (the structured-output shape) is normalized to captured facts.

    The model returns `extraction` as a list of `{"field", "value"}` objects; previously the whole
    list was dropped (`dropped: ['list']`), silently capturing nothing from chat. It is now normalized
    to a `{token: value}` proposal and the well-formed facts are captured. Failing-capable: reds if the
    list is dropped whole again.
    """
    result = extract.extract_facts(
        [{"field": "recovery-status-band", "value": "high"},
         {"field": "goal-priority-order", "value": "strength first"}],
        turn_text="I recover well and my priority is strength",
    )
    assert result.candidate_facts == {"recovery-status-band": "high", "goal-priority-order": "strength first"}
    assert result.dropped == [], f"a well-formed list-of-proposals reported drops: {result.dropped}"


def test_non_dict_proposal_persist_writes_nothing(tmp_path):
    """AC-3/M-2: persisting a non-dict proposal writes NOTHING and never raises.

    `persist_extraction` on a malformed proposal must write no store item and no
    scaffold file, and must not raise into the request thread — the turn captured
    nothing, and the receipt reports an empty store/scaffold plus the dropped reason.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    receipt = extract.persist_extraction(
        "goal-domains=Workout",  # a genuinely unparseable (bare string) proposal
        turn_text="anything", root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )
    assert receipt["store"] == [], "a malformed proposal wrote a store token"
    assert receipt["scaffold"] == [], "a malformed proposal wrote a scaffold record"
    assert receipt["dropped"], "a malformed proposal did not report a dropped reason"
    assert not store_root.exists() or list(store_root.rglob("*.ndjson")) == [], (
        "a malformed proposal wrote a store file"
    )
    assert not scaffold_root.exists() or [p for p in scaffold_root.rglob("*") if p.is_file()] == [], (
        "a malformed proposal wrote a scaffold file"
    )


def test_malformed_proposal_never_fabricates_a_fact(tmp_path):
    """AC-3/M-2: a malformed proposal never invents a candidate fact.

    A non-dict input must not be coerced into a fabricated fact (e.g. parsing a string
    into a token). candidate_facts stays empty — the extractor never guesses.
    """
    result = extract.extract_facts("goal-domains: strength; hard-limits: none", turn_text="t")
    assert result.candidate_facts == {}, "the extractor fabricated a fact from a non-dict string"


# --------------------------------------------------------------------------- #
# AC-4 / M-3 — partial proposal: keep well-formed, drop malformed, receipt = LANDED
# --------------------------------------------------------------------------- #


def test_partial_proposal_keeps_well_formed_drops_malformed(tmp_path):
    """AC-4/M-3: a mixed proposal keeps the well-formed facts and drops the malformed ones.

    A proposal mixing well-formed entries (str token -> scalar value) with malformed
    entries (a non-str key, a non-scalar value) keeps ONLY the well-formed in
    candidate_facts; the malformed land in `dropped`. The extractor never raises on the
    mixed input.
    """
    proposal = {
        "goal-domains": "Workout;Nutrition",        # well-formed wired token
        "hard-limits": "no overhead pressing",       # well-formed wired token
        42: "numeric-key",                           # malformed: non-str key
        "goal-targets": {"nested": "object"},        # malformed: non-scalar value
    }
    result = extract.extract_facts(proposal, turn_text="t")
    assert result.candidate_facts == {
        "goal-domains": "Workout;Nutrition",
        "hard-limits": "no overhead pressing",
    }, "the well-formed facts were not kept verbatim"
    assert set(result.dropped) >= {"42", "goal-targets"} or len(result.dropped) == 2, (
        f"the malformed entries were not all dropped: {result.dropped}"
    )


def test_partial_proposal_receipt_reports_what_landed_in_the_store(tmp_path):
    """AC-4/M-3: the receipt reports what ACTUALLY LANDED + dropped (gap-set vs the STORE).

    Feed a mixed proposal where one well-formed fact is a wired token (lands in the
    store) and one well-formed fact is record-only (lands in the scaffold), plus a
    malformed entry. The receipt's `store`/`scaffold` report what landed (the
    persist_capture receipt) and `dropped` reports the malformed — so the next-turn
    gap-set is computed against the STORE, not the model's claim.

    Each well-formed fact is routed INDEPENDENTLY through the gate (per-field): the
    record-only fact never blocks the wired token from landing.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    proposal = {
        "goal-domains": "Workout;Nutrition",     # wired -> store
        "dietary-pattern": "high protein",       # record-only -> scaffold
        "hard-limits": ["not", "a", "scalar"],   # malformed -> dropped
    }
    receipt = extract.persist_extraction(
        proposal, turn_text="t", root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )
    # What LANDED: the wired token in the store, the record-only in the scaffold.
    assert receipt["store"] == ["goal-domains"], f"store receipt wrong: {receipt['store']}"
    assert "dietary-pattern" in receipt["scaffold"], "the record-only fact is not in the scaffold receipt"
    assert "hard-limits" in receipt["dropped"], "the malformed fact is not in the dropped list"
    # Ground truth: the gap-set is the STORE, not the model's claim — hard-limits never
    # landed, so a next-turn missing-fields against the store still sees it absent.
    assert store.read("hard-limits", root=store_root) == [], (
        "the malformed hard-limits leaked into the store"
    )
    assert store.read("goal-domains", root=store_root), "the well-formed wired token did not land"


# --------------------------------------------------------------------------- #
# AC-6 — a FAILED extraction call vs an empty-from-success (two distinct outcomes)
# --------------------------------------------------------------------------- #


def test_failed_extraction_yields_zero_facts_writes_nothing(tmp_path):
    """AC-6: a FAILED extraction call yields zero facts + writes nothing (never fabricated).

    A failed extraction call (the model client raised / returned the failure sentinel
    `None`) yields zero candidate facts and writes nothing — the extractor never
    fabricates a fact to fill the gap. The result is marked as a failure, distinct from
    an empty-from-success.
    """
    store_root = tmp_path / "store"
    result = extract.extract_facts(None, turn_text="t")
    assert result.candidate_facts == {}, "a failed extraction produced candidate_facts"
    assert result.failed is True, "a failed extraction was not marked failed"
    receipt = extract.persist_extraction(
        None, turn_text="t", root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_ABSENT_IDENTITY,
    )
    assert receipt["store"] == [] and receipt["scaffold"] == [], "a failed extraction wrote something"


def test_empty_from_success_is_a_distinct_valid_outcome(tmp_path):
    """AC-6: an empty proposal from a SUCCESSFUL call is a valid distinct outcome (not a failure).

    An empty dict `{}` from a successful extraction (a turn that captured nothing yet)
    is a VALID outcome: zero candidate facts, but NOT marked failed — distinguishable
    from the failed-call case so the dispatch can tell "the turn captured nothing" from
    "the extraction call failed".
    """
    result = extract.extract_facts({}, turn_text="hello there")
    assert result.candidate_facts == {}, "an empty-from-success produced candidate_facts"
    assert result.failed is False, "an empty-from-success was wrongly marked failed"
    assert result.dropped == [], "an empty-from-success reported dropped fields"


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-2: a raw-PII proposal under a wired token routes record-only
# --------------------------------------------------------------------------- #


def test_raw_pii_proposal_under_wired_token_routes_record_only(tmp_path):
    """AC-2: a model-emitted raw contact value under a free-text wired token -> scaffold, NOT the item.

    A crafted proposal puts a raw contact value (an email) under a free-text wired token
    (`goal-targets`). The gate's full-value PII scan catches it and routes it record-only
    to the gitignored scaffold — it NEVER lands in the model-bound `goal-targets` store
    item. CONCERN-3 NOTE: this asserts identity/contact PII (email) is caught, NOT a
    clinical diagnosis in a free-text token (the accepted V1 residual, excluded).

    Failing-capable: re-add a direct `store.append` bypass in extract.py and the value
    reaches the token, reddening the negative assertion (the negative control below).
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    receipt = extract.persist_extraction(
        {"goal-targets": "add 10 lb to my squat, reach me at operator@example.com"},
        turn_text="t", root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Negative (load-bearing): the raw-PII value never reached the model-bound token item.
    assert store.read("goal-targets", root=store_root) == [], (
        "a raw-PII proposal reached the model-bound goal-targets store item"
    )
    # Positive: it landed record-only in the gitignored scaffold.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "operator@example.com" in scaffold_text, "the raw-PII value did not route record-only"
    assert "goal-targets" in receipt["scaffold"], "the raw-PII fact is not in the scaffold receipt"
    assert "goal-targets" not in receipt["store"], "the raw-PII fact wrongly reported as stored"


def test_raw_phone_proposal_under_wired_token_routes_record_only(tmp_path):
    """AC-2: a model-emitted raw phone value under a free-text wired token -> scaffold, NOT the item.

    A second contact-PII class (a phone number) under `hard-limits` likewise routes
    record-only — the gate catches contact PII regardless of which free-text wired token
    the model mis-classifies it under.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    extract.persist_extraction(
        {"hard-limits": "call me at 555-123-4567 before changing the program"},
        turn_text="t", root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("hard-limits", root=store_root) == [], (
        "a raw phone proposal reached the model-bound hard-limits store item"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "555-123-4567" in scaffold_text, "the raw phone value did not route record-only"


def test_clean_wired_token_proposal_still_lands_in_the_store(tmp_path):
    """AC-2: the gate is selective — a clean wired-token proposal still lands in the store.

    The raw-PII routing must not be a blanket block: a clean de-identified value under a
    wired token still lands in the model-bound store item (proving AC-2 is selective).
    """
    store_root = tmp_path / "store"
    extract.persist_extraction(
        {"goal-targets": "add 10 lb to squat by september"},
        turn_text="t", root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    gt = store.read("goal-targets", root=store_root)
    assert gt and gt[0]["value"] == "add 10 lb to squat by september", (
        "a clean wired-token proposal did not land in the store item"
    )


def test_declined_domains_control_key_populates_field_and_is_not_dropped():
    """The `declined_domains` control key feeds the result field, never the dropped receipt.

    `declined_domains` is a control key, not a fact candidate. A list-valued
    `declined_domains` populates `ExtractionResult.declined_domains` and must NOT appear
    in `dropped` (it is not a malformed fact name) nor in `candidate_facts`. The other
    well-formed facts in the same proposal still pass through.
    """
    result = extract.extract_facts(
        {"declined_domains": ["nutrition", "peptides"], "recovery-status-band": "moderate"},
        turn_text="t",
    )
    assert result.declined_domains == {"nutrition", "peptides"}
    assert "declined_domains" not in result.dropped, (
        "the declined_domains control key was mis-reported as a malformed fact name"
    )
    assert "declined_domains" not in result.candidate_facts
    assert result.candidate_facts == {"recovery-status-band": "moderate"}
