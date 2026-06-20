---
title: "Respiratory Rate (RR): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/respiratory-rate/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.respiratory-rate-design-work
provenance_slug: labs-specialist
source_count: 32
---

# Respiratory Rate (RR): Canonical Research Report

## Summary

Respiratory rate (RR) is the count of complete breathing cycles — one inhalation plus one exhalation — per minute, expressed in **breaths per minute (breaths/min, brpm)**. It is one of the four classic vital signs and is controlled by a distributed brainstem network: the pre-Bötzinger complex (preBötC) in the ventrolateral medulla generates the inspiratory rhythm; the parafacial respiratory group / retrotrapezoid nucleus (pFRG/RTN) couples CO₂ and pH sensing to the rhythm generator; and pontine nuclei (Kölliker-Fuse, parabrachial complex) shape the inspiratory off-switch and breathing pattern. CO₂/pH is the dominant chemical drive; the hypoxic drive via peripheral carotid-body chemoreceptors is a reserve mechanism.

Consumer wearables (Oura Ring, Fitbit, Apple Watch, WHOOP, Garmin) do not directly count breaths. They **derive RR from photoplethysmography (PPG) respiratory modulation** during sleep — extracting one or more of three overlapping signals locked to the breathing cycle: respiratory sinus arrhythmia (RSA/frequency modulation), amplitude modulation of PPG pulse height, and baseline-wander. Algorithms fuse these channels and restrict output to the overnight sleep window, reporting a **single nightly average**. The result is an estimate of resting nocturnal ventilatory rate, not a measure of tidal volume, minute ventilation, or airflow. At rest and under low-motion conditions, PPG-derived RR achieves mean absolute error (MAE) below 1 brpm against polysomnography (PSG) in multiple validated studies, though accuracy degrades substantially with motion, irregular breathing, and severe obstructive sleep apnea.

The normal adult resting range is **12–20 breaths/min**, operationalized in the UK National Early Warning Score 2 (NEWS2) and confirmed by large population datasets (Fitbit cohort mean 15.4 brpm, KORA cohort median 15.80 brpm). Tachypnea is flagged clinically at >20–24 brpm; bradypnea at <12 brpm. Pediatric rates are substantially higher and decline steeply through early life toward adult norms in mid-adolescence.

A defining feature of RR in the wearable context is **remarkable within-person nocturnal stability**. Natarajan et al. [2, cohort] found within-person CV of only 2.3–9.5% in younger adults (ages 20–24) across 14-day monitoring windows. Toften et al. [12, cohort] found nightly Bland-Altman limits of agreement of −0.07 to −0.04 brpm across 3 months of healthy-adult monitoring. This tight personal baseline means a rise of even 1–3 brpm above an individual's own rolling average is physiologically meaningful — a sensitivity that broad population norms would mask. Among all wearable-derived metrics, nocturnal RR is among the most reliable early-illness signals: the TemPredict/Oura study detected COVID-19 a mean of 2.75 days before symptom onset using a multi-signal algorithm (AUC 0.819, sensitivity 82%), with RR as a constituent feature [14, cohort].

RR is also an underused but powerful deterioration vital sign in hospital settings. It is the most heavily weighted single parameter in NEWS2, independently predicts cardiopulmonary arrest at OR 5.56 [20, cohort], and is associated with 21% in-hospital mortality at rates of 25–29 brpm [23, cohort] — yet it remains the least reliably measured and charted vital sign in clinical practice [21, mechanism_review; 22, mechanism_review]. On the other side, opioids and sedatives lower RR via brainstem μ-receptor suppression; in the PRODIGY trial, 46% of general-care-floor patients on parenteral opioids experienced opioid-induced respiratory depression (OIRD) episodes, and high-risk patients had OR 6.07 for OIRD compared with low-risk patients [17, cohort].

RR values are always expressed in **breaths/min**. Wearable nocturnal RR is a wellness and trend metric, not a diagnostic measurement; it does not capture tidal volume, minute ventilation, or apnea events, and should not substitute for bedside clinical counting in any clinical context.

---

## What Respiratory Rate Is & What the Device Measures

### Definition and Units

**Respiratory rate (RR)** is the number of complete breathing cycles — one inhalation plus one exhalation — completed per minute, expressed in **breaths per minute (breaths/min, brpm)**. At rest in healthy adults, RR normally falls in the range of **12–20 breaths/min** [1, cohort]. During sleep — the window most consumer wearables target — resting nocturnal RR in a large healthy-adult cohort (n = 10,000) centers around **15.4 breaths/min**, with 90% of values falling between 11.8 and 19.2 breaths/min [2, cohort]. Common clinical documentation of 18 or 20 breaths/min as a default, rather than an actual count, is a well-characterized measurement failure [1, cohort]. RR is distinct from **tidal volume** (air volume per breath, typically ~0.5 L at rest) and **minute ventilation** (RR × tidal volume, ~6–8 L/min at rest): wearables measure rate only, not volume or flow.

RR occupies a foundational place in clinical medicine as one of the **four classic vital signs** alongside heart rate, blood pressure, and temperature. It is also a durable prognostic signal: in a prospective community cohort of older adults, a mean nocturnal RR ≥ 16 breaths/min was independently associated with cardiovascular mortality (HR 1.57–2.58 across two cohorts) and all-cause mortality (HR 1.18–1.50), after adjustment for sleep-disordered breathing and comorbidities [3, cohort].

### Neural Architecture of Breathing: The Brainstem Control System

RR is not determined at the lungs; it emerges from a distributed network of brainstem nuclei. The **pre-Bötzinger complex (preBötC)**, located in the ventrolateral medulla, serves as the primary **inspiratory rhythm generator**. It contains glutamatergic excitatory interneurons and GABAergic/glycinergic inhibitory interneurons arranged in circuits capable of producing rhythmic inspiratory bursts [4, mechanism_review]. Rhythm generation in the preBötC appears to depend on emergent network properties rather than solely on intrinsic neuronal pacemaker activity: blocking persistent sodium current does not abolish the rhythm, implicating circuit-level recurrence [5, mechanism_review].

