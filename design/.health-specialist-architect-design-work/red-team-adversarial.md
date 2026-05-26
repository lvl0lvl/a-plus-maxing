---
title: Adversarial Review — health-specialist-architect Pass-2 Design Doc
type: adversarial-review
target: design/health-specialist-architect-design.md
created: 2026-05-26
categories_walked:
  - Ambiguity
  - Edge Cases
  - Contradictions
  - References
  - Ordering
  - Scope
  - Downstream
  - Language Economy
  - Role Discipline (agent-specific)
  - Sycophancy Coverage (agent-specific)
  - Mechanical Enforcement Claim Integrity (agent-specific)
mechanical_coverage_checks:
  - AGENT_TEMPLATE_10_base_sections
  - upgrade-agent_8_phase_coverage
status: ready-for-Phase-4-orchestrator-verification
---

# Adversarial Review of `design/health-specialist-architect-design.md`

Walkthrough of 11 categories (8 standard + 3 agent-specific) and 2 mechanical coverage checks per dispatch contract.
Target: a 727-line Pass-2 design doc at status `Phase-3 Red-Team Pending`.
Reviewer applied PF-S3-01 discipline: every claim cites file + line range; suggested fixes that have independent value are flagged for the reject-but-adopt classifier in Phase 4.

---

## Summary table

### By severity

| Severity | Count |
|---|---|
| Critical | 2 |
| Major | 8 |
| Minor | 9 |
| Nitpick | 4 |
| **Total** | **23** |

### By category

| Category | Findings |
|---|---|
| Ambiguity | F-001, F-002, F-003 |
| Edge Cases | F-004, F-005 |
| Contradictions | F-006, F-007 |
| References | F-008, F-009, F-010 |
| Ordering | F-011 |
| Scope | F-012, F-013 |
| Downstream | F-014, F-015 |
| Language Economy | F-016, F-017 |
| Role Discipline (agent-specific) | F-018, F-019 |
| Sycophancy Coverage (agent-specific) | F-020, F-021 |
| Mechanical Enforcement Claim Integrity (agent-specific) | F-022, F-023 |

---

## Findings (F-N format)

### F-001 — AC-4 grep pattern returns LINES not unique identifiers; AC fails against the design doc itself

| Field | Value |
|---|---|
| Category | Mechanical Enforcement Claim Integrity |
| Section affected | §15.2 (AC-4); §2.2 item 3 |
| Severity | **Critical** |

**Description.** AC-4 (line 561) reads: "The 7 class identifiers appear at least once in the design doc body (`grep -cE 'PATIENT_FACING_DIRECTIVE\|IMAGE_OR_SIGNAL_INPUT\|TIME_CRITICAL\|BASIS_NOT_REVIEWABLE\|PRESCRIPTIVE_DIRECTIVE\|DEVICE_FUNCTION\|HIGH_RISK_SAMD'` ≥ 7)." The `grep -c` flag counts MATCHING LINES, not pattern occurrences. The doc currently has 4 matching lines (verified: `grep -cE '…' design/health-specialist-architect-design.md` returns `4`). The 7 identifiers DO each appear (verified: `grep -oE '…' | sort -u | wc -l` returns `7`), but the AC mechanism as written returns 4 and fails. This is the PF-S3-01 pattern at the meta-design layer: a mechanical check whose specified mechanism does not measure what the AC's prose intent measures.

**Cited evidence.**
- `design/health-specialist-architect-design.md:561` — AC-4 mechanism literal text.
- `design/health-specialist-architect-design.md:48` — line that enumerates all 7 identifiers inline (so `grep -c` counts it once).
- `design/health-specialist-architect-design.md:379-385` — line lines that mention 2 more identifiers, contributing 2 to the line count plus line 48 = 3, and line 561 itself adds 1 = 4 total matching lines.
- Empirical run: `grep -cE '<7-class-regex>' design/health-specialist-architect-design.md` → `4`.

**Suggested fix.** Replace `grep -cE … ≥ 7` with `grep -oE … | sort -u | wc -l` equals 7, OR rewrite as a per-identifier check (each of the 7 must match at least once). Note: the qualitative claim "7 identifiers appear" is in fact satisfied — the AC mechanism is broken, not the body.

**Independent-value note for reject-but-adopt evaluation.** The fix has value independent of the finding's framing: the same AC will fail the same way when the audit script is built (PROPOSED row #4 in §13). Adopting the fix prevents a future PF-S3-01-class recurrence at audit-script-author time.

---

### F-002 — §13 cites only 3 of 6 Research-domain INV-* despite the doc establishing they're OUT-OF-SCOPE; row 9 is mis-scoped

| Field | Value |
|---|---|
| Category | Contradictions |
| Section affected | §13 row 9; §16 scope rationale |
| Severity | **Critical** |

