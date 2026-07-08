---
title: Session 119 — 23q5 native toolkit-floor exclusion (merged); the rigor close-audit now passes natively
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-119
---

# Session 119 — 23q5 native toolkit-floor exclusion (merged)

## What landed
Operator directive: *"I would like the rigor framework to work and be followed. if that means you still have to do (23q5 or others) then please do so."* So I built bead **`23q5`** — the durable a-plus-side close-audit toolkit-floor exclusion — to retire the off-label `CLOSE_AUDIT_FLOORS` test-hook interim the S118 close leaned on. Merged via PR #314 → `main` `08559110`. **The mandatory close-audit now passes NATIVELY (0 violations, no off-label warning).**

- **`scripts/tests/toolkit-floor.sh`** — an a-plus twin of the vendored `toolkit/tests/run-all-tests.sh` that runs the toolkit `test-*.sh` with a loud + two-way-stale-guarded exclusion of the ONE tracked library-tree-scoped false-red (`test-roster-select.sh` / bead `ffit`; `roster-select.sh` itself works in a-plus). Never edits the vendored runner. `close-audit.sh` `DEFAULT_FLOORS` now routes the toolkit floor through it.
- **F-007 preserved:** `scripts/tests/test_toolkit_floor.sh` (9 cases) proves the floor still REDs on any un-excluded toolkit failure + both stale conditions. Reversion-probe-confirmed load-bearing.

## The FULL 6-agent /review-pr earned its keep decisively
roster-select classified the change `full-6` (rule-2, guard/governance paths); I ran the full pipeline per widen-never-narrow (a guard-affecting change to the mandatory close gate deserves it). It caught **7 findings**, including a **real design bug that 3 agents independently converged on** (Security/Bug-Hunter/Contracts/Code-Quality all flagged it, all executed):

- **The cross-fire (F1):** my wrapper over-reached by *also* honoring the shared `RUN_ALL_TESTS_EXCLUDE`. The two floors scan disjoint namespaces (toolkit `test-*.sh` vs a-plus `test_*.sh`), so forwarding one `CLOSE_AUDIT_FLOOR_EXCLUDE` value to both made each floor's stale-guard RED on the other's names — breaking the escape hatch (proven end-to-end: `close-audit --session 999` → 2 violations).
- **Fix:** the wrapper no longer reads the shared var (uses only its own seeded `DEFAULT_EXCLUDE`), and BOTH floors' stale-guards are namespace-scoped (each only stale-checks names matching its own glob). Plus: hermetic negative test (F2), env-isolation + namespace test cases (F3), the wrapper's test-hook vars added to close-audit's SEC-002 warning (F4), and header/S65/floor-comment reconciliations (F5/F6/F7). F8 (cosmetic double-count) triaged NOT_A_BUG.
- Blind-triaged (executed the deciding repros) + blind-verified (executed + a **reversion probe** proving the namespace guard is load-bearing). Phase-8 CLEAN (`ff075eba`).

The build's own self-verification (the F-007 test) had covered the `DEFAULT_EXCLUDE` path but not the shared-env cross-fire — the full-review gate is exactly the net for what self-verification misses. This is the layered review process working as designed, not a process failure (no new PF; disclosure ledger in `## Session 119`).

## State
The rigor framework is now followed with **no off-label workaround** — the close-audit passes natively. When the upstream `ffit` fix lands + a-plus re-pulls, `roster-select` passes, the wrapper's stale-guard (b) forces the seeded exclusion's removal (it cannot rot silently). Frozen ADR-0032 spine untouched; 0 live spend. Full detail: `memory/process-failures.md` `## Session 119` + HANDOFF `## Scope Contract — Session 119`.
