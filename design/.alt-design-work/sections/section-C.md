# Section C: Measurement & Standardization

## The IFCC Reference Measurement Procedure

The gold-standard reference procedure for measuring ALT catalytic activity is the IFCC primary reference procedure at 37°C, published in 2002 as Part 4 of the IFCC series on enzyme measurement at 37°C [1, mechanism_review]. This procedure was derived from the earlier 30°C IFCC reference method and is operated by the IFCC Committee on Reference Systems of Enzymes (C-RSE). The 37°C temperature is now universal for all IFCC enzyme reference procedures, replacing earlier 25°C and 30°C methods that produced systematically lower absolute values and impaired comparability across eras and regions.

## The Routine Assay: Coupled Enzymatic-Spectrophotometric Method

In routine automated laboratory practice, ALT is measured by a two-step coupled enzymatic reaction monitored spectrophotometrically. The primary reaction, catalyzed by ALT itself, transfers an amino group from L-alanine to α-ketoglutarate, producing pyruvate and L-glutamate:

> L-alanine + α-ketoglutarate → pyruvate + L-glutamate

The indicator (coupled) reaction then reduces the pyruvate to L-lactate via lactate dehydrogenase (LDH) in the presence of NADH:

> pyruvate + NADH + H⁺ → L-lactate + NAD⁺

The rate of absorbance decrease at 340 nm — where NADH absorbs strongly and NAD⁺ does not — is directly proportional to ALT catalytic activity. Results are reported in units per liter (U/L), where 1 U = the amount of enzyme catalyzing 1 µmol of substrate per minute under defined conditions. This coupled-reaction design is chemically analogous to the AST assay but uses L-alanine as substrate and LDH (rather than malate dehydrogenase) as the indicator enzyme.

## Pyridoxal-5'-Phosphate (P5P) Supplementation: The Key Standardization Variable

The most consequential methodological variable in ALT measurement is whether the reagent includes pyridoxal-5'-phosphate (P5P, also called PLP or vitamin B6 coenzyme). ALT is a pyridoxal-phosphate-dependent enzyme; P5P serves as its essential coenzyme. The IFCC reference procedure specifies P5P supplementation in the reagent to saturate the apoenzyme, ensuring that measured activity reflects the full catalytic potential of the ALT protein present — independent of the patient's circulating B6 status.

When P5P is omitted from the reagent, ALT activity measured depends partly on the patient's endogenous vitamin B6 level. In B6-replete patients this gap is modest, but in individuals with vitamin B6 deficiency — a condition more prevalent than often appreciated — ALT is systematically underestimated. A 2026 analysis of ALT and AST harmonization documented that addition of P5P to the reagent produced an average increase of approximately 12% in ALT concentrations across a mixed clinical population; in the subset with confirmed vitamin B6 deficiency (defined as serum PLP < 20 nmol/L), the underestimation was proportionally larger [2, mechanism_review]. In a clinical B6 deficiency cohort (hemodialysis patients), measured plasma ALT was 8.6 ± 0.6 U/L in deficient patients versus 11.4 ± 0.9 U/L in B6-replete controls — roughly 25% lower — and enzyme activity partially normalized after vitamin B6 supplementation, confirming B6 status as the causal variable [3, cohort].

Despite the IFCC recommendation, more than 60% of laboratories in the United States and internationally have used ALT assays not supplemented with P5P [2, mechanism_review]. This creates a systematic, patient-state-dependent negative bias in non-P5P methods and undermines traceability to the IFCC reference procedure. Laboratories using non-P5P reagents cannot achieve true metrological traceability to the IFCC primary reference and should apply method-specific reference intervals; applying IFCC-derived cutoffs to non-P5P results risks misclassifying elevated ALT as normal in B6-deficient patients.

## Standardization and Harmonization

The IFCC primary reference procedure anchors metrological traceability. One certified reference material exists in the JCTLM database — ERM®-AD454k/IFCC — against which routine method calibrators are theoretically traceable. However, commutability of this material across routine methods is not uniformly established, representing a practical limitation to full standardization.

