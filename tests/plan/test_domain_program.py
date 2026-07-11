"""Conformance tests for the uniform seven-field DOMAIN PROGRAM schema
(`scripts/plan/domain_program.py`).

Every fixture is a SYNTHETIC literal -- a generic "training domain program" and a
generic "compound domain program". No real operator data, no model client, no
network: the module is pure stdlib and the tests run offline (AC-6).

The load-bearing property is FAIL-CLOSED conformance: an under-delivered program
(missing required field, unclassifiable domain kind, a compound program with no
autoregulation or no labs, a monitoring signal with no validity tier) is REJECTED
via `DomainProgramError` -- an honest no-plan state, never a degraded static plan
(ADR-0041 Consequences-Negative-4).

Fixture convention mirrors `tests/plan/test_adjudicate.py`: `_training_program` /
`_compound_program` return a canonical VALID program dict, then `.update(overrides)`
(or a single key-deletion) mutates exactly ONE field per negative test.
"""

import pytest

from scripts.plan import domain_program


# --- fixture builders (canonical-valid program + single-field mutation) ---------


def _training_program(**overrides):
    """A canonical VALID pure-training seven-field program; `overrides` applied last."""
    program = {
        "domain_kind": "training",
        "prescription": [
            {"phase": "accumulation", "start": "2026-07-01", "end": "2026-07-28",
             "sessions_per_week": 4},
        ],
        "rationale": [
            {"claim": "Progressive overload drives hypertrophy.",
             "certainty_of_evidence": "high",
             "strength_of_recommendation": "strong",
             "causality": "causal"},
        ],
        "monitoring_signals": [
            {"signal": "session_rpe", "validity_tier": "high"},
        ],
        "adjustment_rules": [
            {"when": "two consecutive sessions RPE > 9", "then": "deload 10%"},
        ],
        "required_labs": [],  # empty-OK for a pure-training domain
        "refusal_escalation": {"threshold_event": "acute joint pain",
                               "action": "hold_and_escalate"},
        "cross_domain_seams": [
            {"paired_domain": "nutrition", "seam_nature": "route"},
        ],
    }
    program.update(overrides)
    return program


def _compound_program(**overrides):
    """A canonical VALID compound-domain seven-field program; `overrides` applied last."""
    program = {
        "domain_kind": "compound",
        "prescription": [
            {"phase": "titration", "start": "2026-07-01", "end": "2026-07-14", "dose": "low"},
        ],
        "rationale": [
            {"claim": "Compound supports connective-tissue repair.",
             "certainty_of_evidence": "moderate",
             "strength_of_recommendation": "conditional",
             "causality": "associational"},
        ],
        "monitoring_signals": [
            {"signal": "fasting_glucose", "validity_tier": "high"},
            {"signal": "resting_hr", "validity_tier": "moderate"},
        ],
        "adjustment_rules": [
            {"when": "fasting_glucose above threshold", "then": "hold and re-lab"},
        ],
        "required_labs": ["fasting_glucose", "lipid_panel"],  # mandatory + non-empty for compound
        "refusal_escalation": {"threshold_event": "out-of-range lab",
                               "action": "hold_on_human_gate"},
        "cross_domain_seams": [
            {"paired_domain": "training", "seam_nature": "hold"},
        ],
    }
    program.update(overrides)
    return program


# --- AC-1: seven-field conformance across >=2 domains ---------------------------


def test_conformant_training_and_compound_validate():
    """A conformant training program and a conformant compound program both validate."""
    assert domain_program.validate(_training_program()) is None
    assert domain_program.validate(_compound_program()) is None


def test_missing_required_count_zero_for_conformant():
    """Conformant programs report zero missing required fields."""
    assert domain_program.missing_required_fields(_training_program()) == []
    assert domain_program.missing_required_fields(_compound_program()) == []


# --- AC-2: required-field omission -> typed error naming the field (falsifier) ---


@pytest.mark.parametrize(
    "field", ["prescription", "rationale", "monitoring_signals", "adjustment_rules"]
)
def test_omitting_any_required_field_rejects_and_names_it(field):
    """Deleting any ONE required field is rejected; the error names it structurally."""
    program = _training_program()
    del program[field]
    assert field in domain_program.missing_required_fields(program)
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == field


# --- AC-2(kind): missing / non-vocabulary domain kind -> reject (fail-closed) ----


def test_missing_kind_rejects():
    """A program with the domain-kind attribute deleted fails closed (cannot classify)."""
    program = _compound_program()
    del program[domain_program.KIND_FIELD]
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == domain_program.KIND_FIELD


def test_nonvocabulary_kind_rejects():
    """A domain kind outside DOMAIN_KINDS fails closed rather than defaulting."""
    program = _compound_program()
    program[domain_program.KIND_FIELD] = "not-a-real-kind"
    assert "not-a-real-kind" not in domain_program.DOMAIN_KINDS
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == domain_program.KIND_FIELD


# --- AC-3: required-vs-conditional partition, domain-kind-driven (KIND-CONTRAST) -


def test_training_empty_labs_validates():
    """Empty required_labs is legitimate for a pure-training domain."""
    assert domain_program.validate(_training_program(required_labs=[])) is None


def test_compound_empty_labs_rejects():
    """The kind-contrast pair-mate: same field-state ([]), opposite verdict for compound."""
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(_compound_program(required_labs=[]))
    assert exc.value.offending_field == "required_labs"


def test_compound_absent_labs_rejects():
    """A compound program with required_labs absent (key deleted) is rejected."""
    program = _compound_program()
    del program["required_labs"]
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == "required_labs"


# --- AC-4: autoregulation-required for compound (fail-closed falsifier) ----------


def test_compound_zero_monitoring_signals_rejected():
    """A compound program with no monitoring signals is rejected, naming the field."""
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(_compound_program(monitoring_signals=[]))
    assert exc.value.offending_field == "monitoring_signals"


def test_compound_zero_adjustment_rules_rejected():
    """A compound program with no adjustment rules is rejected, naming the field."""
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(_compound_program(adjustment_rules=[]))
    assert exc.value.offending_field == "adjustment_rules"


def test_compound_with_autoregulation_validates():
    """Positive contrast: a compound program with autoregulation present validates."""
    assert domain_program.validate(_compound_program()) is None


# --- AC-5: validity tier on EVERY monitoring signal (per-entry, not first-only) --


def test_monitoring_signal_missing_tier_rejected():
    """A later monitoring-signal entry with no validity tier is rejected (per-entry)."""
    good = {"signal": "fasting_glucose", "validity_tier": "high"}
    bad = {"signal": "resting_hr"}  # no validity tier
    program = _compound_program(monitoring_signals=[good, bad])
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == "monitoring_signals"
    assert exc.value.offending_signal == bad


def test_monitoring_signal_nonvocabulary_tier_rejected():
    """A later entry whose validity tier is outside VALIDITY_TIERS is rejected (per-entry)."""
    good = {"signal": "fasting_glucose", "validity_tier": "high"}
    bad = {"signal": "resting_hr", "validity_tier": "not-a-real-tier"}
    assert "not-a-real-tier" not in domain_program.VALIDITY_TIERS
    program = _compound_program(monitoring_signals=[good, bad])
    with pytest.raises(domain_program.DomainProgramError) as exc:
        domain_program.validate(program)
    assert exc.value.offending_field == "monitoring_signals"
    assert exc.value.offending_signal == bad
