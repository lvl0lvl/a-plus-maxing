#!/usr/bin/env bash
# design-gate.sh — per-recipe DESIGN [MECH] gate (impeccable integration, touchpoint ②).
#
# Runs the impeccable detector over changed UI files and fails CLOSED on blocking design
# findings — the design counterpart to a failing test in the recipe verification gate.
# Hardens impeccable's own advisory PostToolUse hook into a blocking gate.
#
# Exit contract (mirrors the toolkit's 0=PASS / 1=FAIL / 2=FATAL convention):
#   0  PASS   — no UI files to scan, OR clean, OR only advisory findings (reported, not blocking)
#   1  FAIL   — one or more BLOCKING design findings
#   2  FATAL  — the gate could not run (no detector, bad config, detector errored, no python3,
#              UI-class lib missing or empty).
#              A gate that did not run did not pass (F-008): do NOT treat a FATAL as clean.
#
# Config (env):
#   RIGOR_DESIGN_GATE   block-warning (default) | block-all | off | disabled
#       block-warning : block on severity=warning (real defects + strong AI tells); severity=
#                       advisory (design-system drift, repeated kickers, numbered markers) is
#                       reported but does NOT block. Strict on the objective, advisory on taste.
#       block-all     : block on ANY finding (warning or advisory).
#       off           : never block; report ALL findings as advisories (visibility only).
#       disabled      : skip the gate entirely (for projects with no UI surface).
#   RIGOR_DESIGN_DETECTOR  path to impeccable's detect.mjs (or any executable that emits the
#       same `--json` finding array). Fallbacks, in order:
#         $RIGOR_DESIGN_DETECTOR
#         ~/.claude/skills_library/vendor/impeccable/scripts/detect.mjs   (the anchor)
#         ${CLAUDE_PROJECT_DIR:-.}/vendor/impeccable/scripts/detect.mjs
#         ./vendor/impeccable/scripts/detect.mjs
#   RIGOR_DESIGN_GATE_TIER  full (default) | regex-only
#       full       : when the resolved detector ships impeccable's static-html CASCADE engine,
#                    require its deps (htmlparser2/css-select/css-tree/domutils) to be loadable
#                    — else FATAL. The engine dynamically imports them and SILENTLY degrades to
#                    the regex tier when they're absent (verified by execution 2026-07-04: a
#                    dep-less run missed every contrast finding, and the JSON carries no tier
#                    marker). A gate that scanned with a silently-degraded detector did not run
#                    the check it claims to run (F-008).
#       regex-only : skip the dep preflight and stop ASSERTING the cascade tier ran — the gate
#                    says so on every run. Findings then reflect whatever tier the detector
#                    could load: cascade if the deps happen to be present, regex-only (contrast
#                    checks LOST) if they are absent. The mode cannot force the detector down a
#                    tier — impeccable selects its tier purely by dep-loadability.
#       Scope: the preflight covers node-run detectors (*.mjs|*.js|*.cjs|*.mts). Any other
#       detector is executed directly (the test-fake mechanism) and is outside the preflight
#       contract. The detector path is canonicalized (realpath) first, so a symlinked
#       detect.mjs cannot dodge the engine check (fail-open otherwise — sec review 1.15.0).
#
# Usage: design-gate.sh [file_or_dir ...]    (no args → changed UI files from `git diff`)
set -euo pipefail

MODE="${RIGOR_DESIGN_GATE:-block-warning}"
case "$MODE" in
  block-warning|block-all|off|disabled) ;;
  *) echo "design-gate: FATAL — bad RIGOR_DESIGN_GATE='$MODE' (block-warning|block-all|off|disabled)" >&2; exit 2 ;;
esac
[ "$MODE" = "disabled" ] && { echo "design-gate: disabled — skipped"; exit 0; }

TIER="${RIGOR_DESIGN_GATE_TIER:-full}"
case "$TIER" in
  full|regex-only) ;;
  *) echo "design-gate: FATAL — bad RIGOR_DESIGN_GATE_TIER='$TIER' (full|regex-only)" >&2; exit 2 ;;
