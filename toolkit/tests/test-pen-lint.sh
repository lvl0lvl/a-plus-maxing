#!/usr/bin/env bash
# tests/test-pen-lint.sh — F-007 negative test for scripts/pen-lint.sh.
#
# F-007 obligation: a lint that cannot prove it goes RED on bad input enforces nothing.
# pen-lint is the design-time gate over the Interaction-Model exports (spec §6.1 checks
# 1-6,8 + the §6/T-1 non-vacuity floor + the §5 on-export value checks). So the suite
# proves: the committed GOOD golden export → PASS (0); each isolated violation → RED (1
# FAIL or 2 FATAL as the check specifies); the zero-element universe → FATAL (the floor's
# own F-007); and assert_red_when_guard_removed pairings on the load-bearing cases.
#
# METHOD: the ONE committed fixture is good/ (the format's golden export, also the format
# deliverable). Each bad case is good/ COPIED to a temp dir with exactly ONE mutation — the
# mutation IS the isolation, and there is no drifting family of near-duplicate committed
# sets. Digests are not recomputed for bad copies: pen-lint does not read export.digest
# (digest verification is the §6.2 Phase-2 gate), so a stale digest is irrelevant here.
#
# ck8 (deferredRef resolution) shells out to `bd show <id> --json`. The suite stubs `bd` on
# PATH (open/closed/missing by id) so it is hermetic; the real pen-lint uses the real `bd`.
# The bd-absent fail-closed path is exercised via PEN_LINT_BD pointed at a missing binary.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/pen-lint.sh"
GOOD="${TEST_DIR}/fixtures/pen-lint/good"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/pen-lint-fix.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

# --- hermetic `bd` stub: supports `bd show <id> --json` ------------------------
# Real bd 0.49.0 differs by environment (both measured):
#   healthy daemon: `bd show <id> --json` on a FOUND id emits [{... "status":"open|closed" ...}]
#     exit 0; a MISSING id emits {"error":...} on STDOUT, exit 1.
#   legacy-DB / direct-mode fallback (the daemon can't start on an old schema and drops to
#     direct mode): the lookup can exit 0 with EMPTY stdout and the error on stderr — a real
#     exit-0/empty-stdout case, not a measurement artifact. pen-lint must survive it.
# The stub reproduces both STDOUT shapes: *-open* / *-closed* (found) / *-empty* (empty stdout +
# stderr error) / else the {"error":...} missing form. pen-lint reads status from the JSON only
# and never the exit code, so every not-open path resolves to a clean FAIL regardless of it.
STUB="$WORK/stub-bin"
mkdir -p "$STUB"
cat > "$STUB/bd" <<'BD'
#!/usr/bin/env bash
id="$2"
case "$id" in
  *-open*)   printf '[{"id":"%s","status":"open"}]\n' "$id"; exit 0 ;;
  *-closed*) printf '[{"id":"%s","status":"closed"}]\n' "$id"; exit 0 ;;
  *-empty*)  echo "Error: no issue found matching \"$id\"" >&2; exit 1 ;;
  *)         printf '{"error":"no issue found matching \\"%s\\""}\n' "$id"; exit 1 ;;
esac
BD
chmod +x "$STUB/bd"

# --- mutation helpers ---------------------------------------------------------
newcase() { # $1=name -> echoes a fresh good/ copy dir
  local d="$WORK/$1"
  rm -rf "$d"; cp -R "$GOOD" "$d"; echo "$d"
}

with_manifest() { # $1=dir  $2=python body operating on list `m`
  python3 - "$1" "$2" <<'PY'
import json, sys
d, body = sys.argv[1], sys.argv[2]
p = d + "/wiring-manifest.json"
m = json.load(open(p))
exec(body)
json.dump(m, open(p, "w"), sort_keys=True, indent=2)
open(p, "a").write("\n")
PY
}

with_machine() { # $1=dir  $2=python body operating on dict `mc`
  python3 - "$1" "$2" <<'PY'
import json, sys
d, body = sys.argv[1], sys.argv[2]
p = d + "/machine.incident-mgmt.json"
mc = json.load(open(p))
exec(body)
json.dump(mc, open(p, "w"), sort_keys=True, indent=2)
open(p, "a").write("\n")
PY
}

DIGEST="${TEST_DIR}/../scripts/pen-digest.sh"

# assert_output_contains <ere> <cmd...> — the run must emit <ere> on combined stdout/stderr.
assert_output_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qE "$pattern"; then
    echo "[PASS] output matches /$pattern/"
  else
    echo "[FAIL] output lacked /$pattern/: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# assert_one_fail_matching <ere> <cmd...> — EXACTLY one `FAIL:` line, and it matches <ere>.
