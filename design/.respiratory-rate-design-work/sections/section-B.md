# Section B: Interpretation, Norms & The Personal Baseline

## Population Norms: What Is a Normal Respiratory Rate?

Respiratory rate (RR) is the count of complete breath cycles — one inhalation and one exhalation — per minute. In healthy resting adults, the conventionally accepted normal range is **12–20 breaths/min** [1, regulatory]. This band is operationalized in the National Early Warning Score 2 (NEWS2), the NHS-endorsed physiological deterioration system, which assigns a score of zero — meaning no concern — to any RR in this range [1, regulatory]. Rates of 21–24 breaths/min earn a score of 2, and ≥25 breaths/min a score of 3, while ≤8 breaths/min also scores 3 [1, regulatory]. In practical clinical terms, **tachypnea** (abnormally fast breathing) is most commonly flagged at >20 breaths/min, with >24 breaths/min representing a more urgent threshold; **bradypnea** (abnormally slow breathing) is flagged at <12 breaths/min, though clinical concern depends heavily on context (sedation, sleep apnea, high athletic fitness).

Population-level data confirm the norm. In the KORA FF4 cohort study (n = 2,224 adults aged 39–88 from Southern Germany, resting ECG-derived RR over 5 minutes), the median resting RR was 15.80 breaths/min with a 5th–95th percentile range of 12.06–20.06 breaths/min — tracking the conventional clinical band almost exactly [6, cohort]. The large Fitbit-derived dataset analyzed by Natarajan et al. found that 90% of nocturnal RR values in healthy adults fall between 11.8 and 19.2 breaths/min, with a population mean of 15.4 breaths/min [2, cohort]. This tight empirical corridor — essentially the same as the clinical guideline — validates NEWS2's 12–20 band as accurately representing population reality, not just consensus convention.

## Pediatric Ranges: RR Declines Steeply with Age

Children breathe considerably faster than adults, and the rate declines steeply through early life before reaching adult values in mid-adolescence. The most rigorous evidence on this comes from Fleming et al.'s systematic review of 69 studies (n = 3,881 children birth to 18 years), published in The Lancet [3, meta_analysis]. Key age-stratified medians:

| Age group | Approximate median RR (breaths/min) |
|-----------|-------------------------------------|
| Newborn (birth) | ~44 |
| 1–2 years | ~26 |
| 3–5 years | ~24 |
| 6–11 years | ~20 |
| 12–15 years | ~18 |
| >15 years (adolescent) | ~16 → adult range |

The steepest decline occurs in the first two years of life. By school age, rates are approaching but still above adult norms; by mid-adolescence, the 12–20 range applies. This developmental trajectory matters for anyone tracking pediatric wearable data: what reads as tachypnea in an adult is physiological in a 2-year-old.

## The Load-Bearing Wearable Point: The Personal Baseline Is Tight

Here is where RR diverges from every other vital sign in wearable context: **nocturnal RR is remarkably stable within an individual across nights — far more stable than the wide population distribution suggests**.

Natarajan et al. (Fitbit-affiliated), analyzing continuous nocturnal RR data from a large Fitbit cohort across 14-day monitoring windows, found that **within-person coefficient of variation (CV) was only 2.3–9.5% in younger adults (ages 20–24), rising to 2.5–21.7% in older age bands (ages 65–69)** [2, cohort]. The load-bearing point holds across age groups — within-person stability remains the reference frame, because each person's baseline is tight relative to the wide population spread — but the absolute CV ceiling climbs with age, so older adults should expect somewhat wider night-to-night scatter around their personal mean than younger adults. To put the younger-adult figures in concrete terms: for a person whose average nocturnal RR is 14.5 breaths/min, a CV of 2.3–9.5% implies night-to-night fluctuation of roughly ±0.3–1.4 breaths/min around their stable personal mean. The personal range is tight enough that a shift of even 1–2 breaths/min can be physiologically meaningful. By comparison, the **inter-individual** (person-to-person) variance is wide: one healthy adult's stable nocturnal RR might be 13.2 breaths/min while another's is 17.5 — a gap that is entirely normal but would look clinically suspicious if you only had the population reference [2, cohort].

Toften et al. confirmed this in a 3-month longitudinal validation study using a radar-based, contactless sleep monitor (Somnofy; n = 37 healthy adults, nightly monitoring) [4, cohort]. Nightly filtered RR averages were "fairly consistent from night to night," with Bland-Altman 95% limits of agreement for nightly averages of **−0.07 to −0.04 breaths/min** — a span of less than 0.1 brpm that represents exceptionally tight within-person stability. For someone whose nocturnal RR averages 14–15 breaths/min, this measurement window means a genuine 2–3 brpm elevation during illness stands out clearly above the noise floor. Crucially, the study then established personalized baselines from the first 40 nights of data and monitored for deviations. During documented illness episodes, all four participants who became sick showed RR increases that exceeded their individual confidence intervals — deviations that the wide population norm would have classified as "still normal" but the personal baseline flagged immediately [4, cohort].

