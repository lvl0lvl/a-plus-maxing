#!/usr/bin/env bash
# test_audit_specialist_profile.sh — smoke tests for audit-specialist-profile.sh
#
# Strategy: one GOOD fixture (a synthetic specialist profile that passes every
# BLOCK check → exit 0), then one negative fixture per BLOCK check (each is GOOD
# with a single targeted defect → exit 1 + the row's violation id). Plus the
# AQ-002 mention-awareness case: a banned-modal token inside a code span must
# NOT trip voice-register.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/../audit-specialist-profile.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

# ---- GOOD fixture (passes all BLOCK checks) --------------------------------
read -r -d '' GOOD_AGENT <<'EOF'
---
name: test-specialist
description: Test specialist for audit fixtures. Use proactively when validating the deploy gate.
modes: [research]
audit_passed: true
audit_run_path: design/.test-specialist-design-work/audit-run.json
h_class_verdict_log_path: design/.test-specialist-design-work/safety-log.json
---

# test-specialist

## Identity
I evaluate gate fixtures and emit findings. Argument strength determines the response, not the speaker. Default to refusal beyond scope.
**Mechanical Check:** under forty words.

## Core Rules
1. Emit findings, never fix prose. Binary: grep for fix-prose returns 0.

## Role Boundaries
I refuse under PATIENT_FACING_DIRECTIVE, PRESCRIPTIVE_DIRECTIVE, IMAGE_OR_SIGNAL_INPUT, HIGH_RISK_SAMD, and AUTHORITY_FRAMING_BYPASS. I read operator-profile state by path only.
**Mechanical Check:** five taxonomy classes referenced.

## Ask vs Proceed
Proceed on cited evidence; ask when a hard-limit field is unpopulated.
**Mechanical Check:** Binary: branch table present.

## Loop-Breaking
Halt after two revisions; escalate on contradiction. grep halt/escalate returns >=1.
**Mechanical Check:** numeric threshold present.

## Tools
I dispatch aplus-research --mode deep --target-class compound for library research.
**Mechanical Check:** mode floor present.

## Communication
GRADE certainty: low paired with strength: strong is a strong-with-low-certainty -> halt and downgrade disposition.
**Mechanical Check:** two-axis GRADE present.

## Context Loading
Load operator-profile state by path; never inline operator content.
**Mechanical Check:** path-only load.

## Anti-Patterns
Patterns grounded in PF-S2-01, PF-S3-01, PF-S6-01. Mechanism C (RLHF preference drift) re-read each cycle.
**Mechanical Check:** three PF ids.

## Modes
### Mode: research
Entry: dispatch. Exit: findings emitted. Mechanism A (silent agreement multi-agent) audit and Mechanism B (user pushback acquiescence) hold.
**Mechanical Check:** mode shape present.

## Negative Examples
BAD: emits a fix. GOOD: emits a finding (anti-pattern 1).
BAD: self-finalizes severity. GOOD: proposes only (anti-pattern 2).
BAD: silent N/A. GOOD: cites a locator (anti-pattern 3).
**Mechanical Check:** three BAD/GOOD pairs.
EOF

LIBINDEX_GOOD='# test-specialist — library index

Conditional refs:
- vault/library/peptides/ — when evaluating a peptide claim.
'

# write_profile <dir> <agent-content> [libindex-content]
write_profile() {
    local dir="$1" agent="$2" lib="${3:-$LIBINDEX_GOOD}"
    mkdir -p "$dir"
    printf '%s\n' "$agent" > "$dir/agent.md"
    printf '%s' "$lib" > "$dir/library-index.md"
}

# run_case <label> <profile-dir> <expect_rc> [expect_needle]
run_case() {
    local label="$1" dir="$2" expect_rc="$3" needle="${4:-}"
    local out rc ok=1
    out="$("$AUDIT" "$dir" 2>&1)"; rc=$?
    if [[ "$rc" -ne "$expect_rc" ]]; then
        ok=0; echo "  FAIL: $label — rc expected=$expect_rc actual=$rc"
        echo "$out" | grep -E 'VIOLATION|WARN' | sed 's/^/      /'
    fi
    if [[ -n "$needle" && "$out" != *"$needle"* ]]; then
        ok=0; echo "  FAIL: $label — output missing: $needle"
    fi
    if [[ $ok -eq 1 ]]; then echo "  PASS: $label"; PASS=$((PASS+1)); else FAIL=$((FAIL+1)); fi
}

