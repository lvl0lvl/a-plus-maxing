---
title: "eGFR & Creatinine (Kidney Function): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/egfr/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.egfr-design-work
provenance_slug: labs-specialist
source_count: 28
---

# eGFR & Creatinine (Kidney Function): Canonical Research Report

## Summary

Estimated glomerular filtration rate (eGFR) is the best overall index of kidney function in health and disease — but it is an **estimate**, not a direct measurement [6, regulatory; 4, regulatory]. It is derived from serum creatinine (SCr) plus age and sex using regression equations calibrated against populations where GFR was measured directly. The current clinical standard is the **CKD-EPI 2021 creatinine equation** (Inker, Eneanya, Coresh et al., *N Engl J Med* 2021), which removed the race coefficient present in prior versions since race is a social, not biological, construct [8, cohort]. eGFR is reported in **mL/min/1.73 m²**, normalized to a standard body surface area of 1.73 m²; serum creatinine is measured in **mg/dL** (multiply by 88.4 to convert to µmol/L). When cystatin C measurement is available, the CKD-EPI 2021 combined creatinine + cystatin C equation is preferred, achieving P30 accuracy ≥90% across demographic groups [8, cohort].

The central limitation of creatinine-based eGFR is its dependence on **muscle mass**. Creatinine is produced continuously in skeletal muscle from the non-enzymatic cyclization of creatine, so its serum concentration reflects both kidney function and the size of the muscle compartment. This creates two opposing, clinically important error directions. In highly muscular individuals — bodybuilders, strength athletes, or creatine-supplement users — creatinine production is elevated above average, and the eGFR equation maps these higher creatinine values to a falsely low GFR estimate. Nankivell et al. (2021) quantified this at **−5.9 ± 1.4 mL/min per 10 kg of lean mass** [18, cohort]; in the most muscular quartile, CKD-EPI specificity for true GFR <60 was only 47.4%. A muscular person with eGFR 55–65 may not have CKD at all — measured GFR or cystatin C-based eGFR should be obtained before labeling and staging.

Conversely, in sarcopenic, frail, cachectic, or cirrhotic individuals — those with low muscle mass — creatinine production falls, and the equation can return an eGFR that is falsely high, masking genuine GFR loss. Groothof et al. (2022) found 18.5% of men and 15.2% of women with low muscle mass were misclassified as not having kidney disease by creatinine-eGFR when cystatin C identified true impairment [20, cohort]. The clinical consequence is **drug overdosing**: renally cleared drugs (NSAIDs, aminoglycosides, metformin, direct oral anticoagulants) dose-reduced by eGFR will be given at full dose to a patient whose actual clearance is substantially reduced.

A third confounding class is pharmacological: drugs that block proximal-tubule creatinine secretion — cimetidine, trimethoprim, cobicistat — raise serum creatinine without changing GFR, producing an apparent but spurious eGFR drop [25, mechanism_review].

KDIGO classifies CKD into GFR categories G1 (≥90) through G5 (<15 mL/min/1.73 m²) and albuminuria categories A1–A3, with both axes independently predicting all-cause and cardiovascular mortality [4, regulatory; 6, regulatory]. The CKD-PC Matsushita 2010 meta-analysis across 21 general population cohorts established that an eGFR of 45 mL/min/1.73 m² (vs. 95) carries HR 1.57 for all-cause mortality, and the risks from low eGFR and elevated albuminuria combine multiplicatively [27, meta_analysis]. Finally, creatinine has a "blind range": because the creatinine-GFR relationship is hyperbolic, a patient can lose ≥50% of kidney function while serum creatinine remains within the laboratory reference interval [9, cohort] — making eGFR, not creatinine alone, the appropriate screening tool.

---

## Physiology: Creatinine & What eGFR Estimates

### Creatinine: Origin, Production, and Renal Handling

Creatinine is a 113-dalton nitrogenous waste product generated continuously in skeletal muscle through the non-enzymatic, spontaneous dehydration and cyclization of creatine and phosphocreatine (PCr) [1, mechanism_review]. Approximately 1–2% of the muscle creatine pool is irreversibly converted to creatinine each day, meaning that a person's daily creatinine production rate is tightly coupled to their total muscle creatine content — and therefore to their **lean muscle mass** [1, mechanism_review]. An adult male with a large skeletal muscle compartment will generate substantially more creatinine per day than an older woman with age-related sarcopenia, even if their kidneys function identically. This production variability is the foundational limitation of creatinine as a filtration marker.

Once released from muscle into the circulation, creatinine is a small, freely diffusible molecule that crosses the glomerular filtration barrier without restriction. The glomerulus filters creatinine in proportion to the plasma water concentration; essentially none is protein-bound, so the filtered load equals GFR × [serum creatinine] [2, mechanism_review]. In the steady state — when production equals excretion — the serum creatinine concentration (SCr) is inversely proportional to GFR, and this inverse relationship underlies its clinical utility.

### Tubular Secretion: A Source of Systematic Bias

Creatinine is not purely a filtration marker. The proximal tubule actively secretes creatinine via multiple transporters: basolateral uptake into tubule cells via **OAT2 (SLC22A7), OCT2 (SLC22A2), and OCT3 (SLC22A3)**, then apical efflux into urine via **MATE1 (SLC47A1) and MATE2-K (SLC47A2)**. The relative contribution of these transporters is not fully settled: Lepist et al. 2014 found OAT2 had the highest in-vitro transport activity (>2× OCT2/OCT3), revising the older OCT2-centric view, while OCT2 remains the clinically cited basolateral transporter and the locus of inhibition by cimetidine, trimethoprim, and cobicistat (which raise serum creatinine without changing GFR) [25, mechanism_review]. In individuals with normal or near-normal GFR, tubular secretion accounts for roughly **10–15% of total urinary creatinine excretion** [3, mechanism_review], producing a small but consistent overestimation of true filtration when creatinine clearance is used as a GFR surrogate. As GFR declines in chronic kidney disease, the secretory fraction rises markedly — in severe renal insufficiency the creatinine-to-inulin clearance ratio can reach 2.5, meaning creatinine clearance overestimates true GFR by up to 150% [3, mechanism_review]. There is minimal tubular reabsorption of creatinine in normal physiology.

A cooked-meat meal provides an additional exogenous creatinine load: heat converts creatine in meat to creatinine, and this is absorbed directly from the gut. A standardized cooked-meat meal transiently and significantly raises SCr — sufficient to misclassify CKD stage — with the effect resolving after 12 hours of fasting [5, cohort], which is why patients are commonly asked to avoid high-protein meals for 12–24 hours before a creatinine draw.

