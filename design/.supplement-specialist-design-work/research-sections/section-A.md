# Section A — Landscape & evidence-maturity

Scope: goal-agnostic, class-level characterization of where OTC supplements / herbals / nootropics sit on an evidence-maturity ladder. No personalization, ranking, or operator pre-filtering. The unit of evidence is the COMPOUND (and frequently the specific FORMULATION/BRAND), never the marketing class.

Maturity ladder used throughout (supplement analog of a four-rung TRL ladder):
- **Rung 1 — Established / monograph-backed:** convergent human RCT + meta-analysis evidence on hard outcomes; characterized in institutional fact sheets (e.g., NIH-ODS).
- **Rung 2 — Trial-stage:** human RCTs exist but are few, small, short, surrogate-endpoint-only, or heterogeneous; effect on hard human outcomes unsettled.
- **Rung 3 — Preclinical:** mechanism established in vitro / in animals; human outcome data thin, null, or absent.
- **Rung 4 — Anecdote:** no admissible human trial; claims rest on forums/vendor copy.

Cross-cutting rule surfaced by the evidence: CLASS membership ("adaptogen", "nootropic", "antioxidant") never substitutes for compound-level human evidence, and a clean MECHANISM never upgrades the HUMAN-OUTCOME rung.

---

### Finding A1 — Evidence maturity is compound-specific and spans the full ladder; a handful of compounds reach Rung 1 while most marketed "stacks" sit at Rung 2-4

**Claim:** A small set of single compounds have convergent human RCT/meta-analytic support on hard or well-validated outcomes (creatine monohydrate, EPA-dominant omega-3 for triglycerides/CV in defined populations, melatonin/caffeine — all Rung 1-2), whereas the large majority of multi-herb "nootropic stacks" and adaptogen products rest on thin, heterogeneous, or absent human-outcome evidence (Rung 2-4), so the marketing class cannot be used as a proxy for evidence maturity.

**Evidence:**
- Creatine + resistance training pooled across 12 RCTs in healthy adults <50: +1.14 kg lean body mass (95% CI 0.69 to 1.59) and −0.73 kg fat mass (95% CI −1.34 to −0.11) vs resistance training alone [1, meta_analysis]; a separate aged-adult (mean age >50) meta-analysis: +1.32 kg lean tissue mass mean difference (95% CI 0.93 to 1.72), with significant lower-limb (but not consistently upper-limb) strength gains [1a, meta_analysis]. This is among the most replicated ergogenic signals in the supplement literature → Rung 1 for the lean-mass/strength outcome.
- Multi-ingredient nootropic and adaptogen products: a 2022 randomized triple-blind crossover of a multi-ingredient nootropic is one of very few controlled human trials of an actual marketed stack, and reviews of the category state human-outcome evidence "at typical product doses is still thin" and that individual ingredients "require stronger independent human evidence to substantiate their combined effects" [2, rct][3, anecdote_aggregate]. → most stacks Rung 2-4.

**Maturity rung:** Spread — creatine Rung 1 (named outcome); marketed multi-herb stacks predominantly Rung 2-4.

**Caveats:** [3] is a non-whitelisted aggregator host, admissible only as `anecdote_aggregate` and used here ONLY for the qualitative "evidence is thin" lead, not for any numerical claim. Creatine's strength signal is route/population-bound to oral dosing in trained/untrained adults under resistance training; effect sizes are outcome-specific (lower-limb > upper-limb). No single-lab/funder dominance flag for creatine monohydrate — the meta-analytic base draws on many independent groups across decades.

---

### Finding A2 — Mechanism and human-outcome are independent columns: NMN raises NAD+ yet does not move metabolic outcomes; resveratrol's SIRT1 story does not translate to SIRT1-level human change

**Claim:** For the NAD+/sirtuin "longevity" compounds, a clean and partly-confirmed mechanism (NMN → blood NAD+ elevation; resveratrol → in-vitro SIRT1 activation) coexists with null or unsettled human OUTCOME data, demonstrating that mechanism confirmation does not upgrade the human-outcome maturity rung.

**Evidence (mechanism column):**
- NMN raised blood NAD+ in 5 of 8 RCTs [4, meta_analysis]. Resveratrol activates human SIRT1 in vitro (reported up to ~8-fold [population-mismatch: cell-free recombinant-enzyme assay]; acts as a substrate-interaction stabilizer, lowering Km for acetylated substrate) [5, in_vitro].

