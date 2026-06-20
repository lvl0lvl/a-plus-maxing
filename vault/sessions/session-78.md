---
title: Session 78 — closed-loop measure leg + adjust read-back
type: session
status: complete
created: 2026-06-19
last_reviewed: 2026-06-19
permalink: a-plus-maxing/sessions/session-78
---

# Session 78 (2026-06-19)

## Goal

Wire the closed loop's **measure leg + adjust read-back** (`design/vision.md`: plan → act → measure → adjust). A production caller for `record_plan_tracking` (the operator logs what they actually did against a plan — the no-production-caller PF-S63-02 gap) + a plan-vs-actual `resolve_plan_progress` join (the "feeds back into the next plan" read side). The domain-specific **progression algorithm** (specialist-reasoning) + the **SBAR render** (design-led) were explicitly deferred — not invented solo. Operator delegated S78 autonomously ("open S78 and proceed"); the measure leg + read-back is the autonomous-buildable half (the other two need design/operator input).

## What was built

- **`scripts/plan/track.py` (NEW) — the measure leg + adjust read-back.** `record_tracking(domain, tracking, on_date, root)` is the production caller for `plan_schema.record_plan_tracking` — validates the domain is tracked, records one operator-OBSERVED tracking snapshot ONLY when a plan is dated `on_date` (the honest same-date no-plan-to-track boundary), returns a result record. `resolve_plan_progress(domain, on_date, root)` joins the plan + tracking into the plan-vs-actual view (`{plan, tracking, has_plan, has_tracking, specialist, plan_date}`) the deferred re-plan + dashboard read. Writes the EXISTING `plan-track::` via `record_plan_tracking` (no new store key) + reads `plan::`/`plan-track::`. `plan_schema`/`orchestrate`/`generate_plan`/`adjudicate`/`router` UNCHANGED.
- **Tracking is operator-OBSERVED, not specialist-authored** — so there is NO agent dispatch in this flow (a manufactured dispatch would be a fake). The integration is verified by the closed-loop E2E through the real `generate_plan` production path: `generate_plan` → `record_tracking` → `resolve_plan_progress`.
- **Store-surface battery** (cross-stream isolation, dedupe, mutation) on the new write/read surface; `track.py` adds no new store key (reuses `plan_schema`'s keying), so the category-4 keying mutation is the cross-stream + dedupe tests (RED under domain-collapse / constant-source). No S41-class regression (Tier-3 historical-context confirmed).

## Review (three-tier)

- **Tier-1:** suite 1083/3, floor 15/0, core-cap green; the gate, the join, the cross-stream isolation all mutation-proven RED. Contract-grounding RUN up-front (PF-S77-01): read the actual return shapes of `read_plan`/`resolve_tracking`/`record_plan_tracking` before writing track.py.
- **Tier-2:** plan-integrity (full profile) — contract-grounding CLEAN (no S77-class field-off-wrong-return) but caught the **NO_PLAN_TODAY semantic seam**: the gate keyed on `state==NO_PLAN` only, so a plan on file but not for `on_date` fell through (more permissive than the scope contract's own same-date exclusion) → fixed to `state is None` for both the gate + `has_plan`, mutation-proven. QA (Run-It owner, full profile) — store-battery PASS + NO_PLAN_TODAY/precedence/append-order coverage.
- **Tier-3 `/review-pr` (6-agent, local diff):** security + bug-hunter **CLEAN** (no safety/security defect). Test-framing + contract-consistency findings: TEST-1 (the category-4 mutation test was mis-framed — monkeypatched a phantom plan + asserted RECORDED, passing with/without the gate → rewrote self-contained, RED on gate removal) + HIST (category-4 keying attribution → documented) + CONTRACTS-TRACK-1 (`plan_date` diverged across the two functions → aligned to "the plan FOR on_date or None", mutation-proven) + QUAL-1 (Raises docstring overstated → qualified) + TEST-2/3 (NO_PLAN_TODAY precedence + read-side asymmetry coverage). CONTRACTS-TRACK-2 NOT_ACTIONABLE; QUAL-2 DECISION. Blind-verified all RESOLVED (executed).

## Process failure

**PF-S78-01** — the no-plan gate branched on only 1 of `read_plan`'s 3 `state` values (NO_PLAN), letting NO_PLAN_TODAY fall through → recorded tracking with a stale `plan_date` + a `has_plan=True/plan=None` contradiction, MORE PERMISSIVE than my own scope contract's same-date exclusion. Tier-2 caught it (gate-caught, low blast radius — no production consumer yet). Recurrence 5 of `AP-SELF-REVIEW-UNDER-PROBES-INTERACTION-SURFACE` (S74 routing-key types; S75 multi-concern holds; S76 list-field × scan-cap; S77 read a field off an outcome that didn't carry it). The `uerm` contract-grounding (PF-S77-01) HELD for field EXISTENCE — but grounding existence is not grounding the VALUE DOMAIN. Structural sharpening beaded `cjgg`: when new code reads + BRANCHES on a field off an existing return, enumerate the field's full value domain (every enum state) + decide each, AND check the branching against the scope contract's own exclusions, before Tier-2/3. Captured 3-layer (PF log + `harvest.jsonl` + `cjgg`).

## Outcome

PR #176 → `main` (rebase merge). All 6 ACs PASS. The closed loop's measure→read-back is wired: the system records what actually happened against a plan + reads it back as plan-vs-actual (the vision's "closes the loop"). The close gate was re-run on the final post-merge `main` (the PF-S74-01 discipline). Beads: `cjgg` created. The remaining surfaces are the design-led SBAR render (S79, Pencil-first) + the specialist-reasoning progression algorithm (a real-dispatch session).
