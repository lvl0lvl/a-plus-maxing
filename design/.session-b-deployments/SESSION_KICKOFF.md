---
title: Session Kickoff — S13 Sessions B (deploy Roles 2, 3, 4 as agents)
type: session-prep
status: consumed
created: 2026-05-28
prepared_at: S12 close (compaction prep)
target_session: S13 (next session after compaction)
predecessor: design/.medical-safety-reviewer-design-work/SESSION_KICKOFF.md (S12, consumed)
scope: Run `/upgrade-agent` against the 3 Final foundation design docs (Roles 2, 3, 4) to produce `.claude/agents/<role>/agent.md` for each; closes Session B debt = 3 per PF-S12-01 AP-DEFERRED-LOOP-CLOSURE recurrence_count=3 mandatory structural fix
session_b_debt_at_start: 3
---

# Session Kickoff — S13 Sessions B (deploy Roles 2, 3, 4 as agents)

This file is the operational brief for S13 running 3 sequential Session B deployments. Roles 2, 3, 4 design docs are Final at S10/S11/S12 close. Role 1 is already deployed.

S13 closes the Session B debt named in PF-S12-01 (AP-DEFERRED-LOOP-CLOSURE). After S13, Roster B for any future Pass-2 or Pass-3 cycle uses 4 deployed canonical agents instead of v1-substitutes for SE + QA + safety-red-team slots.

**Read this file in full before any work.** If contradiction surfaces between this brief and source files, source files win — flag back to user.

---

## 0. Pre-flight reads (in this order)

