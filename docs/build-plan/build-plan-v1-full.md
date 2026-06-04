---
source-specs: [docs/spec/adr-0001-adr-0003-spec.md, docs/spec/adr-0004-adr-0007-spec.md]
adrs: [ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007]
created: 2026-06-04
status: approved
total-waves: 7
critical-path-length: 6 tasks
estimated-effort: 16 task-days
---

# Build Plan: a-plus-maxing V1 — Data-In Foundation + Data-Out Cut

This plan merges two approved specs into one wave-scheduled build: Spec A (data-in, tier 3, ADR-0001/0002/0003, 7 tasks) and Spec B (data-out, tier 5, ADR-0004/0005/0006/0007, 11 tasks). 18 tasks total, all software (local Python scripts under `scripts/`, template `.py` under `vault/design/templates/`, a pre-commit hook under `.claude/hooks/`, plus four `[Spike]` reports and config). The substrate is local Python 3.12+ over `vault/store/*.ndjson` and the markdown vault; tooling is `pytest`, `rg`, `git`. There is no server, no database engine, and no web framework (both specs state this). The deployed medical specialists are the runtime CONTENT that `assemble.py` (ADR-0006-T2) routes to, not the builder of any script — every script in this plan is built by SE; the design/security/test tasks go to Architect/Security/QA.

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| Python 3.12+ interpreter (project venv) | Every task runs `pytest` and project Python under `scripts/` | `python3 --version \| grep -qE '3\.(1[2-9]\|[2-9][0-9])'` |
| `pytest` installed in the active environment | Every wave checkpoint runs `pytest` over the task's test files | `python3 -c "import pytest"` && `pytest --version` |
| `rg` (ripgrep) on PATH | External-asset / PII-token / key-definition / model-call scans across criteria (ADR-0001-T1, ADR-0003-T1, ADR-0004-T1, ADR-0005-T1, ADR-0007-T1) | `rg --version` |
| `git` on PATH with the repo initialized | `git check-ignore` / `git ls-files` / `git diff --numstat` mechanical assertions (ADR-0002-T1, ADR-0003-T2, ADR-0005-T1, ADR-0005-T2) | `git -C "$(git rev-parse --show-toplevel)" rev-parse --is-inside-work-tree` |
| Writable scratch worktree/clone path for fresh-clone assertions | The tracked-file PII scan and clone-init tests run against a fresh clone/worktree (ADR-0001-T1, ADR-0005-T1, ADR-0005-T2) | `D=$(mktemp -d) && test -w "$D" && rmdir "$D"` |

**Wave-gated prerequisite (NOT a Wave-1 prerequisite).** The egress-capture harness the `ADR-0001-T0` spike selects (a syscall/socket interceptor or offline-namespace run) is a prerequisite for the wave where the guard tasks land — `ADR-0001-T1` in Wave 2 and every 0-egress criterion from Wave 3 onward — not for Wave 1. The Wave-1 spike `ADR-0001-T0` only names/selects the mechanism on paper (its acceptance criteria are spike-report section checks, AC 2 names a mechanism but runs nothing), so it does not itself need the harness running. The harness is therefore listed here but gated to the Wave-2 entry criteria, not the Wave-1 entry criteria, to avoid BP-08 (phantom Wave-1 infrastructure that no Wave-1 task actually exercises). Verification once selected: the egress guard returns exit 0 over a synthetic local-only operation — `python3 -c "from scripts.guard.egress_guard import run; import sys; sys.exit(0 if run(lambda: open('/dev/null').read()) else 1)"` — runnable only after `ADR-0001-T1` builds `egress_guard.py`.

## Wave Schedule

Built directly from the merged Kahn topological sort (analysis §3, independently re-derived in the CPM pass below; all 18 tasks placed, 0 cycles, depth = 7). Risk ordering applied within the topological constraints: the two dependency-free spikes (`ADR-0001-T0`, `ADR-0004-T0`) land in Wave 1; the third spike (`ADR-0006-T0`) lands in Wave 3 as a documented justified exception (Risk Schedule 5a). Effort estimates use the files × criteria heuristic (wave-scheduling §4), upper bound of the range, +0.5 for spikes. Wave wall-clock = the max single-task estimate in the wave (tasks run in parallel).

### Wave 1: Foundations — PII-Boundary Design, Store-Keying Design, Render-Size Measurement

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0001-T0 | [Spike] Data-In PII-Boundary Enforcement Mechanism | Architect | 1-1.5 days |
| ADR-0002-T0 | [Spike] Store Layout + (item, timepoint) Keying Scheme | Architect | 1-1.5 days |
| ADR-0004-T0 | [Spike] D4↔D7 Render-Size Measurement + Cap Parameter | Architect | 1-1.5 days |

**Entry Criteria:**
- All Infrastructure Prerequisites pass verification (the Wave-1 row set; the egress-capture harness is NOT required here — see the wave-gated note).

**Exit Criteria / Checkpoint:**
- `test -f docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md` and the file contains the sections "Egress Guard Mechanism", "Tracked-File PII Scan Mechanism", "No-Raw-Reading-To-Model Rule", "Recommendation", "Follow-up Tasks" (ADR-0001-T0 criteria 1-6); the Recommendation names exactly one egress-capture mechanism + one PII-scan mechanism.
- `test -f docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md` and the file contains "File Granularity", "Timepoint Key", "Line Field Set", "Dedupe Key (ADR-0003 OQ-2)", "Recommendation", "Follow-up Tasks" (ADR-0002-T0 criteria 1-6); the dedupe-key tuple is a subset of the line field set.
- `test -f docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md` and the file contains "Dataset", "Render Method", "Measured Size", "Mitigation If Over Budget", "Cap / Pagination Parameter", "Follow-up Tasks" (ADR-0004-T0 criteria 1-7); Measured Size is a recorded byte number and the Cap is a number or stated rule.
- **Verifier:** Architect (spike content is design-level).

**Wall-clock estimate:** 1.5 days (3 spikes in parallel).

---

### Wave 2: Data-In Store + Guard Implementation

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0002-T1 | Local NDJSON Store Append/Read Library + Gitignore Entry | SE | 2-3 days |
| ADR-0001-T1 | Egress + Tracked-File PII-Scan Guard Implementation | SE + Security review | 1-2 days |

**Entry Criteria:**
- Wave 1 checkpoint passed (all three spike reports present with a selected mechanism / key / cap).
- Egress-capture harness selected in `ADR-0001-T0` is installed/available in the environment (the wave-gated prerequisite; consumed by `ADR-0002-T1` criterion 4 and built into `ADR-0001-T1`).

**Exit Criteria / Checkpoint:**
- `pytest tests/store/test_store.py tests/store/test_keying.py` passes (ADR-0002-T1 criterion 7).
- `pytest tests/guard/test_egress_guard.py tests/guard/test_pii_scan.py` passes (ADR-0001-T1 criterion 5).
- `git check-ignore vault/store/x.ndjson` exits 0 (ADR-0002-T1 criterion 6; ADR-0001-T1 criterion 4 asserts `git check-ignore vault/store/` exits 0).
- `scripts/store/store.py`, `scripts/store/keying.py`, `scripts/guard/egress_guard.py`, `scripts/guard/pii_scan.py` exist on disk; `.gitignore` contains a `vault/store/` entry.
- The egress guard returns pass over a `store.append`→`store.read` cycle and fail over an injected outbound call (ADR-0002-T1 criterion 4; ADR-0001-T1 criterion 1); the PII scan returns 0 on the clean tracked tree and ≥1 on a planted token (ADR-0001-T1 criteria 2-3).
- **Verifier:** QA, with Security sign-off on `ADR-0001-T1` (the PII/egress boundary).

