---
title: Session 146 — Hand-run care-team plan demo + platform-upgrade design
type: session
status: complete
created: 2026-07-19
review_cadence: none
permalink: a-plus-maxing/sessions/session-146
---

# Session 146 — the plan output, demonstrated + the path to build it natively

Continuation of the S145 plan-render crisis. The operator was near-scrapping the project because `/generate-plan` kept producing the same thin exercise list. This session shifted from fixing the platform render to **demonstrating the target output by hand**, then **designing the platform changes** to produce it natively.

## What happened

1. **Hand-ran the full care-team orchestration** (outside the platform, at the operator's direction): as the care agent, assembled the operator's real intake + wearables (HRV/RHR/SpO₂) + 116 genotypes (identity-stripped per the de-id standard), dispatched all 12 specialists as subagents each operating from its full deployed `.claude/agents/<slug>/agent.md` profile, saved their raw sections, reconciled the cross-domain seams, and rendered ONE integrated plan.
   - **Keystone finding, converged on independently by every specialist:** the positive sleep-apnea screen + wearable corroboration (SpO₂ nadir 77.5%, RHR ~80, HRV ~23) is both the top healthspan lever and the confound that makes the recovery/CV/hormonal reads untrustworthy until worked up. That cross-domain convergence is the proof the synthesis was real, not templated.
   - Grades landed honestly (Training A−, Supplements A, Peptides **C physician-gated**, Sleep/Hormonal B−, etc.); genetics caught nutrition+supplements over-reading the FADS genotype and corrected it to "measure the omega-3 index."
2. **Two artifacts rendered** (scratchpad, the render/acceptance spec): the strategic "Your Plan" (10 graded domains + care team + 24/7 loop) and — after the operator flagged it was still a strategy briefing, not executable — the **"Your Week" daily checklist** (timed workouts to the rep in **lb**, crockpot recipes with a Sunday prep day, supplement/peptide schedule, honoring **yoga Wed + sauna Sat**).
3. **Gap analysis** (operator-directed method): walked the plan as the user, mapping every unanswered "what do I do right now" question per category per day, then the 10 recurring gap classes and the 30/60/90 compounding. This produced the spec for what "followable" means.
4. **Onboarding question bank** extracted → `design/onboarding-question-bank.md`: the durable structured intake, designed around the operator's variability lesson (a naive single-value question is worse than no question; capture the goal + the per-day pattern; onboarding = structure, care agent = day-of specifics).
5. **Platform-upgrade architecture** designed → see the decision note. The scaffolding largely EXISTS (rich `_author_rich`, `orchestrate` reconcile, `care_chat` loop, `/plan-decision` approve gate) — it's wired thin (4 domains, thin render). The fix is a 6-ADR extension.

## Decisions / patterns

- **The two artifacts are now the render acceptance spec** for ADR-E (retire thin `_plan_zone`).
- **The tweak→approve loop is the 24/7 loop, user-triggered:** care_chat writes a config change → detect affected domains → targeted re-author (`plan_driver` already supports `revise_domains`) → re-synthesize + re-render → operator approves via `/plan-decision` → `plan_confirm` locks it. Every user lands here; generation is ~90%, the conversation locks the last 10%.
- **Units: pounds, never kg** — burned into user-scoped memory after repeated operator correction. The strategic artifact was corrected kg→lb.

## Open follow-ups

The 6-ADR platform upgrade (ADR-A widen roster · B onboarding→assembler · C care-agent synthesis · D daily-execution compile+recipes · E rich render · F tweak→approve loop) — beaded, ADR-A first (biggest single lever, doesn't touch the ADR-0032 frozen six). The `fix/wire-generate-plan-button` branch (button-wiring `b62e7189` + regeneration-supersede `78ad21b9`, both verified end-to-end) still needs Tier-3 review + merge.

## Next

Open S147, scope **ADR-A (widen the plan dispatch roster from 4 to the full deployed care team + genetics/labs cross-cutting)**, and run it through the ADR → spec → build plan → task plan → execute → review → merge pipeline.
