---
title: Session 72 — the cross-domain reconciler (step-4 integration terminal function)
type: session
date: 2026-06-18
permalink: a-plus-maxing/sessions/session-72
---

# Session 72 — cross-domain reconciler (PR #149, bead 71s4)

## Goal

Build the cross-domain reconciler — the orchestrator terminal function (design `plan-generation-pipeline-v1.md` decision 4, part 1): a `/generate-plan` orchestrator that computes all four candidate plans in one pass, runs the nutrition→workout energy bounce + cross-domain overlap detection, and records the reconciled set. The first half of the held line (S73 = the compound-safety + clinical-adjudication half).

## What was built

- **`scripts/plan/generate_plan.py`** — refactored: `compute_plan` (compute the candidate, NO record) split from `generate_plan` (= `compute_plan` + `record_plan`). The single-domain public contract is unchanged (45 existing tests + the `--self-test` held; plan-integrity confirmed signature + return-shape preservation).
- **`scripts/plan/orchestrate.py`** (NEW) — `generate_plans(authors, store_read, root, *, plan_date, gates, reauthor)` + `reconcile(candidates)`. Three reconcile behaviors:
  1. **RED-S/LEA cross-domain short-circuit** (design Phase 0.5) — a tripped nutrition critical-floor screen ALSO holds the energy-prescribing workout plan to clinical-care routing.
  2. **The nutrition→workout energy BOUNCE** (Phase 2) — `sustains:false` → bounce → re-author once under the sustainable-energy ceiling → record reduced, else HOLD (never an un-fuelable load).
  3. **Cross-domain overlap + author-declared conflict DETECTION** (V1 detect+report; adjudication is S73). Overlap dedupes distinct domains; conflict attribution is non-spoofable.
- **`tests/plan/test_orchestrate.py`** (NEW) — 15 build tests + the review-driven additions (the two safety behaviors mutation-proven RED; the store-adversarial battery at the `generate_plans` boundary; the bounce ceiling-None guard; cross-stream nutrition isolation; the clearance gate through the orchestrator; overlap dedup; multi-author conflict accumulation).
- **`docs/plan-generation/author-dispatch-process.md`** — documents the orchestrator + reconciler + the `reconciliation` envelope contract (`energy_cost_kcal`, `energy_budget`, the optional `bounce_reason` annotation, author-declared `conflicts`).
- **`docs/plan-generation/examples/cross-domain-*`** (NEW, 5 files) — the captured REAL-dispatch envelopes for both reconciler paths (no-bounce + bounce).
- No new store-write stream (records via the existing `record_plan`).

## Real-dispatch E2E (the integration mandate)

Both reconciler paths verified end-to-end over real author reasoning (full profiles inlined per INV-ROLE-INLINING; PII-free synthetic operator):

- **No-bounce path:** the real personal-trainer authored a clearance-deferred 5-exercise session (no load — clearance gate honored; 130-kcal cost), the real nutritionist set a 2150-kcal day plan and returned `sustains:true` (the deferred session is well within the budget). Both recorded; dashboard rendered.
- **Bounce path:** a future-state cleared 700-kcal session → the real nutritionist's `sustains:false` (a ~650-kcal deficit against the constrained intake; ceiling 300) → the trainer re-authored a reduced 260-kcal session → the reduced plan recorded; the bounced 700-kcal load never reached the store; dashboard rendered the reduced plan.

## Review + outcome

- **Tier-2:** plan-integrity (integrity-clean on all seams; flagged the design doc stale) + QA (caught the vacuous bounce store-safety assertion; coverage gaps) → 7 findings fixed.
- **Tier-3:** `/review-pr` 6-agent (over the local diff, GraphQL exhausted) → ~20 deduped findings → profile-less blind triage → 10 LEGITIMATE fixed + blind-verified 10/10 RESOLVED; 1 OUT_OF_SCOPE → bead `axm7`; 6 NOT_A_BUG / 2 NOT_ACTIONABLE / 1 HALLUCINATED. The most material fix: F01, a real dict-spread bug letting an author key override the orchestrator's conflict attribution.
- **Merge:** PR #149 rebase-merged to `main` (REST under GraphQL exhaustion).
- **Suite:** 899 passed / 3 skipped. Core-capability gate green; close-audit + harvest-gate pass.

## Decisions

- **Two-slice split (operator-confirmed at open):** S72 = the orchestrator reconciler (integration terminal function); S73 = the supplement↔peptide additive-AE screen + the medical-liaison terminal gate (clinical-adjudication terminal function). Grounded in design decision 4 ("two terminal functions, not one") + minimal-path-first.
- The bounce is exercised via a caller-provided `reauthor` hook (runtime A: a second personal-trainer dispatch under the energy ceiling) — keeps the mechanism testable + faithful.

## Next (S73)

The compound-safety + clinical-adjudication slice: the additive-AE screen + the medical-liaison terminal gate (the gate to operator-usable), then the measure leg (a `record_plan_tracking` caller) + the adjust leg.
