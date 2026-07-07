#!/usr/bin/env bash
# toolkit/scripts/rotation-stamp-audit.sh
#
# ENFORCES: CDM finding F-009 — the rotation/handoff stamp audit that NO project
# actually shipped working. Walks VOLATILE-labelled sections of a continuity doc
# and FAILs if any distinct session stamp falls outside the rotation window
# {n-1, n, n+1, n+2} around the current session n. "VOLATILE" sections are the
# living-state region of a handoff doc; stacked history there is the bug this
# catches (the doc accretes S140, S141, ... S172 in a section that must only ever
# hold the current rotation neighbourhood).
#
# Also carries the stale-hash sub-audit (CDM F-009 / lineage INV-HO-NO-STALE-HASH,
# AC-CM-03) because the named false-green lives there:
#   BUG-API-002 (carried forward): bash `[[ =~ ]]` uses POSIX ERE, which does NOT
#   honour the `\b` word-boundary escape — it matches a literal backslash-b. A
#   stale-hash regex written as `\b[0-9a-f]{7,40}\b` therefore NEVER matches a real
#   sha prefix and the audit emits "clean" unconditionally: a textbook false-green.
#   Fixed here with explicit character-class surround anchors + BASH_REMATCH capture.
#
# SOURCE LINEAGE:
#   - sources/Quant/scripts/handoff-audit.sh  (Check 2 check_volatile_stacking
#     INV-HO-ROTATION; Check 1 check_stale_hashes INV-HO-NO-STALE-HASH)
#   - maquette/scripts/{docfresh,close-attestation}-audit.sh (verdict/skipped
#     fail-closed exit semantics; BSD/GNU date+awk portability discipline)
#
# BUG-N notes carried forward from the Quant source (stable referents for the test):
#   BUG-003a: stale-hash match must contain >=1 hex letter (a-f) — rejects pure
#             decimal IDs like "20260424" as not-a-SHA.
#   BUG-003b: a bare session stamp (S172) is NOT date evidence for hash freshness;
#             only a YYYY-MM-DD adjacency whitelists a hex run.
#   BUG-API-002: `\b` does not work in bash ERE (see above).
#   BUG-002: rotation pointer bullets (- **Current/Prior/Next/Two-back session:**)
#            must contribute their stamps, not just `- **S{N}**` headers.
#   BUG-004: session-range expressions (Sxxx-Sxxx) require a literal S on BOTH
#            sides of the dash before they're skipped as ranges.
#
# Usage:
#   rotation-stamp-audit.sh [--current N] [--allow-skip] [--no-stale-hash] <target-doc>
#
#   --current N      current session number n (default: parsed from the doc's
#                    `Current session:** S<N>` line; FATAL if neither given).
#   --allow-skip     opt out of fail-closed on a check that cannot run (F-008).
#                    Equivalent to AUDIT_ALLOW_SKIP=1.
#   --no-stale-hash  rotation-window check only; skip the stale-hash sub-audit.
#   <target-doc>     path to the continuity/handoff markdown doc to audit.
#
# Env:
#   ROTATION_CURRENT_SESSION   default for --current.
#   AUDIT_ALLOW_SKIP=1         same as --allow-skip.
#
# Exit: 0 PASS / 1 FAIL (a stamp outside the window, or a stale hash) / 2 FATAL.

set -euo pipefail

AUDIT_TAG="rotation-stamp-audit"
# shellcheck source=../lib/audit-helpers.sh disable=SC1091
source "$(dirname "$0")/../lib/audit-helpers.sh"

# ---------------------------------------------------------------------------
# Argument parsing — proper loop, reject unknown args (SEC-004 lineage).
# ---------------------------------------------------------------------------
CURRENT_SESSION="${ROTATION_CURRENT_SESSION:-}"
DO_STALE_HASH=1
TARGET=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --current)
      shift
      [ "$#" -gt 0 ] || { emit "FATAL: --current requires a value"; exit 2; }
      CURRENT_SESSION="$1"
      ;;
    --current=*)
      CURRENT_SESSION="${1#--current=}"
      ;;
    --allow-skip)
      AUDIT_ALLOW_SKIP=1
      ;;
    --no-stale-hash)
      DO_STALE_HASH=0
      ;;
    --)
      shift
      break
      ;;
    -*)
      emit "FATAL: unknown arg: $1"
      exit 2
      ;;
    *)
      if [ -n "$TARGET" ]; then
        emit "FATAL: more than one target doc given ('$TARGET' and '$1')"
        exit 2
      fi
      TARGET="$1"
      ;;
  esac
  shift
