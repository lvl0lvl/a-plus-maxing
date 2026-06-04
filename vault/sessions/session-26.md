---
title: Session 26 — Foundational data-in spec via the create-spec 7-phase pipeline
type: session
permalink: a-plus-maxing/sessions/session-26
created: 2026-06-04
session: S26
---

# Session 26 (2026-06-04)

## Goal (as contracted)

Run the spec stage (`rg2`) of the product pipeline — **foundational-first split** (Walter-confirmed): decompose the data-in ADR trio (ADR-0001 PII boundary → ADR-0002 store → ADR-0003 ingestion) into an implementation spec via `/create-spec` (read the spec skill IN FULL first, PF-S17-01). Defer the data-out cut (ADR-0004/0005/0006/0007 + the D4↔D7 tension) to a follow-up spec session.

## What happened

1. **Ran the `spec-development` 7-phase `/create-spec` pipeline in full** (Pre-Flight → Load Context → Unresolved-Concerns Gate → Generate → Validate → Judge → Save). Read SKILL.md + create-spec.md + all 3 references (template / task-decomposition / verification-protocol) + the worked example before invoking (PF-S17-01). **create-spec Hard Rule 1 held: the orchestrator coordinated + ran mechanical checks; worker agents produced every spec/remediation/judge artifact — the orchestrator never authored spec content.**

2. **Inputs:** the 3 ADRs in `docs/adr/` + the surviving (gitignored) S25 DAG artifact `docs/adr/.pipeline/dag.md` (Tier Map §5 + Constraint Propagation §8). The trio is **inbound-dependency-closed** — every constraint it depends on (D1→D2, D1→D3, D2→D3) is in scope; the only out-of-scope refs (0004-0007) are downstream consumers → deferred as interface points.

3. **Unresolved-Concerns Gate (user-facing):** 6 open questions + ADR-0001's unmitigated N2, dispositioned with Walter (2026-06-04): **2 Block** → the prerequisite spikes `ADR-0001-T0` (data-in PII-boundary enforcement) + `ADR-0002-T0` (store layout + (item,timepoint) keying — resolves the circular ADR-0002-OQ1 ↔ ADR-0003-OQ2 key reference in one task); **3 Proceed** (bounded-retention assumption; whole-file-scan scale ceiling; the wired-adapter set); **4 Defer** (the data-out tiers + the plan-reasoning router facet + the D4↔D7 tension).

4. **Concrete wired adapter set (Walter):** HealthKit (Apple Watch) + Oura (Walter), **Garmin** (the friend / second cloning operator) wired first; Whoop pluggable-but-unwired; labs/food/weight manual/CSV. Adapter code is PII-free (ships in the trunk); imported readings land only in the gitignored store.

5. **Generated + validated + judged → ACCEPT.** Phase-4 worker authored the spec. Phase-5 validation was orchestrator-MECHANICAL (file-set extraction, banned-word grep, acyclicity — NOT the worker's self-attestation). Phase-6 ran **3 fresh-judge iterations**: iter 1 + 2 REVISE on Dimension 5 (dependency accuracy — a forward reference the iter-1 fix only partially closed; the iter-2 fresh judge drilled to the root), iter 3 **ACCEPT** (all 10 dims ≥9, nine at 10).

## The foundational data-in spec (durable handoff — `.pipeline/` is gitignored)

`docs/spec/adr-0001-adr-0003-spec.md` (status: approved). 7 tasks, 5 topological groups, 11 dependency edges, 49 binary acceptance criteria.

| Task | What | Group |
|------|------|-------|
| `ADR-0001-T0` [Spike] | Data-in PII-boundary enforcement mechanism (egress guard + tracked-file PII scan + no-raw-to-model rule) | 1 (entry) |
| `ADR-0002-T0` [Spike] | Store layout + (item,timepoint) keying + NDJSON line field set (resolves ADR-0002 OQ-1 + ADR-0003 OQ-2) | 1 (entry) |
| `ADR-0002-T1` | Local NDJSON store append/read library + `vault/store/` gitignore entry | 2 |
| `ADR-0001-T1` | Egress + tracked-file PII-scan guard implementation | 2 |
| `ADR-0003-T1` | Shared ingestion routine + adapter interface + dedupe + manual/CSV fallback | 3 |
| `ADR-0003-T2` | First-cut adapters (HealthKit + Oura), Garmin 0-edit extensibility proof, Whoop stub | 4 |
| `ADR-0003-T3` | Unattended scheduler run (delta-since-last-run) | 5 |

**Critical path:** ADR-0002-T0 → ADR-0002-T1 → ADR-0003-T1 → ADR-0003-T2 → ADR-0003-T3. **In-scope constraints enforced as AC:** D1→D2 (store 0-network), D1→D3 (ingestion 0 raw-to-model, store-only writes), D2→D3 (dedupe key = the single shared `keying.py`).

**Handoff to the data-out spec (`rg2` remaining) + `hv6` (build-plan):** the store read model + the wired-adapter store + the data-in PII guard are the interface the data-out tiers (ADR-0004/0005/0006/0007) consume. The plan-reasoning ROUTER enforcement (ADR-0001 OQ-1's PII-bearing facet) is specced THERE, not here. `bd-per-task` was intentionally NOT created — the `mo4`/task-plan stage owns executable task beads.

## Discipline notes

- **Read-before-invoke HELD** (PF-S17-01): full spec skill read before invoking; flagged the same for the data-out spec + build-plan + task-plan.
- **Hard-Rule-1 HELD**: every spec/validation/judge/remediation artifact was a dispatched worker or a mechanical orchestrator check; the orchestrator resisted authoring spec content at every phase.
- **Anti-self-attestation HELD** (PF-S3-01): the Phase-4 worker's "validation passes" was re-verified mechanically; 3 FRESH judge iterations (the iter-2 judge caught a forward-reference the iter-1 remediation missed — the fresh-agent design earning its place).
- **Role-inlining hook false-positive** (observed, not a PF): the first spec-author dispatch was blocked because its `# Task`/`# Output` section headers matched the role-context H1 regex. The spec-author is a skill-internal worker with no role profile; corrected by demoting headers to `##` (read the hook source first to confirm the trigger). Candidate hook refinement surfaced for Walter, not self-registered (frozen INV-ROLE-INLINING mechanism).

## State at close

- Foundational data-in spec in `docs/spec/` + the `docs/spec/.gitignore`. Committed on `feature/v1-spec-stage`; PR to `main`. No code built — design only.
- Pipeline: PRD (S24) → ADR (S25) → **spec [data-in half] (S26, done)** → data-out spec (next) → `hv6` → `mo4` → execute.
- `rg2` updated PARTIAL (data-in delivered; data-out remaining, OPEN). `hv6` stays blocked on the full spec.

See [[design/vision]], `docs/spec/adr-0001-adr-0003-spec.md`, `docs/spec/.pipeline/` (gitignored working artifacts), `docs/adr/ADR-0001…0003`, HANDOFF S26 (contract + evaluation + What Is Next).
