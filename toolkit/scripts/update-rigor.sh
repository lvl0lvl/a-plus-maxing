#!/usr/bin/env bash
# toolkit/scripts/update-rigor.sh — the runnable Discipline 11 PULL (bead: update-rigor).
#
# Discipline 11 documents the pull as prose: "a project pins rigor_version; at a
# periodic boundary the orchestrator diffs the pin against the framework VERSION,
# reads the CHANGELOG delta, and pulls it — re-running toolkit/tests/run-all-tests.sh
# as the acceptance gate (a pulled script that cannot prove it FAILs on bad input is
# not adopted, F-007)." A consuming project holds a COPY of the toolkit (fresh-start
# copies, it does not symlink — symlinks break on clone), so the copy goes stale and
# cannot update itself. This script makes the pull a TOOL, auto-gated:
#
#   1. Read the project's pinned `rigor_version:` (from its static-instructions file).
#   2. Read the central library's framework VERSION (line 1). If pinned >= latest,
#      report up-to-date and exit 0 (no-op).
#   3. Print the CHANGELOG delta (the entries newer than the pin).
#   4. BACK UP the project's current toolkit/, then COPY the central toolkit/ over it.
#   5. Run the project's toolkit/tests/run-all-tests.sh — the ACCEPTANCE GATE. RED →
#      ROLL BACK (restore the backup), leave the pin unchanged, exit 1 (FATAL: a
#      failing toolkit is not adopted). GREEN → keep it.
#   6. On GREEN, update the pin to the latest version and report new wiring the
#      project must apply (e.g. a new hook the delta introduced).
#
# FAIL-CLOSED (F-008): a pull that cannot be verified (tests RED, or the test runner
# is absent/unrunnable) is ROLLED BACK, not adopted. "Couldn't verify the pull" never
# reads as "pulled clean." The pre-update state is always restored on any failure.
#
# CONFIG (args / env):
#   --lib <path>       central skills_library root (has frameworks/rigor/VERSION).
#                      default: $SKILLS_LIBRARY_DIR, else ~/.claude/skills_library.
#   --project <path>   the consuming project root (has toolkit/ + the pin file).
#                      default: $CLAUDE_PROJECT_DIR, else cwd.
#   --pin-file <path>  the static-instructions file carrying `rigor_version:`.
#                      default: <project>/CLAUDE.md.
#   --toolkit <rel>    the project's toolkit dir, relative to --project. default: toolkit.
#   --dry-run          do steps 1-3 (diff + delta) but make NO changes; exit 0.
#
# EXIT: 0 up-to-date OR updated-and-green OR dry-run; 1 pull rolled back (any adopt-time
#       failure: tests RED/unrunnable, copy-from-central failed, or pin write failed); 2
#       FATAL (bad config: no lib/VERSION/pin/contained-toolkit, OR a rollback that could
#       not restore — the backup path is reported).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_TAG="update-rigor"
# audit-helpers gives emit(); source it if present, else a minimal emit.
if [ -f "$SCRIPT_DIR/../lib/audit-helpers.sh" ]; then
  # shellcheck disable=SC1091
  . "$SCRIPT_DIR/../lib/audit-helpers.sh"
else
  emit() { echo "[$AUDIT_TAG] $*"; }
fi
fatal() { emit "FATAL: $*"; exit 2; }

# ── args ──────────────────────────────────────────────────────────────────────
LIB="${SKILLS_LIBRARY_DIR:-$HOME/.claude/skills_library}"
PROJECT="${CLAUDE_PROJECT_DIR:-$PWD}"
PIN_FILE=""
TOOLKIT_REL="toolkit"
DRY_RUN=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --lib)      LIB="$2"; shift 2 ;;
    --project)  PROJECT="$2"; shift 2 ;;
    --pin-file) PIN_FILE="$2"; shift 2 ;;
    --toolkit)  TOOLKIT_REL="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    *) fatal "unknown arg: $1 (usage: update-rigor.sh [--lib P] [--project P] [--pin-file F] [--toolkit REL] [--dry-run])" ;;
  esac
done
[ -z "$PIN_FILE" ] && PIN_FILE="$PROJECT/CLAUDE.md"