done

# trailing positional after `--`
if [ "$#" -gt 0 ] && [ -z "$TARGET" ]; then
  TARGET="$1"
fi

if [ -z "$TARGET" ]; then
  # BUG-RS1 (fresh-start Session-C, F-026): with no explicit target, default to the
  # conventional continuity doc so the close-audit default roster runs CLEAN in a
  # standard project (instead of FATAL-ing for lack of an arg). Override by passing
  # an explicit <target-doc> (e.g. SESSION.md, or a custom path).
  for cand in HANDOFF.md SESSION.md; do
    [ -f "$cand" ] && { TARGET="$cand"; emit "no target given; defaulting to ./$cand"; break; }
  done
fi
if [ -z "$TARGET" ]; then
  emit "FATAL: no target doc given and no conventional continuity doc (HANDOFF.md/SESSION.md) in cwd. Usage: $0 [--current N] [--allow-skip] [--no-stale-hash] <target-doc>"
  exit 2
fi

if [ ! -f "$TARGET" ]; then
  # F-008: a missing target is "couldn't verify", not "verified clean".
  skipped "target doc not found: $TARGET (cannot audit rotation stamps)"
  verdict
fi

# ---------------------------------------------------------------------------
# Resolve current session n.
# BUG-007 lineage: fail-fast on a regex miss; do NOT silently default to 0,
# which would disable the window check and false-PASS everything.
# ---------------------------------------------------------------------------
if [ -z "$CURRENT_SESSION" ]; then
  CURRENT_SESSION=$(grep -Eo 'Current session:\*\*[[:space:]]*S[0-9]+' "$TARGET" 2>/dev/null \
    | head -n 1 | grep -Eo '[0-9]+' || true)
fi
if [ -z "$CURRENT_SESSION" ]; then
  emit "FATAL: cannot resolve current session (pass --current N, set"
  emit "       ROTATION_CURRENT_SESSION, or add a 'Current session:** S<N>' line)"
  exit 2
fi
case "$CURRENT_SESSION" in
  *[!0-9]*|"")
    emit "FATAL: --current must be a positive integer, got: '$CURRENT_SESSION'"
    exit 2
    ;;
esac

emit "auditing rotation stamps in VOLATILE sections of $TARGET (current=S${CURRENT_SESSION})"

