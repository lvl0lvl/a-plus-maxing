# Section C: Measurement & Standardization

## Dye-Binding Assays: BCG and BCP

Serum albumin measurement in routine clinical chemistry relies predominantly on two colorimetric dye-binding methods: bromocresol green (BCG) and bromocresol purple (BCP). Both are fast, inexpensive, and fully automatable, which explains their dominance on high-throughput chemistry analyzers worldwide [1, mechanism_review]. They are not interchangeable.

**BCG systematically overestimates albumin** because the dye binds nonspecifically to proteins beyond albumin — chiefly the acute-phase alpha-1 and alpha-2 globulins. At normal albumin concentrations (≥35 g/L), the BCG–BCP gap is modest: approximately 3 g/L [2, cohort]. It widens substantially as albumin falls. In a controlled method-comparison study using capillary zone electrophoresis (CZE) as the reference standard, BCG showed a mean positive bias of 3.54 g/L relative to CZE, while BCP differed by less than 1 g/L [2, cohort]. The overall BCG–BCP mean difference in that population was 6.4 g/L (95% CI 5.88–6.96), governed by the regression equation BCG = (0.784 × BCP) + 12.58 [2, cohort]. The bias is not constant: at mild hypoalbuminemia (30–35 g/L) it averaged 6.3 g/L, and at severe hypoalbuminemia (≤20 g/L) it reached 9.9 g/L [2, cohort]. This concentration-dependent amplification means BCG is most misleading precisely where accurate measurement matters most. The mechanism is confirmed: BCG overestimation correlates strongly with alpha-1 globulin (r = 0.758, p < 0.001) and CRP (r = 0.729, p < 0.001), both elevated in infection, inflammation, and malignancy [2, cohort]. The original BCP method paper demonstrated that BCP does not react with albumin-free serum globulin preparations or pure human transferrin, confirming its superior dye-binding specificity [1, mechanism_review].

**BCP is more specific but underestimates albumin in chronic kidney disease (CKD) and uremia.** In hemodialysis patients, BCP reads lower than immunonephelometry (INP) by 0–4 g/L, while BCG reads 4–10 g/L higher than INP on the same samples [3, cohort]. The cause is carbamylation: urea accumulating in CKD spontaneously decomposes to isocyanic acid, which covalently modifies albumin's lysine residues. Carbamylated albumin binds BCP less efficiently — BCP's two binding sites on albumin are blocked by the chemical modification — while BCG and immunonephelometry are largely unaffected by this structural change [3, cohort]. A practical conversion was derived in a renal-disease population: AlbBCG ≈ AlbBCP + 5.5 (g/L), which performed with intraclass correlation 0.98 in both derivation and validation sets, though it cannot replace method harmonization [4, cohort].

**Clinical consequence.** Because albumin thresholds drive clinical decisions, method bias translates directly to patient misclassification. BCG falsely elevated albumin results in up to 59% of nephrotic syndrome patients misclassified relative to a BCP or immunoassay-based threshold, affecting decisions about anticoagulation and intravenous albumin therapy [5, cohort]. In CKD at all stages, BCG-based results led to structurally fewer patients being diagnosed with protein-energy wasting compared to BCP [6, cohort]. Albumin-based composite scores — the Child-Pugh score (hepatic function), the ALBI score (hepatocellular carcinoma prognosis), and nutritional indices — all carry albumin thresholds that assume a specific measurement method; applying BCG results to BCP-derived cutoffs (or vice versa) introduces systematic error [5, cohort]. Serial monitoring is equally vulnerable: comparing a BCG result from one visit with a BCP result from another conflates method drift with biological change. Method-specific reference intervals are not optional — they are a prerequisite for valid interpretation.

## Immunoassay Methods: The More Specific Reference Standard

Antibody-based methods — immunonephelometry (IN) and immunoturbidimetry (IT) — measure albumin by antigen–antibody binding and are substantially more analytically specific than dye-binding assays because the antibody distinguishes albumin from other serum proteins. Both IN and IT are used as comparator ("reference") methods in method-comparison studies [3, cohort; 7, mechanism_review]. They are more expensive and less amenable to very-high-throughput chemistry analyzers, so they remain second-line in most general laboratories despite their superiority.

**Standardization.** The certified reference material for serum proteins, including albumin, is **ERM-DA470k/IFCC**, issued by the EU Institute for Reference Materials and Measurements (IRMM) and characterized jointly with IFCC. IVD manufacturers establish their calibration hierarchy from ERM-DA470k/IFCC through secondary calibrators to commercial reagents, enabling traceability and reducing between-laboratory variation for immunoassay-based protein measurement [7, mechanism_review]. Dye-binding assays (BCG, BCP) are not traceable to ERM-DA470k/IFCC; standardization of these methods against a protein reference material remains incomplete, which is a root cause of the persistent inter-platform bias observed in external quality assessment schemes.

## Interferences

Several endogenous and exogenous substances affect albumin measurement by dye-binding methods:

- **Hemolysis:** Clinically significant bias for albumin occurs at moderate hemolysis, though the effect may remain within CLIA performance limits at lower hemolytic indices; visually clear specimens should be the standard [8, mechanism_review].
- **Lipemia:** Measured albumin falls with increasing lipemia; the interference threshold for albumin is lower than for many other analytes [8, mechanism_review].
- **Icterus (bilirubin):** Bilirubin interferes only at markedly elevated concentrations (icteric index <60 does not interfere on validated BCP platforms; at very high bilirubin levels interference can occur) [1, mechanism_review].
- **Drugs:** Salicylate does not interfere with BCP in contrast to some BCG platforms; therapeutic concentrations of common drug panels have no significant effect on validated BCP systems [1, mechanism_review].
- **Gammopathy:** Rarely, IgM paraproteins (Waldenström macroglobulinemia) may cause unreliable dye-binding results.

