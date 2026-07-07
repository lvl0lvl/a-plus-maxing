#!/usr/bin/env bash
# hygiene-audit.sh — PF/bead-hygiene audit family (ADR-0004, spec task T4).
#
# WHAT IT ENFORCES — "PF/bead records are property-audited for integrity."
# One script, TWO independent, individually-reportable PROPERTY-based sub-checks,
# each calling `fail` on its own violations, then a single terminal `verdict`:
#
#   G4 (count-reconciliation, giq.3.7) — the PF log self-reports a total
#     ("Total PF entries: N"). This check RECOMPUTES the count by enumerating the
#     ACTUAL PF entries in the log and FAILs when the recomputed count disagrees
#     with the self-reported N. It NEVER trusts the reported number (F-007:
#     property, not signal) — mirroring how harvest-gate.sh re-derives ids from
#     the source block rather than trusting a summary.
#
#   G6 (close-reason rationale, giq.5.2, rec=12) — every CLOSED bead in the
#     exported .beads/issues.jsonl must carry a NON-EMPTY close_reason. This check
#     inspects the actual close_reason FIELD CONTENT and FAILs on empty/whitespace
#     — it does NOT merely confirm `bd close` was called (the F-007 trap).
#
# ROSTER WIRING (do NOT edit close-audit.sh here): G4+G6 join the per-close
#   DEFAULT_ROSTER alongside rotation-stamp-audit / stale-hash-audit /
#   pf-attestation-audit. The orchestrator wires this script's name into
#   close-audit.sh's DEFAULT_ROSTER separately. G5 (severity-monotonicity) is a
#   SEPARATE per-harvest script (pf-severity-audit.sh, T5) — NOT part of this file
#   and NOT in the per-close roster.
#
# AUDIT_ALLOW_SKIP (ADR-0004): G4/G6 are property checks over artifacts that exist
#   at close; they run or FATAL on their OWN missing inputs and are not silently
#   neutralizable by the global AUDIT_ALLOW_SKIP hatch. If AUDIT_ALLOW_SKIP=1 is
#   set, a WARN is emitted naming this audit so a GREEN close cannot hide it.
#
# Exit codes (via verdict): 0 PASS / 1 FAIL (violation) / 2 FATAL (env/skip).
#
# Usage:
#   hygiene-audit.sh [--pf-log PATH] [--beads PATH]
#   PF_LOG / BEADS_JSONL env vars supply defaults.
# Defaults: PF log = ${PF_LOG:-./memory/process-failures.md};
#           beads   = ${BEADS_JSONL:-./.beads/issues.jsonl}.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="hygiene-audit"

PF_LOG="${PF_LOG:-./memory/process-failures.md}"
BEADS_JSONL="${BEADS_JSONL:-./.beads/issues.jsonl}"

while [ $# -gt 0 ]; do
  case "$1" in
    --pf-log)
      PF_LOG="${2:-}"
      [ -n "$PF_LOG" ] || { emit "FATAL: --pf-log requires a path"; exit 2; }
      shift 2 ;;
    --pf-log=*) PF_LOG="${1#--pf-log=}"; shift ;;
    --beads)
      BEADS_JSONL="${2:-}"
      [ -n "$BEADS_JSONL" ] || { emit "FATAL: --beads requires a path"; exit 2; }
      shift 2 ;;
    --beads=*) BEADS_JSONL="${1#--beads=}"; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) emit "FATAL: unknown flag: $1"; exit 2 ;;
    *)  emit "FATAL: unexpected positional arg: $1"; exit 2 ;;
  esac
done

# AUDIT_ALLOW_SKIP must NOT silently neutralize G4/G6 — log it as a named WARN.
if [ "${AUDIT_ALLOW_SKIP:-0}" = "1" ]; then
  warn "AUDIT_ALLOW_SKIP=1 is set; hygiene-audit (G4/G6) is NOT neutralizable by it — G4/G6 still run or FATAL on their own missing inputs"
fi

# Both inputs are artifacts that exist at a session close; a missing one is an env
# error the operator must fix, not a clean pass (F-008 fail-closed).
[ -f "$PF_LOG" ]      || { emit "FATAL: PF log not found: $PF_LOG (set --pf-log or PF_LOG)"; exit 2; }
[ -f "$BEADS_JSONL" ] || { emit "FATAL: beads JSONL not found: $BEADS_JSONL (set --beads or BEADS_JSONL)"; exit 2; }

emit "G4 PF log: $PF_LOG ; G6 beads: $BEADS_JSONL"

