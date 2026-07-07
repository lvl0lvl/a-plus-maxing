#!/usr/bin/env bash
# toolkit-floor.sh — run the vendored toolkit negative-test floor
# (toolkit/tests/test-*.sh) with the a-plus exclusion discipline (bead
# a-plus-maxing-23q5). The a-plus twin of toolkit/tests/run-all-tests.sh with
# the same loud + stale-guarded exclusion the a-plus floor (run-all-tests.sh)
# already carries — because the VENDORED runner has NO exclusion of its own
# (it ignores RUN_ALL_TESTS_EXCLUDE), so close-audit's CLOSE_AUDIT_FLOOR_EXCLUDE
# could not reach the toolkit floor. This wrapper closes that gap without
# editing the vendored runner (never edit the vendored toolkit — it would fork
# the pull line).
#
# WHY an exclusion is needed at all: the vendored toolkit ships a library-tree-
# scoped test (test-roster-select.sh, bead a-plus-maxing-ffit) whose line-141
# git-range smoke hardcodes a `../` depth valid ONLY for the library's own
# `frameworks/rigor/toolkit/` nesting. a-plus vendors the toolkit at the repo
# root, so that walk overshoots into a non-git parent and the test correctly
# FATALs — while roster-select.sh ITSELF works in a-plus (verified: --files and
# real-range classify correctly). It is a false-red on a path-depth assumption,
# not a real audit failure. The durable ROOT fix is upstream (ffit: resolve the
# repo root via `git rev-parse --show-toplevel`); once it lands and a-plus
# re-pulls, roster-select passes and stale-guard (b) below FAILS this floor,
# forcing the exclusion's removal — it cannot rot silently.
#
# F-007 IS PRESERVED: every OTHER toolkit negative test runs, and any real
# failure REDs this floor. Only the ONE documented, bead-tracked false-red is
# excluded, and only while it is genuinely red.
#
# Exclusions (NEVER silent — F-009 "no silent caps"):
#   DEFAULT_EXCLUDE (below)      the tracked ffit red, seeded so a bare close
#                                needs no env. Remove it when ffit lands.
#   RUN_ALL_TESTS_EXCLUDE        space-separated ADDITIONAL toolkit test
#                                basenames (the SAME env close-audit forwards to
#                                the a-plus floor — so CLOSE_AUDIT_FLOOR_EXCLUDE
#                                now reaches BOTH floors identically)
#   RUN_ALL_TESTS_EXCLUDE_REASON reason string printed for env exclusions
# An exclusion is stale-guarded TWO ways: (a) an excluded name that no longer
# exists fails the run; (b) an excluded test that now PASSES fails the run.
#
# Test hook (NOT production): TOOLKIT_FLOOR_DIR overrides the discovery dir so
# the exclusion / stale logic can be tested against a fixture dir (F9), mirroring
# the a-plus floor's RUN_ALL_TESTS_DIR.
#
# Exit: 0 all non-excluded pass + every exclusion still valid / 1 otherwise.
set -uo pipefail

# Recursion guard (mirror toolkit/tests/run-all-tests.sh): a toolkit test that
# invokes close-audit must not re-enter the floor.
export CLOSE_AUDIT_SKIP_SUITE=1

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SELF_DIR/../.." && pwd)"
TESTS_DIR="${TOOLKIT_FLOOR_DIR:-$REPO_ROOT/toolkit/tests}"

# The tracked pre-existing false-red, seeded so a bare close needs no env.
# When ffit lands + a-plus re-pulls, remove this (stale-guard (b) will force it).
DEFAULT_EXCLUDE="${TOOLKIT_FLOOR_DEFAULT_EXCLUDE-test-roster-select.sh}"
DEFAULT_REASON="ffit: library-tree-scoped test-roster-select.sh (hardcoded ../ depth); roster-select.sh works in a-plus; upstream fix = git rev-parse --show-toplevel"

ENV_EXCLUDE="${RUN_ALL_TESTS_EXCLUDE:-}"
ENV_REASON="${RUN_ALL_TESTS_EXCLUDE_REASON:-no reason given}"
ALL_EXCLUDE=" ${DEFAULT_EXCLUDE} ${ENV_EXCLUDE} "

is_excluded()   { case "$ALL_EXCLUDE" in *" $1 "*) return 0 ;; *) return 1 ;; esac; }
reason_for()    { case " ${DEFAULT_EXCLUDE} " in *" $1 "*) printf '%s' "$DEFAULT_REASON" ;; *) printf '%s' "$ENV_REASON" ;; esac; }

passed=0; failed=0; excluded=0; failed_names=()

for t in "$TESTS_DIR"/test-*.sh; do
  [ -e "$t" ] || continue
  b="$(basename "$t")"
  if is_excluded "$b"; then
    # stale-guard (b): an excluded test that now PASSES means the red is fixed.
    if bash "$t" >/dev/null 2>&1; then
      echo "[toolkit-floor] STALE-EXCLUSION  $b — now PASSES; remove the exclusion (the red is fixed)"
      failed=$((failed + 1)); failed_names+=("stale-pass:$b")
    else
      echo "[toolkit-floor] EXCLUDED  $b — $(reason_for "$b")"
      excluded=$((excluded + 1))
    fi
    continue
  fi
  if bash "$t" >/dev/null 2>&1; then
    echo "[toolkit-floor] PASS  $b"; passed=$((passed + 1))
  else
    echo "[toolkit-floor] FAIL  $b"; failed=$((failed + 1)); failed_names+=("$b")
  fi
done

# stale-guard (a): an excluded name that does not exist (deleted/renamed) — a
# silent cap that no longer applies must not pass quietly.
for ex in $DEFAULT_EXCLUDE $ENV_EXCLUDE; do
  if [ ! -e "$TESTS_DIR/$ex" ]; then
    echo "[toolkit-floor] STALE-EXCLUSION  $ex — no such test (deleted/renamed); remove the exclusion"
    failed=$((failed + 1)); failed_names+=("stale-missing:$ex")
  fi
done

echo "[toolkit-floor] RESULT: ${passed} passed, ${failed} failed, ${excluded} excluded"
if [ "$failed" -ne 0 ]; then
  printf '[toolkit-floor] failed: %s\n' "${failed_names[@]}"
  exit 1
fi
exit 0
