#!/usr/bin/env bash
# test_skill_trace_audit.sh — smoke tests for skill-trace-audit.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/../skill-trace-audit.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

run_case() {
    local label="$1" session="$2" fixture="$3" expect_rc="$4" expect_needle="${5:-}"
    local path="$TMP/$label.md"
    printf '%s' "$fixture" > "$path"

    local stderr_capture
    stderr_capture=$("$AUDIT" --session "$session" --file "$path" 2>&1 >/dev/null)
    local rc=$?

    local ok=1
    if [[ "$rc" -ne "$expect_rc" ]]; then
        ok=0
        echo "  FAIL: $label — rc expected=$expect_rc actual=$rc"
        echo "    stderr: $stderr_capture"
    fi
    if [[ -n "$expect_needle" && "$stderr_capture" != *"$expect_needle"* ]]; then
        ok=0
        echo "  FAIL: $label — stderr missing: $expect_needle"
        echo "    stderr: $stderr_capture"
    fi
    if [[ $ok -eq 1 ]]; then
        echo "  PASS: $label"
        PASS=$((PASS + 1))
    else
        FAIL=$((FAIL + 1))
    fi
}

# ── T1: good table (all YES) → pass ───────────────────────────────────
echo "T1: good table passes"
run_case t1_good 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES (Skill tool) | YES (Skill tool; merge-methodology.md read fresh) |
| #97 | YES | YES |

## Session 52 (2026-06-13)
EOF
)" 0

# ── T2: attestation present but no table → fail ───────────────────────
echo "T2: missing table flagged"
run_case t2_no_table 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

Reviews and merges ran but no table was written.
EOF
)" 1 "no per-PR invocation table"

# ── T3: NO cell without violation marker → fail ───────────────────────
echo "T3: NO without violation marker flagged"
run_case t3_bare_no 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES | YES |
| #100 | YES | **NO — same** |
EOF
)" 1 '/merge cell starts with NO but lacks the word "violation"'

# ── T4: NO cell WITH violation marker → pass ──────────────────────────
echo "T4: NO with violation marker passes"
run_case t4_no_with_marker 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES | YES |
| #100 | YES | **NO — substance run from in-session context (violation, recorded above)** |
EOF
)" 0

# ── T5: zero-row table without the no-lifecycle sentence → fail ───────
echo "T5: empty table without escape hatch flagged"
run_case t5_zero_rows 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
EOF
)" 1 "no data rows"

# ── T6: no-lifecycle sentence without a table → pass ──────────────────
echo "T6: escape-hatch sentence without table passes"
run_case t6_escape_hatch 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

No PR lifecycles ran this session. Governance-only work.
EOF
)" 0

# ── T7: attestation in section is for a different session → fail ──────
echo "T7: wrong-session attestation flagged"
run_case t7_wrong_session 8 "$(cat <<'EOF'
## Session 8 (2026-06-12)

S7 close (2026-06-12): No new PF-class entries this session.

No PR lifecycles ran this session.
EOF
)" 1 "is for S7, not S8"

# ── T8: no Session-N section at all → fail ────────────────────────────
echo "T8: missing session section flagged"
run_case t8_no_section 99 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

No PR lifecycles ran this session.
EOF
)" 1 'no `## Session 99` section'

# ── T9: canonical line-form attestation accepted ──────────────────────
echo "T9: line-form attestation accepted"
run_case t9_line_form 50 "$(cat <<'EOF'
## Session 50 (2026-06-11)

S50 close (2026-06-11): **No new PF-class entries this session.** Rationale.

No PR lifecycles ran this session.
EOF
)" 0

# ── T10: cell starting with neither YES nor NO → fail ─────────────────
echo "T10: neither-YES-nor-NO cell flagged"
run_case t10_neither 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | pending | YES |
EOF
)" 1 "neither YES nor NO"

# ── T11: table is scoped to the session section ───────────────────────
# A valid table in Session 50 must NOT satisfy Session 51's requirement.
echo "T11: table in another session's section does not count"
run_case t11_scoping 51 "$(cat <<'EOF'
## Session 50 (2026-06-11)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #94 | YES | YES |

## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

Reviews ran but the table was written under the wrong session.
EOF
)" 1 "no per-PR invocation table"

