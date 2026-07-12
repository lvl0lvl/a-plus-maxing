---
title: Session 127
type: session
date: 2026-07-11
permalink: a-plus-maxing/sessions/session-127
---

# Session 127 — the product reckoning + the comprehensive-plan re-architecture ADRs

## What happened
A routine session (open → run the operator-present LIVE plan → close) pivoted into a product reckoning. The operator judged the live-generated plan **"overwhelmingly lame"** and named the true gap: the platform never built the intended product — Step-1 care-agent conversation → Step-2 farm briefs to each specialist → Step-3 specialists research+recommend → Step-4 care-agent reconciles+tailors → a comprehensive, personal, periodized, 24/7-monitored plan.

## Root cause (code-grounded)
- **DATA-COLLAPSE** — `router.summarize` collapses the operator's real detail to coarse band tokens (`training-volume-band`, `peptide-use-class`) before any specialist sees it; the closed `SUMMARY_FIELD_SET` (18 tokens) is the ceiling.
- **NO-LOOP** — a one-shot generator; only 4 of 18 specialists wired; no plan-compiled monitoring/adjustment.

## Deliverables
- **Design:** `design/health-plan-spec.md` (what a quality plan contains), `design/plan-platform-architecture.md` (the 7-component control system + UI map), `design/specialist-plan-contracts.md` (the **18 specialist contracts** — inputs / monitoring / tracking / analysis→plan, each authored from its FULL profile via sequential-thinking). Plus a Pencil Plan-page mockup (`design/plan-page-mockup.png`). **These carry the operator's real health data → kept UNSTAGED (public repo).**
- **ADRs (committed on `feature/comprehensive-plan-adr`):** the plan-path re-architecture formalized via the FULL 8-phase `/create-adr` rigor loop.
  - **ADR-0041** uniform specialist DOMAIN PROGRAM output schema (HARD)
  - **ADR-0042** Context Assembler feeding specialists the full identity-stripped record (HARD; genetics carve-out preserves the S102 crown jewel)
  - **ADR-0043** care agent as the plan Orchestrator (MODERATE prompt / HARD on the `orchestrate.reconcile` safety surface)
  - **ADR-0044** comprehensive Plan Model superseding the thin `plan_schema` (HARD — the biggest data-model door)
  - **ADR-0045** plan-compiled monitoring config + tiered adjustment executor (MODERATE)
  - **ADR-0046** specialist-dispatch scale-up 4→15+ with progressive activation (MODERATE)
  - Each judged ≥9/10 on every rubric dimension, whole-set red-teamed (RT-006/007/008 caught + final-fixed), + 17 reciprocal backfills into ADR-0001..0040.

## The frozen spine
The ADRs **deliberately supersede** the ADR-0032 EXTEND-NOT-REBUILD freeze on the plan-authoring + record surfaces — operator-signed-off at the Phase-1 gate, classified HARD, not a silent break. De-id stays PARKED (only pure identity stripped; all health substance flows). No `scripts/` code changed this session (the ADRs are docs).

## Process failures promoted (both operator-surfaced)
- **PF-S127-01** — the core-capability gate measured PLUMBING-WIRED (a 4-domain plan records) not PRODUCT-REALIZED (the orchestrated comprehensive plan); ~60 days of "core capability PROVEN" masked that the intended product was never built. The gate was tautological.
- **PF-S127-02** — asserted operator facts not grounded in the full record (invented "vasectomy" from "snip"=SNP; falsely denied the operator said "norwegian 4×4"/"zone 2" when it was in un-read intake free-text).

## Next
`/create-spec` on ADR-0041..0046 → build-plan → task-plan → execute (bead `a-plus-maxing-xzs9`) — the Slice-1 build (assembler + orchestrator prompt + DOMAIN PROGRAM schema + comprehensive plan model). The orchestrator-prompt rewrite is the fastest visible proof.