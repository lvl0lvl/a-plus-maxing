---
title: Session 76 — supplement↔Rx BPMH axis (rxbp), Phase-4 follow-on
type: session
status: complete
created: 2026-06-19
last_reviewed: 2026-06-19
permalink: a-plus-maxing/sessions/session-76
---

# Session 76 (2026-06-19)

## Goal

Wire the supplement↔Rx **BPMH axis** (`rxbp`, bead `71s4` Phase-4) — read the operator medication surface through the `router.summarize` PII de-identification boundary (ADR-0006-T0) as de-identified Rx-interaction-class tokens, then hold a compound whose author-declared interaction class stacks against a present Rx-class and route it through the **reused** S74 medical-liaison `adjudicate` gate. Operator delegated S76 autonomously ("proceed"). Chosen as the highest-rigor remaining Phase-4 surface — it hardens the project's most security-load-bearing seam (the PII boundary) and produces the medication-interaction flags most relevant to the July MD visit (LM-01).

## What was built

- **`scripts/plan/router.py` — the PII boundary extends to medications.** A new de-identified `rx-interaction-classes` field in `SUMMARY_FIELD_SET` carries operator/liaison-curated class tokens (the canonical AE-class vocabulary — `bleeding-risk`, `cyp3a4-pgp`, …), always-set with a `""` no-meds default (mirroring `recent-trend-direction`). The raw `medication-list` is added to `EXCLUDED_RAW_PII` and is NEVER read (no `_RAW_TO_FIELD`/derivation entry) — the drug-name→class de-identification is an operator/liaison CURATION step at the store layer, so **no pharmacology DB enters `scripts/`**. `_rx_interaction_classes_token` runs the 8j6 PII backstop; `rx_interaction_class_set` parses the `;`-joined scalar for the orchestrator.
- **`scripts/plan/orchestrate.py` — the BPMH screen + the independent hold.** `_rx_bpmh_matched_classes` intersects a compound's declared `additive_classes` with the operator's present Rx-classes; a match holds the compound (supplements OR peptides — symmetric) in an INDEPENDENT `rx_bpmh_held` set; `generate_plans` routes each via the REUSED `adjudicate` gate (`_rx_bpmh_safety_finding` → the S74 override-record schema + critical-non-overridable gate, `adjudicate.py` UNCHANGED). A domain records only when in NONE of `holds`/`conflict_held`/`rx_bpmh_held` (the PF-S75-01 multi-concern model).
- **Real medical-liaison E2E (PII-free synthetic operator/Rx).** Two real deployed `medical-liaison` dispatches (full profile inlined) genuinely DISCRIMINATED on the medication: **aspirin + fish oil → HIGH/H3** cleared via a content-valid informed-refusal override (records the supplement); **warfarin + fish oil → CRITICAL/H2** non-overridable `mechanical-auto-block-per-R3` (the vitamin-K/warfarin watchlist; the operator's informed-refusal does NOT lower the band, grounded against the project's own H2 classification). Captured `liaison-rxbp-{cleared,blocked}.example.json`. The cleared envelope was REVISED by the liaison under the real gate's reject feedback (its `operator_reason` had embedded a vacuous-stop-list phrase — Core Rule 8 repair).

## Review (three-tier)

- **Tier-1:** suite 1030/3, floor 15/0, core-capability green; each behavior mutation-proven RED (the screen, the multi-concern recording check, the PII backstop, the real-E2E caution_verbatim).
- **Tier-2:** plan-integrity (READ-ONLY, full profile) caught 2 doc-freshness SHOULD-FIX — SF-1 (the `orchestrate.py` docstring said "four behaviors", enumerated five) + SF-2 (the `author-dispatch-process.md` deferred section still listed `rxbp` as unbuilt, the MF-1 class) — both fixed; QA (Run-It owner, full profile) PASS + added the triple-concern + peptide-side composition coverage (mutation-proven).
- **Tier-3 `/review-pr` (6-agent, over the local diff under GraphQL exhaustion):** the security-auditor caught **SEC-1 — a real PII leak on the ADR-0006-T0 boundary**: the 8j6 backstop scanned the whole `;`-joined value, defeated by `pii_scan.scan_text`'s `_MAX_SCAN_TEXT_LEN = 4096` truncation once this first list-typed field exceeds it → PII past byte 4096 leaked into the no-train summary. Reproduced (a 5629-char value, email at offset 5609 survived), blind-triaged LEGITIMATE (independently reproduced), fixed via a **per-token scan** (each class token short, the cap never bites), mutation-proven RED, blind-verified RESOLVED (executed). Plus QUAL-1 (docstring Args/Returns) + TEST-rxbp-2 (both-open precedence). Bug-hunter / contracts / historical-context were CLEAN. 2 findings independently triaged NOT_ACTIONABLE.

## Process failure

**PF-S76-01** — Tier-1/Tier-2 self-review under-probed the new PII-backstop's BOUNDARY-SIZE interaction with the EXISTING `scan_text` 4096-char truncation; Tier-3 caught a real PII leak. Recurrence 3 of `AP-SELF-REVIEW-UNDER-PROBES-INTERACTION-SURFACE` (S74 routing-key input class; S75 multi-concern hold composition). The prior interaction-probe (`sip9`) was scoped to hold×hold; it did NOT cover a new value/field × the existing shared infrastructure it flows through, nor the boundary-size case against the guarding validator. Structural fix beaded `pwpr` (pairs with `sip9`): broaden the Tier-1 interaction-probe to probe the max-legitimate-input case against every guarding validator + the new-mechanism × existing-shared-utility-assumption surface. Captured 3-layer (PF log + `harvest.jsonl` + `pwpr`).

## Outcome

PR #174 → `main` (rebase merge). All 6 ACs PASS. The BPMH axis is wired and operator-usable via the terminal gate; the PII boundary is stronger after the SEC-1 fix, not weaker. The close gate was re-run on the final post-merge `main` (the PF-S74-01 discipline). Beads: `rxbp` CLOSED, `pwpr` created. The remaining Phase-4 surface is the doctor-visit-queue/SBAR handout artifact (S77), then the measure/adjust legs.
