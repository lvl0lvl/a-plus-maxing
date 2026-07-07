#!/usr/bin/env bash
# tests/test-consistency-audit-pin.sh — negative test for the 15j content-pin
# hardening of consistency-audit.sh's Mode-B sanctioned by-reference dispatch.
#
# F-007 obligation: prove the new guard goes RED on a STALE pin. Mode B accepts a
# sanctioned by-reference dispatch when a marker is adjacent to a resolving slug.
# The 15j hardening adds an OPTIONAL content pin
#   [role-ref: sanctioned roles/<slug>/agent.md sha256:<first12hex>]
# When pinned, the CURRENT first-12 sha256 of roles/<slug>/agent.md must match the
# pin; otherwise the profile DRIFTED behind a stale reference -> FAIL.
#
# Three properties, against generated temp fixtures:
#   (a) pinned marker whose hash MATCHES  -> audit PASS (exit 0)
#   (b) pinned marker whose hash is STALE -> audit FAIL (exit 1)  [load-bearing RED]
#   (c) UNPINNED marker                   -> audit PASS (exit 0)  [backward compat]

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh disable=SC1091
source "${TEST_DIR}/../lib/test-lib.sh"

AUDIT="${TEST_DIR}/../scripts/consistency-audit.sh"
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# Same portable hasher detection the audit uses — compute the real pin for fixtures.
if command -v shasum >/dev/null 2>&1; then
  _sha() { shasum -a 256 "$1"; }
elif command -v sha256sum >/dev/null 2>&1; then
  _sha() { sha256sum "$1"; }
else
  echo "[FAIL] no sha256 tool (shasum/sha256sum) available — cannot run pin test"
  exit 1
fi
sha12() { out="$(_sha "$1")"; printf '%s' "${out%% *}" | cut -c1-12; }

# write_role <lib> <slug> — a complete canonical role profile (10 fixed + 1 slot).
write_role() {
  local lib="$1" slug="$2" dir="$1/roles/$2"
  mkdir -p "$dir"
  cat > "${dir}/agent.md" <<EOF
# ${slug} role

## Identity
The ${slug}.

## Core Rules
Rules.

## Role Boundaries
Boundaries.

## Ask vs Proceed
Ask.

## Loop-Breaking
Break loops.

## Tools
Tools.

## Communication
Communicate.

## Context Loading
Load context.

## Anti-Patterns
Anti-patterns.

## Negative Examples
Negative examples.

## Audit Protocol
The operational slot synonym.
EOF
}

# write_close <lib> — exactly one canonical close-protocol definer (keeps CHECK (d)
# clean so ONLY the dispatch/pin check decides the verdict).
write_close() {
  cat > "$1/skills/close.md" <<'EOF'
# The session-close protocol
The one canonical close protocol.
EOF
}

# --------------------------------------------------------------------------
# (a) MATCH mini-lib: pinned marker whose hash matches the profile -> PASS.
# --------------------------------------------------------------------------
MATCH="${FIX}/match"
mkdir -p "$MATCH/skills" "$MATCH/roles"
write_role "$MATCH" "auditor"
write_close "$MATCH"
PIN_OK="$(sha12 "$MATCH/roles/auditor/agent.md")"
cat > "${MATCH}/skills/dispatch.md" <<EOF
# skill: dispatch
Dispatch the auditor [role-ref: sanctioned roles/auditor/agent.md sha256:${PIN_OK}].
EOF

# --------------------------------------------------------------------------
# (b) STALE mini-lib: pinned marker whose hash is WRONG -> FAIL (load-bearing).
# Identical to MATCH but the pin is a deliberately wrong 12-hex value.
# --------------------------------------------------------------------------
STALE="${FIX}/stale"
mkdir -p "$STALE/skills" "$STALE/roles"
write_role "$STALE" "auditor"
write_close "$STALE"
cat > "${STALE}/skills/dispatch.md" <<'EOF'
# skill: dispatch
Dispatch the auditor [role-ref: sanctioned roles/auditor/agent.md sha256:deadbeef0000].
EOF

# --------------------------------------------------------------------------
# (c) UNPINNED mini-lib: marker with NO pin -> PASS (backward compat).
# --------------------------------------------------------------------------
UNPINNED="${FIX}/unpinned"
mkdir -p "$UNPINNED/skills" "$UNPINNED/roles"
write_role "$UNPINNED" "auditor"
write_close "$UNPINNED"
cat > "${UNPINNED}/skills/dispatch.md" <<'EOF'
# skill: dispatch
Dispatch the auditor [role-ref: sanctioned roles/auditor/agent.md].
EOF

# --------------------------------------------------------------------------
# Assertions
# --------------------------------------------------------------------------
expect_exit 0 bash "$AUDIT" --lib "$MATCH"     # (a) pin matches -> PASS
expect_exit 1 bash "$AUDIT" --lib "$STALE"     # (b) pin stale  -> FAIL  [RED case]
expect_exit 0 bash "$AUDIT" --lib "$UNPINNED"  # (c) no pin     -> PASS  [backward compat]

# Load-bearing guard-fires: the SAME audit is green on the matching pin and red on
# the stale one — same input shape, only the pin value differs.
assert_red_when_guard_removed \
  "bash '$AUDIT' --lib '$MATCH'" \
  "bash '$AUDIT' --lib '$STALE'"

# The stale-pin diagnostic the tool promises to emit (drift message + re-sanction).
# The audit emits via emit/fail on STDOUT, so capture stdout (not stderr).
TESTS_RUN=$((TESTS_RUN + 1))
stale_out="$(bash "$AUDIT" --lib "$STALE" 2>&1 || true)"
if printf '%s' "$stale_out" | grep -q "profile drift behind a stale reference: roles/auditor/agent.md content changed since it was sanctioned"; then
  echo "[PASS] stale-pin drift diagnostic emitted"
else
  echo "[FAIL] stale-pin drift diagnostic missing"
  printf '%s\n' "$stale_out"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

test_summary
</content>
</invoke>
