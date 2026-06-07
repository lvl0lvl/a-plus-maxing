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
# (wiki-ingest-lint.sh exits non-zero on the staged pages). Everything else passes through.
#
# TEST/OVERRIDE ENV (never set in production):
#   BLOCK_UNGATED_VAULT_PROJECT_ROOT — git root used for staged-file detection + vault
#                                      content (default: derived from this hook's location).
#   WIKI_BDA_CMD — inherited by the gate (tests stub it; unset in production).
#
# Exit codes (Claude Code hook convention):
#   prints deny JSON + exits 0 → deny tool call
#   exits 0 with no output      → allow tool call

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${BLOCK_UNGATED_VAULT_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
INGEST_LINT="$SCRIPT_DIR/../../scripts/wiki-ingest-lint.sh"

COMMAND=$(jq -r '.tool_input.command // empty' < /dev/stdin)
[[ -z "$COMMAND" ]] && exit 0

NORM=$(echo "$COMMAND" | tr -s '[:space:]' ' ')

# Only a git commit is our concern. cvr: hardened matcher — KEEP IN SYNC across
# block-pii-commit.sh / block-commit-main.sh / block-ungated-vault-write.sh. Also
# catches env-var-prefixed (EDITOR=vim git commit), path-prefixed (/usr/bin/git
# commit), and trailing-separator (git commit; / git commit&) forms the prior missed.
if ! echo "$NORM" | grep -qE '(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?git +([^|&;]*\s)?commit( |[;&|]|$)'; then
    exit 0
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
