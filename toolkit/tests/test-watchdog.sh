#!/usr/bin/env bash
# tests/test-watchdog.sh — the F-007 negative test for watchdog.sh (ADR-0005).
#
# F-007 obligation: an audit that cannot prove it FAILs on bad input does not
# count as enforcing anything. `poll` is the runtime complement to the dispatch
# heartbeat hook: the hook guarantees the liveness CLAUSE is present, `poll`
# enforces that the heartbeats the clause promises actually ARRIVE. So the
# load-bearing cases (each from ADR-0005 Validation Approach) are:
#
#   STALLED:   register, advance time past cadence WITHOUT a heartbeat -> poll
#              STALLED, exit 1 (the register-then-never-heartbeat / drop-at-t=0
#              worst case a heartbeat-mtime-only design structurally misses).
#   FRESH:     register + fresh heartbeat within cadence -> poll PASS, exit 0.
#   CLOSED:    register + close -> that agent is no longer scanned -> poll PASS.
#   CORRUPT:   an unparseable registry entry -> poll fail-closed (FATAL/STALLED,
#              exit >=1), NEVER a vacuous empty-loop exit 0 (the CF-1 false-green
#              disease, F-008).
#   EMPTY:     zero tracked agents -> exit 0 BUT a loud "0 tracked" line on
#              stdout/stderr, so genuine-empty is distinguishable from all-healthy.
#   BADCADENCE: register --cadence 0 / non-numeric -> FATAL config error, exit 2
#              (a degenerate cadence is an infinite silent-stall window — fail-OPEN).
#   GUARD:     stub stall-detection so poll always exits 0 -> the test goes RED
#              (assert_red_when_guard_removed).
#
# Hermetic + deterministic: each case points CLAUDE_PROJECT_DIR at a fresh mktemp
# dir and controls "time" via the WATCHDOG_NOW epoch-override seam — no real sleeps.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

WD="${TEST_DIR}/../scripts/watchdog.sh"

# Each case gets an isolated project dir so the per-agent registry files never
# collide. Cleaned on exit so the repo tree stays clean (bead mtz convention).
ROOT="$(mktemp -d "${TMPDIR:-/tmp}/watchdog-fix.XXXXXX")"
trap 'rm -rf "$ROOT"' EXIT

# fresh_proj <name> -> echoes a fresh, empty CLAUDE_PROJECT_DIR for that case.
fresh_proj() {
  d="$ROOT/$1"
  rm -rf "$d"
  mkdir -p "$d"
  printf '%s' "$d"
}

# --- STALLED: register, no heartbeat, now past cadence -> exit 1 -------------
P_STALL="$(fresh_proj stalled)"
CLAUDE_PROJECT_DIR="$P_STALL" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
# t=1000+301 > 1000+300 cadence: registered-then-never-heartbeat is now STALLED.
expect_exit 1 env CLAUDE_PROJECT_DIR="$P_STALL" WATCHDOG_NOW=1301 bash "$WD" poll

# --- FRESH: register + heartbeat within cadence -> exit 0 --------------------
P_FRESH="$(fresh_proj fresh)"
CLAUDE_PROJECT_DIR="$P_FRESH" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
CLAUDE_PROJECT_DIR="$P_FRESH" WATCHDOG_NOW=1250 bash "$WD" heartbeat a1 >/dev/null 2>&1
# t=1250+100 < 1250+300: fresh, healthy.
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_FRESH" WATCHDOG_NOW=1350 bash "$WD" poll

# --- CLOSED: register + close -> not flagged (and registry now empty=loud 0) -
P_CLOSE="$(fresh_proj closed)"
CLAUDE_PROJECT_DIR="$P_CLOSE" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
CLAUDE_PROJECT_DIR="$P_CLOSE" WATCHDOG_NOW=1000 bash "$WD" close a1 >/dev/null 2>&1
# Even far past the cadence, a closed agent is not scanned -> PASS.
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_CLOSE" WATCHDOG_NOW=99999 bash "$WD" poll

# --- CLOSED-among-live: one of two agents closed, the live one healthy -------
P_MIX="$(fresh_proj mixed)"
CLAUDE_PROJECT_DIR="$P_MIX" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
CLAUDE_PROJECT_DIR="$P_MIX" WATCHDOG_NOW=1000 bash "$WD" register a2 --cadence 300 >/dev/null 2>&1
CLAUDE_PROJECT_DIR="$P_MIX" WATCHDOG_NOW=1000 bash "$WD" close a1 >/dev/null 2>&1
# a1 closed (would be stalled if scanned); a2 fresh -> PASS.
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_MIX" WATCHDOG_NOW=1200 bash "$WD" poll

