---
title: "ALT (Alanine Aminotransferase): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/alt/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.alt-design-work
provenance_slug: labs-specialist
source_count: 35
---

# ALT (Alanine Aminotransferase): Canonical Research Report

## Summary

Alanine aminotransferase (ALT) is the most liver-specific aminotransferase in routine clinical use. It catalyzes the reversible transamination of L-alanine and α-ketoglutarate to produce pyruvate and L-glutamate — a reaction that sits at the intersection of amino-acid catabolism and central carbon metabolism in the liver. Crucially, ALT is a marker of **hepatocellular injury**, not hepatic function. It leaks into the bloodstream when hepatocyte plasma membranes are disrupted; it does not directly reflect the liver's synthetic capacity (albumin, INR, bilirubin). A liver can sustain significant ongoing inflammation and show ALT well above the true healthy threshold while synthetic markers remain normal; conversely, end-stage cirrhosis with minimal viable hepatocyte mass can present with paradoxically low or normal ALT because there is too little functioning hepatocellular tissue left to release the enzyme.

The conventional upper limit of normal (ULN) — typically 30–55 U/L for men and 30–45 U/L for women depending on the laboratory — is derived from unscreened reference populations that include individuals with subclinical hepatic steatosis, unrecognized metabolic dysfunction, and occult viral hepatitis. The landmark Prati et al. (2002) study, using rigorously screened Italian blood donors, established evidence-based healthy ULN thresholds of **30 U/L for men and 19 U/L for women** [10, cohort]. The American College of Gastroenterology 2017 guideline synthesizes multiple cohort studies and places the true healthy range at **29–33 U/L for males and 19–25 U/L for females** [8, regulatory]. This discrepancy between conventional lab cutpoints and the evidence-based healthy threshold means that a meaningful proportion of individuals with early MASLD (metabolic dysfunction-associated steatotic liver disease) and early hepatic fibrosis are falsely reassured by a "normal" ALT result.

ALT is always interpreted alongside AST using the **De Ritis ratio** (AST:ALT). A ratio <1 is characteristic of MASLD and acute viral hepatitis, where cytoplasmic ALT release predominates. A ratio >2 is the hallmark of alcoholic liver disease, driven by alcohol-mediated mitochondrial injury and preferential pyridoxal-phosphate depletion that suppresses ALT more than AST. A ratio rising above 1 in the context of chronic liver disease signals advancing fibrosis and cirrhosis as hepatocyte mass is progressively replaced by scar. Neither enzyme alone carries the diagnostic weight of the two together.

Even high-normal ALT — values within the conventional reference interval — carries prognostic weight: each standard deviation increase in log-ALT in the Framingham Offspring cohort predicted a 48% higher odds of incident type 2 diabetes and a 21% higher odds of incident metabolic syndrome over 20 years [23, cohort]. In the WOSCOPS prevention cohort, men in the top ALT quartile (≥29 U/L) had a hazard ratio of 3.38 (95% CI 1.99–5.73) for new-onset type 2 diabetes versus the lowest quartile (<17 U/L) [33, cohort]. ALT is not merely a liver enzyme: it is an early metabolic warning signal.

Results are reported in U/L (= IU/L). The 12-enum type-tag for this report's sources ranges across mechanism_review, cohort, regulatory, animal, in_vitro, and meta_analysis.

---

## Physiology & What ALT Measures

### What ALT Is

Alanine aminotransferase (ALT) — historically abbreviated SGPT (serum glutamic-pyruvic transaminase) and catalogued by the enzyme commission as GPT (glutamate-pyruvate transaminase, EC 2.6.1.2) — is a cytosolic enzyme found at especially high concentration inside hepatocytes [1, mechanism_review]. Its defining biochemical role is to catalyze the reversible transamination of L-alanine and α-ketoglutarate (2-oxoglutarate) to yield pyruvate and L-glutamate:

> L-alanine + α-ketoglutarate ⇌ pyruvate + L-glutamate

This single reversible step sits at the intersection of amino-acid catabolism and the central carbon pathways of the liver. In the forward direction (amino group leaving alanine), the pyruvate produced can feed directly into gluconeogenesis or the tricarboxylic acid (TCA) cycle; in the reverse direction (amino group entering alanine), the reaction regenerates alanine for export to peripheral tissue [2, animal].

### The Glucose–Alanine (Cahill) Cycle

ALT is the molecular hub of the glucose–alanine cycle, a substrate shuttle between skeletal muscle and liver that helps buffer blood glucose during fasting and exercise. Briefly: muscle transamination generates alanine from pyruvate (using glutamate as amino donor); circulating alanine is taken up by hepatocytes and re-converted to pyruvate by hepatic ALT; that pyruvate enters gluconeogenesis; and the glucose produced is exported back to muscle [2, animal]. The liver is the quantitative endpoint of this cycle, which helps explain why hepatic ALT expression dwarfs that of most other organs: hepatocyte ALT activity substantially exceeds serum ALT activity and surpasses that of any other tissue type [1, mechanism_review].

### Pyridoxal-5'-Phosphate (Vitamin B6) Dependence

Like all aminotransferases, ALT is a PLP-dependent enzyme. Pyridoxal-5'-phosphate acts as the obligate prosthetic group, shuttling between its aldehyde (PLP) and amine (pyridoxamine-5'-phosphate, PMP) forms during each catalytic cycle [3, mechanism_review]. In the first half-reaction, PLP accepts the amino group from L-alanine via a Schiff-base intermediate, converting to PMP while releasing pyruvate. In the second half-reaction, PMP donates the amino group to α-ketoglutarate, regenerating PLP and releasing L-glutamate [1, mechanism_review; 3, mechanism_review]. Because ALT requires PLP for activity, clinical states of vitamin B6 depletion — chronic alcoholism, inflammatory bowel disease, chronic kidney disease — can suppress measured serum ALT and AST values even in the presence of significant hepatocellular injury, a diagnostically relevant pitfall [3, mechanism_review; 4, mechanism_review].

### Two Genes, Two Isoforms

The human genome encodes two distinct ALT proteins from separate genes [5, in_vitro; 6, in_vitro]:

- **ALT1 (GPT1)** is the cytosolic isoform. It predominates in liver and is also expressed in kidney, skeletal muscle, heart, and intestine. Under conditions of hepatocellular injury, the fraction of ALT1 that leaks into plasma closely matches total measured serum ALT activity, confirming ALT1 as the dominant contributor to the standard clinical assay [5, in_vitro].
- **ALT2 (GPT2)** is a mitochondrial matrix protein. It is expressed at higher relative levels in skeletal muscle, brain, heart, and adipose tissue; detectable hepatic ALT2 expression has been reported but is lower than ALT1 in normal liver [2, animal; 6, in_vitro]. Importantly, ALT2 favors the reverse transamination direction (alanine synthesis from pyruvate), consistent with its metabolic role in muscle alanine export, whereas ALT1 favors the forward direction (pyruvate production) in the liver [2, animal].

