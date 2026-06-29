#!/usr/bin/env bash
# test_wiki_ingest_lint.sh — non-tautological smoke tests for wiki-ingest-lint.sh.
#
# Each blocking check has a PASS fixture and a FAIL fixture that differ by exactly
# the thing under test, so a removed check makes the FAIL case stop failing.
# bda is stubbed via WIKI_BDA_CMD (this suite tests the gate's orchestration, not
# bda internals — bda has its own 8/8 suite). WIKI_REPO_ROOT points at a temp vault.
#
# Cases:
#   1  valid experimental compound (provenance ok)            -> PASS
#   2  same, provenance_dir/slug removed, not grandfathered    -> FAIL (missing provenance)
#   3  same, provenance present but bda stub rejects           -> FAIL (bda failed)
#   4  no provenance BUT listed in grandfather allowlist       -> PASS (provenance skipped)
#   5  missing a required section (## Risk Profile)            -> FAIL (missing section)
#   6  invalid enum (risk_tier: bogus)                         -> FAIL (enum)
#   7  invalid date (last_verified: notadate)                  -> FAIL (date)
#   8  experimental, contraindications empty (template form)   -> FAIL (experimental completeness)
#   9  valid page not registered in meta/index.md             -> FAIL (index sync)
#   10 valid biomarker page                                    -> PASS
#   11 biomarker invalid enum (category: bogus)                -> FAIL (enum)
#   12 minimal valid library layer page                        -> PASS
#   13 non-gated file (_template.md)                           -> PASS (skipped)
#   14 valid page w/ unresolved forward-ref link               -> PASS (link advisory, non-blocking)
#   15 biomarker source: wearable (ADR-0011 D4 generalized enum) -> PASS
#   16 biomarker source: oura (ADR-0011 D4 retired the device token) -> FAIL (enum)
#   G1 wiki_entity_type genetics path -> genetics, other library -> library  -> routing
#   G2 valid genetics variant page                                          -> PASS
#   G3 genetics missing gene / rsid                                         -> FAIL (frontmatter)
#   G4 genetics missing / empty ## Genotype Findings                        -> FAIL (structural)
#   G4c ## Genotype Findings with only the template placeholder bullet       -> FAIL (no populated finding)
#   G5 genetics missing provenance, not grandfathered                       -> FAIL (no waiver)
#   G6 genetics _template.md (non-gated)                                    -> PASS (skipped)
#   G7 genetics page + injected operator email in body (SEC-ORD-01)         -> FAIL (detection phrase)
#   G7b NAME-class operator token via temp-repo identity config (SEC-ORD-01) -> FAIL (config-driven name path)
#   G8 raw genotype in a ## Genotype Findings trait-token field (SEC-ORD-02) -> FAIL (raw genotype)
#   G-grammar finding line missing the ' — ' em-dash (matcher-unparseable)   -> FAIL (per-line grammar)
#   G9 operator token AFTER >4096 bytes of filler (SEC1 scan_text_full)       -> FAIL (whole-page scan, no cap)
#   G10 INDENTED finding bullet w/ raw rsID in trait-token (BUG1 col-tolerant) -> FAIL (raw genotype)
#   G-WIKI vault/WIKI.md carries the library/genetics schema section (T1 AC-7) -> PASS (schema present)

set -uo pipefail
PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$(cd "$SCRIPT_DIR/.." && pwd)/wiki-ingest-lint.sh"

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO/vault/compounds" "$REPO/vault/biomarkers" "$REPO/vault/library/peptides" \
         "$REPO/vault/library/genetics" \
         "$REPO/vault/meta" "$REPO/vault/library" "$REPO/design/.test-design-work"

# bda stubs (ignore args; exit code is the point)
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/bda-pass.sh"
printf '#!/usr/bin/env bash\nexit 1\n' > "$TMP/bda-fail.sh"
chmod +x "$TMP/bda-pass.sh" "$TMP/bda-fail.sh"

