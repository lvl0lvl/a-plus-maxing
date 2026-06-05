---
title: Integration Notes — design/ folder
type: reference
status: active
owner: walter
created: 2026-05-25
last_reviewed: 2026-05-25
review_cadence: per-checkpoint
permalink: a-plus-maxing/design/integration-notes
---

# `design/` — Integration Notes

This folder is the design-doc-protocol working area for the a-plus-maxing project's 7-role agent roster build (4 foundation + 3 pilot specialists). It is **isolated from the parallel session's work** (the parallel session works in `scripts/`, `INVARIANTS.md`, `CLAUDE.md`).

## Why this folder is isolated

A parallel session running in this repo at the same time is building mechanical-enforcement audit scripts (`scripts/handoff-audit.sh`, `scripts/scope-contract-audit.sh`, `scripts/pf-attestation-audit.sh`, `.claude/hooks/block-commit-main.sh`) per its own Session 5 scope contract. The two sessions share the repo but operate in non-overlapping file scopes:

| Session | Touches |
|---|---|
| This (S5 design) | `design/`, `HANDOFF.md`, `vault/sessions/session-5.md`, `memory/process-failures.md` (if PF), `.beads/*` |
| Parallel (S5 audit-scripts) | `scripts/`, `INVARIANTS.md`, `CLAUDE.md`, `.claude/hooks/`, `.claude/settings.json` |

Both contracts originally coexisted in `HANDOFF.md` under separate `## Scope Contract — Session 5` headers (the audit script accepts the highest-N contract; both are dated 2026-05-25); they were archived to `vault/sessions/scope-contract-archive.md` at S32 (2026-06-05) along with the rest of the Sessions 5-31 contracts.

## What this folder contains

```
design/
├── README.md                                       — pipeline overview + 5-phase per-role protocol
├── INTEGRATION_NOTES.md                            — this file
├── health-specialist-architect-design.md           — (NOT YET; Pass 2 deliverable; design-doc Phase 5 finalize)
├── health-implementer-design.md                    — (NOT YET; Pass 2 deliverable)
├── health-edge-case-reviewer-design.md             — (NOT YET; Pass 2 deliverable)
├── medical-safety-reviewer-design.md               — (NOT YET; Pass 2 deliverable)
├── labs-specialist-design.md                       — (NOT YET; Pass 3 deliverable)
├── peptide-specialist-design.md                    — (NOT YET; Pass 3 deliverable)
├── medical-liaison-design.md                       — (NOT YET; Pass 3 deliverable)
└── .{role}-design-work/
    ├── domain-research.md                          — Phase 0 deep-research output (1 per role, in progress)
    ├── architect-draft.md                          — Phase 1 parallel draft (NOT YET)
    ├── se-draft.md                                 — Phase 1 parallel draft (NOT YET)
    ├── qa-draft.md                                 — Phase 1 parallel draft (NOT YET)
    ├── red-team-adversarial.md                     — Phase 3 red-team (NOT YET)
    ├── red-team-safety.md                          — Phase 3 red-team (NOT YET)
    ├── oq-list-for-user.md                         — Phase 5 open questions (NOT YET)
    └── dispatch-ledger.jsonl                       — Phase 0 agent-dispatch ledger
```

## Current status (as of 2026-05-25 commit)

| Role | Phase 0 deep-research | Phase 1-5 design doc |
|---|---|---|
| health-specialist-architect | ✅ Complete (11,706 words, 49 sources) | ⏸ Pass 2 |
| health-implementer | ✅ Complete (13,876 words, 68 sources) | ⏸ Pass 2 |
| health-edge-case-reviewer | ⏸ Pending | ⏸ Pass 2 |
| medical-safety-reviewer | ⏸ Pending | ⏸ Pass 2 |
| labs-specialist | ⏸ Pending | ⏸ Pass 3 |
| peptide-specialist | ⏸ Pending | ⏸ Pass 3 |
| medical-liaison | ⏸ Pending | ⏸ Pass 3 |

## How to integrate this work into the parallel session's work

The two sessions produce complementary deliverables. The integration cycle when both reach completion:

1. **Parallel session deliverables:** audit scripts in `scripts/`, mechanical-enforcement hooks in `.claude/hooks/`, INVARIANTS.md mechanical-verification entries, CLAUDE.md close-protocol step 8.5 expansion.

2. **This session's deliverables:** domain-research.md per role (Phase 0); design-doc per role (Phases 1-5, future); per-role agent.md files (Session B via `/upgrade-agent`, future).

3. **The integration point:** the audit scripts from the parallel session enforce structural invariants on the agent.md files this session will eventually produce. Specifically:
   - `enforce-role-inlining.sh` PreToolUse hook (already in `.claude/hooks/`) validates that any agent dispatch with role-context inlines the full 11-section profile verbatim — applies to ALL specialist dispatches in production.
   - A future per-section audit script (the implementer-meta deliverable per `health-implementer/domain-research.md` Finding 6) will verify each section's mechanical-check stub against the section's prose.
   - The `IDENTICAL/DIFFER` partition (per `health-implementer/domain-research.md` Finding 7) requires a SHA-256 hash-match script across all 14 specialist profiles; this script is part of the audit deliverable.

