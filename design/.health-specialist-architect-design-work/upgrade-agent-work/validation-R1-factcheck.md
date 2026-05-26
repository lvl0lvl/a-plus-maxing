---
title: Fact-checker — R1 Behavioral Traits
type: upgrade-agent-artifact
phase: 4
role: fact-checker
artifact_under_check: R1-behavioral-traits.md
created: 2026-05-26
---

# Fact-checker R1

## Summary
- Total checks: 30
- PASS: 25
- FAIL: 5
- Overall verdict: **FAIL**

The artifact is sound on content (citations resolve, mechanisms named, mechanical structures encoded) but fails on (a) Core Rules count overshooting the 8-12 budget (rule count = 13), (b) per-rule citation-token compliance for 5 of 13 Core Rules (rules 4, 5, 10, 12, 13 lack a Finding/PF/R/INV/FD&C/FDA/IMDRF token), (c) AP8 source-citation does not match the strict regex (cites "F-S3" not "PF-S\d+-\d+ | Finding \d+ | R\d+"), (d) Loop-Breaking section overshoots ≤6 line budget (7 lines), (e) Anti-Patterns section overshoots ≤8 line budget (10 lines).

## Per-check results

### Identity (D1)

### FC-1.1 (Identity word count ≤ 40)
- Verdict: **PASS** (with note)
- Evidence: Two declarative sentences appear under the `# health-specialist-architect` header before `## Identity`. Sentence 1: "You are the health-specialist-architect." = 4 words. Sentence 2 (role-purpose): "You receive medical-LLM design problems from the orchestrator and deliver a template variant of AGENT_TEMPLATE.md, per-section interface contracts, and an audit script that mechanically gates the 14 downstream specialist profiles (Finding 9 triangle: template + discipline doc + audit script)." = **40 words** (`tr -s '[:space:]' '\n' | grep -c .` = 40). Inclusive ≤ 40 → PASS at the boundary. Note: R1's self-attested "33 words" miscount; actual is 40, exactly at cap. The full Identity-body paragraph (`You serve the architecture…`) is 93 words across multiple sentences, but FC-1.1 instructs counting "the declarative sentence" exclusive of anti-sycophancy and header lines — the role-purpose statement is the canonical Identity sentence at 40 words.

### FC-1.2 (Identity body zero `must|never|always|refuse` lexicon)
- Verdict: **PASS**
- Evidence: `grep -iE 'must|never|always|refuse'` against lines 14-22 of the R1 artifact (Output A code-block body) returns exactly one hit, on the anti-sycophancy line ("Never begin a response with…"), which FC-1.2 explicitly excludes. The Identity declarative sentence body has zero matches.

### FC-1.3 (Anti-sycophancy anchor present)
- Verdict: **PASS**
- Evidence: `grep -E 'Mechanism A|Mechanism B|Mechanism C|sycophan'` against Output A returns 3 matches (Mechanism A, B, C all in the Identity body paragraph). The affirmation-ban line "Never begin a response with…" is on line 22 of the R1 file (line 12 of the rendered identity block).

### FC-1.4 (All three mechanisms named)
- Verdict: **PASS**
- Evidence: "Mechanism C (RLHF preference drift) anchor" + "Mechanism A (multi-agent silent agreement) routes to the Role 4 Council-Mode slot" + "Mechanism B (single-model user acquiescence) is held by the maintain-position-without-new-evidence clause" — all three present in the Identity body paragraph.

### FC-1.5 (Role purpose stated as the deliverable triangle)
- Verdict: **PASS**
- Evidence: Header sentence ends with "(Finding 9 triangle: template + discipline doc + audit script)." All three artifacts named and cited to Finding 9 (design-doc §3.1 row 9 confirms Finding 9 = template + discipline doc + audit script triangle).

### Core Rules (D3)

### FC-3.1 (Core Rules count between 8 and 12 inclusive)
- Verdict: **FAIL**
- Evidence: `grep -cE '^[0-9]+\. '` against Output B markdown body = **13** numbered rules. Rubric requires 8 ≤ N ≤ 12. R1's self-attested count is "13 numbered rules within the 12-15 budget" — but FC-3.1 specifies the rubric's tighter 8-12 cap (D3 rubric line 50). 13 > 12 → FAIL.

