#!/usr/bin/env bash
# toolkit/tests/test-falsification-scan.sh
#
# Negative test for scripts/falsification-scan.sh (CDM-8-10 / extract §3).
#
# F-007 obligation: an audit that cannot prove it goes RED on bad input does not
# count. The scanner's everyday mode is advisory (WARN, exit 0), so we drive it in
# --strict mode for the assertions — strict promotes the increment-by-default WARN
# to a real violation (exit 1), giving the harness a non-zero exit to assert.
#
# Contract case under test (verbatim from the spec): a note exhibiting "every clean
# run advances n" MUST be flagged. The bad fixture contains that exact phrase.

set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/../lib/test-lib.sh"

SCAN="$DIR/../scripts/falsification-scan.sh"
FIX="$DIR/fixtures/falsification-scan"
GOOD="$FIX/good-evidence-close.md"
BAD="$FIX/bad-increment-by-default.md"

# 1. Core guard proof: strict mode PASSes (0) on the good note and FAILs (!=0) on
#    the bad note that exhibits "every clean run advances n".
assert_red_when_guard_removed \
  "bash '$SCAN' --strict '$GOOD'" \
  "bash '$SCAN' --strict '$BAD'"

# 2. Advisory (default) mode: even the bad note exits 0 — WARNs are non-gating by
#    design. This pins the advisory-not-FAIL contract so a future change to a hard
#    FAIL would break a test on purpose.
expect_exit 0 bash "$SCAN" "$BAD"

# 3. Good note is clean in strict mode too (no false positive).
expect_exit 0 bash "$SCAN" --strict "$GOOD"

# 4. Bad note in strict mode is RED (the increment-by-default contract case).
expect_exit 1 bash "$SCAN" --strict "$BAD"

# 5. stdin path works and is flagged in strict mode.
expect_exit 1 bash -c "printf '%s\n' 'every clean run advances n' | bash '$SCAN' --strict"

# 6. F-008 fail-closed: no input at all -> FATAL (exit 2), unless --allow-skip.
expect_exit 2 bash -c "bash '$SCAN' --strict < /dev/null"
expect_exit 0 bash -c "bash '$SCAN' --strict --allow-skip < /dev/null"

# 7. Unreadable note -> FATAL (exit 2).
expect_exit 2 bash "$SCAN" /nonexistent/path/to/note.md

test_summary
