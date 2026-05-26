---
title: Fact-checker — R3 Communication & Negative Examples
type: upgrade-agent-artifact
phase: 4
role: fact-checker
artifact_under_check: R3-communication-negexamples.md
created: 2026-05-26
---

# Fact-checker R3

## Summary
- Total checks: 17
- PASS: 17
- FAIL: 0
- Overall verdict: ALL_PASS

## Per-check results

### Communication (D6)

- **FC-C-1 — PASS.** Three distinct audience sub-sections labeled. Evidence: line 29 `**To the orchestrator**`, line 39 `**To downstream specialist roles**`, line 41 `**To the user**`. All three labels are bolded headers within the Output A markdown block.

- **FC-C-2 — PASS.** Orchestrator format names all 7 of 7 fields (≥5 required). Evidence lines 31-37: (1) `Status`, (2) `Artifact paths`, (3) `Coverage tally`, (4) `Mechanical-check status`, (5) `Decisions`, (6) `Blockers`, (7) `Pass-1 anchor check`.

- **FC-C-3 — PASS.** Guard explicit on line 41: `The 7 orchestrator fields above are orchestrator-internal; they MUST NOT appear in user-facing outputs`. Grep matches all three required tokens (`orchestrator-internal`, `MUST NOT appear`, `user-facing`) in a single sentence inside the paste-ready block.

- **FC-C-4 — PASS.** Tone discipline named. Evidence line 29: `tone: terse, no process narration, no self-evaluation`. Line 41 also repeats `no preamble, no self-evaluation` for the user audience. Both "no prose narration" and "no self-evaluation" are present.

