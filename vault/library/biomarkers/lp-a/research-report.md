---
title: "Lp(a) — Lipoprotein(a): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/lp-a/research-report
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.lp-a-design-work
provenance_slug: labs-specialist
source_count: 16
---

# Lp(a) — Lipoprotein(a): Canonical Research Report

## Summary

Lipoprotein(a) [Lp(a)] is a low-density-lipoprotein (LDL)-like particle in which a single molecule of apolipoprotein(a) [apo(a)] is covalently disulfide-linked to the apolipoprotein B-100 (apoB-100) of an LDL-like core. It is one of the most strongly genetically determined lipid traits in humans — the 2022 European Atherosclerosis Society (EAS) consensus concludes that Lp(a) concentration is "predominantly (>90%) determined by genetic variability at the *LPA* locus" [4, mechanism_review]. Across large prospective cohorts and Mendelian-randomization analyses, elevated Lp(a) is an **independent, causal** risk factor for atherosclerotic cardiovascular disease (ASCVD) and is the only identified modifiable causal risk factor for calcific aortic valve stenosis (AVS) [4, mechanism_review]. The risk relationship is continuous, with no biological "off" threshold, and persists after full adjustment for conventional lipids and risk factors [1, meta_analysis].

Two facts dominate clinical interpretation. First, Lp(a) is reported in two **non-interconvertible** unit systems — particle mass (mg/dL) and the molar concentration of apo(a) (nmol/L) — and a single conversion factor between them "is not appropriate" because apo(a) isoform size varies between individuals [4_B, cohort]. Second, because the plasma concentration is largely fixed at birth, a **single lifetime measurement** suffices for most adults [3_B, mechanism_review]. Lp(a) is largely refractory to diet, exercise, and statins (which may slightly *raise* it); meaningful pharmacologic lowering currently comes from PCSK9 inhibitors (~20–27%) and apheresis (~60–70% acute), with several investigational RNA therapeutics (pelacarsen, olpasiran, lepodisiran) achieving 72–95%+ reductions but none yet approved or shown to reduce cardiovascular outcomes [2_B, mechanism_review][7_B, meta_analysis].

This report merges the validated identity/physiology/causal evidence with the validated ranges/measurement/determinants material into a single canonical reference. It is goal-agnostic — written for any clinician or operator, not personalized.

## Identity & Physiology

### Particle identity

Lp(a) is distinguished from LDL by one extra protein component. Each Lp(a) particle consists of a single apoB-100-containing LDL-like core covalently bound to one molecule of apo(a) through a single disulfide bond [5, mechanism_review]. This covalent linkage is the defining structural feature: apo(a) wraps around the apoB-100 lipoprotein, and the resulting particle carries both the cholesterol-laden LDL moiety and the distinctive apo(a) glycoprotein. Because Lp(a) circulates at concentrations roughly an order of magnitude lower than LDL yet remains a potent risk factor, its excess atherogenicity is attributed to apo(a) and to cargo it carries (oxidized phospholipids), not to its cholesterol mass alone [7, cohort].

Apo(a) is an evolutionary descendant of plasminogen, arising from duplication of the plasminogen gene. It contains sequences highly similar to kringle IV (KIV) and kringle V (KV) of plasminogen plus an inactive protease domain [5, mechanism_review]. Apo(a) is built from ten distinct KIV subtypes (KIV-1 through KIV-10), a single KV domain, and the protease-like domain; nine of the ten KIV types are present in single copy, while KIV type 2 (KIV-2) is present in a variable number of identical repeats [5, mechanism_review]. The plasminogen homology of apo(a) underlies its hypothesized — but not firmly established — role in impaired fibrinolysis (see Mechanisms, below).

### Genetic determination — the *LPA* gene and the KIV-2 copy-number polymorphism

Plasma Lp(a) concentration is among the most strongly genetically determined of all lipid traits. The 2022 EAS consensus statement concludes that Lp(a) concentration is "predominantly (>90%) determined by genetic variability at the *LPA* locus," more than any other lipoprotein [4, mechanism_review]. The single largest genetic determinant is the KIV-2 copy-number variant: the KIV-2-encoding sequence exists in a variable number of identically repeated 5.6-kb copies ranging from 2 to more than 40, generating over 40 distinct apo(a) protein isoforms [5, mechanism_review]. The KIV-2 region alone comprises up to 70% of the *LPA* gene, and the KIV repeat polymorphism explains roughly 30–70% of the variability in plasma Lp(a) concentration [4, mechanism_review].

