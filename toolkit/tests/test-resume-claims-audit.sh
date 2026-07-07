#!/usr/bin/env bash
# tests/test-resume-claims-audit.sh — F-007 suite for the resume-claims audit (bead thm).
#
# The dangerous direction is a STALE RESUME READING AS VERIFIED: every path that could
# let a false or vacuous claim produce a green is pinned RED-able — a closed bead
# claimed open FAILs, a nonexistent bead FAILs, a sha off main FAILs, an unlanded PR
# claimed merged FAILs, a claim-free region is loudly VACUOUS, and bd-present-but-
# unreadable is FATAL (never a silent class-1 skip). bd is stubbed hermetically via
# RESUME_AUDIT_BD (the PEN_LINT_BD model — PATH='' would break git first).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUD="$HERE/../scripts/resume-claims-audit.sh"
PASS=0 FAIL=0

ok()  { PASS=$((PASS+1)); echo "PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "FAIL: $1"; }

# --- hermetic world: a git repo with trunk `main`, a .beads dir, and a bd stub --------
T="$(mktemp -d)"
mkdir -p "$T/repo/.beads" "$T/bin"
(cd "$T/repo" && git init -q -b main \
  && git commit -q --allow-empty -m "feat: base (#41)" \
  && git commit -q --allow-empty -m "feat: landed thing (#42)")
MAIN_SHA="$(git -C "$T/repo" rev-parse --short main)"
OLD_SHA="$(git -C "$T/repo" rev-parse --short main~1)"
(cd "$T/repo" && git checkout -qb side && git commit -q --allow-empty -m "off-main" && git checkout -q main)
SIDE_SHA="$(git -C "$T/repo" rev-parse --short side)"

# bd stub: `bd show <id> --json` answers from canned JSON; unknown ids exit 1 empty
cat > "$T/bin/bd" <<'STUB'
#!/usr/bin/env bash
# real bd --json shape: ARRAY-wrapped, space after the colon (arch-verified live)
case "$2" in
  proj-abc) echo '[{"id": "proj-abc", "status": "closed"}]' ;;
  proj-xyz) echo '[{"id": "proj-xyz", "status": "open"}]' ;;
  proj-wip) echo '[{"id": "proj-wip", "status": "in_progress"}]' ;;
  proj-t*)  echo '[{"id": "'"$2"'", "status": "open"}]' ;;
  *) echo '{"error": "not found"}'; exit 1 ;;
esac
STUB
chmod +x "$T/bin/bd"
run() { RESUME_AUDIT_BD="$T/bin/bd" bash "$AUD" "$@"; }

doc() { printf '%s\n' "$@" > "$T/repo/HANDOFF.md"; }
V='## RESUME — VOLATILE'

# --- adoption contract -----------------------------------------------------------------
doc '# Handoff' '## What Changed' 'prose about `proj-abc` closed long ago.'
OUT="$(run "$T/repo/HANDOFF.md")"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "SKIP: no VOLATILE region" \
  && printf '%s' "$OUT" | grep -q "region=absent" \
  && ok "no delimiter -> loud SKIP exit 0 with region=absent coverage" \
  || bad "no delimiter (rc=$RC out=$OUT)"

# claims OUTSIDE the region are exempt even when false
doc '# Handoff' 'Historical: `proj-abc` is open and active.' "$V" 'Next: bead `proj-xyz` is open.'
OUT="$(run "$T/repo/HANDOFF.md")"; RC=$?
[ "$RC" = 0 ] && ok "false claim OUTSIDE the region is exempt (historical prose)" \
  || bad "region scoping leaked (rc=$RC out=$OUT)"

# --- class 1: bead-status --------------------------------------------------------------
doc '# H' "$V" 'Open the work on bead `proj-xyz` (open).'
run "$T/repo/HANDOFF.md" >/dev/null 2>&1 && ok "open bead claimed open -> PASS" || bad "true open claim failed"

doc '# H' "$V" 'Next up: bead `proj-abc` is open and ready.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "claimed open-class but bd status is 'closed'" \
  && ok "closed bead claimed open -> FAIL (the pilot's exact staleness)" \
  || bad "closed-claimed-open (rc=$RC)"

doc '# H' "$V" 'Bead `proj-abc` closed at 1.17.0.'
run "$T/repo/HANDOFF.md" >/dev/null 2>&1 && ok "closed bead claimed closed -> PASS" || bad "true closed claim failed"

doc '# H' "$V" 'Bead `proj-wip` closed last week.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && ok "in_progress bead claimed closed -> FAIL" || bad "false closed claim passed (rc=$RC)"

doc '# H' "$V" 'Bead `proj-ghost` is open.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "cannot find it" \
  && ok "nonexistent bead -> FAIL (false claim, not infra error)" \
  || bad "ghost bead (rc=$RC)"

# --- class 2: trunk position -------------------------------------------------------------
doc '# H' "$V" "main @ \`$MAIN_SHA\` and bead \`proj-abc\` closed."
run "$T/repo/HANDOFF.md" >/dev/null 2>&1 && ok "main @ current sha -> PASS" || bad "current sha failed"

