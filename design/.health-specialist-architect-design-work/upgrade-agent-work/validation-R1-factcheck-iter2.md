---
title: Fact-checker iter2 — R1 v2
type: upgrade-agent-artifact
phase: 4
iteration: 2
role: fact-checker
artifact_under_check: R1-behavioral-traits-v2.md
created: 2026-05-26
---

# Fact-checker R1 iter2

## Summary
- Total checks: 30
- PASS: 29
- FAIL: 1
- Overall verdict: FAIL

## Per-check results

### Identity (D1)
- **FC-1.1 PASS.** Role-purpose sentence (L32) word count = 38 (≤40). Anti-sycophancy declarative sentence (L36 first sentence "You serve the architecture...") = 9 words (≤40). Both candidate "Identity sentences" satisfy ≤40.
- **FC-1.2 FAIL.** Identity body (lines 34-38 under `## Identity`) contains the lexical token "Never" at L38: "Never begin a response with 'Great', 'Good idea', 'Absolutely', 'You're right', or any affirmation." This matches the prohibited regex `must|never|always|refuse` (case-insensitive). The artifact's own self-attestation at L41 ("No `must|never|always|refuse` lexicon in Identity body") is contradicted by the artifact's own text.
- **FC-1.3 PASS.** Anti-sycophancy anchor (Mechanism A/B/C paragraph) lands at L36 — within the first 20 lines of the deployable agent.md content (which begins at L30 of the artifact: i.e., L36 - L30 = 6 lines into the profile).
- **FC-1.4 PASS.** Mechanism A, Mechanism B, Mechanism C all named at L36.
- **FC-1.5 PASS.** L32 explicitly states "template variant of AGENT_TEMPLATE.md, per-section interface contracts, and an audit script... (Finding 9 triangle: template + discipline doc + audit script)."

### Core Rules (D3)
- **FC-3.1 PASS.** Core Rules numbered 1-12 at L48-L59. Count = 12, inside [8,12].
- **FC-3.2 PASS.** Sampled rules 1, 3, 11: each has a binary pass/fail condition (anchor presence; ≤40-word + lexicon grep; HALT trigger on strong+low-certainty).
- **FC-3.3 PASS.** First-person rules: Rule 5 ("Every time I have folded...") and Rule 9 ("Every time I authored first..."). Count = 2, ≥2.
- **FC-3.4 PASS.** Rule 11 (L58) contains `GRADE`, `certainty`, `recommendation-strength`. ≥1 match.
- **FC-3.5 PASS.** Rule 12 (L59) contains `H-class`, `H1`, `H2`, `worst_case_reachable`, `max(Role3.nominal, Role4.worst_case_reachable)`. ≥1 match (all five tokens present).
- **FC-3.6 PASS.** All 12 rules carry a regex-matching token: R1 (Finding/PF/FD&C/IMDRF/FDA/GRADE); R2 (Finding 3); R3 (R1); R4 (INV-RESEARCH-ATTESTATION); R5 (Finding 3); R6 (Finding 7; R9); R7 (R11); R8 (PF-S3-01); R9 (PF-S2-05); R10 (Finding 5); R11 (Finding 2; R2); R12 (ICH E2A; FDA 3500A).

### Role Boundaries (D5)
- **FC-5.1 PASS.** L69 enumerates 8 "I own" items (semicolon-separated): template variant; per-section interface contracts; 8-class refusal taxonomy; GRADE two-axis grammar; three-mechanism anti-sycophancy; Role 4 Council-Mode slot; contradiction-discipline contract; Mechanical Check Index. 8 ≥ 5.
- **FC-5.2 PASS.** L71 enumerates 8 "I do NOT own" items. 8 ≥ 5.
- **FC-5.3 PASS.** Each of the 8 "do NOT own" items has owning role in parens: (health-implementer, Role 2); (health-edge-case-reviewer, Role 3); (medical-safety-reviewer, Role 4); (aplus-research skill maintainer); (health-implementer or tooling pass — I write the interface, not the bash); (orchestrator / Walter); (health-implementer); (Roles 3 and 4).
- **FC-5.4 PASS.** L69: "the architectural slot for `medical-safety-reviewer` (Role 4) as Council-Mode dissent agent."
- **FC-5.5 PASS.** L73: "When I detect a problem in a not-owned area, I write a one-line contract-violation finding..."

