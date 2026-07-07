#!/usr/bin/env bash
# tests/test-version-bump-audit.sh — F-007 negative test for scripts/version-bump-audit.sh
# (bead skills_library-bd1 — the VERSION forward guard).
#
# Property: toolkit content must never move silently. CHECK 1 FAILs on a watched
# path committed after the last VERSION-touching commit; CHECK 2 FAILs on a dirty
# watched path while VERSION is clean (untracked new files included — the #97
# class). FATAL when the history cannot be read. All cases run against a
# THROWAWAY git repo via RIGOR_VERSION_FILE / RIGOR_BUMP_WATCH — never this repo.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/version-bump-audit.sh"

command -v git >/dev/null 2>&1 || { echo "[SKIP] git not present — cannot exercise the guard" >&2; exit 0; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
REPO="$WORK/repo"
mkdir -p "$REPO/rig/toolkit/scripts"
git -C "$REPO" init -q
git -C "$REPO" config user.email t@t; git -C "$REPO" config user.name t

VF="$REPO/rig/VERSION"
TK="$REPO/rig/toolkit"
CL="$REPO/rig/CHANGELOG.md"   # CHECK 3 default: CHANGELOG.md next to VERSION
echo "1.0.0" > "$VF"
printf '# changelog\n\n## 1.0.0 (t) — initial\n' > "$CL"
echo "echo hi" > "$TK/scripts/a.sh"
git -C "$REPO" add -A && git -C "$REPO" commit -qm "bump 1.0.0 with toolkit"

run_audit() {
  RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$TK" bash "$AUDIT"
}

echo "== version-bump-audit =="

# Clean state: last bump commit covers everything → PASS (0).
expect_exit 0 run_audit

# CHECK 1: a toolkit change COMMITTED after the bump, no VERSION touch → FAIL (1).
echo "echo changed" > "$TK/scripts/a.sh"
git -C "$REPO" commit -qam "toolkit change, silent"
expect_exit 1 run_audit

# Core F-007 pair on the same repo state: bumping VERSION cures it (good=0),
# the silent state above is the guard firing (bad!=0).
assert_red_when_guard_removed \
  "cd '$REPO' && echo 1.1.0 > '$VF' && printf '## 1.1.0 (t)\n' >> '$CL' && git commit -qam 'bump 1.1.0' && RIGOR_VERSION_FILE='$VF' RIGOR_BUMP_WATCH='$TK' bash '$AUDIT'" \
  "cd '$REPO' && echo 'echo more' >> '$TK/scripts/a.sh' && git commit -qam 'another silent toolkit change' && RIGOR_VERSION_FILE='$VF' RIGOR_BUMP_WATCH='$TK' bash '$AUDIT'"

# Cure the silent commit the bad-arm just made → PASS again.
echo "1.2.0" > "$VF"; printf '## 1.2.0 (t)\n' >> "$CL"
git -C "$REPO" commit -qam "bump 1.2.0"
expect_exit 0 run_audit

# CHECK 2: dirty toolkit file, VERSION clean → FAIL (1).
echo "echo dirty" >> "$TK/scripts/a.sh"
expect_exit 1 run_audit

# CHECK 2 satisfied: VERSION dirty alongside → PASS (0) (bump in progress).
echo "1.3.0-wip" > "$VF"
expect_exit 0 run_audit
git -C "$REPO" checkout -q -- .   # reset both

# CHECK 2: UNTRACKED new file under toolkit (the #97 class), VERSION clean → FAIL (1).
echo "new gate" > "$TK/scripts/new-gate.sh"
expect_exit 1 run_audit
rm -f "$TK/scripts/new-gate.sh"

# A change OUTSIDE the watched paths needs no bump → PASS (0).
echo "docs" > "$REPO/rig/notes.md"
git -C "$REPO" add -A && git -C "$REPO" commit -qm "non-toolkit change"
expect_exit 0 run_audit

# Colon-separated multi-path watch: widening the watch to rig/ makes the SAME
# state FAIL (notes.md landed after the last bump) — pins the list split.
expect_exit 1 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$TK:$REPO/rig" bash "$AUDIT"

# FATALs: version file absent / untracked / not a repo → 2 each.
expect_exit 2 env RIGOR_VERSION_FILE="$WORK/nope/VERSION" RIGOR_BUMP_WATCH="$TK" bash "$AUDIT"

echo "9.9.9" > "$WORK/untracked-VERSION"
mkdir -p "$WORK/plain"
expect_exit 2 env RIGOR_VERSION_FILE="$WORK/untracked-VERSION" RIGOR_BUMP_WATCH="$WORK/plain" bash "$AUDIT"

UNTRACKED_VF="$REPO/rig/VERSION-new"
echo "0.0.1" > "$UNTRACKED_VF"
expect_exit 2 env RIGOR_VERSION_FILE="$UNTRACKED_VF" RIGOR_BUMP_WATCH="$TK" bash "$AUDIT"
# Anchor the tracked-guard's OWN message (review E9): without it the same input
# still exits 2 via the downstream no-commit FATAL, so exit code alone cannot
# isolate this guard — the message can. (audit-helpers emit() writes to STDOUT,
# so this is a stdout anchor, not assert_stderr_contains.)
TESTS_RUN=$((TESTS_RUN + 1))
GUARD_OUT="$(RIGOR_VERSION_FILE="$UNTRACKED_VF" RIGOR_BUMP_WATCH="$TK" bash "$AUDIT" 2>&1)"
if printf '%s' "$GUARD_OUT" | grep -q "not tracked by git"; then
  echo "[PASS] untracked-VERSION FATAL names the tracked-guard"
else
  echo "[FAIL] untracked-VERSION FATAL lacked 'not tracked by git' (got: $GUARD_OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
rm -f "$UNTRACKED_VF"

# Vacuous watch list (review E1): colon-only / all-empty RIGOR_BUMP_WATCH must
# NOT pass — zero checks ran. Fail-closed FATAL (2); allowed-skip downgrades.
expect_exit 2 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH=":" bash "$AUDIT"
expect_exit 2 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="::" bash "$AUDIT"

# Watch entry git cannot see (review E2): a wrong-case entry exists on a
# case-insensitive FS but matches no pathspec (on a case-sensitive FS the same
# entry is absent) — BOTH paths must land on skipped()->FATAL (2), never a
# vacuous PASS over real drift.
echo "echo drift" >> "$TK/scripts/a.sh"
git -C "$REPO" commit -qam "silent drift for case test"
UPPER_TK="$(dirname "$TK")/TOOLKIT"
expect_exit 2 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$UPPER_TK" bash "$AUDIT"
echo "1.4.0" > "$VF"; printf '## 1.4.0 (t)\n' >> "$CL"
git -C "$REPO" commit -qam "bump 1.4.0"   # cure the drift

# Watched path absent → fail-closed FATAL via skipped() (2), unless allowed.
expect_exit 2 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$REPO/rig/no-such-dir" bash "$AUDIT"
expect_exit 0 env AUDIT_ALLOW_SKIP=1 RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$REPO/rig/no-such-dir" bash "$AUDIT"

# ═══ CHECK 3 — CHANGELOG completeness (bead skills_library-azt) ═══════════════
# A committed VERSION with no matching '## <version>' heading FAILs (the 1.12.0
# field case); adding the row cures it. The dirty-VERSION deferral is pinned
# above (the 1.3.0-wip case passed with no 1.3.0-wip row).
echo "9.0.0" > "$VF"; git -C "$REPO" commit -qam "bump 9.0.0 without a row"
expect_exit 1 run_audit
# Message anchor: isolate CHECK 3's own FAIL (exit 1 alone could be a watch FAIL).
TESTS_RUN=$((TESTS_RUN + 1))
C3_OUT="$(run_audit 2>&1)"
if printf '%s' "$C3_OUT" | grep -q "no '## 9.0.0' heading"; then
  echo "[PASS] CHECK 3 FAIL names the missing changelog row"
else
  echo "[FAIL] CHECK 3 output lacked the missing-row message (got: $C3_OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
# Guard-fires pair: the row landing cures it (good=0); dropping the row (a
# doc-only commit — outside the watch, so only CHECK 3 can catch it) FAILs.
assert_red_when_guard_removed \
  "cd '$REPO' && printf '## 9.0.0 (t)\n' >> '$CL' && git commit -qam 'row 9.0.0' && RIGOR_VERSION_FILE='$VF' RIGOR_BUMP_WATCH='$TK' bash '$AUDIT'" \
  "cd '$REPO' && sed -i.bak '/## 9.0.0/d' '$CL' && rm -f '$CL.bak' && git commit -qam 'drop row 9.0.0' && RIGOR_VERSION_FILE='$VF' RIGOR_BUMP_WATCH='$TK' bash '$AUDIT'"
# Restore the row → PASS again.
printf '## 9.0.0 (t)\n' >> "$CL"; git -C "$REPO" commit -qam "restore row 9.0.0"
expect_exit 0 run_audit

# Changelog absent entirely → FAIL (1), fail-closed (the version moved, no rows).
expect_exit 1 env RIGOR_VERSION_FILE="$VF" RIGOR_BUMP_WATCH="$TK" \
  RIGOR_CHANGELOG_FILE="$REPO/rig/no-such-changelog.md" bash "$AUDIT"

# Heading-boundary discipline: a '## 9.0.0' row must NOT satisfy VERSION 9.0
# (prefix) — the boundary char excludes digits AND dots.
echo "9.0" > "$VF"; git -C "$REPO" commit -qam "bump 9.0 (prefix probe)"
expect_exit 1 run_audit
echo "9.0.0" > "$VF"; git -C "$REPO" commit -qam "restore 9.0.0"
expect_exit 0 run_audit

# review BUG-2 (fail-open): a PRERELEASE heading must NOT satisfy a FINAL VERSION.
# VERSION 8.0.0 with only '## 8.0.0-rc.1' present → FAIL (the '-' must not read as
# the trailing boundary). The whitespace/EOL boundary still admits the real
# space-suffixed rows above (all '## X.Y.Z (t)'), so this is a pure tightening.
echo "8.0.0" > "$VF"; printf '## 8.0.0-rc.1 (t)\n' >> "$CL"
git -C "$REPO" commit -qam "bump 8.0.0 with only a prerelease row"
expect_exit 1 run_audit
TESTS_RUN=$((TESTS_RUN + 1))
PRE_OUT="$(run_audit 2>&1)"
if printf '%s' "$PRE_OUT" | grep -q "no '## 8.0.0' heading"; then
  echo "[PASS] prerelease-only row does not satisfy a final VERSION (BUG-2)"
else
  echo "[FAIL] prerelease row wrongly satisfied final VERSION (got: $PRE_OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
# Adding the FINAL row cures it; a prerelease VERSION still matches its own row.
printf '## 8.0.0 (t)\n' >> "$CL"; git -C "$REPO" commit -qam "row 8.0.0"
expect_exit 0 run_audit
echo "8.1.0-rc.1" > "$VF"; printf '## 8.1.0-rc.1 (t)\n' >> "$CL"
git -C "$REPO" commit -qam "prerelease VERSION with matching row"
expect_exit 0 run_audit

# review SHOULD-FIX-2: EXPLICIT dirty-VERSION deferral guard (independent of the
# CHECK-2 1.3.0-wip case). A dirty VERSION with NO changelog row must PASS —
# CHECK 3 is deferred to the committed state while a bump is in progress.
echo "9.0.0" > "$VF"; git -C "$REPO" commit -qam "clean baseline for deferral probe"
printf '## 9.0.0 (t)\n' >> "$CL"; git -C "$REPO" commit -qam "row 9.0.0 for deferral baseline"
expect_exit 0 run_audit                     # committed + row present → PASS
echo "9.5.0-wip" > "$VF"                     # dirty bump, NO 9.5.0-wip row
expect_exit 0 run_audit                      # deferred → PASS (not a false FAIL)
git -C "$REPO" checkout -q -- "$VF"          # reset the dirty VERSION

# review SHOULD-FIX-3: empty VERSION line 1 → FAIL (no version to check).
printf '\n1.0.0\n' > "$VF"; git -C "$REPO" commit -qam "blank VERSION line 1"
expect_exit 1 run_audit
TESTS_RUN=$((TESTS_RUN + 1))
EMPTY_OUT="$(run_audit 2>&1)"
if printf '%s' "$EMPTY_OUT" | grep -q "VERSION line 1 is empty"; then
  echo "[PASS] empty VERSION line 1 FAILs with its own message"
else
  echo "[FAIL] empty VERSION line 1 lacked the message (got: $EMPTY_OUT)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

test_summary
