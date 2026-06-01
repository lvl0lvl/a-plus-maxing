# Section C — "Anti-Aging"/Geroprotector Compounds: Evidence Grading, Safety & the Hype Landscape

> SCOPE NOTE: Goal-agnostic library substrate for DESIGNING the `longevity-strategist` agent. No operator personalization. This is the highest pseudoscience-load domain in the project: the dominant epistemic failure mode is laundering mouse and in-vitro data into human prescriptive claims. Every numeric claim sourced to a non-human study carries an inline `[population-mismatch:<species>]` tag in the same sentence. The through-line: **no geroprotector compound has demonstrated extension of human lifespan or healthspan in a powered RCT with hard outcomes.** The agent's default posture toward this entire class is HALT-pending-MD, not recommend.

## Findings

### 1. Rapamycin / rapalogs (sirolimus, everolimus, RTB101)

**Mechanism.** Rapamycin inhibits mTORC1; mTOR suppression is the single most reproducible longevity lever across model organisms (yeast → worms → flies → mice) [1, mechanism_review]. This mechanistic breadth is precisely what fuels over-extrapolation to humans.

**Animal lifespan.** The NIA Interventions Testing Program (ITP) is the gold-standard rodent lifespan platform (genetically heterogeneous mice, three sites). Rapamycin started at 9 months extended median lifespan ~9% (males) / ~14% (females); started later it still worked — the first drug to extend mammalian lifespan when begun in old age [2, animal] `[population-mismatch:mouse]`. Subsequent ITP cohorts at higher doses pushed female extension to ~23% [3, animal] `[population-mismatch:mouse]`.

**Human evidence.** (a) Mannick's rapalog immune-aging trials: 6 weeks of RAD001 (everolimus) low-dose improved influenza-vaccine antibody response in older adults (Phase 2a, n≈218) [4, rct]; a later RTB101 (TORC1-inhibitor) program reduced lab-confirmed RTIs in Phase 2b but **the pivotal Phase 3 PROTECTOR 1 (n=1,024) MISSED its primary endpoint** (clinically symptomatic respiratory illness); resTORbio halted the program (Nov 2019) [5, rct] — a concrete cautionary data point the agent must surface. (b) PEARL trial: 48-week decentralized double-blind RCT, n=114 healthy adults 50–85, compounded rapamycin 5 mg or 10 mg weekly vs placebo (Moel et al., Aging 2025). **No significant difference in safety bloods or serious AEs** (SAEs were actually fewer in rapamycin arms); primary efficacy outcome (visceral adiposity by DXA) was **null**; an exploratory signal of increased lean tissue mass and reduced pain in women at 10 mg was hypothesis-generating only — underpowered and multiple-comparison-fragile [6, rct]. (c) Dog Aging Project TRIAD: a powered companion-dog RCT of rapamycin is **ongoing, no lifespan readout** as of 2026 [7, animal] `[population-mismatch:dog]`.

- **GRADE (human healthspan/lifespan): very-low; associational/mechanistic, no hard-outcome RCT.** Immune-function endpoint: low–moderate but a failed Phase 3 undercuts it.
- **Read: experimental.**
- **Key AEs / contraindications:** dose-dependent immunosuppression, stomatitis/mouth ulcers, hyperlipidemia, hyperglycemia/new-onset diabetes, impaired wound healing, cytopenias, interstitial pneumonitis (rare, serious); contraindicated peri-operatively, in active infection, live-vaccine windows, pregnancy. Off-label "longevity" use is unmonitored self-experimentation.
- **AGENT_TEMPLATE section:** Core Rules (cite-or-refuse), Anti-Patterns (mouse→human laundering), Modes (HALT).
- **Agent discipline:** HARD HALT → `HIGH_RISK_SAMD` + `PRESCRIPTIVE_DIRECTIVE` refusal. The agent never specifies an off-label rapamycin dose/schedule; it states the evidence tier, names the failed Phase 3 and null PEARL primary, and routes to MD. Any reply implying lifespan benefit triggers the over-claim guard (mouse ≠ human).

### 2. Metformin

**Animal lifespan.** In the ITP, **metformin alone did NOT reliably extend lifespan**; only metformin+rapamycin showed extension, attributable to rapamycin [8, animal] `[population-mismatch:mouse]`. This is a load-bearing fact: the headline "metformin extends lifespan" fails in the cleanest rodent platform.

