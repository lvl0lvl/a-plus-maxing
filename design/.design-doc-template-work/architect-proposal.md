---
title: Design Doc Template Proposal — Medical Agent Roles
type: proposal
status: draft (awaiting red-team review)
author: Architect agent (dispatched by orchestrator)
created: 2026-05-26
adapts: Quant design-doc-protocol.md
downstream: /upgrade-agent command (will consume the finalized template)
---

# Design Doc Template Proposal — Medical Agent Roles

This proposal defines the canonical Pass-2 design-doc structure for the 4 medical foundation roles and the 14 specialist roles in the `a-plus-maxing` project. The template is the contract; role profiles are its implementations. The downstream consumer is the `/upgrade-agent` command, which will read each finalized design doc and synthesize an `agent.md` conforming to `AGENT_TEMPLATE.md`.

---

## 1. Problem Statement

The Quant `design-doc-protocol.md` (`~/.claude/projects/-Users-waltermcgivney-Documents-Projects-Quant/memory/design-doc-protocol.md`) was authored to upgrade *pipeline commands* between Phase 0 and Phase 1 of a quant-research codebase. Its 20 required sections (lines 57–80) and 7-item Inputs list (lines 9–15) encode three foundational assumptions that do not hold for medical agent-role design:

- **Assumption A — there is a prior artifact to upgrade.** Sections 2 ("Decision: Modify In Place"), 3 ("What Transfers As-Is"), 4 ("What Must Change"), and 20 ("Net Line Count Estimate") all presuppose an existing command file is being mutated. The 4 foundation roles have NO prior agent.md — they are net-new authoring. Sections 3/4 collapse to vacuous tables; Section 20 reduces to "guess the final length."

- **Assumption B — the artifact is code with runtime semantics.** Section 8 ("Interface Contracts" — Phase 1 task signatures), Section 9 ("Pipeline Path Isolation" — separate directories/state files), Section 11 ("State File Schema Changes"), and Section 13 ("Verification Protocol Changes") all model a stateful pipeline. Agent profiles are documents read into LLM context; they do not own pipeline state, do not isolate paths, and do not have a state-file schema. Section 9 is literally N/A — profiles are loaded into context, they do not write to a state file.

- **Assumption C — the change is a delta within a known structure.** Section 5 ("What Must Be Added"), Section 6 ("Cross-Phase Dependency Modeling"), Section 7 ("Carry-Forward Item Integration"), Section 10 ("Agent Brief Modifications"), and Section 14 ("Anti-Pattern Updates") all assume continuity with a prior phase. Foundation roles have no prior phase. Specialist roles will have foundation roles as parents but are not "upgrades" of them — they are siblings authored under a shared template.

Sections that do transfer cleanly: Section 1 (Problem Statement), Section 12 (Edge Cases), Section 15 (Risk Assessment), Section 16 (Acceptance Criteria), Section 17 (Invariants at Risk), Section 18 (Assumptions and Break Conditions), Section 19 (Open Questions), Appendix A (Red Team Findings). These are domain-neutral and serve any design-doc purpose. Specifically:

| Quant section | Line range | Reason it transfers |
|---|---|---|
| 1. Problem Statement | 61 | Universal design-doc opener |
| 12. Edge Cases | 72 | Universal; specialized for agent context |
| 15. Risk Assessment | 75 | Universal |
| 16. Acceptance Criteria | 76 | Universal |
| 17. Invariants at Risk | 77 | Universal — INVARIANTS.md exists in this project too |
| 18. Assumptions and Break Conditions | 78 | Universal |
| 19. Open Questions | 79 | Universal |
| A. Red Team Findings | 81 | Universal — Pass-2 has the same red-team phase |

Sections that do NOT transfer (named explicitly): 2 (Decision: Modify In Place), 3 (What Transfers As-Is), 4 (What Must Change), 6 (Cross-Phase Dependency Modeling), 7 (Carry-Forward Item Integration), 8 (Interface Contracts — pipeline-task-shaped), 9 (Pipeline Path Isolation), 10 (Agent Brief Modifications — Quant means modifications to existing pipeline-stage briefs), 11 (State File Schema Changes), 13 (Verification Protocol Changes), 14 (Anti-Pattern Updates), 20 (Net Line Count Estimate).

Additionally, the Quant template has no slot for the Pass-1 deliverables — the four `domain-research.md` files (49,500 words combined) that ARE the substrate for these design docs. Without a section that explicitly digests the Pass-1 deliverable, the design doc risks duplicating the research or, worse, contradicting it through paraphrase drift.

