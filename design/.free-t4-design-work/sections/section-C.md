# Section C: Measurement & Interferences

## C.1 The Measurement Challenge: Estimating the Unmeasurable

Free thyroxine (fT4) circulates at picomolar concentrations — roughly 9–23 pmol/L (0.7–1.8 ng/dL) in euthyroid adults — while more than 99.97% of total T4 is protein-bound to thyroxine-binding globulin (TBG), transthyretin, and albumin. Measuring only the tiny unbound fraction without perturbing the binding equilibrium is, in principle, impossible in a direct clinical tube. True physical separation of free from bound hormone requires **equilibrium dialysis (ED)** or **ultrafiltration (UF)**, followed by **isotope-dilution liquid chromatography-tandem mass spectrometry (ID-LC-MS/MS)** to quantify the trace T4 in the dialysate. This two-step combination is the reference measurement procedure (RMP) endorsed by the IFCC [1, regulatory].

The CDC and IFCC C-STFT validated an equilibrium dialysis ID-UPLC-MS/MS candidate RMP that achieves a mean interlaboratory bias of ±2.5% and combined imprecision below 4.4%, with a limit of detection of 0.90 pmol/L [2, mechanism_review]. This procedure is calibrated to a certified pure T4 standard traceable to SI units (pmol/L at pH 7.40, 37 °C) [1, regulatory].

Routine clinical laboratories universally use **automated immunoassays** that do not perform physical separation. The two main immunoassay architectures are:

- **One-step (analog) assays:** A labeled T4 analog and endogenous free T4 compete for a capture antibody while sample binding proteins remain present. The analog is designed to not bind TBG, but in practice the presence of mutant albumin or displaced binding proteins can confound results.
- **Two-step assays:** The sample is first incubated with immobilized antibody to capture fT4, the matrix is washed away, and only then is the label added. Two-step designs are generally less sensitive to binding-protein perturbations than one-step designs [3, mechanism_review].

Critically, all immunoassays are **estimates** of fT4, not direct measurements. They are calibrated against reference procedures but remain vulnerable to matrix effects, and the same serum sample can yield clinically meaningful differences across platforms [4, mechanism_review].

## C.2 Standardization and Method-to-Method Variability

The IFCC **Committee for Standardization of Thyroid Function Tests (C-STFT)** has been working since the mid-2000s to establish a metrological reference system for fT4 [1, regulatory; 5, regulatory]. The challenge is formidable: immunoassay fT4 values routinely differ from the ED-LC-MS/MS RMP by −30% to −72% on the low end, with no single immunoassay clustering to a consensus value [2, mechanism_review]. Recalibration against the RMP is technically feasible, but the C-STFT has demonstrated that bringing immunoassays to a common calibration still leaves an average inter-method spread of roughly 30–50% — a consequence of different assay buffer compositions, competing-analog affinities, and sample matrix interactions that cannot be fully corrected by traceability alone [4, mechanism_review].

The practical consequence is that **reference intervals for fT4 are method-specific and non-transferable between platforms** [4, mechanism_review]. A result of 1.0 ng/dL (12.9 pmol/L) on one instrument may correspond to 1.4 ng/dL (18.0 pmol/L) on another, placing the same patient in normal versus elevated ranges. Two-way communication between the ordering clinician and the laboratory — knowing which analyzer and which reference range applies — is therefore not optional.

## C.3 Interferences

### Biotin (Vitamin B7)

Most major immunoassay platforms (Roche, Siemens, Beckman Coulter, Ortho Clinical Diagnostics) use **streptavidin-biotin coupling** for solid-phase attachment. When a patient takes high-dose biotin supplements (≥5–10 mg/day, far above the 30–70 µg recommended daily intake), exogenous biotin saturates streptavidin in the assay. In **competitive (one-step) fT4 assays**, excess biotin displaces biotinylated fT4-antibody complexes from the solid phase, producing **falsely elevated fT4** readings [6, cohort]. A case series documented fT4 rising from 1.4 to 3.2 ng/dL while a patient was taking biotin, normalizing to 1.3 ng/dL after one week of cessation [6, cohort]. Platform-specific effects are important: Roche ELECSYS fT4 and fT3 tend to be falsely elevated; TSH is simultaneously and falsely suppressed on sandwich platforms, creating a biochemical picture indistinguishable from hyperthyroidism. Clinical guidance from the ATA recommends stopping biotin supplementation at least 2–7 days before thyroid function testing [7, regulatory].

### Heterophile Antibodies, Anti-Streptavidin, and Anti-Ruthenium Antibodies

