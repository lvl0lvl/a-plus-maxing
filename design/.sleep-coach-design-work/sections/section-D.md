# Section D — Sleep Interventions: Evidence Base (Behavioral, Circadian, and Sleep-Relevant Compounds)

Scope: This section grounds the design of a `sleep-coach` medical-specialist agent whose owned
domain is **behavioral and circadian sleep optimization** (risk_tier low). The agent CONSUMES
sleep-relevant compounds but does NOT own the compound class. Every claim below is type-tagged
with exactly one tag: `rct | meta_analysis | cohort | open_label | animal | in_vitro |
mechanism_review | regulatory`. Numbered citations resolve in the Bibliography.

The dominant finding of this section, which the agent's design must inherit: **the evidence
gradient is steep**. CBT-I rests on a guideline strong recommendation backed by dozens of RCTs;
the behavioral/environmental layer is mixed; the OTC/supplement layer is mostly weak-to-very-low
certainty with documented label-integrity failures. The agent must privilege the top of this
gradient and must not over-sell the bottom.

---

## D.1 — Cognitive Behavioral Therapy for Insomnia (CBT-I): the first-line intervention

CBT-I is the guideline-recommended **first-line treatment for chronic insomnia disorder** in
adults. The American Academy of Sleep Medicine (AASM) 2021 clinical practice guideline issues a
**STRONG recommendation** for multicomponent CBT-I — the only strong recommendation in that
guideline, meaning clinicians should follow it under most circumstances [1, regulatory]. The
American College of Physicians (ACP) likewise recommends that all adult patients receive CBT-I
as the initial treatment for chronic insomnia, with pharmacotherapy reserved for cases where
CBT-I alone is unsuccessful [3, regulatory].

**Components.** CBT-I is multicomponent: stimulus control (re-associating the bed with sleep),
sleep restriction therapy (curtailing time-in-bed to consolidate sleep and build homeostatic
pressure), cognitive restructuring (targeting catastrophic beliefs about sleep), relaxation
training, and sleep-hygiene education as an **adjunct, not a sufficient standalone** (see D.2)
[2, meta_analysis; 1, regulatory].

**Effect sizes.** The Trauer 2015 meta-analysis (20 RCTs, multimodal face-to-face CBT-I vs.
inactive comparators in chronic insomnia) found post-treatment improvements of: sleep onset
latency −19.03 min (95% CI −23.93 to −14.12), wake after sleep onset (WASO) −26.00 min (95% CI
−36.52 to −15.48), sleep efficiency +9.91% (95% CI +8.09 to +11.73), and total sleep time +7.61
min (95% CI −0.51 to +15.74, the only non-significant primary outcome) [2, meta_analysis]. The
AASM systematic review/meta-analysis underpinning the 2021 guideline reported a remission rate
33% higher (95% CI 28–39%) and a responder rate 45% greater (95% CI 39–50%) than controls, with
PSQI sleep quality improved by an effect size of 0.66 [1, meta_analysis]. A component network
meta-analysis across delivery formats reported large standardized mean differences for insomnia
severity (individual onsite CBT-I SMD ≈ −1.30; group ≈ −1.01; digital/internet-delivered ≈ −1.01
to −1.04) [4, meta_analysis].

**Design consequence:** the agent should privilege CBT-I and CBT-I components above all
pharmacologic or supplement options for chronic insomnia. Digital/self-guided CBT-I retains
large effects, which matters for an AI agent that can deliver the behavioral protocol directly.

---

## D.2 — Sleep hygiene and environmental factors: grade the evidence honestly

Sleep-hygiene advice is widely repeated but the single-component evidence is **weak**. The AASM
2021 guideline issues a recommendation **AGAINST** sleep hygiene as a single-component therapy
for chronic insomnia (clinicians are advised not to use it standalone) [1, regulatory]. A 2025
systematic review/meta-analysis found sleep-hygiene education inferior to CBT-I, partial CBT-I,
exercise, and acupressure for insomnia severity, with 85.7% of included trials at high risk of
bias [7, meta_analysis]. Sleep hygiene is best framed as a low-cost adjunct inside a
multicomponent plan, not a treatment.

Component-specific evidence:

