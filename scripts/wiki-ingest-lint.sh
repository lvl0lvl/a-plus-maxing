#!/usr/bin/env bash
# wiki-ingest-lint.sh — commit-time blocking accuracy battery for wiki ingestion (bead bte).
#
# Mechanical enforcement for INV-WIKI-INGESTION-GATED: a gated vault entity page
# (vault/{compounds,biomarkers,library}/) may not be committed unless it passes a
# DETERMINISTIC accuracy battery. Turns WIKI.md's Ingest/Conventions + the entity
# templates + research provenance from documented discipline into a hard gate.
#
# WHY THIS EXISTS (bead bte / hfm / PF-S17-01): the "no library page ships without
# passing provenance" rule was trust-based — the same soft-pass shape as the
# gate-3.5 issue that bit batch-4. This is the structural control.
#
# CHECKS (all BLOCKING except link-integrity, which is advisory here and enforced
# in the periodic scripts/wiki-lint.sh — forward-references to not-yet-authored
# pages are legitimate during buildout and must not false-block a commit):
#   1. provenance      — page's provenance_dir/provenance_slug pointer passes bda
#                        (grandfather-aware; see vault/library/_ingest-grandfather.txt)
#   2. structural      — mandatory sections present (compounds/biomarkers strict
#                        per WIKI.md templates; library lighter — heterogeneous)
#   3. frontmatter     — required fields present + enum-valid + last_verified a date;
#                        risk_tier=experimental requires contraindications + a linked
#                        monitoring biomarker + stopping criteria (WIKI.md Conventions)
#   4. index sync      — page registered in vault/meta/index.md (Ingest step 2)
#   5. link integrity  — ADVISORY (info only); blocking version lives in wiki-lint.sh
#
# USAGE:
#   wiki-ingest-lint.sh <vault-page.md> [more-pages.md ...]
#     Lints each gated entity page; non-gated args are skipped with an info line.
#
# TEST/OVERRIDE ENV (never set in production):
#   WIKI_REPO_ROOT  — repo root used to resolve vault/, grandfather, index (default:
#                     derived from this script's location).
#   WIKI_BDA_CMD    — command used for the provenance check (default: the real bda).
#                     Tests stub this to isolate orchestration from bda internals.
#
# EXIT CODES:
#   0 — every gated page passed every blocking check
#   1 — one or more blocking violations
#   2 — usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${WIKI_REPO_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
source "$SCRIPT_DIR/lib/audit-helpers.sh"
source "$SCRIPT_DIR/lib/wiki-helpers.sh"

INV="INV-WIKI-INGESTION-GATED"
BDA="${WIKI_BDA_CMD:-$REPO_ROOT/scripts/audit-research-provenance.sh}"
GRANDFATHER="$REPO_ROOT/vault/library/_ingest-grandfather.txt"
INDEX="$REPO_ROOT/vault/meta/index.md"

die() { echo "wiki-ingest-lint: $*" >&2; exit 2; }
[ "$#" -ge 1 ] || die "usage: wiki-ingest-lint.sh <vault-page.md> [more pages...]"

audit_init "wiki-ingest-lint"

