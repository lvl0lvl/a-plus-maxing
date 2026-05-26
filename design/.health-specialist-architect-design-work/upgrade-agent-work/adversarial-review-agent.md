---
title: Phase 6 Adversarial Review — health-specialist-architect agent.md
type: upgrade-agent-artifact
phase: 6
created: 2026-05-26
target: ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md (119 lines, 3,127 cl100k tokens)
paired:
  - ~/Documents/Projects/skills_library/roles/health-specialist-architect/library-index.md (24 lines)
  - ~/Documents/Projects/skills_library/roles/orchestrator/catalog.md (row 17 health-specialist-architect)
source_of_truth: design/health-specialist-architect-design.md (873 lines, Status: Final)
template: ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md (97 lines)
prior_dispositions: design/.health-specialist-architect-design-work/finding-classifications.md (38 findings — 26 LEGITIMATE, 11 LEGITIMATE-MODIFIED, 1 REJECTED)
---

## Summary

**Counts by severity** (15 findings total)

| Severity | Count |
|---|---|
| Critical | 1 |
| Major | 5 |
| Minor | 6 |
| Nitpick | 3 |

**Mechanical coverage tally**

| Check | Result |
|---|---|
| 10 AGENT_TEMPLATE base sections + Modes | PASS (11 H2s present) |
| Anti-sycophancy anchor ≤ line 20 | PASS (line 7, 9) |
| Negative Examples in last 30 lines | PASS (line 107 of 119; offset 12 from end) |
| Line count ≤ 200 (hard max) | PASS (119) |
| Token count ≤ 2,000 target | FAIL (3,127 cl100k; +56% overrun) |
| Library-index reference paths resolve | PASS (5/5 paths verified) |
| Catalog row matches profile | FAIL — token budget cell stale (~1,900 vs 3,127 actual) |

**Headline findings.** One Critical contradiction inherited from the design doc (refusal-class count: agent.md says 8, design-doc §1 still says 7 in three locations). Five Major findings cluster around (a) the 3,127-token vs catalog "~1,900" mismatch, (b) the Modes-placement deviation from the design-doc §12.4 canonical sequence, (c) the underspecified "Phase-3 channel" reference, (d) Loop-Breaking compressing 5 thresholds to 4 (one bullet bundles spec-revision-cap=2 with design-review-cap=3 in a way the rubric D7 minimum permits but the rubric D7 9/10 pass condition does not), and (e) the design-doc §10.1 "do NOT personalize architect-output to operator content" compressed into a clause whose grammar admits the opposite reading.

---

## Findings (sorted by severity)

### F-A01 — Refusal-class count inherits an upstream contradiction — Critical
**Category.** Internal Contradictions / Broken References (inherited).
**Section.** Agent.md line 22 (Core Rule 10: "The 8-class refusal taxonomy"), line 28 (Role Boundaries: "the 8-class refusal taxonomy").
**Description.** Agent.md correctly says **8** classes. The source-of-truth design doc says BOTH "7-class" (lines 31, 91, 168, 647 of `design/health-specialist-architect-design.md`) and "8 classes" (lines 127, 359, 806). The 8-class count is the post-Phase-4 corrected count (F-S2 LEGITIMATE disposition added `AUTHORITY_FRAMING_BYPASS` as the 8th class per Role 4 substrate L324-L328). Agent.md is internally consistent (count = 8; eight identifiers enumerated in Core Rule 10), but a reader cross-referencing the design doc will encounter the 7-class language and infer the agent.md double-counts. Promoted from Minor to Critical because the count is load-bearing for §13 row 4 grep behaviour, AC-4 audit criterion, and CB §10 row 1 inheritance — any downstream specialist that reads the design-doc §1 framing will under-count the taxonomy.
**Evidence.**
- agent.md:22 — "The 8-class refusal taxonomy (`PATIENT_FACING_DIRECTIVE`, ... `AUTHORITY_FRAMING_BYPASS`)"
- agent.md:28 — "the 8-class refusal taxonomy"
- design-doc:31 — "7-class taxonomy keyed to FD&C Act §520(o)(1)(E)"
- design-doc:91 — "regulation-grounded 7-class refusal taxonomy"
- design-doc:168 — Core Rule 11 cites "7-class refusal taxonomy"
- design-doc:647 — AC-7: "§4 + §11 + §12 do not inline-duplicate the 7-class enum's definitions"
- finding-classifications.md:F-S2 disposition — "Fixed: 8th refusal class added"
**Suggested fix.** This is not a defect of agent.md but of the upstream design-doc residual 7-class language. Two options:
  (a) Treat as out-of-scope for agent.md; record an explicit note in Phase-7 close that the design doc has post-Phase-4 residual "7-class" mentions to be corrected in a follow-up bead (preferred — keeps Phase 6 surgical).
  (b) Add a one-line footnote to agent.md Core Rule 10 / Role Boundaries: `Count corrected from 7 to 8 per F-S2 disposition; design-doc §1 + §3.1 + §5.11 + §15.2 carry residual "7-class" prose pending correction.`
**Prior disposition.** F-S2 (LEGITIMATE) — fix landed for §2.2 / §4 / §11 / §13 but missed §1, §3.1, §5.11, §15.2. Reject-but-adopt does not apply; this is a partial-fix completion gap.

