---
title: Fasting Insulin
type: biomarker
permalink: a-plus-maxing/biomarkers/fasting-insulin
category: blood
unit: µIU/mL
source: lab
confidence: supported
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.fasting-insulin-design-work
provenance_slug: labs-specialist
---

# Fasting Insulin

## Metadata
- category: blood
- unit: µIU/mL (×6.0 → pmol/L; e.g., 5 µIU/mL = 30 pmol/L); WHO conversion: 1 µIU/mL = 6.00 pmol/L
- source: lab
- confidence: supported
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- **No universally validated diagnostic cutpoint.** Fasting insulin values are assay-dependent; between-assay CV is 12–66% (median 24%) across commercial platforms. Absolute cutpoints do not transfer across labs.
- commonly-cited reference interval (ECLIA assay, n = 21,684 metabolically screened adults): 2.52–13.14 µIU/mL (15–79 pmol/L)
- the "insulin-sensitive" framing (lower value = greater sensitivity at normal glucose) is qualitative — no numeric cutpoint has been validated by any regulatory body
- HOMA-IR: (fasting insulin µIU/mL × fasting glucose mg/dL) / 405; ≈ 1.0 in healthy lean adults; > 1.9 early IR; > 2.9 significant IR (framework-specific, assay-dependent)
- HOMA-IR equivalently: (fasting insulin µIU/mL × fasting glucose mmol/L) / 22.5
- source of target: [[library/biomarkers/fasting-insulin/research-report]]

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- raised by:
  - insulin resistance / visceral obesity (dominant driver; elevated free fatty acids initiate β-cell compensatory hypersecretion)
  - refined-carbohydrate / high-glycaemic-load diet (repeated postprandial excursions shift fasting baseline upward)
  - physical inactivity (reduced GLUT4 expression and skeletal muscle insulin receptor signaling increases secretory demand)
  - sleep restriction (RCT: ≤ 6.2 h/night for 6 weeks → HOMA-IR β = 0.30 ± 0.12, P = 0.016, independent of adiposity)
  - PCOS (IR present in 35–80%; hyperinsulinemia amplifies ovarian androgen synthesis — self-reinforcing loop)
  - glucocorticoids, atypical antipsychotics, high-dose thiazide diuretics
  - exogenous insulin / sulfonylureas / meglitinides (directly inflate measured value; use c-peptide instead)
- lowered by:
  - weight loss (5–10% body weight reduction reduces fasting insulin proportional to visceral fat lost)
  - aerobic + resistance exercise (combined training reduces fasting insulin and HOMA-IR in sedentary adults)
  - carbohydrate restriction (proportional to extent of restriction)
  - [[compounds/metformin]] (improves hepatic insulin sensitivity; modest effect on fasting insulin per se)
  - bariatric surgery (meta-analysis of 39 studies, n = 3,855: WMD −0.62, 95% CI −0.88 to −0.36; weight-independent early effects via gut hormones + hepatic insulin clearance)
- analytical confounders: heparin plasma yields ~15% lower values than serum; hemolysis renders sample unreportable (IDE degrades insulin); assay non-standardization limits cross-lab comparison

## Why It Matters
Fasting insulin is the earliest detectable signal of insulin resistance, rising years to decades before fasting glucose leaves the normal range. It can be the only abnormal value in an otherwise normal metabolic panel: in a cross-sectional study of 1,313 young Indian adults, 30.5% displayed hyperinsulinemia despite normal glucose and HbA1c. Prognostically, elevated fasting insulin predicts incident type 2 diabetes (METSIM Study HR 1.37 per unit increase), metabolic syndrome (Korean cohort OR 5.1–10.7 for highest vs. lowest quartile), and cardiovascular events via HOMA-IR (meta-analysis, 65 studies, N = 516,325: CHD RR 1.64 for highest vs. lowest HOMA-IR). Interpretation requires clinical context because a normal fasting insulin is bidirectional: it can reflect either genuine insulin sensitivity or late β-cell exhaustion in which compensatory capacity is lost — a distinction that matters most when glucose is already elevated.

## Relations
- [[biomarkers/fasting-glucose]]
- [[biomarkers/hba1c]]
- [[biomarkers/homa-ir]]
- [[library/biomarkers/fasting-insulin/research-report]]
