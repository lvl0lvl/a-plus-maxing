"""The uniform seven-field DOMAIN PROGRAM schema + its conformance validator.

THE shared contract every downstream comprehensive-plan consumer emits against or
reads: the ADR-0041-T2 translators emit programs that must pass `validate`,
ADR-0044-T1 stores the seven-field program intact (including the first-class domain
KIND), ADR-0043-T2 reconciles the `cross_domain_seams` edge shape, ADR-0045-T1
compiles the `monitoring_signals` + `adjustment_rules`, and ADR-0046-T1's dispatched
specialists emit the uniform shape. This is a leaf module: it imports the standard
library only, so no consumer dependency cycle can form.

The seven fields
----------------
Required (present on every program, any kind):
    prescription      -- a periodized/dated representation (dated blocks/phases).
    rationale         -- the GRADE structure: per claim, certainty-of-evidence x
                         strength-of-recommendation plus a causal-vs-associational
                         marker. `validate` checks presence only; the internal GRADE
                         shape is a downstream-consumer contract, not a validated axis.
    monitoring_signals-- a list; EACH entry carries a validity-tier token drawn from
                         `VALIDITY_TIERS` (checked on every entry, `SIGNAL_TIER_KEY`).
    adjustment_rules  -- the autoregulation rule set.
Conditional (present per the domain kind's required-vs-conditional row):
    required_labs     -- empty-OK for a training domain; PRESENT-AND-NON-EMPTY for a
                         compound domain.
    refusal_escalation-- a safety-threshold escalation marker (a condition/event token
                         slot). T1 pins presence + the marker slot; ADR-0045-T2's
                         Tier-4 owns the escalation-event semantics.
    cross_domain_seams-- a list of seam entries; each entry's LOCKED structure is a
                         paired-domain reference + a seam-nature/conflict token. T1
                         pins this edge shape; ADR-0043-T2 owns the reconciliation
                         semantics.

The domain KIND
---------------
Each program declares a first-class `KIND_FIELD` attribute -- a token from the closed
`DOMAIN_KINDS` vocabulary (distinct from the seven content fields, never re-derived at
read time so it survives ADR-0044-T1's store->load intact). The KIND keys the
required-vs-conditional table (`DOMAIN_KIND_RULES`): a training domain leaves
`required_labs` empty-OK; a compound domain makes `required_labs` mandatory-and-non-empty
AND requires autoregulation (`monitoring_signals` and `adjustment_rules` both non-empty).
`validate` FAIL-CLOSES on an absent or non-vocabulary kind rather than defaulting -- a
default would let an unclassifiable program silently escape the compound-only floors
(ADR-0041 Consequences-Negative-4).

Fail-closed conformance
-----------------------
`validate` is the fail-fast conformance boundary. It raises `DomainProgramError`
(carrying a STRUCTURED offense accessor -- `.offending_field` / `.offending_signal`)
on any non-conformant program; it returns `None` on conformance. It never returns a
degraded program -- an under-delivered author call surfaces as an honest no-plan
state, not a static plan missing autoregulation or required fields.

Change control
--------------
The seven-field shape, the domain-KIND attribute + `DOMAIN_KINDS`, the
`cross_domain_seams` / `refusal_escalation` pinned structure, the `validate` /
`missing_required_fields` signatures, `DomainProgramError`'s accessors, and
`VALIDITY_TIERS` are the frozen seam. ADR-0041-T2 / 0044-T1 / 0043-T2 / 0045-T1 /
0046-T1 must not change them without Architect review.
"""

from collections.abc import Mapping

# --- field-name constants (single source of truth for the shared seam) ----------

PRESCRIPTION = "prescription"
RATIONALE = "rationale"
MONITORING_SIGNALS = "monitoring_signals"
ADJUSTMENT_RULES = "adjustment_rules"
REQUIRED_LABS = "required_labs"
REFUSAL_ESCALATION = "refusal_escalation"
CROSS_DOMAIN_SEAMS = "cross_domain_seams"

REQUIRED_FIELDS = (PRESCRIPTION, RATIONALE, MONITORING_SIGNALS, ADJUSTMENT_RULES)
CONDITIONAL_FIELDS = (REQUIRED_LABS, REFUSAL_ESCALATION, CROSS_DOMAIN_SEAMS)

# --- the domain KIND: first-class attribute + closed, membership-checked vocab ---

KIND_FIELD = "domain_kind"

