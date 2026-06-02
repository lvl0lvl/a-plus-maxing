#!/usr/bin/env bash
# test_branch_completeness_audit.sh — smoke tests for branch-completeness-audit.sh.
#
# Anti-tautological: the ROSTER-GAP case encodes the exact PF-S22-01 failure (an agent on
# the reference branch absent from the checkout) and MUST fail; the COMPLETE case has that
# same agent present so it MUST pass — the two fixtures differ only by that one file.
#
# Cases:
#   1. COMPLETE    checkout has every reference agent + governance → PASS (rc 0)
#   2. ROSTER-GAP  reference has an agent the checkout lacks → FAIL (rc 1)  [the PF-S22-01 case]
#   3. GOV-GAP     checkout lacks bda + the provenance invariant → FAIL (rc 1)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT="$REPO_ROOT/scripts/branch-completeness-audit.sh"

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
OUT="$TMP/out"

REPO="$TMP/repo"; mkdir -p "$REPO"; cd "$REPO"
git init -q
git config user.email t@t.t; git config user.name t
git checkout -q -b base

# base: governance present (bda + invariant) + one foundation agent
mkdir -p scripts .claude/agents/foundation-x
echo '# bda stub' > scripts/audit-research-provenance.sh
printf 'register\n| INV-RESEARCH-PROVENANCE-DISJOINT | ... |\n' > INVARIANTS.md
echo 'foundation' > .claude/agents/foundation-x/agent.md
git add -A; git commit -qm base

# full: base + a specialist agent (the only difference vs base)
git checkout -q -b full
mkdir -p .claude/agents/specialist-y
echo 'specialist' > .claude/agents/specialist-y/agent.md
git add -A; git commit -qm full

# nogov: an agent present but NO bda + INVARIANTS without the invariant
git checkout -q base; git checkout -q -b nogov
rm -f scripts/audit-research-provenance.sh
printf 'register without the registered invariant\n' > INVARIANTS.md
git add -A; git commit -qm nogov

run() { git checkout -q "$1"; bash "$AUDIT" --reference "$2" >"$OUT" 2>&1; RC=$?; }

# Case 1: COMPLETE
run full full
[ "$RC" -eq 0 ] && ok "complete checkout PASSes" || { bad "complete expected rc0, got $RC"; cat "$OUT"; }

# Case 2: ROSTER-GAP (PF-S22-01) — base lacks specialist-y that full has
run base full
if [ "$RC" -eq 1 ] && grep -q "roster gap" "$OUT"; then
    ok "reference agent missing from checkout FAILs (PF-S22-01 roster gap)"
else
    bad "roster-gap expected rc1 + 'roster gap', got rc=$RC"; cat "$OUT"
fi

# Case 3: GOV-GAP — nogov lacks bda + the provenance invariant
run nogov nogov
if [ "$RC" -eq 1 ] && grep -q "governance gap" "$OUT"; then
    ok "missing governance layer FAILs"
else
    bad "gov-gap expected rc1 + 'governance gap', got rc=$RC"; cat "$OUT"
fi

echo
echo "test_branch_completeness_audit: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
