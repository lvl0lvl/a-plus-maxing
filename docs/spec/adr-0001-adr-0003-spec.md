---
scope: "ADR-0001 ADR-0002 ADR-0003 (foundational data-in layer)"
adrs: [ADR-0001, ADR-0002, ADR-0003]
tier: 3
created: 2026-06-04
status: approved
---

# Spec: Foundational Data-In Layer (PII Trust-Boundary, Local NDJSON Store, Source-Extensible Ingestion)

## Component Overview

This spec delivers the inbound data foundation of the a-plus-maxing V1 system: the mechanism that keeps operator PII off any model and out of every tracked file (ADR-0001, data-in facet), the local append-only NDJSON time-series store that accumulates readings keyed by (item, timepoint) (ADR-0002), and the pluggable per-source ingestion interface that refreshes that store from wearable/app exports and manual entry without duplicating readings (ADR-0003). The deliverable is a set of local Python and shell scripts under `scripts/` operating on `vault/store/*.ndjson` files plus the markdown vault — there is no server, no database engine, and no web framework. Every acceptance criterion is verified against that substrate: `pytest` over store-file operations, a network-egress check that observes 0 outbound calls, a tracked-file / gitignore PII-token scan on a fresh clone, and a `git diff` line-count check on the shared ingestion routine.

These three decisions form the closed inbound trio of the V1 architecture DAG. ADR-0001 (Tier 1) is the sole foundation: it constrains the store (no hosted/egress surface) and ingestion (no raw reading through a model step). ADR-0002 (Tier 2) is built only on that constraint; it fixes the on-disk substrate as gitignored per-item NDJSON. ADR-0003 (Tier 3, the highest in scope) is built on both: it writes only to the local store and derives its dedupe key from the store's (item, timepoint) keying. The trio is "inbound-closed" — once an export or a manual entry lands as a deduped NDJSON line on the local, no-egress side, no further data-in decision is open. The spec hands off to the deferred data-out cut (ADR-0004 generation, ADR-0005 PII-free-trunk gitignore boundary, ADR-0006 plan assembly + the plan-reasoning routing-split enforcement, ADR-0007 lab/symptom flow), which reads the store this spec produces; those decisions and the D4↔D7 render-size tension are recorded as out-of-scope open dependencies in the Unresolved Concerns Disposition table and are not specced here.

Two of ADR-0001's data-in guarantees and ADR-0002's keying scheme were left unresolved by the ADRs and are resolved by the two mandatory prerequisite spikes in this spec. `ADR-0001-T0` designs the mechanically-enforceable data-in PII boundary (network-egress guard, tracked-file PII scan, no-raw-reading-to-model rule) because ADR-0001's negative consequence N2 ("a single mis-routed dispatch sends PII to a training-eligible path, and no enforcement mechanism is built yet") is the unmitigated V1 critical-path risk. `ADR-0002-T0` fixes the per-item file layout, the timepoint key, and the NDJSON line field set in one task, resolving ADR-0002 OQ-1 and ADR-0003 OQ-2 together — they reference each other circularly (the store keying defines the dedupe key; the dedupe key constrains the keying), and extracting the shared keying interface into a single spike breaks the cycle. Both spikes are entry points that block the store-write and ingestion tasks whose PII-boundary and dedupe acceptance criteria consume their output.

