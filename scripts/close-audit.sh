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
# Test hooks (NEVER set in production — a loud WARNING is emitted if any is set,
# PR #139 SEC-002/F2):
#   CLOSE_AUDIT_SKIP_FLOOR=1   skip the run-all-tests floor (unit-test isolation)
#   CLOSE_AUDIT_ROSTER         newline list of "script|args" (override roster)
#   CLOSE_AUDIT_ROSTER_DIR     dir holding roster scripts (default: this dir)
#   CLOSE_AUDIT_FLOORS         newline list of floor scripts (override; default =
#                              toolkit + a-plus run-all-tests.sh) — F7 testability
#   CLOSE_AUDIT_FLOOR_EXCLUDE / _REASON  forwarded to the a-plus floor's
#                              RUN_ALL_TESTS_EXCLUDE (documented pre-existing red)
#   CLOSE_AUDIT_FSCAN          override the falsification-scan binary (advisory)
#   CLOSE_AUDIT_PFLOG          override the PF-log path the advisory scans

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
    --session=*)  SESSION="${1#*=}"; [ -n "$SESSION" ] || { echo "close-audit: --session= needs a value" >&2; exit 2; } ;;
    --allow-skip) AUDIT_ALLOW_SKIP=1 ;;
    -h|--help)    sed -n '2,46p' "$0"; exit 0 ;;
    *)            echo "close-audit: unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

# F2 (PR #139 SEC-002): surface accidental production use of a test-hook env var.
for _thv in CLOSE_AUDIT_SKIP_FLOOR CLOSE_AUDIT_ROSTER CLOSE_AUDIT_ROSTER_DIR CLOSE_AUDIT_FLOORS CLOSE_AUDIT_FLOOR_EXCLUDE CLOSE_AUDIT_FSCAN CLOSE_AUDIT_PFLOG; do
  if [ -n "${!_thv:-}" ]; then
    echo "close-audit: WARNING: test-hook env var ${_thv} is active (intended for tests/CI only — NOT a production close)" >&2
  fi
done

# --- FLOOR: prove the audits can still FAIL on bad input (F-007) -------------
# No default exclusion (S65): the former tracked red — test_audit_research_provenance
# (gate_attest verify-chain needed jsonschema) — was FIXED (bead d1kc: jsonschema
# installed into .venv + the audit points at the .venv python), so the full floor now
# runs green. The override remains for any FUTURE tracked pre-existing red, LOUDLY
# (RUN_ALL_TESTS prints the EXCLUDED line + reason; a stale exclusion fails the run,
# so it can never rot silently).
export RUN_ALL_TESTS_EXCLUDE="${CLOSE_AUDIT_FLOOR_EXCLUDE:-}"
export RUN_ALL_TESTS_EXCLUDE_REASON="${CLOSE_AUDIT_FLOOR_EXCLUDE_REASON:-no reason given}"

# Floors are injectable (CLOSE_AUDIT_FLOORS, newline list) so the negative test
# can drive a failing / missing floor without disabling the block (F7/TEST-001).
DEFAULT_FLOORS="${REPO_ROOT}/toolkit/tests/run-all-tests.sh
${SELF_DIR}/tests/run-all-tests.sh"
FLOORS="${CLOSE_AUDIT_FLOORS:-$DEFAULT_FLOORS}"

if [ "${CLOSE_AUDIT_SKIP_FLOOR:-0}" != "1" ]; then
  while IFS= read -r floor; do
    [ -n "$floor" ] || continue
    if [ ! -f "$floor" ]; then
      skipped "negative-test floor missing: $floor"
      continue
    fi
    if bash "$floor" >/dev/null 2>&1; then
      info "floor OK: $floor"
    else
      violation INV-CLOSE-AUDIT "negative-test floor FAILED: ${floor} (an audit cannot prove it goes RED — a green close cannot be trusted)"
    fi
  done <<EOF
$FLOORS
EOF
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
  local entry="$1" script args path rc=0
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
  # word-split $args intentionally (heterogeneous per-audit flags)
  # shellcheck disable=SC2086
  bash "$path" $args >/dev/null 2>&1 || rc=$?
  if [ "$rc" -eq 0 ]; then
    info "PASS: ${script}${args:+ $args}"
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

# --- ADVISORY: falsification-scan over THIS session's PF note (Wave B) --------
# NON-GATING by design (framework Failure-Mode Discipline). falsification-scan is
# a heuristic prose matcher — WARN-only. It surfaces the four falsification anti-
# patterns (increment-by-default / framework-circularity / a-priori-by-construction
# / soft-confirmation-laundering) for the operator/reviewer to confirm or dismiss;
# it NEVER changes this gate's verdict. Scanned over ONLY the current session's PF
# section — scanning the whole log would false-WARN on historical entries that
# quote an anti-pattern in order to refute it. The vendored toolkit script is
# invoked, never edited. Its exit code is intentionally discarded (info-only).
FSCAN="${CLOSE_AUDIT_FSCAN:-${REPO_ROOT}/toolkit/scripts/falsification-scan.sh}"
PFLOG="${CLOSE_AUDIT_PFLOG:-${REPO_ROOT}/memory/process-failures.md}"
if [ -n "$SESSION" ] && [ -f "$FSCAN" ] && [ -f "$PFLOG" ]; then
  # Match the session header EXACTLY (number followed by a non-digit or EOL) so
  # `## Session 6` does not prefix-match `## Session 65`; stop at the next
  # `## Session ` header of any number (PR #141 F-A).
  pf_section="$(awk -v n="${SESSION}" '
    $0 ~ ("^## Session " n "([^0-9]|$)") { grab = 1; print; next }
    grab && /^## Session / { exit }
    grab { print }
  ' "$PFLOG")"
  if [ -n "$pf_section" ]; then
    fs_out="$(printf '%s\n' "$pf_section" | bash "$FSCAN" --allow-skip 2>&1)" || true
    info "falsification-scan (ADVISORY, non-gating) over Session ${SESSION} PF note:"
    while IFS= read -r _l; do [ -n "$_l" ] && info "  fscan: ${_l}"; done <<< "$fs_out"
  else
    info "falsification-scan (ADVISORY): no '## Session ${SESSION}' PF section to scan yet"
  fi
fi

audit_summary
audit_exit
