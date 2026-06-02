# NON-CANONICAL — quarantined (bead a-plus-maxing-0be)

This `research-gates/` directory is **non-canonical**. The canonical research-provenance
layout is bare `gates/` / `judges/` / `sections/` (no prefix) — see the aplus-research
`SKILL.md` section "Canonical provenance directory layout" (single source of truth).

## What this is

Build-time research scaffolding for the `supplement-specialist` design doc (PR #14).
The gate artifacts here are **genuine `gate_attest.py` output**, not fabricated — verified
2026-05-31: when `research-gates/` + `research-judges/` + `research-sections/` are renamed
to the canonical `gates/` / `judges/` / `sections/`, `gate_attest.py verify-chain --up-to 8.5`
returns "attestation chain intact" (all recorded sha256 sources resolve). The defect is purely
the `research-`-prefixed directory names.

## Why it stays non-canonical (not renamed/blessed)

Per the S19 hfm decision (ADR `2026-05-30-grandfather-design-work-research-provenance`):
design-work research is build-time scaffolding, **not** library content. The binding
provenance control is the per-page library-authoring gate — every `vault/` page gets fresh
gated `/aplus-research` with its own passing `verify-chain` before it ships. So this artifact
is grandfathered as-is, deliberately **not** canonicalized:

- Chain-integrity (`verify-chain` passing after rename) does not by itself prove the verifier
  agents were genuinely dispatched (see SKILL.md "What this does NOT prevent").
- This builder has a PF-S17-01 history (attempted to bypass the gated path with `Workflow`).
- `bda` (`scripts/audit-research-provenance.sh`) correctly rejects this layout; in place,
  bare `verify-chain` would vacuously pass (no `gates/` dir to check).

Canonicalizing it would launder provenance we cannot fully confirm, for zero downstream
benefit (no `vault/` page draws on it).

## Do NOT

- Do NOT use this directory as a build template — it is the documented non-canonical instance.
- Do NOT treat these gate JSONs as a passing provenance chain for any wiki write.
- Future builders: emit the canonical `gates/` / `judges/` / `sections/` via `gate_attest.py`.
