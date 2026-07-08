#!/usr/bin/env bash
# test_run_all_tests.sh — negative test for scripts/tests/run-all-tests.sh (F-007 / PR #139 F9).
#
# Proves the aggregator's own logic goes RED on bad input: a failing fixture test
# fails the run, a stale exclusion (an excluded name that does not exist) fails the
# run, and a valid exclusion of an existing test passes + is printed loudly. Uses
# RUN_ALL_TESTS_DIR to point the runner at a fixture dir, so this test does NOT
# recurse into the live suite (which would re-invoke this file).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/run-all-tests.sh"

PASS=0
FAIL=0
assert_rc() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then echo "  PASS: $label (exit $actual)"; PASS=$((PASS + 1));
  else echo "  FAIL: $label (expected $expected, got $actual)"; FAIL=$((FAIL + 1)); fi
}
assert_contains() {
  local label="$1" needle="$2" hay="$3"
  if [[ "$hay" == *"$needle"* ]]; then echo "  PASS: $label"; PASS=$((PASS + 1));
  else echo "  FAIL: $label (missing: $needle)"; FAIL=$((FAIL + 1)); fi
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/test_alpha.sh"
printf '#!/usr/bin/env bash\nexit 1\n' > "$TMP/test_beta.sh"
chmod +x "$TMP"/*.sh

# A: a failing fixture test fails the run (exit 1)
RUN_ALL_TESTS_DIR="$TMP" bash "$RUNNER" >/dev/null 2>&1
assert_rc "a failing test fails the run" 1 $?

# B: excluding the failing test (valid exclusion) passes + prints EXCLUDED
out=$(RUN_ALL_TESTS_DIR="$TMP" RUN_ALL_TESTS_EXCLUDE="test_beta.sh" \
      RUN_ALL_TESTS_EXCLUDE_REASON="fixture: deliberately failing" bash "$RUNNER" 2>&1)
rc=$?
assert_rc "valid exclusion of the failing test passes" 0 $rc
assert_contains "exclusion is printed loudly" "EXCLUDED  test_beta.sh" "$out"

# C: a stale exclusion (name does not exist) fails the run (exit 1)
out=$(RUN_ALL_TESTS_DIR="$TMP" RUN_ALL_TESTS_EXCLUDE="test_nonexistent.sh" bash "$RUNNER" 2>&1)
rc=$?
assert_rc "a stale exclusion fails the run" 1 $rc
assert_contains "stale exclusion is named" "stale exclusion" "$out"

# D: a foreign-namespace exclusion (a toolkit test-*.sh name) is a no-op, not a
# stale RED — this floor only stale-guards its own test_*.sh namespace, so a shared
# CLOSE_AUDIT_FLOOR_EXCLUDE forwarded to both floors cannot cross-fire (bead 23q5).
CLEAN="$(mktemp -d)"
printf '#!/usr/bin/env bash\nexit 0\n' > "$CLEAN/test_alpha.sh"; chmod +x "$CLEAN/test_alpha.sh"
RUN_ALL_TESTS_DIR="$CLEAN" RUN_ALL_TESTS_EXCLUDE="test-roster-select.sh" bash "$RUNNER" >/dev/null 2>&1
rc=$?
rm -rf "$CLEAN"
assert_rc "a foreign-namespace exclusion is a no-op, not a stale RED" 0 $rc

echo ""
echo "test_run_all_tests: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
