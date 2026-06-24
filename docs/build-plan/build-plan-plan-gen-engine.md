---
source-specs: [docs/spec/adr-0020-0025-plan-gen-engine-spec.md]
adrs: [ADR-0020, ADR-0021, ADR-0022, ADR-0023, ADR-0024, ADR-0025]
created: 2026-06-24
status: approved
total-waves: 4
critical-path-length: 4 tasks
estimated-effort: 8 task-days
---

# Build Plan: Plan-Generation Engine (Model-Backed De-Id Envelope, Subscription Orchestrator, Quality+Safety Gates, Maintained Output)

Scope: the six approved plan-generation-engine ADRs (ADR-0020–0025), wrapping the already-built inner reconciliation+adjudication engine into a repeatable, safety-gated, end-to-end plan-generation runtime. The crown-jewel obligation is 0-leak: no raw operator PII past the de-id-IN boundary or into any committed file, and no re-inserted real PII into any tracked render. Every task in this plan WRAPS or EXTENDS the inner engine (EXTEND-NOT-REBUILD); none re-authors `generate_plans`/`assemble`/the reconciler, and none re-introduces the model client.

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| `.venv` Python 3.14 test runtime (pytest + jsonschema, per `requirements.txt`) | Every Python task (all 9 module/test tasks) runs `pytest` against the inner engine; the green baseline is the precondition for the EXTEND-NOT-REBUILD checkpoint | `.venv/bin/python -m pytest -q` (observed 2026-06-24: 1472 passed, 2 skipped, 0 failed) |
| Existing inner engine `scripts/plan/{orchestrate,pipeline,adjudicate,assemble,generate_plan,adjust,track}.py` | Every Wave-2+ task wraps/extends this engine (the orchestrator forwards `reauthor`/`adjudicator` to `generate_plans`; the judge/safety wrap `assemble`'s output; `maintained.py` wraps `render.emit` + `track`) — they cannot build against an absent engine | `for f in orchestrate pipeline adjudicate assemble generate_plan adjust track; do test -f scripts/plan/$f.py || { echo "MISSING $f"; exit 1; }; done && echo OK` |
| Wired `ModelClient.author` seam (`scripts/model/client.py`) + `_author_callable`/`AUTHOR_CALL_FAILED` (`scripts/plan/generate_plan.py`) | ADR-0020-T1 de-id-IN and ADR-0022-T1 orchestrator route through this seam; reusing it is the EXTEND-NOT-REBUILD constraint (no re-introduced client) | `test -f scripts/model/client.py && grep -q "def author" scripts/model/client.py && grep -q "AUTHOR_CALL_FAILED" scripts/plan/generate_plan.py && echo OK` |
| Render + generate surface (`scripts/generate/render.py`, `scripts/generate/generate.py`) writing to `vault/artifacts/generated/` | ADR-0025-T1 `maintained.py` re-emits through `render.emit` (`DEFAULT_OUT_DIR = vault/artifacts/generated`) — the re-emit primitive must exist | `grep -q "DEFAULT_OUT_DIR" scripts/generate/render.py && test -f scripts/generate/generate.py && echo OK` |
| Mock-client + synthetic-fixture harness (`_FixedEnvelopeClient`-style adapters; NO live API) | Every task's AC (incl. the crown-jewel 0-leak probes) is satisfiable against mock clients + synthetic PII-free fixtures; 0 live-API spend is a checkpoint invariant | `grep -q "_FixedEnvelopeClient" scripts/plan/generate_plan.py && echo "mock seam present"` |
| PII hooks + single-sourced scan scope (`.claude/hooks/{block-pii-commit,pre-push-pii-scan}.sh`, `lib/pii-scan-scope.sh`) + `vault/meta/operator-identity.txt` | ADR-0021-T0-SCANSCOPE modifies `pii-scan-scope.sh`; the 0021/0025 0-leak ACs exercise both hooks against the identity token | `test -f .claude/hooks/lib/pii-scan-scope.sh && test -f .claude/hooks/block-pii-commit.sh && test -f .claude/hooks/pre-push-pii-scan.sh && test -f vault/meta/operator-identity.txt && echo OK` |
| Safety-lens agents (`medical-safety-reviewer`, `health-edge-case-reviewer`, `medical-liaison` in `.claude/agents/`) | ADR-0024-T1 dispatches ≥2 of these independent lenses over the composed plan | `for a in medical-safety-reviewer health-edge-case-reviewer medical-liaison; do test -d .claude/agents/$a || { echo "MISSING $a"; exit 1; }; done && echo OK` |
| Store-adversarial checklist (`docs/checklists/store-adversarial-tests.md`) | ADR-0025-T1 `maintained.py` reads/writes the store via `track`; its battery is a Tier-1 + Tier-2 gate (bead `pka`) | `test -f docs/checklists/store-adversarial-tests.md && echo OK` |

All seven prerequisites verified live against `main` @ HEAD on 2026-06-24. No Wave-1 task depends on an unlisted prerequisite (BP-08 clear).

## Wave Schedule

The four waves are the analysis's four Kahn levels (topological depth 4). Wave-to-wall-clock: a wave's duration is the max single-task estimate in the wave (tasks run in parallel). Effort proxy = files-touched × criteria-count per the build-planning heuristic; all module tasks are test-only or 2-file/≤8-criteria → 1–2 days each; the spike is 2-file/6-criteria with a security-review modifier → 1 day.

### Wave 1: PII Envelope Foundation + De-Id-IN Boundary

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0021-T0-SCANSCOPE | [Spike] Fix the PII scan-scope hole on the maintained-output path | SE + Security review | 1 day |
| ADR-0020-T1 | Model-backed de-id-IN boundary over the no-train lane | SE + Security review + Architect review | 1–2 days |

**Entry Criteria:**
- All seven Infrastructure Prerequisites verified (commands above return 0).
- `.venv/bin/python -m pytest -q` baseline green (the EXTEND-NOT-REBUILD precondition).

**Exit Criteria / Checkpoint (Wave 1 → Wave 2):** see Checkpoint Protocol § Wave 1.

---

### Wave 2: OUT Re-Insertion + Outage Halt + Orchestrator Core

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0020-T2 | De-id-boundary whole-run outage → fail-closed halt | SE + Security review | 1 day |
| ADR-0021-T1 | Deterministic PII re-insertion onto the gitignored render | SE + Security review | 1–2 days |
| ADR-0022-T1 | Programmatic subscription orchestrator wrapping the inner engine | SE + Architect review + Security review | 2 days |

**Entry Criteria:**
- Wave 1 checkpoint passed (T0-SCANSCOPE + 0020-T1 ACs run-and-observed green; 0-leak gates green).

**Exit Criteria / Checkpoint (Wave 2 → Wave 3):** see Checkpoint Protocol § Wave 2.

---

### Wave 3: Quality Judge + Safety Review + Maintained Output + Dispatch Budget

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0022-T3 | Dispatch-count instrumentation + fail-closed cap | SE | 1 day |
| ADR-0023-T1 | Post-assembly plan-quality judge + rubric | SE | 1–2 days |
| ADR-0024-T1 | Multi-agent whole-plan safety review | SE + Security review | 1–2 days |
| ADR-0025-T1 | Unified maintained-HTML output (re-emit + folded tracking) | SE + Security review + QA (store battery) | 2 days |

**Entry Criteria:**
- Wave 2 checkpoint passed (orchestrator core records ≥1 plan unattended; inner-safety-gate-bypass probe = 0; de-id-IN no-train-lane-only + outage-halt green; OUT re-insertion 0-tracked-PII green).

**Exit Criteria / Checkpoint (Wave 3 → Wave 4):** see Checkpoint Protocol § Wave 3.

---

### Wave 4: Single Bounded Revise Loop (Composes Both Gates)

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0022-T2 | Single bounded revise loop (both gates, safety-blocking, N=3 halt) | SE + Architect review + Security review | 2 days |

**Entry Criteria:**
- Wave 3 checkpoint passed (quality judge + safety review both exist, fire post-assembly, and feed a loop input; maintained output 0-leak + atomic re-emit + store battery green; dispatch budget cap green).

**Exit Criteria / Checkpoint (Wave 4 → Done):** see Checkpoint Protocol § Wave 4.

## Agent Assignment Matrix

SE implements every task (TDD per recipe). QA verifies at every checkpoint and owns the store-adversarial battery on the 0025-T1 wave. Security review is on EVERY wave — every task is PII/safety-sensitive and the de-id boundary is the crown jewel (assignment-heuristic Rule 1: security wins; a task touching the PII boundary never ships Security-unreviewed). Architect review is on the two seam-touching tasks (0022-T1 wraps the inner engine; 0022-T2 composes the gates into the control flow). The `plan-integrity` role grounds the plan before the build and gates each wave transition (it is a read-only verification lens, not a deployed agent).

| Task ID | Agent | Reviewer(s) | Rationale |
|---------|-------|-------------|-----------|
| ADR-0021-T0-SCANSCOPE | SE | Security | Implementation-level spike (extends `pii-scan-scope.sh` + a fixture test); the scope change IS the crown-jewel leak guard → Security review mandatory. |
| ADR-0020-T1 | SE | Architect, Security | Crown-jewel egress boundary: routes raw intake through the no-train lane (security-sensitive PII module) AND wraps the `ModelClient` seam (cross-module contract) → both reviewers. |
| ADR-0020-T2 | SE | Security | Implementation: the fail-closed outage halt over the de-id boundary; PII-fidelity-sensitive (never degrade) → Security review. |
| ADR-0021-T1 | SE | Security | Implementation with operator-PII handling (re-inserts real name from the gitignored source); the gitignored-only/initials-only fail-closed is a security contract → Security review. |
| ADR-0022-T1 | SE | Architect, Security | Cross-module wiring: wraps `orchestrate`/`pipeline`/`adjudicate`/`assemble`/`record_plan` (3+ inner modules) → Architect validates the seam contract; dispatches the de-identified summary + inner-safety-gate-bypass probe → Security. |
| ADR-0022-T2 | SE | Architect, Security | Composes both gates into one bounded control flow (cross-module: judge + safety + reauthor seam) → Architect; the safety-block-terminal + CRITICAL-non-overridable probes are security-critical → Security. |
| ADR-0022-T3 | SE | Security | Implementation: per-plan dispatch counter + fail-closed cap, wired into the orchestrator dispatch path; fail-closed posture is the security-relevant property → Security. |
| ADR-0023-T1 | SE | Security | Implementation: the post-assembly quality judge + rubric (producer-independent); not safety-deciding but runs inside the PII-bearing plan path → Security review per the crown-jewel-on-every-wave rule. |
| ADR-0024-T1 | SE | Security | Implementation: the multi-lens whole-plan SAFETY review — load-bearing safety tier; Security review is the natural reviewer for a safety-gate task. |
| ADR-0025-T1 | SE | Security, QA | Implementation: the maintained-HTML output writing PII-bearing artifacts to the gitignored path + reading/writing the store → Security (0-leak probe); QA owns the store-adversarial battery (bead `pka`). |

**Multi-agent coordination flags:**
- **0022-T1 → 0022-T3 → 0022-T2 all touch `scripts/plan/plan_orchestrator.py`.** They are dependency-ordered (T3 dep T1; T2 dep T1+T3-companion) so they never co-occupy a wave (no BP-07). The Architect-reviewed seam contract from 0022-T1 (the `run_generation` hook signature + the `record_plan` call set) is the stable interface T2 and T3 extend; a later modification that changes that contract triggers a contract-update notice to the Architect (Core Rule 10). See Cross-Spec Coordination for the shared-file sequencing.
- **0023-T1 ∥ 0024-T1 produce the two gate inputs 0022-T2 composes.** The revise-loop topology (single loop, both gates re-run each pass, safety terminal, N=3) is the Architect-reviewed control-flow contract; both gate modules must expose a verdict the loop reads without re-adjudication (the no-double-gate constraint on 0024-T1 crit 3).

## Checkpoint Protocol

Each criterion is a SPECIFIC command with an expected result. The crown-jewel 0-leak gates and the EXTEND-NOT-REBUILD (0-shared-routine-edit) gate are checkpoint invariants on every wave. The mock/fixture 0-live-spend posture is asserted at every wave (no test opens a network socket / makes a live model call).

### Wave 1 → Wave 2 Boundary

- **Tests:**
  - `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh` → exit 0 (deny case + allow case both green) [T0-SCANSCOPE crit 5]
  - `.venv/bin/python -m pytest tests/plan/test_deid_in.py -q` → all pass, 0 failures [0020-T1 crit 4]
  - `bash scripts/tests/run-all-tests.sh` → exit 0 (no pre-existing PII-hook test regresses) [T0-SCANSCOPE crit 6]
- **Crown-jewel 0-leak gates (go/no-go):**
  - A staged `vault/artifacts/generated/plan.html` carrying the `operator-identity.txt` token is DENIED by `block-pii-commit.sh` (non-zero) AND by `pre-push-pii-scan.sh` [T0-SCANSCOPE crit 2-3]; a de-identified one is ALLOWED by both [crit 4].
  - De-id-IN call count on any training-eligible lane = 0 (asserted in `test_deid_in.py`) [0020-T1 crit 1]; post-run store-read summary raw-PII hits = 0 [0020-T1 crit 3]; raw plan-intake written to any tracked path = 0 [0020-T1 crit 5].
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD -- scripts/plan/orchestrate.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/assemble.py scripts/plan/generate_plan.py scripts/plan/adjust.py scripts/plan/track.py scripts/plan/router.py` → 0 changed lines on every inner-engine/router file (0020-T1 reuses the seam; it does not edit `router.py`) [0020-T1 crit 3 premise].
- **Artifacts Present:** `.claude/hooks/lib/pii-scan-scope.sh` (modified: `vault/artifacts/generated/` now in `DATA_BEARING_PREFIXES` and/or `PER_SE_DENY_PREFIXES`), `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh`, `scripts/plan/deid_in.py`, `tests/plan/test_deid_in.py`.
- **0-live-spend invariant:** `test_deid_in.py` runs entirely against mock clients (0 live-API calls) [0020-T1 crit 4].
- **Go/No-Go:** All tests pass, all artifacts present, all four 0-leak/extend gates green, no blocking defect.
- **Verifier:** Security (0-leak gates) + QA (test execution) + plan-integrity (gates the wave transition: confirms the checkpoint RAN green, executed not reasoned).

### Wave 2 → Wave 3 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_deid_in.py tests/plan/test_reinsert_out.py tests/plan/test_plan_orchestrator.py -q` → all pass, 0 failures [0020-T2 crit 5; 0021-T1 crit 5; 0022-T1 crit 6]
- **Crown-jewel 0-leak gates (go/no-go):**
  - After a re-inserting render, `pii_scan.scan` over `vault/store/` + the tracked set = 0 real-PII hits [0021-T1 crit 4]; a tracked target suppresses re-insertion to initials-only [0021-T1 crit 2]; `rg "ModelClient|client" scripts/plan/reinsert_out.py` = 0 model-send sites [0021-T1 crit 3].
  - Every orchestrator specialist dispatch payload raw-PII field count = 0 [0022-T1 crit 2]; each dispatch prompt contains the full role-profile required sections [0022-T1 crit 5].
- **Inner-safety-gate integration (go/no-go):**
  - Inner-safety-gate-bypass probe: plans recorded past an unadjudicated hold = 0 [0022-T1 crit 4].
  - Outage path: injected whole-run de-id outage → 0 plans recorded, 0 fallback-to-`router.summarize`-as-de-id-IN calls, judge dispatch = 0 AND safety-review dispatch = 0, existing maintained artifact byte-identical pre/post [0020-T2 crit 1-4].
- **Runtime-stage-order E2E (partial, where tasks complete):** `plan_orchestrator` runs end-to-end unattended over a synthetic fixture; `run_generation` returns `results` with ≥1 recorded `plan::<domain>` + populated `dvq_entries` [0022-T1 crit 1]; the orchestrator records nothing outside `record_plan` (spied call set) [0022-T1 crit 3].
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine/router files → 0 changed lines (the orchestrator forwards hooks to `generate_plans` verbatim; the OUT pass is model-free and standalone).
- **Artifacts Present:** `scripts/plan/reinsert_out.py`, `tests/plan/test_reinsert_out.py`, `scripts/plan/plan_orchestrator.py`, `tests/plan/test_plan_orchestrator.py` (+ the Wave-1 `deid_in.py` now carrying the outage path).
- **0-live-spend invariant:** all three test modules run against mock clients (0 live calls).
- **Go/No-Go:** All tests pass, all artifacts present, all 0-leak + inner-gate + outage + extend gates green, no blocking defect.
- **Verifier:** Security (0-leak + inner-gate-bypass) + Architect (orchestrator seam contract) + QA (E2E) + plan-integrity (gate the transition).

### Wave 3 → Wave 4 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_quality_judge.py tests/plan/test_safety_review.py tests/plan/test_dispatch_budget.py tests/generate/test_maintained.py -q` → all pass, 0 failures [0023-T1 crit 5; 0024-T1 crit 5; 0022-T3 crit 5; 0025-T1 crit 8]
- **Gate-existence + producer-independence (go/no-go):**
  - Judge fires AFTER `assemble`/`generate_plans` and BEFORE surfacing — plans surfaced without a judge verdict = 0 [0023-T1 crit 1]; judge input excludes specialist self-assessments + orchestrator notes [0023-T1 crit 2]; `vault/design/plan-quality-rubric.md` contains the four named dimensions [0023-T1 crit 4].
  - Safety review dispatches ≥2 independent lenses over the COMPOSED plan [0024-T1 crit 1]; seeded-emergent-issue (inner gate raises 0 holds) caught → drives revise/block [0024-T1 crit 2]; no-double-gate/no-gap probe (0 conflicting re-adjudications, 0 gaps) [0024-T1 crit 3]; `rg` over `safety_review.py` = 0 writes to the override-record path [0024-T1 crit 4].
- **Crown-jewel 0-leak gate (go/no-go):** re-inserted-PII-in-a-committed-render probe (threshold 0) — a maintained re-emit carrying re-inserted real PII is DENIED by `block-pii-commit.sh` AND `pre-push-pii-scan.sh` [0025-T1 crit 5, exercises the T0-SCANSCOPE coverage]; format-then-fill order holds (render BEFORE name-fill; 0 renders clobber a re-inserted name) [0025-T1 crit 6].
- **Maintained-output integration (go/no-go):** re-emit preserves prior annotations/tracking (lost prior entries = 0) [0025-T1 crit 1]; single-file/<500KB/0-external-request budget held [0025-T1 crit 2]; tracking renders into the maintained format as a folded section [0025-T1 crit 3]; injected mid-write partial re-emit leaves 0 partial-state artifacts (atomic temp-then-rename) [0025-T1 crit 4].
- **Store-adversarial battery (`pka`, go/no-go):** `maintained.py` store read/write paths satisfy `docs/checklists/store-adversarial-tests.md` — cross-stream collision (domain-X read never returns Y), same-timepoint dedupe on `track.record_tracking`, dedupe-key boundary, mutation observed RED — verified in `test_maintained.py` at Tier-1 self-check AND Tier-2 QA dispatch [0025-T1 crit 7].
- **Dispatch budget (go/no-go):** count accrues across every dispatch = the dispatch tally [0022-T3 crit 1]; cap-below-tally HALTS to honest/partial no-plan (plans past cap = 0) [0022-T3 crit 2]; cap is configurable (two configs over one fixture) [0022-T3 crit 3].
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine files → 0 changed lines (the judge/safety wrap `assemble`'s output; `maintained.py` wraps `render.emit`/`track`; none edits `adjudicate`/the reconciler).
- **Artifacts Present:** `scripts/plan/quality_judge.py`, `vault/design/plan-quality-rubric.md`, `tests/plan/test_quality_judge.py`, `scripts/plan/safety_review.py`, `tests/plan/test_safety_review.py`, `scripts/plan/dispatch_budget.py`, `tests/plan/test_dispatch_budget.py`, `scripts/generate/maintained.py`, `tests/generate/test_maintained.py`.
- **0-live-spend invariant:** all four test modules run against mock judge/lens clients (0 live calls).
- **Go/No-Go:** All tests pass, all artifacts present, the 0-leak + gate-existence + store-battery + budget + extend gates green, no blocking defect.
- **Verifier:** Security (0-leak + safety-tier) + QA (store battery + E2E) + plan-integrity (gate the transition).

### Wave 4 → Done Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_plan_orchestrator.py -q` → all pass including the three revise-loop probes [0022-T2 crit 6]
  - `.venv/bin/python -m pytest -q` → full suite green (the integrated runtime), 0 failures.
- **Revise-loop topology (go/no-go):**
  - Seeded clearable quality miss → plan surfaced within ≤3 passes via `reauthor`, both gates re-run [0022-T2 crit 1]; both gates re-run after every pass (spied) [0022-T2 crit 4].
  - Standing-safety-block-terminal probe: standing safety finding re-firing every pass → plans surfaced = 0 [0022-T2 crit 2].
  - Bounded-revise probe: non-converging quality miss → HALT at N=3, plans past N=3 = 0 [0022-T2 crit 3].
  - Seeded CRITICAL/H1-H2 non-overridable probe: seeded CRITICAL/H1-H2 inner hold + override record → 0 plans surfaced past it via any revise pass [0022-T2 crit 5].
- **Full runtime-stage-order E2E (go/no-go):** the complete path — de-id IN (0020) → orchestrate/assemble (0022 + inner engine) → {judge ∥ safety} → revise loop → maintained render (0025) → de-id OUT (0021) — runs end-to-end over a synthetic fixture, records a plan + DVQ, the gates fire in stage order, the loop composes both gates, the maintained artifact is re-emitted. Format-then-fill ordering preserved (render before name-fill).
- **Crown-jewel 0-leak gate (go/no-go):** full-suite run leaves 0 real-PII hits in `vault/store/` + the tracked set (`pii_scan.scan` post-run = 0).
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine files → 0 changed lines (the loop is orchestrator-owned control flow over the reauthor seam).
- **Artifacts Present:** `scripts/plan/plan_orchestrator.py` (now carrying the revise-loop control flow), updated `tests/plan/test_plan_orchestrator.py`.
- **0-live-spend invariant:** the loop probes run against mock clients (0 live calls).
- **Go/No-Go:** All tests pass, the revise-loop + full-E2E + 0-leak + extend gates green, no blocking defect. The live end-to-end run is the operator-present checkpoint AFTER this build (out of plan scope).
- **Verifier:** Security (safety-terminal + CRITICAL-non-overridable) + Architect (control-flow contract) + QA (full E2E) + plan-integrity (final gate).

## Critical Path

```
ADR-0020-T1 → ADR-0022-T1 → {ADR-0023-T1 ∥ ADR-0024-T1} → ADR-0022-T2
```

- Length: 4 tasks (Waves 1, 2, 3, 4 — one task per wave boundary on the path).
- Zero-slack tasks: ADR-0020-T1, ADR-0022-T1, ADR-0023-T1 (and the parallel ADR-0024-T1 — either gate is on the path since 0022-T2 needs both), ADR-0022-T2.
- The path is the longest chain: 0020-T1 (Wave 1) is the de-id-IN input contract the orchestrator (0022-T1, Wave 2) rests on; the orchestrator feeds both gates (0023-T1/0024-T1, Wave 3); the revise loop (0022-T2, Wave 4) composes both gates. No shorter alternate route exists to 0022-T2 (it has three predecessors: 0022-T1, 0023-T1, 0024-T1 — all on or feeding the path).
- Non-critical tasks with slack:
  - ADR-0021-T0-SCANSCOPE: 1 wave slack — Wave 1 entry, but its only successors (0021-T1 Wave 2, 0025-T1 Wave 3) are off the critical path; it is pulled to Wave 1 by the spike rule, not the path.
  - ADR-0020-T2: 2 waves slack — Wave 2, depends only on 0020-T1, no successor (terminal outage path); could slip to Wave 4 without delaying completion.
  - ADR-0021-T1: 1 wave slack — Wave 2, feeds only 0025-T1 (Wave 3, off-path); not on the longest chain.
  - ADR-0022-T3: 1 wave slack — Wave 3, depends only on 0022-T1, terminal (cap mechanism); could slip without impact.
  - ADR-0025-T1: 1 wave slack — Wave 3, terminal (the maintained output), no successor task; off the longest chain to 0022-T2.

## Risk Schedule

- **Spikes:**
  - ADR-0021-T0-SCANSCOPE — Wave 1. Implementation-level spike (closes the scan-scope hole that is a hard dependency of every PII-re-insertion (0021-T1) and maintained-output (0025-T1) task). Risk ordering: no adjustment needed — the topological sort already places it in Wave 1 (it is a true entry point, in-degree 0).

- **Risk-mitigating tasks (risk-mitigating-before-mitigated):**
  - ADR-0021-T0-SCANSCOPE (Wave 1) mitigates the crown-jewel name-scan-scope leak (ADR-0021 Consequence-Negative-2 / ADR-0025 Consequence-Negative-3) — scheduled BEFORE the egress that rests on it: ADR-0021-T1 (Wave 2) and ADR-0025-T1 (Wave 3). The mitigating boundary precedes the mitigated tasks by ≥1 wave.
  - ADR-0020-T1 (Wave 1, the de-id-IN boundary, the crown-jewel egress) mitigates raw-PII-past-the-boundary (ADR-0020 Consequence-Negative-1) — scheduled BEFORE the orchestrator (ADR-0022-T1, Wave 2) that consumes its de-identified-summary output contract. The boundary precedes the consumer.
  - ADR-0020-T2 (Wave 2) mitigates the whole-run outage silent-degrade (ADR-0020 OQ-4 / Consequence-Negative-4) — it is the fail-closed halt; scheduled in the same path as the orchestrator's first plan run, after the boundary it extends (0020-T1).
  - ADR-0024-T1 (Wave 3) mitigates the lost-per-dispatch-human-checkpoint (ADR-0022 Consequence-Negative-1) by routing safety onto the load-bearing tier — feeds the revise loop (0022-T2, Wave 4) that the safety findings block.
  - ADR-0022-T3 (Wave 3) mitigates aggregate-dispatch-volume vs the subscription ceiling (ADR-0022 OQ-4) — the fail-closed cap; in place before the revise loop (0022-T2, Wave 4) that multiplies dispatch volume.

- **Security-sensitive ordering (the crown-jewel boundary before the egress that rests on it):**
  - The PII boundaries are built FIRST: the scan-scope leak guard (T0-SCANSCOPE) and the de-id-IN egress boundary (0020-T1) are both Wave 1, before any task that produces a PII-bearing artifact (0021-T1 re-insertion Wave 2, 0025-T1 maintained output Wave 3) or that egresses raw intake (0022-T1 orchestrator Wave 2).
  - The de-id-IN boundary (0020-T1, Wave 1) precedes the orchestrator (0022-T1, Wave 2) that dispatches over its de-identified output — no specialist dispatch happens before the de-id boundary exists.
  - The OUT re-insertion (0021-T1, Wave 2) cannot ship its gitignored-only target until the scan-scope coverage (T0-SCANSCOPE, Wave 1) backs the 0-committed-PII gate — the dependency edge enforces it.
  - Security review is assigned on EVERY wave (every task is PII/safety-sensitive); the safety tier (0024-T1) and the safety-blocking revise loop (0022-T2) carry Security review through to the terminal wave — not deferred past the wave where the implementation occurs.

Risk-ordering decision: no topological adjustment was required. The spike and both crown-jewel boundaries fall in Wave 1 by the dependency map itself; the mitigating tasks precede the mitigated tasks by construction.

## Cross-Spec Coordination

Single-spec plan (one source spec: `docs/spec/adr-0020-0025-plan-gen-engine-spec.md`). No cross-spec coordination required.

**Intra-spec shared-file sequencing** (within-spec, dependency-ordered — not a BP-07 violation because no two share a wave):

| Shared File | Tasks (wave) | Resolution |
|-------------|--------------|------------|
| `scripts/plan/plan_orchestrator.py` | 0022-T1 (W2, Create) → 0022-T3 (W3, Modify) → 0022-T2 (W4, Modify) | Dependency-ordered: T3 dep T1, T2 dep T1. No two in the same wave. T1's seam (`run_generation` hook signature + `record_plan` call set) is the stable contract T3/T2 extend; a contract-changing edit notifies Architect (Core Rule 10). |
| `scripts/plan/deid_in.py` | 0020-T1 (W1, Create) → 0020-T2 (W2, Modify, adds outage path) | Dependency-ordered (T2 dep T1). Sequential by wave; T2 adds the whole-run outage branch without touching T1's per-call contract. |
| `tests/plan/test_deid_in.py` | 0020-T1 (W1, Create) → 0020-T2 (W2, append outage cases) | Same ordering; T2 appends cases, does not rewrite T1's. |
| `tests/plan/test_plan_orchestrator.py` | 0022-T1 (W2, Create) → 0022-T3 (W3, append) → 0022-T2 (W4, append revise-loop probes) | Same ordering; each appends its task's cases. |

Within-wave shared-file check (parallel-execution safety): Wave 1 {T0-SCANSCOPE, 0020-T1} — disjoint manifests (hooks vs `deid_in.py`). Wave 2 {0020-T2, 0021-T1, 0022-T1} — disjoint (`deid_in.py` / `reinsert_out.py` / `plan_orchestrator.py`; 0020-T2 and 0022-T1 do not co-modify any file). Wave 3 {0022-T3, 0023-T1, 0024-T1, 0025-T1} — 0022-T3 modifies `plan_orchestrator.py` (created W2, sequenced); the other three are disjoint new files. Wave 4 {0022-T2} — single task. No intra-wave collision (BP-07 clear).

## Feedback Protocol

| Issue Type | Action | Blocks Plan? |
|-----------|--------|-------------|
| Spec defect (untestable criteria) | Flag for spec revision, log in `docs/build-plan/.pipeline/engine/deviations.md`; halt the affected wave | Yes — checkpoint cannot verify the criterion |
| Missing dependency discovered | Add the edge, re-run the wave generation, re-validate topological ordering; log the adjusted schedule | No — plan self-corrects in place |
| Acceptance criteria untestable | Flag for spec revision with the specific task-ID + criterion number | Yes — cannot verify completion |
| Scope change needed | Halt execution, escalate to user (the spec scope is fixed; a new requirement is a new spec/ADR) | Yes — plan scope is fixed |
| File manifest conflict (two tasks co-modify a file in one wave with no ordering) | Flag for spec revision, identify the conflicting tasks, apply non-overlap verification or add a dependency edge | Yes — execution order unclear until resolved |
| Task too large for a single wave | Split recommendation in the deviations log, adjust the wave schedule | No — plan accommodates the split |
| Missing task (coverage gap — an in-scope ADR section with no task) | Flag for spec revision naming the uncovered ADR section | Yes — plan would be incomplete |
| **Crown-jewel 0-leak gate RED at a checkpoint** | HALT the wave immediately; do NOT advance; route to the responsible task's SE for fix; re-run the full 0-leak gate before resuming | Yes — a leak past a boundary is release-blocking (ADR-0005 falsification) |
| **EXTEND-NOT-REBUILD violation (non-zero numstat on an inner-engine file)** | HALT; the task must wrap/extend, not re-author; route back to SE to re-implement against the seam | Yes — re-authoring the inner engine is out of scope by the spec's hard grounding fact |
| **0-live-spend violation (a test makes a live API call)** | HALT; replace the live call with the mock/`_FixedEnvelopeClient` seam; the live run is the post-build operator checkpoint only | Yes — live spend in a build test breaks the mock-tested-posture invariant |

Blocking issues halt the pipeline with: "Spec revision needed before build-plan execution can continue. Issues: [list]. Run `/create-spec` to update the spec, then re-run `/create-build-plan`." Non-blocking issues are logged in `docs/build-plan/.pipeline/engine/deviations.md` (issue, original plan state, adjusted state, justification) and execution continues.

## Validation Checklist

### Wave Integrity
- [x] Every task appears in exactly one wave (all 10 spec tasks: W1×2, W2×3, W3×4, W4×1 = 10).
- [x] No task is scheduled in a wave before its dependency's wave (every Dependencies entry resolves to a strictly-earlier wave — verified against the spec Dependency Map).
- [x] Topological ordering respected across all waves (the four waves are the four Kahn levels).

### Checkpoint Quality
- [x] Every wave boundary has at least one verifiable exit criterion (4 boundaries, each with named test commands + 0-threshold gates).
- [x] Every checkpoint names specific test commands or conditions (exact `pytest`/`bash`/`git diff --numstat`/`rg` invocations, not "run tests").
- [x] Every checkpoint identifies a verifier role (Security + QA + Architect/plan-integrity per boundary).

### Agent Assignment
- [x] Every spec task appears in the Agent Assignment Matrix (all 10).
- [x] No implementation task assigned to Architect (SE is primary on all 10; Architect is reviewer only on 0020-T1/0022-T1/0022-T2).
- [x] No interface/contract task assigned to SE without Architect review (the two seam-touching tasks carry Architect review).
- [x] Security-sensitive tasks have Security review assigned (every task — the crown-jewel-on-every-wave rule).

### Critical Path
- [x] Critical path is the actual longest chain (verified by counting: 0020-T1→0022-T1→{0023-T1∥0024-T1}→0022-T2, length 4 = total wave depth).
- [x] Zero-slack tasks identified (0020-T1, 0022-T1, 0023-T1, 0024-T1, 0022-T2).
- [x] No task on the critical path has an alternative shorter route (0022-T2 has three predecessors; no shorter path to it).

### Risk Ordering
- [x] All spike tasks are in Wave 1 (T0-SCANSCOPE).
- [x] Risk-mitigating tasks precede the tasks they protect (T0-SCANSCOPE before 0021-T1/0025-T1; 0020-T1 before 0022-T1; documented in Risk Schedule).
- [x] Security ordering correct (both crown-jewel boundaries in Wave 1, before any PII-bearing-artifact or raw-egress task; Security review through the terminal wave).

### Spec Traceability
- [x] Every spec task appears in the wave schedule (10/10; no orphan).
- [x] No task in the plan is absent from the source spec (every plan task ID traces to a spec task block).
- [x] `source-specs` frontmatter lists the consumed spec.

### Infrastructure
- [x] Every prerequisite has a verification command (7 prerequisites, each with a runnable command verified live 2026-06-24).
- [x] Wave 1 tasks do not depend on an unlisted prerequisite (T0-SCANSCOPE → hooks+identity-token+`run-all-tests.sh`; 0020-T1 → .venv+inner-engine+ModelClient-seam+mock-harness — all listed; BP-08 clear).

### Feedback Protocol
- [x] Feedback protocol section is present.
- [x] Protocol covers: spec defect, missing dep, untestable criteria, scope change, file conflict, oversized task, missing task (+ three project-specific crown-jewel/extend/live-spend categories).
- [x] Each issue type has a blocking/non-blocking classification.

All 24 base checklist items pass. No BP-01..BP-08 anti-pattern present (BP-01 no dependency violation; BP-02 every checkpoint has commands; BP-03 SE-primary with correct reviewers; BP-04 four waves = topological depth, no over-serialization; BP-05 spike + mitigators early; BP-06 no orphan; BP-07 no intra-wave file collision; BP-08 no phantom infrastructure).

## Spec-Defect Scan

No BLOCKING spec defect found. Specifically:
- **No cycle** in the dependency map (Kahn terminates with all 10 tasks placed across 4 levels).
- **No orphan task** (10 spec tasks ↔ 10 plan tasks; no phantom).
- **No untestable AC** (every criterion names a function/command/0-threshold or a present/absent check; the spec's own validation checklist attests binary ACs and I confirmed each is checkpoint-expressible).
- **No file-manifest collision requiring a HALT** — the three shared files (`plan_orchestrator.py`, `deid_in.py`, two test files) are all intra-spec and dependency-ordered so no two share a wave; documented in Cross-Spec Coordination as sequencing, not a defect.
- **No missing task** — every in-scope ADR (0020–0025) has ≥1 task; the five dispositions (one Block → T0-SCANSCOPE spike; four Proceed → 0022-T2/0020-T2/0022-T3) all have corresponding tasks.
