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
    prescription      -- a periodized/dated representation (dated blocks/phases). The
                         renderable IDENTITY that names a card entry (`RENDERABLE_IDENTITY`:
                         `name` for workout/supplements, `compound` for peptides) is a
                         TOP-LEVEL prescription field (ubsp) -- the 58z0 honest-no-plan
                         boundary (`project_renderable`) reads it there, so a specialist
                         emitting identity only INSIDE `blocks` is a degenerate periodized-
                         only shape that projects to honest no-plan, never a card.
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
                         slot). T1 pins the FIELD NAME as a conditional field but does NOT
                         pin its presence or the marker slot's shape; ADR-0045-T2's Tier-4
                         owns the escalation-event semantics (`validate` does not check it).
    cross_domain_seams-- a list of seam entries; each entry's intended structure is a
                         paired-domain reference (`SEAM_WITH_DOMAIN`) + a seam-nature/conflict
                         token (`SEAM_NATURE`; a `SEAM_CONFLICT`-nature seam holds the declaring
                         domain) + an OPTIONAL Option-B adverse-event sub-structure
                         (`SEAM_AE_PROFILE`, the `{additive_classes, interactions}` shape the
                         compound band carries on `meta.ae_profile` — the rich domain's AE channel;
                         kn29 / SEC-W4-01). Those key-names are single-source constants HERE (pule),
                         referenced by `orchestrate.SEAM_*` so a divergent filler is caught, not
                         silently dropped. T1 pins the FIELD NAME as a conditional field but does
                         NOT pin its presence or edge shape; ADR-0043-T2 owns the reconciliation
                         semantics AND the seam-edge validation (`validate` does not check the edge
                         shape, incl. the OPTIONAL `SEAM_AE_PROFILE` — it is reader-enforced).

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
`cross_domain_seams` / `refusal_escalation` pinned structure, the seam-edge key-name
constants (`SEAM_*`) + the renderable-identity table + `project_renderable`, the
`validate` / `missing_required_fields` signatures, `DomainProgramError`'s accessors, and
`VALIDITY_TIERS` are the frozen seam. ADR-0041-T2 / 0044-T1 / 0043-T2 / 0045-T1 /
0046-T1 / 0043-T3 must not change them without Architect review.
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

# --- cross_domain_seams edge key-names (single source of truth, pule) ------------
# The seam-edge structure `orchestrate.reconcile` reads: each entry names a paired domain
# (`SEAM_WITH_DOMAIN`) + a seam-nature token (`SEAM_NATURE`); a `SEAM_CONFLICT`-nature seam
# holds the declaring domain. `orchestrate.SEAM_*` REFERENCE these, so a fixture / specialist
# diverging from the pinned key-names is caught by the reader, never silently dropped.
SEAM_WITH_DOMAIN = "with_domain"
SEAM_NATURE = "nature"
SEAM_CONFLICT = "conflict"
# The OPTIONAL Option-B (kn29 / SEC-W4-01) adverse-event sub-structure on a seam entry: the SAME
# `{additive_classes, interactions}` shape the compound band carries on `meta.ae_profile`, relocated
# onto the seam so a RICH domain (no `meta.ae_profile`) declares its AE profile on its seams. Read by
# `orchestrate` (`orchestrate.SEAM_AE_PROFILE`) — reader-enforced, NOT validated (ADR-0043-T2 boundary).
SEAM_AE_PROFILE = "ae_profile"

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

        0. the program is a Mapping, `monitoring_signals` is a list, and each entry is a
           Mapping -- a malformed non-Mapping/non-list shape from untrusted author output
           leaves via `DomainProgramError`, not a bare AttributeError/TypeError;
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
    if not isinstance(program, Mapping):
        raise DomainProgramError(
            f"program is not a mapping (got {type(program).__name__})"
        )

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

    signals = program[MONITORING_SIGNALS]
    if not isinstance(signals, list):
        raise DomainProgramError(
            f"{MONITORING_SIGNALS} must be a list (got {type(signals).__name__})",
            offending_field=MONITORING_SIGNALS,
        )
    for entry in signals:
        if not isinstance(entry, Mapping):
            raise DomainProgramError(
                f"{MONITORING_SIGNALS} entry is not a mapping (got {type(entry).__name__})",
                offending_field=MONITORING_SIGNALS,
                offending_signal=entry,
            )
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


# --- prescription -> renderable projection (the 58z0 boundary; ubsp/qrg4 single home) ---
# domain -> the renderable IDENTITY field distinguishing a nameable renderable entry from a
# degenerate PERIODIZED-ONLY prescription (dated `blocks`, no card identity at the top). The ubsp
# pin that this identity is a top-level field lives in the `prescription` contract (module docstring
# above), the single authoritative statement. This is the ONE projection home (`project_renderable`),
# reused by `generate_plan` (the four translators) AND `plan_model.read_standing_plan` (qrg4) so no
# consumer duplicates the projection and no layering inversion (`plan_model` never imports
# `generate_plan`) forms.
RENDERABLE_IDENTITY = {
    "workout": "name",
    "supplements": "name",
    "peptides": "compound",
}


def _deep_strip_load(value):
    """Return a deep copy of a prescription structure with every `load` key removed.

    The ADR-0015 clearance gate drops load prescriptions when no clinician clearance is granted. A
    PERIODIZED prescription nests per-block `load` under dated `blocks`/phases, so a top-level pop
    leaks the nested load into the renderable AND the store-bound program; this recurses dicts and
    lists so `load` is stripped at EVERY depth.
    """
    if isinstance(value, dict):
        return {key: _deep_strip_load(sub) for key, sub in value.items() if key != "load"}
    if isinstance(value, list):
        return [_deep_strip_load(item) for item in value]
    return value


def project_renderable(prescription, domain, *, strip_load):
    """Project a (possibly PERIODIZED) DOMAIN PROGRAM prescription to its flat renderable form.

    The uniform prescription is canonically PERIODIZED (dated `blocks`, per-block `load`), but the
    four frozen `plan_schema` per-domain validators + the dashboard consume the FLAT top-level
    fields. This projects the prescription for the renderable, the store-bound program, AND the
    ADR-0044-T2 standing reader (bead 58z0 / qrg4):

      1. DEEP-STRIP `load` over the FULL periodized structure when `strip_load` (the ADR-0015
         clearance leg — a per-block `load` must never reach a rendered plan); the dated `blocks`
         ride on as an open-on-extras extra.
      2. Honest no-plan (return None) for a DEGENERATE periodized-only prescription — dated `blocks`
         but NO top-level renderable identity for its domain — rather than passing a
         `{"blocks": [...]}` shell to a consumer whose frozen validator would raise. A FLAT
         prescription missing a required field is a genuine malformation, NOT a periodized shape, so
         it is passed through and still surfaces LOUD downstream.

    Args:
        prescription: The DOMAIN PROGRAM's prescription (a dict for a real prescription).
        domain (str): The plan domain — keys the renderable-identity check (`RENDERABLE_IDENTITY`).
        strip_load (bool): Deep-strip `load` at every depth when True.

    Returns:
        (dict | None) The projected prescription (flat fields + load-handled `blocks`), or None for
        a non-dict prescription or a degenerate periodized-only shape (the honest no-plan / skip).
    """
    if not isinstance(prescription, dict):
        return None
    projected = _deep_strip_load(prescription) if strip_load else dict(prescription)
    identity = RENDERABLE_IDENTITY.get(domain)
    if identity is not None and "blocks" in projected:
        value = projected.get(identity)
        if not (isinstance(value, str) and value):
            return None
    return projected
