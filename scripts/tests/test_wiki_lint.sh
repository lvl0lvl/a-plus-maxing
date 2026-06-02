#!/usr/bin/env bash
# test_wiki_lint.sh — non-tautological smoke tests for wiki-lint.sh (periodic lint).
#
# The two VIOLATION-class checks (dead-namespace link, open contradiction) get
# pass/fail pairs that differ only by the tested attribute. The info-class checks
# (orphan/stale/confidence/coverage/forward-ref) are asserted to EMIT without
# changing the exit code (advisory, not blocking).
#
# Cases:
#   1 clean vault                                   -> exit 0
#   2 dead-namespace link [[compoundz/x]]           -> exit 1 + "dead link"
#   3 forward-ref [[biomarkers/notyet]] (ns exists) -> exit 0 + "forward-ref" (non-tautological vs 2)
#   4 open contradiction (Status: open, unfenced)   -> exit 1 + "unresolved"
#   5 template-only "Status: open" (fenced)         -> exit 0 (fence excluded; non-tautological vs 4)
#   6 orphan page                                   -> exit 0 + "orphan"
#   7 stale page (monthly cadence, old date)        -> exit 0 + "stale"
#   8 confidence provisional                        -> exit 0 + "provisional"
#   9 coverage gap (active compound, no biomarker)  -> exit 0 + "coverage gap"

set -uo pipefail
PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$(cd "$SCRIPT_DIR/.." && pwd)/wiki-lint.sh"

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"

build_clean() {
    rm -rf "$REPO"
    mkdir -p "$REPO/vault/compounds" "$REPO/vault/biomarkers" "$REPO/vault/meta"
    # a compound that links to an existing biomarker -> all links resolve
    cat > "$REPO/vault/compounds/a.md" <<'EOF'
---
title: A
type: compound
status: researching
last_verified: 2026-06-02
---
# A
## Relations
- [[biomarkers/b]]
EOF
    cat > "$REPO/vault/biomarkers/b.md" <<'EOF'
---
title: B
type: biomarker
confidence: established
last_verified: 2026-06-02
review_cadence: manual
---
# B
## Affected By
- [[compounds/a]]
EOF
    # contradictions with a fenced template (the "Status: open" trap) + no real open
    cat > "$REPO/vault/meta/contradictions.md" <<'EOF'
# Active Contradictions
## Template
```
### YYYY-MM-DD — short title
- **Status:** open | resolved (YYYY-MM-DD)
```
## Open
_(none)_
## Resolved
### 2026-05-24 — something
- **Status:** resolved 2026-05-24
EOF
}

run() { OUT="$(WIKI_REPO_ROOT="$REPO" bash "$SCRIPT" 2>&1)"; RC=$?; }

# Case 1: clean -> exit 0
build_clean; run
[ "$RC" -eq 0 ] && ok "clean vault exits 0" || { bad "case1 expected 0 got $RC"; echo "$OUT"; }

# Case 2: dead-namespace link -> exit 1
build_clean
cat > "$REPO/vault/compounds/typo.md" <<'EOF'
---
title: Typo
type: compound
---
# Typo
- [[compoundz/does-not-exist]]
EOF
run
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "dead link"; } \
    && ok "dead-namespace link is a VIOLATION (exit 1)" || { bad "case2 expected 1+dead link got $RC"; echo "$OUT"; }

# Case 3: forward-ref to existing namespace -> exit 0 (non-tautological vs case 2)
build_clean
cat > "$REPO/vault/compounds/fwd.md" <<'EOF'
---
title: Fwd
type: compound
---
# Fwd
- [[biomarkers/notyet-authored]]
EOF
run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "forward-ref"; } \
    && ok "forward-ref to existing namespace is advisory (exit 0)" || { bad "case3 expected 0+forward-ref got $RC"; echo "$OUT"; }

# Case 4: real open contradiction -> exit 1
build_clean
cat >> "$REPO/vault/meta/contradictions.md" <<'EOF'
### 2026-06-02 — live disagreement
- **Status:** open
EOF
run
{ [ "$RC" -eq 1 ] && echo "$OUT" | grep -q "unresolved"; } \
    && ok "open contradiction is a VIOLATION (exit 1)" || { bad "case4 expected 1+unresolved got $RC"; echo "$OUT"; }

# Case 5: only the fenced template has "Status: open" -> exit 0 (non-tautological vs case 4)
build_clean; run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "0 open contradictions"; } \
    && ok "fenced template 'Status: open' is excluded (exit 0)" || { bad "case5 expected 0 got $RC"; echo "$OUT"; }

# Case 6: orphan -> info, exit 0
build_clean
cat > "$REPO/vault/compounds/lonely.md" <<'EOF'
---
title: Lonely
type: compound
---
# Lonely
EOF
run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "lonely.md: orphan"; } \
    && ok "orphan page emits advisory, exit 0" || { bad "case6 expected 0+orphan got $RC"; echo "$OUT"; }

# Case 7: stale -> info, exit 0
build_clean
cat > "$REPO/vault/biomarkers/old.md" <<'EOF'
---
title: Old
type: biomarker
last_verified: 2020-01-01
review_cadence: monthly
---
# Old
- [[compounds/a]]
EOF
run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "old.md: stale"; } \
    && ok "stale page emits advisory, exit 0" || { bad "case7 expected 0+stale got $RC"; echo "$OUT"; }

# Case 8: provisional -> info, exit 0
build_clean
cat > "$REPO/vault/biomarkers/prov.md" <<'EOF'
---
title: Prov
type: biomarker
confidence: provisional
last_verified: 2026-06-02
review_cadence: manual
---
# Prov
- [[compounds/a]]
EOF
run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "prov.md: confidence provisional"; } \
    && ok "provisional page emits advisory, exit 0" || { bad "case8 expected 0+provisional got $RC"; echo "$OUT"; }

# Case 9: coverage gap -> info, exit 0
build_clean
cat > "$REPO/vault/compounds/active.md" <<'EOF'
---
title: Active
type: compound
status: active
last_verified: 2026-06-02
---
# Active
## Relations
- [[compounds/a]]
EOF
run
{ [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "active.md: coverage gap"; } \
    && ok "active compound w/o biomarker emits coverage advisory, exit 0" || { bad "case9 expected 0+coverage got $RC"; echo "$OUT"; }

echo
echo "test_wiki_lint: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
