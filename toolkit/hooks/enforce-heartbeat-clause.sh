#!/usr/bin/env bash
# enforce-heartbeat-clause.sh — PreToolUse/Task hook enforcing a heartbeat /
# liveness clause on every agent dispatch. The "0-silent-drops" primitive.
#
# WHAT IT ENFORCES
#   When an orchestrator dispatches a sub-agent (the Task / Agent tool), the
#   dispatch prompt MUST inline a heartbeat/liveness clause so the agent emits a
#   poll-able status. Without it, a silent drop (auth-401, zero-byte completion,
#   wedged background job) is invisible until a human notices — "no output" reads
#   as "still working," not "dead." This hook makes the liveness clause a
#   structural precondition of dispatch: missing clause => DENY (fail-closed).
#
#   This is the hook-protocol sibling of the F-008 audit rule ("couldn't verify"
#   != "verified clean"): a dispatch that cannot be observed must not be treated
#   as a dispatch that is healthy. Fail-closed is the default; the operator must
#   add the clause, not the hook must guess intent.
#
# CDM / FINDING LINEAGE
#   Source: Quant .claude/hooks/enforce-heartbeat-clause.sh — mechanical
#   enforcement of heartbeat-polling discipline, originating finding PD-S200-01
#   (silent agent drops detected only by user intervention, hours late;
#   re-observed PD-S200-02, PF-S216-01). Related framework finding: F-008
#   (fail-closed when verification cannot run).
#
# GENERALIZED AWAY FROM SOURCE (what was DROPPED and why)
#   The source hard-pinned Quant-project specifics. Removed / parameterized:
#     - Pinned canonical-clause sha256 + absolute path into a user-local memory
#       file (~/.claude/projects/.../feedback_agent_heartbeat_emission.md). The
#       hash goes stale the moment the clause is edited; it is project archaeology,
#       not a portable mechanism. DROPPED.
#     - The exact heartbeat-file format (heartbeat-<name>.jsonl, the JSON record
#       schema, `heartbeat_record_count` token, `wc -l` attestation). These are
#       ONE valid liveness convention, not THE convention. Kept the GENERAL
#       requirement (a liveness clause + drop/re-dispatch semantics); the precise
#       tokens are now parameterized via HEARTBEAT_MARKER_RE / _LABEL so each
#       adopting project pins its own convention. Sane defaults below match the
#       common "heartbeat file + final-reply count + re-dispatch on miss" pattern.
#     - Quant PD/PF incident IDs inside the DENY reason text. Kept a neutral
#       explanation of the failure mode.
#
# BUG-N NOTES CARRIED FORWARD
#   BUG-1 (fail-closed on parse error): malformed JSON on stdin => DENY, never
#     allow-through. Carried from source (matches sibling enforce-role-inlining).
#   BUG-2 (jq absence is fail-closed): if jq is unavailable the hook cannot read
#     the prompt; per F-008 it must NOT silently allow. It DENYs with a clear
#     env-error reason. (Source assumed jq present; generalized to be explicit.)
#   BUG-3 (parallel marker arrays, not a delimited string): the drop-detection
#     regex contains a literal `|` (alternation), so markers are stored as
#     parallel regex/label arrays — never split on an in-band delimiter. Carried
#     from source.
#   BUG-4 (empty-prompt passthrough): an empty/absent prompt is not an agent
#     dispatch we can gate, so it is allowed (exit 0) rather than denied — denying
#     would break non-dispatch tool calls routed through the same matcher.
#
# CONTRACT
#   PreToolUse hook protocol: reads hook JSON on stdin, writes a
#   hookSpecificOutput decision on stdout, always exits 0 (the DECISION, not the
#   exit code, gates the tool). This is a hook, not a sourced audit, so it does
#   NOT source lib/audit-helpers.sh — that library's verdict()/exit-code grammar
#   is for standalone audits. The fail-closed PRINCIPLE from audit-helpers (F-008)
#   is honored here via DENY-on-cannot-verify.
#
# CONFIG (env, all optional — portable BSD+GNU, no project paths)
#   HEARTBEAT_PROMPT_FIELD   jq path to the prompt within tool_input
#                            (default: .tool_input.prompt)
#   HEARTBEAT_MARKER_RE      newline-separated ERE patterns, ALL required
#   HEARTBEAT_MARKER_LABEL   newline-separated human labels (1:1 with _RE)
#   HEARTBEAT_CLAUSE         canonical clause body echoed in the DENY reason so
#                            the operator can paste it without re-reading a doc
#
# PORTABILITY: POSIX grep -qE; no GNU-only flags; bash 3.2 compatible (arrays
# only, no associative arrays). Works on macOS/BSD and Linux/GNU.

set -euo pipefail

PROMPT_FIELD="${HEARTBEAT_PROMPT_FIELD:-.tool_input.prompt}"

# --- emit a PreToolUse decision and exit -----------------------------------
# Prefers jq for safe JSON encoding; that's also our stdin reader, so if jq is
# gone we fall back to a hand-rolled minimal-escape encoder for the deny path.
emit_decision() {
  decision="$1"; reason="$2"
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg d "$decision" --arg r "$reason" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: $d,
        permissionDecisionReason: $r
      }
    }'
  else
    # jq-less fallback: escape backslash, quote, newline, tab, CR.
    esc=$(printf '%s' "$reason" \
      | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' \
      | awk 'BEGIN{ORS=""} {if(NR>1)printf "\\n"; printf "%s",$0}' \
      | tr '\t' ' ')
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' \
      "$decision" "$esc"
  fi
  exit 0
}

