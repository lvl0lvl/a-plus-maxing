---
title: Session B Kickoff — /upgrade-agent for Role 1 (health-specialist-architect)
type: session-prep
status: ready
created: 2026-05-26
prepared_at: S8 close
target_session: S9 (next session after compaction)
scope: Run /upgrade-agent against design/health-specialist-architect-design.md to produce deployed agent.md
predecessor: design/.health-specialist-architect-design-work/SESSION_KICKOFF.md (S7→S8 brief, now consumed)
---

# Session B Kickoff — /upgrade-agent for Role 1 (health-specialist-architect)

This file is the focused operational brief for the next session running Session B (deployment) for Role 1. The Pass-2 design-doc protocol is COMPLETE for Role 1 (S8 closed clean; design doc Status: Final). Session B is the second half: `/upgrade-agent` consumes the design doc and produces the deployed agent.md.

Read this in full before any work. If a contradiction surfaces between this brief and source files, source files win — flag back to user.

---

## 0. Pre-flight reads (in this order)

1. **`HANDOFF.md`** — standard session-start; especially Current State + What Is Next + S8 close note + Scope Contract for current session
2. **`INVARIANTS.md`** — 12-entry register (no register changes this session unless `/upgrade-agent` surfaces one); INV-ROLE-INLINING is load-bearing for any sub-agents `/upgrade-agent` dispatches
3. **`memory/process-failures.md`** — 8 PFs; especially PF-S3-01 (will be the dominant guard during `/upgrade-agent` Phase 4 validation loop and Phase 6 adversarial review)
4. **`vault/meta/landmarks.md`** — landmark window check (LM-01 first MD visit is the eventual downstream consumer of the deployed agent)
5. **`design/health-specialist-architect-design.md`** — the canonical design doc (873 lines, Status: Final). THIS IS THE SOURCE OF TRUTH for the agent.md. `/upgrade-agent` reads this; you read it so you can answer adjudication questions if `/upgrade-agent` surfaces ambiguity.
6. **`design/.health-specialist-architect-design-work/finding-classifications.md`** — 38 findings with Phase-4 verdicts; useful if `/upgrade-agent` Phase 6 adversarial review surfaces a finding overlapping a Phase-3 finding (saves re-deliberation)
7. **`~/.claude/commands/upgrade-agent.md`** — the command's 8-phase pipeline (16,641 bytes); re-read at every phase boundary per CLAUDE.md re-read-protocol discipline (PF-S2-05 recurrence guard)
8. **`~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`** — structural target (10 base sections + Modes); the agent.md must conform
9. **`design/DESIGN_DOC_TEMPLATE.md`** §4 Phase Coverage Matrix — confirms which design-doc sections feed which `/upgrade-agent` phase

---

## 1. Scope contract template (for your S9 scope contract)

Per CLAUDE.md session-start step 7, write the contract to HANDOFF.md before any work. Suggested shape:

```markdown
## Scope Contract — Session 9 (YYYY-MM-DD)

Goal: Run /upgrade-agent against design/health-specialist-architect-design.md (Status: Final, 873 lines). Produce ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md per the 8-phase pipeline. Update orchestrator catalog to include the new role.

Acceptance criteria:
- [ ] AC1 — /upgrade-agent Phase 1 (Baseline Evaluation): no prior agent.md exists at the target path (net-new authoring); baseline scorecard documents the net-new state; line/token budget targets established (~140 lines target, ≤200 hard max).
- [ ] AC2 — /upgrade-agent Phase 2 (Rubric Construction): agent-specific rubric derived from design doc §15.2 7 binary ACs + 10-dimension generic rubric in the command.
- [ ] AC3 — /upgrade-agent Phase 3 (Research Agents): 3 parallel research dispatches per command default grouping (R1 Behavioral Traits, R2 Reference Integration, R3 Communication & Anti-Patterns); each dispatch inlines required role profile if role-tagged.
- [ ] AC4 — /upgrade-agent Phase 4 (Validation Loop): SEPARATE fact-checker + judge agents (parallel, fresh contexts) per HARD RULES; 9/10 on every dimension required for pass; PF-S3-01 guard held — no orchestrator self-attestation of validator verdicts.
- [ ] AC5 — /upgrade-agent Phase 5 (Synthesis): agent.md produced at ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md; structure conforms to AGENT_TEMPLATE.md (10 base sections + Modes); anti-sycophancy in first 20 lines; Negative Examples in last 30 lines.
- [ ] AC6 — /upgrade-agent Phase 6 (Adversarial Review): /adversarial-review skill dispatched against the synthesized agent.md (NOT against the design doc — they are different artifacts); findings classified per PF-S3-01 guard.
- [ ] AC7 — /upgrade-agent Phase 7 (Final Corrections): line count ≤200 verified; token count ≤2,000 verified; all 10 base AGENT_TEMPLATE.md sections present; library-index.md created if needed; catalog entry added.
- [ ] AC8 — /upgrade-agent Phase 8 (Close Out): summary of changes; deferred items beaded; final scores documented.
- [ ] AC9 — Close: all 3 audit scripts exit 0 at --session 9; PF attestation in canonical form; VOLATILE rotation applied; feature branch only.

Files I WILL touch:
- ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md (NEW)
- ~/Documents/Projects/skills_library/roles/health-specialist-architect/library-index.md (NEW, if needed)
- ~/Documents/Projects/skills_library/roles/orchestrator/catalog.md (append new role row)
- HANDOFF.md (contract + close note + VOLATILE rotation)
- design/.health-specialist-architect-design-work/SESSION_B_KICKOFF.md (mark as consumed at close)
- memory/process-failures.md (only if new PF surfaces)

Files I will NOT touch:
- design/health-specialist-architect-design.md (read-only — Status: Final; defects → ADR-amendment via template change discipline, not in-place edit)
- design/DESIGN_DOC_TEMPLATE.md (read-only)
- design/.health-specialist-architect-design-work/{architect,se,qa,finding-classifications,red-team-*}.md (read-only, Phase-3/4 artifacts frozen)
- Other roles' work dirs in design/
- vault/library/*, vault/compounds/*, vault/biomarkers/*
- .claude/skills/*, scripts/*, .claude/hooks/*
- INVARIANTS.md (unless /upgrade-agent surfaces a new candidate; flag at the time)
- CLAUDE.md
- main branch

NOT doing:
- Pass-2 design docs for Roles 2/3/4 (S10-S12 sequential)
- Other Session B deployments (Role 2/3/4 Session Bs come after their Pass-2 finalizes)
- Pass-3 specialist work
- Peptide library campaign
- Walter pending items
- v2.5 punch-list items
- Vault git-tracking decision
- First HTML artifact (LM-04)

Invariants at risk:
- INV-ROLE-INLINING — any research/judge/fact-check sub-agents `/upgrade-agent` dispatches must inline the full 11-section profile if role-tagged. The hook will block; watch for the same profile-vs-section-name edge case S8 hit (recurrence_count=2 for the class).
- PF-S3-01 guard — Phase 4 Validation Loop is the falsification window in /upgrade-agent context. Fact-checker + judge are SEPARATE agents; no orchestrator self-attestation of verdicts. Pass threshold 9/10 on EVERY dimension — no rounding.
- AP-INCOMPLETE-PROPAGATION — Phase 5 Synthesis must hit all 10 AGENT_TEMPLATE.md base sections; the §7 Final Corrections checklist is the defense.
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN — standard close discipline.

Self-recognition pre-flight: Watching specifically for —
- "the design doc is Status: Final, the agent.md can be derived directly without research dispatches" → would skip Phase 3 (canonical PF-S2-01 framing variant)
- "the line count is 198, 2 over is fine" → would soften the 200 hard max (rejected by command HARD RULES)
- "the fact-checker and judge can be the same agent in two prompts" → would violate the "SEPARATE agents in PARALLEL" rule
- "the 9/10 threshold is a guideline, 8.5 rounds to 9" — rejected by command HARD RULES ("no rounding, no softening")
```

---

## 2. Phase-by-phase operational notes

### Phase 1 — Baseline Evaluation

**Net-new authoring context.** No prior agent.md exists at `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md`. Baseline scorecard scores against the absent-file state: every dimension is the gap between "doesn't exist" and the 10-dimension rubric target. This frames Phase 3 research as net-new, not delta-from-existing.

The design doc (`design/health-specialist-architect-design.md`) is the substrate Phase 3 research grounds against. Phase 1 establishes that the design doc exists and is Status: Final.

### Phase 2 — Rubric Construction

The design doc's §15.2 has 7 binary ACs already specific to this role. They feed into the agent-specific rubric per the command's Phase 2 spec. The 10 generic dimensions (Identity Clarity / Context Efficiency / Behavioral Specificity / Reference Integration / Boundary Enforcement / Communication Protocol / Failure Recovery / Tool Awareness / Anti-Pattern Coverage / Freshness) apply on top.

The agent-specific rubric should explicitly map the 8 refusal classes + H-class composition + 13 Core Rules (incl. 6b) + 8 anti-patterns + AGENT_TEMPLATE.md structure to dimension scores.

### Phase 3 — Research Agents (3 parallel)