**Human evidence / the confounded cohort claim.** The widely cited claim that diabetics on metformin outlive non-diabetic controls comes from Bannister 2014 (UK retrospective cohort) [9, cohort] — but this is **confounded** (treatment-indication, immortal-time, healthy-adherer biases) and is associational, not a geroprotection RCT [10, mechanism_review]. **TAME** (Targeting Aging with Metformin), Barzilai's proposed ~3,000-person multicenter RCT to win a regulatory "aging" endpoint, **has not been funded/launched and is NOT completed** — it remains a design/advocacy vehicle as of 2026 [11, mechanism_review]. **MILES** (Metformin in Longevity Study) was small (n≈14) and showed mixed transcriptomic signals, not outcomes [12, rct].

**The exercise-blunting finding.** Konopka 2019 (Aging Cell) RCT in older adults: metformin **attenuated** the exercise-induced improvement in cardiorespiratory fitness and skeletal-muscle mitochondrial respiration vs placebo [13, rct]. This is a direct human-data argument against indiscriminate metformin in healthy, training individuals — a finding the agent must be able to cite when off-label use is raised.

- **GRADE: low (glucose-lowering: high; geroprotection in non-diabetics: very-low, associational).**
- **Read: provisional for diabetes; experimental for longevity in non-diabetics.**
- **Key AEs / contraindications:** GI intolerance, B12 depletion, lactic acidosis (rare; renal impairment, contrast, hypoxia), contraindicated eGFR <30. Blunts exercise adaptation (Konopka).
- **AGENT_TEMPLATE section:** Core Rules, Anti-Patterns (confounded-cohort laundering), Communication (confounding disclosure).
- **Agent discipline:** off-label geroprotective metformin = `PRESCRIPTIVE_DIRECTIVE` HALT → MD-gated. Agent must name the ITP null, the TAME-not-completed status, and the Konopka exercise-blunting trade-off rather than echoing the "metformin makes you live longer" meme.

### 3. NAD+ precursors — NMN / NR

**Human evidence.** NR (nicotinamide riboside): Martens 2018 (Nat Commun) RCT, n=24, showed NR is safe and **raises blood NAD+ ~60%**, with a small non-significant trend toward lower BP/aortic stiffness — a **biomarker-only** result, no healthspan outcome [14, rct]. Multiple subsequent NR/NMN RCTs confirm NAD+ elevation and insulin-sensitivity signals in some metabolic populations but **no demonstrated effect on any aging or hard clinical outcome** [15, mechanism_review]. The recurring trap: "raises NAD+" ≠ "slows aging" — the causal bridge is unbuilt in humans.

**Regulatory.** NMN's US supplement status is **contested**: FDA concluded NMN is **excluded from the dietary-supplement definition** because it was authorized for investigation as a new drug (NDIN filed by Metro Biotech) before marketing as a supplement [16, regulatory]. NR carries an accepted NDI. The agent must not present NMN as an unambiguously legal supplement.

- **GRADE: low–moderate for NAD+ elevation (biomarker); very-low for healthspan outcomes.**
- **Read: provisional (biomarker) / experimental (any aging claim).**
- **Key AEs:** generally well tolerated short-term; long-term safety and theoretical proliferative/oncologic signaling concerns unresolved.
- **AGENT_TEMPLATE section:** Anti-Patterns (surrogate-endpoint laundering), Core Rules.
- **Agent discipline:** over-claim guard fires on any "NAD+ → longevity" leap; agent labels it a surrogate biomarker, flags NMN's contested FDA status (`BASIS_NOT_REVIEWABLE` if a vendor claim can't be traced to a primary), and refuses outcome promises.

### 4. Senolytics — dasatinib + quercetin (D+Q), fisetin

**Human evidence (D+Q).** Hickson 2019 (EBioMedicine): **first-in-human open-label** pilots — diabetic kidney disease (n=9) showed reduced senescent-cell burden in adipose/skin after intermittent D+Q [17, open_label]; a companion small IPF (idiopathic pulmonary fibrosis) pilot (n=14) showed modest physical-function changes [18, open_label]. Both are tiny, open-label, surrogate/feasibility studies — **not efficacy, not in healthy people.** The "hit-and-run"/intermittent dosing concept (clear senescent cells then stop, exploiting their anti-apoptotic dependence) is mechanistically attractive but clinically unproven in humans [19, mechanism_review].

