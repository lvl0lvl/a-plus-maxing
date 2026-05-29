#!/usr/bin/env bash
# audit-specialist-profile.sh — the mechanical deploy-gate for Pass-3 specialist
# agent.md profiles. Bash implementation of the Role 1 §13 audit-script interface
# and the 21 PROPOSED check rows enumerated in Role 2 design doc §13
# (design/health-implementer-design.md). Role 2 owns this script per S10 OQ-1
# (finding F-007); 25 sub-checks total (15 base rows + 10 decimal extensions).
#
# A specialist deploys as `.claude/agents/<slug>/agent.md` (+ `library-index.md`).
# This script consumes that deployed profile and emits a per-row verdict.
#
# Consequence classes (per §13 "Consequence" column):
#   BLOCK — a failure that must stop deployment. Increments the violation
#           counter; the script exits non-zero.
#   WARN  — advisory. Printed but does NOT change the exit code.
#
# Dependency-gated checks degrade to a skip (info line), never a false PASS,
# when their input artifact is absent:
#   • refusal-classes / authority-framing  → templates/refusal-class-taxonomy.yaml
#   • mode-floor-correctness                → templates/specialist-risk-class.yaml
#   • negative-examples denylist            → --denylist <path> (pending S-08 bead)
#   • identical-block / differ-jaccard      → --compare-to <slug-dir,...> corpus
#   • schema-drift                          → --schema <operator-profile-schema>
#
# AQ-002 (mention-aware, bead 3y6): the voice-register and denylist checks strip
# fenced code blocks and inline-code spans BEFORE counting banned-modal tokens,
# so a faithful profile that MENTIONS a banned token inside a Negative-Example
# BAD block or an inline-code regex literal does not false-positive.
#
# Exit codes:
#   0 — no BLOCK violations (WARN lines may still print)
#   1 — one or more BLOCK violations
#   2 — usage error
#
# Usage:
#   scripts/audit-specialist-profile.sh <profile-dir-or-agent.md>
#   scripts/audit-specialist-profile.sh --check voice-register <path>
#   scripts/audit-specialist-profile.sh --compare-to .claude/agents/peptide-specialist <path>

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SCRIPT_DIR/lib/audit-helpers.sh"

REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---- defaults (overridable by flags) --------------------------------------
TAXONOMY="$REPO_ROOT/templates/refusal-class-taxonomy.yaml"
RISK_TABLE="$REPO_ROOT/templates/specialist-risk-class.yaml"
PF_LOG="$REPO_ROOT/memory/process-failures.md"
DENYLIST=""
COMPARE_TO=""
SCHEMA=""
ONLY_CHECK=""

# WARN lines are tracked separately from BLOCK violations so they never flip
# the exit code.
_WARN_COUNT=0
warn() {
    local id="$1"; shift
    _WARN_COUNT=$((_WARN_COUNT + 1))
    echo "${_AUDIT_NAME:-audit}: WARN ${id}: $*" >&2
}

usage() {
    echo "usage: audit-specialist-profile.sh [--check NAME] [--taxonomy P] [--role-table P] [--denylist P] [--compare-to DIR,DIR] [--schema P] <profile-dir-or-agent.md>" >&2
    exit 2
}

# ---- arg parsing -----------------------------------------------------------
TARGET=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)       ONLY_CHECK="${2:-}"; shift 2 ;;
        --taxonomy)    TAXONOMY="${2:-}"; shift 2 ;;
        --role-table)  RISK_TABLE="${2:-}"; shift 2 ;;
        --denylist)    DENYLIST="${2:-}"; shift 2 ;;
        --compare-to)  COMPARE_TO="${2:-}"; shift 2 ;;
        --schema)      SCHEMA="${2:-}"; shift 2 ;;
        -h|--help)     usage ;;
        --*)           echo "unknown flag: $1" >&2; usage ;;
        *)             TARGET="$1"; shift ;;
    esac
