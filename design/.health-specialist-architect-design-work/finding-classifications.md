---
title: Phase 4 Verification — Finding Classifications for health-specialist-architect Pass-2 Design Doc
type: phase-4-orchestrator-verification
target: design/health-specialist-architect-design.md
red_team_inputs:
  - design/.health-specialist-architect-design-work/red-team-adversarial.md (23 findings)
  - design/.health-specialist-architect-design-work/red-team-safety.md (15 findings)
created: 2026-05-26
guard: PF-S3-01 — orchestrator personally verified each finding against cited source before classification
classifications:
  legitimate: 26
  legitimate-modified: 11
  rejected: 1
total: 38
---

# Finding Classifications — Phase 4 Orchestrator Verification

Per `feedback_reject_but_adopt_pattern.md`: judge the claim and the fix independently. REJECTED with cited evidence does not preclude adopting a fix that has independent value.

## Summary

| Verdict | Count | Findings |
|---|---|---|
| LEGITIMATE | 26 | F-001, F-002, F-004, F-005, F-008, F-010, F-012, F-013, F-015, F-017, F-020, F-022; F-S1, F-S2, F-S3, F-S4, F-S5, F-S6, F-S7, F-S8, F-S9, F-S10, F-S11, F-S13, F-S14, F-S15 |
| LEGITIMATE-MODIFIED | 11 | F-003, F-006, F-007, F-009, F-011, F-014, F-016, F-018, F-021, F-023; F-S12 |
| REJECTED | 1 | F-019 (self-withdrawn by reviewer after personal recount) |
| **Total** | **38** | — |

---

## Adversarial findings (23)

### F-001 — AC-4 grep returns lines not unique identifiers — LEGITIMATE
**Verification.** Empirically confirmed. Ran `grep -cE '<7-class-regex>' design/health-specialist-architect-design.md` → returns `4`. Ran `grep -oE '<...>' | sort -u | wc -l` → returns `7`. The mechanism as written returns 4; the qualitative claim "7 identifiers appear" is satisfied (7 unique identifiers do appear), but the AC's mechanism does not measure what its prose intent requires. Direct PF-S3-01 class defect at the meta-design layer.
**Disposition.** Adopt the fix verbatim: replace `grep -cE … ≥ 7` with `grep -oE … | sort -u | wc -l` equals 7.

### F-002 — §13 row 9 mis-scoped against §16 — LEGITIMATE
**Verification.** Read line 458 (§13 row 9 REFERENCED via INV-RESEARCH-ATTESTATION), line 573 (§16 scope: "Research-domain INV-* OUT-OF-SCOPE"), line 218 (§8.3 forbids `aplus-research runtime dispatch`). All three confirm the contradiction. The architect cannot simultaneously inherit INV-RESEARCH-ATTESTATION (row 9 implies inheritance) and have it OUT-OF-SCOPE (§16).
**Disposition.** Adopt option (b) per suggested fix: restate row 9 as "the architect-designed template REFERENCES this invariant for downstream specialists who DO dispatch aplus-research." The architect itself does not inherit.

### F-003 — Row 6 OUTBOUND framing miscategorizes pre-existing artifact — LEGITIMATE-MODIFIED
**Verification.** Read line 125 (row 6) + line 128 (anti-redefinition rule). Row 6 says SKILL.md is source of truth; anti-redefinition rule says canonical statement lives inside this design doc. The two are inconsistent for row 6 specifically.
**Disposition (modified fix).** Don't introduce a third directionality value (cost > benefit at 7-row table size). Instead, amend row 6's "How handled here" column to: "Defined externally in SKILL.md (predates this doc); design doc establishes the mode-floor convention only. The OUTBOUND scope here is the convention, not the skill spec itself."

### F-004 — Missing EC for Pass-1 substrate defect propagation — LEGITIMATE
**Verification.** Read CB §11 (lines 342-353). The "Suspicious URL list" is real and lists Role 1 [55] explicitly. Role 1 [55] is noted as already-verified at Phase 7, so the immediate risk is resolved — but the EC-9 has independent value for Pass-3 specialists whose flagged citations have NOT been verified.
**Disposition.** Adopt EC-9 addition. Frame as forward-defensive for Pass-3, not as a current Pass-2 defect.

