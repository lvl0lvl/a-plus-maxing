#!/usr/bin/env bash
# toolkit/scripts/wiring-gate.sh — the §6.3 wiring coverage gate, STATIC resolutions + waves.
#
# Joins every wiring-manifest row against a built app and decides, under WAVE SEMANTICS
# (§6.3 / T-10), whether the designed interaction was actually BUILT (res-1) and SERVED
# (res-2). res-3 (executed E2E + mutation proofs) is the NEXT increment and is OUT of scope
# here — this gate does the STATIC half only.
#
# HARD DEPENDENCY [T-3d / BH-F1]: it FIRST runs scripts/pen-integrity.sh (the §6.2 gate) on
# the export dir and REFUSES to run its own checks (FATAL, exit 2) if integrity FAILs or
# FATALs — a downstream gate must not run on exports it cannot trust. A §6.2 exit 0 that
# carries the PEN-CHANGED marker (a PASS-WITH-PEN-CHANGED: the committed exports are intact,
# only the .pen moved) is SAFE to proceed on, but this gate RE-EMITS the PEN-CHANGED marker
# in its OWN output so wave-close consumers see the wave-close block through this gate too
# (per the frozen §6.2 wave-close interface contract).
#
# WAVE SEMANTICS [T-10] (read from wiring-results.json, NEVER the manifest [N-1]):
#   Row's wave NOT-STARTED (no results row / no wave / an OPEN wave) ->
#     res-2 reports PENDING (not FAIL); res-1 runs and is reported informationally as
#     STATIC-PASS / STATIC-FAIL — a static failure on a not-started row is SURFACED, not fatal.
#   Row's wave CLOSED ->
#     res-1 AND res-2 are REQUIRED; anything unresolved -> FAIL by (screen, wireId).
#   Scope note [N-2]: genuine route MISMATCH detection (wired to the wrong served route) binds
#     only at wave CLOSE; during an open wave the gate cannot distinguish "not built yet" from
#     "wired elsewhere" (res-1 resolves the handler SYMBOL, not its call target). This gate
#     claims only what it mechanically delivers.
#
# THE RESOLUTIONS (static half):
#   res-1  the rendered element carries data-oid="<bare-screen>/<wireId>" (the FULL (screen,
#          wireId) join key crosses the seam [NEW-4]; the `screen/` role prefix is dropped only
#          in the attribute spelling, per the §6.3 shell example `data-oid=_shell/<wireId>`),
#          AND its data-handler resolves to a real, NON-EMPTY symbol in the app's JS. A
#          non-empty no-op passes by design (non-vacuity is res-3's job [T-22]); a green here is
#          reported STATIC-PASS, never "wired" [QA S1]. REJECTED: element absent, no
#          data-handler, a link whose only action is href="#", an undefined symbol, an empty
#          body (function(){} / ()=>{}).
#   res-2  every declared endpoint entry joins a route the app actually SERVES (routes.json;
#          method + path, ':param' segments are wildcards), AND every reads/writes entity.field
#          exists in the IMPLEMENTED data model (schema.json — NEVER §8's derived draft [T-18]).
#          endpoint:"none" skips only the ENDPOINT join; a none-endpoint row's reads/writes are
#          STILL schema-checked (endpoint coverage was pen-lint's; schema existence is res-2's).
#
# NON-VACUITY FLOOR [T-1] (floor scoping, review F2 ruling): the per-screen index.md expected-
#   count floor is §6.1's (design-time); THIS gate's own floors are:
#   zero-row manifest -> FATAL (a zero-row universe cannot pass).
#   manifest has rows but the app declares ZERO data-oid elements -> FAIL (the "built nothing"
#   case) — fires regardless of wave state, so it is not laundered by all-open waves.
#   §6.3 hard-depends on §6.2 ONLY (integrity is the precondition for reading exports; §6.1 is a
#   sibling design-time check whose sequencing is the pipeline's).
#
# BIJECTION DIRECTION: this gate checks manifest -> app (every DESIGNED row is built + served).
#   The reverse — a data-oid in the app with NO manifest row ("built-not-designed") — is the
#   §6.4 seam gate's job and is OUT of scope here.
#
# EXIT CONTRACT (0 PASS / 1 FAIL / 2 FATAL, fail-closed per F-008) — the §6.3 output contract is
# FROZEN (spec §6.3, review F3): RESULT is one of PASS / FAIL / FATAL / PASS-WITH-PEN-CHANGED.
#   2 FATAL  — the §6.2 hard dependency FAILed/FATALed (own checks NOT run); a zero-row
#              manifest; an unparseable manifest / results / routes / schema; a wiring-results
#              inconsistency (duplicate (screen,wireId) rows; a non-list `rows`; a row referencing
#              a wave absent from the waves map; a wave state ∉ open|closed); no python3.
#   1 FAIL   — one or more CLOSED-WAVE resolutions unresolved, or the zero-data-oid floor.
#   0 PASS   — every closed-wave row resolves res-1 + res-2; not-started rows PENDING/informational.
#              A propagated PEN-CHANGED keeps exit 0 but marks RESULT PASS-WITH-PEN-CHANGED.
#   VERDICT PRECEDENCE [review BH6 ruling — the shared three-gate toolkit convention]: a FAIL
#   (violation) exits 1 BEFORE a co-occurring FATAL exits 2, so a real violation is never masked
#   (mirrors lib/audit-helpers.sh). Structural FATALs (dup/non-list results, inconsistent waves)
#   are therefore detected UP FRONT and verdict early, before any per-row violation is counted, so
#   an exit-2 case is never downgraded to exit 1 by a co-occurring closed-wave FAIL.
#   AUDIT_ALLOW_SKIP=1 is passed through to the §6.2 hard dependency (it downgrades ONLY that
#   gate's repo-residency skip, per §6.2); this gate has no skip path of its own.
#
# Usage: wiring-gate.sh <export-dir> --app <app-dir> --results <results.json> [--base <repo-root>]
#   <export-dir>  the design/interaction-model directory (wiring-manifest.json + the §6.2 set).
#   --app         the built app dir (rendered *.html + app.js + routes.json + schema.json).
#   --results     wiring-results.json (§6.6) — the wave register (format-v0, provisional T-27).
#   --base        repo root for the §6.2 gate's pinned-.pen resolution. Default $PWD.
set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-wiring-gate}"
emit() { echo "[${AUDIT_TAG}] $*"; }
fatal() { emit "FATAL: $*"; exit 2; }