### GFR: The Quantity Creatinine Estimates

**Glomerular filtration rate (GFR)** is defined as the volume of plasma completely cleared of a marker per unit time, normalized to body surface area, expressed in **mL/min/1.73 m²** [6, regulatory]. KDIGO 2012 identifies GFR as "the most useful overall index of kidney function in health and disease" [6, regulatory], reflecting that it integrates the functional output of all nephrons simultaneously: the sum of single-nephron filtration rates across both kidneys. Normal GFR in young adults is approximately 120–130 mL/min/1.73 m², declining by roughly 1 mL/min/1.73 m² per year after the fourth decade.

**Directly measured GFR** — the reference standard — requires intravenous infusion of an exogenous filtration marker that is freely filtered, not secreted or reabsorbed, and not metabolized: inulin (the historic gold standard), iohexol, iothalamate, or radioisotope-labeled compounds (⁵¹Cr-EDTA, ⁹⁹ᵐTc-DTPA). These methods are accurate but require timed urine collections or serial plasma sampling, are costly and time-consuming, and are impractical for routine clinical monitoring [2, mechanism_review]. Consequently, GFR is estimated in everyday practice from endogenous markers.

**eGFR (estimated GFR)** is derived from serum creatinine plus demographic covariates — primarily age and sex — using regression equations developed in large populations with simultaneously measured true GFR [8, cohort]. The current standard equation is the **CKD-EPI 2021 creatinine equation** (Inker, Eneanya, Coresh J, et al., *N Engl J Med* 2021), which takes age and sex as inputs alongside SCr and, critically, removed the race coefficient present in the 2009 version, since race is a social construct rather than a biological variable and its inclusion introduced systematic inequity in clinical decision-making [8, cohort]. A combined creatinine + cystatin C equation (CKD-EPI 2021 cr-cysC) is now preferred when cystatin C measurement is available, as it provides better accuracy across the GFR range and in populations where muscle mass is atypical [8, cohort].

### The Non-Linear Creatinine–GFR Relationship and the "Creatinine-Blind Range"

The relationship between serum creatinine and GFR is **hyperbolic, not linear**: because SCr = (creatinine production rate) / GFR in the steady state, doubling GFR halves SCr, and halving GFR doubles SCr. At high GFR values, very large changes in filtration produce only small changes in creatinine; at low GFR, small further declines produce large creatinine rises. This non-linearity has a profound clinical consequence.

Consider a patient whose true GFR falls from 120 to 60 mL/min/1.73 m² — a 50% loss of kidney function. If their baseline SCr was 0.9 mg/dL (80 µmol/L), the SCr at GFR 60 will be approximately 1.8 mg/dL (159 µmol/L) — which still falls within or just above the "normal" reference interval in many labs (typically ≤1.2–1.3 mg/dL for men). Studies confirm that patients can lose **≥50% of kidney function while maintaining a serum creatinine within the laboratory reference range** [9, cohort]. One observational study found that 11.6% of patients had normal SCr but eGFR < 60 mL/min/1.73 m² [9, cohort]; the effect was more pronounced in women and older adults with lower muscle mass, in whom even a substantially impaired GFR generates relatively little creatinine.

This insensitivity is sometimes called the **"creatinine-blind range"** — the plateau of the hyperbolic curve at GFR values above ~60 mL/min/1.73 m² where SCr is a flat, poor discriminator of filtration. A serum creatinine of 1.0 mg/dL (88 µmol/L) could correspond to a GFR anywhere from 90 to >120 mL/min/1.73 m² depending on the patient's sex, age, and muscle mass [9, cohort]. Crucially, **a normal serum creatinine does not exclude substantial GFR loss** — a point with direct clinical relevance when dosing renally cleared drugs or evaluating a patient's candidacy for nephrotoxic agents.

### Non-GFR Determinants of Serum Creatinine

Because creatinine production is driven by muscle mass rather than kidney function alone, several factors shift serum creatinine independent of actual GFR:

- **Muscle mass (dominant determinant):** Elderly individuals, women, patients with cachexia, neuromuscular disease, or prolonged immobility produce less creatinine per day; SCr will be deceptively low relative to their true GFR decline. Bodybuilders or individuals with large muscle mass will have higher SCr for the same GFR, potentially triggering false concern [1, mechanism_review].
- **Dietary cooked meat:** Heat-converted creatinine in meat is absorbed intact, transiently raising SCr to a degree that can alter CKD staging [5, cohort]; a creatinine drawn two hours after a large steak will be meaningfully higher than a fasting measurement.
- **Sex and age:** Men have higher average muscle mass than women of similar body weight; SCr is systematically higher in males at equivalent GFR, which is why sex is a required input for all eGFR equations. Age-related sarcopenia progressively lowers creatinine production, so SCr may remain "normal" in elderly patients despite significant nephron loss [1, mechanism_review].
- **Tubular secretion variation:** Drugs competing for proximal tubular secretion transporters (trimethoprim, cimetidine, probenecid, some tyrosine kinase inhibitors) can acutely raise SCr by 10–20% by blocking secretion — without any change in actual GFR [25, mechanism_review].

### Cystatin C: A Muscle-Mass-Independent Alternative

Given creatinine's muscle-mass dependency, there is clinical interest in filtration markers whose production is independent of body composition. **Cystatin C** is a 13.3-kDa cysteine protease inhibitor produced at a constant rate by **all nucleated cells** (not just muscle) under the control of housekeeping genes [10, cohort]. It is freely filtered at the glomerulus, then almost completely reabsorbed and catabolized in the proximal tubule — none returns to the circulation. Because production is ubiquitous and not proportional to muscle mass, cystatin C levels are not confounded by sarcopenia, sex differences in muscle bulk, or dietary meat intake to the same degree as creatinine.

In populations where muscle mass is atypical — elderly patients, those with sarcopenia, patients with amputations or neuromuscular disease — cystatin C-based eGFR equations outperform creatinine-based estimates in predicting measured GFR [10, cohort; 11, cohort]. The 2021 CKD-EPI cr-cysC combined equation, which incorporates both markers, yields the best overall accuracy [8, cohort]. Important caveats apply to cystatin C: it is elevated by systemic inflammation, corticosteroid use, and thyroid dysfunction independent of GFR, and its measurement is more expensive and less standardized than creatinine assays [10, cohort].

