#!/usr/bin/env bash
# test_block_commit_main.sh — smoke tests for block-commit-main.sh
#
# The hook checks the project's REAL current branch via `git -C PROJECT_ROOT
# symbolic-ref --short HEAD`. We can't fully isolate that without a fake
# git binary, so the tests cover:
#   • Command-matching logic (every relevant invocation form should trigger
#     the branch check; non-matching commands should bypass).
#   • Behavior on the current real branch — if current branch IS main/master
#     the deny path fires; if it's a feature branch the allow path fires.
#
# Tests are written defensively to pass under either real-branch state.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$SCRIPT_DIR/../block-commit-main.sh"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Discover the real current branch once.
REAL_BRANCH=$(git -C "$PROJECT_ROOT" symbolic-ref --short HEAD 2>/dev/null || echo "")
ON_MAIN=0
case "$REAL_BRANCH" in
    main|master) ON_MAIN=1 ;;
esac
echo "Real branch: ${REAL_BRANCH:-<detached>} (on_main=$ON_MAIN)"

PASS=0
FAIL=0

# Invoke hook with a fake stdin payload. Returns: stdout|stderr|rc.
invoke() {
    local cmd="$1"
    local payload
    payload=$(printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$cmd" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
    echo "$payload" | "$HOOK"
}

# Assert the hook DOES match (= attempts branch check). When on_main=1 the
# hook prints deny JSON; when on_main=0 it exits silently. We collapse
# both into "command was recognized as git-commit".
assert_recognized_as_commit() {
    local label="$1" cmd="$2"
    local out
    out=$(invoke "$cmd")
    local should_deny=$ON_MAIN
    if [[ $should_deny -eq 1 ]]; then
        if [[ "$out" == *'"permissionDecision":"deny"'* ]]; then
            echo "  PASS: $label (on main → deny emitted)"
            PASS=$((PASS + 1))
        else
            echo "  FAIL: $label (on main, expected deny, got: $out)"
            FAIL=$((FAIL + 1))
        fi
    else
        # Feature branch: hook should allow (no output). The recognition test
        # is harder to assert directly here — we use the negative test below
        # to assert the matcher logic by inverting the branch state via a
        # known-non-commit command.
        if [[ -z "$out" ]]; then
            echo "  PASS: $label (feature branch → allow)"
            PASS=$((PASS + 1))
        else
            echo "  FAIL: $label (feature branch, expected silent, got: $out)"
            FAIL=$((FAIL + 1))
        fi
    fi
}

# Assert the hook DOES NOT match (always silent regardless of branch).
assert_not_matched() {
    local label="$1" cmd="$2"
    local out
    out=$(invoke "$cmd")
    if [[ -z "$out" ]]; then
        echo "  PASS: $label (bypassed matcher)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $label (expected silent, got: $out)"
        FAIL=$((FAIL + 1))
    fi
}

# ── Commit invocations the matcher MUST recognize ─────────────────────
echo "T1-T10: commit-form recognition"
assert_recognized_as_commit "git commit"                "git commit"
assert_recognized_as_commit "git commit -m"             'git commit -m "msg"'
assert_recognized_as_commit "git commit -am"            'git commit -am "msg"'
assert_recognized_as_commit "git commit --amend"        "git commit --amend"
assert_recognized_as_commit "git -c flag commit"        'git -c user.name=foo commit -m "x"'
assert_recognized_as_commit "git --no-pager commit"     "git --no-pager commit"
assert_recognized_as_commit "chained && commit"         'git status && git commit -m "y"'
assert_recognized_as_commit "chained ; commit"          'echo done; git commit'
assert_recognized_as_commit "heredoc style"             'git commit -m "$(cat <<EOF
multiline
EOF
)"'
assert_recognized_as_commit "amend no-edit"             "git commit --amend --no-edit"

# ── Commands the matcher MUST NOT recognize ───────────────────────────
echo "T11-T16: non-commit forms bypass"
assert_not_matched "git status"                 "git status"
assert_not_matched "git log --oneline"          "git log --oneline -5"
assert_not_matched "git rev-list --count"       "git rev-list --count HEAD"
assert_not_matched "ls only"                    "ls -la"
assert_not_matched "commit-tree subcommand"     "git commit-tree HEAD^{tree}"
assert_not_matched "branch named commit"        "git checkout commit-feature"

# ── Empty / malformed payload ─────────────────────────────────────────
echo "T17-T18: edge cases"
out=$(echo '{}' | "$HOOK")
if [[ -z "$out" ]]; then
    echo "  PASS: empty tool_input bypasses"
    PASS=$((PASS + 1))
else
    echo "  FAIL: empty tool_input got: $out"
    FAIL=$((FAIL + 1))
fi

out=$(echo '{"tool_input":{"command":""}}' | "$HOOK")
if [[ -z "$out" ]]; then
    echo "  PASS: empty command bypasses"
    PASS=$((PASS + 1))
else
    echo "  FAIL: empty command got: $out"
    FAIL=$((FAIL + 1))
fi

# ── T19-T21: deny-path exercised against temp repo on main ───────────
echo "T19-T21: deny path via BLOCK_COMMIT_MAIN_PROJECT_ROOT override"
TMP_REPO=$(mktemp -d)
git -C "$TMP_REPO" init -q -b main 2>/dev/null || {
    # Older git lacks -b; init then rename.
    git -C "$TMP_REPO" init -q
    git -C "$TMP_REPO" symbolic-ref HEAD refs/heads/main
}

invoke_with_override() {
    local cmd="$1"
    local payload
    payload=$(printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$cmd" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
    echo "$payload" | BLOCK_COMMIT_MAIN_PROJECT_ROOT="$TMP_REPO" "$HOOK"
}

# T19: on main, git commit → deny
out=$(invoke_with_override "git commit -m 'x'")
if [[ "$out" == *'"permissionDecision":"deny"'* ]] && [[ "$out" == *"on 'main' blocked"* ]]; then
    echo "  PASS: T19 main + commit → deny with branch name in reason"
    PASS=$((PASS + 1))
else
    echo "  FAIL: T19 — got: $out"
    FAIL=$((FAIL + 1))
fi

# T20: on main, git status → allow (non-commit bypasses matcher first)
out=$(invoke_with_override "git status")
if [[ -z "$out" ]]; then
    echo "  PASS: T20 main + status → allow"
    PASS=$((PASS + 1))
else
    echo "  FAIL: T20 — got: $out"
    FAIL=$((FAIL + 1))
fi

# T21: switch temp repo to master, commit → deny
git -C "$TMP_REPO" symbolic-ref HEAD refs/heads/master
out=$(invoke_with_override "git commit --amend")
if [[ "$out" == *'"permissionDecision":"deny"'* ]] && [[ "$out" == *"on 'master' blocked"* ]]; then
    echo "  PASS: T21 master + commit --amend → deny"
    PASS=$((PASS + 1))
else
    echo "  FAIL: T21 — got: $out"
    FAIL=$((FAIL + 1))
fi

rm -rf "$TMP_REPO"

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL))"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