doc '# H' "$V" "main @ \`$OLD_SHA\`."
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "moved past" \
  && ok "main moved past claimed sha -> WARN not FAIL" || bad "behind-sha (rc=$RC out=$OUT)"

doc '# H' "$V" "main @ \`$SIDE_SHA\`."
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "not on main" \
  && ok "sha off main -> FAIL" || bad "off-main sha (rc=$RC)"

doc '# H' "$V" 'main @ `deadbeef1234`.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "no such commit" \
  && ok "nonexistent sha -> FAIL" || bad "ghost sha (rc=$RC)"

# --- class 3: landed PR -----------------------------------------------------------------
doc '# H' "$V" 'The gate landed in #42.'
run "$T/repo/HANDOFF.md" >/dev/null 2>&1 && ok "landed PR on trunk -> PASS" || bad "true landed claim failed"

doc '# H' "$V" 'The gate landed in #99.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q 'ending "(#99)"' \
  && ok "unlanded PR claimed merged -> FAIL" || bad "phantom PR (rc=$RC)"

# --- class 4: heartbeat -----------------------------------------------------------------
doc '# H' "$V" 'Stamped 2020-01-01. Bead `proj-abc` closed.'
OUT="$(run "$T/repo/HANDOFF.md" --heartbeat-limit 1 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "heartbeat" \
  && ok "stale date stamp -> heartbeat WARN, exit 0" || bad "heartbeat (rc=$RC out=$OUT)"

# --- vacuity + coverage -----------------------------------------------------------------
doc '# H' "$V" 'All prose, no machine-checkable statements at all here.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "PASS-VACUOUS" \
  && ok "claim-free region -> loud PASS-VACUOUS, never a silent green" \
  || bad "vacuous region (rc=$RC out=$OUT)"

doc '# H' "$V" 'Bead `proj-abc` closed. Also mentioning `proj-misc` with no status wording.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"
printf '%s' "$OUT" | grep -q "unparsed=1" \
  && ok "unmatched bead token counted as unparsed coverage" || bad "coverage counter ($OUT)"

# --- fail-closed: bd present-but-unresolvable -------------------------------------------
doc '# H' "$V" 'Bead `proj-abc` closed.'
OUT="$(RESUME_AUDIT_BD="$T/bin/no-such-bd" bash "$AUD" "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 2 ] && printf '%s' "$OUT" | grep -q "bd is unresolvable" \
  && ok ".beads present + bd unresolvable -> FATAL (never a silent class-1 skip)" \
  || bad "bd-unresolvable (rc=$RC out=$OUT)"

# no .beads at all -> loud class-1 skip, other classes still run
mkdir -p "$T/nobeads" && (cd "$T/nobeads" && git init -q -b main && git commit -q --allow-empty -m "x (#7)")
printf '%s\n' '# H' "$V" 'Bead `proj-abc` closed. The thing landed in #999.' > "$T/nobeads/H.md"
OUT="$(RESUME_AUDIT_BD="$T/bin/bd" bash "$AUD" "$T/nobeads/H.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "no .beads directory" \
  && ok "no .beads -> loud class-1 skip; class 3 STILL verifies (false #999 FAILs)" \
  || bad "no-beads path (rc=$RC out=$OUT)"

# review fixes (six-agent pass): each executed finding pinned RED-able
# BUG-1: a bead id whose suffix is a status word must not self-trigger a claim
doc '# H' "$V" 'Remember `proj-done` in the backlog for later cleanup work.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "unparsed=1" \
  && ok "id-suffix status word does not self-trigger (token visible as unparsed)" \
  || bad "proj-done self-trigger (rc=$RC out=$OUT)"
# BUG-2: multi-token sentences are ambiguous binding -> unparsed, never misbound
doc '# H' "$V" 'This subsumes `proj-abc` and bead `proj-xyz` is open.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "unparsed=2" \
  && ok "multi-token sentence -> ambiguous, both tokens unparsed (no misbinding)" \
  || bad "multi-token binding (rc=$RC out=$OUT)"
# BUG-3: a commit MENTIONING (#N) mid-subject must not verify a landing
(cd "$T/repo" && git commit -q --allow-empty -m "chore: mentions (#77) in passing here")
doc '# H' "$V" 'The feature landed in #77.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && ok "mention-only (#77) does not verify a landing -> FAIL" \
  || bad "mention-only false PASS (rc=$RC out=$OUT)"
# BUG-4: a master-trunk consumer verifies truthfully
M="$(mktemp -d)"; mkdir -p "$M/.beads"
(cd "$M" && git init -q -b master && git commit -q --allow-empty -m "feat: thing (#8)")
MS="$(git -C "$M" rev-parse --short master)"
printf '%s\n' '# H' "$V" "Landed in #8. main @ \`$MS\`." > "$M/H.md"
OUT="$(RESUME_AUDIT_BD="$T/bin/bd" bash "$AUD" "$M/H.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && ok "master-trunk repo: landed + trunk claims verify (no hardcoded main)" \
  || bad "master trunk (rc=$RC out=$OUT)"
