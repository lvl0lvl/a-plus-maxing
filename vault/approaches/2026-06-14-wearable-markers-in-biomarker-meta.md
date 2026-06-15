---
name: wearable-markers-in-biomarker-meta
type: approach
status: abandoned
session: S63
date: 2026-06-14
supersedes: none
tags: [store, biomarker-meta, dashboard, wearable]
---

# Registering the WHOOP wearable markers (recovery/strain/spo2) in `biomarker_meta`

**What was tried:** During the S63 WHOOP/noop adapter build, adding units +
`good_direction` (polarity) rows for the new wearable markers `recovery`,
`strain`, and `spo2` to `scripts/store/biomarker_meta.py`, so the dashboard could
render them with a reference-state tint and a recent-trend direction (the same
treatment `rhr`/`hrv` get).

**Why abandoned:** The registry rows broke 5 dashboard/trend tests that
DELIBERATELY use `recovery`/`strain`/`spo2` as *unregistered-marker* exemplars
(they assert honest-absence: an unregistered marker reads `None`, renders
trend-only, never a fabricated state/value judgment). Registering the markers
turned those exemplars into registered markers and the honest-absence assertions
flipped. Caught immediately by running the full suite; reverted same-session. The
markers render trend-only via honest-absence in the meantime. Evidence:
`memory/process-failures.md` Session 63 (S63 PF "Observed, NOT promoted" (a));
current `scripts/store/biomarker_meta.py` registers `rhr`/`hrv` but NOT
`recovery`/`strain`/`spo2`; the unregistered-exemplar assertions live in
`tests/store/test_biomarker_meta.py` + the trend/dashboard tests.

**What would change the verdict:** When the dashboard/trend tests are first
rewritten to NOT depend on `recovery`/`strain`/`spo2` being unregistered (pick a
different unregistered exemplar, e.g. a `mystery-marker`), the registry rows can
be added without breaking honest-absence coverage. Registering them is only safe
AFTER that test migration — not before. (And only with real, person/goal-aware
reference ranges where applicable; `strain`/`recovery` have no population range —
their `reference_range` stays `None`, polarity only.)

**Cross-references:**
- `memory/process-failures.md` Session 63 (the build-then-verify catch + the
  "flagged-optional registry expansion has dashboard-test blast radius" lesson).
- `scripts/store/biomarker_meta.py` (the registry seam).
- ADR-0011 (the WHOOP/noop adapter that introduced these markers).
