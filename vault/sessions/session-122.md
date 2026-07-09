---
title: Session 122 — the FIRST operator-present LIVE run; crown-jewel proven on real data, de-id payload optimized 30x, a real plan recorded
type: session
date: 2026-07-09
status: complete
permalink: a-plus-maxing/sessions/session-122
---

# Session 122 — the first live plan-generation run (merged)

## What landed
The operator authorized the operator-present LIVE run ("let's do the live walk through" → "optimize the de-id payload first, then run it" → "proceed"). I ran it bounded — verify setup → a bounded de-id call proving the crown jewel → the full path — and it did exactly what a first live run is for.

## The crown jewel — PROVEN on real data
A real Opus de-id call over the operator's actual intake (DOB present, 12K+ operator-PII-class hits including the raw DOB) produced a de-identified summary with **0 raw PII**, DOB → `training-age-band`, all whitelist-keyed class tokens. The de-id boundary strips the operator's real PII before anything downstream. The whole S120/S121 hardening (DOB/SSN/postal/bare-digit recall + opt-in default) held on live data.

## The de-id payload optimization (30x)
The production model-de-id sends the FULL raw intake to Opus — on real data ~131K tokens, ~30x of it raw wearable timeseries (1974 RHR / 1922 HRV / ... points the model would crunch into a trend). `AggregatingDeidClient` (`scripts/serve/intake_aggregate.py`) collapses each high-cardinality numeric stream to compact per-stream stats BEFORE the metered call: **131K → 4.4K tokens (~$2 → ~$0.07)**, biomarker trend preserved (`recent-trend-direction: hrv-declining-rhr-rising`), all PII/demographic/free-text/genetics fields passed through to be de-identified. Wired into `cadence_runner.main`; the frozen ADR-0032 engine is untouched (numstat=0, the adapter is at the injectable `deid_client` seam).

## What the live run surfaced (real gaps the mocks missed)
1. **bead 940o (fixed):** the no-train MODEL emits LIST-valued SUMMARY_FIELD_SET fields; the frozen string consumers (`assemble._prohibited_classes` does `.lower()`) crash on them — an UNCAUGHT crash of the plan core. `normalize_summary` coerces the model's non-string output to the string contract (total coercion — list/dict/bool → string, per the review). The mock tests used string-shaped fixtures, so this was invisible until live (→ **PF-S122-01**, AP-MOCK-SHAPE-TAUTOLOGY).
2. **bead c34r (open):** the store hard-limits is literally `"none; none"`; the operator has `active-issue-class: shoulder-impingement` but hasn't declared overhead-press as a hard-limit. The deterministic `router.summarize` restricts only declared limits; the model INFERRED the shoulder restrictions. A safety-design decision, not a crash.
3. **bead s923 (open):** the robust fix for 940o is scalar-value enforcement AT the frozen `deid_in` boundary (so any de-id supplier is safe, wrapped or not) — needs an Architect ruling.

## The plan — RECORDED end-to-end
Dispatched the `personal-trainer` specialist (full profile inlined) over the clean summary → 7 exercises honoring the constraints (no overhead pressing, no pull-ups for the shoulder; autoregulated for the reduced-recovery signal; load held pending UNKNOWN clearance). Through assemble's 4 safety filters (7/7 survived) → recorded to `plan::workout`, **0 raw PII**. The core capability — a followable plan from real data — runs live.

## Review
PR #320 (the adapter) went through the FULL 6-agent `/review-pr`: **zero behavioral bugs** (Security/Contracts PASS), Bug-Hunter+Contracts converged on the dict/bool total-coercion gap, Test-Coverage+Historical converged on the tautological 940o test (fixed with a real-consumer integration test through `assemble._prohibited_classes`). Blind-verified (reversion probes RED-capable, frozen INTACT). Merged `24d93f73`.

## Next
The crown jewel + core capability are LIVE-PROVEN. Remaining, all deferred/operator-gated: the other 3 plan domains (nutrition/supplements/peptides — same machinery); the `c34r` safety-design decision; the `s923` boundary enforcement; `pkty` (model-boundary test realism); `stsq` (the live 0-raw-PII gate, now substantially demonstrated); the ADR-0039 runner live-enable (`r3vw`).

## Related
- [[session-121]] (the de-id boundary finalization this live-run validated).
