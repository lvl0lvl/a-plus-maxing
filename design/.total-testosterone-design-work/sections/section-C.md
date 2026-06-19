# C. Measurement & Standardization

## The Immunoassay Problem

Serum total testosterone is among the most commonly ordered endocrine tests, yet for decades the dominant measurement technology—direct immunoassay—has carried a well-characterized accuracy failure at low concentrations. Immunoassays rely on competitive antibody binding: exogenous labeled testosterone competes with the patient's testosterone for a limited number of antibody binding sites. At low concentrations (roughly below 3.47 nmol/L / 100 ng/dL), the signal-to-noise ratio degrades and cross-reactivity with structurally similar steroids—dihydrotestosterone (DHT), androstenedione, dehydroepiandrosterone sulfate (DHEA-S), and other androgens—becomes proportionally meaningful [1, mechanism_review; 2, mechanism_review]. Because all immunoassays broadly overestimate testosterone at low concentrations, the populations most vulnerable are women (typical range 0.35–2.5 nmol/L / 10–70 ng/dL), prepubertal children, and hypogonadal men who fall below 100 ng/dL—precisely the groups where diagnostic accuracy matters most.

A 2007 Endocrine Society position statement by Rosner et al. benchmarked seven commercial immunoassays against isotope-dilution gas chromatography–mass spectrometry (ID/GC-MS) and found that below approximately 8.0 nmol/L (230 ng/dL), methods disagreed by up to 5-fold, with immunoassays uniformly overestimating testosterone concentration in women [1, mechanism_review]. A large proficiency survey involving 142 certified clinical laboratories using 16 immunoassays showed biases as high as 73.1% relative to the reference method at low concentrations [3, cohort]. The failure is not manufacturer-specific; it is intrinsic to the immunoassay architecture.

A further structural weakness of first-generation direct immunoassays is their incomplete release of testosterone from sex hormone-binding globulin (SHBG). Before antibody competition, testosterone must be displaced from its carrier proteins—primarily SHBG (high affinity) and albumin (lower affinity, high capacity). First-generation immunoassays use displacement reagents (typically 8-anilino-1-naphthalene sulfonic acid or danazol) that incompletely strip testosterone from SHBG. The consequence is systematic error that scales with SHBG concentration: patients with high SHBG (e.g., elderly men, women on oral contraceptives, hyperthyroid individuals) are systematically under-reported, while patients with low SHBG (e.g., obese individuals, insulin-resistant men) are over-reported [3, cohort].

## LC-MS/MS: The Reference Method

Liquid chromatography–tandem mass spectrometry (LC-MS/MS) is the reference and preferred method for serum total testosterone measurement, particularly at low concentrations. The technique physically separates testosterone from other steroids via liquid chromatography before identification by mass-to-charge ratio in tandem mass spectrometry—a process that is inherently agnostic to antibody cross-reactivity. When Moal et al. (2007) compared LC-MS/MS against five immunoassay techniques in 70 women and children, all five immunoassays overestimated testosterone relative to the LC-MS/MS reference, with correlation coefficients between 0.77 and 0.87 and slopes indicating positive bias across the board [2, mechanism_review].

The isotope dilution variant—isotope dilution LC-MS/MS (ID-LC-MS/MS)—uses a stable isotope-labeled internal standard (e.g., deuterated testosterone-d3) added to each sample before extraction, compensating for matrix effects and process losses. Thienpont et al. (2008) established the state-of-the-art for this approach in a 14-laboratory comparison against the National Institute of Standards and Technology (NIST) reference measurement procedure (RMP), demonstrating that overall imprecision versus the RMP was below 15% at concentrations above 1.53 nmol/L (44 ng/dL) and below 34% at 0.3 nmol/L (8.65 ng/dL)—substantially better performance than immunoassay at all concentration strata [4, mechanism_review]. The CDC subsequently adopted an isotope dilution LC-MS/MS procedure as its own RMP, published in Clinica Chimica Acta by Wang et al. (2014), achieving total CVs of 3.7–4.8% across the concentration range and mean bias not significantly different from reference over two years of operation [5, regulatory].

## The CDC Hormone Standardization (HoSt) Program

Recognizing that assay variation was a clinical and public-health problem—not merely an analytical nuisance—a coalition of professional societies, government agencies, and industry convened to address it. The 2010 consensus statement by Rosner and Vesper et al., published in JCEM, established specific technical recommendations and launched what became the CDC Hormone Standardization (HoSt) Program for total testosterone [6, regulatory]. The Endocrine Society's 2018 clinical practice guideline (Bhasin et al.) adopted the HoSt-harmonized lower limit of normal in healthy nonobese young men—264 ng/dL (9.2 nmol/L)—explicitly noting that for laboratories not HoSt-certified, reference ranges may vary considerably and may not accurately identify hypogonadism [7, regulatory].

