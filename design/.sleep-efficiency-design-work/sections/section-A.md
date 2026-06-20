# Section A: What Sleep Efficiency Is and What the Device Measures

## Definition and Formula

Sleep efficiency (SE) is a summary index of sleep continuity — the fraction of in-bed time actually spent asleep, expressed as a percentage:

**SE (%) = Total Sleep Time (TST) ÷ Time in Bed (TIB) × 100**

SE does not describe sleep architecture (how much REM or slow-wave sleep occurred) nor the circadian timing of sleep. Its narrow, well-specified job is to capture how consolidated the sleep episode was. An SE of 85% means that 15% of in-bed time was spent awake — through difficulty falling asleep, middle-of-the-night waking, or lying in bed after the final awakening.

## Component Definitions

**Time in Bed (TIB)** is the full window from the moment the person settles into bed with the intent to sleep ("lights out") to the moment they rise for the final time ("out of bed" or "lights on"). TIB is the denominator; it captures total opportunity, not total sleep.

**Total Sleep Time (TST)** is the sum of time actually scored as sleep within the TIB window. In polysomnographic (PSG) terms, TST = time in stages N1 + N2 + N3 + REM. Arithmetically, TST = TIB − sleep-onset latency (SOL) − wake after sleep onset (WASO) − early morning awakening (any wake time before final rising) [1, regulatory].

- **SOL** (sleep-onset latency): the interval from lights-out to the first sustained sleep epoch. The AASM Scoring Manual distinguishes SOL-to-N1 from SOL-to-persistent-sleep (first epoch of N2, N3, or REM sustained across 10 minutes) [1, regulatory].
- **WASO** (wake after sleep onset): all wake time logged after sleep onset and before final rising. WASO captures nocturnal awakenings and is the primary driver of SE degradation in insomnia [1, regulatory].

**Low SE** therefore signals one of two problems — or both: the sleeper took a long time to fall asleep (high SOL), or they woke frequently and lay awake in the night (high WASO). High SE means the available time in bed was used efficiently for sleep.

## SE as a Distinct Metric

SE is a single number that *summarizes* the components above; it does not replace them. SOL, WASO, TST, and sleep-stage percentages each carry distinct clinical information. A person with 7 hours TIB, 30-minute SOL, and 0 WASO has 87% SE; a person with 7 hours TIB, 0-minute SOL, and 30 minutes of fragmented WASO has the same 87% SE. The number is identical but the physiology differs. SE is therefore most informative alongside its component terms, not in isolation [2, mechanism_review].

## The PSG Gold Standard

PSG scores sleep from concurrent electroencephalography (EEG), electro-oculography (EOG), and electromyography (EMG), epoch-by-epoch (standard epoch length: 30 seconds), per AASM Scoring Manual rules [1, regulatory]. The resulting hypnogram is the ground truth from which TIB, TST, SOL, WASO, and stage percentages are computed. PSG-derived SE is the reference against which every wearable estimate is validated.

## What Consumer Wearables Actually Measure

Consumer devices — fitness bands, smartwatches, ring-form-factor trackers — do not record EEG. Instead, they use two primary sensor streams:

1. **Actigraphy / accelerometry**: wrist (or finger) movement signals sampled at high frequency, used to infer sleep/wake state. Immobility is treated as probable sleep; movement interruptions as probable wakefulness.
2. **Photoplethysmography (PPG)**: optical heart rate and, in many modern devices, heart rate variability (HRV). PPG-derived beat-to-beat interval patterns differ between sleep stages and wakefulness, enabling more nuanced stage estimation than movement alone.

Some devices additionally incorporate skin temperature sensors and respiratory-rate estimates derived from PPG signal morphology. These multimodal inputs feed proprietary machine-learning classifiers that are not publicly disclosed by manufacturers [3, mechanism_review; 4, cohort].

From these inferred sleep/wake (and stage) sequences, the device computes its own TST and its own estimate of the sleep window (time in bed), then calculates SE. The key point: **SE from a wearable is a derivative of the device's own imperfect sleep/wake scoring**, not a direct measurement of sleep.

## The Core Tension: Wearables Struggle to Detect Quiet Wakefulness

The most consequential limitation of movement-based wearable sleep scoring — and the one that directly inflates SE estimates — is the inability to distinguish quiet wakefulness from sleep.

A person lying still in bed, fully awake but not moving, generates the same low-amplitude accelerometer signal as a sleeping person. Because actigraphy classifies immobility as sleep, prolonged motionless wakefulness is systematically scored as sleep epochs. This is the "quiet wakefulness" problem, first formally characterized by Paquet et al. (2007), who demonstrated that subjects were immobile approximately half the time when awake, and that actigraphy's specificity for correctly detecting wake epochs was only ~50%, even when sensitivity for sleep detection was approximately 95% [5, cohort].

This asymmetry — high sensitivity to sleep, low specificity for wake — is the defining accuracy pattern across wearable sleep trackers. The SLEEP journal 2021 study of seven consumer devices found epoch-by-epoch wake specificity ranging from 0.18 to 0.54, with Fitbit Alta HR the best performer at 0.54 and both Garmin devices the worst at 0.18–0.19 [4, cohort]. The 2019 JCSM validation of Fitbit Alta HR in adolescents (aged 15–19 years) found that the device overestimated WASO by up to 42 minutes (≤42 min) across three sleep-opportunity conditions compared to PSG [6, cohort].

