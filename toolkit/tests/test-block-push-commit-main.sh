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
# 4jx: transparent-exec wrappers must be stripped so a wrapped commit on main blocks.
write_fixture commit-wrap-command.json 'command git commit -m x'   # block on main
write_fixture commit-wrap-nested.json  'nohup env git commit -m x' # block on main
write_fixture commit-wrap-timeout.json 'timeout 5 git commit -m x' # block (scalar-arg wrapper)
write_fixture commit-wrap-envu.json    'env -u FOO git commit -m x' # block (value-flag)
write_fixture commit-wrap-substr.json  'commander git commit'      # allow (substring-safe)

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
expect_exit 1 run_commit commit-wrap-command.json main # 4jx: command git commit → block
expect_exit 1 run_commit commit-wrap-nested.json  main # 4jx: nohup env git commit → block
expect_exit 1 run_commit commit-wrap-timeout.json main # 4jx: timeout 5 git commit → block
expect_exit 1 run_commit commit-wrap-envu.json    main # 4jx: env -u FOO git commit → block
expect_exit 0 run_commit commit-wrap-substr.json  main # 'commander' substring-safe → allow

# F-008 fail-closed: non-empty input with no extractable command → FATAL (2).
printf '{"tool_input":{}}' > "$FIX/commit-noemcmd.json"
expect_exit 2 run_commit commit-noemcmd.json main

# (pif) case-fold: on a case-insensitive FS `GIT commit` / `TIMEOUT 5 Git commit`
# RUN exactly like their lowercase forms but previously matched nothing → un-gated
# commit on main (executed triage C3). Must block on main, still allow elsewhere.
write_fixture commit-caps.json     'GIT commit -m x'
write_fixture commit-capswrap.json 'TIMEOUT 5 Git commit -m x'
write_fixture echo-caps.json       'ECHO git commit'
expect_exit 1 run_commit commit-caps.json     main       # folds → git commit → block
expect_exit 1 run_commit commit-capswrap.json main       # folds → wrapper strips → block
expect_exit 0 run_commit commit-caps.json     feature/x  # branch still decides
expect_exit 0 run_commit echo-caps.json       main       # fold must not widen echo into exec

# (pif) two-pass hazard parity (review SHOULD-FIX-1): the strip logic is
# byte-identical to enforce-commit-gate, so the setsid/env-C hazards are pinned
# here too. setsid's lowercase -c takes NO argument — pass 1's -[uCg] class must
# keep catching it (a single folded -[ucg] pass would eat 'git' as -c's value).
write_fixture commit-setsid.json 'setsid -c git commit -m x'
write_fixture commit-envC.json   'env -C /tmp git commit -m x'
expect_exit 1 run_commit commit-setsid.json main   # setsid -c git commit → pass 1 catches → block
expect_exit 1 run_commit commit-envC.json   main   # env -C /tmp git commit → value-flag → block

# (kfi) dep preflight: with grep/sed/tr unavailable the old hooks read every
# command as "not our concern" → silent ALLOW (exit 0). Must now FATAL (2).
# Goes RED if the preflight is removed (PATH='' would again exit 0).
expect_exit 2 env PATH='' BLOCK_PUSH_MAIN_TESTMODE=1   /bin/bash "$PUSH_HOOK"   'git push origin main'
expect_exit 2 env PATH='' BLOCK_COMMIT_MAIN_TESTMODE=1 /bin/bash "$COMMIT_HOOK" 'git commit -m x'

test_summary
