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
bar in its section color (the semantic accent device). Where the section's category
exists in the locked ACCENTS set, the bar reuses ACCENTS — regimen teal `#0E9AA3`
(supplements), signals indigo `#5B5BD6` (sleep), asks orange `#E8833A` (nutrition) —
and the header rule + lab-grade tier glyph reuse ACCENTS training blue `#1F6FEB`, so
dashboard and report share one language at the category-bar level. Two bars do NOT
come from ACCENTS: the Biomarkers crimson `#B42318` is a NEW report-local token, and
the Goals bar reuses PALETTE good `#117733` as section chrome — a signed-mock
exception to the chrome/data-state separation, recorded as such. Nine hexes in this
spec are repo-novel report-local tokens sanctioned by the signed mock: `#B42318`,
`#8A6D1F`, `#B7791F`, `#EEF2FD`, `#C9D4F6`, `#FBEAE8`, `#7A2E22`, `#EFF6F0`,
`#FDF4E7`. **BUILD OBLIGATION:** at build time the report-local hexes are registered
as named constants (a report-token set beside `ACCENTS`/`CHROME` in
`component_set.py`) and every text/background pair they form is measured by the AA
gate; the Goals bar's reuse of the data-state green as section chrome is recorded as
a signed-mock exception to the chrome/data-state separation.

**[AMENDED 2026-06-12, S53 (bead `nsxy`): the nine-token framing, the BUILD
OBLIGATION above, and the Goals-bar exception are SUPERSEDED by the
standardized-token blocks below — the v3 bindings govern; this paragraph is the
historical signed-v2 record.]**

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

