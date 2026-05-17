---
title: Document Management Rubric
type: rubric
permalink: a-plus-maxing/rubrics/document-management-rubric
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-05-16
status: active
depends_on:
- DOCUMENT_RUBRIC.md
superseded_by: null
review_cadence: phase
tags:
- rubric
- document-management
- process
---

# Document Management Rubric

Vault-side mirror of `DOCUMENT_RUBRIC.md`. Tracks the six freshness rules and the session-close checklist as a navigable vault entity.

## Six Rules

1. **Single Source of Truth** — one concept, one document.
2. **Staleness Detection** — `last_reviewed` vs `review_cadence`, dependency drift, code drift, closed-issue references.
3. **Conflict Resolution** — date wins; type hierarchy decision > spec > guide > reference; user escalation.
4. **Session Review Gate** — at close, update `last_reviewed` on modified docs; flag unreviewed dependents.
5. **Archive, Don't Delete** — `status: archived`, set `superseded_by`, move to `_archive/`.
6. **Vault Consistency** — vault notes follow the same rules.

## Owner

`DOCUMENT_RUBRIC.md` is the authoritative source. This vault note is the navigable index. If they disagree, DOCUMENT_RUBRIC.md wins and this note is updated.