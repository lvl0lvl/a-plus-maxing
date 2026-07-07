#!/usr/bin/env bash
# toolkit/scripts/seam-gate.sh — the §6.4 seam gate (mock→code structural carry).
#
# Compares the wiring-manifest wireIds against the data-oids collected by a POST-HYDRATION,
# statechart-driven crawl of the BUILT app (harness-substrate-memo §4). This bash entry OWNS
# the contract; the crawl itself is the quarantined node/Playwright harness (harness/pen-
# harness.mjs). The static gates (pen-lint, pen-integrity, wiring-gate) stay node-free — the
# node dependency lives ONLY in the two runtime gates (this + §6.3 res-3, task #45).
#
# WHAT THIS BASH ENTRY OWNS (memo §4): arg parsing; the §6.2 export-integrity HARD DEPENDENCY;
# the node/Playwright presence check (FATAL, never a silent skip — F-008); PEN-CHANGED
# propagation; running the harness; and the VERDICT (set-compare over observations.json, in
# embedded python — the pen-lint/wiring-gate idiom, node just replaces python for the runtime
# crawl STEP).
#
# THE CRAWL (harness): walks each machine from `initial`, induces every documented state
# (modals via portals, tabs, error/empty states), and UNIONs data-oids across states, querying
# the WHOLE document (portal roots included). It writes observations.json; this gate judges it.
#
# THE VERDICT (§6.4 + PA-2, under §6.3 wave semantics):
#   missing  manifest element never seen in any induced state -> FAIL by wireId (CLOSED wave;
#            PENDING if its wave has not started). _shell rows are scoped to their shellStates:
#            absence OUTSIDE a declared screen-state is NOT a fail (contextually-hidden chrome).
#   extra    a rendered data-oid with no manifest row -> FAIL (built-not-designed). Always gates.
#   dup      the SAME data-oid on >1 node in one state, NOT distinguished by distinct data-oiid,
#            is two nodes claiming one identity -> FAIL (BH7 disposition: set semantics would
#            silently collapse them; instances are the sanctioned multiplicity, via data-oiid).
#   PA-2     the crawl MUST target the PRODUCTION build config; the gate asserts mode=production
#            and data-* not stripped over the served build-config (fail-closed if unobserved).
#   T-23     a rendered interactive-ROLE node with no data-oid is reported on a WARN list for
#            design review (role heuristic, NOT handler detection — see the harness honesty note);
#            reported, never gating.
#   floors   zero-row manifest -> FATAL; manifest rows but an EMPTY crawl union -> FAIL.
#
# EXIT CONTRACT (0 PASS / 1 FAIL / 2 FATAL, fail-closed per F-008) — output frozen like §6.2/§6.3:
#   RESULT is one of PASS / FAIL / FATAL / PASS-WITH-PEN-CHANGED.
#   2 FATAL  — the §6.2 hard dependency FAILed/FATALed (own checks NOT run); node/Playwright
#              absent; the app unreachable / hydration timeout; browser launch failure; an
#              unparseable manifest / results / machine / observations; a wiring-results
#              inconsistency; a declared machine state that cannot be induced; a build NOT crawled
#              in production mode (PA-2); a zero-row manifest.
#   1 FAIL   — a CLOSED-wave missing element; an extra (built-not-designed) data-oid; a duplicate
#              data-oid identity; the production build strips data-* (PA-2/T-9); the empty-crawl floor.
#   0 PASS   — manifest and crawl agree on every closed-wave element; not-started rows PENDING/info.
#              A propagated PEN-CHANGED keeps exit 0 but marks RESULT PASS-WITH-PEN-CHANGED.
#   VERDICT PRECEDENCE [toolkit convention]: a FAIL (violation) exits 1 BEFORE a co-occurring
#   FATAL exits 2. Structural FATALs (can't run / can't trust the crawl) are detected UP FRONT and
#   verdict early, so an exit-2 case is never downgraded by a later closed-wave FAIL.
#   AUDIT_ALLOW_SKIP=1 is passed through to the §6.2 hard dependency only; this gate has no skip.
#
# Usage: seam-gate.sh <export-dir> --app-url <url> [--app-cmd <cmd>] --results <results.json>
#                     [--base <repo-root>] [--timeout <ms>] [--browser chromium]
#   <export-dir>  design/interaction-model dir: wiring-manifest.json + machine.*.json + the §6.2 set.
#   --app-url     where the HYDRATED app is reachable (REQUIRED).
#   --app-cmd     OPTIONAL: the harness starts it, waits for --app-url ready, tears it down after.
#   --results     wiring-results.json (§6.6) — the wave register (format-v0).
#   --base        repo root for the §6.2 gate's pinned-.pen resolution. Default $PWD.
# Test hooks (env): PEN_HARNESS_DIR overrides the harness dir; SEAM_HARNESS_NO_INDUCE=1 lobotomizes
#   the crawl to the initial state only (proving the union is load-bearing).
set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-seam-gate}"
emit() { echo "[${AUDIT_TAG}] $*"; }
fatal() { emit "FATAL: $*"; exit 2; }