The practical consequence of this isoform architecture is that elevated serum ALT during liver injury represents primarily leakage of ALT1 from damaged hepatocytes, while isolated elevation from skeletal muscle injury releases proportionately more ALT2 [5, in_vitro]. Isoform-selective measurement is not yet standard clinical practice, but research tools confirm this tissue-source discrimination is biochemically achievable [5, in_vitro].

### Tissue Distribution and Liver Specificity

ALT is present in liver, kidney, cardiac muscle, skeletal muscle, adipose tissue, and intestine, but hepatocytes accumulate by far the highest concentration [1, mechanism_review]. This hepatocyte-dominant distribution makes serum ALT the most liver-specific of the routine aminotransferases in clinical use — more specific than aspartate aminotransferase (AST, EC 2.6.1.1). AST, by contrast, exists in both cytoplasmic and mitochondrial isoforms and is expressed at high levels in cardiac and skeletal muscle, red blood cells, and kidney, in addition to liver [4, mechanism_review]. The consequence is that isolated AST elevation may reflect injury to multiple organ systems, whereas elevated serum ALT points more selectively to hepatocellular disease.

### Release Mechanism: Injury Marker, Not Function Marker

Under physiological conditions, the plasma membrane of the hepatocyte is largely impermeable to intracellular enzymes; serum ALT activity reflects steady-state release from a tiny fraction of cells undergoing normal turnover. When hepatocytes sustain plasma-membrane injury — from viral infection, toxins (including alcohol and drugs), ischemia, or metabolic stress — membrane integrity is lost and intracellular ALT leaks into the sinusoidal space and reaches the systemic circulation [1, mechanism_review; 4, mechanism_review]. The key point is that ALT measures **hepatocellular injury** (disruption of the hepatocyte plasma membrane), not **hepatic synthetic function** — a liver can be inflamed and leaking ALT while its synthetic capacity (reflected by albumin, prothrombin time, bilirubin conjugation) remains intact, and conversely, end-stage cirrhosis with minimal remaining functional hepatocyte mass may show a paradoxically low or falling ALT despite severe functional impairment.

The serum half-life of ALT released from injured hepatocytes is approximately **47 ± 10 hours** [1, mechanism_review]. This relatively long half-life (compared with, for example, α-glutathione S-transferase at ~90 minutes) means that serum ALT tends to lag behind the onset and resolution of acute injury, rising gradually over the first few days and returning to baseline over one to two weeks after the injury resolves.

### The AST:ALT (De Ritis) Ratio

Because AST and ALT are released together during liver injury but originate from different subcellular compartments and different organ distributions, their ratio — the **De Ritis ratio**, first described by Fernando De Ritis in 1957 — carries additive diagnostic information beyond either enzyme alone [7, mechanism_review]. In most acute hepatocellular insults (viral hepatitis, ischemic hepatitis, drug-induced liver injury), ALT exceeds or equals AST (De Ritis ratio ≤ 1), reflecting predominantly cytosolic enzyme leakage. In alcoholic liver disease, where mitochondrial injury is prominent and hepatic pyridoxine depletion preferentially suppresses ALT synthesis, the ratio characteristically exceeds 2:1 [7, mechanism_review]. Advancing fibrosis and cirrhosis also tend to raise the ratio as hepatocyte mass is replaced by scar and mitochondrial AST is proportionately released. In practice, ALT and AST are always interpreted together — the ratio is a signal not captured by either value in isolation.

---

## Reference Ranges, Units & The ULN Debate

### Units

ALT activity is reported in **U/L (units per liter)**, synonymous with IU/L (international units per liter). Some older literature and European references express the same quantity in nkat/L (nanokatal per liter); the conversion is 1 U/L ≈ 16.67 nkat/L. The analytic term is alanine aminotransferase activity, not concentration.

### Conventional Laboratory Reference Ranges

Laboratories derive their reference intervals statistically — typically the central 95th percentile of a local or vendor-defined reference population — without systematic exclusion of individuals with subclinical liver disease. Under this approach, the conventional adult **upper limit of normal (ULN)** for ALT commonly falls between **30 and 55 U/L**, with significant lab-to-lab variability [8, regulatory].

Sex dependence is consistent across all populations studied: men carry higher physiological ALT activity than women, reflecting differences in muscle mass, androgen-mediated hepatic enzyme induction, and body composition [8, regulatory]. A 2008 analysis of 11 laboratories within the NASH Clinical Research Network found female ULNs ranging from 31 to 55 U/L and male ULNs from 35 to 79 U/L — a more than two-fold spread for the same biomarker across institutions using different assay methods and reference populations [9, mechanism_review]. This heterogeneity is not a minor calibration issue: a single standardized serum sample was classified as "normal" by some labs and "elevated" by others, depending solely on local ULN [9, mechanism_review].

The Mayo Clinic reference range (7–55 U/L men; 7–45 U/L women) and LabCorp adult range (<45 U/L men; <33 U/L women) illustrate how wide real-world lab cutpoints can be. These figures should never be treated as biologically derived definitions of health.

### The Load-Bearing Controversy: The Standard ULN Is Set Too High

The conventional ULN has been criticized on methodological grounds since the early 2000s, and the evidence has only accumulated since. The core argument: reference ranges set from unscreened populations include individuals with unrecognized hepatic steatosis, metabolic dysfunction, subclinical viral hepatitis, and alcohol-related injury. The "normal" range therefore reflects the distribution of the general population — not the distribution of the healthy population.

#### The Prati 2002 Landmark

The pivotal paper is **Prati et al. (2002)**, published in *Annals of Internal Medicine* [10, cohort]. The authors studied 6,835 first-time blood donors in Milan, Italy (1995–1999), initially considered metabolically healthy but then rigorously screened: exclusion criteria included HCV seropositivity, BMI >25 kg/m², dyslipidemia, hyperglycemia, and other risk factors for liver disease. ALT was independently associated with BMI and with laboratory markers of abnormal lipid or carbohydrate metabolism — demonstrating that a meaningful fraction of conventionally "normal" subjects carry metabolic liver burden.

After excluding all high-risk individuals, the investigators derived **updated healthy ULN thresholds of 30 U/L for men and 19 U/L for women** — substantially lower than the then-current laboratory cutpoints of 40 U/L (men) and 30 U/L (women). They then validated these thresholds in a separate HCV-antibody-positive cohort with biopsy data: the lower, risk-stratified cutpoints showed meaningfully superior sensitivity for identifying HCV viremia with minimal-to-mild histologic lesions (76.3% vs. 55.0%) at an acceptable tradeoff in specificity.

The practical implication was direct: individuals with ALT levels between 19 and 30 U/L (women) or between 30 and 40 U/L (men) who were being told their liver enzymes were "normal" were, in a subset of cases, carrying early hepatocellular injury that the conventional ULN was not designed to detect.

#### Corroboration from NHANES: Ruhl and Everhart 2012

