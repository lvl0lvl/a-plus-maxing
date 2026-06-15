#!/usr/bin/env bash
# run-all-tests.sh — aggregate every scripts/tests/test_*.sh negative test.
#
# The a-plus twin of toolkit/tests/run-all-tests.sh. Per Rigor Framework
# Discipline 5 (F-007, the negative-test obligation): a mechanical audit only
# counts as enforcing once it has PROVEN it goes RED on bad input. This runner
# executes every project negative test and exits non-zero if any fails to prove
# it can fail. scripts/close-audit.sh runs this FIRST, before the audits
# themselves, so an audit that lost its ability to FAIL is caught before it can
# grant a false pass.
#
# Exclusions (NEVER silent — F-009 "no silent caps"): a documented, tracked
# pre-existing failure may be excluded via:
#   RUN_ALL_TESTS_EXCLUDE         space-separated test basenames to skip
#   RUN_ALL_TESTS_EXCLUDE_REASON  reason string printed for each exclusion
# Each excluded test that exists is printed as a loud EXCLUDED line so the drop
# is visible, never hidden. An excluded name that does NOT exist is itself an
# error (stale exclusion) and fails the run.
#
# Exit: 0 all non-excluded tests passed / 1 one or more failed (or a stale
#       exclusion names a missing test).

set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXCLUDE=" ${RUN_ALL_TESTS_EXCLUDE:-} "
EXCLUDE_REASON="${RUN_ALL_TESTS_EXCLUDE_REASON:-no reason given}"

is_excluded() { case "$EXCLUDE" in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

passed=0
failed=0
excluded=0
failed_names=()

# Verify every excluded name actually exists (a stale exclusion is a silent cap).
for ex in ${RUN_ALL_TESTS_EXCLUDE:-}; do
  if [ ! -e "$SELF_DIR/$ex" ]; then
    echo "[run-all] ERROR: excluded test does not exist: $ex (stale exclusion)"
    failed=$((failed + 1))
    failed_names+=("stale-exclusion:$ex")
  fi
done

for t in "$SELF_DIR"/test_*.sh; do
  [ -e "$t" ] || continue
  b="$(basename "$t")"
  if is_excluded "$b"; then
    echo "[run-all] EXCLUDED  $b — ${EXCLUDE_REASON}"
    excluded=$((excluded + 1))
    continue
  fi
  if bash "$t" >/dev/null 2>&1; then
    echo "[run-all] PASS  $b"
    passed=$((passed + 1))
  else
    echo "[run-all] FAIL  $b"
    failed=$((failed + 1))
    failed_names+=("$b")
  fi
done

echo "[run-all] RESULT: ${passed} passed, ${failed} failed, ${excluded} excluded"
if [ "$failed" -ne 0 ]; then
  printf '[run-all] failed: %s\n' "${failed_names[*]}"
  exit 1
fi
exit 0
