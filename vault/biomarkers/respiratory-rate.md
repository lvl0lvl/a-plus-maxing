---
title: Respiratory Rate (RR)
type: biomarker
permalink: a-plus-maxing/biomarkers/respiratory-rate
category: wearable
unit: breaths/min
source: wearable
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.respiratory-rate-design-work
provenance_slug: labs-specialist
---

# Respiratory Rate (RR)

## Metadata
- category: wearable
- unit: breaths/min (RR is a WEARABLE vital sign — consumer devices derive a single nocturnal average from PPG respiratory modulation during sleep; accurate at rest [±1 brpm MAE vs PSG], NOT a diagnostic ventilation measure; does not capture tidal volume, minute ventilation, or apnea events)
- source: wearable (PPG-derived, sleep window only; proprietary algorithm; cross-device absolute values not comparable — track within-device trend vs personal baseline)
- confidence: established (RR is a well-established vital sign with robust population norms, strong clinical-prognostic evidence, and good PPG accuracy at rest; NEWS2-anchored norm; multiple independent cohort validations)
- review_cadence: per-wearable-sync
- last_verified: 2026-06-20

## Target Range
- ideal: 12–20 breaths/min (RCP NEWS2 normal range — scores 0 / no concern)
- acceptable: 12–20 breaths/min; personally, the key signal is YOUR own rolling baseline (30-night average same device)
- alert: >20–24 brpm = tachypnea (NEWS2 score 2); >24 brpm = urgent (NEWS2 score 3); <12 brpm = bradypnea (NEWS2 score 3 at ≤8); WEARABLE alert: sustained rise of 2–3+ brpm above personal baseline for 1–2 consecutive nights — even if still within the "normal" population range
- source of target: [[library/biomarkers/respiratory-rate/research-report]]; Royal College of Physicians NEWS2 2017

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — wearable export

## Affected By

RAISES RR (nocturnal average rises above personal baseline):
- FEVER / ILLNESS / infection — among the most reliable early signals; RR often rises 1–3 days before symptom awareness; the primary wearable use-case
- exertion — vigorous late training can elevate nocturnal RR (physiological; resolves in 1–2 nights)
- anxiety / stress / panic — neurogenic hyperventilation; elevated nocturnal RR on stressful days
- pain — sympathetic activation
- metabolic acidosis (DKA / Kussmaul breathing) — compensatory respiratory alkalosis; RR may exceed 25–30 brpm
- hypoxia / altitude / cardiorespiratory disease (asthma, COPD, pneumonia, PE, heart failure) — impaired gas exchange drives ventilatory compensation
- ALCOHOL — disrupts sleep architecture; raises nocturnal RR (a common false-positive for illness signal)
- pregnancy — mild sustained increase (~1–2 brpm) via progesterone chemoreceptor sensitization
- stimulants (caffeine, amphetamines) — sympathomimetic; transient
- heat (elevated room temperature, late heat exposure) — common false-positive
- [[protocols/sleep]]

LOWERS RR (a safety signal — respiratory depression):
- OPIOIDS / sedatives / anesthesia — μ-receptor suppression in brainstem respiratory centers; OIRD (opioid-induced respiratory depression) is a major clinical hazard; OR 6.07 for high-risk vs low-risk patients on parenteral opioids (PRODIGY trial); consumer wearables may miss apneic episodes
- benzodiazepines / barbiturates — CNS depression
- hypothyroidism (severe / myxedematous) — reduced metabolic rate, possible hypoventilation
- sleep — modest physiological reduction (~1–2 brpm below waking); the basis for nocturnal measurement
- slow-breathing practice (pranayama, resonance breathing) — intentional 4–8 brpm; physiologically distinct from pathological suppression

## Why It Matters
Respiratory rate is one of the four classic vital signs and a powerful but chronically underused predictor of clinical deterioration — the first vital sign to change before cardiac arrest or ICU transfer, and the most heavily weighted single parameter in the NHS NEWS2 early-warning score. A single RR > 27 brpm predicted cardiopulmonary arrest with OR 5.56 in hospitalized patients (Fieselmann 1993); mortality at 25–29 brpm reached 21% on the ward (Goldhill 2005). Despite this, RR is the least reliably measured and charted vital sign in clinical practice, with nurses frequently entering default values rather than counting. For consumer wearable users, the value is different but equally compelling: nocturnal RR is remarkably stable within an individual (within-person CV ~2–10% in younger adults; nightly LoA −0.07 to −0.04 brpm in one 3-month study), making it among the most sensitive wearable early-illness signals. Wearable studies show nocturnal RR rises around or before symptom onset in respiratory infections, with multi-signal algorithms (RR + temperature + HRV) detecting COVID-19 a mean of 2.75 days before testing (AUC 0.819). The actionable frame is always personal-baseline deviation — a sustained rise of 2–3+ brpm above your own 30-night average on consecutive nights, combined with HR elevation and HRV depression, is an early illness flag worth noting. False positives are common (alcohol, heat, late heavy meals, hard training all raise nocturnal RR without infection), so no single reading is diagnostic. On the opposite end, opioids and sedatives lower RR via brainstem suppression — OIRD is a serious clinical hazard that wearable spot-checks miss (apneic episodes, not just low mean RR). Consumer wearable RR is an accurate-at-rest wellness and trend metric (±1 brpm MAE vs PSG under low-motion conditions), not a diagnostic test; it does not replace bedside counting or formal polysomnography, and should be read as trend vs personal baseline, not as an absolute clinical reading.

## Relations
- [[biomarkers/hrv]]
- [[biomarkers/resting-heart-rate]]
- [[biomarkers/sleep-efficiency]]
- [[protocols/sleep]]
- [[library/biomarkers/respiratory-rate/research-report]]
