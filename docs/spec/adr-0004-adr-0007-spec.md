---
scope: "ADR-0004 ADR-0005 ADR-0006 ADR-0007 (data-out cut)"
adrs: [ADR-0004, ADR-0005, ADR-0006, ADR-0007]
tier: 5
created: 2026-06-04
status: approved
---

# Spec: Data-Out Layer (Single-File Artifact Generation, PII-Free Trunk, Multi-Domain Plan Assembly, Lab-Loop / Matrix / Projection Data-Flow)

## Component Overview

This spec delivers the outbound half of the a-plus-maxing V1 system: the path that turns the local store into the two artifacts a human reads. It implements the on-demand (+cron) single-file self-contained HTML generation path (ADR-0004), the operator-agnostic PII-free-trunk distribution and gitignore/content-scan boundary plus the clone-init step (ADR-0005), the multi-domain plan assembly that routes each goal-domain to its deployed roster specialist and composes one attributable document (ADR-0006), and the lab-loop / watch-out / physician-feedback store schemas plus the biomarker-matrix / projection render-time views (ADR-0007). The deliverable is local Python under `scripts/generate/`, `scripts/plan/`, `scripts/store/`, and `scripts/clone/`, a pre-designed HTML template library under `vault/design/templates/` built from the artifact-design-protocol component set, a pre-commit content-scan hook under `.claude/hooks/`, and a `.gitignore` extension — there is no server, no database engine, and no web framework. Every acceptance criterion is verified against that substrate: a network-disabled render check observing 0 outbound asset requests, a rendered-file byte-size check against the spike-measured cap, a tracked-file PII-token scan on a fresh clone, a plan-completeness scan for source/tier/reversibility on every recommendation, and store-state-to-view assertions for the pending / not-yet-answered / no-prior / projection-guardrail states.

These four decisions form the data-out cut of the V1 architecture DAG (Tiers 3-5, dag.md §5). ADR-0004 (Tier 3) is the render foundation of this cut: ADR-0006 (Tier 4) renders the assembled plan through it, and ADR-0007 (Tier 5, the terminal sink) places the matrix/projection as render-time views over it. ADR-0005 (Tier 3) is the orthogonal distribution boundary — it keeps every generated artifact and filled value out of version control. The cut consumes the upstream data-in spec (`docs/spec/adr-0001-adr-0003-spec.md`, status approved) as a fixed interface, not re-specced here: the store append/read API + `scripts/store/keying.py` (item, timepoint) read model from `ADR-0002-T1`, the egress guard + tracked-file PII scan from `ADR-0001-T0` / `ADR-0001-T1`, and the shared ingestion routine from `ADR-0003-T1`. Tasks that read the store, enforce the model-egress boundary, or extend the gitignore boundary reference those data-in tasks via cross-spec dependency notation and author no data-in work.

Two unresolved concerns are dispositioned **Block** and become mandatory prerequisite spikes. `ADR-0004-T0` measures whether a realistic guardrail-passing biomarker-matrix / multi-timepoint projection render fits ADR-0004's <500KB self-contained ceiling (the D4↔D7 tension, dag.md §7 T1) and produces a measured rendered size plus a render cap / pagination parameter; it blocks the ADR-0004 generation task that renders matrix/projection views (`ADR-0004-T2`) and the ADR-0007 matrix/projection render-view task (`ADR-0007-T2`), whose size-budget acceptance criteria consume that cap. `ADR-0006-T0` is the enforcement-first router/summary spike: it fixes which `operator-profile` / `goals` / `current-state` fields the plan-reasoning dispatch reasons over and how the summary is derived from store-read state, and it designs the routing-enforcement mechanism that guarantees the dispatch runs on the no-train summaries lane with 0 raw-PII sends; it blocks every ADR-0006 plan-reasoning / personalization task (`ADR-0006-T1`, `ADR-0006-T2`) — none may reason over operator PII before this router enforcement is specced (here) and built. It is the V1 PII critical-path guard.

**Consequence-citation convention:** this spec cites each ADR's negative consequences by ADR ID plus a short paraphrase of the bullet (the source ADRs render those bullets unlabeled and carry no register IDs). The paraphrase beside each citation is the source of truth and will visibly mismatch if an ADR ever reorders its Negative bullets. The spec invents no `R01`/`N1`-style register IDs.

