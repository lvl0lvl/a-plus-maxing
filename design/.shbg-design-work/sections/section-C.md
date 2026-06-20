# Section C: Measurement & Standardization

## C.1 Assay Platforms

Sex hormone-binding globulin (SHBG) is measured in clinical laboratories primarily by **immunometric (sandwich/two-site) immunoassays**, most commonly using chemiluminescent detection on automated platforms [1, mechanism_review]. The two-site (sandwich) format uses two antibodies that recognize distinct epitopes on the SHBG molecule: a capture antibody immobilized on a solid phase and a labeled detection antibody, with signal proportional to the amount of SHBG present. Enzyme-linked immunosorbent assay (ELISA) formats are also available, and historically SHBG was measured by **ligand-binding/steroid-saturation assays**, which determined binding capacity by incubating serum with a radiolabeled steroid (typically tritiated dihydrotestosterone) followed by charcoal separation — these older assays measured binding sites rather than immunoreactive protein mass, and results are not interchangeable with immunoassay values [2, mechanism_review].

Contemporary automated SHBG immunoassay analyzers in wide clinical use include platforms from Roche (Elecsys/Cobas), Abbott (Alinity/Architect), and Siemens (Immulite/Atellica). These platforms use electrochemiluminescent or chemiluminescent detection and operate with analytical measuring ranges typically spanning 0.1–250 nmol/L. At the three major platforms, mean SHBG values in a mixed-sex cohort were 47.1, 45.9, and 44.6 nmol/L respectively (Abbott, Roche, Siemens), with statistically significant inter-platform differences (p < 0.001) and proportional differences of approximately +3.3%, ~0%, and −2.3% relative to the group mean [3, cohort].

## C.2 Calibration and the Standardization Gap (Load-Bearing)

Unlike total testosterone — which has the CDC Hormone Standardization (HoSt) accuracy-based certification program, tracing assay calibration to a definitive reference method and requiring laboratories to demonstrate ≤6.4% bias — **SHBG has no equivalent widely-adopted reference-method standardization program** [1, mechanism_review]. This is a meaningful analytical gap. The field relies instead on calibration traceable to WHO/NIBSC International Standards: the 1st IS (NIBSC 95/560) established in 1998, now superseded by the **2nd International Standard for SHBG (NIBSC 08/266)**, which has two-fold higher steroid-binding capacity than its predecessor and improved thermal stability [4, mechanism_review]. Multiple commercial platforms calibrate against this material, and three-assay correlations anchored to the same IS (NIBSC 95/560) showed slopes of 0.926–1.05 with R² = 0.948–0.985 across paired comparisons. However, calibration against the same IS does not guarantee result commutability across platforms: the IS is a pooled freeze-dried serum from healthy female volunteers, and differences in antibody epitope recognition, matrix effects, and assay geometry mean that inter-method bias on patient samples can diverge from IS-based comparison.

An emerging mass spectrometric method for SHBG — antibody-free LC-MS/MS targeting a surrogate peptide after tryptic digestion — has been described as a candidate higher-order reference method. Unlike immunoassays, LC-MS/MS is immune to antibody cross-reactivity and provides SI-traceable quantification; however, it is not yet routinely deployed in clinical practice or used as the anchor for a harmonization program analogous to CDC HoSt-testosterone [5, mechanism_review].

**Why this matters:** SHBG is an input variable to calculated free testosterone (cFT) using the Vermeulen formula and its variants, and to the free androgen index (FAI = total testosterone / SHBG × 100). Because cFT is derived algebraically from total testosterone and SHBG concentrations — and because the sensitivity of cFT to SHBG is non-linear — SHBG assay bias propagates directly into cFT [6, mechanism_review]. Goldman et al. (Endocrine Reviews, 2017) stated explicitly that "the accuracy and precision of total testosterone and SHBG assays" are foundational to reliable calculated free testosterone, and that inaccuracies in either "increase the risk of misclassification in the diagnosis of androgen disorders" [1, mechanism_review]. In the Adaway et al. (2020) head-to-head comparison of five automated SHBG platforms, platform-specific differences in SHBG propagated into cFT estimates differing by up to several percent, leading the authors to recommend using analyzer-specific reference ranges for cFT until SHBG standardization is improved [7, cohort]. The Walravens et al. (2025) dataset, comparing Roche, Abbott, and Siemens SHBG immunoassays with LC-MS/MS testosterone in 113 men and 106 women, similarly found that mean cFT values for men ranged 7.23–7.51 ng/dL across platforms, a modest absolute spread that nonetheless has diagnostic border-zone consequences [3, cohort].

