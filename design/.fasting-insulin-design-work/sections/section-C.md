# Section C: Measurement & Standardization

## C.1 Assay Non-Standardization: The Central Problem

Fasting insulin occupies an unusual position in clinical laboratory medicine: it is routinely ordered, widely interpreted, and yet its measurement remains among the least harmonized of all common analytes. Unlike glucose or HbA1c — both of which have well-established reference measurement procedures (RMPs) and enforced traceability chains — insulin immunoassays differ substantially from one another in calibration, antibody specificity, and reportable range, making numeric results from different platforms functionally non-interchangeable.

The American Diabetes Association convened a formal Insulin Standardization Workgroup to characterize the scope of this problem. In a landmark evaluation of 12 commercial insulin methods from 9 manufacturers — testing a panel of 39 single-donor serum specimens — the Workgroup found among-assay coefficients of variation (CVs) ranging from 12% to 66%, with a median inter-assay CV of 24% [1, cohort]. Within-assay imprecision was more acceptable (CV 3.7%–39.0%, with 7 of 10 assays ≤10.6%), but the cross-platform disagreement dwarfed analytical imprecision as the dominant source of measurement error [1, cohort]. Critically, supplying a common insulin reference preparation to recalibrate assays did not meaningfully reduce the inter-assay scatter, indicating that calibration alone cannot correct for fundamental antibody-specificity and matrix-interaction differences between platforms [1, cohort].

A subsequent study by Miller and colleagues (the Insulin Standardization Work Group, 2009) confirmed the degree of bias relative to a higher-order reference. Using isotope dilution-liquid chromatography/tandem mass spectrometry (ID-LC-MS/MS) calibrated against purified recombinant insulin as the comparator, 7 of 10 commercial assays showed bias exceeding 15.5% in 36%–100% of individual samples [2, cohort]. Calibration using a panel of native human sera was identified as the most effective strategy for reducing inter-method disagreement across the full measuring range [2, cohort].

## C.2 The IFCC Working Group and Reference Measurement Infrastructure

The IFCC Working Group on Standardization of Insulin Assays (WG-SIA) and the ADA-affiliated Insulin Standardization Work Group have jointly pursued a traceability architecture modeled on the ISO metrological hierarchy: a primary certified reference material (high-purity recombinant human insulin with assigned mass-unit values) → a trueness-based RMP → secondary calibrators for commercial use [3, regulatory]. Both groups developed ID-MS candidate RMPs and negotiated with the World Health Organization to obtain the required certified primary calibrators [3, regulatory]. As of the most recent status reports, harmonization of commercial immunoassays to the reference system remains incomplete: even after recalibration exercises, mean inter-method CVs decreased from approximately 22% to approximately 17% — an improvement, but still far above the ≤5% threshold considered acceptable for clinical interchangeability [3, regulatory].

A 2025 publication described a validated candidate RMP for human insulin in serum: immunoaffinity extraction followed by ID-LC-MS/MS, providing method-independent accuracy traceable to SI units [4, mechanism_review]. The JCTLM (Joint Committee for Traceability in Laboratory Medicine) database lists these LC-MS/MS procedures as the higher-order reference methods, though they remain research tools rather than routine clinical platforms [3, regulatory].

## C.3 Assay Methods: From RIA to Mass Spectrometry

**Radioimmunoassay (RIA).** RIA was the original clinical method, using a polyclonal anti-insulin antibody in a competitive displacement format. RIA antibodies are typically less specific than two-site immunometric antibodies and show greater cross-reactivity with proinsulin and its processing intermediates. Many reference-range values and early HOMA-IR derivations were established using RIA, making direct comparison with contemporary assays methodologically problematic.

**Two-site immunometric assays (ELISA, chemiluminescent immunoassay).** Modern platforms predominantly use sandwich immunometric designs — one capture antibody and one detection antibody binding distinct epitopes on the insulin molecule. Two-site formats generally confer higher specificity for intact insulin than RIA because recognition of both epitopes is required for signal generation. Chemiluminescent immunoassays (CLIAs) on automated platforms (e.g., Abbott ARCHITECT, Roche Elecsys, Beckman Coulter Access) are the dominant contemporary clinical format. Each platform is calibrated independently, contributing to the inter-assay scatter documented above.

