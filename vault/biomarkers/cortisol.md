---
title: Cortisol
type: biomarker
permalink: a-plus-maxing/biomarkers/cortisol
category: blood
unit: µg/dL
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.cortisol-design-work
provenance_slug: labs-specialist
---

# Cortisol

## Metadata
- category: blood
- unit: µg/dL (× 27.6 → nmol/L)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- morning serum (8 AM): ~5–25 µg/dL (~138–690 nmol/L); assay- and lab-dependent
- afternoon (~4 PM): ~3–10 µg/dL (~83–276 nmol/L)
- midnight nadir: typically <1.8 µg/dL (<50 nmol/L) in healthy individuals
- **A single random cortisol is rarely diagnostic — interpretation requires TIME + DYNAMIC TESTS:**
  - 1 mg overnight DST (Cushing's screen): suppress to <1.8 µg/dL (<50 nmol/L) = normal
  - late-night salivary cortisol: >~145 ng/dL (≈4 nmol/L) at midnight = abnormal
  - 24-h urinary free cortisol (UFC): integrates daily free-cortisol output; method-specific cutoffs
  - cosyntropin (ACTH 250 µg) stimulation test (AI screen): peak ≥18 µg/dL (≥497 nmol/L) rules out primary AI on older immunoassays; equivalent ~15 µg/dL (~411 nmol/L) on LC-MS/MS
- salivary and urinary assays measure FREE cortisol — unaffected by CBG changes; preferred when CBG is altered
- source of target: [[library/biomarkers/cortisol/research-report]] + Endocrine Society guidelines (Nieman 2008 PMID 18334580; Bornstein 2016 PMID 26760044)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISES cortisol:
  - acute and chronic psychological/physical stress (HPA activation)
  - Cushing's syndrome: pituitary adenoma (Cushing's disease), ectopic ACTH, adrenal adenoma/carcinoma, bilateral adrenal hyperplasia
  - exogenous glucocorticoids (most common cause overall; also cross-reacts in immunoassay → falsely elevated total)
  - estrogen / OCP / pregnancy: ↑CBG → ↑total cortisol (free cortisol may be normal — use salivary/UFC)
  - major depression, chronic alcohol use (pseudo-Cushing's states)
  - critical illness, major surgery
  - sleep deprivation (next-evening cortisol 37–45% higher after one night partial/total sleep loss)
  - acute intense exercise (transient)
- LOWERS cortisol:
  - adrenal insufficiency: primary (Addison's / autoimmune adrenalitis, TB, hemorrhage), secondary (hypopituitarism), tertiary (CRH deficiency)
  - exogenous-steroid-induced HPA suppression (most common cause of AI globally — any route)
  - hypopituitarism
  - time of day: nadir at midnight; a value without a draw time is uninterpretable
- ASSAY INTERFERENCES (falsely elevated total):
  - prednisolone 148% cross-reactivity on Roche Elecsys; methylprednisolone 249%
  - dexamethasone does NOT cross-react (safe for DST)
  - high-dose biotin (≥5–10 mg/day) on streptavidin-based platforms
  - heterophile antibodies / HAMA
  - CBG-lowering states (critical illness, nephrotic syndrome, cirrhosis) → falsely low total despite normal free cortisol

## Why It Matters
Cortisol is the primary glucocorticoid and the body's canonical stress hormone, produced by the adrenal cortex under HPA-axis control (hypothalamus → CRH → pituitary → ACTH → adrenal cortex). It regulates glucose metabolism, immune suppression, cardiovascular tone, and CNS arousal. Its secretion follows a steep circadian rhythm — approximately 10-fold higher at 8 AM than at midnight — meaning timed sampling and dynamic testing (not a single random value) are almost always required for clinical interpretation. Sustained excess (Cushing's syndrome) produces central obesity, proximal myopathy, hypertension, glucose intolerance, and violaceous striae; untreated it carries substantial morbidity. Deficiency (adrenal insufficiency) risks adrenal crisis — a life-threatening decompensation requiring immediate parenteral hydrocortisone — and must be recognized by pattern (low morning cortisol + elevated ACTH in primary AI, blunted cosyntropin response in all forms). Total serum cortisol is an unreliable index when CBG is abnormal (elevated in OCP/pregnancy/estrogen; suppressed in critical illness/cirrhosis/nephrotic syndrome) — salivary or urinary free cortisol is preferred in those states. NOTE: "adrenal fatigue" — the claim that subclinical cortisol deficiency from chronically stressed adrenals causes fatigue/brain fog — is not a recognized endocrine diagnosis and is unsupported by systematic review evidence (Cadegiani 2016, PMID 27557747).

## Relations
- [[biomarkers/dhea-s]]
- [[biomarkers/tsh]]
- [[library/biomarkers/cortisol/research-report]]