# index registers the pages that should pass index-sync
cat > "$REPO/vault/meta/index.md" <<'IDX'
# Wiki Index
## compounds/
- [[compounds/test-compound]]
- [[compounds/grandfathered]]
## biomarkers/
- [[biomarkers/test-marker]]
## library/
- [[library/peptides/test-layer]]
## genetics/
- [[library/genetics/cyp1a2-rs762551]]
IDX

# grandfather allowlist
cat > "$REPO/vault/library/_ingest-grandfather.txt" <<'GF'
# grandfather
vault/compounds/grandfathered.md
GF

# ---- fixture emitters ----
emit_compound() {  # $1 = slug ; emits a fully-valid experimental compound
    cat <<EOF
---
title: Test Compound
type: compound
permalink: a-plus-maxing/compounds/$1
class: peptide
evidence_tier: B
risk_tier: experimental
status: researching
created: 2026-06-02
last_verified: 2026-06-02
provenance_dir: design/.test-design-work
provenance_slug: test-compound
---

# Test Compound

## Metadata
- class: peptide

## Mechanism
Pathway prose, cites a source.

## Evidence Summary
- [Author 2024] — n=20, RCT, endpoint, effect size, [[library/peptides/test-layer]]

## Protocol
- dose: 250 mcg
- route: subQ

## Risk Profile
- contraindications:
  1. Pregnancy and lactation — no human data
  2. Active malignancy — theoretical neoangiogenesis concern
- monitoring:
  - [[biomarkers/test-marker]] — baseline + monthly

## Trial Status
- stopping criteria: any unexpected bleeding; tumor-marker elevation; transaminitis >2x ULN

## Relations
- [[biomarkers/test-marker]]
EOF
}

emit_biomarker() {  # $1 = slug
    cat <<EOF
---
title: Test Marker
type: biomarker
permalink: a-plus-maxing/biomarkers/$1
category: blood
unit: mg/dL
source: lab
confidence: provisional
created: 2026-06-02
last_verified: 2026-06-02
review_cadence: quarterly
provenance_dir: design/.test-design-work
provenance_slug: test-compound
---

# Test Marker

## Metadata
- category: blood

## Target Range
- ideal: 0-1

## Current Value
- value: 0.5 (2026-06-02)

## Affected By
- [[compounds/test-compound]]

## Relations
- [[experiments/x]]
EOF
}

emit_library() {  # minimal valid library layer
    cat <<EOF
---
title: Test Layer
type: layer
permalink: a-plus-maxing/library/peptides/test-layer
provenance_dir: design/.test-design-work
provenance_slug: test-compound
---

# Test Layer

## Survey
Body content with a citation.
EOF
}

emit_genetics() {  # $1 = slug ; emits a fully-valid variant-keyed genetics page
    cat <<EOF
---
title: CYP1A2 rs762551
type: genetics
permalink: a-plus-maxing/library/genetics/$1
gene: CYP1A2
rsid: rs762551
evidence_tier: B
created: 2026-06-02
last_verified: 2026-06-02
provenance_dir: design/.test-design-work
provenance_slug: test-compound
---

# CYP1A2 rs762551

## Genotype Findings
- (A;A): fast-caffeine-metabolism — clears caffeine quickly, tolerates higher intake [1]
- (A;C): intermediate-caffeine-metabolism — intermediate clearance [2]
- (C;C): slow-caffeine-metabolism — slow clearance; higher CV risk at high intake [3]
EOF
}

run() {  # $1 = bda stub ; $2.. = page args (repo-relative). sets RC + OUT
    OUT="$(cd "$REPO" && WIKI_REPO_ROOT="$REPO" WIKI_BDA_CMD="$1" bash "$SCRIPT" "${@:2}" 2>&1)"
    RC=$?
}

CP="$REPO/vault/compounds"; BM="$REPO/vault/biomarkers"; LB="$REPO/vault/library/peptides"
GN="$REPO/vault/library/genetics"