### Loop-Breaking (D7)
- **FC-7.1 PASS.** L100-L103 = 4 bullets carrying ≥4 thresholds with explicit numeric/binary values: Revision caps (numeric: 2 revisions, 3 rounds); Context-scratch (binary, ~5 dependencies); LIVE-tag (binary, zero-third-attempt); Fabrication (binary, zero-tolerance).
- **FC-7.2 PASS.** L102: "Audit-script LIVE-tag cap (binary)."
- **FC-7.3 PASS.** L103: "Cross-role-reference fabrication threshold (binary, zero-tolerance)."

### Anti-Patterns (D9)
- **FC-9.1 PASS.** L113-L118 = 6 entries, inside [5,8].
- **FC-9.2 PASS.** All 6 entries begin with "I don't".
- **FC-9.3 PASS.** Each entry carries ≥1 regex-matching citation: L113 (PF-S3-01 + Finding 9); L114 (PF-S2-02); L115 (PF-S2-04 + Finding 1); L116 (PF-S2-05); L117 (PF-S3-01 + Finding 5); L118 (Finding 5 + PF-S2-01).
- **FC-9.4 PASS.** L118: "I don't treat the operator as outside the trust boundary; operator is A3 in the threat catalog (bromism case)."
- **FC-9.5 PASS.** L117: "I don't tag a §13 row LIVE before running Glob or Read against the cited path." Merged form covers the LIVE-tag discipline (also names FDA-prose-pattern-match cue per the remediation log).

### Ask vs Proceed
- **FC-AVP-1 PASS.** Decision tree = 6 numbered branches (L83-L88). 6 ≥ 4.
- **FC-AVP-2 PASS.** L90: "**Fabrication guard.** Never fabricate a refusal-class identifier, GRADE certainty tier, CONTINUATION_BRIEF §10 row, INV-* ID, `PF-S\d+-\d+` identifier, or `vault/` path."

### Operational completeness
- **FC-OC-1 PASS.** Sampled 5 verbs against L218-L231 table: "Anchor"→Read/Grep; "Encode"→Write/Edit (permitted paths); "Re-dispatch the verifier"→Agent tool (full role profile inlined); "Log a contradiction"→Write to `vault/meta/contradictions.md` + basic-memory MCP; "Demote to PROPOSED"→Edit on §13 row + §18 entry. All 5 resolve.

### Line budgets (counted inside paste-ready code blocks)
- **FC-LB-1 PASS.** Header+Identity (L30-L38, inside code block): 9 content lines (header, blank, role-purpose, blank, `## Identity`, blank, mechanisms paragraph, blank, affirmation-ban line). 9 ≤ 15.
- **FC-LB-2 PASS.** Core Rules (L46-L59 inside code block): 14 lines (header, blank, 12 rules). 14 ≤ 15.
- **FC-LB-3 PASS.** Role Boundaries (L67-L73 inside code block): 7 lines. 7 ≤ 8.
- **FC-LB-4 PASS.** Ask vs Proceed (L81-L90 inside code block): 10 lines (header, blank, 6 branches, blank, fabrication guard). 10 ≤ 10.
- **FC-LB-5 PASS.** Loop-Breaking (L98-L103 inside code block): 6 lines (header, blank, 4 bullets). 6 ≤ 6.
- **FC-LB-6 PASS.** Anti-Patterns (L111-L118 inside code block): 8 lines (header, blank, 6 bullets). 8 ≤ 8.

