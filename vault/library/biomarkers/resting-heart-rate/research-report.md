---
title: "Resting Heart Rate (RHR): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/resting-heart-rate/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.resting-heart-rate-design-work
provenance_slug: labs-specialist
source_count: 34
---

# Resting Heart Rate (RHR): Canonical Research Report

## Summary

Resting heart rate (RHR) is the number of cardiac contractions per minute when the body is fully at rest — no recent exertion, no acute emotional load, no thermoregulatory demand. Expressed in beats per minute (bpm), it is determined primarily by the autonomic nervous system's continuous modulation of the sinoatrial (SA) node's intrinsic ~100 bpm pacemaker rate, predominantly via parasympathetic (vagal) tone, which brakes the SA node toward the 50–80 bpm resting range typical of healthy adults. Aerobic fitness lowers RHR further by increasing stroke volume (requiring fewer beats per minute to maintain cardiac output) and, via intrinsic sinus-node remodeling involving downregulation of the HCN4 pacemaker channel, by reducing the pacemaker's own automaticity — a structural cardiac adaptation documented in animal models with supporting human data [6, animal; 1, mechanism_review].

RHR is a wearable-derived metric measured by consumer devices through photoplethysmography (PPG) during sleep or sedentary rest windows. Unlike heart rate variability (HRV), RHR has **both useful population norms and a sensitive personal-baseline-trend signal**, making it one of the more actionable wearable metrics. The conventional clinical normal range is 60–100 bpm [14, regulatory]; aerobically trained individuals commonly fall below 60 bpm, with endurance athletes sustaining 40–55 bpm — physiological sinus bradycardia, not pathology. In a prospective cohort of 465 endurance athletes (Pro@Heart), **38% had a minimum HR ≤40 bpm on Holter monitoring** [8, cohort]. An elevated RHR above your own rolling baseline flags under-recovery, early illness, alcohol exposure, or inadequate sleep before overt symptoms appear [11, cohort; 12, cohort; 2, cohort].

PPG-derived HR is accurate at rest, with mean absolute errors of approximately 2 bpm against ECG references under resting and sleep conditions [5, cohort]. The skin-tone disparity in PPG accuracy is most pronounced during exercise; at rest, differences across Fitzpatrick groups converge to approximately 2–3 bpm across devices [26, cohort]. Device definitions of "resting heart rate" differ across manufacturers and are not directly interchangeable [20, cohort].

Elevated RHR is robustly and dose-dependently associated with cardiovascular and all-cause mortality across large population cohorts — per 10 bpm increase, relative risk for all-cause mortality is approximately 1.09–1.17 [23, meta_analysis; 24, meta_analysis]. However, RHR is a **marker, not a confirmed modifiable target**: the SIGNIFY trial randomized 19,102 patients with stable coronary artery disease and elevated RHR to ivabradine (a selective HR-lowering agent) vs. placebo and found no reduction in cardiovascular death or MI despite effective heart rate lowering [25, rct]. The path to benefit runs through the aerobic training, sleep, and lifestyle changes that lower RHR for physiological reasons — not through pharmacological rate suppression.

---

## Physiology & What RHR Measures

### The Sinoatrial Node and Its Intrinsic Rate

The heart's rhythm originates at the **sinoatrial (SA) node**, a specialized cluster of pacemaker cells in the right atrium with intrinsic automaticity — they depolarize spontaneously without external neural input [1, mechanism_review]. Under complete pharmacological blockade of both sympathetic and parasympathetic branches (propranolol plus atropine to eliminate all autonomic influence), the human SA node fires at an intrinsic rate of roughly **90–100 bpm**, declining with age according to the approximation IHR ≈ 118 − (0.57 × age) [3, mechanism_review]. This intrinsic rate represents what the heart would do if the nervous system were entirely removed from the equation.

Resting heart rate is almost always substantially lower than this intrinsic rate. The gap is created by the autonomic nervous system.

### Autonomic Balance: Why Vagal Tone Dominates at Rest

Two branches of the autonomic nervous system converge on the SA node and continuously modulate its firing rate [1, mechanism_review]:

- **Parasympathetic (vagal) input** — the vagus nerve releases acetylcholine, binding M2 muscarinic receptors on SA-node cells. This hyperpolarizes the cell membrane, slows spontaneous depolarization, and increases time to each action potential — **negative chronotropy**.
- **Sympathetic input** — norepinephrine and epinephrine bind β1-adrenergic receptors, accelerating spontaneous depolarization and increasing firing rate — **positive chronotropy**.

At rest in healthy adults, parasympathetic tone is dominant [1, mechanism_review]. The vagus nerve exerts a continuous "brake" on the SA node, pulling heart rate from its ~100 bpm intrinsic baseline into the 50–80 bpm range typical of healthy resting adults. Higher vagal tone is a recognized index of cardiovascular health; in animal models, lower vagal tone is associated with elevated cardiovascular risk [4, animal] (rat model; relationship converges with human epidemiological data linking reduced HRV — a proxy for vagal tone — to adverse outcomes).

### Fitness and RHR: The Athlete's Bradycardia

A lower RHR generally reflects greater aerobic fitness, grounded mechanistically in **stroke volume**. Cardiac output (CO) = stroke volume (SV) × heart rate (HR). An endurance-trained heart generates a larger stroke volume at rest through structural left-ventricular remodeling — increased chamber volume and wall mass [9, cohort]. Each beat delivering more blood means fewer beats per minute are required for the same resting cardiac output. The result is physiologically low RHR.

Endurance athletes commonly exhibit resting heart rates of **40–55 bpm** — physiological sinus bradycardia [1, mechanism_review; 22, meta_analysis; 34, mechanism_review]. In highly trained athletes, rates below 40 bpm are common: in a prospective cohort of 465 endurance athletes (Pro@Heart), **38% had a minimum HR ≤40 bpm on Holter monitoring** [8, cohort].

