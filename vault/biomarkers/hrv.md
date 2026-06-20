---
title: Heart Rate Variability (HRV)
type: biomarker
permalink: a-plus-maxing/biomarkers/hrv
category: wearable
unit: ms
source: wearable
confidence: supported
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.hrv-design-work
provenance_slug: labs-specialist
---

# Heart Rate Variability (HRV)

## Metadata
- category: wearable
- unit: ms (rMSSD primary; SDNN secondary — both in milliseconds)
- source: wearable (consumer PPG device — ring, wrist, or chest strap)
- confidence: supported (HRV physiology is well-established; consumer PPG validity for rMSSD during sleep is good-to-excellent; interpretation is individual-baseline-dependent, not fixed-range)
- review_cadence: per-wearable-sync
- last_verified: 2026-06-20
- assay note: Most consumer devices report nocturnal rMSSD or a derived readiness score from PPG. This is NOT an FDA-cleared diagnostic test. The metric is pulse rate variability (PRV), technically distinct from ECG-derived HRV, though a useful surrogate under resting/sleep conditions. Proprietary algorithms differ across brands — do not compare numeric values across devices.

## Target Range
- ideal: no universal cutoff — HRV is enormously inter-individual and age/sex-dependent; rMSSD spans ~15–100+ ms across healthy adults (four-fold lifespan decline from adolescence to age 75+)
- acceptable: YOUR rolling 7–30 day personal baseline on a consistent device and condition; ±12–15% day-to-day variation is normal noise
- alert: sustained multi-day depression >20–30% below your personal rolling baseline, especially with concurrent elevated resting HR, poor sleep, or high training load
- source of target: [[library/biomarkers/hrv/research-report]] — the actionable signal is deviation from personal baseline, not an absolute number; higher-vs-your-baseline ≈ better autonomic recovery; lower-vs-your-baseline ≈ stress, under-recovery, illness, or alcohol

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — wearable export

## Affected By

RAISES (higher HRV vs. your baseline):
- aerobic fitness and regular endurance training (chronic vagal adaptation — the strongest chronic determinant)
- adequate and high-quality sleep (deep NREM sleep = intense parasympathetic dominance)
- well-recovered physiological state (rest between training sessions)
- slow-paced breathing (~5–6 breaths/min acutely amplifies RSA)
- youth (HRV declines progressively from the third decade onward)
- beta-adrenergic blockers (pharmacological sympathetic attenuation)
- [[protocols/exercise]]
- [[protocols/sleep]]

LOWERS (suppressed HRV vs. your baseline):
- ALCOHOL — large acute overnight suppression (dose-dependent: −2 to −13 ms rMSSD; one of the most reproducible wearable signals)
- ILLNESS/infection — HRV drop often precedes overt symptoms by ~1 day
- overtraining / under-recovery / high acute training load
- poor, short, or fragmented sleep
- acute psychological stress (sympathetic activation, vagal withdrawal)
- dehydration and heat exposure
- aging (chronic progressive decline)
- anticholinergic medications (muscarinic blockade)
- [[protocols/exercise]]
- [[protocols/sleep]]

## Why It Matters
HRV is a non-invasive window on autonomic parasympathetic/vagal tone and day-to-day recovery readiness. The most reproducible and interpretable signals for a healthy individual are: the acute alcohol overnight suppression (large, consistent, dose-dependent), the pre-symptomatic illness drop (often detectable before you feel sick), and the overtraining/under-recovery decline (sustained depression that co-occurs with elevated resting HR and poor sleep). Low HRV is associated with elevated cardiovascular event risk and all-cause mortality in epidemiologic cohorts — hazard ratios of 1.35–1.56 for the lowest vs. highest SDNN/rMSSD strata — but that evidence is from clinical short-ECG recordings, not consumer wearable PPG, and is observational; consumer HRV is a wellness/trend metric, not a diagnostic test. Interpret HRV as a trend relative to your own rolling baseline under consistent measurement conditions (same device, same time of day, same posture), not against a population cutoff. A single isolated reading is near-uninterpretable; a sustained 10–14 day downward trend co-occurring with elevated resting HR, poor sleep, and declining training performance is a convergent signal worth acting on.

## Relations
- [[biomarkers/resting-heart-rate]]
- [[biomarkers/sleep-efficiency]]
- [[protocols/exercise]]
- [[protocols/sleep]]
- [[library/biomarkers/hrv/research-report]]