For the FAI, the absence of SHBG harmonization is compounded by a structural limitation: FAI assumes a linear relationship between SHBG-bound and free androgen that breaks down at low SHBG concentrations (<30 nmol/L), where FAI overestimates free androgens and yields misleading results for hyperandrogenism evaluation in women [8, cohort].

Cross-reference: See the calculated free testosterone and total testosterone entries for the full downstream picture of how SHBG measurement error propagates into clinical decision thresholds.

## C.3 Analytical Interferences

**Biotin (vitamin B7):** Many SHBG immunoassays — and the broader hormone immunoassay platform ecosystem — use biotin–streptavidin chemistry to link the biotinylated capture antibody to a streptavidin-coated solid phase. High circulating biotin concentrations (from supplemental doses of 1–300 mg/day, far exceeding the physiological level of ~0.3 ng/mL) compete for streptavidin binding sites, partially displacing the biotinylated antibody–antigen complex and causing **falsely low results in sandwich/two-site assays** [9, mechanism_review]. Interference thresholds vary by assay and platform; even doses as low as 1–3 mg/day have been documented to suppress hormone assay results to clinically misleading levels. Patients should be counseled to withhold biotin supplements for at least 8 hours (and ideally 48–72 hours for high-dose regimens) before sampling.

**Heterophile and anti-animal antibodies:** Antibodies circulating in some patients — directed against animal immunoglobulins or as non-specific "heterophile" antibodies — can bridge the capture and detection antibodies in a two-site assay, producing a false signal independent of analyte concentration. In sandwich formats this results in **falsely elevated** results. Prevalence estimates range from 0.05–6% depending on the assay system. Suspected interference can be evaluated by serial dilution (non-parallel dilution response) or by using assay-specific blocking reagents.

**Abnormal SHBG variants:** SHBG has a number of described genetic variants (e.g., the P156L missense variant causing abnormal glycosylation and reduced secretion). A low SHBG immunoassay result attributable to a structural variant rather than a pathological state may not reflect true binding capacity; the ligand-binding assay would in principle detect reduced steroid-binding capacity independently of immunoreactive protein mass, though such assays are not routinely available [1, mechanism_review].

**Pregnancy:** During pregnancy, high estradiol occupies a substantial fraction of SHBG binding sites. Because standard immunoassays measure total immunoreactive SHBG protein rather than available binding capacity, the SHBG value in pregnancy overestimates actual binding, and calculated free testosterone will be artifactually low — a known limitation of immunoassay-based cFT in this context [6, mechanism_review].

## C.4 Biological Variability

**Within-subject (intraindividual) variation:** SHBG is relatively stable compared to many hormones. In the most rigorous biological variation study using both direct (CV-ANOVA, Bayesian) and indirect methods in a mixed-sex cohort, the within-subject CVI for SHBG was approximately 7–8% by direct methods (total cohort), with marked sex-stratification: ~6–7% in men, ~10–11% in women [10, cohort]. The index of individuality (CVI/CVG ratio) was 0.14 for the total cohort, indicating that population-based reference intervals have low utility for tracking individual change — a relevant consideration when using serial SHBG measurements to monitor disease progression or treatment response.

**Diurnal variation:** SHBG shows minimal diurnal fluctuation, in contrast to total testosterone. Brambilla et al. (JCEM 2009) — in a large study of men across the adult age span — reported that "much lower levels of diurnal variation were found for dihydrotestosterone, SHBG, LH, FSH, and estradiol at all ages," contrasted with a 20–25% testosterone decline by 16:00 h in men aged 30–40 [11, cohort]. Earlier data from Yie et al. (1990) did note modest morning-to-evening variation in male SHBG binding capacity that tracked testosterone fluctuations, but the physiological amplitude is small and not considered clinically significant for specimen timing [12, cohort]. SHBG sampling does not require morning collection, unlike testosterone.

**Postural and fasting effects:** Postural effects on SHBG are small. Fasting state can modestly alter SHBG (insulin suppresses hepatic SHBG production; a postprandial insulin spike may transiently lower SHBG), though this effect is not large enough to require strict fasting protocols in most clinical contexts.

**Sample stability:** SHBG is a glycoprotein and is relatively stable under standard preanalytical conditions. Studies of endocrine analyte stability across freeze-thaw cycles have generally found SHBG to be among the more stable analytes; there is no evidence of significant degradation under the 1–4 freeze-thaw cycles encountered in routine biobank handling [13, mechanism_review].

