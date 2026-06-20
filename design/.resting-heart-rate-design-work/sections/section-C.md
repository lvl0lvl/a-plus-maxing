# Section C: Measurement & Device Validity

## PPG vs. ECG: The Physics of Wrist-Based Heart Rate

Consumer wearables derive heart rate through **photoplethysmography (PPG)** — one or more LEDs (typically green, sometimes red or infrared) illuminate the skin at the wrist, and a photodetector measures the pulse of reflected light that varies with blood-volume changes in the capillaries. This is fundamentally different from **electrocardiography (ECG)**, which records the electrical impulse that triggers each cardiac contraction and is the clinical gold standard for heart rate and rhythm.

The key practical implication: **at rest and during sleep, wrist PPG-derived heart rate is highly accurate**. When the body is still, motion artifacts are absent, perfusion is relatively stable, and the algorithm only needs to identify the average interval between optical pulses — it does not need to resolve the precise timing of individual R-R intervals (which is what HRV requires). A 2024 daily-life validation study compared PPG devices against ambulatory ECG in 25 healthy volunteers across 10 days and found heart rate mean absolute error under 1 bpm during sleep, with Spearman correlations of 0.96–0.98 across the full day [1, cohort]. This resting-HR use case is where consumer PPG performs at its best.

By contrast, **accuracy degrades substantially with movement and rising heart rate**. The same study found walking increased HR error approximately 10% over non-walking conditions [1, cohort]. A 2025 device-validation study found wrist-worn devices showed MAE of 6.41 bpm versus 1.43 bpm for an arm-worn sensor, with the wrist device's within-subject coefficient of variation rising to 23.03% during lying-down transitions where motion or postural vascular changes disrupted the signal [2, cohort]. An analysis of 53 participants across six Fitzpatrick skin-tone categories found that mean absolute error during physical activity averaged 30% higher than at rest, and that rhythmic, repetitive movements like walking caused devices to misidentify the periodic motion signal as heart rate — a phenomenon termed signal crossover [3, cohort].

The 2019 Nelson & Allen 24-hour intraindividual validation study (Apple Watch Series 3 and Fitbit Charge 2 vs. ambulatory ECG) is an early but frequently cited real-world reference: at sleep, MAPE was 3.1–3.4%; during running it rose to 3.0–9.9%; during general activities of daily living it reached 9.2–13.7% [4, cohort]. A 2022 systematic review of 9 studies across 15 devices from 7 brands found Apple Watch MAPE for heart rate ranged 1–7%, while Fitbit devices ranged 2.4–17% depending on activity [5, mechanism_review].

The practical summary: **for the resting-HR use case, wrist PPG is a fit-for-purpose tool** — real-world MAE at rest or during sleep is consistently in the 1–5 bpm range across modern devices, which is adequate for trend tracking, cardiovascular fitness monitoring, and lifestyle applications. It is not a diagnostic instrument, and accuracy degrades meaningfully during exercise.

## Skin Tone, Perfusion, Wrist Fit, and Artifact Sources

Three physical factors govern PPG signal quality beyond motion: **skin pigmentation, tissue perfusion, and optical coupling**.

**Skin tone** is the most clinically important equity concern. Melanin, concentrated in the epidermis, preferentially absorbs green light — the wavelength used by most wrist PPG sensors — which reduces signal amplitude in darker skin tones. A 2025 prospective study of Fitbit Charge 5 vs. Polar H10 reference across three skin-tone groups found no significant between-group difference at rest (~2.8 bpm across all groups), but substantial divergence during exercise: at moderate-to-high intensity, dark skin-tone participants showed mean errors of 14.6–16.5 bpm versus 4 bpm in the light skin-tone group — a fourfold disparity [6, cohort]. A 2025 cross-sectional study of Garmin Forerunner 45 found no statistically significant main effect of Fitzpatrick score on resting or steady-state accuracy, but noted higher PPG readings in darker skin tones during exercise intensity ramps [7, cohort]. A 2022 systematic review of 10 studies (469 participants) found that 4 of 10 reported a statistically significant reduction in heart rate accuracy in darker skin tones, 4 found no significant difference, and 2 showed mixed results — reflecting genuine heterogeneity in study design and activity conditions [11, mechanism_review].

**For resting-HR specifically**, the skin-tone effect is smallest: the Hung et al. data shows convergence at rest. The disparity is most clinically relevant during exercise-derived metrics; however, given that some device RHR algorithms sample brief daytime resting windows rather than solely nocturnal data, the skin-tone interaction warrants disclosure.

