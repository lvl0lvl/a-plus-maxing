## ADR-0008: Biomarker Metadata Registry + Type-Routed Dashboard Rendering

> **Y-Statement:** In the context of the signed-off dashboard v1 target (`vault/design/dashboard-v1-design.md`) requiring per-marker semantics (units, ranges, state, trend) while the current dashboard crashes on any realistic mixed-stream store and `component_set.state_for` is a name-hash placeholder, facing the tension between fabricating clinical judgments the data model cannot support and rendering honestly, we decided to add a curated per-marker metadata registry (`scripts/store/biomarker_meta.py`: units + reference_range + good-direction polarity) and to type-route the dashboard template by stream prefix, to achieve real in/out-of-range state, polarity-aware trend labels, crash-free mixed-stream rendering, and clean labels — accepting that unregistered markers render NEUTRAL (no state judgment), that v1 reference ranges are general-adult population values (not sex/lab-specific), and that the router's generic `raw-lab-values` stream keeps its fail-closed raise.

```yaml
id: ADR-0008
title: "Biomarker Metadata Registry + Type-Routed Dashboard Rendering"
status: accepted
date: 2026-06-10
decision-makers: [Walter McGivney]
tags: [biomarker-metadata, dashboard, type-routing, render, polarity, post-v1]
```

### Context

This is the first post-V1 (lighter-path) ADR: per the S48 documentation model, feature work gets one ADR per contract-changing decision cluster plus the full review lifecycle, instead of the spec→build-plan→task-plan pipeline. It builds Slice 1 of the data-model delta the frozen dashboard design names as its gate.

Four defects converge on one missing layer:

1. **`i1t` (P1):** `generate.run("dashboard")` assembles the read model by globbing every `.ndjson` under the store root — including `panel::*` (value `"pending"`), `watch-out::*` (string answers), and `feedback::physician-feedback` (free text). `dashboard.render` feeds every item's values to `component_set.sparkline`, whose `min()/max()` + arithmetic crash on strings. Any realistic mixed store kills the dashboard; the test seed (`tests/generate/test_generate.py::_seed_store`) is numeric-only, so 340 green tests encode the broken assumption (`04uk`).
2. **`azf`:** the dashboard renders raw store keys (`biomarker::ferritin`) as labels.
3. **`y0h0` / `state_for`:** the store's Line Field Set (`item, timepoint, source, value`) carries no units, reference range, or polarity. `component_set.state_for` cycles good/watch/concern by a hash of the item NAME — a documented placeholder producing arbitrary state colors.
4. **`juc` / `router._trend_token`:** the de-identified plan summary's `recent-trend-direction` cannot label a real numeric change improving/regressing without per-marker good-direction polarity (rising ALT regresses; rising HDL improves), so it RAISES on any directional change — the documented fail-closed gap, with an explicit escalation note to add polarity to the data model.

The dashboard v1 design additionally pins two render decisions that constrain this build: sparklines are bar columns, not SVG path polylines (the path geometry rendered inconsistently), and honesty caveats are part of the design — no good/bad coloring without real grounds. The render palette is decision-pinned (`vault/decisions/2026-06-05-render-colorblind-safe-palette.md`): the accessibility gate reads expected hex values from that decision, so `PALETTE` must not change.

### Decision

**D1 — Metadata registry.** Add `scripts/store/biomarker_meta.py`: a curated module-level registry mapping a marker name to `{"units": str, "reference_range": (low, high) | None, "good_direction": "up" | "down" | "in-range" | None}`, with accessors:

