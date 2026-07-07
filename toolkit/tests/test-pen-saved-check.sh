#!/usr/bin/env bash
# tests/test-pen-saved-check.sh — F-007 negative test for scripts/pen-saved-check.sh
# (spec §5 amendment PA-5; bead skills_library-b30 — the saved-state precondition).
#
# The property under test: extraction from UNSAVED editor state cannot pass the
# precondition. arm records the disk state; verify PASSes only if a write landed
# after arming (sha changed, or same bytes with newer mtime); check PASSes only
# if the disk still matches the verified sha at stamp time. Every "could not
# check" input is FATAL (2), never a pass (F-008).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

SCRIPT="$TEST_DIR/../scripts/pen-saved-check.sh"

PROJ="$(mktemp -d)"
trap 'rm -rf "$PROJ"' EXIT
PEN="$PROJ/design.pen"
WITNESS="$PROJ/.rigor/pen-save-witness.json"

run() { # $1 = subcommand ; $2 = pen path
  CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" "$1" "$2"
}

echo "== pen-saved-check =="

# ── FATALs: a check that cannot run does not pass ─────────────────────────────
# arm on an absent .pen → FATAL (2).
expect_exit 2 run arm "$PEN"

# arm on a symlink → FATAL (2), repo-residency invariant (lstat, non-traversing).
printf 'PENBYTES-v1' > "$PROJ/real.pen"
ln -s "$PROJ/real.pen" "$PROJ/link.pen"
expect_exit 2 run arm "$PROJ/link.pen"

# arm on an a-plus-maxing path → FATAL (2), NEW-5 denylist (lexical).
mkdir -p "$PROJ/a-plus-maxing"
printf 'X' > "$PROJ/a-plus-maxing/x.pen"
expect_exit 2 run arm "$PROJ/a-plus-maxing/x.pen"

# a-plus denylist, BASE-JOINED form (D2): a lexically-clean RELATIVE pen under an
# a-plus-rooted PROJECT_DIR must FATAL — the literal argument alone is blind to it.
# Anchored on the guard-EXCLUSIVE stderr message: with the branch removed the call
# still exits 2 via the file-absence FATAL (blind-verify caught the tautology), but
# only the denylist branch says "base-joined penPath".
assert_stderr_contains "base-joined penPath" \
  env CLAUDE_PROJECT_DIR="$PROJ/a-plus-maxing" bash "$SCRIPT" arm x.pen

# verify with no witness → FATAL (2).
printf 'PENBYTES-v1' > "$PEN"
expect_exit 2 run verify "$PEN"

# ── the core F-007 pair: unsaved state CANNOT pass ────────────────────────────
# arm → (no save) → verify must FAIL (1). Same arm → simulated save → PASS (0).
expect_exit 0 run arm "$PEN"
expect_exit 1 run verify "$PEN"          # nothing written since arm → FAIL

# The FAIL is single-sided: after a simulated save (bytes change), verify PASSes.
expect_exit 0 run arm "$PEN"
printf 'PENBYTES-v2-saved' > "$PEN"      # simulated editor save (bytes differ)
expect_exit 0 run verify "$PEN"

# assert_red_when_guard_removed: the SAME command sequence with the save (good)
# vs without it (bad) — proves the guard is the save-detection, not scaffolding.
assert_red_when_guard_removed \
  "CLAUDE_PROJECT_DIR='$PROJ' bash '$SCRIPT' arm '$PEN' && printf 'v3-more-bytes' >> '$PEN' && CLAUDE_PROJECT_DIR='$PROJ' bash '$SCRIPT' verify '$PEN'" \
  "CLAUDE_PROJECT_DIR='$PROJ' bash '$SCRIPT' arm '$PEN' && CLAUDE_PROJECT_DIR='$PROJ' bash '$SCRIPT' verify '$PEN'"

# Rewrite of IDENTICAL bytes with a newer mtime still counts as a witnessed save
# (a no-op save proves editor==disk). Advance the mtime RELATIVE to now (D6: an
# absolute future date was a time-bomb — once the wall clock passed it, the
# "newer" mtime would read older than arm's and this case would invert).
expect_exit 0 run arm "$PEN"
sleep 1; touch "$PEN"                    # same bytes, mtime advanced past arm's
expect_exit 0 run verify "$PEN"

# verify PASS emits the verified sha for the extractor to stamp (a promised
# diagnostic — F-007 applied to messages).
expect_exit 0 run arm "$PEN"
printf 'v4' >> "$PEN"
TESTS_RUN=$((TESTS_RUN + 1))
OUT="$(CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" verify "$PEN" 2>/dev/null)"
WANT_SHA="$(shasum -a 256 "$PEN" | awk '{print $1}')"
if printf '%s' "$OUT" | grep -q "pen-sha256: $WANT_SHA"; then
  echo "[PASS] verify emits the verified pen-sha256"
