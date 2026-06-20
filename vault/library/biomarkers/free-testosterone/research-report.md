---
title: "Free Testosterone: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/free-testosterone/research-report
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.free-testosterone-design-work
provenance_slug: labs-specialist
source_count: 25
---

# Free Testosterone: Canonical Research Report

## Summary

Free testosterone (free T) is the unbound fraction of circulating testosterone — approximately 1–4% of total testosterone in healthy adult men — and represents the biologically active pool that can cross cell membranes, engage the androgen receptor, and exert tissue-level effects. The remaining testosterone is bound to sex hormone–binding globulin (SHBG, ~44% — tightly bound, biologically inactive) and albumin (~50–54% — loosely bound, largely bioavailable). Because only the free fraction can directly activate androgen receptors, free testosterone is the preferred measure whenever total testosterone is discordant with clinical findings — particularly when SHBG is elevated or suppressed by age, liver disease, thyroid disorders, obesity, or medications.

Three methods exist for determining free testosterone, and they are not interchangeable. **Equilibrium dialysis (ED) + LC-MS/MS** is the gold standard: it physically separates the free fraction by allowing small unbound molecules to cross a semipermeable membrane and quantifies the dialysate by mass spectrometry, detecting concentrations as low as ~1 pg/mL [1, mechanism_review]. The best standardized adult male reference data (Jasuja et al., n = 145) yield 66–309 pg/mL (all men ≥19 yr) and 120–368 pg/mL (men 19–39 yr) by this method [12, cohort]. **Calculated free testosterone (cFT)** using the Vermeulen equation — derived from total T, SHBG, and albumin via mass-action binding constants — is the practical clinical standard when ED is unavailable; it correlates closely with ED (r ≈ 0.99) but systematically overestimates absolute values by a median ratio of ~1.19× (Fiers et al.) [14, mechanism_review]. The two methods require their own reference intervals and cannot be used interchangeably against a single range. A third approach, **direct analog immunoassay**, should not be used for clinical decision-making: the Endocrine Society 2018 Clinical Practice Guideline explicitly advises against it because the tracer binds serum proteins in a manner the assay cannot account for, causing values to track total testosterone rather than the free fraction — producing results approximately one-seventh of equilibrium dialysis values [6, regulatory; 9, cohort].

A **harmonized reference interval for free testosterone does not exist**. Unlike total testosterone, no CDC HoSt–equivalent standardization program has been completed for free T, and reported ranges vary substantially across laboratories, methods, and equations. Clinicians must apply method-matched intervals and should not compare absolute values across methods.

In men with low or borderline SHBG, total testosterone over-estimates androgen deficiency; in men with high SHBG (aging, liver disease, hyperthyroidism), it under-estimates it. Free testosterone resolves this ambiguity. In women, calculated free T and the free androgen index (FAI) are the preferred markers of hyperandrogenism in PCOS, where cFT achieves pooled sensitivity of 0.89 vs. 0.74 for total T at comparable specificity [20, meta_analysis].

Units: pg/mL (conventional) × 3.467 → pmol/L (SI); ÷ 10 → ng/dL. Example: 150 pg/mL = 15 ng/dL = 520 pmol/L.

---

## Physiology & What Free Testosterone Measures

### The Free-Hormone Hypothesis

Testosterone circulates in blood almost entirely bound to plasma proteins — yet the bound fraction is biologically inert. The **free-hormone hypothesis** holds that only the unbound (free) fraction of a hormone can diffuse across cell membranes, enter the cytoplasm, engage the androgen receptor, and exert biological effects [1, mechanism_review]. Carrier-protein binding effectively sequesters the molecule in the vascular compartment, limiting its access to target tissues. This principle applies across multiple hormone classes — vitamin D metabolites, thyroid hormones, glucocorticoids — but is especially consequential for testosterone, because the fraction available for tissue action represents only a tiny sliver of what circulates in total [2, mechanism_review].

In 2016, Laurent and colleagues provided direct experimental validation in a transgenic mouse model [3, animal] (a murine finding; human confirmation is indirect). Mice were engineered to express circulating human SHBG (normal mice lack it). Despite markedly elevated **total** sex steroid concentrations resulting from SHBG-mediated prolongation of ligand half-life and hypothalamic-pituitary feedback, **free** testosterone was unaffected. Critically, sex-steroid bioactivity on reproductive organs was attenuated — a ligand-dependent, genotype-independent effect — confirming that SHBG-bound testosterone cannot effectively access target tissues. These mouse findings directly validated the clinical rationale for preferring free or bioavailable fractions over total testosterone in endocrine assessment, though the translational step to humans relies on indirect evidence rather than equivalent human RCT data.

### The Binding Equilibrium: Three Fractions

Circulating testosterone partitions across three functional pools, held in dynamic equilibrium [1, mechanism_review; 4, regulatory]:

| Fraction | Binding partner | Approximate % of total T | Bioavailable? |
|---|---|---|---|
| Free T | Unbound | ~2% | Yes — immediately |
| Albumin-bound T | Albumin (low affinity) | ~50–54% | Yes — readily dissociates |
| SHBG-bound T | SHBG (high affinity) | ~44% | No — tightly bound |

The canonical reference-adult-male figures (~44% SHBG-bound / ~50–54% albumin-bound / ~2% free) emerge from the equilibrium-binding model of Vermeulen, Verdonck, and Kaufman [5, mechanism_review]. Wider ranges appear in the literature — SHBG-bound fractions as high as 65% have been reported — but these figures carry population and method qualifiers; the canonical values apply to non-obese adult men at physiologic SHBG.

**Free testosterone (~2%)** is the immediately bioavailable fraction — completely unbound, diffusible across cell membranes without carrier assistance. The precise percentage ranges from 1–4% depending on population, sex, age, and assay method [1, mechanism_review].

**Bioavailable testosterone (~50–54%)** is the operationally useful clinical concept: it encompasses both the free fraction and the albumin-bound fraction. Albumin binds testosterone with such low affinity that this bond is readily broken in capillaries and at cell surfaces — the testosterone dissociates and enters tissue.

**SHBG-bound testosterone (~44%)** is the tightly sequestered, biologically inactive fraction. The high-affinity SHBG bond does not readily dissociate under physiological conditions, so this pool is unavailable to androgen receptors.

### Affinity Constants: Why SHBG Binds Irreversibly and Albumin Does Not

The critical distinction between SHBG-bound (unavailable) and albumin-bound (bioavailable) testosterone rests on a five orders-of-magnitude difference in association constants (Ka):

- **SHBG–testosterone:** Ka ≈ 0.7–2 × 10⁹ M⁻¹ (high affinity, tight bond) [1, mechanism_review; 2, mechanism_review]
- **Albumin–testosterone:** Ka ≈ 2.0–4.1 × 10⁴ M⁻¹ (low affinity, labile bond) [1, mechanism_review]

The Vermeulen formula uses Ka values of ~5.97 × 10⁸ L/mol for SHBG and ~3.6 × 10⁴ L/mol for albumin [5, mechanism_review]. This ~10,000-fold affinity difference is the mechanistic basis of the bioavailability distinction. Albumin circulates at approximately 4–5 g/dL — a concentration so high that, despite its low per-molecule affinity, it binds roughly half of all circulating testosterone by mass. The albumin-bound testosterone is loosely held; bond kinetics permit rapid off-rates that allow effective tissue delivery [2, mechanism_review].

The SHBG–testosterone interaction is qualitatively different. SHBG circulates as a 90-kDa homodimer; each homodimer binds testosterone at two sites, and recent biophysical data reveal allosteric interaction between sites — not a simple linear process but a dynamic, multistep interaction with conformational changes in the protein [1, mechanism_review]. The consequence is that even transient exposure to capillary walls is insufficient to liberate testosterone from SHBG under normal physiological conditions.

### SHBG Also Binds DHT and Estradiol: The Ligand-Selectivity Profile

SHBG is not specific to testosterone. Its binding pocket accommodates multiple sex steroids, with a clear affinity hierarchy:

- **Dihydrotestosterone (DHT):** highest affinity (~5× the affinity of testosterone; Kd ~1 nM) [1, mechanism_review]
- **Testosterone:** intermediate affinity (reference)
- **Estradiol (E₂):** approximately 10–20% the affinity of testosterone for SHBG [1, mechanism_review]

Because SHBG sequesters DHT more avidly than testosterone, changes in SHBG concentration have disproportionate effects on free DHT. Conversely, SHBG is a relatively weak buffer for estradiol. This selectivity profile means SHBG functions as a determinant of the androgen-to-estrogen balance at the tissue level, not merely an inert carrier.

### Why Free T Is the Relevant Measure When SHBG Is Abnormal

Total testosterone measures the full pool — free + albumin-bound + SHBG-bound. When SHBG concentration is normal, total testosterone correlates reasonably well with free testosterone and serves as a practical proxy. But SHBG is not fixed [2, mechanism_review; 6, regulatory]:

- **Conditions that lower SHBG** (obesity, type 2 diabetes, hypothyroidism, exogenous androgens, insulin resistance): total testosterone falls disproportionately, but free testosterone may remain normal — total T *understates* androgen status, risking over-diagnosis of deficiency.
- **Conditions that raise SHBG** (aging, hepatic cirrhosis, hyperthyroidism, estrogen exposure, HIV, anticonvulsants): total testosterone may appear normal or elevated, but free testosterone is reduced — total T *overstates* androgen status, masking deficiency.

The Endocrine Society 2018 Clinical Practice Guideline explicitly recommends measuring free testosterone (via equilibrium dialysis or validated calculation) in men whose total T is borderline low or who have conditions known to alter SHBG [6, regulatory].

---

## Measurement vs Calculation

Free testosterone constitutes roughly 1–4% of total circulating testosterone [1, mechanism_review]. Three distinct approaches exist for determining it, and they are **not interchangeable** — choosing the wrong one can produce values that differ by as much as 80% [9, cohort].

