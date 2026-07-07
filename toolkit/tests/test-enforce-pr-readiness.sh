#!/usr/bin/env bash
# tests/test-enforce-pr-readiness.sh — F-007 negative test for hooks/enforce-pr-readiness.sh
# (ADR-0002 no-premature-PR gate + ADR-0006 SHA-bound verdict).
#
# F-007 obligation: a guard that cannot prove it goes RED on bad input enforces
# nothing. This test pins every acceptance criterion as a good/bad pair and
# proves the guard goes RED when its deny logic is removed.
#
# The hook is a PreToolUse(Bash) deny-gate that intercepts `gh pr create` and
# DENIES (exit 2) unless BOTH:
#   (a) ${CLAUDE_PROJECT_DIR}/.rigor/commit-gate-verdict.json exists, reads GREEN,
#       and is BOUND to HEAD: its certified_parent equals HEAD's raw parent set
#       (identity, not wall-clock — ADR-0006), AND
#   (b) an authorization marker is present:
#       ${CLAUDE_PROJECT_DIR}/.rigor/pr-authorized  OR  $RIGOR_PR_AUTHORIZED=1.
# Absent / unreadable / non-GREEN / unbound / pre-ADR-0006 verdict → RED → DENY.
#
# The hook is driven in TEST MODE (verdict carried in the EXIT CODE so test-lib's
# expect_exit / assert_red_when_guard_removed can read it directly):
#   0 = ALLOW (ready),  2 = DENY (not ready / fail-closed).
# The binding reference is pinned deterministically via ENFORCE_PR_HEAD_PARENTS
# (HEAD's parent set; set-but-EMPTY = root commit) so the unit cases do not depend
# on the ambient repo. A git-backed section then exercises the REAL production
# path (writer hook → git commit → reader hook) including the three fail-opens the
# reverted time-comparison had: un-gated follow-up, merge HEAD, shallow clone.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

HOOK="$TEST_DIR/../hooks/enforce-pr-readiness.sh"
WRITER="$TEST_DIR/../hooks/enforce-commit-gate.sh"

# Throwaway project dir holding .rigor/ — never dirties the tracked tree.
PDIR="$(mktemp -d)"
trap 'rm -rf "$PDIR"' EXIT
mkdir -p "$PDIR/.rigor"
VERDICT="$PDIR/.rigor/commit-gate-verdict.json"
MARKER="$PDIR/.rigor/pr-authorized"

# Pinned SHAs for the repo-independent unit cases.
P0="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"   # certified parent (gate-time HEAD)
C1="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"   # an un-gated follow-up commit
P2="cccccccccccccccccccccccccccccccccccccccc"   # a second merge parent

# ── fixture helpers ───────────────────────────────────────────────────────────
write_verdict() { # $1 = roster_result ; $2 = certified_parent
  printf '{"roster_result":"%s","ts":1000000000,"certified_parent":"%s"}\n' "$1" "$2" > "$VERDICT"
}
write_legacy_verdict() { # pre-ADR-0006 shape: GREEN + ts, NO certified_parent
  printf '{"roster_result":"GREEN","ts":1000000000}\n' > "$VERDICT"
}
clear_verdict() { rm -f "$VERDICT"; }
set_marker()    { : > "$MARKER"; }
clear_marker()  { rm -f "$MARKER"; }

# Drive the hook in TEST MODE on a PreToolUse-shaped command.
run_hook() { # $1 = command ; $2 = HEAD parent set (may be empty = root)
  printf '{"tool_input":{"command":"%s"},"cwd":"%s"}\n' "$1" "$PDIR" \
    | ENFORCE_PR_READINESS_TESTMODE=1 \
      CLAUDE_PROJECT_DIR="$PDIR" \
      ENFORCE_PR_HEAD_PARENTS="$2" \
      bash "$HOOK"
}

PR_CREATE="gh pr create --fill"

echo "== enforce-pr-readiness =="

# Core guard-fires proof (F-007): READY (bound GREEN + marker) allows (0);
# the same command with the verdict removed must DENY (!=0).
write_verdict GREEN "$P0"; set_marker
assert_red_when_guard_removed \
  "printf '{\"tool_input\":{\"command\":\"$PR_CREATE\"},\"cwd\":\"$PDIR\"}' | ENFORCE_PR_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR='$PDIR' ENFORCE_PR_HEAD_PARENTS='$P0' RIGOR_PR_AUTHORIZED=1 bash '$HOOK'" \
  "rm -f '$VERDICT'; printf '{\"tool_input\":{\"command\":\"$PR_CREATE\"},\"cwd\":\"$PDIR\"}' | ENFORCE_PR_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR='$PDIR' ENFORCE_PR_HEAD_PARENTS='$P0' RIGOR_PR_AUTHORIZED=1 bash '$HOOK'"

