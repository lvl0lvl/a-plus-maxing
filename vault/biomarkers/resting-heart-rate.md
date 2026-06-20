---
title: Resting Heart Rate (RHR)
type: biomarker
permalink: a-plus-maxing/biomarkers/resting-heart-rate
category: wearable
unit: bpm
source: wearable
confidence: established
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.resting-heart-rate-design-work
provenance_slug: labs-specialist
---

# Resting Heart Rate (RHR)

## Metadata
- category: wearable
- unit: bpm (beats per minute)
- source: wearable (consumer PPG device — ring, wrist, or chest strap; most devices report a nocturnal-minimum or lowest-window HR via photoplethysmography; the definition varies by device and is not interchangeable across manufacturers)
- confidence: established (RHR physiology is well-characterized; population norms and prognostic associations are robustly replicated across large cohorts; consumer PPG accuracy at rest is well-validated; this metric is more population-interpretable than HRV because absolute levels carry meaning, not just personal-baseline deviation)
- review_cadence: per-wearable-sync
- last_verified: 2026-06-20
- assay note: Consumer PPG-derived RHR is accurate for heart rate at rest (MAE ~2 bpm vs. ECG reference). It is NOT an FDA-cleared diagnostic test. Proprietary RHR algorithms differ across brands (nocturnal minimum, lowest 30-minute average, overnight continuous average, etc.) — do not compare numeric values across devices.

## Target Range
- ideal: 50–65 bpm in the context of aerobic fitness; lower-within-physiological-range generally tracks better CV fitness and lower mortality risk
- acceptable: 60–100 bpm (conventional clinical normal); <60 bpm common and expected in aerobically trained individuals (endurance athletes 40–55 bpm; >38% of elite endurance athletes have minimum HR ≤40 bpm on Holter)
- alert: >100 bpm at rest (resting tachycardia — warrants evaluation for reversible causes); <50 bpm in a sedentary, symptomatic, or non-athletic individual (warrants ECG and clinical context); a sustained rise of ≥5–7 bpm above your personal rolling baseline on a consistent device (acute illness, overtraining, or alcohol signal)
- note on athletic bradycardia vs. pathological bradycardia: an RHR of 42 bpm in an asymptomatic endurance athlete is physiological (HCN4 sinus-node remodeling from training); the same value in a sedentary or symptomatic person requires clinical evaluation — symptom-rhythm correlation determines significance, not the number alone
- source of target: [[library/biomarkers/resting-heart-rate/research-report]]; 2018 ACC/AHA/HRS Guideline on Bradycardia and Cardiac Conduction Delay (Kusumoto FM et al., Heart Rhythm 2019, PMID:30412778)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — wearable export

## Affected By

RAISES (higher RHR vs. your baseline or vs. population range):
- acute psychological or physical stress (sympathoadrenal activation, vagal withdrawal)
- ILLNESS/infection — one of the most reliable and earliest acute elevators; RHR often rises ~2 days before ILI symptom onset and takes ~10 days to return to baseline
- ALCOHOL — dose-related acute nocturnal elevation (~+3 bpm after moderate consumption); a robust and reproducible overnight wearable signal of impaired recovery
- overtraining / under-recovery / high acute training load (morning RHR above rolling baseline is a validated load-management signal)
- poor, short, or fragmented sleep
- caffeine and stimulants (most pronounced in non-habituated individuals), nicotine
- dehydration and heat stress (increased resting cardiac output demand)
- deconditioning (loss of stroke-volume efficiency)
- hyperthyroidism, anemia, fever from any cause
- certain medications: bronchodilators, stimulant medications, some antidepressants
- [[protocols/exercise]] (acute heavy session raises; overtraining raises chronically)
- [[protocols/sleep]]

LOWERS (lower RHR vs. your baseline or vs. population range):
- aerobic fitness and endurance training — the dominant chronic determinant; training causes intrinsic HCN4 sinus-node channel downregulation (not merely increased vagal tone); the bradycardia is reversible with detraining
- adequate recovery between training sessions
- good sleep quality and duration
- beta-adrenergic blockers (pharmacological sympathetic attenuation — note: pharmacologically lowering RHR in stable CAD did not improve outcomes in SIGNIFY; this is a blocker effect, not a fitness effect)
- [[protocols/exercise]]
- [[protocols/sleep]]

## Why It Matters
RHR is a cheap, robust window on cardiovascular fitness, autonomic state, and day-to-day recovery. It is one of the few wearable metrics for which both the absolute level and the deviation from personal baseline are independently meaningful: the absolute level tracks aerobic fitness trajectory and long-term cardiovascular risk, while an acute rise above your rolling baseline flags illness onset (often before symptoms), alcohol exposure, overtraining, or poor sleep. Elevated resting HR is robustly and dose-dependently associated with cardiovascular and all-cause mortality across large population cohorts — approximately +1.09–1.17 relative risk per 10 bpm increase across two major meta-analyses (112,680–1.25M participants), with RHR >80 bpm associated with ~54% higher all-cause mortality vs. RHR <65 bpm. These associations are stronger and more population-applicable than HRV for CV risk stratification. However, RHR is a **marker, not a confirmed modifiable target**: the SIGNIFY trial (n=19,102 stable CAD patients, elevated RHR) showed that pharmacologically lowering HR with ivabradine produced no reduction in cardiovascular death or MI (HR 1.08, 95% CI 0.96–1.20). The path to benefit from a lower RHR runs through the fitness, sleep, and lifestyle changes that lower it physiologically — not through rate suppression alone. Consumer RHR is accurate for heart rate but interpret trends vs. your own baseline under consistent conditions (same device, same measurement window); athletic bradycardia is not pathological bradycardia.

## Relations
- [[biomarkers/hrv]]
- [[biomarkers/sleep-efficiency]]
- [[protocols/exercise]]
- [[protocols/sleep]]
- [[library/biomarkers/resting-heart-rate/research-report]]
