#!/usr/bin/env bash
# toolkit/tests/test-rotation-stamp-audit.sh
#
# F-007 obligation: rotation-stamp-audit.sh must PROVE it goes RED on a known-bad
# continuity doc — F-009's whole point is that the audit no project shipped must
# actually FAIL on a stacked VOLATILE section. A clean fixture must PASS.
#
# Cases:
#   GOOD: VOLATILE section holds only the rotation window {n-1,n,n+1,n+2} -> exit 0.
#   BAD : VOLATILE section stacks ancient history (S140, S141, S150) -> exit 1.
#   BAD2 (named false-green, BUG-API-002): a bare stale sha in narrative prose
#         must be caught. If `\b` regex were used, this would false-GREEN.
#   GOOD2: the same sha on a YYYY-MM-DD-stamped / sha256-labelled line is allowed.
#
# NOTE: deliberately NO `set -e`. expect_exit runs commands that are SUPPOSED to
# exit non-zero (the bad fixtures); set -e would abort the harness on the first
# such (correctly failing) audit before the tally is printed.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh disable=SC1091
source "${HERE}/../lib/test-lib.sh"

AUDIT="${HERE}/../scripts/rotation-stamp-audit.sh"
FIX="${HERE}/fixtures/rotation-stamp-audit"
mkdir -p "$FIX"

CUR=172  # current session for all fixtures; window is {S171,S172,S173,S174}

# ---------------------------------------------------------------------------
# GOOD fixture: VOLATILE section references only the window. Clean prose.
# ---------------------------------------------------------------------------
cat > "${FIX}/good.md" <<'EOF'
# HANDOFF

**Current session:** S172

## Current State (VOLATILE)

- **Current session:** S172 — wiring the rotation audit
- **Prior session:** S171 — shipped the helpers lib
- **Next session:** S173 — fold in the meta-audit
- **Two-back session:** S174 — planning the doc rubric

Status unchanged from earlier work; see ranges S160-S171 for backstory.

## History (stable)

Older sessions S140 through S171 are archived below and do not rotate.
EOF

# ---------------------------------------------------------------------------
# BAD fixture: stacked history INSIDE the VOLATILE section. S140/S141/S150 are
# all outside the {S171..S174} window -> must FAIL.
# ---------------------------------------------------------------------------
cat > "${FIX}/bad.md" <<'EOF'
# HANDOFF

**Current session:** S172

## Current State (VOLATILE)

- **Current session:** S172 — wiring the rotation audit
- **Prior session:** S171 — shipped the helpers lib
- **Session 150** — old decision left stacked here
- **Session 141** — even older, never rotated out
- **S140** — ancient, should have moved to History long ago
EOF

# ---------------------------------------------------------------------------
# BAD2 fixture (BUG-API-002 named false-green): a bare git sha in narrative
# prose, no date/hash context. A `\b`-anchored regex would MISS this and
# false-green. Rotation window itself is clean so the ONLY violation is the hash.
# ---------------------------------------------------------------------------
cat > "${FIX}/bad-stale-hash.md" <<'EOF'
# HANDOFF

**Current session:** S172

## Current State (VOLATILE)

- **Current session:** S172 — fine

## Notes

Pinned the build to a1b2c3d4e5 as the last-known-good commit.
EOF

# ---------------------------------------------------------------------------
# GOOD2 fixture: same sha, but on lines that whitelist it (date stamp / sha256
# label). BUG-003a also covered: the pure-decimal id 20260424 is NOT a hash.
# ---------------------------------------------------------------------------
cat > "${FIX}/good-hash-context.md" <<'EOF'
# HANDOFF

**Current session:** S172

## Current State (VOLATILE)

- **Current session:** S172 — fine

## Notes

2026-04-24 pinned the build to a1b2c3d4e5 (last-known-good).
sha256 of artifact: deadbeef1234 verified at build time.
Issue id 20260424 is a ticket number, not a commit hash.
EOF

echo "== rotation window: good PASS / bad (stacked history) FAIL =="
expect_exit 0 bash "$AUDIT" --current "$CUR" "${FIX}/good.md"
expect_exit 1 bash "$AUDIT" --current "$CUR" "${FIX}/bad.md"

echo "== stale-hash false-green (BUG-API-002): bad FAIL / contextualized GOOD PASS =="
expect_exit 1 bash "$AUDIT" --current "$CUR" "${FIX}/bad-stale-hash.md"
expect_exit 0 bash "$AUDIT" --current "$CUR" "${FIX}/good-hash-context.md"

echo "== current session auto-parsed from doc (no --current) =="
expect_exit 0 bash "$AUDIT" "${FIX}/good.md"
expect_exit 1 bash "$AUDIT" "${FIX}/bad.md"

echo "== F-008 fail-closed: missing target is FATAL(2), allow-skip downgrades to PASS =="
expect_exit 2 bash "$AUDIT" --current "$CUR" "${FIX}/does-not-exist.md"
expect_exit 0 bash "$AUDIT" --current "$CUR" --allow-skip "${FIX}/does-not-exist.md"

echo "== FATAL on unresolvable current session / unknown arg =="
printf '# Doc\n\n## State (VOLATILE)\n\n- **Current session:** S5\n' > "${FIX}/no-current-hint.md"
expect_exit 2 bash "$AUDIT" --bogus-flag "${FIX}/good.md"

echo "== guard-fires assertion (F-007 core): good=0, bad!=0 =="
assert_red_when_guard_removed \
  "bash '$AUDIT' --current $CUR '${FIX}/good.md'" \
  "bash '$AUDIT' --current $CUR '${FIX}/bad.md'"

test_summary