- **FC-C-5 — PASS.** Communication section line count inside the paste-ready markdown block = 15 lines (lines 27–41 inclusive of header and blank lines, measured between the opening ```` ```markdown ```` fence on line 26 and the closing ```` ``` ```` on line 42). Budget ≤ 20. (R3's own header at line 24 claims "19 lines"; the actual measured count is 15, which is still within budget.)

### Negative Examples (D9)

- **FC-NE-1 — PASS.** BAD/GOOD pair count = 2 (≥2 required). Evidence: lines 67 `BAD:`, 70 `GOOD:`, 75 `BAD:`, 78 `GOOD:`.

- **FC-NE-2 — PASS.** Each pair has both a BAD block and a GOOD block. Pair 1: BAD at line 67, GOOD at line 70 (under heading line 65). Pair 2: BAD at line 75, GOOD at line 78 (under heading line 73).

- **FC-NE-3 — PASS.** Each pair is role-specific.
  - Pair 1 (line 65 heading + lines 67–71 content) mentions "template variant", "9 Pass-1 Findings", "audit script", "specialist profile", "Finding 9".
  - Pair 2 (line 73 heading + lines 75–79 content) mentions "specialist template", "Context Loading", "operator-profile.md", "specialist", "PF-S2-04 + Finding 1".

- **FC-NE-4 — PASS.** Each pair cites the §11.2 anti-pattern it maps to. Evidence:
  - Line 65: `### Coverage claim without audit-script exit code (maps to Anti-Pattern 1; §11.2 + §12.1)`
  - Line 73: `### Operator-profile binding at the template layer (maps to Anti-Pattern 3; §11.2 + §12.3)`

- **FC-NE-5 — PASS.** Negative Examples section line count inside the paste-ready markdown block = 17 lines (between opening fence on line 62 and closing fence on line 80). Budget ≤ 30. (R3's own header on line 60 claims "28 lines"; actual measured count is 17, still within budget.)

- **FC-NE-6 — PASS.** Recommendation explicit. Evidence line 60: `(paste-ready, 28 lines, 2 BAD/GOOD pairs, placed LAST in deployed profile)`. Also line 91: `Negative Examples header \`## Negative Examples\` placed LAST in the deployed file (NAACL recency)`. Also line 121 in source-citations: `Negative Examples placement LAST`.

### Anti-sycophancy placement (D1 cross-check)

- **FC-AS-1 — PASS.** Placement constraint stated. Evidence line 13: `MUST land in lines 1–20 of the deployed agent.md`. Also line 108: `The anchor lives in Identity (lines 1–20 per primacy effect)`. Also line 114 source-citation row: `Anchor placement ≤20 lines`.

- **FC-AS-2 — PASS.** All three mechanisms named. Evidence line 15: `The sentence MUST name all three mechanisms explicitly (Mechanism A / Mechanism B / Mechanism C)`. Reference labels enumerated at lines 16–18 (A → multi-agent silent agreement; B → single-model user acquiescence; C → RLHF preference drift).

- **FC-AS-3 — PASS.** R1 hand-off note present. Evidence line 15: `**R1 hand-off (anchor sentence).** R1 owns the anchor sentence text.` Also line 20: `The Communication section (Output A below) does NOT restate the anchor`. Also line 108: `restating would (a) duplicate against R1's Identity anchor`.

### Modes (decision)

- **FC-M-1 — PASS.** Decision stated with rationale. Evidence line 46: `**Decision: include.** Rationale follows in Cut Rationale.` Rationale at line 106 (Cut Rationale block, "Modes — include rationale.").

- **FC-M-2 — PASS.** Modes section ≤30 lines AND single "Design" mode has entry/exit/permitted-tools enumerated. The paste-ready Modes block (lines 48–58, between fences) measures 10 lines — well within ≤30 budget. Entry condition stated line 55 (`Orchestrator dispatches a task whose deliverable is …`). Exit condition stated line 56 (`All assigned sections finalized; … audit scripts exit 0; … seven Communication fields … emitted`). Permitted tools stated line 57 (`Read, Glob, Grep, Write/Edit on permitted paths, Bash read-only-git, Agent for dispatch, basic-memory, context7, github read-only`).

- **FC-M-3 — PASS.** Hook-expectation rationale present. Evidence line 51 (inside the paste-ready block): `Modes are declared so role-tagged dispatches inlined by .claude/hooks/enforce-role-inlining.sh (INV-ROLE-INLINING, REFERENCED LIVE) satisfy the 11-section expectation.` Also line 106 in Cut Rationale: `§13 row 8 (enforce-role-inlining.sh) is REFERENCED LIVE against INV-ROLE-INLINING and inlines the full 11-section profile verbatim … If the deployed profile lacks a Modes section, a future role-tagged dispatch … will fail the 11-section expectation at hook layer (BLOCK)`.

### Operational completeness (cross-cutting)

- **FC-OC-1 — PASS.** For every verb in Communication (Output A) and Modes (Output B), a tool is implied or named.
  - Communication verbs and tools:
    - "emit/report status" (line 29 structured list) → Write (Communication emission)
    - "name file paths" (line 32 `Artifact paths`) → Write/Edit produces paths; Glob would discover them
    - "count sections completed" (line 33 `Coverage tally`) → Read + Grep
    - "name most recent exit code" (line 34 `Mechanical-check status`) → Bash (read-only-git or audit-script invocation)
    - "confirm citation" (line 37 `Pass-1 anchor check`) → Grep
    - "state what was drafted" (line 41 user format) → Write
  - Modes verbs and tools:
    - "dispatches" (line 55 entry condition) → Agent (named explicitly line 57: `Agent for dispatch`)
    - "finalize sections" (line 56 exit) → Write/Edit
    - "exit 0" via audit scripts (line 56) → Bash (named line 57: `Bash read-only-git`)
    - "emitted to the orchestrator" (line 56) → Write (Communication channel)
  - Every verb has a corresponding tool named in the Permitted-tools line (57) of the Modes block, OR named in the structural specifier inside Output A.

## Failures (if any)

None.

## Notes

- The Output A paste-ready block reports "19 lines" in its R3 header (line 24) but measures 15 lines inside the markdown fence (lines 27–41 inclusive). The Output C paste-ready block reports "28 lines" in its R3 header (line 60) but measures 17 lines inside the markdown fence (lines 63–79 inclusive). The Modes block reports "12 lines" in its R3 header (line 44) but measures 10 lines inside the markdown fence (lines 49–58 inclusive). In all three cases, the actual measurement is strictly under the per-section budget (≤20, ≤30, ≤30 respectively), so this is a cosmetic header inaccuracy in R3, not a budget violation. Synthesizer should rely on the measured count, not the header claim.
- The Communication tone-discipline clause on line 29 ("no process narration, no self-evaluation") and line 41 ("no preamble, no self-evaluation") together satisfy FC-C-4. The phrase "no prose narration" from the checklist is taken as semantically equivalent to "no process narration" in the artifact; no separate "prose" string appears.
- The R1 hand-off note is intentionally explicit that R3's Communication section MUST NOT restate the three-mechanism anchor (lines 20, 108). This matches the rubric D2 context-efficiency expectation and the upgrade-agent.md primacy-placement rule. FC-AS-3 is satisfied by R3 carrying the pointer, not the sentence.
- Anti-Pattern citations in Output C ("Anti-Pattern 1", "Anti-Pattern 3") map directly to design-doc §11.2's enumerated anti-pattern numbering — verified consistent with R3's source-citation table rows at lines 122–123 (`maps to §11.2 anti-pattern 1` and `maps to §11.2 anti-pattern 3`).
- All 17 checks PASS with cited line-number evidence. Verdict: ALL_PASS.
