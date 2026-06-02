#!/usr/bin/env bash
# test_block_ungated_vault_write.sh — smoke tests for block-ungated-vault-write.sh.
#
# Fully isolated: BLOCK_UNGATED_VAULT_PROJECT_ROOT points the hook at a temp git
# repo, WIKI_BDA_CMD stubs the provenance gate. The hook runs the REAL
# scripts/wiki-ingest-lint.sh, so these tests exercise the gate end-to-end through
# the hook. Non-tautological: case 2 (valid page) and case 3 (same page minus
# provenance) differ only by provenance and yield allow vs deny.
#
# Cases:
#   1 non-commit command (git status)                 -> allow (no deny)
#   2 commit staging a VALID gated page                -> allow
#   3 commit staging an INVALID page (no provenance)   -> DENY
#   4 commit staging only non-vault files              -> allow
#   5 commit staging a grandfathered page (no prov)    -> allow
#   6 commit staging a non-gated vault file (_template)-> allow

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$SCRIPT_DIR/../block-ungated-vault-write.sh"

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO/vault/compounds" "$REPO/vault/meta" "$REPO/vault/library" "$REPO/design/.test-design-work"
cd "$REPO"
git init -q; git config user.email t@t.t; git config user.name t; git checkout -q -b feat

printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/bda.sh"; chmod +x "$TMP/bda.sh"

cat > "$REPO/vault/meta/index.md" <<'IDX'
# Index
- [[compounds/test-compound]]
- [[compounds/ungated]]
- [[compounds/grandfathered]]
IDX
printf '# gf\nvault/compounds/grandfathered.md\n' > "$REPO/vault/library/_ingest-grandfather.txt"

emit() {  # $1 slug ; valid low-risk compound
    cat <<EOF
---
title: T
type: compound
permalink: a-plus-maxing/compounds/$1
class: supplement
evidence_tier: B
risk_tier: low
status: researching
created: 2026-06-02
last_verified: 2026-06-02
provenance_dir: design/.test-design-work
provenance_slug: test-compound
---

# T
## Metadata
- class: supplement
## Mechanism
x
## Evidence Summary
- [A 2024] — n=1, RCT
## Protocol
- dose: 1
## Risk Profile
- contraindications: none known
## Trial Status
- stopping criteria: n/a
## Relations
- [[compounds/$1]]
EOF
}

emit test-compound > "$REPO/vault/compounds/test-compound.md"
emit ungated | grep -v '^provenance_' > "$REPO/vault/compounds/ungated.md"
emit grandfathered | grep -v '^provenance_' > "$REPO/vault/compounds/grandfathered.md"
emit x > "$REPO/vault/compounds/_template.md"
echo "root readme" > "$REPO/README.md"

invoke() {  # $1 = command string ; echoes hook stdout
    printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_UNGATED_VAULT_PROJECT_ROOT="$REPO" WIKI_BDA_CMD="$TMP/bda.sh" bash "$HOOK"
}

# Case 1: non-commit command
git reset -q
OUT=$(invoke "git status")
[[ "$OUT" != *'"deny"'* ]] && ok "non-commit command allowed" || { bad "case1 unexpected deny: $OUT"; }

# Case 2: valid gated page staged -> allow
git reset -q; git add vault/compounds/test-compound.md
OUT=$(invoke "git commit -m 'add compound'")
[[ "$OUT" != *'"deny"'* ]] && ok "commit of valid gated page allowed" || { bad "case2 unexpected deny: $OUT"; }

# Case 3: invalid page (no provenance) staged -> DENY  (non-tautological vs case 2)
git reset -q; git add vault/compounds/ungated.md
OUT=$(invoke "git commit -m 'add ungated'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"INV-WIKI-INGESTION-GATED"* ]]; } \
    && ok "commit of ungated page DENIED" || { bad "case3 expected deny, got: $OUT"; }

# Case 4: only non-vault files staged -> allow
git reset -q; git add README.md
OUT=$(invoke "git commit -m 'docs'")
[[ "$OUT" != *'"deny"'* ]] && ok "commit of non-vault files allowed" || { bad "case4 unexpected deny: $OUT"; }

# Case 5: grandfathered page (no provenance, allowlisted) -> allow
git reset -q; git add vault/compounds/grandfathered.md
OUT=$(invoke "git commit -m 'edit grandfathered'")
[[ "$OUT" != *'"deny"'* ]] && ok "commit of grandfathered page allowed" || { bad "case5 unexpected deny: $OUT"; }

# Case 6: non-gated vault file (_template) only -> allow (gate skips it)
git reset -q; git add vault/compounds/_template.md
OUT=$(invoke "git commit -m 'template'")
[[ "$OUT" != *'"deny"'* ]] && ok "commit of non-gated _template allowed" || { bad "case6 unexpected deny: $OUT"; }

echo
echo "test_block_ungated_vault_write: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
