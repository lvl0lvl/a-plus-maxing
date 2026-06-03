# PRD: a-plus-maxing V1 — Local-First Health Tracking & Planning

| Field | Value |
|-------|-------|
| Owner | Walter McGivney |
| Status | Approved |
| Version | 2.0 |
| Date | 2026-06-03 |
| Approved | 2026-06-03 |
| Upstream | design/vision.md |
| Downstream | ADR (next) — see `bd` pipeline-arc beads |
| Last Updated | 2026-06-03 |

## Problem Statement

The primary operator is a single person who wants a local-first tracking-and-planning capability for his health: an operating plan across his health domains (peptides, training, nutrition, sleep, supplements), a place to hold his own data as it accumulates over time, and on-demand dashboards and reports generated from that data — each built from his real numbers and goals, backed by vetted evidence, and shareable with a physician. Today the project can reason about health but produces no assembled plan, holds no time-series record from which to tell whether last month's choices moved anything, and renders no dashboard or report. The reasoning capacity is live — a 20-agent specialist roster, a gated source-grounded wiki, and rigor governance (Finding 1) — but the input schemas for his profile, goals, and current state, while fully scaffolded, hold only placeholder prompts (Finding 2): a complete knowledge layer with no path from it to a plan, no store to accumulate readings into, and no template to render them through.

Two concrete, dated drivers make this acute. The January-2026 health issue still needs recovery and characterization, and the July-2026 first MD visit (Finding 8) is the operator's first physician touchpoint — the first time a plan, a tracked record, and a report are shared and refined with clinical judgment, lab orders, and prescriptions. The desired state is not a one-off handout: it is a capability that ingests device exports and entered labs/food/weight into a local store on a low-friction schedule, renders Whoop-style tracking dashboards, a biomarker matrix, projections, and a doctor report from a consistent pre-designed template set on demand, and runs the lab and watch-out loops that keep the record honest about what bloodwork can and cannot catch.

The system is deliberately operator-agnostic and clonable, not multi-tenant (Finding 9): friends clone the repository and run their own independent, local, single-operator instances — store, ingestion, and generation all local and model-independent, with no committed operator PII and no hosted server. This bounds V1 out of the North Star — the same engine extended into a hosted product for general practitioners managing many patients' regulated data (`design/vision.md`, "The V1 / North-Star boundary"). Without a solution, the engine stays an engine: the operator walks into the July visit with no sourced plan and no tracked trend a time-constrained doctor can act on; each conversation restarts from scratch because nothing accumulates over time; and friends cannot clone it, because there is no operator-agnostic, PII-free starting point to initialize from.

## Goals & Success Metrics

### Goal 1: Produce and share a physician-ready multi-domain operating plan, rendered through a template, at the first physician touchpoint