The real-world consequence of incomplete harmonization is substantial. A large study across 223 US Veterans Health Administration laboratories — 22,950 ALT measurements from 80 proficiency-testing samples — found that analyzer manufacturer was independently associated with ALT result, with a mean inter-manufacturer difference of 10.4 U/L across all samples and a mean difference of 15.4 U/L for samples with mean ALT below 50 U/L (i.e., the clinically critical range where ULN decisions are made) [4, cohort]. Beckman Coulter, Roche, Siemens, and Vitros platforms produced systematically different values on identical samples. The authors concluded that universal ALT cutoffs should not be applied across platforms until inter-manufacturer variability is resolved.

An IFCC multicenter study (centers in Milan, Beijing, Bursa, and Nordic countries; n = 765 subjects) established method-specific IFCC reference intervals at 37°C as: ALT 8–41 U/L (female) and 9–59 U/L (male), with no significant regional differences in this study [5, cohort]. Preliminary upper reference limits from the IFCC's own inter-laboratory work were 34 U/L (female) and 45 U/L (male) at the 97.5th percentile, providing the method-anchored benchmarks that commercial platforms are expected to approach [6, cohort].

A statewide study of Indiana laboratories found that 83% of laboratories simply adopted their analyzer manufacturer's stated reference interval rather than conducting in-house healthy-volunteer studies, and those manufacturer intervals varied substantially across platforms [7, cohort]. This practice explains why stated ULN values for ALT in common use range from roughly 30 to 65 U/L depending on the laboratory — a range large enough to reclassify individual patients across clinical decision thresholds.

## Pre-analytical Considerations and Interferences

**Hemolysis.** ALT is relatively resistant to hemolysis interference. In an interference study, ALT concentrations were not clinically affected at hemoglobin concentrations up to 2.5–4.5 g/L (severely hemolyzed samples) — in marked contrast to AST and LDH, which are significantly elevated even at hemoglobin < 0.5 g/L (barely visible hemolysis) due to high intracellular concentrations of those enzymes in erythrocytes [8, cohort]. Mildly or moderately hemolyzed specimens are therefore acceptable for ALT measurement, whereas AST and LDH results from the same tube may need rejection or flagging.

**Lipemia.** Lipemic samples can introduce optical interference in spectrophotometric assays; on-board lipemia correction algorithms in modern analyzers partially mitigate but do not fully eliminate this effect at extreme lipemia.

**Sample stability.** ALT in serum is relatively stable but temperature-sensitive. A multi-platform stability study found ALT declines at approximately −4.8%/day at room temperature but only −0.9%/day under refrigeration — roughly a 5-fold improvement in stability with refrigeration [9, cohort]. Samples should be separated and refrigerated promptly; refrigerated serum is stable for several days, whereas room-temperature delays of more than a day introduce meaningful negative bias.

**Vitamin B6 status (P5P effect).** As detailed above, patient B6 deficiency is a pre-analytical variable in the biological sense: it reduces the apparent ALT in non-P5P assays. Populations at elevated risk of B6 deficiency include hemodialysis patients, those with malabsorption, and individuals with chronic inflammatory states.

**Diurnal and day-to-day biological variation.** ALT does not exhibit significant diurnal (within-day) variation, unlike cortisol or iron; fasting state at the time of draw is not required for routine clinical interpretation. There is, however, meaningful day-to-day intraindividual biological variation (coefficient of variation on the order of 10–15% within a healthy individual over weeks), which means that a single borderline-elevated value should be interpreted in the context of serial measurements before clinical action.

## Why Reference Intervals and ULN Are Method- and Population-Specific

The foregoing discussion converges on a single interpretive principle: the upper limit of normal (ULN) for ALT is not a universal biological constant but an analytical-and-statistical construct that depends on (a) assay temperature (37°C vs. older 30°C methods), (b) P5P supplementation status, (c) calibration traceability and commutability, (d) the demographic composition of the reference population (sex, age, BMI, metabolic health), and (e) the statistical threshold applied (95th vs. 97.5th percentile). Laboratories using non-IFCC-traceable, non-P5P methods must validate their own reference intervals rather than importing cutoffs from IFCC-anchored studies. Cross-institution comparisons of ALT results — for clinical trials, referral decisions, or population screening — require knowledge of the assay platform, P5P status, and reference interval in use at each site.

