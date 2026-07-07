#!/usr/bin/env bash
# toolkit/scripts/watchdog.sh — the companion WATCHDOG for active agent supervision.
#
# WHAT IT ENFORCES (ADR-0005, F-007 property-not-signal audit family):
#   The dispatch-time hook enforce-heartbeat-clause.sh guarantees every agent
#   prompt CONTAINS a liveness clause — but nothing tracks whether the heartbeats
#   that clause promises actually ARRIVE. This is the runtime complement: a
#   registry-based polling watchdog. `register` records an agent at dispatch (its
#   registration timestamp begins aging immediately), `heartbeat` refreshes its
#   liveness, `close` reaps it, and `poll` flags every registered-not-closed agent
#   whose last heartbeat is older than its cadence as STALLED — catching the
#   register-then-never-heartbeat / drop-at-t=0 worst case a heartbeat-mtime-only
#   design structurally misses.
#
# FAIL-CLOSED CONSTRAINTS (ADR-0005 Decision, all five are binding, not optional):
#   1. Readability gate — no vacuous PASS. `poll` asserts every registered entry
#      parses. A corrupt/unparseable entry resolves fail-closed (skipped -> FATAL),
#      NEVER a fall-through empty-loop exit 0 (the CF-1 false-green disease, F-008).
#      A legitimate ZERO-tracked poll EMITS a loud "0 tracked" line so a genuine
#      empty is distinguishable in CI logs from "all tracked agents healthy."
#   2. Atomic writes — no torn reads. register/heartbeat/close write a temp file
#      then `mv`-rename it into place (atomic on the same filesystem on BSD + GNU),
#      so a concurrent `poll` reader never observes a half-written / torn entry.
#   3. Roster integration. Running with NO arguments behaves as `poll`, so the
#      watchdog can be a close-audit roster constituent and self-trigger at every
#      session boundary (an open/STALLED agent at close blocks the close gate).
#   4. FATAL on degenerate cadence. A --cadence that is non-numeric or <= 0 is a
#      FATAL config error (exit 2) — it would otherwise be an infinite silent stall
#      window (fail-OPEN). A missing --cadence uses a finite default of 600s.
#   5. Lifecycle. `close <id>` removes the entry (does not merely mark it), so a
#      completed agent stops being scanned and stale STALLED entries do not
#      accumulate into alarm-fatigue.
#
# REGISTRY: one plain file per agent under ${CLAUDE_PROJECT_DIR}/.rigor/watchdog/<id>
#   so individual lookups and globbing are both clean. Each file is a single line:
#     register_ts=<epoch> cadence=<secs> last_heartbeat_ts=<epoch>
#
# BUG-N convention (see lib/audit-helpers.sh): a real defect found+fixed here is
#   annotated `# BUG-N (context): ...` so the negative test has a stable referent.
#   An audit that cannot prove it FAILs on bad input does not count (F-007) — see
#   tests/test-watchdog.sh.
#
# TESTABILITY SEAM: the current epoch is read from WATCHDOG_NOW if set, else
#   `date +%s`, so the negative test is deterministic without real sleeps.
#
# USAGE:
#   watchdog.sh register <id> [--cadence SECS]   # record an agent (cadence default 600)
#   watchdog.sh heartbeat <id>                   # refresh liveness
#   watchdog.sh close <id>                       # reap a completed agent
#   watchdog.sh poll                             # scan; STALLED -> exit 1
#   watchdog.sh                                  # no args == poll (roster constituent)
#
# EXIT: 0 PASS (no registered-not-closed agent past cadence; 0-tracked is a loud
#       PASS) / 1 FAIL (>=1 agent STALLED) / 2 FATAL (corrupt registry, degenerate
#       cadence, bad args — a check that cannot run does not pass).
#
# Portable across BSD (macOS bash 3.2) and GNU. Dependency-free: no jq/python.

set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-watchdog}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "${SELF_DIR}/../lib/audit-helpers.sh"

# --- project state location --------------------------------------------------
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
REG_DIR="${PROJECT_DIR}/.rigor/watchdog"

# now — testability seam: WATCHDOG_NOW override else wall clock.
now() {
  if [ -n "${WATCHDOG_NOW:-}" ]; then
    printf '%s' "$WATCHDOG_NOW"
  else
    date +%s
  fi
}

# is_pos_int <s> — true iff s is a string of digits representing an integer > 0.
is_pos_int() {
  case "$1" in
    ''|*[!0-9]*) return 1 ;;   # empty or contains a non-digit (rejects -5, abc, 1.5)
    *) [ "$1" -gt 0 ] ;;       # rejects 0
  esac
}

