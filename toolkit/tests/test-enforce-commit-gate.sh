#!/usr/bin/env bash
# tests/test-enforce-commit-gate.sh — negative test for hooks/enforce-commit-gate.sh
# (T1 / ADR-0001 — the commit-time fail-closed gate; giq.1.6/1.3 P0).
#
# F-007 obligation: a guard that cannot prove it goes RED on bad input enforces
# nothing. This test asserts T1's binary ACs against the hook in HOOK MODE — the
# verdict is carried in the EXIT CODE the PreToolUse contract already uses (exit 2
# = DENY, exit 0 = ALLOW), so test-lib's expect_exit / assert_red_when_guard_removed
# read it directly without a separate TESTMODE.
#
# Binary ACs proved here (rigor-guards-spec.md T1):
#   (a) RED gate ($RIGOR_COMMIT_GATE exits non-zero)        → exit 2 (DENY).
#   (b) GREEN gate ($RIGOR_COMMIT_GATE exits 0)             → exit 0 (ALLOW) AND
#       ${CLAUDE_PROJECT_DIR}/.rigor/commit-gate-verdict.json written, GREEN + ts.
#   (c) unconfigured ($RIGOR_COMMIT_GATE unset)             → exit 0 (ALLOW) with a
#       loud stderr SKIP line (never silent).
#   (d) matcher catches `git commit`, `git -C <path> commit`, `cd <path> && git
#       commit`; does NOT block `git config` / `git status`.
#   (e) a gate that cannot RUN (run-error, not just non-zero) → fail-closed DENY (2).
#   (f) assert_red_when_guard_removed: GREEN→0 / RED→!=0 — the test goes RED if the
#       deny logic is stripped (a stub that always exits 0 fails this pair).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

HOOK="$TEST_DIR/../hooks/enforce-commit-gate.sh"

# Throwaway project dir so the verdict artifact never dirties the tracked tree
# (skill_consolidator-oas) and CLAUDE_PROJECT_DIR is deterministic.
PROJ="$(mktemp -d)"
trap 'rm -rf "$PROJ"' EXIT
VERDICT="$PROJ/.rigor/commit-gate-verdict.json"

# ── fixtures ──────────────────────────────────────────────────────────────────
# PreToolUse-shaped JSON; the hook extracts .tool_input.command (matching
# block-commit-main.sh's input method).
FIX="$PROJ/fix"
mkdir -p "$FIX"
write_fixture() { # $1 = file ; $2 = command string (JSON-escaped already)
  printf '{"tool_input":{"command":"%s"},"cwd":"%s"}\n' "$2" "$TEST_DIR" > "$FIX/$1"
}

write_fixture commit.json        "git commit -m hello"
write_fixture commit-C.json      "git -C /some/path commit -m hello"
write_fixture commit-cd.json     "cd /some/path && git commit -m hello"
write_fixture config.json        "git config user.name bob"
write_fixture status.json        "git status"
# 4jx transparent-exec wrapper evasions — must be caught (stripped to git commit).
write_fixture commit-command.json "command git commit -m x"
write_fixture commit-env.json     "env git commit -m x"
write_fixture commit-nohup.json   "nohup git commit -m x"
write_fixture commit-exec.json    "exec git commit -m x"
write_fixture commit-time.json    "time git commit -m x"
write_fixture commit-builtin.json "builtin git commit -m x"
write_fixture commit-envflag.json "env -i FOO=b git commit -m x"
write_fixture commit-nested.json  "nohup env git commit -m x"
write_fixture commit-cdwrap.json  "cd /some/path && env git commit -m x"
# arg-taking wrappers (numeric/duration scalar + value-flag) — must be caught.
write_fixture commit-timeout.json "timeout 5 git commit -m x"
write_fixture commit-sudo.json    "sudo git commit -m x"
write_fixture commit-nice.json    "nice -n 10 git commit -m x"
write_fixture commit-envu.json    "env -u FOO git commit -m x"
write_fixture commit-envC.json    "env -C /tmp git commit -m x"
write_fixture commit-cdtimeout.json "cd /some/path && timeout 5 git commit -m x"
# echo is NOT transparent-exec — must NOT be stripped, must NOT match.
write_fixture echo-commit.json    "echo git commit"
# substring-safety: near-miss words must NOT be stripped → NOT a commit.
write_fixture commander.json      "commander git commit"
write_fixture environment.json    "environment git status"
write_fixture timeouty.json       "timeouty git commit"
# semantic: `sudo -u git commit` runs `commit` as user git → NOT git-commit.
write_fixture sudo-u-git.json     "sudo -u git commit"
# pif case-fold: on a case-insensitive FS these RUN like lowercase — must be caught.
write_fixture commit-caps.json     "GIT commit -m x"
write_fixture commit-capswrap.json "TIMEOUT 5 Git commit -m x"
write_fixture echo-caps.json       "ECHO git commit"
# pif two-pass hazard pin: setsid's lowercase -c takes NO argument, so pass 1's
# -[uCg] class must keep catching this (a single folded pass with -[ucg] would
# consume 'git' as -c's value → false ALLOW).
write_fixture setsid-c.json        "setsid -c git commit -m x"

