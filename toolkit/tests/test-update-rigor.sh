#!/usr/bin/env bash
# tests/test-update-rigor.sh — F-007 negative test for scripts/update-rigor.sh
# (the runnable Discipline 11 pull).
#
# The property: a pull is ADOPTED only when the pulled toolkit's own suite passes;
# a RED suite is ROLLED BACK (pre-update toolkit restored, pin unchanged). Up-to-date
# is a no-op. Bad config is FATAL. All cases use throwaway lib+project trees.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

SCRIPT="$TEST_DIR/../scripts/update-rigor.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# ── fixture builders ──────────────────────────────────────────────────────────
# A fake central library at frameworks/rigor with a given VERSION + a toolkit whose
# run-all-tests.sh either passes (rc 0) or fails (rc 1), and a marker file so we can
# tell the copy landed.
make_lib() { # $1 = lib root ; $2 = version ; $3 = pass|fail ; $4 = marker text
  local lib="$1" ver="$2" mode="$3" marker="$4"
  mkdir -p "$lib/frameworks/rigor/toolkit/tests"
  printf '%s\n\n# commentary\n' "$ver" > "$lib/frameworks/rigor/VERSION"
  printf '%s' "$marker" > "$lib/frameworks/rigor/toolkit/MARKER"
  if [ "$mode" = "pass" ]; then
    printf '#!/usr/bin/env bash\nexit 0\n' > "$lib/frameworks/rigor/toolkit/tests/run-all-tests.sh"
  else
    printf '#!/usr/bin/env bash\nexit 1\n' > "$lib/frameworks/rigor/toolkit/tests/run-all-tests.sh"
  fi
  chmod +x "$lib/frameworks/rigor/toolkit/tests/run-all-tests.sh"
}
make_changelog() { # $1 = lib root ; writes a changelog with a hook-introducing entry
  cat > "$1/frameworks/rigor/CHANGELOG.md" <<EOF
# CHANGELOG

## 2.0.0 (2026-07-04) — new gate
Adds hooks/enforce-something.sh, a new boundary gate.

## 1.0.0 (2026-07-01) — base
Initial.
EOF
}
make_project() { # $1 = project root ; $2 = pinned version ; $3 = marker text
  local proj="$1" ver="$2" marker="$3"
  mkdir -p "$proj/toolkit/tests"
  printf '# Project\n\nrigor_version: %s\n' "$ver" > "$proj/CLAUDE.md"
  printf '%s' "$marker" > "$proj/toolkit/MARKER"
  printf '#!/usr/bin/env bash\nexit 0\n' > "$proj/toolkit/tests/run-all-tests.sh"
  chmod +x "$proj/toolkit/tests/run-all-tests.sh"
}
run_update() { # $1 = lib ; $2 = project ; rest = extra args
  local lib="$1" proj="$2"; shift 2
  bash "$SCRIPT" --lib "$lib" --project "$proj" "$@"
}

echo "== update-rigor =="

# ── (1) behind + GREEN pulled suite → ADOPT: toolkit copied, pin bumped, exit 0 ──
L1="$WORK/lib1"; P1="$WORK/proj1"
make_lib "$L1" "2.0.0" pass "CENTRAL-2.0.0"; make_changelog "$L1"
make_project "$P1" "1.0.0" "PROJECT-1.0.0"
expect_exit 0 run_update "$L1" "$P1"
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "CENTRAL-2.0.0" "$P1/toolkit/MARKER" 2>/dev/null \
   && grep -q "rigor_version: 2.0.0" "$P1/CLAUDE.md"; then
  echo "[PASS] behind+GREEN: central toolkit copied AND pin bumped to 2.0.0"
else
  echo "[FAIL] behind+GREEN: expected copied toolkit + bumped pin (marker=$(cat "$P1/toolkit/MARKER" 2>/dev/null); pin=$(grep rigor_version "$P1/CLAUDE.md"))"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ── (2) behind + RED pulled suite → ROLLBACK: FAIL(1), toolkit restored, pin UNCHANGED ──
# THE core F-007 property: a failing pulled toolkit is not adopted.
L2="$WORK/lib2"; P2="$WORK/proj2"
make_lib "$L2" "2.0.0" fail "CENTRAL-BAD-2.0.0"; make_changelog "$L2"
make_project "$P2" "1.0.0" "PROJECT-ORIG-1.0.0"
expect_exit 1 run_update "$L2" "$P2"
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "PROJECT-ORIG-1.0.0" "$P2/toolkit/MARKER" 2>/dev/null \
   && grep -q "rigor_version: 1.0.0" "$P2/CLAUDE.md" \
   && ! grep -q "CENTRAL-BAD" "$P2/toolkit/MARKER" 2>/dev/null; then
  echo "[PASS] behind+RED: rolled back — original toolkit restored, pin stayed 1.0.0"
else
  echo "[FAIL] behind+RED: expected rollback (marker=$(cat "$P2/toolkit/MARKER" 2>/dev/null); pin=$(grep rigor_version "$P2/CLAUDE.md"))"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Core guard-fires proof: the SAME pull adopts on GREEN and rolls back on RED.
