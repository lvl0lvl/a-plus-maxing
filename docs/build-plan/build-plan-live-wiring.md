---
source-specs: [docs/spec/live-wiring-spec.md]
adrs: [ADR-0026, ADR-0027]
created: 2026-06-24
status: approved
total-waves: 3
critical-path-length: 3 tasks
estimated-effort: 5 task-days
---

# Build Plan: Plan-Generation Engine LIVE-WIRING (Live No-Train De-Id Backend + Subscription-Runtime Driver A′)

Scope: the two approved live-wiring ADRs (ADR-0026, ADR-0027) that turn the already-built, mock-tested S92 plan-generation engine into a LIVE, subscription-driven runtime. Five tasks: the live `_ClaudeNoTrainBackend.deidentify` no-train de-id call (ADR-0027-T1, the crown-jewel raw-PII egress); the KEYSTONE extraction of the inline revise loop into ONE shared control-inversion driver + the `run_orchestrated` re-point (ADR-0026-T1); the composed `gate_dispatch` adapter that maps `quality_judge` + `review_plan` into the 3-key `{accept, safety_passed, revise_domains}` disposition (ADR-0026-T2); the `/generate-plan` skill front-door reconciled to the A′ subscription path (ADR-0026-T3); the `core-capability-audit.sh` repoint onto the A′ spine + the non-tautological `--self-test` (ADR-0026-T4).

The crown-jewel obligation is 0-leak: no raw operator PII past the de-id-IN boundary, into any dispatch payload, or into any committed file; and a single un-forked fail-closed safety loop (`safety_passed is True` the only surface path). Every task WRAPS or REFACTORS-WITHIN-THE-WRAPPER — the byte-frozen INNER ENGINE (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py`) stays numstat=0; only `plan_orchestrator.py` (the WRAPPER) + the new files change. The build is MOCK/FIXTURE-tested with 0 live-API spend; the LIVE end-to-end run is the operator-present S94 checkpoint AFTER the build, NOT in any wave.

Grounded live against `feature/engine-live-wiring-build @ 2a457de` (HEAD on 2026-06-24; the spec's behavior-preservation baseline is `main @ e3d5789` at `1611 passed, 2 skipped`). The five entry-task premises were re-confirmed by reading the live files directly: the de-id stub at [client.py:156-160](../../../../scripts/model/client.py) (`NotImplementedError`, `MODEL = "claude-opus-4-8"` at :135, lazy SDK import + `key_source.resolve` at :137-142); the inline `while True:` revise loop at [plan_orchestrator.py:260-300](../../../../scripts/plan/plan_orchestrator.py) (`safety_passed is True` gate :265, accept→`_promote_plans` :271-276, `revise_cap` halt :279-280, `revise_domains` re-dispatch + out-of-run-set guard :286-294, de-id sentinel halt :229-231, dispatch_cap halt :301-305); the audit CALLER pin at [core-capability-audit.sh:47](../../../../scripts/core-capability-audit.sh) (`$REPO_ROOT/scripts/plan/generate_plan.py`); the inner-engine 8 modules all present; `plan_driver.py` / `gate_dispatch.py` (composer) / `_a_prime_self_test.py` all ABSENT; `quality_judge` ([:206](../../../../scripts/plan/quality_judge.py)) + `review_plan` ([:110](../../../../scripts/plan/safety_review.py)) present but not composed.

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| `.venv` Python 3.14 test runtime (pytest + jsonschema, per `requirements.txt`) green at the behavior-preservation baseline | Every task runs `pytest`; the `1611 passed, 2 skipped` baseline (spec @ `e3d5789`) is the precondition for the ADR-0026-T1 EXTEND-NOT-REBUILD behavior-preservation gate | `.venv/bin/python -m pytest -q` (expect `1611 passed, 2 skipped`, 0 failed; re-baseline if the live count differs and record the new number in the Wave-1 checkpoint) |
| Existing inner engine `scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` (byte-frozen) | ADR-0026-T1 drives `pipeline.run_generation` unchanged; the numstat=0 frozen-engine gate is computed against these 8 files | `for f in orchestrate pipeline assemble generate_plan adjudicate adjust track router; do test -f scripts/plan/$f.py || { echo "MISSING $f"; exit 1; }; done && echo OK` |
| Wired `ModelClient.deidentify` seam + `deid_in` + the fail-closed `_call` boundary + `_ClaudeNoTrainBackend.deidentify` stub (`scripts/model/client.py`) | ADR-0027-T1 fills the `NotImplementedError` stub behind the existing seam; `deid_in`'s `⊆ SUMMARY_FIELD_SET` whitelist + the `ModelCallError`-on-failure `_call` wrapper are the downstream gates the ACs assert | `grep -q "def deidentify" scripts/model/client.py && grep -q "NotImplementedError" scripts/model/client.py && grep -q "class ModelCallError\|ModelCallError" scripts/model/client.py && test -f scripts/plan/deid_in.py && grep -q "SUMMARY_FIELD_SET" scripts/plan/router.py && echo OK` |
| The built gate callables `quality_judge(assembled_plan, judge_client)` + `review_plan(assembled_plan, dispatch, *, lenses)` + `DEFAULT_LENSES` (`scripts/plan/quality_judge.py`, `scripts/plan/safety_review.py`) | ADR-0026-T2's composer consumes these two callables verbatim and emits the 3-key disposition; they are inputs, not re-authored | `grep -q "def quality_judge" scripts/plan/quality_judge.py && grep -q "def review_plan" scripts/plan/safety_review.py && grep -q "DEFAULT_LENSES" scripts/plan/safety_review.py && echo OK` |
| The inline revise-loop + the `gate_dispatch=` seam param + the `_promote_plans`→`store.append` site present in `run_orchestrated` (`scripts/plan/plan_orchestrator.py`) | ADR-0026-T1 extracts the `while True:` body ([:260-300]) into `plan_driver.py`; the `gate_dispatch=` seam ([:220]) is the disposition input; `_promote_plans` ([:424,:459]) is the store-write that relocates verbatim (no new store battery) | `grep -q "while True:" scripts/plan/plan_orchestrator.py && grep -q "gate_dispatch" scripts/plan/plan_orchestrator.py && grep -q "def _promote_plans" scripts/plan/plan_orchestrator.py && grep -q "store.append" scripts/plan/plan_orchestrator.py && echo OK` |
| The `anthropic` SDK is NOT installed in `.venv` (the de-id test PATCHES the lazy import site) | ADR-0027-T1 AC-1 injects a fake `Anthropic` at the lazy import site and never imports the real SDK; the absence is what proves the test is patch-driven (0 live spend) | `.venv/bin/python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('anthropic') is None else 1)" && echo "SDK absent (patch-driven test posture OK)"` |
| The governance/audit shell suite + the audit-helpers F-008 scaffold + the audit's own negative test (`scripts/tests/run-all-tests.sh`, `scripts/lib/audit-helpers.sh`, `scripts/core-capability-audit.sh`) | ADR-0026-T4 repoints the audit and re-runs the shell suite; its own negative test (an unwired path → RED) must still go RED after the repoint | `test -f scripts/tests/run-all-tests.sh && test -f scripts/lib/audit-helpers.sh && test -f scripts/core-capability-audit.sh && grep -q "audit_init\|audit_exit" scripts/lib/audit-helpers.sh && echo OK` |
| Safety-lens + specialist agents present (`.claude/agents/{medical-safety-reviewer,health-edge-case-reviewer,medical-liaison,personal-trainer,nutritionist,supplement-specialist,peptide-specialist}`) | ADR-0026-T3's skill front-door dispatches each specialist + each safety lens as a subscription agent over the de-identified summary (the documented dispatch protocol; the live dispatch is the S94 attestation) | `for a in medical-safety-reviewer health-edge-case-reviewer medical-liaison personal-trainer nutritionist supplement-specialist peptide-specialist; do test -d .claude/agents/$a || { echo "MISSING $a"; exit 1; }; done && echo OK` |