# ── T12: missing --session → exit 2 ───────────────────────────────────
echo "T12: missing --session exits 2"
printf '%s' "irrelevant" > "$TMP/t12.md"
"$AUDIT" --file "$TMP/t12.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: missing --session exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: missing --session rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T13: non-integer --session → exit 2 (no vacuous pass) ─────────────
echo "T13: non-integer --session exits 2"
"$AUDIT" --session abc --file "$TMP/t12.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: non-integer --session exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: non-integer --session rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T14: missing file → exit 2 ────────────────────────────────────────
echo "T14: nonexistent file exits 2"
"$AUDIT" --session 51 --file "$TMP/does-not-exist.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: missing file exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: missing file rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T15: quoted hatch sentence mid-prose does not waive the table ─────
# RED-proven: pre-fix (substring hatch test) this exited 0.
echo "T15: quoted escape-hatch sentence mid-prose does not count"
run_case t15_quoted_hatch 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

The close plan said to write "No PR lifecycles ran this session." if zero PRs ran, but six lifecycles ran and no table was written.
EOF
)" 1 "no per-PR invocation table"

# ── T16: table inside a code fence is not a real table ────────────────
# RED-proven: pre-fix (no fence stripping) this exited 0.
echo "T16: fenced example table does not satisfy the table check"
run_case t16_fenced_table 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

An example of the mandated shape (no real table follows):

```
| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES | YES |
```
EOF
)" 1 "no per-PR invocation table"

# ── T17: escaped pipe inside a YES cell stays one cell → pass ─────────
# RED-proven: pre-fix (split on every pipe) this exited 1 with a spurious
# neither-YES-nor-NO finding on the split-off fragment.
echo "T17: escaped pipe in a YES cell passes"
run_case t17_escaped_pipe 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES (Skill tool \| ref) | YES |
EOF
)" 0

# ── T18: invalid UTF-8 crashes the analyzer → exit 2, never 0 ─────────
# Kills the crash-exit-0 mutant (exit 2 → exit 0 in the analyzer-failed
# branch).
echo "T18: analyzer crash on invalid UTF-8 exits 2"
printf '## Session 51\n\xff\xfe\n' > "$TMP/t18.md"
stderr_capture=$("$AUDIT" --session 51 --file "$TMP/t18.md" 2>&1 >/dev/null)
rc=$?
if [[ $rc -eq 2 && "$stderr_capture" == *"analyzer failed"* ]]; then
    echo "  PASS: analyzer crash exit code + message"
    PASS=$((PASS + 1))
else
    echo "  FAIL: analyzer crash rc=$rc (expected 2 + 'analyzer failed')"
    echo "    stderr: $stderr_capture"
    FAIL=$((FAIL + 1))
fi

# ── T19: escape hatch present, but a present table is still validated ──
# Kills the if-no_lifecycle-skip-rows mutant (hatch sentence waiving the
# per-cell validation of a table that IS present).
echo "T19: hatch sentence does not waive row validation of a present table"
run_case t19_composite 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

No PR lifecycles ran this session.

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES | **NO — same** |
EOF
)" 1 'lacks the word "violation"'

# ── T20: --session=N / --file=PATH equals forms parse ─────────────────
# Kills the equals-form-parse mutant (broken --session=* branch).
echo "T20: equals-form arguments accepted"
cat > "$TMP/t20.md" <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | YES | YES |
EOF
"$AUDIT" --session=51 --file="$TMP/t20.md" 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: equals-form exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: equals-form rc=$rc (expected 0)"
    FAIL=$((FAIL + 1))
fi

# ── T21: bare NO in the REVIEW column is attributed to /review-pr ─────
# Kills the column-swap mutant (review/merge skill labels exchanged);
# pairs with T3's /merge-attributed needle.
echo "T21: bare NO in review column attributed to /review-pr"
run_case t21_review_attribution 51 "$(cat <<'EOF'
## Session 51 (2026-06-11 → 12)

### S51 close attestation (2026-06-12)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh |
|---|---|---|
| #96 | **NO — same** | YES |
EOF
)" 1 '/review-pr cell starts with NO but lacks the word "violation"'

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL))"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
