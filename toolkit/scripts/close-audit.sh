#!/usr/bin/env bash
# toolkit/scripts/close-audit.sh — the mandatory CLOSE GATE meta-audit.
#
# WHAT IT ENFORCES (CDM F-008 / maquette BUG-002, EN-011):
#   A "clean close" / "all audits GREEN" attestation is only honest if every
#   constituent audit GENUINELY RAN and returned exit 0 in the same close cycle.
#   "Couldn't verify" != "verified clean". So this meta-audit runs each sibling
#   audit script and:
#     - PASSes (exit 0) only when ALL ran and ALL returned 0;
#     - FAILs  (exit 1) when any constituent reports a real violation (exit 1);
#     - FATALs (exit 2) when any constituent could not RUN (missing, not
#       executable, or exited >=2) — a non-functional check must NOT be silently
#       passed over. This is the F-008 fail-closed posture at the meta level.
#   A GREEN from this gate covers EXACTLY the audits it lists as "ran: PASS".
#
# SOURCE LINEAGE:
#   Generalized from maquette scripts/close-attestation-audit.sh (the FATAL!=clean-
#   pass meta-audit, INV-CLOSE-ATTEST, caught PFs S9-01/S14-01/S15-02). De-hardcoded:
#   no project paths, no project-specific script roster — constituents are
#   discovered from the same scripts/ dir (or supplied via args / $CLOSE_AUDIT_SCRIPTS).
#
# BUG-N NOTES CARRIED FORWARD:
#   BUG-002 (maquette S23): a constituent returning FATAL (exit >=2 — broken parser,
#     missing gitignored input) previously only WARNed and the meta-audit still
#     PASSed, making every "GREEN" close attestation hollow. Now FATAL constituents
#     block with exit 2. (This script's reason for existing.)
#   TEST-001 (maquette PR#10): the meta-audit is often the SOLE automated caller of a
#     constituent, so flags a constituent needs in order to run its full check (e.g.
#     --strict) must be forwarded — else a gated sub-check never fires at close. We
#     forward CLOSE_AUDIT_CHILD_ARGS to every child for this reason.
#   API-001 (maquette PR#10): a constituent declared OPTIONAL may exit >=2 on a
#     deliberately-absent input WITHOUT blocking; but a real violation (exit 1) from
#     an optional constituent still blocks. Optional != "ignored".
#
# USAGE:
#   close-audit.sh [--allow-skip] [--scripts-dir DIR] [--child-arg ARG]... [script...]
#   Env:
#     CLOSE_AUDIT_SCRIPTS      space-separated constituent basenames (overrides discovery)
#     CLOSE_AUDIT_SCRIPTS_DIR  dir to discover/run constituents from (default: this dir)
#     CLOSE_AUDIT_OPTIONAL     space-separated basenames treated as optional
#     CLOSE_AUDIT_CHILD_ARGS   args forwarded verbatim to every constituent
#     AUDIT_ALLOW_SKIP=1       allow-skip: a couldn't-run constituent WARNs, not FATAL
#                              (mirrors --allow-skip / lib's fail-closed opt-out)
#
# EXIT: 0 PASS (all listed audits ran clean) / 1 FAIL (a violation) / 2 FATAL
#       (a constituent could not run, or config/env error).
#
# Portable across BSD (macOS bash 3.2) and GNU. Dependency-free.

set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-close-audit}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$(dirname "$0")/../lib/audit-helpers.sh"

# --- arg / env parsing -------------------------------------------------------
SCRIPTS_DIR="${CLOSE_AUDIT_SCRIPTS_DIR:-$SELF_DIR}"
# Discovery (glob a dir's *-audit.sh) is OPT-IN via an explicit --scripts-dir /
# $CLOSE_AUDIT_SCRIPTS_DIR. With no explicit dir, the canonical DEFAULT_ROSTER is used.
DISCOVER=0; [ -n "${CLOSE_AUDIT_SCRIPTS_DIR:-}" ] && DISCOVER=1
# child args: start from env, append --child-arg occurrences
CHILD_ARGS=()
if [ -n "${CLOSE_AUDIT_CHILD_ARGS:-}" ]; then
  # word-split the env string (intentional)
  # shellcheck disable=SC2206
  CHILD_ARGS=(${CLOSE_AUDIT_CHILD_ARGS})
fi
EXPLICIT_SCRIPTS=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --allow-skip)        AUDIT_ALLOW_SKIP=1 ;;
    --scripts-dir)       shift; [ "$#" -gt 0 ] || { emit "FATAL: --scripts-dir needs a value"; exit 2; }; SCRIPTS_DIR="$1"; DISCOVER=1 ;;
    --scripts-dir=*)     SCRIPTS_DIR="${1#*=}"; DISCOVER=1 ;;
    --child-arg)         shift; [ "$#" -gt 0 ] || { emit "FATAL: --child-arg needs a value"; exit 2; }; CHILD_ARGS+=("$1") ;;
    --child-arg=*)       CHILD_ARGS+=("${1#*=}") ;;
    -h|--help)           sed -n '2,40p' "$0"; exit 0 ;;
    --*)                 emit "FATAL: unknown arg: $1"; exit 2 ;;
    *)                   EXPLICIT_SCRIPTS+=("$1") ;;
  esac
  shift
done

if [ ! -d "$SCRIPTS_DIR" ]; then
  emit "FATAL: scripts dir not found: $SCRIPTS_DIR"
  exit 2
fi