All eight prerequisites are verified live against `feature/engine-live-wiring-build @ 2a457de` on 2026-06-24. No Wave-1 task depends on an unlisted prerequisite (BP-08 clear): ADR-0027-T1 → `.venv` + the `ModelClient.deidentify` seam + the SDK-absent patch posture; ADR-0026-T1 → `.venv` baseline + the byte-frozen inner engine + the inline-loop/`gate_dispatch`/`_promote_plans` premise.

## Wave Schedule

The three waves are the spec's three Kahn levels (Dependency Map §, topological depth 3), confirmed against the spec's verified-acyclic dependency map: Wave 1 = {ADR-0027-T1, ADR-0026-T1}; Wave 2 = {ADR-0026-T2}; Wave 3 = {ADR-0026-T3, ADR-0026-T4}. Wave-to-wall-clock: a wave's duration is the max single-task estimate (tasks run in parallel). Effort proxy = files-touched × criteria-count per the wave-scheduling heuristic, with the new-external-dependency / security-review / spike modifiers applied.

### Wave 1: De-Id Crown-Jewel Boundary + Keystone Shared-Driver Extraction

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0027-T1 | Live no-train de-id backend (`_ClaudeNoTrainBackend.deidentify`) | SE + Security review + Architect review | 1.5-2 days |
| ADR-0026-T1 | Shared control-inversion driver extraction + `run_orchestrated` re-point (KEYSTONE) | SE + Architect review + Security review | 2-3 days |

**Entry Criteria:**
- All eight Infrastructure Prerequisites verified (the commands above return 0).
- `.venv/bin/python -m pytest -q` baseline green at `1611 passed, 2 skipped` (the EXTEND-NOT-REBUILD behavior-preservation precondition for ADR-0026-T1).
- `plan-integrity` has grounded the plan: every task's inputs confirmed against the LIVE tree (`stat`/`grep`, not the plan's prose), the dependency map confirmed an acyclic DAG with artifact-named edges, each wave's checkpoint confirmed runnable.

**Exit Criteria / Checkpoint (Wave 1 → Wave 2):** see Checkpoint Protocol § Wave 1. The keystone behavior-preservation TRIAD (inner-engine numstat=0 + 0 forked loop copies + full suite green) and the de-id crown-jewel 0-leak (0 raw-PII past the boundary + raw-intake-in-memory-only + fail-closed `ModelCallError`) are BOTH gated here — the risk-mitigating boundaries gate the rest of the build.

---

### Wave 2: Composed `gate_dispatch` Adapter

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0026-T2 | Composed `gate_dispatch` adapter (`quality_judge` + `review_plan` → 3-key disposition) | SE + Architect review + Security review | 1-2 days |

