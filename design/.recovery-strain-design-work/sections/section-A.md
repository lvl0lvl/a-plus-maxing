# Section A — What Recovery/Strain Scores Are & What the Device Computes

## The Load-Bearing Frame

Wearable recovery and strain scores are **derived, proprietary composite indices** — algorithmic aggregations of underlying physiological signals, not direct measurements of any single physiological quantity. Each device brand applies an undisclosed weighting algorithm and outputs its own numerical scale. The scores from WHOOP, Oura, Garmin, and Polar are therefore **not interchangeable across brands**: a WHOOP Recovery of 75% and an Oura Readiness of 75 may reflect meaningfully different computational interpretations of overlapping but non-identical raw inputs [1, mechanism_review; 2, mechanism_review].

The underlying signals feeding these composites — nocturnal heart rate variability (HRV), resting heart rate (RHR), sleep duration and architecture, respiratory rate, and (in some devices) skin temperature — are separately validated physiological markers [3, cohort; 4, cohort]. The composite score is the brand's proprietary interpretation layer on top of those validated signals. Users and practitioners should reason from the underlying metrics when possible and treat the composite as a convenience index, not a gold-standard measurement.

---

## The Two Poles: Recovery/Readiness vs. Strain/Load

### Recovery and Readiness Scores

Recovery and readiness scores estimate **how physiologically prepared the body is to handle a training or performance demand**, primarily by sampling the autonomic nervous system's state during sleep — the window in which external confounders (posture, food, emotion, recent movement) are minimized.

**Brand instances and scales:**

- **WHOOP Recovery (0–100%)**: Displayed as Green (67–100%), Yellow (34–66%), or Red (0–33%). Computed from nocturnal HRV (rMSSD via photoplethysmography, PPG), resting heart rate, sleep performance (duration, efficiency, debt), and respiratory rate. WHOOP samples HRV during slow-wave sleep and averages across the full overnight period.
- **Oura Readiness Score (1–100)**: Combines nocturnal RHR, HRV balance (rolling average comparison), sleep score, recovery index, body temperature deviation, activity balance, and previous-day activity. The scale's individual contributors are reported alongside the headline score.
- **Garmin Body Battery (0–100) + Training Readiness**: Body Battery tracks energy reserves across the day, falling with exertion and stress (derived from HRV-based stress score) and rising with sleep. Training Readiness integrates recovery time, sleep score, HRV status, and training load history into a readiness-to-train rating.
- **Polar Nightly Recharge / Recovery Pro**: The "ANS charge" parameter aggregates nocturnal HR, HRV, and breathing rate into a nightly ANS recovery index; Sleep Charge adds total sleep time and continuity. A prospective training study found that ANS charge and changes in sleep-period HRV were associated with subsequent performance adaptations in runners [5, cohort].
- **Apple Watch** (watchOS ≥ 10) does not produce a named recovery score but reports nocturnal RHR, overnight HRV, and sleep duration as discrete metrics for the user to interpret.
- **Fitbit Daily Readiness Score** is calculated from HRV (electrodermal activity in some models), sleep, and recent activity.

**The autonomic basis.** Nocturnal RHR and HRV are the load-bearing inputs. Nuuttila et al. (2022) demonstrated in recreational runners that overnight HRV indices (lnRMSSD, lnHF) are highly reliable across nights (ICC 0.92–0.97 for LnRMSSD; 0.91–0.96 for LnHF) and are sensitive to maximal exercise, with RHR rising and HRV falling most systematically in the full-night recording window — the same window wearables typically sample [6, cohort]. This provides the physiological rationale for overnight sampling as the composite's primary inputs.

### Strain and Load Scores

Strain and load scores estimate **the cumulative cardiovascular and physical demand placed on the body** during activity or across a full day, drawing on continuous HR monitoring and time-in-zone calculations.

**Brand instances and scales:**

- **WHOOP Strain (0–21, logarithmic)**: Scores cardiovascular output continuously by allocating weighted credit for time spent in HR zones derived from each user's individualized heart rate reserve. The scale is logarithmic: the jump from 15 to 16 requires proportionally more cardiac work than the jump from 5 to 6. An "All Out" effort (21) is physiologically rare. Bellenger et al. (2022) note explicitly that "the validity of this metric is presently unknown" and recommend cautious interpretation [7, cohort].
- **Garmin Training Load / Acute Load**: Uses time-in-HR-zones (Edwards-style summated heart rate zones) to calculate training load in arbitrary units, then compares acute to chronic load to flag overreaching risk.
- **Polar Training Load Pro**: Cardio load derived from HR zones during sessions, expressed in a proprietary unit and tracked against recovery time.

These proprietary load scores are algorithmic relatives of validated research constructs. **Training Impulse (TRIMP)** — proposed by Banister et al. and refined across decades — weights session duration by a HR-zone exponential factor and has strong correlations with session RPE [8, mechanism_review]. The **Acute:Chronic Workload Ratio (ACWR)**, which compares 7-day rolling load to 28-day baseline load, has been studied as an injury-risk indicator in team sports, though its predictive validity remains contested [9, cohort]. Consumer wearable strain metrics draw on these frameworks but apply undisclosed parameterizations, making direct equivalence to research TRIMP calculations impossible without manufacturer transparency.

---