DIR=""
APP=""
RESULTS=""
BASE="$PWD"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --app) shift; [ "$#" -gt 0 ] || fatal "--app needs a value"; APP="$1" ;;
    --app=*) APP="${1#*=}" ;;
    --results) shift; [ "$#" -gt 0 ] || fatal "--results needs a value"; RESULTS="$1" ;;
    --results=*) RESULTS="${1#*=}" ;;
    --base) shift; [ "$#" -gt 0 ] || fatal "--base needs a value"; BASE="$1" ;;
    --base=*) BASE="${1#*=}" ;;
    -h|--help) sed -n '2,76p' "$0"; exit 0 ;;
    --*) fatal "unknown arg: $1" ;;
    *) [ -z "$DIR" ] && DIR="$1" || fatal "unexpected extra arg: $1" ;;
  esac
  shift
done

[ -n "$DIR" ] || fatal "usage: wiring-gate.sh <export-dir> --app <app-dir> --results <results.json> [--base <repo-root>]"
[ -d "$DIR" ] || fatal "export dir not found / not a directory: $DIR"
[ -n "$APP" ] || fatal "--app <app-dir> is required"
[ -d "$APP" ] || fatal "app dir not found / not a directory: $APP"
[ -n "$RESULTS" ] || fatal "--results <results.json> is required"
[ -f "$RESULTS" ] || fatal "wiring-results.json not found: $RESULTS"
[ -f "$APP/routes.json" ] || fatal "app dir has no routes.json (the res-2 served-route referent)"
[ -f "$APP/schema.json" ] || fatal "app dir has no schema.json (the res-2 implemented-data-model referent)"
command -v python3 >/dev/null 2>&1 || fatal "python3 required to run wiring-gate"

HERE="$(cd "$(dirname "$0")" && pwd)"
INTEGRITY_SH="$HERE/pen-integrity.sh"
[ -f "$INTEGRITY_SH" ] || fatal "pen-integrity.sh not found next to this gate ($INTEGRITY_SH) — the §6.2 hard dependency is missing"

