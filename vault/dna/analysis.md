---
title: DNA Analysis (23andMe Raw Genotype)
type: reference
status: pending
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: manual
permalink: a-plus-maxing/dna/analysis-1
---

# DNA Analysis (23andMe Raw Genotype)

> **Status:** Pending. Walter has the raw 23andMe download from years ago. Drop the file into `vault/dna/raw/` and the agent will parse the actionable subset into this note.

## Source
- 23andMe genotype file (TSV, ~600K SNPs)
- Downloaded by Walter approximately 8 years ago
- Raw genotype data does not change over time; interpretation tooling has improved
- Filename when added: TBD

## Limitations (important)
- Genotyping array, **not** whole-genome sequencing
- No rare-variant coverage; only common SNPs on the array
- Some loci low-confidence; interpretation varies by tool
- This is informational, not clinical — flag anything action-worthy for discussion with the July 2026 doctor

## Actionable Variants (to be populated)

### Diet & Nutrition
- Lactose persistence (LCT/MCM6)
- Caffeine metabolism (CYP1A2 — fast vs slow metabolizer)
- Alcohol metabolism (ADH1B, ALDH2)
- Folate metabolism (MTHFR C677T, A1298C)
- Vitamin D receptor / metabolism (VDR, GC)
- Omega-3 conversion (FADS1/FADS2)
- Salt sensitivity (AGT, ACE)
- Bitter taste / vegetable preference (TAS2R38)

### Cardiovascular & Longevity
- APOE (E2/E3/E4 — cognitive + cardiovascular risk; LDL target modifier)
- 9p21 cluster (CAD risk)
- LPA-related variants (Lp(a) influence)

### Exercise & Body Composition
- ACTN3 (R577X — power vs endurance bias)
- ACE I/D (endurance vs power)
- FTO (rs9939609 — satiety / weight regulation)
- PPARGC1A (mitochondrial biogenesis response)

### Drug & Supplement Metabolism (flag for doctor)
- VKORC1, CYP2C9 (warfarin sensitivity — informational)
- CYP2D6 (many psychiatric/cardiac meds)
- SLCO1B1 (statin myopathy risk if statins ever prescribed)

### Other
- Gilbert syndrome (UGT1A1)
- Hemochromatosis (HFE C282Y, H63D)
- G6PD deficiency (if applicable to ancestry)

## Recommended Actions per Variant
_To be filled in. Each entry will include: variant, genotype, interpretation, confidence, recommended action, evidence quality._