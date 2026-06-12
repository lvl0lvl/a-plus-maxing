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
# the working tree containing the hook input's `cwd`. Fail-closed design (29u4): a
# missing/empty `cwd`, a non-directory, or a cwd outside any git working tree falls
# back to "<fallback root>" (the pre-29u4 script-path/env behavior), so consumers
# are never weaker than before this lib existed. NOT followed: an in-command
# `cd <elsewhere> && git commit` — the hook input's cwd names the tool call's
# STARTING directory; the pre-push backstop covers that shape (worktrees share the
# common .git, so its hook fires for worktree pushes too).
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