# --- CORRUPT: an unparseable registry entry -> fail-closed (exit >=1) --------
# Worst case: a genuinely corrupt (not torn) entry must never be silently
# skipped to PASS. We expect FATAL (exit 2) — a check that cannot run does not
# pass. The expect_exit helper asserts the exact code; we use a wrapper that
# accepts ">=1" by asserting it is NOT 0.
P_CORRUPT="$(fresh_proj corrupt)"
CLAUDE_PROJECT_DIR="$P_CORRUPT" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
# Clobber the entry with garbage that cannot parse as the registry record shape.
printf 'this is not a valid registry record\n' > "$P_CORRUPT/.rigor/watchdog/a1"
expect_not_zero() {
  TESTS_RUN=$((TESTS_RUN + 1))
  "$@" >/dev/null 2>&1
  actual=$?
  if [ "$actual" != "0" ]; then
    echo "[PASS] expect_not_zero (got $actual): $*"
  else
    echo "[FAIL] expect_not_zero but got 0 (vacuous PASS on corrupt entry): $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}
expect_not_zero env CLAUDE_PROJECT_DIR="$P_CORRUPT" WATCHDOG_NOW=1100 bash "$WD" poll

# --- EMPTY: zero tracked agents -> exit 0 AND a loud "0 tracked" line --------
P_EMPTY="$(fresh_proj empty)"
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_EMPTY" WATCHDOG_NOW=1000 bash "$WD" poll
# The green must be distinguishable from "all healthy": a loud 0-tracked emit.
assert_output_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qiE "$pattern"; then
    echo "[PASS] output matches /$pattern/"
  else
    echo "[FAIL] output lacked /$pattern/: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}
assert_output_contains "0 tracked" env CLAUDE_PROJECT_DIR="$P_EMPTY" WATCHDOG_NOW=1000 bash "$WD" poll

# --- BADCADENCE: non-numeric or <=0 cadence -> FATAL config error, exit 2 ----
P_BAD1="$(fresh_proj badcad1)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_BAD1" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 0
P_BAD2="$(fresh_proj badcad2)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_BAD2" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence abc
P_BAD3="$(fresh_proj badcad3)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_BAD3" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence -5

# --- DEFAULT cadence: omitted -> finite 600 default (still ages) -------------
P_DEF="$(fresh_proj defcad)"
CLAUDE_PROJECT_DIR="$P_DEF" WATCHDOG_NOW=1000 bash "$WD" register a1 >/dev/null 2>&1
# within default 600 -> healthy
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_DEF" WATCHDOG_NOW=1500 bash "$WD" poll
# past default 600 -> stalled (an omitted cadence still has a finite window)
P_DEF2="$(fresh_proj defcad2)"
CLAUDE_PROJECT_DIR="$P_DEF2" WATCHDOG_NOW=1000 bash "$WD" register a1 >/dev/null 2>&1
expect_exit 1 env CLAUDE_PROJECT_DIR="$P_DEF2" WATCHDOG_NOW=1700 bash "$WD" poll

# --- ROSTER: no-args invocation behaves as `poll` (close-audit constituent) --
# Stalled agent, run with NO subcommand -> must FAIL exit 1 (so close blocks).
P_ROSTER="$(fresh_proj roster)"
CLAUDE_PROJECT_DIR="$P_ROSTER" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
expect_exit 1 env CLAUDE_PROJECT_DIR="$P_ROSTER" WATCHDOG_NOW=1400 bash "$WD"

# --- GUARD: assert the test goes RED if stall-detection is stubbed to exit 0 -
# good = a healthy/empty poll (exit 0); bad = the SAME stalled scenario the real
# poll must FAIL on. If a stub forced poll to always exit 0, bad would be 0 and
# this assertion would (correctly) go RED.
P_GOOD="$(fresh_proj guard_good)"
P_BADG="$(fresh_proj guard_bad)"
CLAUDE_PROJECT_DIR="$P_BADG" WATCHDOG_NOW=1000 bash "$WD" register a1 --cadence 300 >/dev/null 2>&1
assert_red_when_guard_removed \
  "CLAUDE_PROJECT_DIR='$P_GOOD' WATCHDOG_NOW=1000 bash '$WD' poll" \
  "CLAUDE_PROJECT_DIR='$P_BADG' WATCHDOG_NOW=1400 bash '$WD' poll"

# --- SILENTDROP: accept-set must equal scan-set (D-1 / D-2 regression) -------
# The asymmetry that watchdog exists to eliminate (giq.1.7 silent supervision):
# an id register ACCEPTS but poll cannot SEE is a silent drop -> vacuous "0 tracked"
# PASS while a real agent is stalled. poll's glob skips leading-dot files, and poll
# reserves the ".tmp.*" temp namespace, so BOTH of these MUST be rejected at register.
#
# D-1: a leading-dot id is invisible to poll's `for entry in "$REG_DIR"/*` glob.
P_SECRET="$(fresh_proj secret)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_SECRET" WATCHDOG_NOW=1000 bash "$WD" register .secret --cadence 300
# REJECTED means the registry stays empty -> a subsequent poll is a genuine loud 0.
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_SECRET" WATCHDOG_NOW=1000 bash "$WD" poll
assert_output_contains "0 tracked" env CLAUDE_PROJECT_DIR="$P_SECRET" WATCHDOG_NOW=1000 bash "$WD" poll

# D-2: a ".tmp.*" id collides with poll's reserved in-flight-temp namespace.
P_TMPEVIL="$(fresh_proj tmpevil)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_TMPEVIL" WATCHDOG_NOW=1000 bash "$WD" register .tmp.evil --cadence 300
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_TMPEVIL" WATCHDOG_NOW=1000 bash "$WD" poll
assert_output_contains "0 tracked" env CLAUDE_PROJECT_DIR="$P_TMPEVIL" WATCHDOG_NOW=1000 bash "$WD" poll

# Charset closure: a leading-dot variant and an out-of-charset id are also rejected,
# while a legal id with INTERNAL dots/underscores/hyphens is still accepted (no
# over-tightening that would break real ids).
P_DOTHID="$(fresh_proj dothidden)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_DOTHID" WATCHDOG_NOW=1000 bash "$WD" register .hidden --cadence 300
P_BADCHR="$(fresh_proj badchar)"
expect_exit 2 env CLAUDE_PROJECT_DIR="$P_BADCHR" WATCHDOG_NOW=1000 bash "$WD" register 'a b' --cadence 300
P_LEGAL="$(fresh_proj legalid)"
expect_exit 0 env CLAUDE_PROJECT_DIR="$P_LEGAL" WATCHDOG_NOW=1000 bash "$WD" register agent.1_worker-2 --cadence 300

# --- BELT-AND-SUSPENDERS: no accepted id is invisible to poll ----------------
# Stronger than the per-case rejects: PROVE the accept-set is a SUBSET of the
# scan-set. For every candidate id, if `valid_id`/register ACCEPTS it (exit 0),
# then a registered-then-stalled instance of it MUST be flagged by poll (exit 1).
# A silent drop is the failure: register accepts but poll exits 0 (vacuous green).
P_INV="$(fresh_proj invariant)"
silentdrop_failures=0
for cand in a1 normal agent.1 a_b a-b .secret .tmp.evil .hidden .. . 'a/b' '.x'; do
  d="$ROOT/inv-$(printf '%s' "$cand" | tr -c 'A-Za-z0-9' _)"
  rm -rf "$d"; mkdir -p "$d"
  CLAUDE_PROJECT_DIR="$d" WATCHDOG_NOW=1000 bash "$WD" register "$cand" --cadence 300 >/dev/null 2>&1
  reg_rc=$?
  if [ "$reg_rc" = "0" ]; then
    # ACCEPTED -> poll, well past cadence, MUST see it stalled (exit 1). If poll
    # exits 0 here, register accepted an id poll cannot scan == the silent drop.
    CLAUDE_PROJECT_DIR="$d" WATCHDOG_NOW=9999 bash "$WD" poll >/dev/null 2>&1
    poll_rc=$?
    if [ "$poll_rc" != "1" ]; then
      echo "  silent-drop: register ACCEPTED '$cand' but poll did not flag it stalled (poll exit $poll_rc)"
      silentdrop_failures=$((silentdrop_failures + 1))
    fi
  fi
done
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$silentdrop_failures" -eq 0 ]; then
  echo "[PASS] accept-set is a subset of scan-set (no id register accepts is invisible to poll)"
else
  echo "[FAIL] $silentdrop_failures accepted id(s) were invisible to poll (silent drop)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

test_summary
