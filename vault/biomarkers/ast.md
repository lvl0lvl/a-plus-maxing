---
title: AST (Aspartate Aminotransferase)
type: biomarker
permalink: a-plus-maxing/biomarkers/ast
category: blood
unit: U/L
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.ast-design-work
provenance_slug: labs-specialist
---

# AST (Aspartate Aminotransferase)

## Metadata
- category: blood
- unit: U/L (= IU/L)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20

## Target Range
- conventional lab ULN (men): ~40–50 U/L (lab-dependent; sex-specific)
- conventional lab ULN (women): ~35–40 U/L (lab-dependent)
- interpret via the **De Ritis ratio** (AST÷ALT) — load-bearing whenever AST is abnormal:
  - ratio > 2: alcoholic liver disease (alcohol-driven mitochondrial AST release + B6 depletion suppressing ALT)
  - ratio < 1: MASLD / acute viral hepatitis (cytoplasmic injury, ALT predominates)
  - ratio > 1 in chronic liver disease: advancing fibrosis / cirrhosis (progressive hepatocyte loss)
- ×ULN elevation bands: <2× borderline; 2–5× mild; 5–15× moderate; >15× marked; >10,000 U/L massive (ischemic/toxin)
- pair AST with ALT + CK to localize source:
  - AST↑ + CK↑ + ALT normal → muscle or cardiac source
  - AST↑ + ALT↑ + CK normal → hepatocellular injury
  - AST↑ + ALT normal + CK normal → consider macro-AST or hemolysis first
- macro-AST (benign): PEG precipitation with post-PEG recovery ≤40% confirms; no organ-directed treatment needed
- source of target: [[library/biomarkers/ast/research-report]] + Williams & Hoofnagle 1988 (PMID 3135226) + Nyblom 2004 (PMID 15208167) + ACG 2017 (PMID 27995906)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISES — hepatic: MASLD (ratio <1, ALT-dominant), alcoholic liver disease (ratio ≥2; hallmark), acute and chronic viral hepatitis, drug/toxin-induced liver injury, ischemic hepatitis / shock liver (AST often >1,000–5,000 U/L), Wilson disease, autoimmune hepatitis
- RAISES — non-hepatic (skeletal muscle — most common extrahepatic source): rhabdomyolysis (CK typically >10,000 U/L; median AST:ALT ratio 2.5 mimics ALD numerically), strenuous eccentric exercise, inflammatory myopathies (polymyositis/dermatomyositis), muscular dystrophies, generalized tonic-clonic seizures — AST 3–10× ULN in complete absence of liver disease
- RAISES — cardiac (historical): myocardial infarction (onset 12–24 h, peak 1–2 days; now supplanted by troponin for AMI diagnosis; troponin is sole guideline-endorsed cardiac biomarker)
- RAISES — hemolysis: erythrocyte AST is ~40× serum concentration; even mild in-vitro hemolysis (traumatic venipuncture, delayed processing) spuriously elevates AST with minimal effect on ALT, artifactually raising the De Ritis ratio — a major pre-analytic pitfall; true hemolytic anemia: LDH↑ + unconjugated bilirubin↑ + reticulocytosis + haptoglobin↓
- RAISES — other: hypothyroidism (muscle myopathy + secondary MASLD), celiac disease (intestinal inflammation-driven), macro-AST (benign immunoglobulin-AST complex)
- LOWERS: vitamin B6 (pyridoxal-5-phosphate) deficiency — assay-dependent; non-P5P reagents (>60% of labs) underestimate AST in B6-depleted patients (heavy alcohol use, dialysis, malnutrition); uremia/hemodialysis — systematically lower AST even in significant hepatic injury (B6 depletion + hemodilution)
- assay variable: non-P5P reagents miss apoenzyme fraction; IFCC procedure mandates P5P supplementation; P5P-supplemented assays may unmask or amplify macro-AST previously cryptic on non-P5P platforms

## Why It Matters
AST is a multi-organ aminotransferase expressed in liver, cardiac and skeletal muscle, red blood cells, kidney, brain, and pancreas — it is fundamentally less liver-specific than ALT. This means an isolated AST elevation cannot be attributed to hepatic injury without integrating ALT, CK, and hemolysis status. The De Ritis ratio (AST÷ALT) is the primary interpretive lens: >2 diagnoses alcoholic liver disease with high specificity (dual mechanism: mitochondrial AST release + preferential ALT suppression by B6 depletion); <1 characterizes MASLD and acute viral hepatitis; rising above 1 in chronic liver disease signals advancing fibrosis — an independent predictor of cirrhosis (HR 2.77 in chronic HBV). The ratio also carries cardiovascular prognostic weight: in the NHANES elderly cohort, a high De Ritis ratio conferred adjusted HR 1.68 for all-cause mortality and 1.67 for cardiovascular mortality. Hemolysis is a major pre-analytic pitfall unique to AST: erythrocyte AST is ~40-fold higher than serum concentration, so even mild in-vitro hemolysis artifactually elevates AST and the De Ritis ratio, potentially mimicking alcoholic liver disease on paper. Macro-AST is the benign mimic of persistent isolated elevation — confirmed by PEG precipitation — and prevents unnecessary invasive workup. Normal AST does not exclude liver disease: in advanced cirrhosis, diminished hepatocyte mass can normalize both aminotransferases while the De Ritis ratio remains elevated.

## Relations
- [[biomarkers/alt]]
- [[biomarkers/albumin]]
- [[biomarkers/fasting-glucose]]
- [[library/biomarkers/ast/research-report]]
