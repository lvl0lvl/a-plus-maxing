#!/usr/bin/env bash
# pf-ingest.sh — transform a Process-Failure (PF) entry into harvest artifacts.
#
# WHAT IT ENFORCES / WHY IT EXISTS (Finding F-018 — the dead learning wire):
#   F-018 is the convergent absence of any mechanism that GROWS a role/skill's
#   Anti-Pattern / Negative-Example surface FROM accumulated PF data. PF entries
#   pile up, but nothing transforms them into the inverse-rule anti-patterns that
#   a role/skill profile carries (Discipline 10: "I don't X" failure-mode catalog).
#   The learning loop has a logged-failure END and an anti-pattern-surface END,
#   and no wire between them. This is that wire — Mechanism 2 (helper):
#     IN : one PF entry (Pattern / Root cause / Detection mode / Lesson /
#          Anti-pattern fields, per the framework PF template).
#     OUT: (a) one machine-readable harvest JSONL record on stdout (the ledger
#             FAIL-schema row — categorized, machine-readable evidence), AND
#          (b) a markdown Anti-Pattern / Negative-Example STUB ("I don't <inverse
#             rule>...") suitable for appending to the implicated role/skill
#             profile — the F-018 wire made concrete.
#
#   This is a TRANSFORM, not a pass/fail audit. It does not run `verdict`. Its
#   contract: well-formed PF entry -> valid JSONL + non-empty stub, exit 0;
#   empty/garbage/unparseable input -> exit 2 (FATAL, fail-closed). It still
#   sources audit-helpers.sh for the normalized `[tag] LEVEL: msg` diagnostic
#   shape (emit/warn to stderr) and the 0/2 exit discipline.
#
# BUG-N convention (per audit-helpers.sh / F-007): a real defect fixed here is
#   annotated `# BUG-N (context): ...` so the negative test pinning it has a
#   stable referent.
#
#   BUG-1 (unparseable fail-closed): an earlier mental model would emit a JSONL
#     record with empty fields for garbage input (a "successful" transform of
#     nothing) — a false-green that silently feeds noise into the harvest ledger.
#     A PF entry with NO recognizable Pattern AND NO Anti-pattern/Lesson is not a
#     PF entry; it must exit 2, never emit. The negative test pins this.
#
# Args:
#   --pf-entry <file>     read the PF entry from <file> ("-" or omitted = stdin)
#   --target-artifact <n> name of the role/skill profile the stub targets
#                         (recorded in JSONL + stub header; default: inferred/"unknown")
#   -h | --help           print this header.
#
# Exit codes: 0 success (JSONL + stub emitted) / 2 FATAL (unparseable input,
#             bad flags, fail-closed empty). There is no exit 1 — this is a
#             transform, not a violation-counting audit.
#
# Dependency-free: pure bash + grep/sed/tr. No jq/python. Portable BSD+GNU.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="pf-ingest"

# Diagnostics go to stderr so stdout carries ONLY the JSONL record (+ the stub,
# which is separated by a sentinel) — keeps stdout machine-consumable.
emit() { echo "[${AUDIT_TAG}] $*" >&2; }

PF_ENTRY=""           # path; empty => stdin
TARGET_ARTIFACT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --pf-entry)
      PF_ENTRY="${2:-}"
      [ -n "$PF_ENTRY" ] || { emit "FATAL: --pf-entry requires a path or '-'"; exit 2; }
      shift 2 ;;
    --pf-entry=*) PF_ENTRY="${1#--pf-entry=}"; shift ;;
    --target-artifact)
      TARGET_ARTIFACT="${2:-}"
      [ -n "$TARGET_ARTIFACT" ] || { emit "FATAL: --target-artifact requires a name"; exit 2; }
      shift 2 ;;
    --target-artifact=*) TARGET_ARTIFACT="${1#--target-artifact=}"; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) emit "FATAL: unknown flag: $1"; exit 2 ;;
    *)
      # Bare positional = the PF entry file (convenience).
      if [ -z "$PF_ENTRY" ]; then PF_ENTRY="$1"; shift
      else emit "FATAL: unexpected argument: $1"; exit 2; fi ;;
  esac
done

# --- Read the raw entry -------------------------------------------------------
if [ -z "$PF_ENTRY" ] || [ "$PF_ENTRY" = "-" ]; then
  RAW="$(cat)"
else
  if [ ! -f "$PF_ENTRY" ]; then
    emit "FATAL: PF entry file not found: $PF_ENTRY"
    exit 2
  fi
  RAW="$(cat "$PF_ENTRY")"
fi

# Fail-closed on empty input (BUG-1): no bytes => nothing to transform.
if [ -z "$(printf '%s' "$RAW" | tr -d '[:space:]')" ]; then
  emit "FATAL: empty PF entry — nothing to transform (fail-closed, F-018/BUG-1)"
  exit 2
fi

# --- Field extraction ---------------------------------------------------------
# Pull the text after a bolded field label, e.g. "**Pattern:** the text".
# Tolerant of: leading whitespace, optional bold markers, "Root cause" vs
# "Root-cause", trailing colon. Returns the FIRST matching line's value, with
# surrounding markdown/whitespace trimmed. Portable BSD+GNU sed (ERE via -E).
extract_field() {
  # $1 = ERE alternation of label spellings (no anchors).
  # Find the first matching label line case-insensitively, then strip everything
  # up to and including the FIRST colon (portable — no GNU sed 'I' flag). The
  # canonical label is bold ("**Pattern:**"), so the colon sits INSIDE the bold
  # and the strip leaves a leading "** " — remove any leading/trailing markdown
  # emphasis markers, then trim surrounding whitespace.
  printf '%s\n' "$RAW" \
    | grep -iE "^[[:space:]]*\**(${1})\**[[:space:]]*:" \
    | head -n1 \
    | sed -E 's/^[^:]*:[[:space:]]*//' \
    | sed -E 's/^[*_[:space:]]+//' \
    | sed -E 's/[*_[:space:]]+$//'
}

