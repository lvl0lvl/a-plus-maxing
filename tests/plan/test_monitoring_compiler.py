"""Tests for the monitoring rule compiler (`scripts/plan/monitoring_compiler.py`, ADR-0045-T1).

The compiler classifies each specialist-authored ``adjustment_rule`` as
Tier-1-auto-apply-safe (positively certified {bounded, in-domain, monotone}) vs
must-escalate, and REJECTS a fatally-unsafe (out-of-domain-bounds / safety-crossing) rule
at compile time — fail-closed. Every fixture is a SYNTHETIC literal built from the
canonical seven-field DOMAIN PROGRAM shape (PF-S131-01): no real operator data, no model
client, no network (AC-5). The load-bearing property is FAIL-CLOSED classification: a rule
the compiler cannot positively certify bounded-in-domain-monotone NEVER lands Tier-1
(ADR-0045 Consequences-Negative-2).

Fixture convention mirrors ``tests/plan/test_domain_program.py``: ``_training_program`` /
``_compound_program`` return a canonical VALID seven-field program whose
``adjustment_rules`` carry the ADR-0045-T1 grammar, then ``.update(overrides)`` swaps in
the one rule variant under test.
"""

import pytest

from scripts.plan import domain_program, monitoring_compiler
from scripts.store import plan_model


# --- the adjustment_rule grammar (ADR-0045-T1-owned) + the signal envelope --------
#
# A Tier-1-safe rule positively certifies {bounded, in-domain, monotone}: its driven
# ``delta`` stays strictly under the target signal's operating ``bound``, it targets a
# signal in its own domain, and it drives a single ``direction``. The paired signal
# declares the operating ``bound`` + the ``materiality_threshold``.


def _training_signal(**over):
    """The canonical training observable: an operating bound + a materiality threshold."""
    signal = {
        "signal": "session_rpe",
        "validity_tier": "high",
        "bound": 2.0,
        "materiality_threshold": 1.0,
    }
    signal.update(over)
    return signal


def _tier1_rule(**over):
    """A bounded (delta < bound), in-domain, monotone, immaterial rule -> Tier-1-safe."""
    rule = {"target_signal": "session_rpe", "direction": "decrease", "delta": 0.5}
    rule.update(over)
    return rule


def _ambiguous_rule():
    """A rule MISSING its direction axis -> monotone un-certifiable -> must-escalate (QA-W3-06)."""
    return {"target_signal": "session_rpe", "delta": 0.5}  # no 'direction'


def _training_program(**overrides):
    """A canonical VALID seven-field training program; a Tier-1-safe adjustment rule."""
    program = {
        "domain_kind": "training",
        "prescription": [
            {"phase": "accumulation", "start": "2026-07-01", "end": "2026-07-28",
             "sessions_per_week": 4},
        ],
        "rationale": [
            {"claim": "Progressive overload drives hypertrophy.",
             "certainty_of_evidence": "high", "strength_of_recommendation": "strong",
             "causality": "causal"},
        ],
        "monitoring_signals": [_training_signal()],
        "adjustment_rules": [_tier1_rule()],
        "required_labs": [],  # empty-OK for a pure-training domain
        "refusal_escalation": {"threshold_event": "acute joint pain",
                               "action": "hold_and_escalate"},
        "cross_domain_seams": [{"paired_domain": "nutrition", "seam_nature": "route"}],
    }
    program.update(overrides)
    return program


def _compound_signal(**over):
    """The canonical compound observable: an operating bound + a materiality threshold."""
    signal = {
        "signal": "fasting_glucose",
        "validity_tier": "high",
        "bound": 20.0,
        "materiality_threshold": 8.0,
    }
    signal.update(over)
    return signal


def _compound_rule(**over):
    """A bounded, in-domain, monotone, immaterial compound rule -> Tier-1-safe."""
    rule = {"target_signal": "fasting_glucose", "direction": "decrease", "delta": 3.0}
    rule.update(over)
    return rule


def _compound_program(**overrides):
    """A canonical VALID seven-field compound program (required_labs non-empty)."""
    program = {
        "domain_kind": "compound",
        "prescription": [
            {"phase": "titration", "start": "2026-07-01", "end": "2026-07-14", "dose": "low"},
        ],
        "rationale": [
            {"claim": "Compound supports connective-tissue repair.",
             "certainty_of_evidence": "moderate", "strength_of_recommendation": "conditional",
             "causality": "associational"},
        ],
        "monitoring_signals": [_compound_signal()],
        "adjustment_rules": [_compound_rule()],
        "required_labs": ["fasting_glucose", "lipid_panel"],  # mandatory + non-empty for compound
        "refusal_escalation": {"threshold_event": "out-of-range lab",
                               "action": "hold_on_human_gate"},
        "cross_domain_seams": [{"paired_domain": "training", "seam_nature": "hold"}],
    }
    program.update(overrides)
    return program


def _only_entry(config, domain="training"):
    """The single compiled rule entry for a one-rule program under ``domain``."""
    return config[domain][monitoring_compiler.DOMAIN_RULES][0]


# --- PF-S131-01: the fixtures are the CANONICAL seven-field shape ------------------


def test_training_and_compound_fixtures_are_canonical():
    """The fixtures pass domain_program.validate — the canonical shape, not a stand-in."""
    assert domain_program.validate(_training_program()) is None
    assert domain_program.validate(_compound_program()) is None