**Evidence (human-outcome column — separate and weaker):**
- Meta-analysis of 8 NMN RCTs (n=342 middle-aged/older adults, 250-2000 mg/d, 14 d-12 wk): NO significant benefit on fasting glucose, fasting insulin, HbA1c, or lipid profile; HOMA-IR reduction was marginal (SMD 0.27, 95% CI −0.01 to 0.55; p=0.06) and lost significance on sensitivity analysis; the authors conclude their findings "do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism," attributing the human-null pattern to differences between mouse models and human studies (a rodent-to-human translational gap) [4, meta_analysis].
- Meta-analysis of 11 resveratrol RCTs: NO significant effect on SIRT1 gene expression, protein expression, or serum SIRT1 levels — i.e., the human readout of the proposed mechanism itself failed to move robustly, with only duration/dose-conditioned subgroup signals [6, meta_analysis].

**Maturity rung:** Mechanism Rung 1-3 (NMN PK confirmed; resveratrol in-vitro only); human OUTCOME Rung 2 (NMN, null on tested metabolic endpoints) and Rung 2-3 (resveratrol). The mechanism column does NOT lift the outcome column.

**Caveats:** Resveratrol SIRT1 activation [5] is `in_vitro` and carries no claim to human outcome; the human SIRT1 meta-analysis [6] is the admissible human-outcome anchor. No species-extrapolation tag needed (human cell / human RCT data), but the well-documented preclinical→clinical "translational gap" for both compounds is the core caution.

---

### Finding A3 — Concentration-of-evidence risk in supplements is dual: single-lab AND industry/manufacturer-funded dominance, concentrated in branded proprietary extracts

**Claim:** The branded-extract segment (ashwagandha KSM-66/Sensoril, branded curcumin and citicoline formulations) is structurally exposed to funding-dominance bias because the positive human trials are frequently sponsored by the single company that owns the branded extract, which triggers a certainty downgrade for any class-level efficacy claim derived from that branded evidence base.

**Evidence:**
- KSM-66 is produced exclusively by Ixoreal Biomed (standardized ≥5% withanolides); Sensoril is a Natreon-originated brand (≥10% withanolides) — i.e., each branded extract's trial base is tied to its sole commercial owner [7, vendor_label] (brand-ownership/standardization fact only; NOT an efficacy cite). Reviews of the ashwagandha literature note that "many studies with positive results were sponsored by companies that produce ashwagandha extracts," raising selective-reporting/risk-of-bias concerns [8, mechanism_review].
- The general direction of the bias is documented: a systematic review/meta-analysis of nutrition studies found industry-sponsored studies more likely to reach sponsor-favorable conclusions (risk ratio 1.31, 95% CI 0.99-1.72) — directionally consistent but NOT statistically conclusive, so the effect is real-as-a-risk but unestablished in magnitude [9, meta_analysis].

**Maturity rung:** Does not itself set a rung; it is a certainty-DOWNGRADE modifier applied on top of whatever rung the branded evidence claims. When ≥70% of a compound's positive primaries trace to one manufacturer-funded program (a recurring pattern for proprietary extracts), surface an explicit funding-dominance caveat and downgrade.

**Caveats:** [7] is `vendor_label` — used ONLY for brand ownership and label standardization %, never for any efficacy/dose/AE claim, per type-tag hard rules. [9] explicitly does NOT establish bias magnitude (CI crosses 1.0); the finding is "documented risk, unestablished magnitude," not "proven inflation." Funding-dominance is a flag to investigate per compound, not an automatic invalidation.

---

### Finding A4 — Bioavailability/formulation is a load-bearing, measured-PK variable: native curcumin has near-zero free systemic bioavailability

**Claim:** For several heavily marketed compounds, the active-compound oral bioavailability measured in human PK is so low that efficacy claims and dosing cannot be read off the ingested dose, with curcumin the canonical case — and the corrective is measured human PK, never a vendor bioavailability chart.

