---
title: "Fasting Plasma Glucose: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/fasting-glucose/research-report
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.fasting-glucose-design-work
provenance_slug: labs-specialist
source_count: 45
---

# Fasting Plasma Glucose: Canonical Research Report

## Summary

Fasting plasma glucose (FPG) is the concentration of free glucose in venous plasma after a minimum 8-hour caloric fast, expressed in mg/dL (US) or mmol/L (SI; conversion: divide mg/dL by 18.0). It is the reference diagnostic test for impaired fasting glucose and diabetes, but it also provides a mechanistic window into hepatic glucose output, insulin resistance, and beta-cell reserve.

**Diagnostic thresholds.** The ADA 2025 Standards of Care classify FPG as normal below 100 mg/dL (5.6 mmol/L), impaired fasting glucose (prediabetes) from 100–125 mg/dL (5.6–6.9 mmol/L), and diabetes at ≥ 126 mg/dL (≥ 7.0 mmol/L). The WHO/IDF 2006 framework sets the IFG lower bound higher at 110 mg/dL (6.1 mmol/L) — the same upper range and diabetes threshold apply to both. Applying the lower ADA cut-point rather than the WHO threshold increases identified IFG prevalence from ~6.6% to ~24.4% in studied populations.

**Optimal vs. diagnostic.** Diagnostic thresholds are administrative cut-points, not lowest-risk targets. A large Korean prospective cohort (n = 12.4 million) found all-cause mortality was lowest at 80–94 mg/dL (4.4–5.2 mmol/L), with risk rising progressively above 94 mg/dL. A second large Korean cohort (n > 1.1 million) found the nadir for incident CVD mortality near ~90 mg/dL (~5.0 mmol/L), with a J-shaped curve; FPG below ~70 mg/dL (< 3.9 mmol/L) also carried modestly elevated stroke risk. These findings place the evidence-based optimum at approximately 80–90 mg/dL (4.4–5.0 mmol/L) — well below the ADA's diagnostic normal ceiling.

**Hypoglycemia thresholds.** Level 1 (alert): < 70 mg/dL (< 3.9 mmol/L). Level 2 (clinically significant, neuroglycopenic): < 54 mg/dL (< 3.0 mmol/L). Level 3: any value causing severe cognitive/physical impairment requiring assistance.

**Physiology.** FPG is the equilibrium between endogenous glucose production (EGP) and peripheral disposal. Approximately 80% of EGP originates in the liver (glycogenolysis first, then gluconeogenesis from lactate, amino acids, and glycerol); the kidneys supply ~20% at rest. The set-point (~80–90 mg/dL at basal insulin 7–10 μU/mL) is governed by the portal insulin:glucagon ratio. The dawn phenomenon — a physiologically-driven early-morning glucose rise due to surges in cortisol, growth hormone, and catecholamines — affects ~50% of type 2 diabetes patients and ~30% of individuals with prediabetes.

**Measurement.** Venous plasma is the reference matrix; the enzymatic hexokinase/G6PD method is the reference assay. In-tube glycolysis is the dominant pre-analytic hazard: unprocessed whole blood loses ~5–7% of glucose per hour at room temperature. Standard sodium fluoride tubes fail to arrest glycolysis in the first 90–120 minutes; citrate-buffered tubes (e.g., Greiner FC-Mix) stabilize glucose within 1–2% for up to 48 hours. POC meters (ISO 15197:2013 ±15% tolerance) are unsuitable for diagnostic classification.

**Determinants.** FPG rises with insulin resistance, obesity, glucocorticoids, thiazides, atypical antipsychotics, beta-blockers, statins, and advancing age. It falls with weight loss (Diabetes Prevention Program: 58% diabetes risk reduction), exercise, metformin, GLP-1 receptor agonists, and SGLT-2 inhibitors. Genetic factors explain 38–68% of inter-individual FPG variance; GCK-MODY (loss-of-function *GCK* variants) produces mild, stable fasting hyperglycemia (typically 100–153 mg/dL) from birth without progression.

---

## Physiology & Regulation

### What Fasting Plasma Glucose Measures

Fasting plasma glucose (FPG) is the concentration of free glucose in venous plasma after a minimum 8-hour period of no caloric intake. It is measured in venous plasma (not whole blood or capillary blood) in an accredited laboratory, a distinction that matters clinically: plasma glucose runs approximately 10–15% higher than whole-blood glucose because red blood cells, which dilute the sample volume without contributing equivalent metabolic activity, are removed by centrifugation [1, mechanism_review]. The FPG is a point-in-time snapshot of the equilibrium between endogenous glucose delivery to the circulation and peripheral glucose disposal — the two processes that must balance precisely to defend euglycemia during the overnight fast.

Clinically, FPG is expressed in mg/dL (US convention) or mmol/L (SI/international convention); conversion factor: 1 mmol/L = 18.0 mg/dL. The diagnostic cut-points for normal fasting glucose, impaired fasting glucose, and diabetes — set by the ADA and WHO — are detailed in the Reference Ranges section [1, mechanism_review].

### The Fasting-State Glucose Set-Point

Under true steady-state fasting conditions (~8–12 hours post-meal), plasma glucose is typically maintained at approximately 80–90 mg/dL (4.4–5.0 mmol/L) with simultaneous circulating insulin of roughly 7–10 μU/mL [2, mechanism_review]. This narrow window is defended by the balance between endogenous glucose production (EGP) and glucose disposal across insulin-dependent and insulin-independent tissues.

Two features of fasting metabolism define the set-point:

1. **Rate of EGP** — in a post-absorptive adult at rest, total EGP approximates 8–10 g/hour (~1.8–2.2 mg/kg/min), enough to supply obligate glucose consumers continuously.
2. **Tissue glucose disposal** — tissues that cannot rely on fatty acids (brain, red blood cells, renal medulla) claim priority on circulating glucose; the residual is taken up by insulin-responsive tissues (skeletal muscle, adipose) at basal insulin concentrations.

When either side drifts — whether from excess hepatic output or impaired peripheral disposal — the set-point shifts upward, manifesting as elevated FPG.

### Hepatic Glucose Production: Glycogenolysis and Gluconeogenesis

The liver is the dominant source of fasting glucose, contributing approximately 80% of EGP in the post-absorptive state; the kidneys supply the remaining ~20% [2, mechanism_review]. (After 60 hours of extended fasting, the renal contribution rises to 24 ± 3% as hepatic glycogen is exhausted [3, cohort].)

During the first several hours of a fast, **glycogenolysis** — the phosphorolytic breakdown of hepatic glycogen into glucose-1-phosphate, then glucose-6-phosphate, then free glucose via glucose-6-phosphatase — is the dominant pathway. Hepatic glycogen stores (~70–100 g in a well-nourished adult) are substantially depleted within approximately 12–24 hours, after which **gluconeogenesis** assumes increasing importance [4, mechanism_review].

Gluconeogenesis is the de novo synthesis of glucose from non-carbohydrate precursors: lactate and pyruvate (from the Cori cycle, carrying ~50% of gluconeogenic flux), amino acids (principally alanine and glutamine from muscle proteolysis), and glycerol (from adipose lipolysis). The pathways converge at phosphoenolpyruvate (via PEPCK, which catalyzes the key rate-limiting step) and proceed through the gluconeogenic bypass reactions — fructose-1,6-bisphosphatase and glucose-6-phosphatase — to deliver free glucose into the portal circulation [4, mechanism_review].

A complementary transcriptional layer amplifies this response: glucagon and glucocorticoids act synergistically to induce at least 31 amino acid catabolism genes — including all five known catabolic routes that feed gluconeogenic precursors — through cooperative binding of CREB (activated by cAMP-PKA downstream of glucagon) and the glucocorticoid receptor at shared gene enhancers. Glucagon alone is insufficient to fully activate this program; corticosterone/cortisol is required for maximal gluconeogenic flux from amino acid substrates (mouse study) [5, animal].

