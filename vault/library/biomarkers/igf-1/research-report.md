---
title: "IGF-1 (Insulin-like Growth Factor 1): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/igf-1/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.igf-1-design-work
provenance_slug: labs-specialist
source_count: 26
---

# IGF-1 (Insulin-like Growth Factor 1): Canonical Research Report

## Summary

Insulin-like growth factor 1 (IGF-1) is the stable, time-integrated read-out of growth hormone (GH) secretory activity. Because IGF-1 circulates bound to binding proteins with a serum half-life of approximately 12–15 hours — versus as little as 10–20 minutes for free GH — it effectively buffers the episodic pulsatility of GH release and reflects the preceding days' integrated GH output. This is its defining clinical property: a single random GH measurement is largely uninterpretable, whereas a single IGF-1 measurement provides a reliable summary signal [2, mechanism_review; 5, regulatory]. Values are reported in ng/mL, which is numerically equivalent to µg/L.

The dominant practical implication for interpretation is that **IGF-1 is uninterpretable without age normalization**. IGF-1 rises steeply through childhood, peaks at puberty, and then declines continuously through adulthood into old age — a trajectory spanning roughly a 5-fold range from peak puberty (values readily exceeding 400–600 ng/mL) to late elderly (often below 100 ng/mL in the eighth decade). A value that is unremarkable in a 70-year-old may indicate significant GH insufficiency in a 17-year-old, and vice versa. The gold standard for interpretation is the **standard deviation score (SDS)**, also called the z-score: the number of standard deviations above or below the age- and sex-matched mean for the specific immunoassay used [9, cohort; 5, regulatory].

The primary clinical applications are (1) first-line biochemical screening for **acromegaly** (GH excess from a pituitary somatotroph adenoma), where an elevated age-adjusted IGF-1 SDS above approximately +2 is the recommended initial test, and (2) supportive evidence in the workup of **GH deficiency**, where a low IGF-1 is suggestive but — crucially — not specific: malnutrition, liver disease, poorly controlled diabetes, hypothyroidism, oral estrogen use, aging, and systemic illness all independently suppress IGF-1 without GH axis pathology.

The longevity literature adds a counterintuitive dimension. Animal models with reduced GH/IGF-1 signaling show substantially extended lifespan, and a 22-year follow-up of ~90 GH-receptor-deficient Ecuadorian subjects with Laron syndrome revealed near-zero cancer and diabetes incidence. However, these findings involve extreme, monogenic reduction in GH signaling from birth — they do not imply that lowering IGF-1 within the normal range in healthy adults extends human lifespan. Epidemiological data in humans reveal a **U-shaped mortality pattern**: both high IGF-1 (associated with breast cancer and prostate cancer risk) and low IGF-1 (associated with cardiovascular mortality in older adults) carry elevated risk, with the nadir around 120–160 ng/mL in one large meta-analysis [25, meta_analysis]. The honest framing is: this is not a parameter to manipulate naively.

---

## Physiology & The GH/IGF-1 Axis

### What IGF-1 Is

Insulin-like growth factor 1, also known historically as somatomedin C, is a 70-amino-acid peptide hormone with a molecular weight of approximately 7,649 Da. Its structural homology to proinsulin gives the molecule its name and partly explains its ability to produce insulin-like metabolic effects at high concentrations [1, mechanism_review]. IGF-1 circulates at concentrations typically in the ng/mL range (equivalent to µg/L), with levels that vary substantially by age, nutritional status, and GH secretory capacity.

The dominant source of circulating IGF-1 is the **liver**: approximately 75% of serum IGF-1 is of hepatic origin, produced by hepatocytes in direct response to growth hormone receptor stimulation [2, mechanism_review]. Outside the liver, IGF-1 is also synthesized locally in bone, muscle, cartilage, and many other tissues, where it acts in autocrine and paracrine fashions to regulate cellular growth and differentiation [1, mechanism_review]. For most clinical purposes, it is the endocrine (hepatic-derived, circulating) fraction that is measured and interpreted.

### The GH/IGF-1 Axis: Hypothalamic Control to Peripheral Action

IGF-1 sits at the downstream end of a tightly regulated neuroendocrine cascade:

1. **Hypothalamus:** Two opposing hypothalamic peptides set the pace of GH output. Growth hormone-releasing hormone (GHRH) stimulates somatotroph cells in the anterior pituitary to synthesize and release GH; somatostatin (SST) provides tonic inhibition, dampening GH pulses. A third input, **ghrelin** (secreted primarily by the stomach), acts on pituitary receptors to amplify GH release — functioning as an endogenous GH secretagogue [2, mechanism_review].

2. **Pituitary somatotrophs:** GHRH binding at pituitary somatotroph cells triggers GH gene transcription and episodic GH release into the portal and then systemic circulation. GH secretion is characteristically **pulsatile**, with 5–8 peaks per 24 hours, the largest occurring in the early hours of sleep.

3. **Liver → IGF-1:** Circulating GH binds hepatic GH receptors, activating the JAK2/STAT5b intracellular pathway. This drives IGF-1 gene transcription and release of IGF-1 peptide into the bloodstream [2, mechanism_review].

4. **Negative feedback:** IGF-1 feeds back at both the hypothalamus (stimulating somatostatin release, blunting GHRH) and at the pituitary (directly suppressing somatotroph GH output). GH itself also feeds back at both levels. This closed-loop architecture prevents runaway somatotropic stimulation and explains why pharmacological blockade of IGF-1 signaling raises circulating GH [2, mechanism_review].

### Why IGF-1 Is the Stable, Integrated Read-Out of GH Status

A clinically important consequence of GH pulsatility is that a **single random serum GH measurement is largely uninterpretable**: a GH level drawn between pulses in a normal individual is indistinguishable from that of a GH-deficient patient. Conversely, a transiently elevated GH level during a physiological pulse does not confirm pathological excess [5, regulatory].

