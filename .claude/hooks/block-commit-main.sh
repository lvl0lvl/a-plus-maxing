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
# Allow tests to point at a temp repo. Never set in production.
PROJECT_ROOT="${BLOCK_COMMIT_MAIN_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

COMMAND=$(jq -r '.tool_input.command // empty' < /dev/stdin)

# Empty command → not our concern.
[[ -z "$COMMAND" ]] && exit 0

# Normalize whitespace for matching.
NORM=$(echo "$COMMAND" | tr '\n' ';' | tr -s '[:space:]' ' ')
NORM="${NORM#" "}"; NORM="${NORM%" "}"

# Only a git commit is our concern. cvr: hardened matcher + normalization — KEEP IN
# SYNC across block-pii-commit.sh / block-commit-main.sh / block-ungated-vault-write.sh.
# NORM maps newlines to ';' (so a commit on a later line is seen) and strips leading/
# trailing space (so a leading-whitespace commit is not missed). The matcher anchors at
# start / after a separator, tolerates optional env-var (VAR=val ) and path (dir/)
# prefixes before git, allows flags between git and commit, and ends on space, a
# separator [;&|], or EOL — so env-var-prefixed (EDITOR=vim git commit), path-prefixed
# (/usr/bin/git commit), and trailing-separator (git commit; / git commit&) forms are
# caught, while embedded text (echo git commit) and commit-tree / --commit-msg are not.
if ! echo "$NORM" | grep -qE '(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?git +([^|&;]*\s)?commit( |[;&|]|$)'; then
    exit 0
fi

# Command is a git commit invocation. Check current branch.
BRANCH=$(git -C "$PROJECT_ROOT" symbolic-ref --short HEAD 2>/dev/null || echo "")

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
    cat <<JSON
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"INV-BRANCH-NOT-MAIN: commit on '${BRANCH}' blocked. PF-S2-06 recurrence guard. Switch to feature/* or fix/* branch first: 'git checkout -b feature/<short-description>'. If this is an authorized hotfix, override via direct user instruction."}}
JSON
    exit 0
fi

exit 0