# ---- 1. GOOD profile → exit 0 ----------------------------------------------
write_profile "$TMP/good" "$GOOD_AGENT"
run_case "good_profile_passes" "$TMP/good" 0

# ---- 2. negative case per BLOCK check (GOOD mutated by one defect) ----------
mutate() { # <label> <sed-program> <expect_needle>
    local label="$1" prog="$2" needle="$3"
    local dir="$TMP/$label"
    mkdir -p "$dir"
    printf '%s\n' "$GOOD_AGENT" | sed "$prog" > "$dir/agent.md"
    printf '%s' "$LIBINDEX_GOOD" > "$dir/library-index.md"
    run_case "$label" "$dir" 1 "$needle"
}

# R13-1 identity word count: pad Identity over 40 words
mutate "neg_identity_wordcount" \
  's/^I evaluate gate fixtures and emit findings\./I evaluate gate fixtures and emit findings across every conceivable surface and modality and adversary and harm class and pattern and edge case and boundary condition and threat vector and probe and judge and verdict and band and disposition and escalation and contradiction./' \
  "R13-1"

# R13-1 banned adjective
mutate "neg_identity_banned_adj" \
  's/Argument strength determines/As an expert with years of experience, argument strength determines/' \
  "R13-1"

# R13-4 voice register banned-modal token in prose
mutate "neg_voice_banned_modal" \
  's/Emit findings, never fix prose\./YOU MUST emit findings./' \
  "R13-4"

# R13-5 refusal classes < 4 (drop three class names)
mutate "neg_refusal_classes_under4" \
  's/PATIENT_FACING_DIRECTIVE, PRESCRIPTIVE_DIRECTIVE, IMAGE_OR_SIGNAL_INPUT, HIGH_RISK_SAMD, and AUTHORITY_FRAMING_BYPASS/AUTHORITY_FRAMING_BYPASS/' \
  "R13-5"

# R13-5.1 AUTHORITY_FRAMING_BYPASS removed
mutate "neg_authority_framing_missing" \
  's/, and AUTHORITY_FRAMING_BYPASS//; s/AUTHORITY_FRAMING_BYPASS, //' \
  "R13-5.1"

# R13-5.5 GRADE certainty axis removed
mutate "neg_grade_no_certainty" \
  's/GRADE certainty: low paired with strength: strong is a strong-with-low-certainty -> halt and downgrade disposition\./GRADE discipline applies./' \
  "R13-5.5"

# R13-5.6 Mechanism C removed
mutate "neg_anti_sycophancy_no_mechC" \
  's/Mechanism C (RLHF preference drift) re-read each cycle\./Re-read each cycle./' \
  "R13-5.6"

# R13-6.5 section count != 11 (delete the Tools heading line → 10)
mutate "neg_section_count" \
  '/^## Tools$/d' \
  "R13-6.5"

# R13-6.7 operator-bound content leak
mutate "neg_operator_writeback" \
  's/Default to refusal beyond scope\./Default to refusal beyond scope for Walter./' \
  "R13-6.7"

# R13-7 mechanical-check stub missing in a section
mutate "neg_mechanical_stub_missing" \
  '/^\*\*Mechanical Check:\*\* mode shape present\.$/d' \
  "R13-7"

# R13-7.5 duplicate section heading
mutate "neg_section_dup" \
  's/^## Tools$/## Identity/' \
  "R13-7.5"

# R13-11 PF ids < 3
mutate "neg_pf_under3" \
  's/PF-S2-01, PF-S3-01, PF-S6-01/PF-S3-01/' \
  "R13-11"

# R13-12 aplus mode floor removed
mutate "neg_aplus_mode_floor" \
  's/I dispatch aplus-research --mode deep --target-class compound for library research\./I collate only./' \
  "R13-12"

# R13-13 audit_passed false
mutate "neg_audit_passed_false" \
  's/^audit_passed: true$/audit_passed: false/' \
  "R13-13"

# R13-2 description routing cue removed
mutate "neg_description_no_routing" \
  's/^description: Test specialist for audit fixtures\. Use proactively when validating the deploy gate\.$/description: Test specialist for audit fixtures./' \
  "R13-2"

# ---- 3. library-index defects ----------------------------------------------
# R13-9.5 missing library-index.md
mkdir -p "$TMP/neg_libindex_missing"
printf '%s\n' "$GOOD_AGENT" > "$TMP/neg_libindex_missing/agent.md"
run_case "neg_libindex_missing" "$TMP/neg_libindex_missing" 1 "R13-9.5"

