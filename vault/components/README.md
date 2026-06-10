---
title: Component Notes — the as-built "what" layer
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/readme
---

# Component Notes

One short note per production module (or tight module cluster): what it does, its key
contracts, who calls it in production, and which ADR governs it. This is the "what's
wired to what" layer the CLAUDE.md Cross-Document Ownership Matrix assigns to
`vault/components/` — ADRs answer *why*, these notes answer *what*, so a future session
or codebase scan doesn't re-derive the data model from source.

**Maintenance rule (the part that keeps this layer alive):** any PR that changes a
module's CONTRACT — its public functions, field sets, stream types, published states,
or routing — updates that module's component note in the same PR. Internal-only changes
(implementation, comments, test-only seams) don't require a note edit.

## Coverage

Seeded S48 (the modules the ADR-0008 build touches): `store`, `loop-schema`,
`biomarker-meta`, `render-engine`, `render-views`, `plan-layer`, `generate-entry`.
Not yet covered (add when first touched by a contract-changing PR): the ingest adapters
(`scripts/ingest/`), the guard layer (`scripts/guard/pii_scan.py`), the clone tooling
(`scripts/clone/`).
