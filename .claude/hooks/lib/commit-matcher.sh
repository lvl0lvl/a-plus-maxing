#!/bin/bash
# commit-matcher.sh — SINGLE SOURCE for the git-commit detection shared by the three
# commit-gating PreToolUse hooks: block-pii-commit.sh, block-commit-main.sh,
# block-ungated-vault-write.sh. Sourced (not executed); each hook computes SCRIPT_DIR
# via BASH_SOURCE and runs `source "$SCRIPT_DIR/lib/commit-matcher.sh"`.
#
# Why a lib (bead mic): the matcher regex AND its NORM normalization were triplicated
# byte-identically across the three hooks, coordinated only by a KEEP-IN-SYNC comment
# that had already drifted once within a single PR (PR#76 QUAL-2). On this SECURITY
# boundary a one-hook divergence is a silent PII / branch / vault bypass — so the regex
# and its normalization live ONCE, here.
#
# is_git_commit "<raw command>" — return 0 if the command is a git commit invocation,
# 1 otherwise. NORM maps newlines to ';' (so a commit on a later line is seen) and
# squeezes + strips whitespace (so a leading-whitespace commit is not missed). The
# matcher (cvr) anchors at start / after a separator, tolerates optional env-var
# (VAR=val ) and path (dir/) prefixes before git, allows flags between git and commit,
# and ends on space, a separator [;&|], or EOL — so env-var-prefixed (EDITOR=vim git
# commit), path-prefixed (/usr/bin/git commit), and trailing-separator (git commit; /
# git commit&) forms are caught, while embedded text (echo git commit) and commit-tree
# / --commit-msg are not.
#
# CONSUMER OBLIGATION: a failed `source` is non-fatal under `set -uo pipefail` (no
# set -e), so a consumer MUST assert this lib loaded before relying on it —
# `declare -F is_git_commit >/dev/null || <fail per the consumer's posture>` — else an
# unguarded `is_git_commit ... || exit 0` silently ALLOWS on a missing/corrupt lib. The
# fail-CLOSED consumer (block-pii-commit) denies; the allow-on-error guards warn loudly
# (PR#80 SEC-1/SEC-2).

# The hardened matcher regex (cvr). Single definition; the three hooks + the unit test
# consume it from here.
COMMIT_MATCHER_RE='(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?git +([^|&;]*\s)?commit( |[;&|]|$)'

is_git_commit() {  # $1 = raw command; return 0 if a git commit invocation, else 1
    local norm
    norm=$(echo "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
    norm="${norm#" "}"; norm="${norm%" "}"
    echo "$norm" | grep -qE "$COMMIT_MATCHER_RE"
}
