---
title: "SHBG (Sex Hormone-Binding Globulin): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/shbg/research-report
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.shbg-design-work
provenance_slug: labs-specialist
source_count: 35
---

# SHBG (Sex Hormone-Binding Globulin): Canonical Research Report

## Summary

Sex hormone-binding globulin (SHBG) is the principal plasma transport protein for sex steroids and the master regulator of their bioavailability in target tissues. Synthesized by hepatocytes as a homodimeric glycoprotein, SHBG circulates in serum at concentrations that determine what fraction of total testosterone and estradiol can actually reach target cells and activate hormone receptors. Its binding affinity hierarchy — DHT > testosterone > estradiol — makes SHBG's regulatory grip tightest on androgens: when SHBG is low, free androgen exposure rises; when SHBG is high, androgens are sequestered. This dual role — as an **essential contextualizer of total testosterone** and as a **standalone metabolic biomarker** in its own right — is what makes SHBG one of the most informative single measurements in a standard endocrine panel.

Reference ranges are strongly assay-dependent and sex-specific. In adult men, population-based intervals span roughly **12.6–92.4 nmol/L** in NHANES-derived data [1, cohort], though clinical practice ranges such as Quest's 10–50 nmol/L [3, regulatory] are narrower. Men average ~27–37 nmol/L depending on age: SHBG rises gradually through middle age and accelerates past 60. Women consistently have higher SHBG than men — the NHANES interval for adult women is 18.4–211.5 nmol/L [1, cohort], with a premenopausal working range of approximately 40–120 nmol/L [5, cohort], driven by estrogenic stimulation of hepatic SHBG synthesis. No single universal cutpoint governs clinical decision-making; each laboratory's reference interval is assay-specific.

SHBG's most immediate clinical function is to correct total testosterone readings. Approximately 40–60% of circulating testosterone is tightly SHBG-bound and biologically inert; the remaining albumin-bound (~35–54%) and free (~1–3%) fractions carry androgen activity. When SHBG is suppressed by obesity or insulin resistance, total testosterone understates bioavailable androgen. When SHBG is elevated by aging, liver disease, or estrogen exposure, total testosterone overstates it. This is why the Endocrine Society's 2018 guideline explicitly recommends measuring free testosterone — using SHBG and total T as inputs to the Vermeulen equation — in any patient whose SHBG status is expected to be abnormal [6, regulatory].

Beyond its role in contextualizing androgens, low serum SHBG is an independent biomarker of insulin resistance and metabolic risk. Ding et al. in the *New England Journal of Medicine* (2009) demonstrated that the lowest SHBG quartile conferred a multivariable OR for incident type 2 diabetes of approximately 0.09–0.10 in women and 0.10 in men (highest vs. lowest quartile), and Mendelian randomization using SHBG gene variants confirmed a causal contribution [15, cohort]. This body of evidence positions SHBG as both a readout of hepatic metabolic function and a plausible participant in the insulin-resistance / T2D causal pathway.

Measurement is by immunometric immunoassay on automated platforms (Roche, Abbott, Siemens), calibrated against the WHO/NIBSC 08/266 International Standard. No equivalent of the CDC testosterone harmonization program exists for SHBG, meaning inter-assay biases of ±10–25% persist across platforms and results are not interchangeable without method-specific validation [19, mechanism_review]. Biotin supplementation causes falsely low results in many SHBG assays; heterophile antibodies cause falsely elevated results.

---

## Physiology & What SHBG Measures

### Hepatic Synthesis and Secretion

SHBG is produced predominantly by hepatocytes and secreted into the systemic circulation [12, mechanism_review]. The liver is the only significant source of plasma SHBG; Sertoli cells in the testis produce an antigenically related protein (androgen-binding protein, ABP) from the same gene via a distinct promoter, but ABP does not contribute meaningfully to circulating SHBG [12, mechanism_review].

Transcription of the SHBG gene in hepatocytes requires the nuclear receptor **hepatocyte nuclear factor 4-alpha (HNF-4α)**, which binds a DR1-like cis element in the SHBG promoter [24, mechanism_review]. HNF-4α is the pivotal transcriptional node through which metabolic and hormonal signals converge to modulate SHBG output. Conditions that reduce hepatic HNF-4α expression — most notably elevated intracellular lipid accumulation driven by dietary monosaccharides and hyperinsulinemia — suppress SHBG transcription, explaining much of the inverse relationship between insulin resistance and circulating SHBG [24, mechanism_review]. Winters et al. confirmed this mechanism in human liver tissue: HNF-4α mRNA levels correlated strongly and positively with SHBG mRNA, while insulin resistance (measured by HOMA-IR) showed inverse associations with both [33, mechanism_review].

SHBG is a glycoprotein; post-translational N-glycosylation at Asn residues in each monomer contributes to its circulating half-life and affects steroid-binding kinetics.

### Molecular Structure: Homodimer with Laminin G-like Domains

X-ray crystallography at 1.55 Å resolution revealed that SHBG is a **non-covalent homodimer**, with each monomer consisting of two laminin G-like (LG) domains [10, mechanism_review]. The N-terminal LG domain (encoded by exons 2–4) carries the **steroid-binding site**: the steroid intercalates into a hydrophobic pocket within a jellyroll β-sheet sandwich, with only ~2% of its surface exposed to solvent. A single hydrogen bond between Ser42 and the C3-oxygen of the steroid anchors the ligand. The two monomers associate head-to-head via a dimer interface of approximately 760 Å², forming a continuous 14-stranded β-sheet spanning the dimer [10, mechanism_review].

This structural arrangement places **two steroid-binding sites per dimer**, one per monomer, and the two sites communicate allosterically — occupancy at one site influences binding kinetics at the other, making SHBG's interaction with testosterone a dynamic, non-linear process [9, mechanism_review].

A calcium-binding site located ~20 Å from the steroid-binding pocket stabilizes the G domain fold and promotes dimerization; calcium occupancy is not required for steroid binding per se but influences the structural integrity of the active conformation [10, mechanism_review].

### Steroid Binding Affinity Hierarchy: DHT > Testosterone > Estradiol

