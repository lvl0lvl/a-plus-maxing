---
name: per-domain-adjust-for-automated-loop
type: approach
status: abandoned
session: S105
date: 2026-07-03
supersedes: none
tags:
- plan-loop
- adjust
- crown-jewel
- safety
permalink: a-plus-maxing/approaches/2026-07-03-per-domain-adjust-for-automated-loop-1
---

# Automating `adjust.py` (per-domain re-author) as the dynamic-plan-loop's re-adjustment path

**What was tried:** The v1 design of the dynamic-plan-loop had the automated re-adjustment fire the existing per-domain `scripts/plan/adjust.py` (which re-authors a single domain's plan from the plan-vs-actual progress via `generate_plan`) on each trigger — reusing the already-built "adjust" leg rather than re-running full generation.

**Why abandoned:** The 6-agent design review + the wave-1 grounding confirmed `adjust.py` records via the SINGLE-domain `generate_plan` path, which runs only `assemble`'s per-domain filters + the clearance gate + the domain veto — it NEVER re-enters `plan_driver.drive` / `gate_dispatch` (the ADR-0023 judge + ADR-0024 safety lenses + ADR-0028 fail-closed composition + the medical-liaison adjudication) NOR the five cross-domain reconciler holds (energy-bounce / additive-AE / conflict / Rx-BPMH / RED-S) that live only in `orchestrate.generate_plans`. `adjust.py`'s own docstring documents this as a deliberate V1 boundary for a RARE, operator-invoked one-off. AUTOMATING it makes it the PRIMARY way plans evolve, so the operator's plan after week 1 would NEVER again pass the safety composition — a progressive erosion of the crown-jewel gate every ADR-0022/23/24/26/28 was built to guarantee. Four independent reviewers flagged this; the Architect confirmed it is a safety regression, not a cost trade-off.

**What would change the verdict:** Never for the AUTOMATED loop — a recurring loop MUST re-enter the full-composition front door (`run_orchestrated` → `plan_driver.drive`), which is what ADR-0036 shipped. `adjust.py` remains valid ONLY as the manual, operator-invoked single-domain one-off it was built for.

**Cross-references:**
- ADR-0036 (Decision: the loop re-runs the front door), docs/adr/ADR-0036-automated-plan-evolution-loop.md
- design/dynamic-plan-loop-design.md §0 finding A
- PR #277 (wave-1 anti-degradation guard: 0 `adjust.py` on the loop path)