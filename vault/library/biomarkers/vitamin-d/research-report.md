---
title: "25-Hydroxyvitamin D (Vitamin D Status): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/vitamin-d/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.vitamin-d-design-work
provenance_slug: labs-specialist
source_count: 33
---

# 25-Hydroxyvitamin D (Vitamin D Status): Canonical Research Report

## Summary

Serum 25-hydroxyvitamin D [25(OH)D] is the correct clinical test for vitamin D status. It is not the active vitamin D hormone — that is 1,25-dihydroxyvitamin D [1,25(OH)₂D / calcitriol] — but rather the intermediate metabolite produced by largely unregulated hepatic 25-hydroxylation. Because this first hydroxylation tracks substrate availability rather than downstream hormonal demand, 25(OH)D faithfully reflects the integrated input from cutaneous photosynthesis, dietary intake, and supplementation, accumulated across weeks. 1,25(OH)₂D, by contrast, has a 4–6-hour half-life and is homeostatically defended: in early vitamin D deficiency, rising parathyroid hormone (PTH) compensatorily upregulates renal 1α-hydroxylase, so 1,25(OH)₂D can be normal or elevated even as body stores are depleted. This regulatory asymmetry is the fundamental reason 25(OH)D is the status marker and 1,25(OH)₂D is not.

Vitamin D is reported in ng/mL in the United States (SI: nmol/L; conversion: 1 ng/mL × 2.496 = nmol/L). The most consequential interpretive issue is the threshold debate. In 2011, two authoritative bodies reviewed overlapping evidence and reached different conclusions. The Institute of Medicine (IOM) set ≥20 ng/mL (50 nmol/L) as adequate for bone health across 97.5% of the population — a public-health floor. The Endocrine Society set ≥30 ng/mL (75 nmol/L) as the individual optimization target, citing PTH-plateau data and calcium-absorption studies. Neither conclusion is incorrect on its own terms; they answer different questions about different populations. In 2024, the Endocrine Society substantially revised its position (Demay et al., JCEM 2024): it no longer endorses the 30 ng/mL target in healthy adults, recommends against routine screening, and shifts toward empiric supplementation for four evidence-supported groups. The 2011 cutoffs remain embedded in laboratory reference ranges globally, creating a situation where a result of 22 ng/mL is simultaneously "normal" and "insufficient" depending on which guideline the reporting lab follows.

A further complication is assay-standardization. Different laboratory platforms have historically reported 25(OH)D values that differed by 10–40% for the same sample. The Vitamin D Standardization Program (VDSP), coordinated by NIH, NIST, and CDC with the NIST Standard Reference Material 972a as anchor calibrator, has substantially reduced inter-assay bias for LC-MS/MS platforms. Immunoassays remain more variable. This assay imprecision spans the same 10 ng/mL gap separating the IOM and Endocrine Society cutoffs, meaning the threshold debate and the measurement-error debate are intertwined.

For clinical significance, the evidence is asymmetric. The deficiency syndromes — rickets in children, osteomalacia in adults, secondary hyperparathyroidism in the deficient elderly — have unambiguous causal vitamin D etiology responding to repletion, supported by a century of clinical and experimental evidence. In contrast, the observational literature associating low 25(OH)D with cardiovascular disease, cancer, diabetes, and mortality has been tested in large, well-powered RCTs and found largely unconfirmed: VITAL (N = 25,871, 2,000 IU/day D3, 5.3 years), D-Health (monthly 60,000 IU D3), and ViDA (monthly high-dose D3) showed no reduction in their primary endpoints of cancer incidence, CVD events, or all-cause mortality in predominantly replete populations. The most credible non-bone signal is the VITAL autoimmune ancillary analysis (Hahn et al., BMJ 2022), showing 22% reduction in confirmed autoimmune disease (HR 0.78; 95% CI 0.61–0.99), though with a borderline P-value. The honest framing: 25(OH)D is a status marker, not a proven causal lever for most non-bone outcomes. Correct documented deficiency for bone and falls risk; do not chase a high-normal number for cardiovascular or cancer prevention.

---

## Physiology & What 25(OH)D Measures

### Vitamin D Is a Secosteroid Prohormone, Not a Classic Vitamin

Vitamin D occupies an unusual conceptual position in clinical biochemistry: it is formally classified as a fat-soluble vitamin yet functions biologically as a **secosteroid prohormone**. A secosteroid is a steroid in which one ring has been cleaved — in vitamin D's case, the B-ring of the steroid backbone opens under ultraviolet irradiation, distinguishing it from classical steroids such as cortisol or estradiol [1, mechanism_review]. The label "vitamin" is largely historical: under conditions of adequate sunlight exposure, the body synthesizes sufficient vitamin D through cutaneous photoproduction without any dietary requirement. Only when sun exposure is inadequate does it become a conditionally dietary nutrient. Vitamin D's final bioactive form, 1,25-dihydroxyvitamin D [1,25(OH)₂D / calcitriol], acts through a nuclear receptor to regulate gene transcription — a mechanism shared with steroid hormones, not classic vitamins [1, mechanism_review; 2, mechanism_review].

### Two Sources: Cutaneous Synthesis and Diet

**Cutaneous photosynthesis** is the dominant physiological source. When UVB radiation (wavelength approximately 290–320 nm) penetrates uncovered skin, it photolytically cleaves the B-ring of **7-dehydrocholesterol** (7-DHC, a cholesterol precursor concentrated in the epidermis and dermis) to form **previtamin D3**. Previtamin D3 is thermally unstable; it undergoes spontaneous, non-enzymatic isomerization over hours to **cholecalciferol (vitamin D3)** driven by body temperature. Cholecalciferol then enters the circulation bound to vitamin D binding protein (DBP) for transport to the liver [2, mechanism_review; 3, mechanism_review]. Several factors limit cutaneous synthesis: solar zenith angle (above ~35° latitude in winter, UVB is absorbed by atmospheric ozone), skin pigmentation (melanin competes with 7-DHC for UVB photons), clothing, sunscreen, aging (older skin has lower 7-DHC concentration), and obesity (fat-soluble vitamin D sequesters in adipose tissue) [3, mechanism_review].

**Dietary and supplemental sources** provide two chemically distinct forms. **Vitamin D3 (cholecalciferol)** is found in fatty fish, fish liver oils, egg yolks, and UV-irradiated animal-source foods; most vitamin D3 supplements are derived from lanolin (sheep wool fat) or lichen. **Vitamin D2 (ergocalciferol)** is plant- and fungal-derived (UV-irradiated yeast, mushrooms, some plant-based supplements). Both D2 and D3 are absorbed in the small intestine via chylomicrons and enter the lymph before reaching the systemic circulation [1, mechanism_review].

