---
title: Serum Albumin
type: biomarker
permalink: a-plus-maxing/biomarkers/albumin
category: blood
unit: g/dL
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.albumin-design-work
provenance_slug: labs-specialist
---

# Serum Albumin

## Metadata
- category: blood
- unit: g/dL (↔ g/L ×10); results not interchangeable across BCG vs. BCP laboratory methods
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- conventional reference interval: 3.5–5.0 g/dL (35–50 g/L); method- and age-dependent
- mild hypoalbuminemia: 3.0–3.5 g/dL (30–35 g/L) — increased surgical risk, impaired wound healing
- moderate hypoalbuminemia: 2.5–3.0 g/dL (25–30 g/L) — oncotic pressure meaningfully impaired
- marked hypoalbuminemia: < 2.5 g/dL (< 25 g/L) — edema/ascites risk; maximum Child-Pugh albumin score at < 2.8 g/dL
- hyperalbuminemia (> 5.0 g/dL): essentially dehydration/hemoconcentration or tourniquet artifact only
- interpret as a MULTI-FACTORIAL marker — liver synthesis + inflammation + protein loss + volume status — NOT as a direct nutrition marker; always pair with CRP
- source of target: [[library/biomarkers/albumin/research-report]]

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- LOWERED — decreased synthesis: cirrhosis / liver failure (dominant hepatic cause); severe malnutrition / malabsorption (celiac, short bowel, IBD) — clinically modest vs. inflammation
- LOWERED — inflammation (negative acute-phase reactant, dominant driver in clinical settings): IL-6 / TNF-α / IL-1 suppress albumin gene transcription AND increase capillary leak into interstitium (infection, sepsis, trauma, surgery, cancer, chronic disease, CKD, autoimmune disease); a low albumin with a high CRP is overwhelmingly inflammation-driven
- LOWERED — protein loss: nephrotic syndrome (urinary losses ≥3.5 g protein/day; hypoalbuminemia is only independent predictor of VTE in membranous nephropathy); protein-losing enteropathy (Crohn, lymphangiectasia); extensive burns / exfoliative dermatitis
- LOWERED — dilution / redistribution: fluid overload (large-volume crystalloid resuscitation, heart failure); pregnancy (plasma volume +40–50%; albumin falls to ~3.2–3.5 g/dL by third trimester); capillary leak syndromes
- RAISED: dehydration / hemoconcentration (essentially the only cause); prolonged tourniquet artifact (pre-analytic)
- MEASUREMENT BIAS: BCG overestimates vs. BCP and immunoassay — bias widens with inflammation and at low albumin concentrations (up to 9.9 g/L gap at severe hypoalbuminemia); BCP underestimates in CKD/uremia (carbamylation blocks binding sites)

## Why It Matters
Serum albumin is the major oncotic protein in plasma — responsible for ~70–80% of plasma colloid osmotic pressure — and a marker of hepatic synthetic function, but its most clinically common meaning is **illness severity and inflammation**, not nutritional status. Albumin is a negative acute-phase reactant: IL-6 from any inflammatory insult (infection, surgery, cancer, chronic disease) directly suppresses albumin synthesis and simultaneously increases capillary permeability, shifting albumin out of the vascular space within hours to days. The ASPEN 2021 position statement explicitly states albumin "should not be used as a nutrition marker" for this reason. Despite being one of the strongest routine mortality predictors in medicine — Seidu et al.'s meta-analysis of 1,492,237 participants found RR 0.66 for all-cause mortality comparing top vs. bottom albumin thirds — the ALBIOS RCT (n=1,818 septic shock patients) showed that albumin supplementation confers zero mortality benefit (RR 1.00), confirming it is a marker, not a lever. The ~19–21 day plasma half-life makes albumin a reliable index of sustained hepatic function and chronic physiological reserve but a **poor acute-nutrition tracker**. Albumin also anchors two routine corrections: the Payne corrected-calcium formula (for hypoalbuminemia-adjusted calcium) and the Figge anion-gap correction (each 1 g/dL drop in albumin lowers the expected anion gap by ~2.5 mEq/L). BCG and BCP assay methods are not interchangeable — BCG overestimates particularly in inflammatory/malignant states; method consistency across serial measurements is essential.

## Relations
- [[biomarkers/alt]]
- [[biomarkers/ast]]
- [[biomarkers/egfr]]
- [[biomarkers/hs-crp]]
- [[library/biomarkers/albumin/research-report]]