- **Caffeine.** Pharmacokinetic half-life is roughly 5 h but ranges ~2–10 h depending on CYP1A2
  genotype and other factors [8, mechanism_review]. The Gardiner 2023 meta-analysis (24 studies)
  found caffeine reduces total sleep time by ~45 min, increases sleep onset latency by ~9 min,
  increases WASO by ~12 min, lowers sleep efficiency by ~7%, and shifts architecture toward more
  N1 and less N3; it modeled cutoffs of ≥8.8 h before bed for a standard coffee (~107 mg) and
  ≥13.2 h for a high-dose pre-workout (~217 mg) [9, meta_analysis]. An earlier fixed-dose RCT
  (400 mg at 0/3/6 h before bed) found measurable disruption even when taken 6 h before bedtime
  [10, rct]. The "stop caffeine by early afternoon" heuristic is **directionally supported but
  dose- and genotype-dependent**; the agent should reason in half-lives, not a fixed clock time.
- **Alcohol.** Alcohol shortens sleep onset and consolidates the first half of the night but
  fragments the second half: it suppresses REM (dose-dependent, pronounced at moderate-to-high
  doses) and increases WASO with reduced sleep efficiency in the latter half — effects seen even
  at low-to-moderate doses near bedtime [11, mechanism_review]. The popular belief that a
  "nightcap" aids sleep is contradicted by the architecture data.
- **Light.** Morning bright light and evening light restriction are mechanistically grounded in
  circadian phase-shifting (see D.3) [6, regulatory]. The *insomnia*-specific RCT evidence for
  blue-light blocking is thinner than marketing implies; the strong evidence is in the *circadian*
  literature, not as a general insomnia cure.
- **Temperature, exercise timing, meal timing.** Cooler ambient temperature supports sleep
  onset (core-body-temperature drop is a physiological sleep signal — the same mechanism invoked
  for glycine, D.4) [12, rct for glycine/temperature mechanism]. Exercise and meal-timing
  effects on sleep are real but heterogeneous and lower-certainty; the agent should treat them as
  reasonable defaults rather than evidence-backed prescriptions.

**Design consequence:** the agent must grade sleep-hygiene advice as lower-certainty than CBT-I
and must not present hygiene as a treatment for diagnosed chronic insomnia.

---

## D.3 — Circadian interventions: timed light and timed (low-dose) melatonin

This is where light and melatonin have their **strongest, mechanism-anchored** evidence — as
*chronobiotics* (phase-shifters), distinct from their weak role as general hypnotics.

**Timed light.** The AASM 2015 clinical practice guideline for intrinsic circadian rhythm
sleep-wake disorders gives a (lower-tier) positive endorsement of light therapy ± behavioral
interventions for advanced sleep-wake phase disorder (ASWPD) in adults, DSWPD in
children/adolescents, and dementia-related irregular rhythm in the elderly — while noting
**insufficient evidence** to recommend bright-light or light-avoidance strategies for adult
DSWPD specifically [6, regulatory]. The honest read: timed light is the right *tool* for
circadian misalignment, but guideline confidence is "second tier," not strong.

**Timed melatonin (chronobiotic dosing).** For circadian use, **low physiological doses
(0.5–1 mg) timed relative to dim-light melatonin onset** are the chronobiotic mechanism — not the
3–10 mg "hypnotic" mega-doses sold OTC. The AASM 2015 guideline positively endorses strategically
timed melatonin for DSWPD, blind adults with non-24-hour disorder, and certain pediatric ISWRD
[6, regulatory]. For **jet lag**, the Cochrane review (10 trials) found melatonin taken near
target bedtime decreased jet lag after eastward flights crossing ≥5 time zones, with NNT ≈ 2;
doses of 0.5–5 mg were similarly effective (5 mg gave marginally better subjective sleep), and
doses >5 mg were no better. Critically, **mistimed melatonin can shift the clock the wrong way**
[5, meta_analysis].

**Design consequence:** the agent should treat *timing relative to the individual's circadian
phase* as the active ingredient and should distinguish chronobiotic dosing (0.5–1 mg) from
hypnotic megadosing. Even at low risk_tier, dosing of an exogenous hormone is a compound decision
— the agent reasons about the protocol but routes the prescription/dose-selection decision per
D.4's routing rule.

---

## D.4 — Sleep-relevant OTC/supplement compounds: evidence tier and honest verdict

For each compound: evidence tier and honest verdict. **The headline: most are weak or mixed, and
OTC melatonin has a documented label-integrity problem.**

