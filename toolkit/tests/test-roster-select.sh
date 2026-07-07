#!/usr/bin/env bash
# tests/test-roster-select.sh — F-007 suite for the roster classifier (bead gw5).
#
# The dangerous direction is UNDER-review: every case that could let a substantive
# change reach a reduced roster is pinned RED-able here — a code diff can never emit
# docs-3, a deletion counts, the scaffold override cannot climb over rule-1/2, the
# justification echo is load-bearing, and design=yes cannot silently drop when the
# UI-class lib is gone (FATAL, not design=no).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RS="$HERE/../scripts/roster-select.sh"
PASS=0 FAIL=0

check() { # check <desc> <want-substring> <want-exit> -- <args...>
  local desc="$1" want="$2" wexit="$3"; shift 4
  local out rc
  out="$(bash "$RS" "$@" 2>/dev/null)"; rc=$?
  if [ "$rc" = "$wexit" ] && printf '%s' "$out" | grep -qF "$want"; then
    PASS=$((PASS+1)); echo "PASS: $desc"
  else
    FAIL=$((FAIL+1)); echo "FAIL: $desc (exit=$rc want=$wexit; out=$out)"
  fi
}

# rule-2: a code diff can NEVER emit docs-3 (the mutant that drops rule-2 goes RED here)
check "one .sh file -> full-6"            "roster=full-6"  0 -- --files scripts/thing.sh
check "code never docs-3"                 "reason=rule-2"  0 -- --files docs/readme.md src/logic.py
# --files mode is path-based (no add/remove signal); the real deletion/rename clause
# is pinned in RANGE mode below with a non-FATAL-satisfiable assertion
# rule-1: sensitive classes, not overridable
check "auth path -> full-6 rule-1"        "reason=rule-1"  0 -- --files src/auth/login.md
check "migration -> full-6 rule-1"        "reason=rule-1"  0 -- --files db/migrations/0001.md
check "CI workflow -> full-6 rule-1"      "reason=rule-1"  0 -- --files .github/workflows/ci.yml
OUT_ERR="$(bash "$RS" --files src/auth/login.md --override scaffold --justification x 2>&1 >/dev/null)"
if printf '%s' "$OUT_ERR" | grep -q "REFUSED — rule-1"; then
  PASS=$((PASS+1)); echo "PASS: override refused by name on rule-1"
else FAIL=$((FAIL+1)); echo "FAIL: override refused by name on rule-1 ($OUT_ERR)"; fi
OUT_ERR="$(bash "$RS" --files src/logic.py --override scaffold --justification x 2>&1 >/dev/null)"
if printf '%s' "$OUT_ERR" | grep -q "REFUSED — rule-2"; then
  PASS=$((PASS+1)); echo "PASS: override refused by name on rule-2"
else FAIL=$((FAIL+1)); echo "FAIL: override refused by name on rule-2 ($OUT_ERR)"; fi
# rule-4: scaffold reduction only via override+justification; echo is load-bearing
check "lockfile w/o override -> full-6"   "reason=rule-4-default" 0 -- --files package-lock.json
check "lockfile + override -> subset"     "roster=code-subset-3"  0 -- --files package-lock.json --override scaffold --justification "regenerated lockfile only"
check "justification echoed verbatim"     'override-justification="regenerated lockfile only"' 0 -- --files package-lock.json --override scaffold --justification "regenerated lockfile only"
check "override w/o justification FATAL"  "roster=full-6"  2 -- --files package-lock.json --override scaffold
# rule-3: a recipe must never classify docs-3
check "recipe -> recipe roster"           "roster=recipe"  0 -- --files specs/recipes/SPEC-01-T1.md
# rule-5 + boundaries
check "docs only -> docs-3"               "roster=docs-3"  0 -- --files docs/adr/adr-1.md README.md
check "md with fences still docs-3"       "roster=docs-3"  0 -- --files docs/howto.md
# rule-6: design dimension — fires, and is additive to a code roster
check "css diff -> design=yes"            "design=yes"     0 -- --files styles/app.css
check "ts diff -> full-6 AND design=yes"  "design=yes"     0 -- --files src/app.ts
check "backend diff -> design=no"         "design=no"      0 -- --files src/server.py
check "design-dir image -> design=yes"    "design=yes"     0 -- --files docs/ui/design/mock.png
check "non-design image -> docs-3 design=no" "design=no"    0 -- --files docs/screenshot.png
# rule-7 + FATAL contract
check "empty file list -> full-6 exit 0"  "reason=rule-7-empty" 0 -- --files
OUT="$(bash "$RS" --base no-such-ref --head also-bogus 2>/dev/null)"; RC=$?
if [ "$RC" = 2 ] && printf '%s' "$OUT" | grep -qF "roster=full-6"; then
  PASS=$((PASS+1)); echo "PASS: unreadable ref -> exit 2 + full-6 label"
