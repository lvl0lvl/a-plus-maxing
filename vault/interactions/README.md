---
title: Interaction Log — README
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: manual
permalink: a-plus-maxing/interactions/readme
---

# Interaction Log

Each `YYYY-MM-DD.md` file in this directory captures meaningful agent-user interactions and friction signals observed during that day's sessions.

## Why this exists
Phase C (custom interface) is deferred until observed friction tells us what to build. These logs are the evidence base for that design. Without them we'd be guessing.

## Entry format

```
- **HH:MM** — Asked: "..."
  - Delivered: <what the agent produced>
  - Friction: <what was awkward, missing, slow, or required follow-up>
  - Resolved: yes | partial | no
```

## What counts as a logged interaction
- Substantive question or request to the agent
- Anything that surfaced a friction point ("I had to repeat myself," "this took too long," "the output wasn't useful")
- Anomalies the agent surfaced proactively + Walter's response to them
- Workflow gaps ("I wanted X but the system didn't support it")

## What does NOT need logging
- One-line clarifications
- Routine artifact generation that worked smoothly
- Pure read-only queries

## Review cadence
- Aggregated quarterly: agent reviews `interactions/` for friction patterns and proposes Phase C requirements