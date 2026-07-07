#!/usr/bin/env bash
# toolkit/scripts/res3-gate.sh — the §6.3 resolution-3 gate (executed E2E + dual mutation proofs).
#
# The FINAL wiring-gate increment. res-1/res-2 (static: element built + endpoint served + schema
# real) are scripts/wiring-gate.sh; §6.4 structural carry is scripts/seam-gate.sh; THIS gate proves
# res-3: for every closed-wave element with a DATA-EFFECT, an executed E2E drives it by data-oid
# (data-oiid per instance), asserts the effect landed in the CORRECT place, and survives NEITHER
# mutation proof. It is a NEW runtime gate beside seam-gate; the static gates stay node-free.
#
# WHAT THIS BASH ENTRY OWNS (harness-substrate-memo §4): arg parsing; the §6.2 export-integrity
# HARD DEPENDENCY; the node/Playwright presence check (FATAL, never a silent skip — F-008);
# PEN-CHANGED propagation; running the harness e2e mode; and the VERDICT (embedded python over the
# harness observations — the pen-lint/wiring-gate idiom; node replaces python for the runtime step).
#
# WHICH ROWS res-3 GATES (a closed-wave row with a DATA-EFFECT):
#   persisted     non-empty `writes`  -> proof (a) dependence AND proof (b) placement.
#   ephemeral     ephemeral:true + empty `writes` -> proof (a) against the localEffect;
#                 placement is NA-EPHEMERAL (no persisted write to redirect; no sign-off) [PA-1].
#   NOT gated     no `writes` and not ephemeral (navigate / intra-screen transition): the data-effect
#                 is a state transition, proven by res-1 (handler resolves) + seam (renders) + the
#                 statechart. res-3's placement enum ({RED,GREEN,UNPROVABLE,NA-EPHEMERAL}) has no
#                 state for a non-writing non-ephemeral row, and spec N-2 defers call-target
#                 verification to Phase-2+; so these rows carry no res-3 obligation here.
#
# THE VERDICT (per res-3 / §6.6, under §6.3 wave semantics):
#   closed-wave res-3 row: e2ePass MUST be true; dependence MUST be RED (a GREEN dependence => the
#     E2E does not depend on the handler => vacuous => FAIL); placement:
#       RED           proven (write redirect observably landed wrong) -> OK.
#       GREEN         vacuous placement assertion -> FAIL.
#       NA-EPHEMERAL  ephemeral+empty writes -> OK (no sign-off).
#       UNPROVABLE    persisted, no observable redirect target -> requires a VALID exceptions.json
#                     sign-off keyed (screen,wireId) + the current DESIGN-DIGEST; else FAIL.
#     an oiid row that COLLAPSED (driving instance k affected another row) fails e2ePass -> FAIL.
#     a closed res-3 row with NO observation (no E2E) -> FAIL (NEW-2: the register is never a pass
#       input; a missing E2E is unresolved, not a silent pass).
#   not-started wave (open / absent results row) -> PENDING (surfaced, not FAIL — mirrors wiring/seam).
#   structural problems -> FATAL.
#
# UNPROVABLE SIGN-OFF DIGEST [F-C, implementer note]: the sign-off is keyed by the DESIGN-DIGEST —
#   the §5 content canonicalization over the export set EXCLUDING exceptions.json. The §6.2
#   content-sha256 INCLUDES exceptions.json (so §6.2 detects hand-edits to the sign-off store), which
#   makes it CIRCULAR as the sign-off's own referent: adding the sign-off changes the digest it would
#   have to name. The design-digest is the non-circular referent that still delivers the spec's stated
#   property — "self-voiding when the DESIGN changes" — because a manifest/machine/index/config/retired
#   edit changes it, while granting the sign-off (an exceptions.json edit) does not. The gate emits the
#   current design-digest so a reviewer can author the sign-off against it.
#
# EXIT CONTRACT (0 PASS / 1 FAIL / 2 FATAL, fail-closed per F-008) — output frozen like §6.2/§6.3/§6.4:
#   RESULT is one of PASS / FAIL / FATAL / PASS-WITH-PEN-CHANGED.
#   2 FATAL  — the §6.2 hard dependency FAILed/FATALed (own checks NOT run); node/Playwright absent;
#              the app unreachable / hydration timeout; browser launch failure; an unparseable
#              manifest / results / schema / exceptions / observations; a wiring-results inconsistency;
#              a zero-row manifest; a harness that could not CONSTRUCT a required proof; a res-3-gated
#              row the harness reported as a `problem`.
#   1 FAIL   — a closed-wave res-3 row that fails e2ePass, a dependence proof that stayed GREEN, a
#              placement GREEN, an UNPROVABLE without a valid sign-off, or a missing E2E.
#   0 PASS   — every closed-wave res-3 obligation resolved; not-started rows PENDING/informational.
#              A propagated PEN-CHANGED keeps exit 0 but marks RESULT PASS-WITH-PEN-CHANGED.
#   VERDICT PRECEDENCE [toolkit convention]: a FAIL (violation) exits 1 BEFORE a co-occurring FATAL
#   exits 2. Structural FATALs are detected UP FRONT and verdict early, so an exit-2 case is never
#   downgraded by a later closed-wave FAIL.
#   AUDIT_ALLOW_SKIP=1 is passed through to the §6.2 hard dependency only; this gate has no skip path.
#
# Usage: res3-gate.sh <export-dir> --app <app-dir> --app-url <url> [--app-cmd <cmd>]
#                     --results <results.json> [--base <repo-root>] [--timeout <ms>] [--browser chromium]
#   <export-dir>  design/interaction-model dir: wiring-manifest.json + e2e.*.json + exceptions.json + §6.2 set.
#   --app         the built app dir (schema.json = the implemented data model; the res-2/placement referent).
#   --app-url     where the HYDRATED app is reachable (REQUIRED).
#   --app-cmd     OPTIONAL: the harness starts it, waits for --app-url ready, tears it down after.
#   --results     wiring-results.json (§6.6) — the wave register (format-v0).
#   --base        repo root for the §6.2 gate's pinned-.pen resolution. Default $PWD.
set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-res3-gate}"
emit() { echo "[${AUDIT_TAG}] $*"; }
fatal() { emit "FATAL: $*"; exit 2; }

