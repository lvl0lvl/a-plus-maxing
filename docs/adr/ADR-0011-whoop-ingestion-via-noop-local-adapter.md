# ADR-0011 — WHOOP wearable ingestion via noop: a local, subscription-free source adapter

**Status:** Accepted (2026-06-14, S60-followup) — operator-ratified. **D2 RE-DECIDED 2026-06-14 (S62)** after a first-party review of noop's actual source (the v1 ADR was authored from noop's README only) — operator-ratified ("proceed with your recommendations"). See Revision History.
**Owner:** Walter McGivney
**Relates to:** ADR-0003 (source-extensible ingestion interface — this is the WHOOP adapter that plugs into its seam), ADR-0001 (no-train PII trust boundary — ingestion routes no reading through a model step), ADR-0002 (local-first store — the (item, timepoint) dedupe key the adapter inherits), `vault/meta/landmarks.md` LM-02 (the wearable-baseline landmark, re-anchored here Oura→Whoop)

> **Source-review provenance.** Every noop claim below is now cited against the cloned repository **noop@`a3f5e39`** (`github.com/NoopApp/noop`, reviewed 2026-06-14, S62) — not the README. The v1 of this ADR was authored from the README as a `[SECONDARY-SOURCE]` and its central build decision (the original D2) was wrong as a result; the S62 review (three adversarial agents + orchestrator adjudication against the source) corrected it. The corrected facts and the D2 flip are below; the lineage is in the Revision History.

## Context

The operator owns a WHOOP strap and is switching to it from the (never-purchased)
Oura ring. ADR-0003 already decided the *architecture* for bringing wearable data in:
a **pluggable per-source adapter interface over a common export contract**, and it
explicitly names Whoop as one of the prepared sources (HealthKit, Apple Watch, Whoop,
Garmin, Oura), with OQ-1 leaving the first-cut wired subset open [VERIFIED — ADR-0003
Decision + OQ-1]. So WHOOP ingestion is **not** a new architectural decision — the adapter
seam, the idempotency contract (dedupe on the ADR-0002 (item, timepoint) key), and the
write-only-to-local-store + no-model-egress constraints (ADR-0001) are all already fixed.
What this ADR settles is **where the WHOOP adapter reads from**, and the two state changes
that follow (the LM-02 device flip and the biomarker `source` enum).

