---
title: "GlycA — Glycoprotein Acetylation (NMR Inflammation Marker): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/glyca/research-report
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.glyca-design-work
provenance_slug: labs-specialist
source_count: 19
---

# GlycA — Glycoprotein Acetylation (NMR Inflammation Marker): Canonical Research Report

## Summary

GlycA (glycoprotein acetylation, also written "glycoprotein acetyls") is not a single molecule. It is a composite signal extracted from proton nuclear magnetic resonance (NMR) spectroscopy of serum or plasma, arising from the mobile N-acetyl methyl protons of glycan side chains — chiefly a subset of N-acetylglucosamine residues — on enzymatically glycosylated acute-phase proteins [1, cohort][8, mechanism_review]. Because the measured peak (near 2.0 ppm in the ¹H spectrum) integrates both the circulating concentrations and the glycosylation states of several abundant acute-phase glycoproteins at once, GlycA functions as an aggregate readout of the systemic acute-phase response rather than a measure of any one analyte [8, mechanism_review][2, mechanism_review].

The practical case for GlycA rests on two properties. First, it is a more time-stable, cumulative index of low-grade systemic inflammation than high-sensitivity C-reactive protein (hs-CRP): its within-subject biological variability is roughly 4.3% over five weeks versus about 29% for hs-CRP, while it still correlates only moderately with hs-CRP (r ≈ 0.56), confirming it carries overlapping-but-distinct inflammatory information [1, cohort]. Second, across large prospective cohorts it independently associates with incident cardiovascular disease (CVD), incident type 2 diabetes (T2D), all-cause and cardiovascular mortality, and severe infection — frequently retaining significance after adjustment for hs-CRP and other inflammatory markers [2, cohort][3, cohort][4, cohort][7, cohort][6, cohort].

Two honesty caveats are load-bearing throughout this report. (1) **Units are platform-specific and not interchangeable.** The Nightingale Health NMR platform reports GlycA on a scale near 1.2–1.5 mmol/L, whereas the LabCorp NMR LipoProfile assay reports a different scale near 369 μmol/L (healthy) — roughly threefold apart and never numerically comparable [7, mechanism_review][2, mechanism_review][10, cohort]. (2) **There is no universally adopted clinical cut-point.** Cohort risk is reported by quartile or percentile, not against a validated threshold; the often-quoted "400 μmol/L" is a proposed research threshold on the LabCorp scale only [2, mechanism_review][9, mechanism_review][11, mechanism_review]. GlycA remains a research/emerging-grade biomarker — offered by some laboratories but not a routine, society-guideline-endorsed clinical test.

This report merges validated identity, physiology, and disease-association material with validated reference-range, measurement, and determinant material into a single goal-agnostic canonical reference. It is written for any clinician or operator and is not personalized.

## Identity & Physiology

### A composite NMR signal, not a molecule

GlycA originates from the mobile N-acetyl methyl protons of glycan side chains — specifically a subset of N-acetylglucosamine residues — on enzymatically glycosylated acute-phase proteins [1, cohort]. The signal sits at approximately 2.0 ppm in the proton (¹H) NMR spectrum of plasma or serum [2, mechanism_review]. The dominant contributors are five abundant acute-phase glycoproteins: α1-acid glycoprotein (orosomucoid), haptoglobin, α1-antitrypsin, α1-antichymotrypsin, and transferrin [1, cohort][2, mechanism_review]. Because the measured signal integrates both the circulating protein levels and the glycosylation states of these proteins, GlycA reads out the systemic acute-phase response as a whole rather than the concentration of any one analyte [8, mechanism_review].

This composite character is the conceptual key to the marker. Conventional single-protein inflammation markers (hs-CRP, fibrinogen, individual cytokines) each track one node of the inflammatory network with its own kinetics and noise. GlycA, by integrating across several proteins and their post-translational glycosylation, produces a smoothed, slow-moving index — closer in spirit to HbA1c's relationship to glucose than to a single spot measurement [9, mechanism_review].

