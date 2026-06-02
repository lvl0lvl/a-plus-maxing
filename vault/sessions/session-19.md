---
title: Session 19 — bda full audit + hfm grandfather decision
type: session
permalink: a-plus-maxing/sessions/session-19
created: 2026-05-30
session: S19
---

# Session 19 (2026-05-30)

## Goal

Run `bda` (`scripts/audit-research-provenance.sh`) across all 10 deployed specialists,
produce the provenance pass/fail table, and frame the `hfm` backfill-vs-grandfather
decision for Walter with the real gap size. Diagnostic + decision-prep — no merges, no
library writes, no agent edits.

## What happened

1. **Session-open protocol run in full** (PF-S13-01 guard held): HANDOFF.md read in full
   (1224 lines, paged past two truncations), INVARIANTS + process-failures + landmarks +
   git status + test baseline all run with real output, scope contract written + confirmed
   before any work.

2. **Session-open finding:** `INV-RESEARCH-PROVENANCE-DISJOINT` was referenced by bda +
   CLAUDE.md close-8.5 and the S18 "register +1" attestation, but was absent from the
   INVARIANTS.md register (no row, no Change Log). Surfaced, bead `08d` filed, NOT
   self-registered.

3. **bda full audit** (audit-only, temp checkouts from origin/main 94496b4): 9 of 9
   research-dispatching specialists FAIL; medical-liaison N/A. None pass. Failures
   classified by substrate beneath the uniform EXIT=1 (see ADR table).

4. **hfm decision brief** delivered. Researching the library model (SKILL.md §1.1,
   WIKI.md, PF-S2-04) reframed the question: the audited research is build-time
   scaffolding, not library content; library pages get fresh gated research at runtime.
   Recommendation: grandfather (Option A) + supplement quarantine.

5. **Walter approved Option A** (grandfather) + the invariant registration.

## Decisions

- **Grandfather all 9** deployed frameworks; library-authoring gate (bda +
  INTEGRATION-CHECKLIST 1a) is the binding provenance control. ADR:
  [[2026-05-30-grandfather-design-work-research-provenance]].
- **Supplement carve-out:** quarantine the mimicked `research-gates/` (not re-run);
  folded into bead `0be`.
- **INV-RESEARCH-PROVENANCE-DISJOINT registered** via change-discipline ritual.

## Bead changes

- `hfm` (P1) CLOSED — grandfather decision recorded → epic `c6k` UNBLOCKED.
- `08d` (P2, NEW) CLOSED — invariant registered.
- `0be` (P2) scope expanded to own the supplement quarantine.

## Artifacts

- bda results: `/tmp/bda-s19-results.txt` (regenerable via the loop in HANDOFF "What Is Next")
- ADR: `vault/decisions/2026-05-30-grandfather-design-work-research-provenance.md`
- INVARIANTS.md: register row + Change Log (S19)

## What is next

- `0be` — pin canonical `gates/` convention + quarantine supplement (before batch-4).
- batch-4 — cardiovascular, recovery, longevity-strategist, mental-performance-coach,
  dermatologist; each clears bda at merge.
- Library-population is no longer bd-ready-blocked, but remains gated by the per-page
  library-authoring control.
