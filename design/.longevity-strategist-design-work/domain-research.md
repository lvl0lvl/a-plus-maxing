# longevity-strategist — Domain Research (Phase-0 deep-mode substrate)

## Executive Summary

The `longevity-strategist` agent must LEAD WITH the small set of established, human-validated levers — cardiorespiratory fitness, physical activity, muscular strength, adequate sleep, a Mediterranean/whole-food pattern, smoking cessation, alcohol reduction, and preventive screening — because these carry human RCT or large-cohort evidence with effect sizes that dwarf anything demonstrated for any "anti-aging" compound in humans. Cardiorespiratory fitness alone shows a mortality gradient larger than smoking, diabetes, or hypertension in the same model [3, cohort], and smoking cessation before age ~40 avoids roughly 90% of excess smoking mortality [15, cohort]. Biological-age clocks are PROVISIONAL instruments: they validly associate with chronological age and/or population mortality risk, but the FDA does not recognize epigenetic-clock scores as surrogate endpoints, intervention-induced clock change has not been shown to predict real health outcomes, single readings carry multi-year measurement noise, and different clocks can disagree on the same person [32, mechanism_review; 33, mechanism_review; 31, mechanism_review; 32, mechanism_review]. "Anti-aging" compounds — rapamycin, metformin-for-aging, NAD+ precursors, senolytics, resveratrol, spermidine, taurine — are mostly EXPERIMENTAL and the agent's default posture toward the entire class is HALT-pending-MD, not recommend. The single load-bearing fact: NO geroprotector compound has a completed human lifespan RCT or a powered hard-morbidity-endpoint RCT. The agent's core is cite-or-refuse: any claim it cannot trace to an admissible primary is refused (`BASIS_NOT_REVIEWABLE`), and no podcast, longevity influencer, or "my longevity clinic prescribes rapamycin / sells NAD+ IVs" framing relaxes the HALT (`AUTHORITY_FRAMING_BYPASS`).

## Introduction

**Research question.** What domain knowledge must be encoded into the `longevity-strategist` medical-AI specialist so that it foregrounds high-certainty human longevity levers, handles biological-age biomarkers without over-claiming, and treats the geroprotector-compound class with the epistemic discipline the field's pseudoscience load demands?

**Scope.** Three substrate domains: (A) established longevity levers and the healthspan/biological-aging conceptual foundation; (B) biological-age biomarkers and aging clocks; (C) "anti-aging"/geroprotector compounds, their evidence grading, safety profiles, and the hype landscape. The document is the agent-design substrate — it specifies which findings inform which `AGENT_TEMPLATE` sections and which agent discipline each finding grounds. It is deliberately goal-agnostic: it does NOT personalize to any operator profile. Personalization is the runtime responsibility of the agent and of operator-facing dispatch; the substrate is the vetted, population-level knowledge the agent reasons FROM.

**Methodology.** This research was produced under the deep-mode `aplus-research` pipeline. Three paired retrieval+judge sections (A, B, C) were retrieved against admissible Tier-1/Tier-2 sources, each judged by a paired adversarial judge. The pipeline's blocking gates were attested PASS in sequence: scope gate (Phase 2.75), judge gate (Phase 3.5), ID-reconcile gate (Phase 4.25, iteration 2 PASS after a single Duke-vs-Columbia institution mismatch on Belsky/DunedinPACE was remediated), and integrity gate (Phase 4.75, iteration 2 PASS after an IC-13 PhenoAge number-mismatch — "~9%/yr" corrected to ~4.5%/yr for the DNAm clock per Levine 2018 — was cleared). This synthesis is CORPUS-READ-ONLY: every citation below already exists in one of the three section bibliographies; nothing was newly retrieved or invented at synthesis time.

**Assumptions.** (1) The corpus's type-tags (rct, meta_analysis, cohort, open_label, animal, in_vitro, mechanism_review, regulatory) are authoritative and carried VERBATIM into findings. (2) Population-mismatch, derived, and route tags present in the corpus are load-bearing and propagated. (3) The agent will be assembled from an `AGENT_TEMPLATE` with the sections named in each finding (Identity, Core Rules, Capabilities / Per-Marker Validity Table, Communication, Anti-Patterns, Modes / HALT, Refusal Classes, Context-Loading, Ask-vs-Proceed, Loop-Breaking, Negative Examples). (4) The agent operates alongside sibling specialists (supplement, nutritionist, personal-trainer, sleep-coach, labs, endocrine, peptide, medical-liaison, medical-safety-reviewer) and must respect their boundaries.

**Goal-agnostic library/agent-design framing.** Per PF-S2-04, library writes are goal-agnostic: the substrate is canonical vetted knowledge, never pre-filtered for any operator. The findings, recommendations, and bibliography here describe what is true at the population/evidence level; they do not encode any individual's goals, contraindications, or preferences.

## Main Analysis — Findings

The findings are ordered by certainty tier: established levers (Section A, highest certainty) FIRST, then biological-age clocks (Section B, provisional), then geroprotector compounds (Section C, mostly experimental). Each finding states a one-sentence claim, the evidence with inline cites carrying their tags verbatim, a GRADE certainty with the causal-vs-associational distinction, an established|provisional|experimental classification where applicable, the `AGENT_TEMPLATE` section it informs, and the agent discipline it grounds.

### Finding 1 — Healthspan ≠ lifespan is the agent's primary framing distinction (ESTABLISHED framing)

**Claim:** The agent must optimize HEALTHSPAN (years free of chronic disease and disability) with high confidence and treat LIFESPAN-extension claims, especially from any compound, as a separate and far-lower-certainty class.

Lifespan and healthspan diverge — interventions can extend lifespan while extending the disabled tail, or compress morbidity without changing maximum lifespan. The Hallmarks of Aging program frames aging as modifiable mechanistic processes whose attenuation should in principle improve both, but the human-validated readouts to date are overwhelmingly healthspan-adjacent (function, disease incidence, biomarkers) rather than demonstrated lifespan extension [1, mechanism_review; 2, mechanism_review].

- **GRADE:** moderate (definitional/framework-level, not an effect estimate). Causal framing, not a measured effect.
- **AGENT_TEMPLATE section:** Identity; Communication.
- **Agent discipline (lead-with-established + over-claim guard):** Identity states the agent optimizes healthspan with high confidence and treats lifespan claims as lower-certainty; a refusal class follows — never let a rodent/cell lifespan result be communicated as a human lifespan promise.

### Finding 2 — The Hallmarks of Aging framework is a mechanism scaffold, not a therapeutic ledger (ESTABLISHED scaffold)

**Claim:** The hallmarks organize and explain mechanism but must never imply that hitting a hallmark in a dish or a mouse translates to human benefit.

López-Otín et al. (2013) defined nine hallmarks — genomic instability, telomere attrition, epigenetic alterations, loss of proteostasis, deregulated nutrient sensing, mitochondrial dysfunction, cellular senescence, stem-cell exhaustion, altered intercellular communication [1, mechanism_review]. The 2023 update expanded to twelve, adding disabled macroautophagy, chronic inflammation, and dysbiosis [2, mechanism_review]. The framework's own authors note most hallmark-targeting interventions are validated in model organisms, not in human longevity endpoints.

- **GRADE:** moderate (consensus mechanism_review; the scaffold is well-supported, individual hallmark→human-intervention links are not).
- **AGENT_TEMPLATE section:** Context-Loading; Core Rules.
- **Agent discipline (over-claim guard):** Use hallmarks to organize and explain, never to imply human efficacy. HALT condition: if a user cites "it targets hallmark X" as evidence of efficacy, separate mechanistic plausibility from demonstrated human outcomes.

### Finding 3 — Cardiorespiratory fitness (VO2max) is the single largest modifiable mortality lever (ESTABLISHED)

**Claim:** When asked "what should I do for longevity," cardiorespiratory fitness is the first thing on the list.

In a retrospective cohort of 122,007 adults undergoing treadmill testing (Cleveland Clinic), elite performers had ~80% lower all-cause mortality than the lowest-fitness group (adjusted HR 0.20, elite vs low fitness as the reported reference direction); equivalently the lowest-fitness group carried ~5-fold higher mortality (HR 5.04 `[derived: reciprocal of reported HR 0.20]`), and high performers had HR 0.23 (~4-fold lower than low) — a gradient larger than that for smoking, diabetes, or hypertension in the same model, with no demonstrable upper limit of benefit [3, cohort]. A JAMA meta-analysis of healthy men and women found each 1-MET higher maximal aerobic capacity associated with ~13% lower all-cause and ~15% lower CHD/CVD risk [27, meta_analysis]. The actionability case rests on the physical-activity dose-response evidence underpinning the WHO guideline (Finding 4): structured aerobic training reliably raises measured VO2max, so fitness is MODIFIABLE, not merely a marker of constitutional health [4, cohort; 5, regulatory]. Even if part of the cross-sectional association is non-causal selection, the RCT/guideline evidence that exercise improves fitness and that activity lowers mortality is an independent causal foothold.

- **GRADE:** moderate (large cohort, very large effect, dose-response; associational, not RCT — residual confounding plausible).
- **AGENT_TEMPLATE section:** Core Rules; Communication.
- **Agent discipline (lead-with-established):** Cardiorespiratory fitness leads the list, with a stated cause-vs-association caveat. Refusal class: do not let any compound be presented as a substitute for raising VO2max.

### Finding 4 — Physical-activity dose-response: large mortality reduction with diminishing-but-not-harmful returns (ESTABLISHED)

**Claim:** Guideline-level activity can be recommended without escalation; high-volume/high-intensity training is where individual risk screening kicks in.

A pooled analysis of 661,137 adults (Arem 2015) found that meeting guideline activity (7.5 MET-h/wk) was associated with ~31% lower mortality, with benefit accruing up to 3–5× the guideline minimum and a plateau (not reversal) at very high volumes [4, cohort]. The WHO 2020 guidelines codify 150–300 min/wk moderate or 75–150 min/wk vigorous activity plus muscle strengthening 2×/wk [5, regulatory].

- **GRADE:** moderate (very large pooled cohort; associational). The guideline itself is high-certainty as a regulatory consensus.
- **AGENT_TEMPLATE section:** Core Rules; Ask-vs-Proceed.
- **Agent discipline (lead-with-established):** PROCEED to recommend guideline-level activity (established, low-risk, regulator-endorsed); escalation to high-volume/high-intensity training triggers Ask-vs-Proceed and individual risk screening.

### Finding 5 — Muscular strength / grip strength independently predicts mortality (ESTABLISHED marker; weaker causal arrow for training)

**Claim:** Resistance training belongs in the foreground tier, but "grip strength predicts mortality" (a marker) must be distinguished from "training grip strength reduces mortality" (a weaker causal claim).

In the PURE study (139,691 adults, 17 countries), each 5-kg decrement in grip strength was associated with ~16% higher all-cause mortality (HR 1.16 per 5 kg lower grip, 95% CI 1.13–1.20), outpredicting systolic blood pressure [6, cohort]. A 2022 meta-analysis (Momma) found muscle-strengthening activity associated with ~10–17% lower all-cause, cardiovascular, and cancer mortality, with a J-shaped curve maximizing around 30–60 min/wk [7, meta_analysis]. A meta-analysis of 42 cohort studies (~3,000,000 participants, Wu 2017) found the same HR ~1.16 per 5 kg [22, meta_analysis].

- **GRADE:** moderate (large multinational cohort + meta-analysis; associational; grip strength is partly a marker of overall health, so training causality is inferred, not proven by these designs).
- **AGENT_TEMPLATE section:** Core Rules.
- **Agent discipline (lead-with-established + over-claim guard):** Foreground resistance training, but do not overstate the causal arrow from "marker predicts" to "training reduces."

