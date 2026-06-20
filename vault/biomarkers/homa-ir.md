---
title: HOMA-IR (Homeostatic Model Assessment of Insulin Resistance)
type: biomarker
permalink: a-plus-maxing/biomarkers/homa-ir
category: functional
unit: index (dimensionless)
source: calculation
confidence: supported
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.homa-ir-design-work
provenance_slug: labs-specialist
---

# HOMA-IR (Homeostatic Model Assessment of Insulin Resistance)

## Metadata
- category: functional
- unit: index (dimensionless)
- source: calculation (derived from fasting glucose + fasting insulin)
- confidence: supported
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- **No universally validated cutpoint.** HOMA-IR is population-, ethnicity-, and assay-dependent; between-assay CV is 12–66% (median 24%) across commercial insulin platforms. Absolute cutpoints do not transfer across labs.
- formula: **HOMA-IR = (fasting insulin [µIU/mL] × fasting glucose [mg/dL]) / 405**
- equivalently (SI): **(fasting insulin [µIU/mL] × fasting glucose [mmol/L]) / 22.5** (22.5 × 18.0 = 405)
- reference in healthy lean adults: ≈ 1.0 (Brazilian n = 21,684 reference interval: 0.39–2.86, 95th percentile)
- named cohort IR thresholds (local + assay-specific; not transportable):
  - 1.4 (Hong Kong Chinese, CRISPS 15-yr prospective, dysglycemia threshold)
  - 1.85–2.07 men / 2.05–2.53 women (Spanish EPIRCE, metabolic syndrome criterion)
  - 2.23–2.48 (Korean NHANES, sex- and menopause-stratified)
- HOMA2 (Oxford DTU nonlinear computer model) preferred for absolute individual comparisons; HOMA1 algebraic formula adequate for ranked epidemiological use
- source of target: [[library/biomarkers/homa-ir/research-report]]

## Current Value
- value: pending (computed from first fasting glucose + insulin)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- raised by:
  - insulin resistance / visceral obesity (dominant driver; elevated free fatty acids and inflammatory cytokines impair hepatic insulin signaling)
  - refined-carbohydrate / high-glycaemic-load diet (chronic postprandial hyperinsulinemia shifts fasting baseline upward)
  - physical inactivity (reduced GLUT4 translocation capacity and mitochondrial density increase secretory demand)
  - sleep restriction (meta-analysis of RCTs: reduced sleep duration increases HOMA-IR primarily through elevated endogenous glucose production and cortisol)
  - PCOS (hyperinsulinemia present in 35–80% of PCOS, independent of BMI)
- lowered by:
  - weight loss (5–10% body weight reduction produces meaningful fall in fasting insulin and HOMA-IR)
  - aerobic + resistance exercise (meta-analysis 30 RCTs, SMD −0.34, 95% CI −0.49 to −0.18)
  - carbohydrate restriction (proportional to extent; pronounced in obesity per secondary analysis, Parry-Strong 2022)
  - [[compounds/metformin]] (AMPK-dependent inhibition of hepatic gluconeogenesis → lower fasting glucose → lower fasting insulin)
  - bariatric surgery (Roux-en-Y: HOMA-IR −3.7 units vs. dietary control at 12–36 months; partial weight-independent gut-peptide effect)
  - GLP-1 receptor agonists (network meta-analysis 25 studies: MD −1.57, 95% CI −2.52 to −0.50)
- invalid where fasting insulin is uninformative:
  - exogenous insulin use (circulating insulin reflects injection, not endogenous secretion)
  - insulin secretagogues (sulfonylureas, meglitinides) inflate fasting insulin pharmacologically
  - advanced beta-cell failure (HOMA-IR may normalize as insulin secretion falls, masking worsening control)
- analytical confounders: heparinized plasma yields ~15% lower insulin than serum; assay non-standardization limits cross-lab comparison

## Why It Matters
HOMA-IR is the most widely used fasting surrogate for hepatic insulin resistance, exploiting the steady-state relationship between fasting glucose and fasting insulin to model the degree to which the liver fails to suppress glucose output in response to ambient insulin. It predicts incident type 2 diabetes (OR 2.8, highest vs. lowest quintile, Hoorn Study 6.4-yr follow-up), cardiovascular events (CHD RR 1.64, highest vs. lowest stratum, meta-analysis 516,325 participants), and MASLD/NAFLD (weighted mean difference in HOMA-IR 1.28 between cases and controls). Because it is computed from routine fasting bloods, requires no infusion or timed samples, and responds to lifestyle and pharmacological interventions, it is the preferred research-grade tool for tracking hepatic insulin sensitivity longitudinally within a single lab on a consistent assay. It does not capture peripheral (skeletal-muscle) insulin resistance and carries no regulatory-body-endorsed diagnostic cutpoint.

## Relations
- [[biomarkers/fasting-glucose]]
- [[biomarkers/fasting-insulin]]
- [[library/biomarkers/homa-ir/research-report]]