### F-005 — EC-7 test stimulus tautological — LEGITIMATE
**Verification.** Read lines 533-535. The test stimulus IS the spec restated. By construction, the OUTBOUND row format is line-range-by-construction; the test cannot fail at the format layer.
**Disposition.** Adopt the reviewer's grep-based test: "For each OUTBOUND row, attempt to resolve the cited Finding-N line range against `domain-research.md`; if the line range does not exist or the cited Finding ID is out of the 1–9 valid range, the reference is forward-dependent and the row fails."

### F-006 — AP4 generic not architect-specific — LEGITIMATE-MODIFIED
**Verification.** Read line 336. AP4 ("don't issue more than 3 clarifying questions") is the canonical PF-S2-03 / feedback_question_economy.md rule and is genuinely project-wide.
**Disposition (modified fix).** Don't drop AP4 (it's still valid). Instead, the §7 Loop-Breaking "audit-script LIVE-tag cap" merits explicit promotion to a §11.2 entry. Add AP7 covering the LIVE-tag-without-verification surface; keep AP4. §11.2 budget is 5-8; current 6 + 1 = 7 fits.

### F-007 — §12 BAD/GOOD gap for AP4 + AP6 — LEGITIMATE-MODIFIED
**Verification.** Read lines 346-433. §12.1-12.4 map to AP1, AP2, AP3, AP5. AP4 and AP6 lack pairs. Template §12 budget is 2-4 pairs; current 4 is at upper bound.
**Disposition.** Add §12 preface rationale rather than additional pairs: "AP4 is covered structurally by §7 Loop-Breaking (the cap mechanism); AP6 is covered by §13 row 4 (the grep). Behavioral Negative Examples for these would duplicate mechanical defenses already in scope."

### F-008 — R-3 mitigation cites wrong anti-pattern — LEGITIMATE
**Verification.** Read line 596 (R-3) + line 334 (AP3). R-3 risk = "architect attempts to author specialist profiles rather than meta-deliverable." AP3 = "I don't ground specialist template on operator-profile contents." Reviewer is correct: AP3 doesn't mitigate R-3.
**Disposition.** Cite §2.2 "I do NOT own" item 1 (line 57: "actual agent-profile prose... owned by health-implementer Role 2") as R-3's load-bearing mitigation. Keep EC-7 citation (forward-dependency).

### F-009 — "sequential 6 → 9" misleading — LEGITIMATE-MODIFIED
**Verification.** Read lines 285-290. The four items are not order-dependent for the architect's purpose.
**Disposition.** Change "Project-spec load (sequential 6 → 9)" to "Project-spec load (required reads; no order dependency among 6–9)."

### F-010 — Phase 4 row claims more validation than 3-row gating set provides — LEGITIMATE
**Verification.** Read line 694 (Phase 4 row) + line 468 (§13 PROPOSED-does-not-gate caveat). 10 of 13 §13 rows are PROPOSED; Phase 4 fact-checker only has 3 LIVE/REFERENCED rows to verify.
**Disposition.** Adopt the precise rewrite: "§13 has 3 REFERENCED rows (8, 9, 10) that Phase 4 fact-checker can verify; 10 PROPOSED rows do not gate. §15.2 has 7 role-specific ACs."

### F-011 — 100% ACCEPTED raises synthesis-judgment question — LEGITIMATE-MODIFIED
**Verification.** Read lines 80-110. All 9 Findings + all 15 Recommendations are ACCEPTED. The Pass-1 substrate cleared 99/100 rubric; the 100% pattern is plausible, not necessarily PF-S2-05.
**Disposition.** Don't artificially mark a Finding MODIFIED. Adopt one-sentence preamble before §3.1: "Synthesis judgment applied to all 9 Findings and 15 Recommendations; no MODIFIED verdicts because each Finding is structural (template-shape) rather than numerical/claim-specific, and each Recommendation maps cleanly to a section default the design doc encodes."

### F-012 — §1 omits Finding 9 deliverable-triangle — LEGITIMATE
**Verification.** Read lines 21-30 (§1). Citations are Findings 5, 2, 3, 1. Finding 9 (the architect-deliverable triangle) is the most distinctive claim and appears throughout §13, §15, §17, §18 — but not in §1's framing.
**Disposition.** Add the 5th gap verbatim per reviewer's suggested fix.

