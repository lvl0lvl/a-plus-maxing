---
title: "LDL-C — LDL Cholesterol: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/ldl-c/research-report
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.ldl-c-design-work
provenance_slug: labs-specialist
source_count: 17
---

# LDL-C — LDL Cholesterol: Canonical Research Report

## Summary

LDL-C (low-density lipoprotein cholesterol) is the mass of cholesterol carried within circulating LDL particles, reported in mg/dL (US) or mmol/L (most of the world; the cholesterol conversion factor is 1 mmol/L ≈ 38.7 mg/dL, equivalently mg/dL ÷ 38.67 = mmol/L) [1, meta_analysis][11, mechanism_review]. It is not a measure of LDL particle *number* — it quantifies the cholesterol cargo, not the carriers. LDL-C is the primary lipid target of every major cardiovascular prevention guideline and the quantity against which lipid-lowering therapy is titrated.

The central finding of cardiovascular medicine over the past four decades is that LDL is not merely a marker but a *cause* of atherosclerotic cardiovascular disease (ASCVD). Three independent evidence streams — randomized statin trials, Mendelian randomization, and epidemiology — converge in direction and are roughly dose-consistent, and the European Atherosclerosis Society (EAS) Consensus Panel concluded that the combined evidence "unequivocally establishes that LDL causes ASCVD" [4, mechanism_review]. The Cholesterol Treatment Trialists' (CTT) meta-analysis of ~170,000 participants showed that each 1.0 mmol/L (≈38.7 mg/dL) reduction in LDL-C reduces major vascular events by 22% (RR 0.78, 95% CI 0.76–0.80) over ~5 years [1, meta_analysis], while Ference's Mendelian randomization of 312,321 participants showed that lifelong genetic exposure to lower LDL-C is associated with a 54.5% reduction in coronary heart disease per 1 mmol/L (95% CI 48.8%–59.5%) — roughly three-fold larger per unit, because the genetic effect integrates LDL exposure over a lifetime rather than ~5 years [3, meta_analysis].

This report synthesizes the identity and physiology of LDL-C, the causal evidence base, the modern risk-stratified reference ranges and units, the measurement methods and their validity limits, the genetic and acquired determinants of the level, and the clinical significance of LDL-C as the primary target alongside the ApoB/non-HDL-C discordance problem.

## Identity & Physiology

LDL particles are the cholesterol-delivery end of the lipoprotein cascade: very-low-density lipoprotein (VLDL) secreted by the liver is progressively delipidated to intermediate-density lipoprotein (IDL) and then to LDL, the principal carrier of cholesterol to peripheral tissues. Each LDL particle, like every atherogenic particle (LDL, VLDL, IDL, Lp(a)), carries exactly one apolipoprotein B (ApoB) molecule — the structural scaffold that solubilizes the lipid core [8, mechanism_review].

The key conceptual distinction is that **LDL-C measures cholesterol mass, not particle number**. ApoB measures the total *number* of atherogenic particles, whereas LDL-C measures the cholesterol *mass* those particles carry. Atherosclerosis tracks particle number more closely than summed cholesterol, because it is particles — not the cholesterol cargo per se — that breach the endothelium and seed plaque [8, mechanism_review]. Because particles vary in their cholesterol content (the small, dense, cholesterol-depleted LDL phenotype carries less cholesterol per particle), LDL-C can understate particle number; the two measures are discordant in a meaningful subset of people [8, mechanism_review].

Mechanistically, the causal pathway is that ApoB-containing particles small enough to cross the arterial endothelium become retained in the subendothelial space, are modified (notably oxidized), and trigger the inflammatory cascade that builds the atherosclerotic plaque. Because plaque accrues with cumulative exposure, the physiology is best understood not as a single threshold but as an integral over time — the "cholesterol-years" of exposure [7, mechanism_review].

## Causal Evidence

The EAS Consensus Panel concluded that "consistent evidence from numerous and multiple different types of clinical and genetic studies unequivocally establishes that LDL causes ASCVD" — i.e., LDL is a causal agent, not merely a risk marker [4, mechanism_review]. This conclusion rests on three converging evidence streams that agree in direction and are roughly dose-consistent.

### Randomized trial evidence — the per-1-mmol/L effect

The Cholesterol Treatment Trialists' (CTT) Collaboration pooled individual-participant data from 26 randomized trials (~170,000 participants) and found that each 1.0 mmol/L (≈38.7 mg/dL) reduction in LDL-C with a statin reduced major vascular events by 22% (RR 0.78, 95% CI 0.76–0.80) [1, meta_analysis]. The same per-1-mmol/L analysis showed:

