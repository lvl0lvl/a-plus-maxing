#!/usr/bin/env bash
# tests/test-seam-gate.sh — F-007 negative test for scripts/seam-gate.sh (the §6.4 seam gate).
#
# F-007 obligation: a gate that cannot prove it goes RED on bad input enforces nothing. The §6.4
# seam gate compares the wiring-manifest against the data-oids collected by a POST-HYDRATION crawl of
# the BUILT React fixture (tests/fixtures/seam-gate/). This suite drives the REAL runtime — headless
# Chromium via the pen-harness — and proves each verdict and every guard against guard-EXCLUSIVE
# anchors (the Phase-2b discipline):
#   GOOD                full app + all-CLOSED-wave results                       -> PASS (0).
#   missing (closed)    a manifest element omitted from the built app            -> FAIL (1) by oid;
#                       the SAME row in an OPEN wave                              -> PENDING, PASS (0).
#   extra               a data-oid the manifest lacks                            -> FAIL (1) built-not-designed.
#   duplicate           the same data-oid on 2 nodes with no distinguishing oiid -> FAIL (1) (BH7).
#   unreachable state   a declared machine state the built UI never reaches      -> FATAL (2).
#   §6.2 hard-dep       a corrupt export digest                                  -> FATAL (2) WITHOUT
#                       running the crawl or emitting a RESULT verdict (leak-check).
#   PEN-CHANGED         a pen-changed export set                                 -> PASS (0) + marker.
#   lobotomized crawl   the SAME good app crawled initial-state-only             -> FAIL (1): proves
#                       the state-induction union is LOAD-BEARING (portal/tab oids vanish).
#   _shell shellStates  contextually-hidden chrome absent on an UNDECLARED screen -> PASS (0, GOOD);
#                       absent on its DECLARED screen                            -> FAIL (1).
#   PA-2 prod build     crawl against a non-production build                     -> FATAL (2);
#                       a production build that strips data-*                     -> FAIL (1).
#   T-23 WARN           an interactive-role node with no data-oid                -> WARN, non-gating (PASS 0).
#   floors              a zero-row manifest -> FATAL (2); an empty crawl union -> FAIL (1).
#   structural FATALs   no build-config, manifest-not-array, results-not-dict, waves-not-object,
#                       rows-not-list, duplicate results row, invalid wave value, row-references-
#                       absent-wave -> FATAL (2), each with a guard-exclusive anchor (mirrors the
#                       sibling test-wiring-gate.sh's equivalents).
#   app-readiness       an --app-cmd that never serves --app-url                 -> FATAL (2).
#   malformed machine   a non-JSON machine file (with --app-cmd) -> FATAL (2) AND the detached app is
#                       torn down (the crawl().catch tears down via `finally`; the port is freed).
#   no runtime          Playwright absent in the harness dir                     -> FATAL (2), never a
#                       silent skip (F-008).  (node absent is impractical to exercise — the test
#                       harness itself requires node; the Playwright-absent FATAL below is the
#                       runtime-absent branch this suite covers.)
#   assert_red_when_guard_removed on the load-bearing guards (missing, extra, duplicate, unreachable,
#                       lobotomized-induction): good=0, mutant=non-zero.
#
# PORTS / TIMING (G9): the fixture server binds port 0 and PRINTS the bound port
# (`SEAM_FIXTURE_READY http://127.0.0.1:<port>/`); this suite starts the server and parses that
# actually-bound port — no pre-allocate-then-close race. The induction timeout is a generous ceiling
# (GTIMEOUT), decoupled from the tight value that spuriously tripped unreachable-FATAL under load; a
# genuinely-unreachable state still fails fast via a short per-case timeout. The readiness-timeout
# FATAL is exercised with PEN_HARNESS_READY_FLOOR_MS so it fails in ~1.5s without weakening the guard.
#
# READINESS (mirrors test-gate-attest's loud optional-dep skip): needs node + the harness's
# Playwright + a launchable Chromium + the built fixture. On a box without them it LOUD-SKIPS (exit 0)
# so run-all-tests.sh stays green; the full F-007 proofs run wherever the one-time install+build
# (fixture README) has been done. NOT a gate skip — the GATE itself FATALs on absent Playwright
# (tested below); this is the test harness declining to run its own substrate.
#
# NOT hermetic re the .pen (mirrors test-wiring-gate): the §6.2 hard dependency runs against the REAL
# committed .pen resolved from the seam export set (--base = repo root). App/export mutations are made
# on COPIES in a temp dir. The crawl is localhost-only — no network beyond 127.0.0.1 at test time.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/seam-gate.sh"
DIGEST="${TEST_DIR}/../scripts/pen-digest.sh"
HARNESS_DIR="${TEST_DIR}/../harness"
REPO="$(cd "${TEST_DIR}/../../../.." && pwd)"          # skills_library repo root
FIX="${TEST_DIR}/fixtures/seam-gate"
EXP="${FIX}/design/interaction-model"
APP="${FIX}/app"
DIST="${APP}/dist"
RESULTS="${FIX}/wiring-results.json"
GTIMEOUT="12000"   # generous induction/goto ceiling (G9: 4000 was too tight under full-suite load)
UNREACH_TO="4000"  # genuinely-unreachable states fail fast; reachable elements still render well within

