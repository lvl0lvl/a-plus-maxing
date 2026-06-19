# Section B: Reference Ranges, Units & Indices

## B.1 The Fundamental Caveat: No Harmonized Diagnostic Cutpoint

Fasting insulin has no universally agreed diagnostic threshold — a fact that is load-bearing for every number that follows in this section. Unlike HbA1c or fasting glucose, which benefit from decades of assay-harmonization efforts anchored to clinical outcome data, fasting insulin values are both **assay-dependent** and **population-dependent**. A result of 10 µIU/mL on one platform does not mean the same thing as 10 µIU/mL on another, and a reference interval derived from a healthy Brazilian cohort does not automatically apply to a South Asian population at matched BMI. Treating any single number from the ranges below as a validated diagnostic cutpoint is a misuse of this biomarker.

---

## B.2 Units and Conversion

Clinical reports use two unit systems:

- **µIU/mL** (also written mU/L or µU/mL — these are numerically equivalent) is the dominant convention in North American laboratories.
- **pmol/L** is preferred in many European and international contexts.

**Conversion factor:** The WHO-recommended conversion is **1 µIU/mL = 6.00 pmol/L** [1, mechanism_review]. An older international standard uses **6.945**, derived from the specific activity of the earlier insulin reference preparation; this factor is still encountered in some published equations and older assay calibrations [2, mechanism_review]. The difference is ~15% — enough to shift a borderline value across an interpretive category — so when comparing values across publications or platforms, confirm which conversion factor the source used.

Throughout this entry, insulin is expressed in **µIU/mL with pmol/L equivalents in parentheses** using the 6.00 factor unless otherwise noted.

---

## B.3 Adult Fasting Insulin Reference Ranges

Laboratory reference ranges for fasting insulin are wide and assay-specific. A commonly cited broad range in adult clinical practice is approximately **2–25 µIU/mL (12–150 pmol/L)**, though the upper bound varies substantially across platforms. A large Brazilian database study (n = 21,684 healthy adults, BMI 18.5–24.9 kg/m², glucose < 100 mg/dL, HbA1c < 5.7%) using electrochemiluminescence immunoassay (ECLIA, Roche Cobas) derived intervals of:

- **Overall: 2.52–13.14 µIU/mL (15.1–78.8 pmol/L)**
- Women: 2.54–13.30 µIU/mL (15.2–79.8 pmol/L)
- Men: 2.43–11.89 µIU/mL (14.6–71.3 pmol/L)

These intervals were notably narrower than manufacturer-supplied ranges, illustrating how reference values anchored to a genuinely healthy, metabolically screened cohort differ from population averages [3, cohort].

A Nepalese study (n = 135 healthy adults, BMI 18.5–24.9 kg/m², chemiluminescence immunoassay) derived a reference interval of **2.63–14.56 µIU/mL** (median 7.69 µIU/mL), higher than the Brazilian data despite similar BMI screening — an instance of the "South Asian phenotype," where greater insulin secretion accompanies comparable glucose levels [4, cohort].

In NHANES samples of US adults (non-diabetic), mean fasting insulin has been reported at approximately **9.3 µIU/mL** (55.8 pmol/L), with the distribution right-skewed and typically log-transformed for statistical analyses [5, cohort]. The NHANES program itself applied cycle-to-cycle assay adjustment via regression equations to account for platform changes — a concrete illustration that raw insulin values are not directly comparable across assay generations [5, cohort].

### The "optimal" or "insulin-sensitive" framing

A lower fasting insulin in the context of normal glucose is a physiological marker of higher insulin sensitivity — a framing commonly used in functional medicine and metabolic health contexts. No specific numeric cutpoint for this "optimal" or "insulin-sensitive" range has been validated or adopted by any major regulatory body (ADA, IFCC, AACE), in part because of the assay standardization problem described below.

---

## B.4 Assay Dependency: Why Numbers Don't Transfer Across Labs

The American Diabetes Association Workgroup on Insulin Immunoassay Standardization evaluated 12 commercial insulin methods from 9 manufacturers and found:

- Within-assay CV: 3.7–39.0% (7 of 10 assays ≤ 10.6%)
- **Between-assay CV: 12–66%, median 24%**
- Only 6 of 10 assays met clinical acceptability (total error ≤ 32% based on biological variability criteria)
- A common reference preparation failed to reduce between-assay disagreement [2, mechanism_review]

A median between-assay CV of 24% means that two laboratories running the same sample could produce results differing by roughly one-quarter of the measured value under typical conditions. The primary sources of discordance include differing antibody specificity, variable cross-reactivity with proinsulin split forms (des(64,65) proinsulin cross-reacted at > 40% in 9 of 10 assays), and platform-specific calibration [2, mechanism_review]. This is the mechanistic reason no universal reference interval exists: the number a laboratory reports is inseparable from the assay it uses.

---

## B.5 Contextualizing Indices

Because a single fasting insulin value is hard to interpret without knowing the concurrent glucose level, several computed indices integrate both measurements to estimate insulin sensitivity or β-cell function.

### HOMA-IR (Homeostatic Model Assessment of Insulin Resistance)

**Formula:**

$$\text{HOMA-IR} = \frac{\text{Fasting insulin (µIU/mL)} \times \text{Fasting glucose (mg/dL)}}{405}$$

Equivalently, with glucose in mmol/L:

$$\text{HOMA-IR} = \frac{\text{Fasting insulin (µIU/mL)} \times \text{Fasting glucose (mmol/L)}}{22.5}$$

The denominator (405 or 22.5) normalizes the result so that a healthy lean individual with insulin ~5 µIU/mL and glucose ~81 mg/dL (4.5 mmol/L) yields HOMA-IR ≈ 1.0 [6, mechanism_review].