- Major coronary events: RR 0.87 (95% CI 0.81–0.93) [1, meta_analysis]
- Coronary revascularization: RR 0.81 (95% CI 0.76–0.85) [1, meta_analysis]
- Ischaemic stroke: RR 0.86 (95% CI 0.77–0.96) [1, meta_analysis]
- All-cause mortality: RR 0.90 (95% CI 0.87–0.93) [1, meta_analysis]

The collaboration summarized the body of work by noting that "each 1 mmol/L reduction reduced the annual rate by just over 20%" [1, meta_analysis]. A subsequent CTT analysis of 27 trials (174,149 participants) extended the finding to people at *low* baseline risk, reporting a 21% reduction in major vascular events per 1 mmol/L (RR 0.79, 95% CI 0.77–0.81), with an absolute reduction of ~11 major vascular events per 1,000 over five years in participants whose five-year risk was below 10% [2, meta_analysis]. The EAS panel summarized this whole body of randomized evidence as a "22% proportional reduction in the risk of major cardiovascular events per millimole per litre reduction in LDL-C" over ~5 years of treatment [4, mechanism_review].

### Mendelian randomization — cumulative, lifetime exposure

Ference and colleagues used genetic variants that lower LDL-C from birth as a natural randomization, exploiting the fact that alleles are allocated at conception independently of confounders. In a meta-analysis of 312,321 participants (9 polymorphisms across 6 genes), naturally randomized lifelong exposure to lower LDL-C was associated with a 54.5% reduction in coronary heart disease risk per 1 mmol/L (95% CI 48.8%–59.5%) — roughly a 3-fold greater reduction per unit LDL-C than a statin started later in life (p = 8.43 × 10⁻¹⁹) [3, meta_analysis]. The EAS panel concurred that long-term exposure to lower LDL-C is associated with "up to a three-fold greater proportional reduction" in cardiovascular risk per unit LDL-C than short-term statin treatment [4, mechanism_review].

### The "lower is better / cumulative burden" model

The reconciling principle is that LDL's causal effect "is determined by both the absolute magnitude and the cumulative duration of exposure to LDL-C" [4, mechanism_review]. These findings define the prevailing model: ASCVD risk is driven by cumulative LDL exposure ("cholesterol-years"), the integral of LDL-C concentration over time, so both magnitude and duration matter [7, mechanism_review]. Because plaque accrues with cumulative exposure, maintaining low LDL-C over many years delays the age at which mature atherosclerotic plaques develop and substantially reduces lifetime ASCVD risk — a single mid-life LDL-C reading captures magnitude but not the accumulated burden [7, mechanism_review].

Critically, the short-term ~22% per-mmol/L statin effect [1, meta_analysis] and the ~54.5% per-mmol/L lifetime-genetic effect [3, meta_analysis] are *not* contradictory; they are the same causal relationship measured over ~5 years versus over decades. The implication of the cumulative-exposure hypothesis is that early, sustained, modest lowering can outperform later, aggressive lowering, because it reduces the area under the LDL-exposure curve for longer.

A further property of the randomized evidence reinforces the causal reading: the proportional benefit per 1 mmol/L is consistent across baseline risk strata. The 2010 CTT meta-analysis established the ~22% per-mmol/L effect in a population enriched for established disease and high baseline risk [1, meta_analysis], and the 2012 low-risk CTT analysis then demonstrated that the *same* proportional reduction (21%, RR 0.79, 95% CI 0.77–0.81) holds even when five-year risk is below 10% [2, meta_analysis]. Because the proportional effect is stable but the *absolute* benefit scales with baseline risk, the low-risk analysis reported a more modest absolute return of ~11 major vascular events avoided per 1,000 over five years [2, meta_analysis] — which is precisely why guidelines set risk-stratified goals rather than a single universal target: the same mmol/L of lowering buys more absolute risk reduction in a higher-risk person. The collaboration's own framing — that "each 1 mmol/L reduction reduced the annual rate by just over 20%" [1, meta_analysis] — captures the per-unit, dose-consistent nature of the relationship that the cumulative-exposure model integrates over time.

## Reference Ranges & Units

Modern lipid guidelines have abandoned a single population "normal" range for LDL-C. Instead they set goals that fall as cardiovascular risk rises, reflecting the "lower is better" model — there is no LDL-C threshold below which no further benefit accrues across the achievable range.