# ---- readiness / loud skip ---------------------------------------------------
skip() { echo "[test-seam-gate] SKIP (loud): $1"; echo "[test-seam-gate] to run the full F-007 crawl proofs: (cd ${APP} && npm ci && npm run build) && (cd ${HARNESS_DIR} && npm ci && npx playwright install chromium)"; exit 0; }
# Portability (update-rigor): this gate resolves a committed .pen via --base "$REPO" (the
# framework-repo root) — content OUTSIDE toolkit/ that does not travel with a toolkit copy. In a
# consuming project (no designs/fixtures/, or REPO overshoots the copied layout), LOUD-SKIP so
# the pulled suite stays green; the framework repo still runs the full crawl proofs.
[ -d "$REPO/designs/fixtures" ] || skip "design fixtures absent under REPO ($REPO) — not a design-pipeline checkout"
command -v node >/dev/null 2>&1 || skip "node not found"
command -v python3 >/dev/null 2>&1 || skip "python3 not found"
[ -d "${HARNESS_DIR}/node_modules/playwright" ] || skip "Playwright not installed in the harness (${HARNESS_DIR})"
[ -d "${APP}/node_modules" ] || skip "fixture app deps not installed (${APP}/node_modules)"
if [ ! -f "${DIST}/index.html" ]; then ( cd "$APP" && npm run build >/dev/null 2>&1 ) || skip "fixture app build failed"; fi
( cd "$HARNESS_DIR" && node -e "require('playwright').chromium.launch({headless:true}).then(b=>b.close()).catch(()=>process.exit(3))" ) >/dev/null 2>&1 || skip "Chromium not launchable (run: npx playwright install chromium in ${HARNESS_DIR})"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/seam-gate.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

# freeport_once — a port nothing is listening on (for the dead-port readiness FATAL + the malformed
# machine cases, where an UNbound port is what we want). NOT used for the live fixture server.
freeport_once() { python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()'; }

# start_server <distdir> -> prints "<pid> <port>"; the server binds port 0 and we parse the bound
# port from its SEAM_FIXTURE_READY line (G9: eliminates the allocate-then-close TOCTOU).
start_server() {
  local dist="$1" outfile pid line port i
  outfile="$(mktemp "$WORK/serve.XXXXXX")"
  node "$APP/serve.mjs" --dir "$dist" --port 0 >"$outfile" 2>&1 &
  pid=$!
  for i in $(seq 1 150); do
    if line="$(grep -m1 'SEAM_FIXTURE_READY' "$outfile" 2>/dev/null)" && [ -n "$line" ]; then break; fi
    kill -0 "$pid" 2>/dev/null || return 1
    sleep 0.1
  done
  port="$(printf '%s' "$line" | sed -n 's#.*127\.0\.0\.1:\([0-9][0-9]*\)/.*#\1#p')"
  [ -n "$port" ] || { kill "$pid" 2>/dev/null; return 1; }
  printf '%s %s' "$pid" "$port"
}

# app_torn_down <port> -> exit 0 if NOTHING accepts a connection on the port within ~3s (the app was
# torn down), else 1. Uses connect (not bind) so it is not confused by TIME_WAIT / SO_REUSEADDR: a
# refused connection means no listener, a successful one means an orphaned serve.mjs is still up.
app_torn_down() {
  python3 - "$1" <<'PY'
import socket, sys, time
port = int(sys.argv[1]); deadline = time.time() + 3.0
while time.time() < deadline:
    s = socket.socket(); s.settimeout(0.3)
    try:
        s.connect(("127.0.0.1", port)); s.close(); time.sleep(0.15)  # still listening -> retry
    except OSError:
        sys.exit(0)  # connection refused -> the app is gone
sys.exit(1)  # still accepting after 3s -> orphaned listener
PY
}

# run_gate <exportdir> <distdir> <query> <results> [no_induce] [timeout] -> stdout=gate output, returns gate exit
# Starts the fixture server itself (bound port parsed), runs the gate against --app-url (no --app-cmd),
# and tears the server down. --app-cmd is exercised separately by the readiness/malformed cases.
run_gate() {
  local exp="$1" dist="$2" query="$3" results="$4" ni="${5:-0}" to="${6:-$GTIMEOUT}" sp pid port out rc
  sp="$(start_server "$dist")" || { echo "[test-error] fixture server failed to start for $dist"; return 97; }
  pid="${sp%% *}"; port="${sp##* }"
  out="$(SEAM_HARNESS_NO_INDUCE="$ni" bash "$GATE" "$exp" \
    --app-url "http://127.0.0.1:${port}/${query}" \
    --results "$results" --base "$REPO" --timeout "$to" 2>&1)"; rc=$?
  kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
  printf '%s' "$out"
  return "$rc"
}

