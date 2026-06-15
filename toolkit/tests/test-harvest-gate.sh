#!/usr/bin/env bash
# tests/test-harvest-gate.sh — negative test for the harvest-gate.sh gate.
#
# F-007 obligation: prove the gate goes RED (non-zero) on bad input. The whole
# point of harvest-gate (Finding F-017, Mechanism 2) is that the self-improvement
# loop only learns from failures captured in ALL THREE layers — PF prose, the
# machine-readable harvest.jsonl ledger, and a tracked bead. So the load-bearing
# negative cases are:
#   - a PF session failure with NO harvest.jsonl record   -> FAIL (exit 1)
#   - a PF session failure with NO referencing bead        -> FAIL (exit 1)
#   - a malformed harvest.jsonl line (unmineable record)   -> FAIL (exit 1)
#
# Cases:
#   GOOD: one failure (FAIL-RIGOR-001) present in PF + harvest.jsonl (schema-valid)
#         + referenced by a bead -> gate exits 0.
#   BAD:  PF logs FAIL-RIGOR-001 AND FAIL-RIGOR-002; only -001 is harvested+beaded;
#         -002 has NO harvest record and NO bead; AND harvest.jsonl carries a
#         malformed (truncated) JSON line -> gate exits 1.
#   BAD2: harvest record present but MISSING a required schema field (detection_mode)
#         -> gate exits 1.
#   BAD3: failure harvested (schema-valid) but NO bead references it -> exit 1.
#   FATAL: a missing --beads input -> exit 2 (a check that cannot run does not pass).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/harvest-gate.sh"
FIX="${TEST_DIR}/fixtures/harvest-gate"

rm -rf "$FIX"
mkdir -p "$FIX/good" "$FIX/bad" "$FIX/bad2" "$FIX/bad3"

# === GOOD ====================================================================
cat > "$FIX/good/process-failures.md" <<'EOF'
# Process Failures

## Session 7
- FAIL-RIGOR-001: gate did not forward --strict to constituent; close attested green falsely.
EOF

cat > "$FIX/good/harvest.jsonl" <<'EOF'
{"id":"FAIL-RIGOR-001","class":"enforcement-gap","source_refs":["memory/process-failures.md:FAIL-RIGOR-001"],"recurrence_count":2,"detection_mode":"mechanical-audit"}
EOF

cat > "$FIX/good/issues.jsonl" <<'EOF'
{"id":"bd-101","title":"forward --strict to constituents","status":"open","refs":["FAIL-RIGOR-001"]}
EOF

# === BAD: a PF failure missing from harvest + bead, and a malformed jsonl line =
cat > "$FIX/bad/process-failures.md" <<'EOF'
# Process Failures

## Session 7
- FAIL-RIGOR-001: gate did not forward --strict; harvested + beaded.
- FAIL-RIGOR-002: heartbeat clause silently dropped; NOT harvested, NOT beaded.
EOF

# -001 is harvested fine; then a malformed (truncated) line; -002 never appears.
cat > "$FIX/bad/harvest.jsonl" <<'EOF'
{"id":"FAIL-RIGOR-001","class":"enforcement-gap","source_refs":["memory/process-failures.md:FAIL-RIGOR-001"],"recurrence_count":2,"detection_mode":"mechanical-audit"}
{"id":"FAIL-RIGOR-003","class":"continuity", "source_refs":[
EOF

cat > "$FIX/bad/issues.jsonl" <<'EOF'
{"id":"bd-101","title":"forward --strict","status":"open","refs":["FAIL-RIGOR-001"]}
EOF

# === BAD2: harvest record missing a required schema field (detection_mode) ====
cat > "$FIX/bad2/process-failures.md" <<'EOF'
# Process Failures

## Session 7
- FAIL-RIGOR-001: harvested but the ledger record is schema-incomplete.
EOF

cat > "$FIX/bad2/harvest.jsonl" <<'EOF'
{"id":"FAIL-RIGOR-001","class":"enforcement-gap","source_refs":["x"],"recurrence_count":2}
EOF

cat > "$FIX/bad2/issues.jsonl" <<'EOF'
{"id":"bd-101","refs":["FAIL-RIGOR-001"]}
EOF

# === BAD3: harvested + schema-valid, but NO bead references it ================
cat > "$FIX/bad3/process-failures.md" <<'EOF'
# Process Failures

## Session 7
- FAIL-RIGOR-001: harvested + schema-valid, but never tracked as a bead.
EOF

cat > "$FIX/bad3/harvest.jsonl" <<'EOF'
{"id":"FAIL-RIGOR-001","class":"enforcement-gap","source_refs":["x"],"recurrence_count":1,"detection_mode":"self"}
EOF

cat > "$FIX/bad3/issues.jsonl" <<'EOF'
{"id":"bd-999","refs":["FAIL-OTHER-005"]}
EOF

# --- assertions --------------------------------------------------------------

# GOOD: failure present in all 3 layers -> PASS (exit 0).
expect_exit 0 bash "$GATE" \
  --pf "$FIX/good/process-failures.md" \
  --harvest "$FIX/good/harvest.jsonl" \
  --beads "$FIX/good/issues.jsonl"

# BAD (load-bearing): a PF failure missing from harvest+bead AND a malformed line -> FAIL (1).
expect_exit 1 bash "$GATE" \
  --pf "$FIX/bad/process-failures.md" \
  --harvest "$FIX/bad/harvest.jsonl" \
  --beads "$FIX/bad/issues.jsonl"

# BAD2: schema-incomplete harvest record -> FAIL (1).
expect_exit 1 bash "$GATE" \
  --pf "$FIX/bad2/process-failures.md" \
  --harvest "$FIX/bad2/harvest.jsonl" \
  --beads "$FIX/bad2/issues.jsonl"

# BAD3: harvested+valid but no bead -> FAIL (1).
expect_exit 1 bash "$GATE" \
  --pf "$FIX/bad3/process-failures.md" \
  --harvest "$FIX/bad3/harvest.jsonl" \
  --beads "$FIX/bad3/issues.jsonl"

# FATAL: a missing input -> exit 2 (a check that cannot run does not pass).
expect_exit 2 bash "$GATE" \
  --pf "$FIX/good/process-failures.md" \
  --harvest "$FIX/good/harvest.jsonl" \
  --beads "$FIX/good/nonexistent.jsonl"

# Bundled guard-fires assertion: good=0, canonical bad (missing layer + malformed)=non-zero.
assert_red_when_guard_removed \
  "bash '$GATE' --pf '$FIX/good/process-failures.md' --harvest '$FIX/good/harvest.jsonl' --beads '$FIX/good/issues.jsonl'" \
  "bash '$GATE' --pf '$FIX/bad/process-failures.md' --harvest '$FIX/bad/harvest.jsonl' --beads '$FIX/bad/issues.jsonl'"

test_summary
