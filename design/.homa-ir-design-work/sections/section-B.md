# Section B: Calculation, Units & Thresholds

## The HOMA1 Formula

The original Homeostasis Model Assessment was introduced by Matthews et al. in 1985 as a way to estimate insulin resistance from two routine fasting measurements [1, mechanism_review]. The HOMA1-IR formula, in its two equivalent forms, is:

**SI form (glucose in mmol/L):**
$$\text{HOMA1-IR} = \frac{\text{fasting insulin} \ (\mu\text{IU/mL}) \times \text{fasting glucose} \ (\text{mmol/L})}{22.5}$$

**Conventional form (glucose in mg/dL):**
$$\text{HOMA1-IR} = \frac{\text{fasting insulin} \ (\mu\text{IU/mL}) \times \text{fasting glucose} \ (\text{mg/dL})}{405}$$

These two expressions are algebraically identical. The conversion factor between mg/dL and mmol/L for glucose is 18.0 (1 mmol/L = 18.0 mg/dL), so 22.5 × 18.0 = 405. The denominator 22.5 is a normalization constant derived from the product of assumed normal fasting values: a fasting plasma insulin of 5 µIU/mL and a fasting plasma glucose of 4.5 mmol/L (5 × 4.5 = 22.5), which together represent the reference homeostatic state in the original 1985 model [1, mechanism_review]. A result of 1.0 therefore corresponds to a fasting state at the model's assumed normal reference point.

Both formulas require that both inputs be **fasting** values — typically drawn after a minimum 8-hour fast — because the HOMA model is derived from steady-state basal physiology. Using non-fasting glucose or insulin invalidates the calculation.

### Unit Conversions

Two unit conversions are encountered in practice:

- **Insulin:** 1 µIU/mL = 6.0 pmol/L (multiply µIU/mL by 6.0 to get pmol/L; divide pmol/L by 6.0 to recover µIU/mL)
- **Glucose:** 1 mmol/L = 18.0 mg/dL (divide mg/dL by 18.0 to get mmol/L)

These factors confirm the formula equivalence: substituting glucose mg/dL / 18.0 into the SI form gives (insulin × glucose_mg/dL / 18.0) / 22.5 = (insulin × glucose_mg/dL) / 405.

---

## HOMA2: The Updated Computer Model

HOMA1 uses a linear algebraic approximation of the original nonlinear physiological feedback equations. This approximation becomes increasingly inaccurate at extreme values of glucose (particularly >10 mmol/L / 180 mg/dL) and at high insulin concentrations. Levy, Matthews, and Hermans (1998) introduced the updated HOMA2 model, which uses the full iterative computer program to solve the nonlinear equations [2, mechanism_review].

HOMA2 is available as an online calculator from the Oxford Diabetes Trials Unit (DTU), a founding unit of the Oxford Centre for Diabetes, Endocrinology and Metabolism (OCDEM) [3, mechanism_review]. The HOMA2 calculator:

- **Accepts three input types:** plasma insulin (conventional immunoassay, µIU/mL or pmol/L), specific insulin (a two-site assay that does not cross-react with proinsulin), or C-peptide (nmol/L). This flexibility is important because assay type affects the computed result, and HOMA2 is recalibrated for each input type.
- **Produces three outputs:** HOMA2-IR (insulin resistance), HOMA2-%S (insulin sensitivity, the inverse of IR), and HOMA2-%B (beta-cell function), each expressed relative to a normal reference population of young adults.
- **Accepted input ranges:** plasma glucose 3.5–25.0 mmol/L; plasma insulin 20–400 pmol/L (conventional); specific insulin 20–300 pmol/L; C-peptide 0.2–3.5 nmol/L. Values outside these ranges produce unreliable output [3, mechanism_review].
- **Accounts for:** variations in hepatic and peripheral glucose resistance, increased insulin secretion above 10 mmol/L glucose, and the contribution of circulating proinsulin — effects the HOMA1 approximation cannot model.

Because HOMA2 and HOMA1 can diverge substantially for the same input pair (especially at high glucose or high insulin), the two versions are **not interchangeable**. When comparing absolute HOMA values across studies or over time, the same model version — and the same input type — must be used consistently. For absolute comparisons, HOMA2 is preferred [2, 3, mechanism_review]. HOMA1's algebraic form remains common in epidemiological literature where only a ranked score is needed, but this should be made explicit.

### QUICKI Relationship

A related index, the Quantitative Insulin Sensitivity Check Index (QUICKI), is defined as:

$$\text{QUICKI} = \frac{1}{\log(\text{insulin} \ [\mu\text{IU/mL}]) + \log(\text{glucose} \ [\text{mg/dL}])}$$

QUICKI is the reciprocal of the sum of log-transformed fasting insulin and glucose. Since log(a × b) = log(a) + log(b), QUICKI is mathematically related to a log-transformed version of HOMA-IR: QUICKI ≈ 1 / log(HOMA-IR × 405), though the exact equivalence depends on what constants are included. QUICKI was reported to show superior linear correlation with euglycemic clamp-derived insulin sensitivity in obese and diabetic populations [4, mechanism_review]; both QUICKI and HOMA-IR are derived from the same two fasting inputs and carry the same assay dependency.

---

## Thresholds: The No-Universal-Cutpoint Problem

**There is no universal HOMA-IR cutpoint.** This is the single most important practical caveat for interpreting HOMA-IR values, and it deserves emphasis.

Two distinct sources of non-universality compound each other:

### 1. Assay Non-Standardization