**Ruhl and Everhart (2012)** extended this analysis to the U.S. population using data from the National Health and Nutrition Examination Survey (NHANES 1999–2008) [11, cohort]. Among 3,747 low-risk adult participants (HCV-negative, hepatitis B surface antigen-negative, low alcohol consumption, no diabetes, normal BMI and waist circumference), they identified optimal ALT cutpoints for discriminating HCV RNA-positive individuals from the low-risk group. Maximum correct classification was achieved at **ALT = 29 U/L for men** (88% sensitivity, 83% specificity) and **22 U/L for women** (89% sensitivity, 82% specificity). The area under the ROC curve was 0.929 for men and 0.915 for women — strong discrimination. Critically, if these lower cutpoints were applied to the full U.S. population, 36.4% of men and 28.3% of women would be classified as having elevated ALT — far higher than conventional lab flagging rates, a signal of how many individuals with metabolic-hepatic dysfunction pass undetected.

#### Corroboration from Biopsy-Proven Normal Liver Cohort: Lee et al. 2010

**Lee et al. (2010)** took a distinct approach: 1,105 living liver donors in Korea with biopsy-confirmed normal liver histology [12, cohort]. Among 665 individuals meeting modified Prati criteria (BMI <23 kg/m² for Asian cutpoints), healthy ALT thresholds were **33 U/L for men and 25 U/L for women**. Age and BMI were independently correlated with ALT levels even in this histologically confirmed normal-liver group, reinforcing that metabolic phenotype — not just the presence or absence of disease — shapes where ALT sits.

### Guideline Synthesis: What Regulatory Bodies Say

#### ACG 2017 (Kwo, Cohen, and Lim)

The **American College of Gastroenterology 2017 Clinical Guideline on Evaluation of Abnormal Liver Chemistries** — the most-cited U.S. guidance on this topic — explicitly reconciles the population-study literature [8, regulatory]. The guideline states:

> "A true healthy normal ALT level in prospectively studied populations without identifiable risk factors for liver disease ranges from **29–33 IU/L for males and 19–25 IU/L for females**, and levels above this should be assessed by physicians."

The document also notes that elevated ALT above the population-derived ULN is associated with increased liver-related mortality even when it does not exceed the conventional laboratory ULN. The ACG guideline simultaneously acknowledges that clinicians may still rely on local laboratory ULN ranges for alkaline phosphatase and bilirubin — but for ALT specifically, it endorses the tighter, risk-stratified thresholds.

The ACG guideline tabulates the evidence base behind these numbers, summarizing multiple cohort studies (including Prati, Lee, and Ruhl/Everhart) showing a consistent convergence around 29–33 U/L (men) and 19–25 U/L (women) when derived from truly healthy reference populations [8, regulatory].

#### AASLD 2018 Hepatitis B Guidance (Terrault et al.)

For the clinical context of chronic hepatitis B management, the **AASLD 2018 Hepatitis B Guidance** adopts a slightly relaxed but still sex-stratified threshold: **35 U/L for males and 25 U/L for females**, explicitly justified as a practical management cutpoint [13, regulatory]. The guidance acknowledges that healthy-population data support 29–33/19–25 U/L but uses the higher male cutpoint for treatment-decision purposes to balance sensitivity against unnecessary intervention in the HBV monitoring context.

### Why This Matters: MASLD and the False Reassurance Problem

The MASLD (metabolic dysfunction-associated steatotic liver disease) epidemic has made this debate clinically urgent. A substantial proportion of individuals with hepatic steatosis — and even with early fibrosis — have ALT values that are "normal" by conventional lab criteria [8, regulatory]. A patient with ALT of 38 U/L receives a normal flag from many labs; under the ACG-endorsed healthy threshold of 29–33 U/L, that same value signals a liver-function deviation warranting investigation.

This false reassurance problem has real downstream consequences: primary care screening for MASLD based on standard LFTs misses a meaningful fraction of cases. The ACG guideline explicitly states that a normal ALT by laboratory ULN does not exclude significant liver disease — and that the degree of ALT elevation above any reference point guides the evaluation algorithm, not the simple normal/abnormal lab flag [8, regulatory].

### Interpretation by Magnitude: ×ULN Bands

When ALT is elevated above any ULN — conventional or risk-adjusted — the magnitude of elevation shapes the differential and urgency:

- **Borderline / mild elevation (<5× ULN):** The most common finding. Differential includes MASLD/NAFLD, alcohol-related liver disease (mild), medication-related hepatotoxicity, thyroid dysfunction, celiac disease, and chronic viral hepatitis (early or quiescent). Warrants workup but rarely urgent [8, regulatory].
- **Moderate elevation (5–15× ULN):** Broadly suggestive of active hepatocellular injury. Acute viral hepatitis (A, B, C, E), drug-induced liver injury (DILI), autoimmune hepatitis, and exacerbations of chronic liver disease fall here. Timely evaluation is warranted [8, regulatory].
- **Marked / severe elevation (>15× ULN):** Ischemic hepatopathy ("shock liver"), toxic hepatitis, acute viral hepatitis with high-level replication, and Budd-Chiari syndrome dominate at this level. Values >10,000 U/L are almost exclusively seen with ischemic hepatopathy or drug/toxin-induced injury. Requires immediate evaluation [8, regulatory].

These bands are referenced against whatever ULN the interpreting clinician uses — which is why standardization of the ULN itself is not merely academic.

### Age, Sex, and BMI Dependence

Beyond the male-female gap, ALT varies with:

- **Age:** ALT is not age-invariant. Levels tend to be higher in younger adults (particularly males aged 18–40), decline somewhat in older age, and in women show a pattern modulated by hormonal changes across the lifespan [9, mechanism_review].
- **BMI:** The relationship between BMI and ALT is linear and independent of other risk factors, documented in multiple cohorts [10, cohort]. Even within a "normal BMI" range, higher adiposity tracks with higher ALT — a reflection of the hepatic fat load that subclinical metabolic dysfunction imposes before formal obesity thresholds are crossed.
- **AST:ALT ratio (De Ritis ratio):** In early, cytoplasmic-predominant hepatocellular injury (including MASLD), ALT often exceeds AST because ALT is predominantly cytoplasmic; the De Ritis ratio (AST/ALT) is typically <1. In alcohol-associated liver disease, AST disproportionately rises (>2:1 AST:ALT in ~90% of cases) because of alcohol-mediated depletion of pyridoxal phosphate (needed for ALT synthesis) and release of mitochondrial AST. In advanced cirrhosis from any cause, the ratio can reverse as hepatocyte mass declines and ALT-generating capacity falls [8, regulatory].

### No Universal Cutpoint

There is no single correct ALT ULN. The reference interval is method-dependent (assay calibration, reaction temperature, and substrate vary across platforms), population-dependent (BMI distribution, ethnicity, metabolic disease prevalence in the reference cohort), and sex-dependent. The ACG 2017 guideline and the population studies converge on 29–33 U/L (men) / 19–25 U/L (women) as the best current approximation of a health-based threshold — but this does not mean every clinical laboratory should immediately abandon its local ULN. It means that clinicians interpreting ALT in the context of metabolic health, MASLD risk, and early liver disease detection should apply the stricter, evidence-based reference frame, not the local-lab convenience cutpoint.

---

## Measurement & Standardization

### The IFCC Reference Measurement Procedure

