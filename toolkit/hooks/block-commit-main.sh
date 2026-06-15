#!/usr/bin/env bash
# toolkit/hooks/block-commit-main.sh — PreToolUse Bash-tool guard: deny a direct
# `git commit` while the target repo's HEAD points at a protected trunk branch
# (main/master by default).
#
# ENFORCES (CDM): INV-BRANCH-NOT-MAIN, commit side. Companion hook
# hooks/block-push-main.sh enforces the push side of the same invariant.
# Source finding lineage:
#   - PF-S2-06 (a-plus-maxing): five S2 commits landed on main locally before the
#     gap was noticed; push was correctly blocked but commit was not. This hook
#     closes the commit gap.
#   - F-008 (rigor toolkit): "couldn't verify" != "verified clean." A broken
#     install / unreadable branch is reported LOUDLY; in TEST MODE it is FATAL
#     (exit 2), not a silent allow.
#
# SOURCE LINEAGE:
#   - a-plus-maxing/.claude/hooks/block-commit-main.sh (the deny-JSON contract,
#     the git-commit matcher, the target-repo-branch check, set -uo pipefail).
#   The a-plus original single-sourced its matcher and target-repo resolution into
#   lib/commit-matcher.sh + lib/resolve-target-repo.sh (shared with two PII/vault
#   hooks not in this toolkit). Here, with only the branch consumer present, the
#   matcher is inlined (BUG-3 note) and target-repo resolution is reduced to its
#   essential worktree-aware form (cwd from the hook input, script-path fallback).
#
# BUG-3 (carried forward, a-plus bead `cvr`/`mic`): the naive `grep 'git commit'`
#   over-matches embedded text (`echo "git commit"`) and `git commit-tree`, and
#   under-matches env-var-prefixed (`EDITOR=vim git commit`), path-prefixed
#   (`/usr/bin/git commit`) and trailing-separator (`git commit; …`) forms. The
#   hardened matcher below anchors at start / after a separator, tolerates env-var
#   and path prefixes, allows flags between git and commit, and ends on a space /
#   separator / EOL — so `commit-tree` and `echo … commit` are NOT matched.
#
# BUG-4 (carried forward, a-plus bead `29u4`): resolving the repo from the
#   script's own path made the branch check read the checkout the hook SHIPS in,
#   not the worktree RECEIVING the commit. Resolution here reads the hook input's
#   `cwd` (worktree-aware) and falls back to the script-path root only when cwd is
#   absent/unresolvable — never weaker than the pre-fix behavior.
#
# RESIDUAL (carried forward): an in-command `cd <elsewhere> && git commit` is
#   checked against the STARTING cwd's repo — block-push-main remains the
#   second-line defense for that shape (PF-S2-06). Detached HEAD passes through
#   (no branch name to match).
#
# PORTABILITY: pure bash 3.2 + POSIX grep/tr/sed + git; jq optional (dependency-
#   free fallback parser). No GNU-isms, no `grep -P`.
#
# ── MODES ────────────────────────────────────────────────────────────────────
# HOOK MODE (default): read PreToolUse JSON on stdin, print a Claude Code deny
#   object + `exit 0` to DENY, or `exit 0` with no output to ALLOW.
#
# TEST MODE (BLOCK_COMMIT_MAIN_TESTMODE=1): verdict in the EXIT CODE for test-lib
#   (0 = ALLOW, 1 = BLOCK). A command that cannot be extracted from non-empty
#   input is exit 2 (FATAL, fail-closed, F-008). The branch to test against may be
#   forced via BLOCK_COMMIT_MAIN_FORCE_BRANCH (so the test needn't depend on the
#   ambient repo's HEAD); otherwise the target repo's real HEAD is read. The
#   command may be supplied as $1 instead of JSON on stdin.

set -uo pipefail

PROTECTED_BRANCHES="${PROTECTED_BRANCHES:-main master}"
TESTMODE="${BLOCK_COMMIT_MAIN_TESTMODE:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Fallback root when the hook input carries no resolvable cwd. Env override seeds
# it for tests; the production default is the toolkit checkout two levels up.
FALLBACK_ROOT="${BLOCK_COMMIT_MAIN_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"

