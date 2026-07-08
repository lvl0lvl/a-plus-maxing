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

genotype_finding_lines() {
    # Print each "- " bullet line in the ## Genotype Findings section, in order.
    # BUG1: tolerate leading whitespace so an INDENTED finding bullet is collected —
    # the matcher (scripts/genetics/match.py _genotype_findings) does line.strip()
    # THEN startswith("- "), so it parses indented findings; a col-0-only collector
    # would let an indented finding's raw genotype (SEC-ORD-02) ride past the gate.
    local f="$1"
    awk '
        /^## Genotype Findings[[:space:]]*$/ { insec=1; next }
        insec && /^## / { exit }                        # next section
        insec && /^[[:space:]]*-[[:space:]]/ { print }
    ' "$f"
}

genotype_findings_populated() {
    # Echo "yes" iff the ## Genotype Findings section has >=1 finding bullet that
    # is real content — a "- " line whose body after the dash is not a <placeholder>
    # or #comment (the same populated-vs-template discrimination as marker_populated).
    local f="$1" line body first
    while IFS= read -r line; do
        body="${line#-}"; body="${body#"${body%%[![:space:]]*}"}"   # strip "- " + leading ws
        first="${body:0:1}"
        if [ -n "$body" ] && [ "$first" != "<" ] && [ "$first" != "#" ]; then
            echo yes; return
        fi
    done < <(genotype_finding_lines "$f")
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
    check_enum  "$f" "$rel" source     "lab wearable manual calculation"
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

check_genetics() {
    # Strict variant-keyed battery for vault/library/genetics/ pages: frontmatter
    # struct (gene/rsid/evidence_tier/last_verified) + a populated ## Genotype
    # Findings section with per-line matcher grammar. The SEC-ORD-01 operator-token
    # scan + SEC-ORD-02 raw-genotype-in-trait-token guard are implemented below.
    # Provenance + index are the shared checks (check_provenance runs before this
    # dispatch — no waiver).
    local f="$1" rel="$2"
    require_field "$f" "$rel" type
    require_field "$f" "$rel" gene
    require_field "$f" "$rel" rsid
    check_enum  "$f" "$rel" evidence_tier "S A B C D"
    check_date  "$f" "$rel" last_verified
    wiki_has_section "$f" "Genotype Findings" \
        || violation "$INV" "$rel: missing required section '## Genotype Findings'"
    [ "$(genotype_findings_populated "$f")" = "yes" ] \
        || violation "$INV" "$rel: '## Genotype Findings' has no populated finding bullet"

    # Per-line grammar (Arch-1/QA-2): each finding bullet must be the matcher's
    # 'genotype: trait — prose' shape — selector ':' trait ' — ' prose (em-dash is
    # U+2014, byte-identical to the emitter). A line missing the colon or the em-dash
    # PASSES the populated check but the T2 matcher (scripts/genetics/match.py
    # _genotype_findings) SILENTLY skips it (degrades to a research-gap, no gate
    # signal), so a gate-passing page is guaranteed matcher-parseable.
    local gline
    while IFS= read -r gline; do
        printf '%s\n' "$gline" | grep -qE '^- .+: .+ — .+' \
            || violation "$INV" "$rel: '## Genotype Findings' line not in 'genotype: trait — prose' grammar (T2 matcher would silently skip): '$gline'"
    done < <(genotype_finding_lines "$f")

    # SEC-ORD-01: 0 operator-identity tokens in the body — the genetics library is
    # variant-keyed + reusable, never operator-associated (crown-jewel). READ-ONLY
    # shell-out to scripts.guard.pii_scan.scan_text_full; PYTHONPATH is the SCRIPT's
    # own checkout root (a temp vault under test carries no scripts/). The page PATH is
    # passed; content is read in-python — no operator PII is interpolated here.
    #
    # SEC1 fix: scan_text TRUNCATES at _MAX_SCAN_TEXT_LEN (4096) — an operator-identity
    # token past byte 4096 of a whole genetics PAGE would pass the gate fail-OPEN on a
    # PUBLIC repo. scan_text_full is the no-cap match-anywhere sibling; the cap only
    # bounds the router's single short field value, not a page-spanning whole-file scan.
    #
    # SEC-W1-03 fail-open fix: pii_scan.DEFAULT_IDENTITY_CONFIG is a RELATIVE path
    # that resolves against the process CWD — a manual `wiki-ingest-lint.sh <page>`
    # from a non-root cwd would silently load NO name tokens (fail-open for the
    # operator-NAME class). Pass an ABSOLUTE config rooted at $REPO_ROOT (the vault
    # under lint; == the script's checkout root in production) so name coverage is
    # cwd-independent. Config absent (fresh clone) -> empty name set, value patterns
    # still run — fail-closed direction.
    local root cfg hits
    root="$(cd "$SCRIPT_DIR/.." && pwd)"
    cfg="$REPO_ROOT/vault/meta/operator-identity.txt"
    # scan_public_content: this is PUBLIC library-PAGE content, not an operator value — a
    # research/provenance DATE or numeric citation in a genetics page is not the operator's
    # DOB/phone (the DOB + bare-digit-run classes guard the operator-VALUE boundary —
    # summarize/capture — beads yduw/6hts). Identity tokens + email/phone/postal still scan
    # (those WOULD be a public-page leak).
    if ! hits="$(PYTHONPATH="$root" python3 -c 'import sys; from scripts.guard.pii_scan import scan_public_content; print(scan_public_content(open(sys.argv[1], encoding="utf-8").read(), token_config=sys.argv[2], full=True))' "$f" "$cfg" 2>/dev/null)"; then
        violation "$INV" "$rel: SEC-ORD-01 operator-token scan failed to run"
    elif [ "${hits:-0}" -ge 1 ]; then
        violation "$INV" "$rel: operator-identity token(s) in body (SEC-ORD-01 — genetics library must be operator-free)"
    fi

    # SEC-ORD-02: no raw-genotype pattern in a finding line's trait-class-token field
    # (between the first ": " and the first " — "). The genotype is the SELECTOR
    # before the ": " ONLY; a raw rsID/allele must not ride the de-id trait-token.
    local line token
    while IFS= read -r line; do
        token="$(printf '%s\n' "$line" | sed -E 's/^- [^:]*: //; s/ — .*$//')"
        if printf '%s\n' "$token" | grep -qE 'rs[0-9]+|\([ACGTDI]+;[ACGTDI]+\)'; then
            violation "$INV" "$rel: raw genotype in '## Genotype Findings' trait-class-token (SEC-ORD-02 — genotype belongs in the selector only): '$token'"
        fi
    done < <(genotype_finding_lines "$f")
    return 0
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
        genetics)  check_genetics  "$abs" "$rel" ;;
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