# ================= HARD DEPENDENCY — §6.2 export integrity [T-3d] =============
# Run the §6.2 gate first; refuse to run our own checks unless the exports are trustworthy.
integrity_out="$(bash "$INTEGRITY_SH" "$DIR" --base "$BASE" 2>&1)"; integrity_rc=$?
if [ "$integrity_rc" -ne 0 ]; then
  emit "note: §6.2 export-integrity hard dependency did not pass (exit ${integrity_rc}) — output below:"
  printf '%s\n' "$integrity_out" | sed 's/^/    /'
  fatal "refusing to run wiring checks on exports that failed §6.2 export-integrity (hard dependency [T-3d]) — fix integrity and re-run"
fi
emit "ok: §6.2 export-integrity hard dependency passed (exit 0)"
PEN_CHANGED=0
if printf '%s' "$integrity_out" | grep -q 'PEN-CHANGED'; then
  PEN_CHANGED=1
  emit "PEN-CHANGED: propagated from §6.2 export-integrity — the pinned .pen moved since extraction; wave-close is BLOCKED until a §6.5 re-extraction runs (re-emitted here so wave-close consumers see it through this gate)"
fi

# ================= own STATIC checks (embedded python — pen-lint idiom) =======
AUDIT_TAG="$AUDIT_TAG" WIRING_PEN_CHANGED="$PEN_CHANGED" python3 - "$DIR" "$APP" "$RESULTS" <<'PYEOF'
import glob
import json
import os
import re
import sys

TAG = os.environ.get("AUDIT_TAG", "wiring-gate")
PEN_CHANGED = os.environ.get("WIRING_PEN_CHANGED", "0") == "1"
EXPORT_DIR = sys.argv[1]
APP_DIR = sys.argv[2]
RESULTS_PATH = sys.argv[3]

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
        emit("RESULT: FAIL (%d unresolved / floor violation(s))" % violations)
        sys.exit(1)
    if fatals > 0:
        emit("RESULT: FATAL (%d check(s) could not run — fail-closed)" % fatals)
        sys.exit(2)
    if PEN_CHANGED:
        emit("RESULT: PASS-WITH-PEN-CHANGED (wiring resolutions clean; wave-close BLOCKED pending "
             "a §6.5 re-extraction — propagated from §6.2)")
        sys.exit(0)
    emit("RESULT: PASS (every closed-wave row resolves res-1 + res-2)")
    sys.exit(0)


def load_json(path, what):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001 — any parse/IO error is FATAL for a required input
        fatal("cannot parse %s: %s" % (what, e))
        return None


# ---- manifest + zero-row floor -----------------------------------------------
manifest = load_json(os.path.join(EXPORT_DIR, "wiring-manifest.json"), "wiring-manifest.json")
if manifest is None:
    verdict()
if not isinstance(manifest, list):
    fatal("wiring-manifest.json must be a JSON array of rows")
    verdict()
if len(manifest) == 0:
    fatal("non-vacuity floor: wiring-manifest has zero interactive-element rows — a zero-row "
          "universe cannot pass (§6.3/T-1; fail-closed)")
    verdict()

# ---- wiring-results.json: the wave register (§6.6, format-v0) -----------------
results = load_json(RESULTS_PATH, "wiring-results.json")
if results is None:
    verdict()
if not isinstance(results, dict):
    fatal("wiring-results.json must be a JSON object (format-v0: waves + rows)")
    verdict()
waves = results.get("waves")
if not isinstance(waves, dict):
    fatal("wiring-results.json 'waves' must be an object mapping wave -> \"open\"|\"closed\"")
    verdict()
# BH4: `rows`, if present, MUST be a list. A null / non-list `rows` would silently become empty,
# making EVERY row not-started -> PASS despite closed waves (fail-open in a fail-closed gate;
# parity with the waves-dict guard above).
raw_rows = results.get("rows", [])
if not isinstance(raw_rows, list):
    fatal("wiring-results.json 'rows' must be a JSON array (got %s) — a non-list rows would "
          "silently mark every row not-started (fail-open)" % type(raw_rows).__name__)
    verdict()

# BH2: a duplicate (screen, wireId) results row is FATAL. Last-write-wins would let a later
# open-wave row launder an earlier closed-wave row's FAIL down to PENDING (exit 0) — fail-open.
wave_of = {}
for rr in raw_rows:
    if not isinstance(rr, dict) or "screen" not in rr or "wireId" not in rr:
        continue
    key = (rr["screen"], rr["wireId"])
    if key in wave_of:
        fatal("wiring-results has a duplicate row for %s/%s — a duplicate can launder a closed-"
              "wave FAIL to PENDING (fail-open); dedupe the results file" % (key[0], key[1]))
        continue
    wave_of[key] = rr.get("wave")

