---
title: Physician Face Sheet v1 — report design spec (transcribed from the signed mock)
type: design
status: approved
owner: walter
created: 2026-06-12
last_reviewed: 2026-06-12
depends_on: [dashboard-v1-visual-spec.md]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/design/physician-facesheet-v1-spec
---

# Physician Face Sheet v1 — report design spec

**Provenance:** designed S52 in Pencil through three operator review rounds; structure
and visual pass both operator-approved 2026-06-12 ("that face sheet structure is right" /
"new face sheet approved and saved to disk"). The signed mock is operator-held (saved
outside the repo per the ADR-0005 boundary); this note is the in-repo build target for
`report.py` (bead `nsxy`) per PF-S49-01. Sample values below describe SLOT SHAPE only;
the honesty rule (ADR-0009 D2) governs what actually renders.

## Product frame

A physician-facing patient face sheet, not a data dump: scannable in 90 seconds, leading
with DELTAS and ADHERENCE (the between-visit data no EHR has). One page first; detail
tables behind it. Print-native (the page IS the print form — no gray app chrome).

## Page frame

Own document identity, NOT the dashboard sheet: ~880px white page, 32px padding, 1px
`#E5E7EB` border, Inter. A 2px primary-blue (`#1F6FEB`) rule under the header block.
Sections separated by ~14px gaps; each section header carries a 4×16px rounded accent
bar in its section color (the semantic accent device — colors from the system ACCENTS
set so dashboard and report share one language).

## Page-one sections, in order

1. **Header** — `A+ Maxing — Physician Face Sheet` (20px/700) + prepared-date/visit
   caption right (12px muted). Status line (12px muted, one line): operator INITIALS
   only (never the full name in a tracked render), age band, issue status, last review,
   next visit.
2. **Since your last review** (the triage block — serves the artifact-design-protocol's
   tldr_banner slot in operator-approved form): indigo-tinted card (`#EEF2FD`, border
   `#C9D4F6`), blue accent bar + dark-blue title. Delta rows (12px), direction-colored:
   improving = good green `#117733` with ▲/▼, attention items (new compounds,
   experimental flags) = amber `#8A6D1F` with ●, neutral = ink. Rows sorted by clinical
   urgency. First-visit state: the card reads `No prior review — full baseline below`.
3. **Current regimen — with adherence** (teal bar `#0E9AA3`): rows of
   `name — dose · since <date>` left, adherence right (`100%` green; below threshold =
   amber `#B7791F` with missed-count, e.g. `94% · 2 missed`). Experimental compounds
   render the whole row detail in amber with `experimental — disclosure attached`.
4. **Biomarkers — out of range or trending** (crimson bar `#B42318`): abnormal rows on
   a rose tint (`#FBEAE8`, radius 8): marker name (12px/700 dark red `#7A2E22`), colored
   source glyph, `value · ref <range> · <numeric delta>/<window> · drawn <date>`, amber
   `watch` chip right. Then the in-range collapse strip (green tint `#EFF6F0`):
   `✓ N markers in range — full table with sparklines on page 2`. Abnormal-first always;
   clinical grouping on page 2, never alphabetical.
5. **Goals & trajectory** (green bar `#117733`): rows `goal label — status phrase` left
   + tinted status chip right (`on track` good tint; regressing = concern tint).
6. **Patient-generated signals — 30-day aggregates** (indigo bar `#5B5BD6`): 4 bordered
   stat boxes; each carries a 3px top edge in its SOURCE-TIER color, a colored tier
   glyph + label row (11px muted), and a 15px/700 value with direction arrow. Monthly
   aggregates only — never raw logs.
7. **Asks & agenda** (orange bar `#E8833A`, on an amber card `#FDF4E7`):
   `Order today:` + bordered chips (one per `panel::` pending draw), then
   `Patient questions:` line (the visit-agenda queue).
8. **Footer** — colored source-tier legend: `◆ lab-grade` blue `#1F6FEB` ·
   `● consumer wearable` teal `#0E9AA3` · `○ self-reported` amber `#B7791F`
   (glyph SHAPES distinct so monochrome print preserves the tiers) + the honesty line
   (`every value tagged · gaps stated, never inferred · local-first · print-safe`) +
   generation date.

## Page 2+ (detail layer)

The existing per-item render (readings tables with Date/Value/Source + sparklines),
re-ordered abnormal-first, each item carrying its source glyph and ref range. Watch-out
rows with operator answers live here too.

## Rules

- **Projection exclusion (operator decision, S52):** the naive-projection readout
  renders on the DASHBOARD trend card only — never on this report. An extrapolation
  must not read as clinical data.
- Every value carries its source tier; honesty rule governs all slots; print-safe.
- **Gating (honest awaiting states until the model lands):** renderable today —
  abnormal-first biomarkers, source tiers, watch-outs, pending draws, patient questions;
  gated — regimen+adherence (`1oh` plan schemas), since-last-review deltas (LM-01 visit
  anchoring), signal aggregates (LM-02 wearable baseline), goals (goal model).

## What this spec does NOT change

ADR-0004 single-file zero-script artifacts; the print contract; `PALETTE`/`SERIES`/
`ACCENTS` (locked — the accent coding above REUSES them); the dashboard's own spec.