---

## The eGFR Equations, Units & CKD Staging

### Units and Standardization

Estimated GFR (eGFR) is reported in **mL/min/1.73 m²** — the GFR normalized to a standard body surface area of 1.73 m², which allows comparison across individuals of different body sizes. Serum creatinine (Scr) is measured in **mg/dL** in US practice (multiply by **88.4** to convert to µmol/L used in SI countries). All modern estimating equations require creatinine values that have been **standardized to isotope dilution mass spectrometry (IDMS)** reference methods; using non-IDMS-calibrated creatinine introduces systematic bias [12, cohort].

### MDRD (Modification of Diet in Renal Disease)

The 4-variable MDRD equation, reexpressed for standardized creatinine by Levey et al. in 2006, was the first widely adopted estimating equation:

> eGFR = 175 × Scr⁻¹·¹⁵⁴ × Age⁻⁰·²⁰³ × 0.742 [if female] × 1.21 [if Black]

(Scr in mg/dL, age in years) [12, cohort]

The MDRD equation systematically **underestimates GFR above ~60 mL/min/1.73 m²** — the range occupied by most people without CKD — and was calibrated in a predominantly CKD population. Its race coefficient (×1.21 for Black individuals) was an empirical correction based on population averages, not a biologically grounded mechanism.

### CKD-EPI Creatinine Equation (2009)

Levey, Stevens, Schmid et al. published the CKD-EPI creatinine equation in 2009, developed and validated by the Chronic Kidney Disease Epidemiology Collaboration across 8,254 participants from 10 studies [13, cohort]. The 2009 formula uses a two-slope spline to handle the nonlinear creatinine-GFR relationship:

> eGFR = 141 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^⁻¹·²⁰⁹ × 0.993^Age × 1.018 [if female] × 1.159 [if Black]

Where κ = 0.7 (female) or 0.9 (male); α = −0.329 (female) or −0.411 (male).

Compared to MDRD, CKD-EPI 2009 showed less bias (median difference 2.5 vs 5.5 mL/min/1.73 m²) and greater P30 accuracy — the proportion of estimates falling within 30% of a measured GFR — (84.1% vs 80.6%) [13, cohort]. P30 ≥90% is the preferred threshold for clinical-grade accuracy. The 2009 equation retained a Black-race multiplier (×1.159) inherited from the MDRD approach; as with MDRD, race is a social construct rather than a biological variable.

### The 2021 Race-Free CKD-EPI Refit

In 2021, Inker LA, Eneanya ND, Coresh J, and colleagues (the CKD-EPI Collaboration) published **"New Creatinine- and Cystatin C-Based Equations to Estimate GFR without Race"** in the *New England Journal of Medicine* [8, cohort]. PMID: 34554658.

The investigators developed two new equations — one creatinine-based, one creatinine + cystatin C — in development cohorts of 8,254 and 5,352 participants respectively, then validated in 4,050 participants from 12 studies. The core change: the race variable was eliminated entirely on the grounds that race "is a social and not a biologic construct" and that assigning systematically different eGFR estimates by race risks perpetuating health inequities, delaying nephrology referral, and distorting transplant wait-time accrual in Black patients.

**The 2021 CKD-EPI creatinine equation (race-free):**

> eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^⁻¹·²⁰⁰ × 0.9938^Age × 1.012 [if female]

Where κ = 0.7 (female) or 0.9 (male); α = −0.241 (female) or −0.302 (male) [8, cohort; 14, regulatory].

The coefficient shift (141→142, exponents slightly adjusted) reflects a refit of the entire spline rather than simply dropping the race term.

**Performance (P30 accuracy):**

| Equation | Black participants | Non-Black participants |
|----------|-------------------|------------------------|
| CKD-EPI creatinine 2021 | 87.2% | 86.5% |
| CKD-EPI creatinine-cystatin C 2021 | 90.5% | 90.8% |

The **creatinine-cystatin C combined equation (2021)** is the most accurate available in routine clinical practice, achieving P30 ≥90% across racial groups [8, cohort]. It performs well because cystatin C is filtered by the glomerulus and not tubularly secreted or reabsorbed at meaningful rates, is produced at a rate largely independent of muscle mass, and therefore provides an orthogonal signal to creatinine that corrects for inter-individual variation in muscle mass — the primary source of creatinine-equation error. The NKF recommends clinical laboratories adopt the 2021 CKD-EPI equations [14, regulatory].

### KDIGO CKD GFR Staging

The **KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease** [4, regulatory] defines CKD using a three-axis classification: **Cause (C)**, **GFR category (G)**, **Albuminuria category (A)** — abbreviated **CGA**.

**CKD definition:** abnormalities of kidney structure or function present for **≥3 months** with implications for health. A single low eGFR reading is not CKD; chronicity must be established. This is clinically important: acute kidney injury (AKI) can produce the same eGFR number as G4 CKD but resolves with treatment, while CKD implies sustained, often progressive loss.

#### GFR Categories

| Category | eGFR (mL/min/1.73 m²) | Description |
|----------|------------------------|-------------|
| G1 | ≥90 | Normal or high |
| G2 | 60–89 | Mildly decreased |
| G3a | 45–59 | Mildly to moderately decreased |
| G3b | 30–44 | Moderately to severely decreased |
| G4 | 15–29 | Severely decreased |
| G5 | <15 | Kidney failure |

G1 and G2 meet CKD criteria only when accompanied by **markers of kidney damage** (albuminuria, haematuria, structural abnormality, pathological diagnosis) present for ≥3 months — an eGFR ≥60 alone, without such markers, does not define CKD. The subdivision of Stage 3 into G3a and G3b reflects meaningfully different cardiovascular and progression risk even within the 30–59 mL/min/1.73 m² range.

#### Albuminuria Categories

| Category | ACR (mg/g) | ACR (mg/mmol) | Description |
|----------|------------|----------------|-------------|
| A1 | <30 | <3 | Normal to mildly increased |
| A2 | 30–300 | 3–30 | Moderately increased |
| A3 | >300 | >30 | Severely increased (includes nephrotic-range) |

#### The GFR × Albuminuria Heat Map

KDIGO presents a **5 × 3 risk grid** cross-tabulating G1–G5 against A1–A3 [4, regulatory]. Each cell carries a color denoting prognosis for CKD progression, ESRD, and cardiovascular mortality:

- **Green** — low risk (if no other kidney disease markers, does not meet CKD criteria)
- **Yellow** — moderately increased risk
- **Orange** — high risk
- **Red** — very high risk
- **Dark red** — highest risk

The heat map conveys that both axes are **independently prognostic**: a patient with G2 + A3 carries higher risk than a patient with G3a + A1, illustrating why albuminuria must be measured and not inferred from eGFR alone. KDIGO recommends measuring both eGFR and urine albumin-to-creatinine ratio (ACR) at least annually in people with established CKD.

### Caveats and Scope Limits of eGFR Estimation

**Single measurement ≠ CKD.** The ≥3-month chronicity requirement exists precisely because acute illness (volume depletion, NSAIDs, contrast agents, AKI) can transiently suppress eGFR into the G3–G4 range; repeat testing after the acute insult resolves is mandatory before diagnosing CKD.

**Age-related GFR decline.** Mean GFR falls roughly 1 mL/min/1.73 m² per year after age ~40 [4, regulatory]. An eGFR of 65 in a 75-year-old may reflect normal aging rather than CKD, especially if ACR is in the A1 range.

**P30 accuracy and equation bias.** Even the best available equation (CKD-EPI creatinine-cystatin C 2021) has P30 ≈ 90% — meaning 1 in 10 estimates differs from the true GFR by more than 30%. At extreme GFR values (e.g., living kidney donor evaluation at eGFR >90), even a 30% error translates to a large absolute uncertainty [13, cohort; 8, cohort].

**Equation validity limits.** The CKD-EPI equations are not validated for: extremes of body composition (severe obesity, amputees, bodybuilders); rapidly changing GFR (AKI, post-transplant early phase); children and adolescents (use CKiD-U25 or Schwartz equations); conditions altering cystatin C independent of GFR (thyroid disease, high-dose corticosteroids). In these settings, measured GFR (via iohexol clearance or iothalamate) is the reference standard.

---

## Measurement & Standardization

### Serum Creatinine Assays

Two assay platforms dominate clinical creatinine measurement: the legacy Jaffe (alkaline picrate) method and the newer enzymatic method. Each carries a distinct interference profile that clinicians and laboratorians must understand.

#### The Jaffe Method

Max Jaffe first described in 1886 that creatinine reacts with picric acid in an alkaline medium to produce a red chromogen. Otto Folin adapted this principle into the clinical colorimetric assay still in widespread use today — largely because of its low cost and high throughput [15, mechanism_review]. The fundamental problem is selectivity: the alkaline picrate reaction is not exclusive to creatinine. A broad class of **non-creatinine chromogens** react similarly, producing falsely elevated readings. Documented interferents include glucose (positive at high concentrations), acetone and ketone bodies (positive), alpha-keto acids, and certain cephalosporin antibiotics. Protein — particularly albumin and immunoglobulins — also contributes a measurable pseudo-creatinine signal, and fetal hemoglobin (Hb F) causes substantial interference in neonatal samples [16, mechanism_review].

Bilirubin, paradoxically, creates **negative** interference in some Jaffe formulations, partly offsetting the positive chromogen contributions. The net direction and magnitude of interference is therefore platform-dependent, which partly explains why no two "Jaffe methods" behave identically across manufacturers. Within-laboratory interferent-related coefficients of variation for Jaffe method-analyzer combinations have been measured at 8.0–27% at low creatinine concentrations (~40 µmol/L), versus under 4% for enzymatic approaches at the same concentration [16, mechanism_review].

#### The Enzymatic Method

Enzymatic assays convert creatinine stepwise via creatininase, creatinase, and sarcosine oxidase (or coupled peroxidase reactions), generating a signal proportional only to creatinine rather than to any chromogenic substance in the matrix. This mechanistic specificity dramatically reduces susceptibility to the interferences that plague Jaffe chemistry. Bilirubin, glucose, and ketones no longer significantly perturb results; albumin and IgG interference is eliminated [16, mechanism_review]. Hemolysis does produce a modest negative interference in some enzymatic platforms — an interference not seen with Jaffe — but its magnitude is smaller than the Jaffe chromogen burden at low creatinine concentrations [17, mechanism_review].

The clinical consequence of greater specificity is most pronounced at **low-normal creatinine concentrations** (roughly < 80 µmol/L), precisely where eGFR is highest and where inaccurate creatinine input most distorts the GFR estimate. Studies comparing paired samples show ~20% of results differ by ≥10% between Jaffe and enzymatic methods, and divergence preferentially clusters at lower creatinine values — which maps exactly onto the CKD staging boundary between no CKD and early CKD [17, mechanism_review]. Enzymatic methods are therefore the preferred platform, particularly for pediatric populations where creatinine is inherently low and Hb F interference is a genuine risk [16, mechanism_review].

### IDMS-Traceable Standardization: The Load-Bearing Requirement

The single most consequential analytical development in creatinine measurement over the past two decades is **isotope-dilution mass spectrometry (IDMS) traceability** — and its direct coupling to the validity of modern eGFR equations.

The CKD-EPI and MDRD equations are empirically derived regression models: their coefficients were fit against study populations whose creatinine was measured with IDMS-traceable methods. A laboratory reporting creatinine values systematically higher or lower than the IDMS reference scale will generate eGFR values that are systematically wrong, not merely noisy. Evidence from matched cohort studies confirms this directly: subjects with identical ages, sexes, BMIs, and measured GFRs show materially different serum creatinine concentrations (females: ~1.13 vs. 0.83 mg/dL in non-standardized vs. standardized cohorts) when creatinine assay calibration differs, and this calibration gap causes the same eGFR equation to produce discordant staging outcomes [19, cohort].

In 2006, the Laboratory Working Group of the **National Kidney Disease Education Program (NKDEP)** — acting in collaboration with the International Federation of Clinical Chemistry and Laboratory Medicine (IFCC) — formally recommended that all clinical laboratories calibrate their serum creatinine procedures to be traceable to an IDMS reference measurement procedure [22, regulatory]. The anchoring reference material is **NIST SRM 967 (Creatinine in Frozen Human Serum)**. By approximately 2013, virtually all global IVD manufacturers had transitioned their creatinine measurement procedures to IDMS traceability [22, regulatory].

### Cystatin C Measurement