# Validate wave DECLARATIONS eagerly, so an inconsistent results file FATALs cleanly UP FRONT —
# before any per-row violation is counted, so the shared violations-first verdict can never
# downgrade an exit-2 case to exit 1 (QA2). Two distinct FATALs: a bad-state wave, and a row
# referencing an undeclared wave. A missing `wave` key is legitimately not-started (no FATAL).
for wname, st in waves.items():
    if st not in ("open", "closed"):
        fatal("wiring-results waves['%s'] = %r, expected \"open\"|\"closed\" (fail-closed)" % (wname, st))
for (screen, wid), w in wave_of.items():
    if w is not None and str(w) not in waves:
        fatal("wiring-results row %s/%s references wave '%s' absent from the waves map — "
              "inconsistent results file (fail-closed)" % (screen, wid, w))
if fatals:
    verdict()


def wave_state(screen, wid):
    """'closed' or 'not-started'. Wave declarations were validated eagerly above, so a referenced
    wave is guaranteed present with an open|closed state here."""
    w = wave_of.get((screen, wid))
    if w is None:
        return "not-started"
    return "closed" if waves.get(str(w)) == "closed" else "not-started"


# ---- res-2 referents: served routes + implemented schema ---------------------
routes = load_json(os.path.join(APP_DIR, "routes.json"), "app/routes.json")
schema = load_json(os.path.join(APP_DIR, "schema.json"), "app/schema.json")
if fatals:
    verdict()
if not isinstance(routes, list):
    fatal("app/routes.json must be a JSON array of 'METHOD /path' served routes")
if not isinstance(schema, dict):
    fatal("app/schema.json must be a JSON object of entity -> [field, ...]")
if fatals:
    verdict()

ROUTE_RE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/\S*)$")
served = []
for r in routes:
    m = ROUTE_RE.match(r) if isinstance(r, str) else None
    if not m:
        fatal("app/routes.json entry %r is not 'METHOD /path'" % (r,))
        continue
    served.append((m.group(1), m.group(2)))
if fatals:
    verdict()


def _segs(path):
    return [s for s in path.split("/") if s != ""]


def route_served(method, path):
    ps = _segs(path)
    for rm, rp in served:
        if rm != method:
            continue
        rs = _segs(rp)
        if len(rs) != len(ps):
            continue
        if all(a.startswith(":") or b.startswith(":") or a == b for a, b in zip(rs, ps)):
            return True
    return False


# ---- scan the app HTML: data-oid -> {handler, href} --------------------------
TAG_RE = re.compile(r'<[a-zA-Z][^>]*\bdata-oid="[^"]+"[^>]*>')
OID_RE = re.compile(r'data-oid="([^"]+)"')
HANDLER_RE = re.compile(r'data-handler="([^"]*)"')
HREF_RE = re.compile(r'href="([^"]*)"')
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
oid_elems = {}
for hp in sorted(glob.glob(os.path.join(APP_DIR, "*.html"))):
    try:
        with open(hp, errors="replace") as f:
            text = f.read()
    except Exception as e:  # noqa: BLE001
        fatal("cannot read app HTML %s: %s" % (os.path.basename(hp), e))
        continue
    # BH1: strip <!-- ... --> regions FIRST — a commented-out element is not rendered, so it must
    # not satisfy res-1 (the README's honest-limit note covers quotes/> in attrs, never comments).
    original_len = len(text)
    # Attribute-shaped count (9hv fix-2): a PROSE mention of data-oid inside a comment
    # (the fixture dashboard.html's own header says "carries no data-oid") must not read
    # as swallowed markup — count the attribute form OID_RE matches, not the bare substring.
    pre_oid_count = len(OID_RE.findall(text))
    text = COMMENT_RE.sub("", text)
    # N-2: an UNBALANCED `<!--` paired with any later `-->` swallows real elements between them ->
    # false "element never built" FAILs downstream. Stays fail-closed (the elements read absent),
    # but warn so the operator isn't chasing ghosts from a malformed comment. Tightened (9hv):
    # only when the strip CONSUMED data-oid-bearing markup — that is the misattribution hazard;
    # a well-formed comment-dominant file (big license header, no swallowed elements) is benign
    # at any strip percentage and previously false-noted.
    if (original_len > 0 and len(text) < original_len * 0.5
            and len(OID_RE.findall(text)) < pre_oid_count):
        emit("note: HTML comment-strip removed >50%% of %s including data-oid markup — a "
             "malformed/unbalanced <!-- --> (or a large intentional comment-out of elements) — "
             "res-1 'element never built' diagnostics from this file may be misattributed"
             % os.path.basename(hp))
    for tag in TAG_RE.findall(text):
        mo = OID_RE.search(tag)
        if not mo:
            continue
        oid = mo.group(1)
        if oid in oid_elems:
            # BH7: an app-side DUPLICATE data-oid (first-wins here) is the §6.4 seam gate's
            # concern (built-not-designed / bijection), out of scope for this manifest->app gate.
            continue
        h = HANDLER_RE.search(tag)
        href = HREF_RE.search(tag)
        oid_elems[oid] = {"handler": h.group(1) if h else None,
                          "href": href.group(1) if href else None}