Ravindran et al., studying contactless nocturnal monitoring in 35 older adults (ages 65–83) over 7–14 nights at home, reported a mean nocturnal breathing rate of 14.7 breaths/min (SD 2.9 across the group), with contactless devices achieving mean absolute error ≤1.6 breaths/min relative to polysomnography — adequate resolution to track personal-baseline shifts of the magnitude seen in illness [5, cohort].

## Why the Personal-Baseline Frame Is the Right Frame

The synthesis from these longitudinal wearable studies produces a clear operating principle for RR interpretation: **population norms establish the outer bounds of plausibility, but the signal lives in deviation from your own baseline**.

RR is less inter-individually variable at rest than HRV — the population spread is a few breaths/min, not an order of magnitude. But within-person, RR is even tighter than within-person HRV: the CV data from Natarajan et al. show that a healthy adult's nocturnal RR varies less night-to-night than their nocturnal heart rate [2, cohort]. This combination — a modest but defined population range, plus high within-person stability — makes nocturnal RR an unusually sensitive personal-trend signal. The clinical utility of wearable RR does not come from comparing you to the population. It comes from comparing tonight to your own last 30 nights.

Deviations from personal baseline — an elevation of 2–3+ breaths/min sustained across 1–2 nights — are early flags for acute illness (respiratory infection, febrile illness), physiological stress (high-intensity training load, significant altitude gain), alcohol consumption (which disrupts sleep architecture and elevates RR), or environmental perturbations. These triggers and their magnitude are covered in Section D (Drivers of Acute RR Elevation).

A measurement-consistency requirement follows directly from this: because the signal is the within-person deviation, **the device, sleep conditions, and measurement window must be stable across nights**. Mixing wrist-based and ring-based device data, or comparing nocturnal resting RR against an active-period measurement, will contaminate the baseline. The personal baseline is only as reliable as the measurement protocol.

---

## Bibliography

1. Royal College of Physicians. *National Early Warning Score (NEWS) 2: Standardising the assessment of acute-illness severity in the NHS. Updated report of a working party.* London: RCP, 2017. — tag: regulatory — tier: 1

2. Natarajan A, Su HW, Heneghan C, Blunt L, O'Connor C, Niehaus L. Measurement of respiratory rate using wearable devices and applications to COVID-19 detection. *NPJ Digital Medicine.* 2021;4(1):136. doi: 10.1038/s41746-021-00493-6. PMID: 34526602. — tag: cohort — tier: 2

3. Fleming S, Thompson M, Stevens R, Heneghan C, Plüddemann A, Maconochie I, Tarassenko L, Mant D. Normal ranges of heart rate and respiratory rate in children from birth to 18 years of age: a systematic review of observational studies. *Lancet.* 2011;377(9770):1011–1018. doi: 10.1016/S0140-6736(10)62226-X. PMID: 21411136. — tag: meta_analysis — tier: 1

4. Toften S, Kjellstadli JT, Thu OKF, Ellingsen OJ. Noncontact Longitudinal Respiratory Rate Measurements in Healthy Adults Using Radar-Based Sleep Monitor (Somnofy): Validation Study. *JMIR Biomedical Engineering.* 2022;7(2):e36618. doi: 10.2196/36618. PMID: 38875674. — tag: cohort — tier: 2

5. Ravindran KKG, della Monica C, Atzori G, Lambert D, Hassanin H, Revell V, Dijk D-J. Reliable Contactless Monitoring of Heart Rate, Breathing Rate, and Breathing Disturbance During Sleep in Aging: Digital Health Technology Evaluation Study. *JMIR mHealth and uHealth.* 2024;12:e53643. doi: 10.2196/53643. PMID: 39190477 — tag: cohort — tier: 2

6. Rückert-Eheberg IM, Steger A, Müller A, Linkohr B, Barthel P, Maier M, et al. Respiratory rate and its associations with disease and lifestyle factors in the general population – results from the KORA-FF4 study. *PLoS ONE.* 2025;20(3):e0318502. doi: 10.1371/journal.pone.0318502. PMID: 40067853. — tag: cohort — tier: 2 — host: journals.plos.org (PLOS One, whitelisted)
