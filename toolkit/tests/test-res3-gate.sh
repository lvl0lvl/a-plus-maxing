#!/usr/bin/env bash
# tests/test-res3-gate.sh — F-007 negative test for scripts/res3-gate.sh (the §6.3 res-3 gate).
#
# F-007 obligation: a gate that cannot prove it goes RED on bad input enforces nothing. The res-3
# gate drives per-element EXECUTED E2Es against the built React fixture (tests/fixtures/seam-gate/)
# and runs the two mutation proofs; this suite drives the REAL runtime — headless Chromium via the
# pen-harness — and proves each verdict and every guard against guard-EXCLUSIVE anchors:
#   GOOD              full app + valid status-note sign-off                    -> PASS (0).
#   dead handler      ?dead=<oid> ships a neutralized handler                  -> FAIL (1): e2ePass RED.
#   vacuous E2E       an e2e effect that stays true when the handler is stubbed-> FAIL (1): dependence GREEN.
#   placement RED     a multi-field entity: the write redirect lands observably
#                     in a sibling                                             -> PASS (0), placement RED.
#   instance collapse ?collapse=1 (row-N-affects-row-0)                        -> FAIL (1): e2ePass RED.
#   UNPROVABLE        single-field note, NO sign-off                           -> FAIL (1) fail-closed;
#                     VALID sign-off (= GOOD)                                  -> PASS (0);
#                     STALE sign-off (wrong digest)                            -> FAIL (1) self-void;
#                     STALE via DESIGN change (valid digest, edited design)    -> FAIL (1) self-void.
#   NA-EPHEMERAL      ephemeral rows PASS with no sign-off (GOOD); a vacuous
#                     ephemeral E2E                                            -> FAIL (1) (proof (a) RED-capable).
#   placement GREEN   a key-blind backend keeps the redirected write in the correct field (vacuous
#                     placement) (H4)                                          -> FAIL (1).
#   reset isolation   a no-op /api/__reset (200 that does NOT clear) (H3)      -> FATAL (2), never
#                     swallowed; a 2-writer repro: CONTROL(working reset) mis-wired writer -> FAIL(1),
#                     TRIGGER(no-op reset) -> FATAL(2) (residual would have laundered it to PASS).
#   non-persist E2E   a persisted row whose e2e effect ≠ persist (H6)          -> FATAL (2), not sign-off-able.
#   orphan e2e        an e2e spec for an oid with no manifest row (H13)        -> FATAL (2), not dropped.
#   missing E2E       a closed res-3 row with no e2e definition (NEW-2)        -> FAIL (1).
#   PENDING           a res-3 row in an OPEN wave                              -> PASS (0), PENDING (not FAIL).
#   §6.2 hard-dep     a corrupt export digest                                  -> FATAL (2) WITHOUT a RESULT verdict.
#   PEN-CHANGED       a pen-changed export set                                 -> PASS (0) + marker.
#   structural FATALs zero-row / manifest-not-array / results-not-dict / rows-not-list / duplicate
#                     results row / invalid wave value / row-references-absent-wave / exceptions-not-
#                     array / no-res-3-row floor                               -> FATAL (2), each anchored.
#   app-readiness     an --app-cmd that never serves --app-url                 -> FATAL (2).
#   no runtime        Playwright absent in the harness dir                     -> FATAL (2), never a
#                     silent skip (F-008).
#   assert_red_when_guard_removed on the load-bearing guards (dead, vacuous, collapse, no-sign-off, placement-GREEN):
#                     good=0, mutant=non-zero.
#
# PORTS / TIMING (G9): the fixture server binds port 0 and PRINTS the bound port; this suite parses
# that actually-bound port (no allocate-then-close race). The res-3 run drives ~13 browser contexts
# per gate invocation (5 elements x primary+proof(a)[+proof(b)]), so it is heavier than the seam crawl.
#
# READINESS: needs node + the harness's Playwright + a launchable Chromium + the built fixture. On a
# box without them it LOUD-SKIPS (exit 0) so run-all-tests stays green; the full F-007 proofs run
# wherever the one-time install+build (fixture README) has been done. NOT a gate skip — the GATE
# itself FATALs on absent Playwright (tested below); this is the test harness declining its substrate.
#
# NOT hermetic re the .pen (mirrors test-seam-gate): the §6.2 hard dependency runs against the REAL
# committed .pen (--base = repo root). App/export mutations are made on COPIES in a temp dir. The run
# is localhost-only — no network beyond 127.0.0.1 at test time.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/res3-gate.sh"
DIGEST="${TEST_DIR}/../scripts/pen-digest.sh"
HARNESS_DIR="${TEST_DIR}/../harness"
REPO="$(cd "${TEST_DIR}/../../../.." && pwd)"          # skills_library repo root
FIX="${TEST_DIR}/fixtures/seam-gate"
EXP="${FIX}/design/interaction-model"
APP="${FIX}/app"
DIST="${APP}/dist"
RESULTS="${FIX}/wiring-results.json"
GTIMEOUT="10000"

