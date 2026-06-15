#!/usr/bin/env bash
# pf-attestation-audit.sh — enforce the close-time process-failure (PF) attestation.
#
# WHAT IT ENFORCES (INV-PF-ATTESTATION / CDM-8-5 hardened):
#   Every session close MUST do exactly one of:
#     (a) append a NEW PF entry for session N to the PF log, OR
#     (b) record an explicit NEGATIVE attestation that NO new PF-class entries
#         were promoted this session AND list what was observed-but-not-promoted
#         (and why it did not rise to PF level).
#   "Silence is NOT equivalent to absence." A close that does NEITHER FAILS.
#
#   The canonical attestation line (CLAUDE.md close-protocol step 4) is:
#       S<N> close (YYYY-MM-DD): <attestation text — affirmative OR negative>
#
#   CDM-8-5 HARDENING over the original presence-only check: a NEGATIVE
#   attestation ("No new PF-class entries this session") is only accepted when it
#   also carries the observed-but-not-promoted rationale (some non-trivial text
#   after the negative claim). A bare "S<N> close (date): No new PF-class entries
#   this session." with nothing else is the false-green this audit exists to
#   catch — it is the mechanical equivalent of silence and FAILS.
#
# SOURCE LINEAGE:
#   sources/a-plus-maxing/scripts/pf-attestation-audit.sh (a-plus-maxing, INV-PF-
#   ATTESTATION). That v1 was a pure presence check (regex match on the canonical
#   line) and ran on HANDOFF.md. This canonical version:
#     - sources the rigor toolkit lib (emit/fail/warn/skipped/verdict, F-008
#       fail-closed skip semantics) instead of the project-local audit_* helpers;
#     - is dependency-free (no python3) — pure bash + grep, portable BSD+GNU;
#     - parameterizes the PF-log path and session N (no hardcoded project paths);
#     - hardens the negative-attestation case per CDM-8-5 (rationale required).
#
# BUG-1 (CDM-8-5, carried forward): the v1 accepted ANY non-empty text after the
#   colon, so a content-free negative attestation false-PASSed. The negative test
#   pins this exact case: a bare "No new PF-class entries this session." with no
#   observed-but-not-promoted rationale must FAIL.
#
# Exit codes (via verdict): 0 PASS / 1 FAIL (violation) / 2 FATAL (env/skip).
#
# Usage:
#   pf-attestation-audit.sh [--session N] [--pf-log PATH] [PATH]
#   PF_LOG / PF_ATTEST_SESSION env vars supply defaults.
# Defaults: PF log = ${PF_LOG:-./memory/process-failures.md}; session = highest seen.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="pf-attestation-audit"

PF_LOG="${PF_LOG:-./memory/process-failures.md}"
REQUIRE_SESSION="${PF_ATTEST_SESSION:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --session)
      REQUIRE_SESSION="${2:-}"
      [ -n "$REQUIRE_SESSION" ] || { emit "FATAL: --session requires an integer argument"; exit 2; }
      shift 2 ;;
    --session=*) REQUIRE_SESSION="${1#--session=}"; shift ;;
    --pf-log)
      PF_LOG="${2:-}"
      [ -n "$PF_LOG" ] || { emit "FATAL: --pf-log requires a path"; exit 2; }
      shift 2 ;;
    --pf-log=*) PF_LOG="${1#--pf-log=}"; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) emit "FATAL: unknown flag: $1"; exit 2 ;;
    *) PF_LOG="$1"; shift ;;
  esac
done

if [ -n "$REQUIRE_SESSION" ] && ! printf '%s' "$REQUIRE_SESSION" | grep -Eq '^[0-9]+$'; then
  emit "FATAL: --session must be an integer, got: $REQUIRE_SESSION"
  exit 2
fi

# The PF log not existing is an env error the operator must fix, not a clean pass.
if [ ! -f "$PF_LOG" ]; then
  emit "FATAL: PF log not found: $PF_LOG (set --pf-log or PF_LOG)"
  exit 2
fi

emit "auditing PF attestation in: $PF_LOG${REQUIRE_SESSION:+ (require session $REQUIRE_SESSION)}"