The **parafacial respiratory group / retrotrapezoid nucleus (pFRG/RTN)**, ventral to the facial nucleus, governs active expiration and functions as the primary **CO₂-sensing relay** to the rhythm generator. Phox2b-expressing neurons here are intrinsically sensitive to CO₂ and pH, directly coupling brainstem chemistry to ventilatory drive [4, mechanism_review; 6, mechanism_review]. During quiet breathing at rest, expiration is passive; the pFRG/RTN becomes recruitable under hypercapnic load or high metabolic demand.

The **pontine respiratory groups** — principally the Kölliker-Fuse nucleus (KF) and the parabrachial complex in the dorsolateral pons — do not generate rhythm independently. They **shape and adapt the breathing pattern** by governing the inspiratory off-switch (the phase transition from inspiration to expiration) and coordinating upper-airway resistance via descending projections [7, mechanism_review]. The KF-area receives ascending drive from the preBötC and projects back to modulate phase timing, thereby influencing breath duration and, through its inverse, respiratory rate.

### Chemical Drive: CO₂/pH Is Primary, O₂ Is Secondary

The dominant **chemical drive** to breathe is CO₂ and its surrogate, arterial pH, sensed by **central chemoreceptors** distributed across multiple brainstem loci including the RTN, locus ceruleus, and raphe nuclei. These neurons detect rising PCO₂ / falling pH and increase the output of the inspiratory rhythm generator, accelerating both depth and rate of breathing [6, mechanism_review]. The response is tonic and continuous: normal resting PaCO₂ (~40 mmHg) exerts background drive that, if withdrawn by prolonged hyperventilation, would produce apnea.

**Peripheral chemoreceptors** — principally the carotid bodies at the carotid bifurcation — are the primary sensors of arterial **O₂ partial pressure (PaO₂)**. They fire when PaO₂ falls below roughly 70 mmHg and relay signals via the glossopharyngeal nerve to the nucleus tractus solitarius [6, mechanism_review]. They also potentiate the central CO₂ response: bilateral carotid denervation depresses hyperoxic CO₂ sensitivity and causes sustained hypoventilation with PaCO₂ retention of 5–13 mmHg [6, mechanism_review]. In healthy adults at sea level, CO₂/pH dominates moment-to-moment RR regulation; the hypoxic drive is a reserve mechanism.

Beyond chemistry, RR is modulated by:

- **Mechanoreceptor feedback** — pulmonary stretch receptors (Hering-Breuer reflex) limit tidal volume inflation, influencing rate via vagal afferents.
- **Metabolic demand** — exercise increases RR and tidal volume; central command and muscle afferent feedback together account for ~40–50% of exercise hyperpnea [6, mechanism_review].
- **Emotional and volitional override** — cortical and limbic projections to the brainstem allow voluntary breath-holding, emotional sighing, and speech patterning.
- **Sleep state** — RR is most stable and lowest in NREM sleep; REM sleep introduces irregularity. The NREM window is the physiological basis for wearable nocturnal averaging.

### What Consumer Wearables Actually Measure

Most consumer wearables (Oura Ring, Apple Watch, Fitbit, WHOOP, Garmin) **do not directly count breaths**. Instead, they **derive RR from the photoplethysmography (PPG) signal** — an optical sensor that shines infrared or green light into peripheral tissue and detects pulsatile changes in blood volume. Three physiological mechanisms allow respiration to be extracted from the cardiac waveform [2, cohort; 8, open_label]:

1. **Respiratory sinus arrhythmia (RSA) — frequency modulation:** Vagal tone to the sinoatrial node varies with the respiratory cycle; heart rate rises slightly during inhalation and falls during exhalation. This creates a spectral peak in the heart-rate-variability power spectrum at exactly the breathing frequency. Isolating this RSA peak from the inter-beat-interval time series yields RR. Against polysomnography ground truth, this method achieves RMSE of ~0.65 brpm and MAE of ~0.46 brpm, with mean absolute percentage error of ~3% and Pearson r = 0.95 [2, cohort] (note: all authors were Fitbit/Google employees; manufacturer-affiliated validation — treat as indicative, not independently established).

2. **Amplitude modulation:** Intrathoracic pressure swings during breathing alter venous return and stroke volume, which in turn modulates the peak-to-trough amplitude of the PPG waveform on a breath-by-breath basis.

3. **Baseline / baseline-wander modulation:** Changes in arterial vasoconstriction and peripheral tissue blood volume driven by respiratory mechanics produce a slow oscillation in the DC baseline of the PPG signal at the breathing frequency.

The same three modulation types — baseline wander (BW), amplitude modulation (AM), and frequency modulation (FM) — are described in the systematic Charlton et al. 2018 review of ECG- and PPG-derived breathing rate [9, mechanism_review].

Device algorithms typically **fuse** two or more of these signals to improve robustness against artifact. Some platforms also incorporate **accelerometry** (wrist or ring micro-movement driven by chest excursion) as an additional modality [8, open_label]. Because motion artifacts corrupt all three PPG modulation mechanisms, virtually all consumer devices restrict their RR estimate to the **overnight sleep window** and report a **single nightly average** rather than continuous breath-by-breath data.

**What this means for interpretation:** PPG-derived nocturnal RR is an **estimate of resting ventilatory rate** during sleep, not a direct measurement of airflow or ventilation. It captures rate but not tidal volume or minute ventilation. It is most accurate in the low-motion NREM sleep window; accuracy degrades at higher respiratory rates because RSA amplitude weakens as RR rises above ~20 brpm [2, cohort]. The signal is fundamentally different from clinical capnography or respiratory inductance plethysmography — the gold standard used in polysomnography — but provides a practical, high-frequency window into resting breathing physiology that was previously inaccessible outside a sleep laboratory.

---

## Interpretation, Norms & The Personal Baseline

### Population Norms: What Is a Normal Respiratory Rate?