# ---- readiness / loud skip ---------------------------------------------------
skip() { echo "[test-res3-gate] SKIP (loud): $1"; echo "[test-res3-gate] to run the full F-007 res-3 proofs: (cd ${APP} && npm ci && npm run build) && (cd ${HARNESS_DIR} && npm ci && npx playwright install chromium)"; exit 0; }
# Portability (update-rigor): resolves a committed .pen via --base "$REPO" — content OUTSIDE
# toolkit/ that does not travel with a toolkit copy. In a consuming project, LOUD-SKIP so the
# pulled suite stays green; the framework repo still runs the full res-3 proofs.
[ -d "$REPO/designs/fixtures" ] || skip "design fixtures absent under REPO ($REPO) — not a design-pipeline checkout"
command -v node >/dev/null 2>&1 || skip "node not found"
command -v python3 >/dev/null 2>&1 || skip "python3 not found"
[ -d "${HARNESS_DIR}/node_modules/playwright" ] || skip "Playwright not installed in the harness (${HARNESS_DIR})"
[ -d "${APP}/node_modules" ] || skip "fixture app deps not installed (${APP}/node_modules)"
if [ ! -f "${DIST}/index.html" ]; then ( cd "$APP" && npm run build >/dev/null 2>&1 ) || skip "fixture app build failed"; fi
( cd "$HARNESS_DIR" && node -e "require('playwright').chromium.launch({headless:true}).then(b=>b.close()).catch(()=>process.exit(3))" ) >/dev/null 2>&1 || skip "Chromium not launchable (run: npx playwright install chromium in ${HARNESS_DIR})"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/res3-gate.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