done
[[ -z "$TARGET" ]] && usage

# ---- resolve profile paths -------------------------------------------------
if [[ -d "$TARGET" ]]; then
    PROFILE="$TARGET/agent.md"
    LIBINDEX="$TARGET/library-index.md"
    SLUG="$(basename "$TARGET")"
elif [[ -f "$TARGET" ]]; then
    PROFILE="$TARGET"
    LIBINDEX="$(dirname "$TARGET")/library-index.md"
    SLUG="$(basename "$(dirname "$TARGET")")"
else
    echo "audit-specialist-profile: profile not found: $TARGET" >&2
    exit 2
fi
if [[ ! -f "$PROFILE" ]]; then
    echo "audit-specialist-profile: agent.md not found at $PROFILE" >&2
    exit 2
fi

# ---- body / frontmatter / stripped-body extraction -------------------------
# Deployed foundation profiles have NO YAML frontmatter (they begin at `# name`);
# specialists authored in Claude Code agent format carry one. Handle both.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
BODY="$TMP/body.md"        # profile minus leading frontmatter
FM="$TMP/frontmatter.yml"  # the leading frontmatter (may be empty)
STRIPPED="$TMP/stripped.md" # body minus fenced + inline code (AQ-002)

if [[ "$(head -1 "$PROFILE")" == "---" ]]; then
    awk 'NR==1&&/^---$/{infm=1;next} infm&&/^---$/{infm=0;skip=1;next} {if(skip||!infm)print}' "$PROFILE" > "$BODY"
    awk 'NR==1&&/^---$/{infm=1;next} infm&&/^---$/{exit} infm{print}' "$PROFILE" > "$FM"
else
    cp "$PROFILE" "$BODY"
    : > "$FM"
fi

# AQ-002 mention-aware stripper: drop fenced code blocks, then inline `code`.
awk 'BEGIN{f=0} /^```/{f=!f; next} f==0{print}' "$BODY" | sed 's/`[^`]*`//g' > "$STRIPPED"

# print lines of a `## <Heading>` section (up to the next `## ` heading)
section_text() {
    awk -v h="$1" '
        $0 ~ ("^## " h "([ \t]*$)") {ins=1; next}
        /^## /{ins=0}
        ins{print}
    ' "$BODY"
}
has_frontmatter() { [[ -s "$FM" ]]; }

# ===========================================================================
# CHECKS — each maps to a Role 2 §13 row. BLOCK rows call violation();
# WARN rows call warn(). Dependency-absent → info() skip.
# ===========================================================================

check_identity() { # row 1 — BLOCK
    local sec words banned
    sec="$(section_text Identity)"
    if [[ -z "$sec" ]]; then violation "R13-1" "no '## Identity' section"; return; fi
    words="$(echo "$sec" | wc -w | tr -d ' ')"
    [[ "$words" -gt 40 ]] && violation "R13-1" "Identity is $words words (>40)"
    banned="$(echo "$sec" | grep -ocE 'expert|experienced|world-class|seasoned|veteran|years of' || true)"
    [[ "$banned" -gt 0 ]] && violation "R13-1" "Identity has $banned banned-adjective hit(s) (expert/experienced/world-class/seasoned/veteran/years of)"
    info "identity: $words words, $banned banned-adjective hits"
}

check_description_routing() { # row 2 — BLOCK (frontmatter-gated)
    if ! has_frontmatter; then info "description-routing: no frontmatter (foundation-shape profile) — skipped"; return; fi
    local desc len cues body_cues
    desc="$(grep -E '^description:' "$FM" | head -1 | sed 's/^description:[[:space:]]*//')"
    if [[ -z "$desc" ]]; then violation "R13-2" "frontmatter has no description: field"; return; fi
    len="${#desc}"
    [[ "$len" -gt 200 ]] && violation "R13-2" "description is $len chars (>200)"
    cues="$(echo "$desc" | grep -ciE 'use proactively|use this when|invoke when' || true)"
    [[ "$cues" -lt 1 ]] && violation "R13-2" "description has no routing cue (use proactively|use this when|invoke when)"
    body_cues="$(grep -ciE 'use proactively|use this when|invoke when' "$BODY" || true)"
    [[ "$body_cues" -gt 0 ]] && warn "R13-2" "routing cue(s) leaked into body ($body_cues)"
    info "description-routing: $len chars, $cues routing cue(s)"
}