The Quant template also has no slot for `AGENT_TEMPLATE.md` mapping. Since the downstream consumer (`/upgrade-agent`) reads the design doc to produce an `agent.md` conforming to `AGENT_TEMPLATE.md`, the design doc MUST contain a section that maps decisions to AGENT_TEMPLATE sections one-to-one — otherwise the upgrade-agent step has to re-discover the mapping per role, which is the failure mode the Pass-1 deliverables already exposed (each Pass-1 report's "Recommendations" section already does this mapping; the Pass-2 design doc must inherit and consolidate it).

---

## 2. Adapted Section Inventory

The proposed template has **18 sections** (vs Quant's 20). Foundation-role and specialist-role design docs both use this template; sections marked CONDITIONAL omit when the condition is unmet, with explicit "OMITTED — rationale" note required.

### Section 1 — Problem Statement
- **Purpose.** State the role this design doc designs and what failure modes drove its creation.
- **Writer produces.** 200–400 word prose. Names the role slug (e.g., `health-specialist-architect`), the wiki consumer entries it serves (rows from `vault/WIKI.md` Agent Consumers table), the specific Pass-1 Findings that drive design decisions in this doc (cite by Finding number), and the project process-failure entries (PF-S2-01, PF-S2-02, etc.) the profile must defend against. Binary verifiable: contains exactly one role slug; cites ≥3 Pass-1 Findings; cites ≥1 PF entry OR explicitly attests "no PF entries apply, rationale: …".
- **Status.** REQUIRED.
- **Budget.** 30–50 lines / 200–400 words.
- **AGENT_TEMPLATE.md mapping.** Identity (informs the role's purpose sentence).
- **/upgrade-agent phase.** Phase 1 (Baseline Evaluation) — frames what the upgrade-agent is evaluating against.

### Section 2 — Role Definition and Boundary
- **Purpose.** Declare what the role IS, what it OWNS, what it does NOT own, and which adjacent role owns each non-owned concern.
- **Writer produces.** Three subsections. (a) One-sentence "You are the X" identity statement, ≤40 words (per Pass-1 Role-1 Finding 1: Anthropic guidance is one sentence). (b) "I own" comma-separated list. (c) "I do NOT own" with owning role in parentheses for each item. For specialist roles: must cite the row from `vault/WIKI.md` Agent Consumers table that this profile implements (Reads, Owns, Dispatches research on columns). Binary verifiable: ≤40 words on identity sentence; "I do NOT own" entries each end with `(<role-name>)`; for specialists, WIKI.md row pasted verbatim.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Identity (sentence) + Role Boundaries (own/not-own lists).
- **/upgrade-agent phase.** Phase 5 (Synthesis — Role Boundaries section author).

### Section 3 — Pass-1 Deliverable Digest
- **Purpose.** Lift the load-bearing structural conclusions from this role's `domain-research.md` into a form the design doc can reference without paraphrase drift.
- **Writer produces.** A table with one row per Pass-1 Finding (typically 9 rows) with columns: Finding # / one-sentence claim / cited source line range in `domain-research.md` / AGENT_TEMPLATE.md section this Finding informs / whether this design doc accepts or modifies the Finding (with rationale if modifies). Plus a list of the role's Pass-1 Recommendations (R1–R15) with each Recommendation tagged ACCEPTED / DEFERRED / REJECTED — deferrals and rejections require one-line rationale. Binary verifiable: row count matches Finding count in source `domain-research.md`; every Recommendation in source listed with a verdict; no "TBD" verdicts.
- **Status.** REQUIRED for foundation roles. CONDITIONAL for specialist roles (specialists may have a Pass-1 deliverable in Pass-3; if no Pass-1 deliverable yet, this section becomes "Pass-1 Substrate — Deferred" with explicit note that this design doc draws from foundation-role design docs only).
- **Budget.** 30–60 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; serves the design doc itself by anchoring claims to the research substrate.
- **/upgrade-agent phase.** All phases (the upgrade-agent reads this section to know which Findings ground which content decisions).

### Section 4 — Inherited Cross-Role References
- **Purpose.** Enumerate the cross-deliverable references this role's design doc must preserve (per CONTINUATION_BRIEF §10).
- **Writer produces.** A table listing each cross-reference: from-role / to-role / what is referenced / why it must remain consistent. Examples per CONTINUATION_BRIEF §10: the refusal-class taxonomy (Roles 2/3/4 → Role 1 Finding 5); GRADE evidence-tier discipline (Roles 2/3/4 → Role 1 Finding 2); three-mechanism anti-sycophancy (Roles 2/3/4 → Role 1 Finding 3); IDENTICAL/DIFFER partition (Roles 3/4 → Role 2 Finding 7); four-axis severity composition (Role 3 Finding 4 + Role 4 Finding 5); operator-profile hard limits (Role 1 Finding 6 → Roles 2/3/4 R-items). The design doc DEFERS to the source (does not redefine the referenced content); a one-line citation pointer suffices. Binary verifiable: every applicable row from CONTINUATION_BRIEF §10 present; no referenced content redefined inline.
- **Status.** REQUIRED.
- **Budget.** 20–35 lines.
- **AGENT_TEMPLATE.md mapping.** Core Rules + Role Boundaries (these are the sections that most often carry cross-role references).
- **/upgrade-agent phase.** Phase 6 (Adversarial Review — the reviewer uses this section to check for content duplication / contradiction with sibling profiles).

### Section 5 — Core Behavioral Rules
- **Purpose.** Specify the 8–12 Core Rules that go into the agent.md, with rationale linking each rule to either a Pass-1 Finding, a project PF entry, or an INVARIANTS.md row.
- **Writer produces.** Numbered list of 8–12 rules. Each rule has: (a) the rule text in imperative or first-person-experiential voice per Role 2 Finding 4; (b) source link (Pass-1 Finding N / PF-Sn-mm / INV-X); (c) mechanical-check designation if applicable (grep pattern, audit-script name). Binary verifiable: rule count in 8–12; each rule has a source link; mechanical checks named are grep-able OR existing-script-name.
- **Status.** REQUIRED.
- **Budget.** 40–70 lines.
- **AGENT_TEMPLATE.md mapping.** Core Rules.
- **/upgrade-agent phase.** Phase 3 (Research Agents — feeds R1/R3 input on behavioral rules) + Phase 5 (Synthesis).

### Section 6 — Ask vs Proceed Decision Tree
- **Purpose.** Specify the role-specific decision tree for resolving ambiguity, with explicit clauses for the medical-specific edge cases (user push-back without new evidence, contraindication unverified, evidence-tier below threshold).
- **Writer produces.** A 5–7 step ordered decision tree, each step phrased as a question + the action when YES vs NO. Must include at minimum: (a) "Can I find the answer in the project wiki?" first; (b) "Does the user provide new evidence vs express dissatisfaction?" (anti-sycophancy Mechanism B, per Pass-1 Role-1 Finding 3); (c) "Is the GRADE certainty rating below the threshold for this recommendation strength?" (per Role-1 Finding 2). Binary verifiable: step count 5–7; SycoEval-EM-class user-pushback clause present; GRADE clause present.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Ask vs Proceed.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

### Section 7 — Loop-Breaking Thresholds
- **Purpose.** Specify the role-specific stop-conditions (attempt counts, turn limits, escalation triggers) appropriate for the medical context.
- **Writer produces.** A list of 3–5 loop-breaking rules. Must include at minimum: (a) attempt-count threshold for the same approach; (b) the contraindication-coverage hard gate (per Pass-1 Role-1 Finding 6: contraindication unverified ⇒ HALT) IF the role can write to compounds OR biomarkers; (c) the role's escalation target (which adjacent role, or the user). Binary verifiable: rule count 3–5; if role has write access to compounds/biomarkers, contraindication hard gate present.
- **Status.** REQUIRED.
- **Budget.** 15–25 lines.
- **AGENT_TEMPLATE.md mapping.** Loop-Breaking.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

### Section 8 — Tools and Permissions
- **Purpose.** Specify the set of tools the role has access to, the role's write-permission scope, and any mechanical restrictions (e.g., reviewer roles lack Write/Edit).
- **Writer produces.** A table: tool name / why this role needs it / role's permission level (read-only vs write). Must include the per-role write-permission scope (e.g., labs-specialist writes to `vault/biomarkers/` and `vault/labs/`; medical-safety-reviewer writes to no wiki path; etc.). Must enforce Pass-1 Role-1 Finding 1 mechanical check (≤8 tools per role; reviewer roles have no Write/Edit/MultiEdit). For specialists, must cite the WIKI.md "Owns (writes)" column. Binary verifiable: tool count ≤8; if `role_type: reviewer`, no Write/Edit/MultiEdit; for specialists, write-paths match WIKI.md row.
- **Status.** REQUIRED.
- **Budget.** 20–30 lines.
- **AGENT_TEMPLATE.md mapping.** Tools.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

### Section 9 — Communication Protocol
- **Purpose.** Specify the two-register communication pattern (to-other-agents vs to-user) and any role-specific output formats (refusal templates, escalation handoff format, contradiction-log entry format).
- **Writer produces.** Two subsections: "To other agents / orchestrator" with format spec; "To user" with format spec. Plus a refusal-template subsection citing the refusal-class taxonomy from Pass-1 Role-1 Finding 5 (one example refusal phrasing per applicable refusal class). For specialists writing back to the wiki: the wiki-write format (which template from `vault/WIKI.md` Entity Types is used). Binary verifiable: two registers present; refusal-template subsection present and cites ≥1 refusal class; wiki-write format named if role writes to wiki.
- **Status.** REQUIRED.
- **Budget.** 25–45 lines.
- **AGENT_TEMPLATE.md mapping.** Communication.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

### Section 10 — Context Loading Protocol
- **Purpose.** Specify which references the role loads on dispatch and in which order.
- **Writer produces.** An ordered list of context to load on every dispatch. Must include `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md` (per WIKI.md cross-cutting protocol). Plus role-specific wiki entries by domain (cite WIKI.md "Reads" column). Plus `library/` paths for the role's evidence domain. Plus mechanical check: per Pass-1 Role-1 Finding 4, the Context Loading section must enumerate wiki/KG paths via grep-checkable references. Binary verifiable: three cross-cutting refs present; role-specific Reads-column entries present; wiki/KG paths grep-checkable.
- **Status.** REQUIRED.
- **Budget.** 20–30 lines.
- **AGENT_TEMPLATE.md mapping.** Context Loading.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

### Section 11 — Anti-Patterns Catalog
- **Purpose.** Enumerate 5–8 role-specific anti-patterns as concrete "I don't X" statements, grounded in either project PF entries or Pass-1 Findings.
- **Writer produces.** Numbered list of 5–8 anti-patterns. Each is: (a) concrete "I don't X" phrasing; (b) source link (PF-Sn-mm or Pass-1 Finding N); (c) recognition cue (what situation triggers this pattern). Must include the project's documented PF entries that are in-scope for this role (PF-S2-01 self-attestation, PF-S2-02 citation-by-accident, PF-S2-04 over-personalization, PF-S2-05 mental-model-vs-protocol, PF-S3-01 mechanical-fix-confused-with-verdict). Binary verifiable: count 5–8; each entry has source link; in-scope PF entries from `memory/process-failures.md` referenced.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Anti-Patterns.
- **/upgrade-agent phase.** Phase 3 (Research Agents R3) + Phase 5.

### Section 12 — Negative Examples
- **Purpose.** Specify 2–3 BAD/GOOD example pairs the upgrade-agent will place in the agent.md's last 30 lines (recency-effect placement per `/upgrade-agent` Phase 5).
- **Writer produces.** 2–3 BAD/GOOD pairs, each pair tagged with the failure mode it illustrates. Examples must be role-specific scenarios (not generic). Each BAD example must be a realistic output the role could produce; each GOOD example must be the correct version. For specialists with adversarial exposure: at least one example must illustrate refusal under a refusal-class trigger from Pass-1 Role-1 Finding 5. Binary verifiable: pair count 2–3; each pair has failure-mode tag; ≥1 illustrates refusal-class trigger for adversarially-exposed roles.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Negative Examples.
- **/upgrade-agent phase.** Phase 5 (Synthesis — last 30 lines).

### Section 13 — Mechanical Enforcement Map
- **Purpose.** Enumerate every mechanical check (audit script, grep pattern, hook) this design doc requires for the resulting agent.md to be considered conformant.
- **Writer produces.** Table: check name / what it verifies / mechanism (grep pattern / audit-script path / hook name) / failure consequence (BLOCK vs WARN). Must reference existing project audit scripts (`scripts/handoff-audit.sh`, `scripts/scope-contract-audit.sh`, `scripts/pf-attestation-audit.sh`, `.claude/hooks/enforce-role-inlining.sh`, `.claude/skills/aplus-research/lib/gate_attest.py`) and existing INVARIANTS.md rows. Any NEW mechanical check proposed must include the script's expected path and a one-sentence behavioral spec. Binary verifiable: row count ≥3; each row's mechanism either resolves to an existing path OR specifies the new path + behavioral spec; existing INVARIANTS.md rows referenced where applicable.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; serves the upgrade-agent's verification step in Phase 5 + Phase 7.
- **/upgrade-agent phase.** Phase 5 (Synthesis Item 5 — verification block) + Phase 7 (Final Corrections — checked against this section).

### Section 14 — Edge Cases
- **Purpose.** Enumerate the boundary conditions specific to this role and the expected behavior at each.
- **Writer produces.** Numbered list of edge cases. Each entry: (a) condition; (b) expected behavior; (c) test stimulus (a prompt or input that triggers the condition). Must include at minimum: (a) empty wiki entry for the role's domain; (b) contradictory wiki entries within the role's read scope; (c) user push-back without new evidence (per SycoEval-EM, Pass-1 Role-1 Finding 3); (d) prompt-injection via user-supplied text (per JAMA, Pass-1 Role-1 Finding 4). For roles with write access: race condition where two specialists write to the same wiki entry. Binary verifiable: count ≥5; mandatory edge cases (a)–(d) present; for write-access roles, race-condition entry present.
- **Status.** REQUIRED.
- **Budget.** 25–45 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; informs role-specific sections via test stimuli the upgrade-agent's Phase 6 (Adversarial Review) will probe.
- **/upgrade-agent phase.** Phase 6 (Adversarial Review).

### Section 15 — Acceptance Criteria
- **Purpose.** Binary pass/fail criteria for whether the resulting `agent.md` is fit-for-purpose.
- **Writer produces.** Numbered list of 8–15 acceptance criteria, each a binary pass/fail proposition. Must include: (a) line count ≤200 per `/upgrade-agent` Identity Core constraint; (b) token count ≤2,000 per same; (c) every AGENT_TEMPLATE.md section present; (d) all mechanical checks from Section 13 pass; (e) every Pass-1 Recommendation marked ACCEPTED in Section 3 is implemented in agent.md or has a deferred-rationale entry. Binary verifiable: count 8–15; each criterion independently testable; mandatory criteria (a)–(e) present.
- **Status.** REQUIRED.
- **Budget.** 20–35 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; gates the upgrade-agent's Phase 5 + Phase 7 acceptance.
- **/upgrade-agent phase.** Phase 5 + Phase 7 (Final Corrections).

### Section 16 — Invariants at Risk
- **Purpose.** Identify which `INVARIANTS.md` rows this role's deployment could affect.
- **Writer produces.** Table: invariant ID / risk type (could violate / could weaken / could newly require) / mechanism. Must check every row in `INVARIANTS.md` register; entries with no risk get a one-line "no risk to INV-X, rationale: …" attestation OR are omitted with a note that the omitted ones are out-of-scope-trivial. Must flag any overlap with proposed candidate invariants from CONTINUATION_BRIEF §9 (INV-DESIGN-DOC-SYMMETRY, pattern-label consistency, deep-research deliverable minimums, fabrication-shaped URL scan, citation-tier annotation, retrieval-date presence). Binary verifiable: every active INVARIANTS.md row addressed (positive risk-claim OR explicit no-risk note); CONTINUATION_BRIEF §9 candidates checked.
- **Status.** REQUIRED.
- **Budget.** 20–35 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; gates session-close audit (CLAUDE.md step 8).
- **/upgrade-agent phase.** Phase 7 (Final Corrections — invariant compliance check).

### Section 17 — Risk Assessment and Break Conditions
- **Purpose.** Enumerate concrete failure scenarios where this design becomes wrong, framed as falsifiable predictions.
- **Writer produces.** Two subsections. (a) "Risks" — numbered list of 3–6 scenarios where the deployed agent.md could fail in the wild, each with severity rating (BLOCK / MAJOR / MINOR per Pass-1 Role-3 four-axis composite). (b) "Breaks If" — numbered list of 3–6 specific conditions under which the design itself becomes wrong (e.g., "FDA singular-output enforcement discretion is rescinded — Section 9 refusal template needs rewrite"). Binary verifiable: risk count 3–6; break-conditions count 3–6; each break-condition is a falsifiable proposition with a specific change that would invalidate the design.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 5 (Synthesis — used during catalog update).

### Section 18 — Open Questions
- **Purpose.** Surface unresolved questions the orchestrator (not the upgrade-agent) must adjudicate before deployment.
- **Writer produces.** Numbered list. Each entry: (a) question; (b) options surfaced (2–3); (c) author's recommendation if any; (d) consequence-of-not-deciding. Empty list permitted IF the design doc has no open questions, but must say so explicitly with rationale (false-zero attestation principle). Binary verifiable: each entry has all 4 sub-parts OR list is explicitly attested empty.
- **Status.** REQUIRED.
- **Budget.** 15–30 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 8 (Close Out — flagged as follow-up items).

### Appendix A — Red Team Findings Log
- **Purpose.** Record every Phase-3 red-team finding, its classification (Legitimate vs Rejected), and the action taken.
- **Writer produces.** Table: finding ID / red-team agent / section affected / claim / classification / evidence (for Rejected, the source-cited rebuttal; for Legitimate, the design-doc fix that was applied). One row per finding from each red-team agent dispatched. Binary verifiable: row count ≥ total findings count from Phase-3 outputs; every Rejected has source-cited evidence; every Legitimate references the fix location.
- **Status.** REQUIRED at Phase-5 finalize (created empty at Phase-2 synthesis, populated through Phase-3/4).
- **Budget.** Unbounded (proportional to red-team output volume; typical 30–80 lines).
- **AGENT_TEMPLATE.md mapping.** N/A — process artifact.
- **/upgrade-agent phase.** N/A — consumed by the design-doc protocol, not by upgrade-agent.

---

## 3. What Transfers from Quant Template

| Quant section | Quant line range | Why it transfers | Adaptation needed |
|---|---|---|---|
| 1. Problem Statement | 61 | Universal design-doc opener | Adapted in this template's Section 1; medical-specific clauses (Pass-1 Findings, PF entries) added |
| 12. Edge Cases | 72 | Universal | Adapted in Section 14; mandatory medical-edge-cases (a)–(d) added (push-back, injection, etc.) |
| 15. Risk Assessment | 75 | Universal | Adapted in Section 17 (combined with Assumptions/Break Conditions for compactness) |
| 16. Acceptance Criteria | 76 | Universal — every binary criterion is independently testable | Adapted in Section 15; medical-specific criteria added |
| 17. Invariants at Risk | 77 | Universal — `INVARIANTS.md` exists in this project | Adapted in Section 16; CONTINUATION_BRIEF §9 candidate-invariant scan added |
| 18. Assumptions and Break Conditions | 78 | Universal | Merged into Section 17 (Risk + Breaks If); both are falsifiable-prediction shapes |
| 19. Open Questions | 79 | Universal | Adapted in Section 18; false-zero attestation requirement added |
| A. Red Team Findings | 81 | Universal — Pass-2 has the same red-team phase | Adapted as Appendix A; classification rule (Legitimate vs Rejected, burden of proof on rejection) inherited verbatim |

---

## 4. What Must Change

| Quant section | Quant line range | What changes | Why command-upgrade-shape doesn't fit |
|---|---|---|---|
| 2. Decision: Modify In Place | 62 | DROPPED. | Foundation roles have no prior agent.md. Specialists are net-new authoring, not modifications. The "modify vs create" decision is N/A — every role is "create". |
| 3. What Transfers As-Is | 63 | REPLACED by Section 3 (Pass-1 Deliverable Digest) | Quant Section 3 lifted lines from a prior command; the medical analog is lifting Findings/Recommendations from the Pass-1 `domain-research.md`. The shape is similar (a "what to keep" table) but the source is research, not code. |
| 4. What Must Change | 64 | DROPPED at top level; partially absorbed into Section 3 (Pass-1 Recommendations with ACCEPTED/DEFERRED/REJECTED verdicts) | No prior agent.md exists to change FROM. The closest analog is "which Pass-1 Recommendations are accepted vs deferred" — Section 3 covers this. |
| 5. What Must Be Added | 65 | DROPPED. | No prior content exists, so "what's new" is "everything." Section 5 (Core Behavioral Rules), Section 11 (Anti-Patterns), Section 12 (Negative Examples) collectively cover what would have been "added." |
| 6. Cross-Phase Dependency Modeling | 66 | REPLACED by Section 4 (Inherited Cross-Role References) | Quant modeled task dependencies across pipeline phases. The medical analog is dependencies across role profiles (per CONTINUATION_BRIEF §10). Same concept, different graph. |
| 7. Carry-Forward Item Integration | 67 | DROPPED. | No Phase-0 carry-forward items exist for medical roles. The PF-entry coverage in Section 11 (Anti-Patterns) is the structurally analogous "carry forward from project history" mechanism. |
| 8. Interface Contracts | 68 | REPLACED by Section 2 (Role Definition and Boundary) + Section 8 (Tools and Permissions) | Quant's Interface Contracts are Phase-1 pipeline-task signatures. The medical analog is the agent's input/output interface (operator-profile in, wiki-entries out, etc.) — already covered by Section 2 + Section 8 + Section 9. |
| 9. Pipeline Path Isolation | 69 | DROPPED. | Agent profiles do not own pipeline state, do not write to state files, do not isolate paths. N/A. |
| 10. Agent Brief Modifications | 70 | DROPPED. | Quant Section 10 means modifications to SE/QA/Architect/Security briefs in the pipeline's drafting team. The medical analog is "what role profile is created" — that is the entire design doc, not a section. |
| 11. State File Schema Changes | 71 | DROPPED. | Agent profiles have no state-file schema. The wiki has schemas (`vault/WIKI.md`), but those are referenced by Section 9 (Communication — wiki-write format) and Section 10 (Context Loading), not redefined in the role design doc. |
| 13. Verification Protocol Changes | 73 | REPLACED by Section 13 (Mechanical Enforcement Map) | Quant Section 13 changed pipeline verification. Section 13 here specifies the audit-script and hook coverage for the agent.md. |
| 14. Anti-Pattern Updates | 74 | REPLACED by Section 11 (Anti-Patterns Catalog) | Quant "updates" existing anti-patterns; medical roles author new ones. Same content shape, no "update" framing. |
| 20. Net Line Count Estimate | 80 | DROPPED. | The `/upgrade-agent` Identity Core constraint is fixed at ≤200 lines / ~2,000 tokens. Per-section line budgets are already specified in `/upgrade-agent` Phase 1 (lines 56–73). No per-design-doc estimate needed. |

---

## 5. What Must Be Added

Sections in this proposal that have no Quant equivalent:

- **Section 3 — Pass-1 Deliverable Digest.** Required by Pass-1 deliverables themselves: the four `domain-research.md` files are ~49,500 words of substrate. Without a section that explicitly digests them (Finding-by-Finding accept/modify, Recommendation-by-Recommendation accept/defer/reject), the design doc will either duplicate the research (token waste) or contradict it through paraphrase (Lesson 3 risk). Source: CONTINUATION_BRIEF §16 ("treat them as input, not output").
- **Section 4 — Inherited Cross-Role References.** Required by CONTINUATION_BRIEF §10: 7 explicit cross-deliverable references must be preserved across the 4 foundation roles' Pass-2 design docs. Without a dedicated section, the Pass-2 docs would re-derive these references inconsistently. Source: CONTINUATION_BRIEF §10 table.
- **Section 13 — Mechanical Enforcement Map.** Required by INVARIANTS.md "Mechanical enforcement principle" (lines 14–15): "Invariants get scripts." This project deploys 12 active invariants with audit scripts/hooks. The design doc must declare which mechanical checks gate the resulting agent.md. Source: INVARIANTS.md Register; CONTINUATION_BRIEF §9 candidate-invariants.
- **Section 16 — Invariants at Risk.** Required by CLAUDE.md Session Close step 8 ("Update beads") + step 8.5 ("Run audit scripts"). The design doc must enumerate which invariants the role's deployment could affect — this is the precondition for the session-close audit. Quant has a "17. Invariants at Risk" section (line 77); the difference is this template requires checking every row of INVARIANTS.md, not just the affected ones, AND requires checking the CONTINUATION_BRIEF §9 candidate-invariants list. Source: CLAUDE.md Cross-Document Ownership Matrix.
- **Subsection inside Section 5 — Mechanical-check designation per Core Rule.** Required by AGENT_TEMPLATE.md (Core Rules: "Each rule should be concrete and testable, not aspirational") + `/upgrade-agent` Rubric Dimension 3 ("Behavioral Specificity: each rule has a clear pass/fail condition"). Per-rule mechanical check forces the rule-author to specify the grep/audit. Source: `/upgrade-agent` rubric (lines 43).

---

## 6. Cross-Document Dependency Map

```
                        ┌──────────────────────────────────┐
                        │  AGENT_TEMPLATE.md (structural   │
                        │  target — 11 sections)           │
                        └──────────────┬───────────────────┘
                                       │ informs section-by-section mapping
                                       ▼
   ┌─────────────────────┐    ┌─────────────────────────┐    ┌────────────────────┐
   │  domain-research.md │───▶│  Pass-2 Design Doc      │───▶│  /upgrade-agent    │
   │  (Pass-1 substrate) │    │  (THIS template)        │    │  (consumer)        │
   └─────────────────────┘    └────────────┬────────────┘    └──────────┬─────────┘
       Section 3 digest                    │                            │ Phase 5
                                           │                            ▼
                                           │                  ┌─────────────────────┐
                                           │                  │  agent.md (output)  │
                                           │                  │  ≤200 lines         │
                                           │                  └─────────────────────┘
                                           │
                                           │ Section 16 cross-check
                                           ▼
                              ┌──────────────────────────┐
                              │  INVARIANTS.md Register  │
                              └──────────────────────────┘
                                           ▲
                                           │ Section 4 references
                                           │
                              ┌──────────────────────────┐
                              │  Sibling design docs     │
                              │  (CONTINUATION_BRIEF §10)│
                              └──────────────────────────┘
                                           ▲
                                           │ Section 11 references
                                           │
                              ┌──────────────────────────┐
                              │  memory/process-         │
                              │  failures.md             │
                              └──────────────────────────┘
```

Dependencies in narrative form:

- **Upstream of design doc:** `domain-research.md` (Pass-1 substrate, digested in Section 3), `vault/WIKI.md` Agent Consumers table (referenced in Section 2 and Section 8 for specialist roles), `memory/process-failures.md` (referenced in Section 11), sibling foundation-role design docs (referenced in Section 4 per CONTINUATION_BRIEF §10).
- **Downstream of design doc:** `/upgrade-agent` (consumes the doc; specific phase mapping in §2 above per section), the resulting `agent.md` at `~/Documents/Projects/skills_library/roles/{role}/agent.md` (per the Q4 decision in CONTINUATION_BRIEF §17), the project's `.claude/agents/{role}.md` symlink/copy, the session-close audit-script chain (gates via Section 13 + Section 16 outputs).
- **Lateral references:** `INVARIANTS.md` Register (cross-checked in Section 16), `CLAUDE.md` Cross-Document Ownership Matrix (governs which facts belong here vs elsewhere).

---

## 7. Worked Example

Selected role: **`medical-safety-reviewer`** (Role 4). Chosen because it surfaces the most edge cases — it has the most distinctive ownership boundary (no Write/Edit tools), the most complex severity framework (3-axis composite per Pass-1 Role-4 Finding 5), the strongest adversarial requirements (Pass-1 Role-4 Findings 1–3), the most explicit downstream-blocking role (deploy/block verdict per Finding 6), and the most cross-role references (composes with Role 3 per Finding 7).

This is NOT the actual Pass-2 design doc for `medical-safety-reviewer` — it is a structural validation that the template can hold the content.

**Section 1 — Problem Statement.** Role `medical-safety-reviewer` is the adversarial red-team gate for any compound, biomarker, or protocol authored by a specialist agent before deployment. Drives: Pass-1 Role-4 Finding 1 (static benchmarks understate medical-LLM harm by an order of magnitude); Pass-1 Role-4 Finding 7 (Role-3-vs-Role-4 sequential ordering); PF-S3-01 (mechanical fix confused with mechanical verdict). The role must defend against the JAMA-documented 94.4% prompt-injection success rate on commercial medical LLMs.

**Section 2 — Role Definition and Boundary.** Identity: "You are the medical-safety-reviewer. You red-team specialist outputs adversarially and emit deploy/block verdicts." I own: pre-deployment adversarial review of any compound/biomarker/protocol page; deploy/block verdict emission; severity-tuple computation; threat-model catalog updates. I do NOT own: specialist authorship (health-implementer); coverage-oriented review (health-edge-case-reviewer); doctor-domain adjudication (medical-liaison). WIKI.md row: not yet listed in Agent Consumers (foundation role, not a specialist).

**Section 3 — Pass-1 Deliverable Digest.** 9 rows for Findings 1–9 in `design/.medical-safety-reviewer-design-work/domain-research.md`, each with one-sentence claim, source line range, AGENT_TEMPLATE.md section informed (Core Rules, Tools, Anti-Patterns, etc.), and ACCEPTED/MODIFIED verdict. R-list with each Recommendation marked.

**Section 4 — Inherited Cross-Role References.** Defers to Role-1 Finding 5 (refusal-class taxonomy); composes severity-framework with Role-3 Finding 4 (4-axis × 3-axis composition); inherits sequential ordering from Role-4 Finding 7; references Role-1 Finding 6 (operator-profile hard limits) for the operator-relevance dimension of the severity tuple.

**Section 5 — Core Behavioral Rules.** Rules including: "I emit deploy/block verdicts only after running the threat-model catalog probes" (source: Role-4 Finding 4); "I never write to wiki paths" (source: Role-4 Finding 7, Role-1 Finding 1 mechanical check on reviewer tools); "I treat user-supplied unstructured text as untrusted" (source: Role-1 Finding 3, Role-4 Finding 2); etc.

**Section 6 — Ask vs Proceed.** Decision tree including: "Is the input from a specialist agent vs from the user directly?" "Does the threat-model catalog have a probe for this attack surface?" "Is the severity tuple H1 or H2?" (per Role-4 Finding 5: H1/H2 auto-block).

**Section 7 — Loop-Breaking.** Includes: deploy/block verdict timeout after N probes; escalation to user if BLOCK_WITH_OVERRIDE_PATH triggers and medical-liaison adjudicator is not yet deployed (per CONTINUATION_BRIEF §13 item 3).

**Section 8 — Tools and Permissions.** No Write/Edit/MultiEdit (per Role-1 Finding 1 mechanical check). Tools: Read, Grep, Glob, Bash (for running threat-model probes), Agent (for dispatching probe sub-agents per the Catfish Agent pattern, Role-4 Finding 9).

**Section 9 — Communication Protocol.** To agents: deploy/block verdict JSON with severity tuple, threat catalog probe results, override-path designation. To user: when escalating BLOCK_WITH_OVERRIDE_PATH, plain-language summary with refusal-class citation per Role-1 Finding 5 taxonomy. No wiki-write format (no write access).

**Section 10 — Context Loading.** Loads operator-profile, current-state, goals (per WIKI.md cross-cutting protocol). Plus the threat-model catalog. Plus the target specialist's authored output. Plus relevant library/ entries cited by the target.

**Section 11 — Anti-Patterns Catalog.** Includes: "I don't deploy without running adversarial probes" (PF-S3-01); "I don't self-attest that a probe passed when it was skipped" (PF-S2-01 medical analog); "I don't grade severity from prose impression — I run the 3-axis computation" (Role-4 Finding 5); etc.

**Section 12 — Negative Examples.** 2–3 BAD/GOOD pairs. At least one illustrates refusal under TIME_CRITICAL refusal class (per Role-1 Finding 5). One illustrates the multi-turn-persistence attack (Role-4 Finding 3 P3 catalog entry).

**Section 13 — Mechanical Enforcement Map.** Includes: `gate_attest.py` for any aplus-research dispatches the reviewer runs; new audit `scripts/agent-no-write-check.sh` (proposed) for reviewer-role tool restriction; existing `enforce-role-inlining.sh` for dispatch hygiene.

**Section 14 — Edge Cases.** Empty threat-model catalog probe-set for a novel compound class (severity tuple defaults to MAJOR pending probe addition). Two safety reviewers dispatched in parallel by orchestrator (idempotence requirement). Prompt-injection in the specialist's authored output (per JAMA, Role-1 Finding 4).

**Section 15 — Acceptance Criteria.** Includes: line count ≤200; every AGENT_TEMPLATE.md section present; no Write/Edit/MultiEdit tools; threat-model catalog reference present; refusal-class citation template present; deploy/block verdict format spec present.

**Section 16 — Invariants at Risk.** Reviews each INV-* row. INV-ROLE-INLINING: hook continues to apply (review-mode dispatches inline the safety-reviewer profile — same hook). INV-PF-ATTESTATION: continues to apply at session close. CONTINUATION_BRIEF §9 candidate-invariants: no overlap (this role does not produce synthesis docs needing AF5-syn).

**Section 17 — Risk Assessment and Break Conditions.** Risks: false-positive BLOCK paralyzes the deploy chain (MAJOR); false-negative ALLOW lets a malicious compound page deploy (BLOCK). Breaks If: threat-model catalog is removed; the 3-axis severity framework is replaced; medical-liaison role is deployed without updating the OVERRIDE_PATH handoff format.

**Section 18 — Open Questions.** Includes the deferred items from CONTINUATION_BRIEF §13: threat-model-catalog ownership decision (likely assigned to Role 1 per CB §13 item 4); BLOCK_WITH_OVERRIDE_PATH adjudicator transition path during pre-Role-7 phase.

**Appendix A.** Empty at Phase-2; populated through Phase-3/4.

The template absorbs the content cleanly. No section is N/A for this role. No content is forced to live in two places.

---

## 8. Alternatives Considered

### Alternative A — Keep Quant 20-section template as-is

REJECTED. Five Quant sections (2, 9, 11, 20, plus subsections of 6/7/8 specific to pipeline mechanics) are literally N/A for agent-role design docs. Forcing the Pass-2 author to write "OMITTED — N/A because agents don't own pipeline state" five times per design doc is structural noise. Worse, the remaining sections lack slots for the load-bearing medical-domain content (Pass-1 Deliverable Digest, Cross-Role References, Mechanical Enforcement Map). A template that requires writing "OMITTED" five times AND adding three new sections per role is the same surgery as this proposal, only less honest about what changed.

### Alternative B — Use AGENT_TEMPLATE.md structure directly as the design doc

REJECTED. AGENT_TEMPLATE.md is the OUTPUT shape (the agent.md the upgrade-agent produces). Using it as the design doc shape collapses the design-doc-protocol's purpose: there is no slot for Problem Statement, Pass-1 Deliverable Digest, Cross-Role References, Mechanical Enforcement Map, Edge Cases, Acceptance Criteria, Invariants at Risk, Risk Assessment, Open Questions, or Red Team Findings — i.e., 10 of the 18 sections in this proposal. The design doc and the agent.md are different artifacts at different stages of the pipeline; conflating them eliminates the layer where Pass-2 review and red-team verification happen. Additionally, AGENT_TEMPLATE.md sections are bounded by token budgets (the agent.md must fit in ≤2,000 tokens); a design doc must be more substantive — it captures rationale, alternatives considered, and the audit trail.

### Alternative C — Use only the 8 transferring Quant sections + a "Pass-1 Substrate Map" appendix

REJECTED. This was the closest competitor. It would have given a 9-section design doc (1, 12, 15, 16, 17, 18, 19, A + Pass-1 Substrate Map) which is appealingly compact. But it omits: (a) the cross-role references section (CONTINUATION_BRIEF §10 enumerates 7 references that must survive Pass-2 — they need a dedicated slot, not a buried appendix line); (b) the section-by-section AGENT_TEMPLATE.md mapping (the upgrade-agent must consume this; without explicit Core Rules / Ask vs Proceed / etc. sections in the design doc, the upgrade-agent re-derives the mapping per role, which is the structural waste Lesson 3 warned against); (c) the Mechanical Enforcement Map (without a dedicated section, mechanical checks get scattered across Core Rules, Edge Cases, and Acceptance Criteria, and the session-close audit step 8.5 has no single anchor to read). The compactness gain (9 sections vs 18) trades structural integrity for token count — wrong direction for a load-bearing template.

---

## 9. Acceptance Criteria for the Template

Binary pass/fail propositions a reader uses to evaluate whether this template is fit-for-purpose:

1. Every AGENT_TEMPLATE.md section (Identity, Core Rules, Role Boundaries, Ask vs Proceed, Loop-Breaking, Tools, Communication, Context Loading, Anti-Patterns, Role-specific sections, Negative Examples) has at least one design-doc section that produces input for it. **Verified:** Identity → §2; Core Rules → §5; Role Boundaries → §2; Ask vs Proceed → §6; Loop-Breaking → §7; Tools → §8; Communication → §9; Context Loading → §10; Anti-Patterns → §11; Negative Examples → §12; Role-specific sections → §5 + §9 (refusal templates) + §11 (project-history-grounded anti-patterns).
2. No proposed section is N/A for >2 of the 4 foundation roles. **Verified:** §3 (Pass-1 Digest) is REQUIRED for all 4 foundation roles. §4 (Cross-Role References) is REQUIRED for all 4. §13 (Mechanical Enforcement Map) is REQUIRED for all 4. No section is N/A for any of the 4.
3. The 12 non-transferring Quant sections (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 20) are each accounted for in §3 (Transfers), §4 (Must Change), or §5 (Must Add) of this proposal. **Verified:** §4 of this proposal tabulates all 12 non-transferring Quant sections with explicit treatment.
4. The 8 transferring Quant sections (1, 12, 15, 16, 17, 18, 19, A) each map to a section in this proposal. **Verified:** §3 of this proposal tabulates all 8 with mapping (1→§1; 12→§14; 15+18→§17; 16→§15; 17→§16; 19→§18; A→Appendix A).
5. Every section in §2 has: section number, name, one-sentence purpose, writer-produces spec, REQUIRED/CONDITIONAL designation with condition, line/word budget, AGENT_TEMPLATE.md mapping, /upgrade-agent phase mapping. **Verified:** §2 sections 1–18 + Appendix A all carry these fields.
6. The proposal has ≤30 sections total. **Verified:** 18 sections + 1 Appendix = 19 ≤ 30.
7. Every cross-role reference enumerated in CONTINUATION_BRIEF §10 has a dedicated slot in the proposal. **Verified:** §4 (Inherited Cross-Role References) explicitly references the CONTINUATION_BRIEF §10 table.
8. The proposal does not specify implementation details for HOW each section is written (only WHAT goes in each section). **Verified:** §2's "Writer produces" subsections specify content, not authoring algorithm. Architecture Core Rule 6 honored.
9. Every active row in INVARIANTS.md is addressed by either an existing template section or has a documented out-of-scope rationale. **Verified:** INV-HO-ROTATION + INV-HO-NO-STALE-HASH (HANDOFF.md only, out-of-scope for design doc); INV-RESEARCH-* (referenced via §16); INV-ROLE-INLINING (referenced via §13 mechanical map); INV-SCOPE-CONTRACT + INV-PF-ATTESTATION + INV-BRANCH-NOT-MAIN (session-process invariants, referenced via §13 and §16).

---

## 10. Open Questions

These are questions the orchestrator must adjudicate before this template becomes canonical:

1. **Are conditional sections allowed to be omitted entirely, or must they appear with an "OMITTED — rationale" stub?** This proposal assumes stub-required (no silent omissions, per the false-zero principle in the Deliverable Check and the project's PF attestation discipline). The orchestrator may prefer to allow truly N/A sections to be cleanly absent. Recommendation: stub-required. Consequence-of-not-deciding: writers will inconsistently omit, complicating the cross-document audit.

2. **Should Section 3 (Pass-1 Deliverable Digest) for specialist roles in Pass-3 reference foundation-role design docs OR foundation-role agent.md files (once deployed)?** Pass-3 ordering is unresolved (CONTINUATION_BRIEF §13 item 1: foundation-role agent.md deployment is the user's Session-B option). If foundation-role agent.md exists at Pass-3 authoring time, specialists could reference the agent.md directly. If not, they reference the Pass-2 design doc. Recommendation: both — reference foundation design doc primarily, with a note that once foundation agent.md is deployed, Pass-3 may cite it directly. Consequence: ambiguous citation target during the transition window.

3. **Should Section 13 (Mechanical Enforcement Map) be empowered to propose NEW invariants (with required `INV-X-YYY` IDs), or strictly reference existing ones?** CONTINUATION_BRIEF §9 lists 7 candidate invariants that have not been promoted. The design doc could either: (a) reference them as candidates (low commitment), or (b) trigger the INVARIANTS.md change ritual when a design doc surfaces a new mechanical check. Recommendation: (a) reference as candidates; promotion to INVARIANTS.md remains a separate user-authorized act per the change discipline in INVARIANTS.md lines 19–24. Consequence: if (b) is chosen, every design doc could grow the invariant register without user review at the right granularity.

4. **Is the line/word budget per section a hard ceiling or a target?** This proposal phrases them as targets ("25–40 lines"). The Quant template has no per-section budgets at the design-doc level. Recommendation: targets, with a Section 15 (Acceptance Criteria) hook that flags any section >150% of its budget upper bound for review. Consequence: hard ceilings would force premature compression; pure targets would allow bloat.

5. **Does Appendix A (Red Team Findings) require the Phase-2 design-doc to ship with an empty stub, or only after Phase-3 dispatches red-team agents?** This proposal says "REQUIRED at Phase-5 finalize (created empty at Phase-2 synthesis)." But the Phase-2 design doc is currently committed (per design-doc-protocol Phase 2 output line 85) — implying Phase-2 commit happens before red-team runs. Recommendation: Phase-2 commit includes the empty Appendix A as a stub with "TO BE POPULATED IN PHASE 3" note. Consequence-of-not-deciding: design-doc-protocol Phase-2 vs Phase-5 commit boundaries become ambiguous.

---

## 11. Risk Assessment

If this template structure is wrong in load-bearing ways, the defect propagates through 4 foundation-role design docs + 14 specialist-role design docs = 18 downstream artifacts. Specific failure scenarios:

- **Risk 1 — Section 3 (Pass-1 Deliverable Digest) is too compressed.** If the Digest table format loses important nuance from the Pass-1 Findings, every foundation-role agent.md inherits a distorted research substrate. Downstream: agent.md misencodes evidence-tier discipline or refusal-class taxonomy. **Severity: BLOCK.** Mitigation: §3 spec requires "cite source line range in `domain-research.md`" — paraphrase drift is detectable by reading the cited range.
- **Risk 2 — Section 4 (Cross-Role References) misses a CONTINUATION_BRIEF §10 entry.** If a cross-role reference is omitted from §4, the role's agent.md may redefine the referenced concept inconsistently with the source role's design doc. Downstream: refusal-class taxonomy or evidence-tier vocabulary diverges across the 4 foundation roles. **Severity: MAJOR.** Mitigation: §4 spec requires "every applicable row from CONTINUATION_BRIEF §10 present"; binary verifiable.
- **Risk 3 — Section 13 (Mechanical Enforcement Map) lists checks that don't exist.** If §13 names an audit script or hook that doesn't actually exist (e.g., a hallucinated `scripts/foo.sh`), the Pass-5 verification step appears to pass but is vacuous. Downstream: agent.md deploys with claimed mechanical enforcement that doesn't run. **Severity: BLOCK.** Mitigation: §13 spec requires "each row's mechanism either resolves to an existing path OR specifies the new path + behavioral spec" — paths must be verifiable.
- **Risk 4 — Section 16 (Invariants at Risk) misses an applicable invariant.** If §16 doesn't catch an invariant the role's deployment could violate, the session-close audit (CLAUDE.md step 8.5) won't fire on the right script. Downstream: invariant violation lands in production. **Severity: BLOCK.** Mitigation: §16 spec requires "every active INVARIANTS.md row addressed (positive risk-claim OR explicit no-risk note)."
- **Risk 5 — Section 18 (Open Questions) is closed prematurely with false-zeros.** If the design-doc author closes Open Questions without honestly surfacing unresolved items (i.e., silent absence rather than explicit attestation), the orchestrator can't adjudicate. Downstream: 18 design docs ship with unflagged ambiguity that compounds at integration time. **Severity: MAJOR.** Mitigation: §18 spec requires "Empty list permitted IF the design doc has no open questions, but must say so explicitly" — false-zero attestation principle inherited from PF-S3-01.

The downstream artifacts that would inherit these defects: every Pass-2 design doc (4 foundation), every Pass-3 design doc (14 specialist), every resulting `agent.md` (18 total), every session-close audit run after deployment.

---

## 12. Breaks If

Concrete conditions under which this proposed template becomes wrong:

1. **AGENT_TEMPLATE.md gains a 12th section or loses one.** This template's §2 mapping table is keyed to the current 11-section AGENT_TEMPLATE.md. If the template upstream changes structure, the design-doc template's AGENT_TEMPLATE.md mapping column goes stale. Detection: when `/upgrade-agent` is rebuilt OR when `AGENT_TEMPLATE.md` is modified — diff the section count.
2. **`/upgrade-agent` command's Phase numbering changes.** Section 2's "/upgrade-agent phase" mapping cites Phase 1/3/5/6/7/8 specifically. If `/upgrade-agent` is refactored (per CONTINUATION_BRIEF §13 transitions), the phase-mapping column goes stale. Detection: when `~/.claude/commands/upgrade-agent.md` is modified — diff the Phase headings.
3. **A new mandatory cross-document fact is added to CLAUDE.md Cross-Document Ownership Matrix that has no slot in this template.** E.g., if a future row "Agent role versioning history" is added to the matrix and assigned to design docs, this template would need a §19 section. Detection: cross-check the matrix at every CLAUDE.md revision.
4. **Pass-1's `domain-research.md` structure changes — Findings are no longer the unit of synthesis.** Section 3 (Pass-1 Deliverable Digest) is keyed to Finding-row format. If a future Pass-1 deliverable uses a different structure (e.g., Themes instead of Findings), §3's row format breaks. Detection: when a new Pass-1 deliverable is committed — check the heading skeleton.
5. **The 4 foundation roles + 14 specialists collapse to a different role count.** This template's §7 (Worked Example) and §11 (Risk Assessment) assume "18 downstream artifacts." If the roster in `vault/WIKI.md` changes substantially (e.g., a master-roster + per-agent specs pattern is adopted per CONTINUATION_BRIEF §13 item 2), the template may need to support a tiered design-doc shape that this proposal does not currently include. Detection: at each `vault/WIKI.md` revision or at the Pass-3 first-specialist authoring milestone.
6. **The refusal-class taxonomy in Role-1 Finding 5 is rescinded by regulatory change.** §9 (Communication Protocol) requires refusal templates citing the taxonomy. If the FDA 2026 CDS Final Guidance is rescinded or substantially revised (per §17 Risk #4 break-condition), the refusal-template requirement may need restructuring across all 18 design docs. Detection: at FDA guidance updates affecting §520(o)(1)(E).
7. **`INVARIANTS.md` adopts a fundamentally different schema.** §16 (Invariants at Risk) and §13 (Mechanical Enforcement Map) both key off INVARIANTS.md's current Register table format (ID / Scope / Property / Statement / Verification / Auth). If the register is refactored, these sections need rewriting. Detection: at INVARIANTS.md schema change.