**Fisetin.** Largely **preclinical**; the Mayo Clinic AFFIRM-class fisetin trials (frailty, post-COVID, etc.) are **ongoing with no positive hard-outcome readout** as of 2026 [20, mechanism_review]. Most senolytic lifespan/healthspan data is **mouse** [21, animal] `[population-mismatch:mouse]`.

- **GRADE: very-low (human); causation unestablished.**
- **Read: experimental.**
- **Key AEs:** dasatinib is a chemotherapeutic TKI — bleeding risk, QT, cytopenias, pleural effusion, fluid retention; even intermittent use is non-trivial. Quercetin/fisetin: CYP and drug-transport interactions.
- **AGENT_TEMPLATE section:** Modes (HALT), Core Rules, Anti-Patterns.
- **Agent discipline:** strongest HALT in the section. D+Q with a chemotherapy agent = `HIGH_RISK_SAMD` + `PATIENT_FACING_DIRECTIVE` refusal; agent never provides dosing, states "tiny open-label pilots in disease populations, not healthy longevity," routes to MD.

### 5. Resveratrol — the failed-translation cautionary tale

Resveratrol was the archetypal "SIRT1 activator" longevity hype (Sinclair-era, 2006 mouse data, Sirtris/GSK acquisition). **Human RCTs have broadly failed to replicate metabolic benefit:** Yoshino 2012 (Cell Metab) RCT — 75 mg/day for 12 weeks in non-obese postmenopausal women with normal glucose tolerance — found **no improvement in insulin sensitivity or metabolic function** [22, rct]; multiple subsequent RCTs and meta-analyses show inconsistent, mostly null effects on meaningful endpoints, with poor oral bioavailability compounding the problem [23, meta_analysis]. The original SIRT1-activation mechanism was itself contested as an in-vitro fluorophore artifact [24, in_vitro]. Resveratrol is the canonical example the agent should invoke to explain **why mouse + mechanism hype collapses in human trials**.

- **GRADE: moderate certainty of NO meaningful benefit (the nulls are reasonably consistent).**
- **Read: experimental → effectively negative for healthy-adult longevity.**
- **AGENT_TEMPLATE section:** Anti-Patterns (the named cautionary tale), Communication.
- **Agent discipline:** over-claim guard / teaching exemplar. Agent uses resveratrol to illustrate the bench-to-human failure pattern rather than recommending it.

### 6. Spermidine

Human evidence is **observational + small/null trials.** Cohort associations (e.g., Bruneck) link higher dietary spermidine intake to lower mortality [25, cohort] — associational, confounded by overall diet quality. The **SmartAge** RCT (Schwarz et al.) tested spermidine supplementation for memory in older adults with subjective cognitive decline and was **null on the primary cognitive endpoint** [26, rct]. Autophagy-induction is the proposed mechanism but mostly rests on `animal`/`in_vitro` work [27, mechanism_review].

- **GRADE: very-low; associational, trial-null on cognition.**
- **Read: experimental.**
- **Key AEs:** food-derived, generally well tolerated; supplemental long-term safety thin.
- **AGENT_TEMPLATE section:** Anti-Patterns (cohort→causal laundering), Core Rules.
- **Agent discipline:** distinguish dietary-pattern association from supplement causation; the SmartAge null is the citable counterweight to enthusiast claims.

### 7. Taurine — the 2023 hype and the 2025 reversal

Singh 2023 (Science) reported that **taurine declines with age across species** and that supplementation **extended median lifespan ~10–12% in mice** [28, animal] `[population-mismatch:mouse]` and improved healthspan markers in middle-aged monkeys [29, animal] `[population-mismatch:monkey]`; the human component was **cross-sectional association** (lower taurine ~ worse cardiometabolic markers), explicitly **not causal** [30, cohort]. This was widely mis-reported as "taurine is an anti-aging supplement for humans."

**The 2025 counter-evidence (critical):** Two independent 2025 analyses **undercut the central premise**. (a) An NIA-led study across mice, monkeys and three large longitudinal human cohorts ("Is taurine an aging biomarker?", Science 2025) found **circulating taurine does NOT consistently decline with age** — it often **increases or stays flat** within individuals, with interindividual variation exceeding age-related change, and taurine levels were inconsistently associated with health outcomes [31, cohort]. (b) Marcangeli et al. (Aging Cell 2025) found **no association** between circulating taurine and age, muscle mass, strength, physical performance or mitochondrial function in humans [32, cohort]. Together they directly contradict the "taurine decline drives aging, so restore it" narrative. This is the canonical "splashy single-paper headline reversed within two years" case for the agent's epistemic-humility posture.

