---
title: Fasting Plasma Glucose
type: biomarker
permalink: a-plus-maxing/biomarkers/fasting-glucose
category: blood
unit: mg/dL
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.fasting-glucose-design-work
provenance_slug: labs-specialist
---

# Fasting Plasma Glucose

## Metadata
- category: blood
- unit: mg/dL (divide by 18.0 for mmol/L)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- normal (ADA 2025): < 100 mg/dL (< 5.6 mmol/L)
- prediabetes / IFG (ADA): 100–125 mg/dL (5.6–6.9 mmol/L)
- prediabetes / IFG (WHO/IDF): 110–125 mg/dL (6.1–6.9 mmol/L)
- diabetes threshold: ≥ 126 mg/dL (≥ 7.0 mmol/L) — confirmed on two separate occasions
- evidence-based optimal: ~80–90 mg/dL (4.4–5.0 mmol/L) — lowest-mortality range in n=12.4M Korean cohort; not a regulatory threshold
- hypoglycemia alert (Level 1): < 70 mg/dL (< 3.9 mmol/L)
- hypoglycemia clinically significant (Level 2): < 54 mg/dL (< 3.0 mmol/L)
- source of target: [[library/biomarkers/fasting-glucose/research-report]] + ADA Standards of Care 2025 + WHO/IDF 2006

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- raised by: insulin resistance / hepatic insulin resistance (primary driver of fasting hyperglycemia in T2D), visceral obesity, physical inactivity, sleep deprivation, psychological stress / elevated cortisol
- raised by drugs: glucocorticoids (40–65% incidence), atypical antipsychotics (10–30%), thiazide diuretics (~10%), beta-blockers (~22%), statins (modest, ~7–20% new-onset diabetes), niacin
- lowered by: [[compounds/metformin]] (hepatic gluconeogenesis suppression; 31% diabetes risk reduction in DPP), [[compounds/glp1-agonists]] (FPG −1.6 mmol/L / −28.8 mg/dL mean in meta-analysis), [[compounds/sglt2-inhibitors]] (glucosuria, insulin-independent), exercise (aerobic + resistance), weight loss
- genetics: [[dna/gck]] — loss-of-function GCK variants (MODY2) produce stable mild hyperglycemia 100–153 mg/dL from birth, non-progressive; common GWAS loci MTNR1B, G6PC2, GCKR each add ~0.5–1.3 mg/dL per allele
- heritability: 38–68% (twin studies)
- dawn phenomenon: early-morning FPG rise driven by cortisol, GH, catecholamines; affects ~50% of T2D patients, ~30% with prediabetes

## Why It Matters
Fasting plasma glucose is the primary marker of hepatic glucose output in the basal state — when FPG is elevated, the liver is failing to suppress gluconeogenesis and glycogenolysis under prevailing insulin concentrations. It is the most widely used screening test for impaired fasting glucose and diabetes. Beyond the diagnostic binary, risk is continuous: all-cause and cardiovascular mortality both rise progressively above ~94 mg/dL (5.2 mmol/L) and are also slightly elevated below ~70 mg/dL (3.9 mmol/L), placing the metabolically optimal window around 80–90 mg/dL. A single FPG result carries ±24% biological and analytical noise, making serial measurements and paired testing (HbA1c, fasting insulin / HOMA-IR) essential for accurate characterisation. FPG captures hepatic fasting-state glucose; it does not capture postprandial excursions, which dominate glycemic burden when HbA1c is near-normal.

## Relations
- [[biomarkers/hba1c]]
- [[biomarkers/fasting-insulin]]
- [[biomarkers/triglycerides]]
- [[library/biomarkers/fasting-glucose/research-report]]