SHBG binds sex steroids with high affinity (nanomolar K_d), but its affinity is not equal across ligands:

**5α-dihydrotestosterone (DHT) > testosterone > 17β-estradiol**

DHT occupies the binding pocket with the highest affinity of any endogenous steroid — its 5α-reduced A ring fits the hydrophobic pocket more snugly than testosterone's 4-ene structure [10, mechanism_review]. Estradiol, despite A-ring aromatization, has meaningfully lower affinity than either androgen [9, mechanism_review].

Physiologically, this affinity hierarchy means that SHBG sequesters a larger fraction of circulating DHT than testosterone, and more testosterone than estradiol. Because SHBG-bound steroid is not available for passive diffusion into target cells, this hierarchy amplifies SHBG's role as an androgen gate: conditions that raise SHBG preferentially suppress androgen bioavailability, while conditions that lower SHBG preferentially liberate androgens [9, mechanism_review; 17, animal].

### Regulating the Free and Bioavailable Fractions

In plasma, circulating testosterone partitions into three functional pools [9, mechanism_review]:

- **SHBG-bound (~44%)** — high affinity, not bioavailable for passive tissue entry
- **Albumin-bound (~50%)** — low affinity, dissociable at the capillary level, conventionally "bioavailable"
- **Free (~1–4%)** — unbound, immediately available to all tissues

The term *bioavailable testosterone* captures the free fraction plus the albumin-bound fraction. Only ~1–4% of total testosterone circulates unbound at any moment; SHBG thus controls access to the majority of plasma testosterone by sequestration [9, mechanism_review].

Transgenic mouse studies (murine) expressing human SHBG at supraphysiological levels confirmed the free hormone hypothesis in vivo — **species: transgenic mouse expressing human SHBG**: elevated SHBG raised total androgen concentrations (via hypothalamic-pituitary feedback sensing declining free hormone) while leaving free testosterone largely unchanged, yet attenuated androgenic effects on reproductive organs, demonstrating that SHBG-bound androgens are functionally restricted from accessing steroid-responsive tissues [17, animal].

Clinical measurement of SHBG in nmol/L therefore enables calculation of free and bioavailable testosterone via established algorithms (Vermeulen equation; modified Ly method), enabling clinicians to assess true androgen status independent of variations in total testosterone driven by SHBG shifts [9, mechanism_review].

### Hormonal Regulation of Hepatic SHBG Synthesis

SHBG production is bidirectionally regulated by overlapping hormonal and metabolic inputs at the hepatic transcription level [20, in_vitro; 24, mechanism_review]:

**Suppressors of SHBG synthesis:**
- **Insulin** — the dominant acute suppressor; directly decreases HNF-4α activity and SHBG promoter transcription, and blunts stimulatory effects of estradiol and thyroid hormone on SHBG output [20, in_vitro]
- **Androgens (in vivo)** — despite in vitro evidence of stimulation at supraphysiological concentrations, physiological androgen excess suppresses SHBG in vivo (reflected in low SHBG in conditions of androgen excess such as PCOS) [24, mechanism_review]
- **Dietary monosaccharides (glucose, fructose)** — trigger hepatic de novo lipogenesis → elevated intracellular fatty acids → reduced HNF-4α → lower SHBG transcription [24, mechanism_review]
- **Prolactin** — inhibits SHBG output in hepatoma cell models [20, in_vitro]

**Stimulators of SHBG synthesis:**
- **Estrogens** — raise SHBG via ERα-mediated promoter activation; exogenous estrogen (oral contraceptives, HRT) reliably elevates serum SHBG
- **Thyroid hormone (T3/T4)** — increases SHBG promoter activity and production; hyperthyroidism raises SHBG, hypothyroidism lowers it [20, in_vitro]
- **Tamoxifen, genistein, mitotane** — pharmacological agents with estrogen-like promoter effects that raise SHBG [24, mechanism_review]

This regulatory architecture explains why SHBG is an integrative hepatic sensor: low SHBG strongly signals an insulin-resistant, hyperandrogenic, or hepatic lipid-accumulation state; high SHBG reflects estrogen excess, hyperthyroidism, or caloric restriction.

### Membrane Receptor (RSHBG) and Non-Classical Signaling

Beyond its plasma transport role, SHBG exerts signaling effects at the cell membrane through a distinct membrane receptor, designated RSHBG (tentatively identified as megalin/LRP2 in some tissues) [22, mechanism_review]. When SHBG binds RSHBG on the cell surface and a steroid subsequently binds the SHBG–RSHBG complex, a G protein-mediated signal cascade is activated that raises intracellular cAMP [22, mechanism_review]. This non-genomic signaling pathway has been documented in prostate stromal and epithelial cells, breast cancer cell lines, and lymphocytes [22, mechanism_review]. The physiological importance of RSHBG signaling in normal tissue homeostasis is an active area of investigation and currently less well characterized than SHBG's plasma binding function.

### What Serum SHBG Indexes

A serum SHBG measurement in nmol/L directly quantifies the plasma binding capacity available to sequester sex steroids. As SHBG rises, a greater fraction of total testosterone and estradiol is held in the bound compartment and less is free. As SHBG falls — whether from insulin resistance, obesity, androgen excess, or hepatic fat accumulation — the free fraction expands without any change in total testosterone production. SHBG thus functions as an amplifier and attenuator of sex steroid signal strength at the tissue level, making it indispensable for interpreting total hormone concentrations: two individuals with identical total testosterone can have radically different free testosterone and tissue androgen exposure depending on their SHBG concentrations.

---

## Reference Ranges, Units & Clinical Use

### Units

SHBG is reported in **nmol/L** (nanomoles per litre) in all modern clinical and research settings. Older literature occasionally expressed SHBG in µg/dL or µg/mL, but nmol/L is now universal and is used throughout this entry.

### Adult Reference Intervals

Reference intervals for SHBG are strongly **assay-dependent, age-dependent, and sex-dependent**. No single universal cutpoint applies across all laboratories or platforms.

#### Men

