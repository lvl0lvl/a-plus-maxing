---
title: Session 21 — bda mhg fix (7.5/8.5 target.type) + 0be Part-2 marker + roster-revert hazard averted
type: session
permalink: a-plus-maxing/sessions/session-21
created: 2026-06-02
session: S21
---

# Session 21 (2026-06-02)

## Goal (as contracted)

Fix bead `mhg` — make `bda` (`scripts/audit-research-provenance.sh`) gate 7.5/8.5 on
the dispatch's `target.type=compound` (from `gate-2.75.json`), not the slug's risk-table
`target_class=compound`, so goal-agnostic reference research stops hitting a false block.
Then close the carried `0be` Part-2 loose end (land the supplement quarantine marker on
main). No scope expansion into bte/hil/library/research.

## What happened

1. **bda `mhg` FIXED (item #1, change-discipline edit — Walter-approved).** Verified the
   premise before scoping: the bead's "`target_type`" is nested in the schema as
   **`target.type`** (enum compound|biomarker|protocol|reference). Confirmed the payoff
   against the 7 real specialists: 3 (cardiovascular/dermatologist/gi) were false-blocked
   on 7.5/8.5 purely because their *slug* risk-table class is `compound`, while ALL 7
   dispatches are `target.type=reference` (goal-agnostic landscapes). Fix: read `target.type`
   from `gate-2.75.json`; require 7.5/8.5 only for a compound ENTRY; fail-closed to the old
   `target_class` behavior when unreadable. Header comment + SKILL.md gate-by-mode matrix
   footnoted to match. INVARIANTS Change Log row appended (S21).
   - **Smoke tests 6→8**, two new NON-tautological cases (reference-landscape PASSes without
     floors; compound-entry still FAILs when floors absent). Non-tautology EMPIRICALLY proven:
     the same Case-6 fixture FAILs under a reverted-trigger copy (2 missing-floor violations),
     PASSes patched. (A first attempt at that proof gave a spurious rc=1 — a scratch copy
     couldn't source `audit-helpers.sh`; caught by reading the output file, not the exit code.)
   - **Production-path validated (AC3):** patched bda run against the real merged design-work
     dirs materialized from main — 7.5/8.5 false-block cleared on all three; genetics control
     still EXIT 0. The three still EXIT=1 on the *orthogonal* gate-3.5 grandfather (ADR
     2026-06-01) — reported honestly, not overclaimed. Commit `73284ca`.
   - `mhg` + `5ot` closed (`5ot`'s own resolution condition — bda distinguishes reference
     from compound-entry, no risk-table change — is met by this fix).

2. **`0be` Part-2 — roster-revert hazard averted (AP-ACT-BEFORE-VERIFY).** Before merging the
   S20 quarantine branch, `git ls-files`/diff caught that `fix/supplement-gates-quarantine`
   was **18 commits stale** (merge-base `94496b4`, predates batch-4 + genetics) — merging it
   would have REVERTED THE ROSTER and clobbered `.beads/` with a May-31 snapshot. Replaced
   with a fresh single-file branch off current main → marker `_QUARANTINE-NONCANONICAL.md`
   landed via PR #25 (rebase-merge). Roster verified intact (20 agents) post-merge. Stale
   branch deleted (local + origin) as a hazard. `0be` CLOSED.

3. **NEW finding (`gdw`, P2).** Materializing origin/main for the marker revealed main is
   **~9 sessions stale on governance**: the bda script + `INV-RESEARCH-PROVENANCE-DISJOINT`
   + the S13-S21 INVARIANTS evolution are ABSENT from main (Change Log ends at S12). Deployed
   agents reached main via per-slug PRs, but the audit/invariants/skills layer lives only on
   the feature continuity-carrier. The S20 builder note "bda present in main" was wrong
   (conflated the `--add-dir` feature checkout with main). Open branch-topology question for
   Walter; directly shapes `bte` (a vault-write gate must live where writes happen). Filed,
   NOT acted on.

## Drift / discipline notes

- Two CHANGED criteria, both documented: `5ot` reframe→resolve (resolution condition met);
  AC5 stale-branch→fresh-branch (forced by the staleness discovery). Both = verify-before-act
  working, not freelancing.
- Session-open protocol (PF-S13-01) HELD: baseline suite RUN, premise verified before scoping.
- No new PF-class entries. `git ls-files`-before-merge + read-the-output-not-the-exit-code both
  fired as designed.

## State at close

- `origin/main` `7cf253b` (2026-06-02): 20 agents + the 0be marker. Roster unchanged otherwise.
- bda mhg fixed; smoke 8/8; 3 close audits green at --session 21.
- Closed S21: `mhg`, `5ot`, `0be`. New: `gdw`.
- Next: `gdw` (governance-sync question) → `bte` (mechanical ingestion) → `hil` (PII vault).

See [[process-failures]], INVARIANTS Change Log (S21), HANDOFF What-Is-Next.