### F-A02 — Token budget catalog row is stale (~1,900 stated, 3,127 actual) — Major
**Category.** Internal Contradictions / Downstream Breakage.
**Section.** catalog.md line 17 (Token Budget column).
**Description.** The catalog row claims "~1,900 tokens" but cl100k_base measurement against the synthesized agent.md yields **3,127 tokens** (+64%). Downstream orchestrator routing uses Token Budget for the budget-guardrail check ("identity core + references < 8,000 tokens"). A 3,127 identity-core leaves only ~4,800 tokens for 3 references; combined with the 1,200-1,800 single-reference target that is feasible for one ref but not three. Catalog row will misroute under "if a task genuinely needs more context: Split into sub-tasks" because the budget check uses the wrong divisor.
**Evidence.**
- catalog.md:17 — `| health-specialist-architect | roles/health-specialist-architect/agent.md | ... | ~1,900 tokens | ...`
- `tiktoken.get_encoding('cl100k_base').encode(agent.md)` → 3,127
- agent-rubric.md D2:33 — "Token count ≤ 2,000 (cl100k_base)" (9/10 pass condition)
- baseline-scorecard.md:24 — `| Token count (agent.md) | 0 (file absent) | ≤2,000 |`
**Suggested fix.** Update catalog.md line 17 Token Budget column to `~3,127 tokens (above generic ≤2,000 target; characterized in Phase 6 review)`. Add a comment in the row's Pairs With column: "Above-budget by structural commitment (medical-domain regulatory anchors); see adversarial-review-agent.md token-budget characterization."
**Prior disposition.** None — this is net-new from the actual synthesis output.

### F-A03 — Modes section placement deviates from the §12.4 canonical sequence — Major
**Category.** Internal Contradictions / Downstream Breakage.
**Section.** Agent.md line 88 (Modes) — appears BEFORE Anti-Patterns (line 98) and Negative Examples (line 107).
**Description.** Agent.md places Modes between Context Loading and Anti-Patterns. The design-doc's own §12.4 GOOD example explicitly states "Mature profiles add Modes between Anti-Patterns and Negative Examples." This is a self-referential consistency defect: the agent.md author followed a section order that the design doc's own Negative Example says is incorrect. Downstream `enforce-role-inlining.sh` hook expects 11 sections but its smoke tests (8/8 per INV-ROLE-INLINING) may not enforce order — verify against `hooks/tests/test_enforce_role_inlining.sh` before classifying further.
**Evidence.**
- agent.md:88 — `## Modes` at line 88 (BEFORE Anti-Patterns at 98 and Negative Examples at 107).
- design-doc:460 — "Mature profiles add Modes between Anti-Patterns and Negative Examples."
- design-doc:482 — INV-ROLE-INLINING row says "full 11-section profile verbatim" but does not assert order.
**Suggested fix.** Move `## Modes` (lines 88-96) to between Anti-Patterns (lines 98-105) and Negative Examples (line 107). New order: Context Loading → Anti-Patterns → Modes → Negative Examples. This preserves Negative Examples in last 30 lines (still within budget — Modes is 9 lines, would push Neg Ex section start from 107 to ~116, still within last 30 lines of a 119-line file).
**Prior disposition.** None — net-new from synthesis. Rubric D9 verification criterion only checks "Negative Examples section line number ≥ (total_lines - 30)" — does not constrain Modes order.

### F-A04 — Loop-Breaking compresses 5 design-doc thresholds to 4 by bundling — Major
**Category.** Internal Contradictions / Language Economy.
**Section.** Agent.md lines 45-50 (Loop-Breaking section).
**Description.** Design-doc §7 enumerates **5** thresholds: spec-revision cap (numeric, 2), design-review cap (numeric, 3), context-scratch threshold (binary), LIVE-tag cap (binary), cross-role-reference fabrication threshold (binary, zero-tolerance). Agent.md line 47 collapses spec-revision cap=2 AND design-review cap=3 into one bullet "Revision caps (2/3)" — structurally both values are preserved, but the rubric D7 9/10 pass condition is "≥5 thresholds per design-doc §7"; D7 7/10 (min acceptable) is "≥3 thresholds with numeric/binary values." The agent.md sits at the 7/10 floor, not the 9/10 target.
**Evidence.**
- agent.md:47 — "**Revision caps (2/3).** >2 revisions ... >3 design-review rounds ..."
- agent.md:48-50 — three remaining thresholds (context-scratch, LIVE-tag cap, fabrication threshold).
- design-doc:191-195 — five distinct bullets.
- agent-rubric.md D7 9/10 — "≥5 thresholds per design-doc §7"
**Suggested fix.** Split the bundled bullet into two:
```
- **Spec revision cap (numeric, 2).** >2 revisions without new external evidence → deliver as-is, surface remainder as §18 OQs.
- **Design-review round cap (numeric, 3).** >3 rounds without convergence → escalate with both positions, evidence, and cost.
```
Adds ~1 line; total agent.md becomes ~120, still well under 200.
**Prior disposition.** None — net-new from synthesis compression decision.

