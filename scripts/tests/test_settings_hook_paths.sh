#!/usr/bin/env bash
# test_settings_hook_paths.sh — asserts .claude/settings.json registers every hook
# with a PORTABLE ${CLAUDE_PROJECT_DIR}-relative path, not an absolute author-home
# path, so the governance/safety hook layer is live on any clone (bead 7zj).
#
# Background: settings.json originally registered all hooks as
#   /Users/<author>/.../.claude/hooks/<hook>.sh — absolute paths that do not exist on
# any other clone/machine, so Claude Code could not run them and the ENTIRE hook layer
# was inert on a clone (no commit-main block, no dangerous-command block, no
# role-inlining enforcement). The hook scripts are location-independent (each
# self-derives its own dir from BASH_SOURCE or references no path at all), so the fix
# is the REGISTRATION: ${CLAUDE_PROJECT_DIR}/.claude/hooks/<hook>.sh (the documented
# Claude Code project-root placeholder).
#
# This is a STATIC check (path shape + file existence + registration set); it does
# NOT prove the hooks EXECUTE — runtime expansion of ${CLAUDE_PROJECT_DIR} depends on
# the Claude Code build and is verified separately by a live-fire at fix time.
#
# Checks (this reds on the pre-fix absolute-path settings.json):
#   1. settings.json is valid JSON and registers >=1 hook command.
#   2. Every registered command is a FLAT ${CLAUDE_PROJECT_DIR}/.claude/hooks/<name>.sh
#      — no absolute /Users/ or /home/ path, no subdir / `..` traversal.
#   3. Each command resolves (PROJECT_ROOT-relative) to an existing script file.
#   4. The 6 governance hooks are all registered.
#   5. block-pii-commit.sh IS registered (3lv resolved S45: the clone-hostile
#      generic-gmail trunk scan became operator-specific + config-driven, so the
#      content-scan boundary is finally ON; an unregistration reds here).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# SETTINGS_HOOK_PATHS_FILE overrides the audited file for fixture tests (never set in
# production); default is the project's real settings.json.
SETTINGS="${SETTINGS_HOOK_PATHS_FILE:-$PROJECT_ROOT/.claude/settings.json}"
PORTABLE_PREFIX='${CLAUDE_PROJECT_DIR}/.claude/hooks/'

PASS=0
FAIL=0
pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

if [[ ! -f "$SETTINGS" ]]; then
    echo "settings.json not found at $SETTINGS"
    exit 1
fi

# Reject a malformed settings file up front: a jq parse error inside the process
# substitution below is invisible to `pipefail` and would otherwise surface as an
# empty CMDS (F1) — a clear message beats a downstream crash.
if ! jq empty "$SETTINGS" 2>/dev/null; then
    fail "settings.json is not valid JSON (or jq unavailable)"
    echo ""
    echo "test_settings_hook_paths: $PASS passed, $FAIL failed"
    exit 1
fi

# Collect every registered hook command (bash 3.2 — no mapfile). The .hooks object is
# keyed by event name; each value is an array of {matcher, hooks:[{type, command}]}.
CMDS=()
while IFS= read -r line; do
    [[ -n "$line" ]] && CMDS+=("$line")
done < <(jq -r '.hooks[][].hooks[].command // empty' "$SETTINGS")

echo "settings.json: ${#CMDS[@]} registered hook command(s)"

# Check 1: at least one hook is registered. Empty here (a zero-hook file) is a hard
# stop — falling through would hit `"${CMDS[@]}"` unbound under `set -u` on bash 3.2
# (F1), crashing before the remaining checks and the summary line print.
if [[ ${#CMDS[@]} -ge 1 ]]; then
    pass "settings.json registers >=1 hook command"
else
    fail "no hook commands registered (zero hooks)"
    echo ""
    echo "test_settings_hook_paths: $PASS passed, $FAIL failed"
    exit 1
fi

# Checks 2 + 3: every command is a FLAT portable path resolving to an existing script.
for cmd in ${CMDS[@]+"${CMDS[@]}"}; do
    case "$cmd" in
        "$PORTABLE_PREFIX"*)
            rest="${cmd#"$PORTABLE_PREFIX"}"
            case "$rest" in
                ""|*/*|*..*)
                    fail "non-flat hook path (subdir / traversal escapes hooks/): '$cmd'"
                    ;;
                *)
                    script="$PROJECT_ROOT/.claude/hooks/$rest"
                    if [[ -f "$script" ]]; then
                        pass "portable + resolves: $cmd"
                    else
                        fail "portable but script missing: $script (from '$cmd')"
                    fi
                    ;;
            esac
            ;;
        /*)
            fail "absolute / clone-hostile path (inert on a clone): '$cmd'"
            ;;
        *)
            fail "command is neither \${CLAUDE_PROJECT_DIR}-relative nor recognized: '$cmd'"
            ;;
    esac
done

# Check 4: the governance hooks are all registered.
for hook in block-dangerous block-push-main block-commit-main block-ungated-vault-write enforce-role-inlining; do
    if printf '%s\n' ${CMDS[@]+"${CMDS[@]}"} | grep -q "/${hook}\.sh$"; then
        pass "registered: $hook"
    else
        fail "governance hook not registered: $hook"
    fi
done

# Check 5 (3lv, flipped S45): block-pii-commit.sh MUST be registered — the S43
# clone-hostility (generic trunk-wide @gmail scan) was resolved by the
# operator-specific config-driven contact model, so the trunk content-scan
# boundary is ON. A future unregistration (silent boundary loss) reds here.
if printf '%s\n' ${CMDS[@]+"${CMDS[@]}"} | grep -q "/block-pii-commit\.sh$"; then
    pass "block-pii-commit.sh registered (3lv resolved S45 — content-scan boundary ON)"
else
    fail "block-pii-commit.sh NOT registered — the trunk content-scan boundary is silently OFF (3lv regression)"
fi

echo ""
echo "test_settings_hook_paths: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