### 1. Equilibrium Dialysis (or Ultrafiltration) + LC-MS/MS — The Reference Method

Equilibrium dialysis (ED) is the gold standard against which all other methods are benchmarked [1, mechanism_review; 2, mechanism_review]. In the standard protocol, serum is placed on one side of a semipermeable membrane; buffer occupies the other. The system equilibrates at 37°C — typically overnight, though centrifugal ultrafiltration cartridges can accelerate this — after which only the unbound (free) hormone has crossed the membrane. The dialysate is quantified by liquid chromatography–tandem mass spectrometry (LC-MS/MS), which can reliably detect concentrations down to ~1 pg/mL [1, mechanism_review].

Ultrafiltration (UF) is a practical variant: centrifugal force pushes the ultrafiltrate through the membrane. When coupled to LC-MS/MS, UF shows excellent agreement with standard ED (correlation coefficient r = 0.978, bias ≈ 2.4%) [10, cohort].

**Why it is the reference, and why it is rarely the routine:** ED + LC-MS/MS physically separates free hormone based on molecular size, making no assumptions about binding constants or albumin concentration. The downsides are real: specialized equipment, multi-step sample handling, long turnaround, and cost. Only a handful of reference laboratories and academic centers run a fully standardized ED pipeline.

### 2. Calculated Free Testosterone (cFT) — The Practical Clinical Standard

Because ED is operationally demanding, mass-action–based algebraic models derive free T from inputs routinely measured: **total testosterone, SHBG, and albumin**. Two foundational equations exist:

- **Södergård equation (1982):** Södergård et al. derived binding constants at 37°C from experimental data, then applied the law of mass action [8, cohort]. In men, approximately 2% of testosterone was unbound — consistent with later ED measurements.

- **Vermeulen equation (1999):** Vermeulen et al. refined this approach in a rigorous validation study comparing calculated free T directly against equilibrium dialysis (PMID 10523012). Their conclusion was unambiguous: calculated free T represents "a rapid, simple, and reliable index of bioavailable T, comparable to AFTC and suitable for clinical routine" [5, mechanism_review]. Concordance between Vermeulen and Södergård estimates is high (r ≈ 0.98) [11, cohort].

In practice, albumin is often fixed at 4.3 g/dL because its intra-individual variation is small in non-critically-ill patients and the calculation output is relatively insensitive to this input [5, mechanism_review]. SHBG accuracy matters more.

The 2018 Endocrine Society Clinical Practice Guideline explicitly endorses calculated free T: when ED is unavailable, clinicians may "estimate fT concentrations using a formula that accurately calculates fT concentrations using TT, SHBG, and albumin concentrations" [6, regulatory]. Online calculators implementing the Vermeulen equation (e.g., issam.ch/freetesto.htm) make this accessible at point of care.

**Caveat:** cFT values trend approximately 20–24% higher than ED-measured free T in published comparisons [1, mechanism_review]. This systematic offset is consistent and predictable — not random noise — which is why cFT remains clinically useful as long as the same method is used for baseline and follow-up comparisons.

### 3. Direct Analog Immunoassay — Do Not Use

Many commercial automated analyzers offer a "free testosterone" result via a direct analog (tracer-based) immunoassay. A radiolabeled testosterone analog competes with endogenous testosterone for binding to an immobilized antibody.

**The method does not work as described.** The analog tracer behaves differently from native free testosterone: it interacts with serum binding proteins in a way the assay design does not account for, causing it to detect protein-bound testosterone rather than the genuinely free hormone [9, cohort]. Fritz et al. (2008, *Clinical Chemistry*) confirmed this mechanistically: when total testosterone was held constant while SHBG was varied, the analog assay tracked total testosterone — not the free fraction [9, cohort].

Clinical consequences:
- Analog assay values are roughly one-eighth of cFT values in the same patients [9, cohort].
- Values vary systematically with SHBG, which a free-fraction measurement should not do.
- The Endocrine Society 2018 guideline states directly: "Clinicians should **not** use direct analog-based free testosterone immunoassays, as they are inaccurate" [6, regulatory].
- The Winters analysis confirmed that the analog assay's dependence on SHBG renders it unreliable for assessing androgen deficiency in patients whose SHBG deviates from normal [18, mechanism_review].
- The 2007 Endocrine Society position statement (Rosner et al., PMID 17090633) flagged methodological pitfalls including direct immunoassay limitations [4, regulatory].

Despite this, direct analog assays remain widely offered because they are cheap, rapid, and run on standard immunoassay platforms. The presence of a "free testosterone" line on a standard lab panel does not mean the method is valid.

### Reference Ranges — Method-Dependent, No Universal Standard

**A harmonized reference interval for free testosterone does not exist.** The 2018 Endocrine Society guideline explicitly acknowledges this: "a harmonized reference range for fT has not been established, so reference ranges may vary considerably depending on the specific equilibrium dialysis method or the algorithm used" [6, regulatory].