### The Insulin:Glucagon Axis

The fasting set-point is governed principally by the molar ratio of insulin to glucagon at the hepatic portal level, not by either hormone in isolation [4, mechanism_review].

**Glucagon** (secreted from pancreatic α-cells in response to falling portal glucose, and to a lesser extent to amino acids and epinephrine) acts on hepatocytes via the glucagon receptor → adenylate cyclase → cAMP → PKA cascade to:
- Activate phosphorylase kinase, which phosphorylates and activates glycogen phosphorylase (driving glycogenolysis)
- Phosphorylate and inactivate glycogen synthase (suppressing glycogen repletion)
- Transcriptionally upregulate PEPCK and glucose-6-phosphatase (stimulating gluconeogenesis)
- Suppress glucokinase and phosphofructokinase-1 (inhibiting glycolysis and glycogen synthesis)

The net result is rapid hepatic glucose output proportional to portal glucagon concentration [4, mechanism_review].

**Insulin** (secreted from pancreatic β-cells when portal glucose rises above ~5 mmol/L / 90 mg/dL) counter-regulates via the PI3K-Akt pathway to phosphorylate and inactivate FOXO1, the transcription factor that drives PEPCK and G6Pase expression, while simultaneously activating phosphodiesterase-3B to degrade hepatic cAMP. Insulin also activates glycogen synthase (via PP1) and glucokinase, channeling incoming glucose toward glycogen rather than export. At basal fasting insulin concentrations (~7–10 μU/mL), these suppressive signals are partial — enough to modulate but not abolish EGP, allowing hepatic glucose output to match the obligate consumption by the brain and red blood cells [2, mechanism_review].

The clinical consequence of this axis is important: when the insulin:glucagon ratio falls — as in type 2 diabetes with relative insulinopenia or in frank glucagon excess — hepatic glucose output increases, elevating FPG. Conversely, excess insulin (exogenous or from an insulinoma) suppresses EGP below the brain's demand, producing fasting hypoglycemia.

### Peripheral Glucose Disposal During Fasting

During fasting, whole-body glucose disposal is dominated by insulin-independent tissues. Approximate distribution of post-absorptive glucose utilization [2, mechanism_review]:

| Tissue | % of total disposal |
|---|---|
| Brain / CNS | 45–60% |
| Skeletal muscle | 15–20% |
| Kidneys | 10–15% |
| Red blood cells | 5–10% |
| Splanchnic / other | 3–6% |
| Adipose tissue | 2–4% |

**The brain** is the largest consumer, claiming up to 60% of fasting glucose despite constituting only ~2% of body mass. Neuronal glucose uptake is mediated primarily by the high-affinity, insulin-independent GLUT3 transporter (the dominant neuronal transporter, with five-fold higher transport capacity than GLUT1), while astrocytes and the blood-brain barrier utilize GLUT1. Because neither GLUT1 nor GLUT3 requires insulin signaling for membrane trafficking, cerebral glucose uptake is obligate and continuous regardless of insulin availability [6, mechanism_review]. This explains why hypoglycemia is neurologically dangerous: there is no insulin-dependent upregulation of brain GLUT expression to compensate.

Skeletal muscle accounts for 15–20% of fasting glucose disposal, relying largely on fatty acid oxidation during the post-absorptive period (sparing glucose for the brain) and using primarily GLUT4, which is insulin-responsive. At basal insulin concentrations, muscle glucose uptake is modest; it rises sharply only with insulin stimulation (postprandial) or with vigorous exercise (contraction-stimulated GLUT4 translocation) [2, mechanism_review].

### The Dawn Phenomenon

A physiologically important modulation of FPG occurs in the early morning hours — the **dawn phenomenon** — first rigorously demonstrated in normal human volunteers by Bolli, Gerich, and colleagues in 1984 [7, cohort]. In nondiabetic individuals, nocturnal plasma glucose remains stable through 1:00–5:00 a.m. at approximately 70–80 mg/dL (3.9–4.4 mmol/L). After approximately 5:30 a.m., plasma glucose, insulin, C-peptide concentrations, and rates of glucose production all rise significantly. The investigators documented simultaneous increases in plasma cortisol, epinephrine, and norepinephrine from their nocturnal nadirs between 4:00 and 6:30 a.m., while growth hormone (GH) — which had surged episodically between 1:00 and 4:30 a.m. — began to fall thereafter [7, cohort].

The counter-regulatory hormones responsible for the dawn phenomenon act by different mechanisms:

- **Growth hormone** (peak nocturnal secretion 1:00–4:30 a.m.): stimulates hepatic glucose production and induces post-receptor insulin resistance in peripheral tissues through induction of SOCS proteins and suppression of IRS-1 signaling; the lag between peak GH and the glucose rise reflects the 2–4 hour delay before GH-induced insulin resistance becomes manifest [7, cohort; 8, mechanism_review].
- **Cortisol** (rises steeply from ~4:00 a.m.): directly stimulates hepatic gluconeogenesis (PEPCK/G6Pase transcription via glucocorticoid response elements), induces peripheral insulin resistance, and — in synergy with glucagon — amplifies amino acid catabolism gene expression to maximize gluconeogenic precursor supply (mouse study) [5, animal].
- **Catecholamines** (epinephrine, norepinephrine): acutely stimulate hepatic glycogenolysis via β2-adrenergic → cAMP → phosphorylase kinase, and suppress pancreatic insulin secretion via α2-adrenergic receptors on β-cells, further disinhibiting hepatic glucose output [8, mechanism_review].

In normal physiology, this coordinated early-morning glucose surge triggers a proportionate rise in insulin secretion that suppresses hepatic glucose production before euglycemia is breached, resulting in at most a modest (< 5–10 mg/dL) pre-breakfast glucose rise [7, cohort]. The dawn phenomenon becomes clinically significant in type 2 diabetes — where β-cell insufficiency prevents the compensatory insulin surge — and is estimated to affect approximately 50% of type 2 diabetes patients and ~30% of individuals with prediabetes [8, mechanism_review]. In these populations, unopposed counter-regulatory hormone action drives hepatic glucose output above disposal capacity, producing the characteristically elevated FPG that exceeds post-midnight nadir by 20–40 mg/dL (1.1–2.2 mmol/L) or more.

### FPG as a Window onto Overall Glycemia

FPG is not a complete picture of glucose homeostasis. In individuals with near-normal HbA1c (≤ 7.3%), postprandial glucose excursions contribute approximately 70% of the overall diurnal hyperglycemic burden, with FPG contributing only ~30%. As glycemic control deteriorates and HbA1c rises above ~9.2%, this relationship inverts: FPG contributes ~70% of the diurnal hyperglycemic load and postprandial excursions ~30% [9, cohort]. This has direct implications for how FPG should be interpreted as a standalone metric: in early or well-managed dysglycemia, a normal FPG may coexist with substantially abnormal postprandial excursions not captured by the fasting measurement. Full glycemic characterization therefore requires either a paired 2-hour postprandial glucose, an oral glucose tolerance test, or continuous glucose monitoring alongside FPG.

---

## Reference Ranges, Units & Diagnostic Thresholds

### Units and Conversion

Fasting plasma glucose (FPG) is reported in two unit systems that are used interchangeably across clinical and research contexts:

- **mg/dL** (milligrams per deciliter) — standard in the United States
- **mmol/L** (millimoles per liter) — standard in most of Europe, Canada, and WHO/IDF publications

**Conversion:** divide mg/dL by 18.0 to obtain mmol/L (more precisely, multiply by 0.0555).

Key reference conversions:

| mg/dL | mmol/L | Clinical landmark |
|-------|--------|-------------------|
| 54    | 3.0    | Level 2 hypoglycemia (clinically significant) |
| 70    | 3.9    | Level 1 hypoglycemia alert value |
| 80    | 4.4    | Lower bound of lowest-mortality range (cohort data) |
| 94–99 | 5.2–5.5 | Population mode, non-Hispanic white adults (NHANES) |
| 100   | 5.6    | ADA IFG lower bound / prediabetes threshold |
| 110   | 6.1    | WHO/IDF IFG lower bound |
| 125   | 6.9    | Upper bound of IFG (both ADA and WHO) |
| 126   | 7.0    | Diabetes diagnostic threshold (both ADA and WHO) |

### Diagnostic Thresholds: ADA 2025 Standards of Care

The American Diabetes Association (ADA) **Standards of Care in Diabetes — 2025** [10, regulatory] defines fasting plasma glucose categories for nonpregnant adults as follows. "Fasting" is defined as no caloric intake for at least 8 hours prior to measurement.

| Category | FPG (mg/dL) | FPG (mmol/L) |
|----------|-------------|--------------|
| Normal | < 100 | < 5.6 |
| Impaired fasting glucose (IFG) / Prediabetes | 100–125 | 5.6–6.9 |
| Diabetes (confirmed) | ≥ 126 | ≥ 7.0 |

A diabetes diagnosis based solely on FPG requires confirmation by a second test on a separate occasion in the absence of unequivocal hyperglycemia symptoms. The ADA notes explicitly that for all three diagnostic tests (FPG, A1C, 2-hour OGTT), "risk is continuous, extending below the lower limit of the range and becoming disproportionately greater at the higher end of the range" [10, regulatory].

### Diagnostic Thresholds: WHO/IDF 2006

The World Health Organization and International Diabetes Federation joint consultation report, **Definition and Diagnosis of Diabetes Mellitus and Intermediate Hyperglycaemia** (WHO/IDF, 2006) [11, regulatory], sets partially different boundaries:

| Category | FPG (mmol/L) | FPG (mg/dL) |
|----------|-------------|-------------|
| Normal | < 6.1 | < 110 |
| Impaired fasting glucose (IFG) | 6.1–6.9 | 110–125 |
| Diabetes | ≥ 7.0 | ≥ 126 |

Note: for WHO/IDF, an IFG classification ideally includes a 2-hour OGTT value < 7.8 mmol/L (< 140 mg/dL) to exclude IGT or diabetes; when the 2-hour value is not measured, glycemic status remains uncertain.

### The ADA vs. WHO IFG Lower Bound: Why It Matters

The single most clinically important discrepancy between the two frameworks is the **lower bound for impaired fasting glucose**: **100 mg/dL (5.6 mmol/L)** per ADA vs. **110 mg/dL (6.1 mmol/L)** per WHO/IDF.

History: the ADA originally endorsed the 110 mg/dL threshold when it was first introduced in 1997. In 2003, the ADA lowered the IFG lower bound to 100 mg/dL (5.6 mmol/L) with the stated rationale of aligning the IFG population's diabetes conversion risk with that of people with impaired glucose tolerance (IGT) based on OGTT [10, regulatory; 12, cohort].

The practical consequence is large. A study in the Korean population found that applying the lower ADA threshold (5.6 mmol/L) rather than the WHO threshold (6.1 mmol/L) increased the prevalence of IFG from 6.6% to 24.4% [12, cohort]. The ADA position means roughly 1 in 4 untreated U.S. adults meets prediabetes criteria by FPG alone, compared to a substantially smaller fraction under WHO criteria. Clinicians interpreting international literature must note which threshold was applied — the two bodies identify materially different populations.

### Optimal vs. Diagnostic: The Continuous Glucose-Risk Relationship

Diagnostic thresholds are administrative cutpoints derived from complication risk inflection points; they do not represent "safe" ceilings. Population cohort data consistently show that cardiovascular and mortality risk is continuous across the fasting glucose range, including within the "normal" zone defined by ADA criteria.

**Lowest-mortality range.** A large Korean prospective cohort study (Kim et al., *Scientific Reports*, 2017; n = 12.4 million) found all-cause mortality was lowest at **80–94 mg/dL (4.4–5.2 mmol/L)**, independent of sex and age group. Mortality began rising progressively above 94 mg/dL. The relative excess risk was highest at younger ages: in men aged 35–44, glucose in the 118–125 mg/dL range carried an HR of 1.45 (95% CI 1.37–1.54) versus the 90–94 mg/dL reference [13, cohort].

**Cardiovascular disease risk.** A Korean prospective cohort study (Cha et al., *Diabetes Care*, 2013; n = 1,197,384) found the nadir for incident CVD mortality near **~90 mg/dL (~5.0 mmol/L)**, with a J-shaped curve. Risks for ischemic heart disease, myocardial infarction, and thrombotic stroke increased progressively above 100 mg/dL (5.6 mmol/L); FPG < 70 mg/dL (< 3.9 mmol/L) was also associated with slightly elevated stroke risk [14, cohort].

These findings position the evidence-based "optimal" fasting glucose at roughly **80–90 mg/dL (4.4–5.0 mmol/L)** — well below the ADA's diagnostic "normal" ceiling of 100 mg/dL (5.6 mmol/L). The distinction matters for clinicians advising non-diabetic patients: absence of a prediabetes label does not imply the lowest achievable risk.

### Population Distributions: NHANES Data

NHANES 2005–2010 data (Selvin et al., *PLOS ONE*, 2014) provide representative distributions for U.S. noninstitutionalized adults [15, cohort]:

- **Overall median FPG:** approximately 98 mg/dL (5.4 mmol/L) across all adults
- **By sex:** men, median 100 mg/dL (5.6 mmol/L); women, median 96 mg/dL (5.3 mmol/L); population mode ~95–99 mg/dL for women and men respectively
- **By age:** median rises with age — 94 mg/dL (5.2 mmol/L) in 18–39 year olds; 99 mg/dL (5.5 mmol/L) in 40–59 year olds; 105 mg/dL (5.8 mmol/L) in ≥60 year olds
- **By race/ethnicity:** non-Hispanic whites and blacks mode ~95–96 mg/dL; Mexican-Americans mode ~98 mg/dL

Based on ADA criteria (FPG 100–125 mg/dL), approximately **33–38% of U.S. adults** without diagnosed diabetes or diabetes met the prediabetes definition during 2005–2016 NHANES cycles [16, regulatory], though awareness remained low (6–13% during that period).

These distributions underscore that the ADA "normal" ceiling of 100 mg/dL (5.6 mmol/L) sits near the population median for American adults aged 40+, meaning a substantial fraction of apparently healthy adults carry glycemia that is diagnostically normal but epidemiologically above the lowest-risk zone.

### Hypoglycemia: The Low End

For completeness of the fasting glucose spectrum, the ADA **Standards of Care 2025** [10, regulatory] defines three levels of hypoglycemia (Table 6.4):

| Level | FPG threshold | Clinical significance |
|-------|--------------|----------------------|
| Level 1 (alert) | < 70 mg/dL (< 3.9 mmol/L) | Threshold for adrenergic response in non-diabetic adults; warrants action |
| Level 2 (clinically significant) | < 54 mg/dL (< 3.0 mmol/L) | Neuroglycopenic symptoms begin; immediate treatment required |
| Level 3 (severe) | Any value with severe cognitive/physical impairment requiring assistance | Medical emergency |

A blood glucose of 70 mg/dL (3.9 mmol/L) has been recognized as the threshold at which adrenergic counterregulatory responses begin in people without diabetes [10, regulatory]. From a cardiovascular standpoint, cohort data show that FPG below ~70 mg/dL (3.9 mmol/L) is associated with modestly elevated stroke risk [14, cohort], consistent with the J-shaped relationship across the full range.

