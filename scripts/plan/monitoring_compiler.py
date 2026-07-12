"""The deterministic monitoring compiler — Tier-1-safe vs must-escalate rule grammar.

ADR-0045-T1. ``compile_config(domain_programs)`` compiles each domain program's
specialist-authored ``adjustment_rules`` (against its ``monitoring_signals`` envelope)
into a DETERMINISTIC ``monitoring_config`` that classifies every rule as
``TIER1_AUTO_APPLY_SAFE`` — positively certified {bounded, in-domain, monotone}, safe for
the ADR-0045-T2/T3 daily loop to auto-apply with 0 model calls — or ``MUST_ESCALATE``
(material, cross-domain, safety-gated, non-monotone, or under-specified: routed to a
higher escalation tier). A fatally-unsafe rule (out-of-domain-bounds or safety-crossing)
is REJECTED at compile time via ``MonitoringCompileError`` — fail-closed.

The load-bearing property is FAIL-CLOSED classification: Tier-1 is a POSITIVE
certification, never a default. A rule the compiler cannot positively certify
bounded-in-domain-monotone NEVER lands Tier-1 — it escalates, or (if fatally unsafe) the
compile raises. A rule that could auto-apply an unsafe adjustment un-modelled is the live
risk this compiler prevents (ADR-0045 Consequences-Negative-2).

The rule grammar
----------------
An ``adjustment_rule`` declares a ``target_signal`` + an optional ``target_domain`` (absent
=> the program's own domain, i.e. in-domain), a ``direction`` (a single token => monotone;
a list / oscillating token => non-monotone) and a ``delta`` magnitude (the bounded axis),
and optionally a ``safety`` marker (``"gate"`` => refusal_escalation-gated, escalate;
``"cross"`` => drives across a hard safety threshold, reject). The paired
``monitoring_signal`` declares the operating ``bound`` (``delta`` must be strictly under it)
and the ``materiality_threshold`` (``delta`` at/above it, but under the bound, is material).

Where the config lives
----------------------
The compiled config is a plain, JSON-serializable dict. The caller slots it into the
ADR-0044 comprehensive plan version's ``monitoring_config`` element, where it rides
``plan_model.record_plan_version`` -> the frozen ``store.append`` UNCHANGED. This module
imports neither the store nor the executor: it emits a value and stores nothing itself.

Trust boundary
--------------
``compile_config`` consumes ``domain_programs`` that are ALREADY
``domain_program.validate``-conformant (validated upstream at the model boundary), so it
does NOT re-run that validation. Its fail-closed boundary is the net-new RULE-GRAMMAR
check (out-of-bounds / safety-crossing -> reject), not program-conformance re-validation.

Change control
--------------
The ``compile_config`` signature, the ``monitoring_config`` shape, the
``{TIER1_AUTO_APPLY_SAFE, MUST_ESCALATE}`` vocabulary, the ``classification_of`` accessor,
the ``adjustment_rule`` grammar, and ``MonitoringCompileError.offending_rule`` are the
Tier-3 config seam ADR-0045-T2's four-tier executor runs on. ADR-0045-T2 must not change
them without Architect review.
"""

import math
from collections.abc import Mapping

from scripts.plan import domain_program

# --- the classification vocabulary: the closed two-member set every entry is tagged with
TIER1_AUTO_APPLY_SAFE = "tier1_auto_apply_safe"
MUST_ESCALATE = "must_escalate"

# --- monitoring_config navigation keys (per-domain grouping) ----------------------
DOMAIN_RULES = "rules"       # per domain: the list of compiled adjustment_rule entries
DOMAIN_SIGNALS = "signals"   # per domain: the bundled monitoring_signals observables

# --- the adjustment_rule grammar (ADR-0041-T1-assigned to this task) + signal envelope
RULE_TARGET_SIGNAL = "target_signal"   # names a monitoring_signals entry
RULE_TARGET_DOMAIN = "target_domain"   # absent -> the program's own domain (in-domain)
RULE_DIRECTION = "direction"           # a single str -> monotone; a list / oscillating token -> non-monotone
RULE_DELTA = "delta"                   # the driven magnitude the rule applies
RULE_SAFETY = "safety"                 # SAFETY_GATE (escalate) | SAFETY_CROSS (reject)

