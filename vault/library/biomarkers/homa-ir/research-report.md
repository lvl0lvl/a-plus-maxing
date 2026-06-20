---
title: "HOMA-IR (Homeostatic Model Assessment of Insulin Resistance): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/homa-ir/research-report
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.homa-ir-design-work
provenance_slug: labs-specialist
source_count: 29
---

# HOMA-IR (Homeostatic Model Assessment of Insulin Resistance): Canonical Research Report

## Summary

HOMA-IR is a dimensionless fasting-state index that estimates insulin resistance from two routine measurements — fasting plasma glucose (FPG) and fasting plasma insulin (FPI) — using the formula:

**HOMA-IR = (fasting insulin [µIU/mL] × fasting glucose [mg/dL]) / 405**

Equivalently, with glucose in mmol/L: **(fasting insulin [µIU/mL] × fasting glucose [mmol/L]) / 22.5**

The two forms are algebraically identical; the factor 18.0 converts mg/dL to mmol/L (22.5 × 18.0 = 405). Introduced by Matthews et al. in 1985 [1, cohort] and updated to a nonlinear computer model (HOMA2) by Levy, Matthews, and Hermans in 1998 [4, cohort], HOMA-IR is now the most widely used fasting surrogate for hepatic insulin resistance in epidemiological and clinical research.

The single most important practical caveat — one that must lead every interpretation of this index — is that **there is no universally validated HOMA-IR cutpoint**. Published thresholds range from approximately 1.4 to 2.9 depending on the population studied, the insulin immunoassay platform used, and the outcome criterion chosen. This non-universality arises from two compounding sources: (1) fasting insulin immunoassays are not harmonized across commercial platforms, with among-assay CVs of 12–66% [13, mechanism_review], meaning a HOMA-IR of 2.0 on one analyzer may not equal 2.0 on another; and (2) genuine biological variation in insulin physiology across ancestries, ages, sexes, and adiposity patterns shifts HOMA-IR distributions such that a cutpoint derived in one cohort cannot be transported to a different population without re-derivation.