# ── command extraction (jq optional, dependency-free fallback) ─────────────────
extract_command() {
  local json="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r '.tool_input.command // empty' <<EOF 2>/dev/null
$json
EOF
    return 0
  fi
  # See block-push-main.sh: BSD basic-sed has no `\|`, so swap escaped quotes to a
  # sentinel, grab the [^"] run, then restore.
  printf '%s' "$json" \
    | tr '\n' ' ' \
    | sed 's/\\"/__ESCQ__/g' \
    | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | sed 's/__ESCQ__/"/g; s/\\\\/\\/g; s/\\n/ /g; s/\\t/ /g'
}

extract_cwd() {
  local json="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r '.cwd // empty' <<EOF 2>/dev/null
$json
EOF
    return 0
  fi
  printf '%s' "$json" \
    | tr '\n' ' ' \
    | sed 's/\\"/__ESCQ__/g' \
    | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | sed 's/__ESCQ__/"/g; s/\\\\/\\/g'
}

# ── git-commit matcher (BUG-3) ────────────────────────────────────────────────
# NORM maps newlines to ';' and squeezes/strips whitespace; the regex (a-plus
# `cvr`) anchors at start/after a separator, tolerates env-var + path prefixes and
# flags, and ends on space / separator / EOL.
COMMIT_MATCHER_RE='(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?git +([^|&;]*[[:space:]])?commit( |[;&|]|$)'

is_git_commit() {  # $1 = raw command; 0 if a git commit invocation, else 1
  local norm
  norm=$(printf '%s' "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
  norm="${norm#" "}"; norm="${norm%" "}"
  printf '%s' "$norm" | grep -qE "$COMMIT_MATCHER_RE"
}

# ── target-repo resolution (BUG-4) ────────────────────────────────────────────
resolve_target_repo() {  # $1 = hook stdin JSON ; $2 = fallback root
  local cwd top
  cwd=$(extract_cwd "$1")
  if [ -n "$cwd" ] && [ -d "$cwd" ]; then
    top=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
    if [ -n "$top" ]; then
      printf '%s' "$top"
      return 0
    fi
  fi
  printf '%s' "$2"
}

current_branch() {  # $1 = repo root; echoes branch or empty (detached/non-repo)
  git -C "$1" symbolic-ref --short HEAD 2>/dev/null || printf '%s' ""
}

is_protected_branch() {  # $1 = branch name
  local b
  for b in $PROTECTED_BRANCHES; do
    [ "$1" = "$b" ] && return 0
  done
  return 1
}

# ── main ──────────────────────────────────────────────────────────────────────
RAW=""
HOOK_INPUT=""
if [ "$#" -ge 1 ] && [ -n "${1:-}" ]; then
  COMMAND="$1"
  RAW="$1"
else
  HOOK_INPUT="$(cat)"
  COMMAND="$(extract_command "$HOOK_INPUT")"
  RAW="$HOOK_INPUT"
fi

# Empty command → not our concern (allow). In TEST MODE, a non-empty input we
# could not parse is FATAL (fail-closed, F-008).
if [ -z "$COMMAND" ]; then
  if [ "$TESTMODE" = "1" ] && [ -n "$RAW" ]; then
    echo "block-commit-main: could not extract a command from non-empty input (fail-closed, F-008)" >&2
    exit 2
  fi
  exit 0
fi

# Not a git commit → not our concern (allow).
is_git_commit "$COMMAND" || exit 0

# Determine the branch to judge against.
if [ -n "${BLOCK_COMMIT_MAIN_FORCE_BRANCH:-}" ]; then
  BRANCH="$BLOCK_COMMIT_MAIN_FORCE_BRANCH"
else
  PROJECT_ROOT="$(resolve_target_repo "$HOOK_INPUT" "$FALLBACK_ROOT")"
  BRANCH="$(current_branch "$PROJECT_ROOT")"
fi

if [ "$TESTMODE" = "1" ]; then
  if is_protected_branch "$BRANCH"; then
    echo "block-commit-main: BLOCK — commit on protected branch '$BRANCH'" >&2
    exit 1
  fi
  exit 0
fi

# HOOK MODE.
if is_protected_branch "$BRANCH"; then
  printf '%s\n' "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"INV-BRANCH-NOT-MAIN: commit on '${BRANCH}' blocked. PF-S2-06 recurrence guard. Switch to a feature/* or fix/* branch first: 'git checkout -b feature/<short-description>'. If this is an authorized hotfix, override via direct user instruction.\"}}"
  exit 0
fi

exit 0