DIR=""
APP_URL=""
APP_CMD=""
RESULTS=""
BASE="$PWD"
TIMEOUT="6000"
BROWSER="chromium"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --app-url) shift; [ "$#" -gt 0 ] || fatal "--app-url needs a value"; APP_URL="$1" ;;
    --app-url=*) APP_URL="${1#*=}" ;;
    --app-cmd) shift; [ "$#" -gt 0 ] || fatal "--app-cmd needs a value"; APP_CMD="$1" ;;
    --app-cmd=*) APP_CMD="${1#*=}" ;;
    --results) shift; [ "$#" -gt 0 ] || fatal "--results needs a value"; RESULTS="$1" ;;
    --results=*) RESULTS="${1#*=}" ;;
    --base) shift; [ "$#" -gt 0 ] || fatal "--base needs a value"; BASE="$1" ;;
    --base=*) BASE="${1#*=}" ;;
    --timeout) shift; [ "$#" -gt 0 ] || fatal "--timeout needs a value"; TIMEOUT="$1" ;;
    --timeout=*) TIMEOUT="${1#*=}" ;;
    --browser) shift; [ "$#" -gt 0 ] || fatal "--browser needs a value"; BROWSER="$1" ;;
    --browser=*) BROWSER="${1#*=}" ;;
    -h|--help) sed -n '2,59p' "$0"; exit 0 ;;
    --*) fatal "unknown arg: $1" ;;
    *) [ -z "$DIR" ] && DIR="$1" || fatal "unexpected extra arg: $1" ;;
  esac
  shift
done

[ -n "$DIR" ] || fatal "usage: seam-gate.sh <export-dir> --app-url <url> [--app-cmd <cmd>] --results <results.json> [--base <repo-root>]"
[ -d "$DIR" ] || fatal "export dir not found / not a directory: $DIR"
[ -n "$APP_URL" ] || fatal "--app-url <url> is required (where the hydrated app is reachable)"
[ -n "$RESULTS" ] || fatal "--results <results.json> is required"
[ -f "$RESULTS" ] || fatal "wiring-results.json not found: $RESULTS"
MANIFEST="$DIR/wiring-manifest.json"
[ -f "$MANIFEST" ] || fatal "export dir has no wiring-manifest.json: $MANIFEST"
MACHINES=()
while IFS= read -r m; do [ -n "$m" ] && MACHINES+=("$m"); done \
  < <(LC_ALL=C find "$DIR" -maxdepth 1 -name 'machine.*.json' 2>/dev/null | LC_ALL=C sort)
[ "${#MACHINES[@]}" -gt 0 ] || fatal "export dir has no machine.*.json (the statechart the crawl walks): $DIR"
command -v python3 >/dev/null 2>&1 || fatal "python3 required to compute the seam-gate verdict"

HERE="$(cd "$(dirname "$0")" && pwd)"
INTEGRITY_SH="$HERE/pen-integrity.sh"
[ -f "$INTEGRITY_SH" ] || fatal "pen-integrity.sh not found next to this gate ($INTEGRITY_SH) — the §6.2 hard dependency is missing"
HARNESS_DIR="${PEN_HARNESS_DIR:-$HERE/../harness}"
HARNESS="$HARNESS_DIR/pen-harness.mjs"

