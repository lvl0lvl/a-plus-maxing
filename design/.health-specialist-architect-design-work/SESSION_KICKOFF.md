---
title: Session Kickoff — Pass-2 Design Doc for Role 1 (health-specialist-architect)
type: session-prep
status: ready
created: 2026-05-26
last_reviewed: 2026-05-26
prepared_at: S7 close
target_session: S8 (next session after compaction)
scope: Pass-2 Phase 1–5 of design-doc-protocol for Role 1 only
---

# Session Kickoff — Pass-2 for Role 1 (health-specialist-architect)

This file is the **focused operational brief** for the next session running Pass-2 for Role 1. It is NOT a session handoff (that's `HANDOFF.md`). It packages the specific reads, dispatches, and decisions the orchestrator needs to execute Pass-2 Phase 1–5 against `DESIGN_DOC_TEMPLATE.md` for the health-specialist-architect role.

If you are starting that session: read this in full before any work. If you find a contradiction between this file and source files, source files win — but flag the contradiction back to the user.

---

## 0. Pre-flight: read these in this order

The first action of the session (after the standard CLAUDE.md session-start protocol) is reading the operational substrate:

1. **`HANDOFF.md`** — standard session-start; especially Current State + What Is Next + Top-3 + Scope Contract for the current session
2. **`INVARIANTS.md`** — the active register (12 invariants); INV-ROLE-INLINING is the load-bearing one for this work
3. **`memory/process-failures.md`** — the 8 documented PFs; especially PF-S3-01 (will be the dominant guard during Phase 4)
4. **`vault/meta/landmarks.md`** — landmark window check (LM-01 first MD visit is the downstream consumer)
5. **`design/DESIGN_DOC_TEMPLATE.md`** — the canonical template you're using; the whole thing
6. **`design/CONTINUATION_BRIEF.md`** — Pass-1 brief; especially §3 (4 compounding lessons), §10 (cross-role references)
7. **`design/.health-specialist-architect-design-work/domain-research.md`** — Role 1's Pass-1 deliverable (~91KB; this is the substrate the design doc anchors against)
8. **`~/.claude/projects/-Users-waltermcgivney-Documents-Projects-Quant/memory/design-doc-protocol.md`** — the original Quant protocol; `DESIGN_DOC_TEMPLATE.md` adapts from this
9. **`~/.claude/commands/upgrade-agent.md`** — the downstream consumer of your design doc
10. **`~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`** — the deployed-agent structural target (10 base sections)

---

## 1. Scope contract template (for your S8 scope contract)

Per CLAUDE.md session-start step 7, the contract goes in HANDOFF.md before any work. Suggested shape (you'll write the binary ACs):

```markdown
## Scope Contract — Session 8 (YYYY-MM-DD)

Goal: Run design-doc-protocol Phases 1-5 for Role 1 (health-specialist-architect) against DESIGN_DOC_TEMPLATE.md. Produce design/health-specialist-architect-design.md with Status: Final.

Acceptance criteria:
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches (architect / senior-engineer / qa via existing software-flavor profiles as v1-substitute). Each drafter's prompt inlines the full role profile per INV-ROLE-INLINING. Drafts written to design/.health-specialist-architect-design-work/{architect,se,qa}-draft.md.
- [ ] AC2 — Phase 2: orchestrator synthesizes design/health-specialist-architect-design.md following DESIGN_DOC_TEMPLATE.md §0.2 frontmatter + 18 sections + Appendix A. body↔bibliography symmetry check before Phase 3 (Lesson 3 guard).
- [ ] AC3 — Phase 3: 2 parallel red-team dispatches (/adversarial-review skill + software security agent v1-substitute briefed on medical-safety per CONTINUATION_BRIEF §7). Outputs to red-team-{adversarial,safety}.md.
- [ ] AC4 — Phase 4: orchestrator personally verifies each finding (PF-S3-01 guard); classifications LEGITIMATE / LEGITIMATE-MODIFIED / REJECTED with cited evidence per finding-classifications.md (reject-but-adopt pattern documented in user-memory).
- [ ] AC5 — Phase 5: design doc carries Status: Final; Appendix A populated; self-attest checklist (DESIGN_DOC_TEMPLATE §7) executed.
- [ ] AC6 — Close-protocol audits exit 0 at --session 8; PF attestation canonical.

Files I WILL touch: design/health-specialist-architect-design.md (NEW), design/.health-specialist-architect-design-work/{architect,se,qa}-draft.md (NEW), red-team-{adversarial,safety}.md (NEW), finding-classifications.md (NEW), dispatch-ledger.jsonl (NEW), HANDOFF.md (contract + close), memory/process-failures.md (only if new PF).

Files I will NOT touch: domain-research.md (read-only Pass-1 substrate), DESIGN_DOC_TEMPLATE.md (read-only template), CONTINUATION_BRIEF.md, other roles' work dirs, vault/library/*, vault/compounds/*, scripts/*, .claude/hooks/*, .claude/skills/*, INVARIANTS.md (unless something forces; flag), CLAUDE.md, ~/Documents/Projects/skills_library/roles/* (read-only — profiles inlined into dispatches, not modified).

NOT doing: Roles 2/3/4 Pass-2 (subsequent sessions), Pass 3 specialist work, /upgrade-agent runs (Session B per role), peptide library campaign, Walter pending items, v2.5 punch-list items.

Invariants at risk: INV-ROLE-INLINING (hook gates every drafter dispatch); PF-S3-01 guard (Phase 4 verification — same falsification window as the design-doc-protocol context we just used in S7); INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN.

Self-recognition pre-flight: Specifically watch for "the architect-draft already looks complete, the SE/QA drafts are confirmation" (avoid SE/QA dispatch skip). Also watch for "the red-team finding's premise is wrong AND its fix is bad" — that's an honest rejection, but verify the fix is actually bad before dropping it (reject-but-adopt pattern applies).
```

---

## 2. Phase-by-phase operational guide

### Phase 1 — Drafting team (3 parallel dispatches)

**Critical pattern: each drafter gets the FULL 11-section software role profile inlined verbatim.** The hook will block if any of the 11 canonical sections is missing. The S7 dispatch inlined the architect profile verbatim — pattern proven.

**Drafter dispatches:**

| Drafter | Role profile to inline | Output path | Focus |
|---|---|---|---|
| Architect | `~/Documents/Projects/skills_library/roles/architect/agent.md` | `design/.health-specialist-architect-design-work/architect-draft.md` | Structural: §2 Role Definition, §4 Cross-Role Refs, §13 Mechanical Enforcement, §6 Ask vs Proceed, §7 Loop-Breaking |
| Senior Engineer | `~/Documents/Projects/skills_library/roles/senior-engineer/agent.md` | `design/.health-specialist-architect-design-work/se-draft.md` | Implementation specifics: §5 Core Rules, §8 Tools, §9 Communication, §10 Context Loading |
| QA | `~/Documents/Projects/skills_library/roles/qa/agent.md` | `design/.health-specialist-architect-design-work/qa-draft.md` | Edge cases + anti-patterns: §11 Anti-Patterns, §12 Negative Examples, §14 Edge Cases, §15 Acceptance Criteria, §17 Risk/Assumptions, §18 Open Questions |

Each drafter brief MUST contain:
- The full 11-section role profile (verbatim from the profile file)
- The task: "produce sections X, Y, Z of `design/health-specialist-architect-design.md` per `design/DESIGN_DOC_TEMPLATE.md` §2 specs" — name the specific sections that drafter owns from the table above
- File paths to read (not paste content for): `design/.health-specialist-architect-design-work/domain-research.md`, `design/DESIGN_DOC_TEMPLATE.md`, `design/CONTINUATION_BRIEF.md` (§3 + §10), `vault/WIKI.md` (Agent Consumers section), `vault/meta/operator-profile.md`, `INVARIANTS.md`, `memory/process-failures.md`
- The reminder: "do NOT redefine Pass-1 Findings; reference by Finding number per DESIGN_DOC_TEMPLATE §3 anti-paraphrase rule"
- Per the Pass-1 Lesson 1: drafters CANNOT dispatch sub-sub-agents (no nested Agent calls); they must do their own reads

Dispatch all 3 in parallel (single message with 3 Agent calls).

**Record each dispatch in `design/.health-specialist-architect-design-work/dispatch-ledger.jsonl`** per the Pass-1 precedent:
```json
{"role": "drafter", "drafter_type": "architect", "agent_id": "...", "brief_hash": "...", "output_path": "...", "timestamp": "..."}
```

### Phase 2 — Synthesis (orchestrator-level; NOT delegated)

You (the orchestrator) read all 3 drafts + the Pass-1 deliverable + the template, and write `design/health-specialist-architect-design.md`.

**Frontmatter** per DESIGN_DOC_TEMPLATE §0.2:
```yaml
---
title: health-specialist-architect Design Doc
type: design-doc
status: Draft
role_slug: health-specialist-architect
role_class: foundation
pass_1_substrate: design/.health-specialist-architect-design-work/domain-research.md
authored_by: design-doc-protocol Pass-2
created: <YYYY-MM-DD of S8>
last-PF-reviewed: PF-S6-01   # confirm against memory/process-failures.md at time of authoring
adapts_template: design/DESIGN_DOC_TEMPLATE.md
downstream: /upgrade-agent → ~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md
---
```

**Section ordering = template ordering** (§1–§18 + Appendix A).

**Role 1 directionality (per template §4 disposition):** This is the FIRST foundation role authored. §4 is OUTBOUND. Per CONTINUATION_BRIEF §10, the 7 cross-role rows all hub through Role 1 — §4 documents what Roles 2–4 + 14 specialists will INHERIT FROM this doc:
- Refusal-class taxonomy (7-class) → Roles 2/3/4 reference this
- GRADE evidence-tier discipline → Roles 2/3/4 reference this
- Three-mechanism anti-sycophancy → Roles 2/3/4 reference this
- Operator-profile hard limits gating compound writes → Roles 2/3/4 R7/R10 reference

**§3 row count:** before authoring §3, run `grep -cE "^### Finding " design/.health-specialist-architect-design-work/domain-research.md` to get the exact Finding count. Reserve that many rows in the §3.1 table. Then walk the file Finding-by-Finding.

**§11 PF coverage:** all 8 PFs enumerated per template §11 with per-role in-scope verdict. For health-specialist-architect specifically:
- PF-S2-01, S2-02, S2-03, S2-04, S2-05, S3-01, S6-01 → IN-SCOPE (this role produces structural decisions; can self-attest, can mis-cite, can over-question, can over-personalize, can pattern-match-protocol, can confuse mechanical-fix-with-verdict, can act-before-verify)
- PF-S2-06 → CONDITIONAL: depends on whether health-specialist-architect's tool palette allows git commits. The Pass-1 deliverable's R1–R15 tool spec should decide this.

**§13 status tags:** every row LIVE / REFERENCED / PROPOSED. The Pass-1 deliverable's recommendations include mechanical checks — tag each per template §13 disposition.

**§16 scope (per F-011 disposition):** Format/Document + Process + Role-discipline categories only. Research-domain INV-* OUT-OF-SCOPE (health-specialist-architect does not dispatch aplus-research; it designs the template that medical specialist profiles use). State the scope restriction explicitly in §16.

**Mid-synthesis Lesson 3 check (body↔bibliography symmetry):** Before dispatching Phase 3, run the by-hand grep from CONTINUATION_BRIEF Q3 disposition:
```bash
body_cites=$(grep -oE '\[[0-9]+\]' design/health-specialist-architect-design.md | grep -oE '[0-9]+' | sort -un)
bib_cites=$(grep -oE '^\[[0-9]+\]' design/health-specialist-architect-design.md | grep -oE '[0-9]+' | sort -un)
comm -23 <(echo "$body_cites") <(echo "$bib_cites")  # body [N] not in bib
comm -13 <(echo "$body_cites") <(echo "$bib_cites")  # bib [N] not in body
```
Both `comm` outputs should be empty before Phase 3 dispatches.

After synthesis, set `status: Phase-3 Red-Team Pending` in frontmatter.

### Phase 3 — Red team (2 parallel dispatches)

**Dispatch 1: `/adversarial-review` skill** on the synthesized design doc. Same pattern S7 used (you'll recognize the prompt shape — see the S7 commit). The skill is NOT role-tagged; do not write `# Adversarial Reviewer` as H1 (the hook blocks; S7 hit this and rerouted).

**Dispatch 2: software `security` agent v1-substitute briefed on medical-safety.** The medical-safety-reviewer (Role 4) is the intended consumer of this position, but its agent.md doesn't exist yet (deployment is Session B for Role 4, AFTER its Pass-2 doc finalizes). For Role 1's Pass-2 Phase 3, dispatch the software `security` agent with the full 11-section profile inlined + a medical-safety briefing addendum:
- Read Role 4's Pass-1 deliverable: `design/.medical-safety-reviewer-design-work/domain-research.md`
- Apply the threat-model from Role 4 Findings (3-axis severity, refusal-class composition)
- Output to `design/.health-specialist-architect-design-work/red-team-safety.md`

**Both dispatches must:**
- Read the synthesized `design/health-specialist-architect-design.md` directly
- Read `DESIGN_DOC_TEMPLATE.md` to know what to check against
- Emit findings as: ID / Category / Section / Severity / Description / Cited evidence / Suggested fix
- Walk ALL categories explicitly (8 standard for adversarial; the safety reviewer uses Role 4 Pass-1 categories)

Record both dispatches in dispatch-ledger.jsonl.

### Phase 4 — Verification (orchestrator-level; PF-S3-01 guard)

Same discipline you applied in S7 — read every finding's cited evidence from source-of-truth before classification.

**Three classification verdicts:**
- **LEGITIMATE** — claim verified factual; fix adopted
- **LEGITIMATE-MODIFIED** — claim factual; fix needs modification; modified disposition stated
- **REJECTED** — claim verified wrong; fix may still be adopted independently per the reject-but-adopt pattern (see user-memory `feedback_reject_but_adopt_pattern.md`)

Output: `design/.health-specialist-architect-design-work/finding-classifications.md`.

**Mandatory attestation:** every REJECTED row carries source-of-truth evidence (file path + section/line) proving the claim is wrong. Not orchestrator prose; cited source.

### Phase 5 — Finalize

1. Apply LEGITIMATE + LEGITIMATE-MODIFIED dispositions to the design doc
2. Populate Appendix A with all findings + verdicts
3. Run DESIGN_DOC_TEMPLATE §7 self-attest checklist (17 binary items)
4. Set frontmatter `status: Final (red team reviewed, all findings classified)`
5. Commit on feature branch (not main; INV-BRANCH-NOT-MAIN)
6. Update `vault/meta/index.md` + `vault/meta/log.md` with the new design doc (cross-document ownership matrix: meta is the next-cycle orchestrator's responsibility)

---

## 3. Known edge cases (handle inline)

**E1. Inlining hook blocks the `/adversarial-review` dispatch if H1 = `# Adversarial Reviewer`.** Documented in CONTINUATION_BRIEF §1 Q1 + observed in S7. Solution: use `/adversarial-review` skill explicitly, no role-tagged H1.

**E2. PF-S2-06 (branch hygiene) in-scope verdict depends on the role's tool restrictions.** The Pass-1 deliverable's tool spec decides. If health-specialist-architect's tools exclude git operations, S2-06 → OUT-OF-SCOPE (structural). If allowed, IN-SCOPE.

**E3. The §3 Pass-1 Recommendations count is empirically 15 (Roles 1-4 all have R1-R15).** Per template disposition: phrase as "R1-R<N>" defensively even though current N=15. Don't hardcode.

**E4. `last-PF-reviewed:` should match the most recent PF in `memory/process-failures.md` at time of authoring.** As of S7 close: `PF-S6-01`. If the file gets a new PF between S7 close and S8 start (unlikely but possible), the frontmatter value updates.

**E5. §4 OUTBOUND content is harder to write than INBOUND.** Role 1 establishes references for later docs; the writer must surface what Roles 2/3/4 + 14 specialists will need to inherit. Look at CONTINUATION_BRIEF §10 table — every row with Role 1 as a source-or-target counts as a Role 1 obligation.

**E6. If the §7 self-attest checklist surfaces a failure (e.g., an AGENT_TEMPLATE.md section has no upstream design-doc section), the design doc is NOT Final.** Either fix the doc or document why the check is N/A for this role with explicit "OMITTED — rationale" note.

---

## 4. What the next session does NOT need to do

To prevent scope creep:

- Do NOT modify `DESIGN_DOC_TEMPLATE.md`. If you find a real template defect during Pass-2 Role 1, surface it as an Open Question (§18) and flag to the user — template changes follow the template's own change-discipline (§11).
- Do NOT design Roles 2/3/4 in the same session. Sequential per CONTINUATION_BRIEF §7.
- Do NOT deploy the health-specialist-architect agent.md. That's Session B for Role 1, after this design doc finalizes.
- Do NOT modify the Pass-1 deliverable `domain-research.md`. Read-only substrate.
- Do NOT promote new invariants without user authorization + INVARIANTS change-discipline ritual.
- Do NOT skip Phase 3 red team even if drafts look clean. The Pass-1 pattern (every Session B catches something) applies here too.
- Do NOT skip Phase 4 personal verification. PF-S3-01 guard is the load-bearing discipline of this session.

---

## 5. Estimated cost

Per CONTINUATION_BRIEF §7 cost estimate:
- 3 parallel drafter dispatches (Phase 1) = 3 Agent calls
- 2 parallel red-team dispatches (Phase 3) = 2 Agent calls
- 0 iteration cycles assumed; iter-2 if red-team surfaces remediation-required findings = +N Agent calls
- Orchestrator-level work: Phase 2 synthesis + Phase 4 verification + Phase 5 finalize

Single session if dispatches are clean. Two sessions if Phase 4 surfaces iter-2 work.

---

## 6. Falsification windows in this session

S8 is the first end-to-end run of the design-doc-protocol using `DESIGN_DOC_TEMPLATE.md`. Three failure-mode classes are live falsification windows:

- **AP-ORCH-SELF-ATTEST (PF-S3-01 class).** Same risk that surfaced in S7's Phase 4. Personal source-reads required; reject-but-adopt pattern available.
- **AP-INCOMPLETE-PROPAGATION (S4 finding, embedded in template §3 + §11 + §16 + §13 with explicit row-count + scope verdicts).** Walking 18 sections against the spec without missing a section is the explicit test. The §7 self-attest checklist is the defense.
- **Template-level defects undetected in S7.** If the design doc cannot be written cleanly against the template, the template has a defect S7's adversarial review missed. Surface to user — template-change discipline applies.

---

## 7. Session close expectations

At close:
- `design/health-specialist-architect-design.md` exists with `status: Final`
- All ACs from the S8 scope contract evaluated PASS / FAIL / CHANGED / N/A in writing
- HANDOFF.md S8 close note appended; VOLATILE sections rotated per CLAUDE.md step 5
- `memory/process-failures.md` either appended (if a new PF surfaced) or attested clean
- All 3 audit scripts exit 0 at `--session 8`
- Commit + push to `feature/wiki-bpc157-aplus-research`
- `vault/meta/index.md` + `vault/meta/log.md` updated with the new design doc
- This file (SESSION_KICKOFF.md) marked `status: consumed` or moved to an archive — not deleted (institutional record)

---

## 8. What to read FIRST after the session-start protocol

If context is tight:
1. This file
2. `design/DESIGN_DOC_TEMPLATE.md`
3. `design/.health-specialist-architect-design-work/domain-research.md`

Everything else is supporting context — these three are the load-bearing reads for Pass-2 Role 1.
