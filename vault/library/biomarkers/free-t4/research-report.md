---
title: "Free T4 (Free Thyroxine): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/free-t4/research-report
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.free-t4-design-work
provenance_slug: labs-specialist
source_count: 38
---

# Free T4 (Free Thyroxine): Canonical Research Report

## Summary

Free thyroxine (fT4) is the biologically active, protein-unbound fraction of circulating T4 — the only portion available for cellular uptake, receptor binding, and enzymatic conversion to the active effector hormone triiodothyronine (T3). Although T4 is the dominant thyroidal secretory product (roughly 80% of thyroid output), more than 99.95% of it circulates bound to thyroxine-binding globulin (TBG), transthyretin, and albumin, rendering it biologically inert in that state. The free fraction — approximately 0.02–0.03% of total T4 — is what the hypothalamic-pituitary-thyroid (HPT) axis regulates and what tissues actually use. In euthyroid adults, fT4 measured by direct immunoassay typically falls within **0.8–1.8 ng/dL (approximately 10–23 pmol/L)** (1 ng/dL = 12.87 pmol/L), though the precise interval is platform-specific and non-transferable between assay systems [1, cohort; 4, mechanism_review].

In clinical practice, fT4 functions primarily as a reflex and confirmatory test following an abnormal TSH result. An elevated TSH with a suppressed fT4 confirms overt primary hypothyroidism; an elevated TSH with a normal fT4 defines subclinical hypothyroidism; a suppressed TSH with an elevated fT4 confirms overt hyperthyroidism. A critical exception is central (pituitary/hypothalamic) hypothyroidism, where TSH is low or inappropriately normal despite true hormone deficiency — here, fT4 is not merely confirmatory but diagnostically essential, as a TSH-only strategy systematically misses the diagnosis [26, mechanism_review]. fT4 is also the primary monitoring endpoint after levothyroxine dose changes in central hypothyroidism (target: above midnormal of the reference range), and is indispensable in the first 4–6 weeks after any dose adjustment in primary hypothyroidism before TSH equilibrates [24, mechanism_review].

Measurement of fT4 presents fundamental analytical challenges. The free fraction circulates at picomolar concentrations and cannot be isolated directly without disturbing the protein-binding equilibrium. The reference measurement procedure (RMP) is equilibrium dialysis followed by isotope-dilution LC-MS/MS, but clinical laboratories universally use automated immunoassays — which are estimates, not true free-fraction separations. Immunoassay values differ from the RMP by up to 30–72%, and different commercial platforms are not interchangeable [18, mechanism_review; 39, mechanism_review]. Three interference classes are of particular clinical relevance: (1) high-dose biotin supplementation (≥5–10 mg/day) produces falsely elevated fT4 and falsely suppressed TSH on streptavidin-based platforms, mimicking hyperthyroidism [19, cohort]; (2) familial dysalbuminemic hyperthyroxinemia (FDH), caused by an albumin mutation that dramatically increases T4 affinity, causes spuriously elevated fT4 on most one-step immunoassays despite clinical euthyroidism [22, cohort]; and (3) heparin activates lipoprotein lipase in vitro, releasing fatty acids that displace T4 from binding proteins and artifactually elevate measured fT4 [23, cohort; 30, mechanism_review]. Pregnancy further degrades immunoassay accuracy; platform-specific biases of 7–29% above the LC-MS/MS reference have been documented in pregnant women [20, cohort], and trimester-specific reference intervals derived with the same assay are required.

---

## Physiology & What Free T4 Measures

### The Dominant Thyroid Secretory Product

Thyroxine (T4; 3,5,3',5'-tetraiodothyronine) is the principal hormone exported by the thyroid gland, comprising roughly 80% of total thyroidal secretory output. Healthy adults produce approximately 80–100 µg (~103–129 nmol) of T4 per day via TSH-driven iodination and coupling of tyrosyl residues on thyroglobulin within the follicular lumen [35, mechanism_review]. This high daily output makes T4 the most abundant circulating thyroid hormone by mass, yet it is not the active effector at the tissue level. T4 functions as a stable, long-half-life (approximately 7 days) prohormone reservoir: its primary biological mission is to supply peripheral tissues with a regulated substrate for local activation [2, mechanism_review].

### A Molecule in Chains: Protein Binding and the Free Fraction

More than 99.95% of circulating T4 travels bound to plasma proteins, rendering it biologically inert in that form. Three carrier proteins partition the total T4 pool [3, mechanism_review]:

- **Thyroxine-binding globulin (TBG):** a 54-kDa serine-protease inhibitor superfamily member that binds approximately 70–75% of total T4 with highest affinity
- **Transthyretin (TTR; formerly thyroxine-binding prealbumin):** a 55-kDa homotetramer that carries ~15–20%
- **Albumin:** a 67-kDa protein with the lowest affinity but enormous capacity, accounting for the remaining ~10%

The result of this near-total sequestration is that only the **free fraction — approximately 0.02–0.03% of total circulating T4** — is available for cellular uptake, receptor binding, and enzymatic conversion [4, mechanism_review]. In absolute terms, this translates to circulating free T4 (fT4) concentrations in the range of roughly **0.7–1.9 ng/dL (approximately 9–24 pmol/L)** in euthyroid adults; method-specific laboratory reference intervals typically cluster around **12–22 pmol/L (0.93–1.71 ng/dL)** using direct immunoassay [5, cohort].

The protein-bound pool acts as a large, stable buffer. Because TBG binding is high-affinity but saturable, and because albumin releases T4 rapidly at capillary surfaces (lowest affinity = fastest off-rate), tissues receive a steady stream of free hormone even though the free pool itself is tiny [3, mechanism_review].

### T4 as a Prohormone: The Deiodinase Activation Step

T4 is chemically defined by four iodine atoms. Removal of the iodine atom at the 5' position of the outer (phenolic) ring by **type 1 (D1) or type 2 (D2) iodothyronine deiodinase** produces triiodothyronine (T3), the biologically active hormone that binds thyroid hormone nuclear receptors (TRα and TRβ) with ~10-fold higher affinity than T4 [2, mechanism_review]. By contrast, **type 3 deiodinase (D3)** removes the inner-ring 5 iodine to yield the metabolically inactive reverse T3 (rT3), shunting T4 away from activation.

