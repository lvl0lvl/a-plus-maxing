---
title: render.emit pagination is caller-orchestrated; emit -> Path contract preserved
type: decision
permalink: a-plus-maxing/decisions/2026-06-06-render-emit-pagination-caller-orchestrated
created: 2026-06-06
status: active
decided_by: Walter (operator); arbitrated by Architect
supersedes: null
relates_to: 2026-06-05-render-colorblind-safe-palette
---

# render.emit pagination is caller-orchestrated; `emit -> Path` preserved

## Decision

ADR-0004-T2's over-cap matrix/projection pagination is implemented as a
**caller-orchestrated loop above the published `render.emit(template, store_read) -> Path`
primitive**, NOT by widening `emit`'s return type. `emit` continues to write ONE
self-contained file and return ONE `Path` per call. The T2 matrix/projection render path
splits an over-cap dataset into per-page slices, calls `emit` once per slice (each per-page
template carries a distinct name, so the existing `_name_for` derives a distinct basename),
and collects the resulting single `Path`s into the `list[Path]` it returns — optionally via
one module-internal helper in `render.py` (not a published surface). `emit`'s published
`-> Path` contract and the ADR-0004-T1 change-control clause are UNCHANGED.

## Context / problem (bead 5wo, PR #53 API-001)

ADR-0004-T2 (`yo6`, Wave 4, unbuilt) requires an over-cap render to paginate into ≥2 output
files (AC-2), while AC-3 requires the at-or-below-cap case to emit exactly one file, and the
recipe simultaneously declared it "does not modify a shared interface" and routed pagination
through `emit` (which returns a single `Path`). The ADR-0004-T1 Interface Contract makes the
path-return contract load-bearing and change-controlled. A single-`Path` primitive cannot
return ≥2 paths from one call — the recipe embedded the contradiction.

## Options considered

- **(a) Amend the T1 contract** → `emit(...) -> Path | list[Path]` (the primitive owns
  pagination). NOT chosen: breaks a change-controlled return type with BUILT consumers — the
  merged `generate.run` (ADR-0004-T3) and 8+ built tests assert a single `Path`; (a) forces
  edits into already-merged code + T3's own contract, for no capability (b) cannot provide via
  a module-internal helper.
- **(b) Caller-orchestrated pagination** (CHOSEN). Keeps `emit -> Path` verbatim; zero
  built-code blast radius (`render.py`, `generate.py`, all built tests stand); faithful to
  ADR-0004 OQ-1's own mitigation ("paginate/split across artifacts" = multiple single-file
  artifacts); makes T2's "does not modify a shared interface" self-description true.

## Resolution applied

- `docs/task-plan/ADR-0004-T2.md`: two recipe-text reconciliations (the Cycle-2 GREEN "the
  split returns the list" sentence + the Interface Contracts "does not modify a shared
  interface" claim) marked `[AMENDED 2026-06-06]`. NO change to ADR-0004-T1, the spec,
  `generate.py` (T3), ADR-0006-T2, or ADR-0007-T2.
- `emit`'s PII-no-egress and refuse-external-asset boundaries are unaffected (every page
  flows through the same guarded `emit`).

## Conditions for revisiting

- A consumer needs a paginated set addressed as one unit through the single-file identifier
  (e.g. an index/manifest `emit` must itself emit) → a dedicated multi-file entry point (a
  NEW function, not a changed `emit`) earns its place.
- More than two consumers independently need pagination and their caller loops measurably
  diverge → promote the module-internal helper to a published multi-file surface, still
  without touching `emit -> Path`.

Arbitration detail: bead `5wo`; full Architect analysis captured in the S37 session record.
