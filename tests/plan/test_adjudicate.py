"""Medical-liaison terminal adjudication gate (`scripts/plan/adjudicate.py`).

Mutation-proof coverage of the two gate invariants:

  - INV-OVERRIDE-RECORD-SCHEMA: an override record clears a hold ONLY when it is content-valid
    (canonical literal, content-bearing operator_reason at the band rung, risks-of-proceeding,
    contradictions-log ref). A presence-only record (the rubber-stamp) is rejected.
  - INV-CRITICAL-NON-OVERRIDABLE: a CRITICAL / H1-H2 finding never gets an override path; an
    envelope that builds one is a violation, not a release.

Deleting either gate makes the corresponding tests go RED (a vacuous override would clear; a
CRITICAL override path would release) — that is the proof.
"""

import json

from scripts.plan import adjudicate

CAUTION = "Supplement<->peptide additive adverse-event risk (shared additive-AE classes: bleeding-risk)"
FINDING_ID = "additive-ae:class:bleeding-risk"


def _override_record(band="HIGH", **overrides):
    """A content-valid override record at `band`, with `overrides` applied last."""
    record = {
        "caution_verbatim": CAUTION,
        "composite_band": band,
        "risks_communicated": {
            "general": "Additive antiplatelet effect raises bleeding risk.",
            "risks_of_proceeding": (
                "Proceeding may cause prolonged bleeding, bruising, or hemorrhage; the combined "
                "antiplatelet load is not offset by home monitoring."
            ),
        },
        "operator_reason": (
            "Recovering a connective-tissue injury under physician follow-up; accepting the "
            "monitored bleeding-risk tradeoff for the recovery benefit."
        ),
        "evidence_tier_required": adjudicate.evidence_tier_required(band),
        "evidence_provided": {
            "rung": "understanding+appreciation+reasoning" if band == "HIGH" else "clear-choice"
        },
        "override_literal": adjudicate.OVERRIDE_LITERAL,
        "voluntariness_note": "Chosen without coercion after the risks were explained.",
        "timestamp": "2026-06-19T10:00:00-04:00",
        "contradictions_log_ref": "vault/meta/contradictions.md#C-088",
    }
    record.update(overrides)
    return record


def _envelope(band="HIGH", harm_class=None, finding_id=FINDING_ID, override="auto", set_by="auto"):
    """A liaison adjudication envelope; `override='auto'` builds a valid record for the band."""
    if override == "auto":
        record = None if adjudicate.is_non_overridable(band, harm_class) else _override_record(band)
    else:
        record = override
    if set_by == "auto":
        set_by = (
            adjudicate.AUTO_BLOCK_SENTINEL
            if adjudicate.is_non_overridable(band, harm_class)
            else adjudicate.LIAISON_SET_BY
        )
    return {
        "finding_id": finding_id,
        "composite_band": band,
        "harm_class": harm_class,
        "verdict": "BLOCK_WITH_OVERRIDE_PATH",
        "severity_final": {"set_by": set_by, "verdict": "BLOCK_WITH_OVERRIDE_PATH"},
        "override_record": record,
    }


def _safety_finding(finding_id=FINDING_ID, caution=CAUTION):
    return {"finding_id": finding_id, "source": "additive-ae", "held_domain": "supplements",
            "caution": caution}


# --- evidence rung + non-overridable predicates --------------------------------


def test_evidence_tier_required_by_band():
    assert adjudicate.evidence_tier_required("MEDIUM") == "clear-choice"
    assert adjudicate.evidence_tier_required("HIGH") == "understanding+appreciation+reasoning"
    assert adjudicate.evidence_tier_required("CRITICAL") is None


def test_is_non_overridable():
    assert adjudicate.is_non_overridable("CRITICAL", None) is True
    assert adjudicate.is_non_overridable("HIGH", "H1") is True
    assert adjudicate.is_non_overridable("MEDIUM", "H2") is True
    assert adjudicate.is_non_overridable("HIGH", "H3") is False
    assert adjudicate.is_non_overridable("MEDIUM", None) is False


# --- validate_override_record (INV-OVERRIDE-RECORD-SCHEMA) ----------------------


def test_valid_high_record_passes():
    valid, reasons = adjudicate.validate_override_record(_override_record("HIGH"), composite_band="HIGH")
    assert valid is True
    assert reasons == []


def test_valid_medium_record_passes():
    valid, reasons = adjudicate.validate_override_record(_override_record("MEDIUM"), composite_band="MEDIUM")
    assert valid is True
    assert reasons == []


