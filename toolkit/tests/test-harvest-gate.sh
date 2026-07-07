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
#
# CF-1 regression cases (cross-deployment finding; the vacuous-pass / false-green):
#   VACUOUS:  a date-form PF id (PF-2026-06-04-03, no "Session N" headings) with NO
#             harvest/bead, under the DEFAULT id pattern, must FATAL (exit 2) — the
#             gate cannot honestly gate this scheme and must NOT read as clean.
#   DATE_OK:  same date-form PF, HARVEST_PF_ID_PATTERN set to a date alternation, id
#             in all 3 layers -> PASS (0); id missing from a layer -> FAIL (1).
#   EMPTY:    a genuinely empty session (no id-shaped tokens) -> PASS (0) "nothing
#             to gate" (backward compat — NOT every empty-id block is a skip).
#   RECUR:    a captured this-session id (all 3 layers) PLUS a prose
#             `Recurrence: PF-S6-01` prior reference -> PASS (0); the prior id must
#             NOT be demanded in harvest/bead.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/harvest-gate.sh"

# Build all fixtures in a throwaway temp dir (cleaned on exit) so the repo tree
# stays clean after a run — the heredocs below are the single source of truth for
# these fixtures, so nothing needs to be tracked under tests/fixtures/ (bead mtz).
FIX="$(mktemp -d "${TMPDIR:-/tmp}/harvest-gate-fix.XXXXXX")"
trap 'rm -rf "$FIX"' EXIT
mkdir -p "$FIX/good" "$FIX/bad" "$FIX/bad2" "$FIX/bad3" \
         "$FIX/vacuous" "$FIX/date_ok" "$FIX/date_missbead" "$FIX/empty" "$FIX/recur" \
         "$FIX/titleword_bad" "$FIX/titleword_good" "$FIX/priorword_bad"

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

# === CF-1 (a) VACUOUS: date-form PF id, default pattern, nothing harvested =====
# No "Session N" heading (date-keyed log); id PF-2026-06-04-03 is failure-id-shaped
# (PF- hyphen prefix) but the DEFAULT pattern can't match it. The gate must NOT take
# the silent "nothing to gate" PASS — it must be loud and fail-closed (FATAL exit 2).
cat > "$FIX/vacuous/process-failures.md" <<'EOF'
# Process Failures (date-keyed)

## 2026-06-04
- PF-2026-06-04-03: gate forwarded no --strict; close attested green falsely.
EOF
printf '' > "$FIX/vacuous/harvest.jsonl"
cat > "$FIX/vacuous/issues.jsonl" <<'EOF'
{"id":"bd-1","refs":[]}
EOF

# === CF-1 (b) DATE_OK: same date-form PF, configurable pattern, all 3 layers ====
cat > "$FIX/date_ok/process-failures.md" <<'EOF'
# Process Failures (date-keyed)

## 2026-06-04
- PF-2026-06-04-03: gate forwarded no --strict.
EOF
cat > "$FIX/date_ok/harvest.jsonl" <<'EOF'
{"id":"PF-2026-06-04-03","class":"enforcement-gap","source_refs":["x"],"recurrence_count":1,"detection_mode":"self"}
EOF
cat > "$FIX/date_ok/issues.jsonl" <<'EOF'
{"id":"bd-7","refs":["PF-2026-06-04-03"]}
EOF

# === CF-1 (b') DATE_MISSBEAD: same date-form PF harvested but NO bead -> FAIL ====
cat > "$FIX/date_missbead/process-failures.md" <<'EOF'
# Process Failures (date-keyed)

## 2026-06-04
- PF-2026-06-04-03: gate forwarded no --strict.
EOF
cat > "$FIX/date_missbead/harvest.jsonl" <<'EOF'
{"id":"PF-2026-06-04-03","class":"enforcement-gap","source_refs":["x"],"recurrence_count":1,"detection_mode":"self"}
EOF
cat > "$FIX/date_missbead/issues.jsonl" <<'EOF'
{"id":"bd-7","refs":["FAIL-OTHER-001"]}
EOF

# === CF-1 (c) EMPTY: genuinely no failure-id-shaped tokens -> PASS "nothing" =====
cat > "$FIX/empty/process-failures.md" <<'EOF'
# Process Failures

