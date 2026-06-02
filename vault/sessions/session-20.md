---
title: Session 20 — 0be Part 1 + batch-4 integration (5 specialists) + genetics-specialist setup
type: session
permalink: a-plus-maxing/sessions/session-20
created: 2026-06-01
session: S20
---

# Session 20 (2026-05-30 → 2026-06-01)

## Goal (as contracted + as expanded)

Contract: land `0be` (pin canonical `gates/` layout + quarantine supplement's
non-canonical `research-gates/`). Expanded mid-session at Walter's direction into:
set up + integrate **batch-4** (the 5 remaining specialists) and add a 16th roster
slot, **genetics-specialist**.

## What happened

1. **`0be` Part 1 (pin) — DONE.** Canonical `gates/` / `judges/` / `sections/`
   layout pinned as single source of truth in `aplus-research SKILL.md`,
   referenced from `design/DESIGN_DOC_TEMPLATE.md`. Part 2 (supplement quarantine
   marker) committed on `fix/supplement-gates-quarantine` + pushed; PR deferred to
   the REST merge lane (GraphQL throttled). `0be` stays OPEN for the PR merge.
   - Empirical correction: supplement's gates are GENUINE `gate_attest.py` output
     misfiled under `research-`-prefixed names (verify-chain passes on rename),
     NOT "mimicked/faked" as S19 described. Marker worded accurately.

2. **batch-4 built + merged (5 specialists).** Builders ran the full pipeline in
   their own worktrees; all 5 reached READY-TO-MERGE.
   - Integrator gates on each: **drafter-binding** (deployed medical agents —
     VERIFIED from the draft files on all 5; no PF-S12-01), **disjointness**
     (clean — only the 2 exclusive paths + canonical gates/judges/sections),
     **bda**.
   - **bda: mental-performance-coach PASSES clean** (called `start-iteration`
     before judge dispatch → real attested `gate-3.5.json`). The other 4
     (cardiovascular, recovery, longevity, dermatologist) FAIL on the same
     **gate-3.5 attestation-ordering** defect: judges dispatched before
     `start-iteration` → recorded as `gate-3.5-summary.md`, inheriting the
     gi/peptide precedent.
   - Merged via REST `gh api .../merges` (rebase): #22, #19, #21, #23, #20.
     `origin/main` → `a0a3fa9`. **19 agents live = 4 foundation + 15 specialists.**

3. **gate-3.5 grandfather — bounded, one-time.** Walter approved merging the 4
   bda-failing PRs as a batch-4-only exception (re-running cost-prohibitive;
   consistent with S19 hfm — design-work ≠ library content; no `vault/` page
   touched). **Containment shipped so it does NOT promulgate forward:**
   - ADR [[2026-06-01-batch4-gate35-ordering-grandfather]] names the exact 4 slugs.
   - `coordination/PROTOCOL.md` mandates `start-iteration` BEFORE judge dispatch;
     retires `gate-3.5-summary.md` by name.
   - `coordination/INTEGRATION-CHECKLIST.md`: bda EXIT≠0 = HARD BLOCK except the 4
     named slugs; no second grandfather without a new operator decision + ADR.
   - Falsification window: **genetics-specialist bda MUST EXIT 0.**

4. **genetics-specialist (16th roster slot) set up.** Kickoff + outbox + WIKI row
   + risk-table row (`mode_floor: deep`, `target_class: reference`) created; build
   NOT started. Closes the genetics/pharmacogenomics gap (becomes OWNER of
   `vault/dna/` — a role no prior specialist held).

## Decisions

- **Grandfather batch-4 gate-3.5 ordering (one-time, bounded).** ADR
  [[2026-06-01-batch4-gate35-ordering-grandfather]].
- **Do NOT change cardiovascular's risk-table `target_class`** — it's correct for
  runtime CV-drug dispatch; the real defect is a systemic bda limitation (7.5/8.5
  required for reference-landscape research that never produces a compound entry).
  Beaded `mhg` + `5ot`, not patched per-slug.

## Bead changes

- Filed (integrator): `mhg` (P2, bda 7.5/8.5 reference-vs-entry — load-bearing),
  `5ot` (P2, cardio risk-class), `3v5` (P2, WIKI longevity Owns), `xg4` (P2,
  endocrine 5ARI gap), `ae0`/`d6g`/`4ba`/`3v6`/`dip` (P3, PROPOSED audits +
  cosmetics).
- `0be` remains OPEN (Part 2 PR pending merge).

## Artifacts

- ADR: `vault/decisions/2026-06-01-batch4-gate35-ordering-grandfather.md`
- Risk table: `templates/specialist-risk-class.yaml` (+ dermatologist + genetics rows)
- WIKI: `vault/WIKI.md` (+ genetics-specialist row)
- 5 builder outboxes carry MERGED replies; worktrees + branches torn down.

## What is next

- **Launch + integrate genetics-specialist** → 16/16 roster complete. bda MUST
  EXIT 0 (grandfather seal falsification window).
- **Library-population** (epic `c6k`) — the first actual product (operator-facing
  wiki); each page gated by fresh `/aplus-research` + passing bda. Resolve `mhg`
  (systemic 7.5/8.5 limitation) before heavy authoring.

## Follow-up (2026-06-02): genetics-specialist MERGED → roster COMPLETE

genetics-specialist built + integrated (PR #24, main `53b23a0`). **16/16 specialists +
4 foundation = 20 agents deployed.** The agent-build phase is DONE.

- **bda EXIT 0 from the integrator's own run — NO grandfather invoked.** This was the
  falsification window for the batch-4 gate-3.5 grandfather seal ([[2026-06-01-batch4-gate35-ordering-grandfather]]):
  it HELD. genetics entered the canonical gated path correctly (real attested
  `gate-3.5.json`; `start-iteration` before judges).
- The PROTOCOL step-5.5 builder SELF-GATE (added before launch) worked as designed: the
  builder ran bda itself and shipped green; integrator independently re-verified.
- Drafter-binding clean (deployed medical agents); disjointness clean.
- Beads filed: `t7z` (design §5/§15.2 numbering), `fsr` (dna-metadata-contract audit),
  `8qe` (6 dna-reading specialists' consumption conformance). Bead #1 (rebase precondition)
  resolved at merge — risk-table row + bda + INV all present, bda re-run EXIT 0.
- Next: library-population (epic `c6k`) — first actual product. Fix systemic bda 7.5/8.5
  limitation (`mhg`) before heavy compound-page authoring.
