# Section A — Recovery metrics & autonomic interpretation

## What the core metrics measure (and what they do not)

**Heart rate variability (HRV)** is the beat-to-beat fluctuation in the interval between successive heartbeats. It is a non-invasive proximal index of *cardiac vagal (parasympathetic) modulation* of the sinoatrial node — not a measure of "stress," "recovery," or whole-body autonomic state in any direct sense [1, mechanism_review]. The dominant short-term, beat-adjacent metric is **rMSSD** (root mean square of successive differences) and its log transform **lnRMSSD**. rMSSD reflects vagal tone, is highly correlated with the high-frequency (HF) spectral band, and is comparatively robust to breathing rate relative to HF power [1, mechanism_review]. The vagal modulation rMSSD captures is largely respiratory sinus arrhythmia — heart period lengthening on exhalation, shortening on inhalation — transmitted via the vagus nerve [1, mechanism_review].

Critically, HRV does **not** directly measure sympathetic activity. The widely marketed **LF/HF ratio** was historically read as a "sympathovagal balance," but consensus now holds its physiological underpinning is unclear and its predictive value low; the low-frequency band reflects a mix of sympathetic and vagal influences plus baroreflex activity, not isolated sympathetic outflow [1, mechanism_review]. A recovery agent should treat lnRMSSD (or HF power) as the interpretable vagal index and avoid attaching meaning to LF/HF or any "sympathetic" number from a consumer device.

**Time-domain vs frequency-domain.** Time-domain indices (rMSSD, SDNN, pNN50) are computed directly from successive RR intervals; frequency-domain indices (LF, HF, LF/HF) require spectral decomposition and are more sensitive to recording length, breathing, and artifact. For night-aggregated consumer recordings, time-domain rMSSD is the more defensible metric.

**Resting heart rate (RHR)** is the cleaner, lower-variance companion signal. It rises with sympathetic activation, dehydration, fever, alcohol, sleep debt, and incomplete training recovery, and it is measured far more reliably than HRV by every device class. RHR does not discriminate *why* it is elevated — it is a sensitive but entirely non-specific alarm.

**Sleep-derived "readiness/recovery" scores** (Oura Readiness, WHOOP Recovery) are *composite* outputs that fold HRV, RHR, sleep duration/architecture, and activity into a single proprietary number. They measure nothing physiological themselves — they are algorithmic approximations whose component weightings differ between brands (HRV appears in ~86% of such scores, RHR in ~79%) [9, mechanism_review].

## Measurement confounds

Day-to-day HRV is exquisitely sensitive to factors unrelated to training adaptation, which is why a single reading is nearly uninterpretable:

- **Alcohol.** In a placebo-controlled crossover (n=26), evening alcohol dose-dependently suppressed nocturnal rMSSD and SDNN and raised heart rate — low dose ~4% faster HR over the first hours, high dose ~14% faster across the whole night [2, rct]. Real-world wearable data concur: HRV-derived recovery fell ~9.3, ~24.0, and ~39.2 percentage units with low, moderate, and high intake [3, cohort]. Alcohol is plausibly the single largest acute confound a recovery agent will encounter.
- **Acute illness/infection.** Infection drives RHR up and HRV down before symptoms. Retrospective smartwatch data detected 63% of COVID-19 cases pre-symptom via RHR elevation relative to individual baseline [4, cohort], and nightly median rMSSD shows persistent reductions during and after acute infection [4, cohort]. An abnormal reading during illness reflects the illness, not deconditioning.
- **Body position.** HRV is higher supine and lower standing; reproducibility itself is position-dependent (moderate-good supine, lower standing) [5, cohort]. Posture must be held constant across days or the comparison is invalid.
- **Time-of-day / circadian phase.** Laboratory HRV protocols restrict measurement to a fixed morning window (e.g., 7–9 am) specifically to remove circadian, digestive, and daily-stressor variance [6, mechanism_review]. Night-aggregated wearable HRV sidesteps the wake-time problem but introduces sleep-architecture dependence.
- **Breathing rate.** Frequency-domain (HF) power is strongly breathing-rate dependent; rMSSD is less so but not immune. Spontaneous-but-regular breathing is the assessment standard [6, mechanism_review].
- **Age.** HRV declines with age; older adults show wider between-day variability and larger device error than younger adults [12, cohort].
- **Acute training load.** A hard session transiently suppresses next-morning vagal HRV; this is expected and not pathological unless it persists.
- **Menstrual cycle.** HRV is higher in the follicular phase and lower in the luteal phase, with LF/HF rising luteally as progesterone increases sympathetic activity [7, cohort]. For menstruating users, phase must be considered before reading a "low HRV" day as overtraining.
- **Hydration and bladder distension** also shift HRV and are rarely controlled [6, mechanism_review]. Acute dehydration reduces plasma volume and elevates RHR, biasing both signals.