### F-A05 — "Phase-3 channel" reference is undefined in agent.md — Major
**Category.** Broken References / Ambiguous Instructions.
**Section.** Agent.md line 32 (Role Boundaries escalation rule).
**Description.** The agent.md says "I write a one-line contract-violation finding (clause + downstream owner) into the Phase-3 channel." The term "Phase-3 channel" is not defined anywhere in agent.md or library-index.md. The design doc §2.2 line 71 spells it out as "the design-doc Phase-3 red-team channel" — i.e., a Phase-3 red-team review artifact under `design/.health-specialist-architect-design-work/red-team-*.md`. An agent dispatched with only agent.md + library-index.md as context cannot resolve "Phase-3 channel" to a concrete artifact path.
**Evidence.**
- agent.md:32 — "I write a one-line contract-violation finding (clause + downstream owner) into the Phase-3 channel."
- design-doc:71 — "I write a contract-violation finding ... into the design-doc Phase-3 red-team channel"
- library-index.md — no mention of Phase-3 channel.
**Suggested fix.** Replace "into the Phase-3 channel" with "into `design/.{role}-design-work/red-team-*.md`" or, if path is intended to vary, with "into the dispatch's design-work Phase-3 red-team artifact."
**Prior disposition.** None.

### F-A06 — Anti-Patterns count 6 misaligns with the §11.2 8-item set; AP coverage of operator-A3 + LIVE-tag is preserved but AP4 (≤3 questions) is silently dropped — Major
**Category.** Scope Violations / Language Economy.
**Section.** Agent.md lines 100-105 (six anti-patterns).
**Description.** Design-doc §11.2 has 8 anti-patterns (AP1-AP8). Agent.md compresses to 6 by dropping AP4 (≤3 clarifying questions / PF-S2-03) and AP6 (FDA prose pattern-match — though this is folded into AP4 of agent.md). The rubric D9 9/10 explicitly permits "may compress to 5-7 if §11 list is selected by leverage," so the count is within tolerance. However, PF-S2-03 (over-questioning) is now uncovered by any agent.md anti-pattern bullet — the F-007 disposition said "AP4 is covered structurally by §7 Loop-Breaking (the cap mechanism)," but agent.md's Loop-Breaking carries no question-count cap (it carries revision/review/scratch/LIVE-tag/fabrication caps). PF-S2-03 has lost its structural anchor in the deployed profile.
**Evidence.**
- agent.md:100-105 — six anti-patterns; PF citations: PF-S3-01, PF-S2-02, PF-S2-04, PF-S2-05, PF-S3-01+PF-S6-01, PF-S2-01.
- agent.md:45-50 — Loop-Breaking has no question-count cap.
- design-doc:355 — AP4 verbatim in §11.2.
- finding-classifications.md F-006 disposition — "AP4 is still valid; the §7 Loop-Breaking audit-script LIVE-tag cap merits explicit promotion to §11.2 as AP7."
- finding-classifications.md F-007 disposition — "AP4 is covered structurally by §7 Loop-Breaking (the cap mechanism)"
**Suggested fix.** Either:
  (a) Add a 7th anti-pattern to agent.md: `- I don't issue more than 3 clarifying questions in scoping; if I have more, I batch and pick top 3 by reversibility cost. [PF-S2-03. Cue: question list longer than 3.]` — keeps the count at 7, still under the rubric D9 5-8 budget.
  (b) Add a question-count cap to Loop-Breaking, citing PF-S2-03, to honor the F-007 "structural coverage" disposition.
Option (a) is simpler and preserves the explicit PF coverage trace.
**Prior disposition.** F-007 (LEGITIMATE-MODIFIED) — structural coverage via §7 was the dispatch-time fix in the design doc; the agent.md drops the structural anchor without preserving the alternative.

### F-A07 — Identity-body §Identity exceeds 40 words (68 words) even though the H1-level role descriptor is compliant — Minor
**Category.** Internal Contradictions / Language Economy.
**Section.** Agent.md line 7 (Identity section body).
**Description.** R1 / design-doc §5 rule 3 / agent-rubric D1 9/10 pass require "Identity sentence ≤40 words, declarative, no `must|never|always|refuse` lexicon." The H1-level role descriptor sentence (line 3, 32 words) satisfies R1. The `## Identity` section body (line 7, 68 words) does not, but the rubric and design doc are ambiguous about whether "Identity sentence" refers to (a) the role descriptor under H1 only, or (b) the full `## Identity` section content. Behavioral-lexicon scan on the Identity body passes (must=0, never=0, always=0, refuse=0). The 40-word constraint is ambiguous between the two interpretations.
**Evidence.**
- agent.md:3 — H1-level role descriptor sentence: 32 words. PASS.
- agent.md:7 — `## Identity` body first paragraph: 68 words. FAIL if R1 applies to this layer.
- AGENT_TEMPLATE.md:7-13 — the template's `## Identity` section has 7 lines of prose, exceeding 40 words; treated as multi-sentence by template.
- design-doc:150 — Rule 3 says "Identity ≤40 words"; no disambiguation between H1 descriptor vs §Identity body.
**Suggested fix.** Two paths:
  (a) Treat as ambiguity in R1's scoping; record interpretation in close: "R1 binds the H1-level role-descriptor sentence; §Identity body is multi-sentence by AGENT_TEMPLATE.md precedent." No agent.md change.
  (b) Compress the §Identity body to ≤40 words per Mechanism-anchoring clause. Mechanism C anchor + mechanism mapping in 40 words: `Update position when arguments have technical merit; otherwise maintain with cited evidence. Mechanism C is the RLHF-drift anchor; Mechanism A routes to Role 4; Mechanism B is the maintain-position clause.` (~38 words.)
