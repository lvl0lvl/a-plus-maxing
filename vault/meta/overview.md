---
title: System Overview
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: monthly
permalink: a-plus-maxing/meta/overview
---

# A+ Maxing — System Overview

## Purpose
Personal health agent focused on longevity + body composition. Bryan Johnson Blueprint-inspired but low-budget. Sleep, diet, training, supplementation, biomarker tracking — all in one agent-driven system. Walter is the user; Claude is the agent.

## Architecture
- **Markdown vault** = single source of truth (this directory)
- **LLM agent (Claude)** = reasoner, planner, course-corrector — reads vault, proposes adjustments
- **HTML artifacts** = generated on demand for rich consumption (weekly reviews, monthly recommendations, doctor handouts)
- **Scheduled jobs** = daily/weekly/monthly agent runs that produce artifacts
- **Custom interface** = deferred (Phase C) until friction patterns inform design

## Phases
- **A: Conversational agent** (active) — Walter interacts with Claude directly via this project
- **B: Scheduled artifact generation** (next) — daily/weekly/monthly automated runs produce artifacts in the vault
- **C: Custom interface** (later, ~6 months out) — designed from interaction-log evidence

## Knowledge Layers
- `protocols/` — Walter's current state (what he eats, takes, does)
- `daily/`, `weekly/`, `reviews/` — Walter's outcome data over time
- `library/` — research corpus on peptides, supplements, interventions, biomarkers (cited evidence, tier-rated)
- `experiments/` — Walter's structured n=1 trials linking library evidence to his data
- `dna/` — genetic context
- `labs/` — biomarker history
- `decisions/` — why protocol changes were made (cites library + experiments)
- `interactions/` — friction log informing Phase C
- `design/` — HTML artifact design protocol (cross-session consistency)
- `meta/` — system-level orientation (this file, targets)

## Data Sources
- Apple Health (Watch + iPhone) — HR, HRV, steps, workouts, weight
- Oura Ring (incoming, ~mid May 2026) — sleep stages, HRV, body temp
- Smart scale (TBD, optional) — daily weight trend
- 23andMe raw genotype — Walter has the file; pending drop into `vault/dna/raw/`
- Bloodwork — first panel via new doctor July 2026

## User Context (durable)
- 20 years of consistent training history
- Returning from a January 2026 health issue; currently rebuilding base fitness
- Full home gym: weight cage, dumbbells, TRX, fan bike, treadmill, infrared sauna
- New doctor in July 2026 — sports-nutrition / exercise-oriented; possibly data-friendly

## Near-Term Goal
Arrive at the July 2026 doctor visit with a structured baseline: meal template, supplement stack, training plan, genetic-actionable summary, target biomarker order list. The visit becomes high-leverage (real data, productive conversation) instead of generic.

## Key Decisions
- See `decisions/` for individual records
- No diet app — LLM computes macros/micros from `protocols/meal-template.md`
- Markdown substrate, HTML output (per Thariq's HTML-effectiveness argument)
- A → B → C phased build; C designed from observed friction, not speculation

## Status as of 2026-05-16
- Vault skeleton created
- All `protocols/` files are placeholders awaiting Walter's input
- 23andMe analysis pending raw file
- Oura purchase imminent (within days)
- No bloodwork yet (none available, none ordered until July visit)