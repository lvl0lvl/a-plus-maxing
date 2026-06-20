# Section C: Measurement & Standardization — Serum 25-Hydroxyvitamin D

## C.1 The Two Assay Classes

Clinical laboratories measure serum total 25-hydroxyvitamin D by one of two fundamentally different approaches, which differ sharply in accuracy, specificity, and cost.

**Automated immunoassays** (chemiluminescent competitive-binding assays and ELISA-based platforms such as Abbott Architect, Roche Cobas, Beckman Coulter, and DiaSorin) dominate routine practice because they are fast, high-throughput, and require minimal sample preparation. Their principal limitations are well documented:

- *D2 (ergocalciferol) cross-reactivity / under-recovery.* Many immunoassays do not respond equivalently to 25(OH)D2 and 25(OH)D3. In a VDSP intralaboratory study evaluating 13 assays (11 immunoassays + 1 LC-MS/MS) across 50 serum samples, nine of eleven immunoassays showed deviations of up to 30% at high 25(OH)D2 concentrations, while only three immunoassays and the LC-MS/MS method handled D2-enriched samples without significant interference [1, mechanism_review]. This D2 under-recovery is clinically important for patients supplementing with ergocalciferol (D2).
- *DBP (vitamin D–binding protein) interference.* 25(OH)D circulates almost entirely bound to DBP (~88%) and albumin (~12%), with only ~0.03% free. Competitive immunoassays require a release reagent to displace 25(OH)D from DBP before antibody capture. Because DBP circulates at a 20–100-fold molar excess relative to 25(OH)D, incomplete displacement or re-binding to residual DBP causes concentration-dependent signal suppression. Immunoassays with different release-reagent formulations therefore show variable DBP-dependent inaccuracies not seen in chromatographic procedures [2, cohort]. In the Biochemia Medica head-to-head comparison, the Roche Cobas showed a mean bias of –14.1% against LC-MS/MS, while Abbott Architect showed +15.1% — both concentration-dependent [3, cohort].
- *C3-epimer cross-reactivity.* The structural isobar 3-epi-25(OH)D3 (see §C.3) is not resolved by most immunoassays and elevates the reported total.

**LC-MS/MS (liquid chromatography–tandem mass spectrometry)** is the reference-grade method. It separates 25(OH)D3 and 25(OH)D2 chromatographically before mass-based detection, providing independent quantification of each form. A modified LC-MS/MS protocol that includes a longer chromatographic run or chemical derivatization can additionally resolve 3-epi-25(OH)D3 from the parent compound [4, cohort]. In the VDSP baseline interlaboratory comparison study (15 laboratories, 50 serum samples), nearly all LC-MS/MS results met VDSP performance criteria (CV ≤10%, mean bias ≤|5%|), while only 3 of 8 immunoassay platforms achieved the bias criterion [5, cohort]. HPLC with UV detection, an older chromatographic approach, separates D2 and D3 but lacks the sensitivity and specificity of tandem mass spectrometry and is now largely supplanted by LC-MS/MS in reference laboratories.

## C.2 The Standardization Story

The inter-laboratory and inter-method disagreement in 25(OH)D measurement has been one of the most consequential analytical problems in clinical chemistry. Before standardization efforts matured, the same serum sample could be reported as vitamin D–deficient by one automated platform and vitamin D–sufficient by another — a bias spread as large as 30–40% was documented depending on concentration range and platform [6, mechanism_review; 3, cohort]. This is not a trivial technical nuance: it directly underlies the threshold-setting controversy. As Binkley et al. (2017) demonstrated using NHANES III data, a ±12% assay bias shifts the apparent prevalence of 25(OH)D <30 nmol/L by several percentage points nationally, and a single concentration point can shift by 15 ng/mL (20 → 35 ng/mL) depending on the direction of the assay bias [6, mechanism_review]. Reported disagreements between the Endocrine Society (sufficiency at ≥30 ng/mL) and IOM (sufficiency at ≥20 ng/mL) are partially confounded by the fact that the threshold studies were conducted on platforms with different systematic biases.

The response to this problem was a three-institution reference measurement infrastructure:

1. **NIST Standard Reference Material 972a** — a four-level frozen human serum panel with certified values for 25(OH)D2, 25(OH)D3, 3-epi-25(OH)D3, and 24R,25(OH)2D3, assigned by dual isotope-dilution LC-MS/MS at NIST and CDC [5, cohort]. SRM 972a is the anchor calibrator for assay developers and laboratory accreditation bodies.