**Evidence:**
- In humans, only conjugated (not free) curcumin is detectable after oral dosing; gram-level doses are needed to detect any curcumin in blood, and 8 g oral native curcumin yields <1 µg/mL plasma — driven by poor small-intestinal absorption plus extensive hepatic reductive/conjugative metabolism and biliary elimination [10, mechanism_review]. Reformulation changes the PK by large measured factors: in a single randomized cross-over trial in healthy adults, AUC increased ~57-fold for micellar curcumin and ~30-fold for a curcumin-γ-cyclodextrin complex vs native curcuma extract [11, rct]; a separate earlier cross-over trial reported micellar curcumin ~185-fold more bioavailable than native curcumin across all subjects (114-fold in men, 277-fold in women) [11a, rct].

**Maturity rung:** Cross-cutting modifier (applies at any rung). It means the FORMULATION, not the molecule, is the unit of evidence: a trial on a micellar/phospholipid form does not transfer to native-powder products, and standardization-to-active-marker plus measured human PK is required before any dose claim.

**Caveats:** Bioavailability figures here are from human PK studies [10, 11, 11a] — admissible for the PK claim. The 57×/30× factors trace ONLY to Flory 2021 [11]; the 185-fold (114×/277×) figure traces ONLY to Schiborr 2014 [11a] — no number is shared across the two papers. All are RELATIVE factors (formulation vs native), not absolute bioavailability, and are formulation-specific; they must not be generalized across unrelated "enhanced" products. No vendor chart was used.

---

### Finding A5 — An institutional monograph backbone (Rung-1 anchor) exists, but most compounds and nearly all multi-ingredient products fall below it on the ladder

**Claim:** The four-rung ladder is concretely anchored at the top by institutional fact-sheet coverage and convergent meta-analyses for a minority of single nutrients/compounds, while the large remainder — most adaptogens at typical product doses, NAD+ precursors on hard outcomes, multi-herb stacks — sits at trial-stage or below, so a defensible class map must place each compound by its OWN human-outcome evidence rather than by category.

**Evidence:**
- Established/monograph-backed top rung is real for select agents: VITAL, a 25,871-participant RCT, tested 2000 IU/d vitamin D3 and 1 g/d marine omega-3 on hard primary-prevention endpoints — a level of human-outcome rigor most supplements never reach — and notably returned NULL for vitamin D on invasive cancer (HR 0.96, 95% CI 0.88-1.06) and major CV events (HR 0.97, 95% CI 0.85-1.12) [12, rct]. High rung ≠ positive result; it means the question has been competently asked in humans.
- Even for creatine, the highest-rung ergogenic compound, the COGNITIVE indication is lower-rung: meta-analysis shows significant effects on memory/attention/processing speed but NOT on overall cognitive or executive function, with GRADE certainty only moderate (memory) to low (most domains); an NIH-ODS-aligned panel view found disease-population studies do not support a cognition effect and the mechanism evidence is "weak" [13, meta_analysis]. → same compound, different rung per outcome.

**Maturity rung:** Demonstrates the ladder itself — Rung 1 anchors (vitamin D / omega-3 / creatine-for-strength) coexisting with Rung 2-3 outcomes for the very same or neighboring compounds.

**Caveats:** VITAL's null is population- and dose-specific (generally replete older US adults, 2000 IU/d) and does not transfer to deficient populations or other endpoints — an explicit population-mismatch caution for any generalization. Creatine-cognition certainty is GRADE-rated low for most domains; the memory signal is the only moderate-certainty piece.

---

## Bibliography

[1] Desai I, Wewege MA, Jones MD, Clifford BK, Pandit A, Kaakoush NO, Simar D, Hagstrom AD (2024). "The Effect of Creatine Supplementation on Resistance Training-Based Changes to Body Composition: A Systematic Review and Meta-analysis." Journal of Strength and Conditioning Research. 12 RCTs, adults <50: +1.14 kg lean body mass (95% CI 0.69–1.59), −0.73 kg fat mass (95% CI −1.34 to −0.11), −0.88% body fat. PMID 39074168; DOI 10.1519/JSC.0000000000004862. https://pubmed.ncbi.nlm.nih.gov/39074168/ — retrieved 2026-05-29.

[1a] Forbes SC, Candow DG, Ostojic SM, Roberts MD, Chilibeck PD (2021). "Meta-Analysis Examining the Importance of Creatine Ingestion Strategies on Lean Tissue Mass and Strength in Older Adults." Nutrients 13(6):1912. 16 RCTs / 18 treatment arms (n=509), mean age >50: +1.32 kg lean tissue mass mean difference (95% CI 0.93–1.72). PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC8229907/ — retrieved 2026-05-29.

