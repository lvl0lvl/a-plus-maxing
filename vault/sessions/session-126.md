---
title: Session 126 — the operator-present LIVE 4-domain plan run; crown jewel proven
  on real data, all 4 plans recorded, 2 surfaced blockers fixed + merged
type: session
date: 2026-07-10
status: complete
permalink: a-plus-maxing/sessions/session-126-1
---

# Session 126 — the first full 4-domain LIVE plan run (merged)

## What landed
Operator-directed "run it" — the operator-present LIVE plan-generation walkthrough on the operator's real `vault/store` data. S122 proved the crown jewel + one workout plan; S126 ran the **full 4 domains** end-to-end.

## The crown jewel — PROVEN on real data (again, richer)
A metered Opus de-id over the operator's actual intake (6263 readings; 131K → 4.4K tokens after the `AggregatingDeidClient` 29.6x timeseries collapse) produced an 18-field de-identified summary with **0 raw PII** — key-whitelist ⊆ SUMMARY_FIELD_SET, per-value `pii_scan` clean, an independent raw-DOB-pattern scan clean. The model inferred the shoulder restrictions (`hard-limits: no-overhead-press; no-pull-ups`, `active-issue: shoulder-impingement`) the deterministic path leaves as `none` — the c34r nuance, live.

## All 4 domains authored + RECORDED (0 raw PII)
- **workout** → Landmine Press (the Strength-Coach chose it *instead of* overhead press — honored the inferred shoulder restriction), no load (clearance-gated until the MD visit).
- **nutrition** → 2200 kcal, 190P/175C/75F, paleo meals (matched the dietary class).
- **supplements** → creatine, D3+K2, L-methylfolate (MTHFR), melatonin (delayed-melatonin trait), omega-3, CoQ10 note — each grounded in the operator's genetic classes.
- **peptides** → BPC-157 for the shoulder, with an honest "rodent models only; physician supervision" caveat.
Every authored payload + every recorded plan independently PII-scanned CLEAN.

## The two blockers the live run surfaced (both fixed + merged, PR #328)
1. **LIVE-01:** the structured-output API 400s on integer `minimum`/`maximum` ("For 'integer' type, properties maximum, minimum are not supported") → workout/nutrition author calls failed. The bounds were soft hints only (real bounds enforced downstream in `record_plan`/`plan_schema`); dropped them, kept string `minLength`.
2. **LIVE-02:** the operator's literal `hard-limits: 'none; none'` is non-empty but maps to no prohibited class, so the frozen HALT filter (`assemble._halt_disposition`) reads it as an unrecognized limit → HALT_INDETERMINATE → strikes EVERY rec → no plan. `_normalize_hard_limits` (new, `router.py`) collapses the confirmed-none sentinel to `''` so the filter clears; real + unrecognized limits preserved verbatim (the guard is unchanged — verified: `no stimulants` still strikes, `no xyz` still fails closed).

## The review earned its keep — a real convergent cluster
PR #328 through the FULL 6-agent `/review-pr` (roster full-6, verdict CLEAN). It converged on:
- **SEC-02 / API-01 / QUAL-02** (Security + Contracts + Code-Quality): my `_normalize_hard_limits` split the raw-case value on a lowercase-literal `' and '` while the frozen `_limit_clauses` lowercases first — so `'none AND none'` was NOT collapsed (fails closed, but the fix was incomplete). Fixed: case-insensitive split.
- **API-03** (Contracts, the important one): `deid_in` is a SECOND producer of the same summary feeding the frozen HALT filter (the run_orchestrated loop path), left unnormalized — the identical bug would recur there. **This is the PF-S124-01 single-seam/all-ingress lesson** — the review caught the sibling producer I missed. Fixed: applied the shared `_normalize_hard_limits` at the de-id adapter too → **PF-S126-01** promoted.
- **QUAL-01 / HIST-03**: `_HARD_LIMIT_SENTINELS` added a 5th token `'nil'` diverging from the sibling derivers + its own comment. Fixed: dropped `'nil'` to match.
- **BUG-01 / HIST-01 = bead `rxe9`** (Bug-Hunter + Historical): LIVE-01 makes reachable a pre-existing FROZEN `record_plan` uncaught-ValueError on a value-invalid author output (e.g. `sets:0`) — deferred to the existing open frozen-side bead.
All fixed at non-frozen seams + blind-verified RESOLVED (both add-a-guard fixes reversion-proven load-bearing). Frozen ADR-0032 spine numstat=0; pytest 2491 passed / 7 skipped. Phase-8 CLEAN (`8adf120b`) → MERGED (PR #328 → `main` `4990400f`).

## PF-S126-01
Promoted (recurrence_count 3 of the single-seam/all-ingress class): I fixed the `router.summarize` producer of the frozen HALT input but missed the `deid_in` second producer; the review's Contracts completeness-critic caught it (API-03). Guard: enumerate ALL producers of a frozen consumer's input before review, not just the one the current bug exercised.

## Beaded (not fixed this session)
- `rxe9` (open) — the frozen `record_plan` value-invalid crash LIVE-01 makes reachable (frozen-side).
- dashboard `referral::` unrouted-stream render crash (the real store has a S104 `referral::` stream the dashboard template doesn't route).
- de-id-model genetics-fidelity divergence (the model re-interprets genotypes — slow- vs fast-caffeine — vs the vetted ADR-0032 library; infers unverified conditions e.g. sleep-apnea).
- SEC-03 — quadratic `re.split` on the shared hard-limits regex (pre-existing in the frozen `_limit_clauses`).

## Next
The core capability is LIVE-PROVEN end-to-end. Remaining are the frozen-side + tangential follow-ups above (all beaded); the scheduled runner's live activation (ADR-0039) stays operator-owned.

## Related
- [[session-122]] (the FIRST live run — crown jewel + one workout plan; this session extended it to all 4 domains).
- [[session-125]] (the pre-flight residuals that unblocked this run).