Other documented accuracy factors: **tattoos** over the measurement site reduce signal amplitude by absorbing or scattering LED light; **perfusion state** (cold hands, vasoconstriction, low blood pressure) reduces the optical pulse amplitude and increases noise; **wrist fit** (band tightness and position relative to the ulnar artery) affects coupling quality, though one study found no significant wrist circumference × accuracy interaction for sizes above vs. below 15.5 cm.

## The Resting-HR Definition Problem: Cross-Device Non-Interchangeability

A critical and frequently overlooked validity issue: **consumer devices do not agree on what "resting heart rate" means**, and the derived metric is not directly interchangeable across devices or even across firmware updates on the same device.

Documented proprietary approaches include:

- **Nocturnal minimum:** the single lowest heart rate recorded during the overnight sleep window (used by some Garmin and Fitbit algorithms in some configurations)
- **Lowest-N-minute average:** the mean heart rate of the lowest-30-minute or lowest-60-minute rolling window during sleep (approaches used by Oura and others)
- **Daytime resting windows:** brief sedentary daytime periods identified by accelerometry, averaged across the day
- **Morning measurement prompts:** some devices present an early-morning seated reading to the user as the "resting" value

A 2023 analysis of wrist-worn device RHR computations in over 92,000 participants documented mean RHR values ranging from 40–109 bpm across devices, with nighttime values averaging 4 bpm lower than daytime values in the same individuals — an entirely algorithm-defined gap [8, cohort]. COI: all authors employed by Google/Alphabet. Heart rate stabilized within ~4 minutes of inactivity in most participants, and over 53% of daily HR minima occurred between 03:00–07:00, meaning nocturnal algorithms and daytime algorithms capture systematically different physiological windows.

A 2024 validation study of the Verily Study Watch against simultaneous ECG in 875 participants found ICC = 0.946 and mean bias of 0.76 bpm for the VSW's PPG-derived RHR — strong agreement with ECG when the algorithm excludes motion-artifact intervals using actigraphy [9, cohort]. COI: multiple authors are Verily employees with equity ownership; study funded by Verily Life Sciences.

**Practical implication for trend analysis:** a user who switches devices mid-longitudinal tracking — from a Garmin to an Apple Watch to an Oura Ring — is effectively switching RHR definitions. Observed week-over-week changes may reflect algorithm differences rather than physiological change. Within-device consistency of conditions (same device, same posture, same measurement time, equivalent sleep duration) is a prerequisite for valid trend inference.

## Wellness Device vs. Medical Device: Regulatory and Clinical Scope

The majority of consumer wrist PPG devices marketed for resting-HR monitoring are **general wellness products** under FDA guidance — not cleared medical devices. This means their heart-rate accuracy claims are not subject to mandatory FDA premarket review, and published accuracy data comes from independent researchers rather than regulatory submissions.

A subset of consumer devices have received **FDA De Novo clearance or 510(k) clearance** for specific medical-grade features. The Apple Watch ECG app received De Novo clearance in 2018 for single-lead ECG recording and AF/sinus-rhythm classification; the KardiaMobile received 510(k) clearance for single-lead ECG. A 2025 validation study of four consumer AF-detection wearables (KardiaMobile 6L, Apple Watch ECG, FibriCheck PPG app, Preventicus PPG app) found sensitivity of 100% and specificity of 96.4–98.9% for AF detection, with 7.4–14.8% of readings requiring re-attempts due to insufficient signal quality [10, cohort].

These FDA-cleared features are specifically for rhythm classification (AF vs. sinus), not for continuous resting-HR accuracy certification. The general continuous PPG heart rate function in the same watches remains a wellness feature. Users and clinicians should not infer that FDA clearance of an ECG feature validates the device's PPG-derived resting-HR accuracy.

**Reproducibility and test-retest:** because device algorithms apply proprietary artifact rejection, smoothing, and coverage thresholds, between-session reproducibility is hardware- and algorithm-specific. The Rehman et al. (2024) Sensors study noted median PPG coverage of 44–52% over full waking days versus 77–88% during sleep — meaning on many measurement days, a substantial fraction of the waking-day HR record is discarded by the algorithm, and the final RHR scalar represents a non-random sample of the day [1, cohort]. COI: all authors are Janssen R&D employees. This selective coverage is rarely disclosed to the end user and can affect day-to-day reproducibility independently of any true physiological change.