# --- AC-1: bounded + in-domain + monotone -> TIER1_AUTO_APPLY_SAFE -----------------


def test_bounded_in_domain_monotone_rule_compiles_tier1_safe():
    """A bounded, in-domain, monotone rule compiles to a Tier-1-auto-apply-safe entry."""
    config = monitoring_compiler.compile_config({"training": _training_program()})
    entry = _only_entry(config)
    assert monitoring_compiler.classification_of(entry) == monitoring_compiler.TIER1_AUTO_APPLY_SAFE


# --- AC-2: each escalate-class rule -> MUST_ESCALATE (never Tier-1) ----------------


def _escalate_rule(variant):
    """Build the one escalate-class rule variant under test (a fresh dict per call)."""
    return {
        "material": lambda: _tier1_rule(delta=1.5),               # >= materiality, < bound
        "cross_domain": lambda: _tier1_rule(target_domain="nutrition"),
        "safety_threshold": lambda: _tier1_rule(safety="gate"),   # refusal_escalation-gated
        "non_monotone": lambda: _tier1_rule(direction=["increase", "decrease"]),
        "ambiguous": _ambiguous_rule,                             # missing certification axis
    }[variant]()


@pytest.mark.parametrize(
    "variant", ["material", "cross_domain", "safety_threshold", "non_monotone", "ambiguous"]
)
def test_escalate_class_rule_compiles_must_escalate(variant):
    """A material / cross-domain / safety-gated / non-monotone / under-specified rule escalates."""
    rule = _escalate_rule(variant)
    config = monitoring_compiler.compile_config(
        {"training": _training_program(adjustment_rules=[rule])}
    )
    entry = _only_entry(config)
    assert monitoring_compiler.classification_of(entry) == monitoring_compiler.MUST_ESCALATE
    assert monitoring_compiler.classification_of(entry) != monitoring_compiler.TIER1_AUTO_APPLY_SAFE


def test_zero_escalate_rules_marked_tier1():
    """A mixed config marks EXACTLY the one safe rule Tier-1 and 0 of the five escalate-class rules."""
    rules = [
        _tier1_rule(),                                    # the ONE Tier-1-safe rule
        _tier1_rule(delta=1.5),                           # material
        _tier1_rule(target_domain="nutrition"),           # cross-domain
        _tier1_rule(safety="gate"),                       # safety-threshold
        _tier1_rule(direction=["increase", "decrease"]),  # non-monotone
        _ambiguous_rule(),                                # ambiguous / under-specified
    ]
    config = monitoring_compiler.compile_config(
        {"training": _training_program(adjustment_rules=rules)}
    )
    entries = config["training"][monitoring_compiler.DOMAIN_RULES]
    tier1 = [e for e in entries
             if monitoring_compiler.classification_of(e) == monitoring_compiler.TIER1_AUTO_APPLY_SAFE]
    escalate = [e for e in entries
                if monitoring_compiler.classification_of(e) == monitoring_compiler.MUST_ESCALATE]
    assert len(tier1) == 1
    assert len(escalate) == 5


# --- AC-3: a fatally-unsafe rule REJECTED at compile (raise, fail-closed) ----------


def test_out_of_domain_bounds_rule_rejected_at_compile():
    """A rule driving a change at/beyond the signal's bound is rejected; the error names it."""
    offending = _tier1_rule(delta=2.5)  # delta >= bound (2.0) -> out-of-domain-bounds
    with pytest.raises(monitoring_compiler.MonitoringCompileError) as exc:
        monitoring_compiler.compile_config(
            {"training": _training_program(adjustment_rules=[offending])}
        )
    assert exc.value.offending_rule == offending


def test_safety_crossing_rule_rejected_at_compile():
    """A rule driving a change across a hard safety threshold is rejected; the error names it."""
    offending = _tier1_rule(safety="cross")  # would cross a hard safety threshold
    with pytest.raises(monitoring_compiler.MonitoringCompileError) as exc:
        monitoring_compiler.compile_config(
            {"training": _training_program(adjustment_rules=[offending])}
        )
    assert exc.value.offending_rule == offending


# --- AC-4: the compiled config round-trips through plan_model (PRODUCTION path) ----


def test_compiled_config_round_trips_in_plan_model(tmp_path):
    """The compiled config survives the REAL record -> store.append -> read path intact."""
    domain_programs = {"workout": _training_program(), "peptides": _compound_program()}
    compiled = monitoring_compiler.compile_config(domain_programs)
    version = {
        "date": "2026-07-13",
        "domain_programs": domain_programs,
        "narrative": "Integrated block: train hard, dose low, monitor.",
        "milestones": [{"date": "2026-08-10", "label": "first re-test", "metric": "e1RM +5%"}],
        "monitoring_config": compiled,
    }
    plan_model.record_plan_version(version, tmp_path)
    loaded = plan_model.read_plan_version(version["date"], tmp_path)["version"]
    assert loaded["monitoring_config"] == compiled


# --- the classification_of read seam (ARCH-W3-04) ---------------------------------


def test_classification_of_reads_the_entry_token():
    """The classification_of accessor returns a compiled entry's closed-set token."""
    config = monitoring_compiler.compile_config({"training": _training_program()})
    token = monitoring_compiler.classification_of(_only_entry(config))
    assert token in {monitoring_compiler.TIER1_AUTO_APPLY_SAFE, monitoring_compiler.MUST_ESCALATE}