### A genuine acute-phase composite driven by IL-6

The contributing proteins are bona fide positive acute-phase reactants. α1-acid glycoprotein, haptoglobin, α1-antitrypsin, and fibrinogen-family glycoproteins are liver-derived proteins whose synthesis is induced by interleukin-6 (IL-6) during inflammation [9, regulatory]. As a reference point for the magnitude and heterogeneity of the acute-phase response, CRP can rise 100- to 1000-fold during acute inflammation, whereas fibrinogen rises later and only about 2-fold [9, regulatory]. A composite signal therefore smooths over the very different kinetics of its individual components: the slow, modest movers and the fast, large movers are averaged into one peak. This is precisely why GlycA behaves as a cumulative inflammatory-burden index rather than a sharp acute-event marker.

Mechanistically, then, GlycA reflects inflammation *burden* rather than any specific disease pathway. It is elevated in chronic inflammatory disease and tracks disease activity — for example in rheumatoid arthritis, systemic lupus erythematosus, and psoriasis [8, mechanism_review][2, mechanism_review]. This breadth is its strength as an integrator and, simultaneously, the reason it cannot localize a mechanism: a raised GlycA says "systemic inflammatory tone is elevated," not "this organ, this pathway."

### Relationship to conventional inflammation markers

GlycA correlates moderately with conventional inflammation markers but is not redundant with them. In the analytical-validation cohort (MESA, n = 5537), GlycA correlated with hs-CRP at r = 0.56, with fibrinogen at r = 0.46, and with IL-6 at r = 0.35 (all P < 0.0001) [1, cohort]. In the Women's Health Study the GlycA–hs-CRP Spearman correlation was r = 0.61 (P < 0.0001) [2, cohort], and in the PREVEND cohort the univariate GlycA–hs-CRP correlation was 0.67 [5, cohort]. These are moderate, not high, correlations — the signature of two markers that capture overlapping but partly distinct facets of inflammation [8, mechanism_review]. The practical consequence, borne out in the cohort data below, is that GlycA adds prognostic information beyond hs-CRP rather than merely duplicating it.

## Evidence & Associations

A consistent picture emerges across prospective cohorts: GlycA is a cumulative, NMR-derived index of systemic low-grade inflammation that independently associates with incident CVD, incident T2D, all-cause and cardiovascular mortality, and severe infection, frequently retaining significance after adjustment for hs-CRP [4, cohort][7, cohort][8, mechanism_review]. The headline effect sizes are summarized below; several of the largest derive from the Women's Health Study (WHS), which is women-only — annotated inline.

### Incident cardiovascular disease

In 27,491 initially healthy **women** in the WHS (median follow-up 17.2 years, 1,648 incident CVD events), hazard ratios (HRs) for CVD across GlycA quartiles 1→4 were 1.00, 1.10 (95% CI 0.92–1.30), 1.34 (95% CI 1.13–1.58), and 1.64 (95% CI 1.39–1.93), Ptrend < 0.0001 — comparable in magnitude to hs-CRP [2, cohort]. After lipid adjustment the per-1-SD HR was 1.15 (95% CI 1.08–1.21; P < 0.0001), and it remained 1.08 (95% CI 1.01–1.15; P = 0.02) even after mutual adjustment for hs-CRP [2, cohort] — direct evidence of non-redundant inflammatory-burden information.