---

## Bibliography

1. Rehman RZU, Chatterjee M, Manyakov NV, et al. Assessment of Physiological Signals from Photoplethysmography Sensors Compared to an Electrocardiogram Sensor: A Validation Study in Daily Life. *Sensors (Basel)*. 2024;24(21):6826. PMID: 39517723. DOI: 10.3390/s24216826. COI: all authors employed by Janssen Research & Development. — tag: cohort — tier: 3

2. Schweizer T, Gilgen-Ammann R. Wrist-Worn and Arm-Worn Wearables for Monitoring Heart Rate During Sedentary and Light-to-Vigorous Physical Activities: Device Validation Study. *JMIR Cardio*. 2025;9:e67110. PMID: 40116771. DOI: 10.2196/67110. COI: none declared. — tag: cohort — tier: 3

3. Bent B, Goldstein BA, Kibbe WA, Dunn JP. Investigating sources of inaccuracy in wearable optical heart rate sensors. *NPJ Digit Med*. 2020;3:18. PMID: 32047863. DOI: 10.1038/s41746-020-0226-6. COI: none declared. — tag: cohort — tier: 2

4. Nelson BW, Allen NB. Accuracy of Consumer Wearable Heart Rate Measurement During an Ecologically Valid 24-Hour Period: Intraindividual Validation Study. *JMIR Mhealth Uhealth*. 2019;7(3):e10828. PMID: 30855232. DOI: 10.2196/10828. COI: none declared. Note: single-participant intraindividual design; findings are illustrative, not population-generalizable. — tag: cohort — tier: 3

5. Germini F, Noronha N, Borg Debono V, et al. Accuracy and Acceptability of Wrist-Wearable Activity-Tracking Devices: Systematic Review of the Literature. *J Med Internet Res*. 2022;24(1):e30791. PMID: 35060915. DOI: 10.2196/30791. COI: none declared. — tag: mechanism_review — tier: 2

6. Hung SH, Serwa K, Rosenthal G, Eng JJ. Validity of heart rate measurements in wrist-based monitors across skin tones during exercise. *PLoS One*. 2025;20(2):e0318724. PMID: 39928630. DOI: 10.1371/journal.pone.0318724. COI: none declared; funded by Canada Research Chairs Program and CIHR. — tag: cohort — tier: 3

7. Icenhower E, Murphy C, Brooks J, Irby T, N'dah J, Robison C, Fanning J. Investigating the accuracy of Garmin PPG sensors on differing skin types based on the Fitzpatrick scale: cross-sectional comparison study. *Front Digit Health*. 2025. DOI: 10.3389/fdgth.2025.1553565. COI: none declared; partial support from Wake Forest University Claude D. Pepper Older Americans Independence Center (P30-AG21332). — tag: cohort — tier: 3

8. Speed C, Arneil T, Harle R, Wilson A, Karthikesalingam A, McConnell M, Phillips J. Measure by measure: Resting heart rate across the 24-hour cycle. *PLOS Digit Health*. 2023;2(4):e0000236. PMID: 37115739. DOI: 10.1371/journal.pdig.0000236. COI: all authors are Google/Alphabet employees with stock options; study funded by Google. — tag: cohort — tier: 3

9. Feng KY, Short SA, Saeb S, et al. Resting Heart Rate and Associations With Clinical Measures From the Project Baseline Health Study: Observational Study. *J Med Internet Res*. 2024;26:e60493. PMID: 39705694. DOI: 10.2196/60493. COI: multiple authors hold Verily employment and equity; study funded by Verily Life Sciences. — tag: cohort — tier: 3

10. Wouters F, Gruwez H, Smeets C, et al. Comparative Evaluation of Consumer Wearable Devices for Atrial Fibrillation Detection: Validation Study. *JMIR Form Res*. 2025;9:e65139. PMID: 39791483. DOI: 10.2196/65139. COI: none declared; FibriCheck device provided by Qompium NV. — tag: cohort — tier: 3

11. Koerber D, Khan S, Shamsheri T, Kirubarajan A, Mehta S. Accuracy of Heart Rate Measurement with Wrist-Worn Wearable Devices in Various Skin Tones: a Systematic Review. *J Racial Ethn Health Disparities*. 2022 Nov 14. PMID: 36376641. DOI: 10.1007/s40615-022-01446-9. COI: none declared. — tag: mechanism_review — tier: 2
