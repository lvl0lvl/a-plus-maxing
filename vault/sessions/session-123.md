---
title: Session 123 — pkty (PF-S122-01) test-fidelity remediation; the model's realistic list shape driven through the real de-id consumers, merged
type: session
date: 2026-07-09
status: complete
permalink: a-plus-maxing/sessions/session-123
---

# Session 123 — model-boundary test fidelity (merged)

## What landed
Resumed the operator-authorized continuous autonomous build→review→merge→close loop (opened via "open the session") on bead `pkty` — the freshest, cleanly-autonomous, test-only item from the S122 first live run. The S122 live run's lesson (AP-MOCK-SHAPE-TAUTOLOGY): the plan-path tests fixtured the de-id summary STRING-shaped (the deterministic `router.summarize` form), so the no-train MODEL's LIST-valued output (the 940o crash class) was invisible until live. `pkty` is the general remediation: at any model-output boundary, at least one test must drive the model's realistic list/dict shape through the REAL consumer.

## The two tests (PR #322)
The S122 pin already covered the private `assemble._prohibited_classes` helper + `router.rx_interaction_class_set` (via `test_intake_aggregate.py`). This PR filled the two gaps that pin left, at the de-id summary boundary:
1. **`test_deid_in.py`** — the `deid_in` boundary passes a list-valued in-set field through UNCHANGED (it whitelists field names + PII-scans `str(value)` but does NOT coerce value SHAPE). Characterizes the no-coercion contract + is the red-to-flip for the frozen-boundary scalar enforcement (bead `s923`).
2. **`test_assemble.py`** — the REAL full `assemble()` composer (the `generate_plan:372` consumer, not the private helper) RAISES on the raw model list + composes cleanly when `normalize_summary`-coerced (the `AggregatingDeidClient` production wrap). Both arms RED-capable.

## The probe that refuted the hypothesis (run-don't-reason, F-011)
The initial hypothesis was that `run_orchestrated` (the cadence/model-de-id path) reaches the `assemble._prohibited_classes` crash. An executed probe REFUTED it: a list-valued `hard-limits` flows through `run_orchestrated` without crashing — it never calls `assemble` (`assemble(` has exactly one caller, `generate_plan:372`, which derives its summary from the deterministic `router.summarize`). So NO false/tautological test was placed there; the audit finding was documented instead. This is the "verification means running the production path" discipline catching a wrong assumption before it became a bad test.

## Review
PR #322 went through the FULL 6-agent `/review-pr` (roster-select `full-6`, widen-never-narrow): 5 lenses 0-findings; Test-Coverage returned 2 Suggestions (neither blocks the gate). Blind triage (profile-less, executed the deciding repros): **TEST-01** (Arm-2's existence-only `assert plan["sections"]`) LEGITIMATE + in-scope → fixed (assert the normalized VALUE flows into the composed section's `personalization["hard-limits"]`, not mere existence; + `match="has no attribute 'lower'"` pins the specific 940o crash) + blind-verified RESOLVED (reversion probe: RED on a broken-but-non-crashing normalize). **TEST-02** (the AUTHOR-output boundary carries the same 940o list/dict crash class, UNPROTECTED in production — `AggregatingDeidClient` normalizes `deidentify` only, not `author`) OUT_OF_SCOPE + crash_is_real → beaded `mk0i` (the author-side analogue of `s923`). Phase-8 verdict CLEAN. Merged `037f6bc9` (REST — GraphQL throttled).

## Crown-jewel + invariants
Net HARDENING: the model's realistic list shape is now driven through the REAL de-id consumers, so the next model-output shape change (or a new unwrapped supplier) is caught at test time, not live. Frozen ADR-0032 spine numstat=0 (tests-only). INV-CORE-CAPABILITY held (the new arms drive the real author→assemble path). 0 spend, 0 real PII.

## What the review taught (beaded, not fixed here)
The 6-agent completeness-critic caught what my PR's own audit missed: the **author-output boundary** has the identical 940o crash class AND lacks the normalize protection the de-id side has — a real latent production crash gated behind a model emitting a list-valued rec field. That's `mk0i` (P2), the author-side of the same class `s923` closes for the de-id side. The review working exactly as designed.

## Next
Remaining, all deferred/operator-gated: `mk0i` (author-boundary hardening — test pin + the production normalize/validate decision, s923-family, Architect); `s923` (frozen-`deid_in` scalar enforcement, Architect); `c34r` (active-issue → hard-limit safety-design, operator); the other 3 plan domains (nutrition/supplements/peptides); `stsq`/`r3vw` (operator-gated live runs). The crown jewel + core capability stay LIVE-PROVEN (S122).

## Related
- [[session-122]] (the first live run whose 940o lesson this session's `pkty` remediation generalizes).
