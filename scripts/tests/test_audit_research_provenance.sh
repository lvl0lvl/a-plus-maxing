#!/usr/bin/env bash
# test_audit_research_provenance.sh — smoke tests for the bda provenance gate.
#
# Anti-tautological by construction: each fixture is built to exercise a distinct
# branch, and the PASS fixture builds a REAL attestation chain (source file +
# matching sha256) so verify-chain genuinely validates it rather than being stubbed.
#
# Cases:
#   1. NO-GATES        empty design-work → FAIL (the vacuous-pass hole bda closes)
#   2. NO-CHAIN        required gate present but attestation_chain null → FAIL
#   3. COLLATION       mode_floor=none slug → PASS (N/A; no research dispatch)
#   4. FULL-VALID      all required gates present with valid chains → PASS

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT="$REPO_ROOT/scripts/audit-research-provenance.sh"

PASS=0; FAIL=0
ok()   { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

run() { # <workdir> <slug> -> sets RC
    bash "$AUDIT" "$1" "$2" >/dev/null 2>&1; RC=$?
}

sha() { python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# --- Case 1: NO-GATES (gi-specialist = standard/compound) → expect FAIL (rc 1) ---
wd="$TMP/case1/design/.gi-specialist-design-work"; mkdir -p "$wd/gates"
run "$wd" gi-specialist
[ "$RC" -eq 1 ] && ok "no-gates dir FAILs (vacuous-pass hole closed)" || bad "no-gates expected rc1, got $RC"

# --- Case 2: NO-CHAIN (gate present, attestation_chain null) → expect FAIL ---
wd="$TMP/case2/design/.gi-specialist-design-work"; mkdir -p "$wd/gates"
echo '{"verdict":"PASS"}' > "$wd/gates/gate-2.75.json"
for g in 3.5 4.25 4.75 7.5 8.5; do echo '{"verdict":"PASS","attestation_chain":null}' > "$wd/gates/gate-$g.json"; done
run "$wd" gi-specialist
[ "$RC" -eq 1 ] && ok "gates-without-attestation_chain FAIL" || bad "no-chain expected rc1, got $RC"

# --- Case 3: COLLATION (medical-liaison = mode_floor none) → expect PASS (rc 0) ---
wd="$TMP/case3/design/.medical-liaison-design-work"; mkdir -p "$wd/gates"
run "$wd" medical-liaison
[ "$RC" -eq 0 ] && ok "collation-only role is N/A-exempt (PASS)" || bad "collation expected rc0, got $RC"

# --- Case 4: FULL-VALID (personal-trainer = standard/protocol → needs 2.75,3.5,4.25,4.75) ---
wd="$TMP/case4/design/.personal-trainer-design-work"; mkdir -p "$wd/gates" "$wd/judges" "$wd/sections"
# 2.75: presence only
echo '{"verdict":"PASS"}' > "$wd/gates/gate-2.75.json"
# 3.5: judge_sources chain
echo '{"verdict":"PASS","total":95}' > "$wd/judges/judge-A.json"
jsha="$(sha "$wd/judges/judge-A.json")"
cat > "$wd/gates/gate-3.5.json" <<EOF
{"verdict":"PASS","attestation_chain":{"judge_sources":[{"path":"judges/judge-A.json","sha256":"$jsha"}]}}
EOF
# 4.25: agent_source chain
echo '## Verdict: PASS' > "$wd/sections/id-reconcile-source.md"
s425="$(sha "$wd/sections/id-reconcile-source.md")"
cat > "$wd/gates/gate-4.25.json" <<EOF
{"verdict":"PASS","attestation_chain":{"agent_source_path":"sections/id-reconcile-source.md","agent_source_sha256":"$s425"}}
EOF
# 4.75: agent_source chain
echo '## Verdict: PASS' > "$wd/gates/gate-4.75.md"
s475="$(sha "$wd/gates/gate-4.75.md")"
cat > "$wd/gates/gate-4.75.json" <<EOF
{"verdict":"PASS","attestation_chain":{"agent_source_path":"gates/gate-4.75.md","agent_source_sha256":"$s475"}}
EOF
run "$wd" personal-trainer
[ "$RC" -eq 0 ] && ok "full valid chain (standard/protocol) PASSes" || bad "full-valid expected rc0, got $RC"

# --- Case 4b: tamper a source file post-attest → verify-chain must catch (FAIL) ---
echo 'EDITED AFTER ATTEST' >> "$wd/gates/gate-4.75.md"
run "$wd" personal-trainer
[ "$RC" -eq 1 ] && ok "post-attest source edit caught by verify-chain (sha mismatch)" || bad "tamper expected rc1, got $RC"

# --- Case 5: NON-CANONICAL layout (research-gates/ not gates/) → FAIL with accurate msg ---
# Mirrors supplement-specialist's real divergence: gates exist but not where the
# canonical gate_attest.py reads them. Must FAIL, and must say "non-canonical",
# not "missing".
wd="$TMP/case5/design/.gi-specialist-design-work"; mkdir -p "$wd/research-gates"
for g in 2.75 3.5 4.25 4.75 7.5 8.5; do echo '{"verdict":"PASS","attestation_chain":{}}' > "$wd/research-gates/gate-$g.json"; done
out="$(bash "$AUDIT" "$wd" gi-specialist 2>&1)"; RC=$?
if [ "$RC" -eq 1 ] && echo "$out" | grep -q "non-canonical"; then
    ok "non-canonical research-gates/ layout FAILs with accurate diagnostic"
else
    bad "non-canonical layout: expected rc1 + 'non-canonical' msg, got rc=$RC"
fi

echo
echo "test_audit_research_provenance: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
