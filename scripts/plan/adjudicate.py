"""Medical-liaison terminal adjudication gate — the pipeline Phase-4 safety gate.

The reconciler (`scripts/plan/orchestrate.py`) HOLDS a supplement when a supplement↔peptide
additive-AE finding fires, but it does not adjudicate the held finding — that is the
medical-liaison's terminal job (design `vault/design/plan-generation-pipeline-v1.md` Phase 4,
decision 4: "two terminal functions, not one"). Under runtime A the orchestrator dispatches the
deployed `medical-liaison` (full profile inlined per INV-ROLE-INLINING) with the held finding as
a `safety_finding`; the liaison returns an adjudication envelope; THIS module validates that
envelope and produces the terminal outcome:

  - a HIGH/MEDIUM finding clears ONLY via a content-valid override record at the band's rung —
    then the hold is RELEASED and the supplement records (the override record rides the returned
    result, NOT a new store stream);
  - a `composite_band == CRITICAL` or `harm_class ∈ {H1, H2}` finding is NON-OVERRIDABLE
    (`mechanical-auto-block-per-R3`): no override path is honored — the block STANDS;
  - any malformed / insufficient / id-mismatched envelope leaves the hold in place — the honest
    block-stands state, never a silent release.

The two invariants this gate enforces (medical-liaison design §16 OQ-3, bead `mdv`):

  - INV-OVERRIDE-RECORD-SCHEMA — an override record is validated on CONTENT, not presence: it
    carries the canonical override literal (referenced, never redefined), a content-bearing
    `operator_reason` (length floor + vacuous stop-list) at HIGH, an `evidence_provided.rung` that
    meets the band's `evidence_tier_required` (Appelbaum-Grisso), a risks-of-proceeding clause, and
    a contradictions-log reference. A presence-only record (every field present but `operator_reason:
    "because I want to try it"`) is REJECTED — the canonical Role-7 rubber-stamp surface.
  - INV-CRITICAL-NON-OVERRIDABLE — a CRITICAL or H1/H2 finding NEVER gets an override path; an
    envelope that builds one for such a finding is an invariant violation, not a release.

`audit_adjudication_envelope` is the mechanical verification both invariants register against
(`scripts/audit-medical-liaison-override.sh`); the `--audit-envelope` CLI wraps it so the bash
audit and the in-code gate share ONE validation source.
"""

import argparse
import json
import sys

# The canonical override literal — referenced verbatim, never redefined (Role 4 §13 row 7 canonical
# per bead z8i; medical-liaison Core Rule 2 / Communication schema). An override record whose
# `override_literal` is not this exact string is rejected.
OVERRIDE_LITERAL = "operator is overriding a safety block"

# The non-role sentinel a CRITICAL / H1-H2 auto-block carries in `severity_final.set_by`
# (medical-liaison Core Rule 2 / Communication field 4).
AUTO_BLOCK_SENTINEL = "mechanical-auto-block-per-R3"

# The adjudicating role's id (the only `set_by` that may finalize a HIGH/MEDIUM override).
LIAISON_SET_BY = "medical-liaison"

# Bands the liaison may carry. HIGH/MEDIUM are operator-overridable via a content-valid record;
# CRITICAL is non-overridable (Core Rule 2).
OVERRIDABLE_BANDS = ("MEDIUM", "HIGH")
BANDS = ("MEDIUM", "HIGH", "CRITICAL")

# Harm classes that are non-overridable regardless of band (medical-liaison Core Rule 2 / Role
# Boundaries: H1/H2 → `mechanical-auto-block-per-R3`, null/absent override path).
NON_OVERRIDABLE_HARM_CLASSES = frozenset({"H1", "H2"})

# Evidence rungs (Appelbaum-Grisso, medical-liaison Core Rule 7), ordinal low→high. A provided rung
# meets a required rung when its ordinal is ≥ the required ordinal.
_RUNG_ORDER = {"clear-choice": 1, "understanding+appreciation+reasoning": 2}

# The `operator_reason` content floor + vacuous stop-list (Core Rule 6: "content-free operator_reason
# at HIGH fails"). A reason shorter than the floor, or one that IS / CONTAINS a vacuous phrase, is
# not content-bearing. The list names the rubber-stamp surface, not an exhaustive grammar.
_OPERATOR_REASON_FLOOR = 20
_VACUOUS_REASON_PHRASES = (
    "because i want to", "i want to try", "want to try it", "just because",
    "trust me", "feel like it", "sounds good", "why not", "no reason",
    "i just want", "because i can", "for fun",
)


def evidence_tier_required(composite_band):
    """The evidence rung a band demands before an override may clear (Appelbaum-Grisso).

    Args:
        composite_band (str): The finding's band — `MEDIUM` or `HIGH`.

    Returns:
        (str) The required rung token, or `None` when the band is not overridable.
    """
    if composite_band == "MEDIUM":
        return "clear-choice"
    if composite_band == "HIGH":
        return "understanding+appreciation+reasoning"
    return None


