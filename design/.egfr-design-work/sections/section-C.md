# Section C: Measurement & Standardization

## C.1 Serum Creatinine Assays

Two assay platforms dominate clinical creatinine measurement: the legacy Jaffe (alkaline picrate) method and the newer enzymatic method. Each carries a distinct interference profile that clinicians and laboratorians must understand.

### C.1.1 The Jaffe Method

Max Jaffe first described in 1886 that creatinine reacts with picric acid in an alkaline medium to produce a red chromogen. Otto Folin adapted this principle into the clinical colorimetric assay still in widespread use today — largely because of its low cost and high throughput [1, mechanism_review]. The fundamental problem is selectivity: the alkaline picrate reaction is not exclusive to creatinine. A broad class of **non-creatinine chromogens** react similarly, producing falsely elevated readings. Documented interferents include glucose (positive at high concentrations), acetone and ketone bodies (positive), alpha-keto acids, and certain cephalosporin antibiotics. Protein — particularly albumin and immunoglobulins — also contributes a measurable pseudo-creatinine signal, and fetal hemoglobin (Hb F) causes substantial interference in neonatal samples [2, mechanism_review].

Bilirubin, paradoxically, creates **negative** interference in some Jaffe formulations, partly offsetting the positive chromogen contributions. The net direction and magnitude of interference is therefore platform-dependent, which partly explains why no two "Jaffe methods" behave identically across manufacturers. Within-laboratory interferent-related coefficients of variation for Jaffe method-analyzer combinations have been measured at 8.0–27% at low creatinine concentrations (~40 µmol/L), versus under 4% for enzymatic approaches at the same concentration [2, mechanism_review].

### C.1.2 The Enzymatic Method

Enzymatic assays convert creatinine stepwise via creatininase, creatinase, and sarcosine oxidase (or coupled peroxidase reactions), generating a signal proportional only to creatinine rather than to any chromogenic substance in the matrix. This mechanistic specificity dramatically reduces susceptibility to the interferences that plague Jaffe chemistry. Bilirubin, glucose, and ketones no longer significantly perturb results; albumin and IgG interference is eliminated [2, mechanism_review]. Hemolysis does produce a modest negative interference in some enzymatic platforms — an interference not seen with Jaffe — but its magnitude is smaller than the Jaffe chromogen burden at low creatinine concentrations [3, mechanism_review].

The clinical consequence of greater specificity is most pronounced at **low-normal creatinine concentrations** (roughly < 80 µmol/L), precisely where eGFR is highest and where inaccurate creatinine input most distorts the GFR estimate. Studies comparing paired samples show ~20% of results differ by ≥10% between Jaffe and enzymatic methods, and divergence preferentially clusters at lower creatinine values — which maps exactly onto the CKD staging boundary between no CKD and early CKD [3, mechanism_review]. Enzymatic methods are therefore the preferred platform, particularly for pediatric populations where creatinine is inherently low and Hb F interference is a genuine risk [2, mechanism_review].

---

## C.2 IDMS-Traceable Standardization: The Load-Bearing Requirement

The single most consequential analytical development in creatinine measurement over the past two decades is **isotope-dilution mass spectrometry (IDMS) traceability** — and its direct coupling to the validity of modern eGFR equations.

### C.2.1 Why Standardization Matters

The CKD-EPI and MDRD equations are empirically derived regression models: their coefficients were fit against study populations whose creatinine was measured with IDMS-traceable methods. This is not a minor calibration footnote — it is load-bearing. A laboratory reporting creatinine values systematically higher or lower than the IDMS reference scale will generate eGFR values that are systematically wrong, not merely noisy. Evidence from matched cohort studies confirms this directly: subjects with identical ages, sexes, BMIs, and measured GFRs show materially different serum creatinine concentrations (females: ~1.13 vs. 0.83 mg/dL in non-standardized vs. standardized cohorts) when creatinine assay calibration differs, and this calibration gap causes the same eGFR equation to produce discordant staging outcomes in the two settings [4, cohort].

### C.2.2 The NKDEP / IFCC Standardization Program

In 2006, the Laboratory Working Group of the **National Kidney Disease Education Program (NKDEP)** — acting in collaboration with the International Federation of Clinical Chemistry and Laboratory Medicine (IFCC) and the European Communities Confederation of Clinical Chemistry — formally recommended that all clinical laboratories calibrate their serum creatinine procedures to be traceable to an IDMS reference measurement procedure [5, regulatory]. The anchoring reference material is **NIST SRM 967 (Creatinine in Frozen Human Serum)**, which was validated for commutability with native serum across a wide range of routine creatinine platforms and established the metrological chain from working reagents up to the primary SI-linked IDMS procedure.

IVD manufacturers responded: by approximately 2013, virtually all global manufacturers had transitioned their creatinine measurement procedures to IDMS traceability [5, regulatory]. This means that in properly accredited clinical laboratories today, the creatinine value reported is expressed on the same measurement scale used to derive CKD-EPI and MDRD — a prerequisite for those equations to produce valid eGFR results. Laboratories still using legacy non-standardized calibrators, or applying equations to point-of-care creatinine measurements that have not been verified for IDMS alignment, operate outside the intended use conditions of the equations.

