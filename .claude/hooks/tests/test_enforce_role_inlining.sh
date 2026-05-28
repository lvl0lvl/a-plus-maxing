#!/usr/bin/env bash
# Smoke tests for enforce-role-inlining.sh.
# Run with: bash tests/test_enforce_role_inlining.sh
set -u  # no -e so we can run all tests and tally
HOOK="$(cd "$(dirname "$0")/.." && pwd)/enforce-role-inlining.sh"

pass=0
fail=0

assert_exit() {
    local name="$1" expected="$2" actual="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS  $name"
        pass=$((pass + 1))
    else
        echo "FAIL  $name — expected exit $expected, got $actual"
        fail=$((fail + 1))
    fi
}

make_payload() {
    # Usage: make_payload "<prompt>"
    python3 -c "import json, sys; print(json.dumps({'tool_input': {'prompt': sys.argv[1]}}))" "$1"
}

# T1: general-purpose verifier brief — no role H1. ALLOW.
make_payload "You are a Phase 4.75 integrity verifier. Read the corpus and check IC-1 through IC-13. Output gates/gate-4.75.md." | bash "$HOOK"
assert_exit "T1 general-purpose verifier passes" 0 $?

# T2: role H1 with FULL 11 sections. ALLOW.
FULL_PROFILE="# Senior Engineer
You are the Senior Engineer.
## Identity
You serve the codebase.
## Core Rules
1. Test first.
## Role Boundaries
I own X. I do NOT own Y.
## Ask vs Proceed
Ask when load-bearing.
## Loop-Breaking
Escape after 2 passes.
## Tools
Read / Edit / Bash.
## Communication
YAML output.
## Context Loading
3 refs max.
## Modes
Implementation / Review.
## Anti-Patterns
I don't ship without tests.
## Negative Examples
BAD: ... GOOD: ..."
make_payload "$FULL_PROFILE" | bash "$HOOK"
assert_exit "T2 full role profile passes" 0 $?

# T3: role H1 but MISSING sections. BLOCK.
BAD_PROFILE="# Senior Engineer
You are the Senior Engineer.
## Identity
You serve the codebase.
## Core Rules
1. Test first."
make_payload "$BAD_PROFILE" | bash "$HOOK" 2>/dev/null
assert_exit "T3 role H1 with missing sections blocks" 2 $?

# T4: roles/<slug>/agent.md path reference without inlined sections. BLOCK.
make_payload "Please follow ~/Documents/Projects/skills_library/roles/senior-engineer/agent.md and review the code." | bash "$HOOK" 2>/dev/null
assert_exit "T4 path-reference without inlining blocks" 2 $?

# T5: H1 with digits/lowercase ('# Phase 3 retrieval agent') — NOT role-context. ALLOW.
make_payload "# Phase 3 retrieval agent
You retrieve. No role profile needed." | bash "$HOOK"
assert_exit "T5 phase-style H1 does not trigger" 0 $?

# T6: empty prompt. ALLOW (not our concern).
make_payload "" | bash "$HOOK"
assert_exit "T6 empty prompt passes" 0 $?

# T7: malformed payload. ALLOW (defensive).
echo 'not-json' | bash "$HOOK"
assert_exit "T7 malformed payload passes" 0 $?

# T8: non-Task payload (Bash tool). No role-context, no prompt field. ALLOW.
echo '{"tool_input":{"command":"ls -la"}}' | bash "$HOOK"
assert_exit "T8 non-Task payload passes" 0 $?

# T9 (hook v2.5): security profile shape uses '## Audit Protocol' as operational slot. ALLOW.
SECURITY_PROFILE="# Security
You are the Security reviewer.
## Identity
You audit for vulnerabilities.
## Core Rules
1. Trust nothing.
## Role Boundaries
I own audit. I do NOT own implementation.
## Ask vs Proceed
Ask when scope is load-bearing.
## Loop-Breaking
Escape after 2 passes.
## Tools
Read / Grep / Bash.
## Communication
YAML output.
## Context Loading
3 refs max.
## Audit Protocol
Threat-model first, then code.
## Anti-Patterns
I don't certify without verification.
## Negative Examples
BAD: ... GOOD: ..."
make_payload "$SECURITY_PROFILE" | bash "$HOOK"
assert_exit "T9 security profile with '## Audit Protocol' as operational slot passes" 0 $?

# T10 (hook v2.5): orchestrator profile shape uses '## Task Routing' as operational slot. ALLOW.
ORCH_PROFILE="# Orchestrator
You are the Orchestrator.
## Identity
You coordinate agents.
## Core Rules
1. Verify before delegating.
## Role Boundaries
I own dispatch. I do NOT own implementation.
## Ask vs Proceed
Ask when route is ambiguous.
## Loop-Breaking
Escape after 2 routes.
## Tools
Task / Read.
## Communication
YAML output.
## Context Loading
3 refs max.
## Task Routing
SE → implementation, QA → tests, Architect → design.
## Anti-Patterns
I don't ship without verification.
## Negative Examples
BAD: ... GOOD: ..."
make_payload "$ORCH_PROFILE" | bash "$HOOK"
assert_exit "T10 orchestrator profile with '## Task Routing' as operational slot passes" 0 $?

# T11 (hook v2.5): role H1 with all 10 required but NO operational slot synonym. BLOCK.
NO_SLOT_PROFILE="# Senior Engineer
You are the Senior Engineer.
## Identity
You serve the codebase.
## Core Rules
1. Test first.
## Role Boundaries
I own X. I do NOT own Y.
## Ask vs Proceed
Ask when load-bearing.
## Loop-Breaking
Escape after 2 passes.
## Tools
Read / Edit / Bash.
## Communication
YAML output.
## Context Loading
3 refs max.
## Anti-Patterns
I don't ship without tests.
## Negative Examples
BAD: ... GOOD: ..."
make_payload "$NO_SLOT_PROFILE" | bash "$HOOK" 2>/dev/null
assert_exit "T11 absence of all operational-slot synonyms blocks" 2 $?

echo ""
echo "$pass/$((pass + fail)) passed"
exit $fail