SIGNAL_NAME = "signal"                 # the observable's name (paired to RULE_TARGET_SIGNAL)
SIGNAL_BOUND = "bound"                 # the operating bound: delta must be < bound (in-bounds)
SIGNAL_MATERIALITY = "materiality_threshold"  # delta >= this (and < bound) -> material

SAFETY_GATE = "gate"     # references refusal_escalation -> must-escalate (non-fatal)
SAFETY_CROSS = "cross"   # would drive a change across a hard safety threshold -> reject (fatal)

# direction tokens that encode a bidirectional / oscillating (non-monotone) adjustment
_NON_MONOTONE_DIRECTIONS = frozenset({"both", "bidirectional", "oscillating"})

# the per-entry classification tag KEY — internal (read through classification_of, ARCH-W3-04)
_CLASSIFICATION_KEY = "classification"
_RULE_KEY = "rule"


class MonitoringCompileError(Exception):
    """The single typed rejection channel for a fatally-unsafe adjustment rule.

    Raised at compile time on an out-of-domain-bounds or safety-crossing rule (fail-closed).
    Carries a STRUCTURED offense accessor so a caller identifies the offending rule without
    substring-scanning the message (mirrors ``domain_program.DomainProgramError`` /
    ``plan_model.PlanVersionError``).

    Attributes:
        offending_rule (Mapping | None): The offending ``adjustment_rule`` entry.
    """

    def __init__(self, message="", *, offending_rule=None):
        super().__init__(message)
        self.offending_rule = offending_rule


def classification_of(entry) -> str:
    """Return a compiled rule entry's classification token.

    The self-describing READ seam ADR-0045-T2's tier predicate reads (ARCH-W3-04): it keeps
    the per-entry tag KEY spelling internal to this module.

    Args:
        entry (Mapping): A compiled rule entry from a ``monitoring_config`` domain's rules.

    Returns:
        (str) The entry's token — ``TIER1_AUTO_APPLY_SAFE`` or ``MUST_ESCALATE``.
    """
    return entry[_CLASSIFICATION_KEY]


def _is_non_monotone(direction) -> bool:
    """Return True unless `direction` is a single monotone direction token.

    Args:
        direction: A rule's declared direction — a single str drives one way (monotone); a
            list/tuple or an oscillating token drives more than one way (non-monotone).

    Returns:
        (bool) True when the direction is non-monotone.
    """
    if isinstance(direction, str):
        return direction in _NON_MONOTONE_DIRECTIONS
    return True


def _is_finite_nonneg_real(magnitude) -> bool:
    """Return True when `magnitude` is a finite, non-negative real number.

    The grammar predicate for a rule's driven `delta` and a signal's `bound` /
    `materiality_threshold`: a present magnitude must be a real int/float (a `bool` is a
    type-confusion, not a magnitude), finite (no `NaN` / `inf`), and non-negative. A present
    value failing this is a grammar violation the compiler rejects fail-closed.

    Args:
        magnitude: A candidate delta, bound, or materiality_threshold value.

    Returns:
        (bool) True when the value is a finite non-negative int/float, `bool` excluded.
    """
    if isinstance(magnitude, bool) or not isinstance(magnitude, (int, float)):
        return False
    return math.isfinite(magnitude) and magnitude >= 0


