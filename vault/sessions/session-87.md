---
title: Session 87 — operator-data enablement, the intake-wiring audit, and the conversational-intake VISION PIVOT
type: session
date: 2026-06-22
owner: Walter McGivney
status: complete
---

# Session 87 — the intake-wiring audit + the vision pivot

**Shape:** an emergent session (no upfront scope contract). It began as "sync my trunk so I can test the intake," and through use became a full wiring audit and then a confirmed **vision pivot** — the headline outcome.

## What happened

1. **Operator-data enablement — the stranded trunk synced.** The operator's MAIN checkout (`a-plus-maxing`) was stranded on `feature/apple-health-adapter` (`d99e437`, 41 commits behind) so it lacked the merged intake server. Synced `main` → `origin/main` (`dfd44e8`) while **preserving the parallel-wiki vault WIP**: a full labeled backup stash (`stash@{0}`), 6 cleanly-re-layable files re-laid as uncommitted changes, and 3 genuinely-diverged `bpc-157` files left at main's version (WIP in the stash for the operator to reconcile — never auto-merged their research). The `.beads` churn + a live basic-memory daemon (re-adding `permalink:` frontmatter) were noted as benign.

2. **Server smoke test.** `python -m scripts.serve` (loopback `127.0.0.1:8765`) started from the operator's real checkout and served the 6-step wizard (HTTP 200, the capture fields). The operator then tried to use it.

3. **The intake-wiring audit (operator-triggered, "I can't input my birth year").** Step-1's "About you" boxes (birth year, sex, bodyweight, equipment) are DEAD static placeholders that capture nothing. The full audit: only **6 signals reach the planner** (goal-domains/goal-targets/goal-priority-order/hard-limits + recovery-status-band + train-around→active-issue-class). Everything else routes record-only and **never reaches the planner** (training specifics: lifts/split/volume/experience; all of nutrition), and **four model-bound tokens are ORPHANS** with no working input (`sex-for-dosing`, `bodyweight-band`, `equipment-access-class`, `training-age-band`). The form collects far more than it feeds the plan.

4. **The VISION PIVOT (operator-confirmed).** The operator's read: the rigid form is too lossy — "workout" can't encode cardio-vs-strength-vs-hypertrophy, and a plan's value is the *interplay* (peptide ⟷ goal ⟷ recovery ⟷ bloodwork ⟷ DNA), which needs dialogue. **Decision:** the FORM keeps only demographics + content uploads (DNA/HealthKit/labs); ALL the rich sections become a **conversational intake agent** (targeted questions + back-and-forth) that writes de-identified facts to the existing store. **Model:** no-train API for V1 (faster to working + generates baselines for later local-model eval) → **local model is the North Star** (deferred but committed). This introduces the **first model client** in the codebase and **relaxes ADR-0001's zero-egress** (raw conversation → a no-train API) — explicitly signed off (the guard-loosening discipline honored). It also finally addresses the core-capability gap (the system never had a model client; plan generation was never wired). Durably recorded in the user memory (`project_vision_pivot_conversational_intake`) + an epic bead (`w3y8`).

## PF this session

**PF-S87-01 (plumbing-reviewed-not-end-to-end-capability, operator-caught).** The S86 Wave-B intake passed its 3-tier review on PII plumbing + the wired fields, but no review asked "does the captured intake produce a *usable plan*?" — so the dead inputs + orphan tokens + record-only-everything surfaced only on operator use. Lessons: a non-functional input is a functional defect (not a cosmetic "minor"); apply the core-capability-first gate to a feature's end-to-end output, not just its unit/boundary tests. Forward-wired into the conversational-intake build's acceptance.

## Next (S88 — AUTONOMOUS)

Build the conversational intake agent through the full pipeline (ADR via `/create-adr` → `design/vision.md` update → design pass → build via `/execute-plan` + 3-tier review → `/merge` → close), autonomously per the operator's standing directive. Full grounding: epic `w3y8` + the memory + this note. Verify END-TO-END capability (a usable plan), not just chat plumbing (PF-S87-01).