- **Melatonin (as a hypnotic).** Modest, mainly latency/circadian. Ferracioli-Oda 2013
  meta-analysis (19 studies, 1,683 subjects) found melatonin reduced sleep onset latency by only
  **7.06 min (95% CI 4.37–9.75)** and increased TST by ~8 min — statistically real, clinically
  small [13, meta_analysis]. Effect is far larger for circadian indications (DSPD ~38.8 min)
  than for insomnia (~7.2 min) [13, meta_analysis]. **Verdict: weak as a hypnotic, legitimate
  as a chronobiotic (D.3).**
  - **OTC purity/labeling problem (documented).** Erland & Saxena 2017 (analytical study, 31
    products / 16 brands) found melatonin content ranging **−83% to +478% of label**, with >71%
    of products outside ±10% of label and serotonin contamination in 26% of samples [14,
    regulatory]. A 2023 JAMA analytical study of 25 melatonin gummies found actual melatonin at
    **74–347% of labeled content**, with unlabeled CBD present in some [15, regulatory]. OTC
    melatonin is a dietary supplement in the US and is not pre-market FDA-verified for content.
- **Magnesium.** Mahdavi/older-adult systematic review & meta-analysis (3 RCTs, 151 subjects)
  found sleep onset latency ~17.4 min lower vs. placebo, but TST gain was non-significant and all
  trials were moderate-to-high risk of bias with **low-to-very-low certainty** [16,
  meta_analysis]. **Verdict: weak/uncertain; evidence base described by the authors as
  substandard for firm recommendations.**
- **Glycine.** Yamadera small RCT — 3 g ~1 h before bed shortened PSG sleep onset latency and
  improved subjective quality in people with sleep complaints, plausibly via core-body-temperature
  lowering [12, rct]. **Verdict: promising mechanism, small/low-N evidence.**
- **L-theanine.** Small RCTs (often combined with other agents, e.g. Mg-L-theanine or
  casein hydrolysate + L-theanine) report subjective sleep-quality improvement, mainly via
  anxiolysis rather than direct hypnosis [17, rct]. **Verdict: weak; effect entangled with
  co-administered agents and anxiety reduction.**
- **Valerian.** Mixed/inconclusive; trials are heterogeneous and frequently low-quality, and
  valerian-containing products were among those contaminated with serotonin in the Erland
  analysis [14, regulatory]. **Verdict: weak/mixed, with quality-control concerns.**
- **Apigenin (chamomile constituent).** Evidence for isolated apigenin in humans is essentially
  mechanistic/preclinical (GABA-A modulation); human sleep RCTs of purified apigenin are lacking
  [18, mechanism_review]. **Verdict: very-low certainty in humans.**

**Routing rule (load-bearing for the agent's design).** Any sleep-relevant compound at
**risk_tier medium or higher**, and **any prescription hypnotic** (z-drugs, benzodiazepines,
DORAs such as suvorexant, sedating antidepressants/antipsychotics used off-label), routes OUT of
this agent's domain to the supplement/endocrine/peptide specialists or to prescribing clinicians.
Even low-risk OTC compounds: the agent may discuss evidence but must not present
purity-unverified OTC melatonin as equivalent to a controlled chronobiotic protocol, given the
label-integrity literature above [14, regulatory; 15, regulatory].

---

## D.5 — GRADE-style two-axis grading (certainty × strength)

The agent's design should inherit a **two-axis** discipline: *certainty* (high/moderate/low/
very-low) is independent of *strength* (strong/weak/conditional). The canonical HALT condition is
**a strong recommendation resting on low certainty** — which is exactly the CBT-I situation.

| Intervention | Certainty | Strength | Note |
|---|---|---|---|
| CBT-I (multicomponent, chronic insomnia) | **Low–moderate** (downgraded for imprecision + risk of bias) [1] | **STRONG** [1] | **HALT-flag case:** strong rec on low-moderate certainty. Privilege it, but the agent should surface the certainty gap rather than imply high-certainty proof. |
| Sleep hygiene as single-component therapy | Low | Recommendation **AGAINST** standalone [1] | Adjunct only. |
| Timed melatonin — circadian (DSPD, jet lag, N24) | Low–moderate [5,6] | Conditional / second-tier positive [6] | Chronobiotic dosing 0.5–1 mg; timing is the active ingredient. |
| Melatonin — general hypnotic for insomnia | Low [13] | Weak | Effect ~7 min on latency; small. |
| Timed light — circadian disorders | Low [6] | Conditional / second-tier [6] | Insufficient evidence for adult DSWPD specifically [6]. |
| Caffeine restriction near bed | Moderate [9] | Reasonable default | Reason in half-lives, not fixed clock. |
| Alcohol avoidance near bed | Moderate [11] | Reasonable default | Contradicts the "nightcap" belief. |
| Magnesium / valerian / L-theanine / glycine / apigenin | Low–very-low [12,16,17,18] | Weak / not recommended | Do not over-sell. |