2. **The Vitamin D Standardization Program (VDSP)** — a collaborative initiative of NIH Office of Dietary Supplements, NIST, CDC, and international national survey laboratories that (a) established reference measurement procedures (RMPs) at NIST, Ghent University, and CDC; (b) conducted interlaboratory comparison exercises quantifying baseline assay disagreement; and (c) developed retrospective standardization protocols allowing older study data measured on pre-standardization assays to be re-expressed on the reference scale [1, mechanism_review; 6, mechanism_review].

3. **CDC Vitamin D Standardization-Certification Program (VDSCP)** — the operational certification arm. Laboratories and manufacturers submit to quarterly performance rounds; certification requires ≤10% CV and ≤|5%| mean bias for four consecutive quarters against CDC's reference measurements. Once certified, laboratories carry an auditable traceability chain to the NIST/Ghent RMPs [7, mechanism_review]. Immunoassay bias has decreased appreciably since the VDSCP launched, but Ferrari et al. (2017) cautioned that as of the mid-2010s, bias exceeding ±15% — and exceeding 100% at very low concentrations (<21 nmol/L) — still appeared in proficiency surveys for some platforms [6, mechanism_review; 8, mechanism_review].

The practical implication: when comparing 25(OH)D values across studies, laboratories, or time points, assay traceability to the NIST/CDC reference scale is the minimum requirement for valid comparison. A value of "20 ng/mL" on a non-standardized immunoassay is not interchangeable with "20 ng/mL" on an RMP-traceable LC-MS/MS.

## C.3 The C3-Epimer

3-epi-25(OH)D3 (the C3-epimer) is a structural isobar of 25(OH)D3 formed by epimerization at carbon-3 of the A-ring. It is not separated from 25(OH)D3 by most immunoassays or by LC-MS/MS methods that do not incorporate a dedicated chromatographic separation step, meaning it contributes to the reported total.

The epimer is present in adult serum at low concentrations (<5% of total 25(OH)D3 in most adults), but it is substantially elevated in infants. Singh et al. (2006) found detectable epimer in 22.7% of 172 infants, where it contributed 8.7–61.1% of the total 25-OHD — with higher fractions in younger infants (r = −0.48 for age) [4, cohort]. This means a non-epimer-separating assay can substantially overestimate true biologically active 25(OH)D3 in neonates and infants.

Wright et al. (2012) confirmed, using both an epimer-resolving and a non-resolving LC-MS/MS method on 71 infants and 1,046 adults, that epimer separation is clinically significant in the first year of life but is not required for accurate 25(OH)D3 measurement in patients older than 2 years [9, mechanism_review]. For pediatric reference-range studies and neonatal screening panels, epimer-resolving methods are preferred. NIST SRM 972a certifies 3-epi-25(OH)D3 concentrations precisely because this epimer poses a recognized interference.

## C.4 Free vs. Total 25(OH)D and DBP Genetic Polymorphisms

Virtually all clinical assays measure TOTAL 25(OH)D (DBP-bound + albumin-bound + free). The **free 25(OH)D hypothesis** proposes that biologically active vitamin D is the ~0.03% unbound (free) fraction, analogous to free thyroid hormones, and that total 25(OH)D is a poor proxy when DBP concentrations vary systematically.

This has direct relevance to interpreting vitamin D status across ancestries. DBP is encoded by the GC gene, and two common single-nucleotide polymorphisms (rs7041 and rs4588) produce GC isoforms with different binding affinities for 25(OH)D and different population frequencies by ancestry. Historically, African Americans were observed to have lower total 25(OH)D than white Americans but paradoxically similar rates of bone-disease endpoints, suggesting adequacy despite lower measured totals.

Nielson et al. (2016) showed that the apparent racial difference in DBP concentration was largely an artifact of monoclonal antibody ELISA assays for DBP: the monoclonal ELISA reported 54% lower DBP in African Americans versus whites, but polyclonal assays and mass-spectrometry-based proteomics showed no significant racial difference in DBP [10, cohort]. Critically, the study found that free 25(OH)D measured from polyclonal DBP assays tracked total 25(OH)D concentration irrespective of race — meaning African Americans with lower total 25(OH)D also had lower free 25(OH)D on the more accurate measurement system. The clinical and policy debate continues, but the methodological lesson is firm: the long-cited "similar bioavailable D despite lower total D in Black populations" was partly a DBP assay artifact.

## C.5 D2 vs. D3 Quantification and Pre-Analytic Stability

When 25(OH)D is reported as a **total** value, clinicians lose information about the D2/D3 split. This matters because ergocalciferol (D2) supplementation raises 25(OH)D2 and some immunoassays differentially under-recover D2, leading to apparent non-response to supplementation. LC-MS/MS reports D2 and D3 separately, which is the preferred approach in research and in patients whose supplementation form matters clinically.