In healthy lean adults, HOMA-IR approximates 1.0 (the model's reference normal: 5 µIU/mL insulin × 4.5 mmol/L glucose ÷ 22.5 = 1.0). A large Brazilian reference study (n = 21,684) found a 95% reference interval of 0.39–2.86 [8, cohort]. Named cohort thresholds for identifying insulin resistance range from 1.4 in Hong Kong Chinese adults [11, cohort] to 2.07–2.53 in Spanish adults [9, cohort] to 2.23–2.48 in Korean adults [10, cohort].

The index primarily reflects hepatic insulin resistance (the degree to which the liver fails to suppress glucose production in response to ambient insulin) and does not capture peripheral (skeletal-muscle) insulin resistance, which requires dynamic testing such as the euglycemic-hyperinsulinemic clamp or Matsuda OGTT index. HOMA-IR is appropriate for epidemiological characterization, baseline assessment, and longitudinal within-patient tracking on a consistent assay. It is not valid where fasting insulin is uninformative: exogenous insulin use, insulin secretagogues (sulfonylureas, meglitinides), or advanced beta-cell failure all distort the calculation.

Despite these caveats, HOMA-IR robustly predicts incident type 2 diabetes [21, meta_analysis; 22, cohort], cardiovascular events [20, meta_analysis], and is consistently elevated in metabolic-associated steatotic liver disease (MASLD/NAFLD) [3, mechanism_review; 26, meta_analysis] at the population level, and it responds meaningfully to interventions including weight loss, exercise, carbohydrate restriction, and pharmacotherapy.

---

## What HOMA-IR Is & The Underlying Model

### The Homeostatic Model: Fasting-State Physiology

Insulin resistance — the blunted ability of target tissues to respond to insulin — is central to the pathophysiology of type 2 diabetes, metabolic syndrome, and cardiovascular disease. Its direct measurement requires resource-intensive, invasive techniques. The Homeostatic Model Assessment (HOMA), introduced by Matthews, Hosker, Rudenski, Naylor, Treacher, and Turner in 1985, offered a practical alternative [1, cohort]. By exploiting the biology of the fasting steady state, HOMA allowed clinicians and researchers to infer insulin resistance and beta-cell function from two routine measurements: fasting plasma glucose and fasting plasma insulin.

The physiological logic rests on a feedback circuit that operates continuously in the post-absorptive state. In healthy fasting physiology, hepatic glucose production (HGP) is the primary determinant of FPG. The liver senses circulating insulin and suppresses glucose output proportionally; pancreatic beta-cells, in turn, sense glucose and adjust insulin secretion accordingly. The system normally converges on a homeostatic equilibrium — a stable pair of fasting glucose and insulin concentrations that reflects the balance between insulin secretory capacity and insulin action. HOMA-IR models this equilibrium mathematically: a given pair of fasting values encodes information about where along the insulin-resistance axis the individual sits [1, cohort]. Because the fasting glucose level is predominantly governed by hepatic glucose output (skeletal muscle is largely quiescent after an overnight fast, not consuming glucose against an insulin gradient), the fasting pair of FPG × FPI most directly reflects **hepatic** insulin resistance — the degree to which the liver fails to suppress glucose production in response to ambient insulin [2, cohort].

### HOMA1: The 1985 Linear Approximation

The original 1985 publication provided a simple algebraic formula derived from piecewise linear approximations to the full computer model's dose-response curves [1, cohort]:

> **HOMA-IR = (FPG [mmol/L] × FPI [µIU/mL]) / 22.5**
> 
> (US units: (FPG [mg/dL] × FPI [µIU/mL]) / 405)

A normalizing constant of 22.5 was chosen so that a healthy young adult with FPG of 4.5 mmol/L and FPI of 5 µIU/mL would score exactly 1.0, representing nominal insulin sensitivity. The formula was computationally convenient and enabled large-scale epidemiological work, but it carried deliberate simplifications: it assumed linear relationships across the physiological range, used a single compartment for insulin action (without separating hepatic from peripheral contributions), and did not account for proinsulin cross-reactivity in insulin assays or for glucose losses via the kidney at hyperglycemic concentrations [3, mechanism_review].

### HOMA2: The Updated Nonlinear Computer Model

Levy, Matthews, and Hermans published a pivotal correction in 1998 [4, cohort]: the original approximation formulae produced systematically biased estimates when applied to subjects outside the narrow normal range for which the linear approximation was adequate, particularly in individuals with insulin resistance or frank hyperglycemia. The 1998 paper clarified that HOMA should be executed using the full computer program — not the simplified formula — whenever quantitative comparisons across a wide physiological range are required [4, cohort].

Wallace, Levy, and Matthews formalized this distinction comprehensively in their 2004 review [3, mechanism_review], now the standard reference for HOMA2. HOMA2 — the updated, nonlinear computer model available from the Diabetes Trials Unit at the University of Oxford — differs from HOMA1 in three material respects:

1. **Nonlinear dose-response curves.** The HOMA2 model replaces the piecewise linear approximations of 1985 with nonlinear (sigmoidal) physiological functions governing both beta-cell insulin secretion in response to glucose and tissue glucose uptake in response to insulin. This substantially improves accuracy across the full pathophysiological range from lean normoglycemic individuals to patients with overt type 2 diabetes [3, mechanism_review].

2. **Proinsulin correction.** HOMA2 incorporates a module for proinsulin secretion, accounting for the fact that many insulin immunoassays cross-react with intact proinsulin and split proinsulin fragments (which circulate at higher concentrations in insulin-resistant and early-diabetic states). This allows either total immunoreactive insulin or specific insulin assay values to be entered appropriately [3, mechanism_review].

3. **Renal glucose loss.** At elevated fasting glucose concentrations (typically above approximately 10 mmol/L), significant glucose is lost via the kidney, altering the apparent fasting glucose level relative to what the endocrine feedback circuit "sees." HOMA2 includes a renal glucose reabsorption module so that the model remains applicable in hyperglycemic subjects [3, mechanism_review].

### HOMA-%S and HOMA-%B: Companion Outputs

HOMA-IR is not the only output the model produces. HOMA2 yields three simultaneous estimates from the same fasting pair:

- **HOMA-IR**: the insulin resistance index (dimensionless; higher = more resistant)
- **HOMA-%S** (insulin sensitivity): expressed as a percentage of a normal reference population value; the reciprocal concept to HOMA-IR
- **HOMA-%B** (beta-cell function): the estimated secretory capacity of the beta-cell mass, expressed as a percentage of normal

HOMA-%B is used in research on beta-cell preservation in pre-diabetes and early type 2 diabetes [3, mechanism_review; 5, cohort]. For clinical and epidemiological purposes, HOMA-IR is the dominant output, appearing in more than 500 publications in the years following the original paper [3, mechanism_review].

### What HOMA-IR Estimates — and What It Does Not

A critical interpretive constraint follows directly from the fasting physiology the model encodes. Because HGP is the dominant determinant of FPG during a post-absorptive fast, **HOMA-IR is primarily a surrogate for hepatic insulin resistance** [2, cohort]. Tripathy et al. demonstrated in a cohort of subjects spanning normal glucose tolerance through frank type 2 diabetes that HOMA-IR correlated strongly with hepatic insulin sensitivity (measured by stable isotope tracer during the euglycemic-hyperinsulinemic clamp), with hepatic sensitivity explaining approximately 40% of HOMA-IR's variance in subjects with IFG/IGT (combined) [2, cohort]. Critically, HOMA-IR did not correlate significantly with the M-value — the clamp's measure of whole-body (predominantly skeletal-muscle) glucose disposal — in subjects with impaired fasting glucose, confirming the conceptual boundary: HOMA-IR and peripheral insulin sensitivity are partially dissociable [2, cohort].

Peripheral (skeletal-muscle) insulin resistance — the dominant defect governing postprandial glucose disposal — requires dynamic testing to quantify. The euglycemic-hyperinsulinemic clamp (gold standard), the Matsuda index from an OGTT, and related methods capture the ability of pharmacological insulin concentrations to drive glucose uptake into muscle, a process that is essentially silent in the fasting state [3, mechanism_review]. A patient can have severely impaired peripheral insulin sensitivity while maintaining a modest HOMA-IR if their hepatic response to basal insulin remains partially intact — a dissociation that is common in early obesity-related insulin resistance and explains why HOMA-IR underestimates the severity of insulin resistance in populations where peripheral resistance predominates.

This does not diminish HOMA-IR's value. As a fasting-state hepatic surrogate, it is highly practical — requiring a single blood draw, no infusion protocol, and no specialized laboratory beyond standard glucose and insulin assays — and it predicts type 2 diabetes incidence and metabolic risk robustly at the population level [3, mechanism_review; 5, cohort]. Its appropriate domain is epidemiological characterization, baseline assessment, and longitudinal tracking of hepatic insulin sensitivity in response to lifestyle or pharmacological intervention, interpreted with awareness that it does not capture the full picture of whole-body insulin action.

---

## Calculation, Units & Thresholds

### The HOMA1 Formula

The HOMA1-IR formula in its two equivalent forms:

**SI form (glucose in mmol/L):**
> HOMA1-IR = (fasting insulin [µIU/mL] × fasting glucose [mmol/L]) / 22.5

**Conventional US form (glucose in mg/dL):**
> HOMA1-IR = (fasting insulin [µIU/mL] × fasting glucose [mg/dL]) / 405

These two expressions are algebraically identical. The conversion factor between mg/dL and mmol/L for glucose is 18.0 (1 mmol/L = 18.0 mg/dL), so 22.5 × 18.0 = 405. The denominator 22.5 is a normalization constant derived from the product of assumed normal fasting values: a fasting plasma insulin of 5 µIU/mL and a fasting plasma glucose of 4.5 mmol/L (5 × 4.5 = 22.5), representing the reference homeostatic state in the original 1985 model [1, cohort]. A result of 1.0 therefore corresponds to a fasting state at the model's assumed normal reference point.

Both formulas require that both inputs be **fasting** values — typically drawn after a minimum 8-hour fast — because the HOMA model is derived from steady-state basal physiology. Using non-fasting glucose or insulin invalidates the calculation.

#### Unit Conversions

Two unit conversions are encountered in practice:

- **Insulin:** 1 µIU/mL = 6.0 pmol/L (multiply µIU/mL by 6.0 to get pmol/L)
- **Glucose:** 1 mmol/L = 18.0 mg/dL (divide mg/dL by 18.0 to get mmol/L)

These factors confirm the formula equivalence: substituting glucose mg/dL / 18.0 into the SI form gives (insulin × glucose_mg/dL / 18.0) / 22.5 = (insulin × glucose_mg/dL) / 405.

### HOMA2: The Updated Computer Model

HOMA1 uses a linear algebraic approximation of the original nonlinear physiological feedback equations. This approximation becomes increasingly inaccurate at extreme values of glucose (particularly >10 mmol/L / 180 mg/dL) and at high insulin concentrations. Levy, Matthews, and Hermans (1998) introduced the updated HOMA2 model, which uses the full iterative computer program to solve the nonlinear equations [4, cohort]. HOMA2 is available as an online calculator from the Oxford Diabetes Trials Unit [29, mechanism_review]. The HOMA2 calculator:

- **Accepts three input types:** plasma insulin (conventional immunoassay, µIU/mL or pmol/L), specific insulin (a two-site assay that does not cross-react with proinsulin), or C-peptide (nmol/L). This flexibility matters because assay type affects the computed result, and HOMA2 is recalibrated for each input type.
- **Produces three outputs:** HOMA2-IR, HOMA2-%S (insulin sensitivity, the inverse of IR), and HOMA2-%B (beta-cell function), each expressed relative to a normal reference population of young adults.
- **Accepted input ranges:** plasma glucose 3.5–25.0 mmol/L; plasma insulin 20–400 pmol/L (conventional); specific insulin 20–300 pmol/L; C-peptide 0.2–3.5 nmol/L. Values outside these ranges produce unreliable output [29, mechanism_review].
- **Accounts for:** variations in hepatic and peripheral glucose resistance, increased insulin secretion above 10 mmol/L glucose, and the contribution of circulating proinsulin.

Because HOMA2 and HOMA1 can diverge substantially for the same input pair (especially at high glucose or high insulin), the two versions are **not interchangeable**. For absolute comparisons, HOMA2 is preferred [4, cohort; 3, mechanism_review]. HOMA1's algebraic form remains common in epidemiological literature where only a ranked score is needed, but this should be made explicit.

#### QUICKI Relationship

A related index, the Quantitative Insulin Sensitivity Check Index (QUICKI), is defined as:

> QUICKI = 1 / (log(insulin [µIU/mL]) + log(glucose [mg/dL]))

QUICKI is mathematically related to a log-transformed version of HOMA-IR. It was reported to show superior linear correlation with euglycemic clamp-derived insulin sensitivity in obese and diabetic populations [7, mechanism_review]. Both QUICKI and HOMA-IR are derived from the same two fasting inputs and carry the same assay dependency; QUICKI shares HOMA-IR's insulin-assay-harmonization problem and confers no advantage in cross-lab comparability.

### Thresholds: The No-Universal-Cutpoint Problem

**There is no universal HOMA-IR cutpoint.** Two distinct sources of non-universality compound each other.

#### 1. Assay Non-Standardization

Fasting plasma insulin measurements are not standardized across immunoassay platforms. Different antibody-based assays cross-react to differing degrees with proinsulin and split products; conventional assays detect proinsulin fragments that specific-insulin assays do not. The Oxford DTU FAQ states explicitly: "There is no absolute value for HOMA indices. These will depend on the specific assays used for glucose, insulin and C-peptide. Because of this, there are no defined thresholds for 'normal' vs. 'abnormal' values" [29, mechanism_review]. HOMA-IR inherits this dependency directly from its fasting insulin input: a value of 2.0 on one analyzer may not equal 2.0 on another.

#### 2. Population and Ethnic Variation

Across populations, HOMA-IR distributions shift with adiposity patterns, ancestry, age, sex, and menopausal status. Published cutpoints span a wide range even across apparently similar health-screening populations.

**Healthy lean adults as a reference:** In the original HOMA1 model, the normalization gives a value near 1.0 for the assumed reference state (fasting insulin 5 µIU/mL, fasting glucose 4.5 mmol/L). A large Brazilian reference-interval study (n = 21,684 healthy individuals, strict exclusion criteria) found a 95% reference interval for HOMA-IR of 0.39–2.86 overall [8, cohort].

**Population-derived insulin-resistance thresholds (named examples):**

- **Spanish general adults (EPIRCE cross-sectional study, n = 2,459):** Using ROC regression with metabolic syndrome components as the criterion, the optimal HOMA-IR cutoff for identifying insulin resistance was approximately **1.85–2.07 in men** and **2.05–2.53 in women** (age-dependent), with the range reflecting different metabolic syndrome criteria (IDF vs. ATP III) and different percentile anchors [9, cohort].

- **Korean adults (Korean NHANES 2008–2010, n = 11,121 non-diabetic adults):** ROC analysis (Youden index, metabolic syndrome as criterion) yielded cutoff values of **2.23 (men), 2.39 (premenopausal women), 2.48 (postmenopausal women)** — sex and menopausal status shift the distribution [10, cohort].

- **Hong Kong Chinese adults (CRISPS cohort, 15-year prospective, n = 2,649 at baseline, 872 with persistent normal glucose tolerance):** The cutoff for dysglycemia was **1.4** (75th percentile of persistently normal subjects); for type 2 diabetes, **2.0** (90th percentile). Asian-ancestry populations characteristically develop insulin resistance at lower absolute HOMA-IR values than European-ancestry populations, a pattern consistent with greater metabolic risk at lower adiposity [11, cohort].

The spread across these three named cohorts — roughly 1.4 to 2.5 for IR identification — reflects genuine biological variation in insulin physiology, differences in metabolic syndrome definitions used as the criterion outcome, and the assay dependency above. A cutpoint from one cohort cannot be transported to a different population, laboratory, or assay platform without re-derivation. Trend tracking within a single laboratory on a consistent assay is more informative than cross-laboratory absolute comparisons.

---

## Validation & Measurement Limitations

### Validation Against the Hyperinsulinemic-Euglycemic Clamp

The hyperinsulinemic-euglycemic glucose clamp remains the accepted gold standard for measuring whole-body insulin sensitivity: exogenous insulin is infused at a fixed rate while glucose is titrated to maintain euglycemia, and the glucose infusion rate required to do so is the direct readout of insulin-mediated glucose disposal. HOMA-IR, derived from fasting glucose and fasting insulin alone, was proposed in 1985 as a tractable surrogate for large-scale work [1, cohort].

The key validating study is Bonora et al. (2000, *Diabetes Care*), who compared HOMA-estimated insulin sensitivity against a 4-hour hyperinsulinemic-euglycemic clamp (~300 pmol/L insulin, ~5 mmol/L glucose target) in 115 subjects spanning a wide spectrum of glucose tolerance and body mass [12, cohort]. The correlation between clamp-measured total glucose disposal and HOMA was r = −0.820 (P < 0.0001), with comparable agreement across sex, age, and obesity strata (weighted κ = 0.63). The Matthews 1985 paper itself reported physiological plausibility via model-derived predictions, but direct clamp cross-validation was supplied by subsequent studies such as Bonora's [1, cohort].

While r ≈ 0.82 is clinically acceptable for an epidemiological screen, the r² ≈ 0.67 means roughly a third of the variance in clamp-measured sensitivity is not captured by HOMA. Studies in more homogeneous or healthy populations generally return lower correlations (r ≈ 0.6), while wider-spectrum cohorts trend toward r ≈ 0.8–0.9. The practical implication is that HOMA performs well for ranking populations but is imprecise for characterizing individuals.

**Hepatic selectivity.** Fasting glucose and insulin concentrations reflect basal hepatic glucose output under pancreatic suppression — not peripheral glucose uptake by skeletal muscle. HOMA-IR therefore tracks **hepatic insulin resistance** preferentially [3, mechanism_review]. The euglycemic clamp, particularly at high insulin infusion rates, interrogates whole-body (predominantly skeletal muscle) disposal — a distinct physiological compartment. Conditions that derange fasting glucose or insulin independent of whole-body sensitivity (acute illness, corticosteroids, significant hepatic disease, late beta-cell failure with insulin deficiency) can yield misleading HOMA-IR values; in those settings, dynamic testing (OGTT + Matsuda index, or formal clamp) is appropriate.

### Assay-Inheritance Limitation

HOMA-IR inherits the measurement error of its fasting-insulin input. Fasting insulin immunoassays are **not harmonized** across manufacturers or platforms. The ADA Workgroup on insulin standardization (Marcovina et al., 2007, *Clinical Chemistry*) evaluated 12 commercial insulin methods and found among-assay CVs ranging from **12% to 66%**, with a median of 24% [13, mechanism_review]. A common insulin reference preparation failed to improve harmonization, and cross-reactivity with des(64,65) proinsulin exceeded 40% in nine of ten assays — introducing systematic upward bias in proinsulin-rich states such as early type 2 diabetes.

Manley et al. (2007, *Clinical Chemistry*) directly compared 11 human insulin assays across 150 serum samples and found insulin values varied by approximately **a factor of 2** across platforms, despite high rank-order correlations (Spearman r = 0.983–0.997) [14, cohort]. Manley et al. (2008, *Diabetes Care*) extended this to show that HOMA-IR estimates for the same individuals varied from 0.8 to 2.0 in normoglycemic subjects and from 1.5 to 2.9 in those with type 2 diabetes depending solely on which of eleven serum assays was used; heparinized plasma yielded insulin values 15% lower than serum, propagating a 15% difference in HOMA-IR [15, cohort].

The operational consequence is direct: **absolute HOMA-IR values do not transfer across laboratories or assays**. A threshold of 2.0 derived in a study using radioimmunoassay A may correspond to 3.5 on platform B. Applying a published cut-point to data collected on a different assay is a category error. Best practice is to use the HOMA2 calculator with locally derived, assay-specific reference ranges, and to ensure any longitudinal or between-group comparisons are conducted within a single, consistently specified assay [3, mechanism_review; 15, cohort].

### Biological and Analytical Variability

Even when assay conditions are held constant, HOMA-IR displays substantial within-subject biological variability. Jayagopal et al. (2002, *Diabetes Care*) measured HOMA-IR on 10 occasions at 4-day intervals in 12 postmenopausal women with diet-controlled type 2 diabetes and 11 matched controls [16, cohort]. The mean intraindividual variation was 1.05 in the diabetic group versus 0.15 in controls (P = 0.001). Because HOMA-IR is log-normally distributed in people with type 2 diabetes, a subsequent measurement in the same individual must **increase by >90% or decrease by >47%** before that change can be attributed to an effect rather than biological variance.

Wallace, Levy, and Matthews (2004, *Diabetes Care*) noted that using a single fasting sample gives an intrasubject CV of 10.3% for HOMA-%S, falling to 5.8% when three samples are averaged [3, mechanism_review]. For research requiring individual-level assessment of change, the three-sample average is recommended. For population-level epidemiological studies where group means are the estimand, a single sample is usually adequate.

Pre-analytical factors compound this variability: sample type (serum vs. plasma), tube additives, centrifugation timing, freeze-thaw cycles, and storage temperature all affect insulin quantitation and propagate into HOMA-IR [15, cohort].

### Comparison to Other Insulin Resistance Indices

| Index | Inputs | What it measures | When to prefer |
|---|---|---|---|
| **HOMA-IR** | Fasting glucose + fasting insulin | Basal / hepatic IR | Epidemiology, large cohorts, single fasting sample |
| **HOMA2** | Fasting glucose + fasting insulin (computer model) | Basal / hepatic IR; corrects for nonlinear beta-cell kinetics | Same as HOMA-IR but preferred for individual estimates; use the Oxford DTU calculator |
| **QUICKI** | Fasting glucose + fasting insulin | Basal IR (log-transformed, compresses skew) | When normally distributed residuals matter for regression; contains essentially the same information as HOMA-IR |
| **Matsuda index** | Glucose + insulin across OGTT (0, 30, 60, 90, 120 min) | Whole-body (hepatic + peripheral/skeletal muscle) sensitivity | When peripheral insulin resistance is clinically relevant (e.g., post-prandial glucose, cardiovascular risk in non-diabetic subjects) |
| **TyG index** | Fasting triglycerides + fasting glucose | Surrogate IR without requiring insulin assay | Resource-limited settings or when insulin assay quality is uncertain |

**QUICKI** was validated against the euglycemic clamp in 56 subjects (r = 0.78 with clamp SI), and the log scale compression improves distributional properties for regression [17, cohort]. Because QUICKI shares HOMA-IR's input variables, it inherits the same insulin-assay-harmonization problem.

**The Matsuda index** (10,000 / √[fasting glucose × fasting insulin × mean OGTT glucose × mean OGTT insulin]) integrates post-load glucose and insulin over the full 2-hour OGTT, capturing peripheral (skeletal muscle) resistance in addition to the hepatic component [18, cohort]. Matsuda and DeFronzo (1999) reported clamp correlations of r = 0.73 (full cohort) to r = 0.86 (non-diabetic subjects). The index is preferred when dynamic or peripheral resistance is the clinical question; the trade-off is the logistical requirement of a timed OGTT.

**The TyG index** (ln[triglycerides (mg/dL) × fasting glucose (mg/dL) / 2]) is the only fasting surrogate that bypasses the insulin assay entirely [19, cohort]. Simental-Mendía et al. (2008) found the optimal TyG cut-point achieved 84% sensitivity against HOMA-IR-defined insulin resistance. Its limitation is mechanistic: TyG reflects hepatic triglyceride synthesis and lipolysis rather than insulin-mediated glucose uptake, so it performs poorly when hypertriglyceridemia has a non-metabolic cause or when subjects are on lipid-lowering therapy.

---

## Clinical Significance & Determinants

### Prognostic Associations

#### Cardiovascular Disease

HOMA-IR is an independent predictor of incident coronary heart disease (CHD) and cardiovascular events in nondiabetic adults. A 2012 PLOS ONE meta-analysis by Gast et al. pooled 65 prospective cohorts and nested case-control studies enrolling 516,325 participants. Comparing the highest to lowest HOMA-IR strata, the pooled relative risk for CHD was **1.64 (95% CI: 1.35–2.00)**; the dose-response analysis showed RR **1.46 (95% CI: 1.26–1.69) per 1-SD increment** in HOMA-IR. Notably, HOMA-IR outperformed both fasting glucose and fasting insulin alone as predictors of CHD (per-SD RR: 1.21 for glucose, 1.04 for insulin), suggesting that the ratio captures hepatic insulin resistance beyond what either constituent alone reflects [20, meta_analysis].

A 2022 systematic review and meta-analysis by González-González et al. (38 studies, 215,878 participants) corroborated this, reporting hazard ratio **1.46 (95% CI: 1.08–1.97)** for non-fatal major adverse cardiovascular events (MACE) in individuals with elevated HOMA-IR, while no association emerged for fatal MACE or cancer mortality [21, meta_analysis].

#### Type 2 Diabetes

Elevated HOMA-IR robustly predicts incident type 2 diabetes. In the population-based Hoorn Study (Ruijgrok et al., *Diabetologia*, 2018), 1,349 participants aged 50–75 years without diabetes were followed for a mean 6.4 years. The odds ratio for incident T2DM comparing the highest to lowest HOMA-IR quintile was **2.8 (95% CI: 1.4–5.6)**, consistent across linear and quintile models [22, cohort].

The Korea Genome and Epidemiology Study (KoGES), a community-based prospective cohort (Lee et al., *Clinical Diabetes and Endocrinology*, 2023) enrolling 4,314 nondiabetic adults followed for a median 9.9 years, found that the high-HOMA-IR tertile independently predicted new-onset T2DM with OR **1.86 (95% CI: 1.17–2.96)** versus the low tertile [23, cohort]. The González-González meta-analysis similarly reported HR **1.87 (95% CI: 1.40–2.49)** for incident T2DM [21, meta_analysis].

#### Metabolic-Associated Steatotic Liver Disease (MASLD/NAFLD)

Insulin resistance quantified by HOMA-IR is mechanistically central to hepatic steatosis: portal hyperinsulinism drives de novo lipogenesis and impairs fatty acid oxidation [3, mechanism_review]. HOMA-IR is consistently elevated in NAFLD/MASLD patients versus healthy controls across intervention trials and cohort studies — a finding robust enough that HOMA-IR reduction serves as a primary efficacy endpoint in NAFLD pharmacotherapy trials [26, meta_analysis].

#### Hypertension and Metabolic Syndrome

The González-González meta-analysis reported HR **1.35 (95% CI: 1.15–1.59)** for incident essential hypertension associated with high HOMA-IR values [21, meta_analysis].

### Research vs. Clinical Use

HOMA-IR is widely deployed as a **research and epidemiological tool**. Its strengths in that role are its low cost, derivation from routine fasting bloods, and large validated evidence base.

Its clinical application is more constrained. Three problems limit bedside use:

1. **No universal diagnostic cutpoint.** Published cutpoints range from 1.5 to 3.0 depending on the population, insulin assay, and outcome studied. A value of 2.5 is commonly cited in Western cohorts but does not transfer reliably across ethnicities, age groups, or laboratory platforms [3, mechanism_review].
2. **Fasting-insulin assay non-standardization.** No international reference preparation for insulin immunoassay exists. Different platforms (RIA, ECLIA, CLIA, ELISA) yield systematically divergent absolute insulin concentrations; HOMA-IR values computed on different analyzers are not numerically equivalent and should not be compared across institutions [3, mechanism_review].
3. **Fasting-state-only signal.** HOMA-IR captures predominantly hepatic (basal) insulin resistance and is insensitive to skeletal-muscle (postprandial) insulin resistance, which can be impaired while fasting measures remain in a normal range.

For these reasons, clinical societies do not endorse HOMA-IR as a diagnostic criterion for insulin resistance in routine care. Its most defensible clinical application is **serial within-patient, within-laboratory tracking** to monitor response to intervention.

### Determinants That Raise HOMA-IR

- **Obesity and visceral adiposity.** Visceral fat releases free fatty acids and inflammatory cytokines that impair hepatic insulin signaling; HOMA-IR rises proportionally with waist circumference and intra-abdominal fat mass.
- **Refined-carbohydrate diet.** Chronic postprandial hyperinsulinemia from high glycemic load dietary patterns promotes hepatic lipid accumulation and downregulates insulin receptor expression.
- **Physical inactivity.** Skeletal muscle is the primary site of insulin-stimulated glucose disposal; inactivity reduces GLUT4 translocation capacity and mitochondrial density, feeding back to raise fasting insulin.
- **Sleep restriction.** Experimental sleep curtailment consistently elevates fasting insulin and HOMA-IR within days. A systematic review and meta-analysis of RCTs on sleep manipulation (Sondrup et al., 2022) confirmed that reduced sleep duration increased markers of insulin resistance including HOMA-IR, primarily through elevated endogenous glucose production and elevated cortisol [27, meta_analysis].
- **Polycystic ovary syndrome (PCOS).** Women with PCOS show disproportionately elevated visceral fat deposition, hyperandrogenism, and hyperinsulinemia independent of BMI, resulting in HOMA-IR values substantially above age-matched controls even in non-obese individuals.

### Determinants That Lower HOMA-IR

- **Weight loss.** A 10% reduction in body weight produces a clinically meaningful fall in fasting insulin and HOMA-IR. In a prospective study of 55 adults comparing bariatric procedures versus dietary intervention over 3 years, Roux-en-Y gastric bypass reduced HOMA-IR by −3.7 units (95% CI: −5.4 to −2.1) versus dietary intervention at 12–36 months [28, cohort], with some improvement appearing before substantial weight loss via gut-peptide mechanisms.
- **Aerobic and resistance exercise.** A 2021 meta-analysis in *Obesity Reviews* by Battista et al. (30 RCTs, 37 study arms, 1,437 participants with overweight or obesity) found exercise training reduced HOMA-IR with SMD **−0.34 (95% CI: −0.49 to −0.18)**, p < 0.0001. The effect was larger in participants with T2DM (SMD −0.50) than in those without diabetes (SMD −0.31) [24, meta_analysis].
- **Carbohydrate restriction.** Reducing dietary carbohydrate intake lowers postprandial insulin secretion and fasting insulin. A 2022 meta-analysis of 8 RCTs in adults with T2DM (Parry-Strong et al., *Diabetes, Obesity and Metabolism*) demonstrated reductions in HOMA-IR with very low-carbohydrate diets, with the effect particularly pronounced in individuals with obesity (BMI > 30 kg/m²); this report is based on a supplementary/secondary analysis within the broader meta-analysis [25, meta_analysis].
- **Metformin.** Metformin reduces hepatic glucose output primarily through AMPK-dependent inhibition of gluconeogenesis, which lowers fasting glucose and secondarily lowers fasting insulin, reducing HOMA-IR.
- **GLP-1 receptor agonists.** A 2022 network meta-analysis by Yan et al. (*Frontiers in Endocrinology*, 25 studies, 1,595 NAFLD/MASLD patients) found GLP-1 RAs reduced HOMA-IR by mean difference **−1.57 (95% CI: −2.52 to −0.50)** versus control [26, meta_analysis]. Some weight-independent improvement in HOMA-IR has been observed with liraglutide within two weeks of initiation.
- **SGLT2 inhibitors.** In the Yan et al. analysis, SGLT2 inhibitor effects on HOMA-IR did not reach statistical significance (MD −0.34, 95% CI: −1.16 to 0.22), likely because their primary mechanism (renal glycosuria) reduces glucose without a direct hepatic insulin-sensitizing effect [26, meta_analysis].

### Limitations

1. **Assay non-standardization.** The absence of an international insulin reference preparation means absolute HOMA-IR values are platform-specific. This is the central reason no universal diagnostic cutpoint has been validated [3, mechanism_review].
2. **No universal cutpoint.** Optimal thresholds vary by population, sex, age, assay, and outcome — a value of 2.5 used in one study cannot be transposed to a different laboratory or ethnic group without re-derivation.
3. **Fasting/basal state only.** HOMA-IR reflects hepatic insulin sensitivity under basal (fasting) steady-state conditions. It is insensitive to postprandial skeletal-muscle insulin resistance and provides no information about first-phase insulin secretion. The gold-standard hyperinsulinemic-euglycemic clamp measures peripheral (mainly muscle) glucose disposal, which HOMA-IR does not capture.
4. **Invalid contexts.** HOMA-IR is not interpretable when fasting insulin measurements are invalid:
   - **Exogenous insulin use** — circulating insulin levels reflect injected insulin, not endogenous secretion.
   - **Insulin secretagogues (sulfonylureas, meglitinides)** — these agents elevate fasting insulin pharmacologically, inflating HOMA-IR independently of biologically meaningful resistance changes.
   - **Advanced beta-cell failure** — in late-stage T2DM or LADA, insulin secretion falls markedly; HOMA-IR may appear to normalize (or even fall) as insulin levels drop, masking worsening metabolic control.
   In these settings, C-peptide-based HOMA or dynamic testing (OGTT, clamp) is required [3, mechanism_review].

---

## Bibliography

[1]. Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. Homeostasis model assessment: insulin resistance and beta-cell function from fasting plasma glucose and insulin concentrations in man. *Diabetologia*. 1985;28(7):412–419. PMID: 3899825. DOI: 10.1007/BF00280883. — tag: cohort — tier: 1

[2]. Tripathy D, Almgren P, Tuomi T, Groop L. Contribution of insulin-stimulated glucose uptake and basal hepatic insulin sensitivity to surrogate measures of insulin sensitivity. *Diabetes Care*. 2004;27(9):2204–2210. PMID: 15333485. DOI: 10.2337/diacare.27.9.2204. — tag: cohort — tier: 1

[3]. Wallace TM, Levy JC, Matthews DR. Use and abuse of HOMA modeling. *Diabetes Care*. 2004;27(6):1487–1495. PMID: 15161807. DOI: 10.2337/diacare.27.6.1487. — tag: mechanism_review — tier: 1

[4]. Levy JC, Matthews DR, Hermans MP. Correct homeostasis model assessment (HOMA) evaluation uses the computer program. *Diabetes Care*. 1998;21(12):2191–2192. PMID: 9839117. DOI: 10.2337/diacare.21.12.2191. — tag: cohort — tier: 1

[5]. Hill NR, Levy JC, Matthews DR. Expansion of the homeostasis model assessment of β-cell function and insulin resistance to enable clinical trial outcome modeling through the interactive adjustment of physiology and treatment effects: iHOMA2. *Diabetes Care*. 2013;36(8):2324–2330. PMID: 23564921. DOI: 10.2337/dc12-0607. — tag: cohort — tier: 1

[6]. Reaven GM. What do we learn from measurements of HOMA-IR? *Diabetologia*. 2013;56(8):1867–1868. PMID: 23722624. DOI: 10.1007/s00125-013-2948-3. — tag: mechanism_review — tier: 1

[7]. Gutch M, Kumar S, Razi SM, Gupta KK, Gupta A. Assessment of insulin sensitivity/resistance. *Indian J Endocrinol Metab*. 2015;19(1):160–164. PMID: 25593845. DOI: 10.4103/2230-8210.146874. — tag: mechanism_review — tier: 2

[8]. Schrank Y, Fontes R, Perozo AFDF, et al. Proposal for fasting insulin and HOMA-IR reference intervals based on an extensive Brazilian laboratory database. *Arch Endocrinol Metab*. 2024;68:e230483. PMID: 39529982. — tag: cohort — tier: 1

[9]. Gayoso-Diz P, Otero-González A, Rodriguez-Alvarez MX, et al. Insulin resistance (HOMA-IR) cut-off values and the metabolic syndrome in a general adult population: effect of gender and age: EPIRCE cross-sectional study. *BMC Endocr Disord*. 2013;13:47. PMID: 24131857. — tag: cohort — tier: 1

[10]. Yun K-J, Han K, Kim MK, Park Y-M, Baek K-H, Song K-H, Kwon H-S. Insulin resistance distribution and cut-off value in Koreans from the 2008-2010 Korean National Health and Nutrition Examination Survey. *PLoS ONE*. 2016;11(4):e0154593. DOI: 10.1371/journal.pone.0154593. — tag: cohort — tier: 1

[11]. Lee CH, et al. Optimal cut-offs of homeostasis model assessment of insulin resistance (HOMA-IR) to identify dysglycemia and type 2 diabetes mellitus: a 15-year prospective study in Chinese. *PLoS ONE*. 2016;11(9):e0163424. PMID: 27658115. — tag: cohort — tier: 1

[12]. Bonora E, Targher G, Alberiche M, Bonadonna RC, Saggiani F, Zenere MB, Monauni T, Muggeo M. Homeostasis model assessment closely mirrors the glucose clamp technique in the assessment of insulin sensitivity: studies in subjects with various degrees of glucose tolerance and insulin sensitivity. *Diabetes Care*. 2000;23(1):57–63. PMID: 10857969. DOI: 10.2337/diacare.23.1.57. — tag: cohort — tier: 1

[13]. Marcovina S, Bowsher RR, Miller WG, Staten M, Myers G, Caudill SP, Campbell SE, Steffes MW; Insulin Standardization Workgroup. Standardization of insulin immunoassays: report of the American Diabetes Association Workgroup. *Clin Chem*. 2007;53(4):711–716. PMID: 17272483. DOI: 10.1373/clinchem.2006.082214. — tag: mechanism_review — tier: 1

[14]. Manley SE, Stratton IM, Clark PM, Luzio SD. Comparison of 11 human insulin assays: implications for clinical investigation and research. *Clin Chem*. 2007;53(5):922–932. PMID: 17363420. DOI: 10.1373/clinchem.2006.077784. — tag: cohort — tier: 1

[15]. Manley SE, Luzio SD, Stratton IM, Wallace TM, Clark PMS. Preanalytical, analytical, and computational factors affect homeostasis model assessment estimates. *Diabetes Care*. 2008;31(9):1877–1883. PMID: 18535197. DOI: 10.2337/dc08-0097. — tag: cohort — tier: 1

[16]. Jayagopal V, Kilpatrick ES, Jennings PE, Hepburn DA, Atkin SL. Biological variation of homeostasis model assessment-derived insulin resistance in type 2 diabetes. *Diabetes Care*. 2002;25(11):2022–2025. PMID: 12401750. DOI: 10.2337/diacare.25.11.2022. — tag: cohort — tier: 1

[17]. Katz A, Nambi SS, Mather K, Baron AD, Follmann DA, Sullivan G, Quon MJ. Quantitative insulin sensitivity check index: a simple, accurate method for assessing insulin sensitivity in humans. *J Clin Endocrinol Metab*. 2000;85(7):2402–2410. PMID: 10902785. DOI: 10.1210/jcem.85.7.6661. — tag: cohort — tier: 1

[18]. Matsuda M, DeFronzo RA. Insulin sensitivity indices obtained from oral glucose tolerance testing: comparison with the euglycemic insulin clamp. *Diabetes Care*. 1999;22(9):1462–1470. PMID: 10480510. DOI: 10.2337/diacare.22.9.1462. — tag: cohort — tier: 1

[19]. Simental-Mendía LE, Rodríguez-Morán M, Guerrero-Romero F. The product of fasting glucose and triglycerides as surrogate for identifying insulin resistance in apparently healthy subjects. *Metab Syndr Relat Disord*. 2008;6(4):299–304. PMID: 18973444. DOI: 10.1089/met.2008.0034. — tag: cohort — tier: 1

[20]. Gast KB, Tjeerdema N, Stijnen T, Smit JWA, Dekkers OM. Insulin resistance and risk of incident cardiovascular events in adults without diabetes: meta-analysis. *PLOS ONE*. 2012;7(12):e52036. PMID: 23300589. DOI: 10.1371/journal.pone.0052036. — tag: meta_analysis — tier: 1

[21]. González-González JG, Violante-Cumpa JR, Zambrano-Lucio M, et al. HOMA-IR as a predictor of health outcomes in patients with metabolic risk factors: a systematic review and meta-analysis. *High Blood Press Cardiovasc Prev*. 2022;29(6):547–564. PMID: 36181637. — tag: meta_analysis — tier: 1

[22]. Ruijgrok C, Dekker JM, Beulens JW, et al. Size and shape of the associations of glucose, HbA1c, insulin and HOMA-IR with incident type 2 diabetes: the Hoorn Study. *Diabetologia*. 2018;61:93–100. PMID: 29018885. DOI: 10.1007/s00125-017-4452-7. — tag: cohort — tier: 1

[23]. Lee J, Byun M, Cha S, et al. Assessment of HOMA as a predictor for new onset diabetes mellitus and diabetic complications in non-diabetic adults: a KoGES prospective cohort study. *Clin Diabetes Endocrinol*. 2023;9(1):7. PMID: 37974292. DOI: 10.1186/s40842-023-00156-3. — tag: cohort — tier: 1

[24]. Battista F, Ermolao A, van Baak MA, et al. Effect of exercise on cardiometabolic health of adults with overweight or obesity: focus on blood pressure, insulin resistance, and intrahepatic fat — a systematic review and meta-analysis. *Obes Rev*. 2021;22(Suppl 4):e13269. PMID: 33960110. DOI: 10.1111/obr.13269. — tag: meta_analysis — tier: 1

[25]. Parry-Strong A, Krebs JD, Hall RM, et al. Very low carbohydrate (ketogenic) diets in type 2 diabetes: a systematic review and meta-analysis of randomized controlled trials. *Diabetes Obes Metab*. 2022;24(12):2431–2442. PMID: 36064937. DOI: 10.1111/dom.14851. — tag: meta_analysis — tier: 1

[26]. Yan H, Xia M, Chang X, et al. GLP-1 RAs and SGLT-2 inhibitors for insulin resistance in nonalcoholic fatty liver disease: systematic review and network meta-analysis. *Front Endocrinol*. 2022;13:923606. PMID: 35909522. DOI: 10.3389/fendo.2022.923606. — tag: meta_analysis — tier: 1

[27]. Sondrup N, Termannsen AD, Eriksen JN, et al. Effects of sleep manipulation on markers of insulin sensitivity: a systematic review and meta-analysis of randomized controlled trials. *Sleep Med Rev*. 2022;62:101594. PMID: 35189549. DOI: 10.1016/j.smrv.2022.101594. — tag: meta_analysis — tier: 1

[28]. Brzozowska MM, Isaacs M, Bliuc D, et al. Effects of bariatric surgery and dietary intervention on insulin resistance and appetite hormones over a 3 year period. *Sci Rep*. 2023;13(1):6032. PMID: 37055514. DOI: 10.1038/s41598-023-33317-6. — tag: cohort — tier: 1

[29]. Oxford Diabetes Trials Unit (DTU), Radcliffe Department of Medicine, University of Oxford. HOMA2 Calculator FAQ. Available at: https://www.rdm.ox.ac.uk/about/our-facilities-and-units/DTU/software/homa/faq [Accessed June 2026]. — tag: mechanism_review — tier: 1