1. **`HANDOFF.md`** — S12 close note (2026-05-28) + Top-3 failure modes (AP-DEFERRED-LOOP-CLOSURE is #1) + Current State + What Is Next + Landmark check.
2. **`memory/process-failures.md`** — PF-S12-01 entry (the failure being remediated this session) + PF-S3-01 (still the dominant verdict-self-attestation guard).
3. **`INVARIANTS.md`** — 12-entry register; INV-ROLE-INLINING is load-bearing for Session B dispatches.
4. **`vault/meta/landmarks.md`** — landmark window check (no S13 triggers expected).
5. **`design/health-implementer-design.md`** — Role 2 Final at S10 close. Status: Final. The first Session B target.
6. **`design/health-edge-case-reviewer-design.md`** — Role 3 Final at S11 close. Second Session B target.
7. **`design/medical-safety-reviewer-design.md`** — Role 4 Final at S12 close. Third Session B target.
8. **`.claude/agents/health-specialist-architect/agent.md`** — Role 1 reference deployment (the only agent that already exists; reference shape for what S13 produces).
9. **`~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`** — canonical agent template structure.
10. **`/upgrade-agent` skill** — read SKILL.md fully before first dispatch. The skill is the canonical mechanism producing `.claude/agents/<role>/agent.md` from a design doc.
11. **bead `a-plus-maxing-ams`** (P1) — PF-S12-01 structural fixes; NOT the path picked for S13. The path picked is "close the debt directly" not "build the audit." Bead ams remains open for a later session.

Then check `bd ready` — beads `a-plus-maxing-3y6` (P1 audit-script) and `a-plus-maxing-ams` (P1 PF-S12-01 structural fixes) are NOT on S13 critical path. Open beads inventory:
- P1: `3y6` (audit-script + smoke tests), `ams` (PF-S12-01 mechanical enforcement)
- P2: `pmp` (denylist starter), `h1z` (AQ-001 resolution), `rc1` (hook v2.5 E2 follow-up)
- P3+: mdg, 5by, 2qq, 1ox, 9yk, 6ln, c7s

---

## 1. PF-S12-01 recurrence-guard check (mandatory at session-start)

Per PF-S12-01 recurrence guard, orchestrator MUST at session-start:

```bash
# 1. Deployed agents
ls .claude/agents/

# 2. Final design docs
ls design/*-design.md | grep -v DESIGN_DOC_TEMPLATE

# 3. Compute set difference
# Expected at S13 start: deployed = {health-specialist-architect}; Final = {health-specialist-architect, health-implementer, health-edge-case-reviewer, medical-safety-reviewer}; Debt = 3 (Roles 2, 3, 4)
```

If debt count ≥ 1 (it is — count is 3), FIRST work-unit offered is "close Session B for oldest debt" = **Role 2 Session B**.

User has pre-authorized this path at S12 close: "we are going to build the agents in the next session (the ones we have the design docs for)."

This authorization carries forward to S13 scope contract. No alternate path needed.

---

## 2. Scope contract template (for S13)

Per CLAUDE.md session-start step 7 + PF-S12-01 Structural-1 expectation. Suggested shape:

```markdown
## Scope Contract — Session 13 (YYYY-MM-DD)

Goal: Run /upgrade-agent against Roles 2, 3, 4 design docs to produce `.claude/agents/<role>/agent.md` for each. Closes Session B debt = 3 per PF-S12-01 mandate (path 1 remediation: close debt directly). Three Session B deployments sequential within one session OR split across 2-3 sessions per user preference at session-start.

Roster B status (per PF-S12-01 Structural-1 expectation, surfaced at S13 mid-session if not at session-start):
- Architect: deployed (.claude/agents/health-specialist-architect/) since S9
- SE drafter: v1-substitute (Role 2 Session B is THIS SESSION's first work-unit)
- QA drafter: v1-substitute (Role 3 Session B is THIS SESSION's second work-unit)
- Safety red-team: v1-substitute (Role 4 Session B is THIS SESSION's third work-unit)
Cumulative-deferral count: 3 → 0 expected at S13 close (or 3 → N where N is unclosed-at-S13-end if user splits across sessions)

Acceptance criteria (3-deployment variant):
- [ ] AC1 — Role 2 `/upgrade-agent` produces `.claude/agents/health-implementer/agent.md` with Phase 7 final-corrections all PASS
- [ ] AC2 — Role 3 `/upgrade-agent` produces `.claude/agents/health-edge-case-reviewer/agent.md` with Phase 7 final-corrections all PASS
- [ ] AC3 — Role 4 `/upgrade-agent` produces `.claude/agents/medical-safety-reviewer/agent.md` with Phase 7 final-corrections all PASS
- [ ] AC4 — Each deployed agent.md passes the generic Phase-7 constraints (line count ≤200, token count ≤2,000, all AGENT_TEMPLATE.md sections present, library-index reference paths resolve, voice-register checks)
- [ ] AC5 — Each deployed agent.md's role-specific 15.2b post-deployment ACs evaluated (LIVE checks pass; PROPOSED checks flagged for follow-up beads if not yet implemented)
- [ ] AC6 — Session B debt at close = 0 (3 deployments completed) OR explicit user-cited rationale for partial completion (e.g., "deploy Role 2 only at S13; Role 3 + Role 4 at S14")
- [ ] AC7 — Close: all 3 audits exit 0 at --session 13; PF attestation canonical S13 close form; VOLATILE rotation; feature branch only.

Files I WILL touch:
- `.claude/agents/health-implementer/agent.md` (NEW, per /upgrade-agent output)
- `.claude/agents/health-edge-case-reviewer/agent.md` (NEW)
- `.claude/agents/medical-safety-reviewer/agent.md` (NEW)
- `~/Documents/Projects/skills_library/roles/health-implementer/` (NEW per Role 1 precedent — canonical agent.md location; .claude/agents symlinks per ADR vault/decisions/2026-05-26-foundation-role-agent-md-location.md)
- Same for health-edge-case-reviewer + medical-safety-reviewer
- HANDOFF.md (contract + close + VOLATILE rotation)
- vault/meta/index.md, vault/meta/log.md (appends per deployment)
- `.beads/*` via `bd` CLI (Session B beads if/when Structural-3 ships; for now, manual note in HANDOFF if any post-deployment §15.2b ACs need beads)
- `memory/process-failures.md` (only if new PF surfaces during deployment)

Files I will NOT touch:
- `design/health-{implementer,edge-case-reviewer,medical-safety-reviewer}-design.md` (Status: Final at S10/S11/S12; design docs are READ-ONLY inputs to /upgrade-agent; any defects discovered → bead + close-out, NOT in-place edit)
- `design/DESIGN_DOC_TEMPLATE.md`, `design/CONTINUATION_BRIEF.md`
- `.claude/agents/health-specialist-architect/` (Role 1 deployed; no S13 modification)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `CLAUDE.md` (would only change if PF-S12-01 Structural-1 ships this session — out of scope for the "close debt" path)
- `INVARIANTS.md` (Structural-5 ship would change this; out of scope for S13)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Pass-3 specialist design docs (S14+ candidates after debt closes)
- Phase-C peptide library campaign (S14+ candidates)
- PF-S12-01 Structural-2 (audit script) + Structural-3 (auto-bead) — bead `ams` tracks; NOT path 1 ("close debt directly" was user's pick)
- Bead `3y6` (audit-script) — not on S13 critical path
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)

Invariants at risk:
- INV-ROLE-INLINING — /upgrade-agent dispatches must inline full role context per the hook (hook v2.5 LIVE since S12)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN — standard close discipline
- AP-DEFERRED-LOOP-CLOSURE — S13 IS the remediation; falsification window AT this session
- AP-ORCH-SELF-ATTEST (PF-S3-01) — 7th consecutive guard at /upgrade-agent Phase 4-6 validation cycles
- INV-SESSION-B-INTERLEAVING candidate — promote-or-defer surface arrives at first post-debt-close cycle (S14 candidate)
```

---

## 3. /upgrade-agent invocation per role (high-level template)

For each role, the /upgrade-agent skill consumes the design doc and produces `.claude/agents/<role>/agent.md`. The skill's 8-phase pipeline (per `~/.claude/commands/upgrade-agent.md` or wherever the canonical skill lives):

1. **Phase 1 Baseline.** Read design doc §1, §15.2, Appendix A.
2. **Phase 2 Rubric Construction.** Read design doc §15 to build per-agent rubric.
3. **Phase 3 Research Agents (R1 Behavioral, R2 Structural, R3 Communication).** Each consumes a slice of the design doc + role profile.
4. **Phase 4 Validation Loop.** Fact-checker verifies §13 LIVE checks resolve; judge verifies design doc → agent.md content coverage.
5. **Phase 5 Synthesis.** Combine R1/R2/R3 outputs + design doc §2.1 + §5 + §11 + §12 into draft agent.md.
6. **Phase 6 Adversarial Review.** Same `/adversarial-review` shape used in design-doc-protocol Phase 3, applied to the synthesized agent.md.
7. **Phase 7 Final Corrections.** Generic constraints (≤200 lines, ≤2,000 tokens, AGENT_TEMPLATE.md sections present, library-index reference paths resolve, voice-register checks).
8. **Phase 8 Close Out.** Write agent.md to `~/Documents/Projects/skills_library/roles/<role>/agent.md` (canonical) + symlink to `.claude/agents/<role>/agent.md` (per ADR vault/decisions/2026-05-26-foundation-role-agent-md-location.md). Update catalog. Surface Open Questions as bead candidates.

**Critical discipline carries from Pass-2 to Session B:**
- PF-S3-01 guard: at Phase 4 + Phase 6, every adversarial finding is personally source-read against design doc cited evidence; no orchestrator self-attestation
- INV-ROLE-INLINING: every sub-agent dispatch inlines full profile per hook v2.5
- Reject-but-adopt pattern: applies at Phase 6 findings classification

---

## 4. Role-specific notes for S13

### 4.1 Role 2 health-implementer (first work-unit)

- **Design doc:** `design/health-implementer-design.md` (S10 Final).
- **Substrate-line anchors:** Role 2 §3 has 15 Findings + 15 Recommendations; §4.1 INBOUND from Role 1 (8 rows); §4.2 OUTBOUND establishes IDENTICAL/DIFFER discipline + audit-script bash contract.
- **Expected deployed agent role:** SE-equivalent in medical domain. After S13 close, this agent replaces software-SE v1-substitute in any future Pass-2 cycle's drafter pool.
- **Phase 6 adversarial-review will likely surface:** PF-S2-04 / PF-S2-06 surfaces for SE-side work; AC-deploy tautology surfaces (S10 PF watch item recurrence_count=1).
- **§13 PROPOSED rows:** Role 2 owns `scripts/audit-specialist-profile.sh` per §4.2 OUTBOUND row 2. The deployed agent.md should reference this script in its Tools/Modes section even though the script is PROPOSED (PROPOSED-with-bead pattern; bead `3y6` tracks).

### 4.2 Role 3 health-edge-case-reviewer (second work-unit)

- **Design doc:** `design/health-edge-case-reviewer-design.md` (S11 Final, 887 lines).
- **Substrate anchors:** §4.3 OUTBOUND row 2 carries the NCC MERP → H-class canonical mapping (load-bearing for Role 4 consumer).
- **Expected deployed agent role:** QA-equivalent in medical domain. After S13 close, this agent replaces software-QA v1-substitute.
- **Phase 6 likely surfaces:** Mechanism A intra-role cosine-similarity audit (§13 row 24 in Role 3 doc; row 22 in the Role 4 doc) — calibration concern carries to the deployed agent.
- **AQ-001 inheritance:** Role 3 §13 row 5 PROPOSED operator-profile-under-coverage in prose-only mode pre-AQ-001-resolution. The deployed agent.md inherits this; bead `h1z` tracks.

### 4.3 Role 4 medical-safety-reviewer (third work-unit)

- **Design doc:** `design/medical-safety-reviewer-design.md` (S12 Final, 874 lines).
- **Substrate anchors:** §4.4 OUTBOUND 9 rows including row 9 Council-Mode (added at synthesis per OQ-4); §13 27 rows; §18 10 OQs.
- **Expected deployed agent role:** Safety-red-team-equivalent in medical domain. After S13 close, this agent replaces software-Security-profile-as-medical-safety-v1-substitute used at S10/S11/S12 Phase 3.
- **Phase 4 + Phase 6 likely surfaces:** Largest design-doc-to-agent-md compression (874 lines → ≤200 lines target); the 27 §13 rows + 24 §15.2b ACs all need to land in agent.md in compact form.
- **Token-budget overrun expected.** Per Role 4 §17.1 Risk-Token-Budget (implicit at Pass-2; surfaces at /upgrade-agent Phase 7). Bead `2qq` tracks token-budget characterization ADR.

---

## 5. Known edge cases (carried from S7–S12)

**E1. Hook v2.5 LIVE (recurrence_count=3 closed at S12).** No workaround needed for `## Modes` / `## Audit Protocol` / `## Task Routing` slot synonyms; Role 4 design doc uses `## Modes` per Role 1 precedent; Role 2 + Role 3 design docs use `## Modes` similarly.

**E2. Hook path-pattern over-trigger (recurrence_count=2; bead `rc1` P2).** Workaround held in S10/S11/S12. Continues to hold at S13.

**E3. Final design docs (Roles 2/3/4) = read-only at S13.** /upgrade-agent consumes the design doc; defects → bead, not edit. Per S12 close, Roles 2/3/4 design docs are stable Final.

**E4. PF-S12-01 recurrence guard active.** If S13 mid-session, user (or orchestrator) considers pivoting to Pass-3 work without closing all 3 Session B's, PF-S12-01 recurrence_count would promote to 4. Mandatory pause at any such pivot; explicit user override + cited rationale required.

**E5. AQ-001 inheritance.** Open at S13 start; both Role 3 + Role 4 deployed agents inherit the prose-only-mode surface. Bead `h1z`.

**E6. Token-budget characterization.** Bead `2qq` deferred from S10; surfaces at Role 4 /upgrade-agent Phase 7 (and possibly Role 3 Phase 7). Document overruns; do NOT aggressively compress at the cost of safety properties.

**E7. PF-S3-01 7th consecutive guard.** At each /upgrade-agent Phase 4 + Phase 6, personally source-read every finding against design doc cited evidence. Six consecutive guards held (S7/S8/S9/S10/S11/S12).

**E8. AP-INCOMPLETE-PROPAGATION at agent.md authoring.** The design-doc-to-agent.md mapping is a NEW propagation surface; row numbers + AC numbers + OQ numbers in the design doc may need to be reflected in the agent.md, or may need to be hidden (agent.md doesn't carry design-doc internal row IDs). Phase 6 adversarial review is the catch mechanism; orchestrator post-synthesis grep audit is the second-line defense.

---

## 6. Sources of truth (frozen for S13)

| Artifact | Status | Path |
|---|---|---|
| Role 1 deployed agent | Final | `.claude/agents/health-specialist-architect/agent.md` |
| Role 1 design doc | Final (S8) | `design/health-specialist-architect-design.md` |
| Role 2 design doc | Final (S10) | `design/health-implementer-design.md` |
| Role 3 design doc | Final (S11) | `design/health-edge-case-reviewer-design.md` |
| Role 4 design doc | Final (S12) | `design/medical-safety-reviewer-design.md` |
| DESIGN_DOC_TEMPLATE | Final (S7) | `design/DESIGN_DOC_TEMPLATE.md` |
| AGENT_TEMPLATE | reference | `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` |
| Refusal-class taxonomy | committed S10 | `templates/refusal-class-taxonomy.yaml` |
| Specialist risk-class | committed S10 | `templates/specialist-risk-class.yaml` |
| Hook v2.5 | LIVE since S12 | `.claude/hooks/enforce-role-inlining.sh` |
| ADR canonical-path | committed S7 era | `vault/decisions/2026-05-26-foundation-role-agent-md-location.md` |
| /upgrade-agent skill | reference | location TBD at S13 session-start (likely `~/.claude/commands/upgrade-agent.md` or `~/.claude/skills/upgrade-agent/`) |
| PF-S12-01 | LIVE | `memory/process-failures.md` |
| Bead `ams` (P1) | OPEN | bd issue tracker — PF-S12-01 mechanical-enforcement fixes |

---

## 7. What S13 does NOT do

- Do NOT modify Roles 2/3/4 design docs (Status: Final; defects → beads)
- Do NOT modify DESIGN_DOC_TEMPLATE.md, AGENT_TEMPLATE.md, INVARIANTS.md, CLAUDE.md
- Do NOT promote candidate INVs (INV-HARM-CLASS-COMPOSITION, INV-DEPLOY-VERDICT-BINARY, INV-SESSION-B-INTERLEAVING) unilaterally
- Do NOT skip PF-S3-01 personal-source-read at /upgrade-agent Phase 4 + Phase 6
- Do NOT start Pass-3 specialist work until ALL THREE Session B's close (PF-S12-01 falsification window)
- Do NOT commit to main
- Do NOT build PF-S12-01 Structural-2 + Structural-3 (bead `ams`) this session — the user explicitly picked path 1 (close debt directly)

---

## 8. Falsification windows in S13

S13 is the FIRST test of:

1. **AP-DEFERRED-LOOP-CLOSURE recurrence-guard at session-start** (per PF-S12-01). If S13 opens with debt count = 3 AND I offer forward Pass-3 work as first option, the documentation-only guard failed and Structural-2 (the audit script) becomes blocking. User pre-authorization at S12 close ("we are going to build the agents in the next session") deflates this falsification window; the path is committed.

2. **PF-S3-01 7th consecutive guard at /upgrade-agent.** Phase 4 + Phase 6 are the verification windows. Each finding personally source-read against design doc cited evidence.

3. **AP-INCOMPLETE-PROPAGATION at design-doc-to-agent.md mapping.** New surface, untested. Phase 6 adversarial-review is the catch; orchestrator post-synthesis grep is second-line defense. Test stimulus: row numbers + AC numbers + OQ numbers in design doc — do they need to land in agent.md or be hidden?

4. **Token-budget compression discipline.** Role 4 design doc is 874 lines; target agent.md is ≤200 lines. The compression ratio is ~4.4×. Document overruns; do NOT aggressively compress at the cost of safety properties (substrate Limitation 14 + 21 alert-fatigue precedent).

---

## 9. Session-close expectations

At S13 close:
- `.claude/agents/health-implementer/agent.md` exists (OR explicit deferral with cited rationale)
- `.claude/agents/health-edge-case-reviewer/agent.md` exists (OR deferral)
- `.claude/agents/medical-safety-reviewer/agent.md` exists (OR deferral)
- HANDOFF.md S13 close note + VOLATILE rotation per 6-clause rule
- `memory/process-failures.md` appended OR PF attestation clean (canonical form `S13 close (YYYY-MM-DD): ...`)
- All 3 audits exit 0 at `--session 13`
- PF-S12-01 recurrence_count remains 3 (NOT promoted to 4); falsification window held
- New beads created for S13 deferred work (mirror S10/S11/S12 pattern); especially: post-deployment §15.2b ACs that didn't pass at Phase 7 for any role
- Commit + push to `feature/wiki-bpc157-aplus-research`
- This file marked `status: consumed`
- Bead `ams` updated with progress toward "debt closed" milestone

---

## 10. What to read FIRST after standard session-start protocol

Six load-bearing reads if context is tight:
1. This file (SESSION_KICKOFF.md)
2. `HANDOFF.md` S12 close note + Top-3 (PF-S12-01 #1; the failure this session remediates)
3. `memory/process-failures.md` PF-S12-01 (full failure analysis)
4. `.claude/agents/health-specialist-architect/agent.md` (the reference shape for what S13 produces)
5. `design/health-implementer-design.md` (first work-unit input)
6. `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` (template every agent.md conforms to)

---

## 11. Parallel work (not on S13 critical path)

S10/S11/S12 beads S13 should NOT pick up unless explicitly directed:

- `a-plus-maxing-3y6` (P1) — audit-script bash. Becomes RELEVANT when Role 2 deploys (its agent.md references the audit script); but the script itself is Role 2 OWNERSHIP per §4.2 OUTBOUND. Decide at S13: does Role 2 deployed agent reference PROPOSED script with bead-tracked path, OR does Role 2 ship script alongside deployment? Default: PROPOSED-with-bead (mirrors Role 1 pattern). Bead `3y6` continues to track.
- `a-plus-maxing-ams` (P1) — PF-S12-01 structural fixes. NOT path 1. Continues open after S13 closes.
- `a-plus-maxing-pmp` (P2) — denylist starter. Role 4 §13 row 19 references; deployed agent.md may need.
- `a-plus-maxing-h1z` (P2) — AQ-001 resolution. Inherited by Role 3 + Role 4 deployments.
- `a-plus-maxing-2qq` (P3) — Token-budget characterization. Likely surfaces at Role 3 or Role 4 Phase 7.

---

## 12. Compaction recovery anchor

If S13 opens after compaction, recovery sequence:
1. Read `HANDOFF.md` (S12 close note + Current State + What Is Next + Top-3 = PF-S12-01 #1; Landmark check)
2. Read this file (`design/.session-b-deployments/SESSION_KICKOFF.md`)
3. Read `memory/process-failures.md` PF-S12-01 (the failure being remediated)
4. Read `INVARIANTS.md` + `vault/meta/landmarks.md`
5. Run `bd ready` (verify `ams` + `3y6` priorities; check for new beads created between S12 close and S13 start)
6. Run PF-S12-01 §1 recurrence-guard check (list deployed agents, list Final design docs, compute debt = 3 expected)
7. User pre-authorized path: "build the agents we have design docs for" — debt count 3 → 0 is the S13 goal
8. Read §0 pre-flight reads
9. Write S13 scope contract to HANDOFF.md (template at §2 above); obtain user confirmation
10. Locate `/upgrade-agent` skill (likely `~/.claude/commands/upgrade-agent.md` or `~/.claude/skills/upgrade-agent/SKILL.md`); read in full before first dispatch
11. Begin Role 2 deployment as first work-unit
