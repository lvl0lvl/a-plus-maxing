---
title: "Sleep Efficiency: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/sleep-efficiency/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.sleep-efficiency-design-work
provenance_slug: labs-specialist
source_count: 30
---

# Sleep Efficiency: Canonical Research Report

## Summary

Sleep efficiency (SE) is the fraction of time in bed actually spent asleep, expressed as a percentage: **SE (%) = Total Sleep Time (TST) ÷ Time in Bed (TIB) × 100**. It is a wearable-derived sleep-continuity metric — the primary quantitative index of how consolidated and uninterrupted sleep is relative to the opportunity provided. SE does not measure sleep architecture, timing, or adequacy of duration; it measures continuity alone.

The population benchmark for healthy adults is **≥85% SE**, established by a National Sleep Foundation expert consensus panel as the threshold consistent with appropriate sleep quality [10, mechanism_review]. In practice, healthy adults typically land in the 85–95% range, though this compresses with age: polysomnographic normative data show SE declines by approximately 2.1% per decade (95% CI: 1.5–2.6%) [11, meta_analysis]. A 65-year-old with SE of 82–83% may be within their age-adjusted norm; the same figure in a 30-year-old is clearly below expectation.

**The most load-bearing technical fact about consumer wearable SE is that it systematically overestimates true SE.** Wearables cannot reliably detect quiet wakefulness — periods when a person lies still in bed but is awake. Because accelerometry classifies immobility as probable sleep, motionless wake epochs are scored as sleep. This produces high sleep-detection sensitivity (≥0.93 across devices) but low wake-detection specificity (0.18–0.54 in the best multi-device study) [4, cohort]. The downstream effect: wearable SE reads 2–15 percentage points above what polysomnography (PSG) would record for the same night, with the overestimate worsening on nights with genuinely poor continuity. Sleep staging accuracy is categorically lower still — consumer apps report light/deep/REM proportions with only 65–75% accuracy on average [21, mechanism_review], making stage counts far less reliable than the SE summary metric.

The actionable signal from a wearable SE is primarily the **personal-baseline trend**, not the absolute number. A sustained drop of 5–8 percentage points below a person's stable 7–14-night rolling average flags acute disruptors — elevated alcohol, illness, stress, environmental disruption — even when the absolute value cannot be directly compared to PSG-derived clinical thresholds. The ≥85% benchmark is a population reference calibrated to PSG and sleep-diary data; a wearable reading of 90% may correspond to a true PSG SE of 80%.