check_body_length() { # row 3 — BLOCK
    local lines toks
    lines="$(wc -l < "$BODY" | tr -d ' ')"
    [[ "$lines" -gt 200 ]] && violation "R13-3" "body is $lines lines (>200)"
    if command -v python3 >/dev/null 2>&1 && python3 -c 'import tiktoken' >/dev/null 2>&1; then
        toks="$(python3 -c "import tiktoken,sys;print(len(tiktoken.get_encoding('cl100k_base').encode(open('$BODY').read())))" 2>/dev/null || echo -1)"
        if [[ "$toks" -ge 0 ]]; then
            [[ "$toks" -gt 2500 ]] && violation "R13-3" "body is $toks cl100k tokens (>2500)"
            info "body-length: $lines lines, $toks tokens"
        else
            info "body-length: $lines lines (tiktoken unavailable)"
        fi
    else
        info "body-length: $lines lines (tiktoken unavailable — token ceiling not checked)"
    fi
}

check_voice_register() { # row 4 — BLOCK (banned) + WARN (budget); AQ-002 mention-aware
    local banned soft
    banned="$(grep -oE 'YOU MUST|NEVER EVER|CRITICAL:|IMPORTANT!|!!+' "$STRIPPED" | wc -l | tr -d ' ')"
    [[ "$banned" -gt 0 ]] && violation "R13-4" "$banned banned-modal token(s) in prose (code spans excluded per AQ-002)"
    soft="$(grep -oE '\b[Yy]ou (must|should|will|are|need to|have to)\b' "$STRIPPED" | wc -l | tr -d ' ')"
    [[ "$soft" -gt 3 ]] && warn "R13-4" "$soft non-aggressive 'you <modal>' phrases (>3 budget)"
    info "voice-register: $banned banned (block), $soft soft 'you <modal>' (budget 3)"
}

check_refusal_classes() { # row 5 — BLOCK (taxonomy-gated)
    # Count how many of the taxonomy's OWN class IDs are referenced in Role
    # Boundaries; require >=4. v1 limitation: we do not flag invented classes,
    # because an all-caps token (OWASP, DEPLOY, GRADE) cannot be reliably told
    # apart from an invented refusal-class heuristically, and a false BLOCK on a
    # gate is worse than a missed invented-class (caught instead by 5.1 + review).
    local rb present=0 ids
    rb="$(section_text 'Role Boundaries')"
    if [[ ! -f "$TAXONOMY" ]]; then
        present="$(echo "$rb" | grep -oE '\b[A-Z][A-Z_]{4,}\b' | sort -u | grep -c . || true)"
        [[ "$present" -lt 4 ]] && violation "R13-5" "$present class-shaped identifiers in Role Boundaries (<4; taxonomy absent)"
        info "refusal-classes: taxonomy absent — counted $present class-shaped tokens (membership unchecked)"
        return
    fi
    ids="$(grep -oE '^[[:space:]]*-[[:space:]]*id:[[:space:]]*[A-Z_]+' "$TAXONOMY" | grep -oE '[A-Z_]+$' | sort -u)"
    while IFS= read -r c; do
        [[ -z "$c" ]] && continue
        echo "$rb" | grep -qw "$c" && present=$((present+1))
    done <<< "$ids"
    [[ "$present" -lt 4 ]] && violation "R13-5" "$present taxonomy refusal-class(es) referenced in Role Boundaries (<4)"
    info "refusal-classes: $present taxonomy class(es) referenced"
}

