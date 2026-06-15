#!/usr/bin/env bash
# run-all-tests.sh — run every toolkit negative test.
#
# The F-007 obligation: an audit/hook that cannot prove it FAILs on bad input
# does not count as enforcing. This runner executes each component's negative
# test (good fixture -> allow/PASS, bad fixture -> block/FAIL, and the test
# itself goes RED if the guard is broken). CI and `close-audit.sh` call this.
#
# Exit 0 if all pass, 1 if any fail.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
pass=0; fail=0; failed=""
for t in "$HERE"/test-*.sh; do
    [ -f "$t" ] || continue
    if bash "$t" >/dev/null 2>&1; then
        echo "[run-all] PASS  $(basename "$t")"
        pass=$((pass + 1))
    else
        echo "[run-all] FAIL  $(basename "$t")"
        fail=$((fail + 1))
        failed="$failed $(basename "$t")"
    fi
done
echo "[run-all] RESULT: $pass passed, $fail failed"
if [ "$fail" -gt 0 ]; then
    echo "[run-all] failed:$failed"
    exit 1
fi
exit 0