The best standardized data come from Jasuja et al. (2023, *Andrology*), applying a rigorously standardized ED procedure in healthy nonobese men (n = 145) [12, cohort]:

| Group | Free T (pg/mL) | Free T (pmol/L) |
|-------|----------------|-----------------|
| All adult men (≥19 yr), 2.5th–97.5th %ile | 66–309 | 229–1072 |
| Young men (19–39 yr), 2.5th–97.5th %ile | 120–368 | 415–1274 |

Mean ED-measured values decline with age: ~102 pg/mL in men aged 20–29, ~80 pg/mL in men aged 70–79 — a ~30–40% age-associated decline [7, mechanism_review]. Calculated free T (Vermeulen) runs about 20–24% higher than ED values in the same populations [1, mechanism_review].

Broadly cited clinical ranges — typically 46–224 pg/mL (~160–776 pmol/L) or ~1.6–7.8 ng/dL — reflect mixed-method literature averages and should be treated as orientation, not precision cutoffs.

### Unit Conversions

| From | To | Factor |
|------|----|--------|
| pg/mL → pmol/L | multiply by | **3.467** |
| pmol/L → pg/mL | multiply by | **0.2884** |
| ng/dL → nmol/L | multiply by | **0.03467** |
| nmol/L → ng/dL | multiply by | **28.84** |
| pg/mL → ng/dL | divide by | **10** |
| ng/dL → pg/mL | multiply by | **10** |

Example: 150 pg/mL = 15 ng/dL = 520 pmol/L.

---

## Calculation Inputs, Standardization & Pitfalls

Calculated free testosterone (cFT) is not a single measured quantity — it is a model-derived estimate whose accuracy is bounded by the accuracy of three independent input measurements and the validity of the mathematical model's underlying assumptions.

### Three Inputs, Three Error Sources

The Vermeulen equation requires three inputs: total testosterone (TT), SHBG, and albumin, combined with experimentally determined association constants (Ka for albumin–testosterone ≈ 3.6 × 10⁴ L/mol; Ks for SHBG–testosterone ≈ 5.97 × 10⁸ L/mol) within a law-of-mass-action framework [5, mechanism_review].

**Total testosterone** is the most impactful input. Immunoassays for TT carry significant inter-assay and inter-laboratory variability. A survey of 1,133 laboratories using 14 different assays measuring the same sample found values ranging from 45 to 365 ng/dL — an eight-fold span [6, regulatory]. Bias of 35–50% relative to mass-spectrometry reference methods has been documented at physiologic male concentrations, with errors reaching 220% in sub-4 nmol/L ranges [4, regulatory]. The CDC Hormone Standardization Program (HoSt) for total testosterone — certifying labs to within ±6.4% of the CDC reference method — has substantially improved LC-MS/MS concordance, but immunoassay adoption of CDC-certified platforms remains incomplete [6, regulatory]. Any immunoassay bias in TT propagates linearly into cFT.

**SHBG** is measured exclusively by immunoassay in routine clinical practice — no mass-spectrometric reference method is in widespread clinical use, and no formal harmonization program equivalent to HoSt-TT exists for SHBG [13, cohort; 14, mechanism_review]. A 2025 European survey found SHBG measured exclusively by immunoassay across all participating centers, with considerable inter-laboratory variability in both absolute concentrations and reported reference intervals [13, cohort]. SHBG assays are calibrated against the WHO 2nd International Standard (NIBSC 08/266), but different platform antibodies recognize different epitopes, producing non-commutable results. Because free testosterone is inversely sensitive to SHBG — especially at high SHBG concentrations common in aging men — SHBG assay error can distort cFT estimates substantially.

**Albumin** is typically not measured; instead, a fixed population-mean value of 4.3 g/dL is assumed. Vermeulen et al. showed cFT is relatively insensitive to albumin within the normal physiologic range (40–50 g/L), with a fixed value of 43 g/L yielding r = 0.992 with equilibrium dialysis [5, mechanism_review]. This assumption breaks down in clinical populations with marked hypoalbuminemia (cirrhosis, nephrotic syndrome, critical illness) or hyperproteinemia.

### The Binding-Constant and Model Debate: Vermeulen vs. Zakharov

The Vermeulen model assumes a 1:1 stoichiometry between testosterone and each SHBG monomer, with identical binding affinity at both sites — a linear, non-cooperative model that predates modern biophysical characterization of the SHBG dimer interface [15, mechanism_review].

In 2015, Zakharov et al. proposed a multi-step, dynamic allosteric model in which the two monomers within the SHBG dimer are allosterically coupled — meaning occupancy of one binding site affects the affinity at the other [15, mechanism_review]. This ensemble-based model (cFT-Z) treats SHBG binding as a non-linear, multiphasic process. The Zakharov model produces systematically higher free T estimates than the Vermeulen equation.

