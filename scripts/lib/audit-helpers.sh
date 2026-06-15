#!/usr/bin/env bash
# audit-helpers.sh — shared primitives for project audit scripts.
#
# Sourced (not executed) by scripts/*-audit.sh. Provides a uniform
# emit / violation / skipped / summary / exit interface so close-protocol
# step 8.5 (via scripts/close-audit.sh) can dispatch each audit identically
# and aggregate results.
#
# Per Rigor Framework Discipline 5 §3: invariants get scripts; scripts share
# a common emitter so output stays diffable across audits and parseable by
# downstream tooling.
#
# Usage:
#   #!/usr/bin/env bash
#   set -euo pipefail
#   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   source "$SCRIPT_DIR/lib/audit-helpers.sh"
#
#   audit_init "handoff-audit"
#   violation INV-HO-ROTATION "two Historical pointers found at lines 14, 31"
#   skipped "jq not found — settings.json hook check not run"   # see F-008 below
#   info "Scanned 187 lines, 4 VOLATILE sections"
#   audit_summary
#   audit_exit
#
# Exit codes (audit_exit) — F-008 fail-closed contract:
#   0 — PASS: ran clean, nothing skipped
#   1 — FAIL: one or more violations (takes precedence over a skip)
#   2 — FATAL: a check could not RUN (skipped) and AUDIT_ALLOW_SKIP != 1.
#       "Couldn't verify" must never read as "verified clean" — a skipped
#       check fails closed. Opt out (treat skip as non-blocking) per-run with
#       AUDIT_ALLOW_SKIP=1, only where a missing dep is a deliberate non-blocker.
#
# Stderr format:
#   <audit_name>: VIOLATION <INV-ID>: <message>
#   <audit_name>: SKIPPED: <message>
#   <audit_name>: info: <message>
#   <audit_name>: <N> violation(s), <M> skipped
#
# Stdout is left untouched so audit scripts can emit machine-readable
# JSON if they want; humans + close-protocol read stderr.

# Guard against double-source.
if [[ "${_AUDIT_HELPERS_LOADED:-0}" == "1" ]]; then
    return 0 2>/dev/null || exit 0
fi
_AUDIT_HELPERS_LOADED=1

# Globals reset by audit_init. Underscore prefix marks them private.
_AUDIT_NAME=""
_AUDIT_COUNT=0
_AUDIT_SKIPS=0

audit_init() {
    # Initialize a new audit run. Resets violation + skip counters.
    # Arg 1: short audit name (used in every stderr line).
    if [[ $# -lt 1 ]]; then
        echo "audit_init: missing audit name argument" >&2
        return 2
    fi
    _AUDIT_NAME="$1"
    _AUDIT_COUNT=0
    _AUDIT_SKIPS=0
}

violation() {
    # Record a violation. Increments counter, prints to stderr.
    # Arg 1: invariant id (e.g., INV-HO-ROTATION)
    # Arg 2+: message (joined with spaces)
    if [[ $# -lt 2 ]]; then
        echo "${_AUDIT_NAME}: violation() requires invariant_id + message" >&2
        return 2
    fi
    local inv_id="$1"; shift
    local msg="$*"
    _AUDIT_COUNT=$((_AUDIT_COUNT + 1))
    echo "${_AUDIT_NAME}: VIOLATION ${inv_id}: ${msg}" >&2
}

skipped() {
    # Record a check that COULD NOT RUN (missing dep/input/tool). Per F-008 this
    # is fail-closed: a skip forces FATAL (exit 2) via audit_exit unless
    # AUDIT_ALLOW_SKIP=1. A violation still takes precedence over a skip.
    # Arg 1+: message
    local msg="$*"
    _AUDIT_SKIPS=$((_AUDIT_SKIPS + 1))
    echo "${_AUDIT_NAME}: SKIPPED: ${msg}" >&2
}

info() {
    # Diagnostic line. Does NOT increment any counter.
    # Arg 1+: message
    local msg="$*"
    echo "${_AUDIT_NAME}: info: ${msg}" >&2
}

audit_summary() {
    # Print one-line summary to stderr. Does not exit.
    echo "${_AUDIT_NAME}: ${_AUDIT_COUNT} violation(s), ${_AUDIT_SKIPS} skipped" >&2
}

audit_exit() {
    # Terminal verdict. F-008 fail-closed exit-code contract:
    #   1 FAIL  — one or more violations (precedence over a skip, so a real
    #             violation is never masked by a concurrent skip).
    #   2 FATAL — a check was skipped (could not run) and AUDIT_ALLOW_SKIP != 1.
    #   0 PASS  — ran clean, nothing skipped.
    if [[ ${_AUDIT_COUNT} -gt 0 ]]; then
        exit 1
    fi
    if [[ ${_AUDIT_SKIPS} -gt 0 && "${AUDIT_ALLOW_SKIP:-0}" != "1" ]]; then
        exit 2
    fi
    exit 0
}

# Read-only accessors for tests that source this lib and want to assert
# state without triggering exit.
audit_count() {
    echo "${_AUDIT_COUNT}"
}

skipped_count() {
    echo "${_AUDIT_SKIPS}"
}
