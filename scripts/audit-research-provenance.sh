#!/usr/bin/env bash
# audit-research-provenance.sh — the mechanical research-provenance gate (bead bda).
#
# Mechanical enforcement for INV-RESEARCH-PROVENANCE-DISJOINT: a specialist's
# `design/.<slug>-design-work/` research provenance must be produced by the gated
# `/aplus-research` path, never a generic Workflow / hand-rolled fan-out, and
# never the orchestrator grading its own research.
#
# WHY THIS EXISTS (PF-S17-01, recurrence_count=2):
#   `gate_attest.py verify-chain` alone is NOT sufficient. It iterates the attested
#   gates and `continue`s past any that are ABSENT — so a design-work dir with ZERO
#   gate JSONs returns an empty failure list and exits 0 (a vacuous PASS). It catches
#   a TAMPERED chain, not an ABSENT one. At S18, personal-trainer + lymphatic shipped
#   real dispatched judge JSONs but NO gates/ dir, and gi shipped only 2 of its
#   mode-required attested gates — all three would have falsely "passed" verify-chain.
#
#   This script closes that hole: it asserts the mode-required attested gates are
#   PRESENT (with an attestation_chain) BEFORE delegating chain-integrity to
#   verify-chain. Presence-then-integrity.
#
# AUTHORITATIVE GATE SET: the SKILL.md gate-by-mode matrix (Walter, S18 decision).
#   .claude/skills/aplus-research/SKILL.md "Gate-by-mode matrix":
#     Gate              quick  standard  deep  ultradeep
#     2.75 SCOPE         ✓       ✓        ✓      ✓     (schema-only; not attestation-chained)
#     3.5  JUDGE         ✓       ✓        ✓      ✓
#     4.25 ID-RECONCILE  -       ✓        ✓      ✓
#     4.75 INTEGRITY     -       ✓        ✓      ✓
#     6    CRITIQUE      -       -        ✓      ✓
#     7.5  RISK-FLOOR    -       ✓        ✓      ✓     (compounds only)
#     8.5  LAYERS        -       ✓        ✓      ✓     (standard+ compounds only)
#
#   ATTESTED_GATES (gate_attest.py) = 3.5 4.25 4.75 6 7.5 8.5  (2.75 is schema-only).
#   7.5 + 8.5 are compound-target-only; gated on target_class==compound from the
#   risk table. (The phase-7.5 docstring further narrows risk-floor to
#   risk_tier=experimental; bda takes the matrix's stricter "compounds at standard+"
#   reading — a compound specialist that legitimately ran no experimental risk-floor
#   should record that as a PASS gate-7.5.json, not omit it. Documented; revisit via
#   change-discipline if it proves over-strict.)
#
# USAGE:
#   audit-research-provenance.sh <design-work-dir> <slug>
#     <design-work-dir>  e.g. design/.gi-specialist-design-work  (the dir containing gates/)
#     <slug>             e.g. gi-specialist  (keys mode_floor + target_class in the risk table)
#
# EXIT CODES:
#   0 — provenance intact (required attested gates present + verify-chain intact)
#   1 — one or more violations (missing gate / no attestation_chain / chain broken)
#   2 — usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/audit-helpers.sh"

RISK_TABLE="$REPO_ROOT/templates/specialist-risk-class.yaml"
GATE_ATTEST="$REPO_ROOT/.claude/skills/aplus-research/lib/gate_attest.py"

die() { echo "audit-research-provenance: $*" >&2; exit 2; }

[ "$#" -eq 2 ] || die "usage: audit-research-provenance.sh <design-work-dir> <slug>"
WORKDIR="$1"
SLUG="$2"

[ -d "$WORKDIR" ] || die "design-work dir not found: $WORKDIR"
[ -f "$RISK_TABLE" ] || die "risk table not found: $RISK_TABLE"
[ -f "$GATE_ATTEST" ] || die "gate_attest.py not found: $GATE_ATTEST"

audit_init "audit-research-provenance($SLUG)"

# --- resolve mode_floor + target_class from the risk table (same awk pattern as
#     audit-specialist-profile.sh: enter the slug's block, read the first matching
#     key, stop at the next top-level slug key) ---
yaml_field() { # <field-name>
    awk -v s="$SLUG:" -v key="$1:" '
        $0 ~ ("^  " s) {f=1; next}
        f && $0 ~ ("^    " key) {print $2; exit}
        /^  [a-z]/ {if (f) exit}
    ' "$RISK_TABLE"
}

MODE_FLOOR="$(yaml_field mode_floor)"
TARGET_CLASS="$(yaml_field target_class)"