### Summary Table: Side-by-Side Reference

| Category | ADA 2025 (mg/dL) | ADA 2025 (mmol/L) | WHO/IDF 2006 (mg/dL) | WHO/IDF 2006 (mmol/L) |
|----------|-----------------|------------------|--------------------|---------------------|
| Hypoglycemia (Level 1) | < 70 | < 3.9 | — | — |
| Normal / Normoglycemia | < 100 | < 5.6 | < 110 | < 6.1 |
| IFG lower bound | 100 | 5.6 | 110 | 6.1 |
| IFG / Prediabetes range | 100–125 | 5.6–6.9 | 110–125 | 6.1–6.9 |
| Diabetes threshold | ≥ 126 | ≥ 7.0 | ≥ 126 | ≥ 7.0 |
| Evidence-based optimal* | ~80–94 | ~4.4–5.2 | — | — |

*Lowest all-cause mortality range from large population cohort [13, cohort]; not a regulatory threshold.

---

## Measurement & Pre-analytics

### Assay Methods and Reference Standardization

The enzymatic hexokinase/glucose-6-phosphate dehydrogenase (HK/G6PD) method is the accepted reference method for plasma glucose measurement. In this two-step reaction, hexokinase catalyzes the phosphorylation of glucose to glucose-6-phosphate (G6P) by ATP; G6P is then oxidized by glucose-6-phosphate dehydrogenase in the presence of NADP⁺, generating NADPH. The resulting increase in NADPH absorbance at 340 nm is directly proportional to glucose concentration [17, mechanism_review]. Because it measures glucose stoichiometrically, is highly specific, and is traceable to the isotope-dilution mass spectrometry (ID-MS) primary reference, the HK method serves as the calibration anchor for all clinical glucose assays [17, mechanism_review].

Glucose oxidase (GOD) methods are also widely used. GOD catalyzes the oxidation of β-D-glucose to gluconic acid and hydrogen peroxide; the H₂O₂ is then detected colorimetrically (Trinder reaction) or amperometrically. GOD methods are inherently selective for glucose but can be subject to oxygen tension interference and peroxidase inhibitors. Many point-of-care (POC) meters exploit glucose oxidase or glucose dehydrogenase (GDH) electrochemistry [18, mechanism_review].

**Reference matrix:** Venous plasma is the reference specimen for FPG. Plasma glucose values are approximately 10–15% higher than whole-blood values because plasma excludes the glucose-poor red cell volume. Serum glucose is analytically acceptable but subject to a brief post-clot glycolytic window before gel barrier separation; it is not the preferred matrix for diagnostic testing [19, mechanism_review].

**Standardization:** Clinical glucose methods are calibrated against reference materials traceable to GC-IDMS (gas chromatography–isotope dilution mass spectrometry), the SI-anchored primary standard. The IFCC/JCTLM framework and the NGSP (for HbA1c) provide the traceability hierarchy; the ADA 2011 and 2024 laboratory guidelines require that FPG methods be traceable to this reference system [20, regulatory].

### Fasting Requirement — Definition

"Fasting" for FPG is defined as no caloric intake for at least 8 hours before the draw (water is permitted) [21, regulatory]. The ADA specifies this threshold explicitly in its diagnostic criteria: an FPG ≥126 mg/dL (7.0 mmol/L) under these conditions meets the glycemic criterion for diabetes; 100–125 mg/dL (5.6–6.9 mmol/L) defines impaired fasting glucose (IFG) / prediabetes. The 8-hour cutoff is a practical standard, not a physiological optimum — overnight fasts of 10–14 hours are common in clinical practice and produce equivalent results in most subjects.

### In-Tube Glycolysis — The Load-Bearing Pre-analytic Hazard

This is the dominant source of systematic pre-analytic error for FPG and the mechanism most likely to produce clinically significant underestimation.

**Rate of ex vivo glycolysis.** Erythrocytes and leukocytes in unprocessed whole blood continue consuming glucose at approximately 5–7% per hour (≈0.6 mmol/L/hr, ≈10 mg/dL/hr) at room temperature [22, cohort]. Because this decay is linear across the clinical range, a sample left unprocessed for 2 hours before centrifugation loses ~10–14% of its glucose — enough to shift a patient from the diabetic range (≥126 mg/dL / 7.0 mmol/L) into the IFG range or from IFG into normal.

**Why sodium fluoride/oxalate tubes fail in the first 1–4 hours.** Sodium fluoride (NaF) inhibits glycolysis by binding to enolase — a late-acting enzyme in the glycolytic pathway. Enzymes upstream of enolase (hexokinase, phosphofructokinase) remain active for 90–120 minutes after collection, continuing to metabolize glucose until fluoride concentrations equilibrate and pH falls sufficiently to inhibit early enzymes [23, mechanism_review; 24, cohort]. In NaF/potassium oxalate tubes at room temperature, Gambino et al. measured a mean glucose decrease of 4.6% at 2 hours and 7.0% at 24 hours — compared with only 0.3% at 2 hours in citrate-buffered tubes [24, cohort]. The 2011 ADA/AACC laboratory guidelines accordingly concluded that NaF alone is not sufficient for accurate glucose preservation [20, regulatory].

**Citrate-buffered tubes as the solution.** Low-pH additive mixtures — combining citric acid, trisodium citrate, EDTA, and NaF (exemplified by the Greiner Bio-One Vacuette FC-Mix / "GlucoEXACT" tube and the Terumo Venosafe Glycaemia tube) — inhibit hexokinase and phosphofructokinase immediately by acidifying the sample to ≈pH 5, blocking early glycolytic enzymes [24, cohort]. In stabilization studies, citrate-buffered tubes held glucose within 1–2% of baseline for up to 48 hours at room temperature [25, cohort]. Equivalent performance was confirmed when the Greiner FC-Mix tube was directly compared with earlier Terumo formulations [25, cohort].

**Clinical consequence — diagnostic misclassification.** Using current WHO/ADA decision limits (diabetes threshold: 7.0 mmol/L / 126 mg/dL; IFG threshold: 5.6 mmol/L / 100 mg/dL), a simulation across 157,415 consecutive glucose requests estimated that switching from standard NaF/heparin tubes to FC-Mix tubes increased the frequency of patients classified as having impaired fasting glucose by ~48–56% [22, cohort]. The corollary is that routine NaF-tube results systematically underestimate true in-vivo glucose, meaning that the diagnostic thresholds (established on NaF-tube samples) partially compensate for this bias — a caution that must be respected when switching tube types or comparing laboratories.

**If citrate tubes are unavailable.** The NACB/WHO fallback is to place tubes immediately in an ice-water slurry and separate plasma within 30 minutes of collection. Centrifuged plasma (regardless of tube type) is stable at room temperature for several hours and at 4°C overnight [19, mechanism_review].

### Plasma vs Serum vs Capillary vs POC Meters

| Matrix / Method | Notes |
|---|---|
| Venous plasma (NaF or citrate-buffered) | Reference matrix; used for all diagnostic decisions |
| Serum (SST/gel tube) | ~10–15% lower than plasma in unprocessed samples; acceptable if centrifuged promptly; not preferred for diagnosis |
| Capillary whole blood (finger-stick) | ~0–15% higher than venous plasma in the fasting state; varies with hematocrit and perfusion |
| POC glucose meters (ISO 15197:2013) | ≥95% of results must fall within ±15 mg/dL (±0.83 mmol/L) of laboratory reference for glucose <100 mg/dL (5.55 mmol/L), and within ±15% for ≥100 mg/dL; 99% of results must fall in Consensus Error Grid zones A+B [27, regulatory] |

