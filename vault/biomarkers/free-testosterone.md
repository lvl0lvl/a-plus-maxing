---
title: Free Testosterone
type: biomarker
permalink: a-plus-maxing/biomarkers/free-testosterone
category: blood
unit: pg/mL
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.free-testosterone-design-work
provenance_slug: labs-specialist
---

# Free Testosterone

## Metadata
- category: blood
- unit: pg/mL (× 3.467 → pmol/L; ÷ 10 → ng/dL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- adult male, ED-measured (all men ≥19 yr): 66–309 pg/mL (229–1072 pmol/L) — 2.5th–97.5th percentile; Jasuja et al. 2023, standardized equilibrium dialysis, nonobese men
- adult male, ED-measured (19–39 yr): 120–368 pg/mL (415–1274 pmol/L) — 2.5th–97.5th percentile
- calculated free T (Vermeulen) is the practical clinical standard when ED is unavailable; it overestimates ED values by a median of ~1.19× — apply calculated-method reference intervals, not ED intervals
- **direct analog immunoassay is DISCOURAGED — Endocrine Society 2018 advises clinicians should NOT use it; values are ~1/7 of ED values and track total testosterone, not the free fraction**
- harmonized reference interval: does NOT exist; ranges vary by method, formula, and laboratory — always confirm which method the reporting lab uses
- when to measure free T (not just total T): whenever total T is borderline low OR SHBG is abnormal (obesity, insulin resistance, aging, liver disease, thyroid disorders, HIV, anticonvulsants, estrogen exposure)
- source of target: [[library/biomarkers/free-testosterone/research-report]] + Endocrine Society 2018 (PMID 29562364) + Jasuja 2023 (DOI 10.1111/andr.13310)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISED: TRT / exogenous androgens (raise total T AND suppress SHBG — doubly raise free fraction); hCG (raises Leydig cell total T output); conditions lowering SHBG: obesity, insulin resistance, type 2 diabetes, metabolic syndrome, hypothyroidism, glucocorticoids, androgens, growth hormone excess
- LOWERED: aging (total T falls + SHBG rises — compressed from both ends; ~30–40% decline from 20s to 70s by ED); opioids, glucocorticoids, chronic illness (suppress HPG axis → lower total T); anything raising SHBG: hyperthyroidism, estrogen/oral contraceptives, hepatic cirrhosis, HIV chronicity, anticonvulsants — lowers free T without necessarily lowering total T; central adiposity with low SHBG (net effect depends on relative degree of total-T suppression vs. SHBG suppression)
- Assay artifact — RAISES cFT inputs falsely: biotin ≥5 mg/day (competitive immunoassay format for TT or SHBG); withhold ≥72 hr before sampling
- Assay artifact — DISTORTS cFT inputs: heterophile antibodies (cross-react with assay antibodies on TT or SHBG immunoassays); confirm with LC-MS/MS if clinically discordant
- Assay artifact — analog free T: tracks total T, not free T; do not use

## Why It Matters
Free testosterone is the biologically active fraction of circulating testosterone — the ~2% that is unbound, diffusible across cell membranes, and able to engage the androgen receptor directly. The remaining testosterone is sequestered: ~44% tightly bound to SHBG (biologically inert) and ~50–54% loosely bound to albumin (largely bioavailable). When SHBG is normal, total testosterone is a reasonable proxy for free T. When SHBG is abnormal — which is common in obesity, insulin resistance, aging, liver disease, thyroid dysfunction, HIV, and with many medications — total testosterone misleads in both directions: suppressed SHBG causes total T to over-diagnose deficiency (the obese man with 52% apparent hypogonadism by total T vs. 17.6% by free T); elevated SHBG causes total T to mask it (the HIV patient where adding free T doubles the hypogonadism detection rate). Three methods exist and are not interchangeable: equilibrium dialysis + LC-MS/MS (gold standard, rarely routine), calculated free T via Vermeulen equation (endorsed by the Endocrine Society, ~1.19× overestimate vs. ED, requires its own reference range), and direct analog immunoassay (explicitly discouraged — results are ~1/7 of ED and reflect total T, not the free fraction). No harmonized reference interval exists across methods. In women, calculated free T and the free androgen index (FAI) are the standard markers for hyperandrogenism in PCOS, where cFT achieves pooled sensitivity of 0.89 vs. 0.74 for total T.

## Relations
- [[biomarkers/total-testosterone]]
- [[biomarkers/shbg]]
- [[biomarkers/estradiol]]
- [[library/biomarkers/free-testosterone/research-report]]