if fatals:
    verdict()

# ---- app.js symbol resolver --------------------------------------------------
def _strip_js_comments(s):
    """Remove // and /* */ comments while PRESERVING string/template literals — a '//' inside a
    real \"https://...\" literal must NOT be eaten [N-1]. Comments are stripped ONCE here, before
    the definition scan, so a COMMENTED-OUT later definition of a handler cannot shadow a live
    earlier one (the resolver takes the last def by position; a naive raw scan would let a comment
    win). Mirrors the HTML COMMENT_RE strip. (Regex literals are not tracked — the fixture-format
    handlers use none; a real-project adapter would use a JS parser.)"""
    out = []
    i, n = 0, len(s)
    state = None  # None | 'line' | 'block' | a quote char ' " `
    while i < n:
        c = s[i]
        nxt = s[i + 1] if i + 1 < n else ""
        if state is None:
            if c == "/" and nxt == "/":
                state = "line"; i += 2; continue
            if c == "/" and nxt == "*":
                state = "block"; i += 2; continue
            if c in ("'", '"', "`"):
                state = c
            out.append(c); i += 1; continue
        if state == "line":
            if c == "\n":
                state = None; out.append(c)
            i += 1; continue
        if state == "block":
            if c == "*" and nxt == "/":
                state = None; i += 2; continue
            i += 1; continue
        # inside a string / template literal
        if c == "\\":
            out.append(c)
            if i + 1 < n:
                out.append(s[i + 1])
            i += 2; continue
        if c == state:
            state = None
        out.append(c); i += 1; continue
    return "".join(out)


js_text = ""
js_path = os.path.join(APP_DIR, "app.js")
if os.path.isfile(js_path):
    with open(js_path, errors="replace") as f:
        js_text = _strip_js_comments(f.read())


def _brace_body(s):
    """s starts with '{'; return the text between it and its matching '}'."""
    depth = 0
    for i, ch in enumerate(s):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[1:i]
    return s[1:]


def symbol_nonempty(sym):
    """(defined, nonempty) for a handler symbol. Resolves the LAST matching definition by file
    position — JS shadows an earlier definition with a later one, so appending a dead
    `function f(){}` after the real one must FAIL [BH3]. `js_text` was comment-stripped at load, so
    a comment-only body {/* todo */} is already {} here -> EMPTY -> res-1 FAIL (spec §6.3 ruling:
    T-22's non-empty-no-op covers code that EXECUTES, not comments); an arrow EXPRESSION body is
    non-empty by construction (a valid arrow carries an expression)."""
    if not sym:
        return (False, False)
    esc = re.escape(sym)
    patterns = (r"\bfunction\s+" + esc + r"\s*\([^)]*\)\s*",
                r"\b" + esc + r"\s*=\s*(?:async\s+)?function\s*\*?\s*\([^)]*\)\s*",
                r"\b" + esc + r"\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*",
                r"\b" + esc + r"\s*=\s*(?:async\s*)?[A-Za-z_$][\w$]*\s*=>\s*")
    best = None  # (start_pos, nonempty) for the LATEST definition seen
    for pat in patterns:
        for m in re.finditer(pat, js_text):
            rest = js_text[m.end():].lstrip()
            nonempty = (_brace_body(rest).strip() != "") if rest.startswith("{") else (rest.strip() != "")
            if best is None or m.start() > best[0]:
                best = (m.start(), nonempty)
    if best is None:
        return (False, False)
    return (True, best[1])