POC meters measure capillary or venous whole blood, not plasma, and are calibrated to report plasma-equivalent values; however, the ±15% allowable error at the diabetes diagnostic threshold (126 mg/dL / 7.0 mmol/L) spans a 36 mg/dL (2.0 mmol/L) range — straddling the IFG/diabetes cut point — making them unsuitable for diagnostic classification. They are appropriate for monitoring but not for establishing a new diagnosis [27, regulatory].

### Analytical and Biological Variability — Reference-Change Value Implications

**Analytical (within-laboratory) variability.** Well-run clinical hexokinase methods achieve a coefficient of analytical variation (CV_A) of 1.5–2.5% for fasting glucose [20, regulatory; 28, meta_analysis]. External quality assurance programs report between-laboratory bias of −6% to +7% for plasma glucose, a significant source of inter-site variation.

**Within-subject biological variability (CV_I).** The EFLM Biological Variation Database (meta-analysis of healthy adult serum/plasma glucose) places the within-subject CV_I at approximately 4.7% (median; 95% CI 3.0–5.4%) [28, meta_analysis]. Older Ricos database entries ranged 4.2–6.5% across study populations. For glucose specifically, CV_I is often close to or slightly greater than between-subject CV_G (~5.4–8.8%), yielding an individuality index near 1.0 — meaning population-based reference intervals and serial patient comparisons contribute roughly equally to interpretation.

**Reference change value (RCV).** Using CV_A = 2.5%, CV_I = 5%, and a two-tailed 95% significance threshold (Z = 1.96):

RCV = √2 × 1.96 × √(CV_A² + CV_I²) = √2 × 1.96 × √(6.25 + 25) ≈ ±24%

In practical terms, a fasting glucose of 100 mg/dL (5.56 mmol/L) can vary on serial testing by ±24 mg/dL (±1.3 mmol/L) due to random biological and analytical noise alone. This magnitude exceeds the 26 mg/dL (1.4 mmol/L) span between the normal upper limit and the IFG threshold — confirming that a single FPG measurement cannot reliably classify borderline individuals and that repeat testing (as mandated by ADA guidelines) is mandatory before diagnosis [21, regulatory].

### FPG vs HbA1c vs OGTT — Concordance and Discordance

Each test captures a distinct physiological window:

- **FPG** primarily reflects hepatic glucose output in the basal state; it is sensitive to acute-day variability and is influenced by the duration of fasting.
- **HbA1c** integrates average plasma glucose over the preceding ~8–12 weeks (weighted toward recent weeks due to red cell turnover); it is insensitive to acute glycemic events but affected by hemoglobin variants, hemolytic conditions, and erythrocyte lifespan (which varies by ethnicity and age).
- **OGTT 2-hour glucose** captures postprandial glucose disposal, primarily reflecting peripheral (muscle) insulin sensitivity; it detects early postprandial hyperglycemia invisible to FPG.

**Degree of discordance.** In a NHANES-based study of 7,412 U.S. adults, among those classified as diabetic by OGTT, concordance with HbA1c was only 34% and with FPG was only 44% [29, cohort]. For prediabetes, agreement was similarly poor across all three test combinations. An independent Vietnamese cohort found that among subjects classified as diabetic by HbA1c ≥6.5%, only 59% also met the FPG ≥126 mg/dL criterion; conversely, among normal-HbA1c subjects, 95% were also FPG-normal [30, cohort]. The practical implication is substantial: relying on any single test alone leads to meaningful missed diagnoses and false positives, particularly in populations with ethnic-specific HbA1c offsets.

The ADA 2024 Standards of Care acknowledge this discordance explicitly, stipulating that when two different tests are obtained simultaneously and both exceed their respective thresholds, diabetes is confirmed; when results are discordant, the above-threshold test should be repeated for confirmation [21, regulatory].

---

## Determinants & Clinical Significance

### Determinants That Raise FPG

#### Insulin Resistance and T2D Pathophysiology

In the fasting state, FPG is governed primarily by the rate of hepatic glucose output (HGO). Insulin normally suppresses HGO by inhibiting the gluconeogenic transcription factor FOXO1 and reducing the expression of glucose-6-phosphatase (G6Pase) and phosphoenolpyruvate carboxykinase (PEPCK). In hepatic insulin resistance — the dominant driver of fasting hyperglycaemia in established type 2 diabetes — this suppression fails, leading to unsuppressed gluconeogenesis and elevated FPG [31, mechanism_review]. Beta-cell dysfunction compounds the problem by reducing portal insulin delivery, further disinhibiting hepatic glucose production. A cross-sectional study in 707 patients with newly diagnosed type 2 diabetes confirmed that hepatic insulin resistance (quantified by hepatic insulin resistance index) was the primary determinant of fasting blood glucose, explaining early-phase post-load glucose as well as fasting levels, whereas beta-cell dysfunction additionally shaped all post-load phases [32, cohort].

#### Obesity, Physical Inactivity, and Diet

Adiposity — particularly visceral adiposity — promotes ectopic hepatic fat accumulation and drives hepatic insulin resistance. Weight gain in adulthood and physical inactivity accelerate this pathway [31, mechanism_review]. Dietary patterns high in refined carbohydrates and energy excess provide sustained substrate for de novo lipogenesis, worsening hepatic steatosis and insulin resistance.

#### Sleep Deprivation and Circadian Disruption

Chronic partial sleep restriction activates the hypothalamic–pituitary–adrenal (HPA) axis, raises evening cortisol, and reduces insulin sensitivity. Laboratory studies restricting healthy young men to 4 hours per night for 6 nights significantly impaired glucose tolerance and elevated evening cortisol [33, mechanism_review]. Shift work is associated with a higher type 2 diabetes risk, partly mediated by circadian disruption of glucose regulation [33, mechanism_review].

#### Psychological and Physical Stress / Cortisol

Glucocorticoids raise FPG through multiple mechanisms: stimulating hepatic gluconeogenesis, reducing peripheral glucose uptake, and impairing insulin secretion. Exogenous **glucocorticoids** are among the most potent pharmacological inducers of hyperglycaemia — incidence of drug-induced diabetes or clinically significant hyperglycaemia reaches 40–65% with chronic glucocorticoid use [34, mechanism_review]. Physiological stress-related cortisol elevations produce the same directional effect through identical receptors.

#### Ageing

Advancing age independently elevates FPG through reduced beta-cell mass and function, declining insulin sensitivity, and increasing adiposity at equivalent body weight. Both environmental and genetic factors interact over the life course.

#### Drugs That Raise FPG

A systematic review of medication-induced hyperglycaemia documented the following approximate incidence figures [34, mechanism_review]:

| Drug class | Approximate hyperglycaemia incidence | Primary mechanism |
|---|---|---|
| Glucocorticoids | 40–65% | ↑ hepatic gluconeogenesis; ↓ insulin sensitivity and secretion |
| Atypical antipsychotics | 10–30% | Weight gain; D2/5-HT2C/M3 receptor antagonism impairing beta-cell glucose response; direct beta-cell apoptosis |
| Thiazide diuretics | ~10% | Hypokalaemia → impaired insulin secretion (dose-dependent) |
| Beta-blockers | ~22% | Impaired insulin release (non-selective > beta-1-selective) |
| Statins | 7–48% (wide range; probably 10–20% for new-onset diabetes) | Complex: ↓ beta-cell function; reduced peripheral insulin sensitivity; interference with the mevalonate pathway |
| Niacin | 6.8–19.8% | Inhibits adipose lipolysis acutely but chronically worsens insulin resistance |

Statin therapy is associated with a modest increase in new-onset diabetes risk; any FPG worsening is typically small and does not negate cardiovascular benefit, though it warrants individual risk–benefit consideration [34, mechanism_review].

### Determinants That Lower FPG

#### Lifestyle: Weight Loss and Exercise