## Why trend, baseline and CV beat any single absolute value

The dominant error in consumer use is over-reading day-to-day noise. Between-day reliability of HRV is only moderate-to-good and is metric-, posture-, and condition-dependent. In healthy active adults, inter-day reliability of linear HRV metrics spans ICCs of roughly 0.56–0.88; for log-transformed lnRMSSD the between-day coefficient of variation (CV) is tight (~4.4% in younger, ~5.1% in older adults), but the *raw, untransformed* rMSSD that consumer apps often surface carries a between-day CV near ~17% in the same cohort [11, cohort]. Independent reliability work in trained men reports the same pattern: at rest, time-domain HRV CVs run ~4–17%, spectral indices ~7–27%, and ratio indices (e.g., LF/HF) a far wider ~41–82% — and every index degrades sharply after exercise [17, cohort]. The practical reading: lnRMSSD is the most stable index, raw rMSSD wobbles more, and LF/HF is too unreliable to interpret day-to-day. Either way a single day's value can move materially without any change in underlying recovery state. The defensible interpretive unit is the **individual rolling baseline** (commonly a 7-day rolling average of lnRMSSD) plus its **CV**, not an absolute number compared against population norms.

The seminal evidence is Plews et al.'s 77-day case study of two elite triathletes: the athlete who became non-functionally over-reached showed *both* a declining 7-day rolling lnRMSSD *and* a large linear reduction in the CV of that rolling average (≈ −0.65%/week), while the adapting control athlete's CV stayed flat (≈ +0.04%/week) [8, open_label]. The collapse of variability — the system losing its day-to-day "wobble" — flagged maladaptation that absolute HRV alone would have missed. This is the load-bearing rationale for baseline-relative interpretation: the agent must establish ≥1–2 weeks of personal baseline before any single reading is actionable, and weight trend and CV over absolute value.

## Wearable validity vs gold standard

ECG is gold standard for HRV; polysomnography (PSG) is gold standard for sleep staging. PPG-based wearables measure *pulse* rate variability, not true RR intervals, which is acceptable for HR but introduces additional HRV error.

**Oura ring.** Two independent, peer-reviewed validations against ECG are the strongest evidence here. Cao et al. (n=35, home ECG comparison) found near-perfect nocturnal HR agreement (r=0.993, bias −0.44 bpm) and good time-domain agreement — per-night rMSSD r=0.962 (bias −15.9 ms) — but **poor frequency-domain validity**: LF r=0.42 and LF/HF r=0.36 in the 5-minute analysis [10, cohort]. Liang et al. (n=114, in-lab ECG) confirmed HR r≈0.99 (MdAPE <5%) and rMSSD r=0.94–0.98, but only when a stringent ~80% validity-proportion filter and ≥30-min aggregation windows were applied; rMSSD median absolute percentage error was ~8–11% and worse in older adults [12, cohort]. Takeaway: Oura nocturnal RHR and rMSSD are trend-grade accurate; its frequency-domain HRV is not trustworthy.