# Guards against a bad-type field iterating per-character into a flood of garbage FAILs.
assert_one_fail_matching() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  nfail="$(printf '%s\n' "$out" | grep -c 'FAIL:')"
  if [ "$nfail" = "1" ] && printf '%s' "$out" | grep -qE "$pattern"; then
    echo "[PASS] exactly one FAIL matching /$pattern/"
  else
    echo "[FAIL] wanted 1 FAIL matching /$pattern/, got $nfail FAIL line(s): $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# =============================================================================
# GOOD: the committed golden export set passes clean.
# =============================================================================
expect_exit 0 bash "$GATE" "$GOOD"

# =============================================================================
# floor (§6/T-1): zero-element universe -> FATAL (2) — the floor's own F-007.
# =============================================================================
d="$(newcase zero-element)"; with_manifest "$d" 'del m[:]'
expect_exit 2 bash "$GATE" "$d"

# floor per-screen undercount: index expects 4 for incident-review, manifest has 3 -> FAIL (1).
d="$(newcase floor-undercount)"
sed 's/Expected interactive elements: 3/Expected interactive elements: 4/' "$GOOD/index.md" > "$d/index.md"
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck1 naming grammar: role not in the §4.1 set -> FAIL (1).
# =============================================================================
d="$(newcase ck1-grammar)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["name"]="button/submit-report"'
expect_exit 1 bash "$GATE" "$d"

# ck2 default (f<n>) name -> FAIL (1).
d="$(newcase ck2-default-name)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="notes")["name"]="f3"'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck3 name<->metadata mismatch: valid grammar, but <what> != wireId -> FAIL (1).
# =============================================================================
d="$(newcase ck3-coherence)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["name"]="btn/submit-reprt"'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck4 duplicate (screen,wireId) -> FAIL (1).
# =============================================================================
d="$(newcase ck4-dup)"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="submit-report"); m.append(dict(r))'
expect_exit 1 bash "$GATE" "$d"

# ck4 dangling transition wireId: add a transition whose fromWireId is in no manifest row.
d="$(newcase ck4-dangling)"
with_machine "$d" 'mc["on"]["GHOST"]=[{"fromWireId":"ghost-button","guard":"","target":"dashboard"}]'
expect_exit 1 bash "$GATE" "$d"

# ck4 retired re-mint: mint a manifest row for a retired (screen,wireId) -> FAIL (1).
d="$(newcase ck4-remint)"
with_manifest "$d" 'm.append({"name":"filter/legacy-filter","screen":"screen/dashboard","wireId":"legacy-filter","action":"filter","endpoint":"none","destination":"self","ephemeral":True,"localEffect":"Filter the dashboard list","status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck5 comp-definition carrying a screen wireId -> FAIL (1).
# =============================================================================
d="$(newcase ck5-comp-def)"
with_manifest "$d" 'm.append({"name":"comp/MetricCard","screen":"screen/dashboard","wireId":"metric-card","action":"navigate","endpoint":"none","destination":"screen/incident-review","ephemeral":False,"status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# ck5 unnamed ref instance (empty instance-name prefix in the minted wireId) -> FAIL (1).
# Coverage is satisfied independently (ephemeral) so ONLY ck5 fires.
d="$(newcase ck5-unnamed-instance)"
with_manifest "$d" 'm.append({"name":"toggle/drill","screen":"screen/dashboard","wireId":".drill","action":"toggle","endpoint":"none","destination":"self","ephemeral":True,"localEffect":"Expand the metric drilldown","status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck6 coverage: reads-only, non-ephemeral, no transition -> FAIL (1).
# =============================================================================
d="$(newcase ck6-coverage)"
with_manifest "$d" 'm.append({"name":"input/lookup","screen":"screen/dashboard","wireId":"lookup","action":"search","reads":["incident.id"],"endpoint":"none","destination":"self","ephemeral":False,"status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# §5 writes + endpoint:"none" -> FAIL (1) (writes mean a persisted effect).
# =============================================================================
d="$(newcase s5-writes-none)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]="none"'
expect_exit 1 bash "$GATE" "$d"

# §5 ephemeral without localEffect -> FAIL (1). Coverage kept via destination!=self + transition.
d="$(newcase s5-ephemeral-no-le)"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["ephemeral"]=True'
expect_exit 1 bash "$GATE" "$d"

