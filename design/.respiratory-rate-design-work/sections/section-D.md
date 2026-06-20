# D. Determinants & Significance

## What Raises Respiratory Rate

**Fever, illness, and infection** are among the most clinically important drivers of elevated RR. The body's metabolic response to infection — including cytokine release, elevated temperature, and increased oxygen demand — accelerates breathing rate, often before the person feels unwell. Wearable cohort studies have documented that nocturnal respiratory rate frequently rises around or just prior to symptom onset in SARS-CoV-2 infection: in a Fitbit-based study by Natarajan et al. (2021), 36.4% of symptomatic individuals had at least one nocturnal RR measurement ≥3 breaths/min above their personal baseline within a 7-day window around illness onset (Cohen's d = 0.70 for the within-subject shift), compared with 23.7% of asymptomatic individuals [1, cohort]. The TemPredict cohort (N = 63,153 Oura ring users; 73 COVID+ participants with PCR-confirmed infection used for algorithm training) detected illness a mean of 2.75 days before participants sought testing, incorporating respiratory rate alongside temperature, HRV, and heart rate, with an AUC of 0.819, sensitivity 82%, specificity 63% [2, cohort]. A 2022 Lancet Digital Health systematic review of wearable COVID-19 detection studies (12 completed articles; devices including Fitbit, Oura, WHOOP, and others) found AUCs of 0.52–0.92 across algorithmic models, with 3 of 4 studies that measured RR finding elevation around symptom onset [3, meta_analysis].

**Exertion and metabolic demand** increase RR proportionally to workload. During intense exercise, RR may reach 40–60 breaths/min in healthy adults. This is physiological and resolves rapidly with rest.

**Anxiety, stress, and panic** can trigger hyperventilation — rapid, shallow breathing that drives down CO₂ (hypocapnia), producing lightheadedness, tingling, and chest tightness. The RR elevation here is neurogenic rather than metabolic.

**Pain** acutely elevates RR via sympathetic activation and the physiological stress response.

**Metabolic acidosis** generates a compensatory respiratory alkalosis: the body increases RR to exhale more CO₂ and partially correct the acidemia. In diabetic ketoacidosis, this produces the characteristic Kussmaul breathing — deep, labored, sighing respirations that may exceed 25–30 breaths/min.

**Hypoxia, altitude, and cardiorespiratory disease** (asthma, COPD, pneumonia, pulmonary embolism, heart failure with pulmonary congestion) all raise RR because the body is attempting to increase alveolar ventilation in response to impaired gas exchange or reduced oxygen availability.

**Pregnancy** causes a mild, sustained RR increase (typically 1–2 breaths/min) driven by progesterone-mediated chemoreceptor sensitization.

**Stimulants** (caffeine, amphetamines, some pre-workout compounds) transiently elevate RR through sympathomimetic effects.

---

## What Lowers Respiratory Rate

**Opioids and sedatives** are the primary pharmacological depressants of respiratory drive and represent a major safety concern in clinical settings. Opioids bind μ-receptors in the brainstem respiratory centers, suppressing both rate and depth of breathing. The PRODIGY trial — an international prospective observational study of 1,335 general care floor patients receiving parenteral opioids, monitored with continuous capnography and oximetry — found that 614 (46%) experienced at least one opioid-induced respiratory depression (OIRD) episode (defined as RR ≤ 5 breaths/min, SpO₂ ≤ 85%, or ETCO₂ out of range for ≥3 min, or apnea > 30 sec) [4, cohort]. Patients with ≥1 OIRD episode had 2.8 additional hospital days (10.5 vs 7.7 days, p < 0.0001) and 17% higher costs (propensity-weighted; ~$3,686/patient additional) [5, cohort]. High-risk patients (PRODIGY score) had 6× the odds of OIRD vs low-risk patients (OR 6.07, 95% CI 4.44–8.30) [4, cohort]. Importantly, OIRD often manifests as intermittent apneic episodes — not simply a slow RR — a pattern that standard spot-check vital signs miss: a post-hoc analysis of the PRODIGY trial found that spot-checks of oxygenation miss up to 90% of clinical hypoxemia episodes [6, cohort].

**CNS depressants** (benzodiazepines, barbiturates, general anesthetics) act similarly, through different receptor mechanisms, to reduce respiratory drive.

**Hypothyroidism** in severe or myxedematous states decreases metabolic rate and may cause hypoventilation.

**Sleep** produces a modest physiological reduction in RR (roughly 1–2 breaths/min below waking baseline) as metabolic demand and CO₂ sensitivity both decrease.

