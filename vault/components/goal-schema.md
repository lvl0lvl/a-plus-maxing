---
title: goal-schema — per-goal progress stream + read-derived percent
type: reference
status: active
created: 2026-06-13
last_reviewed: 2026-06-13
review_cadence: on-change
permalink: a-plus-maxing/components/goal-schema
---

# goal-schema (`scripts/store/goal_schema.py`)

**What:** the dashboard zone-6 (Goals & Progress) data model. Records operator goals as
one per-goal store stream and reads each back as its current progress percent. Writes
THROUGH `scripts/store/store.py` (append/correct) and the `keying.py` Line Field Set —
defines no second key, reimplements no store I/O, reuses `loop_schema._reading`. Stores
only operator-entered goal values; the percent is DERIVED on read, never stored. Local
file I/O only; 0 model-bound send.

**Contracts:**
- **Stream namespace (disjoint):** `goal::<slug>` — one progress stream per goal.
  `timepoint` = the snapshot's `YYYY-MM-DD` date; `source` = the constant `goal-progress`
  tag (one snapshot per slug+date by design); `value` = `{label, baseline, current,
  target[, unit]}`. The `::` separator keeps prefixed ids direct children of the store
  root (`store._item_path` guard). Disjoint from `biomarker::`/`panel::`/`plan::`/
  `plan-track::`/`watch-out::` and the fixed `feedback::physician-feedback` item —
  a shared bare name never cross-reads.
- **Value schema (closed-required, open-extras — the ADR-0006-T2 seam):** `label`
  non-empty str; `baseline`/`current`/`target` numbers (bool excluded); `unit` optional
  str; unknown extra keys permitted and ignored. **`baseline` != `target`** is a writer
  invariant (no progress span to measure; the percent denominator would be 0).
- **percent (read-derived):** `clamp((current - baseline) / (target - baseline), 0, 1) *
  100`, rounded to 1 dp. Direction-agnostic (target above OR below baseline → halfway
  reads 50%); FLOORED at 0 (a regression past baseline reads 0%, never negative); CEILED
  at 100 (overshoot reads complete, never > 100). Honesty rule (ADR-0009): no value is
  invented — absence resolves to None and the zone renders the awaiting state.
- **Writers:** `record_goal(slug, goal, on_date, root)` (append; a same (slug, date)
  re-record with a CHANGED value is a dedupe no-op, never a silent overwrite),
  `correct_goal(...)` (superseding append; the (slug, date) identity must already be
  stored or it raises). Writers raise only `ValueError`.
- **Readers:** `resolve_goal(readings)` (pure; the latest-timepoint snapshot wins —
  order-independent `max` by timepoint; empty → None), `read_goal(slug, root)`,
  `read_goals(root)` (enumerates `goal::` items via `store.items`, slug-ordered, skips a
  fully-corrupted item). Readers never raise on absence.

**Render binding (`vault/design/templates/dashboard.py` zone 6):** `render` routes
`goal::` items into `goal_readings`, then `_goals_zone` resolves each through
`resolve_goal` and renders a row per goal in slug order — label left, percent right
(`.goal-row .ghead`), a good-green (`PALETTE['good']`) progress-fill track — followed by
the landmark note card. Populated state only: with no goals the zone holds the honest
empty state (one unfilled track row + the digit-free awaiting copy, NO percent, NO
landmark card), per the signed `vault/design/dashboard-v1-visual-spec.md` zone 6. The
good-green fill is a non-text progress graphic (not a data-state semantic, not AA-gated as
a text pair); the row's label/percent ride the gated ink-on-paper pair.

**Demo data:** the model + render demo with synthetic fitness-domain goals; real operator
goals are LM-04-gated (no artifact generates until `generate.run` is fed real data).

**Adversarial tests:** `tests/store/test_goal_schema.py` covers the store-adversarial
battery — cross-stream isolation, same-key dedupe / dedupe-key boundary, correction path,
and a mutation battery proven RED with each `(item, timepoint, source)` dedupe-identity
field covered: drop the `goal::` prefix → cross-stream test red; drop the timepoint →
boundary test red; drop the source → source-field test red; give `record_goal` overwrite
behavior → rerecord-noop test red. `tests/generate/test_goals_zone.py` pins the
populated/empty render.