The question of which model better matches equilibrium dialysis was examined by Fiers et al. (2018) in a study of 183 women and 146 men using LC-MS/MS–measured equilibrium dialysis as the comparator [14, mechanism_review]. Despite the Zakharov model's more sophisticated biophysical basis, it performed worse against equilibrium dialysis:

- **Vermeulen (cFT-V):** overestimated by a median ratio of **1.19**; that ratio was stable across SHBG variation (rank correlation ρ range: −0.17 to −0.01)
- **Zakharov (cFT-Z):** overestimated by a median ratio of **2.05**; bias was strongly correlated with SHBG levels (ρ = 0.75)

This means cFT-Z is more susceptible to SHBG-dependent bias than the Vermeulen equation, not less. The practical upshot: cFT values are model-dependent, and the two most-used models do not agree in absolute terms. Clinicians and researchers comparing cFT from different calculators must verify which formula was used. The Vermeulen equation remains the most widely endorsed approximation — acknowledged by the Endocrine Society for clinical use — but it is a systematic overestimate of equilibrium dialysis values.

A five-algorithm comparison by De Ronde et al. found that Bland–Altman analysis showed large absolute differences between algorithms despite moderate-to-high Pearson correlations, with confounding by SHBG concentrations introduced differentially depending on the algorithm [16, cohort]. The conclusion: algorithms must be revalidated in the local population before use.

### Method Discordance Summary

Three clinically available approaches produce materially different numerical values:

1. **ED + LC-MS/MS** — reference method; directly separates free from bound testosterone [14, mechanism_review]
2. **cFT (Vermeulen)** — correlates well with ED (r ≈ 0.986 in men [17, cohort]) and widely endorsed, but systematically overestimates by ~1.19× [14, mechanism_review]; requires its own reference intervals
3. **Direct analog immunoassay** — values approximately one-fourth to one-seventh of ED; correlates more strongly with total testosterone than with bioavailable testosterone, particularly in men with low SHBG [18, mechanism_review]; explicitly discouraged by the Endocrine Society [6, regulatory]

### No Harmonized Reference Interval for Free Testosterone

Total testosterone has benefited from CDC HoSt certification. No analogous program exists for free testosterone. The CDC's roadmap explicitly lists free testosterone and binding proteins under "standardization and harmonization programs in development" — a category distinct from the completed HoSt-TT program [6, regulatory]. The 2025 Narinx European survey confirmed this gap in practice: reference intervals for cFT showed "considerable variability" in both lower and upper limits across laboratories [13, cohort].

### Error Propagation and Analytical Interferences

**Biotin** supplements at supra-physiologic doses (≥5 mg, as used for hair/nail supplements and some multiple sclerosis trials) interfere with biotinylated immunoassays — the sandwich format used by many SHBG and TT platforms. Biotin competes with biotinylated reagents for streptavidin binding sites, producing falsely elevated results in competitive assays and falsely reduced results in sandwich assays. Both TT and SHBG immunoassays are susceptible, meaning biotin can distort both inputs to cFT simultaneously in either direction. LC-MS/MS assays are not affected. Patients should withhold biotin for at least 72 hours (or longer at very high doses) before sampling [19, mechanism_review].

**Heterophile antibodies** — including human anti-animal antibodies (HAAA) and other endogenous immunoglobulins — can produce falsely elevated or depressed results on both TT and SHBG immunoassays by cross-reacting with assay antibodies. Results inconsistent with clinical presentation, or discordant between platforms, should raise suspicion. The confirmatory step is LC-MS/MS for TT and, if possible, a different SHBG platform [19, mechanism_review].

**Extreme SHBG values** expose a structural limitation of the Vermeulen equation. At very high SHBG (>70–100 nmol/L, seen in hepatic disease, thyrotoxicosis, or aging), the cFT-V is particularly sensitive to any SHBG assay error. Published mean biases for cFT across methods range from 5.8% to 56.0% in head-to-head comparisons, with the worst discordance concentrated at the extremes of SHBG distribution [14, mechanism_review; 16, cohort].

**Competing steroids:** High circulating concentrations of DHT (e.g., during topical DHT therapy) or estradiol (e.g., pregnancy) occupy SHBG binding sites, but most immunoassays measure total SHBG protein rather than available binding capacity. This leads to overestimation of free T from the Vermeulen equation in these clinical states [1, mechanism_review].

---

## Determinants & Clinical Significance

### The Core Value: Free T When SHBG Is Abnormal

Total testosterone circulates in three fractions: roughly ~2% unbound (free), ~44% tightly bound to SHBG, and ~50–54% loosely bound to albumin — the canonical reference-adult-male figures [5, mechanism_review]. Wider ranges appear in the literature, but population and method qualifiers apply. Because only the free and albumin-bound fractions are biologically accessible, total testosterone can give a misleading picture whenever SHBG is abnormal.