IGF-1 solves this problem. Because IGF-1 circulates bound to binding proteins (see below), its serum half-life is approximately 15 hours — compared with as little as 10–20 minutes for free GH [2, mechanism_review]. This extended half-life buffers the hour-to-hour fluctuations of GH pulses: **IGF-1 serum concentrations exhibit no meaningful diurnal variation** and represent a time-integrated index of the preceding days' GH secretory activity. The Endocrine Society Clinical Practice Guideline on acromegaly formalizes this: a single IGF-1 measurement is recommended as the primary screening test for both GH excess (acromegaly) and GH deficiency, because it reliably reflects integrated GH status in a way that random GH cannot [5, regulatory].

Research by Faje and Barkan (2010) refined this further, demonstrating that it is specifically the **basal (nadir, non-pulsatile) component** of GH secretion — not the pulse amplitude — that drives ambient circulating IGF-1 concentrations (r² = 0.77 for nadir GH vs. serum IGF-1) [6, cohort].

### The IGFBP System: Carrier, Reservoir, and Regulator

Less than 1% of circulating IGF-1 exists in free form. The vast majority (>98%) is bound to one of six **IGF-binding proteins (IGFBPs)**, of which IGFBP-3 is quantitatively dominant [3, mechanism_review]. IGFBP-3 accounts for 75–90% of all circulating IGF-1 binding [3, mechanism_review].

The key structural arrangement is the **150 kDa ternary complex**: one molecule each of IGF-1, IGFBP-3, and the **acid-labile subunit (ALS)** — a GH-dependent glycoprotein produced by the liver — associate non-covalently into this high-molecular-weight complex [3, mechanism_review]. The functional consequences are significant:

- The ternary complex is too large (~150 kDa) to readily traverse capillary walls, effectively **sequestering IGF-1 within the vasculature** and creating a circulating reservoir.
- ALS stabilizes the IGF-1/IGFBP-3 binary pair, dramatically extending IGF-1 half-life from roughly 10 minutes (free form) to 12–15 hours (ternary complex) [2, mechanism_review].
- Only IGF-1 released from the complex — the small free fraction — is immediately bioavailable to bind tissue IGF-1 receptors.

The physiological importance of ALS is underscored by human genetics: inactivating mutations of the *IGFALS* gene cause a syndrome of severely reduced circulating IGF-1 and IGFBP-3, growth retardation, and delayed puberty, confirming that the ternary complex is not merely a passive carrier but an essential determinant of IGF-1 bioavailability [4, cohort].

### Biological Actions of IGF-1

IGF-1 exerts its effects by binding the **IGF-1 receptor (IGF-1R)**, a transmembrane tyrosine kinase that activates two principal downstream cascades: the PI3K/AKT pathway (promoting cell survival, protein synthesis, and glucose uptake) and the MAPK/ERK pathway (promoting cell proliferation) [2, mechanism_review]. The net biological profile is:

- **Anabolic / growth-promoting:** stimulates protein synthesis, promotes positive nitrogen balance, increases lean body mass.
- **Mitogenic / anti-apoptotic:** drives cell cycle entry and suppresses programmed cell death in many tissues.
- **Insulin-like metabolic effects:** at sufficiently high concentrations, IGF-1 activates insulin receptors, enhancing glucose uptake — clinically relevant in conditions of IGF-1 excess.

The most consequential growth-promoting action is **longitudinal bone elongation at the epiphyseal growth plate**. GH stimulates resting chondrocytes in the growth plate, while both circulating (endocrine) IGF-1 and locally produced (paracrine) IGF-1 drive chondrocyte proliferation in the proliferative zone and hypertrophy in the terminal zone [7, mechanism_review]. Disruption of chondrocyte-specific IGF-1 signaling in animal models causes significant reductions in postnatal body length, confirming that local IGF-1 — not solely hepatic IGF-1 — is required for normal linear growth [7, mechanism_review].

### The Age Trajectory: Puberty Peak to Somatopause

IGF-1 levels follow a characteristic lifespan curve:

- **Infancy / early childhood:** relatively low levels, with GH-independent growth dominating in the neonatal period.
- **Puberty:** IGF-1 rises dramatically, driven by the convergence of increasing GH pulse amplitude (amplified by sex steroids) and robust hepatic GH receptor expression. This pubertal surge mediates the adolescent growth spurt and peak bone accrual.
- **Adulthood:** levels plateau and then begin a progressive, decades-long decline.
- **Aging ("somatopause"):** by the sixth decade and beyond, IGF-1 levels may fall to values resembling those seen in adult GH deficiency — a phenomenon termed the **somatopause** [8, mechanism_review]. The primary driver is declining hypothalamic GHRH output with consequent attenuation of GH pulse amplitude and frequency, not a failure of hepatic IGF-1 production per se.

The somatopause is associated with reduced lean mass, increased visceral fat, and impaired physical function — a body composition phenotype that overlaps substantially with classical adult GH deficiency. However, the longevity literature adds a counterintuitive dimension: reduced GH/IGF-1 signaling has been associated with extended lifespan in multiple animal models, suggesting that the relationship between the somatotropic axis and healthy aging is not simply one of decline to be corrected [8, mechanism_review].

Because IGF-1 levels are strongly age-dependent throughout life, **all clinical interpretation requires comparison to age- and sex-matched reference ranges** for the specific immunoassay used [5, regulatory].

---

## Reference Ranges, Units & Thresholds

### The Central Principle: IGF-1 Is Uninterpretable Without Age

IGF-1 rises steeply during childhood, peaks at puberty (around age 15), then declines continuously through adulthood into old age. A single number means nothing without knowing the patient's age. A reading of 150 ng/mL is reassuring in a 70-year-old but suggests significant GH insufficiency in a healthy 17-year-old at peak puberty. This age-dependence is not a minor caveat — it is the defining feature of IGF-1 interpretation, and clinicians, lab reports, and calculators that present a single adult reference range are providing clinically misleading information.