Respiratory rate is the count of complete breath cycles — one inhalation and one exhalation — per minute. In healthy resting adults, the conventionally accepted normal range is **12–20 breaths/min** [10, regulatory]. This band is operationalized in the National Early Warning Score 2 (NEWS2), the NHS-endorsed physiological deterioration system, which assigns a score of zero — meaning no concern — to any RR in this range [10, regulatory]. Rates of 21–24 breaths/min earn a score of 2, and ≥25 breaths/min a score of 3, while ≤8 breaths/min also scores 3 [10, regulatory]. In practical clinical terms, **tachypnea** (abnormally fast breathing) is most commonly flagged at >20 breaths/min, with >24 breaths/min representing a more urgent threshold; **bradypnea** (abnormally slow breathing) is flagged at <12 breaths/min, though clinical concern depends heavily on context (sedation, sleep apnea, high athletic fitness).

Population-level data confirm the norm. In the KORA FF4 cohort study (n = 2,224 adults aged 39–88 from Southern Germany, resting ECG-derived RR over 5 minutes), the median resting RR was 15.80 breaths/min with a 5th–95th percentile range of 12.06–20.06 breaths/min — tracking the conventional clinical band almost exactly [28, cohort]. The large Fitbit-derived dataset analyzed by Natarajan et al. found that 90% of nocturnal RR values in healthy adults fall between 11.8 and 19.2 breaths/min, with a population mean of 15.4 breaths/min [2, cohort]. This tight empirical corridor — essentially the same as the clinical guideline — validates NEWS2's 12–20 band as accurately representing population reality, not just consensus convention.

### Pediatric Ranges: RR Declines Steeply with Age

Children breathe considerably faster than adults, and the rate declines steeply through early life before reaching adult values in mid-adolescence. The most rigorous evidence comes from Fleming et al.'s systematic review of 69 studies (n = 3,881 children, birth to 18 years), published in The Lancet [11, meta_analysis]. Key age-stratified medians:

| Age group | Approximate median RR (breaths/min) |
|-----------|-------------------------------------|
| Newborn (birth) | ~44 |
| 1–2 years | ~26 |
| 3–5 years | ~24 |
| 6–11 years | ~20 |
| 12–15 years | ~18 |
| >15 years (adolescent) | ~16 → adult range |

The steepest decline occurs in the first two years of life. By school age, rates are approaching but still above adult norms; by mid-adolescence, the 12–20 range applies. This developmental trajectory matters for anyone tracking pediatric wearable data: what reads as tachypnea in an adult is physiological in a 2-year-old.

### The Load-Bearing Wearable Point: The Personal Baseline Is Tight

Here is where RR diverges from every other vital sign in wearable context: **nocturnal RR is remarkably stable within an individual across nights — far more stable than the wide population distribution suggests**.

Natarajan et al. (Fitbit/Google-affiliated), analyzing continuous nocturnal RR data from a large Fitbit cohort across 14-day monitoring windows, found that **within-person coefficient of variation (CV) was only 2.3–9.5% in younger adults (ages 20–24), rising to 2.5–21.7% in older age bands (ages 65–69)** [2, cohort]. The load-bearing point holds across age groups — within-person stability remains the reference frame, because each person's baseline is tight relative to the wide population spread — but the absolute CV ceiling climbs with age, so older adults should expect somewhat wider night-to-night scatter around their personal mean than younger adults. To put the younger-adult figures in concrete terms: for a person whose average nocturnal RR is 14.5 breaths/min, a CV of 2.3–9.5% implies night-to-night fluctuation of roughly ±0.3–1.4 breaths/min around their stable personal mean. The personal range is tight enough that a shift of even 1–2 breaths/min can be physiologically meaningful. By comparison, the **inter-individual** (person-to-person) variance is wide: one healthy adult's stable nocturnal RR might be 13.2 breaths/min while another's is 17.5 — a gap that is entirely normal but would look clinically suspicious if you only had the population reference [2, cohort].

Toften et al. confirmed this in a 3-month longitudinal validation study using a radar-based, contactless sleep monitor (Somnofy; n = 37 healthy adults, nightly monitoring) [12, cohort]. Nightly filtered RR averages were "fairly consistent from night to night," with Bland-Altman 95% limits of agreement for nightly averages of **−0.07 to −0.04 breaths/min** — a span of less than 0.1 brpm that represents exceptionally tight within-person stability. For someone whose nocturnal RR averages 14–15 breaths/min, this measurement window means a genuine 2–3 brpm elevation during illness stands out clearly above the noise floor. Crucially, the study established personalized baselines from the first 40 nights of data and monitored for deviations. During documented illness episodes, all four participants who became sick showed RR increases that exceeded their individual confidence intervals — deviations that the wide population norm would have classified as "still normal" but the personal baseline flagged immediately [12, cohort]. The Toften device MAE was 0.18 brpm against the radar reference standard.

Ravindran et al., studying contactless nocturnal monitoring in 35 older adults (ages 65–83) over 7–14 nights at home, reported a mean nocturnal breathing rate of 14.7 breaths/min (SD 2.9 across the group), with contactless devices achieving mean absolute error ≤1.6 breaths/min relative to polysomnography — adequate resolution to track personal-baseline shifts of the magnitude seen in illness [13, cohort].

### Why the Personal-Baseline Frame Is the Right Frame

The synthesis from these longitudinal wearable studies produces a clear operating principle for RR interpretation: **population norms establish the outer bounds of plausibility, but the signal lives in deviation from your own baseline**.

RR is less inter-individually variable at rest than HRV — the population spread is a few breaths/min, not an order of magnitude. But within-person, RR is even tighter than within-person HRV: the CV data from Natarajan et al. show that a healthy adult's nocturnal RR varies less night-to-night than their nocturnal heart rate [2, cohort]. This combination — a modest but defined population range, plus high within-person stability — makes nocturnal RR an unusually sensitive personal-trend signal. The clinical utility of wearable RR does not come from comparing you to the population. It comes from comparing tonight to your own last 30 nights.

Deviations from personal baseline — an elevation of 2–3+ breaths/min sustained across 1–2 nights — are early flags for acute illness (respiratory infection, febrile illness), physiological stress (high-intensity training load, significant altitude gain), alcohol consumption (which disrupts sleep architecture and elevates RR), or environmental perturbations. These triggers and their magnitudes are covered in detail in the Determinants & Significance section below.

