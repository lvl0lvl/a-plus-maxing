#!/usr/bin/env bash
# tests/test-enforce-merge-readiness.sh — F-007 negative test for
# hooks/enforce-merge-readiness.sh (ADR-0007, the no-merge-without-CLEAN-review gate).
#
# F-007 obligation: a guard that cannot prove it goes RED on bad input enforces
# nothing. This pins every acceptance criterion as a good/bad pair and proves the
# guard goes RED when its deny logic is removed.
#
# The hook DENIES `gh pr merge` (exit 2 in test mode) unless
#   ${CLAUDE_PROJECT_DIR}/.rigor/review-verdict.json exists, reads result CLEAN,
#   and its head_sha equals the current commit (ENFORCE_MERGE_HEAD_SHA override in
#   tests). result FINDINGS / absent / unreadable / sha-mismatch → DENY.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

HOOK="$TEST_DIR/../hooks/enforce-merge-readiness.sh"

PDIR="$(mktemp -d)"
trap 'rm -rf "$PDIR"' EXIT
mkdir -p "$PDIR/.rigor"
VERDICT="$PDIR/.rigor/review-verdict.json"

SHA="1111111111111111111111111111111111111111"   # the reviewed/current HEAD
OTHER="2222222222222222222222222222222222222222" # a commit that landed after review

write_verdict() { # $1 = result ; $2 = head_sha
  printf '{"result":"%s","head_sha":"%s","ts":1000000000}\n' "$1" "$2" > "$VERDICT"
}
clear_verdict() { rm -f "$VERDICT"; }

run_hook() { # $1 = command ; $2 = current HEAD sha
  printf '{"tool_input":{"command":"%s"},"cwd":"%s"}\n' "$1" "$PDIR" \
    | ENFORCE_MERGE_READINESS_TESTMODE=1 \
      CLAUDE_PROJECT_DIR="$PDIR" \
      ENFORCE_MERGE_HEAD_SHA="$2" \
      bash "$HOOK"
}

MERGE="gh pr merge 42 --squash"

echo "== enforce-merge-readiness =="

# Core guard-fires proof (F-007): CLEAN+bound allows (0); same command with the
# verdict removed must DENY (!=0).
write_verdict CLEAN "$SHA"
assert_red_when_guard_removed \
  "printf '{\"tool_input\":{\"command\":\"$MERGE\"},\"cwd\":\"$PDIR\"}' | ENFORCE_MERGE_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR='$PDIR' ENFORCE_MERGE_HEAD_SHA='$SHA' bash '$HOOK'" \
  "rm -f '$VERDICT'; printf '{\"tool_input\":{\"command\":\"$MERGE\"},\"cwd\":\"$PDIR\"}' | ENFORCE_MERGE_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR='$PDIR' ENFORCE_MERGE_HEAD_SHA='$SHA' bash '$HOOK'"

# AC (a): CLEAN verdict bound to HEAD → ALLOW (0).
write_verdict CLEAN "$SHA"
expect_exit 0 run_hook "$MERGE" "$SHA"

# AC (b): verdict ABSENT → DENY (2), fail-closed (review never ran).
clear_verdict
expect_exit 2 run_hook "$MERGE" "$SHA"

# AC (b): result FINDINGS (review ran but not clean) → DENY (2).
write_verdict FINDINGS "$SHA"
expect_exit 2 run_hook "$MERGE" "$SHA"

# AC (b): CLEAN but head_sha != current HEAD (a commit landed after review) → DENY (2).
write_verdict CLEAN "$SHA"
expect_exit 2 run_hook "$MERGE" "$OTHER"

# AC (b): head_sha missing → DENY (2).
printf '{"result":"CLEAN","ts":1000000000}\n' > "$VERDICT"
expect_exit 2 run_hook "$MERGE" "$SHA"

# AC (b): garbage verdict → DENY (2), fail-closed.
printf 'not json at all' > "$VERDICT"
expect_exit 2 run_hook "$MERGE" "$SHA"

# AC (b): cannot establish HEAD (no override, PDIR not a git repo) → DENY (2).
write_verdict CLEAN "$SHA"
expect_exit 2 env CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_MERGE_READINESS_TESTMODE=1 \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr merge 42\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# AC (c): `gh pr view` must NOT be blocked even with no verdict → ALLOW (0).
clear_verdict
expect_exit 0 run_hook "gh pr view 42" "$SHA"

# AC (c): `gh project create` not our concern → ALLOW (0).
expect_exit 0 run_hook "gh project create --title X" "$SHA"

# Word-boundary / embedded text: `echo gh pr merge` must NOT be intercepted.
expect_exit 0 run_hook "echo gh pr merge 42" "$SHA"
# Word-boundary near-misses must NOT false-block (no verdict present → would DENY
# if wrongly matched): `gh pr merge-queue` (create ends on a word boundary) and
# `gh project merge` (lacks the pr-merge adjacency).
expect_exit 0 run_hook "gh pr merge-queue add" "$SHA"
expect_exit 0 run_hook "gh project merge 42" "$SHA"
# …but a real merge appended after the near-miss is still caught → DENY.
expect_exit 2 run_hook "gh pr merge-queue add && gh pr merge 42" "$SHA"

# 4jx: transparent-exec wrappers on the merge must still be intercepted → DENY
# when not ready (no verdict). Pre-strip these would ALLOW an un-reviewed merge.
clear_verdict
expect_exit 2 run_hook "command gh pr merge 42" "$SHA"
expect_exit 2 run_hook "env -u FOO gh pr merge 42" "$SHA"
expect_exit 2 run_hook "timeout 5 gh pr merge 42" "$SHA"

