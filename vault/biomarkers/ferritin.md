---
title: Serum Ferritin
type: biomarker
permalink: a-plus-maxing/biomarkers/ferritin
category: blood
unit: ng/mL
source: lab
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.ferritin-design-work
provenance_slug: labs-specialist
---

# Serum Ferritin

## Metadata
- category: blood
- unit: ng/mL (= µg/L; 1:1 equivalence — both notations appear in guidelines)
- measured analyte: serum ferritin — the L-subunit-rich, glycosylated, iron-poor secreted fraction; reflects intracellular iron-storage pools under non-inflammatory conditions
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-20
- assay note: inter-platform CV ~23% on the same specimens; no single cutoff is fully platform-agnostic; apply thresholds in the context of the reporting laboratory's assay and calibration lineage; hook effect (antigen excess → falsely LOW signal) at extreme concentrations — alert lab to dilute and re-run when clinical picture demands very high ferritin but result is paradoxically normal or mildly elevated

## Target Range
- reference (adult men): ~30–300 ng/mL
- reference (adult women, premenopausal): ~13–150 ng/mL; converges toward male range postmenopause
- IRON DEFICIENCY THRESHOLDS (in the absence of inflammation):
  - < 15 ng/mL: absent stores — high specificity (~99%), sensitivity ~59% [Guyatt 1992 meta-analysis, AUROC 0.95]
  - < 30 ng/mL: low stores — operational threshold (BSG 2021; WHO 2020); Cochrane 2021: 79% sensitivity, 98% specificity
  - < 45–50 ng/mL: functional suboptimum — maximises sensitivity; supported by physiological evidence (iron absorption rises below ~51 ng/mL)
- INFLAMMATION-ADJUSTED THRESHOLDS (raise cutoffs when CRP is elevated):
  - WHO 2020: < 70 ng/mL when CRP > 5 mg/L or α-1 acid glycoprotein elevated
  - ESC 2021 (heart failure): absolute iron deficiency < 100 ng/mL; functional iron deficiency 100–299 ng/mL + TSAT < 20%
  - KDIGO (dialysis CKD): treatment trigger ≤ 500 ng/mL + TSAT ≤ 30%
- no firm upper disease threshold; > 1,000 ng/mL widens the differential substantially (see Why It Matters)
- always interpret WITH CRP and TSAT — a single ferritin value without inflammatory context is frequently uninterpretable
- source of target: [[library/biomarkers/ferritin/research-report]] + BSG Gut 2021 (PMID 34497146) + WHO Guideline 2020 + Cochrane CD011817 2021 (PMID 34028001) + Guyatt J Gen Intern Med 1992 (PMID 1487761) + ESC Eur Heart J 2021 (PMID 34447992)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By

LOW ferritin (= iron deficiency — highly specific; almost nothing else causes a fall):
- blood loss: occult GI bleeding (leading cause in men and postmenopausal women; ~1/3 have structural GI lesion including malignancy); heavy menstrual bleeding (leading cause in premenopausal women); frequent blood donation
- malabsorption: celiac disease (under-recognized; test in all unexplained iron deficiency); IBD; atrophic gastritis; *H. pylori* infection; proton-pump inhibitor use; bariatric surgery (Roux-en-Y gastric bypass bypasses duodenum/proximal jejunum — the primary iron absorptive segment)
- increased demand: pregnancy, infancy, rapid growth
- endurance athletes: exercise-induced hepcidin surges (IL-6, peak 3–6 h post-exercise) block iron absorption; foot-strike hemolysis; GI blood loss during prolonged running; sweat losses — convergent deficit mechanism