else
  echo "[FAIL] verify did not emit 'pen-sha256: $WANT_SHA' (got: $OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# verify is single-shot: a second verify without re-arm → FATAL (2).
expect_exit 2 run verify "$PEN"

# ── check: the verify→stamp gap ───────────────────────────────────────────────
# check right after verify (disk unchanged) → PASS (0), AND it must emit the
# verified pen-sha256 (D9: the extractor stamps the value check emits — an
# unasserted emission is a silent-regression surface).
TESTS_RUN=$((TESTS_RUN + 1))
CHECK_OUT="$(CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" check "$PEN" 2>/dev/null)"; CHECK_RC=$?
CHECK_SHA="$(shasum -a 256 "$PEN" | awk '{print $1}')"
if [ "$CHECK_RC" -eq 0 ] && printf '%s' "$CHECK_OUT" | grep -q "pen-sha256: $CHECK_SHA"; then
  echo "[PASS] check PASSes and emits the verified pen-sha256"
else
  echo "[FAIL] check rc=$CHECK_RC or missing 'pen-sha256: $CHECK_SHA' (got: $CHECK_OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# check against a DIFFERENT pen than the witness verified → FATAL (2). Pins
# check's own path-match guard (D8): without it, check on any byte-identical
# file false-PASSes the stamp gate — the exact drift-at-birth this tool closes.
printf 'OTHERBYTES' > "$PROJ/other2.pen"
expect_exit 2 run check "$PROJ/other2.pen"

# check after the disk moved post-verify → FAIL (1): stamp would describe the
# wrong bytes; re-run verify.
printf 'v5-late-save' >> "$PEN"
expect_exit 1 run check "$PEN"

# check without a verified witness (state=armed) → FATAL (2).
expect_exit 0 run arm "$PEN"
expect_exit 2 run check "$PEN"

# ── witness integrity ─────────────────────────────────────────────────────────
# Witness for a DIFFERENT pen path → FATAL (2), both verify and check.
expect_exit 0 run arm "$PEN"
printf 'OTHER' > "$PROJ/other.pen"
expect_exit 2 run verify "$PROJ/other.pen"

# Garbage witness → FATAL (2).
printf 'not json at all' > "$WITNESS"
expect_exit 2 run verify "$PEN"

# Witness with unparseable pre_mtime → FATAL (2), never a pass (the numeric
# guard: an erroring arithmetic test must not skip the FAIL branch).
printf '{"format":"pen-save-witness-v0","state":"armed","pen_path":"%s","pre_sha256":"deadbeef","pre_mtime":"NaN","armed_ts":"1"}\n' "$PEN" > "$WITNESS"
expect_exit 2 run verify "$PEN"

# Unknown subcommand → FATAL (2).
expect_exit 2 run frobnicate "$PEN"

# Usage guard (D10): fewer than 2 args → FATAL (2), for both arities.
expect_exit 2 env CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" arm
expect_exit 2 env CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT"

# GNU-stat leg (D1): under a shimmed GNU stat (-c %Y works; -f prints an FS-info
# block to STDOUT and exits 1 — the real coreutils shape), the protocol must work
# end-to-end. A BSD-first `||` chain captures the -f garbage (command substitution
# retains the failed branch's stdout), corrupts the witness at arm, and this pair
# goes RED.
SHIM="$PROJ/gnushim"; mkdir -p "$SHIM"
cat > "$SHIM/stat" <<'SHIMEOF'
#!/bin/bash
# -c %Y answers with the file's REAL epoch, delegating to whichever real-stat
# variant AND location this host has: macOS /usr/bin/stat (BSD), most Linuxes
# /usr/bin/stat, alpine /bin/stat (blind-verify round-2 catch — the real stat's
# PATH must not be hardcoded any more than its dialect).
if [ "$1" = "-c" ]; then
  shift; [ "$1" = "%Y" ] && shift; [ "$1" = "--" ] && shift
  RS=/usr/bin/stat; [ -x "$RS" ] || RS=/bin/stat
  m="$("$RS" -f %m -- "$1" 2>/dev/null)"
  case "$m" in ''|*[!0-9]*) m="$("$RS" -c %Y -- "$1" 2>/dev/null)";; esac
  case "$m" in ''|*[!0-9]*) exit 1;; esac
  printf '%s\n' "$m"; exit 0
elif [ "$1" = "-f" ]; then
  echo '  File: "x" ID: 0 Namelen: 255 Type: overlayfs'; exit 1
fi
exit 1
SHIMEOF
chmod +x "$SHIM/stat"
expect_exit 0 env PATH="$SHIM:$PATH" CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" arm "$PEN"
printf 'gnu-save' >> "$PEN"
expect_exit 0 env PATH="$SHIM:$PATH" CLAUDE_PROJECT_DIR="$PROJ" bash "$SCRIPT" verify "$PEN"

test_summary
