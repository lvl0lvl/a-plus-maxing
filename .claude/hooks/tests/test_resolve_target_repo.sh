#!/usr/bin/env bash
# test_resolve_target_repo.sh — unit test for .claude/hooks/lib/resolve-target-repo.sh
# (bead 29u4 + the PR#107 trunk-scope helper).
#
# resolve_target_repo and target_is_this_repo are single-sourced for the three
# commit-gating hooks (block-pii-commit / block-commit-main / block-ungated-vault-
# write). The hook suites pin them end-to-end; this exercises both functions
# DIRECTLY so a lib edit reds here regardless of which hook consumes it — the same
# unit-level pinning test_commit_matcher.sh gives the matcher lib.
#
# Cases (resolve_target_repo "<hook stdin JSON>" "<fallback>"):
#   repo-root cwd          -> that repo's toplevel
#   linked-worktree cwd    -> the WORKTREE's toplevel (not the main checkout's)
#   subdir-of-worktree cwd -> the worktree's toplevel
#   missing cwd field      -> fallback
#   empty cwd              -> fallback
#   non-directory cwd      -> fallback
#   non-git cwd            -> fallback
#   malformed JSON         -> fallback
# Cases (target_is_this_repo "<resolved>" "<fallback>"):
#   same root              -> 0 (in scope)
#   linked worktree        -> 0 (shares the common git dir)
#   foreign repo           -> 1 (provably different -> out of scope)
#   non-git target         -> 0 (indeterminate stays GATED; consumer posture decides)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/resolve-target-repo.sh"

PASS=0
FAIL=0
pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkrepo() {  # $1 = dir ; $2 = branch
    git init -q -b "$2" "$1"
    git -C "$1" config user.email t@t.t
    git -C "$1" config user.name t
    git -C "$1" commit -q --allow-empty -m seed
}

MAIN="$TMP/mainrepo"; mkrepo "$MAIN" feat
WT="$TMP/wtree"; git -C "$MAIN" worktree add -q -b wt-branch "$WT"
mkdir -p "$WT/sub/dir"
FOREIGN="$TMP/foreign"; mkrepo "$FOREIGN" main
PLAIN="$TMP/plaindir"; mkdir -p "$PLAIN"
FALLBACK="$MAIN"

# Physical-path normalizer: git emits real paths while mktemp may hand back a
# symlinked /tmp prefix on macOS — compare apples to apples.
real() { (cd "$1" 2>/dev/null && pwd -P); }

payload_cwd() {  # $1 = cwd value ; emits hook stdin JSON carrying it
    printf '{"cwd":%s,"tool_input":{"command":"git commit"}}' \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')"
}

check_resolve() {  # $1 = label ; $2 = stdin JSON ; $3 = expected dir
    local got
    got=$(resolve_target_repo "$2" "$FALLBACK")
    if [[ -n "$got" && "$(real "$got")" == "$(real "$3")" ]]; then
        pass "$1"
    else
        fail "$1: expected $3, got ${got:-<empty>}"
    fi
}

echo "resolve_target_repo:"
check_resolve "repo-root cwd -> that repo"            "$(payload_cwd "$MAIN")"          "$MAIN"
check_resolve "linked-worktree cwd -> the worktree"   "$(payload_cwd "$WT")"            "$WT"
check_resolve "subdir-of-worktree cwd -> the worktree" "$(payload_cwd "$WT/sub/dir")"   "$WT"
check_resolve "missing cwd -> fallback"               '{"tool_input":{"command":"git commit"}}' "$FALLBACK"
check_resolve "empty cwd -> fallback"                 '{"cwd":"","tool_input":{"command":"git commit"}}' "$FALLBACK"
check_resolve "non-directory cwd -> fallback"         "$(payload_cwd "$TMP/no-such-dir")" "$FALLBACK"
check_resolve "non-git cwd -> fallback"               "$(payload_cwd "$PLAIN")"         "$FALLBACK"
check_resolve "malformed JSON -> fallback"            'not-json-at-all'                 "$FALLBACK"

echo "target_is_this_repo:"
if target_is_this_repo "$MAIN" "$MAIN"; then
    pass "same root -> in scope (rc 0)"
else
    fail "same root returned out-of-scope"
fi
if target_is_this_repo "$WT" "$MAIN"; then
    pass "linked worktree -> in scope (rc 0, shared common dir)"
else
    fail "linked worktree returned out-of-scope"
fi
if target_is_this_repo "$FOREIGN" "$MAIN"; then
    fail "foreign repo returned in-scope (scope gate dead)"
else
    pass "foreign repo -> out of scope (rc 1)"
fi
if target_is_this_repo "$PLAIN" "$MAIN"; then
    pass "non-git target -> indeterminate stays in scope (rc 0)"
else
    fail "non-git target returned out-of-scope (must stay gated — fail-closed consumers decide)"
fi

echo ""
echo "test_resolve_target_repo: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
