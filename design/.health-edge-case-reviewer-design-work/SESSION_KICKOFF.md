---
title: Session Kickoff — Pass-2 Role 3 (health-edge-case-reviewer) design doc
type: session-prep
status: ready
created: 2026-05-27
prepared_at: S10 close
target_session: S11 (next session after compaction)
predecessor: design/.health-implementer-design-work/SESSION_KICKOFF.md (S10, consumed)
scope: Run design-doc-protocol Phases 1-5 for Role 3 against design/DESIGN_DOC_TEMPLATE.md; inherit OUTBOUND interface contracts from Role 1 §4 + Role 2 §4.2
---

# Session Kickoff — Pass-2 Role 3 (health-edge-case-reviewer)

This file is the operational brief for S11 running Pass-2 design-doc protocol for Role 3 (health-edge-case-reviewer). Roles 1 and 2 are FINAL as of S10 close:
- Role 1 deployed at `.claude/agents/health-specialist-architect/`
- Role 2 Final design doc at `design/health-implementer-design.md` (Status: Final; 779 lines; pending /upgrade-agent Session B deploy)

Role 3 design-doc INHERITS OUTBOUND contracts from BOTH prior foundation docs.

Read this in full before any work. If a contradiction surfaces between this brief and source files, source files win — flag back to user.

---

## 0. Pre-flight reads (in this order)

1. **`HANDOFF.md`** — standard session-start; especially S10 close note (2026-05-27) + Top-3 failure modes + Current State + What Is Next + 11-bead open list.
2. **`INVARIANTS.md`** — 12-entry register; INV-ROLE-INLINING is load-bearing for any sub-agents dispatched.
3. **`memory/process-failures.md`** — 8 PFs; PF-S3-01 still the dominant guard during Phase 4.
4. **`vault/meta/landmarks.md`** — landmark window check (no S11 triggers expected).
5. **`design/DESIGN_DOC_TEMPLATE.md`** — canonical contract (781 lines, Status: Final at commit `0563269`); re-read at every section boundary per PF-S2-05.
6. **`design/health-specialist-architect-design.md`** — Role 1 Final; **§4 OUTBOUND** rows (8 items) are inheritance contract for Role 3.
7. **`design/health-implementer-design.md`** — Role 2 Final (S10); **§4.2 OUTBOUND** rows (5 items) are inheritance contract for Role 3. Also read Role 2 §11.1 PF coverage + §13 audit-row table + §14 ECs for cross-reference shape.
8. **`design/.health-edge-case-reviewer-design-work/domain-research.md`** — Role 3 Pass-1 substrate. Cite Findings by number; do NOT paraphrase.
9. **`design/CONTINUATION_BRIEF.md`** — §3 four compounding lessons, §7 v1-substitute drafter rotation table (architect = project-local, SE+QA still v1-sub), §10 cross-role references, §13 open questions.
10. **`.claude/agents/health-specialist-architect/agent.md`** — Role 1 deployed; available as drafter for Phase 1.
11. **`templates/refusal-class-taxonomy.yaml`** — canonical 8-class taxonomy committed S10. Role 3 likely audits specialist profiles' refusal-class enumeration AGAINST this file.
12. **`templates/specialist-risk-class.yaml`** — 14-specialist risk-class + mode-floor table committed S10. Role 3 may audit per-specialist mode-floor correctness.

Then check `bd ready` — six P1-P3 unblocked beads from S10 may interact with S11 scope (especially `a-plus-maxing-3y6` audit-script bash and `a-plus-maxing-h1z` AQ-001 resolution).

---

## 1. Scope contract template (for your S11 scope contract)

Per CLAUDE.md session-start step 7, write the contract to HANDOFF.md before any work. Suggested shape:

```markdown
## Scope Contract — Session 11 (YYYY-MM-DD)

Goal: Run design-doc-protocol Phases 1-5 for Role 3 (health-edge-case-reviewer) against design/DESIGN_DOC_TEMPLATE.md. Produce design/health-edge-case-reviewer-design.md with Status: Final. Third end-to-end exercise of the canonical template (Role 1 S8, Role 2 S10).

Acceptance criteria:
- [ ] AC0 — Roster B status verified: architect drafter = project-local health-specialist-architect (rotation active since S10); SE+QA stay v1-substitute (rotation deferred until Role 2 + Role 3 Session B respectively).
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches inlining full 11-section profiles per INV-ROLE-INLINING; drafts at design/.health-edge-case-reviewer-design-work/{architect,se,qa}-draft.md.
- [ ] AC2 — Phase 2: orchestrator synthesizes design/health-edge-case-reviewer-design.md per template; body↔bibliography symmetry check pre-Phase 3.
- [ ] AC3 — Phase 3: 2 red-team dispatches (/adversarial-review + medical-safety v1-substitute per CB §7).
- [ ] AC4 — Phase 4: PF-S3-01 guard held — every finding personally source-read; classifications at design/.health-edge-case-reviewer-design-work/finding-classifications.md.
- [ ] AC5 — Phase 5: dispositions applied; Appendix A populated; §7 self-attest checklist run; frontmatter status: Final.
- [ ] AC6 — Close: all 3 audits exit 0 at --session 11; PF attestation canonical form; VOLATILE rotation; feature branch only.

Files I WILL touch: design/health-edge-case-reviewer-design.md, design/.health-edge-case-reviewer-design-work/{drafts,red-team,finding-classifications,dispatch-ledger}, HANDOFF.md, vault/meta/index.md + log.md.

Files I will NOT touch: design/health-specialist-architect-design.md (Status: Final), design/health-implementer-design.md (Status: Final), design/DESIGN_DOC_TEMPLATE.md, .claude/agents/* (Session B per role), vault/library/*, vault/compounds/*, .claude/skills/*, INVARIANTS.md, CLAUDE.md, ~/Documents/Projects/skills_library/*, main branch.

NOT doing: Role 2 Session B (separate session), Role 4 Pass-2 (S12), Pass-3 specialists, peptide campaign, S10 follow-up beads (unless one is genuinely on critical path; flag and confirm).

Invariants at risk: INV-ROLE-INLINING (drafter dispatches), PF-S3-01 / AP-ORCH-SELF-ATTEST (Phase 4 fifth consecutive falsification window), AP-INCOMPLETE-PROPAGATION (Phase 5 across 18 sections + 2 inheritance chains), INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH.
```

---

## 2. Role 3 specifics (what's different from Roles 1 + 2)

### Role 3 owns (per Role 1 §2.2 "I do NOT own" item 6 + Role 2 §2.2 "I do NOT own" item 6)

- **Coverage-gap detection** on authored specialist profiles. The implementer (Role 2) emits `.claude/agents/<slug>/agent.md` files; Role 3 reviews each BEFORE deployment for coverage gaps that the audit script can't detect (semantic absences, inheritance breaks, refusal-class enumeration completeness against role domain, sycophancy-collapse detection, contradiction-discipline absence).
- Edge-case catalog discipline (§14-shaped output).
- Coverage-gap report format that orchestrator-accept reads BEFORE deploying the specialist.

### Role 3 INBOUND inheritance (S11 §4.1 from Role 1 + Role 2)

8 rows from Role 1 §4 OUTBOUND (Refusal taxonomy, H-class composition, GRADE two-axis, Anti-sycophancy three-mech, R7 operator-profile, Contradiction discipline, aplus-research mode floor, Role 4 Council-Mode slot) + 5 rows from Role 2 §4.2 OUTBOUND (IDENTICAL/DIFFER discipline, Audit-script bash contract, Self-audit-before-return contract, Architecture Question artifact, Per-role mode-floor encoding). All cited by anchor; canonical content NOT duplicated.

### Role 3 likely NEW OUTBOUND rows (for Role 4 to inherit)

- Coverage-gap report schema (Role 4 reads to scope adversarial probes per gap class).
- 4-axis severity composition for coverage-gap findings (per CB §10 row 5 — Roles 3 + 4 own their axes; Role 3 specifies its own).
- Re-review-on-amendment discipline (when Role 1 design doc amends, Role 3 re-reviews previously-deployed specialists for newly-exposed gaps).