Four assumptions from the Proceed dispositions (dispositions.md rows 3-6) are carried as stated assumptions plus the implementation tasks named in their rationale, not as open items: (3) the content-scan is enforced by **both** a `.gitignore` exclusion and a pre-commit content-scan hook (`ADR-0005-T1`); (4) a goal-domain with no matching deployed specialist emits a **coverage-gap-by-absence** disclosure, the same shape as a thin-library gap (`ADR-0006-T2`); (5) the clone-init default path is "initialize the store and fill the scaffolds locally," delivered as an init step plus a clone README (`ADR-0005-T2`), the exact form a reversible impl detail; (6) watch-out questions are derived at generation from the operator's active protocols/compounds, with signal-*answering* staying operator-manual per NG-6 (`ADR-0007-T1`). Five accepted-trade-off consequences are documented limitations, not tasks: ADR-0004's no-live-view / stale-snapshot behavior, ADR-0005's no-VC-backup for gitignored data, ADR-0006's thin-library coverage gaps, ADR-0007's projections-absent-early guardrail, and ADR-0007's answer-feeds-next-generation loop latency.

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0004 OQ-1 + ADR-0007 OQ-1 + dag.md §7 T1 | Tension (Pending) | Does a realistic guardrail-passing biomarker-matrix / multi-timepoint projection render fit ADR-0004's <500KB self-contained ceiling? No realistic multi-biomarker dataset exists pre-build, so it is empirical, not assumable. | Block | Create prerequisite measurement spike `ADR-0004-T0`. It builds a realistic multi-biomarker, multi-timepoint dataset, renders the most asset-heavy guardrail-passing matrix + projection view through the inline-SVG / no-chart-library template path, measures the rendered file size against the 500KB ceiling, and produces a cap / pagination parameter. Blocks the ADR-0004 generation task rendering matrix/projection views (`ADR-0004-T2`) and the ADR-0007 render-view task (`ADR-0007-T2`), whose size-budget criteria consume the measured cap. |
| ADR-0006 OQ-2 (+ ADR-0001 OQ cross-ref) | Open Question | Concrete shape of the "summaries" the PII-touching plan dispatch reasons over (which profile/goals/current-state fields, how derived) on the no-train lane, plus the PII-free-vs-PII-bearing routing enforcement. | Block | Create prerequisite enforcement-first spike `ADR-0006-T0`. It defines the summary field-set + derivation from store-read state AND the routing-enforcement mechanism guaranteeing the dispatch runs on the no-train summaries lane with 0 raw-PII sends (building on the data-in egress guard, cross-spec `ADR-0001-T0`/`ADR-0001-T1`). Blocks every ADR-0006 plan-reasoning / personalization task (`ADR-0006-T1`, `ADR-0006-T2`); none may reason over operator PII before this router enforcement is built. V1 PII critical-path guard. |
| ADR-0005 OQ-1 | Open Question | Content-scan enforcement mechanism — pre-commit scan hook, `.gitignore`, or both. | Proceed | Assumption: enforce by **both** — `.gitignore` excludes `vault/store/` + every filled-scaffold value, and a pre-commit content-scan hook over tracked files (mirrors the existing `block-ungated-vault-write.sh` / `block-commit-main.sh` PreToolUse pattern + the `wiki-ingest-lint.sh` battery). Specced as the first-group ADR-0005 task `ADR-0005-T1`, whose criteria mitigate ADR-0005's discipline-burden + no-mechanism/gitignore-gap negative consequences. |
| ADR-0006 OQ-1 | Open Question | No-matching-specialist routing — queue a build, coverage-gap-by-absence, or exclude. | Proceed | Assumption: a goal-domain with no matching deployed roster specialist emits a **coverage-gap-by-absence** disclosure (same shape as a thin-library gap), not a fabricated regimen and not a silent drop. `ADR-0006-T2`'s criteria assert the no-specialist case renders a stated gap. |
| ADR-0005 OQ-2 | Open Question | Clone-init step — init script, README, or both. | Proceed | Assumption: default path = "initialize the store and fill the scaffolds locally," delivered as an init step + a clone README (`ADR-0005-T2`); exact form a reversible impl detail. Criteria assert a fresh clone reaches a fillable PII-free instance. |
| ADR-0007 OQ-2 | Open Question | Watch-out question generation, given NG-6 forbids automated signal detection. | Proceed | Assumption: watch-out questions are derived at generation from the operator's active protocols/compounds (the watch-outs they imply); signal-*answering* stays operator-manual per NG-6. `ADR-0007-T1`'s criteria cover question derivation without automating signal detection. |
| ADR-0001 / ADR-0002 / ADR-0003 (upstream, out of scope) | Open Dependency | The store append/read + `keying.py` read model, the egress guard + tracked-file PII scan, and the shared ingestion routine are consumed as the data-in interface. | Defer | Out of scope — authored in the approved data-in spec (`docs/spec/adr-0001-adr-0003-spec.md`). This cut consumes `ADR-0002-T1` (store read model), `ADR-0001-T1` (egress + PII-scan guard), `ADR-0001-T0` (mechanism), and `ADR-0003-T1` (ingestion fallback) via cross-spec dependency notation and authors no data-in task. Safe to defer: those tasks ship in the upstream spec before this cut runs. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md` | Create | Spike report: measured rendered size of the most asset-heavy guardrail-passing matrix+projection render vs the 500KB ceiling, plus the cap / pagination parameter the downstream render tasks consume. |
| `docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md` | Create | Spike report: the plan-reasoning summary field-set + derivation from store-read state, the no-train routing-enforcement design, and its falsifiable check. |
| `vault/design/templates/component_set.py` | Create | The pre-designed template component library (inline-CSS/SVG components from the artifact-design-protocol set) shared by dashboard, report, plan, matrix, and projection renders. |
| `vault/design/templates/dashboard.py` | Create | Dashboard template assembling the component set into the tracking-dashboard artifact. |
| `vault/design/templates/report.py` | Create | Physician-ready report template assembling the component set into the report artifact. |
| `scripts/generate/render.py` | Create | Generation engine: reads the store via the data-in read model and emits one self-contained HTML file (inline CSS/SVG, 0 external asset requests, <500KB) through a named template. |
| `scripts/generate/generate.py` | Create | On-demand + unattended (cron) entry point that produces a named artifact file and exits with no server process. |
| `scripts/generate/render_views.py` | Create | Render-time view builders for the biomarker matrix and projections over stored timepoints (pending / not-yet-answered / no-prior states, the ≥3-timepoint projection guardrail, the cap from `ADR-0004-T0`). |
| `scripts/plan/assemble.py` | Create | Plan-assembly orchestrator: routes each in-scope goal-domain to its roster specialist, composes outputs into one attributable document, attaches source/tier/reversibility, flags population-mismatch, emits coverage-gap disclosures. |
| `scripts/plan/router.py` | Create | Routing + no-train summary enforcement: derives the summary from store-read state per the `ADR-0006-T0` field-set and routes the plan-reasoning dispatch to the no-train lane (0 raw-PII sends). |
| `scripts/store/loop_schema.py` | Create | Store schemas for the lab loop (pending panels), watch-out answers (with question derivation), and physician feedback — pending / not-yet-answered / no-prior / answered-over-time state on the data-in store. |
| `scripts/clone/init_instance.py` | Create | Clone-init step: initializes the store and surfaces the empty scaffolds so a fresh clone reaches a fillable PII-free instance; entered data lands untracked. |
| `.claude/hooks/block-pii-commit.sh` | Create | Pre-commit content-scan hook over tracked files (mirrors `block-commit-main.sh`); blocks a commit when a filled-scaffold value or store file is staged or a PII token appears in a tracked file. |
| `docs/clone-init.md` | Create | Operator-facing clone README: the `git clone` → fillable PII-free instance path (the FR-6 / US-8 onboarding surface). |
| `.gitignore` | Modify | Add filled-scaffold-value exclusions to the existing `vault/store/` boundary so no filled scaffold is tracked. |
| `tests/generate/test_render.py` | Create | Unit/integration tests: single self-contained file, 0 external asset requests with network disabled, <500KB against the cap, WCAG-AA/colorblind/print-safe, identical structure across two same-type generations. |
| `tests/generate/test_generate.py` | Create | Tests for the on-demand + cron entry point: file produced, 0 server process, stdin-closed unattended run. |
| `tests/generate/test_render_views.py` | Create | Tests for matrix/projection views: ≥2-timepoint matrix side-by-side, ≥3-timepoint projection with full label/method/count/band/milestones, exactly-2 trend-only, pending/not-yet-answered/no-prior states, 0 external requests + 0 PII to model. |
| `tests/plan/test_assemble.py` | Create | Tests for plan assembly: one attributable section per in-scope domain, source/tier/reversibility on every recommendation, population-mismatch flag, coverage-gap (thin-library + no-specialist), composition-attribution integrity. |
| `tests/plan/test_router.py` | Create | Tests for routing/summary enforcement: dispatch routes to the no-train lane, summary carries only the `ADR-0006-T0` field-set, 0 raw-PII sends, fails on an injected raw-PII send. |
| `tests/store/test_loop_schema.py` | Create | Tests for the loop schemas: pending panel persists across generations, watch-out answer read on next generation, physician feedback carried forward, question derivation, store-schema-vs-render-view integration. |
| `tests/clone/test_init_instance.py` | Create | Tests for clone-init: fresh clone reaches a fillable PII-free instance, entered data lands untracked, instance generates a plan + dashboard from local inputs alone with 0 cross-clone paths. |
| `tests/hooks/test_block_pii_commit.sh` | Create | Tests for the pre-commit hook: 0 hits on a clean staged tree passes; a staged filled-scaffold value or planted PII token in a tracked file blocks the commit. |

## Tasks

### ADR-0004-T0: [Spike] D4↔D7 Render-Size Measurement + Cap Parameter

**Status:** TODO
**ADR Source:** ADR-0004, Open Questions (OQ-1: realistic matrix/projection render vs the <500KB ceiling); ADR-0004, Consequences — Negative (the <500KB budget caps render richness; inline-everything per-file size pressure over 1+ yr); ADR-0007, Open Questions (OQ-1: same tension, ADR-0007 side); dag.md §7 T1
**Files to create/modify:**
- `docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md` -- spike report with the measured render size, the over-budget mitigation, and the cap / pagination parameter the downstream render tasks consume

**Acceptance Criteria:**
1. File `docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md` exists and contains the sections "Dataset", "Render Method", "Measured Size", "Mitigation If Over Budget", "Cap / Pagination Parameter", and "Follow-up Tasks".
2. The "Dataset" section states a realistic multi-biomarker, multi-timepoint dataset: it names a biomarker count of at least 8 and a per-biomarker timepoint count of at least 3, so at least one projection passes the ≥3-timepoint guardrail and the matrix carries multiple series.
3. The "Render Method" section states the render goes through the inline-SVG / no-chart-library template path and produces one self-contained HTML file with 0 external asset references.
4. The "Measured Size" section reports the rendered file's byte size as a number and states whether it is under or over the 500KB (500000-byte) ceiling (the measurement is a recorded number, not "fits" / "does not fit").
5. The "Cap / Pagination Parameter" section states an explicit cap value — a maximum rendered-timepoints-per-view number and a maximum series-per-view number, or a pagination/split rule — that keeps a worst-case downstream view under 500000 bytes; the value is a number or a stated rule, not "as needed".
6. The "Follow-up Tasks" section names `ADR-0004-T2` and `ADR-0007-T2` as the tasks whose size-budget acceptance criteria consume the cap parameter.
7. The "Mitigation If Over Budget" section selects exactly one concrete mitigation to apply if the measured size exceeds 500000 bytes (cap rendered timepoints/series, paginate/split the matrix across artifacts, or share component-set markup across views), not a list of options.

**Risk Mitigations:** ADR-0004 Negative (the <500KB / self-contained budget caps interactivity and render-richness — inline SVG, no chart library) and ADR-0004 Negative (inline-everything raises per-file size pressure as a 1+ yr constraint, may need capping/pagination) — this spike measures the worst-case render and produces the cap that bounds it. ADR-0007 Negative (matrix/projection views are the artifacts most likely to strain the <500KB budget) — same measurement, ADR-0007 side.
**Dependencies:** None (entry point). Blocks: ADR-0004-T2, ADR-0007-T2.

---

### ADR-0006-T0: [Spike] Plan-Reasoning Summary Contract + No-Train Router Enforcement

**Status:** TODO
**ADR Source:** ADR-0006, Open Questions (OQ-2: the shape of the summaries the plan dispatch reasons over); ADR-0006, Decision (plan reasoning runs on the no-train path over summaries, reads current state from the store); ADR-0006, Consequences — Negative (plan reasoning is the one PII-touching dispatch, constrained by the no-train summaries path + the store read model)
**Files to create/modify:**
- `docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md` -- spike report with the summary field-set + derivation, the routing-enforcement design, and its falsifiable check

**Acceptance Criteria:**
1. File `docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md` exists and contains the sections "Summary Field-Set", "Summary Derivation", "Routing-Enforcement Mechanism", "Falsifiable Check", "Recommendation", and "Follow-up Tasks".
2. The "Summary Field-Set" section enumerates the exact `operator-profile` / `goals` / `current-state` fields the summary carries (a named field list, not "relevant fields"), and states which raw-PII fields are excluded from the summary.
3. The "Summary Derivation" section states how the summary is derived from store-read state: it names the data-in store read model (`scripts/store/store.py` / `scripts/store/keying.py`) as the read source and states the transformation from raw field to summary token.
4. The "Routing-Enforcement Mechanism" section names a concrete mechanism (building on the data-in egress guard `scripts/guard/egress_guard.py`) that routes the plan-reasoning dispatch to the no-train lane and that fails a dispatch carrying a raw-PII field absent from the Summary Field-Set.
5. The "Falsifiable Check" section states a check that returns a pass/fail result and fails when a raw-PII field (one excluded by criterion 2) appears in a model-bound dispatch.
6. The "Recommendation" section selects exactly one routing-enforcement mechanism (not a list) as the build target, and the "Follow-up Tasks" section names `ADR-0006-T1` (router implementation) and `ADR-0006-T2` (assembly) as the consumers.

**Risk Mitigations:** ADR-0006 Negative (plan reasoning is the one PII-touching dispatch; constrained by the no-train summaries path and the store read model, narrowing the model's input) — this spike fixes the summary contract and the routing-enforcement mechanism that `ADR-0006-T1` implements, so the dispatch cannot reason over raw PII. Constraint D1→ADR-0006 (no-train summaries) — the spike's falsifiable check is the basis of the 0-raw-PII criterion the downstream tasks carry.
**Dependencies:** None (entry point). Cross-spec: builds on `ADR-0001-T0` (egress mechanism) and `ADR-0001-T1` (egress guard) from `docs/spec/adr-0001-adr-0003-spec.md`. Blocks: ADR-0006-T1, ADR-0006-T2.

---

### ADR-0004-T1: Generation Engine + Template Component Library (Dashboard + Report)

**Status:** TODO
**ADR Source:** ADR-0004, Decision (read the store, render through a pre-designed template library into one self-contained local HTML file, inline CSS/SVG, 0 external asset requests, <500KB, offline, WCAG-AA, colorblind-safe, print-safe); ADR-0004, Validation Approach (single-file/offline render, size+accessibility, two-generation structural identity)
**Files to create/modify:**
- `vault/design/templates/component_set.py` -- the inline-CSS/SVG component library from the artifact-design-protocol set, shared across artifacts
- `vault/design/templates/dashboard.py` -- dashboard template assembling the component set
- `vault/design/templates/report.py` -- physician-ready report template assembling the component set
- `scripts/generate/render.py` -- generation engine: reads the store via the data-in read model, renders a named template to one self-contained HTML file with everything inlined
- `tests/generate/test_render.py` -- single-file, 0-external-request (network disabled), <500KB, WCAG-AA/colorblind/print-safe, two-generation structural identity

**Acceptance Criteria:**
1. `render.emit(template, store_read)` writes one HTML file whose external-asset reference count is 0 (`rg` over the file for `src=`/`href=`/`url(` pointing at any non-`data:`, non-fragment URL returns 0), and the file renders with the network disabled (an offline open observes 0 outbound requests).
2. The emitted dashboard file and the emitted report file are each strictly less than 500000 bytes (`wc -c` < 500000), measured on a fixture store read.
3. The emitted file passes a WCAG-AA contrast check, a colorblind-safe palette check, and a print-safe check (the test runs a contrast checker over the file's inline styles asserting AA-level pass; asserts every series/category color in the rendered output is a member of the artifact-design-protocol colorblind-safe semantic palette — the good/watch/concern set, never red-only — and that any two colors used for adjacent series stay above a stated deuteranopia/protanopia color-distance threshold under a simulated color-vision transform; and asserts an `@media print` stylesheet block is present).
4. Generating the same artifact type twice from the same store read produces byte-identical template/component structure (a structural diff of the two outputs with data values masked returns 0 differences).
5. `render.emit` reads only the store via the data-in read model (`scripts/store/store.py`) and fetches no remote data or asset — verified by the cross-spec egress guard (`scripts/guard/egress_guard.py`) over an `emit` call observing 0 outbound calls (D1→ADR-0004 PII no-egress at render: 0 PII egress at render).
6. `render.emit` raises when a referenced asset would resolve to an external URL (the engine refuses to emit a file with a non-inlined asset rather than emitting a network-dependent file).
7. `pytest tests/generate/test_render.py` passes.

**Risk Mitigations:** ADR-0004 Negative (generation is constrained by the store read model + the PII no-egress boundary — no freedom to fetch remote data or assets) — criteria 5, 6 enforce store-only reads and refuse external assets. Constraint D1→ADR-0004 (PII no-egress at render) — criteria 1, 5.
**Dependencies:** Cross-spec: `ADR-0002-T1` (store append/read + `keying.py` read model) and `ADR-0001-T1` (egress guard) from `docs/spec/adr-0001-adr-0003-spec.md`. No in-spec predecessor (entry point).

---

### ADR-0004-T2: Single-File Generation of Matrix/Projection-Bearing Artifacts Under the Spike Cap

**Status:** TODO
**ADR Source:** ADR-0004, Decision (the most asset-heavy artifacts render under the <500KB ceiling through the shared component set); ADR-0004, Validation Approach (size budget on the asset-heavy render); ADR-0004, Open Questions (OQ-1 cap consumed here)
**Files to create/modify:**
- `scripts/generate/render.py` -- extend the engine to render the matrix/projection-bearing artifact within the `ADR-0004-T0` cap (cap rendered timepoints/series per view; paginate/split when a view would exceed the cap)
- `tests/generate/test_render.py` -- add: worst-case matrix/projection render stays < 500KB; the cap is applied; pagination/split triggers when a view exceeds the cap

**Acceptance Criteria:**
1. The most asset-heavy matrix+projection artifact rendered over the `ADR-0004-T0` spike dataset is strictly less than 500000 bytes (`wc -c` < 500000).
2. The render applies the `ADR-0004-T0` cap parameter: a view exceeding the cap's rendered-timepoints-per-view or series-per-view value is paginated/split across artifacts rather than emitted over-budget (a test feeding a dataset above the cap asserts at least 2 output files, each strictly less than 500000 bytes).
3. A render at or below the cap emits exactly one file and makes 0 external asset requests (`rg` for external asset references returns 0; an offline open observes 0 outbound requests).
4. The matrix/projection render shares the `component_set.py` markup across views — the chart-component markup appears once in the output's shared-defs block and is referenced per view, not duplicated per series (a test asserts the component template id appears in the shared-defs block exactly once).
5. The matrix/projection recompute is local-only: the cross-spec egress guard over the render observes 0 outbound calls and 0 lab value / symptom answer appears in any model-bound dispatch (D1→ADR-0007 no labs/answers to model; the render path invokes no model step).
6. `pytest tests/generate/test_render.py` passes (including the matrix/projection cases).

**Risk Mitigations:** ADR-0004 Negative (inline-everything per-file size pressure; the most asset-heavy artifacts press against the budget) — criteria 1, 2, 4 keep the worst-case render under 500KB via the cap, pagination, and shared markup. ADR-0007 Negative (matrix/projection strain the <500KB budget) — same coverage, consuming the spike cap. Constraint D1→ADR-0007 (no labs/answers to model) — criterion 5.
**Dependencies:** ADR-0004-T0 (the measured cap / pagination parameter), ADR-0004-T1 (the engine + component library extended here). Cross-spec: `ADR-0002-T1` (store read model), `ADR-0001-T1` (egress guard).

---

### ADR-0004-T3: On-Demand + Unattended (Cron) Generation Entry Point

**Status:** TODO
**ADR Source:** ADR-0004, Decision ("scheduled" = an unattended cron run that produces the file and exits; no live, always-on server or daemon); ADR-0004, Validation Approach (unattended scheduled run produces the file with 0 server process); ADR-0004, Falsification (a running server/daemon to generate or open the file is an NG-4 breach)
**Files to create/modify:**
- `scripts/generate/generate.py` -- on-demand + unattended entry point invoking `render.emit` for a named artifact and exiting; no daemon, no served surface
- `tests/generate/test_generate.py` -- file produced on demand, unattended run with stdin closed, 0 server process / 0 listening socket

**Acceptance Criteria:**
1. `generate.run(artifact_name)` writes the named artifact file and exits with code 0 (the file exists on disk after the call returns).
2. An unattended `generate.run` completes with stdin closed and 0 prompts for operator input (run with stdin closed exits 0).
3. No server process or listening socket is opened during a `generate.run` call (the test asserts 0 sockets were bound during the call), satisfying the no-live-server decision (NG-4).
4. The file produced by `generate.run` opens from disk with the network disabled (the produced file is the `ADR-0004-T1` self-contained artifact; an offline open observes 0 outbound requests).
5. The cron/unattended invocation and the on-demand invocation call the same `render.emit` path (a test asserts both entry modes route through one render function, so the unattended artifact is structurally identical to the on-demand one).
6. `pytest tests/generate/test_generate.py` passes.

**Risk Mitigations:** ADR-0004 Negative (no live server → snapshot only; a stale artifact silently misrepresents the store until re-run) — accepted, documented limitation (Component Overview); criterion 5 keeps every artifact a fresh render of the store at generation time (re-running reflects new readings), the accepted snapshot model. Falsification (a running server/daemon is an NG-4 breach) — criterion 3.
**Dependencies:** ADR-0004-T1 (the render engine the entry point invokes). Cross-spec: `ADR-0003-T1` complements this task (shares the cron/unattended-run seam with ingestion) but is not a prerequisite — generation renders manually-entered data with no importer.

---

### ADR-0005-T1: PII-Free-Trunk Gitignore Boundary + Pre-Commit Content-Scan Hook

**Status:** TODO
**ADR Source:** ADR-0005, Decision (every filled-scaffold value + the entire store excluded from version control; operator-agnostic property guaranteed by a content scan returning 0 PII hits on a fresh clone); ADR-0005, Validation Approach (content scan 0 hits; `git ls-files` lists 0 filled-scaffold value / 0 store file); ADR-0005, Open Questions (OQ-1: enforce by both gitignore + hook)
**Files to create/modify:**
- `.gitignore` -- add filled-scaffold-value exclusions to the existing `vault/store/` boundary
- `.claude/hooks/block-pii-commit.sh` -- pre-commit content-scan hook over staged/tracked files; blocks the commit on a staged filled-scaffold value, a staged store file, or a PII token in a tracked file
- `tests/hooks/test_block_pii_commit.sh` -- hook passes on a clean staged tree; blocks on a staged filled-scaffold value and on a planted tracked-file PII token

**Acceptance Criteria:**
1. `.gitignore` excludes `vault/store/` (extending the data-in entry) and every filled-scaffold value path, and `git check-ignore` exits 0 for a filled-scaffold-value path (the path is ignored).
2. A content scan of all tracked files for operator-PII tokens returns hit count 0 on a fresh clone (`block-pii-commit.sh` run in scan mode over `git ls-files` reports 0 hits).
3. `git ls-files` lists 0 filled-scaffold value and 0 `vault/store/` file (the test stages a filled scaffold and asserts it does not appear in the tracked set).
4. `block-pii-commit.sh` blocks (non-zero exit) a commit that stages a filled-scaffold value, and the message names the offending file.
5. `block-pii-commit.sh` blocks (non-zero exit) a commit when a PII token is planted in a tracked file, and passes (exit 0) on a staged tree with 0 PII tokens.
6. `block-pii-commit.sh` blocks (non-zero exit) a commit that stages any `vault/store/` file.
7. `bash tests/hooks/test_block_pii_commit.sh` passes.

**Risk Mitigations:** ADR-0005 Negative (the tracked-scaffold / gitignored-value split is a standing discipline burden — no substrate mechanism stops staging a filled scaffold) — criteria 4, 6 add the mechanism (the hook) that blocks a staged filled scaffold / store file. ADR-0005 Negative (the content-scan guarantee needs an enforcement mechanism that does not yet exist + `.gitignore` does not yet exclude the store) — criteria 1, 2, 5 land both halves (gitignore + scan hook). Constraint D2→ADR-0005 (store exclusion boundary) — criteria 1, 2, 3.
**Dependencies:** Cross-spec: `ADR-0001-T1` (the tracked-file PII-scan token set + mechanism this hook reuses) and `ADR-0002-T1` (which added the `vault/store/` gitignore entry this task extends) from `docs/spec/adr-0001-adr-0003-spec.md`. No in-spec predecessor (entry point).

---

### ADR-0005-T2: Clone-Init Step + Operator-Facing Clone README

**Status:** TODO
**ADR Source:** ADR-0005, Decision (a fresh clone is a fully independent local instance; a new operator goes from `git clone` to a fillable PII-free instance by initializing the store and filling the scaffolds locally); ADR-0005, Validation Approach (fresh clone fillable in its empty state, entered data untracked, instance generates a plan + dashboard from its own inputs alone, 0 cross-clone paths); ADR-0005, Open Questions (OQ-2: init step + README)
**Files to create/modify:**
- `scripts/clone/init_instance.py` -- clone-init step: initializes the store, surfaces the empty `status: scaffold` pages, leaves entered data untracked
- `docs/clone-init.md` -- operator-facing clone README: the `git clone` → fillable PII-free instance path
- `tests/clone/test_init_instance.py` -- fresh clone reaches a fillable PII-free instance; entered data untracked; instance generates a plan + dashboard from local inputs alone, 0 cross-clone reads

**Acceptance Criteria:**
1. `init_instance.run()` on a fresh clone leaves the scaffolds present in their empty `status: scaffold` state and produces an initialized store with 0 operator readings (the test asserts the scaffolds carry `status: scaffold` and the store directory exists and is empty of readings).
2. Data entered after `init_instance.run()` lands outside `git status` (the test enters a reading and asserts the new file is untracked / gitignored).
3. The initialized instance generates a plan and a dashboard from the clone's own inputs alone, with 0 reads of any other operator's store (the test runs generation on the clone with no other operator data present and asserts both artifacts render from local inputs only).
4. `docs/clone-init.md` exists and contains a section titled "From git clone to a fillable instance" with the concrete init command and a statement that entered data is excluded from version control.
5. `init_instance.run()` references no network resource and no cross-clone path (the cross-spec egress guard over the call observes 0 outbound calls; the test asserts 0 reads outside the local clone root).
6. `pytest tests/clone/test_init_instance.py` passes.

**Risk Mitigations:** ADR-0005 Negative (gitignored store + filled scaffolds carry no version-control backup/history — data loss if the working copy is lost) — accepted, documented limitation (Component Overview); criterion 2 keeps entered data untracked by design (the accepted trade-off), and the README (criterion 4) states the no-VC-backup consequence so the operator keeps a separate local backup.
**Dependencies:** ADR-0005-T1 (the gitignore boundary the clone-init relies on to keep entered data untracked). Cross-spec: `ADR-0002-T1` (store init/read model), `ADR-0001-T1` (egress guard).

---

### ADR-0006-T1: No-Train Router + Summary Derivation Implementation

**Status:** TODO
**ADR Source:** ADR-0006, Decision (plan reasoning runs on the no-train path over summaries, reads current state from the store); ADR-0006, Validation Approach (plan reasoning 100% on the no-train path over summaries, 0 raw-PII sends); ADR-0006, Consequences — Negative (the one PII-touching dispatch, constrained by the no-train summaries path)
**Files to create/modify:**
- `scripts/plan/router.py` -- derives the summary from store-read state per the `ADR-0006-T0` field-set and routes the plan-reasoning dispatch to the no-train lane; refuses a dispatch carrying a raw-PII field outside the summary field-set
- `tests/plan/test_router.py` -- summary carries only the field-set, dispatch routes to the no-train lane, 0 raw-PII sends, fails on an injected raw-PII send

**Acceptance Criteria:**
1. `router.summarize(store_read)` returns a summary containing only the `ADR-0006-T0` Summary Field-Set fields and 0 fields outside it (the test asserts the summary's field set equals the spike field-set, and a raw-PII field excluded by the spike is absent).
2. `router.dispatch(summary)` routes the plan-reasoning dispatch to the no-train lane (the test asserts the dispatch's lane attribute is the no-train lane, not the default/train-eligible lane).
3. `router.dispatch` over a summary built by `router.summarize` carries 0 raw-PII fields to the model — verified by the cross-spec egress guard / falsifiable check observing 0 raw-PII tokens in the model-bound payload (D1→ADR-0006 no-train summaries: 0 raw-PII sends).
4. `router.dispatch` raises (rejects with non-zero) when handed a payload containing a raw-PII field excluded by the summary field-set (the enforcement fails the dispatch rather than sending it).
5. `router.summarize` reads current state through the cross-spec store read model (`scripts/store/store.py` / `scripts/store/keying.py`) and no other source (the test asserts the read source is the store API).
6. `pytest tests/plan/test_router.py` passes.

**Risk Mitigations:** ADR-0006 Negative (plan reasoning is the one PII-touching dispatch; cannot reason over raw PII; bounded by the store read model) — criteria 1, 3, 4 implement the enforcement that keeps raw PII off the model and reads only summaries derived from the store. Constraint D1→ADR-0006 (no-train summaries) — criteria 2, 3, 4.
**Dependencies:** ADR-0006-T0 (the summary field-set + routing-enforcement design). Cross-spec: `ADR-0002-T1` (store read model), `ADR-0001-T1` (egress guard the falsifiable check reuses).

---

### ADR-0006-T2: Multi-Domain Plan Assembly — Routing, Composition, Attribution, Sourcing, Coverage Gaps

**Status:** TODO
**ADR Source:** ADR-0006, Decision (route each in-scope goal-domain to its roster specialist, compose into one attributable document; source + confidence-tier + reversibility on every recommendation; population-mismatch flag; per-section personalization; honest coverage-gap where the library is thin); ADR-0006, Validation Approach (1 attributable section per domain, 100% sourced, 100% population-mismatch-flagged, coverage gaps stated); ADR-0006, Open Questions (OQ-1: no-matching-specialist routing)
**Files to create/modify:**
- `scripts/plan/assemble.py` -- routes each in-scope goal-domain to its roster specialist, composes outputs into one attributable document, attaches source/tier/reversibility, flags population-mismatch, emits coverage-gap (thin-library + no-specialist) disclosures, personalizes per section from the router summary
- `tests/plan/test_assemble.py` -- one attributable section per domain, 100% sourced, population-mismatch flag, thin-library + no-specialist coverage gaps, composition-attribution integrity

**Acceptance Criteria:**
1. The assembled plan contains exactly one section per in-scope goal-domain, each naming the specialist that produced it, and 0 unattributable sections (the test lists the goal-domains and asserts a 1:1 attributed-section mapping).
2. Every recommendation in the plan carries a source citation, a confidence tier, and a reversibility note; every number carries units + a reference range; the count of recommendations missing any of these is 0 (a scan of the assembled plan reports 0 incomplete recommendations).
3. Every animal/in-vitro-grounded recommendation carries an explicit population-mismatch flag (the test plants an animal-grounded recommendation and asserts the flag is present; an unflagged animal-grounded recommendation fails the test).
4. A thin-library in-scope domain renders a stated coverage-gap disclosure, not a fabricated regimen (the test routes a domain with no vetted library coverage and asserts a gap statement, 0 fabricated recommendations).
5. An in-scope goal-domain with no matching deployed roster specialist renders a coverage-gap-by-absence disclosure (same shape as a thin-library gap), not a fabricated regimen and not a silent drop (the test supplies a domain absent from the roster, asserts a stated gap, and asserts the domain is present in the plan).
6. The composition step preserves each section's attribution and introduces 0 cross-domain claims sourced by no single specialist (the test asserts every claim in the composed document traces to exactly one section's specialist; a fabricated cross-domain claim fails the assertion).
7. Plan assembly reasons only over the `ADR-0006-T1` router summary, not raw PII (the test asserts `assemble` consumes the router's no-train summary and the cross-spec egress guard observes 0 raw-PII sends).
8. `pytest tests/plan/test_assemble.py` passes.

> Sizing note: this task carries 8 criteria (one over the 3-7 target). Criteria 1-6 are the distinct FR-1 / NFR-5 / NFR-6 / FR-5 / OQ-1 obligations the ADR Decision and Validation Approach make load-bearing and mutually non-overlapping (attribution, sourcing, population-mismatch, thin-library gap, no-specialist gap, composition integrity); criteria 7-8 are the cross-task PII boundary and the test gate. The set is held at 8 rather than split because criteria 1-6 are a single composition pass over one file (`assemble.py`) and splitting them would fragment one vertical slice; the file count (2) stays within the right-sized band.

**Risk Mitigations:** ADR-0006 Negative (composition/attribution adds an orchestration layer; a composition bug can drop a section's attribution or fabricate a cross-domain claim no single specialist sourced) — criteria 1, 6 assert per-section attribution and 0 fabricated cross-domain claims (the composition-attribution integrity check). ADR-0006 Negative (routing needs a matching specialist; a no-specialist domain has no routing target) — criterion 5 (coverage-gap-by-absence). ADR-0006 Negative (plan richness bounded by thin library) — accepted, documented limitation (Component Overview); criterion 4 enforces the honest coverage-gap that is the accepted contract. Constraint D1→ADR-0006 (no-train summaries) — criterion 7.
**Dependencies:** ADR-0006-T0 (summary contract), ADR-0006-T1 (the router summary `assemble` consumes), ADR-0004-T1 (the plan is rendered through the generation path). Cross-spec: `ADR-0002-T1` (store read model via the router), `ADR-0001-T1` (egress guard).

---

### ADR-0007-T1: Lab-Loop / Watch-Out / Physician-Feedback Store Schemas

**Status:** TODO
**ADR Source:** ADR-0007, Decision (lab loop + watch-out + physician feedback as store schemas: a recommended-but-undrawn panel stored "pending" never a result; watch-out answers + physician feedback stored over time as next-generation inputs; pending / not-yet-answered / no-prior carried as store state); ADR-0007, Validation Approach (pending-not-result, unanswered renders not-yet-answered, answered/feedback read on next generation); ADR-0007, Open Questions (OQ-2: watch-out question derivation)
**Files to create/modify:**
- `scripts/store/loop_schema.py` -- store schemas for the lab loop (pending panels), watch-out answers (with question derivation from active protocols/compounds), and physician feedback; pending / not-yet-answered / no-prior / answered-over-time state on the data-in store
- `tests/store/test_loop_schema.py` -- pending panel persists across generations, watch-out answer read on next generation, physician feedback carried forward, question derivation, no signal automation

**Acceptance Criteria:**
1. A panel recommended by the plan but not yet drawn is stored as "pending" and persists across a generation cycle (after storing a pending panel and re-reading on a later generation, the panel is still "pending", never a fabricated result).
2. An unanswered watch-out check-in is stored as "not yet answered" (the read returns the not-yet-answered state, not a clear or absent result), and a biomarker with one stored timepoint reads "no prior" (not a fabricated trend).
3. A watch-out answer stored this cycle is read on the next generation (the test stores an answer, runs a next-generation read, and asserts the answer is present as a next-generation input — a dropped answer fails the test).
4. A recorded post-visit physician feedback entry is carried forward to the next plan/report generation (the test records feedback, runs a next-generation read, asserts it is present — a dropped entry fails the test).
5. The watch-out question set is derived at generation from the operator's active protocols/compounds (the test supplies an active protocol and asserts the derived question set covers the watch-outs that protocol implies), and the schema performs 0 automated signal detection (the schema only stores operator-entered answers; `rg` over `loop_schema.py` finds 0 threshold-evaluation / automated-detection step — NG-6).
6. The schemas append to the data-in store via the cross-spec store API (`scripts/store/store.py`) and store lab values / symptom answers local-only with 0 model-bound send (the cross-spec egress guard over a store/read cycle observes 0 outbound calls — D1→ADR-0007 no labs/answers to model).
7. `pytest tests/store/test_loop_schema.py` passes.

**Risk Mitigations:** ADR-0007 Negative (a watch-out answer is carried into the NEXT generation, not the current one — inherent loop latency) — accepted, documented limitation (Component Overview); criteria 3, 4 enforce the carry-to-next-generation contract (the accepted latency, not a render bug). ADR-0007 Negative (the store-schema-vs-render-view split adds a contract surface; a state the store records but the view misreads is a 2-decision defect) — criteria 1, 2 fix the store-side state definitions the `ADR-0007-T2` render views must read (the integration test in `ADR-0007-T2` closes the cross-boundary). Constraint D1→ADR-0007 (no labs/answers to model) — criterion 6.
**Dependencies:** ADR-0006-T2 (the plan recommends the bloodwork the loop ingests; the loop's input edge is downstream of plan assembly). Cross-spec: `ADR-0002-T1` (the store append/read + `keying.py` the schemas write through), `ADR-0001-T1` (egress guard).

---

### ADR-0007-T2: Biomarker-Matrix + Projection Render-Time Views

**Status:** TODO
**ADR Source:** ADR-0007, Decision (biomarker matrix + projections as render-time views over stored timepoints; projection guardrail is a render-time contract: ≥3 timepoints, "naive projection" label + method + count + widening band + milestones; exactly-2 trend-only); ADR-0007, Validation Approach (matrix ≥2-timepoint side-by-side, projection ≥3-timepoint full-label, exactly-2 trend-only); ADR-0004, Open Questions (OQ-1 cap consumed here)
**Files to create/modify:**
- `scripts/generate/render_views.py` -- render-time view builders for the matrix (cross-reference each biomarker across its stored timepoints) and projections (≥3-timepoint guardrail, label/method/count/band/milestones), reading the `ADR-0007-T1` store state, applying the `ADR-0004-T0` cap
- `tests/generate/test_render_views.py` -- ≥2-timepoint matrix side-by-side, ≥3-timepoint projection with full label set, exactly-2 trend-only, pending/not-yet-answered/no-prior states, 0 external requests, 0 PII to model

**Acceptance Criteria:**
1. A biomarker with ≥2 stored timepoints renders in the matrix with both timepoints cross-referenced side by side, recomputed from the store with no stored copy (the test stores 2 timepoints and asserts both appear; a latest-only render fails the test).
2. A projection renders only when an item has ≥3 stored timepoints, and an item with exactly 2 timepoints renders trend-only with no projection (the test asserts a projection is present at 3 timepoints and absent at 2; a projection at fewer than 3 timepoints fails the test).
3. A rendered projection carries the label "naive projection from recent trend — not a clinical forecast", its method, its datapoint count, a widening uncertainty band, and key dates/milestones on the time axis (the test asserts all five elements are present in the projection output).
4. A recommended-but-undrawn panel renders "pending" (never a result) and an unanswered check-in renders "not yet answered" (the views read the `ADR-0007-T1` store state and map it 1:1; a pending panel rendered as a result fails the test).
5. The matrix/projection recompute is local-only with 0 external asset requests (`rg` for external asset references returns 0; an offline open observes 0 outbound requests) and 0 lab value / symptom answer appears in any model-bound dispatch (the render path invokes no model step — D1→ADR-0007 no labs/answers to model).
6. The worst-case matrix/projection view stays within the `ADR-0004-T0` cap: a view exceeding the cap is paginated/split so each rendered artifact is strictly less than 500000 bytes (`wc -c` < 500000 per output file).
7. `pytest tests/generate/test_render_views.py` passes.

**Risk Mitigations:** ADR-0007 Negative (the store-schema-vs-render-view split is a 2-decision contract surface; a state the store records but the view misreads is a defect spanning two decisions) — criterion 4 is the cross-boundary integration check, asserting the render views map the `ADR-0007-T1` store states (pending / not-yet-answered) 1:1 to their rendered states. ADR-0007 Negative (matrix/projection strain the <500KB budget) — criterion 6 consumes the `ADR-0004-T0` cap. ADR-0007 Negative (≥3-timepoint guardrail → projections absent early, trend-only) — accepted, documented limitation (Component Overview); criterion 2 enforces the honest-absence contract (the guardrail, not a bug). Constraint D1→ADR-0007 (no labs/answers to model) — criterion 5.
**Dependencies:** ADR-0004-T0 (the render cap), ADR-0004-T1 (the generation engine + component library), ADR-0007-T1 (the store-schema states the views read). Cross-spec: `ADR-0002-T1` (store read model), `ADR-0001-T1` (egress guard).

---

## Dependency Map

```
ADR-0004-T0 --> ADR-0004-T2   (measured cap / pagination parameter the asset-heavy render consumes)
ADR-0004-T0 --> ADR-0007-T2   (measured cap the matrix/projection views keep under 500KB)
ADR-0004-T1 --> ADR-0004-T2   (the render engine + component library, extended for the asset-heavy render)
ADR-0004-T1 --> ADR-0004-T3   (the render engine the on-demand+cron entry point invokes)
ADR-0004-T1 --> ADR-0006-T2   (the plan is rendered through the generation path)
ADR-0004-T1 --> ADR-0007-T2   (the generation engine + component library the views render through)
ADR-0005-T1 --> ADR-0005-T2   (the gitignore boundary the clone-init relies on to keep entered data untracked)
ADR-0006-T0 --> ADR-0006-T1   (the summary field-set + routing-enforcement design the router implements)
ADR-0006-T0 --> ADR-0006-T2   (the summary contract the assembly reasons over)
ADR-0006-T1 --> ADR-0006-T2   (the router summary the assembly consumes)
ADR-0006-T2 --> ADR-0007-T1   (the plan recommends the bloodwork the lab loop ingests; loop input is downstream of plan assembly)
ADR-0007-T1 --> ADR-0007-T2   (the store-schema states the render views read)
```

Entry points (no dependencies on tasks authored in this spec): ADR-0004-T0, ADR-0004-T1, ADR-0005-T1, ADR-0006-T0

Cross-spec dependencies (consumed as a fixed interface from `docs/spec/adr-0001-adr-0003-spec.md`, NOT nodes authored here): `ADR-0002-T1` (store append/read + `keying.py` read model) → ADR-0004-T1, ADR-0005-T2, ADR-0006-T1, ADR-0007-T1, ADR-0007-T2; `ADR-0001-T1` (egress + tracked-file PII-scan guard) → ADR-0004-T1, ADR-0004-T2, ADR-0005-T1, ADR-0005-T2, ADR-0006-T1, ADR-0006-T2, ADR-0007-T1, ADR-0007-T2; `ADR-0001-T0` (egress + PII-scan mechanism) → ADR-0006-T0; `ADR-0003-T1` (ingestion fallback + shared cron seam) → ADR-0004-T3 (complement, no ordering edge — generation renders manually-entered data with no importer).

Topological order (Kahn parallel groups):
1. **Group 1 (parallel — entry points, no in-spec dependencies):** ADR-0004-T0, ADR-0004-T1, ADR-0005-T1, ADR-0006-T0
2. **Group 2 (parallel — each depends only on Group 1):** ADR-0004-T2 (after ADR-0004-T0, ADR-0004-T1), ADR-0004-T3 (after ADR-0004-T1), ADR-0005-T2 (after ADR-0005-T1), ADR-0006-T1 (after ADR-0006-T0)
3. **Group 3:** ADR-0006-T2 (after ADR-0006-T0, ADR-0006-T1, ADR-0004-T1)
4. **Group 4:** ADR-0007-T1 (after ADR-0006-T2)
5. **Group 5:** ADR-0007-T2 (after ADR-0004-T0, ADR-0004-T1, ADR-0007-T1)

Critical path: ADR-0006-T0 → ADR-0006-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2

No cycles (5 groups; every edge points from an earlier group to a later group; Kahn drains all 11 nodes).

**Data flow per edge:**
- `ADR-0004-T0 → ADR-0004-T2`: the measured cap / pagination parameter (the asset-heavy render keeps each output under 500KB by applying it).
- `ADR-0004-T0 → ADR-0007-T2`: the same cap (the matrix/projection views paginate/split against it).
- `ADR-0004-T1 → ADR-0004-T2`: the render engine + `component_set.py` library (T2 extends it for the asset-heavy render).
- `ADR-0004-T1 → ADR-0004-T3`: the `render.emit` path (the on-demand+cron entry point invokes it).
- `ADR-0004-T1 → ADR-0006-T2`: the generation path (the assembled plan is rendered through it).
- `ADR-0004-T1 → ADR-0007-T2`: the generation engine + component library (the views render through it).
- `ADR-0005-T1 → ADR-0005-T2`: the gitignore boundary (the clone-init relies on it so entered data lands untracked).
- `ADR-0006-T0 → ADR-0006-T1`: the summary field-set + routing-enforcement design (the router implements it).
- `ADR-0006-T0 → ADR-0006-T2`: the summary contract (the assembly reasons over it).
- `ADR-0006-T1 → ADR-0006-T2`: the router's no-train summary (the assembly consumes it).
- `ADR-0006-T2 → ADR-0007-T1`: the assembled plan's bloodwork recommendation (the lab loop's input edge depends on it).
- `ADR-0007-T1 → ADR-0007-T2`: the store-schema pending / not-yet-answered / no-prior states (the render views read them).

## Test Strategy

### Unit Tests
- **Scope:** `scripts/generate/render.py`, `scripts/generate/generate.py`, `scripts/generate/render_views.py`, `scripts/plan/assemble.py`, `scripts/plan/router.py`, `scripts/store/loop_schema.py`, `scripts/clone/init_instance.py`, `vault/design/templates/*.py`, `.claude/hooks/block-pii-commit.sh`.
- **Approach:** `pytest` over generation/plan/store operations using a temp `vault/store/` fixture directory and fixture store reads; a render fixture for size (`wc -c`) and external-asset-reference (`rg`) checks; a fixture goal-set + a stubbed roster for plan-assembly attribution/sourcing/coverage-gap checks; planted-token fixtures for the pre-commit hook (run via `bash`); spike-report content checks for the two `[Spike]` tasks.
- **Criteria covered:** ADR-0004-T0 criteria 1-7 (spike report content checks); ADR-0006-T0 criteria 1-6 (spike report content checks); ADR-0004-T1 criteria 1-4, 6, 7; ADR-0004-T2 criteria 1-4, 6; ADR-0004-T3 criteria 1-3, 5, 6; ADR-0005-T1 criteria 1, 3-7; ADR-0005-T2 criteria 1, 4, 6; ADR-0006-T1 criteria 1-2, 4-6; ADR-0006-T2 criteria 1-6, 8; ADR-0007-T1 criteria 1-5, 7; ADR-0007-T2 criteria 1-4, 6, 7.

### Integration Tests
- **Scope:** the cross-task substrate paths — (a) the cross-spec egress guard (`scripts/guard/egress_guard.py`) wrapped around a full `render.emit`, `generate.run`, `router.dispatch`, `assemble`, `loop_schema` store cycle, and `render_views` build, asserting 0 outbound calls / 0 PII to model; (b) the store-schema-to-render-view boundary (the `ADR-0007-T1` states mapped 1:1 by the `ADR-0007-T2` views — the pending / not-yet-answered / no-prior 2-decision contract); (c) the tracked-file PII-scan / gitignore boundary on a fresh clone (the pre-commit hook + `git check-ignore` + `git ls-files`); (d) the clone-init → generate-from-local-inputs-alone path with 0 cross-clone reads; (e) the plan → lab-loop input edge (assembled-plan recommendation feeds the loop schema).
- **Approach:** run each operation end-to-end against the temp store and a scratch clone/worktree, then assert artifact contents, run the egress guard over the same invocation, and run `git check-ignore` / `git ls-files` against the scratch clone.
- **Criteria covered:** ADR-0004-T1 criterion 5; ADR-0004-T2 criterion 5; ADR-0004-T3 criterion 4; ADR-0005-T1 criterion 2; ADR-0005-T2 criteria 2, 3, 5; ADR-0006-T1 criterion 3; ADR-0006-T2 criterion 7; ADR-0007-T1 criterion 6; ADR-0007-T2 criterion 5.

### Risk-Specific Tests
- **D4↔D7 size budget (ADR-0004 Negative — the <500KB budget caps richness + inline-everything per-file size pressure; ADR-0007 Negative — matrix/projection strain the budget):** the `ADR-0004-T0` spike measures the worst-case render (criteria 1-7); `ADR-0004-T2` criteria 1-2 and `ADR-0007-T2` criterion 6 keep the worst-case render under 500KB via the spike cap, pagination, and shared component markup.
- **PII no-egress at render (D1→ADR-0004):** the egress guard over `render.emit` / `generate.run` observes 0 outbound calls (ADR-0004-T1 criterion 5, ADR-0004-T3 criterion 4); the engine refuses an external asset (ADR-0004-T1 criterion 6).
- **No labs/answers to model (D1→ADR-0007):** the matrix/projection recompute is local-only with 0 model-bound send (ADR-0004-T2 criterion 5, ADR-0007-T2 criterion 5); the loop schemas store local-only (ADR-0007-T1 criterion 6).
- **No-train summaries (D1→ADR-0006):** the router routes to the no-train lane with 0 raw-PII sends and fails on an injected raw-PII send (ADR-0006-T1 criteria 2-4); the assembly reasons only over the summary (ADR-0006-T2 criterion 7).
- **Store exclusion boundary (D2→ADR-0005):** the pre-commit hook blocks a staged filled-scaffold value / store file and a planted tracked-file PII token, and the content scan reports 0 hits on a clean tree (ADR-0005-T1 criteria 1-6).
- **Composition-attribution bug (ADR-0006 Negative — a composition bug can drop attribution or fabricate a cross-domain claim no single specialist sourced):** `ADR-0006-T2` criteria 1, 6 assert per-section attribution and 0 fabricated cross-domain claims.
- **Store-schema-vs-render-view defect (ADR-0007 Negative — a state the store records but the view misreads is a 2-decision defect):** `ADR-0007-T1` criteria 1-2 define the store states and `ADR-0007-T2` criterion 4 asserts the render views map them 1:1 (the cross-boundary integration test).
- **No-matching-specialist routing (ADR-0006 Negative — a no-specialist domain has no routing target):** `ADR-0006-T2` criterion 5 renders a coverage-gap-by-absence disclosure.

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section — each task cites ADR Decision / Validation Approach / Consequences / Open Questions by name.
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task — ADR-0004: T0, T1, T2, T3; ADR-0005: T1, T2; ADR-0006: T0, T1, T2; ADR-0007: T1, T2.
- [x] All ADR IDs resolve to actual ADR files on disk — ADR-0004/0005/0006/0007 in `docs/adr/`.

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion — each has 6-8.
- [x] All acceptance criteria are binary (pass/fail, no subjective measures) — each cites a command (`wc -c`, `rg`, `git check-ignore`, `git ls-files`, `pytest`, the egress guard), a file/section condition, or a counted assertion (0 hits, exactly one section, < 500000 bytes).
- [x] No criterion uses words: "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient" (nor "comprehensive", "optimize", "streamline", "enhanced", "flexible") — verified by a banned-word scan over all criteria.

### File Manifest Integrity
- [x] Every task has a file manifest (files to create/modify).
- [x] Every file in any task block appears in the top-level File Manifest — `render.py`/`test_render.py` appear in T1 + T2 and are listed once in the manifest (T2's create/modify of `render.py` is a Modify of the T1-created file, ordered by the ADR-0004-T1→ADR-0004-T2 dependency).
- [x] Every file in the top-level File Manifest appears in at least one task block — 23 manifest entries, each mapped to a task.
- [x] No task lists a directory instead of a specific file — every entry names a file with an extension.
- [x] Every source file has a corresponding test file — `render.py`→`test_render.py`; `generate.py`→`test_generate.py`; `render_views.py`→`test_render_views.py`; `assemble.py`→`test_assemble.py`; `router.py`→`test_router.py`; `loop_schema.py`→`test_loop_schema.py`; `init_instance.py`→`test_init_instance.py`; `block-pii-commit.sh`→`test_block_pii_commit.sh`. The template `.py` files (`component_set.py`/`dashboard.py`/`report.py`) are exercised through `test_render.py` (they have no behavior independent of the render engine that assembles them); `docs/clone-init.md` (README) and the two spike `.md` reports are verified by file/section condition checks in their tasks (doc/spike artifacts, no test file); `.gitignore` is a config file verified by `git check-ignore` in `ADR-0005-T1`.

### Dependency Map Integrity
- [x] Dependency map has no cycles — Kahn drains all 11 nodes; 5 ordered groups; every edge points earlier→later group.
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map — all in-spec Dependencies (ADR-0004-T0/T1/T2/T3, ADR-0005-T1/T2, ADR-0006-T0/T1/T2, ADR-0007-T1/T2) are map nodes; cross-spec deps (ADR-0001-T0/T1, ADR-0002-T1, ADR-0003-T1) are listed separately, not as in-spec nodes.
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block — 12 edges, each matched to a target task's Dependencies field.
- [x] Entry points are listed and have Dependencies: "None (entry point)" — ADR-0004-T0 and ADR-0006-T0 state "None (entry point)"; ADR-0004-T1 and ADR-0005-T1 have only cross-spec dependencies (no in-spec predecessor) and are noted as entry points.

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream constraints in their acceptance criteria — D1→ADR-0004 PII no-egress at render (ADR-0004-T1 criteria 1, 5; ADR-0004-T3 criterion 4); D1→ADR-0007 no labs/answers to model (ADR-0004-T2 criterion 5, ADR-0007-T1 criterion 6, ADR-0007-T2 criterion 5); D1→ADR-0006 no-train summaries (ADR-0006-T1 criteria 2-4, ADR-0006-T2 criterion 7); D2→ADR-0005 store exclusion boundary (ADR-0005-T1 criteria 1-6).
- [x] Constraint Propagation Table entries have corresponding acceptance criteria in affected tasks — all four in-scope DAG §8 rows (context.md constraint table) mapped above.

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present — 7 rows: 2 Block, 4 Proceed, 1 Defer (the upstream data-in interface).
- [x] Every open question, pending tension, and unmitigated risk has a disposition (Proceed/Block/Defer) — the 6 dispositions.md items + the upstream-interface deferral.
- [x] Block dispositions have corresponding research spike tasks — D4↔D7 tension → ADR-0004-T0; ADR-0006 OQ-2 summary/router → ADR-0006-T0.
- [x] Defer dispositions have justifications explaining why deferral is safe — the upstream-interface row states the data-in spec ships those tasks before this cut runs.

### Risk Coverage
- [x] Risk Mitigations field present on every task — all 11 tasks carry it.
- [x] Every negative consequence in in-scope ADRs is covered — ADR-0004: <500KB caps richness → T0/T2; no-live-server/stale snapshot → T3 (documented); inline-everything size pressure → T0/T2; store-read+no-egress constraint → T1 criteria 5-6. ADR-0005: no-VC-backup → T2 (documented); discipline burden → T1; no-mechanism/gitignore-gap → T1. ADR-0006: thin-library bound → T2 coverage-gap (documented); composition/attribution bug → T2 criteria 1,6; no-specialist domain → T2 criterion 5; no-train+store-read bound → T0/T1. ADR-0007: projections-absent-early → T2 (documented guardrail); store-schema-vs-render-view defect → T1/T2 integration; matrix/projection strain budget → T0/T2; loop latency → T1 (documented).

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category — Unit + Integration + Risk-Specific subsections together cover all criteria of all 11 tasks.
- [x] Risk-specific tests exist for every mitigated risk — the Risk-Specific subsection enumerates the D4↔D7 size budget, all four PII-vector constraints, the composition-attribution bug, the store-schema-vs-render-view defect, and the no-matching-specialist routing.

### Downstream Readiness
- [x] Frontmatter has all required fields — scope, adrs, tier (5), created, status.
- [x] All section headers match the template exactly (for machine parsing) — Component Overview, Unresolved Concerns Disposition, File Manifest, Tasks, Dependency Map, Test Strategy, Validation Checklist.
- [x] No placeholder text ("TBD", "TODO: fill in", "...") — `Status: TODO` is the template-defined task field value, not placeholder prose; no unresolved fill-ins remain.