### FC-3.2 (Each rule has a testable pass/fail; sample 3)
- Verdict: **PASS**
- Evidence: Sample 3 of 13 rules:
  - Rule 3 ("Identity ≤40 words, no `must|never|always|refuse` lexicon") — testable by word count + grep. ✓
  - Rule 11 ("Encode 8-class taxonomy `PATIENT_FACING_DIRECTIVE`, … `AUTHORITY_FRAMING_BYPASS`") — testable by grep for 8 named identifiers. ✓
  - Rule 12 ("GRADE strong+low-certainty HALTS the claim") — testable by schema check on certainty × strength pairing. ✓

### FC-3.3 (Voice mix: ≥2 first-person rules)
- Verdict: **PASS**
- Evidence: `grep -cE '\[first-person' /tmp/outB.txt` = 2 (rule 6 and rule 10). ≥ 2 → PASS.

### FC-3.4 (Grep Core Rules for `GRADE|certainty|recommendation strength` ≥1)
- Verdict: **PASS**
- Evidence: `grep -cE 'GRADE|certainty|recommendation strength'` = 2 (rule 1 mentions GRADE; rule 12 contains all three terms).

### FC-3.5 (Grep for `H-class|H1|H2|harm.class|worst.case.reachable|max\(Role` ≥1)
- Verdict: **PASS**
- Evidence: `grep -cE 'H-class|H1|H2|harm.class|worst.case.reachable|max\(Role'` = 1 (rule 13 contains all of: `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`, H1, H2). ≥ 1 → PASS.

### FC-3.6 (Each rule cites at least one of `Finding \d+|PF-S\d+-\d+|R\d+|INV-|FD&C|FDA|IMDRF`)
- Verdict: **FAIL**
- Evidence: Per-rule scan (strict regex):
  - Rule 1: MATCH (Finding 1–9, PF-S\d+-\d+, FD&C, IMDRF, FDA)
  - Rule 2: MATCH (Finding 3)
  - Rule 3: MATCH (R1)
  - **Rule 4: NO_MATCH** — text "(essay reference, substrate line range, INV register row)" uses "INV register" without the `INV-` dash; "§5 rule 4" doesn't match any token.
  - **Rule 5: NO_MATCH** — "INV mechanical-enforcement principle" lacks `INV-` dash.
  - Rule 6: MATCH (Finding 3 Mechanisms B + C)
  - Rule 7: MATCH (Finding 7, R9)
  - Rule 8: MATCH (R11)
  - Rule 9: MATCH (PF-S3-01)
  - **Rule 10: NO_MATCH** — only "[first-person; §5 rule 10]"; no Finding/PF/R/INV/FDA token.
  - Rule 11: MATCH (Finding 5)
  - **Rule 12: NO_MATCH** — body contains "GRADE" but rubric regex does not include `GRADE`; tag "[imperative; §5 rule 12]" has no token. (GRADE is rubric vocabulary but not in the FC-3.6 pattern.)
  - **Rule 13: NO_MATCH** — only "[imperative; §5 rule 13; §4 OUTBOUND row 2]"; no Finding/PF/R/INV/FDA token.
  - 5 of 13 rules fail → FAIL.

### Role Boundaries (D5)

### FC-5.1 (I own ≥ 5 items)
- Verdict: **PASS**
- Evidence: Output C "I own" paragraph split on `;` = **8 items**: (1) 11-section variant of AGENT_TEMPLATE.md; (2) per-section interface contracts; (3) 8-class refusal taxonomy; (4) GRADE grammar; (5) three-mechanism anti-sycophancy commitment; (6) Role 4 Council-Mode slot; (7) contradiction-discipline contract; (8) Mechanical Check Index + audit-script interface spec. 8 ≥ 5.

### FC-5.2 (I do NOT own ≥ 5 items)
- Verdict: **PASS**
- Evidence: Output C "I do NOT own" paragraph split on `;` = **8 items**: (1) specialist agent-profile prose; (2) coverage-gap detection; (3) adversarial red-team; (4) aplus-research internals; (5) audit-script bash implementation; (6) task assignment + sequencing; (7) IDENTICAL/DIFFER cross-specialist boilerplate; (8) 4-axis severity composition. 8 ≥ 5.

### FC-5.3 (Every "do NOT own" item has role name in parentheses)
- Verdict: **PASS**
- Evidence: Verified each:
  - (health-implementer, Role 2) ✓
  - (health-edge-case-reviewer, Role 3) ✓
  - (medical-safety-reviewer, Role 4) ✓
  - (aplus-research skill maintainer) ✓
  - (health-implementer or tooling pass — I write the interface, not the bash) ✓
  - (orchestrator / Walter) ✓
  - (health-implementer) ✓
  - (Roles 3 and 4) ✓
  - All 8/8 have parenthetical role.