# ── drivers ───────────────────────────────────────────────────────────────────
# GREEN: gate exits 0. RED: gate exits non-zero. ERR: gate command does not exist.
run_green() { CLAUDE_PROJECT_DIR="$PROJ" RIGOR_COMMIT_GATE="true"  bash "$HOOK" < "$FIX/$1"; }
run_red()   { CLAUDE_PROJECT_DIR="$PROJ" RIGOR_COMMIT_GATE="false" bash "$HOOK" < "$FIX/$1"; }
run_err()   { CLAUDE_PROJECT_DIR="$PROJ" RIGOR_COMMIT_GATE="this_command_does_not_exist_42" bash "$HOOK" < "$FIX/$1"; }
# unset: scrub $RIGOR_COMMIT_GATE from the child env regardless of any ambient value.
run_unset() { env -u RIGOR_COMMIT_GATE CLAUDE_PROJECT_DIR="$PROJ" bash "$HOOK" < "$FIX/$1"; }

echo "== enforce-commit-gate =="

# (f) Core guard-fires proof: same git-commit command — GREEN allows (0), RED
# denies (!=0). A stub that always exits 0 makes bad_rc=0 → this goes RED.
assert_red_when_guard_removed \
  "CLAUDE_PROJECT_DIR='$PROJ' RIGOR_COMMIT_GATE=true  bash '$HOOK' < '$FIX/commit.json'" \
  "CLAUDE_PROJECT_DIR='$PROJ' RIGOR_COMMIT_GATE=false bash '$HOOK' < '$FIX/commit.json'"

# (a) RED gate on a git commit → DENY (exit 2).
expect_exit 2 run_red commit.json

# (b) GREEN gate on a git commit → ALLOW (exit 0) + verdict file written GREEN+ts
# + certified_parent (the ADR-0006 SHA binding — present as a quoted string even
# when $PROJ is not a repo, where it is empty = "certified root").
rm -f "$VERDICT"
expect_exit 0 run_green commit.json
TESTS_RUN=$((TESTS_RUN + 1))
if [ -f "$VERDICT" ] && grep -q 'GREEN' "$VERDICT" \
     && grep -Eq '"ts"[[:space:]]*:[[:space:]]*[0-9]+' "$VERDICT" \
     && grep -Eq '"certified_parent"[[:space:]]*:[[:space:]]*"' "$VERDICT"; then
  echo "[PASS] verdict written GREEN+ts+certified_parent: $VERDICT"
else
  echo "[FAIL] verdict file missing or lacks GREEN+ts+certified_parent: $VERDICT"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# A RED gate must NOT write a GREEN verdict (no false-green artifact).
rm -f "$VERDICT"
run_red commit.json >/dev/null 2>&1 || true
TESTS_RUN=$((TESTS_RUN + 1))
if [ -f "$VERDICT" ] && grep -q 'GREEN' "$VERDICT"; then
  echo "[FAIL] RED gate wrote a GREEN verdict (false-green, F-008): $VERDICT"
  TESTS_FAILED=$((TESTS_FAILED + 1))
else
  echo "[PASS] RED gate wrote no GREEN verdict"
fi

# (c) Unconfigured (no $RIGOR_COMMIT_GATE) → ALLOW (exit 0) with a loud stderr SKIP.
expect_exit 0 run_unset commit.json
assert_stderr_contains 'SKIP' run_unset commit.json

