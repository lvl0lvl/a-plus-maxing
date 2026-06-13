---
title: z2d0 — recurrence-aware panel pending (both-sides timepoint bracket)
type: decision
owner: Walter McGivney
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
permalink: a-plus-maxing/decisions/2026-06-13-z2d0-recurrence-aware-panel-pending
---

# z2d0 — recurrence-aware panel pending (adopted 2026-06-13, S55)

Resolves bead `a-plus-maxing-z2d0` ("a re-recommended draw after any landed result
never reads pending"). Operator decision: Walter, "go with the both-sides heuristic"
(S55), after the conflict-with-a-pinned-contract was surfaced.

## The problem

`loop_schema.read_panel` resolved a panel to the most-recent landed result and
ignored pending markers entirely, so a panel that was recommended, resulted, then
**re-recommended** (a new draw recommended after the last result) kept reading the
stale result forever — never returning to `pending`. The report's "Order today" list
(`report._pending_panels`) had the analogous gap (`all(source == _TAG_PANEL)` excluded
any panel with a result, permanently).

## The conflict (why this is not a one-line fix)

A naive fix — "if the latest pending marker's timepoint > the latest result's
timepoint, read pending" — **breaks a pinned contract**:
`tests/store/test_loop_schema.py::test_pending_panel_reads_result_once_landed` pins
that *a result at an earlier-sorting timepoint than a pending marker still wins*
("the most-recent reading under a non-pending source tag wins **regardless of how its
timepoint sorts**"). The store sorts readings by timepoint and **does not retain append
order**, so a genuine re-recommendation (pending recorded *after* a result) and a
backdated result (pending marker that merely sorts later) are indistinguishable by a
single timepoint comparison — the two cases the bug and that pinned test need resolved
*oppositely*.

## The decision — both-sides timepoint bracket

A panel reads `pending` again iff a pending marker brackets the latest result on
**both sides** by timepoint:

- ∃ a pending marker with `timepoint <= latest_result.timepoint` (the original
  recommendation the result fulfilled), **and**
- ∃ a pending marker with `timepoint > latest_result.timepoint` (the re-recommendation).

Otherwise the most-recent landed result wins (the pre-existing order-independent
behavior). No result at all → `pending` (unchanged).

This threads the needle: it preserves **all five** pinned `read_panel` contracts
(a single later-sorting pending marker with no prior recommendation is the
backdated / no-prior case → result wins) **and** implements the realistic
recommend → result → re-recommend flow → `pending`.

Single-sourced: `read_panel` and the published `panel_pending(readings)` predicate
(bead `y91q`) both resolve through the pure helpers `_latest_result` + `_re_recommended`.
`panel_pending` is **provenance-based, never value-based** — a landed result valued the
literal string `"pending"` is a result, not a pending state (the r3pq render-boundary
residual stays the render layer's concern). `SUMMARY_FIELD_SET`, the keying Line Field
Set, and the four published render states are UNCHANGED.

## Accepted limitations

Both are the documented cost of the store not retaining append order: a read-model
heuristic cannot pair recommendations to results, so two histories with identical
{pending-timepoints} + {result-timepoints} multisets but different append orders are
indistinguishable yet have different correct answers. The store-schema/sequence
alternative (below) is the only full resolution.

1. **No prior recommendation.** A re-recommendation with **no** prior recommendation
   at-or-before the result (a result, then a single later pending marker, no earlier
   marker) is the same store shape as a backdated result and — per the pinned
   `test_pending_panel_reads_result_once_landed` contract — resolves to the result,
   not pending.
2. **Backdated second result (bead `pq7m`; surfaced by the PR #116 6-agent review,
   blind-triaged DEFERRED).** A panel recommended → resulted → re-recommended →
   resulted-again, where the SECOND result's timepoint is backdated before its own
   re-recommendation marker (`rec@06-01 → R1@06-08 → rerec@06-20 → R2@06-19`), reads
   PENDING though R2 has landed. This history is read-model-IDENTICAL to
   `rec@06-01 → R1@06-08 → R2@06-19 → rerec@06-20` (a genuine re-recommendation after
   the last result), which correctly reads pending — so no timepoint/count heuristic
   resolves both. The both-sides rule resolves the genuine re-recommendation; the
   count-rule (`#pending > #results`) would resolve the backdated case but regresses
   recommend-undrawn-twice-then-draw-once. LATENT in v1 (the panel loop has no
   production writer yet). Resolved only by the store append-order/sequence field below.

## Alternative considered (rejected for v1)

A store-schema sequence/generation field would track recurrence explicitly instead of
inferring it from timepoints, removing the accepted limitation. Rejected for this
build: it touches the `keying` Line Field Set (effectively locked) and is a larger
design conversation. Revisit if the no-prior-recommendation re-draw becomes a real
operator path.

## Revisit triggers ("breaks if")

- The store gains an append-order / sequence field → re-decide on the explicit-sequence
  mechanism (removes the accepted limitation).
- A panel is legitimately re-recommended at the SAME timepoint as its result → the
  strict-`>` re-recommendation side defers to result-wins; reopen if same-day re-draw
  must read pending.
- A consumer needs to distinguish "never resulted" pending from "re-recommended" pending
  → `panel_pending` returns one bool today; split the state if the render needs the grain.

## Cross-system notes

- **Render surfaces affected (the intended z2d0 outcome):** `render_views._panel_row`
  (via `read_panel`) and the report's "Order today" list (via `panel_pending`) now both
  surface a re-recommended panel as pending. The dashboard's panel rendering does not
  call `read_panel` and is unchanged.
- Built with bead `y91q` (the `panel_pending` publication + the formatter promotion) in
  the same PR — the predicate is the shared resolution point for both beads.
