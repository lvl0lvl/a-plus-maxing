---
title: Session 82 — Apple Health adapter (real export.xml ingestion)
type: session
date: 2026-06-20
owner: Walter McGivney
status: complete
---

# Session 82 — Apple Health (HealthKit) adapter: scaffold → real `export.xml`

**Goal:** Build the first REAL-data ingestion adapter — upgrade the Apple Health (HealthKit) adapter from a fabricated-JSON scaffold to streaming the operator's real Apple Health `export.xml`. The operator uses Apple Health, not Whoop.

**Outcome:** PR #199 → `main` @ `b83b12b` (rebase). Full suite 1160 passed / 3 skipped on final `main`; core-capability gate green (untouched — pure ingest).

## What was built

`scripts/ingest/adapters/healthkit.py` (UPGRADED — the scaffold already existed, so this was an upgrade, not a new `apple_health.py`):

- **Streamed read (D1):** parse `export.xml` with `xml.etree.ElementTree.iterparse`, `root.clear()` after each record — memory bounded by the number of distinct (day, item) pairs, not the export size (the export can be 100s of MB). Missing / non-XML file raises (fail-loud).
- **Daily aggregation (D2):** Apple stores RAW per-sample `<Record>`s; the adapter aggregates them to ONE value per (item, day) — the daily MEAN keyed on `startDate`'s calendar date — to match the store's one-reading-per-(item, day, source) key. The granularity difference from the pre-aggregated wearable DB; the one piece of genuinely new logic. Rounded to 2 decimals.
- **Metric map + spo2 scale (D3):** the value-domain-clean HK types — `HeartRateVariabilitySDNN`→hrv, `RestingHeartRate`→rhr, `RespiratoryRate`→resp-rate carry the store unit as-is; `OxygenSaturation`→spo2 is scaled ×100 (HealthKit stores the 0–1 fraction; the store `spo2` item is a percent). Unmapped types yield nothing.
- **Coexistence (D4):** `source_tag` stays `"healthkit"`, device-specific, so a HealthKit reading and a wearable reading at the same (item, day) stay distinct under the (item, timepoint, source) dedupe key. Whoop is NOT disabled — "Apple Health instead of Whoop" is achieved by providing a HealthKit export and no Whoop export (the scheduler runs only the adapters it has an export for).

Documented in **ADR-0012**. `tests/ingest/conftest.py` (NEW at review) single-sources the export test helper.

## Deferred (value-domain-grounded — bead `dfbi`)

- `skin-temp-dev` — Apple's `AppleSleepingWristTemperature` is an ABSOLUTE °C, but the store item is a deviation-from-baseline; deriving the deviation needs a per-operator temperature baseline (the Health app's job).
- `sleep-efficiency` — Apple records sleep as stage records (InBed/AsleepCore/Deep/REM/Awake); efficiency = asleep ÷ in-bed needs a stage-duration roll-up.
- recovery/strain have no Apple equivalent (Whoop-proprietary composites; honest absence).
- Registering the wearable-only store items (spo2/resp-rate/recovery/strain/...) in `biomarker_meta` — a pre-existing condition from the ADR-0011 whoop precedent.

## Two CHANGED items vs the S82-plan (flagged, not silent)

1. The plan said CREATE `apple_health.py`; the scaffold already existed → reframed as an UPGRADE of `healthkit.py` (`source_tag` stays `"healthkit"`).
2. The plan said flip `whoop.py` to `UNWIRED`; the build chose COEXISTENCE (ADR-0012 D4) — disabling a working adapter is unnecessary given the export-presence + device-tag distinction.

## Review (Tier-1/2/3)

- **Tier-1:** pytest; the healthkit format change broke 4 `test_scheduler.py` cases (fixture fed JSON + asserted `store.read("steps")`) — fixed (repointed at `export.xml` + a mapped HK type) as the necessary call-chain consequence; the spo2 ×100 binary-float artifact fixed with `round(…,2)`.
- **Tier-2:** plan-integrity INTEGRITY-CLEAN; QA 6 SHOULD-FIX coverage gaps fixed (the REAL nested-children Apple Record shape, missing-field skip, record-level fail-loud, empty export, spo2 sub-percent rounding, two-metrics-same-day independent aggregation), vacuity audit PASS.
- **Tier-3 `/review-pr` 6-agent** over the THREE-dot diff: security PASS (SEC-1 NOT_ACTIONABLE — XXE/billion-laughs probes EXECUTED clean on the real 3.14/expat-2.7.1 runtime; hardening = unapproved defensive programming); bug-hunter 0 findings (17 trigger inputs executed); contracts "contracts met" (numstat EXECUTED); historical 0 regressions; code-quality + test-coverage → 4 LEGITIMATE (QUAL-1 root.clear() comment, QUAL-2/3 forked test helpers → single-sourced into `conftest.py`, **TEST-001 the round() vacuity gap**) fixed + blind-verified RESOLVED 4/4; TEST-002 NOT_A_BUG.

## The notable finding — TEST-001 (a vacuity near-miss)

The Tier-2 QA pass added a spo2 sub-percent rounding test (`0.976 → 97.6`) intending to cover the ADR-0012 D2 `round(…,2)` decision, but that test does NOT pin `round()` because `0.976*100 == 97.6` is IEEE-754-exact. The independent Tier-3 test-coverage agent caught it by EXECUTING the round()-removal mutation (the suite stayed GREEN), and it was fixed with a non-terminating-mean test (`mean(50,51,53)=51.3333… → 51.33`) proven RED-when-`round()`-removed. The no-tautological-test discipline working as designed; the S82 watch is: every documented numeric decision (scale/round/aggregate) gets a RED-if-removed test, not just the headline capability.

## Process notes

- No new PF-class entries (the vacuity near-miss was caught pre-merge by the correct mechanism).
- The trunk held two parallel wiki sessions' uncommitted `vault/` changes (which also collide with `origin/main`'s new wiki commits) → the full close was run in a clean worktree off post-merge `main` (the worktree fallback), leaving the parallel work untouched.
- GraphQL exhausted → REST for PR create/merge (full-40-char head-SHA guard).
