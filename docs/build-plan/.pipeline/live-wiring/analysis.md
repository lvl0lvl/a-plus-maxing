# Build-Plan Analysis — Plan-Generation Engine LIVE-WIRING (from live-wiring-spec.md)

Source spec: `docs/spec/live-wiring-spec.md` (status: approved). 5 tasks, dependency map verified acyclic. The Architect reads the spec directly for full task detail; this is the extraction summary.

## a-plus path mapping
- Build plan → `docs/build-plan/build-plan-live-wiring.md`
- Working dir → `docs/build-plan/.pipeline/live-wiring/`
- Recipes (downstream) → `docs/task-plan/<task-id>.md`
- FORMAT exemplar: `docs/build-plan/build-plan-plan-gen-engine.md`

## Tasks (5) + dependency edges (acyclic, spec-verified)
| Task | Title | Deps |
|------|-------|------|
| ADR-0027-T1 | Live no-train de-id backend (`_ClaudeNoTrainBackend.deidentify`) | None (BUILD-entry) |
| ADR-0026-T1 | Shared control-inversion driver extraction + `run_orchestrated` re-point (KEYSTONE) | None (BUILD-entry — uses the existing fixture `dispatch` seam; runtime puts de-id first but the BUILD dep is None) |
| ADR-0026-T2 | Composed `gate_dispatch` adapter (quality_judge + review_plan → 3-key disposition) | ADR-0026-T1 |
| ADR-0026-T3 | `/generate-plan` skill front-door (V1 subscription driver) | ADR-0026-T1, ADR-0026-T2, ADR-0027-T1 |
| ADR-0026-T4 | Core-capability-audit repoint + A′-inversion `--self-test` | ADR-0026-T1, ADR-0026-T2 |

## Waves (Kahn levels, from the spec's Dependency Map)
- **Wave 1 (entries):** ADR-0027-T1 [de-id backend], ADR-0026-T1 [KEYSTONE driver extraction]
- **Wave 2:** ADR-0026-T2 [gate composer]
- **Wave 3:** ADR-0026-T3 [skill front-door] ∥ ADR-0026-T4 [audit repoint + self-test]

## Critical path
ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T3 (the full A′ front-door, length 3); parallel tail ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T4 (the wired-spine guard). Slack: ADR-0027-T1 has slack (entry, only consumed at Wave 3 by T3).

## Per-wave checkpoint Go/No-Go (EXECUTED, not reasoned — the cross-task integration gates)
- **Wave 1:** (keystone behavior-preservation TRIAD) inner-engine 8 modules `numstat=0` + 0 duplicated revise-loop copies (grep) + full suite green (`1611 passed / 2 skipped` baseline); (de-id crown-jewel) 0 raw-PII past the boundary + raw-intake-in-memory-only (0 files written carrying a raw token) + fail-closed `ModelCallError` on injected SDK exception/out-of-set field, all via the patched SDK; the shared driver independently drivable by a fixture `dispatch`.
- **Wave 2:** the composed `gate_dispatch` emits EXACTLY the 3-key `{accept, safety_passed, revise_domains}` disposition; fail-closed (malformed/raised composite → NOT `safety_passed is True` → SAFETY_BLOCKED; 0 `safety_passed is True` over a malformed composite); both gates run (judge ≥1 dispatch + review ≥2 lenses).
- **Wave 3:** runtime-stage-order E2E on fixtures (de-id IN → shared-driver dispatch+assemble → composed gate → revise → promote → render); skill front-door 0-raw-PII-to-any-dispatch + no-fork-at-skill-level (0 loop copies in SKILL.md); `core-capability-audit.sh` repointed onto the A′ spine + the A′-inversion `--self-test` passes (promotion-on-accept + 0-plans-on-safety-not-True, non-tautological); `scripts/tests/run-all-tests.sh` green incl. the audit's own negative test still RED on an unwired path.

## Hard constraints (carry into checkpoints)
- EXTEND-NOT-REBUILD: inner engine (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py`) numstat=0; only `plan_orchestrator.py` (the WRAPPER) + new files change. No-fork (0 dup loop copies) + behavior-preservation (suite green) are Wave-1 gates.
- MOCK/FIXTURE-tested (0 live-API spend); the LIVE end-to-end run is the operator-present S94 checkpoint AFTER the build (NOT in any wave).
- Crown-jewel PII 0-leak. Store-surface: NO task adds a new `scripts/store/` write (the existing `_promote_plans` relocates verbatim under the keystone, re-covered by the suite-green gate — note it, no new store battery).

## Agent assignment (heuristic seed)
- SE implements every task (TDD per recipe).
- Security review on every wave (crown-jewel PII boundary + the de-id backend).
- Architect review on Wave 1 (the keystone refactor touches the shared `run_orchestrated` seam) + Wave 2 (the gate composition).
- QA always (checkpoint/AC coverage). plan-integrity grounds the plan before build + gates each wave transition (a wave advances only when its checkpoint Go/No-Go RAN green).

## Test strategy → checkpoints (from the spec)
Every task's binary AC (incl. the crown-jewel 0-leak probes, the behavior-preservation triad, the fail-closed paths, the bounded-revise/dispatch-cap halts, the A′-inversion self-test) is satisfiable with MOCK clients (patched anthropic SDK; fixture dispatch/judge/review) + SYNTHETIC PII-free fixtures (0 live spend). Wave checkpoints = the wave's tasks' ACs run-and-observed + the cross-task integration (the runtime-stage-order E2E appears at Wave 3 where its constituents complete).

## File Manifest (from the spec)
Create: `scripts/plan/plan_driver.py`, `scripts/plan/gate_dispatch.py`, `scripts/plan/_a_prime_self_test.py` + 4 new test files. Modify: `scripts/model/client.py`, `tests/model/test_client.py`, `scripts/plan/plan_orchestrator.py`, `.claude/skills/generate-plan/SKILL.md`, `scripts/core-capability-audit.sh`. (Grounded: Creates absent, Modifies present.)
