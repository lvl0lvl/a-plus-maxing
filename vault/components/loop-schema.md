---
title: loop-schema — stream taxonomy + published store states
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/loop-schema
---

# loop-schema (`scripts/store/loop_schema.py`)

**What:** the data-in loop's stream taxonomy and state vocabulary over the store. Defines
the four prefixed stream namespaces and the five published states the render layer maps
1:1. Stores only operator-entered data; derives watch-out question SETS from active
protocols; raises no automated signal.

**Contracts:**
- **Stream prefixes (disjoint item namespaces):** `biomarker::<name>` (numeric readings,
  source `manual`), `panel::<name>` (value `"pending"` until a result lands),
  `watch-out::<name>` (string answers), `feedback::physician-feedback` (free-text
  entries, one fixed item). The `::` separator keeps prefixed ids direct children of the
  store root.
- **Published states:** `pending`, `not-yet-answered`, `no-data` (zero timepoints),
  `no-prior` (exactly one), `answered-over-time`. Render maps the four absence/pending
  states 1:1 (`render_views._STATE_DISPLAY`); `answered-over-time` has no display row
  (an answered watch-out renders its answers); an unmapped state KeyErrors.
- Writers: `record_biomarker / record_pending_panel / record_watchout_answer /
  record_physician_feedback`. Readers: `read_biomarker` (returns
  `{state, timepoints}` — state None when ≥2 timepoints), `read_panel`,
  `read_watchout(_answers)`, `read_physician_feedback`.
- Same-timepoint distinct values persist via `_content_tag` (value-hash folded into the
  source tag, since the store dedupe identity excludes value).
- The store is the carry-forward medium: answers/feedback recorded in one generation are
  next-generation inputs (nothing expires or is overwritten).

**Called by (production):** `render_views` (typed reads), the type-routed dashboard
template (stream-prefix routing over `generate._read_store`'s flat read model), the
plan loop.

**Governing ADR:** ADR-0007 (placement: loop state = store schema; matrix/projection =
render-time views).