A large-scale population reference established from 1,477 healthy US adults (≥40 years) in NHANES, analyzed by chemiluminescence immunoassay, placed the adult male interval at **12.6–92.4 nmol/L** [1, cohort]. This wide range reflects genuine biological variation compounded by assay differences: a clinical cohort of 1,000 men seen at a men's health practice found individual SHBG values spanning 6–109 nmol/L — a nearly 20-fold spread — with a mean of 31.8 ± 15.2 nmol/L [2, cohort]. Younger men (≤54 years) in that cohort averaged 27.7 nmol/L, while older men (≥55 years) averaged 36.6 nmol/L (p < 0.001), confirming the well-documented **age-dependent rise** [2, cohort]. Quest Diagnostics reports a narrower clinical reference of 10–50 nmol/L for adult men [3, regulatory], illustrating how assay platform and reference population together determine the interval in practice.

The age trajectory in men is clinically important: SHBG rises gradually from middle age and accelerates past 60, such that an SHBG of 50 nmol/L is unremarkable in a 70-year-old man but elevated in a 35-year-old [1, cohort; 2, cohort].

#### Women (non-pregnant)

Women consistently have **higher SHBG than men** [1, cohort]. The NHANES-derived reference interval in adult women (all ages) was 18.4–211.5 nmol/L [1, cohort]. In premenopausal women with normal menstrual cycles, the 5th–95th percentile interval for SHBG at age 30 is approximately **18–86 nmol/L** [4, cohort]; a PCOS reference cohort reported a median of 42 nmol/L (IQR 28–63), with a local reference range of 40–120 nmol/L [5, cohort]. Women have higher circulating SHBG primarily because of estrogenic stimulation of hepatic SHBG synthesis — the same pathway that explains the surge in SHBG during pregnancy (where levels can increase several-fold) and the rise seen with oral contraceptive or estrogen therapy.

#### Factors that lower SHBG (below-range values)

Obesity, insulin resistance, type 2 diabetes, hypothyroidism, hyperprolactinaemia, and androgen use all suppress SHBG [3, regulatory]. Low SHBG is independently associated with metabolic syndrome and is more common in men presenting with suspected hypogonadism: one study found 13 of 14 men with total testosterone < 300 ng/dL (10.4 nmol/L) had SHBG < 30 nmol/L [3, regulatory].

#### Factors that raise SHBG (above-range values)

Advanced age, exogenous estrogen (including oral contraceptives), hepatic disease, hyperthyroidism, anticonvulsants (e.g., phenytoin, carbamazepine), and HIV infection all increase SHBG [6, regulatory].

#### Assay variation

SHBG immunoassays from different manufacturers (Roche Elecsys, Siemens ADVIA Centaur, Abbott Architect, Beckman Coulter) are calibrated against the WHO/NIBSC 95/560 International Standard, but inter-assay biases of ±10–25% remain documented at clinically relevant concentrations [1, cohort]. There is **no full harmonisation** of SHBG assays analogous to the CDC testosterone standardisation programme. Results should not be directly compared across platforms without method-specific validation [8, cohort].

### Primary Clinical Use: Interpreting Total Testosterone

The central clinical purpose of measuring SHBG is to **contextualise a total testosterone result**.

Testosterone circulates bound predominantly to SHBG (~40–60% in most adults) and loosely to albumin (~35–55%), with only 1–3% circulating as free (unbound) testosterone. Only the free fraction — and, by extension, the albumin-bound fraction — can diffuse into target cells and activate androgen receptors. SHBG-bound testosterone is biologically inert.

This binding dynamic creates two clinically important errors when total testosterone is read in isolation:

- **Low SHBG → total T underestimates bioavailable androgen.** When SHBG is suppressed (e.g., in obesity, insulin resistance, or T2DM), a larger fraction of total T is free or albumin-bound. A man with low SHBG and borderline total T may have a normal free T, and a numerically low total T may deliver more bioactive androgen than it appears to suggest.
- **High SHBG → total T overestimates bioavailable androgen.** When SHBG is elevated (e.g., in aging men, HIV, anticonvulsant use), a large portion of total T is sequestered. A total T of 15 nmol/L with SHBG of 80 nmol/L leaves very little free T; the patient may be functionally androgen-deficient despite a numerically acceptable total T.

The Endocrine Society 2018 Clinical Practice Guideline on testosterone deficiency explicitly recommends measuring free T — in addition to total T — in men who have conditions known to alter SHBG levels, precisely because total T alone is an unreliable guide to androgen status in those contexts [6, regulatory].

### Calculated Free Testosterone: The Vermeulen Equation

Direct measurement of free testosterone by equilibrium dialysis is the gold standard but is technically demanding, expensive, and available at few laboratories. The most widely adopted clinical alternative is **calculated free testosterone (cFT)** using the law-of-mass-action equation described by Vermeulen, Verdonck, and Kaufman (1999) [32, mechanism_review]:

> cFT is derived from total testosterone (TT), SHBG, and albumin concentrations using experimentally determined binding constants: K_SHBG = 1 × 10⁹ L/mol and K_albumin ≈ 3–3.57 × 10⁴ L/mol. Because albumin concentration is relatively stable in healthy adults, a fixed value of 43 g/L is commonly assumed, introducing minimal error in non-pregnant individuals.

The Vermeulen calculation is available at www.issam.ch/freetesto.htm and is acknowledged by the Endocrine Society as a clinically reasonable approximation [6, regulatory; 32, mechanism_review]. Independent validation by direct equilibrium dialysis LC-MS/MS (n = 329 men and women) found that cFT-V overestimates free T by ~19% on average but performs as **the most robust approximation** across varying SHBG, albumin, and testosterone levels — its proportional bias is essentially independent of those input variables [11, mechanism_review]. A comparison of five published algorithms found large absolute differences between methods, underscoring the importance of method-specific reference intervals [8, cohort].

### The Free Androgen Index

The **Free Androgen Index (FAI)** is a simpler surrogate, used especially in women:

> **FAI = (Total Testosterone [nmol/L] / SHBG [nmol/L]) × 100**