The relationship between KIV-2 copy number (isoform size) and plasma concentration is **inverse**: small apo(a) isoforms are associated with high concentrations, large isoforms with low concentrations. Median Lp(a) concentrations are 4 to 5 times higher in individuals carrying small apo(a) isoforms (<22 KIV repeats) than in those carrying only large isoforms (≥22 KIV repeats) [5, mechanism_review]. In the Copenhagen City Heart Study (CCHS), KIV-2 repeat number explained 21% of Lp(a) variation (27% in the Copenhagen General Population Study), with mean Lp(a) falling stepwise across ascending repeat-number quartiles — 56, 31, 20, and 15 mg/dL (trend P<.001) [6, cohort]. Heritability of plasma Lp(a) is high; isoform size accounts for 61–69% of variance in individuals of European descent and 19–44% in those of African descent, consistent with the commonly cited ~70–90% heritability figure [5, mechanism_review].

Two single-nucleotide polymorphisms at the *LPA* locus are widely used genetic instruments: rs10455872 and rs3798220. These explain approximately 25% and 8%, respectively, of the variation in plasma Lp(a) concentration [2, cohort]. Population distributions differ markedly by ancestry: in the Lp(a)HERITAGE study, Black individuals had median Lp(a) approximately 3-fold higher than White, Hispanic, or Asian individuals (125.8 vs 34.5–37.2 nmol/L) [5, mechanism_review]. In UK Biobank (440,368 European-ancestry participants), carrying one Lp(a)-raising minor allele (rs10455872 / rs3798220) gave a median Lp(a) of 146.3 nmol/L and two alleles 261.9 nmol/L, versus non-carriers [5_B, mechanism_review].

## Causal Evidence

The case that Lp(a) is causal — not merely associated — rests on the concordance of large observational cohorts with Mendelian-randomization (genetic) evidence. Because *LPA* genotype is fixed at conception and not confounded by lifestyle or reverse causation, agreement between genetic and observational effect sizes is the key causal signal.

### ASCVD — observational cohort evidence

The Emerging Risk Factors Collaboration pooled individual-participant data from 36 prospective studies (126,634 participants, 1.3 million person-years, 22,076 outcomes including 9,336 coronary heart disease [CHD] events and 1,903 ischemic strokes). Per 3.5-fold (≈1 SD) higher usual Lp(a), the risk ratio for CHD was **1.16 (95% CI 1.11–1.22)** adjusted for age and sex, and **1.13 (95% CI 1.09–1.18)** after full adjustment for lipids and conventional risk factors; the risk ratio for ischemic stroke was **1.10 (95% CI 1.02–1.18)**. Associations with nonvascular mortality were null (RR 1.01, 95% CI 0.98–1.05), indicating the relationship is specific to vascular outcomes [1, meta_analysis]. In the Copenhagen City Heart Study (9,330 participants, 498 incident MI over 10 years), extreme Lp(a) (≥120 mg/dL vs <5 mg/dL) carried a multivariable-adjusted hazard ratio for MI of **3.6 (95% CI 1.7–7.7)** in women and **3.7 (95% CI 1.7–8.0)** in men, with no threshold effect; absolute 10-year MI risk in high-risk men rose from 19% (<5 mg/dL) to 35% (≥120 mg/dL) [9, cohort].

### ASCVD — genetic (Mendelian randomization) evidence