# guard_run — run_gate discarding output (for assert_red_when_guard_removed); functions + vars are
# inherited by the ( ) subshell test-lib evals in.
guard_run() { run_gate "$1" "$2" "$3" "$4" "${5:-0}" "${6:-$GTIMEOUT}" >/dev/null 2>&1; }
gcmd() { printf 'guard_run %q %q %q %q %q %q' "$1" "$2" "$3" "$4" "${5:-0}" "${6:-$GTIMEOUT}"; }

# check <label> <expected_exit> <exportdir> <dist> <query> <results> [ni] [to] (+ CK_PRESENT/CK_ABSENT)
CK_PRESENT=""; CK_ABSENT=""
check() {
  local label="$1" exp_exit="$2" out rc
  out="$(run_gate "$3" "$4" "$5" "$6" "${7:-0}" "${8:-$GTIMEOUT}")"; rc=$?
  TESTS_RUN=$((TESTS_RUN + 1))
  local ok=1
  [ "$rc" = "$exp_exit" ] || { ok=0; echo "[FAIL] ${label}: exit ${rc} want ${exp_exit}"; }
  if [ -n "$CK_PRESENT" ] && ! printf '%s' "$out" | grep -qE "$CK_PRESENT"; then ok=0; echo "[FAIL] ${label}: output lacked /${CK_PRESENT}/"; fi
  if [ -n "$CK_ABSENT" ] && printf '%s' "$out" | grep -qE "$CK_ABSENT"; then ok=0; echo "[FAIL] ${label}: output UNEXPECTEDLY matched /${CK_ABSENT}/"; fi
  if [ "$ok" = 1 ]; then echo "[PASS] ${label} (exit ${rc})"; else TESTS_FAILED=$((TESTS_FAILED + 1)); fi
  CK_PRESENT=""; CK_ABSENT=""
}

