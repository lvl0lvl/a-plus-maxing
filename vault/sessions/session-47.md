---
title: Session 47 — dashboard v1 target design (mockup-first) signed off
type: note
owner: Walter McGivney
created: 2026-06-10
last_reviewed: 2026-06-10
status: active
permalink: a-plus-maxing/sessions/session-47
---

# Session 47 (2026-06-10)

## Goal

Mockup-first per the standing directive (`feedback-dashboard-pencil-mockups`): mock the
unified stats + plans + tracking dashboard in Pencil, iterate to Walter's sign-off, and
capture the approved design as the frozen build target. No build this session (pure
design/docs).

## What shipped

### The v1 dashboard target design — SIGNED OFF

A plan-forward Whoop / Apple-Health "Today" command center, mocked in a NEW `.pen`
(the operator's open canvas left untouched), iterated to sign-off across 4 feedback
rounds. **Seven zones:**

1. **Hero — readiness:** Recovery / Sleep / Strain rings + "primed to train" readout +
   HRV/RHR/Sleep/Resp chips.
2. **Week calendar:** 7-day strip, today highlighted, color-coded events (Training / Lab
   draw / Check-in / Appointment), prev/next + **Month** expander.
3. **Today's plan** (dominant): Workout / Nutrition / Supplements / Peptides as live
   app-screens — **live tracking layered on the plan** (per-set completion dots + live
   HR/steps; planned-meal logging with a calorie budget + macro bars). The differentiator.
4. **Performance & trends:** 6 metric cells with bar-column sparklines + trend chips.
5. **Your care team:** ALL 16 domain specialists in a 4×4 grid, each with what it tracks +
   a status (the 4 internal build/review roles correctly OFF).
6. **Goals & progress:** progress bars + the July MD-visit landmark.
7. **Labs:** demoted to a compact supporting strip.

### The iteration loop (what each round changed)

- **Round 1 → 2:** "anemic" lab-report → comprehensive plan-forward command center
  (Whoop/Apple inspiration the operator had asked for; ferritin demoted from the lead).
- **Round 2 → 3:** sparkline jank fixed (twice — path geometry → robust **bar columns**);
  added the weekly calendar with month-expand; added specialist sections.
- **Round 3 → 4:** specialist undercount (9 → all 16) corrected; Workout + Nutrition rebuilt
  as real app-screens with live data on the plan.

### Captured (the frozen target)

`vault/design/dashboard-v1-design.md` — the approved design + load-bearing decisions
(plan-as-spine, locked colorblind-safe palette + category accents, bars-not-paths, the
honesty caveats that encode the specialists' inform-class floors) + the build's
**data-model delta** + the bead-resolution map. All 6 dashboard beads (`i1t`/`azf`/`1oh`/
`i2yw`/`y0h0`/`04uk`) annotated with how the design resolves each.

## The build is NOT free (data-model delta)

The mock is ahead of the current build (store holds only biomarker/panel/watch-out/feedback
streams; `assemble()` composes an attributed plan dict with no render surface). Building it
needs: per-biomarker metadata (units+range+polarity — also replaces the `state_for`
name-hash placeholder + unblocks `router._trend_token` which RAISES); plan-content schemas
(workout/nutrition/supplement/peptide); wearable→recovery/strain/sleep scoring; a
type-routed unified render surface; calendar + goal-progress models. Scoped for S48 as its
own ordered sub-effort (per the design note + HANDOFF What-Is-Next).

## Metrics

Suite **340 passed / 2 skipped** (unchanged — pure design/docs, no production code touched).
branch-completeness 0 (20 agents) at open + close. No hook/settings/INVARIANTS/agent edits.
No `/review-pr`/`/merge`/`/aplus-research` dispatch (PF-S39-01/S40-01 N/A this session).

## Beads

Closed: none. Annotated: `i1t`/`azf`/`1oh`/`i2yw`/`y0h0`/`04uk` (the 6 dashboard beads).

## Drift / PF

All three drift axes clean (see HANDOFF S47 close). No new PF-class entries (see HANDOFF
S47 PF attestation). PF-S6-01 HELD (verified all 6 beads' live state + the deployed-agent
roster + the full data-model source before writing). PF-S13-01 HELD (open + close from the
files).
