---
scope: "ADR-0020 ADR-0021 ADR-0022 ADR-0023 ADR-0024 ADR-0025 (plan-generation engine, Tiers 1-3)"
adrs: [ADR-0020, ADR-0021, ADR-0022, ADR-0023, ADR-0024, ADR-0025]
tier: 3
created: 2026-06-24
status: approved
---

# Spec: Plan-Generation Engine (Model-Backed De-Id Envelope, Subscription Orchestrator, Quality+Safety Gates, Maintained Output)

## Component Overview

This spec implements the six approved plan-generation-engine ADRs (ADR-0020–0025) that wrap the already-built inner reconciliation+adjudication engine into a repeatable, safety-gated, end-to-end plan-generation runtime. The deliverable is the orchestration shell + the PII envelope + the review gates + the maintained output: a model-backed de-identification boundary on the way IN (ADR-0020), a deterministic PII re-insertion on the way OUT (ADR-0021), a programmatic subscription orchestrator that drives the loop unattended (ADR-0022), a post-assembly plan-quality judge (ADR-0023) and a multi-agent whole-plan safety review (ADR-0024) feeding one bounded revise loop, and a unified maintained-HTML output the orchestrator re-emits on new data (ADR-0025). The crown-jewel obligation is 0-leak: no raw operator PII past the de-id-IN boundary or into any committed file, and no re-inserted real PII into any tracked render.

The inner engine already exists and is wired — `scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track}.py`, with the ADR-0015 `ModelClient.author` seam threaded through `generate_plan._author_callable(client)` (its live `_ClaudeNoTrainBackend.author` is `NotImplementedError`, lit at the operator checkpoint) [VERIFIED against the live tree]. Per the DAG's hard EXTEND-NOT-REBUILD grounding fact, every task in this spec WRAPS or EXTENDS that engine; none re-authors `generate_plans`/`assemble`/the reconciler, and none re-introduces the model client. The orchestrator supplies the `reauthor`/`adjudicator` hooks programmatically that the S68 interactive session supplied by hand; `pipeline.run_generation` already forwards them verbatim to `generate_plans`.

