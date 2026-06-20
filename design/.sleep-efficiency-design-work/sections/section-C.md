## C. Measurement & Device Validity vs Polysomnography

### C.1 Polysomnography: The Reference Standard

Polysomnography (PSG) is the established clinical and research reference standard for measuring sleep [1, regulatory]. During an attended overnight study, electroencephalography (EEG), electro-oculography (EOG), and chin electromyography (EMG) are recorded continuously and scored in sequential 30-second epochs according to the AASM Manual for the Scoring of Sleep and Associated Events (current version 3, February 2023) [1, regulatory]. Each epoch receives one of five stage assignments: Wake (W), N1, N2, N3, or REM. Sleep efficiency (SE) is then computed as TST ÷ TIB × 100%, where total sleep time (TST) = the sum of all non-wake epochs and time in bed (TIB) = the interval from lights-out to the end of the recording. Wake after sleep onset (WASO) is scored from the summed wake epochs that fall between sleep onset and final awakening. This epoch-level EEG-based scoring is what consumer wearables must ultimately approximate.

### C.2 How Consumer Wearables Estimate Sleep

Modern consumer sleep trackers — Oura, Fitbit, WHOOP, Apple Watch, Garmin — use one or more of three sensor modalities: wrist or finger accelerometry (detects body movement), photoplethysmography (PPG, detects heart-rate and heart-rate variability via an optical sensor), and skin temperature. Earlier generation devices relied almost exclusively on accelerometry; current generation devices combine PPG-derived HRV features with motion data and, in some cases, temperature signals [2, cohort; 5, mechanism_review]. All scoring is performed by proprietary machine-learning algorithms that are not publicly disclosed, which limits direct cross-device comparisons and reproducibility of research findings [5, mechanism_review].

### C.3 The Canonical Asymmetry: High Sleep Sensitivity, Low Wake Specificity

The single most robust and consistent finding across independent validation studies is an asymmetry between sensitivity for sleep and specificity for wake detection. Because quiet wakefulness (lying still in the dark) is often indistinguishable from light sleep in an accelerometry or PPG signal, wearables systematically classify motionless-wake epochs as sleep.

Chinoy et al. conducted the most-cited multi-device laboratory validation in the US, comparing seven consumer devices against in-lab PSG across two nights in 42 healthy adults [2, cohort]. Epoch-by-epoch results showed all devices achieved sleep-detection sensitivity ≥ 0.93 across the sample. Wake-detection specificity, however, ranged from 0.18 (Garmin Fenix 5S) to 0.54 (Fitbit Alta HR). The downstream consequence was substantial and device-specific overestimation of TST and SE, with WASO underestimation: the Garmin Vivosmart 3 overestimated TST by +46.8 min and SE by +10.1%, while underestimating WASO by −47.6 min; the Fitbit Alta HR performed far better at +2.6 min TST bias, +0.9% SE bias, −2.1 min WASO bias [2, cohort].

Haghayegh et al. performed a systematic review and meta-analysis of all published Fitbit validation studies against PSG through 2019 [3, meta_analysis]. Across earlier-generation (motion-only) Fitbit models, sensitivity for sleep ranged 0.87–0.99 while specificity for wake ranged only 0.10–0.52 — with whole-sample TST overestimation of 7–67 min, SE overestimation of 2%–15%, and WASO underestimation of 6–44 min. Among the newer sleep-staging Fitbit models (HRV + motion), sensitivity was higher (0.95–0.96) and specificity improved substantially (0.58–0.69); in this subset, group-level differences in TST, WASO, and SE vs PSG were no longer statistically significant, though individual-level variability remained [3, meta_analysis]. No conflicts of interest were declared by the authors [3, meta_analysis].

### C.4 Oura Ring Validation: Two Generations

