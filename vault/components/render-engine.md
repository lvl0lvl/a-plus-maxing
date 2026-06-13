---
title: render-engine — emit pipeline + component set + templates
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-12
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
- Escaping convention (bead vp5p, PR#90 F20/SEC-001): all template HTML attributes
  are SINGLE-QUOTED, and `component_set._escape` is the SOLE escape path (templates
  never roll their own) encoding the full `& < > ' "` set — `&` first so later
  entities are not double-encoded.
- `component_set.ACCENTS` (S49) — the five surface-category chrome colors from the
  approved dashboard design (training/nutrition/supplements/peptides/sleep). Chrome
  ONLY (card headers, glyph dots, tint pills) — never data state; data state stays
  the PALETTE good/watch/concern/neutral vocabulary (ADR-0009 D3).
- `component_set.CHROME` (S49, visual-spec pass) — the neutral app-surface tokens:
  page-bg `#F3F4F6`, card-border `#E5E7EB`, plus the FIXED-HEX ~10% tint backgrounds
  (good/concern/neutral + the five accents + the calendar today-tint). Neutral
  chrome, not data state; no runtime color math — each tint literal is commented
  with its base color. The `_style_block` frame (gray page, 1140px white sheet,
  header bar, card system, grid2/4/6 + 7-col `.cal`, pills, stat boxes, tracks,
  print rules) is built from these tokens. Build target:
  `vault/design/dashboard-v1-visual-spec.md`.
- Visual primitives (S49 visual-spec pass): `zone(title, body, subtitle=None)`
  (whitespace-separated section + muted subtitle); `awaiting()` — the mechanical
  honest-empty-state (no numbers ever; zone tests enforce digit-free);
  `progress_ring(label, value=None, color=None)` — ~96px SVG ring, REPLACES
  `ring_scaffold`: honest state (value None) renders the light track only + a
  centered em-dash, never an arc or fake percentage; `pill(text, tint_state=None)` —
  tinted pill (CHROME tint bg + base-color text; unknown tint KeyErrors) /
  `chip_b(text)` — bordered chip (metric chips, pending draws, inert controls);
  `stat_box(label, value="—", tinted=False)` — em-dash-default stat slot (tinted
  picks the enclosing card's CSS tint); `track_bar(fill_pct=None, color=None)` —
  thin progress track, no fill while fill_pct is None.
- Templates: `dashboard.py` — the 7-ZONE "Today" surface (ADR-0009 + the 2026-06-11
  visual-spec amendment): header bar (product name, real long-form `_today` date,
  muted awaiting status pill) replaces the old h1/TL;DR; hero readiness card
  (track-only rings + designed readout; REAL hrv/rhr/sleep-hours bordered chips only
  when the store carries them); week-calendar card (range header, inert
  chevron/Month chips, legend pills, 7-col grid, today column tinted); 2×2 plan
  cards with designed empty anatomy (stat rows, macro tracks — all em-dash);
  Performance & Trends as a `.grid6` of metric cards (the REAL ADR-0008 type-routed
  data: label, value + units, state-tinted trend pill, bar sparkline); 16-card
  care-team grid (static `_SPECIALISTS` tuple mirroring the deployed roster;
  replaced when a rollup model lands); goals (unfilled track + awaiting); labs strip
  card (panel → Pending-draws chip w/ state-marker; watch-out → answers; feedback →
  notes — real). Routing stays total: unknown `::` prefix raises (ADR-0008 D3
  preserved verbatim). `report.py` — the Physician Face Sheet (redesigned S53,
  bead `nsxy`; own page identity + v3 token bindings — see
  `vault/components/report.md`).

**Called by (production):** `generate.run` (dashboard/report), `render_views` (per-page
emit).

**Governing ADR:** ADR-0004 (engine + cap), ADR-0008 (type-routing, state, bars),
ADR-0009 (7-zone visual shell, accents, zone-state honesty).
