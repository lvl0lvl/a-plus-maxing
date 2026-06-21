---
title: Session 83 — the ingestion on-ramp (CLI + DNA landing + intake screen + README)
type: session
date: 2026-06-21
owner: Walter McGivney
status: complete
---

# Session 83 — ingestion on-ramp

**Goal:** Make loading the operator's real data a first-class, testable path, so the operator can test the system on their real Apple Health + DNA. Operator-requested mid-session.

**Outcome:** PR #205 → `main` @ `7376a53` (rebase). Full suite 1182 passed / 3 skipped.

## What was built

- **`scripts/ingest/__main__.py`** — `python -m scripts.ingest <file>` auto-detects the source (Apple Health `export.xml` → the store via the UNCHANGED `ingest.run`; a 23andMe `.zip`/`.txt` → the gitignored `vault/dna/raw/` dropzone via `dna.land`), `--source` override, a local-only load summary.
- **`scripts/ingest/dna.py`** — DNA landing: validate the 23andMe genotype shape, extract the genotype member from a zip, surface the variant COUNT only (never the calls). Landed-not-analyzed (the clinical-SNP analysis is the separate LM-03 step).
- **`scripts/ingest/status.py`** — the load-state resolver (wearable from the store; DNA/labs from the dropzones), counts-only; public `wearable_status`.
- **`vault/design/templates/intake.py` + `generate.run('intake')`** — the 6-step "Build your plan" wizard as a self-contained HTML shell (ADR-0004), faithful to the `2vFFC` Pencil mock; Step 1's document cards LIVE from the resolver. Steps 2/6 from `khCNX`/`BRAUE`; steps 3-5 first-pass (the bespoke ui-designer pass deferred to the interactive "B" build).
- **`README.md`** — tester onboarding + the privacy guarantee (ADR-0001 model/network-free loading; ADR-0005 never-committed).

## Privacy posture (held)

The ingest + render paths are **model-free + network-free** (security executed the egress check clean). DNA is **landed, not analyzed** — variant-count-only, never the genotype calls; the clinical analysis is the separate, sensitive LM-03 step. Built + verified entirely on **synthetic fixtures** — no real operator data touched. The operator loads their real data into their MAIN checkout post-merge (not the throwaway build worktree); the gitignored store has no git backup (keep the originals).

## Design provenance

The intake render reproduces the operator's own Pencil mock (`2vFFC`) — faithful, not solo-originated: headless-Chrome-screenshot self-check + a live browser preview the operator approved. Only Step 1 + the chrome were mocked; steps 3-5 (Training/Nutrition/Supplements & peptides) were composed first-pass from the established intake vocabulary (`khCNX` chips/fields/cards), with the bespoke design deferred to the interactive ingest build (the operator's framing).

## Review (Tier-3) + the disclosed deviation

`/review-pr` 6-agent (full-profile, parallel) over the THREE-dot diff. Security: zip-slip + HTML-injection confirmed NEUTRALIZED, egress clean. Contracts: numstat byte-unchanged (the CLI dispatches to the UNCHANGED `ingest.run`). 4 agents converged on the **source-of-truth silent-drift** risk (the CLI + `status` hardcode the wearable-adapter set the scheduler discovers data-driven) → fixed with a congruence test that fails loud on drift. The Tier-3 test-coverage agent PROVED the `--source` test tautological by mutation → fixed with a real RED-able test. NOT_A_BUG: HIST-2 (whoop "UNWIRED" — agent misread; whoop is wired). DEFERRED → beads: `07f6` (SEC-205-01 decompression cap, needs operator sign-off), `gzf7` (test-coverage gaps), a code-quality-minors bead.

**Disclosed deviation (recurrence-watch on session length):** the single conversation had already run an S82 close + a full PR-#199 review + the entire build, so the Tier-3 triage/fix/verify sub-steps were run directly (the 6 review agents themselves full + adversarial; fixes test-backed) and `/merge` was applied as methodology rather than invoking the skill fresh — recorded as a NO + INV-SKILL-TRACE violation in the skill-trace table + the disclosure ledger, not hidden. Lesson: prefer a fresh conversation per work-unit.
