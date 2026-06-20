# Section C: Measurement & Device Validity

## C.1 The Sensing Modality: ECG vs. PPG

Consumer wearables measure heart rate variability through a fundamentally different signal path than the clinical gold standard. The gold standard is the **electrocardiogram (ECG)**, which captures the cardiac electrical cycle directly; the interval between successive R-wave peaks (the R-R interval) is a precise timestamp of each heartbeat that is unaffected by the peripheral circulation [1, regulatory]. Consumer wearables — wrist bands, rings, and arm straps — predominantly use **photoplethysmography (PPG)**, an optical method that shines light into the skin and measures fluctuations in blood volume as each pulse wave passes through the capillary bed. What PPG detects is therefore the **pulse-to-pulse interval**, which reflects not only the timing of cardiac contraction but also the **pulse arrival time** — the delay introduced by arterial wall compliance, vascular tone, and the travel time of the pressure wave from the heart to the measurement site.

The metric derived from PPG is correctly called **pulse rate variability (PRV)**, not heart rate variability [2, cohort]. Under resting, controlled conditions in healthy individuals, PRV tracks ECG-derived HRV closely enough to be a useful surrogate. However, PRV and HRV are not interchangeable physiological measures. A large clinical study (n = 931, 60.9 years mean age, diverse chronic disease burden) found that PPG-derived PRV significantly underestimated SDNN, rMSSD, and pNN50 relative to ECG-derived HRV across cardiovascular, endocrine, and neurological patient groups — and concluded that "PPG-PRV is a poor surrogate for ECG-HRV" in diseased populations [3, cohort] (note: four of nine co-authors are employed by Tiger Tech Solutions, an ECG-device manufacturer; the study's specific SDNN divergence magnitudes await independent replication). The qualitative direction — PPG-PRV agreement degrades in non-sinus and clinically complex populations — is corroborated by independent sources [4, mechanism_review]. Even in healthy volunteers, PPG transient time delays can artificially inflate or shift parasympathetically-linked metrics such as rMSSD [4, mechanism_review].

## C.2 Why Validity Degrades with Motion and Higher Heart Rates

PPG accuracy has two well-characterized Achilles heels. First, **motion artifact**: skeletal muscle movement generates optical noise that corrupts the peak-detection step used to extract pulse intervals. Because HRV measures reflect very small interval differences (often 5–30 ms), even modest motion-artifact contamination that goes undetected produces spurious beat-to-beat intervals that inflate or deflate variability estimates. Second, **higher heart rates compress the R-R interval**, which narrows the margin for error in peak timing and reduces the signal-to-noise ratio for PPG-derived intervals. Both problems are compounded at the wrist — the dominant wearable placement — because the wrist experiences more movement artifact than the chest or finger and the arterial signal is weaker [2, cohort; 4, mechanism_review].

For these reasons, the research consensus is consistent: **PPG-derived HRV is most accurate during rest and sleep, and accuracy degrades progressively with exercise intensity** [5, mechanism_review; 6, cohort].

## C.3 Why rMSSD Is the Metric of Choice on Wearables

Among all HRV metrics, **rMSSD** (root mean square of successive differences) is the most robust under PPG conditions for two compounding reasons. First, rMSSD is computed from beat-to-beat differences rather than absolute interval length — a property that makes it less sensitive to slow drift in the pulse arrival time baseline, which shifts on the order of seconds and minutes rather than milliseconds. Second, rMSSD captures short-cycle (high-frequency, respiratory-linked) autonomic variation that manifests even in short measurement windows. Frequency-domain metrics such as LF/HF power and SDNN require longer, cleaner recordings and are substantially more sensitive to artifact and to the PPG timing biases described above [7, cohort; 3, cohort]. This is the direct mechanistic reason why **all major consumer wearable platforms — Oura, WHOOP, Apple Watch, Garmin, Polar — anchor their overnight HRV reporting to rMSSD** rather than SDNN or spectral measures.

## C.4 What the Independent Validation Literature Shows

A body of independent peer-reviewed validation studies has tested the agreement between consumer wearables and ECG reference standards. The overall pattern is: **good-to-excellent agreement for rMSSD and mean heart rate during sleep; clinically meaningful error at rest in some devices; substantial degradation during exercise.**

**Multi-device sleep laboratory study.** Miller, Sargent, and Roach (2022, Sensors; n = 53 healthy adults, Australian Institute of Sport funding; authors disclosed research support from WHOOP Inc.) compared six devices simultaneously against ECG during a single sleep laboratory night [8, cohort]. WHOOP 3.0 returned excellent rMSSD agreement (ICC = 0.99, bias −4.5 ± 3.9 ms). Apple Watch S6 (ICC = 0.67), Polar Vantage V (ICC = 0.65), and Oura Gen 2 (ICC = 0.63) each showed good agreement but with wider limits of variation. Garmin Forerunner 245 showed poor rMSSD agreement (ICC = 0.24). The WHOOP conflict of interest disclosure is material: the research group received support from WHOOP Inc., and the device's exceptional ICC should be interpreted with that in mind.

**Oura Ring, comprehensive analysis.** Cao et al. (2022, J Med Internet Res; n = 35 healthy participants, NSF-funded, no conflicts declared) conducted a comprehensive accuracy assessment of Oura nocturnal HR and HRV against a medical-grade chest ECG [7, cohort]. HR, rMSSD, AVNN, and pNN50 showed high positive correlations in 5-minute segments (Pearson r = 0.915 for rMSSD). Critically, accuracy was substantially higher for ring-provided dashboard values than for raw interbeat intervals, pointing to proprietary preprocessing as a meaningful variable. Frequency-domain parameters (LF, LF:HF ratio) showed high error rates in both test durations — consistent with the broader literature's caution about PPG-derived spectral metrics.

**Oura Ring, Sensors 2024.** Liang, Yilmaz, and Soon (2024, Sensors; n = 114 after quality-control exclusions, National Medical Research Council Singapore funded, no conflicts) showed that Oura rMSSD correlated strongly with ECG (r = 0.979 younger, 0.937 older participants) when a strict 80% validity-proportion filter was applied and measurement windows were extended to at least 30 minutes [9, cohort]. More than half of older participants exceeded 10% median absolute percentage error — underscoring clinically relevant individual variability.

**Multi-device nocturnal validation, 536 nights.** Dial et al. (2025, Physiological Reports; n = 13 healthy adults, 536 nights of simultaneous ECG and wearable data) evaluated Garmin Fenix 6, Oura Gen 3, Oura Gen 4, Polar Grit X Pro, and WHOOP 4.0 [10, cohort]. For HRV (rMSSD), Oura Gen 4 achieved the highest concordance (Lin's CCC = 0.99), followed by Oura Gen 3 (CCC = 0.97), WHOOP 4.0 (CCC = 0.94), Garmin (CCC = 0.87), and Polar Grit X Pro (CCC = 0.82). The study did not disclose industry funding.

**WHOOP validation.** Bellenger et al. (2021, Sensors; Australian Research Council + Australian Institute of Sport funded; one author's position was sponsored by WHOOP Inc. after data collection) found acceptable agreement between WHOOP PPG-derived HR and ECG, but for Ln rMSSD the bias and limits of agreement approached or exceeded the smallest worthwhile change for that variable (bias 1.66% ± 1.80%; LOA ±5.93%), leading the authors to recommend interpreting WHOOP-derived HRV changes against the device's own level of bias precision [11, cohort].

**Chest strap vs. wrist PPG vs. ECG in athletes.** Johansson et al. (2026, Frontiers in Physiology; no industry funding, n = 37 trained athletes) directly compared a Polar H10 chest strap, a smartphone camera PPG app, and ECG [6, cohort]. The Polar H10 — which samples the pulse from a chest electrode pad and transmits R-R intervals — showed near-perfect correlation with ECG for rMSSD (MAPE = 2.16%, r = 1.0). The PPG smartphone app remained strongly valid at rest (r = 0.95, MAPE = 17.49%) but with wider limits of agreement, illustrating the performance gap between chest-electrode and optical-wrist sensing.

## C.5 Consistency of Conditions Matters More Than Device Choice

A consistent finding across the validation literature is that **intra-device reliability within stable measurement conditions is generally good, but cross-device and cross-condition comparisons are unreliable**. Because each manufacturer applies proprietary peak-detection, artifact-rejection, and smoothing algorithms before computing the metric reported to the user, a rMSSD value from an Oura ring and a rMSSD value from a WHOOP band are not numerically equivalent even when measured simultaneously — they are outputs of different processing pipelines. Published multi-device studies routinely show absolute rMSSD differences of 5–30 ms between devices in the same night's sleep.

This has a direct practical implication: **switching devices mid-monitoring resets the baseline**. A user who tracks nocturnal rMSSD on one device, then switches to another, cannot interpret the change as a physiological signal. Similarly, measurement context — time of night, posture upon waking, recent alcohol, recent illness, sleep stage at awakening — produces variation of a similar magnitude to many between-day physiological differences. There is no universal reference standard or certified reference material in consumer HRV measurement analogous to the calibrators used in clinical laboratory assays.

**Artifact and ectopic beat correction** is a further data-quality variable. Consumer wearables vary substantially in how aggressively they filter anomalous beats. An ectopic beat (premature atrial or ventricular contraction) creates a spuriously short interval followed by a compensatory long interval; if unfiltered, this inflates rMSSD substantially. Wearable algorithms differ in their detection sensitivity; users are generally not informed of the artifact rate in a given recording.

## C.6 Regulatory Status

No major consumer HRV wearable — including Oura, WHOOP, Apple Watch (standard HRV mode), or Garmin — carries FDA clearance for HRV as a **diagnostic measurement**. These are wellness features. The Apple Watch has FDA clearance for specific cardiac applications (irregular rhythm notification, ECG lead-I capability in the ECG app), but the standard HRV/rMSSD wellness metric reported nightly is not within that clearance. The 1996 Task Force standards that established HRV measurement methodology were developed for clinical-grade ECG recordings, and their normative ranges do not map directly to PPG-derived consumer wearable outputs [1, regulatory].

---

## Bibliography

1. Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. Heart rate variability: standards of measurement, physiological interpretation and clinical use. *Circulation*. 1996;93(5):1043–1065. doi:10.1161/01.CIR.93.5.1043 — tag: regulatory — tier: 1

2. Lam E, Aratia S, Wang J, Tung J. Measuring Heart Rate Variability in Free-Living Conditions Using Consumer-Grade Photoplethysmography: Validation Study. *JMIR Biomed Eng*. 2020;5(1):e17355. doi:10.2196/17355 — tag: cohort — tier: 2

3. Kantrowitz AB, Ben-David K, Morris M, et al. Pulse rate variability is not the same as heart rate variability: findings from a large, diverse clinical population study. *Front Physiol*. 2025;16:1630032. doi:10.3389/fphys.2025.1630032 — tag: cohort — tier: 2

4. Burma JS, Griffiths JK, Lapointe AP, et al. Heart Rate Variability and Pulse Rate Variability: Do Anatomical Location and Sampling Rate Matter? *Sensors (Basel)*. 2024;24(7):2048. PMID: 38610260. doi:10.3390/s24072048 — tag: mechanism_review — tier: 2

5. Georgiou K, Larentzakis AV, Khamis NN, et al. Can Wearable Devices Accurately Measure Heart Rate Variability? A Systematic Review. *Folia Med (Plovdiv)*. 2018;60(1):7–20. PMID: 29668452. doi:10.2478/folmed-2018-0012 — tag: mechanism_review — tier: 2

6. Johansson H, Adderley E, Clarke S, McIntyre P, Reilly G, Caulfield B, Holden S. An observational study of the reliability and concurrent validity of heart rate variability devices in athletes. *Front Physiol*. 2026;16:1707318. PMID: 41574185. PMC: PMC12819663. doi:10.3389/fphys.2025.1707318 — tag: cohort — tier: 2

7. Cao R, Azimi I, Sarhaddi F, et al. Accuracy Assessment of Oura Ring Nocturnal Heart Rate and Heart Rate Variability in Comparison With Electrocardiography in Time and Frequency Domains: Comprehensive Analysis. *J Med Internet Res*. 2022;24(1):e27487. PMID: 35040799. doi:10.2196/27487 — tag: cohort — tier: 2

8. Miller DJ, Sargent C, Roach GD. A Validation of Six Wearable Devices for Estimating Sleep, Heart Rate and Heart Rate Variability in Healthy Adults. *Sensors (Basel)*. 2022;22(16):6317. PMID: 36016077. PMC: PMC9412437. doi:10.3390/s22166317 — tag: cohort — tier: 2

9. Liang T, Yilmaz G, Soon CS. Deriving Accurate Nocturnal Heart Rate, rMSSD and Frequency HRV from the Oura Ring. *Sensors (Basel)*. 2024;24(23):7475. PMID: 39686012. PMC: PMC11644394. doi:10.3390/s24237475 — tag: cohort — tier: 2

10. Dial MB, Hollander ME, Vatne EA, Emerson AM, Edwards NA, Hagen JA. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. *Physiol Rep*. 2025;13(16):e70527. PMID: 40834291. PMC: PMC12367097. doi:10.14814/phy2.70527 — tag: cohort — tier: 2

11. Bellenger CR, Miller DJ, Halson SL, Roach GD, Sargent C. Wrist-Based Photoplethysmography Assessment of Heart Rate and Heart Rate Variability: Validation of WHOOP. *Sensors (Basel)*. 2021;21(10):3571. PMID: 34065516. PMC: PMC8160717. doi:10.3390/s21103571 — tag: cohort — tier: 2