A measurement-consistency requirement follows directly from this: because the signal is the within-person deviation, **the device, sleep conditions, and measurement window must be stable across nights**. Mixing wrist-based and ring-based device data, or comparing nocturnal resting RR against an active-period measurement, will contaminate the baseline. The personal baseline is only as reliable as the measurement protocol.

---

## Measurement & Device Validity

### Reference Standards

Respiratory rate can be measured by a hierarchy of methods, each with distinct trade-offs between accuracy, practicality, and suitability for continuous or ambulatory use.

**Manual observation** — counting chest rises over a full 30–60 seconds — is the bedside clinical standard and has been used as a comparator in numerous validation studies. Despite this role, it is widely documented as the most inaccurate and most poorly charted vital sign in hospital practice. Nurses frequently default to recording 18 or 20 breaths per minute regardless of the patient's actual rate, and during the 24-hour period before cardiac arrest, RR is the vital sign documented least often [15, cohort]. A controlled inter-observer study found that when nurses were asked to count respiratory rate from video, agreement was high (ICC 0.99) under ideal conditions — standardized viewing, no patient movement, full 60-second counting windows — but clinical ward conditions meet none of these criteria [16, cohort]. The gap between protocol-measured agreement and real-world charting accuracy is the central argument for continuous automated monitoring.

**Capnography (end-tidal CO₂, EtCO₂)** is the gold standard for true breath-by-breath detection in instrumented or peri-operative settings. It directly measures exhaled CO₂ concentration, yielding a waveform that unambiguously identifies each breath. Its limitation is practical: capnography requires a nasal cannula or intubation interface that is poorly tolerated for extended ambulatory use and is unsuitable for consumer wearables [24, cohort].

**Respiratory inductance plethysmography (RIP) belts** — circumferential bands placed around the chest and abdomen that sense volume changes via inductance — provide continuous, non-invasive respiratory waveforms and are used both in clinical monitoring and as a reference standard in sleep studies. RIP belts can distinguish obstructive from central apneas; the design of the belt (coil geometry, calibration method) substantially affects signal quality [25, mechanism_review].

**Polysomnography (PSG)** in the sleep laboratory combines multiple channels — nasal thermocouple or pressure transducer, chest and abdominal RIP belts, oximetry, EEG, and EMG — into the definitive multi-channel sleep reference. For wearable RR validation during sleep, PSG-derived RR (from the airflow thermistor or RIP channel) is the standard comparator.

### PPG-Derived Respiratory Rate: The Wearable Method

Consumer wearables derive RR from the photoplethysmography (PPG) signal — the optical measurement of peripheral blood volume that also drives heart-rate estimation. Respiration leaves three distinct modulations on the PPG waveform, described in the systematic Charlton et al. 2018 review [9, mechanism_review]:

1. **Baseline wander (BW):** respiratory-driven slow drift in PPG baseline, reflecting venous pressure changes.
2. **Amplitude modulation (AM):** stroke-volume variation with each breath causes beat-to-beat changes in PPG pulse height.
3. **Frequency modulation (FM):** respiratory sinus arrhythmia (RSA) produces subtle beat-rate changes locked to the breathing cycle.

Consumer devices extract one or more of these modulations, then estimate RR via spectral analysis, peak detection, or learned (neural-network) approaches. Higher-performing algorithms fuse all three modulation channels and apply quality-assessment filters that reject low-confidence windows — a design principle first systematically benchmarked in Charlton et al. 2016 [26, open_label], which tested 314 PPG and ECG algorithms against a nasal-oral pressure reference in healthy adults. The best PPG-based algorithm achieved a Bland-Altman bias of 1.0 brpm with limits of agreement (LoA) of −5.1 to +7.2 brpm. ECG-based algorithms outperformed PPG-based ones, a gap that persists in part because wrist PPG is more susceptible to motion artifact than chest-lead ECG.

### Accuracy Under Rested and Sleep Conditions

PPG-derived RR is most accurate during sleep and rest, when breathing is regular, motion is minimal, and signal quality is high. The Samsung Galaxy Watch validation study — conducted in 195 participants undergoing overnight PSG at a sleep clinic, with nasal thermocouple as reference — reported an average-overnight RR RMSE of 1.13 brpm (bias 0.39 brpm, Bland-Altman LoA −1.68 to +2.46 brpm) and a continuous-epoch RMSE of 1.62 brpm (LoA −2.73 to +3.47 brpm) [27, cohort]. Accuracy exceeded 90% (within ±2 brpm) for participants with normal to moderate obstructive sleep apnea (AHI < 30), but fell to 79.5% (average) and 75.8% (continuous) for severe OSA (AHI ≥ 30). **COI disclosure: two of the four listed authors are Samsung Electronics employees; the study was funded by Samsung Electronics. These figures are manufacturer-reported and await independent (non-vendor) replication before they can be treated as established benchmarks.**

In the algorithm-validation literature, a multi-modulation PPG fusion method tested against capnography (Capnobase dataset, n = 42 recordings) achieved a bias of 0.28 brpm, LoA of −3.62 to +4.17 brpm, and RMSE of 1.8 brpm; against PSG-derived nasal/oral airflow in a pediatric sleep dataset, bias was 0.04 brpm, LoA −5.74 to +5.82 brpm, RMSE 2.3 brpm [29, cohort]. **These fusion-accuracy figures are manufacturer-reported (study with LGT Medical Inc.-affiliated authors) and await independent (non-vendor) replication.** The figures suggest that sub-2 brpm errors (MAE often < 1 brpm against PSG in adults) are achievable at rest when signal quality is controlled, and that fusion of multiple PPG modulation features outperforms single-channel extraction, but the manufacturer affiliation warrants caution in treating these as independently established benchmarks.

The effect of measurement site adds another layer of variability. In a controlled study of six body locations in 36 healthy subjects, the forehead and finger yielded the best PPG-derived respiratory frequency agreement under normal and deep breathing respectively; the wrist showed wider LoA and site-dependent bias [30, cohort]. Consumer devices use the wrist exclusively — a compromise of convenience over signal quality.

