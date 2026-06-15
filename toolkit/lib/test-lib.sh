#!/usr/bin/env bash
# toolkit/lib/test-lib.sh — tiny negative-test harness for rigor audits.
#
# The F-007 obligation: an audit that cannot prove it FAILs on bad input does not
# count as enforcing anything — mechanical presence-checks systematically false-PASS
# (signal ≠ property). So every shipped audit MUST carry a negative test that shows
# it goes RED on a known-bad input (and ideally green on a known-good one).
#
# Dependency-free. Source this from a test file, then:
#   expect_exit <expected> <cmd...>          assert a command exits <expected>.
#   assert_red_when_guard_removed <good> <bad>
#       assert the audit PASSes (exit 0) on <good> and FAILs (exit !=0) on <bad>,
#       i.e. the guard actually fires when its property is violated.
#
# Both verbs print a [PASS]/[FAIL] line and bump TESTS_FAILED. End your test file
# with `test_summary` to print the tally and exit non-zero if anything failed.

TESTS_RUN=0
TESTS_FAILED=0

# expect_exit <expected_code> <cmd> [args...]
expect_exit() {
  expected="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  "$@" >/dev/null 2>&1
  actual=$?
  if [ "$actual" = "$expected" ]; then
    echo "[PASS] expect_exit $expected: $*"
  else
    echo "[FAIL] expect_exit $expected but got $actual: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# assert_red_when_guard_removed <good_cmd> <bad_cmd>
# good_cmd is the audit on input that satisfies the property (must exit 0).
# bad_cmd is the same audit on input that violates it / with the guard removed
# (must exit non-zero). Pass each as a single string; eval'd in a subshell.
assert_red_when_guard_removed() {
  good_cmd="$1"; bad_cmd="$2"
  TESTS_RUN=$((TESTS_RUN + 1))
  ( eval "$good_cmd" ) >/dev/null 2>&1; good_rc=$?
  ( eval "$bad_cmd" )  >/dev/null 2>&1; bad_rc=$?
  if [ "$good_rc" = "0" ] && [ "$bad_rc" != "0" ]; then
    echo "[PASS] guard fires: good=0 bad=$bad_rc"
  else
    echo "[FAIL] guard did not prove it FAILs (good=$good_rc want 0; bad=$bad_rc want !=0)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# assert_stderr_contains <ere_pattern> <cmd> [args...]
# Assert the command's STDERR matches <ere_pattern>. A diagnostic the tool PROMISES
# to emit is a shipped behavior; if it is unasserted, deleting it is a silent
# regression (the F-007 lesson applied to messages, not just exit codes).
assert_stderr_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  err="$("$@" 2>&1 >/dev/null)"
  if printf '%s' "$err" | grep -qE "$pattern"; then
    echo "[PASS] stderr matches /$pattern/: $*"
  else
    echo "[FAIL] stderr lacked /$pattern/: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

test_summary() {
  echo "---"
  echo "tests: ${TESTS_RUN} run, ${TESTS_FAILED} failed"
  [ "$TESTS_FAILED" -eq 0 ] || exit 1
  exit 0
}
