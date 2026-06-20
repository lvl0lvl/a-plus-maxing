---
title: WIKI
type: reference
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-06-14
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/wiki
---

# a-plus-maxing Wiki Schema

The schema layer: defines entity types, page templates, operations, and conventions for the LLM wiki.
The LLM reads this before writing any wiki page. Schema and LLM co-evolve.

This wiki is the structured knowledge graph the agent queries to make recommendations.
The vault's other folders (`sessions/`, `daily/`, `weekly/`, `reviews/`, `interactions/`, `artifacts/`) are operational memory and outputs — they feed and consume the wiki, but are not wiki pages.

---

## Entity Types

### compounds/
Researched substances Walter takes, plans to take, or has rejected: supplements, peptides, nootropics, pharmaceuticals, hormones, herbal extracts.

**Page template:**
```
## Metadata
- class: supplement | peptide | nootropic | pharmaceutical | hormone | herbal
- evidence_tier: S | A | B | C | D (see library/methodology/evidence-tiers.md)
- risk_tier: low | medium | high | experimental
- status: researching | planned | active | paused | trialed-stopped | excluded
- last_verified: YYYY-MM-DD

## Mechanism
One paragraph: pathway, receptors, expected effect.

## Evidence Summary
Strongest 2-3 sources:
- [Author YYYY] — n, design (RCT/cohort/animal/in-vitro), effect size, citation file in library/

## Protocol
- dose: amount, route (oral | sublingual | subQ | IM | transdermal | intranasal), timing
- cycle: duration on, washout
- stack: co-administered compounds
- source: vendor or pharmacy, regulated status (Rx | OTC | research-chemical | gray-market)
- cost: $/month

## Risk Profile
- adverse effects observed in literature
- contraindications: DNA variants, current biomarkers, other compounds
- monitoring: biomarkers to track, cadence

## Trial Status
- linked experiment: [[experiment-id]] (or "none")
- baseline biomarkers: [[biomarker]]
- stopping criteria: what would end the trial

## Relations
- [[biomarker]] (target)
- [[experiment]]
- [[compound]] (stack partner)
- [[protocol]] (if part of routine)
```

### biomarkers/
Measurable values: blood panels, wearable metrics, functional tests, subjective ratings.

**Page template:**
```
## Metadata
- category: blood | wearable | functional | subjective
- unit: e.g., mg/dL, ms, bpm, %
- source: lab | wearable | manual | calculation
- confidence: established | supported | provisional
- last_verified: YYYY-MM-DD
- review_cadence: monthly | quarterly | per-lab-panel | per-wearable-sync

## Target Range
- ideal: x-y
- acceptable: a-b
- alert: < p or > q
- source of target: literature citation, MD recommendation, or n=1 baseline

## Current Value
- value: x (YYYY-MM-DD)
- trend: improving | stable | declining (over last N measurements)
- history: pointer to labs/ or daily/ files

## Affected By
- [[protocol]]
- [[compound]]
- [[dna-variant]]

## Relations
- [[experiment]] (uses this as endpoint)
- [[decision]]
```

### protocols/
Composite procedures — what Walter actually does on a given day or week (meal template, training split, sleep window, fasting protocol, recovery routine). Folder already exists.

**Page template:**
```
## Metadata
- domain: nutrition | training | sleep | recovery | mental | environmental
- status: active | draft | paused | archived
- confidence: established | supported | provisional
- last_verified: YYYY-MM-DD

## Purpose
One sentence: what this protocol does.

## Procedure
The actual steps. Times, doses, sequences. Not theory.

## Parameters
- [[parameter]] values used by this protocol

## Evidence Base
- [[library citation]]
- [[experiment]] (if n=1 supported)

## Adherence
- target: 7/7 days, 5/7 days, etc.
- current: as of YYYY-MM-DD

## Relations
- [[compound]] (taken as part of protocol)
- [[biomarker]] (intended to move)
```

### parameters/
Cross-cutting configuration values: sleep target hours, fasting window, weekly Z2 minutes, protein g/kg, deload frequency, fiber grams.