Sustained endurance training does not lower RHR solely by increasing vagal tone. Animal studies demonstrate that training produces **intrinsic electrophysiological remodeling of the SA node itself** — specifically, downregulation of the HCN4 "funny current" channel (I_f) that drives spontaneous pacemaker depolarization [6, animal] (mouse model; mechanism extrapolated to humans with supporting autonomic-blockade data). Blocking I_f abolished the heart rate difference between trained and sedentary animals. These adaptations are intrinsic to the sinus node, persist after autonomic blockade, and are **reversible with detraining** — detraining restores normal HCN4 expression and resting heart rate within weeks. The practical implication: RHR reflects both the nervous system's influence on the heart and the heart's own structural-electrical state.

### Distinguishing RHR from Related Metrics

- **Maximum heart rate (HR_max)** — the highest achievable HR under maximal exertion. HR_max is largely determined by age (~220 − age as a rough estimate) and does not reflect fitness in the same direct way as RHR.
- **Heart rate reserve (HRR)** — HR_max minus RHR. Used to set exercise intensity targets (Karvonen formula: target HR = RHR + % × HRR). A lower RHR from fitness increases HRR, expanding the usable training range.

RHR is the metric most directly responsive to long-term aerobic training, day-to-day autonomic state, and chronic health changes.

### What Wearables Actually Measure

Consumer wearables derive heart rate from **photoplethysmography (PPG)** — a light-emitting diode (typically green, sometimes near-infrared) shines into the skin at the wrist, and a photodetector captures the fraction of reflected light [29, mechanism_review; 10, cohort]. As the heart beats, blood volume in the capillary bed rises and falls; this modulates light absorption, producing a pulsatile signal from which the algorithm extracts pulse rate. Chest-strap monitors use ECG-derived electrical detection of the R-wave — more accurate during motion because it measures the electrical event directly rather than its vascular consequence.

For **resting heart rate specifically**, PPG performance is strong. At rest, with minimal motion artifact and stable ambient light, wearable PPG devices achieve mean absolute errors of approximately **2 bpm** against ECG reference standards, with concordance classified as moderate to excellent [10, cohort]. This contrasts with the substantially larger errors seen during exercise, where motion artifact dominates. HR measurement at rest is fundamentally easier for PPG than HRV measurement — a single average beat rate is far less sensitive to timing noise than the precise beat-to-beat interval precision HRV requires.

---

## Interpretation, Norms & Personal Baseline

### Population Norms: What Do the Numbers Mean?

The conventional clinical definition of a normal resting heart rate is **60–100 bpm**, codified in guidelines including the 2018 ACC/AHA/HRS Guideline on Bradycardia and Cardiac Conduction Delay [14, regulatory]. This range was not derived from a single large population study — it reflects historical convention — and there is active debate about whether it should be revised [14, regulatory]. In practice, the 60–100 bpm frame serves as a first-pass clinical screen, not a sharp biological boundary.

Large wearable-device datasets confirm that healthy adult RHR spans a considerably wider individual range. In a retrospective cohort of **92,457 Fitbit users** tracked over a median of 320 days (~33 million daily measurements), individual average RHRs ranged from 39.7 to 108.6 bpm, with a population mean of 65.5 bpm [2, cohort]. This spread underscores why a single population cut-point is a coarse tool for evaluating any individual.

### Age and Sex Context

Women consistently average higher RHR than men across all age groups — typically **3–7 bpm higher** — a pattern confirmed in both large wearable cohorts and genetic studies [2, cohort; 15, cohort]. In the 92,457-person Fitbit dataset, the difference persisted at every age strata [2, cohort]. A 2026 longitudinal analysis from the Norwegian HUNT study found baseline RHR of **74 bpm in women vs. 70 bpm in men**, with each 10-bpm increase associated with a 15% higher heart failure risk in women and 9% in men [15, cohort]. The genetic basis for this sex gap is substantial: a 2024 EJPC Mendelian randomization study identified substantially more RHR-associated genetic loci in women (90) than in men (60), with limited overlap [16, cohort].

RHR also varies with age — rising through midlife, peaking around age 50 in most populations, then declining slightly — and with adiposity and sleep duration (the Quer et al. dataset found minimum RHR associated with 7–7.5 hours of sleep per night) [2, cohort].

### The "Lower Is Generally Better" Principle — With Critical Caveats

Within the physiological range, a lower resting heart rate tracks both better cardiovascular fitness and lower CV mortality risk. A pooled analysis of **112,680 participants across 12 cohort studies** in the Asia-Pacific region found a continuous, graded relationship: those with RHR >80 bpm had **54% higher all-cause mortality** and 44% higher cardiovascular mortality compared to those with RHR <65 bpm; the excess risk for heart failure reached 2.08-fold [13, cohort]. Critically, no protective effect was detected below the ~65 bpm threshold, suggesting the risk relationship is not simply linear through the bradycardic range.

### Physiological Bradycardia: Benign and Expected in Fit Individuals