HIGH ferritin (broad differential; the most common causes are NOT iron overload):
- INFLAMMATION / acute-phase (most common): any systemic inflammatory state (infection, autoimmune, malignancy, major surgery, tissue injury) — cytokine-driven (IL-6, TNF-α, IL-1β via NF-κB); ferritin reflects inflammatory load, not iron stores; CRP is essential context
- liver disease / alcohol: hepatocellular injury leaks ferritin; alcohol independently stimulates ferritin synthesis; hepatitis (viral/autoimmune/toxic), cirrhosis, acute liver failure
- metabolic / MASLD: dysmetabolic hyperferritinaemia — typically 300–1,000 ng/mL, normal or mildly elevated TSAT, in metabolic syndrome / insulin resistance / MASLD; driven by altered iron-regulatory gene expression + steatoinflammation; PNPLA3 / TM6SF2 variant carriage increases risk; independent predictor of fibrosis progression (HR 1.68 all-cause mortality, HR 1.92 liver-related events in 7,333-patient MASLD cohort)
- malignancy: hematologic (lymphoma, leukemia, myeloma) and solid tumors (esp. hepatocellular carcinoma)
- iron overload — hemochromatosis (HFE C282Y homozygosity): **requires proof** — diagnostic algorithm = TSAT > 45% (fasting) + HFE genotyping; ferritin is a severity marker not a primary diagnostic test; penetrance markedly variable (iron-overload disease: 28.4% in men, 1.2% in women at 12-year follow-up in n = 31,192 cohort); transfusional overload confirmed by transfusion history + MRI liver/heart
- EXTREME (> 1,000–10,000+ ng/mL): HLH / macrophage activation syndrome (MAS) / adult-onset Still's disease (AOSD) — pathological macrophage activation; ferritin is a diagnostic criterion within the 17-variable HLH framework (2024 Blood guidelines); HScore (9-variable including ferritin, temperature, organomegaly, cytopenias, triglycerides, fibrinogen, AST) achieves 93% sensitivity / 86% specificity at cutoff 169 (n = 312 validation cohort) — NOT an indication for phlebotomy; immune emergency requiring urgent treatment

## Why It Matters

Serum ferritin is the best single laboratory test for iron stores: a low value (< 15–30 ng/mL) is essentially diagnostic of iron deficiency — almost nothing else drives ferritin down, making a low result highly specific without requiring further corroboration. However, ferritin is simultaneously a **positive acute-phase reactant** driven by IL-6, TNF-α, and IL-1β via NF-κB, meaning a normal or elevated ferritin does NOT exclude iron deficiency when inflammation, infection, or chronic disease is present. In those contexts, hepcidin — upregulated by IL-6 via JAK2–STAT3 — sequesters iron within macrophages and hepatocytes, producing **functional iron deficiency**: iron-starved erythropoiesis (low TSAT, low reticulocyte hemoglobin content) despite a non-low ferritin. This is the dominant iron-deficiency pattern in CKD, chronic heart failure, and active IBD, and it is systematically missed by ferritin-only thresholds. Conversely, a high ferritin should not be interpreted as iron overload without supporting evidence: the vast majority of hyperferritinemia in routine practice reflects inflammation, liver disease, alcohol, or metabolic dysfunction, not hemochromatosis. True iron overload requires TSAT > 45% plus HFE genotyping to establish. The assay itself carries two technical caveats: (1) inter-platform harmonization is poor (median inter-assay CV ~23%), so fixed thresholds are not platform-agnostic; and (2) the hook effect — antigen excess paradoxically suppressing the immunoassay signal — can yield a falsely normal or low result in HLH and other extreme hyperferritinemia states, with errors exceeding 1,000-fold in documented cases. Ferritin should always be interpreted alongside CRP (quantifies inflammatory contribution), TSAT (assesses iron availability for erythropoiesis), and — when those are equivocal — soluble transferrin receptor (sTfR), which rises with iron-deficient erythropoiesis and is not an acute-phase reactant.

## Relations
- [[biomarkers/vitamin-d]]
- [[biomarkers/albumin]]
- [[biomarkers/hs-crp]]
- [[library/biomarkers/ferritin/research-report]]