**Description.** §16 (lines 571–585) explicitly scopes Research-domain INV-* OUT-OF-SCOPE for the architect role, with the rationale: "this role does not dispatch `aplus-research`." But §13 row 9 (line 458) tags `aplus-research gate JSON attestation chain` as REFERENCED via INV-RESEARCH-ATTESTATION — claiming this as a live mechanical defense the architect's design doc inherits. The two cannot both be true: either the architect's design encounters INV-RESEARCH-ATTESTATION (in which case §16's OUT-OF-SCOPE claim is wrong) or it doesn't (in which case row 9 belongs in a different role's design doc, not this one). The doc's own §8.3 (line 218) forbids `aplus-research runtime dispatch` for the architect, reinforcing that row 9 is misplaced.

**Cited evidence.**
- `design/health-specialist-architect-design.md:458` — §13 row 9 tagged REFERENCED (INV-RESEARCH-ATTESTATION).
- `design/health-specialist-architect-design.md:573` — §16 scope statement: "Research-domain INV-* OUT-OF-SCOPE because this role does not dispatch `aplus-research`."
- `design/health-specialist-architect-design.md:218` — §8.3 lists `aplus-research runtime dispatch` as Forbidden.
- `INVARIANTS.md:35` — INV-RESEARCH-ATTESTATION row confirms scope = "aplus-research" (a tool the architect cannot use).

**Suggested fix.** Either (a) drop §13 row 9 entirely (the architect doesn't produce gate JSONs), or (b) restate row 9 as a REFERENCED-by-the-template (i.e., the architect's template variant references the invariant for downstream specialists who DO dispatch aplus-research) and explicitly distinguish "the architect inherits" from "the architect-designed template references." Option (b) preserves the documentation value but eliminates the scope contradiction.

**Independent-value note.** The fix's value is independent: even if a reviewer disagreed about the scope direction, the §13/§16 disagreement is empirically present and a downstream consumer (Phase 7 invariant-compliance check per §13 line 451) will read row 9 as a defense it inherits and §16 as a claim it doesn't.

---

### F-003 — "OUTBOUND" directionality semantics undefined for §4 row 6 (aplus-research as Tool)

| Field | Value |
|---|---|
| Category | Ambiguity |
| Section affected | §4 row 6 (line 125) |
| Severity | Major |

**Description.** §4's directionality column lists 7 OUTBOUND rows. Six of them establish a content claim the architect defines (taxonomy, evidence-tier scheme, etc.). Row 6 (line 125) instead says "aplus-research as first-class Tool (mode floor for compound-class targets) ... `aplus-research` SKILL.md is the source of truth for gate behavior." The architect doesn't OWN the aplus-research skill — its SKILL.md predates this design doc. Calling this an "OUTBOUND reference established by this design doc" reframes a pre-existing artifact as a Role-1-originating one. The downstream Role 2/3/4 docs that inherit "OUTBOUND from Role 1" will read this as "Role 1 owns this contract," which is false.

**Cited evidence.**
- `design/health-specialist-architect-design.md:125` — Row 6 OUTBOUND framing.
- `.claude/skills/aplus-research/SKILL.md` exists independently of this design doc (per CLAUDE.md project skill catalog).
- `design/health-specialist-architect-design.md:128` — "Anti-redefinition rule" says canonical statement lives inside this design doc — but for row 6, the canonical lives elsewhere (in SKILL.md).

**Suggested fix.** Reclassify row 6 as INBOUND-from-skills-library (or introduce a third directionality value, e.g., REFERENCED-PRE-EXISTING). Row 6's "What is being referenced" column should cite SKILL.md as the canonical source, not the architect's design doc.

---

### F-004 — Edge case missing: what happens when the Pass-1 substrate is itself defective

| Field | Value |
|---|---|
| Category | Edge Cases |
| Section affected | §14; §17.2 assumption A-1 |
| Severity | Major |

**Description.** §17.2 A-1 (line 605) names the assumption "Pass-1 substrate contains 9 Findings and 15 Recommendations" and a `breaks-if` "a future cycle revisits Pass-1 and changes Finding/Recommendation counts." But the failure mode "Pass-1 substrate contains a defect that the architect cannot patch (because Pass-1 is frozen per §10.2)" is not surfaced as an edge case. CONTINUATION_BRIEF §11 (lines 342–353) explicitly lists 4 "suspicious citations" in the Pass-1 deliverables that "must verify at first specialist authoring" — meaning Role-1's substrate is known to contain unverified citations that a downstream consumer cannot rely on. The architect role inherits these but the design doc has no Edge Case for "I cited a Finding whose underlying primary is itself flagged-for-verification."

**Cited evidence.**
- `design/CONTINUATION_BRIEF.md:342-353` — §11 suspicious URL list flags Role 1 citation [55] (Wang Y arXiv 2602.04294) as "verify before depending on."
- `design/health-specialist-architect-design.md:283` — §10.2 substrate-load rule: "read in full at dispatch start. Cite Findings by number; do NOT paraphrase."
- `design/health-specialist-architect-design.md:481-544` — §14 has 8 ECs; none address substrate-defect propagation.

**Suggested fix.** Add EC-9: "A Pass-1 Finding cites a primary that CONTINUATION_BRIEF §11 flagged for verification. Handling: the architect notes the flag inline (e.g., `Finding N (note: cited primary flagged in CB §11)`) and surfaces it as an Open Question. Test stimulus: an architect-authored §3 row whose source-line citation lands on a CB-§11-flagged primary; audit greps §3.1 source-line column against CB §11 flagged set."

---

### F-005 — EC-7 self-referential test stimulus does not actually test the handling

| Field | Value |
|---|---|
| Category | Edge Cases |
| Section affected | §14 EC-7 (lines 529–535) |
| Severity | Minor |

**Description.** EC-7's test stimulus says "A reviewer reading Role 1's design doc tries to resolve every cross-role reference without opening Role 2/3/4's docs. Expected: every OUTBOUND reference resolves to a Pass-1 Finding line range or a Role 1 design-doc section." This is the spec itself, not a test stimulus. A test stimulus per glossary §3 ("a concrete input the role must handle in the manner specified") should be reproducible by an automated check; here the check is qualitative human reading and tautological — the OUTBOUND row format is line-range-by-construction so the test cannot fail at the format layer. The failure mode this edge case names (forward-dependency at finalize time) is real, but the test stimulus as written cannot detect it.

**Cited evidence.**
- `design/health-specialist-architect-design.md:533-535` — EC-7 handling + test stimulus.
- `design/DESIGN_DOC_TEMPLATE.md:582` — glossary definition of "test stimulus" requires "a concrete input the role must handle in the manner specified."

**Suggested fix.** Replace EC-7 test stimulus with: "For each OUTBOUND row, attempt to resolve the cited Finding-N line range against `domain-research.md`; if the line range does not exist or the cited Finding ID is out of the 1–9 valid range, the reference is forward-dependent and the row fails."

---

### F-006 — §11.2 anti-pattern 4 (≤3 clarifying questions) is generic; not role-specific

| Field | Value |
|---|---|
| Category | Scope |
| Section affected | §11.2 anti-pattern 4 (line 336) |
| Severity | Minor |

**Description.** Anti-pattern 4 reads "I don't issue more than 3 clarifying questions to the user in scoping." This is a generic project-wide discipline (PF-S2-03) and is not architect-specific. The template §11.2 spec (DESIGN_DOC_TEMPLATE.md line 379) requires each entry to be "concrete `I don't X` phrasing" — satisfied — but the project rule was already encoded in CLAUDE.md and the global feedback memory `feedback_question_economy.md`. Including it here as one of only 6 anti-pattern slots (5-8 budget) crowds out a more architect-specific anti-pattern (e.g., "I don't promote a §13 row to LIVE without running Glob against the cited path" — currently spelled out in §7 but absent from §11.2).

**Cited evidence.**
- `design/health-specialist-architect-design.md:336` — anti-pattern 4 generic phrasing.
- `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-a-plus-maxing/memory/MEMORY.md` — `feedback_question_economy.md` index entry: project-wide rule, not architect-specific.
- `design/health-specialist-architect-design.md:182` — §7 Loop-Breaking has the architect-specific "audit-script LIVE-tag cap" but no parallel anti-pattern entry in §11.2.

**Suggested fix.** Replace anti-pattern 4 with an architect-specific one (e.g., "I don't tag a §13 row LIVE before running Glob/Read against the cited path"), and let the generic PF-S2-03 rule live in §5 Core Rules or §11.1 PF coverage (already covered there).

---

### F-007 — §12 BAD/GOOD pair coverage gap: anti-patterns 4 and 6 have no Negative Example

| Field | Value |
|---|---|
| Category | References |
| Section affected | §12 (lines 344–438) ↔ §11.2 (lines 328–340) |
| Severity | Major |

**Description.** §12 contains 4 BAD/GOOD pairs (12.1–12.4) mapping to §11.2 anti-patterns 1, 2, 3, 5. Anti-patterns 4 and 6 have no Negative Example. The template §12 spec (DESIGN_DOC_TEMPLATE.md line 411) requires each BAD/GOOD pair to "map to an anti-pattern from §11 (cited by anti-pattern number)" but does NOT require every anti-pattern to have a pair. However, since §11.2 has exactly 6 entries and §12 has 4, the coverage gap signals editorial: was 4-and-6 omission intentional (the pairs would be redundant) or accidental (drafter ran out)? If intentional, the design doc should explicitly note the rationale.

**Cited evidence.**
- `design/health-specialist-architect-design.md:346` — §12.1 maps to AP1.
- `design/health-specialist-architect-design.md:369` — §12.2 maps to AP2.
- `design/health-specialist-architect-design.md:391` — §12.3 maps to AP3.
- `design/health-specialist-architect-design.md:416` — §12.4 maps to AP5.
- `design/health-specialist-architect-design.md:336,340` — AP4 (≤3 questions) and AP6 (FDA prose pattern-match) lack pairs.

**Suggested fix.** Either add §12.5 and §12.6 covering AP4 and AP6, or add a single sentence in §12 preface naming the rationale for the 4-of-6 selection (e.g., "AP4 and AP6 are covered structurally by §7 loop-breaking and §13 audit script respectively; no behavioral Negative Example is operationally distinct from those mechanical defenses").

---

### F-008 — §17.1 Risk R-3 mitigates via §11.2 anti-pattern 3 but that anti-pattern targets a different failure

| Field | Value |
|---|---|
| Category | References |
| Section affected | §17.1 R-3 (line 596); §11.2 anti-pattern 3 (line 334) |
| Severity | Minor |

**Description.** R-3 names the risk "architect attempts to author actual specialist profiles rather than the template-and-audit-script meta-deliverable." Mitigation cites "§11.2 anti-pattern 3 + EC-7 reinforce." But AP3 is about operator-profile binding (Walter's Jan-2026 issue) — not about architect/Session-B role conflation. The risk maps to AP3's name only by superficial overlap of the word "operator" (the risk is about Session B, not operator binding). EC-7 is closer (forward-dependency at finalize) but also doesn't directly mitigate "architect writes specialist profiles." The mitigation citation does not actually mitigate the risk.

**Cited evidence.**
- `design/health-specialist-architect-design.md:596` — R-3 mitigation column.
- `design/health-specialist-architect-design.md:334` — AP3: operator-profile-binding-at-template-layer.
- `design/health-specialist-architect-design.md:529-535` — EC-7: cross-role forward dependency.

**Suggested fix.** Replace the AP3 citation with a citation to §2.2 "I do NOT own" item 1 (line 57, "actual agent-profile prose... owned by health-implementer Role 2"). That IS the load-bearing mitigation for R-3.

---

### F-009 — §10.3 says "sequential 6 → 9" but items 6/7/8/9 are not actually order-dependent

| Field | Value |
|---|---|
| Category | Ordering |
| Section affected | §10.3 (lines 285–290) |
| Severity | Nitpick |

**Description.** §10.3 header reads "Project-spec load (sequential 6 → 9)" implying ordering matters. The four items are DESIGN_DOC_TEMPLATE.md, INVARIANTS.md, process-failures.md, CONTINUATION_BRIEF.md. None of the listed read purposes depends on prior items' content; they are co-equal references read at dispatch start. The "sequential" label is misleading; "parallel-equivalent" or "all four required" would be honest.

**Cited evidence.**
- `design/health-specialist-architect-design.md:285-290` — §10.3 ordering language.

**Suggested fix.** Replace "sequential 6 → 9" with "required reads (any order); all four must complete before §10.4 conditional reads."

---

### F-010 — Phase Coverage Matrix claims "Phase 4 (Validation Loop) → §13, §15.2" but §13 is 10 PROPOSED rows that don't gate

| Field | Value |
|---|---|
| Category | Downstream |
| Section affected | Phase Coverage Matrix (line 694); §13 (lines 442–476) |
| Severity | Major |

**Description.** Phase Coverage Matrix says Phase 4 (Validation Loop) consumes §13 + §15.2. §13's own caveat (line 468) is explicit: PROPOSED rows "do NOT gate the resulting agent.md." 10 of 13 §13 rows are PROPOSED. So `/upgrade-agent` Phase 4 only has 3 LIVE/REFERENCED rows to consume from §13. The Phase Coverage Matrix entry "§13 has 13 rows with status tags" (line 694) is technically true but operationally misleading — Phase 4's fact-checker (per DESIGN_DOC_TEMPLATE.md §13 mapping line 450, "fact-checker verifies each LIVE row's path resolves") has 3 rows to verify, not 13. The design doc's downstream contract claims more validation coverage than it actually provides.

**Cited evidence.**
- `design/health-specialist-architect-design.md:694` — Phase 4 row in Phase Coverage Matrix.
- `design/health-specialist-architect-design.md:468` — §13 PROPOSED-does-not-gate caveat.
- `design/health-specialist-architect-design.md:450` — §13 PROPOSED rows enumerated.
- `design/DESIGN_DOC_TEMPLATE.md:450` — `/upgrade-agent` Phase 4 mapping spec.

**Suggested fix.** Rewrite Phase Coverage Matrix row for Phase 4 to be explicit: "§13 has 3 REFERENCED rows (rows 8, 9, 10) that Phase 4 fact-checker can verify; 10 PROPOSED rows do not gate. §15.2 has 7 role-specific ACs." This honesty makes downstream verification scope precise.

**Independent-value note.** Even if a reviewer claimed Phase 4 doesn't need all 13 rows, distinguishing the 3-row gating set from the 10-row aspirational set has audit value at Phase 5 finalize. Adopt independently.

---

### F-011 — §3.1 verdict "ACCEPTED" repeats 9× with no "MODIFIED" examples; raises a question about whether real synthesis occurred

| Field | Value |
|---|---|
| Category | Sycophancy Coverage |
| Section affected | §3.1 Findings table (lines 78–88) |
| Severity | Minor |

**Description.** §3.1 has 9 Findings; all 9 verdicts are ACCEPTED. Similarly §3.2's 15 Recommendations are all ACCEPTED. The template (DESIGN_DOC_TEMPLATE.md §3 spec line 169) explicitly contemplates MODIFIED verdicts with rationale. A 100% ACCEPTED-on-Findings, 100% ACCEPTED-on-Recommendations pattern is statistically plausible (the substrate cleared 99/100 rubric), but the synthesis-step verdict semantically equivalent to "no synthesis judgment was applied; copied verdict from source." This is not a defect per se but it shifts the burden: either (a) the synthesis DID apply judgment and every Finding/Recommendation passed (in which case a note explaining "all 9 reviewed; none required modification because X" would document the synthesis pass), or (b) the synthesis copied without judgment, which is the PF-S2-05 pattern. The design doc cannot tell from the current §3 alone which happened.

**Cited evidence.**
- `design/health-specialist-architect-design.md:80-88` — all 9 verdicts ACCEPTED.
- `design/health-specialist-architect-design.md:96-110` — all 15 verdicts ACCEPTED.
- `design/DESIGN_DOC_TEMPLATE.md:169` — template spec allows MODIFIED.
- `memory/process-failures.md:51-55` — PF-S2-05 pattern (operating from mental model rather than re-reading).

**Suggested fix.** Either add a one-sentence preamble before §3.1: "Synthesis judgment applied to all 9 Findings; no Finding required MODIFIED verdict because each is structural, not numerical/claim-specific" (or similar honest rationale). OR mark at least one Finding MODIFIED with rationale if the synthesis actually narrowed scope (e.g., Finding 4's three-layer convergence might warrant MODIFICATION-with-rationale since this design doc places citation-verification in Tools §8.1 rather than as a standalone first-class tool per R4).

---

### F-012 — §1 Problem Statement cites Findings 1, 2, 3, 5 but omits Finding 9 (the deliverable-triangle)

| Field | Value |
|---|---|
| Category | Language Economy |
| Section affected | §1 (lines 21–30) |
| Severity | Minor |

**Description.** §1's 4 specific gaps cite Findings 5, 2, 3, 1. Finding 9 — "the architect's deliverable is the template variant + discipline doc + audit script (triangle), not a canonical specialist profile" — is arguably the most distinctive structural commitment of the role and is referenced throughout the rest of the doc (§13, §15 AC-1, §17 R-1, §17 R-3, OQ-1). It is the load-bearing "what makes this role NOT just an opinionated agent-template-author" anchor. Omitting it from §1 means the reader's 30-second framing is missing the deliverable-shape claim.

**Cited evidence.**
- `design/health-specialist-architect-design.md:21-30` — §1 cites Findings 5, 2, 3, 1.
- `design/health-specialist-architect-design.md:88` — Finding 9 in §3.1.
- `design/health-specialist-architect-design.md:594-595` — §17 R-1 + R-2 reference Finding 9 as load-bearing.

**Suggested fix.** Add a 5th gap to §1: "Deliverable triangle (template variant + discipline doc + audit script) — software roles produce code or reviews; the architect produces three composable artifacts that together gate the 14 downstream specialists. Source: Finding 9 (`domain-research.md` L256–L350)."

---

### F-013 — "OUTBOUND" framing forces row 4 (operator-profile precondition) to count 11 specialists; CB §10 says "Role 2 R7, Role 3 R7, Role 4 R10"

| Field | Value |
|---|---|
| Category | Contradictions |
| Section affected | §4 row 4 (line 123) |
| Severity | Major |

**Description.** §4 row 4 lists counterpart roles as "Roles 2, 3, 4 + 11 specialists that write to `vault/compounds/`." CONTINUATION_BRIEF §10 row 7 (line 336) frames the same reference as flowing into "Role 2 R7, Role 3 R7, Role 4 R10" — i.e., it's a 3-role inheritance, not an 11-specialist inheritance, at the foundation-role layer. The 11-specialists framing extends the inheritance past CB §10's enumeration. The design doc may be correct that 11 specialists eventually inherit the contract, but the CB §10 row it cites does NOT contain that downstream extension. The OUTBOUND row's specialist-count claim cannot be sourced to CB §10 as cited.

**Cited evidence.**
- `design/health-specialist-architect-design.md:123` — §4 row 4 counterpart-roles column.
- `design/CONTINUATION_BRIEF.md:336` — CB §10 row 7 enumeration ("Role 2 R7, Role 3 R7, Role 4 R10").
- `design/health-specialist-architect-design.md:30` — §1 gap 4 cites "Finding 1 (L63–L82), R7" — the substrate citation, not CB §10, for the 11-specialist scope.

**Suggested fix.** Split row 4 into two assertions: (i) OUTBOUND to Roles 2/3/4 per CB §10 row 7 (the foundation-inheritance contract), (ii) OUTBOUND to compound-writing specialists per the architect's design intent (a separate forward-dependency that CB §10 doesn't pre-establish). Alternatively, cite the architect's own §2.2 item 1 as the source for the 11-specialist scope instead of CB §10.

---

### F-014 — §11.1 PF-S6-01 rationale doesn't address the precise failure mode

| Field | Value |
|---|---|
| Category | Sycophancy Coverage |
| Section affected | §11.1 PF-S6-01 row (line 326) |
| Severity | Minor |

**Description.** PF-S6-01 (per `memory/process-failures.md` lines 79–89) is the "act-before-verify on prior-session-described state" failure (the beads cleanup near-miss). §11.1 row marks it IN-SCOPE with rationale: "Architect reads HANDOFF.md + CONTINUATION_BRIEF.md + Pass-1 substrate, all describing state of upstream work. Acting on 'the Pass-1 Finding said X' without re-reading the cited line in `domain-research.md` is the recurrence." This conflates PF-S6-01 (act on prior-state without verification) with PF-S2-05 (operate from mental model rather than re-read protocol). The two are distinct failure modes per the PF log; PF-S6-01's load-bearing recurrence guard is "is the described problem still real?" — verifying STATE not protocol-memory. The architect's analog of PF-S6-01 would be: act on a HANDOFF claim that "the substrate Finding count is 9" without re-running the count. The current rationale describes PF-S2-05 with PF-S6-01's name.

**Cited evidence.**
- `design/health-specialist-architect-design.md:326` — PF-S6-01 row rationale.
- `memory/process-failures.md:79-89` — PF-S6-01 actual failure mode.
- `memory/process-failures.md:51-55` — PF-S2-05 actual failure mode (the one the rationale actually describes).

**Suggested fix.** Rewrite PF-S6-01 rationale to be state-verification-specific: "Architect's `last-PF-reviewed:` frontmatter pin assumes the PF log state at draft time. PF-S6-01 recurrence: assuming `memory/process-failures.md` is still at PF-S6-01 latest at finalize time without re-running `tail -1 memory/process-failures.md`. The mitigation is the Phase-5 re-read (see §17.1 R-5)."

---

### F-015 — §13 row 3 OR's three regex matches "into single fail" — semantically inverted

| Field | Value |
|---|---|
| Category | Ambiguity |
| Section affected | §13 row 3 (line 452) |
| Severity | Minor |

**Description.** Row 3 reads: "Core Rules + Anti-Patterns + Negative Examples contain all three regex matches (anti-sycophancy, maintain-position-without-new-evidence, user-supplied-text-not-numerical) | … three independent grep checks; OR'd into single fail". An OR of three checks "into single fail" means: any one match → fail. But the row's intent is to verify ALL THREE patterns are present (Three-mechanism anti-sycophancy per R3/R10/R11). The logical operator should be AND-negated (fail if ANY of the three grep counts is 0), not OR'd. As written, the row would fail when only one of the three is missing — except "OR'd into single fail" is the wrong English for "any one missing = fail."

**Cited evidence.**
- `design/health-specialist-architect-design.md:452` — row 3 mechanism column.
- `design/health-specialist-architect-design.md:140` — Core Rule 2 establishes three-mechanism requirement.

**Suggested fix.** Replace "OR'd into single fail" with "fail if ANY of the three grep counts == 0; pass requires all three ≥ 1."

---

### F-016 — §17 has 6 risks in §17.1 but template budget is 3-7; six is at upper end with one merge-candidate

| Field | Value |
|---|---|
| Category | Language Economy |
| Section affected | §17.1 R-4 and R-5 (lines 597–598) |
| Severity | Nitpick |

**Description.** R-4 (paraphrase-vs-line-range-citation in design doc) and R-5 (last-PF-reviewed pin going stale) are both about citation freshness at finalize time. They could be merged into a single risk "Citation/PF-pin freshness at finalize" with one mitigation (the orchestrator's Phase-5 re-read of substrate AND PF log). Keeping them separate is not wrong but at 6/7 of the template's budget, every row should earn its slot.

**Cited evidence.**
- `design/health-specialist-architect-design.md:597` — R-4.
- `design/health-specialist-architect-design.md:598` — R-5.

**Suggested fix.** Merge if total budget pressure (template says 3-7, current is 6); keep separate if budget allows. Defer to orchestrator's editorial judgment.

---

### F-017 — §5 Core Rule 12 collapses two axes the rule itself says must not collapse (recursive editorial defect)

| Field | Value |
|---|---|
| Category | Language Economy |
| Section affected | §5 Rule 12 (line 160) |
| Severity | Minor |

**Description.** Core Rule 12 says: "Every claim-emitting section requires a GRADE certainty tag (high/moderate/low/very-low) and a recommendation-strength tag (strong/weak/conditional). … The architect does not collapse the two axes into a single 'evidence rating.'" But the rule's title — "GRADE certainty + recommendation strength is the medical equivalent of static types" — performs the collapse it forbids by using "+" to compound the two into a single rule-name. The bullet body is correct; the title editorially fuses what the body separates. A reader who skims rule titles only would internalize the collapse as the rule.

**Cited evidence.**
- `design/health-specialist-architect-design.md:160` — Rule 12 full text.

**Suggested fix.** Rename rule 12 to "GRADE two-axis tagging is the medical equivalent of static types" (the word "two-axis" preserves the distinction the rule body enforces).

---

### F-018 — §8.4 names PF-S2-06 as OUT-OF-SCOPE structural, but the rationale relies on hooks the architect doesn't enforce

| Field | Value |
|---|---|
| Category | Role Discipline |
| Section affected | §8.4 (lines 224–226); §11.1 PF-S2-06 (line 324) |
| Severity | Minor |

**Description.** §8.4 says PF-S2-06 is OUT-OF-SCOPE structural because "Architect's Bash use forbids state-mutating git. Branch hygiene is enforced at the orchestrator layer via `block-commit-main.sh` + `block-push-main.sh` PreToolUse hooks." The "structural" framing implies the architect *cannot* commit on main even if it tried. But the hooks belong to the *orchestrator's* environment — when the architect dispatches via Bash, the hooks apply because they're system-wide PreToolUse Bash hooks. If a future architect tool palette restricts Bash entirely (which §8.1 does NOT), the structural argument from tool restriction would hold. The current claim is true but for a different reason than stated: it's the hooks that prevent it, not the architect's own §8.3 forbid-list (which forbids "state-mutating git commands" — a rule the architect would have to self-enforce since the architect *can* run Bash). The "structural" label is half-correct: structurally-via-orchestrator-hooks, behaviorally-via-self-enforcement.

**Cited evidence.**
- `design/health-specialist-architect-design.md:225-226` — §8.4 reasoning.
- `design/health-specialist-architect-design.md:197` — §8.1 Bash entry: "MAY NOT run any state-mutating git command" (self-enforcement clause).
- `.claude/hooks/block-commit-main.sh` — exists; PreToolUse Bash hook (verified).
- `INVARIANTS.md:43` — INV-BRANCH-NOT-MAIN: enforced via both hooks.

**Suggested fix.** Rewrite §8.4 PF-S2-06 rationale: "OUT-OF-SCOPE — defense-in-depth structural. (a) Architect's §8.1 Bash entry self-forbids state-mutating git; (b) project-level PreToolUse hooks (`block-commit-main.sh` + `block-push-main.sh`) catch any violation that bypasses (a). Two-layer protection makes PF-S2-06 structurally unreachable from this role."

---

### F-019 — Identity sentence (§2.1) is 41 words; spec is ≤40

| Field | Value |
|---|---|
| Category | Role Discipline |
| Section affected | §2.1 (line 38) |
| Severity | Nitpick |

**Description.** §2.1 Identity reads: "You are the health-specialist-architect. You receive medical-LLM design problems from the orchestrator and deliver a template variant of `AGENT_TEMPLATE.md`, per-section interface contracts, and an audit script that mechanically gates the 14 downstream specialist profiles." Word count of the function sentence (excluding the "You are the X" name slot per template §2 spec line 149): "You receive medical-LLM design problems from the orchestrator and deliver a template variant of `AGENT_TEMPLATE.md`, per-section interface contracts, and an audit script that mechanically gates the 14 downstream specialist profiles." = 33 words. INCLUDING the name slot it's 38 words. R1 (line 352 of substrate) explicitly says "Identity section is a single declarative sentence under 40 words" — current passes either count. **No defect — this finding is withdrawn after verification.** Retained in the report so the orchestrator sees the count was personally verified.

**Cited evidence.**
- `design/health-specialist-architect-design.md:38` — Identity sentence.
- Personally counted: 33-38 words depending on whether the role-name slot is included. Both under 40.

**Suggested fix.** No fix required. This finding documents that the verification was performed.

---

### F-020 — §5 Rule 6 first-person rule risks RLHF-preference-drift recognition gap

| Field | Value |
|---|---|
| Category | Sycophancy Coverage |
| Section affected | §5 Rule 6 (line 148) |
| Severity | Minor |

**Description.** Rule 6 says "Every time I've folded a reviewer comment that re-stated my prior framing in different words, I have lost a load-bearing structural constraint and discovered the loss later in a downstream consumer. Now I treat reviewer pushback as a request for cited evidence; if no new evidence is supplied I restate my position and the evidence behind it." This addresses Sycophancy Mechanism B (single-model user acquiescence). However, Mechanism C (RLHF preference drift, per Finding 3) has no analogous Core Rule guard. The architect itself runs on an RLHF-trained model; the same drift the architect is encoding template defenses against will affect the architect's own outputs. Rule 6 catches reviewer-driven folding; it doesn't catch baseline drift in the absence of pushback (e.g., the architect autonomously softening a refusal-class definition because the RLHF-tuned tone preference favors hedged language).

**Cited evidence.**
- `design/health-specialist-architect-design.md:148` — Rule 6.
- `design/health-specialist-architect-design.md:140` — Rule 2 mentions all three mechanisms but as template defaults for downstream specialists, not as architect-self defenses.
- `design/.health-specialist-architect-design-work/domain-research.md:108-129` — Finding 3 (cited per design doc line 82).

**Suggested fix.** Add a Rule 6b (or expand Rule 6): "I do not soften refusal-class definitions, statutory-citation thresholds, or anti-sycophancy clauses between drafts in the absence of new evidence; baseline-softening is the architect-internal recurrence of Mechanism C."

---

### F-021 — §9.3 sample to-user output uses "What works / What remains" structure but §9.1 to-orchestrator structure is different; cross-audience tone inconsistency unaddressed

| Field | Value |
|---|---|
| Category | Role Discipline |
| Section affected | §9.1 vs §9.3 |
| Severity | Nitpick |

**Description.** §9.1 (orchestrator-bound) format spec lists 7 fields (Status, Artifact paths, Coverage tally, etc.). §9.3 (user-bound) sample output uses a "What works / What remains" structure. Both are valid format specs per template §9 (shapes b and a respectively). But the design doc has no statement that §9.1 fields should NEVER appear in §9.3 outputs (e.g., a user-facing message accidentally including "Mechanical-check status:" field). This is a minor scope-of-audience clarity gap.

**Cited evidence.**
- `design/health-specialist-architect-design.md:236-243` — §9.1 fields.
- `design/health-specialist-architect-design.md:256-267` — §9.3 sample.

**Suggested fix.** Add one sentence to §9.3: "The fields enumerated in §9.1 are orchestrator-internal; they MUST NOT appear in user-facing outputs."

---

### F-022 — §13 row 13 status is WARN-conditional-on-future-policy; ambiguity about who flips it to BLOCK

| Field | Value |
|---|---|
| Category | Mechanical Enforcement Claim Integrity |
| Section affected | §13 row 13 (line 462) |
| Severity | Minor |

**Description.** Row 13 (auditable named modes, R15) has consequence "WARN (escalates to BLOCK if Modes-section-required policy is locked)." Who locks the Modes-section-required policy? The design doc references no decision artifact for this transition. If the answer is "Session B's `/upgrade-agent` Phase 5 decides per-role whether Modes materializes" (per DESIGN_DOC_TEMPLATE.md §5 line 626), then the BLOCK/WARN decision is made downstream of this design doc and shouldn't be a §13 status-tag. If the answer is "the architect locks it via a decision ADR," the ADR doesn't exist.

**Cited evidence.**
- `design/health-specialist-architect-design.md:462` — row 13 consequence.
- `design/DESIGN_DOC_TEMPLATE.md:626` — `/upgrade-agent` Phase 5 decides Modes materialization per role.
- `vault/decisions/` — no Modes-required ADR (verified via prior session work; CB §17 Q4 acknowledges absent decision files in adjacent area).

**Suggested fix.** Either (a) drop the conditional and tag row 13 simply WARN (the BLOCK promotion is a future decision point), or (b) add an Open Question (OQ-7) capturing the Modes-section-required policy decision with explicit owner = orchestrator / Walter.

---

### F-023 — §3.2 R5 says "KG-grounded retrieval enumerated in Context Loading; free-form web search forbidden" — but Context Loading §10 has no explicit forbid clause

| Field | Value |
|---|---|
| Category | Downstream |
| Section affected | §3.2 R5 (line 100); §10 |
| Severity | Major |

**Description.** §3.2 marks R5 ACCEPTED. R5's substrate (domain-research.md line 360) reads: "Context Loading enumerates KG/wiki paths the specialist consults; free-form web search is forbidden." The ACCEPTED verdict commits the design doc to implementing both halves. §10 (Context Loading Protocol) enumerates vault/library paths in §10.1 — the KG-grounded half. But §10 contains no clause forbidding free-form web search. §8.3 forbids `tavily`/`WebSearch`/`WebFetch` for the architect, which covers the architect's own behavior but NOT the template defaults for downstream specialists (which is what R5 is about — the template the architect designs). The R5 ACCEPTED verdict claims a commitment the design doc does not deliver against the downstream-template surface.

**Cited evidence.**
- `design/health-specialist-architect-design.md:100` — R5 ACCEPTED.
- `design/.health-specialist-architect-design-work/domain-research.md:360` — R5 text: forbids free-form web search.
- `design/health-specialist-architect-design.md:272-308` — §10 has no forbid clause.
- `design/health-specialist-architect-design.md:212` — §8.3 forbids web search for the ARCHITECT, not for the template's downstream specialists.

**Suggested fix.** Either (a) downgrade R5 to MODIFIED with rationale "R5's forbid-clause half is delegated to the template variant artifact (`templates/medical-specialist-AGENT_TEMPLATE.md`), not encoded in this design doc's §10," or (b) add a §10.7 clause: "The template variant's Context Loading default MUST include a forbid-clause for free-form web search by the specialist; the architect inherits R5's forbid-clause requirement via the template-artifact deliverable, not via this design doc's §10 (which describes the architect's own loading, not the specialist's)."

---

## Mechanical Coverage Check 1: AGENT_TEMPLATE.md 10-base-section coverage

Per dispatch contract: verify every AGENT_TEMPLATE.md base section has at least one upstream design-doc section.

Source of truth: `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` (97 lines). The 10 base sections (verified by `grep -n '^## '`):

| # | AGENT_TEMPLATE.md section | Design-doc upstream | Status |
|---|---|---|---|
| 1 | Identity | §2.1 + §1 (problem framing) | PASS |
| 2 | Core Rules | §5 (12 rules with voice + source tags) | PASS |
| 3 | Role Boundaries | §2.2 + §4 (cross-role escalations) | PASS |
| 4 | Ask vs Proceed | §6 (6-step decision tree + fabrication guard) | PASS |
| 5 | Loop-Breaking | §7 (5 thresholds) | PASS |
| 6 | Tools | §8 (permitted + skills + forbidden + PF coupling) | PASS |
| 7 | Communication | §9 (9.1 orchestrator + 9.2 downstream + 9.3 user) | PASS |
| 8 | Context Loading | §10 (10.1 auto + 10.2 substrate + 10.3 spec + 10.4 conditional + 10.5 skip + 10.6 cross-role) | PASS |
| 9 | Anti-Patterns | §11.1 PF coverage + §11.2 role-specific | PASS |
| 10 | Negative Examples | §12 (4 BAD/GOOD pairs) | PASS — see F-007 (coverage gap for AP4/AP6) |

**Result: 10/10 base sections have at least one upstream. PASS with F-007 noted.**

Role-specific "Modes" section (11th expected by `enforce-role-inlining.sh` hook): per DESIGN_DOC_TEMPLATE.md §5 line 626, Modes is a Phase-5 synthesis emergent output from §5+§9+§14; design doc does not need a dedicated upstream. This is consistent with the doc's design.

---

## Mechanical Coverage Check 2: `/upgrade-agent` 8-phase coverage

Per dispatch contract: verify every `/upgrade-agent` phase has at least one upstream design-doc section feeding it.

Source: the design doc's own Phase Coverage Matrix (lines 685–700) plus cross-check against DESIGN_DOC_TEMPLATE.md §4 (line 591).

| Phase | Expected upstream (per template §4) | Design doc provides | Status |
|---|---|---|---|
| 1 (Baseline Evaluation) | §1, Appendix A | §1 present; Appendix A empty placeholder (Phase 3 pending — this dispatch) | PASS (Appendix A will populate from this report) |
| 2 (Rubric Construction) | §15 (Acceptance Criteria) | §15.1 inherited reference + §15.2 with 7 binary ACs | PASS — see F-001 (AC-4 mechanism defect) |
| 3 (Research Agents) | §5 Core Rules + §11 Anti-Patterns | §5 has 12 rules; §11 has 8-PF coverage + 6 role-specific anti-patterns | PASS |
| 4 (Validation Loop) | §13 Mechanical Map + §15.2 | §13 has 3 REFERENCED + 10 PROPOSED rows; §15.2 has 7 ACs | PASS WITH CAVEAT — see F-010 (only 3 LIVE/REFERENCED rows actually gate) |
| 5 (Synthesis) | §2, §4, §5, §6, §7, §8, §9, §10, §11, §12, §13, §17 | All 12 sections present | PASS |
| 6 (Adversarial Review) | §4 Cross-Role + §14 Edge Cases | §4 has 7 OUTBOUND rows; §14 has 8 ECs | PASS — see F-004 (missing substrate-defect EC), F-005 (EC-7 test stimulus weak) |
| 7 (Final Corrections) | §13 LIVE checks + §15.1 inherited + §16 Invariants | §13 has 3 REFERENCED rows; §15.1 references upgrade-agent Phase 7; §16 has 6 in-scope invariants | PASS — see F-002 (row 9 mis-scoped against §16) |
| 8 (Close Out) | §18 Open Questions + Appendix A | §18 has 6 OQs; Appendix A pending Phase 3 dispatch | PASS |

**Result: 8/8 phases fed. PASS with caveats from F-001, F-002, F-004, F-005, F-010.**

---

## Notes for orchestrator Phase 4 verification

1. **Critical findings (F-001, F-002).** Both are mechanical-defect class. F-001 will be empirically confirmable by running the cited `grep -c` command. F-002 will be confirmable by reading §13 row 9 and §16 scope statement side-by-side.

2. **Reject-but-adopt candidates surfaced.** F-001 and F-010 carry explicit "independent value" notes per `feedback_reject_but_adopt_pattern.md`. Even if the orchestrator disagrees with the framing (e.g., "the AC's intent is clear, mechanical literalism is uncharitable"), the proposed fix (replace `grep -c` with the unique-identifier count) has audit value at script-author time. Apply the same lens to F-010.

3. **F-019 self-withdraws.** The Identity word-count check passed when the reviewer counted personally. Retained in the report so the orchestrator sees the verification path was walked, not skipped.

4. **No findings in:** Cross-role-reference fabrication (zero-tolerance per §7), §3 count fidelity (9 Findings + 15 R verified), `last-PF-reviewed` frontmatter (PF-S6-01 verified as latest PF in log).

5. **Findings the orchestrator should NOT auto-accept (Quant Phase-4 rule).** Per design-doc-protocol Phase 4: each finding gets a personal read. The Critical + Major set (10 findings) is highest-leverage; the Minor + Nitpick set may compress or reject under editorial judgment, but cite the rejection evidence per PF-S3-01.