4. **No file conflicts expected:** the two sessions' `Files I WILL touch` lists are mutually exclusive (see HANDOFF.md). Both target `HANDOFF.md` only for their own scope contract + close attestation, in non-overlapping sections.

## How to read the per-role domain-research.md

Each domain-research.md follows the deep-research SKILL.md Output Contract:
- **Executive Summary** (50-250 words) — what to take away if you only read one paragraph
- **Introduction** — research question + scope + methodology + assumptions
- **Main Analysis** — 6-12 numbered findings, each mapped to AGENT_TEMPLATE.md sections and a cross-report pattern
- **Synthesis & Insights** — patterns + second-order implications
- **Limitations & Caveats** — counter-evidence, gaps, uncertainties
- **Recommendations** — 14-15 encodable items, each mapped to a specific section of the 11-section AGENT_TEMPLATE.md OR a specific process step
- **Bibliography** — every [N] cited, with URLs and retrieval dates
- **Methodology Appendix** — phase-by-phase execution, dispatch ledger summary, deviation log, final attestation
- **Phase 7 Refinement Log** — fixes applied per Phase 6 critique

The deliverable is consumed downstream by:
- **Pass 2 Phase 1 drafting team** for the same role (architect / SE / QA drafts pull from this domain-research)
- **`/upgrade-agent` runs in Session B** for the same role (the design doc + this research feed the agent.md authoring)
- **Future foundation-role consumers** (e.g., `health-implementer` is the role-2 deliverable; its findings are inputs to Role 3 + 4 + later specialists when designing their profiles)

## Provenance and audit trail

Each domain-research.md's Methodology Appendix records:
- Sub-agent dispatch sequence
- Iteration counts at the JUDGE GATE (deep-mode 99/100 threshold)
- Phase 4 verifier output (unique source count, contradictions, validation checks)
- Phase 6 critique findings
- Phase 7 refinement responses to critique
- Any rubric-correction events (e.g., Role 2 had a mid-run rubric correction documented in its appendix)

Intermediate working artifacts (`/tmp/deep-research/` per-role rubric, retrieval outputs, judge JSONs, dispatch ledgers) are NOT committed to git — they're working state. The final deliverable carries enough provenance metadata in its Methodology Appendix that any external auditor can verify the chain from research question to final synthesis without needing the working artifacts.

For Roles 1+2, the `.{role}-design-work/dispatch-ledger.jsonl` files preserve the Phase 0 dispatch sequence on disk. Roles 3+4 will get the same when their Phase 0 completes.

## Downstream context-package construction (per user instruction)

When all 7 roles' design docs land, a context package will be assembled for use by:
1. The downstream Session B (`/upgrade-agent` runs to author the actual agent.md files for each role)
2. The medical-safety-reviewer role itself (which uses the design-doc body as its training corpus for runtime gating decisions)
3. Anyone integrating these agents into the larger Walter project ecosystem

The context-package should pull:
- `design/{role}-design.md` (the finalized design doc per role, Pass 2 output)
- `design/.{role}-design-work/domain-research.md` (the Phase 0 research substrate per role)
- `design/INTEGRATION_NOTES.md` (this file)
- A cross-role consistency report (to be produced after all 7 design docs are final)

This integration-readiness is the rationale for: (a) every recommendation in each domain-research.md being section-mapped (so it's encodable downstream), (b) the explicit `IDENTICAL/DIFFER` partition tables (so cross-role consistency can be mechanically verified), and (c) the Methodology Appendix carrying its own provenance trail (so the context-package can be audited end-to-end).

## Anti-patterns to guard against during continued work

Per the project's `memory/process-failures.md` PF entries — these are the failure modes that have actually occurred in this project and must not recur during the remaining Roles 3+4 work:

- **PF-S2-01 / PF-S3-01 (Orchestrator self-attests rigor):** All judging is dispatched-agent verdict; never orchestrator-composed. Every iter-N judge is a FRESH agent, not a re-run of the prior judge.
- **PF-S2-02 (Citation errors caught by accident):** The Phase 6 critique caught 5 fabrication-shaped URLs in Role 2's draft synthesis. This is the protocol working as intended. The pattern: my synthesis-level work is suspect until critique runs.
- **PF-S2-04 (Library research over-personalized):** The domain-research is goal-agnostic; specialist personalization happens at dispatch time in production, not in the design doc.
- **PF-S2-05 (Protocol from memory):** Re-read the deep-research SKILL.md + design-doc-protocol at each phase boundary. Operating from memory of the protocol is the canonical failure.

## What this folder is NOT

- Not the agent.md files themselves (those are Session B's deliverable via `/upgrade-agent`)
- Not the architect's runtime role profile (that gets authored by the implementer in Session B, using this folder's design docs as input)
- Not vault/-bound knowledge (this is project documentation, not the queryable wiki)
- Not in scope for the parallel session's modifications (per the Files I will NOT touch list in HANDOFF.md S5 contract)
