#!/usr/bin/env bash
# tests/test-consistency-audit.sh — negative test for consistency-audit.sh.
#
# F-007 obligation: prove the cross-layer audit goes RED on a known-bad library and
# GREEN on a known-good one. consistency-audit.sh exists to catch contradictions
# BETWEEN layers (F-019 self-deny, F-020 phantom role, F-006 threshold drift,
# F-005 competing close protocols), so the fixtures must exercise those.
#
# We build two mini-libraries from scratch:
#   GOOD: roles/ + skills/ where every dispatch either fully inlines the canonical
#         11-section profile or carries a sanctioned by-reference marker, every
#         dispatched slug resolves, every judge threshold uses the X/10 convention,
#         and exactly one file defines the session-close protocol. -> exit 0.
#   BAD : the same library mutated with the three contradictions the spec names —
#         a skill EMBED-dispatching a real role (F-019), a 99/100 threshold while
#         siblings use >=9/10 (F-006), and a dispatch of a NONEXISTENT role (F-020),
#         plus a second competing close protocol (F-005). -> exit non-zero (FAIL).
#
# The load-bearing assertion is assert_red_when_guard_removed: good=PASS, bad=FAIL.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh disable=SC1091
source "${TEST_DIR}/../lib/test-lib.sh"

AUDIT="${TEST_DIR}/../scripts/consistency-audit.sh"
# Fixtures are generated scratch (not committed): write to a throwaway temp dir so
# running the suite never dirties the tracked tree (skill_consolidator-oas).
FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT

