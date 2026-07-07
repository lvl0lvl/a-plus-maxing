#!/usr/bin/env bash
# pf-severity-audit.sh — rigor framework canonical audit (ADR-0004 sub-check G5).
#
# ENFORCES: PF severity-monotonicity / no-silent-softening (giq.4.2).
#   A PF entry's severity must NOT be silently DOWNGRADED between the prior git
#   revision and the current working copy. Any downgrade FAILs UNLESS the entry
#   carries an explicit, structured `re-grade:` exception marker — a documented,
#   adjacent line declaring the re-classification. This is the property, not a
#   signal: it compares the ACTUAL severity values across two revisions and a
#   marker's presence, never merely that a `severity:` field exists (F-007).
#
# CADENCE — PER-HARVEST / PRE-RELEASE, **NOT** in the per-close roster.
#   Per ADR-0004: G5 carries a git-history input dependency (it needs the PF log's
#   prior revision) and a residual false-positive boundary (a forgotten marker on
#   a legitimate re-grade). Both make it unfit for the critical close path, where a
#   non-git PF log would FATAL-block every session close. G5 therefore runs on the
#   per-harvest/pre-release cadence (alongside harvest-gate.sh / parity), where git
#   history is reliably present. It is deliberately ABSENT from close-audit.sh's
#   DEFAULT_ROSTER and MUST NOT be added there.
#
# SEVERITY ORDER (descending): CRITICAL > HIGH > MEDIUM > LOW > COSMETIC.
#   A DOWNGRADE is any move from a higher to a lower rank (e.g. HIGH→LOW). An
#   UPGRADE (LOW→HIGH) or no-change is allowed without a marker. Unknown severity
#   tokens are compared by exact string only (no rank), so a typo cannot be silently
#   treated as a downgrade — but a change between two unknowns still requires care
#   and is reported, not silently passed.
#
# PRIOR REVISION:
#   Default: `git show HEAD:<path-relative-to-its-repo>` for the PF log. If the PF
#   log is NOT git-tracked (not in a repo, or no committed HEAD version), the check
#   CANNOT run → skipped() → FATAL (exit 2, fail-closed F-008) unless AUDIT_ALLOW_SKIP=1.
#   Testability seam: `--prior <file>` supplies the prior revision explicitly,
#   bypassing git (used by the negative test for some cases; the default git path
#   is still exercised so the dependency itself is covered).
#
# EXIT SEMANTICS (via lib/audit-helpers.sh): 0 PASS / 1 FAIL / 2 FATAL.
#
# USAGE:
#   pf-severity-audit.sh [--pf-log PATH] [--prior FILE] [PATH]
#   PF_LOG env var supplies the default PF-log path.
# Defaults: PF log = ${PF_LOG:-./memory/process-failures.md}.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="pf-severity-audit"

PF_LOG="${PF_LOG:-./memory/process-failures.md}"
PRIOR_FILE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --pf-log)
      PF_LOG="${2:-}"
      [ -n "$PF_LOG" ] || { emit "FATAL: --pf-log requires a path"; exit 2; }
      shift 2 ;;
    --pf-log=*) PF_LOG="${1#--pf-log=}"; shift ;;
    --prior)
      PRIOR_FILE="${2:-}"
      [ -n "$PRIOR_FILE" ] || { emit "FATAL: --prior requires a path"; exit 2; }
      shift 2 ;;
    --prior=*) PRIOR_FILE="${1#--prior=}"; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) emit "FATAL: unknown flag: $1"; exit 2 ;;
    *) PF_LOG="$1"; shift ;;
  esac
done

if [ ! -f "$PF_LOG" ]; then
  emit "FATAL: PF log not found: $PF_LOG (set --pf-log or PF_LOG)"
  exit 2
fi

# Severity rank: higher number = more severe. Unknown → empty (no rank).
sev_rank() {
  case "$(printf '%s' "$1" | tr 'a-z' 'A-Z')" in
    CRITICAL) echo 5 ;;
    HIGH)     echo 4 ;;
    MEDIUM|MED) echo 3 ;;
    LOW)      echo 2 ;;
    COSMETIC|TRIVIAL) echo 1 ;;
    *)        echo "" ;;
  esac
}

# Parse "ID<TAB>SEVERITY<TAB>HAS_REGRADE" rows from a PF-log file's content.
# An entry starts at a `## ... PF-<id>...` header; severity is the first
# `severity: X` line within the entry; a `re-grade:` line anywhere in the entry
# sets HAS_REGRADE=1. The entry id is the first PF-token on the header line.
parse_entries() {
  awk '
    function flush() {
      if (id != "") printf "%s\t%s\t%s\n", id, sev, regrade
    }
    /^##[[:space:]]/ {
      flush()
      id=""; sev=""; regrade="0"
      line=$0
      if (match(line, /PF-[A-Za-z0-9._-]+/)) {
        id=substr(line, RSTART, RLENGTH)
      } else {
        # Fall back to the whole trimmed header as the entry key.
        sub(/^##[[:space:]]*/, "", line); id=line
      }
      next
    }
    {
      l=tolower($0)
      if (sev=="" && l ~ /^[[:space:]]*severity:[[:space:]]*/) {
        s=$0
        sub(/^[[:space:]]*[Ss][Ee][Vv][Ee][Rr][Ii][Tt][Yy]:[[:space:]]*/, "", s)
        sub(/[[:space:]].*$/, "", s)
        sev=s
      }
      if (l ~ /^[[:space:]]*re-grade:[[:space:]]*[^[:space:]]/) {
        regrade="1"
      }
    }
    END { flush() }
  '
}