## Input Signals and Their Validation Status

| Signal | Validated? | Key evidence |
|---|---|---|
| Nocturnal HRV (rMSSD) | Yes — WHOOP 4.0: CCC 0.94 vs ECG; Oura Gen 4: CCC 0.99 vs ECG | Dial et al. 2025 [3, cohort] |
| Nocturnal RHR | Yes — Oura Gen 3: CCC 0.97, MAPE 1.67%; WHOOP 4.0: CCC 0.91, MAPE 3.00% | Dial et al. 2025 [3, cohort] |
| Sleep detection (2-state) | Moderate — ~86–89% agreement with PSG across brands | Miller et al. 2022 [4, cohort] |
| Respiratory rate (RR) | PPG-derived; device-dependent accuracy; less independently validated than HRV/RHR | — |
| Composite Recovery/Readiness | Algorithm undisclosed; individual inputs validated, composite correlation with performance equivocal | Bellenger et al. 2021 [10, cohort] |
| Composite Strain/Load | Validity "presently unknown" for WHOOP Strain; no independent peer-reviewed validation as of 2025 | Bellenger et al. 2022 [7, cohort] |

---

## Non-Interchangeability Across Devices

Even when two devices agree on the raw HRV or RHR number, their composite scores are not comparable. Grosicki & Presby (2025) identify three axes of non-equivalence: metric definitions (e.g., RMSSD vs. SDNN vs. pNN50), temporal sampling windows (e.g., full night vs. a specific sleep stage), and data-averaging procedures [2, mechanism_review]. Dial et al. (2025) demonstrated that WHOOP 4.0 and Polar Grit X Pro both showed lower HRV concordance with ECG than Oura devices (WHOOP CCC 0.94 MAPE 8.17%; Polar CCC 0.82 MAPE 16.32%), meaning devices differ not only in their algorithms but in the fidelity of their raw inputs [3, cohort].

The clinical corollary: a practitioner should not substitute one brand's recovery score for another's, should not treat absolute values as population-standardized references, and should interpret trends within the same device for the same individual over time rather than cross-device or cross-person comparisons.

---

## Bibliography

1. Jamieson A, Chico TJA, Jones S, Chaturvedi N, Hughes AD, Orini M. A guide to consumer-grade wearables in cardiovascular clinical care and population health for non-experts. *npj Cardiovascular Health*. 2025; PMID: 40909206; PMC12404996. DOI: 10.1038/s44325-025-00082-6. — tag: mechanism_review — tier: 3

2. Grosicki GJ, Presby DM. Accurate comparison of wearables requires contextual equivalence. *Physiological Reports*. 2025; PMID: 41388834; PMC12701519. — tag: mechanism_review — tier: 3

3. Dial MB, Hollander ME, Vatne EA, Emerson AM, Edwards NA, Hagen JA. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. *Physiological Reports*. 2025; PMID: 40834291; PMC12367097. — tag: cohort — tier: 2

4. Miller DJ, Sargent C, Roach GD. A validation of six wearable devices for estimating sleep, heart rate and heart rate variability in healthy adults. *Sensors (Basel)*. 2022;22(16):6317. PMID: 36016077; PMC9412437. COI: WHOOP Inc. research support — tag: cohort — tier: 2

5. Nuuttila OP, Schäfer Olstad D, Martinmäki K, Uusitalo A, Kyröläinen H. Monitoring sleep and nightly recovery with wrist-worn wearables: links to training load and performance adaptations. *Sensors (Basel)*. 2025;25(2):533. PMID: 39860902. — tag: cohort — tier: 2

6. Nuuttila OP, Seipäjärvi S, Kyröläinen H, Nummela A. Reliability and sensitivity of nocturnal heart rate and heart-rate variability in monitoring individual responses to training load. *International Journal of Sports Physiology and Performance*. 2022;17(8):1296–1303. PMID: 35894977. DOI: 10.1123/ijspp.2022-0145. — tag: cohort — tier: 2

7. Bellenger CR, Miller DJ, Halson SL, Roach GD, Maclennan M, Sargent C. Evaluating the typical day-to-day variability of WHOOP-derived heart rate variability in Olympic water polo athletes. *Sensors (Basel)*. 2022;22(18):6723. PMID: 36146073; PMC9505647. COI: authors received research support from WHOOP Inc. — tag: cohort — tier: 2

8. Halson SL. Monitoring training load to understand fatigue in athletes. *Sports Medicine*. 2014;44 Suppl 2:S139–S147. PMID: 25200666. [Training impulse / TRIMP framework review] — tag: mechanism_review — tier: 3

9. Arazi H, Asadi A, Khalkhali F, Boullosa D, Hackney AC, Granacher U, Zouhal H. Association between the acute to chronic workload ratio and injury occurrence in young male team soccer players: a preliminary study. *Frontiers in Physiology*. 2020; PMID: 32670083; PMC7327085. — tag: cohort — tier: 2

10. Bellenger CR, Miller DJ, Halson SL, Roach GD, Sargent C. Wrist-based photoplethysmography assessment of heart rate and heart rate variability: validation of WHOOP. *Sensors (Basel)*. 2021;21(10):3571. PMID: 34065516; PMC8160717. COI: independent validation; ARC/AIS-funded (not WHOOP-funded) — tag: cohort — tier: 2