CBT-I, specifically its sleep restriction therapy (SRT) component, is the most evidence-supported lever for raising SE. A pre-registered meta-analysis of eight RCTs found SRT produced a large effect on SE (Hedges' g = 0.91; 95% CI 0.52–1.31) [28, meta_analysis]. SE improvement is both a mechanism and a primary outcome target of CBT-I.

Two caveats are load-bearing. First, **SE is necessary but not sufficient**: a person with 5.5 hours in bed and 95% SE is sleep-deprived; SE gives no information about whether total sleep opportunity is adequate in duration or stage composition. Second, the **orthosomnia hazard**: fixating on tracker sleep scores can itself worsen sleep and generate anxiety. Baron et al. named and described this clinically recognized pattern in a case series of sleep-clinic patients who had been harmed by preoccupation with their tracker data [30, open_label]. The hard-outcome epidemiology (cardiovascular, mortality associations) mostly uses self-reported sleep duration and questionnaire-based quality measures, not consumer wearable SE — so the absolute wearable SE number should not be over-medicalized or treated as an individual health-risk predictor.

All SE values in this report are expressed as percentages (%).

---

## What Sleep Efficiency Is & What the Device Measures

### Definition and Formula

Sleep efficiency (SE) is a summary index of sleep continuity — the fraction of in-bed time actually spent asleep:

**SE (%) = Total Sleep Time (TST) ÷ Time in Bed (TIB) × 100**

SE does not describe sleep architecture (how much REM or slow-wave sleep occurred) nor the circadian timing of sleep. Its narrow, well-specified job is to capture how consolidated the sleep episode was. An SE of 85% means that 15% of in-bed time was spent awake — through difficulty falling asleep, middle-of-the-night waking, or lying in bed after the final awakening.

### Component Definitions

**Time in Bed (TIB)** is the full window from the moment the person settles into bed with the intent to sleep ("lights out") to the moment they rise for the final time ("out of bed" or "lights on"). TIB is the denominator; it captures total opportunity, not total sleep.

**Total Sleep Time (TST)** is the sum of time actually scored as sleep within the TIB window. In polysomnographic (PSG) terms, TST = time in stages N1 + N2 + N3 + REM. Arithmetically, TST = TIB − sleep-onset latency (SOL) − wake after sleep onset (WASO) − early morning awakening [1, regulatory].

- **SOL** (sleep-onset latency): the interval from lights-out to the first sustained sleep epoch. The AASM Scoring Manual v3 (2023) distinguishes SOL-to-N1 from SOL-to-persistent-sleep (first epoch of N2, N3, or REM sustained across 10 minutes) [1, regulatory].
- **WASO** (wake after sleep onset): all wake time logged after sleep onset and before final rising. WASO captures nocturnal awakenings and is the primary driver of SE degradation in insomnia [1, regulatory].

**Low SE** therefore signals one of two problems — or both: the sleeper took a long time to fall asleep (high SOL), or they woke frequently and lay awake in the night (high WASO). High SE means the available time in bed was used efficiently for sleep.

### SE as a Distinct Metric

SE is a single number that summarizes the components above; it does not replace them. SOL, WASO, TST, and sleep-stage percentages each carry distinct clinical information. A person with 7 hours TIB, 30-minute SOL, and 0 WASO has 87% SE; a person with 7 hours TIB, 0-minute SOL, and 30 minutes of fragmented WASO has the same 87% SE. The number is identical but the physiology differs. SE is therefore most informative alongside its component terms, not in isolation [2, mechanism_review].

### The PSG Gold Standard

PSG scores sleep from concurrent electroencephalography (EEG), electro-oculography (EOG), and electromyography (EMG), epoch-by-epoch (standard epoch length: 30 seconds), per AASM Scoring Manual v3 (2023) rules [1, regulatory]. The resulting hypnogram is the ground truth from which TIB, TST, SOL, WASO, and stage percentages are computed. PSG-derived SE is the reference against which every wearable estimate is validated. Clinical assessment of insomnia uses SOL or WASO exceeding 30 minutes and SE below 85% as practical anchors for sleep-diary evaluation [22, regulatory].

### What Consumer Wearables Actually Measure

Consumer devices — fitness bands, smartwatches, ring-form-factor trackers — do not record EEG. Instead, they use two primary sensor streams:

1. **Actigraphy / accelerometry**: wrist (or finger) movement signals sampled at high frequency, used to infer sleep/wake state. Immobility is treated as probable sleep; movement interruptions as probable wakefulness.
2. **Photoplethysmography (PPG)**: optical heart rate and, in many modern devices, heart rate variability (HRV). PPG-derived beat-to-beat interval patterns differ between sleep stages and wakefulness, enabling more nuanced stage estimation than movement alone.

Some devices additionally incorporate skin temperature sensors and respiratory-rate estimates derived from PPG signal morphology. These multimodal inputs feed proprietary machine-learning classifiers that are not publicly disclosed by manufacturers [3, mechanism_review; 4, cohort].

From these inferred sleep/wake (and stage) sequences, the device computes its own TST and its own estimate of the sleep window (time in bed), then calculates SE. **SE from a wearable is a derivative of the device's own imperfect sleep/wake scoring**, not a direct measurement of sleep.

### The Core Tension: Wearables Struggle to Detect Quiet Wakefulness

The most consequential limitation of movement-based wearable sleep scoring — and the one that directly inflates SE estimates — is the inability to distinguish quiet wakefulness from sleep.

A person lying still in bed, fully awake but not moving, generates the same low-amplitude accelerometer signal as a sleeping person. Because actigraphy classifies immobility as sleep, prolonged motionless wakefulness is systematically scored as sleep epochs. This is the "quiet wakefulness" problem, first formally characterized by Paquet et al. (2007), who demonstrated that subjects were immobile approximately half the time when awake, and that actigraphy's specificity for correctly detecting wake epochs was only ~50%, even when sensitivity for sleep detection was approximately 95% [5, cohort].

This asymmetry — high sensitivity to sleep, low specificity for wake — is the defining accuracy pattern across wearable sleep trackers. The SLEEP journal 2021 study of seven consumer devices found epoch-by-epoch wake specificity ranging from 0.18 to 0.54, with Fitbit Alta HR the best performer at 0.54 and both Garmin devices the worst at 0.18–0.19 [4, cohort]. The 2019 JCSM validation of Fitbit Alta HR in adolescents (aged 15–19 years; note: late-adolescent sample, results may not generalize to middle-aged or older adults) found that the device overestimated WASO by up to 42 minutes across three sleep-opportunity conditions compared to PSG [6, cohort].

The downstream effect on SE is direct: because WASO is underestimated (wakefulness misclassified as sleep), TST is inflated, and SE is overestimated. Danzig et al. (2020) found the Actiwatch overestimated SE by 6.8% and the Jawbone by 14.9% versus PSG, while underestimating WASO by 50.7 minutes [7, cohort]. In the multicenter 11-device study by Lee et al. (2023), the Google Pixel Watch showed a positive SE bias of approximately 12.8 percentage points above PSG [8, cohort]. A 2025 validation of six current wrist-worn devices found that all significantly overestimated SE by 2.2% to 10.2% compared to PSG, while simultaneously underestimating WASO by 12–48 minutes across devices [29, cohort].

This bias is not uniform: it worsens in populations with fragmented sleep. The more wake time a person accumulates in the night, the more the device misclassifies, and the larger the SE overestimate becomes [3, mechanism_review; 5, cohort]. PSG-validated reviews confirm the consistent pattern: wearables overestimate TST and underestimate WASO, yielding inflated SE, with the gap widening in insomnia and other sleep-disrupted populations [3, mechanism_review; 9, mechanism_review].

### What SE From a Wearable Can and Cannot Tell You

A wearable-derived SE reflects the device's estimate of sleep continuity across the inferred sleep window. For healthy sleepers with relatively consolidated sleep, the value will track reasonably well with PSG-derived SE across nights or weeks as a trend indicator. For nights with frequent nocturnal awakenings — insomnia, stress, illness, disrupted environments — the device will systematically undercount WASO, overcount TST, and return an SE that is measurably higher than what PSG would record.

A wearable SE of 90% may correspond to a PSG SE of 83% or to one of 73%, depending on how much quiet wakefulness occurred. This is not a trivial margin for clinical interpretation, but it does not nullify the metric's value for within-person longitudinal tracking: if a user's habitual wearable SE drops from 88% to 76% across two weeks, that signal likely reflects a real deterioration in sleep continuity even if the absolute calibration is uncertain.

SE remains one of the most interpretable outputs a consumer sleep device produces. Understood alongside its components and its known upward bias, it is a useful, if imprecise, window into how restorative the night was.

---

## Interpretation, Norms & The Personal-Baseline

### Population Norms: The ≥85% Benchmark

The anchoring clinical standard for SE in healthy adults is **≥85%**. A National Sleep Foundation (NSF) expert consensus panel — convened to produce evidence-based, lifespan-spanning sleep quality recommendations — identified SE >85% as the threshold consistent with "appropriate" sleep quality [10, mechanism_review]. The panel represented 19 researchers and clinicians across sleep medicine, neurology, psychiatry, and gerontology, and found SE and sleep onset latency to be the two continuity parameters with the highest expert agreement across all adult age groups [10, mechanism_review].

In practice, healthy adult sleepers typically land in the range of approximately **85–95% SE**, though this range compresses with age (see below). An SE below 85% indicates impaired sleep continuity — time in bed is being spent substantially awake — and SE <85% is a criterion-adjacent feature in the clinical characterization of insomnia: patients with insomnia disorder commonly present with SE well below this floor, and SE <85% (sometimes operationalized as <80–90% depending on the criterion and age context) has been shown to have strong sensitivity and specificity for distinguishing good-sleeping older adults from those with insomnia [13, cohort].

Buysse's multidimensional framework of sleep health — the RuSATED model (Regularity, Satisfaction, Alertness, Timing, Efficiency, Duration) — treats SE as one of six distinct dimensions [15, mechanism_review]. This framing is load-bearing for interpretation: SE is not sleep health in full; it is one facet among six. High SE does not imply adequate TST, favorable timing, or subjective satisfaction.

### SE Declines with Age

SE is not static across the lifespan. The largest polysomnography normative dataset assembled to date — a systematic review and meta-analysis of 169 studies enrolling 5,273 healthy adults, scored using AASM criteria — found that **SE decreases by 2.1% per decade** (95% CI: 1.5–2.6%) of advancing age [11, meta_analysis]. The same analysis documented that wake after sleep onset (WASO) increases by **9.7 minutes per decade** (95% CI: 6.9–12.4 min), and total sleep time falls by approximately 10 minutes per decade [11, meta_analysis]. The mechanistic driver is straightforward: aging is associated with more frequent nocturnal awakenings, lighter sleep architecture, and attenuated homeostatic sleep pressure — all of which lengthen WASO and compress SE [12, mechanism_review].

The practical implication is that the ≥85% benchmark should be applied with age context in mind. A 65-year-old with SE of 83% may represent normal age-adjusted sleep continuity rather than pathological disruption, whereas the same figure in a 30-year-old is more clearly below expectation. Interpreting SE without an age anchor risks pathologizing normative aging trajectories.

### Excessive Time in Bed Suppresses SE: The Sleep-Restriction Rationale

A non-obvious but clinically important property of SE is its **inverse sensitivity to excessive time in bed**. When a person spends more time in bed than their sleep need can fill — a common compensatory behavior in poor sleepers — the numerator (TST) stays roughly fixed while the denominator (TIB) grows, driving SE down. The sleep homeostatic drive is effectively diluted across a longer bed window, resulting in lighter, more fragmented sleep and reduced SE.

This is the core rationale for **sleep restriction therapy (SRT)**, a first-line behavioral component of cognitive behavioral therapy for insomnia (CBT-I). SRT instructs patients to curtail TIB to match estimated TST closely (often TST + ~30 minutes), which concentrates sleep pressure, increases sleep efficiency, and re-consolidates fragmented sleep [14, mechanism_review]. A 2026 mechanistic analysis applied and tested the "Triple-R" model of SRT action — which holds that SRT operates by restricting TIB, regularizing sleep-wake timing, and reconditioning bedroom-sleep associations — and found acute sleep pressure (the homeostatic build) to be the probable primary driver of early SE gains [16, mechanism_review]. The SRT literature consistently demonstrates that SE <85% at baseline is a reliable entry criterion for the intervention, and rising SE toward and past 85% tracks treatment progress [14, mechanism_review].

A parallel observation in older adults reinforces this: a pilot time-in-bed restriction study found that restricting TIB to 75% of habitual levels in older adults with poor SE significantly increased slow-wave activity across the 0.5–4 Hz range — indicating that TIB curtailment improves not just continuity but sleep-stage depth [13, cohort]. The implication for wearable-based self-monitoring is concrete: spending extra hours in bed to "make up" for poor sleep is likely to further erode SE rather than improve it.

### The Personal-Baseline Approach

For wearable users, the most actionable use of SE data is **within-person trending over time**, not population benchmarking. Because SE is subject to individual variation in sleep architecture, chronotype, and baseline sleep need, a single-night reading is low signal. The informative signal is a **deviation from one's own established baseline**: a 5–8 percentage-point drop in SE relative to a stable rolling average (typically 7–14 nights) is a meaningful flag for acute disruptors — elevated stress, alcohol, illness, environmental disruption (temperature, noise, travel), or schedule misalignment.

Common acute disruptors and their SE signatures:
- **Alcohol**: Alcohol accelerates sleep onset (briefly improving apparent sleep latency) but fragments the second half of the night as metabolism proceeds, suppressing REM and increasing WASO — net effect is often a drop in SE despite faster sleep onset.
- **Illness / fever**: Both immune activation and symptom burden (coughing, congestion, discomfort) fragment sleep continuity, raising WASO and lowering SE.
- **Stress / hyperarousal**: Cognitive and physiological hyperarousal at sleep onset extends latency and increases nocturnal awakening frequency, compressing SE.
- **Schedule disruption / late bedtime**: Social jetlag or irregular TIB windows shift homeostatic and circadian alignment, degrading SE.

The personal-baseline approach does not require hitting ≥85% every night. A stable baseline of, say, 82% for an older adult is meaningful health information. The clinically relevant signal is **sustained deterioration** from that individual's baseline, or **acute drops** suggesting a reversible disruptor.

### The Necessary-But-Not-Sufficient Caveat

SE is a necessary but not sufficient indicator of healthy sleep. Three failure modes deserve explicit notice:

1. **High SE with insufficient TST.** A person who spends only 5.5 hours in bed and sleeps 5 of them has SE ~91% — but is chronically sleep-deprived. SE gives no information about whether the sleep opportunity is adequate in duration.

2. **High SE with poor architecture.** SE is stage-agnostic: it counts all sleep equally regardless of depth or stage composition. A night dominated by N1/N2 with suppressed N3 (slow-wave) and REM — as seen with heavy alcohol use, certain medications, or pathological conditions — can produce high SE while delivering sleep of poor restorative quality.

3. **SE perfectionism.** Brief awakenings are a normal feature of healthy sleep. The population norm for SE in young-to-middle-aged healthy adults is roughly 85–92%, not 99–100%. Pursuit of maximally high SE — achieved by aggressively restricting TIB — carries the risk of partial sleep deprivation if TIB is curtailed below actual sleep need.

SE is best read alongside: **TST** (is sleep duration adequate?), **timing** (is sleep aligned with the circadian window?), and **subjective restedness** (does the person feel restored?). These four together substantially out-predict SE alone. The multidimensional RuSATED framework formalizes exactly this principle [15, mechanism_review].

---

## Measurement & Device Validity vs PSG

### Polysomnography: The Reference Standard

Polysomnography (PSG) is the established clinical and research reference standard for measuring sleep [1, regulatory]. During an attended overnight study, EEG, EOG, and chin EMG are recorded continuously and scored in sequential 30-second epochs according to the AASM Manual for the Scoring of Sleep and Associated Events, Version 3 (2023) [1, regulatory]. Each epoch receives one of five stage assignments: Wake (W), N1, N2, N3, or REM. Sleep efficiency is then computed as TST ÷ TIB × 100%, where TST = the sum of all non-wake epochs and TIB = the interval from lights-out to the end of the recording. WASO is scored from the summed wake epochs that fall between sleep onset and final awakening. This epoch-level EEG-based scoring is what consumer wearables must ultimately approximate.

### How Consumer Wearables Estimate Sleep

Modern consumer sleep trackers — Oura, Fitbit, WHOOP, Apple Watch, Garmin — use one or more of three sensor modalities: wrist or finger accelerometry, photoplethysmography (PPG), and skin temperature. Earlier-generation devices relied almost exclusively on accelerometry; current-generation devices combine PPG-derived HRV features with motion data and, in some cases, temperature signals [4, cohort; 9, mechanism_review]. All scoring is performed by proprietary machine-learning algorithms that are not publicly disclosed, which limits direct cross-device comparisons and reproducibility of research findings [9, mechanism_review].

### The Canonical Asymmetry: High Sleep Sensitivity, Low Wake Specificity

The single most robust and consistent finding across independent validation studies is an asymmetry between sensitivity for sleep and specificity for wake detection. Because quiet wakefulness (lying still in the dark) is often indistinguishable from light sleep in an accelerometry or PPG signal, wearables systematically classify motionless-wake epochs as sleep.

Chinoy et al. conducted the most-cited multi-device laboratory validation in the US, comparing seven consumer devices against in-lab PSG across two nights in 42 healthy adults [4, cohort]. Epoch-by-epoch results showed all devices achieved sleep-detection sensitivity ≥ 0.93 across the sample. Wake-detection specificity, however, ranged from 0.18 (Garmin Fenix 5S) to 0.54 (Fitbit Alta HR). The downstream consequence was substantial and device-specific overestimation of TST and SE, with WASO underestimation: the Garmin Vivosmart 3 overestimated TST by +46.8 min and SE by +10.1%, while underestimating WASO by −47.6 min; the Fitbit Alta HR performed far better at +2.6 min TST bias, +0.9% SE bias, −2.1 min WASO bias [4, cohort].

Haghayegh et al. performed a systematic review and meta-analysis of all published Fitbit validation studies against PSG through 2019 [17, meta_analysis]. Across earlier-generation (motion-only) Fitbit models, sensitivity for sleep ranged 0.87–0.99 while specificity for wake ranged only 0.10–0.52 — with whole-sample TST overestimation of 7–67 min, SE overestimation of 2%–15%, and WASO underestimation of 6–44 min. Among the newer sleep-staging Fitbit models (HRV + motion), sensitivity was higher (0.95–0.96) and specificity improved substantially (0.58–0.69); in this subset, group-level differences in TST, WASO, and SE vs PSG were no longer statistically significant, though individual-level variability remained [17, meta_analysis]. No conflicts of interest were declared by the authors [17, meta_analysis].

### Oura Ring Validation: Two Generations

de Zambotti et al. published the first independent PSG validation of the original Oura Ring (Gen 1) in 41 healthy adolescents and young adults (validation sample skewed young — mean age approximately 17; these figures should not be taken as adult-generalizable without qualification) [18, cohort]. Sleep-detection sensitivity was 96% and wake-detection specificity was only 48%, consistent with the canonical asymmetry. Summary measures for TST, WASO, and sleep onset latency did not significantly differ from PSG; 87.8% of TST values and 85.4% of WASO values fell within ±30 min of PSG. Sleep staging agreement, however, was substantially lower: 65% for light sleep (N1), 51% for deep sleep (N2+N3), and 61% for REM [18, cohort].

Svensson et al. (University of Tokyo, 2024) independently validated the Oura Ring Generation 3 with Sleep Staging Algorithm 2.0 against multi-night ambulatory PSG in 96 participants totaling 421,045 scored epochs [19, cohort]. The Gen3 ring did not significantly differ from PSG for TIB, TST, sleep onset latency, WASO, light sleep time, or deep sleep time; SE was slightly underestimated by 1.1%–1.5% and REM by 4.1–5.6 min. Binary sleep–wake classification sensitivity was 94.4%–94.5% with specificity of 73.0%–74.6% — a substantial wake-specificity improvement over earlier devices. Sleep staging accuracy ranged from 75.5% (light sleep) to 90.6% (REM), with overall accuracy 91.7%–91.8% and PABAK reliability of 94.8% [19, cohort]. This was an independent academic validation not funded by the manufacturer per disclosures.

A 2024 three-device comparison evaluated Oura Ring Gen3, Fitbit Sense 2, and Apple Watch Series 8 against PSG in 35 healthy adults [20, cohort]. For binary sleep–wake detection, all three devices achieved sensitivity ≥ 95%. For four-stage classification (wake/light/deep/REM), Oura Gen3 showed the most consistent per-stage sensitivities (76.0–79.5%), followed by Fitbit Sense 2 (61.7–78.0%) and Apple Watch (50.5–86.1%, but notably lower for deep sleep at 50.5%). Epoch-level four-stage agreement was strongest for Oura (Kappa = 0.65) vs Fitbit (0.55) and Apple Watch (0.60) [20, cohort].

### Sleep Staging Accuracy Is Categorically Lower Than Sleep–Wake Accuracy

Across the literature, sleep–wake binary accuracy typically exceeds 90%, but four-class staging (wake/N1/N2/N3/REM) agreement with PSG is substantially lower [9, mechanism_review]. The de Zambotti et al. 2024 consensus review synthesized the field: epoch-by-epoch staging accuracies fall approximately 50%–90% for light sleep (PSG N1+N2), 30%–80% for deep sleep (PSG N3), and 30%–80% for REM sleep, with no consistent directional bias for staging [9, mechanism_review]. (COI note: de Zambotti, lead author of [9, mechanism_review], lists an affiliation with Lisa Health Inc., a digital health company; this potential commercial interest should be weighed when interpreting the review's recommendations, though the quantitative accuracy ranges it synthesizes are drawn from the cited primary studies.) In an independent systematic review of wearable staging algorithms, PPG-based three- and four-class systems achieved classification accuracies broadly in the 65–75% range across published studies [21, mechanism_review]. The poorest agreement is consistently observed at N1/N2 boundaries and during the detection of brief N3 epochs. The consequence for users: consumer "deep sleep" and "REM" minute-counts should be interpreted as rough structural estimates, not precise PSG-equivalent measures. The SE summary metric — which aggregates all non-wake time — is consistently more reproducible than any single stage estimate.

### Practical Limitations for Interpreting Wearable SE

**In-bed window detection.** PSG defines TIB precisely from technician-confirmed lights-out to final-awakening. Consumer wearables must infer bedtime and rise time automatically from movement and physiological signals, or rely on user-entered data. Errors in this inference directly propagate into both SE and TST; a device that detects "lights out" 30 min early can artifactually inflate TIB and thus deflate SE by several percentage points. Manual-log settings generally outperform auto-detection, but compliance is inconsistent in free-living use [9, mechanism_review].

**Proprietary algorithms and firmware updates.** Each manufacturer's scoring algorithm is a trade secret. Validation studies conducted on one firmware version may not generalize after an automatic software update — a documented issue that makes cross-study and longitudinal comparisons difficult [9, mechanism_review; 4, cohort]. Devices from different manufacturers should not be treated as interchangeable even when marketing the same metric.

**Within-device trend validity.** Because systematic biases are partially consistent within the same device and user, relative night-to-night changes in SE (comparing the same device under similar sleep conditions) carry more interpretive weight than absolute SE values compared across devices or against PSG-derived norms. This is the appropriate frame for wellness self-tracking.

**Population boundary.** Validation studies are predominantly conducted in healthy young adults in a single-night laboratory setting. Performance in populations with insomnia disorder, older adults, shift workers, athletes, or individuals with darker skin tones (where PPG accuracy can be lower) may differ meaningfully from reported figures [9, mechanism_review; 20, cohort].

**Diagnostic scope.** Consumer sleep tracking is a wellness tool, not a clinical diagnostic instrument. No wearable device is cleared to diagnose insomnia disorder, obstructive sleep apnea, or any other sleep pathology. A persistently low wearable SE reading that concerns a user is an indication to pursue clinical evaluation — not a substitute for it.

---

## Determinants & Significance

### What Lowers Sleep Efficiency

Sleep efficiency is degraded by any process that increases time spent awake after lights-out while time in bed remains fixed.

**Insomnia.** Poor SE is the cardinal polysomnographic and sleep-diary signature of insomnia disorder. Patients spend adequate or excessive time in bed but cannot initiate or maintain sleep — producing high SOL, high WASO, or both. Clinical thresholds for defining problematic continuity, by consensus, are SOL or WASO exceeding 30 minutes and SE below 85% [22, regulatory]. These values are not hard diagnostic cutoffs but practical anchors for sleep-diary assessment.

**Excessive time in bed.** Paradoxically, spending too long in bed relative to actual sleep need suppresses homeostatic sleep pressure and fragments the sleep that does occur — a key insight underlying the sleep-restriction component of CBT-I. High time-in-bed with low sleep drive is a common perpetuating factor in chronic insomnia.

**Aging.** SE declines across the adult lifespan and continues to fall beyond age 90. Polysomnographic studies document a concurrent rise in arousal frequency, increased WASO, and reduced slow-wave and REM sleep proportions with advancing age [23, mechanism_review]. Men over 70 show roughly a 50% decline in slow-wave sleep relative to men under 55, with concomitant increases in lighter NREM stages and arousal index. The underlying mechanisms include reduced homeostatic sleep pressure, circadian amplitude attenuation, loss of ventrolateral preoptic nucleus neurons, and increased prevalence of age-related sleep-disordered breathing [23, mechanism_review].

**Alcohol.** Evening alcohol reliably suppresses sleep onset latency and promotes deep NREM in the first half of the night, which tends to mask its damaging second-half effect. As ethanol is metabolized — typically around the 3–4-hour mark — sedation gives way to sympathetic rebound, increased arousability, and fragmented sleep. Controlled experimental studies in late-adolescent participants (ages 18–21) document increased WASO and reduced SE specifically in the second half of the night following alcohol consumption, with a statistically significant time-of-night interaction (p = 0.034 for WASO; p = 0.042 for SE) [24, rct] (note: late-adolescent sample, ages 18–21; these quantitative values derive from that age group and may differ in magnitude in older adults). The second-half fragmentation direction is consistent with adult controlled studies: a systematic narrative review of controlled human studies confirmed that this pattern — NREM and slow-wave promotion early, followed by REM suppression with later REM rebound and sleep fragmentation — is reproducible across moderate-to-high doses in adults [25, mechanism_review]. Alcohol also exacerbates snoring and obstructive events, compounding fragmentation through the respiratory pathway.

**Caffeine, nicotine, and evening stimulants.** Caffeine's adenosine-receptor antagonism reduces homeostatic sleep pressure; its half-life of approximately 5–7 hours means afternoon consumption displaces sleep onset and degrades continuity into early morning hours. Nicotine is a stimulant with suppressive effects on REM sleep; regular users show fragmented sleep and early-morning awakenings linked to overnight withdrawal.

**Stress, anxiety, and hyperarousal.** The hyperarousal model of insomnia positions persistent cognitive and physiological over-activation — rumination, worry, somatic tension — as the primary driver of sleep-onset and sleep-maintenance difficulty. Anxious pre-sleep cognition extends SOL and promotes brief nocturnal arousals that elongate into full wakefulness.

**Sleep-disordered breathing.** Obstructive sleep apnea (OSA) fragments sleep via repetitive respiratory arousals; as airway obstruction resolves with each arousal, the patient briefly awakens before returning to sleep — often without conscious recollection. The cumulative arousal burden correlates with excessive daytime sleepiness across OSA severity grades. Because many brief arousals fall below the 30-second epoch threshold for scored wake time, PSG-derived SE in OSA frequently underestimates the true continuity disruption [26, cohort]. Restless legs syndrome and periodic limb movement disorder produce similar fragmentation through limb-movement arousals. Circadian rhythm disorders (shift work, jet lag, delayed or advanced sleep-phase) degrade SE by misaligning the sleep opportunity window with the circadian drive for sleep.

**Environmental and behavioral factors.** Ambient noise, light exposure, and elevated room temperature all raise arousal thresholds and increase microarousal frequency. Evening screen use contributes through blue-light-mediated suppression of melatonin onset and through cognitive arousal from content. Pain and nocturia (both common in older adults and clinical populations) are frequent causes of maintenance insomnia. Certain medications — including some antidepressants, beta-blockers, corticosteroids, and decongestants — activate the CNS or fragment sleep architecture as a side effect.

### What Raises Sleep Efficiency

**CBT-I and sleep restriction therapy.** The most evidence-supported behavioral lever for raising SE is cognitive behavioral therapy for insomnia (CBT-I), for which the AASM issues a strong recommendation as first-line treatment for chronic insomnia in adults [27, regulatory]. Among CBT-I's components, sleep restriction therapy (SRT) is the most directly SE-targeted: by temporarily limiting time in bed to match actual sleep time, it builds homeostatic sleep pressure and compresses wakefulness within the sleep window. A pre-registered meta-analysis of eight RCTs found a large effect favoring SRT over control for SE (Hedges' g = 0.91; 95% CI 0.52–1.31), alongside large effects on insomnia severity index, SOL, and WASO [28, meta_analysis]. SE improvement is therefore not just a consequence of CBT-I — it is a primary mechanism and a primary outcome target. Stimulus control therapy (breaking the conditioned arousal between bed and wakefulness) augments SE by restoring the bed–sleep association.

**Sleep hygiene and sleep pressure.** Regular sleep and wake timing, avoidance of daytime napping, limiting time in bed to actual sleep need, and moderate aerobic exercise all support adequate homeostatic pressure at bedtime. A dark, cool, quiet sleep environment reduces arousals throughout the night.

### Significance: Sleep Continuity, Insomnia, and Health Associations

SE is a core index of **sleep continuity** — the degree to which sleep is sustained from onset through the final awakening without fragmentation. As such, it is among the primary metrics used in clinical assessment of insomnia and in CBT-I outcome trials. A reading below 85% is conventionally flagged as a continuity concern in clinical practice guidelines [22, regulatory]; CBT-I trials routinely use SE as a primary or co-primary endpoint, and SE improvement is one of the most replicable effects in the behavioral sleep medicine literature [27, regulatory; 28, meta_analysis].

Poor sleep continuity — whether indexed by SE, WASO, or total fragmentation — is associated in epidemiological literature with adverse cardiometabolic, mental health, and all-cause mortality outcomes. **However, honesty is required about what this evidence actually shows.** The large prospective cohorts establishing these associations overwhelmingly used self-reported sleep duration, self-reported sleep quality questionnaires, or at most research-grade actigraphy — not consumer wearable SE specifically. Wearable-derived SE as a standalone predictor of hard clinical outcomes (cardiovascular events, incident diabetes, mortality) has not been established in prospective studies with adequate size, follow-up, and outcome adjudication. Translating a population-level associative signal from self-reported sleep measures to an individual's wearable SE number involves a chain of assumptions that the current evidence does not support. Claims that a given nightly wearable SE reading predicts individual health risk go well beyond the data.

### Limitations: Accuracy, Over-Interpretation, and Orthosomnia

**Consumer devices overestimate SE.** The most consistent finding across wearable validation studies is that consumer sleep trackers overestimate SE relative to PSG, because they have difficulty detecting quiet wakefulness. In the 2021 seven-device validation, all devices that significantly overestimated total sleep time did so for SE as well, with biases most pronounced on nights with genuinely low SE [4, cohort]. A 2025 validation of six current wrist-worn devices found that all significantly overestimated SE by 2.2% to 10.2% compared to PSG (p values from <0.001 to 0.024), while simultaneously underestimating WASO by 12–48 minutes across devices [29, cohort]. The practical implication: a device SE reading of 88% may correspond to a PSG-validated SE of 78–86%. The bias is worst precisely when it matters most — in people with the worst continuity.

**Sleep staging is unreliable.** Beyond the binary sleep/wake problem, multi-stage classification (light, deep, REM) on consumer wearables shows only fair-to-moderate agreement with PSG (Cohen's kappa 0.21–0.53 across devices in the Schyvens et al. 2025 study) [29, cohort]. Stage-specific percentages reported by consumer apps should not be interpreted as clinical sleep architecture values.

**SE is necessary but not sufficient.** High SE does not confirm adequate sleep. A person sleeping 5 hours with 95% SE may have far worse cardiometabolic and cognitive consequences than someone sleeping 8 hours with 85% SE. SE must always be interpreted alongside total sleep time, sleep timing, and subjective restedness.

**Orthosomnia.** A clinically documented hazard of consumer sleep tracking is orthosomnia — a preoccupation with achieving perfect or "correct" sleep data that itself worsens sleep. Baron et al. (2017) first described and named the phenomenon in a case series of patients who arrived at a sleep clinic having diagnosed themselves based on tracker output; PSG in several cases showed normal sleep architecture, yet their preoccupation with improving tracker scores had driven them to spend excessive time in bed (worsening SE by the very mechanism of sleep restriction in reverse), generated sleep-related anxiety, and in some cases interfered with CBT-I participation [30, open_label]. The authors coined the term by analogy to orthorexia — the pathological pursuit of dietary perfection — because patients had developed an analogous fixation on sleep perfection. Orthosomnia is not a formal diagnostic entity but a clinically recognized pattern that sleep medicine practitioners should screen for in wearable-using patients presenting with insomnia-like complaints.

**Interpretation guidance for wearable SE.** Consumer SE is best treated as a trend and wellness signal, not a diagnostic reading. Clinically useful questions are: Is my SE trending lower over days or weeks? Does it correlate with how rested I feel? What behavioral factors (alcohol, late screens, stress) predict worse nights? The absolute number — especially a single-night value — should not be over-interpreted, should not be compared directly to clinical thresholds (which are derived from sleep-diary or PSG values, not from biased wearable estimates), and should never become a source of anxiety that itself disrupts sleep.

---

## Bibliography

[1]. American Academy of Sleep Medicine. *The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications*, Version 3. Darien, IL: AASM, 2023. https://aasm.org/clinical-resources/scoring-manual/ — tag: regulatory — tier: 1

[2]. Penzel T. Using the gold mine of sleep data recorded to increase our understanding of sleep. *Sleep*. 2024;47(7):zsae121. doi:10.1093/sleep/zsae121. PMID: 38776172 — tag: mechanism_review — tier: 2

[3]. de Zambotti M, Cellini N, Goldstone A, Colrain IM, Baker FC. Wearable sleep technology in clinical and research settings. *Med Sci Sports Exerc*. 2019;51(7):1538–1557. doi:10.1249/MSS.0000000000001947. PMID: 30789439 — tag: mechanism_review — tier: 2

[4]. Chinoy ED, Cuellar JA, Huwa KE, Jameson JT, Watson CH, Bessman SC, Hirsch DA, Cooper AD, Drummond SPA, Markwald RR. Performance of seven consumer sleep-tracking devices compared with polysomnography. *Sleep*. 2021;44(5):zsaa291. doi:10.1093/sleep/zsaa291. PMID: 33378539 — tag: cohort — tier: 2

[5]. Paquet J, Kawinska A, Carrier J. Wake detection capacity of actigraphy during sleep. *Sleep*. 2007;30(10):1362–1369. doi:10.1093/sleep/30.10.1362. PMID: 17969470 — tag: cohort — tier: 2

[6]. Lee XK, Chee NIYN, Ong JL, Teo TB, van Rijn E, Lo JC, Chee MWL. Validation of a consumer sleep wearable device with actigraphy and polysomnography in adolescents across sleep opportunity manipulations. *J Clin Sleep Med*. 2019;15(9):1337–1346. doi:10.5664/jcsm.7932. PMID: 31538605. Note: late-adolescent sample (ages 15–19); WASO overestimation ≤42 min; adult generalizability qualified. — tag: cohort — tier: 2

[7]. Danzig R, Wang M, Shah A, Trotti LM. The wrist is not the brain: estimation of sleep by clinical and consumer wearable actigraphy devices is impacted by multiple patient- and device-specific factors. *J Sleep Res*. 2020;29(1):e12926. doi:10.1111/jsr.12926. PMID: 31621129 — tag: cohort — tier: 2

[8]. Lee T, Cho Y, Cha KS, Jung J, Cho J, Kim H, Kim D, Hong J, Lee D, Keum M, Kushida CA, Yoon IY, Kim JW. Accuracy of 11 wearable, nearable, and airable consumer sleep trackers: prospective multicenter validation study. *JMIR mHealth uHealth*. 2023;11:e50983. doi:10.2196/50983. PMID: 37917155 — tag: cohort — tier: 2

[9]. de Zambotti M, Goldstein C, Cook J, Menghini L, Altini M, Cheng P, Robillard R. State of the science and recommendations for using wearable technology in sleep and circadian research. *Sleep*. 2024;47(4):zsad325. doi:10.1093/sleep/zsad325. PMID: 38149978. COI: de Zambotti lists affiliation with Lisa Health Inc. (digital health company). — tag: mechanism_review — tier: 2

[10]. Ohayon M, Wickwire EM, Hirshkowitz M, Albert SM, Avidan A, Daly FJ, Dauvilliers Y, Ferri R, Fung C, Gozal D, Hazen N, Krystal A, Lichstein K, Mallampalli M, Plazzi G, Rawding R, Scheer FA, Somers V, Vitiello MV. National Sleep Foundation's sleep quality recommendations: first report. *Sleep Health*. 2017;3(1):6–19. PMID: 28346153. DOI: 10.1016/j.sleh.2016.11.006 — tag: mechanism_review — tier: 1

[11]. Boulos MI, Jairam T, Kendzerska T, Im J, Mekhael A, Murray BJ. Normal polysomnography parameters in healthy adults: a systematic review and meta-analysis. *Lancet Respir Med*. 2019;7(6):533–543. PMID: 31006560. DOI: 10.1016/S2213-2600(19)30057-8 — tag: meta_analysis — tier: 1

[12]. Scullin MK, Bliwise DL. Sleep, cognition, and normal aging: integrating a half century of multidisciplinary research. *Perspect Psychol Sci*. 2015;10(1):97–137. PMID: 25620997. DOI: 10.1177/1745691614556680 — tag: mechanism_review — tier: 2

[13]. Wilckens KA, Habte RF, Dong Y, Stepan ME, Dessa KM, Whitehead AB, Peng CW, Fletcher ME, Buysse DJ. A pilot time-in-bed restriction intervention behaviorally enhances slow-wave activity in older adults. *Front Sleep*. 2024;2:1265006. DOI: 10.3389/frsle.2023.1265006 — tag: cohort — tier: 2

[14]. Altena E, Ellis J, Camart N, Guichard K, Bastien C. Mechanisms of cognitive behavioural therapy for insomnia. *J Sleep Res*. 2023;32(6):e13860. PMID: 36866434. DOI: 10.1111/jsr.13860 — tag: mechanism_review — tier: 2

[15]. Buysse DJ. Sleep health: can we define it? Does it matter? *Sleep*. 2014;37(1):9–17. PMID: 24470692. DOI: 10.5665/sleep.3298 — tag: mechanism_review — tier: 1

[16]. Stanyer EC, Skeldon AC, Kyle SD. Untangling the mechanisms of sleep restriction therapy. *Sleep*. 2026;49(4):zsaf406. PMID: 41416742. DOI: 10.1093/sleep/zsaf406 — tag: mechanism_review — tier: 2

[17]. Haghayegh S, Khoshnevis S, Smolensky MH, Diller KR, Castriotta RJ. Accuracy of wristband Fitbit models in assessing sleep: systematic review and meta-analysis. *J Med Internet Res*. 2019;21(11):e16273. PMID: 31778122. DOI: 10.2196/16273. No conflicts of interest declared. — tag: meta_analysis — tier: 2

[18]. de Zambotti M, Rosas L, Colrain IM, Baker FC. The sleep of the ring: comparison of the ŌURA sleep tracker against polysomnography. *Behav Sleep Med*. 2019;17(2):124–136. PMID: 28323455. DOI: 10.1080/15402002.2017.1300587. Note: sample mean age approximately 17 (adolescents and young adults); adult generalizability qualified. — tag: cohort — tier: 2

[19]. Svensson T, Madhawa K, Nt H, Chung U-I, Svensson AK. Validity and reliability of the Oura Ring Generation 3 (Gen3) with Oura sleep staging algorithm 2.0 (OSSA 2.0) when compared to multi-night ambulatory polysomnography: a validation study of 96 participants and 421,045 epochs. *Sleep Med*. 2024;115:251–263. PMID: 38382312. DOI: 10.1016/j.sleep.2024.01.020. Independent academic validation (University of Tokyo); not manufacturer-funded per disclosures. — tag: cohort — tier: 2

[20]. Robbins R, Weaver MD, Sullivan JP, et al. Accuracy of three commercial wearable devices for sleep tracking in healthy adults. *Sensors*. 2024;24(20):6532. DOI: 10.3390/s24206532 — tag: cohort — tier: 2

[21]. Imtiaz SA. A systematic review of sensing technologies for wearable sleep staging. *Sensors*. 2021;21(5):1562. DOI: 10.3390/s21051562 — tag: mechanism_review — tier: 2

[22]. Sateia MJ, Buysse DJ, Krystal AD, Neubauer DN, Heald JL. Clinical practice guideline for the pharmacologic treatment of chronic insomnia in adults: an American Academy of Sleep Medicine clinical practice guideline. *J Clin Sleep Med*. 2017;13(2):307–349. doi: 10.5664/jcsm.6470. PMID: 27998379 — tag: regulatory — tier: 1

[23]. Mander BA, Winer JR, Walker MP. Sleep and human aging. *Neuron*. 2017;94(1):19–36. doi: 10.1016/j.neuron.2017.02.004. PMID: 28384471 — tag: mechanism_review — tier: 2

[24]. Chan JK, Trinder J, Andrewes HE, Colrain IM, Nicholas CL. The acute effects of alcohol on sleep architecture in late adolescence. *Alcohol Clin Exp Res*. 2013;37(10):1720–1728. doi: 10.1111/acer.12141. PMID: 23800287. Note: late-adolescent sample (ages 18–21); adult corroboration from Ebrahim et al. [25, mechanism_review]. — tag: rct — tier: 2

[25]. Ebrahim IO, Shapiro CM, Williams AJ, Fenwick PB. Alcohol and sleep I: effects on normal sleep. *Alcohol Clin Exp Res*. 2013;37(4):539–549. doi: 10.1111/acer.12006. PMID: 23347102 — tag: mechanism_review — tier: 2

[26]. Punjabi NM. The epidemiology of adult obstructive sleep apnea. *Proc Am Thorac Soc*. 2008;5(2):136–143. doi: 10.1513/pats.200709-155MG. PMID: 18250205 — tag: cohort — tier: 2

[27]. Edinger JD, Arnedt JT, Bertisch SM, et al. Behavioral and psychological treatments for chronic insomnia disorder in adults: an American Academy of Sleep Medicine clinical practice guideline. *J Clin Sleep Med*. 2021;17(2):255–262. doi: 10.5664/jcsm.8986. PMID: 33164742 — tag: regulatory — tier: 1

[28]. Maurer LF, Schneider J, Miller CB, Espie CA, Kyle SD. The clinical effects of sleep restriction therapy for insomnia: a meta-analysis of randomised controlled trials. *Sleep Med Rev*. 2021;58:101493. doi: 10.1016/j.smrv.2021.101493. PMID: 33984745 — tag: meta_analysis — tier: 1

[29]. Schyvens A-M, Peters B, Van Oost NC, et al. A performance validation of six commercial wrist-worn wearable sleep-tracking devices for sleep stage scoring compared to polysomnography. *Sleep Adv*. 2025;6(2):zpaf021. doi: 10.1093/sleepadvances/zpaf021. PMID: 40303381 — tag: cohort — tier: 2

[30]. Baron KG, Abbott S, Jao N, Manalo N, Mullen R. Orthosomnia: are some patients taking the quantified self too far? *J Clin Sleep Med*. 2017;13(2):351–354. doi: 10.5664/jcsm.6472. PMID: 27855740 — tag: open_label — tier: 2
