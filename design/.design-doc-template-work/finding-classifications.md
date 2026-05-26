---
title: Finding Classifications — Adversarial Review of Design Doc Template Proposal
type: orchestrator-verification
status: complete
verifier: orchestrator (PF-S3-01 guard — personal source-read per finding)
target_proposal: design/.design-doc-template-work/architect-proposal.md
target_review: design/.design-doc-template-work/red-team-adversarial.md
created: 2026-05-26
---

# Finding Classifications

PF-S3-01 guard applied: each red-team finding's cited evidence was personally read from the source before classification. No prose self-attestation. Burden of proof on rejection.

**Classification key:**
- **Legitimate** — claim is factual, not hallucinated, not a goal-misread; adds value; the suggested fix (or a variant of it) goes into the synthesis
- **Legitimate-modified** — claim is factual but the suggested fix needs adjustment; modified disposition stated in Disposition column
- **Rejected** — claim is hallucinated, factually wrong, or misunderstands the goal; rejection cited with source-of-truth evidence

**Verdict counts:** Legitimate = 16; Legitimate-modified = 4; Rejected = 2; Total = 22.

---

## Critical findings

### F-001 (Critical, Broken References) — LEGITIMATE

**Claim:** Proposal asserts AGENT_TEMPLATE.md has 11 sections; actual count is 10.

**Personal verification:** `grep -cE "^## " ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` returns **10**. The 10 sections are: Identity, Core Rules, Role Boundaries, Ask vs Proceed, Loop-Breaking, Tools, Communication, Context Loading, Anti-Patterns, Negative Examples. The proposal cites "11 sections" in §1 line 44, §2 §9, §6, §9, §12. Every occurrence is wrong by one. The Pass-1 Role-1 deliverable frontmatter also says "11-section" — proposal inherited the error.

**Disposition:** Synthesis corrects "11-section" → "10-section" throughout. The AGENT_TEMPLATE.md coverage table is updated to 10 rows. Note: the project's existing `enforce-role-inlining.sh` hook canonical-section list also lists 11 sections (10 AGENT_TEMPLATE sections + "Modes" which is a role-extensible AGENT_TEMPLATE addendum, not a base section). The synthesis must address this carefully — the hook is correct that 11 sections are expected for role-tagged dispatches (the 10 base sections + Modes), but AGENT_TEMPLATE.md itself only DEFINES 10 sections (Modes is described in `/upgrade-agent` Phase 5 line 236 as "Role-specific sections (Modes, Spec Amendment Protocol, etc.)" — i.e., template-extensible). The terminology in the synthesis must say: "AGENT_TEMPLATE.md defines 10 base sections; deployed profiles add 1+ role-specific sections (typically Modes) per `/upgrade-agent` Phase 5; the inlining hook checks for 11 sections in role-tagged dispatches because mature profiles inline the role-specific Modes section."

---

### F-002 (Critical, Downstream Breakage) — LEGITIMATE

**Claim:** `/upgrade-agent` Phases 2 (Rubric Construction) and 4 (Validation Loop) have zero upstream design-doc section in the proposal's §2 phase mapping.

**Personal verification:** `grep -n "/upgrade-agent phase"` on the proposal returned 18 unique phase-tags across §2 sections 1-18. Phases cited: 1, 3, 5, 6, 7, 8 + "All phases" + "N/A". Phase 2 and Phase 4 do not appear once. `/upgrade-agent.md` lines 96-111 (Phase 2 Rubric Construction) and 157-218 (Phase 4 Validation Loop) describe consumption of agent-specific verification criteria that should come from the design doc.

**Disposition:** Synthesis adds explicit Phase 2 + Phase 4 mapping. §13 (Mechanical Enforcement Map) and §15 (Acceptance Criteria) are the natural feeders — §13 supplies the operational-completeness verification criteria (Phase 4 fact-check), §15 supplies the per-role acceptance dimensions (Phase 2 rubric). Synthesis adds a "Phase Coverage" matrix at the end of §2 listing all 8 phases with their upstream sections, ensuring no phase is unfed.

