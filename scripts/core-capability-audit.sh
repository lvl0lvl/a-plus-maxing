#!/usr/bin/env bash
# core-capability-audit.sh — the MECHANICAL core-capability-first gate (PF-S63-02).
#
# WHAT IT ENFORCES:
#   The ONE capability the system exists for stays WIRED end-to-end along the A′ spine: the
#   shared control-inversion driver (ADR-0026-T1, `scripts/plan/plan_driver.py`) drives the
#   inner engine (`pipeline.run_generation`) and gates on the composed `safety_passed` surface,
#   promoting survivors into the store -> the rendered dashboard plan. The PF-S63-02 drift was a
#   week of secondary work while this path stayed unbuilt and every component passed its own unit
#   tests; this gate makes "is the core capability wired?" a CHECKED answer, not a remembered one.
#
# CHECKS (PER-MODULE — the A′ spine spans two modules, so each grep is pinned to its host, QA-5):
#   1. the shared DRIVER exists — $CALLER (scripts/plan/plan_driver.py) is present.
#   2. the loop drives the inner engine — RUN_GEN_HOST (scripts/plan/plan_orchestrator.py)
#      references the EXECUTABLE `pipeline.run_generation(` call (not a docstring mention).
#   3. the disposition gate is present — $CALLER (plan_driver.py) carries the EXECUTABLE surface
#      gate `disposition.get("safety_passed") is True` AND the `accept` / `revise_domains` reads.
#      (The retired `record_plan(` structural check is DROPPED: the A′ spine promotes via
#       `_promote_plans`->`store.append`, it does NOT call `record_plan(`.)
#   4. BEHAVIORAL — the A′ spine runs end-to-end under the project .venv:
#      `_a_prime_self_test --self-test` (de-id -> driver -> the REAL composed gate -> promote ->
#      render), asserting the INVERTED loop: ≥1 plan promotes on accept AND 0 plans surface past a
#      non-True safety disposition. A grep proves the SHAPE; the self-test proves it RUNS — and runs
#      NON-TAUTOLOGICALLY (the inversion, not just "a plan renders"). The self-test signals failure
#      via its NON-ZERO EXIT (QA-3); the audit consumes ONLY that exit code (stdout/stderr
#      suppressed), so a self-test that printed "FAIL" but exit 0'd would read GREEN.
#
# EXIT (audit-helpers F-008 contract):
#   0 PASS   — the path is wired and runs.
#   1 FAIL   — a check found the path unwired (the PF-S63-02 regression).
#   2 FATAL  — a check could not RUN (e.g. .venv missing) and AUDIT_ALLOW_SKIP != 1.
#              "Couldn't verify the path runs" must never read as "verified wired".
#
# Test hooks (NEVER set in production — a loud WARNING fires if any is set):
#   CORE_CAP_CALLER        override the $CALLER (the A′ driver) the structural checks read
#   CORE_CAP_RUN_GEN_HOST  override the RUN_GEN_HOST (the run_generation greppee module)
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
for _thv in CORE_CAP_CALLER CORE_CAP_RUN_GEN_HOST CORE_CAP_PY CORE_CAP_SKIP_BEHAVIORAL; do
  if [ -n "${!_thv:-}" ]; then
    echo "core-capability-audit: WARNING: test-hook env var ${_thv} is active (tests/CI only — NOT a production close)" >&2
  fi
done

CALLER="${CORE_CAP_CALLER:-$REPO_ROOT/scripts/plan/plan_driver.py}"
RUN_GEN_HOST="${CORE_CAP_RUN_GEN_HOST:-$REPO_ROOT/scripts/plan/plan_orchestrator.py}"
PY="${CORE_CAP_PY:-$REPO_ROOT/.venv/bin/python}"

# The A′ spine spans TWO modules (QA-5), so each structural grep is PINNED to its host and asserts
# an EXECUTABLE reference (comment-stripped — the bare token `safety_passed` survives in
# plan_orchestrator.py comments, so the disposition-gate grep targets the full `.get(...) is True`
# expression in the driver). A docstring/comment mention must NOT read as a wired call.

