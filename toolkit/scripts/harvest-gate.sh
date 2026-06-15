#!/usr/bin/env bash
# toolkit/scripts/harvest-gate.sh — the self-improvement-loop HARVEST GATE.
#
# WHAT IT ENFORCES (Finding F-017 — the self-improvement loop is a playbook with
#   MECHANICALLY-ENFORCED inputs):
#   A "clean close" is dishonest if a session failure was felt but never captured.
#   The loop only learns from failures that are written down in EVERY layer that
#   the loop reads back: the human-readable Process-Failures log (PF), the
#   machine-readable harvest ledger (harvest.jsonl, the FAIL-record stream the
#   analyst mines), AND the bead backlog (issues.jsonl, the tracked-work layer).
#   A failure logged in only ONE layer falls out of the loop: a PF prose note with
#   no harvest record is invisible to the analyst; a harvest record with no bead is
#   never scheduled to be fixed. So this is a FAIL-CLOSED gate: for every failure id
#   in the PF log's current-session section it asserts a matching, schema-valid
#   record exists in harvest.jsonl AND a bead in issues.jsonl references it. Any
#   failure missing from any of the THREE layers -> FAIL (exit 1).
#
#   Mechanism 2 of F-017 (enforcement). Mechanism 1 is the playbook itself; this is
#   the gate that refuses to let the loop pretend a failure was harvested when it
#   was not.
#
# HARVEST RECORD SHAPE (vault/instruments/ledger-schema.md §2, FAIL-record):
#   Each harvest.jsonl line is one well-formed JSON object with required fields:
#     id            FAIL-<PROJECT>-<NNN>
#     class         failure class (e.g. enforcement-gap)
#     source_refs   array of PF-id / bead-id / file:line back-references
#     recurrence    recurrence count (schema: recurrence_count; accept either key)
#     detection_mode user-catch|spot-check|red-team|mechanical-audit|gate-trip|self
#   A line that is not parseable JSON, or is missing any required field, is itself a
#   violation (a malformed ledger line is unmineable -> the failure is lost).
#
# BUG-N convention (see lib/audit-helpers.sh): a real defect found+fixed in an audit
#   is annotated `# BUG-N (context): ...` so the negative test that proves the fix
#   has a stable referent. An audit that cannot prove it FAILs on bad input does not
#   count (F-007) — see tests/test-harvest-gate.sh.
#
# USAGE:
#   harvest-gate.sh --pf <process-failures.md> --harvest <harvest.jsonl> \
#                   --beads <issues.jsonl> [--session N]
#   --session N   restrict the PF scan to the "Session N" section. Default: the
#                 last/current session section found in the PF log.
#
# EXIT: 0 PASS (every PF failure captured in all 3 layers) / 1 FAIL (a failure
#       missing from a layer, or a malformed harvest line) / 2 FATAL (bad args /
#       unreadable input — a check that cannot run does not pass).
#
# Portable across BSD (macOS bash 3.2) and GNU. Dependency-free: no jq/python.

set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-harvest-gate}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "${SELF_DIR}/../lib/audit-helpers.sh"

# --- arg parsing -------------------------------------------------------------
PF=""
HARVEST=""
BEADS=""
SESSION=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --pf)        shift; [ "$#" -gt 0 ] || { emit "FATAL: --pf needs a value"; exit 2; }; PF="$1" ;;
    --pf=*)      PF="${1#*=}" ;;
    --harvest)   shift; [ "$#" -gt 0 ] || { emit "FATAL: --harvest needs a value"; exit 2; }; HARVEST="$1" ;;
    --harvest=*) HARVEST="${1#*=}" ;;
    --beads)     shift; [ "$#" -gt 0 ] || { emit "FATAL: --beads needs a value"; exit 2; }; BEADS="$1" ;;
    --beads=*)   BEADS="${1#*=}" ;;
    --session)   shift; [ "$#" -gt 0 ] || { emit "FATAL: --session needs a value"; exit 2; }; SESSION="$1" ;;
    --session=*) SESSION="${1#*=}" ;;
    -h|--help)   sed -n '2,40p' "$0"; exit 0 ;;
    --*)         emit "FATAL: unknown arg: $1"; exit 2 ;;
    *)           emit "FATAL: unexpected positional arg: $1"; exit 2 ;;
  esac
  shift
done

[ -n "$PF" ]      || { emit "FATAL: --pf <process-failures.md> is required"; exit 2; }
[ -n "$HARVEST" ] || { emit "FATAL: --harvest <harvest.jsonl> is required"; exit 2; }
[ -n "$BEADS" ]   || { emit "FATAL: --beads <issues.jsonl> is required"; exit 2; }

for f in "$PF" "$HARVEST" "$BEADS"; do
  [ -f "$f" ] || { emit "FATAL: input not found / not a file: $f"; exit 2; }
  [ -r "$f" ] || { emit "FATAL: input not readable: $f"; exit 2; }
done

# --- helpers -----------------------------------------------------------------

# json_has_field <line> <field>
# True if a top-level "field": appears in the JSON line. Dependency-free and
# deliberately conservative: it looks for the quoted key followed by a colon.
json_has_field() {
  case "$1" in
    *"\"$2\""*':'*) return 0 ;;
    *) return 1 ;;
  esac
}

