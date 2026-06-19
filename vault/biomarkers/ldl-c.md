---
title: LDL-C — LDL Cholesterol
type: biomarker
permalink: a-plus-maxing/biomarkers/ldl-c
category: blood
unit: mg/dL
source: lab
confidence: established
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.ldl-c-design-work
provenance_slug: labs-specialist
---

# LDL-C — LDL Cholesterol

## Metadata
- category: blood
- unit: mg/dL (mmol/L = mg/dL ÷ 38.67)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- very-high risk (ESC/EAS 2019): < 55 mg/dL (< 1.4 mmol/L) and ≥50% reduction from baseline
- high risk (ESC/EAS 2019): < 70 mg/dL (< 1.8 mmol/L) and ≥50% reduction
- moderate risk (ESC/EAS 2019): < 100 mg/dL (< 2.6 mmol/L)
- recurrent event within 2 years (ESC/EAS 2019): < 40 mg/dL (< 1.0 mmol/L) may be considered
- NCEP ATP III descriptive bands (mg/dL): < 100 optimal / 100–129 near-optimal / 130–159 borderline high / 160–189 high / ≥ 190 very high
- source of target: [[library/biomarkers/ldl-c/research-report]] + 2019 ESC/EAS dyslipidaemia guideline (Mach et al., Eur Heart J 2020) and NCEP ATP III (NHLBI/NIH)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: [[labs/]] (awaiting first panel)

## Affected By
- genetics [[dna/ldlr]] — LDLR / APOB / PCSK9 variants; familial hypercholesterolemia (LDLR ≥85%, APOB, PCSK9 gain-of-function); HeFH untreated LDL-C >190 mg/dL (~1 in 250), HoFH >450 mg/dL (~1 in 300,000)
- raised by: high saturated- and trans-fat intake, dietary cholesterol, hypothyroidism, nephrotic syndrome, cholestasis, pregnancy, certain drugs (cyclosporine, thiazides)
- lowered by: [[compounds/statins]] (~30–55%), ezetimibe (~15–20% add-on), [[compounds/pcsk9-inhibitors]] (~50–60%), bempedoic acid (~15–25%), inclisiran (~50%), soluble fiber (~1.1 mg/dL per g/day)

## Why It Matters
LDL-C is the primary causal driver of atherosclerotic cardiovascular disease — randomized statin trials, Mendelian randomization, and epidemiology converge to show LDL is a cause, not merely a marker (each 1 mmol/L lowering cuts major vascular events ~22% over ~5 years, and lifelong genetic lowering cuts CHD ~54.5% per mmol/L). Risk is driven by cumulative lifetime LDL burden ("cholesterol-years"), so both the magnitude and the duration of exposure matter, and the goal falls as cardiovascular risk rises. It is the central modifiable lipid target of every major prevention guideline; in discordance with ApoB it can under- or over-state the particle-number-driven risk, but it remains the primary target against which lipid-lowering therapy is titrated.

## Relations
- [[biomarkers/apob]]
- [[biomarkers/hdl-c]]
- [[biomarkers/triglycerides]]
- [[library/biomarkers/ldl-c/research-report]]
