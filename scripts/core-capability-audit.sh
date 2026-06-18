#!/usr/bin/env bash
# core-capability-audit.sh — the MECHANICAL core-capability-first gate (PF-S63-02).
#
# WHAT IT ENFORCES:
#   The ONE capability the system exists for stays WIRED end-to-end: a plan author's
#   output flows through `assemble` (the four safety filters) -> `record_plan` -> the
#   rendered dashboard plan. The PF-S63-02 drift was a week of secondary work while this
#   path stayed unbuilt and every component passed its own unit tests; this gate makes
#   "is the core capability wired?" a CHECKED answer, not a remembered one.
#
# CHECKS:
#   1. assemble HAS a production caller — scripts/plan/generate_plan.py exists and calls
#      `assemble(`.
#   2. that caller records the plan — it calls `record_plan(`.
#   3. BEHAVIORAL — the wired path runs end-to-end under the project .venv:
#      `generate_plan --self-test` (author -> assemble -> record_plan -> the dashboard
#      renders the recorded plan). A grep proves the SHAPE; the self-test proves it RUNS.
#
# EXIT (audit-helpers F-008 contract):
#   0 PASS   — the path is wired and runs.
#   1 FAIL   — a check found the path unwired (the PF-S63-02 regression).
#   2 FATAL  — a check could not RUN (e.g. .venv missing) and AUDIT_ALLOW_SKIP != 1.
#              "Couldn't verify the path runs" must never read as "verified wired".
#
# Test hooks (NEVER set in production — a loud WARNING fires if any is set):
#   CORE_CAP_CALLER        override the caller path the structural checks read
#   CORE_CAP_PY            override the python used for the behavioral self-test
#   CORE_CAP_SKIP_BEHAVIORAL=1  skip the behavioral self-test (structural-only isolation
#                               for the negative test — emits no skipped(), no violation)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SCRIPT_DIR/lib/audit-helpers.sh"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

audit_init "core-capability-audit"

# Surface accidental production use of a test hook (mirrors close-audit F2).
for _thv in CORE_CAP_CALLER CORE_CAP_PY CORE_CAP_SKIP_BEHAVIORAL; do
  if [ -n "${!_thv:-}" ]; then
    echo "core-capability-audit: WARNING: test-hook env var ${_thv} is active (tests/CI only — NOT a production close)" >&2
  fi
done

CALLER="${CORE_CAP_CALLER:-$REPO_ROOT/scripts/plan/generate_plan.py}"
PY="${CORE_CAP_PY:-$REPO_ROOT/.venv/bin/python}"

# --- 1 + 2: structural — assemble has a production caller that records the plan ---
if [ ! -f "$CALLER" ]; then
  violation PF-S63-02 "assemble has no production caller: ${CALLER} is missing (core capability unwired)"
else
  grep -Eq 'assemble\(' "$CALLER" \
    || violation PF-S63-02 "${CALLER} does not call assemble( — assemble has no production caller"
  grep -Eq 'record_plan\(' "$CALLER" \
    || violation PF-S63-02 "${CALLER} does not call record_plan( — the assembled plan is never recorded"
fi

# --- 3: behavioral — the wired path runs end-to-end -----------------------------
if [ "${CORE_CAP_SKIP_BEHAVIORAL:-0}" = "1" ]; then
  info "behavioral self-test skipped (CORE_CAP_SKIP_BEHAVIORAL test hook)"
elif [ "${_AUDIT_COUNT}" -gt 0 ]; then
  info "skipping behavioral self-test — a structural check already FAILed (path unwired)"
elif [ ! -x "$PY" ]; then
  skipped "project python not executable: ${PY} (cannot run the wired-path self-test)"
else
  if ( cd "$REPO_ROOT" && PYTHONPATH="$REPO_ROOT" "$PY" -m scripts.plan.generate_plan --self-test >/dev/null 2>&1 ); then
    info "wired-path self-test PASS (author -> assemble -> record_plan -> dashboard)"
  else
    violation PF-S63-02 "wired-path self-test FAILED — the core capability does not run end-to-end"
  fi
fi

audit_summary
audit_exit
