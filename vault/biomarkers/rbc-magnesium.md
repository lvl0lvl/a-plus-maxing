---
title: RBC Magnesium
type: biomarker
permalink: a-plus-maxing/biomarkers/rbc-magnesium
category: blood
unit: mg/dL
source: lab
confidence: supported
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.rbc-magnesium-design-work
provenance_slug: labs-specialist
---

# RBC Magnesium

## Metadata
- category: blood
- unit: mg/dL of packed RBCs (↔ mmol/L: mg/dL ÷ 2.43)
- source: lab
- confidence: supported (RBC-Mg is an imperfect intracellular surrogate — no universal reference interval; results not interchangeable across labs; not a validated gold standard)
- review_cadence: per-lab-panel
- last_verified: 2026-06-20
- assay note: RBC-Mg is a SURROGATE for intracellular Mg status. No internationally standardized method exists. Reference intervals are lab- and method-specific (ICP-MS vs. AAS vs. colorimetric; normalization per hematocrit vs. Hb vs. RBC count). Use the reporting lab's own interval; do not compare values across labs.

## Target Range
- RBC-Mg (ICP-MS, Bithi 2024): ~4.2–6.7 mg/dL — lab/method-dependent, NOT standardized; legacy lab intervals vary (e.g., 3.6–7.5 mg/dL by some commercial labs)
- serum Mg (reference, for contrast): ~1.7–2.4 mg/dL (0.70–1.00 mmol/L)
- key point: a NORMAL serum Mg does NOT exclude deficiency — less than 1% of body Mg is extracellular; the kidney defends serum concentration at the expense of intracellular and bone stores (normomagnesemic/latent deficiency is common)
- functional reference: Mg-loading test — IV Mg bolus + 24-h urine; retention >27% of the administered dose indicates deficiency
- source of target: [[library/biomarkers/rbc-magnesium/research-report]] + Bithi et al. 2024 (PMID 39469428) + Gullestad et al. 1992 (PMID 1439510)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By

LOWERED (depletion):
- GI loss: chronic diarrhea, malabsorption, IBD, steatorrhea, bariatric surgery
- PPI use (chronic): FDA Drug Safety Communication (March 2, 2011) — impaired TRPM6/TRPM7 colonic transport; serious events (tetany, seizures, arrhythmia) reported after ≥1 year
- inadequate intake: processed/refined diet (strips germ/bran); 48% of Americans below EAR (NHANES 2013–2016)
- renal loss — diuretics: loop + thiazide diuretics → dose-dependent urinary Mg wasting (one of the most common iatrogenic causes)
- renal loss — alcohol: direct tubular wasting + acetaldehyde-mediated inhibition; one of the most common causes of clinically significant deficiency
- renal loss — uncontrolled diabetes / glycosuria: osmotic diuresis obligates Mg co-loss
- renal loss — nephrotoxic drugs: aminoglycosides, amphotericin B, cisplatin, tacrolimus, cyclosporine; cetuximab/EGFR antibodies inhibit TRPM6 expression
- renal loss — inherited tubulopathies: Gitelman syndrome (SLC12A3 loss-of-function → hypokalemia + metabolic alkalosis + hypomagnesemia); Bartter Type III
- redistribution: refeeding syndrome, hungry-bone syndrome post-parathyroidectomy, acute insulin or catecholamine surge

RAISED (hypermagnesemia — uncommon with normal renal function):
- renal failure (ESRD) with Mg-containing antacids or laxatives
- IV magnesium sulfate (obstetric — pre-eclampsia/eclampsia; monitored)

ARTIFACT:
- hemolysis FALSELY RAISES serum Mg (RBCs contain ~2–3× more Mg than serum; lysis floods plasma — prompt centrifugation within 60 min is mandatory)
- EDTA / citrate / oxalate tubes FALSELY LOWER Mg by chelation (use serum or lithium-heparin tubes; never purple-top/blue-top/grey-top for Mg)
- see [[compounds/magnesium]] for supplementation effects

## Why It Matters

Serum magnesium reflects less than 1% of total body Mg — the kidney defends that fraction by drawing down intracellular and bone stores, so a normal serum Mg does NOT exclude deficiency (chronic latent magnesium deficiency). RBC-Mg is a more sensitive but imperfect and poorly standardized intracellular surrogate; the Mg-loading test (retention >27%) is the functional reference when the diagnosis remains uncertain. The critical clinical consequence of magnesium deficiency is the **electrolyte interlock**: Mg depletion disinhibits the ROMK channel in the distal nephron, driving refractory hypokalemia that will not correct with potassium repletion alone; simultaneously, impaired adenylate cyclase function reduces PTH secretion and end-organ PTH response, causing refractory hypocalcemia unresponsive to calcium or vitamin D until Mg is restored. Severe hypomagnesemia lowers the threshold for torsades de pointes (TdP); IV Mg sulfate is the first-line treatment for acquired TdP. Observational data link low Mg intake/status to insulin resistance, type 2 diabetes, hypertension, and CVD; RCTs show modest but real BP reductions with Mg supplementation in deficient or at-risk populations (SMD −0.20 to −0.27 for SBP/DBP; Dibaba 2017) — effects are concentrated in those who are depleted, not in replete individuals.

## Relations
- [[biomarkers/potassium]]
- [[biomarkers/vitamin-d]]
- [[biomarkers/ferritin]]
- [[library/biomarkers/rbc-magnesium/research-report]]
