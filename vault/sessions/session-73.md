---
title: Session 73 — supplement↔peptide additive-AE screen (Phase-3 compound band)
type: session
date: 2026-06-18
permalink: a-plus-maxing/sessions/session-73
---

# Session 73 (2026-06-18)

## Goal
Build the supplement↔peptide additive-AE screen — the Phase-3 compound-band cross-domain safety check (`vault/design/plan-generation-pipeline-v1.md` Phase 3). The first half of the operator-confirmed two-slice split of the compound-safety + clinical-adjudication slice: **S73 = the screen; S74 = the medical-liaison terminal gate** (the held-line closer).

## What was built
- **`reconcile` behavior 4 (`scripts/plan/orchestrate.py`)** — the bidirectional additive-AE screen. Runs only when BOTH a supplement and a peptide candidate carry a plan. Two detection paths:
  - **shared additive-AE class** — both compounds declare the same `ae_profile.additive_classes` token (`_normalized_ae_classes` set-intersection);
  - **author-declared pairwise interaction** — either author's `ae_profile.interactions` names the other compound by its plan identity (`_declared_interaction_findings`, matched against `_compound_identities`).
  A finding surfaces in `report["additive_ae"]` AND sets `holds["supplements"] = ADDITIVE_AE_HELD`, so `generate_plans` does NOT record the supplement (the peptide draft still records). Mutation-proven RED (disabling the hold → 7+ tests RED; QA + the blind verifier independently re-confirmed at 11 RED). No new store-write stream (the screen holds before the existing `record_plan`).
- **The `ae_profile` author contract** — declared in the `reconciliation` envelope, lifted into `meta` by `compute_plan`'s existing generic path (no per-field code). Grounded canonical AE-class vocabulary (`bleeding-risk`, `serotonergic`, `hepatotoxicity`, `malignancy-risk`, `thrombotic`, `igf-elevation`, `cyp3a4-pgp`, …) drawn from the supplement Core-Rule-5 interaction screen + the peptide Rule-6 H-class axes. Documented in `docs/plan-generation/author-dispatch-process.md`.

## Real-dispatch E2E (integration mandate)
Real supplement-specialist (high-dose fish oil) + peptide-specialist (BPC-157), full profiles inlined, INDEPENDENTLY converged on a shared `bleeding-risk` hemostatic axis AND each named the other compound → the additive pair is HELD (the supplement never reaches the store; the BPC-157 clearance-gated draft records + renders); the clean creatine↔BPC-157 pair (creatine declared an honestly empty `ae_profile`) records both. Envelopes under `docs/plan-generation/examples/compound-screen-*`.

## Review + merge
- **Tier-2** (plan-integrity + QA, full profiles): plan-integrity integrity-clean (screen wires, hold reaches the recording loop, no new store stream, held-line accurate, scope clean) + 2 stale-prose lines + a placeholder commit-email (fixed → GitHub noreply). QA 0 MUST FIX + 5 untested edge cases (incl. the malformed-`ae_profile` fail-open) → 5 tests added.
- **Tier-3** `/review-pr` (6-agent) → 4 deduped findings (one stale docstring caught independently by 4 agents; 3 coverage gaps) → blind triage 4/4 LEGITIMATE → fixed → blind verify 4/4 RESOLVED.
- **`/merge`** PR #154 → `main` (REST rebase under GraphQL exhaustion; full-40-char head-SHA guard + local merge-tree conflict check). Suite 916/3 (worktree) / 917/2 (trunk); core-capability gate green.

## Decisions
- **The malformed-`ae_profile` fail-open is deliberate** — a present-but-malformed declaration is treated as no declaration (the trusted-author runtime-A contract), tested + documented; the fail-loud upgrade is deferred to the S74 gate. Surfaced to the operator, not silently taken.
- The interaction-`with` exact-match has a known precision gap (a parenthetical qualifier — `"fish oil (EPA/DHA)"` vs `"Fish oil"` — misses), beaded for a v2 robustness pass; the shared-class path caught the hold regardless.

## Topology
Built on `feature/compound-ae-screen` in the dedicated `../aplus-s73-screen` worktree (idle main trunk parked on `parking/s73-screen`); merged to `main`; worktree + branches cleaned; main trunk restored. The close artifacts landed via a follow-up `fix/s73-close` PR (the build PR merged first — valid per close step 9, less tidy than S72's single-PR close; carried as an S74 discipline note). Two parallel wiki sessions pushed tesamorelin + thymosin-α1 entries to `origin/main` (zero file overlap — clean rebase).

## Next (S74)
The medical-liaison terminal gate — adjudicates the held additive-AE findings + author conflicts + the supplement↔Rx axis (closes the held line to operator-usable); then the measure + adjust legs. Bead `71s4` remains open.
