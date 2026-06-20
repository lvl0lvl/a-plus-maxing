---
title: eGFR (Estimated Glomerular Filtration Rate)
type: biomarker
permalink: a-plus-maxing/biomarkers/egfr
category: blood
unit: mL/min/1.73 m²
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.egfr-design-work
provenance_slug: labs-specialist
---

# eGFR (Estimated Glomerular Filtration Rate)

## Metadata
- category: blood
- unit: mL/min/1.73 m² (derived from serum creatinine [mg/dL ↔ µmol/L ×88.4] via the CKD-EPI 2021 race-free equation; cystatin C-based and combined equations are more accurate; note that serum creatinine is the measured analyte)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- normal: ≥90 mL/min/1.73 m² (G1, normal or high)
- mildly reduced: 60–89 mL/min/1.73 m² (G2; CKD requires ≥3 months + marker of kidney damage)
- CKD threshold: <60 mL/min/1.73 m² for ≥3 months = CKD by KDIGO criteria
- KDIGO GFR staging: G1 ≥90 / G2 60–89 / G3a 45–59 / G3b 30–44 / G4 15–29 / G5 <15 mL/min/1.73 m²
- albuminuria staging: A1 <30 mg/g ACR / A2 30–300 mg/g / A3 >300 mg/g; both axes independently predict CVD/ESRD/mortality (KDIGO heat map: G×A risk from green [low] to dark red [highest])
- serum creatinine conventional reference: ~0.7–1.3 mg/dL sex/lab-dependent (men higher than women; NOT a substitute for eGFR)
- MUSCLE-MASS CAVEAT: a "low" eGFR (55–65) in a muscular or creatine-supplementing person may NOT represent CKD — creatinine is elevated by muscle mass, not GFR loss; obtain measured GFR or cystatin C-based eGFR before labeling. Conversely, a "normal" eGFR in a sarcopenic, frail, or cachectic person may MASK true GFR loss (dangerous for drug dosing).
- source of target: [[library/biomarkers/egfr/research-report]] + KDIGO 2024 CKD Guideline (PMID 38490803) + Inker LA et al. 2021 (PMID 34554658)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- eGFR LOWERED / creatinine RAISED — true GFR loss: CKD (diabetes, hypertension, glomerulonephritis, PKD, aging); AKI (volume depletion, nephrotoxins, obstruction)
- eGFR FALSELY LOWERED / creatinine RAISED — non-GFR confounders: high muscle mass (bodybuilding, elite athletics); creatine supplementation (raises creatinine without changing GFR; washout several weeks before interpreting); cooked-meat meal within 12–24 h; drugs blocking tubular secretion (cimetidine, trimethoprim, cobicistat, dolutegravir — raise SCr by 10–20% with no actual GFR change)
- eGFR FALSELY RAISED / creatinine LOWERED — low-muscle-mass states: sarcopenia, cachexia, cirrhosis, limb amputation, prolonged bedrest (creatinine production falls → eGFR overestimates true GFR → dangerous drug-overdosing risk); pregnancy (true hyperfiltration + equations not validated in gestation)
- [[compounds/creatine]] (supplementation raises serum creatinine; falsely lowers eGFR — not nephrotoxicity)

## Why It Matters
eGFR is the best overall index of kidney function but is an **estimate** derived from serum creatinine, which reflects both kidney filtration and muscle mass. This creates two opposing clinical hazards: in muscular individuals (bodybuilders, creatine users) the equation can return a falsely low eGFR (55–65 mL/min/1.73 m²) that mimics G2–G3a CKD when actual filtration is normal — a label with real consequences for drug access, insurance, and referral; while in sarcopenic, frail, or cachectic individuals the equation can return a falsely high eGFR that masks genuine GFR loss, leading to full-dose prescribing of renally cleared drugs (NSAIDs, aminoglycosides, metformin, direct oral anticoagulants) in a patient whose actual clearance is substantially lower. The creatinine-blind range compounds this: a patient can lose ≥50% of kidney function while serum creatinine remains within the laboratory reference range, because the creatinine-GFR relationship is hyperbolic, not linear. The CKD-PC Matsushita 2010 meta-analysis (21 cohorts, N>1.2M across two parallel strata) established that low eGFR and elevated albuminuria independently and multiplicatively predict all-cause mortality, cardiovascular death, and ESRD — making both measurements together the appropriate minimum screen. When creatinine-eGFR is unreliable (extreme muscle mass, cirrhosis, drugs blocking secretion), cystatin C-based eGFR or the combined CKD-EPI 2021 creatinine + cystatin C equation should be used; measured GFR (iohexol clearance) is the reference standard for donor evaluation and narrow-therapeutic-window drug dosing.

## Relations
- [[biomarkers/alt]]
- [[biomarkers/ast]]
- [[biomarkers/albumin]]
- [[biomarkers/fasting-glucose]]
- [[library/biomarkers/egfr/research-report]]