# --- helper: write a complete canonical role profile (10 fixed + 1 slot) ------
write_role() {
  # write_role <lib> <slug>
  local lib="$1" slug="$2" dir
  dir="${lib}/roles/${slug}"
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

# --- helper: write a skill that FULLY INLINES a role profile ------------------
write_inlining_skill() {
  # write_inlining_skill <lib> <name> <slug>
  local lib="$1" name="$2" slug="$3"
  mkdir -p "${lib}/skills"
  {
    echo "# skill: ${name}"
    echo "Dispatch the role at roles/${slug}/agent.md with the FULL profile inlined:"
    echo
    cat "${lib}/roles/${slug}/agent.md"
  } > "${lib}/skills/${name}.md"
}

# ============================================================================
# GOOD mini-lib
# ============================================================================
GOOD="${FIX}/good"
mkdir -p "$GOOD/skills" "$GOOD/roles"

write_role "$GOOD" "auditor"
write_role "$GOOD" "router"

# A skill that fully inlines the auditor profile -> hook accepts (F-019 clean).
write_inlining_skill "$GOOD" "run-audit" "auditor"

# A skill that dispatches by reference but with a SANCTIONED marker -> hook accepts.
cat > "${GOOD}/skills/route.md" <<'EOF'
# skill: route
Dispatch the router via roles/router/agent.md  <!-- INLINE-EXEMPT: sanctioned by-reference -->
This is an explicitly sanctioned by-reference dispatch.
EOF

# A judge rubric using the X/10 convention (>=9/10) — consistent.
cat > "${GOOD}/skills/rubric.md" <<'EOF'
# rubric
Quality bar: a deliverable must score >= 9/10 to ship.
Sibling check also uses 8/10 as the warn line.
EOF

# Exactly one definer of the session-close protocol.
cat > "${GOOD}/skills/close.md" <<'EOF'
# The session-close protocol
This is the one canonical session-close protocol for the library.
EOF

# A SANCTIONED non-canonical close protocol (a project instance) declares its kind
# and must NOT count as a competing definer -> GOOD stays at 1 unmarked definer.
# Remove the marker handling and GOOD has 2 definers -> RED. Load-bearing.
cat > "${GOOD}/skills/close-instance.md" <<'EOF'
# Session Close Protocol
<!-- close-protocol: instance -->
This project's own close protocol; the canonical definition lives in the framework.
EOF

# Non-shipped scratch: an UNSANCTIONED role dispatch buried in a drafts/ dir must
# be EXCLUDED from the dispatch scan -> GOOD stays PASS. (Guard for the BUG-22e
# class exclusion: remove the drafts/.research prune and GOOD turns RED.)
mkdir -p "${GOOD}/skills/route/drafts"
cat > "${GOOD}/skills/route/drafts/scratch.md" <<'EOF'
# scratch draft (NOT shipped)
Rough idea: dispatch the auditor via roles/auditor/agent.md with no marker.
EOF

# Non-dispatcher corpus: a calibration file that QUOTES role paths as review
# SUBJECTS (including a NONEXISTENT one) must be SKIPPED via the explicit opt-out
# -> GOOD stays PASS. Remove the opt-out marker handling and the quoted phantom
# path turns GOOD RED (F-020). Load-bearing for the opt-out.
cat > "${GOOD}/skills/calibration-examples.md" <<'EOF'
<!-- consistency-audit: not-a-dispatcher — calibration corpus; role paths are review subjects -->
# Review calibration
Example finding: an adversarial review OF roles/ghost-reviewer/agent.md (a
profile that does not exist) flags a broken reference. This path is a SUBJECT of
review, not a role dispatch.
EOF

# F-006 refinement guard: a file that (a) NAMES 99/100 only to record its REMOVAL
# (meta-prose) and (b) uses legitimate graduated bars + 0-100 credibility scores
# must NOT be flagged -> GOOD stays PASS. Revert the check to "flag any N/100" and
# this turns GOOD RED. Load-bearing for the property-not-signal refinement.
cat > "${GOOD}/skills/threshold-notes.md" <<'EOF'
# threshold notes
We REMOVED the literal 99/100 judge threshold (F-006, genesis-disproven) — no
longer used. Graduated per-mode bars (e.g. standard 92/100) and per-source
credibility scored 0-100 (e.g. avg credibility >60/100) are legitimate and stay.
A fractional aggregate like 8.99/100 is a score, not the 99/100 gate (drift_re
left-boundary guard: remove the decimal-reject and this turns GOOD RED).
EOF

# F-005 check-(d) guards: a .sh comment that names "close-protocol" and a prose
# MENTION of "the session-close protocol" (no heading) must NOT count as close-
# protocol definers -> GOOD keeps its single definer (close.md) and stays PASS.
# Re-add .sh scanning or the phrase-match and GOOD gains 2 phantom definers -> RED.
cat > "${GOOD}/skills/helper.sh" <<'EOF'
#!/usr/bin/env bash
# This helper references the session-close protocol (CLAUDE.md close-protocol step 4).
echo "helper"
EOF
cat > "${GOOD}/skills/mentions.md" <<'EOF'
# Notes
See the session-close protocol for the canonical steps; this file only points at it.
EOF

# ============================================================================
# BAD mini-lib — three named contradictions + a competing close protocol.
# ============================================================================
BAD="${FIX}/bad"
mkdir -p "$BAD/skills" "$BAD/roles"

write_role "$BAD" "auditor"
write_role "$BAD" "router"

# F-019: a skill that EMBED-dispatches a REAL role by path WITHOUT inlining the
# full profile and WITHOUT a sanctioned marker -> the role-inlining hook would DENY.
cat > "${BAD}/skills/run-audit.md" <<'EOF'
# skill: run-audit
EMBED the auditor role: see roles/auditor/agent.md for the full profile.
(Profile referenced by path, not inlined.)
EOF

# F-020: a skill dispatching a NONEXISTENT role slug (no roles/ghost/agent.md).
cat > "${BAD}/skills/spawn-ghost.md" <<'EOF'
# skill: spawn-ghost
Dispatch the ghost worker at roles/ghost/agent.md.
EOF

# F-006: a judge rubric using 99/100 while a sibling uses >=9/10 -> threshold drift.
cat > "${BAD}/skills/rubric.md" <<'EOF'
# rubric
create-adr requires a score of 99/100 to pass.
But every sibling rubric uses >= 9/10 — this one drifted.
EOF

# F-005: TWO files each define "the session-close protocol" -> competing protocols.
cat > "${BAD}/skills/close-a.md" <<'EOF'
# The session-close protocol
First competing definition of the session-close protocol.
EOF
cat > "${BAD}/skills/close-b.md" <<'EOF'
## Session-Close Protocol
Second, competing close protocol definition.
EOF

# ============================================================================
# BLANKET mini-lib — a file-wide by-reference marker NOT on the slug's own
# reference line must NOT waive that slug (per-slug tightening, F-007 hole).
# Otherwise clean (one close protocol, no thresholds) so ONLY the dispatch check
# can decide the verdict. With the per-slug fix: auditor's ref line is unmarked
# -> FAIL. Without it (file-wide marker grep): the stray marker rubber-stamps the
# dispatch -> PASS -> this assertion turns RED. Load-bearing.
# ============================================================================
BLANKET="${FIX}/blanket"
mkdir -p "$BLANKET/skills" "$BLANKET/roles"
write_role "$BLANKET" "auditor"
cat > "${BLANKET}/skills/waiver.md" <<'EOF'
# skill: waiver
Note: this library uses role-ref: sanctioned by-reference dispatch in general.

Dispatch the auditor: roles/auditor/agent.md
(The sanctioned marker above is a file-wide note, NOT on this slug's ref line.)
EOF
cat > "${BLANKET}/skills/close.md" <<'EOF'
# The session-close protocol
The one canonical close protocol.
EOF

# ============================================================================
# F006 mini-lib — ONLY an active literal 99/100 judge-pass target, otherwise
# clean (one close protocol, no role dispatches). Isolates CHECK (c): with the
# refinement, the active 99/100 -> FAIL; remove check (c) and it PASSes. The GOOD
# lib already proves the EXEMPT side (meta-prose + graduated bars do not flag), so
# the pair pins the property-not-signal behavior from both directions.
# ============================================================================
F006="${FIX}/f006"
mkdir -p "$F006/skills"
# "literal" in an ACTIVE gate must NOT exempt it (the old meta_re wrongly did).
cat > "${F006}/skills/rubric.md" <<'EOF'
# rubric
Pass threshold: require a literal 99/100 across all dimensions. Iterate until the judge passes.
EOF
cat > "${F006}/skills/close.md" <<'EOF'
# The session-close protocol
The single canonical close protocol for this fixture.
EOF

# ============================================================================
# LEAK mini-lib — a SINGLE line carrying two role refs: one adjacent-marked
# (accepted), one bare/unmarked further along (must FAIL). Proves the marker binds
# per-slug by ADJACENCY, not line-wide. Revert to the line-wide marker grep and the
# unmarked ref is wrongly waived -> this assertion turns RED.
# ============================================================================
LEAK="${FIX}/leak"
mkdir -p "$LEAK/skills"
write_role "$LEAK" "qa"
write_role "$LEAK" "security"
cat > "${LEAK}/skills/dispatch.md" <<'EOF'
# skill: dispatch
Dispatch: QA = [role-ref: sanctioned roles/qa/agent.md], then also Security = roles/security/agent.md
EOF
cat > "${LEAK}/skills/close.md" <<'EOF'
# The session-close protocol
The one canonical close protocol.
EOF

# ============================================================================
# Assertions
# ============================================================================

# GOOD: all layers consistent (drafts/ scratch excluded) -> PASS (exit 0).
expect_exit 0 bash "$AUDIT" --lib "$GOOD"

# BLANKET: stray file-wide marker does NOT waive the unmarked slug ref -> FAIL.
expect_exit 1 bash "$AUDIT" --lib "$BLANKET"

# F006: an active "literal 99/100" judge-pass target (otherwise clean) -> FAIL
# ("literal" must NOT exempt an active gate — the old meta_re hole).
expect_exit 1 bash "$AUDIT" --lib "$F006"

# LEAK: same-line marked+unmarked pair — the unmarked slug is NOT waived -> FAIL.
expect_exit 1 bash "$AUDIT" --lib "$LEAK"

# BAD: at least one cross-layer inconsistency -> FAIL (exit 1).
expect_exit 1 bash "$AUDIT" --lib "$BAD"

# Config errors are FATAL (exit 2), distinct from FAIL.
expect_exit 2 bash "$AUDIT"                       # no --lib
expect_exit 2 bash "$AUDIT" --lib "${FIX}/nope"   # missing root

# Load-bearing guard-fires assertion: good=0, bad=non-zero.
assert_red_when_guard_removed \
  "bash '$AUDIT' --lib '$GOOD'" \
  "bash '$AUDIT' --lib '$BAD'"

test_summary