# is_nonneg_int <s> — true iff s is a string of digits (>= 0). Used to validate
# timestamps read back from a registry entry (a corrupt ts must fail-closed).
is_nonneg_int() {
  case "$1" in
    ''|*[!0-9]*) return 1 ;;
    *) return 0 ;;
  esac
}

# atomic_write <dest> <content> — write a temp file in the same dir then mv-rename
# it over <dest>. mv rename-over-existing is atomic on the same filesystem on both
# BSD and GNU, so a concurrent poll reader never sees a torn entry (ADR-0005 #2).
atomic_write() {
  dest="$1"; content="$2"
  d="$(dirname "$dest")"
  mkdir -p "$d" || { emit "FATAL: cannot create registry dir: $d"; exit 2; }
  tmp="$(mktemp "${d}/.tmp.XXXXXX")" || { emit "FATAL: cannot create temp file in: $d"; exit 2; }
  printf '%s\n' "$content" > "$tmp" || { emit "FATAL: cannot write temp file: $tmp"; rm -f "$tmp"; exit 2; }
  mv -f "$tmp" "$dest" || { emit "FATAL: atomic rename failed: $tmp -> $dest"; rm -f "$tmp"; exit 2; }
}

# valid_id <id> — the accept-set MUST equal poll's scan-set: if register accepts an
# id, poll MUST be able to enumerate it. poll's `for entry in "$REG_DIR"/*` glob
# does NOT match leading-dot files (a stalled ".secret" agent would be invisible —
# silent drop, the giq.1.7 silent-supervision failure), and poll skips the reserved
# ".tmp.*" in-flight-temp namespace (a stalled ".tmp.evil" agent would also vanish).
# So we reject ANY id beginning with '.' — that single rule covers leading-dot ids
# (D-1) AND keeps the ".tmp." temp namespace exclusively atomic_write's, never a
# real id (D-2). We further restrict the charset to [A-Za-z0-9._-] (the glob sees
# all of these), so a first char in [A-Za-z0-9_-] plus any of [A-Za-z0-9._-] after.
valid_id() {
  case "$1" in
    ''|.|..|*/*|*$'\n'*) return 1 ;;   # empty, '.', '..', contains '/' or newline
    .*) return 1 ;;                    # leading dot -> invisible to poll's glob / collides with .tmp. reserved temp namespace
    *[!A-Za-z0-9._-]*) return 1 ;;     # any char outside the glob-visible safe charset
    *) return 0 ;;
  esac
}

require_id() {
  [ -n "${1:-}" ] || { emit "FATAL: <id> is required"; exit 2; }
  valid_id "$1" || { emit "FATAL: invalid agent id (must match [A-Za-z0-9._-], no leading '.', no '/' or newline — an id poll cannot enumerate is a silent drop): $1"; exit 2; }
}

# --- subcommand: register ----------------------------------------------------
cmd_register() {
  id="${1:-}"; shift || true
  require_id "$id"
  cadence=""
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --cadence)   shift; [ "$#" -gt 0 ] || { emit "FATAL: --cadence needs a value"; exit 2; }; cadence="$1" ;;
      --cadence=*) cadence="${1#*=}" ;;
      *)           emit "FATAL: unknown arg to register: $1"; exit 2 ;;
    esac
    shift
  done
  # ADR-0005 #4: missing cadence -> finite default 600; non-numeric / <=0 -> FATAL.
  if [ -z "$cadence" ]; then
    cadence=600
  elif ! is_pos_int "$cadence"; then
    # BUG-1 (ADR-0005 #4 fail-open): a 0/negative/garbage cadence is an infinite
    # silent stall window. A presence-only "did they pass a cadence" check would
    # accept it and never age the agent; we FATAL instead.
    emit "FATAL: --cadence must be a positive integer (got: ${cadence}) — a zero/negative/garbage cadence is an infinite silent stall window"
    exit 2
  fi
  ts="$(now)"
  # last_heartbeat defaults to register_ts so the register-then-never-heartbeat
  # case ages from registration immediately (ADR-0005 decisive property).
  atomic_write "${REG_DIR}/${id}" "register_ts=${ts} cadence=${cadence} last_heartbeat_ts=${ts}"
  emit "registered ${id} (cadence=${cadence}s, register_ts=${ts})"
  exit 0
}

# --- subcommand: heartbeat ---------------------------------------------------
cmd_heartbeat() {
  id="${1:-}"
  require_id "$id"
  entry="${REG_DIR}/${id}"
  [ -f "$entry" ] || { emit "FATAL: heartbeat for unregistered agent: ${id}"; exit 2; }
  # preserve register_ts + cadence, refresh only last_heartbeat_ts.
  line="$(cat "$entry" 2>/dev/null)"
  reg_ts=""; cad=""
  for tok in $line; do
    case "$tok" in
      register_ts=*) reg_ts="${tok#register_ts=}" ;;
      cadence=*)     cad="${tok#cadence=}" ;;
    esac
  done
  if ! is_nonneg_int "$reg_ts" || ! is_pos_int "$cad"; then
    emit "FATAL: registry entry for ${id} is corrupt; cannot heartbeat"
    exit 2
  fi
  ts="$(now)"
  atomic_write "$entry" "register_ts=${reg_ts} cadence=${cad} last_heartbeat_ts=${ts}"
  emit "heartbeat ${id} (last_heartbeat_ts=${ts})"
  exit 0
}

# --- subcommand: close -------------------------------------------------------
cmd_close() {
  id="${1:-}"
  require_id "$id"
  entry="${REG_DIR}/${id}"
  # ADR-0005 #5: remove the entry (do not merely mark) so it stops being scanned.
  rm -f "$entry"
  emit "closed ${id} (entry reaped)"
  exit 0
}

# --- subcommand: poll --------------------------------------------------------
cmd_poll() {
  cur="$(now)"
  if ! is_nonneg_int "$cur"; then
    emit "FATAL: current epoch is non-numeric (WATCHDOG_NOW=${WATCHDOG_NOW:-<unset>})"
    exit 2
  fi

  # Collect registry entries via globbing. The registry dir may legitimately not
  # exist yet (no agent ever registered) -> that is a genuine 0-tracked, not a
  # corrupt state.
  tracked=0
  if [ -d "$REG_DIR" ]; then
    for entry in "$REG_DIR"/*; do
      # glob with no match yields the literal pattern -> skip it.
      [ -e "$entry" ] || continue
      # ignore leftover temp files from an in-flight atomic_write (".tmp.*").
      base="$(basename "$entry")"
      case "$base" in .tmp.*) continue ;; esac
      [ -f "$entry" ] || continue
      tracked=$((tracked + 1))

      line="$(cat "$entry" 2>/dev/null)"
      reg_ts=""; cad=""; last_ts=""
      for tok in $line; do
        case "$tok" in
          register_ts=*)      reg_ts="${tok#register_ts=}" ;;
          cadence=*)          cad="${tok#cadence=}" ;;
          last_heartbeat_ts=*) last_ts="${tok#last_heartbeat_ts=}" ;;
        esac
      done

      # ADR-0005 #1: a corrupt/unparseable entry must fail-closed, NEVER be
      # silently skipped to a vacuous PASS. skipped() -> FATAL (exit 2) via verdict.
      if ! is_nonneg_int "$reg_ts" || ! is_pos_int "$cad" || ! is_nonneg_int "$last_ts"; then
        # BUG-2 (ADR-0005 #1 / CF-1 false-green): an entry that does not parse to a
        # valid (register_ts, cadence>0, last_heartbeat_ts) triple is unmineable.
        # A presence-only "the file exists" check would PASS over it; we fail-closed.
        skipped "registry entry '${base}' is corrupt/unparseable (need register_ts/cadence>0/last_heartbeat_ts): ${line}"
        continue
      fi

      age=$((cur - last_ts))
      if [ "$age" -gt "$cad" ]; then
        # STALLED: last heartbeat is older than the cadence window.
        fail "agent '${base}' STALLED: ${age}s since last heartbeat > cadence ${cad}s (register_ts=${reg_ts}, now=${cur})"
      else
        emit "ok: ${base} healthy (${age}s since heartbeat <= cadence ${cad}s)"
      fi
    done
  fi

  # ADR-0005 #1: a genuine 0-tracked poll is a LOUD PASS — emit so CI logs can
  # tell it apart from "all tracked agents healthy." Silence is never green here.
  if [ "$tracked" -eq 0 ]; then
    emit "0 tracked agents (genuine-empty registry — distinguishable from all-healthy)"
  fi

  verdict
}

# --- dispatch ----------------------------------------------------------------
# ADR-0005 #3: no args == poll, so this script is a drop-in close-audit roster
# constituent that self-triggers at every session boundary.
sub="${1:-poll}"
case "$sub" in
  register)  shift; cmd_register "$@" ;;
  heartbeat) shift; cmd_heartbeat "$@" ;;
  close)     shift; cmd_close "$@" ;;
  poll)      shift; cmd_poll ;;
  -h|--help) sed -n '2,60p' "$0"; exit 0 ;;
  --*)       emit "FATAL: unknown option: ${sub}"; exit 2 ;;
  *)         emit "FATAL: unknown subcommand: ${sub}"; exit 2 ;;
esac
