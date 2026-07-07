#!/usr/bin/env bash
# toolkit/scripts/pen-lint.sh — design-time lint over the Interaction-Model EXPORTS.
#
# Implements the design-process-overhaul spec §6.1 checks 1-6 and 8 (check 7 is
# bootstrap-only and OUT of scope here), the §6/T-1 non-vacuity floor, and the §5
# value-level validations that operate ON EXPORTS. It reads ONLY the committed export
# set (never the encrypted .pen) — the exports are the system of record (§3 rule 1).
#
# WHAT IT CHECKS (source of the "7 checks + floor + 7 value checks" claim — count
# them in the embedded python below; each carries a `# ck<N>` / `# §5` marker):
#   ck1  naming grammar (§4.1 table): interactive element name = <role>/<what-kebab>.
#   ck2  no unnamed interactive-role nodes; no default (f\d+) names.
#   ck3  name<->metadata coherence: the name's <what> matches the wireId (instance rule
#        below), i.e. btn/submit-report carries wireId submit-report.
#   ck4  (screen,wireId) uniqueness; every statechart transition's fromWireId/target
#        resolves; no re-mint of a retired (screen,wireId).
#   ck5  instance identity (§4.1/T-8): an instance wireId is <instance-name>.<def-wireId>
#        with both parts non-empty valid kebab; a comp/ DEFINITION node never appears as
#        a wired screen row (definitions are templates; only minted instances are wired).
#   ck6  coverage predicate (§4.1/T-16): every interactive element satisfies
#        [ reads|writes non-empty  OR  destination != self  OR  ephemeral+localEffect ]
#        AND [ >=1 statechart transition  OR  ephemeral:true ].
#   ck8  status:"deferred" requires a deferredRef that RESOLVES (§6.1/T-2): the file
#        exists, the symbol is present in it, and the bead is real and OPEN (`bd show`).
#   floor  §6/T-1 non-vacuity: a zero-row manifest (or an index that declares no screens
#          while the manifest is non-empty) is FATAL; a screen whose manifest rows fall
#          short of its index.md "Expected interactive elements" count FAILs.
#   §5 value checks (on exports): action in enum OR x-<custom> that is BOTH in config.json
#      xActions AND matched by a transition whose event == the action (§4.1 strict match);
#      endpoint "none" or each "METHOD /path" entry well-formed; reads/writes are lists of
#      "entity.field"; non-empty writes with endpoint:"none" always FAIL; ephemeral<->
#      localEffect pairing; inherently-persisted action (submit/edit/add/remove/reorder/
#      upload) with ephemeral:true FAIL; shell:true shellStates reference real screens AND
#      shellStates present without shell:true FAIL.
#
# OUT OF SCOPE (Phase 1a boundary, stated so nobody reads it as done): §6.1 ck7
#   (bootstrap canvas<->machine consistency); the §6.2 export-integrity / pen-change
#   gate and digest VERIFICATION (pen-digest.sh computes the digest; §6.2 is Phase 2);
#   §6.5 drift. The "ref-delta references a def-wireId absent from the definition" sub-rule
#   needs the comp-definition registry the RESOLVED exports do not carry — it is Phase-1b
#   extractor territory.
#
# ck8 bead resolution shells out to `bd show <id> --json`. Real bd 0.49.0: a FOUND id emits
#   a JSON array [{... "status":"open|closed" ...}] (exit 0); a MISSING id emits the object
#   {"error": ...} on stdout (exit 1). pen-lint reads status from the JSON, never the exit
#   code — any non-array / unparseable / EMPTY stdout counts as unresolved -> FAIL (so the
#   handler is robust to the empty-stdout error path too). In the REAL run this is the real
#   `bd`; the F-007 suite stubs `bd` on PATH (open/closed/missing/empty-stdout per fixture)
#   so it is hermetic. PEN_LINT_BD overrides the resolver command (default `bd`) — used only
#   to exercise the bd-absent fail-closed path.
#
# Exit contract (0 PASS / 1 FAIL / 2 FATAL), fail-closed per F-008:
#   2 FATAL  — cannot run (missing/unparseable export, no python3) OR the non-vacuity
#              floor's zero universe OR a fail-closed SKIP (bd absent, no AUDIT_ALLOW_SKIP).
#   1 FAIL   — one or more property violations.
#   0 PASS   — clean.
# A FAIL takes precedence over a fail-closed SKIP (mirrors lib/audit-helpers.sh verdict).
#
# Usage: pen-lint.sh <export-dir> [--base <repo-root>]
#   <export-dir>  the design/interaction-model directory holding the exports.
#   --base        root for resolving deferredRef file paths (ck8). Default: $PWD.
set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-pen-lint}"