### Units and conversion

LDL-C is reported in **mg/dL** (US) or **mmol/L** (most of the world). The conversion for cholesterol is **mg/dL ÷ 38.67 = mmol/L** (equivalently × 0.02586) [11, mechanism_review]; Ference cites the rounded 38.7 mg/dL per mmol/L for the same factor [3, meta_analysis]. The ESC/EAS goals map as 55 mg/dL ≈ 1.4 mmol/L, 70 ≈ 1.8, 100 ≈ 2.6, 116 ≈ 3.0, and 40 ≈ 1.0 mmol/L [10, mechanism_review][11, mechanism_review].

### 2019 ESC/EAS risk-based treatment goals

The adopted LDL-C goals, by risk category, are [10, mechanism_review]:

- **Very-high risk: <55 mg/dL (<1.4 mmol/L)** *and* ≥50% reduction from baseline.
- **High risk: <70 mg/dL (<1.8 mmol/L)** *and* ≥50% reduction.
- **Moderate risk: <100 mg/dL (<2.6 mmol/L)**.
- **Low risk: <116 mg/dL (<3.0 mmol/L)** should be considered.
- **Recurrent event: <40 mg/dL (<1.0 mmol/L)** may be considered for patients with established ASCVD who suffer a second vascular event within 2 years (not necessarily of the same type) while on maximally tolerated statin therapy.

Risk-category definitions are explicit. Very-high risk includes documented ASCVD (clinical or imaging), diabetes with end-organ damage or three major risk factors, severe CKD (eGFR <30), heterozygous familial hypercholesterolemia (HeFH) with ASCVD or another major risk factor, or SCORE ≥10%. High risk includes a markedly elevated single risk factor (total cholesterol >310 mg/dL, LDL-C >190 mg/dL, or BP 180/110 mmHg), diabetes >10 years, moderate CKD (eGFR 30–59), or SCORE 5–9% [10, mechanism_review].

### 2018 AHA/ACC threshold triggers

Rather than fixed numeric targets, the 2018 AHA/ACC Multisociety blood cholesterol guideline uses LDL-C **thresholds to trigger added therapy**. In very-high-risk ASCVD, ezetimibe is reasonable when LDL-C remains **≥70 mg/dL** on maximally tolerated statin, and a PCSK9 inhibitor is reasonable if LDL-C stays **≥70 mg/dL** on statin plus ezetimibe [12, mechanism_review]. Severe primary hypercholesterolemia is defined as **LDL-C ≥190 mg/dL**: 10-year risk calculation is not required, maximally tolerated statin is recommended, and the aim is to reduce LDL-C **to <100 mg/dL** (a ≥50% reduction) [12, mechanism_review]. The US National Lipid Association (NLA) likewise treats LDL-C ≥190 mg/dL as a standalone high-risk trigger and endorses a <70 mg/dL goal for established ASCVD.

### NCEP ATP III descriptive bands

The earlier NCEP Adult Treatment Panel III (ATP III, NHLBI/NIH) bands remain the source of the "optimal / borderline / high" vocabulary still printed on lab reports. ATP III Table 2 classifies LDL-C (mg/dL) as: **<100 Optimal; 100–129 Near optimal/above optimal; 130–159 Borderline high; 160–189 High; ≥190 Very high** [13, regulatory]. The same table gives total cholesterol as **<200 Desirable, 200–239 Borderline high, ≥240 High**, and HDL as **<40 Low, ≥60 High** [13, regulatory]. These are *descriptive population bands*, not the risk-stratified treatment goals above, and should not be read as treatment targets for an at-risk individual.

## Measurement

LDL-C is most often *calculated*, not directly measured, and the calculation method matters because the error is largest exactly where clinical decisions are tightest (low LDL-C, high triglycerides).

### Friedewald

The default lab estimate is the Friedewald equation, **LDL-C = TC − HDL-C − TG/5** (mg/dL) [11, mechanism_review]. It assumes a fixed triglyceride-to-VLDL-cholesterol ratio of 5:1 [5, cohort]. It is **invalid when triglycerides exceed 400 mg/dL** and in non-fasting samples (the TG/5 term assumes a fixed fasting VLDL ratio), and it **systematically underestimates LDL-C at low values (<70 mg/dL)** [11, mechanism_review].

### Martin-Hopkins