Default grouping per command (no obvious reason to deviate):
- **R1 Behavioral Traits** — Core Rules + Role Boundaries + Identity. Grounds against design-doc §2 + §5.
- **R2 Reference Integration** — Tools + Context Loading + library-index.md. Grounds against design-doc §8 + §10.
- **R3 Communication & Anti-Patterns** — Communication + Anti-Patterns + Negative Examples. Grounds against design-doc §9 + §11 + §12.

**Each research dispatch reads** the design doc (873 lines, source of truth) + AGENT_TEMPLATE.md (structural target) + the dimensions this dispatch is responsible for from the agent-specific rubric.

**Each dispatch is fresh** — new context window. The command's HARD RULES mandate this.

### Phase 4 — Validation Loop (parallel fact-checker + judge)

Per command HARD RULES:
- Fact-checker and judge are SEPARATE agents in PARALLEL
- Fresh agents per iteration (no resuming prior agents)
- Pass threshold: 9/10 on EVERY dimension; no exceptions, no rounding, no softening

Iteration cap: implicit in `/upgrade-agent`. If 3 iterations without 9/10 convergence, escalate per command's loop-breaking equivalent.

**This is the PF-S3-01 falsification window for /upgrade-agent context.** The orchestrator (you) does NOT self-attest validator verdicts. Each iteration produces verdict files from the dispatched validators; you compose the synthesis input from those files, not from prose attestation.

### Phase 5 — Synthesis

Agent.md authored at the target path. Structure:
- AGENT_TEMPLATE.md 10 base sections + `## Modes`
- Anti-sycophancy anchor in first 20 lines (primacy effect)
- Negative Examples in last 30 lines (recency effect)
- Identity core under ~2,000 tokens / 140 lines target / 200 hard max
- Per-section line budgets per the command's table

**Source mapping** (from DESIGN_DOC_TEMPLATE.md §5 Synthesis Order):
1. Identity ← design-doc §2.1 + §1
2. Core Rules ← design-doc §5 (13 rules + 6b)
3. Role Boundaries ← design-doc §2.2 + §4
4. Ask vs Proceed ← design-doc §6
5. Loop-Breaking ← design-doc §7
6. Tools ← design-doc §8
7. Communication ← design-doc §9
8. Context Loading ← design-doc §10 + §4
9. Modes ← design-doc §5 + §9 + §14 (per template — emerges from these three)
10. Anti-Patterns ← design-doc §11
11. Negative Examples ← design-doc §12

### Phase 6 — Adversarial Review

`/adversarial-review` skill against the **synthesized agent.md** (NOT against the design doc — different artifacts).

Same H1 caveat as S7/S8: do NOT write `# Adversarial Reviewer` as H1; use the skill explicitly. The inlining hook will block.

If a Phase-6 finding overlaps a Phase-3 finding from the design-doc red team (already in `design/.health-specialist-architect-design-work/finding-classifications.md`), check the prior verdict and disposition first before re-deliberating.

### Phase 7 — Final Corrections

Mechanical checks per command's spec:
- Line count ≤ 200 (hard max)
- Token count ≤ 2,000
- All 10 AGENT_TEMPLATE.md base sections present
- Per-section line budgets respected
- Anti-sycophancy in first 20 lines (verified by line-number check on the anchor sentence)
- Negative Examples in last 30 lines (verified by section-position check)
- library-index.md created if needed
- Catalog entry added to `~/Documents/Projects/skills_library/roles/orchestrator/catalog.md`

### Phase 8 — Close Out

Summary of changes + deferred items beaded + final scores documented.

---

## 3. Known edge cases (handle inline)

**E1. Hook profile-vs-section mismatch (recurrence_count=2 class).** If `/upgrade-agent` dispatches sub-agents with role-tagged prompts (H1=`# X` or `roles/<slug>/agent.md` reference), and the inlined profile uses a non-`## Modes` 11th section (e.g., `## Audit Protocol` for security, `## Spec Amendment Protocol` for architect), the hook blocks. S7 and S8 both hit this class. Resolution: either (a) use the skill explicitly with no role-tag H1, or (b) add a synthetic `## Modes` pointer to the role-specific section (additive, no paraphrasing).

**E2. Design doc Status: Final means read-only.** If you find a defect during Phase 3 research or Phase 6 adversarial review, do NOT edit the design doc in-place. Surface it as an Open Question for the next design-doc-template-change-discipline cycle. The agent.md can be authored faithfully to the as-Final design doc even if a defect is later identified.

**E3. The 200-line hard max may force §10/§11 compression.** The design doc has 13 Core Rules + 8 anti-patterns + 14 edge cases + 17 §13 mechanical-enforcement rows. The deployed agent.md targets 140 lines. Phase 5 synthesis will need to ABBREVIATE the design-doc content — not all material maps 1:1. Library references (`library-index.md`) are where overflow content lives.