# ============= node / Playwright presence — FATAL, never a silent skip (F-008) =========
command -v node >/dev/null 2>&1 || fatal "node is required for the §6.4 post-hydration crawl (runtime gate) — not found (F-008: no silent skip)"
[ -f "$HARNESS" ] || fatal "pen-harness.mjs not found at $HARNESS (harness missing)"
[ -d "$HARNESS_DIR/node_modules/playwright" ] || fatal "Playwright is not installed in the harness ($HARNESS_DIR) — run: (cd $HARNESS_DIR && npm ci && npx playwright install chromium). A runtime gate that cannot launch a browser FATALs; it never silently skips (F-008)"

# ================= HARD DEPENDENCY — §6.2 export integrity [T-3d] =============
integrity_out="$(bash "$INTEGRITY_SH" "$DIR" --base "$BASE" 2>&1)"; integrity_rc=$?
if [ "$integrity_rc" -ne 0 ]; then
  emit "note: §6.2 export-integrity hard dependency did not pass (exit ${integrity_rc}) — output below:"
  printf '%s\n' "$integrity_out" | sed 's/^/    /'
  fatal "refusing to run the seam crawl on exports that failed §6.2 export-integrity (hard dependency [T-3d]) — fix integrity and re-run"
fi
emit "ok: §6.2 export-integrity hard dependency passed (exit 0)"
PEN_CHANGED=0
if printf '%s' "$integrity_out" | grep -q 'PEN-CHANGED'; then
  PEN_CHANGED=1
  emit "PEN-CHANGED: propagated from §6.2 export-integrity — the pinned .pen moved since extraction; wave-close is BLOCKED until a §6.5 re-extraction runs (re-emitted here so wave-close consumers see it through this gate)"
fi

# ================= run the harness crawl → observations.json ===================
OBS="$(mktemp "${TMPDIR:-/tmp}/seam-obs.XXXXXX")" || fatal "cannot create a temp observations file"
trap 'rm -f "$OBS"' EXIT
HARGS=(crawl --app-url "$APP_URL" --manifest "$MANIFEST" --results "$RESULTS" --out "$OBS" --timeout "$TIMEOUT" --browser "$BROWSER")
[ -n "$APP_CMD" ] && HARGS+=(--app-cmd "$APP_CMD")
for m in "${MACHINES[@]}"; do HARGS+=(--machine "$m"); done
[ "${SEAM_HARNESS_NO_INDUCE:-0}" = "1" ] && HARGS+=(--no-induce)

harness_out="$(node "$HARNESS" "${HARGS[@]}" 2>&1)"; harness_rc=$?
printf '%s\n' "$harness_out" | sed 's/^/    [harness] /'
if [ "$harness_rc" -ne 0 ]; then
  fatal "the post-hydration crawl could not run (harness exit ${harness_rc}) — the gate cannot decide on a crawl it could not complete (fail-closed)"
fi
[ -s "$OBS" ] || fatal "the harness produced no observations.json — cannot decide (fail-closed)"

# ================= verdict (embedded python — pen-lint / wiring-gate idiom) =====
AUDIT_TAG="$AUDIT_TAG" SEAM_PEN_CHANGED="$PEN_CHANGED" python3 - "$OBS" "$MANIFEST" "$RESULTS" <<'PYEOF'
import json
import os
import sys

TAG = os.environ.get("AUDIT_TAG", "seam-gate")
PEN_CHANGED = os.environ.get("SEAM_PEN_CHANGED", "0") == "1"
OBS_PATH, MANIFEST_PATH, RESULTS_PATH = sys.argv[1], sys.argv[2], sys.argv[3]

violations = 0
fatals = 0


def emit(m):
    print("[%s] %s" % (TAG, m))


def fail(m):
    global violations
    emit("FAIL: %s" % m)
    violations += 1