- `get(item)` — prefix-tolerant lookup (`biomarker::ferritin` and `ferritin` both resolve); unknown marker returns `None` (honest absence — never a fabricated range).
- `display_name(item)` — strips the stream prefix (`biomarker::` / `panel::` / `watch-out::`) for clean labels.
- `state_for(item, value)` — real range logic: numeric value inside the registered range → `good`; outside → `concern`; no registered range or non-numeric value → `None` (neutral). **No invented "watch" band in v1**: watch requires a clinical nearing-boundary rule we have no grounds to fabricate; the state stays reserved for future explicit rules.
- `trend(item, prev, latest)` — polarity-aware: `up`/`down` polarity maps the numeric direction to `improving`/`flat`/`regressing`; `in-range` polarity judges by movement relative to the registered range (distance-to-range shrinking → improving); no registered polarity → `None`. An in-range marker's movement WITHIN its range reads `flat` (distance unchanged at 0 — the value moved, the judgment did not); the S39 "flat only for genuine no-change" wording is superseded for in-range polarity.

Registry values are general-adult population reference ranges (textbook values — operator-agnostic reference data, NOT operator PII, clonable per ADR-0005). The v1 seed set covers the markers the project exercises (rhr, hrv, ferritin) plus common panel markers.

**D2 — `component_set.state_for` delegates.** `state_for(item, value=None)` replaces the name-hash with delegation to `biomarker_meta.state_for`; a `None` (neutral) verdict renders with the existing `muted` color. `PALETTE` and `SERIES` are untouched (decision-pinned). A new `bar_sparkline(values, state)` component renders bottom-aligned `<rect>` columns (the design's bars-not-paths decision); the existing polyline `sparkline` remains for `render_views`' ADR-0007 contract.

**D3 — Type-routed dashboard template.** `vault/design/templates/dashboard.py` routes each read-model item by stream prefix: `biomarker::` (and unprefixed numeric series, the legacy direct-append form) → KPI row with clean label, latest value + units, real state, bar sparkline over the NUMERIC values only, and a trend chip (direction-only when polarity is unregistered — the design's honesty caveat); `panel::` → state-marker row (value verbatim, e.g. "pending"); `watch-out::` → label + answers row; `feedback::` → note rows. No string value can reach numeric viz by construction. An item carrying a `::` prefix outside these four routed stream types fails loud (`KeyError` naming the prefix) — routing for a new stream type is added deliberately, never by silent fallthrough. The KPI headline is the stream's TRUE latest reading rendered verbatim, carrying units only when that reading is numeric (state and sparkline still derive from the numeric series). `generate.run`'s CLI surface is unchanged. `render_views.py` remains the matrix/projection DETAIL surface (per the design note: the full matrix table is not a v1 dashboard zone). [AMENDED 2026-06-12 (#110 review, beads `y0h0` + `i2yw`)]: the trend chip is now the NUMERIC delta chip — the latest-minus-prev movement in the metric's own unit, tinted by the polarity-aware semantic state (neutral without registered grounds, preserving the honesty caveat) — and the zone-4 card carries the dashboard-only naive-projection caption (`→ {value} by {date} · naive projection`, ≥3-timepoint gate single-sourced via the shared `biomarker_meta` projection seam), per the 2026-06-12 visual-spec zone-4 amendment.

**D4 — Polarity-aware `_trend_token`.** `router._trend_token` consults the registry via the readings' `item`: a directional change on a registered-polarity marker resolves to `improving`/`regressing`; an UNREGISTERED marker keeps the documented fail-closed raise (never fabricate a value judgment). The generic `raw-lab-values` stream stays unregistered — per-marker lab trends for the summary are the Track-2 residual (`juc` keeps that scope).

**D5 — The mixed-stream test.** A test seeding all four stream types via `loop_schema` writers and running `generate.run("dashboard")` end-to-end (the production path), asserting: no crash, no `biomarker::` prefix in the HTML, panel state rendered as a marker row, watch-out answer rendered, and numeric-only sparkline input. This test RED-proves the `i1t` crash on the pre-fix code.

### Rationale

The registry is the single layer all four defects need: state (`y0h0`) needs ranges, trend (`juc`) needs polarity, and honest type-routing (`i1t`/`azf`/`i2yw`) needs to know what a stream IS. Placing it in `scripts/store/` keeps metadata beside the data model it describes, importable by both render (component_set/dashboard) and plan (router) layers without a circular dependency. The alternative — extending the Line Field Set to carry units/range/polarity per reading — was rejected: that data is per-MARKER, not per-reading; stamping it on every line duplicates state that can go internally inconsistent, and would break every existing store consumer for no informational gain. A second alternative — a YAML/JSON data file — was rejected for v1: a Python module is directly importable, testable, and reviewable, and a file format can be extracted later in one move if operator-editable ranges become a requirement.

The neutral state (rather than fabricating watch/concern for unknown markers) extends the project's honest-absence discipline (ADR-0007's no-prior/no-data states; the projection label) to state semantics: an unregistered marker shows its data without a judgment, exactly as the signed-off design's caveats require. Keeping the raise for unregistered markers in `_trend_token` preserves the fail-closed PII-boundary discipline of ADR-0006 — the change makes the gap CLOSABLE per marker instead of removing the guard.

### Consequences

**Positive:**
- A realistic mixed-stream store renders crash-free through the production `generate.run("dashboard")` path (resolves `i1t`, tested by `04uk`'s mixed-stream test).
- Labels are clean (`Ferritin`, never `biomarker::ferritin`) — resolves `azf`.
- Registered markers carry real in/out-of-range state + units + polarity-aware trend — resolves `y0h0`; replaces the `state_for` placeholder; unblocks `_trend_token` for registered markers (`juc`'s metadata half).
- The dashboard template is the single type-routed surface at dashboard level (`i2yw`'s zone-4 merge), with `render_views` remaining the matrix/projection detail view per the frozen design.

**Negative:**
- v1 reference ranges are general-adult textbook values: not sex-specific, not lab-specific. A marker whose clinically correct range differs (e.g. ferritin by sex) renders against the general range until the registry grows per-operator overrides — a documented v2 path, acceptable because state is advisory display, never a clinical gate.
- Unregistered markers render neutral (no state, direction-only trend chips): coverage grows only as the registry is curated. Honest, but the dashboard's state coverage is bounded by curation effort.
- The router's `recent-trend-direction` still raises for the generic `raw-lab-values` stream (unregistered by design); the production summary path is unchanged until Track-2 lands per-marker lab streams (`juc` residual).
- The design note's `i2yw` projection-readout-on-chips clause is DEFERRED: trend chips carry the trend word/arrow only, and the projection block remains a `render_views`-only surface until a later slice. [AMENDED 2026-06-12 (#110 review, beads `y0h0` + `i2yw`)]: DELIVERED — the dashboard trend card carries the numeric polarity-tinted delta chip and the dashboard-only naive-projection caption; `render_views` keeps the full five-element detail block (see the ADR-0007 2026-06-12 amendment).

**Neutral:**
- `PALETTE`/`SERIES` and the accessibility gate are untouched; neutral renders via the existing `muted` color.
- `render_views.py`'s ADR-0007 contract (polyline sparkline, marker rows, projection guardrail) is unchanged except for passing the latest value to the new `state_for` signature.

### Alternatives Considered

#### Alternative A: Extend the Line Field Set with per-reading units/range/polarity
Stamp metadata on every stored line. Rejected: the metadata is per-marker, not per-reading; per-line copies duplicate state (two readings of one marker could disagree), break `keying`'s closed field set and every store consumer, and bloat the gitignored store for zero informational gain. Becomes right only if per-reading provenance of ranges (lab-specific ranges per draw) becomes a requirement.

#### Alternative B: Patch the crash only (type-guard inside `sparkline`)
A `try/except`/filter inside the sparkline silences the crash without metadata. Rejected: it leaves the placeholder state, the label leak, the raise, and renders panels/watch-outs as garbage KPI rows — the band-aid the HANDOFF explicitly warns against ("do NOT band-aid `i1t` alone"). It also violates the no-defensive-programming rule by swallowing a type error instead of routing by type.

#### Alternative C: Operator-editable YAML registry from day one
A `vault/`-side data file the operator edits. Rejected for v1: adds a parse/validate surface and a file-format contract before any operator has asked to edit ranges; the Python module is importable and testable today and extractable to a data file in one move when the need is real (evidence-driven-design memory).
