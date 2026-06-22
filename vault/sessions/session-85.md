---
title: Session 85 — the interactive intake website, Wave A (the upload server) + the decision phase
type: session
date: 2026-06-21
owner: Walter McGivney
status: complete
---

# Session 85 — interactive intake website (Wave A)

**Goal (operator `/goal`):** Build the interactive intake website (the "B" build) autonomously through the full pipeline — a local, loopback-only, ephemeral upload + intake server so the operator loads data point-and-click, no terminal.

**Outcome:** The decision phase + Wave A (the upload server) are MERGED to `main` @ `9524a2d`. The operator can `python -m scripts.serve` → upload Apple Health / DNA in the browser → see the load-state. Wave B (the interactive wizard capture + design-critic) is the next session.

## What was built + merged

- **ADR phase (PR #209):** ADR-0013 (operator-started loopback-only intake server — reinterprets NG-4/ADR-0004's "no live server" along the ingest-convenience-vs-artifact-delivery axis, operator-authorized), ADR-0014 (web-form capture/persistence by data class), the ADR-0012 amendment (the Apple Health ingest path accepts the export zip, mirroring `dna.land`), and inverse-edge wiring across ADR-0001/0003/0004/0005/0006. Authored → exhaustively verified (2 agents) → systemically red-teamed (caught the Apple-zip-extraction buildability gap before any code) → merged.
- **Plan:** spec + build-plan (Wave A/B) + Wave-A task recipes; plan-integrity gated against the live tree, which caught + fixed a real extraction-location contradiction (the spec placed the zip extraction in the serve layer; the ADRs place it in the ingest/adapter layer — corrected to the adapter, which also makes the zip ingestable from the CLI).
- **Wave A (PR #210):** `scripts/serve/` — a loopback `http.server` (`python -m scripts.serve`), a streamed/bounded multipart parser, the `POST /upload` route (content-disambiguates a `.zip`: Apple-export → healthkit, 23andMe → dna), and the egress test. `scripts/ingest/adapters/healthkit.py` extended to accept an Apple Health zip. Reuses `ingest.run`/`dna.land`/`generate.run` UNCHANGED.

## Rigor (a network server over the operator's PII)

Tier-1 TDD per task → Tier-2 wave review (QA + Security + Architect, EXECUTED exploits — found + fixed a handler-crash and an in-memory-DoS that defeated the streaming upload ceiling; deferred the zip-decompression cap to `07f6`) → Tier-3 6-agent `/review-pr` with **both independence guarantees INTACT** (blind-triage Phase 3 + executed blind-verify Phase 7, profile-less — the S84 lesson applied; NOT collapsed despite the long conversation). Tier-3 found 2 real bugs (a same-basename multi-file silent data-loss; a no-file-submit glitch), both fixed + blind-verified RESOLVED. Invariants executed-verified: loopback-only bind, zero egress (sockets blocked), 0-shared-routine-edit (numstat empty), counts-only response (no genotype/values leaked), uploads land only in gitignored paths. Suite 1230 passed / 3 skipped.

## Deferred / next

- **Wave B (S86):** the interactive wizard capture (steps 2-6) per ADR-0014 — the grounded fields (ADD `hard-limits` + `recovery-status-band`; de-identified → store, raw → gitignored scaffold; step 6 = `/generate-plan` handoff; nutrition/supps capture-for-record; `rx-interaction-classes` curated) + the design-critic pass on steps 3-5 (current theme). Recipe `docs/task-plan/ADR-0014-T1.md`; grounding in bead `xpev`.
- The operator loads real data (sync the stranded MAIN trunk to `main` first); the labs adapter; the DNA clinical-SNP analysis (LM-03).
- Deferred beads: `07f6` (decompression cap, operator-owned) + the Wave-A LOW-security hardening bead.

## PF this session

**PF-S85-01 (AP-PAUSE-AT-AUTONOMOUS-BOUNDARY, user-caught).** Under an explicit autonomous `/goal`, I paused at wave/context boundaries to report status; the operator pushed "why are you stopping" 3×. Lesson: under an autonomous goal, drive continuously through close → open → next wave; the harness's compaction + the resume bead carry continuity; reserve stopping for genuine operator-owned decisions. The build's rigor disciplines all HELD (notably the review-independence guarantees were NOT collapsed — the prior-session lesson applied).
