#!/usr/bin/env bash
# test-role-completeness-audit.sh — proves role-completeness-audit.sh goes RED on
# a role profile missing a canonical section (F-007 negative-test obligation: an
# audit that cannot demonstrate it FAILs on bad input does not count as enforcing).
set -uo pipefail
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"
AUDIT="$TEST_DIR/../scripts/role-completeness-audit.sh"

# A complete 11-section profile (10 fixed + the Modes operational slot).
SECS='## Identity
## Core Rules
## Role Boundaries
## Ask vs Proceed
## Loop-Breaking
## Tools
## Communication
## Context Loading
## Anti-Patterns
## Negative Examples
## Modes'

GOOD="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$GOOD/roles/complete"
printf '%s\n' "$SECS" > "$GOOD/roles/complete/agent.md"

BAD="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$BAD/roles/complete" "$BAD/roles/broken"
printf '%s\n' "$SECS" > "$BAD/roles/complete/agent.md"
# broken: drop the operational slot — the EXACT game-designer/0c8 defect.
printf '%s\n' "$SECS" | grep -v '## Modes' > "$BAD/roles/broken/agent.md"

# Core contract: green when every profile is complete, RED when a broken one is present.
assert_red_when_guard_removed \
  "bash '$AUDIT' --lib '$GOOD'" \
  "bash '$AUDIT' --lib '$BAD'"

# Explicit exit-code assertions.
expect_exit 0 bash "$AUDIT" --lib "$GOOD"   # all complete -> PASS
expect_exit 1 bash "$AUDIT" --lib "$BAD"    # one missing a section -> FAIL

# The specific defect (the broken role) is named in the audit's stdout output.
out="$(bash "$AUDIT" --lib "$BAD" 2>&1 || true)"
TESTS_RUN=$((TESTS_RUN + 1))
if printf '%s' "$out" | grep -q "role 'broken' incomplete"; then
  echo "[PASS] audit names the incomplete role"
else
  echo "[FAIL] audit did not name the incomplete role"; TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Bad args / no roles -> FATAL (exit 2), never a silent pass.
expect_exit 2 bash "$AUDIT"
expect_exit 2 bash "$AUDIT" --lib /no/such/dir/anywhere
expect_exit 2 bash "$AUDIT" --bogus

rm -rf "$GOOD" "$BAD"
test_summary