freeport_once() { python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()'; }

# start_server <distdir> [serveSchema] -> prints "<pid> <port>"; parses the printed bound port.
start_server() {
  local dist="$1" sschema="${2:-}" senv="${3:-}" outfile pid line port i
  outfile="$(mktemp "$WORK/serve.XXXXXX")"
  local sargs=(--dir "$dist" --port 0)
  [ -n "$sschema" ] && sargs+=(--schema "$sschema")
  # shellcheck disable=SC2086  # $senv is a space-separated KEY=VAL list (serve test flags), split intentionally
  env $senv node "$APP/serve.mjs" "${sargs[@]}" >"$outfile" 2>&1 &
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

# run_gate <exportdir> <appdir> <query> <results> [serveSchema] [timeout] [serveEnv] -> stdout, returns exit
run_gate() {
  local exp="$1" app="$2" query="$3" results="$4" sschema="${5:-}" to="${6:-$GTIMEOUT}" senv="${7:-}" sp pid port out rc
  sp="$(start_server "$DIST" "$sschema" "$senv")" || { echo "[test-error] fixture server failed to start"; return 97; }
  pid="${sp%% *}"; port="${sp##* }"
  out="$(bash "$GATE" "$exp" --app "$app" \
    --app-url "http://127.0.0.1:${port}/${query}" \
    --results "$results" --base "$REPO" --timeout "$to" 2>&1)"; rc=$?
  kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
  printf '%s' "$out"
  return "$rc"
}

guard_run() { run_gate "$1" "$2" "$3" "$4" "${5:-}" "${6:-$GTIMEOUT}" "${7:-}" >/dev/null 2>&1; }
gcmd() { printf 'guard_run %q %q %q %q %q %q %q' "$1" "$2" "$3" "$4" "${5:-}" "${6:-$GTIMEOUT}" "${7:-}"; }

CK_PRESENT=""; CK_ABSENT=""
# check <label> <exp_exit> <exportdir> <app> <query> <results> [serveSchema] [timeout] [serveEnv]
check() {
  local label="$1" exp_exit="$2" out rc
  out="$(run_gate "$3" "$4" "$5" "$6" "${7:-}" "${8:-$GTIMEOUT}" "${9:-}")"; rc=$?
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
restamp() { local h; h="$(bash "$DIGEST" "$1")"; python3 -c "
f='$1/export.digest'; h='$h'
out=['content-sha256: '+h if ln.startswith('content-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"; }
mutate_index() { python3 -c "p='$1/index.md';s=open(p).read();open(p,'w').write(s.replace('Inventory','Xnventory',1))"; }
penchange_export() { python3 -c "
f='$1/export.digest'
out=['pen-sha256: deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef' if ln.startswith('pen-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"; }
zero_manifest() { printf '[]\n' > "$1/wiring-manifest.json"; restamp "$1"; }
manifest_not_array() { printf '{}\n' > "$1/wiring-manifest.json"; restamp "$1"; }
navigate_only_manifest() { python3 -c "
import json; p='$1/wiring-manifest.json'; m=json.load(open(p))
keep=[r for r in m if not (isinstance(r.get('writes'),list) and any(isinstance(x,str) for x in r['writes'])) and r.get('ephemeral') is not True]
open(p,'w').write(json.dumps(keep,indent=2,sort_keys=True)+chr(10))
"; restamp "$1"; }
set_exceptions() { printf '%s\n' "$2" > "$1/exceptions.json"; restamp "$1"; }
mutate_e2e_vacuous() { python3 -c "
import json; p='$1/e2e.review.json'; j=json.load(open(p))
j['e2e']['list/open-filters']['effect']={'kind':'present','oid':'list/open-detail'}
open(p,'w').write(json.dumps(j,indent=2)+chr(10))
"; }
remove_e2e_row() { python3 -c "
import json; p='$1/e2e.review.json'; j=json.load(open(p)); j['e2e'].pop('$2',None)
open(p,'w').write(json.dumps(j,indent=2)+chr(10))
"; }
mfapp() { local d="$WORK/mfapp"; mkdir -p "$d"; printf '{ "incident": ["id", "title", "status"], "note": ["text", "author"] }\n' > "$d/schema.json"; echo "$d"; }
results_set() { python3 - "$RESULTS" "$1" "$2" <<'PY'
import json, sys
src, dst, expr = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(src)); exec(expr)
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}
mutate_e2e_nonpersist() { python3 -c "
import json; p='$1/e2e.review.json'; j=json.load(open(p))
j['e2e']['detail/status-note']['effect']={'kind':'present','oid':'detail/status-note'}
open(p,'w').write(json.dumps(j,indent=2)+chr(10))
"; }
orphan_e2e() { python3 -c "
import json; p='$1/e2e.review.json'; j=json.load(open(p))
j['e2e']['list/ghost']={'drive':[{'click':'list/ghost'}],'effect':{'kind':'present','oid':'list/ghost'}}
open(p,'w').write(json.dumps(j,indent=2)+chr(10))
"; }
# design_digest — the res-3 sign-off referent (mirrors res3-gate.sh: §5 set minus exceptions.json).
design_digest() {
  local dir="$1" ht m; local files
  if command -v shasum >/dev/null 2>&1; then ht="shasum -a 256"; else ht="sha256sum"; fi
  files=("$dir/index.md")
  while IFS= read -r m; do [ -n "$m" ] && files+=("$m"); done < <(LC_ALL=C find "$dir" -maxdepth 1 -name 'machine.*.json' | LC_ALL=C sort)
  files+=("$dir/wiring-manifest.json" "$dir/retired-wireids.txt" "$dir/config.json")
  LC_ALL=C sed -e 's/[[:space:]]*$//' "${files[@]}" | $ht | awk '{print $1}'
}
# add_second_writer — a SECOND persisted note.text writer (status-note2). App renders it (mis-wired)
# only under ?twowriters. Re-signs status-note against the NEW design-digest (the manifest change
# self-voids the committed sign-off); status-note2 needs no sign-off (it FAILs/FATALs before that).
add_second_writer() {
  python3 -c "
import json
d='$1'
m=json.load(open(d+'/wiring-manifest.json'))
m.append({'action':'submit','destination':'self','endpoint':['POST /api/note'],'ephemeral':False,'name':'btn/status-note2','reads':[],'screen':'screen/detail','status':'planned','wireId':'status-note2','writes':['note.text']})
open(d+'/wiring-manifest.json','w').write(json.dumps(m,indent=2,sort_keys=True)+chr(10))
j=json.load(open(d+'/e2e.review.json'))
j['e2e']['detail/status-note2']={'drive':[{'click':'list/open-detail'},{'click':'detail/status-note2'}],'effect':{'kind':'persist','entity':'note','field':'text','value':'reviewed'}}
open(d+'/e2e.review.json','w').write(json.dumps(j,indent=2)+chr(10))
"
  local dd; dd="$(design_digest "$1")"
  set_exceptions "$1" '[ { "date": "2026-07-03", "designDigest": "'"$dd"'", "reason": "single-field note; reviewer confirmed", "screen": "screen/detail", "signedBy": "test", "wireId": "status-note" } ]'
}
results_two_writers() { python3 - "$RESULTS" "$1" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
r = json.load(open(src)); r['rows'].append({'screen':'screen/detail','wireId':'status-note2','wave':1})
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}

# the committed status-note sign-off digest (see exceptions.json / fixture README)
GOOD_DIGEST="5ddc8349019840733e9b65d551755b3d9a890c3b90c57b8c342f8046e6ff9bb7"
SIGNOFF_VALID='[ { "date": "2026-07-03", "designDigest": "'"$GOOD_DIGEST"'", "reason": "single-field note; reviewer confirmed", "screen": "screen/detail", "signedBy": "test", "wireId": "status-note" } ]'
SIGNOFF_STALE='[ { "date": "2026-07-03", "designDigest": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef", "reason": "stale", "screen": "screen/detail", "signedBy": "test", "wireId": "status-note" } ]'

# =============================================================================
# GOOD -> PASS (0). The committed fixture carries the valid status-note sign-off.
# =============================================================================
CK_PRESENT="RESULT: PASS"; CK_ABSENT="RESULT: FAIL"
check "GOOD full app + valid sign-off" 0 "$EXP" "$APP" "" "$RESULTS"

# =============================================================================
# dead handler -> FAIL (e2ePass RED). ?dead neutralizes status-note's handler in the running app.
# =============================================================================
CK_PRESENT="detail/status-note: the executed E2E did not pass"
check "dead handler ships -> FAIL" 1 "$EXP" "$APP" "?dead=detail/status-note" "$RESULTS"

# =============================================================================
# vacuous E2E plant -> dependence GREEN -> FAIL. e2e.review.json is not in the digest set, so no
# restamp is needed. open-filters' effect is rewritten to assert an ALWAYS-present element.
# =============================================================================
e="$(newexport vacuous)"; mutate_e2e_vacuous "$e"
CK_PRESENT="list/open-filters: dependence proof \(a\) did NOT go RED"
check "vacuous E2E -> dependence GREEN -> FAIL" 1 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# placement RED -> PASS. A multi-field `note` (temp schema) gives the redirect an observable sibling,
# so the placement proof lands the value in the wrong field and the E2E goes RED (a VALID proof).
# =============================================================================
mf="$(mfapp)"
CK_PRESENT="RESULTS-ROW detail/status-note.*placement:RED"; CK_ABSENT="RESULT: FAIL"
check "placement redirect catches a wrong-location write -> PASS" 0 "$EXP" "$mf" "" "$RESULTS" "$mf/schema.json"

# =============================================================================
# placement GREEN -> FAIL (H4). A key-blind / echo-both backend stores the value into the correct
# field regardless of the redirected key, so the persist assertion stays green after redirect —
# a VACUOUS placement assertion the gate must catch. Multi-field so computePlacement takes the
# sibling branch (the only branch that can yield GREEN).
# =============================================================================
CK_PRESENT="placement proof \(b\) did NOT go RED \(GREEN\)"
check "H4 placement GREEN (key-blind backend) -> FAIL" 1 "$EXP" "$mf" "" "$RESULTS" "$mf/schema.json" "$GTIMEOUT" "PEN_SERVE_KEYBLIND=1"

# =============================================================================
# H3 reset-isolation — a no-op reset (200 that does NOT clear) must be CAUGHT (not swallowed): a
# persist run whose per-run isolation cannot be confirmed is unconstructible -> problem -> FATAL.
# =============================================================================
CK_PRESENT="isolation could not be established"; CK_ABSENT="RESULT: (PASS|FAIL) "
check "H3 no-op reset -> FATAL (isolation unconfirmed)" 2 "$EXP" "$APP" "" "$RESULTS" "" "$GTIMEOUT" "PEN_SERVE_NOOP_RESET=1"

# =============================================================================
# H3 2-writer false-PASS (the triage repro). ?twowriters adds a mis-wired second note.text writer
# (POSTs {wrong:...}, never persists note.text). CONTROL (working reset): the mis-wired writer FAILs
# (e2ePass false); status-note passes -> RESULT FAIL. TRIGGER (no-op reset): the residual store would
# have laundered the mis-wired writer to PASS -> now both persisted rows FATAL, NOT PASS.
# =============================================================================
e2w="$(newexport twowriters)"; add_second_writer "$e2w"; results_two_writers "$WORK/res-2w.json"
CK_PRESENT="detail/status-note2: the executed E2E did not pass"; CK_ABSENT="RESULT: PASS"
check "H3 2-writer CONTROL (working reset): mis-wired writer FAILs" 1 "$e2w" "$APP" "?twowriters=1" "$WORK/res-2w.json"

CK_PRESENT="isolation could not be established"; CK_ABSENT="RESULT: PASS"
check "H3 2-writer TRIGGER (no-op reset): FATAL, not laundered to PASS" 2 "$e2w" "$APP" "?twowriters=1" "$WORK/res-2w.json" "" "$GTIMEOUT" "PEN_SERVE_NOOP_RESET=1"

# =============================================================================
# H6 — a persisted row whose e2e effect is NOT a persist assertion is a construction FATAL (a
# mis-authored non-persist E2E must not be laundered through a sign-off-able UNPROVABLE).
# =============================================================================
e="$(newexport h6)"; mutate_e2e_nonpersist "$e"
CK_PRESENT="not a persist assertion — the placement proof cannot be constructed"
check "H6 persisted row + non-persist E2E -> FATAL" 2 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# H13 — an orphan e2e spec (references an oid with no manifest row) must not be silently dropped.
# =============================================================================
e="$(newexport h13)"; orphan_e2e "$e"
CK_PRESENT="orphan e2e observation: 'list/ghost'"
check "H13 orphan e2e spec -> FATAL" 2 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# instance collapse (?collapse=1) -> FAIL (row-N-affects-row-0).
# =============================================================================
CK_PRESENT="list/incident-row: the executed E2E did not pass.*instance collapse"
check "instance collapse (row-N->row-0) -> FAIL" 1 "$EXP" "$APP" "?collapse=1" "$RESULTS"

# =============================================================================
# UNPROVABLE sign-off directions.
# =============================================================================
e="$(newexport nosignoff)"; set_exceptions "$e" '[]'
CK_PRESENT="placement UNPROVABLE with NO exceptions.json sign-off"
check "UNPROVABLE, no sign-off -> FAIL" 1 "$e" "$APP" "" "$RESULTS"

e="$(newexport stalewrong)"; set_exceptions "$e" "$SIGNOFF_STALE"
CK_PRESENT="placement UNPROVABLE and the sign-off is STALE"
check "UNPROVABLE, stale (wrong digest) sign-off -> FAIL" 1 "$e" "$APP" "" "$RESULTS"

# self-void via DESIGN change: keep the (originally-valid) sign-off, edit a design file so the
# design-digest moves; §6.2 is re-stamped so the hard dep passes and the STALE check is reached.
e="$(newexport staledesign)"; set_exceptions "$e" "$SIGNOFF_VALID"; mutate_index "$e"; restamp "$e"
CK_PRESENT="the sign-off is STALE"
check "UNPROVABLE, sign-off self-voided by design change -> FAIL" 1 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# missing E2E for a closed res-3 row (NEW-2) -> FAIL. Remove status-note's e2e definition.
# =============================================================================
e="$(newexport noe2e)"; remove_e2e_row "$e" "detail/status-note"
CK_PRESENT="detail/status-note: no executed E2E \(no observation\)"
check "closed res-3 row with no E2E (NEW-2) -> FAIL" 1 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# PENDING: status-note in an OPEN wave -> PENDING, not FAIL (even though UNPROVABLE would FAIL closed).
# =============================================================================
results_set "$WORK/res-note-open.json" "[row.__setitem__('wave', 2) for row in r['rows'] if row['screen']=='screen/detail' and row['wireId']=='status-note']"
CK_PRESENT="PENDING: detail/status-note"; CK_ABSENT="RESULT: FAIL"
check "res-3 row in an OPEN wave -> PENDING" 0 "$EXP" "$APP" "" "$WORK/res-note-open.json"

# =============================================================================
# §6.2 hard-dependency [T-3d] — corrupt digest -> FATAL WITHOUT running the E2E / a RESULT verdict.
# =============================================================================
e="$(newexport corrupt)"; mutate_index "$e"   # no restamp -> content-sha256 mismatch
CK_PRESENT="refusing to run res-3"; CK_ABSENT="\[res3-gate\] RESULT: (PASS|FAIL)"
check "§6.2 hard-dep corrupt -> FATAL, no own verdict" 2 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# PEN-CHANGED propagation -> PASS-WITH-PEN-CHANGED.
# =============================================================================
e="$(newexport penchanged)"; penchange_export "$e"
CK_PRESENT="RESULT: PASS-WITH-PEN-CHANGED"
check "PEN-CHANGED propagation" 0 "$e" "$APP" "" "$RESULTS"

# =============================================================================
# structural FATALs — each with a guard-exclusive anchor.
# =============================================================================
e="$(newexport zerorow)"; zero_manifest "$e"
CK_PRESENT="zero rows"
check "zero-row manifest -> FATAL" 2 "$e" "$APP" "" "$RESULTS"

e="$(newexport mfobj)"; manifest_not_array "$e"
CK_PRESENT="must be a JSON array of rows"
check "manifest not an array -> FATAL" 2 "$e" "$APP" "" "$RESULTS"

e="$(newexport navonly)"; navigate_only_manifest "$e"; remove_e2e_row "$e" "detail/status-note"
remove_e2e_row "$e" "list/open-filters"; remove_e2e_row "$e" "list/apply-filter"
remove_e2e_row "$e" "list/search"; remove_e2e_row "$e" "list/incident-row"
CK_PRESENT="NONE is a res-3 data-effect row"
check "manifest with no res-3 row -> FATAL (floor)" 2 "$e" "$APP" "" "$RESULTS"

e="$(newexport exobj)"; set_exceptions "$e" '{}'
CK_PRESENT="exceptions.json must be a JSON array"
check "exceptions not an array -> FATAL" 2 "$e" "$APP" "" "$RESULTS"

printf '[]\n' > "$WORK/res-notdict.json"
CK_PRESENT="must be a JSON object"
check "results not an object -> FATAL" 2 "$EXP" "$APP" "" "$WORK/res-notdict.json"

results_set "$WORK/res-rowsnull.json" "r['rows'] = None"
CK_PRESENT="'rows' must be a JSON array"
check "rows not a list -> FATAL" 2 "$EXP" "$APP" "" "$WORK/res-rowsnull.json"

results_set "$WORK/res-dup.json" "r['rows'].append({'screen':'screen/detail','wireId':'status-note','wave':1})"
CK_PRESENT="duplicate row for screen/detail/status-note"
check "duplicate results row -> FATAL" 2 "$EXP" "$APP" "" "$WORK/res-dup.json"

results_set "$WORK/res-badwave.json" "r['waves']['1'] = 'frozen'"
CK_PRESENT="expected .open."
check "invalid wave value -> FATAL" 2 "$EXP" "$APP" "" "$WORK/res-badwave.json"

results_set "$WORK/res-absentwave.json" "[row.__setitem__('wave', 9) for row in r['rows'] if row['screen']=='screen/detail' and row['wireId']=='status-note']"
CK_PRESENT="absent from the waves map"
check "row references absent wave -> FATAL" 2 "$EXP" "$APP" "" "$WORK/res-absentwave.json"

# =============================================================================
# app-readiness-timeout FATAL — --app-cmd that never serves --app-url.
# =============================================================================
deadport="$(freeport_once)"
out="$(PEN_HARNESS_READY_FLOOR_MS=1500 bash "$GATE" "$EXP" --app "$APP" \
  --app-url "http://127.0.0.1:${deadport}/" --app-cmd "sleep 30" \
  --results "$RESULTS" --base "$REPO" --timeout 800 2>&1)"; rc=$?
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -qE "did not become ready"; then
  echo "[PASS] app-readiness-timeout -> FATAL (exit 2)"
else echo "[FAIL] app-readiness-timeout expected FATAL(2)+message, got exit ${rc}"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi

# =============================================================================
# no runtime — Playwright absent in the harness dir -> FATAL (2), never a silent skip (F-008).
# =============================================================================
NOPW="$WORK/harness-no-pw"; mkdir -p "$NOPW"; cp "${HARNESS_DIR}/pen-harness.mjs" "$NOPW/"
out="$(PEN_HARNESS_DIR="$NOPW" bash "$GATE" "$EXP" --app "$APP" --app-url "http://127.0.0.1:1/" \
  --results "$RESULTS" --base "$REPO" 2>&1)"; rc=$?
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -qE "Playwright is not installed"; then
  echo "[PASS] Playwright absent -> FATAL (F-008 no silent skip)"
else echo "[FAIL] Playwright-absent expected FATAL(2)+message, got exit ${rc}"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi

# =============================================================================
# assert_red_when_guard_removed on the load-bearing guards: good=0, mutant≠0.
# =============================================================================
assert_red_when_guard_removed "$(gcmd "$EXP" "$APP" "" "$RESULTS")" "$(gcmd "$EXP" "$APP" "?dead=detail/status-note" "$RESULTS")"
assert_red_when_guard_removed "$(gcmd "$EXP" "$APP" "" "$RESULTS")" "$(gcmd "$EXP" "$APP" "?collapse=1" "$RESULTS")"
eNS="$(newexport red-nosignoff)"; set_exceptions "$eNS" '[]'
assert_red_when_guard_removed "$(gcmd "$EXP" "$APP" "" "$RESULTS")" "$(gcmd "$eNS" "$APP" "" "$RESULTS")"
# H4 placement-GREEN guard: good = multi-field placement RED (exit 0); mutant = key-blind backend so
# the redirect stays green -> placement GREEN -> FAIL (exit 1).
assert_red_when_guard_removed "$(gcmd "$EXP" "$mf" "" "$RESULTS" "$mf/schema.json")" "$(gcmd "$EXP" "$mf" "" "$RESULTS" "$mf/schema.json" "$GTIMEOUT" "PEN_SERVE_KEYBLIND=1")"

test_summary
