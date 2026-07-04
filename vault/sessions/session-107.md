---
title: Session 107
type: session
created: 2026-07-04
status: complete
permalink: a-plus-maxing/sessions/session-107
---

# Session 107 (2026-07-04)

## Goal

Execute **B1** (bead `31fp`) — author **ADR-0039**, the scheduled-agent-runner that gives the plan-evolution loop's cadence trigger a live dispatch runtime — via `/create-adr` run in full, then land it (`/review-pr` → merge) and close. Operator-directed, autonomous: "open the session and proceed with B1" → "proceed through the pipeline autonomously to the final ADR" → "don't forget the review-pr cycle."

## The decision (ADR-0039, accepted, PR #289 → main `e8abe995`)

A **local scheduled headless Claude-Code runner** (launchd primary, cron fallback; **disabled by default**) hosts the loop's cadence trigger: on the cadence it launches a local headless Claude-Code *subscription* session that reads the local store, supplies the ADR-0027 `deid_client` (the sole metered egress), dispatches the specialists/judge/lenses as subscription sub-agents, and calls the built `plan_loop.signal(trigger=CADENCE_TRIGGER, ...)` — supplying the seams, re-hosting nothing (extend-not-rebuild).

**Local-first PII is decisive:** the loop re-reads the operator's local gitignored store, so a runtime that can't see it either can't run or must export raw PII to a cloud runtime (a new egress class). That rejects the **cloud routine** (a North-Star hosted-product candidate) and **B2 API-backed in-server dispatch** (arms metered spend by default + contradicts ADR-0026's subscription-dispatch design). **Activation is operator-gated** — installing the schedule arms recurring de-id spend; disabled by default, and no build/provision/`init_instance` step may load it.

## Pipeline (`/create-adr` run in full)

author → independent **verify** (8/8 categories pass; every code citation resolves; the Claude Code runtime claims — Agent SDK, `setup-token` OAuth, the `ANTHROPIC_API_KEY`-precedence spend footgun — independently confirmed TRUE) → **judge ACCEPT** (≥9/dim; Citation-Traceability 9 for one inaccurate sentence, all other 8 dims 10) → **whole-set red-team** (8 findings, 2 blocking: the ADR-0026 "truly-headless-is-not-V1" refinement-honesty reframe + a DAG 2-cycle) → **remediation** (all 9 findings + 6-ADR backfill) → **final-verify CLEAN**.

## The `/review-pr` cycle (local 3-lens, GraphQL rate-limited)

Contracts/DAG (sound, 0 findings) + content-quality (HIGH; 2 LOW polish) + cross-ADR-intent — which caught a legitimate **MEDIUM the create-adr red-team missed**: the runner is *itself* a subscription session that reads the store, so raw PII could transit the subscription/consumer lane (not the no-train lane) if the top-level session reads the store into its own context. Hardened to a **binding constraint** pre-merge (the raw `store.read_all` + `deid_in` must run in the Python driver layer, out of the top-level session's transmitted context) + folded into OQ-1. The layered review working as designed — each layer caught what the prior missed. The self-abbreviated-gated-review guard (S106's PF) HELD: the full 3-lens review ran (not abbreviated), every finding fixed or beaded.

## Cross-ADR

- **Refines ADR-0026 Negative-1** (truly-headless is viable in V1 via the non-interactive `setup-token`) — framed honestly as a partial-reversal, not clean consistency.
- **Partially resolves ADR-0036 OQ-2** (the cadence host; data-event/free-text triggers stay open — ADR-0039 OQ-5).
- Append-only reciprocal edges backfilled into ADR-0036/0026/0027/0016/0001/0005.

## Next

- The **BUILD** of the runner: `/create-spec` → `/create-build-plan` → `/create-task-plan` → `/execute-plan` for ADR-0039, resolving its 8 OQs at spec-stage (concrete headless shape + top-level-session PII containment, auth isolation + token-at-rest, missed-window, enable/disable surface, the other two triggers, acceptable-use, store-concurrency, crash semantics). Then the `/plan-loop` front-end consumer + P3 disambiguation.
- Beaded: `tmfm` (ADR-0020..0027 `status: proposed` reconciliation, surfaced by the review); carried `yvrs`/`z2mh`/`55qg`/`qiob`/`jlbh`.
- Operator-gated: the LIVE plan-generation run + the runner's LIVE activation (both real spend).

## References

- PR #289 (merged `e8abe995`); bead `31fp` (closed).
- `docs/adr/ADR-0039-scheduled-agent-runner.md`; ADR-0036 (loop).
- `memory/process-failures.md` `## Session 107` (skill-trace table + PF attestation + disclosure ledger).