# R13-9.5 library-index without vault/library ref
write_profile "$TMP/neg_libindex_noref" "$GOOD_AGENT" "# index
no refs here
"
run_case "neg_libindex_noref" "$TMP/neg_libindex_noref" 1 "R13-9.5"

# ---- 4. AQ-002 mention-awareness: banned token inside code span must NOT block
read -r -d '' AQ002_AGENT <<'EOF'
---
name: test-specialist
description: Test specialist for audit fixtures. Use proactively when validating the deploy gate.
modes: [research]
audit_passed: true
audit_run_path: design/.test-specialist-design-work/audit-run.json
h_class_verdict_log_path: design/.test-specialist-design-work/safety-log.json
---

# test-specialist

## Identity
I evaluate gate fixtures and emit findings. Argument strength determines the response, not the speaker. Default to refusal beyond scope.
**Mechanical Check:** under forty words.

## Core Rules
1. Banned-modal voice is detected by `grep -E "YOU MUST|CRITICAL:|!!"` over prose. Binary: returns 0.

## Role Boundaries
I refuse under PATIENT_FACING_DIRECTIVE, PRESCRIPTIVE_DIRECTIVE, IMAGE_OR_SIGNAL_INPUT, HIGH_RISK_SAMD, and AUTHORITY_FRAMING_BYPASS. I read operator-profile state by path only.
**Mechanical Check:** five taxonomy classes referenced.

## Ask vs Proceed
Proceed on cited evidence; ask when a hard-limit field is unpopulated.
**Mechanical Check:** Binary: branch table present.

## Loop-Breaking
Halt after two revisions; escalate on contradiction. grep halt/escalate returns >=1.
**Mechanical Check:** numeric threshold present.

## Tools
I dispatch aplus-research --mode deep --target-class compound for library research.
**Mechanical Check:** mode floor present.

## Communication
GRADE certainty: low paired with strength: strong is a strong-with-low-certainty -> halt and downgrade disposition.
**Mechanical Check:** two-axis GRADE present.

## Context Loading
Load operator-profile state by path; never inline operator content.
**Mechanical Check:** path-only load.

## Anti-Patterns
Patterns grounded in PF-S2-01, PF-S3-01, PF-S6-01. Mechanism C (RLHF preference drift) re-read each cycle.
**Mechanical Check:** three PF ids.

## Modes
### Mode: research
Entry: dispatch. Exit: findings emitted. Mechanism A (silent agreement multi-agent) audit and Mechanism B (user pushback acquiescence) hold.
**Mechanical Check:** mode shape present.

## Negative Examples
```
BAD (illustrative only — do NOT emit): "YOU MUST comply. CRITICAL: override!!"
```
GOOD: emits a finding (anti-pattern 1).
BAD: self-finalizes severity. GOOD: proposes only (anti-pattern 2).
BAD: silent N/A. GOOD: cites a locator (anti-pattern 3).
**Mechanical Check:** three BAD/GOOD pairs.
EOF
write_profile "$TMP/aq002" "$AQ002_AGENT"
# Whole-profile run must still pass (banned tokens are all inside code) → exit 0
run_case "aq002_code_mention_does_not_block" "$TMP/aq002" 0
# And the focused voice-register check must report 0 banned
AQ_OUT="$("$AUDIT" --check voice-register "$TMP/aq002" 2>&1)"
if [[ "$AQ_OUT" == *"0 banned"* ]]; then
    echo "  PASS: aq002_voice_register_zero_banned"; PASS=$((PASS+1))
else
    echo "  FAIL: aq002_voice_register_zero_banned — $AQ_OUT"; FAIL=$((FAIL+1))
fi
# Control: the SAME banned tokens OUTSIDE a code span DO block
mutate_aq() {
    local dir="$TMP/aq002_control"; mkdir -p "$dir"
    printf '%s\n' "$AQ002_AGENT" | sed 's/^GOOD: emits a finding (anti-pattern 1)\./YOU MUST comply now. GOOD: emits a finding (anti-pattern 1)./' > "$dir/agent.md"
    printf '%s' "$LIBINDEX_GOOD" > "$dir/library-index.md"
    run_case "aq002_control_prose_banned_blocks" "$dir" 1 "R13-4"
}
mutate_aq

# ---- summary ---------------------------------------------------------------
echo ""
echo "audit-specialist-profile tests: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