### Accuracy Degradation: Motion, Irregular Breathing, and Apnea

PPG-derived RR degrades in predictable ways:

- **Motion artifact** is the dominant confound on wrist PPG. Accelerometer-based motion correction helps but cannot eliminate artifact during vigorous activity; most consumer devices suppress RR output or widen uncertainty windows during active epochs.
- **Irregular breathing** (highly variable inter-breath intervals, Cheyne-Stokes patterns) breaks spectral-peak assumptions; the Samsung data showing 20+ percentage-point accuracy drops in severe OSA is the empirical illustration of this [27, cohort].
- **Apnea events** create signal ambiguity — no airflow to detect — and some devices will miss apnea periods entirely or report an interpolated rate rather than zero. This is why consumer PPG RR does not diagnose obstructive sleep apnea or respiratory failure, even in devices that report a breathing disturbance index as a secondary output.
- **Low perfusion and arrhythmia** (atrial fibrillation, frequent ectopy) corrupt both the AM and FM modulation channels, since these rely on beat-to-beat regularity.

The 2020 JMIR systematic review of continuous vital-signs monitoring by wearable devices concluded that, across included studies, RR measurements frequently showed "wide LoA" beyond clinically acceptable ranges (±3 brpm), and that there were no high-quality large controlled studies demonstrating clinical benefit [31, mechanism_review].

### Within-Device Trends vs. Absolute Cross-Device Values

Proprietary RR algorithms are not interchangeable. A Garmin estimate of 14 brpm and an Apple estimate of 14 brpm on the same individual may reflect different algorithmic constructs applied to different PPG wavelengths at different sampling rates. Cross-device comparison of absolute RR values is therefore not meaningful. What is reproducible within a device — under consistent wearing conditions, time of night, and sleep stage — is the trend signal: rising overnight average RR over weeks may reflect developing illness, altitude acclimatization failure, or overtraining, regardless of whether the absolute number is precisely calibrated.

**Regulatory framing:** Consumer RR is consistently classed as a **wellness metric, not a diagnostic measurement**. No current consumer wristwatch carries regulatory clearance for diagnosing respiratory failure, apnea syndrome, or pneumonia based on its PPG-derived RR output. Some devices flag "breathing disturbance" alongside SpO₂ anomalies and pair these with questionnaire prompts to consult a clinician — this is appropriate scope. The validated clinical use of continuous RR monitoring (e.g., the postoperative setting where wrist-PPG devices achieved 93% of measurements within ±3 brpm vs. capnography, with a bias of 0.17 brpm) still requires formal clinical validation per ISO/IEEE device standards, not consumer app approval [24, cohort].

---

## Determinants & Significance

### What Raises Respiratory Rate

**Fever, illness, and infection** are among the most clinically important drivers of elevated RR. The body's metabolic response to infection — including cytokine release, elevated temperature, and increased oxygen demand — accelerates breathing rate, often before the person feels unwell. Wearable cohort studies have documented that nocturnal respiratory rate frequently rises around or just prior to symptom onset in SARS-CoV-2 infection: in a Fitbit-based study by Natarajan et al. [2, cohort], 36.4% of symptomatic individuals had at least one nocturnal RR measurement ≥3 breaths/min above their personal baseline within a 7-day window around illness onset (Cohen's d = 0.70 for the within-subject shift), compared with 23.7% of asymptomatic individuals. The TemPredict cohort (N = 63,153 Oura ring users; 73 COVID+ participants with PCR-confirmed infection used for algorithm training) detected illness a mean of 2.75 days before participants sought testing, incorporating respiratory rate alongside temperature, HRV, and heart rate, with an AUC of 0.819, sensitivity 82%, specificity 63% [14, cohort]. A 2022 Lancet Digital Health systematic review of wearable COVID-19 detection studies (12 completed articles; devices including Fitbit, Oura, WHOOP, and others) found AUCs of 0.52–0.92 across algorithmic models, with 3 of 4 studies that measured RR finding elevation around symptom onset [32, meta_analysis].

**Exertion and metabolic demand** increase RR proportionally to workload. During intense exercise, RR may reach 40–60 breaths/min in healthy adults. This is physiological and resolves rapidly with rest.

**Anxiety, stress, and panic** can trigger hyperventilation — rapid, shallow breathing that drives down CO₂ (hypocapnia), producing lightheadedness, tingling, and chest tightness. The RR elevation here is neurogenic rather than metabolic.

**Pain** acutely elevates RR via sympathetic activation and the physiological stress response.

**Metabolic acidosis** generates a compensatory respiratory alkalosis: the body increases RR to exhale more CO₂ and partially correct the acidemia. In diabetic ketoacidosis, this produces the characteristic Kussmaul breathing — deep, labored, sighing respirations that may exceed 25–30 breaths/min.

**Hypoxia, altitude, and cardiorespiratory disease** (asthma, COPD, pneumonia, pulmonary embolism, heart failure with pulmonary congestion) all raise RR because the body is attempting to increase alveolar ventilation in response to impaired gas exchange or reduced oxygen availability.

**Pregnancy** causes a mild, sustained RR increase (typically 1–2 breaths/min) driven by progesterone-mediated chemoreceptor sensitization.

**Stimulants** (caffeine, amphetamines, some pre-workout compounds) transiently elevate RR through sympathomimetic effects.

### What Lowers Respiratory Rate

**Opioids and sedatives** are the primary pharmacological depressants of respiratory drive and represent a major safety concern in clinical settings. Opioids bind μ-receptors in the brainstem respiratory centers, suppressing both rate and depth of breathing. The PRODIGY trial — an international prospective observational study of 1,335 general care floor patients receiving parenteral opioids, monitored with continuous capnography and oximetry — found that 614 (46%) experienced at least one opioid-induced respiratory depression (OIRD) episode (defined as RR ≤ 5 breaths/min, SpO₂ ≤ 85%, or ETCO₂ out of range for ≥3 min, or apnea > 30 sec) [17, cohort]. Patients with ≥1 OIRD episode had 2.8 additional hospital days (10.5 vs 7.7 days, p < 0.0001) and 17% higher costs (propensity-weighted; ~$3,686/patient additional) [18, cohort]. High-risk patients (PRODIGY score) had 6× the odds of OIRD vs low-risk patients (OR 6.07, 95% CI 4.44–8.30) [17, cohort]. Importantly, OIRD often manifests as intermittent apneic episodes — not simply a slow RR — a pattern that standard spot-check vital signs miss: a post-hoc analysis of the PRODIGY trial found that spot-checks of oxygenation miss up to 90% of clinical hypoxemia episodes [19, cohort].

