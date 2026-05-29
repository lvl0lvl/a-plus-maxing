---
title: Session Kickoff — S15 Role 4 Session B (deploy medical-safety-reviewer)
type: session-prep
status: ready
created: 2026-05-29
prepared_at: S14 close (compaction prep)
target_session: S15 (next session after compaction)
predecessor: design/.health-edge-case-reviewer-design-work/SESSION_B_KICKOFF.md (S14, consumed)
scope: One role, full deploy-and-incorporate loop. Close bead 4ej (XR-002) FIRST, then /upgrade-agent against design/medical-safety-reviewer-design.md -> .claude/agents/medical-safety-reviewer/agent.md; sub-out safety-red-team slot; clean PR off origin/main; /merge; close. Closes the LAST Session B debt (PF-S12-01 AP-DEFERRED-LOOP-CLOSURE; debt 1 -> 0; foundation pipeline complete).
session_b_debt_at_start: 1
---

# Session Kickoff — S15 Role 4 Session B (medical-safety-reviewer)

S15 deploys Role 4 as the safety-red-team-equivalent agent and incorporates it (sub-out), via the **one-role-per-session deploy-and-incorporate loop**. This is the LAST foundation role — debt 1 → 0, 4 of 4 foundation agents deployed.

**Read this file in full before any work. If it conflicts with a source file, the source file wins — flag to the user.**

---

## 0. CRITICAL — session-open discipline (PF-S13-01, recurrence_count=3)

PF-S13-01 (AP-PROTOCOL-FROM-MEMORY) was logged S13 and its falsification window **HELD at S14**. S15 session-open is the next window. Open S15 by RE-READING CLAUDE.md's Session Start Protocol and EXECUTING each numbered step with real output:

1. Read HANDOFF.md **in full** (page past truncation — it is ~430+ lines; read the S14 close note + the rotated Top-3 / Current State / What Is Next). Read the Top-3 first.
2. Read INVARIANTS.md.
3. `git status && git log --oneline -5`. Expect branch `feature/wiki-bpc157-aplus-research` at the S14-close HEAD (`1940f86` as of 2026-05-29 S14 close); `main` carries S7–S14 code. **Branch topology (see §3):** the long-lived feature branch is the diverged continuity carrier; `main` gets code via clean per-session branches off `origin/main`. Continue S15 on the feature branch.
4. Read `memory/process-failures.md` — PF-S13-01 (open-protocol), PF-S12-01 (the debt being closed), PF-S3-01 (the verdict-self-attest guard).
5. Read `vault/meta/landmarks.md` (no S15 windows expected; LM-01 is July 2026).
6. **RUN** the test baseline command (`echo "No test runner configured…"`) — do not reproduce its output from memory.
7. Write the S15 scope contract and obtain user confirmation BEFORE any work-proposal or dispatch.

**Also:** never use the AskUserQuestion option-selection widget with this user (standing "never" — ask open questions in prose). See user-memory.

## 1. AP-DEFERRED-LOOP-CLOSURE recurrence guard (mandatory at session-start)

```bash
ls .claude/agents/                      # expect: health-specialist-architect, health-implementer, health-edge-case-reviewer  (3 deployed)
ls design/*-design.md | grep -v TEMPLATE # expect: 4 Final design docs
# debt = {Final design docs} − {deployed} = { medical-safety-reviewer } = 1
```

Debt = 1 (≥1), so the FIRST offered work-unit is the LAST debt = **Role 4 Session B (medical-safety-reviewer)**. User pre-authorized the per-session loop. Forward Pass-3 work is alternate-path only with explicit user override + cited rationale.

## 2. The loop (one role, this session)

0. **PREREQUISITE — close bead `4ej` (XR-002) FIRST** (see §3; do this BEFORE the `/upgrade-agent` run so the deployed Role 4 agent inherits the correct verdict enum).
1. **`/upgrade-agent`** against `design/medical-safety-reviewer-design.md` (S12 Final, ~874 lines) → `.claude/agents/medical-safety-reviewer/agent.md` (+ `library-index.md`). 8-phase pipeline. Net-new (0/10 baseline). Deploy project-local per ADR `vault/decisions/2026-05-26-foundation-role-agent-md-location.md`.
2. **Sub-out:** rotate the **safety-red-team slot** software-`security` v1-sub → `medical-safety-reviewer` in `design/DESIGN_DOC_TEMPLATE.md` §0.1 (line ~41, the Phase-3 red-team line) + `design/CONTINUATION_BRIEF.md` §7 (line ~231, the "Same rotation applies to Phase 3 red-team safety reviewer" note). Mirror the S13 SE-slot + S14 QA-slot edits. After this, 4 of 4 Roster B slots are project-local — the foundation roster is fully self-hosting.
3. **`/review-pr`** scoped to the S15 deployment commits (local diff range; S13/S14 precedent — no GitHub PR needed for the review itself). Blind triage; PF-S3-01 source-read each finding; fix LEGITIMATE, bead frozen-design-doc findings.
4. **`/merge` — Option A branch topology (see §3):** cut a fresh per-session branch off `origin/main` (`git checkout -b feature/s15-medical-safety-reviewer origin/main`), `git cherry-pick` the S15 deployment commits onto it, push, open a clean PR, `/merge` (rebase) on explicit user go, delete the per-session branch. Do NOT PR the long-lived feature branch → main.
5. **Close** (full CLAUDE.md close protocol on the long-lived feature branch; 3 audits exit 0 at `--session 15`; PF attestation; VOLATILE rotation; commit + push). Foundation pipeline complete → the next forward direction (Pass-3 specialists / Phase-C peptide campaign) unblocks.

