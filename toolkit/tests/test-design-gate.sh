#!/usr/bin/env bash
# test-design-gate.sh — F-007 proof for the design [MECH] gate (scripts/design-gate.sh).
#
# Proves the gate goes RED in the dangerous direction (a blocking design finding BLOCKS;
# a UI change with no runnable detector FAILS CLOSED) and GREEN when safe (clean / advisory
# / off / disabled / non-UI). Driven by a node-free FAKE detector so the gate's classify +
# fail-closed logic is exercised deterministically without impeccable or node. A final
# smoke runs the REAL vendored detector when node + the vendor are present.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GATE="$HERE/../scripts/design-gate.sh"

# The gate classifies findings with python3; skip cleanly where it can't run (the gate
# itself FATALs without python3, so this is honest, not a hidden pass).
if ! command -v python3 >/dev/null 2>&1; then
  echo "[skip] test-design-gate: python3 absent (the gate's classifier needs it) — skipping"
  exit 0
fi

TMP="$(mktemp -d 2>/dev/null || mktemp -d -t designgate)"; trap 'rm -rf "$TMP"' EXIT

# --- node-free fake detector: emits canned --json findings keyed by filename marker ---
FAKE="$TMP/fake-detect.sh"
cat > "$FAKE" <<'FK'
#!/usr/bin/env bash
out="["; first=1
for a in "$@"; do
  [ "$a" = "--json" ] && continue
  case "$a" in
    *blocking*) sev=warning;  ap=side-tab;             nm="Side-tab accent border" ;;
    *advisory*) sev=advisory; ap=design-system-color;  nm="Color outside DESIGN.md" ;;
    *)          continue ;;   # clean files contribute no findings
  esac
  [ "$first" -eq 1 ] || out="$out,"
  first=0
  out="$out{\"antipattern\":\"$ap\",\"name\":\"$nm\",\"severity\":\"$sev\",\"file\":\"$a\",\"line\":1,\"snippet\":\"x\"}"
done
printf '%s]' "$out"
FK
chmod +x "$FAKE"

PASS=0; FAIL=0
expect_exit() { local exp="$1"; shift; "$@" >/dev/null 2>&1; local rc=$?
  if [ "$rc" = "$exp" ]; then echo "[PASS] exit $exp: $*"; PASS=$((PASS+1));
  else echo "[FAIL] expected $exp, got $rc: $*"; FAIL=$((FAIL+1)); fi; }

# fixtures (content irrelevant; the fake keys on filename)
echo '<div></div>' > "$TMP/blocking.html"
echo '<div></div>' > "$TMP/advisory.html"
echo '<div></div>' > "$TMP/clean.html"
echo 'x = 1'       > "$TMP/notui.py"

# --- the F-007 matrix (fake detector) ---
# 1. blocking warning + default → FAIL (the core RED proof)
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 1 bash "$GATE" "$TMP/blocking.html"
# 2. clean → PASS
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 0 bash "$GATE" "$TMP/clean.html"
# 3. advisory-only + default → PASS (reported, not blocking)
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 0 bash "$GATE" "$TMP/advisory.html"
# 4. advisory-only + block-all → FAIL (the dial tightens)
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-all expect_exit 1 bash "$GATE" "$TMP/advisory.html"
# 5. blocking + off → PASS (never blocks)
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=off expect_exit 0 bash "$GATE" "$TMP/blocking.html"
# 6. non-UI file → PASS (nothing to scan)
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 0 bash "$GATE" "$TMP/notui.py"
# 7. UI change + detector MISSING + default → FATAL (fail-closed; F-008)
RIGOR_DESIGN_DETECTOR="/no/such/detector" RIGOR_DESIGN_GATE=block-warning expect_exit 2 bash "$GATE" "$TMP/blocking.html"
# 8. UI change + detector missing + off → PASS (off tolerates a missing detector)
RIGOR_DESIGN_DETECTOR="/no/such/detector" RIGOR_DESIGN_GATE=off expect_exit 0 bash "$GATE" "$TMP/blocking.html"
# 9. disabled → PASS even with a blocking file
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=disabled expect_exit 0 bash "$GATE" "$TMP/blocking.html"
# 10. bad mode → FATAL
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=bogus expect_exit 2 bash "$GATE" "$TMP/blocking.html"

# --- real-detector smoke (skip cleanly if node or the vendored detector is absent) ---
REAL=""
for c in "$HERE/../../../../vendor/impeccable/scripts/detect.mjs" \
         "$HOME/.claude/skills_library/vendor/impeccable/scripts/detect.mjs"; do
  [ -f "$c" ] && { REAL="$c"; break; }
