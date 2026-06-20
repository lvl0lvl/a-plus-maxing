# Section C: Measurement & Standardization

## C.1 The IFCC Reference Measurement Procedure

The IFCC reference measurement procedure for aspartate aminotransferase (AST) was published by Schumann et al. as Part 5 of the primary reference series for enzyme activity at 37°C [1, mechanism_review]. The procedure specifies: serum or plasma; reaction temperature 37°C; and supplementation with **pyridoxal-5′-phosphate (P5P, vitamin B6 coenzyme)** at 0.1 mmol/L, with a preincubation phase to reconstitute the apoenzyme before substrate addition [1, mechanism_review].

The P5P requirement is load-bearing. AST is a pyridoxal-phosphate–dependent transaminase; a portion of circulating AST exists as the inactive apoenzyme (cofactor-free). In populations with subclinical B6 deficiency — patients with acute myocardial infarction, chronic renal disease, inflammatory states, or alcohol use — this apoenzyme fraction is enlarged, and assays without P5P systematically underestimate true catalytic activity [2, mechanism_review]. Despite this, adoption has lagged: more than 60% of US laboratories and a similar proportion internationally still use aminotransferase assays without P5P supplementation, making full metrological traceability to the IFCC reference unachievable on those platforms [2, mechanism_review].

## C.2 The Coupled Enzymatic Assay (Reaction Principle)

The IFCC AST assay is a continuous kinetic indicator method [1, mechanism_review]. The primary (analytical) reaction is:

> L-aspartate + α-ketoglutarate **→** oxaloacetate + L-glutamate  (catalyzed by AST)

Oxaloacetate is detected via an indicator reaction with malate dehydrogenase (MDH) and NADH:

> Oxaloacetate + NADH + H⁺ **→** L-malate + NAD⁺  (catalyzed by MDH)

Because NADH absorbs at 340 nm and NAD⁺ does not, the reaction is measured as a continuous **decrease in absorbance at 340 nm**; ΔA₃₄₀/min is proportional to AST activity reported in U/L [1, mechanism_review]. Lactate dehydrogenase (LDH) is co-included to scavenge endogenous pyruvate, preventing spurious NADH consumption. MDH is added in excess to maintain linearity up to approximately 700 U/L. A 60–90 s blank/lag phase precedes the measurement interval; timing starts once the absorbance decrease is confirmed linear.

## C.3 Hemolysis: A Dominant Pre-Analytic Interference

Hemolysis is the single most clinically significant pre-analytic interference for AST, and the effect is qualitatively different from its effect on ALT [3, 4, cohort]. The mechanism is simple: the **intracellular concentration of AST in red blood cells is approximately 40× higher than in serum/plasma** [3, cohort]. Erythrocyte lysis therefore releases large quantities of AST directly into the sample.

The practical impact is quantified across multiple studies. At a hemolysis index (H-index) of 1+ (≈100 mg/dL free hemoglobin), AST rises by approximately 9.3% from baseline [3, cohort]. At severe hemolysis (plasma Hgb ~4.5 g/L), AST increases by roughly 30 U/L — a 2.5-fold rise above baseline — at levels below the threshold of visual detection [4, cohort]. Concentration-specific H-index thresholds have been developed: for AST values within the reference interval (8–48 U/L male; 8–43 U/L female), an H-index up to 50–100 may be tolerable with an interpretive comment rather than outright rejection [5, open_label].

**ALT is largely immune to this effect.** Studies consistently find ALT percent differences from baseline of less than 3–5% across all clinically encountered hemolysis levels [3, 4, cohort]. This means hemolysis artifactually elevates the AST:ALT ratio — a critical pitfall when the ratio is used to distinguish alcoholic from non-alcoholic disease. Any elevated AST in a hemolyzed specimen must be flagged; if the elevation is isolated and unexplained, specimen recollection is required before clinical action.

## C.4 Macro-AST: Spurious Persistent Elevation

A distinct cause of persistently elevated AST — one that mimics chronic liver or muscle disease — is **macro-AST**: a high-molecular-weight complex formed by the non-covalent binding of AST to a circulating immunoglobulin, most commonly IgG [6, mechanism_review]. The complex is too large for normal clearance, so AST activity accumulates in serum despite the absence of organ injury [6, mechanism_review].

The clinical signature is characteristic: AST elevated (sometimes markedly), ALT normal, all other organ-damage markers (ALP, GGT, bilirubin, creatine kinase, troponin) unremarkable. This pattern should trigger macro-AST testing rather than invasive workup.

**Detection** relies on **polyethylene glycol (PEG) precipitation**: PEG (20–25% w/v) precipitates immunoglobulins and their bound complexes. Residual supernatant AST activity ≤40% of the pre-precipitation value (i.e., a drop of ≥60%) confirms macro-AST [6, mechanism_review]. Alternative approaches — ultrafiltration and protein-A/G immunodepletion — yield consistent results and can characterize the immunoglobulin class [6, mechanism_review].

