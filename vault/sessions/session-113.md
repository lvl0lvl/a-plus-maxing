---
title: Session 113 — hgnt confirm-serialize (merged) + a clean 6/6 executed /review-pr
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-113
---

# Session 113 — hgnt confirm_plan_change TOCTOU serialize (merged)

Passed THROUGH the S112 close (per the never-stop-mid-loop discipline) to complete the `hgnt` cycle — the ADR-0040 OQ-5 confirm-path prerequisite. Built + merged (PR #302, `d8c646d2`): `confirm_plan_change` no longer double-fires the metered `converse` (double metered spend) under `ThreadingHTTPServer` concurrent confirms.

## What was built
- **The TOCTOU serialize fix** (`25b006a3`): a per-store-root `threading.Lock` (`_confirm_locks` registry + `_confirm_locks_guard` + `_confirm_lock_for(root)`) wraps the ENTIRE `confirm_plan_change` critical section — the `decision_for` check → `set_decision` flip → `confirmed_union` build → `_post_promote_tailoring` fire. Two concurrent same-`(domain, plan_date)` confirms now serialize (the 2nd reads the flipped pointer + short-circuits → exactly one fire, ADR-0040 T4 AC-2); concurrent cross-domain confirms serialize the union build (no clobber, AC-6b). Two deterministic Barrier/Event-forced concurrency tests, mutation-RED-proven non-vacuous.

## The /review-pr — a clean 6/6, not a rubber-stamp
The REAL Tier-3 `Skill(review-pr, 302)` ran IN FULL (roster full-6, design=no). All 6 dimensions returned PASS / 0 findings at threshold — and every one EXECUTED its load-bearing claim (F-011 run-it), which is what makes the 0 trustworthy:
- **Security + Test Coverage** each INDEPENDENTLY ran the non-vacuity mutation: neutering `_confirm_lock_for` to return a fresh unshared lock made BOTH concurrency tests go RED (same-domain fires 2×; cross-domain union clobbers) → the double-metered-spend closure is load-bearing.
- **Bug Hunter** ran a re-entrancy deadlock repro (the `threading.Lock` is non-reentrant, but no production callee of the locked section re-enters `confirm_plan_change` → self-deadlock unreachable); also cleared the registry get-or-create-under-guard atomicity, the `str(root)` key stability, and exception-release.
- **Test Coverage** ran 28 flake iterations (20/20 isolated + 8/8 under 4× CPU load, green) — the ~2s/test cost is a deterministic timeout deadline, not a race.
- **Historical Context** cited the introducing SHAs — the unlocked check-then-act was an unaddressed gap flagged MEDIUM in the ADR-0040 T4 build's own review, so this PR is its sanctioned remediation, not a reversal; `threading.Lock` (intra-process) vs the ADR-0039 runner's `fcntl.flock` (cross-process) is complementary-on-a-different-axis, not divergence.
- **Contracts** confirmed the public signature / return-shape / `ValueError` contract byte-identical + the per-root grain correctly realizes AC-2 / AC-6b.

Phases 3–7 (blind triage → fix → blind verify) were vacuous by construction (0 findings, 0 fixes); Phase-8 machine verdict CLEAN (SHA-bound `25b006a3`).

## Orchestrator gating + the orthogonal red
Before the merge I re-confirmed the 3 gating facts by hand: frozen ADR-0032 spine + `plan_loop.py` numstat=0; exactly 2 files changed; the whole-tree secret-shaped-token scan clean (the discipline the prior-session documentation-token recurrence taught, applied proactively). The full suite held at the documented 3-red floor — and the one red not in the trio's usual shape (`test_frozen_spine_and_only_regenerate_changed`) I did NOT wave through: I isolated it and PROVED it orthogonal — its frozen-spine byte-unchanged asserts all PASS; only its own `regenerate != origin/main` vacuity guard fails, because ADR-0040 has since merged to main so origin/main's `regenerate` caught up. Pre-existing merge-artifact, already beaded `2deg` (my accidental duplicate `0ade` closed).

Frozen ADR-0032 spine + `plan_loop.py` byte-frozen throughout; crown-jewel HARDENED; 0 live spend.

## Pipeline note
A clean demonstration of the layered pipeline at the other end from S112: where S112's `/review-pr` caught a Critical the build missed, S113's `/review-pr` confirmed a genuinely-clean small concurrency fix — but only because all 6 lenses EXECUTED (two independent mutation-REDs, a re-entrancy repro, 28 flake runs), not by inspection. A 0-findings review is only worth trusting when the 0 is executed.

Full detail: `memory/process-failures.md#session-113` + HANDOFF `## Scope Contract — Session 113`.