Daily T3 production in healthy adults is approximately 25–30 µg (~38–46 nmol), of which only 4–5 µg is directly secreted by the thyroid; the remaining ~80% is produced extrathyroidally by peripheral deiodination of T4 [2, mechanism_review]. D2 is the dominant source (~20 µg/day), operating in the pituitary, hypothalamus, brown adipose tissue, skeletal muscle, and CNS — tissues that largely self-supply their T3 needs from local T4 activation. D1 contributes to the circulating T3 pool from hepatic and renal tissue. This division of labour means T4 is not a mere transit vehicle: the tissue-specific expression of D2 vs. D3 at any given moment determines whether T4 signals are amplified or silenced locally, independent of thyroidal output [2, mechanism_review].

### Why Free T4, Not Total T4?

The clinical measurement of total T4 counts all hormone — bound and free — and therefore conflates two very different quantities: the biologically active pool (free T4) and the inactive reservoir (protein-bound T4). Because carrier-protein concentrations are neither fixed nor physiologically defended, total T4 fluctuates widely without reflecting true thyroid functional status [4, mechanism_review; 6, mechanism_review].

**Conditions that raise TBG** (and therefore raise total T4 while leaving free T4 largely unchanged):
- Pregnancy: rising estrogen stimulates hepatic TBG synthesis and reduces TBG sialylation-mediated clearance; total T4 rises to ~150% of non-pregnant values by the second trimester [6, mechanism_review]
- Exogenous estrogens (oral contraceptives, hormone therapy, tamoxifen, raloxifene)
- Mitotane, fluorouracil, methadone, heroin

**Conditions that lower TBG** (and therefore lower total T4 while free T4 remains intact):
- Nephrotic syndrome: urinary loss of TBG and albumin precipitates low total T4 despite normal thyroid gland function [6, mechanism_review]
- Androgens and glucocorticoids: suppress hepatic TBG synthesis
- Severe systemic illness (non-thyroidal illness syndrome): multifactorial suppression of binding proteins

In each scenario, measuring total T4 would lead to a misclassification of thyroid status — apparent hyperthyroidism in pregnancy, apparent hypothyroidism in nephrosis — whereas free T4 correctly reports the hormonally relevant concentration. This is the practical application of the **free hormone hypothesis**: biological effect tracks the free, not the total, ligand [4, mechanism_review].

