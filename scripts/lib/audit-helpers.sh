#!/usr/bin/env bash
# audit-helpers.sh — shared primitives for project audit scripts.
#
# Sourced (not executed) by scripts/*-audit.sh. Provides a uniform
# emit / violation / summary / exit interface so close-protocol step 8.5
# can dispatch each audit identically and aggregate results.
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
#   info "Scanned 187 lines, 4 VOLATILE sections"
#   audit_summary
#   audit_exit
#
# Exit codes (audit_exit):
#   0 — no violations
#   1 — one or more violations
#
# Stderr format:
#   <audit_name>: VIOLATION <INV-ID>: <message>
#   <audit_name>: info: <message>
#   <audit_name>: <N> violation(s)
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

audit_init() {
    # Initialize a new audit run. Resets violation counter.
    # Arg 1: short audit name (used in every stderr line).
    if [[ $# -lt 1 ]]; then
        echo "audit_init: missing audit name argument" >&2
        return 2
    fi
    _AUDIT_NAME="$1"
    _AUDIT_COUNT=0
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

info() {
    # Diagnostic line. Does NOT increment violation counter.
    # Arg 1+: message
    local msg="$*"
    echo "${_AUDIT_NAME}: info: ${msg}" >&2
}

audit_summary() {
    # Print one-line summary to stderr. Does not exit.
    echo "${_AUDIT_NAME}: ${_AUDIT_COUNT} violation(s)" >&2
}

audit_exit() {
    # Exit 0 if no violations recorded, exit 1 otherwise.
    if [[ ${_AUDIT_COUNT} -eq 0 ]]; then
        exit 0
    fi
    exit 1
}

# Read-only accessor for tests that source this lib and want to assert
# state without triggering exit.
audit_count() {
    echo "${_AUDIT_COUNT}"
}