## Session 11
No new process failures this session. Clean close.
EOF
printf '' > "$FIX/empty/harvest.jsonl"
cat > "$FIX/empty/issues.jsonl" <<'EOF'
{"id":"bd-1","refs":[]}
EOF

# === CF-1 (d) RECUR: this-session id (all 3 layers) + prose prior reference ======
# PF-S9-01 is the this-session declaration (must be gated, present everywhere).
# PF-S6-01 appears ONLY on a `Recurrence:` line — it must NOT be demanded.
cat > "$FIX/recur/process-failures.md" <<'EOF'
# Process Failures

## Session 9
- PF-S9-01: scope drift; this-session failure, harvested + beaded.
  Recurrence: PF-S6-01 (prior occurrence, already HELD)
EOF
cat > "$FIX/recur/harvest.jsonl" <<'EOF'
{"id":"PF-S9-01","class":"scope-drift","source_refs":["x"],"recurrence_count":2,"detection_mode":"self"}
EOF
cat > "$FIX/recur/issues.jsonl" <<'EOF'
{"id":"bd-9","refs":["PF-S9-01"]}
EOF

# === BUG-6 TITLEWORD: a this-session PF whose TITLE contains a reference keyword ==
# The false-PASS regression (safety PF-S11-01): PF-S11-01 is a genuine this-session
# declaration whose heading mentions "recurrence". It is NOT harvested / NOT beaded,
# so the gate MUST FAIL. The old anywhere-in-line REF_RE dropped this line and PASSed.
cat > "$FIX/titleword_bad/process-failures.md" <<'EOF'
# Process Failures

## Session 11
## PF-S11-01 (2026-07-01): harvest-gate recurrence-filter false-PASS
The prior/superseded reference filter silently dropped this declaration. NOT harvested, NOT beaded.
EOF
printf '' > "$FIX/titleword_bad/harvest.jsonl"
cat > "$FIX/titleword_bad/issues.jsonl" <<'EOF'
{"id":"bd-1","refs":["FAIL-OTHER-001"]}
EOF

# TITLEWORD_GOOD: same declaration (title says "recurrence"), captured in all 3
# layers -> PASS. Proves the title keyword does not wrongly EXCLUDE it either way.
cat > "$FIX/titleword_good/process-failures.md" <<'EOF'
# Process Failures

## Session 11
## PF-S11-01 (2026-07-01): harvest-gate recurrence-filter false-PASS
This-session failure, captured everywhere.
EOF
cat > "$FIX/titleword_good/harvest.jsonl" <<'EOF'
{"id":"PF-S11-01","class":"false-green","source_refs":["x"],"recurrence_count":3,"detection_mode":"red-team"}
EOF
cat > "$FIX/titleword_good/issues.jsonl" <<'EOF'
{"id":"bd-11","refs":["PF-S11-01"]}
EOF

# === BUG-6 review (W1-9) PRIORWORD: a declaration LEADING with a word that merely
# has a reference keyword as a PREFIX ("Priority") must NOT be misread as a reference.
# The trailing word-boundary in REF_RE is what stops "Priority" prefix-matching "Prior";
# without it, this uncaptured id false-PASSed the fail-closed gate.
cat > "$FIX/priorword_bad/process-failures.md" <<'EOF'
# Process Failures

## Session 9
- Priority: 1 — PF-S9-99 (2026-07-02): a real this-session failure. NOT harvested, NOT beaded.
EOF
printf '' > "$FIX/priorword_bad/harvest.jsonl"
cat > "$FIX/priorword_bad/issues.jsonl" <<'EOF'
{"id":"bd-1","refs":["FAIL-OTHER-001"]}
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

# === CF-1 regression assertions ==============================================
DATE_PAT='(FAIL-[A-Z0-9]+-[0-9]+|PF-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]+)'

# (a) LOAD-BEARING: date-form id under DEFAULT pattern, nothing harvested -> the
# vacuous pass is DEAD: gate must FATAL (exit 2), NOT silently PASS (exit 0).
expect_exit 2 bash "$GATE" \
  --pf "$FIX/vacuous/process-failures.md" \
  --harvest "$FIX/vacuous/harvest.jsonl" \
  --beads "$FIX/vacuous/issues.jsonl"