**Wall-clock estimate:** 3 days (`ADR-0002-T1` is the longer task).

---

### Wave 3: Ingestion Routine, Generation Engine, Gitignore Boundary, No-Train Router Design

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0003-T1 | Shared Ingestion Routine, Adapter Interface, Dedupe + Manual-Entry Fallback | SE | 2 days |
| ADR-0004-T1 | Generation Engine + Template Component Library (Dashboard + Report) | SE | 2-3 days |
| ADR-0005-T1 | PII-Free-Trunk Gitignore Boundary + Pre-Commit Content-Scan Hook | SE + Security review | 1-2 days |
| ADR-0006-T0 | [Spike] Plan-Reasoning Summary Contract + No-Train Router Enforcement | Architect | 1-1.5 days |

**Entry Criteria:**
- Wave 2 checkpoint passed (store read model + `keying.py` green; egress + PII-scan guard green — both are cross-spec inputs every Wave-3 task consumes).

**Exit Criteria / Checkpoint:**
- `pytest tests/ingest/test_ingest.py` passes (ADR-0003-T1 criterion 7); the ingestion dedupe key is imported from `scripts/store/keying.py` (`rg "def .*key" scripts/ingest/` returns 0 independent key functions, ADR-0003-T1 criterion 3); ADR-0003-T1 criterion 5 carries BOTH mechanical halves — the egress guard over an `ingest.run` observes 0 outbound calls AND the static no-model-step scan `rg` over `scripts/ingest/` finds 0 model/API-client calls (expect 0; constraint D1→D3).
- `pytest tests/generate/test_render.py` passes (ADR-0004-T1 criterion 7); a dashboard and a report each render to one self-contained HTML file < 500000 bytes (`wc -c`, criterion 2) with 0 external asset references (`rg` for non-`data:` `src=`/`href=`/`url(` returns 0, criterion 1); the egress guard over `render.emit` observes 0 outbound calls (criterion 5).
- **Accessibility / color-vision-safety gate (ADR-0004-T1 criterion 3):** `pytest tests/generate/test_render.py::test_contrast_and_colorblind` reports a **measured AA contrast ratio** (a numeric ratio ≥ 4.5 for normal text / ≥ 3.0 for large text — the test prints the computed ratio, not a boolean) AND a **measured color-distance number** for every adjacent-series color pair above the stated deuteranopia/protanopia threshold under the simulated color-vision transform (the test prints the computed distance), AND asserts an `@media print` block is present in the emitted file. Go/no-go FAILS if any assertion reports a non-numeric / `assert True` stub instead of a computed value — a placeholder cannot pass this checkpoint silently.
- `bash tests/hooks/test_block_pii_commit.sh` passes (ADR-0005-T1 criterion 7); `git check-ignore` exits 0 for a filled-scaffold-value path (criterion 1); `git ls-files` lists 0 filled-scaffold value and 0 `vault/store/` file — the negative-placement assertion that data is NOT in the tracked set, distinct from the `git check-ignore` of criterion 1 (ADR-0005-T1 criterion 3; project mandate: assert placement, not just existence); the hook routes the staged set through the cross-spec `pii_scan.scan` and blocks a staged store file / planted token (criteria 2, 5, 6).
- `test -f docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md` with sections "Summary Field-Set", "Summary Derivation", "Routing-Enforcement Mechanism", "Falsifiable Check", "Recommendation", "Follow-up Tasks" (ADR-0006-T0 criteria 1-6); Recommendation names exactly one routing-enforcement mechanism and the field-set excludes named raw-PII fields.
- Cross-spec integration check: every Wave-3 data-out task runs green only with the Wave-2 guard (`scripts/guard/egress_guard.py`) and store read model (`scripts/store/store.py` / `keying.py`) in place — confirmed by the egress-guard and store-read assertions above.
- **Verifier:** QA, with Security sign-off on `ADR-0005-T1`; Architect verifies the `ADR-0006-T0` spike report (design-level).

**Wall-clock estimate:** 3 days (`ADR-0004-T1` is the longer task).

---

### Wave 4: Adapters, Asset-Heavy Render, Cron Entry Point, Clone-Init, Router Implementation

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0003-T2 | First-Cut Adapters (HealthKit + Oura), Garmin 0-Edit Proof, Whoop Stub | SE | 2-3 days |
| ADR-0004-T2 | Single-File Generation of Matrix/Projection-Bearing Artifacts Under the Spike Cap | SE | 1-2 days |
| ADR-0004-T3 | On-Demand + Unattended (Cron) Generation Entry Point | SE | 1 day |
| ADR-0005-T2 | Clone-Init Step + Operator-Facing Clone README | SE | 1-1.5 days |
| ADR-0006-T1 | No-Train Router + Summary Derivation Implementation | SE + Security review | 1-2 days |

**Entry Criteria:**
- Wave 3 checkpoint passed (shared ingestion routine green, generation engine green, gitignore boundary + hook green, router spike report present with a selected enforcement mechanism).

**Exit Criteria / Checkpoint:**
- `pytest tests/ingest/test_adapters.py` passes (ADR-0003-T2 criterion 7); adding Garmin changes 0 lines in `scripts/ingest/ingest.py` and `scripts/ingest/adapter.py` (`git diff --numstat <pre-garmin> -- scripts/ingest/ingest.py scripts/ingest/adapter.py`, expect 0, criterion 3); the simulated export-format field-rename re-validation re-derives the dedupe key with 0 shared-routine edits — `git diff --numstat <pre-format-rename> -- scripts/ingest/ingest.py scripts/ingest/adapter.py` (a baseline distinct from the Garmin criterion-3 diff; expect 0 changed lines, ADR-0003-T2 criterion 6); Whoop is registered-but-unwired (`rg "whoop" scripts/ingest/scheduler.py` returns 0 invocation references, criterion 5).
- `pytest tests/generate/test_render.py` passes including the matrix/projection cases (ADR-0004-T2 criterion 6); the worst-case matrix+projection over the `ADR-0004-T0` dataset is < 500000 bytes (`wc -c`, criterion 1); an over-cap dataset paginates to ≥2 files each < 500000 bytes (criterion 2); the egress guard observes 0 outbound calls and 0 lab/answer to model (criterion 5).
- `pytest tests/generate/test_generate.py` passes (ADR-0004-T3 criterion 6); `generate.run` produces the file and exits 0 with stdin closed and 0 sockets bound (criteria 1-3); the produced file opens offline with 0 outbound requests (criterion 4).
- `pytest tests/clone/test_init_instance.py` passes (ADR-0005-T2 criterion 6); a fresh clone reaches a fillable PII-free instance (criterion 1); entered data is untracked (criterion 2); `docs/clone-init.md` contains "From git clone to a fillable instance" (criterion 4); the egress guard over `init_instance.run` observes 0 outbound calls (criterion 5).
- `pytest tests/plan/test_router.py` passes (ADR-0006-T1 criterion 6); `router.summarize` returns only the `ADR-0006-T0` field-set (criterion 1); `router.dispatch` routes to the no-train lane (criterion 2), carries 0 raw-PII to the model (criterion 3), and raises on an injected raw-PII field (criterion 4); reads only through the store API (criterion 5).
- **Verifier:** QA, with Security sign-off on `ADR-0006-T1` (the no-train router / raw-PII enforcement).