Kamstrup et al. found that genetically elevated Lp(a) (instrumental-variable analysis using KIV-2 genotype) carried a hazard ratio for MI of **1.22 (95% CI 1.09–1.37)** per doubling, closely matching the observational estimate (1.08 per doubling) — "consistent with a causal association between elevated lipoprotein(a) levels and increased risk of MI" [6, cohort]. The PROCARDIS consortium identified rs10455872 (OR for coronary disease **1.70, 95% CI 1.49–1.95**) and rs3798220 (OR **1.92, 95% CI 1.48–2.49**); critically, adjustment for the Lp(a) level abolished the association between the *LPA* genotype score and coronary disease, "provid[ing] support for a causal role of Lp(a) lipoprotein in coronary disease" [2, cohort]. The EAS consensus summarizes the combined weight as: "Observational and genetic evidence convincingly demonstrates that high Lp(a) concentration is causal for ASCVD, AVS and cardiovascular and all-cause mortality in men and women and across ethnic groups" [4, mechanism_review].

### Calcific aortic valve stenosis (AVS)

Lp(a) is causally implicated in calcific AVS — the only modifiable causal risk factor identified for the condition. Kamstrup et al. reported, in two Danish general-population cohorts, multivariable-adjusted hazard ratios for AVS rising with Lp(a) percentile: **1.6 (95% CI 1.1–2.4)** for the 67th–89th percentile, **2.0 (95% CI 1.2–3.4)** for the 90th–95th, and **2.9 (95% CI 1.8–4.9)** for >95th percentile (>90 mg/dL) versus <22nd percentile; per 10-fold Lp(a) increase, the observational HR was **1.4 (95% CI 1.2–1.7)** and the genetic (instrumental-variable) relative risk **1.6 (95% CI 1.2–2.1)** [3, cohort]. The CHARGE GWAS independently found rs10455872 associated with aortic-valve calcium (OR per allele **2.05, P=9.0×10⁻¹⁰**), with incident clinical aortic stenosis (HR per allele **1.68, 95% CI 1.32–2.15**) and aortic-valve replacement (HR **1.54, 95% CI 1.05–2.27**), concluding the *LPA* association is "mediated by Lp(a) levels … across multiple ethnic groups" [8, cohort].

### Mechanisms

**Pro-atherogenic / cholesterol delivery.** As an apoB-100-containing, cholesterol-bearing particle, Lp(a) can deposit cholesterol in the arterial wall like LDL, but its disproportionate atherogenicity per particle points to apo(a)-specific and cargo-specific effects [5, mechanism_review].

**Oxidized-phospholipid (OxPL) carriage and inflammation.** Lp(a) is the major carrier of oxidized phospholipids in human plasma [5, mechanism_review]. In a controlled human study (30 subjects with elevated Lp(a), median 108 mg/dL, vs 30 with normal Lp(a), median 7 mg/dL), elevated Lp(a) was associated with increased arterial-wall inflammation on ¹⁸F-FDG PET/CT and enhanced monocyte trafficking; isolated monocytes showed greater transmigration and elevated pro-inflammatory cytokines (IL-1β, IL-6, TNFα). Inactivating the OxPL with the E06 antibody substantially attenuated the pro-inflammatory monocyte response — demonstrating that OxPL **mediates**, not merely accompanies, the inflammatory effect [7, cohort]. The *LPA* promoter additionally contains an interleukin-6 response element, so systemic inflammation transiently raises Lp(a) [5, mechanism_review].

**Pro-thrombotic / impaired fibrinolysis (proposed; evidence weight reported honestly).** Because apo(a) is a plasminogen homolog, it has long been hypothesized to impair fibrinolysis by competing with plasminogen (plasminogen mimicry). This mechanism remains mechanistically plausible but is not firmly established in vivo: a 2019 study found that lowering Lp(a) with antisense oligonucleotides produced no significant change in ex vivo clot-lysis time or coagulation/fibrinolysis biomarkers, arguing against a direct, clinically dominant antifibrinolytic effect [5, mechanism_review]. A platelet-related pathway has more support — in an ASPREE subanalysis, rs3798220 carriers derived greater benefit from aspirin, suggesting platelet involvement [5, mechanism_review]. The honest summary: the cholesterol-delivery and OxPL/inflammation mechanisms are well supported; the antifibrinolytic mechanism is biologically motivated by structure but its in-vivo contribution is contested.

## Reference Ranges & Units

There is no biological "off" threshold — the association between Lp(a) and ASCVD is continuous, causal, and present even at low LDL-C [5, mechanism_review]. Guidelines nonetheless define operating bands for decision-making.

