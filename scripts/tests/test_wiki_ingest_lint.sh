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

run() {  # $1 = bda stub ; $2.. = page args (repo-relative). sets RC + OUT
    OUT="$(cd "$REPO" && WIKI_REPO_ROOT="$REPO" WIKI_BDA_CMD="$1" bash "$SCRIPT" "${@:2}" 2>&1)"
    RC=$?
}

CP="$REPO/vault/compounds"; BM="$REPO/vault/biomarkers"; LB="$REPO/vault/library/peptides"

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

echo
echo "test_wiki_ingest_lint: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