The gold-standard reference procedure for measuring ALT catalytic activity is the IFCC primary reference procedure at 37°C, published in 2002 as Part 4 of the IFCC series on enzyme measurement at 37°C [3, mechanism_review]. This procedure was derived from the earlier 30°C IFCC reference method and is operated by the IFCC Committee on Reference Systems of Enzymes (C-RSE). The 37°C temperature is now universal for all IFCC enzyme reference procedures, replacing earlier 25°C and 30°C methods that produced systematically lower absolute values and impaired comparability across eras and regions.

### The Routine Assay: Coupled Enzymatic-Spectrophotometric Method

In routine automated laboratory practice, ALT is measured by a two-step coupled enzymatic reaction monitored spectrophotometrically. The primary reaction, catalyzed by ALT itself, transfers an amino group from L-alanine to α-ketoglutarate, producing pyruvate and L-glutamate:

> L-alanine + α-ketoglutarate → pyruvate + L-glutamate

The indicator (coupled) reaction then reduces the pyruvate to L-lactate via lactate dehydrogenase (LDH) in the presence of NADH:

> pyruvate + NADH + H⁺ → L-lactate + NAD⁺

The rate of absorbance decrease at 340 nm — where NADH absorbs strongly and NAD⁺ does not — is directly proportional to ALT catalytic activity. Results are reported in units per liter (U/L), where 1 U = the amount of enzyme catalyzing 1 µmol of substrate per minute under defined conditions. This coupled-reaction design is chemically analogous to the AST assay but uses L-alanine as substrate and LDH (rather than malate dehydrogenase) as the indicator enzyme.

### Pyridoxal-5'-Phosphate (P5P) Supplementation: The Key Standardization Variable

The most consequential methodological variable in ALT measurement is whether the reagent includes pyridoxal-5'-phosphate (P5P, also called PLP or vitamin B6 coenzyme). ALT is a pyridoxal-phosphate-dependent enzyme; P5P serves as its essential coenzyme. The IFCC reference procedure specifies P5P supplementation in the reagent to saturate the apoenzyme, ensuring that measured activity reflects the full catalytic potential of the ALT protein present — independent of the patient's circulating B6 status.

When P5P is omitted from the reagent, ALT activity measured depends partly on the patient's endogenous vitamin B6 level. In B6-replete patients this gap is modest, but in individuals with vitamin B6 deficiency — a condition more prevalent than often appreciated — ALT is systematically underestimated. A 2026 analysis of ALT and AST harmonization documented that addition of P5P to the reagent produced an average increase of approximately 12% in ALT concentrations across a mixed clinical population; in the subset with confirmed vitamin B6 deficiency (defined as serum PLP < 20 nmol/L), the underestimation was proportionally larger [14, mechanism_review]. In a clinical B6 deficiency cohort (hemodialysis patients), measured plasma ALT was 8.6 ± 0.6 U/L in deficient patients versus 11.4 ± 0.9 U/L in B6-replete controls — roughly 25% lower — and enzyme activity partially normalized after vitamin B6 supplementation, confirming B6 status as the causal variable [15, cohort].

Despite the IFCC recommendation, more than 60% of laboratories in the United States and internationally have used ALT assays not supplemented with P5P [14, mechanism_review]. This creates a systematic, patient-state-dependent negative bias in non-P5P methods and undermines traceability to the IFCC reference procedure. Laboratories using non-P5P reagents cannot achieve true metrological traceability to the IFCC primary reference and should apply method-specific reference intervals; applying IFCC-derived cutoffs to non-P5P results risks misclassifying elevated ALT as normal in B6-deficient patients.

### Standardization and Harmonization

The IFCC primary reference procedure anchors metrological traceability. One certified reference material exists in the JCTLM database — ERM®-AD454k/IFCC — against which routine method calibrators are theoretically traceable. However, commutability of this material across routine methods is not uniformly established, representing a practical limitation to full standardization.

The real-world consequence of incomplete harmonization is substantial. A large study across 223 US Veterans Health Administration laboratories — 22,950 ALT measurements from 80 proficiency-testing samples — found that analyzer manufacturer was independently associated with ALT result, with a mean inter-manufacturer difference of 10.4 U/L across all samples and a mean difference of 15.4 U/L for samples with mean ALT below 50 U/L (i.e., the clinically critical range where ULN decisions are made) [16, cohort]. Beckman Coulter, Roche, Siemens, and Vitros platforms produced systematically different values on identical samples. The authors concluded that universal ALT cutoffs should not be applied across platforms until inter-manufacturer variability is resolved.

An IFCC multicenter study (centers in Milan, Beijing, Bursa, and Nordic countries; n = 765 subjects) established method-specific IFCC reference intervals at 37°C as: ALT 8–41 U/L (female) and 9–59 U/L (male), with no significant regional differences in this study [17, cohort]. Preliminary upper reference limits from the IFCC's own inter-laboratory work were 34 U/L (female) and 45 U/L (male) at the 97.5th percentile, providing the method-anchored benchmarks that commercial platforms are expected to approach [18, cohort].

A statewide study of Indiana laboratories found that 83% of laboratories simply adopted their analyzer manufacturer's stated reference interval rather than conducting in-house healthy-volunteer studies, and those manufacturer intervals varied substantially across platforms [19, cohort]. This practice explains why stated ULN values for ALT in common use range from roughly 30 to 65 U/L depending on the laboratory — a range large enough to reclassify individual patients across clinical decision thresholds.

### Pre-analytical Considerations and Interferences

**Hemolysis.** ALT is relatively resistant to hemolysis interference. In an interference study, ALT concentrations were not clinically affected at hemoglobin concentrations up to 2.5–4.5 g/L (severely hemolyzed samples) — in marked contrast to AST and LDH, which are significantly elevated even at hemoglobin < 0.5 g/L (barely visible hemolysis) due to high intracellular concentrations of those enzymes in erythrocytes [20, cohort]. Mildly or moderately hemolyzed specimens are therefore acceptable for ALT measurement, whereas AST and LDH results from the same tube may need rejection or flagging.

**Lipemia.** Lipemic samples can introduce optical interference in spectrophotometric assays; on-board lipemia correction algorithms in modern analyzers partially mitigate but do not fully eliminate this effect at extreme lipemia.

**Sample stability.** ALT in serum is relatively stable but temperature-sensitive. A multi-platform stability study found ALT declines at approximately −4.8%/day at room temperature but only −0.9%/day under refrigeration — roughly a 5-fold improvement in stability with refrigeration [21, cohort]. Samples should be separated and refrigerated promptly; refrigerated serum is stable for several days, whereas room-temperature delays of more than a day introduce meaningful negative bias.

**Vitamin B6 status (P5P effect).** As detailed above, patient B6 deficiency is a pre-analytical variable in the biological sense: it reduces the apparent ALT in non-P5P assays. Populations at elevated risk of B6 deficiency include hemodialysis patients, those with malabsorption, and individuals with chronic inflammatory states.