### Risk thresholds and target bands

**European Atherosclerosis Society (EAS) 2022 consensus** grades [8_B, mechanism_review]:
- **Desirable / low concern:** < 30 mg/dL (≈ < 75 nmol/L).
- **Intermediate "grey zone":** 30–50 mg/dL (≈ 75–125 nmol/L) — interpret alongside other risk factors.
- **High / risk factor:** > 50 mg/dL (≈ > 125 nmol/L).

The continuous gradient under the same EAS document: relative to a median Lp(a) of 7 mg/dL, levels of 30, 50, 75–100, and 150 mg/dL carry roughly **1.22-, 1.40-, 1.65–1.95-, and 2.72-fold** increases in ASCVD risk [8_B, mechanism_review].

**National Lipid Association (NLA)** uses a slightly different molar cut: an Lp(a) **≥ 50 mg/dL or ≥ 100 nmol/L** is a risk-enhancing factor favouring statin initiation; this level corresponds to roughly the 80th population percentile in predominantly Caucasian populations [1_B, mechanism_review]. The NLA's use of 100 nmol/L versus the EAS's 125 nmol/L at the same 50 mg/dL mass cut is itself a direct illustration of the units problem — guideline bodies do not agree on a single molar equivalent of 50 mg/dL [1_B, mechanism_review][8_B, mechanism_review].

**Extreme / genetic very-high tier:** Lp(a) **> 180 mg/dL (> 430 nmol/L)** is "extremely elevated," conferring a lifetime ASCVD risk comparable to heterozygous familial hypercholesterolaemia (heFH); the Copenhagen General Population Study placed the Lp(a) level equivalent to genetic-FH LDL-C for myocardial infarction at **180 mg/dL (389 nmol/L)** [8_B, cohort]. **Caveat on a common figure:** this heFH-equivalent tier is anchored at ~180 *mg/dL* (~430 nmol/L), not 180 *nmol/L*; a value of 180 nmol/L sits in the high-but-not-extreme band. HEART UK separately flags very-high *inherited* Lp(a) for cascade screening at **> 200 nmol/L** [3_B, mechanism_review].

### Units: the mass-vs-molar problem

Lp(a) is reported either as particle **mass (mg/dL)** or as the **molar concentration of apo(a) (nmol/L)**, the latter considered the gold standard [4_B, cohort]. The two are **not linearly interconvertible**, because apo(a) isoform size varies between people (driven by the number of KIV-2 repeats), so a given mass of Lp(a) corresponds to a variable number of particles. Empirically, measured nmol/L : mg/dL ratios range from **< 1 to > 5** across assays and, critically, **rise with concentration** — for one reference pairing the ratio was ~1.82 below 75 nmol/L but ~2.80 above 125 nmol/L [4_B, cohort]. The authors conclude a single conversion factor "is not appropriate" [4_B, cohort]. The EAS therefore declines to endorse a fixed factor, offering only a discouraged "best guess" of ~2–2.5 (mg/dL → nmol/L) and stating that molar measurement is the preferred clinical standard [8_B, mechanism_review]. **Practical consequence:** the parenthetical nmol/L values beside mg/dL thresholds above are approximate alignments adopted by the guidelines, not arithmetic conversions, and an individual patient's two readings should never be derived from one another.

## Measurement

The core analytical problem is **apo(a) size heterogeneity**. Mass-based immunoassays that detect the repeating KIV-2 epitope **overestimate larger isoforms and underestimate smaller ones** — and smaller isoforms are precisely those most strongly associated with elevated Lp(a) and higher cardiovascular risk [2_B, mechanism_review; corroborated 1_B, mechanism_review]. nmol/L assays count apo(a) particle number using antibodies directed at non-repeating epitopes, making them **isoform-insensitive**; methods reporting mg/dL "are sensitive to the size of the apo(a) isoform and may report values that deviate from the real concentration" [3_B, mechanism_review]. The field's standardisation target is reporting in **nmol/L traceable to the WHO/IFCC reference reagent (SRM 2B)**, which reduces size-related bias [1_B, mechanism_review][3_B, mechanism_review]. The NLA notes that, as of its statement, measurement was still "not standardized or harmonized" [1_B, mechanism_review].