abs_path() { case "$1" in /*) printf '%s\n' "$1" ;; *) printf '%s\n' "$REPO_ROOT/$1" ;; esac; }
rel_path() { local a; a="$(abs_path "$1")"; printf '%s\n' "${a#"$REPO_ROOT"/}"; }

is_grandfathered() {
    local rel="$1"
    [ -f "$GRANDFATHER" ] || return 1
    grep -vE '^[[:space:]]*(#|$)' "$GRANDFATHER" 2>/dev/null | grep -qxF "$rel"
}

require_field() {
    local f="$1" rel="$2" field="$3"
    [ -n "$(wiki_frontmatter_field "$f" "$field")" ] \
        || violation "$INV" "$rel: missing frontmatter field '$field'"
}

check_enum() {
    local f="$1" rel="$2" field="$3" allowed="$4" v a
    v="$(wiki_frontmatter_field "$f" "$field")"
    if [ -z "$v" ]; then violation "$INV" "$rel: missing frontmatter field '$field'"; return; fi
    for a in $allowed; do [ "$v" = "$a" ] && return 0; done
    violation "$INV" "$rel: frontmatter '$field: $v' not in {$(echo "$allowed" | tr ' ' ',')}"
}

check_date() {
    local f="$1" rel="$2" field="$3" v
    v="$(wiki_frontmatter_field "$f" "$field")"
    if [ -z "$v" ]; then violation "$INV" "$rel: missing frontmatter field '$field'"; return; fi
    echo "$v" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' \
        || violation "$INV" "$rel: '$field: $v' is not a YYYY-MM-DD date"
}

require_sections() {
    local f="$1" rel="$2"; shift 2
    local s
    for s in "$@"; do
        wiki_has_section "$f" "$s" || violation "$INV" "$rel: missing required section '## $s'"
    done
}

marker_populated() {
    # Echo "yes" iff the file has a bullet/heading line mentioning <keyword>
    # (case-insensitive) that is actually populated — either inline content
    # after the colon, or a following indented list/prose line. An empty
    # template form (#-comment or <placeholder> after the colon, or an
    # immediately-following sibling "- " bullet) counts as NOT populated.
    # Format-tolerant: handles "- contraindications:", bold "- **contraindications
    # (mechanism-derived):**", inline values, and following numbered lists.
    local f="$1" kw="$2"
    awk -v kw="$kw" '
        index(tolower($0), kw) > 0 && $0 ~ /^[[:space:]]*(-|\*|#)/ {
            n = split($0, p, ":")
            if (n >= 2) {
                rest = p[n]
                gsub(/^[[:space:]*_]+/, "", rest); gsub(/[[:space:]]+$/, "", rest)
                if (rest != "" && substr(rest,1,1) != "#" && substr(rest,1,1) != "<") { print "yes"; exit }
            }
            watching = 1; next
        }
        watching == 1 {
            if ($0 ~ /^##[[:space:]]/) exit          # next section
            if ($0 ~ /^-[[:space:]]/) exit           # next sibling bullet -> marker was empty
            s = $0; gsub(/[[:space:]]/, "", s); if (s == "") next
            match($0, /[^[:space:]]/); c = substr($0, RSTART, 1)
            if (c == "#" || c == "<") exit           # template placeholder
            print "yes"; exit                        # numbered item / sub-bullet / prose
        }
    ' "$f"
}

check_experimental() {
    # WIKI.md Conventions: risk_tier=experimental requires populated contraindications,
    # a linked monitoring biomarker, and stopping criteria.
    local f="$1" rel="$2"
    [ "$(marker_populated "$f" contraindication)" = "yes" ] \
        || violation "$INV" "$rel: risk_tier=experimental needs populated contraindications (WIKI.md Conventions)"
    wiki_wikilinks "$f" | grep -qE '^biomarkers/' \
        || violation "$INV" "$rel: risk_tier=experimental needs a linked monitoring [[biomarkers/...]] (WIKI.md Conventions)"
    [ "$(marker_populated "$f" 'stopping criteria')" = "yes" ] \
        || violation "$INV" "$rel: risk_tier=experimental needs populated stopping criteria in Trial Status (WIKI.md Conventions)"
}

check_compound() {
    local f="$1" rel="$2"
    require_sections "$f" "$rel" Metadata Mechanism "Evidence Summary" Protocol "Risk Profile" "Trial Status" Relations
    require_field "$f" "$rel" class
    check_enum  "$f" "$rel" evidence_tier "S A B C D"
    check_enum  "$f" "$rel" risk_tier     "low medium high experimental"
    check_enum  "$f" "$rel" status        "researching planned active paused trialed-stopped excluded"
    check_date  "$f" "$rel" last_verified
    [ "$(wiki_frontmatter_field "$f" risk_tier)" = "experimental" ] && check_experimental "$f" "$rel"
    return 0
}

check_biomarker() {
    local f="$1" rel="$2"
    require_sections "$f" "$rel" Metadata "Target Range" "Current Value" "Affected By" Relations
    check_enum  "$f" "$rel" category   "blood wearable functional subjective"
    require_field "$f" "$rel" unit
    check_enum  "$f" "$rel" source     "lab oura manual calculation"
    check_enum  "$f" "$rel" confidence "established supported provisional"
    check_date  "$f" "$rel" last_verified
}

check_library() {
    # library/ is heterogeneous (entry-shape pages AND /aplus-research output layers),
    # so the structural bar is light: frontmatter title+type + at least one section.
    local f="$1" rel="$2"
    require_field "$f" "$rel" title
    require_field "$f" "$rel" type
    [ -n "$(wiki_sections "$f")" ] || violation "$INV" "$rel: library page has no '## ' sections"
}

check_index() {
    local f="$1" rel="$2" wp
    [ -f "$INDEX" ] || { info "$rel: meta/index.md absent — index-sync skipped"; return; }
    wp="$(wiki_page_wikipath "$f")"
    if grep -qF "[[$wp]]" "$INDEX" || grep -qF "[[$wp " "$INDEX" || grep -qF "[[$wp|" "$INDEX"; then
        info "$rel: index-sync OK"
    else
        violation "$INV" "$rel: not registered in meta/index.md as [[$wp]] (Ingest step 2)"
    fi
}

check_links_advisory() {
    local f="$1" rel="$2" t miss=0
    while IFS= read -r t; do
        [ -z "$t" ] && continue
        case "$t" in */*) ;; *) continue ;; esac     # skip bare placeholders like [[experiment]]
        if ! wiki_resolve_link "$REPO_ROOT" "$t"; then
            info "$rel: unresolved link [[$t]] (advisory — enforced in periodic wiki-lint.sh)"
            miss=$((miss + 1))
        fi
    done < <(wiki_wikilinks "$f")
    [ "$miss" -eq 0 ] && info "$rel: all links resolve"
    return 0
}

