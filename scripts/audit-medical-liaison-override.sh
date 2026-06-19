#!/usr/bin/env bash
# audit-medical-liaison-override.sh — mechanical gate for the two medical-liaison
#   adjudication invariants (medical-liaison design §16 OQ-3, bead mdv):
#
#   INV-OVERRIDE-RECORD-SCHEMA      — an override record is validated on CONTENT, not
#                                     presence (canonical literal, content-bearing
#                                     operator_reason at the band rung, risks-of-
#                                     proceeding, contradictions-log ref). A presence-only
#                                     record (the rubber-stamp) is REJECTED.
#   INV-CRITICAL-NON-OVERRIDABLE    — a CRITICAL / H1-H2 finding never carries an override
#                                     path; an envelope that builds one is a VIOLATION.
#
# It delegates to `scripts/plan/adjudicate.py --audit-envelope` — the SAME
# `audit_adjudication_envelope` the in-code gate runs — so the bash audit and the
# runtime gate share ONE validation source and cannot drift (F-007 keep-them-equal).
# The adjudicate CLI is stdlib-only (no jsonschema), so this gate runs under a bare
# `python3` when no project `.venv` is present (e.g. a fresh worktree).
#
# USAGE:
#   audit-medical-liaison-override.sh <adjudication-envelope.json>
#
# EXIT CODES (audit-helpers F-008 contract):
#   0 — the envelope violates neither invariant (sound)
#   1 — one or more invariant violations
#   2 — usage error / the validator could not run (must-not-pass)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/audit-helpers.sh"

ADJUDICATE="$REPO_ROOT/scripts/plan/adjudicate.py"
PY="$REPO_ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3 || true)"

die() { echo "audit-medical-liaison-override: $*" >&2; exit 2; }

[ "$#" -eq 1 ] || die "usage: audit-medical-liaison-override.sh <adjudication-envelope.json>"
ENVELOPE="$1"
[ -f "$ENVELOPE" ] || die "envelope not found: $ENVELOPE"
[ -f "$ADJUDICATE" ] || die "adjudicate.py not found: $ADJUDICATE"
[ -n "$PY" ] || die "no python interpreter found (.venv or python3)"

audit_init "audit-medical-liaison-override"

OUT="$("$PY" "$ADJUDICATE" --audit-envelope "$ENVELOPE" 2>&1)"
RC=$?

case "$RC" in
    0)
        info "adjudication envelope sound: $ENVELOPE"
        ;;
    1)
        # adjudicate.py prints `VIOLATION [INV-...]: reason` per violation; surface each.
        while IFS= read -r line; do
            case "$line" in
                *"VIOLATION ["*)
                    inv="${line#*VIOLATION [}"; inv="${inv%%]*}"
                    violation "$inv" "${line#*]: }"
                    ;;
            esac
        done <<< "$OUT"
        # Fail closed: a non-zero validator with no parseable violation still must not pass.
        [ "$(audit_count)" -gt 0 ] || violation "INV-OVERRIDE-RECORD-SCHEMA" "validator rejected the envelope: $OUT"
        ;;
    *)
        skipped "validator could not run (exit $RC): $OUT"
        ;;
esac

audit_summary
audit_exit