### Two Activating Hydroxylations: Liver Then Kidney

Dietary and cutaneous vitamin D is biologically inert and must undergo sequential enzymatic activation.

**First hydroxylation — hepatic (liver) → 25(OH)D:** Vitamin D3 or D2 travels to the liver, where it undergoes 25-hydroxylation to form **25-hydroxyvitamin D [25(OH)D]** — also called calcifediol or calcidiol. The primary enzyme responsible is **CYP2R1** (a microsomal cytochrome P450), which 25-hydroxylates both D3 and D2 with comparable kinetics [4, mechanism_review]. CYP27A1 (a mitochondrial enzyme) contributes minor additional 25-hydroxylase activity. Genetic polymorphisms in CYP2R1 account for a portion of inter-individual variation in circulating 25(OH)D concentrations. This hepatic step is **largely substrate-driven and not tightly regulated** by feedback — which is precisely why 25(OH)D faithfully reflects vitamin D input from all sources (sun + diet + supplements) and accumulation in body stores [5, mechanism_review].

**Second hydroxylation — renal (kidney) → 1,25(OH)₂D:** In the proximal renal tubule, 25(OH)D is converted to **1,25-dihydroxyvitamin D [1,25(OH)₂D / calcitriol]** by **1α-hydroxylase (CYP27B1)**. Calcitriol is the hormonally active form that binds the vitamin D receptor (VDR) with high affinity to drive genomic effects. Unlike hepatic 25-hydroxylation, renal CYP27B1 activity is **tightly regulated** by a trio of hormonal signals [5, mechanism_review; 6, mechanism_review]:

- **PTH (parathyroid hormone) — upregulates CYP27B1**, increasing 1,25(OH)₂D production when serum calcium falls
- **FGF23 (fibroblast growth factor 23, secreted by osteocytes) — downregulates CYP27B1** and simultaneously upregulates **CYP24A1 (24-hydroxylase)**, which catabolizes 1,25(OH)₂D to inactive products; FGF23 thus acts as the brake when 1,25(OH)₂D rises [6, mechanism_review]
- **Calcium and phosphate levels** — provide direct substrate-level feedback

### Why 25(OH)D Is the Clinical Status Test — and Why 1,25(OH)₂D Is Not

This is the most clinically load-bearing concept in interpreting vitamin D laboratory results.

**25(OH)D as the status biomarker:**
- **Integrates all sources**: reflects sun exposure + dietary intake + supplementation, accumulated over weeks [5, mechanism_review]
- **Long circulating half-life**: approximately **2–3 weeks** for 25(OH)D3 (the D2 form, 25(OH)D2, has a somewhat shorter half-life owing to lower DBP affinity) [1, mechanism_review; 4, mechanism_review]
- **High serum concentration**: orders of magnitude above 1,25(OH)₂D, making it technically easier to measure accurately [4, mechanism_review]
- **Unregulated hepatic step**: hepatic 25-hydroxylation tracks substrate availability (vitamin D input) rather than downstream demand, so 25(OH)D rises and falls with true body stores

**Why 1,25(OH)₂D fails as a status test:**
- **Short half-life**: approximately **4–6 hours** [5, mechanism_review; 7, mechanism_review]
- **Homeostatically defended**: renal CYP27B1 is tightly regulated; in early vitamin D deficiency, rising PTH drives compensatory upregulation of CYP27B1 — so 1,25(OH)₂D concentrations can be **normal or even elevated** even as body stores (25(OH)D) are depleted [7, mechanism_review]
- **Consequence**: measuring 1,25(OH)₂D to assess nutritional vitamin D status will systematically miss deficiency in the population most at risk

**Clinical rule**: Reserve 1,25(OH)₂D testing for specific diagnostic questions — chronic kidney disease (where CYP27B1 is lost), granulomatous disease (sarcoidosis, TB — ectopic CYP27B1 in macrophages causes hypercalcemia), or hereditary forms of rickets (CYP27B1 loss-of-function; VDR mutations) [2, mechanism_review].

### Vitamin D Receptor and Classical Functions

Both 25(OH)D and 1,25(OH)₂D exert effects via the **vitamin D receptor (VDR)**, a nuclear receptor and transcription factor, though 1,25(OH)₂D binds the VDR with approximately 1,000-fold higher affinity. The VDR heterodimerizes with the retinoid X receptor (RXR) and binds vitamin D response elements (VDREs) in gene promoters, regulating expression of hundreds of target genes [3, mechanism_review].

**Classical skeletal/mineral functions:**
- Enhanced intestinal absorption of **calcium and phosphate** (via TRPV6 and other channels)
- Regulation of bone mineralization in concert with PTH
- Renal calcium reabsorption in the distal tubule

**Non-classical/pleiotropic functions** reflect the broad tissue distribution of VDR — it is expressed in immune cells (T-cells, B-cells, macrophages), muscle, pancreatic beta-cells, cardiovascular tissue, and many others. Macrophages express CYP27B1, enabling autocrine production of calcitriol for immune modulation (cathelicidin upregulation, innate defense) [3, mechanism_review]. These non-skeletal VDR actions motivate much of the population-level epidemiology linking low 25(OH)D to immune, cardiometabolic, and neuromuscular outcomes — though mechanistic causation in humans remains contested for most endpoints beyond bone.

### Transport: DBP and the Free Hormone Concept

In circulation, 25(OH)D is almost entirely protein-bound:
- **~88% bound to vitamin D binding protein (DBP)**, a high-affinity globulin (dissociation constant ~10⁻⁸ mol/L for 25(OH)D)
- **~12–15% bound to albumin** (lower affinity, higher concentration)
- **~0.03% free (unbound)** in serum from non-pregnant individuals [8, mechanism_review; 9, mechanism_review]

The **free hormone hypothesis** posits that only unbound 25(OH)D crosses cell membranes by passive diffusion, making the free fraction the biologically active pool for most tissues. A notable exception is the kidney proximal tubule, where the DBP–25(OH)D complex filtered at the glomerulus is endocytosed intact via **megalin/cubilin** receptors, enabling tubular cells to access protein-bound vitamin D for local 1,25(OH)₂D synthesis [9, mechanism_review].

Clinical relevance: conditions altering DBP levels (hepatic failure reduces DBP synthesis; pregnancy increases it; nephrotic syndrome causes urinary DBP loss) can dissociate total 25(OH)D from free 25(OH)D. Whether measuring free 25(OH)D provides clinical advantage over total 25(OH)D for most outcomes remains an active research question; for routine vitamin D status assessment, **total serum 25(OH)D is the standard** [8, mechanism_review].

### Vitamin D2 vs. D3: Assay and Clinical Distinctions