# (a') the FATAL must be LOUD: name the unmatched token AND point at the env
# override (audit-helpers emit() writes to stdout, so capture combined output).
assert_output_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qE "$pattern"; then
    echo "[PASS] output matches /$pattern/"
  else
    echo "[FAIL] output lacked /$pattern/: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}
assert_output_contains "PF-2026-06-04-03" bash "$GATE" \
  --pf "$FIX/vacuous/process-failures.md" \
  --harvest "$FIX/vacuous/harvest.jsonl" \
  --beads "$FIX/vacuous/issues.jsonl"
assert_output_contains "HARVEST_PF_ID_PATTERN" bash "$GATE" \
  --pf "$FIX/vacuous/process-failures.md" \
  --harvest "$FIX/vacuous/harvest.jsonl" \
  --beads "$FIX/vacuous/issues.jsonl"

# (b) configurable pattern + all 3 layers present -> PASS (exit 0).
expect_exit 0 env HARVEST_PF_ID_PATTERN="$DATE_PAT" bash "$GATE" \
  --pf "$FIX/date_ok/process-failures.md" \
  --harvest "$FIX/date_ok/harvest.jsonl" \
  --beads "$FIX/date_ok/issues.jsonl"

# (b') configurable pattern but the bead layer is missing the id -> FAIL (exit 1).
expect_exit 1 env HARVEST_PF_ID_PATTERN="$DATE_PAT" bash "$GATE" \
  --pf "$FIX/date_missbead/process-failures.md" \
  --harvest "$FIX/date_missbead/harvest.jsonl" \
  --beads "$FIX/date_missbead/issues.jsonl"

# (c) genuinely empty session (no id-shaped tokens) -> PASS "nothing to gate" (0).
expect_exit 0 bash "$GATE" \
  --pf "$FIX/empty/process-failures.md" \
  --harvest "$FIX/empty/harvest.jsonl" \
  --beads "$FIX/empty/issues.jsonl"

# (d) this-session id gated, prose prior `Recurrence:` reference NOT demanded -> PASS.
expect_exit 0 bash "$GATE" \
  --pf "$FIX/recur/process-failures.md" \
  --harvest "$FIX/recur/harvest.jsonl" \
  --beads "$FIX/recur/issues.jsonl"

# BUG-6 (W1-5) the FALSE-PASS is DEAD: a this-session PF whose TITLE says "recurrence",
# missing from harvest+bead, MUST FAIL (1) — not be silently dropped and PASSed.
expect_exit 1 bash "$GATE" \
  --pf "$FIX/titleword_bad/process-failures.md" \
  --harvest "$FIX/titleword_bad/harvest.jsonl" \
  --beads "$FIX/titleword_bad/issues.jsonl"

# The same declaration captured in all 3 layers -> PASS (0): the title keyword neither
# wrongly excludes (false-PASS) nor is demanded when it IS present.
expect_exit 0 bash "$GATE" \
  --pf "$FIX/titleword_good/process-failures.md" \
  --harvest "$FIX/titleword_good/harvest.jsonl" \
  --beads "$FIX/titleword_good/issues.jsonl"

# Guard-fires pairing for the fix: captured title-keyword PF GREEN, uncaptured one RED.
assert_red_when_guard_removed \
  "bash '$GATE' --pf '$FIX/titleword_good/process-failures.md' --harvest '$FIX/titleword_good/harvest.jsonl' --beads '$FIX/titleword_good/issues.jsonl'" \
  "bash '$GATE' --pf '$FIX/titleword_bad/process-failures.md' --harvest '$FIX/titleword_bad/harvest.jsonl' --beads '$FIX/titleword_bad/issues.jsonl'"

# BUG-6 review (W1-9): a "Priority:"-leading declaration with an uncaptured id MUST FAIL
# (the trailing-boundary fix; without it "Priority" prefix-matched "Prior" -> false-PASS).
expect_exit 1 bash "$GATE" \
  --pf "$FIX/priorword_bad/process-failures.md" \
  --harvest "$FIX/priorword_bad/harvest.jsonl" \
  --beads "$FIX/priorword_bad/issues.jsonl"

test_summary