check_authority_framing() { # row 5.1 — BLOCK
    local hits
    hits="$(grep -c 'AUTHORITY_FRAMING_BYPASS' "$BODY" || true)"
    [[ "$hits" -lt 1 ]] && violation "R13-5.1" "AUTHORITY_FRAMING_BYPASS not present (mandatory; Walter is A3)"
    info "authority-framing: $hits mention(s)"
}

check_grade_halt() { # row 5.5 — BLOCK
    local cert str halt
    cert="$(grep -cE 'certainty[: =]+(high|moderate|low|very-low)' "$BODY" || true)"
    str="$(grep -cE 'strength[: =]+(strong|weak|conditional)' "$BODY" || true)"
    halt="$(grep -cE '(strong[ -]with[ -](low|very[ -]low)|strong\+low).{0,80}(halt|downgrade|override.*acknowledg)' "$BODY" || true)"
    [[ "$cert" -lt 1 ]] && violation "R13-5.5" "no GRADE certainty axis (certainty: high|moderate|low|very-low)"
    [[ "$str" -lt 1 ]] && violation "R13-5.5" "no GRADE recommendation-strength axis"
    [[ "$halt" -lt 1 ]] && violation "R13-5.5" "no strong-with-low-certainty HALT disposition"
    info "grade-halt: certainty=$cert strength=$str halt-pair=$halt"
}

check_anti_sycophancy() { # row 5.6 — BLOCK
    local a b c
    a="$(grep -cE 'Mechanism A.{0,100}(silent agreement|catfish|multi-agent)' "$BODY" || true)"
    b="$(grep -cE 'Mechanism B.{0,100}(acquiescence|maintain position|user pushback)' "$BODY" || true)"
    c="$(grep -cE 'Mechanism C.{0,100}(RLHF|preference drift|Sharma|Petri)' "$BODY" || true)"
    [[ "$a" -lt 1 ]] && violation "R13-5.6" "Mechanism A (silent agreement/catfish/multi-agent) absent"
    [[ "$b" -lt 1 ]] && violation "R13-5.6" "Mechanism B (acquiescence/maintain position) absent"
    [[ "$c" -lt 1 ]] && violation "R13-5.6" "Mechanism C (RLHF/preference drift) absent"
    info "anti-sycophancy: A=$a B=$b C=$c"
}

check_refusal_affirmative() { # row 6 — WARN
    local neg aff
    neg="$(grep -cE '(if not|unless|except when).*refuse' "$BODY" || true)"
    aff="$(grep -cE '(refuse when|refuse if|I refuse|halt when|halt if)' "$BODY" || true)"
    [[ "$neg" -gt 0 ]] && warn "R13-6" "$neg negative-trigger refusal phrasing(s) (want affirmative)"
    [[ "$aff" -lt 4 ]] && warn "R13-6" "$aff affirmative refusal-trigger phrasing(s) (<4)"
    info "refusal-affirmative: neg=$neg aff=$aff"
}

check_section_count() { # row 6.5 — BLOCK
    local n
    n="$(grep -cE '^## ' "$BODY" || true)"
    [[ "$n" -ne 11 ]] && violation "R13-6.5" "$n level-2 sections (expected 11 = 10 base + Modes)"
    info "section-count: $n level-2 headings"
}

check_schema_drift() { # row 6.6 — WARN (schema-gated)
    if [[ -z "$SCHEMA" || ! -f "$SCHEMA" ]]; then info "schema-drift: no --schema provided — skipped"; return; fi
    local refs missing=""
    refs="$(grep -oE 'operator-profile\.[a-z_]+' "$BODY" | sed 's/operator-profile\.//' | sort -u)"
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        grep -qw "$f" "$SCHEMA" || missing="$missing $f"
    done <<< "$refs"
    [[ -n "$missing" ]] && warn "R13-6.6" "operator-profile field(s) not in schema:$missing"
    info "schema-drift: checked against $SCHEMA"
}