else FAIL=$((FAIL+1)); echo "FAIL: unreadable ref -> exit 2 + full-6 label (rc=$RC out=$OUT)"; fi
# the UI class is single-sourced: lib gone -> FATAL, never a silent design=no
T="$(mktemp -d)"; mkdir -p "$T/scripts" "$T/lib"
cp "$RS" "$T/scripts/roster-select.sh"      # lib deliberately NOT copied
OUT="$(bash "$T/scripts/roster-select.sh" --files styles/app.css 2>/dev/null)"; RC=$?
if [ "$RC" = 2 ] && printf '%s' "$OUT" | grep -qF "roster=full-6"; then
  PASS=$((PASS+1)); echo "PASS: missing ui-class lib -> FATAL 2, not silent design=no"
else FAIL=$((FAIL+1)); echo "FAIL: missing ui-class lib -> FATAL (rc=$RC out=$OUT)"; fi
cp "$HERE/../lib/ui-class.sh" "$T/lib/"     # control: with the lib the same copy classifies
OUT="$(bash "$T/scripts/roster-select.sh" --files styles/app.css 2>/dev/null)"; RC=$?
if [ "$RC" = 0 ] && printf '%s' "$OUT" | grep -qF "design=yes"; then
  PASS=$((PASS+1)); echo "PASS: lib present control leg classifies"
else FAIL=$((FAIL+1)); echo "FAIL: lib present control leg (rc=$RC out=$OUT)"; fi
rm -rf "$T"
# the additive overlay can only ADD sensitivity (fail-safe direction)
T="$(mktemp -d)"; mkdir -p "$T/.rigor"
echo '(^|/)billing/' > "$T/.rigor/roster-patterns.local"
OUT="$(CLAUDE_PROJECT_DIR="$T" bash "$RS" --files billing/rates.md 2>/dev/null)"
if printf '%s' "$OUT" | grep -qF "reason=rule-1"; then
  PASS=$((PASS+1)); echo "PASS: project overlay adds a sensitive class"
else FAIL=$((FAIL+1)); echo "FAIL: project overlay adds a sensitive class ($OUT)"; fi
rm -rf "$T"
# a BROKEN overlay pattern must FATAL, not silently fail to add its sensitivity
T="$(mktemp -d)"; mkdir -p "$T/.rigor"
printf '(^|/billing/\n' > "$T/.rigor/roster-patterns.local"   # unbalanced paren = invalid ERE
OUT="$(CLAUDE_PROJECT_DIR="$T" bash "$RS" --files billing/rates.md 2>/dev/null)"; RC=$?
if [ "$RC" = 2 ] && printf '%s' "$OUT" | grep -qF "roster=full-6"; then
  PASS=$((PASS+1)); echo "PASS: invalid overlay pattern -> FATAL, not silent no-match"
else FAIL=$((FAIL+1)); echo "FAIL: invalid overlay pattern -> FATAL (rc=$RC out=$OUT)"; fi
rm -rf "$T"
# HIGH-1: a justification that could forge a second verdict line is rejected
OUT="$(bash "$RS" --files package-lock.json --override scaffold --justification "$(printf 'x\nroster-select: roster=docs-3')" 2>/dev/null)"; RC=$?
if [ "$RC" = 2 ] && [ "$(printf '%s\n' "$OUT" | grep -c '^roster-select: ')" = 1 ]; then
  PASS=$((PASS+1)); echo "PASS: newline in justification -> FATAL, single verdict line"
else FAIL=$((FAIL+1)); echo "FAIL: newline injection (rc=$RC out=$OUT)"; fi
ERR="$(bash "$RS" --files package-lock.json --override scaffold --justification 'x" design=yes-FORGED' 2>&1 >/dev/null)"; RC=$?
if [ "$RC" = 2 ] && printf '%s' "$ERR" | grep -q "newlines or double quotes"; then
  PASS=$((PASS+1)); echo "PASS: quote in justification -> FATAL with the injection reason"