de Zambotti et al. published the first independent PSG validation of the original Oura Ring (Gen 1) in 41 healthy adolescents and young adults (validation sample skewed young — mean age ~17) [4, cohort]. Sleep-detection sensitivity was 96% and wake-detection specificity was only 48%, consistent with the canonical asymmetry. Summary measures for TST, WASO, and sleep onset latency did not significantly differ from PSG; 87.8% of TST values and 85.4% of WASO values fell within ±30 min of PSG. Sleep staging agreement, however, was substantially lower: 65% for light sleep (N1), 51% for deep sleep (N2+N3), and 61% for REM [4, cohort]. These figures should not be taken as adult-generalizable without qualification given the sample's age skew.

Svensson et al. (University of Tokyo, 2024) independently validated the Oura Ring Generation 3 with Sleep Staging Algorithm 2.0 against multi-night ambulatory PSG in 96 participants totaling 421,045 scored epochs [6, cohort]. The Gen3 ring did not significantly differ from PSG for TIB, TST, sleep onset latency, WASO, light sleep time, or deep sleep time; SE was slightly underestimated by 1.1%–1.5% and REM by 4.1–5.6 min. Binary sleep–wake classification sensitivity was 94.4%–94.5% with specificity of 73.0%–74.6% — a substantial wake-specificity improvement over earlier devices. Sleep staging accuracy ranged from 75.5% (light sleep) to 90.6% (REM), with overall accuracy 91.7%–91.8% and PABAK reliability of 94.8% [6, cohort]. Note: Oura Ring is a commercial product; this study was an independent academic validation not funded by the manufacturer.

A 2024 three-device comparison (Robbins et al., Sensors) evaluated Oura Ring Gen3, Fitbit Sense 2, and Apple Watch Series 8 against PSG in 35 healthy adults [7, cohort]. For binary sleep–wake detection, all three devices achieved sensitivity ≥ 95%. For four-stage classification (wake/light/deep/REM), Oura Gen3 showed the most consistent per-stage sensitivities (76.0–79.5%), followed by Fitbit Sense 2 (61.7–78.0%) and Apple Watch (50.5–86.1%, but notably lower for deep sleep at 50.5%). Epoch-level four-stage agreement was strongest for Oura (Kappa = 0.65) vs Fitbit (0.55) and Apple Watch (0.60) [7, cohort].

### C.5 Sleep Staging Accuracy Is Categorically Lower Than Sleep–Wake Accuracy

Across the literature, sleep–wake binary accuracy typically exceeds 90%, but four-class staging (wake/N1/N2/N3/REM) agreement with PSG is substantially lower [5, mechanism_review]. The de Zambotti et al. 2024 consensus review synthesized the field: epoch-by-epoch staging accuracies fall approximately 50%–90% for light sleep (PSG N1+N2), 30%–80% for deep sleep (PSG N3), and 30%–80% for REM sleep, with no consistent directional bias for staging [5, mechanism_review]. In an independent systematic review of wearable staging algorithms, PPG-based three- and four-class systems achieved classification accuracies broadly in the 65–75% range across published studies [8, mechanism_review]. The poorest agreement is consistently observed at N1/N2 boundaries and during the detection of brief N3 epochs. The consequence for users: consumer "deep sleep" and "REM" minute-counts should be interpreted as rough structural estimates, not precise PSG-equivalent measures. The SE summary metric — which aggregates all non-wake time — is consistently more reproducible than any single stage estimate.

COI note: de Zambotti, lead author of [5, mechanism_review], lists an affiliation with Lisa Health Inc., a digital health company; this potential commercial interest should be weighed when interpreting the review's recommendations, though the quantitative accuracy ranges it synthesizes are drawn from the cited primary studies.

### C.6 Practical Limitations for Interpreting Wearable SE

**In-bed window detection.** PSG defines TIB precisely from technician-confirmed lights-out to final-awakening. Consumer wearables must infer bedtime and rise time automatically from movement and physiological signals, or rely on user-entered data. Errors in this inference directly propagate into both SE and TST; a device that detects "lights out" 30 min early can artifactually inflate TIB and thus deflate SE by several percentage points. Manual-log settings generally outperform auto-detection, but compliance is inconsistent in free-living use [5, mechanism_review].

