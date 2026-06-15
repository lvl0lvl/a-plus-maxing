#!/usr/bin/env bash
# scripts/close-audit.sh — the mandatory session-CLOSE GATE (a-plus).
#
# WHAT IT ENFORCES (Rigor Framework v1.0.0, Discipline 1 step 7 / F-008):
#   A "clean close" / "all audits GREEN" attestation is honest only if every
#   constituent audit GENUINELY RAN and returned 0 in the same close cycle.
#   "Couldn't verify" != "verified clean". So this gate:
#     - runs the negative-test FLOOR first (toolkit + a-plus run-all-tests.sh),
#       proving each audit can still go RED on bad input before it is trusted to
#       go green (F-007);
#     - then runs a-plus's per-close roster, mapping each: exit 0 -> PASS,
#       exit 1 -> FAIL (a real violation), exit >=2 / missing -> SKIPPED
#       (fail-closed FATAL — a check that could not run must not pass).
#
# ADOPTION NOTE: this embodies the toolkit/scripts/close-audit.sh pattern
#   (the upstream for future pulls) but is purpose-built for a-plus's bespoke
#   roster, whose audits take heterogeneous args (some need --session, some do
#   not) — which the toolkit's single-child-arg forwarding cannot express. The
#   bespoke audits are kept (more evolved / domain-specific); this gate
#   orchestrates them. Per-close blocking roster = CLAUDE.md close step 8.5:
#     handoff-audit, scope-contract-audit, pf-attestation-audit,
#     skill-trace-audit, branch-completeness-audit.
#   audit-research-provenance is CONDITIONAL (run separately per step 8.5 only
#   when an aplus-research dispatch occurred), so it is NOT in this roster.
#
# USAGE: close-audit.sh --session N [--allow-skip]
# EXIT:  0 PASS / 1 FAIL (a constituent violation) / 2 FATAL (a constituent or
#        the floor could not run — fail-closed).
#
# Test hooks (NEVER set in production):
#   CLOSE_AUDIT_SKIP_FLOOR=1   skip the run-all-tests floor (unit-test isolation)
#   CLOSE_AUDIT_ROSTER         newline list of "script|args" (override roster)
#   CLOSE_AUDIT_ROSTER_DIR     dir holding roster scripts (default: this dir)
#   CLOSE_AUDIT_FLOOR_EXCLUDE / _REASON  forwarded to the a-plus floor's
#                              RUN_ALL_TESTS_EXCLUDE (documented pre-existing red)

set -uo pipefail

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SELF_DIR/.." && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SELF_DIR/lib/audit-helpers.sh"
audit_init "close-audit"

SESSION=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --session)    shift; SESSION="${1:-}"; [ -n "$SESSION" ] || { echo "close-audit: --session needs a value" >&2; exit 2; } ;;
    --session=*)  SESSION="${1#*=}" ;;
    --allow-skip) AUDIT_ALLOW_SKIP=1 ;;
    -h|--help)    sed -n '2,40p' "$0"; exit 0 ;;
    *)            echo "close-audit: unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

# --- FLOOR: prove the audits can still FAIL on bad input (F-007) -------------
# Default-exclude the one tracked pre-existing environmental red from the a-plus
# floor, LOUDLY (RUN_ALL_TESTS prints the EXCLUDED line + reason — never silent).
export RUN_ALL_TESTS_EXCLUDE="${CLOSE_AUDIT_FLOOR_EXCLUDE:-test_audit_research_provenance.sh}"
export RUN_ALL_TESTS_EXCLUDE_REASON="${CLOSE_AUDIT_FLOOR_EXCLUDE_REASON:-pre-existing environmental failure: gate_attest verify-chain needs jsonschema (absent here); tracked by bead. Tests a CONDITIONAL audit, not a per-close roster member.}"

if [ "${CLOSE_AUDIT_SKIP_FLOOR:-0}" != "1" ]; then
  for floor in "$REPO_ROOT/toolkit/tests/run-all-tests.sh" "$SELF_DIR/tests/run-all-tests.sh"; do
    if [ ! -f "$floor" ]; then
      skipped "negative-test floor missing: $floor"
      continue
    fi
    if bash "$floor" >/dev/null 2>&1; then
      info "floor OK: $floor"
    else
      violation INV-CLOSE-AUDIT "negative-test floor FAILED: ${floor} (an audit cannot prove it goes RED — a green close cannot be trusted)"
    fi
  done
fi

# --- per-close roster --------------------------------------------------------
DEFAULT_ROSTER="handoff-audit.sh
scope-contract-audit.sh|--session {SESSION}
pf-attestation-audit.sh|--session {SESSION}
skill-trace-audit.sh|--session {SESSION}
branch-completeness-audit.sh"

ROSTER="${CLOSE_AUDIT_ROSTER:-$DEFAULT_ROSTER}"
ROSTER_DIR="${CLOSE_AUDIT_ROSTER_DIR:-$SELF_DIR}"

run_one() {
  entry="$1"
  script="${entry%%|*}"
  args="${entry#"$script"}"; args="${args#|}"
  case "$args" in
    *"{SESSION}"*)
      if [ -z "$SESSION" ]; then
        violation INV-CLOSE-AUDIT "${script} requires --session but none was given"
        return
      fi
      args="${args//\{SESSION\}/$SESSION}"
      ;;
  esac
  path="${ROSTER_DIR}/${script}"
  if [ ! -f "$path" ]; then
    skipped "constituent missing: ${script} (${path}) — cannot run, cannot attest"
    return
  fi
  rc=0
  # word-split $args intentionally (heterogeneous per-audit flags)
  # shellcheck disable=SC2086
  bash "$path" $args >/dev/null 2>&1 || rc=$?
  if [ "$rc" -eq 0 ]; then
    info "PASS: ${script} ${args}"
  elif [ "$rc" -eq 1 ]; then
    violation INV-CLOSE-AUDIT "constituent FAILed: ${script} ${args} (exit 1)"
  else
    skipped "constituent could not run: ${script} ${args} (exit ${rc})"
  fi
}

while IFS= read -r entry; do
  [ -n "$entry" ] || continue
  run_one "$entry"
done <<EOF
$ROSTER
EOF

audit_summary
audit_exit
