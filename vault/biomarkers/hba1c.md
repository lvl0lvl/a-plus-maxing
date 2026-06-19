---
title: Hemoglobin A1c (HbA1c)
type: biomarker
permalink: a-plus-maxing/biomarkers/hba1c
category: blood
unit: "%"
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.hba1c-design-work
provenance_slug: labs-specialist
---

# Hemoglobin A1c (HbA1c)

## Metadata
- category: blood
- unit: % (NGSP); mmol/mol (IFCC) — linked by NGSP (%) = [0.09148 × IFCC] + 2.152
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- normal (ADA 2025): < 5.7% (< 39 mmol/mol)
- prediabetes (ADA): 5.7–6.4% (39–47 mmol/mol)
- diabetes threshold (ADA + WHO): ≥ 6.5% (≥ 48 mmol/mol) — confirmed on repeat test
- treatment target — general (most adults): < 7.0% (< 53 mmol/mol)
- treatment target — stringent (low-risk, short duration): < 6.5% (< 48 mmol/mol)
- treatment target — relaxed (complex/older adults): < 8.0% (< 64 mmol/mol)
- eAG reference: 6.0% ≈ 126 mg/dL (7.0 mmol/L) | 7.0% ≈ 154 mg/dL (8.6 mmol/L) | 8.0% ≈ 183 mg/dL (10.1 mmol/L)
- source of target: [[library/biomarkers/hba1c/research-report]] + ADA Standards of Care 2025/2026 + WHO 2011

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- falsely RAISED: iron-deficiency anemia (prolongs RBC lifespan, most common cause); vitamin B12 or folate deficiency (megaloblastic anemia); splenectomy/asplenia (removes senescent RBC clearance); certain hemoglobinopathies co-eluting on HPLC/CE (method-specific)
- falsely LOWERED: hemolytic anemia (any cause — autoimmune, G6PD, sickle-cell HbSS/HbCC/HbSC); recent blood loss or transfusion; EPO, iron, or B12/folate therapy (drives new RBC production, lowers mean cell age); late pregnancy (hemodilution + accelerated RBC turnover); splenomegaly; HbF elevation (hereditary persistence, some thalassaemias)
- CKD/dialysis: net effect usually falsely LOW — renal anemia + EPO-driven turnover; glycated albumin preferred in advanced CKD
- ethnicity offset: Black/African American individuals average ~0.3–0.4% higher HbA1c than White individuals at identical mean glucose; does not reflect greater pathology (no ethnic difference in HbA1c–retinopathy association in NHANES 2005–2008)
- genetics: HGI heritability ~39% (GWAS, ACCORD cohort); glycation gap heritability ~66–69% (twin studies); loci independent of FPG loci

## Why It Matters
HbA1c is the primary long-term glycaemic monitoring tool in diabetes care, integrating approximately 8–12 weeks of antecedent mean glucose via the irreversible Amadori glycation of haemoglobin β-chain N-terminal valines. Landmark trials establish that lowering HbA1c reduces microvascular complications continuously and with no lower threshold in early diabetes (DCCT: 76% retinopathy reduction at 7.0% vs. 9.0%; UKPDS 35: 37% microvascular risk reduction per 1% HbA1c decrease). Macrovascular benefit requires early metabolic control — UKPDS legacy data show 15% MI reduction (p ≈ 0.01) and 13% all-cause mortality reduction 10 years after trial end — but aggressive near-normalization in patients with established cardiovascular disease increases mortality (ACCORD: 22% excess, HR 1.22). In people without diabetes the lowest-mortality HbA1c range is approximately 5.0–5.5%; very low values (< 5.0%) raise all-cause mortality risk, likely via confounded states (hemolysis, chronic illness). HbA1c cannot resolve glycaemic variability, cannot substitute for CGM time-in-range metrics, and is invalid when RBC lifespan is disturbed.

## Relations
- [[biomarkers/fasting-glucose]]
- [[biomarkers/fasting-insulin]]
- [[library/biomarkers/hba1c/research-report]]