Clinical cystatin C is measured by **particle-enhanced turbidimetric immunoassay (PETIA)** or **particle-enhanced nephelometric immunoassay (PENIA)** — both formats use antibody-coated particles that aggregate in proportion to analyte concentration. Prior to international standardization, proficiency-testing surveys documented close to a **twofold variation** in cystatin C results for the same sample across measurement procedures [23, mechanism_review].

The IFCC Working Group on Cystatin C released the **ERM-DA471/IFCC** international certified reference material in June 2010, with a certified cystatin C mass concentration of 5.48 mg/L (expanded uncertainty k=2: ±0.15 mg/L) [24, regulatory]. All PETIA and PENIA assays for cystatin C are now expected to be calibrated against this reference material. Standardization to ERM-DA471/IFCC is specifically required for valid use of the **CKD-EPI cystatin C** and **CKD-EPI creatinine–cystatin C combined** equations, which were derived in populations where cystatin C was measured with ERM-DA471/IFCC-traceable methods [23, mechanism_review].

### Drugs That Block Tubular Secretion

Even perfectly standardized, interference-free creatinine measurement can produce misleading eGFR values when drugs block tubular creatinine secretion. Creatinine is not purely filtered; a meaningful fraction (~10–40% of urinary creatinine at normal GFR) reaches the tubular lumen via active secretion. Basolateral uptake into proximal tubule cells involves **OAT2 (SLC22A7)**, **OCT2 (SLC22A2)**, and **OCT3 (SLC22A3)**; apical efflux is mediated by **MATE1 (SLC47A1)** and **MATE2-K (SLC47A2)**. Lepist et al. (2014) found that OAT2 had the highest in-vitro creatinine transport activity at physiological concentrations — over twofold higher than OCT2 or OCT3 — while OCT2 remains the clinically cited locus of inhibition by cimetidine and trimethoprim [25, mechanism_review].

Several drugs potently inhibit one or more of these transporters:

- **Cimetidine** — inhibits creatinine transporters broadly; at high doses can nearly abolish tubular secretion
- **Trimethoprim** — potently inhibits MATE2-K and OCT2; the antibiotic's effect on serum creatinine is well-documented and clinically relevant
- **Cobicistat** — preferentially inhibits MATE1 (IC₅₀ ~0.99 µmol/L), with MATE1 inhibition identified as the primary driver of serum creatinine elevation; OAT2 and OCT2 also contribute [25, mechanism_review]
- **Dolutegravir** — preferentially inhibits OCT2
- **Others** — ritonavir, fenofibrate, certain proton-pump inhibitors, and tyrosine kinase inhibitors

The result: **serum creatinine rises, eGFR falls, but true GFR is unchanged** [25, mechanism_review]. A patient starting trimethoprim-sulfamethoxazole may show an apparent eGFR drop of 10–15 mL/min/1.73 m² that triggers unnecessary concern about drug-induced kidney injury.

### When to Prefer Measured GFR or Cystatin-C-Based eGFR

Creatinine-based eGFR is appropriate for the vast majority of clinical encounters. However, in defined situations the creatinine input is sufficiently confounded that measured GFR or cystatin-C-based eGFR is more reliable [26, mechanism_review]:

| Situation | Preferred approach | Rationale |
|---|---|---|
| Extremes of muscle mass (amputees, bodybuilders, severe sarcopenia) | Cystatin C eGFR or measured GFR | Creatinine set-point divorced from filtration |
| Cirrhosis / hepatic failure | Cystatin C eGFR or measured GFR | Reduced creatinine synthesis + volume expansion |
| Pre-nephrotoxic chemotherapy dosing (e.g., cisplatin, aminoglycosides) | Iohexol/iothalamate clearance | Narrow therapeutic window requires exact GFR |
| Living kidney donor evaluation | Iohexol/iothalamate clearance | Regulatory/ethical requirement for precision |
| Renal transplant recipients | Cystatin C eGFR or measured GFR | Immunosuppressant interference with muscle mass assumptions |
| Suspected hyperfiltration (early diabetic nephropathy) | Measured GFR | eGFR equations perform poorly above ~120 mL/min/1.73 m² |
| Drugs blocking tubular secretion in use | Cystatin C eGFR | Creatinine elevated by drug, not GFR change |

**Iohexol plasma clearance** has emerged as the practical measured-GFR reference for outpatient and research settings: it involves a single intravenous injection followed by timed blood sampling, requires no urine collection, and is not radioactive [26, mechanism_review].

---

## Determinants & Clinical Significance

### Low eGFR / Elevated Creatinine: AKI vs. CKD

A rising serum creatinine signals falling GFR, but the time course determines whether this represents **acute kidney injury (AKI)** or **chronic kidney disease (CKD)** — clinically distinct entities with different workups and management.

**Acute kidney injury** is defined by the KDIGO 2012 AKI criteria as any of: a rise in serum creatinine ≥0.3 mg/dL within 48 hours, a ≥1.5× increase from baseline within 7 days, or urine output <0.5 mL/kg/hr for ≥6 hours [7, regulatory]. AKI is classified by mechanism: *pre-renal* (volume depletion, reduced cardiac output), *intrinsic* (direct parenchymal damage — ischemic or nephrotoxic acute tubular necrosis, glomerulonephritis, interstitial nephritis), and *post-renal* (obstruction). Importantly, in AKI the GFR is changing rapidly, so eGFR equations — calibrated for steady-state creatinine — produce misleading absolute values; clinical management relies on the *trend* in creatinine over hours to days rather than a single eGFR number.

**Chronic kidney disease** is defined as structural or functional kidney abnormality persisting for ≥3 months, including eGFR <60 mL/min/1.73 m² or albuminuria (ACR ≥30 mg/g), identified on ≥2 occasions at least 90 days apart [4, regulatory]. The leading causes of true GFR loss underlying CKD are:

- **Diabetes mellitus** (leading cause globally; diabetic nephropathy via glomerulosclerosis)
- **Hypertension** (hypertensive nephrosclerosis; second leading cause of ESRD)
- **Glomerulonephritis** (IgA nephropathy, focal segmental glomerulosclerosis, membranous nephropathy, lupus nephritis)
- **Polycystic kidney disease** (autosomal dominant PKD — structural cyst replacement of nephrons)
- **Obstructive uropathy** (benign prostatic hyperplasia, nephrolithiasis, malignancy)
- **Aging** (normal physiologic GFR decline of ~1 mL/min/1.73 m² per year after age 40)

### The Critical Confounder: Non-GFR Determinants of Creatinine

