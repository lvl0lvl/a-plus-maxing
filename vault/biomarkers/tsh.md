---
title: TSH (Thyroid-Stimulating Hormone)
type: biomarker
permalink: a-plus-maxing/biomarkers/tsh
category: blood
unit: mIU/L
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.tsh-design-work
provenance_slug: labs-specialist
---

# TSH (Thyroid-Stimulating Hormone)

## Metadata
- category: blood
- unit: mIU/L (= µIU/mL numerically; older US reports use µIU/mL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- standard adult: ~0.4–4.0 mIU/L (some assays upper limit 4.5 mIU/L); log-normal distribution — geometric mean ~1.40 mIU/L in NHANES III; assay- and lab-specific
- upper-limit debate: NACB 2003 proposed ~2.5 mIU/L cutoff; 2012 AACE/ATA guidelines retain conventional ~4.0–4.5 mIU/L as operational standard; neither is universally settled
- age-drift: upper 97.5th percentile rises from ~3.56 mIU/L (age 20–29) to ~7.49 mIU/L (age ≥80); ~70% of older adults with TSH >4.5 mIU/L are within their age-appropriate range
- pregnancy (ATA 2017 preferred approach): population- and assay-specific local reference; pragmatic fallback = non-pregnant upper limit minus 0.5 mU/L per trimester; first trimester typically lowest
- pregnancy (ATA 2011 fixed fallback): first trimester 0.1–2.5 mIU/L; second 0.2–3.0 mIU/L; third 0.3–3.5 mIU/L
- subclinical hypothyroidism: TSH above upper limit + normal fT4 (HPT axis must be intact; not during acute illness)
- overt hypothyroidism: TSH elevated (often >10 mIU/L) + low fT4
- subclinical hyperthyroidism: TSH suppressed (<0.4 mIU/L; Grade 1: 0.1–0.39; Grade 2: <0.1) + normal fT4/fT3
- overt hyperthyroidism: TSH suppressed (<0.1 mIU/L) + elevated fT4 and/or fT3
- source of target: [[library/biomarkers/tsh/research-report]] + ATA 2017 pregnancy guidelines + NACB 2003 LMPG + AACE/ATA 2012 hypothyroidism guidelines

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISES TSH: Hashimoto's / autoimmune hypothyroidism (leading cause); iodine deficiency or excess (Wolff-Chaikoff); recovery phase of non-thyroidal illness (transient rebound); drugs — lithium, amiodarone, immune-checkpoint inhibitors (anti-PD-1/PD-L1/CTLA-4, up to 15–20% rate), interferon-alpha; thyroid surgery / radioiodine ablation; aging (physiological set-point shift); macro-TSH or heterophile antibody assay interference (falsely elevated)
- LOWERS TSH: Graves' disease / toxic nodule (stimulatory TSH-receptor antibodies or autonomous secretion); central (secondary/tertiary) hypothyroidism — low TSH + low fT4, the key exception where TSH alone misleads; exogenous thyroid hormone over-replacement (most common cause in clinical practice); glucocorticoids (high-dose) and dopamine / dobutamine (pituitary suppression); first-trimester pregnancy (hCG cross-reactivity, nadir ~10–12 weeks); acute phase of non-thyroidal illness; biotin supplementation ≥5 mg/day on streptavidin-based assays (falsely suppressed)

## Why It Matters
TSH is the first-line thyroid screen because the pituitary integrates thyroid hormone exposure over days-to-weeks and amplifies small fT4 changes into proportionally large TSH shifts — a 2-fold drop in fT4 can move TSH ~100-fold — making it far more sensitive than peripheral hormone measurements for detecting early dysfunction. Subclinical hypothyroidism (elevated TSH + normal fT4) carries graded cardiovascular risk above TSH ~7 mIU/L, with CHD event hazard ratios reaching ~1.89 at TSH 10–19.9 mIU/L in the 55,287-participant Thyroid Studies Collaboration meta-analysis; however, the TRUST RCT found no symptom or cardiovascular benefit from levothyroxine in 737 older adults with mild SCH, so treatment decisions are age- and TSH-level-dependent. Subclinical hyperthyroidism (suppressed TSH + normal fT4/fT3) is associated with atrial fibrillation (HR 1.68), increased all-cause mortality (HR 1.24), and substantially elevated fracture risk (hip fracture HR up to 1.61 at TSH <0.1 mIU/L). TSH alone misses central hypothyroidism (pituitary/hypothalamic failure produces low or normal TSH with low fT4) and lags dose changes by 4–8 weeks; always pair with fT4 when hypothyroidism is suspected, and wait ≥6–8 weeks after any dose adjustment before rechecking.

## Relations
- [[biomarkers/free-t4]]
- [[biomarkers/free-t3]]
- [[library/biomarkers/tsh/research-report]]
