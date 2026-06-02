---
title: Batch-4 gate-3.5 ordering — one-time grandfather (bounded)
type: decision
permalink: a-plus-maxing/decisions/2026-06-01-batch4-gate35-ordering-grandfather
created: 2026-06-01
status: active
decided_by: Walter (operator)
supersedes: null
relates_to: 2026-05-30-grandfather-design-work-research-provenance
---

# Batch-4 gate-3.5 ordering — one-time grandfather (bounded)

## Decision

Merge the four batch-4 specialists whose design-work FAILS `bda`
(`scripts/audit-research-provenance.sh`) on a **gate-3.5 attestation-ordering**
defect, as a **one-time, batch-4-only exception**. The fifth
(`mental-performance-coach`) passes `bda` clean and needs no exception.

**Grandfathered under this ADR (exact list — the exception covers these slugs ONLY):**

| Slug | PR | bda failure |
|---|---|---|
| cardiovascular-specialist | #19 | gate-3.5 is `gate-3.5-summary.md`, not attested `gate-3.5.json`; also missing 4.25/7.5/8.5 |
| recovery-specialist | #21 | gate-3.5 summary-md; missing 4.25 |
| longevity-strategist | #23 | gate-3.5 summary-md |
| dermatologist | #20 | gate-3.5 summary-md; no risk-table row at audit time (added in this change) |

`mental-performance-coach` (PR #22) is NOT on this list — it passes `bda` (real
attested `gate-3.5.json`; `start-iteration` called before judge dispatch).

## Root cause

The four builders dispatched Phase-3 judge agents **before** calling
`gate_attest.py start-iteration`. With judges pre-dating the iteration window,
`gate_attest attest` would HALT `stale-agent-source`, so the builders recorded the
judge gate as a hand-written `gate-3.5-summary.md` instead of the canonical
attested `gate-3.5.json`. They cited the already-merged `gi-specialist` /
`peptide-specialist` design-work as precedent. The judge work itself is real
(dispatched paired retrieval+judge, scored, defects caught and remediated —
cardiovascular's judges caught a *retracted* paper grounding live BP numbers);
only the gate-3.5 **attestation layer** is non-canonical. `verify-chain` reports
"intact" on all four because it vacuously skips the absent canonical gate — the
exact hole `bda` exists to close.

## Why grandfather (not re-run)

1. **Re-running is cost-prohibitive at this point** (operator decision). The fix
   is an ordering change, not a research defect; re-dispatching judges to
   re-attest would re-spend the full Phase-3 cost for a provenance-layer
   formality.
2. **Consistent with the S19 hfm decision**
   ([[2026-05-30-grandfather-design-work-research-provenance]]): design-work
   research is build-time scaffolding, NOT library content. None of these four
   PRs writes a single `vault/` page (disjointness verified: each branch touches
   only its two exclusive per-slug paths). The binding provenance control remains
   the per-page library-authoring gate.
3. The judge work is genuine and the deployed agent frameworks are
   source-disciplined (cite-or-refuse, zero hardcoded facts).

## Boundary — this exception DOES NOT promulgate forward

This is the load-bearing half of the decision. The exception is sealed to the
four slugs named above. Specifically:

- **`genetics-specialist` (next build) gets NO grandfather.** Its `bda` must
  EXIT 0 at merge — real attested `gate-3.5.json`. If it ships a
  `gate-3.5-summary.md`, the integrator issues CHANGES-REQUESTED, not a second
  exception.
- **Library-population gets NO grandfather.** Every `vault/` page ships only on a
  fresh `/aplus-research` run whose `bda` / `verify-chain` passes on its OWN
  research (the hfm binding control). The batch-4 design-work is never a
  provenance source for a wiki page.
- **The `gate-3.5-summary.md` path is RETIRED.** `coordination/PROTOCOL.md` now
  mandates `start-iteration` BEFORE judge dispatch so `gate-3.5.json` is
  attestable. The gi/peptide/batch-4 summary-md precedent is explicitly
  non-canonical and must not be cited forward.
- **The integrator checklist is amended** so a `bda` EXIT≠0 blocks the merge
  UNLESS the slug is one of the four named here. Any slug not on this list is a
  hard block. Adding a slug to the exception requires a new operator decision +
  a new ADR — it cannot be done silently.

## Tripwire (landmark)

`vault/meta/landmarks.md` LM registers: the next `bda` run at a specialist merge
(`genetics-specialist`) and every library-authoring `bda`/`verify-chain` MUST be
EXIT 0. A non-zero `bda` that gets merged anyway = this exception promulgated =
PF-class failure.

## Follow-up (beaded, non-blocking)

- Per-slug gate-3.5 re-attestation debt (optional; only matters if a future
  decision makes design-work a provenance source — it is not today).
- `cardiovascular-specialist` risk-table mis-classification: `target_class:
  compound` but the role writes zero compounds (owns biomarkers/protocols/
  parameters). `bda` requires compound-only gates 7.5/8.5 it can never produce.
  Fix the row to a non-compound `target_class` before its library-authoring
  phase.
- `dermatologist` + `genetics-specialist` risk-table rows added in this change.
