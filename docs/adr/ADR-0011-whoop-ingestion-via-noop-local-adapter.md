# ADR-0011 — WHOOP wearable ingestion via noop: a local, subscription-free source adapter

**Status:** Accepted (2026-06-14, S60-followup) — operator-ratified
**Owner:** Walter McGivney
**Relates to:** ADR-0003 (source-extensible ingestion interface — this is the WHOOP adapter that plugs into its seam), ADR-0001 (no-train PII trust boundary — ingestion routes no reading through a model step), ADR-0002 (local-first store — the (item, timepoint) dedupe key the adapter inherits), `vault/meta/landmarks.md` LM-02 (the wearable-baseline landmark, re-anchored here Oura→Whoop)

## Context

The operator owns a WHOOP strap and is switching to it from the (never-purchased)
Oura ring. ADR-0003 already decided the *architecture* for bringing wearable data in:
a **pluggable per-source adapter interface over a common export contract**, and it
explicitly names Whoop as one of the prepared sources (HealthKit, Apple Watch, Whoop,
Garmin, Oura), with OQ-1 leaving the first-cut wired subset open [VERIFIED — ADR-0003
Decision + OQ-1]. So WHOOP ingestion is **not** a new architectural decision — the adapter
seam, the idempotency contract (dedupe on the ADR-0002 (item, timepoint) key), the
schedulability contract, and the write-only-to-local-store + no-model-egress constraints
(ADR-0001) are all already fixed. What is undecided is narrower and concrete: **where the
WHOOP adapter reads from**, and the two state changes that follow (the LM-02 device flip
and the biomarker `source` enum).

The forces:
- **Off-cloud + low-budget is the project's spine.** The system is local-first, keeps
  operator PII off the cloud, and is "Bryan Johnson Blueprint-inspired but low-budget"
  [VERIFIED — `vault/meta/overview.md`]. WHOOP's own data access (the WHOOP cloud API, or
  the in-app CSV export) requires an active WHOOP subscription and routes through WHOOP's
  cloud.
- **A community tool removes both dependencies.** `noop` (github.com/NoopApp/noop) is an
  offline WHOOP companion: it pairs **directly with the strap over Bluetooth**, computes
  recovery/strain/HRV/sleep **locally**, stores them in an on-device SQLite DB, uploads
  nothing, and can export CSV [SECONDARY-SOURCE — the noop README]. It is licensed
  PolyForm Noncommercial 1.0.0 [SECONDARY-SOURCE — the noop README].
- **ADR-0003's adapter model is export-based.** Its "common export contract" + idempotency
  + schedulability assume an adapter maps an *export* into the reading shape; "an export
  format changing breaks the adapter" is its standing negative [VERIFIED — ADR-0003
  Consequences]. A live read of another app's internal database is a *different* adapter
  shape than ADR-0003 contemplated.
- **The wiki has 0 biomarker entries today** [VERIFIED — `vault/biomarkers/` holds only
  `_template.md`], so any change to the biomarker `source` enum (`lab|oura|manual|calculation`)
  is a zero-migration change right now.

## Decision

**D1 — Adopt `noop` as the WHOOP local-ingestion layer.** The WHOOP adapter (an instance
of the ADR-0003 interface) sources its data from `noop`, not from WHOOP's cloud API. `noop`
gives subscription-free, fully-local (Bluetooth strap → local store) access with the WHOOP
metrics computed on-device — the only evaluated path that needs neither a WHOOP cloud
account nor an ongoing network dependency, matching the local-first + off-cloud + low-budget
spine and ADR-0001's no-cloud-egress posture.

