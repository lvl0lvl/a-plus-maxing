---
title: Session 112 — zsre held-plan render-filter (merged) + the /review-pr Critical
  it caught
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-112
---

# Session 112 — zsre held-plan render-filter fix (merged)

Passed THROUGH the S111 close (per the never-stop-mid-loop discipline) into the next `bd ready` P1 item. Built + merged `zsre` (PR #300, `715b0d24`): a held (pending-pointer, un-confirmed) large plan re-gen no longer renders as the operator's **standing** plan on any render surface — the ADR-0040 OQ-5 render-side hard prerequisite.

## What was built
- **The render-filter fix** (`e58617d`): threaded the store `root` into 4 render paths + applied `plan_confirm.filter_confirmed(readings, domain, root)` before `resolve_plan` on `report`/`app_shell`/`dashboard`/`handout` (via `generate.run` + `maintained.reemit_maintained`). 4 render tests RED→GREEN, proven non-vacuous by counterfactual.
- **A self-inflicted regression fix** (`9aac507b`): my S111 close disclosure-ledger prose had written the verbatim `sk-ant-oat`+alnum token literal — the exact H1 time-bomb — which self-tripped the ADR-0039 T2 token scan on `main`. Caught by the zsre regression run; elided. → **PF-S112-01**: the H1 guard is a TRACKED-FILE guard, not code-only; never write a verbatim secret-shaped literal in ANY tracked file (prose included); re-run the token scan after writing close docs.
- **The /review-pr Critical fix** (`d89530c`): the real Tier-3 `/review-pr` (6 agents, all executing) CONVERGED on a 5th `_plan_zone` call site the build missed — `server.py:808` (the live `POST /generate-plan` handler) rendered held plans unfiltered (the Factory-to-Component/Call-Chain wiring class; the build's tests only drove `generate.run('app')`). Fixed (thread `store_root`) + a served-path held-plan test + blind-verified RESOLVED with the reversion probe.
- **A PF-S63-02-adjudicated guard scope-correction**: fixing `server.py` tripped an over-broad ADR-0039 guard (`test_extend_not_rebuild_no_rehost_no_serve_edit`'s whole-`scripts/serve/`-dir blanket diff). The SE HALTed (didn't default-loosen); I adjudicated a verified mis-fire (runner byte-unchanged, `plan_loop.py` frozen, `server.py` editable) + scope-corrected assertion #2 to the frozen `plan_loop.py` containment host — informed sign-off, broader tripwire beaded.

Frozen ADR-0032 spine + `plan_loop.py` byte-frozen (numstat=0) throughout; crown-jewel HARDENED; 0 live spend.

## Pipeline note
This cycle is a clean demonstration of the layered pipeline working: the P1 fix built + committed, then the REAL Tier-3 `/review-pr` (run in full, no substitution) caught a Critical the build's own tests could not — vindicating running the full pipeline on a "small" fix.

Full detail: `memory/process-failures.md#session-112` + HANDOFF `## Scope Contract — Session 112`.