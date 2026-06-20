---
title: Vitamin B12 (Cobalamin)
type: biomarker
permalink: a-plus-maxing/biomarkers/vitamin-b12
category: blood
unit: pg/mL
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.vitamin-b12-design-work
provenance_slug: labs-specialist
---

# Vitamin B12 (Cobalamin)

## Metadata
- category: blood
- unit: pg/mL (= ng/L; conversion ↔ pmol/L: pg/mL × 0.738 = pmol/L)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20
- assay note: standard competitive-immunoassay measures total B12 (~80% metabolically inert haptocorrin-bound); this is an UNRELIABLE single test — poor sensitivity/specificity in the grey zone (~200–400 pg/mL / 148–300 pmol/L). Anti-intrinsic-factor antibodies (present in 50–70% of pernicious anemia patients) produce falsely normal or elevated results on IF-based platforms. Confirm true deficiency with MMA ± holotranscobalamin (holoTC); apply local platform reference range.

## Target Range
- reference (adults): ~200–900 pg/mL (148–664 pmol/L) — lab-dependent
- deficiency (NICE NG239): < 180 ng/L (< 133 pmol/L) total B12; < 25 pmol/L holoTC
- deficiency unlikely (NICE NG239): > 350 ng/L (> 258 pmol/L) total B12; > 70 pmol/L holoTC
- indeterminate grey zone: ~200–400 pg/mL (148–300 pmol/L) — total B12 cannot confirm or exclude deficiency here; add MMA ± holoTC
- MMA elevated (B12-specific, normal renal function): > 280–300 nmol/L
- holoTC indeterminate: 25–70 pmol/L
- note: B12 deficiency is a combined clinical and biochemical diagnosis — no single cutoff is definitive; local reference ranges vary by assay platform
- source of target: [[library/biomarkers/vitamin-b12/research-report]] + NICE NG239 (2024) + BSH Br J Haematol 2014 (PMID 24942828)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By

LOWERED (deficiency states):
- pernicious anemia — anti-parietal-cell and anti-intrinsic-factor (IF) antibodies; most common cause in developed countries; note IF-antibody false-normal analytical trap
- atrophic gastritis / aging — gastric hypochlorhydria impairs food-bound B12 release; dominant mechanism in adults ≥65; crystalline (supplement) B12 is unaffected
- gastrectomy / bariatric surgery — loss of parietal-cell mucosa eliminates IF secretion
- ileal disease or resection — Crohn's disease or ileal resection destroys cubilin receptor; cubam-mediated B12 uptake lost
- METFORMIN — calcium-dependent ileal membrane antagonism impairs B12–IF complex uptake at cubilin receptors; dose- and duration-dependent; routine monitoring guideline-endorsed
- PPIs / H2-blockers — acid suppression replicates food-bound malabsorption; crystalline B12 unaffected
- strict vegan / vegetarian diet — zero animal-product intake; stores (2–5 mg hepatic) deplete over 3–5 years
- exocrine pancreatic insufficiency — impaired haptocorrin cleavage in duodenum

RAISED:
- supplements / injections — common, benign; B12 is water-soluble with renal excretion; no documented toxicity
- liver disease (cirrhosis, hepatitis, HCC) — hepatocyte damage releases stored B12, impairs haptocorrin clearance; paraneoplastic red flag
- myeloproliferative neoplasms (CML, PV, myelofibrosis) — expanded granulocyte pool overproduces haptocorrin; CML can reach 10-fold normal
- solid malignancy (paraneoplastic) — unexplained persistent B12 ≥ 1000 ng/L; aOR 4.21 for metastatic solid cancer

ARTIFACT:
- IF-antibody false-normal — AIFAs in pernicious anemia bind the IF-based immunoassay reagent, skewing the result toward falsely normal/high; confirmed B12 within range does not exclude PA when clinical suspicion is present

## Why It Matters

Total serum B12 is an unreliable single test: it measures primarily the ~80% haptocorrin-bound fraction, which is metabolically inert, producing an indeterminate grey zone (~200–400 pg/mL / 148–300 pmol/L) where deficiency can be neither confirmed nor excluded — up to 45% of elderly samples fall here on total B12 alone. Confirming true deficiency requires functional markers: holotranscobalamin (holoTC; AUC 0.90 vs. 0.80 for total B12 in elderly cohort; an earlier and more accurate marker) and methylmalonic acid (MMA; most specific metabolic marker of tissue depletion, but rises independently with renal impairment). An additional analytical trap in pernicious anemia: anti-intrinsic-factor antibodies (present in 50–70% of PA patients) bind the IF-based immunoassay reagent and return a falsely normal B12 result — a normal value does not exclude PA when clinical features are present. Two safety points govern management and override the hematological picture: first, **neurological disease — subacute combined degeneration of the spinal cord (demyelination of dorsal columns and lateral corticospinal tracts) — can develop without anemia**; a normal CBC including normal MCV does not exclude neurologically significant B12 deficiency, and delay permits irreversible damage — treat on clinical suspicion. Second, **high folate intake (food fortification, supplements) masks the anemia of B12 deficiency while neurological damage progresses**: exogenous folic acid bypasses the methyl-folate trap and restores red cell maturation, eliminating the hematological signal, while the separate adenosylcobalamin pathway driving myelin synthesis remains impaired. Conversely, an unexplained persistently elevated B12 in a non-supplementing patient is a red flag for liver disease, myeloproliferative neoplasm, or solid malignancy — warrants active workup at ≥ 1000 ng/L.

## Relations
- [[biomarkers/ferritin]]
- [[biomarkers/vitamin-d]]
- [[biomarkers/fasting-glucose]]
- [[library/biomarkers/vitamin-b12/research-report]]
