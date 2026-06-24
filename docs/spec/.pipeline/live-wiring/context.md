# Spec Context — Plan-Generation Engine LIVE-WIRING (ADR-0026 + ADR-0027)

Scope: the 2 live-wiring ADRs, merged main @ e3d5789. The spec author reads each ADR IN FULL (docs/adr/ADR-0026-*.md, ADR-0027-*.md); this file carries the cross-ADR extraction + the a-plus conventions + the live-grounding map.

## a-plus path mapping (the spec pipeline's `specs/` → a-plus `docs/spec/`)
- Final spec → `docs/spec/live-wiring-spec.md`
- Working dir → `docs/spec/.pipeline/live-wiring/`
- Recipes (downstream) → `docs/task-plan/<task-id>.md`; build plan → `docs/build-plan/`
- FORMAT exemplar: `docs/spec/adr-0020-0025-plan-gen-engine-spec.md` (same project, same pipeline)

## The 2 decisions + their dependency (from docs/adr/.pipeline/live-wiring/dag.md)
- **Tier 1 — ADR-0027** (live no-train API de-id backend; implements ADR-0020's boundary). Entry task — depends only on existing merged code.
- **Tier 2 — ADR-0026** (V1 subscription-runtime driver A′; the keystone; amends ADR-0022). depends-on ADR-0027 (the driver consumes the de-id backend — de-id IN is the first runtime stage).

## RUNTIME STAGE ORDER (the live A′ control flow — distinct from dependency tiers)
de-id IN (ADR-0027 live backend, via the ADR-0020 boundary) → the SKILL dispatches subscription specialist AGENTS + assemble (ADR-0026 driver + the inner engine `pipeline.run_generation`) → {quality judge ∥ safety review} composed via gate_dispatch (ADR-0026) → bounded revise loop (the shared inverted driver) → de-id OUT (deterministic, ADR-0021, already built) → maintained render (ADR-0025, already built).

## EXTEND-NOT-REBUILD (hard grounding fact — encode in every task AC)
The byte-frozen set is the INNER ENGINE: `scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` (numstat=0). `scripts/plan/plan_orchestrator.py` (`run_orchestrated`) is the S92-authored WRAPPER and TAKES the behavior-preserving control-inversion refactor (the keystone). The no-fork proof = 0 duplicated copies of the revise-loop control flow (grep). The behavior-preservation proof = the full existing suite (1611 passed / 2 skipped) stays green.

## Live-grounding map (ground every task against these — NOT the ADR prose alone)
- `scripts/plan/plan_orchestrator.py` — `run_orchestrated` @ :136; inline revise loop @ ~260-300; synchronous dispatch site `authors[domain]=dispatch(...)` @ :369; helpers `_dispatch_domains`/`_safe_gate`/`_promote_plans`/`_honest_no_plan`; disposition keys consumed @ :265 (safety_passed is True) / :271 (accept) / :286 (revise_domains); dispatch_cap @ :301-305; de-id sentinel halt @ :229-231.
- `scripts/model/client.py` — `_ClaudeNoTrainBackend.deidentify` NotImplementedError stub @ ~156; `from anthropic import Anthropic` @ ~138; `ModelCallError`; `MODEL` attribute (`claude-opus-4-8`); `_FixedEnvelopeClient` mock; the backend-injection swap @ ~44-45.
- `scripts/plan/deid_in.py` — `deid_in(raw_intake, client)`; enforces `set(summary) ⊆ router.SUMMARY_FIELD_SET`; fail-closed to `{"deidentified": False, "reason": DEID_CALL_FAILED, ...}` catching Exception.
- `scripts/plan/{quality_judge,safety_review,reinsert_out}.py` — gate return shapes (`quality_judge → {verdict: ACCEPT|REVISE}`, `review_plan → {passed, findings, lenses}`); `reinsert_out` deterministic.
- `scripts/plan/router.py` — `SUMMARY_FIELD_SET`.
- `scripts/generate/maintained.py` — `reemit_maintained`.
- `scripts/core-capability-audit.sh` — the `CALLER=` pin @ ~47 (currently `generate_plan.py` — repoint onto the A′ spine).
- `.claude/skills/generate-plan/SKILL.md` — the superseded runtime-A skill (the V1 front-door to reconcile to the built A′ driver).
- `scripts/model/key_source.py` — `key_source.resolve` @ :64-90 (call-time env key, no keychain read, never tracked/printed/committed).

## Constraint propagation (encode in task ACs)
- ADR-0001 (summaries-not-raw) → every subscription dispatch over the de-identified summary (⊆ SUMMARY_FIELD_SET).
- ADR-0005 (no-committed-PII) → the API key + the raw plan-intake never tracked/committed; raw intake in-memory only (disposition #7).
- ADR-0016 (egress relaxation) → the de-id call is the bounded 2nd raw-egress class (no-train lane).
- ADR-0015 (swappable client) → the MODEL id + the de-id backend stay swappable (the all-API path is run_orchestrated with a programmatic dispatch).

## Build-test posture
Whole build is MOCK/FIXTURE-tested (0 live-API spend): the deidentify backend via a patched anthropic SDK; the skill-driven subscription dispatch via fixture envelopes; the shared driver via a programmatic/fixture dispatch. NO task makes a live API call. The LIVE end-to-end run is the operator-present S94 checkpoint AFTER the build.

## Dispositions
See `dispositions.md` (Phase 3 COMPLETE): 6 PROCEED (documented as assumptions/ACs — incl. the load-bearing #7 raw-intake-in-memory-only AC on the deidentify task), 2 DEFER (ADR-0026 OQ-3 subscription rate ceiling + ADR-0027 OQ-2 retention window — operator-side/operational, post-build), 0 BLOCK.

## Likely task shape (the spec's Dependency Map sizes it precisely)
1. **ADR-0027-T1** — the live `_ClaudeNoTrainBackend.deidentify` (no-train API call; fail-closed ModelCallError; summary ⊆ SUMMARY_FIELD_SET; raw intake in-memory-only; mock-tested via patched SDK). Entry.
2. **ADR-0026-T1** — the shared control-inversion driver extraction + run_orchestrated re-point (keystone behavior-preserving refactor; inner engine numstat=0; suite green; 0 forked loop copies). depends-on T-de-id? No — the driver refactor is pure control flow; it depends on the existing run_orchestrated, not the live backend. Verify the dependency direction against the runtime stage order vs the build dependency.
3. **ADR-0026-T2** — the composed gate_dispatch adapter (quality_judge ∥ review_plan → 3-key disposition; fail-closed → SAFETY_BLOCKED).
4. **ADR-0026-T3** — the `/generate-plan` skill front-door (the V1 subscription driver: de-id via the ADR-0027 API client → dispatch specialists/lenses as subscription agents → drive the shared driver → reinsert_out → maintained render; reconcile the superseded skill).
5. **ADR-0026-T4** — the core-capability-audit repoint + the A′-inversion fixture `--self-test` (CALLER onto the A′ spine; promotion-on-accept + 0-plans-on-not-True).
(Out-of-scope downstream: operator-data ingestion + the live run = operator-side / S94.)
The spec author VERIFIES this shape against the ADRs + the live tree and sizes/splits/merges as the dependency map requires.