The standard clinical test reports **total 25(OH)D** = 25(OH)D3 + 25(OH)D2 combined, in **ng/mL** (SI: nmol/L; conversion: 1 ng/mL × 2.496 = nmol/L).

Key D2/D3 differences with practical implications:

1. **Potency**: D3 raises total serum 25(OH)D to a greater extent and sustains it longer than equimolar D2 doses, particularly with less-frequent dosing regimens. This reflects D3's higher DBP affinity and longer 25(OH)D3 half-life vs. 25(OH)D2 [1, mechanism_review; 10, rct].

2. **Assay cross-reactivity**: Older immunoassays (RIA, some automated platforms) show variable cross-reactivity for 25(OH)D2 — some underestimate it by 25–31% relative to 25(OH)D3. LC-MS/MS is the analytical gold standard and measures D2 and D3 metabolites separately with equivalent accuracy [7, mechanism_review].

3. **Source**: D2 is the form in most prescription vitamin D preparations (50,000 IU capsules in many markets) and plant-based/vegan supplements; D3 dominates OTC supplements derived from lanolin. Patients on D2 prescriptions may show lower total 25(OH)D response than expected from D3-based dose tables.

---

## Reference Ranges, Units & The Threshold Debate

### Units and Conversion

Serum 25(OH)D is reported in two unit systems depending on geography and laboratory convention. In the United States, ng/mL (nanograms per milliliter) is standard. In most other countries and in SI-based literature, nmol/L (nanomoles per liter) is used. The conversion factor is **×2.496**: multiply ng/mL by 2.496 to get nmol/L, or divide nmol/L by 2.496 to get ng/mL.

Key landmark conversions:
- 12 ng/mL ≈ 30 nmol/L
- 20 ng/mL ≈ 50 nmol/L
- 30 ng/mL ≈ 75 nmol/L
- 50 ng/mL ≈ 125 nmol/L
- 100 ng/mL ≈ 250 nmol/L
- 150 ng/mL ≈ 375 nmol/L

Because these landmarks fall at round numbers in both unit systems only approximately, the threshold in one system will always appear "off" when converted precisely. The IOM's 50 nmol/L is exactly 20.03 ng/mL — close enough to 20 ng/mL that the distinction is clinically negligible, but it explains why some laboratory reports show 20 ng/mL and others show 50 nmol/L as the same threshold.

### The Central Controversy: Two Authoritative Bodies, Two Different Cutoffs

The most clinically consequential feature of serum 25(OH)D interpretation is that two major authoritative bodies examined much of the same evidence base in 2011 and arrived at different sufficiency thresholds. This is not a minor technical disagreement — it is the reason that one clinical laboratory may flag 22 ng/mL as "normal" while another flags it as "insufficient," even when running the same patient sample.

**The IOM / National Academy of Medicine (2011)**

In 2011, the Institute of Medicine (now the National Academy of Medicine) published its *Dietary Reference Intakes for Calcium and Vitamin D*, a systematic review covering over 1,000 publications [11, regulatory]. The committee's framework was **population-level bone-health adequacy** — it asked what serum 25(OH)D level, if maintained across a population, would ensure that essentially everyone (specifically, 97.5% of individuals) had adequate skeletal health.

Their conclusions:

| Category | nmol/L | ng/mL |
|---|---|---|
| Deficiency (risk of rickets/osteomalacia) | <30 | <12 |
| At risk of inadequacy | 30–<50 | 12–<20 |
| Adequate (97.5% of population) | ≥50 | ≥20 |

The IOM concluded that **≥20 ng/mL (50 nmol/L) meets the vitamin D requirements of at least 97.5% of the population** for bone health and that "serum concentrations of 25(OH)D above 75 nmol/L (30 ng/mL) are not consistently associated with increased benefit" [11, regulatory]. Members of the IOM committee later published a direct response to the Endocrine Society guideline in JCEM, arguing that the Endocrine Society's higher threshold was "not supported by a comprehensive review of the evidence" and relied on "expert opinion regarding a selective set of data" [12, mechanism_review].

The IOM's framing matters: it was designing a reference intake for **healthy people at the population level**, not a clinical treatment target for individuals with bone disease or malabsorption. The question it answered was: "What level protects essentially all Americans from deficiency-related skeletal disease?"

**The Endocrine Society (2011)**

In the same year, the Endocrine Society convened a task force under Michael F. Holick that published its *Clinical Practice Guideline* in JCEM [13, regulatory]. The Endocrine Society's framing was different: it was addressing **clinical management of individuals at risk for or with vitamin D deficiency**, including the elderly, dark-skinned individuals, the obese, people with malabsorption syndromes, and those on medications affecting vitamin D metabolism.

Their thresholds:

| Category | ng/mL | nmol/L |
|---|---|---|
| Deficiency | <20 | <50 |
| Insufficiency | 20–29 | 50–72 |
| Sufficiency | ≥30 | ≥75 |

The Endocrine Society supported the higher 30 ng/mL threshold on two biochemical grounds [13, regulatory]:

1. **PTH suppression:** Parathyroid hormone (PTH) levels are inversely correlated with 25(OH)D and begin to plateau — signaling adequate vitamin D — when 25(OH)D is between 30 and 40 ng/mL, not at 20 ng/mL.
2. **Calcium absorption efficiency:** Studies in postmenopausal women demonstrated that raising 25(OH)D from ~20 to ~32 ng/mL increased intestinal calcium absorption efficiency by 45–65%, a physiologically meaningful benefit above the IOM's adequacy cut point.

The Endocrine Society's question was effectively: "What level optimizes individual-level calcium and phosphorus homeostasis in people who may be at risk?" That question yields a higher target.

**Why the Disagreement Persists**

The IOM and Endocrine Society disagreement is not primarily a dispute about the biology — it is a dispute about **what question is being answered and who the target population is** [11, regulatory; 12, mechanism_review; 13, regulatory]:

- The IOM assessed what level protects 97.5% of a *healthy general population* from classical deficiency disease (rickets, osteomalacia). At 20 ng/mL, the population is, by this metric, adequately covered.
- The Endocrine Society asked what level *optimizes* individual metabolic parameters (PTH, calcium absorption) in *at-risk patients*. By that criterion, 30 ng/mL is the better target.

Neither framework is wrong on its own terms. The IOM's 20 ng/mL is a public-health floor; the Endocrine Society's 30 ng/mL is a clinical optimization target. The confusion arises when a laboratory applies one body's threshold in a context designed for the other — which is precisely what happens when labs print "reference ranges" without noting which guideline they are following.

### The 2024 Endocrine Society Shift

In June 2024, the Endocrine Society published a new clinical practice guideline — *Vitamin D for the Prevention of Disease* (Demay et al., JCEM 2024) — that represents a significant departure from its 2011 position [14, regulatory].