### FC-5.4 (Role 4 Council-Mode slot mentioned)
- Verdict: **PASS**
- Evidence: `grep -cE 'medical-safety-reviewer|Role 4|Council-Mode'` against Output C = 2 hits ("`medical-safety-reviewer` (Role 4) as Council-Mode dissent agent" in "I own" and "(medical-safety-reviewer, Role 4)" in "I do NOT own").

### FC-5.5 (Escalation rule present)
- Verdict: **PASS**
- Evidence: Line 58 of R1 artifact: "When I detect a problem in a not-owned area, I write a one-line contract-violation finding ... I do not edit the affected artifact or rewrite another role's prose. [§2.2]"

### Loop-Breaking (D7)

### FC-7.1 (≥3 thresholds with numeric or binary values)
- Verdict: **PASS**
- Evidence: 5 thresholds in Output E, all with explicit numeric/binary values: spec-revision cap (numeric, 2); design-review cap (numeric, 3); context-scratch (binary); LIVE-tag cap (binary); fabrication threshold (binary, zero-tolerance). 5 ≥ 3.

### FC-7.2 (LIVE-tag cap present)
- Verdict: **PASS**
- Evidence: `grep -cE 'LIVE|verify|verification'` against Output E = 1 line — the "Audit-script LIVE-tag cap (binary)" bullet contains "LIVE", "verification fails twice", "verify(ied)". The single line matches all three keywords.

### FC-7.3 (Cross-role-reference fabrication zero-tolerance present)
- Verdict: **PASS**
- Evidence: `grep -cE 'fabricat|zero-tolerance|cannot cite'` against Output E = 1 line — the "Cross-role-reference fabrication threshold (binary, zero-tolerance)" bullet contains "fabrication" and "zero-tolerance" and "Cannot cite".

### Anti-Patterns (D9)

### FC-9.1 (Anti-Patterns count between 5 and 8 inclusive)
- Verdict: **PASS**
- Evidence: `grep -cE "^- I don" /tmp/outF.txt` = 8 entries. 5 ≤ 8 ≤ 8.

### FC-9.2 (Every entry starts with "I don't")
- Verdict: **PASS**
- Evidence: All 8 entries open with "- I don't ..." (verbatim line starts confirmed above).

### FC-9.3 (Every entry has ≥1 source citation in PF-S\d+-\d+ | Finding \d+ | R\d+ pattern)
- Verdict: **FAIL**
- Evidence: 7 of 8 anti-patterns match. **AP8 fails the strict regex**: cited as "F-S3 disposition + Role 4 substrate L122 + L278 (bromism case)". "F-S3" lacks the `PF-` prefix required by the FC-9.3 pattern `PF-S\d+-\d+`. The cited source is real (F-S3 = Phase-3 finding-disposition ID, resolves at design-doc line 807) but does not match the rubric's whitelisted citation pattern. Strict reading: FAIL. Smallest fix: append `(maps to PF-S3-01 pattern: operator-as-adversary)` or relabel to include a matching identifier.

### FC-9.4 (Operator-as-A3 anti-pattern present)
- Verdict: **PASS**
- Evidence: `grep -cE 'A3|operator.*adversar|inside trust|bromism'` against Output F = 1 line — AP8 contains "named A3 in the threat catalog", "INSIDE the trust boundary", and "(bromism case)".

### FC-9.5 (LIVE-tag-without-verification anti-pattern present)
- Verdict: **PASS**
- Evidence: AP7 = "I don't tag a §13 row LIVE before running Glob or Read against the cited path."

### Ask vs Proceed (structural)

### FC-AVP-1 (≥4 branches)
- Verdict: **PASS**
- Evidence: 6 numbered branches in Output D (Authoritative-source check, Cross-role-contract impact, Mechanical-check tag impact, Operator-profile compound-write impact, Internal-component-only, Default). 6 ≥ 4.

### FC-AVP-2 (Fabrication guard present)
- Verdict: **PASS**
- Evidence: Final paragraph of Output D: "**Fabrication guard.** Never fabricate a refusal-class identifier, GRADE certainty tier, CONTINUATION_BRIEF §10 row, INV-* ID, `PF-S\d+-\d+` identifier, or `vault/` path. If uncertain, halt and resolve via branch 1 or 2. [§6]"

### Operational completeness (cross-cutting)