# §5 localEffect without ephemeral -> FAIL (1) (the vice-versa direction).
d="$(newcase s5-le-no-ephemeral)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["localEffect"]="flash a toast"'
expect_exit 1 bash "$GATE" "$d"

# §5 action off-enum without an allowlisted x- -> FAIL (1).
d="$(newcase s5-action-offenum)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="frobnicate"'
expect_exit 1 bash "$GATE" "$d"

# §5 x-<custom> action NOT in config.json xActions allowlist -> FAIL (1).
d="$(newcase s5-xaction-unlisted)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="x-teleport"'
expect_exit 1 bash "$GATE" "$d"

# §5 x-<custom> allowlisted (x-annotate) WITH a transition whose event == the action -> PASS (0).
d="$(newcase s5-xaction-listed)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="x-annotate"'
with_machine "$d" 'mc["on"]["x-annotate"]=[{"fromWireId":"new-incident","guard":"","target":"incident-review"}]'
expect_exit 0 bash "$GATE" "$d"

# §5 x-<custom> allowlisted but NO transition whose event == the action -> FAIL (1) (T-03 strict).
# new-incident's only transition event is NEW_INCIDENT, not x-annotate -> the strict match fails.
d="$(newcase s5-xaction-no-match)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="x-annotate"'
expect_exit 1 bash "$GATE" "$d"

# §5 inherently-persisted action with ephemeral:true -> FAIL (1). Isolated fresh row.
d="$(newcase s5-persisted-ephemeral)"
with_manifest "$d" 'm.append({"name":"btn/save-draft","screen":"screen/dashboard","wireId":"save-draft","action":"add","endpoint":"none","destination":"self","ephemeral":True,"localEffect":"Buffer the draft locally","status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# §5 malformed endpoint entry inside a LIST -> FAIL (1).
d="$(newcase s5-endpoint-list)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]=["POST /incidents/:id/submit","notaverb /x"]'
expect_exit 1 bash "$GATE" "$d"

# §5 malformed reads entity.field -> FAIL (1).
d="$(newcase s5-entity-field)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="notes")["reads"]=["Incident..notes"]'
expect_exit 1 bash "$GATE" "$d"

# §5 shell:true with a shellStates reference to a nonexistent screen -> FAIL (1).
d="$(newcase s5-shellstates)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="incidents")["shellStates"]=["screen/ghost"]'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# ck8 deferredRef resolution (bd stubbed on PATH; deferredRef file under --base).
# =============================================================================
# GOOD deferral: file exists + symbol present + bead OPEN -> PASS (0).
d="$(newcase ck8-good)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){ return 1 }\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:handleNewIncident + sk-open-1"'
expect_exit 0 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 phantom file (missing file) -> FAIL (1).
d="$(newcase ck8-phantom-file)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/nope.js:handleNewIncident + sk-open-1"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 absent symbol (file exists, symbol not present) -> FAIL (1).
d="$(newcase ck8-absent-symbol)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:ghostSymbol + sk-open-1"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 CLOSED bead -> FAIL (1).
d="$(newcase ck8-closed-bead)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:handleNewIncident + sk-closed-1"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 MISSING bead (bd resolves nothing) -> FAIL (1).
d="$(newcase ck8-missing-bead)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:handleNewIncident + sk-ghost-1"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 status:deferred with NO deferredRef -> FAIL (1).
d="$(newcase ck8-no-ref)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["status"]="deferred"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# ck8 bd resolver ABSENT -> FATAL (2) fail-closed (F-008); AUDIT_ALLOW_SKIP=1 downgrades -> PASS (0).
d="$(newcase ck8-bd-absent)"; mkdir -p "$d/refs"; printf 'function handleNewIncident(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:handleNewIncident + sk-open-1"'
expect_exit 2 env PEN_LINT_BD="/no/such/bd" bash "$GATE" "$d" --base "$d"
expect_exit 0 env PEN_LINT_BD="/no/such/bd" AUDIT_ALLOW_SKIP=1 bash "$GATE" "$d" --base "$d"

# =============================================================================
# floor fail-open (T-01/T-02): malformed screen header + undeclared manifest screen.
# =============================================================================
# A malformed h2 heading that mentions a screen but has trailing text -> FATAL (2): counts
# must not be silently mis-attributed.
d="$(newcase floor-bad-header)"
sed 's|## screen/dashboard|## screen/dashboard — Main view|' "$GOOD/index.md" > "$d/index.md"
expect_exit 2 bash "$GATE" "$d"