Weight loss — through calorie restriction or lifestyle intervention — reduces hepatic fat, restores insulin suppression of HGO, and lowers FPG substantially. In the Diabetes Prevention Program (DPP), a 7% weight-loss target through intensive lifestyle intervention reduced incident diabetes by 58% over ~3 years in high-risk individuals with IFG and impaired glucose tolerance (FPG 5.3–6.9 mmol/L [95–124 mg/dL]); 10-year DPPOS follow-up showed a 34% sustained reduction in diabetes incidence and persistent reductions in FPG versus placebo [35, rct]. Exercise training, both aerobic and resistance types, independently reduces FPG by improving peripheral and hepatic insulin sensitivity.

#### Pharmacological Agents

**Metformin** (primary mechanism: suppression of hepatic gluconeogenesis via AMPK activation) reduces HbA1c by approximately 1.0–1.5 percentage points as monotherapy; in the DPP, metformin reduced diabetes incidence by 31% versus placebo over 3 years, with an 18% sustained benefit at 10 years [35, rct].

**GLP-1 receptor agonists** lower FPG significantly. In the PIONEER 2 trial (n=816 T2DM patients), once-daily oral semaglutide 14 mg reduced HbA1c by 1.4% at 26 weeks versus 0.9% for empagliflozin [36, rct]. GLP-1 RAs exert their primary effect on post-prandial glucose (via delayed gastric emptying and glucose-dependent insulin secretion), but FPG falls as well. A meta-analysis of 14 RCTs in pre- and non-diabetic subjects found that GLP-1 RA and/or SGLT-2 inhibitor treatment reduced fasting blood glucose by a mean of −1.6 mmol/L (−28.8 mg/dL, SD 0.4) versus control [37, meta_analysis].

**SGLT-2 inhibitors** exert a relatively greater effect on FPG (through glucosuria that is independent of insulin) compared with GLP-1 RAs, which have a stronger post-prandial effect [36, rct]. HbA1c reductions of 0.7–1.0% are observed across both classes.

**Sulfonylureas** lower HbA1c by 1.0–1.25% as monotherapy (similar to metformin); over time, secondary failure is common (54% required insulin addition over 6 years in UKPDS to maintain a fasting glucose target below 5.9 mmol/L [106 mg/dL]) [38, mechanism_review].

**Insulin** lowers FPG by direct receptor-mediated inhibition of hepatic glucose output and stimulation of peripheral glucose uptake; magnitude depends on dose, type, and baseline FPG.

### Genetic Determinants

#### GCK-MODY (MODY2)

Loss-of-function variants in the glucokinase gene (*GCK*) produce a monogenic form of diabetes in which the pancreatic glucose sensor is recalibrated to a higher set-point, resulting in mild, stable fasting hyperglycaemia typically in the range of 5.5–8.5 mmol/L (100–153 mg/dL), with HbA1c usually 5.6–7.6% [39, mechanism_review]. This phenotype is present from birth, is non-progressive (unlike T2D), and is rarely associated with microvascular or macrovascular complications, meaning most affected individuals do not require pharmacological treatment outside of pregnancy. Over 600 pathogenic *GCK* variants have been documented; the specific variant does not substantially alter the clinical phenotype. Inheritance is autosomal dominant with ~50% penetrance in offspring [39, mechanism_review].

#### Common Variant Loci

Genome-wide association studies (GWAS) in large European and Asian cohorts have identified several common variants robustly associated with FPG at genome-wide significance [40, cohort]:

- **G6PC2** (rs560887, P = 1.1 × 10⁻⁵⁷): encodes islet-specific glucose-6-phosphatase catalytic subunit; glucose-raising allele paradoxically associated with mildly *reduced* T2D risk in Europeans.
- **MTNR1B** (rs10830963, P = 3.2 × 10⁻⁵⁰): each G allele raises FPG by ~0.07 mmol/L (1.3 mg/dL) and reduces beta-cell function (HOMA-B), with a modest increase in T2D risk (OR ~1.09 per allele).
- **GCK** promoter (rs4607517, P = 1.0 × 10⁻²⁵): common regulatory variants shift the glucokinase set-point moderately, distinct from rare loss-of-function MODY2 variants.
- **GCKR** (rs780094): encodes glucokinase regulatory protein; the T2D-risk allele raises FPG and HOMA-IR.

Per-allele effect sizes for these common variants are small (approximately 0.03–0.07 mmol/L [0.5–1.3 mg/dL] per allele), contrasting with the ~2.0–2.5 mmol/L (36–45 mg/dL) elevation in GCK-MODY [40, cohort].

#### Heritability

Twin studies estimate the heritability of FPG at 38–68%, with variation by measurement setting and population. A Chinese adult twin study (n=382 pairs) found FPG heritability of 67.7% (95% CI: 60.5–73.6%), with the remaining ~32% attributable to unique environmental factors [41, cohort]. A Dutch family study in non-diabetic adults estimated heritability at 38–66% depending on the measurement setting, with genetic factors influencing FPG and HbA1c being largely uncorrelated — evidence that the two markers reflect partially distinct aspects of glucose metabolism [42, cohort]. Broadly, roughly one-third to two-thirds of inter-individual FPG variation in non-diabetic populations is explained by additive genetic effects.

### Clinical Significance and Prognosis

#### FPG as a Predictor of Incident Type 2 Diabetes

FPG within the impaired fasting glucose (IFG) range — ADA definition 5.6–6.9 mmol/L (100–125 mg/dL); WHO definition 6.1–6.9 mmol/L (110–125 mg/dL) — substantially elevates risk of progression to T2D. The DPP demonstrated that high-risk individuals (FPG 5.3–6.9 mmol/L + IGT) had a placebo-group diabetes incidence of ~11% per year over 3 years (cumulative ~29% at 3 years, ~52% at 10 years) [35, rct].

#### FPG and Cardiovascular / All-Cause Mortality

A large meta-analysis of 129 studies involving over 10 million individuals found that prediabetes (any definition) was associated with increased risk of all-cause mortality (RR 1.13, 95% CI 1.10–1.17), composite CVD (RR 1.15, 95% CI 1.11–1.18), coronary heart disease (RR 1.16, 95% CI 1.11–1.21), and stroke (RR 1.14, 95% CI 1.08–1.20) over a median follow-up of 9.8 years in the general population [43, meta_analysis]. These associations held even for ADA-defined IFG (FPG 100–125 mg/dL [5.6–6.9 mmol/L]).

The Australian Diabetes, Obesity, and Lifestyle Study (AusDiab, n=10,428, median follow-up 5.2 years) found that IFG (WHO definition) independently predicted all-cause mortality (HR 1.6, 95% CI 1.0–2.4) and CVD mortality (HR 2.5, 95% CI 1.2–5.1) after adjustment for age, sex, and traditional CVD risk factors, comparable in magnitude to newly diagnosed diabetes [44, cohort].

Importantly, the FPG–mortality relationship is **J-shaped** (or continuous with no clearly safe lower threshold in the normoglycaemic range): risk rises at high levels but very low fasting glucose (<4.5 mmol/L [<81 mg/dL]) is also associated with excess mortality, as demonstrated in large Asian cohort analyses [45, cohort]. A Korean longitudinal cohort study further showed that cumulative exposure to IFG (across repeated annual measurements) was associated in a graded fashion with all-cause mortality — higher cumulative IFG burden carried higher adjusted hazard ratios up to HR ~1.20 (95% CI 1.15–1.25) — underscoring that chronicity and severity both matter [45, cohort].

### Relationship to Fasting Insulin and HOMA-IR

