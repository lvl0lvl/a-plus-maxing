---
title: Session Kickoff — Pass-2 Role 2 (health-implementer) design doc
type: session-prep
status: ready
created: 2026-05-26
prepared_at: S9 close
target_session: S10 (next session after compaction)
predecessor: design/.health-specialist-architect-design-work/SESSION_B_KICKOFF.md (S9, consumed)
scope: Run design-doc-protocol Phases 1-5 for Role 2 against design/DESIGN_DOC_TEMPLATE.md; inherit OUTBOUND interface contracts from Role 1 §4
---

# Session Kickoff — Pass-2 Role 2 (health-implementer)

This file is the focused operational brief for the next session running Pass-2 design-doc protocol for Role 2 (health-implementer). Role 1 (health-specialist-architect) is **fully deployed** as of S9 close: design-doc Status: Final + project-local agent at `.claude/agents/health-specialist-architect/`. Role 2 design-doc inherits OUTBOUND interface contracts from Role 1's now-Final §4.

Read this in full before any work. If a contradiction surfaces between this brief and source files, source files win — flag back to user.

---

## 0. Pre-flight reads (in this order)

1. **`HANDOFF.md`** — standard session-start; especially S9 close note (the re-scope decision) + Current State + What Is Next + Top-3 failure modes.
2. **`INVARIANTS.md`** — 12-entry register; INV-ROLE-INLINING is load-bearing for any sub-agents dispatched.
3. **`memory/process-failures.md`** — 8 PFs; PF-S3-01 remains the dominant guard during Phase 4 of design-doc-protocol.
4. **`vault/meta/landmarks.md`** — landmark window check.
5. **`design/DESIGN_DOC_TEMPLATE.md`** — canonical contract (781 lines, Status: Final at commit `0563269`); re-read at every section boundary per PF-S2-05.
6. **`design/health-specialist-architect-design.md`** — Role 1's finalized design doc; **§4 OUTBOUND** rows are the inheritance contract for Role 2. Read §2.2 (Role Boundaries with explicit not-owned items pointing at Role 2 = "specialist agent-profile prose"), §4 (8 OUTBOUND rows), §15.2 (7 binary ACs as pattern for Role 2 §15.2).
7. **`design/.health-implementer-design-work/domain-research.md`** — Role 2 Pass-1 substrate (verified exists). Cite Findings by number; do NOT paraphrase.
8. **`design/CONTINUATION_BRIEF.md`** — §3 four compounding lessons, §10 cross-role references, §13 open questions.
9. **`.claude/agents/health-specialist-architect/agent.md`** — Role 1 deployed profile; reference for cross-role escalation contract (Role 2 will write contract-violation findings into Role 2's Phase-3 channel rather than editing Role 1 artifacts).

---

## 1. Scope contract template (for your S10 scope contract)

Per CLAUDE.md session-start step 7, write the contract to HANDOFF.md before any work. Suggested shape:

```markdown
## Scope Contract — Session 10 (YYYY-MM-DD)

Goal: Run design-doc-protocol Phases 1-5 for Role 2 (health-implementer) against design/DESIGN_DOC_TEMPLATE.md. Produce design/health-implementer-design.md with Status: Final. Second end-to-end exercise of the canonical template (first was Role 1 in S8).

Acceptance criteria:
- [ ] AC1 — Phase 1: drafter dispatches (architect / senior-engineer / qa per CONTINUATION_BRIEF §7 v1-substitute path). Each drafter prompt inlines full 11-section role profile verbatim per INV-ROLE-INLINING. Drafts written to design/.health-implementer-design-work/{architect,se,qa}-draft.md. Dispatches recorded in dispatch-ledger.jsonl.
- [ ] AC2 — Phase 2: orchestrator synthesizes design/health-implementer-design.md per DESIGN_DOC_TEMPLATE.md §0.2 frontmatter + 18 sections + Appendix A. Body↔bibliography symmetry check before Phase 3.
- [ ] AC3 — Phase 3: 2 red-team dispatches (`/adversarial-review` skill + medical-safety v1-substitute per CB §7). Findings to red-team-{adversarial,safety}.md.
- [ ] AC4 — Phase 4: PF-S3-01 guard held; each finding personally source-read; classifications in finding-classifications.md with cited evidence for REJECTED rows. Reject-but-adopt pattern applied where appropriate.
- [ ] AC5 — Phase 5: dispositions applied; Appendix A populated; §7 self-attest checklist (17 binary items) executed; frontmatter `status: Final`.
- [ ] AC6 — Close: all 3 audits exit 0 at --session 10; PF attestation canonical form; VOLATILE rotation; feature branch only.

Files I WILL touch: design/health-implementer-design.md, design/.health-implementer-design-work/{drafts/red-team/finding-classifications/dispatch-ledger}, HANDOFF.md, vault/meta/index.md + log.md.

Files I will NOT touch: design/health-specialist-architect-design.md (Status: Final), design/DESIGN_DOC_TEMPLATE.md, .claude/agents/* (Session B per role, separate cycle), vault/library/*, vault/compounds/*, .claude/skills/*, INVARIANTS.md, CLAUDE.md, ~/Documents/Projects/skills_library/* (deploy lives project-local), main branch.

NOT doing: Roles 3/4 Pass-2 (S11/S12), Session B per role (after Pass-2 finalizes), Pass-3 specialists, Phase C peptide campaign, design-doc F-A01 follow-up.

Invariants at risk:
- INV-ROLE-INLINING (drafter dispatches inline 11 sections; hook is mechanical defense)
- PF-S3-01 / AP-ORCH-SELF-ATTEST (Phase 4 falsification window)
- AP-INCOMPLETE-PROPAGATION (Phase 5 disposition application across 18 sections)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH (close discipline)
```

---

## 2. Role 2 specifics (what's different from Role 1)

### Role 2 owns (per Role 1 §2.2 "I do NOT own" item 1)

> Specialist agent-profile prose (health-implementer, Role 2)

Role 2's deliverable is the **prose** that fills the 11-section template variant that Role 1 designed. Concretely: per-specialist drafts (peptide-specialist, labs-specialist, ...) following the medical-specialist `AGENT_TEMPLATE.md` variant — not the template itself.

Role 2 also owns (per Role 1 §2.2 "I do NOT own" items 5, 7):
- Audit-script bash implementation (`scripts/audit-specialist-profile.sh`) — Role 1 designed the interface; Role 2 writes the bash
- IDENTICAL/DIFFER cross-specialist boilerplate discipline (CB §10 row 4)

### Role 2 OUTBOUND inheritance (from Role 1 §4)

Role 2's design-doc §4 will be **INBOUND-only** for the 8 rows Role 1 established:
1. Refusal-class taxonomy (8 classes incl. `AUTHORITY_FRAMING_BYPASS`) — reference by section/anchor; do NOT redefine
2. H-class composition (H1-H8 + worst-case-reachable rule) — reference by anchor
3. GRADE two-axis evidence-tier discipline — reference
4. Three-mechanism anti-sycophancy structural commitment — reference
5. Operator-profile R7 precondition for compound-class writes — Role 2 ENCODES the read-order in specialist Context Loading
6. Contradiction-discipline contract — Role 2 ENCODES the wiki-write protocol
7. aplus-research mode-floor convention — Role 2 ENCODES specialist Tools defaults
8. Role 4 Council-Mode slot — Role 2 references the slot; Role 4 design owns its content

Role 2 will likely surface NEW OUTBOUND rows for Roles 3/4 to inherit (e.g., IDENTICAL/DIFFER discipline per CB §10 row 4).

---

## 3. Known edge cases (carried forward from S8/S9)

**E1. Hook profile-vs-section mismatch (recurrence_count=2).** Same as S7/S8: if drafter role-profile uses non-`## Modes` 11th section (e.g., `## Audit Protocol` for security), hook blocks. Resolution: synthetic `## Modes` pointer OR use `/adversarial-review` skill explicitly without role-tag H1.

**E2. Hook path-pattern over-trigger (recurrence_count=2 — new class from S9).** Hook regex `roles/[a-z-]+/agent\.md` over-triggers on non-role-tagged research dispatches that merely mention a role-profile path. Workaround: refactor path references to directory-only (no `/agent.md` suffix) + avoid canonical H2 patterns (`## Tools`, etc.) in prompt examples.

**E3. Design doc Status: Final = read-only.** Same as S9: Role 1's design doc residual "7-class" prose (F-A01 deferred bead) is upstream; Role 2 design-doc cites Role 1 by section, do NOT inline the residual prose.

**E4. /review-pr architectural-layer-mismatch (NEW, S9).** Watch: Role 2 deploys to `.claude/agents/health-implementer/` at Session B, not skills_library. If /review-pr is run against the Session-B PR, do not force-fix LEGITIMATE findings that name shared-library guardrails — Role 2 is project-local by construction.

**E5. Token-budget overrun.** Role 2 will likely also overshoot the ≤2,000-token target due to inherited medical-domain anchors. Document the overrun in the design-doc adversarial-review characterization; do not aggressively compress at the cost of safety properties.

**E6. F-A01 residual prose in Role 1 design doc** (deferred bead candidate). If Role 2 Phase-3 red-team surfaces the same 7-vs-8 contradiction in Role 1 cited prose, flag it but do NOT edit Role 1's design doc. Surface as Open Question in Role 2 §18.

---

## 4. Sources of truth (frozen for Role 2)

| Artifact | Status | Path |
|---|---|---|
| Role 1 design doc | Final | `design/health-specialist-architect-design.md` |
| Role 1 deployed agent | Final | `.claude/agents/health-specialist-architect/agent.md` |
| DESIGN_DOC_TEMPLATE | Final | `design/DESIGN_DOC_TEMPLATE.md` |
| Role 2 Pass-1 substrate | Final (frozen for this Pass) | `design/.health-implementer-design-work/domain-research.md` |
| CONTINUATION_BRIEF | Final | `design/CONTINUATION_BRIEF.md` |

---

## 5. What the next session does NOT do

- Do NOT modify Role 1 design-doc (Status: Final; defects → bead, not edit)
- Do NOT modify DESIGN_DOC_TEMPLATE.md
- Do NOT deploy Role 2 agent profile (that's Session B per role, after Pass-2 finalizes)
- Do NOT skip Phase 3 red-team even if Phase 2 synthesis "looks clean"
- Do NOT skip the PF-S3-01 personal-source-read discipline at Phase 4
- Do NOT commit to main
- Do NOT promote INV-HARM-CLASS-COMPOSITION to the register unilaterally
- Do NOT address F-A01 residual prose in Role 1 design doc (deferred to its own follow-up)

---

## 6. Falsification windows in S10

S10 is the second end-to-end run of design-doc-protocol against the canonical template. Three failure-mode classes are live:

- **AP-ORCH-SELF-ATTEST (PF-S3-01 class, recurrence_count=2).** Three consecutive guards held: S7 design-doc adversarial, S8 design-doc Phase-4, S9 `/upgrade-agent` Phase-4. S10 is the next test.
- **AP-INCOMPLETE-PROPAGATION.** Phase 5 disposition application across 18 sections + Appendix A is the natural stress case. DESIGN_DOC_TEMPLATE.md §7 self-attest checklist (17 binary items) is the explicit defense.
- **Hook edge cases (both at recurrence_count=2).** If S10 hits either class a third time, structural fix becomes mandatory.

---

## 7. Session-close expectations

At close:
- `design/health-implementer-design.md` exists with `status: Final`; all 18 sections + Appendix A; §7 self-attest 17/17
- All Phase-3 + Phase-4 provenance preserved in `design/.health-implementer-design-work/`
- HANDOFF.md S10 close note + VOLATILE rotation
- `memory/process-failures.md` appended OR PF attestation clean
- All 3 audits exit 0 at `--session 10`
- Commit + push to `feature/wiki-bpc157-aplus-research`
- This file marked `status: consumed`

---

## 8. What to read FIRST after standard session-start protocol

Three load-bearing reads if context is tight:
1. This file (SESSION_KICKOFF.md)
2. `design/DESIGN_DOC_TEMPLATE.md`
3. `design/health-specialist-architect-design.md` §4 (OUTBOUND inheritance contract)