DIR=""
APP=""
APP_URL=""
APP_CMD=""
RESULTS=""
BASE="$PWD"
TIMEOUT="8000"
BROWSER="chromium"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --app) shift; [ "$#" -gt 0 ] || fatal "--app needs a value"; APP="$1" ;;
    --app=*) APP="${1#*=}" ;;
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
    -h|--help) sed -n '2,71p' "$0"; exit 0 ;;
    --*) fatal "unknown arg: $1" ;;
    *) [ -z "$DIR" ] && DIR="$1" || fatal "unexpected extra arg: $1" ;;
  esac
  shift
done

[ -n "$DIR" ] || fatal "usage: res3-gate.sh <export-dir> --app <app-dir> --app-url <url> [--app-cmd <cmd>] --results <results.json> [--base <repo-root>]"
[ -d "$DIR" ] || fatal "export dir not found / not a directory: $DIR"
[ -n "$APP" ] || fatal "--app <app-dir> is required (the res-2/placement referent: schema.json)"
[ -d "$APP" ] || fatal "app dir not found / not a directory: $APP"
[ -f "$APP/schema.json" ] || fatal "app dir has no schema.json (the implemented data model — placement-proof sibling referent)"
[ -n "$APP_URL" ] || fatal "--app-url <url> is required (where the hydrated app is reachable)"
[ -n "$RESULTS" ] || fatal "--results <results.json> is required"
[ -f "$RESULTS" ] || fatal "wiring-results.json not found: $RESULTS"
MANIFEST="$DIR/wiring-manifest.json"
[ -f "$MANIFEST" ] || fatal "export dir has no wiring-manifest.json: $MANIFEST"
EXCEPTIONS="$DIR/exceptions.json"
[ -f "$EXCEPTIONS" ] || fatal "export dir has no exceptions.json (the UNPROVABLE sign-off store; an empty [] is valid)"
E2ES=()
while IFS= read -r e; do [ -n "$e" ] && E2ES+=("$e"); done \
  < <(LC_ALL=C find "$DIR" -maxdepth 1 -name 'e2e.*.json' 2>/dev/null | LC_ALL=C sort)
[ "${#E2ES[@]}" -gt 0 ] || fatal "export dir has no e2e.*.json (the res-3 E2E definitions the harness drives): $DIR"
command -v python3 >/dev/null 2>&1 || fatal "python3 required to compute the res3-gate verdict"

HERE="$(cd "$(dirname "$0")" && pwd)"
INTEGRITY_SH="$HERE/pen-integrity.sh"
[ -f "$INTEGRITY_SH" ] || fatal "pen-integrity.sh not found next to this gate ($INTEGRITY_SH) — the §6.2 hard dependency is missing"
HARNESS_DIR="${PEN_HARNESS_DIR:-$HERE/../harness}"
HARNESS="$HARNESS_DIR/pen-harness.mjs"

