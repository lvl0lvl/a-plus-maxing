# Section C: Measurement, Standardization & Interferences

## C.1 Standardization Networks: NGSP and IFCC

Two parallel certification networks anchor HbA1c measurements worldwide. The **National Glycohemoglobin Standardization Program (NGSP)**, established in 1996, certifies manufacturer methods to be traceable to the Diabetes Control and Complications Trial (DCCT) reference assay [1, regulatory]. The DCCT-aligned result is reported in **percent HbA1c (%)** and is the number tied to all landmark clinical outcome data and current ADA treatment targets. The **International Federation of Clinical Chemistry (IFCC)** reference system, finalized in 2004, is a higher-order accuracy-based anchor using mass spectrometry and capillary electrophoresis to quantify glycated and non-glycated hexapeptides derived from purified HbA1c and HbA0 calibrators [2, regulatory]. IFCC results are expressed in **mmol/mol** (SI units).

The two networks are linked by a master equation: **NGSP (%) = [0.09148 × IFCC (mmol/mol)] + 2.152** [1, regulatory]. Because the IFCC method adds a systematic offset (~1.5–2% HbA1c lower throughout the clinical range), IFCC results are not numerically interchangeable with NGSP/DCCT values. The practical implication: a patient target of 7.0% (NGSP/DCCT) corresponds to approximately 53 mmol/mol (IFCC). The relationship is monitored by twice-yearly inter-network comparisons to confirm stability [3, mechanism_review]. Countries report in one or both systems; the US, per ADA recommendation, reports in % (NGSP); most of Europe reports in mmol/mol (IFCC).

Manufacturers must obtain annual NGSP certificates by demonstrating agreement within ±6% of Secondary Reference Laboratory means on fresh blood samples; the criteria are performance-based (clinical need) rather than metrological [4, regulatory]. The 2023 ADA/AACC laboratory guidelines (Recommendation 8.13) specify intralaboratory analytical imprecision below a CV of 1.5%, with interlaboratory CV not exceeding 2.5%, assessed across at least two HbA1c concentrations and ideally with no measurable bias [17, regulatory].

---

## C.2 Assay Methods

Five distinct measurement platforms are in clinical use; each exploits either the **charge difference** or **structural difference** between glycated and non-glycated hemoglobin.

**Cation-exchange HPLC (ion-exchange chromatography)** is the most widely deployed high-complexity laboratory method. A positively charged resin separates hemoglobin species by charge; the HbA1c fraction elutes at a characteristic retention time and its percentage is quantified. HPLC generates a chromatogram that **reveals the presence of hemoglobin variants** as anomalous peaks or altered elution patterns—a major diagnostic advantage. However, the method is sensitive to temperature and some variants co-elute with the HbA1c peak, producing falsely elevated or falsely depressed values depending on the variant's charge [5, mechanism_review].

**Capillary electrophoresis (CE)**, like HPLC, separates hemoglobin fractions by charge and similarly generates a variant-revealing electropherogram. CE is IFCC-traceable and NHS-approved in the UK, and handles a broader range of hemoglobin variants than some HPLC programs; head-to-head studies in patients without hemoglobin variants show results that are not significantly different from HPLC [5, mechanism_review].

**Boronate-affinity chromatography** uses boronate columns that selectively retain glycated hemoglobin through covalent boronate–diol interaction, allowing all other hemoglobin species to elute. Because it detects the structural presence of the cis-diol moiety (glycation chemistry) rather than charge, it is **largely unaffected by common structural variants** (HbS, HbC, HbE). The critical limitation is that it **cannot detect the presence of a variant**—the clinician receives no flag [5, mechanism_review]. Elevated fetal hemoglobin (HbF) can still interfere because immunoassay, boronate-affinity, and enzymatic methods all show HbF interference at clinically meaningful levels [2, regulatory].

**Immunoassay** methods raise antibodies against the glycated N-terminal four to eight amino acids of the hemoglobin β-chain. They are the most common platform by instrument count among NGSP-certified instruments [17, regulatory], are automatable on general analyzers, and cannot detect variant hemoglobin. Because the antibody epitope is at the N-terminal β-chain, amino-acid substitutions elsewhere in the molecule do not affect the assay; variants near the epitope (e.g., Hb Okayama, β2 His→Gln) can cause falsely low results by escaping antibody recognition [5, mechanism_review].