What noop actually is [VERIFIED — noop@`a3f5e39`]:
- **A cross-platform, offline WHOOP companion** (macOS + Android full apps; iOS sideload, "newer
  and less battle-tested"). The **mature** platform is **macOS** (`README.md` Platform status;
  `project.yml` `Strand` app target = macOS 13+). It pairs directly with the strap over
  Bluetooth, computes recovery/strain/HRV/sleep **on-device** (`Packages/StrandAnalytics/`),
  and stores everything in a local **SQLite DB via GRDB** (`Packages/WhoopStore/`, a versioned
  migrator). No WHOOP account, no WHOOP cloud, no subscription (`README.md` "no account, no
  cloud, no subscription"; `:168` "never logs into a WHOOP account and never hits a WHOOP server").
- **It ships a first-party, read-only, local-access surface — including an MCP server.**
  `Packages/NoopLocalAccess/` is a public Swift package (`.library(NoopLocalAccessCore)` +
  `.executable(noop-local-access)`) that opens noop's SQLite **read-only** (`config.readonly = true`)
  via a documented `DatabasePathResolver` and exposes a curated JSON API: an **MCP server**
  (`noop-local-access mcp`, MCP protocol `2025-06-18`) with tools `health_snapshot`,
  `metric_series`, `data_freshness`, `sleep_summary`, `workout_summary` (all `readOnlyHint`),
  resources (`noop://health/snapshot`, `noop://metrics/catalog`, `noop://sources`), health-review
  prompts, and a `codex-config` helper that emits ready-to-paste MCP-client registration. It is
  an **announced, opt-in feature** ("a read-only local-access package (MCP) for power users who
  want to query their own on-device NOOP data from local tools — opt-in, nothing leaves the
  device" — `CHANGELOG.md`). **This package is macOS-only** (`Packages/NoopLocalAccess/Package.swift`
  `platforms: [.macOS(.v13)]`). [VERIFIED — noop@`a3f5e39`]
- **Its on-device schema is documented**, not internal-only: `docs/DATA_MODEL.md` (21 KB) details
  every table, column, natural key, index, and the migration history; the DB lives at a fixed,
  resolvable path (`~/Library/.../Application Support/OpenWhoop/whoop.sqlite`). [VERIFIED]
- **noop both imports and exports WHOOP's CSV format.** The README's headline "CSV export" is
  WHOOP's *official* export that noop **imports** (`Packages/StrandImport/WhoopExportImporter.swift`;
  the 4-file bundle `physiological_cycles.csv` / `sleeps.csv` / `workouts.csv` / `journal_entries.csv`).
  noop *also* has its own **"Settings → Backup & restore → Export CSV…"** that re-serializes its
  computed `dailyMetric` rows back into the same WHOOP 4-CSV zip (`Strand/Data/CsvExport.swift`,
  `Packages/StrandImport/WhoopCsvExporter.swift`). That noop export **does** carry the computed
  Recovery/Strain/HRV/RHR/Sleep values (resolves the v1 ADR's OQ-1 = **yes**), but it is lossy: it
  excludes Apple-Health rows, tags on-device-computed days `"noop (APPROXIMATE)"`, down-converts
  Day Strain to WHOOP's 0–21 scale, and the lossless restore path is the `.sqlite` backup. [VERIFIED]

The forces:
- **Off-cloud + low-budget is the project's spine.** Local-first, operator PII off the cloud,
  "Blueprint-inspired but low-budget" [VERIFIED — `vault/meta/overview.md`]. WHOOP's own access
  (cloud API / in-app CSV export) requires an active subscription + the WHOOP cloud. noop removes
  both — verified above.
- **The consumer is an LLM-agent health system on macOS.** a-plus-maxing's reasoning layer is
  Claude, which speaks **MCP natively**, and the operator's machine is a **macOS M2 Studio** — so
  noop's mature macOS app *and* its macOS-only read-only MCP server can co-reside on the one box
  the agent already runs on. This is the single strongest fact for the integration, and the v1 ADR
  missed it.
- **ADR-0003's adapter model is export-file-based**, but it already contemplated a **live
  local-source** adapter variant as the unattended upgrade. noop's read-only access surface
  realizes exactly that variant with a *documented, first-party, read-only* contract — so the
  "different adapter shape" concern is a known, bounded extension, not a seam break. [VERIFIED —
  ADR-0003 Consequences]
- **The wiki has 0 biomarker entries today** [VERIFIED — `vault/biomarkers/` holds only
  `_template.md`], so the biomarker `source` enum change (D4, already propagated S62) was
  zero-migration.
- **Single-device Bluetooth bond (operational cost).** A WHOOP strap holds an encrypted BLE bond
  with **one device at a time**; the computed recovery/strain/sleep require that exclusive bond.
  Pairing the strap to noop takes the bond away from the official WHOOP app (live HR still streams
  to both via the bond-free profile, but deep metrics do not). The operator must **commit the strap
  to noop**. [VERIFIED — `README.md` "Pairing a WHOOP 5.0 / MG"]

## Decision

**D1 — Adopt `noop` as the WHOOP local-ingestion layer.** The WHOOP adapter (an instance of the
ADR-0003 interface) sources its data from `noop`, not from WHOOP's cloud API. `noop` gives
subscription-free, fully-local (Bluetooth strap → on-device SQLite) access with the WHOOP metrics
computed on-device — the only evaluated path needing neither a WHOOP cloud account nor an ongoing
network dependency, matching the local-first + off-cloud + low-budget spine and ADR-0001's
no-cloud-egress posture. [VERIFIED — noop@`a3f5e39`: subscription-free/off-cloud confirmed in source.]

**D2 (RE-DECIDED S62) — The WHOOP adapter consumes noop's first-party, read-only local-access
surface; a manual CSV-import is the documented fallback for bulk history.** The primary path is
noop's **`noop-local-access`** read-only API — its MCP server (the schema-insulated, supported
contract) and/or a direct read-only read of the documented `whoop.sqlite` (per `docs/DATA_MODEL.md`
+ the `DatabasePathResolver` path). This path is **read-only by construction, no-network, unattended
(no manual export step), schema-documented + migration-versioned, and macOS-native** — and it returns
the computed metrics directly (`health_snapshot` / `metric_series` / `sleep_summary` / `data_freshness`).
It **satisfies ADR-0003's schedulability contract** (the thing the original CSV decision broke) and
realizes the "live local-source adapter" the v1 ADR had *deferred*. The manual **CSV export** (noop's
"Export CSV…", or the raw WHOOP CSV of Alternative A) is retained as the **fallback / one-time bulk
backfill** path — it works and carries the computed metrics, but is manual, lossy, and WHOOP-scaled.

  *Why this reverses the v1 D2:* the v1 D2 chose the manual CSV and **deferred** the live read,
  justified by "noop's undocumented, version-volatile internal SQLite schema (a third-party app's
  internals are not an API)." The source refutes that: noop ships a **documented** schema
  (`docs/DATA_MODEL.md`) **and a first-party read-only API + MCP server** purpose-built for external
  tools to read the data. Reading via that surface is *lower* break-risk than scraping a CSV (it is a
  versioned, read-only, fail-closed contract), and it is the natural fit for an MCP-speaking agent on
  the same macOS box. The v1 reasoning was an artifact of reading only the README (which never mentions
  `NoopLocalAccess`).

  *Build mechanism (open, see OQ-2):* a-plus-maxing's ingest layer is Python; `noop-local-access` is a
  Swift macOS binary. The adapter will either (i) subprocess `noop-local-access mcp` and speak MCP
  JSON-RPC over stdio (uses the curated, schema-insulated API), or (ii) read `whoop.sqlite` read-only
  with Python `sqlite3` against the documented `docs/DATA_MODEL.md` schema (simpler, Python-native, but
  couples to the documented schema). Both are first-party-documented, unattended, and **ship no noop
  code inside a-plus-maxing** (the binary/DB are the operator's). The choice is a build-time decision.

**D3 — LM-02 re-anchors from Oura to Whoop.** The "first 30-day wearable baseline" landmark becomes a
Whoop baseline. Because the strap is **already owned**, the purchase-gate is removed and the baseline
can begin once the strap is **bonded to noop** (see the single-device-bond cost). Oura is retired as
the operator's wearable; it remains a valid (unwired) ADR-0003 adapter slot. *(Propagated S62: `vault/meta/landmarks.md` + `current-state.md`.)*

**D4 — Generalize the biomarker `source` enum from `oura` to `wearable`.** The device-specific `oura`
value is replaced with a device-agnostic `wearable`; the specific device (Whoop, via noop) is recorded
in the entry body, not the enum. *(Propagated S62 across `scripts/wiki-ingest-lint.sh`, the biomarker
template, and `vault/WIKI.md`, mutation-proven; the `oura` adapter slot is unaffected.)* **Provenance
refinement:** noop distinguishes WHOOP-*imported* days from noop-*recomputed* (`APPROXIMATE`) days; the
adapter SHOULD carry that into the biomarker `confidence` field (imported → `supported`; noop-computed
→ `provisional`) rather than flattening it.

## Consequences

**Positive:**
- WHOOP data enters the store with **no WHOOP subscription and no cloud round-trip**; ADR-0001's
  no-egress constraint holds trivially (the read-only API is local, no-network by construction).
- **Unattended now (not deferred).** The read-only API/MCP path needs no manual export, so it
  **satisfies** ADR-0003's schedulability contract — the v1 ADR's "WHOOP source breaks schedulability"
  carve-out is no longer needed.
- **Schema-insulated + fail-closed.** The MCP/read-only-store path returns curated JSON and validates
  the DB (rejects a non-noop/un-migrated file), so it is more robust than an ad-hoc CSV parser; the
  `data_freshness` tool directly feeds the dashboard readiness surface for free.
- **LLM-agent-native + license-safe.** MCP is the agent's native protocol, and consuming the
  `noop-local-access` binary as a **separate operator-run process** ships zero noop code in
  a-plus-maxing (see the license analysis).
- **LM-02 unblocked** (Whoop owned) once the strap is bonded to noop — the `category: wearable`
  entries the research plan's Wave 1 names can start ahead of the July 13 visit.

**Negative:**
- **`noop` is a required local companion app** the operator runs + maintains (one-person project). If
  abandoned, ingestion breaks. *Mitigation:* the ADR-0003 seam means swapping to a raw-WHOOP-CSV
  (Alternative A) or Apple-Health (Alternative B) adapter is one adapter change.
- **Single-device BLE bond.** Computing recovery/strain/sleep requires the strap bonded to noop, which
  takes the bond from the official WHOOP app. The operator must commit the strap to noop (and the
  baseline needs ~14 days of offload + several nights to learn). A real adoption cost.
- **Day Strain is on WHOOP's 0–21 scale, not 0–100** [VERIFIED — `WhoopExportImporter.swift`
  `dayStrainToEffortScale = 100.0/21.0`]. The adapter + the `strain` biomarker page MUST record the
  scale (`unit: strain (0–21)`); a 0–100 render is ~5× wrong. (This is exactly the unit-mismatch class
  `docs/checklists/store-adversarial-tests.md` exists to catch.)
