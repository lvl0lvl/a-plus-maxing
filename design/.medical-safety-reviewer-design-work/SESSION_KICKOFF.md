---
title: Session Kickoff — Pass-2 Role 4 (medical-safety-reviewer) design doc
type: session-prep
status: ready
created: 2026-05-28
prepared_at: S11 close (compaction prep)
target_session: S12 (next session after compaction)
predecessor: design/.health-edge-case-reviewer-design-work/SESSION_KICKOFF.md (S11, consumed)
scope: Run design-doc-protocol Phases 1-5 for Role 4 against design/DESIGN_DOC_TEMPLATE.md; inherit OUTBOUND interface contracts from Role 1 §4 + Role 2 §4.2 + Role 3 §4.3 (16 rows total)
---

# Session Kickoff — Pass-2 Role 4 (medical-safety-reviewer)

This file is the operational brief for S12 running Pass-2 design-doc protocol for Role 4. Roles 1, 2, 3 are FINAL as of S11 close:
- Role 1 deployed at `.claude/agents/health-specialist-architect/`
- Role 2 Final design doc at `design/health-implementer-design.md` (S10 close; awaits Session B `/upgrade-agent`)
- Role 3 Final design doc at `design/health-edge-case-reviewer-design.md` (S11 close; awaits Session B `/upgrade-agent`)

Role 4 design-doc INHERITS OUTBOUND contracts from ALL THREE prior foundation docs (16 rows total).

Role 4 is the **medical-safety-reviewer**: ADVERSARIAL + RUNTIME-GATING (structurally distinct from Role 3 which is COVERAGE + PRE-DEPLOYMENT per Role 3 §1 gap 1 + Finding 9 Insight). Role 4 dispatches under v1-substitute pattern (software-security agent) during S10 and S11 were stand-ins; S12 produces Role 4's canonical design doc.

Read this in full before any work. If contradiction surfaces between this brief and source files, source files win — flag back to user.

---

## 0. Pre-flight reads (in this order)

1. **`HANDOFF.md`** — S11 close note (2026-05-27) + Top-3 failure modes + Current State + What Is Next + bead state.
2. **`INVARIANTS.md`** — 12-entry register; INV-ROLE-INLINING is load-bearing.
3. **`memory/process-failures.md`** — 8 PFs; PF-S3-01 still the dominant Phase 4 guard.
4. **`vault/meta/landmarks.md`** — landmark window check (no S12 triggers expected).
5. **`design/DESIGN_DOC_TEMPLATE.md`** — canonical contract; re-read at every section boundary per PF-S2-05.
6. **`design/health-specialist-architect-design.md`** — Role 1 Final; **§4 OUTBOUND** rows (8 items) are inheritance contract #1.
7. **`design/health-implementer-design.md`** — Role 2 Final; **§4.2 OUTBOUND** rows (5 items) are inheritance contract #2.
8. **`design/health-edge-case-reviewer-design.md`** — Role 3 Final (S11); **§4.3 OUTBOUND** rows (3 items) are inheritance contract #3. ALSO read §13 (26-row table — Role 4 needs to know what coverage-class checks Role 3 owns so adversarial-class checks don't duplicate), §11.2 + §12 + §14 for shape reference, Appendix A for finding-disposition pattern.
9. **`design/.medical-safety-reviewer-design-work/domain-research.md`** — Role 4 Pass-1 substrate. Cite Findings by number; do NOT paraphrase.
10. **`design/CONTINUATION_BRIEF.md`** — §3 four compounding lessons, §7 v1-substitute drafter rotation table (Roster B status check), §10 cross-role references, §13 open questions.
11. **`.claude/agents/health-specialist-architect/agent.md`** — Role 1 deployed; available as drafter for Phase 1 (Roster B architect).
12. **`templates/refusal-class-taxonomy.yaml`** — canonical 8-class taxonomy. Role 4 likely audits taxonomy-bypass adversarially against specialist profiles.
13. **`templates/specialist-risk-class.yaml`** — 14-specialist risk-class + mode-floor table.

