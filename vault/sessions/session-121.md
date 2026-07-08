---
title: Session 121 — de-id boundary FINALIZED (bare-digit floor + email cap + named entry points); nothing remains before the live run
type: session
date: 2026-07-08
status: complete
permalink: a-plus-maxing/sessions/session-121
---

# Session 121 — de-id boundary finalized (merged)

## What landed
Operator directive: *"finish everything so there is nothing remaining before the live run."* So I closed the de-id-boundary items teed up at the S120 close, via PR #318 (merged `main` `ca4778fa`):

- **`6hts` bare-digit `>=9`-floor** (operator-signed-off): a `digitrun-long` = `(?<!\d)\d{9,}(?!\d)` class catching a phone/MRN/no-separator-SSN/account typed as ONE contiguous number that the separator-anchored patterns miss. OPT-IN (the `digitrun-` prefix routes it into a gated group), so it applies only at the free-text operator-value boundaries, never the frozen engine. `>=9` is the MINIMUM safe floor: legit per-entry metrics run up to 8 digits (a lifetime step count reaches 8 digits within a few years), so `>=9` clears the metric ceiling while catching the 9-digit SSN.
- **`i95h` / SEC-DEID-05 email bound**: local-part bounded to RFC-64 + domain to 255, fixing the O(n^2) backtracking on a long no-@ blob in the uncapped `scan_text_full` (1066ms→7ms at 20k chars, 149x); no recall loss.
- **`ul41` / contracts-2 named entry points**: `scan_operator_value` (base + DOB + digit-run ON) / `scan_public_content` (base only), replacing the raw `include_dob` boolean at the call sites so a caller cannot silently land on the wrong side of the split (the contracts-1 class). Migrated the 5 callers; the frozen engine + structured-token scans stay on the low-level default.

## Review
The FULL 6-agent `/review-pr` found **zero behavioral bugs** (Security/Bug-Hunter/Contracts/Historical all PASS — recall, frozen-caller safety, email-bound, migration completeness verified by execution). Its highest-value finding was Test-Coverage's **TC-318-01**: the digit-run WIRING at the 3 operator-value boundaries was untested end-to-end (mutation-proven — reverting the opt-in left the suite green, because the one existing router phone row is SEPARATED, not a bare run). Fixed with a bare-digit-run row on the router 8j6 test + capture/care_review wiring pins, blind-verified RED-capable. The rest were doc-accuracy (the "<=7 digits" flood comment — a lifetime step count is 8-9 digits, so the `>=9` VALUE is correct but the justification was wrong; stale docstrings; a per-class public-content gap).

## Process failure
**PF-S121-01** (AP-SHARED-CHECKOUT-MUTATION-RACE): the review's mutation-testing lenses transiently dirtied the shared main checkout (Contracts saw `capture.py` reverted, Historical saw the pattern as `\d{6,}`, Test-Coverage hit a stale `.pyc`). No harm — caught by verify-tree-clean + clear-bytecode before every fix commit. A recurrence of the shared-checkout-corruption class ([[2026-07-08-edit-frozen-plan-step-for-dob-gate]] is unrelated; the class bead is `fbyr`, git-reset mechanism) via a new mechanism. Guard: isolate mutation agents OR verify-clean+clear-bytecode before every review-fix commit (bead `1u5m`).

## State
The crown-jewel de-id boundary is FULLY FINALIZED. **Nothing remains before the operator-present LIVE run** — the ONLY remaining step is the run itself (real key + real data + real spend + operator presence, operator-gated), with `stsq` (observe 0-raw-PII to a real agent) as its own acceptance gate DURING the run.

## Related
- [[session-120]] (the DOB-opt-in hardening this builds on).