LG="$WORK/libG"; PG="$WORK/projG"; LB="$WORK/libB"; PB="$WORK/projB"
make_lib "$LG" "2.0.0" pass "G"; make_project "$PG" "1.0.0" "orig"
make_lib "$LB" "2.0.0" fail "B"; make_project "$PB" "1.0.0" "orig"
assert_red_when_guard_removed \
  "bash '$SCRIPT' --lib '$LG' --project '$PG'" \
  "bash '$SCRIPT' --lib '$LB' --project '$PB'"

# ── (3) up-to-date (pinned == latest) → no-op, exit 0, nothing copied ──
L3="$WORK/lib3"; P3="$WORK/proj3"
make_lib "$L3" "2.0.0" pass "CENTRAL-2.0.0"
make_project "$P3" "2.0.0" "PROJECT-UNCHANGED"
expect_exit 0 run_update "$L3" "$P3"
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "PROJECT-UNCHANGED" "$P3/toolkit/MARKER" 2>/dev/null; then
  echo "[PASS] up-to-date: no-op, project toolkit untouched"
else
  echo "[FAIL] up-to-date: toolkit was modified"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ── (3b) pinned AHEAD of latest → no-op, exit 0 ──
L3b="$WORK/lib3b"; P3b="$WORK/proj3b"
make_lib "$L3b" "1.5.0" pass "C"; make_project "$P3b" "2.0.0" "AHEAD"
expect_exit 0 run_update "$L3b" "$P3b"

# ── (4) --dry-run behind → exit 0, NO change (toolkit + pin untouched) ──
L4="$WORK/lib4"; P4="$WORK/proj4"
make_lib "$L4" "2.0.0" pass "CENTRAL-2.0.0"; make_changelog "$L4"
make_project "$P4" "1.0.0" "PROJECT-DRYRUN"
expect_exit 0 run_update "$L4" "$P4" --dry-run
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "PROJECT-DRYRUN" "$P4/toolkit/MARKER" 2>/dev/null \
   && grep -q "rigor_version: 1.0.0" "$P4/CLAUDE.md"; then
  echo "[PASS] dry-run: nothing changed (marker + pin intact)"
else
  echo "[FAIL] dry-run mutated state"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ── (5) FATAL classes → exit 2 ──
expect_exit 2 bash "$SCRIPT" --lib "$WORK/nope" --project "$P1"           # no central lib
L5="$WORK/lib5"; make_lib "$L5" "2.0.0" pass "C"
expect_exit 2 bash "$SCRIPT" --lib "$L5" --project "$WORK/no-such-proj"   # no project toolkit
# pin file with no rigor_version line → FATAL
P6="$WORK/proj6"; mkdir -p "$P6/toolkit/tests"; printf '# no pin here\n' > "$P6/CLAUDE.md"
printf '#!/usr/bin/env bash\nexit 0\n' > "$P6/toolkit/tests/run-all-tests.sh"
expect_exit 2 bash "$SCRIPT" --lib "$L5" --project "$P6"

# ── (6) CONTAINMENT (security HIGH): a `../` --toolkit pointing OUTSIDE the project →
# FATAL(2), and the outside dir is NOT deleted (the rm -rf never runs). Make the victim
# a valid-looking toolkit so ONLY the containment guard stops it.
L6="$WORK/lib6"; make_lib "$L6" "2.0.0" pass "C"; make_changelog "$L6"
P7="$WORK/proj7"; make_project "$P7" "1.0.0" "PROJ7"
VICTIM="$WORK/victim"; mkdir -p "$VICTIM/tests"
printf 'PRECIOUS' > "$VICTIM/wallet.txt"
printf '#!/usr/bin/env bash\nexit 0\n' > "$VICTIM/tests/run-all-tests.sh"
expect_exit 2 bash "$SCRIPT" --lib "$L6" --project "$P7" --toolkit ../victim
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "PRECIOUS" "$VICTIM/wallet.txt" 2>/dev/null; then
  echo "[PASS] containment: ../ --toolkit rejected, outside dir NOT deleted"
else
  echo "[FAIL] containment: the outside victim dir was destroyed by a ../ --toolkit"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ── (6b) a --toolkit dir under the project that is NOT a rigor toolkit → FATAL(2) ──
mkdir -p "$P7/notatoolkit"; printf 'data' > "$P7/notatoolkit/x"
expect_exit 2 bash "$SCRIPT" --lib "$L6" --project "$P7" --toolkit notatoolkit
TESTS_RUN=$((TESTS_RUN + 1))
grep -q "data" "$P7/notatoolkit/x" 2>/dev/null \
  && echo "[PASS] not-a-toolkit dir refused (no run-all-tests.sh), not deleted" \
  || { echo "[FAIL] a non-toolkit dir under the project was deleted"; TESTS_FAILED=$((TESTS_FAILED + 1)); }