## Urine Albumin: A Distinct Measurement

Urine albumin (albuminuria) and serum albumin are different tests, different clinical questions, and must not be conflated. Urine albumin is measured by immunoassay — not by BCG or BCP — and is expressed as the **albumin-creatinine ratio (ACR)**, which corrects for urine concentration. ACR is the primary screening tool for kidney damage, stratifying CKD severity alongside estimated glomerular filtration rate (eGFR): ACR ≥3 mg/mmol (≥30 mg/g) signals albuminuria; ACR ≥30 mg/mmol (≥300 mg/g) marks macroalbuminuria (nephrotic-range proteinuria threshold) [10, regulatory]. The immunoassay standardization for urine albumin has its own history — including a secondary reference material of highly purified monomeric human serum albumin used to reduce inter-laboratory variation in urine immunoassays [7, mechanism_review]. None of this is connected to how serum albumin is measured by dye-binding methods on a chemistry analyzer. A clinician ordering a "serum albumin" and a "urine ACR" is ordering two completely different analytes by two completely different measurement principles for two completely different clinical questions.

## Pre-Analytic Factors

Albumin is a large, non-filterable plasma protein, so any process causing plasma water to shift affects its measured concentration:

- **Posture:** Changing from supine to standing causes approximately 8–10% hemoconcentration as protein-free plasma filtrates into the interstitium under hydrostatic pressure [9, mechanism_review]. This effect is essentially complete within 15–20 minutes of standing. Ambulatory outpatients (upright for >20 min before phlebotomy) will have systematically higher albumin than inpatients sampled supine. Standardized seated rest for a minimum of 15 minutes before collection is recommended to reduce this source of pre-analytic variation [1, mechanism_review].
- **Prolonged tourniquet / venous stasis:** Stasis acts as localized hemoconcentration: protein-free fluid filtrates distally, raising albumin (and other large-molecule) concentrations in the collected sample. Tourniquet application should be minimized and released as soon as the needle is in the vein.
- **Dehydration:** Systemic volume contraction raises all plasma protein concentrations, including albumin, without any change in total albumin mass.
- **Sample stability:** Separated serum or plasma is stable approximately 5 days at 4°C, approximately 4 months at −20°C, and longer at −70°C [1, mechanism_review]. Repeated freeze-thaw cycles should be avoided.

---

## Bibliography

1. Pinnell AE, Northam BE. New automated dye-binding method for serum albumin determination with bromcresol purple. *Clin Chem.* 1978;24(1):80–86. PMID: 618669. — tag: mechanism_review — tier: 1

2. Garcia Moreira V, Beridze Vaktangova N, Martinez Gago MD, Laborda Gonzalez B, Garcia Alonso S, Fernandez Rodriguez E. Overestimation of albumin measured by bromocresol green vs bromocresol purple method: influence of acute-phase globulins. *Lab Med.* 2018;49(4):355–361. PMID: 29790973. — tag: cohort — tier: 1

3. Kok MB, Tegelaers FP, van Dam B, van Rijn JL, van Pelt J. Carbamylation of albumin is a cause for discrepancies between albumin assays. *Clin Chim Acta.* 2014;434:6–10. PMID: 24709253. — tag: cohort — tier: 1

4. Clase CM, St Pierre MW, Churchill DN. Conversion between bromcresol green- and bromcresol purple-measured albumin in renal disease. *Nephrol Dial Transplant.* 2001;16(9):1925–1929. PMID: 11522881. — tag: cohort — tier: 1

5. van de Logt AE, Rijpma SR, Vink CH, Prudon-Rosmulder E, Wetzels JF, van Berkel M. The bias between different albumin assays may affect clinical decision-making. *Kidney Int.* 2019;95(6):1514–1517. PMID: 31053386. — tag: cohort — tier: 1

6. van Schrojenstein Lantman M, van de Logt AE, Prudon-Rosmulder E, et al. Albumin determined by bromocresol green leads to erroneous results in routine evaluation of patients with chronic kidney disease. *Clin Chem Lab Med.* 2023;61(12):2112–2121. DOI: 10.1515/cclm-2023-0463. — tag: cohort — tier: 1

7. Zegers I, Schreiber W, Sheldon J, et al. "Certification of Proteins in the Human Serum — Certified Reference Material ERM-DA470k/IFCC." European Commission, Joint Research Centre. JRC46604 (2008). ISBN 978-92-79-09490-3. URL: https://publications.jrc.ec.europa.eu/repository/handle/JRC46604 [Preparation and certification of ERM-DA470k/IFCC, the IFCC-designated certified reference material for 12 serum proteins including albumin; traceability anchor for immunoassay standardization.] — tag: mechanism_review — tier: 2

8. Koseoglu M, Hur A, Atay A, Cuhadar S. Effects of hemolysis interference on routine biochemistry parameters. *Biochemia Medica.* 2011;21(1):79–85. DOI: 10.11613/BM.2011.015. — tag: mechanism_review — tier: 1

9. Simundic AM, Lippi G. Preanalytical phase — a continuous challenge for laboratory professionals. *Biochemia Medica.* 2012;22(2):145–149. PMID: 22838180. DOI: 10.11613/BM.2012.017. [Reviews posture-related hemoconcentration: plasma volume reduces ~10% on standing, raising concentrations of albumin and other large plasma proteins; tourniquet stasis exacerbates local hemoconcentration; standardized seated rest minimizes both effects.] — tag: mechanism_review — tier: 1

10. Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2012 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease. *Kidney Int Suppl.* 2013;3(1):1–150. DOI: 10.1038/kisup.2012.73. kdigo.org. — tag: regulatory — tier: 2