# Case 1: valid compound -> PASS
emit_compound test-compound > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
[ "$RC" -eq 0 ] && ok "valid experimental compound PASSes" || { bad "case1 expected rc0 got $RC"; echo "$OUT"; }

# Case 2: remove provenance, not grandfathered -> FAIL (non-tautological vs case 1)
emit_compound test-compound | grep -v '^provenance_' > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "missing provenance"; } \
    && ok "missing provenance FAILs" || { bad "case2 expected rc1+missing provenance got $RC"; echo "$OUT"; }

# Case 3: provenance present but bda rejects -> FAIL (non-tautological vs case 1's passing stub)
emit_compound test-compound > "$CP/test-compound.md"
run "$TMP/bda-fail.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "bda provenance gate FAILED"; } \
    && ok "bda-rejected provenance FAILs" || { bad "case3 expected rc1+bda FAILED got $RC"; echo "$OUT"; }

# Case 4: no provenance but grandfathered -> PASS (non-tautological vs case 2: only the allowlist differs)
emit_compound grandfathered | grep -v '^provenance_' > "$CP/grandfathered.md"
run "$TMP/bda-fail.sh" vault/compounds/grandfathered.md
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "grandfathered"; } \
    && ok "grandfathered page skips provenance and PASSes" || { bad "case4 expected rc0 got $RC"; echo "$OUT"; }

# Case 5: missing required section -> FAIL
emit_compound test-compound | sed 's/^## Risk Profile/## RiskProfileTypo/' > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "missing required section '## Risk Profile'"; } \
    && ok "missing required section FAILs" || { bad "case5 expected rc1 got $RC"; echo "$OUT"; }

# Case 6: invalid enum -> FAIL
emit_compound test-compound | sed 's/^risk_tier: experimental/risk_tier: bogus/' > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "risk_tier: bogus"; } \
    && ok "invalid enum FAILs" || { bad "case6 expected rc1 got $RC"; echo "$OUT"; }

# Case 7: invalid date -> FAIL
emit_compound test-compound | sed 's/^last_verified: 2026-06-02/last_verified: notadate/' > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "not a YYYY-MM-DD date"; } \
    && ok "invalid date FAILs" || { bad "case7 expected rc1 got $RC"; echo "$OUT"; }

# Case 8: experimental with empty contraindications (template form) -> FAIL
emit_compound test-compound \
  | sed '/^## Risk Profile/,/^## Trial Status/c\
## Risk Profile\
- contraindications:\
- monitoring:\
  - [[biomarkers/test-marker]] — baseline\
\
## Trial Status' > "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "populated contraindications"; } \
    && ok "experimental w/ empty contraindications FAILs" || { bad "case8 expected rc1 got $RC"; echo "$OUT"; }

# Case 9: valid page NOT in index -> FAIL
emit_compound not-indexed > "$CP/not-indexed.md"
run "$TMP/bda-pass.sh" vault/compounds/not-indexed.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "not registered in meta/index.md"; } \
    && ok "page absent from index FAILs" || { bad "case9 expected rc1 got $RC"; echo "$OUT"; }

# Case 10: valid biomarker -> PASS
emit_biomarker test-marker > "$BM/test-marker.md"
run "$TMP/bda-pass.sh" vault/biomarkers/test-marker.md
[ "$RC" -eq 0 ] && ok "valid biomarker PASSes" || { bad "case10 expected rc0 got $RC"; echo "$OUT"; }

# Case 11: biomarker invalid enum -> FAIL
emit_biomarker test-marker | sed 's/^category: blood/category: bogus/' > "$BM/test-marker.md"
run "$TMP/bda-pass.sh" vault/biomarkers/test-marker.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "category: bogus"; } \
    && ok "biomarker invalid enum FAILs" || { bad "case11 expected rc1 got $RC"; echo "$OUT"; }

