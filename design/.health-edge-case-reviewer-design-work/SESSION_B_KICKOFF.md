---
title: Session Kickoff — S14 Role 3 Session B (deploy health-edge-case-reviewer)
type: session-prep
status: consumed
created: 2026-05-29
prepared_at: S13 close (compaction prep)
target_session: S14 (next session after compaction)
predecessor: design/.session-b-deployments/SESSION_KICKOFF.md (S13, consumed)
scope: One role, full deploy-and-incorporate loop. /upgrade-agent against design/health-edge-case-reviewer-design.md -> .claude/agents/health-edge-case-reviewer/agent.md; sub-out QA drafter slot; /review-pr; /merge; close. Closes the next-oldest Session B debt (PF-S12-01 AP-DEFERRED-LOOP-CLOSURE).
session_b_debt_at_start: 2
---

# Session Kickoff — S14 Role 3 Session B (health-edge-case-reviewer)

S14 deploys Role 3 as the QA-equivalent agent and incorporates it (sub-out), via the **one-role-per-session deploy-and-incorporate loop**. Debt 2 → 1.

**Read this file in full before any work. If it conflicts with a source file, the source file wins — flag to the user.**

---

## 0. CRITICAL — session-open discipline (PF-S13-01, recurrence_count=3, logged S13)

S13 logged **PF-S13-01 (AP-PROTOCOL-FROM-MEMORY)**: the S13 session-open was run partly from mental model — the test baseline was *stated* without being *run*, and work was proposed before the scope contract was written. **S14 session-open is the falsification window.** Open S14 by RE-READING CLAUDE.md's Session Start Protocol and EXECUTING each numbered step, checking each off with real output:

1. Read HANDOFF.md **in full** (page past any truncation — S13's partial read was part of PF-S13-01). Read the Top-3 first.
2. Read INVARIANTS.md.
3. `git status && git log --oneline -5`. Expect branch `feature/wiki-bpc157-aplus-research` at the S13-close HEAD; `main` carries S7–S13 (rebased). **Branch topology note:** S13 close artifacts (HANDOFF rotation, vault/session-13) are on the feature branch; `main` has the S13 code only. S14 continues on the feature branch.
4. Read `memory/process-failures.md` — PF-S13-01 (the failure this open must not repeat) + PF-S12-01 (the debt being closed) + PF-S3-01 (the verdict-self-attest guard).
5. Read `vault/meta/landmarks.md` (no S14 windows expected; LM-01 is July 2026).
6. **RUN** the test baseline command (`echo "No test runner configured…"`) — do not reproduce its output from memory.
7. Write the S14 scope contract and obtain user confirmation BEFORE any work-proposal or dispatch.

**Also:** never use the AskUserQuestion option-selection widget with this user (it railroads — standing "never", see user-memory). Ask open questions in prose.

## 1. AP-DEFERRED-LOOP-CLOSURE recurrence guard (mandatory at session-start)

```bash
ls .claude/agents/                      # expect: health-specialist-architect, health-implementer  (2 deployed)
ls design/*-design.md | grep -v TEMPLATE # expect: 4 Final design docs
# debt = {Final design docs} − {deployed} = { health-edge-case-reviewer, medical-safety-reviewer } = 2
```

Debt = 2 (≥1), so the FIRST offered work-unit is the OLDEST debt = **Role 3 Session B (health-edge-case-reviewer)**. User pre-authorized the per-session loop ("build the agents we have design docs for, one per session"). Forward Pass-3 work is alternate-path only with explicit user override + cited rationale.

## 2. The loop (one role, this session)

1. **`/upgrade-agent`** against `design/health-edge-case-reviewer-design.md` (S11 Final, ~887 lines) → `.claude/agents/health-edge-case-reviewer/agent.md` (+ `library-index.md`). 8-phase pipeline. Net-new (0/10 baseline). Deploy project-local per ADR `vault/decisions/2026-05-26-foundation-role-agent-md-location.md`.
2. **Sub-out:** rotate the **QA drafter slot** software-`qa` v1-sub → `health-edge-case-reviewer` in `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7 (mirror the S13 SE-slot edit; the qa row currently reads "OWED, not yet run").
3. **`/review-pr`** scoped to the S14 commits (S13 precedent: scope to the session's deployment, not the whole PR). Blind triage; PF-S3-01 source-read each finding; fix LEGITIMATE, bead frozen-design-doc findings.
4. **`/merge`** on explicit user go (PR → main). Recommend rebase (preserves provenance, as S13). Confirm before deleting the branch.
5. **Close** (full CLAUDE.md close protocol; 3 audits exit 0 at `--session 14`; PF attestation; VOLATILE rotation; commit + push).

## 3. Discipline carried into S14 (worked at S13)

- **DOCUMENT_RUBRIC Rule 7** (budget overage → load-bearing review): if the Role 3 profile exceeds the ~2,000-token target (it likely will — medical-domain density, see Role 1 ~3,252 / Role 2 ~5,245), classify load-bearing vs reducible, cut only reducible, document residual vs bead `2qq`. Never blind-trim; never cut a safety binary.
- **AQ-002** (voice-register use-vs-mention): Role 3's profile will hit the same banned-token-MENTION issue. The disposition is fixed (deploy faithfully; mention-aware audit is bead `3y6`). Do not re-litigate.
- **PF-S3-01 guard:** independent blind-triage agent for `/review-pr`; personally source-read every `/upgrade-agent` Phase-4/6 + review finding.
- **Cross-role consistency:** run the targeted backlog consistency pass again IF Role 3's profile inherits contracts that S13's XR findings touched (esp. confirm Role 3 doesn't inherit the XR-002 `DEPLOY_WITH_OVERRIDE_PATH` inversion).

## 4. NOT S14 (do not pull in unless directed)

- **Bead `4ej` (XR-002 verdict-enum inversion) is a Role-4 / S15 prerequisite, NOT S14.** Role 3 (QA-equivalent) does not own the deploy-verdict schema. Close `4ej` via design-doc change discipline BEFORE S15 (Role 4), not now.
- Role 4 Session B (S15). Pass-3 specialists. Phase-C peptide campaign.
- Beads `ams`, `3y6` build-out (tracked, not on S14 critical path).
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue).

## 5. Sources of truth (frozen for S14)

| Artifact | Status | Path |
|---|---|---|
| Role 3 design doc | Final (S11) | `design/health-edge-case-reviewer-design.md` |
| Role 1 deployed (reference shape) | Final | `.claude/agents/health-specialist-architect/agent.md` |
| Role 2 deployed (S13, sibling + IDENTICAL/Jaccard oracle) | Final | `.claude/agents/health-implementer/agent.md` |
| AGENT_TEMPLATE | reference | `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` |
| /upgrade-agent skill | reference | `~/.claude/commands/upgrade-agent.md` |
| Roster B | mutable (S14 edits the qa row) | `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7 |

## 6. Compaction recovery anchor

If S14 opens after compaction:
1. Read `HANDOFF.md` (S13 close note + Top-3 + Current State + What Is Next).
2. Read THIS file.
3. Read `memory/process-failures.md` PF-S13-01 + PF-S12-01.
4. Read `vault/sessions/session-13.md` (what S13 did).
5. Run §0 session-open discipline + §1 recurrence guard.
6. Begin Role 3 deployment as first work-unit.

Mark this file `status: consumed` at S14 close.