# (e) Gate that cannot RUN (run-error, not just non-zero) → fail-closed DENY (2).
expect_exit 2 run_err commit.json

# (d) Matcher coverage: git -C and cd && git commit are caught (RED → DENY 2);
# git config / git status are NOT our concern (GREEN gate, but also must ALLOW —
# and crucially a RED gate must NOT block a non-commit command).
expect_exit 2 run_red commit-C.json    # git -C <path> commit → matched → DENY
expect_exit 2 run_red commit-cd.json   # cd <path> && git commit → matched → DENY
expect_exit 0 run_red config.json      # git config → NOT a commit → ALLOW even on RED gate
expect_exit 0 run_red status.json      # git status → NOT a commit → ALLOW even on RED gate

# (4jx) Transparent-exec wrapper evasions over a RED gate → DENY (2). Without the
# strip pre-pass each of these ALLOWs an un-gated commit (the false-ALLOW the bead
# closes). The echo case must still ALLOW (not a commit — echo is not exec).
expect_exit 2 run_red commit-command.json  # command git commit → stripped → DENY
expect_exit 2 run_red commit-env.json      # env git commit → stripped → DENY
expect_exit 2 run_red commit-nohup.json    # nohup git commit → stripped → DENY
expect_exit 2 run_red commit-exec.json     # exec git commit → stripped → DENY
expect_exit 2 run_red commit-time.json     # time git commit → stripped → DENY
expect_exit 2 run_red commit-builtin.json  # builtin git commit → stripped → DENY
expect_exit 2 run_red commit-envflag.json  # env -i FOO=b git commit → stripped → DENY
expect_exit 2 run_red commit-nested.json   # nohup env git commit → stripped → DENY
expect_exit 2 run_red commit-cdwrap.json   # cd && env git commit → stripped → DENY
expect_exit 2 run_red commit-timeout.json  # timeout 5 git commit → scalar consumed → DENY
expect_exit 2 run_red commit-sudo.json     # sudo git commit → stripped → DENY
expect_exit 2 run_red commit-nice.json     # nice -n 10 git commit → flag+scalar → DENY
expect_exit 2 run_red commit-envu.json     # env -u FOO git commit → value-flag → DENY
expect_exit 2 run_red commit-envC.json     # env -C /tmp git commit → value-flag → DENY
expect_exit 2 run_red commit-cdtimeout.json # cd && timeout 5 git commit → DENY
expect_exit 0 run_red echo-commit.json     # echo git commit → NOT stripped → ALLOW
expect_exit 0 run_red commander.json       # 'commander' → substring-safe → ALLOW
expect_exit 0 run_red environment.json     # 'environment git status' → ALLOW
expect_exit 0 run_red timeouty.json        # 'timeouty' → substring-safe → ALLOW
expect_exit 0 run_red sudo-u-git.json      # sudo -u git commit → runs 'commit' → ALLOW

# (pif) case-fold: GIT / TIMEOUT 5 Git run like lowercase on a case-insensitive FS
# and previously matched nothing → un-gated commit over a RED roster. ECHO must
# stay non-exec (folding must not widen the must-NOT-block set).
expect_exit 2 run_red commit-caps.json     # GIT commit → folds → DENY
expect_exit 2 run_red commit-capswrap.json # TIMEOUT 5 Git commit → folds+strips → DENY
expect_exit 0 run_red echo-caps.json       # ECHO git commit → folds to echo → ALLOW
expect_exit 2 run_red setsid-c.json        # setsid -c git commit → pass 1 catches → DENY

# (kfi) dep preflight: missing grep/sed/tr must DENY (2) — previously PATH=''
# made the matcher read "not a commit" → silent ALLOW even over a RED roster.
# Goes RED if the preflight is removed (PATH='' would again exit 0).
expect_exit 2 env PATH='' CLAUDE_PROJECT_DIR="$PROJ" RIGOR_COMMIT_GATE=false /bin/bash "$HOOK" 'git commit -m x'

