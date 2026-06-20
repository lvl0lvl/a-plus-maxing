---
title: 25-Hydroxyvitamin D
type: biomarker
permalink: a-plus-maxing/biomarkers/vitamin-d
category: blood
unit: ng/mL
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.vitamin-d-design-work
provenance_slug: labs-specialist
---

# 25-Hydroxyvitamin D

## Metadata
- category: blood
- unit: ng/mL (SI: nmol/L; conversion: 1 ng/mL × 2.496 = nmol/L)
- measured analyte: 25(OH)D — the vitamin D STATUS marker, NOT the active hormone 1,25(OH)₂D
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20
- assay note: result depends on assay platform and VDSP standardization status; LC-MS/MS is reference-grade; immunoassays show ±10–30% inter-platform bias at clinically relevant concentrations; serial monitoring is most interpretable on the same platform at the same laboratory

## Target Range
- IOM / National Academy of Medicine (2011) — population bone-health adequacy:
  - deficiency: <12 ng/mL (<30 nmol/L)
  - at risk of inadequacy: 12–<20 ng/mL (30–<50 nmol/L)
  - adequate (97.5% of population): ≥20 ng/mL (≥50 nmol/L)
- Endocrine Society (2011) — individual optimization in at-risk patients:
  - deficiency: <20 ng/mL (<50 nmol/L)
  - insufficiency: 20–29 ng/mL (50–72 nmol/L)
  - sufficiency: ≥30 ng/mL (≥75 nmol/L)
- Endocrine Society (2024 update, Demay et al.): no longer endorses the 30 ng/mL target in healthy adults; recommends against routine screening; favors empiric supplementation for four evidence-supported groups
- potentially excessive: >50 ng/mL (>125 nmol/L); no established additional benefit above this range
- frank toxicity zone: >150 ng/mL (>375 nmol/L); hypercalcemia typically present; requires sustained massive supplementation
- interpretation note: a "low" result's significance depends on (1) which guideline the reporting laboratory uses, (2) assay standardization status — a non-VDSP-standardized immunoassay result of 20 ng/mL is not interchangeable with an LC-MS/MS result of 20 ng/mL
- source of target: [[library/biomarkers/vitamin-d/research-report]] + IOM/NAM 2011 DRI report + Endocrine Society 2011 CPG (Holick et al.) + Endocrine Society 2024 CPG (Demay et al.)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- LOWERS 25(OH)D:
  - low UVB exposure: high latitude, winter season, indoor occupation, sunscreen, full-body clothing
  - darker skin pigmentation: melanin competes with 7-dehydrocholesterol for UVB photons; requires substantially more sun exposure to synthesize equivalent vitamin D3
  - low dietary intake: few foods naturally rich in vitamin D; fortified foods/supplements necessary without sun
  - fat malabsorption: celiac disease, Crohn's/IBD, cholestatic liver disease, cystic fibrosis, bariatric surgery (especially Roux-en-Y gastric bypass)
  - obesity: volumetric dilution across larger body mass (evidence favors dilution over adipose sequestration as primary mechanism)
  - chronic kidney disease: impairs both hepatic 25-hydroxylation (early CKD) and renal 1α-hydroxylation
  - liver disease: impairs initial hepatic 25-hydroxylation step
  - nephrotic syndrome: urinary loss of vitamin D-binding protein (DBP) and its bound 25(OH)D
  - aging: skin 7-dehydrocholesterol content decreases ~75% between ages 20 and 80
  - drugs: anticonvulsants (phenytoin, carbamazepine), glucocorticoids, antiretrovirals, rifampin — induce CYP3A4/CYP24A1 and accelerate 25(OH)D catabolism
- RAISES 25(OH)D:
  - supplementation: vitamin D3 (cholecalciferol) raises and sustains 25(OH)D more potently than equimolar D2 (ergocalciferol), especially with infrequent dosing; see [[compounds/vitamin-d3]]
  - increased sun exposure (UVB to uncovered skin)
  - granulomatous disease (sarcoidosis, TB, berylliosis): raises 1,25(OH)₂D via ectopic macrophage CYP27B1 — the clinically relevant elevated metabolite in this context is 1,25, not 25(OH)D per se; both should be monitored

## Why It Matters
25(OH)D is the vitamin D status marker: it integrates cutaneous photosynthesis, dietary intake, and supplementation over weeks, and it is measured by the standard serum test. It is not the active vitamin D hormone — that is 1,25-dihydroxyvitamin D [calcitriol], which is homeostatically regulated and can be normal or elevated even when vitamin D stores are depleted. The deficiency syndromes — rickets in children (bowing deformities, hypocalcemic tetany), osteomalacia in adults (unmineralized osteoid, bone pain, stress fractures, proximal myopathy), and secondary hyperparathyroidism driving PTH-mediated bone resorption — are unambiguously causally linked to vitamin D deficiency and respond to repletion. This bone-axis causal evidence is solid. However, the large observational associations between low 25(OH)D and cardiovascular disease, cancer, and mortality have not been confirmed in major RCTs: VITAL (N = 25,871, 2,000 IU/day D3, 5.3 years) met neither its cancer nor CVD primary endpoints; D-Health (monthly 60,000 IU D3) showed no all-cause mortality benefit; ViDA (monthly high-dose D3) showed no CVD reduction. The most credible non-bone signal is VITAL's autoimmune ancillary (Hahn et al., BMJ 2022: 22% reduction in confirmed autoimmune disease, HR 0.78; 95% CI 0.61–0.99), pending independent replication. The 2024 Endocrine Society guideline (Demay et al.) reflects this RCT evidence base: it retires the 30 ng/mL target and recommends against routine screening in healthy adults. The practical guidance: document and correct deficiency for bone health and falls risk; do not chase a high-normal 25(OH)D number for cardiovascular or cancer prevention. The threshold debate (IOM ≥20 vs. Endocrine Society former ≥30) and assay-standardization variability mean that the exact numeric cutoff used, and the platform reporting it, are both load-bearing context for interpretation.

## Relations
- [[biomarkers/ferritin]]
- [[biomarkers/albumin]]
- [[library/biomarkers/vitamin-d/research-report]]