# Canonical attestation line:  [## ] S<N> close (YYYY-MM-DD): <rest>
# Extract: "<N>|<rest>" for every matching line. Portable ERE (BSD+GNU grep -E).
# BUG-PA1 (fresh-start Session-C, F-026): allow an OPTIONAL markdown header prefix
#   (`#{0,6} `). The canonical attestation line in real PF logs is an H2 header
#   ('## S<N> close (date): ...'); the original ^\s*S anchor rejected its OWN
#   prescribed format. Now both '## S1 close (...)' and bare 'S1 close (...)' match.
ATTEST_RE='^[[:space:]]*#{0,6}[[:space:]]*S[0-9]+[[:space:]]+close[[:space:]]+\([0-9]{4}-[0-9]{2}-[0-9]{2}\):[[:space:]]+[^[:space:]]'

# Gather matches into "N<TAB>rest" pairs.
matches="$(grep -nE "$ATTEST_RE" "$PF_LOG" 2>/dev/null || true)"

if [ -z "$matches" ]; then
  # Neither a new PF entry framed as an attestation nor a negative attestation
  # was found. This is the core negative case: silence != absence -> FAIL.
  fail "no canonical \`S<N> close (YYYY-MM-DD):\` attestation line found in $PF_LOG (silence is not absence — INV-PF-ATTESTATION)"
  verdict
fi

# Find the highest session N among the matches, and the text of that line.
highest_n=-1
highest_line=""
while IFS= read -r line; do
  [ -n "$line" ] || continue
  # strip leading "lineno:" from grep -n
  content="${line#*:}"
  # BUG-PA1 part-2 (dv2.7): the session-number EXTRACTION must allow the same
  # optional markdown-header prefix the ATTEST_RE grep allows (#{0,6}) — else a
  # canonical '## S4 close ...' header is FOUND but its N mis-parses (to garbage,
  # observed as S-1). Mirror the prefix here.
  n="$(printf '%s' "$content" | sed -E 's/^[[:space:]]*#{0,6}[[:space:]]*S([0-9]+)[[:space:]]+close.*/\1/')"
  case "$n" in
    ''|*[!0-9]*) continue ;;
  esac
  if [ "$n" -gt "$highest_n" ]; then
    highest_n="$n"
    highest_line="$content"
  fi
done <<EOF
$matches
EOF

count="$(printf '%s\n' "$matches" | grep -c . )"
emit "$count attestation line(s) found; latest is session S$highest_n"

# Session-match enforcement: the latest attestation must be for the required N.
if [ -n "$REQUIRE_SESSION" ] && [ "$highest_n" != "$REQUIRE_SESSION" ]; then
  fail "latest attestation is session S$highest_n but --session required S$REQUIRE_SESSION (stale/missing close attestation)"
  verdict
fi

# CDM-8-5 / BUG-1: if the latest attestation is NEGATIVE ("no new PF ... this
# session"), it must also carry observed-but-not-promoted rationale. A bare
# negative claim with no following content is the false-green we reject.
# Pull the text after the "S<N> close (date):" prefix.
attest_text="$(printf '%s' "$highest_line" | sed -E 's/^[[:space:]]*S[0-9]+[[:space:]]+close[[:space:]]+\([0-9]{4}-[0-9]{2}-[0-9]{2}\):[[:space:]]*//')"

# Is it a negative attestation? Match the canonical "no new PF" phrasing, case-insensitive.
if printf '%s' "$attest_text" | grep -Eiq 'no[[:space:]]+(new[[:space:]]+)?PF([- ]class)?[[:space:]]+(entries|incidents)'; then
  # Negative attestation. Strip the negative-claim sentence and require that
  # SOMETHING substantive remains (the observed-but-not-promoted rationale).
  # Remove the first sentence up to and including its terminating period.
  rationale="$(printf '%s' "$attest_text" | sed -E 's/^[^.]*\.[[:space:]]*//')"
  # Collapse whitespace; count remaining non-space chars.
  rationale_trimmed="$(printf '%s' "$rationale" | tr -d '[:space:]')"
  if [ "${#rationale_trimmed}" -lt 10 ]; then
    fail "S$highest_n is a NEGATIVE PF attestation but lists no observed-but-not-promoted rationale (CDM-8-5: a bare 'no new PF' is mechanical silence — BUG-1)"
    verdict
  fi
  emit "negative attestation S$highest_n carries observed-but-not-promoted rationale (CDM-8-5 OK)"
else
  emit "affirmative attestation S$highest_n (new PF entry promoted)"
fi

verdict
