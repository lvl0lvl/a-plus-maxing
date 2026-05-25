---
title: Project Invariants Register
type: reference
status: active
created: 2026-05-25
last_reviewed: 2026-05-25
review_cadence: every-5-sessions
permalink: a-plus-maxing/invariants
---

# Project Invariants Register

Rules that MUST remain true across all sessions and dispatches. Distinct from guidelines, conventions, or stylistic preferences. The defining property is binary: at any moment, the rule is either satisfied or violated, and violation requires explicit user approval BEFORE the work proceeds.

> **Mechanical enforcement principle:** Invariants get scripts. If a rule is important enough to be called an invariant, it earns a script (or schema, or hook) that audits it. Rules that AREN'T mechanically enforceable get classified differently — as guidelines, anti-patterns, or decision records — but NOT as invariants. See Rigor Framework Discipline 5.

## Change discipline

Invariants change only by this four-step ritual:
1. Cite the invariant being violated.
2. Present new evidence (PF entry, downstream consumer report, etc.).
3. Explicit user approval.
4. Append a row to the Change Log table below with date, old, new, evidence, session ID.

This prevents soft erosion via small exceptions.

---

## Register

| ID | Scope | Property | One-line statement | Mechanical Verification | Auth |
|---|---|---|---|---|---|
| INV-HO-ROTATION | HANDOFF.md | 6-clause rotation | Volatile sections contain only current-session content + at most one Historical pointer line | `scripts/handoff-audit.sh` (TODO S4) | S2 |
| INV-HO-NO-STALE-HASH | HANDOFF.md | no SHA prefixes in narrative | HANDOFF prose does not cite sha256/commit hash prefixes; provenance lives in artifact citations | `scripts/handoff-audit.sh` content-pattern check (TODO S4) | S2 |
| INV-RESEARCH-ATTESTATION | aplus-research | gate JSON attestation_chain required | Gate JSONs for phases 3.5/4.75/6/7.5/8.5 carry `attestation_chain` matching agent-source sha256 + mtime > iter_start_ts | `lib/gate_attest.py` + schema validation; smoke tests `tests/test_gate_attest.py` (9/9 pass) | S3 |
| INV-RESEARCH-POPULATION-MISMATCH | aplus-research | animal/in-vitro numerical claims tagged | Every animal/in-vitro numerical claim carries `[population-mismatch: <species>]` in same sentence or has species as subject within 100 chars | aplus-research IC-7 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-CONCENTRATION-SURFACED | aplus-research | first-class concentration section | When single-cluster share ≥70%, draft has first-class concentration section before any indication subsection | aplus-research IC-9 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-NO-VENDOR-NUMERICAL | aplus-research | vendor/anecdote cites never ground numerical | `vendor_label` and `anecdote_aggregate` tags never appear in same sentence as dose/effect-size/AE-rate/n claim | aplus-research IC-3 + IC-4 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-IC13-CORPUS | aplus-research | per-citation corpus scoping | Deep mode requires ≥80% (min 20) of numerical/quoted claims grep-verified against retrieved source corpus | aplus-research IC-13 verifier (Phase 4.75) | S2 |
| INV-ROLE-INLINING | Task dispatch | full 11-section role profile | Agent dispatches matching role-context (H1=`# {Role Name}` or `roles/<slug>/agent.md` ref) inline the full 11-section profile verbatim | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook; smoke tests `hooks/tests/test_enforce_role_inlining.sh` (8/8 pass) | S3 |
| INV-SCOPE-CONTRACT | Session lifecycle | binary AC + WILL/NOT lists | Every session has a written scope contract before any work: Goal, binary ACs, Files I WILL touch, Files I will NOT touch, NOT doing, Invariants at risk | Close protocol step 0 checks for scope contract presence (TODO S4 audit script) | S3 |
| INV-BRANCH-NOT-MAIN | git | no commits on main | Working commits land on `feature/*` or `fix/*` branches, never `main` | `.claude/hooks/block-push-main.sh` (push only); pre-commit hook TODO S4 | S2 |
| INV-PF-ATTESTATION | Session close | mandatory "No PF" attestation | Every session close either appends a PF entry OR explicitly attests "No new PF-class entries this session" with rationale | CLAUDE.md close protocol step 4 (manual; audit TODO S5) | S3 |

## Category breakdown

- **Format / Document:** INV-HO-ROTATION, INV-HO-NO-STALE-HASH
- **Process:** INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN
- **Role-discipline:** INV-ROLE-INLINING
- **Research-domain (aplus-research):** INV-RESEARCH-ATTESTATION, INV-RESEARCH-POPULATION-MISMATCH, INV-RESEARCH-CONCENTRATION-SURFACED, INV-RESEARCH-NO-VENDOR-NUMERICAL, INV-RESEARCH-IC13-CORPUS

## Change Log

| Date | Invariant | Change | Evidence | Session |
|---|---|---|---|---|
| 2026-05-25 | (all initial entries) | Created register | PF-S3-01 demonstrated gap; Rigor Framework Discipline 5 adopted | S3 |

## Audit cadence

- Session close: every invariant whose mechanical verification is automated runs.
- Every 5 sessions: full register reviewed for entries whose mechanical verification is still TODO.
- On PF entry: cross-reference whether any invariant was violated. If yes, log under "documented failure" rationale in the relevant invariant row.

## Pending mechanical-enforcement gaps (TODO)

These invariants currently rely on manual discipline; promote to script by S5:

- INV-HO-ROTATION + INV-HO-NO-STALE-HASH → `scripts/handoff-audit.sh`
- INV-BRANCH-NOT-MAIN → pre-commit hook (currently only push is blocked)
- INV-SCOPE-CONTRACT → close-protocol audit (checks HANDOFF.md for scope contract appended at session start)
- INV-PF-ATTESTATION → close-protocol audit (checks PF log was either appended-to or carries explicit "No PF this session" line dated this session)
