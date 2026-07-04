---
title: Session 105 — Dynamic plan-loop feature (ADR-0036/0037/0038)
type: session
date: 2026-07-03
status: complete
permalink: a-plus-maxing/sessions/session-105
---

# Session 105 — Dynamic, personalized, time-horizon plan loop

**Goal (operator-directed, autonomous):** build the dynamic plan-tailoring loop — specialists' de-identified sections → the care agent tailors them with the operator's raw data → the plan spans daily/weekly/monthly horizons and evolves toward goals → it re-adjusts dynamically when new data arrives — through the FULL autonomous pipeline (Sequential Thinking → design → 6-agent adversarial review → ADR → Spec → Build Plan → Task Plan → Execute Plan), wave-by-wave with review → merge → close → continue.

## What was built (all merged to `main`, PRs #277–283)

- **ADR-0036 (loop):** the automated re-adjustment RE-RUNS the full-composition front door (`plan_orchestrator.run_orchestrated` → `plan_driver.drive` → `gate_dispatch`), NOT the per-domain `adjust.py` — so every evolved plan clears the same safety composition + cross-domain holds as the first. Mechanical debounce (`plan_loop.signal` / `_sustained_signal`). Module: `scripts/serve/plan_loop.py`.
- **ADR-0038 (horizons):** `scripts/plan/horizons.py` read-layer over `goal_schema`/`calendar_schema` + the ADR-0010 extras seam; deterministic on-track/behind/ahead classifier.
- **ADR-0037 (tailoring):** `scripts/plan/tailoring.py` — the care-lane pass personalizes each recorded, non-held plan with the operator's RAW care data, rendered ONLY to the gitignored maintained artifact (crown-jewel: verified artifact-only, no leak to store / de-id dashboard / specialist lane). Emit-gate keyed on the current re-gen's hold-set. Dosing-token reject (active, hardened lexicon). Load-time SUMMARY_FIELD_SET-disjointness tripwire + ADR-0001 egress carve-out amendment.

## Review rigor (the load-bearing story — PF-S105-01)

The Tier-3 adversarial bug-hunter caught a real HIGH/CRITICAL defect the SE's happy-path tests masked in EVERY deterministic wave (2–7): a cross-stream debounce false-fire, a verdict-flipping realized-rate anchor, a cosmetic large-change gate, a shadow-prescribe emit-gate, a DORMANT interaction screen (`ae_profile` dropped at `record_plan`), and a dormant tripwire test. All fixed pre-merge. Three design contradictions went to binding Architect rulings: the large-change hold re-scoped to T4b (structurally impossible in-scope); two frozen-glob carve-outs (horizons.py, tailoring.py); the interaction screen RETIRED (redundant with the primary reconciler BPMH screen).

## State + follow-ups

- Full suite on `main`: 2261 passed / 2 known env-fail (`test_bind`, `test_server`) / 7 skipped. Crown-jewel + EXTEND-NOT-REBUILD held every wave (frozen engine numstat=0).
- **Terminal step (operator-gated):** the LIVE loop run (real key + spend) + wiring the production `loop_dispatch`/`loop_deid_client` seams (`3ge1`) — the loop is inert-but-safe until then.
- Beaded: `qiob` (interaction-screen dormancy resolution), `z2mh` (re-open frozen-glob deny-by-default design, 3rd carve-out + non-hermetic frozen-test), `yvrs` (T4b genuine hold-until-confirm), `55qg` (CSRF on /chat + /care-chat), `cs58` (conversation summarization).

## Links

- [[2026-07-03-per-domain-adjust-for-automated-loop]] · [[2026-07-03-large-change-hold-in-t4-scope]] · [[2026-07-03-tailoring-lane-interaction-screen]]
- ADRs: docs/adr/ADR-0036/0037/0038; spec: docs/spec/adr-0036-0038-dynamic-plan-loop-spec.md; design: design/dynamic-plan-loop-design.md
- PF-S105-01: memory/process-failures.md `## Session 105`