eGFR is an *estimate* derived from serum creatinine, and creatinine production is directly proportional to muscle mass. This creates systematic, clinically important distortions that have nothing to do with true GFR. Two opposing error directions exist.

#### High Muscle Mass → Falsely Low eGFR

Individuals with high muscle mass produce more creatinine per unit time. A very muscular person (bodybuilder, elite athlete) can carry serum creatinine values of 1.3–1.6 mg/dL that CKD-EPI maps to an eGFR of 55–65 mL/min/1.73 m² — within the "mild CKD" range — when measured GFR may be entirely normal or even supra-normal. Nankivell et al. (2021) quantified this in 137 kidney transplant recipients measured against isotopic GFR: **eGFR was falsely reduced by −5.9 ± 1.4 mL/min per 10 kg of lean mass** [18, cohort]. In the most muscular quartile (highest appendicular skeletal muscle index), CKD-EPI specificity for true GFR <60 mL/min/1.73 m² dropped to 47.4%, with a positive predictive value of only 54.5% — effectively a coin flip [18, cohort].

**Creatine supplementation** adds another layer: oral creatine (as used in strength athletes and the general fitness population) is non-enzymatically converted to creatinine in muscle and plasma. Supplementation can transiently raise serum creatinine and depress the calculated eGFR without any change in actual GFR [4, regulatory]. A washout period of several weeks is advisable before creatinine-based eGFR is interpreted at face value in supplementing athletes.

**Clinical bottom line:** a muscular person with eGFR 55–65 is not automatically CKD. Measured GFR or cystatin C-based eGFR (which is muscle-mass-independent) should be obtained before labeling and staging.

#### Low Muscle Mass → Falsely High eGFR (a Dangerous Overestimate)

The mirror scenario is in many ways more clinically hazardous. In sarcopenia, cachexia, advanced cirrhosis, limb amputation, prolonged bedrest, and frailty — all states of reduced muscle mass — creatinine production falls. A 78-year-old with end-stage COPD may have a serum creatinine of 0.6 mg/dL that CKD-EPI maps to an eGFR of 95 mL/min/1.73 m², giving the impression of preserved kidney function when the measured GFR may be 35–40 mL/min/1.73 m².

Groothof et al. (2022) quantified this longitudinally in the PREVEND study (N=8,076): among adults ≥60 years with low muscle mass, **18.5% of men and 15.2% of women were misclassified as not having kidney disease** by creatinine-eGFR when cystatin C-based eGFR identified true GFR impairment [20, cohort]. For a 70-year-old male with low muscle mass experiencing progressive sarcopenia, the disagreement between creatinine-eGFR and measured function grew to ~24.7 mL/min/1.73 m² at baseline and widened further with muscle wasting over 15 years [20, cohort]. Okamura et al. (2023) further confirmed that sarcopenic patients with CKD (N=428,320) face nearly twice the risk of progressing to ESRD (HR 1.98; 95% CI 1.45–2.70) — yet the very low creatinine may obscure the diagnosis until it is far advanced [21, cohort].

The clinical consequence is **drug overdosing**: renally-cleared medications (NSAIDs, aminoglycosides, metformin, digoxin, direct oral anticoagulants) are dose-reduced based on eGFR, and an overestimated eGFR leads to full-dose prescribing in a patient with substantially reduced actual clearance. Cystatin C-based eGFR, or the combined creatinine/cystatin C CKD-EPI equation, should be used to guide drug dosing in sarcopenic, frail, or cachectic patients.

#### Drugs Blocking Tubular Secretion

As described in the Measurement section, cimetidine, trimethoprim, cobicistat, and dolutegravir raise serum creatinine substantially without any change in GFR [25, mechanism_review]. Patients on these drugs who appear to develop CKD G3 on creatinine should have creatinine re-checked after drug cessation or be assessed with cystatin C.

#### Pregnancy: Hyperfiltration, Not High eGFR

Pregnancy causes true glomerular hyperfiltration via renal vasodilation and increased cardiac output; GFR rises 40–60% above baseline. Serum creatinine falls (typically 0.4–0.6 mg/dL) and creatinine-based eGFR values appear elevated. **The CKD-EPI and MDRD equations are not validated in pregnancy** [4, regulatory], so eGFR values are unreliable for clinical decision-making throughout gestation. Furthermore, a creatinine value in the "normal" non-pregnant range (0.9 mg/dL) may indicate significant renal impairment in a pregnant woman.

### Prognostic Significance: Independent, Multiplicative Risk

The strongest evidence for the clinical significance of eGFR comes from the **Chronic Kidney Disease Prognosis Consortium (CKD-PC)** — a coordinated meta-analysis of individual participant data across general population cohorts worldwide.

Matsushita et al. (2010) ran **two parallel analyses** across 21 general population cohorts [27, meta_analysis]:

- **ACR stratum — 14 cohorts, N=105,872, ~730,577 person-years:** cohorts with quantitative albumin-to-creatinine ratio measurements. The joint eGFR × albuminuria hazard ratios are derived from this stratum.
- **Dipstick proteinuria stratum — 7 cohorts, N=1,128,310, ~4,732,110 person-years:** cohorts with qualitative urine dipstick data only; analyzed in parallel but reported separately.

These two strata were not pooled into a single unified analysis — the arithmetic sum (1,234,182 participants) reflects the combined count across both parallel arms, not a single pooled dataset. Both strata independently demonstrated that low eGFR and elevated albuminuria are **independently and multiplicatively associated with all-cause and cardiovascular mortality**, without statistically significant interaction between the two.

The joint eGFR × ACR hazard ratios (from the ACR stratum, N=105,872):

| eGFR (vs. 95 mL/min/1.73 m²) | HR, all-cause mortality (95% CI) |
|-------------------------------|----------------------------------|
| 60 mL/min/1.73 m² | 1.18 (1.05–1.32) |
| 45 mL/min/1.73 m² | 1.57 (1.39–1.78) |
| 15 mL/min/1.73 m² | 3.14 (2.39–4.13) |

| ACR (vs. 5 mg/g) | HR, all-cause mortality (95% CI) |
|-------------------|----------------------------------|
| 10 mg/g | 1.20 (1.15–1.26) |
| 30 mg/g | 1.63 (1.50–1.77) |
| 300 mg/g | 2.22 (1.97–2.51) |