- **PolyForm Noncommercial 1.0.0** [VERIFIED — `LICENSE`]. The integration path determines the license
  consequence (the v1 ADR's blanket "cannot bundle or depend on noop" conflated three different paths):
  - **(a) parse a file the operator exports** — no noop code in a-plus-maxing → safe for alpha **and**
    commercial.
  - **(b) link `NoopLocalAccessCore` (the Swift library)** — bundles PolyForm-Noncommercial code →
    OK for personal/alpha V1, **prohibited for the commercial North Star**. **Do not vendor noop into
    the repo.**
  - **(c) talk to the `noop-local-access` MCP server as a separate operator-run process** — interop,
    ships no noop code → same posture as (a).
  V1 uses **(a) or (c)**, never (b). For the commercial GP product, even (a)/(c) only hold if the end
  user's use is non-commercial and they run noop themselves; the durable commercial answer is a WHOOP
  API/Apple-Health path — so **noop is a V1 / personal-alpha dependency only.** (Bundled MIT deps
  GRDB/ZIPFoundation don't change this — the boundary is set by noop's own PolyForm code, which (a)/(c)
  never ship.)
- **The existing `scripts/ingest/adapters/whoop.py` scaffold's assumed format is fabricated** — it
  parses a flat JSON `{metric_name, cycle_start, score}` that matches **no** real noop/WHOOP artifact
  [VERIFIED — no such shape in noop@`a3f5e39`]. It must be rewritten, not extended. The real adapter
  consumes `noop-local-access` JSON (closer to the scaffold's JSON shape than to CSV) or the 4-CSV
  bundle for the fallback. Tracked as a build bead.

**Neutral:**
- The `source: wearable` generalization (D4) records "Whoop via noop" in the entry body, not the enum.
- The mature noop platform (macOS) + macOS-only read API co-reside with the operator's M2 Studio — the
  integration is **not** portable to a Linux/cloud host (acceptable: a-plus-maxing runs on the Mac).

## Alternatives Considered

**Alternative A — Raw WHOOP CSV export (skip `noop`).** The operator exports the official WHOOP CSV.
- *Rejected as primary because:* it requires an active WHOOP **subscription** + the WHOOP cloud — the
  exact dependencies noop removes. *Retained as a fallback/backfill format* (it is byte-identical to
  noop's own export, so one CSV-bundle parser serves both).

**Alternative B — Apple Health export (WHOOP → HealthKit → `export.xml`).**
- *Rejected as primary because:* Apple Health does **not** carry WHOOP-proprietary recovery/strain, and
  it is a manual export. *Retained as a valid secondary adapter* for the HRV/RHR/sleep subset (noop
  itself imports it).

**Alternative C — WHOOP cloud API.** OAuth into WHOOP's developer API.
- *Rejected because:* requires a WHOOP subscription + OAuth/cloud round-trip + ongoing network — a
  direct conflict with the local-first/off-cloud/low-budget spine. (Likely the eventual *commercial*
  path, where the PolyForm boundary rules noop out anyway.)

**Alternative D — Manual CSV export from noop (the v1 D2, now DEMOTED to fallback).** The operator runs
noop's "Export CSV…" and the adapter parses the 4-CSV zip.
- *Supporting:* familiar export-file adapter shape (fits ADR-0003 directly); the export exists and
  carries computed metrics (OQ-1 = yes).
- *Demoted because:* it is **manual** (breaks ADR-0003 schedulability), **lossy** (excludes Apple
  Health, `APPROXIMATE`-tags computed rows, down-scales strain to 0–21), and strictly weaker than the
  read-only API/MCP path it was wrongly preferred over. Kept as the **one-time bulk backfill** + the
  offline fallback if the operator doesn't run the local-access binary.

**Alternative E — Consume noop's read-only `noop-local-access` MCP server / store API (the new D2).**
- *Supporting:* documented, first-party, read-only, no-network, unattended, schema-insulated,
  macOS-native, MCP-agent-native, license-safe as a separate process; exposes the computed metrics +
  `data_freshness` directly.
- *Cost:* a live-source adapter shape (a known ADR-0003 variant, not a seam break); requires the
  operator to run the macOS binary (or a Python read-only SQLite read against the documented schema).
- **Chosen as D2.**

## Validation Approach

**Confirmation criteria:**
- A WHOOP adapter reads via `noop-local-access` (or a read-only `whoop.sqlite` read) into the store with
  **0 edits** to the shared ADR-0003 routine/dedupe/scheduler (diff the shared routine → 0 lines).
- The WHOOP-derived metrics (HRV, RHR, sleep efficiency, recovery, strain[0–21]) land as
  `source: wearable` readings on the (item, timepoint) key with `confidence` reflecting imported vs
  noop-computed; the `category: wearable` biomarker entries render the dashboard readiness data.
- Re-running over an unchanged source appends **0 duplicate** readings (ADR-0002/0003 idempotency).
- Strain is stored/rendered on the 0–21 scale (a fixture pins a 0–21 value through to the store).

**Falsification criteria:**
- If wiring the adapter requires editing the **shared** routine (≥1 line) → the ADR-0003 seam leaked.
- If `noop-local-access` / the documented SQLite read cannot be driven from a-plus-maxing's Python on
  macOS → re-evaluate the mechanism (subprocess-MCP vs read-only-sqlite3) or fall back to the CSV path.
- If `noop` cannot pair/score the strap without a WHOOP subscription → D1's premise is false
  (CONFIRMED false-risk is low: source shows subscription-free pairing). Re-evaluate D1 vs A/C.

**Review triggers:** `noop` releases a breaking schema/API change · the operator drops the strap-to-noop
bond · the commercial GP product track begins (PolyForm boundary forces a different ingestion).

## Open Questions

| # | Question | Owner | Resolve by | Impact |
|---|----------|-------|-----------|--------|
| OQ-1 | ~~Does `noop`'s CSV export include the computed metrics?~~ **RESOLVED (S62) — YES.** noop's "Export CSV…" re-serializes the computed `dailyMetric` (recovery/strain/HRV/RHR/sleep) into the WHOOP 4-CSV shape [VERIFIED — `WhoopCsvExporter.cyclesCSV`]. | — | resolved | — |
| OQ-2 | ~~Is `noop`'s data location stable enough to read live?~~ **RESOLVED (S62) — YES.** Fixed documented path (`~/Library/.../OpenWhoop/whoop.sqlite`, `docs/DATA_MODEL.md` + `DatabasePathResolver`) + a first-party read-only API. **New residual:** which mechanism — subprocess `noop-local-access` MCP vs Python read-only `sqlite3` over the documented schema. | build session | first WHOOP adapter build | Build-time mechanism choice; both are first-party-documented + license-safe. |
| OQ-3 | Does `noop-local-access` expose a non-interactive query mode usable from Python (beyond the MCP stdio loop), or must a-plus-maxing run a minimal MCP stdio client? | build session | first WHOOP adapter build | Shapes the adapter's invocation of noop. |

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-06-14 | Initial draft (v1.0) — **Proposed**, awaiting operator ratification | Walter McGivney (drafted by Claude) |
| 2026-06-14 | v1.1 — **Accepted** (operator ratified "ratify it"; the D2 CSV-export recommendation stands; D3/D4 propagation = follow-up build work) | Walter McGivney |
| 2026-06-14 (S62) | **v2.0 — D2 RE-DECIDED after a first-party noop-source review** (the v1 was authored from the README only). Three adversarial agents compared the ADR against noop@`a3f5e39` + orchestrator adjudication against source. Corrected: noop ships a documented schema (`docs/DATA_MODEL.md`) + a first-party read-only **MCP server** (`NoopLocalAccess`, macOS-only) — so the v1 "undocumented internals" rationale was false; **D2 flips from "manual CSV export" to "consume noop's read-only local-access surface,"** CSV demoted to fallback. Also added: the 0–21 Day-Strain scale, the single-device BLE-bond cost, the license × integration-path (a/b/c) analysis, the macOS platform alignment, the imported-vs-`APPROXIMATE` provenance, and the fabricated-`whoop.py`-scaffold note. OQ-1 + OQ-2 resolved. Operator-ratified ("proceed with your recommendations"). | Walter McGivney (review + drafting by Claude) |