FAI is not a direct estimate of free testosterone concentration — it is a dimensionless ratio reflecting the balance between androgen and its primary binding protein. It is widely used in **PCOS diagnosis and monitoring** because SHBG suppression (from insulin resistance and obesity — hallmarks of the syndrome) inflates the FAI even when total T is in the normal range.

Under the **Rotterdam 2003 consensus** for PCOS diagnosis, biochemical hyperandrogenism can be established by a raised FAI; commonly applied cutoffs include FAI > 4.5 or > 5.0 in clinical practice, though published values range from > 4 to > 5 depending on reference population and assay [5, cohort; 7, meta_analysis]. An FAI > 4.5 is validated against the Rotterdam phenotype definition in large gynaecological cohorts [5, cohort]. A 2025 systematic review and diagnostic meta-analysis found FAI had a sensitivity of 0.78 and specificity of 0.85 for PCOS hyperandrogenism by Rotterdam criteria using direct immunoassay — comparable to total testosterone alone at most thresholds, and more useful in obese patients where SHBG suppression is prominent [7, meta_analysis].

FAI is less reliable at the extremes: when SHBG is severely elevated (e.g., in hyperthyroidism or anticonvulsant use), FAI can falsely appear normal even when free T is low. At low SHBG concentrations (<30 nmol/L), FAI overestimates free androgens because the linear ratio breaks down [13, cohort]. In men, FAI is not a standard clinical tool; the Vermeulen cFT or direct equilibrium dialysis is preferred.

### No Universal SHBG Cutpoint

No single SHBG threshold has been universally adopted for clinical decision-making. The absence of full assay harmonisation means that a value flagged as "high" or "low" by one laboratory's reference interval may fall within normal limits at another institution using a different immunoassay platform. Clinicians must apply the reference interval derived from the same assay and population from which the result was generated [1, cohort; 8, cohort].

---

## Measurement & Standardization

### Assay Platforms

SHBG is measured in clinical laboratories primarily by **immunometric (sandwich/two-site) immunoassays**, most commonly using chemiluminescent detection on automated platforms [9, mechanism_review]. The two-site format uses two antibodies that recognize distinct epitopes on the SHBG molecule: a capture antibody immobilized on a solid phase and a labeled detection antibody, with signal proportional to the amount of SHBG present. ELISA formats are also available, and historically SHBG was measured by **ligand-binding/steroid-saturation assays**, which determined binding capacity by incubating serum with radiolabeled steroid (typically tritiated dihydrotestosterone) followed by charcoal separation — these older assays measured binding sites rather than immunoreactive protein mass, and results are not interchangeable with immunoassay values [14, mechanism_review].

Contemporary automated analyzers in wide clinical use include platforms from Roche (Elecsys/Cobas), Abbott (Alinity/Architect), and Siemens (Immulite/Atellica). These use electrochemiluminescent or chemiluminescent detection with analytical measuring ranges typically spanning 0.1–250 nmol/L. At three major platforms, mean SHBG values in a mixed-sex cohort were 47.1, 45.9, and 44.6 nmol/L respectively (Abbott, Roche, Siemens), with statistically significant inter-platform differences (p < 0.001) and proportional differences of approximately +3.3%, ~0%, and −2.3% relative to the group mean [31, cohort].

### Calibration and the Standardization Gap

Unlike total testosterone — which has the CDC Hormone Standardization (HoSt) accuracy-based certification program requiring ≤6.4% bias — **SHBG has no equivalent widely-adopted reference-method standardization program** [9, mechanism_review]. The field relies on calibration traceable to WHO/NIBSC International Standards: the 1st IS (NIBSC 95/560) established in 1998, now superseded by the **2nd International Standard for SHBG (NIBSC 08/266)**, which has two-fold higher steroid-binding capacity than its predecessor and improved thermal stability [29, mechanism_review]. Three-assay correlations anchored to the same IS showed slopes of 0.926–1.05 with R² = 0.948–0.985 across paired comparisons. However, calibration against the same IS does not guarantee result commutability across platforms: differences in antibody epitope recognition, matrix effects, and assay geometry mean that inter-method bias on patient samples can diverge from IS-based comparison.

An emerging mass spectrometric method for SHBG — antibody-free LC-MS/MS targeting a surrogate peptide after tryptic digestion — has been described as a candidate higher-order reference method. Unlike immunoassays, LC-MS/MS is immune to antibody cross-reactivity and provides SI-traceable quantification; however, it is not yet routinely deployed in clinical practice or used as the anchor for a harmonization program analogous to CDC HoSt-testosterone [19, mechanism_review].

**Why this matters:** SHBG is an input variable to calculated free testosterone (cFT) using the Vermeulen formula and to the free androgen index (FAI = total testosterone / SHBG × 100). Because cFT is derived algebraically from total testosterone and SHBG — and because the sensitivity of cFT to SHBG is non-linear — SHBG assay bias propagates directly into cFT [32, mechanism_review]. Goldman et al. (Endocrine Reviews, 2017) stated explicitly that "the accuracy and precision of total testosterone and SHBG assays" are foundational to reliable calculated free testosterone, and that inaccuracies in either "increase the risk of misclassification in the diagnosis of androgen disorders" [9, mechanism_review]. In the Adaway et al. (2020) head-to-head comparison of five automated SHBG platforms, platform-specific differences in SHBG propagated into cFT estimates differing by several percent, leading the authors to recommend using analyzer-specific reference ranges for cFT until SHBG standardization improves [16, cohort]. The Walravens et al. (2025) dataset, comparing Roche, Abbott, and Siemens SHBG immunoassays with LC-MS/MS testosterone in 113 men and 106 women, found that mean cFT values for men ranged 7.23–7.51 ng/dL across platforms — modest absolute spread that nonetheless has diagnostic border-zone consequences [31, cohort].

For the FAI, the absence of SHBG harmonization is compounded by a structural limitation: FAI assumes a linear relationship between SHBG-bound and free androgen that breaks down at low SHBG concentrations (<30 nmol/L), where FAI overestimates free androgens [13, cohort].

### Analytical Interferences