**Slow-breathing practices** (pranayama, resonance frequency breathing, coherent breathing) deliberately lower RR to 4–8 breaths/min; this is intentional and physiologically distinct from pathological suppression.

---

## Significance

### 1. The Underused Vital Sign: RR as an Early Deterioration Signal

Respiratory rate is among the most powerful predictors of clinical deterioration in hospitalized patients — yet it remains the least reliably measured and documented of the conventional vital signs.

In an early landmark case-control study (Fieselmann et al., 1993; N = 59 arrest cases, 91 matched controls), a single RR > 27 breaths/min in the 72 hours before arrest predicted cardiopulmonary arrest with OR 5.56 (95% CI 2.67–11.49; sensitivity 0.54, specificity 0.83) [7, cohort]. Crucially, pulse rate and blood pressure were not predictive of arrest in the same cohort — RR stood alone. Subsequent work by Goldhill and colleagues found that 21% of ward patients with a RR of 25–29 breaths/min — assessed by a critical care outreach service — died in hospital, a figure that rose with higher rates [11, cohort].

This evidence is formalized in the **National Early Warning Score 2 (NEWS2)**, the UK Royal College of Physicians' standardized acute-illness severity tool, adopted across NHS England and NHS Improvement for identifying acutely ill patients including those with sepsis [9, regulatory]. In NEWS2, RR is scored as follows:

| RR (breaths/min) | NEWS2 points |
|---|---|
| ≤ 8 | 3 |
| 9–11 | 1 |
| 12–20 | 0 (normal) |
| 21–24 | 2 |
| ≥ 25 | 3 |

A score of 3 on any single parameter — which RR achieves at both the very low and high ends — triggers an urgent clinical response independent of total score. A total NEWS2 score ≥ 7 requires emergency assessment with critical care involvement. RR is described in NEWS2 guidance as the most sensitive early indicator of clinical deterioration, with a rising rate often preceding other physiological changes by hours.

Despite this, respiratory rate has been documented as the vital sign most likely to be omitted or inaccurately recorded in clinical practice. Palmer et al. (2023) — an integrative review of 19 studies across acute care settings — found that RR was "consistently the least frequently measured and accurately documented vital sign," with nurses frequently entering values into charts without performing a count [10, mechanism_review]. An earlier editorial synthesis by Cretikos et al. (2008) titled "Respiratory rate: the neglected vital sign" summarized multicentre evidence that documentation of vital signs in many hospitals was extremely poor, with RR in particular often absent even when the patient's primary problem was respiratory [8, mechanism_review].

### 2. Wearable Early-Illness Detection: The Marquee Consumer Application

For healthy individuals using consumer wearables (Oura, Fitbit, WHOOP, Garmin, and others), elevated nocturnal RR versus personal baseline is among the most actionable illness-detection signals these devices can provide. During sleep, motion artifact is minimized and the signal is relatively stable, making it the preferred window for PPG-derived RR measurement.

The evidence base is real but requires honest framing. The Natarajan et al. (2021) Fitbit study [1, cohort] and the TemPredict/Oura study [2, cohort] demonstrate that multi-signal wearable algorithms — incorporating RR alongside temperature, HRV, and heart rate — can detect illness around or before symptom onset with meaningful AUC values (0.77–0.82). However, RR alone does not function as a diagnostic test: the Mitratza et al. (2022) Lancet Digital Health review [3, meta_analysis] reports that across the broader wearable COVID-detection literature, model AUCs span a wide range (0.52–0.92), reflecting heterogeneous populations, device types, and reference standards.

**False positives are common.** Alcohol consumption, a late or heavy meal, elevated ambient room temperature, vigorous late-evening training, and heat illness all raise nocturnal RR without any infectious cause. This means a single elevated reading carries low specificity. The appropriate interpretation is *sustained elevation above personal baseline (typically 2–3+ breaths/min for multiple consecutive nights), in conjunction with other signals (resting HR elevation, HRV depression, temperature rise, sleep disruption)*.

### 3. Sleep-Disordered Breathing

Some wearable devices (Withings, Oura Gen 3+, Garmin) track RR variability across the night to flag potential obstructive sleep apnea patterns — specifically, the periodic fluctuations in RR associated with respiratory events. This is an emerging application; devices are not FDA-cleared diagnostic tools, and anyone with suspected sleep apnea requires formal polysomnography.

---

## Limitations

**Consumer-grade RR is a nocturnal estimate, not a continuous ventilation measurement.** Wearable PPG-derived RR is computed from respiratory sinus arrhythmia in the heart rate signal during sleep. It does not measure tidal volume, minute ventilation, or breathing pattern quality — all clinically meaningful. A normal RR does not exclude pathological breathing (e.g., Cheyne-Stokes, Kussmaul, or obstructive apneas with normal mean rate).