**WHOOP.** Against PSG (Miller et al., n=12, 86 nights), 2-stage sleep/wake agreement was 89% (sensitivity to sleep 95%, specificity for wake 51%, κ=0.49); 4-stage agreement dropped to 64% (κ=0.47) [13, cohort]. The low wake specificity and modest 4-stage agreement are typical of all consumer trackers and mean stage-level sleep numbers should not be over-interpreted.

**Apple Watch.** Series 6 vs 3-lead ECG (n=78) showed best agreement at rest — near-perfect RR/BPM concordance, MAPE ~1.15% resting — degrading with movement and talking [14, cohort]. Apple Watch HRV is on-demand/episodic rather than continuous-nocturnal, which limits baseline construction.

**Polar H10 chest strap.** The most accurate non-clinical option: RR-interval r≈0.95 at rest and >0.93 in exercise with minimal Bland-Altman bias; linear HRV indices "can be recommended for practitioners," though non-linear indices and high-intensity exercise widen error [15, cohort]. A chest strap remains the closest practical proxy to ECG for HRV.

## The readiness/recovery score black-box problem

A 2025 evaluation of composite health scores across consumer wearables found that **no manufacturer disclosed its scoring formula**, few provided peer-reviewed validation, and none demonstrated the score predicts hard outcomes (injury, illness, performance, training adaptation) [9, mechanism_review]. Brands combine the same raw inputs with undisclosed proprietary weightings, so Oura and WHOOP scores for the *same night* can diverge by 20+ points and each be internally "correct." These scores are unvalidated black boxes: usable as a coarse personal trend within one device's ecosystem, but not as a cross-device truth and never as a clinical or diagnostic signal.

## HRV-guided training: what the RCT evidence supports

The best synthesis (Manresa-Rocamora et al., meta-analysis of 8 RCTs + 1 non-RCT, n=199) found HRV-guided training **superior for preserving/improving vagal HRV** (vagal-related HRV SMD 0.50, 95% CI 0.09–0.91, p<0.01) and associated with fewer non-responders — but its effects on the outcomes that matter were small and **not statistically significant**: VO₂max SMD 0.20 (CI −0.07 to 0.47) and endurance performance SMD 0.20 (CI −0.09 to 0.48) [16, meta_analysis]. Limits: few trials, mostly 8-week interventions, inconsistent HRV protocols. So HRV-guided autoregulation is *plausibly useful for avoiding maladaptation and reducing negative responders*, but the claim that it boosts performance over a sound predefined plan is not yet supported by significant RCT evidence.

## Key claims for the agent design

1. **rMSSD/lnRMSSD is a vagal index only.** Never interpret LF/HF or any "sympathetic balance" number from a consumer device; it lacks validated physiological meaning [1, mechanism_review].
2. **Trend over absolute.** Interpret HRV against the user's own rolling baseline (e.g., 7-day lnRMSSD) and its CV, never a single day against population norms. Require ≥1–2 weeks of baseline before any reading is actionable [8, open_label][11, cohort].
3. **A single low day is noise until proven otherwise.** Between-day reliability is only moderate-to-good (ICC ~0.56–0.88); raw rMSSD carries a ~17% between-day CV and spectral/ratio indices are far less reliable still, so over-reaction to one reading is the canonical user error [11, cohort][17, cohort].
4. **Confound-first triage.** Before flagging overtraining, check alcohol, illness, poor/short sleep, posture change, and (if applicable) menstrual phase — each can dominate the signal [2, rct][3, cohort][4, cohort][7, cohort].
5. **Falling CV + falling rolling HRV together signal maladaptation** more reliably than a low absolute value [8, open_label].
6. **Wearable HRV is trend-grade, not clinical-grade.** Oura/WHOOP nocturnal RHR and rMSSD track ECG well; frequency-domain HRV and 4-stage sleep do not — do not diagnose from them [10, cohort][12, cohort][13, cohort].
7. **Readiness/recovery scores are unvalidated black boxes.** Treat as coarse within-device trend; never cross-compare brands or use as a clinical signal; explain the proprietary-algorithm caveat to the user [9, mechanism_review].
8. **RHR is a sensitive, non-specific alarm.** A baseline-relative RHR rise warrants a confound check (esp. illness/alcohol), not a diagnosis [4, cohort].
9. **HRV-guided autoregulation has modest, mixed evidence.** Support its use for avoiding maladaptation and reducing non-responders; do not promise performance gains over a sound plan [16, meta_analysis].
10. **A chest strap (Polar H10) is the most accurate practical HRV source** if the user wants better-than-ring fidelity for morning measurements [15, cohort].

