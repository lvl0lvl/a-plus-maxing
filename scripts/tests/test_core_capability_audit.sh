#!/usr/bin/env bash
# test_core_capability_audit.sh — negative test for core-capability-audit.sh (F-007).
#
# Per Rigor Framework Discipline 5 (F-007): a mechanical gate only counts as enforcing
# once it has PROVEN it goes RED on bad input. This proves core-capability-audit.sh:
#   - FAILs (exit 1) when assemble has no production caller (the PF-S63-02 regression):
#       (A) the caller does not call assemble, (B) the caller file is missing;
#   - PASSes (exit 0) on a structurally-wired caller; and
#   - PASSes (exit 0) on the REAL tree incl. the behavioral wired-path self-test.
# A gate that stayed green under (A)/(B) would be tautological.

set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATE="$SELF_DIR/../core-capability-audit.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail=0
check() {  # check <label> <expected-exit> <actual-exit>
  if [ "$2" != "$3" ]; then
    echo "FAIL: $1 — expected exit $2, got $3"
    fail=1
  else
    echo "ok: $1 (exit $3)"
  fi
}

# (A) RED — a caller that does not call assemble (structural, behavioral skipped).
cat > "$TMP/no-assemble.py" <<'PY'
# a caller stub that forgot to call assemble — record_plan(x) only
PY
rc=0; CORE_CAP_CALLER="$TMP/no-assemble.py" CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "caller-without-assemble FAILs" 1 "$rc"

# (B) RED — the caller file is missing entirely.
rc=0; CORE_CAP_CALLER="$TMP/does-not-exist.py" CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "missing-caller FAILs" 1 "$rc"

# (C) GREEN — a structurally-wired caller (calls both assemble and record_plan).
cat > "$TMP/wired.py" <<'PY'
# stub: section = assemble([domain], summary, roster)
# record_plan(domain, plan, plan_date, specialist, root)
PY
rc=0; CORE_CAP_CALLER="$TMP/wired.py" CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "structurally-wired caller PASSes" 0 "$rc"

# (D) GREEN — the REAL tree, including the behavioral wired-path self-test.
rc=0; bash "$GATE" >/dev/null 2>&1 || rc=$?
check "real wired path (incl. self-test) PASSes" 0 "$rc"

if [ "$fail" -ne 0 ]; then
  echo "test_core_capability_audit: FAILED"
  exit 1
fi
echo "test_core_capability_audit: all cases passed"
exit 0