**When SHBG is LOW** (obesity, insulin resistance, type 2 diabetes, metabolic syndrome, nephrotic syndrome, hypothyroidism, glucocorticoids, exogenous androgens): less testosterone is sequestered, so the free fraction may be preserved even as total T falls. In a cohort of 150 obese men, 52% met standard criteria for testosterone deficiency by total T, but that figure fell to 17.6% when calculated free testosterone was used instead — the discrepancy driven by SHBG levels tracking inversely with BMI [21, cohort]. Both insulin resistance (HOMA-IR) and SHBG independently predicted free testosterone after multivariate adjustment [21, cohort]. Defaulting to total T alone in an obese or metabolically unwell man risks labelling functional hormone status as deficient.

**When SHBG is HIGH** (aging, hyperthyroidism, estrogen/oral contraceptives, hepatic cirrhosis, HIV infection, anticonvulsants): more testosterone is locked onto the carrier, reducing the bioavailable fraction even as total T appears normal or high. In a single-centre retrospective cohort of HIV-infected men (n = 94 complete-profile patients), roughly 36% had SHBG > 70 nmol/L; using total testosterone alone identified hypogonadism in 10.6% of patients, whereas adding calculated free testosterone increased that rate to 20.2% — approximately a two-fold diagnostic gain [22, cohort]. SHBG rose with HIV infection duration, and compensatory increases in total T masked the progressive decline in free T.

### Endocrine Society Measurement Guidance

The 2018 Endocrine Society Clinical Practice Guideline specifies that when total testosterone is near the lower limit of normal, or when conditions known to alter SHBG are present, clinicians should obtain free testosterone by **equilibrium dialysis** or estimate it using a validated formula [6, regulatory]. The guideline explicitly cautions against the **analog immunoassay** [17, cohort; 5, mechanism_review]. Equilibrium dialysis remains the reference method; among calculated approaches, the Vermeulen equation demonstrates strong correlation with equilibrium dialysis (r ≈ 0.99), though it consistently overestimates, and different approaches require their own reference ranges [5, mechanism_review; 14, mechanism_review].

### Women and PCOS

In women, SHBG is typically higher than in men, so the total testosterone/free testosterone discrepancy is proportionally larger and more diagnostically consequential. The **free androgen index** (FAI = total T [nmol/L] × 100 / SHBG [nmol/L]) and calculated free testosterone are the standard biochemical markers of hyperandrogenism in suspected polycystic ovary syndrome (PCOS), because total testosterone alone is less sensitive for detecting androgen excess when SHBG varies.

A 2025 systematic review and diagnostic meta-analysis (13 studies, n = 2,182 for total T; 6 studies, n = 1,035 for calculated free T) found that calculated free testosterone achieved pooled sensitivity of **0.89** (95% CI 0.69–0.96) vs. 0.74 (0.63–0.82) for total testosterone in detecting biochemical hyperandrogenism in PCOS, at comparable specificity (0.83 vs. 0.86) [20, meta_analysis]. The AUC for the two methods was similar (0.85 vs. 0.87), but the near-10-point sensitivity advantage means free T catches substantially more cases of androgen excess that total T misses. Rotterdam consensus criteria include FAI > 4 as evidence of biochemical hyperandrogenism.

### Determinants of Free Testosterone

Because free T is the unbound fraction of total T filtered through SHBG, its determinants are the union of total-T drivers and SHBG modulators:

**Raise free T:**
- Exogenous testosterone or anabolic androgens (raise total T, suppress SHBG, doubly increase free fraction)
- hCG stimulation (raises Leydig cell total T output)
- Conditions that suppress SHBG: obesity, insulin resistance, hypothyroidism, glucocorticoids, androgens themselves, growth hormone excess
- Higher LH pulse amplitude and frequency (intact HPG axis in young men)

**Lower free T:**
- Aging: both total T falls (declining Leydig cell mass and LH pulse amplitude) and SHBG rises, compressing the free fraction from both ends
- Opioids, glucocorticoids, chronic illness: suppress HPG axis → lower total T
- Anything raising SHBG (hyperthyroidism, estrogens, oral contraceptives, anticonvulsants, hepatic disease, HIV chronicity) → lower free T without necessarily lowering total T
- Central adiposity and insulin resistance: lowers total T as well, so the net effect on free T depends on the degree of each component

### Clinical Associations: Bone, Function, and Mortality

Several large cohort studies show that free or bioavailable testosterone tracks outcomes more closely than total T when SHBG varies.

**Bone density and fracture:** In MrOS Sweden (n = 2,908 men, mean age 75.4 years), free testosterone below the median was an independent predictor of prevalent osteoporosis-related fractures (OR 1.56; 95% CI 1.14–2.14; p < 0.01) and was significantly associated with cortical bone mineral density at the hip, arm, and total body — even after adjustment for BMD itself [23, cohort]. A smaller cross-sectional study of 83 community-dwelling men aged > 65 years with low bioavailable testosterone found bioavailable T the strongest single predictor of femoral neck BMD, explaining approximately 21% of variance, exceeding contributions of physical activity and BMI [24, cohort].