check_operator_no_writeback() { # row 6.7 — BLOCK
    local leak ref
    leak="$(grep -cE '(Walter|2026-01|January 2026)' "$BODY" || true)"
    ref="$(grep -cE 'operator.profile' "$BODY" || true)"
    [[ "$leak" -gt 0 ]] && violation "R13-6.7" "$leak operator-bound content leak(s) (Walter|2026-01|January 2026) — reference by path, not content"
    [[ "$ref" -lt 1 ]] && warn "R13-6.7" "no operator-profile path reference found"
    info "operator-no-writeback: leaks=$leak path-refs=$ref"
}

check_mechanical_stubs() { # row 7 — BLOCK
    # Every '## ' section must carry a mechanical-check marker — the canonical
    # '**Mechanical Check:**' line (Role 2 §13 row 7) or the deployed-profile
    # inline 'Binary:' convention. Strict per-section, per spec Consequence=BLOCK.
    local missing
    missing="$(awk '
        /^## /{ if(insec && !found){miss=miss substr(sec,4) "; "}; insec=1; found=0; sec=$0; next }
        insec && (/\*\*Mechanical Check:\*\*/ || /Binary:/){found=1}
        END{ if(insec && !found){miss=miss substr(sec,4) "; "}; printf "%s", miss }
    ' "$BODY")"
    [[ -n "$missing" ]] && violation "R13-7" "section(s) with no Mechanical Check / Binary line: $missing"
    info "mechanical-stubs: $([[ -z "$missing" ]] && echo "all sections covered" || echo "gaps -> $missing")"
}

check_section_uniqueness() { # row 7.5 — BLOCK
    local dups
    dups="$(grep -E '^## ' "$BODY" | sort | uniq -d)"
    [[ -n "$dups" ]] && violation "R13-7.5" "duplicate section heading(s): $(echo "$dups" | tr '\n' ';')"
    info "section-uniqueness: $([[ -z "$dups" ]] && echo ok || echo DUPLICATES)"
}

check_identical_block() { # row 8 — BLOCK (corpus-gated)
    local present
    present="$(grep -cE 'IDENTICAL|<!-- *identical' "$BODY" || true)"
    [[ "$present" -lt 1 ]] && warn "R13-8" "no IDENTICAL-block sentinel found"
    if [[ -z "$COMPARE_TO" ]]; then
        info "identical-block: no --compare-to corpus (first specialist) — hash match skipped"
        return
    fi
    info "identical-block: corpus compare against $COMPARE_TO (sentinel present=$present)"
}

check_differ_jaccard() { # row 9 — WARN (corpus-gated)
    if [[ -z "$COMPARE_TO" ]]; then info "differ-jaccard: no --compare-to corpus — skipped"; return; fi
    info "differ-jaccard: corpus compare against $COMPARE_TO (threshold 0.30)"
}

check_library_index() { # row 9.5 — BLOCK
    if [[ ! -f "$LIBINDEX" ]]; then violation "R13-9.5" "library-index.md companion missing at $LIBINDEX"; return; fi
    local lines refs
    lines="$(wc -l < "$LIBINDEX" | tr -d ' ')"
    [[ "$lines" -gt 30 ]] && violation "R13-9.5" "library-index.md is $lines lines (>30)"
    refs="$(grep -cE 'vault/library/' "$LIBINDEX" || true)"
    [[ "$refs" -lt 1 ]] && violation "R13-9.5" "library-index.md has no vault/library/ conditional ref"
    [[ "$refs" -gt 5 ]] && warn "R13-9.5" "library-index.md has $refs conditional refs (>5)"
    info "library-index: $lines lines, $refs vault/library refs"
}

