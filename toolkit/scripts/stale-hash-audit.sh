#!/usr/bin/env bash
# stale-hash-audit.sh — rigor framework canonical audit.
#
# ENFORCES: INV-HO-NO-STALE-HASH (CDM finding family F-007).
#   Narrative prose (HANDOFF/MEMORY/docs) must NOT cite bare commit-hash /
#   sha256-prefix tokens. Hashes go stale the instant a fix-commit lands;
#   provenance belongs in versioned artifacts (ADRs, vault decisions) cited by
#   filename, OR — if a SHA must appear — next to a date/session stamp so its
#   staleness is self-evident to the next reader.
#
# SOURCE LINEAGE:
#   Generalized from sources/a-plus-maxing/scripts/handoff-audit.sh — the WORKING
#   stale-hash check (Python `re`, clause-3 of INV-HO-ROTATION). That version is
#   sound because Python's `\b` is real. It is the authoritative reference.
#   NOT generalized from Quant's variant, which used `\b[0-9a-f]{7,}\b` in a BSD
#   ERE grep: a FALSE-GREEN (F-007). On BSD/POSIX `grep -E`, `\b` is NOT a defined
#   word-boundary operator — it is interpreted inconsistently (literal / undefined),
#   so the guard silently failed to match bare hashes and reported PASS on bad input.
#
# BUG-N notes carried forward:
#   BUG-7 (F-007, the false-green): DO NOT use `\b` in a BSD ERE. This version uses
#     NO `\b`. Word-boundary semantics are reconstructed portably: candidate hex
#     tokens are isolated by translating every non-[0-9a-f] byte to a newline, then
#     each isolated token is length-gated AND required to carry >=1 hex LETTER (a-f).
#     The hex-letter requirement is load-bearing: it excludes pure-decimal runs
#     (years "2026", line numbers, counts) that a length-only check would false-fire on.
#   BUG-7b (anchoring): because we split on non-hex bytes, an embedded run inside a
#     longer alphanumeric word (e.g. "g123abc4" -> the `g` splits it) is handled by the
#     same non-hex-delimiter logic — no `\b` needed and no over-match into word interiors.
#
# DETECTION CONTRACT:
#   - Operates line-by-line over a target file (default) or stdin.
#   - EXCLUDES fenced code blocks (``` ... ```), where hashes are legitimate.
#   - EXCLUDES lines that NAME the hash ("sha256", "hash") — those are labeled
#     references handled by their own policy, not bare narrative leakage.
#   - EXCLUDES date-adjacent lines (a SHA next to YYYY-MM-DD / "Session N" / "S<N> close"
#     is self-dating per clause 4 — allowed).
#   - A surviving token of 7..40 hex chars containing >=1 a-f letter is a VIOLATION.
#
# EXIT SEMANTICS (via lib/audit-helpers.sh): 0 PASS / 1 FAIL / 2 FATAL.
#   Missing target file -> FATAL. Skips are fail-closed (F-008) unless AUDIT_ALLOW_SKIP=1.
#
# USAGE:
#   stale-hash-audit.sh [FILE]          # audit FILE (default: $STALE_HASH_TARGET or ./HANDOFF.md)
#   cat file | stale-hash-audit.sh -    # audit stdin
#   STALE_HASH_MIN_LEN=8 stale-hash-audit.sh FILE   # override min hash length (default 7)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="stale-hash-audit"

# --- Parameters (no hardcoded project paths) -------------------------------
TARGET="${1:-${STALE_HASH_TARGET:-./HANDOFF.md}}"
MIN_LEN="${STALE_HASH_MIN_LEN:-7}"
MAX_LEN="${STALE_HASH_MAX_LEN:-40}"

# Date-adjacency: a SHA on a line carrying any of these is self-dating (allowed).
DATE_RE='[0-9]{4}-[0-9]{2}-[0-9]{2}|[Ss]ession [0-9]+|S[0-9]+ close'
# Labeled-hash lines: the token is named, not bare narrative leakage.
LABEL_RE='sha256|[Hh]ash'

# --- Input acquisition -----------------------------------------------------
if [ "$TARGET" = "-" ]; then
  CONTENT="$(cat)"
else
  if [ ! -f "$TARGET" ]; then
    emit "FATAL: target file not found: $TARGET"
    exit 2
  fi
  CONTENT="$(cat "$TARGET")"
fi

emit "scanning ${TARGET} (hex token len ${MIN_LEN}..${MAX_LEN}, >=1 a-f letter required, no \\b)"

# --- Scan ------------------------------------------------------------------
# Track fenced-code state across lines so in-block hashes are excluded.
in_fence=0
lineno=0

# Iterate WITHOUT a subshell pipe so $violations (in helpers) survives.
while IFS= read -r line || [ -n "$line" ]; do
  lineno=$((lineno + 1))

  # Toggle fenced code block on any line whose first non-space run is ``` (or ~~~).
  trimmed="${line#"${line%%[![:space:]]*}"}"  # left-trim
  case "$trimmed" in
    '```'*|'~~~'*)
      in_fence=$((1 - in_fence))
      continue
      ;;
  esac
  [ "$in_fence" -eq 1 ] && continue

  # Skip indented code blocks (>=4 leading spaces) — Markdown code, hashes legit.
  case "$line" in
    '    '*) continue ;;
  esac

  # EXCLUSION: labeled hash line (names sha256/hash) — handled by its own policy.
  if printf '%s' "$line" | grep -Eq "$LABEL_RE"; then
    continue
  fi

  # EXCLUSION: date-adjacent line — SHA is self-dating, allowed (clause 4).
  if printf '%s' "$line" | grep -Eq "$DATE_RE"; then
    continue
  fi

  # Lowercase the line for hex matching (commit SHAs are lowercase hex by convention;
  # uppercase hex words like "DEAD" in prose are not hashes — keep them out).
  low="$(printf '%s' "$line" | tr 'A-Z' 'a-z')"

  # Isolate candidate hex tokens WITHOUT \b: translate every non-[0-9a-f] byte to a
  # newline, leaving one hex run per line, then gate by length + hex-letter presence.
  # This is the F-007 fix: pure character-class splitting, no word-boundary operator.
  hits="$(printf '%s' "$low" \
    | tr -c '0-9a-f' '\n' \
    | grep -E "^[0-9a-f]{${MIN_LEN},${MAX_LEN}}$" \
    | grep -E '[a-f]' || true)"

  if [ -n "$hits" ]; then
    while IFS= read -r tok; do
      [ -z "$tok" ] && continue
      fail "line ${lineno}: bare commit/sha256 hash prefix in narrative prose: '${tok}' — cite a dated artifact instead (INV-HO-NO-STALE-HASH / F-007)"
    done <<EOF
$hits
EOF
  fi
done <<EOF
$CONTENT
EOF

verdict