**Physical function and frailty:** In the Framingham Offspring Study (n = 1,445 men, mean age 61 years), each standard deviation increase in baseline free testosterone was associated with a 22% lower risk of incident mobility limitation and a 25% lower risk of worsening limitation over follow-up [25, cohort]. Free testosterone outperformed total testosterone as a predictor of physical decline.

These associations are observational: they establish that free T tracks clinically relevant outcomes in aging men, but cannot establish causation — low free T may be tracking an underlying disease state rather than causing the adverse outcome. Causal inference requires intervention data; no large RCT has specifically randomized by free T level.

### Limitations

**Method dependence.** Equilibrium dialysis, calculated free T (Vermeulen), and the analog immunoassay return discordant absolute values and cannot share a single reference range. The analog assay systematically underestimates vs. dialysis; the calculated method systematically overestimates; different calculated formulas diverge in edge-population distributions [5, mechanism_review; 14, mechanism_review].

**No harmonised reference range.** Unlike total testosterone, no population-anchored reference range for free T has been established across methods, laboratories, or age/sex strata [6, regulatory; 5, mechanism_review].

**Error propagation.** Calculated free T inherits analytical error from both total T and SHBG assays; imprecision in either input compounds in the calculation. At low concentrations — where the clinical question is often most pressing — percentage error is largest [5, mechanism_review].

**Analog immunoassay persistence.** Despite documented unreliability, the direct analog assay remains widely ordered. Its results should not be used for diagnostic decision-making in the conditions where free T matters most (low and high SHBG extremes).

---

## Bibliography

[1]. Goldman AL, Bhasin S, Wu FCW, Krishna M, Matsumoto AM, Jasuja R. A Reappraisal of Testosterone's Binding in Circulation: Physiological and Clinical Implications. Endocrine Reviews. 2017;38(4):302–324. PMID: 28673039. DOI: 10.1210/er.2017-00025. — tag: mechanism_review — tier: 1

[2]. Bikle DD. The Free Hormone Hypothesis: When, Why, and How to Measure the Free Hormone Levels to Assess Vitamin D, Thyroid, Sex Hormone, and Cortisol Status. JBMR Plus. 2021;5(1):e10418. PMID: 33553985. DOI: 10.1002/jbm4.10418. — tag: mechanism_review — tier: 1

[3]. Laurent MR, Hammond GL, Blokland M, Jardí F, Antonio L, Dubois V, Khalil R, Sterk SS, Gielen E, Decallonne B, Carmeliet G, Kaufman JM, Fiers T, Huhtaniemi IT, Vanderschueren D, Claessens F. Sex hormone-binding globulin regulation of androgen bioactivity in vivo: validation of the free hormone hypothesis. Scientific Reports. 2016;6:35539. PMID: 27748448. DOI: 10.1038/srep35539. — tag: animal — tier: 1

[4]. Rosner W, Auchus RJ, Azziz R, Sluss PM, Raff H. Position statement: Utility, limitations, and pitfalls in measuring testosterone: an Endocrine Society position statement. J Clin Endocrinol Metab. 2007;92(2):405–413. PMID: 17090633. DOI: 10.1210/jc.2006-1864. — tag: regulatory — tier: 2

[5]. Vermeulen A, Verdonck L, Kaufman JM. A Critical Evaluation of Simple Methods for the Estimation of Free Testosterone in Serum. J Clin Endocrinol Metab. 1999;84(10):3666–3672. PMID: 10523012. DOI: 10.1210/jcem.84.10.6079. — tag: mechanism_review — tier: 1

[6]. Bhasin S, Brito JP, Cunningham GR, Hayes FJ, Hodis HN, Matsumoto AM, Snyder PJ, Swerdloff RS, Wu FC, Yialamas MA. Testosterone Therapy in Men With Hypogonadism: An Endocrine Society Clinical Practice Guideline. J Clin Endocrinol Metab. 2018;103(5):1715–1744. PMID: 29562364. DOI: 10.1210/jc.2018-00229. Note: CDC Hormone Standardization Program for Testosterone (HoSt-TT) also referenced in context of harmonization; available at cdc.gov/clinical-standardization-programs. — tag: regulatory — tier: 2

[7]. Nankin HR, Calkins JH. Laboratory Assessment of Testicular Function. In: Feingold KR, et al., eds. Endotext [Internet]. South Dartmouth, MA: MDText.com, Inc.; updated 2019. NCBI Bookshelf NBK279145. — tag: mechanism_review — tier: 2

[8]. Södergård R, Bäckström T, Shanbhag V, Carstensen H. Calculation of free and bound fractions of testosterone and estradiol-17 beta to human plasma proteins at body temperature. J Steroid Biochem. 1982;16(6):801–810. PMID: 7202083. — tag: cohort — tier: 2

[9]. Fritz KS, McKean AJ, Nelson JC, Wilcox RB. Analog-based free testosterone test results linked to total testosterone concentrations, not free testosterone concentrations. Clin Chem. 2008;54(3):512–516. PMID: 18171714. — tag: cohort — tier: 2