Sex also matters, though to a lesser degree: across the lifespan, women tend to have modestly lower mean IGF-1 concentrations than age-matched men [9, cohort].

### Units

IGF-1 is reported in **ng/mL** (nanograms per milliliter) or **µg/L** (micrograms per liter). These are numerically identical (1 ng/mL = 1 µg/L); this document uses ng/mL throughout.

### The Preferred Metric: Age- and Sex-Normalized SDS

Because the reference interval shifts substantially with every decade of life, the gold standard for interpreting IGF-1 is the **standard deviation score (SDS)**, also called the z-score: how many standard deviations above or below the age- and sex-matched population mean a given value sits.

Bidlingmaier et al. (2014) established this framework rigorously in a multicenter normative cohort of 15,014 subjects aged 0–94 years across the US, Canada, and Europe, using the IDS-iSYS automated chemiluminescence assay [9, cohort]. The study derived age- and sex-adjusted reference intervals conforming to international consensus standards, with SDS as the preferred output. An SDS of 0 means exactly average for that age/sex; an SDS of +2 corresponds roughly to the 97.5th percentile for age; SDS below −2 corresponds to the 2.5th percentile. These SDS cutpoints are the thresholds used in diagnosis.

The LMS method — fitting a Box-Cox power (lambda), median (M), and coefficient of variation (S) as smooth functions of age — allows continuous SDS computation across the full age range, replacing coarse decade-based bins [10, cohort]. Online and mobile calculators implementing this transform are available for specific assay platforms.

### Representative Age-Banded Reference Ranges (ng/mL)

**Critical caveat before reading these numbers:** reference intervals are assay-specific. The values below are from two large published normative studies using common immunoassay platforms and should not be applied to results from a different assay without using that assay's own reference data [10, cohort; 11, cohort].

**Puberty (peak around age 14–16):**
Concentrations reach their lifetime maximum. Values can readily exceed 400–600 ng/mL; the 97.5th percentile for a 15-year-old male on the IMMULITE platform is above 700 ng/mL [11, cohort].

**Young adults (18–20 years), 2.5–97.5th percentile:**
- Males (iSYS platform): ~168–391 ng/mL
- Females (iSYS platform): ~155–421 ng/mL [11, cohort]

**Mid-adulthood (30–39 years), 2.5–97.5th percentile:**
- Males (iSYS): ~108–265 ng/mL
- Females (iSYS): ~113–294 ng/mL [11, cohort]

**Late adulthood (70–89 years), 2.5–97.5th percentile:**
- Males (iSYS): ~64–192 ng/mL
- Females (iSYS): ~56–154 ng/mL [11, cohort]

Across the VARIETE adult cohort (911 subjects, ages 18–90), assay-specific medians tracked the same trajectory: a median of ~374 ng/mL at age 18 declining to ~180 ng/mL by ages 35–39 and ~93 ng/mL in those older than 70, with the sharpest fall between ages 21 and 50 [10, cohort]. Upper limits varied markedly across the six immunoassays compared, while lower limits were more concordant — reinforcing that the upper bound is the clinically critical moving target that must be derived from each platform's own normative dataset [11, cohort].

### Diagnostic Uses

**Acromegaly / GH excess**

Elevated IGF-1 is the recommended first-line biochemical screening test for acromegaly [5, regulatory]. Unlike growth hormone itself — which is secreted in brief, irregular pulses and is highly variable even within a single day — IGF-1 reflects the integrated GH output of the preceding days. A single random GH measurement is therefore an unreliable diagnostic proxy; IGF-1 is not [5, regulatory].

The Endocrine Society Clinical Practice Guideline (Katznelson et al., 2014) recommends measuring IGF-1 in any patient presenting with typical features of acromegaly (Grade 1|⊕⊕⊕○ — strong recommendation, moderate evidence) [5, regulatory]. A normal age-matched IGF-1 effectively excludes the diagnosis. An elevated value requires confirmation by an oral glucose tolerance test (OGTT) with GH measurement: in healthy individuals, GH suppresses below 1 µg/L following a 75 g glucose load; failure to suppress confirms autonomous GH excess.

The guideline does not specify a single numeric cutpoint for "elevated" IGF-1 [5, regulatory]. Elevation is defined as an IGF-1 SDS above +2 (approximately the 97.5th percentile for age and sex) — reinforcing why age-normalization is not optional.

**Growth hormone deficiency (GHD)**

In GHD, IGF-1 is typically low, but a low-normal or even normal IGF-1 does **not** exclude the diagnosis. In adults with suspected GHD, a subnormal IGF-1 is supportive evidence, but confirmation requires dynamic GH stimulation testing (e.g., insulin tolerance test or glucagon stimulation test), except in patients with established genetic or structural pituitary lesions documented from childhood [12, regulatory]. Normal IGF-1 has limited negative predictive value for ruling out adult GHD, particularly in the elderly — where age-related decline makes distinguishing GHD from normal aging based on IGF-1 alone unreliable.

**Monitoring GH therapy and acromegaly treatment**

IGF-1 is the preferred tool for monitoring both GH replacement in GHD and somatostatin analogue therapy in acromegaly. The target in both contexts is an IGF-1 within the age- and sex-specific normal range (SDS between approximately −2 and +2) — not a single fixed number [5, regulatory; 12, regulatory]. In GH replacement, over-treatment (supra-normal IGF-1) carries its own concerns; in acromegaly treatment, under-treatment (persistently elevated IGF-1) indicates inadequate biochemical control.

### Summary: No Universal Cutpoint