The HoSt Program works by providing participating laboratories with a set of well-characterized reference sera traceable to the NIST ID-LC-MS/MS RMP. Laboratories submit results; performance criterion is ±6.4% mean bias versus the reference measurement procedure over the concentration range of 2.50–1,000 ng/dL. Certification requires two consecutive successful phases and is valid for one year, enforcing ongoing assay performance surveillance. As of the most recent CDC certified list, the certification range does not extend below 2.5 ng/dL (0.087 nmol/L), which remains a limitation for the lowest female and pediatric concentrations.

The program's measurable impact on the field: between 2007 and 2011, participation in HoSt activities reduced inter-laboratory measurement bias among mass spectrometry methods by approximately 50% [4, mechanism_review]. A 2016 retrospective analysis of accuracy-based survey data nonetheless found that commonly used immunoassays still exhibited unacceptable biases at low concentrations, and that the Beckman testosterone immunoassay demonstrated an R² of 0.16 versus the CDC RMP in the 7.4–37.6 ng/dL range—statistically indistinguishable from no correlation [3, cohort]. The Partnership for the Accurate Testing of Hormones (PATH), a collaboration between the Endocrine Society and the CDC, has pushed for all clinical testosterone assays to achieve HoSt certification.

## Analytical Interferences

Immunoassays carry several interference vulnerabilities that LC-MS/MS avoids.

**Biotin (vitamin B7).** Many immunoassay platforms use biotin-streptavidin capture chemistry. High-dose biotin supplementation (≥5 mg/day, common in hair/nail supplements) floods the streptavidin binding sites, blocking capture of biotinylated reagents. In competitive immunoassays this mechanism drives results falsely high; in sandwich immunoassays, falsely low. The FDA issued a safety communication on this interference in November 2017. Clinical guidance: testosterone should not be drawn until at least 8 hours (standard doses) or 72 hours (mega-doses) after the last biotin ingestion. LC-MS/MS has no biotin susceptibility.

**Heterophile and anti-animal antibodies.** Patients exposed to animal sera (veterinary workers, users of certain biologic therapies) may develop heterophile antibodies that cross-link immunoassay antibodies and produce artifactually elevated results. Case reports document falsely high testosterone values in women that resolved to the low-normal range on LC-MS/MS confirmation [10, open_label].

**DHT and androgen cross-reactivity.** Dihydrotestosterone (5α-reduced form of testosterone) shares high structural similarity and can cross-react with anti-testosterone antibodies in immunoassays. This is clinically relevant in men using 5α-reductase inhibitors (where DHT is suppressed, so effect is minor) or in individuals using exogenous DHT preparations. Anabolic-androgenic steroids with testosterone-like structure also vary in their immunoassay cross-reactivity.

## Pre-analytical Considerations

**Diurnal variation and timing.** Total testosterone follows a circadian rhythm driven by pulsatile LH secretion. In healthy young men, morning (08:00–10:00) concentrations are 15–20% higher than evening nadir values, with individual variation as large as 50% [8, mechanism_review]. The diurnal amplitude is blunted with advancing age and in men with primary testicular failure. Because reference ranges are established on morning samples, blood should be drawn between 08:00 and 10:00. The Endocrine Society 2018 guideline recommends two separate morning draws on different days before a diagnosis of hypogonadism is made [7, regulatory].

**Fasting status.** A glucose load acutely suppresses testosterone—oral glucose (75 g) has been shown to decrease serum testosterone by 25–30% within two hours in healthy men, likely via insulin-mediated suppression of LH pulsatility. Fasting samples are therefore preferred for diagnostic accuracy.

**Acute illness.** Intercurrent illness, surgery, and any acute physiological stress suppress hypothalamic-pituitary-gonadal signaling; testosterone measurements during acute illness reflect the stress state, not the baseline androgen milieu, and should be deferred.

**Intra-individual biological variability.** Independent of diurnal rhythm, total testosterone carries a within-person coefficient of variation of approximately 15–20% across repeated measurements over weeks, even under controlled conditions. This variability is a principal reason clinical guidelines require two confirmatory measurements before treatment decisions.

## SHBG-Driven Discordance and Free Testosterone

Approximately 44% of circulating testosterone is tightly bound to SHBG (dissociation constant ~10⁹ L/mol), 54% is loosely bound to albumin (dissociation constant ~3×10⁴ L/mol), and only 1–3% circulates as free (unbound) testosterone. Biologically active testosterone is the sum of free and albumin-bound fractions (often called "bioavailable testosterone"), because albumin-bound testosterone dissociates readily at the capillary-tissue interface.