# ---------------------------------------------------------------------------
# Check 1: VOLATILE-section rotation stacking (INV-HO-ROTATION / F-009).
#
# Allowed window per section: {n-1, n, n+1, n+2}. Any DISTINCT stamp outside it
# is stacking -> FAIL. Only STRUCTURAL session positions count as stamps (header
# lines and canonical rotation pointer bullets) — inline narrative mentions like
# "unchanged from S168" are not stacking.
#
# Skipped contexts (do not contribute stamps): fenced code blocks, markdown table
# rows, single legitimate Historical pointer line, Sxxx-Sxxx range expressions.
#
# awk is invoked through process substitution `< <(...)` (NOT a pipe), so the
# `while read`/fail loop runs in the PARENT shell and `$violations` survives
# (BUG-008 lineage).
# ---------------------------------------------------------------------------
check_volatile_stacking() {
  local file="$1" cur="$2"
  local marker header count stamps
  local walked=0
  while IFS=: read -r marker header count stamps; do
    walked=1
    if [ "$marker" = "STACK" ]; then
      fail "VOLATILE-section stacking in '${header}' — distinct out-of-window stamps: ${count} (${stamps}); window is {S$((cur-1))..S$((cur+2))}"
    fi
  done < <(awk -v cur="$cur" -v ed="$(printf '\xe2\x80\x93')" '
    function flush_section() {
      if (current != "") {
        n = split(stamps, parts, ",")
        extra_count = 0
        delete seen_extra
        for (i = 1; i <= n; i++) {
          tok = parts[i]
          if (tok == "") continue
          sub(/^S/, "", tok)
          # Allowed window {cur-1, cur, cur+1, cur+2}.
          if (tok == cur || tok == (cur - 1) || tok == (cur + 1) || tok == (cur + 2)) continue
          if (!(tok in seen_extra)) {
            seen_extra[tok] = 1
            extra_count++
          }
        }
        if (extra_count > 0) {
          extras = ""
          for (k in seen_extra) extras = extras " S" k
          print "STACK:" current ":" extra_count ":" extras
        } else {
          print "OK:" current ":0:"
        }
      }
      current = ""
      stamps = ""
    }
    /^```/ { in_fence = 1 - in_fence; next }
    in_fence == 1 { next }
    /^#+ .*VOLATILE/ { flush_section(); current = $0; stamps = ""; next }
    /^#+ / { flush_section(); next }
    current != "" {
      line = $0
      if (line ~ /^\|/) { next }                                   # table row
      if (line ~ /^\*\*Historical \(kept for reference\):\*\*/) { next }
      # BUG-004: only skip ranges with a literal S on BOTH sides of the dash.
      # BUG-009 (W1-7, 2026-07-02): the en-dash was written as an in-regex byte escape
      # /[-\xe2\x80\x93]/, which byte-oriented BSD/BWK awk does NOT honour (and a 3-byte
      # en-dash cannot live in a single-char bracket anyway), so `S140–S172` ranges were
      # NOT skipped and their endpoints counted as stamps -> false STACK FAIL. The
      # en-dash bytes now arrive via -v ed=... and match as a literal alternation.
      if (line ~ ("S[0-9]+(-|" ed ")S[0-9]+") || line ~ /S[0-9]+ ?through ?S[0-9]+/) { next }
      # Structural-position filter — count only canonical pointer bullets and
      # session-block headers (BUG-002 widened the pointer set).
      if (line !~ /^- \*\*(Current|Prior(-session)?( pointer)?|Next|Two-back) session:/ \
          && line !~ /^- \*\*[Ss](ession)? ?[0-9]+/ \
          && line !~ /^\*\*[Ss](ession)? ?[0-9]+/ \
          && line !~ /^#+ .*[Ss]ession [0-9]+/) { next }
      while (match(line, /S[0-9][0-9]?[0-9]?[0-9]?|Session [0-9][0-9]?[0-9]?[0-9]?/)) {
        tok = substr(line, RSTART, RLENGTH)
        gsub(/Session /, "S", tok)
        stamps = stamps "," tok
        line = substr(line, RSTART + RLENGTH)
      }
    }
    END { flush_section() }
  ' "$file")

  if [ "$walked" -eq 0 ]; then
    # No VOLATILE section at all -> the property is unverifiable on this doc.
    # F-008 fail-closed: count it as a skip unless the operator allows it.
    skipped "no VOLATILE-labelled section found in $file (rotation window unverifiable)"
  else
    emit "rotation-window audit: walked VOLATILE section(s)"
  fi
}

check_volatile_stacking "$TARGET" "$CURRENT_SESSION"

# ---------------------------------------------------------------------------
# Check 2: stale-hash sub-audit (INV-HO-NO-STALE-HASH / AC-CM-03).
# Bare 7-40 hex runs (git SHA family) in narrative prose are stale evidence.
# Allowed: inside a fenced code block; on a line mentioning 'sha256'/'hash';
# on a line carrying a YYYY-MM-DD date stamp (BUG-003b: a session stamp is NOT
# date evidence). BUG-003a: the hex run must contain >=1 letter a-f AND >=1 digit.
#
# BUG-API-002 (the named false-green): `\b` is inert in bash ERE; use explicit
# character-class surround anchors and read the capture from BASH_REMATCH[2].
# ---------------------------------------------------------------------------
check_stale_hashes() {
  local file="$1"
  local in_fence=0 lineno=0 hits=0 line match
  local hex_re='(^|[^0-9a-f])([0-9a-f]{7,40})($|[^0-9a-f])'
  local date_re='(^|[^0-9])(20[0-9][0-9]-[0-1][0-9]-[0-3][0-9])($|[^0-9])'
  local sha_or_hash_re='(sha256|hash)'

  while IFS= read -r line || [ -n "$line" ]; do
    lineno=$((lineno + 1))
    if [[ "$line" =~ ^\`\`\` ]]; then
      in_fence=$((1 - in_fence))
      continue
    fi
    [ "$in_fence" -eq 1 ] && continue

    if [[ "$line" =~ $hex_re ]]; then
      match="${BASH_REMATCH[2]}"
      [[ "$match" =~ [a-f] ]] || continue   # BUG-003a: need a hex letter
      [[ "$match" =~ [0-9] ]] || continue   # need a digit (reject English words)
      [[ "$line" =~ $sha_or_hash_re ]] && continue
      [[ "$line" =~ $date_re ]] && continue # BUG-003b: only date adjacency whitelists
      hits=$((hits + 1))
      fail "stale-hash in ${file}:${lineno}: ${line:0:120}"
    fi
  done < "$file"

  [ "$hits" -eq 0 ] && emit "stale-hash audit: clean"
}

if [ "$DO_STALE_HASH" -eq 1 ]; then
  check_stale_hashes "$TARGET"
fi

verdict