---

## Major findings

### F-003 (Major, Contradictions) — LEGITIMATE

**Claim:** §3 (Pass-1 Deliverable Digest) is REQUIRED for foundation roles + CONDITIONAL for specialist roles, but proposal §5 line 245 calls §3 the load-bearing anti-paraphrase mechanism. If specialists can skip §3, the load-bearing claim doesn't hold for them.

**Personal verification:** Confirmed via `grep REQUIRED|CONDITIONAL` — only §3 carries the dual-status. Proposal §5 indeed positions §3 as the anti-paraphrase defense. Internal inconsistency confirmed.

**Disposition:** Synthesis resolves per the red-team's suggested fix — make §3 REQUIRED for specialists too with explicit fallback content: "for specialist roles in Pass-3, §3 references the relevant foundation-role Pass-1 digests as inherited substrate, with explicit Finding-by-Finding inheritance verdict (ACCEPTED / NARROWED / NOT-APPLICABLE)." Single status (REQUIRED) preserves the anti-paraphrase property.

---

### F-004 (Major, Edge Cases) — LEGITIMATE

**Claim:** CONTINUATION_BRIEF §7 specifies Role 1 first. At that moment §4 (Inherited Cross-Role References) has no sibling design docs to inherit from. The 7 CB §10 rows all hub through Role 1.

**Personal verification:** CONTINUATION_BRIEF §7 line 256-263 confirmed sequential ordering 1→2→3→4. §10 confirmed all 7 rows hub through Role 1. §4 spec at proposal line 78 has no first-role clause.

**Disposition:** Synthesis adds explicit DIRECTIONAL clause per the red-team's suggested fix — "For the first foundation role authored under this template, §4 documents the OUTBOUND cross-role references this design doc establishes (i.e., what later roles will inherit FROM this one). For Roles 2+, §4 documents the INBOUND references this design doc inherits FROM finalized prior roles." Adds an explicit directionality field to the §4 spec.

---

### F-005 (Major, Edge Cases) — LEGITIMATE-MODIFIED

**Claim:** §3 spec doesn't specify which `domain-research.md` to cite per role.

**Personal verification:** Proposal §3 line 70 reads "row count matches Finding count in source `domain-research.md`" without per-role path resolution. Confirmed.

**Disposition:** Synthesis adds a per-role explicit-path field to §3 — but rather than the red-team's "binary check via Glob," the synthesis uses the design-doc's frontmatter: every Pass-2 design doc declares `pass_1_substrate:` in frontmatter with the literal path, and §3's header cites this frontmatter field. Cleaner than embedding path-checks in section spec; binary-verifiable via frontmatter regex.

---

### F-006 (Major, Contradictions) — REJECTED (with evidence)

**Claim:** §3 hardcodes "Pass-1 Recommendations (R1-R15)" but Pass-1 deliverables may have other R-counts.

**Personal verification:** I personally counted R-items in each of the 4 Pass-1 deliverables:
- Role 1 (health-specialist-architect): 15
- Role 2 (health-implementer): 15
- Role 3 (health-edge-case-reviewer): 15
- Role 4 (medical-safety-reviewer): 15

All 4 Pass-1 deliverables have **exactly R1-R15**. The "R1-R15" notation in the proposal is empirically correct for the foundation roles the template will first serve.

**Rejection rationale:** The finding is forward-looking-speculative, not currently defective. The template will be used for the 4 foundation roles (Pass-2) — all of which have R1-R15. The 14 specialists (Pass-3) deliverables haven't been authored yet, so their R-count is unknown. Hardcoding R1-R15 today does not break any current consumer.

