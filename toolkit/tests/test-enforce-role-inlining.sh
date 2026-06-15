#!/usr/bin/env bash
# test-enforce-role-inlining.sh — negative test for the role-inlining hook.
#
# F-007 obligation: a guard that cannot prove it goes RED on bad input enforces
# nothing. This test feeds the hook PreToolUse JSON payloads on stdin and asserts:
#   GOOD  (full 11-section profile inlined)        -> exit 0 (allow)
#   BAD   (role-shaped but missing sections)        -> exit 2 (block)
#   NON-ROLE (bespoke prompt, no role H1 / agent.md)-> exit 0 (pass through)
#   F-002 (audit role using '## Audit Protocol' as  -> exit 0 (allow)
#         the operational slot instead of '## Modes')
#     This is the exact false-GREEN-inverse the F-002 fix prevents: the old
#     literal '## Modes' check false-BLOCKED this valid profile. We assert it
#     is allowed so a regression to the hardcoded header is caught.
#
# Uses the toolkit test harness (../lib/test-lib.sh).

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
HOOK="${HERE}/../hooks/enforce-role-inlining.sh"
# Fixtures are generated scratch (not committed): write to a throwaway temp dir so
# running the suite never dirties the tracked tree (skill_consolidator-oas).
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# shellcheck source=../lib/test-lib.sh
. "${HERE}/../lib/test-lib.sh"

# --- Build the canonical 11-section profile body (reused by fixtures) --------
# 10 fixed sections + operational slot. We emit it as the Task prompt.
profile_body() {
  local slot="$1"
  cat <<EOF
# Verifier Agent

## Identity
You verify claims.

## Core Rules
Be rigorous.

## Role Boundaries
Stay in lane.

## Ask vs Proceed
Ask when blocked.

## Loop-Breaking
Escalate after 3 tries.

## Tools
Read, Grep, Bash.

${slot}
Operational behavior here.

## Communication
Terse.

## Context Loading
Load on demand.

## Anti-Patterns
No hand-waving.

## Negative Examples
Bad: skipping verification.
EOF
}

# json_payload <prompt-text> — wrap a prompt into a PreToolUse Task JSON payload.
# Uses jq if present for correct escaping; else python3; else a manual escape.
json_payload() {
  local p="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -n --arg p "$p" '{tool_name:"Task", tool_input:{prompt:$p}}'
  elif command -v python3 >/dev/null 2>&1; then
    P="$p" python3 -c 'import json,os; print(json.dumps({"tool_name":"Task","tool_input":{"prompt":os.environ["P"]}}))'
  else
    local esc
    esc=$(printf '%s' "$p" | sed -E 's/\\/\\\\/g; s/"/\\"/g' | awk 'BEGIN{ORS=""}{print (NR>1?"\\n":"") $0}')
    printf '{"tool_name":"Task","tool_input":{"prompt":"%s"}}' "$esc"
  fi
}

# --- Fixtures ----------------------------------------------------------------

# GOOD: full profile, operational slot = '## Modes'.
json_payload "$(profile_body "## Modes")" > "${FIX}/good.json"

# BAD: role-shaped (has role H1) but missing several required sections.
json_payload "$(cat <<'EOF'
# Verifier Agent

## Identity
You verify claims.

## Core Rules
Be rigorous.
EOF
)" > "${FIX}/bad-missing-sections.json"

# BAD-2: references roles/<slug>/agent.md (role-shaped) but inlines NOTHING.
json_payload "Please act per roles/verifier/agent.md and check the build." \
  > "${FIX}/bad-agentmd-ref.json"

# NON-ROLE: bespoke prompt, no role H1, no agent.md ref -> must pass through.
json_payload "Gather the failing test names and summarize them." \
  > "${FIX}/non-role.json"

# F-002: audit role whose operational slot is '## Audit Protocol' (a synonym).
# Old literal '## Modes' check would FALSE-BLOCK this. Must be allowed.
json_payload "$(profile_body "## Audit Protocol")" > "${FIX}/good-audit-slot.json"

# F-002b: '## Task Routing' synonym likewise must be allowed.
json_payload "$(profile_body "## Task Routing")" > "${FIX}/good-routing-slot.json"

# F-019 (S4): an UNEXPANDED Mode-B by-reference template — role-shaped, carries the
# sanctioned marker, but the profile is NOT inlined — must STILL be DENIED (exit 2).
# The marker NEVER relaxes runtime enforcement (INV-PROFILE-INLINING). If the hook
# were wrongly made to "honor" the marker as a pass (the F-007 hole), this turns
# GREEN — so this is the load-bearing guard for the two-object contract.
json_payload "$(cat <<'EOF'
# Senior Engineer

[role-ref: sanctioned roles/senior-engineer/agent.md]
(Mode-B template not yet expanded — full profile NOT inlined here.)
EOF
)" > "${FIX}/bad-unexpanded-marker.json"

# --- Assertions --------------------------------------------------------------

# Core negative-test obligation: GOOD allowed (0), BAD blocked (non-zero).
assert_red_when_guard_removed \
  "bash '${HOOK}' < '${FIX}/good.json'" \
  "bash '${HOOK}' < '${FIX}/bad-missing-sections.json'"

# Explicit exit-code checks.
expect_exit 0 bash "${HOOK}" < "${FIX}/good.json"
expect_exit 2 bash "${HOOK}" < "${FIX}/bad-missing-sections.json"
expect_exit 2 bash "${HOOK}" < "${FIX}/bad-agentmd-ref.json"
expect_exit 0 bash "${HOOK}" < "${FIX}/non-role.json"

# F-002 regression guards: synonym operational slots must be ALLOWED.
expect_exit 0 bash "${HOOK}" < "${FIX}/good-audit-slot.json"
expect_exit 0 bash "${HOOK}" < "${FIX}/good-routing-slot.json"

# F-019 (S4): unexpanded Mode-B marker without the profile is STILL DENIED.
expect_exit 2 bash "${HOOK}" < "${FIX}/bad-unexpanded-marker.json"

# F-019 (S4): and the DENY carries the targeted "unexpanded template" diagnostic
# (not the opaque "missing ## Identity" message) — the shipped behavior is asserted.
assert_stderr_contains 'UNEXPANDED by-reference/EMBED marker' bash "${HOOK}" < "${FIX}/bad-unexpanded-marker.json"

# Empty / non-JSON stdin must not crash; allow (nothing to check).
expect_exit 0 bash "${HOOK}" < /dev/null

test_summary