# The required-vs-conditional TABLE keyed by domain kind. `DOMAIN_KINDS` derives from
# its keys, so the vocabulary and the rule table share a single source of truth.
DOMAIN_KIND_RULES = {
    "training": {"required_labs_nonempty": False, "autoregulation_required": False},
    "compound": {"required_labs_nonempty": True, "autoregulation_required": True},
}
DOMAIN_KINDS = frozenset(DOMAIN_KIND_RULES)

# --- monitoring-signal validity tiers: closed, membership-checked (GRADE) --------

SIGNAL_TIER_KEY = "validity_tier"
VALIDITY_TIERS = frozenset({"high", "moderate", "low", "very_low"})


class DomainProgramError(Exception):
    """The single typed rejection channel for a non-conformant DOMAIN PROGRAM.

    Carries structured offense accessors so a caller identifies the offense without
    substring-scanning the message.

    Attributes:
        offending_field (str | None): The field/attribute at fault -- a required field
            name, the kind attribute (`KIND_FIELD`), `required_labs`, `monitoring_signals`,
            or `adjustment_rules`.
        offending_signal (Mapping | None): The offending `monitoring_signals` entry for a
            per-signal validity-tier offense; `None` otherwise.
    """

    def __init__(self, message="", *, offending_field=None, offending_signal=None):
        super().__init__(message)
        self.offending_field = offending_field
        self.offending_signal = offending_signal


def missing_required_fields(program: Mapping) -> list[str]:
    """Return the required-field names absent from `program`.

    A non-raising conformance probe on the required-field axis: an empty list means
    every required field is present (it does not by itself mean the program is
    conformant -- the kind and compound-only floors are checked by `validate`).

    Args:
        program (Mapping): A DOMAIN PROGRAM mapping.

    Returns:
        (list[str]) The required-field names, in `REQUIRED_FIELDS` order, missing from
            `program`.
    """
    return [field for field in REQUIRED_FIELDS if field not in program]


def validate(program: Mapping) -> None:
    """Raise `DomainProgramError` unless `program` conforms to the DOMAIN PROGRAM contract.

    Fail-closed: an incomplete or under-delivered program is rejected with a structured
    offense accessor set, never returned in a degraded form. The checks, in order:

        1. every required field is present (else `offending_field` = the missing field);
        2. the domain kind is present and a `DOMAIN_KINDS` member (else `offending_field`
           = `KIND_FIELD` -- absent/non-vocabulary kinds fail closed, never default);
        3. every `monitoring_signals` entry carries a `VALIDITY_TIERS`-member tier (else
           `offending_field` = `monitoring_signals`, `offending_signal` = the entry);
        4. for a compound-kind program, `required_labs` is present-and-non-empty and
           autoregulation is present (`monitoring_signals` and `adjustment_rules` both
           non-empty).

    Args:
        program (Mapping): A DOMAIN PROGRAM mapping.

    Returns:
        (None) When the program conforms.
    """
    missing = missing_required_fields(program)
    if missing:
        raise DomainProgramError(
            f"missing required field(s): {missing}", offending_field=missing[0]
        )

    kind = program.get(KIND_FIELD)
    if kind not in DOMAIN_KINDS:
        raise DomainProgramError(
            f"domain kind absent or unrecognized: {kind!r}", offending_field=KIND_FIELD
        )

    for entry in program[MONITORING_SIGNALS]:
        if entry.get(SIGNAL_TIER_KEY) not in VALIDITY_TIERS:
            raise DomainProgramError(
                f"monitoring signal without a valid {SIGNAL_TIER_KEY}",
                offending_field=MONITORING_SIGNALS,
                offending_signal=entry,
            )

    rules = DOMAIN_KIND_RULES[kind]
    if rules["required_labs_nonempty"] and not program.get(REQUIRED_LABS):
        raise DomainProgramError(
            f"{REQUIRED_LABS} is mandatory and non-empty for a {kind} domain",
            offending_field=REQUIRED_LABS,
        )
    if rules["autoregulation_required"]:
        if not program[MONITORING_SIGNALS]:
            raise DomainProgramError(
                f"a {kind} domain requires at least one monitoring signal",
                offending_field=MONITORING_SIGNALS,
            )
        if not program[ADJUSTMENT_RULES]:
            raise DomainProgramError(
                f"a {kind} domain requires at least one adjustment rule",
                offending_field=ADJUSTMENT_RULES,
            )