---

## C.3 Cystatin C: Muscle-Independent Filtration Marker

Cystatin C is a 13-kDa cysteine protease inhibitor produced by all nucleated cells at a near-constant rate. Unlike creatinine, its production is not strongly influenced by muscle mass, protein intake, or cooked-meat consumption. It is freely filtered at the glomerulus, reabsorbed and catabolized in the proximal tubule (not returned to plasma), and not secreted — making its serum concentration a cleaner index of filtration rate in populations where creatinine is confounded by non-GFR determinants.

### C.3.1 Immunoassay Platforms

Clinical cystatin C is measured by **particle-enhanced turbidimetric immunoassay (PETIA)** or **particle-enhanced nephelometric immunoassay (PENIA)** — both formats use antibody-coated particles that aggregate in proportion to analyte concentration, detected by light-scatter or light-absorbance changes respectively [6, mechanism_review]. Prior to international standardization, proficiency-testing surveys documented close to a **twofold variation** in cystatin C results for the same sample across measurement procedures, a spread that made cross-platform or cross-institution eGFR comparisons unreliable [6, mechanism_review].

### C.3.2 ERM-DA471/IFCC Reference Material

The IFCC Working Group on Cystatin C released the **ERM-DA471/IFCC** international certified reference material in June 2010, with a certified cystatin C mass concentration of 5.48 mg/L (expanded uncertainty k=2: ±0.15 mg/L) [7, regulatory]. Characterization was performed by particle-enhanced immuno-nephelometry, particle-enhanced immuno-turbidimetry, and enzyme-amplified single radial immunodiffusion — multiple orthogonal methods to anchor the assigned value. All PETIA and PENIA assays for cystatin C are now expected to be calibrated against this reference material.

Standardization to ERM-DA471/IFCC is specifically required for valid use of the **CKD-EPI cystatin C** and **CKD-EPI creatinine–cystatin C combined** equations, which were derived in populations where cystatin C was measured with ERM-DA471/IFCC-traceable methods [6, mechanism_review]. As with creatinine, a non-traceable cystatin C input produces a systematically biased eGFR output.

---

## C.4 Non-GFR Determinants: Confounders of the Creatinine Input

Even perfectly standardized, interference-free creatinine measurement can produce misleading eGFR values when non-GFR factors shift the creatinine set-point without changing actual filtration. The most clinically significant category is pharmacological blockade of tubular creatinine secretion.

### C.4.1 Drugs That Block Tubular Secretion

Creatinine is not purely filtered; a meaningful fraction (~10–40% of urinary creatinine at normal GFR) reaches the tubular lumen via active secretion through multiple transporters. Basolateral uptake into proximal tubule cells involves **OAT2 (SLC22A7)**, **OCT2 (SLC22A2)**, and **OCT3 (SLC22A3)**; apical efflux into the tubular lumen is mediated by **MATE1 (SLC47A1)** and **MATE2-K (SLC47A2)**. The relative contribution of these transporters is not settled: Lepist et al. (2014) found that OAT2 had the highest in-vitro creatinine transport activity at physiological concentrations — over twofold higher than OCT2 or OCT3 — revising the older OCT2-centric view, while OCT2 remains the clinically cited basolateral transporter and the locus of inhibition by cimetidine, trimethoprim, and cobicistat [8, mechanism_review]. Several drugs potently inhibit one or more of these transporters:

- **Cimetidine** — inhibits creatinine transporters broadly; at high doses can nearly abolish tubular secretion, making creatinine clearance approximate true GFR
- **Trimethoprim** — potently inhibits MATE2-K and OCT2; the antibiotic's effect on serum creatinine is well-documented and clinically relevant given its common use
- **Cobicistat** — preferentially inhibits MATE1 (IC₅₀ ~0.99 µmol/L), with MATE1 inhibition identified as the primary driver of serum creatinine elevation; OAT2 and OCT2 also contribute to cobicistat's tubular handling [8, mechanism_review]
- **Dolutegravir** — preferentially inhibits OCT2
- **Others** — ritonavir, fenofibrate, certain proton-pump inhibitors, and tyrosine kinase inhibitors have been identified in transporter inhibition studies

The result: **serum creatinine rises, eGFR falls, but true GFR is unchanged** [8, mechanism_review]. This is a pharmacologically induced pseudo-elevation of creatinine, not nephrotoxicity. The clinical pitfall is significant — a patient starting trimethoprim-sulfamethoxazole for a urinary tract infection may show an apparent eGFR drop of 10–15 mL/min/1.73 m² that triggers unnecessary concern about drug-induced kidney injury when the kidneys are filtering normally.

### C.4.2 Other Non-GFR Determinants