**Page template:**
```
## Metadata
- value: current value
- unit: hours | g/kg | minutes | % | grams
- source: literature | n=1 | placeholder | MD recommendation
- confidence: established | provisional
- last_verified: YYYY-MM-DD

## Definition
What this parameter controls. One sentence.

## Derivation
How chosen. Citation or "placeholder."

## Sensitivity
What happens at 2x and 0.5x. Risks at extremes.

## Consumers
Protocols/experiments that use this value.

## Relations
- [[protocol]]
- [[experiment]]
```

### decisions/
ADRs, strategy choices, rejected alternatives. Folder already exists.

**Page template:**
```
## Metadata
- status: active | superseded | draft
- confidence: established | supported
- date: YYYY-MM-DD
- superseded_by: (if applicable)

## Decision
What was decided.

## Context
Why this decision was needed.

## Alternatives Considered
What was rejected and why.

## Breaks If
Conditions that would invalidate this decision.

## Relations
- [[protocol]] or [[compound]] affected
- [[prior-decision]]
```

### experiments/ (existing)
n=1 trials per `library/methodology/n-of-1-trial-design.md`. Uses the existing `_template.md`.

### library/ (existing)
Research corpus — papers, methodology, evidence summaries. Citation source for wiki pages. Entries already carry `evidence_tier:` in frontmatter per `evidence-tiers.md`.

### dna/ (existing)
Genetic variant pages derived from 23andMe raw data.

### labs/ (existing)
Bloodwork panels by date.

### Non-wiki folders
`sessions/`, `daily/`, `weekly/`, `reviews/`, `interactions/`, `design/`, `artifacts/`, `architecture/`, `methodology/`, `rubrics/` — operational memory and outputs. Not entity pages; do not follow entity templates.

---

## Meta Files

| File | Purpose | Update frequency |
|------|---------|-----------------|
| meta/index.md | Catalog of every wiki page by entity type | Every page create/delete |
| meta/overview.md | Executive summary of system state (exists) | Every session close |
| meta/targets.md | Current health targets (exists) | On change |
| meta/contradictions.md | Active contradictions with resolution status | On discovery |
| meta/log.md | Append-only operation log | Every wiki operation |
| meta/context-packages/ | Exported briefings for focused sessions | On demand |

---

## Operations

### Ingest
When new knowledge arrives (compound researched, lab result in, protocol changed, decision made):
0. **Provenance (gated).** A `vault/{compounds,biomarkers,library}/` page declares its research provenance in frontmatter: `provenance_dir:` (the `/aplus-research` design-work dir that holds `gates/`) and `provenance_slug:` (the bda slug) — i.e. the `audit-research-provenance.sh <design-work-dir> <slug>` pair. The commit-time gate `scripts/wiki-ingest-lint.sh` (PreToolUse hook `block-ungated-vault-write.sh`, `INV-WIKI-INGESTION-GATED`) refuses the commit unless that provenance passes `bda` + `verify-chain`, every mandatory section is present, frontmatter enums are valid, and the page is registered in `meta/index.md`. Pre-gate pages are listed in `vault/library/_ingest-grandfather.txt` (provenance-exempt ONLY — every other check still applies; each is a back-fill obligation, not a permanent waiver).
1. Create or update the relevant entity page following the template
2. Update meta/index.md
3. Check for contradictions with existing pages
4. Update meta/overview.md if system state changed
5. Append to meta/log.md

### Query
When asking the agent about the system:
1. Read meta/index.md to find relevant pages
2. Read pages, following [[wikilinks]] for context
3. Cite wiki pages in the answer

### Lint
Two mechanical controls enforce this (S23, bead `bte` — previously manual discipline):

