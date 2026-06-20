---
title: <Biomarker Name>
type: biomarker
permalink: a-plus-maxing/biomarkers/<slug>
category: blood | wearable | functional | subjective
unit: <e.g., mg/dL, ms, bpm, %>
source: lab | wearable | manual | calculation
confidence: established | supported | provisional
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
review_cadence: monthly | quarterly | per-lab-panel | per-wearable-sync
---

# <Biomarker Name>

## Metadata
- category:
- unit:
- source:
- confidence:
- review_cadence:
- last_verified:

## Target Range
- ideal:               # x - y
- acceptable:          # a - b
- alert:               # < p or > q
- source of target:    # literature citation | MD recommendation | n=1 baseline | [[library/...]]

## Current Value
- value:               # x (YYYY-MM-DD)
- trend:               # improving | stable | declining (over last N measurements)
- history pointer:     # [[labs/YYYY-MM-DD]] or [[daily/YYYY-MM-DD]] or wearable export path

## Affected By
- [[protocols/<name>]]
- [[compounds/<name>]]
- [[dna/<variant>]]
- lifestyle factor: <sleep | training | stress>

## Why It Matters
One paragraph: what this biomarker indicates physiologically. What conditions does deviation flag.

## Relations
- [[experiments/<id>]] (uses this as endpoint)
- [[decisions/<adr>]]
- [[compounds/<intended-mover>]]
