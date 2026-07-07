#!/usr/bin/env bash
# tests/test-wiring-gate.sh — F-007 negative test for scripts/wiring-gate.sh (the §6.3 gate).
#
# F-007 obligation: a gate that cannot prove it goes RED on bad input enforces nothing. The §6.3
# wiring gate does the STATIC half (res-1 + res-2) under WAVE SEMANTICS (§6.3 / T-10). This suite
# proves each verdict and every wave-direction boundary against the committed fixture app
# (fixtures/wiring-gate/) joined to the real auth manifest (designs/fixtures/auth-interaction-model):
#   GOOD                full app + all-CLOSED-wave results                     -> PASS (0).
#   PF-S87 (dead input) a CLOSED-wave element missing / handler empty body     -> FAIL (1),
#                       naming (screen, wireId).
#   PF-S16 (unserved)   a CLOSED-wave declared endpoint absent from routes.json -> FAIL (1);
#                       the SAME row in an OPEN wave                            -> PENDING, PASS (0)
#                       [T-10 both directions].
#   schema-field        a CLOSED-wave reads/writes field absent from schema.json -> FAIL (1).
#   floor               manifest has rows but the app has ZERO data-oid nodes   -> FAIL (1);
#                       a zero-row manifest                                      -> FATAL (2).
#   integrity hard-dep  a corrupt export digest                                 -> FATAL (2),
#                       WITHOUT running the gate's own checks (§6.2 hard dependency [T-3d]).
#   PEN-CHANGED         a pen-changed export set                                -> PASS (0) + the
#                       PEN-CHANGED marker re-emitted in THIS gate's output.
#   wildcard            res-2 treats a routes.json ':param' segment as a wildcard.
#   assert_red_when_guard_removed on the FIVE load-bearing guards: res-1 element-presence, res-1
#                       handler-non-empty, res-2 route-join, the closed-wave requirement, and the
#                       zero-data-oid floor. Each pairing ISOLATES its guard (the bad input trips
#                       ONLY that guard); the closed-wave and floor pairings use OPEN waves to keep
#                       the promotion / floor from being masked by the closed-wave res-1 path — the
#                       §6.2-review vacuity lesson (anchor on text/behaviour EXCLUSIVE to the guard).
#
# Scope note [N-2]: this suite does NOT claim OPEN-wave mismatch detection — during an open wave a
# defect is PENDING, never FAIL. Nor does it test "wired to a DIFFERENT served route" (res-1
# resolves the handler SYMBOL, not its call target); only "declared endpoint not served" is a res-2
# obligation. Bijection direction: extra app data-oids (built-not-designed) are §6.4, out of scope.
#
# NOT hermetic BY DESIGN (mirrors test-pen-integrity): the §6.2 hard dependency runs against the
# REAL committed .pen resolved from the auth export set (--base = repo root). App / results / schema
# mutations are made on COPIES in a temp dir; the pristine auth export set drives integrity.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/wiring-gate.sh"
DIGEST="${TEST_DIR}/../scripts/pen-digest.sh"
REPO="$(cd "${TEST_DIR}/../../../.." && pwd)"           # skills_library repo root
AUTH="${REPO}/designs/fixtures/auth-interaction-model"  # real journey, .pen committed in-repo
# Portability (update-rigor): design fixture lives OUTSIDE toolkit/ and does not travel with a
# toolkit copy. In a consuming project without designs/fixtures/, LOUD-SKIP so the pulled suite
# stays green — the framework repo (fixture present) still runs the full test.
[ -d "$AUTH" ] || { echo "[test-wiring-gate] SKIP (loud): design fixture absent ($AUTH) — not a design-pipeline checkout"; exit 0; }
FIXROOT="${TEST_DIR}/fixtures/wiring-gate"
APP="${FIXROOT}/app"                                    # the committed GOOD fixture app
GOOD_RESULTS="${FIXROOT}/wiring-results.json"           # all 25 rows -> wave 1 (closed)

WORK="$(mktemp -d "${TMPDIR:-/tmp}/wiring-gate.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

