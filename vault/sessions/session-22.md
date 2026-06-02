---
title: Session 22 — single-trunk reconciliation (gdw); main is the complete trunk; carrier retired
type: session
permalink: a-plus-maxing/sessions/session-22
created: 2026-06-02
session: S22
---

# Session 22 (2026-06-02)

## Goal (as contracted)

Resolve `gdw` — make `main` the single complete trunk (union of main's 20 agents + design
provenance and feature's governance/tooling/vault/skills), install a mechanical guard against
re-fragmentation, log the root cause as a new PF class, retire the long-lived feature carrier.

## What happened

1. **Root cause verified, not assumed (PF-S22-01, `AP-BRANCH-WRITE-FRAGMENTATION`).** Git
   archaeology: merge-base of `origin/main` and the feature carrier froze at `d6c992a` (S5/S6);
   feature NEVER merged main; the 16 specialists were committed only to main (per-slug PRs),
   the governance/tooling only to feature. NEITHER branch was the complete runnable system. The
   deeper cause: PF-S2-06's remediation (`never-PR-feature→main`) forbade one reconciliation
   direction without mandating the inverse — a guard that prevented one failure seeded the next.
   Walter's hypothesis (parallel worktree builds + a neglected branch) was directionally right
   but it was bidirectional. Logged in full with the parallel-research-tracks recurrence vector.

2. **Mechanical guard built (`branch-completeness-audit.sh`, INV-TRUNK-COMPLETENESS).** Asserts
   the checkout holds every deployed `agent.md` on a reference branch + the governance layer;
   3/3 non-tautological smoke tests (throwaway-repo fixtures); the roster-gap case encodes the
   exact PF-S22-01 failure. Validated by detecting the LIVE split on feature (20 on origin/main,
   16 absent). Wired into close step 8.5 + session open.

3. **Reconciliation (verified union merge).** Aborted dry-run first to enumerate the real
   conflict set (7 files) and confirm the 20 agents survive. Pre-merge analysis proved feature
   is a content-superset for all 7 (risk-class.yaml diff = ONLY +dermatologist +genetics rows,
   14 shared rows byte-identical — the highest-risk file; INVARIANTS/process-failures supersets;
   log.md only stale-frontmatter). Merged feature into `fix/single-trunk-reconciliation` off
   origin/main; resolved all 7 to feature (`--theirs`), zero loss. AC4 gate green BEFORE main
   touched: 20 agents, branch-completeness 0 violations, bda smoke 8/8, completeness smoke 3/3,
   `bd doctor` no corruption / no duplicate IDs, handoff + scope-contract(S22) audits 0.

4. **Trunk decided + carrier retired.** ADR `2026-06-02-single-trunk-reconciliation`: main = the
   single complete trunk; short-lived `feature/*`/`fix/*` off main going forward; carrier
   tag-and-frozen as `archive/feature-wiki-bpc157-aplus-research`. CLAUDE.md branch-topology
   convention + close step 8.5 + step 9 updated. `gdw` CLOSED.

## Drift / discipline notes

- Two near-misses pre-empted by verify-before-act: losing a risk-class row in the union (caught
  by the superset analysis) and bead corruption from the JSONL auto-merge (caught by `bd doctor`).
- No agent or design-doc bodies edited — the merge preserved them.
- One new PF-class entry (PF-S22-01). Recurrence guard is mechanical (the completeness audit) +
  structural (single trunk).

## State at close

- `main` is the complete trunk (20 agents + governance/tooling/vault/skills) as of S22 close.
- Carrier retired; working checkout now on `main`; normal short-lived-branch flow going forward.
- `INV-TRUNK-COMPLETENESS` live (open + close). Closed S22: `gdw`.
- Next: `bte` (mechanical wiki ingestion — now unblocked) → `hil` (PII vault, P1).

See [[process-failures]] (PF-S22-01), [[decisions/2026-06-02-single-trunk-reconciliation]],
INVARIANTS Change Log (S22), HANDOFF What-Is-Next.