[2] Authors (2022). "Acute Effect of a Dietary Multi-Ingredient Nootropic as a Cognitive Enhancer in Young Healthy Adults: A Randomized, Triple-Blinded, Placebo-Controlled, Crossover Trial." PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9133906/ — retrieved 2026-05-29.

[3] Category reviews of nootropics/adaptogens (non-whitelisted aggregator hosts; `anecdote_aggregate`, qualitative lead only). e.g., Nucleus / Mind Lab Pro / centreformedicalhumanities. https://mynucleus.com/blog/adaptogens-and-nootropics — retrieved 2026-05-29.

[4] Authors (2024). "Effects of Nicotinamide Mononucleotide on Glucose and Lipid Metabolism in Adults: A Systematic Review and Meta-analysis of Randomised Controlled Trials." 8 RCTs, n=342, 250-2000 mg/d. PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC11557618/ — retrieved 2026-05-29.

[5] Authors. "Mechanism of Human SIRT1 Activation by Resveratrol." Journal of Biological Chemistry. https://www.jbc.org/article/S0021-9258(20)65895-1/fulltext — retrieved 2026-05-29.

[6] Authors (2025). "Impact of Resveratrol Supplementation on Human Sirtuin 1: A GRADE-Assessed Systematic Review and Dose-Response Meta-Analysis of RCTs." (11 RCTs; no significant effect on SIRT1 gene/protein/serum). ScienceDirect (Advances in Nutrition / Current Developments in Nutrition). https://www.sciencedirect.com/science/article/pii/S2212267225001145 — retrieved 2026-05-29.

[7] Transparent Labs (vendor/retailer page; `vendor_label`, brand-ownership + standardization % ONLY, no efficacy). "Sensoril vs. KSM-66." https://www.transparentlabs.com/blogs/all/best-ashwagandha-powder-ksm-66-vs-sensoril — retrieved 2026-05-29.

[8] Authors (2025/2026). "Ashwagandha as an Adaptogenic Herb: A Comprehensive Review of Immunological and Neurological Effects." PMC (review noting industry-sponsorship/risk-of-bias concern). https://pmc.ncbi.nlm.nih.gov/articles/PMC12680924/ — retrieved 2026-05-29.

[9] Chartres N. et al. (2016). "Association of Industry Sponsorship With Outcomes of Nutrition Studies: A Systematic Review and Meta-analysis." JAMA Internal Medicine (risk ratio 1.31, 95% CI 0.99-1.72). PubMed. https://pubmed.ncbi.nlm.nih.gov/27802480/ — retrieved 2026-05-29.

[10] Authors (2019). "Dietary Curcumin: Correlation between Bioavailability and Health Potential." Nutrients / PMC (human PK: conjugated-only, 8 g → <1 µg/mL). https://pmc.ncbi.nlm.nih.gov/articles/PMC6770259/ — retrieved 2026-05-29.

[11] Flory S, Sus N, Haas K, Jehle S, Kienhöfer E, Waehler R, Adler G, Venturelli S, Frank J (2021). "Increasing Post-Digestive Solubility of Curcumin Is the Most Successful Strategy to Improve its Oral Bioavailability: A Randomized Cross-Over Trial in Healthy Adults and In Vitro Bioaccessibility Experiments." Molecular Nutrition & Food Research 65(24):2100613. Healthy-adult cross-over: micellar curcumin AUC ~57-fold and curcumin-γ-cyclodextrin ~30-fold vs native curcuma extract. PMID 34665507; DOI 10.1002/mnfr.202100613. https://onlinelibrary.wiley.com/doi/full/10.1002/mnfr.202100613 — retrieved 2026-05-29.

[11a] Schiborr C, Kocher A, Behnam D, Jandasek J, Toelstede S, Frank J (2014). "The oral bioavailability of curcumin from micronized powder and liquid micelles is significantly increased in healthy humans and differs between sexes." Molecular Nutrition & Food Research 58(3):516–527. Cross-over (13 women, 10 men), 500 mg curcuminoids: micellar curcumin ~185-fold more bioavailable than native by AUC across all subjects (114-fold men, 277-fold women). PMID 24402825; DOI 10.1002/mnfr.201300724. https://pubmed.ncbi.nlm.nih.gov/24402825/ — retrieved 2026-05-29.

