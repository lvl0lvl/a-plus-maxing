---
title: Session 97 — the ADR-0028 A′ gate-dispatch control-inversion, designed + built + merged end-to-end
type: session
date: 2026-06-25
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-97
---

# Session 97 — ADR-0028: making the live /generate-plan run executable

**Shape:** the operator directed "proceed and run all the way through the whole build pipeline to the session close autonomously." The session opened with a 0-spend dry-run of `/generate-plan` that found the live run was NOT executable, then ran the entire design→build→review→merge→close pipeline for the fix (ADR-0028). Continuous, autonomous; mock/fixture-tested (0 live spend). The ONLY remaining step is the operator-present LIVE run — now genuinely executable.

## The dry-run finding (the why)

A 0-spend dry-run traced the operator-facing `/generate-plan` path and found it cannot execute as designed: the A′ control-inversion (S93-S95) inverted only the AUTHOR dispatch — the GATE (quality judge + safety lenses) + the reauthor/adjudicator hooks were SYNCHRONOUS Python callables, and the Agent tool belongs to the orchestrator, not to a Python frame, so the skill cannot fulfill them with subscription agents. The author/judge/lens model backends are stubs/absent; `run_orchestrated` had no production caller. This is the PF-S87-01 "plumbing wired, end-to-end capability not" pattern — caught for $0 before any spend. Operator chose option A: complete the control-inversion.

## The full gated pipeline (each stage through its own gate)

- **ADR-0028** (`/create-adr`): AUTHOR (S97 checkpoint) → VERIFY (PASS) → RED-TEAM (caught AR-001: reauthor/adjudicator fire DEEP INSIDE the byte-frozen `orchestrate.generate_plans`, so they cannot become direct yields without editing the engine → forced the THROW/REPLAY-MEMO mechanism: a `BaseException` sentinel on a memo-cache miss unwinds to `drive`, which yields the typed request + caches the `.send()` envelope + re-drives over a fresh scratch — the engine stays byte-frozen) → JUDGE (REVISE: a false `BaseException` justification citing a nonexistent `except Exception`) → bounded revise → `status: accepted` + inverse-edge backfill. #255.
- **Spec** (`/create-spec`): 5 tasks, binary mock-satisfiable ACs; validate 11/11 + judge ACCEPT (all 11 dims ≥9). #256.
- **Build plan** (`/create-build-plan`): 4 waves T1→T2→T3→{T4,T5}; judge REVISE→fixed (added the Wave-2 consumer no-fork release-grep). #257.
- **Recipes** (`/create-task-plan`): 5 TDD recipes; judge ACCEPT (every recipe all-dims ≥9, no same-wave collision, every crown-jewel/no-fork AC RED-capable). #258.
- **Build** (`/execute-plan`): T1 typed-protocol + AUTHOR/GATE direct-yield; T2 throw/replay-memo; T3 step-harness (`plan_step.py`, OQ-5); T4 SKILL reconcile + yield-payload value-scan; T5 non-tautological replay self-test. Each wave's checkpoint EXECUTED green. #259.

## The layered review caught a real crown-jewel defect at TWO layers (the headline)

- **Tier-2 (Wave-1 Architect):** the build shipped the GATE as a COMPOSED callable — the ADR-rejected shape (OQ-2 requires the RAW-VERDICT producer the skill needs to dispatch judge/lenses as agents). MUST-FIX → fixed (`compose_disposition` is the ONE composition site; the GATE yields `(assembled_plan, gate_producer)`) → Architect re-review RESOLVED (executed-verified, drove the generator with an exploding producer that's never invoked).
- **Tier-3 (the full 6-agent `/review-pr` over the integrated diff):** **BUG-1 (Critical)** — the `plan_step` step-harness skips caching a `None` hook return, so the SAFE-default outcome (a declined re-author → workout HELD; a declined adjudication → the hold stands) INFINITE-LOOPS the production skill path. Three agents converged (Bug-Hunter + Test-Coverage + Historical-Context), Test-Coverage RAN it (harness never terminates; synchronous terminates after 1). All 4 per-wave EXECUTED checkpoints + the green 1718-test suite MISSED it — because a per-wave checkpoint tests one task in isolation; only the integrated review composes all 5. + BUG-2 (the harness GATE-raise fail-closed path dead) + QUAL-1/QUAL-2 (stale doc refs). Profile-less blind-triage: all 4 LEGITIMATE. Fixed (3 commits) + EXECUTED blind-verify: all 4 RESOLVED (mutation→RED non-vacuity). → `/merge` PR #259 → `main` `747ff39`.

## State at close

- pytest **1721 passed / 2 skipped** on `main` `747ff39`; core-cap audit exit 0; EXTEND-NOT-REBUILD held (inner engine + `deid_in.py` numstat=0); NO-FORK 1/1/1 across all 4 consumers. The V1 A′ runtime is fully built + integrated + executable.
- **One new PF (PF-S97-01):** a review agent ran `git checkout`/`reset` in the shared checkout mid-build, corrupting the tree (QA caught it via reflog; recovered, no loss). Guard: review/verify agents use read-only git only — applied for the rest of the session.
- Beads: created `fbyr` (PF-S97-01). Carry: `6hts` (de-id value-scan residuals) + `stsq` (SEC-3) before the real-PII run; `f0gh`, `myts`, `zsp5`.

## Next

The operator-present LIVE run — `/generate-plan` synthetic-first (real dispatch + real de-id spend, 0 real PII), then real data; the operator injects the no-train key. Land `6hts` (value-scan residuals) + observe `stsq` (live-dispatch 0-leak) before real PII. The build is complete; the run is now genuinely executable.
