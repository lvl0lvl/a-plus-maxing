# health-implementer /upgrade-agent — Phase 1 Baseline + Phase 2 Rubric

Run: S13 (2026-05-28). Source of truth: `design/health-implementer-design.md` (Status: Final, 780 lines). Target: `.claude/agents/health-implementer/agent.md` (project-local per ADR `vault/decisions/2026-05-26-foundation-role-agent-md-location.md`). Reference shape: `.claude/agents/health-specialist-architect/agent.md` (Role 1, 127 lines / ~3,252 cl100k tokens, 11 sections + Modes).

## Phase 1 — Baseline Evaluation

**Net-new authoring.** No prior `agent.md` at the target path (`.claude/agents/health-implementer/` does not exist). Per the protocol's net-new case: baseline = **0/10 on all 10 dimensions**; **all 10 are research targets.**

Line/token targets (reconciled across two authorities):
- `/upgrade-agent` HARD RULE: ≤200 lines hard max, ~140 target; ~2,000 token target.
- Design doc R3 (§5 rule 3): body ≤200 lines / ≤2,500 tokens; target 150–180.
- S9 precedent (Role 1): deployed at 127 lines / ~3,252 tokens with a **documented medical-domain token overrun** (8-class enum + GRADE HALT + H-class composition + 3-mechanism anti-sycophancy are load-bearing density). Token ceiling is treated as soft-with-documentation per S9, line ceiling (200) as hard.
- **Target for Role 2:** 150–180 lines, ≤200 hard. Token overrun documented if it occurs (do not compress at the cost of a safety property — S9 precedent + design doc Limitation 14 alert-fatigue).

## Phase 2 — Agent-Specific Rubric (per-dimension 9/10 + 7/10 + verification)

All dimensions ground to design-doc sections; a 9/10 means the agent.md faithfully encodes the design-doc contract for that dimension at deployable density.

| # | Dimension | 9/10 for health-implementer | 7/10 (min) | Judge verification |
|---|---|---|---|---|
| 1 | Identity Clarity | Identity = §2.1 (≤40-word declarative; "runs once per specialist and stops" purpose clear in 30s); anti-sycophancy "strength of argument not speaker's role" anchor in first 20 lines | Purpose clear but anchor below line 20 | Read first 20 lines; confirm anchor + ≤40-word Identity |
| 2 | Context Efficiency | 150–180 lines, ≤200 hard; no duplication with library-index; token overrun documented if present | ≤200 lines, minor redundancy | `wc -l`; tiktoken; diff vs library-index |
| 3 | Behavioral Specificity | Core Rules from §5 (12→compressed); each testable (cites the §13 binary it satisfies); first-person on the learned-failure rules (§5 r6, r10) | Rules concrete, some thresholds vague | Each rule has pass/fail; no platitudes |
| 4 | Reference Integration | library-index.md companion maps §10.2 conditional reads; ≤30 lines, ≤5 refs; no Context7 override (static project refs, per Role 1 precedent) | Mostly correct, one stale path | Glob every path; confirm ≤5 refs |
| 5 | Boundary Enforcement | §2.2 I-own (8 items) / I-do-NOT-own (10 items, owning role in parens); escalation = Architecture Question routing | Owned/not-owned present, escalation vague | Every not-owned names a role; AQ escalation present |
| 6 | Communication Protocol | §9 two-register: 7-field structured list to orchestrator; 3–5-line sample to user; "7 fields MUST NOT appear in user output" | Two registers present, format loose | Both registers; output format specified not prose |
| 7 | Failure Recovery | §7 Loop-Breaking: 6 concrete thresholds (revision cap 2, persona zero-tolerance, second-person budget 3, refusal-invention zero, audit-failure 3-paths, context-scratch >5); DUAL-GATE clause | Thresholds present, 1–2 non-numeric | Each threshold has number/binary; dual-gate present |
| 8 | Tool Awareness | §8 permitted/forbidden; negative constraints (no sub-sub-agents, no state-mutating git, no aplus-research invocation); every verb has a tool | Tools listed, weak negatives | Every verb→tool; forbidden list present |
| 9 | Anti-Pattern Coverage | §11.2: 5–8 "I don't X" each citing a PF-S\d+-\d+ (≥3 distinct, incl PF-S2-04/PF-S3-01/PF-S6-01); Negative Examples (§12) ≥3 BAD/GOOD in last 30 lines | 5 anti-patterns, ≥3 PFs | grep PF IDs resolve; ≥3 pairs; placement |
| 10 | Freshness | Tool/skill names current (`/aplus-research`, `/upgrade-agent`, hook v2.5); §13 paths reflect reality (audit script PROPOSED/not-yet-existing stated honestly) | Mostly current | No stale claims; PROPOSED state honest |

**Research grouping (default 3, proven in S9):**
- **R1 Behavioral Traits** → Identity (§2.1), Core Rules (§5), Role Boundaries (§2.2), Ask-vs-Proceed (§6), Loop-Breaking (§7). Dims 1,3,5,7.
- **R2 Tools & Configuration** → Tools (§8), Context Loading (§10), library-index.md companion, Modes (§2.2/§13 r15), aplus-research mode-floor. Dims 2,4,8,10.
- **R3 Communication & Anti-Patterns** → Communication (§9), Anti-Patterns (§11), Negative Examples (§12). Dims 6,9.

**Net-new note:** because the design doc is near-deployable prose, the research task is *faithful compression to ≤200 lines* (not net-new derivation). Research-waste risk is low; over-inclusion (copying the full 780 lines) is the real risk — each researcher produces a Minimum Viable Encoding + Cut Rationale.

**Hook watch (rc1):** dispatch prompts avoid literal role-tagged H1 (`# health-implementer` as a standalone line) and literal `roles/<slug>/agent.md` paths; researchers Read the source files themselves from provided paths.
