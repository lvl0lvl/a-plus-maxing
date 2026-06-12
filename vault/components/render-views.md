---
title: render-views — biomarker matrix + projection detail views
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/render-views
---

# render-views (`scripts/generate/render_views.py`)

**What:** the matrix/projection DETAIL surface (the terminal sink of the V1 DAG).
`render_views(root, panels=, watchouts=, biomarkers=)` recomputes the biomarker matrix
and naive projections from stored timepoints AT RENDER TIME via typed `loop_schema`
reads, paginates within the ADR-0004-T0 cap, and emits each page through `render.emit`.
Per the frozen dashboard design, the full matrix table is NOT a v1 dashboard zone — this
module remains the detail output until v2.

**Contracts:**
- `_STATE_DISPLAY` covers the four absence/pending states (`pending`,
  `not-yet-answered`, `no-data`, `no-prior`) 1:1; `ANSWERED_OVER_TIME` deliberately has
  no row (an answered watch-out renders its answers, not a state marker); an unmapped
  state KeyErrors (fails loud, never a silent wrong render).
- Panel rows branch in `_panel_row` (bead s38+byj): `read_panel` == `PENDING` renders
  the pending state marker; a landed result (a VALUE, not a fifth state) renders as a
  value row mirroring the answered-watchout shape. `_STATE_DISPLAY`'s KeyError stays
  reserved for genuinely-unmapped published STATES.
- Projection guardrail (ADR-0007, render-time contract): renders only at
  `PROJECTION_MIN_TIMEPOINTS = 3`+; carries the verbatim honest-absence
  `PROJECTION_LABEL`, the method, datapoint count, widening band, time axis. At most ONE
  projection per biomarker, attached only to the final window, computed from the series'
  actual last two stored points.
- Windowing: `_window_bounds` splits over-cap series into ≥2-point windows preserving
  every stored point; pages bound by `render.MAX_SERIES_PER_VIEW`.
- Uses the polyline `component_set.sparkline` (its pinned surface) and
  `cs.state_for(item, values[-1])` (value-passing since S48).

**Called by (production):** operator/specialist invocations for biomarker detail; the
dashboard does NOT call it (two surfaces by design — dashboard at-a-glance, this for
depth).

**Governing ADR:** ADR-0007 (placement + guardrails), ADR-0004 (cap/emit).