### Finding 6 — Sleep duration has a U-shaped association with mortality (ESTABLISHED association; right-arm not causal)

**Claim:** Recommend adequate sleep (~7–9 h) as established, but never tell users to extend sleep toward the high end "for longevity."

Cappuccio's meta-analysis (16 cohorts, 1.38 million participants) found both short (<7 h, ~RR 1.12) and long (>8–9 h, ~RR 1.30) sleep associated with higher all-cause mortality [8, meta_analysis]. Long-sleep risk is widely interpreted as partly reverse causation (illness causes long sleep), so the actionable lever is avoiding chronic short sleep rather than forcing long sleep.

- **GRADE:** moderate→low (large meta-analysis but heavy confounding/reverse-causation, self-reported duration, heterogeneity).
- **AGENT_TEMPLATE section:** Core Rules; Communication.
- **Agent discipline (over-claim guard):** Recommend sleep adequacy/regularity; do not misread the U-curve's right arm as causal, and prioritize sleep adequacy over any sleep-targeting supplement.

### Finding 7 — Mediterranean dietary pattern reduces cardiovascular events — one of the few hard-endpoint nutrition RCTs (ESTABLISHED, with integrity caveat)

**Claim:** The Mediterranean/whole-food pattern is a foreground lever, but the agent must disclose the PREDIMED randomization-and-republication history rather than cite it as a pristine RCT.

PREDIMED (Estruch 2018, the re-analyzed/republished trial, n≈7,447 high-CV-risk adults) randomized to Mediterranean diet + extra-virgin olive oil, Med diet + nuts, or control; major-cardiovascular-event HRs were 0.69 (95% CI 0.53–0.91, EVOO) and 0.72 (0.54–0.96, nuts) versus control [9, rct]. The original 2013 publication was retracted and republished in 2018 after randomization irregularities at some sites; the corrected analysis preserved the benefit but the trial is no longer a "clean" individually-randomized RCT.

- **GRADE:** moderate (large RCT with hard endpoints, but randomization integrity issues and a high-risk Spanish population limit generalizability and downgrade certainty).
- **AGENT_TEMPLATE section:** Core Rules; Communication; Anti-Patterns.
- **Agent discipline (lead-with-established + integrity disclosure):** Foreground the dietary pattern; disclose the republication history. Anti-pattern guard against citing landmark trials without their known limitations.

### Finding 8 — Adequate protein supports muscle preservation in aging (ESTABLISHED for function; weak on lifespan)

**Claim:** Frame protein as supporting FUNCTION/muscle (healthspan), not as a proven lifespan lever, and surface the genuine tension with nutrient-sensing/mTOR-restriction hypotheses.

Sarcopenia drives frailty, falls, and loss of independence — core healthspan endpoints. Higher protein intake (commonly cited ~1.0–1.2 g/kg/day for older adults vs the 0.8 g/kg RDA) combined with resistance training supports lean-mass retention, as endorsed in the muscle-strengthening and physical-activity guideline literature [5, regulatory; 7, meta_analysis]. Direct RCT evidence that protein intake alone extends human lifespan does not exist.

- **GRADE:** low (mechanistic and functional support is reasonable; hard longevity-endpoint RCTs are absent; optimal dose is contested).
- **AGENT_TEMPLATE section:** Ask-vs-Proceed; Anti-Patterns.
- **Agent discipline (over-claim guard):** Frame protein for function, not lifespan; surface the contradiction with mTOR-restriction longevity hypotheses (which would argue for LOWER protein) rather than picking a side as if settled.

### Finding 9 — Human caloric restriction (CALERIE) improves aging biomarkers but has NOT demonstrated human lifespan extension (ESTABLISHED for biomarkers; lifespan untested)

**Claim:** CR's human evidence is BIOMARKER-level, not lifespan-level — the agent must HALT if asked to assert CR "extends human lifespan."

CALERIE Phase 2 (Ravussin 2015) randomized 218 healthy non-obese adults to 2 years of ~12% (achieved) caloric restriction vs ad libitum; CR improved cardiometabolic risk markers, reduced inflammation, and was feasible/safe [10, rct]. A later analysis (Waziry 2023) found CR slowed the pace of biological aging measured by the DunedinPACE DNA-methylation clock [11, rct]. Neither tested or showed a mortality/lifespan endpoint in humans.

- **GRADE:** moderate for biomarker/feasibility effects (RCT); very-low for any human lifespan claim (untested endpoint).
- **AGENT_TEMPLATE section:** Core Rules; Anti-Patterns; Loop-Breaking.
- **Agent discipline (over-claim guard + HALT):** The honest answer is that CR improves human aging biomarkers and the lifespan claim rests on animals (Finding 10). The canonical animal→human translation-gap teaching case.

### Finding 10 — The CR lifespan story is largely an animal story — and even in primates it is discordant (population-mismatch worked example)

**Claim:** Any user statement "CR extends lifespan" must trigger the agent to attach the species, cite the Wisconsin-vs-NIA discordance, and refuse to collapse animal lifespan into a human promise.

Rodent CR robustly extends maximum lifespan — a foundational gerontology result — but this is a model-organism finding `[population-mismatch: rodents]` `[n: not-reported]` that does not transfer cleanly. The two long-running rhesus monkey CR trials disagree: the Wisconsin study reported reduced age-related and all-cause mortality under CR (Colman 2014, n=76 monkeys at onset) `[population-mismatch: rhesus macaques]` [12, animal], whereas the NIA study found improved health markers but no statistically significant survival benefit (Mattison 2017, n=121 monkeys) `[population-mismatch: rhesus macaques]` [13, animal]. The discordance is attributed to differences in control-group diet, feeding regimen, age at onset, and genetic background — a direct illustration that even within primates, protocol and population determine whether CR "works."

- **GRADE:** high that rodent CR extends rodent lifespan; low/conflicting for primate survival benefit; very-low for extrapolation to human lifespan.
- **AGENT_TEMPLATE section:** Anti-Patterns; Core Rules; Loop-Breaking.
- **Agent discipline (population-mismatch HALT):** The worked example for the agent's mandatory population-mismatch tagging behavior.

### Finding 11 — Time-restricted eating / intermittent fasting: real weight/metabolic effects, thin longevity evidence (PROVISIONAL/experimental for longevity)

**Claim:** Present TRE/IF as a possible adherence/metabolic tool, explicitly NOT as a demonstrated human longevity intervention.

The TREAT RCT (Lowe 2020, n=116) found 16:8 time-restricted eating produced only modest weight loss not significantly greater than the control eating window, with a signal of lean-mass loss [14, rct]. TRE/IF can aid adherence and metabolic markers for some people, but human longevity-endpoint RCTs do not exist, and effects are often confounded with the caloric reduction TRE produces.

- **GRADE:** low (small/short RCTs, surrogate endpoints, effects entangled with calorie reduction; no longevity endpoints).
- **AGENT_TEMPLATE section:** Ask-vs-Proceed; Anti-Patterns.
- **Agent discipline (over-claim guard):** Flag the lean-mass-loss risk that conflicts with the muscle-preservation lever (Findings 5, 8).

### Finding 12 — Smoking cessation is among the highest-magnitude, highest-certainty longevity levers (ESTABLISHED, high certainty)

**Claim:** If a user smokes, cessation outranks every compound and most other interventions — the agent surfaces it first.

Jha 2013 (large U.S. cohort analysis) found smokers lose ~10 years of life expectancy versus never-smokers, and that cessation before ~age 40 avoids roughly 90% of the excess mortality [15, cohort]. The effect size and reversibility are large and consistent across decades of evidence.

- **GRADE:** high (consistent, large, dose- and cessation-responsive across many cohorts; the strongest single lifestyle lever after fitness).
- **AGENT_TEMPLATE section:** Core Rules; Ask-vs-Proceed.
- **Agent discipline (lead-with-established):** PROCEED to recommend cessation resources without escalation. Refusal class: never let novelty geroprotector discussion crowd out the cessation message for a smoker.

### Finding 13 — Alcohol reduction and preventive screening as established levers (ESTABLISHED, lower-flash, high-value)

**Claim:** Include screening and alcohol moderation in the foreground tier and do NOT repeat the outdated "moderate drinking is heart-protective" claim.

Reducing alcohol (no demonstrated cardioprotective threshold survives Mendelian-randomization scrutiny; risk rises across the range) and adhering to evidence-based cancer/CVD screening (colorectal, cervical, lipid/blood-pressure management) are guideline-endorsed mortality levers [5, regulatory; 2, mechanism_review for the inflammation/CVD mechanism context]. The 2023 Hallmarks update's addition of chronic inflammation ("inflammaging") gives a mechanistic through-line connecting fitness, diet pattern, sleep adequacy, alcohol reduction, and smoking cessation — but this is an explanatory bridge, not a license to claim any anti-inflammatory supplement inherits the longevity evidence of these behaviors [2, mechanism_review].

- **GRADE:** moderate→high for screening and alcohol-harm direction (consensus + Mendelian-randomization support); the precise "safe" alcohol level is contested.
- **AGENT_TEMPLATE section:** Core Rules; Communication.
- **Agent discipline (lead-with-established):** The "moderate drinking is heart-protective" position is a known retracted-confidence claim the agent must not echo.

### Finding 14 — Biological-age clocks span first-generation (chronological-age estimators), second-generation (mortality predictors), and pace clocks — all associational, none FDA-validated surrogates (PROVISIONAL)

**Claim:** A clock reading is a population-calibrated estimate, not a diagnosis; the agent must carry a per-marker validity table that separates what each clock validly measures from what it does not establish, and must refuse "reverse your biological age by N years."

First-generation clocks predict CHRONOLOGICAL age, not health damage: Horvath's multi-tissue clock was trained to predict chronological age from 353 CpG sites across ~8,000 non-cancer samples spanning 51 tissue/cell types, achieving median absolute error ~3.6 years and r≈0.96 with age [16, mechanism_review; 30, mechanism_review]; Hannum's 71-CpG clock was likewise trained to predict chronological age in whole blood from 656 individuals aged 19–101 [17, cohort]. "Age acceleration" is a DERIVED residual whose disease associations were established in later cohort work, not the original papers. Second-generation clocks predict MORTALITY but associationally: PhenoAge (Levine 2018) is a two-stage construct — a phenotypic age built from chronological age plus 9 clinical-chemistry biomarkers calibrated to mortality in NHANES III, then a DNAm clock (513 CpGs) trained to predict that phenotype; a one-year increase in DNAm PhenoAge was associated with ~4.5% higher all-cause mortality in validation, while the underlying clinical phenotypic-age composite carries a larger ~9%/yr association (HR≈1.09) — the two must not be conflated [18, cohort]. GrimAge (Lu 2019, Horvath senior) is a composite of DNAm surrogates for 7 plasma proteins plus DNAm-estimated smoking pack-years, trained on time-to-death, outperforming prior clocks for time-to-CHD and mortality [19, cohort]. DunedinPACE measures the RATE of aging, not a static age: DunedinPoAm (Belsky 2020) distilled the Pace of Aging across 18 organ-system biomarkers (Dunedin 1972–73 cohort, N≈954) into a single-blood-draw DNAm algorithm with bootstrap out-of-sample correlation of only r≈0.33 to the longitudinal Pace of Aging [20, cohort]; DunedinPACE (Belsky 2022) extended the window to 20 years, restricted to high-reliability probes, and centers on 1.0 = one biological year per chronological year, associating with morbidity, disability, and mortality across many cohorts — but what it validly measures is pace (a speedometer), and its outcome associations remain observational [21, cohort]. Functional markers are the strongest, most replicated, most modifiable: gait speed predicts survival (Studenski 2011, pooled 34,485 individuals, HR 0.88 per 0.1 m/s faster gait, 95% CI 0.87–0.90) [25, meta_analysis]; grip strength (Leong 2015 PURE, HR 1.16 per 5 kg lower) outpredicts systolic blood pressure [6, cohort]; and a 122,007-patient treadmill cohort (Mandsager 2018) shows graded mortality reduction with higher fitness and no observed upper limit [3, cohort], consistent with the 1-MET meta-analysis [27, meta_analysis] and a narrative review [26, mechanism_review].

