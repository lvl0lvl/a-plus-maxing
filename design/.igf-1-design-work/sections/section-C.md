# Section C: Measurement & Standardization

## The Assay Challenge: IGFBP Interference

More than 90% of circulating IGF-1 travels as part of a ternary complex — bound to insulin-like growth factor binding protein-3 (IGFBP-3) and an acid-labile subunit (ALS). The remaining fraction binds to other IGFBPs (principally IGFBP-1 and IGFBP-2). This pervasive binding creates the central technical problem in IGF-1 measurement: the binding proteins occlude the antibody epitopes required for immunoassay recognition, a phenomenon called IGFBP interference [1, mechanism_review].

Early radioimmunoassays did not include a protein dissociation step. Results were therefore substantially affected by the IGFBP milieu, which varies with age, nutritional status, and disease state — meaning two patients with identical true IGF-1 concentrations could yield different assay readings depending on their IGFBP-3 levels alone. Modern assays address this by dissociating IGF-1 from its binding proteins before measurement [2, mechanism_review].

The two dominant dissociation strategies are:

- **Acid-ethanol extraction**: serum is acidified (typically to pH ~2.0) and precipitated with ethanol, denaturing the binding proteins and releasing IGF-1. After neutralization, the extracted supernatant is assayed. This approach is the historical workhorse and remains widely used for its relative simplicity [2, mechanism_review].
- **Acid dissociation followed by IGF-II excess**: large molar excess of IGF-II is added after acidification, competitively displacing IGF-1 from residual IGFBP binding sites before assay reading. This approach is used in some automated two-site sandwich immunoassays [1, mechanism_review].

Neither method is perfect. Residual IGFBP carryover remains a documented interference source if the dissociation is incomplete, particularly at high IGFBP-3 concentrations. Lot-to-lot calibrator variability and internal standard losses during extraction add further scatter.

## Standardization and Harmonization

Recognizing that inter-laboratory IGF-1 values were clinically non-comparable, the international community established formal standardization infrastructure. The **WHO First International Standard for IGF-1 (coded 02/254)** — a recombinant human preparation with an assigned content of 8.50 µg per ampoule — was developed and calibrated through an international collaborative study and adopted as the common calibration anchor for immunoassays [3, regulatory].

A landmark consensus statement from Clemmons (2011, *Clinical Chemistry*), convened under the auspices of the Growth Hormone Research Society, the IGF Society, and the IFCC, formalized recommendations for IGF-1 assay standardization and evaluation [4, mechanism_review]. Key recommendations included: calibrating assays against the WHO IS 02/254, validating extraction efficiency, establishing large age- and sex-matched normative datasets using the specific assay, and reporting results as an age-normalized standard deviation score (SDS) alongside absolute concentration in ng/mL.

Despite adoption of a common calibrator, inter-assay variation remains clinically significant. A six-immunoassay comparison in 911 healthy adults found that while lower reference limits were broadly similar, upper limits varied markedly between platforms — meaning whether a patient's IGF-1 is "elevated" depends substantially on which commercial assay performs the measurement, and results are not transferable between platforms even when both nominally trace to the WHO standard [5, cohort].

## LC-MS/MS and the Emerging Method Landscape

Liquid chromatography-tandem mass spectrometry (LC-MS/MS) has emerged as an alternative to immunoassay. Mass spectrometry avoids antibody epitope dependence and IGFBP interference by measuring tryptic peptides or intact IGF-1 directly by mass. In principle, this provides higher specificity and enables traceability to pure reference material independent of matrix effects [2, mechanism_review].

In practice, harmonization of LC-MS/MS assays requires alignment to both the WHO IS 02/254 and NIST reference standards. A multi-laboratory study of intact IGF-1 measurement by mass spectrometry found intra-laboratory variability of 2–4% CV but inter-laboratory variability of 14.5% CV — comparable in magnitude to the immunoassay problem [7, cohort]. A subsequent study showed that when LC-MS/MS methods are carefully traceable to both NIST and WHO standards, strong inter-laboratory agreement (R² > 0.93) is achievable, enabling reference interval sharing between laboratories — a step immunoassays have not matched [6, cohort]. LC-MS/MS remains a specialist method not yet in routine clinical use, but its traceability properties make it the method toward which the field is moving.

## Serial Monitoring and the SDS Requirement