# --- mutation helpers ---------------------------------------------------------
newapp() { local d="$WORK/$1"; rm -rf "$d"; cp -R "$APP" "$d"; echo "$d"; }
newexport() { local d="$WORK/$1"; rm -rf "$d"; cp -R "$AUTH" "$d"; echo "$d"; }

remove_oid() { # $1=appdir $2=data-oid  — delete the HTML line carrying it (element never built)
  python3 - "$1" "$2" <<'PY'
import glob, os, sys
appdir, oid = sys.argv[1], sys.argv[2]
needle = 'data-oid="%s"' % oid
removed = 0
for hp in glob.glob(os.path.join(appdir, "*.html")):
    lines = open(hp).read().splitlines(keepends=True)
    kept = [ln for ln in lines if needle not in ln]
    if len(kept) != len(lines):
        open(hp, "w").write("".join(kept)); removed += len(lines) - len(kept)
assert removed > 0, "remove_oid: no line carried " + needle
PY
}

empty_handler() { # $1=appdir $2=symbol — collapse its body to {} (dead handler)
  python3 - "$1/app.js" "$2" <<'PY'
import re, sys
p, sym = sys.argv[1], sys.argv[2]
s = open(p).read()
s2 = re.sub(r"function " + re.escape(sym) + r"\([^)]*\)\s*\{.*?\n\}",
            "function " + sym + "() {}", s, count=1, flags=re.S)
assert s2 != s, "empty_handler: no match for " + sym
open(p, "w").write(s2)
PY
}

remove_route() { # $1=appdir $2=substr — drop served routes matching substr
  python3 -c "import json;p='$1/routes.json';r=json.load(open(p));r2=[x for x in r if '$2' not in x];assert len(r2)<len(r),'remove_route no-op';json.dump(r2,open(p,'w'),indent=2);open(p,'a').write(chr(10))"
}

wildcard_login_route() { # $1=appdir — replace concrete POST /api/auth/login with a :param route
  python3 -c "import json;p='$1/routes.json';r=[x for x in json.load(open(p)) if x!='POST /api/auth/login'];r.append('POST /api/auth/:action');json.dump(r,open(p,'w'),indent=2);open(p,'a').write(chr(10))"
}

remove_field() { # $1=appdir $2=entity $3=field
  python3 -c "import json;p='$1/schema.json';s=json.load(open(p));s['$2']=[f for f in s['$2'] if f!='$3'];json.dump(s,open(p,'w'),indent=2);open(p,'a').write(chr(10))"
}

results_move() { # $1=dst-file $2=screen $3=wireId $4=wave  (from GOOD_RESULTS)
  python3 - "$GOOD_RESULTS" "$1" "$2" "$3" "$4" <<'PY'
import json, sys
src, dst, screen, wid, wave = sys.argv[1:6]
r = json.load(open(src))
for row in r["rows"]:
    if row["screen"] == screen and row["wireId"] == wid:
        row["wave"] = int(wave)
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}

results_all() { # $1=dst-file $2=wave  — put EVERY row in one wave (from GOOD_RESULTS)
  python3 - "$GOOD_RESULTS" "$1" "$2" <<'PY'
import json, sys
src, dst, wave = sys.argv[1], sys.argv[2], int(sys.argv[3])
r = json.load(open(src))
for row in r["rows"]:
    row["wave"] = wave
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}

corrupt_export() { # $1=exportdir — hand-edit an export without re-stamping (breaks §6.2 CHECK 1)
  python3 -c "p='$1/index.md';s=open(p).read();open(p,'w').write(s.replace('Expected','Xxpected',1))"
}