### FC-OC-1 (5 sampled verbs each have tool/workflow)
- Verdict: **PASS**
- Evidence: 5-verb sample (drawn from CR/AP/Ask vs Proceed):
  - "Anchor" (CR1) → Read / Grep (substrate, INVARIANTS, regulatory text) — operational-completeness table line 203 of R1 artifact names both tools.
  - "Encode" (CR2, CR11) → Write/Edit — table line 204 (permitted paths enumerated).
  - "Re-dispatch the verifier" (CR9) → Agent tool — table line 207.
  - "Read / Glob / Grep" (Ask vs Proceed 1, 3, 4; AP5/6/7) → corresponding tools — table line 210.
  - "Run `scripts/audit-specialist-profile.sh`" (AP1) → Bash — table line 215.
  - All 5/5 have tool/workflow named.

### Line budgets

### FC-LB-1 (Header+Identity section ≤ 15)
- Verdict: **PASS**
- Evidence: Output A code-block content = 9 lines (`# health-specialist-architect` + blank + role-purpose + blank + `## Identity` + blank + Identity-body paragraph + blank + anti-sycophancy line). 9 ≤ 15.

### FC-LB-2 (Core Rules section ≤ 15)
- Verdict: **PASS**
- Evidence: Output B code-block content = 15 lines (`## Core Rules` + blank + 13 rule lines). 15 ≤ 15 (at cap).

### FC-LB-3 (Role Boundaries section ≤ 8)
- Verdict: **PASS**
- Evidence: Output C code-block content = 7 lines (`## Role Boundaries` + blank + I-own + blank + I-do-NOT-own + blank + escalation). 7 ≤ 8.

### FC-LB-4 (Ask vs Proceed section ≤ 10)
- Verdict: **PASS**
- Evidence: Output D code-block content = 10 lines (`## Ask vs Proceed` + blank + 6 numbered + blank + fabrication-guard + blank). 10 ≤ 10 (at cap).

### FC-LB-5 (Loop-Breaking section ≤ 6)
- Verdict: **FAIL**
- Evidence: Output E code-block content = 7 lines (`## Loop-Breaking` + blank + 5 threshold bullets). 7 > 6. R1's self-claim "5 lines = 5 thresholds, within the 5-6 budget" counted only the threshold bullets, omitting the section header and blank. Strict per-section line count including header/blank is 7. Smallest fix: drop one bullet (e.g., merge spec-revision + design-review caps into a compound threshold) or accept header-exclusion convention (would need explicit ratification by upgrade-agent.md).

### FC-LB-6 (Anti-Patterns section ≤ 8)
- Verdict: **FAIL**
- Evidence: Output F code-block content = 10 lines (`## Anti-Patterns` + blank + 8 AP entries). 10 > 8. R1's self-claim "8 entries within the 6-8 budget" counted only entries. Strict per-section line count including header/blank is 10. Smallest fix: drop or merge to ≤6 entries (e.g., fold AP4 ≤3-questions into Loop-Breaking, fold AP6 FDA-prose-pattern-match into AP1 audit-script requirement) to reach 7-8 total lines, OR ratify the entries-only convention upstream.

### Citation integrity

### FC-CI-1 (Sample 5 cited identifiers resolve)
- Verdict: **PASS**
- Evidence:
  - **PF-S3-01** → `grep -c "PF-S3-01" memory/process-failures.md` = 3 (Session 3 entry exists). RESOLVES.
  - **PF-S2-02** → `grep -c "PF-S2-02" memory/process-failures.md` = 1 (citation-error entry). RESOLVES.
  - **Finding 9** → `grep -c "Finding 9" design/health-specialist-architect-design.md` = 14 (Finding 9 row in §3.1 table). RESOLVES.
  - **Finding 5** → 11 matches; §3.1 table row 5 + §2.2 item 3 + §11.2 AP6. RESOLVES.
  - **INV-ROLE-INLINING** → 2 matches in INVARIANTS.md (register row + category breakdown). RESOLVES.
  - All 5/5 resolve.

### FC-CI-2 (No fabricated identifiers)
- Verdict: **PASS**
- Evidence: Enumerated all identifiers in R1:
  - PF-S\d+-\d+: PF-S2-01, PF-S2-02, PF-S2-03, PF-S2-04, PF-S2-05, PF-S3-01 — all 6 exist in `memory/process-failures.md`. No PF-S0-*, no PF-S>6 fabrications.
  - Finding \d+: Finding 1, 3, 5, 7, 9 — all within 1-9 range; design-doc §3.1 row count = 9. No Finding 0, no Finding 10+.
  - INV-*: only INV-ROLE-INLINING — exists in register row 9 of INVARIANTS.md.
  - "F-S2", "F-S3" identifiers (used in AP8 / cut-rationale) — these are Phase-3 finding-disposition IDs that exist in the design doc (line 807 "F-S3", line 823 "F-S2", "F-S3", "F-S6"). RESOLVE.
  - No fabricated identifiers detected.