def test_vacuous_operator_reason_rejected():
    # The canonical Role-7 rubber-stamp: every field present, but the reason is content-free.
    record = _override_record("HIGH", operator_reason="because I want to try it")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("operator_reason" in r for r in reasons)


def test_short_operator_reason_rejected():
    record = _override_record("HIGH", operator_reason="ok")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("operator_reason" in r for r in reasons)


def test_missing_canonical_literal_rejected():
    record = _override_record("HIGH", override_literal="I accept this risk")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("override_literal" in r for r in reasons)


def test_rung_below_band_rejected():
    # HIGH demands understanding+appreciation+reasoning; a clear-choice rung is below it.
    record = _override_record("HIGH", evidence_provided={"rung": "clear-choice"})
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("rung" in r for r in reasons)


def test_evidence_tier_required_token_must_match_band():
    record = _override_record("HIGH", evidence_tier_required="clear-choice")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("evidence_tier_required" in r for r in reasons)


def test_risks_without_risks_of_proceeding_rejected():
    record = _override_record("HIGH", risks_communicated={"general": "some risk"})
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("risks_of_proceeding" in r for r in reasons)


def test_risks_not_a_dict_rejected():
    record = _override_record("HIGH", risks_communicated="bleeding risk")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("risks_of_proceeding" in r for r in reasons)


def test_band_mismatch_rejected():
    record = _override_record("MEDIUM")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
    assert valid is False
    assert any("does not match" in r for r in reasons)


def test_critical_band_in_record_rejected():
    record = _override_record("HIGH", composite_band="CRITICAL")
    valid, reasons = adjudicate.validate_override_record(record, composite_band="CRITICAL")
    assert valid is False
    assert any("not overridable" in r for r in reasons)


def test_caution_verbatim_mismatch_rejected_when_caution_given():
    record = _override_record("HIGH", caution_verbatim="a paraphrase of the caution")
    valid, reasons = adjudicate.validate_override_record(
        record, composite_band="HIGH", caution=CAUTION
    )
    assert valid is False
    assert any("verbatim" in r for r in reasons)


def test_missing_required_fields_rejected():
    for field in ("contradictions_log_ref", "timestamp", "voluntariness_note", "caution_verbatim"):
        record = _override_record("HIGH")
        del record[field]
        valid, reasons = adjudicate.validate_override_record(record, composite_band="HIGH")
        assert valid is False, field


def test_non_dict_record_rejected():
    valid, reasons = adjudicate.validate_override_record("not-a-record", composite_band="HIGH")
    assert valid is False
    assert reasons


# --- audit_adjudication_envelope (the shared mechanical check) ------------------


def test_audit_valid_high_override_ok():
    ok, violations = adjudicate.audit_adjudication_envelope(_envelope("HIGH"))
    assert ok is True
    assert violations == []


def test_audit_valid_medium_override_ok():
    ok, violations = adjudicate.audit_adjudication_envelope(_envelope("MEDIUM"))
    assert ok is True


def test_audit_high_with_no_override_is_ok_block_stands():
    # A HIGH finding with no override is the honest block-stands state, not a violation.
    ok, violations = adjudicate.audit_adjudication_envelope(
        _envelope("HIGH", override=None, set_by=adjudicate.LIAISON_SET_BY)
    )
    assert ok is True


def test_audit_critical_with_override_path_violates_non_overridable():
    # INV-CRITICAL-NON-OVERRIDABLE: an override path built for a CRITICAL finding is a violation.
    envelope = _envelope("CRITICAL", override=_override_record("HIGH"), set_by=adjudicate.LIAISON_SET_BY)
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-CRITICAL-NON-OVERRIDABLE" for v in violations)


def test_audit_h1_with_override_path_violates_non_overridable():
    envelope = _envelope("HIGH", harm_class="H1", override=_override_record("HIGH"),
                         set_by=adjudicate.LIAISON_SET_BY)
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-CRITICAL-NON-OVERRIDABLE" for v in violations)


def test_audit_h2_with_override_path_violates_non_overridable():
    envelope = _envelope("MEDIUM", harm_class="H2", override=_override_record("MEDIUM"),
                         set_by=adjudicate.LIAISON_SET_BY)
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-CRITICAL-NON-OVERRIDABLE" for v in violations)


def test_audit_critical_autoblock_is_ok():
    ok, violations = adjudicate.audit_adjudication_envelope(_envelope("CRITICAL"))
    assert ok is True


def test_audit_critical_null_override_wrong_set_by_violates():
    envelope = _envelope("CRITICAL", set_by=adjudicate.LIAISON_SET_BY)
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-CRITICAL-NON-OVERRIDABLE" for v in violations)