**Wall-clock estimate:** 3 days (`ADR-0003-T2` is the longer task).

---

### Wave 5: Scheduler, Multi-Domain Plan Assembly

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0003-T3 | Unattended Scheduler Run (Delta-Since-Last-Run) | SE | 1 day |
| ADR-0006-T2 | Multi-Domain Plan Assembly — Routing, Composition, Attribution, Sourcing, Coverage Gaps | SE + Security review | 2-2.5 days |

**Entry Criteria:**
- Wave 4 checkpoint passed (wired adapters green for the scheduler; router implementation green — `ADR-0006-T2` consumes the `ADR-0006-T1` router summary; generation engine green — the plan renders through `ADR-0004-T1`).

**Exit Criteria / Checkpoint:**
- `pytest tests/ingest/test_scheduler.py` passes (ADR-0003-T3 criterion 7); a second `scheduler.run` appends only new-timepoint readings (criterion 2) and a no-new-readings run appends 0 lines (criterion 3); Whoop is not invoked (criterion 4); the egress guard over `scheduler.run` observes 0 outbound calls (criterion 5).
- `pytest tests/plan/test_assemble.py` passes (ADR-0006-T2 criterion 10); exactly one attributed section per in-scope domain, 0 unattributable (criterion 1); every recommendation carries source + tier + reversibility, 0 incomplete (criterion 2); animal-grounded recommendations carry a population-mismatch flag (criterion 3); thin-library and no-specialist domains render a stated coverage-gap, 0 fabricated regimens (criteria 4-5); composition introduces 0 unsourced cross-domain claims (criterion 6); assembly reasons only over the `ADR-0006-T1` router summary and the egress guard observes 0 raw-PII sends (criterion 7); each section reflects ≥1 operator-specific input (criterion 8); 0 recommendations contradict a stated hard limit — HALT honored (criterion 9).
- **Verifier:** QA, with Security sign-off on `ADR-0006-T2` (criterion 7 PII boundary + criterion 9 HALT/hard-limit safety).

**Wall-clock estimate:** 2.5 days (`ADR-0006-T2` is the longer task).

---

### Wave 6: Lab-Loop / Watch-Out / Physician-Feedback Store Schemas

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0007-T1 | Lab-Loop / Watch-Out / Physician-Feedback Store Schemas | SE | 1-1.5 days |

