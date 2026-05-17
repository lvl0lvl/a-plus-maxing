---
title: Session 1 — Initial Scoping + Vault Architecture
type: session
status: complete
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: manual
permalink: a-plus-maxing/sessions/session-1
---

# Session 1 — Initial Scoping + Vault Architecture (2026-05-16)

First working session after `/fresh-start` ran on desktop. This session was run from Walter's phone (separate Claude process; shared filesystem with desktop, no shared conversation memory).

## Scope
- Audit the fresh-start output
- Scope the project's actual purpose
- Design the vault architecture
- Set up structural directories and placeholder files for the personal health agent

## What got decided
- **Project identity:** LLM-driven personal health agent, NOT a SaaS tracker. Bryan Johnson Blueprint-inspired, low-budget.
- **Architecture:** Markdown substrate + HTML artifacts on demand (per Thariq Shihipar's html-effectiveness argument).
- **Phasing:** A (conversational, active) → B (scheduled artifact jobs) → C (custom interface, deferred until friction-log evidence justifies it).
- **No diet app:** meal template + LLM-computed macros/micros via USDA data.
- **Near-term goal:** July 2026 doctor visit baseline.
- **Research corpus folded into same vault** under `library/` (peptides, supplements, interventions, biomarkers, methodology).
- **N=1 trial methodology** captured as a first-class concern with explicit design rules.

Full decision record: `vault/decisions/2026-05-16-system-architecture.md`.

## What got built (all under `vault/`)
- `meta/overview.md`, `meta/targets.md`
- `protocols/` placeholders: meal-template, supplement-stack, exercise, sleep
- `dna/analysis.md` (pending raw file from Walter)
- `library/README.md` + entry-shape guide
- `library/methodology/n-of-1-trial-design.md`
- `library/methodology/evidence-tiers.md`
- `experiments/_template.md`
- `design/artifact-design-protocol.md` (HTML design system, skeleton)
- `interactions/README.md` (friction-log format for Phase C)
- `decisions/2026-05-16-system-architecture.md`
- `sessions/session-1.md` (this file)

## What got built outside vault
- 3 memory files in `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-a-plus-maxing/memory/`:
  - `project_overview.md` (project)
  - `user_walter_context.md` (user)
  - `feedback_evidence_driven_product_design.md` (feedback)
  - `MEMORY.md` index
- 1 beads epic: `a-plus-maxing-c6k` "Establish health baseline by July 2026 doctor visit" (P1)

## What did NOT get done (next session)
- Fill in any actual protocol content (meal template, supplement stack, exercise plan) — Walter to draft
- Parse 23andMe raw genotype — pending Walter dropping file into `vault/dna/raw/`
- Generate first HTML artifact (will inform the design protocol)
- Order Oura (Walter, in next few days)
- Schedule any Phase B jobs

## Drift detection (per CLAUDE.md session close)
- **Task drift:** None. Scope grew via explicit user approval (added research library + experiments mid-session). All in-conversation, no silent changes.
- **Architecture drift:** N/A — INVARIANTS.md does not exist yet (no invariants formalized). The decisions made this session SHOULD become the first invariants: markdown substrate, HTML artifacts on demand, phased A→B→C build, evidence-driven Phase C design.
- **Vision drift:** N/A — `design/vision.md` does not exist. The vision is `vault/meta/overview.md` written this session. Self-consistent.

## Open questions / next-session candidates
- Should `vault/` come out of `.gitignore`? Walter wants multi-device coherence (mobile + desktop). Currently the vault is local-only as fresh-start designed it, which breaks the multi-device pattern.
- Should we formalize the first invariants (markdown substrate, etc.) into a project `INVARIANTS.md`?
- January 2026 health issue — need details before exercise protocol can be drafted responsibly.

## Confidence + notes
- Heavy structural session; no actual content yet. Real value lands when Walter starts populating protocols and we generate the first artifact.
- The "agent + wiki + n=1" framing now has concrete bones. Future sessions can read `meta/overview.md` and orient in under a minute.