The Martin-Hopkins method replaces the fixed factor of 5 with an **adjustable factor** selected from a 180-cell table stratified by triglyceride and non-HDL-C concentrations, with values ranging roughly 3 to 12 (cited as 3.1 to 11.9; median ratio 5.2, IQR 4.5–6.0) [5, cohort][11, mechanism_review]. Validated against 1,350,908 lipid profiles (derivation 900,605; validation 450,303), it raised overall concordance with the reference method to **91.7% vs 85.4% for Friedewald** (triglycerides <400 mg/dL); the gain was largest for classifying LDL-C <70 mg/dL at elevated triglycerides — e.g., **84.0% vs 40.3%** concordance at triglycerides 200–399 mg/dL [5, cohort]. It was recommended by the 2018 AHA/ACC guideline for reporting LDL-C **<70 mg/dL** [14, cohort].

### Sampson (NIH equation 2)

The Sampson/NIH equation is a fixed (non-adjustable) formula derived by beta-quantification, **LDL-C = TC/0.948 − HDL-C/0.971 − [TG/8.56 + (TG × non-HDL-C)/2140 − TG²/16100] − 9.44**, extending validity to triglycerides up to **800 mg/dL** [6, cohort][11, mechanism_review]. It outperformed both Friedewald and Martin-Hopkins at low LDL-C and high triglycerides, reporting a validation concordance correlation coefficient of **0.992** [6, cohort]. A head-to-head comparison across the full triglyceride range (111,939 patients) reported accuracy versus the reference method of **62.1% (Martin/Hopkins) vs 40.4% (Sampson) vs 19.3% (Friedewald)** — illustrating that the equations are not interchangeable and that performance depends on the population's triglyceride distribution [14, cohort].

### Direct measurement and fasting status

Direct enzymatic LDL-C assays and the reference **beta-quantification** (preparative ultracentrifugation) are used when triglycerides exceed 400 mg/dL or in non-fasting samples; beta-quantification is the gold standard but is expensive, time-consuming, and impractical for routine use [11, mechanism_review]. Friedewald requires a fasting sample; non-fasting lipid panels are increasingly accepted for screening, but a non-fasting triglyceride >400 mg/dL still mandates a direct LDL-C method, and **neither Martin-Hopkins nor Sampson is considered accurate enough to report LDL-C at triglycerides ≥400 mg/dL** [11, mechanism_review][14, cohort].

The practical takeaway is that calculated LDL-C carries equation-dependent error, and that error is not random — it is systematic and concentrated exactly where treatment decisions are tightest. Friedewald's underestimation at LDL-C <70 mg/dL [11, mechanism_review] is most consequential precisely because the very-high-risk ESC/EAS goal sits at <55 mg/dL [10, mechanism_review]: a Friedewald value can read "at goal" when the true LDL-C is higher, falsely reassuring both clinician and patient. The Martin-Hopkins gain is largest in exactly this regime — at triglycerides 200–399 mg/dL, concordance for the <70 mg/dL category rises from 40.3% (Friedewald) to 84.0% (Martin-Hopkins) [5, cohort] — which is why the 2018 AHA/ACC guideline specifically recommends Martin-Hopkins for reporting LDL-C below 70 mg/dL [14, cohort]. For longitudinal tracking against a fixed goal, the implication is that the *calculation method should be held constant* between panels: a switch from Friedewald to Martin-Hopkins or Sampson can move a reported LDL-C by several mg/dL with no real physiological change, so the method is a meaningful confounder when interpreting any value near a treatment threshold or a trend across panels.

## Determinants

### Genetics — familial hypercholesterolemia (FH)

FH arises from pathogenic variants in three principal genes: **LDLR** (the LDL receptor, ≥85% of cases, >1600 mutations described), **APOB** (defective apolipoprotein B that impairs LDL-receptor binding, commonly the position-3500 mutation), and **PCSK9** (gain-of-function variants that increase LDL-receptor degradation) [15, mechanism_review]. **Heterozygous FH (HeFH)** typically presents with untreated **LDL-C >190 mg/dL** and a prevalence of about **1 in 250**; **homozygous FH (HoFH)** presents with **LDL-C >450 mg/dL** and a prevalence of about **1 in 300,000**, reaching up to **1 in 100** in founder populations (French Canadians, Lebanese, Afrikaners) [15, mechanism_review].

### Diet

