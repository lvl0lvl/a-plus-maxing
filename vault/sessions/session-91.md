---
title: Session 91 — conversational-intake Wave-B FOUNDATION (demographic activation + de-identified token vocabulary) built + merged; the real plan-generation engine teed up
type: session
date: 2026-06-23
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-91
---

# Session 91 — conversational-intake Wave-B foundation (autonomous build loop)

**Shape:** the autonomous `/execute-plan` build loop continued from S90. The operator opened with "go" and delegated the Wave-B build autonomously, then mid-session clarified the real plan-generation architecture (a richer multi-agent pipeline) and directed the next step as a proper design pass. S91 ran grounding → build → checkpoint → 3-tier review → `/review-pr` → `/merge` → close. All on synthetic fixtures + mock clients; **0 live-API spend**.

## What was built (PR #237 → `main`)

- **ADR-0018-T1 — demographic activation** (commit `d2f338b`): activated the dead Step-1 demographic placeholders in `vault/design/templates/intake.py` into real POSTing inputs; lit the 4 orphan `SUMMARY_FIELD_SET` tokens (`training-age-band`/`sex-for-dosing`/`bodyweight-band`/`equipment-access-class`) by wiring their capture in `scripts/serve/capture.py`; RECONCILED the `equipment-access-class` double-source — removed the postal-address→equipment-access-class derivation + `_region_class` from `scripts/plan/router.py`, making it a pass-through token sourced from the demographic selection. The form stays objective-demographics-only (the rich sections are chat-only).
- **ADR-0019-T1 — de-identified chat-sourced token vocabulary** (commit `90d064d`): minted 4 kind-2 raw-backed-derived tokens — `dietary-pattern-class` ← `raw-nutrition-free-text`, `supplement-stack-class` ← `raw-supplement-free-text`, `peptide-use-class` ← `raw-peptide-free-text`, `training-volume-band` ← `raw-training-detail-free-text` — in `scripts/plan/router.py` with their capture wiring in `scripts/serve/capture.py`, each consumed by its domain translator.
- **Review fixes** (commits `950ca43` + `da43f14`): the `not-discussed` absent-source honesty sentinel; `_age_band` strip+4-digit+1900..current-year validation; `_training_volume_band` `\d{1,2}` regex + clamp; empty-parts guards in `_supplement_stack_class`/`_peptide_use_class`; allergy-checked-first `_dietary_pattern_class`; dead-CSS removal.

## De-identification (the crown jewel)

The 8j6 `summarize` gate does NOT run on the raw-backed-derived path (`router.py` runs no `scan_text` there) — so each of the 8 new derived tokens (4 demographic + 4 chat-sourced) is de-identified by its DERIVATION'S COARSENESS, proven by an INDEPENDENT per-token output scan (a crafted raw value seeded at the source store item → 0 raw in the emitted token). `training-age-band` is a born-decade band (raw birth year never in token); `bodyweight-band` a coarse band (never raw kg); the 4 chat tokens coarse classes (never raw food/supplement/peptide names). The disjointness tripwires (`set(_RAW_TO_FIELD)⊆EXCLUDED_RAW_PII`, `SUMMARY_FIELD_SET.isdisjoint(EXCLUDED_RAW_PII)`, `WIRED_TOKENS⊆SUMMARY_FIELD_SET`) stay green at module load. Security review: 0 findings, executed.

## The operator's plan-generation architecture (mid-session clarification)

The operator rejected the "single model call" framing and described the real engine: an API (no-train) model de-identifies PII **in** → a SUBSCRIPTION orchestrator runs the SPECIALISTS as agents (like the autonomous build pipeline) → a JUDGE verify step → a `/review-pr`-style multi-agent SAFETY review of the plan → revise → the API agent re-inserts the necessary PII **out** + builds the (reviewed) tracking/testing → a unified maintained format (HTML) the API agent adjusts as wearables/labs arrive ("at some later date it can all be API or a local model or some combo"). This SUPERSEDES `ADR-0017-T2`'s minimal-author premise — so ADR-0017-T2 was NOT built here; the engine gets its own design pass (S92, via the full autonomous build pipeline).

## Reviews

- **plan-integrity** (read-only grounding/gating): CONDITIONAL GO. Caught the **NOTE-T3-1 production-wiring gap** — `pipeline.run_generation → orchestrate.generate_plans → compute_plan` forwards no `client=`, so production rides `_FixedEnvelopeClient`; the planned end-to-end would have proven a `generate_plan`-seam path production never runs (the core-capability-not-really-closed trap). Resolved by the Architect as a THIN `client=` forward + a spec amendment (`docs/spec/.wave-b-note-t3-1-amendment.md`), deferred to the engine. Also caught the ADR-0018-T1 manifest gap (21 coupled `test_router.py` cases).
- **Tier-1** per-task TDD with executed negative controls. The SE correctly HALTED on the equipment-reconciliation's 21-test coupling (not the 1 the recipe anticipated); the orchestrator adjudicated extend-the-manifest + UPDATE the fixtures to the new sourcing (the "update earlier-phase tests when behavior changes" discipline — not weakening; the updated tests re-proven failing-capable).
- **Tier-3 `/review-pr`** 7-agent (the standard 6 + a design-reviewer for the activated UI) over the LOCAL three-dot diff (GraphQL exhausted), independence INTACT (profile-less blind-triage Phase 3 + EXECUTED blind-verify Phase 7): 12 findings → 9 LEGITIMATE fixed → 9/9 blind-verified RESOLVED; 2 OUT_OF_SCOPE/DEFERRED → bead `f0gh`. The 9 were free-text-deriver value-domain bugs (the `AP-SELF-REVIEW-UNDER-PROBES-INTERACTION-SURFACE` class) + the always-set-token honesty gap. Design-reviewer PASS (on-theme Clinical Light, honest labels, no sparklines).

## State at close

- pytest **1472 passed / 2 skipped**; `generate_plan.py`/`assemble.py`/`store.py`/`keying.py`/`ingest/*` byte-unchanged; the store-adversarial battery non-tautological (category-4 RED).
- **No new PF.** The layered pipeline worked as designed (plan-integrity caught the NOTE-T3-1 trap + manifest gap; the SE HALTED rather than weaken tests; `/review-pr` caught 9 real defects; the architecture clarification was engaged honestly, not rubber-stamped). Disclosure ledger: 5 caught, all self/gate, 0 to operator.
- New bead `f0gh` (chat-elicitation wiring — the 4 ADR-0019 tokens are minted but `chat.py` never asks the nutrition/supplement/peptide/training domains; co-design with the engine's conversation stage). Carry-over: `j432`/`pqb0`/`zwow`/`v70t`/`f22s`/`oves`/`02m1` + the prior set.
- A process note (disclosure ledger): the uncommitted S91 scope contract was reverted by a sub-agent `git checkout`/`restore` during the build; re-authored at close. Lesson — commit the scope contract before dispatching build agents.

## Next (S92)

The `plan-generation-engine` design pass + build via the FULL autonomous build pipeline: refresh skills_library (new commands), `/create-adr` the engine ADR, then ADR→spec→build-plan→task-plan→`/execute-plan`. Be extra-engaged monitoring the pipeline (it is the live reference model for how the health-plan pipeline should be organized); bead any new-skill/command rough edges. Carried engine obligations: NOTE-T3-1 thin `client=` forward (spec amendment); the chat-elicitation wiring (`f0gh`); the DESIGN-ESCALATION (stale plan-gen docs describe the superseded runtime-A interactive-dispatch model — reconcile with the programmatic-orchestrator model).