The association replicates in independent, mixed-sex cohorts. In PREVEND (Dutch general population, n = 4,759; 298 events over 8.5 years), the fully adjusted per-1-SD HR for incident CVD was 1.16 (95% CI 1.01–1.33; P = 0.04), and risk was highest when both GlycA and hs-CRP were elevated (HR 1.79; 95% CI 1.31–2.46; P < 0.001) [5, cohort]. On a continuous scale in the very large UK Biobank (n = 118,461, mixed-sex, Nightingale platform), each 1-SD increment in GlycA is associated with roughly 26% higher risk across a wide range of incident diseases (median HR ≈ 1.26 per SD) [5b, cohort], and a separate analysis reports about 43% higher 5-year cardiovascular mortality risk per SD [11, mechanism_review]. A quartile illustration from MESA (n = 6,507, ages 45–84, median 14-year follow-up): the highest-versus-lowest GlycA quartile predicted incident heart failure with preserved ejection fraction (adjusted HR 2.18, 95% CI 1.15–4.13) but not HFrEF (HR 1.06, 95% CI 0.63–1.79) [11, mechanism_review].

### Incident type 2 diabetes

In 26,508 diabetes-free **women** (WHS, 17.2-year median follow-up, 2,087 incident cases), the unadjusted GlycA quartile-4-versus-1 HR for incident T2D was 2.67 (95% CI 2.26–3.14), attenuating to 1.65 (95% CI 1.39–1.95) after adjustment for conventional risk factors and to 1.11 (95% CI 0.93–1.33; Ptrend = 0.10) after mutual adjustment for hs-CRP [3, cohort]. The honest reading: the crude diabetes signal is strong, but a substantial part of it is shared with hs-CRP and conventional risk factors — after full mutual adjustment the residual GlycA-specific T2D association is no longer significant in this women-only cohort.

### All-cause and cardiovascular mortality

In the WHS extended to 27,524 **women** (median follow-up 20.5 years, 3,523 deaths), the risk-factor-adjusted per-1-SD HR for all-cause mortality was 1.21 (95% CI 1.06–1.40) at 5 years and 1.14 (95% CI 1.09–1.16) at maximal follow-up; the JUPITER trial replication cohort (n = 12,527, statin-eligible elevated-hs-CRP population, mixed-sex) gave a per-1-SD HR of 1.33 (95% CI 1.21–1.45) [7, cohort]. In MESA (multi-ethnic US, n = 6,523; median 12.1-year follow-up), the per-1-SD GlycA relative risk ranged 1.05–1.20 for total death (915 events), total CVD events (922), and chronic inflammatory-related disease (1,324), persisting after adjustment for hs-CRP, IL-6, and D-dimer [4, cohort]. The persistence after adjustment for three other inflammatory markers is the key result: GlycA is not simply a noisier restatement of hs-CRP or IL-6.

### Severe infection and hospitalization

In the population-based FINRISK 1997 cohort (Finnish general population, n = 7,599; 13.8-year follow-up), baseline GlycA predicted long-term infection risk. Per-1-SD HRs were 1.40 for hospitalization from non-localized infection (P = 2×10⁻⁹, 585 cases) and 1.48 for respiratory-infection hospitalization (P = 3×10⁻¹², 571 cases); for fatal non-localized infection the HR was 2.36 (P = 8×10⁻⁵, 29 cases), driven largely by septicemia (HR 2.25, P = 4×10⁻³, 18 cases) [6, cohort]. This infection link is mechanistically coherent with GlycA as a chronic-inflammation/immune-tone integrator: a higher baseline inflammatory burden tracks higher long-term susceptibility to severe infection.

### Evidence-grade honesty

Putting the cohorts together, GlycA carries non-redundant inflammatory-burden information that independently associates with CVD, T2D, mortality, and severe infection, and it does so with the practical advantage of greater measurement stability than hs-CRP. But the grade must be stated plainly: GlycA reflects inflammation *burden*, not a specific disease mechanism, and it remains a **research/emerging-grade** biomarker. It is offered by some laboratories but is **not** a routine, guideline-endorsed clinical test, and society guidelines do not yet recommend it for risk stratification [8, mechanism_review]. Several headline effect sizes (CVD, T2D, mortality) derive from the women-only WHS — annotated above — so sex-generalizability rests on the replication cohorts (PREVEND, MESA, FINRISK, UK Biobank). Claims that a single GlycA draw can replace serial hs-CRP measurements originate from assay-maker framing and are reported here only as context, never as an efficacy basis [8, mechanism_review].

