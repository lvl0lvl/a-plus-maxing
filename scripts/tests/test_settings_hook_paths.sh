#!/usr/bin/env bash
# test_settings_hook_paths.sh — asserts .claude/settings.json registers every hook
# with a PORTABLE ${CLAUDE_PROJECT_DIR}-relative path, not an absolute author-home
# path, so the governance/safety hook layer is live on any clone (bead 7zj).
#
# Background: settings.json originally registered all hooks as
#   /Users/<author>/.../.claude/hooks/<hook>.sh — absolute paths that do not exist on
# any other clone/machine, so Claude Code could not run them and the ENTIRE hook layer
# was inert on a clone (no commit-main block, no dangerous-command block, no
# role-inlining enforcement). The hook SCRIPTS self-derive their own dir, so the fix is
# the REGISTRATION: ${CLAUDE_PROJECT_DIR}/.claude/hooks/<hook>.sh (the documented
# Claude Code project-root placeholder).
#
# Checks (this reds on the pre-fix absolute-path settings.json):
#   1. settings.json parses and registers >=1 hook command.
#   2. Every registered command is ${CLAUDE_PROJECT_DIR}/.claude/hooks/<name>.sh —
#      no absolute /Users/ or /home/ or other absolute path.
#   3. Each command resolves (PROJECT_ROOT-relative) to an existing script file.
#   4. The 5 governance hooks are all registered.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SETTINGS="$PROJECT_ROOT/.claude/settings.json"
PORTABLE_PREFIX='${CLAUDE_PROJECT_DIR}/.claude/hooks/'

PASS=0
FAIL=0
pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

if [[ ! -f "$SETTINGS" ]]; then
    echo "settings.json not found at $SETTINGS"
    exit 1
fi

# Collect every registered hook command (bash 3.2 — no mapfile). The .hooks object is
# keyed by event name; each value is an array of {matcher, hooks:[{type, command}]}.
CMDS=()
while IFS= read -r line; do
    [[ -n "$line" ]] && CMDS+=("$line")
done < <(jq -r '.hooks[][].hooks[].command // empty' "$SETTINGS")

echo "settings.json: ${#CMDS[@]} registered hook command(s)"

# Check 1: at least one hook is registered.
if [[ ${#CMDS[@]} -ge 1 ]]; then
    pass "settings.json registers >=1 hook command"
else
    fail "no hook commands registered (jq parse failed or empty)"
fi

# Checks 2 + 3: every command is portable and resolves to an existing script.
for cmd in "${CMDS[@]}"; do
    case "$cmd" in
        "$PORTABLE_PREFIX"*)
            script="$PROJECT_ROOT/.claude/hooks/${cmd#"$PORTABLE_PREFIX"}"
            if [[ -f "$script" ]]; then
                pass "portable + resolves: $cmd"
            else
                fail "portable but script missing: $script (from '$cmd')"
            fi
            ;;
        /*)
            fail "absolute / clone-hostile path (inert on a clone): '$cmd'"
            ;;
        *)
            fail "command is neither \${CLAUDE_PROJECT_DIR}-relative nor recognized: '$cmd'"
            ;;
    esac
done

# Check 4: the governance hooks are all registered (block-pii-commit stays out — 3lv).
for hook in block-dangerous block-push-main block-commit-main block-ungated-vault-write enforce-role-inlining; do
    if printf '%s\n' "${CMDS[@]}" | grep -q "/${hook}\.sh$"; then
        pass "registered: $hook"
    else
        fail "governance hook not registered: $hook"
    fi
done

echo ""
echo "test_settings_hook_paths: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