# AC (a): verdict GREEN + bound (certified_parent == HEAD parents) + marker → ALLOW.
write_verdict GREEN "$P0"; set_marker
expect_exit 0 run_hook "$PR_CREATE" "$P0"

# AC (a) via env marker instead of file → ALLOW (0).
write_verdict GREEN "$P0"; clear_marker
expect_exit 0 env RIGOR_PR_AUTHORIZED=1 CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_PR_HEAD_PARENTS="$P0" ENFORCE_PR_READINESS_TESTMODE=1 \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr create --fill\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# Root-commit binding: certified_parent EMPTY == HEAD parents EMPTY → ALLOW (0).
write_verdict GREEN ""; set_marker
expect_exit 0 run_hook "$PR_CREATE" ""

# AC (b): verdict ABSENT → DENY (2), fail-closed.
clear_verdict; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0"

# AC (b): UNBOUND — an un-gated commit landed after the gate (HEAD's parent is the
# gated commit C1, not the certified parent P0) → DENY (2). THE F4 fail-open the
# reverted time-comparison allowed.
write_verdict GREEN "$P0"; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$C1"

# AC (b): MERGE HEAD — two parents where the verdict certified one → DENY (2).
write_verdict GREEN "$P0"; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0 $P2"

# AC (b): root-forgery — verdict certifies parent P0 but HEAD reads as root
# (the shallow-graft misread shape) → DENY (2).
write_verdict GREEN "$P0"; set_marker
expect_exit 2 run_hook "$PR_CREATE" ""

# AC (b): pre-ADR-0006 verdict (GREEN + ts, NO certified_parent) → DENY (2):
# an unbound GREEN proves nothing about WHICH commit it certified.
write_legacy_verdict; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0"

# (pif) case-folded wrapper: `TIMEOUT 5 gh pr create` runs like lowercase on a
# case-insensitive FS and must be treated as a PR create — DENY when not ready,
# ALLOW when ready (no over-deny of the folded form).
clear_verdict; set_marker
expect_exit 2 run_hook "TIMEOUT 5 gh pr create --fill" "$P0"
write_verdict GREEN "$P0"; set_marker
expect_exit 0 run_hook "TIMEOUT 5 gh pr create --fill" "$P0"

# (pif) two-pass hazard parity (review SHOULD-FIX-1): setsid -c must still be
# intercepted (setsid's arg-less -c must not eat the target under the folded pass).
clear_verdict; set_marker
expect_exit 2 run_hook "setsid -c gh pr create --fill" "$P0"

# (kfi) dep preflight: missing grep/sed/tr must FATAL (2) — previously PATH=''
# read the command as "not a pr create" → silent ALLOW. Goes RED if removed.
expect_exit 2 env PATH='' ENFORCE_PR_READINESS_TESTMODE=1 /bin/bash "$HOOK" 'gh pr create --fill'

# AC (b): pre-ADR-0006 verdict at a ROOT HEAD → DENY (2). This pins the presence
# guard ITSELF (triage C9): without it the absent field parses as "" and equals a
# root's empty parent set — the exact false-ALLOW the guard closes. The non-root
# legacy case above cannot catch a removed guard (equality already denies there).
write_legacy_verdict; set_marker
expect_exit 2 run_hook "$PR_CREATE" ""

# Override discipline (triage C1): outside TESTMODE the ENFORCE_PR_HEAD_PARENTS
# override is IGNORED — the production path always reads real git, so a durable
# env var cannot forge the binding. In this non-repo PDIR the hook must fail
# closed (DENY reason on stderr) even though the override matches the verdict.
write_verdict GREEN "$P0"; set_marker
assert_stderr_contains "cannot establish" \
  env CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_PR_HEAD_PARENTS="$P0" \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr create\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# AC (b): verdict reads NON-GREEN (RED) → DENY (2), even when bound.
write_verdict RED "$P0"; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0"

# AC (b): verdict present but UNREADABLE/garbage → DENY (2), fail-closed.
printf 'not json at all' > "$VERDICT"; set_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0"

# AC (b): no ENFORCE_PR_HEAD_PARENTS override and PDIR is NOT a git repo →
# parents unestablishable → DENY (2), fail-closed (no "assume bound" path).
write_verdict GREEN "$P0"; set_marker
expect_exit 2 env CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_PR_READINESS_TESTMODE=1 \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr create\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# AC (c): MARKER absent (no file, no env) → DENY (2), even with bound GREEN.
write_verdict GREEN "$P0"; clear_marker
expect_exit 2 run_hook "$PR_CREATE" "$P0"

# AC (d): `gh pr view` must NOT be blocked even when NOT ready → ALLOW (0).
clear_verdict; clear_marker
expect_exit 0 run_hook "gh pr view 42" "$P0"

