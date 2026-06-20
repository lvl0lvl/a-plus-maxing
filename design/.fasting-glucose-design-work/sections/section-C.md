# Section C: Measurement & Pre-analytics — Fasting Plasma Glucose (FPG)

## C.1 Assay Methods and Reference Standardization

The enzymatic hexokinase/glucose-6-phosphate dehydrogenase (HK/G6PD) method is the accepted reference method for plasma glucose measurement. In this two-step reaction, hexokinase catalyzes the phosphorylation of glucose to glucose-6-phosphate (G6P) by ATP; G6P is then oxidized by glucose-6-phosphate dehydrogenase in the presence of NADP⁺, generating NADPH. The resulting increase in NADPH absorbance at 340 nm is directly proportional to glucose concentration [1, mechanism_review]. Because it measures glucose stoichiometrically, is highly specific, and is traceable to the isotope-dilution mass spectrometry (ID-MS) primary reference, the HK method serves as the calibration anchor for all clinical glucose assays [1, mechanism_review].

Glucose oxidase (GOD) methods are also widely used. GOD catalyzes the oxidation of β-D-glucose to gluconic acid and hydrogen peroxide; the H₂O₂ is then detected colorimetrically (Trinder reaction) or amperometrically. GOD methods are inherently selective for glucose but can be subject to oxygen tension interference and peroxidase inhibitors. Many point-of-care (POC) meters exploit glucose oxidase or glucose dehydrogenase (GDH) electrochemistry [2, mechanism_review].

**Reference matrix:** Venous plasma is the reference specimen for FPG. Plasma glucose values are approximately 10–15% higher than whole-blood values because plasma excludes the glucose-poor red cell volume. Serum glucose is analytically acceptable but subject to a brief post-clot glycolytic window before gel barrier separation; it is not the preferred matrix for diagnostic testing [3, mechanism_review].

**Standardization:** Clinical glucose methods are calibrated against reference materials traceable to GC-IDMS (gas chromatography–isotope dilution mass spectrometry), the SI-anchored primary standard. The IFCC/JCTLM framework and the NGSP (for HbA1c) provide the traceability hierarchy; the ADA 2011 and 2024 laboratory guidelines require that FPG methods be traceable to this reference system [4, regulatory].

## C.2 Fasting Requirement — Definition

"Fasting" for FPG is defined as no caloric intake for at least 8 hours before the draw (water is permitted) [5, regulatory]. The ADA specifies this threshold explicitly in its diagnostic criteria: an FPG ≥126 mg/dL (7.0 mmol/L) under these conditions meets the glycemic criterion for diabetes; 100–125 mg/dL (5.6–6.9 mmol/L) defines impaired fasting glucose (IFG) / prediabetes. The 8-hour cutoff is a practical standard, not a physiological optimum — overnight fasts of 10–14 hours are common in clinical practice and produce equivalent results in most subjects.

## C.3 In-Tube Glycolysis — The Load-Bearing Pre-analytic Hazard

This is the dominant source of systematic pre-analytic error for FPG and the mechanism most likely to produce clinically significant underestimation.

**Rate of ex vivo glycolysis.** Erythrocytes and leukocytes in unprocessed whole blood continue consuming glucose at approximately 5–7% per hour (≈0.6 mmol/L/hr, ≈10 mg/dL/hr) at room temperature [6, cohort]. Because this decay is linear across the clinical range, a sample left unprocessed for 2 hours before centrifugation loses ~10–14% of its glucose — enough to shift a patient from the diabetic range (≥126 mg/dL / 7.0 mmol/L) into the IFG range or from IFG into normal.

**Why sodium fluoride/oxalate tubes fail in the first 1–4 hours.** Sodium fluoride (NaF) inhibits glycolysis by binding to enolase — a late-acting enzyme in the glycolytic pathway. Enzymes upstream of enolase (hexokinase, phosphofructokinase) remain active for 90–120 minutes after collection, continuing to metabolize glucose until fluoride concentrations equilibrate and pH falls sufficiently to inhibit early enzymes [7, mechanism_review; 8, cohort]. In NaF/potassium oxalate tubes at room temperature, Gambino et al. measured a mean glucose decrease of 4.6% at 2 hours and 7.0% at 24 hours — compared with only 0.3% at 2 hours in citrate-buffered tubes [8, cohort]. The 2011 ADA/AACC laboratory guidelines accordingly concluded that NaF alone is not sufficient for accurate glucose preservation [4, regulatory].

**Citrate-buffered tubes as the solution.** Low-pH additive mixtures — combining citric acid, trisodium citrate, EDTA, and NaF (exemplified by the Greiner Bio-One Vacuette FC-Mix / "GlucoEXACT" tube and the Terumo Venosafe Glycaemia tube) — inhibit hexokinase and phosphofructokinase immediately by acidifying the sample to ≈pH 5, blocking early glycolytic enzymes [8, cohort]. In stabilization studies, citrate-buffered tubes held glucose within 1–2% of baseline for up to 48 hours at room temperature [9, cohort]. Equivalent performance was confirmed when the Greiner FC-Mix tube was directly compared with earlier Terumo formulations [9, cohort].

