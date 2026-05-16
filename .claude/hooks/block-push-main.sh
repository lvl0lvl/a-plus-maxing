#!/bin/bash
# Block direct push to main/master (PreToolUse hook)
COMMAND=$(jq -r '.tool_input.command // empty' < /dev/stdin)
NORM=$(echo "$COMMAND" | tr -s '[:space:]' ' ')
# Match "git push <remote> main" or "git push <remote> master" (remote is any word)
if echo "$NORM" | grep -qiE 'git\s+push\s+\S+\s+(main|master)\b'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Direct push to main/master blocked. Use a feature branch."}}'
else
  exit 0
fi