def res1(oid):
    """(ok, kind, detail); kind in {None,'absent','handler'}."""
    if oid not in oid_elems:
        return (False, "absent", None)
    el = oid_elems[oid]
    h = el["handler"]
    if not h:
        href = el["href"]
        if href is not None and href.strip() in ("#", ""):
            return (False, "handler", "the element's only action is href=\"#\" — not a real handler")
        return (False, "handler", "the element carries no data-handler symbol")
    defined, nonempty = symbol_nonempty(h)
    if not defined:
        return (False, "handler", "handler symbol '%s' is not defined in app.js" % h)
    if not nonempty:
        return (False, "handler", "handler '%s' resolves to an empty body (dead handler)" % h)
    return (True, None, None)


def res2(row):
    """List of res-2 failure detail strings ([] = resolved). endpoint 'none' skips only the
    ENDPOINT join — a none-endpoint row's reads/writes are still schema-checked."""
    out = []
    ep = row.get("endpoint", "none")
    if ep == "none":
        eps = []
    elif isinstance(ep, str):
        eps = [ep]
    elif isinstance(ep, list):
        eps = [e for e in ep if isinstance(e, str)]
    else:
        eps = []
    for e in eps:
        m = ROUTE_RE.match(e)
        if not m:
            out.append("endpoint '%s' is not 'METHOD /path'" % e)
            continue
        if not route_served(m.group(1), m.group(2)):
            out.append("endpoint '%s' is served by no route in routes.json" % e)
    # BH5: a bare-string reads/writes must NOT be iterated char-by-char (silent skip / garbage
    # message). Type-check first: a present-but-non-list value is one clean res-2 detail.
    for fname in ("reads", "writes"):
        val = row.get(fname)
        if val is None:
            continue
        if not isinstance(val, list):
            out.append("%s must be a list of entity.field, not %s" % (fname, type(val).__name__))
            continue
        for fld in val:
            if not isinstance(fld, str) or "." not in fld:
                continue  # §5 / pen-lint validates entity.field FORMAT; res-2 checks EXISTENCE only
            ent, _, f = fld.partition(".")
            if ent not in schema:
                out.append("reads/writes '%s' entity '%s' is not present in schema.json" % (fld, ent))
            elif f not in (schema.get(ent) or []):
                out.append("reads/writes '%s' field '%s' is not present in schema.json" % (fld, f))
    return out


# ---- non-vacuity floor: manifest has rows but the app built nothing ----------
if len(oid_elems) == 0:
    fail("non-vacuity floor: the app declares ZERO data-oid elements while the manifest has "
         "%d row(s) — nothing was built (§6.3/T-1)" % len(manifest))

# ---- per-row resolutions under wave semantics --------------------------------
for row in manifest:
    if not isinstance(row, dict):
        fail("manifest row is not an object: %r" % (row,))
        continue
    screen = row.get("screen")
    wid = row.get("wireId")
    bare = screen[len("screen/"):] if isinstance(screen, str) and screen.startswith("screen/") else screen
    oid = "%s/%s" % (bare, wid)
    st = wave_state(screen, wid)

    r1_ok, r1_kind, r1_detail = res1(oid)
    if st == "not-started":
        # informational only: res-1 surfaced, res-2 PENDING (§6.3 / T-10)
        emit("row %s: res1=%s res2=PENDING (wave-not-started)"
             % (oid, "STATIC-PASS" if r1_ok else "STATIC-FAIL"))
        if not r1_ok:
            emit("  note: res-1 STATIC-FAIL — %s" % (r1_detail or "element absent"))
        continue

    # st == "closed": res-1 AND res-2 REQUIRED (§6.3 / T-10)
    if r1_ok:
        emit("row %s: res1=STATIC-PASS (CLOSED wave)" % oid)
    elif r1_kind == "absent":
        fail("res-1 CLOSED-WAVE %s: no element in the app carries data-oid=\"%s\" (element never "
             "built)" % (oid, oid))
    else:
        fail("res-1 CLOSED-WAVE %s: %s" % (oid, r1_detail))
    for d in res2(row):
        fail("res-2 CLOSED-WAVE %s: %s" % (oid, d))

verdict()
PYEOF