**PPG-RR degrades with motion and arrhythmia.** During movement or in patients with atrial fibrillation, the RSA-based RR estimate becomes unreliable. Wearable RR is best interpreted during confirmed sleep periods.

**Single nocturnal readings have high false-positive rates for illness.** As noted above, alcohol, heat, overtraining, and stress all elevate nocturnal RR. No single reading should be acted upon in isolation.

**This is a wellness and trend metric, not a diagnostic test.** Consumer wearable RR is appropriate for personal trend monitoring and population-level research; it is not a clinical measurement and cannot substitute for bedside respiratory rate counting (one full minute) in any clinical context.

---

## Bibliography

1. Natarajan A, Su HW, Heneghan C, Blunt L, O'Connor C, Niehaus L. Measurement of respiratory rate using wearable devices and applications to COVID-19 detection. *NPJ Digit Med*. 2021;4(1):136. doi:10.1038/s41746-021-00493-6. PMID: 34526602 — tag: cohort — tier: 2. Note: study used Fitbit devices; authors include employees of Google (Fitbit parent); device-affiliated funding context applies.

2. Mishra T, Wang M, Metwally AA, et al. Detection of COVID-19 using multimodal data from a wearable device: results from the first TemPredict Study. *Sci Rep*. 2022;12:4349. doi:10.1038/s41598-022-07314-0. PMID: 35236896 — tag: cohort — tier: 2. Note: study used Oura Ring devices; conducted at UCSF with Oura Health collaboration; device-affiliated funding context applies.

3. Mitratza M, Goodale BM, Shagadatova A, et al. The performance of wearable sensors in the detection of SARS-CoV-2 infection: a systematic review. *Lancet Digit Health*. 2022;4(6):e410–e425. doi:10.1016/S2589-7500(22)00019-X. PMID: 35461692 — tag: meta_analysis — tier: 1

4. Khanna AK, Bergese SD, Jungquist CR, et al. Prediction of opioid-induced respiratory depression on inpatient wards using continuous capnography and oximetry: an international prospective, observational trial. *Anesth Analg*. 2020;131(4):1012–1024. doi:10.1213/ANE.0000000000004788. PMID: 32925318 — tag: cohort — tier: 2

5. Khanna AK, Saager L, Bergese SD, et al. Opioid-induced respiratory depression increases hospital costs and length of stay in patients recovering on the general care floor. *BMC Anesthesiol*. 2021;21(1):88. doi:10.1186/s12871-021-01307-8. PMID: 33743588 — tag: cohort — tier: 2

6. Doufas AG, Laporta ML, Driver CN, et al. Incidence of postoperative opioid-induced respiratory depression episodes in patients on room air or supplemental oxygen: a post-hoc analysis of the PRODIGY trial. *BMC Anesthesiol*. 2023;23:332. doi:10.1186/s12871-023-02291-x. PMID: 37794334 — tag: cohort — tier: 2

7. Fieselmann JF, Hendryx MS, Helms CM, Wakefield DS. Respiratory rate predicts cardiopulmonary arrest for internal medicine inpatients. *J Gen Intern Med*. 1993;8(7):354–360. doi:10.1007/BF02600071. PMID: 8410395 — tag: cohort — tier: 2

8. Cretikos MA, Bellomo R, Hillman K, Chen J, Finfer S, Flabouris A. Respiratory rate: the neglected vital sign. *Med J Aust*. 2008;188(11):657–659. doi:10.5694/j.1326-5377.2008.tb01825.x. PMID: 18513176 — tag: mechanism_review — tier: 3

9. Royal College of Physicians. National Early Warning Score (NEWS) 2: Standardising the assessment of acute-illness severity in the NHS. London: RCP; December 2017. — tag: regulatory — tier: 1

10. Palmer JH, James S, Wadsworth D, Gordon CJ, Craft J. How registered nurses are measuring respiratory rates in adult acute care health settings: An integrative review. *J Clin Nurs*. 2023;32(15-16):4515–4527. doi:10.1111/jocn.16522. PMID: 36097417 — tag: mechanism_review — tier: 3

11. Goldhill DR, McNarry AF, Mandersloot G, McGinley A. A physiologically-based early warning score for ward patients: the association between score and outcome. *Anaesthesia*. 2005;60(6):547–553. doi:10.1111/j.1365-2044.2005.04186.x. PMID: 15918825 — tag: cohort — tier: 2
