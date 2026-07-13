---
title: Session 136
type: session
date: 2026-07-13
permalink: a-plus-maxing/sessions/session-136
---

# Session 136 — kn29 / SEC-W4-01: rich-domain adverse-event screening (the live-run safety blocker)

## What happened
Post the ADR-0041–0046 build (S135), the operator directed the operator-gated follow-ups toward operational readiness. This session built **kn29 / SEC-W4-01 — rich-domain adverse-event (AE) screening** (the P1 live-run safety blocker) end-to-end through the rigor pipeline: architect design → SE build → a Tier-2-Security-mandated fail-closed fix → Tier-2 whole-change review → the FULL Tier-3 `/review-pr` → `/merge`. **PR #342 squash-merged kn29 to `main` (`e5a7e698`).** The additive-AE / Rx-BPMH safety floors now screen the RICH specialist DOMAIN PROGRAMs (not just the supplement/peptide compound band), fail-closed on malformed — the operator-present LIVE comprehensive-plan run is no longer blocked by kn29 (Security's ruling).

## The problem it closed
The additive-AE / Rx-BPMH floors caught dangerous *combinations* by reading the author-declared `ae_profile` — but ONLY for the compound band. The comprehensive re-architecture (ADR-0041) gave the rich specialists a uniform DOMAIN PROGRAM carrying `cross_domain_seams`, but the floors were never wired to screen the rich domains' AE data → a LIVE run left the rich specialists' interactions un-screened (SEC-W4-01).

## Deliverable (on `main` via #342)
- **Option B (operator-decided):** fold a strongly-typed `ae_profile` sub-structure onto `cross_domain_seams` entries (`SEAM_AE_PROFILE`, single-source) + re-base `orchestrate.reconcile`'s additive-AE/Rx-BPMH screen to read the rich domains from there (shared AE-class holds both; declared interaction holds the declarer; Rx-BPMH extends to seams). The compound-band `meta.ae_profile` path untouched (no regression); `care_chat.synthesize` drops via the existing hold sets. Frozen ADR-0032 six numstat=0.
- **Fail-closed on malformed** (Tier-2 Security HIGH): a present-but-malformed seam `ae_profile` (a garbled AI declaration) HOLDS the declaring domain rather than folding it un-screened. Mis-named-key residual honestly deferred to the `validate_plan_version` chokepoint (does not block the operator-present run).

## The review earned its keep — a real safety regression + a stale safety contract caught before merge
The FULL Tier-3 `/review-pr` (6-agent → blind triage → fix → blind verify) surfaced **6 legitimate findings**, all fixed + independently re-verified (each fix's guard reverted → RED):
- **BUG-1 (Important, PF-S136-01):** the first-cut screen's `holds`-dict overwrite clobbered the compound-band `ADDITIVE_AE_HELD` reason that the medical-liaison adjudication gate keys on → **a detected supplement↔peptide bleeding-risk interaction silently dropped from the doctor-visit queue** (queue 1→0). The adversarial Bug-Hunter proved it end-to-end. Fixed with `holds.setdefault`. This was the "benign/latent" `tkqs` bead — Tier-3 proved it non-benign.
- **CONTRACTS-1 (Important):** the author-facing safety contract still described the superseded fail-open posture. Reworded.
- QUAL-1/TEST-1/HIST-1 (comment, mixed-shape test, docstring breadcrumb) + OBS-A (`[{}]` no-op).

## Process (1 PF promoted — PF-S136-01)
**PF-S136-01** (`tsm7`) — a "benign by membership" assessment of a shared-mutable-state overwrite missed a value/reason-keyed consumer (the adjudication gate). Guard: trace the FULL consumer set (membership AND value-keyed — the Call Chain Review Rule) + execute the end-to-end production path (F-011) before ruling an overwrite benign; scrutinize shared-state overwrites at the earlier review tiers. Disciplines that HELD: safety-parity-unconditional (the malformed transform is now unconditional fail-closed); run-it (every claim executed, incl. BUG-1's queue-1→0 proof); the operator-held daily-monitor layer + the operator-decided Option-B design both honored (no drift).

Disclosure ledger: 3 caught (BUG-1, CONTRACTS-1, the malformed-AE fail-open), ALL self/gate, 0 operator-surfaced. pytest 2 env-floor / 2748 passed / 8 skipped on the merged head.

## Next
The operator directed the **tracker-ingestion automation** as the next build (S137): API-pull adapters for **Whoop + Oura + Garmin + Google Health** (the new Google Health API `health.googleapis.com/v4/`, Google OAuth 2.0 — covers the Fitbit Air / Pixel; the legacy Fitbit Web API sunsets Sept 2026, so build on the new one). Apple Health stays an operator Shortcut → a watched folder. The existing ADR-0003 adapter seam is already pluggable/idempotent/schedulable — the new work is the OAuth + scheduled-pull adapters handing readings to the existing land path; the LIVE pull is operator-gated (register dev apps + OAuth credentials in the keychain). Run via the pipeline (design/ADR → build → three-tier review → merge). The daily-monitor co-arming (`7nw7`/`yeo3`/`glzi`/`4wno`) + the kn29 chokepoint (`kn29`, re-scoped P3) remain held/deferred.