**Biotin (vitamin B7):** Many SHBG immunoassays use biotin–streptavidin chemistry. High circulating biotin concentrations (from supplemental doses of 1–300 mg/day, far exceeding the physiological level of ~0.3 ng/mL) compete for streptavidin binding sites, causing **falsely low results in sandwich/two-site assays** [18, mechanism_review]. Interference thresholds vary by platform; even doses as low as 1–3 mg/day have been documented to suppress hormone assay results to clinically misleading levels. Patients should withhold biotin supplements for at least 8 hours (ideally 48–72 hours for high-dose regimens) before sampling.

**Heterophile and anti-animal antibodies:** Antibodies circulating in some patients — directed against animal immunoglobulins or as non-specific heterophile antibodies — can bridge the capture and detection antibodies in a two-site assay, producing a false signal independent of analyte concentration. In sandwich formats this results in **falsely elevated** results. Prevalence estimates range from 0.05–6% depending on the assay system. Suspected interference can be evaluated by serial dilution (non-parallel dilution response) or by using assay-specific blocking reagents.

**Abnormal SHBG variants:** SHBG has a number of described genetic variants (e.g., the P156L missense variant causing abnormal glycosylation and reduced secretion). A low SHBG immunoassay result attributable to a structural variant may not reflect true binding capacity; the ligand-binding assay would in principle detect reduced steroid-binding capacity independently of immunoreactive protein mass, though such assays are not routinely available [9, mechanism_review].

**Pregnancy:** During pregnancy, high estradiol occupies a substantial fraction of SHBG binding sites. Because standard immunoassays measure total immunoreactive SHBG protein rather than available binding capacity, the SHBG value in pregnancy overestimates actual binding, and calculated free testosterone will be artifactually low — a known limitation of immunoassay-based cFT in this context [32, mechanism_review].

### Biological Variability

**Within-subject (intraindividual) variation:** SHBG is relatively stable compared to many hormones. In a rigorous biological variation study using both direct (CV-ANOVA, Bayesian) and indirect methods in a mixed-sex cohort, the within-subject CV_I for SHBG was approximately 7–8% by direct methods (total cohort), with marked sex-stratification: ~6–7% in men, ~10–11% in women [25, cohort]. The index of individuality (CV_I/CV_G ratio) was 0.14 for the total cohort, indicating that population-based reference intervals have low utility for tracking individual change — a relevant consideration when using serial SHBG measurements to monitor disease progression or treatment response.

**Diurnal variation:** SHBG shows minimal diurnal fluctuation, in contrast to total testosterone. Brambilla et al. (JCEM 2009) — in a large study of men across the adult age span — reported that "much lower levels of diurnal variation were found for dihydrotestosterone, SHBG, LH, FSH, and estradiol at all ages," contrasted with a 20–25% testosterone decline by 16:00 h in men aged 30–40 [30, cohort]. Earlier data noted modest morning-to-evening variation in male SHBG binding capacity that tracked testosterone fluctuations, but the physiological amplitude is small and not considered clinically significant for specimen timing [35, cohort]. **SHBG sampling does not require morning collection**, unlike testosterone.

**Postural and fasting effects:** Postural effects on SHBG are small. Fasting state can modestly alter SHBG (insulin suppresses hepatic SHBG production; a postprandial insulin spike may transiently lower SHBG), though this effect is not large enough to require strict fasting protocols in most clinical contexts.

**Sample stability:** SHBG is relatively stable under standard preanalytical conditions. Studies of endocrine analyte stability across freeze-thaw cycles have generally found SHBG to be among the more stable analytes; there is no evidence of significant degradation under the 1–4 freeze-thaw cycles encountered in routine biobank handling [34, mechanism_review].

### Practical Implications for Result Interpretation

Because no mature harmonization program for SHBG exists, **results are not fully transportable across platforms or laboratories**. Reference intervals established on one platform cannot be directly applied to another, and calculated free testosterone results from different laboratories should not be compared at face value. Clinicians and laboratory teams should use analyzer-specific reference ranges for both SHBG and cFT. Where longitudinal tracking is critical (monitoring response to treatment), samples should ideally be run on the same platform in the same laboratory. For borderline clinical decisions that hinge on calculated free testosterone, the analytical uncertainty introduced by SHBG assay variation is a real contributor to diagnostic uncertainty.

---

## Determinants & Clinical Significance

### What Lowers SHBG

**Insulin resistance and hyperinsulinemia** are the dominant drivers of low SHBG in the general population. Insulin directly suppresses hepatic SHBG synthesis in a dose-dependent fashion by downregulating HNF-4α, the transcription factor that drives SHBG gene expression in hepatocytes. HNF-4α mRNA levels correlate strongly and positively with SHBG mRNA, while insulin resistance (measured by HOMA-IR) shows inverse associations with both [33, mechanism_review].

**Obesity and central adiposity** lower SHBG through the same HNF-4α / insulin-suppression axis; visceral fat drives chronic hyperinsulinemia, and hepatic steatosis further impairs HNF-4α activity. In the MAILES longitudinal cohort (n = 1,786 men, 4.9-year follow-up), abdominal fat mass and serum triglycerides were the strongest independent inverse predictors of SHBG across time [21, cohort].

**Type 2 diabetes and metabolic syndrome.** Low SHBG reliably marks the insulin-resistant phenotype antecedent to both conditions. In Brand et al.'s individual-participant-data meta-analysis of 20 observational studies pooling 9,525 men, each quartile decline in SHBG was associated with an OR of 1.73 (95% CI 1.62–1.85) for prevalent metabolic syndrome and a HR of 1.44 (95% CI 1.30–1.60) for incident metabolic syndrome [27, meta_analysis].

**NAFLD/MASLD (hepatic fat).** Luo et al. examined 2,912 Chinese adults (cross-sectional) and found that participants with NAFLD had significantly lower SHBG than controls; in the fully adjusted model the OR for NAFLD was 0.24 (95% CI 0.18–0.32) comparing the highest vs. lowest SHBG quartile. Liver biopsy sub-analysis in 32 subjects showed that both SHBG and HNF-4α expression fell in step with increasing hepatic steatosis severity [23, cohort].

**Androgens and anabolic-androgenic steroids** suppress SHBG through direct hepatic effects, creating a positive-feedback loop in androgen excess states: lower SHBG → higher free androgen → further SHBG suppression.