def _rung_meets(provided, required):
    """Whether a provided evidence rung meets (≥) the required rung; unknown rungs never meet."""
    if provided not in _RUNG_ORDER or required not in _RUNG_ORDER:
        return False
    return _RUNG_ORDER[provided] >= _RUNG_ORDER[required]


def _reason_is_content_bearing(reason):
    """Whether an `operator_reason` is content-bearing (floor + vacuous stop-list)."""
    if not isinstance(reason, str):
        return False
    normalized = " ".join(reason.split()).strip().lower()
    if len(normalized) < _OPERATOR_REASON_FLOOR:
        return False
    return not any(phrase in normalized for phrase in _VACUOUS_REASON_PHRASES)


def _nonempty_str(value):
    """Whether `value` is a non-whitespace string."""
    return isinstance(value, str) and bool(value.strip())


def is_non_overridable(composite_band, harm_class):
    """Whether a finding is non-overridable (INV-CRITICAL-NON-OVERRIDABLE).

    Args:
        composite_band (str): The finding's band.
        harm_class (str): The finding's harm class (may be `None`).

    Returns:
        (bool) True when the band is CRITICAL or the harm class is H1/H2 — no override path is
        honored for such a finding.
    """
    return composite_band == "CRITICAL" or harm_class in NON_OVERRIDABLE_HARM_CLASSES


def validate_override_record(record, *, composite_band, caution=None):
    """Validate an override record on CONTENT, not presence (INV-OVERRIDE-RECORD-SCHEMA).

    Args:
        record (dict): The override record (the 10-field schema).
        composite_band (str): The band the record claims to override (must be MEDIUM or HIGH and
            must match the record's own `composite_band`).
        caution (str, optional): The originating finding's caution text. When given, the record's
            `caution_verbatim` must reproduce it; when omitted (audit-only, no originating finding),
            the verbatim-match is skipped but `caution_verbatim` must still be content-bearing.

    Returns:
        (bool) valid — whether the record passes every content check.
        (list) reasons — one string per failed check (empty when valid).
    """
    reasons = []
    if not isinstance(record, dict):
        return False, ["override_record is not an object"]

    required = (
        "caution_verbatim", "composite_band", "risks_communicated", "operator_reason",
        "evidence_tier_required", "evidence_provided", "override_literal", "voluntariness_note",
        "timestamp", "contradictions_log_ref",
    )
    for field in required:
        if field not in record:
            reasons.append(f"missing field: {field}")

    if record.get("override_literal") != OVERRIDE_LITERAL:
        reasons.append("override_literal is not the canonical literal")

    band = record.get("composite_band")
    if band not in OVERRIDABLE_BANDS:
        reasons.append(f"composite_band {band!r} is not overridable (MEDIUM/HIGH only)")
    elif band != composite_band:
        reasons.append("composite_band does not match the finding's band")

    if not _nonempty_str(record.get("caution_verbatim")):
        reasons.append("caution_verbatim is empty")
    elif caution is not None and record.get("caution_verbatim") != caution:
        reasons.append("caution_verbatim is not verbatim from the finding")

    if not _reason_is_content_bearing(record.get("operator_reason")):
        reasons.append("operator_reason is content-free (floor or vacuous stop-list)")

    risks = record.get("risks_communicated")
    if not isinstance(risks, dict) or not _nonempty_str(risks.get("risks_of_proceeding")):
        reasons.append("risks_communicated lacks a content-bearing risks_of_proceeding clause")

    required_tier = evidence_tier_required(composite_band)
    if record.get("evidence_tier_required") != required_tier:
        reasons.append("evidence_tier_required does not match the band's required rung")
    provided = record.get("evidence_provided")
    provided_rung = provided.get("rung") if isinstance(provided, dict) else None
    if not _rung_meets(provided_rung, required_tier):
        reasons.append("evidence_provided.rung is below the band's required rung")

    if not _nonempty_str(record.get("voluntariness_note")):
        reasons.append("voluntariness_note is empty")
    if not _nonempty_str(record.get("timestamp")):
        reasons.append("timestamp is empty")
    if not _nonempty_str(record.get("contradictions_log_ref")):
        reasons.append("contradictions_log_ref is empty")

    return not reasons, reasons