**CNS depressants** (benzodiazepines, barbiturates, general anesthetics) act similarly, through different receptor mechanisms, to reduce respiratory drive.

**Hypothyroidism** in severe or myxedematous states decreases metabolic rate and may cause hypoventilation.

**Sleep** produces a modest physiological reduction in RR (roughly 1–2 breaths/min below waking baseline) as metabolic demand and CO₂ sensitivity both decrease.

**Slow-breathing practices** (pranayama, resonance frequency breathing, coherent breathing) deliberately lower RR to 4–8 breaths/min; this is intentional and physiologically distinct from pathological suppression.

### 1. The Underused Vital Sign: RR as an Early Deterioration Signal

Respiratory rate is among the most powerful predictors of clinical deterioration in hospitalized patients — yet it remains the least reliably measured and documented of the conventional vital signs.

In an early landmark case-control study (Fieselmann et al., 1993; N = 59 arrest cases, 91 matched controls), a single RR > 27 breaths/min in the 72 hours before arrest predicted cardiopulmonary arrest with OR 5.56 (95% CI 2.67–11.49; sensitivity 0.54, specificity 0.83) [20, cohort]. Crucially, pulse rate and blood pressure were not predictive of arrest in the same cohort — RR stood alone. Subsequent work by Goldhill and colleagues found that 21% of ward patients with a RR of 25–29 breaths/min — assessed by a critical care outreach service — died in hospital, a figure that rose with higher rates [23, cohort].

This evidence is formalized in the **National Early Warning Score 2 (NEWS2)**, the UK Royal College of Physicians' standardized acute-illness severity tool, adopted across NHS England and NHS Improvement for identifying acutely ill patients including those with sepsis [10, regulatory]. In NEWS2, RR is scored as follows:

| RR (breaths/min) | NEWS2 points |
|---|---|
| ≤ 8 | 3 |
| 9–11 | 1 |
| 12–20 | 0 (normal) |
| 21–24 | 2 |
| ≥ 25 | 3 |

A score of 3 on any single parameter — which RR achieves at both the very low and high ends — triggers an urgent clinical response independent of total score. A total NEWS2 score ≥ 7 requires emergency assessment with critical care involvement. RR is described in NEWS2 guidance as the most sensitive early indicator of clinical deterioration, with a rising rate often preceding other physiological changes by hours.

Despite this, respiratory rate has been documented as the vital sign most likely to be omitted or inaccurately recorded in clinical practice. Palmer et al. (2023) — an integrative review of 19 studies across acute care settings — found that RR was "consistently the least frequently measured and accurately documented vital sign," with nurses frequently entering values into charts without performing a count [22, mechanism_review]. An earlier editorial synthesis by Cretikos et al. (2008) titled "Respiratory rate: the neglected vital sign" summarized multicentre evidence that documentation of vital signs in many hospitals was extremely poor, with RR in particular often absent even when the patient's primary problem was respiratory [21, mechanism_review].

### 2. Wearable Early-Illness Detection: The Marquee Consumer Application

For healthy individuals using consumer wearables (Oura, Fitbit, WHOOP, Garmin, and others), elevated nocturnal RR versus personal baseline is among the most actionable illness-detection signals these devices can provide. During sleep, motion artifact is minimized and the signal is relatively stable, making it the preferred window for PPG-derived RR measurement.

The evidence base is real but requires honest framing. The Natarajan et al. (2021) Fitbit study [2, cohort] and the TemPredict/Oura study [14, cohort] demonstrate that multi-signal wearable algorithms — incorporating RR alongside temperature, HRV, and heart rate — can detect illness around or before symptom onset with meaningful AUC values (0.77–0.82). However, RR alone does not function as a diagnostic test: the Mitratza et al. (2022) Lancet Digital Health review [32, meta_analysis] reports that across the broader wearable COVID-detection literature, model AUCs span a wide range (0.52–0.92), reflecting heterogeneous populations, device types, and reference standards.

**False positives are common.** Alcohol consumption, a late or heavy meal, elevated ambient room temperature, vigorous late-evening training, and heat illness all raise nocturnal RR without any infectious cause. This means a single elevated reading carries low specificity. The appropriate interpretation is *sustained elevation above personal baseline (typically 2–3+ breaths/min for multiple consecutive nights), in conjunction with other signals (resting HR elevation, HRV depression, temperature rise, sleep disruption)*.

### 3. Sleep-Disordered Breathing

Some wearable devices (Withings, Oura Gen 3+, Garmin) track RR variability across the night to flag potential obstructive sleep apnea patterns — specifically, the periodic fluctuations in RR associated with respiratory events. This is an emerging application; devices are not FDA-cleared diagnostic tools, and anyone with suspected sleep apnea requires formal polysomnography.

### Limitations

**Consumer-grade RR is a nocturnal estimate, not a continuous ventilation measurement.** Wearable PPG-derived RR is computed from respiratory sinus arrhythmia in the heart rate signal during sleep. It does not measure tidal volume, minute ventilation, or breathing pattern quality — all clinically meaningful. A normal RR does not exclude pathological breathing (e.g., Cheyne-Stokes, Kussmaul, or obstructive apneas with normal mean rate).

**PPG-RR degrades with motion and arrhythmia.** During movement or in patients with atrial fibrillation, the RSA-based RR estimate becomes unreliable. Wearable RR is best interpreted during confirmed sleep periods.

**Single nocturnal readings have high false-positive rates for illness.** Alcohol, heat, overtraining, and stress all elevate nocturnal RR. No single reading should be acted upon in isolation.