# =============================================================================
# G4 — count-reconciliation (PROPERTY: recompute, never trust the reported total)
# =============================================================================
# Read the self-reported total: a line "Total PF entries: N" (case-insensitive,
# tolerant of leading markdown/whitespace and surrounding bold markers).
reported_line="$(grep -iE '^[[:space:]]*[#*_ ]*total[[:space:]]+PF[[:space:]]+entries[[:space:]]*:' "$PF_LOG" 2>/dev/null | head -n1 || true)"

if [ -z "$reported_line" ]; then
  # No self-reported total to reconcile against. A count check with no reported
  # number cannot assert the property — fail-closed (couldn't run), not a pass.
  skipped "G4: no 'Total PF entries: N' self-report line found in $PF_LOG — nothing to reconcile against (fail-closed)"
else
  reported_count="$(printf '%s' "$reported_line" \
    | sed -E 's/.*[Tt]otal[[:space:]]+PF[[:space:]]+entries[[:space:]]*:[[:space:]]*\*?_?([0-9]+).*/\1/')"
  case "$reported_count" in
    ''|*[!0-9]*)
      skipped "G4: could not parse an integer from the total line: $reported_line (fail-closed)" ;;
    *)
      # RECOMPUTE: enumerate the ACTUAL PF entries. A PF entry is a line that
      # DECLARES a PF id at the start of content: 'PF-S<n>-<nn>:' (optionally
      # behind markdown list/whitespace). We never read the reported number for
      # this — it is derived purely from the log body.
      actual_count="$(grep -cE '^[[:space:]]*[-*]?[[:space:]]*PF-S[0-9]+-[0-9]+[[:space:]]*:' "$PF_LOG" 2>/dev/null || true)"
      # grep -c can emit nothing on some platforms when 0 matches under pipefail.
      [ -n "$actual_count" ] || actual_count=0
      emit "G4: reported total=$reported_count ; recomputed from actual PF entries=$actual_count"
      if [ "$reported_count" != "$actual_count" ]; then
        fail "G4: PF count mismatch — self-reported $reported_count but actual entry enumeration found $actual_count (count drift; the reported number is not trusted — giq.3.7)"
      else
        emit "G4: PF count reconciles ($actual_count)"
      fi ;;
  esac
fi

# =============================================================================
# G6 — close-reason rationale (PROPERTY: inspect close_reason field CONTENT)
# =============================================================================
# Scan every CLOSED bead record. A closed bead is a JSON line with
# '"status":"closed"'. For each, read its top-level "close_reason" value and FAIL
# when that value is empty or only whitespace. Reading the field content (not the
# mere presence of a closed record) is the property — an always-pass stub that
# trusts "the bead is closed" false-greens an empty reason.
g6_checked=0
g6_bad=0
while IFS= read -r bline || [ -n "$bline" ]; do
  case "$bline" in
    ''|\#*) continue ;;
  esac
  # Only closed records are subject to the close_reason requirement.
  case "$bline" in
    *'"status":"closed"'*|*'"status": "closed"'*) : ;;
    *) continue ;;
  esac
  g6_checked=$((g6_checked + 1))
  # Extract the bead id for diagnostics.
  bid="$(printf '%s\n' "$bline" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  [ -n "$bid" ] || bid="<unknown-id>"
  if ! printf '%s' "$bline" | grep -q '"close_reason"'; then
    # Closed but no close_reason field at all — the tracker did not export the
    # rationale we require. Fail-closed (cannot assert clean; ADR-0004 negative).
    fail "G6: closed bead '$bid' has NO close_reason field — closed without a recorded rationale (giq.5.2)"
    g6_bad=$((g6_bad + 1))
    continue
  fi
  # Read the close_reason value content (the substring between its quotes).
  # Portable extraction (BSD + GNU): take everything after the opening quote of
  # the close_reason value, then strip from the first unescaped closing quote on.
  # A non-greedy match isn't available in POSIX sed, so we cut the value as the
  # text up to the next '"' — close_reason values do not contain raw quotes in
  # the exported JSONL (they would be \"-escaped, which we tolerate below).
  reason="$(printf '%s\n' "$bline" | sed -n 's/.*"close_reason"[[:space:]]*:[[:space:]]*"//p')"
  reason="${reason%%\"*}"
  # Strip escaped whitespace tokens (\t \n) and all literal whitespace, leaving
  # only substantive characters to test against.
  reason_trimmed="$(printf '%s' "$reason" | sed -E 's/\\[tn]//g' | tr -d '[:space:]')"
  if [ -z "$reason_trimmed" ]; then
    fail "G6: closed bead '$bid' has an empty/whitespace close_reason — rationale-free close (giq.5.2; inspecting field content, not just that bd close ran)"
    g6_bad=$((g6_bad + 1))
  fi
done < "$BEADS_JSONL"

emit "G6: inspected $g6_checked closed bead(s); $g6_bad rationale-free"

verdict
