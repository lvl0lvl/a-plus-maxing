#!/usr/bin/env bash
# wiki-helpers.sh — shared primitives for the wiki ingestion gate + periodic lint.
#
# Sourced (not executed) by scripts/wiki-ingest-lint.sh (commit-time blocking
# battery) and scripts/wiki-lint.sh (periodic whole-vault lint). Provides the
# parsing both need so the two controls agree on what a "page", a "section", a
# "[[wikilink]]", and a "gated entity page" are.
#
# Pure read-only string/file helpers. No audit state, no exit. Compose with
# lib/audit-helpers.sh (which owns violation/info/exit).
#
# Usage:
#   source "$SCRIPT_DIR/lib/wiki-helpers.sh"
#   val=$(wiki_frontmatter_field "$page" risk_tier)
#   wiki_is_gated_entity_page "$page" && echo "gated"

# Guard against double-source.
if [[ "${_WIKI_HELPERS_LOADED:-0}" == "1" ]]; then
    return 0 2>/dev/null || exit 0
fi
_WIKI_HELPERS_LOADED=1

wiki_has_frontmatter() {
    # Exit 0 if the file's first line is a YAML frontmatter fence.
    local file="$1"
    [ -f "$file" ] || return 1
    [ "$(head -n1 "$file")" = "---" ]
}

wiki_frontmatter_field() {
    # Print the value of a top-level scalar frontmatter field, or nothing.
    # Only scans the frontmatter block (first --- ... ---), never the body,
    # so a body line like "- contraindications:" never masquerades as a field.
    # Arg 1: file. Arg 2: field name.
    local file="$1" field="$2"
    [ -f "$file" ] || return 1
    awk -v field="$field" '
        NR==1 && $0!="---" { exit }          # no frontmatter at all
        NR==1 { infm=1; next }
        infm && $0=="---" { exit }            # end of frontmatter
        infm {
            if ($0 ~ "^" field ":[[:space:]]*") {
                sub("^" field ":[[:space:]]*", "")
                gsub(/^["'\''[:space:]]+|["'\''[:space:]]+$/, "")
                print
                exit
            }
        }
    ' "$file"
}

wiki_sections() {
    # List level-2 (## ) section names, one per line, in document order.
    # Exactly two hashes + space, so ### subsections do not match.
    local file="$1"
    [ -f "$file" ] || return 1
    grep -E '^## ' "$file" 2>/dev/null | sed -E 's/^##[[:space:]]+//' || true
}

wiki_has_section() {
    # Exit 0 if the file has a level-2 section whose name matches arg 2 exactly.
    local file="$1" name="$2"
    wiki_sections "$file" | grep -qxF "$name"
}

wiki_wikilinks() {
    # List unique [[wikilink]] targets, stripped of |alias and #anchor.
    # Placeholder targets containing < or > (template residue) are dropped.
    local file="$1"
    [ -f "$file" ] || return 1
    grep -oE '\[\[[^][]+\]\]' "$file" 2>/dev/null \
        | sed -E 's/^\[\[//; s/\]\]$//; s/\|.*$//; s/#.*$//; s/[[:space:]]+$//' \
        | grep -vE '[<>]' \
        | sort -u || true
}

wiki_resolve_link() {
    # Exit 0 if a wikilink target resolves to an existing vault file.
    # Arg 1: repo root. Arg 2: target (e.g. compounds/bpc-157).
    local repo_root="$1" target="$2"
    target="${target%.md}"
    [ -f "$repo_root/vault/${target}.md" ]
}

wiki_entity_type() {
    # Echo the gated entity type for a path:
    # compound | biomarker | genetics | library | other.
    # genetics is matched BEFORE the library catch-all (more-specific glob first),
    # so a vault/library/genetics/ page routes to the strict check_genetics battery.
    case "$1" in
        *vault/compounds/*)        echo compound ;;
        *vault/biomarkers/*)       echo biomarker ;;
        *vault/library/genetics/*) echo genetics ;;
        *vault/library/*)          echo library ;;
        *)                         echo other ;;
    esac
}

wiki_page_wikipath() {
    # Echo the vault-relative wiki path (no .md) for a page, e.g.
    # /x/vault/compounds/bpc-157.md -> compounds/bpc-157. Used for index-sync.
    local path="$1"
    path="${path##*vault/}"
    echo "${path%.md}"
}

wiki_is_gated_entity_page() {
    # Exit 0 iff the path is a page the ingestion gate governs:
    #   under vault/{compounds,biomarkers,library}/, a .md file,
    #   NOT a _-prefixed template/meta file, NOT README.md,
    #   NOT under library/methodology/, NOT under any _archive/ dir.
    local path="$1"
    case "$path" in
        *vault/compounds/*|*vault/biomarkers/*|*vault/library/*) ;;
        *) return 1 ;;
    esac
    case "$path" in *.md) ;; *) return 1 ;; esac
    case "$path" in *_archive/*|*vault/library/methodology/*) return 1 ;; esac
    local base="${path##*/}"
    case "$base" in _*|README.md) return 1 ;; esac
    return 0
}