**Enzymatic assays** cleave and oxidize glycated hemoglobin peptides; they are largely resistant to common hemoglobin variants (HbS, HbC, HbE, HbD) but cannot identify their presence and show interference from elevated HbF, similar to boronate and immunoassay platforms [2, regulatory].

**Point-of-care (POC) analyzers** typically use boronate affinity or immunoassay chemistry in cartridge form, with test volumes of 1–10 µL and turnaround times of 1.5–12 minutes. The majority of POC devices listed in the NGSP-certified methods registry are dual-certified (IFCC-traceable and NGSP-certified) and capable of reporting results in both units [1, regulatory].

---

## C.3 Interferences: What Falsely Raises HbA1c

**Iron-deficiency anemia** is the most common cause of a spuriously elevated HbA1c. Iron deficiency prolongs red blood cell (RBC) lifespan—cells are released more slowly from the marrow, accumulate more glycation over their extended existence, and the measured fraction rises. Malondialdehyde, which is elevated in iron-deficiency states, independently enhances hemoglobin glycation [2, regulatory]. Iron replacement therapy lowers both HbA1c and fructosamine. Iron deficiency is also the mechanism behind the HbA1c elevation seen in late pregnancy in non-diabetic individuals. Alternative glycemic assessment (CGM or glucose monitoring) should replace HbA1c until the deficiency is corrected [2, regulatory].

**Vitamin B12 and folate deficiency** similarly prolong RBC survival through impaired erythropoiesis (megaloblastic anemia), leading to older cells and falsely elevated HbA1c.

**Splenectomy and asplenia** remove the organ responsible for culling senescent red cells, thereby lengthening mean RBC age and raising HbA1c independent of glycemia.

**Hemoglobinopathies causing co-elution on HPLC/CE:** Certain charge-based variants elute at the same retention time or mobility window as HbA1c, producing a falsely elevated composite peak. The specific variants and the degree of elevation are method-dependent and published in the NGSP interference table [2, regulatory].

**Carbamylation (uremia):** Urea-derived carbamyl groups attach to hemoglobin in patients with renal failure, producing carbamylated hemoglobin—a modified species that historically interfered with older charge-based HPLC methods by eluting near HbA1c. This analytical interference has been largely eliminated in current-generation assays [3, mechanism_review]. However, CKD still depresses HbA1c via renal anemia and EPO-driven RBC turnover (see below); the net effect is usually a falsely low reading in advanced CKD, not falsely high.

**Acetylation (aspirin):** Acetylated hemoglobin, formed through aspirin-mediated modification, can alter hemoglobin charge and produce falsely elevated results on some charge-based assays [6, mechanism_review].

---

## C.4 Interferences: What Falsely Lowers HbA1c

The common denominator for falsely low HbA1c is **shortened RBC lifespan**—younger cells have had less time for glucose to attach, so the glycated fraction is underrepresented regardless of the assay method used [2, regulatory].

**Hemolytic anemia** (any cause—autoimmune, microangiopathic, G6PD deficiency, sickle-cell disease) accelerates red cell destruction, raising RBC turnover and depressing HbA1c. Patients with **HbSS, HbCC, or HbSC** genotypes (homozygous sickle-cell disease, hemoglobin C disease, and compound heterozygotes) have pathological hemolysis severe enough that HbA1c should not be used for glycemic monitoring in these individuals; glycated albumin is the preferred alternative [2, regulatory].

**HbS trait (sickle-cell trait), HbC trait, HbE trait:** In heterozygotes the hemolytic burden is minimal, but the structural variant itself can directly interfere with charge-based HPLC or CE methods—co-eluting with HbA or causing abnormal peak shapes. The NGSP publishes method-specific interference data for each variant [2, regulatory]. Boronate affinity and enzymatic methods are largely unaffected by HbS, HbC, and HbE traits analytically, though they cannot flag the variant's presence. HbE trait is not detected by some HPLC programs, causing HbA1c to be artifactually lowered in the undetected state.

**Fetal hemoglobin (HbF):** HbF does not glycate at the same rate as HbA and is included in the total hemoglobin denominator; elevated HbF (hereditary persistence of fetal hemoglobin, some thalassemia syndromes, bone marrow stress) lowers the measured HbA1c fraction. Immunoassay, boronate affinity, and enzymatic methods all show clinically significant interference from HbF; most current HPLC/CE methods tolerate HbF up to 15–30% without significant bias [2, regulatory].

