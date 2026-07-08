---
title: Session 120 — de-id recall hardening (yduw/6hts/yaeh) merged; DOB class made opt-in to preserve the frozen engine
type: session
date: 2026-07-08
status: complete
permalink: a-plus-maxing/sessions/session-120
---

# Session 120 — crown-jewel de-id recall hardening (merged)

## What landed
Operator directive: *"proceed with your recommendations"* — my recommendation was to HOLD the operator-present LIVE run and first close the de-id recall gaps that would leak the operator's real DOB/address to the no-train model. Ran a FULL 6-agent `/review-pr` of PR #316 (the `yduw`/`6hts`/`yaeh` de-id recall hardening) → merged `e1ba0839`.

## The crown-jewel finding (contracts-1)
The original PR added the DOB/date value class to `pii_scan` with `include_dob=True` as the DEFAULT. Contracts (executed) found this silently changed the byte-FROZEN ADR-0032 engine's behavior: `plan_step`'s GATE scan of the DERIVED assembled plan began flagging legitimate SCHEDULE dates ("retest by 2026-09-01") → the gate fails closed → NO plan surfaces (a core-capability regression, INV-CORE-CAPABILITY). My first fix edited `plan_step.py` directly — caught immediately by the post-fix full-suite gate (the frozen-engine byte-unchanged tests RED).

**The correct fix (design decision):** make the DOB class OPT-IN (`include_dob=False` default). The frozen engine (`plan_step`, `deid_in`) keeps its pre-yduw no-DOB behavior UNCHANGED (byte-identical); only the free-text operator-value boundaries — `capture`, `router.summarize`'s 8j6 gate, `care_review` — opt in with `include_dob=True`. This closes the leak AND the regression under EXTEND-NOT-REBUILD: **a new PII class must not silently alter a byte-frozen caller** — add it opt-in and opt the specific non-frozen boundaries in.

## Recall gaps closed (flood-safe, executed by Security/Bug-Hunter, blind-verified)
- 2-digit-year DOB (`born 3/14/86` — the most common birthday form) — co-signal-anchored on a DOB cue word (0 hits on `40/30/30`, `5/3/1`, `zone 2/3/4`).
- Time-suffix ISO DOB (`1986-03-14 08:00`, next-line `\n08:00`) — the `[T\s]`→`T` store-exclusion narrowing (store timepoints stay scoped out; the date-picker `T00:00:00` is a documented residual).
- Non-padded dash year-first (`1986-3-14`) — `[/.]`→`[/.-]` + the T-guard so store timepoints stay off.
- Unicode en/em-dash DOB — dash-fold before matching.
Every hardening guard proven load-bearing by a blind reversion probe (removed in-memory → RED).

## Pipeline
6-agent `/review-pr` (all FULL profiles inlined) → synthesis (16 findings) → blind profile-less executed triage → SE fixes → blind executed verification (7/7 RESOLVED, reversion probes RED, FROZEN SPINE INTACT) → Phase-8 CLEAN verdict → merged.

## Beads
- Closed: `yduw` (DOB detector + summarize 8j6 opt-in), `yaeh` (pass-through-field DOB probe).
- Updated: `6hts` — SSN + two-line postal DONE; scoped to the operator-gated bare-digit `>=10`-floor residual (SEC-DEID-03, non-blocking for the live run).
- Created: `contracts-2` (named `scan_public_content`/`scan_operator_value` entry points), the `scan_text_full` O(n^2) email cap (SEC-DEID-05, pre-existing).

## Next
The de-id boundary is watertight for the LIVE run. The ONLY remaining step is the operator-present LIVE run (real key + real data + spend, operator-gated). Plus the operator's call on the bare-digit `>=10` floor (`6hts`).

## Related
- [[session-119]] · the abandoned direct-edit approach: [[2026-07-08-edit-frozen-plan-step-for-dob-gate]]