done
if command -v node >/dev/null 2>&1 && [ -n "$REAL" ]; then
  # Consumer portability: with the 1.15.0 cascade preflight, a machine WITHOUT the vendor
  # deps would FATAL these full-tier cases (suite 31/1 → /update-rigor rollback on fresh
  # consumers — observed in the 1.16.0 review). The slop fixture's tells are regex-tier
  # (side-tab + gradient-text), so when deps are unloadable run the smoke at the explicit
  # regex-only tier instead of failing: same RED/GREEN direction, honestly reduced scope.
  if (cd "$(dirname "$REAL")" && node --input-type=module -e 'await Promise.all(["htmlparser2","css-select","css-tree","domutils"].map(m=>import(m)))' >/dev/null 2>&1); then
    SMOKE_TIER=full
  else
    echo "[note] cascade deps not installed next to $REAL — real-detector smoke runs at regex-only tier"
    SMOKE_TIER=regex-only
  fi
  printf '<section style="border-left:4px solid #7c3aed"><h1 style="background:linear-gradient(90deg,#7c3aed,#06b6d4);-webkit-background-clip:text;color:transparent">x</h1></section>' > "$TMP/realslop.html"
  RIGOR_DESIGN_DETECTOR="$REAL" RIGOR_DESIGN_GATE=block-warning RIGOR_DESIGN_GATE_TIER="$SMOKE_TIER" expect_exit 1 bash "$GATE" "$TMP/realslop.html"
  printf '<h1 style="color:#111;background:#fff">clean</h1>' > "$TMP/realclean.html"
  RIGOR_DESIGN_DETECTOR="$REAL" RIGOR_DESIGN_GATE=block-warning RIGOR_DESIGN_GATE_TIER="$SMOKE_TIER" expect_exit 0 bash "$GATE" "$TMP/realclean.html"
else
  echo "[skip] real-detector smoke (node or vendor/impeccable absent) — fake-detector matrix above covers the gate logic"
fi

# --- cascade-tier preflight (F-008; bead cat) --------------------------------
# The impeccable static-html cascade engine dynamically imports htmlparser2/css-select/
# css-tree/domutils and SILENTLY degrades to the regex tier when they're absent —
# verified by execution 2026-07-04: a dep-less run missed every contrast finding and
# the JSON carries no tier marker. Pre-hardening, the gate PASSED (0) a pure contrast
# failure whenever the deps were missing; these cases pin the FATAL and the explicit
# regex-only opt-out. Hermetic: the dep-less detector is a TMP COPY of the vendored
# scripts tree (no node_modules anywhere up the TMP path) — the repo vendor dir is
# never touched.
if command -v node >/dev/null 2>&1 && [ -n "$REAL" ]; then
  # low-contrast-only fixture: clean for the regex tier, dirty for the cascade tier —
  # exactly the finding class the silent degradation loses.
  printf '<p style="color:#cccccc;background:#ffffff;padding:16px">barely readable</p>' > "$TMP/lowcontrast.html"

  cp -R "$(dirname "$REAL")" "$TMP/depless-scripts"
  DEPLESS="$TMP/depless-scripts/detect.mjs"

  # Hermetic probe (QA review 1.15.0; blind-verify extended it to case 16): cases 11-12 and
  # 16 assume NO node_modules resolves up the TMP ancestry. If one unexpectedly does, they'd
  # fail LOUD (exit 1 ≠ expected) — safe direction but cryptic; loud-skip with a diagnostic
  # instead. (13/14/15/17 are hermeticity-independent — verified in the blind pass.)
  if (cd "$TMP/depless-scripts" && node --input-type=module -e 'await Promise.all(["htmlparser2","css-select","css-tree","domutils"].map(m=>import(m)))' >/dev/null 2>&1); then
    echo "[skip] cases 11-12,16: a node_modules up the TMP ancestry makes the dep-less copy loadable (non-hermetic environment)"
  else
  # 11. deps unloadable + default tier → FATAL (the core RED: pre-hardening this was 0)
  RIGOR_DESIGN_DETECTOR="$DEPLESS" RIGOR_DESIGN_GATE=block-warning expect_exit 2 bash "$GATE" "$TMP/lowcontrast.html"
  # 12. deps unloadable + regex-only → PASS (reduced scope accepted EXPLICITLY) — and the
  #     stderr NOTE is a tested contract, not decoration: assert it, so deleting the echo
  #     goes RED (QA review 1.15.0: the message contract had no test).
  TESTS_ERR="$(RIGOR_DESIGN_DETECTOR="$DEPLESS" RIGOR_DESIGN_GATE=block-warning RIGOR_DESIGN_GATE_TIER=regex-only \
    bash "$GATE" "$TMP/lowcontrast.html" 2>&1 >/dev/null)"; rc12=$?
  if [ "$rc12" = 0 ] && printf '%s' "$TESTS_ERR" | grep -q 'regex-only: dep preflight skipped'; then
    echo "[PASS] case 12: regex-only exit 0 + reduced-scope NOTE on stderr"; PASS=$((PASS+1))
  else
    echo "[FAIL] case 12: rc=$rc12 stderr='$TESTS_ERR'"; FAIL=$((FAIL+1))
  fi
  # 16. symlinked detect.mjs into the dep-less tree → still FATAL. Pre-canonicalization the
  #     lexical dirname missed the engine file, the preflight silently skipped, and the gate
  #     PASSed (sec review 1.15.0: reproduced fail-open — the exact hazard this guard closes).
  #     Inside the hermetic guard: shares 11-12's dep-less assumption (blind-verify note).
  mkdir -p "$TMP/symdir" && ln -s "$DEPLESS" "$TMP/symdir/detect.mjs"
  RIGOR_DESIGN_DETECTOR="$TMP/symdir/detect.mjs" RIGOR_DESIGN_GATE=block-warning expect_exit 2 bash "$GATE" "$TMP/lowcontrast.html"
  fi
  # 13. deps unloadable + off → PASS (off tolerates an unrunnable tier, like a missing detector)
  RIGOR_DESIGN_DETECTOR="$DEPLESS" RIGOR_DESIGN_GATE=off expect_exit 0 bash "$GATE" "$TMP/lowcontrast.html"
  # 14. bad tier value → FATAL — against the FAKE detector, which cannot FATAL on its own,
  #     so exit 2 can ONLY come from tier validation (bug-hunt review 1.15.0: the DEPLESS
  #     detector made this case tautological — its preflight FATALed regardless).
  RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE_TIER=bogus expect_exit 2 bash "$GATE" "$TMP/clean.html"
  # 17. custom node detector WITHOUT the cascade engine → exempt from the preflight (clause d;
  #     QA review 1.15.0: the exemption had no test — a regression dropping the engine-file
  #     check would falsely FATAL every custom detector).
  printf 'console.log("[]")\n' > "$TMP/custom-noengine.mjs"
  RIGOR_DESIGN_DETECTOR="$TMP/custom-noengine.mjs" RIGOR_DESIGN_GATE=block-warning expect_exit 0 bash "$GATE" "$TMP/lowcontrast.html"

  # 15. deps LOADABLE (repo vendor) → the cascade tier actually catches the contrast
  #     failure and blocks (1). Loud-skip when the vendor deps aren't installed —
  #     without this case a broken preflight could FATAL everything and look "safe".
  if (cd "$(dirname "$REAL")" && node --input-type=module -e 'await Promise.all(["htmlparser2","css-select","css-tree","domutils"].map(m=>import(m)))' >/dev/null 2>&1); then
    RIGOR_DESIGN_DETECTOR="$REAL" RIGOR_DESIGN_GATE=block-warning expect_exit 1 bash "$GATE" "$TMP/lowcontrast.html"
  else
    echo "[skip] cascade-deps-present case (vendor node_modules not installed: cd vendor/impeccable && npm install --no-save css-tree htmlparser2 css-select domutils)"
  fi