The 2024 guideline:

- **Recommends against routine 25(OH)D testing** in all populations examined, including healthy adults under 50, adults 50–74, adults 75 and older, and pregnant individuals.
- **Explicitly retires its prior numeric targets**: "The Endocrine Society no longer endorses the target 25(OH)D level of 30 ng/mL (75 nmol/L) suggested in the previous guideline" and no longer specifies numeric serum concentrations to define sufficiency, insufficiency, or deficiency.
- **Recommends empiric (test-free) vitamin D supplementation** at standard dietary reference intake doses for four groups where RCT evidence supports benefit: children and adolescents (1–18 years, to prevent rickets and reduce respiratory infections), adults 75 and older (potential mortality reduction), pregnant individuals (reduced risk of preeclampsia and preterm birth), and adults with prediabetes (delayed progression to diabetes).
- For healthy adults under 75, the guideline recommends taking the standard recommended daily allowance, with no mandate for serum testing to guide that decision.

The 2024 guideline was built on GRADE evidence review of randomized controlled trials rather than observational literature — a methodological shift that led to more conservative conclusions than the 2011 expert-opinion-weighted approach.

### Toxicity: The Upper Boundary

The toxicity zone for 25(OH)D is well above any sufficiency threshold. The NIH Office of Dietary Supplements and the IOM identify emerging concern above approximately **125–150 nmol/L (50–60 ng/mL)** [3, mechanism_review]. Frank vitamin D toxicity, characterized by hypercalcemia (serum calcium >11.1 mg/dL) and its sequelae (nausea, weakness, polyuria, nephrolithiasis), is typically associated with levels **>375 nmol/L (>150 ng/mL)** and almost always requires sustained massive supplementation (50,000–1,000,000 IU/day for months). Levels encountered in clinical practice from standard supplementation are extremely unlikely to reach the toxic range.

In practice:
- **>125 nmol/L (>50 ng/mL):** Potentially excessive; no established additional benefit.
- **>375 nmol/L (>150 ng/mL):** Frank toxicity zone; hypercalcemia typically present.
- Levels commonly seen in clinical patients (20–80 ng/mL) carry no toxicity risk.

The IOM/National Academies (2011) set the tolerable upper intake level (UL) at 4,000 IU/day for adults; toxicity is unlikely below 10,000 IU/day in most adults but documented at sustained doses above 4,000 IU/day in some individuals [11, regulatory; 27, mechanism_review].

---

## Measurement & Standardization

### The Two Assay Classes

Clinical laboratories measure serum total 25-hydroxyvitamin D by one of two fundamentally different approaches, which differ sharply in accuracy, specificity, and cost.

**Automated immunoassays** (chemiluminescent competitive-binding assays and ELISA-based platforms such as Abbott Architect, Roche Cobas, Beckman Coulter, and DiaSorin) dominate routine practice because they are fast, high-throughput, and require minimal sample preparation. Their principal limitations are well documented:

- *D2 (ergocalciferol) cross-reactivity / under-recovery.* Many immunoassays do not respond equivalently to 25(OH)D2 and 25(OH)D3. In a VDSP intralaboratory study evaluating 13 assays (11 immunoassays + 1 LC-MS/MS) across 50 serum samples, nine of eleven immunoassays showed deviations of up to 30% at high 25(OH)D2 concentrations, while only three immunoassays and the LC-MS/MS method handled D2-enriched samples without significant interference [16, mechanism_review]. This D2 under-recovery is clinically important for patients supplementing with ergocalciferol (D2).
- *DBP (vitamin D–binding protein) interference.* 25(OH)D circulates almost entirely bound to DBP (~88%) and albumin (~12%), with only ~0.03% free. Competitive immunoassays require a release reagent to displace 25(OH)D from DBP before antibody capture. Because DBP circulates at a 20–100-fold molar excess relative to 25(OH)D, incomplete displacement or re-binding to residual DBP causes concentration-dependent signal suppression. Immunoassays with different release-reagent formulations therefore show variable DBP-dependent inaccuracies not seen in chromatographic procedures [17, cohort]. In the Biochemia Medica head-to-head comparison, the Roche Cobas showed a mean bias of –14.1% against LC-MS/MS, while Abbott Architect showed +15.1% — both concentration-dependent [18, cohort].
- *C3-epimer cross-reactivity.* The structural isobar 3-epi-25(OH)D3 (see §C3-Epimer below) is not resolved by most immunoassays and elevates the reported total.

**LC-MS/MS (liquid chromatography–tandem mass spectrometry)** is the reference-grade method. It separates 25(OH)D3 and 25(OH)D2 chromatographically before mass-based detection, providing independent quantification of each form. A modified LC-MS/MS protocol that includes a longer chromatographic run or chemical derivatization can additionally resolve 3-epi-25(OH)D3 from the parent compound [19, cohort]. In the VDSP baseline interlaboratory comparison study (15 laboratories, 50 serum samples), nearly all LC-MS/MS results met VDSP performance criteria (CV ≤10%, mean bias ≤|5%|), while only 3 of 8 immunoassay platforms achieved the bias criterion [15, cohort]. HPLC with UV detection, an older chromatographic approach, separates D2 and D3 but lacks the sensitivity and specificity of tandem mass spectrometry and is now largely supplanted by LC-MS/MS in reference laboratories.

### The Standardization Infrastructure

The inter-laboratory and inter-method disagreement in 25(OH)D measurement has been one of the most consequential analytical problems in clinical chemistry. Before standardization efforts matured, the same serum sample could be reported as vitamin D–deficient by one automated platform and vitamin D–sufficient by another — a bias spread as large as 30–40% was documented depending on concentration range and platform [20, mechanism_review; 18, cohort]. This is not a trivial technical nuance: it directly underlies the threshold-setting controversy. As Binkley et al. (2017) demonstrated using NHANES III data, a ±12% assay bias shifts the apparent prevalence of 25(OH)D <30 nmol/L by several percentage points nationally, and a single concentration point can shift by 15 ng/mL (20 → 35 ng/mL) depending on the direction of the assay bias [20, mechanism_review]. Reported disagreements between the Endocrine Society (sufficiency at ≥30 ng/mL) and IOM (sufficiency at ≥20 ng/mL) are partially confounded by the fact that the threshold studies were conducted on platforms with different systematic biases.

The response to this problem was a three-institution reference measurement infrastructure:

1. **NIST Standard Reference Material 972a** — a four-level frozen human serum panel with certified values for 25(OH)D2, 25(OH)D3, 3-epi-25(OH)D3, and 24R,25(OH)2D3, assigned by dual isotope-dilution LC-MS/MS at NIST and CDC [15, cohort]. SRM 972a is the anchor calibrator for assay developers and laboratory accreditation bodies.