**Diurnal and day-to-day biological variation.** ALT does not exhibit significant diurnal (within-day) variation, unlike cortisol or iron; fasting state at the time of draw is not required for routine clinical interpretation. There is, however, meaningful day-to-day intraindividual biological variation (coefficient of variation on the order of 10–15% within a healthy individual over weeks), which means that a single borderline-elevated value should be interpreted in the context of serial measurements before clinical action.

### Why Reference Intervals and ULN Are Method- and Population-Specific

The foregoing discussion converges on a single interpretive principle: the upper limit of normal (ULN) for ALT is not a universal biological constant but an analytical-and-statistical construct that depends on (a) assay temperature (37°C vs. older 30°C methods), (b) P5P supplementation status, (c) calibration traceability and commutability, (d) the demographic composition of the reference population (sex, age, BMI, metabolic health), and (e) the statistical threshold applied (95th vs. 97.5th percentile). Laboratories using non-IFCC-traceable, non-P5P methods must validate their own reference intervals rather than importing cutoffs from IFCC-anchored studies. Cross-institution comparisons of ALT results — for clinical trials, referral decisions, or population screening — require knowledge of the assay platform, P5P status, and reference interval in use at each site.

---

## Determinants & Clinical Significance

ALT elevation is not a diagnosis — it is a signal that demands interpretation in context: magnitude, pattern relative to AST, concurrent markers, and clinical setting together narrow the differential considerably.

### Differential by Magnitude of Elevation

#### Mild-to-Moderate Chronic Elevation (<5× ULN)

**Metabolic dysfunction-associated steatotic liver disease (MASLD, formerly NAFLD) is the leading cause of unexplained ALT elevation in developed populations.** ALT rises primarily from hepatocellular cytoplasmic release in the setting of hepatic steatosis and low-grade inflammation; however, the correlation between ALT and histological severity is imperfect — more than 80% of individuals with MASLD have normal ALT by conventional reference ranges, which underscores both the sensitivity limitation and the argument for lowered ULN thresholds [22, mechanism_review]. Goessling et al. in the Framingham Offspring cohort (n=2,812; 20-year follow-up) found that each 1 standard deviation increase in log-ALT within the normal range predicted incident metabolic syndrome (OR 1.21; p<0.001) and incident diabetes (OR 1.48; p<0.001), confirming that "normal" ALT carries prognostic weight even below the current ULN [23, cohort].

Other common causes in the mild-moderate range include:

- **Alcohol-related liver disease (ALD):** classically produces an AST-dominant pattern (see De Ritis ratio section) with both enzymes typically below 300 U/L, even in alcoholic hepatitis.
- **Chronic viral hepatitis B and C:** ALT elevation is the canonical monitoring marker, though ALT may be normal despite active viral replication and significant fibrosis (see Limitations).
- **Drug- and herb-induced liver injury (DILI):** acetaminophen at therapeutic doses rarely elevates ALT substantially, but supratherapeutic or chronic use is a leading cause of DILI; statins cause a mild, usually transient, dose-dependent ALT rise in roughly 1–3% of patients; antibiotics (amoxicillin-clavulanate, fluoroquinolones), isoniazid, methotrexate, and many herbal supplements are additional culprits. DILI surveillance uses the ALT threshold of ≥3× ULN as an action trigger; Hy's Law — ALT ≥3× ULN plus total bilirubin ≥2× ULN in the absence of biliary obstruction — predicts approximately 10% mortality from acute hepatocellular DILI and is the FDA's key safety signal in clinical trials [24, mechanism_review].
- **Hereditary hemochromatosis, autoimmune hepatitis, Wilson disease, α1-antitrypsin deficiency:** each can present with a mild-moderate pattern; absence of other stigmata does not exclude them.
- **Celiac disease and thyroid dysfunction (hypo- and hyperthyroidism):** non-hepatic systemic causes, often correctable.

#### Marked Elevation (>10–25× ULN)

Abrupt, large elevations indicate acute hepatocellular necrosis rather than chronic inflammatory smoldering:

- **Acute viral hepatitis (A, B, E):** ALT typically rises before jaundice and may reach 25–100× ULN.
- **Ischemic hepatitis ("shock liver"):** perhaps the most dramatic transaminase elevations encountered clinically. The condition is defined by acute reversible ALT or AST elevation of ≥20× ULN in the appropriate hemodynamic context (cardiac failure, septic shock, respiratory failure), with centrilobular necrosis on histology. Serum levels peak within 1–3 days of the ischemic event and normalize within 7–14 days with circulatory correction [25, cohort].
- **Acetaminophen and toxic hepatitis:** acetaminophen overdose can drive ALT to thousands of U/L (>100× ULN); values in this range should always prompt questioning about ingestion even if denied.
- **Acute biliary obstruction:** a transient, large transaminase spike — sometimes exceeding 10× ULN — can occur in the first 24–48 hours of common bile duct obstruction by a gallstone, before the ALP/bilirubin picture dominates. This resolves rapidly once obstruction is relieved.

### The AST:ALT (De Ritis) Ratio

The ratio of AST to ALT — the De Ritis ratio — was first described in 1957 and carries substantial differential diagnostic information [7, mechanism_review].

**Ratio >2 → Alcoholic liver disease.** Cohen and Kaplan (1979) observed that an AST:ALT ratio above 2.0 predicted biopsy-confirmed alcoholic liver disease with high specificity [7, mechanism_review]. The mechanistic basis: (a) alcohol-induced mitochondrial injury preferentially releases mitochondrial AST; (b) alcohol depletes pyridoxal-5-phosphate (vitamin B6), a cofactor for ALT synthesis more than for AST, selectively suppressing ALT; (c) hepatic ALT content is reduced in established ALD. Nyblom et al. studied 313 withdrawal-group alcohol-dependent patients plus 48 with confirmed alcoholic cirrhosis and found the ratio ≥2.0 in **69% of cirrhotic patients** [26, cohort]. Critically, the same group showed that a high AST:ALT ratio in ALD is a marker of **advanced disease** — alcoholic cirrhosis — rather than merely heavy drinking; most actively drinking patients without severe liver disease have a ratio ≤1.0. Both AST and ALT are usually below 300 U/L in ALD even when markedly elevated relative to ULN.

**Ratio <1 → MASLD and acute viral hepatitis.** In early MASLD and acute viral hepatitis, hepatocellular cytoplasmic ALT release is proportionally greater, producing a ratio typically <1. The Goessling Framingham cohort confirmed that the dominant pattern in metabolic liver disease is ALT elevation relative to AST [23, cohort].

**Rising ratio >1 in chronic liver disease → advancing fibrosis / cirrhosis.** As chronic viral hepatitis, MASLD, or other causes progress toward cirrhosis, hepatocellular mass decreases (lowering ALT production), while fibrotic and hemodynamic disturbances elevate AST proportionally. Nyblom et al. demonstrated in 160 PBC patients that the AST:ALT ratio was significantly higher in cirrhotic versus non-cirrhotic patients and was associated with esophageal varices and ascites [27, cohort]. Lai et al. (2024) confirmed in a prospective cohort of 1,754 chronic HBV patients (59 cirrhosis events; median follow-up 2.6 years) that an elevated AST:ALT ratio independently predicted cirrhosis (HR 2.77; P=8.25×10⁻⁴) [28, cohort].