There is no single IGF-1 value that is "normal" across all ages. Reporting and interpreting IGF-1 without simultaneous age and sex normalization — ideally as an SDS against the same assay's reference population — is insufficient for clinical decision-making. Every diagnostic and therapeutic threshold is defined relative to the age-normal range for the specific assay used.

---

## Measurement & Standardization

### The Assay Challenge: IGFBP Interference

More than 90% of circulating IGF-1 travels as part of a ternary complex — bound to IGFBP-3 and an acid-labile subunit (ALS). The remaining fraction binds to other IGFBPs (principally IGFBP-1 and IGFBP-2). This pervasive binding creates the central technical problem in IGF-1 measurement: the binding proteins occlude the antibody epitopes required for immunoassay recognition, a phenomenon called IGFBP interference [13, mechanism_review].

Early radioimmunoassays did not include a protein dissociation step. Results were therefore substantially affected by the IGFBP milieu, which varies with age, nutritional status, and disease state — meaning two patients with identical true IGF-1 concentrations could yield different assay readings depending on their IGFBP-3 levels alone. Modern assays address this by dissociating IGF-1 from its binding proteins before measurement [14, mechanism_review].

The two dominant dissociation strategies are:

- **Acid-ethanol extraction**: serum is acidified (typically to pH ~2.0) and precipitated with ethanol, denaturing the binding proteins and releasing IGF-1. After neutralization, the extracted supernatant is assayed. This approach is the historical workhorse and remains widely used for its relative simplicity [14, mechanism_review].
- **Acid dissociation followed by IGF-II excess**: large molar excess of IGF-II is added after acidification, competitively displacing IGF-1 from residual IGFBP binding sites before assay reading. This approach is used in some automated two-site sandwich immunoassays [13, mechanism_review].

Neither method is perfect. Residual IGFBP carryover remains a documented interference source if the dissociation is incomplete, particularly at high IGFBP-3 concentrations. Lot-to-lot calibrator variability and internal standard losses during extraction add further scatter.

### Standardization and Harmonization

Recognizing that inter-laboratory IGF-1 values were clinically non-comparable, the international community established formal standardization infrastructure. The **WHO First International Standard for IGF-1 (coded 02/254)** — a recombinant human preparation with an assigned content of 8.50 µg per ampoule — was developed and calibrated through an international collaborative study and adopted as the common calibration anchor for immunoassays [15, regulatory].

A landmark consensus statement from Clemmons (2011, *Clinical Chemistry*), convened under the auspices of the Growth Hormone Research Society, the IGF Society, and the IFCC, formalized recommendations for IGF-1 assay standardization and evaluation [16, mechanism_review]. Key recommendations included: calibrating assays against the WHO IS 02/254, validating extraction efficiency, establishing large age- and sex-matched normative datasets using the specific assay, and reporting results as an age-normalized SDS alongside absolute concentration in ng/mL.

Despite adoption of a common calibrator, inter-assay variation remains clinically significant. A six-immunoassay comparison in 911 healthy adults found that while lower reference limits were broadly similar, upper limits varied markedly between platforms — meaning whether a patient's IGF-1 is "elevated" depends substantially on which commercial assay performs the measurement, and results are not transferable between platforms even when both nominally trace to the WHO standard [11, cohort].

### LC-MS/MS and the Emerging Method Landscape

Liquid chromatography-tandem mass spectrometry (LC-MS/MS) has emerged as an alternative to immunoassay. Mass spectrometry avoids antibody epitope dependence and IGFBP interference by measuring tryptic peptides or intact IGF-1 directly by mass. In principle, this provides higher specificity and enables traceability to pure reference material independent of matrix effects [14, mechanism_review].

In practice, harmonization of LC-MS/MS assays requires alignment to both the WHO IS 02/254 and NIST reference standards. A multi-laboratory study of intact IGF-1 measurement by mass spectrometry found intra-laboratory variability of 2–4% CV but inter-laboratory variability of 14.5% CV — comparable in magnitude to the immunoassay problem [18, cohort]. A subsequent study showed that when LC-MS/MS methods are carefully traceable to both NIST and WHO standards, strong inter-laboratory agreement (R² > 0.93) is achievable, enabling reference interval sharing between laboratories — a step immunoassays have not matched [17, cohort]. LC-MS/MS remains a specialist method not yet in routine clinical use, but its traceability properties make it the method toward which the field is moving.

### Serial Monitoring and the SDS Requirement

