---
title: Project Setup
type: decision
permalink: a-plus-maxing/decisions/project-setup
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-05-16
status: active
depends_on: []
superseded_by: null
review_cadence: manual
tags:
- project-setup
- decision
- infrastructure
---

# Project Setup

## Decision

Initialize `a-plus-maxing` with the standard fresh-start scaffold: git on main, beads issue tracker, basic-memory vault, document freshness rubric, safety hooks, and session protocols.

## Context

This is the project's first session. No prior code, no prior decisions. The fresh-start recipe captures the standardized infrastructure layer so the project starts with the same defaults as every other project: VOLATILE-section rotation, cross-document ownership matrix, hook-based guards against destructive git ops, and a vault for cross-session knowledge.

## Consequences

- Every session begins with HANDOFF.md and ends with the close protocol from CLAUDE.md.
- Destructive `git` and `rm` commands are denied at the harness layer.
- Direct push to `main` is blocked; feature branches required.
- `/upgrade-skill` is wired with `pending-deploy` placeholder for `sanitization_contract_sha256`; will be replaced on first `/upgrade-skill` run.

## Related

- `CLAUDE.md` — session protocols
- `DOCUMENT_RUBRIC.md` — document lifecycle
- `.claude/upgrade-skill.yml` — `/upgrade-skill` config
- `memory/process-failures.md` — canonical failure log