# Case 12: minimal valid library layer -> PASS
emit_library > "$LB/test-layer.md"
run "$TMP/bda-pass.sh" vault/library/peptides/test-layer.md
[ "$RC" -eq 0 ] && ok "valid library layer PASSes" || { bad "case12 expected rc0 got $RC"; echo "$OUT"; }

# Case 13: non-gated file (_template) -> PASS (skipped)
emit_compound x > "$CP/_template.md"
run "$TMP/bda-pass.sh" vault/compounds/_template.md
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "not a gated entity page"; } \
    && ok "non-gated _template skipped, PASSes" || { bad "case13 expected rc0+skip got $RC"; echo "$OUT"; }

# Case 14: unresolved forward-ref link does NOT block (advisory) -> PASS
emit_compound test-compound > "$CP/test-compound.md"
printf '\n- [[biomarkers/does-not-exist-yet]]\n' >> "$CP/test-compound.md"
run "$TMP/bda-pass.sh" vault/compounds/test-compound.md
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "advisory"; } \
    && ok "unresolved forward-ref link is advisory, non-blocking" || { bad "case14 expected rc0+advisory got $RC"; echo "$OUT"; }

# Case 15: biomarker source: wearable -> PASS (ADR-0011 D4: source enum generalized oura->wearable)
emit_biomarker test-marker | sed 's/^source: lab/source: wearable/' > "$BM/test-marker.md"
run "$TMP/bda-pass.sh" vault/biomarkers/test-marker.md
[ "$RC" -eq 0 ] && ok "biomarker source: wearable PASSes (D4 generalized enum)" || { bad "case15 expected rc0 got $RC"; echo "$OUT"; }

# Case 16: biomarker source: oura -> FAIL (ADR-0011 D4 retired the device-specific token; non-tautological vs case 15)
emit_biomarker test-marker | sed 's/^source: lab/source: oura/' > "$BM/test-marker.md"
run "$TMP/bda-pass.sh" vault/biomarkers/test-marker.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "source: oura"; } \
    && ok "biomarker source: oura FAILs (D4 retired the oura token)" || { bad "case16 expected rc1+source: oura got $RC"; echo "$OUT"; }

# ---- genetics library section (ADR-0032-T1) ----

# Case G1: wiki_entity_type routes a genetics path -> genetics, other library -> library (AC-1)
G1=$( source "$(cd "$SCRIPT_DIR/.." && pwd)/lib/wiki-helpers.sh"
      printf '%s %s' "$(wiki_entity_type "$REPO/vault/library/genetics/x.md")" \
                     "$(wiki_entity_type "$REPO/vault/library/peptides/x.md")" )
[ "$G1" = "genetics library" ] \
    && ok "genetics path types 'genetics', other library types 'library'" \
    || bad "G1 expected 'genetics library' got '$G1'"

# Case G2: valid genetics variant page -> PASS (positive control)
emit_genetics cyp1a2-rs762551 > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
[ "$RC" -eq 0 ] && ok "valid genetics page PASSes" || { bad "G2 expected rc0 got $RC"; echo "$OUT"; }

# Case G3a: missing gene -> FAIL (non-tautological vs G2)
emit_genetics cyp1a2-rs762551 | grep -v '^gene:' > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "field 'gene'"; } \
    && ok "genetics missing gene FAILs" || { bad "G3a expected rc1+gene got $RC"; echo "$OUT"; }

# Case G3b: missing rsid -> FAIL
emit_genetics cyp1a2-rs762551 | grep -v '^rsid:' > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "field 'rsid'"; } \
    && ok "genetics missing rsid FAILs" || { bad "G3b expected rc1+rsid got $RC"; echo "$OUT"; }

# Case G4a: ## Genotype Findings section missing (renamed) -> FAIL (structural)
emit_genetics cyp1a2-rs762551 | sed 's/^## Genotype Findings/## GenotypeFindingsTypo/' > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "Genotype Findings"; } \
    && ok "genetics missing Genotype Findings section FAILs" || { bad "G4a expected rc1 got $RC"; echo "$OUT"; }