**LC-MS/MS.** Isotope dilution LC-MS/MS represents the current reference-measurement standard. After immunoaffinity capture to enrich insulin from the complex serum matrix, the analyte is quantified by tandem mass spectrometry using a stable-isotope-labeled internal standard, providing absolute molar specificity without antibody cross-reactivity [4, mechanism_review]. This method defines what insulin "really is" in a reference material but is not currently deployed in clinical routine.

## C.4 Cross-Reactivity with Proinsulin and Split Products

Insulin biosynthesis passes through proinsulin, which is cleaved to mature insulin plus C-peptide, generating partially processed intermediates — split (32,33) proinsulin and des-(64,65) proinsulin — along the way. These precursors share structural epitopes with mature insulin and can cross-react with assay antibodies. The clinical relevance is highest in states of beta-cell stress (early type 2 diabetes, insulinoma), where disproportionate proinsulin secretion can inflate apparent insulin readings in non-specific assays.

The ADA Workgroup characterized specificity systematically across 10 methods [1, cohort]:

- **Intact proinsulin:** <2% cross-reactivity in 9 of 10 assays — acceptably low across nearly all platforms.
- **Split (32,33) proinsulin:** <3% cross-reactivity in 8 of 10 assays — similarly well-discriminated.
- **Des-(64,65) proinsulin:** exceeded 40% cross-reactivity in 9 of 10 assays — a striking and near-universal failure mode [1, cohort].

Des-(64,65) proinsulin, the product of cleavage at the B-chain/C-peptide junction (the "65-66" split), retains the C-terminal B-chain sequence that many antibodies use for insulin recognition, explaining the high and consistent cross-reactivity. In normal fasting physiology, des-(64,65) proinsulin concentrations are low enough that this artifact is minor. In subjects with beta-cell dysfunction or insulin resistance (precisely the population where fasting insulin testing is most clinically informative), elevated proinsulin intermediates can produce spuriously elevated apparent insulin values. The degree of inflation is assay-specific and unpredictable in magnitude.

## C.5 Pre-Analytical Requirements

**Hemolysis.** The single most clinically impactful pre-analytical hazard for insulin measurement is hemolysis. Erythrocytes contain insulin-degrading enzyme (IDE, also called insulysin), a zinc metallopeptidase that cleaves insulin at multiple sites [5, mechanism_review]. When red cells lyse — whether from difficult venipuncture, rough handling, delay in separation, or temperature excursion — IDE is released into the sample and degrades insulin at a rate proportional to hemolysis severity, lysate concentration, and time at ambient temperature. Even slight hemolysis (hemoglobin ~0.5 g/L) measurably lowers insulin, while massive hemolysis (hemoglobin ~6 g/L) can destroy >90% of insulin immunoreactivity within one hour at 37 °C [5, mechanism_review]. The effect is amplified in immunometric (two-site) assays relative to RIA, because degradation of either antibody-binding epitope on the insulin molecule eliminates sandwich-signal generation entirely, whereas competitive RIA may show partial rather than complete loss. Hemolysis renders a sample unreportable; no correction algorithm is reliable across assays.

**Prompt centrifugation and separation.** Because IDE activity is ongoing in whole blood, prompt centrifugation and plasma/serum separation are essential. EDTA-anticoagulated plasma tubes provide acceptable stability at room temperature for at least 24 hours when centrifuged and kept separated, making them suitable for resource-limited settings [6, cohort]. Serum yields comparable results to EDTA plasma when processed promptly. Samples should be stored at −20 °C or lower if analysis is delayed beyond several hours.

**Fasting state.** Insulin concentrations reflect the dynamic interplay of beta-cell secretion and hepatic clearance, with postprandial values rising several-fold above fasting values and returning toward baseline over 2–4 hours. A minimum 8-hour overnight fast is standard; shorter fasts introduce noise that overwhelms the signal at low fasting concentrations. Patient compliance with fasting should be confirmed at sample collection.

**Tube type.** Heparin plasma yields insulin values approximately 15% lower than serum due to heparin's interaction with insulin binding or assay antibodies; the Manley et al. Diabetes Care analysis documented this matrix effect across multiple assay platforms [7, cohort]. Serum or EDTA plasma are preferred; heparin plasma should be avoided or, if used, results should not be compared to serum-derived reference ranges.