**Design consequence:** CBT-I is the explicit two-axis HALT case — a STRONG recommendation built
on LOW-to-MODERATE certainty. The agent should still privilege CBT-I (the strength axis is what
governs the *action*), but its communication layer must not launder low certainty into false
confidence. Where the popular framing claims high-certainty proof for any intervention in this
section, the agent flags the certainty/strength mismatch.

---

## Bibliography

[1] Edinger JD, et al. 2021 — *J Clin Sleep Med* — AASM clinical practice guideline + systematic review/meta-analysis/GRADE — PMID 33164741 — https://pmc.ncbi.nlm.nih.gov/articles/PMC7853211/ (companion guideline: https://pmc.ncbi.nlm.nih.gov/articles/PMC7853203/)
[2] Trauer JM, Qian MY, Doyle JS, Rajaratnam SMW, Cunnington D. 2015 — *Ann Intern Med* 163(3):191–204 — systematic review/meta-analysis — PMID 26054060 — https://pubmed.ncbi.nlm.nih.gov/26054060/
[3] Qaseem A, et al. (ACP) 2016 — *Ann Intern Med* — clinical practice guideline (CBT-I first-line) — summarized via AASM/ACP — https://aasm.org/new-guideline-supports-behavioral-psychological-treatments-for-insomnia/
[4] Furukawa Y, et al. 2024 — *JAMA Psychiatry* — component & delivery-format network meta-analysis — PMID 38231522 — https://pubmed.ncbi.nlm.nih.gov/38231522/
[5] Herxheimer A, Petrie KJ. 2002 — *Cochrane Database Syst Rev* — systematic review/meta-analysis (melatonin for jet lag) — PMID 12076414 — https://pubmed.ncbi.nlm.nih.gov/12076414/
[6] Auger RR, et al. 2015 — *J Clin Sleep Med* 11(10):1199–1236 — AASM clinical practice guideline, intrinsic circadian rhythm sleep-wake disorders — PMID 26414986 — https://pubmed.ncbi.nlm.nih.gov/26414986/
[7] (2025) — *systematic review/meta-analysis, sleep hygiene education for insomnia* — PMID 40449065 — https://pubmed.ncbi.nlm.nih.gov/40449065/
[8] Evans J, Richards JR, Battisti AS. — *Caffeine — StatPearls* (NIH/NCBI Bookshelf) — mechanism/pharmacokinetics review — NBK519490 — https://www.ncbi.nlm.nih.gov/books/NBK519490/
[9] Gardiner C, et al. 2023 — *Sleep Med Rev* 69:101764 — systematic review/meta-analysis (caffeine & sleep) — PMID 36870101, DOI 10.1016/j.smrv.2023.101764 — https://pubmed.ncbi.nlm.nih.gov/36870101/
[10] Drake C, Roehrs T, Shambroom J, Roth T. 2013 — *J Clin Sleep Med* 9(11):1195–1200 — RCT (caffeine 0/3/6 h before bed) — PMID 24235903 — https://pubmed.ncbi.nlm.nih.gov/24235903/
[11] Ebrahim IO, Shapiro CM, Williams AJ, Fenwick PB. 2013 — *Alcohol Clin Exp Res* — mechanism/narrative review (alcohol and normal sleep) — PMID 23347102 — https://pubmed.ncbi.nlm.nih.gov/23347102/
[12] Yamadera W, et al. 2007 — *Sleep Biol Rhythms* — RCT (glycine 3 g before bed, PSG) — https://pmc.ncbi.nlm.nih.gov/articles/PMC10828290/ (systematic review of glycine effects collating the trial)
[13] Ferracioli-Oda E, Qawasmi A, Bloch MH. 2013 — *PLoS One* 8(5):e63773 — meta-analysis (melatonin for primary sleep disorders) — PMID 23691095 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3656905/
[14] Erland LAE, Saxena PK. 2017 — *J Clin Sleep Med* 13(2):275–281 — analytical/regulatory-quality study (melatonin content variability + serotonin contamination) — PMID 27855744, DOI 10.5664/jcsm.6462 — https://pmc.ncbi.nlm.nih.gov/articles/PMC5263083/
[15] Cohen PA, et al. 2023 — *JAMA* — analytical study (melatonin & CBD content of gummies) — PMID 37097362 — https://pubmed.ncbi.nlm.nih.gov/37097362/
[16] Mah J, Pitre T. 2021 — *BMC Complement Med Ther* — systematic review/meta-analysis (oral magnesium for insomnia in older adults) — PMID 33865376 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8053283/
[17] Dasdelen MF, et al. 2022 — *Front Nutr* — RCT (Mg-L-theanine, sleep quality) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9017334/
[18] Salehi B, et al. — apigenin mechanism review (GABA-A modulation) — *NCBI/PMC* mechanism_review — https://pmc.ncbi.nlm.nih.gov/articles/PMC1490287/ (and StatPearls melatonin/herbal context)

