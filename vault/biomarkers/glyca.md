---
title: GlycA — Glycoprotein Acetylation
type: biomarker
permalink: a-plus-maxing/biomarkers/glyca
category: blood
unit: mmol/L
source: lab
confidence: provisional
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: per-lab-panel
provenance_dir: design/.glyca-design-work
provenance_slug: labs-specialist
---

# GlycA — Glycoprotein Acetylation

## Metadata
- category: blood
- unit: mmol/L — NOTE platform-specific: Nightingale reports mmol/L (~1.2–1.5), LabCorp NMR LipoProfile reports a different μmol/L scale (~369). The two scales are NOT interchangeable.
- source: lab
- confidence: provisional
- review_cadence: per-lab-panel
- last_verified: 2026-06-18

## Target Range
- NO universal clinical cut-point. GlycA risk is reported by quartile/percentile within a cohort, not against a validated threshold.
- population context (Nightingale platform): general-population means ~1.2–1.5 mmol/L.
- provisional research threshold (LabCorp platform): the often-quoted ~400 μmol/L figure is a PROPOSED research threshold on the LabCorp μmol/L scale ONLY — not an FDA- or society-endorsed clinical decision limit.
- units are platform-specific and NOT interconvertible: a Nightingale mmol/L value and a LabCorp μmol/L value cannot be compared numerically (the scales differ ~3×). Always record which platform produced a value.
- source of target: [[library/biomarkers/glyca/research-report]]

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: [[labs/]]

## Affected By
- systemic inflammation / infection (raises)
- adiposity / BMI (raises)
- smoking (raises — strong, dose-dependent)
- age (raises — inflammaging)
- sex (women slightly higher, gap ≤ ~10%)
- weight loss (lowers — ~15–23% after bariatric surgery)
- exercise (lowers — endurance training, ~−9 μmol/L pooled)
- statins: minimal effect on GlycA (statin-resistant residual-inflammatory component) — contrast with hs-CRP
- heritability ~30% (majority of variance is acquired/modifiable)

## Why It Matters
GlycA is an integrated, cumulative index of low-grade systemic inflammation — a composite NMR signal from the N-acetyl glycan groups on several acute-phase glycoproteins, behaving like an inflammatory analogue of HbA1c. Prospectively it is associated with incident cardiovascular disease, type 2 diabetes, all-cause and cardiovascular mortality, and severe infection across large cohorts, frequently retaining significance after adjustment for hs-CRP. It is more analytically and biologically stable than hs-CRP (~5% vs ~30% within-person variability), so a single draw is a cleaner estimate of chronic inflammatory tone. It remains EMERGING / research-grade: offered by some labs but not yet guideline-endorsed for routine clinical use, with no universal cut-point.

## Relations
- [[biomarkers/hs-crp]]
- [[biomarkers/apob]]
- [[library/biomarkers/glyca/research-report]]