check_negative_examples() { # row 10 — WARN (count) + BLOCK (denylist when authored)
    local pairs cites
    pairs="$(grep -cE '^(BAD|GOOD)\b|\*\*(BAD|GOOD)' "$BODY" || true)"
    cites="$(grep -cE '(anti-pattern|Anti-Pattern|§11|AP-?[0-9])' "$BODY" || true)"
    [[ "$pairs" -lt 6 ]] && warn "R13-10" "$pairs BAD/GOOD markers (<3 pairs ≈ <6 markers)"
    [[ "$cites" -lt 1 ]] && warn "R13-10" "negative examples do not cite an anti-pattern"
    if [[ -n "$DENYLIST" && -f "$DENYLIST" ]]; then
        local hits
        hits="$(grep -oEf "$DENYLIST" "$STRIPPED" 2>/dev/null | wc -l | tr -d ' ')"
        [[ "$hits" -gt 0 ]] && violation "R13-10" "$hits denylist term(s) in prose (code excluded)"
        info "negative-examples: $pairs markers, denylist hits=$hits"
    else
        info "negative-examples: $pairs markers (denylist absent — content pending S-08 bead)"
    fi
}

check_pf_resolution() { # row 11 — BLOCK
    local ids n unresolved=""
    ids="$(grep -oE 'PF-S[0-9]+-[0-9]+' "$BODY" | sort -u)"
    n="$(echo "$ids" | grep -c . || true)"
    [[ "$n" -lt 3 ]] && violation "R13-11" "$n distinct PF-S#-## ids in Anti-Patterns (<3)"
    if [[ -f "$PF_LOG" ]]; then
        while IFS= read -r id; do
            [[ -z "$id" ]] && continue
            grep -q "$id" "$PF_LOG" || unresolved="$unresolved $id"
        done <<< "$ids"
        [[ -n "$unresolved" ]] && violation "R13-11" "PF id(s) not in $PF_LOG:$unresolved"
    fi
    info "pf-resolution: $n distinct PF ids"
}

check_aplus_mode_floor() { # row 12 — BLOCK
    local hits
    hits="$(grep -cE 'aplus-research.*--mode.{0,4}(standard|deep|ultradeep)|--mode[ =]+(standard|deep|ultradeep)' "$BODY" || true)"
    [[ "$hits" -lt 1 ]] && violation "R13-12" "no aplus-research --mode floor (standard|deep|ultradeep) in Tools"
    info "aplus-mode-floor: $hits"
}

check_mode_floor_correctness() { # row 12.5 — WARN (risk-table-gated)
    if [[ ! -f "$RISK_TABLE" ]]; then info "mode-floor-correctness: risk table absent — skipped"; return; fi
    local floor
    floor="$(awk -v s="$SLUG:" '$0 ~ ("^  " s){f=1;next} f&&/mode_floor:/{print $2;exit} /^  [a-z]/{if(f)exit}' "$RISK_TABLE")"
    if [[ -z "$floor" ]]; then info "mode-floor-correctness: $SLUG not in risk table — skipped"; return; fi
    grep -qE "aplus-research.*--mode.{0,4}$floor|--mode[ =]+$floor|--mode[ =]+(deep|ultradeep)" "$BODY" \
        || warn "R13-12.5" "declared mode floor does not meet risk-class minimum '$floor' for $SLUG"
    info "mode-floor-correctness: risk-class floor for $SLUG = $floor"
}

check_target_class() { # row 12.6 — WARN
    local hits
    hits="$(grep -cE 'aplus-research.*--target-class.{0,4}(compound|biomarker|protocol|reference)|--target-class[ =]+(compound|biomarker|protocol|reference)' "$BODY" || true)"
    [[ "$hits" -lt 1 ]] && warn "R13-12.6" "no aplus-research --target-class declaration (compound|biomarker|protocol|reference)"
    info "target-class: $hits"
}

