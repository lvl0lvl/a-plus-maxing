# Section C: Calculation Inputs, Standardization & Pitfalls

Calculated free testosterone (cFT) is not a single measured quantity — it is a model-derived estimate whose accuracy is bounded by the accuracy of three independent input measurements and the validity of the mathematical model's underlying assumptions. Each layer introduces its own error budget, and those errors propagate through to the final cFT value in ways that are non-obvious to the clinician receiving a single number on a lab report.

## Three Inputs, Three Error Sources

The Vermeulen equation — the most widely used cFT formula in clinical practice — requires three inputs: total testosterone (TT), sex hormone–binding globulin (SHBG), and albumin. It then applies experimentally determined association constants (Ka for albumin–testosterone ≈ 3.6 × 10⁴ L/mol; Ks for SHBG–testosterone ≈ 5.97 × 10⁸ L/mol) within a law-of-mass-action framework to derive the unbound fraction [1, mechanism_review].

**Total testosterone** is the most impactful input. Immunoassays for TT carry significant inter-assay and inter-laboratory variability — particularly at low concentrations. A survey of 1,133 laboratories using 14 different assays measuring the same hypogonadal man's sample found values ranging from 45 to 365 ng/dL, an eight-fold span [2, regulatory]. Bias of 35–50% relative to mass-spectrometry reference methods has been documented at physiologic male concentrations, with errors reaching 220% in the sub-4 nmol/L range relevant for women and borderline-low men [3, mechanism_review]. The CDC Hormone Standardization Program (HoSt) for total testosterone — which certifies labs to within ±6.4% of the CDC reference method — has substantially improved LC-MS/MS concordance, but immunoassay adoption of CDC-certified platforms remains incomplete [2, regulatory]. Liquid chromatography–tandem mass spectrometry (LC-MS/MS) is the analytically preferred method for TT [3, mechanism_review]. Any immunoassay bias in TT propagates linearly into cFT.

**SHBG** is measured exclusively by immunoassay in routine clinical practice — no mass-spectrometric reference method is in widespread clinical use, and no formal harmonization program equivalent to HoSt-TT exists for SHBG [4, cohort; 5, mechanism_review]. A 2025 European survey of clinical laboratories found SHBG was measured exclusively by immunoassay across all participating centers, with considerable inter-laboratory variability in both absolute concentrations and reported reference intervals, leading the authors to call explicitly for continued harmonization efforts [4, cohort]. SHBG assays are calibrated against the WHO 2nd International Standard (NIBSC 08/266), but different platform antibodies recognize different epitopes, producing non-commutable results. Because free testosterone is inversely sensitive to SHBG — especially at the high SHBG concentrations common in aging men or men on certain medications — SHBG assay error can distort cFT estimates substantially.

**Albumin** is typically not measured for this purpose; instead, a fixed population-mean value is assumed (commonly 4.3 g/dL). Vermeulen et al. themselves showed that cFT is relatively insensitive to albumin within the normal physiologic range (40–50 g/L), with a fixed value of 43 g/L yielding a correlation of r = 0.992 with equilibrium dialysis [1, mechanism_review]. However, this assumption breaks down in clinical populations with marked hypoalbuminemia (cirrhosis, nephrotic syndrome, critical illness) or hyperproteinemia, where the assumed albumin value introduces meaningful systematic error.

## The Binding-Constant and Model Debate

The Vermeulen model assumes a 1:1 stoichiometry between testosterone and each SHBG monomer within the homodimer, with identical binding affinity at both sites — a linear, non-cooperative binding model. This assumption predates the resolution of SHBG's crystal structure and subsequent biophysical characterization of its dimer interface [6, mechanism_review].

In 2015, Zakharov et al. proposed a multi-step, dynamic allosteric model in which the two monomers within the SHBG dimer are allosterically coupled — meaning occupancy of one binding site affects the affinity at the other [6, mechanism_review]. This ensemble-based model (cFT-Z) treats SHBG binding as a non-linear, multiphasic process, consistent with newer crystallographic and surface-plasmon-resonance data showing that SHBG affinity for testosterone varies with SHBG concentration itself. The Zakharov model produces systematically higher free-T estimates than the Vermeulen equation [7, cohort].