# AC (d): `gh project create` must NOT be blocked when NOT ready → ALLOW (0).
clear_verdict; clear_marker
expect_exit 0 run_hook "gh project create --title X" "$P0"

# Word-boundary / embedded-text: `echo gh pr create` must NOT be intercepted.
clear_verdict; clear_marker
expect_exit 0 run_hook "echo gh pr create" "$P0"

# (4jx) Transparent-exec wrapper evasions: `command gh pr create` etc. MUST be
# intercepted → with NO verdict + NO marker (not ready) they DENY (2). Pre-strip
# these ALLOWed (0), bypassing the PR gate — the false-ALLOW the bead closes.
clear_verdict; clear_marker
expect_exit 2 run_hook "command gh pr create" "$P0"
expect_exit 2 run_hook "env gh pr create --fill" "$P0"
expect_exit 2 run_hook "exec gh pr create" "$P0"
expect_exit 2 run_hook "time gh pr create" "$P0"
expect_exit 2 run_hook "builtin gh pr create" "$P0"
expect_exit 2 run_hook "nohup gh pr create" "$P0"
expect_exit 2 run_hook "cd /x && env gh pr create" "$P0"
# arg-taking wrappers (scalar + value-flag) → intercepted → DENY.
expect_exit 2 run_hook "timeout 5 gh pr create" "$P0"
expect_exit 2 run_hook "sudo gh pr create" "$P0"
expect_exit 2 run_hook "nice -n 10 gh pr create" "$P0"
expect_exit 2 run_hook "env -u FOO gh pr create" "$P0"
expect_exit 2 run_hook "env -C /tmp gh pr create" "$P0"
# echo is not transparent-exec → still NOT intercepted → ALLOW (0).
expect_exit 0 run_hook "echo command gh pr create" "$P0"
# substring-safety: near-miss words → NOT intercepted → ALLOW (0).
expect_exit 0 run_hook "timeouty gh pr create" "$P0"
expect_exit 0 run_hook "environment gh pr create" "$P0"

# The DENY path emits its reason to stderr (a promised diagnostic — asserting it
# means deleting it is a caught regression, F-007 applied to messages).
clear_verdict; set_marker
assert_stderr_contains "enforce-pr-readiness" \
  env CLAUDE_PROJECT_DIR="$PDIR" ENFORCE_PR_HEAD_PARENTS="$P0" ENFORCE_PR_READINESS_TESTMODE=1 \
  bash -c 'printf "{\"tool_input\":{\"command\":\"gh pr create\"},\"cwd\":\"$CLAUDE_PROJECT_DIR\"}" | bash "$0"' "$HOOK"