**Glucocorticoids** suppress SHBG synthesis at the hepatic level.

**Hypothyroidism.** Thyroid hormones stimulate SHBG gene transcription; hypothyroidism removes this stimulus and lowers circulating SHBG.

**Growth hormone excess / acromegaly.** Excess GH suppresses SHBG, likely via IGF-1 and associated insulin resistance.

**Progestins** (particularly 19-nortestosterone derivatives) suppress SHBG.

**Nephrotic syndrome.** Urinary loss of intermediate-sized plasma proteins, including SHBG, reduces circulating levels — distinct from the hepatic-production suppression seen in metabolic disease.

### What Raises SHBG

**Aging.** SHBG rises progressively with age in both sexes, driven partly by declining androgens; in the MAILES cohort, age was the strongest positive predictor of SHBG (β = 0.409, p < 0.001) over 4.9 years [21, cohort].

**Estrogens, oral contraceptives, and pregnancy.** Estrogen stimulates hepatic SHBG synthesis via estrogen-receptor pathways. Combined oral contraceptives containing ethinylestradiol can raise SHBG 80–300% above baseline, an effect that persists and may have downstream androgen-availability implications.

**Hyperthyroidism.** Thyroid hormones (T3/T4) are positive regulators of SHBG gene expression; thyrotoxicosis markedly elevates SHBG, and SHBG measurement has historically been used as a surrogate for thyroid hormone action in peripheral tissues.

**Hepatic cirrhosis.** Although the liver is the sole synthetic organ for SHBG, advanced cirrhosis typically raises SHBG — probably reflecting impaired hepatic estrogen clearance (elevated estrogen then drives SHBG up) rather than increased synthetic capacity.

**Caloric restriction, anorexia nervosa, and low energy availability.** Severe negative energy balance raises SHBG, likely through reduced insulin secretion and improved insulin sensitivity, and may suppress free androgen/estrogen availability with reproductive and bone consequences.

**Anticonvulsants (phenytoin, carbamazepine)** induce hepatic CYP enzymes and increase SHBG production.

**HIV infection** is associated with elevated SHBG; mechanism not fully resolved.

### SHBG as an Independent Biomarker: the T2D and Cardiometabolic Story

The most consequential insight about SHBG over the past two decades is that low circulating SHBG does not merely reflect poor metabolic health — it may contribute causally to it.

#### Landmark evidence: Ding et al. 2009 (NEJM)

The pivotal study is Ding EL et al.'s prospective nested case-control analysis published in the *New England Journal of Medicine* in 2009 [15, cohort]. Using two independent cohorts — 359 postmenopausal women with incident T2D and 359 controls from the **Women's Health Study**, and 170 incident T2D men and 170 controls from the **Physicians' Health Study II** — Ding et al. showed dose-response inverse associations between baseline plasma SHBG and T2D risk that were striking in magnitude. In women, the multivariable OR for T2D across SHBG quartiles (lowest as reference): Q2: 0.16 (95% CI 0.08–0.33), Q3: 0.04 (0.01–0.12), Q4: 0.09 (0.03–0.21), P < 0.001 for trend. In men, Q4 vs. Q1 OR was 0.10 (0.03–0.36).

Critically, Ding et al. applied Mendelian randomization using two functional SHBG gene polymorphisms (rs6259, associated with ~10% higher SHBG, and rs6257, associated with ~10% lower SHBG) as genetic instruments. The predicted OR of T2D per SD increase in genetically instrumented SHBG was **0.28 (95% CI 0.13–0.58) in women** and **0.29 (95% CI 0.15–0.58) in men** — indicating that genetically higher SHBG reduces T2D risk even before metabolic disease develops, consistent with a causal contribution.

#### Corroborating Mendelian randomization: Perry et al. 2010

Perry JRB et al. in *Human Molecular Genetics* confirmed this in a larger sample: 27,657 T2D cases and 58,481 controls across 15 studies [26, meta_analysis]. A SHBG-raising allele (rs1799941) was associated with OR 0.94 (95% CI 0.91–0.97, P = 2 × 10⁻⁵) for T2D per allele copy, with T2D patients showing SHBG levels 0.23 SD lower than controls. The concordance between the genetic and observational signal strengthened the causal interpretation.

#### Metabolic syndrome in men: Brand et al. 2014

The individual-participant-data meta-analysis by Brand JS et al. across 20 observational studies in men found that each quartile decline in SHBG predicted incident metabolic syndrome with HR 1.44 (95% CI 1.30–1.60), independent of testosterone, with the strongest component associations for hypertriglyceridaemia, abdominal obesity, and hyperglycaemia [27, meta_analysis].

#### Cardiovascular disease: Yang et al. 2024

A Mendelian randomization and mediation analysis by Yang J et al. using the UK Biobank GWAS (n = 368,929) and CARDIoGRAMplusC4D CHD meta-analysis (60,801 cases, 123,504 controls) found OR 0.73 (95% CI 0.63–0.86) per SD increase in genetically instrumented SHBG for CHD. The causal pathway ran substantially through lipid profiles: triglycerides (44.3%) and total cholesterol (48%) each mediated nearly half of the protective effect — consistent with the shared insulin-resistance mechanism linking low SHBG to dyslipidaemia [28, cohort].

#### Causality: the honest framing

The MR evidence supports that SHBG is not merely a downstream reflection of insulin resistance — it plausibly contributes causally to T2D and metabolic risk, perhaps via direct cellular signalling through membrane SHBG receptors or by modulating free androgen/estrogen availability. However, the genetic instruments used in these studies (common SHBG gene variants) are not fully independent of the broader metabolic-risk locus, and the observational associations are partly confounded by the shared insulin-resistance pathway. The current consensus is that SHBG is both a robust biomarker and a plausible causal contributor, not a confirmed causal factor with a definitive mechanistic pathway established in humans.

### Dominant Clinical Use: Interpreting Total Testosterone