**Recent blood loss and transfusion:** Acute hemorrhage triggers a surge of young reticulocytes; blood transfusion dilutes the patient's glycated pool with donor RBCs. Either event lowers measured HbA1c irrespective of glucose control.

**Erythropoietin (EPO), iron, and B12/folate therapy:** All three stimulate new RBC production, lowering mean cell age and depressing HbA1c. HbA1c is suppressed during EPO therapy in CKD; diabetic patients with CKD stages 3–4 have been shown to have mean blood glucose levels that exceed the HbA1c-derived estimated average glucose, confirming that HbA1c underestimates true glycemia in this population [7, cohort]. In dialysis-dependent patients the degree of underestimation is clinically meaningful and the GA/HbA1c ratio is systematically elevated relative to controls [8, mechanism_review].

**Pregnancy (late):** Volume expansion and physiological hemodilution in the third trimester lower hematocrit; concurrently, RBC turnover increases. HbA1c may underestimate glucose exposure, and fructosamine or frequent glucose monitoring is preferred.

**Splenomegaly:** Enlargement accelerates RBC sequestration and destruction, shortening mean cell age and lowering HbA1c.

---

## C.5 Race and Ethnicity Offset

Across multiple large studies, Black/African American individuals have consistently higher HbA1c than non-Hispanic White individuals at the same measured mean glucose—an offset of approximately **0.3–0.4% (3–4 mmol/mol)** in adjusted analyses [9, cohort]. A retrospective cohort study of 1,788 CGM-linked Kaiser Permanente patients found a 0.33% higher A1C in Black versus White patients at identical average blood glucose [10, cohort]. A re-analysis of the Screening for Impaired Glucose Tolerance Study (SIGT) cohort and NHANES III data by Herman and Cohen (2012 JCEM, PMC3319188) found that Black, Hispanic, and other minority participants had significantly higher HbA1c than White participants after adjusting for measured plasma glucose and clinical covariates [9, cohort]. Mexican Americans show an approximately 0.12% offset and non-Hispanic Blacks approximately 0.21% versus non-Hispanic Whites in population-representative data [11, cohort]. The biological mechanism is incompletely understood but appears to involve differences in RBC survival, intracellular glycation rate, and possibly genetic determinants of hemoglobin glycation—not differences in glycemia per se. Crucially, population-level data from NHANES 2005–2008 show no ethnic differences in the association of HbA1c with retinopathy, implying that the offset is a measurement phenomenon rather than a marker of greater pathology [12, cohort]. Clinicians should interpret HbA1c in the context of self-monitored glucose or CGM data when the two are discordant, regardless of race.

---

## C.6 Variability: Analytical and Biological CVs

HbA1c is substantially more stable than fasting plasma glucose (FPG) as a glycemic marker. Comparative estimates show:

- **Within-subject biological CV (CVi) for HbA1c:** approximately **1.6–2%** in healthy adults (EFLM database; confirmed by a 2023 meta-analysis of 111 studies, which reported a median CVi of 1.7% in healthy subjects) [13, meta_analysis]. By contrast, **FPG CVi is ~5.7%** and 2-hour OGTT CVi is ~16.7% [14, cohort].
- **Analytical CV (CVa) for HbA1c:** typically **1–2%** for modern HPLC and immunoassay methods (intra-assay CV as low as 0.6% for DCCT-standardized HPLC in research settings) [15, cohort]. The 2023 ADA/AACC guidelines specify intralaboratory CVa <1.5% and interlaboratory CVa <2.5% [17, regulatory]. FPG CVa is ~2.5% [14, cohort].
- **Between-laboratory bias** for HbA1c: −3% to +2.5%; substantially tighter than FPG (−6% to +7%) [14, cohort].

The low CVi of HbA1c means a result does not need to be repeated immediately to confirm stability—a meaningful clinical and logistical advantage over glucose-based tests. However, in patients with diabetes, within-subject HbA1c variability increases (median CVi ~8% in T2DM, ~8.4% in T1DM [13, meta_analysis]), suggesting that for monitoring purposes, serial readings integrate more reliably than any single test.

---