# --- 1: structural — the A′ shared driver exists --------------------------------
if [ ! -f "$CALLER" ]; then
  violation PF-S63-02 "the A′ shared driver is missing: ${CALLER} (core capability unwired)"
fi

# --- 2: structural — the loop drives the inner engine ($RUN_GEN_HOST) -----------
# An EXECUTABLE `pipeline.run_generation(` call in plan_orchestrator.py (comment lines stripped).
if [ ! -f "$RUN_GEN_HOST" ]; then
  violation PF-S63-02 "the A′ run_generation host is missing: ${RUN_GEN_HOST} (the loop is unwired)"
elif ! grep -vE '^\s*#' "$RUN_GEN_HOST" | grep -Eq 'pipeline\.run_generation\('; then
  violation PF-S63-02 "${RUN_GEN_HOST} does not drive pipeline.run_generation( — the A′ loop is unwired"
fi

# --- 3: structural — the disposition gate is present ($CALLER) -------------------
# The EXECUTABLE surface gate `disposition.get("safety_passed") is True` AND the accept /
# revise_domains reads, matched on a NON-COMMENT line (the bare `safety_passed` token survives in
# plan_orchestrator.py comments — so target the full expression in the driver, comment-stripped).
if [ -f "$CALLER" ]; then
  _caller_exec="$(grep -vE '^\s*#' "$CALLER")"
  if ! printf '%s\n' "$_caller_exec" | grep -Fq 'disposition.get("safety_passed") is True'; then
    violation PF-S63-02 "${CALLER} does not gate on the safety_passed disposition — the A′ fail-closed gate is unwired"
  fi
  if ! printf '%s\n' "$_caller_exec" | grep -Eq 'disposition\.get\("accept"\)'; then
    violation PF-S63-02 "${CALLER} does not read the accept disposition — the A′ surface read is unwired"
  fi
  if ! printf '%s\n' "$_caller_exec" | grep -Eq 'revise_domains'; then
    violation PF-S63-02 "${CALLER} does not read revise_domains — the A′ bounded-revise read is unwired"
  fi
fi

# The live subscription dispatch (the real specialist/lens agents) is OUT of this audit's reach —
# the self-test drives a FIXTURE dispatch + the real composer over fixture judge/review (0 live
# spend). The live-dispatch leg is the S94 operator-present attestation, not a shell check.
info "live subscription dispatch is the S94 operator attestation, out of this audit's reach (the self-test uses a fixture dispatch)"

# --- 4: behavioral — the A′ spine runs end-to-end (NON-TAUTOLOGICAL inversion) --
if [ "${CORE_CAP_SKIP_BEHAVIORAL:-0}" = "1" ]; then
  info "behavioral self-test skipped (CORE_CAP_SKIP_BEHAVIORAL test hook)"
elif [ "${_AUDIT_COUNT}" -gt 0 ]; then
  info "skipping behavioral self-test — a structural check already FAILed (path unwired)"
elif [ ! -x "$PY" ]; then
  skipped "project python not executable: ${PY} (cannot run the A′ self-test)"
else
  # The audit consumes ONLY the self-test's exit code (stdout/stderr suppressed): the failure
  # signal is the NON-ZERO EXIT, never a printed message (QA-3) — a printed "FAIL" that exit 0'd
  # would read GREEN, the exact PF-S63-02 tautology.
  if ( cd "$REPO_ROOT" && PYTHONPATH="$REPO_ROOT" "$PY" -m scripts.plan._a_prime_self_test --self-test >/dev/null 2>&1 ); then
    info "A′-inversion self-test PASS (de-id -> driver -> composed gate -> promote -> render)"
  else
    violation PF-S63-02 "A′-inversion self-test FAILED — the core capability does not run end-to-end (or a loop inversion broke)"
  fi
fi

audit_summary
audit_exit