**D2 — The WHOOP adapter ingests `noop`'s CSV export, not `noop`'s internal SQLite.** A
user-facing CSV export is a stable contract that fits ADR-0003's export-based adapter +
idempotency model directly, and avoids coupling the system to `noop`'s undocumented,
version-volatile internal SQLite schema (a third-party app's internals are not an API). A
**live "local-source" adapter** that reads `noop`'s SQLite for unattended refresh is the
**documented future upgrade**, gated on (a) confirming `noop` exposes a stable/documented
data location and (b) *evidenced* manual-export friction — an evidence-driven deferral, not
a v1 build. Build-time check: confirm `noop`'s CSV export carries the computed
recovery/strain/HRV/RHR/sleep values; if it only re-exports raw samples, fall back to the
raw WHOOP CSV (Alternative A) for the computed metrics.

**D3 — LM-02 re-anchors from Oura to Whoop.** The "first 30-day wearable baseline" landmark
becomes a Whoop baseline. Because the strap is **already owned**, the landmark's
purchase-gate is removed and the baseline can begin now (it no longer waits on a purchase).
Oura is retired as the operator's wearable; it remains a valid (unwired) ADR-0003 adapter
slot, not a wired source.

**D4 — Generalize the biomarker `source` enum from `oura` to `wearable`.** Replace the
device-specific `oura` value in `scripts/wiki-ingest-lint.sh` `check_biomarker` (and the
biomarker template) with a device-agnostic `wearable`; the specific device (Whoop, via noop)
is recorded in the entry body/metadata, not the enum. This matches ADR-0003's multi-wearable,
source-extensible intent and costs zero migration (0 biomarker entries exist).

## Consequences

**Positive:**
- WHOOP data enters the store with **no WHOOP subscription and no cloud round-trip** —
  the off-cloud + low-budget spine is preserved, and ADR-0001's no-egress constraint holds
  trivially (nothing leaves the machine).
- The WHOOP source is **one new ADR-0003 adapter**: it inherits the shared routine, the
  (item, timepoint) dedupe/idempotency, and the store-only-write for free — 0 changes to the
  shared ingestion routine.
- **LM-02 is unblocked now** (Whoop owned), so the 30-day wearable baseline — and the
  `category: wearable` biomarker entries the research plan's Wave 1 names — can start ahead
  of the July 13 visit.
- The CSV-export contract is **testable with a fixture** (a sample noop CSV → expected
  readings), so the adapter is easy to build and pin.

**Negative:**
- **`noop` becomes a required local companion app** the operator runs and maintains — a
  third-party dependency outside the project's control. If `noop` is abandoned or its export
  changes, the WHOOP ingestion breaks. *Mitigation:* the ADR-0003 seam means swapping to a
  raw-WHOOP-CSV adapter (Alternative A) or an Apple-Health adapter (Alternative B) is one
  adapter change, not a routine rewrite.
- **PolyForm Noncommercial license.** `noop` is free for personal + alpha use, but the
  North-Star *commercial* GP product **cannot bundle or depend on `noop`** — a hard v1-vs-
  commercial boundary. The commercial product needs its own WHOOP ingestion (an API/SDK
  partnership, or Apple Health). This ADR is scoped to V1 (personal + alpha) only.
- **The CSV path is not unattended.** A manual export from `noop` breaks ADR-0003's
  schedulability contract *for the WHOOP source specifically* — accepted for v1; the
  deferred live-source (SQLite) adapter restores unattended refresh when justified.
- **`noop`'s CSV export contents are [UNVERIFIED]** (the README confirms a CSV export exists
  but not its exact columns) — D2 carries a build-time confirmation step + the Alternative-A
  fallback.

**Neutral:**
- The `source: wearable` generalization (D4) means the entry body, not the enum, records
  "Whoop via noop" — a small shift of device-identity from schema to content.
- LM-02's relevant_scopes gain a Whoop-derived biomarker set; the old "Oura" naming in
  `current-state.md` / `landmarks.md` is updated as a follow-up (not part of this ADR's
  decision, but its required propagation).

## Alternatives Considered

