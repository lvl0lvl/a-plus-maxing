---
title: Plan-Adjust Dispatch Process (V1, runtime A) — the progression leg
type: guide
status: active
owner: walter
created: 2026-06-20
last_reviewed: 2026-06-20
depends_on: [author-dispatch-process.md]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/plan-generation/adjust-dispatch-process
---

# Plan-Adjust Dispatch Process (V1, runtime A) — the progression leg

The closed loop is **plan → act → measure → adjust** (`design/vision.md`). The plan leg
records `plan::<domain>` (`generate_plan`, the author-dispatch process), the measure leg
records the tracking snapshot (`track.record_tracking`), and the read-back joins them into the
plan-vs-actual view (`track.resolve_plan_progress`). This doc covers the LAST leg: the
**progression** — re-authoring an ADJUSTED plan (de-load / advance / hold) from the progress.

The progression REASONING is the domain SPECIALIST'S, authored at dispatch over the
plan-vs-actual progress — it is **not** computed in `scripts/` (a de-load/advance decision is a
clinical/coaching judgment, never invented in code). `scripts/plan/adjust.py` `adjust_plan` is
the production caller: it reads the progress for the honest "nothing to progress from" boundary,
then records the specialist's adjusted author output through the SAME `generate_plan` path.

## The path (what runs)

1. **Read the progress.** `track.resolve_plan_progress(domain, prior_date, root)` →
   `{plan, tracking, specialist, plan_date, has_plan, has_tracking, ...}` — the prior
   prescription paired with what the operator actually did.
2. **Boundary.** Adjusting requires BOTH a prior plan AND a tracking snapshot. No prior plan is
   *generate*, not adjust; a plan with no tracking is no actual to progress from. Either absent →
   `adjust_plan` records nothing and returns `no-plan-to-adjust-from` / `no-tracking-to-adjust-from`.
3. **Dispatch the specialist with the progress** (below) → capture the ADJUSTED author output.
4. **Record.** `adjust_plan(domain, author_output, store_read, root, prior_date=…, adjust_date=…,
   gates=…)` runs the adjusted output through `generate_plan` (so `assemble`'s four safety filters
   + the workout clearance gate + the domain veto apply to the re-plan exactly as to the initial
   plan's per-domain step — the per-domain floor is NOT bypassed) and records it as a NEW dated
   plan for `adjust_date`. The prior plan +
   tracking are immutable history; `resolve_plan_progress` at the new date reads the adjusted
   prescription.

## The adjust dispatch (runtime A)

The orchestrator dispatches the domain's specialist (the same `TRACKED_DOMAINS` author —
personal-trainer / nutritionist / supplement-specialist — full role profile inlined per
INV-ROLE-INLINING), briefing it with:

- the **prior prescription** (`progress["plan"]`) — what was prescribed last block;
- the **tracked actual** (`progress["tracking"]`) — what the operator actually did (e.g.
  `sets_done`, `volume_lb`, `elapsed_min`, adherence);
- the **de-identified operator summary** (`router.summarize`) + the gated wiki — the same
  state + evidence surface the initial author got.

The specialist returns the SAME universal recommendation contract the author-dispatch process
defines (`{specialist, recommendations: [rec, …]}`, each rec carrying `claim` / `source` /
`confidence_tier` / `reversibility` / `category` / `payload`) — now an ADJUSTED prescription
reasoned from the progress (de-load when the actual fell short or symptoms rose; advance when the
actual met or exceeded the prescription cleanly; hold otherwise). The progression rationale lives
in the rec's `claim` + `payload.detail` (the GRADE-annotated reasoning), exactly as in initial
authoring. The CLAIM-PHRASING RULE and the GRADE discipline from the author-dispatch process
carry over unchanged.

`adjust_plan` does NOT re-run the reasoning — it records the captured output. The de-load/advance
judgment is the specialist's; the code is the wiring + the boundary + the safety floor.

## The per-domain safety floor is NOT bypassed on the re-plan

Because `adjust_plan` records via `generate_plan`, every PER-DOMAIN safety filter the initial
plan's `generate_plan` step passed applies to the adjusted plan too: `assemble`'s attribution /
sourcing-completeness / population-mismatch / class-aware HALT filters, the workout **clearance
gate** (an un-cleared load prescription is dropped from the adjusted plan exactly as from the
initial — the LM-01 July-13 clinician clearance is still the V1 unlock), and the nutrition
RED-S/LEA critical-floor veto. An adjusted plan whose recommendations are all struck /
payload-less records NOTHING and surfaces `generate_plan`'s reason — never a fabricated
adjustment that skipped the per-domain floor.

**Cross-domain reconciliation is a separate step (a V1 adjust boundary).** The cross-domain
holds — `orchestrate`'s nutrition→workout energy-bounce, supplement↔peptide additive-AE,
author-conflict, and supplement↔Rx BPMH — live in the reconciler (`orchestrate.py`), NOT in the
single-domain `generate_plan`. A per-domain adjust via `adjust_plan` does not re-run them, exactly
as the initial plan's per-domain `generate_plan` step does not (only the orchestrator's
cross-domain pass does). A multi-domain re-plan that needs cross-domain reconciliation routes
through `orchestrate` like the initial plan; the per-domain adjust leg is the V1 surface.

## Running + verifying

The deterministic tests (`tests/plan/test_adjust.py`) exercise the path with a FIXTURE adjusted
output (the closed loop, the boundary states, the floor-applies-to-the-re-plan guarantee, the
store-surface battery). The REAL-AGENT progression is verified by a live specialist dispatch over
a SYNTHETIC PII-free progress (a prior plan + a tracking snapshot showing missed/exceeded work):
the specialist authors the adjusted output, `adjust_plan` records it, and the new dated plan
reflects the specialist's de-load/advance reasoning — proving the progression is specialist-
authored, not invented in code (the S73–S77 real-dispatch-E2E pattern).

## What is deliberately NOT here yet

- The dashboard's plan-vs-actual + adjust render surface (a design-led visual surface — Pencil +
  operator sign-off + the design agents, never originated solo).
- A multi-block periodization model (the V1 progression is one adjust step from one observed
  block; a multi-block macrocycle is a later specialist-reasoning surface).
- Peptide progression — peptides are not a `TRACKED_DOMAIN` (peptide tracking is the watch-out
  stream, not a tracked plan), so they do not ride this path.