**Data-state adjudication (report-local):** the abnormal/attention data-state colors
above (`#B42318`/`#7A2E22`/`#FBEAE8` red-family; `#B7791F`/`#8A6D1F` ambers) are
report-local tokens from the signed mock and deliberately diverge from the dashboard's
colorblind-safe PALETTE concern/watch. The CVD guard on the report is glyph/shape
redundancy — the source-tier glyphs and direction arrows this spec already defines —
so color is never the sole carrier of a data state. The build registers these as
report-state tokens and AA-measures every text/background pair they form (the same
obligation as the Page frame's report-local tokens). The dashboard and report share
one language only at the ACCENTS category-bar level, not at the data-state level.

**[AMENDED 2026-06-12 (bead `nsxy`)]: report-local color tokens -> standardized
system tokens. Reason: operator direction at S53 ("shouldn't the colors for the platform be
standardized so future builds operate within the design theme? If the facesheet does
not match the dashboard, that seems like an issue") — supersedes the report-local
adjudication paragraph above and the Page frame's nine-report-local-token framing.**

- **Data states re-map to the locked PALETTE:** out-of-range/abnormal renders in
  PALETTE concern `#882255` (with its measured tint pair and AA-darkened text
  variant per the existing CHROME `*-text` pattern); attention/below-threshold and
  the `watch` chip render in PALETTE watch `#DDAA33` semantics (AA-darkened watch
  text token on tints — never raw `#DDAA33` text on white); improving/in-range
  stays PALETTE good `#117733`; the in-range collapse strip uses the measured good
  tint pair. The red-family/amber hexes (`#B42318` as a data state, `#7A2E22`,
  `#FBEAE8`, `#B7791F` as text, `#8A6D1F`) and the report-local in-range strip
  green `#EFF6F0` do NOT ship.
- **Chrome/data-state separation holds everywhere — no signed-mock exception:** the
  Goals bar does not use data-state green as chrome; it and the Biomarkers bar get
  section-accent tokens registered in the SYSTEM token set (`component_set.py`,
  beside ACCENTS — values chosen and operator-signed at the Package C design round,
  AA-measured by the gate like every other registered token). Card tints
  (`#EEF2FD`/`#C9D4F6`, `#FDF4E7`) likewise resolve to system tokens (existing
  measured tints where suitable, else registered) at the same round.
- **One language, both surfaces:** dashboard and report share the full design
  vocabulary — ACCENTS for category chrome, PALETTE + measured tint pairs for data
  state. Glyph/shape redundancy stays as specified (it is a print/monochrome
  guarantee, not a divergence compensator).
- **PF-S49-01 consequence:** the signed mock's colors change under this re-map, so
  Package C starts with an updated Pencil render + operator sign-off BEFORE any
  `report.py` code; this amendment is the recorded direction, not the signed visual.

**[AMENDED 2026-06-12, S53 (bead `nsxy`) — the v3 standardized render is
SIGNED]:** the Pencil re-render carrying this re-map ("Physician Face Sheet — v3 (standardized tokens)")
was reviewed on screen and operator-approved ("approved and saved"); the signed v3
mock is operator-held per ADR-0005. The v3 token bindings, exact:

- **New system tokens to register in `component_set.py` at build (all rendered
  pairs gate-measured):** `biomarkers` section accent `#B42318` (the v2 crimson,
  kept — now a SYSTEM section accent; named for the section it colors, distinct
  from the `lab-draw-*` event tints and the lab-grade source tier); `goals`
  section accent `#2E8B57` (replaces the data-state green as section chrome);
  `watch-text` `#8A6D1F` (the AA-dark form of PALETTE watch — supersedes the
  "does NOT ship" listing of this hex above: it ships as the registered
  watch-text token, not as an ad-hoc amber; also the fix vehicle for the `b6um`
  sub-AA watch-text class); `watch-tint` `#FCF7EA` (pre-measured at the #111
  review: 4.58:1 with `watch-text` `#8A6D1F` — the originally recorded `#FAF3E0`
  computed 4.42, below the 4.5 floor; the signed text amber is kept, the tint
  lightened). Registration shape: the section accents land in a NEW named
  constant (e.g. `SECTION_ACCENTS`) beside `ACCENTS` — NOT as new `ACCENTS`
  keys: `component_set._TINTABLE` is built from `*ACCENTS` and `_tint_rules()`
  indexes `CHROME[name+'-tint']`/`CHROME[name+'-text']` for every tintable name,
  so an ACCENTS key without its CHROME pair KeyErrors every render.
- **Re-mapped to existing measured tokens:** abnormal rows -> concern `#882255` on
  concern-tint `#F3E9EE`; in-range strip + adherence chips -> good-tint `#E7F1EB`;
  triage card -> training-tint `#EAF1FD` with `training-text` `#1D67DB` title;
  asks card -> nutrition-tint `#FDF3EB`; borders -> card-border `#E5E7EB`; small
  captions -> muted `#555555`; footer source-tier legend text -> the `*-text`
  shades (`#1D67DB` lab-grade, `#0B787F` wearable, `#8A6D1F` self-reported (the
  NEW `watch-text` token above, not a pre-existing CHROME entry)). Source-tier
  colors everywhere (section-4 row glyphs, section-6 stat-box top edges + tier
  glyphs, footer legend): tier TEXT renders the `*-text` triple
  `#1D67DB`/`#0B787F`/`#8A6D1F`; non-text tier edges and glyph fills keep the
  base triple `#1F6FEB`/`#0E9AA3`/`#B7791F` as source-tier chrome (per the
  signed v3 mock) — `#B7791F` ships ONLY as non-text tier chrome, never as text.
- **Unchanged (correct usages):** improving/in-range data states PALETTE good
  `#117733`; the ACCENTS section bars (supplements teal, sleep indigo, nutrition
  orange) + the training-blue header rule; glyph shapes ◆/●/○.
- The v2 hex literals in the body above are the historical signed record; the v3
  bindings in this block govern the build.

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
  **[AMENDED 2026-06-12, S53 build (bead `nsxy`): the regimen gate is PARTIALLY
  satisfied — the `1oh` plan schemas landed, so plan CONTENT renders from today's
  `plan::supplements`/`plan::peptides`; the adherence % column stays an em-dash
  awaiting state until the 30-day adherence aggregate model exists.]** Header
  status line: age band + issue status source from `vault/meta/operator-profile.md`,
  which is still an unfilled scaffold (the Demographics age and January-issue status
  prompts are blank) — gated with em-dash awaiting slots until the profile is filled;
  last review + next visit are gated on LM-01 visit anchoring, also em-dash awaiting
  slots. **[AMENDED 2026-06-12, S53 build (bead `nsxy`): the header fields source
  from the ADR-0005 filled-scaffold copy (`vault/scaffold/filled/operator-profile.md`)
  when present, else the tracked scaffold's awaiting state.]**
- **Section 2 awaiting state:** until LM-01 visit anchoring lands, the card renders
  the first-visit copy (`No prior review — full baseline below`), which is literally
  true in both the first-visit and model-not-landed conditions — the first-visit copy
  doubles as the awaiting state.

## What this spec does NOT change

ADR-0004 single-file zero-script artifacts; the print contract; `PALETTE`/`SERIES`/
`ACCENTS` (locked — their VALUES are untouched; per the [AMENDED 2026-06-12]
standardization the report draws on the locked sets plus the four v3-registered
system tokens (two section accents + the watch-text/watch-tint data-state pair),
with no report-local color vocabulary); the dashboard's own spec.
