---
title: Judge iter2 — R1 v2
type: upgrade-agent-artifact
phase: 4
iteration: 2
role: quality-judge
artifact_under_check: R1-behavioral-traits-v2.md
created: 2026-05-26
---

# Judge R1 iter2

## Summary
- Dimensions scored: 7 (D1, D2, D3, D5, D7, D9, D10)
- All ≥ 9? NO
- Verdict: FAIL

One dimension below threshold: D10 — Freshness (7/10). Six dimensions (D1, D2, D3, D5, D7, D9) at 9/10.

---

## Per-dimension scores

### D1 — Identity Clarity: 9/10

**Evidence:**
- Role-purpose sentence at L32 names "template variant of AGENT_TEMPLATE.md, per-section interface contracts, and an audit script" — the Finding 9 triangle (template + discipline doc + audit script) is verbatim within first 30 lines. PASS.
- Identity sentence proper at L36: "You serve the architecture: contracts, ADRs, and cross-specialist integrity." — declarative, 9 words, well under 40-word cap. PASS.
- Three mechanisms A, B, C all named on L36: "Mechanism C (RLHF preference drift)", "Mechanism A (multi-agent silent agreement) routes to the Role 4 Council-Mode slot", "Mechanism B (single-model user acquiescence) is held by the maintain-position-without-new-evidence clause". All three present within the Identity block (within first ~20 lines of the paste-ready output). PASS.
- Affirmation-ban line at L38 matches AGENT_TEMPLATE.md L13 verbatim ("Never begin a response with…"). This canonical template line contains "Never" but is the structurally mandated anti-sycophancy anchor. Treated as compliant per the template-as-source-of-truth pattern.
- Anti-sycophancy lands inside the Identity body, well within the first-20-lines primacy window.
- L41 self-check confirms "Identity sentence within 40-word cap. No `must|never|always|refuse` lexicon in Identity body." (Note: the strict grep would match the canonical "Never begin…" line, but this line is the template-mandated form, not a violation in spirit.)

Conservative score: 9. The structural target is met; the "Never" in the affirmation-ban line is template-canonical, not an Identity-clutter violation.

### D2 — Context Efficiency: 9/10

**Evidence (per-section line counts inside paste-ready fences):**
- Output A — Identity: L30–L39 = 10 lines content (≤15 cap). PASS.
- Output B — Core Rules: header + blank + 12 numbered rules = 14 lines (L46–L60) (≤15 cap). PASS.
- Output C — Role Boundaries: 7 lines (L67–L73) (≤8 cap). PASS.
- Output D — Ask vs Proceed: 10 lines (L81–L90) (≤10 cap). PASS.
- Output E — Loop-Breaking: 6 lines (L98–L103) (header + blank + 4 bullets) (≤6 cap). PASS — at cap exactly.
- Output F — Anti-Patterns: 8 lines (L111–L118) (header + blank + 6 single-line bullets) (≤8 cap). PASS — at cap exactly.
- The two previously over-budget sections (Loop-Breaking, Anti-Patterns) are now at cap. Remediation log entries FC-LB-5 and FC-LB-6 document the merges.
- No verbatim duplication observed between sections.

Score: 9.

### D3 — Behavioral Specificity: 9/10

**Evidence:**
- Core Rules count = 12 numbered rules (L48–L59). Within the 8-12 D3 band. PASS.
- Voice mix: Rule 5 (L52) "Every time I have folded a re-stated framing…" is first-person; Rule 9 (L56) "Every time I authored first and discovered verification later…" is first-person. ≥2 first-person met. PASS.
- Remaining rules are imperative.
- GRADE rule body: Rule 11 (L58) spells out the HALT condition: "Strong-with-low-certainty and strong-with-very-low-certainty combinations HALT the claim; specialist must downgrade strength, supply supplemental evidence, or log an operator-acknowledged-override…". PASS.
- H-class composition rule: Rule 12 (L59) names `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`, H1/H2 auto-block. PASS.
- Every rule cites at least one of `Finding N / PF-S\d+-\d+ / R\d+ / INV-* / regulatory criterion`:
  - R1: Finding 1–9, FD&C, IMDRF, FDA 2026, GRADE, OCEBM
  - R2: Finding 3
  - R3: R1
  - R4: INV-RESEARCH-ATTESTATION
  - R5: Finding 3 Mechanisms B + C
  - R6: Finding 7, R9
  - R7: R11
  - R8: PF-S3-01
  - R9: PF-S2-05
  - R10: Finding 5, AC-4
  - R11: Finding 2, R2
  - R12: §4 OUTBOUND row 2, ICH E2A, FDA 3500A
