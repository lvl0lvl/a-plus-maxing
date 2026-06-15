#!/usr/bin/env bash
# test-parity-audit.sh — negative test for parity-audit.sh.
#
# F-007 obligation (test-lib.sh): an audit that cannot prove it goes RED on bad
# input does not count as enforcing anything. This test proves parity-audit.sh:
#   1. PASSes (exit 0) on a known-GOOD mini-lib where every catalog record, every
#      reference (references/, roles/<slug>/agent.md, ~/.claude/...), resolves and
#      there are NO dead symlinks and NO orphan reference bundles.
#   2. FAILs (exit 1) on a known-BAD mini-lib carrying the EXACT F-022 cracks:
#        - a SKILL.md referencing references/rubric-methodology.md that is MISSING,
#        - a dead symlink (skills/dead-ui -> does-not-exist),
#        - an orphaned references/ bundle (skills/orphan/references, no SKILL.md),
#        - a catalog record (skill ghost) with no artifact on disk.
#   3. FATALs (exit 2) on bad args (no --lib).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/parity-audit.sh"
FIX="$TEST_DIR/fixtures/parity-audit"
GOOD="$FIX/good"
BAD="$FIX/bad"

# Resolve ~/.claude deploy refs against each fixture's own deploy/ root so the test
# is hermetic (does not depend on the runner's real $HOME/.claude).
GOOD_DEPLOY="$GOOD/deploy"
BAD_DEPLOY="$BAD/deploy"

# F-025: ship ZERO committed dead symlinks. The bad fixture's dead symlink
# (skills/dead-ui) is NOT committed — a dead symlink at rest in the repo breaks
# some checkouts, archivers, and tree-walkers. Create it at RUNTIME and remove it
# on exit, so every BAD-fixture assertion below still sees the crack while the repo
# itself never carries a dead symlink.
ln -s ../skills/does-not-exist "$BAD/skills/dead-ui"
trap 'rm -f "$BAD/skills/dead-ui"' EXIT

# Core contract: green on good, red on bad (the guard actually fires).
assert_red_when_guard_removed \
  "bash '$AUDIT' --lib '$GOOD' --deploy '$GOOD_DEPLOY'" \
  "bash '$AUDIT' --lib '$BAD' --deploy '$BAD_DEPLOY'"

# Explicit exit-code assertions.
expect_exit 0 bash "$AUDIT" --lib "$GOOD" --deploy "$GOOD_DEPLOY"
expect_exit 1 bash "$AUDIT" --lib "$BAD" --deploy "$BAD_DEPLOY"

# F-022 regression: confirm each SPECIFIC crack is the thing caught (not incidental).
out="$(bash "$AUDIT" --lib "$BAD" --deploy "$BAD_DEPLOY" 2>&1 || true)"