SHBG's most frequent clinical role is adjusting total testosterone for the fraction that is biologically available. Approximately 44–65% of circulating testosterone is tightly bound to SHBG (not bioavailable), ~33–54% is loosely bound to albumin (bioavailable), and only 1–3% is free. When SHBG is high (e.g., aging, hyperthyroidism, oral estrogens), total testosterone overstates androgen activity; when SHBG is low (e.g., obesity, insulin resistance), total testosterone understates available androgen. Calculated free testosterone (using the Vermeulen equation) and the Free Androgen Index (FAI = 100 × total T / SHBG) are both derived from the total T + SHBG pair. The Endocrine Society recommends measuring SHBG when total testosterone results are discordant with clinical presentation, particularly in populations where SHBG is predictably shifted [6, regulatory].

### Limitations

- **Not a standalone diagnostic.** Low SHBG identifies insulin resistance and metabolic risk with high sensitivity but poor specificity — many conditions lower SHBG. It does not diagnose T2D, metabolic syndrome, or androgen deficiency in isolation.
- **Assay heterogeneity.** There is no international harmonisation standard for SHBG immunoassays; inter-laboratory CVs up to 15–25% have been reported, limiting direct comparison of absolute values across studies [9, mechanism_review].
- **Confounding by shared pathway.** The epidemiological associations between SHBG and T2D, MetS, and CVD are all embedded in the insulin-resistance / adiposity axis; residual confounding is difficult to exclude even in MR designs.
- **Sex, age, and menopausal status modifier effects.** Reference intervals differ substantially between men, premenopausal women, and postmenopausal women; clinical cut-offs lack universal consensus.
- **Hepatic disease complicates interpretation.** Cirrhosis raises SHBG via estrogen accumulation even as hepatocyte mass is lost; in this context SHBG does not reflect androgen bioavailability in the usual way.

---

## Bibliography

[1]. Wang Y, et al. Definition, Prevalence, and Risk Factors of Low Sex Hormone-Binding Globulin in US Adults. *J Clin Endocrinol Metab.* 2021;106(11):e4660–e4673. PMID: 34125885. — tag: cohort — tier: 1

[2]. Krakowsky Y, et al. Serum Concentrations of Sex Hormone-binding Globulin Vary Widely in Younger and Older Men: Clinical Data from a Men's Health Practice. *Eur Urol Focus.* 2019;5(4):631–636. PMID: 28753796. — tag: cohort — tier: 1

[3]. Winters SJ. SHBG and total testosterone levels in men with adult onset hypogonadism: what are we overlooking? *Clin Diabetes Endocrinol.* 2020;6:18. PMID: 33014416. — tag: regulatory — tier: 1

[4]. Braunstein GD, et al. Testosterone reference ranges in normally cycling healthy premenopausal women. *J Sex Med.* 2011;8(10):2924–2934. PMID: 21771278. — tag: cohort — tier: 1

[5]. Rasquin Leon LI, et al. The relationships of sex hormone-binding globulin, total testosterone, androstenedione and free testosterone with metabolic and reproductive features of PCOS. *Clin Endocrinol (Oxf).* 2021;95(4):629–638. PMID: 34277990. — tag: cohort — tier: 1

[6]. Bhasin S, et al. Testosterone Therapy in Men With Hypogonadism: An Endocrine Society Clinical Practice Guideline. *J Clin Endocrinol Metab.* 2018;103(5):1715–1744. PMID: 29562364. — tag: regulatory — tier: 1

[7]. Bizuneh AD, et al. Evaluating the diagnostic accuracy of androgen measurement in polycystic ovary syndrome: a systematic review and diagnostic meta-analysis to inform evidence-based guidelines. *Hum Reprod Update.* 2025;31(1):48–63. PMID: 39305127. — tag: meta_analysis — tier: 1

[8]. de Ronde W, et al. Calculation of bioavailable and free testosterone in men: a comparison of 5 published algorithms. *Clin Chem.* 2006;52(9):1777–1784. PMID: 16793931. — tag: cohort — tier: 1

[9]. Goldman AL, Bhasin S, Wu FCW, Krishna M, Matsumoto AM, Jasuja R. A reappraisal of testosterone's binding in circulation: physiological and clinical implications. *Endocr Rev.* 2017;38(4):302–324. PMID: 28673039. DOI: 10.1210/er.2017-00025. — tag: mechanism_review — tier: 1

[10]. Grishkovskaya I, Avvakumov GV, Sklenar G, Dales D, Hammond GL, Muller YA. Crystal structure of human sex hormone-binding globulin: steroid transport by a laminin G-like domain. *EMBO J.* 2000 Feb 15;19(4):504–12. PMID: 10675319. DOI: 10.1093/emboj/19.4.504. — tag: mechanism_review — tier: 1

[11]. Fiers T, et al. Reassessing Free-Testosterone Calculation by Liquid Chromatography-Tandem Mass Spectrometry Direct Equilibrium Dialysis. *J Clin Endocrinol Metab.* 2018;103(6):2314–2323. PMID: 29618085. — tag: mechanism_review — tier: 1

[12]. Hammond GL. Sex hormone-binding globulin: gene organization and structure/function analyses. *Horm Res.* 1996;45(3-5):197–201. PMID: 8964583. — tag: mechanism_review — tier: 1

[13]. Keevil BG, Adaway J. The free androgen index is inaccurate in women when the SHBG concentration is low. *Clin Endocrinol.* 2018. DOI: 10.1111/cen.13561. — tag: cohort — tier: 1

[14]. Brotherton J. Estimation of serum sex hormone-binding globulin by five direct and two indirect methods. *J Clin Lab Anal.* 1990;4(6):405–409. PMID: 2283558. — tag: mechanism_review — tier: 1

[15]. Ding EL, Song Y, Malik VS, Liu S. Sex hormone-binding globulin and risk of type 2 diabetes in women and men. *N Engl J Med.* 2009;361(12):1152–1163. PMID: 19657112. — tag: cohort — tier: 1

[16]. Adaway J, Keevil B, Miller A, Monaghan PJ, Merrett N, Owen L. Ramifications of variability in sex hormone-binding globulin measurement by different immunoassays on the calculation of free testosterone. *Ann Clin Biochem.* 2020;57(1):88–94. PMID: 31679389. — tag: cohort — tier: 1