FPG is one of two inputs to the Homeostatic Model Assessment of Insulin Resistance (HOMA-IR), developed by Matthews et al. in 1985: **HOMA-IR = (fasting insulin [µIU/mL] × fasting glucose [mmol/L]) / 22.5** (or ÷ 405 when glucose is in mg/dL). Because FPG reflects primarily the liver's failure to suppress glucose output under fasting insulin concentrations, HOMA-IR primarily captures hepatic insulin resistance — hepatic insulin sensitivity is the dominant contributor to HOMA-IR variance in individuals with elevated fasting glucose.

A key clinical implication: FPG can remain normal while insulin resistance is already severe, because compensatory hyperinsulinaemia maintains normoglycaemia. Conversely, a rising FPG in the presence of declining or stable fasting insulin signals progressive beta-cell failure. HOMA-IR has substantial within-person biological variability, so single-occasion measurements carry meaningful imprecision.

### Relationship to HbA1c

FPG and HbA1c are moderately correlated (r ~0.45–0.57 in large observational datasets) but reflect distinct aspects of glycaemia [42, cohort]. Genetic factors influencing FPG and HbA1c are largely uncorrelated, meaning the two markers index partially independent processes. FPG captures the hepatic/fasting-state component of glucose dysregulation; HbA1c integrates 8–12 weeks of average glucose including post-prandial excursions. Neither alone is sufficient for complete glycaemic characterisation.

### Limitations of FPG as a Single Measure

1. **Day-to-day biological variability**: Within-individual biological CV for FPG is approximately 5–7%, translating to meaningful point-to-point variation. A single FPG reading may misclassify individuals near diagnostic thresholds.
2. **Hepatic-state bias**: FPG predominantly reflects hepatic fasting-state glycaemia and is insensitive to post-prandial glucose excursions, which can be elevated — and cardiovascularly relevant — even when FPG is normal.
3. **Pre-analytic sensitivity**: Prolonged sample handling at room temperature causes glycolysis; glucose falls ~5–7% per hour in whole blood unless sodium fluoride tubes are used promptly.

---

## Bibliography

[1]. Gurung P, Zubair M, Jialal I. Plasma Glucose. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2024 Feb 27. PMID: 31082125. NBK541081. — tag: mechanism_review — tier: 2.5

[2]. Dimitriadis GD, Maratou E, Kountouri A, Board M, Lambadiari V. Regulation of Postabsorptive and Postprandial Glucose Metabolism by Insulin-Dependent and Insulin-Independent Mechanisms: An Integrative Approach. *Nutrients*. 2021;13(1):159. DOI: 10.3390/nu13010159. PMID: 33419065. — tag: mechanism_review — tier: 1

[3]. Ekberg K, Landau BR, Wajngot A, Chandramouli V, Efendic S, Brunengraber H, Wahren J. Contributions by kidney and liver to glucose production in the postabsorptive state and after 60 h of fasting. *Diabetes*. 1999;48(2):292–298. DOI: 10.2337/diabetes.48.2.292. — tag: cohort — tier: 1

[4]. Rix I, Nexøe-Larsen C, Bergmann NC, Lund A, Knop FK. Glucagon Physiology. In: Feingold KR, et al., eds. *Endotext* [Internet]. South Dartmouth (MA): MDText.com, Inc.; 2019 Jul 16. PMID: 25905350. NBK279127. — tag: mechanism_review — tier: 2.5

[5]. Korenfeld N, Finkel M, Buchshtab N, et al. Fasting Hormones Synergistically Induce Amino Acid Catabolism Genes to Promote Gluconeogenesis. *Cell Mol Gastroenterol Hepatol*. 2021;12(3):1021–1036. DOI: 10.1016/j.jcmgh.2021.04.017. PMID: 33957303. — tag: animal — tier: 1

[6]. Rebelos E, Rinne JO, Nuutila P, Ekblad LL. Brain Glucose Metabolism in Health, Obesity, and Cognitive Decline — Does Insulin Have Anything to Do with It? A Narrative Review. *J Clin Med*. 2021 Apr 6;10(7):1532. DOI: 10.3390/jcm10071532. PMID: 33917464. — tag: mechanism_review — tier: 1

[7]. Bolli GB, De Feo P, De Cosmo S, Perriello G, Ventura MM, Calcinaro F, Lolli C, Campbell P, Brunetti P, Gerich JE. Demonstration of a dawn phenomenon in normal human volunteers. *Diabetes*. 1984;33(12):1150–1153. DOI: 10.2337/diab.33.12.1150. PMID: 6389230. — tag: cohort — tier: 1

[8]. O'Neal TB, Luther EE. Dawn Phenomenon. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2023 May 16. PMID: 28613643. NBK430893. — tag: mechanism_review — tier: 2.5

[9]. Monnier L, Lapinski H, Colette C. Contributions of Fasting and Postprandial Plasma Glucose Increments to the Overall Diurnal Hyperglycemia of Type 2 Diabetic Patients: Variations with increasing levels of HbA1c. *Diabetes Care*. 2003;26(3):881–885. DOI: 10.2337/diacare.26.3.881. PMID: 12610053. — tag: cohort — tier: 1

[10]. American Diabetes Association Professional Practice Committee. 2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2025. *Diabetes Care*. 2025;48(Suppl. 1):S27–S49. doi:10.2337/dc25-S002. PMC12690183. — tag: regulatory — tier: 2

[11]. World Health Organization / International Diabetes Federation. *Definition and Diagnosis of Diabetes Mellitus and Intermediate Hyperglycaemia: Report of a WHO/IDF Consultation*. Geneva: WHO; 2006. ISBN 9241594934. Available: https://iris.who.int/bitstream/handle/10665/43588/9241594934_eng.pdf — tag: regulatory — tier: 2

[12]. Kim MK, Ko SH, Kim BY, et al. The Effect of Lowering the Threshold for Diagnosis of Impaired Fasting Glucose. *Diabetes Res Clin Pract*. 2009. PMID: 19124167. PMC2615324. — tag: cohort — tier: 1

[13]. Kim NH, Han KH, Choi J, Lee J, Kim SG. Association between fasting glucose and all-cause mortality according to sex and age: a prospective cohort study. *Scientific Reports*. 2017;7:8194. doi:10.1038/s41598-017-08498-6. — tag: cohort — tier: 1

[14]. Cha SA, Yun JS, Lim TS, et al. Fasting Glucose Level and the Risk of Incident Atherosclerotic Cardiovascular Diseases. *Diabetes Care*. 2013;36(7):1988–1993. doi:10.2337/dc12-1577. PMC3687304. — tag: cohort — tier: 1

[15]. Selvin E, Crainiceanu CM, Brancati FL, Coresh J. Hemoglobin A1c, fasting plasma glucose, and 2-hour plasma glucose distributions in US population subgroups: NHANES 2005–2010. *PLOS ONE*. 2014. PMC3946694. doi:10.1371/journal.pone.0090021. — tag: cohort — tier: 1

[16]. Centers for Disease Control and Prevention / National Center for Health Statistics. *National Diabetes Statistics Report 2020: Estimates of Diabetes and Its Burden in the United States*. Atlanta, GA: CDC; 2020. Available: https://www.cdc.gov/diabetes/data/statistics-report/index.html — tag: regulatory — tier: 2

[17]. NHANES Fasting Plasma Glucose Laboratory Procedure Manual (2015–2016). CDC/NCHS. Method: hexokinase (HK/G6PD) reference method; traceability to ID/MS. URL: https://wwwn.cdc.gov/nchs/data/nhanes/public/2015/labmethods/GLU_I_MET_C311.pdf — tag: mechanism_review — tier: 2

[18]. Ferri S, Kojima K, Sode K. Review of glucose oxidases and glucose dehydrogenases: a bird's eye view of glucose sensing enzymes. *J Diabetes Sci Technol*. 2011;5(5):1068–1076. DOI: 10.1177/193229681100500507. PMID: 22027299. PMC: PMC3208862. — tag: mechanism_review — tier: 1