esac

# The UI class is single-sourced (bead 48d): toolkit/lib/ui-class.sh owns it. A gate
# that cannot load the definition of "UI" must not silently decide nothing is UI (F-008).
UI_CLASS_LIB="$(CDPATH= cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../lib/ui-class.sh"
if [ ! -f "$UI_CLASS_LIB" ]; then
  [ "$MODE" = "off" ] && { echo "design-gate: ui-class lib missing; off → skipped"; exit 0; }
  echo "design-gate: FATAL — toolkit/lib/ui-class.sh missing; the UI class is undefined (F-008)" >&2
  exit 2
fi
# shellcheck source=../lib/ui-class.sh
. "$UI_CLASS_LIB"
if [ -z "${RIGOR_UI_RE:-}" ]; then
  [ "$MODE" = "off" ] && { echo "design-gate: ui-class lib defines no RIGOR_UI_RE; off → skipped"; exit 0; }
  echo "design-gate: FATAL — ui-class.sh loaded but RIGOR_UI_RE is undefined (F-008)" >&2
  exit 2
fi
UI_RE="$RIGOR_UI_RE"

# --- collect candidate UI files (args, or git-changed) ---
cand=()
if [ "$#" -gt 0 ]; then
  for a in "$@"; do
    if [ -d "$a" ]; then
      while IFS= read -r f; do [ -n "$f" ] && cand+=("$f"); done < <(find "$a" -type f 2>/dev/null | grep -E "$UI_RE" || true)
    else
      cand+=("$a")
    fi
  done
else
  while IFS= read -r f; do [ -n "$f" ] && cand+=("$f"); done < <(git diff --name-only HEAD 2>/dev/null | grep -E "$UI_RE" || true)
fi

ui=()
for f in ${cand[@]+"${cand[@]}"}; do
  printf '%s\n' "$f" | grep -qE "$UI_RE" && [ -f "$f" ] && ui+=("$f")
done

if [ "${#ui[@]}" -eq 0 ]; then echo "design-gate: no UI files to scan — PASS"; exit 0; fi

# --- resolve the detector ---
# An EXPLICITLY-set RIGOR_DESIGN_DETECTOR must exist: a missing configured path is a
# misconfiguration, not a cue to silently fall back to a different detector. Discovery
# fallbacks apply only when it is unset.
det="${RIGOR_DESIGN_DETECTOR:-}"
if [ -n "$det" ]; then
  if [ ! -f "$det" ]; then
    [ "$MODE" = "off" ] && { echo "design-gate: configured detector '$det' missing; off → skipped"; exit 0; }
    echo "design-gate: FATAL — RIGOR_DESIGN_DETECTOR='$det' does not exist. A gate that did not run did not pass (F-008)." >&2
    exit 2
  fi
else
  for c in "$HOME/.claude/skills_library/vendor/impeccable/scripts/detect.mjs" \
           "${CLAUDE_PROJECT_DIR:-.}/vendor/impeccable/scripts/detect.mjs" \
           "./vendor/impeccable/scripts/detect.mjs"; do
    [ -f "$c" ] && { det="$c"; break; }
  done
  if [ -z "$det" ]; then
    [ "$MODE" = "off" ] && { echo "design-gate: no detector found; off → skipped"; exit 0; }
    echo "design-gate: FATAL — impeccable detector not found (set RIGOR_DESIGN_DETECTOR). A gate that did not run did not pass (F-008)." >&2
    exit 2
  fi
fi

command -v python3 >/dev/null 2>&1 || { echo "design-gate: FATAL — python3 required (path canonicalization + finding classification)" >&2; exit 2; }

