---
title: 'Decision: Grandfather design-work research provenance; library-authoring gate is the binding control'
type: decision
permalink: a-plus-maxing/decisions/grandfather-design-work-research-provenance
created: 2026-05-30
session: S19
---

# Decision: Grandfather design-work research provenance (hfm)

## Context

`bda` (`scripts/audit-research-provenance.sh`, S18) was run across all 10 deployed
specialists' `design/.<slug>-design-work/` (S19). Result: 9 of 9 research-dispatching
specialists FAIL; `medical-liaison` is N/A (collation-only). No deployed specialist
currently passes bda. The `hfm` bead asked: per failing agent, BACKFILL (re-run the
missing `/aplus-research` gates) or GRANDFATHER (accept the framework-sound agent, gate
only future research)?

Failures classified by the substrate *beneath* the uniform EXIT=1 (S19 inventory):

| Tier | Specialists | Substrate |
|---|---|---|
| N/A collation | medical-liaison | no research dispatch — correctly exempt |
| Partial-canonical | gi-specialist | real `gate_attest.py` run (canonical `gates/`, 2 of 5 required gates, 6 judge JSONs, 3 sections) — ran the skill, didn't finish |
| Non-canonical / mimicked | supplement-specialist | most-complete gate set (2.75→8.5) but in `research-gates/` with bare source paths — NOT produced by `gate_attest.py`; imitates the output. Sits on top of REAL research (5 judge JSONs + 6 sourced sections) |
| Dispatched, no attestation | peptide, endocrine, sleep-coach, personal-trainer, lymphatic | real dispatched paired-judge research (2–4 judge JSONs + sourced sections) but zero attestation chain — orchestrator-level discipline, never entered the gated path |
| Bare substrate | labs, nutritionist | thinnest — only `domain-research.md` at Phase-0; no judges/sections/gates |

## Decision

**Grandfather all 9 deployed frameworks.** Do not backfill the design-work research.
The **library-authoring gate is the binding provenance control.**

Rationale (three load-bearing facts):

1. **The audited research never reaches the wiki.** It is build-time scaffolding that
   shaped each agent's *framework*. Library pages (`vault/library`, `compounds`,
   `biomarkers`, `protocols`) are authored by *fresh*, goal-agnostic `/aplus-research`
   at runtime — not by reusing design-work research (SKILL.md §1.1 "library-build
   dispatches are goal-agnostic"; WIKI.md "never write a page from memory — read the
   source first"). Backfilling design-work research re-runs research the library phase
   runs again from scratch: motion with no library-integrity payoff.

2. **The frameworks do not carry the research's claims.** Deployed agents are
   0-hardcoded-fact, cite-or-refuse (verified S18). Even were a design-work research
   doc wrong, the deployed agent does not repeat it — it cites live or refuses
   (`BASIS_NOT_REVIEWABLE`). Build-time research provenance is therefore not
   load-bearing for anything merged.

3. **The gap that CAN reach the wiki is already gated.** `bda` +
   `coordination/INTEGRATION-CHECKLIST.md` step 1a block any `vault/` write whose fresh
   research lacks a passing `verify-chain`. That control exists and bites at the point
   that matters — library-authoring time.

## Supplement-specialist carve-out (the one targeted action)

Supplement's `research-gates/` *mimics* canonical `gate_attest.py` output (a
trust-erosion signal distinct from "didn't run gates"). The fix is **quarantine, not
re-run**: relabel/quarantine the mimicked `research-gates/` so no future reader mistakes
it for canonical provenance. Folded into bead `0be` (which pins the canonical `gates/`
convention and already touches that dir). A deep-mode re-run was rejected: it would
produce a clean record for research that gets superseded at library time regardless —
quarantine kills the deception; the re-run buys a record no downstream consumer reads.

## Consequences

- All 9 deployed frameworks accepted as-is (reviewed, sound, merged — unchanged).
- `0be` (P2): pin canonical `gates/` convention in SKILL.md + design-doc-protocol AND
  quarantine supplement's mimicked `research-gates/`. Do before batch-4 or any library work.
- **Standing posture:** no `vault/` page is authored without a passing bda/verify-chain
  on that page's own fresh research. The library-authoring gate is the binding control.
- batch-4's 5 remaining specialists (cardiovascular, recovery, longevity-strategist,
  mental-performance-coach, dermatologist) clear bda at merge (INTEGRATION-CHECKLIST 1a
  already enforces).
- What this gives up: we do not force a "prove you can run the gated path" until library
  time. Accepted — the library gate IS that proof, at the moment it counts.

## Provenance

S19 bda run: `/tmp/bda-s19-results.txt` (regenerable via the loop in HANDOFF "What Is
Next"). Substrate inventory: `git ls-tree -r origin/main design/.<slug>-design-work`.
Decision authored 2026-05-30 (S19) on Walter's explicit approval of Option A.