- **Baseline:** Zero plans exist. No assembled, source-grounded, shareable plan has ever been produced; LM-04 (first HTML artifact) is unstarted.
- **Target:** One multi-domain operating plan (covering all domains present in the operator's goals, each driven by its matching specialist and each bounded by library coverage), built from the operator's profile + goals + current state and rendered through the pre-designed plan/report template, is produced and shared at the July-2026 MD visit. The plan meets all 5 points of the physician-ready bar (sourced, safety-surfaced, honestly uncertain, decision-framed, clinician-legible).
- **Measurement method:** Manual checklist against the 5-point physician-ready bar (`design/vision.md`) applied to the rendered artifact, plus confirmation the artifact was opened/shared at the visit. Per-domain coverage verified against the roster specialist that drove each domain section; template conformance verified against the artifact-design-protocol component set.
- **Attribution window:** By the July-2026 visit date (the LM-01 deadline); evaluated at the visit.

### Goal 2: Accumulate a local time-series record and render tracking dashboards and projections from it on demand

- **Baseline:** Zero. No local time-series store exists; biomarker pages hold a single current value + last-verified date, current-state holds a snapshot, and no dashboard, trend, or projection has ever been rendered.
- **Target:** A local time-series store holds data from at least one import source and at least one manual-entry source, across at least two timepoints for at least one tracked item; and at least one Whoop-style tracking dashboard — showing per-item trend and a projection — is generated on demand from that store through the pre-designed templates before the July visit.
- **Measurement method:** Inspect the store for ≥2 timepoints of ≥1 tracked item sourced from ≥1 import and ≥1 manual entry. Inspect a generated dashboard for: a trend rendered across the stored timepoints (not a single snapshot), a projection rendered for at least one item, and conformance to the template component set. Failure threshold: any dashboard rendering a tracked item as current-only with no historical timepoint, or any item with ≥2 stored timepoints rendering no trend.
- **Attribution window:** First store-and-render cycle completed before the July-2026 visit; evaluated on the generated dashboard.

### Goal 3: Let a second operator initialize a working clone with none of the first operator's data present

- **Baseline:** Not possible today. The repository has no operator-agnostic initialization path; scaffolds hold placeholder prompts, and there is no verified guarantee the trunk carries zero operator PII.
- **Target:** A second operator clones the repository and initializes a working instance — scaffolds present and fillable, store and ingestion and generation operable locally, governance intact — with zero of the first operator's profile, goals, current-state, biomarker, or stored time-series values present anywhere in the clone.
- **Measurement method:** On a fresh clone, run a content scan of all tracked (committed) files for the first operator's PII tokens (name, biomarker values, stored readings, protocol entries); confirm zero hits. Confirm the scaffolds initialize (status `scaffold`, placeholder prompts only) and the operator can begin importing and entering their own local, gitignored data. Failure threshold: any first-operator PII value present in a tracked file on the fresh clone.
- **Attribution window:** Evaluated whenever a second operator first clones (target: a friend test-clones before or around the July-2026 visit window); re-verified on each release.

## User Stories

**US-1:** As the operator, I want to build a multi-domain operating plan from my goals and current data, so that I have concrete regimens (peptides, training, nutrition, and other domains) I can actually run, each driven by its matching specialist.

Acceptance Criteria:
- [ ] The assembled plan contains a distinct section for each in-scope domain present in the operator's goals, each attributable to the roster specialist that produced it.
- [ ] Every domain section is personalized from the operator's profile, goals, and current state — not generic — and reflects at least one operator-specific input (e.g., the January-2026 issue, a hard limit, or a stated goal).
- [ ] Each recommendation in the plan carries its source citation, a confidence tier, and a reversibility note.
- [ ] Where the library lacks coverage for an in-scope domain, the plan states the coverage gap honestly rather than fabricating a recommendation.

**US-2:** As the operator, I want my readings and entries accumulated in a local store over time and surfaced as trends, so that I can tell whether an intervention actually moved a biomarker rather than starting every review from a snapshot.

Acceptance Criteria:
- [ ] A reading imported or entered at one timepoint remains available and comparable when a later reading for the same item is added.
- [ ] For a tracked item with two or more stored timepoints, a generated view shows the value over time, not only the latest value.
- [ ] An item with a single stored timepoint is shown as "no prior" rather than given a fabricated trend.
- [ ] Numbers display with units and reference range.

**US-3:** As the operator, I want to import my device and app exports into the store with a low-friction routine I can run on a schedule, so that my record refreshes without manual re-keying of every reading.

Acceptance Criteria:
- [ ] An export file from a device or app (e.g., a wearable/health export or a CSV) is brought into the store in a single routine, without per-reading manual entry.
- [ ] The same import routine can be run unattended on a schedule and refreshes the store with new readings since the last run.
- [ ] Readings that already exist in the store are not duplicated when the routine runs again.
- [ ] Labs, food, and weight that have no export are entered manually into the same store.

**US-4:** As the operator, I want bloodwork recommendations to flow into a lab loop and results to land in a cross-referenced matrix, so that my doctor orders the right panel and the results are tracked against my interventions over time.

Acceptance Criteria:
- [ ] The plan recommends specific bloodwork tied to the interventions and biomarkers it implies monitoring.
- [ ] Entered lab results appear in a matrix cross-referencing each biomarker across the timepoints it was measured.
- [ ] A biomarker measured at two or more timepoints shows its values side by side in the matrix.
- [ ] A recommended panel the operator has not yet had drawn is shown as pending, not as a result.

**US-5:** As the operator, I want to answer periodic check-in questions about symptoms and contraindications that bloodwork cannot catch, so that the un-measurable watch-outs are tracked alongside my measured data.

Acceptance Criteria:
- [ ] A check-in surfaces questions covering the symptom and contraindication watch-outs the operator's active protocols imply.
- [ ] Answers are stored over time and are available to the next plan generation.
- [ ] A watch-out answer that signals a contraindication or adverse symptom is surfaced in the next generated plan or report.
- [ ] An unanswered check-in is shown as not-yet-answered rather than treated as a clear result.

**US-6:** As the operator, I want to view a Whoop-style tracking dashboard with trends and projections generated on demand, so that I can see where my markers are heading without standing up a live always-on app.

Acceptance Criteria:
- [ ] A dashboard is generated on demand from the store and opens locally as a single self-contained file with no network.
- [ ] The dashboard renders the template component set (KPI cards, sparklines/trends, timelines) over the stored timepoints.
- [ ] At least one projection is rendered for a tracked item, labeled as a projection with its method and confidence stated.
- [ ] The same dashboard can be produced unattended on a schedule.

**US-7:** As the operator, I want to share generated reports with my physician by email or at the visit, so that the July-2026 visit consumes a credible, decision-framed report rather than my walking in with nothing actionable.

Acceptance Criteria:
- [ ] A report renders as a single self-contained file that opens locally with no network and no external assets, suitable to email or print.
- [ ] The report opens with a TL;DR and states explicitly what the operator is doing/considering and the specific asks of the physician.
- [ ] Contraindications, interactions, and the biomarkers they imply monitoring are surfaced up front.
- [ ] The report is print-safe and legible for a time-constrained reader.

**US-8:** As a new operator, I want to clone the repository and initialize my own instance — store, ingestion, and generation — with only my data, so that I can run an independent local capability without inheriting anyone else's private health information.

Acceptance Criteria:
- [ ] A fresh clone contains the engine, scaffolds, templates, ingestion routine, and governance, and zero committed operator PII.
- [ ] The new operator can initialize the store and begin importing and entering their own data locally, with that data excluded from version control.
- [ ] The new operator's instance generates a plan and a dashboard from their own inputs without any dependency on another operator's data.
- [ ] No content from any other operator appears anywhere in the new clone.

**US-9:** As the operator, I want my private data never retained by or used to train the model, with the store and ingestion and generation running locally, so that I can put my real labs, DNA, and health history into the system without it leaking into model training or open-ended retention.

Acceptance Criteria:
- [ ] The store, the ingestion routine, and dashboard/report generation run locally and produce their output without sending operator PII to the model.
- [ ] Only plan reasoning touches the model, and it reasons over summaries rather than raw PII; that dispatch runs on a no-train, non-retained processing path.
- [ ] PII-free library work is separable from PII-bearing personalization and does not require the PII path.
- [ ] No operator PII is written into any committed (tracked) file at any point in producing a plan, dashboard, or report.

## Requirements

### Functional Requirements

**FR-1:** The system assembles a multi-domain operating plan by routing each in-scope domain to its matching specialist in the roster and composing their outputs into one plan.
- **Priority:** Must
- **Traces to:** US-1, Goal 1
- **Acceptance Criteria:**
  - [ ] For each domain named in the operator's goals, the plan contains a section produced by the corresponding specialist.
  - [ ] The assembled plan is a single coherent document, not a set of disconnected specialist outputs.
  - [ ] Each domain section is attributable to the specialist that produced it.

**FR-2:** The system personalizes every domain section from the operator's profile, goals, and current state.
- **Priority:** Must
- **Traces to:** US-1, Goal 1
- **Acceptance Criteria:**
  - [ ] Each section reflects at least one operator-specific input (e.g., the January-2026 issue and its HALT rules, a hard limit, an active protocol, or a stated per-domain goal).
  - [ ] Operator hard limits and HALT rules are honored — no recommendation contradicts a stated hard limit.

**FR-3:** The system maintains a local time-series store that holds imported and manually entered readings (device/app data, labs, food, weight, questionnaire responses) across timepoints, with no hosted backend.
- **Priority:** Must
- **Traces to:** US-2, Goal 2
- **Acceptance Criteria:**
  - [ ] A reading added at one timepoint persists and remains retrievable when later readings for the same item are added.
  - [ ] The store holds at least two timepoints for a tracked item and distinguishes them by time.
  - [ ] The store operates entirely from local files, with no read or write to a shared or hosted service.

**FR-4:** The system refreshes the store through a low-friction import routine that brings device/app exports and CSVs in without per-reading manual entry and can run unattended on a schedule, alongside manual entry for sources that have no export.
- **Priority:** Must
- **Traces to:** US-3, Goal 2
- **Acceptance Criteria:**
  - [ ] An export file is brought into the store in a single routine without per-reading manual entry.
  - [ ] The routine runs unattended on a schedule and adds only readings new since the last run.
  - [ ] Re-running the routine does not duplicate readings already in the store.
  - [ ] Sources without an export (labs, food, weight) are entered manually into the same store.
  - [ ] The import design is source-extensible (pluggable): it is prepared for HealthKit, Apple Watch, Whoop, Garmin, and Oura exports over a common export pattern, with only a subset wired and actionable in the first cut and the remainder pluggable later without reworking the routine.

**FR-5:** The system surfaces honest coverage gaps when the library lacks vetted content for an in-scope domain or claim.
- **Priority:** Must
- **Traces to:** US-1, Goal 1
- **Acceptance Criteria:**
  - [ ] For any in-scope domain the library cannot support, the plan states the gap explicitly rather than producing an unsourced recommendation.
  - [ ] No recommendation appears in the plan without a backing source from the vetted library.

**FR-6:** The system lets a new operator initialize their own instance — store, ingestion, generation, and scaffolds — from the shipped repository with only their own data.
- **Priority:** Must
- **Traces to:** US-8, Goal 3
- **Acceptance Criteria:**
  - [ ] A fresh clone exposes fillable scaffolds and an operable store/ingestion/generation path in their initial (un-filled) state.
  - [ ] The new operator can begin importing and entering their data locally, excluded from version control.
  - [ ] The instance produces a plan and a dashboard from the new operator's inputs alone, with no dependency on any other operator's data.

**FR-7:** The system generates dashboards and reports on demand — and optionally on a schedule — from the store, rendering each into the pre-designed templates as a single self-contained local file, with no live always-on server.
- **Priority:** Must
- **Traces to:** US-6, US-7, Goal 1, Goal 2
- **Acceptance Criteria:**
  - [ ] A dashboard or report is generated on demand and opens locally as one self-contained file with no network.
  - [ ] Generation renders the template component set (KPI cards, sparklines/trends, timelines, comparison tables) over the stored data.
  - [ ] The same generation can be produced unattended on a schedule without a running server.

**FR-8:** The system provides a pre-designed template library that all dashboards and reports render through — Whoop-style tracking screens, a biomarker matrix, projections, and a doctor report — so output is consistent across generations.
- **Priority:** Must
- **Traces to:** US-6, US-7, Goal 1, Goal 2
- **Acceptance Criteria:**
  - [ ] Every generated dashboard and report renders through a template from the library rather than ad-hoc layout.
  - [ ] The V1 template library includes an overview dashboard, a drill-down/detail view, a plan view, a projection view, a biomarker matrix, and a doctor report.
  - [ ] Every template is built from the artifact-protocol component set (KPI cards, sparklines, timelines, comparison tables, TL;DR).
  - [ ] Two generations of the same type produce the same layout and component set.

**FR-9:** The system runs a lab loop: it recommends bloodwork from the plan, accepts entered results, and renders them into a biomarker matrix cross-referenced over time.
- **Priority:** Must
- **Traces to:** US-4, Goal 1, Goal 2
- **Acceptance Criteria:**
  - [ ] The plan recommends specific bloodwork tied to the interventions and the biomarkers they imply monitoring.
  - [ ] Entered results appear in a matrix cross-referencing each biomarker across the timepoints it was measured.
  - [ ] A recommended-but-not-yet-drawn panel is shown as pending, never as a result.

**FR-10:** The system runs a watch-out check-in questionnaire that tracks symptoms and contraindications bloodwork cannot catch, storing answers over time as inputs to the next generation.
- **Priority:** Should
- **Traces to:** US-5, Goal 2
- **Acceptance Criteria:**
  - [ ] A check-in surfaces questions covering the watch-outs the operator's active protocols imply.
  - [ ] Answers are stored over time and made available to the next plan or report.
  - [ ] A watch-out answer signaling a contraindication or adverse symptom is surfaced in the next generation.

**FR-11:** The system renders projections for tracked items into the templates, each labeled as a projection with its method and confidence stated.
- **Priority:** Should
- **Traces to:** US-6, Goal 2
- **Acceptance Criteria:**
  - [ ] At least one tracked item with sufficient stored timepoints has a projection rendered.
  - [ ] The projection is computed by simple trend extrapolation over the stored timepoints — a linear fit or a trailing moving-average slope — not a modeled or clinical forecast.
  - [ ] Each projection is shown with a widening uncertainty band and is labeled "naive projection from recent trend — not a clinical forecast," stating its method and the count of datapoints it was computed from.
  - [ ] Key dates and milestones (July MD visit, landmark dates, protocol start/stop) are marked on the projection's time axis.
  - [ ] A guardrail of at least three stored timepoints is met before any projection renders; an item with fewer is shown with its trend only and no projection, rather than given a fabricated one.

**FR-12:** The system lets the operator capture physician feedback from a visit and carry it into the next generation.
- **Priority:** Could
- **Traces to:** US-7, Goal 1 (post-visit ingestion surface, Finding 10)
- **Acceptance Criteria:**
  - [ ] Physician asks/answers recorded after a visit appear as inputs available to the next plan and report.
  - [ ] The next generation reflects at least one recorded physician input where one exists.

### Non-Functional Requirements

**NFR-1:** Operator private data is never retained by or used to train the model — the store, ingestion, and generation run locally and model-independently, and only plan reasoning touches the model, over summaries rather than raw PII, on a no-train, non-retained processing path.
- **Priority:** Must
- **Traces to:** US-9, Goal 3, and the PII trust-boundary constraint (`design/vision.md`, threat-model B)
- **Acceptance Criteria:**
  - [ ] 0 PII bytes from the store leave the local machine during ingestion or dashboard/report generation.
  - [ ] 100% of plan-reasoning dispatches that touch operator data run on the no-train path over summaries; 0% run on a training-eligible path.
  - [ ] PII-free library work is fully separable and requires 0 use of the PII path.

**NFR-2:** The shipped repository is operator-agnostic — zero committed operator PII, including stored readings, in any tracked file.
- **Priority:** Must
- **Traces to:** US-8, US-9, Goal 3
- **Acceptance Criteria:**
  - [ ] A content scan of all tracked files for operator PII tokens (including stored readings) returns 0 hits on a fresh clone.
  - [ ] All operator data files, including the store, are excluded from version control (0 operator-data files tracked).

**NFR-3:** Each clone is an independent local instance — 0 runtime dependency on any shared service, host, account, or another operator's data, for store, ingestion, and generation alike.
- **Priority:** Must
- **Traces to:** US-8, Goal 3
- **Acceptance Criteria:**
  - [ ] Ingestion and dashboard/report generation complete with 0 network calls to a shared/hosted backend and 0 login.
  - [ ] 0 cross-clone data paths exist (no clone can read another clone's store).

**NFR-4:** Every generated dashboard and report is self-contained, offline, print-safe, accessible, and size-bounded.
- **Priority:** Must
- **Traces to:** US-6, US-7, Goal 1, Goal 2 (artifact-design-protocol, Finding 4)
- **Acceptance Criteria:**
  - [ ] Each generated file is a single file with 0 external asset requests and renders fully with the network disabled.
  - [ ] Each generated file is ≤ 500KB.
  - [ ] Each generated file passes WCAG-AA contrast and is colorblind-safe and print-safe.

**NFR-5:** Every claim in a generated dashboard or report is sourced, and every recommendation carries a confidence tier and a reversibility note.
- **Priority:** Must
- **Traces to:** US-1, US-7, Goal 1 (physician-ready bar, artifact-design-protocol)
- **Acceptance Criteria:**
  - [ ] 100% of recommendations display a source citation, a confidence tier, and a reversibility note.
  - [ ] 100% of numeric values display units and a reference range.
  - [ ] 0 unsourced claims appear in any generated dashboard or report.

**NFR-6:** Animal/in-vitro evidence and population mismatch are flagged wherever a recommendation rests on them.
- **Priority:** Should
- **Traces to:** US-1, US-7, Goal 1 (physician-ready bar point 3; population-mismatch discipline, Finding 11)
- **Acceptance Criteria:**
  - [ ] 100% of recommendations grounded in animal/in-vitro evidence carry an explicit evidence-population flag.

**NFR-7:** All dashboards and reports are produced through the pre-designed template library, and the import routine is low-friction and schedulable, so output stays consistent and the store refreshes without manual re-keying.
- **Priority:** Should
- **Traces to:** US-3, US-6, Goal 2 (artifact-design-protocol components + frequencies, Finding 4/Finding 12)
- **Acceptance Criteria:**
  - [ ] 100% of generated dashboards/reports render through a library template (0 ad-hoc layouts).
  - [ ] A single import routine brings an export into the store in ≤ 1 invocation, with 0 per-reading manual entry for exported sources.
  - [ ] The import routine completes unattended when run on a schedule.

## Non-Goals

- **NG-1:** No multi-tenancy, shared hosting, accounts, or login. Each instance is one local operator; an architect should eliminate any hosted-service, per-account, or shared-database design. (Bounds Goal 3 / US-8.)
- **NG-2:** No regulated-PHI (HIPAA/BAA) trust model. V1's trust boundary is threat-model B (individual no-train API + local PII); designs presupposing a Business Associate Agreement, per-tenant isolation, or HIPAA controls are out of scope. (Bounds Goal 3 / NFR-1.)
- **NG-3:** No cross-operator data sharing, aggregation, or comparison. Each clone is isolated; an architect should eliminate any design that reads, pools, or benchmarks across operators' stores. (Bounds Goal 3 / US-8.)
- **NG-4:** No hosted, live, always-on web application or server. V1 generates dashboards and reports on demand (and optionally on a schedule) as single-file local artifacts; a *local* time-series store IS in scope, but a running web app/server that serves it live is deferred to v2+. (Bounds Goal 2 / FR-7.) **[Reversed from V1.0: a local time-series store is now IN scope; only the hosted/live surface is deferred.]**
- **NG-5:** No native device sync. V1 ingests via import/export routines (device/app exports, CSVs); native live-sync integrations that pull from a device directly are deferred to v2+. (Bounds FR-4.)
- **NG-6:** No automated watch-out tracking. V1's watch-out loop is a check-in questionnaire the operator answers; automated detection of watch-out signals from sensor data is deferred to v2+. (Bounds FR-10.)
- **NG-7:** No doctor login or clinician-facing hosted surface. V1 delivers reports to the physician by email or at the visit as single-file artifacts; a doctor login or hosted report surface is deferred to v2+. (Bounds FR-7 / FR-12.)
- **NG-8:** No complete library before V1. V1 is a thin-library MVP that builds from current vetted content and states coverage gaps honestly; library population runs as a parallel research track and V1 does not block on it. (Bounds Goal 1 / FR-5.)
- **NG-9:** No GP product surface. V1 builds neither a clinician-facing hosted plan/report surface nor the engine extensions the North Star requires; the GP product is architected-for, not built. (Bounds the whole-of-V1 boundary in `design/vision.md`.)
- **NG-10:** No migration of operator data into a hosted store. The local time-series store is additive — it reads the existing scaffolded vault data in place and accumulates new imports/entries beside it locally; it is not a migration of the vault into a separate hosted datastore. (Bounds FR-3.)

## Assumptions, Dependencies & Open Questions

### Assumptions

**A-1:** The operator fills the scaffolded profile/goals/current-state with real values before plan production.
- **Confidence:** High
- **Evidence:** Schemas are complete and `status: scaffold` with placeholder prompts (Finding 2); filling them is a known, owner-controlled action.
- **If wrong:** No personalized plan can be produced; FR-2 and Goal 1 cannot be evaluated.

**A-2:** Device and app data the operator wants tracked is exportable to a file the import routine can read (e.g., a wearable/health export or a CSV), and the import routine is an extensible interface over a common export pattern shared across HealthKit, Apple Watch, Whoop, Garmin, and Oura.
- **Confidence:** Medium
- **Evidence:** current-state.md models a Wearable (Oura) section and LM-02 plans an Oura purchase + 30-day baseline (Finding 12); consumer wearable/health platforms commonly expose file exports over a comparable pattern. Treating import as a pluggable interface over that common pattern (OQ-5 resolved) de-risks any single source: a source not yet wired in the first cut plugs in later without reworking the routine, rather than blocking ingestion. The specific export the operator will use is not yet exercised, so confidence stays Medium.
- **If wrong:** Import-based ingestion narrows to manual entry for that source; FR-4's "without per-reading manual entry" cannot be met for it until that source is wired into the extensible interface.

**A-3:** Template-based generation is sufficient for V1 — a fixed pre-designed template set covers the dashboards, matrix, projections, and report V1 needs, without per-generation bespoke layout.
- **Confidence:** Medium
- **Evidence:** artifact-design-protocol already names the component set (KPI card, sparkline, comparison table, timeline) and artifact types (incl. doctor handout) the templates render (Finding 4); whether that set is complete for V1 is OQ-6.
- **If wrong:** Generation needs bespoke per-artifact layout work; FR-8/NFR-7 consistency target loosens.

**A-4:** V1 projections use simple trend extrapolation over the stored timepoints — a linear fit or trailing moving-average slope — not a modeled forecast. They render with a widening uncertainty band, are labeled "naive projection from recent trend — not a clinical forecast" with method + datapoint count stated, mark key dates/milestones on the time axis, and require ≥3 stored timepoints before rendering (OQ-4 resolved).
- **Confidence:** Medium
- **Evidence:** The locked V1 scope places projections in V1 and the store provides timepoints to extrapolate from (Finding 5/Finding 12); the projection *method* is now fixed (simple trend extrapolation, OQ-4 resolved). The *source* of timepoints remains [INTAKE-DIRECTED] — projections have no codebase surface yet and the data they extrapolate from depends on operator intake. No codebase surface defines a forecasting model, and none is needed.
- **If wrong:** A modeled forecast would need its own evidence and validation; FR-11 method changes. With the method fixed, the residual risk is the source/quantity of stored timepoints, mitigated by the ≥3-timepoint guardrail.

**A-5:** The library grows via parallel research-only sessions and is not a blocker for V1.
- **Confidence:** High
- **Evidence:** Ingestion hardening is DONE (`INV-WIKI-INGESTION-GATED`, S23); specialist-build/research sessions can grow the wiki independently of V1 (Finding 6).
- **If wrong:** V1's plan richness stays minimal; mitigated by FR-5 (honest coverage gaps), so V1 still ships.

**A-6:** A no-train, non-retained processing path for the PII-touching plan-reasoning dispatch will be available for V1 personalization.
- **Confidence:** Medium
- **Evidence:** The trust boundary is decided (threat-model B, `bd show hil`) but not yet built (Finding 7); it is a named dependency, not a guess about feasibility.
- **If wrong:** FR-2/NFR-1 cannot be satisfied for plan reasoning on real PII; this is the highest-risk dependency (see Dependencies + OQ-1). The local store, ingestion, and generation are unaffected, since they run model-independently.

**A-7:** The existing scaffolded vault data layer can be read in place and the local time-series store can accumulate beside it without migrating the vault into a separate store.
- **Confidence:** High
- **Evidence:** Finding 2 + Finding 5 — operator-profile/goals/current-state schemas and the rolling change log already exist in the vault as local files; the store is additive local files.
- **If wrong:** NG-10 would relax and a vault-to-store migration enters V1 scope.

### Dependencies

| Dependent Component | Depends On | Type | Impact if Unavailable |
|--------------------|-----------:|------|----------------------|
| Personalized plan reasoning (FR-2, NFR-1) | The no-train PII routing/guard (`hil`, threat-model B) | Internal | Plan reasoning cannot run on real operator data; Goal 1 and the July-visit deliverable stall until the path exists. Store/ingestion/generation are unaffected (model-independent). |
| Plan domain richness (FR-1, FR-5) | Vetted library content (gated wiki) | Internal | Plans cover fewer domains and lean on FR-5 coverage-gap disclosures; richness is bounded by current wiki content (thin-library MVP). |
| Time-series store + tracking views (FR-3, FR-7, Goal 2) | Scaffolded vault data layer (operator-profile/goals/current-state + rolling change log) read in place | Internal | The store has no existing readings to anchor to; trends cannot render until ≥2 timepoints accumulate. |
| Import-based ingestion (FR-4) | Operator-exportable device/app data (e.g., HealthKit/wearable export, Finding 12) | External | Import narrows to manual entry for that source; FR-4's low-friction criterion fails for it. |
| Generated dashboards/reports (FR-7, FR-8, NFR-4, NFR-5) | Artifact-design-protocol conventions + component set (single-file HTML, KPI/sparkline/timeline/comparison, citation/confidence/reversibility, accessibility) | Internal | Output may not meet the physician-ready bar or render consistent templates; Goal 1/Goal 2 quality criteria fail. |
| Projections (FR-11) | Stored timepoints + a chosen projection method (OQ-4) | Internal | No projection can render until enough timepoints accumulate and a method is fixed. |

### Open Questions

| ID | Question | Blocking? | Owner | Target Date | Impact |
|----|----------|-----------|-------|-------------|--------|
| OQ-1 | What is the concrete shape of the no-train PII path (which plan-reasoning dispatches route to it, how the PII-free/PII-bearing split is enforced)? | No | Walter | 2026-06-30 | Resolved by the `hil` ADR downstream; shapes how NFR-1/FR-2 are realized but does not change the requirement. |
| OQ-2 | What is the operator-facing initialization step for a new clone (how a friend goes from `git clone` to a fillable, PII-free instance with an operable store/ingestion/generation)? | No | Walter | 2026-06-30 | Shapes FR-6's onboarding surface; default is "initialize the store and fill the scaffolds locally," which satisfies Goal 3 regardless. |
| OQ-3 | Which domains beyond peptide/training/nutrition are in scope for the first July plan, given thin-library coverage? | Resolved (2026-06-03) | Walter | — | **Resolved:** All domains in the operator's goals are in scope for the first plan, bounded by library coverage (FR-5). Shapes Goal 1 / FR-1. |
| OQ-4 | What projection method does V1 use (simple trend extrapolation vs. something richer)? | Resolved (2026-06-03) | Walter | — | **Resolved:** Simple linear-fit / trailing moving-average-slope trend extrapolation over stored timepoints, shown with a widening uncertainty band, labeled "naive projection from recent trend — not a clinical forecast" with method + datapoint count, milestones marked on the time axis, and a ≥3-stored-timepoint guardrail before any projection renders. Shapes FR-11 / A-4. |
| OQ-5 | Which import sources are in the first cut (HealthKit/Apple Watch export, sleep/app exports, CSVs)? | Resolved (2026-06-03) | Walter | — | **Resolved:** The import design is source-extensible/pluggable over a common export pattern, prepared for HealthKit, Apple Watch, Whoop, Garmin, and Oura, with only a subset wired/actionable in the first cut and the rest pluggable later. Shapes FR-4 / A-2. |
| OQ-6 | What is the initial template-set scope (which dashboard/matrix/projection/report templates ship in V1)? | Resolved (2026-06-03) | Walter | — | **Resolved:** The V1 template library is an overview dashboard, a drill-down/detail view, a plan view, a projection view, a biomarker matrix, and a doctor report — all built from the artifact-protocol component set (KPI cards, sparklines, timelines, comparison tables, TL;DR). Shapes FR-8. |

## Discovery Evidence

1. **[CODEBASE] The engine exists; the product layer does not.** `.claude/agents/*` holds 20 deployed specialists (confirmed: peptide-specialist, personal-trainer, nutritionist, plus cardiovascular/endocrine/labs/recovery/sleep/etc.); `INVARIANTS.md` and `vault/WIKI.md` confirm the gated wiki and rigor governance are live. Nothing assembles a plan, accumulates a time-series store, renders a dashboard or report, or routes PII. This grounds the Problem Statement and FR-1 (plan assembly routes domains to roster specialists). [Finding 1]

2. **[CODEBASE] The personalization data layer is fully scaffolded, not greenfield.** `vault/meta/operator-profile.md`, `goals.md`, and `current-state.md` (all `status: scaffold`) already define complete schemas: profile (demographics, training, the January-2026 issue section with HALT rules, meds, allergies, DNA, risk posture), goals (north-star, the "Active milestone: July 2026 doctor visit" + objectives + doctor-handout queue, per-domain goals, hard limits), and current-state (latest biomarkers, active protocols/compounds/experiments, rolling change log). They hold placeholder prompts and no real values — filling them is what creates the PII surface. This grounds FR-2 (personalization inputs), FR-3 (store reads this data in place), US-1/US-2, and A-1/A-7. [Finding 2]

3. **[CODEBASE] The doctor report is already a first-class anticipated artifact.** `goals.md` ("Active milestone: July 2026 doctor visit", "Get baseline blood panel ordered", doctor-handout queue) plus `vault/design/artifact-design-protocol.md` (Artifact Types: "Doctor visit handout", audience: Doctor, path `artifacts/doctor-visits/YYYY-MM-DD.html`) corroborate that the July visit is a modeled output and the system already anticipates a queue feeding it. This grounds US-7, FR-7/FR-8 (doctor-report template), FR-9 (lab loop / baseline panel), and Goal 1 (the July touchpoint). [Finding 3]

4. **[CODEBASE] Artifact conventions and the component set are pre-specified — the template + interface NFRs are pre-drafted.** `vault/design/artifact-design-protocol.md` (status: draft) specifies a Components set — **KPI card** (metric + trend arrow + delta vs target), **Sparkline** (30–90d inline trend), **Comparison table** (current vs target vs prior period), **Timeline** (events + labs over time), **Protocol diff**, **TL;DR banner** — and File Conventions: single-file HTML, inline CSS/SVG, no external assets, works offline, <500KB, vanilla; print-safe + WCAG-AA + colorblind-safe; every artifact opens with a TL;DR; every claim cites its source; every recommendation carries confidence + reversibility; numbers carry units + reference range. These map 1:1 to FR-8 (template library = the component set), NFR-4 (self-contained/offline/size/accessible), NFR-5 (sourced/confidence/reversibility/units), and the physician-ready bar. [Finding 4]

5. **[CODEBASE] The data model is point-in-time today — the store is the missing accumulation layer.** `current-state.md` stores latest values + a `trend` field + a rolling 4-week change log, and `vault/biomarkers/*` store a single `Current Value` + `last_verified`; `artifact-design-protocol.md` names sparkline (30–90d) and timeline (events+labs over time) components that want a *time series* the model does not yet hold. The local time-series store (FR-3) is exactly the accumulation layer that turns these point-in-time snapshots into the multi-timepoint series the trend and projection components render. This grounds FR-3 (store), FR-11 (projections need stored timepoints), Goal 2, and A-4/A-7. [Finding 5]

6. **[CODEBASE] The wiki is thin but gated; library population is an unblocked parallel track.** `vault/compounds/` holds only bpc-157 (grandfathered/suspect); `INV-WIKI-INGESTION-GATED` is live (S23) with the ingest gate + hook wired; the ADR-backfill bead is filed (P2). Plan richness is bounded by current content (thin-library MVP), but ingestion hardening is DONE, so library population runs now as separate research-only sessions without blocking V1. This grounds FR-5 (honest coverage gaps), NG-8 (no complete library before V1), A-5, and the library dependency. [Finding 6]

7. **[CODEBASE/DECISION] The PII boundary is decided but unbuilt.** `bd show hil` records threat-model B (individual commercial no-train API; routing + guard architecture, settled in-session). Plan reasoning over real operator data depends on this no-train path existing; the store, ingestion, and generation run locally and model-independently, so they do not. This grounds NFR-1 (PII never retained/trained; store+ingestion+generation local), NFR-2/NFR-3 (operator-agnostic, independent local clones), US-9, A-6, the highest-risk dependency, and OQ-1. [Finding 7]

8. **[CODEBASE] Landmarks frame the timeline, the lab loop, and the device-ingestion source.** `vault/meta/landmarks.md`: LM-01 (July-2026 MD visit) is V1's first physician touchpoint and natural deadline, with trigger windows for baseline-panel/lab-order and a generated MD-handoff artifact — grounding the lab loop (FR-9) and doctor report (US-7); LM-04 (first HTML artifact) is what V1 delivers; LM-02 (Oura ring purchase + first 30-day wearable baseline) is the operator-named wearable that feeds device ingestion. This grounds the Goal attribution windows, FR-9 (lab loop), and FR-4 (import ingestion). [Finding 8]

9. **[SCAFFOLD/INTAKE] Operator-agnostic + clonable distribution, the multi-domain plan, and the local-first tracking layer (2026-06-03 corrected scope, intake.md "Tracking scope CORRECTED").** The intake's corrected scope establishes: the repo ships engine + scaffolds + templates + ingestion + governance with no operator PII; friends clone and run independent local single-operator instances; the deliverable is a multi-domain operating plan (peptides/training/nutrition/etc.) each driven by the matching roster specialist; and a *local* time-series store + import/export ingestion + on-demand-and-cron template generation + lab-results matrix + watch-out questionnaire + projections are all IN v1, with the hosted/live web app, native device sync, automated watch-out tracking, and doctor login deferred to v2+. This grounds US-8 (clone), US-1 (multi-domain plan), US-2/US-3/US-4/US-5/US-6 (store/ingestion/lab/watch-out/dashboard loops), FR-1/FR-3/FR-4/FR-6/FR-7/FR-8/FR-9/FR-10/FR-11, NFR-2/NFR-3/NFR-7, Goal 2/Goal 3, and NG-1 through NG-10. [Intake corrected scope]

10. **[CODEBASE] Post-visit feedback ingestion is a modeled, anticipated surface.** `vault/meta/landmarks.md` LM-01 makes inbound visit-outcome capture a first-class trigger window: "**0–7 days after:** ingest visit outcomes — new prescriptions, lab orders, diagnoses, follow-up schedule" (line 45). `vault/meta/goals.md` makes the same loop a goals-update trigger: "Doctor visit close-outs (goals shift on new diagnosis or all-clear)" (line 23). Together these establish that physician feedback flows back in after a visit and changes the next generation's inputs. This grounds FR-12 (capture physician feedback and carry it into the next generation). [Finding 10]

11. **[CODEBASE] Animal/in-vitro evidence flagging and population-mismatch discipline are governed project invariants.** `INVARIANTS.md` carries `INV-RESEARCH-POPULATION-MISMATCH`: "animal/in-vitro numerical claims tagged … `[population-mismatch: <species>]`", mechanically enforced by the "aplus-research IC-7 verifier (Phase 4.75)". `design/vision.md` "Physician-ready, defined" point 3 requires "animal/in-vitro evidence flagged (population-mismatch discipline)". The discipline is already a load-bearing project rule, not a new ask. This grounds NFR-6 (flag animal/in-vitro evidence and population mismatch wherever a recommendation rests on them). [Finding 11]

12. **[CODEBASE] Artifact frequencies ground scheduled generation; the wearable section grounds device ingestion; the subjective rolling-daily section grounds the watch-out questionnaire.** `vault/design/artifact-design-protocol.md` Artifact Types assign **Daily / Weekly / Monthly / Quarterly** frequencies to its review artifacts — the basis for on-demand-plus-cron-scheduled generation (FR-7, NFR-7). `vault/meta/current-state.md` models a **Wearable (Oura)** section (HRV / RHR / sleep duration / sleep efficiency / body-temp deviation / readiness) — the device/wearable data import ingests (FR-4); the specific **HealthKit/Apple Watch** export named in the locked scope has no codebase surface and is marked **[INTAKE-DIRECTED]**, grounded in this wearable scaffold + LM-02. `current-state.md` also models a **Subjective (daily, last 7-day rolling)** section (Energy / Recovery / Mood / Pain) — the kind of un-measurable, periodically-asked check-in the watch-out questionnaire formalizes (FR-10). **Projections** as a rendered artifact have no codebase surface and are marked **[INTAKE-DIRECTED]**, grounded in the locked V1 scope + the stored timepoints (Finding 5). [Finding 12]