def _classify(rule, own_domain, signal_index) -> str:
    """Classify ONE adjustment rule, or raise on a fatally-unsafe one (fail-closed).

    Tier-1 is a POSITIVE certification of {bounded, in-domain, monotone}: the absence or
    ambiguity of any axis -> must-escalate. A rule driving at/beyond the operating bound or
    across a hard safety threshold -> raise.

    Args:
        rule (Mapping): The adjustment rule entry.
        own_domain (str): The domain the rule's program belongs to (the in-domain reference).
        signal_index (Mapping): The program's monitoring signals keyed by signal name.

    Returns:
        (str) ``TIER1_AUTO_APPLY_SAFE`` or ``MUST_ESCALATE``.

    Raises:
        MonitoringCompileError: The rule is out-of-domain-bounds or safety-crossing.
    """
    safety = rule.get(RULE_SAFETY)
    direction = rule.get(RULE_DIRECTION)
    delta = rule.get(RULE_DELTA)
    target_domain = rule.get(RULE_TARGET_DOMAIN, own_domain)
    signal = signal_index.get(rule.get(RULE_TARGET_SIGNAL))
    bound = signal.get(SIGNAL_BOUND) if signal is not None else None
    materiality = signal.get(SIGNAL_MATERIALITY) if signal is not None else None

    # 0. GRAMMAR — reject a PRESENT-but-malformed magnitude (non-numeric, bool, NaN, inf,
    #    negative) fail-closed, so a bad delta/bound/materiality never falls through to a silent
    #    Tier-1 or a bare TypeError on the ordered comparisons below. (An ABSENT None is handled
    #    by the escalate ladder — only a present malformed value raises.)
    for magnitude in (delta, bound, materiality):
        if magnitude is not None and not _is_finite_nonneg_real(magnitude):
            raise MonitoringCompileError(
                "malformed magnitude: delta/bound/materiality must be a finite non-negative real",
                offending_rule=rule,
            )

    # 1. FATAL rejects — raise ONLY on a positive determination of unsafety (fail-closed).
    if safety == SAFETY_CROSS:
        raise MonitoringCompileError(
            "safety-crossing rule drives a change across a hard safety threshold",
            offending_rule=rule,
        )
    if delta is not None and bound is not None and delta >= bound:
        raise MonitoringCompileError(
            "out-of-domain-bounds rule drives a change at/beyond the signal's operating bound",
            offending_rule=rule,
        )

    # 2. must-escalate — any escalate trigger, OR a missing certification axis. Positive
    #    certification is required for Tier-1, so any un-certifiable axis escalates here.
    if direction is None or delta is None:
        return MUST_ESCALATE                     # ambiguous / under-specified (QA-W3-06)
    if _is_non_monotone(direction):
        return MUST_ESCALATE                     # non-monotone
    if target_domain != own_domain:
        return MUST_ESCALATE                     # cross-domain
    if safety == SAFETY_GATE:
        return MUST_ESCALATE                     # safety-threshold (refusal_escalation-gated)
    if bound is None or materiality is None:
        return MUST_ESCALATE                     # signal envelope incomplete -> un-certifiable
    if delta >= materiality:
        return MUST_ESCALATE                     # material

    # 3. Tier-1: positively certified {bounded, in-domain, monotone}, immaterial, un-gated.
    return TIER1_AUTO_APPLY_SAFE


def compile_config(domain_programs: Mapping) -> dict:
    """Compile the domain programs' adjustment rules into a classified monitoring config.

    Iterates each domain's ``adjustment_rules``, classifies each rule Tier-1-auto-apply-safe
    vs must-escalate against its ``monitoring_signals`` envelope, and returns a NON-EMPTY,
    JSON-serializable config grouping — per domain — the compiled rule entries (each tagged
    with its classification token) and the domain's monitoring signals. Fail-closed: an
    out-of-domain-bounds or safety-crossing rule raises ``MonitoringCompileError`` — the
    config never admits such a rule.

    ``domain_programs`` is assumed ``domain_program.validate``-conformant on arrival (the
    trust boundary — validated upstream at the model boundary); this compiler re-runs no
    program conformance check, only the net-new rule-grammar classification.

    Args:
        domain_programs (Mapping): ``{domain_name: seven-field DOMAIN PROGRAM}`` (the
            ``plan_model`` ``DOMAIN_PROGRAMS`` shape).

    Returns:
        (dict) The ``monitoring_config``: ``{domain_name: {DOMAIN_RULES: [entry, ...],
            DOMAIN_SIGNALS: [signal, ...]}}``, JSON-serializable throughout.

    Raises:
        MonitoringCompileError: A rule is out-of-domain-bounds or safety-crossing.
    """
    config = {}
    for domain_name, program in domain_programs.items():
        signals = program[domain_program.MONITORING_SIGNALS]
        # Fail-closed on a DUPLICATE signal name — a last-wins index would silently collapse two
        # signals sharing a name, so one rule could be certified against the wrong envelope.
        signal_index = {}
        for signal in signals:
            name = signal.get(SIGNAL_NAME)
            if name in signal_index:
                raise MonitoringCompileError(
                    f"duplicate signal name {name!r} in the monitoring_signals envelope",
                    offending_rule=None,
                )
            signal_index[name] = signal
        compiled_rules = [
            {_RULE_KEY: rule, _CLASSIFICATION_KEY: _classify(rule, domain_name, signal_index)}
            for rule in program[domain_program.ADJUSTMENT_RULES]
        ]
        config[domain_name] = {DOMAIN_RULES: compiled_rules, DOMAIN_SIGNALS: signals}
    return config