Beyond drugs, **muscle mass** is the dominant physiologic variable: higher lean body mass generates more creatinine regardless of GFR. Cooked-meat ingestion transiently raises creatinine because cooking converts muscle creatine to creatinine that is absorbed intestinally. These factors mean that creatinine-based eGFR systematically overestimates GFR in individuals with markedly high muscle mass (elite athletes, bodybuilders) and underestimates it in those with very low muscle mass (sarcopenia, cachexia, amputees).

---

## C.5 When to Prefer Measured GFR or Cystatin-C-Based eGFR

Creatinine-based eGFR is appropriate for the vast majority of clinical encounters. However, in defined situations, the creatinine input is sufficiently confounded that measured GFR or cystatin-C-based eGFR is the more reliable approach [9, mechanism_review]:

| Situation | Preferred approach | Rationale |
|---|---|---|
| Extremes of muscle mass (amputees, bodybuilders, severe sarcopenia) | Cystatin C eGFR or measured GFR | Creatinine set-point divorced from filtration |
| Cirrhosis / hepatic failure | Cystatin C eGFR or measured GFR | Reduced creatinine synthesis + volume expansion |
| Pre-nephrotoxic chemotherapy dosing (e.g., cisplatin, aminoglycosides) | Iohexol/iothalamate clearance | Narrow therapeutic window requires exact GFR |
| Living kidney donor evaluation | Iohexol/iothalamate clearance | Regulatory/ethical requirement for precision |
| Renal transplant recipients | Cystatin C eGFR or measured GFR | Immunosuppressant interference with muscle mass assumptions |
| Suspected hyperfiltration (early diabetic nephropathy) | Measured GFR | eGFR equations perform poorly above ~120 mL/min/1.73 m² |
| Drugs blocking tubular secretion in use | Cystatin C eGFR | Creatinine elevated by drug, not GFR change |

**Iohexol plasma clearance** has emerged as the practical measured-GFR reference for outpatient and research settings: it involves a single intravenous injection followed by timed blood sampling, requires no urine collection, and is not radioactive [9, mechanism_review]. Inulin and iothalamate clearances remain reference standards in research; radiolabeled tracers (⁵¹Cr-EDTA, ⁹⁹ᵐTc-DTPA) are alternatives where nuclear medicine infrastructure exists.

---

## Bibliography

1. Delanghe JR, Speeckaert MM. Creatinine determination according to Jaffe — what does it stand for? *Clin Kidney J*. 2011;4(2):83–86. https://doi.org/10.1093/ndtplus/sfq211 — tag: mechanism_review — tier: 1

2. Cobbaert CM, Baadenhuijsen H, Weykamp CW. Prime time for enzymatic creatinine methods in pediatrics. *Clin Chem*. 2009;55(3):549–558. https://doi.org/10.1373/clinchem.2008.116863 — tag: mechanism_review — tier: 1

3. Syme NR, Stevens K, Stirling C, McMillan DC, Talwar D. Clinical and analytical impact of moving from Jaffe to enzymatic serum creatinine methodology. *J Appl Lab Med*. 2020;5(4):631–642. https://doi.org/10.1093/jalm/jfaa053 — tag: mechanism_review — tier: 1

4. Pottel H, Cavalier E, Björk J, et al. Standardization of serum creatinine is essential for accurate use of unbiased estimated GFR equations: evidence from three cohorts matched on renal function. *Clin Kidney J*. 2022;15(12):2258–2265. https://doi.org/10.1093/ckj/sfac182 — tag: cohort — tier: 1

5. National Kidney Disease Education Program (NKDEP) / NIDDK Laboratory Working Group. Creatinine Standardization Program. Bethesda, MD: National Institute of Diabetes and Digestive and Kidney Diseases; 2006 (recommendations); updated 2013 (full IVD manufacturer adoption). https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/creatinine-standardization-program — tag: regulatory — tier: 2

6. Voskoboev NV, Larson TS, Rule AD, Lieske JC. Importance of cystatin C assay standardization. *Clin Chem*. 2011;57(8):1209–1211. https://doi.org/10.1373/clinchem.2011.164798 — tag: mechanism_review — tier: 1

7. Blirup-Jensen S, Grubb A, Lindström V, Schmidt C, Althaus H. First certified reference material for cystatin C in human serum ERM-DA471/IFCC. *Clin Chem Lab Med*. 2010;48(11):1619–1621. https://doi.org/10.1515/CCLM.2010.318 — tag: regulatory — tier: 2

8. Lepist EI, Zhang X, Hao J, et al. Contribution of the organic anion transporter OAT2 to the renal active tubular secretion of creatinine and mechanism for serum creatinine elevations caused by cobicistat. *Kidney Int*. 2014;86(2):350–357. https://doi.org/10.1038/ki.2014.66 — tag: mechanism_review — tier: 1

9. Delanaye P, Melsom T, Ebert N, et al. Iohexol plasma clearance for measuring glomerular filtration rate in clinical practice and research: a review. Part 2: Why to measure glomerular filtration rate with iohexol? *Clin Kidney J*. 2016;9(5):700–704. https://doi.org/10.1093/ckj/sfw071 — tag: mechanism_review — tier: 1