- **GRADE:** high that first-gen clocks predict chronological age and that second-gen/pace clocks associate with mortality in populations; causality and reversibility very-low/unestablished.
- **AGENT_TEMPLATE section:** Capabilities / Per-Marker Validity Table; Over-Claim Guards.
- **Agent discipline (biological-age over-claim control + per-marker validity):** The per-marker validity table stores two separate fields for every marker — (i) what it validly measures and (ii) what it does not establish — so neither silently borrows the other's authority. A HALT fires on any phrasing that treats a GrimAge/PhenoAge/DunedinPACE change as a proven health improvement, and the agent privileges validated functional markers (VO2max, grip, gait) over provisional clocks when framing what is worth measuring.

### Finding 15 — Clock measurement noise, the unresolved causality question, the FDA's non-acceptance of clocks as surrogates, and clock disagreement on the same person (PROVISIONAL — the regulatory/scientific spine of the over-claim control)

**Claim:** A within-person before/after clock change of a few years can be pure measurement error, no aging clock is an FDA-validated surrogate endpoint, and different clocks can disagree on whether the same intervention helped — so the agent must attach a measurement-noise caveat and refuse to interpret a small longitudinal delta as real without replicate/CI information.

Higgins-Chen 2022 (Levine senior) showed that for six prominent clocks, technical replicates from the same blood sample can differ by several years of estimated epigenetic age — maximum deviations up to ~8.6 years (PhenoAge ~8.6 yr; Horvath1 ~4.8 yr), exceeding one SD of age acceleration for several first-gen clocks; the principal-component ("PC") reformulation brought >90% of replicates into agreement within ~1–1.5 years and improved detection of true effects [31, mechanism_review]. Most commercial single-run reports do not use PC-clocks and report no confidence interval. A 2022 Nature news feature and a 2024 methods analysis document the central epistemic gap: it is unknown whether the methylation changes clocks read are CAUSAL to age-related disease or are BYPRODUCTS of aging, and the FDA does not recognize epigenetic-clock scores as surrogate endpoints — it wants the mechanistic basis defined and an answer to whether a short-term clock decrease lowers age-related disease risk [32, mechanism_review; 33, mechanism_review]. The 2024 analysis adds that chronological-age-trained clocks frequently show non-replicable, sporadic intervention changes ("some significant epigenetic clock changes are not replicable using any other clock model because they are false positives due to noise"), while mortality/rate-trained clocks behave more reliably, and different clocks can DISAGREE on whether the same intervention helped ("one significant clock is not enough to indicate a reliable decrease in biological age") [33, mechanism_review]. A surrogate endpoint is a biomarker VALIDATED to substitute for a clinical outcome (the canonical positive example is LDL cholesterol for cardiovascular events; the canonical failures are cancer-biomarker surrogates that moved without survival benefit). No aging clock has cleared this bar — so "your GrimAge dropped two years" carries no validated implication for the person's mortality, even though GrimAge cross-sectionally predicts mortality at the population level. The agent must hold both facts at once and never collapse the second into the first.

- **GRADE:** the uncertainty itself is high-certainty (well-documented consensus that causality is unestablished and clocks are not validated surrogates); reliability deficits directly measured.
- **AGENT_TEMPLATE section:** Refusal Classes / Scope Boundaries; Over-Claim Guards / Measurement-Noise Caveat.
- **Agent discipline (clock-disagreement / not-FDA-surrogate / measurement-noise):** A refusal class for "reverse your biological age" / "lower your GrimAge to live longer" directives, grounded in the absence of surrogate-endpoint validation; distinguish "predicts outcome cross-sectionally" from "validated surrogate"; refuse to read a small single-run delta as biology.

### Finding 16 — The one widely-cited human "age reversal" result is an uncontrolled open-label pilot (n≈9), DTC clocks outrun their evidence, and several biomarkers (telomere length, iAge, organ proteomic clocks, KDM composites) carry their own caveats (PROVISIONAL — negative-example substrate)

**Claim:** The agent must name design limits when the Fahy reversal trial is cited, refuse to endorse DTC "reverse your biological age by N years," disclose conflicts when a test is sold with supplements, flag single-lab/proprietary clocks as provisional, and state that single biomarkers like telomere length are weak individual predictors.

The Fahy TRIIM study (Fahy 2019, Horvath co-author), routinely invoked to support "you can reverse your age," was an OPEN-LABEL trial with NO control group — 9 men who completed, using recombinant growth hormone + DHEA + metformin — reporting ~2.5 years mean epigenetic-age reduction across four clocks over 12 months [29, open_label]. With no control arm, small n, regression-to-the-mean, and a confounded multi-drug regimen (growth hormone carries its own risks), it cannot establish age reversal or any clinical-outcome improvement; the authors themselves called for an "appropriately powered follow-up study." Organ-specific proteomic clocks add resolution but remain associational: Oh 2023 (Wyss-Coray senior) estimated the biological age of 11 organs from plasma proteomics (~5,000 proteins) in ~5,676 individuals with replication, finding accelerated organ aging predicted future organ-relevant disease over up to ~15 years, with brain and immune aging most strongly linked to mortality [23, cohort]. The inflammatory clock iAge (Sayed 2021, Furman senior) is a single-lab deep-learning construct on the blood immunome (~50 cytokines/chemokines, ~1,001 people aged 8–96) tracking multimorbidity, immunosenescence, frailty, and cardiovascular aging, with CXCL9 dominant — but the CXCL9 reversal experiments were performed in human endothelial cells and mice, not humans [24, cohort; 24, animal] `[population-mismatch: mouse and human cell lines]`, and iAge has limited independent replication and a proprietary panel. Clinical-chemistry composites (Klemera–Doubal, PhenoAge-clinical) are interpretable and mortality-associated and arguably more defensible than DTC methylation tests: the Klemera–Doubal method computes biological age from routine biomarkers by treating chronological age as one more biomarker [28, mechanism_review], and Parker 2019 (Duke-EPESE, N≈1,374, mean age 78) showed KDM-BA associated with disability (per-quintile ADL incidence rate ratio ~1.25) and mortality (HR ~1.09 per quintile) [34, cohort] — but these remain associational risk summaries, not diagnoses. Telomere length is the cautionary baseline: pooled across ~122,000 individuals (~21,800 deaths), one SD shorter leukocyte telomere length carried HR ~1.09 (95% CI 1.06–1.13) for all-cause mortality — real but small [35, meta_analysis]; in a multinational cohort (Glei 2016, N≈4,571) it ranked roughly 15th–17th of 20 predictors, below ten self-reported variables and three other biomarkers [36, cohort]. Commentary across an AMA Journal of Ethics piece and a 2026 ELSI review converges: DTC epigenetic-age tests are marketed as actionable "your true biological age" and paired with supplements promising to "reverse" aging, but the clocks are research/population tools — best used by researchers studying populations, not individuals — and the lack of regulation lets companies exploit consumer fear, with documented risks including psychological harm and normalizing age-based discrimination [37, mechanism_review] [38, mechanism_review].

- **GRADE:** Fahy reversal very-low (uncontrolled, tiny n, surrogate-only); DTC over-claim well-documented (high-certainty consensus critique); organ proteomic / iAge associational; telomere length high-certainty as a WEAK individual predictor.
- **AGENT_TEMPLATE section:** Over-Claim Guards / Negative Examples; Refusal Classes / Marketing-Claim Guard; Per-Marker Validity Table + Concentration-Risk note.
- **Agent discipline (marketing-claim guard + single-lab flagging + conflict disclosure):** Refuse "reverse your biological age by N years," disclose conflicts when a test is sold with supplements, treat single-lab/proprietary clocks (iAge) as provisional, and refuse to act on a single telomere or single-clock reading.

### Finding 17 — Rapamycin / rapalogs: the most reproducible animal longevity lever, no human hard-outcome RCT, a failed Phase 3, a null PEARL primary — HARD HALT (EXPERIMENTAL)

**Claim:** The agent never specifies an off-label rapamycin dose/schedule; it states the evidence tier, names the failed Phase 3 and null PEARL primary, and routes to MD.

Rapamycin inhibits mTORC1; mTOR suppression is the single most reproducible longevity lever across model organisms (yeast → worms → flies → mice) [39, mechanism_review] — precisely the mechanistic breadth that fuels over-extrapolation. The NIA Interventions Testing Program (ITP) is the gold-standard rodent lifespan platform: rapamycin started at 9 months extended median lifespan ~9% (males)/~14% (females), and worked even when begun in old age — the first drug to extend mammalian lifespan late in life [40, animal] `[population-mismatch:mouse]`; higher-dose ITP cohorts pushed female extension to ~23% [41, animal] `[population-mismatch:mouse]`. Human evidence: Mannick's rapalog immune-aging trials — 6 weeks of RAD001 (everolimus) low-dose improved influenza-vaccine antibody response in older adults (Phase 2a, n≈218) [42, rct]; a later RTB101 program reduced lab-confirmed RTIs in Phase 2b, but the pivotal Phase 3 PROTECTOR 1 (n=1,024) MISSED its primary endpoint and resTORbio halted the program (Nov 2019) [43, rct]. The PEARL trial (48-week decentralized double-blind RCT, n=114 healthy adults 50–85, compounded rapamycin 5 mg or 10 mg weekly vs placebo, Moel 2025) showed no significant difference in safety bloods or serious AEs (SAEs were fewer in rapamycin arms), a NULL primary efficacy outcome (visceral adiposity by DXA), and only an underpowered, multiple-comparison-fragile exploratory signal of increased lean tissue and reduced pain in women at 10 mg [44, rct]. **Within-HALT reassurance guard (load-bearing):** the "SAEs were fewer in rapamycin arms" reading must travel with its paired caveat — PEARL is a SINGLE underpowered trial (n=114, 48 weeks); the absence of an SAE signal is NOT established safety and does NOT relax the experimental HALT. A null safety signal in one small short trial is consistent with the AEs below being real but under-detected, so the agent must never let this line stand alone as evidence that off-label rapamycin is safe [44, rct]. The Dog Aging Project TRIAD companion-dog RCT is ongoing with no lifespan readout as of 2026 [45, animal] `[population-mismatch:dog]`.