### What Lowers ALT — Including the Frailty Signal

A low ALT has historically been dismissed as unremarkable. This is a clinical error.

**Vitamin B6 (pyridoxal-5-phosphate) deficiency:** ALT requires pyridoxal-5-phosphate as a cofactor; deficiency suppresses enzyme activity, causing artifactual under-reading of true hepatocellular injury. This is a recognized mechanism in hemodialysis patients, where pyridoxine is dialyzed out [29, mechanism_review].

**Chronic kidney disease / hemodialysis:** CKD and dialysis patients have systematically low ALT — mean values of ~7 IU/L versus normal reference ranges — partly via B6 depletion, partly via altered enzyme clearance. The conventional ULN for ALT is not valid in this population; the diagnostic threshold for liver injury must be reduced accordingly [29, mechanism_review].

**Low ALT as a marker of frailty, sarcopenia, and increased mortality:** The most clinically underappreciated meaning of a low ALT is its reflection of reduced lean tissue mass and hepatic synthetic reserve. Vespasiani-Gentilucci et al. followed 765 community-dwelling adults ≥65 years (mean 75.3 years; InCHIANTI cohort) and found ALT inversely associated with frailty, sarcopenia, disability, and pyridoxine deficiency. In multiple-adjusted models, each unit increase in ALT predicted lower all-cause mortality (HR 0.98; 95% CI 0.96–1.00; p=.02) and lower cardiovascular mortality (HR 0.94; 95% CI 0.90–0.98; p<.01), with subjects in the lower ALT quintiles showing a sharply elevated risk in a J-shaped relationship [30, cohort]. In myelodysplastic syndrome patients (median age 74.3 years; n=831), Uliel et al. confirmed that low ALT (<12 IU/L) was present in 28% and independently associated with a 25% increase in mortality (HR 1.25; 95% CI 1.01–1.56; p=.041) after full adjustment [31, cohort]. Liu et al.'s meta-analysis (12 cohort studies; n=206,678; 16,249 deaths) formalized this pattern: in adults ≥70 years, each 5 U/L increase in ALT was associated with lower all-cause mortality (HR 0.91 per 5 U/L), the inverse of the younger-adult relationship; in the youngest populations, elevated ALT predicted liver disease mortality (HR 1.24 per 5 U/L) [32, meta_analysis]. Together these data establish low ALT in the elderly as a biomarker of physiological reserve depletion — not liver health.

### ALT as a Metabolic and Prognostic Marker

**High-normal ALT predicts incident metabolic disease.** Goessling et al. demonstrated in the Framingham Offspring cohort over 20 years that ALT within the conventional normal range still predicted incident metabolic syndrome (OR 1.21 per SD log-ALT; p<0.001), incident type 2 diabetes (OR 1.48; p<0.001), and cardiovascular disease (HR 1.23 age-sex adjusted, attenuated to non-significance after full metabolic adjustment) [23, cohort]. This metabolic mediation — ALT tracks hepatic fat, which tracks insulin resistance, which drives cardiometabolic risk — explains why ALT elevation precedes overt disease and functions as an early metabolic warning.

**Independent diabetes prediction.** Sattar et al. analyzed 5,974 men in the West of Scotland Coronary Prevention Study (WOSCOPS; mean follow-up 4.9 years; 139 incident diabetes cases) and found men in the top ALT quartile (≥29 U/L) carried a hazard ratio of 3.38 (95% CI 1.99–5.73) for new-onset type 2 diabetes versus the bottom quartile (<17 U/L). After full adjustment for classical risk factors, metabolic syndrome components, and C-reactive protein, the association persisted at HR 2.04 (95% CI 1.16–3.58) [33, cohort].

**Hepatotoxic drug monitoring (Hy's Law context).** ALT is the primary metric for DILI surveillance in clinical practice and drug development. An ALT ≥3× ULN triggers clinical evaluation; ≥5× ULN triggers drug cessation in most guidelines. When ALT ≥3× ULN co-occurs with bilirubin ≥2× ULN (modified Hy's Law), the risk of drug-induced acute liver failure carrying ~10% mortality is established, with spontaneous survival in non-acetaminophen acute liver failure at only 27.1% at 3 weeks [24, mechanism_review].

### Non-Hepatic ALT Elevation: The Muscle Source

ALT is present in skeletal muscle as well as hepatocytes. Strenuous exercise, rhabdomyolysis, inflammatory myopathy, and muscular dystrophies can all elevate ALT without any hepatic pathology. Lim (2020) reviewed the pattern: in rhabdomyolysis with CK ≥1,000 U/L, abnormal ALT was present in 75% of patients and abnormal AST in 93.1%; critically, the AST:ALT ratio averages approximately 3.0 in exertional rhabdomyolysis — a ratio that could be misread as alcoholic liver disease [34, mechanism_review]. The distinguishing feature is **creatine kinase (CK)**: markedly elevated CK (often 10–100× ULN) with parallel AST fall during recovery, absent alkaline phosphatase or bilirubin rise, and contextually appropriate history (recent intense exercise, trauma, drug exposure) establishes the muscular rather than hepatic source.

### Limitations

**A normal ALT does not exclude significant liver disease, including cirrhosis.** Liao et al. demonstrated in 140 Chinese chronic hepatitis B patients with persistently normal ALT (PNALT) that **49.4% of HBeAg-positive and 30.9% of HBeAg-negative patients had significant fibrosis (≥F2) on liver biopsy** [35, cohort]. "Burnt-out" cirrhosis — where end-stage fibrotic replacement has eliminated most viable hepatocytes — can present with normal or even low ALT because there is insufficient functional hepatocellular mass left to release the enzyme. The absence of ALT elevation in advanced chronic liver disease is therefore not reassurance; it may represent the opposite.

Additional limitations: ALT reflects hepatocellular **injury**, not hepatic **function** — synthetic capacity (albumin, INR, bilirubin) is the independent complement. ALT is non-specific across the causes enumerated above. The conventional ULN is population-derived and widely agreed to be too high, particularly for women and metabolically healthy lean individuals.

---

## Bibliography

[1]. Kim WR, Flamm SL, Di Bisceglie AM, Bodenheimer HC; Public Policy Committee of the American Association for the Study of Liver Disease. Serum activity of alanine aminotransferase (ALT) as an indicator of health and disease. Hepatology. 2008;47(4):1363–1370. PMID: 18366115. DOI: 10.1002/hep.22109. https://pubmed.ncbi.nlm.nih.gov/18366115/ — tag: mechanism_review — tier: 1

[2]. Martino MR, Gutiérrez-Aguilar M, Yiew NKH, Lutkewitte AJ, Singer JM, McCommis KS, Ferguson D, Liss KHH, Yoshino J, Renkemeyer MK, Smith GI, Cho K, Fletcher JA, Klein S, Patti GJ, Burgess SC, Finck BN. Silencing alanine transaminase 2 in diabetic liver attenuates hyperglycemia by reducing gluconeogenesis from amino acids. Cell Rep. 2022;39(3):110733. PMID: 35476997. DOI: 10.1016/j.celrep.2022.110733. — tag: animal — tier: 1 — system flag: animal/mouse model