### F-013 — §4 row 4 specialist count not sourced to CB §10 — LEGITIMATE
**Verification.** Read line 123 (§4 row 4) + CB §10 row 7 (line 336). CB §10 enumerates Role 2 R7, Role 3 R7, Role 4 R10 — three roles, not 11 specialists. The "+11 specialists" framing extends past CB §10.
**Disposition.** Adopt the dual-source fix: cite CB §10 for foundation-role inheritance; cite §2.2 item 1 (architect's own design intent) for the 11-specialist extension. Two sentences in row 4's "What is being referenced" column.

### F-014 — PF-S6-01 rationale conflates with PF-S2-05 — LEGITIMATE-MODIFIED
**Verification.** Read line 326 (PF-S6-01 row) + PF log lines 79-89 (PF-S6-01 actual) + lines 51-55 (PF-S2-05). PF-S6-01 = "act on prior-session state without verifying current"; PF-S2-05 = "operate from mental-model of protocol rather than re-read." The current rationale leans PF-S2-05.
**Disposition.** Rewrite the rationale to be state-verification-specific: "Architect's `last-PF-reviewed:` frontmatter pin assumes the PF log state at draft time. PF-S6-01 recurrence: assuming `memory/process-failures.md` is still at PF-S6-01 latest at finalize time without re-running the tail-line check. Mitigation: Phase-5 re-read per §17.1 R-5."

### F-015 — §13 row 3 "OR'd into single fail" semantic inversion — LEGITIMATE
**Verification.** Read line 452. "OR'd into single fail" is wrong English for "any-of-N missing = fail" (which requires AND-negation or any-zero check).
**Disposition.** Replace with: "fail if ANY of the three grep counts == 0; pass requires all three ≥ 1."

### F-016 — R-4 and R-5 merge candidate — LEGITIMATE-MODIFIED
**Verification.** Read lines 597-598. R-4 is about paraphrase-vs-line-range-citation; R-5 is about `last-PF-reviewed` pin staleness. Both relate to "freshness at finalize" but address different artifacts.
**Disposition (modified fix).** Keep R-4 and R-5 separate (they cite different evidence). Add a one-line cross-reference: under R-4, append "(see also R-5 for the PF-pin analog)."

### F-017 — Rule 12 title collapses what body forbids — LEGITIMATE
**Verification.** Read line 160. Rule 12 title says "GRADE certainty + recommendation strength is the medical equivalent of static types." The "+" performs the collapse the body forbids.
**Disposition.** Rename: "GRADE two-axis tagging is the medical equivalent of static types."

### F-018 — §8.4 PF-S2-06 "structural" reasoning half-correct — LEGITIMATE-MODIFIED
**Verification.** Read lines 197 (§8.1 Bash entry, self-enforcement) + 225-226 (§8.4 reasoning, hook-centric). Both true; the "structural" claim has two valid layers.
**Disposition.** Adopt the defense-in-depth rephrasing per reviewer's suggested fix.

### F-019 — Identity word count — REJECTED (reviewer-withdrawn)
**Verification.** Read line 38. Reviewer's own count: 33-38 words depending on whether the role-name slot ("You are the health-specialist-architect.") counts. R1 spec is ≤40. Both counts pass.
**Rejection rationale.** Reviewer self-withdrew after personal recount; finding retained in the adversarial report explicitly to document the verification path was walked. The Identity sentence is within spec. No design-doc change required.
**Cited-evidence attestation.** `design/health-specialist-architect-design.md:38` — Identity sentence; personally counted at 38 words including role-name slot, 33 words excluding. R1 ≤40 satisfied either way.
**Reject-but-adopt note.** The fix is null (no change); no independent value to adopt.

### F-020 — Rule 6 catches Mechanism B but not Mechanism C — LEGITIMATE
**Verification.** Read line 148. Rule 6 is first-person about reviewer-pushback (Mechanism B). Mechanism C (autonomous RLHF preference drift, no pushback required) has no analogous Core Rule.
**Disposition.** Adopt the Rule 6b (or expand Rule 6) per reviewer's fix. Architect-self defense against baseline-softening between drafts.

### F-021 — §9.1 vs §9.3 audience-tone clarity gap — LEGITIMATE-MODIFIED
**Verification.** Read lines 236-243 (§9.1) + 256-267 (§9.3). Format specs differ by audience but no explicit "9.1 fields NEVER appear in 9.3 outputs" rule.
**Disposition.** Adopt the one-sentence addition to §9.3 per reviewer's fix.

### F-022 — §13 row 13 WARN-conditional-on-future-policy ambiguous — LEGITIMATE
**Verification.** Read line 462. Modes-section-required policy is decided downstream (per DESIGN_DOC_TEMPLATE.md §5 line 626). No vault/decisions/ ADR exists for this transition.
**Disposition.** Adopt option (b) per reviewer's fix: drop the conditional, tag row 13 simply WARN, and add OQ-7 capturing the Modes-required policy decision (owner = orchestrator / Walter).

### F-023 — R5 ACCEPTED but §10 has no web-search-forbid clause for downstream template — LEGITIMATE-MODIFIED
**Verification.** Read line 100 (R5 ACCEPTED) + lines 272-308 (§10) + line 212 (§8.3 forbids web search for architect). The architect's web-search forbid covers the architect itself, not the downstream specialist template (which is the R5 surface).
**Disposition (modified fix).** Add a §10.7 clarification (not a full clause): "The R5 forbid-clause for free-form web search applies to the **specialist template variant** the architect designs (per Finding 9's deliverable triangle), not to this design doc's §10. The architect inherits R5's forbid-clause requirement via the template-artifact deliverable. §10 here describes only the architect's own context-loading."

---

## Safety findings (15)

### F-S1 — H-class enumeration (H1-H8) absent from OUTBOUND interface — LEGITIMATE
**Verification.** Read Role 4 substrate L147-L156 (H1-H8 enumeration with ICH E2A + FDA 3500A anchor) + L211 (composition rule `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`). Both confirmed. Read design doc §4 — only refusal-class taxonomy carried OUTBOUND; no H-class row.
**Disposition.** Adopt the 5-item remediation: 2nd OUTBOUND row in §4 + Core Rule in §5 + §13 row + §16 invariant entry. Strengthens Role 3/Role 4 severity-composition interface.

### F-S2 — AUTHORITY_FRAMING_BYPASS refusal class missing — LEGITIMATE
**Verification.** Read Role 4 substrate L304 ("load-bearing single fact for the reviewer's threat model") + L324-L328 (81.8% from medRxiv; 83.3% Educational Authority sub-strategy; HiddenLayer + Mondillo + Han + CALM corroboration). Read design doc §2.2 item 3 (line 48) — 7 refusal classes, none addresses framing.
**Disposition.** Adopt the 8th refusal-class addition: `AUTHORITY_FRAMING_BYPASS`. Update §13 row 4 grep; add §11.2 anti-pattern. Single-row addition unlocks 81.8% attack-surface coverage. Highest-leverage remediation.

### F-S3 — Operator-as-adversary (A3) has no template slot — LEGITIMATE
**Verification.** Read Role 4 substrate L122 (A3 explicit) + L278 (bromism canonical A3 case). Read design doc §14 (8 ECs; none addresses A3) + §11.2 (6 APs; none addresses operator-as-A3 asymmetry). Walter (single operator) dispatches the 14 specialists himself → A3 is the primary surface.
**Disposition.** Adopt: EC-9 explicitly naming A3 + a §11.2 anti-pattern recognizing operator-as-A3 asymmetry. Pair with F-S2 (authority-framing) since the two compose.

### F-S4 — TOCTOU operator-profile→compound write — LEGITIMATE
**Verification.** Read §13 row 5 (R7 enforcement) + §14 EC-2 (contradiction between current-state and write). No atomicity requirement, no mtime check between read and write.
**Disposition.** Adopt: extend §13 row 5 (or add row 14) requiring either re-read within N seconds OR recorded mtime/hash. Acknowledge architect-template-vs-Role-2-implementation boundary per architect's role-discipline; document the deferral with named consumer.

### F-S5 — Refusal-class presence != adversarial-probe pass — LEGITIMATE
**Verification.** Read §13 row 4 (presence-grep check) + Role 4 substrate L94-L111 (refusal-training insufficient as gating signal) + L109-L111 ("reviewer's verdict must NOT rely on candidate's own refusal behavior"). Architect's §13 row 4 currently is the presence check; Role 4's adversarial-probe verdict is the real gate but has no template-side anchor.
**Disposition.** Adopt the PROPOSED §13 row: "Adversarial-probe pass anchor — specialist's deployment is gated by a Role-4 evaluation log file showing adversarial-probe verdict = DEPLOY or DEPLOY_WITH_OVERRIDE_PATH." Mirror in §18 as Role-4-contract-pending OQ.

### F-S6 — §13 row 4 unconditional disjunctive; image-handling specialists pass without IMAGE_OR_SIGNAL_INPUT — LEGITIMATE
**Verification.** Read Role 4 substrate L81-L92 (GPT-4o 70% ASR for sub-visual injection) + R13 L438 (mandatory ≥3 image probes for image-handling). Read §13 row 4 — unconditional disjunctive grep over 7 class names. Labs-specialist (LM-01 critical path through July 2026 doctor visit) processes lab PDFs.
**Disposition.** Adopt the Tools-conditional amendment to row 4: "If specialist's Tools section permits Read against image MIME types OR WebFetch from image-serving URLs, Role Boundaries MUST cite `IMAGE_OR_SIGNAL_INPUT` (mandatory, not disjunctive)." Add §14 edge case naming the lab-PDF + sub-visual injection scenario.

### F-S7 — Bromism-class context-mismatch beyond animal→human — LEGITIMATE
**Verification.** Read Role 4 substrate L278 (Annals 2024/2025 bromism case) + L394-L400 (broader category: model gives correct factual content but fails to recognize deployment context). Read design doc §14 EC-4 (covers animal→human population-mismatch only).
**Disposition.** Adopt the EC-10 addition (or extend EC-4): "Context-mismatch — operator question's framing differs from specialist's declared scope (bromism-class)." NOTE-class; secondary to F-S2/F-S3.

### F-S8 — GRADE strong-with-low-certainty "flagged" undefined — LEGITIMATE
**Verification.** Read line 160 (Rule 12). The word "flagged" appears but is not mechanically defined. §13 row 2 only checks GRADE vocabulary presence; no HALT condition on strong+low.
**Disposition.** Adopt the mechanical definition: "strong-with-low-certainty combinations HALT the claim and require either (a) downgrading recommendation strength, (b) supplemental evidence raising certainty, or (c) explicit operator-acknowledged-override logged in vault/meta/contradictions.md." Update §13 row 2 to check the HALT condition.

### F-S9 — No multi-turn / many-shot template slot — LEGITIMATE
**Verification.** Read Role 4 substrate L73 (Yang et al. 69.4% persistence at turn 6) + L142 (Anil many-shot) + R8 L428 (Role 4 probe coverage). Architect's §10 Context Loading is dispatch-start only; no mid-dispatch re-anchor.
**Disposition.** Adopt the PROPOSED §13 row for multi-turn re-anchor. Combined with F-S14 (template-level slot for re-anchor clause).

### F-S10 — Mechanism A pre-Role-4 fallback unnamed — LEGITIMATE
**Verification.** Read §2.2 item 6 + §4 row 7 + §18 OQ-2 + §17.2 A-3 + Role 4 substrate L386 (Limitation 11; reviewer cited as L386 which is correct; the "Limitation 20" label in the finding's metadata is a copy-edit miss but the cited content is accurate). The architect doc relies on Role 4 deployment; doesn't name the v1-substitute fallback explicitly.
**Disposition.** Adopt the §17.2 A-7 assumption per reviewer's fix.

### F-S11 — vendor_label+number at specialist output not gated — LEGITIMATE
**Verification.** Read §14 EC-3 (catches at dispatch layer via aplus-research IC-3/IC-4) + §13 rows 11-12 (KG-grounded retrieval + citation-verification tool). §8.1 permits direct Read against vault/library, bypassing aplus-research.
**Disposition.** Adopt the PROPOSED §13 row grep-auditing specialist-output sentence collision. Mirrors INV-RESEARCH-NO-VENDOR-NUMERICAL at specialist-write-path layer.

### F-S12 — No template slot for eval-awareness — LEGITIMATE-MODIFIED
**Verification.** Read Role 4 substrate L298-L302 + L394 (Petri 2.0; production-shaped probes). Architect's §14 ECs are test-shaped, not production-shaped.
**Disposition (modified fix).** Reviewer's fix is to document the gap as an assumption (§17.2 A-8). Adopt as-is — the gap is genuinely Role 4-owned, not architect-fixable at template layer. The assumption clarifies role-boundary discipline.

### F-S13 — Indirect injection via Tier-1 fetched content not template-gated — LEGITIMATE
**Verification.** Read Role 4 substrate L121 (A2) + L132 (S3) + L137 (P1). Read §8.1 (permissive Read against vault/library). aplus-research IC-13 catches at dispatch; direct Read bypasses.
**Disposition.** Adopt the §10.6 cross-role trigger: Tier-Tag-gated Read discipline required when specialists Read vault/library/ outside aplus-research dispatch.

### F-S14 — No multi-turn re-anchor cadence — LEGITIMATE
**Verification.** Read Role 4 substrate L143, L145. Read §10 (auto-load at dispatch start only). No turn-by-turn re-anchor discipline.
**Disposition.** Combine with F-S9 remediation: single §13 row + Core Rule for multi-turn re-anchor cadence (default N=3 turns OR after framing-class change).

### F-S15 — Pre-Role-7 escalation routes to A3 operator — LEGITIMATE
**Verification.** Read §13 row 6 (escalation target `medical-liaison`) + §14 EC-2 + EC-6. Read Role 4 substrate L386 (Limitation 11 — "during pre-Role-7 phase override paths route to user directly — itself a documented risk surface"). Reviewer cited as "Limitation 20" but content is at Limitation 11; substantive evidence correct, label miss is a copy-edit defect.
**Disposition.** Adopt the §13 row 6 amendment + §17.2 A-9 + §14 EC-9. Highest-leverage Pre-Role-7 deployment-exposure fix. Composes with F-S3 (operator-as-A3) and F-S2 (authority-framing).

---

## Reject-but-adopt summary

Only F-019 is REJECTED (reviewer self-withdrew after personal recount; Identity word count passes R1 ≤40 either way). No reject-but-adopt cases this Phase 4 — all REJECTED has null fix. The pattern was on watch per S7 precedent (F-006, F-023 in DESIGN_DOC_TEMPLATE.md review); no recurrence here.

---

## Disposition application order (for Phase 5 synthesis)

Highest-leverage first (matching F-S verdict severity + F-N criticality):

1. **F-S2** — AUTHORITY_FRAMING_BYPASS 8th refusal class (covers 81.8% attack surface)
2. **F-S15** — Pre-Role-7 escalation amendment (largest pre-deployment runtime exposure)
3. **F-S3** — Operator-as-A3 EC-9 + AP (composes with F-S2)
4. **F-S6** — Image-handling Tools-conditional row 4 (labs-specialist critical path)
5. **F-S1** — H-class composition OUTBOUND row + Core Rule + §13 + §16 invariant
6. **F-002** — §13 row 9 mis-scope fix (single-line restate)
7. **F-001** — AC-4 grep mechanism fix (single-line fix)
8. **F-010** — Phase 4 coverage row precision
9. **F-013** — §4 row 4 dual-source citation
10. **F-023** — §10.7 clarification clause
11. **F-S4 / F-S5 / F-S8 / F-S10 / F-S11** — WARN-class structural additions
12. **F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-011, F-012, F-014, F-015, F-016, F-017, F-018, F-020, F-021, F-022** — Minor + Nitpick polish
13. **F-S7 / F-S9 / F-S12 / F-S13 / F-S14** — NOTE-class defense-in-depth additions

---

## PF-S3-01 guard attestation

Each of 38 findings personally source-read before classification. Cited evidence per finding includes file path and line range, verified empirically (grep counts, line content). The 1 REJECTED finding (F-019) carries the reviewer's own self-withdrawal as cited evidence; no orchestrator prose substitution.

Reject-but-adopt discipline applied: 0 cases this cycle (the F-006/F-023 pattern from S7 didn't recur). All 11 LEGITIMATE-MODIFIED dispositions document the modification rationale explicitly per the discipline.

**Phase 4 verification complete. Ready for Phase 5 synthesis (apply 37 dispositions + Appendix A population).**