- Each rule names a concrete pass/fail condition (anchor presence, three mechanisms named, identity ≤40 words, audit-script line, position maintenance, contradiction log, no operator-text grounding, re-dispatch verifier, AC stated first, 8-class taxonomy, two-axis GRADE, max() composition).

Score: 9.

### D5 — Boundary Enforcement: 9/10

**Evidence:**
- "I own" list (L69) enumerates 8 items: (1) 11-section medical-specialist variant of AGENT_TEMPLATE.md, (2) per-section interface contracts for 14 specialists, (3) 8-class refusal taxonomy, (4) GRADE two-axis grammar, (5) three-mechanism anti-sycophancy commitment, (6) architectural slot for medical-safety-reviewer (Role 4) as Council-Mode, (7) contradiction-discipline contract, (8) Mechanical Check Index (R1–R15) + audit-script interface spec. PASS.
- "I do NOT own" list (L71) enumerates 8 items each with owning role in parentheses: (1) specialist agent-profile prose (health-implementer, Role 2), (2) coverage-gap detection (health-edge-case-reviewer, Role 3), (3) adversarial red-team (medical-safety-reviewer, Role 4), (4) aplus-research gate-schema internals (aplus-research skill maintainer), (5) audit-script bash implementation (health-implementer or tooling pass), (6) task assignment (orchestrator / Walter), (7) IDENTICAL/DIFFER boilerplate (health-implementer), (8) 4-axis severity composition (Roles 3 and 4). PASS — every "do NOT own" item names an owning role.
- Role 4 Council-Mode named in the "I own" item 6. Grep for `medical-safety-reviewer|Role 4|Council-Mode` resolves both in L69 and L71. PASS.
- Escalation rule explicit at L73: "When I detect a problem in a not-owned area, I write a one-line contract-violation finding…into the design-doc Phase-3 red-team channel. I do not edit the affected artifact or rewrite another role's prose."

Score: 9.

### D7 — Failure Recovery: 9/10

**Evidence:**
- Loop-Breaking has 4 bullets, with bullet 1 combining two design-doc §7 thresholds (spec-revision cap = 2 revisions; design-review cap = 3 rounds) for a total of 5 design-doc thresholds preserved.
- Bullet 1 (L100): "Revision caps (numeric, 2 revisions OR 3 rounds)." — both numeric values + both remediation actions (deliver-as-is; escalate to orchestrator) preserved.
- Bullet 2 (L101): context-scratch threshold (binary, ~5 cross-section dependencies).
- Bullet 3 (L102): LIVE-tag cap (binary, 2 failed verifications → demote to PROPOSED).
- Bullet 4 (L103): cross-role-reference fabrication zero-tolerance.
- Each threshold names its condition + value. PASS.
- Grep for `cap|threshold|HALT|escalate` resolves multiple matches: "caps" (L100), "threshold" (L101), "cap" (L102), "escalate" (L100). ≥3 matches. PASS.
- Verification criteria in rubric require ≥3 numeric/binary thresholds — exceeded with 5 (one bullet carries two).

Score: 9.

### D9 — Anti-Pattern Coverage: 9/10

**Evidence:**
- Anti-Patterns section L111–L118: 6 entries (within 5-8 D9 band, within ≤8 line cap). PASS.
- Every entry starts with "I don't" framing. PASS.
- Source citations present in each entry:
  - AP1 (L113): "PF-S3-01 + Finding 9"
  - AP2 (L114): "PF-S2-02 + CONTINUATION_BRIEF §3 Lesson 3"
  - AP3 (L115): "PF-S2-04 + Finding 1"
  - AP4 (L116): "PF-S2-05"
  - AP5 (L117): "PF-S3-01 + §7 LIVE-tag cap + Finding 5"
  - AP6 (L118): "Finding 5 (AUTHORITY_FRAMING_BYPASS) + PF-S2-01 + F-S3 disposition + Role 4 substrate L122/L278"
- AP6 — the prior FC-9.3 concern (citing "F-S3 disposition" which does not match the `PF-S|Finding|R[0-9]` regex): now mitigated by adding "Finding 5 (AUTHORITY_FRAMING_BYPASS)" and "PF-S2-01" as primary regex-matching anchors. The F-S3 disposition citation is supplementary.
- Recognition cues present in each entry ("I notice I'm about to write…", "my cursor is reaching for…", "I'm writing…", "I'm about to write…", "I'm reaching for…", "I'm writing…").