# (pif) case-folded wrapper: `TIMEOUT 5 gh pr merge` runs like lowercase on a
# case-insensitive FS and must be treated as a merge — DENY when unreviewed,
# ALLOW when CLEAN+bound (no over-deny of the folded form).
clear_verdict
expect_exit 2 run_hook "TIMEOUT 5 gh pr merge 42" "$SHA"
write_verdict CLEAN "$SHA"
expect_exit 0 run_hook "TIMEOUT 5 gh pr merge 42" "$SHA"
clear_verdict

# (pif) two-pass hazard parity (review SHOULD-FIX-1): setsid -c / env -C on the
# merge must still be intercepted (DENY when unreviewed). pass 1's -[uCg] class
# keeps setsid's arg-less -c from eating the target.
expect_exit 2 run_hook "setsid -c gh pr merge 42" "$SHA"
expect_exit 2 run_hook "env -C /tmp gh pr merge 42" "$SHA"

# (kfi) dep preflight: missing grep/sed/tr must FATAL (2) — previously PATH=''
# read the command as "not a merge" → silent ALLOW. Goes RED if removed.
expect_exit 2 env PATH='' ENFORCE_MERGE_READINESS_TESTMODE=1 /bin/bash "$HOOK" 'gh pr merge 42'

# The DENY path emits its reason to stderr (a promised diagnostic — F-007 on messages).
clear_verdict
assert_stderr_contains "enforce-merge-readiness" \
  env CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_MERGE_HEAD_SHA="$SHA" ENFORCE_MERGE_READINESS_TESTMODE=1 \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr merge 42\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# ═══ git-backed production path (git present only) ════════════════════════════
# No ENFORCE_MERGE_HEAD_SHA override — the binding is read from a real repo.
if command -v git >/dev/null 2>&1; then
  REPO="$PDIR/repo"; mkdir -p "$REPO/.rigor"
  git -C "$REPO" init -q
  git -C "$REPO" config user.email t@t; git -C "$REPO" config user.name t
  echo a > "$REPO/f"; git -C "$REPO" add f; git -C "$REPO" commit -qm c1
  REAL_SHA="$(git -C "$REPO" rev-parse HEAD)"
  RVERDICT="$REPO/.rigor/review-verdict.json"
  run_repo() {
    printf '{"tool_input":{"command":"gh pr merge 42 --squash"},"cwd":"%s"}\n' "$REPO" \
      | ENFORCE_MERGE_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR="$REPO" bash "$HOOK"
  }
  # CLEAN verdict bound to the real HEAD → ALLOW (0).
  printf '{"result":"CLEAN","head_sha":"%s","ts":1000000000}\n' "$REAL_SHA" > "$RVERDICT"
  expect_exit 0 run_repo
  # A new commit lands after the review → HEAD moves → DENY (2).
  echo b > "$REPO/f"; git -C "$REPO" commit -qam c2
  expect_exit 2 run_repo
  # Re-review re-stamps the new HEAD → ALLOW (0) again.
  printf '{"result":"CLEAN","head_sha":"%s","ts":1000000000}\n' "$(git -C "$REPO" rev-parse HEAD)" > "$RVERDICT"
  expect_exit 0 run_repo

  # Producer↔consumer seam: emit the verdict EXACTLY as commands/review-pr.md Phase 8
  # does (same printf shape + `git rev-parse HEAD`), so the test exercises the real
  # producer contract, not a hand-written fixture. CLEAN → ALLOW; then the Phase-8
  # FINDINGS branch → DENY.
  PROD_SHA="$(git -C "$REPO" rev-parse HEAD)"
  printf '{"result":"%s","head_sha":"%s","ts":%s}\n' "CLEAN" "$PROD_SHA" "1000000000" > "$RVERDICT"
  expect_exit 0 run_repo
  printf '{"result":"%s","head_sha":"%s","ts":%s}\n' "FINDINGS" "$PROD_SHA" "1000000000" > "$RVERDICT"
  expect_exit 2 run_repo

  # PRODUCTION-MODE override discipline (bug-hunt: the override must NOT be honored
  # outside TESTMODE, or a durable env var forges the binding). A stale CLEAN
  # verdict (bound to a bogus sha) + ENFORCE_MERGE_HEAD_SHA set to that bogus sha,
  # run in HOOK MODE (no TESTMODE) → the hook must DENY (emit a deny-object), not
  # read the override. Verify by stdout: hook-mode DENY prints a deny-object; ALLOW
  # prints nothing. TESTMODE-only tests cannot see this — it needs hook mode.
  printf '{"result":"CLEAN","head_sha":"deadbeefdeadbeefdeadbeefdeadbeefdeadbeef","ts":1000000000}\n' > "$RVERDICT"
  TESTS_RUN=$((TESTS_RUN + 1))
  PROD_OUT="$(printf '{"tool_input":{"command":"gh pr merge 42"},"cwd":"%s"}\n' "$REPO" \
    | ENFORCE_MERGE_HEAD_SHA="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef" CLAUDE_PROJECT_DIR="$REPO" \
      bash "$HOOK" 2>/dev/null)"
  if printf '%s' "$PROD_OUT" | grep -q '"permissionDecision":"deny"'; then
    echo "[PASS] production mode ignores ENFORCE_MERGE_HEAD_SHA (durable env cannot forge the binding)"
  else
    echo "[FAIL] production mode honored ENFORCE_MERGE_HEAD_SHA — env-forged binding ALLOWed a stale merge"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
else
  echo "[SKIP] git-backed production-path cases: git not present" >&2
fi

test_summary
