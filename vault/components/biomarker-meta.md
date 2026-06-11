---
title: biomarker-meta — per-marker units / range / polarity registry
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/biomarker-meta
---

# biomarker-meta (`scripts/store/biomarker_meta.py`, NEW S48)

**What:** the curated per-marker metadata registry — `{units, reference_range,
good_direction}` per marker name. The single layer that turns raw stored values into
honest semantics: real in/out-of-range state, units on display, polarity-aware trend
labels. General-adult population reference values (operator-agnostic reference data per
ADR-0005 — NOT operator PII). Unknown markers resolve to `None` everywhere: honest
absence, never a fabricated range.

**Contracts:**
- `get(item)` — prefix-tolerant (`biomarker::ferritin` ≡ `ferritin`), lowercased lookup;
  unknown → None.
- `display_name(item)` — strips stream prefixes, title-cases words, upper-cases the
  acronym set (HRV/RHR/CRP/ALT/HDL/LDL + 1RM, S49). The clean-label source (`azf`).
- Fitness markers (S49, ADR-0009 D4): bodyweight (lb), sleep-hours (h), est-1rm (lb),
  steps (steps) — units always; `reference_range` None (goal/person-dependent, no invented
  ranges); `good_direction` only where unambiguous (sleep-hours up; others None →
  direction-only neutral arrow on the dashboard).
- `state_for(item, value)` — in registered range (inclusive) → `good`; outside →
  `concern`; no range / non-numeric / unknown marker → None (neutral). `watch` is
  RESERVED — no invented nearing-boundary band (ADR-0008 D1).
- `trend(item, prev, latest)` — `up`/`down` polarity maps direction to
  improving/flat/regressing; `in-range` polarity judges by distance-to-range movement;
  unknown polarity → None.
- v1 limitation (accepted): ranges are not sex- or lab-specific; per-operator overrides
  are the documented v2 path.

**Called by (production):** `component_set.state_for` (delegation), the dashboard
template (labels, units, trend chips), `router._trend_token` (polarity resolution —
registered markers resolve, unregistered keep the fail-closed raise).

**Governing ADR:** ADR-0008.
