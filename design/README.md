---
title: Design Directory
type: reference
status: active
owner: walter
created: 2026-05-25
last_reviewed: 2026-05-25
review_cadence: session
permalink: a-plus-maxing/design/readme
---

# `design/` — agent profile design docs

Working space for the agent-roster build. Each role gets a finalized design doc at the top level plus a working sub-directory holding parallel-agent drafts, red-team reports, and orchestrator notes.

Pattern adapted from `Quant/design/` and the `design-doc-protocol` memory note (Session A of the 3-session A/B/C cycle: A = design doc, B = `/upgrade-agent` build, C = first real run validates).

## Pipeline (Session 5 scope)

Sequential across roles, parallel within each role. Built in two passes:

### Pass 1 — Foundation drafting team

These 4 roles replace the software-flavored `architect / senior-engineer / qa / security` agents from `~/Documents/Projects/skills_library/roles/` when the design subject is a medical-domain specialist. Until they exist, Pass 1 uses the software-flavored roles as a documented v1 substitute.

1. `health-specialist-architect` — structural designer for medical specialist agent profiles
2. `health-implementer` — writes agent.md prose for medical specialist profiles
3. `health-edge-case-reviewer` — finds untested boundaries in medical specialist profiles
4. `medical-safety-reviewer` — red-team #2 for medical specialist designs (replaces software `security` agent)

**Checkpoint after Pass 1.** User authorization required before Pass 2 begins. Foundation roles get deployed via `/upgrade-agent` in Session B, not in this session.

### Pass 2 — Pilot specialists (use new foundation team)

5. `labs-specialist` — bloodwork interpretation, biomarker context
6. `peptide-specialist` — peptides, GH secretagogues, healing peptides
7. `medical-liaison` — MD-handout queue, contraindication tracking, Rx coordination

After the pilot completes, the user decides whether to extend with the remaining 11 roles from `vault/WIKI.md` Agent Consumers table, and whether to tier the design (one master roster doc + per-agent specs) or keep per-agent design docs.

## Per-role file layout

```
design/
├── README.md                                  ← this file
├── {role}-design.md                           ← finalized doc, frontmatter Status: Final
└── .{role}-design-work/                       ← working dir; per-role subspace
    ├── domain-research.md                     ← Phase 0 /deep-research output
    ├── architect-draft.md                     ← Phase 1 parallel draft
    ├── se-draft.md                            ← Phase 1 parallel draft
    ├── qa-draft.md                            ← Phase 1 parallel draft
    ├── red-team-adversarial.md                ← Phase 3 parallel red-team
    ├── red-team-safety.md                     ← Phase 3 parallel red-team
    └── oq-list-for-user.md                    ← Phase 5 open questions, if any
```

## 5-phase pipeline (per role)

Per `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-Quant/memory/design-doc-protocol.md`, adapted with one health-specific addition (Phase 0).

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 0 | Domain research | `/deep-research --mode=deep` | `domain-research.md` |
| 1 | Drafting team (parallel) | architect + senior-engineer + qa, each with FULL 11-section role profile inlined per INV-ROLE-INLINING | 3 draft files |
| 2 | Synthesis | orchestrator | `{role}-design.md` (20-section structure, omissions noted) |
| 3 | Red team (parallel) | `/adversarial-review` + safety reviewer | 2 finding lists |
| 4 | Verify findings | orchestrator (personally; not delegated; not auto-accept; not auto-reject; burden of proof on rejection) | Appendix A with verdicts |
| 5 | Finalize | orchestrator | frontmatter `Status: Final` + commit |

## Anti-patterns guarded against

Per `memory/process-failures.md`:

- **PF-S2-01 / PF-S3-01 — Orchestrator self-attests rigor.** All judging and red-teaming runs as separate dispatched agents. The orchestrator never composes a red-team verdict, judgment, or finding-list from prose summaries.
- **PF-S2-02 — Citation errors caught by accident.** Phase 4 verifies each red-team finding against the cited source. Not delegated.
- **PF-S2-03 — Over-questioning.** Open questions only when genuinely ambiguous and hard-to-reverse. Logged in `oq-list-for-user.md` for the user; not surfaced inline during the pipeline.
- **PF-S2-04 — Library research over-personalized.** Domain research (Phase 0) is "what does a competent {role} need to know / do / boundary against," role-agnostic to the operator. Specialist-time operator personalization happens at dispatch time in production, not in the design doc.
- **PF-S2-05 — Protocol from memory.** Re-read this README and `design-doc-protocol.md` at each phase boundary. Operating from memory is the canonical failure.
- **PF-S2-06 — Branch hygiene.** All commits on `feature/wiki-bpc157-aplus-research`.

## Invariants tied to this work

- `INV-ROLE-INLINING` — every dispatched agent prompt pastes the full 11-section profile verbatim from `~/Documents/Projects/skills_library/roles/{role}/agent.md`. Enforced at dispatch time by `.claude/hooks/enforce-role-inlining.sh`.
- `INV-SCOPE-CONTRACT` — each role's design pipeline operates under the parent session's scope contract; no per-role mini-contracts.
- `INV-PF-ATTESTATION` — at session close, either a new PF entry or explicit "no new PF" with rationale.

## v1 substitutes (documented honestly)

Pass 1 uses software-flavored drafters (architect / senior-engineer / qa / security). The reasoning is identical to `aplus-research` v1's brief-hash-uniqueness-as-substitute-for-UUIDv4 acknowledgment: the right tool doesn't exist yet, so use the closest available tool and document the substitute explicitly.

After Pass 1, the project owns medical-domain foundation roles. From that point forward, no further design doc work should use software-flavored drafters for medical-specialist subjects.
