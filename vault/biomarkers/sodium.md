---
title: Serum Sodium
type: biomarker
permalink: a-plus-maxing/biomarkers/sodium
category: blood
unit: mmol/L
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.sodium-design-work
provenance_slug: labs-specialist
---

# Serum Sodium

## Metadata
- category: blood
- unit: mmol/L (= mEq/L; monovalent, no conversion needed); result is method-dependent — indirect ISE (standard hospital analyzers) and direct ISE (blood-gas analyzers) can differ by 2–7 mmol/L; pseudohyponatremia artifact on indirect ISE (and historical flame photometry) when severe hyperlipidemia or hyperproteinemia is present; direct ISE is immune
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- reference interval: 135–145 mmol/L (indirect ISE / standard chemistry platform)
- mild hyponatremia: 130–134 mmol/L
- moderate hyponatremia: 125–129 mmol/L
- severe hyponatremia: < 125 mmol/L
- hypernatremia: > 145 mmol/L; severe > 155 mmol/L
- interpret by tonicity (measure serum osmolality) + volume status (see 3-step algorithm in research report) — serum [Na⁺] reflects WATER balance, not salt intake
- glucose correction: Katz factor +1.6 mmol/L per 100 mg/dL glucose above normal; Hillier 1999 factor +2.4 mmol/L per 100 mg/dL (preferred — better validated, especially at glucose > 400 mg/dL)
- source of target: [[library/biomarkers/sodium/research-report]] + Spasovski et al. 2014 European hyponatremia guideline (PMID 24569125)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By

**HYPONATREMIA (< 135 mmol/L) — by volume status:**

- Hypovolemic (sodium + water loss; more water replaced): thiazide diuretics, GI losses (vomiting/diarrhea), third-spacing (burns/pancreatitis), adrenal insufficiency (aldosterone deficiency → renal salt wasting), cerebral salt wasting
- Euvolemic (water retention without edema): SIADH — SSRIs, carbamazepine, antipsychotics, small-cell lung cancer (ectopic ADH), CNS disease (stroke/TBI/meningitis), pulmonary disease (pneumonia/TB/ARDS), post-operative pain/nausea; hypothyroidism; glucocorticoid deficiency; primary polydipsia; beer potomania / low solute intake
- Hypervolemic (expanded ECF; effective volume perceived as low): heart failure, cirrhosis (incorporated into MELD-Na), nephrotic syndrome, advanced renal failure
- Exercise-associated (EAH): over-drinking hypotonic fluid during endurance events + non-osmotic ADH; weight gain during race is strongest predictor

**HYPERNATREMIA (> 145 mmol/L) — free-water deficit:**

- Impaired water access/thirst: elderly, neurological impairment, infants, iatrogenic restriction
- Central diabetes insipidus: ADH deficiency (neurosurgery, TBI, tumor, infiltration) — responds to desmopressin
- Nephrogenic diabetes insipidus: renal ADH resistance — lithium (AQP2 downregulation), hypercalcemia, chronic hypokalemia; hereditary (AVPR2/AQP2 mutations)
- Osmotic diuresis: hyperglycemia, mannitol, urea
- GI/skin losses without adequate water replacement: cholera/rotavirus diarrhea, burns, profuse sweating

**ARTIFACTS (not physiological dysnatremia):**
- Pseudohyponatremia (falsely LOW): indirect ISE or flame photometry + severe hypertriglyceridemia (typically > 10–15 mmol/L / > 1000 mg/dL) or severe hyperproteinemia (myeloma, IVIG) — normal osmolality on the same specimen confirms artifact; reflex to direct ISE (blood-gas analyzer) to correct
- IV-saline contamination (falsely HIGH): blood drawn above a running normal-saline infusion

## Why It Matters
Serum sodium is the single most abundant extracellular cation and the dominant determinant of plasma osmolality, but what it actually measures is the ratio of total-body exchangeable solutes to total body water — in other words, **water balance, not salt intake**. A patient can be hypervolemic with high total-body sodium yet hyponatremic if free-water retention outpaces sodium accumulation (heart failure, cirrhosis, nephrotic syndrome). Hyponatremia (< 135 mmol/L) is the most common electrolyte disorder in hospitalized adults (14–30% prevalence) and in both directions independently predicts increased short- and long-term mortality across heart failure, cirrhosis, general hospitalized patients, and community-acquired pneumonia — primarily as a severity marker of neurohormonal dysregulation. Acute symptomatic hyponatremia is directly dangerous via cerebral edema; even mild chronic hyponatremia (mean Na 126 mEq/L) causes objective gait instability and falls. The signature iatrogenic danger is **over-rapid correction of chronic hyponatremia**: once the brain has adapted by exporting osmolytes, correction faster than ≤ 6–8 mmol/L per 24 hours (≤ 8 per the 2014 European guideline; stricter for high-risk patients) risks osmotic demyelination syndrome (ODS). The symmetric danger in chronic hypernatremia — cerebral edema on over-rapid correction (limit: 10–12 mmol/L per 24 hours) — applies when the brain has accumulated idiogenic osmoles. Two measurement artifacts are essential to exclude before interpreting a result: pseudohyponatremia (indirect ISE or flame photometry + severe hyperlipidemia/hyperproteinemia — the only immune method is direct ISE) and IV-saline contamination (spuriously high sodium from a line above a running saline drip). Interpretation always requires layering serum osmolality and volume status before classifying etiology.

## Relations
- [[biomarkers/albumin]]
- [[biomarkers/egfr]]
- [[biomarkers/fasting-glucose]]
- [[library/biomarkers/sodium/research-report]]
