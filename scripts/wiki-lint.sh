#!/usr/bin/env bash
# wiki-lint.sh — periodic whole-vault wiki lint (WIKI.md "Lint" operation, finally a script).
#
# WIKI.md specifies a 6-check Lint to "run every 5 sessions or at phase boundaries"
# but never had a script — it was manual discipline. This is that script. It is the
# PERIODIC companion to the commit-time scripts/wiki-ingest-lint.sh: the commit gate
# blocks a single page's deterministic accuracy battery; this surveys the whole graph.
#
# THE 6 CHECKS (WIKI.md > Operations > Lint):
#   1 orphan        — entity page with no inbound [[link]] from another entity page   (info)
#   2 stale         — last_verified older than the page's review_cadence              (info)
#   3 contradiction — unresolved (Status: open) entries in meta/contradictions.md     (VIOLATION)
#   4 coverage      — active/planned compound or protocol with no [[biomarkers/...]]  (info)
#   5 link          — [[wikilink]] that does not resolve: forward-ref to an existing
#                     namespace = advisory (info); typo'd/dead namespace = VIOLATION
#   6 confidence    — page still marked confidence: provisional                       (info)
#
# Severity: `violation` (→ exit 1) only for genuinely-wrong state (unresolved
# contradiction, dead-namespace link). Advisory review flags use `info` so a vault
# mid-buildout (legitimate forward-refs, orphans, provisional pages) is not "red".
#
# Corpus: vault/{compounds,biomarkers,library,protocols,parameters} entity pages
# (excludes _*-templates, README, library/methodology/, _archive/). Other folders are
# operational memory, not wiki entities (WIKI.md "Non-wiki folders").
#
# TEST/OVERRIDE ENV: WIKI_REPO_ROOT (default: derived from this script's location).
#
# EXIT CODES: 0 — no violations; 1 — one or more violations.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${WIKI_REPO_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
source "$SCRIPT_DIR/lib/audit-helpers.sh"
source "$SCRIPT_DIR/lib/wiki-helpers.sh"

INV="INV-WIKI-INGESTION-GATED"
VAULT="$REPO_ROOT/vault"
CONTRADICTIONS="$VAULT/meta/contradictions.md"

audit_init "wiki-lint"

is_lint_corpus() {
    local p="$1" base="${1##*/}"
    case "$p" in
        *vault/compounds/*|*vault/biomarkers/*|*vault/library/*|*vault/protocols/*|*vault/parameters/*) ;;
        *) return 1 ;;
    esac
    case "$p" in *.md) ;; *) return 1 ;; esac
    case "$p" in *_archive/*|*vault/library/methodology/*) return 1 ;; esac
    case "$base" in _*|README.md) return 1 ;; esac
    return 0
}

days_since() {
    python3 - "$1" <<'PY' 2>/dev/null || echo -1
import sys, datetime
try:
    d = datetime.date.fromisoformat(sys.argv[1])
    print((datetime.date.today() - d).days)
except Exception:
    print(-1)
PY
}

cadence_threshold() {  # echo day-threshold for a review_cadence, or empty to skip
    case "$1" in
        weekly) echo 7 ;;
        monthly) echo 30 ;;
        quarterly) echo 90 ;;
        *) echo "" ;;          # manual | per-lab-panel | phase | session | unset -> no staleness
    esac
}

[ -d "$VAULT" ] || { info "no vault/ at $VAULT — nothing to lint"; audit_summary; audit_exit; }

# Build the corpus.
CORPUS=()
while IFS= read -r f; do
    is_lint_corpus "$f" && CORPUS+=("$f")
done < <(find "$VAULT" -type f -name '*.md' 2>/dev/null | sort)

if [ "${#CORPUS[@]}" -eq 0 ]; then
    info "corpus empty (no entity pages yet)"; audit_summary; audit_exit
fi
info "corpus: ${#CORPUS[@]} entity page(s)"

# All wikilink targets across the corpus (for the orphan inbound count).
ALL_LINKS="$(for f in "${CORPUS[@]}"; do wiki_wikilinks "$f"; done | sort)"

for f in "${CORPUS[@]}"; do
    rel="${f#"$REPO_ROOT"/}"
    wp="$(wiki_page_wikipath "$f")"
    type="$(wiki_entity_type "$f")"

    # --- 5: link integrity ---
    while IFS= read -r link; do
        [ -z "$link" ] && continue
        case "$link" in */*) ;; *) continue ;; esac          # skip bare placeholders
        wiki_resolve_link "$REPO_ROOT" "$link" && continue
        ns="${link%%/*}"
        if [ -d "$VAULT/$ns" ]; then
            info "$rel: forward-ref [[$link]] (target namespace exists; page not authored yet)"
        else
            violation "$INV" "$rel: dead link [[$link]] — namespace '$ns/' is not a vault folder (typo?)"
        fi
    done < <(wiki_wikilinks "$f")

    # --- 1: orphan ---
    inbound="$(printf '%s\n' "$ALL_LINKS" | grep -cxF "$wp" || true)"
    self="$(wiki_wikilinks "$f" | grep -cxF "$wp" || true)"
    if [ "$((inbound - self))" -le 0 ]; then
        info "$rel: orphan (no inbound [[$wp]] from another entity page)"
    fi

    # --- 2: stale ---
    lv="$(wiki_frontmatter_field "$f" last_verified)"
    rc="$(wiki_frontmatter_field "$f" review_cadence)"
    thr="$(cadence_threshold "$rc")"
    if [ -n "$lv" ] && [ -n "$thr" ]; then
        age="$(days_since "$lv")"
        if [ "$age" -ge 0 ] && [ "$age" -gt "$thr" ]; then
            info "$rel: stale (last_verified ${lv}, ${age}d ago > ${rc} ${thr}d)"
        fi
    fi

    # --- 6: confidence ---
    [ "$(wiki_frontmatter_field "$f" confidence)" = "provisional" ] \
        && info "$rel: confidence provisional (flag for trial/verification)"

    # --- 4: coverage ---
    if [ "$type" = "compound" ] || [ "$type" = "other" ]; then
        st="$(wiki_frontmatter_field "$f" status)"
        case "$st" in
            active|planned)
                wiki_wikilinks "$f" | grep -qE '^biomarkers/' \
                    || info "$rel: coverage gap (status=$st but no [[biomarkers/...]] tracking)"
                ;;
        esac
    fi
done

# --- 3: contradictions (once, whole-file) ---
# Strip ``` fenced blocks first so the "## Template" example (which literally shows
# "Status: open | resolved") is not miscounted as a real open contradiction.
if [ -f "$CONTRADICTIONS" ]; then
    open_n="$(awk '/^```/{fence=!fence; next} !fence' "$CONTRADICTIONS" \
        | grep -ciE '^[[:space:]]*-[[:space:]]*\*\*status:\*\*[[:space:]]*open' || true)"
    if [ "$open_n" -gt 0 ]; then
        violation "$INV" "meta/contradictions.md has ${open_n} unresolved (Status: open) contradiction(s)"
    else
        info "meta/contradictions.md: 0 open contradictions"
    fi
fi

audit_summary
audit_exit
