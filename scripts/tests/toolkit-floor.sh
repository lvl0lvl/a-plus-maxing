#!/usr/bin/env bash
# toolkit-floor.sh — run the vendored toolkit negative-test floor
# (toolkit/tests/test-*.sh) with a loud + stale-guarded exclusion of the ONE
# tracked library-tree-scoped false-red, so close-audit passes NATIVELY without
# the off-label CLOSE_AUDIT_FLOORS test hook (bead a-plus-maxing-23q5).
#
# WHY an exclusion is needed: the vendored toolkit ships test-roster-select.sh
# (bead a-plus-maxing-ffit) whose line-141 git-range smoke hardcodes a `../`
# depth valid ONLY for the library's own frameworks/rigor/toolkit/ nesting.
# a-plus vendors the toolkit at the repo root, so that walk overshoots into a
# non-git parent and the test correctly FATALs — while roster-select.sh ITSELF
# works in a-plus (verified: --files + real-range classify). It is a false-red on
# a path-depth assumption, not a real audit failure. The durable ROOT fix is
# upstream (ffit: resolve the repo root via `git rev-parse --show-toplevel`);
# when it lands and a-plus re-pulls, roster-select passes, stale-guard (b) below
# FAILS this floor, and the exclusion must be removed — it cannot rot silently.
# The vendored runner (toolkit/tests/run-all-tests.sh) has no exclusion of its
# own and is NEVER edited (that forks the pull line), so this a-plus twin adds it.
#
# NAMESPACE / not the a-plus floor: this floor owns ONLY the toolkit `test-*.sh`
# namespace. The a-plus floor (scripts/tests/run-all-tests.sh, `test_*.sh`) is
# separate and keeps its own CLOSE_AUDIT_FLOOR_EXCLUDE / RUN_ALL_TESTS_EXCLUDE
# escape hatch. This floor deliberately does NOT read that shared env var: a
# single exclusion value forwarded to two disjoint-namespace floors cross-fires
# each floor's stale-guard on the other's names (bead 23q5 review, finding F1).
# A future tracked TOOLKIT red is excluded by adding its basename to
# DEFAULT_EXCLUDE below — a reviewed code edit, stale-guarded — NOT via an env var.
#
# F-007 IS PRESERVED: every OTHER toolkit negative test runs and any real failure
# REDs this floor. Only the ONE documented, bead-tracked false-red is excluded,
# and only while it is genuinely red (stale-guard (b)).
#
# Stale-guarded TWO ways (NEVER silent — F-009): (a) an excluded name that no
# longer exists (deleted/renamed) fails the run; (b) an excluded test that now
# PASSES fails the run. Both scoped to this floor's `test-*.sh` namespace.
#
# Test hooks (NOT production — both are on close-audit's SEC-002 warning list):
#   TOOLKIT_FLOOR_DIR              override the test-discovery dir (fixture dir),
#                                  mirroring the a-plus floor's RUN_ALL_TESTS_DIR
#   TOOLKIT_FLOOR_DEFAULT_EXCLUDE  override the seeded default exclusion. The `-`
#                                  (not `:-`) form below is DELIBERATE: an
#                                  explicit EMPTY value means "no exclusion" (the
#                                  negative test's no-exclusion cases depend on
#                                  it; `:-` would wrongly re-inject the default).
#
# Exit: 0 all non-excluded pass + every exclusion still valid / 1 otherwise.
set -uo pipefail

# Recursion guard (mirror toolkit/tests/run-all-tests.sh): a toolkit test that
# invokes close-audit must not re-enter the floor.
export CLOSE_AUDIT_SKIP_SUITE=1

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SELF_DIR/../.." && pwd)"
TESTS_DIR="${TOOLKIT_FLOOR_DIR:-$REPO_ROOT/toolkit/tests}"

# The tracked pre-existing false-red(s), seeded so a bare close needs no env.
# Add a future tracked toolkit red here (reviewed, stale-guarded); remove ffit
# when the upstream fix lands + a-plus re-pulls (stale-guard (b) forces it).
DEFAULT_EXCLUDE="${TOOLKIT_FLOOR_DEFAULT_EXCLUDE-test-roster-select.sh}"
EXCLUDE_REASON="ffit: library-tree-scoped test-roster-select.sh (hardcoded ../ depth); roster-select.sh works in a-plus; upstream fix = git rev-parse --show-toplevel"
EXCLUDE=" ${DEFAULT_EXCLUDE} "

is_excluded() { case "$EXCLUDE" in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

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
      echo "[toolkit-floor] EXCLUDED  $b — $EXCLUDE_REASON"
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
# silent cap that no longer applies must not pass quietly. Scoped to this floor's
# own `test-*.sh` namespace: a name that is not a toolkit test basename belongs
# to another floor and is not this floor's stale concern (so a mis-seeded foreign
# name is a no-op, never a cross-floor stale RED).
for ex in $DEFAULT_EXCLUDE; do
  case "$ex" in test-*.sh) ;; *) continue ;; esac
  if [ ! -e "$TESTS_DIR/$ex" ]; then
    echo "[toolkit-floor] STALE-EXCLUSION  $ex — no such toolkit test (deleted/renamed); remove the exclusion"
    failed=$((failed + 1)); failed_names+=("stale-missing:$ex")
  fi
done

echo "[toolkit-floor] RESULT: ${passed} passed, ${failed} failed, ${excluded} excluded"
if [ "$failed" -ne 0 ]; then
  printf '[toolkit-floor] failed: %s\n' "${failed_names[@]}"
  exit 1
fi
exit 0
