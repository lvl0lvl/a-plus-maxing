#!/usr/bin/env bash
# tests/test-block-dangerous.sh — negative test for hooks/block-dangerous.sh (F-007).
#
# Proves the guard goes RED on known-BAD commands and GREEN on known-GOOD ones. A hook
# that cannot demonstrate it DENIES a destructive command is not enforcing anything; a
# mechanical presence-check that never fires is a false-green (signal != property).
#
# Specifically pins the BUG-F003 cases: BSD-grep portability of the `rm -rf /` pattern
# (and -fr / -r -f ordering), and the --force-with-lease carve-out that MUST stay ALLOWed.

here="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
. "$here/../lib/test-lib.sh"

HOOK="$here/../hooks/block-dangerous.sh"
FIX="$here/fixtures/block-dangerous"

# --- 1. --check mode: every GOOD line must ALLOW (exit 0). -------------------
while IFS= read -r line; do
  [ -z "$line" ] && continue
  expect_exit 0 bash "$HOOK" --check "$line"
done < "$FIX/good.txt"

# --- 2. --check mode: every BAD line must DENY (exit 1). ---------------------
while IFS= read -r line; do
  [ -z "$line" ] && continue
  expect_exit 1 bash "$HOOK" --check "$line"
done < "$FIX/bad.txt"

# --- 3. Guard-fires assertion: pair a good cmd against a bad cmd. ------------
assert_red_when_guard_removed \
  "bash '$HOOK' --check 'rm -rf ./build'" \
  "bash '$HOOK' --check 'rm -rf /'"

# --- 4. The exact BUG-F003 false-green: 'rm -fr /' must DENY (order swap,
#        and must work under BSD grep with no \b). ---------------------------
expect_exit 1 bash "$HOOK" --check 'rm -fr /'
expect_exit 1 bash "$HOOK" --check 'rm -r -f /'

# --- 5. The --force-with-lease carve-out: safe force MUST stay ALLOWed. ------
expect_exit 0 bash "$HOOK" --check 'git push --force-with-lease origin main'
expect_exit 1 bash "$HOOK" --check 'git push --force origin main'

# --- 6. Hook (JSON stdin) mode end-to-end: bad command -> deny decision. -----
if command -v jq >/dev/null 2>&1; then
  out=$(printf '{"tool_input":{"command":"rm -rf /"}}' | bash "$HOOK")
  TESTS_RUN=$((TESTS_RUN + 1))
  if printf '%s' "$out" | grep -q '"permissionDecision":"deny"'; then
    echo "[PASS] hook-mode deny JSON emitted for 'rm -rf /'"
  else
    echo "[FAIL] hook-mode did not emit deny JSON: $out"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi

  out=$(printf '{"tool_input":{"command":"rm -rf ./build"}}' | bash "$HOOK")
  TESTS_RUN=$((TESTS_RUN + 1))
  if [ -z "$out" ]; then
    echo "[PASS] hook-mode emitted no deny for safe 'rm -rf ./build'"
  else
    echo "[FAIL] hook-mode wrongly emitted for safe command: $out"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
else
  echo "[SKIP] jq absent; hook-mode JSON checks skipped (--check mode still covered)"
fi

test_summary
