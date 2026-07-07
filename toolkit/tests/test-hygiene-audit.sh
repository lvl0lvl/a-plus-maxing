#!/usr/bin/env bash
# test-hygiene-audit.sh — F-007 negative test for hygiene-audit.sh (ADR-0004, T4).
#
# F-007 obligation: an audit that cannot prove it FAILs on bad input enforces
# nothing. A count check that trusts the self-reported number, or a close-reason
# check that only confirms `bd close` was called, is a SIGNAL, not the PROPERTY.
# This test pins both sub-checks against good AND known-bad fixtures, and proves
# the audit goes RED — so a sub-check stubbed to always-pass fails the suite.
#
# G4 (count-reconciliation): the PF log carries a self-reported total line
#   ("Total PF entries: N"). The audit must RECOMPUTE N from the actual PF
#   entries and FAIL when the reported number disagrees with the real count.
#     GOOD-G4 : reported total == actual entry count        -> exit 0.
#     BAD-G4  : reported total != actual entry count (off by >=1) -> exit 1.
#
# G6 (close-reason rationale): every CLOSED bead in issues.jsonl must carry a
#   non-empty close_reason. The audit must inspect the FIELD CONTENT and FAIL on
#   an empty/whitespace reason — not merely confirm the record is closed.
#     GOOD-G6 : every closed bead has a substantive close_reason -> exit 0.
#     BAD-G6  : a closed bead with empty/whitespace close_reason -> exit 1.
#
# A fully-good fixture (counts reconcile + every closed bead has a reason) must
# PASS (exit 0). Each known-bad fixture isolates ONE sub-check so a stub that
# always-passes that sub-check leaves its bad fixture green -> RED suite.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/hygiene-audit.sh"
# Fixtures are generated scratch (not committed): write to a throwaway temp dir so
# running the suite never dirties the tracked tree.
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# =============================================================================
# PF-LOG fixtures (G4)
# =============================================================================

# A PF log with 3 real entries (PF-S7-01, PF-S7-02, PF-S8-01) and a self-reported
# total that AGREES (3). Recompute -> 3 == 3 -> reconciles.
cat > "$FIX/pf-good.md" <<'EOF'
# Process Failures

Total PF entries: 3

## Session 7
PF-S7-01: Assumed instead of verified. Root cause: skipped the check.
PF-S7-02: Shipped a fix to a copy. Root cause: no blast-radius pass.

## Session 8
PF-S8-01: Reported a count without recomputing it.
EOF

# Same 3 real entries but the self-reported total LIES (says 5). Recompute -> 3,
# reported 5 -> mismatch -> G4 FAIL. If the audit trusts the reported number this
# stays green (signal, not property) — the F-007 trap.
cat > "$FIX/pf-bad-count.md" <<'EOF'
# Process Failures

Total PF entries: 5

## Session 7
PF-S7-01: Assumed instead of verified. Root cause: skipped the check.
PF-S7-02: Shipped a fix to a copy. Root cause: no blast-radius pass.

## Session 8
PF-S8-01: Reported a count without recomputing it.
EOF

# =============================================================================
# BEAD fixtures (G6) — issues.jsonl shape: closed records carry close_reason,
# open records omit it (ADR-0004 [VERIFIED]).
# =============================================================================

# All closed beads carry a substantive close_reason; an open bead omits it.
cat > "$FIX/beads-good.jsonl" <<'EOF'
{"id":"proj-aaa","title":"do a thing","status":"closed","priority":1,"close_reason":"Shipped via PR #12; verified by run-attest record."}
{"id":"proj-bbb","title":"open thing","status":"open","priority":2}
{"id":"proj-ccc","title":"another","status":"closed","priority":0,"close_reason":"Superseded by proj-aaa — no longer needed."}
EOF

# A closed bead carries an empty/whitespace close_reason -> G6 FAIL. A check that
# only confirms the bead is closed (bd close was called) false-PASSes here.
cat > "$FIX/beads-bad-reason.jsonl" <<'EOF'
{"id":"proj-aaa","title":"do a thing","status":"closed","priority":1,"close_reason":"Shipped via PR #12; verified by run-attest record."}
{"id":"proj-bbb","title":"open thing","status":"open","priority":2}
{"id":"proj-ccc","title":"rationale-free close","status":"closed","priority":0,"close_reason":"   "}
EOF

# =============================================================================
# Assertions
# =============================================================================

# Fully-good: counts reconcile AND every closed bead has a reason -> PASS.
expect_exit 0 bash "$AUDIT" --pf-log "$FIX/pf-good.md" --beads "$FIX/beads-good.jsonl"

# G4 isolated: bad count, good beads -> FAIL(1).
expect_exit 1 bash "$AUDIT" --pf-log "$FIX/pf-bad-count.md" --beads "$FIX/beads-good.jsonl"

# G6 isolated: good count, empty close_reason on a closed bead -> FAIL(1).
expect_exit 1 bash "$AUDIT" --pf-log "$FIX/pf-good.md" --beads "$FIX/beads-bad-reason.jsonl"

# Missing input is an env error -> FATAL(2), never a clean pass (F-008).
expect_exit 2 bash "$AUDIT" --pf-log "$FIX/does-not-exist.md" --beads "$FIX/beads-good.jsonl"

# Guard proof G4: same audit, good vs bad-count, must flip green->red. If the
# count sub-check is stubbed to always-pass, bad-count stays green -> this FAILs.
assert_red_when_guard_removed \
  "bash '$AUDIT' --pf-log '$FIX/pf-good.md' --beads '$FIX/beads-good.jsonl'" \
  "bash '$AUDIT' --pf-log '$FIX/pf-bad-count.md' --beads '$FIX/beads-good.jsonl'"

# Guard proof G6: same audit, good vs empty-reason, must flip green->red. If the
# close-reason sub-check is stubbed to always-pass, bad-reason stays green -> FAILs.
assert_red_when_guard_removed \
  "bash '$AUDIT' --pf-log '$FIX/pf-good.md' --beads '$FIX/beads-good.jsonl'" \
  "bash '$AUDIT' --pf-log '$FIX/pf-good.md' --beads '$FIX/beads-bad-reason.jsonl'"

test_summary
