---
title: Total Testosterone
type: biomarker
permalink: a-plus-maxing/biomarkers/total-testosterone
category: blood
unit: ng/dL
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.total-testosterone-design-work
provenance_slug: labs-specialist
---

# Total Testosterone

## Metadata
- category: blood
- unit: ng/dL (× 0.0347 → nmol/L; 1 nmol/L = 28.8 ng/dL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- adult male (harmonized, non-obese, aged 19–39): 264–916 ng/dL (9.2–31.8 nmol/L) — 2.5th–97.5th percentile; median 531 ng/dL (18.4 nmol/L)
- hypogonadism threshold: ~300 ng/dL (10.4 nmol/L) is a clinical landmark, NOT a bright line — diagnosis requires ≥2 separate AM fasting samples below the lower limit PLUS symptoms; roughly 30% of men with one low value are normal on repeat
- female (premenopausal, LC-MS/MS): ~15–70 ng/dL (0.5–2.4 nmol/L); immunoassay unreliable at these concentrations
- collection: draw 08:00–10:00, fasting; afternoon draws may be 20–35% lower than morning peak
- assay preference: LC-MS/MS (CDC HoSt-certified); immunoassay acceptable above 300 ng/dL in men, but biased at low concentrations
- SHBG caveat: when SHBG is abnormal (obesity, aging, thyroid disease, liver disease, certain drugs), interpret total T alongside free or calculated free T
- source of target: [[library/biomarkers/total-testosterone/research-report]] + Travison 2017 (PMID 28324103) + Endocrine Society 2018 (PMID 29562364)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISES (men): TRT / exogenous androgens; hCG (LH-mimetic, preserves fertility); clomiphene / SERMs (reduce estrogen negative feedback → ↑LH/FSH → ↑T); weight loss in obese men (↑SHBG + remission of central HPG suppression)
- RAISES (women): PCOS (ovarian + adrenal androgen excess); androgen-secreting ovarian or adrenal tumors (rapid virilization, markedly elevated); congenital adrenal hyperplasia (21-hydroxylase deficiency); exogenous androgen administration
- LOWERS: aging (~1%/yr total T, ~2–3%/yr bioavailable T); obesity / metabolic syndrome / T2D (↓SHBG + central HPG suppression via aromatase/leptin/insulin); opioids (20–80% of chronic users develop biochemically confirmed hypogonadism via central GnRH inhibition); glucocorticoids (dual central + gonadal mechanism; mean 211 ng/dL vs. 449 ng/dL in matched controls); OSA / sleep deprivation; alcohol (acute: ↓LH pulse amplitude; chronic: Leydig cell toxicity); marijuana (cannabinoid inhibition of GnRH/LH pulsatility); hyperprolactinemia (central GnRH suppression); anabolic-androgenic steroids (HPG suppression → testicular atrophy; may take months–years to recover); chronic systemic illness
- Assay artifact — RAISES falsely: biotin supplementation ≥5 mg/day (competitive immunoassay); heterophile antibodies
- Assay artifact — LOWERS falsely: biotin (sandwich immunoassay platforms); acute illness (defer draw)

## Why It Matters
Total testosterone sums the three circulating pools (SHBG-bound ~44%, albumin-bound ~50%, free ~2%), making it the standard first-line androgen screen but an incomplete surrogate when SHBG is abnormal. Pairing with LH and FSH localizes the failure axis: primary hypogonadism (testicular failure) produces low T + high LH/FSH, while secondary/central hypogonadism (pituitary or hypothalamic failure) produces low T + low or inappropriately normal LH/FSH — distinguishing these drives treatment choice and fertility planning. The diagnostic threshold is a continuum: the Endocrine Society places the lower limit of normal at 264 ng/dL (CDC-harmonized) and requires two AM fasting samples plus symptoms before diagnosing hypogonadism, because diurnal variation, day-to-day biological variability (~10–15% CV), and assay imprecision mean that a single borderline value is unreliable. SHBG confounds the picture in both directions — obesity and insulin resistance suppress SHBG and lower total T while free T may be preserved; aging, liver disease, and thyroid excess raise SHBG and can mask free-T deficiency. For CV-safety context: the TRAVERSE RCT (5,246 men, 2023) showed TRT was noninferior to placebo for MACE (HR 0.96), but secondary signals emerged for atrial fibrillation, pulmonary embolism, and acute kidney injury, so the risk-benefit calculus is individual. Much of the observational association between low T and adverse outcomes reflects reverse causation — chronic disease and obesity suppress testosterone, not only the reverse.

## Relations
- [[biomarkers/free-testosterone]]
- [[biomarkers/shbg]]
- [[biomarkers/estradiol]]
- [[library/biomarkers/total-testosterone/research-report]]