## Reference Ranges & Units

This section carries two of the report's most consequential caveats: the unit scale is platform-specific, and there is no universal cut-point.

### Units are platform-specific and not interchangeable

There is **no single canonical unit** for GlycA. The reported unit and numeric scale depend on the measurement platform, and values from different platforms are **not interchangeable**:

- **Nightingale Health platform** (Finland; used across UK Biobank and Finnish cohorts) reports GlycA in **mmol/L** [7, mechanism_review]. Typical general-population means cluster around **~1.2–1.5 mmol/L** — e.g. cohort means of 1230, 1216, 1233, and 1236 μmol/L (= 1.23–1.24 mmol/L) across several cohorts processed on the Nightingale pipeline [10, cohort, preprint]. The same platform's figures appear in the literature labelled either "mmol/L" or "μmol/L"; 1230 μmol/L ≡ 1.23 mmol/L — the same scale ×1000 [10, cohort][7, mechanism_review].
- **LabCorp NMR LipoProfile** reports a **different μmol/L scale entirely**, with healthy-population values near **369 μmol/L (IQR 326–416)** [2, mechanism_review].

The two scales differ by roughly threefold and **must not be compared numerically**. A "1.3" from Nightingale and a "390" from LabCorp are both "normal" on their own platforms; treating either number as portable to the other platform is an error. Always record which platform produced a value.

### No universally adopted clinical cut-point

This is a load-bearing caveat. **There is no universally adopted clinical cut-point for GlycA.** Cohort studies report risk by **quartiles or percentiles**, not against a validated threshold [9, mechanism_review][11, mechanism_review]. The "400 μmol/L" value sometimes cited as a cut-point for systemic inflammatory states is a *research/proposed* threshold specific to the LabCorp μmol/L scale, not an FDA- or society-endorsed clinical decision limit [2, mechanism_review]. Sex-specific reference ranges have been called for but **not yet established** [9, mechanism_review]. Any cut-point claim should be treated as provisional / emerging-grade.

For population context only (not a clinical threshold): on the Nightingale scale, general-population means run ~1.2–1.5 mmol/L [10, cohort][7, mechanism_review]; on the LabCorp scale, healthy means run ~369 μmol/L, with chronic-inflammatory-disease cohorts higher — RA 398 μmol/L (348–473), SLE 398 (350–445), psoriasis mean 412.3 μmol/L versus 369 (326–416) in healthy women [2, mechanism_review]. Risk in cohorts is consistently expressed per-SD or by quartile; the practical interpretation for an operator is *relative position within a population distribution and change over time*, not crossing a fixed line.

## Measurement

### Quantified by high-throughput proton NMR

GlycA is quantified by **high-throughput proton (¹H) NMR spectroscopy** of plasma or serum, reading the composite N-acetyl peak near 2.0 ppm [2, mechanism_review][1, cohort]. The two dominant platforms are the **Nightingale Health** platform (the platform behind UK Biobank and the Finnish cohorts) [5b, cohort][7, mechanism_review] and the **LabCorp NMR LipoProfile** assay (the platform on which the original Otvos analytical validation was performed) [1, cohort][2, mechanism_review]. The platform identity governs both the unit and the numeric scale (see Reference Ranges & Units).

### Analytical performance and biological stability — lower variability than hs-CRP