## C.7 Fructosamine and Glycated Albumin: When to Use Them

When RBC lifespan is abnormal or the hemoglobin matrix is structurally compromised, HbA1c loses its validity as a glycemic index regardless of assay method. The preferred alternatives are **fructosamine** (a measure of total glycated serum proteins, predominantly albumin, reflecting mean glucose over 2–4 weeks) and **glycated albumin (GA)** (a direct measure of the glycated fraction of albumin, also reflecting 2–4 weeks) [16, mechanism_review].

Clinical triggers for switching to fructosamine/GA include: hemolytic anemia, recent transfusion, HbSS/HbCC/HbSC disease, significant iron deficiency, advanced CKD on dialysis (where HbA1c underestimates true glycemia—the GA/HbA1c ratio is systematically elevated in dialysis and pre-dialysis patients [8, mechanism_review]), EPO therapy, and late pregnancy [2, regulatory].

Limitations of fructosamine/GA: results are unreliable when serum albumin is low (hypoalbuminemia, nephrotic syndrome, chronic liver disease); they have no validated diagnostic thresholds for diabetes diagnosis; and they are not yet included in most clinical guideline algorithms. The shorter integration window (2–4 weeks vs. 8–12 weeks for HbA1c) can be a feature in rapidly changing situations (e.g., gestational diabetes, medication titration) but means results can be gamed by short-term compliance improvements before a clinic visit [16, mechanism_review].

---

## Bibliography

1. NGSP. IFCC Standardization of HbA1c — The IFCC and NGSP. ngsp.org/ifccngsp.asp [regulatory]
2. NGSP. Factors that Interfere with HbA1c Test Results. ngsp.org/factors.asp [regulatory]
3. Little RR, Rohlfing C. The National Glycohemoglobin Standardization Program (NGSP): Over 20 Years of Improving HbA1c Measurement. *Clinical Chemistry*. 2019;65(7):839–848. PMC6693326. [mechanism_review]
4. NGSP. NGSP Protocol: Certification. ngsp.org/protcert.asp [regulatory]
5. Ghouri N et al. Hemoglobin A1C. StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing. NCBI Bookshelf NBK549816. [mechanism_review]
6. Gils C, Reinholdt B, Andreassen BD, Brandslund I, Vinholt PJ. False increase of glycated hemoglobin due to aspirin interference in Tosoh G8 analyzer. *Clinical Chemistry and Laboratory Medicine*. 2018;56(5):e118–e120. DOI: 10.1515/cclm-2017-0768. PMID 29306911. [mechanism_review]
7. Chen H-S et al. Hemoglobin A(1c) and fructosamine for assessing glycemic control in diabetic patients with CKD stages 3 and 4. *American Journal of Kidney Diseases*. 2010. PMID 20202728. [cohort]
8. Vos FE, Schollum JB, Walker RJ. Glycated albumin is the preferred marker for assessing glycaemic control in advanced chronic kidney disease. *Clinical Kidney Journal*. 2011;4(6):368–375. [mechanism_review]
9. Herman WH, Cohen RM. Racial and Ethnic Differences in the Relationship between HbA1c and Blood Glucose: Implications for the Diagnosis of Diabetes. *Journal of Clinical Endocrinology & Metabolism*. 2012;97(4):1067–1072. PMC3319188. PMID 22238408. [cohort]
10. Karter AJ, Parker MM, Moffet HH, Gilliam LK. Racial and Ethnic Differences in the Association Between Mean Glucose and Hemoglobin A1c. *Diabetes Technology & Therapeutics*. 2023;25(10):697–704. PMID 37535058. PMC10611955. [cohort]
11. Davidson MB, Schriger DL. Effect of age and race/ethnicity on HbA1c levels in people without known diabetes mellitus: implications for the diagnosis of diabetes. *Diabetes Research and Clinical Practice*. 2010;87(3):415–421. PMID 20061043. [cohort]
12. Bower JK, Brancati FL, Selvin E. No ethnic differences in the association of glycated hemoglobin with retinopathy: the National Health and Nutrition Examination Survey 2005–2008. *Diabetes Care*. 2013;36(3):569–573. PMID 23069841. [cohort]
13. Rasmussen L et al. Within-subject variation of HbA1c: A systematic review and meta-analysis. PMC10395823. [meta_analysis]
14. Lim LL et al. Impact of analytical and biological variations on classification of diabetes using fasting plasma glucose, oral glucose tolerance test and HbA1c. *Scientific Reports*. 2017;7:13114. [cohort]
15. van Dijk W et al. Heritability of HbA1c and Fasting Blood Glucose in Different Measurement Settings. *Twin Research and Human Genetics*. [cohort]
16. Vos FE et al. Clinical Utility of Fructosamine and Glycated Albumin. StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing. NCBI Bookshelf NBK470185. [mechanism_review]
17. ElSayed NA et al. (ADA/AACC). Guidelines and Recommendations for Laboratory Analysis in the Diagnosis and Management of Diabetes Mellitus. *Diabetes Care*. 2023;46(10):e151–e199. PMC10516242. [regulatory]