emit() { echo "[${AUDIT_TAG}] $*"; }

DIR=""
BASE="$PWD"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --base) shift; [ "$#" -gt 0 ] || { emit "FATAL: --base needs a value"; exit 2; }; BASE="$1" ;;
    --base=*) BASE="${1#*=}" ;;
    -h|--help) sed -n '2,61p' "$0"; exit 0 ;;
    --*) emit "FATAL: unknown arg: $1"; exit 2 ;;
    *) [ -z "$DIR" ] && DIR="$1" || { emit "FATAL: unexpected extra arg: $1"; exit 2; } ;;
  esac
  shift
done

[ -n "$DIR" ] || { emit "FATAL: usage: pen-lint.sh <export-dir> [--base <repo-root>]"; exit 2; }
[ -d "$DIR" ] || { emit "FATAL: export dir not found / not a directory: $DIR"; exit 2; }

# Required export files. exceptions.json is part of the §5 digest set but is not consumed
# by any §6.1 check, so pen-lint does not require it here — its presence and digest coverage
# are §6.2's concern (Phase 2). A missing required export is FATAL: the lint cannot run.
for f in index.md wiring-manifest.json retired-wireids.txt config.json; do
  [ -f "$DIR/$f" ] || { emit "FATAL: missing required export: $f (in $DIR)"; exit 2; }
done
if ! ls "$DIR"/machine.*.json >/dev/null 2>&1; then
  emit "FATAL: no machine.*.json statechart in $DIR"; exit 2
fi

command -v python3 >/dev/null 2>&1 || { emit "FATAL: python3 required to run pen-lint"; exit 2; }

AUDIT_TAG="$AUDIT_TAG" python3 - "$DIR" "$BASE" <<'PYEOF'
import glob
import json
import os
import re
import shutil
import subprocess
import sys

TAG = os.environ.get("AUDIT_TAG", "pen-lint")
ALLOW_SKIP = os.environ.get("AUDIT_ALLOW_SKIP", "0") == "1"
BD_CMD = os.environ.get("PEN_LINT_BD", "bd")
EXPORT_DIR = sys.argv[1]
BASE = sys.argv[2]

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


def skipped(m):
    global fatals
    if ALLOW_SKIP:
        emit("SKIPPED: %s (allowed via AUDIT_ALLOW_SKIP=1; not gating)" % m)
    else:
        emit("SKIPPED: %s (fail-closed: a check that cannot run does not pass — F-008)" % m)
        fatals += 1


def verdict():
    # FAIL takes precedence over a fail-closed SKIP (mirrors lib/audit-helpers.sh).
    if violations > 0:
        emit("RESULT: FAIL (%d violation(s))" % violations)
        sys.exit(1)
    if fatals > 0:
        emit("RESULT: FATAL (%d check(s) could not run / vacuous — fail-closed)" % fatals)
        sys.exit(2)
    emit("RESULT: PASS")
    sys.exit(0)


def load_json(name):
    try:
        with open(os.path.join(EXPORT_DIR, name)) as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001 — any parse/IO error is FATAL for this export
        fatal("cannot parse %s: %s" % (name, e))
        return None


manifest = load_json("wiring-manifest.json")
config = load_json("config.json")
machines = []
for mp in sorted(glob.glob(os.path.join(EXPORT_DIR, "machine.*.json"))):
    try:
        with open(mp) as f:
            machines.append(json.load(f))
    except Exception as e:  # noqa: BLE001
        fatal("cannot parse %s: %s" % (os.path.basename(mp), e))

if fatals:  # a required export did not parse — cannot run the checks
    verdict()

if not isinstance(manifest, list):
    fatal("wiring-manifest.json must be a JSON array of rows")
    verdict()
x_actions = set(config.get("xActions", []) if isinstance(config, dict) else [])

