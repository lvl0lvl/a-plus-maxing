# ADR-0012 — Apple Health ingestion via the real export.xml: upgrading the HealthKit adapter from scaffold to a streamed, daily-aggregated read

**Status:** Accepted (2026-06-20, S82) — operator-chosen (the operator uses Apple Health, not Whoop, as the first real wearable source).
**Owner:** Walter McGivney
**Relates to:** ADR-0003 (the source-extensible ingestion interface — this upgrades the HealthKit adapter that plugs into its seam; the 0-shared-routine-edit invariant holds), ADR-0011 (the WHOOP adapter — this is the same scaffold→real-format upgrade pattern applied to HealthKit), ADR-0002 (the local-first store — the (item, timepoint, source) dedupe key the adapter inherits), `vault/meta/landmarks.md` LM-02 (the wearable-baseline landmark — Apple Health is now the operator's source).

## Context

ADR-0003 fixed the *architecture* for bringing wearable data in — a pluggable per-source adapter over a common export contract (`source_tag` + `read_readings(export_file)` → store readings), with the shared routine (`ingest.run`) owning the dedupe + the store write. It explicitly named **HealthKit / Apple Watch** as a prepared source. The HealthKit adapter `scripts/ingest/adapters/healthkit.py` existed, but — like the WHOOP adapter before ADR-0011 D2 — it read a **fabricated JSON scaffold** (`[{type, startDate, qty}]`) matching no real Apple Health artifact: it passed `type` straight through as the store item (so the JSON had to already carry item names like `"hrv"`) and did no parsing of Apple's real export.

The operator owns an Apple Watch and uses **Apple Health** (not Whoop) as the wearable aggregator. So bringing the operator's wearable data in is **not a new architectural decision** — the adapter seam, the idempotency contract, and the no-egress constraints are all already fixed by ADR-0003. What this ADR settles is **what the HealthKit adapter reads and how it aggregates it**.

What the real Apple Health export is:
- The Health app exports a **zip** (Health app → profile → *Export All Health Data*) whose `export.xml` holds one `<Record>` element **per raw sample** — `type` = an `HKQuantityTypeIdentifier`, `startDate`/`endDate` = `"YYYY-MM-DD HH:MM:SS -ZZZZ"`, a `value`, a `unit`. The export can be **hundreds of MB** (years of per-second-ish samples).
- The operator owns the file; the read is one-way + read-only (parse only) — the same ADR-0011 license path (the operator exports their own data; no account, no cloud, no API).

## Decision

**Upgrade the HealthKit adapter from the JSON scaffold to read the real `export.xml`**, keeping `source_tag = "healthkit"` and conforming to the frozen ADR-0003-T1 contract. Four sub-decisions:

- **D1 — Streamed read.** Parse `export.xml` with `xml.etree.ElementTree.iterparse`, clearing the parsed tree as it goes (the stdlib memory-safety pattern: hold the root, `root.clear()` after each record), so memory is bounded by the number of distinct (day, item) pairs, not the export size. A missing / non-XML file raises (fail-loud), never silently imports nothing — the same posture as the WHOOP read.
- **D2 — Daily aggregation (the granularity difference from Whoop).** Apple stores RAW per-sample records (dozens of HRV / heart-rate samples a day); the adapter AGGREGATES them to ONE value per (item, day) — the **daily mean**, keyed on the sample's `startDate` calendar date — to match the store's one-reading-per-(item, day, source) key. (Whoop's on-device DB already gives one pre-aggregated row per day, so the WHOOP adapter needed no roll-up; this is the one piece of genuinely new logic.) The stored value is rounded to 2 decimals: the daily mean + the SpO2 scale (below) produce binary-float artifacts (`0.97*100 = 96.9999…`); more precision than these metrics carry is meaningless. A day with no samples of a metric yields no reading (honest absence).
- **D3 — The metric map + the SpO2 scale.** Map only the **value-domain-clean** HK quantity types to the existing store items: `HeartRateVariabilitySDNN`→`hrv` (ms), `RestingHeartRate`→`rhr` (bpm), `RespiratoryRate`→`resp-rate` (breaths/min) carry the store item's unit as-is; `OxygenSaturation`→`spo2` is scaled **×100** (HealthKit stores the 0–1 fraction; the store `spo2` item is a percent, as the WHOOP adapter writes 97.0). An unmapped type yields no reading. `recovery`/`strain` are **not** emitted — Apple Health has no recovery-score or strain equivalent (Whoop-proprietary composites); their absence is honest and consistent with treating wearable readiness composites as non-validated black boxes (the personal-trainer Core-Rule-10 posture).
- **D4 — Coexistence, not replacement.** `source_tag` stays `"healthkit"`, device-specific, so a HealthKit reading and a Whoop reading at the same (item, day) stay distinct under the (item, timepoint, source) dedupe key. **Whoop is NOT disabled.** The operator's "read Apple Health instead of Whoop" is achieved by *providing a HealthKit export and no Whoop export* — the scheduler runs only the adapters it has an export for (`scripts/ingest/scheduler.py`, the `if export_file is not None` skip). Both adapters stay wired; they never collide.

**0-shared-routine-edit invariant (ADR-0003-T2).** The upgrade touches only `healthkit.py` + its tests; `ingest.py`, `adapter.py`, and `scheduler.py` are byte-unchanged (proven by the existing numstat gate in `tests/ingest/test_adapters.py`).

## Deferred (value-domain-grounded, not arbitrary) — a follow-on

Two metrics are deliberately **not** mapped, because mapping them naively would land a wrong-domain value on the wrong stream — the exact class the WHOOP strain-scale guard (ADR-0011) exists to prevent:

- **`skin-temp-dev`** — Apple's `HKQuantityTypeIdentifierAppleSleepingWristTemperature` is an **absolute** °C, but the store `skin-temp-dev` item is a **deviation from baseline** (what the WHOOP `skinTempDevC` writes). Mapping the absolute onto the deviation stream would be 30°C-vs-±0.3°C wrong; deriving the deviation needs a per-operator baseline computation (the Health app's job), out of scope for a file parser.
- **`sleep-efficiency`** — Apple records sleep as `HKCategoryTypeIdentifierSleepAnalysis` stage records (InBed / AsleepCore / Deep / REM / Awake); efficiency = asleep ÷ in-bed needs a stage-duration roll-up with a wake-day attribution convention — a distinct sub-problem from the per-sample-mean quantity metrics.

Both are tracked as a follow-on bead. The SpO2 fraction→percent convention (D3) is a documented assumption to confirm against the operator's first real export (a 1-line scale fix if Apple's export differs); the four mapped metrics are the evidence-supported tier the personal-trainer trusts.

## Consequences

- The operator's real Apple Health export now imports `hrv`/`rhr`/`resp-rate`/`spo2` end-to-end (export.xml → daily-mean readings → the store → the dashboard wearable zone + the specialists, all source-agnostic — they key on the item, not the device).
- The fabricated JSON scaffold is gone; the adapter exercises a real-format read path under the store-adversarial battery (cross-stream, dedupe-idempotent, distinct-days, same-identity-changed-value, distinct-source-from-Whoop, fail-loud).
- Verified on a synthetic `export.xml` fixture; the operator's real export is the production validation (and confirms the SpO2 scale).
