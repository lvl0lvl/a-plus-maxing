---
title: Approaches Ledger (negative-knowledge library)
type: reference
status: active
created: 2026-06-15
review_cadence: per-non-trivial-approach
permalink: a-plus-maxing/approaches/readme
---

# Approaches Ledger — negative-knowledge library

Adopted S65 from the Rigor Framework v1.0.0 (Discipline 2, F-014). One file per
abandoned technical approach. This is the home for the negative knowledge the PF
log explicitly excludes.

## What lives here (vs the PF log)

- **`memory/process-failures.md`** records *process* failures — protocol
  violations, near-misses — and EXPLICITLY excludes failed technical experiments.
- **This ledger** records failed *approaches* — dead-end designs, rejected
  optimizations, abandoned algorithms. Without it, that negative knowledge has no
  canonical home and a future session re-walks the dead-end.

A single event can touch both: if a failed approach also caused a protocol
failure, the PF entry holds the *process* lesson and the approach entry holds the
*technical* lesson, cross-referenced.

## Inclusion test

> "Would a future session waste time re-trying this without the entry?"

If no, do not write it. (The PF log's inclusion test, applied to technical
dead-ends instead of process failures.) Do NOT fabricate entries to populate the
ledger — an empty ledger is correct until a real dead-end is hit.

## Write cadence

Append on abandon; never delete. A verdict may be `superseded` by a newer entry
that names the predecessor in `supersedes:`.

## Read cadence

Before committing to a non-trivial technical approach, query this directory by
tag for the work area:
- a hit whose **"why abandoned"** is still true stops a known dead-end;
- a hit whose **"what would change the verdict"** now holds is a green light to
  re-open (flip the predecessor to `superseded` and write the new entry).

## Entry shape

See `_template.md`. Frontmatter (`name/type/status/session/date/supersedes/tags`)
plus three load-bearing fields: **What was tried**, **Why abandoned**, **What
would change the verdict** — and **Cross-references**.