When SHBG is abnormal—which is common—total testosterone misrepresents the androgen milieu. **Conditions lowering SHBG** (obesity, type 2 diabetes, insulin resistance, hypothyroidism, androgen use, nephrotic syndrome, glucocorticoid excess) reduce total testosterone while free testosterone may remain in the normal range, leading to unnecessary treatment initiation if only total testosterone is reviewed. **Conditions raising SHBG** (aging, hyperthyroidism, cirrhosis, estrogen/oral contraceptive use, HIV, some anticonvulsants) can elevate total testosterone into the normal or high-normal range even when free testosterone is low, masking androgen deficiency [7, regulatory].

The Endocrine Society explicitly recommends measuring free or bioavailable testosterone in men with conditions known to alter SHBG [7, regulatory]. The gold standard measurement—equilibrium dialysis—is time-consuming, expensive, and limited to specialized laboratories. The practical alternative endorsed by clinical guidelines is **calculated free testosterone (cFT)** using the Vermeulen equation, which applies experimentally determined binding constants for testosterone's distribution among SHBG (Kd ~10⁹ L/mol) and albumin (Kd ~3.6×10⁴ L/mol) and the law of mass action. Vermeulen et al. (1999) validated this approach against apparent free testosterone by equilibrium dialysis across a wide range of SHBG concentrations—from low (hirsute women) to very high (hyperthyroid patients)—finding close agreement except in pregnancy, where estradiol occupies SHBG binding sites and causes the calculation to underestimate free testosterone [9, mechanism_review]. The calculation requires total testosterone (preferably by LC-MS/MS), SHBG, and albumin (or an assumed value of 4.3 g/dL, which introduces negligible error at physiologic albumin concentrations). Online calculators are available at the ISSAM website. Because the Vermeulen cFT directly inherits all error in the total testosterone measurement, use of a non-standardized immunoassay for total testosterone substantially degrades the reliability of the calculated free testosterone. Direct analog-based free testosterone immunoassays—an older and simpler approach—are explicitly condemned by the Endocrine Society as inaccurate and should not be used [7, regulatory].

---

## Bibliography

1. Rosner W, Auchus RJ, Azziz R, Sluss PM, Raff H. Position statement: Utility, limitations, and pitfalls in measuring testosterone: an Endocrine Society position statement. *J Clin Endocrinol Metab*. 2007;92(2):405–413. PMID: 17090633.

2. Moal V, Mathieu E, Reynier P, Malthièry Y, Gallois Y. Low serum testosterone assayed by liquid chromatography-tandem mass spectrometry: comparison with five immunoassay techniques. *Clin Chim Acta*. 2007;386(1–2):12–19. PMID: 17706625.

3. [PMC8589107] Using mass spectrometry to overcome the longstanding inaccuracy of a commercially-available clinical testosterone immunoassay. *Practical Laboratory Medicine*. 2021. PMC8589107.

4. Thienpont LM, Van Uytfanghe K, Blincko S, et al. State-of-the-art of serum testosterone measurement by isotope dilution-liquid chromatography-tandem mass spectrometry. *Clin Chem*. 2008;54(8):1290–1297. PMID: 18556330.

5. Wang Y, Gay GD, Cook Botelho JC, Caudill SP, Vesper HW. Total testosterone quantitative measurement in serum by LC-MS/MS. *Clin Chim Acta*. 2014;436:263–267. PMID: 24960363.

6. Rosner W, Vesper H; Endocrine Society, et al. Toward excellence in testosterone testing: a consensus statement. *J Clin Endocrinol Metab*. 2010;95(10):4542–4548. PMID: 20926540.

7. Bhasin S, Brito JP, Cunningham GR, et al. Testosterone therapy in men with hypogonadism: an Endocrine Society clinical practice guideline. *J Clin Endocrinol Metab*. 2018;103(5):1715–1744. PMID: 29562364.

8. Endotext — Laboratory assessment of testicular function (Anawalt B, Matsumoto AM). NBK279145. NCBI Bookshelf. (diurnal variation data; no PMID — book chapter).

9. Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab*. 1999;84(10):3666–3672. PMID: 10523012.

10. Gardini B, Bondanelli M, Cariani A, Zatelli MC, Ambrosio MR. Intricate diagnosis due to falsely elevated testosterone levels by immunoassay. *Endocrine*. 2025;88(3):706–710. PMID: 39948210. PMC: 12143982. [open_label]
