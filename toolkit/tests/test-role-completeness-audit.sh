#!/usr/bin/env bash
# test-role-completeness-audit.sh — proves role-completeness-audit.sh goes RED on
# a role profile missing a canonical section (F-007 negative-test obligation: an
# audit that cannot demonstrate it FAILs on bad input does not count as enforcing).
set -uo pipefail
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"
AUDIT="$TEST_DIR/../scripts/role-completeness-audit.sh"

# A complete 11-section profile (10 fixed + the Modes operational slot).
SECS='## Identity
## Core Rules
## Role Boundaries
## Ask vs Proceed
## Loop-Breaking
## Tools
## Communication
## Context Loading
## Anti-Patterns
## Negative Examples
## Modes'

GOOD="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$GOOD/roles/complete"
printf '%s\n' "$SECS" > "$GOOD/roles/complete/agent.md"

BAD="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$BAD/roles/complete" "$BAD/roles/broken"
printf '%s\n' "$SECS" > "$BAD/roles/complete/agent.md"
# broken: drop the operational slot — the EXACT game-designer/0c8 defect.
printf '%s\n' "$SECS" | grep -v '## Modes' > "$BAD/roles/broken/agent.md"

# Core contract: green when every profile is complete, RED when a broken one is present.
assert_red_when_guard_removed \
  "bash '$AUDIT' --lib '$GOOD'" \
  "bash '$AUDIT' --lib '$BAD'"

# Explicit exit-code assertions.
expect_exit 0 bash "$AUDIT" --lib "$GOOD"   # all complete -> PASS
expect_exit 1 bash "$AUDIT" --lib "$BAD"    # one missing a section -> FAIL

# The specific defect (the broken role) is named in the audit's stdout output.
out="$(bash "$AUDIT" --lib "$BAD" 2>&1 || true)"
TESTS_RUN=$((TESTS_RUN + 1))
if printf '%s' "$out" | grep -q "role 'broken' incomplete"; then
  echo "[PASS] audit names the incomplete role"
else
  echo "[FAIL] audit did not name the incomplete role"; TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Bad args / no roles -> FATAL (exit 2), never a silent pass.
expect_exit 2 bash "$AUDIT"
expect_exit 2 bash "$AUDIT" --lib /no/such/dir/anywhere
expect_exit 2 bash "$AUDIT" --bogus

# --- Frontmatter validation (dogfooding finding: invalid YAML / missing keys) ---
# All four roles below carry the full 11 sections so ONLY the frontmatter varies;
# this isolates the frontmatter guard from the section guard.
VALID_FM='---
name: complete
title: Complete
description: "A complete role with valid frontmatter."
---'
# Invalid YAML: an unquoted value containing a colon+space (the exact real defect).
INVALID_FM='---
name: complete
title: Complete
description: this has: an unquoted colon
---'
# Valid YAML but missing a required key (no description).
MISSING_FM='---
name: complete
title: Complete
---'

FM="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$FM/roles/valid_fm" "$FM/roles/no_fm"
# A role WITH valid complete frontmatter prepended to the 11 sections.
printf '%s\n%s\n' "$VALID_FM" "$SECS" > "$FM/roles/valid_fm/agent.md"
# A role with NO frontmatter at all (backward compat: must still PASS).
printf '%s\n' "$SECS" > "$FM/roles/no_fm/agent.md"

# Frontmatter YAML validation is gated on PyYAML, an OPTIONAL dependency (BUG-1).
# The section-completeness negative test above is dependency-free and always runs;
# the frontmatter lint needs PyYAML and, when it is absent, the audit WARNs (loud,
# non-gating) and the suite stays GREEN — parity with test-gate-attest.sh's loud
# skip. So the invalid/missing-key FAIL direction (the lint's F-007 negative test)
# is exercised only when the dep is present; when absent we instead prove the audit
# does NOT wrongly gate on the missing dep and warns loudly.
BADYAML="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$BADYAML/roles/badyaml"
printf '%s\n%s\n' "$INVALID_FM" "$SECS" > "$BADYAML/roles/badyaml/agent.md"
MISSINGKEY="$(mktemp -d 2>/dev/null || mktemp -d -t rolecomp)"
mkdir -p "$MISSINGKEY/roles/missingkey"
printf '%s\n%s\n' "$MISSING_FM" "$SECS" > "$MISSINGKEY/roles/missingkey/agent.md"

if python3 -c "import yaml" >/dev/null 2>&1; then
  # Valid + no-frontmatter together -> PASS (frontmatter optional, valid when present).
  expect_exit 0 bash "$AUDIT" --lib "$FM"

  # Invalid-YAML frontmatter -> RED (FAIL, exit 1) — the lint's negative test.
  assert_red_when_guard_removed \
    "bash '$AUDIT' --lib '$FM'" \
    "bash '$AUDIT' --lib '$BADYAML'"
  expect_exit 1 bash "$AUDIT" --lib "$BADYAML"
  out_y="$(bash "$AUDIT" --lib "$BADYAML" 2>&1 || true)"
  TESTS_RUN=$((TESTS_RUN + 1))
  if printf '%s' "$out_y" | grep -q "role 'badyaml' frontmatter: invalid YAML"; then
    echo "[PASS] audit names the invalid-YAML frontmatter role"
  else
    echo "[FAIL] audit did not flag invalid-YAML frontmatter"; TESTS_FAILED=$((TESTS_FAILED + 1))
  fi

  # Missing required key -> RED (FAIL, exit 1).
  expect_exit 1 bash "$AUDIT" --lib "$MISSINGKEY"
  out_m="$(bash "$AUDIT" --lib "$MISSINGKEY" 2>&1 || true)"
  TESTS_RUN=$((TESTS_RUN + 1))
  if printf '%s' "$out_m" | grep -q "role 'missingkey' frontmatter: missing or empty required key(s): description"; then
    echo "[PASS] audit names the missing frontmatter key"
  else
    echo "[FAIL] audit did not flag the missing frontmatter key"; TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
else
  echo "[SKIP] PyYAML absent — frontmatter YAML-lint negative tests not exercised (loud, like test-gate-attest.sh)"
  # The optional-dep path must NOT wrongly gate: a section-complete tree with
  # invalid frontmatter still PASSes (exit 0) because the lint WARNs, not FAILs.
  expect_exit 0 bash "$AUDIT" --lib "$FM"
  expect_exit 0 bash "$AUDIT" --lib "$BADYAML"
  # ...and the audit says loudly that it did not run the YAML lint.
  out_w="$(bash "$AUDIT" --lib "$BADYAML" 2>&1 || true)"
  TESTS_RUN=$((TESTS_RUN + 1))
  if printf '%s' "$out_w" | grep -q "PyYAML unavailable — YAML lint NOT run"; then
    echo "[PASS] audit loudly warns the YAML lint was skipped"
  else
    echo "[FAIL] audit did not loudly warn about the skipped YAML lint"; TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
fi

rm -rf "$GOOD" "$BAD" "$FM" "$BADYAML" "$MISSINGKEY"
test_summary
