---
title: hs-CRP — High-Sensitivity C-Reactive Protein
type: biomarker
permalink: a-plus-maxing/biomarkers/hs-crp
category: blood
unit: mg/L
source: lab
confidence: established
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.hs-crp-design-work
provenance_slug: labs-specialist
---

# hs-CRP — High-Sensitivity C-Reactive Protein

## Metadata
- category: blood
- unit: mg/L (CRP sometimes reported in mg/dL; 1 mg/dL = 10 mg/L, so 3.0 mg/L = 0.3 mg/dL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- low CV risk: < 1.0 mg/L (AHA/CDC tertile)
- average (moderate) CV risk: 1.0–3.0 mg/L (AHA/CDC tertile)
- high CV risk: > 3.0 mg/L (AHA/CDC tertile)
- alert / discard-and-retest: > 10 mg/L = acute inflammation, infection, or trauma — do NOT use for CV risk; defer and RETEST ~2 weeks later when metabolically stable
- best practice: measure TWICE, ≥ 2 weeks apart, in metabolically stable patients; average the results or use the lower value (justified by the ~44–59% within-subject biological CV)
- source of target: [[library/biomarkers/hs-crp/research-report]] + AHA/CDC scientific statement (Pearson et al., Circulation 2003;107(3):499–511; PMID 12551878)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- raised by: adiposity / BMI (major modifiable determinant — visceral fat secretes IL-6 driving hepatic CRP; BMI alone ~15% of CRP variance), acute infection / inflammation / trauma / surgery / MI (the >10 mg/L spikes), smoking, metabolic syndrome / type 2 diabetes, aging, sleep disturbance, depression, physical inactivity
- raised by (route-dependent artifact): oral estrogen / hormone therapy / combined oral contraceptives (first-pass hepatic CRP synthesis; oral but NOT transdermal — may NOT reflect vascular inflammation)
- lowered by: [[compounds/statins]] (~15–37%; partly LDL-independent), weight loss (~9.4% reduction lowered CRP), exercise (moderate-intensity, >12 weeks; SMD −0.53)

## Why It Matters
hs-CRP is a marker of residual inflammatory cardiovascular risk that is independent of, and additive to, the lipid profile — in JUPITER, an elevated-hs-CRP / normal-LDL population that lipids alone would miss still benefited from statin therapy. It is a hepatic acute-phase reactant driven by IL-6, so it reads out the activity of the upstream inflammatory pathway. The decisive interpretive point: the CAUSAL target is the IL-6/IL-1β pathway (proven by CANTOS, where anti–IL-1β canakinumab cut events without changing lipids), NOT CRP itself — Mendelian randomization is null for CRP causality (CRP-lowering genotypes: OR 1.00, 95% CI 0.97–1.02). Treat hs-CRP as a window onto inflammatory risk, not a lever to push down for its own sake.

## Relations
- [[biomarkers/glyca]]
- [[biomarkers/ldl-c]]
- [[biomarkers/apob]]
- [[library/biomarkers/hs-crp/research-report]]