check_provenance() {
    local f="$1" rel="$2" pdir pslug
    if is_grandfathered "$rel"; then
        info "$rel: provenance grandfathered (pre-gate page) — other checks still apply"
        return
    fi
    pdir="$(wiki_frontmatter_field "$f" provenance_dir)"
    pslug="$(wiki_frontmatter_field "$f" provenance_slug)"
    if [ -z "$pdir" ] || [ -z "$pslug" ]; then
        violation "$INV" "$rel: missing provenance_dir/provenance_slug frontmatter (no research provenance)"
    elif [ ! -d "$REPO_ROOT/$pdir" ]; then
        violation "$INV" "$rel: provenance_dir not found: $pdir"
    elif ! ( cd "$REPO_ROOT" && "$BDA" "$pdir" "$pslug" ) >/dev/null 2>&1; then
        violation "$INV" "$rel: bda provenance gate FAILED for $pdir ($pslug)"
    else
        info "$rel: provenance OK (bda EXIT 0 — $pdir / $pslug)"
    fi
}

check_page() {
    local arg="$1" abs rel type
    abs="$(abs_path "$arg")"; rel="$(rel_path "$arg")"
    if [ ! -f "$abs" ]; then info "$rel: not a regular file (deleted/renamed?) — skipped"; return; fi
    if ! wiki_is_gated_entity_page "$abs"; then info "$rel: not a gated entity page — skipped"; return; fi

    wiki_has_frontmatter "$abs" || violation "$INV" "$rel: missing YAML frontmatter"

    check_provenance "$abs" "$rel"
    type="$(wiki_entity_type "$abs")"
    case "$type" in
        compound)  check_compound  "$abs" "$rel" ;;
        biomarker) check_biomarker "$abs" "$rel" ;;
        library)   check_library   "$abs" "$rel" ;;
    esac
    check_index "$abs" "$rel"
    check_links_advisory "$abs" "$rel"
}

for page in "$@"; do
    check_page "$page"
done

audit_summary
audit_exit