**Alternative A — Raw WHOOP CSV export (skip `noop`).** The operator exports the official
WHOOP CSV (which carries WHOOP's own computed recovery/strain/HRV/sleep) and the adapter
parses it.
- *Supporting:* No third-party (noop) dependency; the vendor's own export format; the
  computed metrics are guaranteed present.
- *Rejected because:* the WHOOP CSV export requires an active WHOOP **subscription** and the
  WHOOP app/cloud to produce — it keeps the cloud + subscription dependency `noop` exists to
  remove, against the low-budget + off-cloud spine. *Retained as the D2 fallback* if `noop`'s
  CSV proves to lack the computed metrics.

**Alternative B — Apple Health export (WHOOP → HealthKit → `export.xml`).** WHOOP writes a
subset of metrics to Apple Health; the adapter reads the Apple Health export (HealthKit is
already a prepared ADR-0003 source).
- *Supporting:* Apple Health is a stable, documented format; reuses a prepared adapter slot;
  `noop` itself can read it.
- *Rejected as the primary because:* Apple Health does **not** carry WHOOP-proprietary
  recovery/strain (those are WHOOP-computed), so it is insufficient for the WHOOP-specific
  metrics; and it is also a manual export. *Retained as a valid secondary adapter* for the
  HRV/RHR/sleep subset.

**Alternative C — WHOOP cloud API.** OAuth into WHOOP's developer API and pull metrics over
the network.
- *Supporting:* Real-time, unattended, official, complete metrics.
- *Rejected because:* it requires a WHOOP subscription, an OAuth/cloud round-trip, and an
  ongoing network dependency — a direct conflict with the local-first + off-cloud + low-budget
  spine. (It routes no reading through a *model*, so it does not violate ADR-0001 literally,
  but it violates the broader off-cloud posture the system is built on.)

**Alternative D (for D2) — Read `noop`'s internal SQLite live.** The adapter reads `noop`'s
on-device SQLite DB directly, getting frictionless, unattended, computed-metric access.
- *Supporting:* No manual export — satisfies ADR-0003's schedulability contract; gets `noop`'s
  computed scores directly; live/always-current.
- *Deferred (not rejected) because:* it couples the system to `noop`'s **undocumented,
  version-volatile internal schema** (higher break-risk than a user-facing export) and is a
  *different adapter shape* than ADR-0003's export model — so it is the **documented upgrade**
  gated on a confirmed-stable noop data contract + evidenced export friction, not the v1 build.

## Validation Approach

**Confirmation criteria:**
- A `noop` CSV export ingests into the store via **one new WHOOP adapter with 0 edits** to
  the shared ADR-0003 routine, dedupe step, or scheduler (diff the shared routine → 0 lines).
- The WHOOP-derived metrics (HRV, RHR, sleep efficiency, recovery, strain) land as
  `source: wearable` readings on the (item, timepoint) key; the `category: wearable`
  biomarker entries can then render the dashboard readiness data.
- Re-running the adapter over an already-imported export appends **0 duplicate** readings
  (ADR-0002/0003 idempotency inherited).

**Falsification criteria:**
- If wiring the WHOOP adapter requires editing the **shared** routine (≥1 line) → the
  ADR-0003 seam has leaked; fix the boundary before wiring more sources.
- If `noop`'s CSV export **lacks** the computed recovery/strain → D2's source is
  insufficient; switch the adapter to Alternative A (raw WHOOP CSV) and record the change.
- If `noop` cannot pair/sync the strap without a WHOOP subscription after all
  [UNVERIFIED — the README claims direct Bluetooth pairing] → D1's subscription-free premise
  is false; re-evaluate D1 vs Alternative A/C.

**Review triggers:** `noop` releases a breaking export change · the operator drops the WHOOP
subscription (test the subscription-free claim) · the live-source (SQLite) upgrade is
considered (confirm noop's data-location stability first) · the commercial GP product track
begins (the PolyForm-Noncommercial boundary forces a different ingestion).

## Open Questions

| # | Question | Owner | Resolve by | Impact |
|---|----------|-------|-----------|--------|
| OQ-1 | Does `noop`'s CSV export include the computed recovery/strain/HRV/RHR/sleep, or only raw samples? | build session | first WHOOP adapter build | If raw-only, D2 falls back to Alternative A (raw WHOOP CSV). |
| OQ-2 | Is `noop`'s data location (SQLite path / a documented export) stable enough to read live for the unattended upgrade? | deferred | when export-friction is evidenced | Gates the Alternative-D live-source adapter; until then, CSV-export (manual) stands. |

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-06-14 | Initial draft (v1.0) — **Proposed**, awaiting operator ratification | Walter McGivney (drafted by Claude) |
| 2026-06-14 | v1.1 — **Accepted** (operator ratified "ratify it"; the D2 CSV-export recommendation stands; D3/D4 propagation = follow-up build work) | Walter McGivney |
