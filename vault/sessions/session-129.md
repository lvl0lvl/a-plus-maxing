---
title: Session 129
type: session
date: 2026-07-11
permalink: a-plus-maxing/sessions/session-129
---

# Session 129 — comprehensive-plan Wave-1 task recipes (create-task-plan)

## What happened
Resumed the comprehensive-plan build loop into the terminal planning stage: ran `/create-task-plan` for build-plan **Wave 1** = {ADR-0041-T1, ADR-0042-T1}, producing the first two executable TDD recipes. Did NOT stop at the planning→build boundary — the operator's standing "run the loop" directive + the resume-the-loop discipline. The S128 close was finalized first (two coupled close-audit violations — the S128 Resume cited commit SHAs without an adjacent date, failing INV-HO-NO-STALE-HASH + the coupled floor `test_handoff_audit.sh` — both cleared by removing the SHAs from the Resume narrative). 0 `scripts/` changed (recipes are docs).

## Deliverables
- **`docs/task-plan/adr-0041-t1.md`** (status: approved) — the uniform seven-field DOMAIN PROGRAM schema + conformance validator (greenfield `scripts/plan/domain_program.py`; the schema every downstream specialist emits + the orchestrator/model/monitoring consume). 6 spec ACs → 13 RED-capable tests.
- **`docs/task-plan/adr-0042-t1.md`** (status: approved) — the crown-jewel Context Assembler (`scripts/plan/context_assembler.py` + the `generate_plan.py:356` `router.summarize`→`assemble_context` swap): feeds specialists the full identity-stripped record, replacing the DATA-COLLAPSE. 7 spec ACs → RED tests incl. the crown-jewel identity-leak + genetics carve-out mutation-RED probes.
- Both committed on `feature/comprehensive-plan-adr` (`04894c15`).

## The rigor loop (per recipe)
Author (SE, full profile inlined) → Phase-4 review (QA always; Architect for the interface/schema task; Security for the crown-jewel task) → Phase-5 remediation (all findings blocking) → Phase-6 validate → Phase-7 judge (fresh agent, 10-dimension rubric, ≥9/10). Both recipes landed **10/10 on all ten dimensions**. Cross-recipe manifest check PASS (disjoint: `domain_program.py`+test vs `context_assembler.py`+`generate_plan.py`+test).

## What the review caught (the loop working)
The mock-authored drafts each had a real load-bearing defect the review found + remediation fixed:
- **ADR-0041-T1 (QA + Architect converged):** the domain-kind discriminator was NOT RED-capable — a kind-blind validator passed the whole suite — AND a partial interface (no closed vocabulary, no fail-closed on missing kind → reopening the AC-4 fail-closed guarantee). Fixed: a closed `DOMAIN_KINDS` vocab + fail-closed + a kind-contrast test pair (same field-state, opposite verdict → forces kind-reading). Plus the `cross_domain_seams` edge shape (a T1-owned deliverable that 0043-T2 reads + 0046-T1 emits) pinned.
- **ADR-0042-T1 (Security, executed audit):** the read-set read as a **denylist** that leaked the three health-identifier classes (MRN / insurance-id / provider-name) with no downstream backstop (`assemble_context`→`client.author` inlines to the model directly), and AC-4 seeded only 5 of 10 identity classes; plus a nested-flatten depth hole. Fixed: a fail-closed **health-substance allowlist** (mirroring the existing `_care_profile._CARE_HEALTH_DETAIL` precedent — not a new de-id scheme; "all health substance flows" preserved by full enumeration) + AC-4 seeding all 10 classes + a flat-scalar payload contract + recursive scan + a nested-sentinel reach test.

## The frozen spine + de-id (unchanged)
0041-T1 is greenfield (no frozen edit). 0042-T1's `:356` swap supersedes the plan-path USE of `router.summarize`; `router.py` + the 6-file `<always-frozen>` glob (incl. `adjust.py`) stay byte-frozen (numstat=0 checks in Entry State + regression). De-id PARKED; the genetics de-id-by-construction crown jewel preserved (raw genotypes never cross; only the coarse `genetic-trait-classes` token). ZERO operator PII in either recipe (synthetic probes only; public repo).

## Process
No new PF-class entries. The `/create-task-plan` rigor loop worked as designed (find→remediate→judge); the prior product-not-plumbing lesson + read-the-full-record discipline both held (author/reviewer/judge each grounded against the LIVE tree; the security review executed its checks). Disclosure ledger: 3 caught (all self/gate — the S128 stale-hash near-miss, the two recipe falsifier under-specifications, the `adjust.py` numstat omission).

## Next
`/create-task-plan` Waves 2-6 (the remaining 13 recipes) OR `/execute-plan` Wave 1 (build {ADR-0041-T1, ADR-0042-T1}, mock/fixture-tested, 0 spend). The highest-leverage downstream task is ADR-0043-T1 (the care-agent orchestrator system-prompt rewrite — the fastest visible proof the platform writes the plan). Bead `a-plus-maxing-xzs9`. EXECUTE's LIVE runs are the operator-present boundary. Two operator-owned calls stay PARKED: the health-laden `design/*` docs' privacy, and the ADR branch → PR-to-main.