GlycA's defining practical advantage over hs-CRP is its **stability**. In the original analytical validation (LabCorp NMR LipoProfile), analytic precision was **intra-assay CV 1.9%** and **inter-assay CV 2.6%** [1, cohort]. Critically, **within-subject (intra-individual) biological variability was 4.3%** over 5 weeks in 23 healthy volunteers — far lower than **hs-CRP (29.2%)**, and also lower than cholesterol (5.7%) and triglycerides (18.0%) [1, cohort]. A review summarizes this as roughly **~5% biological variability for GlycA versus ~30% for hs-CRP**, likening GlycA to HbA1c — an integrated, slow-moving marker without the day-to-day or post-prandial swings of hs-CRP, which can stay elevated for days to weeks after a minor infection [9, mechanism_review]. The Nightingale platform documentation independently states that GlycA has **greater long-term stability than hs-CRP** [7, mechanism_review].

The interpretive payoff is direct: because a single GlycA draw integrates over a longer window with much less within-person noise, it is a cleaner estimate of an individual's chronic inflammatory tone than a single hs-CRP — which is the legitimate, evidence-grounded version of the "single draw" claim, distinct from the assay-maker marketing version flagged above. As noted, GlycA correlates only moderately with other inflammatory markers (hs-CRP r = 0.56, fibrinogen r = 0.46, IL-6 r = 0.35; all P < 0.0001 in MESA, n = 5537) [1, cohort], confirming it captures an overlapping-but-distinct inflammatory signal rather than restating hs-CRP.

## Determinants

GlycA is modifiable. Roughly 30% of population variance is genetic and the majority is acquired — driven by inflammation, adiposity, smoking, age, and lifestyle — which is what makes the determinant list actionable.

**Systemic inflammation / infection.** As an acute-phase composite, GlycA rises with active inflammation and is elevated in chronic inflammatory disease — e.g. RA 398 μmol/L (348–473), SLE 398 (350–445), psoriasis mean 412.3 μmol/L on the LabCorp scale versus 369 μmol/L (326–416) in healthy women [2, mechanism_review].

**Adiposity / BMI.** GlycA tracks adipose-associated low-grade inflammation. In severe obesity, baseline GlycA was **451 ± 47 μmol/L vs 326 ± 36 μmol/L** in normal-BMI controls [3, cohort]; the within-group cross-sectional correlation with BMI is, however, **modest** (r = 0.14, p = 0.33 in one obese cohort) [3, cohort] — i.e. obesity raises the level meaningfully, but BMI does not finely predict GlycA within an already-obese group.

**Smoking.** A strong, dose-dependent determinant. In pooled MESA + ELSA-Brasil (n = 11,509), adjusted mean GlycA was **+19.9 μmol/L (95% CI 16.6–23.2) in current smokers** and **+4.1 μmol/L (1.7–6.6) in former smokers** versus never-smokers [8b, cohort]. Each 5-pack-year increase added +1.6 μmol/L (current) and +0.7 μmol/L (former); each 5 years since quitting lowered GlycA by 1.6 μmol/L [8b, cohort].

**Age and sex.** GlycA correlates moderately positively with age (inflammaging) [9, mechanism_review][11, mechanism_review]. The **sex difference is small**: women run slightly higher than men but the gap **does not exceed ~10%** — in marked contrast to hs-CRP, which is ~40% higher in women [9, mechanism_review]. (This small sex gap is part of why the women-only WHS effect sizes are taken as broadly informative, though sex-generalizability still rests on the mixed-sex replication cohorts.)

**Statins — modest to negligible effect.** Whereas statins lower hs-CRP substantially (rosuvastatin reduced hs-CRP **37%** in JUPITER, external context), **GlycA itself does not fall meaningfully with statin therapy**: in the JUPITER post-hoc analysis (N = 10,039, median 1.9-year follow-up), statin therapy reduced CVD incidence across GlycA quartiles, but "GlycA levels failed to show significant reductions … in response to statins" [9, mechanism_review]. This is a key contrast with hs-CRP and supports GlycA capturing a statin-resistant residual-inflammatory component. (The 37% statin→hs-CRP figure is cited from JUPITER for contrast only and is not a GlycA numeric claim.)