Heterophile antibodies — polyclonal immunoglobulins directed against animal-derived assay antibodies — can bridge capture and detection antibodies spuriously, causing falsely elevated fT4 on affected platforms [8, cohort]. Anti-streptavidin antibodies (endogenously produced, persisting 18–24 months) and anti-ruthenium antibodies (directed at electrochemiluminescence labels) produce similar patterns: elevated fT4 with suppressed TSH on biotin-streptavidin or ruthenium-labeled platforms [3, mechanism_review]. Anti-ruthenium interference may in some cases push fT4 in the falsely low direction, making its clinical footprint heterogeneous. When results conflict with clinical presentation, repeating the assay on a platform from a different manufacturer (using different animal-species antibodies, coupling chemistry, or detection system) is the most practical detection strategy.

**Anti-T4 autoantibodies** (thyroid hormone autoantibodies, THAbs) are a distinct interference: endogenous IgG or IgM that bind thyroxine can sequester the T4 tracer in competitive assays, causing falsely elevated fT4, or alternatively compete with the capture antibody, causing falsely low readings — direction depends on assay architecture [3, mechanism_review].

### Familial Dysalbuminemic Hyperthyroxinemia (FDH)

FDH is caused by a missense mutation in albumin (most commonly Arg218His) that dramatically increases albumin's affinity for T4. Affected individuals are biochemically euthyroid but have elevated total T4 and — on most one-step immunoassays — **spuriously elevated fT4**, mimicking hyperthyroidism [9, cohort]. The mechanism: in one-step competitive assays, the mutant albumin binds the labeled T4 analog with enhanced avidity, reducing analog availability to compete with endogenous fT4 at the capture antibody; the assay then reads fT4 as artificially high [9, cohort]. The Khoo et al. study ranked commercial immunoassays by FDH susceptibility from greatest to least: Beckman ACCESS > Roche ELECSYS > Fujirebio Lumipulse > Siemens CENTAUR > Abbott ARCHITECT; only Ortho VITROS was largely resistant [9, cohort]. Equilibrium dialysis remains the confirmatory method that correctly shows normal free T4 in FDH. Prevalence of R218H FDH ranges from 0.01% to 1.8% depending on ethnicity, and the condition is substantially underdiagnosed. Discordance between two platforms should always raise FDH as a differential.

### Heparin

Intravenous and subcutaneous heparin cause **spurious fT4 elevation** through an in-vitro artifact. Heparin activates endothelial lipoprotein lipase in vivo; once blood is drawn and the sample is incubated (even briefly), that released lipase continues to hydrolyze triglycerides in vitro, generating nonesterified fatty acids (NEFAs) [10, cohort]. At NEFA concentrations exceeding approximately 2–3 mmol/L, fatty acids competitively displace T4 from TBG and albumin, elevating the apparent free fraction [11, mechanism_review]. The artifact affects even equilibrium dialysis methods if incubation is prolonged, and is exacerbated by hypoalbuminemia, elevated baseline triglycerides, and delayed sample processing. Clinical mitigation: draw thyroid function tests at least 10–12 hours after the last heparin dose when possible, and process samples promptly.

### Drugs Displacing T4 from Binding Proteins

Several drugs compete for TBG and albumin binding sites, acutely elevating the free T4 fraction and in some cases causing a sustained reduction in total T4:

- **Furosemide:** Significant displacement occurs at doses above approximately 80 mg/day (particularly intravenous), transiently raising fT4 [11, mechanism_review].
- **Salicylates and NSAIDs:** Compete for TBG binding sites; high-dose aspirin can produce detectable rises in apparent fT4.
- **Phenytoin and carbamazepine:** Both displace T4 from binding proteins AND induce hepatic enzymes that increase T4 metabolic clearance. The net effect is a paradox: total T4 falls 20–40%, the free fraction initially rises, but chronically fT4 tends to normalize or fall modestly while TSH remains normal in euthyroid patients [12, cohort]. Immunoassays may still show low fT4 in treated patients despite clinical and biochemical euthyroidism, making TSH the more reliable thyroid status marker in this population [12, cohort].

### Non-Thyroidal Illness (NTI) / Low-T4 Syndrome

In critically ill patients, a complex pattern of thyroid axis suppression produces a challenging assay environment. T3 falls first, driven by reduced peripheral conversion; in severe NTI, total T4 also falls (total T4 below 26 nmol/L correlates with mortality up to 80%), and fT4 may be low, normal, or spuriously elevated depending on the assay used [11, mechanism_review]. The NTI matrix — with altered binding protein concentrations, elevated free fatty acids, and circulating inhibitors — degrades immunoassay accuracy in a method-specific manner. Equilibrium dialysis may show elevated fT4 in early NTI (reflecting genuine displacement from binding proteins), while some immunoassays track in the opposite direction. Results should be interpreted with caution in the context of acute illness; TSH remains the primary test when illness is resolved.

### Pregnancy

