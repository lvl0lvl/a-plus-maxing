---
title: Dashboard v1 — Approved Target Design
type: design
status: approved
owner: walter
created: 2026-06-10
last_reviewed: 2026-06-10
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/design/dashboard-v1-design
---

# Dashboard v1 — Approved Target Design

**Status:** Walter signed off as the v1 target on 2026-06-10 (S47). v2 iterates on this
and adds the other screens. The working Pencil mock was saved to disk by the operator
(location operator-held; this note is the durable design record).

Mockup-first per `feedback-dashboard-pencil-mockups`. This is the DESIGN target — the
build is a separate, post-sign-off effort (see Build implications below). It is the
frozen target the dashboard build beads are measured against.

## What it is

A plan-forward "Today" command center — not a lab report. The operator opens it to see
**today's plan (workout, nutrition, supplements, peptides) and how they're tracking
against it**, plus readiness at a glance. Inspired by Whoop (readiness rings, strain) and
Apple Health / MacroFactor / Strong (summary cards, trend cells, plan-as-spine tracking).
The differentiator vs generic trackers: **the plan is the spine and tracking hangs off
it** — every surface lists the actual plan (sets, meals, stack, protocol) and lets you
log against it, rather than presenting an empty log.

## Zones (top to bottom, single scroll for v1)

1. **Hero — readiness.** Three rings (Recovery %, Sleep %, Strain) + a "primed to train"
   readout + HRV / RHR / Sleep / Resp chips. Answers "how is my body today."
2. **Week calendar.** 7-day strip, today highlighted, color-coded events (Training / Lab
   draw / Check-in / Appointment), prev/next nav + **Month expander** (caret) to full month.
3. **Today's plan** — the dominant zone, four specialist-attributed app-screen cards:
   - **Workout** (personal-trainer): live session — elapsed / volume / sets / live HR,
     today's steps+move+exercise from the watch, and the plan's exercises with **per-set
     completion dots**, rest timer, Resume.
   - **Nutrition** (nutritionist): calorie budget (Goal − Food + Exercise = Remaining),
     macro bars, and **today's planned meals listed from the diet plan** with one-tap Log
     (breakfast logged → lunch up next → dinner/snack queued) + water.
   - **Supplements** (supplement-specialist): today's stack with taken/pending state.
   - **Peptides** (peptide-specialist): protocol (compound · dose · route · site · week of
     cycle), watch-out check-ins, risk tier, link to wiki evidence.
4. **Performance & trends.** Metric cells (Recovery, HRV, Sleep, Bodyweight, est. 1RM, RHR)
   with **bar/column sparklines** (NOT line paths — see decisions) + trend chips.
5. **Your care team — all 16 domain specialists** in a 4×4 grid, each with what it tracks +
   a status. The 4 internal build/review roles (architect, implementer, edge-case, safety)
   are intentionally OFF — they don't track operator data.
6. **Goals & progress.** Progress bars toward targets (overhead pressing, bodyweight, 1RM)
   + the July MD-visit landmark (LM-01).
7. **Labs & bloodwork.** Demoted to a compact supporting strip (biomarker chips + pending
   draws + latest physician note). Labs are detail, not the headline.

## Design decisions (load-bearing)

- **Plan-as-spine.** Workout set-dots, nutrition planned-meals, supplement stack, peptide
  protocol, and the attributed `assemble()` plan all follow one pattern: render the plan,
  hang live tracking off it. This is the product's differentiator.
- **Palette.** The locked colorblind-safe semantic palette (`good #117733`, `watch #DDAA33`,
  `concern #882255`, `ink #1A1A1A`, `muted #555`, `paper #FFFFFF`) for data state, plus a
  category-accent set for surfaces (training blue `#1F6FEB`, nutrition orange `#E8833A`,
  supplements teal `#0E9AA3`, peptides purple `#7C3AED`, sleep indigo `#5B5BD6`). Light
  theme (matches the print-safe artifact palette + readability); dark-hero is a v2 option.
- **Sparklines = bars, not paths.** Hand-authored SVG `path` geometry rendered inconsistently
  in the layout engine ("janky"). The approved approach is bottom-aligned rectangles in a
  flex row (gradient-shaded by height) — robust, contained, and reads cleanly. The build
  should generate bar columns, not polylines.
- **Honesty caveats are part of the design** (inform-class specialists): cardio carries the
  causal-vs-associational split; delta chips are direction-only (no good/bad coloring) until
  per-marker polarity exists; genetics shows DTC = unconfirmed; lymphatic shows "no validated
  routine test"; dermatology routes lesions to a clinician. These are not decoration — they
  encode the deployed agents' refusal/over-claim floors.

## Build implications (the data-model delta — this is NOT free)

The mock is ahead of the current build. Today the store holds only biomarker / panel /
watch-out / feedback streams (`{item, timepoint, source, value}` via `loop_schema`), and
`scripts/plan/assemble.py` composes an attributed plan dict that has **no render surface**. Building
this dashboard requires, scoped as its own effort:

- **Biomarker metadata** (per-marker units + reference_range + good-direction polarity).
  Resolves `y0h0`; replaces the `component_set.state_for` name-hash placeholder with real
  in-range/out-of-range state; unblocks `router._trend_token` (which currently RAISES on a
  directional change for lack of polarity) → real improving/regressing.
- **Plan-content schemas** for workout (exercises/sets/reps/%1RM/RPE), nutrition (meal plan +
  macro targets), supplements (stack + timing), peptides (protocol + site rotation + cycle).
  This generalizes `1oh` beyond "plans-on-dashboard" to structured daily plans + logging.
- **Wearable ingestion → derived scores.** Adapters exist (`scripts/ingest/adapters/`:
  oura/whoop/garmin/healthkit); recovery/strain/sleep SCORING + steps/HR/activity surfacing
  are new. Gated on real operator data (LM-02 Oura baseline).
- **Type-routed unified render surface.** Route by stream type (typed reads) so non-numeric
  streams never hit a numeric viz. Resolves `i1t` (crash), `i2yw` (unify the two surfaces),
  `azf` (clean labels).
- **Calendar/event model** (training days, lab-draw due dates, check-in cadence, appointments).
- **Goal-progress model** (`vault/meta/goals.md` is currently `status: scaffold`).
- **Per-specialist rollup** for the 16 care-team cards (summarize each domain's tracked state).

## Bead resolution map

| Bead | Resolved by the approved design |
|------|----------------------------------|
| `i1t` (P1) | Unified surface routes by stream TYPE (typed reads); biomarkers → numeric viz, panels/watch-outs/feedback → typed renders. No string value reaches a numeric sparkline. |
| `azf` (P2) | Clean labels throughout ("Ferritin", never `biomarker::ferritin`). |
| `1oh` (P2) | The entire Today's-plan zone + a render surface for `assemble()` output; generalized to structured daily plans (workout/nutrition/supplements/peptides). |
| `i2yw` (P2) | Stats zone merges `dashboard.py` value-cards + `render_views.py` matrix/projection into one type-routed surface. |
| `y0h0` (P3) | Cards carry units, dates, deltas, ranges, state dots — gated on the new biomarker metadata. |
| `04uk` (P2) | The design forces a mixed store; the test seeds biomarker+panel+watch-out+feedback and asserts no crash + correct type-routing (the coverage that hid the F1 crash). |