**Entry Criteria:**
- Wave 1 checkpoint passed (the keystone TRIAD + the de-id crown-jewel 0-leak gates all RAN green; the shared driver is independently drivable by a fixture `dispatch`, the disposition-shape contract the composer must emit is fixed by T1's extracted loop).

**Exit Criteria / Checkpoint (Wave 2 → Wave 3):** see Checkpoint Protocol § Wave 2. The composer emits EXACTLY the 3-key `{accept, safety_passed, revise_domains}` disposition; fail-closed on a malformed composite (0 `safety_passed is True` over a malformed composite → `SAFETY_BLOCKED`); both gates run (judge ≥1 dispatch + review ≥2 lenses).

---

### Wave 3: Skill Front-Door ∥ Audit Repoint + A′-Inversion Self-Test

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0026-T3 | `/generate-plan` skill front-door (the V1 subscription driver) | SE + Security review | 1-2 days |
| ADR-0026-T4 | Core-capability-audit repoint + A′-inversion `--self-test` | SE + Security review | 1-1.5 days |

**Entry Criteria:**
- Wave 2 checkpoint passed (the composer emits the exact 3-key disposition, fails closed on a malformed composite, runs both gates).
- ADR-0027-T1 complete (its de-id backend is the de-id-IN input ADR-0026-T3 calls; ADR-0027-T1 has slack — it is a Wave-1 entry consumed only here at Wave 3).

**Exit Criteria / Checkpoint (Wave 3 → Done):** see Checkpoint Protocol § Wave 3. The runtime-stage-order E2E on fixtures (de-id IN → shared-driver dispatch+assemble → composed gate → revise → promote → render); the skill front-door 0-raw-PII-to-any-dispatch + no-fork-at-skill-level; `core-capability-audit.sh` repointed onto the A′ spine + the A′-inversion `--self-test` passes (promotion-on-accept + 0-plans-on-safety-not-True, non-tautological); `scripts/tests/run-all-tests.sh` green incl. the audit's own negative test still RED on an unwired path.

## Agent Assignment Matrix

SE implements every task (TDD per recipe). Security review is on EVERY wave — the de-id boundary is the crown jewel and every task either touches the PII boundary or the fail-closed safety loop (assignment-heuristic Rule 1: security wins; a task touching the PII boundary never ships Security-unreviewed). Architect review is on Wave 1 (ADR-0027-T1 wraps the `ModelClient` seam; ADR-0026-T1 refactors the shared `run_orchestrated` control-inversion seam) AND Wave 2 (ADR-0026-T2 composes the two built gate callables into the disposition the loop reads — a cross-module gate-composition contract). QA verifies at every checkpoint (AC/checkpoint coverage). The `plan-integrity` role grounds the plan before the build and gates each wave transition (a wave advances only when its checkpoint Go/No-Go RAN green — executed, not reasoned); it is a read-only verification lens, not a deployed agent.

| Task ID | Agent | Reviewer(s) | Rationale |
|---------|-------|-------------|-----------|
| ADR-0027-T1 | SE | Architect, Security | Crown-jewel egress boundary: fills the live no-train de-id call (security-sensitive PII module — raw intake transits the API) AND wraps the `ModelClient`/`_call` seam (cross-module contract via `MODEL`/`key_source.resolve`) → both reviewers. New-external-dependency modifier (the live SDK call, patch-tested) raises the estimate. |
| ADR-0026-T1 | SE | Architect, Security | KEYSTONE cross-module refactor: extracts the inline revise loop into the shared control-inversion seam both consumers drive → Architect validates the extracted-driver contract + the byte-frozen-inner-engine boundary; the fail-closed safety loop (`safety_passed is True` the only surface path) + the no-fork single-source-of-truth are security-critical → Security. |
| ADR-0026-T2 | SE | Architect, Security | Cross-module gate composition: maps `quality_judge` + `review_plan` into the 3-key disposition the shared driver reads → Architect validates the fixed-3-key contract; the fail-closed-on-malformed-composite path (no malformed composite surfaces `safety_passed is True`) + the ≥2-lens contract are security-critical → Security. |
| ADR-0026-T3 | SE | Security | Implementation: the skill front-door dispatches each specialist + lens over the de-identified summary; the 0-raw-PII-to-any-subscription-agent probe + the no-fork-at-skill-level constraint are the crown-jewel/safety properties → Security review per the crown-jewel-on-every-wave rule. (Skill prose + thin Python glue; the live dispatch is the S94 attestation, not a mock-test target.) |
| ADR-0026-T4 | SE | Security | Implementation: the audit repoint + the A′-inversion `--self-test`; the inversion behaviors it asserts (promotion-on-accept, 0-plans-on-safety-not-True) are the fail-closed crown-jewel guarantees the PF-S63-02 guard must prove non-tautologically → Security review. |

**Multi-agent coordination flags:**
- **ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T3/T4 all rest on the extracted `plan_driver.py` contract.** They are dependency-ordered (T2 dep T1; T3 dep T1+T2+ADR-0027-T1; T4 dep T1+T2) so they never co-occupy a wave (no BP-07). The Architect-reviewed shared-driver seam from ADR-0026-T1 (the yielded dispatch-request protocol + the 3-key disposition the driver consumes) is the stable interface T2's composer emits into and T3/T4 drive; a later edit changing that contract triggers a contract-update notice to the Architect (Core Rule 10).
- **ADR-0026-T2 produces the disposition ADR-0026-T1's shared driver consumes.** The fixed 3-key `{accept, safety_passed, revise_domains}` shape (OQ-2 NOTE: a richer disposition would break the loop's single-disposition read) is the Architect-reviewed contract; the composer's internal one-pass-vs-two ordering is the build decision, but it must emit exactly that shape.
- **ADR-0026-T3 ∥ ADR-0026-T4 in Wave 3 have disjoint manifests** (`.claude/skills/generate-plan/SKILL.md` + `tests/plan/test_generate_plan_skill_glue.py` for T3; `scripts/core-capability-audit.sh` + `scripts/plan/_a_prime_self_test.py` + `tests/plan/test_a_prime_self_test.py` for T4) — no intra-wave file collision, true parallel execution.

## Checkpoint Protocol

Each criterion is a SPECIFIC command/grep/numstat/count with an expected result and a verifier role. These gates are EXECUTED at `/execute-plan` time, not reasoned. The crown-jewel 0-leak gates, the EXTEND-NOT-REBUILD (inner-engine numstat=0) gate, and the mock/fixture 0-live-spend posture are checkpoint invariants on every wave (no test opens a network socket / makes a live model call). `<wave-base>` is the merge-base of the wave's branch with `feature/engine-live-wiring-build`.

### Wave 1 → Wave 2 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/model/test_client.py -q` → all pass, 0 failures [ADR-0027-T1 crit 9]
  - `.venv/bin/python -m pytest tests/plan/test_plan_driver.py tests/plan/test_plan_orchestrator.py tests/plan/test_revise_loop.py -q` → all pass, 0 failures [ADR-0026-T1 crit 11]
  - `.venv/bin/python -m pytest -q` → `1611 passed, 2 skipped` (the behavior-preservation baseline; re-baseline only with a recorded count delta) [ADR-0026-T1 crit 3]
- **Keystone behavior-preservation TRIAD (go/no-go):**
  - **Frozen-engine:** `git diff --numstat <wave-base>..HEAD -- scripts/plan/orchestrate.py scripts/plan/pipeline.py scripts/plan/assemble.py scripts/plan/generate_plan.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/track.py scripts/plan/router.py` → 0 changed lines on every inner-engine module (`plan_orchestrator.py` — the WRAPPER — MAY change) [ADR-0026-T1 crit 1]
  - **No-fork:** a grep over `scripts/plan/plan_orchestrator.py` + `.claude/skills/generate-plan/SKILL.md` for a SECOND copy of the `while True:` gate→branch→re-dispatch sequencing / the `safety_passed is True` surface gate / the bounded-revise cap / the scratch-and-promote logic finds EXACTLY 1 definition (in `plan_driver.py`) and 0 duplicated copies [ADR-0026-T1 crit 2]
  - **Behavior-preservation:** the full suite green at the baseline above, 0 tests that passed pre-extract now failing [ADR-0026-T1 crit 3]