---

## 3. Known edge cases (carried forward from S7/S8/S9/S10)

**E1. Hook profile-vs-section mismatch (recurrence_count=2; bead `a-plus-maxing-hca` open).** Same as S7-S10. Workaround: use `## Modes` as 11th section in all drafter dispatches.

**E2. Hook path-pattern over-trigger (recurrence_count=2; same bead).** Same as S9-S10. Workaround: directory-only path references; avoid canonical H2 (`## Tools`, `## Identity`) inside prompt examples.

**E3. Role 1 + Role 2 design docs Status: Final = read-only.** Defects → bead, not edit. Role 1 has open bead `a-plus-maxing-c7s` (F-A01 7-class residual prose) and `a-plus-maxing-mdg` (§13 header QA-strict amendment). Role 2 has 6 S10-sourced beads.

**E4. Role 3 reviews specialist profiles BUT specialist profiles don't yet exist** (Role 2 Session B hasn't run). Role 3's design doc must anticipate the consumption surface without consuming yet. Mirror Role 2's pattern: design doc IS the contract; deployed agent.md is the runtime instance.

**E5. AQ-001 unresolved** (bead `a-plus-maxing-h1z`). Per-specialist operator-profile field enumeration is open. Role 3 coverage-gap detection MAY need to check operator-profile reads against the enumeration — if so, AQ-001 is on Role 3's critical path; flag for S11 scope-contract decision.

**E6. /review-pr architectural-layer-mismatch (recurrence_count=1; S9 surface).** Watch in case S11 design doc Phase 3 surfaces a structural defect that wants line-fixes when it actually wants a structural rethink.

**E7. Token-budget characterization** (bead `a-plus-maxing-2qq`). Role 3 deployed agent.md will likely overshoot 2,000-token target (same pattern as Roles 1 + 2). Document the overrun in adversarial-review characterization; do NOT aggressively compress at the cost of safety properties.

---

## 4. Sources of truth (frozen for Role 3)

| Artifact | Status | Path |
|---|---|---|
| Role 1 design doc | Final | `design/health-specialist-architect-design.md` |
| Role 1 deployed agent | Final | `.claude/agents/health-specialist-architect/agent.md` |
| Role 2 design doc | Final | `design/health-implementer-design.md` |
| Role 2 deployed agent | NOT YET (Session B pending) | `.claude/agents/health-implementer/agent.md` (does not exist S10 close) |
| DESIGN_DOC_TEMPLATE | Final | `design/DESIGN_DOC_TEMPLATE.md` |
| Role 3 Pass-1 substrate | Final (frozen for this Pass) | `design/.health-edge-case-reviewer-design-work/domain-research.md` |
| CONTINUATION_BRIEF | Final | `design/CONTINUATION_BRIEF.md` |
| Refusal-class taxonomy (NEW S10) | committed | `templates/refusal-class-taxonomy.yaml` |
| Specialist risk-class table (NEW S10) | committed | `templates/specialist-risk-class.yaml` |
| AQ-001 (NEW S10) | open | `design/.health-implementer-design-work/architecture-questions/AQ-001-per-specialist-operator-profile-fields.md` |

---

## 5. What the next session does NOT do

