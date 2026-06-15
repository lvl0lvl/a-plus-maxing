#!/usr/bin/env bash
# role-completeness-audit.sh — at-rest verification that every role profile
# (roles/<slug>/agent.md) carries the canonical 11-section structure the
# enforce-role-inlining.sh DISPATCH hook requires.
#
# WHY (surfaced S10, bead `bue`): the dispatch hook (INV-PROFILE-INLINING) fires
# only when an agent is actually dispatched with the role. consistency-audit
# checks that role REFERENCES resolve, not that each profile is structurally
# complete. So a role missing a canonical section — e.g. game-designer's absent
# operational slot (bead `0c8`) — ships silently and only fails at dispatch time.
# This audit is the AT-REST twin of the dispatch hook: it catches the broken
# profile in the repo, before anything tries to dispatch it.
#
# Required structure (mirrors enforce-role-inlining.sh EXACTLY):
#   10 fixed sections + 1 operational slot (## Modes | ## Audit Protocol | ## Task Routing).
#
# Exit: 0 PASS / 1 FAIL (a profile missing a section) / 2 FATAL (bad args / no roles).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_TAG="role-completeness-audit"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

LIB=""
while [ $# -gt 0 ]; do
  case "$1" in
    --lib) LIB="${2:-}"; shift 2 ;;
    --lib=*) LIB="${1#--lib=}"; shift ;;
    *) emit "FATAL: unknown arg: $1"; exit 2 ;;
  esac
done
[ -n "$LIB" ] || { emit "FATAL: --lib <library-root> is required"; exit 2; }
[ -d "$LIB/roles" ] || { emit "FATAL: no roles/ dir under $LIB"; exit 2; }

# The 10 fixed canonical sections (verbatim from enforce-role-inlining.sh).
REQUIRED=(
  "## Identity" "## Core Rules" "## Role Boundaries" "## Ask vs Proceed"
  "## Loop-Breaking" "## Tools" "## Communication" "## Context Loading"
  "## Anti-Patterns" "## Negative Examples"
)
# The 9th operational slot varies by role.
SLOTS=( "## Modes" "## Audit Protocol" "## Task Routing" )

found_any=0
for prof in "$LIB"/roles/*/agent.md; do
  [ -f "$prof" ] || continue
  found_any=1
  slug="$(basename "$(dirname "$prof")")"
  missing=""
  for sec in "${REQUIRED[@]}"; do
    grep -qF "$sec" "$prof" || missing="$missing '$sec'"
  done
  slot_ok=0
  for slot in "${SLOTS[@]}"; do
    grep -qF "$slot" "$prof" && { slot_ok=1; break; }
  done
  [ "$slot_ok" -eq 1 ] || missing="$missing '## Modes (or ## Audit Protocol / ## Task Routing)'"
  if [ -n "$missing" ]; then
    fail "role '$slug' incomplete — missing:$missing — would be DENIED by enforce-role-inlining on dispatch"
  else
    emit "role '$slug': complete (11 sections)"
  fi
done

[ "$found_any" -eq 1 ] || { emit "FATAL: no roles/*/agent.md profiles found under $LIB"; exit 2; }
verdict