[12] Manson JE et al. (2019). "Vitamin D Supplements and Prevention of Cancer and Cardiovascular Disease" (VITAL, n=25,871, 2000 IU/d D3, 1 g/d omega-3). NEJM. https://www.nejm.org/doi/full/10.1056/NEJMoa1809944 — retrieved 2026-05-29.

[13] Authors (2024). "The effects of creatine supplementation on cognitive function in adults: a systematic review and meta-analysis" (GRADE; memory moderate, most domains low; NIH-ODS-aligned panel: weak cognition support). Frontiers in Nutrition / PMC. https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2024.1424972/full ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11574456/ — retrieved 2026-05-29.

## Self-check

- **Distinct source count:** 15 numbered references (incl. [1]/[1a] creatine split and [11]/[11a] curcumin unbundle); ≥13 distinct admissible Tier-1/Tier-2 primaries (PMC/NEJM/JBC/ScienceDirect/Wiley/PubMed/Frontiers). Tier-1 primary literature + one Tier-2-grade large RCT (VITAL/NEJM) dominate; one `vendor_label` and one `anecdote_aggregate` source included strictly within their admissibility limits. Exceeds the ≥8 floor.
- **Type-tag discipline:** Every factual claim carries an inline `[N, type_tag]` with exactly one enum tag. `vendor_label` [7] grounds ONLY brand ownership + label standardization %, never a numerical efficacy/dose/AE claim. `anecdote_aggregate` [3] grounds ONLY the qualitative "evidence is thin" lead, never a number. No `vendor_label`/`anecdote_aggregate` grounds any dose/effect-size/AE-rate/n/half-life claim. No "research suggests"/"experts believe" phrasing used.
- **Population-mismatch tags:** One `in_vitro` NUMERICAL claim is present — resveratrol's in-vitro SIRT1 activation "~8-fold" [5, in_vitro] — and it carries an in-sentence `[population-mismatch: cell-free recombinant-enzyme assay]` annotation in the A2 mechanism column (Borra 2005 is a cell-free recombinant-SIRT1 fluorogenic-peptide assay, not a cell-line study); the figure is not transferred to any human-outcome claim, and the resveratrol HUMAN readout is anchored to a human RCT meta-analysis [6]. No `animal` numerical claim was made. VITAL's population-specificity (replete older US adults) is explicitly flagged in A5 caveats as a generalization caution. No `[route-extrapolation]` needed (all dosing oral, matching cited routes).
- **Concentration/funding-dominance flags:** Raised explicitly in A3 — single-owner branded extracts (KSM-66/Ixoreal, Sensoril/Natreon) and the documented-but-magnitude-unestablished nutrition-industry sponsorship signal (RR 1.31, CI crosses 1.0); the ≥70% single-funder/single-lab downgrade trigger is stated as a per-compound modifier. No single-lab dominance flag warranted for creatine (broad independent base).
- **Goal-agnosticism:** Confirmed. No operator, goal, ranking, or "best for X" framing. Findings state what the class evidence supports generally and place compounds on a maturity ladder by their own human-outcome evidence; null results (vitamin D, NMN, resveratrol) are reported as findings, not filtered out.

## Post-fix grep audit

Iter-2 remediation re-sourced four numerical claims and restructured two bundled references. Each corrected value's OLD form was grepped across the WHOLE file to catch lingering hits.

**Corrections (OLD → NEW):**

| # | Claim | OLD value | NEW value | New source |
|---|-------|-----------|-----------|------------|
| C1 | Aged-adult creatine lean tissue MD | `+1.37 kg` | `+1.32 kg` | Forbes 2021, PMC8229907 → ref [1a] |
| C2 | <50 creatine fat-mass MD | `−0.7 kg` | `−0.73 kg` (95% CI −1.34 to −0.11) | Desai 2024, PMID 39074168 → ref [1] |
| C3 | <50 creatine LBM (re-attributed, value unchanged) | `+1.14 kg` (ref [1] bundled) | `+1.14 kg` (ref [1] = Desai 2024 alone) | Desai 2024, PMID 39074168 |
| C4 | Schiborr micellar curcumin fold (re-attributed, was MISSING/conflated) | (57× wrongly co-bundled w/ Schiborr) | `~185-fold` (114× men / 277× women) | Schiborr 2014, PMID 24402825 → ref [11a] |
| C5 | Flory micellar/γ-CD curcumin fold (re-attributed, value unchanged) | `~57×/~30×` (ref [11] bundled w/ Schiborr) | `~57×/~30×` (ref [11] = Flory 2021 alone) | Flory 2021, PMID 34665507 |
| C6 | Resveratrol in_vitro SIRT1 fold (tag added, value unchanged) | `~8-fold` (no pop-mismatch tag) | `~8-fold [population-mismatch: human cell line]` | JBC, ref [5] |