Recommend (a) — the H1-level sentence is what readers consume as "the identity"; the §Identity body is the anti-sycophancy anchor. Two layers, two purposes.
**Prior disposition.** None.

### F-A08 — "do NOT personalize architect-output to operator content" reads as imperative-against-the-architect but a sloppy parse can flip it — Minor
**Category.** Ambiguous Instructions.
**Section.** Agent.md line 78 (Context Loading "Auto-load" clause).
**Description.** "Read to author template defaults against actual file shape; do NOT personalize architect-output to operator content." The grammar parses correctly under attentive reading (architect reads operator-profile to confirm the template's Context Loading clause is shaped to actual file fields; the architect does not embed Walter's January 2026 issue into the template). Under skim reading, "personalize architect-output to operator content" can be misparsed as "the architect's output should adapt to operator state" — exactly the failure mode AP3 forbids. The Negative Example at lines 115-119 reinforces the correct reading but is 30+ lines away from the Context Loading clause.
**Evidence.**
- agent.md:78 — "Read to author template defaults against actual file shape; do NOT personalize architect-output to operator content."
- agent.md:102 — Anti-Pattern 3 reinforces the correct reading.
- agent.md:115-119 — Negative Example 12.3-equivalent reinforces it.
- design-doc:290 — "The architect does NOT personalize architect-output to operator content."
**Suggested fix.** Replace with the design-doc explicit form: "do NOT bind the template to operator state (PF-S2-04; AP3)." This eliminates the misparse path by naming the failure mode and citing the AP.
**Prior disposition.** None; F-S3 (LEGITIMATE) addressed the operator-as-A3 mechanism but not this language drift.

### F-A09 — "Max 3 per task" in Context Loading is ambiguous about whether it includes auto-load files — Minor
**Category.** Ambiguous Instructions.
**Section.** Agent.md line 86 (Context Loading skip-pre-loading clause).
**Description.** "Max 3 per task" — referent ambiguous. Library-index.md line 17 makes it explicit: "Max references per task: 3 (per catalog.md Budget Guardrails; inherited)" — meaning 3 LIBRARY references, NOT counting the 4 auto-load files in §10.1 or the substrate in §10.2. Agent.md's compressed phrasing is parsable as "3 files total" which would HALT the agent at file 4 of the auto-load list.
**Evidence.**
- agent.md:86 — "Max 3 per task."
- library-index.md:17 — "Max references per task: 3 (per catalog.md Budget Guardrails; inherited)."
- catalog.md:88 — "Max references per task: 3."
- design-doc:316 — "The architect does NOT pre-load files in §10.4 'just in case.'"
**Suggested fix.** Replace "Max 3 per task" with "Max 3 conditional references per task (auto-load + substrate do not count)."
**Prior disposition.** None.

### F-A10 — `aplus-research REFERENCED in the template I author — not dispatched by me` may be misread as a self-permission to dispatch — Minor
**Category.** Ambiguous Instructions / Scope Violations.
**Section.** Agent.md line 56 (Tools — Skills sub-section).
**Description.** The intent is clear from the design doc: the architect names the skill in the template variant but never invokes it. The agent.md form "REFERENCED in the template I author — not dispatched by me" is correct but the structure invites a misparse where the agent reads "I author — not dispatched by me" as a self-license clause ("by me" rebuts the implicit "dispatched"). Compare with the forbidden-list clause at line 58: "Runtime `aplus-research`" — short, unambiguous. The Skills-section phrasing should mirror the forbidden-list precision.
**Evidence.**
- agent.md:56 — "`aplus-research` REFERENCED in the template I author — not dispatched by me."
- agent.md:58 — "Runtime `aplus-research`" listed under Forbidden.
- library-index.md:9 — "Treat as REFERENCED-not-dispatched. The architect names the skill in the template; the specialist runs it. Do not invoke gates from this role."
- design-doc:219 — "`aplus-research` skill — REFERENCED in the template variant (per R14); NOT dispatched by the architect itself (architect does not produce wiki entries)."
**Suggested fix.** Replace with: "`aplus-research` — named in the template I author; NEVER invoked by this role (mirror: §Forbidden 'Runtime aplus-research')."
**Prior disposition.** None.

