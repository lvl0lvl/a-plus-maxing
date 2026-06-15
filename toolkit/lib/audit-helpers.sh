#!/usr/bin/env bash
# toolkit/lib/audit-helpers.sh — portable shared helpers for rigor audit scripts.
#
# Dependency-free (no jq/python). Source this from every audit; it normalizes
# output to `[<AUDIT_TAG>] LEVEL: msg` so operators grepping CI logs see one shape.
#
# Verbs: emit (info), warn (non-blocking), fail (records a violation),
#        skipped (records a couldn't-run check), verdict (terminal exit).
#
# EXIT SEMANTICS — 0 PASS / 1 FAIL / 2 FATAL:
#   verdict exits 0 only when violations==0 AND no fail-closed skips.
#   violations>0  -> exit 1 (FAIL).
#   skips present and NOT explicitly allowed -> exit 2 (FATAL).
#   A config/env error the caller can't recover from -> `emit "FATAL: ..."; exit 2`.
#
# SKIPPED / FAIL-CLOSED rationale (Finding F-008): a green audit is NOT evidence
# when the gated check was env-skipped (e.g. a dep was absent and the path WARN'd
# to exit 0). "Couldn't verify" must never read as "verified clean." So a SKIPPED
# check is FAIL-CLOSED by default: it forces FATAL (exit 2) — mirroring maquette's
# FATAL≠clean-pass meta-audit insight that a check which cannot RUN must not PASS.
# Opt out only with AUDIT_ALLOW_SKIP=1 (then skips warn but don't gate), for
# environments where a missing dep is a deliberate, documented non-blocker.
#
# BUG-N convention: when a real defect is found and fixed in an audit (or here),
# annotate the fix site with a `# BUG-N (context): ...` comment so the negative
# test that proves the fix has a stable referent. An audit that cannot prove it
# FAILs on bad input does not count (F-007) — see test-lib.sh.

AUDIT_TAG="${AUDIT_TAG:-audit}"
violations=0
skips=0

emit() {
  echo "[${AUDIT_TAG}] $*"
}

fail() {
  emit "FAIL: $*"
  violations=$((violations + 1))
}

warn() {
  emit "WARN: $*"
}

# skipped — record a check that could not run. Fail-closed unless AUDIT_ALLOW_SKIP=1.
skipped() {
  if [ "${AUDIT_ALLOW_SKIP:-0}" = "1" ]; then
    emit "SKIPPED: $* (allowed via AUDIT_ALLOW_SKIP=1; not gating)"
  else
    emit "SKIPPED: $* (fail-closed: a check that cannot run does not pass — F-008)"
    skips=$((skips + 1))
  fi
}

# verdict — terminal call: prints RESULT and exits 0 (PASS) / 1 (FAIL) / 2 (FATAL).
# FAIL takes precedence over FATAL-on-skip so a real violation is never masked.
verdict() {
  if [ "$violations" -gt 0 ]; then
    emit "RESULT: FAIL (${violations} violation(s))"
    exit 1
  fi
  if [ "$skips" -gt 0 ]; then
    emit "RESULT: FATAL (${skips} skipped check(s) could not run — fail-closed)"
    exit 2
  fi
  emit "RESULT: PASS"
  exit 0
}