# --- index.md expected per-screen interactive-element counts (§5/T-1 floor input) ---
# A `##` heading that MENTIONS a screen but is not a clean `## screen/<name>` header must
# not silently mis-attribute counts (T-01/T-02 floor fail-open) — it is FATAL, and it
# resets the current screen so a following "Expected:" line cannot bind to a stale header.
expected = {}
cur = None
with open(os.path.join(EXPORT_DIR, "index.md")) as f:
    for line in f:
        strict = re.match(r"^##\s+(screen/\S+)\s*$", line)
        if strict:
            cur = strict.group(1)
            continue
        # Anchor to h2 ONLY (## not followed by #): a malformed h2 screen header must FATAL,
        # but a legitimate h3+ sub-heading like `### screen/dashboard notes` must not (N-1).
        if re.match(r"^##(?!#)", line) and "screen/" in line:
            fatal("index.md malformed screen header (counts cannot be attributed): %r"
                  % line.rstrip("\n"))
            cur = None
            continue
        m = re.match(r"^\s*Expected interactive elements:\s*(\d+)\s*$", line)
        if m and cur is not None:
            expected[cur] = int(m.group(1))

# A malformed index header is a cannot-run condition: counts are unattributable, so the
# floor would mis-report against a partial expected-count map. FATAL now, before any per-row
# or floor check turns that partial map into a misleading FAIL (T-01/T-02).
if fatals:
    verdict()

# --- retired (screen, wireId) pairs ---
retired = set()
with open(os.path.join(EXPORT_DIR, "retired-wireids.txt")) as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        if len(parts) >= 2:
            retired.add((parts[0], parts[1]))

# --- statechart: collect state names and transitions ---
STATE_NAMES = set()
TRANSITIONS = []  # (fromWireId, event, target)


def collect_states(node):
    if isinstance(node, dict):
        st = node.get("states")
        if isinstance(st, dict):
            for k, v in st.items():
                STATE_NAMES.add(k)
                collect_states(v)


def collect_transitions(node):
    if isinstance(node, dict):
        on = node.get("on")
        if isinstance(on, dict):
            for event, trs in on.items():
                if isinstance(trs, dict):
                    trs = [trs]
                if isinstance(trs, list):
                    for t in trs:
                        if isinstance(t, dict):
                            TRANSITIONS.append((t.get("fromWireId"), event, t.get("target")))
        st = node.get("states")
        if isinstance(st, dict):
            for v in st.values():
                collect_transitions(v)


for mc in machines:
    collect_states(mc)
    collect_transitions(mc)

TRANSITION_FROM = {t[0] for t in TRANSITIONS if t[0] is not None}
MANIFEST_WIREIDS = {r.get("wireId") for r in manifest if isinstance(r, dict)}
SCREENS = {r.get("screen") for r in manifest if isinstance(r, dict)} | set(expected.keys())

# --- grammar constants ---
ROLES = {"btn", "input", "select", "chip", "toggle", "link", "nav", "tab",
         "row-action", "modal", "search", "filter", "sort", "upload", "drag"}
# `input` = transient form-field entry (ephemeral-compatible; the submit persists) —
# spec §4.1 amendment 2026-07-02, Phase-1b feedback. `edit` = persisted-record mutation
# and stays in PERSISTED_ACTIONS (NEW-7).
ENUM_ACTIONS = {"submit", "edit", "input", "select", "toggle", "navigate", "open", "close",
                "add", "remove", "reorder", "search", "filter", "sort", "upload", "drag"}
PERSISTED_ACTIONS = {"submit", "edit", "add", "remove", "reorder", "upload"}
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEFAULT_NAME = re.compile(r"^f[0-9]+$")
METHOD_RE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS) /\S*$")
FIELD_RE = re.compile(r"^[a-z][A-Za-z0-9_]*\.[a-z][A-Za-z0-9_]*$")

# ======================= §6/T-1 non-vacuity floor =======================
total = len(manifest)
rows_per_screen = {}
for r in manifest:
    if isinstance(r, dict):
        rows_per_screen[r.get("screen")] = rows_per_screen.get(r.get("screen"), 0) + 1

if total == 0:
    fatal("non-vacuity floor: wiring-manifest has zero interactive-element rows — "
          "a zero-row universe cannot pass (§6/T-1; fail-closed)")
