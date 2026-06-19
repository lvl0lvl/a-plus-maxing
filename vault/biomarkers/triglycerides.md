---
title: Triglycerides
type: biomarker
permalink: a-plus-maxing/biomarkers/triglycerides
category: blood
unit: mg/dL
source: lab
confidence: established
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.triglycerides-design-work
provenance_slug: labs-specialist
---

# Triglycerides

## Metadata
- category: blood
- unit: mg/dL (mmol/L = mg/dL ÷ 88.5)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- FASTING — normal: < 150 mg/dL (< 1.7 mmol/L)
- FASTING — borderline-high: 150–199 mg/dL
- FASTING — high: 200–499 mg/dL
- FASTING — very high: ≥ 500 mg/dL (pancreatitis risk rises markedly above ~1000–2000 mg/dL)
- NON-fasting — abnormal: ≥ 175 mg/dL (≥ 2 mmol/L, EAS/EFLM)
- unit note: divide mg/dL by 88.5 for mmol/L (e.g., 150 ≈ 1.7, 500 ≈ 5.6)
- source of target: [[library/biomarkers/triglycerides/research-report]] + NCEP ATP III (fasting bands) / AHA 2011 scientific statement (optimal < 100; non-fasting ≥ 200 → fasting panel)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: [[labs/]] (awaiting first panel)

## Affected By
- diet (major): refined carbohydrate, sugar/fructose, and alcohol — raise hepatic VLDL secretion and apoC-III
- adiposity / insulin resistance / uncontrolled type 2 diabetes — major secondary drivers (↑ VLDL production, impaired LpL clearance); hypothyroidism also raises TG
- genetics [[dna/triglycerides]] — LPL, APOC2, APOA5, GPIHBP1, LMF1 (familial chylomicronemia syndrome, biallelic) vs polygenic/multifactorial chylomicronemia (~1 in 600); APOC3 loss-of-function lowers TG
- raised by: oral estrogen, corticosteroids, retinoids, beta-blockers, thiazides, protease inhibitors, atypical antipsychotics
- lowered by: fibrates (~30–50%), omega-3 fatty acids / [[compounds/icosapent-ethyl]] (REDUCE-IT, 4 g/day), statins (modest, ~10–30%)

## Why It Matters
Triglycerides mark the burden of triglyceride-rich lipoproteins and their cholesterol-enriched remnants: the TG molecule itself is not directly atherogenic, but remnant cholesterol — the cholesterol carried within these particles — is the atherogenic mediator that deposits in the arterial wall and drives residual cardiovascular risk after LDL-C is controlled. So a TG value is best read as a readily measured surrogate for remnant-cholesterol burden, with causality carried by genetic (Mendelian-randomization) evidence on the TRL/remnant pathway rather than by the TG number itself. Separately and mechanistically distinct, very-high TG (≥500, and especially above ~1000–2000 mg/dL) saturates lipoprotein-lipase clearance, causes chylomicrons to accumulate, and confers acute pancreatitis risk — a chylomicron-mass problem that is a different clinical domain from atherosclerotic risk.

## Relations
- [[biomarkers/ldl-c]]
- [[biomarkers/apob]]
- [[biomarkers/hdl-c]]
- [[library/biomarkers/triglycerides/research-report]]