## C.6 Variability: Analytical, Biological, and Inter-Assay

**Analytical CV.** Within-assay imprecision is acceptable for most modern automated platforms (typically 3%–10% CV at mid-range concentrations) but varies considerably at the low end of the fasting range, where most clinically interesting samples fall. At concentrations <5 µIU/mL, analytical CV often rises substantially, limiting the ability to distinguish fine gradations.

**Within-subject biological CV.** Fasting insulin exhibits high within-subject biological variation independent of assay choice. The European Biological Variation Study (EuBIVAS), the largest and most methodologically rigorous dataset of its kind, estimated within-subject biological CV (CVI) for serum insulin at 25.3% (95% CI 24.0%–26.6%) in healthy adults [8, cohort]. This figure, on its own, means that serial measurements in a single individual will differ by approximately 25% simply from day-to-day physiological fluctuation — before any analytical error is added. The reference change value (RCV) derived from this CVI implies that a serial change of ~71% or more is required to confidently attribute a difference to a true biological change rather than noise (at 95% probability, assuming comparable analytical CV ~5%).

**The cutpoint-transferability problem.** The compound effect of (a) inter-assay bias of up to 66% CV, (b) within-subject biological CV ~25%, and (c) non-specific cross-reactivity with des-(64,65) proinsulin means that a fasting insulin cutpoint established on one platform in one population cannot be applied to results from a different platform. Clinical decision thresholds for insulin resistance (e.g., >10 µIU/mL or >25 pmol/L) that appear in the literature were derived on specific assays — frequently RIA or early ELISA platforms — and are not automatically valid for contemporary chemiluminescent immunoassays. Laboratories should specify the assay platform used, and clinicians interpreting serial results should verify that platform and calibration have not changed between measurements.

---

## Bibliography

1. Marcovina S, Bowsher RR, Miller WG, Staten M, Myers G, Caudill SP, Campbell SE, Steffes MW; American Diabetes Association Workgroup on Insulin Assays. Standardization of insulin immunoassays: report of the American Diabetes Association Workgroup. *Clin Chem*. 2007;53(4):711–716. doi:10.1373/clinchem.2006.082214 [cohort]

2. Miller WG, Thienpont LM, Van Uytfanghe K, Clark PM, Lindstedt P, Nilsson G, Steffes MW; Insulin Standardization Work Group. Toward standardization of insulin immunoassays. *Clin Chem*. 2009;55(5):1011–1018. doi:10.1373/clinchem.2008.118380 [cohort]

3. Thienpont LM, Van Uytfanghe K, Stöckl D, De Leenheer AP. Standardization of insulin and C-peptide — a status report. *Clin Chim Acta*. 2010;411(17–18):1265–1271. doi:10.1016/j.cca.2010.05.013 [regulatory]

4. Stoyanov A, et al. A candidate reference measurement procedure for quantification of human insulin in serum based on immunoaffinity extraction and isotope dilution-liquid chromatography-tandem mass spectrometry. *Anal Bioanal Chem*. 2025. doi:10.1007/s00216-025-05900-5 [mechanism_review]

5. Nakagawa Y, et al. Effect of hemolysis on the concentration of insulin in serum determined by RIA and IRMA. *Clin Chem*. 1998;44(2):354–357. [mechanism_review]

6. Shields BM, McDonald TJ, Vaidya B, et al. EDTA tubes are suitable for insulin and C-peptide measurement in resource-limited settings and can be stored at room temperature for up to 24 hours. *Clin Chem Lab Med*. 2024. PMC12208407. [cohort]

7. Manley SE, Luzio SD, Stratton IM, Wallace TM, Clark PMS. Preanalytical, analytical, and computational factors affect homeostasis model assessment estimates. *Diabetes Care*. 2008;31(9):1877–1883. doi:10.2337/dc07-2054 [cohort]

8. Carobene A, Aarsand AK, Bartlett WA, et al. Biological variation of serum insulin: updated estimates from the European Biological Variation Study (EuBIVAS) and meta-analysis. *Clin Chem Lab Med*. 2021;59(9):1518–1527. doi:10.1515/cclm-2020-1490 [cohort]
