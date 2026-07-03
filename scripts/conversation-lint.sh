#!/usr/bin/env bash
# conversation-lint.sh — validate the care-agent conversation vault's frontmatter + structure.
#
# The same shape the wiki linter enforces on library entities, applied to the conversation vault
# (`vault/conversations/*.md`): every conversation file must carry conforming YAML frontmatter
# (title / type=conversation / participant / created / updated / turns / status), a valid date on
# `created`/`updated`, and an integer `turns`. Exit 0 clean, 1 on a violation (audit-helpers F-008
# contract). Usage: `conversation-lint.sh [conversation-dir]` (default `vault/conversations`).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/audit-helpers.sh"
source "$SCRIPT_DIR/lib/wiki-helpers.sh"

audit_init "conversation-lint"

CONV_DIR="${1:-vault/conversations}"

if [[ ! -d "$CONV_DIR" ]]; then
    info "no conversation vault at $CONV_DIR — nothing to lint"
    audit_summary
    audit_exit
fi

REQUIRED_FIELDS=(title type participant created updated turns status)

shopt -s nullglob
found=0
for page in "$CONV_DIR"/*.md; do
    found=1
    if ! wiki_has_frontmatter "$page"; then
        violation INV-CONVERSATION-VAULT "$page: no YAML frontmatter block"
        continue
    fi
    for field in "${REQUIRED_FIELDS[@]}"; do
        if [[ -z "$(wiki_frontmatter_field "$page" "$field")" ]]; then
            violation INV-CONVERSATION-VAULT "$page: missing required frontmatter field '$field'"
        fi
    done
    typ="$(wiki_frontmatter_field "$page" type)"
    if [[ -n "$typ" && "$typ" != "conversation" ]]; then
        violation INV-CONVERSATION-VAULT "$page: type must be 'conversation' (got '$typ')"
    fi
    turns="$(wiki_frontmatter_field "$page" turns)"
    if [[ -n "$turns" && ! "$turns" =~ ^[0-9]+$ ]]; then
        violation INV-CONVERSATION-VAULT "$page: 'turns' must be an integer (got '$turns')"
    fi
    for datefield in created updated; do
        val="$(wiki_frontmatter_field "$page" "$datefield")"
        if [[ -n "$val" && ! "$val" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            violation INV-CONVERSATION-VAULT "$page: '$datefield' must be YYYY-MM-DD (got '$val')"
        fi
    done
done

if [[ "$found" -eq 0 ]]; then
    info "no conversation files in $CONV_DIR — nothing to lint"
fi

audit_summary
audit_exit