if [ -z "$MODE_FLOOR" ]; then
    violation "INV-RESEARCH-PROVENANCE-DISJOINT" \
        "slug '$SLUG' has no mode_floor in $RISK_TABLE — cannot determine required gates"
    audit_summary; audit_exit
fi

# Collation-only roles (mode_floor: none / not_applicable) dispatch no research.
case "$MODE_FLOOR" in
    none|not_applicable)
        info "$SLUG is collation-only (mode_floor=$MODE_FLOOR) — no research dispatch; provenance gate N/A"
        audit_summary; audit_exit
        ;;
esac

info "mode_floor=$MODE_FLOOR target_class=${TARGET_CLASS:-<unset>}"

# --- compute the REQUIRED attestation-chained gate set for this (mode, target) ---
# Base sets per mode (attestation-chained gates only; 2.75 handled separately).
case "$MODE_FLOOR" in
    quick)              required="3.5" ;;
    standard)           required="3.5 4.25 4.75" ;;
    deep|ultradeep)     required="3.5 4.25 4.75 6" ;;
    *) die "unknown mode_floor '$MODE_FLOOR' for $SLUG (expected quick|standard|deep|ultradeep)" ;;
esac

# Compound-target-only gates (7.5 risk-floor, 8.5 layers) fire at standard+.
if [ "$TARGET_CLASS" = "compound" ] && [ "$MODE_FLOOR" != "quick" ]; then
    required="$required 7.5 8.5"
fi

info "required attested gates: $required"

# --- canonical layout check (PF-S18: builders diverged on the gates dir name) ---
# gate_attest.py is the ONLY sanctioned gate producer; it reads/writes `gates/`
# (hardcoded in SOURCE_MD + verify_chain). A design-work dir using any other
# layout (e.g. supplement-specialist's `research-gates/`) was NOT produced by the
# canonical tool — that is itself the unverifiable-provenance failure bda exists
# to catch. Report it accurately rather than as a misleading "missing gate".
if [ ! -d "$WORKDIR/gates" ] && [ -d "$WORKDIR/research-gates" ]; then
    violation "INV-RESEARCH-PROVENANCE-DISJOINT" \
        "non-canonical gates layout: found research-gates/ but no gates/ — gate JSONs were not produced by the canonical gate_attest.py (which reads/writes gates/). verify-chain cannot validate this layout; re-run Phase-0 through /aplus-research so gate_attest.py emits the canonical gates/ chain."
fi

# --- 2.75 SCOPE gate: present in every mode (schema-only, not attestation-chained) ---
if [ ! -f "$WORKDIR/gates/gate-2.75.json" ]; then
    violation "INV-RESEARCH-PROVENANCE-DISJOINT" \
        "missing gates/gate-2.75.json (SCOPE gate — fires in every mode; a run with no scope gate in the canonical gates/ dir did not enter the gated path)"
fi

# --- PRESENCE + attestation_chain shape for each required attested gate ---
# This is the assertion verify-chain cannot make: an ABSENT gate is the failure mode.
for g in $required; do
    gj="$WORKDIR/gates/gate-$g.json"
    if [ ! -f "$gj" ]; then
        violation "INV-RESEARCH-PROVENANCE-DISJOINT" \
            "missing required gate-$g.json for mode=$MODE_FLOOR target=${TARGET_CLASS:-?} (vacuous-pass hole: verify-chain skips absent gates)"
        continue
    fi
    # Must carry a non-null attestation_chain — an orchestrator-fabricated gate
    # JSON without one is exactly what PF-S3-01 forbids.
    if ! python3 -c "
import json,sys
try:
    d=json.load(open('$gj'))
except Exception as e:
    sys.exit(3)
sys.exit(0 if d.get('attestation_chain') else 4)
" 2>/dev/null; then
        violation "INV-RESEARCH-GATE-ATTESTATION" \
            "gate-$g.json present but has no attestation_chain (orchestrator-fabricated gate JSON)"
    fi
done

# --- delegate chain-integrity (source files exist + sha256 match) to gate_attest.py ---
# verify-chain validates every attested gate that IS present; combined with the
# presence checks above, absent-AND-tampered are both now caught.
vc_out="$(python3 "$GATE_ATTEST" verify-chain --base "$WORKDIR" 2>&1)" && vc_rc=0 || vc_rc=$?
if [ "$vc_rc" -ne 0 ]; then
    while IFS= read -r line; do
        [ -n "$line" ] && violation "INV-RESEARCH-GATE-ATTESTATION" "verify-chain: $line"
    done <<< "$vc_out"
else
    info "verify-chain: $vc_out"
fi

audit_summary
audit_exit