def audit_adjudication_envelope(envelope):
    """Audit a liaison adjudication envelope against BOTH gate invariants (the mechanical check).

    The shared validation source for `scripts/audit-medical-liaison-override.sh` and the in-code
    gate. An envelope is sound when it neither builds an override path for a non-overridable finding
    (INV-CRITICAL-NON-OVERRIDABLE) nor carries a content-invalid override record for an overridable
    one (INV-OVERRIDE-RECORD-SCHEMA). A HIGH/MEDIUM envelope with NO override record is sound — the
    operator simply has not overridden; the block stands.

    Args:
        envelope (dict): The liaison adjudication envelope.

    Returns:
        (bool) ok — whether the envelope violates neither invariant.
        (list) violations — one `{invariant, reason}` per violation (empty when ok).
    """
    violations = []
    if not isinstance(envelope, dict):
        return False, [{"invariant": "schema", "reason": "envelope is not an object"}]

    band = envelope.get("composite_band")
    harm_class = envelope.get("harm_class")
    override_record = envelope.get("override_record")
    set_by = (envelope.get("severity_final") or {}).get("set_by")

    if band not in BANDS:
        violations.append({"invariant": "schema", "reason": f"composite_band {band!r} not in {BANDS}"})

    if is_non_overridable(band, harm_class):
        if override_record is not None:
            violations.append({
                "invariant": "INV-CRITICAL-NON-OVERRIDABLE",
                "reason": "override path built for a CRITICAL / H1-H2 finding",
            })
        if set_by != AUTO_BLOCK_SENTINEL:
            violations.append({
                "invariant": "INV-CRITICAL-NON-OVERRIDABLE",
                "reason": f"severity_final.set_by must be {AUTO_BLOCK_SENTINEL!r} for a non-overridable finding",
            })
    elif override_record is not None:
        if set_by != LIAISON_SET_BY:
            violations.append({
                "invariant": "INV-OVERRIDE-RECORD-SCHEMA",
                "reason": f"severity_final.set_by must be {LIAISON_SET_BY!r} for an override record",
            })
        valid, reasons = validate_override_record(override_record, composite_band=band)
        if not valid:
            violations.extend(
                {"invariant": "INV-OVERRIDE-RECORD-SCHEMA", "reason": r} for r in reasons
            )

    return not violations, violations


def adjudicate(safety_finding, envelope):
    """Apply the liaison's adjudication of a held finding and return the terminal outcome.

    Args:
        safety_finding (dict): The held finding routed to the liaison (`finding_id` + `caution` +
            the held domain). The orchestrator builds it from the reconciler's additive-AE finding.
        envelope (dict): The liaison's adjudication envelope (its runtime-A output), or `None` when
            no adjudicator ran.

    Returns:
        (dict) outcome — `finding_id`, `outcome` (`cleared` | `block-stands`), `non_overridable`
        (bool), `reasons` (why, esp. for block-stands), `override_record` (the validated record
        when cleared, else `None`), and `severity_final` (echoed from the envelope).
    """
    finding_id = safety_finding.get("finding_id")
    held = {
        "finding_id": finding_id, "outcome": "block-stands", "non_overridable": False,
        "reasons": [], "override_record": None, "severity_final": None,
    }

    if not isinstance(envelope, dict):
        held["reasons"] = ["no adjudication (no envelope) — the block stands"]
        return held

    held["severity_final"] = envelope.get("severity_final")
    band = envelope.get("composite_band")
    harm_class = envelope.get("harm_class")

    if envelope.get("finding_id") != finding_id:
        held["reasons"] = ["envelope finding_id does not match the held finding — the block stands"]
        return held

    if is_non_overridable(band, harm_class):
        held["non_overridable"] = True
        # The envelope must NOT carry an override path; if it does, that is the invariant violation.
        ok, violations = audit_adjudication_envelope(envelope)
        held["reasons"] = (
            [AUTO_BLOCK_SENTINEL] if ok else [v["reason"] for v in violations]
        )
        return held

    if band not in OVERRIDABLE_BANDS:
        held["reasons"] = [f"composite_band {band!r} is not overridable — the block stands"]
        return held

    record = envelope.get("override_record")
    if record is None:
        held["reasons"] = ["no override record provided — the block stands"]
        return held

    if (envelope.get("severity_final") or {}).get("set_by") != LIAISON_SET_BY:
        held["reasons"] = [f"severity_final.set_by must be {LIAISON_SET_BY!r} — the block stands"]
        return held

    valid, reasons = validate_override_record(
        record, composite_band=band, caution=safety_finding.get("caution")
    )
    if not valid:
        held["reasons"] = reasons
        return held

    return {
        "finding_id": finding_id, "outcome": "cleared", "non_overridable": False,
        "reasons": [], "override_record": record, "severity_final": envelope.get("severity_final"),
    }


def _cli(argv=None):
    """`--audit-envelope <path.json>`: exit 0 when the envelope violates neither invariant, else 1."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--audit-envelope", metavar="PATH", required=True,
                        help="a liaison adjudication envelope JSON to audit against both invariants")
    args = parser.parse_args(argv)
    with open(args.audit_envelope) as handle:
        envelope = json.load(handle)
    ok, violations = audit_adjudication_envelope(envelope)
    if ok:
        print("OK: adjudication envelope violates neither gate invariant")
        return 0
    for violation in violations:
        print(f"VIOLATION [{violation['invariant']}]: {violation['reason']}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(_cli())