Pregnancy substantially alters the protein binding equilibrium for T4. Estrogen-driven hepatic synthesis increases TBG by roughly 50% in the first trimester, while albumin falls; hCG-mediated TSH suppression is common in the first trimester. These changes render fT4 immunoassays unreliable throughout pregnancy. In a controlled study, first-trimester fT4 immunoassay values were comparable to or lower than nonpregnant controls despite the expected physiological rise in thyroid hormone production, and by the second and third trimesters fT4 values had fallen to approximately 65% of nonpregnant controls [13, cohort]. Different immunoassay platforms changed in opposite directions in the first trimester in the same women, underscoring method-specific matrix effects. Reference ranges derived from nonpregnant adults must not be applied. Trimester-specific, method-specific reference intervals are required; where these are unavailable, total T4 (≥1.5× nonpregnant lower limit) or the free T4 index provide more stable indices of thyroid status during pregnancy.

---

## Bibliography

1. Thienpont LM, Van Uytfanghe K, Beastall G, et al. (IFCC WG-STFT). Proposal of a candidate international conventional reference measurement procedure for free thyroxine in serum. *Clin Chem Lab Med.* 2007;45(7):934–936. PMID: 17617044. DOI: 10.1515/CCLM.2007.155. [regulatory]

2. Ribera A, Bruns DE, Greenberg N, et al. Development of an equilibrium dialysis ID-UPLC-MS/MS candidate reference measurement procedure for free thyroxine in human serum. *Clin Biochem.* 2023;115:110–117. PMID: 36940844. DOI: 10.1016/j.clinbiochem.2023.03.010. [mechanism_review]

3. Favresse J, Burlacu M-C, Maiter D, Gruson D. Interferences with thyroid function immunoassays: clinical implications and detection algorithm. *Endocr Rev.* 2018;39(5):830–850. PMID: 29982406. DOI: 10.1210/er.2018-00119. [mechanism_review]

4. Ancelle D, Bardet S, d'Herbomez M, et al. Free thyroxine measurement in clinical practice: how to optimize indications, analytical procedures, and interpretation criteria while waiting for global standardization. *Crit Rev Clin Lab Sci.* 2023;60(2):101–140. DOI: 10.1080/10408363.2022.2121960. [mechanism_review]

5. IFCC Committee for Standardization of Thyroid Function Tests (C-STFT). Standardization of FT4 and FT3 measurements. Available at: https://ifcc-cstft.org/standardization-of-ft4-and-ft3-measurements [regulatory]

6. Ardabilygazir A, Afshariyamchi F, Piccoli P, Rao SD. Effect of high-dose biotin on thyroid function tests: case report and literature review. *Cureus.* 2018;10(6):e2845. PMID: 30140596. DOI: 10.7759/cureus.2845. [cohort]

7. American Thyroid Association. Thyroid function testing: biotin interference guidance. *Clinical Thyroidology for the Public.* December 2018;11(12):3–4. Available at: https://www.thyroid.org/patient-thyroid-information/ct-for-patients/december-2018/vol-11-issue-12-p-3-4/ [regulatory]

8. Serei VD, Marshall I, Carayannopoulos MO. Heterophile antibody interference affecting multiple Roche immunoassays: a case study. *Clin Chim Acta.* 2019;497:125–129. PMID: 31325446. DOI: 10.1016/j.cca.2019.07.010. [cohort]

9. Khoo S, Lyons G, McGowan A, et al. Familial dysalbuminaemic hyperthyroxinaemia interferes with current free thyroid hormone immunoassay methods. *Eur J Endocrinol.* 2020;182(6):533–538. PMID: 32213658. DOI: 10.1530/EJE-19-1021. [cohort]

10. Jaume JC, Mendel CM, Frost PH, Greenspan FS, Laughton CW. Extremely low doses of heparin release lipase activity into the plasma and can thereby cause artifactual elevations in the serum-free thyroxine concentration as measured by equilibrium dialysis. *Thyroid.* 1996;6(1):79–83. PMID: 8733876. [cohort]

11. Koulouri O, Moran C, Halsall D, Chatterjee K, Gurnell M. Pitfalls in the measurement and interpretation of thyroid function tests. *Best Pract Res Clin Endocrinol Metab.* 2013;27(6):745–762. PMID: 24275187. DOI: 10.1016/j.beem.2013.10.003. [mechanism_review]

12. Surks MI, DeFesi CR. Normal serum free thyroid hormone concentrations in patients treated with phenytoin or carbamazepine: a paradox resolved. *JAMA.* 1996;275(19):1495–1498. PMID: 8622224. [cohort]

13. Lee RH, Spencer CA, Mestman JH, et al. Free T4 immunoassays are flawed during pregnancy. *Am J Obstet Gynecol.* 2009;200(3):260.e1–260.e6. PMID: 19114271. DOI: 10.1016/j.ajog.2008.10.042. [cohort]
