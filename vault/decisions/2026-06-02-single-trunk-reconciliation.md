---
title: Single-trunk reconciliation — main is the complete trunk; feature carrier retired
type: decision
permalink: a-plus-maxing/decisions/2026-06-02-single-trunk-reconciliation
created: 2026-06-02
status: active
decided_by: Walter (operator)
supersedes: null
relates_to: 2026-05-23-aplus-research-skill
---

# Single-trunk reconciliation — `main` is the complete trunk; feature carrier retired

## Decision

`main` becomes the **single complete trunk** of the project: the 20 deployed agents
(4 foundation + 16 specialists) AND the governance/tooling/vault/skills layer, reconciled
by a one-time **union merge**. The long-lived working branch
`feature/wiki-bpc157-aplus-research` is **retired** (tag-and-freeze: `archive/feature-wiki-bpc157-aplus-research`,
branch ref deleted, history reachable via the tag). Going forward, work happens on
**short-lived `feature/*` / `fix/*` branches off `main`**, deleted after merge — normal git flow.

## Context / problem (bead `gdw`, PF-S22-01)

For ~15 sessions the project wrote to two branches that never reconciled (merge-base froze
at the S5/S6 joint close, `d6c992a`):

- **Product → `main`:** the 16 specialists were built in worktrees cut off `origin/main`
  and merged back to `main` via per-slug PRs. The feature branch never pulled them — all 16
  specialist `agent.md` lived on main, **zero on feature**.
- **Process → `feature`:** governance docs, the `bda` audit, INVARIANTS S13-S21, skills,
  vault, beads were committed directly to the feature working checkout and **never reached main**.

Net: **neither branch was the complete runnable system.** The operational checkout (feature)
could not dispatch the 16 specialists (not on disk); main could not run the gated pipeline
(no bda / stale skills). Root cause analysis: PF-S22-01 (`AP-BRANCH-WRITE-FRAGMENTATION`) — a
prior remediation (PF-S2-06's "never PR feature→main") forbade one reconciliation direction and
nothing mandated the inverse, so the halves diverged silently. Discovered S21 (materializing
main for the `0be` marker), resolved S22.

## How the union merge was resolved (7 conflicts)

Verified pre-merge that **feature is a content-superset of main** for every governance doc, so
all 7 conflicts resolved to feature's version (`--theirs`) with **zero loss**:

| File | Resolution | Verification |
|---|---|---|
| `templates/specialist-risk-class.yaml` | feature | diff shows ONLY +dermatologist +genetics rows; the 14 shared rows byte-identical; every deployed specialist has a row post-merge |
| `INVARIANTS.md` | feature | feature = main's invariant IDs + `INV-RESEARCH-PROVENANCE-DISJOINT` (superset) |
| `memory/process-failures.md` | feature | feature = main's PF IDs + S16/S17/S22 (superset) |
| `vault/meta/log.md` | feature | only main-only lines were stale frontmatter dates; no log entries lost |
| `HANDOFF.md` | feature | continuity doc; feature is the evolution |
| `design/DESIGN_DOC_TEMPLATE.md` | feature | integrator-maintained; feature current (0be canonical-layout ref) |
| `design/.session-b-deployments/SESSION_KICKOFF.md` | feature | process artifact; feature current |

The 364 main-only files (specialists + design-work) were untouched by the merge (kept). The 13
feature-only files (bda + tests, vault sessions, ADRs, the new completeness audit + PF) were added.
Post-merge AC4 gate (all green BEFORE main was touched): 20 agents; `branch-completeness-audit`
0 violations; bda smoke 8/8; completeness smoke 3/3; `bd doctor` no corruption / no duplicate IDs;
handoff + scope-contract audits clean.

## Recurrence guard (so this can't silently happen again)

- **`scripts/branch-completeness-audit.sh`** (INV-TRUNK-COMPLETENESS) — asserts the checkout
  holds every deployed `agent.md` on a reference branch + the governance layer; run at session
  open + close (CLAUDE.md step 8.5). Would have fired at S16.
- **Single trunk.** The dual-branch carrier model — the root enabler — is retired.
- **Parallel tracks** (the next phase, e.g. library-population research batches) declare ONE
  canonical merge target and run the completeness audit after the batch reconciles; a batch is
  not "done" until the trunk is verified complete.

## Consequences

- Positive: one branch is the whole runnable system; normal git flow; a mechanical guard against
  re-fragmentation; the next (parallel) phase has a completeness gate.
- Cost: one careful reconciliation merge (done, gated); the working checkout moves to `main`;
  the 21-session feature history is preserved as a tag, not a live branch.
- Trade-off accepted: `main` no longer has a "clean agents-only" history — it now carries the full
  project (the clean-history goal was the original reason the carrier existed; it caused this split,
  so it is abandoned in favor of completeness).