Fasting plasma insulin measurements are not standardized across immunoassay platforms. Different antibody-based assays cross-react to differing degrees with proinsulin and split products; conventional assays detect proinsulin fragments that specific-insulin assays do not. The Oxford DTU FAQ states explicitly: "There is no absolute value for HOMA indices. These will depend on the specific assays used for glucose, insulin and C-peptide. Because of this, there are no defined thresholds for 'normal' vs. 'abnormal' values" [3, mechanism_review]. HOMA-IR inherits this dependency directly from its fasting insulin input: a value of 2.0 on one analyzer may not equal 2.0 on another.

### 2. Population and Ethnic Variation in Insulin Physiology

Across populations, HOMA-IR distributions shift with adiposity patterns, ancestry, age, sex, and menopausal status. Published cutpoints span a wide range even across apparently similar health-screening populations.

**Healthy lean adults as a reference:** In the original HOMA1 model, the normalization gives a value near 1.0 for the assumed reference state (fasting insulin 5 µIU/mL, fasting glucose 4.5 mmol/L). Studies of metabolically healthy lean adults consistently cluster near this region. A large Brazilian reference-interval study (n = 21,684 healthy individuals, strict exclusion criteria) found a 95% reference interval for HOMA-IR of 0.39–2.86 (overall), with values for men and women essentially equivalent [5, cohort].

**Population-derived insulin-resistance thresholds (named examples):**

- **Spanish general adults (EPIRCE cross-sectional study, n = 2,459):** Using ROC regression with metabolic syndrome components as the criterion, the optimal HOMA-IR cutoff for identifying insulin resistance was approximately **1.85–2.07 in men** and **2.05–2.53 in women** (age-dependent), with the range reflecting different metabolic syndrome criteria (IDF vs. ATP III) and different percentile anchors [6, cohort].

- **Korean adults (Korean NHANES 2008–2010, n = 11,121 non-diabetic adults):** ROC analysis (Youden index, metabolic syndrome as criterion) yielded first cutoff values of **2.23 (men), 2.39 (premenopausal women), 2.48 (postmenopausal women)**. Mean HOMA-IR was 2.11 / 2.00 / 2.14 in the three groups respectively, underscoring that sex and menopausal status shift the distribution [7, cohort].

- **Hong Kong Chinese adults (CRISPS cohort, 15-year prospective, n = 2,649 at baseline, 872 with persistent normal glucose tolerance):** The cutoff for dysglycemia was **1.4** (75th percentile of persistently normal subjects); for type 2 diabetes, **2.0** (90th percentile). Asian-ancestry populations characteristically develop insulin resistance at lower absolute HOMA-IR values than European-ancestry populations, a pattern consistent with greater metabolic risk at lower adiposity [8, cohort].

The spread across these three named cohorts — roughly 1.4 to 2.5 for IR identification — reflects genuine biological variation in insulin physiology, differences in metabolic syndrome definitions used as the criterion outcome, and the assay dependency above. A cutpoint from one cohort cannot be transported to a different population, laboratory, or assay platform without re-derivation. Trend tracking within a single laboratory on a consistent assay is more informative than cross-laboratory absolute comparisons.

---

## Bibliography

1. Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. Homeostasis model assessment: insulin resistance and beta-cell function from fasting plasma glucose and insulin concentrations in man. *Diabetologia.* 1985;28(7):412–419. PMID: 3899825. DOI: 10.1007/BF00280883.

2. Levy JC, Matthews DR, Hermans MP. Correct homeostasis model assessment (HOMA) evaluation uses the computer program. *Diabetes Care.* 1998;21(12):2191–2192. PMID: 9839117. DOI: 10.2337/diacare.21.12.2191.

3. Oxford Diabetes Trials Unit (DTU), Radcliffe Department of Medicine, University of Oxford. HOMA2 Calculator FAQ. Available at: https://www.rdm.ox.ac.uk/about/our-facilities-and-units/DTU/software/homa/faq [Accessed June 2026].

4. Gutch M, Kumar S, Razi SM, Gupta KK, Gupta A. Assessment of insulin sensitivity/resistance. *Indian J Endocrinol Metab.* 2015;19(1):160–164. PMID: 25593845. DOI: 10.4103/2230-8210.146874. [mechanism_review]

5. Schrank Y, Fontes R, Perozo AFDF, et al. Proposal for fasting insulin and HOMA-IR reference intervals based on an extensive Brazilian laboratory database. *Arch Endocrinol Metab.* 2024;68:e230483. PMID: 39529982. [cohort]

6. Gayoso-Diz P, Otero-González A, Rodriguez-Alvarez MX, et al. Insulin resistance (HOMA-IR) cut-off values and the metabolic syndrome in a general adult population: effect of gender and age: EPIRCE cross-sectional study. *BMC Endocr Disord.* 2013;13:47. PMID: 24131857. [cohort]

7. Yun K-J, Han K, Kim MK, Park Y-M, Baek K-H, Song K-H, Kwon H-S. Insulin resistance distribution and cut-off value in Koreans from the 2008-2010 Korean National Health and Nutrition Examination Survey. *PLoS ONE.* 2016;11(4):e0154593. DOI: 10.1371/journal.pone.0154593. [cohort]

8. Lee CH, et al. Optimal cut-offs of homeostasis model assessment of insulin resistance (HOMA-IR) to identify dysglycemia and type 2 diabetes mellitus: a 15-year prospective study in Chinese. *PLoS ONE.* 2016;11(9):e0163424. PMID: 27658115. [cohort]