**Clinical consequence — diagnostic misclassification.** Using current WHO/ADA decision limits (diabetes threshold: 7.0 mmol/L / 126 mg/dL; IFG threshold: 5.6 mmol/L / 100 mg/dL), a simulation across 157,415 consecutive glucose requests estimated that switching from standard NaF/heparin tubes to FC-Mix tubes increased the frequency of patients classified as having impaired fasting glucose by ~48–56% [6, cohort]. The corollary is that routine NaF-tube results systematically underestimate true in-vivo glucose, meaning that the diagnostic thresholds (established on NaF-tube samples) partially compensate for this bias — a caution that must be respected when switching tube types or comparing laboratories.

**If citrate tubes are unavailable.** The NACB/WHO fallback is to place tubes immediately in an ice-water slurry and separate plasma within 30 minutes of collection. Centrifuged plasma (regardless of tube type) is stable at room temperature for several hours and at 4°C overnight [3, mechanism_review].

## C.4 Plasma vs Serum vs Capillary vs POC Meters

| Matrix / Method | Notes |
|---|---|
| Venous plasma (NaF or citrate-buffered) | Reference matrix; used for all diagnostic decisions |
| Serum (SST/gel tube) | ~10–15% lower than plasma in unprocessed samples; acceptable if centrifuged promptly; not preferred for diagnosis |
| Capillary whole blood (finger-stick) | ~0–15% higher than venous plasma in the fasting state; varies with hematocrit and perfusion |
| POC glucose meters (ISO 15197:2013) | ≥95% of results must fall within ±15 mg/dL (±0.83 mmol/L) of laboratory reference for glucose <100 mg/dL (5.55 mmol/L), and within ±15% for ≥100 mg/dL; 99% of results must fall in Consensus Error Grid zones A+B [11, regulatory] |

POC meters measure capillary or venous whole blood, not plasma, and are calibrated to report plasma-equivalent values; however, the ±15% allowable error at the diabetes diagnostic threshold (126 mg/dL / 7.0 mmol/L) spans a 36 mg/dL (2.0 mmol/L) range — straddling the IFG/diabetes cut point — making them unsuitable for diagnostic classification. They are appropriate for monitoring but not for establishing a new diagnosis [11, regulatory].

## C.5 Analytical and Biological Variability — Reference-Change Value Implications

**Analytical (within-laboratory) variability.** Well-run clinical hexokinase methods achieve a coefficient of analytical variation (CV_A) of 1.5–2.5% for fasting glucose [4, regulatory; 12, cohort]. External quality assurance programs report between-laboratory bias of −6% to +7% for plasma glucose, a significant source of inter-site variation.

**Within-subject biological variability (CV_I).** The EFLM Biological Variation Database (meta-analysis of healthy adult serum/plasma glucose) places the within-subject CV_I at approximately 4.7% (median; 95% CI 3.0–5.4%) [12, meta_analysis]. Older Ricos database entries ranged 4.2–6.5% across study populations. For glucose specifically, CV_I is often close to or slightly greater than between-subject CV_G (~5.4–8.8%), yielding an individuality index near 1.0 — meaning population-based reference intervals and serial patient comparisons contribute roughly equally to interpretation.

**Reference change value (RCV).** Using CV_A = 2.5%, CV_I = 5%, and a two-tailed 95% significance threshold (Z = 1.96):

RCV = √2 × 1.96 × √(CV_A² + CV_I²) = √2 × 1.96 × √(6.25 + 25) ≈ ±24%

In practical terms, a fasting glucose of 100 mg/dL (5.56 mmol/L) can vary on serial testing by ±24 mg/dL (±1.3 mmol/L) due to random biological and analytical noise alone. This magnitude exceeds the 26 mg/dL (1.4 mmol/L) span between the normal upper limit and the IFG threshold — confirming that a single FPG measurement cannot reliably classify borderline individuals and that repeat testing (as mandated by ADA guidelines) is mandatory before diagnosis [5, regulatory].

## C.6 FPG vs HbA1c vs OGTT — Concordance and Discordance

Each test captures a distinct physiological window:

- **FPG** primarily reflects hepatic glucose output in the basal state; it is sensitive to acute-day variability and is influenced by the duration of fasting.
- **HbA1c** integrates average plasma glucose over the preceding ~8–12 weeks (weighted toward recent weeks due to red cell turnover); it is insensitive to acute glycemic events but affected by hemoglobin variants, hemolytic conditions, and erythrocyte lifespan (which varies by ethnicity and age).
- **OGTT 2-hour glucose** captures postprandial glucose disposal, primarily reflecting peripheral (muscle) insulin sensitivity; it detects early postprandial hyperglycemia invisible to FPG.

**Degree of discordance.** In a NHANES-based study of 7,412 U.S. adults, among those classified as diabetic by OGTT, concordance with HbA1c was only 34% and with FPG was only 44% [13, cohort]. For prediabetes, agreement was similarly poor across all three test combinations. An independent Vietnamese cohort found that among subjects classified as diabetic by HbA1c ≥6.5%, only 59% also met the FPG ≥126 mg/dL criterion; conversely, among normal-HbA1c subjects, 95% were also FPG-normal [14, cohort]. The practical implication is substantial: relying on any single test alone leads to meaningful missed diagnoses and false positives, particularly in populations with ethnic-specific HbA1c offsets.