**This is a wellness and trend metric, not a diagnostic test.** Consumer wearable RR is appropriate for personal trend monitoring and population-level research; it is not a clinical measurement and cannot substitute for bedside respiratory rate counting (one full minute) in any clinical context.

---

## Bibliography

[1]. Badawy J, Nguyen OK, Clark C, Halm EA, Makam AN. Is everyone really breathing 20 times a minute? Assessing epidemiology and variation in recorded respiratory rate in hospitalised adults. *BMJ Quality & Safety*. 2017;27(11):842–848. PMID: 28652259 — tag: cohort — tier: 2

[2]. Natarajan A, Su H-W, Heneghan C, Blunt L, O'Connor C, Niehaus L. Measurement of respiratory rate using wearable devices and applications to COVID-19 detection. *npj Digital Medicine*. 2021;4:136. doi:10.1038/s41746-021-00493-6. PMID: 34526602 — tag: cohort — tier: 2. COI: authors include Fitbit/Google employees; device-affiliated funding context applies — treat accuracy figures as indicative, not independently established.

[3]. Baumert M, Linz D, Stone K, McEvoy RD, Cummings S, Redline S, Mehra R, Immanuel S. Mean nocturnal respiratory rate predicts cardiovascular and all-cause mortality in community-dwelling older men and women. *European Respiratory Journal*. 2019;54(1):1900120. PMID: 31151958 — tag: cohort — tier: 1

[4]. Ikeda K, Kawakami K, Onimaru H, Okada Y, Yokota S, Koshiya N, Oku Y, Iizuka M, Koizumi H. The respiratory control mechanisms in the brainstem and spinal cord: integrative views of the neuroanatomy and neurophysiology. *Journal of Physiological Sciences*. 2017;67(1):45–62. PMID: 27535569 — tag: mechanism_review — tier: 2

[5]. Feldman JL, Mitchell GS, Nattie EE. Breathing: rhythmicity, plasticity, chemosensitivity. *Annual Review of Neuroscience*. 2003;26:239–266. PMID: 12598679 — tag: mechanism_review — tier: 1

[6]. Dempsey JA, Smith CA. Pathophysiology of human ventilatory control. *European Respiratory Journal*. 2014;44(2):495–512. PMID: 24925922 — tag: mechanism_review — tier: 1

[7]. Dutschmann M, Dick TE. Pontine mechanisms of respiratory control. *Comprehensive Physiology*. 2012;2(4):2443–2469. PMID: 23720253 — tag: mechanism_review — tier: 2

[8]. Kim H, Kim J-Y, Im C-H. Fast and robust real-time estimation of respiratory rate from photoplethysmography. *Sensors (Basel)*. 2016;16(9):1494. PMID: 27649182 — tag: open_label — tier: 3

[9]. Charlton PH, Birrenkott DA, Bonnici T, Pimentel MAF, Johnson AEW, Alastruey J, Tarassenko L, Watkinson PJ, Beale R, Clifton DA. Breathing rate estimation from the electrocardiogram and photoplethysmogram: a review. *IEEE Reviews in Biomedical Engineering*. 2018;11:2–20. doi:10.1109/RBME.2017.2763681. PMID: 29990026 — tag: mechanism_review — tier: 1

[10]. Royal College of Physicians. *National Early Warning Score (NEWS) 2: Standardising the assessment of acute-illness severity in the NHS. Updated report of a working party.* London: RCP; December 2017. — tag: regulatory — tier: 1

[11]. Fleming S, Thompson M, Stevens R, Heneghan C, Plüddemann A, Maconochie I, Tarassenko L, Mant D. Normal ranges of heart rate and respiratory rate in children from birth to 18 years of age: a systematic review of observational studies. *Lancet*. 2011;377(9770):1011–1018. doi:10.1016/S0140-6736(10)62226-X. PMID: 21411136 — tag: meta_analysis — tier: 1

[12]. Toften S, Kjellstadli JT, Thu OKF, Ellingsen OJ. Noncontact Longitudinal Respiratory Rate Measurements in Healthy Adults Using Radar-Based Sleep Monitor (Somnofy): Validation Study. *JMIR Biomedical Engineering*. 2022;7(2):e36618. doi:10.2196/36618. PMID: 38875674 — tag: cohort — tier: 2. Toften MAE: 0.18 brpm; nightly LoA −0.07 to −0.04 brpm.

[13]. Ravindran KKG, della Monica C, Atzori G, Lambert D, Hassanin H, Revell V, Dijk D-J. Reliable Contactless Monitoring of Heart Rate, Breathing Rate, and Breathing Disturbance During Sleep in Aging: Digital Health Technology Evaluation Study. *JMIR mHealth and uHealth*. 2024;12:e53643. doi:10.2196/53643. PMID: 39190477 — tag: cohort — tier: 2

[14]. Mishra T, Wang M, Metwally AA, et al. Detection of COVID-19 using multimodal data from a wearable device: results from the first TemPredict Study. *Scientific Reports*. 2022;12:4349. doi:10.1038/s41598-022-07314-0. PMID: 35236896 — tag: cohort — tier: 2. COI: conducted with Oura Health collaboration; device-affiliated funding context applies.

[15]. Rivas E, López-Baamonde M, Sanahuja J, Del Rio E, Ramis T, Recasens A, López A, Arias M, Kampakis S, Lauteslager T, Awara O, Mascha EJ, Soriano A, Badía JR, Castro P, Sessler DI, et al. Early detection of deterioration in COVID-19 patients by continuous ward respiratory rate monitoring: a pilot prospective cohort study. *Frontiers in Medicine*. 2023;10:1243050. doi:10.3389/fmed.2023.1243050. PMID: 38020176 — tag: cohort — tier: 3. COI: three authors employed by Circadia Technologies Ltd. (device manufacturer); study funded by Circadia Technologies Ltd.

[16]. Nielsen LG, Folkestad L, Brodersen JB, Brabrand M. Inter-observer agreement in measuring respiratory rate. *PLoS ONE*. 2015;10(6):e0129493. doi:10.1371/journal.pone.0129493. PMID: 26090961 — tag: cohort — tier: 3