The downstream effect on SE is direct: because WASO is underestimated (wakefulness misclassified as sleep), TST is inflated, and SE is overestimated. Danzig et al. (2020) found the Actiwatch overestimated SE by 6.8% and the Jawbone by 14.9% versus PSG, while underestimating WASO by 50.7 minutes [7, cohort]. In the multicenter 11-device study by Lee et al. (2023), the Google Pixel Watch showed a positive SE bias of approximately 12.8 percentage points above PSG [8, cohort].

This bias is not uniform: it worsens in populations with fragmented sleep. The more wake time a person accumulates in the night, the more the device misclassifies, and the larger the SE overestimate becomes [3, mechanism_review; 5, cohort]. PSG-validated reviews confirm the consistent pattern: wearables overestimate TST and underestimate WASO, yielding inflated SE, with the gap widening in insomnia and other sleep-disrupted populations [3, mechanism_review; 9, mechanism_review].

## What SE From a Wearable Can and Cannot Tell You

A wearable-derived SE reflects the device's estimate of sleep continuity across the inferred sleep window. For healthy sleepers with relatively consolidated sleep, the value will track reasonably well with PSG-derived SE across nights or weeks as a trend indicator. For nights with frequent nocturnal awakenings — insomnia, stress, illness, disrupted environments — the device will systematically undercount WASO, overcount TST, and return an SE that is measurably higher than what PSG would record.

A wearable SE of 90% may correspond to a PSG SE of 83% or to one of 73%, depending on how much quiet wakefulness occurred. This is not a trivial margin for clinical interpretation, but it does not nullify the metric's value for within-person longitudinal tracking: if a user's habitual wearable SE drops from 88% to 76% across two weeks, that signal likely reflects a real deterioration in sleep continuity even if the absolute calibration is uncertain.

SE remains one of the most interpretable outputs a consumer sleep device produces. Understood alongside its components and its known upward bias, it is a useful, if imprecise, window into how restorative the night was.

---

## Bibliography

1. American Academy of Sleep Medicine. *The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications*, Version 3. Darien, IL: AASM, 2023. https://aasm.org/clinical-resources/scoring-manual/ — tag: regulatory — tier: 1

2. Penzel T. Using the gold mine of sleep data recorded to increase our understanding of sleep. *Sleep*. 2024;47(7):zsae121. doi:10.1093/sleep/zsae121. PMID: 38776172 — tag: mechanism_review — tier: 2

3. de Zambotti M, Cellini N, Goldstone A, Colrain IM, Baker FC. Wearable sleep technology in clinical and research settings. *Med Sci Sports Exerc*. 2019;51(7):1538–1557. doi:10.1249/MSS.0000000000001947. PMID: 30789439 — tag: mechanism_review — tier: 2

4. Chinoy ED, Cuellar JA, Huwa KE, Jameson JT, Watson CH, Bessman SC, Hirsch DA, Cooper AD, Drummond SPA, Markwald RR. Performance of seven consumer sleep-tracking devices compared with polysomnography. *Sleep*. 2021;44(5):zsaa291. doi:10.1093/sleep/zsaa291. PMID: 33378539 — tag: cohort — tier: 2

5. Paquet J, Kawinska A, Carrier J. Wake detection capacity of actigraphy during sleep. *Sleep*. 2007;30(10):1362–1369. doi:10.1093/sleep/30.10.1362. PMID: 17969470 — tag: cohort — tier: 2

6. Lee XK, Chee NIYN, Ong JL, Teo TB, van Rijn E, Lo JC, Chee MWL. Validation of a consumer sleep wearable device with actigraphy and polysomnography in adolescents across sleep opportunity manipulations. *J Clin Sleep Med*. 2019;15(9):1337–1346. doi:10.5664/jcsm.7932. PMID: 31538605 — tag: cohort — tier: 2

7. Danzig R, Wang M, Shah A, Trotti LM. The wrist is not the brain: estimation of sleep by clinical and consumer wearable actigraphy devices is impacted by multiple patient- and device-specific factors. *J Sleep Res*. 2020;29(1):e12926. doi:10.1111/jsr.12926. PMID: 31621129 — tag: cohort — tier: 2

8. Lee T, Cho Y, Cha KS, Jung J, Cho J, Kim H, Kim D, Hong J, Lee D, Keum M, Kushida CA, Yoon IY, Kim JW. Accuracy of 11 wearable, nearable, and airable consumer sleep trackers: prospective multicenter validation study. *JMIR mHealth uHealth*. 2023;11:e50983. doi:10.2196/50983. PMID: 37917155 — tag: cohort — tier: 2

9. de Zambotti M, Goldstein C, Cook J, Menghini L, Altini M, Cheng P, Robillard R. State of the science and recommendations for using wearable technology in sleep and circadian research. *Sleep*. 2024;47(4):zsad325. doi:10.1093/sleep/zsad325. PMID: 38149978 — tag: mechanism_review — tier: 2