- **De-id crown-jewel 0-leak gates (go/no-go):**
  - **Raw-PII-past-the-boundary:** with a seeded synthetic legal name + lab value in the raw intake, the de-identified summary `deid_in` surfaces carries 0 of those raw tokens — count of raw-PII tokens past the boundary = 0 [ADR-0027-T1 crit 8]
  - **Raw-intake-in-memory-only (QA-1, non-vacuous tmp-tree rglob + mutation):** running the live-wired backend over a synthetic raw-PII intake under an isolated tmp `HOME`/`CWD` (`tmp_path` as both), then `rglob("*")` over that whole tmp tree and grep EVERY file written during the de-id call for the synthetic raw-PII token → count of files carrying the token = 0. The scan is a tmp-tree filesystem rglob (NOT only a patched-`builtins.open` write-spy — a write-spy misses `os.write`/`pathlib.Path.write_text`/`tempfile`/SDK-internal write paths). **Mutation step (proves the gate is non-vacuous):** a deliberately-injected `path.write_text(raw_intake)` inside the call boundary makes this same rglob scan find ≥1 file and go RED — asserted by a mutation test that injects the leak and expects the scan to fail, confirming the scan can detect a real on-disk raw-PII write before it is trusted. [ADR-0027-T1 crit 7]
  - **Fail-closed:** an injected SDK exception → `ModelCallError` → `deid_in` returns the `DEID_CALL_FAILED` sentinel (count of fabricated/partial summaries past the boundary = 0) [ADR-0027-T1 crit 4]; an out-of-`SUMMARY_FIELD_SET` field → `DEID_CALL_FAILED` sentinel (count of out-of-set summaries surfaced = 0) [ADR-0027-T1 crit 5]; the bounded-retry-then-fail path raises after exactly the bounded count, never unbounded [ADR-0027-T1 crit 6]; the parsed summary keys ⊆ `SUMMARY_FIELD_SET`, out-of-set keys = 0 [ADR-0027-T1 crit 3]; `MODEL`-attribute-driven model id, 0 caller-side edits to swap [ADR-0027-T1 crit 2]
  - **Key-never-committed:** the de-id key is resolved via `key_source.resolve` at call time (env→keychain), never tracked/printed/committed — `grep` over the diff for a literal key = 0 hits (the agent never reads the keychain) [ADR-0027-T1 Risk Mitigations / ADR-0005]
  - **Error-surface-carries-no-secret (SEC-4, locks the SEC-01 constant-message control):** the raised `ModelCallError` (and any de-id prompt/response surfaced on the failure path) carries no resolved-key substring AND no raw-intake substring — assert `str(exc)` and the exception's args, over a run seeded with a synthetic key + synthetic raw-PII token, contain 0 occurrences of either token. This locks the live `_call` constant-message control (`client.py` never interpolates the exception with raw input or the key) rather than adding a new control [ADR-0027-T1 Risk Mitigations / SEC-01]
