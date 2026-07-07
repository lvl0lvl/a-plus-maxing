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
#                 last/current session section found in the PF log. Projects whose
#                 PF log has NO "Session N" headings (e.g. a date-keyed log) simply
#                 omit --session: the whole file is scanned as one block.
#
# ENV OVERRIDES (so non-numbered-session / date-keyed projects can gate honestly):
#   HARVEST_PF_ID_PATTERN   grep -oE alternation for the failure-id shapes to gate.
#       Default: (FAIL-[A-Z0-9]+-[0-9]+|PF-S[0-9]+-[0-9]+)
#       A date-keyed project sets e.g. (FAIL-[A-Z0-9]+-[0-9]+|PF-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]+).
#   HARVEST_SESSION_PATTERN awk ERE for a session heading line (used to slice the
#       --session block). Default: [Ss]ession[ \t]+[0-9]+
#
#   WHY THIS MATTERS (cross-deployment finding CF-1, F-008): the id pattern was
#   hardwired to the numbered-session scheme. A date-keyed PF log (ids like
#   PF-2026-06-04-03, no "Session N" headings) matched ZERO ids, so the gate took
#   its "nothing to gate" branch and PASSed (exit 0) WITHOUT enforcing anything — a
#   vacuous pass / false-green, the exact disease this gate exists to prevent. The
#   empty-id branch now distinguishes "genuinely clean" from "couldn't gate this
#   id scheme" and fails CLOSED (skipped -> FATAL) on the latter (see below).
#
# EXIT: 0 PASS (every PF failure captured in all 3 layers) / 1 FAIL (a failure
#       missing from a layer, or a malformed harvest line) / 2 FATAL (bad args /
#       unreadable input, OR the PF block carries failure-id-shaped tokens the
#       active id pattern cannot match — a check that cannot run does not pass).
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