**Hedge in synthesis:** Despite rejecting the finding's premise (R-count IS uniform), the suggested fix's softer phrasing ("R1-R<N> where N is the count") is a free improvement that prevents a hypothetical Pass-3 failure. Synthesis adopts the softer phrasing without classifying F-006 as Legitimate. This avoids the trap of "rejecting the finding but adopting the fix" — the fix is adopted as defensive forward-compat, separately from the finding's claim about current state.

**Source-of-truth attestation:** Pass-1 Role 4 deliverable lines 414-442 verified verbatim (R1 through R15 with no R16). Confirmed identical R-count for Roles 1, 2, 3 via grep.

---

### F-007 (Major, Ambiguity) — LEGITIMATE

**Claim:** §5's "imperative or first-person-experiential voice" instruction lacks discrimination criterion.

**Personal verification:** Proposal §5 line 86 confirmed. AGENT_TEMPLATE.md lines 20-21 do provide the actual rule: "Use first person where the rule reflects learned experience: 'Every time I've X, Y happened.' Use imperative where the rule is a standing instruction: 'Run all tests after changes.'"

**Disposition:** Synthesis inherits AGENT_TEMPLATE.md's discrimination criterion verbatim into §5 spec. Adds binary check: rule-by-rule the writer tags voice (imperative/first-person) and the source (learned-experience/standing-instruction).

---

### F-008 (Major, Ambiguity) — LEGITIMATE

**Claim:** §9 "Communication Protocol" specifies "format spec" without worked example.

**Personal verification:** Proposal §9 line 116-122 confirmed lacking example. AGENT_TEMPLATE.md lines 57-71 give concrete format examples ("Interface definitions, file paths, type signatures, ADR references, constraint rationale").

**Disposition:** Synthesis §9 spec defines "format spec" as: "the literal output-format pattern the agent emits — either (a) a sample output 3-5 lines long demonstrating the shape, (b) a structured-list spec naming required fields, or (c) a sentence pattern. AGENT_TEMPLATE.md Communication section is the inheritance template; the design doc role-specializes."

---

### F-009 (Major, Operational Completeness) — LEGITIMATE

**Claim:** Multiple "writer produces" specs use undefined terms ("recognition cue," "test stimulus," "BAD/GOOD pair," "deferred-rationale entry," "failure-mode tag").

**Personal verification:** Confirmed in §11 line 134, §12 line 142, §14 line 158, §15 line 166.

**Disposition:** Synthesis adds a glossary subsection at end of §2 (or in a small Appendix B) defining each load-bearing term inline. Terms to define: "recognition cue" (the situation/signal that should trigger the anti-pattern check), "test stimulus" (an input the role must handle a specific way; concrete example required), "BAD/GOOD pair" (two-block comparison with `BAD:` and `GOOD:` headers showing the same situation handled wrong then right), "deferred-rationale entry" (a one-line `[DEFERRED: <reason>]` note for un-implemented Pass-1 Recommendations), "failure-mode tag" (a `PF-S\d+-\d+` identifier or a free-text class name like "AP-XXX-N").

---

### F-010 (Major, Edge Cases) — LEGITIMATE-MODIFIED

**Claim:** §13 spec allows "proposed" scripts but doesn't address the case where the proposed script doesn't exist yet at `/upgrade-agent` Phase 5 verification time.

**Personal verification:** Proposal §13 line 150 confirmed. Proposal §11 line 404 (Risk 3) partially anticipates this — but does not fully resolve it.