# --- BUG-2: jq absence is fail-closed --------------------------------------
if ! command -v jq >/dev/null 2>&1; then
  emit_decision "deny" \
    "Heartbeat-clause hook cannot run: jq not found on PATH. Per fail-closed policy (F-008), a dispatch that cannot be verified is DENIED, not allowed. Install jq or fix PATH."
fi

# --- Read tool input (BUG-1: parse error is fail-closed) -------------------
if ! PROMPT=$(jq -r "${PROMPT_FIELD} // empty" < /dev/stdin 2>/dev/null); then
  emit_decision "deny" \
    "Heartbeat-clause hook input parse error (malformed JSON on stdin). Failing closed."
fi

# --- BUG-4: no prompt => not a gatable dispatch => allow -------------------
if [ -z "$PROMPT" ]; then
  exit 0
fi

# --- Required markers (parameterizable; BUG-3 parallel arrays) -------------
# Defaults capture the GENERAL liveness mechanism, not Quant's exact tokens:
#   1. a liveness/heartbeat clause is present at all
#   2. the agent must emit/append observable status as it works
#   3. drop-detection / re-dispatch semantics (the "0-silent-drops" teeth)
# A project that pins a stricter convention overrides via env (see header).
default_marker_re='([Hh]eartbeat|[Ll]iveness|[Kk]eep[- ]?alive)
([Ee]mit|[Aa]ppend|[Ww]rite|[Rr]eport|[Pp]oll|[Oo]utput).*(status|progress|heartbeat|update)
([Rr]e-?dispatch|[Pp]resume[ds]? (a )?drop|[Tt]reated? as (a )?drop|[Ss]ilent drop)'
default_marker_label='liveness/heartbeat clause heading
"emit/append observable status as you work" instruction
drop-detection / re-dispatch (presume-drop) semantics'

# Read markers into parallel arrays from env-or-default newline-separated lists.
MARKER_RE=()
MARKER_LABEL=()
while IFS= read -r _line; do
  [ -n "$_line" ] && MARKER_RE+=("$_line")
done <<EOF
${HEARTBEAT_MARKER_RE:-$default_marker_re}
EOF
while IFS= read -r _line; do
  [ -n "$_line" ] && MARKER_LABEL+=("$_line")
done <<EOF
${HEARTBEAT_MARKER_LABEL:-$default_marker_label}
EOF

# Defensive: if a project supplies mismatched RE/LABEL counts, fail closed —
# we cannot reliably report what is missing, so we cannot certify the dispatch.
if [ "${#MARKER_RE[@]}" -ne "${#MARKER_LABEL[@]}" ]; then
  emit_decision "deny" \
    "Heartbeat-clause hook misconfigured: HEARTBEAT_MARKER_RE has ${#MARKER_RE[@]} entries but HEARTBEAT_MARKER_LABEL has ${#MARKER_LABEL[@]}. Failing closed (F-008)."
fi

MISSING=()
for i in "${!MARKER_RE[@]}"; do
  if ! printf '%s\n' "$PROMPT" | grep -qE "${MARKER_RE[$i]}"; then
    MISSING+=("${MARKER_LABEL[$i]}")
  fi
done

# --- All markers present => allow ------------------------------------------
if [ "${#MISSING[@]}" -eq 0 ]; then
  exit 0
fi

# --- Build DENY reason -----------------------------------------------------
CLAUSE="${HEARTBEAT_CLAUSE:-$(cat <<'EOF'
## Heartbeat / liveness protocol (MANDATORY)

1. As your FIRST action, create a heartbeat/liveness record (e.g. a
   heartbeat-<agent-name>.jsonl file, or whatever this project pins).
2. After every distinct work or verification step, emit/append a one-line
   status record: {"ts":"<iso8601 UTC>","step":"<short desc>","progress":"<n/total>"}.
3. In your final reply, attest the observable-status count (e.g. include the
   heartbeat record count, matching `wc -l` of the heartbeat file).
4. If the heartbeat is not maintained, the orchestrator presumes a DROP and
   re-dispatches. No silent drops.
EOF
)}"

REASON="HEARTBEAT / LIVENESS CLAUSE NOT INLINED."
REASON+=$'\n'"Agent dispatch detected but the prompt is missing ${#MISSING[@]} required liveness marker(s):"
for label in "${MISSING[@]}"; do
  REASON+=$'\n'"  - ${label}"
done
REASON+=$'\n\n'"Every agent dispatch MUST inline a liveness clause so the agent emits poll-able status. Otherwise a silent drop (auth failure, zero-byte completion, wedged job) is invisible until a human notices. Paste this canonical clause into the dispatch prompt:"
REASON+=$'\n\n'"${CLAUSE}"
REASON+=$'\n\n'"Failing closed (F-008 / 0-silent-drops): a dispatch that cannot be observed is not certified healthy."

emit_decision "deny" "$REASON"
