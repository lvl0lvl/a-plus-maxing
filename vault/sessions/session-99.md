---
title: Session 99
type: session
created: 2026-06-27
status: complete
permalink: a-plus-maxing/sessions/session-99
---

# Session 99 (2026-06-27)

## Goal
Two-part autonomous directive: (1) land the operator-approved SPA front-end via the gated `/review-pr` → `/merge` lifecycle so real testing can begin; then (2) on the operator finding the system could not ingest a DNA report PDF ("that's a real flaw … each section [must] parse whatever format comes in"), run the FULL build pipeline to make ingestion **format-agnostic** (ADR-0030 Model-Based Universal Ingestion), then run the full automatic session close. Operator: "land it and proceed to build. Run autonomously through it, including review-pr/merge and session close. Remember the stop justification rules."

## What shipped (all merged to `main`)
- **PR #264** — the faithful SPA front-end (top-nav 3-column "Chat with Team" workspace + Profile + in-app `/settings/key` save to keychain `a-plus-maxing-api-key`). Full 6-agent `/review-pr` (9 LEGITIMATE fixed + 9/9 blind-verified) → rebase merge → `main` `dc39246`.
- **PR #265** — ADR-0013 `[AMENDED]` recording the GET/POST `/settings/key` route. Docs amendment → merge → `main` `de13723`.
- **PR #266** — the full ADR-0030 build. Pipeline: `/create-adr` (ADR-0030 accepted; the red-team correctly flagged it as a crown-jewel boundary EXTENSION → amended ADR-0001/0003/0013/0029; operator informed sign-off by accepting the ADR, PF-S63-02) → `/create-spec` (5 tasks, judged 11/11) → `/create-build-plan` (4 waves, judged 10/10) → `/create-task-plan` (5 TDD recipes) → `/execute-plan` (4 waves, per-wave EXECUTED checkpoints + Tier-2) → Tier-3 6-agent `/review-pr` → rebase merge → `main` `8361f82`.

## ADR-0030 in one line
Any-format upload (PDF / arbitrary CSV-JSON / a photo) → the SAME no-train lane the chat/de-id already use → `extract_readings` (structured `(item, timepoint, source, value)`) → operator confirms every value → lands via the UNCHANGED `store.append`. The first model step on the ingestion axis; swappable to a local model (ADR-0015 North-Star) as a backend choice, not a re-plumb.

## The Tier-3 review caught the showstopper the mock-tested build missed
- **F1 (LEGITIMATE, fixed):** production confirm-landing was DEAD. `scripts/serve/__main__` builds the server with no `store_root` (None); `_do_confirm_extraction` called `land_confirmed(root=None)`; an EXPLICIT None overrode the sink's `root=store.DEFAULT_ROOT` default → `store._item_path(item, None)` → `Path(None)` TypeError → degraded to `{"landed": []}`. The headline capability was 100% non-functional in production while the whole suite was green (every test injected a tmp store_root). Found **independently by Bug-Hunter + Contracts, both reproduced by execution.** Fixed: resolve None→DEFAULT_ROOT in `land_confirmed` (mirroring `route_upload`/`persist_capture`) + a production-None landing test (`96abc1b`). → **PF-S99-01.**
- **F2 (LEGITIMATE, fixed):** the SPA confirm handler did `.then(r=>r.json())` with no status check; every error body (400/413/415) carries `landed:[]`, so an HTTP error painted a green "✓ Landed 0" AND wiped the pending review — false success + data loss. Gated success on `res.ok && !error && !degraded && n` (`85dbc96`).
- **F3 (LEGITIMATE, fixed):** the empty-extraction negative control was tautological (`_offered_readings`==[] passes for any non-JSON response). Pinned the distinguishing no-data shape (`ctype != application/json`) so a fabrication mutation reds it (`3d2f371`).
- **F6 (bundled):** `land_confirmed`'s non-dict guard was untested (asymmetric with the client.py twin) → parametrized test added.
- **F4 (DECISION → bead `by30`):** POST /upload has no CSRF/Origin gate + now wires a live client → a cross-site page could drive metered extraction (denial-of-wallet). Bounded (loopback-only, nothing LANDS via the CSRF-gated confirm path, attacker's own content — NOT a PII leak); the same-origin gate is defense-in-depth needing operator sign-off.
- **F5 (DEFERRED → bead `nuct`):** the SEC-01 fail-closed scaffolding is now 3 copies → extract a shared `_bounded_call` helper.

All fixes blind-verified RESOLVED by EXECUTION (each RED-reproduced on scratch copies). Crown-jewel PII 0-leak HELD by execution; EXTEND-NOT-REBUILD numstat=0; core-capability-audit exit 0. Full suite 1846 passed / 7 skipped / 2 env (port-8765).

## Process failures promoted
- **PF-S99-01** (`2xu4`): a new production WRITE path reachable from the operator-entry factory was built + reviewed entirely with injected tmp roots; the None-default production path was never exercised, so a None→crash that broke the headline feature survived to Tier-3 (caught there, $0, pre-merge). Recurrence of the PF-S87-01/PF-S97-01 components-pass-integration-breaks class. Guard: such a recipe's ACs MUST include a test driving the real factory default path; Tier-2 QA verifies it exists.
- **PF-S99-02** (`2l69`): presented the operator a false binary (no-train API vs local-model pivot) during scoping — the operator corrected it twice. The red-team finding only required amending the boundary ADRs, not a pivot. Guard: verify both options are real + on-topic before offering a choice.

The defining POSITIVE: the layered Tier-3 review caught all three legitimate ingestion defects the mock-tested per-wave build missed — the same pattern as S97's BUG-1, working as designed.

## State after S99
`main` @ `8361f82`. The build (intake + plan engine + format-agnostic ingestion) is COMPLETE + mock-proven. The ONLY remaining step is the operator-present LIVE run (real key + real data + spend, ADR-0030 OQ-1) — operator-gated. See HANDOFF.md "What Is Next" + the carry beads.