# --- Acquire the prior revision --------------------------------------------
PRIOR_CONTENT=""
if [ -n "$PRIOR_FILE" ]; then
  if [ ! -f "$PRIOR_FILE" ]; then
    emit "FATAL: --prior file not found: $PRIOR_FILE"
    exit 2
  fi
  PRIOR_CONTENT="$(cat "$PRIOR_FILE")"
  emit "comparing $PF_LOG against explicit prior: $PRIOR_FILE"
else
  # Resolve the PF log's repo and its path within that repo.
  PF_DIR="$(cd "$(dirname "$PF_LOG")" && pwd)"
  PF_BASE="$(basename "$PF_LOG")"
  REPO_ROOT="$(git -C "$PF_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
  if [ -z "$REPO_ROOT" ]; then
    skipped "PF log is not inside a git repository: $PF_LOG (no prior revision to compare — G5 needs git history)"
    verdict
  fi
  # Path of the PF log relative to the repo root, for `git show HEAD:<rel>`.
  # NB: do NOT derive this by string-prefixing PF_DIR (a `cd && pwd` path) against
  # REPO_ROOT (a `--show-toplevel` realpath). On macOS those disagree (/var vs
  # /private symlinks), the prefix test fails, REL collapses to the bare basename,
  # and any PF log in a subdir (the real default, memory/) silently FATALs. Ask
  # git itself for the tracked repo-relative path instead — symlink-agnostic.
  REL="$(git -C "$PF_DIR" ls-files --full-name --error-unmatch -- "$PF_BASE" 2>/dev/null || true)"
  if [ -z "$REL" ]; then
    skipped "PF log not tracked at HEAD: $PF_LOG in $REPO_ROOT (no committed prior revision — G5 fail-closed F-008)"
    verdict
  fi
  if ! git -C "$REPO_ROOT" cat-file -e "HEAD:$REL" 2>/dev/null; then
    skipped "PF log not tracked at HEAD: $REL in $REPO_ROOT (no committed prior revision — G5 fail-closed F-008)"
    verdict
  fi
  PRIOR_CONTENT="$(git -C "$REPO_ROOT" show "HEAD:$REL" 2>/dev/null)"
  emit "comparing $PF_LOG against git HEAD:$REL"
fi

CURR_CONTENT="$(cat "$PF_LOG")"

# Build prior severity lookup: "id\tseverity" lines.
PRIOR_ROWS="$(printf '%s\n' "$PRIOR_CONTENT" | parse_entries)"
CURR_ROWS="$(printf '%s\n' "$CURR_CONTENT" | parse_entries)"

# Look up the prior severity for a given id (first match wins).
prior_sev_for() {
  local want="$1" line pid psev
  while IFS=$'\t' read -r pid psev _; do
    [ -n "$pid" ] || continue
    if [ "$pid" = "$want" ]; then printf '%s' "$psev"; return 0; fi
  done <<EOF
$PRIOR_ROWS
EOF
  return 1
}

checked=0
while IFS=$'\t' read -r id csev cregrade; do
  [ -n "$id" ] || continue
  psev="$(prior_sev_for "$id" || true)"
  # New entry (no prior) → nothing to downgrade; skip.
  [ -n "$psev" ] || continue
  [ -n "$csev" ] || continue
  checked=$((checked + 1))

  prank="$(sev_rank "$psev")"
  crank="$(sev_rank "$csev")"

  if [ -n "$prank" ] && [ -n "$crank" ]; then
    if [ "$crank" -lt "$prank" ]; then
      # DOWNGRADE detected. Allowed only with an explicit re-grade: marker.
      if [ "$cregrade" = "1" ]; then
        emit "$id: severity downgrade ${psev}->${csev} carries a re-grade: marker (allowed)"
      else
        fail "$id: silent severity downgrade ${psev}->${csev} with no adjacent \`re-grade:\` marker (no-softening / G5 — giq.4.2)"
      fi
    fi
  else
    # One or both severities are unrecognized tokens: cannot rank, but a CHANGE
    # between two differing values is still worth surfacing (report, don't silently pass).
    if [ "$(printf '%s' "$psev" | tr 'a-z' 'A-Z')" != "$(printf '%s' "$csev" | tr 'a-z' 'A-Z')" ]; then
      if [ "$cregrade" = "1" ]; then
        emit "$id: severity changed ${psev}->${csev} (unranked) with re-grade: marker (allowed)"
      else
        warn "$id: severity changed ${psev}->${csev} but one is an unrecognized token; cannot prove monotonicity — review manually"
      fi
    fi
  fi
done <<EOF
$CURR_ROWS
EOF

emit "$checked entr(y/ies) compared against prior revision"
verdict
