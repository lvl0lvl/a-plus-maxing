#!/usr/bin/env bash
# test-pf-attestation-audit.sh — negative test for pf-attestation-audit.sh.
#
# F-007 obligation: an audit that cannot prove it FAILs on bad input enforces
# nothing. This test pins:
#   GOOD-affirmative : a close with a NEW PF entry attestation -> exit 0.
#   GOOD-negative    : a "no new PF" close WITH observed-but-not-promoted
#                      rationale -> exit 0.
#   BAD-silence      : a PF log with NO attestation line at all -> non-zero.
#   BAD-bare-negative: the CDM-8-5 / BUG-1 false-green — a bare "No new PF-class
#                      entries this session." with no rationale -> non-zero.
#   BAD-session-stale: latest attestation is an older session than --session N.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/pf-attestation-audit.sh"
# Fixtures are generated scratch (not committed): write to a throwaway temp dir so
# running the suite never dirties the tracked tree (skill_consolidator-oas).
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# --- GOOD: affirmative (a new PF entry was promoted this session) -------------
cat > "$FIX/good-affirmative.md" <<'EOF'
# Process Failures

## Session 7
PF-S7-01: Did the thing wrong. Root cause: assumed instead of verified.

S7 close (2026-06-12): One new PF entry promoted (PF-S7-01). No additional
PF-class incidents observed during the S7 work.
EOF

# --- GOOD: negative WITH observed-but-not-promoted rationale (CDM-8-5) ---------
cat > "$FIX/good-negative.md" <<'EOF'
# Process Failures

S6 close (2026-06-10): No new PF-class entries this session. Two surprises were
observed but neither rose to PF level: a flaky test (env, not process) and a slow
review turnaround (capacity, not a repeatable failure mode).
EOF

# --- GOOD: canonical markdown-HEADER attestation (BUG-PA1) --------------------
cat > "$FIX/good-md-header.md" <<'EOF'
# Process Failures

## S7 close (2026-06-14): No new PF-class entries this session. Observed but not
promoted: a one-off third-party timeout (not a repeatable process failure).
EOF

# --- BAD: silence — no attestation line at all (core negative case) ------------
cat > "$FIX/bad-silence.md" <<'EOF'
# Process Failures

## Session 7
Some notes about the session. Nothing here matches the close-attestation form,
so this close attested nothing. Silence is not absence.
EOF

# --- BAD: bare negative — CDM-8-5 / BUG-1 false-green --------------------------
cat > "$FIX/bad-bare-negative.md" <<'EOF'
# Process Failures

S6 close (2026-06-10): No new PF-class entries this session.
EOF

# --- BAD: stale session — latest attestation is older than required N ----------
cat > "$FIX/bad-stale-session.md" <<'EOF'
# Process Failures

S5 close (2026-06-09): One new PF entry promoted (PF-S5-01). Nothing else of
PF level observed.
EOF

# --- Assertions ---------------------------------------------------------------

# Affirmative good close passes.
expect_exit 0 bash "$AUDIT" "$FIX/good-affirmative.md"

# Negative good close (with rationale) passes.
expect_exit 0 bash "$AUDIT" "$FIX/good-negative.md"

# Core negative: silence must FAIL (exit 1).
expect_exit 1 bash "$AUDIT" "$FIX/bad-silence.md"

# CDM-8-5 / BUG-1: bare negative attestation must FAIL (exit 1).
expect_exit 1 bash "$AUDIT" "$FIX/bad-bare-negative.md"

# Stale session: latest is S5 but we require S6 -> FAIL (exit 1).
expect_exit 1 bash "$AUDIT" --session 6 "$FIX/bad-stale-session.md"

# Missing PF log is an env error -> FATAL (exit 2), never a clean pass (F-008).
expect_exit 2 bash "$AUDIT" "$FIX/does-not-exist.md"

# The headline guard proof: same audit, good vs bad, must flip green->red.
assert_red_when_guard_removed \
  "bash '$AUDIT' '$FIX/good-negative.md'" \
  "bash '$AUDIT' '$FIX/bad-bare-negative.md'"

# BUG-PA1 regression (fresh-start Session-C, F-026): the canonical attestation line is
# a markdown H2 header ('## S<N> close (date): ...'); the audit must accept it.
expect_exit 0 bash "$AUDIT" "$FIX/good-md-header.md"

# BUG-PA1 part-2 (dv2.7): exercise the EXTRACTION path under --session N. The
# fixture's header is '## S7 close ...'; the session number must extract to 7
# THROUGH the markdown prefix. With the part-2 bug the prefix isn't stripped, the
# number mis-parses, and --session 7 FAILs — so this assertion is the load-bearing
# guard the original (no-flag) markdown test lacked.
expect_exit 0 bash "$AUDIT" --session 7 "$FIX/good-md-header.md"

test_summary