# N-1: an h3+ sub-heading that merely mentions a screen is NOT a malformed h2 header -> PASS (0).
# (The guard anchors to h2 only; h3 `### screen/... notes` must not FATAL.)
d="$(newcase floor-h3-subheading)"
printf '\n### screen/dashboard notes\n\nContext notes about the dashboard screen.\n' >> "$d/index.md"
expect_exit 0 bash "$GATE" "$d"

# A manifest row for a screen with NO index expected-count escapes the floor -> FAIL (1).
d="$(newcase floor-undeclared-screen)"
with_manifest "$d" 'm.append({"name":"btn/ghost","screen":"screen/ghosttown","wireId":"ghost","action":"navigate","endpoint":"none","destination":"screen/dashboard","ephemeral":True,"localEffect":"noop marker","status":"planned"})'
expect_exit 1 bash "$GATE" "$d"

# =============================================================================
# digest (T-05): the committed content digest recomputes, and a one-byte edit changes it.
# export.digest is now the §5 format-v0 ENVELOPE (§6.2 / architect-F3): pen-digest.sh still
# emits ONLY the bare content hash (its unchanged Phase-1a contract), which is the envelope's
# `content-sha256:` line — so this asserts THAT line recomputes. The envelope's other fields
# (pen-sha256 / pen-path / stamped) are the §6.2 pen-integrity gate's concern (test-pen-integrity.sh).
# =============================================================================
recomputed="$(bash "$DIGEST" "$GOOD")"
stored="$(sed -n 's/^content-sha256: //p' "$GOOD/export.digest" | head -n1)"
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$recomputed" = "$stored" ]; then
  echo "[PASS] committed export.digest recomputes ($stored)"
else
  echo "[FAIL] digest mismatch: recomputed=$recomputed stored=$stored"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
d="$(newcase digest-negative)"
python3 -c "p='$d/config.json'; s=open(p).read(); open(p,'w').write(s.replace('safety-platform','safety-platfXrm',1))"
edited="$(bash "$DIGEST" "$d")"
TESTS_RUN=$((TESTS_RUN + 1))
if [ "$edited" != "$stored" ]; then
  echo "[PASS] one-byte export edit changes the digest"
else
  echo "[FAIL] digest unchanged after a one-byte edit"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# T-04: a file without exactly one trailing newline -> pen-digest FATAL (2); restore -> green.
d="$(newcase digest-trailing-nl)"
python3 -c "p='$d/config.json'; s=open(p).read(); open(p,'w').write(s.rstrip(chr(10)))"
expect_exit 2 bash "$DIGEST" "$d"
python3 -c "p='$d/config.json'; s=open(p).read(); open(p,'w').write(s if s.endswith(chr(10)) else s+chr(10))"
expect_exit 0 bash "$DIGEST" "$d"

# =============================================================================
# ck6 non-exempt for deferred rows (T-08): deferral defers implementation, not design.
# =============================================================================
# A deferred row WITHOUT a transition and not ephemeral must still FAIL ck6, with the message.
d="$(newcase ck6-deferred-uncovered)"; mkdir -p "$d/refs"; printf 'function h(){}\n' > "$d/refs/h.js"
with_manifest "$d" 'm.append({"name":"btn/later","screen":"screen/dashboard","wireId":"later","action":"navigate","endpoint":"none","destination":"screen/incident-review","ephemeral":False,"status":"deferred","deferredRef":"refs/h.js:h + sk-open-1"})'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"
assert_output_contains "deferred element must still declare its transition or ephemeral" \
  env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"
# (a deferred row WITH a transition passing is already proven by ck8-good above: new-incident
# is deferred there and carries the NEW_INCIDENT transition.)

# =============================================================================
# §5 endpoint sub-branches (T-12): bad-string / empty-list / wrong-type / method-no-path.
# =============================================================================
d="$(newcase s5-endpoint-badstring)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]="POST-incidents"'
expect_exit 1 bash "$GATE" "$d"

d="$(newcase s5-endpoint-emptylist)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]=[]'
expect_exit 1 bash "$GATE" "$d"

d="$(newcase s5-endpoint-wrongtype)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]=123'
expect_exit 1 bash "$GATE" "$d"

d="$(newcase s5-endpoint-nopath)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]=["POST"]'
expect_exit 1 bash "$GATE" "$d"

# §5 writes-direction entity.field (the reads-direction is covered above) -> FAIL (1).
d="$(newcase s5-writes-field)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="submit-report")["writes"]=["incident..status"]'
expect_exit 1 bash "$GATE" "$d"

