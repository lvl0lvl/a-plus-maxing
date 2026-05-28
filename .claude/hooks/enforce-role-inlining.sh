#!/usr/bin/env bash
# enforce-role-inlining.sh — PreToolUse hook for Task tool dispatches.
#
# Implements INV-ROLE-INLINING from the project Invariants Register.
# Blocks dispatches that look like role-tagged agents (H1 matches '# {Role
# Name}' OR path reference to a roles/<slug>/agent.md file) but omit the
# canonical 11-section role profile.
#
# General-purpose / verifier / skill-internal dispatches (no role H1, no
# roles/<slug>/agent.md reference) pass through unblocked.
#
# Exit 0  = allow tool call
# Exit 2  = block (stderr is shown to the dispatching agent)
#
# Rationale: Rigor Framework Discipline 9, Pattern 3 (Mechanical Enforcement
# of Inlining). PF-S2-01 / PF-S3-01 demonstrate that the orchestrator
# under-uses role profiles even when CLAUDE.md mandates them; mechanical
# enforcement at PreToolUse closes the gap.

set -euo pipefail

# Read full stdin payload from Claude Code hook system
input=$(cat)

# Extract tool_input.prompt via python3 (jq may not be installed everywhere).
# Falls through cleanly if payload doesn't have the expected shape.
prompt=$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print(d.get('tool_input', {}).get('prompt', ''))
except Exception:
    pass
" <<< "$input")

# Empty prompt → not our concern; allow.
[[ -z "$prompt" ]] && exit 0

# Detect role-context. Two triggers:
#   (a) H1 matches '# {Capitalized Words}' on its own line (e.g., '# Architect',
#       '# Senior Engineer'). Digits/lowercase-first-letter words reject (so
#       '# Phase 3 retrieval agent' does NOT trigger).
#   (b) Prompt body references a roles/<slug>/agent.md path.
if ! echo "$prompt" | grep -qE '^# [A-Z][a-zA-Z]+( [A-Z][a-zA-Z]+){0,4}$|roles/[a-z-]+/agent\.md'; then
    exit 0
fi

# Role-context detected. Require all 11 canonical sections.
#
# The 9th-section "operational slot" varies by role per the actual content of
# ~/Documents/Projects/skills_library/roles/<slug>/agent.md:
#   - ## Modes              (architect, design-critic, qa, senior-engineer, ui-designer)
#   - ## Audit Protocol     (security)
#   - ## Task Routing       (orchestrator)
# Hook v2.5 (S12) accepts any one of these as the operational-slot equivalent
# rather than requiring '## Modes' literally. This closes E1 recurrence=3
# (PF: S9 architect / S10 path-pattern / S11 security profile blocked).
REQUIRED=(
    "## Identity"
    "## Core Rules"
    "## Role Boundaries"
    "## Ask vs Proceed"
    "## Loop-Breaking"
    "## Tools"
    "## Communication"
    "## Context Loading"
    "## Anti-Patterns"
    "## Negative Examples"
)
OPERATIONAL_SLOT_SYNONYMS=(
    "## Modes"
    "## Audit Protocol"
    "## Task Routing"
)

missing=()
for section in "${REQUIRED[@]}"; do
    grep -qF "$section" <<< "$prompt" || missing+=("$section")
done

# Operational slot: pass if ANY synonym is present.
slot_found=0
for syn in "${OPERATIONAL_SLOT_SYNONYMS[@]}"; do
    if grep -qF "$syn" <<< "$prompt"; then
        slot_found=1
        break
    fi
done
if [ "$slot_found" -eq 0 ]; then
    missing+=("operational-slot (one of: ${OPERATIONAL_SLOT_SYNONYMS[*]})")
fi

if [ ${#missing[@]} -gt 0 ]; then
    {
        echo "BLOCK: Role profile not fully inlined (INV-ROLE-INLINING)."
        echo ""
        echo "Dispatch matched role-context (H1 = '# {Role Name}' or roles/<slug>/agent.md)"
        echo "but is missing canonical sections:"
        for s in "${missing[@]}"; do echo "  - $s"; done
        echo ""
        echo "The 9th-section operational slot accepts any one of:"
        for syn in "${OPERATIONAL_SLOT_SYNONYMS[@]}"; do echo "  - $syn"; done
        echo "per the actual section names used across skills_library/roles/*/agent.md."
        echo ""
        echo "Required: paste the COMPLETE 11-section role profile verbatim from"
        echo "  ~/Documents/Projects/skills_library/roles/<role-slug>/agent.md"
        echo ""
        echo "Do NOT paraphrase, summarize, or abbreviate. The system prompt's"
        echo "'be concise' bias does NOT apply to role profiles — they are"
        echo "load-bearing reasoning frameworks, not prose to optimize."
        echo ""
        echo "See: CLAUDE.md 'Agent Role Profile Mandate' + Rigor Framework"
        echo "Discipline 9 + PF-S2-01 / PF-S3-01."
    } >&2
    exit 2
fi

exit 0
