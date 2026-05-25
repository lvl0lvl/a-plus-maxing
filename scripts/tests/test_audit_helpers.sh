#!/usr/bin/env bash
# test_audit_helpers.sh — smoke tests for scripts/lib/audit-helpers.sh
#
# Each test runs the lib in a subshell so audit_exit doesn't kill the
# runner. Exit code + stderr content are asserted.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB="$SCRIPT_DIR/../lib/audit-helpers.sh"

PASS=0
FAIL=0

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "  PASS: $label"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $label"
        echo "    expected: $expected"
        echo "    actual:   $actual"
        FAIL=$((FAIL + 1))
    fi
}

assert_contains() {
    local label="$1" needle="$2" haystack="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "  PASS: $label"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $label (missing: $needle)"
        echo "    haystack: $haystack"
        FAIL=$((FAIL + 1))
    fi
}

# ── T1: clean audit (no violations) exits 0 ────────────────────────────
echo "T1: clean audit exits 0"
(
    source "$LIB"
    audit_init "t1"
    info "scanned everything"
    audit_summary
    audit_exit
) 2>/dev/null
assert_eq "exit code" "0" "$?"

# ── T2: violation increments counter and exits 1 ──────────────────────
echo "T2: single violation exits 1"
out=$(
    (
        source "$LIB"
        audit_init "t2"
        violation INV-FOO "thing is wrong"
        audit_summary
        audit_exit
    ) 2>&1
)
rc=$?
assert_eq "exit code" "1" "$rc"
assert_contains "violation line"  "t2: VIOLATION INV-FOO: thing is wrong" "$out"
assert_contains "summary count"   "t2: 1 violation(s)" "$out"

# ── T3: multiple violations all recorded ──────────────────────────────
echo "T3: three violations recorded"
out=$(
    (
        source "$LIB"
        audit_init "t3"
        violation INV-A "a problem"
        violation INV-B "b problem"
        violation INV-A "another a"
        audit_summary
        audit_exit
    ) 2>&1
)
rc=$?
assert_eq "exit code" "1" "$rc"
assert_contains "summary count" "t3: 3 violation(s)" "$out"

# ── T4: info does NOT count as violation ──────────────────────────────
echo "T4: info() is non-counting"
out=$(
    (
        source "$LIB"
        audit_init "t4"
        info "diagnostic 1"
        info "diagnostic 2"
        info "diagnostic 3"
        audit_summary
        audit_exit
    ) 2>&1
)
rc=$?
assert_eq "exit code" "0" "$rc"
assert_contains "summary count" "t4: 0 violation(s)" "$out"
assert_contains "info line"     "t4: info: diagnostic 1" "$out"

# ── T5: audit_init resets counter from prior session ──────────────────
echo "T5: audit_init resets state"
out=$(
    (
        source "$LIB"
        audit_init "first"
        violation INV-X "first violation"
        audit_init "second"
        audit_summary
        audit_exit
    ) 2>&1
)
rc=$?
assert_eq "exit code" "0" "$rc"
assert_contains "second audit summary" "second: 0 violation(s)" "$out"

# ── T6: violation without args fails defensively ──────────────────────
echo "T6: violation() with missing args returns non-zero"
(
    source "$LIB"
    audit_init "t6"
    violation 2>/dev/null
) 2>/dev/null
rc_zero_args=$?
[[ $rc_zero_args -ne 0 ]] && { echo "  PASS: zero-arg rejected"; PASS=$((PASS+1)); } || { echo "  FAIL: zero-arg accepted"; FAIL=$((FAIL+1)); }

(
    source "$LIB"
    audit_init "t6"
    violation INV-FOO 2>/dev/null
) 2>/dev/null
rc_one_arg=$?
[[ $rc_one_arg -ne 0 ]] && { echo "  PASS: one-arg rejected"; PASS=$((PASS+1)); } || { echo "  FAIL: one-arg accepted"; FAIL=$((FAIL+1)); }

# ── T7: audit_init without name fails ─────────────────────────────────
echo "T7: audit_init() with no args fails"
(
    source "$LIB"
    audit_init 2>/dev/null
) 2>/dev/null
rc=$?
[[ $rc -ne 0 ]] && { echo "  PASS: no-name rejected"; PASS=$((PASS+1)); } || { echo "  FAIL: no-name accepted"; FAIL=$((FAIL+1)); }

# ── T8: audit_count accessor returns current count ────────────────────
echo "T8: audit_count() reads counter"
out=$(
    (
        source "$LIB"
        audit_init "t8"
        violation INV-A "one"
        violation INV-B "two"
        audit_count
    ) 2>/dev/null
)
assert_eq "audit_count output" "2" "$out"

# ── T9: double-source guard ───────────────────────────────────────────
echo "T9: source twice does not error"
(
    source "$LIB"
    source "$LIB"
    audit_init "t9"
    audit_exit
) 2>/dev/null
assert_eq "exit code after double-source" "0" "$?"

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL)) tests"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