How it fits the architecture: the dependency tiers (DAG §4) are Tier 1 = the PII envelope (ADR-0020 de-id IN ∥ ADR-0021 de-id OUT), Tier 2 = the runtime control surface (ADR-0022 orchestrator, depends on 0020's de-identified-summary input contract), Tier 3 = the review+output layers (ADR-0023 ∥ ADR-0024 ∥ ADR-0025, all depending only on Tiers 1-2). The RUNTIME stage order DIFFERS from the dependency tiers and is the sequence the orchestrator executes one plan through (DAG §"Runtime Stage Order"): **(1) de-id IN (0020) → (2) orchestrate/assemble (0022 + inner engine) → (3) {quality judge (0023) ∥ safety review (0024)} → (4) bounded revise loop → (5) maintained-format render (0025) → (6) de-id OUT re-insertion (0021) as the FINAL local pass over the produced HTML**. The format-then-fill ordering is load-bearing: per ADR-0021 Rationale the deterministic name fill is "the last, local, model-free pass over whatever HTML the format step produced," so the maintained render (0025) runs BEFORE re-insertion (0021). The other load-bearing divergence: ADR-0021 (de-id OUT) is Tier-1 by dependency but executes LAST at render time.

The resolved tensions are documented trade-offs, not open items. ADR-0020↔ADR-0001 (raw plan-intake PII crosses the no-train API before de-id) is accepted under bounded no-train retention reusing ADR-0016's already-adopted second-raw-egress-class posture, mitigated by the fail-closed-halt contract and the retained persisted-side `router.summarize` gate. ADR-0020/0021↔ADR-0005 (no committed/tracked PII) is held by the gitignored-only surfaces plus the `block-pii-commit.sh` + `pre-push-pii-scan.sh` hooks — whose scan-SCOPE hole on `vault/artifacts/generated/` is closed by the prerequisite T-SCANSCOPE task before any re-insertion or maintained-output task ships. The Proceed-dispositions are encoded as stated ASSUMPTIONS: the revise-loop topology (disposition #2 — a SINGLE bounded loop, both gates re-run each pass, safety findings are BLOCKING and terminal, quality findings drive revision, cap N=3 then HALT to honest no-plan), the de-id-boundary outage path (disposition #3 — fail-closed HALT to honest no-plan, never silently degrade to the coarser deterministic gate), and the dispatch-cap (disposition #4 — instrument per-plan dispatch count + a configurable fail-closed cap).

Informing research: the ADRs cite the Phase-3 DAG (`docs/adr/.pipeline/engine/dag.md`), the cross-ADR extraction (`docs/spec/.pipeline/engine/context.md`), the Phase-3 dispositions (`docs/spec/.pipeline/engine/dispositions.md`), the rubric/judge-discipline references in the skills_library, and the `~/.claude/skills/review-pr/SKILL.md` multi-lens topology — downstream workers load them on demand.

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0021 OQ-1 / ADR-0025 OQ-1 / ADR-0020 OQ-1 (RT-03) | Open Question | PII scan-SCOPE hole — `pii_scan.scan_scoped` runs the operator-name tokens only over the `data_bearing` subset, and `DATA_BEARING_PREFIXES` (`lib/pii-scan-scope.sh`) excludes `vault/artifacts/generated/`, so a committed maintained-HTML artifact carrying a re-inserted real NAME is not name-scanned by either hook. | **Block** | Crown-jewel leak guard. Build the boundary before the egress that rests on it. → prerequisite spike task **ADR-0021-T0-SCANSCOPE**, a hard dependency of every PII-re-insertion (0021) and maintained-output (0025) task. The fix extends the scan scope (`DATA_BEARING_PREFIXES` and/or `PER_SE_DENY_PREFIXES`), not merely a fixture — a fixture under the current scope still would not deny a name-bearing artifact. |
| ADR-0023 OQ-2 / ADR-0024 OQ-2 (RT-06) | Open Question (SHARED, #1 build-blocking) | Revise-loop composition topology across the quality judge (0023) and the safety review (0024) — one loop vs two; ordering; gate re-trigger rule; joint iteration cap. | **Proceed** (decided in-spec) | Rigorous topology decided as the spec's control-flow assumption: a SINGLE bounded revise loop. After assembly, run BOTH gates. SAFETY findings are BLOCKING and never overridden; a standing safety block is terminal (no plan ships). QUALITY findings drive revision. On any gate failure → one revise dispatch through the `reauthor` seam → RE-RUN BOTH gates → bounded cap **N=3** → on non-convergence HALT to honest no-plan. Encoded in ADR-0022-T2 + a falsification AC (0 plans past a standing safety block; 0 plans loop past N). |
| ADR-0020 OQ-4 (RT-09) | Open Question | De-id boundary outage for a WHOLE run — degrade to the deterministic `router.summarize` gate, or halt? | **Proceed** (fail-closed-halt) | The rigorous choice for the crown jewel: NEVER silently degrade de-id fidelity. When the de-id API boundary is unreachable for a run, the engine HALTS to the honest no-plan state; the last-good maintained artifact stays in place; no new plan is recorded. Encoded in ADR-0020-T2 AC + a falsification test (boundary-down → 0 plans recorded, honest no-plan surfaced). |
| ADR-0022 OQ-4 (RT-08) | Open Question | Aggregate dispatch volume (N specialists × revise iters + judge + M safety reviewers, per plan, daily) vs the subscription rate/usage ceiling. | **Proceed** (instrument + cap) | The spec includes a task to INSTRUMENT the per-plan dispatch count + a configurable cap that fails closed (honest no-plan / partial) on exceed, surfacing the count. The actual ceiling number is an operator/billing fact confirmed at the operator-present live-run checkpoint downstream of the mock-tested build; not a build blocker. Encoded in ADR-0022-T3. |
| DAG §6 — the 3 PII tensions (0020↔0001, 0020↔0005, 0021↔0005), marked Pending | Tension (Pending) | The crown-jewel mitigations rest on enforcement not yet re-verified against the new maintained-HTML output path. | **Proceed** (resolved via the T-SCANSCOPE task) | The tensions ARE resolved in the ADRs (mitigations documented + grounded). The "Pending" is precisely the scan-scope re-verification = ADR-0021-T0-SCANSCOPE. With it landed, the enforcement covers the new path. The re-insertion/output tasks' acceptance criteria REQUIRE T-SCANSCOPE complete + the hook coverage proven on `vault/artifacts/generated/`. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `.claude/hooks/lib/pii-scan-scope.sh` | Modify | Extend `DATA_BEARING_PREFIXES` (and/or `PER_SE_DENY_PREFIXES`) to cover `vault/artifacts/generated/` so the operator-name scan reaches a committed maintained-HTML artifact. |
| `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh` | Create | Fixture/regression test asserting `block-pii-commit.sh` + `pre-push-pii-scan.sh` deny a name-bearing committed artifact under `vault/artifacts/generated/`, and still allow a de-identified one. |
| `scripts/model/client.py` | Modify | **[AMENDED 2026-06-24]** Add `ModelClient.deidentify(raw_intake) -> de_identified_summary` (+ the `_FixedEnvelopeClient`/`_ClaudeNoTrainBackend` stubs) — the de-id-IN seam. The ALLOWED model-boundary extension (ADR-0020 sanctions extending the model surface; the EXTEND-NOT-REBUILD freeze covers the inner engine + `router.py`, not `client.py`). |
| `scripts/plan/deid_in.py` | Create | The model-backed de-id-IN boundary: ingests raw plan-intake, returns the de-identified summary via `ModelClient.deidentify` on the no-train backend, fail-closed-halt on failure/outage. |
| `tests/plan/test_deid_in.py` | Create | Unit tests for de-id-IN: no-train lane only, fail-closed on `ModelCallError`, raw-PII-leak probe over the emitted summary, whole-run outage → halt. |
| `scripts/plan/reinsert_out.py` | Create | The deterministic OUT re-insertion: substitutes real operator PII from the gitignored identity config into the rendered artifact; fail-closed to initials-only when the target is not confirmable gitignored. |
| `tests/plan/test_reinsert_out.py` | Create | Unit tests for OUT re-insertion: name fill from gitignored source, initials-only fallback on a tracked target, 0 real PII in the persisted store after render. |
| `scripts/plan/plan_orchestrator.py` | Create | The programmatic subscription orchestrator: drives the de-id-IN → orchestrate/assemble → {judge ∥ safety} → revise → render → de-id-OUT runtime over the inner engine, inlining specialist role profiles, fail-closed on the inner safety gate. |
| `tests/plan/test_plan_orchestrator.py` | Create | Unit/integration tests: end-to-end unattended run over synthetic fixtures + mock clients, inner-safety-gate-bypass probe, revise-loop topology (single loop, both gates, N=3 halt), de-identified-summary-only dispatch. |
| `scripts/plan/dispatch_budget.py` | Create | Per-plan dispatch-count instrumentation + a configurable fail-closed cap that halts to honest/partial no-plan on exceed and surfaces the count. |
| `tests/plan/test_dispatch_budget.py` | Create | Unit tests: count accrual across specialists/judge/reviewers/revise iters, fail-closed halt on cap exceed, count surfaced. |
| `scripts/plan/quality_judge.py` | Create | The post-assembly plan-quality judge: scores the assembled plan against the plan-quality rubric (producer-independent), emits ACCEPT/REVISE, feeds the shared revise loop. |
| `vault/design/plan-quality-rubric.md` | Create | The maintained plan-quality rubric (followability, coherence, internal consistency, completeness) the judge scores against. |
| `tests/plan/test_quality_judge.py` | Create | Unit tests: judge fires after assembly before surfacing, producer-independence, seeded-quality-defect rejection, bounded-revise halt at N. |
| `scripts/plan/safety_review.py` | Create | The multi-agent whole-plan safety review: dispatches ≥2 independent safety lenses over the composed plan, synthesizes + blind-triages, routes legitimate findings into the shared revise loop, reads the reconciler hold set to exclude already-adjudicated findings (no double-gate/gap). |
| `tests/plan/test_safety_review.py` | Create | Unit tests: ≥2 lenses over the composed whole, seeded-emergent-issue catch, no double-gate/no gap against the inner `adjudicate` gate, blind-triage dedupe. |
| `scripts/generate/maintained.py` | Create | The unified maintained-HTML lifecycle: re-emits one living artifact via `render.emit` preserving prior annotations/tracking across re-emits, atomic write-to-temp-then-rename, folds the tracking/testing sub-surfaces, gitignored-only PII-bearing output. |
| `tests/generate/test_maintained.py` | Create | Unit tests: re-emit preserves prior content + folds new data, single-file/<500KB/0-external-request budget held, atomic re-emit never leaves store-divergence, re-inserted-PII-in-committed-render probe (threshold 0). |

## Tasks

### ADR-0021-T0-SCANSCOPE: [Spike] Fix the PII Scan-Scope Hole on the Maintained-Output Path
**Status:** TODO
**ADR Source:** ADR-0021, OQ-1 + Consequences-Negative-2; ADR-0025, OQ-1 + Consequences-Negative-3; ADR-0020, OQ-1; DAG §6 (the 3 Pending PII tensions); dispositions.md #1 (Block)
**Files to create/modify:**
- `.claude/hooks/lib/pii-scan-scope.sh` -- add `vault/artifacts/generated/` to `DATA_BEARING_PREFIXES` (name-scan coverage) and/or to `PER_SE_DENY_PREFIXES` (by-location denial); the single-sourced scope both hooks read
- `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh` -- fixture test proving the scope change denies a name-bearing committed artifact under the new prefix and still allows a de-identified one

**Acceptance Criteria:**
1. `vault/artifacts/generated/` appears in `DATA_BEARING_PREFIXES` (and/or `PER_SE_DENY_PREFIXES`) in `.claude/hooks/lib/pii-scan-scope.sh`; both `block-pii-commit.sh` and `pre-push-pii-scan.sh` build their `data_bearing` argument from that shared list (verified by `rg "DATA_BEARING_PREFIXES" .claude/hooks/block-pii-commit.sh .claude/hooks/pre-push-pii-scan.sh` matching the iteration sites).
2. A staged file `vault/artifacts/generated/plan.html` containing the operator-identity token from `vault/meta/operator-identity.txt` is DENIED by `block-pii-commit.sh` (the hook exits non-zero / emits a deny decision).
3. The same name-bearing artifact in a push range is DENIED by `pre-push-pii-scan.sh`.
4. A de-identified `vault/artifacts/generated/plan.html` (initials-only, no identity token, no contact token) is ALLOWED by both hooks (the scope change does not over-block clean artifacts).
5. `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh` passes with both the deny case and the allow case green.
6. `scripts/tests/run-all-tests.sh` (the hook/governance suite) passes after the change — no pre-existing PII-hook test regresses.

**Risk Mitigations:** ADR-0021 Consequence-Negative-2 / ADR-0025 Consequence-Negative-3 (the name scan-scope hole — a committed name-bearing maintained-HTML artifact is scanned only for contact tokens) — mitigated by extending the scope so the name token is scanned on the artifacts path, proven by criteria 2-3. ADR-0005 Falsification (≥1 operator-PII value in a tracked file is release-blocking) — this task is the boundary the 0021/0025 egress rests on.
**Dependencies:** None (entry point)

---

### ADR-0020-T1: Model-Backed De-Id-IN Boundary Over the No-Train Lane
**Status:** TODO
**ADR Source:** ADR-0020, Decision + Rationale (model-backed no-train de-id-IN superseding `router.summarize` as the sole de-id-IN on the plan path)
**Files to create/modify:**
- `scripts/model/client.py` (Modify: add `deidentify`) -- **[AMENDED 2026-06-24]** add the `ModelClient.deidentify(raw_intake) -> de_identified_summary` method (+ the `_FixedEnvelopeClient.deidentify` / `_ClaudeNoTrainBackend.deidentify` stubs mirroring `author`/`converse`). This is the ALLOWED model-boundary extension: the EXTEND-NOT-REBUILD freeze covers the INNER ENGINE (`orchestrate`/`pipeline`/`assemble`/`generate_plan`/`adjudicate`/`adjust`/`track`) + `router.py`, NOT `client.py` — `client.py` is the boundary ADR-0020 sanctions extending (ADR-0020 Decision: "model-backed de-id boundary"; ADR-0015 revision: the third method alongside `converse`/`author`).
- `scripts/plan/deid_in.py` -- the de-id-IN boundary: takes raw plan-intake + the wired `ModelClient`, returns the de-identified summary via `ModelClient.deidentify` on the no-train backend; reuses the existing `ModelClient` seam (does NOT re-introduce or construct a second client); `router.summarize` survives unchanged as the persisted-side de-id
- `tests/plan/test_deid_in.py` -- unit tests with a mock/`_FixedEnvelopeClient`-style client + synthetic raw-PII fixtures

**Acceptance Criteria:**
1. `deid_in(raw_intake, client)` returns a de-identified summary object the orchestrator consumes; the de-id call routes through the injected no-train `ModelClient`, fail-closed on failure. **[AMENDED 2026-06-24]:** the de-id seam is a new `ModelClient.deidentify(raw_intake) -> de_identified_summary` method (the model-boundary extension ADR-0020 sanctions), NOT `author` (`author(domain, summary)` consumes an already-de-identified summary — it cannot ingest raw and emit a de-identified summary). The no-train guarantee = the call runs on the no-train `_ClaudeNoTrainBackend` AND `deid_in` constructs NO second client / opens no SDK path (assert the injected no-train `ModelClient` is the ONLY client used — a boundary that instantiated its own client turns this RED) — NOT a `router.Dispatch` lane (no no-train lane lives on `ModelClient`; binding the guarantee to a router lane made the crown-jewel containment test tautological). Reason: the recipe-review (QA+Security+Architect convergent) caught that `author` cannot de-identify raw and the "no-train lane" the prior AC bound to lives on `router.Dispatch`, not on `ModelClient` — the de-id-seam spec defect (bead `a-plus-maxing-pqlx`).
2. With a mock client raising `ModelCallError`, `deid_in` returns the honest no-plan state (mirroring `generate_plan`'s `AUTHOR_CALL_FAILED`), never a fabricated or partial summary.
3. The persisted-side `router.summarize` path is unchanged: a post-run scan of the store-read summary returns 0 raw-PII hits (the existing `summarize`/`dispatch` whitelist still enforced; this task does not edit `router.py`).
4. `bash` / `pytest tests/plan/test_deid_in.py` passes with all cases green, run entirely against mock clients (0 live-API calls).
5. The boundary never writes raw plan-intake to a tracked path (the test asserts any raw residue lands only on a gitignored target or in-memory; nothing under a tracked path is written).

**Risk Mitigations:** ADR-0020 Consequence-Negative-1 (raw plan-intake PII transits the API before de-id) — mitigated by the no-train-lane-only routing (criterion 1) reusing ADR-0016's bounded posture. ADR-0020 Consequence-Negative-4 (per-call failure) — mitigated by the fail-closed degrade (criterion 2). Constraint ADR-0001 (summaries-not-raw, no-train lane) — criteria 1+3. Constraint ADR-0016 (raw-egress bounded to no-train lane) — criterion 1.
**Dependencies:** None (entry point)

---

### ADR-0020-T2: De-Id-Boundary Whole-Run Outage → Fail-Closed Halt
**Status:** TODO
**ADR Source:** ADR-0020, OQ-4 + Consequences-Negative-4 (system-level outage path); dispositions.md #3 (Proceed — fail-closed-halt)
**Files to create/modify:**
- `scripts/plan/deid_in.py` -- add the whole-run outage path: when the de-id boundary is unreachable for a run, raise/return the honest no-plan halt (distinct from a single failed call); never fall back to `router.summarize` as the de-id-IN
- `tests/plan/test_deid_in.py` -- add outage-injection cases (boundary unreachable for the whole run)

**Acceptance Criteria:**
1. With the de-id boundary injected as unreachable for the whole run, `deid_in` (and the orchestrator that calls it) records 0 plans and surfaces the honest no-plan state — verified by asserting `run_generation`/the orchestrator returns no recorded `plan::<domain>` after an injected outage.
2. On outage, the engine does NOT call `router.summarize` as a degraded de-id-IN substitute (asserted by a spy/mock confirming 0 fallback-to-`summarize`-as-de-id-IN calls).
3. On outage, any existing maintained-HTML artifact is left untouched (no partial re-emit) — asserted by comparing the artifact's pre- and post-outage content (identical).
4. On an injected whole-run de-id-boundary outage, the downstream gates issue 0 dispatches — judge (ADR-0023) dispatch count = 0 AND safety-review (ADR-0024) lens dispatch count = 0 (asserted by spying both dispatch paths). Cites ADR-0020 OQ-4 ("judge/review/maintained-format all idle").
5. `pytest tests/plan/test_deid_in.py` passes including the outage cases, against mock clients (0 live calls).

**Risk Mitigations:** ADR-0020 Consequence-Negative-4 / OQ-4 (whole-run outage unspecified would let the engine silently degrade de-id fidelity) — mitigated by the fail-closed halt (criteria 1-2). ADR-0025 Falsification-2 (no partial/stale re-emit) — criterion 3. ADR-0020 OQ-4 (judge/review/maintained-format all idle on outage — the missing negative assertion, E2E-placement discipline) — criterion 4.
**Dependencies:** ADR-0020-T1

---

### ADR-0021-T1: Deterministic PII Re-Insertion Onto the Gitignored Render
**Status:** TODO
**ADR Source:** ADR-0021, Decision + Rationale (deterministic local re-insertion from the gitignored identity config; no model on the OUT path; gitignored-only target; fail-closed to initials-only)
**Files to create/modify:**
- `scripts/plan/reinsert_out.py` -- the deterministic OUT pass: reads the real name/identifiers from `vault/scaffold/filled/operator-profile.md` / `vault/meta/operator-identity.txt` (the same gitignored source `component_set.read_profile` reads initials from) and substitutes them into the rendered HTML; suppresses re-insertion (initials-only) when the target is not confirmable gitignored
- `tests/plan/test_reinsert_out.py` -- unit tests with synthetic gitignored fixtures (no real operator PII in the test tree)

**Acceptance Criteria:**
1. `reinsert_out(html, target_path)` with a confirmable-gitignored target produces an artifact whose header shows the operator's full name (from the gitignored source), not initials.
2. The same call with a TRACKED target path suppresses re-insertion and renders initials-only (the fail-closed default) — verified on a crafted tracked target.
3. No real PII is sent to any model on the OUT path (the module imports no `ModelClient`; asserted by `rg "ModelClient|client" scripts/plan/reinsert_out.py` returning 0 model-send sites).
4. After a re-inserting render, `pii_scan.scan` over `vault/store/` and the tracked set returns 0 real-PII hits (the persisted store and every tracked render stay de-identified).
5. `pytest tests/plan/test_reinsert_out.py` passes with all cases green, run against synthetic fixtures (0 live calls, 0 real operator PII in the test tree).

**Risk Mitigations:** ADR-0021 Consequence-Negative-1 (real PII materializes in a local artifact) — mitigated by the gitignored-only target + initials-only fail-closed (criteria 1-2). Constraint ADR-0005 (no committed/tracked PII) — criterion 4 + the T-SCANSCOPE dependency. ADR-0021 single-egress-class invariant — criterion 3.
**Dependencies:** ADR-0021-T0-SCANSCOPE

---

### ADR-0022-T1: Programmatic Subscription Orchestrator Wrapping the Inner Engine
**Status:** TODO
**ADR Source:** ADR-0022, Decision + Rationale (programmatic subscription orchestrator superseding the S68 interactive runtime, wrapping `orchestrate.generate_plans`/`pipeline.run_generation`/`adjudicate`/`assemble`, dispatching through the `ModelClient` seam, inlining specialist role profiles)
**Files to create/modify:**
- `scripts/plan/plan_orchestrator.py` -- the orchestrator drive layer: dispatches the plan-domain specialists (full role profiles inlined per INV-ROLE-INLINING) over the de-identified summary, supplies the `reauthor`/`adjudicator` hooks programmatically to `run_generation`, and records the survivors via the existing `record_plan`; reuses the inner engine verbatim
- `tests/plan/test_plan_orchestrator.py` -- end-to-end unattended run over synthetic PII-free fixtures + mock clients

**Acceptance Criteria:**
1. The orchestrator runs end-to-end unattended (no human dispatch) over a synthetic fixture and `run_generation` returns `results` with ≥1 recorded `plan::<domain>` and `dvq_entries` populated.
2. Every specialist dispatch the orchestrator issues receives the de-identified summary only — count of raw-PII fields in any dispatch payload = 0 (asserted by inspecting each dispatch).
3. The orchestrator reuses the inner engine: it calls `orchestrate.generate_plans` / `collate_doctor_visit_queue` and records nothing outside `record_plan` (no new store stream) — asserted by spying the call set.
4. **Inner-safety-gate-bypass probe:** with a seeded held safety finding and NO content-valid override, the held domain records nothing and reaches the honest no-plan state — count of plans recorded past an unadjudicated hold = 0.
5. Each dispatched specialist's full role profile is inlined verbatim in its prompt (asserted by checking the dispatch prompt contains the profile's required sections — the `enforce-role-inlining` discipline).
6. `pytest tests/plan/test_plan_orchestrator.py` passes against mock clients (0 live-API calls).

**Risk Mitigations:** ADR-0022 Consequence-Negative-1 (lost per-dispatch human checkpoint) — mitigated by routing safety onto the load-bearing safety-review tier (ADR-0024-T1) + the inner-gate-bypass probe (criterion 4). ADR-0022 Consequence-Negative-2 (autonomous adjudicator dispatch) — criterion 4. OQ-1 (full-profile inlining) — criterion 5.
**Dependencies:** ADR-0020-T1

---

### ADR-0022-T2: Single Bounded Revise Loop (Both Gates, Safety-Blocking, N=3 Halt)
**Status:** TODO
**ADR Source:** ADR-0022, Decision (the orchestrator owns the control flow the gates run inside); ADR-0023/0024 OQ-2 (the SHARED revise-loop topology); dispositions.md #2 (Proceed — single bounded loop)
**Files to create/modify:**
- `scripts/plan/plan_orchestrator.py` -- add the revise-loop control flow: after assembly run BOTH gates (quality judge ADR-0023, safety review ADR-0024); a safety finding is BLOCKING and a standing safety block is terminal; a quality finding drives one revise dispatch via `reauthor`; RE-RUN BOTH gates each pass; cap N=3 then HALT to honest no-plan
- `tests/plan/test_plan_orchestrator.py` -- add revise-loop topology tests (seeded quality miss converging within N; seeded standing safety block terminal; non-converging plan halting at N)

**Acceptance Criteria:**
1. On a seeded quality miss that the revise can clear, the loop re-authors through `reauthor`, re-runs BOTH gates, and surfaces a plan within ≤3 passes.
2. **Standing-safety-block-terminal probe:** with a seeded safety finding that re-fires every pass, 0 plans are surfaced — the loop never overrides a standing safety block (count of plans surfaced past a standing safety block = 0).
3. **Bounded-revise probe:** with a non-converging quality miss, the loop HALTS at N=3 and escalates to honest no-plan — count of plans that loop past N=3 revise passes = 0.
4. Both gates re-run after every revise pass (asserted by spying the judge + safety dispatches per pass — each pass fires both).
5. **Seeded CRITICAL/H1-H2 non-overridable probe:** with a seeded CRITICAL or H1-H2 inner hold AND an override record, 0 plans are surfaced past it via any revise pass — the non-overridable tier is never laundered to a surfaced plan by the autonomous loop. (Distinct from the standing-HIGH/MEDIUM-block probe, which a content-valid override could clear.) Cites ADR-0022 Falsification-2 / INV-CRITICAL-NON-OVERRIDABLE.
6. `pytest tests/plan/test_plan_orchestrator.py` passes including the three revise-loop probes (0 live calls).

**Risk Mitigations:** ADR-0023 Consequence-Negative-3 / ADR-0024 Consequence-Negative-2 (unbounded loop / multi-lens over-block) — mitigated by the N=3 cap (criterion 3) + safety-block terminal (criterion 2). ADR-0024 Consequence-Negative-3 (the safety tier is load-bearing) — criterion 2. ADR-0022 Falsification-2 / INV-CRITICAL-NON-OVERRIDABLE (the autonomous adjudicator path must never surface a plan over a held CRITICAL / H1-H2 finding even with an override record) — criterion 5.
**Note (cap N):** N=3 is fixed at build-plan time per dispositions #2 and discharges ADR-0023 OQ-1 (blocking-for-test); it binds at build-plan time whereas the ADR-0022-T3 dispatch cap stays runtime-configurable because its ceiling is an operator/billing fact confirmed at the live-run checkpoint.
**Dependencies:** ADR-0022-T1, ADR-0023-T1, ADR-0024-T1

---

### ADR-0022-T3: Dispatch-Count Instrumentation + Fail-Closed Cap
**Status:** TODO
**ADR Source:** ADR-0022, OQ-4 + OQ-2 (aggregate dispatch volume vs the subscription ceiling); dispositions.md #4 (Proceed — instrument + cap)
**Files to create/modify:**
- `scripts/plan/dispatch_budget.py` -- a per-plan dispatch counter (specialists + revise iters + judge + M safety reviewers + triage) + a configurable cap that fails closed (honest/partial no-plan) on exceed and surfaces the count
- `scripts/plan/plan_orchestrator.py` -- wire the counter into the orchestrator's dispatch path
- `tests/plan/test_dispatch_budget.py` -- unit tests for the counter + cap

**Acceptance Criteria:**
1. `dispatch_budget` accrues a count across every orchestrator dispatch (specialist, judge, each safety reviewer, each revise iteration) — verified by asserting the count equals the dispatch tally over a synthetic run.
2. With the cap set below the run's dispatch tally, the orchestrator HALTS to the honest/partial no-plan state and surfaces the count (count of plans recorded past the cap = 0).
3. The cap is configurable (a build-plan parameter, not hard-coded) — asserted by running two configs (one allowing, one blocking) over the same fixture.
4. With the cap set above the tally, the run completes normally and the count is reported.
5. `pytest tests/plan/test_dispatch_budget.py` passes against mock clients (0 live calls).

**Risk Mitigations:** ADR-0022 Consequence (subscription ceiling vs loop volume) / OQ-4 — mitigated by the instrument + fail-closed cap (criteria 1-2). The ceiling NUMBER is an operator/billing fact confirmed downstream at the live-run checkpoint; this task builds the mechanism only.
**Dependencies:** ADR-0022-T1

---

### ADR-0023-T1: Post-Assembly Plan-Quality Judge + Rubric
**Status:** TODO
**ADR Source:** ADR-0023, Decision + Rationale + Validation Approach (independent post-assembly quality judge scoring the assembled plan against a rubric, producer-independent, feeding the bounded revise loop)
**Files to create/modify:**
- `scripts/plan/quality_judge.py` -- the judge: scores the assembled plan against the plan-quality rubric, emits ACCEPT/REVISE, runs producer-independent (no specialist self-assessments / orchestrator notes in its input), wraps the `assemble`/`generate_plans` output (does not edit the inner engine)
- `vault/design/plan-quality-rubric.md` -- the maintained rubric: followability, coherence, internal consistency, completeness dimensions
- `tests/plan/test_quality_judge.py` -- unit tests with synthetic assembled-plan fixtures

**Acceptance Criteria:**
1. The judge fires AFTER `assemble`/`generate_plans` produce the plan and BEFORE it is surfaced/recorded as final — count of plans surfaced without a judge verdict = 0.
2. The judge input excludes the specialists' self-assessments and the orchestrator's notes (producer-independence asserted by inspecting the dispatch payload).
3. **Seeded-quality-defect probe:** an assembled plan with internally contradictory cross-section targets OR an empty/incoherent in-scope domain section gets a REVISE verdict (or triggers the loop) — count of seeded-defective plans surfaced with ACCEPT = 0.
4. `vault/design/plan-quality-rubric.md` exists and contains the four named dimensions (followability, coherence, internal consistency, completeness).
5. `pytest tests/plan/test_quality_judge.py` passes against mock judge clients (0 live calls).

**Risk Mitigations:** ADR-0023 Consequence-Negative-2 (the judge can reject a clinically-safe plan on quality) — accepted; the gate is distinct from safety. Rubber-stamping (judge-discipline §2) — mitigated by producer-independence (criterion 2) + the seeded-defect probe (criterion 3). The bounded-revise cap N=3 is enforced in ADR-0022-T2 (the loop owner), per the SHARED OQ-2 single-loop resolution.
**Dependencies:** ADR-0022-T1

---

### ADR-0024-T1: Multi-Agent Whole-Plan Safety Review
**Status:** TODO
**ADR Source:** ADR-0024, Decision + Rationale + Validation Approach (`/review-pr`-style multi-lens whole-plan safety review wrapping the inner per-finding `adjudicate` gate, feeding the bounded revise loop, composing without double-gate/gap)
**Files to create/modify:**
- `scripts/plan/safety_review.py` -- dispatches ≥2 independent safety lenses (`medical-safety-reviewer`, `health-edge-case-reviewer`, `medical-liaison`-as-whole-plan-reviewer — all present in `.claude/agents/`) over the composed plan, synthesizes + blind-triages, routes legitimate findings into the shared revise loop, reads the reconciler hold set to EXCLUDE already-adjudicated per-finding holds (no double-gate, no gap); does NOT touch `adjudicate`/the reconciler
- `tests/plan/test_safety_review.py` -- unit tests with synthetic composed-plan fixtures carrying a seeded emergent issue

**Acceptance Criteria:**
1. The review dispatches ≥2 independent safety lenses over the COMPOSED multi-domain plan (not per-finding fragments) and produces a synthesized, blind-triaged finding set — asserted by counting ≥2 lens dispatches over the whole-plan input.
2. **Seeded-emergent-issue probe:** an assembled plan carrying a known cross-domain emergent issue the inner per-finding gate raises 0 holds for (verified via `reconcile` raising 0 holds) is caught by the review and drives a revise (or a block to honest no-plan) — count of seeded emergent-unsafe plans surfaced un-flagged = 0.
3. **No-double-gate/no-gap probe:** a per-finding hold already adjudicated by `adjudicate` is NOT re-adjudicated to a conflicting disposition by the review (0 conflicting re-adjudications), and no inner-gate hold reaches the surface because the tier assumed the inner gate handled it (0 gaps) — asserted by seeding one of each.
4. The review adds no override path of its own and does not edit `adjudicate`/the reconciler (asserted by `rg` over `scripts/plan/safety_review.py` finding 0 writes to the override-record path).
5. `pytest tests/plan/test_safety_review.py` passes against mock lens clients (0 live calls).

**Risk Mitigations:** ADR-0024 Consequence-Negative-1 (added latency/dispatch volume) — bounded by the dispatch cap (ADR-0022-T3) + the N=3 loop. ADR-0024 Consequence-Negative-2 (lens over-block/conflict) — mitigated by blind-triage dedupe (criterion 1) + the bounded loop. ADR-0024 Consequence-Negative-3 (the tier is load-bearing) — the seeded-emergent probe (criterion 2). Double-gate/gap falsification — criterion 3.
**Dependencies:** ADR-0022-T1

---

### ADR-0025-T1: Unified Maintained-HTML Output (Re-Emit + Folded Tracking)
**Status:** TODO
**ADR Source:** ADR-0025, Decision + Rationale + Validation Approach (maintained/re-emit-on-new-data lifecycle amending ADR-0004's single-file render, preserving prior content, atomic re-emit, folding tracking/testing surfaces, gitignored-only PII-bearing output)
**Files to create/modify:**
- `scripts/generate/maintained.py` -- the maintained lifecycle: re-emits one living artifact through the existing `render.emit` (does not re-author the render engine), preserves prior annotations/tracking across re-emits, write-to-temp-then-rename atomicity, folds the `track.resolve_plan_progress` plan-vs-actual view as a section, writes the PII-bearing artifact only to the gitignored `vault/artifacts/generated/`
- `tests/generate/test_maintained.py` -- unit tests with synthetic plan + tracking fixtures

**Acceptance Criteria:**
1. After emitting the maintained plan, adding an annotation/tracking entry, and re-emitting on a new data point: the new data point is present AND the prior annotation/tracking entry survives in the re-emitted file (count of lost prior entries = 0).
2. Each emitted/re-emitted artifact is one self-contained offline file with 0 external asset requests and size < 500KB (asserted via `render.emit`'s external-reference raise + a size check).
3. The tracking/testing surface renders INTO the maintained format: after `track.record_tracking` records a snapshot, the re-emitted artifact contains the plan-vs-actual view as a folded section (not a separate file).
4. A partial/failed re-emit (injected mid-write) never leaves the artifact diverged from the store — the atomic write-to-temp-then-rename leaves either the prior good artifact or the new complete one (0 partial-state artifacts).
5. **Re-inserted-PII-in-a-committed-render probe (threshold 0):** a maintained re-emit carrying re-inserted real PII, staged/committed and staged/pushed, is DENIED by `block-pii-commit.sh` AND `pre-push-pii-scan.sh` — 0 real-PII values reach any tracked/committed file (this exercises the T-SCANSCOPE coverage).
6. The maintained-format render runs BEFORE the deterministic name-fill; re-insertion is the FINAL pass over the produced HTML and the re-inserted name survives into the emitted artifact unmodified — 0 renders clobber a re-inserted name. Cites ADR-0021 Rationale.
7. **Store-adversarial battery (`pka`):** the `maintained.py` store read/write paths satisfy `docs/checklists/store-adversarial-tests.md` — cross-stream collision (a `track.resolve_plan_progress` read for domain X never returns Y's tracking), same-timepoint dedupe on the `track.record_tracking` write, dedupe-key boundary, mutation observed RED — verified in `tests/generate/test_maintained.py`; checked at Tier-1 self-check AND the Tier-2 QA dispatch (bead `pka`).
8. `pytest tests/generate/test_maintained.py` passes against synthetic fixtures (0 live calls, 0 real operator PII in the test tree).

**Risk Mitigations:** ADR-0025 Consequence-Negative-1 (maintained-artifact state/staleness/divergence) — mitigated by atomic re-emit (criterion 4). ADR-0025 Consequence-Negative-2 (widened local-PII surface) + Negative-3 (the name scan-scope hole) — mitigated by the gitignored-only output + the T-SCANSCOPE coverage (criterion 5). ADR-0021 Rationale (format-then-fill: the deterministic name fill is the last pass over the produced HTML) — criterion 6. Constraint ADR-0004 (single-file/<500KB/WCAG-AA/0-external budget) — criterion 2. Constraint ADR-0005 (no committed PII) — criterion 5. Store-surface mandate (`pka`) — criterion 7.
**Dependencies:** ADR-0021-T0-SCANSCOPE, ADR-0021-T1, ADR-0022-T1

---

## Dependency Map

```
ADR-0021-T0-SCANSCOPE --> ADR-0021-T1
ADR-0021-T0-SCANSCOPE --> ADR-0025-T1
ADR-0020-T1 --> ADR-0020-T2
ADR-0020-T1 --> ADR-0022-T1
ADR-0021-T1 --> ADR-0025-T1
ADR-0022-T1 --> ADR-0022-T2
ADR-0022-T1 --> ADR-0022-T3
ADR-0022-T1 --> ADR-0023-T1
ADR-0022-T1 --> ADR-0024-T1
ADR-0022-T1 --> ADR-0025-T1
ADR-0023-T1 --> ADR-0022-T2
ADR-0024-T1 --> ADR-0022-T2
```

Topological order (Kahn's algorithm; parallel groups):

1. **ADR-0021-T0-SCANSCOPE, ADR-0020-T1** (parallel — entry points, no dependencies)
2. **ADR-0020-T2, ADR-0021-T1, ADR-0022-T1** (parallel — each depends only on a group-1 task: T2 on 0020-T1; 0021-T1 on T0-SCANSCOPE; 0022-T1 on 0020-T1)
3. **ADR-0022-T3, ADR-0023-T1, ADR-0024-T1, ADR-0025-T1** (parallel — 0022-T3/0023-T1/0024-T1 depend on 0022-T1; 0025-T1 depends on T0-SCANSCOPE + 0021-T1 + 0022-T1, all in groups 1-2)
4. **ADR-0022-T2** (after 0022-T1 + 0023-T1 + 0024-T1 — it composes both gates into the single revise loop)

Entry points: ADR-0021-T0-SCANSCOPE, ADR-0020-T1
Critical path: ADR-0020-T1 → ADR-0022-T1 → ADR-0023-T1 (or ADR-0024-T1) → ADR-0022-T2

These parallel groups map to the build-plan waves: Wave 1 = the PII envelope foundation + de-id-IN (group 1); Wave 2 = the OUT re-insertion + outage path + orchestrator core (group 2); Wave 3 = the gates + maintained output + budget (group 3); Wave 4 = the revise-loop composition (group 4).

## Test Strategy

All tasks are satisfiable with mock clients (`_FixedEnvelopeClient`-style adapters / fixture envelopes mirroring the S88–S91 foundation) and synthetic PII-free fixtures (the test tree carries 0 real operator PII; the T-SCANSCOPE / re-insertion / maintained probes use a synthetic identity token). **No task makes a live API call (0 live-API spend); the live end-to-end run is the operator-present checkpoint AFTER the build.**

### Unit Tests
- **Scope:** `deid_in.py`, `reinsert_out.py`, `plan_orchestrator.py`, `dispatch_budget.py`, `quality_judge.py`, `safety_review.py`, `maintained.py`, and `lib/pii-scan-scope.sh`.
- **Approach:** pytest with mock/`_FixedEnvelopeClient` model clients and synthetic fixtures for the Python modules; a bash fixture test (`test_pii_scan_scope_artifacts.sh`) for the scope change. No live dependencies, no real PII.
- **Criteria covered:** ADR-0021-T0-SCANSCOPE 1-6, ADR-0020-T1 1-5, ADR-0020-T2 1-5, ADR-0021-T1 1-5, ADR-0022-T1 1-6, ADR-0022-T2 1-6, ADR-0022-T3 1-5, ADR-0023-T1 1-5, ADR-0024-T1 1-5, ADR-0025-T1 1-8.

### Integration Tests
- **Scope:** the end-to-end runtime-stage-order path — de-id IN (0020) → orchestrate/assemble (0022 + inner engine) → {judge ∥ safety} → revise loop → maintained render (0025) → de-id OUT (0021) — over a synthetic fixture with mock clients.
- **Approach:** invoke `plan_orchestrator` end-to-end (no human in the loop); assert `run_generation` records a plan + DVQ, the gates fire in stage order, the revise loop composes both gates, and the maintained artifact is re-emitted. Exercises a file created by one task and consumed by another (0022-T1's recorded plan → 0023-T1's judge → 0025-T1's render).
- **Criteria covered:** ADR-0022-T1 1+3, ADR-0022-T2 1+4, ADR-0023-T1 1, ADR-0024-T1 1, ADR-0025-T1 1+3.

### Risk-Specific Tests
- **Scope:** the crown-jewel leak probes (ADR-0020/0021/0025 raw-PII / re-inserted-PII thresholds), the de-id outage-halt + downstream-gate-idle assertion (ADR-0020 OQ-4), the inner-safety-gate-bypass + standing-safety-block-terminal + CRITICAL/H1-H2 non-overridable (ADR-0022/0024), the bounded-revise-cap (ADR-0022/0023), the dispatch-cap (ADR-0022-T3), and the `maintained.py` store-adversarial battery (ADR-0025-T1, bead `pka`).
- **Approach:** seed each adversarial condition (a synthetic raw-PII token; a whole-run outage; an unadjudicated hold; a standing safety block; a seeded CRITICAL/H1-H2 hold with an override record; a non-converging plan; a name-bearing committed artifact; an over-budget dispatch tally; a cross-stream/dedupe store-keying mutation) and assert the 0-threshold / fail-closed outcome.
- **Store-surface mandate (`pka`):** the store-adversarial battery on the `maintained.py` `track.resolve_plan_progress` read + `track.record_tracking` write paths — cross-stream collision, same-timepoint dedupe, dedupe-key boundary, mutation observed RED (ADR-0025-T1 crit 7).
- **Criteria covered:** ADR-0021-T0-SCANSCOPE 2-4, ADR-0020-T1 2+5, ADR-0020-T2 1-4, ADR-0021-T1 2+4, ADR-0022-T1 4, ADR-0022-T2 2-3,5, ADR-0022-T3 2, ADR-0023-T1 3, ADR-0024-T1 2-3, ADR-0025-T1 4-5,7.

## Repo-Grounding Ledger

Grounded against the worktree-authoritative checkout at `main` @ `293d930` (HEAD). The EXTEND-NOT-REBUILD fact was confirmed by reading the inner engine + the `ModelClient` seam directly.

| Task | RGC-1 (manifest) | RGC-2 (premise) | RGC-3 (cited input) | RGC-4 (dup) | Disposition |
|------|------------------|-----------------|---------------------|-------------|-------------|
| ADR-0021-T0-SCANSCOPE | pass — `lib/pii-scan-scope.sh` present (Modify); `tests/test_pii_scan_scope_artifacts.sh` absent (Create) | pass — `DATA_BEARING_PREFIXES` excludes `vault/artifacts/generated/` (confirmed L30); both hooks build `data_bearing` from it (`block-pii-commit.sh:279`, `pre-push-pii-scan.sh:126`); `.gitignore:6` covers the path | pass — `scan_scoped(changed, data_bearing,…)` runs the identity scan only over `data_bearing` (confirmed L375-406); `vault/meta/operator-identity.txt` present (16 bytes) | pass — `.claude/hooks/tests/` has no artifacts/name scan fixture; this is a new test | Grounded |
| ADR-0020-T1 | pass — `scripts/model/client.py` present (Modify: add `deidentify`); `scripts/plan/deid_in.py` absent (Create); `tests/plan/test_deid_in.py` absent (Create) **[AMENDED 2026-06-24]** | pass — `ModelClient` 2-method surface (`converse`/`author`) present (`client.py:45,60`), `_ClaudeNoTrainBackend`/`ModelCallError`/`_FixedEnvelopeClient` patterns present for `deidentify` to mirror; no existing `deidentify` (grep clean); `_author_callable`/`AUTHOR_CALL_FAILED` present (`generate_plan.py:90,68`); `router.summarize` persisted-side de-id present | pass — `ModelClient` + `_FixedEnvelopeClient`/`_FixtureBackend` exist and are the declared mock seam (`generate_plan.py:71`, `tests/model/test_client.py:32`) | pass — no existing de-id-IN module/test and no existing `deidentify` method (grep over `scripts/`+`tests/` found none) | Grounded |
| ADR-0020-T2 | pass — `deid_in.py` created by ADR-0020-T1 (Create-by-prior-task exempt); test file likewise | pass — OQ-4 outage path is genuinely unspecified in code today (no whole-run outage branch); `router.summarize` exists as the path NOT to fall back to | pass — same `ModelClient` seam; outage injected via mock | pass — no existing outage-halt path | Grounded |
| ADR-0021-T1 | pass — `scripts/plan/reinsert_out.py` absent (Create); `tests/plan/test_reinsert_out.py` absent (Create) | pass — `component_set.read_profile` reads initials from the gitignored `_PROFILE_PATHS` source (`handout.py:43-46`, `component_set.py:736`); `vault/scaffold/filled/operator-profile.md` is the declared gitignored source (`.gitignore:5`) | pass — `pii_scan.scan` present (`pii_scan.py:210`); `operator-identity.txt` present | pass — no existing re-insertion module; initials-only `read_profile` is the path being extended, not duplicated | Grounded |
| ADR-0022-T1 | pass — `scripts/plan/plan_orchestrator.py` absent (Create); test absent (Create) | pass — `pipeline.run_generation` forwards `reauthor`/`adjudicator` to `generate_plans` (`pipeline.py:28-65`); `generate_plans`/`collate_doctor_visit_queue`/`record_plan` present; inner gate fail-closed default present | pass — `run_generation(authors, store_read, root, *, plan_date,…)` signature confirmed; the de-identified summary is the declared input | pass — no existing orchestrator module/test (grep found none); `.claude/agents/` specialist roster present for inlining | Grounded |
| ADR-0022-T2 | pass — modifies `plan_orchestrator.py` (Created by ADR-0022-T1, dependency-ordered); test likewise | pass — `reauthor` seam present for the revise dispatch; the revise-loop topology is genuinely undecided in code (no loop exists yet) — encoded per disposition #2 | pass — judge (0023-T1) + safety review (0024-T1) are in-spec predecessors supplying the gates | pass — no existing revise-loop control flow | Grounded |
| ADR-0022-T3 | pass — `scripts/plan/dispatch_budget.py` absent (Create); modifies `plan_orchestrator.py` (dependency-ordered); test absent (Create) | pass — no existing dispatch-count/cap instrumentation in the orchestrator path | pass — the orchestrator's dispatch path (0022-T1) is the wired count site | pass — no existing budget/cap module | Grounded |
| ADR-0023-T1 | pass — `scripts/plan/quality_judge.py` + `vault/design/plan-quality-rubric.md` + `tests/plan/test_quality_judge.py` all absent (Create) | pass — `assemble`/`generate_plans` produce the assembled plan the judge scores (`assemble.py:278`, `orchestrate.py:482`); judge-discipline references present in skills_library | pass — the assembled-plan output is the declared judge input; `reauthor` seam present for the revise | pass — no existing quality-judge module/rubric (grep found none) | Grounded |
| ADR-0024-T1 | pass — `scripts/plan/safety_review.py` + `tests/plan/test_safety_review.py` absent (Create) | pass — inner per-finding `adjudicate` gate present (`adjudicate.py`); `reconcile` raises the hold set (`orchestrate.py:337`); the emergent-class gap is genuine (per-finding screens only) | pass — `medical-safety-reviewer`, `health-edge-case-reviewer`, `medical-liaison` all present in `.claude/agents/` (confirmed); the reconciler hold set is readable for the no-double-gate exclusion | pass — no existing whole-plan safety-review module; the inner `adjudicate` gate is WRAPPED not replaced | Grounded |
| ADR-0025-T1 | pass — `scripts/generate/maintained.py` + `tests/generate/test_maintained.py` absent (Create) | pass — `render.emit` present, writes to `DEFAULT_OUT_DIR = vault/artifacts/generated` (`render.py:23,149`); `generate.run` single-file path present (`generate.py:34`); `track.record_tracking`/`resolve_plan_progress` present (`track.py:34,81`); `.gitignore:6` covers the artifacts path | pass — `track.resolve_plan_progress(domain, on_date, root)` signature confirmed; `render.emit` is the re-emit primitive (extended, not re-authored) | pass — no existing maintained/re-emit module; `generate.run` stateless render is AMENDED not duplicated | Grounded |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task (0020→T1/T2; 0021→T0-SCANSCOPE/T1; 0022→T1/T2/T3; 0023→T1; 0024→T1; 0025→T1)
- [x] All ADR IDs resolve to actual ADR files on disk (ADR-0020..0025 present in `docs/adr/`)

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion (all have ≥4)
- [x] All acceptance criteria are binary (pass/fail, no subjective measures) — each names a function/command/condition with a 0-threshold or a present/absent check
- [x] No criterion uses words: "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest (files to create/modify)
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in at least one task block
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (verified by topo sort — 4 parallel groups, all edges forward)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed and have Dependencies: "None (entry point)" (ADR-0021-T0-SCANSCOPE, ADR-0020-T1)

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream ADR constraints in their acceptance criteria (ADR-0001 no-train/summaries → ADR-0020-T1 crit 1+3; ADR-0005 no-committed-PII → T0-SCANSCOPE + ADR-0021-T1 crit 4 + ADR-0025-T1 crit 5; ADR-0016 raw-egress bound → ADR-0020-T1 crit 1; ADR-0004 single-file budget → ADR-0025-T1 crit 2; store-surface mandate `pka` (`docs/checklists/store-adversarial-tests.md`) → ADR-0025-T1 crit 7, since `maintained.py` reads/writes `scripts/store/` via `track.resolve_plan_progress`/`track.record_tracking`; ADR-0021 Rationale format-then-fill → ADR-0025-T1 crit 6 + ADR-0022-T2 N-fixed note; ADR-0022 INV-CRITICAL-NON-OVERRIDABLE → ADR-0022-T2 crit 5)
- [x] Constraint Propagation Table entries (DAG §5) have corresponding acceptance criteria in affected tasks

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present (5 items, all from dispositions.md)
- [x] Every open question, pending tension, and unmitigated risk has a disposition (Proceed/Block/Defer)
- [x] Block dispositions have corresponding research spike tasks (ADR-0021-T0-SCANSCOPE for the scan-scope hole)
- [x] Defer dispositions have justifications (none deferred)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in in-scope ADRs is covered by at least one task's Risk Mitigations (0020 N1-N5, 0021 N1-N2, 0022 N1-N3, 0023 N1-N3, 0024 N1-N3, 0025 N1-N3 all traced)

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (crown-jewel leak, outage-halt, gate-bypass, revise-cap, dispatch-cap)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the template exactly (for machine parsing)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`lib/pii-scan-scope.sh`) or is `Create`d by a prior task in dependency order (`deid_in.py`, `plan_orchestrator.py`)
- [x] Every File Manifest `Create` row names a path that does NOT already exist in the current worktree
- [x] Every ADR premise about repo state that a task relies on was re-verified against the current repo and is still true (EXTEND-NOT-REBUILD confirmed; scan-scope hole confirmed)
- [x] Every cited input a task parses/globs/reads declares its structural assumption AND the live file exists and satisfies it (no phantom inputs)
- [x] No task proposes a new artifact that duplicates an existing repo capability (no existing orchestrator/judge/safety-review/de-id/re-insertion/maintained module or scan-scope fixture)
- [x] Repo-Grounding Ledger present, with one row per task and a disposition (all 11 tasks: Grounded)
