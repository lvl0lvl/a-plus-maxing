#!/usr/bin/env bash
# test_scope_contract_audit.sh — smoke tests for scope-contract-audit.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/../scope-contract-audit.sh"
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

# Full well-formed contract template used by tests.
GOOD_CONTRACT=$(cat <<'EOF'
# Handoff

## Scope Contract — Session 5 (2026-05-25)

Goal: build the audit scripts.

Acceptance criteria:
- [ ] script A exists
- [x] script B exists

Files I WILL touch:
- scripts/foo.sh

Files I will NOT touch:
- vault/*

NOT doing:
- specialist roles

Invariants at risk:
- INV-HO-ROTATION
EOF
)

# ── T1: well-formed contract → pass ──────────────────────────────────
echo "T1: well-formed contract passes"
run_case t1_good "$GOOD_CONTRACT" 0

# ── T2: missing Goal field ────────────────────────────────────────────
echo "T2: missing Goal field flagged"
run_case t2_no_goal "$(cat <<'EOF'
## Scope Contract — Session 5

Acceptance criteria:
- [ ] thing

Files I WILL touch: x
Files I will NOT touch: y
NOT doing: z
Invariants at risk: none
EOF
)" 1 "missing required field: Goal"

# ── T3: missing Acceptance criteria ───────────────────────────────────
echo "T3: missing Acceptance criteria flagged"
run_case t3_no_acs "$(cat <<'EOF'
## Scope Contract — Session 5

Goal: stuff.
Files I WILL touch: x
Files I will NOT touch: y
NOT doing: z
Invariants at risk: none
EOF
)" 1 "missing required field: Acceptance criteria"

# ── T4: no binary checkbox AC ─────────────────────────────────────────
echo "T4: missing binary AC checkbox flagged"
run_case t4_no_checkbox "$(cat <<'EOF'
## Scope Contract — Session 5

Goal: stuff.
Acceptance criteria:
- Just a regular bullet, no checkbox.

Files I WILL touch: x
Files I will NOT touch: y
NOT doing: z
Invariants at risk: none
EOF
)" 1 "no binary AC checkbox"

# ── T5: no contract section at all ────────────────────────────────────
echo "T5: no contract section flagged"
run_case t5_no_contract "$(cat <<'EOF'
# Handoff

## Some other section
Nothing about contracts here.
EOF
)" 1 "no \`## Scope Contract"

# ── T6: multiple contracts → latest validated ─────────────────────────
echo "T6: latest of multiple contracts is validated"
run_case t6_multiple_contracts "$(cat <<'EOF'
## Scope Contract — Session 3
(malformed, missing fields)

## Scope Contract — Session 4
(also malformed)

## Scope Contract — Session 5

Goal: x.
Acceptance criteria:
- [ ] thing

Files I WILL touch: x
Files I will NOT touch: y
NOT doing: z
Invariants at risk: none
EOF
)" 0

# ── T7: en-dash variant in header ─────────────────────────────────────
echo "T7: header with hyphen variant"
run_case t7_hyphen "$(cat <<'EOF'
## Scope Contract - Session 5

Goal: x.
Acceptance criteria:
- [ ] thing

Files I WILL touch: x
Files I will NOT touch: y
NOT doing: z
Invariants at risk: none
EOF
)" 0

# ── T8: --session flag enforcement (latest below required) ────────────
echo "T8: --session N where latest < N flagged"
"$AUDIT" "$TMP/t1_good.md" --session 99 2>/dev/null
rc=$?
if [[ $rc -eq 1 ]]; then
    echo "  PASS: latest < required flagged"
    PASS=$((PASS + 1))
else
    echo "  FAIL: latest < required rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T9: --session flag where latest >= required ───────────────────────
echo "T9: --session N where latest >= N passes"
"$AUDIT" "$TMP/t1_good.md" --session 5 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: latest >= required passes"
    PASS=$((PASS + 1))
else
    echo "  FAIL: latest >= required rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T10: --session=N equals-form ──────────────────────────────────────
echo "T10: --session=N equals-form parses"
"$AUDIT" "$TMP/t1_good.md" --session=5 2>/dev/null
rc=$?
if [[ $rc -eq 0 ]]; then
    echo "  PASS: equals-form parses"
    PASS=$((PASS + 1))
else
    echo "  FAIL: equals-form rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T11: missing file → exit 2 ────────────────────────────────────────
echo "T11: nonexistent file exits 2"
"$AUDIT" "$TMP/does-not-exist.md" 2>/dev/null
rc=$?
if [[ $rc -eq 2 ]]; then
    echo "  PASS: missing file exit code"
    PASS=$((PASS + 1))
else
    echo "  FAIL: missing file rc=$rc"
    FAIL=$((FAIL + 1))
fi

# ── T12: real HANDOFF.md → clean ──────────────────────────────────────
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