## C.5 Practical Implications for Result Interpretation

Because no mature harmonization program for SHBG exists, **results are not fully transportable across platforms or laboratories**. Reference intervals established on one platform cannot be directly applied to another, and calculated free testosterone results from different laboratories should not be compared at face value. Clinicians and laboratory teams should use analyzer-specific reference ranges for both SHBG and cFT. Where longitudinal tracking is critical (monitoring response to treatment), samples should ideally be run on the same platform in the same laboratory. For borderline clinical decisions that hinge on calculated free testosterone, the analytical uncertainty introduced by SHBG assay variation is a real contributor to diagnostic uncertainty — not a background technical footnote.

---

## Bibliography

1. Goldman AL, Bhasin S, Wu FCW, Krishna M, Matsumoto AM, Jasuja R. A reappraisal of testosterone's binding in circulation: physiological and clinical implications. *Endocr Rev.* 2017;38(4):302–324. PMID: 28673039. [mechanism_review]

2. Brotherton J. Estimation of serum sex hormone-binding globulin by five direct and two indirect methods. *J Clin Lab Anal.* 1990;4(6):405–409. PMID: 2283558. [mechanism_review]

3. Walravens J, Adaway J, Reyns T, Narinx N, Nyamaah JA, Antonio L, Kaufman JM, Keevil B, Fiers T, Lapauw B. Variability in SHBG assays and the effect thereof on calculated estimates of free testosterone. *Ann Clin Biochem.* 2025;62(6):493–500. DOI: 10.1177/00045632251350676. [cohort]

4. Thaler M, Müller C, Schlichtiger A, Gründler K, Moore M, Luppa PB. Steroid binding properties of the 2nd WHO International Standard for sex hormone-binding globulin. *Clin Chem Lab Med.* 2011;49(5):869–872. PMID: 21345159. [mechanism_review]

5. Vierbaum L, Weiss N, Kaiser P, Kremser M, Wenzel F, Thevis M, Schellenberg I, Luppa PB. Longitudinal analysis of external quality assessment of immunoassay-based steroid hormone measurement indicates potential for improvement in standardization. *Front Mol Biosci.* 2024. PMID: 38357630. DOI: 10.3389/fmolb.2024.1345356. [mechanism_review]

6. Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012. [mechanism_review]

7. Adaway J, Keevil B, Miller A, Monaghan PJ, Merrett N, Owen L. Ramifications of variability in sex hormone-binding globulin measurement by different immunoassays on the calculation of free testosterone. *Ann Clin Biochem.* 2020;57(1):88–94. PMID: 31679389. [cohort]

8. Keevil BG, Adaway J. The free androgen index is inaccurate in women when the SHBG concentration is low. *Clin Endocrinol.* 2018. DOI: 10.1111/cen.13561. [cohort]

9. Luong JHT, Male KB, Glennon JD. Biotin interference in immunoassays based on biotin-strept(avidin) chemistry: an emerging threat. *Biotechnol Adv.* 2019;37(5):634–641. PMID: 30872068. [mechanism_review]

10. Røys EA, Guldhaug NA, Viste K, Jones GD, Alaour B, Sylte MS, Torsvik J, Kellmann R, Strand H, Theodorsson E, Marber M, Omland T, Aakre KM. Sex hormones and adrenal steroids: biological variation estimated using direct and indirect methods. *Clin Chem.* 2023;69(1):100–109. DOI: 10.1093/clinchem/hvac175. [cohort]

11. Brambilla DJ, Matsumoto AM, Araujo AB, McKinlay JB. The effect of diurnal variation on clinical measurement of serum testosterone and other sex hormone levels in men. *J Clin Endocrinol Metab.* 2009;94(3):907–913. PMID: 19088162. [cohort]

12. Yie SM, Wang R, Zhu YX, Liu GY, Zheng FX. Circadian variations of serum sex hormone binding globulin binding capacity in normal adult men and women. *J Steroid Biochem.* 1990;36(1-2):111–115. PMID: 2362439. [cohort]

13. Yang J, Hamilton C, Robyak K, Zhu Y. Discrepancies in four algorithms for the calculation of free and bioavailable testosterone. *Clin Chem.* 2023;69(12):1429–1431. DOI: 10.1093/clinchem/hvad177. [mechanism_review]