## 3. Disciplines carried into S15

- **BEAD `4ej` IS THE S15 PREREQUISITE (close it before `/upgrade-agent`).** XR-002 = `DEPLOY_WITH_OVERRIDE_PATH` (Role 1 design doc `design/health-specialist-architect-design.md` §13 row 15) is inverted vs the canonical `BLOCK_WITH_OVERRIDE_PATH` (Role 4 `design/medical-safety-reviewer-design.md` §4.3 row 1 + §13 deploy-verdict schema; canonical mapping CRITICAL→BLOCK, HIGH/MEDIUM→BLOCK_WITH_OVERRIDE_PATH, LOW/NONE→DEPLOY). Reconcile **Role 1 §13 row 15** to `BLOCK_WITH_OVERRIDE_PATH` via INVARIANTS.md change-discipline ritual (Role 1 doc is Status:Final — the bead authorizes the in-place edit; cite the bead + present to user). If unfixed, the inverted verdict propagates into the deployed Role 4 agent + orchestrator deploy-gate.
- **Branch topology (NEW, S14 Option A — see user-memory `project-branch-topology`).** `main` = code via clean per-session branches cut off `origin/main` (cherry-pick → clean PR → rebase-merge → delete). The long-lived `feature/wiki-bpc157-aplus-research` diverged from main at S13's rebase-merge and is the continuity carrier (HANDOFF/vault bookkeeping commit there). **Never PR feature→main.**
- **DOCUMENT_RUBRIC Rule 7** (budget overage → load-bearing review): Role 4's profile will likely exceed the ~2,000-token target (Role 1 ~3,252 / Role 2 ~5,245 / Role 3 ~6,364 — medical-domain density). Classify load-bearing vs reducible; cut only reducible; document residual vs bead `2qq`. Never blind-trim; never cut a safety binary. Keep ≤200 lines (the hard max).
- **Design-doc-inconsistency watch.** S14's /review-pr surfaced 3 frozen-design-doc defects in the Role-3 doc (`p47` flat-vs-nested severity_final, `o9y` owned-schema-list omission, `7is` non-enumerated catalog). Watch whether Role 4's design doc carries analogous owned-schema-list-vs-canonical-field or flat-vs-nested mismatches; bead any found (do not in-place edit Status:Final without change-discipline).
- **AQ-002** (voice-register use-vs-mention): Role 4's profile will hit the same banned-token-MENTION issue in its Negative Examples / threat-catalog. Disposition is fixed (deploy faithfully — mentions OK, zero usages; AC-deploy voice grep = 0; mention-aware audit is bead `3y6`). Do not re-litigate.
- **PF-S3-01 guard:** separate+parallel fact-checker/judge in `/upgrade-agent` Phase 4 (9/10 every dimension, no rounding); independent blind-triage + blind-verification agents in `/review-pr`; personally source-read every finding before classification. The S14 layered review caught a synthesis defect (Modes dead-end) that the Phase-4 judge + Phase-6 adversarial missed — Role 4's profile is the most safety-critical; run the full review stack and expect synthesized-content (no-design-anchor sections like Modes) to need it.

## 4. NOT S15 (do not pull in unless directed)

- Pass-3 specialist deep-research / `/upgrade-agent` for the 14 specialists. Phase-C peptide library campaign. These unblock only AFTER Role 4 deploys (4 of 4 foundation agents).
- Beads `ams`, `3y6` build-out (tracked, not on S15 critical path).
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue).
- Promoting any candidate INV (INV-SESSION-B-INTERLEAVING etc.) — requires the change-discipline ritual, not S15-automatic.

## 5. Sources of truth (frozen for S15)

| Artifact | Status | Path |
|---|---|---|
| Role 4 design doc | Final (S12) | `design/medical-safety-reviewer-design.md` |
| Role 1 deployed (reference shape) | Final | `.claude/agents/health-specialist-architect/agent.md` |
| Role 2 deployed (sibling) | Final | `.claude/agents/health-implementer/agent.md` |
| Role 3 deployed (S14 sibling + IDENTICAL/Jaccard oracle) | Final | `.claude/agents/health-edge-case-reviewer/agent.md` |
| XR-002 fix target | bead `4ej` (P1) | Role 1 doc §13 row 15 → `BLOCK_WITH_OVERRIDE_PATH` |
| AGENT_TEMPLATE | reference | `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` |
| /upgrade-agent skill | reference | `~/.claude/commands/upgrade-agent.md` |
| Roster B | mutable (S15 edits the safety-red-team row) | `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7 |

## 6. Compaction recovery anchor

If S15 opens after compaction:
1. Read `HANDOFF.md` (S14 close note + Top-3 + Current State + What Is Next).
2. Read THIS file.
3. Read `memory/process-failures.md` PF-S13-01 + PF-S12-01 + PF-S3-01.
4. Read `vault/sessions/session-14.md` (what S14 did) + user-memory `project-branch-topology`.
5. Run §0 session-open discipline + §1 recurrence guard.
6. Close bead `4ej` (§3) as the FIRST work-unit, THEN begin Role 4 deployment.

Mark this file `status: consumed` at S15 close.