rm -rf "$M"
# BUG-6: a future prose date must not suppress the heartbeat when a Stamped line exists
doc '# H' "$V" 'Stamped 2020-01-01, target 2099-12-31. Bead `proj-abc` closed.'
OUT="$(run "$T/repo/HANDOFF.md" --heartbeat-limit 1 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "heartbeat" \
  && ok "Stamped line anchors the heartbeat past future prose dates" \
  || bad "heartbeat anchor (rc=$RC out=$OUT)"
# sec HIGH: fenced content neither opens a phantom region nor terminates a real one
doc '# H' "$V" 'Bead `proj-abc` closed.' '```bash' '# start here' 'run this' '```' 'Bead `proj-wip` closed at the end.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 1 ] && printf '%s' "$OUT" | grep -q "proj-wip" \
  && ok "a # comment in a fence does not truncate the region (post-fence false claim still FAILs)" \
  || bad "fence truncation (rc=$RC out=$OUT)"
doc '# H' 'intro prose' '```' '## EXAMPLE — VOLATILE' 'Bead `proj-abc` is open.' '```'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "SKIP: no VOLATILE region" \
  && ok "a fenced VOLATILE heading opens no phantom region" \
  || bad "phantom region (rc=$RC out=$OUT)"
# BUG-8: adopted-but-emptied region is not an un-adopted SKIP
doc '# H' "$V"
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "present but EMPTY" \
  && ok "emptied region -> loud EMPTY warn, not un-adopted SKIP" \
  || bad "emptied region (rc=$RC out=$OUT)"
# QA MUST FIX: a false claim in a mixed-keyword sentence must not pass SILENTLY —
# the unverified-tokens WARN makes unparsed>0 loud even when parsed>0
doc '# H' "$V" 'Bead `proj-abc` closed. Meanwhile bead `proj-xyz` is closed though the epic stays open.'
OUT="$(run "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
[ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "WARN: .*NOT verified" \
  && ok "mixed-keyword sentence -> loud unverified-tokens WARN (never a silent PASS)" \
  || bad "mixed-keyword silence (rc=$RC out=$OUT)"
# sec MED-3: unique-id bd calls are bounded, loudly
BULK=""
for i in 1 2 3 4 5; do BULK="${BULK}Bead \`proj-t${i}\` is open. "; done
doc '# H' "$V" "$BULK"
OUT="$(RESUME_AUDIT_BD="$T/bin/bd" RESUME_AUDIT_BD_LIMIT=2 bash "$AUD" "$T/repo/HANDOFF.md" 2>&1)"; RC=$?
printf '%s' "$OUT" | grep -q "bd call limit" \
  && ok "bd call limit is loud and bounded" || bad "bd bound ($OUT)"

# doc outside any git repo -> classes 2-4 skip LOUDLY; unverified tokens are unparsed
G="$(mktemp -d)"
printf '%s\n' '# H' "$V" 'Bead `proj-abc` closed. Landed in #5. main @ `abcdef1`.' > "$G/h.md"
OUT="$(RESUME_AUDIT_BD="$T/bin/bd" bash "$AUD" "$G/h.md" 2>&1)"; RC=$?
if [ "$RC" = 0 ] && printf '%s' "$OUT" | grep -q "not inside a git repo" \
   && printf '%s' "$OUT" | grep -q "unparsed=1"; then
  ok "no-git doc -> loud classes-2-4 skip; unverified bead token counted unparsed"
else bad "no-git doc (rc=$RC out=$OUT)"; fi
rm -rf "$G"

# missing doc -> FATAL
bash "$AUD" "$T/absent.md" >/dev/null 2>&1
[ $? = 2 ] && ok "missing doc -> FATAL" || bad "missing doc not FATAL"

# --- F-007 reversion probe: the class-1 verification is load-bearing --------------------
# mutant: bd stub that answers EVERYTHING closed — the closed-claimed-open case must
# stay RED-able (i.e., our earlier FAIL case relied on real status, and a stub change
# flips outcomes). Prove outcomes differ across stubs for the same doc.
cat > "$T/bin/bd-always-open" <<'STUB'
#!/usr/bin/env bash
echo '{"id":"x","status":"open"}'
STUB
chmod +x "$T/bin/bd-always-open"
doc '# H' "$V" 'Next up: bead `proj-abc` is open and ready.'
RESUME_AUDIT_BD="$T/bin/bd" bash "$AUD" "$T/repo/HANDOFF.md" >/dev/null 2>&1; RC1=$?
RESUME_AUDIT_BD="$T/bin/bd-always-open" bash "$AUD" "$T/repo/HANDOFF.md" >/dev/null 2>&1; RC2=$?
[ "$RC1" = 1 ] && [ "$RC2" = 0 ] \
  && ok "verification consumes real bd status (outcome flips with the stub) — not vacuous" \
  || bad "reversion probe (real=$RC1 always-open=$RC2)"

rm -rf "$T"
echo "----"
echo "resume-claims-audit test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = 0 ]
