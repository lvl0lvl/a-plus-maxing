---
title: render-engine — emit pipeline + component set + templates
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/render-engine
---

# render-engine (`scripts/generate/render.py` + `vault/design/templates/`)

**What:** the single-file HTML artifact pipeline. `render.emit(template, store_read)`
inlines, size-checks (<500KB, ADR-0004-T0 cap), external-asset-refuses, and writes one
self-contained HTML file. Templates are callables `template(store_read) -> html_str`.

**Contracts:**
- `render.emit` REFUSES external asset references (raises; `generate.run` propagates as
  a non-zero exit, never a partial artifact).
- `render.MAX_SERIES_PER_VIEW` / `MAX_TIMEPOINTS_PER_VIEW` — the single source of the
  per-view cap (render_views reuses them, never a second size check).
- `component_set.PALETTE` + `SERIES` — DECISION-PINNED
  (`vault/decisions/2026-06-05-render-colorblind-safe-palette.md`); the ADR-0004-T1
  accessibility gate reads expected hex values from the decision. Do not change.
- `component_set.state_for(item, value=None)` — delegates to `biomarker_meta` (S48);
  returns good/concern or `"neutral"` (no judgment possible → rendered muted). The
  pre-S48 name-hash placeholder is gone.
- `component_set.sparkline(values, state)` — polyline SVG (render_views' ADR-0007
  surface). `bar_sparkline(values, state)` (S48) — bottom-aligned rect columns, the
  dashboard's bars-not-paths component. Both: numeric values ONLY (callers route).
- Templates: `dashboard.py` — the TYPE-ROUTED operator surface (routes by stream prefix:
  biomarker/unprefixed-numeric → KPI + units + state + bar sparkline + trend chip;
  panel → state-marker row; watch-out → answers; feedback → notes; no string ever
  reaches numeric viz). `report.py` — the physician-facing summary template.

**Called by (production):** `generate.run` (dashboard/report), `render_views` (per-page
emit).

**Governing ADR:** ADR-0004 (engine + cap), ADR-0008 (type-routing, state, bars).
