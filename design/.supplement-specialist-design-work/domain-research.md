# Supplement-Specialist Domain Research (Pass-3, deep mode)

Provenance: deep-mode `aplus-research` run. Five validated section drafts (A landscape & evidence-maturity; B safety hazards; C regulatory + contract-mapping; D prescribing-practice; E non-English literature) were each produced by a paired retrieve+judge dispatch and judged at deep-99; gates 2.75 (scope), 3.5 (judge), 4.25 (population-mismatch), and 4.75 (integrity) PASS, integrity-verified, with the Phase-6 critique pending. This file is a CORPUS-READ-ONLY synthesis: no new retrieval was performed, no claim is invented, and every numerical claim carried forward retains its section type-tag and any `[population-mismatch: <species/method>]` / concentration / funding / language-dominance caveat verbatim. IC-1 normalization (Phase-4.75 WARN) is applied here: section-C's contract-inheritance references to in-repo DESIGN SURFACES render as plain design-surface references (file path + section), NOT literature type-tags, and section-D's `regulatory-derived`/`regulatory-registry` descriptors are normalized to `regulatory` or restated. Every literature claim keeps exactly one enum type-tag.

---

## Executive Summary

A supplement-specialist medical agent must be, above all, an **evidence-maturity discriminator and an adulteration/interaction circuit-breaker** — not a supplement enthusiast with a dose chart. The load-bearing thesis across the five validated sections is that OTC supplements, herbals, and nootropics stratify by **evidence maturity, not by marketing class**: a handful of single compounds (creatine for strength, EPA-omega-3, vitamin D — the compounds the findings below actually carry) reach the established/monograph-backed rung while the large majority of adaptogens, NAD+ precursors on hard outcomes, and multi-ingredient "stacks" sit at trial-stage or below, and a clean mechanism never upgrades a thin human-outcome rung. The signature domain hazards are distinct from the inherent-pharmacology hazards: **adulteration/contamination** (undeclared pharmaceuticals — sildenafil, sibutramine, synthetic steroids, novel stimulants — is the category's signature hazard), **toxicity ceilings** (fat-soluble vitamins, B6 neuropathy, mineral ULs where "more is worse"), and **herb-/supplement-drug interactions** (St John's Wort CYP3A4/P-gp induction, additive bleeding, serotonergic stacking). The regulatory frame is **DSHEA post-market-only**: FDA does NOT pre-approve supplements; "natural," "GRAS," "NDI-notified," "structure/function," and "third-party-tested" are each distinct from "approved / proven / safe," and conflating them is the laundering hazard. This synthesis carries **15 Findings** (consolidating sections A-E plus the inherited agent-design contract pack) and **18 Recommendations** that become the design-doc §3 directive list. The single highest-leverage risk is **status-laundering compounded by the adulteration base rate** — a sycophantic agent reading "natural supplement" as "safe and unregulated-but-fine" is exactly the failure that the mandatory AUTHORITY_FRAMING_BYPASS refusal class, the DSHEA status-disambiguation card, and the adulteration/third-party-testing surfacing exist to break.

---

## §0 Introduction

**Research question.** What goal-agnostic domain knowledge — evidence maturity, safety hazards, regulatory status, prescribing/use conventions, non-English literature structure, and inherited agent-design contracts — must ground the design of a `supplement-specialist` medical sub-agent that produces vetted, class-level supplement/herbal/nootropic knowledge and performs personalized compound reasoning under the a-plus-maxing safety architecture?

**Scope.** Five domains were researched as goal-agnostic library knowledge (supplements as therapeutic classes, NOT pre-filtered for operator Walter): (A) landscape & evidence-maturity, (B) safety hazards, (C) regulatory + agent contract-mapping, (D) prescribing-practice convention-vs-trial, (E) non-English literature. Section-D agent-design conclusions are grounded against named in-repo contract/design surfaces rather than external evidence.

**Methodology.** Five paired retrieval+judge dispatches were run at `deep` mode (supplement-specialist `risk_class: compound-experimental-or-medium`, mode floor `deep`), each iterated to a judge PASS of 99/100. This document preserves, never re-derives, the section type-tags and population-mismatch annotations. No new numbers are introduced.

---

## Findings

### Finding F1 — OTC supplements stratify by EVIDENCE MATURITY, not by marketing class; class membership never substitutes for compound-level human evidence

**Claim.** A supplement's marketing class ("adaptogen," "nootropic," "antioxidant") tells you nothing about whether the specific compound has convergent human-outcome evidence; the agent must locate every compound on a four-rung maturity ladder (established/monograph-backed → trial-stage → preclinical → anecdote) by its OWN human-outcome data before reasoning about it.

**Evidence.** A small set of single compounds reach the top rung: creatine + resistance training pooled across 12 RCTs in healthy adults <50 gives +1.14 kg lean body mass (95% CI 0.69 to 1.59) and −0.73 kg fat mass (95% CI −1.34 to −0.11) [1, meta_analysis]; an aged-adult (mean age >50) meta-analysis: +1.32 kg lean tissue mass (95% CI 0.93 to 1.72) [2, meta_analysis] — one of the most replicated ergogenic signals (Rung 1, lean-mass/strength outcome). By contrast multi-ingredient nootropic and adaptogen products rest on thin/heterogeneous/absent human-outcome evidence: a 2022 randomized triple-blind crossover is one of very few controlled trials of a marketed stack [3, rct], and category reviews state human-outcome evidence "at typical product doses is still thin" [4, anecdote_aggregate] (qualitative lead only, no number). Most marketed stacks therefore sit Rung 2-4.

**Maturity rung.** Spread — creatine Rung 1 (named outcome); marketed multi-herb stacks predominantly Rung 2-4. Same compound differs per outcome: creatine's COGNITIVE indication is GRADE moderate (memory) to low (most domains), lower than its strength rung [16, meta_analysis].

**Caveats.** [4] is a non-whitelisted aggregator, admissible only as `anecdote_aggregate` for the qualitative lead, not any number. Creatine's strength signal is route/population-bound (oral, trained/untrained adults under resistance training; lower-limb > upper-limb). No single-lab/funder dominance flag for creatine monohydrate (broad independent base).

→ consumes: Identity (agent IS a maturity discriminator) / Core Rules (per-compound `maturity_rung` mandatory) / Anti-Patterns (class membership as a credibility proxy) / Edge Cases (same compound, different rung per outcome).

---

### Finding F2 — Mechanism and human-outcome are independent columns; a confirmed mechanism never upgrades the human-outcome rung

**Claim.** For the NAD+/sirtuin "longevity" compounds, a clean and partly-confirmed mechanism coexists with null or unsettled human OUTCOME data, demonstrating that mechanism confirmation does not lift the human-outcome maturity rung; the agent must hold two columns per compound.

**Evidence (mechanism column).** NMN raised blood NAD+ in 5 of 8 RCTs [5, meta_analysis]. Resveratrol activates human SIRT1 in vitro (reported up to ~8-fold [population-mismatch: cell-free recombinant-enzyme assay]; lowers Km for acetylated substrate) [6, in_vitro].

**Evidence (human-outcome column — separate and weaker).** Meta-analysis of 8 NMN RCTs (n=342 middle-aged/older, 250-2000 mg/d, 14 d-12 wk): NO significant benefit on fasting glucose, fasting insulin, HbA1c, or lipids; HOMA-IR reduction marginal (SMD 0.27, 95% CI −0.01 to 0.55; p=0.06) and lost significance on sensitivity analysis; authors conclude findings "do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism," attributing the human-null pattern to mouse-vs-human differences (a rodent-to-human translational gap) [5, meta_analysis]. Meta-analysis of 11 resveratrol RCTs: NO significant effect on SIRT1 gene/protein/serum levels — the human readout of the proposed mechanism itself failed to move robustly [7, meta_analysis].

**Maturity rung.** Mechanism Rung 1-3; human OUTCOME Rung 2 (NMN, null on tested endpoints) / 2-3 (resveratrol). The mechanism column does NOT lift the outcome column.

**Caveats.** Resveratrol SIRT1 activation [6] is `in_vitro` and carries no claim to human outcome; the human SIRT1 meta-analysis [7] is the admissible human anchor. The preclinical→clinical translational gap is the core caution.

→ consumes: Identity / Core Rules (two-column mechanism/outcome discipline) / Anti-Patterns (mechanism-as-efficacy).

---

### Finding F3 — Concentration-of-evidence is dual: single-lab AND industry/manufacturer-funded dominance, concentrated in branded proprietary extracts

**Claim.** The branded-extract segment (ashwagandha KSM-66/Sensoril, branded curcumin and citicoline) is structurally exposed to funding-dominance bias because the positive human trials are frequently sponsored by the single company that owns the branded extract, triggering a certainty downgrade for any class-level efficacy claim derived from that branded base.

**Evidence.** KSM-66 is produced exclusively by Ixoreal Biomed (≥5% withanolides); Sensoril is Natreon-originated (≥10% withanolides) — each branded extract's trial base is tied to its sole commercial owner [8, vendor_label] (brand-ownership/standardization fact ONLY, not efficacy). Reviews note "many studies with positive results were sponsored by companies that produce ashwagandha extracts," raising selective-reporting concerns [9, mechanism_review]. Directionally, a systematic review/meta-analysis of nutrition studies found industry-sponsored studies more likely to reach sponsor-favorable conclusions (risk ratio 1.31, 95% CI 0.99-1.72) — real-as-a-risk but magnitude unestablished (CI crosses 1.0) [10, meta_analysis].

**risk_tier implied.** Not itself a rung; a certainty-DOWNGRADE modifier. When ≥70% of a compound's positive primaries trace to one manufacturer-funded program (recurring for proprietary extracts), surface an explicit funding-dominance caveat and downgrade.