Then check `bd ready` — beads `a-plus-maxing-hca` (P1, hook v2.5 — RECOMMENDED to address before S12 per recurrence=3) and `a-plus-maxing-3y6` (P1, audit-script) may interact with S12 scope.

---

## 1. Pre-S12 prerequisite: address bead `a-plus-maxing-hca` (hook v2.5 punch-list)

Per S11 close: hook E1 (Security profile lacks `## Modes` → enforce-role-inlining.sh BLOCKED Phase-3 medical-safety dispatch) hit at **recurrence_count=3**. Per Rigor Framework Discipline 8, structural fix is now MANDATORY not optional. S12 will dispatch the medical-safety-reviewer profile shape multiple times (drafter + red-team); if E1 hits again it is the 4th occurrence.

**Two options at S12 start:**

- **Option A (recommended):** Address `a-plus-maxing-hca` FIRST as a separate work-unit before Phase 1 dispatch. Likely fix: extend the hook to accept `## Audit Protocol` (and other documented section variants) as 11th-section-equivalents, OR introduce a `## Modes` synonym table.
- **Option B:** Apply the S11 workaround (synthetic `## Modes` section appended to the inlined profile, naming the dispatch's operational mode) and document each application. Risk: E1 recurrence=4 with no structural fix is now a Rigor-Framework violation, not just a PF watch entry.

Decide at S12 scope-contract time. If Option B, flag the choice explicitly and create a follow-up bead to track recurrence escalation.

---

## 2. Scope contract template (for S12)

Per CLAUDE.md session-start step 7. Suggested shape:

```markdown
## Scope Contract — Session 12 (YYYY-MM-DD)

Goal: Run design-doc-protocol Phases 1-5 for Role 4 (medical-safety-reviewer) against design/DESIGN_DOC_TEMPLATE.md. Produce design/medical-safety-reviewer-design.md with Status: Final. Fourth end-to-end exercise of canonical template (Role 1 S8, Role 2 S10, Role 3 S11). Final foundation-role Pass-2; closes the v1-substitute software-security gap that S10 + S11 used to fill the safety red-team slot.

Acceptance criteria:
- [ ] AC0a — Bead `a-plus-maxing-hca` (hook v2.5) addressed OR Option-B workaround flagged. Roster B status verified.
- [ ] AC0b — Roster B status: architect = project-local; SE + QA status determined per Role 2 + Role 3 Session B state at S12 start.
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches, full profiles inlined per INV-ROLE-INLINING.
- [ ] AC2 — Phase 2: orchestrator synthesizes design/medical-safety-reviewer-design.md per template; §4 INBOUND inherits 8 from Role 1 + 5 from Role 2 + 3 from Role 3 = 16 rows by anchor; pre-Phase-3 mechanical checks PASS.
- [ ] AC3 — Phase 3: 2 red-team dispatches (`/adversarial-review` + a v1-substitute for whatever role would normally adversarially-review the medical-safety-reviewer — likely a peer-review pattern; design-doc time will surface this).
- [ ] AC4 — Phase 4: PF-S3-01 guard held — every finding personally source-read; classifications at design/.medical-safety-reviewer-design-work/finding-classifications.md.
- [ ] AC5 — Phase 5: dispositions applied; Appendix A populated; §7 self-attest run; frontmatter status: Final.
- [ ] AC6 — Close: all 3 audits exit 0 at --session 12; PF attestation canonical form; VOLATILE rotation; feature branch only.

Files I WILL touch: design/medical-safety-reviewer-design.md, design/.medical-safety-reviewer-design-work/{drafts,red-team,finding-classifications,dispatch-ledger}, HANDOFF.md, vault/meta/index.md + log.md.

Files I will NOT touch: design/health-{specialist-architect,implementer,edge-case-reviewer}-design.md (Final), design/DESIGN_DOC_TEMPLATE.md, .claude/agents/* (Session B per role), vault/library/*, vault/compounds/*, .claude/skills/*, INVARIANTS.md, CLAUDE.md, ~/Documents/Projects/skills_library/*, main branch.

NOT doing: Role 4 Session B (separate session), Pass-3 specialists, S10/S11/S12 follow-up beads unless on critical path.

Invariants at risk: INV-ROLE-INLINING (drafter dispatches; hook v2.5 status), PF-S3-01 / AP-ORCH-SELF-ATTEST (6th consecutive falsification window), AP-INCOMPLETE-PROPAGATION (Phase 5 across 18 sections + 3 inheritance chains; largest cross-role propagation surface yet), INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH.
```

---

## 3. Role 4 specifics (what's different from Roles 1, 2, 3)

### Role 4 owns (per Role 1 §2.2 "I do NOT own" item 3 + Role 2 §2.2 "I do NOT own" item 3 + Role 3 §2.2 "I do NOT own" item 1)

- **Adversarial red-team probing** for taxonomy bypass, jailbreak-style framings, persuasion-collapse attacks, prompt-injection. (Role 3 catches COVERAGE gaps; Role 4 catches BYPASS gaps — structurally distinct per substrate Insight in Role 3 substrate L298-L300.)
- **3-axis severity composition** (OWASP × H-class × exploitability) per Role 1 §4 OUTBOUND row 2. Role 4 reads Role 3's `severity_proposed.h_class_equivalent_max` (now per S11's embedded NCC MERP → H-class table) and computes `worst_case_reachable`. Final composition: `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`. H1/H2 auto-block.
- **Council-Mode dissent slot** (multi-agent silent-agreement defense; Mechanism A surface (a) per Role 3 §2.1 routing).
- **Runtime-gating** behavior (vs Role 3's pre-deployment coverage gating).

### Role 4 INBOUND inheritance (S12 §4.1 from Role 1 + §4.2 from Role 2 + §4.3 from Role 3)

**8 rows from Role 1 §4 OUTBOUND** (refusal taxonomy / H-class composition / GRADE / three-mechanism anti-sycophancy / R7 operator-profile / contradiction discipline / aplus-research mode floor / Role 4 Council-Mode slot — note Role 4 IS the Council-Mode slot, so this last row is self-referential: Role 4's design doc DEFINES what the slot does).

**5 rows from Role 2 §4.2 OUTBOUND** (IDENTICAL/DIFFER discipline / audit-script bash contract / self-audit-before-return / Architecture Question artifact / per-role mode-floor encoding).

**3 rows from Role 3 §4.3 OUTBOUND** (coverage-gap report schema — Role 4 reads to scope adversarial probes per gap class; 4-axis severity composition input → 3-axis output composition via max(); re-review-on-amendment discipline).

All cited by anchor; canonical content NOT duplicated. §4 directionality is MIXED (INBOUND from 3 prior + OUTBOUND to specialist runtime — Role 4 gates deployment of every specialist agent.md and is the runtime appeal path for any specialist-time HALT).

### Role 4 likely NEW OUTBOUND rows (no Role 5+ Pass-2 follow-up exists; Role 4 OUTBOUND consumes at specialist runtime + Pass-3 specialists)

- Adversarial probe catalog (≥10 probe-classes per substrate Finding patterns); specialists' runtime behavior is tested against this catalog.
- Council-Mode dissent activation protocol (when does Role 4 dispatch a Council-Mode session vs single-instance review?).
- 3-axis severity composition canonical mapping (OWASP × H-class × exploitability → `worst_case_reachable` enum).
- Runtime-HALT propagation contract (specialist HALT → Role 4 appeal → adjudicator).
- Pre-Role-7 (medical-liaison) adjudicator-bridge — Role 7 is the canonical adjudicator but is not deployed; how does Role 4 surface `severity_final` setter in pre-Role-7 phase?

---

## 4. Known edge cases (carried from S7/S8/S9/S10/S11)

**E1. Hook profile-vs-section mismatch (recurrence_count=3; bead `a-plus-maxing-hca` P1).** Mandatory structural fix per Discipline 8. See §1.

**E2. Hook path-pattern over-trigger (recurrence_count=2; same bead).** Workaround held in S10 + S11.

**E3. Status:Final design docs (Roles 1/2/3) = read-only.** Defects → bead, not edit. Role 3 has open bead `a-plus-maxing-hca` (priority P1 hook); no other Role 3 follow-up beads at S11 close.

**E4. Role 4 reviews specialist runtime behavior BUT specialists don't yet exist** (Role 2 Session B + Pass-3 not yet run). Mirror Roles 2 + 3: design doc IS the contract; deployed agent.md is the runtime instance.

**E5. AQ-001 still open** (bead `a-plus-maxing-h1z`). Per-specialist operator-profile field enumeration. Role 4 may need to audit operator-profile reads adversarially (e.g., does the specialist read fields it claims to under adversarial framings?); if so, AQ-001 dependency surfaces. Flag at S12 scope-contract.

**E6. /review-pr architectural-layer-mismatch (recurrence_count=1; S9 surface).** Watch.

**E7. Token-budget characterization** (bead `a-plus-maxing-2qq`). Role 4 deployed agent.md will likely overshoot the 2,000-token target like Roles 1, 2, 3. Document overrun; do NOT aggressively compress at the cost of safety properties.

**E8. Role 4 reviews ITSELF for sycophancy** (Mechanism A Council-Mode is Role 4's own architecture). Recursive concern: Role 4 instances reaching the same erroneous adversarial verdict via silent-agreement. Substrate likely names this; if not, surface as §18 OQ.

**E9. NCC MERP → H-class table is now canonical at Role 3 §4.3 row 2** (S11 Bundle D fix). Role 4's `worst_case_reachable` arithmetic MUST round-trip with Role 3's emission per the contract embedded in Role 3 §4.3 row 2.

---

## 5. Sources of truth (frozen for Role 4)

| Artifact | Status | Path |
|---|---|---|
| Role 1 design doc | Final | `design/health-specialist-architect-design.md` |
| Role 1 deployed agent | Final | `.claude/agents/health-specialist-architect/agent.md` |
| Role 2 design doc | Final | `design/health-implementer-design.md` |
| Role 3 design doc | Final | `design/health-edge-case-reviewer-design.md` |
| DESIGN_DOC_TEMPLATE | Final | `design/DESIGN_DOC_TEMPLATE.md` |
| Role 4 Pass-1 substrate | Final (frozen) | `design/.medical-safety-reviewer-design-work/domain-research.md` |
| Refusal-class taxonomy | committed S10 | `templates/refusal-class-taxonomy.yaml` |
| Specialist risk-class | committed S10 | `templates/specialist-risk-class.yaml` |
| AQ-001 | open | `design/.health-implementer-design-work/architecture-questions/AQ-001-per-specialist-operator-profile-fields.md` |
| NCC MERP → H-class mapping | embedded S11 | Role 3 design doc §4.3 row 2 |

---

## 6. What S12 does NOT do

- Do NOT modify Roles 1/2/3 design docs (Status: Final; defects → beads)
- Do NOT modify DESIGN_DOC_TEMPLATE.md, AGENT_TEMPLATE.md, INVARIANTS.md, CLAUDE.md
- Do NOT deploy Role 4 agent profile (Session B per role)
- Do NOT run Roles 2 + 3 Session B (`/upgrade-agent`) unless explicitly authorized
- Do NOT skip Phase 3 red-team even if Phase 2 synthesis looks clean
- Do NOT skip PF-S3-01 personal-source-read at Phase 4
- Do NOT commit to main
- Do NOT promote INV-HARM-CLASS-COMPOSITION or any S11 candidate INVs to register unilaterally
- Do NOT work S10 + S11 follow-up beads unless on Role 4 critical path (flag + confirm)

---

## 7. Falsification windows in S12

S12 is the fourth end-to-end run of design-doc-protocol. Three failure-mode classes live:

- **AP-ORCH-SELF-ATTEST (PF-S3-01, recurrence_count=2).** Five consecutive guards held (S7/S8/S9/S10/S11). S12 = 6th test.
- **AP-INCOMPLETE-PROPAGATION.** S12's §4 INBOUND inherits from THREE prior design docs (8 + 5 + 3 = 16 anchor citations). Largest cross-role propagation surface yet. §7 self-attest 17-item checklist is explicit defense.
- **Hook edge cases (recurrence=3; bead `hca` P1).** Mandatory structural fix per Discipline 8. If S12 hits E1 a 4th time WITHOUT addressing hca first, this is a Rigor-Framework escalation event, not a routine PF watch.

---

## 8. Session-close expectations

At close:
- `design/medical-safety-reviewer-design.md` exists with `status: Final`; all 18 sections + Appendix A; §7 self-attest 17/17.
- All Phase-3 + Phase-4 provenance preserved in `design/.medical-safety-reviewer-design-work/`.
- HANDOFF.md S12 close note + VOLATILE rotation per 6-clause rule.
- `memory/process-failures.md` appended OR PF attestation clean (canonical form `S12 close (YYYY-MM-DD): ...`).
- All 3 audits exit 0 at `--session 12`.
- New beads created for S12 deferred work (mirror S10/S11 pattern).
- Commit + push to `feature/wiki-bpc157-aplus-research`.
- This file marked `status: consumed`.

---

## 9. What to read FIRST after standard session-start protocol

Five load-bearing reads if context is tight:
1. This file (SESSION_KICKOFF.md)
2. `design/DESIGN_DOC_TEMPLATE.md`
3. `design/health-specialist-architect-design.md` §4 (8 OUTBOUND rows — INBOUND for Role 4)
4. `design/health-implementer-design.md` §4.2 (5 OUTBOUND rows) + §11.1 + Appendix A
5. `design/health-edge-case-reviewer-design.md` §4.3 (3 OUTBOUND rows) + §13 (26-row table) + Appendix A (32-finding disposition pattern; NCC MERP → H-class table at §4.3 row 2)

---

## 10. Parallel work (not on S12 critical path)

S10/S11 beads S12 should NOT pick up unless explicitly directed:

- `a-plus-maxing-3y6` (P1) — audit-script bash. Becomes Role 2 + Role 3 Session B unblocker; not Role 4 design-doc prerequisite.
- `a-plus-maxing-pmp` (P2) — denylist starter. Pre-Role-4 might intersect — flag at S12 scope contract if Role 4 design touches harmful-content denylist.
- `a-plus-maxing-h1z` (P2) — AQ-001 resolution. May surface in Role 4 critical path (see E5).
- `a-plus-maxing-9yk` (P3) — Roster A rotation. Defers to first PR after Role 2 + Role 3 Session B.

Roster B status at S12 (review at start):
- Architect drafter = project-local `health-specialist-architect` (active since S10).
- SE drafter = v1-substitute software senior-engineer UNLESS Role 2 Session B has deployed `.claude/agents/health-implementer/agent.md` between S11 close and S12 start.
- QA drafter = v1-substitute software qa UNLESS Role 3 Session B has deployed `.claude/agents/health-edge-case-reviewer/agent.md` between S11 close and S12 start.

Most likely state at S12: both Session B's pending → both v1-substitute.

---

## 11. Compaction recovery anchor

If S12 opens after compaction, recovery sequence:
1. Read `HANDOFF.md` (S11 close note + Current State + What Is Next + Top-3 + Landmark check)
2. Read this file
3. Read `INVARIANTS.md` + `memory/process-failures.md` + `vault/meta/landmarks.md`
4. Run `bd ready`
5. Read the 5 load-bearing reads from §9 above
6. Decide hook-fix-pre-S12 (Option A vs Option B per §1)
7. Write S12 scope contract to HANDOFF.md and obtain user confirmation
8. Begin Phase 1 dispatches with Roster B in effect