# ═══ certified_parent binding (ADR-0006; git present only) ════════════════════
# The verdict must record the SHA the certified commit will be built on: HEAD at
# gate time for a plain commit, HEAD's raw parent set for --amend, empty for an
# unborn branch. This is what enforce-pr-readiness.sh checks HEAD identity against.
if command -v git >/dev/null 2>&1; then
  REPO="$PROJ/repo"
  mkdir -p "$REPO"
  git -C "$REPO" init -q
  git -C "$REPO" config user.email t@t; git -C "$REPO" config user.name t
  echo one > "$REPO/f"; git -C "$REPO" add f; git -C "$REPO" commit -qm c1
  echo two > "$REPO/f"; git -C "$REPO" commit -qam c2
  HEAD_SHA="$(git -C "$REPO" rev-parse HEAD)"
  PARENT_SHA="$(git -C "$REPO" rev-parse HEAD^)"
  RVERDICT="$REPO/.rigor/commit-gate-verdict.json"

  run_repo() { # $1 = command string (JSON-escaped already)
    printf '{"tool_input":{"command":"%s"},"cwd":"%s"}\n' "$1" "$REPO" \
      | CLAUDE_PROJECT_DIR="$REPO" RIGOR_COMMIT_GATE="true" bash "$HOOK"
  }
  check_cert() { # $1 = expected certified_parent ; $2 = label
    TESTS_RUN=$((TESTS_RUN + 1))
    if grep -q "\"certified_parent\":\"$1\"" "$RVERDICT" 2>/dev/null; then
      echo "[PASS] certified_parent $2"
    else
      echo "[FAIL] certified_parent $2 — wanted '$1', verdict: $(cat "$RVERDICT" 2>/dev/null)"
      TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
  }

  # Plain commit → certified_parent = HEAD at gate time.
  rm -f "$RVERDICT"
  expect_exit 0 run_repo "git commit -m next"
  check_cert "$HEAD_SHA" "= gate-time HEAD (plain commit)"

  # --amend → certified_parent = HEAD's parent (the amend REPLACES HEAD).
  rm -f "$RVERDICT"
  expect_exit 0 run_repo "git commit --amend --no-edit"
  check_cert "$PARENT_SHA" "= HEAD's parent (--amend)"

  # Parent-header parse discipline (triage C10): a commit MESSAGE line starting
  # "parent <sha>" must NOT be read as a header by raw_head_parents — the /^$/q
  # first-blank-line stop. Without the stop, the decoy token joins the recorded
  # parent set and this check goes RED.
  echo three > "$REPO/f"; git -C "$REPO" add f
  git -C "$REPO" commit -qm decoy -m "parent dddddddddddddddddddddddddddddddddddddddd"
  TRUE_P2="$(git -C "$REPO" rev-parse HEAD^)"
  rm -f "$RVERDICT"
  expect_exit 0 run_repo "git commit --amend --no-edit"
  check_cert "$TRUE_P2" "= true parent only (decoy 'parent ' message line ignored, --amend)"

  # (8ul) --amend token inside a QUOTED message must NOT flip the base: this is a
  # PLAIN commit → certified_parent = gate-time HEAD (previously HEAD's parents →
  # reader false-DENY on the happy path, executed triage C4).
  HEAD_NOW="$(git -C "$REPO" rev-parse HEAD)"
  rm -f "$RVERDICT"
  expect_exit 0 run_repo "git commit -m \\\"do not --amend this\\\""
  check_cert "$HEAD_NOW" "= gate-time HEAD (--amend only inside the quoted message)"

  # (8ul) the reverse direction: a REAL --amend outside quotes still flips the
  # base even with a quoted message present (the strip removes the message text,
  # not the flag).
  rm -f "$RVERDICT"
  expect_exit 0 run_repo "git commit --amend -m \\\"nothing about it\\\""
  check_cert "$(git -C "$REPO" rev-parse HEAD^)" "= HEAD's parent (real --amend + quoted message)"

  # Unborn branch (fresh init, no commits) → certified_parent = "" (root-to-be).
  FRESH="$PROJ/fresh"
  mkdir -p "$FRESH"; git -C "$FRESH" init -q
  printf '{"tool_input":{"command":"git commit -m first"},"cwd":"%s"}\n' "$FRESH" \
    | CLAUDE_PROJECT_DIR="$FRESH" RIGOR_COMMIT_GATE="true" bash "$HOOK" >/dev/null 2>&1
  RVERDICT="$FRESH/.rigor/commit-gate-verdict.json"
  check_cert "" "= empty (unborn branch → root commit)"
else
  echo "[SKIP] certified_parent binding cases: git not present" >&2
fi

test_summary
