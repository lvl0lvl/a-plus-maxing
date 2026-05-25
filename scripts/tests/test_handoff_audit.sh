#!/usr/bin/env bash
# test_handoff_audit.sh — fixture-driven smoke tests for handoff-audit.sh
#
# Each test writes a temporary HANDOFF.md fixture, invokes the audit, and
# asserts exit code + stderr content.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/../handoff-audit.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

run_case() {
    local label="$1" fixture="$2" expect_rc="$3" expect_needle="${4:-}"
    local path="$TMP/$label.md"
    printf '%s' "$fixture" > "$path"

    local stderr_capture
    stderr_capture=$("$AUDIT" "$path" 2>&1 >/dev/null)
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

# ── T1: empty volatile section, no SHAs anywhere → clean ──────────────
echo "T1: minimal clean fixture exits 0"
run_case t1_clean "$(cat <<'EOF'
---
title: handoff
---

# Handoff

## Current State (volatile)
- No SHAs in this fixture.
- All clean.
EOF
)" 0

# ── T2: literal sha256 reference → INV-HO-NO-STALE-HASH ───────────────
echo "T2: literal sha256 flagged"
run_case t2_sha256_literal "$(cat <<'EOF'
# Handoff

## Notes
The hash was sha256 abc123def456 which we used earlier.
EOF
)" 1 "INV-HO-NO-STALE-HASH"

# ── T3: bare commit SHA, no date → flagged ────────────────────────────
echo "T3: bare commit SHA without date flagged"
run_case t3_bare_sha "$(cat <<'EOF'
# Handoff

## Status
Branch is at commit `8b05b30` currently.
EOF
)" 1 "INV-HO-NO-STALE-HASH"

# ── T4: commit SHA with same-line date → allowed ──────────────────────
echo "T4: commit SHA with same-line date passes"
run_case t4_sha_line_dated "$(cat <<'EOF'
# Handoff

## Status
Branch at commit `8b05b30` as of 2026-05-25.
EOF
)" 0

# ── T5: commit SHA in section with dated header → allowed ─────────────
echo "T5: commit SHA in dated section header passes"
run_case t5_sha_section_dated "$(cat <<'EOF'
# Handoff

## Session 4 close — 2026-05-25
Commit `8b05b30` landed clean.
EOF
)" 0

# ── T6: VOLATILE section with two "Historical" mentions → clause 5 ────
echo "T6: clause 5 (max 1 Historical per VOLATILE section)"
run_case t6_two_historical "$(cat <<'EOF'
# Handoff

## Current State (volatile)
- Active work line.

**Historical (kept for reference):** vault/sessions/session-3.md

Some more Historical context here too.
EOF
)" 1 "INV-HO-ROTATION"

# ── T7: VOLATILE section with malformed Historical pointer → clause 2 ─
echo "T7: clause 2 (Historical pointer missing target)"
run_case t7_bad_historical "$(cat <<'EOF'
# Handoff

## Current State (volatile)
- Stuff.

**Historical (kept for reference):**
EOF
)" 1 "INV-HO-ROTATION"

# ── T8: non-volatile section with multiple "Historical" → allowed ─────
echo "T8: non-volatile section can mention Historical freely"
run_case t8_historical_in_normal_section "$(cat <<'EOF'
# Handoff

## Background
Historical context here.
More Historical notes here.
Yet another Historical reference.
EOF
)" 0

# ── T9: VOLATILE section with single well-formed Historical → clean ───
echo "T9: well-formed single Historical pointer passes"
run_case t9_good_historical "$(cat <<'EOF'
# Handoff

## What Is Next (volatile)
- Future work.

**Historical (kept for reference):** vault/sessions/session-3.md
EOF
)" 0

# ── T10: case-insensitive VOLATILE detection ──────────────────────────
echo "T10: VOLATILE uppercase detected as volatile"
run_case t10_volatile_upper "$(cat <<'EOF'
# Handoff

## Top-3 active failure modes (VOLATILE — rotates each session)

**Historical (kept for reference):** vault/foo.md

Another Historical mention.
EOF
)" 1 "INV-HO-ROTATION"

# ── T11: missing file → exit 2 ────────────────────────────────────────
echo "T11: nonexistent file exits 2"
"$AUDIT" "$TMP/does-not-exist.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: missing file exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: missing file rc expected=2 actual=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T12: real HANDOFF.md → clean (regression guard for project state) ─
echo "T12: project HANDOFF.md is clean"
"$AUDIT" "$SCRIPT_DIR/../../HANDOFF.md" 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: real HANDOFF.md exits 0"
    PASS=$((PASS + 1))
else
    echo "  FAIL: real HANDOFF.md exits $rc"
    "$AUDIT" "$SCRIPT_DIR/../../HANDOFF.md"
    FAIL=$((FAIL + 1))
fi

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL))"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
