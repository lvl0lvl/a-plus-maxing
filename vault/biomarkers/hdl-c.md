---
title: HDL-C — HDL Cholesterol
type: biomarker
permalink: a-plus-maxing/biomarkers/hdl-c
category: blood
unit: mg/dL
source: lab
confidence: established
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.hdl-c-design-work
provenance_slug: labs-specialist
---

# HDL-C — HDL Cholesterol

## Metadata
- category: blood
- unit: mg/dL (mmol/L = mg/dL ÷ 38.67)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- "low" (cardiovascular risk factor): < 40 mg/dL in men / < 50 mg/dL in women (NCEP ATP III; metabolic-syndrome criterion)
- historically "≥ 60 mg/dL protective" — DE-EMPHASIZED: the HDL-C–mortality relationship is U-shaped, not monotonic, so a high number is not extra protection
- alert (very high): ≳ 80–90 mg/dL, especially in men — associated with INCREASED all-cause mortality (Copenhagen cohorts: men ≥ 3.0 mmol/L ≈ 116 mg/dL HR 2.06, 95% CI 1.44–2.95; women ≥ 3.5 mmol/L ≈ 135 mg/dL HR 1.68, 95% CI 1.09–2.58). NOT a target to maximize.
- "normal" band sits roughly 40–60 mg/dL; all-cause-mortality nadir ≈ 73 mg/dL (men) / 93 mg/dL (women)
- source of target: [[library/biomarkers/hdl-c/research-report]] + NCEP ATP III (NHLBI/NIH) and 2018 AHA/ACC/Multisociety cholesterol guideline

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- genetics [[dna/cetp]] — CETP / LIPC / SCARB1 / LIPG drive high HDL-C; ABCA1 (Tangier disease) / APOA1 / LCAT drive low HDL-C; ~18.7% of low-HDL and ~10.9% of high-HDL extremes carry a rare large-effect variant
- raised by: aerobic exercise (~2.53 mg/dL mean; ~1.4 mg/dL per extra 10 min/session), moderate alcohol (~3.6 mg/dL), weight loss, estrogen, smoking cessation (~3.9 mg/dL)
- lowered by: smoking, obesity, insulin resistance / type 2 diabetes, very-low-fat/high-carbohydrate diets, anabolic-androgenic steroids (~60–80%, case reports > 90%)

## Why It Matters
HDL-C is a strong, reproducible INVERSE risk MARKER and a legitimate risk-calculator input (it sits in the Pooled Cohort Equations; a 1-SD higher HDL-C carries an MI OR of 0.62, 95% CI 0.58–0.66), and a low value flags the metabolic-syndrome phenotype — but it is NOT a validated causal or treatment target. Mendelian randomization is null (a 14-SNP HDL genetic score gave an MI OR per 1-SD of 0.93, 95% CI 0.68–1.26, p=0.63), every major HDL-C-raising drug trial failed (torcetrapib caused net harm; evacetrapib and niacin were futile), and the HDL-C–mortality curve is U-shaped, so very high HDL-C tracks higher mortality. The protective biology lives in HDL *function* (cholesterol efflux capacity, particle quality), not in the cholesterol mass on the panel. Do NOT raise HDL-C in order to lower risk.

## Relations
- [[biomarkers/ldl-c]]
- [[biomarkers/apob]]
- [[biomarkers/triglycerides]]
- [[library/biomarkers/hdl-c/research-report]]