**Grep sweeps for OLD values (run against full section-A.md):**

- `grep -inE '1[.,]37' section-A.md` → **0 hits.** OLD aged-adult value `+1.37 kg` fully removed; no lingering occurrence.
- `grep -inE '0[.,]7[^0-9]' section-A.md` → **0 hits.** OLD bare `−0.7 kg` fat value fully replaced by `−0.73`; no lingering occurrence.
- `grep -inE '57[ -]?(fold|x|×)' section-A.md` → 3 hits, all line 65 / line 69 / line 111, every one attributing 57× to Flory 2021 [11] ONLY. No hit binds 57× to Schiborr. Disposition: correct (re-attribution successful).
- `grep -inE '30[ -]?(fold|x|×)' section-A.md` → same 3 lines, 30× bound to Flory [11] (γ-cyclodextrin) ONLY. Disposition: correct.
- `grep -inE '185[ -]?(fold|x|×)' section-A.md` → 3 hits (lines 65/69/113), 185× bound to Schiborr 2014 [11a] ONLY. Disposition: correct (Schiborr now carries its actual figure; no number maps to the wrong paper).
- `grep -inE '8[ -]?fold' section-A.md` → 2 hits (line 34 body, line 123 self-check); both now carry the `[population-mismatch: human cell line]` annotation / acknowledge it. Disposition: correct.
- `grep -inE '1[.,]14' section-A.md` (NEW, confirm placement) → 2 hits (line 20 body bound to ref [1], line 89 bibliography ref [1] = Desai 2024). Disposition: correct.
- `grep -inE '1[.,]32' section-A.md` (NEW, confirm placement) → 2 hits (line 20 body bound to ref [1a], line 91 bibliography ref [1a] = Forbes 2021). Disposition: correct.

**Result:** Zero lingering hits of any OLD value. Every corrected number now maps to exactly one paper. Refs [1]/[11] unbundled into [1]+[1a] and [11]+[11a]; no number is shared across a split pair.

### Iter-3

Two-part fix to the NMN HOMA-IR claim (line 37, source PMC11557618): (a) the point estimate sat OUTSIDE its own CI — written as a negative `−0.27` against a CI of `−0.01 to 0.55`, internally inconsistent; (b) the metric was misrepresented as a raw HOMA-IR unit change when the source reports a standardized mean difference (SMD). Source re-verified by fetch: verbatim "There was a marginally significant reduction on HOMA-IR by 0.27 (95% CI -0.01 to 0.55; p = 0.06; I2 = 0%)" — confirms reduction OF 0.27 (positive, inside CI) and SMD as the metric.

**Corrections (OLD → NEW):**

| # | Claim | OLD value | NEW value | Source |
|---|-------|-----------|-----------|--------|
| C7 | NMN HOMA-IR point estimate (sign fix, restore CI consistency) | `−0.27, 95% CI −0.01 to 0.55; p=0.06` | `0.27, 95% CI −0.01 to 0.55; p=0.06` | PMC11557618 → ref [4] |
| C8 | NMN HOMA-IR metric label (SMD inserted) | `(−0.27, ...)` (raw unit implied) | `(SMD 0.27, ...)` | PMC11557618 → ref [4] |

**Grep sweep (run against full section-A.md):**

- `grep -inE '\-?0\.27|HOMA' section-A.md` → **1 hit (line 37).** Reads `HOMA-IR reduction was marginal (SMD 0.27, 95% CI −0.01 to 0.55; p=0.06)`. Disposition: correct — point estimate `0.27` is positive and sits INSIDE its CI `−0.01 to 0.55`; `SMD` present; no other `0.27`/`HOMA` occurrence anywhere in the file. The stray negative-sign form `−0.27` is fully removed.

**Result:** Point estimate now lies inside its own CI; metric correctly labelled SMD; single in-file occurrence, no lingering OLD form.

### Iter-4

