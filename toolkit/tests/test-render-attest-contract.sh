#!/usr/bin/env bash
# tests/test-render-attest-contract.sh — the render-before-claiming gate's mechanical
# floor (bead 1ec, improvements plan item 3).
#
# execute-plan's DESIGN GATE requires UI recipes to render UNDER run-attest
# (capture-at-source) and blocks GREEN unless BOTH checks pass: (1) the record
# verifies, (2) the sidecar names each changed screen's PNG as a path+sha line.
# This suite exercises that shape hermetically: the GREEN path (capture, verify,
# content check); RED paths — absent record, tampered-after-capture sidecar, a
# hand-authored record (field-presence reject), a wrong keyed marker with all else
# intact (the keyed layer itself), and a no-op capture that verifies at layer 1
# but fails the sidecar-content check. The stale-RE-EMIT case (a render command
# re-printing an old PNG) is NOT mechanically caught — that is the dispatch
# review's trust surface, stated in the execute-plan wording.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RA="$HERE/../scripts/run-attest.sh"
PASS=0 FAIL=0
ok()  { PASS=$((PASS+1)); echo "PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "FAIL: $1"; }

T="$(mktemp -d)"
export CLAUDE_PROJECT_DIR="$T"
unset RUN_ATTEST_DIR RUN_ATTEST_KEY 2>/dev/null || true   # ambient overrides would escape $T
mkdir -p "$T/.rigor"

# the stub render command: writes a PNG, prints path + sha (the contract's shape)
cat > "$T/render.sh" <<'STUB'
#!/usr/bin/env bash
printf 'PNG-BYTES-%s' "$1" > "$2"
sha="$( (shasum -a 256 "$2" 2>/dev/null || sha256sum "$2") | cut -c1-64 )"
echo "$2 $sha"
STUB
chmod +x "$T/render.sh"

# GREEN: render under run-attest -> capture 0; verify -> ACCEPT 0
bash "$RA" render-r1-home -- bash "$T/render.sh" v1 "$T/home.png" >/dev/null 2>&1
RC=$?
REC="$T/.rigor/run-attest/render-r1-home.json"
if [ "$RC" = 0 ] && [ -f "$REC" ] && [ -f "$T/home.png" ]; then
  ok "render under run-attest captures (record + PNG exist)"
else bad "capture (rc=$RC rec=$([ -f "$REC" ] && echo y || echo n))"; fi
bash "$RA" verify "$REC" >/dev/null 2>&1
[ $? = 0 ] && ok "verify ACCEPTs the genuine capture (GREEN path)" || bad "verify genuine"
# the record binds THIS run's output: the PNG path+sha the command printed are in the sidecar
grep -q "home.png" "$T/.rigor/run-attest/render-r1-home.out" \
  && ok "sidecar carries the artifact path+sha (identity bound to this run)" \
  || bad "sidecar binding"

# RED 1: no attestation record for the claimed screen -> verify FATALs (no silent green)
bash "$RA" verify "$T/.rigor/run-attest/render-r1-settings.json" >/dev/null 2>&1
RC=$?
[ "$RC" = 2 ] && ok "absent record -> verify FATAL 2 (a missing record is not a record)" \
  || bad "absent record (rc=$RC)"

# RED 2: anti-TAMPER (layer 2) — a sidecar swapped after capture REJECTS. (This is
# the tamper leg; the stale-RE-EMIT case — a render command re-printing an old PNG —
# is NOT mechanically caught and is the dispatch review's trust surface, per the
# execute-plan wording. The sidecar-CONTENT check below is what a no-op fails.)
bash "$RA" render-r1-detail -- bash "$T/render.sh" v1 "$T/detail.png" >/dev/null 2>&1
printf 'STALE-OTHER-RUN' > "$T/.rigor/run-attest/render-r1-detail.out"
bash "$RA" verify "$T/.rigor/run-attest/render-r1-detail.json" >/dev/null 2>&1
RC=$?
[ "$RC" = 1 ] && ok "tampered/stale sidecar -> verify REJECT 1 (presence is not freshness)" \
  || bad "stale swap (rc=$RC)"

# the gate's check 2: a NO-OP capture (verifies clean at layer 1/2) fails the
# sidecar-content check — no `<path> <64-hex>` PNG line
bash "$RA" render-r1-noop -- true >/dev/null 2>&1
bash "$RA" verify "$T/.rigor/run-attest/render-r1-noop.json" >/dev/null 2>&1
V=$?
if [ "$V" = 0 ] && ! grep -qE '\.png [0-9a-f]{64}$' "$T/.rigor/run-attest/render-r1-noop.out"; then
  ok "no-op capture verifies at layer 1 but FAILS the sidecar-content check (gate check 2)"
else bad "no-op sidecar-content (verify=$V)"; fi
grep -qE '\.png [0-9a-f]{64}$' "$T/.rigor/run-attest/render-r1-home.out" \
  && ok "genuine render PASSES the sidecar-content check" || bad "genuine content check"

# RED 3: a hand-authored record without the capture key REJECTS or FATALs, never accepts
cat > "$T/.rigor/run-attest/render-r1-forged.json" <<J
{"claim":"render-r1-forged","cmd":"echo x","exit":0,"output_sha":"0000000000000000000000000000000000000000000000000000000000000000","marker":"forged"}
J
printf 'x\n' > "$T/.rigor/run-attest/render-r1-forged.out"
bash "$RA" verify "$T/.rigor/run-attest/render-r1-forged.json" >/dev/null 2>&1
RC=$?
{ [ "$RC" = 1 ] || [ "$RC" = 2 ]; } && ok "hand-authored record never ACCEPTs (rc=$RC)" \
  || bad "forged record accepted (rc=$RC)"

# RED 4: the KEYED marker itself — a record whose ONLY defect is a wrong
# capture_marker (fields well-formed, sidecar intact, sha matching) must reach the
# keyed re-derivation and REJECT. This is the layer an informed forger without the
# 0600 key cannot mint; a neutered marker check ships green without this case.
bash "$RA" render-r1-keyed -- bash "$T/render.sh" v1 "$T/keyed.png" >/dev/null 2>&1
KREC="$T/.rigor/run-attest/render-r1-keyed.json"
python3 - "$KREC" <<'PY'
import json, sys
p = sys.argv[1]
r = json.load(open(p))
for k in list(r):
    if "marker" in k:
        r[k] = "a" * 64
json.dump(r, open(p, "w"))
PY
bash "$RA" verify "$KREC" >/dev/null 2>&1
RC=$?
[ "$RC" = 1 ] && ok "wrong keyed marker (all else intact) -> REJECT at the keyed layer" \
  || bad "keyed-marker case (rc=$RC)"

rm -rf "$T"
echo "----"
echo "render-attest-contract test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = 0 ]
