---
title: Free T4 (Free Thyroxine)
type: biomarker
permalink: a-plus-maxing/biomarkers/free-t4
category: blood
unit: ng/dL
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.free-t4-design-work
provenance_slug: labs-specialist
---

# Free T4 (Free Thyroxine)

## Metadata
- category: blood
- unit: ng/dL (×12.87 → pmol/L; US labs report ng/dL, most international labs report pmol/L)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- adult (immunoassay): ~0.8–1.8 ng/dL (~10–23 pmol/L); assay- and method-dependent — NOT freely transferable across platforms; a value of 1.0 ng/dL on one analyzer may read as 1.4 ng/dL on another
- pregnancy (trimester-specific, method-specific required — ATA 2017): first trimester ~1.08–2.05 ng/dL (13.9–26.5 pmol/L); second trimester ~0.95–1.50 ng/dL (12.3–19.3 pmol/L); third trimester ~0.88–1.49 ng/dL (11.4–19.2 pmol/L); these are Siemens Centaur-derived illustrative values only; use assay-matched local intervals when available; immunoassay accuracy degrades throughout gestation
- TSH/fT4 diagnostic grid:
  - high TSH + low fT4 → overt primary hypothyroidism
  - high TSH + normal fT4 → subclinical hypothyroidism
  - suppressed TSH + high fT4 → overt hyperthyroidism
  - suppressed TSH + normal fT4 → subclinical hyperthyroidism
  - low fT4 + low-to-normal TSH → central hypothyroidism (pituitary/hypothalamic failure — TSH alone systematically misses this)
- central hypothyroidism levothyroxine target: fT4 above midnormal of reference range (ATA 2014 Jonklaas et al.)
- source of target: [[library/biomarkers/free-t4/research-report]] + ATA 2017 pregnancy guidelines (Alexander et al.) + NACB 2003 LMPG (Baloch et al.) + ATA 2014 hypothyroidism guidelines (Jonklaas et al.)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISES fT4 (physiological/pathological): Graves' disease (TSI-driven unregulated synthesis); toxic multinodular goiter or toxic adenoma (autonomous secretion); exogenous/factitious levothyroxine excess; thyroiditis destructive phase (subacute, postpartum, amiodarone type 2); amiodarone-induced thyrotoxicosis (types 1 and 2); acute psychiatric admission (stress-driven transient shift, normalizes by discharge)
- RAISES fT4 (assay artifact — clinically euthyroid): familial dysalbuminemic hyperthyroxinemia (FDH; R218H albumin mutation; affects most one-step immunoassays — Beckman ACCESS most susceptible, Ortho VITROS largely resistant; confirm with equilibrium dialysis); high-dose biotin ≥5–10 mg/day on streptavidin-based platforms (Roche, Siemens, Beckman — also falsely suppresses TSH, mimics hyperthyroidism; stop biotin 2–7 days before testing); heparin (IV or SC) via in-vitro lipoprotein lipase activation releasing free fatty acids that displace T4 from binding proteins; heterophile/anti-streptavidin/anti-ruthenium antibodies
- LOWERS fT4 (physiological/pathological): primary hypothyroidism (Hashimoto's, post-thyroidectomy, post-radioablation, severe iodine deficiency); central hypothyroidism (pituitary or hypothalamic disease — TSH unreliable; fT4 is the diagnostic anchor); non-thyroidal illness / euthyroid sick syndrome (cytokines + macronutrient restriction suppress HPT axis; distinguish from central hypothyroidism clinically); phenytoin and carbamazepine (enzyme induction + T4 displacement — routine immunoassay may show low fT4 in euthyroid patients; use TSH as primary monitor unless central hypothyroidism independently suspected)
- note: assay-method dependence and pregnancy matrix effects alter measured fT4 independent of true thyroid status; always interpret with the platform's own reference interval

## Why It Matters
Free T4 is the biologically available form of thyroxine — the only fraction capable of entering cells, binding nuclear receptors (via local conversion to T3 by deiodinases), and regulating metabolism. Although TSH is the first-line thyroid screen, fT4 is the essential reflex test when TSH is abnormal: it confirms overt versus subclinical disease and provides a severity gradient. More critically, fT4 is diagnostically indispensable in central hypothyroidism, where TSH is low or inappropriately normal despite genuine hormone deficiency — a pattern that a TSH-alone strategy systematically misses. During levothyroxine therapy for central hypothyroidism, fT4 (not TSH) is the primary monitoring endpoint. fT4 also fills the gap in the first 4–8 weeks after any dose change before TSH has equilibrated to the new steady state. Because immunoassay estimates of fT4 are not standardized across platforms, results are interpretable only relative to the same laboratory's method-specific reference interval.

## Relations
- [[biomarkers/tsh]]
- [[biomarkers/free-t3]]
- [[library/biomarkers/free-t4/research-report]]