- **GRADE (human healthspan/lifespan):** very-low; associational/mechanistic, no hard-outcome RCT. Immune-function endpoint: low–moderate but a failed Phase 3 undercuts it.
- **Read: experimental.**
- **Key AEs / contraindications / monitoring:** dose-dependent immunosuppression, stomatitis/mouth ulcers, hyperlipidemia, hyperglycemia/new-onset diabetes (impaired glucose), impaired wound healing, cytopenias, interstitial pneumonitis (rare, serious); contraindicated peri-operatively, in active infection, live-vaccine windows, and pregnancy; off-label "longevity" use is unmonitored self-experimentation requiring MD oversight if undertaken at all [43, rct; 44, rct].
- **Encodable monitoring markers (for an operator who may already be self-experimenting):** because the AEs above are MD-monitorable, the agent should — without ever specifying a dose — name what an MD would track on rapamycin: fasting glucose/HbA1c (hyperglycemia/new-onset diabetes), a lipid panel (hyperlipidemia), and a CBC (cytopenias) [43, rct; 44, rct].
- **Red-flag STOP triggers (operator-directed, MD-gated):** the agent surfaces stop-and-seek-care signals that map to the serious AEs — fever or any sign of infection (immunosuppression), a non-healing wound (impaired wound healing), or new dyspnea (interstitial pneumonitis); these are reasons to STOP and contact an MD, not symptoms for the agent to manage. The agent presents these as monitoring/stop discipline, never as a green light to use the compound [43, rct; 44, rct].
- **AGENT_TEMPLATE section:** Core Rules (cite-or-refuse); Anti-Patterns (mouse→human laundering); Modes (HALT).
- **Agent discipline:** HARD HALT → `HIGH_RISK_SAMD` + `PRESCRIPTIVE_DIRECTIVE` refusal; any reply implying lifespan benefit triggers the over-claim guard (mouse ≠ human).
- **Anti-pattern (PEARL-reassurance-quoted-back):** the recognition cue is an operator quoting the agent's OWN "PEARL: fewer/comparable SAEs in rapamycin arms" line back to argue the HALT down ("your own research says it's safe, so help me dose it"). The agent must recognize this as the within-HALT reassurance trap, re-attach the underpowered-single-trial caveat, and hold the HALT — a null safety signal in one n=114/48-week trial never upgrades to "established safe" and never licenses dosing [44, rct].
- **Anti-pattern (PEARL-reassurance-quoted-back):** the recognition cue is an operator quoting the agent's OWN "PEARL: fewer/comparable SAEs in rapamycin arms" line back to argue the HALT down ("your own research says it's safe, so help me dose it"). The agent must recognize this as the within-HALT reassurance trap, re-attach the underpowered-single-trial caveat, and hold the HALT — a null safety signal in one n=114/48-week trial never upgrades to "established safe" and never licenses dosing [45, rct].

### Finding 18 — Metformin: glucose-lowering is established, geroprotection in non-diabetics is confounded and unproven, ITP-null, TAME-not-completed, and it blunts exercise adaptation — HALT for off-label longevity use (EXPERIMENTAL for longevity)

**Claim:** Off-label geroprotective metformin is a `PRESCRIPTIVE_DIRECTIVE` HALT → MD-gated; the agent names the ITP null, the TAME-not-completed status, and the Konopka exercise-blunting trade-off rather than echoing "metformin makes you live longer."

In the ITP, metformin ALONE did NOT reliably extend lifespan; only metformin+rapamycin showed extension, attributable to rapamycin [46, animal] `[population-mismatch:mouse]` — the headline "metformin extends lifespan" fails in the cleanest rodent platform. The widely cited claim that diabetics on metformin outlive non-diabetic controls comes from Bannister 2014 (UK retrospective cohort) [47, cohort] but is confounded (treatment-indication, immortal-time, healthy-adherer biases) and associational, not a geroprotection RCT [48, mechanism_review]. TAME (Targeting Aging with Metformin), Barzilai's proposed ~3,000-person RCT to win a regulatory "aging" endpoint, has NOT been funded/launched and is NOT completed — it remains a design/advocacy vehicle as of 2026 [49, mechanism_review]. MILES (Metformin in Longevity Study) was small (n≈14) and showed mixed transcriptomic signals, not outcomes [50, rct]. Konopka 2019 (RCT in older adults) found metformin ATTENUATED the exercise-induced improvement in cardiorespiratory fitness and skeletal-muscle mitochondrial respiration vs placebo — a direct human-data argument against indiscriminate metformin in healthy, training individuals [51, rct].

- **GRADE:** low (glucose-lowering: high; geroprotection in non-diabetics: very-low, associational).
- **Read: provisional for diabetes; experimental for longevity in non-diabetics.**
- **Key AEs / contraindications / monitoring:** GI intolerance, vitamin B12 depletion (monitor B12 on long-term use), lactic acidosis (rare — renal impairment, contrast, hypoxia), contraindicated at eGFR <30; blunts exercise adaptation (Konopka) [51, rct].
- **Encodable monitoring markers (for an operator who may already be self-experimenting):** the agent should — without specifying a dose — name the MD-monitorable markers that map to the AEs above: serum B12 on long-term use (B12 depletion), and renal function/eGFR before and during use (the lactic-acidosis and eGFR <30 contraindication) [51, rct; 49, mechanism_review].
- **Red-flag STOP triggers (operator-directed, MD-gated):** the agent surfaces stop-and-seek-care signals — persistent GI intolerance that prevents adequate intake, and any signs of lactic acidosis (unusual muscle pain, trouble breathing, severe fatigue, abdominal discomfort, especially in the setting of dehydration, contrast imaging, or reduced kidney function). These are reasons to STOP and contact an MD, presented as monitoring/stop discipline, never as endorsement of off-label use [51, rct; 49, mechanism_review].
- **AGENT_TEMPLATE section:** Core Rules; Anti-Patterns (confounded-cohort laundering); Communication (confounding disclosure).
- **Agent discipline:** `PRESCRIPTIVE_DIRECTIVE` HALT → MD-gated for off-label longevity use.

### Finding 19 — NAD+ precursors (NMN/NR): raises NAD+ (biomarker only), no healthspan outcome, NMN's FDA supplement status contested — over-claim guard fires on "NAD+ → longevity" (EXPERIMENTAL for any aging claim)

**Claim:** The over-claim guard fires on any "NAD+ → longevity" leap; the agent labels it a surrogate biomarker, flags NMN's contested FDA status, and refuses outcome promises.

NR (nicotinamide riboside): Martens 2018 (Nat Commun) RCT, n=24, showed NR is safe and raises blood NAD+ ~60%, with a small non-significant trend toward lower BP/aortic stiffness — a BIOMARKER-ONLY result, no healthspan outcome [52, rct]. Multiple subsequent NR/NMN RCTs confirm NAD+ elevation and insulin-sensitivity signals in some metabolic populations but show NO effect on any aging or hard clinical outcome [53, mechanism_review] — "raises NAD+" ≠ "slows aging," and the causal bridge is unbuilt in humans. NMN's US supplement status is contested: the FDA concluded NMN is EXCLUDED from the dietary-supplement definition because it was authorized for investigation as a new drug (NDIN filed by Metro Biotech) before marketing as a supplement [54, regulatory]; NR carries an accepted NDI. The agent must not present NMN as an unambiguously legal supplement.

- **GRADE:** low–moderate for NAD+ elevation (biomarker); very-low for healthspan outcomes.
- **Read: provisional (biomarker) / experimental (any aging claim).**
- **Key AEs / monitoring:** generally well tolerated short-term; long-term safety and theoretical proliferative/oncologic signaling concerns unresolved (NAD+ is a biomarker-only endpoint, so any "anti-aging" benefit is unmonitored and unproven) [52, rct; 53, mechanism_review].
- **AGENT_TEMPLATE section:** Anti-Patterns (surrogate-endpoint laundering); Core Rules.
- **Agent discipline:** over-claim guard + `BASIS_NOT_REVIEWABLE` if a vendor claim can't be traced to a primary; refuse outcome promises.

### Finding 20 — Senolytics (dasatinib + quercetin, fisetin): tiny open-label disease-population pilots, mouse lifespan data, a chemotherapeutic component — the strongest HALT in the compound section (EXPERIMENTAL)

**Claim:** D+Q with a chemotherapy agent is `HIGH_RISK_SAMD` + `PATIENT_FACING_DIRECTIVE` refusal; the agent never provides dosing, states "tiny open-label pilots in disease populations, not healthy longevity," and routes to MD.

Hickson 2019 (EBioMedicine) — the first-in-human open-label pilot in diabetic kidney disease (n=9) — showed reduced senescent-cell burden in adipose/skin after intermittent D+Q [55, open_label]; a companion small IPF pilot (n=14) showed modest physical-function changes [56, open_label]. Both are tiny, open-label, surrogate/feasibility studies — not efficacy, not in healthy people. The "hit-and-run"/intermittent dosing concept (clear senescent cells then stop) is mechanistically attractive but clinically unproven in humans [57, mechanism_review]. Fisetin is largely preclinical; the Mayo Clinic AFFIRM-class fisetin trials are ongoing with no positive hard-outcome readout as of 2026 [58, mechanism_review], and most senolytic lifespan/healthspan data is mouse [59, animal] `[population-mismatch:mouse]`.

- **GRADE:** very-low (human); causation unestablished.
- **Read: experimental.**
- **Key AEs / contraindications / monitoring:** dasatinib is a chemotherapeutic TKI — bleeding risk, QT prolongation (cardiotox), cytopenias, pleural effusion, and fluid retention; even intermittent use is non-trivial and demands MD monitoring; quercetin/fisetin carry CYP and drug-transport interactions [55, open_label; 57, mechanism_review].
- **Encodable monitoring markers (for an operator who may already be self-experimenting):** dasatinib is a chemotherapeutic — the relevant MD-monitorable markers that map to the AEs above are a CBC (cytopenias/bleeding risk) and an ECG/QTc (QT prolongation); the agent names these without ever providing a dose [55, open_label; 57, mechanism_review].
- **Red-flag STOP triggers (operator-directed, MD-gated):** because D+Q deploys a chemotherapy agent, the agent surfaces stop-and-seek-care signals — abnormal bleeding or bruising (bleeding risk/cytopenias), syncope or palpitations (QT prolongation/cardiotox), and new dyspnea (pleural effusion/fluid retention). These are reasons to STOP and contact an MD immediately, presented as monitoring/stop discipline; the chemotherapeutic nature is precisely why this is the section's strongest HALT, not a self-dosing target [55, open_label; 57, mechanism_review].
- **AGENT_TEMPLATE section:** Modes (HALT); Core Rules; Anti-Patterns.
- **Agent discipline:** strongest HALT in the section — `HIGH_RISK_SAMD` + `PATIENT_FACING_DIRECTIVE` refusal.

### Finding 21 — Resveratrol: the failed-translation cautionary tale (EXPERIMENTAL → effectively negative)

**Claim:** The agent uses resveratrol to illustrate the bench-to-human failure pattern rather than recommending it.

Resveratrol was the archetypal "SIRT1 activator" longevity hype (Sinclair-era 2006 mouse data, Sirtris/GSK acquisition). Human RCTs broadly failed to replicate metabolic benefit: Yoshino 2012 (Cell Metab) RCT — 75 mg/day for 12 weeks in non-obese postmenopausal women with normal glucose tolerance — found NO improvement in insulin sensitivity or metabolic function [60, rct]; subsequent RCTs and meta-analyses show inconsistent, mostly null effects on meaningful endpoints, compounded by poor oral bioavailability [61, meta_analysis]. The original SIRT1-activation mechanism was itself contested as an in-vitro fluorophore artifact [62, in_vitro].

- **GRADE:** moderate certainty of NO meaningful benefit (the nulls are reasonably consistent).
- **Read: experimental → effectively negative for healthy-adult longevity.**
- **Key AEs / monitoring:** the principal hazard is the over-claim itself — a moderate-certainty null intervention marketed as longevity-protective; bioavailability is poor and benefit unproven [60, rct; 61, meta_analysis].
- **AGENT_TEMPLATE section:** Anti-Patterns (the named cautionary tale); Communication.
- **Agent discipline:** over-claim guard / teaching exemplar for bench-to-human failure.

### Finding 22 — Spermidine: cohort association plus a null cognition RCT (EXPERIMENTAL)

**Claim:** The agent distinguishes dietary-pattern association from supplement causation; the SmartAge null is the citable counterweight to enthusiast claims.