The question of which model is more accurate against the gold standard (equilibrium dialysis followed by LC-MS/MS) was examined directly by Fiers et al. (2018) in a study of 183 women and 146 men using direct LC-MS/MS–measured equilibrium dialysis as the comparator. The finding was counterintuitive: despite the Zakharov model's more sophisticated biophysical underpinning, it performed worse against equilibrium dialysis in this population. The Vermeulen equation (cFT-V) overestimated free-T values by a median ratio of 1.19, but that ratio was notably stable across variation in SHBG, albumin, and total testosterone (rank correlation ρ range: −0.17 to −0.01). By contrast, cFT-Z overestimated by a median ratio of 2.05, and that bias was strongly correlated with SHBG levels (ρ = 0.75) [5, mechanism_review]. This means cFT-Z is more susceptible to SHBG-dependent bias in clinical samples than the Vermeulen equation, not less.

The practical upshot: cFT values are model-dependent, and the two most-used models do not agree in absolute terms. Clinicians and researchers comparing cFT from different calculators or studies must verify which formula was used. The Vermeulen equation remains the most widely endorsed approximation — acknowledged by the Endocrine Society for clinical use in hypogonadism assessment — but it is a systematic overestimate of equilibrium dialysis values, and its bias grows at extreme SHBG concentrations [1, mechanism_review; 5, mechanism_review].

## Method Discordance: cFT vs. Equilibrium Dialysis vs. Analog Immunoassay

Three clinically available approaches produce materially different numerical values for "free testosterone":

1. **Equilibrium dialysis (ED) + LC-MS/MS** is the reference method. It directly separates free from bound testosterone across a semipermeable membrane at physiologic equilibrium [5, mechanism_review].
2. **Calculated free testosterone (cFT, Vermeulen)** correlates well with ED (r ≈ 0.986 in men [8, cohort]) and is widely endorsed, but systematically overestimates absolute free-T values — the Fiers study found a median cFT-V/ED ratio of 1.19 in men [5, mechanism_review]. It requires its own reference intervals and cannot be directly compared against ED-derived ranges.
3. **Direct analog immunoassay (aFT)** uses a labeled testosterone analog to estimate free-T without separation steps. Multiple studies document that aFT values are approximately one-fourth to one-seventh of ED values and correlate more strongly with total testosterone than with bioavailable testosterone, particularly in men with low SHBG [9, mechanism_review]. The Endocrine Society explicitly advises against direct analog immunoassays in clinical practice. The Winters analysis confirmed that the analog assay's strong dependence on SHBG renders it unreliable for assessing androgen deficiency in patients whose SHBG deviates from normal [9, mechanism_review].

A five-algorithm comparison by De Ronde et al. found that Bland–Altman analysis showed large absolute differences between algorithms despite moderate-to-high Pearson correlations, and that confounding by SHBG concentrations was introduced differentially depending on the algorithm used [7, cohort]. The conclusion was direct: algorithms must be revalidated in the local population setting before use, and over- or underestimation of cFT is otherwise unavoidable.

## No Harmonized Reference Interval for Free Testosterone

Total testosterone has benefited from CDC HoSt certification (targeting ±6.4% bias to the reference method) and the derivation of harmonized reference ranges across cohorts [2, regulatory]. No analogous program exists for free testosterone. The CDC's own roadmap explicitly lists free testosterone and binding proteins under "standardization and harmonization programs in development" [2, regulatory] — a category distinct from the completed HoSt-TT program. The 2025 Narinx survey confirmed this gap in practice: across European laboratories, reference intervals for cFT showed "considerable variability" in both lower and upper limits, making inter-laboratory comparison of cFT results unreliable without knowledge of the specific formula, input assay platforms, and population from which the reference intervals were derived [4, cohort].

## Error Propagation and Interferences

Several pre-analytical and analytical factors can corrupt one or more of the three cFT inputs:

**Biotin** supplements taken at supra-physiologic doses (≥5 mg, as used for hair/nail supplements and some MS trials) interfere with biotinylated immunoassays — the sandwich format used by many SHBG and TT immunoassay platforms. Biotin competes with biotinylated reagents for streptavidin binding sites, producing falsely elevated results in competitive assays and falsely reduced results in sandwich assays. Both TT and SHBG immunoassays are susceptible, meaning biotin can distort both inputs to cFT simultaneously in either direction. LC-MS/MS assays are not affected. Patients should withhold biotin for at least 72 hours (or longer at very high doses) before sampling [10, mechanism_review].