2. **The Vitamin D Standardization Program (VDSP)** — a collaborative initiative of NIH Office of Dietary Supplements, NIST, CDC, and international national survey laboratories that (a) established reference measurement procedures (RMPs) at NIST, Ghent University, and CDC; (b) conducted interlaboratory comparison exercises quantifying baseline assay disagreement; and (c) developed retrospective standardization protocols allowing older study data measured on pre-standardization assays to be re-expressed on the reference scale [16, mechanism_review; 20, mechanism_review].

3. **CDC Vitamin D Standardization-Certification Program (VDSCP)** — the operational certification arm. Laboratories and manufacturers submit to quarterly performance rounds; certification requires ≤10% CV and ≤|5%| mean bias for four consecutive quarters against CDC's reference measurements. Once certified, laboratories carry an auditable traceability chain to the NIST/Ghent RMPs [21, mechanism_review]. Immunoassay bias has decreased appreciably since the VDSCP launched, but Ferrari et al. (2017) cautioned that as of the mid-2010s, bias exceeding ±15% — and exceeding 100% at very low concentrations (<21 nmol/L) — still appeared in proficiency surveys for some platforms [20, mechanism_review; 22, mechanism_review].

The practical implication: when comparing 25(OH)D values across studies, laboratories, or time points, assay traceability to the NIST/CDC reference scale is the minimum requirement for valid comparison. A value of "20 ng/mL" on a non-standardized immunoassay is not interchangeable with "20 ng/mL" on an RMP-traceable LC-MS/MS.

### The C3-Epimer

3-epi-25(OH)D3 (the C3-epimer) is a structural isobar of 25(OH)D3 formed by epimerization at carbon-3 of the A-ring. It is not separated from 25(OH)D3 by most immunoassays or by LC-MS/MS methods that do not incorporate a dedicated chromatographic separation step, meaning it contributes to the reported total.

The epimer is present in adult serum at low concentrations (<5% of total 25(OH)D3 in most adults), but it is substantially elevated in infants. Singh et al. (2006) found detectable epimer in 22.7% of 172 infants, where it contributed 8.7–61.1% of the total 25-OHD — with higher fractions in younger infants (r = −0.48 for age) [19, cohort]. This means a non-epimer-separating assay can substantially overestimate true biologically active 25(OH)D3 in neonates and infants.

Wright et al. (2012) confirmed, using both an epimer-resolving and a non-resolving LC-MS/MS method on 71 infants and 1,046 adults, that epimer separation is clinically significant in the first year of life but is not required for accurate 25(OH)D3 measurement in patients older than 2 years [23, mechanism_review]. For pediatric reference-range studies and neonatal screening panels, epimer-resolving methods are preferred. NIST SRM 972a certifies 3-epi-25(OH)D3 concentrations precisely because this epimer poses a recognized interference.

### Free vs. Total 25(OH)D and DBP Genetic Polymorphisms

Virtually all clinical assays measure TOTAL 25(OH)D (DBP-bound + albumin-bound + free). The **free 25(OH)D hypothesis** proposes that biologically active vitamin D is the ~0.03% unbound (free) fraction, analogous to free thyroid hormones, and that total 25(OH)D is a poor proxy when DBP concentrations vary systematically.

This has direct relevance to interpreting vitamin D status across ancestries. DBP is encoded by the GC gene, and two common single-nucleotide polymorphisms (rs7041 and rs4588) produce GC isoforms with different binding affinities for 25(OH)D and different population frequencies by ancestry. Historically, African Americans were observed to have lower total 25(OH)D than white Americans but paradoxically similar rates of bone-disease endpoints, suggesting adequacy despite lower measured totals.

Nielson et al. (2016) showed that the apparent racial difference in DBP concentration was largely an artifact of monoclonal antibody ELISA assays for DBP: the monoclonal ELISA reported 54% lower DBP in African Americans versus whites, but polyclonal assays and mass-spectrometry-based proteomics showed no significant racial difference in DBP [24, cohort]. Critically, the study found that free 25(OH)D measured from polyclonal DBP assays tracked total 25(OH)D concentration irrespective of race — meaning African Americans with lower total 25(OH)D also had lower free 25(OH)D on the more accurate measurement system. The clinical and policy debate continues, but the methodological lesson is firm: the long-cited "similar bioavailable D despite lower total D in Black populations" was partly a DBP assay artifact.

### D2 vs. D3 Quantification and Pre-Analytic Stability

When 25(OH)D is reported as a **total** value, clinicians lose information about the D2/D3 split. This matters because ergocalciferol (D2) supplementation raises 25(OH)D2 and some immunoassays differentially under-recover D2, leading to apparent non-response to supplementation. LC-MS/MS reports D2 and D3 separately, which is the preferred approach in research and in patients whose supplementation form matters clinically.

**Pre-analytic stability:** 25-hydroxyvitamin D is unusually robust. Antoniucci et al. (2005) found serum 25(OH)D unaffected by multiple freeze-thaw cycles [25, cohort]; Wielders and Wijnberg (2009) demonstrated stability "solid as a rock" at room temperature in whole blood and serum [26, cohort]. Routine sample handling with brief room-temperature exposure, standard refrigeration during processing, and multiple freeze-thaw cycles does not meaningfully alter results. Light protection and prompt centrifugation remain standard practice but are less critical for this analyte than for, e.g., folate or bilirubin.

---

## Determinants & Clinical Significance

### What Lowers Serum 25(OH)D

Circulating 25(OH)D reflects the integrated output of cutaneous synthesis and dietary supply, processed by hepatic 25-hydroxylation. Multiple independent factors deplete this reserve.

**Reduced UVB exposure** is the dominant population-level determinant. High latitude, winter season, consistent sunscreen use, indoor occupations, and full-body clothing all reduce the UVB photons reaching skin. Darker skin pigmentation is a distinct mechanism: melanin competes with 7-dehydrocholesterol for UVB photons, so individuals with higher constitutive pigmentation require substantially greater sun exposure to synthesize equivalent amounts of pre-vitamin D3 [27, mechanism_review]. This is reflected in population data showing markedly lower mean 25(OH)D in Black Americans compared with White Americans at equivalent dietary intakes and latitudes [3, mechanism_review].

**Low dietary intake** contributes in populations with limited fortified food consumption. Few foods are naturally rich in vitamin D; reliance on fortified dairy, fatty fish, or supplements is necessary in the absence of adequate sun exposure.

