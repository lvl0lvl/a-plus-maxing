---
title: Session 125 — the last mk0i residuals closed (99y4 category canonicalization + ec4e single model boundary); live run fully unblocked
type: session
date: 2026-07-09
status: complete
permalink: a-plus-maxing/sessions/session-125
---

# Session 125 — mk0i residuals closed (merged)

## What landed
Operator-directed "fix the last beads please." Closed the 2 residuals the S124 mk0i review beaded, so nothing is left before the operator-present LIVE run.

- **99y4 (the SEC-01 plural/synonym category fail-open):** `_canonical_category` canonicalizes a scalar rec category to the frozen composer's prohibited-class token, so a plural/synonym/spaced form ("stimulants", "CNS stimulant", "overhead pressing") still hits the exact `category in prohibited_classes` set (fail-closed strike) instead of shipping actionable. Uses a curated **word-level** match against a **subset** of the frozen phrase→class map.
- **ec4e (the durable single model boundary):** `normalize_author_output` is now applied inside `ModelClient.author` — the single metered-model author boundary — so every consumer (the `/generate-plan` front door via `compute_plan`, any future ModelClient.author caller) is structurally covered, not seam-by-seam. The PF-S124-01 lesson realized structurally.

## The review earned its keep (again) — the over-match
My first 99y4 cut used naive **substring** containment (`phrase in norm`). The 6-agent `/review-pr` — all PASS/Suggestions (0 Critical/Important) — had **three convergent lenses** (Security SEC-01 + Bug-Hunter BUG-01 + Test-Coverage TEST-01) catch that this over-strikes **benign fitness recs on the operator's own domain**: "bench pressing" / "leg pressing" (a bench press is NOT overhead pressing), "compressing", "appetite-suppressing", "breakfasting" all struck under a matching limit — a legit rec silently dropped + a false `contradiction_disposition`. Security proved it is **fail-SAFE** (0 fail-open across 85 category×limit pairs — an over-strike, never a leak). I had **flagged the over-match class to the reviewers proactively** (the enumerate-before-review discipline, PF-S124-01's own guard), so the review confirmed + sharpened it. Fixed by dropping the ambiguous "pressing" phrase (keep "overhead" as the marker) + WORD-level matching — verified by reversion probe (old substring over-strikes; new word-level doesn't; real prohibited categories still strike). Doc/coverage findings (QUAL-01/02 normalize-locus + import WHY, API-02 fasting coverage + structural note, HIST-01 mirror-debt) reconciled; the model→serve layering relocation beaded `ywgr` (P3, Architect). Phase-8 CLEAN → merged `1d652586`.

## No new PF
The over-match was a fail-safe trade-off I flagged to the review (guard applied); the review working as designed. One INV-ROLE-INLINING self-catch (a QA dispatch over-condensed → the hook blocked it → re-inlined the full profile — the mechanical guard working).

## Live-run readiness
The crown-jewel de-id + the author path are now fail-CLOSED on real/adversarial model output, with fewer benign false-strikes. Frozen ADR-0032 spine numstat=0; pytest 2483 passed / 2 env-floor. **The operator-present LIVE run (real spend, real data, operator present) is the ONLY remaining operator-gated step.**

## Next
The LIVE run (operator-gated). Remaining beaded/gated: `ywgr` (normalizer relocation, P3, Architect), `c34r` (active-issue → hard-limit safety-design, operator), `s923` (de-id-side boundary enforcement, Architect), the others unchanged.

## Related
- [[session-124]] (the mk0i fix + review that beaded these 2 residuals).