- **Injected-safety-not-True (shared driver, go/no-go):** drive the shared driver via a fixture `dispatch` + a fixture disposition with `safety_passed` not boolean-True (`False`/`None`/absent/non-dict/raised) → count of plans promoted into `root` = 0 (terminal `SAFETY_BLOCKED`) [ADR-0026-T1 crit 4]; the preserved halts — de-id sentinel → 0 dispatches/0 plans (`DEID_HALTED`) [crit 7], out-of-run-set `revise_domains` → `SAFETY_BLOCKED` 0 plans [crit 8], `dispatch_cap` below tally → `DISPATCH_CAP_EXCEEDED` 0 plans [crit 9], bounded-revise non-converging → `REVISE_EXHAUSTED` 0 plans past `revise_cap` [crit 6]; promotion-on-accept → ≥1 `plan::<domain>` promoted + `dispatch_count` present [crit 5]
- **Driver-independently-drivable (go/no-go):** `plan_driver` runs end-to-end under a fixture `dispatch` with NO live client and NO skill present [ADR-0026-T1 crit 10]
- **Store-surface (go/no-go):** NO new `scripts/store/` write is added; the existing `_promote_plans`→`store.append` ([plan_orchestrator.py:459]) relocates verbatim under the keystone and is re-covered by the suite-green gate above (the S92 store-adversarial battery in `tests/plan/test_revise_loop.py` + `tests/plan/test_pipeline.py` re-runs across the extraction) — NO new store battery is authored. `grep -c "store.append" scripts/plan/plan_driver.py scripts/plan/plan_orchestrator.py` shows the write moved, not duplicated.
- **Store-seam golden-line (QA-2, go/no-go):** run an identical accept-fixture through `run_orchestrated` pre-extraction (`<wave-base>`) and post-extraction (`HEAD`), capture the promoted store lines (the raw `plan::`/`store::` keyed bytes `store.append` receives) for both, and `diff` the two captures → 0 differing lines. The existing suite asserts on `results`/`reason`, not the stored line bytes; this golden-line byte-diff makes a SILENT keying drift at the relocated `_promote_plans`→`store.append` seam go RED (same-surface-different-bytes), proving the relocation preserves the exact stored keying, not just the surfaced result shape. [ADR-0026-T1 crit 3 — extends the behavior-preservation leg]
- **Artifacts Present:** `scripts/model/client.py` (modified: live `deidentify`), `tests/model/test_client.py` (modified: patched-SDK tests), `scripts/plan/plan_driver.py` (created), `scripts/plan/plan_orchestrator.py` (modified: `run_orchestrated` re-pointed, inline loop deleted), `tests/plan/test_plan_driver.py` (created).
- **0-live-spend invariant:** `test_client.py` runs entirely against the patched `anthropic` SDK (0 live calls); `test_plan_driver.py` runs against a fixture `dispatch` (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the keystone TRIAD + the de-id crown-jewel 0-leak (incl. the non-vacuous raw-intake-in-memory-only mutation gate + the error-surface-carries-no-secret lock) + the injected-safety-not-True + the driver-drivable + the store-surface + the store-seam golden-line gates all green, no blocking defect.
- **Verifier:** Security (de-id 0-leak + the fail-closed safety loop) + Architect (the `ModelClient` seam + the extracted shared-driver contract + the frozen-engine boundary) + QA (test execution) + `plan-integrity` (gates the transition: confirms the checkpoint RAN green, executed not reasoned).

### Wave 2 → Wave 3 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_gate_dispatch.py -q` → all pass, 0 failures [ADR-0026-T2 crit 7]
- **3-key-disposition contract (go/no-go):**
  - Over an assembled result with a fixture judge returning ACCEPT-band scores AND a fixture review returning 0 findings → `{accept: True, safety_passed: True, revise_domains: []}`, asserted `set(disposition.keys()) == {"accept", "safety_passed", "revise_domains"}` — the EXACT 3 keys, no more, no fewer [ADR-0026-T2 crit 1]
  - A REVISE verdict + passing review → `{accept: False, safety_passed: True, revise_domains: [<flagged domain(s)>]}`, `revise_domains` non-empty and listing only run-set domains [ADR-0026-T2 crit 2]; a not-passed review → `safety_passed: False` regardless of judge verdict (safety dominates) [crit 3]; `revise_domains` only ever names run-set domains [crit 6]
- **Fail-closed-on-malformed (go/no-go):** a `judge_client` that RAISES, a `review` that RAISES, a non-dict judge return, or a missing key → a disposition whose `safety_passed` is NOT boolean-True (or raises in a way `_safe_gate` catches to `None`) → the loop routes to `SAFETY_BLOCKED`. Count of `safety_passed is True` dispositions over a malformed composite = 0 [ADR-0026-T2 crit 4]
- **Both-gates-run (go/no-go):** over a fixture run the judge dispatch count ≥ 1 AND the review lens dispatch count ≥ 2 (the `review_plan` ≥2-lens contract), asserted by spying both — no vacuous single-lens PASS [ADR-0026-T2 crit 5]
- **T1↔T2 composer-driver contract-seam (QA-4, go/no-go — moves the seam catch upstream from Wave 3):** feed `gate_dispatch`'s REAL output (the actual composer, not a fixture disposition) into `plan_driver`'s disposition-read path (`run_orchestrated._safe_gate` / the `safety_passed is True` surface gate) over two fixtures — (a) an accept fixture (ACCEPT judge band + 0-finding review) and (b) a malformed fixture (a raised/non-dict judge or review) — and assert the driver routes accept→`plan::` promote (≥1 plan) and malformed→`SAFETY_BLOCKED` (0 plans). This is a thin integration assertion buildable AT Wave 2 (both `gate_dispatch.py` and `plan_driver.py` exist), so a disposition-SHAPE mismatch between what T2 emits and what T1's driver reads surfaces HERE at the Wave-2 boundary, not only at the terminal Wave-3 E2E. [ADR-0026-T2 crit 1+4 ∩ ADR-0026-T1 crit 4+5 — the cross-task seam both verify in isolation]
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine files → 0 changed lines (the composer is Create-only over the built callables, edits no inner-engine/gate module).
- **Artifacts Present:** `scripts/plan/gate_dispatch.py` (created), `tests/plan/test_gate_dispatch.py` (created).
- **0-live-spend invariant:** `test_gate_dispatch.py` runs against a fixture judge/review (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the 3-key-disposition + fail-closed-on-malformed + both-gates-run + T1↔T2 composer-driver contract-seam + extend gates green, no blocking defect.
- **Verifier:** Security (the fail-closed-on-malformed path + the ≥2-lens contract) + Architect (the fixed-3-key disposition contract) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 3 → Done Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py tests/plan/test_a_prime_self_test.py -q` → all pass, 0 failures [ADR-0026-T3 crit 6; ADR-0026-T4 crit 7]
  - `.venv/bin/python -m pytest -q` → full suite green (the integrated runtime), 0 failures.
  - `bash scripts/core-capability-audit.sh` → exit 0 on the wired A′ spine [ADR-0026-T4 crit 5]
  - `bash scripts/tests/run-all-tests.sh` → exit 0; no pre-existing audit test regresses AND the core-capability audit's own negative test (a deliberately-unwired path) still goes RED [ADR-0026-T4 crit 8]
- **Runtime-stage-order E2E on fixtures (go/no-go):** the complete path — de-id IN (ADR-0027 backend, patched SDK) → shared-driver dispatch+assemble (ADR-0026-T1) → composed gate (ADR-0026-T2, real composer over fixture judge/review) → bounded revise loop → promote → render — runs end-to-end over a synthetic PII-free fixture: a plan promotes on accept, 0 plans on safety-not-True, the de-id sentinel halts to 0 plans, the dispatch_cap halts to 0 plans past the cap. (Exercises a file created by one task and consumed by another: T1's driver → T2's disposition → the run.)
- **Skill front-door crown-jewel 0-leak (go/no-go):**
  - **0-raw-PII-to-any-dispatch (QA-5, RECURSIVE payload scan):** over a synthetic raw-PII intake, every dispatch payload the glue/driver issues carries the de-identified summary only — count of raw-PII tokens in any dispatch payload = 0. The count scans the FULL serialized dispatch payload RECURSIVELY (walk every nested envelope/context field — JSON-serialize the whole payload and grep, or recurse all dict/list values — NOT just the top-level `summary` key), so a raw token smuggled into a NESTED field (e.g., an envelope's `context`/`metadata` sub-dict) goes RED. (The glue only ever holds the `deid_in` summary.) [ADR-0026-T3 crit 2]
  - **No-fork-at-skill-level:** a grep over `.claude/skills/generate-plan/SKILL.md` finds 0 copies of the `while True:` / `safety_passed is True` / scratch-and-promote control flow (the skill drives the ONE shared driver) [ADR-0026-T3 crit 3]
  - The de-id step calls the ADR-0027 `ModelClient.deidentify` path, NOT a deterministic `router.summarize` substitute as the de-id-IN [ADR-0026-T3 crit 1]; the glue feeds the shared driver a fixture envelope per yielded request and the driver completes a synthetic run [crit 4]; the skill prose documents the live subscription dispatch as the S94 attestation [crit 5]
  - **Crown-jewel property NOT closed by this build (SEC-6, make-explicit — flag for the S94 checkpoint owner):** the live-subscription-dispatch **0-raw-PII-to-a-REAL-agent** property is the ONE crown-jewel property this build's gates do NOT close. It is correctly + EXPLICITLY deferred to the S94 operator-present checkpoint. The pre-build gates here verify only the GLUE-CONTRACT level — the glue STRUCTURALLY only ever holds the de-identified `deid_in` summary (the recursive 0-raw-PII scan above proves the payload the glue BUILDS is clean), but whether a REAL subscription agent receives only the summary on the LIVE path is an operator-present observation, not a fixture assertion. **Flagged for the S94 checkpoint owner:** the live dispatch over real agents must be observed to carry the de-identified summary only — this is the residual 0-leak verification the mock-tested build cannot perform.
- **Audit repoint + A′-inversion self-test (go/no-go):**
  - **Repoint:** `grep` over `scripts/core-capability-audit.sh` finds 0 references to `generate_plan.py` as the `CALLER` and ≥1 to the A′ spine module (`plan_orchestrator.py` / `plan_driver.py`) [ADR-0026-T4 crit 1]; the structural checks assert the shared driver exists, references `pipeline.run_generation`, and the `safety_passed`/`accept`/`revise_domains` disposition gate is present — each a grep that goes RED if the path is unwired [crit 2]
  - **Non-tautological promotion-on-accept:** the `--self-test` drives the shared driver with a fixture accept disposition and asserts ≥1 plan promoted/rendered — exits non-zero if 0 plans surface on accept [ADR-0026-T4 crit 3]
  - **Non-tautological 0-plans-on-safety-not-True:** the `--self-test` drives an injected `safety_passed` not-True disposition and asserts 0 plans surface — exits non-zero if ≥1 plan surfaces past a non-True safety disposition (this is what makes the pass non-tautological — it exercises the INVERTED loop) [ADR-0026-T4 crit 4]
  - **Audit→self-test exit-code chain goes RED end-to-end (QA-3, go/no-go — closes the tautological-pass-through-exit-code hole):** drive `_a_prime_self_test.py` with a KNOWN-BROKEN spine (e.g., a promote-everything stub that surfaces a plan PAST a non-True safety disposition, inverting the fail-closed gate) and assert `bash scripts/core-capability-audit.sh` exits NON-zero. This proves the audit's BEHAVIORAL leg goes RED THROUGH the exit-code path — the audit consumes ONLY the self-test's exit code (stdout/stderr suppressed), so a self-test that printed "FAIL" but `exit 0`'d would read GREEN (the exact PF-S63-02 tautology this criterion exists to prevent). **The self-test signals failure via a NON-ZERO EXIT, NOT a printed message** — assert the broken-spine run produces a non-zero exit code AND that the audit propagates that non-zero exit (the audit does not swallow it to 0). [ADR-0026-T4 crit 3+4 — proves the exit-code chain, not just the in-process assertion]
  - The audit does NOT claim to verify the live subscription dispatch — the self-test uses a fixture `dispatch`; the live dispatch is the S94 attestation (asserted by the fixture-`dispatch` construction + an info line) [ADR-0026-T4 crit 6]
- **EXTEND-NOT-REBUILD gate:** `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine files → 0 changed lines (the skill is prose+glue; the audit repoints; the self-test drives the existing spine).
- **Artifacts Present:** `.claude/skills/generate-plan/SKILL.md` (modified: A′ subscription driver), `tests/plan/test_generate_plan_skill_glue.py` (created), `scripts/core-capability-audit.sh` (modified: A′-spine repoint + `--self-test`), `scripts/plan/_a_prime_self_test.py` (created), `tests/plan/test_a_prime_self_test.py` (created).
- **0-live-spend invariant:** `test_generate_plan_skill_glue.py` + `test_a_prime_self_test.py` + the `--self-test` all run against a fixture `dispatch` (0 live agent dispatch, 0 live spend); the live subscription dispatch is the post-build S94 operator-present checkpoint (out of plan scope).
- **Go/No-Go:** all tests pass, all artifacts present, the runtime-stage-order E2E + skill 0-leak (recursive payload scan) /no-fork + audit-repoint + non-tautological self-test + the audit→self-test exit-code chain (RED on a known-broken spine) + run-all-tests-green-incl-negative-test + extend gates green, no blocking defect. The live end-to-end subscription run is the operator-present S94 checkpoint AFTER this build (out of plan scope), and the live 0-raw-PII-to-a-REAL-agent property is the one residual crown-jewel property flagged for that checkpoint.
- **Verifier:** Security (skill 0-leak + the inversion fail-closed behaviors) + QA (full E2E + the audit's negative-test-still-RED) + `plan-integrity` (final gate: confirms the audit RAN exit-0 on the wired spine + the negative test RAN RED).

## Critical Path

```
ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T3
```

- Length: 3 tasks (Waves 1, 2, 3 — one task per wave boundary on the path).
- Zero-slack tasks: ADR-0026-T1, ADR-0026-T2, ADR-0026-T3.
- Parallel tail (also zero-slack, off the named longest chain only by tie-break): ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T4 (the wired-spine guard). T4 has the same predecessor depth as T3 and completes in the same wave, so it carries 0 wave slack; T3 is named the critical path because it is the full A′ front-door (de-id → dispatch → driver → render) and ADR-0027-T1 is its third predecessor, making T3's predecessor set strictly larger than T4's.
- The path is the longest chain: ADR-0026-T1 (Wave 1, the keystone shared driver) is the seam ADR-0026-T2 (Wave 2, the composer) emits into; both feed ADR-0026-T3 (Wave 3, the skill front-door that de-ids + dispatches + drives + renders). No shorter alternate route to ADR-0026-T3 exists (it has three predecessors: ADR-0026-T1, ADR-0026-T2, ADR-0027-T1).
- Non-critical tasks with slack:
  - **ADR-0027-T1: 2 waves slack** — a Wave-1 entry point (in-degree 0, build-independent of the driver because the keystone drives via the existing fixture `dispatch` seam), but its only consumer is ADR-0026-T3 in Wave 3. It could slip to Wave 2 without delaying completion; it is pulled to Wave 1 by the crown-jewel-boundary-first risk rule (the de-id egress boundary is built before any task that egresses over it), not by the path. The runtime-stage order puts de-id IN first, but the BUILD dependency is None (DAG §7 build-vs-runtime divergence).

## Risk Schedule

- **Spikes:**
  - NONE. This build has no separate spike task (no `T0`-suffixed research task). The two highest-risk entries — the de-id crown-jewel boundary (ADR-0027-T1) and the keystone behavior-preserving refactor (ADR-0026-T1) — are BOTH in Wave 1 as full build tasks, not spikes; their open questions (OQ-1 driver shape, OQ-4 retry mechanics) are resolved in-task during TDD, bounded by their ACs, not by a prior spike. Stated explicitly per the wave-scheduling Rule-1 exception: where the high-risk work is a build task rather than a knowledge-gathering spike, "spikes-in-Wave-1" is satisfied by placing the high-risk build tasks in Wave 1.

- **Risk-mitigating tasks (risk-mitigating-before-mitigated):**
  - **ADR-0027-T1 (Wave 1, the de-id crown-jewel boundary)** mitigates raw-PII-past-the-boundary (ADR-0027 Consequence-Negative-1/-4) — scheduled BEFORE ADR-0026-T3 (Wave 3), the skill front-door that dispatches over its de-identified-summary output. The boundary precedes the consumer by 2 waves. Its fail-closed `ModelCallError` → DEID_HALTED (AC-4) mitigates the hard-runtime-API-dependency consequence (N-3); its in-memory-only raw handling (AC-7) mitigates the new-raw-input-surface consequence (N-4).
  - **ADR-0026-T1 (Wave 1, the keystone)** mitigates the forked-safety-loop latent failure vector (ADR-0026 Falsification forked-loop probe / Consequence-Negative-2) via the single shared-driver extraction proven by 0 duplicated loop copies + the 1611-test suite green — scheduled BEFORE every task that drives the loop (ADR-0026-T2 Wave 2, ADR-0026-T3/T4 Wave 3). The behavior-preservation proof (the TRIAD) gates the rest of the build: no downstream task can build on a silently-drifted `run_orchestrated` contract.
  - **ADR-0026-T2 (Wave 2)** mitigates the malformed-composite-surfaces-a-plan vector (ADR-0026 Falsification injected-safety-not-True probe, at the composer) via the fail-closed-on-malformed disposition — in place before ADR-0026-T3/T4 (Wave 3) drive the gate end-to-end.
  - **ADR-0026-T4 (Wave 3)** mitigates the PF-S63-02 / INV-CORE-CAPABILITY core-capability-unwired regression via the non-tautological A′-inversion `--self-test` (it asserts the inversion behaviors, not just "a plan renders") — the guard that proves the spine stays wired.

- **Security-sensitive / crown-jewel ordering (the PII boundary before the egress that rests on it):**
  - The crown-jewel boundaries are built FIRST: the de-id-IN egress boundary (ADR-0027-T1) and the fail-closed shared safety loop (ADR-0026-T1, the `safety_passed is True` surface gate, extracted) are BOTH Wave 1 — before any task that dispatches over the de-identified summary (ADR-0026-T3 Wave 3) or that composes/drives the safety gate (ADR-0026-T2 Wave 2, ADR-0026-T3/T4 Wave 3).
  - The de-id-IN boundary (ADR-0027-T1, Wave 1) precedes the skill front-door (ADR-0026-T3, Wave 3) that dispatches over its de-identified output — no subscription specialist dispatch happens before the de-id boundary exists (the 0-raw-PII-to-any-dispatch gate rests on it).
  - The crown-jewel 0-leak (raw-PII-past-the-boundary + raw-intake-in-memory-only) is gated at Wave 1 (ADR-0027-T1) and re-gated at Wave 3 (ADR-0026-T3's 0-raw-PII-to-any-dispatch + no-fork-at-skill-level) — the ordering puts the 0-leak proof at the boundary BEFORE the egress that rests on it.
  - Security review is assigned on EVERY wave (every task is PII/safety-sensitive); it carries through to the terminal wave (ADR-0026-T3/T4) — not deferred past the wave where the implementation occurs.
  - **Build-vs-runtime divergence must be PRESERVED at execute time (SEC-1, verifier watch-item):** ADR-0026-T1 (the keystone) has BUILD-dependency NONE on ADR-0027-T1 — it drives a FIXTURE `dispatch`, never a live raw intake — yet at RUNTIME the only task that feeds a REAL raw intake into the driver (ADR-0026-T3, the skill front-door) DEPENDS on ADR-0027-T1, so no live raw PII can reach the driver before the de-id boundary exists. This divergence is load-bearing for the 0-leak crown jewel: a future edit that gives the keystone a LIVE raw-intake path (rather than the fixture `dispatch`) BEFORE ADR-0027-T1 lands would INVERT this property and route raw PII through the driver pre-boundary. The `plan-integrity` verifier and Security MUST confirm at execute time that ADR-0026-T1's driver is fed ONLY a fixture `dispatch` (no live de-id-IN path is introduced into the keystone) — a watch-item, not a one-time check.

**Store-surface fact:** NO task in this build adds a NEW `scripts/store/` write. The only store write on the A′ path is the existing `_promote_plans`→`store.append` ([plan_orchestrator.py:459]), which is MOVED-not-modified by the ADR-0026-T1 extraction (its scratch-and-promote logic relocates into `plan_driver.py` verbatim) and is already covered by the S92 store-adversarial battery (`docs/checklists/store-adversarial-tests.md` via `tests/plan/test_revise_loop.py` + `tests/plan/test_pipeline.py`). The Wave-1 suite-green gate (ADR-0026-T1 AC-3) re-runs that battery across the relocation, re-proving the cross-stream / same-timepoint-dedupe / dedupe-key-boundary / mutation-RED guarantees over the moved promote — so the store-adversarial obligation (bead `pka`) is satisfied by the Wave-1 suite-green gate, NOT a new battery.

Risk-ordering decision: no topological adjustment was required. The two crown-jewel boundaries fall in Wave 1 by the dependency map itself (both in-degree 0); the mitigating tasks precede the mitigated tasks by construction. (Risk ordering satisfies all wave-scheduling Rules 1-4 with no edge added or removed.)

## Cross-Spec Coordination

Single-spec plan (one source spec: `docs/spec/live-wiring-spec.md`). No cross-spec coordination required.

**Intra-spec shared-file sequencing** (within-spec, dependency-ordered — not a BP-07 violation because no two share a wave):

| Shared File | Tasks (wave) | Resolution |
|-------------|--------------|------------|
| `scripts/plan/plan_orchestrator.py` | ADR-0026-T1 (W1, Modify — `run_orchestrated` re-pointed, inline loop deleted) | Single modifier across the plan. No other task touches it (the composer, skill, and audit are Create/Modify on distinct files). No collision. |

Within-wave shared-file check (parallel-execution safety): Wave 1 {ADR-0027-T1, ADR-0026-T1} — disjoint manifests (`scripts/model/client.py` + `tests/model/test_client.py` vs `scripts/plan/plan_driver.py` + `scripts/plan/plan_orchestrator.py` + `tests/plan/test_plan_driver.py`). Wave 2 {ADR-0026-T2} — single task. Wave 3 {ADR-0026-T3, ADR-0026-T4} — disjoint (`.claude/skills/generate-plan/SKILL.md` + `tests/plan/test_generate_plan_skill_glue.py` vs `scripts/core-capability-audit.sh` + `scripts/plan/_a_prime_self_test.py` + `tests/plan/test_a_prime_self_test.py`). No intra-wave collision (BP-07 clear).

## Feedback Protocol

| Issue Type | Action | Blocks Plan? |
|-----------|--------|-------------|
| Spec defect (untestable criteria) | Flag for spec revision, log in `docs/build-plan/.pipeline/live-wiring/deviations.md`; halt the affected wave | Yes — checkpoint cannot verify the criterion |
| Missing dependency discovered | Add the edge, re-run the wave generation (Kahn), re-validate topological ordering; log the adjusted schedule | No — plan self-corrects in place |
| Acceptance criteria untestable | Flag for spec revision with the specific task-ID + criterion number | Yes — cannot verify completion |
| Scope change needed | Halt execution, escalate to user (the spec scope is fixed by ADR-0026/0027; a new requirement is a new spec/ADR) | Yes — plan scope is fixed |
| File manifest conflict (two tasks co-modify a file in one wave with no ordering) | Flag for spec revision, identify the conflicting tasks, apply non-overlap verification or add a dependency edge | Yes — execution order unclear until resolved |
| Task too large for a single wave | Split recommendation in the deviations log, adjust the wave schedule | No — plan accommodates the split |
| Missing task (coverage gap — an in-scope ADR section with no task) | Flag for spec revision naming the uncovered ADR section | Yes — plan would be incomplete |
| **Crown-jewel 0-leak gate RED at a checkpoint** | HALT the wave immediately; do NOT advance; route to the responsible task's SE for fix; re-run the full 0-leak gate before resuming | Yes — a leak past a boundary is release-blocking (ADR-0005 falsification) |
| **No-fork violation (a second copy of the revise loop)** | HALT; the duplicated loop is the latent forked-safety-loop failure vector ADR-0026 rejects; route back to SE to drive the ONE shared driver, never re-host the loop | Yes — a forked safety loop is the A-naive failure class |
| **EXTEND-NOT-REBUILD violation (non-zero numstat on an inner-engine file)** | HALT; the task must wrap/refactor-within-the-wrapper, not re-author the byte-frozen inner engine; route back to SE to re-implement against the seam | Yes — re-authoring the inner engine is out of scope by the spec's hard grounding fact |
| **0-live-spend violation (a test makes a live API call)** | HALT; replace the live call with the patched-SDK / fixture-`dispatch` seam; the live run is the post-build S94 operator checkpoint only | Yes — live spend in a build test breaks the mock-tested-posture invariant |

Blocking issues halt the pipeline with: "Spec revision needed before build-plan execution can continue. Issues: [list]. Run `/create-spec` to update the spec, then re-run `/create-build-plan`." Non-blocking issues are logged in `docs/build-plan/.pipeline/live-wiring/deviations.md` (issue, original plan state, adjusted state, justification) and execution continues.

## Validation Checklist

### Wave Integrity
- [x] Every task appears in exactly one wave (all 5 spec tasks: W1×2, W2×1, W3×2 = 5).
- [x] No task is scheduled in a wave before its dependency's wave (ADR-0026-T2 dep ADR-0026-T1: W2>W1; ADR-0026-T3 dep T1+T2+ADR-0027-T1: W3>W1,W2,W1; ADR-0026-T4 dep T1+T2: W3>W1,W2 — all strictly earlier).
- [x] Topological ordering respected across all waves (the three waves are the spec's three Kahn levels, verified against the spec Dependency Map).

### Checkpoint Quality
- [x] Every wave boundary has at least one verifiable exit criterion (3 boundaries, each with named test commands + numstat/grep/count 0-threshold gates).
- [x] Every checkpoint names specific test commands or conditions (exact `pytest`/`bash`/`git diff --numstat`/`grep`/`set(keys)==` invocations, not "run tests").
- [x] Every checkpoint identifies a verifier role (Security + Architect/QA + `plan-integrity` per boundary).

### Agent Assignment
- [x] Every spec task appears in the Agent Assignment Matrix (all 5).
- [x] No implementation task assigned to Architect (SE is primary on all 5; Architect is reviewer only on ADR-0027-T1/ADR-0026-T1/ADR-0026-T2).
- [x] No interface/contract task assigned to SE without Architect review (the three seam/contract-touching tasks — ADR-0027-T1 `ModelClient` seam, ADR-0026-T1 shared-driver seam, ADR-0026-T2 disposition contract — all carry Architect review).
- [x] Security-sensitive tasks have Security review assigned (every task — the crown-jewel-on-every-wave rule).

### Critical Path
- [x] Critical path is the actual longest chain (ADR-0026-T1→ADR-0026-T2→ADR-0026-T3, length 3 = total wave depth; verified by counting predecessor sets — T3 has 3 predecessors, the largest).
- [x] Zero-slack tasks identified (ADR-0026-T1, ADR-0026-T2, ADR-0026-T3; the parallel tail ADR-0026-T4 also 0 wave slack).
- [x] No task on the critical path has an alternative shorter route (ADR-0026-T3 has three predecessors; no shorter path to it).

### Risk Ordering
- [x] All spike tasks are in Wave 1 (NONE exist — stated explicitly; the two high-risk build entries are both in Wave 1 per the Rule-1 exception).
- [x] Risk-mitigating tasks precede the tasks they protect (ADR-0027-T1 before ADR-0026-T3; ADR-0026-T1 before T2/T3/T4; ADR-0026-T2 before T3/T4; documented in Risk Schedule).
- [x] Security ordering correct (both crown-jewel boundaries in Wave 1, before any de-identified-summary dispatch or gate-driving task; Security review through the terminal wave).

### Spec Traceability
- [x] Every spec task appears in the wave schedule (5/5; no orphan).
- [x] No task in the plan is absent from the source spec (every plan task ID traces to a spec task block).
- [x] `source-specs` frontmatter lists the consumed spec.

### Infrastructure
- [x] Every prerequisite has a verification command (8 prerequisites, each with a runnable command verified live 2026-06-24).
- [x] Wave 1 tasks do not depend on an unlisted prerequisite (ADR-0027-T1 → .venv + `ModelClient.deidentify` seam + SDK-absent posture; ADR-0026-T1 → .venv baseline + byte-frozen inner engine + inline-loop/`gate_dispatch`/`_promote_plans` premise — all listed; BP-08 clear).

### Feedback Protocol
- [x] Feedback protocol section is present.
- [x] Protocol covers: spec defect, missing dep, untestable criteria, scope change, file conflict, oversized task, missing task (+ four project-specific crown-jewel/no-fork/extend/live-spend categories).
- [x] Each issue type has a blocking/non-blocking classification.

All 24 base checklist items pass. No BP-01..BP-08 anti-pattern present (BP-01 no dependency violation; BP-02 every checkpoint has commands + verifier; BP-03 SE-primary with correct reviewers; BP-04 three waves = topological depth 3, no over-serialization; BP-05 no deferred spike — the high-risk boundaries are Wave-1; BP-06 no orphan — 5 spec tasks ↔ 5 plan tasks; BP-07 no intra-wave file collision; BP-08 no phantom infrastructure).

## Spec-Defect Scan

No BLOCKING spec defect found. Specifically:
- **No cycle** in the dependency map (Kahn terminates with all 5 tasks placed across 3 levels; the spec's own Dependency Map is verified-acyclic and was re-confirmed against the live edges).
- **No orphan task** (5 spec tasks ↔ 5 plan tasks; no phantom).
- **No untestable AC** (every criterion names a function/command/numstat/grep/count 0-threshold or a present/absent check; the spec's own Validation Checklist attests binary ACs and each was confirmed checkpoint-expressible).
- **No file-manifest collision requiring a HALT** — the one shared file (`plan_orchestrator.py`) is touched by a single task (ADR-0026-T1); documented in Cross-Spec Coordination as a single-modifier surface, not a defect.
- **No missing task** — every in-scope ADR (0026, 0027) has ≥1 task; the 6 Proceed dispositions are encoded as ACs/assumptions and the 2 Defer dispositions (OQ-3 subscription ceiling, OQ-2 retention window) are correctly task-less (operator-side/operational, post-build).
- **Grounding note (non-blocking):** the spec's behavior-preservation baseline (`1611 passed, 2 skipped`) is pinned at `main @ e3d5789`; the live HEAD is `feature/engine-live-wiring-build @ 2a457de`. The Wave-1 entry criterion re-runs the baseline and instructs a re-baseline-with-recorded-delta if the live count differs — the gate is the suite staying green across the extraction, not the absolute integer, so a benign drift in the baseline count is not a defect (the no-regression assertion holds regardless).