elif not expected:
    fatal("non-vacuity floor: index.md declares no screen counts while the manifest is "
          "non-empty — the independent expected count is absent (§6/T-1; fail-closed)")
else:
    for scr in sorted(expected):
        act = rows_per_screen.get(scr, 0)
        if act < expected[scr]:
            fail("non-vacuity floor: screen %s has %d manifest row(s) < expected %d (§6/T-1)"
                 % (scr, act, expected[scr]))
    # manifest subset of index: a manifest screen with NO index expected-count would escape
    # the per-screen floor entirely (fail-open) — FAIL naming it (T-01/T-02).
    for scr in sorted(s for s in rows_per_screen if s is not None):
        if scr not in expected:
            fail("non-vacuity floor: manifest screen %s has no index.md expected count — an "
                 "undeclared screen escapes the floor (§6/T-1)" % scr)

# a zero universe is FATAL and there is nothing per-row to check
if total == 0:
    verdict()

# ======================= per-row checks =======================
seen_keys = set()
for r in manifest:
    if not isinstance(r, dict):
        fail("manifest row is not an object: %r" % (r,))
        continue
    name = r.get("name")
    screen = r.get("screen")
    wid = r.get("wireId")
    where = "%s/%s" % (screen, wid)

    # ---- ck4: (screen, wireId) uniqueness + retired re-mint ----
    key = (screen, wid)
    if key in seen_keys:
        fail("ck4: duplicate (screen, wireId) = %s" % (where,))
    seen_keys.add(key)
    if key in retired:
        fail("ck4: re-mint of retired (screen, wireId) = %s — remove its retired-wireids.txt "
             "entry in the same change or pick a new wireId (§4.1/T-30)" % (where,))

    # ---- ck2: name present / not a default ----
    if not name:
        fail("ck2: interactive element %s has no name (unnamed interactive-role node)" % (where,))
        continue
    if any(DEFAULT_NAME.match(seg) for seg in name.split("/")):
        fail("ck2: default (f<n>) name '%s' at %s — name every node (§4.1)" % (name, where))
        continue

    # ---- ck5: comp DEFINITION must not be a wired screen row ----
    if name.startswith("comp/"):
        fail("ck5: comp-definition node '%s' at %s carries a screen-level (screen,wireId) — "
             "definitions are templates; only minted instances are wired (§4.1/T-8)" % (name, where))
        continue

    # ---- ck1: naming grammar for interactive elements ----
    parts = name.split("/")
    if len(parts) != 2 or parts[0] not in ROLES or not KEBAB.match(parts[1]):
        fail("ck1: name '%s' at %s is not <role>/<what-kebab> with role in the §4.1 set" % (name, where))
        # keep going: other checks still meaningful, but coherence below relies on <what>
        role_what = None
    else:
        role_what = parts[1]

    # ---- ck5 + ck3: instance identity and name<->metadata coherence ----
    is_instance = isinstance(wid, str) and "." in wid
    if is_instance:
        inst, _, defw = wid.rpartition(".")
        if inst == "" or defw == "":
            fail("ck5: instance wireId '%s' at %s is not <instance-name>.<def-wireId> with both "
                 "parts present — the instance name is load-bearing (unnamed ref instance) (§4.1/T-8)"
                 % (wid, where))
        else:
            if not KEBAB.match(inst):
                fail("ck5: instance-name '%s' in wireId '%s' at %s is not valid kebab (§4.1/T-8)"
                     % (inst, wid, where))
            if not KEBAB.match(defw):
                fail("ck5: definition-wireId '%s' in wireId '%s' at %s is not valid kebab (§4.1/T-8)"
                     % (defw, wid, where))
            if role_what is not None and role_what != defw:
                fail("ck3: name '%s' (<what>=%s) disagrees with instance def-wireId '%s' at %s (§4.1)"
                     % (name, role_what, defw, where))
    else:
        if role_what is not None and wid != role_what:
            fail("ck3: name '%s' (<what>=%s) does not match wireId '%s' at %s (§4.1)"
                 % (name, role_what, wid, where))

    # ---- normalized field views ----
    # reads/writes must be LISTS. A bare string would otherwise iterate per-character and
    # emit garbage FAILs — type-check first, ONE clean FAIL, then normalise to [] (§4.1/T-14).
    raw_reads = r.get("reads")
    raw_writes = r.get("writes")
    if raw_reads is not None and not isinstance(raw_reads, list):
        fail("§5: %s reads must be a list of entity.field, not %s (§4.1/T-14)"
             % (where, type(raw_reads).__name__))
    if raw_writes is not None and not isinstance(raw_writes, list):
        fail("§5: %s writes must be a list of entity.field, not %s (§4.1/T-14)"
             % (where, type(raw_writes).__name__))
    reads = raw_reads if isinstance(raw_reads, list) else []
    writes = raw_writes if isinstance(raw_writes, list) else []
    endpoint = r.get("endpoint", "none")
    dest = r.get("destination")
    eph = r.get("ephemeral") is True
    le = r.get("localEffect")
    action = r.get("action")
    status = r.get("status")

    # ---- §5: action enum + x-allowlist + x-strict transition match (§4.1) ----
    if action in ENUM_ACTIONS:
        pass
    elif isinstance(action, str) and action.startswith("x-"):
        if action not in x_actions:
            fail("§5: x-custom action '%s' at %s is not in config.json xActions allowlist" % (action, where))
        elif not any(f == wid and e == action for (f, e, _t) in TRANSITIONS):
            fail("§5: x-custom action '%s' at %s has no statechart transition whose event == the "
                 "action — the escape hatch still requires the §4.1 strict match" % (action, where))
    else:
        fail("§5: action '%s' at %s is off-enum and not an allowlisted x-<custom> (§4.1)" % (action, where))

    # ---- §5: endpoint format (each entry) ----
    def bad_endpoint(ep):
        return not (isinstance(ep, str) and METHOD_RE.match(ep))
    if endpoint == "none":
        pass
    elif isinstance(endpoint, str):
        if bad_endpoint(endpoint):
            fail("§5: endpoint '%s' at %s is not 'METHOD /path' nor 'none' (§4.1/T-17)" % (endpoint, where))
    elif isinstance(endpoint, list):
        if not endpoint:
            fail("§5: endpoint list at %s is empty — use 'none' or list entries (§4.1/T-17)" % (where,))
        for ep in endpoint:
            if bad_endpoint(ep):
                fail("§5: endpoint entry '%s' at %s is not 'METHOD /path' (§4.1/T-17)" % (ep, where))
    else:
        fail("§5: endpoint at %s must be a string, a list of 'METHOD /path', or 'none' (§4.1/T-17)" % (where,))

    # ---- §5: reads/writes entity.field format ----
    for fld in list(reads) + list(writes):
        if not (isinstance(fld, str) and FIELD_RE.match(fld)):
            fail("§5: '%s' at %s is not a valid entity.field (§4.1/T-14)" % (fld, where))

    # ---- §5: non-empty writes require endpoint != none ----
    if writes and endpoint == "none":
        fail("§5: %s has non-empty writes but endpoint:'none' — writes mean a PERSISTED effect; "
             "local-only effects go in localEffect (§4.1/T-12)" % (where,))

    # ---- §5: ephemeral <-> localEffect pairing ----
    if eph and not le:
        fail("§5: %s is ephemeral:true without a localEffect (required iff ephemeral) (§4.1/T-12)" % (where,))
    if le and not eph:
        fail("§5: %s declares a localEffect without ephemeral:true (§4.1/T-12)" % (where,))

    # ---- §5: action <-> ephemeral incompatibility ----
    if eph and action in PERSISTED_ACTIONS:
        fail("§5: %s action '%s' has inherently-persisted semantics and is incompatible with "
             "ephemeral:true (§4.1/NEW-7)" % (where, action))

    # ---- §5: shell / shellStates validity ----
    shell = r.get("shell") is True
    ss = r.get("shellStates")
    if ss is not None and not shell:
        fail("§5: %s declares shellStates without shell:true (§4.1/F-A)" % (where,))
    if shell and isinstance(ss, list):
        for s in ss:
            if s != "*" and s not in SCREENS:
                fail("§5: shell element %s shellStates references unknown screen '%s' (§4.1/F-A)"
                     % (where, s))

    # ---- ck6: coverage predicate (§4.1/T-16) ----
    # ck6 is NOT exempted for deferred rows: a deferral defers IMPLEMENTATION, not DESIGN
    # (§6.1 ck8 note), so a deferred element must still declare its transition or ephemeral.
    conj_a = bool(reads) or bool(writes) or (dest is not None and dest != "self") or (eph and bool(le))
    conj_b = (wid in TRANSITION_FROM) or eph
    if not (conj_a and conj_b):
        missing = []
        if not conj_a:
            missing.append("no reads/writes, no destination!=self, no ephemeral+localEffect")
        if not conj_b:
            if status == "deferred":
                missing.append("deferred element must still declare its transition or ephemeral "
                               "(deferral defers implementation, not design)")
            else:
                missing.append("no statechart transition and not ephemeral")
        fail("ck6: coverage predicate unmet at %s — %s (§4.1/T-16)" % (where, "; ".join(missing)))

