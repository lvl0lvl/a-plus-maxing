---
title: Recovery & Strain Scores
type: biomarker
permalink: a-plus-maxing/biomarkers/recovery-strain
category: wearable
unit: score
source: wearable
confidence: provisional
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-wearable-sync
provenance_dir: design/.recovery-strain-design-work
provenance_slug: labs-specialist
---

# Recovery & Strain Scores

## Metadata
- category: wearable
- unit: score — brand-specific scale (WHOOP Recovery 0–100% / Strain 0–21 logarithmic; Oura Readiness 1–100; Garmin Body Battery 0–100); these are PROPRIETARY COMPOSITE indices of validated inputs (nocturnal HRV, RHR, sleep, respiratory rate), NOT a measured physiological quantity and NOT interchangeable across brands
- source: wearable (composite output; algorithm undisclosed, firmware-modifiable; trends within the same device meaningful; cross-brand absolute values are not comparable)
- confidence: provisional — the individual inputs (HRV/RHR/sleep) are validated, but the composite score itself is largely NOT independently validated as a predictor of readiness or performance; proprietary algorithms prevent audit; sparse and mixed independent evidence; this is the lowest confidence of the wearable cluster
- review_cadence: per-wearable-sync
- last_verified: 2026-06-20

## Target Range
- ideal: no universal population norm exists — recovery/strain scores are personal-baseline-relative; "green/high" (WHOOP ≥67%, Oura ≥85, Garmin ≥75) is a signal you are above YOUR own rolling baseline, not an absolute threshold
- acceptable: any score interpreted as a trend vs your own rolling baseline (typically 14–30 day window per device); the key action is checking WHICH input drove a low score (HRV? RHR? sleep duration?) — that determines the response, not the headline number
- alert: sustained multi-day depression of the composite alongside converging low HRV + elevated RHR + poor sleep = meaningful fatigue or illness signal; single-day red scores without a clear behavioral cause warrant attention; no validated clinical threshold exists
- source of target: [[library/biomarkers/recovery-strain/research-report]]; all targets are personal-baseline-relative, NOT absolute population reference values

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — wearable export

## Affected By

LOWERS recovery / worsens the composite score:
- ALCOHOL — most reproducible acute suppressor; controlled ethanol studies show RMSSD falls, HF power drops, LF/HF rises, RHR rises; large real-world dataset (N = 4,098) shows recovery decreases 9.3 / 24.0 / 39.2 percentage units at low / moderate / high intake; the single most actionable lever for adults who drink
- poor or short sleep — the dominant input; partial sleep deprivation (3 hrs/night x 3 nights) significantly depresses parasympathetic HRV indices; the composite is largely measuring what the nocturnal HRV measured
- high training load / overreaching — vagal HRV decreases and RHR rises; resting HRV correlates with non-functional overreaching (r = 0.88)
- illness / infection — sympathetic activation via inflammatory/cytokine pathways depresses HRV, often before overt symptoms; the primary early-warning use case
- acute psychological stress — vagal withdrawal; sympathetic activation persisting into early sleep
- heat and dehydration — raise sympathetic tone and RHR
- late meals close to sleep — metabolic load shifts autonomic balance during early sleep
- age — HRV declines nonlinearly after young adulthood; personal baseline tracks this drift
- deconditioning — blunts resting parasympathetic tone
- [[protocols/sleep]], [[protocols/exercise]]

RAISES recovery / improves the composite score:
- sufficient, high-quality sleep — the dominant restorer; nocturnal HRV measurement is taken during sleep
- rest days / reduced training load — parasympathetic rebound; RMSSD returns toward baseline within 24–48 hrs of low-intensity loading
- aerobic fitness and training adaptation — meta-analysis of RCTs (26 studies, N = 649 sedentary individuals) shows exercise training increases RMSSD (SMD = 0.57) and HF power (SMD = 0.21); a fitter person has a structurally higher score ceiling
- abstaining from alcohol — night-to-night improvement in nocturnal HRV visible in large real-world datasets
- recovery practices (cold water immersion, light flush work, adequate nutrition) — supporting evidence exists but effect sizes on HRV specifically are smaller and less consistent than sleep/alcohol effects
- [[protocols/sleep]], [[protocols/exercise]]

## Why It Matters
A recovery/strain score is a convenience aggregation of validated physiological inputs — primarily nocturnal HRV, resting heart rate, sleep, and respiratory rate — into a single branded readiness or load number. The central honesty: the inputs are validated; the composite score itself is largely NOT independently validated as a readiness or performance predictor. The algorithms are proprietary, undisclosed, and firmware-modifiable, meaning the score can shift with a software update independent of any physiological change; WHOOP's Strain composite had "presently unknown" validity as of the most recent relevant study, and the Recovery Score composite was explicitly described as outside the scope of the most rigorous independent hardware validation and in need of future research. Independent studies show WHOOP's composite Strain and Recovery scores had no significant correlations with validated psychological recovery scales, resting metabolic rate, or triiodothyronine in competitive swimmers, while HRV alone showed the expected weak-to-moderate associations — the composite added nothing. Cross-device scores correlate only r = 0.41 despite ostensibly measuring the same construct; they are not interchangeable. There is no population norm — the score is meaningful only relative to your own rolling baseline. The scientific support for HRV-guided training is modest (meta-analyses show small, not consistently statistically significant VO₂max advantages; Manresa-Rocamora: SMD = 0.13 for VO₂max; Granero-Gallegos: ES = 0.402 vs 0.215), and critically that evidence is for raw HRV protocols, not branded composites — no RCT has tested whether acting on a WHOOP/Oura/Garmin score improves outcomes. The actionable information lives in the inputs: a low score is most useful when you identify which input drove it (sleep? HRV? RHR?). Useful as a personal-trend nudge and behavior-change motivator (RCT evidence supports feedback-driven improvements in sleep, activity, and VO₂max), but not a measured physiological quantity or diagnostic. The over-reliance and score-anxiety risk is real: cross-sectional data link wearable score preoccupation with higher insomnia and anxiety scores, and a pattern analogous to orthosomnia has been documented with recovery metrics.

## Relations
- [[biomarkers/hrv]]
- [[biomarkers/resting-heart-rate]]
- [[biomarkers/sleep-efficiency]]
- [[biomarkers/respiratory-rate]]
- [[protocols/exercise]]
- [[protocols/sleep]]
- [[library/biomarkers/recovery-strain/research-report]]
