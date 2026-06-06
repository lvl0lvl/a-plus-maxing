---
title: ADR-0004-T0 render-size cap re-validated against the real component_set.py render; cap UNCHANGED
type: decision
permalink: a-plus-maxing/decisions/2026-06-06-adr-0004-t0-cap-revalidation
created: 2026-06-06
status: active
decided_by: Architect (cap parameter is under Architect change-control)
supersedes: null
relates_to: 2026-06-06-render-emit-pagination-caller-orchestrated
---

# ADR-0004-T0 render-size cap re-validated against the real render; cap UNCHANGED

## Decision

The ADR-0004-T0 render-size cap — **max 16 series-per-view AND max 12
timepoints-per-view**, working budget **350000 bytes** (0.70 × 500000), hard
ceiling **500000 bytes** — is **UNCHANGED**. The harness bound holds against the
real `vault/design/templates/component_set.py` render with very large margin. No
re-derivation is needed. ADR-0004-T2 may consume the cap as-recorded in the spike.

## Context / problem (the gap this closes)

The cap was derived in spike ADR-0004-T0
(`docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md`) from a throwaway in-spike
harness, because the production template path did not exist at Wave 1. The spike
recorded a re-validation trigger: when ADR-0004-T1 builds the real
`component_set.py` template, the measurement MUST be re-run against the real
render and the reconciliation recorded BEFORE ADR-0004-T2 / ADR-0007-T2 consume
the cap.

The ADR-0004-T1 recipe (`docs/task-plan/ADR-0004-T1.md`, ~line 48) scoped the cap
re-validation OUT of T1. So the reconciliation was never recorded, and ADR-0004-T2
halted at Entry State: its prerequisite requires the cap to have been re-validated
against the real `component_set.py` render with the reconciliation recorded. This
note is that recorded reconciliation.

## Independent measurement

Built a worst-case combined matrix + projection view AT the cap — **16 series ×
12 timepoints** — assembling the chart-component markup from the REAL
`component_set.py` the way the production `dashboard.py` and `report.py` templates
assemble it:

- **Matrix section:** per-series `kpi()` card + inline-SVG `sparkline()` (the
  `dashboard.py` per-item shape), 16 series.
- **Projection section:** per-series projection panel — `h2` heading + `kpi()` +
  a projection `sparkline()` (the series extended by the 1-step linear projection
  point) + the 12-row readings comparison table (the `report.py` per-section
  shape), every series carrying a projection panel.
- Drew the head/style block, legend, KPI cards, sparklines, and table markup from
  `component_set.py`'s real functions (`head`, `legend`, `kpi`, `sparkline`,
  `_escape`); realistic long biomarker names and multi-digit lab-magnitude values.

Measured the rendered bytes with `len(html.encode("utf-8"))` (the `wc -c`
equivalent named in the spike and in the T2 size-budget gates), via a throwaway
`.venv/bin/python -c "..."` invocation — no production file was written or
modified.

**Result:**

- Worst-case 16 × 12 combined matrix+projection = **34117 bytes** (32 inline
  `<svg>` elements: 16 matrix sparklines + 16 projection sparklines).
- That is **9.7 % of the 350000 working budget** (315883 bytes of margin) and
  **6.8 % of the 500000 hard ceiling** (465883 bytes of margin).
- Per-series decomposition (real `component_set.py`): ≈ 2 KB per series for the
  combined matrix card + projection panel (KPI ×2, sparkline ×2 at 12 points
  ≈ 261 bytes each, a 12-row readings table ≈ 1163 bytes), plus ≈ 1.5 KB fixed
  overhead (head/style block ≈ 1187 bytes + legend ≈ 358 bytes). 16 series ×
  ≈ 2 KB ≈ 32 KB, consistent with the 34117-byte total.

## Reconciliation against the spike

The spike's harness measured 57741 bytes for a 10 × 4 view and projected a
worst-case-at-cap (16 × 12) of ≈ 165065 harness bytes / ≈ 330130 real bytes,
applying a **2.0× density-inflation** assumption (harness under-estimates the real
template) plus a **30 % ceiling reserve** (working budget = 350000).

The real `component_set.py` render is **lighter than the harness**, not 2× heavier:
the spike harness modeled richer per-element SVG geometry (axis ticks, per-point
markers, value labels, per-series reference bands) that the real `sparkline()`
does not emit — it is a lean single `<polyline>`. So the 2.0× density assumption
is conservative in the safe direction (real bytes are well under harness bytes).
The measured 34117 bytes sits an order of magnitude below the spike's ≈ 330130
real projection and the 350000 working budget. **The harness bound holds; the cap
needs no re-derivation.**

## Breaks if

- The real `component_set.py` matrix/projection markup volume per series grows by
  more than **~10×** (e.g. the per-series panel rises from ≈ 2 KB toward ≈ 20 KB
  through richer SVG `<defs>`, per-point markers/labels, embedded reference bands,
  or inline `data:` raster assets) — at that point a 16 × 12 view would approach
  the 350000 working budget and the cap MUST be re-measured. The current real
  markup has ~10× of headroom against the working budget at the cap.
- A future matrix/projection template embeds large inline `data:` assets (raster
  thumbnails, embedded fonts) — those bypass the per-element text-markup model
  this measurement assumes; re-measure before relying on the cap.
- The cap's series/timepoint numbers change — any change to the cap is itself
  under Architect change-control (the spike's own constraint: ADR-0004-T2 /
  ADR-0007-T2 MUST NOT change the cap without Architect review).

## Conditions for revisiting

- ADR-0004-T2 or ADR-0007-T2 measures a real `render.emit` worst-case at the cap
  that exceeds the 350000 working budget (or approaches 500000) — escalate to the
  Architect for a cap re-derivation with the same 30 % reserve; do not change the
  cap value in the render code.
- The `component_set.py` per-series markup volume crosses the "breaks if"
  ~10× growth threshold above.

Re-validation recorded 2026-06-06 (S39). Spike slot updated in
`docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md` (gitignored working
artifact) to point at this durable record.
