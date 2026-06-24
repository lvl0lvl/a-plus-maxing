---
title: Session 94 — recipe stage completed + Wave 1 of the live-wiring built, 3-tier-reviewed,
  merged
type: session
date: 2026-06-24
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-94-1
---

# Session 94 — live-wiring Wave 1 (the code build begins)

**Shape:** the operator opened S94 ("write the scope contract and proceed") to BUILD the live-wiring (the design + recipes landed S93). The session completed the recipe stage (the PF-S93-01 carry-over), then built + merged WAVE 1 of the 3-wave build. Continuous, autonomous; mock/fixture-tested (0 live spend). Closed cleanly at the Wave-1 boundary (the sanctioned per-wave session model).

## What was done

1. **Recipe stage completed (PF-S93-01 carry-over).** The 12 laddered executability findings applied PER-TASK (4 remediation agents, one per recipe — the prior session's batched-remediation lesson applied), grounded against the live tree; the recipe judge pass (deferred S93) re-run → ACCEPT all dims ≥9 on all 5 recipes; promoted `draft-ADR-002x-T*.md` → `docs/task-plan/<id>.md`.
2. **Wave 1 built (`/execute-plan`), 3-tier reviewed, merged (#248 → `main` `35a312d`).**
   - **ADR-0027-T1** — the live no-train de-id backend (`_ClaudeNoTrainBackend.deidentify`): the real `claude-opus-4-8` no-train Anthropic call (swappable `MODEL`; key via `key_source.resolve` at call time, never tracked/printed/committed; bounded retries+timeout → `ModelCallError`; summary ⊆ `SUMMARY_FIELD_SET`; raw intake in-memory-only). Mock-tested via a patched anthropic SDK.
   - **ADR-0026-T1 (KEYSTONE)** — the shared control-inversion driver (`scripts/plan/plan_driver.py`): the inline revise loop EXTRACTED out of `run_orchestrated` into ONE generator-coroutine (`drive`, yield/`.send()`) both the API/test path and the future skill path drive — no fork. Behavior-preserving refactor of the wrapper; the inner engine byte-frozen.

## The 3-tier review caught + fixed real crown-jewel defects (the headline)

- **Tier-1** SE self-check (per-recipe verification checklist).
- **Tier-2** wave review (QA APPROVED + Security PASS + Architect APPROVE, all RUN-IT verified; the de-id mutation gates demonstrated-RED by mutating prod code). Security flagged one pre-existing LOW (the `deid_in` key-name-only whitelist — beaded `8d8r`, gates the live run).
- **Tier-3** FULL 6-agent `/review-pr` with both independence phases intact (profile-less blind-triage + EXECUTED blind-verify). 5 findings; the blind-triage classified 3 LEGITIMATE (fixed + blind-verified RESOLVED), 1 DEFERRED (beaded), 1 NOT_ACTIONABLE:
  - **SEC-1** (Important) — a latent **key + PII traceback leak**: the de-id `ModelCallError` chained the raw+key-bearing SDK exception via `__cause__`; the SEC-01 control + its test covered only `str()`/`.args`, NOT the rendered traceback — a future `logger.exception()`/`print_exc()` caller would leak both the raw operator PII + the live no-train key into a PUBLIC-repo log. Fixed `from None` (cause suppression) + a RED-capable traceback test; the SE also corrected a pre-existing test that was encoding the leak behavior. Blind-verified RESOLVED (the verifier mutated `from None`→`from last_exc` and re-ran to prove non-vacuity).
  - **ROLEMAP** (convergent — 3 reviewers) — the keystone extraction FORKED `_ROLE_OF_DOMAIN` (1→2 defs), a no-fork violation in the no-fork wave. Single-sourced (driver owns it, orchestrator imports it, no cycle).
  - **TEST-1** — the de-id in-memory-only scan isolated HOME+CWD but not `$TMPDIR`; the SE found env vars alone don't redirect Python's memoized `tempfile.tempdir` and patched it + made the mutation leg write a no-`dir=` tempfile.

## State at close

- pytest **1636 passed / 2 skipped**; EXTEND-NOT-REBUILD held (inner-engine numstat=0); behavior-preservation triad green. close-audit + harvest-gate green (S94).
- **No new PF** (the session executed cleanly; the per-task remediation applied the prior batched-remediation lesson). Observed-but-not-promoted: the SE per-task-sub-branch coordination nuance (caught + folded; hardened by the "specify the commit branch" build note); the Wave-2/3 deferral (the contract's escape clause).
- New beads: `8d8r` (SEC-1 de-id value-scan — land BEFORE the live run), `zsp5` (TEST-2 cap-branch test). Open: `stsq` (SEC-3 release gate), `s4i4` (PF-S93-01), `71s4`.

## Next (S95)

`/execute-plan` Wave 2 {ADR-0026-T2 gate_dispatch composer} → Wave 3 {ADR-0026-T3 skill front-door ∥ ADR-0026-T4 audit repoint — closes `71s4`/PF-S63-02}, each SE-TDD → checkpoint → `/review-pr` → `/merge`; land `8d8r` before the operator-present LIVE run (key injection). Build-execution notes for S95: specify the SE commit branch; run a wave's SE tasks sequentially (shared-working-tree git-index race).