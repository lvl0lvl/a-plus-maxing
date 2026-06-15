#!/usr/bin/env bash
# test-stale-hash-audit.sh — negative test for stale-hash-audit.sh.
#
# F-007 obligation (test-lib.sh): an audit that cannot prove it goes RED on bad
# input does not count as enforcing anything. This test proves stale-hash-audit.sh:
#   1. PASSes (exit 0) on a known-GOOD file (date-adjacent SHAs, labeled hashes,
#      fenced/indented code hashes, pure-decimal numbers — all correctly allowed).
#   2. FAILs (exit 1) on a known-BAD file containing the EXACT F-007 false-green:
#      a bare hash `deadbeef0` in narrative prose that a naive `\b`-based BSD-ERE
#      check would MISS. This version must CATCH it.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/stale-hash-audit.sh"
FIX="$TEST_DIR/fixtures/stale-hash-audit"
GOOD="$FIX/good.md"
BAD="$FIX/bad.md"

# Core contract: green on good, red on bad (the guard actually fires).
assert_red_when_guard_removed \
  "bash '$AUDIT' '$GOOD'" \
  "bash '$AUDIT' '$BAD'"

# Explicit exit-code assertions for clarity.
expect_exit 0 bash "$AUDIT" "$GOOD"
expect_exit 1 bash "$AUDIT" "$BAD"

# F-007 regression: confirm the SPECIFIC bare-hash token is the thing caught,
# i.e. this is genuinely the false-green case and not an incidental failure.
TESTS_RUN=$((TESTS_RUN + 1))
out="$(bash "$AUDIT" "$BAD" 2>&1 || true)"
if printf '%s' "$out" | grep -q 'deadbeef0'; then
  echo "[PASS] F-007 false-green caught: bare hash 'deadbeef0' flagged"
else
  echo "[FAIL] F-007 false-green NOT caught — expected 'deadbeef0' in output:"
  printf '%s\n' "$out"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Missing target -> FATAL (exit 2), per audit-helpers exit semantics.
expect_exit 2 bash "$AUDIT" "$FIX/does-not-exist.md"

# stdin mode works (TARGET '-').
TESTS_RUN=$((TESTS_RUN + 1))
printf 'we reverted to deadbeef0 with no date\n' | bash "$AUDIT" - >/dev/null 2>&1
if [ "$?" = "1" ]; then
  echo "[PASS] stdin mode catches bare hash"
else
  echo "[FAIL] stdin mode did not catch bare hash"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

test_summary