[19]. Nikolac N. The impact of preanalytical factors on glucose concentration measurement. *Biochemia Medica*. 2014;24(1):5–8. URL: https://www.biochemia-medica.com/assets/images/upload/Clanci/24/N.Nikolac-_The_imapct_of_preanalytical_factors_on_glucose_concetration_measurement.pdf — tag: mechanism_review — tier: 1

[20]. Sacks DB, Arnold M, Bakris GL, Bruns DE, Horvath AR, Kirkman MS, et al. Guidelines and recommendations for laboratory analysis in the diagnosis and management of diabetes mellitus. *Clin Chem*. 2011;57(6):e1–e47. DOI: 10.1373/clinchem.2010.161596. — tag: regulatory — tier: 2

[21]. American Diabetes Association Professional Practice Committee. 2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2024. *Diabetes Care*. 2024;47(Suppl 1):S20–S42. PMC: PMC9810477. — tag: regulatory — tier: 2

[22]. Bowen RAR, Hortin GL, Csako G, et al. Effects of different tube types on patient classification using current diabetes decision limits. *Clin Biochem*. 2019;74:45–52. PMCID: PMC6804563. DOI: 10.1016/j.clinbiochem.2019.09.011. — tag: cohort — tier: 1

[23]. Mikesh LM, Bruns DE. Stabilization of glucose in blood specimens: mechanism of delay in fluoride inhibition of glycolysis. *Clin Chem*. 2008;54(5):930–932. DOI: 10.1373/clinchem.2007.102160. — tag: mechanism_review — tier: 1

[24]. Gambino R, Piscitelli J, Ackattupathil TA, Theriault JL, Andrin RD, Sanfilippo ML, Etienne M. Acidification of blood is superior to sodium fluoride alone as an inhibitor of glycolysis. *Clin Chem*. 2009;55(5):1019–1021. PMID: 19282354. DOI: 10.1373/clinchem.2008.121707. — tag: cohort — tier: 1

[25]. Cadamuro J, von Meyer A, Wiedemann H, et al. The new Greiner FC-Mix tubes equal the old Terumo ones and are better than standard NaF. *Clin Chem Lab Med*. 2017;55(10):e239–e242. PMCID: PMC5628000. DOI: 10.1515/cclm-2017-0059. — tag: cohort — tier: 1

[26]. Bruns DE, Knowler WC. Stabilization of glucose in blood samples: why it matters. *Clin Chem*. 2009;55(5):850–852. PMCID: PMC3556871 (cited in). DOI: 10.1373/clinchem.2009.126037. — tag: mechanism_review — tier: 1

[27]. International Organization for Standardization. ISO 15197:2013. In vitro diagnostic test systems — Requirements for blood-glucose monitoring systems for self-testing in managing diabetes mellitus. Geneva: ISO; 2013. URL: https://www.iso.org/standard/54976.html — tag: regulatory — tier: 2

[28]. EFLM Biological Variation Database — Glucose (meta-analysis, serum/plasma). Updated 2026. URL: https://biologicalvariation.eu/api/search/by_id?query=1518. Also: Aarsand AK et al. The biological variation data critical appraisal checklist. *Clin Chem*. 2018;64:501–514. DOI: 10.1373/clinchem.2017.281808. — tag: meta_analysis — tier: 1

[29]. Zheng Y, Ma H, Wang M, et al. Limited Agreement between Classifications of Diabetes and Prediabetes Resulting from the OGTT, Hemoglobin A1c, and Fasting Glucose Tests in 7412 U.S. Adults. *J Clin Med*. 2020;9(7):2207. PMID: 32668564. DOI: 10.3390/jcm9072207. — tag: cohort — tier: 1

[30]. Ho-Pham LT, Nguyen UDT, Tran TX, Nguyen TV. Discordance in the diagnosis of diabetes: Comparison between HbA1c and fasting plasma glucose. *PLoS ONE*. 2017;12(8):e0182192. DOI: 10.1371/journal.pone.0182192. — tag: cohort — tier: 1

[31]. Galicia-Garcia U, et al. Pathophysiology of Type 2 Diabetes Mellitus. *Int J Mol Sci*. 2020;21(17):6275. PMC7503727. — tag: mechanism_review — tier: 1

[32]. Ji L, et al. Contributions of Hepatic Insulin Resistance and Islet β-Cell Dysfunction to the Blood Glucose Spectrum in Newly Diagnosed Type 2 Diabetes Mellitus. *Diabetes Metab J*. 2023. https://doi.org/10.4093/dmj.2022.0219. — tag: cohort — tier: 1

[33]. Hirotsu C, et al. Interactions between sleep, stress, and metabolism: From physiological to pathological conditions. *Sleep Sci*. 2015;8(3):143–152. PMC4688585. — tag: mechanism_review — tier: 1

[34]. Sanchez-Rangel E, et al. Medication-Induced Hyperglycemia and Diabetes Mellitus: A Review of Current Literature and Practical Management Strategies. *Curr Diab Rep*. 2024. PMC11330434. — tag: mechanism_review — tier: 1

[35]. Knowler WC, et al. 10-year follow-up of diabetes incidence and weight loss in the Diabetes Prevention Program Outcomes Study. *Lancet*. 2009;374(9702):1677–1686. PMC3135022. — tag: rct — tier: 1

[36]. Rosenstock J, et al. GLP-1 receptor agonist shows superior improvement of HbA1c compared to SGLT2 inhibitor: PIONEER 2 trial results. *Lancet Diabetes Endocrinol*. 2019. https://doi.org/10.1016/S2213-8587(19)30155-5. — tag: rct — tier: 1

[37]. Nascimento EB, et al. GLP1 receptor agonists and SGLT2 inhibitors for the prevention or delay of type 2 diabetes mellitus onset: a systematic review and meta-analysis. *BMC Med*. 2025. PMC12588854. — tag: meta_analysis — tier: 1

[38]. Foretz M, et al. Diabetic Agents, From Metformin to SGLT2 Inhibitors and GLP1 Agonists. *Front Pharmacol*. 2020. PMC7219531. — tag: mechanism_review — tier: 1

[39]. Chakera AJ, et al. Clinical Implications of the Glucokinase Impaired Function — GCK-MODY Today. *Front Endocrinol*. 2021. PMC8549873. — tag: mechanism_review — tier: 2

[40]. Prokopenko I, et al. Variants in MTNR1B influence fasting glucose levels. *Nat Genet*. 2009;41(1):77–81. PMID 19060907. — tag: cohort — tier: 1

[41]. Wang W, et al. Heritability and genome-wide association analyses of fasting plasma glucose in Chinese adult twins. *BMC Genomics*. 2020;21:484. PMID 32682390. — tag: cohort — tier: 1

[42]. Simonis-Bik AMC, et al. The heritability of HbA1c and fasting blood glucose in different measurement settings. *Twin Res Hum Genet*. 2008;11(6):597–602. PMID 19016616. — tag: cohort — tier: 1

[43]. Huang Y, et al. Association between prediabetes and risk of all cause mortality and cardiovascular disease: updated meta-analysis. *BMJ*. 2020;370:m2297. PMC7362233. — tag: meta_analysis — tier: 1

[44]. Barr EL, et al. Risk of cardiovascular and all-cause mortality in individuals with diabetes mellitus, impaired fasting glucose, and impaired glucose tolerance: the AusDiab Study. *Circulation*. 2007;116(2):151–157. PMID 17576864. — tag: cohort — tier: 1

[45]. Kim MK, et al. Frequency of Exposure to Impaired Fasting Glucose and Risk of Mortality and Cardiovascular Outcomes. *Endocrinol Metab*. 2022;37(1):e1218. https://doi.org/10.3803/EnM.2021.1218. — tag: cohort — tier: 1