- **Commit-time (blocking)** — `scripts/wiki-ingest-lint.sh`, run by PreToolUse hook `block-ungated-vault-write.sh` on every staged `vault/{compounds,biomarkers,library}/` page. Deterministic per-page battery: provenance (bda + verify-chain), structural conformance (compounds/biomarkers strict per the templates above; library lighter — heterogeneous), frontmatter/enum validity, index sync. Link integrity is **advisory** here (forward-references to not-yet-authored pages are legitimate mid-buildout). A failing page cannot be committed (`INV-WIKI-INGESTION-GATED`).
- **Periodic (whole-vault)** — `scripts/wiki-lint.sh`, run every 5 sessions / at phase boundaries. The 6 graph-level checks below. **Violations (exit 1):** dead-namespace links (typo'd folder) + unresolved (`Status: open`) contradictions. **Advisory (info):** orphan, stale, coverage, provisional, forward-ref links.

1. Orphan check — pages with no inbound links
2. Stale check — last_verified older than review_cadence
3. Contradiction check — unresolved items in contradictions.md
4. Coverage check — active protocols/compounds with no biomarker tracking
5. Link integrity — [[wikilinks]] that don't resolve
6. Confidence audit — pages still marked "provisional"

### Export (Context Package)
For focused sessions or pre-compaction:
1. Identify topic pages from index (e.g., "everything related to sleep")
2. Assemble a single markdown briefing (~2000 words)
3. Save to meta/context-packages/{topic}-context.md

---

## Confidence Levels

Confidence applies to the claim on the page (target range, dose, mechanism). Evidence tier (S-D) and risk tier (low/medium/high/experimental) live in metadata per `library/methodology/evidence-tiers.md`.

| Level | Meaning | Verification |
|-------|---------|-------------|
| **Established** | n=1 trial completed with measured outcome, OR multiple RCTs in line | Cited experiment or S/A-tier evidence |
| **Supported** | Strong literature evidence per evidence-tiers.md, no n=1 yet | A/B-tier evidence + last_verified date |
| **Provisional** | Mechanistic/animal evidence only, or single small study | C-tier evidence; flagged for trial |
| **Contested** | Sources disagree | In contradictions.md |
| **Placeholder** | Target/dose set without strong basis (best guess) | Flagged in page |

---

## Agent Consumers

The wiki is queryable knowledge — agnostic to who reads or writes it. Specialist agents read what their domain needs, write back in entity form, and dispatch research when their domain has gaps. Multiple agents may write to the same entity type (e.g., both peptide-specialist and supplement-specialist write to `compounds/`); contradictions land in `meta/contradictions.md`.

| Agent | Domain | Reads | Owns (writes) | Dispatches research on |
|---|---|---|---|---|
| personal-trainer | training programming, periodization, return-to-training, MSK rehab | operator-profile, current-state, goals, biomarkers, protocols/exercise | protocols/exercise, parameters (training volumes/intensities) | training literature, MSK rehab |
| labs-specialist | bloodwork interpretation, biomarker context | operator-profile, current-state, goals, dna, compounds, labs/ | biomarkers, labs/, contradictions | clinical literature, lab reference ranges |
| nutritionist | macros, micronutrients, meal structure, fasting | operator-profile, current-state, goals, biomarkers, dna | protocols/meal-template, parameters (protein g/kg, fiber, fasting window) | nutrition literature |
| supplement-specialist | OTC supplements, herbals, nootropics | operator-profile, current-state, goals, compounds, biomarkers | compounds (supplement class), protocols/supplement-stack | supplement literature |
| peptide-specialist | peptides, GH secretagogues, healing peptides | operator-profile, current-state, goals, compounds, dna, biomarkers, library/peptides/_triage | compounds (peptide class), library/peptides/ | peptide literature, vendor sourcing |
| endocrine-specialist | testosterone, thyroid, cortisol, insulin, GH/IGF-1, estrogen, DHEA, full HPA/HPG/HPT axes | operator-profile, current-state, goals, biomarkers (hormones), dna, compounds (hormone-affecting) | biomarkers (hormone class), compounds (hormones/TRT), contradictions for axis interpretation | endocrinology literature |
| lymphatic-specialist | lymphatic drainage, interstitial fluid, immune trafficking, drainage modalities | operator-profile, current-state, biomarkers (immune/inflammation), protocols (recovery) | protocols (lymphatic), biomarkers (lymphatic/inflammation) | lymphatic + manual-therapy literature |
| gi-specialist | microbiome, digestion, food sensitivities, gut barrier, motility | operator-profile, current-state, goals, biomarkers (GI/inflammation), dna, compounds, protocols/meal-template | biomarkers (GI), protocols (gut), compounds (probiotics/prebiotics/digestive aids) | microbiome + GI literature |
| dermatologist | skin/hair/nail health, topical + systemic derm, derm-relevant compound effects (incl. peptide skin signals), photoaging | operator-profile, current-state, goals, biomarkers (inflammation/hormonal), compounds (derm-relevant), dna | biomarkers (skin/derm class), compounds (topical/derm class), contradictions | dermatology literature |
| cardiovascular-specialist | HR/HRV, BP, lipids, vascular health, Z2 work, plaque burden | operator-profile, current-state, goals, biomarkers (CV), wearable data | biomarkers (CV class), protocols (Z2, cardio), parameters (HR zones) | cardiovascular literature |
| sleep-coach | sleep architecture, circadian, recovery | operator-profile, current-state, wearable data, compounds (sleep-relevant) | protocols/sleep, parameters (sleep targets) | sleep literature |
| recovery-specialist | sauna, cold exposure, breathwork, manual therapy, fascia | operator-profile, current-state, goals, biomarkers (recovery/inflammation) | protocols (recovery modalities), parameters (sauna/cold dose) | recovery-modality literature |
| longevity-strategist | longevity-class interventions, biological-age tracking | operator-profile, current-state, goals, all biomarkers, all compounds | longevity-tagged biomarkers and compounds | longevity literature |
| mental-performance-coach | focus, mood, cognitive enhancers, stress | operator-profile, current-state, compounds (cognitive class) | cognitive protocols, parameters (mental) | cognitive literature |
| genetics-specialist | genetics & pharmacogenomics, SNP/variant interpretation, drug-gene interactions, nutrigenomics, disease-risk variants | operator-profile, current-state, goals, dna/raw, compounds, biomarkers | dna/ (analysis + variant pages), PGx annotations on compounds, contradictions | clinical genetics, pharmacogenomics (PharmGKB/CPIC), nutrigenomics |
| medical-liaison | MD-handout queue, contraindication tracking, Rx coordination | operator-profile (Jan 2026 issue), all compounds risk_tier medium+, prescriptions | artifacts/_doctor-visit-queue, contraindications entries | none — collates only |

**Cross-cutting protocol:**
- Every specialist reads `meta/operator-profile.md`, `meta/current-state.md`, `meta/goals.md` on invocation.
- Every specialist respects `goals.md` hard limits.
- Any specialist finding a contradiction with existing wiki content logs to `meta/contradictions.md`.
- Any specialist writing a compound with `risk_tier: medium+` triggers medical-liaison to queue it for the next doctor visit.
- Agent profiles live at `<project>/.claude/agents/<name>.md` once authored (not yet — draft on demand, not speculatively).

**Cross-cutting consultants (not yet own-agent):**
- Environmental factors (light, EMF, air, water, temperature exposure) — currently cross-cutting; promote to own-agent when a specific question forces it.
- Skin, dental, vision, hearing — not yet; add when an actual question forces them.

---

## Conventions

- All pages use [[wikilink]] syntax for cross-references
- All claims cite their source: research file in library/, lab result by date, ADR file, or experiment id
- Compound pages always include ACTUAL dose, route, source — not paraphrased
- Biomarker pages always include ACTUAL current value with date — not "see labs/"
- Parameter pages always include ACTUAL current value — not "see protocol"
- When in doubt about accuracy, mark as provisional and flag for lint
- Never write a page from memory — read the source (library citation, lab file, raw data) first
- Risk tier `experimental` (peptides, research chemicals, off-label) requires:
  - explicit Contraindications section populated
  - linked monitoring biomarker(s)
  - stopping criteria in Trial Status
- Pages cite the decision matrix in `library/methodology/evidence-tiers.md` when status moves from `researching` → `planned`
- Every `vault/{compounds,biomarkers,library}/` page declares its research provenance: `provenance_dir:` + `provenance_slug:` frontmatter pointing at the gated `/aplus-research` design-work dir (the bda `<design-work-dir> <slug>` pair). Enforced at commit by `INV-WIKI-INGESTION-GATED` (`scripts/wiki-ingest-lint.sh`); pre-gate exemptions live in `vault/library/_ingest-grandfather.txt`.