**Fat malabsorption syndromes** impair absorption of this lipid-soluble vitamin: celiac disease, Crohn's disease/IBD, cholestatic liver disease, cystic fibrosis, and bariatric surgery (particularly Roux-en-Y gastric bypass, which bypasses the proximal small bowel where absorption is greatest) all reduce bioavailable vitamin D from diet and supplements.

**Obesity** lowers serum 25(OH)D through volumetric dilution: the same oral or cutaneous vitamin D dose distributes across a larger body volume, reducing peak serum concentration. Evidence favors dilution over passive sequestration in adipose tissue as the primary mechanism, though both likely contribute [28, cohort]. At the same vitamin D intake, obese individuals consistently show lower circulating 25(OH)D [3, mechanism_review].

**Chronic kidney disease (CKD)** impairs both the initial 25-hydroxylation step (early CKD, combined with reduced dietary intake common in these patients) and, critically, the renal 1α-hydroxylation that converts 25(OH)D to the active hormone 1,25(OH)₂D. Liver disease impairs the first hydroxylation step. Nephrotic syndrome causes urinary loss of vitamin D-binding protein (DBP) and its bound 25(OH)D.

**Aging** reduces skin content of 7-dehydrocholesterol by approximately 75% between ages 20 and 80, substantially decreasing cutaneous vitamin D3 production for a given UVB exposure [3, mechanism_review].

**Drug-induced catabolism**: anticonvulsants (phenytoin, carbamazepine), glucocorticoids, certain antiretrovirals, and rifampin all induce hepatic CYP3A4 and/or 24-hydroxylase (CYP24A1), accelerating 25(OH)D catabolism and lowering serum levels.

**What raises 25(OH)D:** supplementation (D3 more potently than D2 at equivalent doses), increased sun exposure, and granulomatous disease — though in granulomatous disease (sarcoidosis, TB, berylliosis) the elevated metabolite of concern is 1,25(OH)₂D (produced ectopically by macrophage CYP27B1), not 25(OH)D per se. Monitoring both in sarcoidosis is appropriate.

### Deficiency Consequences — Causal Evidence

The unambiguous causal deficiency disease of vitamin D is impaired bone mineralization. In children with unfused growth plates, severe deficiency causes **rickets**: widened growth plates, bowing deformities of weight-bearing bones, craniotabes, rachitic rosary, and in severe cases hypocalcemic tetany or seizures. In adults, the equivalent disorder is **osteomalacia**: defective mineralization of newly formed osteoid produces soft, pain-prone bones prone to stress fractures and pseudofractures, with characteristic proximal muscle weakness. These syndromes respond to vitamin D repletion; they do not occur in replete individuals. This causal relationship is not in dispute and is supported by a century of clinical and experimental evidence [3, mechanism_review; 27, mechanism_review].

The mechanism is direct: 1,25(OH)₂D drives intestinal calcium and phosphate absorption and regulates their incorporation into hydroxyapatite. Without adequate substrate delivery, osteoid remains unmineralized.

**Secondary hyperparathyroidism** is a downstream consequence of vitamin D deficiency operating through calcium. Low 25(OH)D → reduced 1,25(OH)₂D → reduced intestinal calcium absorption → hypocalcemia → sustained parathyroid hormone (PTH) elevation → PTH-mediated bone resorption and renal phosphate wasting. Over time this drives cortical bone loss and fracture risk in deficient individuals, particularly in the institutionalized elderly with concurrent calcium inadequacy.

**Proximal myopathy and falls risk** accompany overt deficiency through a less completely characterized pathway involving VDR signaling in skeletal muscle, with reversal on repletion.

### The Observational–RCT Divergence

Low serum 25(OH)D is consistently associated in large observational cohorts with higher risks of cardiovascular disease, cancer, all-cause mortality, autoimmune disease, respiratory infection, type 2 diabetes, and depression. These associations are graded, biologically plausible, and numerically substantial. They drove two decades of optimistic RCT design.

The large, well-powered supplementation trials have largely failed to confirm the benefits implied by observational associations in general or replete populations.

**VITAL (Manson JE et al., NEJM 2019; PMID 30415629; N = 25,871)**: This factorial, randomized, double-blind trial tested vitamin D3 2,000 IU/day versus placebo in U.S. adults (men ≥50, women ≥55) with median follow-up of 5.3 years. Neither co-primary endpoint was met: invasive cancer incidence HR 0.96 (95% CI 0.88–1.06; P = 0.47); major cardiovascular events HR 0.97 (95% CI 0.85–1.12; P = 0.69) [29, rct]. A secondary analysis suggested a cancer-mortality signal (HR 0.83, 95% CI 0.67–1.02), but this did not cross the significance threshold and was not prespecified as a primary endpoint.

A notable finding came from the VITAL autoimmune ancillary analysis: **Hahn et al. (BMJ 2022; DOI 10.1136/bmj-2021-066452; N = 25,871)**, using the same cohort with blinded adjudicated outcomes, found that vitamin D3 2,000 IU/day reduced confirmed autoimmune disease incidence by 22% (HR 0.78; 95% CI 0.61–0.99; P = 0.05), including rheumatoid arthritis, polymyalgia rheumatica, psoriasis, and autoimmune thyroid disease [30, rct]. This is among the more credible positive signals in the supplementation literature, though the P-value is borderline and the diseases were analyzed as a composite.

**D-Health (Neale RE et al., Lancet Diabetes Endocrinol 2022; PMID 35026158; N = 21,315)**: Monthly oral vitamin D3 60,000 IU in Australians aged ≥60 was tested with all-cause mortality as the primary endpoint. No benefit was observed: HR 1.04 (95% CI 0.93–1.18; P = 0.47) [31, rct]. Exploratory analyses excluding the first two years showed numerically higher cancer mortality in the vitamin D arm, a hypothesis-generating signal requiring cautious interpretation.

**ViDA (Scragg R et al., JAMA Cardiology 2017; PMID 28384800; N = 5,108)**: Monthly high-dose vitamin D3 (initial 200,000 IU then 100,000 IU monthly) in New Zealand adults aged 50–84 over a median 3.3 years showed no reduction in cardiovascular disease: HR 1.02 (95% CI 0.87–1.20) [32, rct].

**Fracture evidence**: Meta-analysis of 33 RCTs (N = 51,145 community-dwelling adults) found no significant association between vitamin D supplementation alone or combined calcium+vitamin D supplementation and fracture incidence [33, meta_analysis]. Benefit from calcium+vitamin D supplementation has been observed in institutionalized older adults and those with documented deficiency with concurrent calcium inadequacy; it is not generalizable to replete community-dwelling populations.