**Heterophile antibodies** — including human anti-animal antibodies (HAAA) and other endogenous immunoglobulins — can produce falsely elevated or depressed results on both TT and SHBG immunoassays by cross-reacting with assay antibodies. Results that are inconsistent with clinical presentation, or that are discordant between platforms, should raise suspicion for antibody interference. The confirmatory step is LC-MS/MS for TT and, if possible, a different SHBG platform [10, mechanism_review].

**Extreme SHBG values** expose a structural limitation of the Vermeulen equation. At very high SHBG (>70–100 nmol/L, seen in hepatic disease, thyrotoxicosis, or aging), most testosterone is SHBG-bound and the cFT-V is particularly sensitive to any SHBG assay error. Published mean biases for cFT across methods range from 5.8% to 56.0% in head-to-head comparisons, with the worst discordance concentrated at the extremes of SHBG distribution [5, mechanism_review; 7, cohort].

**Competing steroids**: High circulating concentrations of DHT (e.g., during topical DHT therapy) or estradiol (e.g., pregnancy) occupy SHBG binding sites, but most immunoassays measure total SHBG protein rather than available binding capacity. This leads to overestimation of free-T from the Vermeulen equation in these clinical states [1, mechanism_review].

---

## Bibliography

1. Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012. [mechanism_review]

2. Bhasin S et al. (Endocrine Society guidelines); CDC Hormone Standardization Program for Testosterone (HoSt-TT). CDC Clinical Standardization Programs — Hormones Certified Assays. Available at: cdc.gov/clinical-standardization-programs. [regulatory]

3. Rosner W, Auchus RJ, Azziz R, Sluss PM, Raff H. Utility, limitations, and pitfalls in measuring testosterone: an Endocrine Society position statement. *J Clin Endocrinol Metab.* 2007;92(2):405–413. PMID: 17090633. [mechanism_review]

4. Narinx N, Nyamaah JA, Antonio L, et al. A survey on measurement and reporting of total testosterone, sex hormone-binding globulin and free testosterone in clinical laboratories in Europe. *Clin Chem Lab Med.* 2025. PMID: 40068942. [cohort]

5. Fiers T, Wu F, Moghetti P, Vanderschueren D, Lapauw B, Kaufman JM. Reassessing free-testosterone calculation by liquid chromatography–tandem mass spectrometry direct equilibrium dialysis. *J Clin Endocrinol Metab.* 2018;103(6):2167–2174. PMID: 29618085. [mechanism_review]

6. Zakharov MN, Bhasin S, Travison TG, Xue R, Ulloor J, Vasan RS, Carter E, Wu F, Jasuja R. A multi-step, dynamic allosteric model of testosterone's binding to sex hormone binding globulin. *Mol Cell Endocrinol.* 2015;399:190–200. DOI: 10.1016/j.mce.2014.09.001. [mechanism_review]

7. De Ronde W, van der Schouw YT, Pols HA, et al. Calculation of bioavailable and free testosterone in men: a comparison of 5 published algorithms. *Clin Chem.* 2006;52(9):1777–1784. PMID: 16793931. [cohort]

8. Kacker R, Hornstein AM, Morgentaler A. Free testosterone by direct and calculated measurement versus equilibrium dialysis in a clinical population. *Aging Male.* 2013;16(4):164–168. PMID: 24090209. [cohort]

9. Winters SJ, Kelley DE, Goodpaster B. The analog free testosterone assay: are the results in men clinically useful? *Clin Chem.* 1998;44(10):2178–2182. PMID: 9761253. [mechanism_review]

10. Katzman BM, Lueke AJ, Donato LJ, Jaffe AS, Baumann NA. Prevalence of biotin supplement usage in outpatients and plasma biotin concentrations in patients presenting to the emergency department. *Clin Biochem.* 2018;60:11–16; and: Bowen R, Bhargava A, Kinsey A, et al. AACC Guidance Document on Biotin Interference in Laboratory Tests. 2019. [mechanism_review]