Because absolute IGF-1 concentrations differ systematically between assay platforms, the Clemmons/Bidlingmaier consensus is unambiguous: **serial monitoring must use the same assay and its own matched age-sex reference population** [13, mechanism_review]. Results expressed as SDS (z-scores vs. the assay's own normative dataset) are more portable than absolute ng/mL values across age but are still not portable across assay platforms — the SDS denominator (the normative SD) is itself method-specific.

Cross-assay comparisons are unreliable. A patient whose IGF-1 is measured at one laboratory and then re-measured at a second laboratory using a different commercial platform may show a clinically meaningful apparent change that reflects only assay bias, not a biological shift. Treatment decisions — particularly in acromegaly or GH deficiency management — should not be made on a cross-platform basis without a parallel-measurement bridging study.

### Analytical Interferences Beyond IGFBP

Three additional interference categories are relevant:

- **Residual IGFBP carryover**: incomplete acid dissociation in individual samples can suppress immunoreactivity. High IGFBP-3 states (pregnancy, late-stage liver disease) are the primary risk contexts.
- **Heterophile antibodies**: patient immunoglobulins capable of cross-linking assay antibodies cause spuriously elevated readings. The mechanism is assay-agnostic; dilution studies or blocking tube confirmations are the standard diagnostic maneuver when results are inconsistent with clinical presentation.
- **Biotin**: supplemental biotin at very high concentrations (>100 ng/mL) can interfere with biotin-streptavidin capture immunoassays, producing falsely low IGF-1 results. Clinically significant interference has been documented for the IDS-iSYS platform at pharmacological biotin doses [19, cohort]; at typical dietary biotin intake, interference is negligible.

### Pre-Analytics: Stability and the Nutritional State Caveat

IGF-1 has a serum half-life of approximately 12–15 hours when bound in the ternary complex, and total serum IGF-1 shows **no clinically significant circadian variation** in healthy subjects [20, cohort]. This stability is a practical advantage: sampling time of day is not a material pre-analytical variable, unlike cortisol or GH. Serum is stable at room temperature for at least 48 hours and for months when frozen.

However, a critical biological qualifier applies. IGF-1 is produced predominantly by the liver in a GH-dependent, nutrition-dependent manner. Both caloric and protein availability govern hepatic IGF-1 gene expression and secretion rate; fasting and protein malnutrition suppress IGF-1 independently of GH status. This means that a low IGF-1 result in a patient with inadequate caloric or protein intake may reflect nutritional suppression rather than GH deficiency — and an elevated IGF-1 in a well-nourished state tells a different story than one in a malnourished patient. This is a biological determinant of circulating concentration, not an analytic artifact, and must be addressed in interpretation rather than pre-analytical protocol.

---

## Determinants & Clinical Significance

### D.1 High IGF-1: Acromegaly and Exogenous GH

The primary clinical use of serum IGF-1 is as the **screening and disease-activity biomarker for acromegaly** — GH excess from a pituitary somatotroph adenoma. Because IGF-1 reflects integrated GH secretion over hours-to-days (in contrast to the minute-to-minute pulsatile fluctuation of GH itself), a single IGF-1 measurement captures tonic GH exposure far more reliably than random GH. The 2014 Endocrine Society Clinical Practice Guideline (Katznelson et al.) recommends measuring serum IGF-1 — age-adjusted — as the initial screen in any patient with clinical features suggesting acromegaly (acral enlargement, facial coarsening, sleep apnoea, new-onset type 2 diabetes, debilitating arthritis, carpal tunnel syndrome, hyperhidrosis). A normal age-adjusted IGF-1 effectively excludes active acromegaly; an elevated result requires confirmatory oral glucose tolerance testing (GH nadir ≥1 µg/L confirms disease). The same guideline designates normalisation of age-adjusted IGF-1 as the primary biochemical treatment target [5, regulatory].

Exogenous GH administration (therapeutic or illicit) raises IGF-1 proportionally to dose and duration. This forms the basis of the GH Biomarkers anti-doping test (see §D.5).

### D.2 Low IGF-1: GH Deficiency — and the Non-GH Causes That Confound It

**GH deficiency (GHD)** is the second major clinical context for IGF-1. In children, low IGF-1 contributes to the diagnostic workup of growth failure; in adults, GHD — from pituitary adenoma, cranial irradiation, traumatic brain injury, or hypopituitarism — causes a syndrome of reduced lean mass, increased fat mass, dyslipidaemia, and impaired quality of life.

However, the critical interpretive caveat is that **low IGF-1 is not specific to GHD.** The 2011 Endocrine Society guideline on adult GHD (Molitch, Clemmons, Malozowski, Merriam, and Vance) states explicitly that a low IGF-1 cannot serve as a stand-alone diagnostic test: a normal IGF-1 does not exclude GHD (stimulation testing remains mandatory), and multiple non-GH conditions suppress IGF-1 independently [12, regulatory]:

- **Malnutrition, fasting, anorexia nervosa** — protein-energy deficit blunts hepatic IGF-1 synthesis directly; IGF-1 falls acutely during caloric restriction even when GH is normal or elevated (a state of GH resistance).
- **Liver disease / cirrhosis** — because IGF-1 is synthesised predominantly in hepatocytes, hepatic insufficiency depresses IGF-1 regardless of GH status.
- **Poorly controlled type 1 or type 2 diabetes** — chronic hyperglycaemia and insulinopaenia reduce hepatic IGF-1 production (insulin is permissive for hepatic GH signalling).
- **Hypothyroidism** — thyroid hormone is required for normal GH secretion and for hepatic IGF-1 production; hypothyroid patients can present with low IGF-1 that corrects on thyroxine replacement.
- **Oral oestrogen** — exogenous oestrogen administered orally (but not transdermally) induces hepatic GH resistance, reducing IGF-1 by 30–50% at typical contraceptive or HRT doses. This is a first-pass hepatic effect absent with transdermal or parenteral oestrogen.
- **Aging (somatopause)** — IGF-1 declines progressively from the third decade onward; by the seventh decade, many healthy adults have IGF-1 levels that would fall in the "low" range of younger reference intervals. This makes age-matched reference ranges mandatory.
- **Systemic illness / catabolism** — sepsis, major surgery, burns, and cancer cachexia suppress IGF-1 as part of the catabolic response.

In practice, any patient with a low IGF-1 who has potentially confounding factors (nutritional deficit, liver disease, diabetes, oral oestrogen use) requires those conditions to be corrected or accounted for before interpreting IGF-1 in the context of GH axis assessment. Stimulation testing (insulin tolerance test or GHRH-arginine test) remains the diagnostic standard for GHD.

### D.3 The GH/IGF-1 and Longevity Paradox

A well-documented and genuinely unresolved tension runs through the IGF-1 literature: **the same GH/IGF-1 axis that drives growth, anabolism, and tissue repair in youth appears to accelerate aging and disease at sustained elevations.**

**Model-organism evidence (animal — not human-proven):** Reduced insulin/IGF-1 signalling extends lifespan in *C. elegans*, *Drosophila melanogaster*, and multiple mouse strains with GH receptor deletion or GH deficiency. Ames and Snell dwarf mice are substantially longer-lived than controls (animal — not human-proven). These findings are consistent and mechanistically well-characterised (reduced mTORC1, enhanced stress resistance, lower oxidative damage), but the magnitude of the effect does not translate directly to humans, and the relevance of nematode/fly longevity pathways to human aging remains a subject of active investigation.

**The Ecuadorian Laron syndrome cohort — a human experiment of nature:** The most striking human data come from Guevara-Aguirre and colleagues, who followed ~90 GH-receptor-deficient subjects with Laron syndrome (loss-of-function mutations in the GH receptor gene, causing severe GH resistance and very low circulating IGF-1) for 22 years. Compared with unaffected relatives of similar genetic background and lifestyle, the Laron cohort showed only one non-lethal malignancy (versus ~17% cancer prevalence in controls) and zero cases of type 2 diabetes (versus ~5% in controls). The GHR-deficient individuals showed substantially lower fasting insulin (1.4 versus 4.4 µU/mL) and markedly reduced pro-aging signalling markers [21, cohort].

**How to read this evidence honestly:** The Laron cohort is small, geographically isolated, and reflects a monogenic extreme (GHR absence) rather than normal IGF-1 variation. Laron individuals are also severely short-statured and have multiple metabolic differences. The finding does not imply that lowering IGF-1 within the normal range in healthy adults extends human lifespan or prevents cancer — that inference would be unwarranted. What the data establish is that profoundly reduced GH/IGF-1 signalling, from birth, is compatible with remarkable disease protection in this population, confirming the importance of this pathway in cancer and metabolic biology. The translation to normal-range optimisation in health-tracking contexts is unproven.

### D.4 U-Shaped Associations: Cancer and Cardiovascular Risk

The epidemiological risk landscape for IGF-1 is U-shaped: both extremes associate with adverse outcomes, though through different mechanisms.

**High IGF-1 and cancer risk.** The Endogenous Hormones and Breast Cancer Collaborative Group performed a pooled individual-data analysis of 17 prospective studies including nearly 10,000 women. Higher circulating IGF-1 was positively associated with breast cancer risk; women in the highest IGF-1 quintile had a 28% higher risk than those in the lowest quintile, with a stronger association for oestrogen receptor-positive tumours [22, meta_analysis].

For prostate cancer, Travis, Appleby, Martin, Holly, Albanes et al. conducted an individual participant data meta-analysis of 19 studies (10,554 cases, 13,618 controls). IGF-I showed a clear positive association: OR 1.29 (95% CI 1.16–1.43) for highest versus lowest quintile in prospective studies [23, meta_analysis]. Colorectal cancer associations have been reported in independent analyses. These associations are epidemiological and largely observational; residual confounding, reverse causation, and the complexity of IGF-1 biology (IGF-1 is both mitogenic and anti-apoptotic) make causal inference difficult. Mendelian randomisation studies have provided partial causal support for the breast and prostate associations, but the clinical implications for normal-range IGF-1 optimisation remain unclear.

**Low IGF-1 and cardiovascular/mortality risk.** In older adults the picture inverts. Laughlin, Barrett-Connor, Criqui, and Kritz-Silverstein, in the Rancho Bernardo prospective cohort (N=1,185; mean age 74; 9–13-year follow-up), found that ischemic heart disease mortality risk was 38% higher for every 40 ng/mL decrease in IGF-1, persisting after adjustment for established cardiovascular risk factors [24, cohort].

Across the literature, a meta-analysis of 19 prospective cohort studies (N=30,876) by Rahmani, Montesanto, Giovannucci, Zand et al. confirmed the U-shaped pattern: low IGF-1 (versus mid-range) carried HR 1.33 (95% CI 1.14–1.57) for all-cause mortality, and high IGF-1 (versus mid-range) HR 1.23 (95% CI 1.06–1.44), with the 120–160 ng/mL range associated with lowest mortality risk [25, meta_analysis]. These are associational findings in largely elderly populations; frailty, illness, and malnutrition causally lower IGF-1 (reverse causation), which confounds the low-IGF-1 arm substantially.

### D.5 GH Doping and Anti-Doping Detection

Exogenous recombinant human GH (rhGH) is abused in sport for its anabolic and lipolytic effects. Because the isoform-based GH detection test has a short window (12–24 hours post-dose), the World Anti-Doping Agency (WADA) employs a parallel **GH Biomarkers Test** using two GH-responsive analytes: **IGF-1** (reflecting hepatic GH action, peaking ~2 weeks post-administration) and **P-III-NP** (N-terminal propeptide of procollagen type III, reflecting GH-dependent connective-tissue synthesis, peaking at 4–6 weeks). The combination extends the detection window to approximately 2 weeks post-dose for IGF-1 and longer for P-III-NP. Erotokritou-Mulligan et al. validated the intra-individual variability of these markers across 381 athletes, finding IGF-1 variability of 14–16%, supporting a longitudinal athlete biological passport approach over single-time-point thresholds [26, cohort].

### D.6 Determinants Summary

| Direction | Cause |
|-----------|-------|
| **Raises IGF-1** | GH-secreting pituitary adenoma (acromegaly); exogenous GH therapy or abuse; puberty (peak in adolescence); adequate caloric and protein intake; insulin (permissive hepatic effect); sex steroids (non-oral routes) |
| **Lowers IGF-1** | GH deficiency (pituitary/hypothalamic disease); malnutrition, prolonged fasting, anorexia nervosa; liver disease / cirrhosis; poorly controlled diabetes; hypothyroidism; oral oestrogen; aging (somatopause); acute/chronic systemic illness |

### D.7 Key Interpretive Limitations

1. **Age-SDS is mandatory.** IGF-1 peaks in mid-adolescence and declines progressively throughout adult life. A value of 100 ng/mL may be normal for a 70-year-old and severely deficient for a 20-year-old. Results must always be interpreted against age- and sex-matched reference intervals from the specific assay used.

2. **Assay non-standardisation.** There is no universal IGF-1 assay standard. Reference ranges differ substantially between platforms; numeric values from different assays should not be directly compared. Serial monitoring of any individual should use the same assay throughout.

3. **Nutritional and hepatic confounding.** A low IGF-1 in a malnourished or cirrhotic patient reflects that pathology, not GHD. Clinicians must account for nutritional status, liver function, diabetes control, and oestrogen use before attributing a low IGF-1 to GH axis disease.

4. **A single value requires context.** Dynamic testing (stimulation for GHD, OGTT suppression for acromegaly) remains the diagnostic standard. IGF-1 is the screen, not the verdict.

---

## Bibliography

[1]. Laron Z. Insulin-like growth factor 1 (IGF-1): a growth hormone. *Mol Pathol*. 2001;54(5):311–316. PMID: 11577173. — tag: mechanism_review — tier: 2

[2]. Al-Samerria S, Radovick S. The Role of Insulin-like Growth Factor-1 (IGF-1) in the Control of Neuroendocrine Regulation of Growth. *Cells*. 2021;10(10):2664. PMID: 34685644. DOI: 10.3390/cells10102664. — tag: mechanism_review — tier: 1

[3]. Jogie-Brahim S, Feldman D, Oh Y. Unraveling Insulin-Like Growth Factor Binding Protein-3 Actions in Human Disease. *Endocr Rev*. 2009;30(5):417–437. PMID: 19477944. DOI: 10.1210/er.2008-0028. — tag: mechanism_review — tier: 1

[4]. Domené HM, Bengolea SV, Martínez AS, Ropelato MG, Pennisi P, Scaglia P, Heinrich JJ, Jasper HG. Deficiency of the circulating insulin-like growth factor system associated with inactivation of the acid-labile subunit gene. *N Engl J Med*. 2004;350(6):570–577. PMID: 14762184. DOI: 10.1056/NEJMoa013100. — tag: cohort — tier: 1

[5]. Katznelson L, Laws ER Jr, Melmed S, Molitch ME, Murad MH, Utz A, Wass JAH. Acromegaly: an Endocrine Society clinical practice guideline. *J Clin Endocrinol Metab*. 2014;99(11):3933–3951. PMID: 25356808. DOI: 10.1210/jc.2014-2700. — tag: regulatory — tier: 2

[6]. Faje AT, Barkan AL. Basal, but not pulsatile, growth hormone secretion determines the ambient circulating levels of insulin-like growth factor-I. *J Clin Endocrinol Metab*. 2010;95(5):2486–2491. PMID: 20190159. — tag: cohort — tier: 1

[7]. Racine HL, Serrat MA. The Actions of IGF-1 in the Growth Plate and its Role in Postnatal Bone Elongation. *Curr Osteoporos Rep*. 2020;18(3):210–227. PMID: 32415542. DOI: 10.1007/s11914-020-00570-x. — tag: mechanism_review — tier: 1

[8]. Junnila RK, List EO, Berryman DE, Murrey JW, Kopchick JJ. The GH/IGF-1 axis in ageing and longevity. *Nat Rev Endocrinol*. 2013;9(6):366–376. PMID: 23591370. DOI: 10.1038/nrendo.2013.67. — tag: mechanism_review — tier: 1

[9]. Bidlingmaier M, Friedrich N, Emeny RT, Spranger J, Wolthers OD, Roswall J, Körner A, Obermayer-Pietsch B, Hübener C, Dahlgren J, Frystyk J, Pfeiffer AFH, Doering A, Bielohuby M, Wallaschofski H, Arafat AM. Reference intervals for insulin-like growth factor-1 (IGF-I) from birth to senescence: results from a multicenter study using a new automated chemiluminescence IGF-I immunoassay conforming to recent international recommendations. *J Clin Endocrinol Metab*. 2014;99(5):1712–1721. PMID: 24606072. DOI: 10.1210/jc.2013-3059. — tag: cohort — tier: 1

[10]. Sabbah N, Wolf P, Piedvache C, Trabado S, Verdelet T, Cornu C, Souberbielle JC, Chanson P; VARIETE Investigators. Reference values for IGF-I serum concentration in an adult population: use of the VARIETE cohort for two new immunoassays. *Endocr Connect*. 2021;10(9):1027–1034. PMID: 34343107. DOI: 10.1530/EC-21-0175. — tag: cohort — tier: 1

[11]. Chanson P, Arnoux A, Mavromati M, Brailly-Tabard S, Massart C, Young J, Piketty ML, Souberbielle JC; VARIETE Investigators. Reference values for IGF-I serum concentrations: comparison of six immunoassays. *J Clin Endocrinol Metab*. 2016;101(9):3450–3458. PMID: 27167056. DOI: 10.1210/jc.2016-1257. — tag: cohort — tier: 1

[12]. Molitch ME, Clemmons DR, Malozowski S, Merriam GR, Vance ML. Evaluation and treatment of adult growth hormone deficiency: an Endocrine Society clinical practice guideline. *J Clin Endocrinol Metab*. 2011;96(6):1587–1609. PMID: 21602453. — tag: regulatory — tier: 2

[13]. Clemmons DR, Bidlingmaier M. IGF-I assay methods and biologic variability: evaluation of acromegaly treatment response. *Eur J Endocrinol*. 2024;191(1):R1–R8. PMID: 38916798. DOI: 10.1093/ejendo/lvae065. — tag: mechanism_review — tier: 1

[14]. Ketha H, Singh RJ. Clinical assays for quantitation of insulin-like-growth-factor-1 (IGF1). *Methods*. 2015;81:93–98. PMID: 25937392. DOI: 10.1016/j.ymeth.2015.04.029. — tag: mechanism_review — tier: 1

[15]. Burns C, Rigsby P, Moore M, Rafferty B. The First International Standard for Insulin-like Growth Factor-1 (IGF-1) for immunoassay: preparation and calibration in an international collaborative study. *Growth Horm IGF Res*. 2009;19(5):457–462. PMID: 19303800. DOI: 10.1016/j.ghir.2009.02.002. — tag: regulatory — tier: 1

[16]. Clemmons DR. Consensus statement on the standardization and evaluation of growth hormone and insulin-like growth factor assays. *Clin Chem*. 2011;57(4):555–559. PMID: 21285256. DOI: 10.1373/clinchem.2010.150631. — tag: mechanism_review — tier: 1

[17]. Ezra S, Winstone TML, Singh R, Orton DJ. Agreement of LC-MS assays for IGF-1 traceable to NIST and WHO standards permits harmonization of reference intervals between laboratories. *Clin Biochem*. 2023;116:75–78. PMID: 37031902. DOI: 10.1016/j.clinbiochem.2023.04.002. — tag: cohort — tier: 1

[18]. Moncrieffe D, Cox HD, Carletta S, Becker JO, Thomas A, Eichner D, Ahrens B, Thevis M, Bowers LD, Cowan DA, Hoofnagle AN. Inter-laboratory agreement of insulin-like growth factor 1 concentrations measured intact by mass spectrometry. *Clin Chem*. 2020;66(4):579–586. DOI: 10.1093/clinchem/hvaa043. — tag: cohort — tier: 1

[19]. Knudsen CS, Adelborg K, Søndergaard E, Parkner T. Biotin interference in routine IDS-iSYS immunoassays for aldosterone, renin, insulin-like growth factor 1, growth hormone and bone alkaline phosphatase. *Scand J Clin Lab Invest*. 2022;82(1):6–11. PMID: 34859720. DOI: 10.1080/00365513.2021.2003854. — tag: cohort — tier: 1

[20]. Skjaerbaek C, Frystyk J, Kaal A, Laursen T, Møller J, Weeke J, Jørgensen JO, Sandahl Christiansen J, Orskov H. Circadian variation in serum free and total insulin-like growth factor (IGF)-I and IGF-II in untreated and treated acromegaly and growth hormone deficiency. *Clin Endocrinol (Oxf)*. 2000;52:25–33. PMID: 10651750. DOI: 10.1046/j.1365-2265.2000.00876.x. — tag: cohort — tier: 1

[21]. Guevara-Aguirre J, Balasubramanian P, Guevara-Aguirre M, Wei M, Madia F, Cheng CW, Hwang D, Martin-Montalvo A, Saavedra J, Ingles S, de Cabo R, Cohen P, Longo VD. Growth hormone receptor deficiency is associated with a major reduction in pro-aging signaling, cancer, and diabetes in humans. *Sci Transl Med*. 2011;3(70):70ra13. PMID: 21325617. — tag: cohort — tier: 1

[22]. Endogenous Hormones and Breast Cancer Collaborative Group; Key TJ, Appleby PN, Reeves GK, Roddam AW, et al. Insulin-like growth factor 1 (IGF1), IGF binding protein 3 (IGFBP3), and breast cancer risk: pooled individual data analysis of 17 prospective studies. *Lancet Oncol*. 2010;11(6):530–542. PMID: 20472501. — tag: meta_analysis — tier: 1

[23]. Travis RC, Appleby PN, Martin RM, Holly JMP, Albanes D, Black A, Bueno-de-Mesquita HB, Chan JM, Chen C, Chirlaque MD, Cook MB, Deschasaux M, Donovan JL, Ferrucci L, Galan P, Giles GG, Giovannucci EL, Gunter MJ, Habel LA, Hamdy FC, Helzlsouer KJ, Hercberg S, Hoover RN, Janssen JAMJL, Kaaks R, Kubo T, Le Marchand L, Metter EJ, Mikami K, Morris JK, Neal DE, Neuhouser ML, Ozasa K, Palli D, Platz EA, Pollak M, Price AJ, Roobol MJ, Schaefer C, Schenk JM, Severi G, Stampfer MJ, Stattin P, Tamakoshi A, Tangen CM, Touvier M, Wald NJ, Weiss NS, Ziegler RG, Key TJ, Allen NE. A meta-analysis of individual participant data reveals an association between circulating levels of IGF-I and prostate cancer risk. *Cancer Res*. 2016;76(8):2288–2300. PMID: 26921328. — tag: meta_analysis — tier: 1

[24]. Laughlin GA, Barrett-Connor E, Criqui MH, Kritz-Silverstein D. The prospective association of serum insulin-like growth factor I (IGF-I) and IGF-binding protein-1 levels with all cause and cardiovascular disease mortality in older adults: the Rancho Bernardo Study. *J Clin Endocrinol Metab*. 2004;89(1):114–120. PMID: 14715837. — tag: cohort — tier: 1

[25]. Rahmani J, Montesanto A, Giovannucci E, Zand H, Barati M, Kopchick JJ, Mirisola MG, Lagani V, Bawadi H, Vardavas R, Laviano A, Christensen K, Passarino G, Longo VD. Association between IGF-1 levels ranges and all-cause mortality: a meta-analysis. *Aging Cell*. 2022;21(2):e13540. PMID: 35048526. — tag: meta_analysis — tier: 1

[26]. Erotokritou-Mulligan I, Bassett EE, Cowan DA, Bartlett C, Milward P, Sartorio A, Sönksen PH, Holt RIG. The use of growth hormone (GH)-dependent markers in the detection of GH abuse in sport: physiological intra-individual variation of IGF-I, type 3 pro-collagen (P-III-P) and the GH-2000 detection score. *Clin Endocrinol (Oxf)*. 2010;72(4):520–526. PMID: 19650783. — tag: cohort — tier: 1
