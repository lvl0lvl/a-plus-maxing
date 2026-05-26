---
title: Judge — R2 Tools & Configuration
type: upgrade-agent-artifact
phase: 4
role: quality-judge
artifact_under_check: R2-tools-configuration.md
created: 2026-05-26
---

# Judge R2

## Summary
- Dimensions scored: 4 (D2, D4, D8, D10)
- All >= 9? YES
- Verdict: PASS

## Per-dimension scores

### D2 — Context Efficiency: 9/10

**Evidence.**
- Output A "Tools" section: self-reported 7 lines (3 paragraphs + 4 blank/header), within the ≤12 budget (R2 line 23). Inspection of the fenced block (R2 lines 13-21) confirms 3 substantive paragraphs (Permitted / Skills / Forbidden) plus the `## Tools` header — within budget.
- Output B "Context Loading" section: self-reported 9 lines, within ≤12 budget (R2 line 41). Inspection of the fenced block (R2 lines 27-39) confirms 4 paragraphs (Auto-load / Substrate / Project spec / Conditional) + Skip-pre-loading rule + header — within budget.
- Output C "library-index": ~32 body lines, within ≤80 budget (R2 line 74).
- Output D "catalog row": single-line table row (R2 line 79) — within catalog row format.
- No verbatim duplication between agent.md sections and library-index: the library-index Reference Map (R2 lines 54-60) covers only the conditional refs from §10.4; auto-loads and substrate are explicitly excluded by the preamble (R2 line 50), avoiding the per-rubric "no content duplicated" requirement (agent-rubric D2 line 33).
- "Minimum Viable Encoding" (R2 lines 83-100) and "Cut Rationale" (R2 lines 102-113) demonstrate active token discipline — items considered and excluded with reasons (PF-S2-06 reasoning cut to R1; §10.7 meta-commentary cut; F-S13 cut as out-of-scope; audit cookbook cut; per-reference token counts cut).

**Minor observation (not blocking 9):** Output A's Permitted paragraph is long-form prose with many clauses. It fits the 12-line budget when rendered, but the density is at the upper end of what AGENT_TEMPLATE.md "imperative + scannable" expects. This does not drop the score below 9 because the rubric D2 budget is line-based and the count is well within ≤12.

No remediation required.

### D4 — Reference Integration: 9/10