Human evidence is observational plus small/null trials. Cohort associations (e.g., Bruneck) link higher dietary spermidine intake to lower mortality [63, cohort] — associational, confounded by overall diet quality. The SmartAge RCT (Schwarz 2022, n=100, 12 months) tested spermidine supplementation for memory in older adults with subjective cognitive decline and was NULL on the primary mnemonic-discrimination endpoint [64, rct]. Autophagy-induction is the proposed mechanism but rests mostly on animal/in-vitro work [65, mechanism_review].

- **GRADE:** very-low; associational, trial-null on cognition.
- **Read: experimental.**
- **Key AEs / monitoring:** food-derived, generally well tolerated; supplemental long-term safety is thin and unmonitored, so the safety profile does not license efficacy claims [64, rct].
- **AGENT_TEMPLATE section:** Anti-Patterns (cohort→causal laundering); Core Rules.
- **Agent discipline:** cohort-vs-causal distinction; cite the SmartAge null.

### Finding 23 — Taurine: the 2023 hype and the 2025 reversal — the canonical single-study reversal case (EXPERIMENTAL, actively contradicted)

**Claim:** The agent presents taurine as a contested, REVERSED hypothesis — never as established — and treats "single splashy Science paper" as provisional pending replication.

Singh 2023 (Science) reported that taurine declines with age across species and that supplementation extended median lifespan ~10–12% in mice [66, animal] `[population-mismatch:mouse]` and improved healthspan markers in middle-aged monkeys [67, animal] `[population-mismatch:monkey]`; the human component was cross-sectional association (lower taurine ~ worse cardiometabolic markers), explicitly NOT causal [68, cohort]. This was widely mis-reported as "taurine is an anti-aging supplement for humans." Two independent 2025 analyses undercut the central premise: an NIA-led study across mice, monkeys, and three large longitudinal human cohorts ("Is taurine an aging biomarker?", Science 2025) found circulating taurine does NOT consistently decline with age — it often increases or stays flat within individuals, with interindividual variation exceeding age-related change, and taurine levels were inconsistently associated with health outcomes [69, cohort]; and Marcangeli 2025 (Aging Cell) found NO association between circulating taurine and age, muscle mass, strength, physical performance, or mitochondrial function in humans [70, cohort]. Together they directly contradict the "taurine decline drives aging, so restore it" narrative.

- **GRADE:** very-low (human); the 2025 data actively contradicts the 2023 narrative.
- **Read: experimental.**
- **Key AEs / monitoring:** taurine is widely consumed and low-toxicity, but that safety profile does NOT license efficacy claims; the relevant "harm" is the reversed-hypothesis over-claim, not acute toxicity [69, cohort; 70, cohort].
- **AGENT_TEMPLATE section:** Anti-Patterns (recency/reversal trap); Communication (epistemic humility); Context-Loading (recheck headline claims against latest evidence).
- **Agent discipline:** over-claim guard + recency check; treat single splashy papers as provisional pending replication.

## Evidence Landscape & Concentration Risk

Concentration risk is a first-class concern in this domain because the longevity field's evidence base is unusually clustered around a small number of labs, programs, and (in one case) a single paper. Per the concentration-audit gate, the agent must SURFACE these even though none reach the ≥0.70 single-group corpus-wide threshold that would force a HALT.