**E4. `last-PF-reviewed: PF-S6-01` frontmatter pin in the design doc.** Per `/upgrade-agent` Phase 1, the command diff-checks PF entries against this field and surfaces any new PF entries as candidate Anti-Pattern additions. At time of S8 close, PF-S6-01 was still the latest — verify at S9 start.

**E5. Catalog entry needs a one-paragraph role summary.** Per the command's Phase 7 final-corrections spec, `roles/orchestrator/catalog.md` gains a row for the new role. The catalog summary differs in format from the agent.md identity sentence.

**E6. INV-HARM-CLASS-COMPOSITION (PROPOSED).** This invariant was surfaced in design-doc §16 per F-S1 but is NOT yet in the register. The agent.md should NOT cite it as if it were live. If the agent.md needs to reference H-class composition, cite the design doc §4 OUTBOUND row 2 + Core Rule 13 explicitly, not the invariant.

**E7. v1-substitute artifact note.** The design doc Phase-3 safety review was a v1-substitute (software security agent briefed on medical safety) because Role 4 isn't deployed. The agent.md should NOT assert "medical-safety-reviewer has audited this profile" — that audit hasn't happened. §17.2 A-7 documents the v1-substitute path.

---

## 4. What the next session does NOT need to do

- Do NOT modify `design/health-specialist-architect-design.md` (Status: Final; defects → ADR, not edit)
- Do NOT modify `DESIGN_DOC_TEMPLATE.md`
- Do NOT modify the Phase-3 artifacts (architect-draft / se-draft / qa-draft / red-team-* / finding-classifications)
- Do NOT design Roles 2/3/4 (those are S10-S12 sequential Pass-2 runs)
- Do NOT skip Phase 6 adversarial review even if Phase 5 synthesis "looks clean"
- Do NOT promote INV-HARM-CLASS-COMPOSITION to the register (out-of-band change-discipline ritual)
- Do NOT skip the 200-line hard max (command HARD RULE)
- Do NOT skip the SEPARATE-fact-checker-and-judge requirement (command HARD RULE)

---

## 5. Estimated cost

Per `/upgrade-agent` command:
- Phase 3: 3 parallel research agents
- Phase 4: SEPARATE fact-checker + judge per iteration (2 agents × N iterations; pass threshold 9/10 per dim)
- Phase 6: 1 `/adversarial-review` dispatch
- Plus orchestrator-level work for Phase 1, 2, 5, 7, 8

Single session if dispatches are clean. Two sessions if Phase 4 iter-2+ needed or Phase 6 findings trigger Phase 7 corrections.

---

## 6. Falsification windows in this session

S9 is the first end-to-end run of `/upgrade-agent` in the a-plus-maxing project context. Three failure-mode classes are live falsification windows:

- **AP-ORCH-SELF-ATTEST (PF-S3-01 class).** Phase 4 Validation Loop is the explicit test. Pass threshold 9/10 on every dimension — orchestrator MUST consume validator JSON, not self-attest. Same discipline that held in S7 + S8 (design-doc-protocol Phase 4); now tested in /upgrade-agent Phase 4.
- **AP-INCOMPLETE-PROPAGATION.** Phase 5 Synthesis writes a 140-line agent.md from a 873-line design doc. The compression risk is missing a load-bearing piece. The §7 Final Corrections mechanical checks (10 sections present, anti-sycophancy first 20 lines, etc.) are the explicit defense.
- **Hook profile-vs-section mismatch (recurrence_count=2 class).** S8 and S7 both hit it. If S9 hits it again (recurrence_count=3), the hook is the candidate for structural change (e.g., accept `## Modes` OR project-recognized role-specific section name).

---

## 7. Session close expectations

At close:
- `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` exists with all 10 AGENT_TEMPLATE.md sections + Modes
- Line count ≤ 200 (verified mechanically); token count ≤ 2,000
- `~/Documents/Projects/skills_library/roles/orchestrator/catalog.md` gains a row for the new role
- All ACs from the S9 scope contract evaluated PASS / FAIL / CHANGED / N/A
- HANDOFF.md S9 close note appended; VOLATILE sections rotated
- `memory/process-failures.md` either appended (new PF) or attested clean
- All 3 audit scripts exit 0 at `--session 9`
- Commit + push to `feature/wiki-bpc157-aplus-research`
- This file (SESSION_B_KICKOFF.md) marked `status: consumed` — not deleted (institutional record)

---

## 8. What to read FIRST after the session-start protocol

If context is tight, the three load-bearing reads:
1. This file (SESSION_B_KICKOFF.md)
2. `~/.claude/commands/upgrade-agent.md` (the protocol itself)
3. `design/health-specialist-architect-design.md` (the source of truth for the agent.md)

Everything else is supporting context.
