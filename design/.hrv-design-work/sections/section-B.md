# Section B: Interpretation, Values & The Individual-Baseline Principle

## Why Population Reference Ranges Are Weak Guides for HRV

Heart rate variability is one of the most inter-individually variable measures in human physiology. Population normative data are useful for research framing but are genuinely poor guides for individual interpretation — and understanding why is the foundation of using HRV well.

The Lifelines Cohort Study (n = 84,772) quantified this dramatically [1, cohort]. Median rMSSD at age 13–14 was ~66–67 ms in both sexes; by age 75+ it had fallen to ~16 ms in women and ~15 ms in men — a greater than four-fold decline across the lifespan. The interquartile spread at any given age decade is similarly enormous: across healthy adults in their 30s and 40s, rMSSD values spanning roughly 20–100+ ms all fall within the plausible healthy range. Van den Berg et al., analysing 13,943 ECGs from ages 11 days to 91 years, confirmed this progressive decline from childhood through middle age and found sex differences modest in magnitude but real in the reproductive years (women slightly higher in the 20–45 bracket, converging after 60) [2, cohort]. The Task Force standards established the foundational time- and frequency-domain metrics but did not and could not resolve inter-individual spread into a single actionable cutoff [3, regulatory].

The practical implication is blunt: a 38-year-old with a resting rMSSD of 28 ms may be perfectly healthy; a 38-year-old with a resting rMSSD of 80 ms may be perfectly healthy. Calling either of those values "low" or "high" relative to a population table tells you little. What matters is whether either person has moved substantially away from *their own* stable baseline.

## The Actionable Signal: Personal Baseline + Deviation from It

Because inter-individual spread dwarfs within-person day-to-day variation, the operative HRV signal for a healthy individual is their rolling personal baseline and the day-to-day deviation from it [4, mechanism_review]. Buchheit (2014) framed this precisely: a single HRV recording is "highly susceptible to transient fluctuations caused by daily stressors, disruptions in sleep, environmental factors, and measurement inconsistencies," making isolated readings unreliable for tracking meaningful physiological change [4, mechanism_review]. A minimum of roughly one week of consecutive data is needed to establish a person's homeostatic baseline; once established, the actionable question becomes not "is this value above 50 ms?" but "is today's value depressed relative to *my* usual level?"

Consumer wearable platforms operationalize this as a personalized readiness or recovery flag — computing a rolling 7–30 day rMSSD average and flagging days where the current reading falls meaningfully below that individual window. This is the correct framework: Nuuttila et al. (2024) found that while morning and nocturnal HRV recordings tracked similarly over longer periods, their short-term day-to-day responses to training loads were not interchangeable, emphasizing that trend trajectory within a person's dataset is the signal worth reading [5, cohort].

A useful quantitative anchor for normal within-person fluctuation: rMSSD's coefficient of variation (CV) in field measurements is approximately 12% — substantially lower than spectral indices (LF/HF ratio CV ≈ 82%) — making it the most reliable time-domain metric for day-to-day tracking [4, mechanism_review]. The corollary: a single reading ~12–15% below a person's rolling mean might be noise; a sustained multi-day depression of 20–30% below that mean is a plausible signal of inadequate recovery, illness, or excessive training load. No fixed millisecond cutoff captures this; the deviation-from-baseline framing does.

## Measurement Consistency Is Not Optional

HRV is exquisitely sensitive to conditions that have nothing to do with recovery or health status: time of day, body posture, recent food, caffeine, alcohol, ambient temperature, and breathing pattern all shift rMSSD by meaningful amounts. A reading taken supine immediately after waking will differ from one taken upright after coffee. This is not measurement error — it is genuine physiology — but it makes within-person comparisons across inconsistent conditions uninformative or actively misleading [5, cohort; 6, cohort].

For trend validity, the key rules are:

- **Same time of day.** Morning (upon waking, before caffeine or food) is the most widely validated window for day-to-day training and recovery monitoring [4, mechanism_review]. Nocturnal wearable recordings during sleep are an alternative — Nuuttila et al. (2024) found they captured training responses — but morning and nocturnal values respond to acute stressors on different timescales and should not be mixed in the same trend series [5, cohort].
- **Same posture and state.** Supine or seated immediately after waking, before activity. Postural shift from supine to standing reduces HRV via baroreflex activation; comparing supine vs. seated readings conflates condition with signal.
- **Same device and algorithm.** Johansson et al. (2026) confirmed strong intra-session reliability within a device (ICC 0.83–0.90) but demonstrated that algorithm differences between platforms account for meaningful measurement variance [6, cohort]. Swapping devices mid-series resets the baseline.
- **Consistent recording duration.** Ultra-short recordings (30 s) are less stable than 5-minute recordings; consumer devices standardize this internally, but switching between app-based and device-native protocols changes the effective window.

