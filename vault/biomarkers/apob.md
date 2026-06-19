---
title: ApoB — Apolipoprotein B
type: biomarker
permalink: a-plus-maxing/biomarkers/apob
category: blood
unit: mg/dL
source: lab
confidence: established
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.apob-design-work
provenance_slug: labs-specialist
---

# ApoB — Apolipoprotein B

## Metadata
- category: blood
- unit: mg/dL (g/L also reported; 1 g/L = 100 mg/dL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- very-high risk (ESC/EAS): < 65 mg/dL (≈ 0.65 g/L)
- high risk (ESC/EAS): < 80 mg/dL (≈ 0.80 g/L)
- moderate risk (ESC/EAS): < 100 mg/dL (≈ 1.00 g/L)
- optimal: < 80 mg/dL
- population context (NHANES 2005–2016 untreated US adults): median ~90 mg/dL, 90th percentile ~125 mg/dL, 95th percentile ~137 mg/dL — the untreated median sits at the upper edge of "acceptable," not "optimal"
- source of target: [[library/biomarkers/apob/research-report]] + ESC/EAS 2019 dyslipidaemia guideline (Mach et al., Eur Heart J 2020; DOI 10.1093/eurheartj/ehz455)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: [[labs/]] (awaiting first panel)

## Affected By
- genetics [[dna/apob]] — APOB / LDLR / PCSK9 variants; familial hypercholesterolemia (LDLR ~90%, APOB ~5–10%, PCSK9 ~1% of monogenic dominant FH)
- raised by: type 2 diabetes / insulin resistance, metabolic syndrome, hypothyroidism, high saturated- and trans-fat intake, excess adiposity, nephrotic syndrome
- lowered by: [[compounds/statins]] (~33%), ezetimibe (~13–15% add-on), [[compounds/pcsk9-inhibitors]] (~46–58%), inclisiran (~34%)
- minimal / indirect effect: aerobic exercise (mediated through weight and triglyceride change)

## Why It Matters
ApoB is the total atherogenic particle number — exactly one apoB-100 molecule sits on each VLDL, IDL, LDL, and Lp(a) particle, so the measured concentration counts the circulating atherogenic particles rather than the cholesterol mass they carry. Across Mendelian randomization and large cohorts it provides the best (or equal-best) cardiovascular risk discrimination versus LDL-C and non-HDL-C, and it remains the single causal lipid exposure once particle number is in the model. Its decisive clinical use is capturing residual risk when LDL-C is "at goal": at an identical LDL-C of ~130 mg/dL, individuals with high apoB carry nearly double the 10-year ASCVD risk of those with low apoB, because the cholesterol-poor small-dense-LDL phenotype hides a high particle count that only apoB reveals.

## Relations
- [[biomarkers/ldl-c]]
- [[biomarkers/lp-a]]
- [[library/biomarkers/apob/research-report]]
