---
title: Session 103 — ADR-0033/0034/0035 Intake/Onboarding Build
type: session
created: 2026-07-01
status: complete
permalink: a-plus-maxing/sessions/session-103
---

# Session 103 (2026-06-30 → 2026-07-01)

## Goal
Execute the ADR-0033/0034/0035 intake/onboarding build (7-wave plan, 9 tasks) via `/execute-plan` to completion — the first-run completeness gate + platform-unlock, the unlocked shell, the care-agent review + de-associated meds curation, the composed E2E + falsification probes — then Tier-3 review → merge to `main` → full close. Continuation of the 2026-06-30 design + T1–T5 build that checkpointed at the W3 boundary without a close.

## What happened
- **Waves 4–7 built** via `/execute-plan` (T6 completeness gate `166f762`; T7 unlocked shell `a9a0eca`+`b78f03d`; T8 care-agent review `5aaf9df`+`908bd48`; T9 E2E+probes `ee8d2fa`+`c54e5d5`), each SE-TDD → EXECUTED checkpoint → Tier-2 wave review (QA always; +Security/Architect per the matrix) → plan-integrity gate. Full role profiles inlined verbatim on every dispatch.
- **Tier-2 caught a real crown-jewel defect at T8:** Security + QA independently converged on a leg-2 meds-curation identity bypass — operator identity typed into the meds free-text egressed verbatim into the leg-2 `converse` request (the mock build's own probes seeded a clean drug + injected identity into the profile, never the meds field). Fixed fail-closed (`_med_value_has_identity` scans each med value with `pii_scan` + a `_DATE_LIKE` DOB backstop, defers on any hit); Security reproduced-then-resolved by execution.
- **Local 6-lens Tier-3** (GitHub API rate-limited; operator-directed "local Tier-3 now, then local merge") over `origin/main...HEAD` with the six specialized reviewers (bug / security / contracts / test-coverage / code-quality / historical). Findings blind-triaged; the review caught, beyond the green suite:
  - a SAFETY routing break masked by a **tautological test** — drug-allergy contraindications silently dropped via a `drug-allergies`(markup)/`drug-allergy`(`_ALLERGY_FIELDS`) field-name mismatch; the `_ALLERGY_FIELDS` capture branch also dead-relative-to-production + unscanned (an unscanned `hard-limits` sink);
  - a permanent meds-curation **defer-trap** (`_scaffold_meds` unioned all historical captures → one dated med poisoned the curation forever + repeated spend);
  - the **front-end wiring gaps** (the 9-step wizard never POSTs → the gate is unreachable through the served UI; the care-review JSON receipt is read as HTML + silently dropped; `confirm_curation`/`referral.collate` unwired) — the untracked "T10";
  - a pre-existing pass-through **DOB de-id residual** (`pii_scan` has no date detector, so a full DOB in a free-text pass-through field crosses the frozen `summarize` boundary).
- **Remediation `a26c4cc`** (blind-verified by execution): allergy field-name reconcile + uncapped scan + de-tautologized test; meds-scaffold latest-capture-only (fixes trap + repeated spend); leg-1 preservation on leg-2 failure; the `_DATE_LIKE` isolated test. Full suite **2103/0**.
- **Merge:** fast-forward of `main` to the branch HEAD (no push, ephemeral-branch model; no commit ever targeted `main`).

## Deferred / beaded
- Front-end wiring "T10" (P1) — every wiring point named.
- `a-plus-maxing-yduw` (P1) — `pii_scan` DOB value-class detector; a hard blocker on the ADR-0035 OQ-1 live run.
- Record-only-free-text-now-model-bound framing reconcile + INV-CAREAGENT-EGRESS-0IDENTITY registration (operator ratification) + the T6 nav-rail + the identity_config divergence + the Tier-3 low/cosmetic roll-up.

## PF
PF-S103-01 — over-stopping via the `AskUserQuestion` menu format (twice), operator-corrected. A recurrence of the never-stop-mid-loop class (PF-S92-01). Hardened via `memory/feedback-no-askuserquestion.md`. The layered-review discipline was the session's defining positive.

## Invariants
EXTEND-NOT-REBUILD held (frozen 7-engine + store numstat=0; `SUMMARY_FIELD_SET`+`dispatch` byte-frozen; the sole non-additive router change the ADR-sanctioned `_age_band` repurpose). Crown-jewel held by execution at every de-id-touching wave; net HARDENED by the two review-driven fixes.