**When to measure:** because Lp(a) is genetically stable across the lifespan, a **single lifetime measurement** suffices for most adults. The Canadian Cardiovascular Society recommends testing "once in a person's lifetime as part of initial lipid screening"; ESC/EAS frame a one-off measurement as a way to identify people with very high inherited Lp(a) and substantial lifetime risk [3_B, mechanism_review]. Testing is reasonable particularly in those with premature ASCVD, family history of premature ASCVD or raised Lp(a), suspected/diagnosed familial hypercholesterolaemia, and people of **South Asian or African ancestry** [3_B, mechanism_review]. Repeat testing is warranted mainly to confirm an extreme value, or after an intervention expected to change Lp(a).

## Determinants

**Genetics dominate (~80–90%).** Around 90% of an individual's Lp(a) concentration is genetically determined, governed by the *LPA* locus; nearly 70% of the Lp(a) coding sequence lies in the KIV-2 copy-number-variable region, which yields ~40 apo(a) allelic isoforms [2_B, mechanism_review]. The number of KIV-2 repeats is **inversely** related to plasma Lp(a) (fewer repeats → smaller isoform → higher levels) [2_B, mechanism_review].

**Ancestry:** mean Lp(a) is **higher in people of African and South Asian descent** and **lower in East Asian populations** [2_B, mechanism_review][3_B, mechanism_review]. (Population annotation: most threshold percentiles derive from predominantly Caucasian cohorts — e.g. the NLA's 80th-percentile anchor [1_B, mechanism_review] — so cut-points are not fully validated across ancestries.)

**Modifiers that raise Lp(a):** menopause, hypothyroidism, and renal/nephrotic disease are recognised secondary elevators (guideline-level) [1_B, mechanism_review]. Notably, **statins do not lower Lp(a) and may slightly raise it** — a paradoxical increase of roughly **10.6–19.3%** has been reported, attributed to LDL-receptor upregulation [2_B, mechanism_review].

**Interventions that lower Lp(a) (approximate effects):**
- **Diet / exercise / weight loss:** minimal effect — Lp(a) is largely refractory to lifestyle, consistent with its genetic fixity [2_B, mechanism_review].
- **PCSK9 inhibitors (evolocumab, alirocumab):** ~**20–25%** reduction in reviews [2_B, mechanism_review]; outcomes-trial analyses give a median **27%** (evolocumab, FOURIER) and **~23%** (alirocumab, ODYSSEY OUTCOMES), with a meta-analytic alirocumab estimate of **24.5% (95% CI −27.96 to −21.04)** [7_B, meta_analysis].
- **Niacin:** lowers Lp(a) but is **not recommended** — no demonstrated ASCVD benefit and a suggestion of harm [1_B, mechanism_review].
- **Lipoprotein apheresis:** acute reductions of **~60–70%** per session, with mean interval (time-averaged) concentration reduced ~25–40% [2_B, mechanism_review].
- **Emerging RNA therapeutics (trial-stage, not approved):**
  - **Pelacarsen** (antisense oligonucleotide): phase 2 reduced Lp(a) by **72%** (60 mg monthly) and **80%** (20 mg weekly); 98% of the weekly cohort reached < 50 mg/dL. Phase 3 outcomes trial (Lp(a)HORIZON) ongoing [7_B, rct].
  - **Olpasiran** (siRNA): phase 2 OCEAN(a)-DOSE — doses ≥ 75 mg every 12 weeks cut Lp(a) by **> 95%** at week 36 (placebo-adjusted **97.4%** at 75 mg Q12W). Phase 3 OCEAN(a)-Outcomes ongoing [7_B, rct].
  - **Lepodisiran** (long-duration siRNA): phase 2 ALPACA — single 400 mg dose reduced Lp(a) by a mean **93.9%** over days 60–180; phase 3 (ACCLAIM-Lp(a)) enrolling [6_B, rct].

These agents are investigational; **none is approved**, and no Lp(a)-lowering drug has yet demonstrated cardiovascular-outcome benefit — the phase 3 outcomes trials above are designed to answer that question.

## Clinical Significance

Lp(a) is a once-in-a-lifetime genetic measure with outsized prognostic weight. Roughly 20–25% of the global population carries clinically meaningful elevation, and because the trait is set at conception, a single measurement reclassifies lifetime ASCVD and aortic-stenosis risk for the individual and — through cascade screening — for first-degree relatives. The risk it confers is **independent of and additive to** LDL-C and apoB: full adjustment for conventional lipids does not abolish the association [1, meta_analysis], so a patient at goal LDL-C can still carry substantial residual Lp(a)-mediated risk. This is why guideline bodies (EAS 2022, NLA, ESC, Canadian Cardiovascular Society, HEART UK) converge on universal or near-universal one-time screening, even though no Lp(a)-targeted therapy has yet proven outcome benefit.

For decision-making, the practical reading is: a value below ~30 mg/dL (~75 nmol/L) is reassuring; the 30–50 mg/dL (75–125 nmol/L) grey zone should be integrated with global risk; above 50 mg/dL (>125 nmol/L) Lp(a) is itself a risk-enhancing factor that justifies more aggressive management of every *modifiable* co-risk (LDL-C, blood pressure, smoking); and >180 mg/dL (>430 nmol/L) marks an heFH-equivalent lifetime burden warranting specialist attention and family screening. Until outcome trials read out, management is intensification of conventional risk-factor control plus, in the highest-risk refractory cases, apheresis — with RNA therapeutics held as investigational. Throughout, the unit a result is reported in (mg/dL vs nmol/L) and the assay's traceability to the WHO/IFCC SRM 2B reference must be checked, because a single conversion factor between the two systems is not valid for an individual.

## Bibliography

[1]. Erqou S, Kaptoge S, Perry PL, et al. (Emerging Risk Factors Collaboration). Lipoprotein(a) concentration and the risk of coronary heart disease, stroke, and nonvascular mortality. JAMA. 2009;302(4):412-423. PMID: 19622820. DOI: 10.1001/jama.2009.1063. — tag: meta_analysis — tier: 1

[2]. Clarke R, Peden JF, Hopewell JC, et al. (PROCARDIS Consortium). Genetic variants associated with Lp(a) lipoprotein level and coronary disease. N Engl J Med. 2009;361(26):2518-2528. PMID: 20032323. DOI: 10.1056/NEJMoa0902604. — tag: cohort — tier: 1

[3]. Kamstrup PR, Tybjaerg-Hansen A, Nordestgaard BG. Elevated lipoprotein(a) and risk of aortic valve stenosis in the general population. J Am Coll Cardiol. 2014;63(5):470-477. PMID: 24161338. DOI: 10.1016/j.jacc.2013.09.038. — tag: cohort — tier: 1

[4]. Kronenberg F, Mora S, Stroes ESG, et al. Lipoprotein(a) in atherosclerotic cardiovascular disease and aortic stenosis: a European Atherosclerosis Society consensus statement. Eur Heart J. 2022;43(39):3925-3946. PMID: 36036785. DOI: 10.1093/eurheartj/ehac361. — tag: mechanism_review — tier: 1  *(shared identity/causal source [4] and ranges source [5_B]; single merged entry)*

[5]. Volgman AS, Koschinsky ML, Mehta A, Rosenson RS. Genetics and Pathophysiological Mechanisms of Lipoprotein(a)-Associated Cardiovascular Risk. J Am Heart Assoc. 2024;13(12):e033654. PMID: 38879448. DOI: 10.1161/JAHA.123.033654. — tag: mechanism_review — tier: 1

[6]. Kamstrup PR, Tybjaerg-Hansen A, Steffensen R, Nordestgaard BG. Genetically elevated lipoprotein(a) and increased risk of myocardial infarction. JAMA. 2009;301(22):2331-2339. PMID: 19509380. DOI: 10.1001/jama.2009.801. — tag: cohort — tier: 1

[7]. van der Valk FM, Bekkering S, Kroon J, et al. (incl. Koschinsky, Witztum, Tsimikas, Stroes). Oxidized Phospholipids on Lipoprotein(a) Elicit Arterial Wall Inflammation and an Inflammatory Monocyte Response in Humans. Circulation. 2016;134(8):611-624. PMID: 27496857. DOI: 10.1161/CIRCULATIONAHA.116.020838. — tag: cohort — tier: 1

[8]. Thanassoulis G, Campbell CY, Owens DS, et al. (CHARGE Extracoronary Calcium Working Group). Genetic associations with valvular calcification and aortic stenosis. N Engl J Med. 2013;368(6):503-512. PMID: 23388002. DOI: 10.1056/NEJMoa1109034. — tag: cohort — tier: 1

[9]. Kamstrup PR, Benn M, Tybjaerg-Hansen A, Nordestgaard BG. Extreme lipoprotein(a) levels and risk of myocardial infarction in the general population: the Copenhagen City Heart Study. Circulation. 2008;117(2):176-184. PMID: 18086931. DOI: 10.1161/CIRCULATIONAHA.107.715698. — tag: cohort — tier: 1

[1_B]. Koschinsky ML, et al. Use of Lipoprotein(a) in clinical practice: a biomarker whose time has come. A scientific statement from the National Lipid Association. J Clin Lipidol. 2024. https://www.lipidjournal.com/article/S1933-2874(22)00244-6/fulltext — tag: mechanism_review — tier: 1

[2_B]. Lipoprotein(a): Underrecognized Risk with a Promising Future. PMC11607505. 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11607505/ — tag: mechanism_review — tier: 1 (NIH-hosted)

[3_B]. Lipoprotein(a): an important piece of the ASCVD risk factor puzzle across diverse populations. PMC10945898. https://pmc.ncbi.nlm.nih.gov/articles/PMC10945898/ — tag: mechanism_review — tier: 1 (NIH-hosted)

[4_B]. Marcovina SM, et al. Relationship of lipoprotein(a) molar concentrations and mass according to lipoprotein(a) thresholds and apolipoprotein(a) isoform size. J Clin Lipidol. 2018. PMID: 30100157. https://pubmed.ncbi.nlm.nih.gov/30100157/ — tag: cohort — tier: 1

[5_B]. (See [4].) Kronenberg F, Mora S, Stroes ESG, et al. EAS consensus statement. Eur Heart J. 2022;43(39):3925-3946. PMID: 36036785. — tag: mechanism_review — tier: 1 — *duplicate of [4]; cited inline as [5_B] for ranges/determinants claims; deduplicated to [4] in the source count.*

[6_B]. Nissen SE, et al. Lepodisiran — a long-duration small interfering RNA targeting lipoprotein(a) (ALPACA, phase 2). N Engl J Med. 2025. DOI: 10.1056/NEJMoa2415818. — tag: rct — tier: 1

[7_B]. Tsimikas S, et al. Lipoprotein(a) reduction in persons with cardiovascular disease (pelacarsen, phase 2). N Engl J Med. 2020;382:244-255. DOI: 10.1056/NEJMoa1905239. + O'Donoghue ML, et al. Small interfering RNA to reduce lipoprotein(a) in cardiovascular disease (olpasiran, OCEAN(a)-DOSE, phase 2). N Engl J Med. 2022;387:1855-1864. DOI: 10.1056/NEJMoa2211023. + PCSK9i Lp(a) outcomes analyses (FOURIER, ODYSSEY OUTCOMES). — tag: rct / meta_analysis — tier: 1

[8_B]. EAS 2022 risk-grade table + EAS FAQ (Atherosclerosis 2023, PMID 37188555) + extreme-tier (Copenhagen General Population Study / ESC 2023 framing), via ACC Update on Lp(a) (acc.org 2023). https://www.acc.org/Latest-in-Cardiology/Articles/2023/09/19/10/54/An-Update-on-Lipoprotein-a — tag: mechanism_review — tier: 1

**Distinct source count: 16** (Section-A refs [1]–[9] = 9; Section-B refs [1_B]–[8_B] = 8; the EAS 2022 consensus is shared between [4] and [5_B], so [5_B] is not counted separately → 9 + 8 − 1 = 16). The `_B` suffix preserves the original section-B numbering for traceability while keeping the merged list unambiguous.
