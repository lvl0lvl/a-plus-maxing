---
title: Phase 2 Agent-Specific Rubric — health-specialist-architect
type: upgrade-agent-artifact
phase: 2
created: 2026-05-26
source_design_doc: design/health-specialist-architect-design.md (Status: Final)
binds: generic 10-dimension rubric (upgrade-agent.md §Agent Rubric) + design-doc §15.2 7 binary ACs
---

# Agent-Specific Rubric

This rubric binds the `/upgrade-agent` 10 generic dimensions to **health-specialist-architect** specifics. Each dimension defines a 9/10 (pass) state and a 7/10 (minimum acceptable improvement) state plus verification criteria a judge MUST check.

The 7 §15.2 design-doc ACs are role-specific binary checks. They are not redundant with the 10 dimensions — the design-doc ACs verify role-specific deliverable shape (template variant, refusal taxonomy, citation discipline). The 10 dimensions verify generic agent-profile shape. Both must pass.

---

## D1 — Identity Clarity

**9/10 (pass).** Identity sentence ≤40 words, declarative, no `must|never|always|refuse` lexicon (design-doc §5 rule 3 + R1). Anti-sycophancy anchor lands in the **first 20 lines** of agent.md (NAACL 2024 primacy effect; command HARD RULE). Three-mechanism anti-sycophancy structure cited: A (multi-agent silent agreement), B (single-model acquiescence), C (RLHF preference drift) per design-doc §4 OUTBOUND row 4. A reader knows the role's purpose in 30 seconds: designs the medical-specialist template variant + discipline doc + audit script.

**7/10 (min acceptable).** Identity sentence ≤40 words; anti-sycophancy clause present in first 30 lines; at least Mechanism C named.

**Verification criteria (judge):**
- Count words in Identity sentence (≤40)
- Grep Identity body for `must|never|always|refuse` — must be 0 matches in Identity body (these belong in Core Rules)
- Locate first anti-sycophancy line — line number ≤ 20
- Grep for `Mechanism A`, `Mechanism B`, `Mechanism C` — all three present
- Confirm role purpose stated as "template + discipline doc + audit script" (Finding 9 triangle) within first 30 lines

## D2 — Context Efficiency

**9/10 (pass).** Total agent.md line count ≤ 200 (hard max). Per-section budgets respected per upgrade-agent.md table (Header+Identity ≤15, Core Rules ≤15, Role Boundaries ≤8, Ask vs Proceed ≤10, Loop-Breaking ≤6, Tools ≤12, Communication ≤20, Context Loading ≤12, Anti-Patterns ≤8, Modes ≤30, Negative Examples ≤30). Token count ≤ 2,000 (cl100k_base). No content duplicated between agent.md and library-index.md.

**7/10 (min acceptable).** Total ≤ 200; one section may exceed its budget by ≤2 lines if compensated elsewhere. Token count ≤ 2,000.

**Verification criteria (judge):**
- `wc -l agent.md` ≤ 200 (mechanical; hard max, no rounding)
- Per-section line counts within budgets
- Tiktoken cl100k_base count ≤ 2,000
- No verbatim duplication with library-index.md

## D3 — Behavioral Specificity

**9/10 (pass).** 8-12 Core Rules. Each rule has a concrete pass/fail condition. Voice tags: imperative for standing instructions, first-person for learned-experience rules (design-doc §5 pattern). GRADE two-axis (certainty × recommendation-strength) tagging in a rule body (design-doc §5 rule 12; HALT condition spelled out). H-class composition rule in a rule body (design-doc §5 rule 13; `max(Role3.nominal, Role4.worst_case_reachable)`).

**7/10 (min acceptable).** 8 Core Rules; majority testable; GRADE and H-class rules present even if HALT-condition compressed.

**Verification criteria (judge/fact-checker):**
- Core Rules count between 8 and 12
- Each rule has a testable pass/fail (fact-checker check)
- Voice mix: ≥2 first-person, remainder imperative (per design-doc §5 pattern)
- Grep Core Rules body for `GRADE`, `certainty`, `recommendation strength` — ≥1 match
- Grep Core Rules body for `H-class|H1|H2|harm.class|worst.case.reachable|max\(Role` — ≥1 match
- Each rule cites at least one of: Finding N / PF-S\d+-\d+ / R\d+ / INV-* / regulatory criterion (design-doc §5 rule 1)

## D4 — Reference Integration