# ============= node / Playwright presence — FATAL, never a silent skip (F-008) =========
command -v node >/dev/null 2>&1 || fatal "node is required for the §6.3 res-3 executed-E2E gate (runtime gate) — not found (F-008: no silent skip)"
[ -f "$HARNESS" ] || fatal "pen-harness.mjs not found at $HARNESS (harness missing)"
[ -d "$HARNESS_DIR/node_modules/playwright" ] || fatal "Playwright is not installed in the harness ($HARNESS_DIR) — run: (cd $HARNESS_DIR && npm ci && npx playwright install chromium). A runtime gate that cannot launch a browser FATALs; it never silently skips (F-008)"

# ============= DESIGN-DIGEST — the sign-off referent (§5 canonicalization minus exceptions.json) =====
# Mirrors scripts/pen-digest.sh EXCEPT it excludes exceptions.json, so granting a sign-off does not
# change the digest the sign-off names (non-circular), while a DESIGN edit does (self-voiding).
if command -v shasum >/dev/null 2>&1; then HASHTOOL="shasum -a 256"
elif command -v sha256sum >/dev/null 2>&1; then HASHTOOL="sha256sum"
else fatal "need shasum or sha256sum to compute the res-3 sign-off design-digest"; fi
DDFILES=("$DIR/index.md")
while IFS= read -r m; do [ -n "$m" ] && DDFILES+=("$m"); done \
  < <(LC_ALL=C find "$DIR" -maxdepth 1 -name 'machine.*.json' 2>/dev/null | LC_ALL=C sort)
for f in wiring-manifest.json retired-wireids.txt config.json; do
  [ -f "$DIR/$f" ] || fatal "export dir missing $f (design-digest input)"
  DDFILES+=("$DIR/$f")
done
DESIGN_DIGEST="$(LC_ALL=C sed -e 's/[[:space:]]*$//' "${DDFILES[@]}" | $HASHTOOL | awk '{print $1}')"
[ -n "$DESIGN_DIGEST" ] || fatal "could not compute the res-3 design-digest"
emit "design-digest: $DESIGN_DIGEST (UNPROVABLE sign-off referent; excludes exceptions.json)"

# ================= HARD DEPENDENCY — §6.2 export integrity [T-3d] =============
integrity_out="$(bash "$INTEGRITY_SH" "$DIR" --base "$BASE" 2>&1)"; integrity_rc=$?
if [ "$integrity_rc" -ne 0 ]; then
  emit "note: §6.2 export-integrity hard dependency did not pass (exit ${integrity_rc}) — output below:"
  printf '%s\n' "$integrity_out" | sed 's/^/    /'
  fatal "refusing to run res-3 E2E on exports that failed §6.2 export-integrity (hard dependency [T-3d]) — fix integrity and re-run"
fi
emit "ok: §6.2 export-integrity hard dependency passed (exit 0)"
PEN_CHANGED=0
if printf '%s' "$integrity_out" | grep -q 'PEN-CHANGED'; then
  PEN_CHANGED=1
  emit "PEN-CHANGED: propagated from §6.2 export-integrity — the pinned .pen moved since extraction; wave-close is BLOCKED until a §6.5 re-extraction runs (re-emitted here so wave-close consumers see it through this gate)"
fi

# ================= run the harness e2e → observations.json ===================
OBS="$(mktemp "${TMPDIR:-/tmp}/res3-obs.XXXXXX")" || fatal "cannot create a temp observations file"
trap 'rm -f "$OBS"' EXIT
HARGS=(e2e --app-url "$APP_URL" --manifest "$MANIFEST" --schema "$APP/schema.json" \
  --results "$RESULTS" --oiid --out "$OBS" --timeout "$TIMEOUT" --browser "$BROWSER")
[ -n "$APP_CMD" ] && HARGS+=(--app-cmd "$APP_CMD")
for e in "${E2ES[@]}"; do HARGS+=(--e2e "$e"); done

harness_out="$(node "$HARNESS" "${HARGS[@]}" 2>&1)"; harness_rc=$?
printf '%s\n' "$harness_out" | sed 's/^/    [harness] /'
if [ "$harness_rc" -ne 0 ]; then
  fatal "the res-3 executed-E2E run could not complete (harness exit ${harness_rc}) — the gate cannot decide on a run it could not complete (fail-closed)"
fi
[ -s "$OBS" ] || fatal "the harness produced no observations.json — cannot decide (fail-closed)"