**Caveats.** [8] is `vendor_label` — brand ownership + standardization % only, never efficacy/dose/AE. [10] does NOT establish magnitude; "documented risk, unestablished magnitude," not "proven inflation." Funding-dominance is a per-compound flag to investigate, not automatic invalidation.

→ consumes: Core Rules (mandatory concentration/funding-dominance check) / Tools (concentration-audit gate on aplus-research returns) / Anti-Patterns (counting one funder's many papers as a strong base).

---

### Finding F4 — Bioavailability/formulation is a load-bearing measured-PK variable; native curcumin has near-zero free systemic bioavailability and the FORMULATION, not the molecule, is the unit of evidence

**Claim.** For several heavily marketed compounds the active-compound oral bioavailability measured in human PK is so low that efficacy and dosing cannot be read off the ingested dose; curcumin is canonical, and the corrective is measured human PK, never a vendor bioavailability chart.

**Evidence.** In humans only conjugated (not free) curcumin is detectable after oral dosing; 8 g oral native curcumin yields <1 µg/mL plasma — poor small-intestinal absorption plus hepatic conjugative metabolism and biliary elimination [11, mechanism_review]. Reformulation changes PK by large measured factors: a randomized cross-over in healthy adults found AUC increased ~57-fold for micellar curcumin and ~30-fold for curcumin-γ-cyclodextrin vs native curcuma extract [12, rct]; a separate earlier cross-over reported micellar curcumin ~185-fold more bioavailable than native (114-fold men, 277-fold women) [13, rct].

**Maturity rung.** Cross-cutting modifier (any rung). A trial on a micellar/phospholipid form does NOT transfer to native-powder products; standardization-to-active-marker plus measured human PK is required before any dose claim.

**Caveats.** The 57×/30× factors trace ONLY to ref [12]; the 185-fold (114×/277×) figure traces ONLY to ref [13] — no number is shared across the two papers. All are RELATIVE factors (formulation vs native), formulation-specific, not absolute bioavailability, and must not be generalized across unrelated "enhanced" products. No vendor chart used.

→ consumes: Core Rules (formulation/measured-PK is load-bearing; reject vendor bioavailability charts) / Tools (formulation-specificity check) / Anti-Patterns (transferring an enhanced-form trial to a native-powder product).

---

### Finding F5 — A four-rung maturity ladder anchored by an institutional monograph backbone exists, but most compounds and nearly all multi-ingredient products fall below it

**Claim.** The ladder is anchored at the top by institutional fact-sheet coverage and convergent meta-analyses for a minority of single nutrients, while most adaptogens, NAD+ precursors on hard outcomes, and multi-herb stacks sit at trial-stage or below; a defensible class map places each compound by its OWN human-outcome evidence, and a high rung means the question was competently asked in humans, NOT that the result was positive.

**Evidence.** VITAL, a 25,871-participant RCT, tested 2000 IU/d vitamin D3 and 1 g/d marine omega-3 on hard primary-prevention endpoints and returned NULL for vitamin D on invasive cancer (HR 0.96, 95% CI 0.88-1.06) and major CV events (HR 0.97, 95% CI 0.85-1.12) [14, rct] — high rung ≠ positive result. Even creatine's COGNITIVE indication is lower-rung than its strength rung: significant effects on memory/attention/processing speed but NOT overall cognitive/executive function, GRADE moderate (memory) to low (most domains); an NIH-ODS-aligned panel found disease-population studies do not support a cognition effect and the mechanism evidence is "weak" [16, meta_analysis].

**Maturity rung.** Demonstrates the ladder itself — Rung 1 anchors (vitamin D / omega-3 / creatine-for-strength) coexisting with Rung 2-3 outcomes for the same or neighboring compounds. Monograph backbone (NIH-ODS fact sheets) is the Rung-1 institutional anchor.

**Caveats.** VITAL's null is population- and dose-specific (generally replete older US adults, 2000 IU/d) and does NOT transfer to deficient populations or other endpoints — an explicit population-mismatch caution for any generalization.

→ consumes: Identity (maturity ladder + monograph backbone) / Core Rules (place each compound by own human-outcome evidence; high rung ≠ positive) / Edge Cases (population-specific null does not generalize).

---

### Finding F6 — Fat-soluble vitamins, B6, and trace minerals have hard toxicity ceilings ("more is worse") codified as IOM/NIH/EFSA Tolerable Upper Intake Levels

**Claim.** Several common supplement nutrients carry established Tolerable Upper Intake Levels (ULs) above which harm rises, and the OTC supplement format is the dominant route to exceeding them; the agent must encode a UL/toxicity-ceiling gate.

**Evidence.** Preformed vitamin A UL is 3,000 mcg RAE/day adults, teratogenicity the critical effect (provitamin A carotenoids NOT teratogenic) [17, regulatory]; vitamin D UL is 100 mcg (4,000 IU)/day, toxicity as hypercalcemia/hypercalciuria/renal failure/soft-tissue calcification/arrhythmia [18, regulatory]; selenium UL 400 mcg/day (selenosis) [19, regulatory]; zinc UL 40 mg/day, ≥50 mg/day over weeks inhibits copper absorption and lowers HDL [20, regulatory]; iron UL 45 mg/day adults [21, regulatory]. Vitamin B6 (pyridoxine) causes dose-/duration-dependent sensory neuropathy: IOM adult UL 100 mg/day, but chronic 1-6 g/day for 12-40 months causes severe progressive sensory neuropathy [22, regulatory], and the 2023 EFSA panel lowered the UL to 12 mg/day [23, regulatory] — an 8-fold IOM-vs-EFSA divergence putting many "high-potency B-complex" products in a contested zone. Dose-response detail: in a 3-year RCT of vitamin-D-replete adults (Billington 2020, Calgary, n=373) hypercalcemia occurred in 0%/3%/9% and hypercalciuria in 17%/22%/31% at 400/4,000/10,000 IU/day [24, rct].

**risk_tier implied.** medium (deterministic, dose-dependent, avoidable with label literacy; high at the tail — vitamin A teratogenicity, vitamin D hypercalcemia, B6 neuropathy are serious and the UL is easy to exceed with concentrated OTC products).

**Caveats.** ULs are intake ceilings, not toxicity thresholds — onset is individual and time-integrated. ULs are also life-stage-conditional: pregnancy and age modulate the relevant ceiling (vitamin A's teratogenicity-driven threshold is the canonical pregnancy-specific case, and several mineral ULs differ by life stage), so a single adult number must not be read as universal. Iron's hazard is two distinct concerns, not one: an ACUTE pediatric-overdose hazard (accidental single-bolus ingestion of adult iron products by children) versus the CHRONIC adult UL/overload concern the 45 mg/day ceiling [21] addresses — the agent must not collapse the acute-poisoning and chronic-ceiling framings. The zinc-copper antagonism is the canonical "one supplement depletes another nutrient" mechanism. The IOM-100 vs EFSA-12 B6 UL is a live contradiction worth logging to `vault/meta/contradictions.md`; B6 reversibility is typical but not universal. Where IOM and EFSA diverge, cite both and flag the divergence.

→ consumes: Core Rules (UL/toxicity-ceiling gate) / Anti-Patterns ("more is better" for fat-soluble vitamins/minerals) / Edge Cases (high-potency B-complex; nutrient-depletes-nutrient antagonism) / Tools (contradiction logging on diverging ULs).

---

### Finding F7 — Herbal/botanical hepatotoxicity is a recurring idiosyncratic class hazard at LABEL doses: green tea extract (EGCG), kava, ashwagandha, sustained-release niacin

**Claim.** Multiple popular botanicals and high-dose vitamins are documented causes of clinically apparent drug-induced liver injury (DILI) in LiverTox, several at label-recommended (not overdose) doses; the agent must carry hepatotoxicity as a class hazard with a pharmacogenomic component.

**Evidence.** Green tea extract DILI is linked to EGCG ~140-1,000 mg/day, is hepatocellular, fatal in ~9% of confirmed cases, and is strongly HLA-B*35:01-associated (72% of confirmed cases carry the allele vs 5-15% population) [25, mechanism_review]; kava is associated with hepatitis/cirrhosis/liver failure with ≥9 published cases plus unpublished German-agency reports including 1 death and 3 transplants, prompting a 2002 FDA advisory and multi-country bans [26, mechanism_review]; ashwagandha causes cholestatic/mixed injury 2-12 weeks after initiation with rare fatal/transplant outcomes, especially in pre-existing liver disease [27, mechanism_review]; sustained-release niacin at high lipid-lowering doses causes acute hepatic necrosis more frequently than immediate-release at equivalent lipid effect [28, mechanism_review].

**risk_tier implied.** high (idiosyncratic, partly unpredictable, can be fatal or require transplant; GTE and ashwagandha injuries occur at label-recommended doses).

**Caveats.** Most botanical DILI is idiosyncratic/low-incidence relative to exposure, not dose-deterministic. The HLA-B*35:01 association makes GTE risk partly pharmacogenomic. Kava hepatotoxicity is confounded by extract solvent/plant-part/species ("ill-defined herbal identity"). Ashwagandha case attribution is partly confounded by the contamination/mislabeling base rate (F9) — some "ashwagandha" liver-injury products were polyherbal or adulterated. EGCG and niacin numbers are human case/RCT-level, not animal extrapolation.

→ consumes: Core Rules (hepatotoxicity class hazard; label-dose injury) / Anti-Patterns (treating "at label dose" as proof of liver safety) / Edge Cases (pre-existing liver disease; HLA-B*35:01 pharmacogenomic risk).

---

### Finding F8 — Herb-/supplement-drug interactions are clinically consequential: St John's Wort CYP3A4/P-gp induction, serotonergic stacking, additive bleeding

**Claim.** OTC botanicals interact with prescription drugs through pharmacokinetic and pharmacodynamic mechanisms; the agent must run an interaction-screen, with St John's Wort the canonical inducer.

**Evidence.** Via hyperforin-driven PXR activation, St John's Wort induces CYP3A4 and P-glycoprotein, lowering plasma levels of cyclosporine, tacrolimus, HIV protease/NNRTI agents, irinotecan, imatinib, warfarin, digoxin, and oral contraceptives, with induction magnitude correlating with product hyperforin content [29, mechanism_review]. Pharmacodynamically, SJW and other serotonergic agents added to SSRIs/SNRIs can precipitate serotonin syndrome [30, mechanism_review]. Additive bleeding risk arises when antiplatelet/anticoagulant-affecting supplements (ginkgo, garlic, vitamin E, ginger, fish oil) combine with warfarin or surgery, though controlled-trial evidence is weaker than the case-report signal [31, cohort].

**risk_tier implied.** high (SJW induction can cause transplant rejection, contraceptive failure, HIV-regimen failure; serotonin syndrome is potentially life-threatening; additive bleeding is medium and more contested).

**Caveats.** SJW induction magnitude is hyperforin-dependent — low-hyperforin extracts induce less, so product-to-product variability is large. The additive-bleeding signal is dominated by case reports (often null in controlled ginkgo+warfarin studies); certainty is downgraded and labeled `cohort`/case-level. 5-HTP/L-tryptophan serotonergic stacking is mechanistically plausible (1989 L-tryptophan EMS outbreak was contamination-driven) but no confirmed human 5-HTP-monotherapy serotonin-syndrome case was found — flag as theoretical for 5-HTP specifically while SJW + SSRI is documented.

→ consumes: Core Rules (mandatory interaction-screen) / Tools (drug-interaction surfacing) / Anti-Patterns (treating a botanical as inert against an Rx regimen) / Edge Cases (transplant/HIV/contraceptive/warfarin context; hyperforin-content variability).

---

### Finding F9 — Adulteration/contamination is the category SIGNATURE hazard; third-party testing is the mitigation; "natural ≠ safe / not FDA pre-market-approved" is the frame

**Claim.** The defining, supplement-specific hazard is that products marketed as "natural" dietary supplements contain undeclared, unapproved pharmaceuticals — distinct from inherent-ingredient hazards — and the agent must surface this base rate plus third-party batch certification as mitigation.

**Evidence.** An FDA-warning analysis (2007-2016) found unapproved pharmaceutical ingredients in 776 supplements, dominated by sildenafil in sexual-enhancement products (47.0%, 166/353), sibutramine in weight-loss products (84.9%, 269/317), and synthetic steroids in muscle-building products (89.1%, 82/92), with 20.2% (157) containing >1 undeclared drug [32, cohort]. Novel/prohibited stimulants persist after FDA action: of 12 supplements purchased in 2017 post-enforcement, 75% (9/12) contained ≥1 of four prohibited DMAA/DMHA-class stimulants and 50% contained ≥2 [33, cohort]. Single-ingredient herbal products show species substitution/contamination on DNA barcoding — 4/20 online single-ingredient products did not match the labeled species [34, cohort]. Mitigation: NSF Certified for Sport screens for 280 banned substances and is the only program recognized by USADA/MLB/NHL/CFL; USP Verified audits manufacturing + lab-tests label conformance; Informed-Sport tests every batch [35, regulatory].

**Frame.** US dietary supplements are NOT FDA pre-market-approved for safety or efficacy; "natural" does not entail safe, and contents frequently diverge from labels [32, cohort][34, cohort].

**risk_tier implied.** high (undeclared sildenafil/sibutramine/steroids/novel stimulants carry direct cardiovascular and pharmacologic harm to an unwitting consumer; the hazard most unique to the category).

**Caveats.** Adulteration prevalence is highest in three "high-risk intent" categories (sexual enhancement, weight loss, muscle building) — base rates for a single-ingredient USP-verified vitamin are far lower; do NOT over-generalize the 47-89% figures. The flagship 2013 DNA-barcoding paper ("30/44 substitution") is RETRACTED — the substitution phenomenon is real and replicated, but that specific figure must not be cited. Certification mitigates but does not eliminate risk (voluntary, sampling-based for some programs). A THIRD contamination mode sits alongside undeclared-drug-spiking and botanical species-mislabeling: heavy-metal contamination (lead/arsenic/cadmium/mercury, classically in botanicals and imported traditional remedies), which needs yet another detection method again distinct from the first two — none of DNA barcoding (species), LC-MS (synthetic drugs), or elemental analysis (metals) substitutes for the others. This heavy-metal mode was NOT separately sourced in the validated corpus [retrieval gap]; it is named here as a recognized third mode the specialist must screen for, flagged for primary retrieval before any quantitative claim. DNA barcoding detects species, not undeclared synthetic drugs — those two modes already need different detection (DNA vs LC-MS).

→ consumes: Core Rules (adulteration is the signature hazard; "natural ≠ safe / not pre-approved" frame) / Tools (third-party-testing surfacing: NSF/USP/Informed-Sport) / Anti-Patterns (reading "natural"/"supplement" as safe or vetted) / Edge Cases (high-risk-intent categories; retracted-source guard).

---

### Finding F10 — The stimulant/dependence gray zone (phenibut, tianeptine, kratom, yohimbine) carries controlled-drug hazards; modafinil marks the Rx boundary

**Claim.** A cluster of OTC/gray-market "nootropics" carry dependence, withdrawal, and overdose hazards more characteristic of controlled drugs, and several are not lawful US dietary ingredients but are sold as such — the "supplement" framing is itself the hazard.

**Evidence.** Phenibut is a GABA-B agonist producing tolerance, dependence, and a severe withdrawal syndrome (psychomotor agitation, delirium) managed with baclofen taper, recovery sometimes up to ~6 months [36, mechanism_review]; tianeptine ("gas station heroin") is a full mu-/weak delta-opioid agonist whose opioid effects emerge at higher doses (75-3,000 mg/day), is NOT an FDA-recognized dietary ingredient, and drove a poison-center increase from 11 cases (2000-2013) to 151 in 2020 alone [37, regulatory]; kratom (mitragynine / 7-OH-mitragynine) acts on mu-opioid receptors producing sedation, dependence, respiratory depression and overdose deaths (usually in combination), with some products adulterated with elevated 7-hydroxymitragynine [38, regulatory]; yohimbine adverse-event review found GI distress (46%), tachycardia (43%), anxiety (33%), hypertension (25%) and a higher rate of severe outcomes than the average toxic exposure [39, cohort]. Modafinil is a prescription drug named ONLY to mark the Rx/OTC boundary; it is out-of-scope for supplement-hazard cataloging [route/regulatory boundary — prescriptive, not OTC].

**risk_tier implied.** high for phenibut/tianeptine/kratom (dependence, withdrawal, opioid-class respiratory-depression and death potential); medium-high for yohimbine (cardiovascular/sympathomimetic AEs). Synephrine/bitter orange: experimental-to-medium — case reports of CV events (16 Canadian cases 1998-2004) vs ~30 human studies showing no CV effect at common doses; evidence conflicting.

**Caveats.** Tianeptine and phenibut are not lawful US dietary ingredients but are sold in gray-market channels. Kratom deaths are predominantly polydrug, so attributable single-agent lethality is uncertain. Synephrine CV evidence is genuinely conflicting (case-series signal vs RCT/meta-analysis null at common doses) — report both and downgrade certainty. Modafinil deliberately excluded as a prescriptive boundary marker.

→ consumes: Core Rules (gray-zone dependence hazards; Rx/OTC boundary) / Refusal taxonomy (sourcing/dosing a non-lawful dietary ingredient) / Anti-Patterns ("it's sold as a supplement so it's a supplement") / Edge Cases (phenibut/tianeptine/kratom/yohimbine; modafinil boundary; conflicting synephrine evidence).

---

### Finding F11 — For tested athletes, supplement contamination converts to anti-doping strict-liability sanctions

**Claim.** Because WADA's strict-liability principle holds athletes solely responsible for substances in their bodies regardless of intent, and ~9-15% of tested commercial supplements are contaminated with prohibited substances, supplements are a documented major source of adverse analytical findings; for athlete-context users the agent must flag strict liability and third-party certification.

**Evidence.** Across an 18-year span athletes claimed a supplement source in 26% of analytical anti-doping violations, with supporting evidence found in ~14% of all analytical violations [40, cohort]; a 2002 IOC international study found ~15% of non-hormonal supplements contained undeclared anabolic steroids [40, cohort]. WADA's strict-liability framing places the burden of "no fault/negligence" on the athlete; poor labeling is not a defense [41, regulatory].

**risk_tier implied.** high for the tested-athlete population specifically (career-ending sanctions from inadvertent contamination); the underlying contamination base rate is the same hazard as F9, here with a strict-liability consequence multiplier.

**Caveats.** Population-conditional — strict liability applies only to athletes in tested pools; for the general population the same contamination is an F9 pharmacologic hazard, not a sanction risk. Third-party batch certification (F9: NSF Certified for Sport / Informed-Sport) is the specific mitigation. Contamination prevalence (9-15%) varies by era, category, and sampling frame.

→ consumes: Core Rules (athlete-context strict-liability flag as goal-agnostic fact) / Refusal taxonomy (performance/doping context) / Edge Cases (tested-athlete population conditionality).

---

### Finding F12 — DSHEA is post-market-only: manufacturer bears the safety burden, FDA does NOT pre-approve; "legally marketed" ≠ "reviewed / safe / effective"

**Claim.** Under DSHEA (1994), FDA does NOT approve dietary supplements before marketing; the manufacturer is solely responsible for safety and truthful/substantiated claims, and FDA authority is post-market only (action against adulterated/misbranded products; cGMP under 21 CFR 111) — the structural inverse of the drug pathway's mandatory premarket safety+efficacy approval.

**Evidence.** FDA: "FDA does not have the authority to approve dietary supplements before they are marketed... companies... are responsible for ensuring that their products are safe and that label claims are truthful and substantiated," with authority "to take action against any adulterated or misbranded dietary supplement product after it reaches the market" [42, regulatory]. cGMP recordkeeping/quality-control obligations (21 CFR 111.70/.75/.80) confirm post-market manufacturer responsibility [43, regulatory].

**Status/disposition.** ACTIVE and structural (statute 1994; 21 CFR 111 in force). Stable, not a time-sensitive enforcement status. Maps to a `BASIS_NOT_REVIEWABLE` refusal: "supplement is legally marketed" ≠ "FDA reviewed it."

**Caveats.** "Legally marketed dietary supplement" is a regulatory status, not a safety or efficacy finding. cGMP governs manufacturing quality (identity/purity/composition), NOT efficacy. No animal/in_vitro numerics; no population-mismatch tag.

→ consumes: Core Rules (DSHEA post-market-only frame; legally-marketed ≠ reviewed) / Refusal taxonomy (BASIS_NOT_REVIEWABLE) / Anti-Patterns (reading marketed-status as approval) / Edge Cases (drug-vs-supplement pathway inversion).

---

### Finding F13 — The confusable-status set (GRAS / NDI-notified / structure-function / third-party-tested) is each DISTINCT from "approved / proven / safe"; status answers must be time-stamped

**Claim.** Four supplement statuses are routinely laundered into an unwarranted efficacy/safety inference, and the agent must encode a status-disambiguation card and time-stamp every status answer.

**Evidence.** (a) **GRAS** = "generally recognized as safe" for a food use — a safety-of-ingestion conclusion, NOT efficacy and NOT premarket approval; (b) **NDI notification** = a 75-day-premarket safety *notification* for ingredients not marketed before Oct 15, 1994 — FDA can object but does NOT "approve"; non-objection is not endorsement [45, regulatory]; (c) **structure/function claim** = a permitted labeling claim that "are not pre-approved by FDA," requiring the mandatory disclaimer that the claim "has not been evaluated by the Food and Drug Administration" and the product "is not intended to diagnose, treat, cure, or prevent any disease" [44, regulatory]; (d) **third-party tested (USP/NSF/Informed-Sport)** = a purity/identity/label-accuracy certification, NOT an efficacy or safety-of-use finding. Treating any as "approved/proven/safe" is the laundering hazard — the supplement analog of the peptide "compoundable ≠ approved" trap.

**Status/disposition.** ACTIVE. Encode as the specialist's status-disambiguation card. Status answers MUST be time-stamped (retrieval 2026-05-29) because GRAS/NDI dispositions and certification marks change.

**Caveats.** GRAS self-affirmation (manufacturer-determined, no FDA notification) is weaker still than GRAS-notified — surface that gradient per ingredient. Third-party certs are private-body marks, not regulatory; cite the certifier's own scope, never as efficacy. No numerics; no population-mismatch tag.

→ consumes: Core Rules (status-disambiguation card; time-stamp) / Refusal taxonomy (status-laundering block) / Anti-Patterns (GRAS/NDI/structure-function/third-party-tested → approved/proven/safe) / Edge Cases (GRAS self-affirmation gradient).

---

### Finding F14 — Banned / enforcement-action ingredients are sold under a supplement label; status is the highest-volatility finding and must be re-verified and time-stamped at answer time

**Claim.** A recurring class of ingredients is marketed under a "dietary supplement" label while FDA holds them NOT to be lawful dietary ingredients (adulterated/misbranded or unapproved drugs); any specialist answer citing a ban/enforcement status must re-verify against current FDA directories and stamp the answer.

**Evidence (dated FDA actions).** Ephedrine alkaloids (ephedra) — final rule declaring them adulterated, published 2004-02-11, effective 2004-04-12 [46, regulatory]; DMAA/DMHA — adulterated, 12 DMHA warning letters [47, regulatory]; BMPEA — warning letters 2015-04-23, "does not meet the statutory definition of a dietary ingredient"; Acacia rigidula — warning letters 2016-03-15 [48, regulatory]; SARMs and "andro"/androstenedione — FDA: "not dietary supplements... unapproved drugs," 4-androstenedione not GRAS (2022-03-01 memo) [49, regulatory]; kratom — "not appropriate for use as a dietary supplement," NDI with inadequate safety assurance, Import Alert 54-15 [50, regulatory]; higenamine present in some stimulant/weight-loss supplements (WADA-relevant) [47, regulatory].

**Status/disposition.** TIME-SENSITIVE — the highest-volatility finding (retrieved 2026-05-29). Enforcement status (import alerts, warning-letter counts, watch-list additions) changes continuously; any ban/enforcement answer MUST re-verify against the current FDA "Information on Select Dietary Supplement Ingredients" directory and Import Alert pages at answer time. Maps to `BASIS_NOT_REVIEWABLE` + the H1/H2 auto-block when a queried "supplement" is in fact an unapproved-drug/banned class — couple to F10.

**Caveats.** A "dietary supplement" label does NOT establish lawful dietary-ingredient status. Warning-letter counts (12 DMHA; 5 BMPEA; 6 Acacia) are point-in-time. The 4-androstenedione concerns are FDA's regulatory characterization, not an effect-size claim.

→ consumes: Core Rules (banned-ingredient class; re-verify + time-stamp) / Refusal taxonomy (BASIS_NOT_REVIEWABLE + H1/H2 auto-block) / Tools (re-verify against live FDA directory at answer time) / Edge Cases (label ≠ lawful ingredient; point-in-time counts).

---

### Finding F15 — Prescribing-practice is convention-vs-trial; stacks inherit `combination_evidence: none` and the WEAKEST component rung; and the agent inherits the foundation contract pack (with one surfaced live CONTRADICTION)

**Claim.** Supplement dose conventions originate from functional/integrative-medicine bodies and manufacturer/community lore rather than trials, so every practitioner dose renders as "practitioner convention, not trial-validated"; multi-ingredient stacks carry `combination_evidence: none` and inherit the weakest component rung; and the specialist inherits the full foundation contract set, which the agent must encode rather than re-derive — including one live contradiction it must NOT silently inherit.

**Evidence (convention-vs-trial).** Functional-medicine convention targets serum 25(OH)D 50-80 ng/mL (IFM ~60-80) — 2-3× the conventional ≥30 ng/mL threshold — driving higher doses; this is a `practitioner_protocol` target NOT trial-validated, while the regulatory range is IOM ~20 ng/mL "adequate" / Endocrine Society ≥30 ng/mL with ULs of 4,000 IU (IOM) vs 10,000 IU (Endocrine Society) [51, regulatory; 52, practitioner_protocol]; RCTs powered on hard outcomes (VITAL) did not validate driving 25(OH)D to 60-80 ng/mL, and the Tier-1 dose-response literature is itself split on direction (Veugelers & Ekwaru 2014 argue MORE intake needed; McKenna & Murray 2013 argue the rate constant should be doubled) [53, mechanism_review]. The creatine "loading phase" (20 g/day × ~6 days) is a speed-of-saturation convention, not a necessity: Hultman 1996 showed 3 g/day × 28 days reaches the same ~20% muscle-creatine rise [54, rct]. Stacks carry no combination evidence unless a combination study exists — caffeine + L-theanine is the rare nootropic pair with a combination RCT and it behaves DIFFERENTLY from the sum of parts (theanine attenuated caffeine's vasoconstrictive/CBF effects while improving task-switching) [55, rct; 56, rct]; ≥3-ingredient blends have NO located combination trial [retrieval gap]. The ashwagandha "600 mg KSM-66" dose is trial-anchored (Chandrasekhar 2012: ~28%, exact 27.9% serum cortisol reduction vs 7.9% placebo, between-group P=0.002, from the full-text results table not the abstract) but manufacturer-associated and extract-specific [57, rct]. NAD+ precursors RAISE blood NAD+ (NR ~60% PBMC rise [58, rct]; NMN 300/600/900 mg/d × 60 d, n=80, p ≤ 0.001 [61, rct]; NMN 1250 mg/d × 4 wk tolerated, NAD+ NOT measured [59, rct]) but the clinical benefit literature is "in its infancy" [60, mechanism_review]; and NMN's regulated status shifted twice — FDA excluded NMN from the supplement definition Nov-2022, REVERSED Sep-29-2025, confirmed Dec-2-2025, so as of 2026 NMN is a LAWFUL dietary ingredient (NDI status, premarket notification still required) [62, regulatory].

**Evidence (inherited contract pack — design surfaces, not literature).** The supplement-specialist must encode, verbatim or by faithful instantiation (reasoned against `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, `vault/library/_source-whitelist.md`, and repo commit 0514f2d): (1) the **8-class refusal taxonomy**, ≥4 distinct classes, with **AUTHORITY_FRAMING_BYPASS MANDATORY** (`mandatory_for_every_specialist: true`); operator Walter is adversary-class A3 (operator-self-harm via own-agent), the ~81.8%-of-successful-jailbreaks vector — educational/"asking for a friend"/trainee framing does NOT relax the directive gate (the 81.8% figure is CONTRACT-INHERITED from the refusal taxonomy, not independently corpus-verified here); (2) **H1-H8 worst-case-reachable composition with H1/H2 auto-block**, coupled to F14's banned/unapproved-drug classes; (3) **GRADE two-axis** (certainty × strength) with a **strong-recommendation-on-low/very-low-certainty HALT** — which, given F1/F2/F15, means the agent essentially cannot issue a strong "use this supplement" recommendation for any preclinical/Rung-2-low-certainty compound; (4) **three-mechanism anti-sycophancy** (A no silent agreement, B maintain position under pushback, C guard RLHF-drift) against "everyone takes ashwagandha"/"everyone megadoses D" social proof; (5) **operator-profile R7 read-before-`vault/compounds/*`-write precondition** — HALT on an unpopulated hard-limit field before writing any compound entry; (6) **append-only `vault/meta/contradictions.md`**; (7) **escalation of `BLOCK_WITH_OVERRIDE_PATH` + PRESCRIPTIVE/PATIENT_FACING directives to the LIVE medical-liaison (Role 7) adjudicator** per commit 0514f2d; (8) **research dispatch is ONLY `aplus-research --mode=deep --target-class=compound`** (supplement `risk_class = compound-experimental-or-medium`; deep mode covers the experimental floor — MK-677, novel nootropics, phenibut — and standard would under-protect); (9) **write surface:** WRITES `vault/compounds/` (supplement class) + `vault/protocols/supplement-stack`, and UNLIKE peptide-specialist does NOT own a `vault/library/` tree; (10) **enforces type-tag / population-mismatch / concentration-audit on aplus-research returns** and NEVER self-attests a gate (PF-S2-01 / PF-S3-01).

**Status/disposition.** Convention findings ACTIVE (D1-D3). Contract pack is an ACTIVE design contract; each numbered item maps to a profile section the specialist's `agent.md` must contain.

**Caveats / surfaced CONTRADICTION (log to `vault/meta/contradictions.md`).** Commit 0514f2d deprecates the pre-Role-7 operator-acknowledged-override fallback, but `templates/refusal-class-taxonomy.yaml` escalation fields (PATIENT_FACING_DIRECTIVE, BASIS_NOT_REVIEWABLE, PRESCRIPTIVE_DIRECTIVE) STILL carry the deprecated "medical-liaison when deployed; otherwise operator-acknowledged-override" fallback verbatim; the specialist MUST encode the LIVE-Role-7 escalation per the commit, and the stale template fallback language must NOT be inherited until the template is reconciled to the commit. Practitioner cite [52] (IFM 50-80 ng/mL) was HTTP-403 and lacks author+date — flag for re-fetch before wiki lock; [52] may NOT ground a 60-80 ng/mL efficacy claim. Branded ashwagandha [57] is manufacturer-associated (sponsor-bias flag), extract-specific (does not transfer to generic or Sensoril). [59] supports NMN tolerability ONLY (NAD+ not measured). [62] regulated status re-verify against posted FDA NDIN letters before ingest (posture changed twice). The H1-H8 composition and GRADE/anti-sycophancy canonical wording live in Role-1/Role-2 design docs NOT read this dispatch — flagged `basis-not-fully-reviewable`; do not self-attest their exact wording.

→ consumes: Identity / Core Rules / Role Boundaries / Tools (aplus-research dispatch; convention `source_tier`; stack `combination_evidence: none`) / Anti-Patterns (practitioner-convention-as-validated; manufacturer-dose-as-generic; stack-from-single-ingredient-data; inheriting the stale template fallback) / Edge Cases (50-80 ng/mL target; creatine loading; NMN status-shift; LIVE-Role-7 escalation). Section F15 informs every AGENT_TEMPLATE section.

---

## Recommendations

**R1.** Encode a mandatory per-compound `maturity_rung` ∈ {established/monograph-backed, trial-stage, preclinical, anecdote} and forbid marketing-class membership ("adaptogen"/"nootropic") from substituting for compound-level human evidence; record rung PER OUTCOME (creatine strength vs cognition differ). → Core Rules / design-doc §3. ACCEPTED.

**R2.** Maintain two separate columns per compound — `mechanism_target` and `human_outcome_evidence` — and block any mechanism-justified confidence upgrade when human-outcome evidence is null/preclinical (NMN, resveratrol canonical). → Core Rules / Anti-Patterns. ACCEPTED.

**R3.** Implement a concentration/funding-dominance check: if ≥70% of a compound's positive primaries trace to one lab OR one manufacturer-funded program (branded proprietary extracts canonical), surface the dominance explicitly, downgrade GRADE certainty, and note absent independent replication. → Core Rules / Tools (concentration-audit gate). ACCEPTED.

**R4.** Treat formulation and measured human PK as load-bearing: a trial on an enhanced form (micellar/γ-cyclodextrin/phospholipid) does NOT transfer to a native-powder product; forbid grounding any bioavailability/dose number on a vendor bioavailability chart. → Core Rules / Tools / Anti-Patterns. ACCEPTED.

**R5.** Place each compound on the four-rung ladder by its OWN human-outcome evidence against the NIH-ODS monograph backbone; render "high rung" as "competently asked in humans," never as "positive result" (VITAL null canonical). → Core Rules / Identity. ACCEPTED.

**R6.** Implement a UL/toxicity-ceiling gate for fat-soluble vitamins (A teratogenicity, D hypercalcemia), B6 (sensory neuropathy), and trace minerals (selenium, zinc-copper antagonism, iron); where IOM and EFSA ULs diverge (B6 100 vs 12 mg/day), cite both and log the contradiction. → Core Rules / Tools (contradiction logging) / Anti-Patterns ("more is better"). ACCEPTED.

**R7.** Carry hepatotoxicity as a class hazard occurring at LABEL doses (green tea extract/EGCG, kava, ashwagandha, sustained-release niacin), with the GTE HLA-B*35:01 pharmacogenomic flag and a pre-existing-liver-disease edge case. → Core Rules / Edge Cases. ACCEPTED.

**R8.** Run a mandatory herb-/supplement-drug interaction-screen: St John's Wort CYP3A4/P-gp induction (hyperforin-content-dependent), additive bleeding (ginkgo/garlic/vitamin E/ginger/fish oil + warfarin), and serotonergic stacking (SJW + SSRI documented; 5-HTP theoretical). → Core Rules / Tools / Anti-Patterns. ACCEPTED.

**R9.** Surface adulteration/contamination as the SIGNATURE category hazard with its base rate (undeclared sildenafil/sibutramine/steroids/novel stimulants, highest in sexual-enhancement/weight-loss/muscle-building), pair every such discussion with third-party-testing mitigation (NSF Certified for Sport / USP Verified / Informed-Sport), and guard the retracted 2013 "30/44" barcoding figure. → Core Rules / Tools / Anti-Patterns / Edge Cases. ACCEPTED.

**R10.** Encode the "natural ≠ safe / not FDA pre-market-approved" frame and never read "natural"/"supplement"/"legally marketed" as safe, vetted, or reviewed. → Core Rules / Anti-Patterns. ACCEPTED.

**R11.** Flag the stimulant/dependence gray zone (phenibut GABA-B, tianeptine mu-opioid, kratom mu-opioid, yohimbine sympathomimetic) as carrying controlled-drug hazards, note that several are not lawful US dietary ingredients despite supplement framing, and mark modafinil as the Rx/OTC boundary (out of scope). → Core Rules / Refusal taxonomy / Edge Cases. ACCEPTED.

**R12.** For athlete/competition context, surface WADA strict liability and the ~9-15% contamination base rate as goal-agnostic facts, and route to third-party batch certification as the mitigation. → Core Rules / Refusal taxonomy / Edge Cases. ACCEPTED.

**R13.** Encode the DSHEA post-market-only frame: manufacturer bears the safety burden, FDA does not pre-approve; map "legally marketed" to `BASIS_NOT_REVIEWABLE`, not to a safety/efficacy finding. → Core Rules / Refusal taxonomy. ACCEPTED.

**R14.** Encode a status-disambiguation card distinguishing GRAS / NDI-notified / structure-function / third-party-tested from "approved / proven / safe" (with the GRAS-self-affirmation gradient), hard-block any output laundering one into another, and time-stamp every status answer. → Core Rules / Refusal taxonomy / Anti-Patterns. ACCEPTED.

**R15.** Treat banned/enforcement-action ingredients (ephedra, DMAA/DMHA, BMPEA, Acacia rigidula, SARMs/andro, kratom, higenamine) as the highest-volatility finding: re-verify against the live FDA "Select Dietary Supplement Ingredients" directory + Import Alerts at answer time, time-stamp, and trigger BASIS_NOT_REVIEWABLE + the H1/H2 auto-block when a queried "supplement" is in fact a banned/unapproved-drug class. → Core Rules / Refusal taxonomy / Tools. ACCEPTED.

**R16.** Attach a `source_tier` to every dose; render `[practitioner_protocol]` doses (vitamin D 50-80 ng/mL target, creatine loading) as "practitioner convention, not trial-validated"; where Tier-1 contradicts convention, give the academic source primacy and report both. → Core Rules / Anti-Patterns. ACCEPTED.

**R17.** Emit `combination_evidence: none` for any multi-ingredient stack lacking a combination study (≥3-ingredient nootropic blends canonical), make a stack inherit the WEAKEST component rung, and never infer combination effect/safety from single-ingredient data (caffeine + L-theanine proves the combination ≠ sum of parts). → Core Rules / Edge Cases. ACCEPTED.

**R18.** Bind the inherited contract pack in `agent.md`: AUTHORITY_FRAMING_BYPASS (mandatory) plus ≥3 other refusal classes; a per-compound `worst_case_h_class` with H1/H2 auto-block; a GRADE HALT for strong-on-low-certainty; the 3-mechanism anti-sycophancy stance; the R7 read-`vault/meta/operator-profile.md`-before-`vault/compounds/*`-write ordering; append-only `vault/meta/contradictions.md`; LIVE medical-liaison (Role 7) escalation for PRESCRIPTIVE/PATIENT_FACING + BLOCK_WITH_OVERRIDE_PATH (encoding the LIVE escalation, NOT the deprecated pre-Role-7 fallback that the stale `templates/refusal-class-taxonomy.yaml` still carries); deep-mode-only `aplus-research --mode=deep --target-class=compound` dispatch (never bare `deep-research`); a write surface of `vault/compounds/` + `vault/protocols/supplement-stack` with NO `vault/library/` tree; and NO gate self-attestation (PF-S2-01/PF-S3-01). → Identity / Core Rules / Role Boundaries / Tools. ACCEPTED.

---

## Bibliography

Consolidated and deduplicated across the five section bibliographies. Section A contributed 15 entries, B 26, C 16 (incl. 4 design surfaces), D 14, E 7 (78 raw). Cross-section duplicates merged: NIH-ODS vitamin D fact sheet (B2 ≡ D1 regulatory); WADA Prohibited List / strict-liability (B25 ≡ C-WADA-context); FDA kratom / Import Alert (B22 ≡ C9); NSF/USP/Informed-Sport certification (B19 used once); ashwagandha branded-extract trial provenance (A/D cross-reference, single Chandrasekhar entry [57]); curcumin PK split preserved as two papers [12]/[13]. Design surfaces are listed separately and are NOT literature entries.

*Landscape & evidence-maturity (Section A):*
[1] Desai I, Wewege MA, Jones MD, et al. (2024). "The Effect of Creatine Supplementation on Resistance Training-Based Changes to Body Composition: A Systematic Review and Meta-analysis." J Strength Cond Res. PMID 39074168; DOI 10.1519/JSC.0000000000004862. https://pubmed.ncbi.nlm.nih.gov/39074168/ (Retrieved 2026-05-29). [meta_analysis]
[2] Forbes SC, Candow DG, Ostojic SM, et al. (2021). "Meta-Analysis Examining the Importance of Creatine Ingestion Strategies on Lean Tissue Mass and Strength in Older Adults." Nutrients 13(6):1912. PMC8229907. https://pmc.ncbi.nlm.nih.gov/articles/PMC8229907/ (Retrieved 2026-05-29). [meta_analysis]
[3] Authors (2022). "Acute Effect of a Dietary Multi-Ingredient Nootropic as a Cognitive Enhancer in Young Healthy Adults: A Randomized, Triple-Blinded, Placebo-Controlled, Crossover Trial." PMC9133906. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9133906/ (Retrieved 2026-05-29). [rct]
[4] Category reviews of nootropics/adaptogens (non-whitelisted aggregator hosts; qualitative lead only). https://mynucleus.com/blog/adaptogens-and-nootropics (Retrieved 2026-05-29). [anecdote_aggregate]
[5] Authors (2024). "Effects of Nicotinamide Mononucleotide on Glucose and Lipid Metabolism in Adults: A Systematic Review and Meta-analysis of RCTs." PMC11557618. https://pmc.ncbi.nlm.nih.gov/articles/PMC11557618/ (Retrieved 2026-05-29). [meta_analysis]
[6] Authors. "Mechanism of Human SIRT1 Activation by Resveratrol" (Borra 2005, PMID 15749705). J Biol Chem. https://www.jbc.org/article/S0021-9258(20)65895-1/fulltext (Retrieved 2026-05-29). [in_vitro]
[7] Authors (2025). "Impact of Resveratrol Supplementation on Human Sirtuin 1: A GRADE-Assessed Systematic Review and Dose-Response Meta-Analysis of RCTs." ScienceDirect S2212267225001145. https://www.sciencedirect.com/science/article/pii/S2212267225001145 (Retrieved 2026-05-29). [meta_analysis]
[8] Transparent Labs (vendor/retailer page; brand-ownership + standardization % ONLY, no efficacy). "Sensoril vs. KSM-66." https://www.transparentlabs.com/blogs/all/best-ashwagandha-powder-ksm-66-vs-sensoril (Retrieved 2026-05-29). [vendor_label]
[9] Authors (2025/2026). "Ashwagandha as an Adaptogenic Herb: A Comprehensive Review of Immunological and Neurological Effects." PMC12680924. https://pmc.ncbi.nlm.nih.gov/articles/PMC12680924/ (Retrieved 2026-05-29). [mechanism_review]
[10] Chartres N, et al. (2016). "Association of Industry Sponsorship With Outcomes of Nutrition Studies: A Systematic Review and Meta-analysis." JAMA Intern Med (RR 1.31, 95% CI 0.99-1.72). PMID 27802480. https://pubmed.ncbi.nlm.nih.gov/27802480/ (Retrieved 2026-05-29). [meta_analysis]
[11] Authors (2019). "Dietary Curcumin: Correlation between Bioavailability and Health Potential." Nutrients / PMC6770259. https://pmc.ncbi.nlm.nih.gov/articles/PMC6770259/ (Retrieved 2026-05-29). [mechanism_review]
[12] Flory S, Sus N, Haas K, et al. (2021). "Increasing Post-Digestive Solubility of Curcumin Is the Most Successful Strategy to Improve its Oral Bioavailability: A Randomized Cross-Over Trial in Healthy Adults." Mol Nutr Food Res 65(24):2100613 (micellar ~57-fold, γ-cyclodextrin ~30-fold vs native). PMID 34665507; DOI 10.1002/mnfr.202100613. https://onlinelibrary.wiley.com/doi/full/10.1002/mnfr.202100613 (Retrieved 2026-05-29). [rct]
[13] Schiborr C, Kocher A, Behnam D, et al. (2014). "The oral bioavailability of curcumin from micronized powder and liquid micelles is significantly increased in healthy humans and differs between sexes." Mol Nutr Food Res 58(3):516-527 (micellar ~185-fold; 114× men, 277× women). PMID 24402825; DOI 10.1002/mnfr.201300724. https://pubmed.ncbi.nlm.nih.gov/24402825/ (Retrieved 2026-05-29). [rct]
[14] Manson JE, et al. (2019). "Vitamin D Supplements and Prevention of Cancer and Cardiovascular Disease" (VITAL, n=25,871). NEJM. https://www.nejm.org/doi/full/10.1056/NEJMoa1809944 (Retrieved 2026-05-29). [rct]
*(Note: [15] is an intentional renumbering gap, not a dropped citation — see Self-check. [16] retained its Section-A source number after the [12]/[13] curcumin split left [15] unused at the Section-A boundary.)*
[16] Authors (2024). "The effects of creatine supplementation on cognitive function in adults: a systematic review and meta-analysis" (GRADE; memory moderate, most domains low). Frontiers in Nutrition / PMC11574456. https://pmc.ncbi.nlm.nih.gov/articles/PMC11574456/ (Retrieved 2026-05-29). [meta_analysis]

*Safety hazards (Section B):*
[17] NIH Office of Dietary Supplements (n.d.). "Vitamin A and Carotenoids — Health Professional Fact Sheet" (UL 3,000 mcg RAE/day; teratogenicity); corroborated by EFSA NDA Panel UL opinion, PMC11154838. https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[18] NIH Office of Dietary Supplements (n.d.). "Vitamin D — Health Professional Fact Sheet" (UL 100 mcg/4,000 IU). https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[19] NIH Office of Dietary Supplements (n.d.). "Selenium — Health Professional Fact Sheet" (UL 400 mcg/day; selenosis). https://ods.od.nih.gov/factsheets/Selenium-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[20] NIH Office of Dietary Supplements (n.d.). "Zinc — Health Professional Fact Sheet" (UL 40 mg/day; ≥50 mg/day copper-absorption inhibition, HDL reduction). https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[21] NIH Office of Dietary Supplements (n.d.). "Iron — Health Professional Fact Sheet" (UL 45 mg/day adults). https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[22] NIH Office of Dietary Supplements (n.d.). "Vitamin B6 — Health Professional Fact Sheet" (UL 100 mg/day; 1-6 g/day for 12-40 mo → severe sensory neuropathy). https://ods.od.nih.gov/factsheets/VitaminB6-HealthProfessional/ (Retrieved 2026-05-29). [regulatory]
[23] EFSA NDA Panel (2023). "Scientific opinion on the tolerable upper intake level for vitamin B6" (revised UL 12 mg/day). PMC10189633. (Retrieved 2026-05-29). [regulatory]
[24] Billington EO, et al. (2020). "Safety of High-Dose Vitamin D Supplementation: Secondary Analysis of a Randomized Controlled Trial." J Clin Endocrinol Metab 105(4):1290-1297 (Calgary, 3-yr, n=373; hypercalcemia 0/3/9%, hypercalciuria 17/22/31% at 400/4,000/10,000 IU/day). PMID 31746327; DOI 10.1210/clinem/dgz212. (Retrieved 2026-05-29). [rct]
[25] LiverTox (NIDDK/NIH). "Green Tea" (NBK547925) + USP hepatotoxicity review (PubMed 32140423) + DILIN SLIMQUICK (PMC4961850) + HLA-B*35:01 study (PMC10731652) (EGCG 140-1,000 mg/day; ~9% fatal; 72% HLA-B*35:01). (Retrieved 2026-05-29). [mechanism_review]
[26] LiverTox (NIDDK/NIH). "Kava Kava" (NBK548637) + FDA 2002 advisory + clinical review (PubMed 20720265) + ban-lifted analysis (PubMed 26695707) (9 published + 24 unpublished cases; 1 death; 3 transplants). (Retrieved 2026-05-29). [mechanism_review]
[27] LiverTox (NIDDK/NIH). "Ashwagandha" (NBK548536) + Iceland/US DILIN case series (PMC8041491) (cholestatic/mixed; 2-12 wk onset). (Retrieved 2026-05-29). [mechanism_review]
[28] LiverTox (NIDDK/NIH). "Niacin" (NBK548176) + time-release niacin hepatotoxicity (PubMed 1731514) (sustained-release > immediate-release at equi-lipid dose). (Retrieved 2026-05-29). [mechanism_review]
[29] SJW/hyperforin interaction reviews (PubMed 16477470, 15350151) + P-gp induction (PMC1874544, PubMed 11180019) (PXR/hyperforin CYP3A4 + P-gp induction; cyclosporine, tacrolimus, HIV PIs/NNRTIs, irinotecan, imatinib, warfarin, digoxin, OCPs). (Retrieved 2026-05-29). [mechanism_review]
[30] St. John's Wort StatPearls (NBK557465) + SJW-SSRI interaction review (PMC12420457) + delayed serotonin-syndrome case report (PMC12580605). (Retrieved 2026-05-29). [mechanism_review]
[31] "Dietary supplements and bleeding" review (PMC9586694) + Ginkgo-warfarin EHR signal (PMC5760175) + Ginkgo antiplatelet evidence review (PubMed 18214851) (garlic↔surgical bleeding; ginkgo/ginger/vitamin E warfarin caution). (Retrieved 2026-05-29). [cohort]
[32] Tucker J, et al. (2018). "Unapproved Pharmaceutical Ingredients Included in Dietary Supplements Associated With US FDA Warnings." JAMA Netw Open. PMC6324457 (776 supplements; sildenafil 47.0%, sibutramine 84.9%, synthetic steroids 89.1%; 20.2% multi-adulterant). (Retrieved 2026-05-29). [cohort]
[33] Cohen PA, et al. "Prohibited Stimulants in Dietary Supplements After FDA Enforcement Action." PMC6583602 + FDA "DMHA and Phenibut" notice (75% of 12 products contained ≥1 prohibited stimulant). (Retrieved 2026-05-29). [cohort]
[34] "DNA Barcoding of Online Herbal Supplements" (Urban Barcode). PMC7874675 / PubMed 33817067 (4/20 single-ingredient products substituted). NOTE: 2013 Newmaster BMC Medicine "30/44" paper is RETRACTED — not cited as a number. (Retrieved 2026-05-29). [cohort]
[35] NSF Certified for Sport; USP Dietary Supplements Verification Program; Informed-Sport (nsf.org, usp.org). (Retrieved 2026-05-29). [regulatory]
[36] Phenibut dependence/withdrawal review (PMC5952553) + withdrawal case reports (PMC8273510, PubMed 28614159) (GABA-B agonism; baclofen-managed withdrawal; prolonged recovery). (Retrieved 2026-05-29). [mechanism_review]
[37] FDA tianeptine consumer pages + systematic review (PMC12551324) + use-disorder case report (PMC12542876) (full-mu/weak-delta agonist; 75-3,000 mg/day; not a lawful dietary ingredient; poison-center 11→151). (Retrieved 2026-05-29). [regulatory]
[38] FDA "FDA and Kratom" + CDC overdose-death field note (PMC6459583) + coroner postmortem analysis (PMC10806006) (mu-opioid action; dependence/respiratory depression; 7-OH adulteration). (Retrieved 2026-05-29). [regulatory]
[39] California Poison Control yohimbine retrospective. PubMed 20442348 (GI 46%, tachycardia 43%, anxiety 33%, hypertension 25%). (Retrieved 2026-05-29). [cohort]
[40] "Dietary Supplements as a Major Cause of Anti-doping Rule Violations" (PMC8990797) + "...Source of Unintentional Doping" (PMC9054437) + systematic review (PMC13021601) (9-15% contamination; 26% claimed / ~14% evidenced; 2002 IOC ~15%). (Retrieved 2026-05-29). [cohort]
[41] WADA. "The Prohibited List" + strict-liability principle. https://www.wada-ama.org/en/prohibited-list (Retrieved 2026-05-29). [regulatory]

*Regulatory (Section C):*
[42] FDA. "Questions and Answers on Dietary Supplements." https://www.fda.gov/food/information-consumers-using-dietary-supplements (Retrieved 2026-05-29). [regulatory]
[43] FDA. "NDI Notifications guidance"; 21 CFR 111.70/.75/.80. fda.gov/media/99538; accessdata.fda.gov CFR Title 21 Part 111. (Retrieved 2026-05-29). [regulatory]
[44] FDA. "Structure/Function Claims; Small Entity Compliance Guide." https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/structurefunction-claims (Retrieved 2026-05-29). [regulatory]
[45] FDA. "New Dietary Ingredients in Dietary Supplements: Background for Industry; Draft NDI Guidance." fda.gov/media/176512, /99538. (Retrieved 2026-05-29). [regulatory]
[46] FDA. "Small Entity Compliance Guide: Final Rule Declaring Ephedrine Alkaloids Adulterated" (published 2004-02-11; eff. 2004-04-12). (Retrieved 2026-05-29). [regulatory]
[47] FDA. "DMAA in Products Marketed as Dietary Supplements"; "DMHA in Dietary Supplements"; "FDA Acts on DMHA and Phenibut." fda.gov/food/information-select-dietary-supplement-ingredients-and-other-substances. (Retrieved 2026-05-29). [regulatory]
[48] FDA. "Recent FDA Action on Supplements Labeled as Containing BMPEA" (2015-04-23); "...Acacia Rigidula" (2016-03-15). (Retrieved 2026-05-29). [regulatory]
[49] FDA. "Bodybuilding Products: SARMs Cause Harm"; "Scientific Memorandum: Androstenedione" (2022-03-01). fda.gov/media/169491. (Retrieved 2026-05-29). [regulatory]
[50] FDA. "FDA and Kratom"; Import Alert 54-15; "US Marshals seize kratom supplements." accessdata.fda.gov/cms_ia/importalert_1137.html. (Retrieved 2026-05-29). [regulatory]
(International divergence — EU Directive 2002/46/EC (EUR-Lex, [regulatory], primary); Australia TGA / Canada Health Canada NHPD specifics rest on non-whitelisted secondary compliance-vendor summaries, admissible only as `anecdote_aggregate`-class leads flagged for primary re-verification at tga.gov.au / canada.ca — carried as a caveat, NOT a grounding citation.)

*Prescribing-practice (Section D):*
[51] IOM (2011). "Dietary Reference Intakes for Calcium and Vitamin D" (UL 4,000 IU/day; adequacy ~20 ng/mL), PAIRED with Endocrine Society 2011 guideline (Holick MF, et al., J Clin Endocrinol Metab 96(7):1911-30, PMID 21646368; ≥30 ng/mL sufficiency, 10,000 IU/day upper limit). nap.nationalacademies.org/catalog/13050. (Retrieved 2026-05-29). [regulatory]
[52] IFM. "Vitamin D Evaluation: A Clinical Tool in Personalized Medicine" (50-80 ng/mL target; HTTP-403, author+date NOT yet captured — target/dose convention ONLY, not efficacy; re-fetch before wiki lock). ifm.org. (Retrieved 2026-05-29). [practitioner_protocol]
[53] Veugelers PJ, Ekwaru JP (2014). "A Statistical Error in the Estimation of the Recommended Dietary Allowance for Vitamin D." Nutrients 6(10):4472-5 (re-analysis: ~8,895 IU/day needed for 97.5% to reach 50 nmol/L; figure beyond studied dose range). PMID 25333201 / PMC4210929. Distinct from McKenna & Murray 2013 (PMC3680954), which argues the OPPOSITE direction (rate constant should be doubled). (Retrieved 2026-05-29). [mechanism_review]
[54] Hultman E, Söderlund K, Timmons JA, et al. (1996). "Muscle creatine loading in men." J Appl Physiol 81(1):232-7 (20 g×6d and 3 g×28d both → ~20% muscle Cr; maintenance 2 g/d; loading framed as optional). PMID 8828669. (Retrieved 2026-05-29). [rct]
[55] Dodd FL, et al. "A double-blind, placebo-controlled study evaluating the effects of caffeine and L-theanine both alone and in combination on cerebral blood flow, cognition and mood." PMID 25761837 / PMC4480845 (combination ≠ sum of parts; theanine attenuated caffeine CBF/mood effects). (Retrieved 2026-05-29). [rct]
[56] Owen GN, et al. "The combination of L-theanine and caffeine improves cognitive performance and increases subjective alertness." PMID 21040626. (Retrieved 2026-05-29). [rct]
[57] Chandrasekhar K, Kapoor J, Anishetty S (2012). "A prospective, randomized double-blind, placebo-controlled study of safety and efficacy of a high-concentration full-spectrum extract of ashwagandha root in reducing stress and anxiety in adults." Indian J Psychol Med 34(3):255-62 (KSM-66 600 mg/day; ~28% / exact 27.9% serum cortisol reduction vs 7.9% placebo, between-group P=0.002, from full-text results table not abstract; manufacturer-associated — sponsor-bias flag). PMID 23439798 / PMC3573577. (Retrieved 2026-05-29). [rct]
[58] Martens CR, et al. "Chronic nicotinamide riboside supplementation is well-tolerated and elevates NAD+ in healthy middle-aged and older adults." PMID 29599478 / PMC5876407 (NAD+ elevation + tolerability, NOT clinical benefit). (Retrieved 2026-05-29). [rct]
[59] "Safety evaluation of β-nicotinamide mononucleotide oral administration in healthy adult men and women." PMC9400576 (NMN 1250 mg/day × 4 wk, n=31, no SAEs; NAD+ NOT measured — cannot support an NMN→NAD+ elevation claim). (Retrieved 2026-05-29). [rct]
[60] "Dietary Supplementation With NAD+-Boosting Compounds in Humans: Current Knowledge and Future Directions." PMC10692436 (clinical functional benefit unclear / early). (Retrieved 2026-05-29). [mechanism_review]
[61] Yi L, Maier AB, et al. "The efficacy and safety of β-nicotinamide mononucleotide (NMN) supplementation in healthy middle-aged adults: a randomized, multicenter, double-blind, placebo-controlled, parallel-group, dose-dependent clinical trial." PMC9735188 (NMN 300/600/900 mg/day × 60 d, n=80; whole-blood NAD+ significantly increased in all NMN groups vs placebo at days 30 and 60, p ≤ 0.001 — biomarker only, NOT clinical benefit). (Retrieved 2026-05-29). [rct]
[62] FDA new-dietary-ingredient correspondence on β-NMN (NDIN responses to SyncoZymes NDIN 1247 and Inner Mongolia Kingdomway NDIN 1259): Nov-2022 exclusion → Sep-29-2025 reversal → Dec-2-2025 confirmation letters; CURRENT 2026 STATUS: NMN is a LAWFUL dietary ingredient retaining NDI status (premarket notification still required). Re-verify against posted FDA NDIN letters before ingest. (Retrieved 2026-05-29). [regulatory]

*Non-English literature (Section E):*
[63] Vasil'eva EV, Kondrakhin EA, et al. (2020). "Predominance of Nootropic or Anxiolytic Effects of Selank, Semax, and Noopept Peptides Depending on the Route of Administration to BALB/c and C57BL/6 Mice." Neurochem J. https://link.springer.com/article/10.1134/S1819712420030113 (Springer full-text paywalled; abstract-confirmed). `[population-mismatch:mouse]` (Retrieved 2026-05-29). [animal]
[64] Stakhovskaya LV, et al. (2017). "[EPICA: RCT of mexidol in acute/early-recovery hemispheric ischemic stroke]." Zh Nevrol Psikhiatr Im S S Korsakova (n=150; lower mean mRS vs placebo, p=0.04). PMID 28665371 (English abstract / Russian full text; `[non-english-untranslated]` for in-text secondary endpoints). (Retrieved 2026-05-29). [rct]
[65] Ziganshina LE, et al. (2023). "Cerebrolysin for acute ischaemic stroke." Cochrane Database Syst Rev CD007026.pub7; PMID 37818733 (judged risk of bias HIGH wherever manufacturer sponsorship/involvement; full-text CAPTCHA-gated, finding from record summary). (Retrieved 2026-05-29). [meta_analysis]
[66] Guo J, et al. (2021). "The Effect of Berberine on Metabolic Profiles in Type 2 Diabetic Patients: A Systematic Review and Meta-Analysis of RCTs." Oxidative Med Cell Longev. PMC8696197 (46 RCTs / 4,158 participants; searched CNKI/Wanfang/VIP; HbA1c MD −0.73; authors: "literature qualities were uneven," "most trials... conducted among Chinese patients"). (Retrieved 2026-05-29). [meta_analysis]
[67] "Quality Evaluation of Randomized Controlled Trials of Rhodiola Species: A Systematic Review." PMC8266448 (39 RCTs; CONSORT scores R. rosea 0.33 / R. crenulata 0.25 / R. wallichiana 0.17; China-exclusive species at lowest scores). (Retrieved 2026-05-29). [meta_analysis]
[68] Ashwagandha human-trials systematic reviews + classical-literature review: ScienceDirect S2210803321000142 (human trials; standardization <0.9% withanolides) + classical Ayurvedic text review (World J Pharm Res, wisdomlib) — `mechanism_review` for trials; classical text is traditional-use/`anecdote_aggregate`-equivalent (qualitative only). (Retrieved 2026-05-29). [mechanism_review]
[69] German Commission E monographs (1984-1994), ginkgo (EGb 761: flavone glycosides 22-27%, terpene lactones 2.8-3.4%) + St. John's wort; Expanded Commission E (HerbalGram) + independent ginkgo assessment (PMC2950792, "insufficient evidence... improve memory in healthy subjects"). (Retrieved 2026-05-29). [regulatory]

*Design surfaces (in-repo; NOT literature, NOT type-tagged — IC-1-normalized to plain file references):*
- `templates/refusal-class-taxonomy.yaml` (S10 Phase 5; owner Role 1) — 8 refusal classes; AUTHORITY_FRAMING_BYPASS mandatory; A3 / 81.8% rationale; PATIENT_FACING/PRESCRIPTIVE escalation. (Carries the deprecated pre-Role-7 fallback verbatim — see F15 CONTRADICTION.)
- `templates/specialist-risk-class.yaml` (S10 Phase 5; owner Role 2) — supplement-specialist row: `risk_class: compound-experimental-or-medium`, `mode_floor: deep`, `target_class: compound`.
- `vault/library/_source-whitelist.md` — type-tag enum + admissibility matrix (consumed as the BASE list; supplement-specialist does NOT author/extend a library tree).
- Repo git log, commit 0514f2d ("dispatch-flip: medical-liaison live adjudicator; deprecate pre-Role-7 fallback (BC-1)") — grounds the LIVE-Role-7 escalation requirement.

---

## Methodology & gate provenance

**Pipeline.** Deep-mode `aplus-research` run. Five sections (A landscape & evidence-maturity; B safety hazards; C regulatory + contract-mapping; D prescribing-practice; E non-English literature), each a paired retrieve+judge dispatch judged at deep-99. Gates 2.75 (scope), 3.5 (judge), 4.25 (population-mismatch), 4.75 (integrity) PASS, integrity-verified. Phase-6 critique pending; this synthesis is corpus-read-only (no new retrieval).

**Judge iterations of note.** Section A required four iterations: iter-2 re-sourced four numerical claims and unbundled two reference pairs ([1]/[2] creatine, [12]/[13] curcumin) with a full grep sweep for OLD values; iter-3 fixed the NMN HOMA-IR point estimate (sign correction so it sits inside its CI, SMD label restored); **iter-4 was an anti-hallucination AUTO-FAIL remediation** — a fabricated quotation ("an exaggeration of the benefits of NMN supplementation") attributed to [5] (PMC11557618) was confirmed absent by three independent fetches and replaced with the source-verbatim conclusion; iter-4b corrected the resveratrol population-mismatch descriptor to "cell-free recombinant-enzyme assay." Section B iter-2 re-attributed the vitamin D 0/3/9% hypercalcemia dose-response from the NIH-ODS fact sheet to the Billington 2020 Calgary RCT [24, rct]. Section C two web searches were classifier-outage-blocked (Australia/Canada regulators), forcing secondary-source reliance for the non-EU international specifics. Section D iter-2 corrected a mis-attributed vitamin-D dose-response author (Heaney → Veugelers & Ekwaru) and re-anchored the NMN regulatory timeline; iter-3 disaggregated an over-attributed NR/NMN NAD+-elevation claim and added the Yi & Maier NMN RCT [61]. Section E disclosed paywalled/CAPTCHA-gated fetches (Springer [63], Cochrane [65]) rather than paraphrasing as if read.

**IC-1 normalization applied here (Phase-4.75 WARN).** Section-C's contract-inheritance references to in-repo DESIGN SURFACES are rendered as plain file-path references (no literature type-tag); section-D's `regulatory-derived` / `regulatory-registry` descriptors are normalized to `regulatory`. Every literature claim retains exactly one enum type-tag.

**Residual WARNs.**
- Section C international divergence: Australia (TGA) / Canada (Health Canada NHPD) specifics rest on non-whitelisted secondary compliance-vendor summaries (single-source dominance for those two sub-claims), flagged for primary re-verification at tga.gov.au / canada.ca; the EU claim is independently EUR-Lex-grounded.
- Corpus-missing / paywalled: section-E [63] Springer full-text and [65] Cochrane full-text were paywall/CAPTCHA-gated (abstract/record-summary confirmed). Section-E Khavinson bioregulator numericals (775 papers / lifespan / infection figures) were NOT carried — every hit was a non-whitelisted vendor host; flagged as the largest unresolved concentration risk in the Russian corpus pending direct primary retrieval.
- Practitioner cite [52] (IFM 50-80 ng/mL) HTTP-403: venue captured, author+date NOT — re-fetch before wiki lock.
- Surfaced live CONTRADICTION (F15): `templates/refusal-class-taxonomy.yaml` still carries the deprecated pre-Role-7 operator-acknowledged-override fallback that commit 0514f2d deprecates — log to `vault/meta/contradictions.md`; the specialist encodes the LIVE-Role-7 escalation, NOT the stale fallback.

## Self-check

- **Finding count:** 15 `### Finding` blocks (F1-F15). PASS (target ~14-15).
- **Recommendation count:** 18 (R1-R18), each one-sentence design-actionable and marked ACCEPTED. PASS (target ~15-18).
- **Bibliography entries:** 68 numbered literature entries ([1]-[14] and [16]-[69]; the single gap at [15] is intentional — Section A's [16] creatine-cognition reference kept its source-section number while the curcumin split occupies [12]/[13], leaving [15] unused at the Section-A boundary), plus 4 design-surface references listed separately and NOT type-tagged. Cross-section duplicates merged (NIH-ODS vitamin D, WADA, FDA kratom, ashwagandha branded-extract). Every literature entry carries exactly one enum type-tag in `[N] ... [type_tag]` form.
- **Type-tag discipline:** PASS. Every literature claim carries exactly one enum type-tag. `vendor_label` [8] grounds ONLY brand-ownership/standardization %, never efficacy/dose/AE. `anecdote_aggregate` [4] grounds ONLY the qualitative "evidence is thin" lead. `in_vitro` [6] (resveratrol ~8-fold) is not transferred to any human-outcome claim. Design surfaces carry NO literature type-tag (IC-1-normalized).
- **Population-mismatch tags preserved verbatim:** PASS. Resveratrol `[population-mismatch: cell-free recombinant-enzyme assay]` (F2); Russian nootropic mouse study `[population-mismatch:mouse]` (Methodology / [63]). No animal/in_vitro number transferred to a human claim.
- **Concentration / funding / language-dominance caveats preserved:** PASS. F3 (single-lab AND manufacturer-funded dominance; ≥70% downgrade trigger; RR 1.31 CI-crosses-1.0); F15 branded-extract sponsor-bias flag; Methodology Russian-nootropic / Chinese-botanical / Khavinson concentration caveats and `[non-english-untranslated]` carried.
- **Goal-agnosticism (PF-S2-04):** PASS. All findings stated at class/population level; no operator personalization, ranking, or "best for X" framing; null results (vitamin D VITAL, NMN, resveratrol) reported as findings, not filtered.
- **No-self-attest provenance:** PASS. This substrate marks NO aplus-research gate as passed (PF-S2-01/PF-S3-01); it is research substrate only. The 81.8% jailbreak figure is marked CONTRACT-INHERITED (not corpus-verified here); the H1-H8 composition and GRADE/anti-sycophancy canonical wording are flagged `basis-not-fully-reviewable` pending Role-1/Role-2 design-doc read.
- **No new numbers introduced:** PASS. Every numeral appears in section A-E or the contract pack.
