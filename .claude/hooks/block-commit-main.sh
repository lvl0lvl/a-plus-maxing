#!/bin/bash
# block-commit-main.sh — PreToolUse hook for Bash tool.
#
# Implements INV-BRANCH-NOT-MAIN at commit time. Mirror of block-push-main.sh:
# that hook blocks `git push` to main/master; this hook blocks `git commit`
# while HEAD points at main/master, closing the gap exposed by PF-S2-06
# (five S2 commits landed on main locally before the gap was noticed; push
# was correctly blocked but commit was not).
#
# Decision: deny if (command is a git commit invocation) AND (current branch
# is main or master). Detached HEAD passes through (no branch name to match).
#
# Exit codes (Claude Code hook convention):
#   prints deny JSON + exits 0 → deny tool call
#   exits 0 with no output      → allow tool call

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Fallback root when the hook input carries no resolvable cwd (see resolve-target-repo
# below). The env override lets tests seed it. Never set in production.
FALLBACK_ROOT="${BLOCK_COMMIT_MAIN_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# git-commit detection is single-sourced (bead mic). Allow-on-error guard (block-push-main
# is the second-line defense), but a missing/corrupt lib is a broken install — warn LOUDLY
# rather than silently disable the commit-on-main guard (PR#80 SEC-2).
source "$SCRIPT_DIR/lib/commit-matcher.sh" 2>/dev/null
declare -F is_git_commit >/dev/null 2>&1 || {
    echo "block-commit-main: commit-matcher lib failed to load; commit-on-main guard inactive." >&2
    exit 0
}

# Target-repo resolution single-sourced (bead 29u4): the branch check must read the
# repo RECEIVING the commit (a worktree's HEAD when the commit is issued there), not
# the checkout this script ships in.
source "$SCRIPT_DIR/lib/resolve-target-repo.sh" 2>/dev/null

HOOK_INPUT=$(cat)
COMMAND=$(jq -r '.tool_input.command // empty' <<< "$HOOK_INPUT")

# Empty command → not our concern.
[[ -z "$COMMAND" ]] && exit 0

# Only a git commit is our concern — detection single-sourced in lib/commit-matcher.sh (mic).
is_git_commit "$COMMAND" || exit 0

# Command is a git commit invocation. Resolve the repo receiving it (29u4); a
# missing/corrupt lib falls back to the pre-29u4 root — never weaker — with a loud
# warning (broken install).
if declare -F resolve_target_repo >/dev/null 2>&1; then
    PROJECT_ROOT=$(resolve_target_repo "$HOOK_INPUT" "$FALLBACK_ROOT")
else
    echo "block-commit-main: resolve-target-repo lib failed to load; branch check uses the script-path root." >&2
    PROJECT_ROOT="$FALLBACK_ROOT"
fi

# Check the target repo's current branch.
BRANCH=$(git -C "$PROJECT_ROOT" symbolic-ref --short HEAD 2>/dev/null || echo "")

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
    cat <<JSON
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"INV-BRANCH-NOT-MAIN: commit on '${BRANCH}' blocked. PF-S2-06 recurrence guard. Switch to feature/* or fix/* branch first: 'git checkout -b feature/<short-description>'. If this is an authorized hotfix, override via direct user instruction."}}
JSON
    exit 0
fi

exit 0
