---
title: Serum Potassium
type: biomarker
permalink: a-plus-maxing/biomarkers/potassium
category: blood
unit: mmol/L
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.potassium-design-work
provenance_slug: labs-specialist
---

# Serum Potassium

## Metadata
- category: blood
- unit: mmol/L (= mEq/L; monovalent, no conversion needed); serum runs ~0.2–0.5 mmol/L higher than plasma because platelets release K⁺ during clotting — in thrombocytosis this gap can exceed 2 mmol/L; always verify specimen type (serum vs. lithium-heparin plasma) when interpreting borderline results
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- reference interval: 3.5–5.0 mmol/L (serum; some labs report upper limit as 5.2 mmol/L)
- hypokalemia: < 3.5 mmol/L — mild 3.0–3.4, moderate 2.5–2.9, severe < 2.5
- hyperkalemia: > 5.0–5.5 mmol/L — mild 5.0–6.0, moderate 6.1–6.5, severe > 6.5
- optimal for mortality: 4.0–4.5 mmol/L (U-shaped mortality nadir across multiple large cohorts)
- first question on any elevated result: is this REAL or PSEUDOHYPERKALEMIA? — exclude hemolysis, fist-clenching, thrombocytosis, delayed processing before treating
- second question: transcellular shift (no change in total-body K⁺) vs. true total-body excess vs. impaired renal excretion
- ECG correlation: hyperK peaked-T → PR prolongation → P-wave loss → QRS widening → sine-wave → VF/asystole; hypoK T-wave flattening → U waves → QT/QU prolongation → torsades; ECG sensitivity for hyperK is poor (18–52% in retrospective series) — a normal ECG does NOT rule out dangerous hyperkalemia
- interpret with: eGFR, acid-base status, serum magnesium, full medication list, ECG
- source of target: [[library/biomarkers/potassium/research-report]]

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By

**HYPERKALEMIA (> 5.0–5.5 mmol/L):**

Decreased renal excretion (dominant mechanism):
- CKD/AKI — most common substrate; excretory reserve lost as eGFR falls below 30 mL/min/1.73 m²
- RAAS inhibitors: ACE inhibitors, ARBs, mineralocorticoid-receptor antagonists (spironolactone, eplerenone, finerenone) — block aldosterone-driven K⁺ secretion; risk ≤2% in uncomplicated hypertension, 5–10% with CKD/heart failure/diabetes on monotherapy, higher with combinations
- K⁺-sparing diuretics (amiloride, triamterene) — block ENaC, impair luminal K⁺ secretion driving force
- NSAIDs — suppress renin → reduce aldosterone + reduce GFR (triple hit)
- Trimethoprim — ENaC blocker, underappreciated cause of drug-induced hyperkalemia
- Calcineurin inhibitors (cyclosporine, tacrolimus) — suppress Na/K-ATPase + blunt aldosterone response
- Heparin/LMWH — suppress aldosterone synthesis
- Hypoaldosteronism: Addison's disease, Type 4 RTA (hyporeninemic hypoaldosteronism — common in elderly diabetics with CKD on RAAS inhibitors)

Transcellular shift OUT of cells:
- Metabolic acidosis: ~0.4–0.6 mmol/L rise per 0.1-unit pH fall (inorganic > organic acidosis)
- Insulin deficiency (DKA) — serum K⁺ falsely elevated at presentation despite total-body depletion; unmasks with insulin/fluid treatment
- Tissue destruction: rhabdomyolysis, tumor lysis syndrome, burns, intravascular hemolysis
- Non-selective beta-blockers (propranolol) — impair β₂-mediated Na/K-ATPase drive
- Digoxin toxicity — poisons Na/K-ATPase globally; doubly dangerous (raises K⁺ + sensitizes myocardium)
- Succinylcholine — motor endplate depolarization releases K⁺ from all muscle; potentially fatal in denervation/burns/immobilization

