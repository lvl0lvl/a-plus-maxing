---
title: Dashboard v1 — Visual Language Spec (transcribed from the signed-off mock)
type: design
status: approved
owner: walter
created: 2026-06-11
last_reviewed: 2026-06-11
depends_on: [dashboard-v1-design.md]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/design/dashboard-v1-visual-spec
---

# Dashboard v1 — Visual Language Spec

**Provenance:** transcribed 2026-06-11 (S49) from the operator-held signed-off Pencil
mock ("Dashboard v2 — Today"), which Walter showed side-by-side against the S49 zone
shell ("They are not the same"). The mock carries health-domain sample content and
therefore stays OUT of this public repo (ADR-0005 boundary); this text spec is the
in-repo build target for the visual language. `dashboard-v1-design.md` owns the zone
semantics; this file owns how it LOOKS. Where sample values appear below they describe
SLOT SHAPE only — the honesty rule (ADR-0009 D2) governs what may actually render.

## Page frame

- Page background: light neutral gray (`#F3F4F6`). The dashboard is a white SHEET
  (`#FFFFFF`, border-radius 12px, 1px border `#E5E7EB`, max-width ~1140px, centered,
  24-32px inner padding) sitting on the gray page — an app surface, not a document.
- **Header bar** (top of sheet, full width, bottom border `#E5E7EB`): left — product
  name `A+ Maxing` (bold, ~17px) over the real long-form date (`Wednesday · June 10,
  2026`, muted 13px). Right — a status pill (see Pills) carrying the readiness
  headline when wearable scoring exists; until then the pill reads the awaiting
  state (`— awaiting wearable baseline`, muted), and a `Today` label chip.
- Zone sections separate by whitespace (28-32px), NOT rules/borders. Zone heading:
  ~16px bold ink; most zones carry a one-line muted ~13px subtitle under the heading
  (subtitles are part of the design — see per-zone copy below).

## Tokens

- Colors: data-state stays the locked `PALETTE` (good/watch/concern/ink/paper/muted);
  category chrome stays `ACCENTS` (training `#1F6FEB`, nutrition `#E8833A`,
  supplements `#0E9AA3`, peptides `#7C3AED`, sleep `#5B5BD6`). New NEUTRAL chrome
  tokens (not data state): page-bg `#F3F4F6`, card-border `#E5E7EB`, tint backgrounds
  at ~10% of their base color for pills.
- Cards: white, 1px `#E5E7EB` border, border-radius 10px, padding 14-16px, very
  subtle shadow (`0 1px 2px rgba(0,0,0,.05)`).
- Card grids: CSS grid with 12-16px gap. Plan zone = 2 columns; trends = 6 columns
  (wraps 3/2 on narrow); care team = 4 columns; calendar = 7 columns.
  [AMENDED 2026-06-11]: the trends narrow wrap is pinned at max-width 900px → 3
  columns and max-width 560px → 2 columns.
- **Pills/chips** (one component, two flavors): tinted pill — radius 999px, 12px
  text, colored text on its ~10% tint background (e.g. good-green status pill);
  bordered chip — radius 999px, 12px, 1px `#E5E7EB` border, ink text, used for
  metric chips (`HRV 64 ms`), pending items, legend entries.
- Type scale: zone heading 16px/700; card title 13-14px/600; big metric value
  24-28px/700; body 13px; captions/labels 11-12px muted. [AMENDED 2026-06-11]:
  as built, the trends-card value is 20-22px (`.grid6 .kpi .value` 21px) — 28px
  stays the non-grid KPI default, not the trends-card value; captions/labels
  run 11-13px (the 13px `.caption` carry-over is accepted).

## Zone 1 — Readiness (hero)

One full-width card. Two horizontal halves:
- **Left — three progress rings** (Recovery / Sleep / Strain), each ~96px: an SVG
  arc ring with thick stroke (~9px), rounded caps, a light full-circle track
  (`#E5E7EB`) underneath, the value centered inside (24px bold) and the label
  beneath. Ring colors: Recovery = PALETTE good green; Sleep = ACCENTS sleep
  indigo; Strain = ACCENTS training blue (chrome usage — the arc is chrome around
  a value, not a data-state semantic). **Honest state (current):** track-only ring
  (no colored arc), an em-dash `—` centered where the value would be, label
  beneath — never a fake percentage or arc fill.
- **Right — readout block:** headline (~16px bold; honest state: `Awaiting wearable
  baseline`), 1-2 lines of muted body copy, then a **chips row of real latest
  metrics from the store when present** (bordered chips: `HRV 67 ms`, `RHR 49 bpm`,
  `Sleep 7.5 h` — these are real stored readings, so they render under the honesty
  rule; omit any chip whose marker has no reading).

## Zone 2 — This Week (calendar)

[AMENDED 2026-06-11, Walter side-by-side review: "your's is not a calendar —
it's just boxes; the top nav of your calendar is off". This section supersedes
the earlier header/body description with his direction.]

**Card header row, two sides:**
- **Left — week nav:** calendar glyph + `This week` (bold) + the week nav shaped
  `‹ Jun 7 – 13 ›` — prev/next chevrons FLANKING the real date range (small
  bordered square buttons, inert until a calendar model exists).
