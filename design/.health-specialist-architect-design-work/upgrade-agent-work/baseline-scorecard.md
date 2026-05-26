---
title: Phase 1 Baseline Scorecard — health-specialist-architect
type: upgrade-agent-artifact
phase: 1
created: 2026-05-26
target_path: ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md
source_design_doc: design/health-specialist-architect-design.md (873 lines, Status: Final)
---

# Phase 1 — Baseline Evaluation

## Net-new authoring context

The target path `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` **does not exist** at session start. Confirmed via `ls -la ~/Documents/Projects/skills_library/roles/health-specialist-architect/`: directory not present.

Existing role profiles at `~/Documents/Projects/skills_library/roles/`: architect, design-critic, game-designer, orchestrator, qa, security, senior-engineer, ui-designer. No `health-specialist-architect/` directory.

This is **net-new authoring**, not a delta upgrade. Phase 1 step 1 of `/upgrade-agent` (`Read the current agent profile`) is satisfied by recording the absent-file state.

## Baseline measurements

| Measurement | Current | Target |
|---|---|---|
| Line count (agent.md) | 0 (file absent) | ~140 target, ≤200 hard max |
| Token count (agent.md) | 0 (file absent) | ≤2,000 |
| library-index.md | absent | optional — only if references warrant |
| Catalog row | absent | one row in `roles/orchestrator/catalog.md` |

## Reference materials read for baseline

- `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` — 97 lines, structural target (10 base sections + Modes for mature profiles)
- `~/Documents/Projects/skills_library/roles/orchestrator/catalog.md` — 89 lines, target catalog row format
- `design/health-specialist-architect-design.md` — 873 lines, Status: Final (source of truth for agent.md content)

## Per-dimension baseline (10 dimensions × 0-10)

Every dimension scores `0/10` because no file exists. Score evidence below names what would be measured against once a draft exists. All 10 dimensions are **research targets** for Phase 3.

| # | Dimension | Score | Evidence (gap) |
|---|---|---|---|
| 1 | Identity Clarity | 0/10 | No Identity section exists. Anti-sycophancy anchor must land in first 20 lines per command HARD RULE; design doc §2.1 has the canonical Identity sentence ready. |
| 2 | Context Efficiency | 0/10 | No token usage yet. 873-line design doc must compress to ~140 lines. Compression ratio ~6.2x. Per-section budgets per command's table. |
| 3 | Behavioral Specificity | 0/10 | No Core Rules. Design doc §5 has 14 rules (13 + 6b); deployed agent.md target 8-12 rules per AGENT_TEMPLATE.md guidance. Each rule must have testable pass/fail. |
| 4 | Reference Integration | 0/10 | No library-index.md. Design doc §10 enumerates 4 mandatory auto-load files + conditional reads. Mapping to be designed in Phase 3 R2. |
| 5 | Boundary Enforcement | 0/10 | No Role Boundaries section. Design doc §2.2 has 8 owns / 8 not-owned with owning roles in parentheses. |
| 6 | Communication Protocol | 0/10 | No Communication section. Design doc §9 has 3 audiences (orchestrator structured-list / downstream sentence-pattern / user plain-language). |
| 7 | Failure Recovery | 0/10 | No Loop-Breaking. Design doc §7 has 5 thresholds (spec-revision cap=2, design-review cap=3, scratch threshold, LIVE-tag cap, fabrication zero-tolerance). |
| 8 | Tool Awareness | 0/10 | No Tools section. Design doc §8 has permitted/skills/forbidden tri-partite split with explicit boundaries. |
| 9 | Anti-Pattern Coverage | 0/10 | No Anti-Patterns. Design doc §11.2 has 8 anti-patterns each with source + recognition cue. |
| 10 | Freshness | 0/10 | Versionless reference target. Design doc cites FD&C Act §520(o)(1)(E), FDA 2026 CDS, IMDRF SaMD N12, GRADE, OCEBM 2011 — fresh as of design-doc finalize 2026-05-26. |

## Research targets identified

All 10 dimensions are below 7/10 (they are at 0/10 — file absent). All 10 are research targets. Default grouping per `/upgrade-agent` Phase 3 spec applies:

- **R1 Behavioral Traits** → dimensions 1, 3, 5, 7, 9 (Identity, Core Rules, Boundaries, Loop-Breaking, Anti-Patterns)
- **R2 Tools & Configuration** → dimensions 4, 8 (Tools, Context Loading, library-index.md, catalog row)
- **R3 Communication & Anti-Patterns** → dimensions 6, 9 (Communication, Anti-Patterns, Negative Examples, anti-sycophancy placement)

Dimensions 2 (Context Efficiency) and 10 (Freshness) are cross-cutting; all three researchers respect line budgets and version-fresh references.

## Net-new framing

The standard `/upgrade-agent` flow assumes an existing profile to upgrade. For net-new authoring:

1. Phase 2 Rubric Construction: derive from design-doc §15.2 7 binary ACs + 10 generic dimensions (no per-dimension delta from "current state" because current state is absent).
2. Phase 3 Research: each researcher grounds against the design doc as source of truth; produces implementation-ready content (the agent.md text), not recommendations.
3. Phase 4 Validation: SEPARATE fact-checker + judge per researcher's output. Pass threshold 9/10 every dimension. **Operational completeness** check has special weight in net-new context (every verb in the agent.md must have a tool/workflow because there's no prior text to inherit from).
4. Phase 5 Synthesis: agent.md authored at target path; 10 AGENT_TEMPLATE.md sections + Modes; 200-line hard max.
5. Phase 6 Adversarial Review against the synthesized agent.md.
6. Phase 7 Mechanical Verification.

## Phase 1 self-attest

- [x] Target path checked — does not exist (net-new authoring confirmed)
- [x] AGENT_TEMPLATE.md read — structural target captured (10 base + Modes)
- [x] catalog.md read — target row format captured
- [x] Design doc read in full — source of truth confirmed at Status: Final
- [x] Baseline scores recorded — 0/10 across all 10 dimensions (no profile exists)
- [x] Line/token budgets stated — ≤200 lines / ≤2,000 tokens hard max; ~140 / ~1,900 targets
- [x] Research targets identified — all 10 dimensions; default 3-researcher grouping applies