**Pre-analytic stability:** 25-hydroxyvitamin D is unusually robust. Antoniucci et al. (2005) found serum 25(OH)D unaffected by multiple freeze-thaw cycles [11, cohort]; Wielders and Wijnberg (2009) demonstrated stability "solid as a rock" at room temperature in whole blood and serum [12, cohort]. Routine sample handling with brief room-temperature exposure, standard refrigeration during processing, and multiple freeze-thaw cycles does not meaningfully alter results. Light protection and prompt centrifugation remain standard practice but are less critical for this analyte than for, e.g., folate or bilirubin.

---

## Bibliography

1. Wise SA, Camara JE, Sempos CT, et al. Vitamin D Standardization Program (VDSP) intralaboratory study for the assessment of 25-hydroxyvitamin D assay variability and bias. *J Steroid Biochem Mol Biol.* 2021;212:105917. PMID: 34010687. https://doi.org/10.1016/j.jsbmb.2021.105917 — tag: mechanism_review — tier: 2

2. Heijboer AC, Blankenstein MA, Kema IP, Buijs MM. Accuracy of 6 routine 25-hydroxyvitamin D assays: influence of vitamin D binding protein concentration. *Clin Chem.* 2012;58(3):543–548. PMID: 22247500. doi:10.1373/clinchem.2011.176545 — tag: cohort — tier: 1

3. Kocak FE, Ozturk B, Isiklar OO, et al. A comparison between two different automated total 25-hydroxyvitamin D immunoassay methods using liquid chromatography-tandem mass spectrometry. *Biochemia Medica.* 2015;25(3):430–438. https://doi.org/10.11613/BM.2015.044 — tag: cohort — tier: 1

4. Singh RJ, Taylor RL, Reddy GS, Grebe SKG. C-3 Epimers Can Account for a Significant Proportion of Total Circulating 25-Hydroxyvitamin D in Infants, Complicating Accurate Measurement and Interpretation of Vitamin D Status. *J Clin Endocrinol Metab.* 2006;91(8):3055–3061. https://doi.org/10.1210/jc.2006-0710 — tag: cohort — tier: 1

5. Wise SA, Phinney KW, Tai SS-C, et al. Baseline Assessment of 25-Hydroxyvitamin D Assay Performance: A Vitamin D Standardization Program (VDSP) Interlaboratory Comparison Study. *J AOAC Int.* 2017;100(5):1244–1252. https://doi.org/10.5740/jaoacint.17-0258 — tag: cohort — tier: 2

6. Binkley N, Dawson-Hughes B, Durazo-Arvizu R, et al. Vitamin D measurement standardization: The way out of the chaos. *J Steroid Biochem Mol Biol.* 2017;173:117–121. https://doi.org/10.1016/j.jsbmb.2016.12.002 [PMID 27979577] — tag: mechanism_review — tier: 2

7. Centers for Disease Control and Prevention. Vitamin D Standardization-Certification Program (VDSCP). CDC Clinical Standardization Programs. https://www.cdc.gov/clinical-standardization-programs/php/vitamin-d/index.html — tag: mechanism_review — tier: 2

8. Ferrari D, Lombardi G, Banfi G. Concerning the vitamin D reference range: pre-analytical and analytical variability of vitamin D measurement. *Biochemia Medica.* 2017;27(3):030501. https://doi.org/10.11613/BM.2017.030501 — tag: mechanism_review — tier: 1

9. Wright MJP, Halsall DJ, Keevil BG. Removal of 3-Epi-25-Hydroxyvitamin D3 Interference by Liquid Chromatography–Tandem Mass Spectrometry Is Not Required for the Measurement of 25-Hydroxyvitamin D3 in Patients Older than 2 Years. *Clin Chem.* 2012;58(12):1719–1720. https://doi.org/10.1373/clinchem.2012.191460 — tag: mechanism_review — tier: 1

10. Nielson CM, Jones KS, Chun RF, et al. Free 25-Hydroxyvitamin D: Impact of Vitamin D Binding Protein Assays on Racial-Genotypic Associations. *J Clin Endocrinol Metab.* 2016;101(5):2226–2234. https://doi.org/10.1210/jc.2016-1104 — tag: cohort — tier: 1

11. Antoniucci DM, Black DM, Sellmeyer DE. Serum 25-Hydroxyvitamin D Is Unaffected by Multiple Freeze-Thaw Cycles. *Clin Chem.* 2005;51(1):258–261. https://doi.org/10.1373/clinchem.2004.041954 — tag: cohort — tier: 1

12. Wielders JPM, Wijnberg FA. Preanalytical Stability of 25(OH)–Vitamin D3 in Human Blood or Serum at Room Temperature: Solid as a Rock. *Clin Chem.* 2009;55(8):1584–1585. https://doi.org/10.1373/clinchem.2008.117366 — tag: cohort — tier: 1