**Why the divergence?** The observational associations carry substantial confounding that is difficult to eliminate. Reverse causation is particularly likely: illness, obesity, and physical inactivity all independently lower 25(OH)D through reduced sun exposure, reduced outdoor activity, and volumetric dilution in obesity. A low 25(OH)D may thus be a marker of poor health rather than a cause of it. Supplementing to correct the biomarker in a population already replete, or in whom low 25(OH)D is a downstream consequence of another condition, is unlikely to replicate the observational benefit.

**The honest summary**: 25(OH)D is a robust marker of vitamin D status, and the bone-disease evidence — rickets, osteomalacia, secondary hyperparathyroidism in deficient individuals — is unambiguously causal. Supplementing documented deficiency for bone protection is evidence-based. The large RCTs, however, provide little support for supplementing to chase a high-normal 25(OH)D number as a strategy to prevent cardiovascular disease, cancer, diabetes, or mortality in replete or general populations. The autoimmune-disease signal from VITAL is the most promising non-bone finding but requires independent replication.

### Measurement Limitations and Clinical Framing

Serum 25(OH)D is the correct test for status assessment; 1,25(OH)₂D is not a status marker (it may be normal or even elevated as PTH drives its synthesis despite 25(OH)D deficiency). Assay standardization matters: the VDSP has documented 10–15% inter-assay variation between platforms, making threshold comparisons across studies imprecise. The total vs. free 25(OH)D debate remains active — DBP-bound vitamin D may not be bioavailable, and conditions that alter DBP (liver disease, nephrotic syndrome, pregnancy, genetic DBP variants) may cause total 25(OH)D to misrepresent biologically active vitamin D. Deficiency thresholds (20 ng/mL per IOM; 30 ng/mL per Endocrine Society, now de-emphasized in 2024) remain contested. In any patient where bone disease is suspected, serum calcium, phosphate, PTH, and alkaline phosphatase should be interpreted alongside 25(OH)D; 25(OH)D in isolation does not diagnose osteomalacia.

**25(OH)D is a status marker, not a proven causal lever for most non-bone outcomes. Treat the underlying condition that drives deficiency, correct deficiency for bone protection, and resist the temptation to optimize the number as a proxy for disease prevention.**

---

## Bibliography

[1]. Ramasamy I. Vitamin D Metabolism and Guidelines for Vitamin D Supplementation. *Clin Biochem Rev.* 2020;41(3):103–126. PMCID: PMC7731935. PMID: 33343045 — tag: mechanism_review — tier: 2

[2]. Holick MF. The Vitamin D Deficiency Pandemic and Consequences for Nonskeletal Health: Mechanisms of Action. *Mol Aspects Med.* 2008;29(6):361–368. PMCID: PMC2629072. PMID: 18801384 — tag: mechanism_review — tier: 2

[3]. National Institutes of Health, Office of Dietary Supplements. Vitamin D: Fact Sheet for Health Professionals. Updated 2024. https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/ — tag: regulatory — tier: 1

[4]. Bikle DD. Vitamin D: Newer Concepts of Its Metabolism and Function at the Basic and Clinical Level. *J Endocr Soc.* 2020;4(2):bvz038. DOI: 10.1210/jendso/bvz038 — tag: mechanism_review — tier: 2

[5]. Tuckey RC, Cheng CYS, Slominski AT. The serum vitamin D metabolome: What we know and what is still to discover. *J Steroid Biochem Mol Biol.* 2019;186:4–21. PMCID: PMC6342654. PMID: 30205156 — tag: mechanism_review — tier: 2

[6]. Latic N, Erben RG. FGF23 and Vitamin D Metabolism. *JBMR Plus.* 2021;5(12):e10558. DOI: 10.1002/jbm4.10558 — tag: mechanism_review — tier: 2

[7]. Wootton AM. Improving the Measurement of 25-hydroxyvitamin D. *Clin Biochem Rev.* 2005;26(1):33–36. PMCID: PMC1240027. PMID: 16278775 — tag: mechanism_review — tier: 2

[8]. Bikle D. The Free Hormone Hypothesis: When, Why, and How to Measure the Free Hormone Levels to Assess Vitamin D, Thyroid, Sex Hormone, and Cortisol Status. *JBMR Plus.* 2021;5(1):e10418. PMCID: PMC7839820. PMID: 33553985 — tag: mechanism_review — tier: 2

[9]. Portales-Castillo I, Simic P. PTH, FGF-23, Klotho and Vitamin D as regulators of calcium and phosphorus: Genetics, epigenetics and beyond. *Front Endocrinol (Lausanne).* 2022;13:992666. PMCID: PMC9558279. PMID: 36246903 — tag: mechanism_review — tier: 2

[10]. Hammami MM, Yusuf A. Differential effects of vitamin D2 and D3 supplements on 25-hydroxyvitamin D level are dose, sex, and time dependent: a randomized controlled trial. *BMC Endocr Disord.* 2017;17(1):12. PMCID: PMC5324269. PMID: 28231782 — tag: rct — tier: 2

[11]. National Academies of Sciences (Institute of Medicine). *Dietary Reference Intakes for Calcium and Vitamin D*. Ross AC, Manson JE, Abrams SA, et al. (Committee Chairs). Washington, DC: National Academies Press; 2011. https://www.nationalacademies.org/read/13050/chapter/10 — tag: regulatory — tier: 1

[12]. Rosen CJ, Abrams SA, Aloia JF, Brannon PM, Clinton SK, Durazo-Arvizu RA, Gallagher JC, Gallo RL, Jones G, Kovacs CS, Manson JE, Mayne ST, Ross AC, Shapses SA, Taylor CL. IOM Committee Members Respond to Endocrine Society Vitamin D Guideline. *J Clin Endocrinol Metab.* 2012;97(4):1146–1152. PMID: 22442278. https://academic.oup.com/jcem/article-abstract/97/4/1146/2833210 — tag: mechanism_review — tier: 1

[13]. Holick MF, Binkley NC, Bischoff-Ferrari HA, Gordon CM, Hanley DA, Heaney RP, et al. Evaluation, Treatment, and Prevention of Vitamin D Deficiency: an Endocrine Society Clinical Practice Guideline. *J Clin Endocrinol Metab.* 2011;96(7):1911–1930. PMID: 21646368. https://academic.oup.com/jcem/article/96/7/1911/2833671 — tag: regulatory — tier: 1

[14]. Demay MB, Pittas AG, Bikle DD, et al. Vitamin D for the Prevention of Disease: An Endocrine Society Clinical Practice Guideline. *J Clin Endocrinol Metab.* 2024;109(8):1907–1947. PMID: 38828931. https://academic.oup.com/jcem/article/109/8/1907/7685305 — tag: regulatory — tier: 1

