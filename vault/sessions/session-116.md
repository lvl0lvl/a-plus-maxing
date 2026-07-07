---
title: Session 116 — 2deg frozen-spine vacuity guard repoint (merged); floor 3→2 reds
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-116
---

# Session 116 — pin the frozen-spine vacuity guard to PRE_TASK_HEAD (2deg, merged)

Passed THROUGH the S115 close into `2deg` — a stale-test cleanup that removes a permanent floor red. Merged (PR #308, `9cc08d70`): the suite floor drops from 3 reds to 2, sharpening every future close's "no new failure" gate.

## What was fixed
`tests/serve/test_plan_loop_hold.py::test_frozen_spine_and_only_regenerate_changed` asserts the ADR-0040-changed defs (`regenerate`, `_change_magnitude`, `_post_promote_tailoring`) DID change vs a baseline (the non-vacuity "the fix is applied" guard). It compared vs **origin/main** — which worked while the ADR-0040 build sat unmerged, but once ADR-0040 merged, origin/main caught up to the changed defs, so `current != origin` read empty and the guard self-invalidated (a permanent RED, the 3rd floor failure alongside the 2 env/port-sensitive ones).

Fix (`552b2170`): repoint the vacuity guard at a **fixed** `PRE_TASK_HEAD = 300de2f` (the parent of the first ADR-0040-hold `plan_loop.py` commit — the pre-hold state where the 3 defs exist in their pre-ADR-0040 form), mirroring `test_generate_plan.py`'s established PRE_TASK_HEAD pattern. The changed defs differ from that fixed baseline permanently, so the guard stays non-vacuous forever. The freeze checks (numstat=0 + per-def byte-unchanged) stay vs origin/main — only the vacuity guard's baseline moved.

## Review + verification
TEST-only edit — the frozen ADR-0032 spine + `plan_loop.py` stayed byte-frozen (numstat=0). Non-vacuity proven by execution: the 3 changed defs differ from PRE_TASK_HEAD (True) while 3 unchanged helpers (`_last_regen_date`, `_prior_standing_plan`, `_should_regenerate`) are byte-EQUAL to it (True) — so the `!=` guard genuinely discriminates, not trivially-true; and its mutation-sensitivity is proven by the original bug (the guard RED'd precisely when the baseline == current). Full suite floor now `2 failed, 2380 passed, 7 skipped`.

**Review-path disclosure:** for this single-file test-cleanup (no behavior/security surface, frozen spine untouched) I ran a rigorous EXECUTED direct review rather than the full 6-agent `/review-pr`, per the skill's OWN "single-file → review directly; the 6-agent pipeline is overkill" negative-example. Disclosed here + in `memory/process-failures.md` `## Session 116` for operator adjudication, given the prior-session `/review-pr`-substitution sensitivity (the more-conservative full `/review-pr` was available). No new PF.

## Run status
This run completed a coherent hardening set — aque (OAuth secret scan) + SEC-01 (no-train-API-key secret scan), hgnt/zsre (confirm-TOCTOU + held-plan render-filter), 2deg (floor red) — all merged. The highest-value REMAINING steps are operator-gated (the LIVE core-plan run, the ADR-0040 OQ-5 live wiring's real spend, the ADR-0039 runner activation, the DNA research); the remaining autonomous items are lower-value (`krny` N=4, the PF-family/P3 beads).

Full detail: `memory/process-failures.md#session-116` + HANDOFF `## Scope Contract — Session 116`.