Breaking any of these creates noise that can exceed the within-person day-to-day variation the metric is trying to detect.

## Why Proprietary HRV Scores Are Not Interchangeable Across Brands

Commercial wearables — Oura, WHOOP, Garmin, Polar — all report HRV but compute it via proprietary algorithms that differ in sensor type (ECG vs. PPG), sampling window (e.g., WHOOP uses a weighted average across the whole sleep period with greater weight on slow-wave sleep; Garmin Fenix 6 reports the lowest 30-minute average over 24 hours; Polar Grit X Pro uses the first 4 hours of sleep), artifact filtering, interpolation of missing data, and normalization [7, cohort]. These are not minor implementation details: the same physiological state produces systematically different numeric outputs on different devices.

Dial et al. (2025) found Oura Gen 4 achieved the highest nocturnal HRV accuracy against ECG reference (CCC = 0.99, MAPE ≈ 6%), while Polar showed substantially lower concordance (CCC = 0.82, MAPE ≈ 16%) [7, cohort]. The npj Cardiovascular Health guide to consumer wearables notes that manufacturers provide variable transparency — some publish white papers on their algorithms, others (notably WHOOP) offer "non-specific definitions of HRV" in public documentation [8, mechanism_review]. A numeric HRV value from one brand cannot be compared to the same number from another. Switching devices should be treated as restarting a baseline, not continuing a trend.

## Summary Principle

HRV has no single actionable "normal" cutoff because inter-individual spread and age-related decline are far larger than the signal of interest. The evidence base supports one framing: establish the individual's rolling baseline (7–30 days of consistent morning or nocturnal recordings on the same device in the same conditions), then monitor for sustained deviations from that baseline. A single isolated reading, evaluated against a population table, is nearly uninterpretable. The trend is the signal.

---

## Bibliography

1. Tegegne BS, Man T, van Roon AM, Snieder H, Riese H. Reference values of heart rate variability from 10-second resting electrocardiograms: the Lifelines Cohort Study. *Eur J Prev Cardiol*. 2020;27(19):2191–2194. doi:10.1177/2047487319872567. PMID: 31500461 — tag: cohort — tier: 1

2. van den Berg ME, Rijnbeek PR, Niemeijer MN, Hofman A, van Herpen G, Bots ML, Hillege H, Swenne CA, Eijgelsheim M, Stricker BH, Kors JA. Normal Values of Corrected Heart-Rate Variability in 10-Second Electrocardiograms for All Ages. *Front Physiol*. 2018;9:424. doi:10.3389/fphys.2018.00424. PMID: 29755366 — tag: cohort — tier: 2

3. Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. Heart rate variability: standards of measurement, physiological interpretation and clinical use. *Circulation*. 1996;93(5):1043–1065. doi:10.1161/01.CIR.93.5.1043. PMID: 8598068 — tag: regulatory — tier: 1

4. Buchheit M. Monitoring training status with HR measures: do all roads lead to Rome? *Front Physiol*. 2014;5:73. doi:10.3389/fphys.2014.00073. PMID: 24578692 — tag: mechanism_review — tier: 2

5. Nuuttila OP, Kyröläinen H, Kokkonen VP, Uusitalo A. Morning versus Nocturnal Heart Rate and Heart Rate Variability Responses to Intensified Training in Recreational Runners. *Sports Med Open*. 2024;10(1):115. doi:10.1186/s40798-024-00779-5. PMID: 39503915 — tag: cohort — tier: 2

6. Johansson H, Adderley E, Clarke S, McIntyre P, Reilly G, Caulfield B, Holden S. An observational study of the reliability and concurrent validity of heart rate variability devices in athletes. *Front Physiol*. 2026;16:1707318. doi:10.3389/fphys.2025.1707318. PMID: 41574185 — tag: cohort — tier: 2

7. Dial MB, Hollander ME, Vatne EA, Emerson AM, Edwards NA, Hagen JA. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. *Physiol Rep*. 2025;13(16):e70527. doi:10.14814/phy2.70527. PMID: 40834291 — tag: cohort — tier: 2

8. Jamieson A, Chico TJA, Jones S, et al. A guide to consumer-grade wearables in cardiovascular clinical care and population health for non-experts. *npj Cardiovasc Health*. 2025;2:44. doi:10.1038/s44325-025-00082-6. PMID: 40909206 — tag: mechanism_review — tier: 2