[17]. Laurent MR, Hammond GL, Blokland M, Jardí F, Antonio L, Dubois V, Khalil R, Sterk SS, Gielen E, Decallonne B, Carmeliet G, Kaufman JM, Fiers T, Huhtaniemi IT, Vanderschueren D, Claessens F. Sex hormone-binding globulin regulation of androgen bioactivity in vivo: validation of the free hormone hypothesis. *Sci Rep.* 2016 Oct 17;6:35539. PMID: 27748448. — tag: animal — tier: 1

[18]. Luong JHT, Male KB, Glennon JD. Biotin interference in immunoassays based on biotin-strept(avidin) chemistry: an emerging threat. *Biotechnol Adv.* 2019;37(5):634–641. PMID: 30872068. — tag: mechanism_review — tier: 1

[19]. Vierbaum L, Weiss N, Kaiser P, Kremser M, Wenzel F, Thevis M, Schellenberg I, Luppa PB. Longitudinal analysis of external quality assessment of immunoassay-based steroid hormone measurement indicates potential for improvement in standardization. *Front Mol Biosci.* 2024. PMID: 38357630. DOI: 10.3389/fmolb.2024.1345356. — tag: mechanism_review — tier: 1

[20]. Plymate SR, Matej LA, Jones RE, Friedl KE. Inhibition of sex hormone-binding globulin production in the human hepatoma (Hep G2) cell line by insulin and prolactin. *J Clin Endocrinol Metab.* 1988 Sep;67(3):460–4. PMID: 2842359. — tag: in_vitro — tier: 1

[21]. Gyawali P, Martin SA, Heilbronn LK, et al. Cross-sectional and longitudinal determinants of serum sex hormone binding globulin (SHBG) in a cohort of community-dwelling men. *PLoS One.* 2018;13(7):e0200078. PMID: 29995902. — tag: cohort — tier: 1

[22]. Nakhla AM, Khan MS, Romas NA, Rosner W. Sex hormone-binding globulin receptor signal transduction proceeds via a G protein. *Steroids.* 1999 Apr;64(4):213–6. PMID: 10400382. — tag: mechanism_review — tier: 1

[23]. Luo J, Hendryx M, Qi L, et al. Association of sex hormone-binding globulin with nonalcoholic fatty liver disease in Chinese adults. *Nutr Metab (Lond).* 2018;15:79. PMID: 30455723. — tag: cohort — tier: 1

[24]. Pugeat M, Nader N, Hogeveen K, Raverot G, Déchaud H, Grenot C. Sex hormone-binding globulin gene expression in the liver: drugs and the metabolic syndrome. *Mol Cell Endocrinol.* 2010 Mar 5;316(1):129–35. PMID: 19786070. — tag: mechanism_review — tier: 1

[25]. Røys EA, Guldhaug NA, Viste K, Jones GD, Alaour B, Sylte MS, Torsvik J, Kellmann R, Strand H, Theodorsson E, Marber M, Omland T, Aakre KM. Sex hormones and adrenal steroids: biological variation estimated using direct and indirect methods. *Clin Chem.* 2023;69(1):100–109. DOI: 10.1093/clinchem/hvac175. — tag: cohort — tier: 1

[26]. Perry JRB, Weedon MN, Langenberg C, et al. Genetic evidence that raised sex hormone binding globulin (SHBG) levels reduce the risk of type 2 diabetes. *Hum Mol Genet.* 2010;19(3):535–544. PMID: 19933169. — tag: meta_analysis — tier: 1

[27]. Brand JS, Rovers MM, Yeap BB, et al. Testosterone, sex hormone-binding globulin and the metabolic syndrome in men: an individual participant data meta-analysis of observational studies. *PLoS One.* 2014;9(7):e100409. PMID: 25019163. — tag: meta_analysis — tier: 1

[28]. Yang J, Chen S, Xu Y, et al. Blood lipid levels mediating the effects of sex hormone-binding globulin on coronary heart disease: Mendelian randomization and mediation analysis. *Sci Rep.* 2024;14(1):12014. PMID: 38796576. — tag: cohort — tier: 1

[29]. Thaler M, Müller C, Schlichtiger A, Gründler K, Moore M, Luppa PB. Steroid binding properties of the 2nd WHO International Standard for sex hormone-binding globulin. *Clin Chem Lab Med.* 2011;49(5):869–872. PMID: 21345159. — tag: mechanism_review — tier: 1

[30]. Brambilla DJ, Matsumoto AM, Araujo AB, McKinlay JB. The effect of diurnal variation on clinical measurement of serum testosterone and other sex hormone levels in men. *J Clin Endocrinol Metab.* 2009;94(3):907–913. PMID: 19088162. — tag: cohort — tier: 1

[31]. Walravens J, Adaway J, Reyns T, Narinx N, Nyamaah JA, Antonio L, Kaufman JM, Keevil B, Fiers T, Lapauw B. Variability in SHBG assays and the effect thereof on calculated estimates of free testosterone. *Ann Clin Biochem.* 2025;62(6):493–500. DOI: 10.1177/00045632251350676. — tag: cohort — tier: 1

[32]. Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012. — tag: mechanism_review — tier: 1

[33]. Winters SJ, Talbott E, Guzick DS, Zborowski J, McHugh KP. Sex hormone-binding globulin gene expression and insulin resistance. *J Clin Endocrinol Metab.* 2014;99(12):E2780–E2785. PMID: 25226295. — tag: mechanism_review — tier: 1

[34]. Yang J, Hamilton C, Robyak K, Zhu Y. Discrepancies in four algorithms for the calculation of free and bioavailable testosterone. *Clin Chem.* 2023;69(12):1429–1431. DOI: 10.1093/clinchem/hvad177. — tag: mechanism_review — tier: 1

[35]. Yie SM, Wang R, Zhu YX, Liu GY, Zheng FX. Circadian variations of serum sex hormone binding globulin binding capacity in normal adult men and women. *J Steroid Biochem.* 1990;36(1-2):111–115. PMID: 2362439. — tag: cohort — tier: 1
