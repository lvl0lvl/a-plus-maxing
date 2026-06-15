#!/usr/bin/env bash
# test-pf-ingest.sh — negative test for pf-ingest.sh (the F-018 learning wire).
#
# F-007 obligation: an artifact that cannot prove it rejects bad input enforces
# nothing. pf-ingest is a TRANSFORM, not a pass/fail audit, so its negative test
# pins the transform contract instead of a verdict:
#   GOOD  : a well-formed PF entry -> exit 0, emits a schema-valid JSONL record
#           (ledger.fail.v1) AND a NON-EMPTY "I don't ..." anti-pattern stub.
#   BAD-garbage : non-PF garbage (no Pattern/Anti-pattern/Lesson) -> exit 2,
#                 emits NOTHING to stdout. (BUG-1 fail-closed.)
#   BAD-empty   : empty input -> exit 2.
# The headline guard proof: same transform, good vs bad, must flip 0 -> non-zero.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

INGEST="$TEST_DIR/../scripts/pf-ingest.sh"
FIX="$TEST_DIR/fixtures/pf-ingest"
mkdir -p "$FIX"

# --- GOOD: a well-formed PF entry (framework PF template) ---------------------
cat > "$FIX/good-pf-entry.md" <<'EOF'
## PF-S7-03 (2026-06-12): Shipped an audit with no negative test

**Pattern:** Added a presence-check audit to the toolkit and marked the bead
done without a test that proves it goes RED on bad input.

**Root cause:** No pre-merge mechanical gate requiring a paired negative test for
every shipped audit.

**Detection mode:** user catch — the operator noticed the missing test in review.

**surfaced_by:** user

**Lesson:** Ship every audit with its negative test before it counts as enforcing.

**Anti-pattern to avoid:** Trusting that a green audit means the property holds
when the audit was never shown to fail on a violation.

**Recurrence:** First documented; recurrence_count = 1.
EOF

# --- BAD: garbage — no recognizable PF fields (BUG-1 unparseable) --------------
cat > "$FIX/bad-garbage.md" <<'EOF'
lorem ipsum dolor sit amet
just some notes
nothing structured here at all
EOF

# --- BAD: empty input ---------------------------------------------------------
: > "$FIX/bad-empty.md"

# --- Assertions ---------------------------------------------------------------

# Good entry transforms successfully (exit 0).
expect_exit 0 bash "$INGEST" --pf-entry "$FIX/good-pf-entry.md" --target-artifact "rigor-auditor"

# Garbage is unparseable -> FATAL (exit 2), fail-closed (BUG-1).
expect_exit 2 bash "$INGEST" --pf-entry "$FIX/bad-garbage.md"

# Empty input -> FATAL (exit 2).
expect_exit 2 bash "$INGEST" --pf-entry "$FIX/bad-empty.md"

# Missing file -> FATAL (exit 2), never a silent empty success (F-008).
expect_exit 2 bash "$INGEST" --pf-entry "$FIX/does-not-exist.md"

# stdin path works too (good entry via stdin -> exit 0).
expect_exit 0 sh -c "bash '$INGEST' < '$FIX/good-pf-entry.md'"

# Content checks on GOOD output: schema-valid JSONL + non-empty inverse stub.
out="$(bash "$INGEST" --pf-entry "$FIX/good-pf-entry.md" --target-artifact "rigor-auditor" 2>/dev/null)"

TESTS_RUN=$((TESTS_RUN + 1))
jsonl="$(printf '%s\n' "$out" | sed -n '1p')"
if printf '%s' "$jsonl" | grep -q '"schema":"ledger.fail.v1"' \
   && printf '%s' "$jsonl" | grep -q '"pf_id":"PF-S7-03"' \
   && printf '%s' "$jsonl" | grep -q '"record_type":"pf_harvest"'; then
  echo "[PASS] good output line 1 is schema-valid JSONL (ledger.fail.v1, pf_id captured)"
else
  echo "[FAIL] good output line 1 is not schema-valid JSONL: $jsonl"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

TESTS_RUN=$((TESTS_RUN + 1))
if printf '%s\n' "$out" | grep -q -- "I don't "; then
  echo "[PASS] good output contains a non-empty \"I don't ...\" anti-pattern stub"
else
  echo "[FAIL] good output missing the inverse-rule anti-pattern stub"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# BAD output must be EMPTY on stdout (fail-closed emits nothing).
TESTS_RUN=$((TESTS_RUN + 1))
bad_out="$(bash "$INGEST" --pf-entry "$FIX/bad-garbage.md" 2>/dev/null || true)"
if [ -z "$bad_out" ]; then
  echo "[PASS] garbage input emits nothing to stdout (no noise into the ledger)"
else
  echo "[FAIL] garbage input emitted stdout (should be empty): $bad_out"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# The headline guard proof: good transforms (exit 0), garbage is caught (!=0).
assert_red_when_guard_removed \
  "bash '$INGEST' --pf-entry '$FIX/good-pf-entry.md'" \
  "bash '$INGEST' --pf-entry '$FIX/bad-garbage.md'"

test_summary
