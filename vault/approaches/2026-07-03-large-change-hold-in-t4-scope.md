---
name: large-change-hold-in-t4-scope
type: approach
status: abandoned
session: S105
date: 2026-07-03
supersedes: none
tags:
- plan-loop
- large-change-confirm
- frozen-spine
- adr-0036-t4
permalink: a-plus-maxing/approaches/2026-07-03-large-change-hold-in-t4-scope
---

# Holding the standing plan pending operator confirmation within ADR-0036-T4's scope

**What was tried:** ADR-0036-T4 AC-2 asked the large-change confirmation gate to "hold the standing plan pending until the operator confirms" — implemented as a post-promote block in `plan_loop.regenerate` that flags a large change (>= a threshold of domains differing from the prior standing plan).

**Why abandoned:** A genuine hold is STRUCTURALLY IMPOSSIBLE within T4's constraints (Architect binding ruling, feature/dyn-loop-w4). `run_orchestrated` unconditionally persists the new plan via `record_plan` BEFORE the post-promote magnitude check runs; the dashboard resolves the "standing plan" as the latest-dated plan (`resolve_plan`), so the swap has ALREADY happened at the store layer — `confirm_large_change` persists nothing and rolls nothing back. Holding requires touching one of three locked constraints: the write lives inside the ADR-0032 BYTE-FROZEN `orchestrate`; a pending-state marker needs a new store stream (AC-6 forbids it); a resolver change is outside T4's manifest. Every option hits at least one. The tautological test masked it (asserted the receipt FLAG, not the store placement — the project's own "assert placement not existence" mandate). Shipped instead as an HONEST ADVISORY (flags + names the changed domains + rationale, no hold claim).

**What would change the verdict:** The genuine hold (ADR-0036-T4b, beaded `yvrs`) needs EITHER a pre-record gate hook in the frozen spine (ADR-0032 coordination) OR a bounded confirmation-pointer the standing-plan resolver honors (amend ADR-0038's no-new-stream rule) — both are one-way-door cross-boundary decisions requiring their own ADR, not a T4-clean edit. Hard AC for T4b: the hold must ALSO gate the tailoring seam, or it re-introduces a swap-then-render leak.

**Cross-references:**
- Architect ruling (feature/dyn-loop-w4); ADR-0036-T4 recipe `[AMENDED 2026-07-03]`
- bead `yvrs` (ADR-0036-T4b — genuine hold-until-confirm, OQ-4 hold half)
- PR #280 (wave-4: honest advisory gate)