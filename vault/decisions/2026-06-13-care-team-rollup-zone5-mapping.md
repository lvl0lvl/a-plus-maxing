---
title: Care-team rollup (Zone 5) — specialist→stream mapping + 30-day freshness status rule
type: decision
owner: Walter McGivney
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
permalink: a-plus-maxing/decisions/2026-06-13-care-team-rollup-zone5-mapping
---

# Care-team rollup (Zone 5) — mapping + 30-day status rule (adopted 2026-06-13, S58)

Resolves bead `a-plus-maxing-ektw` (the last awaiting dashboard zone). Records the two
design decisions the signed visual spec deliberately left UNSIGNED, so the build has a
signed target (PF-S49-01). Operator decision: Walter, "'a' sounds right" (S58), on the one
genuinely-open product question surfaced at session open.

## The problem (why Zone 5 was a design-then-build, not a signed-anatomy build)

`dashboard-v1-visual-spec.md:208` ("Zone 5 — Your Care Team") signs only the CARD ANATOMY
(name + leading glyph dot, tracks-line, status line) and the sentence: *"status line (12px —
honest state: `no rollup yet` muted; when a rollup model lands this line carries the colored
per-domain status)."* It does NOT sign:

1. **Which data drives each specialist's status** — the `_SPECIALISTS` tuple
   (`dashboard.py:122`) carries 16 `(slug, name, free-text tracks-line)` rows; there is no
   structured specialist→store-stream mapping.
2. **What the color means** — no aggregation rule, no status semantics, no 30-day window
   definition.

Verify-first at the S57 close established this (it drove the S57 pivot away from the rollup to
the fully-signed calendar-events). S58 records the decision here, THEN builds.

## Decision 1 — the specialist→store-stream mapping (v1)

Each specialist's status is derived from the store streams ALREADY attributed to it through
existing wiring (the `_PLAN_CARDS` `default_specialist` at `dashboard.py:85`, the labs streams,
the physician-note stream), plus the calendar event categories by their natural owner. Streams
read directly from the same `store_read` the dashboard already groups (`_readings_by_item`).

| Specialist | Streams |
|---|---|
| personal-trainer | `plan::workout`, `plan-track::workout`, `calendar::events`[training] |
| nutritionist | `plan::nutrition`, `plan-track::nutrition` |
| supplement-specialist | `plan::supplements`, `plan-track::supplements` |
| peptide-specialist | `plan::peptides`, `watch-out::*` (the peptide card already reads watch-out answers, ADR-0010 D5; `peptides` is in `PLAN_DOMAINS` but NOT `TRACKED_DOMAINS`, so no `plan-track::peptides`) |
| labs-specialist | `panel::*`, `biomarker::*`, `calendar::events`[lab-draw] |
| medical-liaison | `feedback::*`, `calendar::events`[appointment], `calendar::events`[check-in] |
| cardiovascular-specialist, dermatologist, endocrine-specialist, genetics-specialist, gi-specialist, longevity-strategist, lymphatic-specialist, mental-performance-coach, recovery-specialist, sleep-coach | **(no stream yet → `none`)** |

- **Excluded from the rollup:** `goal::*` (Zone 6 owns goals — cross-cutting, not
  specialist-attributed) and the unprefixed hero loop readings (Zone 1).
- **Honest sparseness:** 6 of 16 specialists have a stream in v1; the other 10 render the honest
  "no data yet" grey state. This is the explicit operator choice (Decision 3).

## Decision 2 — the 30-day freshness status/color rule

For each specialist, collect the `timepoint` of every reading across its mapped streams (plus
the dates of its mapped calendar event categories). Store timepoints are ISO strings — date-only
`YYYY-MM-DD` (plan/calendar, `_DATE_RE`-validated) OR full datetimes
`YYYY-MM-DDTHH:MM:SS+00:00` (the loop streams: panel/biomarker/watch-out/feedback) — so each is
reduced to its nominal calendar date via the house `datetime.date.fromisoformat(timepoint[:10])`
(the `render_views` date-axis convention, mirroring `component_set.reading_date`; an unparseable
or non-string timepoint contributes nothing — the same honest-absence degrade the trend card
takes, never a crash). Let `latest = max(dates)` and `days = (today -
latest).days` (a future `latest` — an upcoming scheduled event — yields `days <= 0`, treated as
current). The status:

| Status | Condition | Dot color (data-state) | Caption (muted) |
|---|---|---|---|
| `current` | has data, `days <= 30` (incl. future/today) | PALETTE `good` (green) | `updated {days}d ago` / `updated today` |
| `stale` | has data, `31 <= days <= 60` | PALETTE `watch` (amber) | `updated {days}d ago` |
| `dormant` | has data, `days > 60` | PALETTE `muted` (grey) | `updated {days}d ago` |
| `none` | no data in any mapped stream | PALETTE `muted` (grey) | `no data yet` |

Three colors (green / amber / grey); `none` and `dormant` share grey, distinguished by caption
text. The caption always states the EXACT age (the dot bands it) — non-redundant, and honest
about staleness rather than inventing a clinical judgment.

**Why freshness, NOT "on track / off track":** an adherence/target rule would need per-domain
targets that do not exist and are not signed — that is overreach (and the kind of fabricated
judgment the project's honesty discipline forbids). Recency of the latest data the specialist
is working from is a real, honestly-derivable signal, and directly useful for the July-visit
framing ("is each domain's data current?"). It is also color-blind-safe: status is conveyed by
BOTH the dot color AND the caption text, never color alone (WCAG).

## Decision 3 — the sparse-domain honesty handling (Walter's choice)

At session open, the genuinely-open product question was: given only 6 of 16 specialists have a
stream, should Zone 5 (a) show all 16 with honest grey "no data yet" on the empty domains, or
(b) only color the streamed few and leave the rest at the static "no rollup yet"? **Walter chose
(a).** All 16 cards render; the streamless 10 carry the grey `none` dot + "no data yet". The
all-empty store (no readings at all) keeps the current static "no rollup yet" caption (the
honest zone-level empty state, unchanged).

## AA / chrome-separation rationale

The status indicator is a **data-state dot** (a small colored circle on the status line), NOT
the name's leading glyph dot. ADR-0009 D3 (`component_set.py:44`) reserves ACCENTS for category
chrome and PALETTE `good`/`watch`/`concern`/`muted` for data state — so the freshness dot uses
PALETTE data-state hexes, and the name's category glyph dot is untouched. The dot is non-text
chrome (like the goal good-green fill, S56) → it adds NO new AA-gated text pair; the recency
text rides `muted` (already AA on paper). The render AA gate is therefore not extended, and
`b6um` (the `watch-text` sub-AA fix) is NOT triggered this session.

## Deferred refinements (not built here)

- **Wearable-vital → specialist sub-attribution.** When LM-02 (Oura) lands, `biomarker::hrv`/
  `rhr` → recovery-specialist and `biomarker::sleep-*` → sleep-coach (currently all `biomarker::`
  → labs-specialist). Deferred because there is no wearable data to attribute yet — mapping it now
  would be speculative (evidence-driven-design memory). All three render grey today regardless.
- **Append-order staleness.** The store drops append order (the `pq7m`/`z2d0` limitation); a
  backdated timepoint can mis-date `latest`. Out of scope — the rollup reads timepoints, same as
  every other read-model; the store sequence-field fix (`pq7m`) addresses the class globally.
