---
title: Evidence Tiers
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/library/methodology/evidence-tiers
---

# Evidence Tiers

Used in every `library/<topic>/<thing>.md` entry as the `evidence_tier:` frontmatter field.

| Tier | Criteria | Examples |
|---|---|---|
| **S** | Multiple high-quality human RCTs OR a meta-analysis of RCTs OR strong mechanism + consistent RCT evidence | Statins → LDL, creatine monohydrate → strength, GLP-1s → weight loss |
| **A** | A single well-designed human RCT OR strong prospective cohort data OR multiple smaller human studies in agreement | Omega-3 EPA/DHA → triglycerides, magnesium → sleep latency |
| **B** | Mixed human evidence, mostly observational, or small/early RCTs with inconsistent results | NMN → biomarkers, methylene blue → cognition |
| **C** | Animal or preclinical evidence only, OR weak/contradictory human data, OR very limited n | BPC-157 → tendon healing (mostly rodent), most peptide claims |
| **D** | Anecdotal reports, n=few, speculative mechanism, or no replicable evidence | "Reddit consensus," practitioner anecdote, single uncontrolled case reports |

## Risk Tiers

Used alongside evidence tier. They are independent — a tier-S intervention can still be high-risk (statins are S-evidence but have known side effects).

| Tier | Criteria |
|---|---|
| **low** | Well-tolerated, common adverse effects mild and reversible, no known major interactions, common at OTC doses |
| **medium** | Known meaningful side-effect profile, monitoring recommended (e.g., liver enzymes, lipids), some interaction potential |
| **high** | Significant adverse effect risk, requires monitoring, multiple known interactions, dose-sensitive |
| **experimental** | Risk profile not well characterized, quality-control concerns on supply side, off-label or research-chemical status |

## Decision matrix (rough guidance)

| Evidence \ Risk | low | medium | high | experimental |
|---|---|---|---|---|
| **S** | adopt freely | adopt with monitoring | adopt with doctor | avoid unless strong indication |
| **A** | consider | trial carefully | doctor required | avoid |
| **B** | trial | trial with caution | doctor required | avoid |
| **C** | trial cautiously | doctor required | avoid | avoid |
| **D** | informational only | informational only | avoid | avoid |

This is rough guidance, not a hard rule. Specific risk/benefit varies per Walter's context (DNA, labs, current protocol). The doctor-visit handout surfaces anything `B+` evidence with `medium+` risk for review.