---

## Bibliography

1. Schumann G, Bonora R, Ceriotti F, Férard G, Ferrero CA, Franck PF, Gella FJ, Hoelzel W, Jørgensen PJ, Kanno T, Kessner A, Klauke R, Kristiansen N, Lessinger JM, Linsinger TPJ, Misaki H, Panteghini M, Pauwels J, Schiele F, Schimmel HG, Weidemann G, Siekmann L. IFCC primary reference procedures for the measurement of catalytic activity concentrations of enzymes at 37 degrees C. Part 4: Reference procedure for the measurement of catalytic concentration of alanine aminotransferase. *Clin Chem Lab Med.* 2002;40(7):718–24. PMID: 12241021. https://pubmed.ncbi.nlm.nih.gov/12241021/ — tag: mechanism_review — tier: 2

2. Brinc D, Agbor TA, Fabros A, Cheng PL, Kulasingam V, Selvaratnam R. The Harmonization Hurdle—A Case for Pyridoxal-5′-Phosphate. *J Appl Lab Med.* 2026. DOI: 10.1093/jalm/jfag018. https://academic.oup.com/jalm/advance-article/doi/10.1093/jalm/jfag018/8504010 — tag: mechanism_review — tier: 2

3. Ono K, Ono T, Matsumata T. The pathogenesis of decreased aspartate aminotransferase and alanine aminotransferase activity in the plasma of hemodialysis patients: the role of vitamin B6 deficiency. *Clin Nephrol.* 1995;43(6):405–8. PMID: 7554526. https://pubmed.ncbi.nlm.nih.gov/7554526/ — tag: cohort — tier: 2

4. Beste LA, Icardi M, Hunt CM, Gylys-Colwell I, Lowy E, Taylor L, Morgan TR, Chang MF, Maier MM, Cheung R. Alanine Aminotransferase Results Differ by Analyzer Manufacturer in a National Integrated Health Setting, 2012–2017. *Arch Pathol Lab Med.* 2020;144(6):748–754. PMID: 31697169. https://pubmed.ncbi.nlm.nih.gov/31697169/ — tag: cohort — tier: 2

5. Ceriotti F, Henny J, Queraltó J, Ziyu S, Özarda Y, Chen B, Boyd JC, Panteghini M. Common reference intervals for aspartate aminotransferase (AST), alanine aminotransferase (ALT) and γ-glutamyl transferase (GGT) in serum: results from an IFCC multicenter study. *Clin Chem Lab Med.* 2010;48(11):1593–1601. PMID: 21034260. https://pubmed.ncbi.nlm.nih.gov/21034260/ — tag: cohort — tier: 2

6. Schumann G, Klauke R. New IFCC reference procedures for the determination of catalytic activity concentrations of five enzymes in serum: preliminary upper reference limits obtained in hospitalized subjects. *Clin Chim Acta.* 2003;327(1–2):69–79. PMID: 12482620. https://pubmed.ncbi.nlm.nih.gov/12482620/ — tag: cohort — tier: 2

7. Dutta A, Saha C, Johnson CS, Chalasani N. Variability in the upper limit of normal for serum alanine aminotransferase levels: a statewide study. *Hepatology.* 2009;50(6):1957–62. PMID: 19787805. https://pubmed.ncbi.nlm.nih.gov/19787805/ — tag: cohort — tier: 2

8. Koseoglu M, Hur A, Atay A, Cuhadar S. Effects of hemolysis interferences on routine biochemistry parameters. *Biochem Med (Zagreb).* 2011;21(1):79–85. PMID: 22141211. https://pubmed.ncbi.nlm.nih.gov/22141211/ — tag: cohort — tier: 2

9. Bauça JM, Caballero A, Gómez C, Martínez-Espartosa D, García del Pino I, Puente JJ, Llopis MA, Marzana I, Segovia M, Ibarz M, Ventura M, Salas P, Gómez-Rioja R. Influence of study model, baseline catalytic concentrations and analytical system on the stability of serum alanine aminotransferase. *Adv Lab Med.* 2020. PMID: 37363778. https://pmc.ncbi.nlm.nih.gov/articles/PMC10158745/ — tag: cohort — tier: 2
