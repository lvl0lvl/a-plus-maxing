#!/usr/bin/env bash
# test_commit_matcher.sh — unit test for .claude/hooks/lib/commit-matcher.sh (bead mic).
#
# The git-commit matcher + its NORM normalization are single-sourced in the lib for the
# three commit-gating hooks (block-pii-commit / block-commit-main / block-ungated-vault-
# write). This exercises is_git_commit DIRECTLY on the canonical positive, cvr-bypass,
# and non-commit forms — the cases the three hook suites pin end-to-end, now also pinned
# once at the unit level so a future matcher edit reds here regardless of which hook
# consumes it.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/commit-matcher.sh"

PASS=0
FAIL=0
pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

# Forms the matcher MUST detect: plain commits, flag/option forms, chained, AND the
# cvr-hardened bypass forms (env-var prefix, path prefix, trailing separator, leading
# whitespace, newline-on-a-later-line).
POSITIVE_FORMS=(
    "git commit"
    'git commit -m "msg"'
    'git commit -am "msg"'
    "git commit --amend"
    "git commit --amend --no-edit"
    'git -c user.name=foo commit -m "x"'
    "git --no-pager commit"
    'git status && git commit -m "y"'
    'echo done; git commit'
    "EDITOR=vim git commit -m x"
    "/usr/bin/git commit -m x"
    "git commit;"
    "git commit&"
    "FOO=1 BAR=2 git commit"
    "EDITOR=vim git commit;"
    " git commit"
    $'ls\ngit commit'
)

# Forms the matcher MUST NOT detect: other git subcommands, commit-tree, a branch named
# commit, and embedded-text negative controls (the commit token is not an invocation).
NON_COMMIT_FORMS=(
    "git status"
    "git log --oneline -5"
    "git rev-list --count HEAD"
    "ls -la"
    "git commit-tree HEAD^{tree}"
    "git checkout commit-feature"
    "echo git commit"
    "echo EDITOR=vim git commit"
    ""
)

echo "POSITIVE forms (is_git_commit -> match):"
for cmd in "${POSITIVE_FORMS[@]}"; do
    if is_git_commit "$cmd"; then
        pass "detected: ${cmd//$'\n'/\\n}"
    else
        fail "MISSED (bypass): ${cmd//$'\n'/\\n}"
    fi
done

echo "NON-COMMIT forms (is_git_commit -> no match):"
for cmd in "${NON_COMMIT_FORMS[@]}"; do
    if is_git_commit "$cmd"; then
        fail "FALSE-MATCH: ${cmd//$'\n'/\\n}"
    else
        pass "correctly ignored: ${cmd//$'\n'/\\n}"
    fi
done

# The hardened regex is exposed as a single named constant (the single-source guard).
if [[ -n "${COMMIT_MATCHER_RE:-}" ]]; then
    pass "COMMIT_MATCHER_RE is defined (single source for the 3 hooks)"
else
    fail "COMMIT_MATCHER_RE is not defined"
fi

# --- consumers' load posture on a MISSING lib (PR#80 SEC-1/SEC-2/F4) ----------------
# The hooks source the lib via $SCRIPT_DIR/lib/. Run each hook from a tmp dir WITHOUT a
# lib/ so the source fails, and confirm: block-pii-commit DENIES (fail-CLOSED — its PII
# scan must NOT be silently skipped); the two annoyance guards exit 0 with a LOUD stderr
# warning (allow-on-error posture, but a broken install must be visible, not silent).
HOOKS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MISSING_LIB_PAYLOAD='{"tool_input":{"command":"git commit -m x"}}'

run_hook_without_lib() {  # $1 = hook filename; sets globals OUT / ERR
    local hook="$1" tmp
    tmp=$(mktemp -d)
    cp "$HOOKS_DIR/$hook" "$tmp/$hook"   # copied alone — no sibling lib/ dir
    OUT=$(printf '%s' "$MISSING_LIB_PAYLOAD" | bash "$tmp/$hook" 2>"$tmp/err")
    ERR=$(cat "$tmp/err")
    rm -rf "$tmp"
}

echo "Consumer posture on a MISSING lib:"
run_hook_without_lib "block-pii-commit.sh"
if echo "$OUT" | grep -q '"permissionDecision":"deny"'; then
    pass "block-pii-commit.sh DENIES on missing lib (fail-closed)"
else
    fail "block-pii-commit.sh did NOT fail closed on missing lib (out: ${OUT:-<empty>})"
fi
for hook in block-commit-main.sh block-ungated-vault-write.sh; do
    run_hook_without_lib "$hook"
    if [[ -z "$OUT" ]] && echo "$ERR" | grep -qi "failed to load"; then
        pass "$hook loud-allows on missing lib (exit 0 + stderr warning)"
    else
        fail "$hook missing-lib posture wrong (out: ${OUT:-<empty>} / err: ${ERR:-<empty>})"
    fi
done

echo ""
echo "test_commit_matcher: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