**Interpretation:** HOMA-IR < 1.0 is widely referenced as "optimal" insulin sensitivity. Values > 1.9 suggest early insulin resistance; values > 2.9 indicate significant insulin resistance in most frameworks [6, mechanism_review]. The Brazilian reference interval (screened healthy adults, ECLIA assay) was **0.39–2.86** overall, and the Nepalese study derived **0.56–3.50** using the classical HOMA1 model [3, cohort; 4, cohort]. The span across these two populations alone (~20% difference in upper bound) underscores the population-dependence of HOMA-IR cutpoints.

No HOMA-IR value has been universally validated as a clinical diagnostic threshold. In the ADA's "Use and Abuse of HOMA Modeling" article, the authors explicitly caution that threshold cutpoints depend on the assay platform used to measure insulin [6, mechanism_review].

### QUICKI (Quantitative Insulin Sensitivity Check Index)

**Formula:**

$$\text{QUICKI} = \frac{1}{\log(\text{Fasting insulin, µIU/mL}) + \log(\text{Fasting glucose, mg/dL})}$$

A higher QUICKI indicates greater insulin sensitivity. Validated against the hyperinsulinemic-euglycemic clamp, QUICKI demonstrated a correlation of r = 0.78 with directly measured insulin sensitivity — superior to the minimal model (r = 0.57) in the original validation study [7, cohort]. The Nepalese reference interval was **0.32–0.42**, consistent with Iranian and Korean reference data [4, cohort]. Values ≤ 0.30–0.33 are associated with insulin resistance in most published series, though, again, no universal cutpoint is recognized.

### HOMA-β (β-Cell Function)

**Formula:**

$$\text{HOMA-β (\%)} = \frac{20 \times \text{Fasting insulin (µIU/mL)}}{\text{Fasting glucose (mmol/L)} - 3.5}$$

HOMA-β estimates β-cell secretory capacity relative to a healthy young adult reference (100%) [6, mechanism_review]. A value ≥ 100% is considered normal function. HOMA-β is most useful longitudinally or in relative comparison, not as a standalone diagnostic number.

### Fasting Glucose-to-Insulin Ratio (FGIR)

**Formula:**

$$\text{FGIR} = \frac{\text{Fasting glucose (mg/dL)}}{\text{Fasting insulin (µIU/mL)}}$$

A higher ratio reflects better insulin sensitivity (glucose is controlled with less insulin). In girls with premature adrenarche, FGIR < 7 achieved 87% sensitivity and 89% specificity for insulin resistance [8, cohort]. In women with PCOS, FGIR < 4.5 performed better than HOMA-IR in one cohort [8, cohort]. Population-specific cutpoints vary; no universal adult threshold exists.

---

## B.6 Population Distribution Notes

Population-level insulin data carry the same assay caveat. In NHANES samples of non-diabetic US adults, mean fasting insulin approximates 9–10 µIU/mL with a right-skewed distribution [5, cohort]. The NHANES team standardized measurements by applying regression-based cross-calibration across assay cycles — meaning the published NHANES insulin values are not raw assay outputs but adjusted estimates, and they should not be used to validate absolute thresholds on other platforms [5, cohort].

South Asian adults demonstrate systematically higher fasting insulin levels than matched Caucasian controls at equivalent BMI and glucose, reflecting ethnic differences in insulin secretion and peripheral sensitivity that require ethnicity-specific reference intervals [4, cohort].

---

## Bibliography

1. Knopp JL, Holder-Pearson L, Chase JG. Insulin Units and Conversion Factors: A Story of Truth, Boots, and Faster Half-Truths. *J Diabetes Sci Technol*. 2019;13(3):609–611. PMID: 30318910; PMC: PMC6501531. — tag: mechanism_review — tier: 2
2. Staten MA et al. Standardization of Insulin Immunoassays: Report of the American Diabetes Association Workgroup. *Clin Chem.* 2007;53(4):711–716. https://academic.oup.com/clinchem/article/53/4/711/5627663 — tag: mechanism_review — tier: 2
3. de Queiroz Mello A et al. Proposal for fasting insulin and HOMA-IR reference intervals based on an extensive Brazilian laboratory database. *PMC11554367.* 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11554367/ — tag: cohort — tier: 1
4. Karki R et al. Reference intervals for fasting insulin and insulin-related indices in healthy adults: a cross-sectional study in Gandaki Province, Nepal. *PMC13007168.* 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC13007168/ — tag: cohort — tier: 1
5. Chooi YC et al. Physical Activity and Insulin Resistance in 6,500 NHANES Adults: The Role of Abdominal Obesity. *PMC7745049.* 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7745049/ — tag: cohort — tier: 1
6. Wallace TM, Levy JC, Matthews DR. Use and Abuse of HOMA Modeling. *Diabetes Care.* 2004;27(6):1487–1495. https://diabetesjournals.org/care/article/27/6/1487/22836/Use-and-Abuse-of-HOMA-Modeling — tag: mechanism_review — tier: 1
7. Katz A et al. Quantitative insulin sensitivity check index: a simple, accurate method for assessing insulin sensitivity in humans. *J Clin Endocrinol Metab.* 2000;85(7):2402–2410. https://pubmed.ncbi.nlm.nih.gov/10902785/ — tag: cohort — tier: 1
8. Legro RS, Finegood D, Dunaif A. Fasting Glucose to Insulin Ratio Is a Useful Measure of Insulin Sensitivity in Women with Polycystic Ovary Syndrome. *J Clin Endocrinol Metab.* 1998;83(8):2694–2698. https://academic.oup.com/jcem/article/83/8/2694/2660463 — tag: cohort — tier: 1
