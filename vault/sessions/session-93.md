---
title: Session 93 — the plan-generation engine LIVE-WIRING, designed + recipe'd via
  the full design pipeline
type: session
date: 2026-06-24
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-93
---

# Session 93 — engine live-wiring (the design pipeline; the code build set up for S94)

**Shape:** the operator settled the runtime-dispatch fork (PII → no-train API; everything else → subscription) and directed "run the full session close and set up the rest of the build for the next session (complete everything needed to get us to the live test)." Continuous, autonomous. The session ran the full DESIGN pipeline for the live-wiring (ADR → spec → build-plan → recipes); the CODE build (`/execute-plan`) is set up for S94.

## What was designed (the live-wiring)

The runtime that connects the S92-built engine to real clients, so the only remaining step is the operator-present live test:

- **ADR-0026 — V1 subscription-runtime driver A′** (skill-as-orchestrator, control-flow-inverted): the `/generate-plan` skill drives subscription specialist + gate-lens AGENT dispatch (the operator's "subscription for everything else"); the fail-closed safety loop stays in Python as a SINGLE source of truth via a behavior-preserving control-inversion REFACTOR of `run_orchestrated` (extract the revise loop into ONE shared driver both the skill and the API/test path drive — no fork). Amends ADR-0022.
- **ADR-0027 — live no-train API de-identification backend** (`_ClaudeNoTrainBackend.deidentify`): the real no-train Anthropic call over raw PII (`claude-opus-4-8`, the swappable `MODEL` seam; the no-train property is a key/account property, NOT a fabricated per-request flag; key runtime-only/never-committed; fail-closed to `ModelCallError`; summary ⊆ `SUMMARY_FIELD_SET`; raw intake in-memory-only). Implements ADR-0020.

## The pipeline + the layered review (the headline)

`/create-adr` (8-phase; judge ACCEPT 10/10 both ADRs; red-team) → `/create-spec` (ACCEPT 10/10) → `/create-build-plan` (ACCEPT 10/10) → 5 `/create-task-plan` recipes (authored + reviewed). PR #247 merged the ADRs → `main` `e3d5789` (3-agent docs `/review-pr`, QUAL-1 fixed; rebase). Spec/build-plan/recipes committed on `feature/engine-live-wiring-build`.

The layered review caught a REAL defect at every layer BEFORE the build — the operator's stated meta-goal (the pipeline informs how the health-plan pipeline gets organized):
- **`/create-adr` red-team:** RT-01 (the keystone "no-fork by sharing helpers, run_orchestrated byte-frozen" claim is not mechanically realizable for the revise loop — corrected to a behavior-preserving control-inversion refactor; the freeze is the INNER ENGINE, not the wrapper) + RT-02 (the core-capability-audit cannot verify the skill-driven A′ path with a shell grep — the audit asserts the deterministic SPINE, the live dispatch is the S94 attestation). Both fixed in the ADRs before merge.
- **`/create-build-plan` QA+Security review:** hardened 3 crown-jewel checkpoints against vacuous/tautological-pass risk (the de-id tmp-tree-scan-with-mutation; the audit→self-test exit-code chain; the store-seam golden-line).
- **`/create-task-plan` recipe-review (QA+Architect+Security):** the CONTRACT gap ARCH-1 (`gate_dispatch` revise_domains keyed on rubric DIMENSIONS, not plan DOMAINS — unsatisfiable as written; FIXED inline with a section-domain-localization + all-run-set-fallback derivation rule) + 12 executability findings (laddered).

## State at close

- pytest **1611 passed / 2 skipped** (docs-only work; baseline unchanged). close-audit + harvest-gate green (S93).
- **The recipe stage is NOT pipeline-complete (PF-S93-01):** a monthly spend limit interrupted a SINGLE BATCHED remediation subagent (all-or-nothing — lost in-progress fixes). The recipe judge (Phase 6/7) + promotion to `docs/task-plan/<id>.md` + the 12 executability findings are carried to S94 (the findings in a committed ledger `docs/task-plan/.pipeline/live-wiring/review-findings.md`, a per-wave blocking dependency). The one build-breaking finding (ARCH-1) was fixed inline.
- **One new PF — PF-S93-01** (batched remediation is all-or-nothing → prefer per-task remediation; ladder un-completable stage findings into a committed ledger + bead). Beads: `s4i4` (PF), `stsq` (SEC-3 live-dispatch 0-leak release gate), `2gik` (S94 recipe-stage completion).

## Next (S94)

Clear the recipe stage (apply the ledger + judge + promote), then `/execute-plan` the 3 waves (Wave 1 {de-id backend ∥ keystone driver} → Wave 2 {gate composer} → Wave 3 {skill front-door ∥ audit repoint}), each SE-TDD → checkpoint → `/review-pr` → `/merge`; repoint `core-capability-audit.sh` onto the A′ spine (closes `71s4`/PF-S63-02); light the live de-id backend + the operator-present LIVE run.