# ======================= ck4: transition cross-references =======================
for frm, event, target in TRANSITIONS:
    if frm is not None and frm not in MANIFEST_WIREIDS:
        fail("ck4: transition (event=%s) fromWireId '%s' resolves to no manifest wireId "
             "(dangling transition) (§5)" % (event, frm))
    if target is not None and target not in STATE_NAMES:
        fail("ck4: transition (event=%s) target '%s' resolves to no statechart state (§5)"
             % (event, target))

# ======================= ck8: deferredRef resolution =======================
DREF_RE = re.compile(r"^\s*(?P<file>.+?):(?P<sym>[^:\s]+)\s*\+\s*(?P<bead>\S+)\s*$")


def bead_open(bead):
    """Return (True|False|None, reason). None => bd resolver unavailable."""
    if os.path.basename(BD_CMD) == BD_CMD:
        exe = shutil.which(BD_CMD)
    else:
        exe = BD_CMD if os.access(BD_CMD, os.X_OK) else None
    if not exe:
        return (None, "bd-unavailable")
    try:
        proc = subprocess.run([exe, "show", bead, "--json"],
                              capture_output=True, text=True, timeout=20)
    except Exception as e:  # noqa: BLE001
        return (False, "bd-error:%s" % e)
    try:
        data = json.loads(proc.stdout)
    except Exception:  # noqa: BLE001 — missing id yields {"error":...} or non-JSON
        return (False, "unparseable-or-error")
    if isinstance(data, list) and data and isinstance(data[0], dict) and "status" in data[0]:
        return (data[0]["status"] == "open", data[0].get("status"))
    return (False, "no-status")  # e.g. {"error": ...} for a missing id


