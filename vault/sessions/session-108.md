---
title: Session 108
type: session
created: 2026-07-04
status: complete
permalink: a-plus-maxing/sessions/session-108
---

# Session 108 (2026-07-04)

## Goal

The Tier-1 "quick safety fixes" from the S107 remaining-work recommendation, operator-directed ("do the quick safety fixes now") — beads `55qg` (CSRF gate on `/chat` + `/care-chat`) and `qiob` (dormant interaction screen).

## What landed — `55qg` (PR #292 → main `a28a760`)

`_do_chat` and `_do_care_chat` drove `client.converse` (metered no-train spend on the operator's key) with **no** `application/json` Content-Type 415 gate, while every other POST handler (`/generate-plan`, `/plan-loop`, `/save-key`, `/confirm-*`) enforces one — a cross-site CORS-simple `text/plain`/form POST could force converse spend. Added the same inlined gate to both handlers (refuse before any work), byte-consistent with the five sibling gates. Serve-layer only; frozen engine + store numstat=0. TDD: per-route 415-refusal (0 converse, mutation-proven) + `application/json; charset=utf-8` accept (mutation-proven the `;`-split isn't over-broad) + missing-header 415.

## `qiob` — grounded, NOT a quick fix, surfaced (not fake-fixed)

Grounding revealed `qiob` is a **design decision**, not mechanical: the tailoring interaction screen is dormant because `record_plan` (the **frozen** spine, `generate_plan.py:447`) drops the candidate's `ae_profile`, so a recorded compound plan carries no additive-AE class basis → the screen finds nothing. The bead's fix options all touch the frozen path or need an ADR (persist via `record_plan` + ADR-0032 coordination / re-derive at tailoring / document), and it is **secondary defense-in-depth** — the *primary* additive-AE/BPMH screening still HOLDS unsafe compound domains at generation (a held domain records no plan → no tailoring), so the dormancy "does not open the primary hole." So I built `55qg` and **surfaced `qiob` for the operator's design call** (the S105 Architect leaned *retire*) rather than fake-fix it or make a unilateral frozen-spine edit — the same grounding-reveals-more honesty applied to `3ge1` (S106).

## Review (local 3-lens, GraphQL rate-limited)

Security (gate SOUND, 0 in-diff findings — every CORS-simple type refused, byte-consistent with siblings) + correctness (0 bugs) + test-coverage (reject tests mutation-proven; a MEDIUM charset-accept gap + LOW cases fixed). The layered review worked as designed — the security lens caught an **out-of-scope forced-spend gap on `/upload`** (multipart is a CORS-simple content-type a content-type gate structurally can't cover → beaded `o2gj`, needs an Origin allowlist), and the test-coverage lens caught the charset-accept gap. All findings fixed or beaded, no severity suppression.

## Next

- **`qiob`** — the operator's design call (retire vs persist-via-frozen-spine+ADR vs re-derive).
- **`yvrs`** (the genuine large-change hold — gates the runner's live activation), the **ADR-0039 BUILD**, the operator-present **LIVE core-plan run** (target before the Aug-4 visit), **LM-01 prep** (~July 28).
- New beads: `o2gj` (`/upload` forced-spend), `o0vg` (git-mutating governance-test flake — the third full-suite-contention flake this arc). Carried: `tmfm`/`z2mh`/`jlbh`/`x4zj`/`hekm` + the close-audit flake.

## References

- PR #292 (merged `a28a760`); bead `55qg` (closed).
- `scripts/serve/server.py` (`_do_chat`/`_do_care_chat` gates).
- `memory/process-failures.md` `## Session 108` (skill-trace + PF attestation + disclosure ledger).
- LM-01 rescheduled to 2026-08-04 (PR #291).