# ── resolve central library ───────────────────────────────────────────────────
CENTRAL_VERSION="$LIB/frameworks/rigor/VERSION"
CENTRAL_TOOLKIT="$LIB/frameworks/rigor/toolkit"
CENTRAL_CHANGELOG="$LIB/frameworks/rigor/CHANGELOG.md"
[ -d "$LIB" ]              || fatal "central library not found: $LIB (set --lib or \$SKILLS_LIBRARY_DIR)"
[ -f "$CENTRAL_VERSION" ]  || fatal "central VERSION absent: $CENTRAL_VERSION"
[ -d "$CENTRAL_TOOLKIT" ]  || fatal "central toolkit absent: $CENTRAL_TOOLKIT"

# ── resolve project ───────────────────────────────────────────────────────────
PROJECT_TOOLKIT="$PROJECT/$TOOLKIT_REL"
[ -f "$PIN_FILE" ]         || fatal "pin file absent: $PIN_FILE (needs a 'rigor_version:' line)"
[ -d "$PROJECT_TOOLKIT" ]  || fatal "project toolkit absent: $PROJECT_TOOLKIT (is this a rigor-adopted project?)"

# CONTAINMENT (security review): a later `rm -rf "$PROJECT_TOOLKIT"` is destructive, so
# before we trust that path it MUST be (a) a real directory strictly UNDER $PROJECT —
# canonicalized, so a `../`-bearing --toolkit cannot point rm at an outside/sibling dir —
# and (b) actually a rigor toolkit (carries tests/run-all-tests.sh). Either failing is
# FATAL: we delete nothing we cannot prove is the project's own toolkit (fail-closed).
PROJECT_ABS="$(cd "$PROJECT" 2>/dev/null && pwd -P)" || fatal "cannot resolve --project: $PROJECT"
TOOLKIT_ABS="$(cd "$PROJECT_TOOLKIT" 2>/dev/null && pwd -P)" || fatal "cannot resolve toolkit dir: $PROJECT_TOOLKIT"
case "$TOOLKIT_ABS/" in
  "$PROJECT_ABS"/*/) : ;;   # strictly under the project root
  *) fatal "refusing to operate on a toolkit outside the project: '$TOOLKIT_ABS' is not under '$PROJECT_ABS' (a '../' --toolkit is rejected — nothing is deleted)" ;;
esac
[ -f "$TOOLKIT_ABS/tests/run-all-tests.sh" ] \
  || fatal "'$TOOLKIT_ABS' is not a rigor toolkit (no tests/run-all-tests.sh) — refusing to rm -rf it"
# Operate on the canonicalized, contained path from here on.
PROJECT_TOOLKIT="$TOOLKIT_ABS"

# ── read versions ─────────────────────────────────────────────────────────────
LATEST="$(sed -n '1p' "$CENTRAL_VERSION" | tr -d '[:space:]')"
case "$LATEST" in ''|*[!0-9.]*) fatal "central VERSION line 1 is not a semver: '$LATEST'";; esac

# Pin: the FIRST LINE whose content begins `rigor_version: X.Y.Z` (case-tolerant).
# ANCHORED to line-start (review: an un-anchored match clobbered inline prose like
# "…adopted rigor_version: 1.0.0…" and the read/write disagreed on which line was the
# pin). The read and the write below use the SAME anchor so they agree on the one line.
PIN_RE='^[[:space:]]*[Rr]igor_[Vv]ersion[[:space:]]*:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+'
PINNED="$(grep -Eo "$PIN_RE" "$PIN_FILE" | head -1 | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
[ -n "$PINNED" ] || fatal "no 'rigor_version: X.Y.Z' pin line found in $PIN_FILE (must start the line)"

emit "pinned rigor_version: $PINNED ; central latest: $LATEST"

# ── semver compare (portable, no sort -V dependency) ──────────────────────────
# ver_ge A B → 0 if A >= B. Splits on dots, compares MAJOR.MINOR.PATCH numerically.
ver_ge() {
  local a="$1" b="$2" IFS=. ; local -a A B
  read -r -a A <<EOF
$a
EOF
  read -r -a B <<EOF
$b
EOF
  local i x y
  for i in 0 1 2; do
    x="${A[$i]:-0}"; y="${B[$i]:-0}"
    [ "$x" -gt "$y" ] && return 0
    [ "$x" -lt "$y" ] && return 1
  done
  return 0   # equal
}

if ver_ge "$PINNED" "$LATEST"; then
  emit "up to date (pinned $PINNED >= latest $LATEST) — nothing to pull."
  exit 0
fi

# ── the CHANGELOG delta (entries newer than the pin) ──────────────────────────
emit "── CHANGELOG delta ($PINNED → $LATEST) ──"
if [ -f "$CENTRAL_CHANGELOG" ]; then
  # Print from the top of the changelog down to (but not including) the pinned
  # version's heading — i.e. everything that landed after the pin. If the pin has NO
  # heading in the changelog, don't dump the WHOLE file (review): say so and show only
  # the headings, so the operator sees the version span without a wall of text.
  if grep -Eq "^## .*$(printf '%s' "$PINNED" | sed 's/\./\\./g')" "$CENTRAL_CHANGELOG"; then
    awk -v pin="$PINNED" '
      /^## / {
        if (match($0, /[0-9]+\.[0-9]+\.[0-9]+/)) {
          v = substr($0, RSTART, RLENGTH)
          if (v == pin) { exit }
        }
      }
      { print }
    ' "$CENTRAL_CHANGELOG"
  else
    emit "(pinned $PINNED has no heading in the central CHANGELOG — showing version headings only, newest first:)"
    grep -E '^## ' "$CENTRAL_CHANGELOG"
  fi
else
  emit "(no CHANGELOG.md in the central library — skipping delta)"
fi
emit "── end delta ──"

if [ "$DRY_RUN" = "1" ]; then
  emit "dry-run: no changes made. Re-run without --dry-run to pull + gate."
  exit 0
fi

# ── the gated pull: back up → copy → test → keep|rollback ─────────────────────
BACKUP="$(mktemp -d)" || fatal "cannot create backup dir"
DONE=0   # set to 1 only after the pin bump succeeds; gates EXIT cleanup vs restore.
# cleanup fires on EXIT for ANY reason. If we did NOT finish (a signal, an unexpected
# exit) while the destructive window was open, RESTORE first, then remove the backup —
# so a Ctrl-C mid-pull cannot leave a half-updated toolkit with the backup already gone
# (bug-hunt: the old EXIT-only trap deleted the sole backup on signal, losing rollback).
cleanup() {
  if [ "$DONE" = "0" ] && [ -n "${BACKUP:-}" ] && [ -d "$BACKUP/toolkit.bak" ] && [ -n "${PROJECT_TOOLKIT:-}" ]; then
    emit "interrupted before completion — restoring the pre-update toolkit from backup."
    rm -rf "$PROJECT_TOOLKIT" 2>/dev/null
    cp -R "$BACKUP/toolkit.bak" "$PROJECT_TOOLKIT" 2>/dev/null
  fi
  [ -n "${BACKUP:-}" ] && rm -rf "$BACKUP"
}
# EXIT covers normal exits; INT/TERM/HUP a mid-pull interrupt (the multi-second gate run
# is the widest window). All route through cleanup's restore-if-not-done path.
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

emit "backing up current toolkit → $BACKUP"
# Copy the CONTENTS (so restore overwrites cleanly). cp -R of the dir itself.
cp -R "$PROJECT_TOOLKIT" "$BACKUP/toolkit.bak" || fatal "backup copy failed"

restore_and_fail() {
  emit "ROLLING BACK — restoring the pre-update toolkit (the pull is NOT adopted)."
  rm -rf "$PROJECT_TOOLKIT"
  # The restore itself is the fail-closed path the header promises — if it cannot
  # complete, say so LOUDLY and point at the backup (never a silent "clean rollback").
  if ! cp -R "$BACKUP/toolkit.bak" "$PROJECT_TOOLKIT" 2>/dev/null; then
    DONE=1   # don't let EXIT cleanup re-try / then delete the backup out from under the operator
    emit "FATAL: ROLLBACK FAILED to restore $PROJECT_TOOLKIT — the pre-update toolkit is preserved at $BACKUP/toolkit.bak; restore it by hand. (pull cause: $1)"
    trap - EXIT
    exit 2
  fi
  emit "RESULT: FAIL (pull rolled back — $1)"
  exit 1
}

emit "copying central toolkit ($LATEST) → $PROJECT_TOOLKIT"
# Replace the project toolkit with the central one wholesale (a copy is authoritative;
# a merge would leave retired files behind). Then run the acceptance gate.
rm -rf "$PROJECT_TOOLKIT"
cp -R "$CENTRAL_TOOLKIT" "$PROJECT_TOOLKIT" || restore_and_fail "copy from central failed"

RUNNER="$PROJECT_TOOLKIT/tests/run-all-tests.sh"
[ -f "$RUNNER" ] || restore_and_fail "the pulled toolkit has no tests/run-all-tests.sh — cannot verify"

emit "running the acceptance gate: $RUNNER"
if bash "$RUNNER" >/dev/null 2>&1; then
  emit "acceptance gate GREEN — the pulled toolkit passes its own suite."
else
  restore_and_fail "acceptance gate RED (tests failed on the pulled toolkit)"
fi

# ── update the pin ────────────────────────────────────────────────────────────
# Rewrite the version on the FIRST pin line only (awk, not sed) — case-tolerant,
# anchored to the SAME line-start pattern the read used, so inline prose mentions of
# 'rigor_version' are never touched and read/write agree on the one line (review:
# the old un-anchored sed rewrote EVERY match incl. prose, and was case-sensitive).
TMP_PIN="$(mktemp)" || restore_and_fail "cannot stage pin update"
awk -v latest="$LATEST" '
  !done && /^[[:space:]]*[Rr]igor_[Vv]ersion[[:space:]]*:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+/ {
    sub(/[0-9]+\.[0-9]+\.[0-9]+/, latest); done=1
  }
  { print }
' "$PIN_FILE" > "$TMP_PIN" && mv "$TMP_PIN" "$PIN_FILE" \
  || restore_and_fail "pin update failed (could not write $PIN_FILE)"
# Post-write verification: PASS must imply the pin ACTUALLY moved. If the rewrite was a
# no-op (unexpected pin shape), roll back rather than report a bump that did not happen
# (security: a case-mismatched pin silently no-op'd yet reported PASS).
grep -Eq "^[[:space:]]*[Rr]igor_[Vv]ersion[[:space:]]*:[[:space:]]*$(printf '%s' "$LATEST" | sed 's/\./\\./g')([[:space:]]|$)" "$PIN_FILE" \
  || restore_and_fail "pin did not update to $LATEST in $PIN_FILE (unexpected pin shape) — rolled back rather than report a false bump"

# The update is COMPLETE and adopted. Past this point the EXIT/signal cleanup must NOT
# roll back (a signal during the final report should keep the finished update).
DONE=1

emit "pin updated: rigor_version $PINNED → $LATEST in $PIN_FILE"

# ── report new wiring the delta may require ───────────────────────────────────
# A pulled version can introduce a hook/gate the project must WIRE (copying the file
# is not the same as activating it). Surface any new hook in the delta so the operator
# wires it — the copy alone never changes .claude/settings.json.
NEW_HOOKS="$(awk -v pin="$PINNED" '
  /^## / { if (match($0,/[0-9]+\.[0-9]+\.[0-9]+/)) { if (substr($0,RSTART,RLENGTH)==pin) exit } }
  /hooks\/[a-z0-9-]+\.sh/ { while (match($0,/hooks\/[a-z0-9-]+\.sh/)) { print substr($0,RSTART,RLENGTH); $0=substr($0,RSTART+RLENGTH) } }
' "$CENTRAL_CHANGELOG" 2>/dev/null | sort -u)"
if [ -n "$NEW_HOOKS" ]; then
  emit "NOTE: the delta references these hooks — verify each is WIRED in .claude/settings.json (copying the file does not activate it):"
  printf '%s\n' "$NEW_HOOKS" | while IFS= read -r h; do [ -n "$h" ] && emit "  - $h"; done
  emit "See the toolkit README wiring section (e.g. the merge gate needs its hook + a Bash(gh pr merge:*) allow rule)."
fi

emit "RESULT: PASS (updated to $LATEST, acceptance gate GREEN, pin bumped)"
exit 0
