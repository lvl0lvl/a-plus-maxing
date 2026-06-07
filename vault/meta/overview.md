---
title: System Overview
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-06-07
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
- `library/` — research corpus on peptides, supplements, interventions, biomarkers (cited evidence, tier-rated); base source whitelist at `library/_source-whitelist.md`
- `compounds/` — canonical compound entries (peptides, supplements, hormones, etc.) — flat folder, class is metadata
- `biomarkers/` — canonical biomarker entries — populated as labs / wearable data ingested
- `experiments/` — Walter's structured n=1 trials linking library evidence to his data
- `dna/` — genetic context
- `labs/` — biomarker history
- `decisions/` — why protocol changes were made (cites library + experiments)
- `interactions/` — friction log informing Phase C
- `design/` — HTML artifact design protocol (cross-session consistency)
- `meta/` — system-level orientation: this file + `targets.md` + `operator-profile.md` (slow-changing Walter context) + `current-state.md` (fast-changing snapshot) + `goals.md` (hard limits + doctor-handout queue) + `contradictions.md` (active contradictions log) + `index.md` (catalog of every wiki entity page) + `log.md` (append-only wiki operation log)

## Wiki Schema (added S2 2026-05-23)
`vault/WIKI.md` defines the queryable knowledge-base layer:
- **Entity types** with templates: compounds, biomarkers, protocols, parameters, decisions
- **Agent consumer roster** — 14 specialist agents (personal-trainer, labs-specialist, nutritionist, supplement-specialist, peptide-specialist, endocrine-specialist, lymphatic-specialist, gi-specialist, cardiovascular-specialist, sleep-coach, recovery-specialist, longevity-strategist, mental-performance-coach, medical-liaison) — agent profiles drafted on-demand, not speculatively
- **Source whitelist** with 5 standard tiers + Tier 2.7 (practitioner_protocol for prescribing-practice claims) + Tier NE (non-English literature) + 12-tag type enum + admissibility matrix
- Distinction between **library research** (goal-agnostic canonical entries) and **specialist-agent dispatches** (operator-personalized queries against the wiki)

## Research Pipeline (added S2 2026-05-23)
`.claude/skills/aplus-research/` wraps the global `deep-research` with mechanically enforced gates. Six blocking gates with JSON-schema-validated verdicts: 2.75 SCOPE, 3.5 JUDGE (paired retrieval+judge), 4.75 INTEGRITY (incl IC-13 per-citation corpus scoping), 6 CRITIQUE (deep+), 7.5 RISK-FLOOR (compounds), 8.5 LAYERS (standard+ compounds). Three health-specific gates not in deep-research: population-mismatch, risk-floor, concentration-audit. Use `/aplus-research` for any wiki-bound research from S3 forward.

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

## Status as of 2026-06-07 (S40) — V1 build execution wave-state

The V1 build executes `docs/build-plan/build-plan-v1-full.md` (18 tasks across 7 topological waves). Built **16/18** leaves; verified sound against every runnable build-plan checkpoint (full suite 227 passed / 2 skipped; Wave 2→3 + 3→4 + 4→5 + 5→6 checkpoint gates green; 0 dangling references to unbuilt modules). S40 completed Wave 5 via `/execute-plan` WAVE mode (Phase C) — the three-tier review caught + fixed a **Critical HALT compound-hard-limit fail-open** the builder's 227 tests + Tier-2 both missed (Tier-3 SEC-1: a rec contradicting the 2nd clause of a compound limit shipped actionable) before the W5→W6 checkpoint gate.

- **Wave 1** — PII-boundary / store-keying / render-size spikes — ✅ complete (`394`, `bez`, `qbb`)
- **Wave 2** — NDJSON store + egress/PII guard — ✅ complete (`89a`, `e9m`)
- **Wave 3** — ingest routine, render engine, gitignore-hook, router spike — ✅ complete: `6be`+`gu4` (prior) + `xlu` (0005-T1) + `br1` (0006-T0 spike) built S38
- **Wave 4** — adapters, matrix render, cron entry, clone-init, router impl — ✅ complete: `n9h`+`3gp` (prior) + `yo6` (0004-T2 matrix render) + `ml1` (0005-T2 clone-init) + `ftm` (0006-T1 no-train router) built S39 (PR #66)
- **Wave 5** — scheduler + plan assembly — ✅ complete: `oaf` (0003-T3 scheduler) + `8cv` (0006-T2 multi-domain plan assembly — reasons over the `ftm` router summary; fail-closed class-aware HALT) built S40 (PR #69). Tier-3 caught + fixed a Critical HALT compound-limit fail-open; residuals `8j6` P1 / `10h` / `7lt` / `e3b` / `20d` beaded (LM-04-gated)
- **Wave 6** — lab-loop store schemas — ⏭ NEXT WAVE — open: `1aa` (0007-T1)
- **Wave 7** — biomarker matrix/projection views — open: `1ih`

Execute-stage protocol: `/execute-plan` in wave mode, adopted S36 after **PF-S36-01** (the build had been hand-rolled per-task off the wave schedule from S32 — outputs verified undamaged, but the wave-checkpoint discipline lapsed). Re-entry completes the open waves in order; Phase B (S37) cleared `5wo`/`qwj` (the W3/W4 design blockers — `5wo`→caller-orchestrated pagination preserving `emit -> Path`, `qwj`/`ko5`→ADR-0005 "PII-free = health-data-free" clarification); Phase C built W3 (`br1`+`xlu`) at S38, W4 (`yo6`+`ml1`+`ftm`) at S39, and W5 (`oaf`+`8cv`) at S40 via `/execute-plan` wave runs (three-tier review + checkpoint gate each), and resumes at W6 (`1aa`). The no-train router PII boundary (`ftm`) AND the multi-domain plan assembly (`8cv`, the V1 PII-trust + fail-closed class-aware HALT task) are now BUILT before any further plan-reasoning task; the in-summary pass-through PII value-gate (`8j6` P1) is the tracked LM-04-gated residual. No actual artifact generates until `generate.run` is fed real operator data (LM-04 pending). Prior session titles (S32-S35) use the old ADR-family wave labels and are NOT retro-corrected — cross-reference the build-plan wave numbers here, not the archived session titles. The S2/S1 snapshots below are historical.

## Status as of 2026-05-23 (S2 close)
- Wiki schema layered onto operational vault (`vault/WIKI.md`)
- Agent-shared context layer in place: operator-profile, current-state, goals, contradictions, index, log
- Source whitelist + entity templates (compounds, biomarkers) authored
- `aplus-research` project-local skill built with 6 mechanically enforced gates; never invoked end-to-end yet
- First compound library entry (BPC-157) exists at `vault/library/peptides/bpc-157/` + `vault/compounds/bpc-157.md` — **suspect**, scheduled for re-run via `aplus-research` next session (the original deep-research dispatch did not follow protocol; entry may contain hallucinations/fabrications)
- All `protocols/` files still placeholders awaiting Walter's input (unchanged from S1)
- 23andMe analysis pending raw file (unchanged from S1)
- Oura purchase pending (unchanged from S1)
- No bloodwork yet (none ordered until July 2026 visit)

## Status as of 2026-05-16 (S1 close)
See `vault/sessions/session-1.md` for the initial vault-skeleton + project-identity work.