penchange_export() { # $1=exportdir — set pen-sha256 to a bogus value (§6.2 CHECK 2 signal)
  python3 -c "
f='$1/export.digest'
out=['pen-sha256: deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef' if ln.startswith('pen-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"
}

zero_manifest() { # $1=exportdir — []-manifest, re-stamped so §6.2 CHECK 1 stays clean
  printf '[]\n' > "$1/wiring-manifest.json"
  local h; h="$(bash "$DIGEST" "$1")"
  python3 -c "
f='$1/export.digest'; h='$h'
out=['content-sha256: '+h if ln.startswith('content-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"
}

zero_oid_app() { # $1=dst-appdir — a valid app dir (routes+schema) but ZERO data-oid nodes
  rm -rf "$1"; mkdir -p "$1"
  cp "$APP/routes.json" "$APP/schema.json" "$APP/app.js" "$1/"
  printf '<main data-screen="screen/login"><p>nothing built yet</p></main>\n' > "$1/blank.html"
}

# combined stdout/stderr must (not) match <ere>
assert_output_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qE "$pattern"; then echo "[PASS] output matches /$pattern/"
  else echo "[FAIL] output lacked /$pattern/: $*"; TESTS_FAILED=$((TESTS_FAILED + 1)); fi
}
assert_output_absent() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qE "$pattern"; then
    echo "[FAIL] output UNEXPECTEDLY matched /$pattern/: $*"; TESTS_FAILED=$((TESTS_FAILED + 1))
  else echo "[PASS] output correctly lacks /$pattern/"; fi
}

# =============================================================================
# GOOD: full app + all-CLOSED-wave results -> PASS (0).
# =============================================================================
expect_exit 0 bash "$GATE" "$AUTH" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# PF-S87 (dead input) — element MISSING in a CLOSED wave -> FAIL, naming (screen, wireId).
# =============================================================================
a="$(newapp dead-missing)"; remove_oid "$a" "login/sign-in"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "no element in the app carries data-oid=\"login/sign-in\"" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# PF-S87 (dead input) — handler EMPTY body in a CLOSED wave -> FAIL.
a="$(newapp dead-handler)"; empty_handler "$a" submitSignIn
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "resolves to an empty body" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# PF-S16 (unserved endpoint) — declared endpoint absent from routes.json in a CLOSED wave -> FAIL.
# =============================================================================
a="$(newapp unserved-closed)"; remove_route "$a" "reset/request"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "served by no route in routes.json" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# T-10 other direction: the SAME unserved-endpoint row in an OPEN wave -> PENDING, PASS (0).
results_move "$WORK/res-sendreset-open.json" "screen/reset-request" "send-reset" 2
expect_exit 0 bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-sendreset-open.json" --base "$REPO"
assert_output_contains "reset-request/send-reset: res1=STATIC-PASS res2=PENDING" \
  bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-sendreset-open.json" --base "$REPO"
# and it must NOT claim a CLOSED-WAVE detection on that open row.
assert_output_absent "res-2 CLOSED-WAVE reset-request/send-reset" \
  bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-sendreset-open.json" --base "$REPO"

# =============================================================================
# schema-field missing — a CLOSED-wave reads field absent from schema.json -> FAIL.
# (account.email is read by reset-request/send-reset AND verify-email/resend.)
# =============================================================================
a="$(newapp schema-missing)"; remove_field "$a" account email
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "not present in schema.json" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# res-2 ':param' route is a WILDCARD: replace concrete POST /api/auth/login with POST
# /api/auth/:action — login/sign-in must still resolve (only the wildcard can match it) -> PASS (0).
# =============================================================================
a="$(newapp wildcard)"; wildcard_login_route "$a"
expect_exit 0 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# floor — manifest has rows but the app has ZERO data-oid nodes -> FAIL (1). "built nothing".
# =============================================================================
zero_oid_app "$WORK/zero-oid"
expect_exit 1 bash "$GATE" "$AUTH" --app "$WORK/zero-oid" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "declares ZERO data-oid elements" \
  bash "$GATE" "$AUTH" --app "$WORK/zero-oid" --results "$GOOD_RESULTS" --base "$REPO"

# floor — a zero-ROW manifest -> FATAL (2).
e="$(newexport zero-row)"; zero_manifest "$e"
expect_exit 2 bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "zero interactive-element rows" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# integrity hard-dependency [T-3d] — a corrupt export digest -> FATAL (2) WITHOUT running the
# gate's own checks (no STATIC-PASS line ever prints).
# =============================================================================
e="$(newexport corrupt)"; corrupt_export "$e"
expect_exit 2 bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "refusing to run wiring checks" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_absent "STATIC-PASS" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# PEN-CHANGED propagation — a pen-changed export set -> PASS (0) + the PEN-CHANGED marker
# re-emitted in THIS gate's own output (wave-close consumers grep for it).
# =============================================================================
e="$(newexport pen-changed)"; penchange_export "$e"
expect_exit 0 bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "PEN-CHANGED" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "RESULT: PASS-WITH-PEN-CHANGED" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# Guard-fires pairings (good GREEN, mutant RED) on the FIVE load-bearing guards.
# Each bad input isolates its guard; the closed-wave + floor pairings use OPEN waves so the
# res-1 closed-wave path cannot mask them (the §6.2-review vacuity lesson).
# =============================================================================
G="bash '$GATE' '$AUTH' --app '$APP' --results '$GOOD_RESULTS' --base '$REPO'"   # pristine GOOD

# G1 res-1 element-presence: bad = a CLOSED-wave element removed.
g1="$(newapp g1-bad)"; remove_oid "$g1" "twosv-challenge/verify"
assert_red_when_guard_removed "$G" "bash '$GATE' '$AUTH' --app '$g1' --results '$GOOD_RESULTS' --base '$REPO'"

# G2 res-1 handler-non-empty: bad = a CLOSED-wave element PRESENT with an empty handler body.
g2="$(newapp g2-bad)"; empty_handler "$g2" submitVerify
assert_red_when_guard_removed "$G" "bash '$GATE' '$AUTH' --app '$g2' --results '$GOOD_RESULTS' --base '$REPO'"

# G3 res-2 route-join: bad = a CLOSED-wave declared endpoint removed from routes.json.
g3="$(newapp g3-bad)"; remove_route "$g3" "2sv/verify"
assert_red_when_guard_removed "$G" "bash '$GATE' '$AUTH' --app '$g3' --results '$GOOD_RESULTS' --base '$REPO'"

# G4 closed-wave requirement: the SAME defect, wave state is the only difference.
# good = defect in an OPEN wave (PENDING, 0); bad = defect in a CLOSED wave (promoted FAIL, 1).
g4="$(newapp g4-bad)"; remove_route "$g4" "reset/confirm"       # breaks reset-set-new/update-password
results_move "$WORK/res-updatepw-open.json" "screen/reset-set-new" "update-password" 2
assert_red_when_guard_removed \
  "bash '$GATE' '$AUTH' --app '$g4' --results '$WORK/res-updatepw-open.json' --base '$REPO'" \
  "bash '$GATE' '$AUTH' --app '$g4' --results '$GOOD_RESULTS' --base '$REPO'"

# G5 zero-data-oid floor: bad = zero-oid app; BOTH sides use ALL-OPEN waves so ONLY the floor can
# fail (res-1 failures on the missing nodes are informational under open waves).
results_all "$WORK/res-all-open.json" 2
assert_red_when_guard_removed \
  "bash '$GATE' '$AUTH' --app '$APP' --results '$WORK/res-all-open.json' --base '$REPO'" \
  "bash '$GATE' '$AUTH' --app '$WORK/zero-oid' --results '$WORK/res-all-open.json' --base '$REPO'"

# =============================================================================
# review-pr fix pass (rev2b): BH1/BH2/BH3/BH4/BH5 + comment-body ruling + QA2/QA3/QA4/QA5.
# Each new guard is ALSO scratch-mutation-verified out-of-band (see the SE report); here we pin
# the exit code + a guard-EXCLUSIVE message anchor.
# =============================================================================

# --- extra mutation helpers ---
comment_oid() { # $1=appdir $2=oid — wrap the element's HTML line in <!-- ... --> (BH1)
  python3 - "$1" "$2" <<'PY'
import glob, os, sys
appdir, oid = sys.argv[1], sys.argv[2]
needle = 'data-oid="%s"' % oid; done = 0
for hp in glob.glob(os.path.join(appdir, "*.html")):
    lines = open(hp).read().splitlines(keepends=True); out = []
    for ln in lines:
        if needle in ln and not done:
            out.append("<!-- " + ln.rstrip("\n") + " -->\n"); done = 1
        else:
            out.append(ln)
    open(hp, "w").write("".join(out))
assert done, "comment_oid: no line carried " + needle
PY
}
append_dead_def() { printf 'function %s() {}\n' "$2" >> "$1/app.js"; }  # shadowing empty def (BH3)
comment_only_body() { # $1=appdir $2=symbol — body becomes { /* todo */ } (comment-body ruling)
  python3 - "$1/app.js" "$2" <<'PY'
import re, sys
p, sym = sys.argv[1], sys.argv[2]
s = open(p).read()
s2 = re.sub(r"function " + re.escape(sym) + r"\([^)]*\)\s*\{.*?\n\}",
            "function " + sym + "() { /* todo */ }", s, count=1, flags=re.S)
assert s2 != s, "comment_only_body: no match for " + sym
open(p, "w").write(s2)
PY
}
edit_tag() { # $1=appdir $2=oid $3=python-lambda-on-line  — rewrite the single tag line
  python3 - "$1" "$2" "$3" <<'PY'
import glob, os, re, sys
appdir, oid, expr = sys.argv[1], sys.argv[2], sys.argv[3]
fn = eval("lambda ln: " + expr)
needle = 'data-oid="%s"' % oid; done = 0
for hp in glob.glob(os.path.join(appdir, "*.html")):
    lines = open(hp).read().splitlines(keepends=True); out = []
    for ln in lines:
        if needle in ln and not done:
            out.append(fn(ln)); done = 1
        else:
            out.append(ln)
    open(hp, "w").write("".join(out))
assert done, "edit_tag: no line carried " + needle
PY
}
remove_entity() { python3 -c "import json;p='$1/schema.json';s=json.load(open(p));s.pop('$2',None);json.dump(s,open(p,'w'),indent=2);open(p,'a').write(chr(10))"; }
results_dup() { # $1=dst $2=screen $3=wireId $4=wave  — append a DUPLICATE key row (BH2)
  python3 - "$GOOD_RESULTS" "$1" "$2" "$3" "$4" <<'PY'
import json, sys
src, dst, screen, wid, wave = sys.argv[1:6]
r = json.load(open(src)); r["rows"].append({"screen": screen, "wireId": wid, "wave": int(wave)})
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}
results_set() { # $1=dst $2=python-mutation-on-r  — generic results mutator (BH4/QA2)
  python3 - "$GOOD_RESULTS" "$1" "$2" <<'PY'
import json, sys
src, dst, expr = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(src)); exec(expr)
json.dump(r, open(dst, "w"), indent=2); open(dst, "a").write("\n")
PY
}
restamp() { local h; h="$(bash "$DIGEST" "$1")"; python3 -c "
f='$1/export.digest'; h='$h'
out=['content-sha256: '+h if ln.startswith('content-sha256:') else ln for ln in open(f).read().splitlines()]
open(f,'w').write(chr(10).join(out)+chr(10))
"; }
set_row() { # $1=exportdir $2=screen $3=wireId $4=field $5=python-value  — mutate a manifest row + restamp
  python3 - "$1" "$2" "$3" "$4" "$5" <<'PY'
import ast, json, sys
d, screen, wid, field, val = sys.argv[1:6]; p = d + "/wiring-manifest.json"; m = json.load(open(p))
for row in m:
    if row.get("screen") == screen and row.get("wireId") == wid:
        row[field] = ast.literal_eval(val)
json.dump(m, open(p, "w"), indent=2, sort_keys=True); open(p, "a").write("\n")
PY
  restamp "$1"
}

# --- BH1: a commented-out element does NOT satisfy res-1 (CLOSED wave -> FAIL) ---
a="$(newapp bh1-comment)"; comment_oid "$a" "twosv-challenge/verify"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "no element in the app carries data-oid=\"twosv-challenge/verify\"" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# --- BH2: a duplicate (screen,wireId) results row -> FATAL (no closed-wave laundering) ---
results_dup "$WORK/res-dup.json" "screen/reset-request" "send-reset" 2
expect_exit 2 bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-dup.json" --base "$REPO"
assert_output_contains "duplicate row for screen/reset-request/send-reset" \
  bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-dup.json" --base "$REPO"

# --- BH3: a later shadowing empty def wins (JS runtime uses LAST) -> CLOSED-wave FAIL ---
a="$(newapp bh3-shadow)"; append_dead_def "$a" submitVerify
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "resolves to an empty body" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# --- BH4: a non-list `rows` -> FATAL (parity with the waves-dict guard) ---
results_set "$WORK/res-rowsnull.json" "r['rows'] = None"
expect_exit 2 bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-rowsnull.json" --base "$REPO"
assert_output_contains "'rows' must be a JSON array" \
  bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-rowsnull.json" --base "$REPO"

# --- comment-body ruling: a comment-only handler body is behaviorally EMPTY -> CLOSED-wave FAIL ---
a="$(newapp comment-body)"; comment_only_body "$a" submitVerify
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "resolves to an empty body" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# --- BH5: reads/writes as a bare STRING -> res-2 FAIL (no char-iteration), CLOSED wave ---
e="$(newexport bh5-readsstr)"; set_row "$e" "screen/reset-request" "send-reset" reads "'account.email'"
expect_exit 1 bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "reads must be a list of entity.field" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# --- QA2: inconsistent-wave FATALs (both branches) -> exit 2, distinct anchors ---
results_set "$WORK/res-badstate.json" "r['waves']['1'] = 'frozen'"
expect_exit 2 bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-badstate.json" --base "$REPO"
assert_output_contains "expected .open.\\|.closed." \
  bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-badstate.json" --base "$REPO"
results_set "$WORK/res-waveabsent.json" "[row.__setitem__('wave', 9) for row in r['rows'] if row['screen']=='screen/login' and row['wireId']=='sign-in']"
expect_exit 2 bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-waveabsent.json" --base "$REPO"
assert_output_contains "absent from the waves map" \
  bash "$GATE" "$AUTH" --app "$APP" --results "$WORK/res-waveabsent.json" --base "$REPO"

# --- QA3: open-wave STATIC-FAIL surfacing — missing element in an OPEN wave -> exit 0 + surfaced ---
a="$(newapp qa3-openfail)"; remove_oid "$a" "login/sign-in"
results_move "$WORK/res-signin-open.json" "screen/login" "sign-in" 2
expect_exit 0 bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-signin-open.json" --base "$REPO"
assert_output_contains "login/sign-in: res1=STATIC-FAIL res2=PENDING" \
  bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-signin-open.json" --base "$REPO"
assert_output_contains "note: res-1 STATIC-FAIL" \
  bash "$GATE" "$AUTH" --app "$a" --results "$WORK/res-signin-open.json" --base "$REPO"

# --- QA4: pin the DEDICATED PEN-CHANGED marker line (not just the RESULT line) ---
e="$(newexport qa4-penchg)"; penchange_export "$e"
assert_output_contains "PEN-CHANGED: propagated from §6.2 export-integrity" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# --- QA5: the untested res-1/res-2 sub-branches, one bad fixture each (CLOSED wave -> FAIL) ---
a="$(newapp qa5-hrefhash)"; edit_tag "$a" "login/forgot-password" "re.sub(r' data-handler=\"[^\"]*\"','',re.sub(r'href=\"[^\"]*\"','href=\"#\"',ln))"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "only action is href=\"#\"" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

a="$(newapp qa5-nohandler)"; edit_tag "$a" "twosv-challenge/verify" "re.sub(r' data-handler=\"[^\"]*\"','',ln)"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "carries no data-handler symbol" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

a="$(newapp qa5-undef)"; edit_tag "$a" "login/sign-in" "re.sub(r'data-handler=\"[^\"]*\"','data-handler=\"noSuchFn\"',ln)"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "handler symbol 'noSuchFn' is not defined in app.js" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

a="$(newapp qa5-noentity)"; remove_entity "$a" account
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "entity 'account' is not present in schema.json" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

e="$(newexport qa5-badendpoint)"; set_row "$e" "screen/reset-request" "send-reset" endpoint "'GET'"
expect_exit 1 bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "is not 'METHOD /path'" \
  bash "$GATE" "$e" --app "$APP" --results "$GOOD_RESULTS" --base "$REPO"

# =============================================================================
# blind-verify fixes: N-1 (comment-aware js resolver) + N-2 (unbalanced-HTML-comment note).
# =============================================================================
empty_then_commented_def() { # $1=appdir $2=sym — live def emptied, a COMMENTED real def appended after
  python3 - "$1/app.js" "$2" <<'PY'
import re, sys
p, sym = sys.argv[1], sys.argv[2]; s = open(p).read()
s = re.sub(r"function " + re.escape(sym) + r"\([^)]*\)\s*\{.*?\n\}",
           "function " + sym + "() {}", s, count=1, flags=re.S)
s += "\n/* function " + sym + "() { return post(\"/api/auth/login\", {}); } */\n"
open(p, "w").write(s)
PY
}
string_slash_body() { # $1=appdir $2=sym — a real body with a // comment AND a "//"-containing string (15d probe)
  python3 - "$1/app.js" "$2" <<'PY'
import re, sys
p, sym = sys.argv[1], sys.argv[2]; s = open(p).read()
b = "function " + sym + "() {\n  return post(\"//host/path/api/auth/login\", {}); // do the login\n}"
s = re.sub(r"function " + re.escape(sym) + r"\([^)]*\)\s*\{.*?\n\}", b, s, count=1, flags=re.S)
open(p, "w").write(s)
PY
}

# --- N-1: a COMMENTED-OUT later def must NOT shadow a live (empty) earlier def -> CLOSED-wave FAIL ---
a="$(newapp n1-commented-def)"; empty_then_commented_def "$a" submitSignIn
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "handler 'submitSignIn' resolves to an empty body" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# N-1 control: a real LAST def keeps STATIC-PASS (the BH3 last-def direction is preserved) -> PASS
a="$(newapp n1-real-last)"; printf '\nfunction submitSignIn() { return doAgain(); }\n' >> "$a/app.js"
expect_exit 0 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# N-1 15d probe: a // comment + a "//"-containing string in a REAL body stays STATIC-PASS -> PASS
a="$(newapp n1-slash-string)"; string_slash_body "$a" submitSignIn
expect_exit 0 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# --- N-2: an unbalanced <!-- with a later --> warns (>50% removed), stays fail-closed ---
a="$(newapp n2-unbalanced)"
python3 -c "
open('$a/login.html','w').write(
  '<main data-screen=\"screen/login\">\n<!-- TODO restore this whole form\n'
  '<input data-oid=\"login/email\" data-handler=\"onEmailInput\">\n'
  '<button data-oid=\"login/sign-in\" data-handler=\"submitSignIn\">Sign in</button>\n'
  'padding padding padding padding padding padding padding padding padding\n'
  '<span>end of removed section --></span>\n</main>\n')
"
expect_exit 1 bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"
assert_output_contains "removed >50" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

# --- 9hv: a WELL-FORMED comment-dominant file (no data-oid swallowed) must NOT note ---
# The old >50%-bytes-alone condition false-noted a legit big comment. The tightened
# condition also requires the strip to have consumed data-oid markup. Goes RED if the
# tightening is reverted (the fixture is >50% comment by bytes, zero data-oid inside).
a="$(newapp n2-benign-comment)"
python3 -c "
open('$a/login.html','w').write(
  '<!-- license header line one, long enough to dominate this tiny file byte-wise\n'
  '     license header line two, still no markup in here at all\n'
  '     license header line three, more prose padding to stay over half -->\n'
  '<main data-screen=\"screen/login\">\n'
  '<input data-oid=\"login/email\" data-handler=\"onEmailInput\">\n'
  '<button data-oid=\"login/sign-in\" data-handler=\"submitSignIn\">Sign in</button>\n</main>\n')
"
assert_output_absent "removed >50" \
  bash "$GATE" "$AUTH" --app "$a" --results "$GOOD_RESULTS" --base "$REPO"

test_summary