# ── (7) pin anchoring + case (bug/security MEDIUM): only the FIRST line that STARTS
# with rigor_version is bumped; an inline prose mention is NOT clobbered; a capitalized
# pin is handled. ──
L7="$WORK/lib7"; make_lib "$L7" "2.0.0" pass "CENTRAL-2.0.0"; make_changelog "$L7"
P8="$WORK/proj8"; mkdir -p "$P8/toolkit/tests"
printf '#!/usr/bin/env bash\nexit 0\n' > "$P8/toolkit/tests/run-all-tests.sh"
printf '# Project\n\nWe historically pinned rigor_version: 0.5.0 in an old note.\nRigor_Version: 1.0.0\n' > "$P8/CLAUDE.md"
expect_exit 0 run_update "$L7" "$P8"
TESTS_RUN=$((TESTS_RUN + 1))
if grep -q "historically pinned rigor_version: 0.5.0" "$P8/CLAUDE.md" \
   && grep -Eq "^[Rr]igor_[Vv]ersion: 2.0.0" "$P8/CLAUDE.md"; then
  echo "[PASS] pin anchoring: capitalized pin bumped to 2.0.0, inline prose (0.5.0) untouched"
else
  echo "[FAIL] pin anchoring/case (file: $(grep -i rigor_version "$P8/CLAUDE.md" | tr '\n' '|'))"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ── (8) SIGNAL during the destructive window (bug HIGH): SIGTERM mid-gate → the
# pre-update toolkit is RESTORED, the pin stays. Central gate sleeps so the kill lands
# inside the window. ──
if command -v sleep >/dev/null 2>&1; then
  L8="$WORK/lib8"; mkdir -p "$L8/frameworks/rigor/toolkit/tests"
  printf '2.0.0\n' > "$L8/frameworks/rigor/VERSION"
  printf 'CENTRAL-SLOW' > "$L8/frameworks/rigor/toolkit/MARKER"
  printf '#!/usr/bin/env bash\nsleep 3\nexit 0\n' > "$L8/frameworks/rigor/toolkit/tests/run-all-tests.sh"
  chmod +x "$L8/frameworks/rigor/toolkit/tests/run-all-tests.sh"
  make_changelog "$L8"
  P9="$WORK/proj9"; make_project "$P9" "1.0.0" "PROJ9-ORIGINAL"
  bash "$SCRIPT" --lib "$L8" --project "$P9" >/dev/null 2>&1 &
  UPID=$!
  sleep 1                         # let it reach the sleeping gate (after rm+cp)
  kill -TERM "$UPID" 2>/dev/null
  wait "$UPID" 2>/dev/null
  TESTS_RUN=$((TESTS_RUN + 1))
  if grep -q "PROJ9-ORIGINAL" "$P9/toolkit/MARKER" 2>/dev/null \
     && grep -q "rigor_version: 1.0.0" "$P9/CLAUDE.md" \
     && ! grep -q "CENTRAL-SLOW" "$P9/toolkit/MARKER" 2>/dev/null; then
    echo "[PASS] SIGTERM mid-pull: toolkit restored, pin unchanged (no half-update)"
  else
    echo "[FAIL] SIGTERM mid-pull left a half-updated/broken toolkit (marker=$(cat "$P9/toolkit/MARKER" 2>/dev/null); pin=$(grep rigor_version "$P9/CLAUDE.md" 2>/dev/null))"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
else
  echo "[SKIP] signal test: sleep unavailable" >&2
fi

# ── (9) toolkit PORTABILITY (ur-qa production-path): the design-fixture tests must
# LOUD-SKIP (exit 0) when run from a COPIED toolkit whose REPO resolves to a checkout
# with no designs/fixtures/ — else a real pull's acceptance gate always goes RED and the
# update NEVER adopts. Copy the real toolkit into a consuming layout (<proj>/toolkit, so
# the tests' 4-up REPO lands on a fixture-less ancestor), drop heavy node_modules to stay
# fast, and assert each design test skips (exit 0). A regression (removing the skip guard)
# makes these FAIL in a consuming project. ──
REAL_TOOLKIT="$TEST_DIR/.."
if [ -d "$REAL_TOOLKIT/tests" ]; then
  PORT="$WORK/port/proj/toolkit"
  mkdir -p "$WORK/port/proj"
  cp -R "$REAL_TOOLKIT" "$PORT" 2>/dev/null
  find "$PORT" -name node_modules -type d -prune -exec rm -rf {} + 2>/dev/null
  find "$PORT" -name dist -type d -prune -exec rm -rf {} + 2>/dev/null
  for dt in test-pen-integrity test-wiring-gate test-seam-gate test-res3-gate; do
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -f "$PORT/tests/$dt.sh" ]; then
      if bash "$PORT/tests/$dt.sh" >/dev/null 2>&1; then
        echo "[PASS] portability: $dt loud-skips from a fixture-less copy (pull can adopt)"
      else
        echo "[FAIL] portability: $dt does NOT skip when designs/fixtures/ is absent — a real pull would roll back forever"
        TESTS_FAILED=$((TESTS_FAILED + 1))
      fi
    else
      echo "[PASS] portability: $dt not present in this toolkit (n/a)"
    fi
  done
else
  echo "[SKIP] portability: real toolkit tests dir not found" >&2
fi

test_summary
