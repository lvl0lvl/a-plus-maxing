---
title: loop-schema — stream taxonomy + published store states
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-12
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
  source `manual`), `panel::<name>` (pending markers under `plan-recommendation`, landed
  results under content-tagged `panel-result` sources), `watch-out::<name>` (string
  answers), `feedback::physician-feedback` (free-text entries, one fixed item). The `::`
  separator keeps prefixed ids direct children of the store root.
- **Published states:** `pending`, `not-yet-answered`, `no-data` (zero timepoints),
  `no-prior` (exactly one), `answered-over-time`. Render maps the four absence/pending
  states 1:1 (`render_views._STATE_DISPLAY`); `answered-over-time` has no display row
  (an answered watch-out renders its answers); an unmapped state KeyErrors. A landed
  panel result is a VALUE returned by `read_panel`, not a fifth marker — render_views
  renders it as a value row (bead s38+byj).
- Writers: `record_biomarker / record_pending_panel / record_panel_result /
  record_watchout_answer / record_physician_feedback`. Readers: `read_biomarker`
  (returns `{state, timepoints}` — state None when ≥2 timepoints), `read_panel`
  (order-independent pending→result resolution: the most-recent reading under a
  non-pending source tag wins (its value returned verbatim) regardless of timepoint
  sort, else `pending`), `read_watchout(_answers)`,
  `read_physician_feedback`.
- Same-timepoint distinct values persist via `_content_tag` (value-hash folded into the
  source tag, since the store dedupe identity excludes value).
- The store is the carry-forward medium: answers/feedback recorded in one generation are
  next-generation inputs (nothing expires or is overwritten).
- All readers inherit `store.read`'s latest-wins identity resolution (bead 1vi): an
  explicit `store.correct` superseding append reads back as the corrected value with the
  timepoint COUNT unchanged, so the published states (no-data / no-prior) never flip on
  a correction. Content-tagged streams (watch-out / feedback / panel results) carry
  per-value source tags, so their carry-forward lists are untouched by the READ
  resolution; the write primitive (`store.correct`) is out-of-contract for those
  content-tagged identities — the supported correction story there is re-recording.

**Called by (production):** `render_views` (typed reads), the type-routed dashboard
template (stream-prefix routing over `store.read_all`'s flat read model), the
plan loop.

**Governing ADR:** ADR-0007 (placement: loop state = store schema; matrix/projection =
render-time views).