[10]. Chen Y, Yazdanpanah M, Hoffman BR, Diamandis EP, Wong PY. Direct measurement of serum free testosterone by ultrafiltration followed by liquid chromatography tandem mass spectrometry. Clin Biochem. 2010;43(4–5):490–496. PMID: 20026023. — tag: cohort — tier: 2

[11]. Travison TG, Zhuang WV, Lunetta KL, et al. Calculated free testosterone in men: comparison of four equations and with free androgen index. Clin Endocrinol (Oxf). 2007;66(5):652–658. PMID: 17036414. — tag: cohort — tier: 2

[12]. Jasuja R, Pencina KM, Spencer DJ, et al. Reference intervals for free testosterone in adult men measured using a standardized equilibrium dialysis procedure. Andrology. 2023;11(1):125–133. DOI: 10.1111/andr.13310. — tag: cohort — tier: 1

[13]. Narinx N, Nyamaah JA, Antonio L, et al. A survey on measurement and reporting of total testosterone, sex hormone-binding globulin and free testosterone in clinical laboratories in Europe. Clin Chem Lab Med. 2025. PMID: 40068942. — tag: cohort — tier: 2

[14]. Fiers T, Wu F, Moghetti P, Vanderschueren D, Lapauw B, Kaufman JM. Reassessing free-testosterone calculation by liquid chromatography–tandem mass spectrometry direct equilibrium dialysis. J Clin Endocrinol Metab. 2018;103(6):2167–2174. PMID: 29618085. — tag: mechanism_review — tier: 1

[15]. Zakharov MN, Bhasin S, Travison TG, Xue R, Ulloor J, Vasan RS, Carter E, Wu F, Jasuja R. A multi-step, dynamic allosteric model of testosterone's binding to sex hormone binding globulin. Mol Cell Endocrinol. 2015;399:190–200. DOI: 10.1016/j.mce.2014.09.001. — tag: mechanism_review — tier: 1

[16]. De Ronde W, van der Schouw YT, Pols HA, et al. Calculation of bioavailable and free testosterone in men: a comparison of 5 published algorithms. Clin Chem. 2006;52(9):1777–1784. PMID: 16793931. — tag: cohort — tier: 2

[17]. Kacker R, Hornstein AM, Morgentaler A. Free testosterone by direct and calculated measurement versus equilibrium dialysis in a clinical population. Aging Male. 2013;16(4):164–168. PMID: 24090209. — tag: cohort — tier: 2

[18]. Winters SJ, Kelley DE, Goodpaster B. The analog free testosterone assay: are the results in men clinically useful? Clin Chem. 1998;44(10):2178–2182. PMID: 9761253. — tag: mechanism_review — tier: 2

[19]. Katzman BM, Lueke AJ, Donato LJ, Jaffe AS, Baumann NA. Prevalence of biotin supplement usage in outpatients and plasma biotin concentrations in patients presenting to the emergency department. Clin Biochem. 2018;60:11–16. Bowen R, Bhargava A, Kinsey A, et al. AACC Guidance Document on Biotin Interference in Laboratory Tests. 2019. — tag: mechanism_review — tier: 2

[20]. Bizuneh AD, Joham AE, Teede H, Mousa A, Earnest A, Hawley JM, Smith L, Azziz R, Arlt W, Tay CT. Evaluating the diagnostic accuracy of androgen measurement in polycystic ovary syndrome: a systematic review and diagnostic meta-analysis to inform evidence-based guidelines. Hum Reprod Update. 2025;31(1):48–63. DOI: 10.1093/humupd/dmae028. — tag: meta_analysis — tier: 1

[21]. Souteiro P, Belo S, Oliveira SC, et al. Insulin resistance and sex hormone-binding globulin are independently correlated with low free testosterone levels in obese males. Andrologia. 2018;50(7):e13035. PMID: 29744905. — tag: cohort — tier: 2

[22]. Pezzaioli LC, Quiros-Roldan E, Paghera S, et al. The importance of SHBG and calculated free testosterone for the diagnosis of symptomatic hypogonadism in HIV-infected men: a single-centre real-life experience. Infection. 2020;49(2):295–303. PMID: 33289905. — tag: cohort — tier: 2

[23]. Mellström D, Johnell O, Ljunggren O, et al. Free testosterone is an independent predictor of BMD and prevalent fractures in elderly men: MrOS Sweden. J Bone Miner Res. 2006;21(4):529–535. PMID: 16598372. — tag: cohort — tier: 2

[24]. Kenny AM, Prestwood KM, Marcello KM, Raisz LG. Determinants of bone density in healthy older men with low testosterone levels. J Gerontol A Biol Sci Med Sci. 2000;55(9):M492–7. PMID: 10995046. — tag: cohort — tier: 2

[25]. Krasnoff JB, Basaria S, Pencina MJ, et al. Free testosterone levels are associated with mobility limitation and physical performance in community-dwelling men: the Framingham Offspring Study. J Clin Endocrinol Metab. 2010;95(6):2790–9. PMID: 20382680. — tag: cohort — tier: 2
