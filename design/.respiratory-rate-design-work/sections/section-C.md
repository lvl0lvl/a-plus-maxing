# Section C: Measurement & Device Validity

## Reference Standards

Respiratory rate (RR) can be measured by a hierarchy of methods, each with distinct trade-offs between accuracy, practicality, and suitability for continuous or ambulatory use.

**Manual observation** — counting chest rises over a full 30–60 seconds — is the bedside clinical standard and has been used as a comparator in numerous validation studies. Despite this role, it is widely documented as the most inaccurate and most poorly charted vital sign in hospital practice. Nurses frequently default to recording 18 or 20 breaths per minute regardless of the patient's actual rate, and during the 24-hour period before cardiac arrest, RR is the vital sign documented least often [1, cohort]. A controlled inter-observer study found that when nurses were asked to count respiratory rate from video, agreement was high (ICC 0.99) under ideal conditions — but the key word is *ideal*: standardized viewing, no patient movement, full 60-second counting windows [2, cohort]. Clinical ward conditions are none of these things. The gap between protocol-measured agreement and real-world charting accuracy is the central argument for continuous automated monitoring.

**Capnography (end-tidal CO₂, EtCO₂)** is the gold standard for true breath-by-breath detection in instrumented or peri-operative settings. It directly measures exhaled CO₂ concentration, yielding a waveform that unambiguously identifies each breath. Its limitation is practical: capnography requires a nasal cannula or intubation interface that is poorly tolerated for extended ambulatory use and is unsuitable for consumer wearables [3, cohort].

**Respiratory inductance plethysmography (RIP) belts** — circumferential bands placed around the chest and abdomen that sense volume changes via inductance — provide continuous, non-invasive respiratory waveforms and are used both in clinical monitoring and as a reference standard in sleep studies. RIP belts can distinguish obstructive from central apneas, an advantage over thermistor-alone approaches. The design of the belt (coil geometry, calibration method) substantially affects signal quality [4, mechanism_review].

**Polysomnography (PSG)** in the sleep laboratory combines multiple channels — nasal thermocouple or pressure transducer, chest and abdominal RIP belts, oximetry, EEG, and EMG — into the definitive multi-channel sleep reference. For wearable RR validation during sleep, PSG-derived RR (from the airflow thermistor or RIP channel) is the standard comparator.

---

## PPG-Derived Respiratory Rate: The Wearable Method

Consumer wearables (wrist-worn smartwatches, fitness trackers, ring sensors) derive RR from the photoplethysmography (PPG) signal — the optical measurement of peripheral blood volume that also drives heart-rate estimation. Respiration leaves three distinct modulations on the PPG waveform, described in the seminal Charlton et al. 2018 review [5, mechanism_review]:

1. **Baseline wander (BW):** respiratory-driven slow drift in PPG baseline, reflecting venous pressure changes.
2. **Amplitude modulation (AM):** stroke-volume variation with each breath causes beat-to-beat changes in PPG pulse height.
3. **Frequency modulation (FM):** respiratory sinus arrhythmia (RSA) produces subtle beat-rate changes locked to the breathing cycle.

Consumer devices extract one or more of these modulations, then estimate RR via spectral analysis, peak detection, or learned (neural-network) approaches. Higher-performing algorithms fuse all three modulation channels and apply quality-assessment filters that reject low-confidence windows — a design principle first systematically benchmarked in Charlton et al. 2016 [6, open_label], which tested 314 PPG and ECG algorithms against a nasal-oral pressure reference in healthy adults. The best PPG-based algorithm achieved a Bland-Altman bias of 1.0 bpm with limits of agreement (LoA) of −5.1 to +7.2 bpm. ECG-based algorithms outperformed PPG-based ones, a gap that persists in part because wrist PPG is more susceptible to motion artifact than chest-lead ECG.

---

## Accuracy Under Rested and Sleep Conditions

PPG-derived RR is most accurate during sleep and rest, when breathing is regular, motion is minimal, and signal quality is high. The Samsung Galaxy Watch validation study — conducted in 195 participants undergoing overnight PSG at a sleep clinic, with nasal thermocouple as reference — reported an average-overnight RR RMSE of 1.13 bpm (bias 0.39 bpm, Bland-Altman LoA −1.68 to +2.46 bpm) and a continuous-epoch RMSE of 1.62 bpm (LoA −2.73 to +3.47 bpm) [7, cohort]. Accuracy exceeded 90% (within ±2 bpm) for participants with normal to moderate obstructive sleep apnea (AHI < 30), but fell to 79.5% (average) and 75.8% (continuous) for severe OSA (AHI ≥ 30). **COI disclosure: two of the four listed authors are Samsung Electronics employees; the study was funded by Samsung Electronics. The accuracy figures should be interpreted with this manufacturer affiliation in mind. These figures are manufacturer-reported and await independent (non-vendor) replication before they can be treated as established benchmarks.**