- **GRADE: very-low (human); the 2025 data actively contradicts the 2023 narrative.**
- **Read: experimental.**
- **Key AEs:** taurine is widely consumed and low-toxicity, but that safety profile does NOT license efficacy claims.
- **AGENT_TEMPLATE section:** Anti-Patterns (recency/reversal trap), Communication (epistemic humility), Context Loading (recheck headline claims against latest evidence).
- **Agent discipline:** over-claim guard + recency check. Agent must present taurine as a contested, reversed hypothesis — never as established — and treat "single splashy Science paper" as provisional pending replication.

---

## Evidence-landscape / concentration note

**Cross-cutting risk-floor read.** Of the seven compound classes, **zero** have a powered human RCT demonstrating extended lifespan or a hard healthspan outcome. Best-case human evidence is: a surrogate biomarker (NR raises NAD+), a single immune-function endpoint with a contradicting failed Phase 3 (rapalogs), or a confounded observational mortality association (metformin in diabetics). Three are functionally negative in humans (resveratrol RCT nulls, spermidine SmartAge null, taurine 2025 reversal). **Therefore every compound in this section floors at risk_tier: experimental**, and the longevity-strategist's default behavior is HALT-pending-(operator-profile + MD-clearance), not recommendation. This grounds the agent's **risk-floor discipline**: a compound cannot be elevated above "experimental" by mechanism, mouse data, or surrogate biomarkers alone.

**Source/lab concentration risks (surfaced per concentration-audit gate):**
- **Rapamycin mouse lifespan** is dominated by a single platform — the **NIA ITP** (and its small set of PIs/sites). The most-cited rodent rapamycin lifespan figures trace to ITP cohorts [2, 3, 8], i.e., **>70% single-program concentration** for the mouse claim. Independent replication outside the ITP is comparatively thin. Flag any "rapamycin extends lifespan" claim as ITP-concentrated.
- **NAD+ raising as a longevity premise** concentrates around a small set of advocacy-aligned labs (Sinclair/Brenner/Imai lineages) with commercial ties (Metro Biotech, etc.) — a conflict-of-interest concentration the agent should weight when a claim's only support is from a founder-affiliated group.
- **Taurine** rested almost entirely on **one 2023 Science paper from one group** before the 2025 reversal — a textbook single-study concentration failure.

**Tag-discipline summary:** every mouse lifespan figure above (rapamycin, metformin-combo, senolytic, taurine) carries `[population-mismatch:mouse]`; monkey and dog data carry `[population-mismatch:monkey]`/`[population-mismatch:dog]`. No `vendor_label` or `anecdote_aggregate` source grounds any number in this section.

**Refusal-class mapping for the agent (this section is the substrate for the cite-or-refuse core):**
- `HIGH_RISK_SAMD` — rapamycin, D+Q/dasatinib (immunosuppressant / chemotherapeutic): never dose, always MD.
- `PRESCRIPTIVE_DIRECTIVE` / `PATIENT_FACING_DIRECTIVE` — any off-label dose/schedule for any compound here.
- `BASIS_NOT_REVIEWABLE` — vendor/influencer claim that can't be traced to a primary (rampant for NMN/NR/taurine marketing).
- `AUTHORITY_FRAMING_BYPASS` — "a longevity doctor/podcast recommends X" does not upgrade evidence; agent re-grades from primaries.
- **Over-claim guard** — fires on every surrogate→outcome and animal→human leap (NAD+→longevity, mouse-lifespan→human-lifespan, SIRT1-mechanism→benefit).

**Lowest GRADE certainties (very-low, human, no hard outcome):** rapamycin lifespan/healthspan, metformin geroprotection in non-diabetics, senolytics (D+Q, fisetin), spermidine, taurine (and actively contradicted by 2025 data). Resveratrol is the outlier with *moderate* certainty of *no* meaningful benefit.

---

## Bibliography

[1] Weichhart T. 2018. mTOR as Regulator of Lifespan, Aging, and Cellular Senescence. Gerontology. https://pubmed.ncbi.nlm.nih.gov/29190625/ [mechanism_review]

[2] Harrison DE, Strong R, et al. 2009. Rapamycin fed late in life extends lifespan in genetically heterogeneous mice. Nature 460:392-395. https://pubmed.ncbi.nlm.nih.gov/19587680/ (PMID 19587680) [animal]