Saturated and trans fats and dietary cholesterol raise LDL-C; soluble fiber lowers it. A dose-response meta-analysis of **165 RCTs (199 arms, 12,773 participants)** found each **5 g/day** of soluble fiber lowered LDL-C by **−5.57 mg/dL (95% CI −7.44, −3.69)**, roughly **1.11 mg/dL per gram**, with an overall effect of **−8.28 mg/dL (95% CI −11.38, −5.18)** and an optimal **−10.75 mg/dL at 10 g/day (95% CI −12.66, −8.83)** [16, meta_analysis].

### Lifestyle and secondary conditions

Weight loss and exercise lower LDL-C modestly relative to the dietary and pharmacologic levers above; effect sizes vary widely and overlap with concurrent diet change (no single numeric threshold is adopted here). Reversible (secondary) causes of *elevated* LDL-C include **hypothyroidism** (reduced LDL clearance), **nephrotic syndrome**, **cholestasis**, pregnancy, and certain drugs (cyclosporine, thiazides) — all "excludable by history, physical examination, and laboratory tests" [15, mechanism_review].

### Pharmacotherapy — approximate % LDL-C lowering

- **Statins** lower LDL-C by **≥50%** at high intensity (atorvastatin 40–80 mg, rosuvastatin 20–40 mg) or **30–49%** at moderate intensity, with low-intensity <30% [12, mechanism_review].
- **Ezetimibe** adds roughly **15–20%** as add-on therapy (≈26–46% less reduction than a PCSK9 inhibitor) [17, meta_analysis].
- **PCSK9 monoclonal antibodies** (evolocumab, alirocumab) lower LDL-C by about **50–60%** versus placebo (evolocumab 420 mg monthly −54.6%; alirocumab −52.6%; real-world 12-month −58% to −62%) [17, meta_analysis].
- **Bempedoic acid** lowers LDL-C by about **15–25%** (−17.4% to −18.1% on maximal statin; −21.4% to −28.5% in statin-intolerant patients; pooled ≈−20.7%) [17, meta_analysis].
- **Inclisiran** (siRNA against PCSK9) lowers LDL-C by about **50%** (−51% from baseline vs placebo at 77 weeks; real-world ~−47% at 12 months) [17, meta_analysis].

The breadth of effective levers — from soluble fiber's single-digit mg/dL effect to PCSK9 inhibition's ~50–60% — is itself part of why LDL-C is the central modifiable lipid target: it is both causal and highly tractable.

## Clinical Significance

LDL-C is the **primary causal driver of ASCVD** and the central modifiable lipid target of every major prevention guideline. Because risk is driven by cumulative lifetime LDL burden, the clinical aim is not merely to cross a threshold but to lower and sustain the value over time, with the goal falling as baseline cardiovascular risk rises [4, mechanism_review][7, mechanism_review][10, mechanism_review].

### ApoB / non-HDL-C discordance

LDL-C remains the primary guideline target, but it has a known limitation: because each atherogenic particle carries exactly one ApoB, ApoB measures the total number of atherogenic particles, whereas LDL-C measures only cholesterol mass, and atherosclerosis tracks particle number more closely [8, mechanism_review]. When the two are *discordant* — which happens in a meaningful subset of people, particularly those with high triglycerides, diabetes, or the small-dense-LDL phenotype — LDL-C can under- or over-state the particle-driven risk that ApoB captures.

The magnitude is quantified in 293,876 UK Biobank adults (age 40–73, 42% male): ApoB and LDL-C correlated strongly (r = 0.96), yet at a fixed LDL-C of 130 mg/dL, ApoB spanned **85.8–108.8 mg/dL** across 95% of observations [9, cohort]. When discordant, ApoB was the better predictor: at LDL-C 130 ± 10 mg/dL, 10-year ASCVD rates were **7.3 vs 4.0 per 100** for high vs low ApoB, and residual ApoB remained significant after adjusting for LDL-C (HR 1.06), while residual LDL-C was *not* significant once ApoB was included [9, cohort]. The practical implication is that LDL-C is the right primary target for most people, but a measured ApoB resolves residual risk when LDL-C is "at goal," and the discordance is largest exactly in the metabolically high-risk phenotypes where it matters most.

## Bibliography

