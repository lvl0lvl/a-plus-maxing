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
| INV-HO-ROTATION | HANDOFF.md | 6-clause rotation | Volatile sections contain only current-session content + at most one Historical pointer line | `scripts/handoff-audit.sh` (clauses 2 + 5 enforced; clauses 1 + 6 require prior-version diff — v2); smoke tests `scripts/tests/test_handoff_audit.sh` (12/12 pass) | S2 |
| INV-HO-NO-STALE-HASH | HANDOFF.md | no SHA prefixes in narrative | HANDOFF prose does not cite sha256/commit hash prefixes; provenance lives in artifact citations | `scripts/handoff-audit.sh` content-pattern check (lenient: section-header date OR same-line date satisfies clause 4); smoke tests `scripts/tests/test_handoff_audit.sh` (12/12 pass) | S2 |
| INV-RESEARCH-ATTESTATION | aplus-research | gate JSON attestation_chain required | Gate JSONs for phases 3.5/4.75/6/7.5/8.5 carry `attestation_chain` matching agent-source sha256 + mtime > iter_start_ts | `lib/gate_attest.py` + schema validation; smoke tests `tests/test_gate_attest.py` (9/9 pass) | S3 |
| INV-RESEARCH-POPULATION-MISMATCH | aplus-research | animal/in-vitro numerical claims tagged | Every animal/in-vitro numerical claim carries `[population-mismatch: <species>]` in same sentence or has species as subject within 100 chars | aplus-research IC-7 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-CONCENTRATION-SURFACED | aplus-research | first-class concentration section | When single-cluster share ≥70%, draft has first-class concentration section before any indication subsection | aplus-research IC-9 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-NO-VENDOR-NUMERICAL | aplus-research | vendor/anecdote cites never ground numerical | `vendor_label` and `anecdote_aggregate` tags never appear in same sentence as dose/effect-size/AE-rate/n claim | aplus-research IC-3 + IC-4 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-IC13-CORPUS | aplus-research | per-citation corpus scoping | Deep mode requires ≥80% (min 20) of numerical/quoted claims grep-verified against retrieved source corpus | aplus-research IC-13 verifier (Phase 4.75) | S2 |
| INV-RESEARCH-CROSS-SECTION-ID | aplus-research | shared-entity reconciliation | Citations, institutions, compound identifiers, regulatory dates, and trial registrations appearing in 2+ section drafts must agree; mismatches HALT before outline refinement | Phase 4.25 ID-Reconcile gate; schema `schemas/gate-4.25.schema.json`; gate-attest tests T13-T16 (4/4 pass) | S6 |
| INV-ROLE-INLINING | Task dispatch | full 11-section role profile | Agent dispatches matching role-context (H1=`# {Role Name}` or `roles/<slug>/agent.md` ref) inline the full 11-section profile verbatim; 9th section is an operational slot accepting `## Modes` \| `## Audit Protocol` \| `## Task Routing` (hook v2.5) | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook; smoke tests `hooks/tests/test_enforce_role_inlining.sh` (11/11 pass) | S3 |
| INV-SCOPE-CONTRACT | Session lifecycle | binary AC + WILL/NOT lists | Every session has a written scope contract before any work: Goal, binary ACs, Files I WILL touch, Files I will NOT touch, NOT doing, Invariants at risk | `scripts/scope-contract-audit.sh` (validates 6 required subfields + ≥1 binary checkbox); smoke tests `scripts/tests/test_scope_contract_audit.sh` (12/12 pass) | S3 |
| INV-BRANCH-NOT-MAIN | git | no commits on main | Working commits land on `feature/*` or `fix/*` branches, never `main` | `.claude/hooks/block-push-main.sh` (push) + `.claude/hooks/block-commit-main.sh` (commit) — both PreToolUse Bash hooks; smoke tests `.claude/hooks/tests/test_block_commit_main.sh` (21/21 pass) | S2 |
| INV-PF-ATTESTATION | Session close | mandatory "No PF" attestation | Every session close either appends a PF entry OR explicitly attests "No new PF-class entries this session" with rationale | `scripts/pf-attestation-audit.sh` (validates `S<N> close (YYYY-MM-DD):` line presence); smoke tests `scripts/tests/test_pf_attestation_audit.sh` (12/12 pass) | S3 |

## Category breakdown

- **Format / Document:** INV-HO-ROTATION, INV-HO-NO-STALE-HASH
- **Process:** INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN
- **Role-discipline:** INV-ROLE-INLINING
- **Research-domain (aplus-research):** INV-RESEARCH-ATTESTATION, INV-RESEARCH-POPULATION-MISMATCH, INV-RESEARCH-CONCENTRATION-SURFACED, INV-RESEARCH-NO-VENDOR-NUMERICAL, INV-RESEARCH-IC13-CORPUS, INV-RESEARCH-CROSS-SECTION-ID

## Change Log

| Date | Invariant | Change | Evidence | Session |
|---|---|---|---|---|
| 2026-05-25 | (all initial entries) | Created register | PF-S3-01 demonstrated gap; Rigor Framework Discipline 5 adopted | S3 |
| 2026-05-25 | INV-HO-ROTATION, INV-HO-NO-STALE-HASH, INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN | Mechanical verification promoted from TODO to live scripts/hooks | Audit scripts + commit-block hook built and tested (57/57 across 4 suites); wired into close protocol step 8.5 | S5 |
| 2026-05-25 | INV-RESEARCH-CROSS-SECTION-ID | Added | v2 calibration AC1: S3/S4 BPC-157 iter-3 surfaced cross-section metadata mismatches that iter-2 missed (PMID inversion in Section A; Xue 2004 institution narrative drift in Section C). Phase 4.25 ID-Reconcile gate prevents this class upstream of integrity verifier. | S6 |
| 2026-05-28 | INV-ROLE-INLINING | Hook v2.5: 9th section is operational-slot synonym set (`## Modes` \| `## Audit Protocol` \| `## Task Routing`) rather than literal `## Modes` | E1 recurrence_count=3 across S9/S10/S11 — required structural fix per Rigor Framework Discipline 8. Survey of `~/Documents/Projects/skills_library/roles/*/agent.md` confirms the 9th section varies by role (security uses Audit Protocol, orchestrator uses Task Routing). Smoke tests extended 8→11; existing 8 still pass. | S12 |

## Audit cadence

- Session close: every invariant whose mechanical verification is automated runs.
- Every 5 sessions: full register reviewed for entries whose mechanical verification is still TODO.
- On PF entry: cross-reference whether any invariant was violated. If yes, log under "documented failure" rationale in the relevant invariant row.

## Pending mechanical-enforcement gaps (TODO)

All S4-vintage TODOs were resolved in S5. Remaining gaps for future sessions:

- INV-HO-ROTATION clauses 1 (replace-don't-accrue) + 6 (session-close diff check) require diffing HANDOFF.md against the prior-session-N snapshot. Deferred to v2 once a session-versioned snapshot system exists.
- `audit-helpers.sh` does not yet emit machine-parseable JSON (only human-readable stderr). Promote to JSON line-protocol if/when a close-protocol orchestrator wants to aggregate results programmatically.