def fatal(m):
    global fatals
    emit("FATAL: %s" % m)
    fatals += 1


def verdict():
    if violations > 0:
        emit("RESULT: FAIL (%d violation(s))" % violations)
        sys.exit(1)
    if fatals > 0:
        emit("RESULT: FATAL (%d check(s) could not run — fail-closed)" % fatals)
        sys.exit(2)
    if PEN_CHANGED:
        emit("RESULT: PASS-WITH-PEN-CHANGED (seam carry clean; wave-close BLOCKED pending a §6.5 "
             "re-extraction — propagated from §6.2)")
        sys.exit(0)
    emit("RESULT: PASS (manifest and post-hydration crawl agree; every closed-wave element built)")
    sys.exit(0)


def load(path, what):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001 — any parse/IO error on a required input is FATAL
        fatal("cannot parse %s: %s" % (what, e))
        return None


obs = load(OBS_PATH, "observations.json")
if obs is None:
    verdict()

# ---- PA-2: the crawl MUST target the PRODUCTION build config (structural, up front) ----
bc = obs.get("buildConfig")
if not isinstance(bc, dict):
    fatal("PA-2: no build-config observed from the served app — cannot confirm the crawl targeted "
          "the PRODUCTION build config (§6.4/PA-2, fail-closed)")
    verdict()
if bc.get("mode") != "production":
    fatal("PA-2: the crawl ran against build mode %r, not 'production' — the seam crawl MUST target "
          "the production build config (§6.4/PA-2)" % bc.get("mode"))
    verdict()

# ---- manifest + zero-row floor (structural, up front) ----
manifest = load(MANIFEST_PATH, "wiring-manifest.json")
if manifest is None:
    verdict()
if not isinstance(manifest, list):
    fatal("wiring-manifest.json must be a JSON array of rows")
    verdict()
if len(manifest) == 0:
    fatal("non-vacuity floor: wiring-manifest has zero rows — a zero-row universe cannot pass "
          "(§6/T-1; fail-closed)")
    verdict()

# ---- wiring-results wave register (structural, up front — mirrors §6.3) ----
results = load(RESULTS_PATH, "wiring-results.json")
if results is None:
    verdict()
if not isinstance(results, dict):
    fatal("wiring-results.json must be a JSON object (waves + rows)")
    verdict()
waves = results.get("waves")
if not isinstance(waves, dict):
    fatal("wiring-results.json 'waves' must be an object mapping wave -> \"open\"|\"closed\"")
    verdict()
raw_rows = results.get("rows", [])
if not isinstance(raw_rows, list):
    fatal("wiring-results.json 'rows' must be a JSON array — a non-list rows would silently mark "
          "every row not-started (fail-open)")
    verdict()
wave_of = {}
for rr in raw_rows:
    if not isinstance(rr, dict) or "screen" not in rr or "wireId" not in rr:
        continue
    kk = (rr["screen"], rr["wireId"])
    if kk in wave_of:
        fatal("wiring-results has a duplicate row for %s/%s — a duplicate can launder a closed-wave "
              "FAIL to PENDING (fail-open)" % kk)
        continue
    wave_of[kk] = rr.get("wave")
for wn, st in waves.items():
    if st not in ("open", "closed"):
        fatal("wiring-results waves['%s'] = %r, expected \"open\"|\"closed\" (fail-closed)" % (wn, st))
for (s, w2), wv in wave_of.items():
    if wv is not None and str(wv) not in waves:
        fatal("wiring-results row %s/%s references wave '%s' absent from the waves map "
              "(inconsistent results file)" % (s, w2, wv))
if fatals:
    verdict()


def wave_state(screen, wid):
    w = wave_of.get((screen, wid))
    if w is None:
        return "not-started"
    return "closed" if waves.get(str(w)) == "closed" else "not-started"


# ---- unreachable declared state -> FATAL up front (incomplete crawl; can't trust missing) ----
unreachable = obs.get("unreachableStates") or []
if unreachable:
    for u in unreachable:
        fatal("declared machine state '%s' (%s) could not be induced by the crawl — the machine "
              "claims a state the built UI never reaches (behavior source ↔ build divergence): %s"
              % (u.get("state"), u.get("machine"), u.get("reason", "")))
    verdict()

