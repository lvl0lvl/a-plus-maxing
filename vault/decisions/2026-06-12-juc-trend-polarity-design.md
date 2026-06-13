---
title: juc — recent-trend-direction per-marker polarity design (adopted)
type: decision
owner: Walter McGivney
created: 2026-06-12
last_reviewed: 2026-06-12
status: active
permalink: a-plus-maxing/decisions/2026-06-12-juc-trend-polarity-design
---

# juc — `recent-trend-direction` per-marker polarity design (adopted 2026-06-12, S53)

Resolves the four S51-adjudicated sub-questions on bead `a-plus-maxing-juc`. Analysis
produced by an Architect-profile dispatch (full profile inlined per INV-ROLE-INLINING)
against the live code (`scripts/plan/router.py`, `scripts/store/biomarker_meta.py`,
`scripts/store/keying.py`, ADR-0006-T0/T1, ADR-0008); operator adoption: Walter,
"adopt all four as recommended" — including the explicitly-surfaced sub-call to keep
the daily-cadence streams (rhr, hrv, sleep-hours) in the v1 feed.

## The four decisions

1. **Feed (which streams):** registry-driven fixed list — every marker in
   `biomarker_meta.METADATA` with non-None `good_direction`, read under the
   `biomarker::` namespace only. The source set is version-controlled via the
   registry, never hand-retyped, never store-enumerated, never goal-filtered.
   Daily-cadence streams included for v1; revisit trigger below.
2. **Aggregation:** worst-wins over the per-stream trends — any `regressing` →
   `regressing`; else any `improving` → `improving`; else `flat`. The locked
   ADR-0006-T0 vocabulary and `SUMMARY_FIELD_SET` are UNCHANGED (no Security
   MEDIUM-2 change-control event). Per-stream trends are computed per stream
   (each stream's own last two numeric readings via `biomarker_meta.trend`),
   then reduced — the existing cross-item and unknown-polarity raises in
   `_trend_token` stay untouched.
3. **Plumbing/boundary disposition:** the field gets a DISTINCT, named
   registry-driven derivation mechanism with its own load-time tripwire
   (sources == the registry-polarity set; no source stream name in
   `SUMMARY_FIELD_SET`; output pinned to `TREND_DIRECTIONS`). The
   `raw-lab-values` → `recent-trend-direction` entry is REMOVED from
   `_RAW_TO_FIELD`; `raw-lab-values` REMAINS permanently in `EXCLUDED_RAW_PII`
   (the exclusion is the boundary promise; the mapping was only derivation
   plumbing). No generic-stream fallback feed (it could never produce a labeled
   trend; speculative machinery). Boundary promise unchanged and strengthened:
   only the derived closed-vocabulary token crosses the PII boundary, never a
   lab value. The registry-polarity `biomarker::` stream names do NOT join
   `EXCLUDED_RAW_PII` — that set enumerates raw-PII item classes, the new
   streams never enter `_RAW_TO_FIELD`, the dispatch whitelist already rejects
   them as payload fields, and the new mechanism's tripwire owns their
   disjointness from `SUMMARY_FIELD_SET`. This resolves the second half of S51
   sub-question (c).
4. **Zero-lab-stream operator:** emit the no-signal `flat` instead of the
   partial-summary block. Rationale (required, since this touches a deliberate
   S39 behavior): the surviving fail-closed raises both prevent WRONG
   AFFIRMATIVES (fabricated polarity, cross-item pseudo-trend); the removed
   block was suppressing a TRUE NEGATIVE ("no lab-trend signal" is the true
   statement about a fresh operator) and ran the ADR-0007 loop backwards (the
   plan is what tells a fresh operator which labs to get). `dispatch`'s
   partial-summary raise itself is untouched.

## Revisit triggers ("breaks if")

- Registry grows operator-edited entries → the version-controlled-source-set
  property needs re-deciding.
- The token saturates `regressing` under daily-stream noise → reopen the feed
  (cadence facet/subset) as its own design conversation; do not weaken worst-wins.
- Plan quality shows the model needs marker-level attribution → field-set
  amendment becomes a deliberate ADR (one-way door), not a default.
- `flat` acquires an affirmative "stability" meaning to any plan consumer → the
  no-data/flat conflation becomes a fabricated stability claim; an explicit
  no-signal vocabulary amendment becomes the necessary fix.
- Any feed source outside `biomarker::` (e.g. `panel::`) added without extending
  the mechanism's tripwire.

## Cross-system notes (recorded for downstream work)

- **Registry is now dual-surface:** a `good_direction` edit changes both the
  dashboard chips AND the model-bound summary token. Registry polarity edits get
  a review note from this decision forward.
- **Surface disagreement is by design:** the dashboard shows per-marker grain;
  the summary shows the worst-wins aggregate (eight improving chips can coexist
  with a `regressing` summary). To be stated in the operator-facing visual spec
  when the worst-wins summary token ships (the `juc` router build — the
  disagreement only materializes once the aggregate exists; Package B's
  per-marker cards landed without it, correctly).
- **Registry validity pin justified non-speculative:** every `in-range` entry
  must carry a `reference_range` (an in-range marker without one is a
  polarity-bearing feed marker producing an unlabelable trend).
- **Caller-binds-clone-root (bead `e3b`)** applies to the new multi-item reads
  unchanged — they ride the existing bound `store_read` surface.

## Build

The build brief lives on bead `a-plus-maxing-juc` (notes). The router mechanism
build is separable from Package B (different surface: plan dispatch vs dashboard
render); it is scheduled as its own unit when capacity allows. Decisions 1+2
also bind Package B's trend-card rendering semantics (per-marker grain via
`biomarker_meta.trend`, consistent with the summary's per-stream rule).
