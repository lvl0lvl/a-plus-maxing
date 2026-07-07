#!/usr/bin/env bash
# test_toolkit_floor.sh — negative test for scripts/tests/toolkit-floor.sh
# (bead a-plus-maxing-23q5). The F-007 obligation: this floor only counts as
# enforcing once it PROVES it goes RED on bad input. Cases:
#   (1) only a documented-excluded test is red        -> floor PASSES (exit 0)
#   (2) an un-excluded test fails                      -> floor REDs  (exit 1)  [F-007]
#   (3) an excluded test now PASSES (stale-guard b)    -> floor REDs  (exit 1)
#   (4) an excluded name no longer exists (guard a)    -> floor REDs  (exit 1)
#   (5) clean dir, no exclusion                        -> floor PASSES (exit 0)
#   (6) red dir, no exclusion                          -> floor REDs  (exit 1)
# Fixtures live in a temp dir reached via the TOOLKIT_FLOOR_DIR test hook, so the
# live toolkit floor is never touched.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLOOR="$HERE/toolkit-floor.sh"
pass=0; fail=0
ok()  { echo "  PASS: $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL: $1"; fail=$((fail + 1)); }
mktest() { printf '#!/usr/bin/env bash\nexit %s\n' "$2" > "$1"; chmod +x "$1"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# (1) only the excluded test is red -> exit 0
d="$TMP/excl-red"; mkdir -p "$d"
mktest "$d/test-good.sh" 0
mktest "$d/test-roster-select.sh" 1
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="test-roster-select.sh" bash "$FLOOR" >/dev/null 2>&1; then
  ok "only the documented-excluded test red -> floor PASSES (exit 0)"
else
  bad "excluded-red should pass but floor failed"
fi

# (2) an un-excluded failure -> exit 1 (F-007: real reds bite)
d="$TMP/unexcl-fail"; mkdir -p "$d"
mktest "$d/test-real-red.sh" 1
mktest "$d/test-roster-select.sh" 1
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="test-roster-select.sh" bash "$FLOOR" >/dev/null 2>&1; then
  bad "un-excluded failure should RED the floor but it passed (F-007 broken)"
else
  ok "un-excluded failure REDs the floor (exit 1) — F-007 intact"
fi

# (3) stale-guard (b): excluded test now PASSES -> exit 1
d="$TMP/stale-pass"; mkdir -p "$d"
mktest "$d/test-roster-select.sh" 0
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="test-roster-select.sh" bash "$FLOOR" >/dev/null 2>&1; then
  bad "stale exclusion (excluded test now passes) should RED but floor passed"
else
  ok "stale-exclusion (excluded test now passes) REDs the floor (exit 1)"
fi

# (4) stale-guard (a): excluded name no longer exists -> exit 1
d="$TMP/stale-missing"; mkdir -p "$d"
mktest "$d/test-good.sh" 0
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="test-gone.sh" bash "$FLOOR" >/dev/null 2>&1; then
  bad "stale exclusion (missing excluded name) should RED but floor passed"
else
  ok "stale-exclusion (excluded name no longer exists) REDs the floor (exit 1)"
fi

# (5) clean dir, no exclusion -> exit 0
d="$TMP/clean"; mkdir -p "$d"
mktest "$d/test-good.sh" 0
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="" bash "$FLOOR" >/dev/null 2>&1; then
  ok "clean dir with no exclusion -> floor PASSES (exit 0)"
else
  bad "clean dir should pass but floor failed"
fi

# (6) red dir, no exclusion -> exit 1
d="$TMP/red"; mkdir -p "$d"
mktest "$d/test-bad.sh" 1
if TOOLKIT_FLOOR_DIR="$d" TOOLKIT_FLOOR_DEFAULT_EXCLUDE="" bash "$FLOOR" >/dev/null 2>&1; then
  bad "red dir with no exclusion should RED but floor passed"
else
  ok "red dir with no exclusion REDs the floor (exit 1)"
fi

echo "test_toolkit_floor: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
