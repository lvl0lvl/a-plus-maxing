#!/usr/bin/env bash
# enforce-role-inlining.sh — PreToolUse/Task hook (rigor toolkit, canonical).
#
# ENFORCES: INV-PROFILE-INLINING. When an agent dispatches a Task that *looks*
# like a role-tagged sub-agent — i.e. the prompt carries a role H1
# ('# {Role Name}') OR references a 'roles/<slug>/agent.md' profile path — the
# FULL canonical role profile must be inlined verbatim, not paraphrased or
# referenced by path. Dispatches that are not role-shaped (bespoke
# gatherer/verifier/analyst prompts with no role H1 and no agent.md ref) pass
# through untouched.
#
# A canonical role profile has 11 sections: 10 fixed headers plus a single
# 9th "operational slot" whose header varies by role family. The fixed 10 are
# required literally; the operational slot is satisfied by ANY ONE of the
# accepted synonyms (default: '## Modes' | '## Audit Protocol' | '## Task
# Routing').
#
# EXIT SEMANTICS (PreToolUse hook contract):
#   0 = allow the dispatch.
#   2 = BLOCK the dispatch; stderr is surfaced to the dispatching agent.
#   (Other non-zero -> treated by the harness as a non-blocking hook error.)
# This mirrors the toolkit's 0=PASS / 2=FATAL-gate convention: a role dispatch
# we cannot certify as fully inlined is fail-closed (blocked), not waved through.
#
# SOURCE LINEAGE: generalized from this project's own
# .claude/hooks/enforce-role-inlining.sh (v2.5), itself modeled on the
# battle-tested a-plus-maxing v2.5 hook.
#
# BUG / FINDING NOTES CARRIED FORWARD:
#   F-002 (operational-slot synonyms): an earlier hook hard-checked the literal
#     '## Modes' header. Audit/router roles legitimately use '## Audit Protocol'
#     or '## Task Routing' in that slot, so the literal check false-BLOCKED valid
#     fully-inlined profiles (recurrence=3). FIX: accept any one synonym for the
#     operational slot. The canonical framework's example hook (Discipline 9,
#     Pattern 3) still hardcodes '## Modes' and is subtly wrong here.
#
# GENERALIZATION NOTES (vs. the project-local source):
#   - No hardcoded project paths. JSON field extraction is portable.
#   - JSON parsing degrades gracefully: jq -> python3 -> a pure-shell fallback,
#     so the hook is usable on hosts without python3 or jq.
#   - Required sections, synonyms, the role-H1 regex, and the agent.md path
#     pattern are all overridable via environment (see CONFIG below) so the same
#     hook serves frameworks whose canonical profile differs.
#   - Portable across BSD (macOS) and GNU userlands: POSIX grep -E only, no
#     GNU-only flags, no process substitution dependence beyond bash here-strings.

set -euo pipefail

# Dep preflight (bead skills_library-kfi): a missing grep/sed/tr makes the
# role-detection greps fail, which reads as "not a role dispatch" → silent ALLOW
# of an un-inlined role prompt. A gate whose matcher cannot run must fail CLOSED
# instead (F-008). `command -v` is a bash builtin, so the preflight itself needs
# none of the tools it checks.
for _dep in grep sed tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "enforce-role-inlining: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

# ---------------------------------------------------------------------------
# CONFIG (all overridable via environment) ----------------------------------
# ---------------------------------------------------------------------------

# Fixed sections that MUST appear literally (the 10 non-slot headers).
# Override by exporting ROLE_REQUIRED_SECTIONS as a newline-separated list.
if [ -n "${ROLE_REQUIRED_SECTIONS:-}" ]; then
  IFS=$'\n' read -r -d '' -a REQUIRED <<< "${ROLE_REQUIRED_SECTIONS}" || true
else
  REQUIRED=(
    "## Identity" "## Core Rules" "## Role Boundaries" "## Ask vs Proceed"
    "## Loop-Breaking" "## Tools" "## Communication" "## Context Loading"
    "## Anti-Patterns" "## Negative Examples"
  )
fi

# The single operational slot — satisfied by ANY ONE of these synonyms (F-002).
# Override via ROLE_OPERATIONAL_SLOT_SYNONYMS (newline-separated).
if [ -n "${ROLE_OPERATIONAL_SLOT_SYNONYMS:-}" ]; then
  IFS=$'\n' read -r -d '' -a OPERATIONAL_SLOT_SYNONYMS <<< "${ROLE_OPERATIONAL_SLOT_SYNONYMS}" || true
else
  OPERATIONAL_SLOT_SYNONYMS=( "## Modes" "## Audit Protocol" "## Task Routing" )
fi

# Detection patterns (POSIX ERE). A dispatch is "role-shaped" if EITHER matches.
# NOTE: the H1 default is assigned WITHOUT a `${VAR:-default}` one-liner because
# an escaped end-anchor (\$) inside a double-quoted ':-' default is mangled by
# the shell (the trailing $ migrates inside the {0,4} repeat -> "invalid
# repetition count" on BSD/ugrep). Build it in two steps to keep the anchor.
if [ -z "${ROLE_H1_REGEX:-}" ]; then
  ROLE_H1_REGEX='^# [A-Z][a-zA-Z]+( [A-Z][a-zA-Z]+){0,4}$'