---

## Self-check

**Claims where the popular claim outruns the evidence (the agent must guard against these):**

1. **"Sleep hygiene fixes insomnia."** False as stated. AASM recommends *against* sleep hygiene
   as standalone therapy [1]; it is an adjunct. Popular wellness content inverts this.
2. **"Melatonin is a sleeping pill."** Overstated. Hypnotic effect on latency is ~7 min [13];
   its real strength is circadian/chronobiotic, low-dose, timed [5,6]. And OTC content is
   frequently wrong by large margins [14,15] — a popular product with a documented quality
   problem.
3. **"Magnesium / valerian / L-theanine / glycine / apigenin are proven sleep aids."** All sit at
   low-to-very-low certainty with small N, high risk of bias, or human evidence largely absent
   (apigenin) [12,16,17,18]. The agent must not present them as established.
4. **"A nightcap helps you sleep."** Contradicted: alcohol fragments the second half of the
   night and suppresses REM [11].
5. **"Stop caffeine by 2 pm" as a universal rule.** Directionally right but the agent should
   reason in half-lives and dose, not a fixed clock time; genotype variation is large [8,9].

**Two-axis HALT condition surfaced:** CBT-I is a **STRONG recommendation on LOW-to-MODERATE
certainty** [1] — the canonical "strong-rec-on-low-certainty" case. The agent privileges CBT-I
(strength governs action) but must report the certainty gap rather than imply high-certainty
proof.

**Claims with citation-traceability caveats (flagged for verification before wiki ingestion):**

- [3] ACP first-line CBT-I recommendation: cited here via the AASM/ACP summary page (aasm.org,
  Tier-2 whitelisted). The primary is Qaseem A, et al. *Ann Intern Med* 2016 (PMID 27136449);
  the Annals full text returned HTTP 403 during retrieval (paywall) — the *recommendation
  direction* is corroborated by [1], but the exact primary citation should be re-pulled from PMC
  before ingestion.
- [12] Yamadera glycine RCT: accessed via a 2024 systematic review collating the trial rather
  than the 2007 primary directly; the primary (Yamadera W, et al. *Sleep Biol Rhythms* 2007)
  should be confirmed by PMID before ingestion.
- [17] L-theanine: effect is entangled with co-administered agents (Mg, casein hydrolysate);
  isolated L-theanine sleep RCTs are sparse. Treat as weak.
- [18] Apigenin: human sleep RCT evidence is essentially absent; the citation supports mechanism
  only. The DOI/PMID for the apigenin-specific mechanism source should be pinned before ingestion
  (currently anchored to a melatonin/herbal-context PMC record).
- Caffeine half-life "~5 h (range 2–10 h)" [8] is from StatPearls (NIH Bookshelf, Tier-2,
  whitelisted) — acceptable as authoritative, not a primary RCT.

All other claims are grounded to whitelisted Tier-1 (PMC/PubMed: SLEEP/JCSM, Ann Intern Med,
PLoS One, Sleep Med Rev, JAMA, Cochrane) or Tier-2 (aasm.org, nih.gov/NCBI Bookshelf) sources.