for r in manifest:
    if not isinstance(r, dict) or r.get("status") != "deferred":
        continue
    where = "%s/%s" % (r.get("screen"), r.get("wireId"))
    dref = r.get("deferredRef")
    if not dref:
        fail("ck8: %s is status:'deferred' with no deferredRef (required iff deferred) (§4.1/T-2)" % (where,))
        continue
    m = DREF_RE.match(dref)
    if not m:
        fail("ck8: %s deferredRef '%s' is not 'file:symbol + bead-id' (§4.1)" % (where, dref))
        continue
    fpart, sym, bead = m.group("file"), m.group("sym"), m.group("bead")
    fpath = os.path.join(BASE, fpart)
    if not os.path.isfile(fpath):
        fail("ck8: %s deferredRef file '%s' does not exist (phantom referent) (§6.1/T-2)" % (where, fpart))
        continue
    try:
        with open(fpath, errors="replace") as fh:
            content = fh.read()
    except Exception as e:  # noqa: BLE001
        fail("ck8: %s deferredRef file '%s' unreadable: %s" % (where, fpart, e))
        continue
    if re.search(r"\b" + re.escape(sym) + r"\b", content) is None:
        fail("ck8: %s deferredRef symbol '%s' not present in '%s' (phantom referent) (§6.1/T-2)"
             % (where, sym, fpart))
        continue
    opened, reason = bead_open(bead)
    if opened is None:
        skipped("ck8 bead resolution for %s: resolver '%s' not found" % (bead, BD_CMD))
    elif opened is True:
        emit("ok: %s deferral resolves (file+symbol+open bead %s)" % (where, bead))
    else:
        fail("ck8: %s deferredRef bead '%s' does not resolve OPEN (status=%s) — a closed/missing "
             "bead FAILS (§6.1/T-2)" % (where, bead, reason))

verdict()
PYEOF