# ---- mutation helpers --------------------------------------------------------
newexport() { local d="$WORK/$1"; rm -rf "$d"; cp -R "$EXP" "$d"; echo "$d"; }
newdist()   { local d="$WORK/$1"; rm -rf "$d"; cp -R "$DIST" "$d"; echo "$d"; }
restamp() { local h; h="$(bash "$DIGEST" "$1")"; python3 -c "
f='$1/export.digest'; h='$h'
out=['content-sha256: '+h if ln.startswith('content-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"; }
corrupt_export() { python3 -c "p='$1/index.md';s=open(p).read();open(p,'w').write(s.replace('Inventory','Xnventory',1))"; }
penchange_export() { python3 -c "
f='$1/export.digest'
out=['pen-sha256: deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef' if ln.startswith('pen-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"; }
zero_manifest() { printf '[]\n' > "$1/wiring-manifest.json"; restamp "$1"; }
manifest_not_array() { printf '{}\n' > "$1/wiring-manifest.json"; restamp "$1"; }
no_build_config() { rm -f "$1/build-config.json"; }
add_unreachable_state() { # add a machine state reachable only via an element the app never renders
  python3 - "$1/machine.review.json" <<'PY'
import json, sys
p = sys.argv[1]; m = json.load(open(p))
m["states"]["settings"] = {"initial": "idle", "states": {"idle": {}}}
m["states"]["list"]["states"]["idle"]["on"]["OPEN_SETTINGS"] = [
    {"fromWireId": "open-settings", "guard": "", "target": "settings"}]
json.dump(m, open(p, "w"), indent=2, sort_keys=True); open(p, "a").write("\n")
PY
  restamp "$1"
}
single_state_machine() { printf '%s\n' '{ "id": "review", "initial": "list", "states": { "list": {} } }' > "$1/machine.review.json"; restamp "$1"; }
results_move() { # $1=dst $2=screen $3=wireId $4=wave  (from RESULTS)
  python3 - "$RESULTS" "$1" "$2" "$3" "$4" <<'PY'
import json, sys
src, dst, screen, wid, wave = sys.argv[1:6]
r = json.load(open(src))
for row in r["rows"]:
    if row["screen"] == screen and row["wireId"] == wid:
        row["wave"] = int(wave)
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}
results_set() { # $1=dst $2=python-expr-on-r  (generic results mutator, from RESULTS)
  python3 - "$RESULTS" "$1" "$2" <<'PY'
import json, sys
src, dst, expr = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(src)); exec(expr)
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}
set_build_config() { printf '%s\n' "$2" > "$1/build-config.json"; }  # $1=distdir $2=json

# =============================================================================
# GOOD -> PASS (0). Also proves _shell/back (shellStates screen/detail) is absent on the list
# screen and does NOT false-fail (the contextually-hidden-chrome positive).
# =============================================================================
CK_PRESENT="RESULT: PASS"; CK_ABSENT="missing: manifest element _shell/back"
check "GOOD full app + all-closed waves" 0 "$EXP" "$DIST" "" "$RESULTS"

# =============================================================================
# missing (CLOSED wave) — list/search is a pure leaf (not a trigger) so omitting it isolates the
# missing guard (no state becomes unreachable).
# =============================================================================
CK_PRESENT="missing: manifest element list/search"
check "missing closed-wave element" 1 "$EXP" "$DIST" "?omit=list/search" "$RESULTS"

results_move "$WORK/res-search-open.json" "screen/list" "search" 2
CK_PRESENT="PENDING: list/search"; CK_ABSENT="RESULT: FAIL"
check "missing element OPEN wave -> PENDING" 0 "$EXP" "$DIST" "?omit=list/search" "$WORK/res-search-open.json"

# =============================================================================
# extra / duplicate.
# =============================================================================
CK_PRESENT="built-not-designed: data-oid 'list/ghost'"
check "extra built-not-designed" 1 "$EXP" "$DIST" "?extra=1" "$RESULTS"

CK_PRESENT="duplicate data-oid '_shell/home'"
check "duplicate data-oid identity" 1 "$EXP" "$DIST" "?dup=_shell/home" "$RESULTS"

# =============================================================================
# unreachable declared machine state -> FATAL (short per-case timeout: the missing element fails fast).
# =============================================================================
e="$(newexport unreachable)"; add_unreachable_state "$e"
CK_PRESENT="could not be induced"
check "declared-but-unreachable state -> FATAL" 2 "$e" "$DIST" "" "$RESULTS" 0 "$UNREACH_TO"

# =============================================================================
# §6.2 hard-dependency [T-3d] — corrupt digest -> FATAL WITHOUT running the crawl / a RESULT verdict.
# =============================================================================
e="$(newexport corrupt)"; corrupt_export "$e"
CK_PRESENT="refusing to run the seam crawl"; CK_ABSENT="\[seam-gate\] RESULT: (PASS|FAIL)"
check "§6.2 hard-dep corrupt -> FATAL, no own verdict" 2 "$e" "$DIST" "" "$RESULTS"

# =============================================================================
# PEN-CHANGED propagation.
# =============================================================================
e="$(newexport penchanged)"; penchange_export "$e"
CK_PRESENT="RESULT: PASS-WITH-PEN-CHANGED"
check "PEN-CHANGED propagation" 0 "$e" "$DIST" "" "$RESULTS"

# =============================================================================
# lobotomized crawl (initial-state-only) -> FAIL missing: proves the induction union is load-bearing.
# =============================================================================
CK_PRESENT="missing: manifest element list/apply-filter"
check "lobotomized (initial-only) crawl -> FAIL" 1 "$EXP" "$DIST" "" "$RESULTS" 1

# =============================================================================
# _shell shellStates — absent on its DECLARED screen (detail) DOES fail (scoping is not a blanket
# exemption). The undeclared-screen positive is the GOOD case above.
# =============================================================================
CK_PRESENT="missing: manifest element _shell/back.*within its declared shellStates"
check "shell element missing on its DECLARED screen -> FAIL" 1 "$EXP" "$DIST" "?omit=_shell/back" "$RESULTS"

# =============================================================================
# PA-2 — non-production build -> FATAL; production build that STRIPS data-* -> FAIL. The served
# build-config.json is what the harness fetches; mutate a served copy (dist is not digested).
# =============================================================================
d="$(newdist dev-build)"; set_build_config "$d" '{ "mode": "development", "dataAttributes": "preserved" }'
CK_PRESENT="not 'production'"
check "PA-2 non-production build -> FATAL" 2 "$EXP" "$d" "" "$RESULTS"

d="$(newdist stripped-build)"; set_build_config "$d" '{ "mode": "production", "dataAttributes": "stripped" }'
CK_PRESENT="MUST NOT strip data-\*"
check "PA-2 production strips data-* -> FAIL" 1 "$EXP" "$d" "" "$RESULTS"

# =============================================================================
# T-23 WARN — non-gating.
# =============================================================================
CK_PRESENT="WARN: an interactive-role node"; CK_ABSENT="RESULT: FAIL"
check "T-23 role-heuristic WARN is non-gating" 0 "$EXP" "$DIST" "?warn=1" "$RESULTS"

# =============================================================================
# floors — zero-row manifest -> FATAL; empty crawl union -> FAIL.
# =============================================================================
e="$(newexport zero-row)"; zero_manifest "$e"
CK_PRESENT="zero rows"
check "zero-row manifest floor -> FATAL" 2 "$e" "$DIST" "" "$RESULTS"

e="$(newexport empty-crawl)"; single_state_machine "$e"
CK_PRESENT="observed ZERO data-oid elements"
check "empty crawl union floor -> FAIL" 1 "$e" "$DIST" "?omit=_shell/home,list/search,list/incident-row,list/open-filters,list/open-detail" "$RESULTS"

# =============================================================================
# structural FATALs (mirror test-wiring-gate.sh) — each with a guard-exclusive anchor. All are checked
# AFTER a successful crawl, so run_gate stands up the GOOD server for each.
# =============================================================================
d="$(newdist nobc)"; no_build_config "$d"
CK_PRESENT="no build-config observed"
check "no build-config -> FATAL (PA-2 fail-closed)" 2 "$EXP" "$d" "" "$RESULTS"

e="$(newexport manifestobj)"; manifest_not_array "$e"
CK_PRESENT="must be a JSON array of rows"
check "manifest not an array -> FATAL" 2 "$e" "$DIST" "" "$RESULTS"

printf '[]\n' > "$WORK/res-notdict.json"
CK_PRESENT="must be a JSON object"
check "results not an object -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-notdict.json"

results_set "$WORK/res-wavesarr.json" "r['waves'] = []"
CK_PRESENT="'waves' must be an object"
check "waves not an object -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-wavesarr.json"

results_set "$WORK/res-rowsnull.json" "r['rows'] = None"
CK_PRESENT="'rows' must be a JSON array"
check "rows not a list -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-rowsnull.json"

results_set "$WORK/res-dup.json" "r['rows'].append({'screen':'screen/list','wireId':'search','wave':1})"
CK_PRESENT="duplicate row for screen/list/search"
check "duplicate results row -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-dup.json"

results_set "$WORK/res-badwave.json" "r['waves']['1'] = 'frozen'"
CK_PRESENT="expected .open."
check "invalid wave value -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-badwave.json"

results_set "$WORK/res-absentwave.json" "[row.__setitem__('wave', 9) for row in r['rows'] if row['screen']=='screen/list' and row['wireId']=='search']"
CK_PRESENT="absent from the waves map"
check "row references absent wave -> FATAL" 2 "$EXP" "$DIST" "" "$WORK/res-absentwave.json"

# =============================================================================
# app-readiness-timeout FATAL — --app-cmd that never serves --app-url. PEN_HARNESS_READY_FLOOR_MS
# shortens the readiness floor so this fails in ~1.5s; the guard is unchanged (default floor 15s).
# =============================================================================
deadport="$(freeport_once)"
out="$(PEN_HARNESS_READY_FLOOR_MS=1500 bash "$GATE" "$EXP" \
  --app-url "http://127.0.0.1:${deadport}/" --app-cmd "sleep 30" \
  --results "$RESULTS" --base "$REPO" --timeout 800 2>&1)"; rc=$?
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -qE "did not become ready"; then
  echo "[PASS] app-readiness-timeout -> FATAL (exit 2)"
else echo "[FAIL] app-readiness-timeout expected FATAL(2)+message, got exit ${rc}"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi

# =============================================================================
# malformed machine + --app-cmd -> FATAL, AND the detached app is torn down (G2: the throw runs the
# harness `finally` before crawl().catch converts to FATAL; a die() there would orphan serve.mjs).
# =============================================================================
em="$(newexport badmachine)"; printf 'this is not json\n' > "$em/machine.review.json"; restamp "$em"
mport="$(freeport_once)"
out="$(bash "$GATE" "$em" --app-url "http://127.0.0.1:${mport}/" \
  --app-cmd "node ${APP}/serve.mjs --dir ${DIST} --port ${mport}" \
  --results "$RESULTS" --base "$REPO" --timeout "$GTIMEOUT" 2>&1)"; rc=$?
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -qE "cannot parse machine"; then
  echo "[PASS] malformed machine -> FATAL (exit 2)"
else echo "[FAIL] malformed machine expected FATAL(2)+message, got exit ${rc}"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi
TESTS_RUN=$((TESTS_RUN + 1))
if app_torn_down "$mport"; then echo "[PASS] malformed-machine app torn down (port ${mport}, no orphan listener)"
else echo "[FAIL] malformed-machine leaked serve.mjs (port ${mport} still accepting)"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi

# =============================================================================
# no runtime — Playwright absent in the harness dir -> FATAL (2), never a silent skip (F-008).
# A harness dir carrying pen-harness.mjs but NO node_modules/playwright; the gate FATALs at its
# presence check BEFORE the crawl, so no server is needed.
# =============================================================================
NOPW="$WORK/harness-no-pw"; mkdir -p "$NOPW"; cp "${HARNESS_DIR}/pen-harness.mjs" "$NOPW/"
out="$(PEN_HARNESS_DIR="$NOPW" bash "$GATE" "$EXP" --app-url "http://127.0.0.1:1/" \
  --results "$RESULTS" --base "$REPO" 2>&1)"; rc=$?
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -qE "Playwright is not installed"; then
  echo "[PASS] Playwright absent -> FATAL (F-008 no silent skip)"
else echo "[FAIL] Playwright-absent expected FATAL(2)+message, got exit ${rc}"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi

# =============================================================================
# assert_red_when_guard_removed on the load-bearing guards: good=0, mutant≠0. Each mutant ISOLATES
# its guard. gcmd allocates a fresh server per invocation inside the eval'd subshell.
# =============================================================================
assert_red_when_guard_removed "$(gcmd "$EXP" "$DIST" "" "$RESULTS")" "$(gcmd "$EXP" "$DIST" "?omit=list/search" "$RESULTS")"
assert_red_when_guard_removed "$(gcmd "$EXP" "$DIST" "" "$RESULTS")" "$(gcmd "$EXP" "$DIST" "?extra=1" "$RESULTS")"
assert_red_when_guard_removed "$(gcmd "$EXP" "$DIST" "" "$RESULTS")" "$(gcmd "$EXP" "$DIST" "?dup=_shell/home" "$RESULTS")"
eU="$(newexport red-unreach)"; add_unreachable_state "$eU"
assert_red_when_guard_removed "$(gcmd "$EXP" "$DIST" "" "$RESULTS")" "$(gcmd "$eU" "$DIST" "" "$RESULTS" 0 "$UNREACH_TO")"
assert_red_when_guard_removed "$(gcmd "$EXP" "$DIST" "" "$RESULTS")" "$(gcmd "$EXP" "$DIST" "" "$RESULTS" 1)"

test_summary