fi
ROLE_AGENTMD_REGEX="${ROLE_AGENTMD_REGEX:-roles/[a-z0-9-]+/agent\.md}"

# Recognized UNEXPANDED by-reference / EMBED template markers (F-019 two-object
# contract, S4). This hook judges the RUNTIME object: a real Task dispatch MUST
# contain the fully-inlined profile. The marker NEVER relaxes that — runtime
# dispatches are always full-inline (INV-PROFILE-INLINING). Its only use here is a
# TARGETED diagnostic: a denied dispatch still carrying the marker means the
# orchestrator pasted a Mode-B template instead of EXPANDING it, so we say exactly
# that instead of an opaque "missing ## Identity ...". The consistency-audit is the
# layer that certifies the STATIC template (sanctioned + resolvable); the hook
# certifies the dispatch is inlined. Together they reconcile, not contradict.
ROLE_BYREF_MARKER_REGEX="${ROLE_BYREF_MARKER_REGEX:-(INLINE-EXEMPT|by-reference: sanctioned|role-ref: sanctioned|EMBED .*read from)}"

INV_ID="${ROLE_INV_ID:-INV-PROFILE-INLINING}"

# ---------------------------------------------------------------------------
# Read hook payload from stdin ----------------------------------------------
# ---------------------------------------------------------------------------
input="$(cat)"

# extract_prompt — pull tool_input.prompt (fallback tool_input.description) out
# of the PreToolUse JSON payload, using whatever parser is available.
extract_prompt() {
  local raw="$1"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$raw" | jq -r \
      '(.tool_input.prompt // .tool_input.description // "")' 2>/dev/null && return 0
  fi
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "$raw" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
    ti = d.get("tool_input", {}) or {}
    print(ti.get("prompt", "") or ti.get("description", ""))
except Exception:
    pass
' 2>/dev/null && return 0
  fi
  # Pure-shell last resort: best-effort extraction of "prompt"/"description".
  # Not a full JSON parser; conservative — only used when neither tool exists.
  printf '%s' "$raw" \
    | tr -d '\n' \
    | grep -oE '"(prompt|description)"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' \
    | head -n1 \
    | sed -E 's/^"(prompt|description)"[[:space:]]*:[[:space:]]*"//; s/"$//' \
    | sed -E 's/\\n/\n/g; s/\\"/"/g; s/\\\\/\\/g'
}

prompt="$(extract_prompt "$input")"

# Nothing to check -> allow.
[ -z "$prompt" ] && exit 0

# ---------------------------------------------------------------------------
# Detect role-context -------------------------------------------------------
# ---------------------------------------------------------------------------
# Check each pattern separately: combining an anchored H1 regex (ending in $)
# with the agent.md alternation into one ERE breaks BSD grep ("invalid
# repetition count(s)") because the mid-pattern $ collides with the following
# alternation. Two greps are also clearer and equally portable.
is_role=0
printf '%s\n' "$prompt" | grep -qE "${ROLE_H1_REGEX}" && is_role=1
printf '%s\n' "$prompt" | grep -qE "${ROLE_AGENTMD_REGEX}" && is_role=1
if [ "$is_role" -eq 0 ]; then
  # Not a role dispatch — pass through.
  exit 0
fi

# ---------------------------------------------------------------------------
# Require the canonical sections --------------------------------------------
# ---------------------------------------------------------------------------
missing=()
for section in "${REQUIRED[@]}"; do
  grep -qF "$section" <<< "$prompt" || missing+=("$section")
done

# Operational slot: any one synonym satisfies it (F-002).
slot_ok=0
for slot in "${OPERATIONAL_SLOT_SYNONYMS[@]}"; do
  if grep -qF "$slot" <<< "$prompt"; then
    slot_ok=1
    break
  fi
done
if [ "$slot_ok" -eq 0 ]; then
  # Render the synonym set in the diagnostic so the dispatcher knows the options.
  synonyms_joined="$(printf '%s / ' "${OPERATIONAL_SLOT_SYNONYMS[@]}")"
  synonyms_joined="${synonyms_joined% / }"
  missing+=("operational slot (one of: ${synonyms_joined})")
fi

if [ "${#missing[@]}" -gt 0 ]; then
  {
    echo "ROLE PROFILE NOT FULLY INLINED (${INV_ID})."
    echo "This dispatch is role-shaped (role H1 or roles/<slug>/agent.md ref) but"
    echo "the inlined profile is missing required section(s):"
    for m in "${missing[@]}"; do
      echo "  - ${m}"
    done
    if printf '%s\n' "$prompt" | grep -qE "$ROLE_BYREF_MARKER_REGEX"; then
      echo "NOTE: this dispatch still carries an UNEXPANDED by-reference/EMBED marker."
      echo "Mode B (sanctioned by-reference) templates must be EXPANDED before dispatch:"
      echo "read the referenced roles/<slug>/agent.md and paste the FULL profile inline"
      echo "here. The marker is a static-template construct; a runtime dispatch is"
      echo "always full-inline (${INV_ID})."
    else
      echo "Paste the COMPLETE role profile verbatim. Do NOT paraphrase, abbreviate,"
      echo "or reference it by path."
    fi
  } >&2
  exit 2
fi

exit 0