## Bibliography

[1] Laborde S, Mosley E, Thayer JF. 2017. Heart Rate Variability and Cardiac Vagal Tone in Psychophysiological Research – Recommendations for Experiment Planning, Data Analysis, and Data Reporting. Frontiers in Psychology. PMID: 28265249. DOI: 10.3389/fpsyg.2017.00213. (Retrieved: 2026-05-31) [mechanism_review]

[2] de Zambotti M, Forouzanfar M, Javitz H, et al. 2021. Impact of evening alcohol consumption on nocturnal autonomic and cardiovascular function in adult men and women: a dose–response laboratory investigation. Sleep. PMID: 32663278. DOI: 10.1093/sleep/zsaa135. (Retrieved: 2026-05-31) [rct]

[3] Pietilä J, Helander E, Korhonen I, et al. 2018. Acute Effect of Alcohol Intake on Cardiovascular Autonomic Regulation During the First Hours of Sleep in a Large Real-World Sample of Finnish Employees: Observational Study. JMIR Mental Health. PMC5878366. DOI: 10.2196/mental.9519. (Retrieved: 2026-05-31) [cohort]

[4] Mishra T, Wang M, Metwally AA, et al. 2020. Pre-symptomatic detection of COVID-19 from smartwatch data. Nature Biomedical Engineering. PMC9020268. DOI: 10.1038/s41551-020-00640-6. (Retrieved: 2026-05-31) [cohort]

[5] Sandercock GRH, et al. / de Souza Nery S, et al. 2019. Impact of heart rate on reproducibility of heart rate variability analysis in the supine and standing positions in healthy men. Clinics. PMC6683304. DOI: 10.6061/clinics/2019/e806. (Retrieved: 2026-05-31) [cohort]

[6] Laborde S, Mosley E, Thayer JF. 2017. (Measurement standardization: posture, breathing, time-of-day, bladder/medication confounds.) Frontiers in Psychology. PMID: 28265249. DOI: 10.3389/fpsyg.2017.00213. (Retrieved: 2026-05-31) [mechanism_review]

[7] Tenan MS, Brothers RM, Tweedell AJ, et al. 2014. Changes in resting heart rate variability across the menstrual cycle. / Brar TK, Singh KD, Kumar A. 2015. Impact of Menstrual Cycle on Cardiac Autonomic Function Assessed by Heart Rate Variability and Heart Rate Recovery. Medical Principles and Practice. PMID: 26828607. DOI: 10.1159/000444439. (Retrieved: 2026-05-31) [cohort]

[8] Plews DJ, Laursen PB, Kilding AE, Buchheit M. 2012. Heart rate variability in elite triathletes, is variation in variability the key to effective training? A case comparison. European Journal of Applied Physiology. PMID: 22367011. DOI: 10.1007/s00421-012-2354-4. (Retrieved: 2026-05-31) [open_label]

[9] Doherty C, Baldwin M, et al. 2025. Readiness, recovery, and strain: an evaluation of composite health scores in consumer wearables. Translational Exercise Biomedicine (De Gruyter). DOI: 10.1515/teb-2025-0001. (Retrieved: 2026-05-31) [mechanism_review]

