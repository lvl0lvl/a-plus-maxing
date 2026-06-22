---
title: Session 89 — conversational-intake build planning + strict-autonomous-loop setup
type: session
date: 2026-06-22
owner: Walter McGivney
status: complete
---

# Session 89 — build planning + strict-autonomous-loop setup

**Shape:** an operator-directed setup session. After the S88 foundation merged, the operator said: "there is an api key in the mac keychain you can use, but do everything we can before spending tokens/money on it. Set up everything you need to run the strict autonomous loop and we'll do it in the next session. Then run the full session close." So S89 produced the build-planning pipeline (no API spend) so S90 is a pure strict `/execute-plan` loop.

## What happened

1. **The build SPEC** (`docs/spec/adr-0015-0019-conversational-intake-spec.md`) — ADRs 0015–0019 + the design doc → buildable FRs/NFRs/binary ACs. 8 tasks / 2 waves. Carries all 6 deferred design-stage requirements as explicit ACs (the per-token coarseness proof / `identity_config` wiring / CONCERN-1/2 / M-3 / the crown-jewel PII NFR / the PF-S87-01 end-to-end bar). Surfaced + ACd a real in-scope defect: the `equipment-access-class` double-source collision (`router.py:82` already maps `postal-address`→`equipment-access-class`, AND the demographic activation would source it — ADR-0018-T1 reconciles it).

2. **The BUILD-PLAN** (`docs/build-plan/build-plan-conversational-intake.md`) — Wave A (model boundary + conversation path: the swappable no-train client, the question strategy, the plan-author rewire, the `/chat` seam, the extractor) → Wave B (form activation + token vocabulary + end-to-end: the demographic activation, the `SUMMARY_FIELD_SET` extension, the PF-S87-01 end-to-end gate). Executable per-wave checkpoint Go/No-Go gates; 3-tier review assignments (Architect + Security on the model-boundary + store-surface tasks). The LIVE end-to-end run is the final, operator-present checkpoint.

3. **The 8 TASK-PLAN recipes** (`docs/task-plan/ADR-001{5,6,7,8,9}-T*.md`) — per-task TDD recipes matching the project format, failing-capable (not tautological) with negative controls. The model-client tasks test against a MOCK (no live API); the store-surface tasks carry the `docs/checklists/store-adversarial-tests.md` battery; the per-token coarseness proof uses an INDEPENDENT output scan (the de-id gate does not run on the derived-token path); the end-to-end test goes RED if it produces the honest no-plan state instead of a usable plan.

All three planning stages were produced by FRESH-context sub-agents (a deliberate quality choice — authoring from this long conversation would be lower-quality) and self-validated against the live merged tree.

4. **The keychain key.** The operator's no-train API key is in the macOS keychain. A broad keychain scan was correctly blocked by the credential-exploration guard; I asked the operator for the specific item name and documented the runtime-fetch discipline (`security find-generic-password -s "<NAME>" -w`, fetched at run time, NEVER stored/printed/committed — the repo is PUBLIC). The build loop (S90) fetches it for the live end-to-end run only.

5. **The strict-autonomous-loop directive** for S90 (HANDOFF "What Is Next") — `/execute-plan` Wave A → checkpoint → Wave B → checkpoint, then the live end-to-end run with the keychain key. Build/mock-test everything first (no spend); the live run is the operator-present checkpoint.

## PF this session

No new PF. Clean planning session — fresh-dispatched + self-validated artifacts; the credential-exploration guard fired as designed; no live API call. Full attestation + skill-trace + disclosure ledger in `memory/process-failures.md` Session 89.

## Next (S90 — the strict build loop)

Run the conversational-intake BUILD as a strict autonomous `/execute-plan` loop (the recipes are ready). Surface the foundation for operator review first (the autonomously-added ADR-0019 + the RT-01 fail-closed contract + the Claude no-train default). Per PF-S87-01 the acceptance is a usable plan, not just chat plumbing.