A resting HR below 60 bpm — technically classified as sinus bradycardia — is **common, expected, and benign** in aerobically trained individuals. Endurance athletes frequently sustain RHRs of 40–55 bpm [34, mechanism_review]; in the Pro@Heart cohort of 465 endurance athletes, **38% had a minimum HR ≤40 bpm on Holter monitoring** [8, cohort]. This is not disease — it is the hallmark of the "athlete's heart." A 2026 Circulation analysis (D'Ambrosio et al.) confirmed that resting bradycardia (HR ≤40 bpm) and sinus pauses of 2–3 seconds in endurance athletes were well-tolerated and not associated with increased risk of adverse cardiovascular outcomes over 5.5 years of follow-up [8, cohort].

### Pathological Bradycardia: A Different Entity

Physiological athletic bradycardia must be distinguished from **pathological bradycardia** — due to sinus node disease, AV block, hypothyroidism, or drug effect (beta-blockers, certain antiarrhythmics, digoxin). The distinguishing features are:

- **Symptoms**: physiological bradycardia is asymptomatic at rest; pathological bradycardia may produce fatigue, pre-syncope, syncope, exercise intolerance, or dyspnea
- **Context**: athletic bradycardia develops in the setting of regular endurance training and reverses when training stops — detraining restores normal HCN4 expression and resting heart rate within weeks [6, animal]
- **Response to exercise**: physiological bradycardia appropriately accelerates with activity; failure to augment HR with exertion (chronotropic incompetence) is a red flag

The 2018 ACC/AHA/HRS Guideline makes clear that for sinus node dysfunction, **symptom-rhythm correlation is the key determinant of treatment** — no minimum HR or pause duration alone triggers a recommendation for pacing in asymptomatic individuals [14, regulatory]. Bradycardia that is symptomatic, unexplained, or arises in a non-athletic context warrants medical evaluation.

### Personal Baseline Trend: The Load-Bearing Wearable Signal

Population norms tell you where you fall on the population curve. The more actionable wearable signal for day-to-day health management is the **deviation from your own rolling baseline** — RHR is a sensitive, continuously available indicator of physiological stress state.

States that increase sympathetic drive or impair autonomic recovery transiently raise RHR:

- **Illness onset**: Acute infection drives systemic inflammation and elevated sympathetic tone, producing measurable RHR elevation — often before subjective symptom awareness. In a JMIR cohort study, wearable-measured RHR began rising above individual baselines **~2 days before ILI symptom onset**, peaked at day +1 (3.2 bpm above baseline in confirmed influenza), and took a median of 10 days to return to pre-illness levels [11, cohort]. The ILI-associated RHR signal was statistically significant from day −2 through day +6 relative to symptom onset.
- **Alcohol**: Even moderate alcohol consumption transiently elevates nocturnal RHR. A prospective observational study found nocturnal RHR rose from 63.6 bpm at baseline to 66.6 bpm after low-to-moderate drinking (p < 0.001), normalizing post-exposure — a physiological signal of impaired overnight recovery [12, cohort].
- **Poor sleep**: Sleep restriction and poor sleep quality are independently associated with higher RHR; the Quer et al. dataset found minimum average RHR in subjects sleeping 7–7.5 hours [2, cohort].
- **Heat and dehydration**: Environmental thermal load and volume depletion increase cardiac output demand at rest, raising steady-state RHR.
- **Psychological stress and overreaching**: Elevated sympathetic tone from stress, overtraining, or insufficient recovery produces above-baseline RHR that can persist for days [17, meta_analysis].

Because **intra-individual RHR is highly stable under stable conditions** (the Quer et al. dataset showed ~80% of subjects had weekly maximum RHR swings below 10 bpm, with median weekly change of ~3 bpm) [2, cohort], an elevation of 5+ bpm above one's rolling 7–14 day morning or nocturnal average is a meaningful signal worth acting on — even before symptoms appear.

RHR is notable in being one of the few wearable metrics for which **both population norms and personal-baseline deviation are independently actionable**: the absolute level informs fitness trajectory and CV risk, while the day-to-day deviation indicates acute recovery state and possible illness. HRV, by contrast, has such wide interindividual spread that population norms are largely uninformative and deviation from personal baseline is nearly the whole story.

### Measurement Consistency Requirements

RHR is sensitive to multiple confounders that make cross-session comparisons unreliable unless measurement conditions are standardized:

- **Time of day**: RHR follows circadian rhythm — lowest in early morning, higher mid-afternoon. Comparing a morning reading to an afternoon reading can yield apparent "elevations" of 5–10 bpm reflecting circadian physiology, not a meaningful change [5, cohort].
- **Posture**: Supine RHR is lower than seated, which is lower than standing (orthostatic HR response). Consumer wearables measuring during sleep get a relatively posture-stable nocturnal estimate.
- **Recent activity, caffeine, food**: Any activity within 10–15 minutes, caffeine intake, or a large meal will transiently elevate HR.
- **Device consistency**: Between-device variability is substantial; mixing devices mid-tracking breaks personal baseline continuity [5, cohort]. Oura Gen 3/4 rings showed concordance coefficients of 0.97–0.98 against ECG for nocturnal RHR in a 536-night validation study [5, cohort].

Practical standard: for personal-baseline tracking, use nocturnal or morning RHR from the same device in a lying/resting state, at the same relative time each day. A 7-day rolling average smooths day-to-day noise. Flag deviations ≥5 bpm above the rolling average as a recovery or health signal worth noting.

---

## Measurement & Device Validity

### PPG vs. ECG: The Physics of Wrist-Based Heart Rate

Consumer wearables derive heart rate through **photoplethysmography (PPG)** — LEDs (typically green, sometimes red or infrared) illuminate the skin at the wrist, and a photodetector measures the pulse of reflected light varying with blood-volume changes in the capillaries. This is fundamentally different from **electrocardiography (ECG)**, which records the electrical impulse triggering each cardiac contraction and is the clinical gold standard for heart rate and rhythm.

The key practical implication: **at rest and during sleep, wrist PPG-derived heart rate is highly accurate**. A 2024 daily-life validation study compared PPG devices against ambulatory ECG in 25 healthy volunteers across 10 days and found heart rate mean absolute error under 1 bpm during sleep, with Spearman correlations of 0.96–0.98 across the full day [18, cohort]. Note: all authors of that study are Janssen R&D employees (COI); the accuracy findings are consistent with the broader independent literature.

**Accuracy degrades substantially with movement and rising heart rate.** The Rehman et al. study found walking increased HR error approximately 10% over non-walking conditions [18, cohort]. A 2025 device-validation study found wrist-worn devices showed MAE of 6.41 bpm versus 1.43 bpm for an arm-worn sensor, with the wrist device's within-subject coefficient of variation rising to 23.03% during postural transitions [19, cohort]. The Bent et al. analysis of 53 participants across six Fitzpatrick skin-tone categories found that mean absolute error during physical activity averaged 30% higher than at rest, and that rhythmic, repetitive movements caused devices to misidentify the periodic motion signal as heart rate [10, cohort]. A 2019 real-world intraindividual validation study (Apple Watch Series 3 and Fitbit Charge 2 vs. ambulatory ECG; single-participant design, findings illustrative not population-generalizable) found at sleep MAPE was 3.1–3.4%; during running it rose to 3.0–9.9%; during general activities of daily living it reached 9.2–13.7% [28, cohort]. A 2022 systematic review of 9 studies across 15 devices from 7 brands found Apple Watch MAPE for heart rate ranged 1–7%, while Fitbit devices ranged 2.4–17% depending on activity [7, mechanism_review].

The practical summary: **for resting-HR, wrist PPG is fit for purpose** — real-world MAE at rest or during sleep is consistently in the 1–5 bpm range across modern devices, adequate for trend tracking, cardiovascular fitness monitoring, and lifestyle applications. It is not a diagnostic instrument, and accuracy degrades meaningfully during exercise.

### Skin Tone, Perfusion, Wrist Fit, and Artifact Sources

**Skin tone** is the most clinically important equity concern. Melanin, concentrated in the epidermis, preferentially absorbs green light — the wavelength used by most wrist PPG sensors — which reduces signal amplitude in darker skin tones. A 2025 prospective study of Fitbit Charge 5 vs. Polar H10 reference across three skin-tone groups found no significant between-group difference at rest (~2.8 bpm across all groups), but substantial divergence during exercise: at moderate-to-high intensity, dark skin-tone participants showed mean errors of 14.6–16.5 bpm versus 4 bpm in the light skin-tone group — a fourfold disparity [26, cohort]. A 2025 cross-sectional study of Garmin Forerunner 45 found no statistically significant main effect of Fitzpatrick score on resting or steady-state accuracy, but noted higher PPG readings in darker skin tones during exercise intensity ramps [30, cohort]. A 2022 systematic review of 10 studies (469 participants) found that 4 of 10 reported a statistically significant reduction in heart rate accuracy in darker skin tones, 4 found no significant difference, and 2 showed mixed results — reflecting genuine heterogeneity in study design and activity conditions [27, mechanism_review].

**For resting-HR specifically**, the skin-tone effect is smallest: the Hung et al. data shows convergence at rest. The disparity is most clinically relevant during exercise-derived metrics; however, given that some device RHR algorithms sample brief daytime resting windows rather than solely nocturnal data, the skin-tone interaction warrants disclosure.

Other documented accuracy factors: **tattoos** over the measurement site reduce signal amplitude by absorbing or scattering LED light; **perfusion state** (cold hands, vasoconstriction, low blood pressure) reduces optical pulse amplitude and increases noise; **wrist fit** (band tightness and position relative to the ulnar artery) affects coupling quality.

### The Resting-HR Definition Problem: Cross-Device Non-Interchangeability

Consumer devices do not agree on what "resting heart rate" means, and the derived metric is not directly interchangeable across devices or even across firmware versions.

Documented proprietary approaches include:

- **Garmin**: lowest 30-minute moving average within a 24-hour period
- **Oura**: continuous overnight average from 10-minute segments throughout sleep
- **WHOOP**: nightly calculation weighted toward slow-wave sleep readings
- **Polar**: restricted to the first four hours post-sleep-onset
- **Apple and Samsung**: HR sampled every 5 minutes during rest periods

A 2023 analysis of wrist-worn device RHR computations in over 92,000 participants documented mean RHR values ranging from 40–109 bpm across devices, with nighttime values averaging 4 bpm lower than daytime values in the same individuals [20, cohort]. COI: all authors are Google/Alphabet employees with stock options; study funded by Google. Heart rate stabilized within ~4 minutes of inactivity in most participants, and over 53% of daily HR minima occurred between 03:00–07:00 — meaning nocturnal and daytime algorithms capture systematically different physiological windows.

A 2024 validation study of the Verily Study Watch against simultaneous ECG in 875 participants found ICC = 0.946 and mean bias of 0.76 bpm for PPG-derived RHR when the algorithm excluded motion-artifact intervals using actigraphy [31, cohort]. COI: multiple authors hold Verily employment and equity; study funded by Verily Life Sciences.

Validation data show that Oura (ring form factor, worn on the finger with a shorter optical path through tissue) achieves the highest nocturnal RHR accuracy (concordance correlation coefficient 0.97–0.98, mean absolute percentage error ~1.7–1.9%), outperforming wrist-worn devices in head-to-head nocturnal comparisons [5, cohort]. A person who owns both a Garmin and an Oura will routinely see different "resting HR" numbers even on the same night, not because one is wrong, but because they are measuring different things under the same label. **Values from different devices are not directly interchangeable.** Trending within a single device is meaningful; cross-device comparisons require caution.

### Wellness Device vs. Medical Device: Regulatory and Clinical Scope

The majority of consumer wrist PPG devices marketed for resting-HR monitoring are **general wellness products** under FDA guidance — not cleared medical devices. Accuracy claims are not subject to mandatory FDA premarket review; published accuracy data comes from independent researchers rather than regulatory submissions.

A subset of consumer devices have received **FDA De Novo clearance or 510(k) clearance** for specific medical-grade features. The Apple Watch ECG app received De Novo clearance in 2018 for single-lead ECG recording and AF/sinus-rhythm classification; KardiaMobile received 510(k) clearance for single-lead ECG. A 2025 validation study of four consumer AF-detection wearables found sensitivity of 100% and specificity of 96.4–98.9% for AF detection, with 7.4–14.8% of readings requiring re-attempts due to insufficient signal quality [21, cohort].

These FDA-cleared features are specifically for rhythm classification (AF vs. sinus), not for continuous resting-HR accuracy. The general continuous PPG heart rate function remains a wellness feature. FDA clearance of an ECG feature does not validate the device's PPG-derived resting-HR accuracy.

**Reproducibility and test-retest:** device algorithms apply proprietary artifact rejection, smoothing, and coverage thresholds, so between-session reproducibility is hardware- and algorithm-specific. The Rehman et al. study noted median PPG coverage of 44–52% over full waking days versus 77–88% during sleep — meaning on many days, a substantial fraction of the waking-day HR record is discarded by the algorithm, and the final RHR scalar represents a non-random sample of the day [18, cohort]. This selective coverage is rarely disclosed to the end user and can affect day-to-day reproducibility independently of true physiological change.

---

## Determinants & Significance

### What Raises Resting Heart Rate

RHR is exquisitely sensitive to a wide range of short- and long-term inputs, making it a composite read-out of physiological state rather than a fixed trait.

**Acute and day-to-day elevators.** Physical and psychological stress activate the sympathoadrenal axis, raising RHR within minutes via catecholamine release and vagal withdrawal. Illness and infection are among the most reliable acute elevators: inflammatory cascade, fever, and increased metabolic demand all drive heart rate up, and this elevation typically precedes or accompanies early symptoms. Mishra et al. analyzed smartwatch data from 5,262 participants and found that among 32 confirmed COVID-19 cases, 81% showed abnormal physiological signals; of the 25 cases with symptom-timing information available, **22 were detected at or before symptom onset, with 4 cases detectable at least 9 days before symptoms**, primarily through resting-heart-rate algorithms [33, cohort].

Alcohol produces a reproducible, dose-related acute overnight RHR elevation. Strüven et al. (2025) ran a 9-day prospective smartwatch study in 40 healthy adults: nocturnal RHR rose from 63.6 ± 9.2 bpm at baseline to 66.6 ± 9.0 bpm during three consecutive alcohol-exposure days (40 g/day women, 60 g/day men), with rapid normalization post-exposure (p < 0.001); objective sleep architecture was unchanged even as subjective sleep quality fell, suggesting the elevated heart rate independently impairs overnight recovery [12, cohort].

High training load, overtraining, and under-recovery raise morning RHR relative to personal baseline. An acutely elevated morning RHR vs. the prior rolling average is one of the oldest and most validated athlete monitoring signals for under-recovery or accumulated fatigue [17, meta_analysis].

Additional elevators: poor or short sleep, caffeine and stimulants (sympathomimetic; most pronounced in non-habituated individuals), nicotine, dehydration, elevated ambient temperature and heat stress, deconditioning, pregnancy, stimulant medications, and pathological states including hyperthyroidism, anemia, fever from any cause, and cardiac arrhythmias. Some antidepressants and bronchodilators raise RHR pharmacologically.

**Clinical thresholds.** Resting tachycardia is conventionally defined as >100 bpm at rest; resting bradycardia as <60 bpm — though neither threshold alone defines pathology without clinical context.

### What Lowers Resting Heart Rate

**Aerobic and endurance training is the dominant chronic determinant.** Regular aerobic exercise produces training-induced resting bradycardia, one of the best-established exercise adaptations. The mechanism was long attributed primarily to enhanced vagal tone; current evidence has substantially revised that framing. D'Souza et al. (2014, Nature Communications) demonstrated in mouse models (with supporting human data) that exercise training produces widespread remodeling of sinus node pacemaker ion channels — notably downregulation of the HCN4 channel and its corresponding funny current (I_f). Blocking I_f abolished the heart rate difference between trained and sedentary animals. These adaptations are intrinsic to the sinus node, persist after autonomic blockade, and reverse with detraining, establishing a structural cardiac remodeling mechanism that operates independently of, and in parallel with, autonomic changes (mouse model; mechanism extrapolated to humans) [6, animal]. Endurance athletes can reach resting values of 35–50 bpm; an RHR in this range in a fit individual is a physiological signature of cardiac efficiency, not pathology.

**Additional lowering factors.** Adequate recovery and high-quality sleep restore vagal tone acutely. High chronic vagal tone (HRV-correlated) tracks with lower resting rates. Beta-blockers pharmacologically lower RHR by blocking sympathetic beta-1 receptor activation at the sinus node — a key point relevant to the marker-vs-target debate below.

**Athletic bradycardia vs. pathological bradycardia.** D'Ambrosio et al. confirmed that athlete bradycardia typically reflects benign sinus bradycardia from cardiac remodeling; pathological causes (sinus node dysfunction, complete heart block, sick sinus syndrome) require clinical evaluation when accompanied by symptoms, syncope, or hemodynamic compromise [8, cohort]. An RHR of 42 bpm in an asymptomatic marathon runner is not the same clinical entity as an RHR of 42 bpm in a sedentary 65-year-old with syncope.

### Significance

#### 1. Prognostic: Elevated RHR and Mortality

Elevated resting heart rate is one of the most reproducible cardiovascular epidemiological findings across population cohorts spanning multiple continents. Two large meta-analyses characterize the dose-dependent association:

Zhang, Shen, and Qi (2016, CMAJ) pooled 46 prospective cohort studies in **1,246,203 individuals** with 78,349 deaths. Per 10 bpm increase in resting heart rate, relative risk for all-cause mortality was **1.09 (95% CI 1.07–1.12)** and for cardiovascular mortality **1.08 (95% CI 1.06–1.10)**. An RHR >80 bpm vs. <60 bpm carried RR 1.45 (95% CI 1.34–1.57) for all-cause mortality [23, meta_analysis].

Aune et al. (2017, Nutrition Metabolism Cardiovascular Diseases) extended this across **87 prospective studies**. Per 10 bpm increase, summary relative risk was **1.17 (95% CI 1.14–1.19)** for all-cause mortality, **1.15 (95% CI 1.11–1.18)** for cardiovascular disease, 1.07 for coronary heart disease, 1.18 for heart failure, and 1.09 for sudden cardiac death. A clear positive dose-response relationship was present across all outcomes [24, meta_analysis].

The Framingham Heart Study demonstrated that resting heart rate is independently associated with incident cardiovascular events, with graded risk across the normal range [32, cohort].

These associations are biologically plausible: elevated sympathetic tone and reduced parasympathetic tone increase myocardial oxygen demand, reduce diastolic coronary perfusion time, and are mechanistically linked to adverse cardiac remodeling, hypertension, and insulin resistance.

#### Marker, Not a Confirmed Modifiable Target

The mortality-RHR associations are observational and highly consistent, with dose-response grading consistent with causality. However, the critical test of whether pharmacologically lowering RHR improves outcomes was run and failed: the **SIGNIFY trial** (Fox et al., 2014, NEJM) randomized **19,102 patients** with stable coronary artery disease, elevated RHR (≥70 bpm), but without clinical heart failure to ivabradine vs. placebo. Ivabradine selectively reduces RHR via I_f inhibition without other hemodynamic effects. Despite effective heart rate lowering, the primary endpoint — composite of cardiovascular death or nonfatal MI — showed **hazard ratio 1.08 (95% CI 0.96–1.20, P = 0.20)** with no benefit, and a significant signal toward harm in patients with higher-grade angina [25, rct]. This is the clearest evidence that pharmacologically lowering an elevated RHR in stable CAD does not translate to the outcome benefit that the epidemiological marker association predicts.

(Note: RHR lowering does improve outcomes in heart failure with reduced ejection fraction — a different clinical context where elevated RHR is part of the pathophysiology, not just a marker.)

The practical implication: the path to benefit from a lower RHR runs primarily through lifestyle and fitness changes that lower it for physiological reasons — aerobic training, improved sleep, stress reduction, reduced alcohol — not through pharmacological rate suppression.

#### 2. Training and Recovery Monitoring

Morning or nocturnal RHR relative to a personal rolling baseline is the most established wearable application for this metric. An acute elevation of 5–7 bpm above a stable personal mean is a well-recognized signal for under-recovery, high accumulated training load, or early illness in athletic populations — validated as a practical component of load management frameworks [17, meta_analysis]. The illness-detection work from COVID-19 wearable cohorts has extended this into general populations, with individual-referenced RHR algorithms outperforming population-referenced thresholds for early illness flagging [33, cohort].

#### 3. Resting Tachycardia and Bradycardia Thresholds

Sustained resting tachycardia (>100 bpm) warrants clinical evaluation for reversible causes (dehydration, anemia, hyperthyroidism, anxiety, arrhythmia, stimulant use) before attributing to deconditioning. Bradycardia (<60 bpm) in a sedentary, asymptomatic individual without training history requires ECG and clinical context, particularly if symptomatic.

### Limitations

**Confounding.** RHR measured outside of controlled conditions is heavily confounded by caffeine timing, stress, body position (standing vs. supine: ~10–15 bpm difference), recent physical activity, ambient temperature, hydration status, time of day, and autonomic state. Even in clinical settings, a single spot measurement carries substantial within-person variability.

**Device definition heterogeneity.** Consumer devices compute "resting heart rate" using proprietary algorithms — typically the lowest overnight PPG readings, sometimes a daytime low-activity window. These definitions differ across manufacturers, making cross-device comparisons of absolute values unreliable. Trend monitoring within a single device is more meaningful than comparing an absolute value against population references from different measurement conditions.

**Marker-vs-target.** The mortality association is observational and consistent, but the SIGNIFY trial evidence shows that the marker is not straightforwardly a causal target in stable CAD without heart failure. Fitness-based RHR lowering may carry benefit through correlated improvements in fitness, autonomic balance, and metabolic health — the RHR reduction itself may not be the active ingredient.

**Consumer RHR is a wellness and trend metric.** Wearable RHR is accurate for heart rate as a quantity but should be interpreted as a longitudinal trend relative to personal baseline, not as a single-reading diagnostic. Individual variation of ±3–5 bpm day-to-day is normal; single readings should not drive clinical decisions.

**Athletic bradycardia ≠ pathological bradycardia.** An RHR below 50 bpm in a trained athlete is a different clinical entity from the same number in a sedentary or symptomatic individual. Context — training history, symptom status, ECG rhythm — determines significance.

---

## Bibliography

[1]. MacDonald EA, Rose RA, Quinn TA. Neurohumoral Control of Sinoatrial Node Activity and Heart Rate: Insight From Experimental Models and Findings From Humans. *Frontiers in Physiology*. 2020;11:170. doi:10.3389/fphys.2020.00170 — tag: mechanism_review — tier: 2

[2]. Quer G, Gouda P, Galarnyk M, et al. Inter- and intraindividual variability in daily resting heart rate and its associations with age, sex, sleep, BMI, and time of year: retrospective, longitudinal cohort study of 92,457 adults. *PLoS One*. 2020;15(2):e0227709. PMID:32023264. doi:10.1371/journal.pone.0227709 — tag: cohort — tier: 2

[3]. Opthof T. The normal range and determinants of the intrinsic heart rate in man. *Cardiovascular Research*. 2000;45(1):177–184. doi:10.1016/S0008-6363(99)00322-3 — tag: mechanism_review — tier: 2

[4]. Carnevali L, Sgoifo A. Vagal modulation of resting heart rate in rats: the role of stress, psychosocial factors, and physical exercise. *Frontiers in Physiology*. 2014;5:118. doi:10.3389/fphys.2014.00118 — tag: animal — tier: 2

[5]. Dial MB, Hollander ME, Vatne EA, et al. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. *Physiological Reports*. 2025;13:e70527. PMID:40834291. doi:10.14814/phy2.70527 — tag: cohort — tier: 2

[6]. D'Souza A, Bucchi A, Johnsen AB, et al. Exercise training reduces resting heart rate via downregulation of the funny channel HCN4. *Nature Communications*. 2014;5:3775. PMID:24825544. doi:10.1038/ncomms4775 — tag: animal — tier: 2

[7]. Germini F, Noronha N, Borg Debono V, et al. Accuracy and Acceptability of Wrist-Wearable Activity-Tracking Devices: Systematic Review of the Literature. *Journal of Medical Internet Research*. 2022;24(1):e30791. PMID:35060915. doi:10.2196/30791. COI: none declared. — tag: mechanism_review — tier: 2

[8]. D'Ambrosio P, De Paepe J, Spencer LW, Ohanian M, Janssens K, et al.; Pro@Heart Consortium. Bradycardia in athletes: prevalence, mechanisms, and risks. *Circulation*. 2026;153(9):616–630. PMID:41410046. doi:10.1161/CIRCULATIONAHA.125.076170 — tag: cohort — tier: 1

[9]. Letnes JM, Nes BM, Sandbakk Ø, et al. Comparison of resting heart rate and left ventricular ejection fraction in elite endurance athletes and the general population. *European Journal of Preventive Cardiology*. 2024. doi:10.1093/eurjpc/zwae294 — tag: cohort — tier: 2

[10]. Bent B, Goldstein BA, Kibbe WA, Dunn JP. Investigating sources of inaccuracy in wearable optical heart rate sensors. *NPJ Digital Medicine*. 2020;3:18. PMID:32047863. doi:10.1038/s41746-020-0226-6. COI: none declared. — tag: cohort — tier: 2

[11]. Hunter V, Shapiro A, Chawla D, et al. Characterization of influenza-like illness burden using commercial wearable sensor data and patient-reported outcomes: mixed methods cohort study. *Journal of Medical Internet Research*. 2023;25:e41050. PMID:36951890. doi:10.2196/41050 — tag: cohort — tier: 2

[12]. Strüven A, Schlichtiger J, Hoppe JM, et al. The impact of alcohol on sleep physiology: a prospective observational study on nocturnal resting heart rate using smartwatch technology. *Nutrients*. 2025;17(9):1470. PMID:40362779. doi:10.3390/nu17091470 — tag: cohort — tier: 2

[13]. Woodward M, Webster R, Murakami Y, et al. The association between resting heart rate, cardiovascular disease and mortality: evidence from 112,680 men and women in 12 cohorts. *European Journal of Preventive Cardiology*. 2014;21(6):719–726. PMID:22718796. doi:10.1177/2047487312452501 — tag: cohort — tier: 1

[14]. Kusumoto FM, Schoenfeld MH, Barrett C, et al. 2018 ACC/AHA/HRS guideline on the evaluation and management of patients with bradycardia and cardiac conduction delay. *Heart Rhythm*. 2019;16(9):e128–e226. PMID:30412778. doi:10.1016/j.hrthm.2018.10.037 — tag: regulatory — tier: 1

[15]. Hansen LMS, Jui SSH, Braaten T, et al. Sex-specific longitudinal changes in resting heart rate and all-cause heart failure: insights from the HUNT study. *Frontiers in Cardiovascular Medicine*. 2026. doi:10.3389/fcvm.2026.1752910 — tag: cohort — tier: 2

[16]. Nordeidet AN, Klevjer M, Øvretveit K, et al. Sex-specific and polygenic effects underlying resting heart rate and associated risk of cardiovascular disease. *European Journal of Preventive Cardiology*. 2024;31(13):1585–1594. PMID:38437179. doi:10.1093/eurjpc/zwae092 — tag: cohort — tier: 2

[17]. Bellenger CR, Fuller JT, Thomson RL, Davison K, Robertson EY, Buckley JD. Monitoring athletic training status through autonomic heart rate regulation: a systematic review and meta-analysis. *Sports Medicine*. 2016;46(10):1461–1486. PMID:26888648. doi:10.1007/s40279-016-0484-2 — tag: meta_analysis — tier: 2

[18]. Rehman RZU, Chatterjee M, Manyakov NV, et al. Assessment of Physiological Signals from Photoplethysmography Sensors Compared to an Electrocardiogram Sensor: A Validation Study in Daily Life. *Sensors (Basel)*. 2024;24(21):6826. PMID:39517723. doi:10.3390/s24216826. COI: all authors employed by Janssen Research & Development. — tag: cohort — tier: 3

[19]. Schweizer T, Gilgen-Ammann R. Wrist-Worn and Arm-Worn Wearables for Monitoring Heart Rate During Sedentary and Light-to-Vigorous Physical Activities: Device Validation Study. *JMIR Cardio*. 2025;9:e67110. PMID:40116771. doi:10.2196/67110. COI: none declared. — tag: cohort — tier: 3

[20]. Speed C, Arneil T, Harle R, Wilson A, Karthikesalingam A, McConnell M, Phillips J. Measure by measure: Resting heart rate across the 24-hour cycle. *PLOS Digital Health*. 2023;2(4):e0000236. PMID:37115739. doi:10.1371/journal.pdig.0000236. COI: all authors are Google/Alphabet employees with stock options; study funded by Google. — tag: cohort — tier: 3

[21]. Wouters F, Gruwez H, Smeets C, et al. Comparative Evaluation of Consumer Wearable Devices for Atrial Fibrillation Detection: Validation Study. *JMIR Formative Research*. 2025;9:e65139. PMID:39791483. doi:10.2196/65139. COI: none declared; FibriCheck device provided by Qompium NV. — tag: cohort — tier: 3

[22]. Reimers AK, Knapp G, Reimers CD. Effects of exercise on the resting heart rate: a systematic review and meta-analysis of interventional studies. *Journal of Clinical Medicine*. 2018;7(12):503. PMID:30513777. doi:10.3390/jcm7120503 — tag: meta_analysis — tier: 1

[23]. Zhang D, Shen X, Qi X. Resting heart rate and all-cause and cardiovascular mortality in the general population: a meta-analysis. *CMAJ*. 2016;188(3):E53–E63. PMID:26598376. doi:10.1503/cmaj.150535 — tag: meta_analysis — tier: 1

[24]. Aune D, Sen A, Ó'Hartaigh B, et al. Resting heart rate and the risk of cardiovascular disease, total cancer, and all-cause mortality — a systematic review and dose-response meta-analysis of prospective studies. *Nutrition, Metabolism and Cardiovascular Diseases*. 2017;27(6):504–517. PMID:28552551. doi:10.1016/j.numecd.2017.04.004 — tag: meta_analysis — tier: 1

[25]. Fox K, Ford I, Steg PG, Tardif JC, Tendera M, Ferrari R; SIGNIFY Investigators. Ivabradine in stable coronary artery disease without clinical heart failure. *New England Journal of Medicine*. 2014;371(12):1091–1099. PMID:25176136. doi:10.1056/NEJMoa1406430 — tag: rct — tier: 1

[26]. Hung SH, Serwa K, Rosenthal G, Eng JJ. Validity of heart rate measurements in wrist-based monitors across skin tones during exercise. *PLoS One*. 2025;20(2):e0318724. PMID:39928630. doi:10.1371/journal.pone.0318724. COI: none declared; funded by Canada Research Chairs Program and CIHR. — tag: cohort — tier: 3

[27]. Koerber D, Khan S, Shamsheri T, Kirubarajan A, Mehta S. Accuracy of Heart Rate Measurement with Wrist-Worn Wearable Devices in Various Skin Tones: a Systematic Review. *Journal of Racial and Ethnic Health Disparities*. 2022 Nov 14. PMID:36376641. doi:10.1007/s40615-022-01446-9. COI: none declared. — tag: mechanism_review — tier: 2

[28]. Nelson BW, Allen NB. Accuracy of Consumer Wearable Heart Rate Measurement During an Ecologically Valid 24-Hour Period: Intraindividual Validation Study. *JMIR mHealth and uHealth*. 2019;7(3):e10828. PMID:30855232. doi:10.2196/10828. COI: none declared. Note: single-participant intraindividual design; findings are illustrative, not population-generalizable. — tag: cohort — tier: 3

[29]. Charlton PH, Kyriacou PA, Mant J, et al. Wearable Photoplethysmography for Cardiovascular Monitoring. *Proceedings of the IEEE*. 2022. PMID:35356509. doi:10.1109/JPROC.2022.3149785 — tag: mechanism_review — tier: 2

[30]. Icenhower E, Murphy C, Brooks J, Irby T, N'dah J, Robison C, Fanning J. Investigating the accuracy of Garmin PPG sensors on differing skin types based on the Fitzpatrick scale: cross-sectional comparison study. *Frontiers in Digital Health*. 2025. doi:10.3389/fdgth.2025.1553565. COI: none declared; partial support from Wake Forest University Claude D. Pepper Older Americans Independence Center (P30-AG21332). — tag: cohort — tier: 3

[31]. Feng KY, Short SA, Saeb S, et al. Resting Heart Rate and Associations With Clinical Measures From the Project Baseline Health Study: Observational Study. *Journal of Medical Internet Research*. 2024;26:e60493. PMID:39705694. doi:10.2196/60493. COI: multiple authors hold Verily employment and equity; study funded by Verily Life Sciences. — tag: cohort — tier: 3

[32]. Ho JE, Larson MG, Ghorbani A, et al. Long-term cardiovascular risks associated with an elevated heart rate: the Framingham Heart Study. *Journal of the American Heart Association*. 2014;3(3):e000668. PMID:24811610. doi:10.1161/JAHA.113.000668 — tag: cohort — tier: 2

[33]. Mishra T, Wang M, Metwally AA, et al. Pre-symptomatic detection of COVID-19 from smartwatch data. *Nature Biomedical Engineering*. 2020;4(12):1208–1220. PMID:33208926. doi:10.1038/s41551-020-00640-6 — tag: cohort — tier: 2

[34]. Jamieson A, Chico TJA, Jones S, et al. A guide to consumer-grade wearables in cardiovascular clinical care and population health for non-experts. *NPJ Cardiovascular Health*. 2025. PMID:40909206. doi:10.1038/s44325-025-00082-6 — tag: mechanism_review — tier: 2
