#!/bin/bash
# resolve-target-repo.sh — SINGLE SOURCE for the target-repo resolution shared by the
# three commit-gating PreToolUse hooks: block-pii-commit.sh, block-commit-main.sh,
# block-ungated-vault-write.sh. Sourced (not executed), like lib/commit-matcher.sh.
#
# Why a lib (bead 29u4): each hook used to resolve PROJECT_ROOT from its own script
# path (SCRIPT_DIR/../.. — the checkout the hook ships in), but a `git commit` issued
# from a linked worktree lands on THAT worktree's HEAD/index. Script-path resolution
# made the branch check read the wrong repo (false denies / vacuous passes) and the
# staged-set scans read the wrong index (vacuous PII / ingestion passes). The repo
# that actually receives the commit is the working tree containing the Bash tool
# call's `cwd`, which the PreToolUse hook input carries on stdin. As with
# commit-matcher.sh, a one-hook divergence on this boundary is a silent bypass, so
# the resolution lives ONCE, here.
#
# resolve_target_repo "<hook stdin JSON>" "<fallback root>" — echo the toplevel of
# the working tree containing the hook input's `cwd`. Fallback behavior (29u4): a
# missing/empty `cwd`, a non-directory, or a cwd outside any git working tree falls
# back to "<fallback root>" (the pre-29u4 script-path/env behavior) — on THOSE
# fallback branches a consumer is never weaker than before this lib existed. (A
# cwd that RESOLVES to a different repository is a separate, deliberate case: the
# trunk-scope helper below lets consumers allow it through.) NOT followed: an
# in-command `cd <elsewhere> && git commit` — the hook input's cwd names the tool
# call's STARTING directory. Each consumer has its own catch-up layer for that
# residual: block-pii-commit -> the pre-push scan (worktrees share the common
# .git, so its hook fires for worktree pushes too); block-commit-main ->
# block-push-main; block-ungated-vault-write -> the periodic scripts/wiki-lint.sh.
#
# CONSUMER OBLIGATION: a failed `source` is non-fatal under `set -uo pipefail`, so a
# consumer MUST `declare -F resolve_target_repo` before calling and fall back to its
# pre-29u4 root on a missing/corrupt lib, warning loudly (broken install).

resolve_target_repo() {  # $1 = hook stdin JSON ; $2 = fallback root
    local cwd top
    cwd=$(jq -r '.cwd // empty' <<< "$1" 2>/dev/null)
    if [[ -n "$cwd" && -d "$cwd" ]]; then
        top=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
        if [[ -n "$top" ]]; then
            printf '%s\n' "$top"
            return 0
        fi
    fi
    printf '%s\n' "$2"
}

# target_is_this_repo "<resolved root>" "<fallback root>" — return 1 ONLY when the
# resolved target PROVABLY belongs to a different repository than the checkout this
# lib ships in: both roots resolve a `git rev-parse --git-common-dir` AND the real
# paths differ. Return 0 for the same repo, any of its linked worktrees (they share
# the common dir), and any INDETERMINATE target (non-git / unresolvable). The
# indeterminate case deliberately stays IN scope: the consumer's own posture (e.g.
# block-pii-commit's fail-closed git-plumbing deny) must decide what a broken
# target means — a scope check that cannot identify the target must not convert
# that into a silent allow.
target_is_this_repo() {  # $1 = resolved target root ; $2 = fallback root
    local t f
    t=$(git -C "$1" rev-parse --git-common-dir 2>/dev/null) || return 0
    f=$(git -C "$2" rev-parse --git-common-dir 2>/dev/null) || return 0
    # rev-parse emits a root-relative path at a main-checkout toplevel (".git") and
    # an absolute one from a linked worktree — real-path both against their roots
    # so the two forms compare (and /tmp symlinks on macOS normalize away).
    t=$(cd "$1" 2>/dev/null && cd "$t" 2>/dev/null && pwd -P) || return 0
    f=$(cd "$2" 2>/dev/null && cd "$f" 2>/dev/null && pwd -P) || return 0
    [[ "$t" == "$f" ]]
}
