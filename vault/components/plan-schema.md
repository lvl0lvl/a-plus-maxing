---
title: plan-schema — plan-content / plan-tracking streams + absence states
type: reference
status: active
created: 2026-06-12
last_reviewed: 2026-06-12
review_cadence: on-change
permalink: a-plus-maxing/components/plan-schema
---

# plan-schema (`scripts/store/plan_schema.py`)

**What:** the plan zone's stream taxonomy and absence-state vocabulary over the store
(ADR-0010). Records per-domain specialist-attributed plan documents and per-domain
day-snapshot tracking; reads them back through two published absence states. Stores only
operator-entered data; writes only through `scripts.store.store` keyed by the one keying
Line Field Set — no second key, no second content-tag derivation (loop_schema's
`_content_tag` is imported).

**Contracts:**
- **Stream prefixes (disjoint item namespaces):** `plan::<domain>` (domain ∈
  `PLAN_DOMAINS` = workout/nutrition/supplements/peptides; timepoint = the plan's
  declared YYYY-MM-DD date; source = `plan::<specialist-slug>`, the attribution home;
  value = the structured plan document), `plan-track::<domain>` (domain ∈
  `TRACKED_DOMAINS` = workout/nutrition/supplements; day-snapshot values under
  content-tagged sources, so distinct same-day snapshots both persist). Peptide tracking
  IS the existing `watch-out::` stream — no fourth tracked domain.
- **Published absence states:** `NO_PLAN` (`no-plan`, zero stored plans) and
  `NO_PLAN_TODAY` (`no-plan-today`, plans on file but none dated the render date,
  carrying the latest on-file `plan_date`). Presence is not a marker: a resolved plan is
  `{state: None, plan, specialist, plan_date}`.
- **Writers** (`ValueError` only): `record_plan(domain, plan, plan_date, specialist,
  root)` — validates domain / YYYY-MM-DD date (date equality IS today-resolution, so a
  malformed date is rejected at the boundary) / non-empty specialist / the domain schema
  table; appends exactly one reading. Re-recording a CHANGED value for a stored identity
  is a store-dedupe no-op — never a silent overwrite. `correct_plan(...)` — same
  validation, delegates to `store.correct` (raises on a never-stored identity).
  `record_plan_tracking(domain, tracking, on_date, root)` — known-field type checks per
  the tracking tables.
- **Readers** (never raise on absence; ValueError on an unknown domain):
  `read_plan(domain, on_date, root)` / `read_plan_tracking(domain, on_date, root)`, both
  thin over the PURE `resolve_plan(readings, on_date)` / `resolve_tracking(readings,
  on_date)` — latest-appended wins within a date (the `read_panel` reversed-scan shape);
  no tracking snapshot for the date is `None`, never an invented empty snapshot.
- **Plan schema tables** (closed required, open extras — the ADR-0006 T2 seam):
  *workout* `exercises` (≥1 dicts: `name`, `sets` int ≥1; opt `load`/`reps`/`detail`);
  *nutrition* `calorie_goal` int >0, `macros` (all of protein/carbs/fat int >0), `meals`
  (≥1 dicts: `name`; opt `contents`/`kcal`), opt `water_l` >0; *supplements* `items` (≥1
  dicts: `name`, `dose`; opt `timing`); *peptides* `compound` (feeds
  `loop_schema.derive_watchout_questions`), `dose`, `route`, opt
  `cycle_week`/`cycle_length_weeks` int ≥1, `tags`, `evidence`.
- **Tracking tables** (all optional unless noted): *workout* `elapsed_min`/`volume_lb`/
  `heart_rate_bpm` numbers, `sets_done` dict name→int ≥0, `steps`/`kcal_burned`/
  `exercise_min` ints; *nutrition* `food_kcal`/`exercise_kcal` ints, `macros_g` (subset
  of protein/carbs/fat → ints), `meals_logged`, `water_l`; *supplements* `taken`
  REQUIRED (`{"taken": []}` is the explicit none-taken snapshot, distinct from no
  snapshot).

**Render integration (ADR-0010 D5):** the dashboard routes `plan::`/`plan-track::`
items to the zone-3 cards ONLY (unknown domain suffix KeyErrors; never `_metric_card`,
sparklines, zone 4, or zone 7); the peptide card additionally reads the grouped
`watch-out::` answers (second consumer, not a re-route). Slot-level honesty: absent
tracked values render em-dash/unfilled, derived slots only with all operands, controls
inert, awaiting copy digit-free. The report renders plan items as heading + verbatim
readings table — no KPI, no sparkline (a dict value never reaches numeric viz).

**Called by (production):** the type-routed dashboard template (zone 3), the report
template (verbatim-table route), the manual recording path (the `correction.py`
precedent; ADR-0006 T2 adopts the same surface).

**Governing ADR:** ADR-0010 (decisions D1-D6; build target
`vault/design/dashboard-v1-visual-spec.md` zone 3 as amended 2026-06-12).