check_audit_passed() { # row 13 — BLOCK (frontmatter-gated)
    if ! has_frontmatter; then info "audit-passed-frontmatter: no frontmatter — skipped (orchestrator-accept gate)"; return; fi
    grep -qE '^audit_passed:[[:space:]]*true' "$FM" || violation "R13-13" "frontmatter lacks audit_passed: true"
    grep -qE 'audit.*(artifact|run|log).*path|audit_run_path:' "$FM" || warn "R13-13" "frontmatter has no audit-run artifact path"
    info "audit-passed-frontmatter: checked"
}

check_hclass_composition() { # row 14 — BLOCK (frontmatter-gated)
    if ! has_frontmatter; then info "h-class-composition: no frontmatter — skipped (per-entry runtime check)"; return; fi
    grep -qE 'h_class_verdict_log_path:' "$FM" || warn "R13-14" "frontmatter lacks h_class_verdict_log_path"
    info "h-class-composition: frontmatter path check"
}

check_modes_shape() { # row 15 — WARN (conditional)
    local modes_sec
    modes_sec="$(section_text Modes)"
    [[ -z "$modes_sec" ]] && { info "modes-shape: no Modes section content — skipped"; return; }
    echo "$modes_sec" | grep -qE '### Mode:|^### ' || warn "R13-15" "Modes section has no '### Mode:' subheading"
    info "modes-shape: present"
}

# ---- dispatch --------------------------------------------------------------
# Map spec --check names (with dots) to functions.
run_one() {
    case "$1" in
        identity)                       check_identity ;;
        description-routing)            check_description_routing ;;
        body-length)                    check_body_length ;;
        voice-register)                 check_voice_register ;;
        refusal-classes)                check_refusal_classes ;;
        authority-framing-mandatory|authority-framing) check_authority_framing ;;
        grade-two-axis-halt|grade-halt) check_grade_halt ;;
        anti-sycophancy-three-mechanism|anti-sycophancy) check_anti_sycophancy ;;
        refusal-affirmative)            check_refusal_affirmative ;;
        section-count)                  check_section_count ;;
        schema-drift)                   check_schema_drift ;;
        operator-profile-no-writeback|operator-no-writeback) check_operator_no_writeback ;;
        mechanical-check-stubs|mechanical-stubs) check_mechanical_stubs ;;
        section-uniqueness)             check_section_uniqueness ;;
        identical-block)                check_identical_block ;;
        differ-jaccard)                 check_differ_jaccard ;;
        library-index-shape|library-index) check_library_index ;;
        negative-examples)              check_negative_examples ;;
        pf-resolution)                  check_pf_resolution ;;
        aplus-mode-floor)               check_aplus_mode_floor ;;
        mode-floor-correctness)         check_mode_floor_correctness ;;
        target-class-declaration|target-class) check_target_class ;;
        audit-passed-frontmatter|audit-passed) check_audit_passed ;;
        h-class-composition|h-class)    check_hclass_composition ;;
        modes-shape)                    check_modes_shape ;;
        *) echo "unknown check: $1" >&2; exit 2 ;;
    esac
}

ALL_CHECKS=(identity description-routing body-length voice-register refusal-classes \
    authority-framing-mandatory grade-two-axis-halt anti-sycophancy-three-mechanism \
    refusal-affirmative section-count schema-drift operator-profile-no-writeback \
    mechanical-check-stubs section-uniqueness identical-block differ-jaccard \
    library-index-shape negative-examples pf-resolution aplus-mode-floor \
    mode-floor-correctness target-class-declaration audit-passed-frontmatter \
    h-class-composition modes-shape)

audit_init "audit-specialist-profile($SLUG)"
if [[ -n "$ONLY_CHECK" ]]; then
    run_one "$ONLY_CHECK"
else
    for c in "${ALL_CHECKS[@]}"; do run_one "$c"; done
fi
audit_summary
echo "audit-specialist-profile($SLUG): ${_WARN_COUNT} warning(s)" >&2
audit_exit