---

## Post-fix grep audit

Grep results run against the final file (all must be CLEAN or explicitly dispositioned):

| Pattern | Result | Disposition |
|---|---|---|
| `[5, regulatory]` on StatPearls | CLEAN | Fixed: [5] retains `mechanism_review` tag; CV standards moved to [17, regulatory] (ADA/AACC 2023) |
| `[3, regulatory]` on Little & Rohlfing 2019 | CLEAN | Fixed: all three occurrences (lines C.1 inter-network comparison, C.3 carbamylation, bib entry) changed to `mechanism_review`; ngsp.org citations [1]/[2]/[4] `regulatory` tags untouched |
| `[6]` bib entry malformed (Frontiers/BJBS 13898) | CLEAN | Replaced with Gils C et al., *Clinical Chemistry and Laboratory Medicine* 2018;56(5):e118–e120, DOI 10.1515/cclm-2017-0768, PMID 29306911 — directly reports aspirin interference on Tosoh G8 HPLC analyzer; `[mechanism_review]` tag retained; inline `[6, mechanism_review]` in C.3 aspirin paragraph unchanged |
| CAP Today / captodayonline | CLEAN | Removed entirely; old [6] bib entry deleted |
| Malta Medical Journal / mmsjournals | CLEAN | Removed entirely; old [7] bib entry deleted; CE/HPLC comparison claim re-sourced to [5, mechanism_review] (StatPearls) |
| Clinical Laboratory Science / Löffler | CLEAN | Removed entirely; old [8] bib entry deleted; immunoassay platform-count claim softened (no number) and re-sourced to [17, regulatory] (ADA/AACC 2023) |
| ADLM / myadlm / Clinical Laboratory News | CLEAN | Removed entirely; old [12] bib entry deleted; dialysis underestimation claim replaced with [7, cohort] (Chen 2010, AJKD, PMID 20202728) and [8, mechanism_review] (Vos 2011, Clin Kidney J) |
| Kaiser press release / divisionofresearch | CLEAN | Replaced with peer-reviewed paper: Karter AJ et al., *Diabetes Technology & Therapeutics* 2023;25(10):697-704, PMID 37535058 [10, cohort] |
| Diabetes Prevention Program (mislabel) | CLEAN | Fixed: DPP label removed; text now correctly identifies the cohort as SIGT + NHANES III (Herman & Cohen 2012 JCEM) |
| finddx / FIND NGO | CLEAN | Removed from both body and bib; qualitative POC device landscape claim re-sourced to [1, regulatory] (NGSP registry) |
| Roche vendor paper / diagnostics.roche | CLEAN | Removed from bib; Hb Okayama epitope claim re-sourced to [5, mechanism_review] (StatPearls) |
| Numbers in body with no bib entry | CLEAN | All 17 inline cite numbers map to a bib entry |
| Inline tag / bib tag consistency | CLEAN | All [N, tag] pairs match their bib entry tags |

**C-F07 (microvascular risk equivalence):** The original text cited Little & Rohlfing 2019 (at the time tagged `[3, regulatory]`, now corrected to `[3, mechanism_review]`) for the claim that higher HbA1c in Black patients confers no greater microvascular risk. Little & Rohlfing is an NGSP standardization paper and contains no outcomes data. Replaced with Bower, Brancati & Selvin 2013 (*Diabetes Care*, PMID 23069841) [12, cohort] — an NHANES 2005–2008 cross-sectional study that specifically found no ethnic differences in the association of HbA1c with retinopathy.
