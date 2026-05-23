---
title: Operator Profile
type: note
permalink: a-plus-maxing/meta/operator-profile
status: scaffold
created: 2026-05-23
last_reviewed: 2026-05-23
review_cadence: quarterly (or on material change)
---

# Operator Profile — Walter

Slow-changing context the research agent must anchor every dispatch to. Auto-loaded by `aplus-research` (once built); manually pasted into any `deep-research` dispatch in the interim.

If a field is unknown, leave the prompt in place — do NOT delete it. The agent treats unfilled fields as HALT conditions for compounds whose risk class depends on them.

---

## Demographics
- **Sex:** <M | F>
- **Age:** <years>  (DOB if you want auto-update: <YYYY-MM-DD>)
- **Height:** <cm / in>
- **Weight:** <kg / lbs>  → tracked over time in `current-state.md`
- **Body composition:** <body fat % if known, source: DEXA | bioimpedance | estimate>
- **Ancestry:** <relevant to DNA variant interpretation>

## Training history
- **Years training:** ~20
- **Modalities:** <strength | endurance | hybrid | combat sports | other>
- **Current training status:** <active | rebuilding post-injury | deconditioned post-illness | other>
- **Home gym equipment:** <one line — full home gym per memory>
- **Notable historical PRs / capacity markers:** <so research can calibrate "elite vs novice" claims>

## Current physical state
- **Resting HR:** <bpm — fill from Oura when available>
- **Blood pressure:** <systolic/diastolic, last measured YYYY-MM-DD>
- **Subjective energy 1-10:** <today's number>
- **Subjective recovery 1-10:** <today's number>
- **Pain / injury map:** <body region: status, e.g., "left Achilles: chronic tendinopathy, post-January illness deconditioning">

## January 2026 health issue (REQUIRED — load-bearing for safety filtering)
- **System affected:** <cardiovascular | metabolic | neurological | immune | endocrine | GI | other>
- **Diagnosis (if any):** <ICD-10 or layperson term>
- **Suspected cause:** <known | unknown>
- **Current status:** <resolved | improving | stable | ongoing>
- **Active medications:** <list — name, dose, frequency, prescriber>
- **Diagnostic tests run:** <list with dates and results pointer to `vault/labs/`>
- **Contraindicated systems for intervention:** <e.g., "anything affecting clotting" or "anything affecting <organ>" — what to avoid until cleared by MD>
- **MD follow-up scheduled:** <date>

> Until this section is populated, the research agent must treat ALL `risk_tier: medium+` compounds as HALT.

## Current prescriptions / OTC medications
- <drug, dose, frequency, indication, prescriber>
- <drug, dose, frequency, indication, prescriber>

## Known allergies / sensitivities
- <substance — reaction severity — confirmed/suspected>

## Known DNA variants of note
Source: 23andMe raw file → parsed in `vault/dna/analysis.md` when ingested.
- <rsID — gene — variant — clinical implication> (populate after parsing)

## Lifestyle baseline
- **Sleep:** <typical bedtime / wake, hours, location quality (dark/quiet)>
- **Alcohol:** <drinks/week>
- **Caffeine:** <mg/day, cutoff time>
- **Nicotine / other recreational:** <none | specify>
- **Stress baseline 1-10:** <number>
- **Work demands:** <sedentary / physical / cognitive load>

## Medical relationship
- **Primary care MD:** <name | none — first visit July 2026 per HANDOFF>
- **Insurance coverage status:** <relevant for Rx access — full | limited | cash-pay>
- **Compounding pharmacy access:** <yes/no, vendor names if yes>
- **Bloodwork access:** <MD-ordered | direct-to-consumer (Marek, Function, Empower) | both>

## Risk posture
- **Self-experimentation comfort:** <conservative | moderate | aggressive>
- **Off-label / gray-market compounds:** <willing under what conditions>
- **n=1 cycle length willing to commit:** <typical weeks before judging>
- **Stopping threshold:** <any subjective effect | adverse lab | sustained adverse symptom>

---

## How the agent uses this file

Per dispatch the agent extracts:
- Population-match relevance (age, sex, training status) — for filtering study generalization
- Active contraindications (Jan 2026 issue, prescriptions, allergies, DNA variants)
- Risk-tier ceiling (risk posture + MD access)
- Trial-design parameters (cycle length, stopping threshold)

If the dispatch lacks an operator-profile reference, it must HALT with `operator-profile-missing`.
