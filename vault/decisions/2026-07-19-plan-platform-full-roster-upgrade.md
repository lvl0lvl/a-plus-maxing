---
title: Plan platform — full-roster upgrade (the 6-ADR path to the demonstrated output)
type: decision
status: accepted
created: 2026-07-19
permalink: a-plus-maxing/decisions/2026-07-19-plan-platform-full-roster-upgrade
---

# Decision: extend the plan pipeline to produce the demonstrated care-team output

## Context

S146 hand-ran the care-team orchestration and rendered the target output (two artifacts: strategic "Your Plan" + executable "Your Week"). The platform today produces a thin 4-domain exercise list. Grounding the gap against the live code showed the machinery mostly EXISTS but is wired thin:

- **Dispatch is 4 domains** — `plan_driver._ROLE_OF_DOMAIN` / `plan_schema.PLAN_DOMAINS` = {workout→personal-trainer, nutrition→nutritionist, supplements→supplement-specialist, peptides→peptide-specialist}. This is the single biggest reason the plan is minimal.
- **Cross-domain step is safety-only** — `orchestrate.generate_plans` (FROZEN) reconciles the 4 for holds (energy bounce, supplement↔Rx BPMH), not the integrated narrative/calendar/goals.
- **Render is thin** — `_plan_zone` (`vault/design/templates/app_shell.py:194`) collapses the rich `plan-model::` store to a `<ul>` of exercises.
- **Rich authoring exists** — `_author_rich` writes the rich `plan-model::` `domain_programs` (prescription/rationale/GRADE/monitoring/adjustment_rules/required_labs); the render discards it.
- **Care-chat loop exists** — `care_chat.respond` / `.synthesize`; per-domain approve gate exists — `/plan-decision` → `plan_confirm`.

## Decision

Ship the demonstrated output as a **6-ADR extension** (not a rebuild), against `design/plan-platform-architecture.md` (the specialist contracts were "Slice 1"):

- **ADR-A — full-roster dispatch.** Widen from 4 to the full deployed roster in `design/specialist-plan-contracts.md` (10 renderable domains + genetics/labs cross-cutting run first). Each maps to its deployed `.claude/agents/<slug>` profile. **First — biggest single lever, does not touch the ADR-0032 frozen six.** (~12 contract-grounded author calls/generation vs 4 — spend note.)
- **ADR-B — onboarding → assembler.** Wire `design/onboarding-question-bank.md` capture into `context_assembler` (per-day schedule grid, loads in lb, equipment, injury map, med/peptide schedules + ingredient panels, cooking-time budget, devices/labs access, clinician-oversight flag, concrete goals).
- **ADR-C — care-agent synthesis layer.** Turn N sections into ONE plan: keystone elevation, narrative, weekly calendar (honoring schedule constraints), dated goals, care-team roster, holds.
- **ADR-D — daily-execution compile + recipes.** Compile approved domain programs + schedule config into the daily checklist + crockpot recipe bank + supplement/peptide daily schedule.
- **ADR-E — rich render.** Retire thin `_plan_zone`; the two S146 artifacts are the acceptance target. Data already lands in `plan-model::`.
- **ADR-F — tweak → approve loop.** Wire care_chat: config change → detect affected domains → targeted re-author (`revise_domains`) → re-synthesize + re-render → operator approves via `/plan-decision` → `plan_confirm` locks. The 24/7 loop, user-triggered.

## Consequences

- Acceptance specs are concrete + already authored: the two artifacts (render) + `onboarding-question-bank.md` (intake).
- Roster-widening + render are clean of the frozen six.
- The full 6-ADR build is multi-session, driven per `/run-pipeline` stop rules.
- Cost rises (~12 author calls/generation); the operator-present LIVE run remains the load-bearing non-mock verification.

Relates to: [[operator-health-plan-vision]] · `design/health-plan-spec.md` · `design/plan-page-mockup.png` · `design/specialist-plan-contracts.md`.