# json_well_formed <line>
# Minimal structural JSON-object validity check without jq: must be wrapped in
# braces, balanced braces/brackets, and balanced double quotes (ignoring escaped
# quotes). Catches the common malformed-line cases (truncated object, stray text).
json_well_formed() {
  line="$1"
  # strip leading/trailing whitespace
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [ -n "$line" ] || return 1
  case "$line" in
    '{'*'}') : ;;     # must be a brace-wrapped object
    *) return 1 ;;
  esac
  # balanced quotes (count unescaped double-quotes; must be even)
  tmp="$line"
  tmp="${tmp//\\\"/}"           # drop escaped quotes
  q="${tmp//[!\"]/}"            # keep only quotes
  qn=${#q}
  [ $((qn % 2)) -eq 0 ] || return 1
  # balanced braces and brackets
  ob="${line//[!\{]/}"; cb="${line//[!\}]/}"
  [ "${#ob}" -eq "${#cb}" ] || return 1
  obk="${line//[!\[]/}"; cbk="${line//[!\]]/}"
  [ "${#obk}" -eq "${#cbk}" ] || return 1
  return 0
}

# extract_session_block — print the lines of the PF log belonging to the target
# session. If --session N given, slice from the heading matching "Session N" to
# the next session heading. Otherwise take the LAST session heading onward (the
# current session). Headings are markdown lines mentioning "Session <n>".
extract_session_block() {
  awk -v want="$SESSION" '
    function is_heading(l) { return (l ~ /[Ss]ession[ \t]+[0-9]+/) }
    {
      lines[NR] = $0
      if (is_heading($0)) {
        n = $0
        # extract the first integer after "session"
        match($0, /[Ss]ession[ \t]+[0-9]+/)
        s = substr($0, RSTART, RLENGTH)
        gsub(/[^0-9]/, "", s)
        hnum[++hc] = s
        hline[hc] = NR
      }
    }
    END {
      if (hc == 0) { for (i = 1; i <= NR; i++) print lines[i]; exit }
      start = 0; stop = NR + 1
      if (want != "") {
        for (i = 1; i <= hc; i++) if (hnum[i] == want) { start = hline[i]; if (i < hc) stop = hline[i+1]; break }
        if (start == 0) exit   # requested session not present -> empty block
      } else {
        start = hline[hc]      # last/current session heading
      }
      for (i = start; i < stop; i++) print lines[i]
    }
  ' "$PF"
}

# --- 1. validate every harvest.jsonl line; index by id ----------------------
# We build a newline-separated set of valid harvest ids.
HARVEST_IDS=""
lineno=0
while IFS= read -r hline || [ -n "$hline" ]; do
  lineno=$((lineno + 1))
  # skip blank lines (a trailing newline is not a record)
  case "$hline" in
    '' ) continue ;;
    \#* ) continue ;;   # tolerate comment lines
  esac
  if ! json_well_formed "$hline"; then
    # BUG-1 (F-017 harvest ledger): a malformed JSONL line is an unmineable record —
    # the analyst silently drops it, so the failure it was meant to carry is lost.
    # A presence-only gate would skip non-JSON noise and false-PASS; we FAIL on it.
    fail "harvest.jsonl line ${lineno} is not well-formed JSON: ${hline}"
    continue
  fi
  missing=""
  for req in id class source_refs detection_mode; do
    json_has_field "$hline" "$req" || missing="${missing} ${req}"
  done
  # recurrence: schema key is recurrence_count; accept either for portability.
  if ! json_has_field "$hline" "recurrence_count" && ! json_has_field "$hline" "recurrence"; then
    missing="${missing} recurrence"
  fi
  if [ -n "$missing" ]; then
    fail "harvest.jsonl line ${lineno} missing required field(s):${missing}"
    continue
  fi
  # extract the id value: "id"\s*:\s*"VALUE"
  hid="$(printf '%s\n' "$hline" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  if [ -z "$hid" ]; then
    fail "harvest.jsonl line ${lineno} has an empty/unparseable id value"
    continue
  fi
  HARVEST_IDS="${HARVEST_IDS}
${hid}"
done < "$HARVEST"

# bead reference test: does issues.jsonl mention this id anywhere (a bead that
# references the failure id in any field)?
bead_references() {
  grep -qF -- "$1" "$BEADS"
}

harvest_has() {
  printf '%s\n' "$HARVEST_IDS" | grep -qxF -- "$1"
}

# --- 2. for each PF failure id in the session, require all 3 layers ----------
# PF failure ids look like FAIL-<PROJECT>-<NNN> or PF-S<n>-<nn>. We extract any
# token matching those shapes from the current-session block.
SESSION_BLOCK="$(extract_session_block)"

PF_IDS="$(printf '%s\n' "$SESSION_BLOCK" \
  | grep -oE '(FAIL-[A-Z0-9]+-[0-9]+|PF-S[0-9]+-[0-9]+)' \
  | sort -u)"

if [ -z "$PF_IDS" ]; then
  # No failures recorded this session is a legitimate clean state — nothing to
  # harvest. (This is NOT a couldn't-run skip: the PF log was read fine.)
  emit "no session failure ids found in PF log${SESSION:+ (session ${SESSION})} — nothing to gate"
else
  while IFS= read -r pfid; do
    [ -n "$pfid" ] || continue
    miss_layers=""
    harvest_has "$pfid"     || miss_layers="${miss_layers} harvest.jsonl"
    bead_references "$pfid" || miss_layers="${miss_layers} issues.jsonl(bead)"
    if [ -n "$miss_layers" ]; then
      # BUG-2 (F-017 three-layer capture): a failure present in PF but missing from a
      # downstream layer falls out of the self-improvement loop. Fail-closed.
      fail "PF session failure '${pfid}' not captured in:${miss_layers}"
    else
      emit "ok: ${pfid} present in PF + harvest.jsonl + a bead"
    fi
  done <<EOF
$PF_IDS
EOF
fi

verdict