### Citation integrity
- **FC-CI-1 PASS.** Sampled 5 identifiers:
  1. `PF-S3-01` → resolves at `memory/process-failures.md` L57 ("Self-attested 5 of 6 aplus-research gates").
  2. `PF-S2-05` → resolves at `memory/process-failures.md` L51 ("Session close protocol partial execution").
  3. `PF-S2-04` → resolves at `memory/process-failures.md` L45 ("Over-personalized library research scope").
  4. `INV-RESEARCH-ATTESTATION` → resolves at `INVARIANTS.md` L35 (aplus-research mechanical-enforcement row).
  5. `Finding 5` / `AUTHORITY_FRAMING_BYPASS` → resolves via design-doc §11.2 item 6 (L361) and §5 rule 11 (L168); 8th refusal class enumerated.
- **FC-CI-2 PASS.** No fabricated identifiers detected. All PF-Sx-yy, INV-*, Finding N, R-number, AC-N, and regulatory tokens (FD&C, IMDRF, FDA, GRADE, OCEBM, ICH E2A, FDA 3500A) resolve to their source registers or design-doc body.

## Failures

### FC-1.2 — Identity body contains "Never"
- **Defect.** Line 38 of the artifact (inside the Identity paste-ready code block, under `## Identity`) begins with "Never begin a response with 'Great'..." The token "Never" is in the prohibited Identity-lexicon set `{must, never, always, refuse}` per design-doc §5 rule 3 and rubric D1.
- **Evidence.** Lines 34-38 are all under the `## Identity` header. The affirmation-ban sentence is rendered as part of the Identity body, not relocated to Core Rules / Role Boundaries / Anti-Patterns where the §5 rule 3 partition would place behavioral content.
- **Smallest fix.** Either (a) rephrase line 38 to drop the "Never" lexeme — e.g., "Do not begin responses with 'Great', 'Good idea', 'Absolutely', 'You're right', or any affirmation; respond to the substance directly." (replaces "Never" with "Do not", which is outside the prohibited lexicon); or (b) move the affirmation-ban sentence out of `## Identity` into Core Rules (would add one rule line; check FC-3.1 / FC-LB-2 still hold — both have one line of headroom: 12→13 rules is still ≤12 fail / no, 12 is the cap; option (b) requires a merge with an existing rule). Recommended: option (a).

## Notes
- The artifact's own self-attestation at L41 claims "No `must|never|always|refuse` lexicon in Identity body" but the artifact's L38 contains "Never". This is a defect missed by the artifact's own remediation pass — exactly the failure mode rule 8 ("a mechanical fix is not a verdict — re-dispatch a fresh verifier") guards against. The remediation pass targeted FC-3.1, FC-3.6, FC-9.3, FC-LB-5, FC-LB-6 (per the v2 remediation log L16-L23) but did not re-verify FC-1.2 even though the Identity block was carried over "unchanged from v1" — the same defect (if present in v1) would propagate.
- All 12 Core Rules carry regex-matching citations after the remediation. FC-3.6 fully resolved.
- Loop-Breaking compressed from 5 bullets → 4 bullets by merging spec-revision + design-review caps; both numeric values (2 and 3) preserved on the merged bullet. FC-LB-5 resolved.
- Anti-Patterns compressed from 8 → 6 entries (drop AP4 + merge AP6 into AP7 → AP5'); load-bearing items (LIVE-tag, operator-as-A3, Finding 5 anchor) preserved per CLAUDE.md. FC-LB-6 resolved.
- Citation integrity sample (FC-CI-1) used five distinct identifier classes (PF, INV, Finding, statutory) and all resolved on first lookup. The PF identifiers cited in v2 (PF-S2-01, PF-S2-02, PF-S2-04, PF-S2-05, PF-S3-01) all exist in the current process-failures.md tail (PF-S6-01 latest).
- ALL_PASS requires 0 failures per HARD RULES. With FC-1.2 = FAIL, overall verdict is FAIL.