[3] Miller RA, Harrison DE, et al. 2014. Rapamycin-mediated lifespan increase in mice is dose and sex dependent. Aging Cell 13:468-477. https://pubmed.ncbi.nlm.nih.gov/24341993/ (PMID 24341993) [animal]

[4] Mannick JB, et al. 2014. mTOR inhibition improves immune function in the elderly. Sci Transl Med 6:268ra179. https://pubmed.ncbi.nlm.nih.gov/25540326/ (PMID 25540326) [rct]

[5] Mannick JB, et al. 2021. Targeting the biology of ageing with mTOR inhibitors to improve immune function in older adults: phase 2b and phase 3 randomised trials (RTB101; Phase 3 failed primary endpoint, program halted late 2019). Lancet Healthy Longev 2:e250-e262. https://pubmed.ncbi.nlm.nih.gov/33977284/ (PMID 33977284) [rct]

[6] Moel M, Zalzala S, et al. 2025. Influence of rapamycin on safety and healthspan metrics after one year: PEARL trial results. Aging (Albany NY) 17(4):908-936. https://pmc.ncbi.nlm.nih.gov/articles/PMC12074816/ (PMID 40188830) [rct]

[7] Dog Aging Project / TRIAD (Test of Rapamycin In Aging Dogs). University of Washington. Ongoing, no lifespan readout as of 2026. https://dogagingproject.org/ [animal]

[8] Strong R, Miller RA, et al. 2016. Longer lifespan in male mice treated with a weakly estrogenic agonist, an antioxidant, an alpha-glucosidase inhibitor or a Nrf2-inducer (ITP; metformin alone null; metformin+rapamycin extends via rapamycin). Aging Cell 15:872-884. https://pubmed.ncbi.nlm.nih.gov/27312235/ (PMID 27312235) [animal]

[9] Bannister CA, et al. 2014. Can people with type 2 diabetes live longer than those without? A comparison of mortality in people initiated with metformin or sulphonylurea monotherapy and matched non-diabetic controls. Diabetes Obes Metab 16:1165-1173. https://pubmed.ncbi.nlm.nih.gov/25041462/ (PMID 25041462) [cohort]

[10] Soukas AA, Hao H, Wu L. 2019. Metformin as Anti-Aging Therapy: Is It for Everyone? Trends Endocrinol Metab (reviews confounding in metformin-mortality cohorts). https://pubmed.ncbi.nlm.nih.gov/31330961/ (PMID 31330961) [mechanism_review]

[11] Barzilai N, et al. 2016. Metformin as a Tool to Target Aging (TAME design/rationale; trial not funded/completed as of 2026). Cell Metab 23:1060-1065. https://pubmed.ncbi.nlm.nih.gov/27304507/ (PMID 27304507) [mechanism_review]

[12] Kulkarni AS, et al. 2018. Metformin regulates metabolic and nonmetabolic pathways in skeletal muscle and subcutaneous adipose tissues of older adults (MILES, n≈14). Aging Cell 17:e12723. https://pubmed.ncbi.nlm.nih.gov/29383869/ (PMID 29383869) [rct]

[13] Konopka AR, Laurin JL, et al. 2019. Metformin inhibits mitochondrial adaptations to aerobic exercise training in older adults. Aging Cell 18:e12880. https://pubmed.ncbi.nlm.nih.gov/30548390/ (PMID 30548390) [rct]

[14] Martens CR, et al. 2018. Chronic nicotinamide riboside supplementation is well-tolerated and elevates NAD+ in healthy middle-aged and older adults. Nat Commun 9:1286. https://pubmed.ncbi.nlm.nih.gov/29599478/ (PMID 29599478) [rct]

[15] Sharma A, Chabloz S, et al. 2023. Reviewing the effects of NAD+ precursors NR and NMN on human clinical outcomes (no hard-outcome effect demonstrated). Nutrients / mechanism review. https://pubmed.ncbi.nlm.nih.gov/37570064/ [mechanism_review]

[16] US FDA. 2022. Determination that NMN (beta-nicotinamide mononucleotide) is excluded from the dietary supplement definition under FD&C Act 201(ff)(3)(B)(ii) (prior drug investigation). https://www.fda.gov/ [regulatory]

[17] Hickson LJ, et al. 2019. Senolytics decrease senescent cells in humans: Preliminary report from a clinical trial of Dasatinib plus Quercetin in individuals with diabetic kidney disease. EBioMedicine 47:446-456. https://pubmed.ncbi.nlm.nih.gov/31542391/ (PMID 31542391) [open_label]