[17]. Khanna AK, Bergese SD, Jungquist CR, et al. Prediction of opioid-induced respiratory depression on inpatient wards using continuous capnography and oximetry: an international prospective, observational trial. *Anesthesia & Analgesia*. 2020;131(4):1012–1024. doi:10.1213/ANE.0000000000004788. PMID: 32925318 — tag: cohort — tier: 2

[18]. Khanna AK, Saager L, Bergese SD, et al. Opioid-induced respiratory depression increases hospital costs and length of stay in patients recovering on the general care floor. *BMC Anesthesiology*. 2021;21(1):88. doi:10.1186/s12871-021-01307-8. PMID: 33743588 — tag: cohort — tier: 2

[19]. Doufas AG, Laporta ML, Driver CN, et al. Incidence of postoperative opioid-induced respiratory depression episodes in patients on room air or supplemental oxygen: a post-hoc analysis of the PRODIGY trial. *BMC Anesthesiology*. 2023;23:332. doi:10.1186/s12871-023-02291-x. PMID: 37794334 — tag: cohort — tier: 2

[20]. Fieselmann JF, Hendryx MS, Helms CM, Wakefield DS. Respiratory rate predicts cardiopulmonary arrest for internal medicine inpatients. *Journal of General Internal Medicine*. 1993;8(7):354–360. doi:10.1007/BF02600071. PMID: 8410395 — tag: cohort — tier: 2

[21]. Cretikos MA, Bellomo R, Hillman K, Chen J, Finfer S, Flabouris A. Respiratory rate: the neglected vital sign. *Medical Journal of Australia*. 2008;188(11):657–659. doi:10.5694/j.1326-5377.2008.tb01825.x. PMID: 18513176 — tag: mechanism_review — tier: 3

[22]. Palmer JH, James S, Wadsworth D, Gordon CJ, Craft J. How registered nurses are measuring respiratory rates in adult acute care health settings: An integrative review. *Journal of Clinical Nursing*. 2023;32(15-16):4515–4527. doi:10.1111/jocn.16522. PMID: 36097417 — tag: mechanism_review — tier: 3

[23]. Goldhill DR, McNarry AF, Mandersloot G, McGinley A. A physiologically-based early warning score for ward patients: the association between score and outcome. *Anaesthesia*. 2005;60(6):547–553. doi:10.1111/j.1365-2044.2005.04186.x. PMID: 15918825 — tag: cohort — tier: 2

[24]. van der Stam JA, Mestrom EHJ, Scheerhoorn J, Jacobs FENB, Nienhuijs S, Boer AK, van Riel NAW, de Morree HM, Bonomi AG, Scharnhorst V, Bouwman RA. The accuracy of wrist-worn photoplethysmogram-measured heart and respiratory rates in abdominal surgery patients: observational prospective clinical validation study. *JMIR Perioperative Medicine*. 2023;6(1):e40474. doi:10.2196/40474. PMID: 36804173 — tag: cohort — tier: 2. COI: one author consulted for Philips Research; two authors were Philips Research employees; funded by Dutch RVO ITEA grant.

[25]. Hussain T, Ullah S, Fernández-García R, Gil I. Wearable sensors for respiration monitoring: a review. *Sensors (Basel)*. 2023;23(17):7518. doi:10.3390/s23177518. PMID: 37687977 — tag: mechanism_review — tier: 3

[26]. Charlton PH, Bonnici T, Tarassenko L, Clifton DA, Beale R, Watkinson PJ. An assessment of algorithms to estimate respiratory rate from the electrocardiogram and photoplethysmogram. *Physiological Measurement*. 2016;37(4):610–626. doi:10.1088/0967-3334/37/4/610. PMID: 27027672 — tag: open_label — tier: 1

[27]. Jung H, Kim D, Choi J, Joo EY. Validating a consumer smartwatch for nocturnal respiratory rate measurements in sleep monitoring. *Sensors (Basel)*. 2023;23(18):7976. doi:10.3390/s23187976. PMID: 37766031 — tag: cohort — tier: 3. COI: Jung and Choi affiliated with Samsung Electronics; study funded by Samsung Electronics and Samsung Medical Center. Treat absolute accuracy figures with caution given manufacturer funding; manufacturer-reported, pending independent replication.

[28]. Rückert-Eheberg IM, Steger A, Müller A, Linkohr B, Barthel P, Maier M, et al. Respiratory rate and its associations with disease and lifestyle factors in the general population — results from the KORA-FF4 study. *PLoS ONE*. 2025;20(3):e0318502. doi:10.1371/journal.pone.0318502. PMID: 40067853 — tag: cohort — tier: 2

[29]. Dehkordi P, Garde A, Molavi B, Ansermino JM, Dumont GA. Extracting instantaneous respiratory rate from multiple photoplethysmogram respiratory-induced variations. *Frontiers in Physiology*. 2018;9:948. doi:10.3389/fphys.2018.00948. PMID: 30072918 — tag: cohort — tier: 2. COI: Ansermino and Dumont are founders of LGT Medical Inc. with equity in related technology; Molavi is employed by LGT Medical Inc. Manufacturer-reported; pending independent replication.

[30]. Hartmann V, Liu H, Chen F, Hong W, Hughes S, Zheng D. Toward accurate extraction of respiratory frequency from the photoplethysmogram: effect of measurement site. *Frontiers in Physiology*. 2019;10:732. doi:10.3389/fphys.2019.00732. PMID: 31316390 — tag: cohort — tier: 2

[31]. Leenen JPL, Leerentveld C, van Dijk JD, van Westreenen HL, Schoonhoven L, Patijn GA. Current evidence for continuous vital signs monitoring by wearable wireless devices in hospitalized adults: systematic review. *Journal of Medical Internet Research*. 2020;22(6):e18636. doi:10.2196/18636. PMID: 32469323 — tag: mechanism_review — tier: 2

[32]. Mitratza M, Goodale BM, Shagadatova A, et al. The performance of wearable sensors in the detection of SARS-CoV-2 infection: a systematic review. *Lancet Digital Health*. 2022;4(6):e410–e425. doi:10.1016/S2589-7500(22)00019-X. PMID: 35461692 — tag: meta_analysis — tier: 1
