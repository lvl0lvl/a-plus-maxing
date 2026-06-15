#!/usr/bin/env bash
# test_close_audit.sh — negative test for scripts/close-audit.sh (F-007).
#
# Proves the close gate goes RED on bad input: a constituent that FAILs -> exit 1,
# a constituent that cannot run (exit >=2 or missing) -> exit 2 (fail-closed),
# FAIL precedence over a skip, and a clean roster -> exit 0. Roster cases run with
# CLOSE_AUDIT_SKIP_FLOOR=1 + a FIXTURE roster so the exit-code mapping is tested in
# isolation. The FLOOR cases instead INJECT a fixture floor via CLOSE_AUDIT_FLOORS
# (no SKIP_FLOOR) so the floor block's own RED paths are exercised (PR #139 F7).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLOSE_AUDIT="$SCRIPT_DIR/../close-audit.sh"

PASS=0
FAIL=0
assert_rc() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "  PASS: $label (exit $actual)"; PASS=$((PASS + 1))
  else
    echo "  FAIL: $label (expected $expected, got $actual)"; FAIL=$((FAIL + 1))
  fi
}
assert_contains() {
  local label="$1" needle="$2" hay="$3"
  if [[ "$hay" == *"$needle"* ]]; then
    echo "  PASS: $label"; PASS=$((PASS + 1))
  else
    echo "  FAIL: $label (missing: $needle)"; FAIL=$((FAIL + 1))
  fi
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/alpha-audit.sh"
printf '#!/usr/bin/env bash\nexit 1\n' > "$TMP/beta-audit.sh"
printf '#!/usr/bin/env bash\nexit 2\n' > "$TMP/gamma-audit.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/needs-session-audit.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/floor-ok.sh"
printf '#!/usr/bin/env bash\nexit 1\n' > "$TMP/floor-fail.sh"
chmod +x "$TMP"/*.sh

run() { # $1 = roster; CLOSE_AUDIT_SKIP_FLOOR=1 isolates the roster mapping from the floor
  CLOSE_AUDIT_SKIP_FLOOR=1 CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="$1" \
    bash "$CLOSE_AUDIT" --session 64 >/dev/null 2>&1
}

# --- roster-mapping cases (floor skipped) ---
# C1: a clean roster -> PASS (0)
run "alpha-audit.sh"; assert_rc "all-clean roster passes" 0 $?
# C2: a FAILing constituent -> FAIL (1)
run $'alpha-audit.sh\nbeta-audit.sh'; assert_rc "a violation fails the gate" 1 $?
# C3: a could-not-run constituent (exit 2) -> FATAL (2)
run $'alpha-audit.sh\ngamma-audit.sh'; assert_rc "a fatal constituent fails closed" 2 $?
# C4: a missing constituent -> FATAL (2)
run $'alpha-audit.sh\nnonexistent-audit.sh'; assert_rc "a missing constituent fails closed" 2 $?
# C5: FAIL precedence over a skip -> 1
run $'beta-audit.sh\ngamma-audit.sh'; assert_rc "violation takes precedence over skip" 1 $?
# C6: {SESSION} substitution runs clean -> PASS
run "needs-session-audit.sh|--session {SESSION}"; assert_rc "{SESSION} substitution runs clean" 0 $?

# C7: {SESSION} required but --session OMITTED -> violation (exit 1, NOT FATAL 2):
#     the audit COULD run with a session; absence is caller error => a violation.
CLOSE_AUDIT_SKIP_FLOOR=1 CLOSE_AUDIT_ROSTER_DIR="$TMP" \
  CLOSE_AUDIT_ROSTER="needs-session-audit.sh|--session {SESSION}" \
  bash "$CLOSE_AUDIT" >/dev/null 2>&1
assert_rc "omitted --session for a templated audit is a violation (1, not FATAL 2)" 1 $?

# C8 (F5/F10): --session= (empty equals form) is a usage error -> exit 2, matching
#     the space form, BEFORE any roster runs.
CLOSE_AUDIT_SKIP_FLOOR=1 CLOSE_AUDIT_ROSTER_DIR="$TMP" \
  CLOSE_AUDIT_ROSTER="needs-session-audit.sh|--session {SESSION}" \
  bash "$CLOSE_AUDIT" --session= >/dev/null 2>&1
assert_rc "--session= (empty) is a usage error (exit 2)" 2 $?

# C9: --allow-skip downgrades a could-not-run to non-blocking -> PASS (0)
CLOSE_AUDIT_SKIP_FLOOR=1 CLOSE_AUDIT_ROSTER_DIR="$TMP" \
  CLOSE_AUDIT_ROSTER=$'alpha-audit.sh\ngamma-audit.sh' \
  bash "$CLOSE_AUDIT" --session 64 --allow-skip >/dev/null 2>&1
assert_rc "--allow-skip lets a skip pass" 0 $?

# C10 (F8): --allow-skip does NOT swallow a real FAIL -> still 1
CLOSE_AUDIT_SKIP_FLOOR=1 CLOSE_AUDIT_ROSTER_DIR="$TMP" \
  CLOSE_AUDIT_ROSTER=$'beta-audit.sh\ngamma-audit.sh' \
  bash "$CLOSE_AUDIT" --session 64 --allow-skip >/dev/null 2>&1
assert_rc "--allow-skip does not swallow a violation" 1 $?

# --- floor cases (floor INJECTED, not skipped) — F7/TEST-001 ---
# C11: floor that FAILS -> violation -> exit 1 (a clean roster must not rescue it)
CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-fail.sh" \
  bash "$CLOSE_AUDIT" --session 64 >/dev/null 2>&1
assert_rc "a FAILING floor fails the gate (1)" 1 $?

# C12: floor MISSING -> skipped -> FATAL exit 2 (cannot prove the audits bite)
CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/nonexistent-floor.sh" \
  bash "$CLOSE_AUDIT" --session 64 >/dev/null 2>&1
assert_rc "a MISSING floor fails closed (2)" 2 $?

# C13: floor OK + clean roster -> PASS (0) (the happy floor path)
CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  bash "$CLOSE_AUDIT" --session 64 >/dev/null 2>&1
assert_rc "a passing floor + clean roster passes (0)" 0 $?

# C14 (Wave B): the falsification-scan advisory is NON-GATING. A PF section that
#     trips an anti-pattern (increment-by-default) WARNs but must NOT change the
#     gate verdict — a clean roster + clean floor still exits 0, and the WARN is
#     surfaced (advisory ran, info-only). Uses the REAL vendored toolkit scan.
printf '## Session 64 (2026-06-15)\nWe decided every clean run advances n regardless of region.\n' > "$TMP/pf-fixture.md"
out=$(CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  CLOSE_AUDIT_FSCAN="$SCRIPT_DIR/../../toolkit/scripts/falsification-scan.sh" \
  CLOSE_AUDIT_PFLOG="$TMP/pf-fixture.md" \
  bash "$CLOSE_AUDIT" --session 64 2>&1)
assert_rc "falsification advisory does not gate a clean close" 0 $?
assert_contains "advisory surfaced the anti-pattern WARN" "increment-by-default" "$out"

# C15 (PR #141 F-D): a scan that EXITS NON-ZERO must still not gate — proving the
#     `|| true` exit-discard is load-bearing (the C14 real-scan exits 0, so it could
#     not exercise this). Inject a stub fscan that emits a WARN and `exit 2`s.
printf '#!/usr/bin/env bash\necho "increment-by-default (stub)"; exit 2\n' > "$TMP/fscan-exit2.sh"
chmod +x "$TMP/fscan-exit2.sh"
out=$(CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  CLOSE_AUDIT_FSCAN="$TMP/fscan-exit2.sh" \
  CLOSE_AUDIT_PFLOG="$TMP/pf-fixture.md" \
  bash "$CLOSE_AUDIT" --session 64 2>&1)
assert_rc "advisory scan exiting 2 does NOT gate the close (|| true is load-bearing)" 0 $?

# C16 (PR #141 F-A): exact-session scoping — `--session 6` must NOT bleed `## Session 65`.
#     The increment-by-default phrase lives ONLY in Session 65; Session 6 is clean. The
#     old prefix-match awk would over-grab 65 and surface the WARN under session 6.
printf '## Session 6 (2026-01-01)\nClean session, no anti-patterns here.\n\n## Session 65 (2026-06-15)\nWe decided every clean run advances n regardless of region.\n' > "$TMP/pf-multi.md"
out=$(CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  CLOSE_AUDIT_FSCAN="$SCRIPT_DIR/../../toolkit/scripts/falsification-scan.sh" \
  CLOSE_AUDIT_PFLOG="$TMP/pf-multi.md" \
  bash "$CLOSE_AUDIT" --session 6 2>&1)
assert_rc "exact session match keeps the close clean" 0 $?
if [[ "$out" != *"increment-by-default"* ]]; then
  echo "  PASS: --session 6 scan does not bleed --session 65 content"; PASS=$((PASS + 1))
else
  echo "  FAIL: --session 6 scan bled session 65 (awk prefix-match regression)"; FAIL=$((FAIL + 1))
fi

# C17 (PR #141 F-E): the advisory's no-matching-section and missing-FSCAN branches are
#     non-gating too (advisory ABSENT != close failure).
out=$(CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  CLOSE_AUDIT_FSCAN="$SCRIPT_DIR/../../toolkit/scripts/falsification-scan.sh" \
  CLOSE_AUDIT_PFLOG="$TMP/pf-fixture.md" \
  bash "$CLOSE_AUDIT" --session 999 2>&1)
assert_rc "advisory with no matching session section does not gate" 0 $?
assert_contains "no-section path is surfaced" "no '## Session 999' PF section" "$out"
CLOSE_AUDIT_ROSTER_DIR="$TMP" CLOSE_AUDIT_ROSTER="alpha-audit.sh" \
  CLOSE_AUDIT_FLOORS="$TMP/floor-ok.sh" \
  CLOSE_AUDIT_FSCAN="$TMP/nonexistent-fscan.sh" \
  CLOSE_AUDIT_PFLOG="$TMP/pf-fixture.md" \
  bash "$CLOSE_AUDIT" --session 64 >/dev/null 2>&1
assert_rc "advisory with a missing FSCAN binary does not gate" 0 $?

echo ""
echo "test_close_audit: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