Three assumptions from the Proceed dispositions are carried as stated limitations rather than tasks. (1) V1 accepts bounded (non-zero) commercial-API retention for plan reasoning; the exact window is a vendor-facts item Walter resolves out-of-band by 2026-06-30 and no task in this spec depends on the number (the plan-reasoning path itself is the deferred ADR-0006 data-out cut, not this trio). (2) The whole-file-scan scale ceiling is empirical and measured post-build; the documented upgrade path is a SQLite re-ingest of the per-item NDJSON files, and no task gates on a benchmark that no realistic pre-build dataset exists to produce. (3) The first-cut wired adapter set is HealthKit (Apple Watch) + Oura + Garmin, with Whoop pluggable-but-unwired and labs/food/weight entered manually/CSV; adapter code is PII-free and ships in the trunk, while imported readings land only in the gitignored store. These three named adapters give the "add the Nth adapter with 0 shared-routine edits" criterion concrete targets: HealthKit and Oura are wired first, then Garmin is added and the shared routine is diffed to prove 0 lines changed.

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0001 OQ-1 (+ N2 unmitigated risk) | Open Question / Unmitigated Risk | PII enforcement-mechanism shape; split-path complexity is unmitigated and no enforcement is built, so a mis-routed dispatch can send PII to a training-eligible path | Block | Create prerequisite spike `ADR-0001-T0`. It designs the mechanically-enforceable data-in guarantees: a network-egress guard (store read / ingest / generation emit 0 PII bytes off-machine), a tracked-file / gitignore PII-token scan (0 operator-PII tokens in any committed file on a fresh clone), and the no-raw-reading-to-model ingestion rule. Blocks `ADR-0002-T1`, `ADR-0001-T1`, and `ADR-0003-T1`. The plan-reasoning *router* facet (which plan dispatch routes to the no-train path) depends on ADR-0006 and is recorded below as an out-of-scope open dependency. |
| ADR-0001 OQ-2 | Open Question | Exact commercial-API retention window / ZDR availability outside an enterprise tier | Proceed | Documented as a known limitation: V1 accepts bounded (non-zero) retention; the precise window is a vendor-facts item (Anthropic Trust Center / DPA) Walter resolves out-of-band by 2026-06-30. No task in this spec depends on the number; the plan-reasoning path that carries the retention exposure is the deferred ADR-0006 data-out cut, not this data-in trio. |
| ADR-0002 OQ-1 | Open Question | Exact per-item file layout + (item, timepoint) keying + NDJSON line field set | Block | Create prerequisite spike `ADR-0002-T0`. It fixes per-item file granularity (one file per biomarker/wearable-stream vs per-category), the timepoint key (timestamp granularity + source tag), and the NDJSON line field set. Merged with the ADR-0003 OQ-2 dedupe-key concern (next row) into this one task to break their circular reference. Blocks `ADR-0002-T1` and `ADR-0003-T1`. |
| ADR-0002 OQ-2 | Open Question | Stored-row volume at which whole-file scans stop serving the trend/projection read | Proceed | Documented as an accepted scale trade-off: V1 single-operator volumes are small; the per-item NDJSON files are a clean SQLite import source; the review trigger is a measured read regression or file-size growth post-build. No task; no realistic pre-build dataset exists to benchmark against. |
| ADR-0003 OQ-1 | Open Question | First-cut wired source set vs pluggable-but-unwired | Proceed | Documented as a stated assumption (Walter-confirmed): first-cut wired adapters = HealthKit (Apple Watch), Oura, Garmin; Whoop = pluggable-but-unwired; labs/food/weight = manual/CSV. Adapter code is PII-free (ships in the trunk); imported readings land only in the gitignored store. The named set gives `ADR-0003-T2`'s "0 shared-routine edits" criterion concrete targets. |
| ADR-0003 OQ-2 | Open Question | Exact idempotency key field (timestamp granularity, source tag, reading-identity fields) | Block | Resolved by the shared `ADR-0002-T0` keying spike (same decision as the ADR-0002 OQ-1 row). The ingestion-dedupe task `ADR-0003-T1` depends on `ADR-0002-T0` for the finalized key. |
| ADR-0006 (out of scope) | Open Dependency | Plan-reasoning routing-split enforcement (which plan dispatch routes to the no-train path) is the PII-bearing dispatch facet of ADR-0001 OQ-1 | Defer | Out of scope for this data-in trio. ADR-0001 is-prerequisite-of ADR-0006; the router enforcement lives in the deferred data-out cut. Safe to defer: this spec's `ADR-0001-T0` covers the data-in egress + no-committed-PII guarantees that ship before any plan-reasoning path exists. Recorded as an interface point, not specced. |
| ADR-0004 (out of scope) | Open Dependency | Generation (local-only render) and the shared cron/unattended-run seam both read this store and share scheduling with ingestion | Defer | Out of scope; deferred data-out cut. ADR-0002 is-prerequisite-of ADR-0004 (generation reads the store's keyed history); ADR-0003 complements ADR-0004 (shared cron seam). Safe to defer: the read model and scheduler this spec builds are the interface ADR-0004 consumes; no data-out behavior is required for the inbound trio to be complete. |
| ADR-0005 (out of scope) | Open Dependency | The PII-free-trunk gitignore exclusion boundary; ADR-0002 constrains where it is drawn | Defer | Out of scope; deferred data-out cut. ADR-0002 constrains ADR-0005 (store file locations fix the exclusion boundary). Safe to defer: this spec adds the `vault/store/` gitignore entry it needs (`ADR-0002-T1`); the trunk-wide segregation guarantee is ADR-0005's, not this trio's. |
| ADR-0007 (out of scope) | Open Dependency | Lab/symptom data-flow placement; and the D4↔D7 render-size tension (biomarker matrix + projections vs the <500KB artifact budget) | Defer | Out of scope; deferred data-out cut. ADR-0007 depends on ADR-0002/0004/0005 and is constrained by ADR-0001. The D4↔D7 render-size tension lives entirely in the deferred cut (no in-scope ADR participates). Safe to defer: lab values enter this trio's store via the manual-entry fallback (`ADR-0003-T1`); their render-time flow is ADR-0007's. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md` | Create | Spike report fixing the data-in PII-boundary enforcement mechanisms (egress guard, tracked-file PII scan, no-raw-to-model rule) and the follow-up implementation tasks. |
| `docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md` | Create | Spike report fixing the per-item file layout, the (item, timepoint) key, and the NDJSON line field set (resolves ADR-0002 OQ-1 + ADR-0003 OQ-2). |
| `.gitignore` | Modify | Add the `vault/store/` exclusion entry so the operator-reading store is never tracked. |
| `scripts/store/store.py` | Create | NDJSON store library: per-item append (idempotent, dedupe-then-append on the spike key) and read (whole-file scan returning readings in timepoint order). |
| `scripts/store/keying.py` | Create | Shared keying module implementing the (item, timepoint) line key and field set from the `ADR-0002-T0` spike; imported by both store and ingestion so the dedupe key has one definition. |
| `tests/store/test_store.py` | Create | Unit tests for append persistence across timepoints, idempotent re-append, read ordering, and 0-network store operation. |
| `tests/store/test_keying.py` | Create | Unit tests asserting the line key and field set match the spike schema and reject lines missing keying fields. |
| `scripts/guard/egress_guard.py` | Create | Network-egress guard: runs a store/ingest/generation operation under egress capture and asserts 0 outbound calls carrying store content. |
| `scripts/guard/pii_scan.py` | Create | Tracked-file / gitignore PII-token scan over a fresh clone's tracked files, asserting 0 operator-PII tokens and that `vault/store/` is gitignored. |
| `tests/guard/test_egress_guard.py` | Create | Unit/integration tests for the egress guard: passes on a local-only operation, fails on an injected outbound call. |
| `tests/guard/test_pii_scan.py` | Create | Unit/integration tests for the PII scan: 0 hits on a clean tracked tree, ≥1 hit when a PII token is planted in a tracked file. |
| `scripts/ingest/ingest.py` | Create | Shared ingestion routine: runs registered adapters, dedupes once against the store key, writes only to the local store, no model step; carries the manual-entry/CSV fallback path. |
| `scripts/ingest/adapter.py` | Create | Adapter interface (the common export contract) every source adapter implements to map its export into the store reading shape. |
| `scripts/ingest/adapters/healthkit.py` | Create | HealthKit (Apple Watch) adapter mapping the HealthKit export into the store reading shape. |
| `scripts/ingest/adapters/oura.py` | Create | Oura (sleep) adapter mapping the Oura export into the store reading shape. |
| `scripts/ingest/adapters/garmin.py` | Create | Garmin adapter, added after HealthKit + Oura to prove a new source wires with 0 shared-routine edits. |
| `scripts/ingest/adapters/whoop.py` | Create | Whoop adapter scaffold, registered as pluggable-but-unwired (not invoked in the first cut). |
| `scripts/ingest/scheduler.py` | Create | Unattended-run entry point that invokes the shared ingestion routine over wired adapters and appends only readings new since the last run. |
| `tests/ingest/test_ingest.py` | Create | Unit tests for the shared routine: single-invocation import, idempotent re-run (0 duplicate lines), manual-entry/CSV fallback landing in the store, no model step. |
| `tests/ingest/test_adapters.py` | Create | Unit tests for HealthKit/Oura/Garmin adapters mapping a sample export to store readings, plus the 0-shared-routine-edit extensibility check. |
| `tests/ingest/test_scheduler.py` | Create | Unit tests for the unattended run: delta-since-last-run append, completion with no operator interaction, re-run idempotency. |

## Tasks

### ADR-0001-T0: [Spike] Data-In PII-Boundary Enforcement Mechanism

**Status:** TODO
**ADR Source:** ADR-0001, Open Questions (OQ-1); ADR-0001, Consequences — Negative (N2 split-path / mis-routed-dispatch, unmitigated); ADR-0001, Validation Approach (egress + tracked-file-scan confirmation criteria)
**Files to create/modify:**
- `docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md` -- spike report selecting the data-in enforcement mechanisms and listing follow-up implementation tasks

**Acceptance Criteria:**
1. File `docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md` exists and contains the sections "Egress Guard Mechanism", "Tracked-File PII Scan Mechanism", "No-Raw-Reading-To-Model Rule", "Recommendation", and "Follow-up Tasks".
2. The "Egress Guard Mechanism" section names a concrete local mechanism (named tool or technique, e.g. a syscall/socket interceptor or an offline-namespace run) by which a store read, an ingestion run, and a generation run are each observed to emit 0 outbound network calls carrying store content.
3. The "Tracked-File PII Scan Mechanism" section names a concrete token set and a scan command (e.g. `rg`-based) that returns a hit count, and states the pass condition as 0 operator-PII hits across tracked files on a fresh clone.
4. The "No-Raw-Reading-To-Model Rule" section states the rule that ingestion writes only to the local store and routes 0 raw readings through a model step, and names the check that would detect a violation.
5. The "Follow-up Tasks" section names `ADR-0001-T1` (guard implementation) and references `ADR-0002-T1` and `ADR-0003-T1` as the tasks whose PII-boundary acceptance criteria consume the chosen mechanisms.
6. The "Recommendation" section selects exactly one egress-capture mechanism and one PII-scan mechanism (not a list of options) as the build target.

**Risk Mitigations:** ADR-0001 N2 (split-path complexity; a mis-routed dispatch sends PII to a training-eligible path; no enforcement mechanism built yet) — this spike designs the data-in enforcement mechanism that `ADR-0001-T1` then implements, converting N2 from unmitigated to mechanism-backed for the data-in facet. ADR-0001 N1 (bounded retention) — the spike records the data-in egress guarantee that bounds the data-in surface to 0 (retention applies only to the deferred plan-reasoning path).
**Dependencies:** None (entry point). Blocks: ADR-0002-T1, ADR-0001-T1, ADR-0003-T1.

---

### ADR-0002-T0: [Spike] Store Layout + (item, timepoint) Keying Scheme

**Status:** TODO
**ADR Source:** ADR-0002, Open Questions (OQ-1: per-item layout + timepoint key + line field set); ADR-0003, Open Questions (OQ-2: exact idempotency key field); ADR-0002, Decision (one file per item, line keyed by item + timepoint)
**Files to create/modify:**
- `docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md` -- spike report fixing the file granularity, the timepoint key, and the NDJSON line field set

**Acceptance Criteria:**
1. File `docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md` exists and contains the sections "File Granularity", "Timepoint Key", "Line Field Set", "Dedupe Key (ADR-0003 OQ-2)", "Recommendation", and "Follow-up Tasks".
2. The "File Granularity" section states whether the store uses one NDJSON file per biomarker/wearable-stream or one per category, and gives the file-path pattern under `vault/store/`.
3. The "Timepoint Key" section states the timestamp granularity (e.g. ISO-8601 to the second) and the source-tag field, such that two readings for the same item are distinguishable by timepoint.
4. The "Line Field Set" section enumerates the exact JSON field names every store line carries, including the item identifier, the timepoint, the source tag, and the value field(s).
5. The "Dedupe Key (ADR-0003 OQ-2)" section states the field tuple that constitutes a reading's identity for dedupe, and that tuple is a subset of the "Line Field Set" fields (proving the dedupe key fits the line model).
6. The "Recommendation" section selects exactly one layout and one key tuple (not a list of options) as the build target, and the "Follow-up Tasks" section names `ADR-0002-T1` and `ADR-0003-T1` as consumers.

**Risk Mitigations:** ADR-0002 N2 (NDJSON enforces no schema; a malformed line is not rejected by the substrate) — the spike fixes the field set so the keying/validation discipline `ADR-0002-T1` and `ADR-0003-T1` enforce has a definition. ADR-0003 N3 (dedupe key cannot be finalized independently of D2 keying; a later D2-keying change re-opens the dedupe design) — resolving both keys in one spike removes the circular dependency.
**Dependencies:** None (entry point). Blocks: ADR-0002-T1, ADR-0003-T1.

---

### ADR-0002-T1: Local NDJSON Store Append/Read Library + Gitignore Entry

**Status:** TODO
**ADR Source:** ADR-0002, Decision (append-only per-item NDJSON in gitignored `vault/store/`, line keyed by item + timepoint); ADR-0002, Validation Approach (persistence-across-timepoints, multi-timepoint read, 0-network operation, idempotent append)
**Files to create/modify:**
- `scripts/store/keying.py` -- shared keying module implementing the line key and field set from the `ADR-0002-T0` spike
- `scripts/store/store.py` -- append (dedupe-then-append on the spike key) and read (whole-file scan, timepoint order) over per-item NDJSON files
- `.gitignore` -- add the `vault/store/` exclusion entry
- `tests/store/test_keying.py` -- key/field-set conformance and missing-field rejection
- `tests/store/test_store.py` -- persistence, idempotent re-append, read ordering, 0-network operation

**Acceptance Criteria:**
1. After `store.append(item, reading_T1)` then `store.append(item, reading_T2)` for the same item, `store.read(item)` returns ≥2 readings distinguishable by their timepoint field (the T1 reading is still present after the T2 append).
2. `store.read(item)` returns the item's readings as a sequence ordered by timepoint (a caller can render value-over-time, not only the latest), verified by asserting the returned timepoints are non-descending.
3. Re-running `store.append(item, reading_T1)` when `reading_T1` is already stored leaves the item's file line count unchanged (the appended-then-re-appended file has exactly the line count of the distinct readings).
4. The egress check from `ADR-0001-T0` over a `store.append` followed by a `store.read` observes 0 outbound network calls and 0 login step.
5. `store.append` rejects (raises) a reading missing any field in the `ADR-0002-T0` line field set, and the rejected reading produces 0 new lines in the item's file.
6. `.gitignore` contains a `vault/store/` entry, and `git check-ignore vault/store/<any-item>.ndjson` exits 0 (the path is ignored).
7. `pytest tests/store/test_store.py tests/store/test_keying.py` passes.

**Risk Mitigations:** ADR-0002 N2 (no schema; malformed line not rejected by substrate) — criterion 5 puts the field-set validation in this layer (the substrate cannot, so the store library does). ADR-0002 N4 (store gitignored, excluded from VC history) — criterion 6 enforces the gitignore entry so operator readings never reach tracked history; the no-repo-backup consequence is the accepted limitation (Proceed, ADR-0002 OQ-2 row is scale, N4 backup is documented here). Constraint D1→D2 (no hosted/egress surface) — criterion 4.
**Dependencies:** ADR-0001-T0 (egress check mechanism consumed by criterion 4), ADR-0002-T0 (line key + field set consumed by `keying.py` and criterion 5).

---

### ADR-0001-T1: Egress + Tracked-File PII-Scan Guard Implementation

**Status:** TODO
**ADR Source:** ADR-0001, Decision (store/ingestion/generation run local, 0 PII to any model; 0 operator PII in any tracked file); ADR-0001, Validation Approach (egress confirmation, tracked-file PII-scan confirmation)
**Files to create/modify:**
- `scripts/guard/egress_guard.py` -- runs a target operation under the `ADR-0001-T0` egress-capture mechanism and asserts 0 outbound calls carrying store content
- `scripts/guard/pii_scan.py` -- scans a fresh clone's tracked files for the `ADR-0001-T0` PII token set and asserts 0 hits; asserts `vault/store/` is gitignored
- `tests/guard/test_egress_guard.py` -- guard passes on a local-only op, fails on an injected outbound call
- `tests/guard/test_pii_scan.py` -- scan returns 0 on a clean tracked tree, ≥1 on a planted PII token

**Acceptance Criteria:**
1. `egress_guard.run(callable)` returns a pass result (exit 0) when `callable` performs only local file I/O (a synthetic local-only file read defined in the test), and a fail result (non-zero) when `callable` is wrapped to make ≥1 outbound network call.
2. `pii_scan.scan(tracked_files)` returns hit count 0 on the current tracked tree (no operator-PII tokens in any committed file).
3. `pii_scan.scan` returns hit count ≥1 when a test plants an operator-PII token into a tracked file, and the failing path names the offending file.
4. `pii_scan` asserts `git check-ignore vault/store/` exits 0 (the store directory is excluded from version control on the scanned clone).
5. `pytest tests/guard/test_egress_guard.py tests/guard/test_pii_scan.py` passes.

**Risk Mitigations:** ADR-0001 N2 (mis-routed PII / no enforcement built) — criteria 1, 3 implement the mechanically-failing guard that detects a PII egress or a committed-PII token, converting N2 to a covered, test-backed check for the data-in surface.
**Dependencies:** ADR-0001-T0 (egress + PII-scan mechanisms chosen in the spike).

---

### ADR-0003-T1: Shared Ingestion Routine, Adapter Interface, Dedupe + Manual-Entry Fallback

**Status:** TODO
**ADR Source:** ADR-0003, Decision (pluggable per-source adapter interface over a common export contract; idempotency contract keyed off the D2 key; manual-entry fallback; writes only to the local store, no model step); ADR-0003, Validation Approach (single-invocation import, re-run 0 duplicates, manual entry into the same store)
**Files to create/modify:**
- `scripts/ingest/adapter.py` -- the common export-contract interface every adapter implements
- `scripts/ingest/ingest.py` -- shared routine: run registered adapters, dedupe once against the store key (imported from `scripts/store/keying.py`), write only to the local store, no model step; manual-entry / CSV fallback path
- `tests/ingest/test_ingest.py` -- single-invocation import, idempotent re-run, manual-entry/CSV fallback, no-model-step

**Acceptance Criteria:**
1. `ingest.run(adapter, export_file)` brings the export's readings into the store in a single invocation with 0 per-reading manual entry (the store contains the export's readings after one call; the test asserts the imported count equals the export's reading count).
2. Re-running `ingest.run(adapter, export_file)` over an export whose readings are already stored appends 0 duplicate lines (item-file line count unchanged for already-present readings).
3. The dedupe key used by `ingest.run` is imported from `scripts/store/keying.py` (the same module `store.append` uses), verified by asserting `ingest` references no second key definition (`rg "def .*key" scripts/ingest/` returns 0 independent key functions).
4. A manual-entry call (`ingest.manual_entry(item, reading)`) and a CSV-import call (`ingest.import_csv(path)`) each land a reading in the same `vault/store/` files as adapter imports, verified by `store.read` returning the manually-entered reading alongside imported readings.
5. `ingest.run` writes only to `vault/store/` files and invokes no model step — verified by the `ADR-0001-T1` egress guard observing 0 outbound calls over an `ingest.run` invocation, and by `rg` over `scripts/ingest/` finding 0 model/API client calls.
6. An export whose readings carry already-stored timepoints plus new timepoints appends only the new-timepoint readings (the delta), verified by line-count delta equal to the count of new-timepoint readings.
7. `pytest tests/ingest/test_ingest.py` passes.

**Risk Mitigations:** ADR-0003 N3 (dedupe key cannot be finalized independently of D2 keying) — criterion 3 enforces a single shared key module so the ingestion dedupe key fits the store's (item, timepoint) keying (constraint D2→D3). Constraint D1→D3 (no raw reading through a model step; writes only to the local store) — criterion 5. ADR-0002 N2 inherited (no-schema discipline lives in ingestion) — the dedupe/validation runs here against the shared field set.
**Dependencies:** ADR-0002-T0 (finalized dedupe key), ADR-0002-T1 (store append/read + `keying.py`), ADR-0001-T0 (no-raw-to-model rule), ADR-0001-T1 (egress guard applied in criterion 5). The ADR-0001-T1 egress guard is applied to this routine in criterion 5.

---

### ADR-0003-T2: First-Cut Adapters (HealthKit + Oura), Garmin 0-Edit Extensibility Proof, Whoop Stub

**Status:** TODO
**ADR Source:** ADR-0003, Decision (each source is an adapter; a new source plugs in by adding an adapter without reworking the shared routine; first cut wires a subset); ADR-0003, Validation Approach (new source wires with 0 edits to the shared routine — diff = 0 lines); ADR-0003 OQ-1 (wired set: HealthKit + Oura + Garmin; Whoop pluggable-unwired)
**Files to create/modify:**
- `scripts/ingest/adapters/healthkit.py` -- HealthKit (Apple Watch) adapter mapping its export to the store reading shape
- `scripts/ingest/adapters/oura.py` -- Oura adapter mapping its export to the store reading shape
- `scripts/ingest/adapters/garmin.py` -- Garmin adapter added after HealthKit + Oura to prove 0 shared-routine edits
- `scripts/ingest/adapters/whoop.py` -- Whoop adapter scaffold registered pluggable-but-unwired
- `tests/ingest/test_adapters.py` -- per-adapter mapping tests + the 0-shared-routine-edit check

**Acceptance Criteria:**
1. The HealthKit adapter maps a sample HealthKit export into store readings that pass the `ADR-0002-T0` field set, verified by `ingest.run(healthkit_adapter, sample)` then `store.read` returning the mapped readings.
2. The Oura adapter maps a sample Oura export into store readings that pass the field set, verified the same way as criterion 1.
3. After HealthKit and Oura are wired, adding the Garmin adapter changes 0 lines in `scripts/ingest/ingest.py` and `scripts/ingest/adapter.py` (the shared routine + adapter interface) — verified by `git diff --numstat <pre-garmin> -- scripts/ingest/ingest.py scripts/ingest/adapter.py` reporting 0 changed lines.
4. The Garmin adapter, once added, imports a sample Garmin export via the unchanged `ingest.run` and its readings appear in the store (the 0-edit addition is functional, not just non-breaking).
5. The Whoop adapter is present as a registered-but-unwired scaffold: it is importable and not invoked by the first-cut scheduler run (`rg "whoop" scripts/ingest/scheduler.py` returns 0 invocation references).
6. After a simulated export-format field rename, a re-validation re-run of an adapter's sample export re-derives the dedupe key with 0 shared-routine edits (`git diff --numstat` on the shared routine = 0 changed lines).
7. `pytest tests/ingest/test_adapters.py` passes.

**Risk Mitigations:** ADR-0003 N1 (a per-source adapter's export-format change breaks the adapter and can break idempotency-key derivation, silently duplicating/dropping readings) — criterion 6's simulated format-rename re-validation asserts the dedupe key is re-derived with 0 shared-routine edits, the re-validation criterion that fails if a format change breaks idempotency. ADR-0003 N2 (first cut wires only a subset; unwired sources narrow to manual entry) — criterion 5 documents Whoop as the pluggable-unwired case that falls back to manual entry until wired.
**Dependencies:** ADR-0003-T1 (shared routine + adapter interface).

---

### ADR-0003-T3: Unattended Scheduler Run (Delta-Since-Last-Run)

**Status:** TODO
**ADR Source:** ADR-0003, Decision (schedulability contract — the same routine runs unattended on a schedule); ADR-0003, Validation Approach (scheduled unattended run appends only readings new since the last run; re-run appends 0 duplicates)
**Files to create/modify:**
- `scripts/ingest/scheduler.py` -- unattended entry point invoking the shared ingestion routine over wired adapters, appending only readings new since the last run
- `tests/ingest/test_scheduler.py` -- delta-since-last-run append, no-operator-interaction completion, re-run idempotency

**Acceptance Criteria:**
1. `scheduler.run()` invokes `ingest.run` over the wired adapters (HealthKit, Oura, Garmin) and completes with exit 0 and 0 prompts for operator input (no stdin read), verified by running it with stdin closed.
2. After a first `scheduler.run()` imports an export, a second `scheduler.run()` over an export that gained new-timepoint readings appends only the new-timepoint readings (line-count delta equals the new-reading count).
3. A `scheduler.run()` over an export with no new readings since the last run appends 0 lines (idempotent unattended re-run).
4. `scheduler.run()` does not invoke the Whoop (unwired) adapter, verified by asserting Whoop's adapter is absent from the run's invoked-adapter list.
5. The egress guard from `ADR-0001-T1` over a `scheduler.run()` observes 0 outbound network calls.
6. Adding a further wired adapter after the scheduler exists changes 0 lines in `scripts/ingest/scheduler.py` (the scheduler runs a data-driven wired-adapter set, not a hardcoded per-adapter call list), verified by `git diff --numstat <pre-add> -- scripts/ingest/scheduler.py` reporting 0 changed lines.
7. `pytest tests/ingest/test_scheduler.py` passes.

**Risk Mitigations:** ADR-0003 N1 (format-change breaks idempotency) — criteria 2 and 3 assert delta-only and 0-duplicate unattended behavior, which fail if a format change corrupts the dedupe key during an unattended run. Constraint D1→D3 (no egress) — criterion 5.
**Dependencies:** ADR-0003-T1 (shared routine), ADR-0003-T2 (wired adapters the scheduler runs), ADR-0001-T1 (egress guard applied in criterion 5).

---

## Dependency Map

```
ADR-0001-T0 --> ADR-0002-T1   (egress-check mechanism consumed by the store's 0-network criterion)
ADR-0001-T0 --> ADR-0001-T1   (chosen egress + PII-scan mechanisms implemented as the guard)
ADR-0001-T0 --> ADR-0003-T1   (no-raw-reading-to-model rule the ingestion routine enforces)
ADR-0002-T0 --> ADR-0002-T1   (line key + field set the store library implements)
ADR-0002-T0 --> ADR-0003-T1   (finalized dedupe key the ingestion routine dedupes against)
ADR-0002-T1 --> ADR-0003-T1   (store append/read + keying.py the ingestion routine imports)
ADR-0001-T1 --> ADR-0003-T1   (egress guard consumed by the ingestion routine's 0-egress criterion 5)
ADR-0003-T1 --> ADR-0003-T2   (shared routine + adapter interface the adapters implement)
ADR-0003-T1 --> ADR-0003-T3   (shared routine the scheduler invokes)
ADR-0003-T2 --> ADR-0003-T3   (wired adapters the scheduler runs)
ADR-0001-T1 --> ADR-0003-T3   (egress guard consumed by the scheduler run's 0-egress criterion 5)
```

Entry points (no dependencies): ADR-0001-T0, ADR-0002-T0

Topological order (Kahn parallel groups):
1. **Group 1 (parallel — entry points, no dependencies):** ADR-0001-T0, ADR-0002-T0
2. **Group 2 (parallel — each depends only on Group 1):** ADR-0002-T1 (after ADR-0001-T0 + ADR-0002-T0), ADR-0001-T1 (after ADR-0001-T0)
3. **Group 3:** ADR-0003-T1 (after ADR-0001-T0, ADR-0002-T0, ADR-0002-T1, ADR-0001-T1)
4. **Group 4:** ADR-0003-T2 (after ADR-0003-T1)
5. **Group 5:** ADR-0003-T3 (after ADR-0003-T1, ADR-0003-T2, ADR-0001-T1)

Critical path: ADR-0002-T0 → ADR-0002-T1 → ADR-0003-T1 → ADR-0003-T2 → ADR-0003-T3

No cycles (5 groups, every edge points from an earlier group to a later group; Kahn drains all 7 nodes).

**Data flow per edge:**
- `ADR-0001-T0 → ADR-0002-T1`: the chosen egress-capture mechanism (the store's 0-network criterion runs it).
- `ADR-0001-T0 → ADR-0001-T1`: the selected egress + PII-scan mechanisms (implemented as the guard).
- `ADR-0001-T0 → ADR-0003-T1`: the no-raw-reading-to-model rule (the ingestion routine writes only to the store).
- `ADR-0002-T0 → ADR-0002-T1`: the line key + field set (the store library's `keying.py`).
- `ADR-0002-T0 → ADR-0003-T1`: the finalized dedupe key tuple (ingestion dedupes against it).
- `ADR-0002-T1 → ADR-0003-T1`: the `store.append`/`store.read` API + `keying.py` (ingestion imports both).
- `ADR-0001-T1 → ADR-0003-T1`: the egress guard (consumed by ADR-0003-T1 criterion 5, which runs it over an `ingest.run` invocation to observe 0 outbound calls).
- `ADR-0003-T1 → ADR-0003-T2`: the adapter interface + shared routine (adapters implement the interface; the 0-edit proof diffs the routine).
- `ADR-0003-T1 → ADR-0003-T3`: the shared routine entry point (the scheduler invokes `ingest.run`).
- `ADR-0003-T2 → ADR-0003-T3`: the wired adapter set (the scheduler runs HealthKit + Oura + Garmin).
- `ADR-0001-T1 → ADR-0003-T3`: the egress guard (consumed by ADR-0003-T3 criterion 5, which runs it over a `scheduler.run()` invocation to observe 0 outbound calls).

## Test Strategy

### Unit Tests
- **Scope:** `scripts/store/store.py`, `scripts/store/keying.py`, `scripts/ingest/ingest.py`, `scripts/ingest/adapter.py`, `scripts/ingest/adapters/*.py`, `scripts/ingest/scheduler.py`, `scripts/guard/egress_guard.py`, `scripts/guard/pii_scan.py`.
- **Approach:** `pytest` over store-file operations using a temp `vault/store/` fixture directory; sample export fixtures for each adapter; planted-token fixtures for the PII scan; an injected-outbound-call wrapper for the egress guard.
- **Criteria covered:** ADR-0002-T1 criteria 1-3, 5, 7; ADR-0002-T0 criteria 1-6 (spike report content checks); ADR-0001-T0 criteria 1-6 (spike report content checks); ADR-0001-T1 criteria 1-3, 5; ADR-0003-T1 criteria 1-4, 6, 7; ADR-0003-T2 criteria 1-2, 4-5, 7; ADR-0003-T3 criteria 1-4, 7.

### Integration Tests
- **Scope:** the cross-task substrate paths — (a) ingestion routine → store files → read-back; (b) the egress guard wrapped around a full `ingest.run` and a full `scheduler.run`; (c) the gitignore/tracked-file boundary on a fresh clone; (d) the Garmin 0-shared-routine-edit `git diff` proof, the format-rename re-validation 0-edit `git diff` proof, and the scheduler 0-edit `git diff` proof.
- **Approach:** run `ingest.run` / `scheduler.run` end-to-end against the temp store, then assert store contents and run the egress guard over the same invocation; run `git check-ignore` and `git diff --numstat` against a scratch clone/worktree.
- **Criteria covered:** ADR-0002-T1 criteria 4, 6; ADR-0001-T1 criterion 4; ADR-0003-T1 criterion 5; ADR-0003-T2 criteria 3, 6; ADR-0003-T3 criteria 5, 6.

### Risk-Specific Tests
- **ADR-0001 N2 (mis-routed PII / no enforcement):** the egress guard fails on an injected outbound call (ADR-0001-T1 criterion 1) and the PII scan fails on a planted tracked-file token (ADR-0001-T1 criterion 3); the guard over `ingest.run` and `scheduler.run` sees 0 calls (ADR-0003-T1 criterion 5, ADR-0003-T3 criterion 5).
- **ADR-0001 N1 (bounded retention):** the data-in egress guarantee bounds the data-in surface to 0 outbound calls; recorded in the ADR-0001-T0 spike (criteria 2, 6) — retention applies only to the deferred plan-reasoning path.
- **ADR-0002 N2 (no schema):** `store.append` rejects a reading missing a keying field (ADR-0002-T1 criterion 5); ingestion dedupes/validates against the shared field set (ADR-0003-T1 criterion 3).
- **ADR-0002 N4 (store excluded from VC history):** the gitignore entry is enforced (ADR-0002-T1 criterion 6, ADR-0001-T1 criterion 4); the no-repo-backup limitation is documented (Proceed disposition).
- **ADR-0003 N1 (adapter format-change breaks idempotency):** a simulated export-format field rename re-derives the dedupe key with 0 shared-routine edits (ADR-0003-T2 criterion 6), and the unattended delta/0-duplicate checks fail if the key is corrupted (ADR-0003-T3 criteria 2-3).
- **ADR-0003 N2 (subset wired first; unwired narrows to manual entry):** Whoop is a registered-but-unwired scaffold not invoked by the scheduler (ADR-0003-T2 criterion 5, ADR-0003-T3 criterion 4), with labs/food/weight via the manual-entry fallback (ADR-0003-T1 criterion 4).
- **ADR-0003 N3 (dedupe key cannot be finalized independently of D2 keying):** the dedupe key is imported from the single shared `keying.py` (ADR-0003-T1 criterion 3); the `ADR-0002-T0` spike resolves both keys together.

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task (ADR-0001: T0, T1; ADR-0002: T0, T1; ADR-0003: T1, T2, T3)
- [x] All ADR IDs resolve to actual ADR files on disk (ADR-0001/0002/0003 in `docs/adr/`)

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion (each has 6-7)
- [x] All acceptance criteria are binary (pass/fail, no subjective measures) — each cites a command, a file/section condition, or a counted assertion
- [x] No criterion uses words: "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest (files to create/modify)
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in at least one task block
- [x] No task lists a directory instead of a specific file
- [x] Every source file has a corresponding test file (`store.py`/`keying.py`→`test_store.py`/`test_keying.py`; `egress_guard.py`/`pii_scan.py`→`test_egress_guard.py`/`test_pii_scan.py`; `ingest.py`/`adapter.py`→`test_ingest.py`; `adapters/*.py`→`test_adapters.py`; `scheduler.py`→`test_scheduler.py`); `.gitignore` and the two spike `.md` reports need no test file (config / spike-report artifacts, verified by file/section condition checks in their tasks)

### Dependency Map Integrity
- [x] Dependency map has no cycles (Kahn drains all 7 nodes; 5 ordered groups)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed and have Dependencies: "None (entry point)" (ADR-0001-T0, ADR-0002-T0)

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream constraints in their acceptance criteria — D1→D2 (store 0-network: ADR-0002-T1 criterion 4); D1→D3 (ingestion 0 raw-to-model, writes only to store: ADR-0003-T1 criterion 5; ADR-0001-T1 implements the egress guard that ADR-0003-T1 criterion 5 runs); D2→D3 (dedupe key fits the (item, timepoint) keying: ADR-0003-T1 criterion 3)
- [x] Constraint Propagation Table entries have corresponding acceptance criteria in affected tasks (all three in-scope rows mapped above)

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present (10 rows: 6 dispositioned ADR items + 4 out-of-scope deferrals)
- [x] Every open question, pending tension, and unmitigated risk has a disposition (Proceed/Block/Defer)
- [x] Block dispositions have corresponding research spike tasks (ADR-0001 OQ-1→ADR-0001-T0; ADR-0002 OQ-1 + ADR-0003 OQ-2→ADR-0002-T0)
- [x] Defer dispositions have justifications explaining why deferral is safe (each out-of-scope row states the interface point and why this trio is complete without it)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in in-scope ADRs is covered (ADR-0001 N1→T0; N2→T0+T1; N3 plan-reasoning side is out-of-scope ADR-0006, data-in side has no consequence; ADR-0002 N1 scale→Proceed/OQ-2; N2→T0+T1; N3 downstream-reader constraint→D2→D3 criterion in T1; N4→T1 gitignore; ADR-0003 N1→T2+T3; N2→T2; N3→T1)

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (Risk-Specific Tests subsection enumerates ADR-0001 N1/N2, ADR-0002 N2/N4, ADR-0003 N1/N2/N3)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the template exactly (for machine parsing)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")