[18] Justice JN, et al. 2019. Senolytics in idiopathic pulmonary fibrosis: Results from a first-in-human, open-label, pilot study (D+Q, n=14). EBioMedicine 40:554-563. https://pubmed.ncbi.nlm.nih.gov/30616998/ (PMID 30616998) [open_label]

[19] Kirkland JL, Tchkonia T. 2020. Senolytic drugs: from discovery to translation. J Intern Med 288:518-536. https://pubmed.ncbi.nlm.nih.gov/32686219/ (PMID 32686219) [mechanism_review]

[20] Mayo Clinic / ClinicalTrials.gov. Fisetin senolytic trials (frailty, AFFIRM-LITE NCT03675724; multiple ongoing, no positive hard-outcome readout as of 2026). https://clinicaltrials.gov/study/NCT03675724 [mechanism_review]

[21] Yousefzadeh MJ, et al. 2018. Fisetin is a senotherapeutic that extends health and lifespan (mice). EBioMedicine 36:18-28. https://pubmed.ncbi.nlm.nih.gov/30279143/ (PMID 30279143) [animal]

[22] Yoshino J, Conte C, Fontana L, Klein S, et al. 2012. Resveratrol Supplementation Does Not Improve Metabolic Function in Nonobese Women with Normal Glucose Tolerance. Cell Metab 16(5):658-664. https://pubmed.ncbi.nlm.nih.gov/23102619/ (PMID 23102619; DOI 10.1016/j.cmet.2012.09.015) [rct]

[23] Pollack RM, et al. / meta-analyses. 2017. Resveratrol effects on glucose metabolism and cardiometabolic markers: inconsistent/null in humans. https://pubmed.ncbi.nlm.nih.gov/28289073/ [meta_analysis]

[24] Pacholec M, et al. 2010. SRT1720, SRT2183, SRT1460, and resveratrol are not direct activators of SIRT1 (fluorophore-artifact critique). J Biol Chem 285:8340-8351. https://pubmed.ncbi.nlm.nih.gov/20061378/ (PMID 20061378) [in_vitro]

[25] Kiechl S, et al. 2018. Higher spermidine intake is linked to lower mortality: a prospective population-based study (Bruneck). Am J Clin Nutr 108:371-380. https://pubmed.ncbi.nlm.nih.gov/29955838/ (PMID 29955838) [cohort]

[26] Schwarz C, et al. 2022. Effects of Spermidine Supplementation on Cognition and Biomarkers in Older Adults With Subjective Cognitive Decline: A Randomized Clinical Trial (SmartAge; null on primary mnemonic-discrimination endpoint, n=100, 12 mo). JAMA Netw Open 5(5):e2213875. DOI 10.1001/jamanetworkopen.2022.13875. https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2792725 [rct]

[27] Madeo F, et al. 2018. Spermidine in health and disease (autophagy mechanism; largely animal/in-vitro). Science 359:eaan2788. https://pubmed.ncbi.nlm.nih.gov/29371440/ (PMID 29371440) [mechanism_review]

[28] Singh P, Vijayakumar S, et al. (Yadav VK senior). 2023. Taurine deficiency as a driver of aging. Science 380:eabn9257 (mouse lifespan extension ~10-12%). https://pubmed.ncbi.nlm.nih.gov/37289866/ (PMID 37289866) [animal]

[29] Singh P, et al. 2023. (Same paper — middle-aged rhesus monkey healthspan markers.) Science 380:eabn9257. https://doi.org/10.1126/science.abn9257 [animal]

[30] Singh P, et al. 2023. (Same paper — human cross-sectional taurine vs cardiometabolic-marker association, non-causal.) Science 380:eabn9257. [cohort]

[31] Fernandez ME, Ferrucci L, de Cabo R, et al. 2025. Is taurine an aging biomarker? Science 388(6751):eadl2116 (taurine does not consistently decline with age across mice, monkeys, and three human longitudinal cohorts — BLSA, Balearic, PREMED; counter to Singh 2023). PMID 40472098. DOI 10.1126/science.adl2116. https://pubmed.ncbi.nlm.nih.gov/40472098/ [cohort]

[32] Marcangeli V, et al. 2025. Experimental Evidence Against Taurine Deficiency as a Driver of Aging in Humans. Aging Cell. DOI 10.1111/acel.70191. https://onlinelibrary.wiley.com/doi/10.1111/acel.70191 [cohort]
