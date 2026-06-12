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
)" 1 'lacks the word "violation"'

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

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL))"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
