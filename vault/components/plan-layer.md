---
title: plan-layer — de-identified summary router + attributed plan assembly
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-13
review_cadence: on-change
permalink: a-plus-maxing/components/plan-layer
---

# plan-layer (`scripts/plan/router.py` + `scripts/plan/assemble.py`)

**What:** the plan-reasoning pipeline. `router.summarize` derives the de-identified
summary from store-read state (THE PII boundary); `router.dispatch` routes it to the
no-train lane behind a closed-field-set whitelist; `assemble.assemble()` composes the
attributed multi-domain plan dict from the specialist roster. The plan dict has NO
render surface yet — that is the `1oh` gap (dashboard build Slice 2).

**Contracts:**
- `SUMMARY_FIELD_SET` — the closed 11-field allowlist (ADR-0006-T0 spike); the
  version-controlled PII-boundary source of truth. `EXCLUDED_RAW_PII` names the stripped
  raw fields; module-load asserts keep the two structures consistent (the §5b tripwire).
- `summarize` — per-field derivation (`_RAW_TO_FIELD` + `_FIELD_DERIVATION` band/class
  transforms); `recent-trend-direction` is special-cased to the registry-driven juc
  mechanism (below), not a raw-PII-backed field; pass-through fields are PII-scanned
  fail-closed (the 8j6 gate; names the field, never echoes the value).
- `dispatch` — fail-closed on absent/partial summaries; whitelist
  `set(payload) ⊆ SUMMARY_FIELD_SET`; scalar-only payload values (fga). The sink is
  never reached on any violation.
- `recent-trend-direction` (juc, 2026-06-12 decision) — `_recent_trend_direction`
  reduces WORST-WINS (regressing > improving > flat) over `_POLARITY_FEED`: every
  registered-polarity `biomarker::` marker (registry-driven, never hand-typed). Each
  stream's trend comes from `_trend_token` over that one stream's series; zero feed
  signal emits the no-signal `flat` (always present — a fresh operator never trips
  dispatch's partial raise). A load-time tripwire pins the feed to the registry, its
  disjointness from `SUMMARY_FIELD_SET` + `EXCLUDED_RAW_PII`, and the output to
  `TREND_DIRECTIONS`. `raw-lab-values` is de-plumbed from `_RAW_TO_FIELD` but stays a
  named-excluded raw-PII class (the boundary promise); `SUMMARY_FIELD_SET` unchanged.
- `_trend_token` — closed vocabulary improving/flat/regressing. Resolves via
  `biomarker_meta.trend` for REGISTERED-polarity markers; an unregistered marker with a
  determinable directional change keeps the fail-closed raise (never fabricate a value
  judgment). Reused per-stream by `_recent_trend_direction`; its cross-item +
  unknown-polarity raises stay as fail-closed safety nets.
- `assemble()` — attributed plan dict: per-domain sections, recommendations with
  source/tier/reversibility, coverage-gap disclosures, HALT-struck recs,
  population-mismatch flags.

**Called by (production):** plan generation (summarize → dispatch → assemble); the
future Slice-2 plan render surface will consume `assemble()` output.

**Governing ADR:** ADR-0006 (assembly + no-train routing), ADR-0001 (PII boundary),
ADR-0008 (trend polarity).
