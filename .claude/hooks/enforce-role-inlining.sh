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
CANONICAL=(
    "## Identity"
    "## Core Rules"
    "## Role Boundaries"
    "## Ask vs Proceed"
    "## Loop-Breaking"
    "## Tools"
    "## Communication"
    "## Context Loading"
    "## Modes"
    "## Anti-Patterns"
    "## Negative Examples"
)

missing=()
for section in "${CANONICAL[@]}"; do
    grep -qF "$section" <<< "$prompt" || missing+=("$section")
done

if [ ${#missing[@]} -gt 0 ]; then
    {
        echo "BLOCK: Role profile not fully inlined (INV-ROLE-INLINING)."
        echo ""
        echo "Dispatch matched role-context (H1 = '# {Role Name}' or roles/<slug>/agent.md)"
        echo "but is missing canonical sections:"
        for s in "${missing[@]}"; do echo "  - $s"; done
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
