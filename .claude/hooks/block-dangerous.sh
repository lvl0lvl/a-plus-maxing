#!/bin/bash
# Block destructive commands (PreToolUse hook)
COMMAND=$(jq -r '.tool_input.command // empty' < /dev/stdin)
# Normalize whitespace for pattern matching
NORM=$(echo "$COMMAND" | tr -s '[:space:]' ' ')
if echo "$NORM" | grep -qiE '(^|[[:space:];])rm[[:space:]]+-[a-zA-Z]*[rRfF][a-zA-Z]*[[:space:]]+/($|[[:space:]])'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Destructive rm at filesystem root blocked."}}'
elif echo "$NORM" | grep -qiE 'git\s+reset\s+--hard'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git reset --hard blocked. Use git stash or git checkout instead."}}'
elif echo "$NORM" | grep -qiE 'git\s+push\s+.*(-f\b|--force\b)' && ! echo "$NORM" | grep -qiE -e '--force-with-lease'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git push --force blocked. Use --force-with-lease if needed."}}'
elif echo "$NORM" | grep -qiE 'git\s+clean\s+.*-[a-z]*f[a-z]*d|git\s+clean\s+.*-[a-z]*d[a-z]*f'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git clean -fd blocked. Review untracked files manually."}}'
else
  exit 0
fi