# Case G4b: ## Genotype Findings present but empty (no finding bullet) -> FAIL (populated)
emit_genetics cyp1a2-rs762551 | sed '/^## Genotype Findings/,$d' > "$GN/cyp1a2-rs762551.md"
printf '\n## Genotype Findings\n' >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "Genotype Findings"; } \
    && ok "genetics empty Genotype Findings FAILs" || { bad "G4b expected rc1 got $RC"; echo "$OUT"; }

# Case G4c: ## Genotype Findings whose only bullet is the literal template placeholder
# -> FAIL (no populated finding; QA-2). The placeholder satisfies the grammar but its
# `<...>`-led body is not real content.
emit_genetics cyp1a2-rs762551 | sed '/^## Genotype Findings/,$d' > "$GN/cyp1a2-rs762551.md"
printf '\n## Genotype Findings\n- <genotype>: <trait-class-token> — ...\n' >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "has no populated finding"; } \
    && ok "genetics template-placeholder-only finding FAILs (no populated finding)" || { bad "G4c expected rc1 got $RC"; echo "$OUT"; }

# Case G5: missing provenance, not grandfathered -> FAIL (no genetics waiver)
emit_genetics cyp1a2-rs762551 | grep -v '^provenance_' > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "missing provenance"; } \
    && ok "genetics missing provenance FAILs (no waiver)" || { bad "G5 expected rc1 got $RC"; echo "$OUT"; }

# Case G6: _template.md is non-gated -> PASS (skipped, mirrors case 13)
emit_genetics x > "$GN/_template.md"
run "$TMP/bda-pass.sh" vault/library/genetics/_template.md
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "not a gated entity page"; } \
    && ok "genetics _template skipped, PASSes" || { bad "G6 expected rc0+skip got $RC"; echo "$OUT"; }

# Case G7: G2 page + one injected value-class operator token in body -> FAIL (SEC-ORD-01).
# Asserts the DETECTION-specific phrase, not a bare "operator" — "operator-identity
# token" appears only in the detection message, never in the "operator-token scan
# failed to run" error (SEC-W1-02/QA-1: a scan that merely ERRORS must not pass G7).
emit_genetics cyp1a2-rs762551 > "$GN/cyp1a2-rs762551.md"
printf '\nFurther reading: contact the cohort author at not-walter@example.com\n' >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "operator-identity token"; } \
    && ok "genetics operator-token in body FAILs (SEC-ORD-01)" || { bad "G7 expected rc1+detection got $RC"; echo "$OUT"; }

# Case G7b: NAME-class operator token (SEC-W1-02) — write a synthetic name into the
# temp repo's gitignored operator-identity config, inject that name into the body,
# assert FAIL with the operator-identity-token message. Guards the config-driven NAME
# path (the primary "operator-free library" threat) that G7's value-class email does
# NOT cover, and proves the SEC-W1-03 absolute-config fix loads $REPO_ROOT's config.
mkdir -p "$REPO/vault/meta"
printf 'SyntheticOperatorName\n' > "$REPO/vault/meta/operator-identity.txt"
emit_genetics cyp1a2-rs762551 > "$GN/cyp1a2-rs762551.md"
printf '\nCurated by SyntheticOperatorName.\n' >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "operator-identity token"; } \
    && ok "genetics NAME-token in body FAILs (SEC-ORD-01 config-driven name path)" || { bad "G7b expected rc1+detection got $RC"; echo "$OUT"; }
rm -f "$REPO/vault/meta/operator-identity.txt"

# Case G8: raw genotype in a Genotype-Findings trait-token field -> FAIL (SEC-ORD-02)
emit_genetics cyp1a2-rs762551 \
  | sed 's/^- (A;A): fast-caffeine-metabolism/- (A;A): fast-caffeine-metabolism rs762551/' \
  > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -qi "raw genotype"; } \
    && ok "genetics raw-genotype in trait-token FAILs (SEC-ORD-02)" || { bad "G8 expected rc1+raw genotype got $RC"; echo "$OUT"; }