- **Right — legend + month nav + expand:** the four event-category legend pills,
  each in its OWN category tint (Training = training blue tint; Lab draw = amber
  tint; Check-in = purple tint; Appointment = green tint — event-category chrome
  hexes live in CHROME as fixed literals, AA-measured by the tint gate, distinct
  from data-state PALETTE), then a month nav shaped `‹ Month ›` (inert), then the
  **expand control** — a real, functional caret that expands the week view to the
  full current month.
- **Expand mechanics:** native `<details>`/`<summary>` (no scripts — ADR-0004
  single-file rule intact): the summary is the caret control; opening it renders
  the **full month grid in document flow below the week strip, pushing every
  zone below DOWN — never sliding over the cards beneath** (Walter's explicit
  requirement). The month grid: real weeks × 7 of the current month, day numbers,
  today's cell highlighted, leading/trailing other-month days muted, empty cells
  (no events exist yet).

**Body — an actual calendar table, not boxes:** a bordered 7-column grid reading
as one connected calendar: a header STRIP (one bordered row: weekday abbrev +
day number per column, vertical separators between columns; today's header cell
in the training-blue tint with the bolded `WED 10 · Today` form), and beneath it
full-height day COLUMNS (~180px min-height, shared vertical separators, no gaps
between cells — one table, not seven floating boxes). Today's full column is
tinted. Event pills land inside the cells when the calendar model exists; until
then the cells stay empty and one muted caption under the grid reads the
awaiting copy (`No scheduled events — the calendar model is pending.`).

## Zone 3 — Today's Plan

Heading + subtitle: `Your training, fuel, and protocol for today — built from your
goals, attributed to each specialist.`
**2×2 card grid** (Workout+Nutrition top, Supplements+Peptides bottom). Each card:
- Header row: accent-colored glyph dot + card title (accent-colored, 14px/600) +
  `via <specialist-slug>` muted caption; right-aligned status pill (tinted) — honest
  state: a muted pill reading `awaiting plan`.
- Body (designed internal anatomy, rendered as STYLED EMPTY STATES until the `1oh`
  plan schemas land — structure visible, no invented numbers):
  - **Workout:** a 4-slot stat-box row (Elapsed / Volume / Sets / Heart rate —
    boxes with 11px labels and em-dash values, the last box accent-tinted), then an
    exercise-list area with one dashed empty-state row (`No plan on file —
    plan-content schemas are the next slice.`).
  - **Nutrition:** a 4-slot calorie-arithmetic row (Goal − Food + Exercise =
    Remaining; em-dash values, Remaining box tinted), three thin macro-bar tracks
    (Protein/Carbs/Fat — empty tracks, label + em-dash, no fill), then the dashed
    empty-state row.
  - **Supplements:** an items-list area: dashed empty-state row only.
  - **Peptides:** a protocol-line area: dashed empty-state row only.
- Stat boxes: 1px border, radius 8px, centered 11px label over 16px value.

## Zone 4 — Performance & Trends

Heading + subtitle: `How you're tracking — recent readings per metric.` Legend
(existing semantic legend) right-aligned on the heading row or directly beneath.
**6-column grid of metric cards** (one card per tracked numeric item, in the
existing sort; wraps). Card anatomy, top to bottom:
- label (11px muted, clean display name),
- big value + units (20-22px/700),
- a delta/trend chip on the same row or under it: the existing trend verdict —
  tinted pill colored by its semantic state (improving=good tint, regressing=
  concern tint, flat/direction-only=neutral) with the arrow or word,
- the **bar sparkline** at the card bottom, full card width (the existing
  bar_sparkline component, state-colored as today).
Empty store: the zone renders one dashed awaiting card (existing copy).

## Zone 5 — Your Care Team

Heading + subtitle: `What each specialist tracks for you — every claim attributed
and evidence-gated.`
**4-column grid** of compact cards: name (13px/600, with a small leading glyph
dot), tracks-line (12px muted), status line (12px — honest state: `no rollup yet`
muted; when a rollup model lands this line carries the colored per-domain status).

## Zone 6 — Goals & Progress

Heading + subtitle: `Where each goal stands.`
Designed anatomy: full-width rows — goal label left, percent right, a thin
progress-bar track (radius 999px, `#E5E7EB`) with a good-green fill; plus a
landmark note card at the bottom. **Honest state (current):** one empty
progress-track row with the awaiting copy (`No goals on file — the goal-progress
model is pending.`) and NO percent — track rendered, no fill.

## Zone 7 — Labs & Bloodwork

Heading + subtitle: `Clinical detail — the supporting layer under your plan.`
One compact strip card rendering the zone's EXISTING routed content (the
ADR-0008/0009 D5 routing is untouched — biomarker chips in the mock belong to a
future lab-stream slice, NOT this pass):
- a `Pending draws:` row of bordered chips (one chip per `panel::` item: clean
  label + the stored value verbatim),
- watch-out rows (clean label + answers) and the latest physician note as muted
  caption lines (real `watch-out::`/`feedback::` data).
Empty store: the existing dashed awaiting copy inside the strip card.

## Print

The `@media print` block keeps: white page, ink text, borders collapse to plain
1px, shadows off, grids may flatten to fewer columns. Print-safe remains a
requirement (physician handoff path).

## What this spec does NOT change

- Zone order/titles, the routing contract (ADR-0008 D3), `PALETTE`/`SERIES`
  (decision-pinned), the honesty rule (ADR-0009 D2), single-file artifact rule
  (ADR-0004), bar-sparklines-not-paths.
- No new data models: every value rendered is a stored reading or a real date;
  every unbuilt slot renders designed chrome with an explicit empty state.