def test_audit_high_vacuous_override_violates_schema():
    record = _override_record("HIGH", operator_reason="trust me")
    envelope = _envelope("HIGH", override=record)
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-OVERRIDE-RECORD-SCHEMA" for v in violations)


def test_audit_high_override_wrong_set_by_violates_schema():
    envelope = _envelope("HIGH", set_by="orchestrator")
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False
    assert any(v["invariant"] == "INV-OVERRIDE-RECORD-SCHEMA" for v in violations)


def test_audit_unknown_band_violates():
    envelope = _envelope("SEVERE")
    ok, violations = adjudicate.audit_adjudication_envelope(envelope)
    assert ok is False


# --- adjudicate (the terminal outcome the orchestrator applies) -----------------


def test_adjudicate_high_valid_override_clears():
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("HIGH"))
    assert outcome["outcome"] == "cleared"
    assert outcome["non_overridable"] is False
    assert outcome["override_record"] is not None
    assert outcome["reasons"] == []


def test_adjudicate_medium_valid_override_clears():
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("MEDIUM"))
    assert outcome["outcome"] == "cleared"


def test_adjudicate_vacuous_override_block_stands():
    record = _override_record("HIGH", operator_reason="because I want to try it")
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("HIGH", override=record))
    assert outcome["outcome"] == "block-stands"
    assert outcome["override_record"] is None
    assert outcome["reasons"]


def test_adjudicate_critical_autoblock_block_stands_non_overridable():
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("CRITICAL"))
    assert outcome["outcome"] == "block-stands"
    assert outcome["non_overridable"] is True
    assert outcome["reasons"] == [adjudicate.AUTO_BLOCK_SENTINEL]


def test_adjudicate_critical_override_path_rejected_block_stands():
    # INV-CRITICAL-NON-OVERRIDABLE at the gate: a CRITICAL override path never releases.
    envelope = _envelope("CRITICAL", override=_override_record("HIGH"), set_by=adjudicate.LIAISON_SET_BY)
    outcome = adjudicate.adjudicate(_safety_finding(), envelope)
    assert outcome["outcome"] == "block-stands"
    assert outcome["non_overridable"] is True
    assert outcome["override_record"] is None


def test_adjudicate_h1_override_path_rejected():
    envelope = _envelope("HIGH", harm_class="H1", override=_override_record("HIGH"),
                         set_by=adjudicate.LIAISON_SET_BY)
    outcome = adjudicate.adjudicate(_safety_finding(), envelope)
    assert outcome["outcome"] == "block-stands"
    assert outcome["non_overridable"] is True


def test_adjudicate_no_envelope_block_stands():
    outcome = adjudicate.adjudicate(_safety_finding(), None)
    assert outcome["outcome"] == "block-stands"
    assert outcome["override_record"] is None


def test_adjudicate_finding_id_mismatch_block_stands():
    envelope = _envelope("HIGH", finding_id="additive-ae:class:serotonergic")
    outcome = adjudicate.adjudicate(_safety_finding(), envelope)
    assert outcome["outcome"] == "block-stands"
    assert any("finding_id" in r for r in outcome["reasons"])


def test_adjudicate_wrong_set_by_block_stands():
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("HIGH", set_by="orchestrator"))
    assert outcome["outcome"] == "block-stands"


def test_adjudicate_caution_mismatch_block_stands():
    # The override record must reproduce the finding's caution verbatim to clear.
    record = _override_record("HIGH", caution_verbatim="a different caution text entirely")
    outcome = adjudicate.adjudicate(_safety_finding(), _envelope("HIGH", override=record))
    assert outcome["outcome"] == "block-stands"


# --- the --audit-envelope CLI (what the bash audit wraps) -----------------------


def test_cli_audit_valid_envelope_exits_zero(tmp_path):
    path = tmp_path / "valid.json"
    path.write_text(json.dumps(_envelope("HIGH")))
    assert adjudicate._cli(["--audit-envelope", str(path)]) == 0


def test_cli_audit_critical_override_exits_nonzero(tmp_path):
    path = tmp_path / "bad.json"
    envelope = _envelope("CRITICAL", override=_override_record("HIGH"), set_by=adjudicate.LIAISON_SET_BY)
    path.write_text(json.dumps(envelope))
    assert adjudicate._cli(["--audit-envelope", str(path)]) == 1


def test_cli_audit_malformed_json_exits_two(tmp_path):
    # A non-JSON envelope is a could-not-run (exit 2), not a found violation (exit 1) — the F-008
    # exit-code contract the bash wrapper maps to its skipped/FATAL path.
    path = tmp_path / "malformed.json"
    path.write_text("not json {")
    assert adjudicate._cli(["--audit-envelope", str(path)]) == 2