The analytical gold standard for fT4 is equilibrium dialysis at 37°C and physiological pH, followed by isotope dilution liquid-chromatography tandem mass spectrometry (ID-LC-MS/MS) of the dialysate. Direct immunoassays are faster and cheaper but suffer measurable interference from TBG and albumin concentrations, autoantibodies (present in ~20% of Hashimoto's patients), and rare variants such as familial dysalbuminemic hyperthyroxinemia, which can cause spuriously elevated immunoassay fT4 results in clinically euthyroid individuals [4, mechanism_review].

### The TSH↔fT4 Feedback Axis

Free T4 is the dominant negative-feedback signal that suppresses pituitary thyrotroph TSH secretion. The relationship is characteristically **inverse and log-linear**: within an individual, a given fold-change in fT4 corresponds to a proportionally larger fold-change in TSH in the opposite direction — a consequence of the logarithmic sensitivity of pituitary thyrotrophs [7, cohort; 8, mechanism_review]. Intra-individual analysis of large datasets confirms that while cross-sectional population data appear complex and non-linear (partly due to biological heterogeneity across individuals), the within-person TSH↔fT4 dynamic is robustly log-linear [7, cohort].

This steep TSH amplification of small fT4 changes is clinically pivotal: a fT4 drop of as little as 10–15% from an individual's set-point can double serum TSH, making TSH a far more sensitive primary screen for thyroid dysfunction than fT4 itself — and making fT4 the essential complementary test when TSH is abnormal, particularly to distinguish primary from central (pituitary/hypothalamic) hypothyroidism. Conversely, fT4 is the dominant readout in pituitary disease, where TSH is rendered unreliable by its own deficiency.

---

## Reference Ranges, Units & Thresholds

### Adult Reference Interval

For healthy, euthyroid adults, free T4 (fT4) measured by routine immunoassay typically falls within **0.8–1.8 ng/dL (approximately 10–23 pmol/L)**, though the precise interval varies by platform, reagent kit, calibration, and the reference population used to establish it. A large Korean population study (n = 5,987; iodine-replete; TPOAb-negative; Roche electrochemiluminescence immunoassay) derived an overall reference interval of **0.92–1.60 ng/dL (11.84–20.59 pmol/L)** using 2.5–97.5 percentiles [1, cohort]. Males had significantly higher mean fT4 than females (1.29 vs 1.20 ng/dL), and fT4 declined progressively with age after 20 years — underscoring that even within a single validated assay, demographic sub-intervals carry clinical weight [1, cohort].

### Units and Conversion

fT4 is reported in **ng/dL** (nanograms per deciliter) in the United States and in **pmol/L** (picomoles per liter) in most of the rest of the world. The conversion factor is:

> **1 ng/dL = 12.87 pmol/L**

| ng/dL | pmol/L |
|-------|--------|
| 0.8   | 10.3   |
| 1.0   | 12.9   |
| 1.5   | 19.3   |
| 1.8   | 23.2   |

Always confirm which unit a laboratory report uses before comparing values across institutions or over time.

### Method-Dependence: A Load-Bearing Caveat

**fT4 immunoassay values are not freely transferable between platforms.** This is not a minor technical footnote — it is a fundamental property of how fT4 is measured clinically.

Unlike total T4 (which is well-standardized), immunoassay estimates of fT4 are sensitive to dilution conditions, buffer composition, affinity of the antibody reagent, and the T4-binding protein milieu of the sample. Different platforms therefore produce systematically different absolute values from the same specimen. A head-to-head study comparing immunoassay (IA), liquid chromatography–tandem mass spectrometry (LC-MS/MS), and equilibrium dialysis (ED) in 62 healthy subjects found that IA values averaged 8.3% below LC-MS/MS and 6.0% below ED, while LC-MS/MS and ED agreed closely (r = 0.952 vs 0.763 for IA vs LC-MS/MS) [9, cohort]. The published reference intervals for each method reflected this: IA 9–16 pg/mL; LC-MS/MS 8–21 pg/mL; ED 7–23 pg/mL — a range of nearly 2× from lower to upper bound depending on method [9, cohort].

The International Federation of Clinical Chemistry (IFCC) has established a conventional reference measurement procedure based on equilibrium dialysis isotope-dilution LC-MS/MS at physiological pH 7.40 and 37°C [10, regulatory]. This anchors a metrological hierarchy, but routine clinical analyzers remain immunoassay-based and cannot be assumed interchangeable. The NACB laboratory medicine practice guidelines (Baloch et al., 2003) explicitly endorse method-specific reference intervals for this reason [11, regulatory].

**Practical implication:** when tracking fT4 longitudinally, the same platform should be used at each time point. A shift from 0.9 ng/dL to 1.2 ng/dL matters clinically only if the assay did not change. A transfer between laboratories without assay documentation can produce apparent changes that are instrument artefacts.

### Trimester-Specific Pregnancy Ranges

fT4 physiology changes substantially during pregnancy, and immunoassay performance degrades further, making this a high-risk context for misinterpretation.

**Physiological trajectory:** fT4 is mildly elevated or unchanged in the first trimester (driven by hCG-stimulated thyroid production), then declines across the second and third trimesters as thyroxine-binding globulin (TBG) rises (up to ~800 nmol/L, nearly tripling from ~300 nmol/L in nonpregnant women) and albumin falls. A Chinese meta-analysis of 11,629 women across 5 kit platforms (Roche, Bayer, Abbott, DPC, Beckman) found that fT4 upper and lower limits both declined with gestational trimester: upper limits fell ~22% by the second trimester and ~25% by the third, while lower limits fell ~13% and ~21%, respectively [12, cohort]. An illustrative set of trimester-specific values from a Siemens Centaur chemiluminescence study were: first trimester 13.93–26.49 pmol/L (1.08–2.05 ng/dL), second trimester 12.33–19.33 pmol/L (0.95–1.50 ng/dL), third trimester 11.38–19.21 pmol/L (0.88–1.49 ng/dL) [13, cohort].

**Assay pitfalls in pregnancy:** All five immunoassay platforms tested in one study overestimated fT4 in pregnant women by 7–29% compared to the LC-MS/MS reference, with the largest positive biases from Atellica (28.7%) and Cobas [20, cohort]. The 2017 ATA guidelines (Alexander, Pearce et al.) note that automated immunoassays produce an "assay-dependent reduction in measured fT4" in the third trimester inconsistent with direct equilibrium dialysis measurements, attributing this to disruption of the equilibrium by altered binding protein concentrations, buffer effects, and dilution [14, regulatory]. The ATA recommends that each laboratory establish its own **trimester- and method-specific** reference intervals; when that is not feasible, intervals from the literature derived with the same assay and a demographically similar population should be adopted [14, regulatory].

When assay-specific pregnancy ranges are unavailable, total T4 (which rises ~50% in pregnancy due to TBG elevation) or the free T4 index (see below) may be more interpretable than immunoassay fT4 [14, regulatory].

### Diagnostic Patterns: The TSH/fT4 Grid

fT4 is almost never interpreted in isolation. Its clinical meaning is established relative to TSH in a two-axis diagnostic grid [15, mechanism_review]:

| TSH | fT4 | Pattern |
|-----|-----|---------|
| Elevated (> ULN) | Low (< LLN) | **Overt primary hypothyroidism** |
| Elevated (> ULN) | Normal | **Subclinical hypothyroidism** |
| Suppressed (< LLN) | Elevated (> ULN) | **Overt hyperthyroidism** |
| Suppressed (< LLN) | Normal | **Subclinical hyperthyroidism** |
| Low or inappropriately normal | Low | **Central hypothyroidism** (pituitary/hypothalamic) |

The distinction between overt and subclinical disease is primarily a laboratory distinction, not a purely clinical one [15, mechanism_review]: subclinical disease is defined by an abnormal TSH with a fT4 (or fT3) still within the assay reference interval, regardless of symptom burden. Central hypothyroidism is a critical pattern to recognize because TSH alone would appear misleadingly normal or low despite true hormone deficiency — only the low fT4 reveals the defect.

Interpretation requires adherence to the method-specific reference interval for fT4: because upper and lower limits differ by platform, an fT4 of 14 pmol/L may be within interval on one system and marginally below the lower reference limit on another.

### Historical Context: The Free T4 Index (FTI / T7)

Before direct immunoassay for fT4 was widely available, clinicians estimated free hormone availability via the **Free Thyroxine Index (FTI)**, also called the **T7 index**:

> **FTI = Total T4 × T3 resin uptake (%) / 100**

The T3 resin uptake (also called thyroid hormone binding ratio) is an indirect proxy for TBG-binding capacity: when TBG is saturated (as in hyperthyroidism), more T3 binds the resin (high uptake); when TBG is elevated (as in pregnancy or OCP use), more T3 binds TBG (low resin uptake). Multiplying total T4 by the uptake ratio corrects for binding protein changes and approximates the free fraction. The FTI was the clinical standard through the 1970s–1980s [16, mechanism_review].

The FTI retains niche use: during pregnancy, when direct fT4 immunoassays are unreliable, total T4 × binding ratio (or a target range of 1.5× the nonpregnant upper limit for total T4) may provide a more stable index of thyroid status than immunoassay fT4. Mayo Clinic Laboratories still offers FTI as a reflex calculation [16, mechanism_review]. In most nonpregnant adults with normal binding proteins, however, direct fT4 immunoassay has supplanted it.

---

## Measurement & Interferences

### The Measurement Challenge: Estimating the Unmeasurable

Free thyroxine (fT4) circulates at picomolar concentrations — roughly 9–23 pmol/L (0.7–1.8 ng/dL) in euthyroid adults — while more than 99.97% of total T4 is protein-bound to thyroxine-binding globulin (TBG), transthyretin, and albumin. Measuring only the tiny unbound fraction without perturbing the binding equilibrium is, in principle, impossible in a direct clinical tube. True physical separation of free from bound hormone requires **equilibrium dialysis (ED)** or **ultrafiltration (UF)**, followed by **isotope-dilution liquid chromatography-tandem mass spectrometry (ID-LC-MS/MS)** to quantify the trace T4 in the dialysate. This two-step combination is the reference measurement procedure (RMP) endorsed by the IFCC [17, regulatory].

The CDC and IFCC C-STFT validated an equilibrium dialysis ID-UPLC-MS/MS candidate RMP that achieves a mean interlaboratory bias of ±2.5% and combined imprecision below 4.4%, with a limit of detection of 0.90 pmol/L [18, mechanism_review]. This procedure is calibrated to a certified pure T4 standard traceable to SI units (pmol/L at pH 7.40, 37°C) [17, regulatory].

Routine clinical laboratories universally use **automated immunoassays** that do not perform physical separation. The two main immunoassay architectures are:

- **One-step (analog) assays:** A labeled T4 analog and endogenous free T4 compete for a capture antibody while sample binding proteins remain present. The analog is designed to not bind TBG, but in practice the presence of mutant albumin or displaced binding proteins can confound results.
- **Two-step assays:** The sample is first incubated with immobilized antibody to capture fT4, the matrix is washed away, and only then is the label added. Two-step designs are generally less sensitive to binding-protein perturbations than one-step designs [38, mechanism_review].

Critically, all immunoassays are **estimates** of fT4, not direct measurements. They are calibrated against reference procedures but remain vulnerable to matrix effects, and the same serum sample can yield clinically meaningful differences across platforms [39, mechanism_review].

### Standardization and Method-to-Method Variability

The IFCC **Committee for Standardization of Thyroid Function Tests (C-STFT)** has been working since the mid-2000s to establish a metrological reference system for fT4 [17, regulatory; 21, regulatory]. The challenge is formidable: immunoassay fT4 values routinely differ from the ED-LC-MS/MS RMP by −30% to −72% on the low end, with no single immunoassay clustering to a consensus value [18, mechanism_review]. Recalibration against the RMP is technically feasible, but the C-STFT has demonstrated that bringing immunoassays to a common calibration still leaves an average inter-method spread of roughly 30–50% — a consequence of different assay buffer compositions, competing-analog affinities, and sample matrix interactions that cannot be fully corrected by traceability alone [39, mechanism_review].

The practical consequence is that **reference intervals for fT4 are method-specific and non-transferable between platforms** [39, mechanism_review]. A result of 1.0 ng/dL (12.9 pmol/L) on one instrument may correspond to 1.4 ng/dL (18.0 pmol/L) on another, placing the same patient in normal versus elevated ranges. Two-way communication between the ordering clinician and the laboratory — knowing which analyzer and which reference range applies — is therefore not optional.

### Biotin (Vitamin B7)

Most major immunoassay platforms (Roche, Siemens, Beckman Coulter, Ortho Clinical Diagnostics) use **streptavidin-biotin coupling** for solid-phase attachment. When a patient takes high-dose biotin supplements (≥5–10 mg/day, far above the 30–70 µg recommended daily intake), exogenous biotin saturates streptavidin in the assay. In **competitive (one-step) fT4 assays**, excess biotin displaces biotinylated fT4-antibody complexes from the solid phase, producing **falsely elevated fT4** readings [19, cohort]. A case series documented fT4 rising from 1.4 to 3.2 ng/dL while a patient was taking biotin, normalizing to 1.3 ng/dL after one week of cessation [19, cohort]. Platform-specific effects are important: Roche ELECSYS fT4 and fT3 tend to be falsely elevated; TSH is simultaneously and falsely suppressed on sandwich platforms, creating a biochemical picture indistinguishable from hyperthyroidism. Clinical guidance from the ATA recommends stopping biotin supplementation at least 2–7 days before thyroid function testing [14, regulatory].

### Heterophile Antibodies, Anti-Streptavidin, and Anti-Ruthenium Antibodies

Heterophile antibodies — polyclonal immunoglobulins directed against animal-derived assay antibodies — can bridge capture and detection antibodies spuriously, causing falsely elevated fT4 on affected platforms [38, mechanism_review; 29, cohort]. Anti-streptavidin antibodies (endogenously produced, persisting 18–24 months) and anti-ruthenium antibodies (directed at electrochemiluminescence labels) produce similar patterns: elevated fT4 with suppressed TSH on biotin-streptavidin or ruthenium-labeled platforms [38, mechanism_review]. Anti-ruthenium interference may in some cases push fT4 in the falsely low direction, making its clinical footprint heterogeneous. When results conflict with clinical presentation, repeating the assay on a platform from a different manufacturer (using different animal-species antibodies, coupling chemistry, or detection system) is the most practical detection strategy.

**Anti-T4 autoantibodies** (thyroid hormone autoantibodies, THAbs) are a distinct interference: endogenous IgG or IgM that bind thyroxine can sequester the T4 tracer in competitive assays, causing falsely elevated fT4, or alternatively compete with the capture antibody, causing falsely low readings — direction depends on assay architecture [38, mechanism_review].

### Familial Dysalbuminemic Hyperthyroxinemia (FDH)

FDH is caused by a missense mutation in albumin (most commonly Arg218His) that dramatically increases albumin's affinity for T4. Affected individuals are biochemically euthyroid but have elevated total T4 and — on most one-step immunoassays — **spuriously elevated fT4**, mimicking hyperthyroidism [22, cohort]. The mechanism: in one-step competitive assays, the mutant albumin binds the labeled T4 analog with enhanced avidity, reducing analog availability to compete with endogenous fT4 at the capture antibody; the assay then reads fT4 as artificially high [22, cohort]. The Khoo et al. study ranked commercial immunoassays by FDH susceptibility from greatest to least: Beckman ACCESS > Roche ELECSYS > Fujirebio Lumipulse > Siemens CENTAUR > Abbott ARCHITECT; only Ortho VITROS was largely resistant [22, cohort]. Equilibrium dialysis remains the confirmatory method that correctly shows normal free T4 in FDH. Prevalence of R218H FDH ranges from 0.01% to 1.8% depending on ethnicity, and the condition is substantially underdiagnosed. Discordance between two platforms should always raise FDH as a differential.

### Heparin

Intravenous and subcutaneous heparin cause **spurious fT4 elevation** through an in-vitro artifact. Heparin activates endothelial lipoprotein lipase in vivo; once blood is drawn and the sample is incubated (even briefly), that released lipase continues to hydrolyze triglycerides in vitro, generating nonesterified fatty acids (NEFAs) [23, cohort]. At NEFA concentrations exceeding approximately 2–3 mmol/L, fatty acids competitively displace T4 from TBG and albumin, elevating the apparent free fraction [6, mechanism_review]. The artifact affects even equilibrium dialysis methods if incubation is prolonged, and is exacerbated by hypoalbuminemia, elevated baseline triglycerides, and delayed sample processing. Clinical mitigation: draw thyroid function tests at least 10–12 hours after the last heparin dose when possible, and process samples promptly.

### Drugs Displacing T4 from Binding Proteins

Several drugs compete for TBG and albumin binding sites, acutely elevating the free T4 fraction and in some cases causing a sustained reduction in total T4:

- **Furosemide:** Significant displacement occurs at doses above approximately 80 mg/day (particularly intravenous), transiently raising fT4 [6, mechanism_review].
- **Salicylates and NSAIDs:** Compete for TBG binding sites; high-dose aspirin can produce detectable rises in apparent fT4.
- **Phenytoin and carbamazepine:** Both displace T4 from binding proteins AND induce hepatic enzymes that increase T4 metabolic clearance. The net effect is a paradox: total T4 falls 20–40%, the free fraction initially rises, but chronically fT4 tends to normalize or fall modestly while TSH remains normal in euthyroid patients [28, cohort]. Immunoassays may still show low fT4 in treated patients despite clinical and biochemical euthyroidism, making TSH the more reliable thyroid status marker in this population [28, cohort].

### Non-Thyroidal Illness (NTI) / Low-T4 Syndrome

In critically ill patients, a complex pattern of thyroid axis suppression produces a challenging assay environment. T3 falls first, driven by reduced peripheral conversion; in severe NTI, total T4 also falls (total T4 below 26 nmol/L correlates with mortality up to 80%), and fT4 may be low, normal, or spuriously elevated depending on the assay used [6, mechanism_review]. The NTI matrix — with altered binding protein concentrations, elevated free fatty acids, and circulating inhibitors — degrades immunoassay accuracy in a method-specific manner. Equilibrium dialysis may show elevated fT4 in early NTI (reflecting genuine displacement from binding proteins), while some immunoassays track in the opposite direction. Results should be interpreted with caution in the context of acute illness; TSH remains the primary test when illness is resolved.

### Pregnancy (Measurement Perspective)

Pregnancy substantially alters the protein binding equilibrium for T4. Estrogen-driven hepatic synthesis increases TBG by roughly 50% in the first trimester, while albumin falls; hCG-mediated TSH suppression is common in the first trimester. These changes render fT4 immunoassays unreliable throughout pregnancy. In a controlled study, first-trimester fT4 immunoassay values were comparable to or lower than nonpregnant controls despite the expected physiological rise in thyroid hormone production, and by the second and third trimesters fT4 values had fallen to approximately 65% of nonpregnant controls [27, cohort]. Different immunoassay platforms changed in opposite directions in the first trimester in the same women, underscoring method-specific matrix effects. Reference ranges derived from nonpregnant adults must not be applied. Trimester-specific, method-specific reference intervals are required; where these are unavailable, total T4 (≥1.5× nonpregnant lower limit) or the free T4 index provide more stable indices of thyroid status during pregnancy.

---

## Determinants & Clinical Significance

### fT4 as the Reflex/Confirmatory Test After Abnormal TSH

In clinical practice, serum TSH is the first-line screening test for thyroid dysfunction, but fT4 is the essential reflex when TSH falls outside the reference range. An elevated TSH with a suppressed fT4 confirms **overt primary hypothyroidism**, while an elevated TSH with a normal fT4 defines **subclinical hypothyroidism** — a category where treatment decisions hinge on the degree of TSH elevation and symptom burden rather than on the fT4 value alone [24, mechanism_review]. Conversely, a suppressed TSH with an elevated fT4 confirms **overt hyperthyroidism/thyrotoxicosis**; a suppressed TSH with a normal fT4 defines **subclinical hyperthyroidism**. The degree of fT4 deviation from the reference range (roughly 0.8–1.8 ng/dL; 10–23 pmol/L, method-dependent) provides a severity gradient: a fT4 of 0.2 ng/dL (2.6 pmol/L) in a patient with TSH >100 mIU/L signals a depth of hypothyroidism with different clinical urgency than a fT4 near the lower reference limit.

In older adults with isolated TSH elevation, fT4 adds prognostic granularity that TSH alone cannot provide. A prospective cohort study of 72 older adults from the Baltimore Longitudinal Study of Aging used decision tree analysis to identify a fT4 threshold of 0.89 ng/dL (11.45 pmol/L) — the 24th percentile of the normal range — as the cut-point distinguishing participants who went on to develop overt hypothyroidism from those showing other aging-related thyroid changes, while TSH level, fT3, and anti-TPO antibody status had no significant predictive value. This underscores fT4's role in refining the clinical meaning of a borderline-elevated TSH [25, cohort].

### Central (Secondary/Tertiary) Hypothyroidism: Where TSH Fails

The cardinal scenario in which TSH is an unreliable guide is **central (secondary or tertiary) hypothyroidism** arising from pituitary or hypothalamic disease. In this setting the pituitary either cannot produce adequate TSH or secretes TSH with altered glycosylation and reduced biological activity, yet normal immunoreactivity on standard assays. The result is a low or inappropriately normal TSH in the face of insufficient thyroid hormone production — a biochemical pattern that a TSH-reflex strategy will systematically miss.

Beck-Peccoz and colleagues, in a clinical review in Nature Reviews Endocrinology, characterize the defining biochemical feature as "low circulating levels of free T4 in the presence of low-to-normal TSH concentrations," and identify reliance on "the sole TSH-reflex strategy" as a primary diagnostic pitfall [26, mechanism_review]. The practical corollary is that any patient with known or suspected pituitary disease must have fT4 measured regardless of the TSH result.

Monitoring during levothyroxine replacement in central hypothyroidism follows the same logic. The 2014 American Thyroid Association (ATA) guidelines (Jonklaas et al., Thyroid 2014) explicitly state that "the log-linear relationship between TSH and fT4 is lost in patients with central hypothyroidism" and designate serum fT4 as the alternative biochemical monitor of therapy adequacy, with a target **above the midnormal reference range** [24, mechanism_review].

### Monitoring Thyroid Hormone Therapy

**Primary hypothyroidism on levothyroxine.** In standard primary hypothyroidism, TSH is the primary monitoring target, measured 6–8 weeks after any dose adjustment, by which point steady-state is reached. fT4 serves a supporting role: it can flag over-replacement before TSH suppresses, and it is useful when serum TSH is unreliable — for example, in the first 6–8 weeks after a dose change, before TSH equilibrates. The ATA guidelines note that fT4 should be used alongside TSH when TSH seems discordant with clinical status [24, mechanism_review].

**Thyroid cancer TSH-suppression therapy.** In patients with differentiated thyroid cancer (DTC) who are receiving supraphysiological levothyroxine to suppress TSH, fT4 functions as a safety guardrail. The ATA's 2015 Management Guidelines for Differentiated Thyroid Cancer (Haugen et al.) recommend individualized TSH targets based on risk stratification: <0.1 mIU/L for high-risk and many intermediate-risk patients, 0.1–0.5 mIU/L for lower-intermediate-risk, and 0.5–2 mIU/L for low-risk patients. Because TSH is intentionally suppressed in this population, fT4 is the practical measure used to confirm the patient is not over-replaced into frank thyrotoxicosis [24, mechanism_review]. The 2016 ATA Hyperthyroidism Guidelines (Ross et al., Thyroid 2016) similarly emphasize monitoring fT4 and fT3 when assessing thyrotoxicosis severity in clinical practice [30, mechanism_review].

### What Raises fT4

| Cause | Mechanism |
|---|---|
| **Graves' disease** | TSH receptor antibodies (TSI) drive unregulated thyroid synthesis; fT4 and fT3 rise together with TSH suppressed [30, mechanism_review] |
| **Toxic multinodular goiter / toxic adenoma** | Autonomous nodule function independent of TSH; degree of fT4 elevation correlates with functional mass |
| **Exogenous/factitious thyroxine** | Exogenous T4 load overwhelms feedback; TSH suppressed, fT4 elevated |
| **Thyroiditis (destructive phase)** | Inflammation (subacute, postpartum, amiodarone type 2) releases preformed hormone; fT4 rises transiently |
| **Amiodarone-induced thyrotoxicosis (AIT)** | Type 1 AIT: iodine-excess driven synthesis (Jod-Basedow); Type 2 AIT: destructive release; both markedly elevate fT4 and fT3 with suppressed TSH [30, mechanism_review] |
| **Familial dysalbuminemic hyperthyroxinemia (FDH)** | Autosomal dominant R218H or R218P albumin mutation; most routine immunoassays report artefactually elevated fT4 with normal TSH — the patient is clinically euthyroid [22, cohort] |
| **Heparin** | Even low-dose heparin activates lipoprotein lipase in vitro, releasing nonesterified fatty acids that displace T4 from binding proteins and artifactually raise measured fT4; the in vivo effect is negligible [36, mechanism_review] |
| **Acute psychiatric admission** | In a cohort of 539 unselected psychiatric inpatients (Sakai et al., 2018), 21.9% had fT4 above the reference range at admission versus the expected 2.5%; fT4 normalized significantly by discharge (mean 17.09 → 16.07 pmol/L) while TSH remained unchanged — consistent with a stress-driven peripheral shift rather than true hyperthyroidism [31, cohort] |

### What Lowers fT4

**Primary hypothyroidism** (Hashimoto's thyroiditis, post-radioablation, post-thyroidectomy, severe iodine deficiency) produces high TSH with low fT4 — the classic pattern detected by TSH reflex.

**Central hypothyroidism** yields low fT4 with an inappropriately low or normal TSH, as described above [26, mechanism_review].

**Non-thyroidal illness (NTI / euthyroid sick syndrome).** Critical illness suppresses deiodinase activity, reducing T4-to-T3 conversion and lowering circulating thyroid hormone levels without a proportionate TSH rise. In mild-to-moderate NTI the predominant finding is low fT3 with variably affected fT4; in severe NTI, fT4 may fall substantially, reflecting both reduced synthesis and altered binding-protein levels. A 2014 narrative review in Thyroid (Van den Berghe) identified pro-inflammatory cytokines and macronutrient restriction as central drivers, distinguishing acute NTI from prolonged critical illness with suppressed hypothalamic TRH expression [32, mechanism_review]. Distinguishing NTI from true central hypothyroidism remains a clinical challenge since both present with low fT4 and a non-elevated TSH.

**Drugs.** Phenytoin and carbamazepine lower total T4 and have complex effects on fT4 measurements. The primary mechanisms are: (a) enzyme induction accelerating T4 clearance, and (b) displacement of T4 from thyroxine-binding globulin. A key clinical trap: routine one-step immunoassays in phenytoin-treated patients frequently show artifactually low fT4 — the dilution-based assay detects the reduced binding capacity — while equilibrium dialysis shows normal or near-normal free hormone concentrations, and TSH remains normal. Pattan et al. (Cureus, 2020, PMID 33282597) documented this mimicry of central hypothyroidism in a case of long-term phenytoin use [33, mechanism_review]. The practical guidance: use TSH (not fT4) to assess thyroid status in euthyroid phenytoin-treated patients unless central hypothyroidism is independently suspected.

### Within-Range fT4 and Metabolic/Cardiovascular Associations

Emerging observational data suggest that fT4 position within the reference range is not biologically inert. A retrospective cohort study in a Chinese population (Ding et al., BMC Endocrine Disorders 2021, PMID 33663458) followed 929 euthyroid participants and found that those with lower-normal fT4 (≤16.0 pmol/L, the reference-range median) had a significantly higher incidence of metabolic syndrome (hazard ratio 2.13, 95% CI 1.38–3.29, P=0.006) compared with higher-normal fT4 [34, cohort]. This association was strongest when combined with TSH >2.0 mIU/L.

At the other end, high-normal and mildly elevated fT4 have been linked to atrial fibrillation, heart failure, and all-cause mortality in older adults, though these associations are predominantly from observational data subject to confounding. **These findings are preliminary and should not be used to target fT4 to a specific intra-range sub-zone** in otherwise clinically euthyroid individuals; they inform research hypotheses rather than current practice.

### Limitations of fT4 Measurement

**Assay-method dependence.** There is no universally standardized free-hormone assay. Commercially available one-step analog immunoassays are subject to interference from abnormal binding proteins, as occurs in FDH [22, cohort] and heparin administration [23, cohort]. Results are not interchangeable between platforms.

**Pregnancy.** Expanding plasma volume and estrogen-driven TBG rise during pregnancy create binding-protein conditions for which most immunoassays are uncalibrated. Lee et al. (American Journal of Obstetrics and Gynecology, 2009, PMID 19114271) demonstrated that routine fT4 immunoassays declined to approximately 65% of non-pregnant control values by the second and third trimesters while total T4 and the free T4 index (FTI) retained an appropriate inverse relationship with TSH throughout gestation [27, cohort]. Current ATA guidelines recommend that pregnancy-specific TSH reference ranges be used as the primary monitoring tool, with fT4 or the FTI (not routine immunoassay alone) as adjuncts.

**Non-thyroidal illness.** In critical illness, hypoalbuminemia and altered binding-protein profiles invalidate the binding-equilibrium assumptions on which all indirect free-hormone assays rest. Equilibrium dialysis or ultrafiltration remains the reference method, but these are impractical for routine care.

**Single time-point limitation.** Because fT4 has a ~6-day half-life, any single measurement reflects recent synthesis and secretory rate but cannot capture the circadian or dose-timing variability relevant to long-term assessment.

---

## Bibliography

[1]. Park SY, et al. Age- and gender-specific reference intervals of TSH and free T4 in an iodine-replete area: Data from Korean National Health and Nutrition Examination Survey IV (2013–2015). *PLoS ONE*. 2018;13(2):e0190738. PMID: 29390008. DOI: 10.1371/journal.pone.0190738. — tag: cohort

[2]. Abdalla SM, Bianco AC. Defending plasma T3 is a biological priority. *Clin Endocrinol (Oxf)*. 2014 Nov;81(5):633–641. PMID: 25040645. DOI: 10.1111/cen.12563. — tag: mechanism_review

[3]. Schussler GC. The thyroxine-binding proteins. *Thyroid*. 2000 Feb;10(2):141–149. PMID: 10718550. DOI: 10.1089/thy.2000.10.141. — tag: mechanism_review

[4]. Westbye AB, Aas FE, Kelp O, Dahll LK, Thorsby PM. Analysis of free, unbound thyroid hormones by liquid chromatography-tandem mass spectrometry: A mini-review of the medical rationale and analytical methods. *Anal Sci Adv*. 2023;4:244–254. DOI: 10.1002/ansa.202200067. PMID: 38716305. — tag: mechanism_review

[5]. Yeap BB, Manning L, Chubb SAP, Hankey GJ, Golledge J, Almeida OP, Flicker L. Reference Ranges for Thyroid-Stimulating Hormone and Free Thyroxine in Older Men: Results From the Health In Men Study. *J Gerontol A Biol Sci Med Sci*. 2017 Mar;72(3):444–449. PMID: 27440910. DOI: 10.1093/gerona/glw121. — tag: cohort

[6]. Koulouri O, Moran C, Halsall D, Chatterjee K, Gurnell M. Pitfalls in the measurement and interpretation of thyroid function tests. *Best Pract Res Clin Endocrinol Metab*. 2013 Dec;27(6):745–762. PMID: 24275187. DOI: 10.1016/j.beem.2013.10.003. — tag: mechanism_review

[7]. Rothacker KM, Brown SJ, Hadlow NC, Wardrop R, Walsh JP. Reconciling the Log-Linear and Non–Log-Linear Nature of the TSH-Free T4 Relationship: Intra-Individual Analysis of a Large Population. *J Clin Endocrinol Metab*. 2016 Mar;101(3):1151–1158. PMID: 26735261. DOI: 10.1210/jc.2015-4011. — tag: cohort

[8]. Hoermann R, Midgley JEM, Larisch R, Dietrich JW. Homeostatic Control of the Thyroid-Pituitary Axis: Perspectives for Diagnosis and Treatment. *Front Endocrinol (Lausanne)*. 2015;6:177. PMID: 26635726. DOI: 10.3389/fendo.2015.00177. — tag: mechanism_review

[9]. Meng F, Jonklaas J, Leow MK. Interconversion of plasma free thyroxine values from assay platforms with different reference intervals using linear transformation methods. *Biology (Basel)*. 2021;10(1):45. PMID: 33440665. DOI: 10.3390/biology10010045. — tag: cohort

[10]. Van Houcke SK, Van Uytfanghe K, Shimizu E, Tani W, Umemoto M, Thienpont LM. IFCC international conventional reference procedure for the measurement of free thyroxine in serum. *Clin Chem Lab Med*. 2011;49(8):1275–1281. PMID: 21675941. DOI: 10.1515/CCLM.2011.639. — tag: regulatory

[11]. Baloch Z, Carayon P, Conte-Devolx B, et al. Laboratory medicine practice guidelines: laboratory support for the diagnosis and monitoring of thyroid disease. *Thyroid*. 2003;13(1):3–126. PMID: 12625976. DOI: 10.1089/105072503321086962. — tag: regulatory

[12]. Gao X, et al. Gestational TSH and FT4 reference intervals in Chinese women: a systematic review and meta-analysis. *Front Endocrinol (Lausanne)*. 2018;9:432. PMID: 30123185. DOI: 10.3389/fendo.2018.00432. — tag: cohort

[13]. Zhang D, Cai K, Wang G, et al. Trimester-specific reference intervals for thyroid hormones in pregnant women. *Medicine (Baltimore)*. 2019;98(4):e14245. PMID: 30681614. DOI: 10.1097/MD.0000000000014245. — tag: cohort

[14]. Alexander EK, Pearce EN, Brent GA, et al. 2017 Guidelines of the American Thyroid Association for the Diagnosis and Management of Thyroid Disease During Pregnancy and the Postpartum. *Thyroid*. 2017;27(3):315–389. PMID: 28056690. DOI: 10.1089/thy.2016.0457. — tag: regulatory

[15]. Feldt-Rasmussen U, Klose M. Clinical strategies in the testing of thyroid function. In: Feingold KR, et al., eds. *Endotext*. MDText.com; 2020. Available at: https://www.ncbi.nlm.nih.gov/books/NBK285558/. — tag: mechanism_review

[16]. Mayo Clinic Laboratories. Free Thyroxine Index (FTI), Serum — Test ID: FRTUP. Available at: https://www.mayocliniclabs.com/test-catalog/overview/62583. — tag: mechanism_review

[17]. Thienpont LM, Van Uytfanghe K, Beastall G, et al. (IFCC WG-STFT). Proposal of a candidate international conventional reference measurement procedure for free thyroxine in serum. *Clin Chem Lab Med*. 2007;45(7):934–936. PMID: 17617044. DOI: 10.1515/CCLM.2007.155. — tag: regulatory

[18]. Ribera A, Bruns DE, Greenberg N, et al. Development of an equilibrium dialysis ID-UPLC-MS/MS candidate reference measurement procedure for free thyroxine in human serum. *Clin Biochem*. 2023;115:110–117. PMID: 36940844. DOI: 10.1016/j.clinbiochem.2023.03.010. — tag: mechanism_review

[19]. Ardabilygazir A, Afshariyamchi F, Piccoli P, Rao SD. Effect of high-dose biotin on thyroid function tests: case report and literature review. *Cureus*. 2018;10(6):e2845. PMID: 30140596. DOI: 10.7759/cureus.2845. — tag: cohort

[20]. Jansen HI, et al. Pregnancy disrupts the accuracy of automated fT4 immunoassays. *Eur Thyroid J*. 2022;11(6):e220145. PMID: 36219545. DOI: 10.1530/ETJ-22-0145. — tag: cohort

[21]. IFCC Committee for Standardization of Thyroid Function Tests (C-STFT). Standardization of FT4 and FT3 measurements. Available at: https://ifcc-cstft.org/standardization-of-ft4-and-ft3-measurements. — tag: regulatory

[22]. Khoo S, Lyons G, McGowan A, et al. Familial dysalbuminaemic hyperthyroxinaemia interferes with current free thyroid hormone immunoassay methods. *Eur J Endocrinol*. 2020;182(6):533–538. PMID: 32213658. DOI: 10.1530/EJE-19-1021. — tag: cohort

[23]. Jaume JC, Mendel CM, Frost PH, Greenspan FS, Laughton CW. Extremely low doses of heparin release lipase activity into the plasma and can thereby cause artifactual elevations in the serum-free thyroxine concentration as measured by equilibrium dialysis. *Thyroid*. 1996;6(1):79–83. PMID: 8733876. — tag: cohort

[24]. Jonklaas J, Bianco AC, Bauer AJ, et al. Guidelines for the treatment of hypothyroidism: Prepared by the American Thyroid Association Task Force on Thyroid Hormone Replacement. *Thyroid*. 2014;24(12):1670–1751. PMID: 25266247. — tag: mechanism_review

[25]. Abbey EJ, Balogun OD, George KS, et al. Free thyroxine distinguishes subclinical hypothyroidism from other aging-related changes in those with isolated elevated thyrotropin. *Front Endocrinol*. 2022;13:847843. PMID: 35311240. — tag: cohort

[26]. Beck-Peccoz P, Rodari G, Giavoli C, Lania A. Central hypothyroidism — a neglected thyroid disorder. *Nat Rev Endocrinol*. 2017;13(10):588–598. PMID: 28549061. — tag: mechanism_review

[27]. Lee RH, Spencer CA, Mestman JH, et al. Free T4 immunoassays are flawed during pregnancy. *Am J Obstet Gynecol*. 2009;200(3):260.e1–260.e6. PMID: 19114271. DOI: 10.1016/j.ajog.2008.10.042. — tag: cohort

[28]. Surks MI, DeFesi CR. Normal serum free thyroid hormone concentrations in patients treated with phenytoin or carbamazepine: a paradox resolved. *JAMA*. 1996;275(19):1495–1498. PMID: 8622224. — tag: cohort

[29]. Serei VD, Marshall I, Carayannopoulos MO. Heterophile antibody interference affecting multiple Roche immunoassays: a case study. *Clin Chim Acta*. 2019;497:125–129. PMID: 31325446. DOI: 10.1016/j.cca.2019.07.010. — tag: cohort

[30]. Ross DS, Burch HB, Cooper DS, et al. 2016 American Thyroid Association guidelines for diagnosis and management of hyperthyroidism and other causes of thyrotoxicosis. *Thyroid*. 2016;26(10):1343–1421. PMID: 27521067. — tag: mechanism_review

[31]. Sakai Y, Shibuya T, Takagi S, et al. FT4 and TSH, relation to diagnoses in an unselected psychiatric acute-ward population, and change during acute psychiatric admission. *BMC Psychiatry*. 2018;18(1):218. PMID: 30055589. — tag: cohort

[32]. Van den Berghe G. Non-thyroidal illness in the ICU: a syndrome with different faces. *Thyroid*. 2014;24(10):1456–1465. PMID: 24845024. DOI: 10.1089/thy.2014.0201. — tag: mechanism_review

[33]. Pattan V, Javed A, Kalra S, et al. Phenytoin — medication that warrants deviation from standard approach for thyroid lab interpretation. *Cureus*. 2020;12(11):e11617. PMID: 33282597. — tag: mechanism_review

[34]. Ding X, Xu Y, Wang Y, et al. Lower normal free thyroxine is associated with a higher risk of metabolic syndrome: a retrospective cohort on Chinese population. *BMC Endocr Disord*. 2021;21(1):45. PMID: 33663458. — tag: cohort

[35]. Chopra IJ. An assessment of daily production and significance of thyroidal secretion of 3,3',5'-triiodothyronine (reverse T3) in man. *J Clin Invest*. 1976 Nov;58(5):1125–1134. PMID: 932209. — tag: mechanism_review

[36]. Mendel CM, Frost PH, Kunitake ST, Cavalieri RR. Mechanism of the heparin-induced increase in the concentration of free thyroxine in plasma. *J Clin Endocrinol Metab*. 1987;65(6):1259–1264. PMID: 3680482. — tag: mechanism_review

[38]. Favresse J, Burlacu M-C, Maiter D, Gruson D. Interferences with thyroid function immunoassays: clinical implications and detection algorithm. *Endocr Rev*. 2018;39(5):830–850. PMID: 29982406. DOI: 10.1210/er.2018-00119. — tag: mechanism_review

[39]. Ancelle D, Bardet S, d'Herbomez M, et al. Free thyroxine measurement in clinical practice: how to optimize indications, analytical procedures, and interpretation criteria while waiting for global standardization. *Crit Rev Clin Lab Sci*. 2023;60(2):101–140. DOI: 10.1080/10408363.2022.2121960. — tag: mechanism_review
