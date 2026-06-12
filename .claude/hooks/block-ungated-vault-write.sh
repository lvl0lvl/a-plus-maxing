#!/bin/bash
# block-ungated-vault-write.sh — PreToolUse hook for the Bash tool.
#
# Implements INV-WIKI-INGESTION-GATED at commit time. Mirror of block-commit-main.sh:
# when a `git commit` stages a gated wiki entity page (vault/{compounds,biomarkers,
# library}/), run scripts/wiki-ingest-lint.sh on the staged page(s); deny the commit
# if any fails the deterministic accuracy battery (provenance, structural, frontmatter,
# index sync). Turns the "no ungated page ships" discipline (bead bte / hfm / PF-S17-01)
# into a structural block instead of trust.
#
# Decision: deny iff (command is a git commit) AND (it stages a gated entity page) AND
# (wiki-ingest-lint.sh exits non-zero on the staged pages). Everything else passes
# through. The staged set and vault content are read from the TARGET repo — the
# working tree containing the hook input's cwd (worktree-aware since 29u4;
# script-path fallback when cwd is absent/unresolvable).
#
# TEST/OVERRIDE ENV (never set in production):
#   BLOCK_UNGATED_VAULT_PROJECT_ROOT — FALLBACK git root for staged-file detection +
#                                      vault content, used when the hook input
#                                      carries no resolvable cwd (29u4).
#   WIKI_BDA_CMD — inherited by the gate (tests stub it; unset in production).
#
# Exit codes (Claude Code hook convention):
#   prints deny JSON + exits 0 → deny tool call
#   exits 0 with no output      → allow tool call

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Fallback root when the hook input carries no resolvable cwd (see resolve-target-repo
# below). The env override lets tests seed it. Never set in production. The lint
# SCRIPT stays script-relative — it ships with this checkout; only the CONTENT root
# (staged pages, index, grandfather list) follows the target repo.
FALLBACK_ROOT="${BLOCK_UNGATED_VAULT_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
INGEST_LINT="$SCRIPT_DIR/../../scripts/wiki-ingest-lint.sh"

# git-commit detection is single-sourced (bead mic). Allow-on-error guard (wiki-ingest-lint
# is the second-line defense), but a missing/corrupt lib is a broken install — warn LOUDLY
# rather than silently disable the ingestion gate (PR#80 SEC-2).
source "$SCRIPT_DIR/lib/commit-matcher.sh" 2>/dev/null
declare -F is_git_commit >/dev/null 2>&1 || {
    echo "block-ungated-vault-write: commit-matcher lib failed to load; ingestion gate inactive." >&2
    exit 0
}

# Target-repo resolution single-sourced (bead 29u4): the staged-page check must read
# the index of the repo RECEIVING the commit (a worktree's, when the commit is issued
# there), not the checkout this script ships in.
source "$SCRIPT_DIR/lib/resolve-target-repo.sh" 2>/dev/null

HOOK_INPUT=$(cat)
COMMAND=$(jq -r '.tool_input.command // empty' <<< "$HOOK_INPUT")
[[ -z "$COMMAND" ]] && exit 0

# Only a git commit is our concern — detection single-sourced in lib/commit-matcher.sh (mic).
is_git_commit "$COMMAND" || exit 0

# Resolve the repo receiving the commit (29u4); a missing/corrupt lib falls back to
# the pre-29u4 root — never weaker — with a loud warning (broken install).
if declare -F resolve_target_repo >/dev/null 2>&1; then
    PROJECT_ROOT=$(resolve_target_repo "$HOOK_INPUT" "$FALLBACK_ROOT")
else
    echo "block-ungated-vault-write: resolve-target-repo lib failed to load; using the script-path root." >&2
    PROJECT_ROOT="$FALLBACK_ROOT"
fi

# Scope gate: the ingestion gate guards THIS trunk's wiki only — a commit whose
# target repo provably belongs to a different repository passes through (another
# project's vault/ layout is not this gate's concern). Worktrees of this repo
# share the git common dir and stay gated; an indeterminate target stays gated.
# Guarded on the helper existing: on a missing resolve lib the fallback above
# already pinned PROJECT_ROOT to this checkout, which is trivially in scope.
if declare -F target_is_this_repo >/dev/null 2>&1; then
    target_is_this_repo "$PROJECT_ROOT" "$FALLBACK_ROOT" || exit 0
fi

# Collect staged gated-dir pages (added/copied/modified; deletions are not gated).
# bash 3.2 — no mapfile; the case '*' spans '/', so nested library pages match.
PAGES=()
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    case "$f" in
        vault/compounds/*.md|vault/biomarkers/*.md|vault/library/*.md) PAGES+=("$f") ;;
    esac
done < <(git -C "$PROJECT_ROOT" diff --cached --name-only --diff-filter=ACM 2>/dev/null)

[[ ${#PAGES[@]} -eq 0 ]] && exit 0

# Run the deterministic gate on the staged pages. wiki-ingest-lint.sh itself skips
# any non-gated path (templates, README, methodology/, _archive/).
OUT=$(cd "$PROJECT_ROOT" && WIKI_REPO_ROOT="$PROJECT_ROOT" bash "$INGEST_LINT" "${PAGES[@]}" 2>&1)
RC=$?

[[ $RC -eq 0 ]] && exit 0

REASON="INV-WIKI-INGESTION-GATED: staged wiki page(s) failed the ingestion gate.
$(echo "$OUT" | grep 'VIOLATION' | head -8)
Fix the page, run 'scripts/wiki-ingest-lint.sh <page>' to re-check; for a pre-gate page add it to vault/library/_ingest-grandfather.txt."

jq -nc --arg r "$REASON" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
exit 0
