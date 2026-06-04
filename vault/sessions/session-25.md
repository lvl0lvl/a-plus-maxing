---
title: Session 25 — V1 ADR set via the create-adr 8-phase pipeline
type: session
permalink: a-plus-maxing/sessions/session-25
created: 2026-06-04
session: S25
---

# Session 25 (2026-06-03 → 2026-06-04)

## Goal (as contracted)

Run the ADR stage (`fm4`) of the product pipeline — author the V1 architecture decision records the Approved PRD defers, via `/create-adr` (read `adr-development` SKILL.md + `create-adr.md` in FULL first, PF-S17-01). Resolve the ADR-home convention (AC1); produce the foundational `hil` PII-path ADR (AC3); formally supersede `2026-05-16-system-architecture.md` (AC5).

## What happened

1. **Ran the `adr-development` 8-phase pipeline in full** (Discovery → Rubric → DAG → Author → Verify → Judge → Red Team → Final Fix). Read SKILL.md + create-adr.md before invoking (PF-S17-01). **create-adr Hard Rule 1 held: the orchestrator coordinated; worker agents produced every ADR, verification, and judge verdict — the orchestrator never authored an ADR.** User-gated at Phases 1/2/3 (Discovery list, Rubric, DAG).

2. **Discovery → 7 decisions** (D8 clone-init folded into D6 at the Phase-1 gate; D7 kept as one parent). 11 items correctly excluded as resolved / already-recorded / implementation-detail (projection math, template tokens, the gated-wiki substrate, cron mechanism, the HIPAA ceiling, the ADR-home convention itself).

3. **DAG → 16 edges, 5 tiers, 1 tension.** Tier 1 D1 (sole foundation) → Tier 2 D2 → Tier 3 {D3,D4,D6} → Tier 4 D5 → Tier 5 D7. One real tension: **D4 (single-file <500KB budget) ↔ D7 (asset-heavy matrix/projection render)** → a build-plan render-size measurement task + an OQ on both sides.

4. **Authored, verified, judged-ACCEPTED all 7 ADRs** (3×90/90, 4×89/90 under the revised threshold). Zero fabricated citations across the set (the Anthropic no-train terms verified live; the retention window honestly tagged [UNVERIFIED]).

5. **Rubric governance refined mid-pipeline (Walter-directed)** when ADR-0001 exposed two mis-calibrations: (a) the 99% threshold on 9 dimensions forced all-10s and false-failed a depth-justified single-9 → relaxed to **≥95%/no-dim-<9**; (b) the word-count ceiling was a blocking Dim-2 penalty that would force cutting load-bearing content → converted to a **review-trigger + individual length exception** (Length-Exception Protocol; never preference a count over load-bearing quality). All 7 ADRs over-ceiling, all granted logged exceptions after a load-bearing review.

6. **Whole-set Red Team: 0 BLOCKING, 3 IMPORTANT, 4 ADVISORY.** Caught two cross-ADR defects the per-ADR judges structurally could not see: the `2026-05-16` supersession cross-links were told three inconsistent ways (and ADR-0004's required edge was missing), and FR-12 (physician-feedback capture) was referenced but never placed. Phase-8 fixes applied + final-verified PASS (16-edge DAG unchanged).

7. **Governance flips (AC1 + AC5):** `2026-05-16-system-architecture.md` formally superseded by ADR-0002/0004/0006 (its markdown-substrate + July-visit-goal calls carried forward, not reversed); ADR-home convention recorded (product-pipeline → `docs/`; vault-native → `vault/decisions/`) in the CLAUDE.md ownership matrix; the contradictions.md ADR-home entry closed.

## The V1 ADR set (durable handoff — the `.pipeline/` working artifacts are gitignored)

| ADR | Decision | Tier | Judge |
|-----|----------|------|-------|
| ADR-0001 | No-train PII trust boundary (threat-model B; the `hil` decision) — local store/ingestion/generation, plan reasoning only over summaries on a no-train non-retained path | 1 | 90/90 |
| ADR-0002 | Local-first time-series store = **append-only NDJSON, one file per item, gitignored `vault/store/`** (over SQLite) | 2 | 89/90 |
| ADR-0003 | Source-extensible ingestion = **pluggable per-source adapter** over a common export pattern; idempotent; schedulable; manual fallback | 3 | 90/90 |
| ADR-0004 | **On-demand (+cron) single self-contained HTML file**, no server, <500KB, renders through the artifact-protocol template library | 3 | 89/90 |
| ADR-0005 | Operator-agnostic clonable distribution: **PII-free trunk + gitignored local data**, scaffold/value split, content-scan guarantee (absorbs clone-init) | 3 | 89/90 |
| ADR-0006 | Multi-domain plan assembly: **route each goal-domain → roster specialist → compose → attribute → coverage-gap-disclose**; reasoning on the no-train path | 4 | 89/90 |
| ADR-0007 | Lab-loop + watch-out = **store schemas**; biomarker-matrix + projections = **render-time views**; ≥3-timepoint projection guardrail; FR-12 capture placed as a store schema | 5 | 90/90 |

**Handoff to the spec stage (`rg2`):** each ADR's Validation criteria → acceptance criteria; Open Questions → spec spikes (esp. ADR-0001 OQ-1 the PII enforcement mechanism + the D4↔D7 render-size measurement); DAG tiers → build phases (ADR-0001 first).

## Discipline notes

- **Read-before-invoke HELD** (PF-S17-01): full adr-development read before invoking; flagged the spec/build-plan/task-plan stages get the same treatment.
- **Hard-Rule-1 HELD**: every ADR / verification / judge verdict was a dispatched worker; the orchestrator resisted the "I've read the skill, I'll write it myself" temptation at all 5 tiers.
- **The whole-set Red Team earned its place** — it caught the supersession-inconsistency + the unplaced FR-12 that 7 passing per-ADR judges missed. A reminder that systemic review ≠ the sum of per-item reviews.
- **Rubric mis-calibration is not a process failure** — the verify+judge gates surfaced it, and it was corrected by a user-approved governance change, the multi-gate pipeline working as designed.

## State at close

- 7 ADRs in `docs/adr/` + governance flips. PR #29 `/review-pr`'d (Gate PASS; 2 suggestion fixes) and rebase-merged to `main`; a follow-up `fix/s25-handoff-postmerge` PR reconciled the HANDOFF to the merged state (PF-S25-01). No code built — design only.
- Pipeline: PRD (S24) → **ADR (S25, done)** → next = spec (`rg2`).
- `fm4` + `hil` closed; `75t` filed (P3, wiki-schema `depends_on` freshness, from the #29 review). The PII boundary is DECIDED (ADR-0001) but UNBUILT — the spec stage must place its enforcement mechanism before the personalization path reaches implementation.

See [[design/vision]], `docs/adr/ADR-0001…0007`, `docs/adr/.pipeline/` (gitignored working artifacts), HANDOFF S25 (contract + evaluation + What Is Next).
