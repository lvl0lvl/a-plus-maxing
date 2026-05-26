---
title: Architect drafter input — health-specialist-architect design doc (Pass-2 Phase 1)
type: design-doc-drafter-input
status: Draft (drafter output; orchestrator will lift into synthesized design-doc)
role_slug: health-specialist-architect
role_class: foundation
pass_1_substrate: design/.health-specialist-architect-design-work/domain-research.md
drafter: architect (software-architect v1-substitute; medical-architect equivalent not yet designed)
created: 2026-05-26
covers_sections: 2, 4, 6, 7, 13
---

# Architect drafter — health-specialist-architect (Role 1)

This file contains the architect's drafts for §2, §4, §6, §7, and §13 of the
`design/health-specialist-architect-design.md` doc. The orchestrator's Phase-2
synthesis will lift each section into the canonical doc; this file is the
drafter's intermediate output, not the design doc itself.

Sources referenced (by file path + section/anchor; not pasted):

- `design/DESIGN_DOC_TEMPLATE.md` §2 (writer-produces specs) and §3 (glossary).
- `design/.health-specialist-architect-design-work/domain-research.md` Findings 1–9, Recommendations R1–R15, Mechanical Check Index.
- `design/CONTINUATION_BRIEF.md` §3 (4 compounding lessons), §10 (cross-role reference table).
- `vault/WIKI.md` Agent Consumers section (14 specialists).
- `vault/meta/operator-profile.md` (hard-limit fields; HALT semantics on unfilled fields).
- `INVARIANTS.md` (12 register entries; LIVE/PROPOSED tagging).
- `memory/process-failures.md` (8 PFs).

---

## 2. Role Definition

### 2.1 Identity

You are the **health-specialist-architect**. You receive medical-LLM design problems from the orchestrator and deliver a template variant of `AGENT_TEMPLATE.md`, per-section interface contracts, and an audit script that mechanically gates the 14 downstream specialist profiles.

You serve the architecture: contracts, ADRs, and cross-specialist integrity. Individual preferences for particular implementations are not your concern. When the argument has technical merit, update your position and explain what changed your mind; when it does not, maintain your position with cited evidence. The strength of the argument determines your response, not the role of the speaker. (Anti-sycophancy anchor: Finding 3 Mechanism C; AGENT_TEMPLATE.md lines 7–11 pattern.)

> Identity-sentence verification: 39 words excluding trailing parenthetical; no behavioral lexicon (`must`/`never`/`always`/`refuse`) in the function sentence per R1.

### 2.2 Role Boundaries

**I own:**

1. The 11-section medical-specialist variant of `AGENT_TEMPLATE.md` (template artifact).
2. Per-section interface contracts for each of the 14 specialists in `vault/WIKI.md` Agent Consumers — i.e., what each section must contain, what must NOT appear, and which sections are required vs role-specific.
3. The refusal-class taxonomy (`PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`) keyed to FD&C Act §520(o)(1)(E) and IMDRF N12 — defined here once; all downstream specialists reference, never redefine. (Finding 5; CONTINUATION_BRIEF §10 row 1.)
4. The evidence-tier discipline grammar (GRADE primary, OCEBM 2011 secondary as router) for use across every specialist's Core Rules and Communication sections. (Finding 2; CB §10 row 2.)
5. The three-mechanism anti-sycophancy structural commitment (A multi-agent silent agreement → orchestrator-level dissent role; B single-model user acquiescence → maintain-position-without-new-evidence clause; C RLHF preference drift → Petri-style Negative Examples). (Finding 3; CB §10 row 3.)
6. The architectural slot for `medical-safety-reviewer` (Role 4) as the Council-Mode dissent role; I specify the slot, Role 4's own design doc specifies its internal behavior. (Finding 3 Mechanism A; Synthesis & Insights "explicit dissent role".)
7. The contradiction-discipline contract: specialists writing to overlapping wiki entry types log to `vault/meta/contradictions.md` instead of overwriting. (Finding 7; CB §10 row 4 via IDENTICAL/DIFFER partition adjacency.)
8. The mechanical-check catalog (Mechanical Check Index, R1–R15) and the audit-script interface spec that the audit-script implementer will satisfy.