# --- configurable id / session patterns (CF-1) -------------------------------
# Defaults preserve the historical numbered-session behavior exactly.
HARVEST_PF_ID_PATTERN="${HARVEST_PF_ID_PATTERN:-(FAIL-[A-Z0-9]+-[0-9]+|PF-S[0-9]+-[0-9]+)}"
HARVEST_SESSION_PATTERN="${HARVEST_SESSION_PATTERN:-[Ss]ession[ \t]+[0-9]+}"

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
  awk -v want="$SESSION" -v hpat="$HARVEST_SESSION_PATTERN" '
    function is_heading(l) { return (l ~ hpat) }
    {
      lines[NR] = $0
      if (is_heading($0)) {
        n = $0
        # extract the first integer in the matched session heading
        match($0, hpat)
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
# PF failure ids match HARVEST_PF_ID_PATTERN (default FAIL-<PROJECT>-<NNN> or
# PF-S<n>-<nn>). We extract any token matching that shape from the current-session
# block — but ONLY from this-session DECLARATION context, not from prior-failure
# references.
SESSION_BLOCK="$(extract_session_block)"

# BUG-4 (CF-1 over-extraction, a-plus #8): the PF template carries a
# `Recurrence: <prior-ids>` field, and a "No new PF" close may attest a prior id.
# Greping EVERY id token in the block then false-FAILs: the gate demands a harvest
# record + bead for a failure that is NOT this session's. So ids that occur ONLY on a
# prior/recurrence-reference line are dropped; an id that also appears on a
# non-reference (declaration) line is kept (the `grep -Ev` below realizes this set
# logic — a declaration line survives the filter, so its id is still extracted).
#
# BUG-6 (W1-5, 2026-07-02): the prior REF_RE matched the reference keyword ANYWHERE
# in a line, so a genuine this-session PF entry whose TITLE/body merely MENTIONED
# one of those words (safety PF-S11-01 — a PF *about* the recurrence filter; its
# heading contained "recurrence") had its whole declaration line dropped and was
# NEVER gated — a silent FALSE-PASS in a fail-closed gate, the exact disease this
# gate exists to prevent (it left PF-S5-02 / PF-S8-01 historically ungated). Fix: a
# line is a prior-REFERENCE only when it LEADS with a reference FIELD LABEL
# (`Recurrence:` / `Superseded:` / `Prior`, after optional indent / list-marker /
# bold) AND the keyword ends on a word boundary — `([^A-Za-z]|:|$)`, so "Priority"/
# "Prioritize" do NOT prefix-match "Prior" (BUG-6 review, 2026-07-02: dropping that
# trailing boundary let a `- Priority: … PF-Sn-nn …` declaration be misread as a
# reference and false-PASS). A declaration heading or `- <id>:` entry never leads with
# such a label, so its id is always gated even if its title says "recurrence". (KNOWN
# RESIDUAL: a standalone `- <id> HELD` prior reference with NO leading Recurrence label
# is treated as a declaration and gated — a SAFE false-FAIL the operator resolves by
# moving it into a `Recurrence:` field, the documented a-plus #8 mitigation. The
# dangerous false-PASS direction is NARROWED, not fully closed: a genuine declaration
# whose line LEADS with the bare word "Prior"/"Recurrence" as prose is still dropped —
# same as before this change, pre-existing, not introduced here.)
REF_RE='^[[:space:]]*([-*>][[:space:]]*)*(\*\*)?([Rr]ecurrence|[Ss]upersed(e|ed|es)|[Pp]rior)([^A-Za-z]|:|$)'

# ids appearing on any non-reference line (genuine this-session declarations)
PF_IDS="$(printf '%s\n' "$SESSION_BLOCK" \
  | grep -Ev "$REF_RE" \
  | grep -oE "$HARVEST_PF_ID_PATTERN" \
  | sort -u)"

if [ -z "$PF_IDS" ]; then
  # The active id pattern matched nothing in the declaration lines. Two cases —
  # and they are NOT the same (CF-1 / F-008):
  #   (a) genuinely clean: the block contains NO failure-id-shaped token at all
  #       -> legitimately nothing to gate -> PASS.
  #   (b) couldn't gate: the block DOES carry a failure-id-shaped token (PF-/FAIL-
  #       hyphen prefix) that the ACTIVE pattern did not match — e.g. a date-form id
  #       PF-2026-06-04-03 under the default numbered-session pattern. This is the
  #       vacuous-pass trap: it must be LOUD and fail-closed, not read as clean.
  # Conservative "looks like a failure id" probe: require the PF-/FAIL- hyphen
  # prefix shape (NOT the bare words "PF"/"failure" in prose). Then subtract the
  # ids the active pattern already matched anywhere in the block.
  MATCHED_ANY="$(printf '%s\n' "$SESSION_BLOCK" \
    | grep -oE "$HARVEST_PF_ID_PATTERN" | sort -u)"
  LOOKS_LIKE="$(printf '%s\n' "$SESSION_BLOCK" \
    | grep -oE '(PF-[A-Za-z0-9-]+|FAIL-[A-Za-z0-9-]+)' | sort -u)"
  UNMATCHED="$(comm -23 \
    <(printf '%s\n' "$LOOKS_LIKE" | grep -v '^$' | sort -u) \
    <(printf '%s\n' "$MATCHED_ANY" | grep -v '^$' | sort -u))"
  if [ -n "$UNMATCHED" ]; then
    # case (b): cannot honestly gate this id scheme.
    unmatched_flat="$(printf '%s' "$UNMATCHED" | tr '\n' ' ')"
    skipped "PF block carries failure-id-shaped token(s) the active id pattern did not match:${unmatched_flat:+ }${unmatched_flat}— set HARVEST_PF_ID_PATTERN to this project's id scheme (this gate cannot honestly gate it as-is)"
  else
    # case (a): genuinely clean. The PF log was read fine — NOT a couldn't-run skip.
    emit "no session failure ids found in PF log${SESSION:+ (session ${SESSION})} — nothing to gate"
  fi
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