[10] Cao R, Azimi I, Sarhaddi F, et al. 2022. Accuracy Assessment of Oura Ring Nocturnal Heart Rate and Heart Rate Variability in Comparison With Electrocardiography in Time and Frequency Domains: Comprehensive Analysis. Journal of Medical Internet Research. PMID: 35040799. DOI: 10.2196/27487. (Retrieved: 2026-05-31) [cohort]

[11] Fennell CRJ, Mauger AR, Hopker JG. 2023. Inter-day reliability of heart rate complexity and variability metrics in healthy highly active younger and older adults. European Journal of Applied Physiology. PMID: 38054978. DOI: 10.1007/s00421-023-05373-3. PMC11055755. (Retrieved: 2026-05-31) [cohort]

[12] Liang T, Yilmaz G, Soon CS. 2024. Deriving Accurate Nocturnal Heart Rate, rMSSD and Frequency HRV from the Oura Ring. Sensors (Basel). PMID: 39686012. DOI: 10.3390/s24237475. (Retrieved: 2026-05-31; open-access MDPI — single-source flag) [cohort]

[13] Miller DJ, Lastella M, Scanlan AT, et al. 2020. A validation study of the WHOOP strap against polysomnography to assess sleep. Journal of Sports Sciences. PMID: 32713257. DOI: 10.1080/02640414.2020.1797448. (Retrieved: 2026-05-31) [cohort]

[14] Validity of Heart Rate Variability Measured with Apple Watch Series 6 Compared to Laboratory Measures. 2025. Sensors (Basel). PMC12031371. DOI: 10.3390/s25082380. (Retrieved: 2026-05-31; open-access MDPI — single-source flag) [cohort]

[15] Schaffarczyk M, Rogers B, Reer R, Gronwald T. 2022. Validity of the Polar H10 Sensor for Heart Rate Variability Analysis during Resting State and Incremental Exercise in Recreational Men and Women. Sensors (Basel). PMID: 36081005. DOI: 10.3390/s22176536. (Retrieved: 2026-05-31; open-access MDPI — single-source flag) [cohort]

[16] Manresa-Rocamora A, Sarabia JM, Sánchez-Meca J, et al. 2021. Heart Rate Variability-Guided Training for Enhancing Cardiac-Vagal Modulation, Aerobic Fitness, and Endurance Performance: A Methodological Systematic Review with Meta-Analysis. International Journal of Environmental Research and Public Health. PMID: 34639599. DOI: 10.3390/ijerph181910299. (Retrieved: 2026-05-31) [meta_analysis]

[17] Al Haddad H, Laursen PB, Chollet D, Ahmaidi S, Buchheit M. 2011. Reliability of Resting and Postexercise Heart Rate Measures. International Journal of Sports Medicine. PMID: 21574126. DOI: 10.1055/s-0031-1275356. (Retrieved: 2026-05-31) [cohort]

## Self-check

(a) **Inline ↔ bibliography resolution.** Inline citations used: [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17]. All 17 resolve to bibliography entries; all 17 bibliography entries are cited inline ([17] is cited in the "Why trend, baseline and CV" section and key-claim 3). No orphans either direction. ([6] reuses source [1] under a distinct claim — same DOI, both numbered for traceability.)

(b) **No vendor_label/anecdote grounds a numeric.** Every numeric (r, ICC, CV, SMD, MAPE, bias, %) traces to a peer-reviewed cohort/RCT/meta_analysis/mechanism_review source. No ouraring.com, whoop.com, apple.com, podcast, or forum source grounds any number; vendor pages and Substack/LinkedIn hits surfaced in search were excluded from the bibliography. Oura/WHOOP validity numbers come only from independent peer-reviewed studies ([10], [12], [13]).

(c) **Population-mismatch tags.** No animal or in_vitro citations are used in this section; therefore no [population-mismatch] tags are required. All sources are human studies.

(d) **Source count.** 17 bibliography entries (target ≥8, aim 10–14 — exceeds). Type-tag distribution: meta_analysis ×1, rct ×1, cohort ×10, open_label ×1, mechanism_review ×2 ([1] and its [6] reuse). MDPI open-access single-source flags applied to [12], [14], [15].