- Do NOT modify Role 1 or Role 2 design docs (Status: Final; defects → beads, not edit)
- Do NOT modify DESIGN_DOC_TEMPLATE.md, AGENT_TEMPLATE.md, INVARIANTS.md, CLAUDE.md
- Do NOT deploy Role 3 agent profile (that's Session B per role, after Pass-2 finalizes)
- Do NOT run Role 2 Session B (`/upgrade-agent` against Role 2 design doc) unless explicitly authorized — likely separate session
- Do NOT skip Phase 3 red-team even if Phase 2 synthesis "looks clean"
- Do NOT skip the PF-S3-01 personal-source-read discipline at Phase 4
- Do NOT commit to main
- Do NOT promote INV-HARM-CLASS-COMPOSITION to the register unilaterally
- Do NOT work the S10 follow-up beads unless one is genuinely on Role 3's critical path (flag + confirm)

---

## 6. Falsification windows in S11

S11 is the third end-to-end run of design-doc-protocol against the canonical template. Three failure-mode classes are live:

- **AP-ORCH-SELF-ATTEST (PF-S3-01 class, recurrence_count=2).** Four consecutive guards held: S7 / S8 / S9 / S10. S11 is the fifth test.
- **AP-INCOMPLETE-PROPAGATION.** S11's §4 INBOUND inherits from BOTH Role 1 (8 rows) AND Role 2 (5 rows) — 13 anchor citations to keep faithful. The §7 self-attest 17-item checklist in DESIGN_DOC_TEMPLATE.md is the explicit defense.
- **Hook edge cases (both at recurrence_count=2; bead `a-plus-maxing-hca` open).** S10 hit zero blocks with workarounds applied. If S11 hits either class a third time, structural fix becomes mandatory.

---

## 7. Session-close expectations

At close:
- `design/health-edge-case-reviewer-design.md` exists with `status: Final`; all 18 sections + Appendix A; §7 self-attest 17/17.
- All Phase-3 + Phase-4 provenance preserved in `design/.health-edge-case-reviewer-design-work/`.
- HANDOFF.md S11 close note + VOLATILE rotation per 6-clause rule.
- `memory/process-failures.md` appended OR PF attestation clean (canonical form `S11 close (YYYY-MM-DD): ...`).
- All 3 audits exit 0 at `--session 11`.
- New beads created for S11 deferred work (mirror S10 pattern).
- Commit + push to `feature/wiki-bpc157-aplus-research`.
- This file marked `status: consumed`.

---

## 8. What to read FIRST after standard session-start protocol

Four load-bearing reads if context is tight:
1. This file (SESSION_KICKOFF.md)
2. `design/DESIGN_DOC_TEMPLATE.md`
3. `design/health-specialist-architect-design.md` §4 (OUTBOUND row 1-8 — INBOUND for Role 3)
4. `design/health-implementer-design.md` §4.2 (OUTBOUND row 1-5 — INBOUND for Role 3) + §11.1 (PF coverage table — pattern for Role 3 §11.1) + Appendix A (Role 2's 40-finding disposition table — pattern for Role 3 Appendix A)

---

## 9. Parallel work (not on S11 critical path)

These are S10-sourced beads that S11 should NOT pick up unless explicitly directed:

- `a-plus-maxing-3y6` (P1) — audit-script bash. Will become Role 2 Session B unblocker; not Role 3 design-doc prerequisite. Probably a dedicated session.
- `a-plus-maxing-9yk` (P3) — Roster A rotation (/review-pr). Defers to first PR after Role 2 Session B.
- `a-plus-maxing-h1z` (P2) — AQ-001 resolution. MAY become Role 3 critical path; flag at S11 scope contract.
- `a-plus-maxing-pmp` (P2) — denylist starter. Pre-Role-4 (S12); not Role 3 prerequisite.

Roster B status at S11: architect drafter = project-local health-specialist-architect (active since S10). SE drafter = v1-substitute software senior-engineer (rotates to health-implementer once Role 2 Session B deploys; S11 likely PRE that, so SE stays substitute). QA drafter = v1-substitute software qa (rotates after Role 3 Session B — so S11 is the LAST cycle running v1-substitute QA).

---

## 10. Compaction recovery anchor

If S11 opens after compaction, recovery sequence:
1. Read `HANDOFF.md` (S10 close note + Current State + What Is Next + Top-3 + Landmark check)
2. Read this file
3. Read `INVARIANTS.md` + `memory/process-failures.md` + `vault/meta/landmarks.md`
4. Run `bd ready`
5. Read the 4 load-bearing reads from §8 above
6. Write S11 scope contract to HANDOFF.md and obtain user confirmation
7. Begin Phase 1 dispatches with Roster B rotation in effect (architect = project-local; SE+QA = v1-sub)