# --- run the detector (node extensions via node; anything else executed directly so tests can fake it) ---
case "$det" in
  *.mjs|*.js|*.cjs|*.mts)
    command -v node >/dev/null 2>&1 || { echo "design-gate: FATAL — node required to run $det" >&2; exit 2; }
    # Canonicalize BEFORE deriving the directory: node resolves a symlinked detect.mjs to
    # its realpath, so a lexical dirname would check for the engine (and resolve deps) in
    # the wrong tree — the preflight would silently skip while the real detector degrades
    # (sec review 1.15.0: reproduced fail-open). python3 realpath resolves the full chain
    # (file symlinks included) where `cd && pwd -P` resolves directories only.
    det="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$det")"
    # Cascade-tier preflight (F-008; bead cat). Applies only when the resolved detector
    # ships impeccable's cascade engine — a custom RIGOR_DESIGN_DETECTOR without it is
    # exempt by construction, not by guesswork.
    cascade_engine="$(dirname "$det")/detector/engines/static-html/detect-html.mjs"
    if [ "$TIER" = "regex-only" ]; then
      echo "design-gate: NOTE — RIGOR_DESIGN_GATE_TIER=regex-only: dep preflight skipped; findings reflect whatever tier the detector could load (regex-only, contrast checks LOST, when deps are absent)" >&2
    elif [ -f "$cascade_engine" ]; then
      if ! (cd "$(dirname "$det")" && node --input-type=module -e 'await Promise.all(["htmlparser2","css-select","css-tree","domutils"].map(m=>import(m)))' >/dev/null 2>&1); then
        [ "$MODE" = "off" ] && { echo "design-gate: cascade-tier deps unloadable; off → skipped"; exit 0; }
        echo "design-gate: FATAL — cascade-tier deps (htmlparser2/css-select/css-tree/domutils) are not loadable next to $det; the detector would SILENTLY degrade to regex-only and skip every contrast check. Install them: (cd <vendor>/impeccable && npm install --no-save css-tree htmlparser2 css-select domutils) — or accept the reduced scope explicitly with RIGOR_DESIGN_GATE_TIER=regex-only. A gate that did not run did not pass (F-008)." >&2
        exit 2
      fi
    fi
    if out="$(node "$det" --json ${ui[@]+"${ui[@]}"} 2>/dev/null)"; then rc=0; else rc=$?; fi ;;
  *)
    if out="$("$det" --json ${ui[@]+"${ui[@]}"} 2>/dev/null)"; then rc=0; else rc=$?; fi ;;
esac
# impeccable detect.mjs: 0 = clean, 2 = findings. Any OTHER code means it could not run.
if [ "$rc" != "0" ] && [ "$rc" != "2" ]; then
  echo "design-gate: FATAL — detector exited $rc (could not run)" >&2; exit 2
fi

# --- classify by tier, report, exit fail-closed ---
set +e
printf '%s' "$out" | RIGOR_DESIGN_GATE="$MODE" python3 -c '
import sys, os, json
mode = os.environ.get("RIGOR_DESIGN_GATE", "block-warning")
try:
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        raise ValueError("not an array")
except Exception:
    sys.stderr.write("design-gate: FATAL — detector output was not a JSON array (could not run)\n")
    sys.exit(2)

def is_block(f):
    if mode == "off":       return False
    if mode == "block-all": return True
    return f.get("severity") == "warning"          # block-warning (default)

block = [f for f in data if is_block(f)]
adv   = [f for f in data if not is_block(f)]
def line(f):
    return "  [%s] %s — %s:%s  %s" % (f.get("severity","?"), f.get("antipattern","?"),
                                      f.get("file","?"), f.get("line","?"), f.get("name",""))
if adv:
    sys.stderr.write("design-gate: %d advisory finding(s) (non-blocking):\n%s\n" % (len(adv), "\n".join(line(f) for f in adv)))
if block:
    sys.stderr.write("design-gate: FAIL — %d blocking design finding(s):\n%s\n" % (len(block), "\n".join(line(f) for f in block)))
    sys.exit(1)
sys.stderr.write("design-gate: PASS — no blocking design findings\n")
sys.exit(0)
'
exit $?