In the algorithm-validation literature, a multi-modulation PPG fusion method tested against capnography (Capnobase dataset, n = 42 recordings) achieved a bias of 0.28 bpm, LoA of −3.62 to +4.17 bpm, and RMSE of 1.8 bpm; against PSG-derived nasal/oral airflow in a pediatric sleep dataset, bias was 0.04 bpm, LoA −5.74 to +5.82 bpm, RMSE 2.3 bpm [8, cohort]. **These fusion-accuracy figures are manufacturer-reported (from a study with LGT Medical Inc.-affiliated authors) and await independent (non-vendor) replication.** The figures suggest that sub-2 bpm errors (MAE often < 1 brpm against PSG in adults) are achievable at rest when signal quality is controlled, and that fusion of multiple PPG modulation features outperforms single-channel extraction, but the manufacturer affiliation warrants caution in treating these as independently established benchmarks.

The effect of measurement *site* adds another layer of variability. In a controlled study of six body locations in 36 healthy subjects, the forehead and finger yielded the best PPG-derived respiratory frequency agreement under normal and deep breathing respectively; the wrist showed wider LoA and site-dependent bias [9, cohort]. Consumer devices use the wrist exclusively — a compromise of convenience over signal quality.

---

## Accuracy Degradation: Motion, Irregular Breathing, and Apnea

PPG-derived RR degrades in predictable ways:

- **Motion artifact** is the dominant confound on wrist PPG. Accelerometer-based motion correction helps but cannot eliminate artifact during vigorous activity; most consumer devices suppress RR output or widen uncertainty windows during active epochs.
- **Irregular breathing** (highly variable inter-breath intervals, Cheyne-Stokes patterns) breaks spectral-peak assumptions; the Samsung data showing 20+ percentage-point accuracy drops in severe OSA is the empirical illustration of this.
- **Apnea events** create signal ambiguity — no airflow to detect — and some devices will miss apnea periods entirely or report an interpolated rate rather than zero. This is why consumer PPG RR does *not* diagnose obstructive sleep apnea or respiratory failure, even in devices that report a breathing disturbance index as a secondary output.
- **Low perfusion and arrhythmia** (atrial fibrillation, frequent ectopy) corrupt both the AM and FM modulation channels, since these rely on beat-to-beat regularity.

The 2020 JMIR systematic review of continuous vital-signs monitoring by wearable devices concluded that, across included studies, RR measurements frequently showed "wide LoA" beyond clinically acceptable ranges (±3 bpm), and that there were no high-quality large controlled studies demonstrating clinical benefit [10, mechanism_review].

---

## Within-Device Trends vs. Absolute Cross-Device Values

The key practical implication follows from the above: proprietary RR algorithms are not interchangeable. A Garmin estimate of 14 bpm and an Apple estimate of 14 bpm on the same individual may reflect different algorithmic constructs applied to different PPG wavelengths at different sampling rates. Cross-device comparison of absolute RR values is therefore not meaningful. What *is* reproducible within a device — under consistent wearing conditions, time of night, and sleep stage — is the trend signal: rising overnight average RR over weeks may reflect developing illness, altitude acclimatization failure, or overtraining, regardless of whether the absolute number is precisely calibrated.

**Regulatory framing:** Consumer RR is consistently classed as a **wellness metric, not a diagnostic measurement**. No current consumer wristwatch carries regulatory clearance for diagnosing respiratory failure, apnea syndrome, or pneumonia based on its PPG-derived RR output. Some devices flag "breathing disturbance" alongside SpO₂ anomalies and pair these with questionnaire prompts to consult a clinician — this is appropriate scope. The validated clinical use of continuous RR monitoring (e.g., the postoperative setting where wrist-PPG devices achieved 93% of measurements within ±3 bpm vs. capnography, with a bias of 0.17 bpm) still requires formal clinical validation per ISO/IEEE device standards, not consumer app approval [3, cohort].

---

## Bibliography

