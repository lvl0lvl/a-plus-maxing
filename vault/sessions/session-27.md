---
title: Session 27 — Data-out spec via the create-spec 7-phase pipeline; rg2 closed
type: session
permalink: a-plus-maxing/sessions/session-27
created: 2026-06-04
session: S27
---

# Session 27 (2026-06-04)

## Goal (as contracted)

Run the remaining half of the spec stage (`rg2`) — the **full data-out cut** (Walter-confirmed: one unified spec, not a further split): ADR-0004 (generation) / 0005 (PII-free trunk) / 0006 (plan-assembly + plan-reasoning ROUTER enforcement) / 0007 (lab-flow), carrying the D4↔D7 render-size tension as a measurement spike, via `/create-spec` (read the skill IN FULL first, PF-S17-01). Closes `rg2`; unblocks `hv6`.

## What happened

1. **Ran the `spec-development` 7-phase `/create-spec` pipeline in full** (Pre-Flight → Load Context → Unresolved-Concerns Gate → Generate → Validate → Judge → Save). Read SKILL.md + create-spec.md + all 3 references (template / task-decomposition / verification-protocol) + the worked example before invoking (PF-S17-01, per-invocation). **Hard Rule 1 held: the orchestrator coordinated + ran mechanical checks; worker agents produced every spec/remediation artifact.**

2. **Inputs:** the 4 data-out ADRs in `docs/adr/` + the S25 DAG artifact `docs/adr/.pipeline/dag.md` (§5 tier map, §7 D4↔D7 tension, §8 constraint table). The data-in spec `docs/spec/adr-0001-adr-0003-spec.md` is the upstream cross-spec interface — consumed (`ADR-0001-T0`/`T1`, `ADR-0002-T1`, `ADR-0003-T1`), not re-specced.

3. **Unresolved-Concerns Gate (user-facing, prose):** 6 items dispositioned with Walter ("accept all"): **2 Block** → the prerequisite spikes `ADR-0004-T0` (D4↔D7 render-size measurement) + `ADR-0006-T0` (plan-reasoning summary contract + no-train router enforcement, enforcement-first); **4 Proceed** (content-scan = gitignore+hook; no-specialist → coverage-gap-by-absence; clone-init default; watch-out question derivation).

4. **Generated + validated + judged → ACCEPT.** Phase-4 worker authored the spec (transient socket error AFTER the complete write — verified 423 lines, all sections, before proceeding). Phase-5 validation was orchestrator-MECHANICAL (23≡23 manifest, acyclic 11/11, 12 map edges ≡ 12 declared deps, 0 banned words, all 4 constraint criteria) — NOT worker self-attestation. Phase-6 fresh judge **ACCEPT 99/100** (all 10 dims ≥9, Dim-3 at 9). Two real judge-flagged findings (manifest miscount; colorblind sub-check mechanism) FIXED by a remediation worker + re-validated (PF-S26-01: real → fixed, not suppressed).

5. **Reviewed (`/review-pr` #35) + merged.** 3 docs-PR agents (Code-Quality / Contracts-Architect / Historical-Context, full profiles inlined, local-git-only). 4 findings → blind triage → **2 LEGITIMATE FIXED + blind-verified** (API-001: the FR-2 personalization + HALT-rule safety obligation had no binary criterion → added `ADR-0006-T2` c8/c9; QUAL-002: `pii_scan.py` cross-spec reuse unnamed → named + relationship stated), **2 NOT_A_BUG** (QUAL-001 mitigated; QUAL-003 by-design). 0 suppressed — matrix priority-only. Rebase-merged via REST (GraphQL throttled).

## The data-out spec (durable handoff — `.pipeline/` is gitignored)

`docs/spec/adr-0004-adr-0007-spec.md` (status: approved). 11 tasks, 5 topological groups, 12 dependency edges.

| Task | What | Group |
|------|------|-------|
| `ADR-0004-T0` [Spike] | D4↔D7 render-size measurement + cap parameter | 1 (entry) |
| `ADR-0006-T0` [Spike] | Plan-reasoning summary contract + no-train router enforcement (PII guard) | 1 (entry) |
| `ADR-0004-T1` | Generation engine + template component library (dashboard + report) | 1 (entry) |
| `ADR-0005-T1` | PII-free-trunk gitignore boundary + pre-commit content-scan hook | 1 (entry) |
| `ADR-0004-T2` | Single-file matrix/projection artifacts under the spike cap | 2 |
| `ADR-0004-T3` | On-demand + unattended (cron) generation entry point | 2 |
| `ADR-0005-T2` | Clone-init step + operator-facing README | 2 |
| `ADR-0006-T1` | No-train router + summary derivation implementation | 2 |
| `ADR-0006-T2` | Multi-domain plan assembly (routing/composition/attribution/sourcing/coverage-gaps/personalization/HALT) | 3 |
| `ADR-0007-T1` | Lab-loop / watch-out / physician-feedback store schemas | 4 |
| `ADR-0007-T2` | Biomarker-matrix + projection render-time views | 5 |

**Critical path:** ADR-0006-T0 → ADR-0006-T1 → ADR-0006-T2 → ADR-0007-T1 → ADR-0007-T2. **Constraints enforced as AC (DAG §8):** D1→ADR-0004 (0 PII egress at render), D1→ADR-0007 (0 labs/answers to model), D1→ADR-0006 (no-train summaries, 0 raw-PII sends), D2→ADR-0005 (store-exclusion content scan).

**Handoff to `hv6` (build-plan):** the full spec is now both halves on the trunk (7 data-in + 11 data-out = 18 tasks). The four prerequisite spikes (`ADR-0001-T0`, `ADR-0002-T0`, `ADR-0004-T0`, `ADR-0006-T0`) are the earliest waves; `ADR-0006-T0` stays enforcement-first ahead of any plan-reasoning-over-PII task. `bd-per-task` intentionally NOT created — the `mo4`/task-plan stage owns executable task beads.

## Discipline notes

- **Read-before-invoke HELD** (PF-S17-01): the spec skill, the `/review-pr` skill (+ scoring-rubric + review-methodology + the 3 role profiles), and the `/merge` methodology all read in full before invoking.
- **Hard-Rule-1 HELD**: every spec/validation/judge/remediation/review artifact was a dispatched worker or a mechanical orchestrator check; the orchestrator never authored spec content.
- **Anti-self-attestation HELD** (PF-S3-01): mechanical Phase-5 re-extraction + a FRESH judge + a blind triage + a blind verification (independent agents).
- **PF-S25-01 window TRIPPED-CLEAN**: the close was sequenced AFTER the merge on a separate branch → no stale forward-looking HANDOFF lines.
- **PF-S26-01 window TRIPPED-CLEAN**: low-impact-but-real findings routed through triage; legitimate fixed, not-real got no action; 0 suppressed by severity.

## State at close

- Data-out spec in `docs/spec/` (status approved). Reviewed (`/review-pr` #35 Gate PASS) and rebase-merged to `main`. No code built — design only.
- Pipeline: PRD (S24) → ADR (S25) → **spec [data-in S26 + data-out S27] ✓** → `hv6` (build-plan, UNBLOCKED) → `mo4` (task-plan) → execute.
- `rg2` CLOSED (both halves delivered); `hv6` UNBLOCKED.

See [[design/vision]], `docs/spec/adr-0004-adr-0007-spec.md`, `docs/spec/.pipeline/` (gitignored), `docs/adr/ADR-0004…0007`, HANDOFF S27 (contract + evaluation + What Is Next).