**9/10 (pass).** library-index.md maps each design-doc §10 reference to load conditions (auto-load vs conditional). Mandatory auto-load list = 4 files per design-doc §10.1 (operator-profile, current-state, goals, source-whitelist) + substrate `domain-research.md`. Conditional reads enumerated with trigger conditions. Pre-load forbidden per design-doc §10.5. Max-refs ≤ 3 per task per catalog.md. Context7 override pattern present if Tools section references library frameworks.

**7/10 (min acceptable).** library-index.md present; 4 auto-loads enumerated; conditional reads listed; max-refs limit cited.

**Verification criteria (fact-checker):**
- library-index.md exists at `~/Documents/Projects/skills_library/roles/health-specialist-architect/library-index.md`
- Reference paths in library-index resolve (Glob check)
- 4 auto-load files named with correct paths
- Max-refs limit cited (≤3 per design-doc inheritance from catalog)

## D5 — Boundary Enforcement

**9/10 (pass).** Role Boundaries section enumerates "I own" (8 items per design-doc §2.2) and "I do NOT own" (8 items per design-doc §2.2) with owning role in parentheses. Escalation rule cited (design-doc §2.2 "when I detect a problem in a not-owned area"). Role-4 architectural slot mentioned for Council-Mode dissent (design-doc §2.2 item 6 + §4 OUTBOUND row 7).

**7/10 (min acceptable).** ≥6 items per side; owning roles in parentheses; escalation rule present.

**Verification criteria (judge/fact-checker):**
- Grep "I own" then count items
- Grep "I do NOT own" then count items
- Every "do NOT own" item has a role name in parentheses
- Grep for `medical-safety-reviewer|Role 4|Council-Mode` — ≥1 match

## D6 — Communication Protocol

**9/10 (pass).** Three distinct audience formats: (a) orchestrator structured-list (7 fields per design-doc §9.1: Status / Artifact paths / Coverage tally / Mechanical-check status / Decisions / Blockers / Pass-1 anchor check); (b) downstream-specialist sentence-pattern per design-doc §9.2; (c) user plain-language per design-doc §9.3 with explicit "fields from §9.1 NOT in §9.3" guard (design-doc §9.3 + F-021 disposition).

**7/10 (min acceptable).** Three audiences distinguished; orchestrator format names ≥5 fields.

**Verification criteria (fact-checker):**
- Communication section has ≥3 distinct sub-sections labeled by audience
- Orchestrator format names ≥5 of the 7 fields
- Grep for "fields from .* NOT.*user-facing|orchestrator-internal" — ≥1 match (audience-separation discipline)

## D7 — Failure Recovery

**9/10 (pass).** Loop-Breaking section has ≥5 thresholds per design-doc §7: spec-revision cap (numeric, 2); design-review cap (numeric, 3); context-scratch threshold (binary); LIVE-tag cap (binary); cross-role-reference fabrication zero-tolerance. Each threshold has its numeric/binary value stated.

**7/10 (min acceptable).** ≥3 thresholds with numeric/binary values.

**Verification criteria (fact-checker):**
- Loop-Breaking section has ≥3 numeric or binary thresholds
- Each threshold names its condition + value
- Grep for `cap|threshold|HALT|escalate` — ≥3 matches

## D8 — Tool Awareness

**9/10 (pass).** Tools section has tri-partite split: permitted (Read/Glob/Grep/Write/Edit on permitted paths/Bash read-only-git/Agent/basic-memory/context7/github-read-only); permitted skills (`/adversarial-review`, `/critique`, aplus-research as REFERENCED-not-dispatched, `/upgrade-agent` as consumer); explicit forbidden list (tavily/WebSearch/WebFetch; vault-write paths; delete operations; PR-mutation MCP calls; state-mutating git; sub-sub-agent dispatch; aplus-research runtime; Edit on template/substrate). Every verb in agent.md has a corresponding tool or workflow (operational completeness).

**7/10 (min acceptable).** Permitted + forbidden lists present; ≥3 forbidden items named; operational completeness satisfied for primary verbs.

**Verification criteria (fact-checker):**
- Three sub-sections: permitted / skills / forbidden
- Forbidden list contains ≥5 items
- Grep for `tavily|WebSearch|WebFetch` in forbidden context — present
- Operational completeness: for every verb in agent.md, grep produces a tool name (sample 5 verbs)

## D9 — Anti-Pattern Coverage

