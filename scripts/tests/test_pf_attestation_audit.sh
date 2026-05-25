#!/usr/bin/env bash
# test_pf_attestation_audit.sh — smoke tests for pf-attestation-audit.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/../pf-attestation-audit.sh"
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

# ── T1: affirmative attestation (new PF entry) → pass ────────────────
echo "T1: affirmative attestation passes"
run_case t1_affirmative "$(cat <<'EOF'
# Handoff

## PF attestation
S4 close (2026-05-25): One new PF entry promoted (PF-S3-01). Rationale text here.
EOF
)" 0

# ── T2: negative attestation (no PF this session) → pass ──────────────
echo "T2: negative attestation passes"
run_case t2_negative "$(cat <<'EOF'
# Handoff

## PF attestation
S6 close (2026-06-10): No new PF-class entries this session. Two surprises observed but neither rose to PF level.
EOF
)" 0

# ── T3: no attestation line → fail ────────────────────────────────────
echo "T3: missing attestation flagged"
run_case t3_missing "$(cat <<'EOF'
# Handoff

## Session notes
Things happened but no attestation line written.
EOF
)" 1 "no \`S<N> close"

# ── T4: malformed attestation (missing date) → fail ───────────────────
echo "T4: missing date flagged"
run_case t4_missing_date "$(cat <<'EOF'
# Handoff

## PF attestation
S5 close: No new PF this session.
EOF
)" 1 "no \`S<N> close"

# ── T5: malformed attestation (empty body) → fail ─────────────────────
echo "T5: empty attestation body flagged"
run_case t5_empty_body "$(cat <<'EOF'
# Handoff

S5 close (2026-05-25):
EOF
)" 1 "no \`S<N> close"

# ── T6: multiple attestations → latest validated against --session ────
echo "T6: latest of multiple attestations is current"
run_case t6_multiple "$(cat <<'EOF'
# Handoff

S2 close (2026-05-23): Six PF entries this session.
S3 close (2026-05-24): One PF entry promoted.
S4 close (2026-05-25): No new PF-class entries this session. All clean.
EOF
)" 0

# ── T7: --session N where latest != N → fail ──────────────────────────
echo "T7: --session N where latest != N flagged"
"$AUDIT" "$TMP/t1_affirmative.md" --session 99 2>/dev/null
rc=$?
if [[ $rc -eq 1 ]]; then
    echo "  PASS: session mismatch flagged"
    PASS=$((PASS + 1))
else
    echo "  FAIL: session mismatch rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T8: --session N where latest = N → pass ───────────────────────────
echo "T8: --session N where latest = N passes"
"$AUDIT" "$TMP/t1_affirmative.md" --session 4 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: session match passes"
    PASS=$((PASS + 1))
else
    echo "  FAIL: session match rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T9: --session=N equals-form ───────────────────────────────────────
echo "T9: --session=N equals-form parses"
"$AUDIT" "$TMP/t1_affirmative.md" --session=4 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: equals-form parses"
    PASS=$((PASS + 1))
else
    echo "  FAIL: equals-form rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T10: missing file → exit 2 ────────────────────────────────────────
echo "T10: nonexistent file exits 2"
"$AUDIT" "$TMP/does-not-exist.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: missing file exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: missing file rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T11: real HANDOFF.md → clean ──────────────────────────────────────
echo "T11: project HANDOFF.md has attestation"
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

# ── T12: indented attestation line ────────────────────────────────────
echo "T12: leading-whitespace attestation accepted"
run_case t12_indented "$(cat <<'EOF'
# Handoff

  S5 close (2026-05-25): Attestation text with leading whitespace.
EOF
)" 0

# ── Summary ───────────────────────────────────────────────────────────
echo ""
echo "Total: $((PASS + FAIL))"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