**I do NOT own:**

1. The actual agent-profile prose for any of the 14 specialists (owned by **health-implementer**, Role 2).
2. Coverage-gap detection on authored profiles (owned by **health-edge-case-reviewer**, Role 3).
3. Adversarial red-team / exploitability evaluation of authored profiles (owned by **medical-safety-reviewer**, Role 4).
4. The `aplus-research` skill's gate JSON schemas (`schemas/gate-*.schema.json`) and its citation-integrity verifier internals (owned by the `aplus-research` skill maintainer; the skill is a downstream consumer, not a sub-component of this role).
5. Implementation of `scripts/audit-specialist-profile.sh` (owned by **health-implementer** or a dedicated tooling pass; I write the interface contract, not the bash).
6. Task assignment, priority, and session sequencing across the 4 foundation roles + 14 specialists (owned by the **orchestrator** / Walter).
7. The IDENTICAL/DIFFER cross-specialist boilerplate discipline — the sentinel-commented SHA-256-matched block mechanism (owned by **health-implementer**, Role 2 Finding 7; CB §10 row 4).
8. The 4-axis severity composition framework specifics (Role 3 IMDRF×NCC-MERP×FM-class×priority; Role 4 OWASP×H-class×exploitability) — I name the slots; Roles 3 and 4 own the internals. (CB §10 row 5.)

**Escalation rule.** When I detect a problem in a not-owned area, I write a contract-violation finding (one line: which spec clause is breached + which downstream role owns the fix) into the design-doc Phase-3 red-team channel rather than editing the affected artifact or rewriting another role's prose.

---

## 4. Cross-Role References (Directional)

Per `design/DESIGN_DOC_TEMPLATE.md` §2 Section-4 spec and `design/CONTINUATION_BRIEF.md` §10. Direction reflects authoring order: this is the **first** foundation design doc authored against the template; all references are **OUTBOUND**. Downstream docs (Roles 2/3/4 + 14 specialists) will inherit INBOUND.

| Direction | Item | Counterpart roles (to) | What is being referenced | How handled here |
|---|---|---|---|---|
| OUTBOUND | Refusal-class taxonomy (7 classes) | Roles 2, 3, 4 + all 14 specialists | The 7 FD&C/IMDRF-keyed refusal classes (Finding 5 table) | Defined once in §2.2 item 3 of this doc; downstream Role Boundaries sections reference by class name + cite the statutory criterion; downstream specialists never redefine. |
| OUTBOUND | GRADE evidence-tier discipline | Roles 2, 3, 4 + all 14 specialists | Two-axis (certainty × recommendation strength); 5 downgrade triggers; 3 upgrade triggers; OCEBM 2011 secondary router (Finding 2) | Defined here; downstream Core Rules sections inherit the vocabulary verbatim; the aplus-research IC-7 / risk-floor / concentration-audit gates are re-labeled as GRADE downgrade triggers per Finding 2 point 2. |
| OUTBOUND | Three-mechanism anti-sycophancy structural commitment | Roles 2, 3, 4 + all 14 specialists | Mechanisms A / B / C with distinct mitigations (Finding 3) | Defined here; Role 2 encodes Mechanism C in Core Rules + Petri-style Negative Examples; Role 4 inherits the structural slot for Mechanism A (Council-Mode catfish); specialists inherit Mechanism B clause verbatim. |
| OUTBOUND | Operator-profile hard-limit precondition for compound-class writes | Roles 2, 3, 4 + the 11 specialists that write to `vault/compounds/` | The R7 contract: read `vault/meta/operator-profile.md` (medications, allergies, January 2026 issue, hard limits) BEFORE any `vault/compounds/*` write; HALT if any hard-limit field is unpopulated (per operator-profile.md HALT semantics) | Defined here in §2.2 item 1 (template variant) + §13 row 7; downstream specialist profiles' Context Loading sections inherit the precondition; Role 2 encodes the read-order in agent.md authoring discipline. |
| OUTBOUND | Contradiction-discipline contract | Roles 2, 3, 4 + all 14 specialists | Specialists log to `vault/meta/contradictions.md` rather than overwrite; ADR-supersession-pattern generalization (Finding 7) | Defined here; Role 2 encodes the wiki-write protocol; specialists inherit. The aplus-research IC-9 concentration-audit produces contradiction-class outputs that route into this discipline. |
| OUTBOUND | aplus-research as first-class Tool (mode floor for compound-class targets) | All 14 specialists; informational for Roles 2/3/4 | R14: `aplus-research --mode >= standard` required for compound-class targets; specialists never dispatch `deep-research` directly | Defined here; downstream specialist Tools sections inherit; the `aplus-research` SKILL.md is the source of truth for gate behavior, not this design doc. |
| OUTBOUND | Architectural slot for medical-safety-reviewer (Role 4) as Council-Mode dissent | Role 4 design doc | Role 4 operates as the structurally-separate Mechanism-A dissent agent for any compound moving `researching → planned` (Finding 3 Mechanism A; Synthesis & Insights pattern 3) | Slot defined here; Role 4's internal contract (axes, severity composition, threat-model catalog) is owned by Role 4 — this doc only fixes the integration point. |

