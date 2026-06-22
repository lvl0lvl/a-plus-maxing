---
title: Session 86 — the interactive intake website, Wave B (the wizard capture) + the crown-jewel PII fix
type: session
date: 2026-06-22
owner: Walter McGivney
status: complete
---

# Session 86 — interactive intake website (Wave B)

**Goal (operator `/goal`):** Build the interactive intake website autonomously following the rigor framework — Wave B is the interactive wizard capture (steps 2-6) so the operator fills their profile point-and-click, on the current theme, with the design-critic run over it. "Only stop if you absolutely need me to weigh in; if ambiguous, choose the more robust / more rigorous path."

**Outcome:** Wave B is BUILT, 3-tier reviewed, and MERGED to `main` @ `7c374ad` (PR #212). The interactive intake website is now COMPLETE (Wave A upload S85 + Wave B wizard capture S86). The operator can `python -m scripts.serve` → fill the steps-1-6 wizard + upload Apple Health / 23andMe → the de-identified profile lands in the store, raw/rich context in the gitignored scaffold. Built + verified entirely on SYNTHETIC fixtures — no real operator data.

## What was built + merged (PR #212)

- **`scripts/serve/capture.py` (new) — `persist_capture`:** routes each submitted form field BY DATA CLASS. The 5 de-identified `WIRED_TOKENS` (`goal-domains`, `goal-priority-order`, `goal-targets`, `hard-limits`, `recovery-status-band`) → `store.append(source="intake")` into the closed `SUMMARY_FIELD_SET` that reaches the no-train model via `summarize`; everything raw/rich (nutrition, the supplement/peptide stack, the rx field, training detail) → the gitignored `vault/scaffold/filled/` (ADR-0005), never the model. A load-time `WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` tripwire; server-side enum validation; a non-truncating full-value PII scan.
- **`vault/design/templates/intake.py`:** the steps 2-6 form markup on the CURRENT theme (the operator's explicit requirement — the design-reviewer confirmed CONSISTENT) + accessibility (focus ring, 3.22:1 control border, `fieldset`/`legend`) + honesty fixes.
- **`scripts/serve/server.py`:** `do_POST` field routing into `persist_capture`.
- **`scripts/guard/pii_scan.py`:** an additive `scan_text_full` helper (the default `scan_text` byte-unchanged) used by the capture path to scan a free-text value with no 4096-char truncation.
- **Docs reconciled:** the recipe / spec / build-plan updated so `rx-interaction-classes` is described record-only (matching the as-built routing), the curation surface deferred to ADR-0014 OQ-2.

## Rigor — the crown-jewel PII boundary stressed and held

The marquee of this session was the PII boundary (ADR-0001: zero raw PII to the no-train model). The 3-tier review caught TWO real leaks before merge:

1. **Tier-2 (executed exploits):** `rx-interaction-classes` was wired to the model-bound token, but the form field collects operator-typed text the server cannot trust to be de-identified, and the 8j6 PII gate catches email/phone but NOT drug names — so `persist_capture({"rx-interaction-classes": "warfarin 5mg"})` put a raw drug name into `summarize`. **Fixed:** removed from `WIRED_TOKENS` → routes record-only; the model-bound item is deferred to the OQ-2 curation surface (beaded).
2. **Tier-3 `/review-pr` (6-agent + design-reviewer, independence phases INTACT):** the free-text wired tokens were scanned in 4096-char windows with a 64-char overlap; a US postal address (match span > 64) straddling the window boundary past char 4096 was seen whole by neither window → it leaked into the model-bound `goal-targets` token AND `summarize`, reproduced END-TO-END through the live loopback server by two independent agents + the blind triage. **Fixed:** a non-truncating full-value scan (no window, no boundary to straddle — the value-PII patterns are unbounded-span, so no fixed overlap is provably safe); the straddle test goes RED under the old `overlap=64` and GREEN after; EXECUTED-blind-verified RESOLVED.

The review independence guarantees ran PROPERLY — profile-less blind-triage (Phase 3) + profile-less EXECUTED blind-verify (Phase 7), NOT collapsed under the long autonomous run. Six legitimate findings fixed, 6/6 blind-verified RESOLVED. 0-shared-routine-edit HELD (numstat empty; `pii_scan.py` gained only an additive helper). Suite 1264 passed / 3 skipped.

## Beaded follow-ups (none blocking)

- ADR-0014 OQ-2: the `rx-interaction-classes` curation surface (operator/liaison emits de-identified class tokens → the model-bound item).
- `summarize()` 8j6 backstop: also capped at 4096; uncap / full-scan it, single-sourced with the capture scan (defense-in-depth; no live vector once the capture leak is fixed).
- The multipart parser collapses repeated form fields last-write-wins → a multi-select `goal-domains` captures one value; add repeated-field support or join client-side.
- The full-value scan is O(n^2) on a pathological no-`@` blob (~60K chars ≈ 10s); NULL remote threat model (loopback, single-operator = self-DoS only) → a per-field length cap is a non-blocking robustness item (defensive — needs operator sign-off).
- Two design-polish items: the single-scroll stepper-nav affordance; the goal-domains chip checked-state styling.

## PF this session

**No new PF-class entries.** The continuous-drive discipline held (no pause-at-autonomous-boundary — the prior-session lesson applied; I drove fix → checkpoint → review → merge → close without a status pause). The review pipeline worked as designed (caught + fixed a real CRITICAL crown-jewel PII leak, blind-verified). One abbreviated SE-profile dispatch was caught by the `enforce-role-inlining` hook and corrected with the full profile (zero downstream impact) — a disclosure-ledger item with an active guard, not a new PF. Full attestation + the per-PR skill-trace table + the disclosure ledger (7 caught, all self/gate-caught, 0 operator-surfaced) in `memory/process-failures.md` Session 86.