1. Rivas E, López-Baamonde M, Sanahuja J, Del Rio E, Ramis T, Recasens A, López A, Arias M, Kampakis S, Lauteslager T, Awara O, Mascha EJ, Soriano A, Badía JR, Castro P, Sessler DI, et al. Early detection of deterioration in COVID-19 patients by continuous ward respiratory rate monitoring: a pilot prospective cohort study. *Frontiers in Medicine.* 2023;10:1243050. doi:10.3389/fmed.2023.1243050. PMID: 38020176 — **COI: three authors employed by Circadia Technologies Ltd. (device manufacturer); study funded by Circadia Technologies Ltd.** — tag: cohort — tier: 3

2. Nielsen LG, Folkestad L, Brodersen JB, Brabrand M. Inter-observer agreement in measuring respiratory rate. *PLoS ONE.* 2015;10(6):e0129493. doi:10.1371/journal.pone.0129493. PMID: 26090961 — tag: cohort — tier: 3

3. van der Stam JA, Mestrom EHJ, Scheerhoorn J, Jacobs FENB, Nienhuijs S, Boer AK, van Riel NAW, de Morree HM, Bonomi AG, Scharnhorst V, Bouwman RA. The accuracy of wrist-worn photoplethysmogram-measured heart and respiratory rates in abdominal surgery patients: observational prospective clinical validation study. *JMIR Perioperative Medicine.* 2023;6(1):e40474. doi:10.2196/40474. PMID: 36804173 — **COI: one author consulted for Philips Research; two authors were Philips Research employees; funded by Dutch RVO ITEA grant** — tag: cohort — tier: 2

4. Hussain T, Ullah S, Fernández-García R, Gil I. Wearable sensors for respiration monitoring: a review. *Sensors (Basel).* 2023;23(17):7518. doi:10.3390/s23177518. PMID: 37687977 — tag: mechanism_review — tier: 3

5. Charlton PH, Birrenkott DA, Bonnici T, Pimentel MAF, Johnson AEW, Alastruey J, Tarassenko L, Watkinson PJ, Beale R, Clifton DA. Breathing rate estimation from the electrocardiogram and photoplethysmogram: a review. *IEEE Reviews in Biomedical Engineering.* 2018;11:2–20. doi:10.1109/RBME.2017.2763681. PMID: 29990026 — tag: mechanism_review — tier: 1

6. Charlton PH, Bonnici T, Tarassenko L, Clifton DA, Beale R, Watkinson PJ. An assessment of algorithms to estimate respiratory rate from the electrocardiogram and photoplethysmogram. *Physiological Measurement.* 2016;37(4):610–626. doi:10.1088/0967-3334/37/4/610. PMID: 27027672 — tag: open_label — tier: 1

7. Jung H, Kim D, Choi J, Joo EY. Validating a consumer smartwatch for nocturnal respiratory rate measurements in sleep monitoring. *Sensors (Basel).* 2023;23(18):7976. doi:10.3390/s23187976. PMID: 37766031 — **COI: Jung and Choi affiliated with Samsung Electronics; study funded by Samsung Electronics and Samsung Medical Center. Treat absolute accuracy figures with caution given manufacturer funding.** — tag: cohort — tier: 3

8. Dehkordi P, Garde A, Molavi B, Ansermino JM, Dumont GA. Extracting instantaneous respiratory rate from multiple photoplethysmogram respiratory-induced variations. *Frontiers in Physiology.* 2018;9:948. doi:10.3389/fphys.2018.00948. PMID: 30072918 — **COI: Ansermino and Dumont are founders of LGT Medical Inc. with equity in related technology; Molavi is employed by LGT Medical Inc.** — tag: cohort — tier: 2

9. Hartmann V, Liu H, Chen F, Hong W, Hughes S, Zheng D. Toward accurate extraction of respiratory frequency from the photoplethysmogram: effect of measurement site. *Frontiers in Physiology.* 2019;10:732. doi:10.3389/fphys.2019.00732. PMID: 31316390 — tag: cohort — tier: 2

10. Leenen JPL, Leerentveld C, van Dijk JD, van Westreenen HL, Schoonhoven L, Patijn GA. Current evidence for continuous vital signs monitoring by wearable wireless devices in hospitalized adults: systematic review. *Journal of Medical Internet Research.* 2020;22(6):e18636. doi:10.2196/18636. PMID: 32469323 — tag: mechanism_review — tier: 2