### F-A11 — "INVARIANTS.md: 12 entries as of 2026-05-26" embeds a volatile fact that will go stale — Minor
**Category.** Edge Case Gaps / Freshness.
**Section.** Agent.md line 16 (Core Rule 4).
**Description.** Citing the register cardinality "12 entries as of 2026-05-26" in the agent.md body embeds a date-stamped fact. The INVARIANTS register currently has 12 entries (verified via Grep against INVARIANTS.md lines 33-44). The number will increment as new invariants are added (the document's history table on line 58-59 shows ongoing additions). A reader 30 days from now sees a count that may be wrong and has no way to know without re-grepping. Aligns with HANDOFF rotation rule clause 4 (self-dating volatile facts) but the date is buried mid-rule.
**Evidence.**
- agent.md:16 — "[INV-RESEARCH-ATTESTATION; INVARIANTS.md: 12 entries as of 2026-05-26]"
- INVARIANTS.md:33-44 — 12 distinct INV-* IDs confirmed.
- CLAUDE.md HANDOFF rotation clause 4 — "Self-dating volatile facts"
**Suggested fix.** Either (a) drop the "12 entries" parenthetical (it's not load-bearing; INV-RESEARCH-ATTESTATION on its own is the citation); or (b) rephrase as "[INVARIANTS.md register; see file for current count]." Option (a) is simpler.
**Prior disposition.** None.

### F-A12 — Agent.md cites both `Finding 5` and an inline taxonomy enumeration — borderline anti-paraphrase violation — Minor
**Category.** Scope Violations / Language Economy.
**Section.** Agent.md line 22 (Core Rule 10).
**Description.** Core Rule 10 enumerates all 8 refusal-class identifiers inline (`PATIENT_FACING_DIRECTIVE`, ..., `AUTHORITY_FRAMING_BYPASS`). The design doc §12.2 Negative Example explicitly cites this pattern as a BAD example: "The 7 classes are: PATIENT_FACING_DIRECTIVE ... [continues for 20+ lines]" is the BAD form; the GOOD form is "see Finding 5 (`domain-research.md` lines 158-196). The 7 classes are enumerated in Finding 5's table. Roles 2/3/4 reference by Finding number; do not redefine." Agent.md inlines all 8 identifiers as a single comma-separated list, which is less than 20 lines but technically reproduces the enum body in the agent.md body. The AC-7 design-doc rule explicitly says "Refusal taxonomy is referenced not redefined."
**Evidence.**
- agent.md:22 — "The 8-class refusal taxonomy (`PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`, `AUTHORITY_FRAMING_BYPASS`)"
- design-doc:401-413 — §12.2 BAD/GOOD pair against this exact pattern.
- design-doc:647 — AC-7: "§4 + §11 + §12 do not inline-duplicate the 7-class enum's definitions; bodies reference Finding 5 by line range."
**Suggested fix.** Two options:
  (a) Compress to: "The 8-class refusal taxonomy (`PATIENT_FACING_DIRECTIVE` ... `AUTHORITY_FRAMING_BYPASS`; see Finding 5 / design-doc §2.2 item 3 for all 8)." Saves ~5 tokens, satisfies AC-7.
  (b) Keep current form, justify on grounds that the comma-list is not "inline duplication" in the §12.2 sense (which targeted multi-line enum with statutory cites). Add an editorial note to F-A12's close-out disposition.
The current form is a borderline case. The AC-7 wording targets §4 + §11 + §12 of the design doc, not the agent.md. The agent.md is not technically bound by AC-7. Tentatively Minor.
**Prior disposition.** None directly; F-S2 added AUTHORITY_FRAMING_BYPASS but did not address the agent-md-layer enumeration discipline.

### F-A13 — H-class composition rule body (Core Rule 12) inlines 7 items in a comma list rather than citing §4 OUTBOUND row 2 — Nitpick
**Category.** Language Economy.
**Section.** Agent.md line 24 (Core Rule 12).
**Description.** Core Rule 12 says "final_harm_class = max(Role3.nominal, Role4.worst_case_reachable) under H1>H2>…>H8". The list expansion is compact (uses ellipsis), but the rule body cites "§4 OUTBOUND row 2; ICH E2A; FDA 3500A" — three citations for one rule. The H1-H8 enumeration is implicit; readers wanting the full list must read the design doc §4 OUTBOUND row 2. Adequate but dense.
**Evidence.**
- agent.md:24 — "`final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)` under H1>H2>…>H8; H1/H2 auto-block deployment regardless of nominal."
- design-doc:128 — full H1-H8 expansion.
**Suggested fix.** None required — the ellipsis-with-citation pattern is defensible. Note retained for completeness.

### F-A14 — Modes section content is structurally minimal (1 mode); rationale for "1 mode" given but D8 mode-count rubric is silent — Nitpick
**Category.** Edge Case Gaps.
**Section.** Agent.md lines 88-96 (Modes section).
**Description.** Modes section declares "This role operates in a single named mode. Declared so role-tagged dispatches inlined by `enforce-role-inlining.sh` satisfy the 11-section expectation." This is a reasonable structural rationale (defensive against the hook's count check), but the design doc §15 R15 talks about "Auditable named modes with entry/exit conditions + permitted tools per mode" — plural. A single-mode role may technically satisfy R15 if entry + exit + permitted tools are spelled out, but the rubric D7 and §15 phrasing assume plural.
**Evidence.**
- agent.md:89-96 — single Mode: Design with Entry, Exit, Permitted tools.
- design-doc:117 — R15 "Auditable named Modes with entry/exit conditions + permitted tools per mode" (plural).
- agent-rubric.md D7 — "Loop-Breaking ... cap|threshold|HALT|escalate" — not Modes; D-dimension for Modes is folded into D8 Tool Awareness which is silent on mode count.
**Suggested fix.** None required — single-mode is a legitimate structural choice for a meta-role with one purpose. Note retained.

### F-A15 — Library-index "Pre-load forbidden" rule lives in library-index.md only, not agent.md — Nitpick
**Category.** Ordering/Dependency Gaps.
**Section.** Agent.md line 86 vs library-index.md line 18.
**Description.** Agent.md says "Skip-pre-loading. Do not pre-load conditional references. Max 3 per task." Library-index.md says "Skip-pre-loading: Per design-doc §10.5, conditional reads happen only when the task surface requires them. Do not load 'just in case.'" Agent.md's terser form misses the "task surface requires" criterion — the agent.md form admits a literal reading where any conditional reference NOT in `library/` would not count under skip-pre-loading. Library-index.md is the authoritative form but only loads after agent.md per the catalog composition protocol step 2.
**Evidence.**
- agent.md:86 — "Skip-pre-loading. Do not pre-load conditional references. Max 3 per task."
- library-index.md:18 — fuller form.
- catalog.md:79-81 — composition protocol "1. Load identity core; 2. Instruct read of library-index" sequencing.
**Suggested fix.** None required for agent.md (the library-index is the canonical second-load). Note retained as ordering signal.

---

## Mechanical coverage results

| # | Check | Result | Evidence |
|---|---|---|---|
| M1 | 10 AGENT_TEMPLATE base sections + Modes present | PASS | Grep `^## ` against agent.md returns 11 H2s: Identity (5), Core Rules (11), Role Boundaries (26), Ask vs Proceed (34), Loop-Breaking (45), Tools (52), Communication (60), Context Loading (76), Modes (88), Anti-Patterns (98), Negative Examples (107). |
| M2 | Anti-sycophancy anchor ≤ line 20 | PASS | First anti-sycophancy clause at line 7 (Mechanism C anchor); first explicit "Do not begin a response with 'Great'..." at line 9. Both well within line ≤20 (NAACL primacy). |
| M3 | Negative Examples in last 30 lines | PASS | `## Negative Examples` header at line 107 of 119 total; offset 12 from EOF. Within last 30 lines (NAACL recency). |
| M4 | Line count ≤ 200 | PASS | `wc -l agent.md` = 119; hard max 200. |
| M5 | Token count ≤ 2,000 target | FAIL | `tiktoken cl100k_base` = 3,127; target ≤2,000. Overrun characterized below. |
| M6 | Library-index reference paths resolve | PASS (5/5) | (a) `.claude/skills/aplus-research/SKILL.md` — exists (36963 bytes). (b) `vault/WIKI.md` — exists (14067 bytes). (c) `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` — exists (4807 bytes). (d) `vault/decisions/` — exists (6 ADR files). (e) Regulatory primary text — abstract, no path to verify. |
| M7 | Auto-load paths resolve (agent.md §Context Loading) | PASS (4/4 + substrate) | `vault/meta/operator-profile.md` (4379 B), `vault/meta/current-state.md` (3412 B), `vault/meta/goals.md` (3881 B), `vault/library/_source-whitelist.md` (14201 B), substrate `design/.health-specialist-architect-design-work/domain-research.md` (91129 B). |
| M8 | Catalog row matches profile slot | PARTIAL | Profile name, path, identity core, primary use, pairs-with all align with agent.md. **Token Budget cell FAILS** — catalog says "~1,900 tokens"; actual 3,127. See F-A02. |
| M9 | Identity body behavioral lexicon (must\|never\|always\|refuse) | PASS | grep against `## Identity` body (lines 6-10): 0 matches for each. |
| M10 | Three-mechanism anti-sycophancy named (A, B, C) | PASS | "Mechanism C" / "Mechanism A" / "Mechanism B" all appear in line 7. Mappings: A → Role 4 Council-Mode; B → maintain-position; C → RLHF-drift anchor. |
| M11 | Anti-Patterns count 5-8 | PASS | 6 bullets at agent.md:100-105. |
| M12 | Loop-Breaking ≥3 thresholds with values | PASS | 4 bullets at agent.md:47-50 (Revision caps 2/3 / Context-scratch >5 / LIVE-tag cap 2 failures / Fabrication zero-tolerance). Note D7 9/10 requires 5 — see F-A04. |
| M13 | Communication: 3 audience formats | PASS | Orchestrator (line 62), Downstream specialists (line 72), User (line 74). Orchestrator format names 7 fields. |
| M14 | Role Boundaries: ≥6 owns + ≥6 not-owned with owner-role parenthetical | PASS | "I own" — 8 items at line 28. "I do NOT own" — 8 items at line 30, each with downstream owner in parens. |
| M15 | Anti-Patterns "I don't X" framing + ≥1 source citation each | PASS | All 6 bullets begin "I don't"; all 6 cite at least one of PF-S\d+-\d+ / Finding N. |
| M16 | Refusal-class identifiers all 8 named in agent.md | PASS | All 8 enumerated in Core Rule 10 (line 22). See F-A12 (anti-paraphrase nuance). |

---

## Token-budget characterization

**Headline.** Actual: 3,127 cl100k_base tokens. Target: ≤2,000 (per agent-rubric.md D2 9/10 pass). Catalog claims: ~1,900. **Overrun: +56% vs target, +64% vs catalog.**

### Load-bearing content (medical-domain-specific structural commitments — should NOT be compressed)

These categories carry information the medical-LLM specialist downstream cannot reconstruct from upstream references without losing safety properties:

1. **Three-mechanism anti-sycophancy mapping (line 7).** ~80 tokens. Mechanism A → Role 4 Council-Mode, Mechanism B → maintain-position, Mechanism C → RLHF-drift. The Sharma/Petri/Catfish/SycoEval-EM substrate cannot be regenerated from any compressed form. Load-bearing per F-S2 + design-doc §4 OUTBOUND row 4.
2. **8-class refusal taxonomy enumeration (Core Rule 10).** ~110 tokens. Each class is keyed to a statutory criterion downstream specialists rely on for `risk_tier` derivation. Removing the enum would force every consuming specialist to load Finding 5 verbatim from `domain-research.md` (91 KB substrate file).
3. **GRADE two-axis HALT clause (Core Rule 11).** ~75 tokens. Strong+low-certainty HALT condition with downgrade/raise/override-log alternatives. Removing the HALT branches admits the "single evidence rating" collapse that Finding 2 forbids.
4. **H-class composition rule (Core Rule 12).** ~75 tokens. `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)` with H1/H2 auto-block. The composition rule is the §4 OUTBOUND row 2 anchor; downstream specialists encode this verbatim in Loop-Breaking.
5. **Fabrication guard (Ask vs Proceed line 43).** ~50 tokens. Enumerates 6 fabrication surfaces (refusal-class identifier, GRADE tier, CONTINUATION_BRIEF §10 row, INV-* ID, PF-S\d+-\d+, vault/ path). Compressing would lose the surface coverage signal.
6. **Refusal taxonomy in Role Boundaries (line 28).** ~30 tokens — already compressed to "the 8-class refusal taxonomy" without identifier enum (the enum lives in Core Rule 10 once).
7. **Anti-Pattern citations + cues (lines 100-105).** ~250 tokens. Each cue line is the recognition pattern; the design doc §11.2 says cues are "more valuable than the cue label."

**Subtotal load-bearing.** ~670 tokens of the 3,127 are medical-domain-specific and resist further compression without losing safety properties.

### Candidate-for-further-compression content

These categories carry text that could be trimmed without losing the agent's load-bearing safety properties:

| Section | Current tokens (est.) | Compression candidate | Risk if trimmed |
|---|---|---|---|
| Core Rules (lines 11-25, 13 rules) | ~700 | Rules 1, 4, 5, 7, 9 carry voice/source tags and provenance citations. Tag set could compress: "[Finding N + R\d]" instead of "[Finding 1]" + "[INV-RESEARCH-ATTESTATION; INVARIANTS.md: 12 entries as of 2026-05-26]". Drop the "12 entries" volatile fact (F-A11). Save ~50 tokens. | Low — provenance preserved. |
| Tools section (lines 52-58) | ~340 | Permitted list verbose enumeration of paths could compress: "Read/Glob/Grep on substrate, role profiles, INVARIANTS.md, memory/process-failures.md, vault/WIKI.md, vault/meta/*, regulatory text" → "Read/Glob/Grep on Pass-1 substrate + project artifacts (no writes outside permitted-paths)." Save ~30 tokens. | Low if "permitted-paths" is defined elsewhere (it is, in Write/Edit clause). |
| Communication orchestrator section (lines 62-70, 7 fields) | ~190 | Field descriptions could compress one-line each. E.g. "Mechanical-check status — per LIVE/REFERENCED §13 row: exit code or `(not-run)`; PROPOSED = `(deferred per §18)`" → "Mechanical-check status — §13 row codes". Save ~40 tokens. | Medium — exit-code semantics are load-bearing for orchestrator parsing. Recommend NOT to compress. |
| Context Loading conditional list (line 84) | ~40 | Already compressed to a comma list ("aplus-research SKILL.md, vault/WIKI.md, AGENT_TEMPLATE.md + existing profiles, vault/decisions/, regulatory primary text"). No further compression. | N/A. |
| Modes section (lines 88-96) | ~120 | Rationale clause "Declared so role-tagged dispatches inlined by `enforce-role-inlining.sh` satisfy the 11-section expectation" could become a one-line note. Entry/Exit/Permitted-tools format is structural; keep. Save ~15 tokens. | Low. |
| Negative Examples (lines 107-119, 2 pairs) | ~340 | Already compressed from design-doc's 4 pairs to 2. Each pair is well-chosen (AP1 + AP3 — the highest-leverage failure modes). Could drop further to 1 pair, saving ~150 tokens, BUT D9 rubric requires ≥2 pairs. Hard floor. | High — would fail D9. |
| Anti-Patterns cues (in-line bracketed) | ~120 | Cues are the load-bearing content per design-doc §11.2 rationale. Trimming them flips the section to "label-only" which the rubric explicitly says fails. | High — do NOT trim. |

**Subtotal candidate-for-trim.** ~135 tokens of low-risk savings if all suggestions adopted.

### Section-by-section recommendation

| Section | Current | Recommended action |
|---|---|---|
| Header + Identity | 198 tokens | Keep. F-A07 is interpretive, not a defect. |
| Core Rules | ~700 | Trim ~50 via F-A11 fix + tag normalization. Target: ~650. |
| Role Boundaries | ~310 | Keep. Owns/not-owns are inheritance-load-bearing. |
| Ask vs Proceed | ~210 | Keep. Each branch is a decision-tree edge. |
| Loop-Breaking | ~210 | Split bundled bullet per F-A04 (+~15 tokens) → ~225. Net cost accepted to restore 5 thresholds. |
| Tools | ~340 | Trim ~30 via path-list compression. Target: ~310. |
| Communication | ~310 | Keep. Field semantics are orchestrator-binding. |
| Context Loading | ~270 | Fix F-A09 ambiguity (+5 tokens). Target: ~275. |
| Modes | ~120 | Trim ~15 via rationale compression. Target: ~105. |
| Anti-Patterns | ~370 | If F-A06 fix option (a) adopted: +~40 tokens. Target: ~410. |
| Negative Examples | ~340 | Keep. Rubric floor at 2 pairs. |

**Projected post-fix total.** ~3,127 + 40 (F-A06 AP7 addition) + 15 (F-A04 split) + 5 (F-A09 fix) − 50 (F-A11 normalize) − 30 (Tools compress) − 15 (Modes rationale) − 5 (F-A12 enum compress) = **~3,087 tokens** (net −40).

The structural overrun is **not removable to ≤2,000** without dropping load-bearing content (the 8-class enum, Mechanism A/B/C mapping, GRADE HALT, H-class composition, fabrication guard surface list, two Negative Example pairs). The agent.md is approximately **50% over the generic-target budget** by structural commitment to the medical-domain safety surface.

**Honest characterization.** This is not "scope creep" or "verbose drafting" — the medical-domain anchors are doing work no compressible form can replicate. The catalog row's "~1,900 token" claim was anticipatory; the synthesized profile fell ~60% over because every Pass-1 Finding (1-9) and every load-bearing OUTBOUND reference (§4 rows 1-7) had to land somewhere visible.

**Two paths forward (orchestrator decision).**
  (a) **Accept the budget.** Update catalog.md to `~3,100 tokens` with an in-row note "above generic budget by medical-domain structural commitment; see Phase-6 token-budget characterization." Adjust the per-task max-loaded-context guardrail upward for tasks routed to this role.
  (b) **Split the agent.** Move the 8-class refusal taxonomy enumeration + the H-class composition rule + the GRADE HALT clause to a sibling document (e.g., `roles/health-specialist-architect/medical-discipline-anchors.md`) and reference by path from agent.md. Saves ~250 tokens net but adds a second mandatory-read file, contradicting the catalog composition protocol (which assumes agent.md + library-index.md only). Net token cost across the dispatched context is unchanged; the cost is shifted but not eliminated.

Recommend (a). The medical-domain anchors are precisely what this role exists to encode; relocating them out of the identity core would be a category error.

---

## Notes

**Observations not promoted to findings.**

- **Hook order verification deferred.** F-A03 (Modes placement) recommends a move from line 88 to between Anti-Patterns and Negative Examples. The `enforce-role-inlining.sh` hook smoke tests (8/8 pass per INVARIANTS.md:41) were not re-run against the candidate post-fix order. The hook may or may not enforce section order. Recommend Phase 7 verify before applying the move.
- **`/upgrade-agent` downstream consumer.** Agent.md line 56 says "`/upgrade-agent` consumes my deliverable." This is true for the architect's design-doc artifact (873-line design doc that fed this synthesis). It is NOT true at the agent.md layer — `/upgrade-agent` consumed the design doc to produce the agent.md, not the other way around. Possible inversion that does not affect the dispatched agent's behavior but reads oddly to a reader unfamiliar with the pipeline. Not promoted because the consume-direction is unambiguous from CLAUDE.md skill description and design-doc downstream field.
- **library-index.md "Cross-reference pairs" clause is rich (line 19).** Lists three cross-reference clusters (aplus-research+WIKI for Tools+Context; AGENT_TEMPLATE+existing role for §3; regulatory+vault decisions for refusal-taxonomy). Strong as written; orchestrator can use this for ref selection. No finding — observation.
- **No personality-trap findings.** The 4th agent-specific criterion (personality adjectives encoding observable behaviors) returned zero hits. The agent.md is uniformly behavior-stated; lexicon scan yielded no "thoughtful / careful / detail-oriented / rigorous" — only conditions and verb commitments.
- **Operational completeness — most verbs map.** Sampled verbs: "dispatch" → Agent (Tools §54); "Glob/Read" → §54; "Write/Edit" → §54; "audit" → Bash audit-script invocation (§54); "escalate" → workflow named in §32 (write contract-violation finding to Phase-3 channel — but see F-A05 ambiguity); "log a contradiction" → workflow named in Core Rule 6 (vault/meta/contradictions.md). One borderline: "halt and resolve via branch 1 or 2" in fabrication guard (line 43) — workflow named but resolution path is conditional. Acceptable.
- **First-person voice mix.** Rubric D3 9/10 requires ≥2 first-person rules. Agent.md Core Rules count: Rule 5 ("Maintain my position...") is first-person. Other rules are imperative. The design doc §5 has two first-person rules (Rule 6 + Rule 10); the agent.md compresses these to one. Borderline against D3, but rubric D3 7/10 accepts "majority testable" without first-person count. Not promoted to finding.
- **Phase 4 validation reports not re-cross-checked.** This review accepted Phase-4 fact-checker + judge dispositions for R1/R2/R3 as-given. A finding that would surface there but not here is out of scope by construction — Phase 6 reviews the synthesized agent.md, not the validation pipeline.
