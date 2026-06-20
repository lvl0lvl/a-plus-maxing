---
title: Sleep Efficiency
type: biomarker
permalink: a-plus-maxing/biomarkers/sleep-efficiency
category: wearable
unit: "%"
source: wearable
confidence: supported
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.sleep-efficiency-design-work
provenance_slug: labs-specialist
---

# Sleep Efficiency

## Metadata
- category: wearable
- unit: % (percentage; SE = TST ÷ TIB × 100 — a sleep-continuity metric, not a staging metric)
- source: wearable (consumer PPG + accelerometry device; proprietary algorithm, not EEG-based; consumer devices OVERESTIMATE SE vs. PSG — they miss quiet wakefulness; sleep staging percentages are additionally unreliable [~65–75% accuracy])
- confidence: supported (the ≥85% population norm is well-established in PSG normative literature; however, consumer wearable SE is a biased upward estimate of true SE — a wearable's SE reads higher than a simultaneous PSG SE — so the metric is not population-calibrated at face value; NOT a diagnostic test)
- review_cadence: per-wearable-sync
- last_verified: 2026-06-20

## Target Range
- ideal: ≥85% is the conventional "good" / normal SE threshold in healthy adults (NSF expert consensus); most healthy adults land 85–95%
- acceptable: 80–84% may be within age-adjusted normal for adults ≥60 (SE declines ~2.1%/decade); SE declines with age — interpret with age context
- alert: <80% sustained over ≥5 nights warrants investigation (insomnia pattern); a drop of ≥5–8 percentage points below your personal rolling baseline (7–14 nights same device) flags an acute disruptor
- wearable calibration note: consumer devices overestimate SE — a device reading of 90% may correspond to a true PSG SE of ~80%; do NOT compare across devices or treat the absolute number as a PSG-equivalent reading
- source of target: [[library/biomarkers/sleep-efficiency/research-report]]; Ohayon 2017 NSF consensus (PMID 28346153); Boulos 2019 normative meta-analysis (PMID 31006560)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — wearable export

## Affected By

LOWERS SE (more wake time in bed):
- insomnia disorder (high SOL or WASO — cardinal SE-lowering condition)
- excessive time in bed relative to actual sleep need (dilutes homeostatic sleep pressure — counter-intuitive; more TIB → lower SE)
- aging (SE declines ~2.1%/decade; WASO rises ~9.7 min/decade)
- ALCOHOL — fragments second half of night via sympathetic rebound as ethanol clears; drops SE even when it accelerates sleep onset
- caffeine and nicotine (adenosine antagonism / stimulant arousal)
- stress, anxiety, cognitive hyperarousal (extends SOL; increases nocturnal arousals)
- obstructive sleep apnea / periodic limb movement disorder (repetitive arousals)
- circadian misalignment (shift work, jet lag, delayed/advanced sleep phase)
- pain, nocturia, ambient noise / light / heat
- certain medications (some antidepressants, beta-blockers, corticosteroids, decongestants)
- [[protocols/sleep]]

RAISES SE (less wake time, more consolidated sleep):
- CBT-I / sleep restriction therapy (the single most evidence-supported lever; Hedges' g = 0.91 vs. control across 8 RCTs)
- stimulus control (reconditions the bed–sleep association)
- regular sleep/wake schedule; adequate sleep pressure at bedtime
- dark, cool, quiet sleep environment
- aerobic exercise (improves sleep depth and continuity)
- treating underlying OSA or PLMD
- [[protocols/sleep]]

## Why It Matters
Sleep efficiency is the primary quantitative index of sleep continuity — how much of the time in bed is spent actually asleep — and is among the two parameters with highest expert consensus as indicators of sleep quality across the adult lifespan. It is the central outcome metric of CBT-I, the most evidence-based treatment for chronic insomnia, where raising SE from below to above 85% is both a mechanism and a goal. Consumer wearables systematically overestimate SE because they cannot detect quiet wakefulness — a person lying still but awake looks like a sleeping person to an accelerometer. A device SE reading will reliably be a few to many percentage points higher than what PSG would record the same night, with the gap widening on nights with the worst true continuity. Sleep staging numbers (light/deep/REM) are even less reliable (~65–75% accuracy vs. PSG epoch-by-epoch). The actionable signal from a wearable SE is therefore the personal-baseline trend — a drop of ≥5–8 percentage points below your own stable average flags alcohol, illness, stress, or environmental disruption — not the absolute number compared against population norms. SE is necessary but not sufficient: a person with 5.5 hours in bed and 95% SE is sleep-deprived; stage composition can be poor even with high SE. The orthosomnia caveat applies: preoccupation with tracker sleep scores can itself worsen sleep and generate anxiety; if the number is causing distress rather than insight, the tracker is counterproductive. The hard-outcome epidemiology (cardiovascular, mortality) mostly uses sleep duration and questionnaire-based quality, not wearable SE — so do not treat the nightly number as an individual health-risk readout.

## Relations
- [[biomarkers/hrv]]
- [[biomarkers/resting-heart-rate]]
- [[biomarkers/respiratory-rate]]
- [[protocols/sleep]]
- [[library/biomarkers/sleep-efficiency/research-report]]