# --- build the constituent roster -------------------------------------------
# Precedence: explicit args > $CLOSE_AUDIT_SCRIPTS > the explicit DEFAULT per-close
# roster below. We do NOT glob *-audit.sh: that wrongly swept in parity-audit.sh and
# consistency-audit.sh (which are per-HARVEST / pre-release, library-wide — NOT per
# session close) and excluded *-scan / *-gate members. The default roster below is
# the single canonical per-close blocking set; it must match Discipline 1 step 7.
#   IN  (per-close, blocking): rotation-stamp-audit, stale-hash-audit, pf-attestation-audit
#   OUT (advisory):            falsification-scan.sh — warnings only, never blocks; run separately
#   OUT (distinct close step): harvest-gate.sh — needs session args (--pf/--harvest/--beads)
#   OUT (per-harvest/release): parity-audit.sh, consistency-audit.sh — library-wide cadence (Discipline 11)
# Override the roster per project via $CLOSE_AUDIT_SCRIPTS or positional args.
DEFAULT_ROSTER="rotation-stamp-audit.sh stale-hash-audit.sh pf-attestation-audit.sh"
SCRIPTS=()
if [ "${#EXPLICIT_SCRIPTS[@]}" -gt 0 ]; then
  SCRIPTS=("${EXPLICIT_SCRIPTS[@]}")
elif [ -n "${CLOSE_AUDIT_SCRIPTS:-}" ]; then
  # shellcheck disable=SC2206
  SCRIPTS=(${CLOSE_AUDIT_SCRIPTS})
elif [ "$DISCOVER" -eq 1 ]; then
  # Explicit --scripts-dir: discover sibling *-audit.sh in that dir (used for testing
  # against fixture rosters). Portable, no `find -printf`.
  self_base="$(basename "$0")"
  for f in "$SCRIPTS_DIR"/*-audit.sh; do
    [ -e "$f" ] || continue
    b="$(basename "$f")"
    [ "$b" = "$self_base" ] && continue
    SCRIPTS+=("$b")
  done
else
  # shellcheck disable=SC2206
  SCRIPTS=(${DEFAULT_ROSTER})
  # A rostered audit that isn't present on disk is fail-closed by run_one (FATAL),
  # so a project that hasn't installed one must override the roster, not silently skip it.
fi

# Optional set (membership test below).
OPTIONAL_SET=" ${CLOSE_AUDIT_OPTIONAL:-} "

is_optional() {
  case "$OPTIONAL_SET" in
    *" $1 "*) return 0 ;;
    *)        return 1 ;;
  esac
}

if [ "${#SCRIPTS[@]}" -eq 0 ]; then
  # No constituents to run is itself a couldn't-verify state: fail-closed.
  skipped "no constituent audit scripts found in ${SCRIPTS_DIR} — nothing to attest"
  verdict
fi

# --- run each constituent ----------------------------------------------------
ran_pass=()
failed_scripts=()
fatal_scripts=()

run_one() {
  s="$1"
  # Allow either a bare basename (resolved against SCRIPTS_DIR) or a path.
  case "$s" in
    */*) path="$s" ;;
    *)   path="${SCRIPTS_DIR}/${s}" ;;
  esac

  if [ ! -f "$path" ]; then
    if is_optional "$s"; then
      warn "${s}: missing (optional) — not blocking"
      return
    fi
    fatal_scripts+=("$s")
    emit "FATAL: ${s}: missing at ${path} (cannot run -> cannot attest)"
    return
  fi
  if [ ! -x "$path" ]; then
    if is_optional "$s"; then
      warn "${s}: not executable (optional) — not blocking"
      return
    fi
    fatal_scripts+=("$s")
    emit "FATAL: ${s}: not executable at ${path} (cannot run -> cannot attest)"
    return
  fi

  emit "running ${s}..."
  rc=0
  if [ "${#CHILD_ARGS[@]}" -gt 0 ]; then
    bash "$path" "${CHILD_ARGS[@]}" >/dev/null 2>&1 || rc=$?
  else
    bash "$path" >/dev/null 2>&1 || rc=$?
  fi

  if [ "$rc" -eq 0 ]; then
    emit "  ${s}: PASS"
    ran_pass+=("$s")
  elif [ "$rc" -eq 1 ]; then
    # A real violation blocks regardless of optional status (API-001).
    failed_scripts+=("$s")
    emit "  ${s}: FAIL (exit 1)"
  else
    # rc >= 2: the constituent could not run / fataled.
    if is_optional "$s"; then
      warn "${s}: exit ${rc} (FATAL) — optional; not blocking the meta-audit"
    else
      fatal_scripts+=("$s")
      emit "  ${s}: FATAL (exit ${rc}) — could not run"
    fi
  fi
}

for s in "${SCRIPTS[@]}"; do
  run_one "$s"
done

# --- verdict accounting ------------------------------------------------------
# FAIL (real violation) takes precedence over FATAL-on-couldn't-run, so a true
# violation is never masked by a missing sibling.
if [ "${#failed_scripts[@]}" -gt 0 ]; then
  for s in "${failed_scripts[@]}"; do fail "constituent FAILed: ${s}"; done
fi

# A constituent that could not run is fail-closed via skipped() (F-008): it bumps
# $skips and forces FATAL via verdict, unless AUDIT_ALLOW_SKIP=1.
if [ "${#fatal_scripts[@]}" -gt 0 ]; then
  for s in "${fatal_scripts[@]}"; do
    skipped "constituent could not run: ${s} (a GREEN must not cover an audit that did not run)"
  done
fi

# State plainly what a GREEN here covers.
if [ "${#ran_pass[@]}" -gt 0 ]; then
  emit "ran + PASSED (${#ran_pass[@]}): ${ran_pass[*]}"
  emit "a GREEN from this close gate covers EXACTLY the audits listed above as ran+PASSED"
else
  emit "ran + PASSED (0): none"
fi

verdict