Because absolute IGF-1 concentrations differ systematically between assay platforms, the Clemmons/Bidlingmaier consensus is unambiguous: **serial monitoring must use the same assay and its own matched age-sex reference population** [1, mechanism_review]. Results expressed as SDS (z-scores vs. the assay's own normative dataset) are more portable than absolute ng/mL values across age but are still not portable across assay platforms — the SDS denominator (the normative SD) is itself method-specific.

Cross-assay comparisons are unreliable. A patient whose IGF-1 is measured at one laboratory and then re-measured at a second laboratory using a different commercial platform may show a clinically meaningful apparent change that reflects only assay bias, not a biological shift. Treatment decisions — particularly in acromegaly or growth hormone deficiency management — should not be made on a cross-platform basis without a parallel-measurement bridging study.

## Analytical Interferences Beyond IGFBP

Three additional interference categories are relevant:

- **Residual IGFBP carryover**: incomplete acid dissociation in individual samples can suppress immunoreactivity. High IGFBP-3 states (pregnancy, late-stage liver disease) are the primary risk contexts.
- **Heterophile antibodies**: patient immunoglobulins capable of cross-linking assay antibodies cause spuriously elevated readings. The mechanism is assay-agnostic; dilution studies or blocking tube confirmations are the standard diagnostic maneuver when results are inconsistent with clinical presentation.
- **Biotin**: supplemental biotin at very high concentrations (>100 ng/mL) can interfere with biotin-streptavidin capture immunoassays, producing falsely low IGF-1 results. Clinically significant interference has been documented for the IDS-iSYS platform at pharmacological biotin doses [8, cohort]; at typical dietary biotin intake, interference is negligible.

## Pre-Analytics: Stability and the Nutritional State Caveat

IGF-1 has a serum half-life of approximately 12–15 hours when bound in the ternary complex (effectively much longer than free GH at 20–30 minutes), and total serum IGF-1 shows **no clinically significant circadian variation** in healthy subjects [9, cohort]. This stability is a practical advantage: sampling time of day is not a material pre-analytical variable, unlike cortisol or GH. Serum is stable at room temperature for at least 48 hours and for months when frozen.

However, a critical biological qualifier applies. IGF-1 is produced predominantly by the liver in a GH-dependent, nutrition-dependent manner. Both caloric and protein availability govern hepatic IGF-1 gene expression and secretion rate; fasting and protein malnutrition suppress IGF-1 independently of GH status [10, mechanism_review]. This means that a low IGF-1 result in a patient with inadequate caloric or protein intake may reflect nutritional suppression rather than GH deficiency — and an elevated IGF-1 in a well-nourished state tells a different story than one in a malnourished patient. This is a biological determinant of circulating concentration, not an analytic artifact, and must be addressed in interpretation rather than pre-analytical protocol.

---

## Bibliography

1. Clemmons DR, Bidlingmaier M. IGF-I assay methods and biologic variability: evaluation of acromegaly treatment response. *Eur J Endocrinol.* 2024;191(1):R1–R8. DOI: 10.1093/ejendo/lvae065. PMID: 38916798. [mechanism_review]

2. Ketha H, Singh RJ. Clinical assays for quantitation of insulin-like-growth-factor-1 (IGF1). *Methods.* 2015;81:93–98. DOI: 10.1016/j.ymeth.2015.04.029. PMID: 25937392. [mechanism_review]

3. Burns C, Rigsby P, Moore M, Rafferty B. The First International Standard for Insulin-like Growth Factor-1 (IGF-1) for immunoassay: preparation and calibration in an international collaborative study. *Growth Horm IGF Res.* 2009;19(5):457–462. DOI: 10.1016/j.ghir.2009.02.002. PMID: 19303800. [regulatory]

4. Clemmons DR. Consensus statement on the standardization and evaluation of growth hormone and insulin-like growth factor assays. *Clin Chem.* 2011;57(4):555–559. DOI: 10.1373/clinchem.2010.150631. PMID: 21285256. [mechanism_review]

5. Chanson P, Arnoux A, Mavromati M, Brailly-Tabard S, Massart C, Young J, Piketty ML, Souberbielle JC. Reference Values for IGF-I Serum Concentrations: Comparison of Six Immunoassays. *J Clin Endocrinol Metab.* 2016;101(9):3450–3458. DOI: 10.1210/jc.2016-1257. PMID: 27167056. [cohort]

6. Ezra S, Winstone TML, Singh R, Orton DJ. Agreement of LC-MS assays for IGF-1 traceable to NIST and WHO standards permits harmonization of reference intervals between laboratories. *Clin Biochem.* 2023;116:75–78. DOI: 10.1016/j.clinbiochem.2023.04.002. PMID: 37031902. [cohort]

7. Moncrieffe D, Cox HD, Carletta S, Becker JO, Thomas A, Eichner D, Ahrens B, Thevis M, Bowers LD, Cowan DA, Hoofnagle AN. Inter-Laboratory Agreement of Insulin-like Growth Factor 1 Concentrations Measured Intact by Mass Spectrometry. *Clin Chem.* 2020;66(4):579–586. DOI: 10.1093/clinchem/hvaa043. [cohort]

8. Knudsen CS, Adelborg K, Søndergaard E, Parkner T. Biotin interference in routine IDS-iSYS immunoassays for aldosterone, renin, insulin-like growth factor 1, growth hormone and bone alkaline phosphatase. *Scand J Clin Lab Invest.* 2022;82(1):6–11. DOI: 10.1080/00365513.2021.2003854. PMID: 34859720. [cohort]

9. Skjaerbaek C, Frystyk J, Kaal A, Laursen T, Møller J, Weeke J, Jørgensen JO, Sandahl Christiansen J, Orskov H. Circadian variation in serum free and total insulin-like growth factor (IGF)-I and IGF-II in untreated and treated acromegaly and growth hormone deficiency. *Clin Endocrinol (Oxf).* 2000;52:25–33. DOI: 10.1046/j.1365-2265.2000.00876.x. PMID: 10651750. [cohort]

10. Hawkes CP, Grimberg A. Insulin-Like Growth Factor-I is a Marker for the Nutritional State. *Pediatr Endocrinol Rev.* 2015;13(2):499–511. PMID: 26841638. [mechanism_review]