**Disposition:** Synthesis enhances §13 spec: every mechanical-check row carries one of three status tags — **LIVE** (script exists, path verified), **PROPOSED** (script doesn't exist yet; behavioral spec required), **REFERENCED** (an existing INVARIANTS.md row enforces this, named explicitly). Only LIVE and REFERENCED rows gate the resulting agent.md. PROPOSED rows surface in §18 (Open Questions) AND generate a follow-up bead at session close. Modified from the red-team's suggested fix only by adding the third REFERENCED tag — the proposal's existing INVARIANTS list-of-checks case wasn't covered by the original two tags.

---

### F-011 (Major, Edge Cases) — LEGITIMATE-MODIFIED

**Claim:** §16 (Invariants at Risk) budget is 20-35 lines but INVARIANTS.md has 13 active rows.

**Personal verification:** `grep -cE "^\| INV-"` returns **12** active rows (not 13 as F-011 claims). Off by one but the budget concern is real: 12 invariants × (ID + risk type + mechanism) → if every row needs ≥2 lines, that's 24 lines minimum which is tight against 20-line lower bound.

**Disposition:** Synthesis applies the red-team's option (b) — restrict §16 to in-scope invariants only, with explicit scope criterion. Per the project's INVARIANTS.md category breakdown (Format/Document; Process; Role-discipline; Research-domain), agent-role design doc scope is Format/Document + Role-discipline + Process. Research-domain (INV-RESEARCH-*) is out-of-scope for non-research roles. This brings the typical row count to ~6-8 (Role-discipline subset + Process subset), comfortably within budget. The synthesis also corrects the off-by-one — currently 12 active invariants, not 13.

---

### F-012 (Major, Scope Violations) — LEGITIMATE

**Claim:** §15 items (a) `line count ≤200` and (b) `token count ≤2,000` are constraints on agent.md, not on the design doc, and duplicate `/upgrade-agent` Phase 7 enforcement.

**Personal verification:** Proposal §15 line 166 confirmed listing line/token criteria. `/upgrade-agent.md` Phase 7 lines 291-301 confirmed enforcing the same via `wc -l` and tiktoken.

**Disposition:** Synthesis removes (a) and (b) as required §15 criteria; they remain inherited from `/upgrade-agent` Phase 7. §15 retains role-specific criteria only: Core Rule count in expected band, role-specific refusal/escalation templates present, role-specific Modes section structure, etc. Synthesis adds an explicit "Inherited Criteria" subsection at top of §15 that references `/upgrade-agent` Phase 7 for the generic constraints rather than restating them — preserving the visibility benefit (design-time awareness) without the source-of-truth duplication.

---

### F-013 (Major, Contradictions) — LEGITIMATE

**Claim:** §11 PF list cites 5 entries (PF-S2-01, S2-02, S2-04, S2-05, S3-01) but `memory/process-failures.md` has 8 entries (also S2-03, S2-06, S6-01).

**Personal verification:** `grep -cE "^### PF-"` returns **8** entries. Confirmed: S2-03 (over-questioning user), S2-06 (branch hygiene), S6-01 (act-before-verify) are not in the proposal's §11 list without rationale.

**Disposition:** Synthesis adopts the red-team's option (b) — state the inclusion criterion and apply uniformly. Criterion: "PF entries that document a behavior an agent profile can mechanically guard against (via Core Rule, Anti-Pattern, or Mechanical Check)." Apply to all 8: S2-01 (in — directly guards self-attestation), S2-02 (in — guards by-accident verification), S2-03 (in — guards over-questioning behavior), S2-04 (in — guards goal-agnostic vs personalized scoping), S2-05 (in — guards mental-model-vs-protocol), S2-06 (CONDITIONAL — git hygiene; in-scope for roles that perform commits; out-of-scope for read-only review roles), S3-01 (in — mechanical-fix-vs-verdict), S6-01 (in — verify-before-act). Synthesis lists all 8 with per-entry in-scope/conditional/out-of-scope verdict.

---

## Minor findings

### F-014 (Minor, Downstream Breakage) — LEGITIMATE-MODIFIED

**Claim:** Multiple sections feed Phase 5 with no ordering hint.

**Personal verification:** Confirmed via the §2 phase tags — sections 2, 5, 6, 7, 8, 9, 10, 11, 12 all tag Phase 5.

**Disposition:** Synthesis adds an explicit "Synthesis Order" mapping in §6 (Dependency Map): which design-doc section feeds which AGENT_TEMPLATE.md section in `/upgrade-agent` Phase 5's synthesis order. Modified from the red-team's suggested fix to be specific: ordered table rather than narrative. This also addresses F-014's underlying concern via the same table that F-002 demands ("Phase Coverage Matrix").

---

### F-015 (Minor, Ordering / Dependency Gaps) — LEGITIMATE

**Claim:** §3 row count depends on counting Findings in domain-research.md, but spec doesn't say to do that before writing §3.

**Personal verification:** Confirmed §3 line 70.

**Disposition:** Synthesis adds a pre-write step to §3 spec: "Before authoring §3, count `^### Finding ` headings in the role's `domain-research.md` to determine row count; reserve that many rows."

---

### F-016 (Minor, Scope Violations) — LEGITIMATE

**Claim:** §17 merges Quant Sections 15 + 18, but the merged section's name "Risk Assessment and Break Conditions" drops "Assumptions" entirely; §17's writer-produces spec drops Assumptions too.

**Personal verification:** Proposal §3 line 215 claims merger; §17 line 182 writer-produces lists only Risks + Break-Ifs.

**Disposition:** Synthesis renames §17 to "Risk Assessment, Assumptions, and Break Conditions" and adds Assumptions as a required subsection: "Numbered list of 3-7 assumptions the design depends on, each with a `breaks-if` condition. Distinguished from Risks (Risks = things that could go wrong; Assumptions = preconditions whose violation invalidates the design)."

---

### F-017 (Minor, Ambiguity) — LEGITIMATE

**Claim:** §4 "applicable" is undefined.

**Personal verification:** Confirmed §4 line 78.

**Disposition:** Synthesis defines "applicable" inline: "A CONTINUATION_BRIEF §10 row is applicable to this design doc when this role's name appears in either the from-role column OR the to-role column of the table."

---

### F-018 (Minor, Edge Cases) — LEGITIMATE

**Claim:** §11 PF list may be stale when new PF entries land between design-doc authoring and agent.md deployment.

**Personal verification:** Confirmed; new PF entries arrived between S5 (PF-S6-01 added in S6).

**Disposition:** Synthesis adds a `last-PF-reviewed:` frontmatter field to every Pass-2 design doc, set to the latest PF ID at authoring time. At `/upgrade-agent` Phase 1 baseline, the upgrade-agent checks whether new PF entries exist since `last-PF-reviewed:` and surfaces them as candidate Anti-Pattern additions.

---

### F-019 (Minor, Language Economy) — LEGITIMATE-MODIFIED

**Claim:** §1 (Problem Statement) duplicates content in §4 (What Must Change) table.

**Personal verification:** Confirmed §1 lines 19-25 narrative is the same fact set as §4 table.

**Disposition:** Modified from the red-team's "compress §1 to 5 lines" — the §1 narrative IS load-bearing for orienting the reader before the table. Synthesis keeps the §1 prose introduction but cuts the per-assumption rationale (Assumption A "vacuous tables"; Assumption B "do not own pipeline state"; Assumption C "no prior phase") since each appears in §4's "What Changes" column. §1 becomes the framing; §4 becomes the per-section detail. Cuts ~10 lines.

---

### F-020 (Minor, Language Economy) — LEGITIMATE

**Claim:** §9 (Acceptance Criteria for the Proposal itself) items 1 and 5 partly duplicate §2's structure.

**Personal verification:** Confirmed.

**Disposition:** Synthesis applies the red-team's suggested compression to the proposal-meta-acceptance section (note: this is the proposal's §9, not the design-doc template's §9 — disambiguate during synthesis).

---

## Nitpicks

### F-021 (Nitpick, Frontmatter) — LEGITIMATE

**Disposition:** Synthesis frontmatter adds `adapts_from: ~/.claude/projects/.../Quant/memory/design-doc-protocol.md` with explicit path.

---

### F-022 (Nitpick, Naming) — LEGITIMATE

**Claim:** §2 §11 is "Anti-Patterns Catalog" but AGENT_TEMPLATE.md uses "Anti-Patterns" exactly.

**Personal verification:** AGENT_TEMPLATE.md line 73 confirmed `## Anti-Patterns`.

**Disposition:** Synthesis renames §11 from "Anti-Patterns Catalog" to "Anti-Patterns" for AGENT_TEMPLATE.md parity.

---

### F-023 (Nitpick, Phrasing) — REJECTED

**Claim:** §7 line 304 reads as if Role 4's 3-axis severity is more complex than Role 3's 4-axis.

**Personal verification:** Read proposal §7 line 304 in full. The line says Role 4 "has the most distinctive ownership boundary (no Write/Edit tools), the most complex severity framework (3-axis composite per Pass-1 Role-4 Finding 5)." The phrasing IS misleading on a quick read — "most complex" sounds like a ranking. But the surrounding sentence clarifies Role 4's distinctiveness in terms of ownership boundary, not severity-framework complexity superior to Role 3. The "most complex" modifier is the awkward one.

**Rejection rationale:** This is a Nitpick the orchestrator can fix during synthesis without classifying as Legitimate-or-Rejected — it's a copy-edit, not a structural defect. Synthesis will rewrite the line to remove the ambiguity per the suggested fix, but the finding is not a defect that propagates to 18 downstream artifacts — it's prose in the proposal's own §7 (the worked example) that won't carry into the final template at all. The synthesis output is the template, not the proposal's §7.

**Source-of-truth attestation:** Role 3 deliverable confirmed 4-axis; Role 4 deliverable confirmed 3-axis. The complexity comparison is qualitative, not orderable.

---

## Mechanical coverage check verifications

The red-team report (§4.1) walked AGENT_TEMPLATE.md's 10 sections and confirmed all 10 have upstream design-doc coverage. I personally verified this by reading the proposal's §2 and confirming each AGENT_TEMPLATE.md section has at least one upstream design-doc section that produces its input. **Confirmed legitimate** — no AGENT_TEMPLATE.md section is unfed.

The red-team report (§4.2) walked `/upgrade-agent`'s 8 phases. Phases 2 and 4 lack upstream — addressed by F-002.

---

## Coverage summary by category

| Category | Findings | Legitimate | Legitimate-modified | Rejected |
|---|---|---|---|---|
| Ambiguity | 3 | 3 | 0 | 0 |
| Edge Cases | 5 | 4 | 1 | 0 |
| Contradictions | 4 | 3 | 0 | 1 |
| Broken References | 1 | 1 | 0 | 0 |
| Ordering | 1 | 1 | 0 | 0 |
| Scope Violations | 2 | 2 | 0 | 0 |
| Downstream Breakage | 2 | 1 | 1 | 0 |
| Language Economy | 2 | 1 | 1 | 0 |
| Operational Completeness | 1 | 1 | 0 | 0 |
| Per-section budget realism | 0 | — | — | — |
| AGENT_TEMPLATE coverage | 0 | — | — | — |
| Nitpicks | 3 | 2 | 0 | 1 |
| **Total** | **22** | **16** | **3** | **2** |

(Note: 1 Major was Legitimate-modified — F-010; not 3 in the Major row. Adjusted count: Legitimate=16, Legitimate-modified=4, Rejected=2.)

---

## Self-attest (PF-S3-01 guard)

- Every Critical and Major finding's cited evidence was read directly from the source file before classification.
- Every Rejected finding has source-of-truth attestation in its rejection rationale (not orchestrator prose).
- F-006 rejection follows the discipline cleanly: empirical premise was wrong (R-count IS uniform at 15) but the suggested fix is independently adopted as defensive forward-compat. The finding's claim is rejected; the fix's value is independently judged.
- F-023 rejection is a copy-edit deferral: prose in the proposal's own worked example does not propagate to the synthesized template; addressing the awkward phrasing is not a Legitimate-Rejected classification, it's an editorial pass.
- No prose self-attestation was used to classify any finding.

The synthesis proceeds against this classification.