# ================= verdict (embedded python — pen-lint / wiring-gate idiom) =====
AUDIT_TAG="$AUDIT_TAG" RES3_PEN_CHANGED="$PEN_CHANGED" RES3_DESIGN_DIGEST="$DESIGN_DIGEST" \
python3 - "$OBS" "$MANIFEST" "$RESULTS" "$EXCEPTIONS" <<'PYEOF'
import json
import os
import sys

TAG = os.environ.get("AUDIT_TAG", "res3-gate")
PEN_CHANGED = os.environ.get("RES3_PEN_CHANGED", "0") == "1"
DESIGN_DIGEST = os.environ.get("RES3_DESIGN_DIGEST", "")
OBS_PATH, MANIFEST_PATH, RESULTS_PATH, EXCEPTIONS_PATH = sys.argv[1:5]

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
        emit("RESULT: PASS-WITH-PEN-CHANGED (res-3 clean; wave-close BLOCKED pending a §6.5 "
             "re-extraction — propagated from §6.2)")
        sys.exit(0)
    emit("RESULT: PASS (every closed-wave res-3 element drove a non-vacuous E2E and survived neither "
         "mutation proof)")
    sys.exit(0)


def load(path, what):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001 — any parse/IO error on a required input is FATAL
        fatal("cannot parse %s: %s" % (what, e))
        return None


def bare(screen):
    return screen[len("screen/"):] if isinstance(screen, str) and screen.startswith("screen/") else screen


obs = load(OBS_PATH, "observations.json")
if obs is None:
    verdict()
if not isinstance(obs, dict) or obs.get("mode") != "e2e":
    fatal("observations.json is not an e2e-mode artifact (mode=%r) — cannot decide" % (obs.get("mode") if isinstance(obs, dict) else None))
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

# ---- wiring-results wave register (structural, up front — mirrors §6.3/§6.4) ----
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


# ---- exceptions.json (UNPROVABLE sign-off store) ----
exceptions = load(EXCEPTIONS_PATH, "exceptions.json")
if exceptions is None:
    verdict()
if not isinstance(exceptions, list):
    fatal("exceptions.json must be a JSON array of sign-off entries (an empty [] is valid)")
    verdict()
signoffs = {}  # (screen, wireId) -> designDigest it was granted against
for ex in exceptions:
    if not isinstance(ex, dict) or "screen" not in ex or "wireId" not in ex:
        fatal("exceptions.json entry is malformed (needs screen + wireId): %r" % (ex,))
        continue
    signoffs[(ex["screen"], ex["wireId"])] = ex.get("designDigest")
if fatals:
    verdict()

# ---- harness observations, indexed by (screen, wireId) ----
obs_rows = {}
for r in obs.get("rows") or []:
    if isinstance(r, dict) and "screen" in r and "wireId" in r:
        obs_rows[(r["screen"], r["wireId"])] = r

# ---- a harness `problem` on a res-3-gated row is a construction FATAL (memo §4.4) ----
problems_by_oid = {}
for p in obs.get("problems") or []:
    if isinstance(p, dict) and p.get("oid"):
        problems_by_oid[p["oid"]] = p.get("reason", "")


def res3_gated(row):
    """(gated, kind) — kind in {'persisted','ephemeral'}; a data-effect row res-3 must prove."""
    writes = row.get("writes")
    has_writes = isinstance(writes, list) and any(isinstance(x, str) for x in writes)
    if has_writes:
        return (True, "persisted")
    if row.get("ephemeral") is True:
        return (True, "ephemeral")
    return (False, None)


