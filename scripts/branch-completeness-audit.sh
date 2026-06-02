#!/usr/bin/env bash
# branch-completeness-audit.sh — trunk-completeness guard (INV-TRUNK-COMPLETENESS).
#
# Detects AP-BRANCH-WRITE-FRAGMENTATION (PF-S22-01): a deployed agent or the governance
# layer existing on some branch but NOT on the operational trunk/checkout. Asserts the
# current checkout (HEAD) contains every deployed agent.md present on a reference branch
# (default origin/main) + the governance layer (the bda audit + the registered provenance
# invariant). Run at session open + close (CLAUDE.md step 8.5).
#
# WHY THIS EXISTS (PF-S22-01): for ~15 sessions the 16 specialist agents lived on `main`
# while the governance/tooling (bda, INVARIANTS S13-S21, skills, vault) lived only on the
# `feature` working checkout — neither branch was the complete runnable system, and the
# split was invisible because the halves are operationally separate until library-population.
# This audit would have fired at S16 the instant the first specialist landed on main but not
# the working branch. A "20 agents on main" attestation is true AND misleading; this asserts
# completeness against the OPERATIONAL checkout, not just the merge target.
#
# Operates on the git repo containing the current working directory (compares refs via
# git cat-file / ls-tree), so it is testable against throwaway repos.
#
# USAGE:
#   branch-completeness-audit.sh [--reference <git-ref>]
#     --reference  branch/ref whose deployed agents the checkout (HEAD) must contain
#                  (default: origin/main). Roster check is skipped (info, not fail) if the
#                  ref is unresolvable (offline / not fetched); the governance check always runs.
#
# EXIT CODES:
#   0 — complete (checkout has every reference agent + the governance layer)
#   1 — one or more gaps (missing agent / missing governance artifact)
#   2 — usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/audit-helpers.sh"

REFERENCE="origin/main"
while [ "$#" -gt 0 ]; do
    case "$1" in
        --reference) REFERENCE="${2:?--reference needs a ref}"; shift 2 ;;
        *) echo "branch-completeness-audit: unknown arg '$1'" >&2; exit 2 ;;
    esac
done

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "branch-completeness-audit: not inside a git work tree" >&2; exit 2; }

audit_init "branch-completeness-audit"

# --- governance layer present in the current checkout (HEAD) ---
# The bda audit script: the mechanical research-provenance gate.
if ! git cat-file -e "HEAD:scripts/audit-research-provenance.sh" 2>/dev/null; then
    violation "INV-TRUNK-COMPLETENESS" \
        "governance gap: scripts/audit-research-provenance.sh (bda) absent from the current checkout (HEAD)"
fi
# The registered provenance invariant must be in the checkout's INVARIANTS register.
inv_blob="$(git show "HEAD:INVARIANTS.md" 2>/dev/null || true)"
if ! printf '%s' "$inv_blob" | grep -q "INV-RESEARCH-PROVENANCE-DISJOINT"; then
    violation "INV-TRUNK-COMPLETENESS" \
        "governance gap: INV-RESEARCH-PROVENANCE-DISJOINT absent from INVARIANTS.md on the current checkout (HEAD)"
fi

# --- every deployed agent on the reference branch must be present in this checkout ---
if ! git rev-parse --verify --quiet "$REFERENCE" >/dev/null 2>&1; then
    info "reference '$REFERENCE' unresolvable (offline / not fetched) — roster comparison skipped; governance check only. Re-run with a fetched reference to verify roster completeness."
else
    checked=0; missing=0
    while IFS= read -r agent; do
        [ -n "$agent" ] || continue
        checked=$((checked + 1))
        if ! git cat-file -e "HEAD:$agent" 2>/dev/null; then
            violation "INV-TRUNK-COMPLETENESS" \
                "roster gap: $agent present on $REFERENCE but ABSENT from the current checkout (HEAD) — branch-write fragmentation (PF-S22-01)"
            missing=$((missing + 1))
        fi
    done < <(git ls-tree -r --name-only "$REFERENCE" | grep -E '^\.claude/agents/[^/]+/agent\.md$' || true)
    info "roster check vs $REFERENCE: $checked deployed agent(s) on reference, $missing absent from checkout"
fi

audit_summary
audit_exit