PATTERN="$(extract_field 'Pattern')"
ROOT_CAUSE="$(extract_field 'Root[- ]cause')"
DETECTION="$(extract_field 'Detection[- ]mode')"
LESSON="$(extract_field 'Lesson')"
ANTIPATTERN="$(extract_field 'Anti[- ]pattern( to avoid)?')"

# PF id + title from the canonical heading "## PF-S{N}-{NN} (date): title".
PF_ID="$(printf '%s\n' "$RAW" \
  | grep -oiE 'PF-S[0-9]+-[0-9]+' | head -n1)"
PF_TITLE="$(printf '%s\n' "$RAW" \
  | grep -iE '^[[:space:]]*#+[[:space:]]*PF-S[0-9]+-[0-9]+' | head -n1 \
  | sed -E 's/.*\)[[:space:]]*:?[[:space:]]*//' \
  | sed -E 's/^[[:space:]]*#+[[:space:]]*//' \
  | sed -E 's/[[:space:]]+$//')"

# --- Parseability gate (BUG-1) ------------------------------------------------
# A genuine PF entry must yield AT LEAST a Pattern, OR an Anti-pattern/Lesson we
# can invert. Garbage with none of these is unparseable -> exit 2, emit nothing.
if [ -z "$PATTERN" ] && [ -z "$ANTIPATTERN" ] && [ -z "$LESSON" ]; then
  emit "FATAL: unparseable PF entry — no Pattern, Anti-pattern, or Lesson field found (fail-closed, F-018/BUG-1)"
  exit 2
fi

# --- Derive the inverse-rule anti-pattern stub --------------------------------
# Prefer an explicit Anti-pattern field; else invert the Lesson; else the Pattern.
if [ -n "$ANTIPATTERN" ]; then
  INVERSE="$ANTIPATTERN"
elif [ -n "$LESSON" ]; then
  INVERSE="$LESSON"
else
  INVERSE="$PATTERN"
fi
# Normalize to an "I don't ..." inverse-rule sentence. Lowercase the leading
# char so it reads naturally after "I don't " (portable: no GNU \L).
first_ch="$(printf '%s' "$INVERSE" | cut -c1 | tr '[:upper:]' '[:lower:]')"
rest_ch="$(printf '%s' "$INVERSE" | cut -c2-)"
inverse_lc="${first_ch}${rest_ch}"

# Target artifact: explicit flag wins; else "unknown" (operator fills in).
TARGET="${TARGET_ARTIFACT:-unknown}"

# --- JSON string escaper (no jq) ----------------------------------------------
json_escape() {
  # Escape backslash, double-quote, and collapse control chars/newlines to space.
  printf '%s' "$1" \
    | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' \
    | tr '\n\r\t' '   '
}

# --- Emit the harvest JSONL record (ledger FAIL-schema) -----------------------
# One line, machine-readable. Fields mirror the PF template + harvest routing.
{
  printf '{'
  printf '"record_type":"pf_harvest",'
  printf '"schema":"ledger.fail.v1",'
  printf '"pf_id":"%s",'        "$(json_escape "${PF_ID:-}")"
  printf '"title":"%s",'        "$(json_escape "${PF_TITLE:-}")"
  printf '"pattern":"%s",'      "$(json_escape "$PATTERN")"
  printf '"root_cause":"%s",'   "$(json_escape "$ROOT_CAUSE")"
  printf '"detection_mode":"%s",' "$(json_escape "$DETECTION")"
  printf '"lesson":"%s",'       "$(json_escape "$LESSON")"
  printf '"anti_pattern":"%s",' "$(json_escape "$ANTIPATTERN")"
  printf '"inverse_rule":"%s",' "$(json_escape "$inverse_lc")"
  printf '"target_artifact":"%s",' "$(json_escape "$TARGET")"
  printf '"nominated":true'
  printf '}\n'
}

# --- Emit the markdown anti-pattern / negative-example stub -------------------
# Sentinel separates the JSONL (line 1) from the stub for downstream splitting.
printf -- '---PF-INGEST-STUB---\n'
printf -- '### Anti-pattern (nominated from %s — target: %s)\n\n' \
  "${PF_ID:-PF-entry}" "$TARGET"
printf -- "I don't %s\n\n" "$inverse_lc"
if [ -n "$ROOT_CAUSE" ]; then
  printf -- '- Root cause this guards: %s\n' "$ROOT_CAUSE"
fi
if [ -n "$DETECTION" ]; then
  printf -- '- Was caught by: %s\n' "$DETECTION"
fi
printf -- '- Source: %s\n' "${PF_ID:-PF entry (unidentified)}"
printf -- '- Status: NOMINATED — review before adding to the %s profile (F-018 wire).\n' "$TARGET"

emit "transformed ${PF_ID:-PF entry} -> JSONL + anti-pattern stub (target: $TARGET)"
exit 0
