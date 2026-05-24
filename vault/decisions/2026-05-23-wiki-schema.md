---
title: Wiki Schema — Karpathy-Style Entity Types + Agent Consumer Roster
type: decision
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
depends_on: ["2026-05-16-system-architecture"]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/decisions/2026-05-23-wiki-schema
---

# Decision: Wiki Schema

## Context

After session 1, the vault held operational memory (sessions, daily, weekly, reviews, interactions) and methodology (evidence tiers, n=1 trial design, artifact protocol). It did NOT have a queryable knowledge-base layer — the kind Karpathy describes ("LLM wiki") where the LLM can ingest a question, consult entity pages with templates and confidence levels, and answer with citation. The Quant project has this layer at `vault/WIKI.md` with templates for components, decisions, parameters. We needed the health equivalent.

The wiki is a different thing from the operational vault. Operational vault = "what happened, what we tried, what's next." Wiki = "what is true about this compound / biomarker / protocol, with admissible-source citations, queryable by any future agent."

## Decisions

### 1. Wiki schema lives at `vault/WIKI.md`

Top-level schema file defining: entity types, page templates, operations (ingest / query / lint / export), confidence levels, conventions. Pattern borrowed from Quant project's `vault/WIKI.md`.

### 2. Five entity types

- `compounds/` — peptides, supplements, hormones, nootropics, pharmaceuticals, herbals
- `biomarkers/` — blood / wearable / functional / subjective measurements
- `protocols/` — composite procedures (meal template, training split, sleep window)
- `parameters/` — cross-cutting configuration values (protein g/kg, fasting window)
- `decisions/` — ADRs

Each has a page template with required metadata, evidence summary, relations, and a self-check structure.

### 3. Distinct from operational folders

`sessions/`, `daily/`, `weekly/`, `reviews/`, `interactions/`, `design/`, `artifacts/`, `architecture/`, `methodology/`, `rubrics/` are NOT wiki pages. They are operational memory / outputs / methodology. They feed the wiki and consume it but do not follow entity templates.

### 4. Agent consumer roster

14 specialist agents documented in `WIKI.md` with read/owns/dispatch columns: personal-trainer, labs-specialist, nutritionist, supplement-specialist, peptide-specialist, endocrine-specialist, lymphatic-specialist, gi-specialist, cardiovascular-specialist, sleep-coach, recovery-specialist, longevity-strategist, mental-performance-coach, medical-liaison.

Agent profile files are NOT drafted speculatively. They are drafted on-demand when a specific agent is first invoked. The roster documents the design; the profiles get written when needed.

### 5. Library research is goal-agnostic; specialist dispatches are personalized

A wiki entry is built once, used by many future queries. Pre-filtering at library-build time for one specific patient context (e.g., "filter for Walter's January 2026 health issue") corrupts the entry for other future queries. This split is enforced in the `aplus-research` skill (see related ADR).

### 6. Three meta files form the agent-shared context layer

- `vault/meta/operator-profile.md` — slow-changing (demographics, training history, current Rx, allergies)
- `vault/meta/current-state.md` — fast-changing snapshot (current biomarkers, active protocols)
- `vault/meta/goals.md` — hard limits, doctor-handout queue, accepted tradeoffs

These load as context for any specialist dispatch but are NOT injected into library-build dispatches.

### 7. Output path convention

- Compound entries: `vault/compounds/<slug>.md` — flat folder, class is metadata
- Research artifacts: `vault/library/<class>s/<slug>/{research-report, practitioner-layer, non-english-layer}.md` — class-organized because research clusters by domain (peptide compounders are peptide-specific, etc.)

Compounds flat = trivial to list / cross-reference. Library class-organized = domain extensions (whitelists, triage lists) live alongside their entries.

## Alternatives Considered

- **No wiki layer, just operational vault.** Rejected: future agents need an entity-typed, queryable layer that operational memory can't provide. Sessions are episodic; entities are durable.
- **Wiki content lives in compound pages only, no separate library/.** Rejected: research artifacts (full reports with 10k+ words, supplementary layers) are too large to keep in compound entries. Library/ for the research; compounds/ for the digested decision-grade page.
- **Single combined source of truth = compound page only, research in frontmatter.** Rejected: research output isn't structured enough for frontmatter, and the practitioner-layer + non-English-layer pattern adds two more artifacts per compound that need their own files.

## Breaks If

- Walter chooses to abandon the wiki/operational split — then the entity-template discipline is wasted
- Specialist agents are never built — then the roster is documentation without consumers (still useful as scaffolding for future)
- Goal-agnostic library principle gets violated (PF-S2-04) — entries get corrupted for queries they should have served

## Relations

- [[decisions/2026-05-16-system-architecture]] (parent — markdown + HTML hybrid)
- [[decisions/2026-05-23-source-whitelist]] (companion — admissibility rules used by wiki research)
- [[decisions/2026-05-23-aplus-research-skill]] (companion — research pipeline that produces wiki entries)
- [[WIKI.md]] (the schema itself)
- [[library/methodology/evidence-tiers]] (tier methodology applied)