"Multiplicative" here means the risks combine multiplicatively on the hazard scale under the standard Cox no-interaction model — not super-multiplicative synergy. A patient with both eGFR 45 and ACR 300 mg/g faces roughly the *product* of their individual hazards, substantially higher than either marker alone, but there is no statistically significant amplification beyond that multiplicative baseline. The consortium subsequently expanded this analysis to high-risk populations (diabetes, hypertension, cardiovascular disease), confirming comparable risk gradients in those cohorts as well [28, meta_analysis].

This evidence base underpins the **KDIGO risk heat map**, which cross-classifies patients by six eGFR categories (G1–G5, with G3 split into G3a/G3b) and three albuminuria categories (A1 <30 mg/g; A2 30–300 mg/g; A3 >300 mg/g) to assign risk from "low" (green) through "moderately increased" (yellow), "high" (orange), and "very high risk" (red) [4, regulatory]. A patient at G4/A3 is in the deepest red — annual nephrology review, aggressive cardiorenal risk modification, and preparation for renal replacement therapy planning.

### Clinical Applications

**CKD staging and nephrology referral:** eGFR is the gate-keeper for CKD diagnosis, staging, and the G4 (<30 mL/min/1.73 m²) nephrology referral threshold. It triggers evaluation for anemia of CKD, mineral-bone disease, and acid-base management.

**Renal drug dosing:** The most routine use of eGFR outside nephrology clinics is calculating dose reductions for renally excreted drugs. Most pharmacopoeia entries express dose adjustments at eGFR thresholds of 60, 45, 30, and 15 mL/min/1.73 m². The caveats above (sarcopenia, high muscle mass) apply here with direct patient-safety implications.

**Contrast and nephrotoxin caution:** Intravenous iodinated contrast is withheld or used with caution at eGFR <30 mL/min/1.73 m² given risk of contrast-induced AKI; NSAIDs and aminoglycosides are generally avoided at eGFR <30. Metformin is paused for procedures and restricted at eGFR <30.

**Transplant evaluation:** Both donor and recipient workups rely on eGFR; living donors require measured GFR (iothalamate or iohexol clearance) to confirm truly preserved function before a kidney is surrendered.

### Limitations of eGFR

1. **It is an estimate, not a measurement.** CKD-EPI eGFR achieves P30 accuracy in ~86–87% of individuals in validation populations — meaning roughly 1 in 7 results are off by >30% from true GFR [4, regulatory].
2. **Muscle-mass and dietary confounders** (detailed above) create systematic bias in opposite directions depending on body composition.
3. **Not valid in rapidly changing GFR:** in AKI, creatinine is not at steady state; trend matters more than absolute value.
4. **Not validated in extremes of body size** (morbid obesity, extreme short stature) or **pregnancy**.
5. **The creatinine-blind range:** at high GFR (>90 mL/min/1.73 m²) there is very low sensitivity for early GFR decline; a patient who started at GFR 140 (e.g., due to early diabetic hyperfiltration) and has lost 50 mL/min may still have an eGFR of 90, classified as G1.
6. **Cystatin C provides a muscle-mass-independent alternative** and performs better in the elderly, sarcopenic patients, and individuals with extreme body composition. The combined creatinine/cystatin C CKD-EPI equation has improved accuracy across subgroups. Formally measured GFR (plasma clearance of iothalamate, iohexol, or DTPA) remains the reference standard when creatinine-eGFR is unreliable.

---

## Bibliography

[1]. Ávila M, Mora Sánchez MG, Bernal Amador AS, Paniagua R. The metabolism of creatinine and its usefulness to evaluate kidney function and body composition in clinical practice. *Biomolecules*. 2025;15(1):41. PMID: 39858438. DOI: 10.3390/biom15010041 — tag: mechanism_review — tier: 2

[2]. Rácz O, Lepej J, Fodor B, Lepejová K, Jarčuška P, Kováčová A. Pitfalls in the measurements and assessment of glomerular filtration rate and how to escape them. *EJIFCC*. 2012;23(2):33–40. PMID: 27683410 — tag: mechanism_review — tier: 2

[3]. Thompson LE, Joy MS. Endogenous markers of kidney function and renal drug clearance processes of filtration, secretion, and reabsorption. *Curr Opin Toxicol*. 2022;30:100338. PMID: 36777447. DOI: 10.1016/j.cotox.2022.03.005 — tag: mechanism_review — tier: 2

[4]. Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease. *Kidney Int*. 2024;105(4S):S117–S314. PMID: 38490803. DOI: 10.1016/j.kint.2023.10.018 — tag: regulatory — tier: 1

[5]. Nair S, O'Brien SV, Hayden K, Pandya B, Lisboa PJG, Hardy KJ, Wilding JPH. Effect of a cooked meat meal on serum creatinine and estimated glomerular filtration rate in diabetes-related kidney disease. *Diabetes Care*. 2014;37(2):483–487. PMID: 24062331. DOI: 10.2337/dc13-1770 — tag: cohort — tier: 1

[6]. Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2012 clinical practice guideline for the evaluation and management of chronic kidney disease. *Kidney Int Suppl*. 2013;3(1):1–150 — tag: regulatory — tier: 1

[7]. Kidney Disease: Improving Global Outcomes (KDIGO) AKI Work Group. KDIGO Clinical Practice Guideline for Acute Kidney Injury. *Kidney International Supplements*. 2012;2(1):1–138 — tag: regulatory — tier: 2

[8]. Inker LA, Eneanya ND, Coresh J, Tighiouart H, Wang D, Sang Y, Crews DC, Doria A, Estrella MM, Froissart M, Grams ME, Greene T, et al. (CKD-EPI Collaboration). New creatinine- and cystatin C–based equations to estimate GFR without race. *N Engl J Med*. 2021;385(19):1737–1749. PMID: 34554658. DOI: 10.1056/NEJMoa2102953 — tag: cohort — tier: 1

[9]. Kannapiran M, Nisha D, Madhusudhana Rao A. Underestimation of impaired kidney function with serum creatinine. *Indian J Clin Biochem*. 2010;25(4):380–384. PMID: 21966109. DOI: 10.1007/s12291-010-0080-4 — tag: cohort — tier: 2

[10]. Murty MSN, Sharma UK, Pandey VB, Kankare SB. Serum cystatin C as a marker of renal function in detection of early acute kidney injury. *Indian J Nephrol*. 2013;23(3):180–183. PMID: 23814415. DOI: 10.4103/0971-4065.111840 — tag: cohort — tier: 2