**Weight loss.** GlycA is meaningfully lowered by substantial weight loss: after bariatric surgery it fell from 451 ± 47 to **383 ± 50 μmol/L at 6 months (~15%, p < 0.001)** and **348 ± 41 μmol/L at 12 months (~23%, p < 0.001)**, with the change tracking weight change (r = 0.41, p = 0.002) [3, cohort].

**Exercise.** Regular endurance exercise modestly lowers GlycA. A combined analysis of 14 exercise interventions (n = 1568, 7 studies) found a pooled reduction of **−9.12 ± 1.9 μmol/L (p = 1.22 × 10⁻⁶)** after adjustment for age, sex, race, and baseline BMI — i.e. the effect is **independent of those covariates** [4b, meta_analysis].

**Heritability.** GlycA is **modestly heritable**: familial variance-decomposition in TwinsUK gave **h² = 0.2971 ± 0.0802 (p = 2.11 × 10⁻⁴)** — comparable to CRP (0.2786 ± 0.0246) — with a genetic correlation between the two of Rg = 0.4397 ± 0.0854 [6b, cohort]. So ~30% of population variance is genetic; the majority is acquired (inflammation, adiposity, smoking, lifestyle), consistent with the modifiable determinants above [6b, cohort].

## Clinical Significance

GlycA is best understood as an **integrated, cumulative index of low-grade systemic inflammation** — an inflammatory analogue of HbA1c, smoothing over the kinetic heterogeneity of its constituent acute-phase proteins into one slow-moving number [9, mechanism_review][1, cohort]. Its clinical value, on current evidence, rests on three legs: (1) it predicts incident CVD, T2D, all-cause/CV mortality, and severe infection across multiple large prospective cohorts [2, cohort][3, cohort][4, cohort][7, cohort][6, cohort]; (2) it frequently retains significance after adjustment for hs-CRP, IL-6, and other markers, so it carries non-redundant inflammatory-burden information [4, cohort][2, cohort]; and (3) it is far more analytically and biologically stable than hs-CRP (~5% vs ~30% within-person variability), making a single draw a cleaner estimate of chronic inflammatory tone [1, cohort][9, mechanism_review].

Against those strengths, the limits are equally clear and must travel with every use. GlycA is **research/emerging-grade**: it is offered by some laboratories but is not a routine, society-guideline-endorsed clinical test, and no professional society currently recommends it for risk stratification [8, mechanism_review]. There is **no universal clinical cut-point** — risk is quartile/percentile-based, and the "400 μmol/L" figure is a provisional research threshold on the LabCorp scale only [2, mechanism_review][9, mechanism_review]. **Units are platform-specific and non-interchangeable** (Nightingale mmol/L ~1.2–1.5; LabCorp μmol/L ~369), so a value is meaningless without its platform [7, mechanism_review][2, mechanism_review][10, cohort]. Several headline associations derive from the women-only WHS, with sex-generalizability resting on mixed-sex replication cohorts [2, cohort][7, cohort].

The actionable reading for an operator or clinician: interpret GlycA as a *relative position within a population distribution on a stated platform, tracked longitudinally* — not as a number to be compared against a fixed clinical line or across platforms. It is modifiable through the determinants above (weight loss ~15–23% after bariatric surgery; endurance exercise ~−9 μmol/L pooled; smoking cessation), and notably is **not** meaningfully lowered by statins, marking a statin-resistant residual-inflammatory component [9, mechanism_review][3, cohort][4b, meta_analysis][8b, cohort]. Used this way — as a stable, trackable inflammatory-burden index rather than a guideline-grade decision threshold — GlycA is a defensible adjunct, while the honest grade remains: promising, replicated, but not yet clinically endorsed.

## Bibliography

Merged, deduplicated, and renumbered across Sections A and B. Format: Authors. Title. Journal. Year. PMID/DOI — tag — tier. Open-access and preprint sources flagged. Otvos 2015 was the only source appearing in both sections (de-duplicated to a single entry, [1]).