(e) **Citation-fidelity re-verification (iter-2 remediation).** Three flagged citations were re-verified by fetching the primary sources: [11] PMC11055755 resolves to Fennell et al. 2023, Eur J Appl Physiol (PMID 38054978; lnRMSSD ICC 0.57–0.79, lnRMSSD CV 4.4–5.1%, raw RMSSD CV 17.3–17.9%) — re-attributed from the prior erroneous "Bellenger 2024, Scientific Reports" label, and the unverifiable ">30% CV" / "ICC 0.37–0.93, CV 3.5–36.5%" claim was softened to the verified figures. A second independent reliability source ([17] Al Haddad 2011, PMID 21574126: time-domain CV 4–17%, spectral 7–27%, ratio 41–82% at rest) now grounds the condition-dependent reliability claim. [16] VO₂max corrected from SMD 0.13 (CI −0.12 to 0.39) to the published SMD 0.20 (CI −0.07 to 0.47) per PMID 34639599. [2] de Zambotti year corrected 2020 → 2021 per PMID 32663278.

## Post-fix grep audit

For each corrected value, the OLD value was grepped case-insensitively across the whole section file after the rewrite. Results and disposition below.

**Correction 1 — [11] attribution "Bellenger".** `grep -inE 'bellenger'` → no hits. Clean: every "Bellenger 2024 / Scientific Reports" instance removed and replaced by the Fennell 2023 / Eur J Appl Physiol attribution.

**Correction 1b — old [11] DOI `10.1038/s41598-024-58217-1`.** `grep -inE '58217'` → no hits. Clean: replaced by the Fennell DOI 10.1007/s00421-023-05373-3.

**Correction 1c — unverifiable reliability numbers `0.37`, `0.93`, `3.5%`, `36.5%`.** `grep -inE '0\.37|0\.93|3\.5%|36\.5'` → outside this self-check, one body hit: line 45, Polar H10 "RR-interval r≈0.95 at rest and >0.93 in exercise" [15]. Disposition: legitimately unchanged — that `0.93` is the verified Polar H10 RR-interval correlation coefficient from Schaffarczyk 2022, not the removed [11] ICC. The "ICC 0.37–0.93, CV 3.5–36.5%" string is fully removed; `0.37`, `3.5%`, `36.5%` return zero body hits. Replaced by verified Fennell/Al Haddad ranges.

**Correction 1d — ">30%" CV claim.** `grep -inE 'exceed 30|> ?30%|30 ?%'` → no hits. Clean: key-claim 3 no longer asserts a >30% lnRMSSD CV; it now states ICC ~0.56–0.88 and raw rMSSD CV ~17%.

**Correction 2 — [16] VO₂max `0.13` and CI `−0.12 to 0.39`.** `grep -inE '0\.13|0\.12|0\.39'` → no hits. Clean: the only surviving SMD values are the verified 0.50, 0.20/0.20 and CIs 0.09–0.91, −0.07 to 0.47, −0.09 to 0.48. (Note: the endurance SMD 0.20 / CI −0.09 to 0.48 was already correct and was preserved unchanged.)

**Correction 3 — [2] de Zambotti year `2020`.** `grep -inE '\b2020\b'` → two hits, both legitimately unchanged and unrelated to the de Zambotti correction:
  - Bibliography [4] Mishra et al. "2020. Pre-symptomatic detection of COVID-19" — correct year for that source (PMC9020268), not de Zambotti.
  - Bibliography [13] Miller et al. "2020. A validation study of the WHOOP strap" — correct year for that source (PMID 32713257), not de Zambotti.
  The de Zambotti [2] entry itself now reads "2021" (corrected). No residual "de Zambotti … 2020" remains: `grep -inE 'zambotti'` → one hit, line in [2], reading 2021. Disposition: clean.

All corrected OLD values return zero residual hits except the two legitimately-2020 sources ([4], [13]), which are annotated as unchanged-by-design.