**9/10 (pass).** 5-8 anti-patterns per AGENT_TEMPLATE.md guidance. Each anti-pattern: (a) "I don't X" framing; (b) source citation (PF-S\d+-\d+, Finding N, or R\d+); (c) recognition cue. Design-doc §11.2 has 8; deployed agent.md may compress to 5-7 if §11 list is selected by leverage. Negative Examples section at end of file (recency effect) with ≥2 BAD/GOOD pairs (design-doc §12 has 4 — deployment may select top-2 by leverage if line-budget pressure).

**7/10 (min acceptable).** 5 anti-patterns; ≥2 BAD/GOOD pairs in Negative Examples; Negative Examples in last 30 lines.

**Verification criteria (judge/fact-checker):**
- Anti-Patterns section line count 5-8 entries
- Every entry starts with "I don't" (or equivalent imperative)
- Every entry has at least one source citation (Grep for `PF-S|Finding|R[0-9]`)
- Negative Examples section line number ≥ (total_lines - 30)
- BAD/GOOD pairs count ≥ 2; each pair is role-specific (mentions template/audit/specialist/Finding)

## D10 — Freshness

**9/10 (pass).** References cite current regulatory anchors (FD&C Act §520(o)(1)(E); FDA 2026 CDS Final Guidance; IMDRF SaMD N12; GRADE; OCEBM 2011). No stale framework versions. Context7 override pattern present if agent.md cites versioned APIs. Project anchors (PF-S6-01 latest at finalize; INVARIANTS register 12 entries) re-verified at synthesis time.

**7/10 (min acceptable).** Regulatory anchors named; PF and INV references current as of design-doc finalize.

**Verification criteria (fact-checker):**
- Grep for `FD&C|FDA 2026|IMDRF|GRADE|OCEBM` — ≥3 matches
- PF-S6-01 cited as latest OR PF-S\d+-\d+ chain ends at PF-S6-01 in any list
- INVARIANTS register count (12) cited or referenced

---

## Design-doc §15.2 ACs as additional binary checks

These 7 checks are role-specific binary pass/fail beyond the 10 generic dimensions. The deployed agent.md inherits §15.2 ACs that map to agent.md content (not all 7 do — ACs 1-3 are design-doc deliverable-level, not agent.md-level). The agent.md-relevant ACs:

| AC | One-line claim | Verifiable in agent.md? |
|---|---|---|
| AC-1 | Template variant artifact present | NO — design-doc-level deliverable (template lives elsewhere) |
| AC-2 | All 9 Pass-1 Findings have a template-section anchor | NO — design-doc-level |
| AC-3 | All 15 Pass-1 Recommendations have a verdict | NO — design-doc-level |
| AC-4 | Refusal-class taxonomy enumerated as OUTBOUND; 8 identifiers each appear ≥1 in design doc | PARTIAL — agent.md should mention `AUTHORITY_FRAMING_BYPASS` since it's the 8th class and the 81.8% attack vector |
| AC-5 | Citation discipline encoding present | YES — agent.md Core Rules + Tools must mention citation-verification |
| AC-6 | Project PF coverage attested (8 PFs IN-SCOPE / OUT-OF-SCOPE in §11.1) | NO — design-doc-level; agent.md cites PFs in Anti-Patterns, but doesn't carry the full table |
| AC-7 | Refusal taxonomy referenced not redefined | YES — agent.md must cite Finding 5 or design-doc §2.2 item 3 for the taxonomy, not redefine |

The agent.md-binding subset (AC-4 partial, AC-5, AC-7) is folded into D1/D3/D5/D8/D9 verification criteria above.

---

## Operational completeness (cross-cutting check)

Per upgrade-agent.md HARD RULE: every verb in agent.md must have a corresponding tool or workflow. Fact-checker samples ≥5 verbs and verifies each:

- "dispatch" → Agent tool (or `/adversarial-review`, `/critique` skills)
- "Read" / "Grep" / "Glob" → corresponding tool listed in Tools
- "write" / "Edit" → Write/Edit tools, with permitted-path constraint
- "audit" → bash with audit script invocation
- "escalate" → workflow named (write contract-violation finding to Phase-3 red-team channel)

A verb without a tool or workflow named = fail.

---

## Pass condition

Agent.md passes Phase 4 validation IFF:

1. All 10 generic dimensions score ≥ 9/10 (judge)
2. All fact-checker mechanical items PASS (no failures)
3. Operational completeness: every sampled verb has a tool/workflow

No rounding, no softening. Pass threshold is binary at the per-dimension level.
