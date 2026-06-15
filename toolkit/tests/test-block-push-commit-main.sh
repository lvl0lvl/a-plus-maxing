#!/usr/bin/env bash
# tests/test-block-push-commit-main.sh — negative tests for hooks/block-push-main.sh
# and hooks/block-commit-main.sh (the two sides of INV-BRANCH-NOT-MAIN).
#
# F-007 obligation: a guard that cannot prove it goes RED on bad input enforces
# nothing. So for EACH hook this test asserts:
#   - GOOD input  → exit 0 (allow),
#   - BAD  input  → exit non-zero (block).
# It also pins the BUG-1 false-green named in the push hook header — `git push -u
# origin main` (flags between push and remote) — which the original `\S+`-remote
# regex missed, and the word-boundary case (`git push origin maintenance` must NOT
# block). Fixtures are JSON files under fixtures/block-push-commit-main/.
#
# The hooks are driven in TEST MODE (verdict carried in the exit code) so test-lib's
# expect_exit / assert_red_when_guard_removed can read the verdict directly.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

PUSH_HOOK="$TEST_DIR/../hooks/block-push-main.sh"
COMMIT_HOOK="$TEST_DIR/../hooks/block-commit-main.sh"
# Fixtures are generated scratch (not committed): write to a throwaway temp dir so
# running the suite never dirties the tracked tree (skill_consolidator-oas).
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# ── fixtures ──────────────────────────────────────────────────────────────────
# PreToolUse-shaped JSON. The command is what each hook extracts.
write_fixture() { # $1 = file ; $2 = command string (JSON-escaped already)
  printf '{"tool_input":{"command":"%s"},"cwd":"%s"}\n' "$2" "$TEST_DIR" > "$FIX/$1"
}

# --- push hook fixtures ---
write_fixture push-good.json  "git push origin feature/x"          # allow
write_fixture push-bad.json   "git push origin main"               # block
write_fixture push-bug1.json  "git push -u origin main"            # BUG-1: must block
write_fixture push-master.json "git push origin master"            # block (master)
write_fixture push-wordboundary.json "git push origin maintenance" # allow (not 'main')

# --- commit hook fixtures (branch forced via env so the test is repo-independent) ---
write_fixture commit-good.json "git commit -m hello"               # allow when branch ok
write_fixture commit-bad.json  "git commit -m hello"               # block when branch=main
write_fixture commit-embedded.json 'echo git commit'               # allow (embedded text, BUG-3)

# ── helpers that invoke the hooks in TEST MODE ────────────────────────────────
run_push()   { BLOCK_PUSH_MAIN_TESTMODE=1   bash "$PUSH_HOOK"   < "$FIX/$1"; }
# commit hook: $2 forces the branch the commit is judged against.
run_commit() { BLOCK_COMMIT_MAIN_TESTMODE=1 BLOCK_COMMIT_MAIN_FORCE_BRANCH="$2" bash "$COMMIT_HOOK" < "$FIX/$1"; }

echo "== block-push-main =="
# Core guard-fires proof: good allows (0), bad blocks (!=0).
assert_red_when_guard_removed \
  "BLOCK_PUSH_MAIN_TESTMODE=1 bash '$PUSH_HOOK' < '$FIX/push-good.json'" \
  "BLOCK_PUSH_MAIN_TESTMODE=1 bash '$PUSH_HOOK' < '$FIX/push-bad.json'"

expect_exit 0 run_push push-good.json          # feature branch push → allow
expect_exit 1 run_push push-bad.json           # push origin main → block
expect_exit 1 run_push push-bug1.json          # BUG-1 false-green: -u origin main → block
expect_exit 1 run_push push-master.json        # master → block
expect_exit 0 run_push push-wordboundary.json  # 'maintenance' must NOT false-match

# F-008 fail-closed: non-empty input with no extractable command → FATAL (2).
printf '{"tool_input":{}}' > "$FIX/push-noemcmd.json"
expect_exit 2 run_push push-noemcmd.json

echo "== block-commit-main =="
# Guard-fires proof: same command, allowed on a feature branch, blocked on main.
assert_red_when_guard_removed \
  "BLOCK_COMMIT_MAIN_TESTMODE=1 BLOCK_COMMIT_MAIN_FORCE_BRANCH=feature/x bash '$COMMIT_HOOK' < '$FIX/commit-good.json'" \
  "BLOCK_COMMIT_MAIN_TESTMODE=1 BLOCK_COMMIT_MAIN_FORCE_BRANCH=main      bash '$COMMIT_HOOK' < '$FIX/commit-bad.json'"

expect_exit 0 run_commit commit-good.json feature/x   # commit on feature branch → allow
expect_exit 1 run_commit commit-bad.json  main        # commit on main → block
expect_exit 1 run_commit commit-bad.json  master      # commit on master → block
expect_exit 0 run_commit commit-embedded.json main    # 'echo git commit' on main → allow (BUG-3)

# F-008 fail-closed: non-empty input with no extractable command → FATAL (2).
printf '{"tool_input":{}}' > "$FIX/commit-noemcmd.json"
expect_exit 2 run_commit commit-noemcmd.json main

test_summary
