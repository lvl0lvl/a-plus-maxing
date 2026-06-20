---
title: SHBG (Sex Hormone-Binding Globulin)
type: biomarker
permalink: a-plus-maxing/biomarkers/shbg
category: blood
unit: nmol/L
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.shbg-design-work
provenance_slug: labs-specialist
---

# SHBG (Sex Hormone-Binding Globulin)

## Metadata
- category: blood
- unit: nmol/L
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- adult men (~18–54 nmol/L working range): NHANES population interval 12.6–92.4 nmol/L; clinical lab reference (Quest) 10–50 nmol/L; mean ~28–37 nmol/L age-dependent; rises with age, lower in obesity/insulin resistance
- adult women (~40–120 nmol/L working range): NHANES interval 18.4–211.5 nmol/L; higher than men due to estrogenic hepatic stimulation; PCOS cohort median 42 nmol/L (IQR 28–63)
- no universal cutpoint: reference intervals are assay-specific and population-specific; no full harmonization across platforms
- age effect (men): SHBG rises ~9 nmol/L from younger (≤54 yr, mean 27.7) to older (≥55 yr, mean 36.6) men
- FAI = total T (nmol/L) / SHBG (nmol/L) × 100: used especially in women/PCOS (FAI > 4.5–5.0 indicates biochemical hyperandrogenism by Rotterdam criteria)
- source of target: [[library/biomarkers/shbg/research-report]] + Wang 2021 (PMID 34125885) + Krakowsky 2019 (PMID 28753796) + Rasquin Leon 2021 (PMID 34277990)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- LOWERS SHBG: insulin resistance/hyperinsulinemia (central driver — suppresses hepatic HNF-4α → SHBG gene transcription); obesity/central adiposity (chronic hyperinsulinemia + hepatic steatosis); type 2 diabetes; metabolic syndrome; NAFLD/MASLD; androgens/anabolic-androgenic steroids; glucocorticoids; hypothyroidism (removes thyroid-hormone stimulation of SHBG); growth hormone excess/acromegaly (via IGF-1 + insulin resistance); progestins (especially 19-nortestosterone derivatives); nephrotic syndrome (urinary SHBG loss)
- RAISES SHBG: aging (strongest positive predictor); estrogens/oral contraceptives (ethinylestradiol raises SHBG 80–300% above baseline)/pregnancy (several-fold rise); hyperthyroidism (T3/T4 are positive SHBG gene regulators); hepatic cirrhosis (impaired estrogen clearance → estrogen drives SHBG up); caloric restriction/anorexia nervosa/low energy availability (reduced insulin); anticonvulsants — phenytoin, carbamazepine (hepatic CYP induction); HIV infection (mechanism not fully resolved)
- Assay interferences: biotin supplementation (falsely LOW in streptavidin-based sandwich assays — withhold ≥8 h, ideally 48–72 h for high-dose); heterophile antibodies (falsely ELEVATED)

## Why It Matters
SHBG sets the bioavailable fraction of testosterone and estradiol: ~44% of testosterone is tightly SHBG-bound and biologically inert, while the albumin-bound (~50%) and free (~1–4%) fractions carry androgen activity. SHBG is therefore essential context for interpreting total testosterone — when SHBG is low (obesity, insulin resistance), total T understates bioavailable androgen and a numerically borderline total T may deliver normal free T; when SHBG is high (aging, hyperthyroidism, estrogen exposure), total T overstates androgen activity and a patient may be functionally androgen-deficient despite an acceptable total T. The Endocrine Society 2018 guideline explicitly recommends measuring free testosterone (calculated via the Vermeulen equation from total T + SHBG) when SHBG status is expected to be abnormal. Beyond androgen interpretation, low SHBG is an independent metabolic biomarker: each quartile decline in SHBG predicts incident metabolic syndrome (HR 1.44) and Mendelian randomization evidence supports a causal contribution to type 2 diabetes risk (Ding 2009 NEJM; OR ~0.09–0.10 highest vs. lowest quartile, genetically instrumented OR ~0.28–0.29). Assay variation (no global SHBG harmonization program; inter-platform bias ±10–25%) means results are not directly comparable across laboratories; use assay-specific reference intervals and run serial measurements on the same platform.

## Relations
- [[biomarkers/total-testosterone]]
- [[biomarkers/free-testosterone]]
- [[biomarkers/estradiol]]
- [[library/biomarkers/shbg/research-report]]
