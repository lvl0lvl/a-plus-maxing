---
title: care-team-rollup — per-specialist 30-day freshness read-model
type: reference
status: active
created: 2026-06-13
last_reviewed: 2026-06-13
review_cadence: on-change
permalink: a-plus-maxing/components/care-team-rollup
---

# care-team-rollup (`scripts/store/care_team_rollup.py`)

**What:** the dashboard zone-5 ("Your Care Team") data model. A pure READ-MODEL — NO new
store stream, no write path, no keyed dedupe identity. It attributes each existing store
reading to at most one specialist and reduces the specialist to a 30-day recorded-data
freshness status the zone-5 render colors. The design rationale (the mapping, the rule, the
sparse-domain honesty choice) lives in the decision note
`vault/decisions/2026-06-13-care-team-rollup-zone5-mapping.md` (Walter-confirmed, S58); this
page is the interface reference. Imports only `datetime`; local, read-only.

**Interface:**
- **`resolve_rollup(store_read, today) -> {slug: {state, days}}`** — pure over the
  `store.read_all` read model. Each reading routes to a specialist by item prefix
  (`SPECIALIST_STREAMS`) or, for `calendar::events`, by its value category
  (`_CATEGORY_OWNER`); the specialist's status is taken from its latest RECORDED-DATA
  timepoint. A specialist with no mapped recorded data is ABSENT from the result (the render
  fills the honest "no data yet" grey state). `state ∈ {current, stale, dormant}`; `days` is
  the non-negative age `today - latest`.
- **`SPECIALIST_STREAMS`** — `slug -> (item prefixes, calendar event categories)`. The 6
  mapped specialists: personal-trainer (`plan::workout`/`plan-track::workout`/training),
  nutritionist (`plan::nutrition`/`plan-track::nutrition`), supplement-specialist
  (`plan::supplements`/`plan-track::supplements`), peptide-specialist
  (`plan::peptides`/`watch-out::`), labs-specialist (`panel::`/`biomarker::`/lab-draw),
  medical-liaison (`feedback::`/appointment/check-in). The other 10 specialists are absent
  (streamless) → honest grey. Prefixes are disjoint across specialists.
- **`CURRENT_MAX_DAYS` = 30, `STALE_MAX_DAYS` = 60** — the freshness band edges:
  `days <= 30` current, `31..60` stale, `> 60` dormant. `none` (no data) and `dormant` share
  the grey dot, distinguished by caption.

**Contracts / invariants:**
- **Future timepoints are EXCLUDED** (`day > today` skipped): a scheduled event is activity
  shown in Zone 2, not recorded data — labeling it "updated today" would be a false data
  claim (the #122-review honesty refinement). A future-only specialist reads "no data yet".
- **`goal::` and unprefixed hero loop readings are EXCLUDED** — Zone 6 owns goals; the hero
  loop metrics are Zone 1.
- **Timepoint tolerance:** `_timepoint_date` reduces an ISO timepoint (date-only plan/calendar
  OR full-datetime loop streams) via the house `datetime.date.fromisoformat(timepoint[:10])`
  under `except (TypeError, ValueError) -> None` — an unparseable/non-string timepoint
  contributes nothing (the same honest-absence degrade as `component_set.reading_date`; the
  parser is mirrored store-layer-local to avoid a `vault/design/templates` import inversion).
- **Parallel read, fail-loud preserved:** `resolve_rollup` reads the same `store_read` the
  `dashboard.render` routing loop iterates; it runs strictly AFTER that loop's fail-loud
  KeyError on any unrouted `::` prefix, so silently ignoring an unmapped item here never
  masks a routing gap.
- **Chrome/data-state (ADR-0009 D3):** the render's freshness dot (`.sdot-*`) is PALETTE
  `good`/`watch`/`muted` data-state chrome (non-text), a SEPARATE element from the name's
  category glyph `.dot` — no accent on data state, no new AA-gated text pair.

**Consumers:** `vault/design/templates/dashboard.py` `render()` → `_care_team_zone(rollup)`.

**Tests:** `tests/store/test_care_team_rollup.py` (mapping, band boundaries, calendar
routing, future-exclusion, order-independent latest-wins, cross-stream isolation + real
`store.read_all` end-to-end, unparseable-skip; mutation battery proven RED per the per-test
docstrings — dedupe categories N/A for a read-model). `tests/generate/test_care_team_zone.py`
(colored status render, streamless grey, all-empty static fallback, exact captions,
no-accent-leak, no-raw-key-leak).