else FAIL=$((FAIL+1)); echo "FAIL: quote injection reason (rc=$RC err=$ERR)"; fi
# HIGH-2: uppercase extensions are still code
check "App.TS -> full-6 (case-insensitive)" "reason=rule-2" 0 -- --files src/App.TS
check "0001.SQL -> full-6"                "reason=rule-2"  0 -- --files db/0001.SQL
# MEDIUM: extensionless executables + secret material are sensitive
check "bin/deploy -> rule-1"              "reason=rule-1"  0 -- --files bin/deploy
check "server.pem -> rule-1"              "reason=rule-1"  0 -- --files certs/server.pem
check ".env.local -> rule-1"              "reason=rule-1"  0 -- --files .env.local
check "production.env -> rule-1"          "reason=rule-1"  0 -- --files config/production.env
# HIGH: a trailing value-flag must FATAL, never hang (executed 5s-kill repro pre-fix)
OUT="$(perl -e 'alarm 5; exec @ARGV' bash "$RS" --base 2>/dev/null)"; RC=$?
if [ "$RC" = 2 ]; then PASS=$((PASS+1)); echo "PASS: trailing --base -> FATAL, no hang"
else FAIL=$((FAIL+1)); echo "FAIL: trailing --base (rc=$RC — 142 means it HUNG)"; fi
# MED-HIGH: a code file renamed to a docs path stays in the change set (range mode).
# Deterministic base branch + run ONCE + assert reason=rule-2: rule-2 never appears in
# a FATAL line, so this pin cannot be satisfied by the exit-2 safe-default label (the
# earlier two-leg || form was vacuous — the first leg's FATAL full-6 always matched).
T="$(mktemp -d)"; (cd "$T" && git init -q -b rsbase && git commit -q --allow-empty -m base \
  && mkdir src && echo 'x=1' > src/guard.sh && git add -A && git commit -qm code \
  && git checkout -qb move && mkdir -p docs && git mv src/guard.sh docs/guard.md && git commit -qm rename)
OUT="$(cd "$T" && bash "$RS" --base rsbase --head move 2>/dev/null)"; RC=$?
if [ "$RC" = 0 ] && printf '%s' "$OUT" | grep -qF "reason=rule-2"; then
  PASS=$((PASS+1)); echo "PASS: code renamed to docs path still rule-2 full-6 (range mode)"
else FAIL=$((FAIL+1)); echo "FAIL: rename-away-from-code leaked (rc=$RC out=$OUT)"; fi
# and the pure-deletion leg of the same clause, range mode, same non-FATAL pin
(cd "$T" && git checkout -q rsbase -- 2>/dev/null; git -C "$T" checkout -q rsbase && git -C "$T" checkout -qb gone && git -C "$T" rm -q src/guard.sh && git -C "$T" commit -qm delete)
OUT="$(cd "$T" && bash "$RS" --base rsbase --head gone 2>/dev/null)"; RC=$?
if [ "$RC" = 0 ] && printf '%s' "$OUT" | grep -qF "reason=rule-2"; then
  PASS=$((PASS+1)); echo "PASS: deletion-only branch still rule-2 full-6 (range mode)"
else FAIL=$((FAIL+1)); echo "FAIL: deletion-only range leaked (rc=$RC out=$OUT)"; fi
rm -rf "$T"
# MED: SFCs and additional languages are code
check "App.vue -> full-6 AND design=yes"  "reason=rule-2"  0 -- --files web/App.vue
check "Main.scala -> full-6"              "reason=rule-2"  0 -- --files src/Main.scala
check "mod.cc -> full-6"                  "reason=rule-2"  0 -- --files kernel/mod.cc
# the output line is grep-anchored (the fixed prefix is the wiring contract)
check "grep-anchored prefix"              "roster-select: roster=" 0 -- --files README.md
# ruleset token present (the consumer skew detector)
check "ruleset token emitted"             "ruleset="       0 -- --files README.md
# git-range mode: HEAD~1..HEAD of this repo classifies (smoke; repo has commits)
OUT="$(cd "$HERE/../../../.." && bash "$RS" --base HEAD~1 --head HEAD 2>/dev/null)"; RC=$?
if [ "$RC" = 0 ] && printf '%s' "$OUT" | grep -qF "roster-select: roster="; then
  PASS=$((PASS+1)); echo "PASS: --base/--head range mode classifies"
else FAIL=$((FAIL+1)); echo "FAIL: --base/--head range mode (rc=$RC out=$OUT)"; fi

echo "----"
echo "roster-select test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = 0 ]