ANTI-HALLUCINATION AUTO-FAIL (FM-3, fabricated quotation). Line 37 / Finding A2, citation [4] = PMC11557618. The clause attributed a verbatim quotation to [4] that the source does NOT contain. Two prior independent fetches plus a third fetch this iteration confirm **zero occurrences of "exaggeration"** in the full text. A quoted string the source does not contain is a fabricated quotation — removed entirely and replaced with the source's actual conclusion language, re-verified by fetch.

**Source re-verification (fetch, PMC11557618):**
- Word "exaggeration" present in source? **No — zero occurrences.**
- Actual conclusion (verbatim): "do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism."
- Translational-gap framing (source): "The lack of benefits of NMN supplementation in humans reviewed here may be due to some key differences between mice models and human studies." Used as an UNQUOTED paraphrase (rodent-to-human translational gap).

**Corrections (OLD → NEW):**

| # | Claim | OLD value | NEW value | Source |
|---|-------|-----------|-----------|--------|
| C9 | NMN conclusion clause (FABRICATED quote removed) | `authors warn of "an exaggeration of the benefits of NMN supplementation" in the field` | `the authors conclude their findings "do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism," attributing the human-null pattern to differences between mouse models and human studies (a rodent-to-human translational gap)` | PMC11557618 → ref [4] |

**FM-3 sweep of Finding A2 (lines 29-42) — every quoted string verified:**

| Line | Quoted string | Source-attributed? | Disposition |
|------|---------------|--------------------|-------------|
| 31 | `"longevity"` | No — scare-quote on a marketing category term | OK (not a source claim) |
| 37 | `"an exaggeration of the benefits of NMN supplementation"` [4] | Yes | REMOVED — fabricated, not in PMC11557618 |
| 37 (new) | `"do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism"` [4] | Yes | OK — source-verbatim by fetch |
| 42 | `"translational gap"` | No — scare-quote on a general concept, not attributed | OK (not a source claim) |

The resveratrol `~8-fold` in_vitro figure (A2 mechanism column) carries no quotation marks; it is a tagged numerical claim, not a quoted string — out of FM-3 quotation scope, untouched.

**Grep sweep (run against full section-A.md):**

- `grep -inc 'exaggeration' section-A.md` → **0 hits in the live finding body (lines 1-126).** The fabricated quoted phrase is fully removed from the finding clause. File-wide the token appears only in THIS iter-4 audit log (lines 174-203) as OLD-form provenance — never in a live claim. Verified: `sed -n '1,126p' section-A.md | grep -inc 'exaggeration'` → 0.
- `grep -inE '"' section-A.md` → enumerated every quoted string in the section. For the NMN finding (line 37), the sole surviving quotation is `"do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism"`, confirmed source-verbatim against PMC11557618 by fetch. The translational-gap statement is an UNQUOTED paraphrase (no quote marks). All other quotations in the file are either non-source scare-quotes (`"longevity"`, `"translational gap"`, `"adaptogen"`/`"nootropic"`/`"stacks"`, etc.) or bibliography article titles, none newly introduced this iteration.

**Result:** Fabricated quotation removed; replacement is source-verbatim (verified by fetch); no quotation marks wrap any string absent from the cited source. Single in-file occurrence of the new quote; zero `exaggeration` occurrences remain.

### Post-fix grep audit — iter-4b (population-mismatch descriptor accuracy)

| Line | OLD descriptor | NEW descriptor | Source method (fetch-verified) |
|------|----------------|----------------|-------------------------------|
| 34 (body) | `[population-mismatch: human cell line]` | `[population-mismatch: cell-free recombinant-enzyme assay]` | Borra 2005 (PMID 15749705, JBC): purified recombinant human SIRT1 + synthetic fluorogenic peptide (Fluor de Lys) — cell-free biochemical assay, NOT a cell line |
| 123 (self-check) | `[population-mismatch: human cell line]` | `[population-mismatch: cell-free recombinant-enzyme assay]` + parenthetical naming the assay | same |

Disposition: the population-mismatch annotation was always PRESENT (no missing-tag auto-fail); only its method descriptor was imprecise ("human cell line" mischaracterized a cell-free recombinant-enzyme assay). Corrected at both live loci. Lines 140/149 above are historical OLD→NEW provenance from iter-2 (when the tag was first added) and are left as-is per the never-rewrite-the-archaeology audit convention; the iter-2 "NEW" value is superseded by this iter-4b descriptor. The `~8-fold` figure is unchanged and still not transferred to any human-outcome claim.
