---
title: Library — Entry Format Guide
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/library/readme
---

# Library

The research corpus for things Walter might use, is trialing, or has adopted. Sourced from peer-reviewed literature, high-quality reviews (Examine.com, Cochrane, NIH), and reputable practitioners. Anecdotal sources allowed only with explicit tier marking.

## Subdirectories
- `peptides/` — BPC-157, TB-500, GLP-1s, etc.
- `supplements/` — creatine, magnesium glycinate, NMN, etc.
- `interventions/` — sauna, cold exposure, fasting, HBOT, etc.
- `biomarkers/` — ApoB, Lp(a), GlycA, hs-CRP, etc. — what they mean, how to move them
- `methodology/` — how to design n=1 trials, evidence-tier definitions, search practices

## Entry shape (every `library/<topic>/<thing>.md` follows this)

```markdown
---
title: <Compound or intervention name>
type: reference
status: active | draft | archived
owner: walter
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
depends_on: []
superseded_by: null
review_cadence: quarterly | manual
evidence_tier: S | A | B | C | D
risk_tier: low | medium | high | experimental
walter_status: never-tried | considering | trialing | adopted | discontinued
doctor_discussion_required: true | false
---

# <Name>

## TL;DR
One sentence: what it is, what it claims to do, where the evidence stands.

## Mechanism
Brief — how it's proposed to work. Cite the strongest mechanistic source.

## Evidence Summary
Tiered:
- **S:** Multiple human RCTs, meta-analyses
- **A:** Single well-designed human RCT or strong cohort data
- **B:** Mixed human evidence, mostly observational
- **C:** Animal / preclinical only, or weak human data
- **D:** Anecdotal, n=few, or speculative

Pull the 3-5 strongest references. Note where evidence is contradictory.

## Dose & Administration
Range, common protocols, timing, route, form.

## Risk Profile
- Known adverse effects
- Contraindications
- Drug interactions (flag any that touch likely-current meds)
- Quality-control concerns on the supply side (esp. peptides)
- Regulatory status (FDA-approved? research chemical? Schedule?)

## N=1 Trial Design
- Expected outcome measures (what to look for)
- Expected time to see effect
- Recommended baseline duration
- Washout consideration
- Confounders to control

## Key References
- [Title, year, PMID/DOI]
- ...

## Walter's Status
- Status: `<one of the tier values above>`
- History: dates of trials, results, references to `experiments/` entries
- Current notes: anything relevant right now

## Last Literature Sweep
- YYYY-MM-DD — summary of what was searched, what's new
```

## When entries get added
- When Walter asks about a topic, or a decision is about to be made, the agent does a focused search and writes the entry
- Walter can also drop a PDF / paper link and ask the agent to file it
- Phase B (later): monthly scheduled job re-sweeps for `trialing | adopted` items

## Evidence honesty rule
Every claim cites a source. Anecdote is allowed if labeled. "Studies show..." without a citation is not allowed in this library.