# Case G-grammar: a finding line missing the ' — ' em-dash PASSES the populated check
# but the T2 matcher would silently skip it -> FAIL (Arch-1/QA-2 per-line grammar).
# Non-tautological vs G2: only the em-dash is removed from one otherwise-valid line.
emit_genetics cyp1a2-rs762551 \
  | sed 's/^- (A;A): fast-caffeine-metabolism — clears caffeine quickly, tolerates higher intake \[1\]/- (A;A): fast-caffeine-metabolism clears caffeine quickly, tolerates higher intake [1]/' \
  > "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "grammar"; } \
    && ok "genetics finding line missing em-dash FAILs (per-line grammar)" || { bad "G-grammar expected rc1+grammar got $RC"; echo "$OUT"; }

# Case G9 (SEC1 regression): a value-class operator token AFTER >4096 bytes of benign
# filler must still FAIL the SEC-ORD-01 whole-page scan. The old shell-out used
# scan_text, which TRUNCATES at _MAX_SCAN_TEXT_LEN=4096 (fail-OPEN past the cap on a
# PUBLIC repo); the fix uses scan_text_full (no cap). Filler is plain prose (no '- '
# bullets, no '## ' headings) so it stays inside Genotype Findings without becoming a
# finding line — only the page-spanning SEC-ORD-01 scan sees the trailing token. REDs
# against the old capped scan_text (the token past 4096 is truncated away -> vacuous PASS).
emit_genetics cyp1a2-rs762551 > "$GN/cyp1a2-rs762551.md"
{ printf '\n'
  for i in $(seq 1 90); do
      printf 'Filler reference %02d: benign curated commentary, no PII, no finding-bullet shape, padding the page well beyond the four-thousand-ninety-six byte cap.\n' "$i"
  done
  printf 'Further reading: contact the cohort author at not-walter@example.com\n'
} >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "operator-identity token"; } \
    && ok "genetics operator-token past 4096 bytes FAILs (SEC-ORD-01 scan_text_full)" || { bad "G9 expected rc1+detection got $RC"; echo "$OUT"; }

# Case G10 (BUG1 regression): an INDENTED finding bullet carrying a raw rsID in its
# trait-token must FAIL (SEC-ORD-02). The matcher (_genotype_findings) strips leading
# whitespace then matches '- ', so it parses indented findings the col-0 gate awk never
# collected. Non-tautological vs G2: only one indented finding line is appended. REDs
# against the old /^-[[:space:]]/ col-0 anchor (the indented line is invisible -> PASS).
emit_genetics cyp1a2-rs762551 > "$GN/cyp1a2-rs762551.md"
printf '  - (C;C): rs999bad — indented finding smuggling a raw rsID in the trait token\n' >> "$GN/cyp1a2-rs762551.md"
run "$TMP/bda-pass.sh" vault/library/genetics/cyp1a2-rs762551.md
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -qi "raw genotype"; } \
    && ok "genetics indented finding w/ raw rsID FAILs (SEC-ORD-02 col-tolerant)" || { bad "G10 expected rc1+raw genotype got $RC"; echo "$OUT"; }

# Case G-WIKI (TEST1): vault/WIKI.md carries the library/genetics/ schema section (T1 AC-7) —
# the '### library/genetics/' heading AND the '## Genotype Findings' grammar token. Guards
# the canonical schema doc against either being dropped (it had no committed regression test).
WIKI_MD="$(cd "$SCRIPT_DIR/../.." && pwd)/vault/WIKI.md"
{ grep -q '^### library/genetics/' "$WIKI_MD" && grep -q '## Genotype Findings' "$WIKI_MD"; } \
    && ok "WIKI.md carries the library/genetics schema section (T1 AC-7)" \
    || bad "G-WIKI expected '### library/genetics/' + '## Genotype Findings' in $WIKI_MD"

echo
echo "test_wiki_ingest_lint: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
