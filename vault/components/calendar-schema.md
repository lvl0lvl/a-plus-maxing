---
title: calendar-schema — content-tagged event stream + date-grouped render
type: reference
status: active
created: 2026-06-13
last_reviewed: 2026-06-13
review_cadence: on-change
permalink: a-plus-maxing/components/calendar-schema
---

# calendar-schema (`scripts/store/calendar_schema.py`)

**What:** the dashboard zone-2 (This Week) data model. Records operator calendar events
as one content-tagged store stream and reads them back grouped by date for the
month-calendar render. Writes THROUGH `scripts/store/store.py` (`append`) on the one
`keying.py` Line Field Set — defines no second key, reimplements no store I/O, reuses
`loop_schema._reading` + `loop_schema._content_tag`. Local file I/O only; 0 model-bound
send.

**Contracts:**
- **Stream (one item, content-tagged sources — the `plan-track` pattern):**
  `calendar::events`. `timepoint` = the event's `YYYY-MM-DD` date; `source` = a content
  tag over the value (`_content_tag("calendar::", value)`), so two DISTINCT events on the
  same date both persist while an identical re-entry (same category + label + date) is an
  idempotent no-op; `value` = `{category, label}`. The `::` separator keeps the prefixed id
  a direct child of the store root. Disjoint from `biomarker::`/`panel::`/`plan::`/
  `plan-track::`/`goal::`/`watch-out::` and the fixed `feedback::physician-feedback` item —
  a shared bare name never cross-reads.
- **`EVENT_CATEGORIES`** = `("training", "lab-draw", "check-in", "appointment")` — the four
  signed event categories, ALSO the pill tint names the render pairs each event with
  (`component_set` CHROME `training`/`lab-draw`/`check-in`/`appointment` tint+text pairs,
  AA-measured). A category outside the set has no rendered tint pair (`pill` KeyErrors), so
  it is rejected at the writer (`_check_event`); `label` must be a non-empty str.
- **Date-only `timepoint`:** the render matches an event against a calendar day's
  `date.isoformat()`, so the writer rejects a timestamped or malformed date
  (`_check_date`) — a bad date would silently never land in a cell.
- **Corrections by re-recording:** the content-tagged stream is OUTSIDE `store.correct`'s
  content-independent-source contract (like the loop_schema watch-out/feedback streams);
  there is no `correct_event`.
- **Writers:** `record_event(category, label, on_date, root)` (append; idempotent on an
  identical event). **Readers:** `resolve_events(readings)` (pure; groups by date →
  `{date: [{category, label}, ...]}` in store-read order; empty → `{}`),
  `read_events(root)`. Writers raise only `ValueError`; readers never raise on absence.

**Render binding (`vault/design/templates/dashboard.py` zone 2):** `render` routes the
`calendar::events` item through `calendar_schema.resolve_events` into `events_by_date`,
passed to `_calendar_zone` → `_month_calendar`. Each day cell whose `date.isoformat()` has
events renders them as category-tinted pills (`cs.pill(label, category)`) inside a `.cal
.evlist` stack; a cell with no events keeps the bare day-number markup (the empty-store
path the calendar-shell tests pin). The muted awaiting caption (`No scheduled events — the
calendar model is pending.`) under the grid shows ONLY while no events are stored (ADR-0009
honest-absence). The event pills ride the already-measured CHROME category tint pairs — no
new AA-gated pair; the locked `PALETTE`/`SERIES`/`ACCENTS` are untouched.

**Demo data:** the model + render demo with synthetic events; real operator events are
LM-04-gated (no artifact generates until `generate.run` is fed real data).

**Adversarial tests:** `tests/store/test_calendar_schema.py` covers the store-adversarial
battery — cross-stream isolation, same-date distinct-events / idempotent re-entry, the
content-tag derivation, and the timepoint-field contribution — with the mutation battery
proven RED (drop the `calendar::` prefix → cross-stream test red; constant source instead
of the content tag → same-date-distinct + content-tag tests red; drop the timepoint from
the dedupe identity → same-event-distinct-dates red). `tests/generate/test_calendar_zone.py`
pins the in-cell pill render, the correct-day placement, and the honest empty state.