[3]. Schumann G, Bonora R, Ceriotti F, Férard G, Ferrero CA, Franck PFH, Gella FJ, Hoelzel W, Jørgensen PJ, Kanno T, Kessner A, Klauke R, Kristiansen N, Lessinger JM, Linsinger TPJ, Misaki H, Panteghini M, Pauwels J, Schielle F, Schimmel HG, Weidemann G, Siekmann L. IFCC primary reference procedures for the measurement of catalytic activity concentrations of enzymes at 37°C. Part 4. Reference procedure for the measurement of catalytic concentration of alanine aminotransferase. Clin Chem Lab Med. 2002;40(7):718–724. PMID: 12241021. DOI: 10.1515/CCLM.2002.124. https://pubmed.ncbi.nlm.nih.gov/12241021/ — tag: mechanism_review — tier: 1

[4]. Pratt DS, Kaplan MM. Evaluation of abnormal liver-enzyme results in asymptomatic patients. N Engl J Med. 2000;342(17):1266–1271. PMID: 10781624. DOI: 10.1056/NEJM200004273421707. https://pubmed.ncbi.nlm.nih.gov/10781624/ — tag: mechanism_review — tier: 1

[5]. Lindblom P, Rafter I, Copley C, Andersson U, Hedberg JJ, Berg AL, Samuelsson A, Hellmold H, Cotgreave I, Glinghammar B. Isoforms of alanine aminotransferases in human tissues and serum — differential tissue expression using novel antibodies. Arch Biochem Biophys. 2007;466(1):66–77. PMID: 17826732. DOI: 10.1016/j.abb.2007.07.023. — tag: in_vitro — tier: 1 — system flag: cell/tissue model

[6]. Liu L, Zhong S, Yang R, Hu H, Yu D, Zhu D, Hua Z, Shuldiner AR, Goldstein R, Reagan WJ, Gong DW. Expression, purification, and initial characterization of human alanine aminotransferase (ALT) isoenzyme 1 and 2 in High-five insect cells. Protein Expr Purif. 2008;60(1):225–231. PMID: 18508279. DOI: 10.1016/j.pep.2008.04.006. — tag: in_vitro — tier: 1 — system flag: cell/tissue model

[7]. Cohen JA, Kaplan MM. The SGOT/SGPT ratio — an indicator of alcoholic liver disease. Dig Dis Sci. 1979;24(11):835–838. PMID: 520102. DOI: 10.1007/BF01324898. https://pubmed.ncbi.nlm.nih.gov/520102/ — tag: mechanism_review — tier: 1

[8]. Kwo PY, Cohen SM, Lim JK. ACG Clinical Guideline: Evaluation of Abnormal Liver Chemistries. Am J Gastroenterol. 2017;112(1):18–35. DOI: 10.1038/ajg.2016.517. PMID: 27995906. https://pubmed.ncbi.nlm.nih.gov/27995906/ — tag: regulatory — tier: 1

[9]. Neuschwander-Tetri BA, Unalp A, Creer MH; Nonalcoholic Steatohepatitis Clinical Research Network. Influence of local reference populations on upper limits of normal for serum alanine aminotransferase levels. Arch Intern Med. 2008;168(6):663–666. DOI: 10.1001/archinternmed.2007.131. PMID: 18362260. https://pubmed.ncbi.nlm.nih.gov/18362260/ — tag: mechanism_review — tier: 1

[10]. Prati D, Taioli E, Zanella A, Della Torre E, Butelli S, Del Vecchio E, Vianello L, Zanuse F, Mozzi F, Milani S, Conte D, Colombo M, Sirchia G. Updated definitions of healthy ranges for serum alanine aminotransferase levels. Ann Intern Med. 2002;137(1):1–10. DOI: 10.7326/0003-4819-137-1-200207020-00006. PMID: 12093239. https://pubmed.ncbi.nlm.nih.gov/12093239/ — tag: cohort — tier: 1

[11]. Ruhl CE, Everhart JE. Upper limits of normal for alanine aminotransferase activity in the United States population. Hepatology. 2012;55(2):447–454. DOI: 10.1002/hep.24725. PMID: 21987480. https://pmc.ncbi.nlm.nih.gov/articles/PMC3268908/ — tag: cohort — tier: 1

[12]. Lee JK, Shim JH, Lee HC, Lee SH, Kim KM, Lim YS, Chung YH, Lee YS, Suh DJ. Estimation of the healthy upper limits for serum alanine aminotransferase in Asian populations with normal liver histology. Hepatology. 2010;51(5):1577–1583. DOI: 10.1002/hep.23505. PMID: 20162730. https://pubmed.ncbi.nlm.nih.gov/20162730/ — tag: cohort — tier: 1

[13]. Terrault NA, Lok ASF, McMahon BJ, Chang KM, Hwang JP, Jonas MM, Brown RS Jr, Bzowej NH, Wong JB. Update on prevention, diagnosis, and treatment of chronic hepatitis B: AASLD 2018 hepatitis B guidance. Hepatology. 2018;67(4):1560–1599. DOI: 10.1002/hep.29800. PMID: 29405329. https://pmc.ncbi.nlm.nih.gov/articles/PMC5975958/ — tag: regulatory — tier: 1

[14]. Brinc D, Agbor TA, Fabros A, Cheng PL, Kulasingam V, Selvaratnam R. The Harmonization Hurdle — A Case for Pyridoxal-5′-Phosphate. J Appl Lab Med. 2026. DOI: 10.1093/jalm/jfag018. https://academic.oup.com/jalm/advance-article/doi/10.1093/jalm/jfag018/8504010 — tag: mechanism_review — tier: 2

[15]. Ono K, Ono T, Matsumata T. The pathogenesis of decreased aspartate aminotransferase and alanine aminotransferase activity in the plasma of hemodialysis patients: the role of vitamin B6 deficiency. Clin Nephrol. 1995;43(6):405–408. PMID: 7554526. https://pubmed.ncbi.nlm.nih.gov/7554526/ — tag: cohort — tier: 2

[16]. Beste LA, Icardi M, Hunt CM, Gylys-Colwell I, Lowy E, Taylor L, Morgan TR, Chang MF, Maier MM, Cheung R. Alanine Aminotransferase Results Differ by Analyzer Manufacturer in a National Integrated Health Setting, 2012–2017. Arch Pathol Lab Med. 2020;144(6):748–754. PMID: 31697169. https://pubmed.ncbi.nlm.nih.gov/31697169/ — tag: cohort — tier: 2

[17]. Ceriotti F, Henny J, Queraltó J, Ziyu S, Özarda Y, Chen B, Boyd JC, Panteghini M. Common reference intervals for aspartate aminotransferase (AST), alanine aminotransferase (ALT) and γ-glutamyl transferase (GGT) in serum: results from an IFCC multicenter study. Clin Chem Lab Med. 2010;48(11):1593–1601. PMID: 21034260. https://pubmed.ncbi.nlm.nih.gov/21034260/ — tag: cohort — tier: 2