**Evidence.**
- 4 auto-load files explicitly enumerated in Output B (R2 line 30): `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, `vault/library/_source-whitelist.md`. Matches design-doc §10.1 per Source citations (R2 line 164).
- Substrate `domain-research.md` named with "read in full at dispatch start; cite Findings by number, never paraphrase" discipline (R2 line 32), satisfying the agent-rubric D4 "auto-load list = 4 files + substrate" requirement.
- HALT semantics: `HALT context-load-missing if any absent` (R2 line 30) — satisfies the design-doc §10.1 HALT requirement and provides the failure-mode wiring the rubric expects.
- library-index Reference Map (R2 lines 54-60) covers all five conditional categories from design-doc §10.4 (aplus-research SKILL, vault/WIKI.md, AGENT_TEMPLATE.md + role profiles, vault decisions, regulatory primary text), each with a "When to Load" trigger column and "Role-Specific Notes" column matching `LIBRARY_INDEX_TEMPLATE.md` lines 7-11.
- Loading Rules (R2 lines 62-67): max-3-refs cited from catalog.md Budget Guardrails; skip-pre-loading rule cited from design-doc §10.5; cross-reference pairs enumerated; MCP-first override explicitly marked inapplicable with reasoning ("all references above are static project artifacts (skill docs, vault content, regulatory text)"). This addresses the agent-rubric D4 "Context7 override pattern present if Tools section references library frameworks" — by stating the override is *inert* for this role's reference set, R2 makes the conditional check pass affirmatively rather than leaving it unaddressed.
- "Notes on framework" (R2 lines 69-71) prevents the orchestrator from routing shared library refs to this profile — defensive against catalog-routing drift.
- Skip-pre-loading rule re-stated inside Context Loading section (R2 line 38) as well as inside library-index — paired enforcement.

No remediation required.

### D8 — Tool Awareness: 9/10

**Evidence.**
- Tri-partite split present per agent-rubric D8 line 105:
  - **Permitted** paragraph (R2 line 16) names: Read, Glob, Grep with path scope; Write/Edit with path-scoped allowlist (3 paths); Bash for audit scripts/schema validators/read-only git (`status`, `diff`, `log`); Agent/Task with INV-ROLE-INLINING and "no sub-sub-agents"; basic-memory MCP (search + close-time write); context7 MCP; github MCP read-only.
  - **Skills** paragraph (R2 line 18) names: `/adversarial-review`, `/critique` at Phase 3; aplus-research as REFERENCED-not-dispatched; `/upgrade-agent` as consumer.
  - **Forbidden** paragraph (R2 line 20) names: tavily MCP / WebSearch / WebFetch; vault-write paths (compounds/biomarkers/protocols/library); basic-memory delete operations (`delete_note`, `delete_project`); github mutation MCPs (`create_pull_request`, `merge_pull_request`, `create_branch`, `push_files`); state-mutating git (commit, push, reset --hard, restore); sub-sub-agent dispatch; runtime aplus-research dispatch; Edit on DESIGN_DOC_TEMPLATE.md / domain-research.md / AGENT_TEMPLATE.md.
- Forbidden item count: ≥5 satisfied — I count 8 distinct forbidden categories (well above the ≥5 rubric threshold at D8 line 111).
- `tavily|WebSearch|WebFetch` grep target (D8 line 112) — all three present in forbidden paragraph.
- Operational completeness table (R2 lines 119-139) maps every verb in Outputs A+B+C to a permitted tool or named workflow. 18 verbs sampled — every one has a tool name. Result line (R2 line 140): "every verb maps to a permitted tool or named workflow. No orphan verbs." This satisfies agent-rubric D8 line 113 (sample 5 verbs) and the upgrade-agent.md HARD RULE "every verb in agent.md has a corresponding tool or workflow."
- Negative constraints (the "what NOT to use tools for" requirement at upgrade-agent.md D8 row 8) are explicit and behavior-shaped, not generic — e.g., "Write/Edit ONLY on [3 paths]," "Bash for [audit scripts/schema validators/read-only git]" (positive constraint with implicit negative), plus the entire Forbidden paragraph.
- Cross-role anchor present: INV-ROLE-INLINING for Agent/Task dispatch; Pass-1 Lesson 1 cited for sub-sub-agent forbiddance (R2 lines 149, 161).

No remediation required.

### D10 — Freshness: 9/10

**Evidence.**
- Regulatory anchors named in library-index (R2 line 60): FD&C Act §520(o)(1)(E); FDA 2026 CDS Final Guidance §V; IMDRF SaMD N12; FDA GMLP principles 1-10. The agent-rubric D10 grep target requires ≥3 of `FD&C|FDA 2026|IMDRF|GRADE|OCEBM` — R2 hits 4 (FD&C, FDA 2026, IMDRF, GMLP — and GRADE is named in the rubric as covered by D3; not R2's scope to embed here).
- Tool names current: Read, Glob, Grep, Write, Edit, Bash, Agent/Task are the current Claude Code tool surface. MCP server names — `basic-memory`, `context7`, `github`, `tavily` — match the currently installed MCP servers (per `~/.claude/CLAUDE.md` global instructions catalog).
- MCP tool names cited match current schema:
  - `mcp__basic-memory__delete_note` and `delete_project` (forbidden list, R2 line 20) — match the current basic-memory MCP tool surface visible in the deferred-tool list.
  - `mcp__github__create_pull_request`, `merge_pull_request`, `create_branch`, `push_files` (forbidden list, R2 line 20) — match the current github MCP tool surface.
- No stale framework versions: the role consumes no framework refs (per "Notes on framework," R2 lines 69-71), so version-staleness exposure is structurally zero. Context7 override pattern marked inapplicable with reasoning (R2 line 67) — this is the correct freshness posture for a role with no framework dependencies, per LIBRARY_INDEX_TEMPLATE.md lines 20-29 (override is for "rapid release cycles," which static project artifacts don't have).
- Project anchors: `INV-ROLE-INLINING`, `PF-S2-05`, `PF-S2-06` named in Outputs A and B and Cut Rationale — these match the currently-active invariant and process-failure register IDs.
- Self-dating: artifact frontmatter `created: 2026-05-26` and design-doc references dated to current synthesis cycle.

No remediation required.

## Findings (sorted by severity)

None. All four scored dimensions reach 9/10.

## Notes

- R2 is unusual among research outputs in that it makes its compression discipline auditable: "Minimum Viable Encoding" (R2 lines 83-100) names the 15 load-bearing lines, and "Cut Rationale" (R2 lines 102-113) names what was excluded and why. This is the right shape for a D2/D8 deliverable — it lets the downstream synthesis pass know which lines may NOT be cut further without violating verification criteria.
- The "Operational completeness check" table (R2 lines 119-139) is the strongest piece of D8 evidence in the artifact — it pre-satisfies the rubric's verb→tool grep sample of 5 by exhaustively mapping 18 verbs.
- The library-index "Notes on framework" paragraph (R2 lines 69-71) is a useful defensive instruction to the orchestrator that prevents shared library refs from being routed to this profile. Worth preserving through synthesis.
- One area worth a synthesis-time note (not a remediation, score-affecting issue): the Permitted paragraph in Output A is a single dense sentence-block. If the deployed agent.md needs to fit a stricter scannability test downstream, breaking it into bulleted form within the 12-line budget would help readability without changing content. Not required for D2/D8 pass.
- R2 correctly distinguishes "REFERENCED-not-dispatched" for aplus-research in two places (Tools and library-index) — this is the load-bearing constraint that prevents the architect from invoking the runtime research pipeline and is the kind of role-specific operational discipline D8 was designed to catch.