1. Otvos JD, Shalaurova I, Wolak-Dinsmore J, Connelly MA, Mackey RH, Stein JH, Tracy RP. GlycA: A Composite Nuclear Magnetic Resonance Biomarker of Systemic Inflammation. Clin Chem. 2015;61(5):714–723. PMID 25779987; DOI 10.1373/clinchem.2014.232918 — cohort (analytical validation, MESA n=5537) — Tier 1.
2. Akinkuolie AO, Buring JE, Ridker PM, Mora S. A Novel Protein Glycan Biomarker and Future Cardiovascular Disease Events. J Am Heart Assoc. 2014;3(5):e001221. PMID 25249300; DOI 10.1161/JAHA.114.001221 — cohort (Women's Health Study, women only) — Tier 1 — open-access.
3. Akinkuolie AO, Pradhan AD, Buring JE, Ridker PM, Mora S. Novel Protein Glycan Side-Chain Biomarker and Risk of Incident Type 2 Diabetes Mellitus. Arterioscler Thromb Vasc Biol. 2015;35(6):1544–1550. PMID 25908766; DOI 10.1161/ATVBAHA.115.305635 — cohort (Women's Health Study, women only) — Tier 1.
4. Duprez DA, Otvos J, Sanchez OA, Mackey RH, Tracy R, Jacobs DR Jr. Comparison of the Predictive Value of GlycA and Other Biomarkers of Inflammation for Total Death, Incident Cardiovascular Events, Noncardiovascular and Noncancer Inflammatory-Related Events, and Total Cancer Events. Clin Chem. 2016;62(7):1020–1031. PMID 27173011; DOI 10.1373/clinchem.2016.255828 — cohort (MESA, multi-ethnic) — Tier 1.
5. Gruppen EG, Riphagen IJ, Connelly MA, Otvos JD, Bakker SJL, Dullaart RPF. GlycA, a Pro-Inflammatory Glycoprotein Biomarker, and Incident Cardiovascular Disease: Relationship with C-Reactive Protein and Renal Function. PLoS One. 2015;10(9):e0139057. PMID 26398105; DOI 10.1371/journal.pone.0139057 — cohort (PREVEND, Dutch) — Tier 1 — open-access.
5b. Julkunen H, Cichońska A, Tiainen M, et al. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nat Commun. 2023;14:604. PMC9898515; DOI 10.1038/s41467-023-36231-7 — cohort (UK Biobank, Nightingale platform) — Tier 1 — open-access.
6. Ritchie SC, Würtz P, Nath AP, Abraham G, Havulinna AS, Fearnley LG, et al. The Biomarker GlycA Is Associated with Chronic Inflammation and Predicts Long-Term Risk of Severe Infection. Cell Systems. 2015;1(4):293–301. PMID 27136058; DOI 10.1016/j.cels.2015.09.007 — cohort (FINRISK 1997, Finnish general population) — Tier 1.
6b. Coelewij L, et al. GlycA and CRP Are Genetically Correlated: Insight into the Genetic Architecture of Inflammageing. Biomolecules. 2024;14(5):563. DOI 10.3390/biom14050563 — cohort (TwinsUK) — Tier 1 — open-access, flagged single-source heritability figure.
7. Lawler PR, Akinkuolie AO, Chandler PD, et al. Circulating N-Linked Glycoprotein Acetyls and Longitudinal Mortality Risk. Circ Res. 2016;118(7):1106–1115. PMID 26951635; DOI 10.1161/CIRCRESAHA.115.308078 — cohort (Women's Health Study + JUPITER replication; WHS women only) — Tier 1.
8. Connelly MA, Otvos JD, Shalaurova I, Playford MP, Mehta NN. GlycA, a novel biomarker of systemic inflammation and cardiovascular disease risk. J Transl Med. 2017;15(1):219. PMID 29078787; DOI 10.1186/s12967-017-1321-6 — mechanism_review — Tier 1 — open-access.
8b. McGarrah RW, et al. Association Between Smoking and Serum GlycA and hs-CRP Levels: MESA and ELSA-Brasil. J Am Heart Assoc. 2017;6(8):e006545. PMID 28838917; DOI 10.1161/JAHA.117.006545 — cohort — Tier 1 — open-access.
9. Jain S, Gautam V, Naseem S. Physiology, Acute Phase Reactants. StatPearls [Internet]. StatPearls Publishing / NCBI Bookshelf, National Library of Medicine (NIH). Bookshelf ID NBK519570 — regulatory — Tier 2.
   (Note: in this merged report, [9] is also used for the GlycA-specific mechanism-review framing from Ballout RA, Remaley AT. GlycA: a new biomarker for systemic inflammation and cardiovascular disease (CVD) risk assessment. J Lab Precis Med. 2020 — mechanism_review — Tier 1. See [9-review] below.)
9-review. Ballout RA, Remaley AT. GlycA: a new biomarker for systemic inflammation and cardiovascular disease (CVD) risk assessment. J Lab Precis Med. 2020 — mechanism_review — Tier 1.
10. The inflammatory marker glycoprotein acetyls is associated with cardiovascular outcomes. medRxiv 2025; DOI 10.1101/2025.12.01.25341421 — cohort — Tier 1 — PREPRINT, not peer-reviewed.
11. Towards clinical application of GlycA and GlycB for early detection of inflammation associated with (pre)diabetes and cardiovascular disease. J Inflamm (Lond). 2023. DOI 10.1186/s12950-023-00358-7 — mechanism_review — Tier 1 — open-access.
12. Connelly MA, et al. GlycA measured by NMR spectroscopy is associated with disease activity and cardiovascular disease risk in chronic inflammatory diseases. PMC8315361 — mechanism_review — Tier 1 — open-access. (Distinct paper from [8]; both Connelly reviews retained as separate entities per cross-section reconciliation.)
13. Nightingale Health. Venous blood analysis — Blood biomarker data analysis guide. V1.0, 11/2025 — mechanism_review (platform documentation citing primaries) — Tier 1-equivalent technical documentation.

*External context (statin→hs-CRP magnitude, JUPITER design) is cited for contrast only and is not a GlycA numeric claim: JUPITER (N Engl J Med 2008;359:2195) reported rosuvastatin lowering hs-CRP 37% — used solely to frame the GlycA-vs-statin contrast established by the GlycA reviews.*

**Bibliography note on inline citation keys.** To preserve every verified number from both source sections without renumber collisions, the inline keys map to this bibliography as follows: [1] Otvos 2015; [2] Akinkuolie 2014 CVD (in Evidence sections) — and, where the text concerns LabCorp-scale units/cut-point/disease-cohort means, the Connelly disease-activity review [12]; [3] Akinkuolie 2015 T2D and (in Determinants) the bariatric-surgery cohort [3b: Elevated GlycA in Severe Obesity is Normalized by Bariatric Surgery, PMC6585399 — cohort — Tier 1 — open-access]; [4] Duprez 2016 MESA and [4b] the exercise meta-analysis (Effects of regular endurance exercise on GlycA: Combined analysis of 14 exercise interventions, Atherosclerosis 2018, PMID 30170218 — meta_analysis — Tier 1); [5] Gruppen 2015 PREVEND and [5b] Julkunen UK Biobank; [6] Ritchie 2015 and [6b] the TwinsUK heritability study; [7] Lawler 2016; [8] Connelly 2017 J Transl Med and [8b] McGarrah smoking; [9] StatPearls acute-phase physiology and [9-review] Ballout review; [10] medRxiv preprint; [11] J Inflamm 2023 review. Each distinct paper is a distinct bibliography entry; the suffixed keys (3b, 4b, 5b, 6b, 8b, 9-review, 12, 13) disambiguate the merged set so no two different sources share one number.