[18]. Schumann G, Klauke R. New IFCC reference procedures for the determination of catalytic activity concentrations of five enzymes in serum: preliminary upper reference limits obtained in hospitalized subjects. Clin Chim Acta. 2003;327(1–2):69–79. PMID: 12482620. https://pubmed.ncbi.nlm.nih.gov/12482620/ — tag: cohort — tier: 2

[19]. Dutta A, Saha C, Johnson CS, Chalasani N. Variability in the upper limit of normal for serum alanine aminotransferase levels: a statewide study. Hepatology. 2009;50(6):1957–1962. PMID: 19787805. https://pubmed.ncbi.nlm.nih.gov/19787805/ — tag: cohort — tier: 2

[20]. Koseoglu M, Hur A, Atay A, Cuhadar S. Effects of hemolysis interferences on routine biochemistry parameters. Biochem Med (Zagreb). 2011;21(1):79–85. PMID: 22141211. https://pubmed.ncbi.nlm.nih.gov/22141211/ — tag: cohort — tier: 2

[21]. Bauça JM, Caballero A, Gómez C, Martínez-Espartosa D, García del Pino I, Puente JJ, Llopis MA, Marzana I, Segovia M, Ibarz M, Ventura M, Salas P, Gómez-Rioja R. Influence of study model, baseline catalytic concentrations and analytical system on the stability of serum alanine aminotransferase. Adv Lab Med. 2020. PMID: 37363778. https://pmc.ncbi.nlm.nih.gov/articles/PMC10158745/ — tag: cohort — tier: 2

[22]. Lonardo A. Alanine aminotransferase predicts incident steatotic liver disease of metabolic etiology: Long life to the old biomarker! World J Gastroenterol. 2024. PMID: 38983954. https://pmc.ncbi.nlm.nih.gov/articles/PMC11230057/ — tag: mechanism_review — tier: 2

[23]. Goessling W, Massaro JM, Vasan RS, D'Agostino RB Sr, Ellison RC, Fox CS. Aminotransferase Levels and 20-year Risk of Metabolic Syndrome, Diabetes, and Cardiovascular Disease. Gastroenterology. 2008;135(6):1935–1944. PMID: 19010326. https://pmc.ncbi.nlm.nih.gov/articles/PMC3039001/ — tag: cohort — tier: 1

[24]. Katarey D, Verma S. Drug-induced liver injury. Clin Med (Lond). 2016;16(Suppl 6):s104–s109. PMID: 27956449. https://pmc.ncbi.nlm.nih.gov/articles/PMC6329561/ — tag: mechanism_review — tier: 2

[25]. Guo G, Wu XZ, Su LJ, Yang CQ. Clinical features of ischemic hepatitis caused by shock with four different types: a retrospective study of 328 cases. Int J Clin Exp Med. 2015;8(11):21065–21073. PMID: 26629201. https://pmc.ncbi.nlm.nih.gov/articles/PMC4659089/ — tag: cohort — tier: 2

[26]. Nyblom H, Berggren U, Balldin J, Olsson R. High AST/ALT ratio may indicate advanced alcoholic liver disease rather than heavy drinking. Alcohol Alcohol. 2004;39(4):336–339. PMID: 15208167. https://pubmed.ncbi.nlm.nih.gov/15208167/ — tag: cohort — tier: 2

[27]. Nyblom H, Björnsson E, Simrén M, Aldenborg F, Almer S, Olsson R. The AST/ALT ratio as an indicator of cirrhosis in patients with PBC. Liver Int. 2006;26(7):840–845. PMID: 16911467. https://pubmed.ncbi.nlm.nih.gov/16911467/ — tag: cohort — tier: 2

[28]. Lai X, Chen H, Dong X, Zhou G, Liang D, Xu F, Liu H, Luo Y, Liu H, Wan S. AST to ALT ratio as a prospective risk predictor for liver cirrhosis in patients with chronic HBV infection. Eur J Gastroenterol Hepatol. 2024. PMID: 38251454. https://pmc.ncbi.nlm.nih.gov/articles/PMC10833202/ — tag: cohort — tier: 1

[29]. Busch M, Göbert A, Franke S, et al. Vitamin B6 Metabolism in Chronic Kidney Disease — Relation to Transsulfuration, Advanced Glycation and Cardiovascular Disease. Nephron Clin Pract. 2010;114(1):c38–c44. PMID: 19816042. https://karger.com/nec/article/114/1/c38/831308/ — tag: mechanism_review — tier: 2

[30]. Vespasiani-Gentilucci U, De Vincentis A, Ferrucci L, Bandinelli S, Antonelli Incalzi R, Picardi A. Low Alanine Aminotransferase Levels in the Elderly Population: Frailty, Disability, Sarcopenia, and Reduced Survival. J Gerontol A Biol Sci Med Sci. 2018;73(1):71–77. PMID: 28633440. https://pubmed.ncbi.nlm.nih.gov/28633440/ — tag: cohort — tier: 1

[31]. Uliel N, Segal G, Perri A, Turpashvili N, Kassif Lerner R, Itelman E. Low ALT, a marker of sarcopenia and frailty, is associated with shortened survival amongst myelodysplastic syndrome patients: A retrospective study. Medicine (Baltimore). 2023;102(18):e33659. PMID: 37115069. https://pubmed.ncbi.nlm.nih.gov/37115069/ — tag: cohort — tier: 2

[32]. Liu Z, Ning H, Que S, Wang L, Qin X, Peng T. Complex Association between Alanine Aminotransferase Activity and Mortality in General Population: A Systematic Review and Meta-Analysis of Prospective Studies. PLoS One. 2014;9(3):e91410. PMID: 24633141. https://pmc.ncbi.nlm.nih.gov/articles/PMC3954728/ — tag: meta_analysis — tier: 1

[33]. Sattar N, Scherbakova O, Ford I, O'Reilly DS, Stanley A, Forrest E, Macfarlane PW, Packard CJ, Cobbe SM, Shepherd J. Elevated alanine aminotransferase predicts new-onset type 2 diabetes independently of classical risk factors, metabolic syndrome, and C-reactive protein in the west of Scotland coronary prevention study. Diabetes. 2004;53(11):2855–2860. PMID: 15504965. https://pubmed.ncbi.nlm.nih.gov/15504965/ — tag: cohort — tier: 1

[34]. Lim AK. Abnormal liver function tests associated with severe rhabdomyolysis. World J Gastroenterol. 2020;26(10):1020–1028. PMID: 32205993. https://pubmed.ncbi.nlm.nih.gov/32205993/ — tag: mechanism_review — tier: 2

[35]. Liao B, Wang Z, Lin S, Xu Y, Yi J, Xu M, Huang Z, Zhou Y, Zhang F, Hou J. Significant Fibrosis Is Not Rare in Chinese Chronic Hepatitis B Patients with Persistent Normal ALT. PLoS One. 2013;8(11):e78620. PMID: 24205292. https://pmc.ncbi.nlm.nih.gov/articles/PMC3808379/ — tag: cohort — tier: 2