An important interpretive nuance: P5P can reactivate the apoenzyme fraction within the macro-AST complex, so P5P-supplemented assays may measure higher macro-AST activity than non-supplemented assays. This means a laboratory's transition to an IFCC-compliant P5P platform can unmask or amplify macro-AST that was previously cryptic; PEG precipitation results should be interpreted using the same analytical method (with or without P5P) for both pre- and post-precipitation measurements [7, mechanism_review]. Macro-AST is a **benign finding** — once confirmed, no organ-directed treatment is required.

## C.5 Cytosolic vs. Mitochondrial Isoenzymes

AST exists as two genetically distinct isoenzymes: **cytosolic AST (cAST, AST1)** and **mitochondrial AST (mAST, AST2)**. Although hepatocytes contain approximately 80% mAST by total activity, **healthy serum is dominated by cAST**; mitochondrial AST is a minor fraction in the absence of severe or necrotic injury. This disparity reflects the compartmental barrier: mild, reversible membrane damage releases cAST preferentially, while mAST release requires disruption of the inner mitochondrial membrane.

**Elevated mAST** therefore signals severe injury — liver ischemia, acute necrosis, halothane hepatotoxicity. In alcoholic hepatitis, the mAST:cAST ratio in serum is elevated relative to viral hepatitis, reflecting mitochondrial susceptibility to ethanol; in uncomplicated viral hepatitis, cell-membrane damage predominates and cAST dominates the release pattern. mAST can be selectively measured via immunoinhibition (anti-mAST antibodies suppress mAST activity, leaving cAST measurable) or immunoassay. However, mAST measurement lacks IFCC standardization and is not routinely available. It remains a specialized research and clinical tool.

## C.6 Sample Stability

Serum AST is robust to freeze-thaw cycling: Cuhadar et al. (2013) found no statistically significant change after ten freeze-thaw cycles at −20°C, and stability extended over three months of storage at −20°C [8, cohort]. For routine samples, separation within 1–2 hours and measurement within 24 hours at 2–8°C is standard practice. Stability data are contingent on the absence of hemolysis — hemolyzed samples are artifactually elevated at collection and remain unreliable regardless of storage. Severe lipemia can impair 340 nm absorbance measurement in instruments without bichromatic correction.

---

## Bibliography

1. Schumann G, Bonora R, Ceriotti F, Férard G, Ferrero CA, Franck PFH, Gella FJ, Hoelzel W, Jørgensen PJ, Kanno T, Kessner A, Klauke R, Kristiansen N, Lessinger JM, Linsinger TPJ, Misaki H, Panteghini M, Pauwels J, Schimmel HG, Vialle A, Weidemann G, Schlenck A. IFCC primary reference procedures for the measurement of catalytic activity concentrations of enzymes at 37°C. Part 5. Reference procedure for the measurement of catalytic concentration of aspartate aminotransferase. *Clin Chem Lab Med.* 2002;40(7):725–733. https://doi.org/10.1515/CCLM.2002.125 — tag: mechanism_review — tier: 1

2. Brinc D, Agbor TA, Fabros A, Cheng PL, Kulasingam V, Selvaratnam R. The harmonization hurdle — a case for pyridoxal-5′-phosphate. *J Appl Lab Med.* 2026. https://doi.org/10.1093/jalm/jfag018 — tag: mechanism_review — tier: 1

3. Parambu MM, Bush V. Evaluation of sensitive analytes to hemolysis interference on an automated chemistry analyzer. *J Appl Lab Med.* 2024;9(3):558–564. https://doi.org/10.1093/jalm/jfad124 — tag: cohort — tier: 1

4. Koseoglu M, Hur A, Atay A, Cuhadar S. Effects of hemolysis interference on routine biochemistry parameters. *Biochem Med (Zagreb).* 2011;21(1):79–85. https://doi.org/10.11613/BM.2011.015 — tag: cohort — tier: 1

5. Rosemark CL, Baumann N, Block D, Andress B. Reducing hemolyzed specimen rejection for aspartate aminotransferase (AST): a quality improvement initiative to further optimize concentration-specific H-index thresholds. *Clin Chem.* 2024;70(Suppl 1):hvae106.097. https://doi.org/10.1093/clinchem/hvae106.097 — tag: open_label — tier: 1

6. van Wijk XMR, Magee CA, Wu AHB, Tana MM, Lynch KL. A comparison of methods for evaluation of a case of suspected macro-aspartate aminotransferase. *Clin Chim Acta.* 2016;463:1–3. https://doi.org/10.1016/j.cca.2016.10.011 — tag: mechanism_review — tier: 1

7. Fermon EJ, Sy M, Drake TA, Song L. "Activation" of macro-AST by pyridoxal-5-phosphate in the assay for aspartate aminotransferase. *Clin Chem Lab Med.* 2024;63(4):e97–e100. PMID 39402965. https://doi.org/10.1515/cclm-2024-0944 — tag: mechanism_review — tier: 1

8. Cuhadar S, Koseoglu M, Atay A, Dirican A. The effect of storage time and freeze-thaw cycles on the stability of serum samples. *Biochem Med (Zagreb).* 2013;23(1). https://doi.org/10.11613/BM.2013.009 — tag: cohort — tier: 1
