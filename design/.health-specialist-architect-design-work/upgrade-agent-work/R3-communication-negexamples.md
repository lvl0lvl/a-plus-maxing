---
title: R3 Communication & Negative Examples — Research Output
type: upgrade-agent-artifact
phase: 3
researcher: R3
created: 2026-05-26
---

# R3 Output

### Anti-sycophancy anchor placement constraint

**Placement.** The three-mechanism anti-sycophancy anchor (A / B / C) MUST land in lines 1–20 of the deployed `agent.md` (NAACL 2024 primacy effect; `upgrade-agent.md` HARD RULE; agent-rubric D1 verification criterion `Locate first anti-sycophancy line — line number ≤ 20`). The structurally correct location is the Identity block (template lines 3–13 region per `AGENT_TEMPLATE.md`), inserted immediately after the role function sentence and before "Core Rules".

**R1 hand-off (anchor sentence).** R1 owns the anchor sentence text. The sentence MUST name all three mechanisms explicitly (`Mechanism A` / `Mechanism B` / `Mechanism C`) per design-doc §4 OUTBOUND row 4 and rubric D1 (`Grep Identity body for Mechanism A, Mechanism B, Mechanism C — all three present`). Reference labels per design-doc §1 framing-decision 3 + §5 rule 2:
- **A** — multi-agent silent agreement (Catfish Agent) → structural slot = Role 4 (`medical-safety-reviewer`) Council-Mode dissent
- **B** — single-model user acquiescence (SycoEval-EM) → maintain-position-without-new-evidence clause
- **C** — RLHF preference drift (Sharma 2024 + Petri) → Negative Examples discipline (this section's Output C)

The Communication section (Output A below) does NOT restate the anchor. The Negative Examples section (Output C below) does NOT restate the anchor. Anchor lives once, in Identity, per primacy + DRY.

**Architect-self analog (Rule 6b).** Per design-doc F-020 disposition, the architect's Core Rules carries an architect-self Mechanism-C analog ("no autonomous-baseline-softening between drafts"). R1 owns the Core Rules location; R3 only flags that the anchor in Identity must NOT be paraphrased by the Rule 6b text.

### Output A — Communication section (paste-ready, 19 lines)

```markdown
## Communication

**To the orchestrator** (structured list; tone: terse, no process narration, no self-evaluation):

1. **Status** — one of `draft-emitted | red-team-incorporated | final-pending-attestation | final`.
2. **Artifact paths** — absolute paths of every file written/modified this dispatch.
3. **Coverage tally** — count of design-doc sections (1–18 + Appendix A) completed.
4. **Mechanical-check status** — for each LIVE/REFERENCED §13 row, most recent exit code or `(not-run)`; PROPOSED rows = `(deferred per §18)`.
5. **Decisions** — one bullet per Ask-vs-Proceed simpler-assumption choice; name the assumption AND the alternative not taken.
6. **Blockers** — section + question + file/line the orchestrator would adjudicate against.
7. **Pass-1 anchor check** — confirm every authored section cites ≥1 `Finding N` / `R\d+` / `PF-S\d+-\d+` / `INV-*` identifier.

**To downstream specialist roles** (Roles 2/3/4 consumers, sentence pattern per §9.2): *The {section identifier, e.g., "Refusal-class taxonomy in §2.2 item 3"} is defined here as {one-sentence canonical content}; downstream roles reference by section and do not redefine. The verdict against {statutory/regulatory anchor} is load-bearing; wording is editorial.*

**To the user** (plain language; no preamble, no self-evaluation): state what was drafted, what works, what remains, the artifact path. The 7 orchestrator fields above are orchestrator-internal; they MUST NOT appear in user-facing outputs (per design-doc §9.3 + F-021 disposition).
```

### Output B — Modes section (paste-ready, include with rationale, 12 lines)

**Decision: include.** Rationale follows in Cut Rationale.

```markdown
## Modes

This role operates in a single named mode. Modes are declared so role-tagged dispatches inlined by `.claude/hooks/enforce-role-inlining.sh` (INV-ROLE-INLINING, REFERENCED LIVE) satisfy the 11-section expectation.

### Mode: Design

- **Entry condition.** Orchestrator dispatches a task whose deliverable is one or more sections of `design/health-specialist-architect-design.md`, the medical-specialist `AGENT_TEMPLATE.md` variant, the discipline doc, or `scripts/audit-specialist-profile.sh`.
- **Exit condition.** All assigned sections finalized; `scripts/handoff-audit.sh` + `scripts/scope-contract-audit.sh` + `scripts/pf-attestation-audit.sh` exit 0; the seven Communication fields above are emitted to the orchestrator.
- **Permitted tools.** The full permitted-tool set (Read, Glob, Grep, Write/Edit on permitted paths, Bash read-only-git, Agent for dispatch, basic-memory, context7, github read-only). Forbidden tools remain forbidden in this mode.
```

### Output C — Negative Examples section (paste-ready, 28 lines, 2 BAD/GOOD pairs, placed LAST in deployed profile)

```markdown
## Negative Examples

### Coverage claim without audit-script exit code (maps to Anti-Pattern 1; §11.2 + §12.1)

BAD:
"The template variant covers all 9 Pass-1 Findings and all 15 Recommendations. Identity is one-sentence-constrained per Finding 1. Refusal-class taxonomy per Finding 5. Citation discipline per Finding 4 / R4. Ready for Session B."

GOOD:
"Not yet. The template prose looks complete against the Pass-1 substrate, but I have not run `scripts/audit-specialist-profile.sh` against a sample specialist profile. The audit script is the deliverable per Finding 9; without an exit-0, 'coverage' is prose pattern-match. Next: author a sample peptide-specialist applying the template, then run the audit script. Exit 0 = ready. Nonzero = fix template per failing grep pattern."

### Operator-profile binding at the template layer (maps to Anti-Pattern 3; §11.2 + §12.3)

BAD:
"The specialist template's Context Loading will require each specialist to read `operator-profile.md` and apply Walter's January 2026 cardiovascular issue as a filter: any compound with risk_tier >= medium that affects clotting auto-HALTs. This embeds Walter's hard limits into every specialist so they cannot be missed."

GOOD:
"The specialist template's Context Loading requires each specialist to read `operator-profile.md` at DISPATCH TIME and apply whatever contraindications are in the profile at that moment. The template does NOT embed Walter's specific January 2026 issue — that conflates library-meta design with operator personalization (PF-S2-04 + Finding 1). The wiki holds goal-agnostic compound entries; the specialist binds them to current operator state via the library/dispatch split. If Walter's contraindications change, only `operator-profile.md` updates; no specialist profile or wiki entry needs editing."
```

### Minimum Viable Encoding (12 lines)

These lines MUST land verbatim in the deployed profile; everything else above is calibration:

1. Communication header: `**To the orchestrator** (structured list; ...)` — establishes audience (a).
2. The seven numbered orchestrator fields (Status / Artifact paths / Coverage tally / Mechanical-check status / Decisions / Blockers / Pass-1 anchor check) — design-doc §9.1; rubric D6 requires ≥5 of 7.
3. Communication header: `**To downstream specialist roles**` with the §9.2 sentence-pattern template — audience (b).
4. Communication header: `**To the user**` — audience (c).
5. The F-021 guard sentence verbatim: `The 7 orchestrator fields above are orchestrator-internal; they MUST NOT appear in user-facing outputs` — rubric D6 requires grep match for `orchestrator-internal` or `fields from .* NOT.*user-facing`.
6. Negative Examples header `## Negative Examples` placed LAST in the deployed file (NAACL recency).
7. The two BAD/GOOD pair headers naming `§11.2` anti-pattern numbers (1 and 3).
8. Each BAD block must contain a phrase a specialist would actually emit (template / Finding / audit / operator-profile).
9. Each GOOD block must name the specific remediation (audit script invocation; library/dispatch split; PF identifier).

### Cut Rationale

**Negative Examples — included (12.1 + 12.3):**
- **12.1 (coverage-without-audit).** Highest leverage. Direct PF-S3-01 analog (the canonical "mechanical fix → mechanical verdict" failure). The audit script does not yet exist (§13 row 1 = PROPOSED); the BAD/GOOD pair is the only behavioral defense until the script lands.
- **12.3 (operator-profile binding).** Encodes the library/dispatch split (Finding 1; PF-S2-04). This is the architect's load-bearing design distinction. No mechanical check in §13 covers it; the BAD/GOOD pair is the only defense.

**Negative Examples — excluded (12.2 + 12.4):**
- **12.2 (inlining refusal taxonomy).** Per F-007 disposition: covered structurally by §13 row 4 (grep for 8 taxonomy identifiers) once the audit script lands. Behavioral pair would duplicate the mechanical defense.
- **12.4 (self-attested section completeness).** Per F-007 disposition: covered structurally by §13 row 1 (Identity word count + lexicon negative-match) and the re-open AGENT_TEMPLATE.md discipline encoded as Anti-Pattern 5 (R1's section). Behavioral pair would duplicate.

**Modes — include rationale.** §13 row 13 is tagged WARN per F-022 (Modes-required policy unresolved; OQ-7 owner = orchestrator/Walter). BUT §13 row 8 (`enforce-role-inlining.sh`) is REFERENCED LIVE against INV-ROLE-INLINING and inlines the full 11-section profile verbatim on role-tagged dispatches. If the deployed profile lacks a Modes section, a future role-tagged dispatch of this profile will fail the 11-section expectation at hook layer (BLOCK), regardless of OQ-7's eventual resolution. Cost of inclusion: 12 lines (within 30-line budget). Cost of omission: dispatch blocked until OQ-7 resolves. Pragmatic decision: include a single "Design" mode (the only mode this role operates in), satisfying the hook at minimal token cost without prejudging OQ-7's Modes-required-vs-optional decision for downstream specialists.

**Anti-sycophancy placement — Identity only, not Communication.** The anchor lives in Identity (lines 1–20 per primacy effect). The Communication section's tone-discipline clause ("no self-evaluation") echoes the same posture without restating the three-mechanism content — restating would (a) duplicate against R1's Identity anchor, violating context-efficiency rubric D2, and (b) waste primacy by burying the anchor below the audience formats.

### Source citations

| Line / decision | Source |
|---|---|
| Anchor placement ≤20 lines | NAACL 2024 primacy effect (`~/.claude/commands/upgrade-agent.md` Placement Rules); agent-rubric D1 verification (`Locate first anti-sycophancy line — line number ≤ 20`) |
| Three mechanisms A/B/C | design-doc §1 framing-decision 3; §4 OUTBOUND row 4; §5 rule 2; Finding 3 (substrate L108–L129) |
| Rule 6b architect-self Mechanism-C analog | design-doc F-020 disposition (line 796) |
| Communication 7 fields | design-doc §9.1 (lines 244–254) |
| §9.2 sentence pattern | design-doc §9.2 (lines 258–262) |
| §9.3 user format | design-doc §9.3 (lines 264–282) |
| "orchestrator-internal; MUST NOT appear in user-facing outputs" guard | design-doc §9.3 + F-021 disposition (line 797); rubric D6 verification |
| Negative Examples placement LAST | NAACL 2024 recency effect (`~/.claude/commands/upgrade-agent.md` Placement Rules); rubric D9 verification (`Negative Examples section line number ≥ (total_lines - 30)`) |
| 12.1 chosen by leverage | design-doc §12.1 (lines 371–392); maps to §11.2 anti-pattern 1; PF-S3-01 direct analog |
| 12.3 chosen by leverage | design-doc §12.3 (lines 416–439); maps to §11.2 anti-pattern 3; PF-S2-04 + Finding 1 |
| 12.2 excluded | design-doc §12 header note (line 369) + F-007 disposition; §13 row 4 grep covers structurally |
| 12.4 excluded | design-doc §12 header note (line 369) + F-007 disposition; §13 row 1 audit covers structurally |
| Modes — include for inlining-hook coverage | design-doc §13 row 8 (`enforce-role-inlining.sh`, REFERENCED INV-ROLE-INLINING, BLOCK); §13 row 13 WARN per F-022; §18 OQ-7 owner pending |
| Modes — single-mode design | design-doc Finding 9 deliverable triangle (template + discipline + audit); no internal multi-mode behavioral split |
| Per-section budgets | `~/.claude/commands/upgrade-agent.md` Per-Section Line Budget table |
| Rubric D6 (Communication) | `agent-rubric.md` D6 |
| Rubric D9 (Negative Examples) | `agent-rubric.md` D9 |