1. Cholesterol Treatment Trialists' (CTT) Collaboration. Efficacy and safety of more intensive lowering of LDL cholesterol: a meta-analysis of data from 170,000 participants in 26 randomised trials. The Lancet. 2010;376(9753):1670–1681. PMID 21067804 — DOI 10.1016/S0140-6736(10)61350-5 — meta_analysis — Tier 1
2. Cholesterol Treatment Trialists' (CTT) Collaborators. The effects of lowering LDL cholesterol with statin therapy in people at low risk of vascular disease: meta-analysis of individual data from 27 randomised trials. The Lancet. 2012;380(9841):581–590. PMID 22607822 — meta_analysis — Tier 1
3. Ference BA, Yoo W, Alesh I, et al. Effect of long-term exposure to lower low-density lipoprotein cholesterol beginning early in life on the risk of coronary heart disease: a Mendelian randomization analysis. J Am Coll Cardiol. 2012;60(25):2631–2639. PMID 23083789 — DOI 10.1016/j.jacc.2012.09.017 — meta_analysis — Tier 1
4. Ference BA, Ginsberg HN, Graham I, et al. (European Atherosclerosis Society Consensus Panel). Low-density lipoproteins cause atherosclerotic cardiovascular disease. 1. Evidence from genetic, epidemiologic, and clinical studies. A consensus statement. Eur Heart J. 2017;38(32):2459–2472. PMID 28444290 — DOI 10.1093/eurheartj/ehx144 — mechanism_review — Tier 1
5. Martin SS, Blaha MJ, Elshazly MB, et al. Comparison of a novel method vs the Friedewald equation for estimating low-density lipoprotein cholesterol levels from the standard lipid profile. JAMA. 2013;310(19):2061–2068. PMID 24240535 — DOI 10.1001/jama.2013.280532 — cohort — Tier 1
6. Sampson M, Ling C, Sun Q, et al. A new equation for calculation of low-density lipoprotein cholesterol in patients with normolipidemia and/or hypertriglyceridemia. JAMA Cardiol. 2020;5(5):540–548. PMID 32101259 — DOI 10.1001/jamacardio.2020.0013 — cohort — Tier 1
7. Ference BA, Braunwald E, Catapano AL. The LDL cumulative exposure hypothesis: evidence and practical applications. Nat Rev Cardiol. 2024;21(10):701–716. PMID 38969749 — DOI 10.1038/s41569-024-01039-5 — mechanism_review — Tier 1
8. Glavinovic T, Thanassoulis G, de Graaf J, Couture P, Hegele RA, Sniderman AD. Physiological bases for the superiority of apolipoprotein B over low-density lipoprotein cholesterol and non–high-density lipoprotein cholesterol as a marker of cardiovascular risk. J Am Heart Assoc. 2022;11(20):e025858. PMID 36216435 — DOI 10.1161/JAHA.122.025858 — mechanism_review — Tier 1
9. Sniderman AD, Dufresne L, Pencina KM, Bilgic S, Thanassoulis G, Pencina MJ. Discordance among apoB, non–high-density lipoprotein cholesterol, and triglycerides: implications for cardiovascular prevention. Eur Heart J. 2024;45(27):2410–2418. DOI 10.1093/eurheartj/ehae258 — cohort — Tier 1
10. 2019 ESC/EAS Guidelines for the Management of Dyslipidaemias (Mach F, et al.; ACC ten-points-to-remember summary). Eur Heart J. 2020;41(1):111–188. — mechanism_review (society guideline) — Tier 2.5
11. Low-Density Lipoprotein Cholesterol Gymnastics: Friedewald, Martin–Hopkins, and Sampson Equations (review). PMC11433184. — mechanism_review — Tier 1
12. 2018 AHA/ACC/Multisociety Guideline on the Management of Blood Cholesterol (Grundy SM, et al.; ACC summary). J Am Coll Cardiol. 2019;73(24):e285–e350. — mechanism_review (society guideline) — Tier 2.5
13. NCEP ATP III Executive Summary, Table 2 (NHLBI/NIH). JAMA. 2001;285(19):2486–2497. — regulatory (US government / NIH NHLBI) — Tier 2
14. Comparison of Martin/Hopkins, Sampson/NIH, and Friedewald Equations (111,939 patients). Am J Clin Pathol. 2024;162(Suppl_1):S168. — cohort — Tier 1
15. Ibrahim MA, Asuka E, Jialal I. Hypercholesterolemia. StatPearls (NCBI Bookshelf, NIH). NBK459188. — mechanism_review — Tier 1
16. Soluble Fiber Supplementation and Serum Lipid Profile: A Dose-Response Meta-Analysis of RCTs (165 RCTs, 12,773 participants). PMC10201678. — meta_analysis — Tier 1
17. Relative Efficacy of Alirocumab, Evolocumab, Inclisiran, and Bempedoic Acid on Lipids (network meta-analysis + supporting MAs). PMC12653900. — meta_analysis — Tier 1