**Entry Criteria:**
- Wave 5 checkpoint passed (`ADR-0006-T2` plan assembly green — the lab loop's input edge is downstream of plan assembly, which recommends the bloodwork the loop ingests).

**Exit Criteria / Checkpoint:**
- `pytest tests/store/test_loop_schema.py` passes (ADR-0007-T1 criterion 7); a recommended-but-undrawn panel persists as "pending" across a generation cycle (criterion 1); unanswered check-ins read "not yet answered" and a single-timepoint biomarker reads "no prior" (criterion 2); a watch-out answer and a physician-feedback entry are read on the next generation (criteria 3-4); the watch-out question set derives from active protocols with 0 automated signal detection (`rg` over `loop_schema.py` returns 0 threshold-evaluation step, criterion 5); the egress guard over a store/read cycle observes 0 outbound calls (criterion 6).
- **Verifier:** QA.

**Wall-clock estimate:** 1.5 days.

---

### Wave 7: Biomarker-Matrix + Projection Render-Time Views

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0007-T2 | Biomarker-Matrix + Projection Render-Time Views | SE | 1-1.5 days |

**Entry Criteria:**
- Wave 6 checkpoint passed (`ADR-0007-T1` store-schema states green — the render views read them). Generation engine (`ADR-0004-T1`) and the cap (`ADR-0004-T0`) from earlier waves remain green.

**Exit Criteria / Checkpoint:**
- `pytest tests/generate/test_render_views.py` passes (ADR-0007-T2 criterion 7); a ≥2-timepoint biomarker renders side-by-side in the matrix (criterion 1); a projection renders only at ≥3 timepoints and is trend-only at 2 (criterion 2) with the "naive projection" label + method + count + widening band + milestones (criterion 3); pending / not-yet-answered map 1:1 from the `ADR-0007-T1` store state (criterion 4, the cross-boundary integration check); the recompute is local-only with 0 external requests and 0 lab/answer to model (criterion 5); a worst-case view paginates so each artifact is < 500000 bytes (`wc -c`, criterion 6).
- **Verifier:** QA.

**Wall-clock estimate:** 1.5 days.

## Agent Assignment Matrix

Every build task is a software task. The three `[Spike]` reports are design-level (they name mechanisms / schemas / caps and produce no code) → Architect. Implementation scripts → SE. Tasks touching the PII/egress/no-train boundary or the gitignore/content-scan trust boundary or the HALT safety filter → SE with Security review (per heuristic Decision Rule 1: security wins ties). No task is assigned two primary agents; "SE + Security review" is one primary (SE) plus a reviewer.

**SEC-02 egress-boundary Security-review de-scoping (documented, not silent).** `ADR-0004-T1`, `ADR-0004-T2`, `ADR-0007-T1`, and `ADR-0007-T2` each carry a 0-egress / 0-PII-to-model criterion, which by the rule above would read as "SE + Security review." They are deliberately NOT assigned Security review: the egress-boundary Security audit is performed once, at `ADR-0001-T1` (the guard's build + audit). These four render/store tasks CONSUME the already-audited guard (`scripts/guard/egress_guard.py`) and implement no new egress control of their own — they wrap their code path in the existing guard. Per-render/-store Security review is therefore not assigned. The residual risk (the guard's coverage of the NEW code paths these tasks introduce — subprocess/async render and store/read cycles) is closed not by a sign-off but by the failing-capable cross-spec egress checks added at W4→5 and W6→7 per SEC-03 (a synthetic outbound call injected into a render / init / store cycle must drive the guard to FAIL). This de-scoping is recorded here and in the Risk Schedule "Security-sensitive ordering" subsection so the absence is explicit, not an oversight.

| Task ID | Agent | Rationale |
|---------|-------|-----------|
| ADR-0001-T0 | Architect | Design-level spike: selects the data-in PII-boundary enforcement mechanisms (egress capture, PII scan, no-raw-to-model rule); affects the architecture, produces a report not code. |
| ADR-0002-T0 | Architect | Design-level spike: fixes the store file layout, (item, timepoint) key, and NDJSON field set; an architecture-shaping decision report, no code. |
| ADR-0004-T0 | Architect | Design-level spike: measures worst-case render size and produces the cap/pagination parameter; architecture trade-off (D4↔D7), report not code. |
| ADR-0002-T1 | SE | Core implementation: NDJSON store append/read library + `keying.py` + the gitignore entry and its unit tests. |
| ADR-0001-T1 | SE + Security review | Implementation of the egress guard + tracked-file PII scan — the PII trust boundary; SE implements, Security audits the no-egress / no-committed-PII enforcement. |
| ADR-0003-T1 | SE | Core implementation: shared ingestion routine, adapter interface, dedupe against the shared key, manual-entry fallback, and unit tests. |
| ADR-0004-T1 | SE | Core implementation: generation engine + inline-CSS/SVG template component library (dashboard, report) and render unit tests. |
| ADR-0005-T1 | SE + Security review | Implementation of the PII-free-trunk gitignore boundary + pre-commit content-scan hook — the trunk distribution trust boundary; SE implements, Security audits the content-scan enforcement. |
| ADR-0006-T0 | Architect | Design-level spike: fixes the plan-reasoning summary field-set + derivation and selects the no-train routing-enforcement mechanism; architecture-shaping PII-boundary design, report not code. |
| ADR-0003-T2 | SE | Core implementation: HealthKit/Oura/Garmin/Whoop adapters + the 0-shared-routine-edit extensibility proof and adapter tests. |
| ADR-0004-T2 | SE | Core implementation: extends the render engine for the asset-heavy matrix/projection artifact under the spike cap, with pagination and shared-markup. |
| ADR-0004-T3 | SE | Core implementation: on-demand + cron generation entry point invoking the render path; config-/entry-point implementation, no daemon. |
| ADR-0005-T2 | SE | Core implementation: clone-init step + operator-facing README so a fresh clone reaches a fillable PII-free instance. |
| ADR-0006-T1 | SE + Security review | Implementation of the no-train router + summary derivation — the raw-PII-off-the-model enforcement; SE implements, Security audits the no-train-lane routing and raw-PII rejection. |
| ADR-0003-T3 | SE | Core implementation: unattended scheduler entry point with delta-since-last-run append and idempotent re-run, plus tests. |
| ADR-0006-T2 | SE + Security review | Implementation of multi-domain plan assembly; SE implements, Security audits the no-train PII boundary (criterion 7) and the HALT / hard-limit safety filter (criterion 9). |
| ADR-0007-T1 | SE | Core implementation: lab-loop / watch-out / physician-feedback store schemas writing through the store API, with question derivation and no signal automation. |
| ADR-0007-T2 | SE | Core implementation: render-time matrix + projection view builders reading the loop-schema state and applying the render cap. |

**Tally:** SE — 11 (ADR-0002-T1, ADR-0003-T1, ADR-0004-T1, ADR-0003-T2, ADR-0004-T2, ADR-0004-T3, ADR-0005-T2, ADR-0003-T3, ADR-0007-T1, ADR-0007-T2 = 10 plain SE; plus the SE-primary of the 4 review-paired tasks). Architect — 4 (the four spikes; ADR-0006-T0 is the spike, Architect-owned, not a builder). SE + Security review — 4 (ADR-0001-T1, ADR-0005-T1, ADR-0006-T1, ADR-0006-T2). QA — verifier at every wave checkpoint (no standalone QA-owned build task; both specs fold integration/E2E assertions into each task's own test file, which the SE author writes and QA verifies at the checkpoint). Net: 14 SE-primary build tasks (10 plain + 4 Security-paired) + 4 Architect spikes = 18.

## Checkpoint Protocol

A checkpoint sits at every wave boundary. Each names the test command(s), the acceptance criteria verified (by task ID + criterion number), the artifacts that must exist (by path), a go/no-go rule, and the verifier role. Criteria derive from each completing task's Test Strategy entry + acceptance criteria. Cross-spec integration checks are added at the boundaries the analysis §6 names: the egress guard (`ADR-0001-T1`) green before every data-out 0-egress task; the store read model (`ADR-0002-T1`) green before every data-out store-reader.

### Wave 1 → Wave 2 Boundary

- **Tests:** `test -f docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md && test -f docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md && test -f docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md`; section-presence checks via `rg "^## " <each spike file>`.
- **Acceptance Criteria Verified:** ADR-0001-T0 criteria 1-6; ADR-0002-T0 criteria 1-6; ADR-0004-T0 criteria 1-7.
- **Artifacts Present:** `docs/spec/.pipeline/spike-ADR-0001-T0-pii-boundary.md`, `docs/spec/.pipeline/spike-ADR-0002-T0-store-keying.md`, `docs/spec/.pipeline/spike-ADR-0004-T0-render-size.md`.
- **Go/No-Go:** All three reports present; each names exactly one selected mechanism / key tuple / cap value (not a list); ADR-0004-T0 Measured Size is a recorded byte number. Any "list of options" instead of a single selection is a no-go (the downstream build target is undefined).
- **Verifier:** Architect.

### Wave 2 → Wave 3 Boundary

- **Tests:** `pytest tests/store/test_store.py tests/store/test_keying.py tests/guard/test_egress_guard.py tests/guard/test_pii_scan.py`; `git check-ignore vault/store/x.ndjson`.
- **Acceptance Criteria Verified:** ADR-0002-T1 criteria 1-7; ADR-0001-T1 criteria 1-5.
- **Artifacts Present:** `scripts/store/store.py`, `scripts/store/keying.py`, `scripts/guard/egress_guard.py`, `scripts/guard/pii_scan.py`, `.gitignore` (with `vault/store/`), `tests/store/test_store.py`, `tests/store/test_keying.py`, `tests/guard/test_egress_guard.py`, `tests/guard/test_pii_scan.py`.
- **Cross-spec integration check (enforcement-first guard):** the egress guard fails on an injected outbound call and the PII scan fails on a planted token — the guard is genuinely failing-capable, not a no-op — before any data-out task (all Wave 3+) is allowed to consume it.
- **SEC-01(a) reuse-contract assertion (shared-scanner signature):** `python3 -c "from scripts.guard.pii_scan import scan; assert callable(scan); n = scan([]); assert isinstance(n, int)"` exits 0 — `scripts/guard/pii_scan.py` exposes `scan(tracked_files)` as an importable function returning a hit count (the exact signature ADR-0005-T1's hook will call cross-spec). This is a positive assertion on the published surface, not merely that `pii_scan`'s own unit tests pass — it guarantees the downstream hook has a real shared scanner to route through.
- **Go/No-Go:** All tests pass, all artifacts present, the guard is failing-capable, `pii_scan.scan(tracked_files)` is importable and returns a hit count, `vault/store/` is gitignored, no blocking defects.
- **Verifier:** QA; Security signs off on `ADR-0001-T1`.

### Wave 3 → Wave 4 Boundary

- **Tests:** `pytest tests/ingest/test_ingest.py tests/generate/test_render.py`; `bash tests/hooks/test_block_pii_commit.sh`; `rg "def .*key" scripts/ingest/` (expect 0 independent key functions); `git check-ignore <a filled-scaffold-value path>`; `test -f docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md`.
- **Accessibility / color-vision-safety checkpoint item (ADR-0004-T1 criterion 3):** `pytest tests/generate/test_render.py::test_contrast_and_colorblind` — the go/no-go requires the contrast and color-distance assertions report **measured numeric values** (an AA contrast ratio and a per-adjacent-pair color-distance above the stated deuteranopia/protanopia threshold under the simulated color-vision transform) plus a present `@media print` block; a `assert True` placeholder reporting no computed value is a no-go.
- **Acceptance Criteria Verified:** ADR-0003-T1 criteria 1-7; ADR-0004-T1 criteria 1-7; ADR-0005-T1 criteria 1-7; ADR-0006-T0 criteria 1-6.
- **Artifacts Present:** `scripts/ingest/ingest.py`, `scripts/ingest/adapter.py`, `scripts/generate/render.py`, `vault/design/templates/component_set.py`, `vault/design/templates/dashboard.py`, `vault/design/templates/report.py`, `.claude/hooks/block-pii-commit.sh`, `.gitignore` (extended), `docs/spec/.pipeline/spike-ADR-0006-T0-summary-router.md`, and their test files.
- **Cross-spec integration check:** each data-out task (`ADR-0004-T1`, `ADR-0005-T1`) ran green only with the Wave-2 egress guard (`scripts/guard/egress_guard.py`) and store read model (`scripts/store/store.py`/`keying.py`) present — the render's 0-egress (ADR-0004-T1 criterion 5) and the hook's reuse of `pii_scan.scan` (ADR-0005-T1 criteria 2, 5) confirm the cross-spec wiring.
- **SEC-01(b) adversarial reuse-contract check (no parallel bash reimplementation):** with `scripts/guard/pii_scan.py`'s `scan` stubbed to return 0 (monkeypatched in the test), `block-pii-commit.sh` FAILS to block a commit that stages a planted PII token — i.e. the hook's block decision flips with the shared scanner's verdict. This proves the hook routes through ADR-0001-T1's shared `pii_scan.scan` rather than a parallel bash reimplementation of the token scan (Spec B ADR-0005-T1 criteria 2, 5). If the hook still blocks the planted token while `scan` returns 0, the hook has a private scanner and the reuse contract is violated — a no-go.
- **Go/No-Go:** All tests pass, all artifacts present, the ingestion routine references no second key definition, the router spike names exactly one enforcement mechanism, no blocking defects.
- **Verifier:** QA; Security signs off on `ADR-0005-T1`; Architect verifies the `ADR-0006-T0` spike.

### Wave 4 → Wave 5 Boundary

- **Tests:** `pytest tests/ingest/test_adapters.py tests/generate/test_render.py tests/generate/test_generate.py tests/clone/test_init_instance.py tests/plan/test_router.py`; `git diff --numstat <pre-garmin> -- scripts/ingest/ingest.py scripts/ingest/adapter.py` (the Garmin 0-edit proof, ADR-0003-T2 criterion 3; expect 0); `git diff --numstat <pre-format-rename> -- scripts/ingest/ingest.py scripts/ingest/adapter.py` (the format-rename re-validation 0-edit proof against its own distinct baseline, ADR-0003-T2 criterion 6; expect 0).
- **Acceptance Criteria Verified:** ADR-0003-T2 criteria 1-7; ADR-0004-T2 criteria 1-6; ADR-0004-T3 criteria 1-6; ADR-0005-T2 criteria 1-6; ADR-0006-T1 criteria 1-6.
- **Artifacts Present:** `scripts/ingest/adapters/healthkit.py`, `scripts/ingest/adapters/oura.py`, `scripts/ingest/adapters/garmin.py`, `scripts/ingest/adapters/whoop.py`, `scripts/generate/generate.py`, `scripts/clone/init_instance.py`, `docs/clone-init.md`, `scripts/plan/router.py`, and their test files (`render.py` extended in place).
- **Cross-spec integration check (enforcement-first):** `ADR-0006-T1` (the no-train router) is green BEFORE Wave 5 lets `ADR-0006-T2` reason over PII — the router's no-train-lane routing (criterion 2) and raw-PII rejection (criterion 4) are verified here; the egress guard over `ADR-0004-T2` / `ADR-0005-T2` confirms 0 egress.
- **SEC-03 failing-capable egress check (new guard-consuming code paths):** beyond the happy-path "guard observes 0 calls," inject a synthetic outbound call into one `ADR-0004-T2` render path and one `ADR-0005-T2` `init_instance.run` and assert the egress guard returns FAIL (non-zero) on each — proving the guard actually intercepts these new code paths (subprocess- and async-spawned calls included), not merely that a clean run happens to make 0 calls. This generalizes the W2→3 failing-capable assertion to every wave that introduces a new guard-consuming code path; a guard that does NOT flip to FAIL on the injected call is a no-go.
- **Go/No-Go:** All tests pass, all artifacts present, Garmin 0-edit proof holds, the router rejects an injected raw-PII field, no blocking defects.
- **Verifier:** QA; Security signs off on `ADR-0006-T1`.

### Wave 5 → Wave 6 Boundary

- **Tests:** `pytest tests/ingest/test_scheduler.py tests/plan/test_assemble.py`; `git diff --numstat <pre-add> -- scripts/ingest/scheduler.py` (expect 0).
- **Acceptance Criteria Verified:** ADR-0003-T3 criteria 1-7; ADR-0006-T2 criteria 1-10.
- **Artifacts Present:** `scripts/ingest/scheduler.py`, `scripts/plan/assemble.py`, `tests/ingest/test_scheduler.py`, `tests/plan/test_assemble.py`.
- **Cross-spec integration check:** `ADR-0006-T2` consumes only the `ADR-0006-T1` router summary (criterion 7) and the egress guard observes 0 raw-PII sends — the plan-reasoning-over-PII path runs entirely behind the router built in Wave 4.
- **Go/No-Go:** All tests pass; the assembled plan is 100% attributed + sourced, coverage-gap-honest, and HALT-safe (criterion 9: 0 recommendations contradict a stated hard limit). Population-mismatch is asserted adversarially, parallel to HALT: the test plants an animal-grounded recommendation with NO population-mismatch flag and asserts the plan FAILS (ADR-0006-T2 criterion 3 is failing-capable — an unflagged animal→human extrapolation breaks the test), not merely that a flag appears on an already-flagged input. Health-domain safety control. No blocking defects.
- **Verifier:** QA; Security signs off on `ADR-0006-T2` (PII boundary + HALT safety).

### Wave 6 → Wave 7 Boundary

- **Tests:** `pytest tests/store/test_loop_schema.py`; `rg "threshold\|detect" scripts/store/loop_schema.py` (expect 0 automated-detection step).
- **Acceptance Criteria Verified:** ADR-0007-T1 criteria 1-7.
- **Artifacts Present:** `scripts/store/loop_schema.py`, `tests/store/test_loop_schema.py`.
- **Cross-spec integration check:** the loop schemas write through the cross-spec store API (`scripts/store/store.py`) and the egress guard over a store/read cycle observes 0 outbound calls (criterion 6) — the store states the Wave-7 render views will read are fixed and PII-bounded here.
- **SEC-03 failing-capable egress check (new guard-consuming code path):** inject a synthetic outbound call into one `ADR-0007-T1` store/read cycle and assert the egress guard returns FAIL (non-zero) — proving the guard intercepts the loop-schema store path (subprocess/async included), not merely that a clean cycle makes 0 calls. The W7→Done `ADR-0007-T2` render-view path is covered by the same failing-capable check at that boundary (a synthetic outbound call injected into a `render_views` recompute must drive the guard to FAIL); a guard that does NOT flip to FAIL is a no-go.
- **Go/No-Go:** All tests pass; pending / not-yet-answered / no-prior states are defined and persist; 0 signal automation; no blocking defects.
- **Verifier:** QA.

### Wave 7 → Done

- **Tests:** `pytest tests/generate/test_render_views.py`; `wc -c <each rendered view file>` (expect < 500000 each); regression: `pytest` over the full suite.
- **Acceptance Criteria Verified:** ADR-0007-T2 criteria 1-7.
- **Artifacts Present:** `scripts/generate/render_views.py`, `tests/generate/test_render_views.py`.
- **Cross-spec integration check (2-decision contract):** `ADR-0007-T2` criterion 4 maps the `ADR-0007-T1` store states (pending / not-yet-answered) 1:1 to rendered states — the cross-boundary integration test that closes the store-schema-vs-render-view contract; the render applies the `ADR-0004-T0` cap (criterion 6).
- **SEC-03 failing-capable egress check (render-view code path):** inject a synthetic outbound call into one `render_views` recompute and assert the egress guard returns FAIL (non-zero) — proving the guard intercepts the `ADR-0007-T2` render-view path (subprocess/async included), not merely that a clean recompute makes 0 calls (the W7→Done leg of the SEC-03 generalization noted at W6→7); a guard that does NOT flip to FAIL is a no-go.
- **Go/No-Go:** All tests pass; the matrix/projection views map store state 1:1, stay under 500KB, and make 0 outbound calls; full-suite regression green; plan execution complete.
- **Verifier:** QA.

## Critical Path

Computed via CPM forward/backward pass (wave-scheduling §2) over the merged DAG with files × criteria upper-bound durations (spikes +0.5). The analysis §3 named a node-count-7 seed (`ADR-0001-T0 → ADR-0001-T1 → ADR-0006-T0 → ADR-0006-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2`); independent verification finds that chain is NOT the duration-critical path — it carries positive slack at `ADR-0001-T1`, `ADR-0006-T0`, and `ADR-0006-T1` (each 0.5 day). The duration-critical path runs through the store→generation→assembly spine, where `ADR-0002-T1` (3 days), `ADR-0004-T1` (3 days), and `ADR-0006-T2` (2.5 days) dominate. Two tied zero-slack paths converge at `ADR-0002-T1`:

```
Path A: ADR-0001-T0 → ADR-0002-T1 → ADR-0004-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2
Path B: ADR-0002-T0 → ADR-0002-T1 → ADR-0004-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2
```

Both span 6 tasks and 13.0 task-days. They diverge only at the Wave-1 entry spike (`ADR-0001-T0` vs `ADR-0002-T0`, both 1.5 days, both zero-slack) and converge at `ADR-0002-T1`. A delay on either entry spike, or on any shared node, delays the plan.

- **Length:** 6 tasks (Waves 1, 2, 3, 5, 6, 7 — the path skips Wave 4 because `ADR-0006-T2` in Wave 5 depends on `ADR-0004-T1` in Wave 3, not on any Wave-4 task).
- **Zero-slack tasks:** ADR-0001-T0, ADR-0002-T0, ADR-0002-T1, ADR-0004-T1, ADR-0006-T2, ADR-0007-T1, ADR-0007-T2 (7 tasks across the two tied paths).
- **Non-critical tasks with slack (CPM total float, days):**
  - ADR-0001-T1: 0.5 day slack (Wave 2; successor chain through the router is shorter than the store spine).
  - ADR-0006-T0: 0.5 day slack (Wave 3; the spike's downstream chain has float).
  - ADR-0006-T1: 0.5 day slack (Wave 4).
  - ADR-0003-T1: 2.5 days slack (Wave 3; the ingestion spine is shorter than the generation spine).
  - ADR-0003-T2: 2.5 days slack (Wave 4).
  - ADR-0003-T3: 2.5 days slack (Wave 5; leaf of the ingestion spine).
  - ADR-0004-T2: 3.5 days slack (Wave 4; leaf render — ES 7.5 / EF 9.5 / LS 11.0 / LF 13.0, dur 2.0, total float = LS − ES = 11.0 − 7.5 = 3.5; gated by `ADR-0004-T1`'s EF on the store→generation spine, latest finish bounded by the 13.0 makespan).
  - ADR-0004-T3: 4.5 days slack (Wave 4; isolated cron entry leaf).
  - ADR-0005-T1: 5.0 days slack (Wave 3; the gitignore-boundary spine is the shortest).
  - ADR-0005-T2: 5.0 days slack (Wave 4; leaf of the gitignore spine).
  - ADR-0004-T0: 10.0 days slack (Wave 1; its cap is consumed late, in Waves 4 and 7, so it has the most float).

## Risk Schedule

### Spikes

- **ADR-0001-T0** (PII-boundary design) — **Wave 1.** No dependencies; zero-slack entry. Correct Wave-1 placement.
- **ADR-0002-T0** (store-keying design) — **Wave 1.** No dependencies; zero-slack entry. Correct Wave-1 placement.
- **ADR-0004-T0** (render-size measurement) — **Wave 1.** No dependencies (analysis §5c). Correct Wave-1 placement; its cap is consumed downstream in Waves 4 and 7.
- **ADR-0006-T0** (no-train router design) — **Wave 3.** NOT Wave 1. This is the documented justified exception (5a, resolved below).

### 5a resolution — ADR-0006-T0 placed in Wave 3 as a justified exception (option i)

**Decision: keep both cross-spec edges and document `ADR-0006-T0`'s non-Wave-1 placement as a justified exception** (analysis §5a option i; wave-scheduling §6 spike exception, inverted).

Independence test (wave-scheduling §3 Rule 1) applied to BOTH edges:

- **Edge `ADR-0001-T0 → ADR-0006-T0` is REAL, not phantom.** `ADR-0006-T0`'s "Routing-Enforcement Mechanism" section (criterion 4) must name a mechanism "building on the data-in egress guard." The router-enforcement design is the plan-reasoning extension of the same PII-boundary the `ADR-0001-T0` spike selects — it reasons over which mechanism the egress guard uses. A router spike that names an enforcement mechanism built on an egress-capture mechanism that has not yet been selected would be naming a mechanism over a void. The edge carries the selected egress mechanism (a design artifact, available at `ADR-0001-T0` completion), so the two spikes cannot share Wave 1: `ADR-0006-T0` consumes `ADR-0001-T0`'s recommendation.
- **Edge `ADR-0001-T1 → ADR-0006-T0` is REAL, not phantom — but is the load-bearing one for the exception.** A design spike that merely *names* a planned mechanism could, in principle, reference the planned guard from the `ADR-0001-T0` report without the *built* `egress_guard.py`. However, `ADR-0006-T0` criterion 4 cites `scripts/guard/egress_guard.py` by path and criterion 5 requires a "Falsifiable Check" that "returns a pass/fail result" — a falsifiable check that fails on a raw-PII send is only specifiable as falsifiable against the built guard's observed behavior, not against a paper plan. The router spike's enforcement design is the plan-reasoning extension of the implemented data-in boundary; it legitimately builds on the implemented guard. This is the enforcement-first chain itself: the V1 PII critical-path guard is built (data-in, `ADR-0001-T1`) before its plan-reasoning extension is even designed.

**Why this is an exception and not a BP-05 violation (and not a spec defect).** Per wave-scheduling §6, a tier-5 spike that *genuinely depends on* tier-1/3 output does not qualify for the Wave-1 exception. `ADR-0006-T0` genuinely depends on the data-in PII-boundary foundation. This is the correct structural shape, not a phantom edge to remove (option ii rejected — the `ADR-0001-T1` edge is real per the falsifiable-check analysis above) and not a spike-that-is-really-a-follow-up-task (option iii rejected — `ADR-0006-T0` produces a report, names a mechanism, and runs no implementation; it is a true spike, just one that builds on prior output). The placement at Wave 3 (topological depth 3, after `ADR-0001-T1` lands in Wave 2) is the justified exception.

### 5b — Enforcement-first invariant (HARD, V1 PII critical-path guard)

This ordering is non-negotiable and holds in the final schedule:

- **No plan-reasoning-over-PII task precedes the router spike + impl.** `ADR-0006-T0` (Wave 3, spike) → `ADR-0006-T1` (Wave 4, impl) → `ADR-0006-T2` (Wave 5, assembly) and `ADR-0006-T2` (Wave 5) is the only assembly task — both `ADR-0006-T1` and `ADR-0006-T2` are strictly after the router spike, and `ADR-0006-T2` is strictly after the router impl. No PII-reasoning task runs before the router is specced AND built. This is the V1 PII critical-path guard.
- **No data-out 0-egress / 0-PII task precedes the guard `ADR-0001-T1`.** `ADR-0001-T1` lands in Wave 2. Every data-out task carrying a 0-egress / 0-raw-PII criterion (`ADR-0004-T1`, `ADR-0004-T2`, `ADR-0005-T1`, `ADR-0005-T2`, `ADR-0006-T1`, `ADR-0006-T2`, `ADR-0007-T1`, `ADR-0007-T2`) lands in Wave 3 or later — strictly after the guard. The Wave 2→3 checkpoint asserts the guard is failing-capable before any of them is allowed to consume it.

### Risk-mitigating-before-protected ordering

- **The PII egress guard + PII scan (`ADR-0001-T1`, Wave 2) precede every 0-egress / 0-PII task** (Waves 3-7) — verified above (5b).
- **The render-size spike (`ADR-0004-T0`, Wave 1) precedes the asset-heavy renders** `ADR-0004-T2` (Wave 4) and `ADR-0007-T2` (Wave 7) — the cap is measured before any render consumes it.
- **The router spike + impl (`ADR-0006-T0` Wave 3, `ADR-0006-T1` Wave 4) precede plan assembly (`ADR-0006-T2`, Wave 5)** — the no-train enforcement is built before any plan reasons over operator state.
- **The store-keying spike (`ADR-0002-T0`, Wave 1) precedes the store library + dedupe (`ADR-0002-T1` Wave 2, `ADR-0003-T1` Wave 3)** — the (item, timepoint) key is fixed before the store and ingestion implement it.

### Security-sensitive ordering

The four security-reviewed tasks land in dependency order with Security review in the same wave as the implementation (never deferred): `ADR-0001-T1` (Wave 2, the foundational PII/egress boundary) → `ADR-0005-T1` (Wave 3, the trunk content-scan boundary, reusing `ADR-0001-T1`'s `pii_scan.scan`) → `ADR-0006-T1` (Wave 4, the no-train router) → `ADR-0006-T2` (Wave 5, plan assembly with the HALT/hard-limit safety filter). The PII boundary is fully in place before any task reasons over operator state.

**SEC-02 de-scoping — `ADR-0004-T1` / `ADR-0004-T2` / `ADR-0007-T1` / `ADR-0007-T2` carry a 0-egress / 0-PII-to-model criterion but get NO Security review (documented).** The egress-boundary Security audit is performed once at `ADR-0001-T1` (the guard's build + audit). These four render/store tasks consume the already-audited guard and implement no new egress control — so per-render / per-store Security review is not assigned. The residual (the guard's coverage of the NEW code paths these tasks introduce) is closed by the failing-capable cross-spec egress checks added at W4→5 and W6→7 per SEC-03, not by a sign-off. Recorded in the Agent Assignment Matrix preamble and here so the absence is explicit, not silent.

## Cross-Spec Coordination

This is a two-spec plan (data-in tier 3 + data-out tier 5). The data-out spec's cross-spec references to data-in tasks are real intra-plan edges here (the data-in tasks are authored in Spec A and built in this same plan).

### Shared-file ordering: `.gitignore` (the only cross-spec file overlap)

| Conflict | Spec A Task | Spec B Task | Resolution |
|----------|------------|------------|------------|
| `.gitignore` | ADR-0002-T1 (Wave 2, **adds** `vault/store/`) | ADR-0005-T1 (Wave 3, **extends** with filled-scaffold-value exclusions) | Ordered create-then-extend, NOT a BP-07 collision. The cross-spec edge `ADR-0002-T1 → ADR-0005-T1` already sequences them (Wave 2 before Wave 3); Spec B `ADR-0005-T1` text says "extending the data-in entry." No same-wave overlap, no conflict. |

No other cross-spec file overlap. `scripts/store/loop_schema.py` (ADR-0007-T1) is a new file in the shared `scripts/store/` directory, distinct from `store.py`/`keying.py`. `scripts/generate/render.py` appears in `ADR-0004-T1` (create, Wave 3) and `ADR-0004-T2` (modify, Wave 4), but that is intra-Spec-B and already ordered by the `ADR-0004-T1 → ADR-0004-T2` edge.

### Tier ordering

Spec A = tier 3, Spec B = tier 5. The merged graph uses the explicit declared cross-spec edges (more precise than blanket tier ordering, per wave-scheduling §6). No tier-5 task precedes a tier-3 task it depends on (Kahn respects every edge). The one tier-5 spike with no tier-3 dependency, `ADR-0004-T0`, sits in Wave 1 alongside the tier-3 spikes — the legitimate §6 spike exception. The other tier-5 spike, `ADR-0006-T0`, does NOT qualify for that exception (it genuinely depends on the tier-3 PII foundation) and is placed in Wave 3 per the 5a resolution.

### Merged cross-spec dependency edges (analysis §2)

These 18 data-in → data-out edges are real intra-plan edges (not blanket tier ordering):
- `ADR-0001-T0 → ADR-0006-T0`; `ADR-0001-T1 → ADR-0006-T0` (router spike builds on the PII boundary).
- `ADR-0002-T1 → {ADR-0004-T1, ADR-0005-T1, ADR-0004-T2, ADR-0005-T2, ADR-0006-T1, ADR-0006-T2, ADR-0007-T1, ADR-0007-T2}` (store read model consumed by every data-out store-reader).
- `ADR-0001-T1 → {ADR-0004-T1, ADR-0005-T1, ADR-0004-T2, ADR-0005-T2, ADR-0006-T1, ADR-0006-T2, ADR-0007-T1, ADR-0007-T2}` (egress guard consumed by every data-out 0-egress task).

The plan's `ADR-0002-T1` fan-out is intentionally a superset of Spec B's literal Dependency Map (line 329, which gives `ADR-0002-T1` only 5 explicit targets and omits `ADR-0005-T1`, `ADR-0004-T2`, `ADR-0006-T2`): the union captures the transitive store-read dependencies those tasks carry (`ADR-0006-T2` reads the store via the `ADR-0006-T1` router; `ADR-0005-T1` / `ADR-0004-T2` consume the store read model), introduces 0 wave-order violations (every added edge still points to a later wave), and is recorded here for the same reason as the logged `ADR-0001-T1 → ADR-0006-T0` spec-map gap.

**Complement, not an edge:** `ADR-0004-T3` (cron entry point) names `ADR-0003-T1` as a complement that "is not a prerequisite — generation renders manually-entered data with no importer." No edge added. `ADR-0004-T3` depends only on `ADR-0004-T1` (Wave 3), so it sits in Wave 4 — it does NOT wait on the ingestion spine.

### Merged checkpoint integration checks

At every boundary where a data-out task consumes a data-in artifact, the checkpoint asserts the cross-spec wiring is live (not just that the data-out task's own unit tests pass): the egress guard green before the data-out 0-egress tasks (Wave 2→3, 3→4, 4→5, 6→7), and the store read model green before the data-out store-readers (same boundaries). These are written into the Checkpoint Protocol above.

## Feedback Protocol

| Issue Type | Action | Blocks Plan? |
|-----------|--------|-------------|
| Spec defect (untestable criterion) | Flag for spec revision with the specific task ID + criterion number; log in `docs/build-plan/.pipeline/deviations.md` | Yes — a checkpoint cannot verify an untestable criterion |
| Missing dependency discovered | Add the edge to the wave schedule, re-run the Kahn sort + CPM pass, re-validate topological ordering; log the discrepancy for spec revision | No — the plan self-corrects |
| Acceptance criteria untestable | Flag for spec revision with the specific criterion ID and the reason it cannot be reduced to a command/file/count assertion | Yes — completion cannot be verified |
| Scope change needed | Halt, write resume state, escalate to the user | Yes — plan scope is fixed at 18 tasks |
| File manifest conflict | Flag for spec revision, name both spec paths + the conflicting file; if a true same-wave create-create on one file, add an ordering edge or split | Yes — execution order is unclear until resolved |
| Task too large for single wave | Recommend a split in `deviations.md` with the sub-task boundary, adjust the wave schedule | No — the plan accommodates (note: `ADR-0006-T2` carries 10 criteria but 2 files and one composition pass; the spec's sizing note holds it intact — not a split candidate unless execution shows the single pass is unbuildable) |
| Missing task (coverage gap) | Flag for spec revision naming the ADR section not covered by any of the 18 tasks | Yes — the plan would be incomplete |

**Defect found during this plan's creation (one, non-blocking — classified for spec revision):** Spec B's `ADR-0006-T0` task block (`docs/spec/adr-0004-adr-0007-spec.md` line 102) names cross-spec deps `ADR-0001-T0` AND `ADR-0001-T1`, but Spec B's Dependency Map cross-spec section (line 329) routes only the `ADR-0001-T0 → ADR-0006-T0` edge — it omits the `ADR-0001-T1 → ADR-0006-T0` edge. This is **non-blocking** for this plan: the plan uses the stronger ordering — `ADR-0006-T0` sits in Wave 3, strictly after `ADR-0001-T1` lands in Wave 2 (the Risk Schedule 5a resolution treats the `ADR-0001-T1 → ADR-0006-T0` edge as the load-bearing, real edge for the enforcement-first chain) — so enforcement-first holds whether or not the spec's map carries the edge. It is **classified for spec revision** (a bead will track adding the missing `ADR-0001-T1 → ADR-0006-T0` edge to Spec B's Dependency Map cross-spec section so the map matches the task block). The plan does **NOT** edit either spec file. Beyond this one discrepancy: all 18 tasks trace to a spec task; every checkpoint criterion traces to a spec acceptance criterion or Test Strategy entry; the merged DAG is acyclic (Kahn drains all 18); the only cross-spec file overlap (`.gitignore`) is an ordered create-then-extend, not a collision. The `ADR-0006-T0` Wave-3 placement is a documented justified exception (5a), not a spec defect — the spike genuinely depends on the data-in foundation and produces a report, not implementation work.

## Validation Checklist

### Wave Integrity
- [x] Every task appears in exactly one wave — all 18 tasks placed across 7 waves (3+2+4+5+2+1+1 = 18), 0 duplicates, 0 omissions, verified against the Kahn sort.
- [x] No task is scheduled in a wave before its dependency's wave — every edge in the merged edge list points from an earlier wave to a later wave (CPM forward pass confirms ES(successor) ≥ EF(predecessor) for all 40 edges).
- [x] Topological ordering respected across all waves — the wave schedule is the Kahn result of the merged 18-node graph, independently re-derived.

### Checkpoint Quality
- [x] Every wave boundary has at least one verifiable exit criterion — all 7 boundaries name a `pytest`/`test -f`/`git`/`rg`/`wc -c` command.
- [x] Every checkpoint names specific test commands or conditions — each boundary lists exact commands (not "run tests").
- [x] Every checkpoint identifies a verifier role — Architect (W1→2 boundary, spike content), QA with Security sign-off where a security-reviewed task completes (W2→3, W3→4, W4→5, W5→6), QA (W6→7, W7→Done).

### Agent Assignment
- [x] Every spec task appears in the Agent Assignment Matrix — all 18 tasks listed.
- [x] No implementation task assigned to Architect — Architect holds only the four `[Spike]` design reports; every script-writing task is SE-primary.
- [x] No interface/contract task assigned to SE without Architect review — the design-level interface/mechanism decisions ARE the spikes (Architect-owned); the SE tasks implement against those fixed contracts, no contract definition is SE-owned.
- [x] Security-sensitive tasks have Security review assigned — `ADR-0001-T1` (egress/PII guard), `ADR-0005-T1` (content-scan boundary), `ADR-0006-T1` (no-train router), `ADR-0006-T2` (PII boundary + HALT) all carry "SE + Security review".

### Critical Path
- [x] Critical path is the actual longest chain (verified by counting) — CPM forward/backward pass over the merged DAG; two tied 6-task / 13.0-day paths converging at `ADR-0002-T1`; independently disproved the analysis §3 node-count-7 seed (it carries 0.5-day slack at three nodes).
- [x] Zero-slack tasks identified — ADR-0001-T0, ADR-0002-T0, ADR-0002-T1, ADR-0004-T1, ADR-0006-T2, ADR-0007-T1, ADR-0007-T2.
- [x] No task on critical path has an alternative shorter route — both tied paths share the `ADR-0002-T1 → ADR-0004-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2` spine; the only divergence is the two equal-duration Wave-1 entry spikes.

### Risk Ordering
- [x] All spike tasks are in Wave 1 — except `ADR-0006-T0`, which is in Wave 3 as a documented justified exception (5a: it genuinely depends on the tier-1/3 PII foundation; wave-scheduling §6 inverted-exception). The other three spikes are in Wave 1.
- [x] Risk-mitigating tasks precede the tasks they protect — egress guard (W2) before every 0-egress task (W3+); render-size spike (W1) before asset-heavy renders (W4, W7); router spike+impl (W3, W4) before plan assembly (W5); store-keying spike (W1) before store + dedupe (W2, W3).
- [x] Security ordering correct — the four security-reviewed tasks land in dependency order (`ADR-0001-T1` W2 → `ADR-0005-T1` W3 → `ADR-0006-T1` W4 → `ADR-0006-T2` W5), Security review in the implementing wave; the PII boundary is in place before any plan reasons over operator state (enforcement-first, 5b).

### Spec Traceability
- [x] Every spec task appears in the wave schedule — Spec A's 7 (ADR-0001-T0/T1, ADR-0002-T0/T1, ADR-0003-T1/T2/T3) and Spec B's 11 (ADR-0004-T0/T1/T2/T3, ADR-0005-T1/T2, ADR-0006-T0/T1/T2, ADR-0007-T1/T2) all scheduled.
- [x] No task in the plan is absent from the source spec(s) — all 18 plan task IDs are spec task IDs; no invented tasks (BP-06).
- [x] `source-specs` frontmatter lists all consumed specs — both `docs/spec/adr-0001-adr-0003-spec.md` and `docs/spec/adr-0004-adr-0007-spec.md`.

### Infrastructure
- [x] Every prerequisite has a verification command — all five Wave-1 prerequisites carry a command that exits 0 on success; the wave-gated egress harness carries a command runnable once `ADR-0001-T1` builds the guard.
- [x] Wave 1 tasks do not depend on unlisted prerequisites — the three Wave-1 spikes produce reports using `python3`/`git`/`rg` only (all listed); the egress-capture harness is explicitly NOT a Wave-1 prerequisite (no Wave-1 spike runs it — BP-08 avoided), it gates Wave-2 entry.

### Feedback Protocol
- [x] Feedback protocol section is present.
- [x] Protocol covers: spec defect, missing dep, untestable criteria, scope change, file conflict, oversized task, missing task — all seven rows present.
- [x] Each issue type has a blocking/non-blocking classification — every row carries a Yes/No with rationale.