[11]. Zhang X, Rule AD, McCulloch CE, Lieske JC, Ku E, Hsu C-Y. Tubular secretion of creatinine and kidney function: an observational study. *BMC Nephrol*. 2020;21(1):108. PMID: 32228497. DOI: 10.1186/s12882-020-01736-6 — tag: cohort — tier: 2

[12]. Levey AS, Coresh J, Greene T, Stevens LA, Zhang YL, Hendriksen S, Kusek JW, Van Lente F; Chronic Kidney Disease Epidemiology Collaboration. Using standardized serum creatinine values in the modification of diet in renal disease study equation for estimating glomerular filtration rate. *Ann Intern Med*. 2006;145(4):247–254. PMID: 16908915 — tag: cohort — tier: 1

[13]. Levey AS, Stevens LA, Schmid CH, Zhang YL, Castro AF 3rd, Feldman HI, Kusek JW, Eggers P, Van Lente F, Greene T, Coresh J; CKD-EPI Collaboration. A new equation to estimate glomerular filtration rate. *Ann Intern Med*. 2009;150(9):604–612. PMID: 19414839 — tag: cohort — tier: 1

[14]. National Kidney Foundation. CKD-EPI Creatinine Equation (2021). National Kidney Foundation. https://www.kidney.org/ckd-epi-creatinine-equation-2021-0. Accessed 2026 — tag: regulatory — tier: 2

[15]. Delanghe JR, Speeckaert MM. Creatinine determination according to Jaffe — what does it stand for? *Clin Kidney J*. 2011;4(2):83–86. DOI: 10.1093/ndtplus/sfq211 — tag: mechanism_review — tier: 1

[16]. Cobbaert CM, Baadenhuijsen H, Weykamp CW. Prime time for enzymatic creatinine methods in pediatrics. *Clin Chem*. 2009;55(3):549–558. DOI: 10.1373/clinchem.2008.116863 — tag: mechanism_review — tier: 1

[17]. Syme NR, Stevens K, Stirling C, McMillan DC, Talwar D. Clinical and analytical impact of moving from Jaffe to enzymatic serum creatinine methodology. *J Appl Lab Med*. 2020;5(4):631–642. DOI: 10.1093/jalm/jfaa053 — tag: mechanism_review — tier: 1

[18]. Nankivell BJ, Nankivell LFJ, Elder GJ, Gruenewald SM. How unmeasured muscle mass affects estimated GFR and diagnostic inaccuracy. *eClinicalMedicine* (The Lancet). 2021;31:100686. PMID: 33437955 — tag: cohort — tier: 1

[19]. Pottel H, Cavalier E, Björk J, et al. Standardization of serum creatinine is essential for accurate use of unbiased estimated GFR equations: evidence from three cohorts matched on renal function. *Clin Kidney J*. 2022;15(12):2258–2265. DOI: 10.1093/ckj/sfac182 — tag: cohort — tier: 1

[20]. Groothof D, Post A, Polinder-Bos HA, Erler NS, Flores-Guerrero JL, Kootstra-Ros JE, Pol RA, de Borst MH, Gansevoort RT, Gans ROB, Kremer D, Kieneker LM, Bano A, Muka T, Franco OH, Bakker SJL. Muscle mass and estimates of renal function: a longitudinal cohort study. *Journal of Cachexia, Sarcopenia and Muscle*. 2022;13(4):2036–2047. PMID: 35596604 — tag: cohort — tier: 1

[21]. Okamura M, et al. Kidney function in cachexia and sarcopenia: Facts and numbers. *Journal of Cachexia, Sarcopenia and Muscle*. 2023;14(3):1275–1285. PMID: 37222019 — tag: cohort — tier: 1

[22]. National Kidney Disease Education Program (NKDEP) / NIDDK Laboratory Working Group. Creatinine Standardization Program. Bethesda, MD: National Institute of Diabetes and Digestive and Kidney Diseases; 2006 (recommendations); updated 2013 (full IVD manufacturer adoption). https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/creatinine-standardization-program — tag: regulatory — tier: 2

[23]. Voskoboev NV, Larson TS, Rule AD, Lieske JC. Importance of cystatin C assay standardization. *Clin Chem*. 2011;57(8):1209–1211. DOI: 10.1373/clinchem.2011.164798 — tag: mechanism_review — tier: 1

[24]. Blirup-Jensen S, Grubb A, Lindström V, Schmidt C, Althaus H. First certified reference material for cystatin C in human serum ERM-DA471/IFCC. *Clin Chem Lab Med*. 2010;48(11):1619–1621. DOI: 10.1515/CCLM.2010.318 — tag: regulatory — tier: 2

[25]. Lepist EI, Zhang X, Hao J, et al. Contribution of the organic anion transporter OAT2 to the renal active tubular secretion of creatinine and mechanism for serum creatinine elevations caused by cobicistat. *Kidney Int*. 2014;86(2):350–357. PMID: 24646860. DOI: 10.1038/ki.2014.66 — tag: mechanism_review — tier: 1

[26]. Delanaye P, Melsom T, Ebert N, et al. Iohexol plasma clearance for measuring glomerular filtration rate in clinical practice and research: a review. Part 2: Why to measure glomerular filtration rate with iohexol? *Clin Kidney J*. 2016;9(5):700–704. DOI: 10.1093/ckj/sfw071 — tag: mechanism_review — tier: 1

[27]. Matsushita K, van der Velde M, Astor BC, Woodward M, Levey AS, de Jong PE, Coresh J, Gansevoort RT; Chronic Kidney Disease Prognosis Consortium. Association of estimated glomerular filtration rate and albuminuria with all-cause and cardiovascular mortality in general population cohorts: a collaborative meta-analysis. *Lancet*. 2010;375(9731):2073–2081. PMID: 20483451 — tag: meta_analysis — tier: 1

[28]. Chronic Kidney Disease Prognosis Consortium; Matsushita K, Coresh J, Sang Y, Chalmers J, Fox C, Guallar E, Jafar T, Jassal SK, Landman GW, Muntner P, Roderick P, Sairenchi T, Schöttker B, Shankar A, Shlipak M, Tonelli M, Townend J, van Zuilen A, Yamagishi K, Yamashita K, Gansevoort R, Hemmelgarn B, Woodward M, Levey AS, Astor BC. Estimated glomerular filtration rate and albuminuria for prediction of cardiovascular outcomes: a collaborative meta-analysis of individual participant data. *Lancet Diabetes & Endocrinology*. 2015;3(7):514–525 — tag: meta_analysis — tier: 1