check_caught() {
  desc="$1"; pat="$2"
  TESTS_RUN=$((TESTS_RUN + 1))
  if printf '%s' "$out" | grep -q "$pat"; then
    echo "[PASS] F-022 crack caught: $desc"
  else
    echo "[FAIL] F-022 crack NOT caught: $desc (expected /$pat/)"
    printf '%s\n' "$out"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

check_caught "missing reference bundle file"   "rubric-methodology.md"
check_caught "dead symlink"                    "dead symlink"
check_caught "orphaned reference bundle"       "orphaned reference bundle"
check_caught "catalog declares absent skill"   "ghost"

# Bad args -> FATAL (exit 2).
expect_exit 2 bash "$AUDIT"
expect_exit 2 bash "$AUDIT" --lib
expect_exit 2 bash "$AUDIT" --lib /no/such/dir/anywhere
expect_exit 2 bash "$AUDIT" --bogus

# BUG-22e regression (fresh-start dogfood, F-024): a NESTED tests/fixtures/ tree is
# broken ON PURPOSE; a project that VENDORS a toolkit must NOT false-FAIL on it. But
# the exclusion must be SCOPED — the same breakage OUTSIDE fixtures is still caught.
NEST="$(mktemp -d 2>/dev/null || mktemp -d -t parity)"
mkdir -p "$NEST/toolkit/tests/fixtures/parity-audit/bad/skills"
ln -s ../does-not-exist "$NEST/toolkit/tests/fixtures/parity-audit/bad/skills/dead-ui"
expect_exit 0 bash "$AUDIT" --lib "$NEST" --deploy "$NEST"   # nested fixture breakage -> EXEMPT -> PASS
mkdir -p "$NEST/skills"
ln -s ../does-not-exist "$NEST/skills/real-dead"             # same breakage OUTSIDE fixtures
expect_exit 1 bash "$AUDIT" --lib "$NEST" --deploy "$NEST"   # -> still CAUGHT -> FAIL
rm -rf "$NEST"

# BUG-22g regression (anchored-substring immunity, F-007): a `references/<x>` that is the
# TAIL of a longer anchored deploy path (e.g. ~/.claude/skills_library/skills/rubric/
# references/x.md) is NOT a relative bundle ref — it is handled by the ~/.claude resolver
# and must NOT be re-resolved against the referencing file's own references/ dir. Before
# the fix, every anchored reference false-FAILed here. Load-bearing: GOOD (anchored only)
# must PASS; the control (a genuinely broken BARE references/x) must still FAIL.
ANCH="$(mktemp -d 2>/dev/null || mktemp -d -t parity)"
mkdir -p "$ANCH/skills/consumer" "$ANCH/skills/rubric/references"
echo "# methodology" > "$ANCH/skills/rubric/references/rubric-methodology.md"
printf -- '---\nname: rubric\ndescription: x\n---\n# r\n' > "$ANCH/skills/rubric/SKILL.md"
# Consumer references the bundle ONLY via the anchored path (its tail contains references/x).
printf -- '---\nname: consumer\ndescription: x\n---\n# c\nRead `~/.claude/skills_library/skills/rubric/references/rubric-methodology.md`.\n' \
  > "$ANCH/skills/consumer/SKILL.md"
expect_exit 0 bash "$AUDIT" --lib "$ANCH" --deploy "$ANCH"   # anchored substring -> NOT a false relative FAIL
# Control: a genuinely broken BARE relative ref is still caught.
printf -- '\nAlso read `references/does-not-exist.md`.\n' >> "$ANCH/skills/consumer/SKILL.md"
expect_exit 1 bash "$AUDIT" --lib "$ANCH" --deploy "$ANCH"   # genuine bare broken ref -> CAUGHT
rm -rf "$ANCH"

# BUG-22h regression (leading-./ relative ref, F-007): `./references/<x>` is the SAME
# relative ref as `references/<x>` (the file's own bundle dir). The BUG-22g keep-filter
# kept only bare `references/`, which over-suppressed the `./`-prefixed form so a DEAD
# `./references/x` slipped through the audit. Load-bearing: a resolvable `./references/x`
# must PASS (no over-flag); a dead `./references/x` must FAIL (the hole is closed).
DOT="$(mktemp -d 2>/dev/null || mktemp -d -t parity)"
mkdir -p "$DOT/skills/c1/references" "$DOT/skills/c2"
printf -- '---\nname: c1\ndescription: x\n---\n# c1\nSee `./references/exists.md`.\n' > "$DOT/skills/c1/SKILL.md"
echo "# real" > "$DOT/skills/c1/references/exists.md"
expect_exit 0 bash "$AUDIT" --lib "$DOT" --deploy "$DOT"   # resolvable ./references/x -> PASS
printf -- '---\nname: c2\ndescription: x\n---\n# c2\nSee `./references/missing.md`.\n' > "$DOT/skills/c2/SKILL.md"
expect_exit 1 bash "$AUDIT" --lib "$DOT" --deploy "$DOT"   # dead ./references/x -> CAUGHT
rm -rf "$DOT"

test_summary