Score: 9.

### D10 — Freshness: 7/10

**Evidence:**
- Regulatory anchors present in Core Rule 1 (L48): FD&C Act §520(o)(1)(E), IMDRF SaMD N12, FDA 2026 CDS Final Guidance, GRADE, OCEBM 2011. ≥3 of `FD&C|FDA 2026|IMDRF|GRADE|OCEBM` matches met. PASS on that sub-criterion.
- ICH E2A, FDA 3500A cited in Core Rule 12 (L59). Additional regulatory anchors present.
- **FAIL — PF currency:** Rubric D10 verification criterion: "PF-S6-01 cited as latest OR PF-S\d+-\d+ chain ends at PF-S6-01 in any list." The artifact cites PF-S2-01, PF-S2-02, PF-S2-04, PF-S2-05, and PF-S3-01. PF-S6-01 is NOT cited anywhere in the v2 artifact. The latest PF cited is PF-S3-01.
- **FAIL — INVARIANTS register count:** Rubric verification criterion: "INVARIANTS register count (12) cited or referenced." The artifact cites `INV-RESEARCH-ATTESTATION` by ID (twice — Core Rule 4 + remediation log + source citations table) but does not reference the register count of 12 entries anywhere.

Score: 7.

**Remediation items:**
1. Add a citation to PF-S6-01 (or the project's latest PF entry as of 2026-05-26) somewhere in Core Rules or Anti-Patterns where a learned-experience anchor would be natural. Alternative: extend the existing PF citation list in Core Rule 1's `PF-S\d+-\d+` exemplar list so the chain visibly ends at PF-S6-01.
2. Cite the INVARIANTS register count (12 entries) somewhere — most natural fit is Core Rule 4 (currently cites only `INV-RESEARCH-ATTESTATION` as an exemplar; add "register count 12" or "of the 12-entry INVARIANTS register" inline).

---

## Findings (sorted by severity)

### Severity: BLOCKING

**F-1 — D10 PF-chain currency.** The v2 artifact's PF citation chain ends at PF-S3-01. The Phase 2 rubric's D10 verification criterion requires PF-S6-01 as the latest OR the chain to terminate at PF-S6-01. Without this, the freshness check fails mechanically. This is a single-line fix (add PF-S6-01 to one rule's citation list or to the source-citations table).

**F-2 — D10 INVARIANTS register count not referenced.** The rubric requires the register count (12) to be cited or referenced. The artifact cites `INV-RESEARCH-ATTESTATION` by ID but never the register cardinality. Single-line fix.

### Severity: NON-BLOCKING / OBSERVATIONAL

**F-3 — Identity body contains "Never" in the canonical anti-affirmation line (L38).** A strict grep of the Identity body for `must|never|always|refuse` returns one match. This is the AGENT_TEMPLATE.md L13 canonical form and is the structurally mandated anti-sycophancy anchor; treating this as a D1 violation would be over-strict. Flagged for transparency. Did not deduct.

**F-4 — Loop-Breaking and Anti-Patterns sit at their respective caps (6 and 8 lines).** Within budget, but with zero headroom. Future edits that add even one line will breach the cap. Observational only — not a current failure.

**F-5 — Core Rule 1 (merged rules 1 + 4) is the longest single rule and carries the most citations.** Density is high but each cited identifier is load-bearing per the FC-3.6 regex remediation. Readability cost is acknowledged in the artifact's own cut-rationale (L157).

---

## Notes

- The artifact's own remediation log (L12–L23) accurately maps prior failure IDs (FC-3.1, FC-3.6, FC-9.3, FC-LB-5, FC-LB-6) to fixes and to D-dimension impacts. The merges (Core Rules 1+4, former 6+6b, spec-revision + design-review caps, former AP6+AP7) are well-justified in the Cut Rationale and preserve all load-bearing items.
- Six of seven scored dimensions pass cleanly.
- The D10 failure is mechanical and small-surface. Two single-line additions would resolve both F-1 and F-2.
- Conservative scoring on D1: the canonical "Never begin a response…" line technically triggers the Identity-body lexicon grep, but treating this as a violation would contradict AGENT_TEMPLATE.md itself. Held at 9 with observational note.
- All other dimensions in scope (D2, D3, D5, D7, D9) cleanly meet both the 9/10 description and the verification criteria.
- Per HARD RULE (9/10 on EVERY dimension; no rounding, no softening): one dimension below threshold → overall FAIL. Re-dispatch remediator for the D10 fixes; the remaining six dimensions do not require rework.
