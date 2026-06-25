#!/usr/bin/env bash
# test_core_capability_audit.sh — negative test for core-capability-audit.sh (F-007).
#
# Per Rigor Framework Discipline 5 (F-007): a mechanical gate only counts as enforcing
# once it has PROVEN it goes RED on bad input. This proves core-capability-audit.sh goes
# RED on a deliberately-UNWIRED A′ spine (ADR-0026-T4 repoint). The A′ spine spans TWO
# modules (QA-5), so each RED case OMITS a SPECIFIC A′-spine token in its host module:
#   - (A) the DRIVER ($CALLER) omits the disposition gate -> structural check 3 FAILs;
#   - (B) the DRIVER file is missing -> structural check 1 FAILs;
#   - (B2) the RUN_GEN_HOST omits `pipeline.run_generation(` -> structural check 2 FAILs;
#   - (C) a structurally-wired A′ spine (driver carries the disposition gate + accept /
#         revise_domains reads, RUN_GEN_HOST carries `pipeline.run_generation(`) PASSes;
#   - (D) the REAL tree (incl. the A′-inversion behavioral self-test) PASSes.
# Each RED case REDs on its specific A′-spine token — NEVER on the retired `assemble(` /
# `record_plan(` checks the repoint DROPPED. A gate that stayed green under (A)/(B)/(B2)
# would be tautological.

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

# A valid A′ DRIVER stub ($CALLER): carries the EXECUTABLE disposition gate + the accept /
# revise_domains reads (the structural check-3 surface). Reused by the GREEN case + as the valid
# half of the per-check-independence RED cases.
cat > "$TMP/driver-wired.py" <<'PY'
# an A′ shared-driver stub carrying the executable disposition gate + accept / revise reads
def drive(...):
    if not (isinstance(disposition, dict) and disposition.get("safety_passed") is True):
        return _honest_no_plan(SAFETY_BLOCKED)
    if disposition.get("accept") is True:
        _promote_plans(scratch, root)
    revise_domains = disposition.get("revise_domains") or []
PY

# A valid RUN_GEN_HOST stub: carries the EXECUTABLE `pipeline.run_generation(` call (check-2 surface).
cat > "$TMP/host-wired.py" <<'PY'
# an A′ run_generation host stub driving the inner engine
result = pipeline.run_generation(authors, store_read, scratch, plan_date=plan_date)
PY

# (A) RED — the DRIVER omits the disposition gate (check 3 FAILs on its specific A′ token).
# A valid RUN_GEN_HOST (so check 2 passes) isolates the failure to the disposition-gate check.
cat > "$TMP/driver-no-gate.py" <<'PY'
# an A′ driver stub MISSING the disposition gate — drives nothing, gates on nothing
def drive(...):
    authors = yield (domains, summary, gates)
    return {"results": {}}
PY
rc=0; CORE_CAP_CALLER="$TMP/driver-no-gate.py" CORE_CAP_RUN_GEN_HOST="$TMP/host-wired.py" \
  CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "driver-without-disposition-gate FAILs" 1 "$rc"

# (B) RED — the DRIVER ($CALLER) file is missing entirely (check 1 FAILs).
rc=0; CORE_CAP_CALLER="$TMP/does-not-exist.py" CORE_CAP_RUN_GEN_HOST="$TMP/host-wired.py" \
  CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "missing-driver FAILs" 1 "$rc"

# (B2) RED — the RUN_GEN_HOST omits `pipeline.run_generation(` (check 2 FAILs INDEPENDENTLY of
# check 3 — a valid driver with the disposition gate, so the failure isolates to the host's
# run_generation check; the original B2 per-check-independence intent).
cat > "$TMP/host-no-run-gen.py" <<'PY'
# a RUN_GEN_HOST stub that does NOT drive pipeline.run_generation(
result = None  # the inner engine is never driven
PY
rc=0; CORE_CAP_CALLER="$TMP/driver-wired.py" CORE_CAP_RUN_GEN_HOST="$TMP/host-no-run-gen.py" \
  CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "host-without-run_generation FAILs" 1 "$rc"

# (C) GREEN — a structurally-wired A′ spine (driver carries the disposition gate + accept /
# revise reads; RUN_GEN_HOST carries pipeline.run_generation(). Both wired via the two hooks.
rc=0; CORE_CAP_CALLER="$TMP/driver-wired.py" CORE_CAP_RUN_GEN_HOST="$TMP/host-wired.py" \
  CORE_CAP_SKIP_BEHAVIORAL=1 bash "$GATE" >/dev/null 2>&1 || rc=$?
check "structurally-wired A′ spine PASSes" 0 "$rc"

# (D) GREEN — the REAL tree, including the A′-inversion behavioral self-test.
rc=0; bash "$GATE" >/dev/null 2>&1 || rc=$?
check "real wired A′ path (incl. self-test) PASSes" 0 "$rc"

if [ "$fail" -ne 0 ]; then
  echo "test_core_capability_audit: FAILED"
  exit 1
fi
echo "test_core_capability_audit: all cases passed"
exit 0