else
  echo "[skip] cascade-tier preflight cases (node or vendor/impeccable absent)"
fi

# --- 48d: the UI class is single-sourced — a gate whose lib is MISSING must FATAL, ---
# --- never silently decide nothing is UI (F-008). Scratch copy, repo untouched.      ---
LIBLESS="$TMP/libless"
mkdir -p "$LIBLESS/scripts" "$LIBLESS/lib"
cp "$GATE" "$LIBLESS/scripts/design-gate.sh"
# lib deliberately NOT copied
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 2 bash "$LIBLESS/scripts/design-gate.sh" "$TMP/blocking.html"
# control: with the lib present the same copy classifies normally (goes RED if the
# FATAL branch were wrongly unconditional)
cp "$HERE/../lib/ui-class.sh" "$LIBLESS/lib/ui-class.sh"
RIGOR_DESIGN_DETECTOR="$FAKE" RIGOR_DESIGN_GATE=block-warning expect_exit 1 bash "$LIBLESS/scripts/design-gate.sh" "$TMP/blocking.html"

# --- 48d: the command-doc quotes of the UI class are guarded copies — each doc's ---
# --- quoted regex must equal the lib's RIGOR_UI_RE, or "that file wins" prose is  ---
# --- adjudicating a divergence nothing detects (drift test).                      ---
LIB_RE="$(. "$HERE/../lib/ui-class.sh"; printf '%s' "$RIGOR_UI_RE")"
REPO_ROOT="$HERE/../../../.."
for doc in "$REPO_ROOT/commands/review-pr.md" "$REPO_ROOT/commands/execute-plan.md"; do
  if [ -f "$doc" ]; then
    if grep -qF "$LIB_RE" "$doc"; then
      PASS=$((PASS+1)); echo "PASS: $(basename "$doc") quotes the lib's UI class verbatim"
    else
      FAIL=$((FAIL+1)); echo "FAIL: $(basename "$doc") UI-class quote drifted from lib/ui-class.sh"
    fi
  fi
done

echo "----"
echo "design-gate test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = 0 ]