## Failures (if any)

1. **FC-3.1 — Core Rules count = 13, exceeds 12-cap.**
   - Defect: Rubric D3 sets 8-12 Core Rules. R1 ships 13.
   - Smallest fix: merge rule 12 (GRADE HALT) + rule 13 (H-class composition) into one "evidence-rigor + harm-class" rule with both axes named; OR merge rule 4 (numerical-default tracing) into rule 1 (anchor-every-default) as a sub-clause. Either reduces count to 12.

2. **FC-3.6 — 5 of 13 Core Rules (rules 4, 5, 10, 12, 13) lack a regex-matching citation token.**
   - Defect: Rules cite "[§5 rule N]" only, or use "INV" without the required `INV-` dash.
   - Smallest fix: add at least one of `Finding N | PF-S\d+-\d+ | R\d+ | INV-* | FD&C | FDA | IMDRF` to each of the 5 affected rule tail-tags. E.g., rule 4 → "[…; R4]"; rule 5 → "[…; INV-RESEARCH-* mechanical-enforcement principle]"; rule 10 → "[…; R-related]"; rule 12 → "[…; Finding 2; R2]"; rule 13 → "[…; ICH E2A; FDA 3500A]" (both are already in the design-doc §4 row 2 source path).

3. **FC-9.3 — AP8 source-citation "F-S3 disposition" does not match the FC-9.3 strict regex `PF-S\d+-\d+ | Finding \d+ | R\d+`.**
   - Defect: F-S3 is a real Phase-3 finding-disposition ID (resolves in design-doc) but the regex required by the fact-checker rubric does not whitelist that family.
   - Smallest fix: append a matching identifier — e.g., change "Source: F-S3 disposition + Role 4 substrate L122 + L278" to "Source: F-S3 disposition + Finding 5 (refusal-class) + Role 4 substrate L122 + L278" — Finding 5 already underwrites the operator-inside-trust frame via the AUTHORITY_FRAMING_BYPASS class.

4. **FC-LB-5 — Loop-Breaking section = 7 lines, exceeds 6-cap.**
   - Defect: Section header + blank + 5 bullets = 7 lines.
   - Smallest fix: merge spec-revision cap (numeric, 2) + design-review round cap (numeric, 3) into one "revision/round cap (numeric, 2 revisions OR 3 rounds → escalate)" bullet, reducing to 4 bullets + header + blank = 6.

5. **FC-LB-6 — Anti-Patterns section = 10 lines, exceeds 8-cap.**
   - Defect: Section header + blank + 8 AP entries = 10 lines.
   - Smallest fix: drop 2 lower-leverage APs to reach 6 entries + header + blank = 8. Candidates to drop or fold: AP2 (paraphrase-Finding — covered by Core Rule 1's anchor requirement); AP4 (≤3 questions — covered by Loop-Breaking spec-revision cap + PF-S2-03 directly). The R1 cut-rationale acknowledges this trade-off but elected to preserve all 8; the strict rubric requires reducing to ≤8 lines total.

## Notes

- R1's self-attested counts are inconsistent with strict measurement at multiple points: "Identity sentence = 33 words" (actual: 40); "13 numbered rules within the 12-15 budget" (rubric cap is 12, not 15); "5 lines = 5 thresholds, within the 5-6 budget" (actual section = 7 lines including header); "8 entries within the 6-8 budget" (actual section = 10 lines). These are not citation defects, but they signal that R1 used an entries-only line-counting convention while the rubric uses total-section-lines. The discrepancy is the root cause of FC-LB-5 and FC-LB-6 failures.
- Content quality is high: every mechanism (A/B/C), every load-bearing mechanical structure (GRADE two-axis HALT, H-class max() composition, LIVE-tag cap, fabrication zero-tolerance, operator-as-A3), and every required citation family (Finding, PF, INV, R, regulatory) is present somewhere in the artifact. The failures above are quantitative (count overruns, regex-strictness, line-budget arithmetic) rather than substantive omissions.
- The operational-completeness self-check table (R1 lines 199-219) is well-formed and resolves every behavioral verb in Core Rules / Anti-Patterns / Ask vs Proceed / Loop-Breaking to a tool from §8.1 of the design doc or a named workflow. This is stronger than the rubric minimum.
- Citation integrity is clean: 0 fabricated identifiers. All PF, Finding, INV, R identifiers used resolve in their source files.