**Proprietary algorithms and firmware updates.** Each manufacturer's scoring algorithm is a trade secret. Validation studies conducted on one firmware version may not generalize after an automatic software update — a documented issue that makes cross-study and longitudinal comparisons difficult [5, mechanism_review; 2, cohort]. Devices from different manufacturers should not be treated as interchangeable even when marketing the same metric.

**Within-device trend validity.** Because systematic biases are partially consistent within the same device and user, relative night-to-night changes in SE (e.g., comparing Monday vs Wednesday on the same device, under similar sleep conditions) carry more interpretive weight than absolute SE values compared across devices or against PSG-derived norms. This is the appropriate frame for wellness self-tracking.

**Population boundary.** Validation studies are predominantly conducted in healthy young adults in a single-night laboratory setting. Performance in populations with insomnia disorder, older adults, shift workers, athletes, or individuals with darker skin tones (where PPG accuracy can be lower) may differ meaningfully from reported figures [5, mechanism_review; 7, cohort].

**Diagnostic scope.** Consumer sleep tracking is a wellness tool, not a clinical diagnostic instrument. No wearable device is cleared to diagnose insomnia disorder, obstructive sleep apnea, or any other sleep pathology. A persistently low wearable SE reading that concerns a user is an indication to pursue clinical evaluation — not a substitute for it.

---

## Bibliography

1. American Academy of Sleep Medicine. *The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications*, Version 3. Darien, IL: AASM, 2023. Available: aasm.org. — tag: regulatory — tier: 1

2. Chinoy ED, Cuellar JA, Huwa KE, Jameson JT, Watson CH, Bessman SC, Hirsch DA, Cooper AD, Drummond SPA, Markwald RR. Performance of seven consumer sleep-tracking devices compared with polysomnography. *Sleep*. 2021 May 14;44(5):zsaa291. PMID: 33378539. DOI: 10.1093/sleep/zsaa291. — tag: cohort — tier: 2

3. Haghayegh S, Khoshnevis S, Smolensky MH, Diller KR, Castriotta RJ. Accuracy of wristband Fitbit models in assessing sleep: systematic review and meta-analysis. *J Med Internet Res*. 2019 Nov 28;21(11):e16273. PMID: 31778122. DOI: 10.2196/16273. No conflicts of interest declared. — tag: meta_analysis — tier: 2

4. de Zambotti M, Rosas L, Colrain IM, Baker FC. The sleep of the ring: comparison of the ŌURA sleep tracker against polysomnography. *Behav Sleep Med*. 2019 Mar–Apr;17(2):124–136. PMID: 28323455. DOI: 10.1080/15402002.2017.1300587. — tag: cohort — tier: 2

5. de Zambotti M, Goldstein C, Cook J, Menghini L, Altini M, Cheng P, Robillard R. State of the science and recommendations for using wearable technology in sleep and circadian research. *Sleep*. 2024 Apr 12;47(4):zsad325. PMID: 38149978. DOI: 10.1093/sleep/zsad325. COI: de Zambotti lists affiliation with Lisa Health Inc. (digital health company). — tag: mechanism_review — tier: 2

6. Svensson T, Madhawa K, Nt H, Chung U-I, Svensson AK. Validity and reliability of the Oura Ring Generation 3 (Gen3) with Oura sleep staging algorithm 2.0 (OSSA 2.0) when compared to multi-night ambulatory polysomnography: a validation study of 96 participants and 421,045 epochs. *Sleep Med*. 2024 Mar;115:251–263. PMID: 38382312. DOI: 10.1016/j.sleep.2024.01.020. Independent academic validation (University of Tokyo); not manufacturer-funded per disclosures. — tag: cohort — tier: 2

7. Robbins R, Weaver MD, Sullivan JP, et al. Accuracy of three commercial wearable devices for sleep tracking in healthy adults. *Sensors*. 2024;24(20):6532. DOI: 10.3390/s24206532. — tag: cohort — tier: 2

8. Imtiaz SA. A systematic review of sensing technologies for wearable sleep staging. *Sensors*. 2021;21(5):1562. DOI: 10.3390/s21051562. — tag: mechanism_review — tier: 2