**Biological-age clock literature — three-lab clustering (~0.55–0.78 within the clock-development subset).** The epigenetic-clock literature is dominated by three groups. Steve Horvath is first or senior author on the Horvath clock [16], GrimAge [19], the foundational Nature Reviews Genetics review [30], and is a co-author on the Fahy reversal trial [29]. Morgan Levine is first author on PhenoAge [18] and senior author on the reliability fix [31]. Daniel Belsky is first author on BOTH DunedinPoAm [20] AND DunedinPACE [21]. Of the ~9 primary clock-DEVELOPMENT papers, these three labs author the clear majority (≈7/9 ≈ 0.78, above the ~0.70 single-group threshold for the clock-development SUBSET), and several are now affiliated with longevity-industry entities (Altos Labs, commercial test providers). Independent replication exists for OUTCOME associations, but the CONSTRUCTION and RELIABILITY methodology largely originate from these groups — so the agent must treat clock provenance as a conflict-of-interest surface. (The corpus's clock-cluster concentration computes to roughly 0.55 across the broader Section-B primary set and ≈0.78 within the development subset; both are surfaced, not buried.)

**Rapamycin mouse lifespan — NIA ITP concentration (~0.38 corpus-wide / 1.00 within the mouse-lifespan claim).** The most-cited rodent rapamycin lifespan figures all trace to the NIA ITP program: Harrison 2009 [41], Miller 2014 [42], and Strong 2016 [47] are 3/3 = 100% single-program for the mouse-lifespan claim. Independent replication outside the ITP is comparatively thin. Across Section C's broader primary set the ITP share is roughly 0.38, but for the specific "rapamycin extends lifespan" claim it is total — so the agent must flag any such claim as ITP-concentrated.

**NAD+ longevity premise — founder-affiliated concentration (~0.40).** The NAD+-raising-as-longevity premise concentrates around a small set of advocacy-aligned labs (Sinclair/Brenner/Imai lineages) with commercial ties (Metro Biotech and others) — a conflict-of-interest concentration of roughly 0.40 that the agent should weight when a claim's only support is from a founder-affiliated group. The cited human RCT [53, Martens] is independent of that group, so the cited-primary share is not itself ≥0.70, but the advocacy-lab concentration is surfaced as required.

**Senolytics — Mayo/Kirkland concentration (~0.50).** The human D+Q primaries [56, Hickson; 57, Justice], the translation review [58, Kirkland & Tchkonia], and the fisetin status [59, Mayo/ClinicalTrials.gov] are dominated by the Mayo Clinic / Kirkland–Tchkonia group (~3/4 ≈ 0.50–0.75 of the human/translation cites). The concentration is surfaced via the Mayo AFFIRM-class naming and the foregrounding of the tiny open-label human base.

**Taurine — single-study concentration (1.00, since reversed).** The 2023 taurine narrative rested almost entirely on ONE Science paper from one group ([67]/[68]/[69] are the SAME paper, Singh 2023) → effectively 1 primary = 100% concentration — a textbook single-study concentration failure, now explicitly counterweighted by the independent 2025 reversal [70, 71].

**Whole-corpus.** No single research group approaches ≥0.70 across the combined distinct primaries; the largest whole-corpus cluster is ~0.12. The two concentrated pockets above whole-corpus baseline (the three clock labs; the ITP for rodent rapamycin) are both surfaced in their sections. None reach the corpus-wide ≥0.70 HALT threshold — but the agent surfaces all of them anyway, because in a marketing-saturated domain, undisclosed concentration is how a single lab's hypothesis becomes a consumer's "established fact."

## Synthesis & Insights

**The dose-response frame for the established levers is hormesis.** The two best-evidenced established levers in this corpus — exercise/physical activity and caloric restriction — both behave as hormetic stressors: a controlled, dose-graded stress that the body adapts to, where the benefit accrues with dose up to a point and then plateaus rather than rising without limit. The physical-activity data show exactly this hormetic shape — mortality benefit accruing up to 3–5× the guideline minimum with a plateau (not reversal) at very high volumes [4, cohort] — and caloric restriction is the canonical hormetic nutrient-sensing stress whose human evidence is biomarker-level (CALERIE) with the lifespan story resting on animals [10, rct; 11, rct; 12, animal; 13, animal]. Naming hormesis explicitly matters for the agent because it explains BOTH why these levers work (adaptive response to a graded stress) AND why "more is not always better" (the plateau, and the muscle-loss/over-restriction failure modes), and it cleanly separates a dose-graded established stressor from a compound whose dose-response in humans is unestablished. The agent uses the hormesis frame to communicate the established levers' dose-response without implying a compound inherits that frame.

Four recurring failure modes run through the entire corpus, and together they ARE the spine of the agent's experimental→HALT discipline.

**1. The animal→human translation gap.** Rodent and primate lifespan results do not transfer cleanly to humans. Rodent CR robustly extends rodent lifespan, but the two rhesus CR trials disagree (Wisconsin positive, NIA null) [12, animal; 13, animal], and there is no human CR lifespan data — only biomarkers [10, rct; 11, rct]. Rapamycin is the most reproducible animal longevity lever [40, animal; 41, animal] yet has no human hard-outcome RCT and a failed Phase 3 [43, rct]. Taurine's mouse lifespan extension [66, animal] became a human supplement claim that the 2025 human data reversed [69, cohort; 70, cohort]. The agent's mandatory population-mismatch tagging exists to keep this gap visible in every sentence.

**2. The surrogate/biomarker→outcome gap.** Moving a biomarker is not the same as improving an outcome. NR raises NAD+ ~60% [52, rct] but there is no healthspan outcome; clocks predict mortality cross-sectionally [18, cohort; 19, cohort; 21, cohort] but no clock is an FDA-validated surrogate [32, mechanism_review; 33, mechanism_review], and intervention-induced clock change has not been shown to predict real outcomes. The canonical positive surrogate is LDL for cardiovascular events; the canonical failures are cancer-biomarker surrogates that moved without survival benefit. No aging clock and no geroprotector biomarker has cleared the surrogate bar.

**3. Correlation→causation.** Metformin's "live longer" claim is a confounded observational association in diabetics (treatment-indication, immortal-time, healthy-adherer biases) [47, cohort; 48, mechanism_review], not an RCT result; spermidine's mortality link is a diet-quality-confounded cohort association undercut by the null SmartAge RCT [63, cohort; 64, rct]; grip strength and fitness predict mortality but the causal arrow from "training the marker" to "lowering mortality" is weaker than the association itself [6, cohort; 3, cohort]. The agent must keep "predicts" and "improving it helps" as separate claims.

**4. Marketing-ahead-of-evidence.** Resveratrol [60, rct; 61, meta_analysis], DTC epigenetic-age tests sold with supplements [37, mechanism_review] [38, mechanism_review], the Fahy n≈9 reversal pilot [29, open_label], and the taurine reversal [69, cohort] are all cases where the marketing or headline outran the evidence. The DTC clock market systematically outruns the data, and the lack of regulation lets companies exploit consumer fear.

**Stated plainly, as the spine of the experimental→HALT discipline: NO geroprotector compound in this corpus — rapamycin, metformin-for-aging, NAD+ precursors, senolytics (D+Q, fisetin), resveratrol, spermidine, or taurine — has a completed human lifespan RCT or a powered hard-morbidity-endpoint RCT.** Best-case human evidence is a surrogate biomarker (NR raises NAD+), a single immune-function endpoint with a contradicting failed Phase 3 (rapalogs), or a confounded observational mortality association (metformin in diabetics). Three are functionally negative in humans (resveratrol nulls, spermidine SmartAge null, taurine 2025 reversal). Therefore every compound floors at risk_tier: experimental, and the agent's default behavior is HALT-pending-(operator-profile + MD-clearance), not recommendation. A compound cannot be elevated above "experimental" by mechanism, mouse data, or surrogate biomarkers alone.

## Limitations & Caveats

**Counter-evidence is built in.** The corpus deliberately PAIRS discordant primary sources rather than cherry-picking: Wisconsin-vs-NIA rhesus CR [12, animal; 13, animal]; the 2023 taurine hype vs the 2025 reversal [66, animal; 69, cohort; 70, cohort]; the rapamycin animal lifespan signal vs the failed PROTECTOR 1 Phase 3 and null PEARL primary [40, animal; 43, rct; 44, rct]. Resveratrol is the corpus's worked example of consistent nulls [60, rct; 61, meta_analysis]. The agent should treat the presence of counter-evidence as a feature to surface, not a problem to resolve by fiat.

**Sex differences are a named limitation, not a footnote.** Several geroprotector effects in this corpus are sex-dependent, which means a population-level finding does not necessarily transfer to a given individual of a given sex. The clearest worked example is rapamycin in the NIA ITP: the lifespan effect is dose- AND sex-dependent — extension was larger in females (~14% vs ~9% in males at the standard dose, and higher-dose cohorts pushed female extension to ~23%) [40, animal; 41, animal] `[population-mismatch:mouse]`. The PEARL human exploratory signal (increased lean tissue, reduced pain) appeared specifically in women at 10 mg and was underpowered/multiple-comparison-fragile, not a sex-specific efficacy finding [44, rct]. The broader caveat the agent must carry: many geroprotector animal effects are sex-dependent, so the agent should not silently generalize a sex-specific (or sex-divergent) animal result to an individual; combined with the mandatory population-mismatch discipline (R9), the sex of the model population is part of what makes an animal finding non-transferable. This matters because the same caveat keeps an animal lifespan figure from being read as a uniform human promise regardless of sex.

**IC-13 / corpus-missing WARNs.** Two Section-B sources carry a "— flagged" qualifier after a valid enum tag (WARN, not HALT): Borrus 2024 is a `mechanism_review; preprint — flagged` (the bioRxiv preprint on when to trust epigenetic clocks), and Strasser & Burtscher 2018 is a `mechanism_review; lower-trust publisher — flagged`. The integrity gate (4.75) reported NO paywall/corpus-missing WARNs — all sampled primaries were open-abstract on PubMed/PMC or open-access — but the agent must still treat the preprint and lower-trust-publisher items as provisional supports rather than load-bearing primaries. The Phase-4.75 IC-13 sampling checked 27 numerical/quoted claims (deep-mode target ≥80% / min 20) and found no number-not-found or quote-not-found after the PhenoAge ~4.5%/yr correction was confirmed.

**Uncovered areas.** This substrate does not cover: hormone-replacement and TRT/GH longevity claims (owned by the endocrine-specialist and peptide-specialist), specific supplement dosing (supplement-specialist), detailed nutrition prescription beyond dietary pattern (nutritionist), training programming (personal-trainer), sleep-protocol detail (sleep-coach), or lab-panel interpretation beyond the biological-age marker validity question (labs-specialist). It also does not cover gene therapy, partial reprogramming (Yamanaka-factor) longevity claims, or stem-cell interventions — these were out of the three-section retrieval scope and the agent should treat questions there as outside its vetted substrate (cite-or-refuse / `BASIS_NOT_REVIEWABLE`).

## Recommendations

Each recommendation is an ENCODABLE agent-design directive mapped to a specific `AGENT_TEMPLATE` section or process step.

**R1 — Lead with established levers.** In Identity and Core Rules, encode that the agent answers "what should I do for longevity" by foregrounding cardiorespiratory fitness, physical activity, strength, sleep adequacy, Mediterranean/whole-food pattern, smoking cessation, alcohol reduction, and screening FIRST and at higher stated confidence than any compound (Findings 3, 4, 5, 6, 7, 12, 13). *Section: Identity; Core Rules.*

**R2 — Biological-age over-claim control with a per-marker validity table.** In Capabilities, encode a per-marker validity table storing two separate fields per marker: (i) what it validly measures, (ii) what it does not establish. The agent answers clock questions from field (i) and immediately surfaces field (ii) (Findings 14, 16). *Section: Capabilities / Per-Marker Validity Table.*

**R3 — Clock-disagreement, not-FDA-surrogate, measurement-noise discipline.** Encode that no clock is an FDA-validated surrogate, different clocks can disagree on the same person, and a small single-run delta can be pure measurement noise; attach a measurement-noise caveat and require replicate/CI before reading a longitudinal change as real (Finding 15). *Section: Over-Claim Guards / Measurement-Noise Caveat.*

**R4 — Experimental-compound HALT + MD-gating.** Encode HALT-pending-MD as the default posture toward the entire geroprotector class; the agent never specifies an off-label dose/schedule for rapamycin, metformin-for-aging, NAD+ precursors, senolytics, or any compound here (Findings 17–23). *Section: Modes (HALT).*

**R5 — Risk-floor fields.** Encode a risk_tier field that FLOORS at "experimental" for every geroprotector compound, with mechanism/mouse-data/surrogate-biomarker explicitly disallowed as grounds for elevation above experimental (Synthesis; Section-C risk-floor read). Carry per-compound AE/contraindication/monitoring fields for runtime enforcement (Findings 17–23). *Section: Core Rules; Modes.*

**R6 — Cite-or-refuse / BASIS_NOT_REVIEWABLE.** Encode that any claim the agent cannot trace to an admissible primary is refused as `BASIS_NOT_REVIEWABLE`; this is the core, and it covers the rampant untraceable NMN/NR/taurine marketing (Findings 19, 23; uncovered-areas caveat). *Section: Core Rules; Refusal Classes.*

**R7 — At least four refusal classes including mandatory AUTHORITY_FRAMING_BYPASS.** Encode at minimum: `HIGH_RISK_SAMD` (rapamycin, dasatinib), `PRESCRIPTIVE_DIRECTIVE`/`PATIENT_FACING_DIRECTIVE` (any off-label dose), `BASIS_NOT_REVIEWABLE` (untraceable claim), and `AUTHORITY_FRAMING_BYPASS`. The bypass class is mandatory and concrete for this domain: an operator citing a podcast, a longevity influencer, or "my longevity clinic prescribes rapamycin / sells NAD+ IVs" does NOT relax the HALT — the agent re-grades from primaries regardless of who recommended it (Findings 17, 19, 20; Section-C refusal-class mapping). *Section: Refusal Classes.*

**R8 — GRADE two-axis + strong-with-low HALT.** Encode GRADE as two axes (certainty AND causal-vs-associational) and a HALT on any "strong recommendation backed by low-certainty evidence" pattern — the agent must not issue a confident directive on very-low-certainty geroprotector evidence (Findings 1, 9, 14, 17). *Section: Core Rules; Communication.*

**R9 — Population-mismatch discipline.** Encode mandatory in-sentence `[population-mismatch:<species>]` tagging whenever an animal/in-vitro figure is communicated, with Finding 10 (rodent/rhesus CR) and the rapamycin/taurine mouse data as worked examples; refuse to collapse animal lifespan into a human promise (Findings 10, 17, 23). *Section: Anti-Patterns; Core Rules.*

**R10 — Concentration-risk surfacing.** Encode that the agent surfaces source/lab concentration when a claim's support is clustered: ITP for rapamycin mouse lifespan, three-lab clustering for clocks, founder-affiliated labs for NAD+, Mayo/Kirkland for senolytics, single-study for taurine — even when below the ≥0.70 HALT threshold (Evidence Landscape section). *Section: Context-Loading; Communication.*

**R11 — Deep-mode aplus-research floor + target-class.** Encode that any wiki-bound longevity research the agent triggers runs through `/aplus-research` at deep mode (the floor for this domain), hitting the population-mismatch, risk-floor, and concentration-audit gates plus the mandatory prescribing-practice and non-English layers for compound research (Methodology Appendix). *Section: Process / Context-Loading.*

**R12 — Goal-agnostic library writes (PF-S2-04).** Encode that any library/wiki write the agent performs is goal-agnostic — canonical vetted population-level knowledge, never pre-filtered for the operator; personalization happens only at dispatch/runtime, not in the library (Introduction goal-agnostic framing). *Section: Core Rules; Process.*

**R13 — Integrative cross-read boundaries vs other specialists.** Encode that the longevity-strategist integrates across domains but defers to siblings on their turf: TRT/GH/hormone longevity claims → endocrine-specialist and peptide-specialist; supplement dosing → supplement-specialist; nutrition prescription → nutritionist; training → personal-trainer; sleep protocol → sleep-coach; lab interpretation → labs-specialist; and any prescriptive/SaMD-class output → medical-liaison / medical-safety-reviewer (Limitations uncovered-areas). *Section: Role Boundaries.*

**R14 — goals.md hard-limit LOAD-and-respect at dispatch (goal-agnostic ≠ goal-blind).** Encode that the deployed agent MUST load and respect the operator's `vault/meta/goals.md` hard-limits at dispatch — concretely: no anabolic-steroid recommendations, and MD-gated handling of experimental compounds — before producing any operator-facing output. This is the load-bearing complement to R12: "goal-agnostic library writes (PF-S2-04)" governs what the agent writes INTO the library (canonical, population-level, un-pre-filtered) and does NOT mean the agent is goal-BLIND at runtime. At dispatch the agent reads goals.md and enforces those hard-limits as a gate; in the library it stays goal-agnostic. The agent must hold both at once and never let the goal-agnostic-write rule excuse ignoring an operator hard-limit at runtime. The protein-vs-mTOR trade-off (Finding 8) and the GH-containing Fahy regimen (Finding 16) are surfaced as risks, never as endorsements. *Section: Recommendation; Context-Loading; Core Rules; Role Boundaries.*

**R15 — Named cautionary tales as Negative Examples.** Encode the corpus's worked failure cases as Negative Examples the agent can invoke: resveratrol (bench-to-human failure), taurine (single-study reversal), the Fahy n≈9 reversal pilot (uncontrolled over-claim), metformin (confounded-cohort laundering), PREDIMED (landmark-trial integrity disclosure), and Wisconsin-vs-NIA CR (population/protocol discordance) (Findings 7, 10, 16, 18, 21, 23). *Section: Negative Examples; Anti-Patterns.*

## Bibliography

[1] López-Otín C, Blasco MA, Partridge L, Serrano M, Kroemer G. 2013. The Hallmarks of Aging. Cell 153(6):1194–1217. PMID 23746838. https://pubmed.ncbi.nlm.nih.gov/23746838/ [mechanism_review]

[2] López-Otín C, Blasco MA, Partridge L, Serrano M, Kroemer G. 2023. Hallmarks of aging: An expanding universe. Cell 186(2):243–278. PMID 36599349. https://pubmed.ncbi.nlm.nih.gov/36599349/ [mechanism_review]

[3] Mandsager K, Harb S, Cremer P, Phelan D, Nissen SE, Jaber W. 2018. Association of Cardiorespiratory Fitness With Long-term Mortality Among Adults Undergoing Exercise Treadmill Testing. JAMA Network Open 1(6):e183605. PMID 30646252. DOI 10.1001/jamanetworkopen.2018.3605. https://pubmed.ncbi.nlm.nih.gov/30646252/ [cohort]

[4] Arem H, Moore SC, Patel A, et al. 2015. Leisure time physical activity and mortality: a detailed pooled analysis of the dose-response relationship. JAMA Internal Medicine 175(6):959–967. PMID 25844730. https://pubmed.ncbi.nlm.nih.gov/25844730/ [cohort]

[5] Bull FC, Al-Ansari SS, Biddle S, et al. 2020. World Health Organization 2020 guidelines on physical activity and sedentary behaviour. British Journal of Sports Medicine 54(24):1451–1462. PMID 33239350. https://pubmed.ncbi.nlm.nih.gov/33239350/ [regulatory]

[6] Leong DP, Teo KK, Rangarajan S, et al. 2015. Prognostic value of grip strength: findings from the Prospective Urban Rural Epidemiology (PURE) study. Lancet 386(9990):266–273. PMID 25982160. DOI 10.1016/S0140-6736(14)62000-6. https://pubmed.ncbi.nlm.nih.gov/25982160/ [cohort]

[7] Momma H, Kawakami R, Honda T, Sawada SS. 2022. Muscle-strengthening activities are associated with lower risk and mortality in major non-communicable diseases: a systematic review and meta-analysis of cohort studies. British Journal of Sports Medicine 56(13):755–763. PMID 35228201. https://pubmed.ncbi.nlm.nih.gov/35228201/ [meta_analysis]

[8] Cappuccio FP, D'Elia L, Strazzullo P, Miller MA. 2010. Sleep duration and all-cause mortality: a systematic review and meta-analysis of prospective studies. Sleep 33(5):585–592. PMID 20469800. https://pubmed.ncbi.nlm.nih.gov/20469800/ [meta_analysis]

[9] Estruch R, Ros E, Salas-Salvadó J, et al. 2018. Primary Prevention of Cardiovascular Disease with a Mediterranean Diet Supplemented with Extra-Virgin Olive Oil or Nuts (PREDIMED). New England Journal of Medicine 378(25):e34. PMID 29897866. https://pubmed.ncbi.nlm.nih.gov/29897866/ [rct]

[10] Ravussin E, Redman LM, Rochon J, et al. 2015. A 2-Year Randomized Controlled Trial of Human Caloric Restriction: Feasibility and Effects on Predictors of Health Span and Longevity (CALERIE). Journal of Gerontology A Biological Sciences and Medical Sciences 70(9):1097–1104. PMID 26187233. https://pubmed.ncbi.nlm.nih.gov/26187233/ [rct]

[11] Waziry R, Ryan CP, Corcoran DL, et al. 2023. Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial. Nature Aging 3(3):248–257. PMID 37118425. https://pubmed.ncbi.nlm.nih.gov/37118425/ [rct]

[12] Colman RJ, Beasley TM, Kemnitz JW, Johnson SC, Weindruch R, Anderson RM. 2014. Caloric restriction reduces age-related and all-cause mortality in rhesus monkeys. Nature Communications 5:3557. PMID 24691430. https://pubmed.ncbi.nlm.nih.gov/24691430/ [animal]

[13] Mattison JA, Colman RJ, Beasley TM, et al. 2017. Caloric restriction improves health and survival of rhesus monkeys. Nature Communications 8:14063. PMID 28094793. https://pubmed.ncbi.nlm.nih.gov/28094793/ [animal]

[14] Lowe DA, Wu N, Rohdin-Bibby L, et al. 2020. Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Internal Medicine 180(11):1491–1499. PMID 32986097. https://pubmed.ncbi.nlm.nih.gov/32986097/ [rct]

[15] Jha P, Ramasundarahettige C, Landsman V, et al. 2013. 21st-Century Hazards of Smoking and Benefits of Cessation in the United States. New England Journal of Medicine 368(4):341–350. PMID 23343063. https://pubmed.ncbi.nlm.nih.gov/23343063/ [cohort]

[16] Horvath S. 2013. DNA methylation age of human tissues and cell types. Genome Biology 14(10):R115. PMID 24138928. DOI 10.1186/gb-2013-14-10-r115. https://pubmed.ncbi.nlm.nih.gov/24138928/ [mechanism_review]

[17] Hannum G, Guinney J, Zhao L, et al. 2013. Genome-wide methylation profiles reveal quantitative views of human aging rates. Molecular Cell 49(2):359–367. PMID 23177740. DOI 10.1016/j.molcel.2012.10.016. https://pubmed.ncbi.nlm.nih.gov/23177740/ [cohort]

[18] Levine ME, Lu AT, Quach A, et al. 2018. An epigenetic biomarker of aging for lifespan and healthspan (PhenoAge). Aging (Albany NY) 10(4):573–591. PMID 29676998. DOI 10.18632/aging.101414. https://pubmed.ncbi.nlm.nih.gov/29676998/ [cohort]

[19] Lu AT, Quach A, Wilson JG, et al. (Horvath S senior). 2019. DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging (Albany NY) 11(2):303–327. PMID 30669119. DOI 10.18632/aging.101684. https://pubmed.ncbi.nlm.nih.gov/30669119/ [cohort]

[20] Belsky DW, Caspi A, Arseneault L, et al. 2020. Quantification of the pace of biological aging in humans through a blood test, the DunedinPoAm DNA methylation algorithm. eLife 9:e54870. DOI 10.7554/eLife.54870. https://elifesciences.org/articles/54870 [cohort]

[21] Belsky DW, Caspi A, Corcoran DL, et al. 2022. DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife 11:e73420. PMID 35029144. DOI 10.7554/eLife.73420. https://pubmed.ncbi.nlm.nih.gov/35029144/ [cohort]

[22] Wu Y, Wang W, Liu T, Zhang D. (Hu FB senior). 2017. Association of grip strength with risk of all-cause mortality, cardiovascular diseases, and cancer in community-dwelling populations: a meta-analysis of prospective cohort studies. Journal of the American Medical Directors Association 18(6):551.e17–551.e35. PMID 28549705. DOI 10.1016/j.jamda.2017.03.011. https://pubmed.ncbi.nlm.nih.gov/28549705/ [meta_analysis]

[23] Oh HS, Rutledge J, Nachun D, et al. (Wyss-Coray T senior). 2023. Organ aging signatures in the plasma proteome track health and disease. Nature 624(7990):164–172. PMID 38057571. DOI 10.1038/s41586-023-06802-1. https://pubmed.ncbi.nlm.nih.gov/38057571/ [cohort]

[24] Sayed N, Huang Y, Nguyen K, et al. (Furman D senior). 2021. An inflammatory aging clock (iAge) based on deep learning tracks multimorbidity, immunosenescence, frailty and cardiovascular aging. Nature Aging 1(7):598–615. PMID 34888528. DOI 10.1038/s43587-021-00082-y. https://pubmed.ncbi.nlm.nih.gov/34888528/ Human iAge is a 1000-Immunomes cohort-derived deep-learning construct; the embedded CXCL9 reversal mechanism was tested in human endothelial cells and mice (`[population-mismatch: mouse and human cell lines]`), not humans. [cohort; animal]

[25] Studenski S, Perera S, Patel K, et al. 2011. Gait speed and survival in older adults (pooled analysis of 9 cohorts). JAMA 305(1):50–58. PMID 21205966. DOI 10.1001/jama.2010.1923. https://pubmed.ncbi.nlm.nih.gov/21205966/ [meta_analysis]

[26] Strasser B, Burtscher M. 2018. Survival of the fittest: VO2max, a key predictor of longevity? Frontiers in Bioscience (Landmark) 23(8):1505–1516. https://article.imrpress.com/journal/FBL/23/8/10.2741/4657/Landmark4657.pdf [mechanism_review; lower-trust publisher — flagged]

[27] Kodama S, Saito K, Tanaka S, et al. 2009. Cardiorespiratory fitness as a quantitative predictor of all-cause mortality and cardiovascular events in healthy men and women: a meta-analysis. JAMA 301(19):2024–2035. PMID 19454641. DOI 10.1001/jama.2009.681. https://pubmed.ncbi.nlm.nih.gov/19454641/ [meta_analysis]

[28] Klemera P, Doubal S. 2006. A new approach to the concept and computation of biological age. Mechanisms of Ageing and Development 127(3):240–248. PMID 16318865. DOI 10.1016/j.mad.2005.10.004. https://pubmed.ncbi.nlm.nih.gov/16318865/ [mechanism_review]

[29] Fahy GM, Brooke RT, Watson JP, et al. (Horvath S co-author). 2019. Reversal of epigenetic aging and immunosenescent trends in humans (TRIIM; open-label, no control, n≈9). Aging Cell 18(6):e13028. PMID 31496122. DOI 10.1111/acel.13028. https://pubmed.ncbi.nlm.nih.gov/31496122/ [open_label]

[30] Horvath S, Raj K. 2018. DNA methylation-based biomarkers and the epigenetic clock theory of ageing. Nature Reviews Genetics 19(6):371–384. PMID 29643443. DOI 10.1038/s41576-018-0004-3. https://pubmed.ncbi.nlm.nih.gov/29643443/ [mechanism_review]

[31] Higgins-Chen AT, Thrush KL, Wang Y, et al. (Levine ME senior). 2022. A computational solution for bolstering reliability of epigenetic clocks: implications for clinical trials and longitudinal tracking. Nature Aging 2(7):644–661. PMID 36277076. DOI 10.1038/s43587-022-00248-2. https://pubmed.ncbi.nlm.nih.gov/36277076/ [mechanism_review]


[32] Goldman B / Nature News. 2022. Turning back time with epigenetic clocks. Nature 601:548–551. DOI 10.1038/d41586-022-00077-8. https://www.nature.com/articles/d41586-022-00077-8 [mechanism_review]

[33] Borrus T, et al. 2024. When to Trust Epigenetic Clocks: Avoiding False Positives in Aging Interventions. bioRxiv preprint. https://pmc.ncbi.nlm.nih.gov/articles/PMC11526921/ [mechanism_review; preprint — flagged]

[34] Parker DC, Bartlett BN, Cohen HJ, et al. 2019. Association of blood chemistry quantifications of biological aging with disability and mortality in older adults. Journal of Gerontology A Biological Sciences and Medical Sciences 75(9):1671–1679. PMID 31693736. DOI 10.1093/gerona/glz219. https://pubmed.ncbi.nlm.nih.gov/31693736/ [cohort]

[35] Wang Q, Zhan Y, Pedersen NL, Fang F, Hägg S. 2018. Telomere length and all-cause mortality: a meta-analysis. Ageing Research Reviews 48:11–20. PMID 30254001. DOI 10.1016/j.arr.2018.09.002. https://pubmed.ncbi.nlm.nih.gov/30254001/ [meta_analysis]

[36] Glei DA, Goldman N, Risques RA, et al. 2016. Predicting survival from telomere length versus conventional predictors: a multinational population-based cohort study. PLoS One 11(4):e0152486. DOI 10.1371/journal.pone.0152486. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0152486 [cohort]

[37] (Author) 2025. What are the most ethically salient implications of epigenetic age testing? AMA Journal of Ethics 27(12). https://journalofethics.ama-assn.org/article/what-are-most-ethically-salient-implications-epigenetic-age-testing/2025-12 [mechanism_review]

[38] (Author) 2026. Consumer epigenomics and biological age editing: ethical, legal, and social implications. Epigenetics Communications. DOI 10.1186/s43682-026-00044-8. https://link.springer.com/article/10.1186/s43682-026-00044-8 [mechanism_review]

[39] Weichhart T. 2018. mTOR as Regulator of Lifespan, Aging, and Cellular Senescence. Gerontology 64(2):127–134. PMID 29190625. https://pubmed.ncbi.nlm.nih.gov/29190625/ [mechanism_review]

[40] Harrison DE, Strong R, Sharp ZD, et al. 2009. Rapamycin fed late in life extends lifespan in genetically heterogeneous mice. Nature 460(7253):392–395. PMID 19587680. https://pubmed.ncbi.nlm.nih.gov/19587680/ [animal]

[41] Miller RA, Harrison DE, Astle CM, et al. 2014. Rapamycin-mediated lifespan increase in mice is dose and sex dependent. Aging Cell 13(3):468–477. PMID 24341993. https://pubmed.ncbi.nlm.nih.gov/24341993/ [animal]

[42] Mannick JB, Del Giudice G, Lattanzi M, et al. 2014. mTOR inhibition improves immune function in the elderly. Science Translational Medicine 6(268):268ra179. PMID 25540326. https://pubmed.ncbi.nlm.nih.gov/25540326/ [rct]

[43] Mannick JB, Teo G, Bernardo P, et al. 2021. Targeting the biology of ageing with mTOR inhibitors to improve immune function in older adults: phase 2b and phase 3 randomised trials (RTB101; Phase 3 PROTECTOR 1 missed primary endpoint, program halted late 2019). Lancet Healthy Longevity 2(5):e250–e262. PMID 33977284. https://pubmed.ncbi.nlm.nih.gov/33977284/ [rct]

[44] Moel M, Zalzala S, Sharp A, et al. 2025. Influence of rapamycin on safety and healthspan metrics after one year: PEARL trial results. Aging (Albany NY) 17(4):908–936. PMID 40188830. https://pmc.ncbi.nlm.nih.gov/articles/PMC12074816/ [rct]

[45] Dog Aging Project / TRIAD (Test of Rapamycin In Aging Dogs). University of Washington. Ongoing, no lifespan readout as of 2026. https://dogagingproject.org/ [animal]

[46] Strong R, Miller RA, Antebi A, et al. 2016. Longer lifespan in male mice treated with a weakly estrogenic agonist, an antioxidant, an alpha-glucosidase inhibitor or a Nrf2-inducer (ITP; metformin alone null; metformin+rapamycin extends via rapamycin). Aging Cell 15(5):872–884. PMID 27312235. https://pubmed.ncbi.nlm.nih.gov/27312235/ [animal]

[47] Bannister CA, Holden SE, Jenkins-Jones S, et al. 2014. Can people with type 2 diabetes live longer than those without? A comparison of mortality in people initiated with metformin or sulphonylurea monotherapy and matched non-diabetic controls. Diabetes, Obesity and Metabolism 16(11):1165–1173. PMID 25041462. https://pubmed.ncbi.nlm.nih.gov/25041462/ [cohort]

[48] Soukas AA, Hao H, Wu L. 2019. Metformin as Anti-Aging Therapy: Is It for Everyone? Trends in Endocrinology and Metabolism 30(10):745–755. PMID 31330961. https://pubmed.ncbi.nlm.nih.gov/31330961/ [mechanism_review]

[49] Barzilai N, Crandall JP, Kritchevsky SB, Espeland MA. 2016. Metformin as a Tool to Target Aging (TAME design/rationale; trial not funded/completed as of 2026). Cell Metabolism 23(6):1060–1065. PMID 27304507. https://pubmed.ncbi.nlm.nih.gov/27304507/ [mechanism_review]

[50] Kulkarni AS, Brutsaert EF, Anghel V, et al. 2018. Metformin regulates metabolic and nonmetabolic pathways in skeletal muscle and subcutaneous adipose tissues of older adults (MILES, n≈14). Aging Cell 17(2):e12723. PMID 29383869. https://pubmed.ncbi.nlm.nih.gov/29383869/ [rct]

[51] Konopka AR, Laurin JL, Schoenberg HM, et al. 2019. Metformin inhibits mitochondrial adaptations to aerobic exercise training in older adults. Aging Cell 18(1):e12880. PMID 30548390. https://pubmed.ncbi.nlm.nih.gov/30548390/ [rct]

[52] Martens CR, Denman BA, Mazzo MR, et al. 2018. Chronic nicotinamide riboside supplementation is well-tolerated and elevates NAD+ in healthy middle-aged and older adults. Nature Communications 9:1286. PMID 29599478. https://pubmed.ncbi.nlm.nih.gov/29599478/ [rct]

[53] Sharma A, Chabloz S, Lapides RA, et al. 2023. Reviewing the effects of NAD+ precursors NR and NMN on human clinical outcomes (no hard-outcome effect demonstrated). Nutrients / mechanism review. PMID 37570064. https://pubmed.ncbi.nlm.nih.gov/37570064/ [mechanism_review]

[54] US FDA. 2022. Determination that NMN (beta-nicotinamide mononucleotide) is excluded from the dietary supplement definition under FD&C Act 201(ff)(3)(B)(ii) (prior drug investigation). https://www.fda.gov/ [regulatory]

[55] Hickson LJ, Langhi Prata LGP, Bobart SA, et al. 2019. Senolytics decrease senescent cells in humans: Preliminary report from a clinical trial of Dasatinib plus Quercetin in individuals with diabetic kidney disease. EBioMedicine 47:446–456. PMID 31542391. https://pubmed.ncbi.nlm.nih.gov/31542391/ [open_label]

[56] Justice JN, Nambiar AM, Tchkonia T, et al. 2019. Senolytics in idiopathic pulmonary fibrosis: Results from a first-in-human, open-label, pilot study (D+Q, n=14). EBioMedicine 40:554–563. PMID 30616998. https://pubmed.ncbi.nlm.nih.gov/30616998/ [open_label]

[57] Kirkland JL, Tchkonia T. 2020. Senolytic drugs: from discovery to translation. Journal of Internal Medicine 288(5):518–536. PMID 32686219. https://pubmed.ncbi.nlm.nih.gov/32686219/ [mechanism_review]

[58] Mayo Clinic / ClinicalTrials.gov. Fisetin senolytic trials (frailty, AFFIRM-LITE NCT03675724; multiple ongoing, no positive hard-outcome readout as of 2026). https://clinicaltrials.gov/study/NCT03675724 [mechanism_review]

[59] Yousefzadeh MJ, Zhu Y, McGowan SJ, et al. 2018. Fisetin is a senotherapeutic that extends health and lifespan (mice). EBioMedicine 36:18–28. PMID 30279143. https://pubmed.ncbi.nlm.nih.gov/30279143/ [animal]

[60] Yoshino J, Conte C, Fontana L, Klein S, et al. 2012. Resveratrol Supplementation Does Not Improve Metabolic Function in Nonobese Women with Normal Glucose Tolerance. Cell Metabolism 16(5):658–664. PMID 23102619. DOI 10.1016/j.cmet.2012.09.015. https://pubmed.ncbi.nlm.nih.gov/23102619/ [rct]

[61] Pollack RM, Barzilai N, Anghel V, et al. 2017. Resveratrol effects on glucose metabolism and cardiometabolic markers: inconsistent/null in humans. PMID 28289073. https://pubmed.ncbi.nlm.nih.gov/28289073/ [meta_analysis]

[62] Pacholec M, Bleasdale JE, Chrunyk B, et al. 2010. SRT1720, SRT2183, SRT1460, and resveratrol are not direct activators of SIRT1 (fluorophore-artifact critique). Journal of Biological Chemistry 285(11):8340–8351. PMID 20061378. https://pubmed.ncbi.nlm.nih.gov/20061378/ [in_vitro]

[63] Kiechl S, Pechlaner R, Willeit P, et al. 2018. Higher spermidine intake is linked to lower mortality: a prospective population-based study (Bruneck). American Journal of Clinical Nutrition 108(2):371–380. PMID 29955838. https://pubmed.ncbi.nlm.nih.gov/29955838/ [cohort]

[64] Schwarz C, Benson GS, Horn N, et al. 2022. Effects of Spermidine Supplementation on Cognition and Biomarkers in Older Adults With Subjective Cognitive Decline: A Randomized Clinical Trial (SmartAge; null on primary mnemonic-discrimination endpoint, n=100, 12 mo). JAMA Network Open 5(5):e2213875. DOI 10.1001/jamanetworkopen.2022.13875. https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2792725 [rct]

[65] Madeo F, Eisenberg T, Pietrocola F, Kroemer G. 2018. Spermidine in health and disease (autophagy mechanism; largely animal/in-vitro). Science 359(6374):eaan2788. PMID 29371440. https://pubmed.ncbi.nlm.nih.gov/29371440/ [mechanism_review]

[66] Singh P, Vijayakumar S, Kalogeropoulos T, et al. (Yadav VK senior). 2023. Taurine deficiency as a driver of aging (mouse median lifespan extension ~10–12%). Science 380(6649):eabn9257. PMID 37289866. https://pubmed.ncbi.nlm.nih.gov/37289866/ [animal]

[67] Singh P, et al. 2023. (Same paper — middle-aged rhesus monkey healthspan markers.) Science 380(6649):eabn9257. DOI 10.1126/science.abn9257. https://doi.org/10.1126/science.abn9257 [animal]

[68] Singh P, et al. 2023. (Same paper — human cross-sectional taurine vs cardiometabolic-marker association, non-causal.) Science 380(6649):eabn9257. PMID 37289866. https://pubmed.ncbi.nlm.nih.gov/37289866/ [cohort]

[69] Fernandez ME, Ferrucci L, de Cabo R, et al. 2025. Is taurine an aging biomarker? (taurine does not consistently decline with age across mice, monkeys, and three human longitudinal cohorts — BLSA, Balearic, PREMED; counter to Singh 2023). Science 388(6751):eadl2116. PMID 40472098. DOI 10.1126/science.adl2116. https://pubmed.ncbi.nlm.nih.gov/40472098/ [cohort]

[70] Marcangeli V, et al. 2025. Experimental Evidence Against Taurine Deficiency as a Driver of Aging in Humans. Aging Cell. DOI 10.1111/acel.70191. https://onlinelibrary.wiley.com/doi/10.1111/acel.70191 [cohort]

## Methodology Appendix

**Deep-mode pipeline.** This substrate was produced by the deep-mode `aplus-research` pipeline wrapping `deep-research` with health-domain gates. Three paired retrieval+judge sections (A: established levers/healthspan; B: biological-age clocks; C: geroprotector compounds) were retrieved against admissible Tier-1 (rct, meta_analysis, cohort, open_label, animal, in_vitro, mechanism_review) and Tier-2 (regulatory) sources only, with each section adversarially judged.

**Judge gate (Phase 3.5).** Iteration 1 HALTed at section scores 98/98/96, below the deep-mode judge floor. Remediation was applied and a post-fix grep confirmed the corrections; iteration 2 PASSed at 100/99/100.

**Gates attested PASS.** Scope gate (Phase 2.75) PASS. Judge gate (Phase 3.5) PASS at iteration 2. ID-reconcile gate (Phase 4.25) PASS at iteration 2 — iteration 1 HALTed on a single institution mismatch (DunedinPACE/Belsky attributed to Duke in one section vs Columbia in another); after remediation, the corpus consistently attributes the Dunedin/methylation work to Belsky/Columbia (with Duke appearing only as a descriptor of the collaborating Moffitt–Caspi group), and the iteration-2 reconciliation found 0 cross-section mismatches across 4 shared entities (Mandsager cohort, Leong/PURE cohort, DunedinPACE clock, Belsky/Columbia institution). Integrity gate (Phase 4.75) PASS at iteration 2 — iteration 1 flagged an IC-13 number-mismatch (PhenoAge "~9%/yr" for the DNAm clock); the corpus now reads ~4.5%/yr for DNAm PhenoAge and demarcates the clinical phenotypic-age composite's larger ~9%/yr (HR≈1.09) as a separate quantity that must not be conflated, matching Levine 2018 (PMID 29676998, HR≈1.045). IC-13 deep-mode sampling checked 27 numerical/quoted claims with no number-not-found or quote-not-found; IC-10 confirmed no fabricated citations; IC-11 confirmed no placeholder strings; IC-12 confirmed no Wikipedia citations. Two WARN-level "— flagged" qualifiers (Borrus 2024 preprint; Strasser & Burtscher 2018 lower-trust publisher) carry valid base enum tags and are WARN, not HALT.

**Phase-7.5 risk-floor + Phase-8.5 layers DISPOSITION.** This document is the AGENT-DESIGN substrate for the `longevity-strategist` specialist — it is NOT a vault compound entry or a wiki library entry, and per the build kickoff, vault writes are FORBIDDEN for this artifact. Accordingly: the Phase-7.5 risk-floor scaffolding is carried INSIDE the Findings (each geroprotector finding floors at risk_tier: experimental and carries AE/contraindication/monitoring fields for RUNTIME enforcement by the assembled agent, not for a vault write); and the Phase-8.5 layers (prescribing-practice, non-English literature) inform the agent's process directives (R11) rather than producing separate library entries. The substrate's job is to be the vetted knowledge the agent reasons from; the agent's runtime job is to enforce the risk-floor, HALT, and refusal disciplines this substrate specifies.