[15]. Wise SA, Phinney KW, Tai SS-C, et al. Baseline Assessment of 25-Hydroxyvitamin D Assay Performance: A Vitamin D Standardization Program (VDSP) Interlaboratory Comparison Study. *J AOAC Int.* 2017;100(5):1244–1252. PMID: 28822355. https://doi.org/10.5740/jaoacint.17-0258 — tag: cohort — tier: 2

[16]. Wise SA, Camara JE, Sempos CT, et al. Vitamin D Standardization Program (VDSP) intralaboratory study for the assessment of 25-hydroxyvitamin D assay variability and bias. *J Steroid Biochem Mol Biol.* 2021;212:105917. PMID: 34010687. https://doi.org/10.1016/j.jsbmb.2021.105917 — tag: mechanism_review — tier: 2

[17]. Heijboer AC, Blankenstein MA, Kema IP, Buijs MM. Accuracy of 6 routine 25-hydroxyvitamin D assays: influence of vitamin D binding protein concentration. *Clin Chem.* 2012;58(3):543–548. PMID: 22247500. doi:10.1373/clinchem.2011.176545 — tag: cohort — tier: 1

[18]. Kocak FE, Ozturk B, Isiklar OO, et al. A comparison between two different automated total 25-hydroxyvitamin D immunoassay methods using liquid chromatography-tandem mass spectrometry. *Biochemia Medica.* 2015;25(3):430–438. https://doi.org/10.11613/BM.2015.044 — tag: cohort — tier: 1

[19]. Singh RJ, Taylor RL, Reddy GS, Grebe SKG. C-3 Epimers Can Account for a Significant Proportion of Total Circulating 25-Hydroxyvitamin D in Infants, Complicating Accurate Measurement and Interpretation of Vitamin D Status. *J Clin Endocrinol Metab.* 2006;91(8):3055–3061. https://doi.org/10.1210/jc.2006-0710 — tag: cohort — tier: 1

[20]. Binkley N, Dawson-Hughes B, Durazo-Arvizu R, et al. Vitamin D measurement standardization: The way out of the chaos. *J Steroid Biochem Mol Biol.* 2017;173:117–121. PMID: 27979577. https://doi.org/10.1016/j.jsbmb.2016.12.002 — tag: mechanism_review — tier: 2

[21]. Centers for Disease Control and Prevention. Vitamin D Standardization-Certification Program (VDSCP). CDC Clinical Standardization Programs. https://www.cdc.gov/clinical-standardization-programs/php/vitamin-d/index.html — tag: mechanism_review — tier: 2

[22]. Ferrari D, Lombardi G, Banfi G. Concerning the vitamin D reference range: pre-analytical and analytical variability of vitamin D measurement. *Biochemia Medica.* 2017;27(3):030501. https://doi.org/10.11613/BM.2017.030501 — tag: mechanism_review — tier: 1

[23]. Wright MJP, Halsall DJ, Keevil BG. Removal of 3-Epi-25-Hydroxyvitamin D3 Interference by Liquid Chromatography–Tandem Mass Spectrometry Is Not Required for the Measurement of 25-Hydroxyvitamin D3 in Patients Older than 2 Years. *Clin Chem.* 2012;58(12):1719–1720. https://doi.org/10.1373/clinchem.2012.191460 — tag: mechanism_review — tier: 1

[24]. Nielson CM, Jones KS, Chun RF, et al. Free 25-Hydroxyvitamin D: Impact of Vitamin D Binding Protein Assays on Racial-Genotypic Associations. *J Clin Endocrinol Metab.* 2016;101(5):2226–2234. https://doi.org/10.1210/jc.2016-1104 — tag: cohort — tier: 1

[25]. Antoniucci DM, Black DM, Sellmeyer DE. Serum 25-Hydroxyvitamin D Is Unaffected by Multiple Freeze-Thaw Cycles. *Clin Chem.* 2005;51(1):258–261. https://doi.org/10.1373/clinchem.2004.041954 — tag: cohort — tier: 1

[26]. Wielders JPM, Wijnberg FA. Preanalytical Stability of 25(OH)–Vitamin D3 in Human Blood or Serum at Room Temperature: Solid as a Rock. *Clin Chem.* 2009;55(8):1584–1585. https://doi.org/10.1373/clinchem.2008.117366 — tag: cohort — tier: 1

[27]. Holick MF. Vitamin D Deficiency. *N Engl J Med.* 2007;357(3):266–281. doi:10.1056/NEJMra070553. PMID: 17634462 — tag: mechanism_review — tier: 1

[28]. Drincic AT, Armas LAG, Van Diest EE, Heaney RP. Volumetric dilution, rather than sequestration best explains the low vitamin D status of obesity. *Obesity.* 2012;20(7):1444–1448. doi:10.1038/oby.2011.404. PMID: 22262154 — tag: cohort — tier: 2

[29]. Manson JE, Cook NR, Lee I-M, et al. Vitamin D supplements and prevention of cancer and cardiovascular disease. *N Engl J Med.* 2019;380(1):33–44. doi:10.1056/NEJMoa1809944. PMID: 30415629 — tag: rct — tier: 1

[30]. Hahn J, Cook NR, Alexander EK, Friedman S, Walter J, Bubes V, Kotler G, Lee I-M, Manson JE, Costenbader KH. Vitamin D and marine omega 3 fatty acid supplementation and incident autoimmune disease: VITAL randomized controlled trial. *BMJ.* 2022;376:e066452. PMID: 35082139. doi:10.1136/bmj-2021-066452 — tag: rct — tier: 1

[31]. Neale RE, Baxter C, Duarte Romero B, McLeod DSA, English DR, Armstrong BK, Ebeling PR, Hartel G, Kimlin MG, O'Connell R, van der Pols JC, Venn AJ, Webb PM, Whiteman DC, Waterhouse M. The D-Health Trial: a randomised controlled trial of the effect of vitamin D on mortality. *Lancet Diabetes Endocrinol.* 2022;10(2):120–128. doi:10.1016/S2213-8587(21)00345-4. PMID: 35026158 — tag: rct — tier: 1

[32]. Scragg R, Stewart AW, Waayer D, Lawes CMM, Toop L, Sluyter J, Murphy J, Khaw KT, Camargo CA Jr. Effect of monthly high-dose vitamin D supplementation on cardiovascular disease in the Vitamin D Assessment Study: a randomized clinical trial. *JAMA Cardiol.* 2017;2(6):608–616. doi:10.1001/jamacardio.2017.0175. PMID: 28384800 — tag: rct — tier: 1

[33]. Zhao JG, Zeng XT, Wang J, Liu L. Association between calcium or vitamin D supplementation and fracture incidence in community-dwelling older adults: a systematic review and meta-analysis. *JAMA.* 2017;319(24):2466–2477. doi:10.1001/jama.2017.19344. PMID: 29279934 — tag: meta_analysis — tier: 1