# ═══ git-backed production-path section (git present only) ════════════════════
# Runs the REAL chain: writer hook (enforce-commit-gate, GREEN roster) → actual
# `git commit` → reader hook, with NO ENFORCE_PR_HEAD_PARENTS override — the
# binding is read from the real repo. Then proves each ADR-0006 target RED:
# un-gated follow-up, merge HEAD, shallow clone, plus the --amend happy path.
# ORDER-DEPENDENT: the cases below build one narrative history on $REPO (happy →
# un-gated → re-gate → merge → amend-of-merge); reordering or resetting between
# cases changes which git shape each case exercises.
if command -v git >/dev/null 2>&1; then
  REPO="$PDIR/repo"
  mkdir -p "$REPO"
  git -C "$REPO" init -q
  git -C "$REPO" config user.email t@t; git -C "$REPO" config user.name t
  echo one > "$REPO/f"; git -C "$REPO" add f; git -C "$REPO" commit -qm base

  run_reader() { # reader in TEST MODE against $1 = project dir (real git binding)
    printf '{"tool_input":{"command":"gh pr create"},"cwd":"%s"}\n' "$1" \
      | ENFORCE_PR_READINESS_TESTMODE=1 CLAUDE_PROJECT_DIR="$1" RIGOR_PR_AUTHORIZED=1 \
        bash "$HOOK"
  }
  gate_then_commit() { # $1 = repo ; $2 = commit msg ; writer sees the same command git runs
    printf '{"tool_input":{"command":"git commit -m %s"},"cwd":"%s"}\n' "$2" "$1" \
      | CLAUDE_PROJECT_DIR="$1" RIGOR_COMMIT_GATE="true" bash "$WRITER" >/dev/null 2>&1
    git -C "$1" commit -qm "$2"
  }

  # Happy path: gate → commit → PR reads BOUND → ALLOW (0).
  echo two > "$REPO/f"; git -C "$REPO" add f
  gate_then_commit "$REPO" gated
  expect_exit 0 run_reader "$REPO"

  # Un-gated follow-up commit (bypasses the writer) → UNBOUND → DENY (2).
  echo three > "$REPO/f"; git -C "$REPO" commit -qam ungated
  expect_exit 2 run_reader "$REPO"

  # Re-gate, then a MERGE lands (git merge is never gated) → DENY (2).
  echo four > "$REPO/f"; git -C "$REPO" add f
  gate_then_commit "$REPO" regated
  git -C "$REPO" checkout -qb side HEAD~1 2>/dev/null
  echo side > "$REPO/g"; git -C "$REPO" add g; git -C "$REPO" commit -qm sidework
  git -C "$REPO" checkout -q -; git -C "$REPO" merge -q --no-ff -m merged side >/dev/null 2>&1
  expect_exit 2 run_reader "$REPO"

  # --amend happy path — HEAD is the MERGE commit here, so this is the
  # amend-of-merge / TWO-PARENT binding case (triage C6: do not reorder or reset
  # before this block, or the two-parent coverage silently degrades). The verdict
  # assertion below pins the two-parent recording explicitly.
  MP1="$(git -C "$REPO" rev-parse HEAD^1)"; MP2="$(git -C "$REPO" rev-parse HEAD^2)"
  echo five > "$REPO/f"; git -C "$REPO" add f
  printf '{"tool_input":{"command":"git commit --amend --no-edit"},"cwd":"%s"}\n' "$REPO" \
    | CLAUDE_PROJECT_DIR="$REPO" RIGOR_COMMIT_GATE="true" bash "$WRITER" >/dev/null 2>&1
  TESTS_RUN=$((TESTS_RUN + 1))
  if grep -q "\"certified_parent\":\"$MP1 $MP2\"" "$REPO/.rigor/commit-gate-verdict.json" 2>/dev/null; then
    echo "[PASS] amend-of-merge verdict records BOTH merge parents"
  else
    echo "[FAIL] amend-of-merge verdict lacks the two-parent binding: $(cat "$REPO/.rigor/commit-gate-verdict.json" 2>/dev/null)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
  git -C "$REPO" commit -q --amend --no-edit
  expect_exit 0 run_reader "$REPO"

  # Parent-header parse discipline (triage C10): a commit MESSAGE line starting
  # "parent <sha>" must NOT be read as a header — the /^$/q first-blank-line stop.
  # A bound verdict on such a HEAD ALLOWs; without the stop the decoy token would
  # join the parent set → mismatch → this case goes RED.
  DECOY="$PDIR/decoy"
  mkdir -p "$DECOY"; git -C "$DECOY" init -q
  git -C "$DECOY" config user.email t@t; git -C "$DECOY" config user.name t
  echo a > "$DECOY/f"; git -C "$DECOY" add f; git -C "$DECOY" commit -qm base
  echo b > "$DECOY/f"; git -C "$DECOY" add f
  git -C "$DECOY" commit -qm decoy -m "parent dddddddddddddddddddddddddddddddddddddddd"
  TRUE_P="$(git -C "$DECOY" rev-parse HEAD^)"
  mkdir -p "$DECOY/.rigor"
  printf '{"roster_result":"GREEN","ts":1000000000,"certified_parent":"%s"}\n' "$TRUE_P" \
    > "$DECOY/.rigor/commit-gate-verdict.json"
  expect_exit 0 run_reader "$DECOY"

  # SHALLOW clone: rev-parse HEAD^ / log %P are graft-blinded there — the reader
  # must read TRUE parents from the raw object. A bound verdict ALLOWS (0)…
  SRC="$PDIR/shallow-src"
  mkdir -p "$SRC"; git -C "$SRC" init -q
  git -C "$SRC" config user.email t@t; git -C "$SRC" config user.name t
  echo a > "$SRC/f"; git -C "$SRC" add f; git -C "$SRC" commit -qm c1
  echo b > "$SRC/f"; git -C "$SRC" commit -qam c2
  SHALLOW="$PDIR/shallow"
  if git clone -q --depth 1 "file://$SRC" "$SHALLOW" 2>/dev/null; then
    TRUE_PARENT="$(git -C "$SRC" rev-parse HEAD^)"
    mkdir -p "$SHALLOW/.rigor"
    printf '{"roster_result":"GREEN","ts":1000000000,"certified_parent":"%s"}\n' "$TRUE_PARENT" \
      > "$SHALLOW/.rigor/commit-gate-verdict.json"
    expect_exit 0 run_reader "$SHALLOW"
    # …and a root-claiming verdict must DENY (2): the shallow HEAD is NOT a root.
    # (The reverted time-comparison read exactly this shape as fresh — fail-open.)
    printf '{"roster_result":"GREEN","ts":1000000000,"certified_parent":""}\n' \
      > "$SHALLOW/.rigor/commit-gate-verdict.json"
    expect_exit 2 run_reader "$SHALLOW"
  else
    echo "[SKIP] shallow-clone cases: git clone --depth 1 over file:// unavailable" >&2
  fi
else
  echo "[SKIP] git-backed production-path cases: git not present" >&2
fi

test_summary