# ---- per-row res-3 verdict under wave semantics ----
gated_seen = 0
manifest_oids = set()
for row in manifest:
    if not isinstance(row, dict):
        fail("manifest row is not an object: %r" % (row,))
        continue
    screen = row.get("screen")
    wid = row.get("wireId")
    oid = "%s/%s" % (bare(screen), wid)
    manifest_oids.add(oid)
    gated, kind = res3_gated(row)
    if not gated:
        emit("row %s: res-3 N/A (no persisted writes and not ephemeral — data-effect is a transition, "
             "covered by res-1 + seam + statechart)" % oid)
        continue
    gated_seen += 1
    st = wave_state(screen, wid)

    # a harness construction problem on a gated row is FATAL (a required proof could not be built)
    if oid in problems_by_oid:
        if st == "closed":
            fatal("res-3 CLOSED-WAVE %s: the harness could not run/construct the E2E — %s"
                  % (oid, problems_by_oid[oid]))
        else:
            emit("PENDING: %s harness problem but wave not started — surfaced, not FATAL (%s)"
                 % (oid, problems_by_oid[oid]))
        continue

    rec = obs_rows.get((screen, wid))
    if rec is None:
        if st == "closed":
            fail("res-3 CLOSED-WAVE %s: no executed E2E (no observation) — a res-3 data-effect row "
                 "MUST have an E2E; absent is unresolved, never a silent pass (NEW-2)" % oid)
        else:
            emit("PENDING: %s has no E2E but its wave has not started — surfaced, not FAIL" % oid)
        continue

    dep = (rec.get("mutationProofs") or {}).get("dependence")
    plc = (rec.get("mutationProofs") or {}).get("placement")
    e2e_pass = rec.get("e2ePass") is True

    # §6.6 RECORD line (regenerated; never read back as evidence — NEW-2)
    oiid = rec.get("oiid")
    emit("RESULTS-ROW %s: e2eRef=%s e2ePass=%s mutationProofs={dependence:%s, placement:%s}%s lastRun=%s"
         % (oid, rec.get("e2eRef"), e2e_pass, dep, plc,
            (" oiid=%s" % json.dumps(oiid)) if oiid else "", rec.get("lastRun")))

    if st != "closed":
        emit("PENDING: %s res-3 not-required (wave not started) — surfaced, not FAIL" % oid)
        continue

    # closed wave: every res-3 obligation is REQUIRED
    if not e2e_pass:
        detail = ""
        if oiid and oiid.get("collapsed"):
            detail = (" — instance collapse: driving an instance affected another row "
                      "(perInstance=%s)" % oiid.get("perInstance"))
        fail("res-3 CLOSED-WAVE %s: the executed E2E did not pass (e2ePass=false)%s" % (oid, detail))
    if dep != "RED":
        fail("res-3 CLOSED-WAVE %s: dependence proof (a) did NOT go RED (got %r) — stubbing the "
             "res-1 handler left the E2E green => the E2E does not depend on the handler => vacuous"
             % (oid, dep))

    if kind == "persisted":
        if plc == "RED":
            pass
        elif plc == "GREEN":
            fail("res-3 CLOSED-WAVE %s: placement proof (b) did NOT go RED (GREEN) — redirecting the "
                 "write left the E2E green => vacuous placement assertion" % oid)
        elif plc == "UNPROVABLE":
            granted = signoffs.get((screen, wid), False)
            if granted is False:
                fail("res-3 CLOSED-WAVE %s: placement UNPROVABLE with NO exceptions.json sign-off "
                     "keyed (%s, %s) — fail-closed (%s)"
                     % (oid, screen, wid, rec.get("placementDetail", "")))
            elif granted != DESIGN_DIGEST:
                fail("res-3 CLOSED-WAVE %s: placement UNPROVABLE and the sign-off is STALE — it was "
                     "granted against design-digest %r but the current design-digest is %r "
                     "(self-voiding: the design changed since sign-off)" % (oid, granted, DESIGN_DIGEST))
            else:
                emit("row %s: placement UNPROVABLE but a VALID sign-off (design-digest matches) covers "
                     "it — PASS for this row" % oid)
        elif plc == "NA-EPHEMERAL":
            fail("res-3 CLOSED-WAVE %s: a persisted row (has writes) reported NA-EPHEMERAL — a "
                 "persisted element can never claim it (harness/manifest inconsistency)" % oid)
        else:
            fatal("res-3 CLOSED-WAVE %s: unrecognized placement state %r (harness inconsistency)"
                  % (oid, plc))
    else:  # ephemeral
        if plc == "NA-EPHEMERAL":
            pass
        elif plc == "RED":
            emit("row %s: ephemeral row reported placement RED (a persisted-style redirect landed) — "
                 "informational; the ephemeral obligation is proof (a), already checked" % oid)
        else:
            fail("res-3 CLOSED-WAVE %s: ephemeral row (ephemeral:true + empty writes) expected "
                 "NA-EPHEMERAL placement, got %r (harness/manifest inconsistency)" % (oid, plc))

# ---- H13: an ORPHAN harness problem (an e2e spec pointing at an oid with no manifest row) is only
# looked up inside the manifest loop, so its oid — by definition NOT a manifest row — would be
# silently dropped. A dead/typo'd e2e spec must produce a signal (fail-closed) ----
for oid, reason in problems_by_oid.items():
    if oid not in manifest_oids:
        fatal("orphan e2e observation: '%s' has an executed-E2E problem but NO wiring-manifest row "
              "(a dead/renamed/typo'd e2e spec) — fail-closed (%s)" % (oid, reason))

if gated_seen == 0:
    fatal("non-vacuity floor: the manifest has %d row(s) but NONE is a res-3 data-effect row — a "
          "res-3 gate with nothing to prove cannot pass (fail-closed)" % len(manifest))

verdict()
PYEOF