# ---- assemble observed sets ----
union = set(obs.get("union") or [])
states = obs.get("states") or []
oid_states = {}  # data-oid -> set of screen-states it was observed in
for stt in states:
    ss = stt.get("screenState")
    for o in (stt.get("oids") or []):
        oid_states.setdefault(o, set()).add(ss)

# ---- WARN list (T-23 role heuristic; reported, never gating) ----
for w in (obs.get("warnList") or []):
    emit("WARN: an interactive-role node (<%s>%s) carrying NO data-oid was rendered in %s — a "
         "role heuristic for design review (NOT handler detection; T-23 backstop), non-gating: %r"
         % (w.get("tag"), (" role=%s" % w.get("role")) if w.get("role") else "",
            ",".join(w.get("states") or []), (w.get("text") or "")[:40]))

# ---- non-vacuity floor: manifest rows but an empty crawl ----
if len(union) == 0:
    fail("non-vacuity floor: the crawl observed ZERO data-oid elements while the manifest has %d "
         "row(s) — nothing was built / data-* stripped (§6.4 + PA-2)" % len(manifest))

# ---- PA-2 (data-*): the production build must not strip data-* ----
if bc.get("dataAttributes") != "preserved":
    fail("PA-2/T-9: the production build config reports data-* attributes %r (expected "
         "'preserved') — a gated build MUST NOT strip data-*" % bc.get("dataAttributes"))

# ---- duplicate data-oid (BH7): two nodes claiming one identity ----
# Instances (distinct data-oiid) are the sanctioned multiplicity; anything else FAILs.
for stt in states:
    by_oid = {}
    for n in (stt.get("nodes") or []):
        by_oid.setdefault(n["oid"], []).append(n.get("oiid"))
    for oid, oiids in by_oid.items():
        if len(oiids) <= 1:
            continue
        if any(x is None for x in oiids) or len(set(oiids)) != len(oiids):
            fail("duplicate data-oid '%s' in state %s: %d nodes claim one identity (data-oiid=%r) — "
                 "set semantics would silently collapse them; repeated instances MUST carry DISTINCT "
                 "data-oiid (BH7 / T-31)" % (oid, stt.get("state"), len(oiids), oiids))


def bare(screen):
    return screen[len("screen/"):] if isinstance(screen, str) and screen.startswith("screen/") else screen


manifest_oids = set()
for row in manifest:
    if isinstance(row, dict):
        manifest_oids.add("%s/%s" % (bare(row.get("screen")), row.get("wireId")))

# ---- extra: built-not-designed (union ∖ manifest) -> FAIL (always gates) ----
for o in sorted(union - manifest_oids):
    fail("built-not-designed: data-oid '%s' was rendered by the app but has no manifest row "
         "(§6.4 extra)" % o)

# ---- missing: manifest ∖ observed, wave-scoped, shellStates-scoped ----
for row in manifest:
    if not isinstance(row, dict):
        fail("manifest row is not an object: %r" % (row,))
        continue
    screen = row.get("screen")
    wid = row.get("wireId")
    oid = "%s/%s" % (bare(screen), wid)
    is_shell = row.get("shell") is True or screen == "screen/_shell"
    shell_states = row.get("shellStates")
    if is_shell and isinstance(shell_states, list) and "*" not in shell_states:
        declared = set(bare(s) for s in shell_states)
        observed = len(declared & oid_states.get(oid, set())) > 0
        scope = " within its declared shellStates %s" % shell_states
    else:
        observed = oid in union
        scope = ""
    if observed:
        continue
    st = wave_state(screen, wid)
    if st == "closed":
        fail("missing: manifest element %s was never seen in any induced state%s — element never "
             "built (§6.4 missing)" % (oid, scope))
    else:
        emit("PENDING: %s not observed but its wave has not started — surfaced, not FAIL "
             "(§6.4 under §6.3 wave semantics)" % oid)

verdict()
PYEOF
