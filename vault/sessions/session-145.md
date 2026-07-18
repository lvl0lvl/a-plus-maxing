---
title: Session 145 — Plan-personalization Wave 1 (ADR-0050) + the de-id egress catch
type: session
status: complete
created: 2026-07-18
review_cadence: none
permalink: a-plus-maxing/sessions/session-145
---

# Session 145 — Plan-personalization build, Wave 1

`/run-pipeline` "to completion" drive for the S145 core-capability fix: make `/generate-plan` produce a genuinely personalized plan from the operator's real data.

## What landed on `main`

- **P2** — spec `docs/spec/adr-0050-0051-plan-personalization-spec.md` (#374; coverage amendment #375) + build plan `docs/build-plan/build-plan-adr-0050-0051.md` (#376).
- **P3 Wave 1 (COMPLETE):**
  - **ADR-0050-T1** (#377) — the `/generate-plan` front door now authors each domain from `context_assembler.assemble_context`'s identity-stripped FULL record, not `router.summarize`'s thin band.
  - **ADR-0050-T2** (#378, merged `aae34feb`) — `_author_system_prompt` is contract-driven + genetics-aware, sourcing each renderable specialist's section from `design/specialist-plan-contracts.md` (single-source; ADR-0050 Alternative-C rejected).

## The de-identification crisis (the load-bearing event)

T2's initial build interpolated the **operator-grounded** `specialist-plan-contracts.md` into the model SYSTEM prompt — leaking the operator's real name + medical record to the no-train model **unscanned** (the `pii_scan` de-id gate covers only the user-message summary). It nearly advanced past Tier-2: the Architect's first-pass Position-A APPROVE accepted "no live path" + "file ships in repo" claims without executing them (F-011 lapse; PF-S145-06). Caught only because the orchestrator grounded QA's `care_chat` Leg-2 reachability against the live tree and reopened the binding ruling → the Architect surfaced Finding 3 (the egress).

**Fix (operator-approved SPLIT):** `design/specialist-plan-contracts.md` is now the GENERIC committed doc the prompt reads; the operator-grounded original is untracked + gitignored (`design/*.operator-grounded.md`); per-domain negative-PII tests guard the prompt (proven non-vacuous — RED-fire against the operator-grounded doc). The operator's raw record reaches the model only via the identity-stripped user-message channel. Independently re-verified closed by a fresh 4-lens Tier-2 + a full 6-agent Tier-3 (`.rigor` machine verdict CLEAN → merged).

## Decisions / patterns

- **Two-channel de-id (the durable architecture):** SYSTEM prompt = generic specialist methodology (zero operator identity); USER message = the operator's identity-stripped raw record (`pii_scan`-gated). Personalization comes from the record, never from the prompt.
- **SEC-001 (operator-decided):** the ride-along bead + the negative-PII test blocklist commit the operator's health record to the public tree. The model egress being fixed, the operator chose to genericize the gratuitous bead reproduction, keep the load-bearing test tokens, and bead the commit-hook-widening (`ijd5`) rather than a deeper scrub — his record is already extensively self-published in his own repo, and his de-id standard concerns the model channel.

## Open follow-ups

`rbwh` (runtime `pii_scan` over the assembled system prompt), `ijd5` (widen commit-hook to health-record vocabulary), `qmae` (server.py Leg-2 logging), `yoyc` (metered-lane arming-gate), `t99p` (test-infra git-index footgun), `dbp3` (build-plan prose freshness), `cdde`/`s7bn` (ADR-0051-T1 reconciliation), `2u6k`/`y2dk` (this session's PF beads).

## Next

The **Phase-1 operator-verification** — the operator runs `/generate-plan` on real data and confirms the plan is personalized (the deferred AC3 quality check) — operator-gated (real key + data + spend). Wave 2 = **ADR-0051-T1** (raw genetics carry, identity-stripped) builds *after* that verification.