# §5 shellStates present WITHOUT shell:true -> FAIL (1).
d="$(newcase s5-shellstates-noshell)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="new-incident")["shellStates"]=["screen/dashboard"]'
expect_exit 1 bash "$GATE" "$d"

# ck2 name-absent (distinct from the default-name branch) -> FAIL (1).
d="$(newcase ck2-name-absent)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="notes").pop("name",None)'
expect_exit 1 bash "$GATE" "$d"

# ck8 malformed-but-present deferredRef -> FAIL (1) (parse fails before any bd call).
d="$(newcase ck8-malformed-ref)"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="not a valid ref"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# =============================================================================
# ck8 empty-stdout parser branch (T-13): bd emits nothing on stdout -> unresolved -> FAIL (1).
# =============================================================================
d="$(newcase ck8-empty-stdout)"; mkdir -p "$d/refs"; printf 'function h(){}\n' > "$d/refs/handler.js"
with_manifest "$d" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:h + sk-empty-1"'
expect_exit 1 env PATH="$STUB:$PATH" bash "$GATE" "$d" --base "$d"

# =============================================================================
# §5 reads/writes type-check (T-14): a bare string is ONE clean FAIL, not per-char garbage.
# =============================================================================
d="$(newcase s5-reads-nonlist)"
with_manifest "$d" 'next(r for r in m if r["wireId"]=="notes")["reads"]="incident.notes"'
assert_one_fail_matching "reads must be a list" bash "$GATE" "$d"

# =============================================================================
# Guard-fires pairings on the load-bearing cases (good GREEN, mutant RED).
# =============================================================================
zdir="$WORK/gp-zero"; rm -rf "$zdir"; cp -R "$GOOD" "$zdir"; with_manifest "$zdir" 'del m[:]'
assert_red_when_guard_removed "bash '$GATE' '$GOOD'" "bash '$GATE' '$zdir'"

cdir="$WORK/gp-cov"; rm -rf "$cdir"; cp -R "$GOOD" "$cdir"
with_manifest "$cdir" 'm.append({"name":"input/lookup","screen":"screen/dashboard","wireId":"lookup","action":"search","reads":["incident.id"],"endpoint":"none","destination":"self","ephemeral":False,"status":"planned"})'
assert_red_when_guard_removed "bash '$GATE' '$GOOD'" "bash '$GATE' '$cdir'"

wdir="$WORK/gp-writes"; rm -rf "$wdir"; cp -R "$GOOD" "$wdir"
with_manifest "$wdir" 'next(r for r in m if r["wireId"]=="submit-report")["endpoint"]="none"'
assert_red_when_guard_removed "bash '$GATE' '$GOOD'" "bash '$GATE' '$wdir'"

# ck8 pairing: resolving deferral GREEN, same deferral with a CLOSED bead RED.
gd="$WORK/gp-ck8-good"; rm -rf "$gd"; cp -R "$GOOD" "$gd"; mkdir -p "$gd/refs"; printf 'function handleNewIncident(){}\n' > "$gd/refs/handler.js"
with_manifest "$gd" 'r=next(x for x in m if x["wireId"]=="new-incident"); r["status"]="deferred"; r["deferredRef"]="refs/handler.js:handleNewIncident + sk-open-1"'
bd_c="$WORK/gp-ck8-closed"; rm -rf "$bd_c"; cp -R "$gd" "$bd_c"
with_manifest "$bd_c" 'next(r for r in m if r["wireId"]=="new-incident")["deferredRef"]="refs/handler.js:handleNewIncident + sk-closed-1"'
assert_red_when_guard_removed \
  "PATH='$STUB:$PATH' bash '$GATE' '$gd' --base '$gd'" \
  "PATH='$STUB:$PATH' bash '$GATE' '$bd_c' --base '$bd_c'"

# x-strict pairing (T-03): allowlisted x-action WITH a matching transition GREEN; the same
# allowlisted x-action WITHOUT one RED.
xg="$WORK/gp-xstrict-good"; rm -rf "$xg"; cp -R "$GOOD" "$xg"
with_manifest "$xg" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="x-annotate"'
with_machine "$xg" 'mc["on"]["x-annotate"]=[{"fromWireId":"new-incident","guard":"","target":"incident-review"}]'
xb="$WORK/gp-xstrict-bad"; rm -rf "$xb"; cp -R "$GOOD" "$xb"
with_manifest "$xb" 'next(r for r in m if r["wireId"]=="new-incident")["action"]="x-annotate"'
assert_red_when_guard_removed "bash '$GATE' '$xg'" "bash '$GATE' '$xb'"

test_summary