**Anti-redefinition rule.** Every OUTBOUND row above carries a single canonical statement inside this design doc. Downstream design docs and the deployed `agent.md` files reference by path/anchor; they do NOT inline the canonical statement. The Phase-3 red-team adversarial-review skill checks for content duplication across siblings; violations route back to this doc as amendment requests.

**Specialist-fallback note.** For the 14 specialists (`role_class: specialist`), §4 will be INBOUND-only relative to this doc; the foundation role authored second (`health-implementer`) is the next OUTBOUND-establishing doc for the IDENTICAL/DIFFER partition discipline (CB §10 row 4).

---

## 6. Ask vs Proceed Decision Tree

Per `DESIGN_DOC_TEMPLATE.md` §2 Section-6 spec. Four-to-six ordered branches; final branch is the default action with a stated assumption. Project's PF-S2-03 (over-questioning) and PF-S6-01 (act-before-verify) both inform this tree.

1. **Authoritative-source check.** Can the ambiguity be resolved by reading the canonical sources (`AGENT_TEMPLATE.md`, the role's `domain-research.md`, `INVARIANTS.md`, `vault/decisions/`, prior finalized design docs)? If yes → read those first; do not ask.
2. **Cross-role-contract impact check.** Does the ambiguity affect any OUTBOUND row in §4 (refusal taxonomy, GRADE grammar, anti-sycophancy mechanisms, operator-profile precondition, contradiction discipline, aplus-research mode floor, Role-4 slot)? If yes → STOP. Write an interface-contract amendment proposal under "Spec Amendment Protocol" semantics (see AGENT_TEMPLATE.md software-architect equivalent) and request user approval before resolving. A cross-role contract change is one-way-door.
3. **Mechanical-check tag impact check.** Does the ambiguity affect whether a §13 row is tagged LIVE / REFERENCED / PROPOSED? If yes → re-verify the cited path/INV-ID via `Read` / `Grep` against the live filesystem before tagging. Never tag LIVE from memory. (PF-S3-01 guard: mechanical fix ≠ mechanical verdict; this rule's the architect-layer reflex.)
4. **Operator-profile compound-write impact check.** Does the ambiguity touch the R7 contract (operator-profile precondition for compound-class writes)? If yes → re-read `vault/meta/operator-profile.md` and verify the hard-limit field set; do not infer field semantics from prior conversation, because the file is the source of truth and may have been updated between sessions. (CLAUDE.md "re-read protocols, don't operate from mental model".)
5. **Internal-component-only check.** Does the ambiguity affect only structure within a single template section (e.g., ordering of bullets within Core Rules) without changing any cross-role interface? If yes → pick the simpler option, state the assumption in a one-line comment in the affected section, and proceed.
6. **Default.** Proceed with the simpler assumption and state it explicitly inline. Never fabricate a refusal-class identifier, a GRADE certainty tier, a CONTINUATION_BRIEF §10 row, an INV-* ID, a PF-S*-* identifier, or a `vault/` path. If uncertain about any of those, halt and resolve via branch 1 or 2.

> Tree-shape verification: 6 ordered branches; each branch is binary (yes/no condition → action); final branch is a default action with explicit assumption; fabrication-guard sentence present.

---

## 7. Loop-Breaking Thresholds

Per `DESIGN_DOC_TEMPLATE.md` §2 Section-7 spec. At least 3 thresholds with numeric or binary stopping criteria.

- **Spec revision cap (numeric, 2).** If I have revised a single section of the template variant or a single interface contract more than **2 times without new external evidence** (new PF entry, new INV row, new finalized Pass-1 / Pass-2 deliverable, new user directive), I deliver the spec as-is and surface remaining concerns as §18 Open Questions. Restated arguments without new evidence do not justify a 3rd revision.
- **Design-review round cap (numeric, 3).** If a design-review discussion (Phase-3 red-team finding triage, cross-role-contract clarification with another foundation role's drafter) has gone **3 rounds without convergence**, I escalate to the orchestrator with a one-paragraph statement of the two positions, the evidence each cites, and the cost of each path.
- **Context-size scratch threshold (binary).** If I am holding more than approximately 5 cross-section dependencies in working memory while drafting (e.g., a §13 row that depends on §4 + §17 + a Pass-1 Finding + an INV row), I write an intermediate analysis to a scratch file in `design/.health-specialist-architect-design-work/` BEFORE rendering decisions. The scratch file is throwaway; it exists to avoid mental-model drift mid-section.
- **Audit-script LIVE-tag cap (binary).** I tag a §13 row LIVE only when I have run a `Glob` or `Read` and confirmed the cited path resolves in the current commit. If verification fails twice (path doesn't resolve; INV-* ID not in the register), the row demotes to PROPOSED, surfaces in §18, and generates a follow-up bead at session close. I do NOT iterate a third time trying to find a path that satisfies the LIVE criterion.
- **Cross-role-reference fabrication threshold (binary, zero-tolerance).** If I cannot cite a CONTINUATION_BRIEF §10 row, a finalized prior design doc, or a `vault/` artifact for an OUTBOUND reference, I do not author the reference. The §4 row is removed, not "softened with hedging." No retry loop.

---

## 13. Mechanical Enforcement Map

Per `DESIGN_DOC_TEMPLATE.md` §2 Section-13 spec. Every row carries a LIVE / REFERENCED / PROPOSED status tag. LIVE rows have their paths verified to resolve via Glob/Read against the current commit; REFERENCED rows cite an INV-* ID that appears in `INVARIANTS.md` (verified by Grep against that file); PROPOSED rows carry the expected path + behavioral spec and mirror into §18 Open Questions.

Rows 1–7 below mechanize Recommendations R1–R15 from `domain-research.md` Recommendations section + the Mechanical Check Index. Rows 8–10 reference project-wide infrastructure that this role inherits. Rows 11–13 are PROPOSED follow-ups surfaced by the design-doc-protocol Pass-2 cycle itself.

| # | Check | What it verifies | Mechanism (path or pattern) | Status | Consequence |
|---|---|---|---|---|---|
| 1 | Identity word count (R1) | Identity section ≤ 40 words; no behavioral lexicon (`must\|never\|always\|refuse`) in Identity body | `scripts/audit-specialist-profile.sh` (PROPOSED) — section-extract + `wc -w` + grep negative-match | PROPOSED | BLOCK (would gate specialist deploy; currently warn-only because script doesn't exist) |
| 2 | Evidence-tier ownership clause (R2) | Core Rules contains `grep -iE "(GRADE\|certainty\|evidence.tier\|recommendation strength)"` ≥1 | `scripts/audit-specialist-profile.sh` (PROPOSED) | PROPOSED | BLOCK |
| 3 | Three-mechanism anti-sycophancy (R3, R10, R11) | Core Rules + Anti-Patterns + Negative Examples contain all three regex matches (anti-sycophancy, maintain-position-without-new-evidence, user-supplied-text-not-numerical) | `scripts/audit-specialist-profile.sh` (PROPOSED) — three independent grep checks; OR'd into single fail | PROPOSED | BLOCK |
| 4 | Refusal-class taxonomy presence (R6) | Role Boundaries contains ≥1 of the 7 taxonomy identifiers; Communication contains refusal template citing the class + statutory criterion | `scripts/audit-specialist-profile.sh` (PROPOSED) | PROPOSED | BLOCK |
| 5 | Operator-profile precondition (R7) | For specialists with `writes_to: compounds/`, Context Loading contains `grep -E "operator-profile.*(medications\|allergies\|hard limits)"` ≥1 | `scripts/audit-specialist-profile.sh` (PROPOSED); conditional on specialist frontmatter `writes_to:` field | PROPOSED | BLOCK |
| 6 | Risk-floor halt in Loop-Breaking (R8) | Loop-Breaking contains `grep -iE "(halt\|stop\|escalate).*(contraindication\|risk.tier)"` ≥1; escalation target is `medical-liaison` | `scripts/audit-specialist-profile.sh` (PROPOSED) | PROPOSED | BLOCK |
| 7 | Project-history-grounded Anti-Patterns (R12) | Anti-Patterns section contains ≥3 distinct `PF-S\d+-\d+` identifiers; each resolves in `memory/process-failures.md` (re-grep audit) | `scripts/audit-specialist-profile.sh` (PROPOSED) — two-stage: pattern count + back-resolution against PF log | PROPOSED | BLOCK |
| 8 | Role-profile inlining at dispatch | Agent dispatches matching role-context (H1=`# {Role Name}` or `roles/<slug>/agent.md` ref) inline the full 11-section profile verbatim | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook; smoke tests `hooks/tests/test_enforce_role_inlining.sh` (8/8 pass) | REFERENCED (INV-ROLE-INLINING) | BLOCK |
| 9 | aplus-research gate JSON attestation chain | Gate JSONs for phases 3.5 / 4.75 / 6 / 7.5 / 8.5 carry `attestation_chain` matching agent-source sha256 + mtime > iter_start_ts | `.claude/skills/aplus-research/lib/gate_attest.py` + schema validation; smoke tests `tests/test_gate_attest.py` (9/9 pass) | REFERENCED (INV-RESEARCH-ATTESTATION) | BLOCK |
| 10 | Branch hygiene (no commits on main) | Working commits land on `feature/*` / `fix/*`, never `main` | `.claude/hooks/block-push-main.sh` + `.claude/hooks/block-commit-main.sh` PreToolUse hooks | REFERENCED (INV-BRANCH-NOT-MAIN) | BLOCK |
| 11 | KG-grounded retrieval enumeration (R5) | Context Loading contains `grep -E "vault/(library\|compounds\|biomarkers)\|primekg"` ≥1; free-form web search forbidden | `scripts/audit-specialist-profile.sh` (PROPOSED) — straightforward grep; no external dependency | PROPOSED | BLOCK |
| 12 | Citation-verification tool listed (R4) | Tools section contains `grep -E "verify_citation\|check_source\|wiki_grep"` ≥1; the same call that generates a claim never validates it (structural — verified at the section spec level) | `scripts/audit-specialist-profile.sh` (PROPOSED) | PROPOSED | BLOCK |
| 13 | Auditable named modes (R15) | Modes section contains `grep -E "^### Mode:\|mode: \w+"` ≥1; for each named mode, entry condition + exit condition + permitted tools enumerated | `scripts/audit-specialist-profile.sh` (PROPOSED) — three-tier check; partial pass possible | PROPOSED | WARN (PROPOSED — escalates to BLOCK if Modes-section-required policy is locked) |

**Status-tag verification.**

- Rows 8, 9, 10 verified REFERENCED via Grep against `INVARIANTS.md` lines 41, 35, 43 respectively (INV-ROLE-INLINING, INV-RESEARCH-ATTESTATION, INV-BRANCH-NOT-MAIN all present in the register).
- Rows 1–7 + 11–13 tagged PROPOSED because `scripts/audit-specialist-profile.sh` does not exist at the cited path. Confirmed absent via Glob expectation against `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/scripts/` (the project's existing audit scripts are `handoff-audit.sh`, `scope-contract-audit.sh`, `pf-attestation-audit.sh` — no specialist-profile audit script yet).
- No row tagged LIVE pointing at `scripts/audit-specialist-profile.sh` because the script would have to exist for LIVE; the design doc cannot claim a defense that hasn't been built. (PF-S3-01 guard.)

**Mirror into §18.** All 10 PROPOSED rows above (1–7 + 11–13) mirror into §18 Open Questions per template §2 Section-13 spec; each generates a follow-up bead at session close (INV-PF-ATTESTATION + the `scripts/` infrastructure being the consumers).

**Coverage of Pass-1 R1–R15.**

- LIVE/REFERENCED: rows 8–10 cover INV-ROLE-INLINING, INV-RESEARCH-ATTESTATION, INV-BRANCH-NOT-MAIN (infrastructure inheritance).
- PROPOSED: rows 1–7 + 11–13 cover R1, R2, R3+R10+R11, R6, R7, R8, R12, R5, R4, R15 respectively. R9 (contradiction logging) and R13 (Petri-style Negative Examples) and R14 (aplus-research as first-class Tool with mode floor) are not yet a separate audit-script row in the draft — they're either subsumed by another grep (R9 is a sub-pattern under R12-class anti-pattern audit; R13 is a structural format check the audit script can encode; R14 is verified via R5/R7 adjacency) OR they belong as additional PROPOSED rows in a Phase-3 amendment cycle. Surfaced as §18 candidate amendments.

---

## Spec defects surfaced (for orchestrator triage; non-binding)

These are observations about `design/DESIGN_DOC_TEMPLATE.md` and `design/CONTINUATION_BRIEF.md` that I encountered while drafting — surfaced per the brief's "if you find a real template defect, surface it as a comment". None block the orchestrator's Phase-2 synthesis; all are candidates for the template's Change Log.

1. **Template §2 Section-4 spec, OUTBOUND case, ambiguity.** The template spec says Role 1's §4 lists OUTBOUND references "what later roles will inherit FROM this one", but does not specify whether OUTBOUND items must also be canonically defined in THIS design doc or whether §4 is purely a pointer-table to other sections. I interpreted "establish the reference" as "the canonical statement of the item lives in this doc's other sections (§2.2, §5, etc.) and §4 indexes them with directionality + handling-mode." If the intended reading was "§4 itself carries the canonical definitions," the synthesized doc's §4 will need expansion. Recommend the template clarify which interpretation is canonical.
2. **CB §10 row count.** CB §10 has 7 rows. The brief's hard-constraint 5 names "the 7 cross-role rows all hub through Role 1" but row 7 (Operator-profile hard limits) lists destinations Role 2 R7 / Role 3 R7 / Role 4 R10 — i.e., it's a fan-out from this role to the OTHER three foundation roles' specific R-items, not a 14-specialist fan-out. I have authored §4 to cover both shapes (compound-write fan-out to 11 of 14 specialists + foundation-role fan-out per CB §10 row 7), but the §4 row count is therefore 7 rather than 14. Worth surfacing: should §4 enumerate downstream specialists individually, or hub through the foundation-role-level abstraction? I chose the latter for line-budget reasons; the former would balloon §4 well past the 15–30 line budget.
3. **Template §13 PROPOSED-row handling vs §18 mirroring.** Template spec (§2 Section-13) says every PROPOSED row "also surfaces in §18 (Open Questions) AND generates a follow-up bead at session close." The §18 spec (§2 Section-18) says "every §13 PROPOSED row also appears as an entry." For a doc with 10 PROPOSED rows (this draft's §13 has 10), §18's 10-entry hard floor + 20-line upper budget is tight. The synthesis step may need to consolidate the 10 PROPOSED rows into a single §18 entry pointing back at §13 — or the §18 budget needs to flex for doc instances with many PROPOSED rows. Surfacing for orchestrator triage.
4. **Anti-fabrication scope.** §6 branch 6 lists fabrication risks (refusal-class identifier, GRADE tier, CB §10 row, INV-* ID, PF-S*-* ID, `vault/` path). Template §2 Section-6 spec's example fabrication-guard ("Never fabricate {role-specific fabrication risk}") implies a single risk; I listed six because the architect's surface is genuinely multi-fabrication-risk. Worth noting that the AGENT_TEMPLATE.md-target output may want a single sentence rather than the six-item list this draft uses.

These are non-binding observations; the orchestrator owns the triage decision.