Pseudohyperkalemia — MUST BE EXCLUDED FIRST (no arrhythmia risk; treating causes iatrogenic hypokalemia):
- Hemolysis (#1 cause): difficult draw, small-gauge needle, fist-clenching, delayed processing
- Thrombocytosis: platelet K⁺ release during clotting; gap can exceed 2 mmol/L
- Extreme leukocytosis: cell lysis during centrifugation
- Delayed centrifugation/cold storage: Na/K-ATPase temperature-sensitive
- Familial pseudohyperkalemia (rare; PIEZO1/KCNN4/ABCB6 mutations; temperature-dependent red-cell K⁺ leak)

**HYPOKALEMIA (< 3.5 mmol/L):**

Renal and GI losses:
- Loop diuretics (furosemide, bumetanide) and thiazides — #1 pharmacological cause; increase distal Na⁺ delivery + aldosterone-driven K⁺ secretion
- Vomiting — primarily renal K⁺ loss via metabolic alkalosis (bicarbonaturia + aldosterone), not gastric loss per se
- Diarrhea, laxative abuse — direct GI K⁺ loss
- Primary hyperaldosteronism (Conn's syndrome) — hypokalemia + hypertension
- Secondary hyperaldosteronism: heart failure, cirrhosis, renal artery stenosis
- Bartter syndrome, Gitelman syndrome — hereditary salt-wasting tubulopathies
- RTA types 1 and 2 — impaired acid excretion + renal K⁺ wasting
- Amphotericin B — tubular membrane damage

Transcellular shift INTO cells:
- Insulin, glucose loading — Na/K-ATPase activation
- β₂-agonists (salbutamol/albuterol) — same ATPase pathway; clinically significant in high-dose nebulized therapy
- Metabolic alkalosis — H⁺/K⁺ exchange
- Refeeding syndrome — electrolyte shift into cells as anabolism restarts
- Thyrotoxic periodic paralysis — β-adrenergic hypersensitivity of Na/K-ATPase; East Asian males disproportionately affected

Hypomagnesemia → refractory hypokalemia (replace Mg first):
- Low intracellular Mg²⁺ releases ROMK channel inhibition → unrestrained renal K⁺ secretion regardless of K⁺ supplementation
- Causes: alcoholism, diuretics, PPI use, diarrheal illness

## Why It Matters
Serum potassium is the most acutely lethal common electrolyte: life-threatening arrhythmia — ventricular fibrillation, asystole, torsades de pointes — can occur at both extremes, making it the only routine electrolyte where an abnormal result can be a cardiac emergency. This urgency is compounded by the fact that serum K⁺ is a small extracellular window — only ~2% of total body potassium — and NOT a reliable measure of total-body stores; transcellular shifts from acid-base changes, insulin, or catecholamines can dramatically change serum K⁺ without altering whole-body content, while large depletions can coexist with a near-normal serum value. The pseudohyperkalemia artifacts (hemolysis being the most frequent) must be excluded before any treatment, because treating a spurious result risks iatrogenic hypokalemia in a patient who may already be depleted. A U-shaped mortality association is robustly documented across populations — acute MI, chronic heart failure, and a 27-cohort meta-analysis of 1.2 million participants (CKD Prognosis Consortium) — with the nadir at 4.0–4.5 mmol/L and excess mortality rising sharply at both low and high extremes. The central management tension in cardio-nephrology is the RAAS-inhibitor dilemma: ACE inhibitors, ARBs, and mineralocorticoid-receptor antagonists are the most effective drugs for reducing cardiorenal mortality, yet they are exactly the agents most likely to cause hyperkalemia in CKD, heart failure, and diabetes — the populations that benefit most. Novel potassium binders (patiromer, sodium zirconium cyclosilicate) enable continued RAAS-inhibitor use despite hyperkalemia. Interpretation always integrates eGFR, acid-base status, serum magnesium, full medication list, and ECG — the serum value alone is insufficient.

## Relations
- [[biomarkers/sodium]]
- [[biomarkers/egfr]]
- [[biomarkers/albumin]]
- [[library/biomarkers/potassium/research-report]]
