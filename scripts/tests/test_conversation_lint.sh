#!/usr/bin/env bash
# test_conversation_lint.sh — non-tautological smoke tests for conversation-lint.sh.
#
# Each check has a PASS fixture and a FAIL fixture differing by exactly the thing under test, so a
# removed check makes the FAIL case stop failing.
#
# Cases:
#   1  valid conversation file                       -> PASS (exit 0)
#   2  missing a required field (participant)         -> FAIL (exit 1)
#   3  wrong type (type: note)                        -> FAIL (exit 1)
#   4  non-integer turns                              -> FAIL (exit 1)
#   5  invalid created date                           -> FAIL (exit 1)
#   6  empty conversation dir                         -> PASS (nothing to lint)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$SCRIPT_DIR/../conversation-lint.sh"
PASSED=0
FAILED=0

_check() {
    # _check <expected-exit> <case-name> <dir>
    local expected="$1" name="$2" dir="$3" actual=0
    "$LINT" "$dir" >/dev/null 2>&1 || actual=$?
    if [[ "$actual" -eq "$expected" ]]; then
        PASSED=$((PASSED + 1))
    else
        FAILED=$((FAILED + 1))
        echo "FAIL: $name — expected exit $expected, got $actual" >&2
    fi
}

_valid() {
    cat <<'EOF'
---
title: Care Assistant conversation
type: conversation
participant: care
created: 2026-07-02
updated: 2026-07-02
turns: 2
status: active
tags: [conversation, care-agent]
---

# Care Assistant conversation

## 2026-07-02T18:30:00+00:00 — You
It's my age.

## 2026-07-02T18:30:05+00:00 — Assistant
Got it — you're 55.
EOF
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 1 — valid -> PASS
d="$TMP/c1"; mkdir -p "$d"; _valid >"$d/care.md"; _check 0 "valid conversation" "$d"

# 2 — missing participant -> FAIL
d="$TMP/c2"; mkdir -p "$d"; _valid | grep -v '^participant:' >"$d/care.md"; _check 1 "missing participant" "$d"

# 3 — wrong type -> FAIL
d="$TMP/c3"; mkdir -p "$d"; _valid | sed 's/^type: conversation/type: note/' >"$d/care.md"; _check 1 "wrong type" "$d"

# 4 — non-integer turns -> FAIL
d="$TMP/c4"; mkdir -p "$d"; _valid | sed 's/^turns: 2/turns: lots/' >"$d/care.md"; _check 1 "non-integer turns" "$d"

# 5 — invalid created date -> FAIL
d="$TMP/c5"; mkdir -p "$d"; _valid | sed 's/^created: 2026-07-02/created: notadate/' >"$d/care.md"; _check 1 "invalid created date" "$d"

# 6 — empty dir -> PASS
d="$TMP/c6"; mkdir -p "$d"; _check 0 "empty conversation dir" "$d"

echo "test_conversation_lint: ${PASSED} passed, ${FAILED} failed" >&2
[[ "$FAILED" -eq 0 ]]