The ADA 2024 Standards of Care acknowledge this discordance explicitly, stipulating that when two different tests are obtained simultaneously and both exceed their respective thresholds, diabetes is confirmed; when results are discordant, the above-threshold test should be repeated for confirmation [5, regulatory].

---

## Bibliography

[1]. NHANES Fasting Plasma Glucose Laboratory Procedure Manual (2015–2016). CDC/NCHS. Method: hexokinase (HK/G6PD) reference method; traceability to ID/MS. URL: https://wwwn.cdc.gov/nchs/data/nhanes/public/2015/labmethods/GLU_I_MET_C311.pdf — tag: mechanism_review — tier: 2

[2]. Heng SY, Adnan A, Nadia OS, et al. Benchmarking Point-of-Care Glucometers: A Comparative Study Using the Hexokinase Test and International Organization for Standardization (ISO) Standards. PMC11539051. Cureus. 2024. PMID: PMC11539051 — tag: cohort — tier: 1

[3]. Nikolac N. The impact of preanalytical factors on glucose concentration measurement. Biochemia Medica. 2014;24(1):5–8. URL: https://www.biochemia-medica.com/assets/images/upload/Clanci/24/N.Nikolac-_The_imapct_of_preanalytical_factors_on_glucose_concetration_measurement.pdf — tag: mechanism_review — tier: 1

[4]. Sacks DB, Arnold M, Bakris GL, Bruns DE, Horvath AR, Kirkman MS, et al. Guidelines and recommendations for laboratory analysis in the diagnosis and management of diabetes mellitus. Clin Chem. 2011;57(6):e1–e47. DOI: 10.1373/clinchem.2010.161596 — tag: regulatory — tier: 2

[5]. American Diabetes Association Professional Practice Committee. 2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2024. Diabetes Care. 2024;47(Suppl 1):S20–S42. PMC: PMC9810477 — tag: regulatory — tier: 2

[6]. Bowen RAR, Hortin GL, Csako G, et al. Effects of different tube types on patient classification using current diabetes decision limits. Clin Biochem. 2019;74:45–52. PMCID: PMC6804563. DOI: 10.1016/j.clinbiochem.2019.09.011 — tag: cohort — tier: 1

[7]. Mikesh LM, Bruns DE. Stabilization of glucose in blood specimens: mechanism of delay in fluoride inhibition of glycolysis. Clin Chem. 2008;54(5):930–932. DOI: 10.1373/clinchem.2007.102160 — tag: mechanism_review — tier: 1

[8]. Gambino R, Piscitelli J, Ackattupathil TA, Theriault JL, Andrin RD, Sanfilippo ML, Etienne M. Acidification of blood is superior to sodium fluoride alone as an inhibitor of glycolysis. Clin Chem. 2009;55(5):1019–1021. PMID: 19282354. DOI: 10.1373/clinchem.2008.121707 — tag: cohort — tier: 1

[9]. Cadamuro J, von Meyer A, Wiedemann H, et al. The new Greiner FC-Mix tubes equal the old Terumo ones and are better than standard NaF. Clin Chem Lab Med. 2017;55(10):e239–e242. PMCID: PMC5628000. DOI: 10.1515/cclm-2017-0059 — tag: cohort — tier: 1

[10]. Bruns DE, Knowler WC. Stabilization of glucose in blood samples: why it matters. Clin Chem. 2009;55(5):850–852. PMCID: PMC3556871 (cited in). DOI: 10.1373/clinchem.2009.126037 — tag: mechanism_review — tier: 1

[11]. International Organization for Standardization. ISO 15197:2013. In vitro diagnostic test systems — Requirements for blood-glucose monitoring systems for self-testing in managing diabetes mellitus. Geneva: ISO; 2013. URL: https://www.iso.org/standard/54976.html — tag: regulatory — tier: 2

[12]. EFLM Biological Variation Database — Glucose (meta-analysis, serum/plasma). Updated 2026. URL: https://biologicalvariation.eu/api/search/by_id?query=1518. Also: Aarsand AK et al. The biological variation data critical appraisal checklist. Clin Chem. 2018;64:501–514. DOI: 10.1373/clinchem.2017.281808 — tag: meta_analysis — tier: 1

[13]. Zheng Y, Ma H, Wang M, et al. Limited Agreement between Classifications of Diabetes and Prediabetes Resulting from the OGTT, Hemoglobin A1c, and Fasting Glucose Tests in 7412 U.S. Adults. J Clin Med. 2020;9(7):2207. PMID: 32668564. DOI: 10.3390/jcm9072207 — tag: cohort — tier: 1

[14]. Ho-Pham LT, Nguyen UDT, Tran TX, Nguyen TV. Discordance in the diagnosis of diabetes: Comparison between HbA1c and fasting plasma glucose. PLoS ONE. 2017;12(8):e0182192. DOI: 10.1371/journal.pone.0182192 — tag: cohort — tier: 1
