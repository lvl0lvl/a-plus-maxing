---
title: Session 142
type: session
created: 2026-07-17
permalink: a-plus-maxing/sessions/session-142
---

# Session 142 (2026-07-17) — Credential-onboarding Wave 4 (OAuth callback + spend cap); Wave-5 spec-defect HALT

## Goal
Build **Wave 4** of the credential-onboarding code build via `/run-pipeline` — ADR-0048-T2 (app-mediated OAuth-2.0 callback + D7 crown-jewel wire-scan) + ADR-0049-T3 (per-tester monthly spend cap), file-disjoint — then the Wave-4→5 checkpoint, then **Wave 5** (ADR-0048-T4 onboarding UI), driving continuously without stopping at boundaries. Opened mid-run after the S141 close under the standing run-until-everything directive (no separate S142-open).

## What happened
- **ADR-0048-T2 → merged #362** (`a261171b`, pre-compaction): the localhost PKCE OAuth callback + the D7 egress wire-scan. The load-bearing event: an SE HALT on a spec/frozen-invariant conflict (the `scripts/serve/` layer is egress-free by ADR-0001, but the OAuth code→token exchange needs egress). Resolved on the **operator's Option-B sign-off** — relocate the exchange to the egress-permitted `scripts/ingest/oauth_pull.py` layer behind the fail-closed `_NoFollowRedirect` opener (guard-preserving, no drift-guard loosening). Tier-3 full-6 → merged.
- **ADR-0049-T3 → merged #363** (`9b66d2bb`): the per-tester cumulative monthly spend cap on the shared `a-plus-maxing-api-key` metered lane. The recipe cleared FOUR doc gates (3-lens: 2 BLOCKING — the `SpendCapExceeded`-must-subclass-`DispatchCapExceeded` propagation-crash + the lock-free TOCTOU fail-open — remediated; fresh-judge ACCEPT all ≥9, re-derived both fixes; adversarial-review: 4 SHOULD-FIX incl. the concurrency-falsifier determinism). SE built it (16 tests); **Tier-2 3-lens** (QA PASS, Security PASS with LOW-1 a value-corruption fail-OPEN bypass — a negative-count ledger bypassed the ceiling — FIXED + independently re-verified CLOSED, Architect APPROVE-W-A); **Tier-3 full-6** (0 Critical/High/Medium; 6 LOW: the `cap=None` LSP trap [3-agent convergent], the lock path-normalization footgun, 2 test-coverage gaps, 2 doc nits — all fixed + **Phase-7 blind-verified**, the required-cap/`.resolve`/temp-cleanup guards revert-probed RED = load-bearing). CLEAN bound to `0e2f8f35` → merged. The cap ships **default-OFF** (`spend_cap=None`); the metered loop stays unarmed (bead `23xr` carries the arming ACs).
- **Wave-4→5 checkpoint GO**: 75 checkpoint-module tests (oauth_callback + spend_cap + metered_dispatch) + the full suite 3000 passed / 8 skipped / 2 env-floor; frozen-six numstat EMPTY; all artifacts present; ledger gitignored.
- **Wave 5 (ADR-0048-T4 onboarding UI) HALTED at the recipe doc-gate** on a blocking spec-grounding defect (PF-S142-01, bead `2awb`). The recipe (authored orchestrator-direct) targeted `intake.py` as the Surface-A intake credential step, but the doc-gate 2-lens (QA + Architect) proved `intake.py` is an UNSERVED CLI-only artifact — `server.py` serves ONLY the SPA (`generate.run('app')`) at `GET /`; the live intake surface is the SPA's `screen-wizard` (`app_view.html`), and `screen-profile`'s Surface-B markup is also in `app_view.html` (absent from the manifest). Per create-task-plan HARD RULE 9, a spec defect HALTs the recipe pipeline. Recipe marked `blocked`; the spec-revision (retarget Surface A to the SPA + add `app_view.html`) + the full doc-gate recipe-defect checklist beaded (`2awb`).

## Beads (new/updated this session)
`a-plus-maxing-2awb` (P1 — the ADR-0048-T4 spec-grounding defect + PF-S142-01 + the recipe-rewrite checklist); `23xr` updated (the spend-cap arming ACs: cap-injection call site, the `:314` honest-no-plan catch, an armed-loop E2E, the concurrency AC, + the Tier-3 out-of-scope items — gate/revise-uncapped, the `dispatch_count` telemetry-overload); `y7ms` (P4 — the `.gitignore` glob for atomic-write temp siblings). Plus the ADR-0049-T3 pre-merge beads folded into `23xr`.

## PF entries
**PF-S142-01** (bead `2awb`) — recipe render-target grounding miss (authored ADR-0048-T4 targeting the unserved `intake.py`; the ground-against-the-live-tree discipline [PF-S141-02 class] applied to a render surface — verify the target is on the SERVED path, not merely that the file exists). Gate-caught (doc-gate 2-lens), self-surfaced. In `memory/process-failures.md` `## Session 142` + `harvest.jsonl` + bead `2awb`.

## State at close
main @ `9b66d2bb`. Waves 1-4 of the 6-wave credential-onboarding build COMPLETE + merged + checkpointed. Wave 5 (ADR-0048-T4) HALTED on the spec-grounding defect — resumes next session from the spec-revision (retarget Surface A to the SPA `screen-wizard`). Wave 6 (ADR-0049-T2) follows. The in-app plan loop stays honestly degraded (metered cap default-OFF) until `23xr`; the LIVE runs stay operator-gated (`m8ia`; `d1yz` first).
