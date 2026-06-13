---
title: Session 57 — the calendar-event data model shipped (zone 2 This Week)
type: note
owner: Walter McGivney
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
permalink: a-plus-maxing/sessions/session-57
---

# Session 57 (2026-06-13)

## What happened

Merged the owed S56 close PR, then built the second of the three remaining "done"-path
dashboard data models — the calendar-event data model (zone 2 This Week) — through a full
6-agent review/merge lifecycle. The session PIVOTED from the operator-recommended
30-day-rollup to calendar-events after verify-first found the rollup needs unsigned design
(below). Two PR lifecycles, every gated skill invoked fresh.

## Merged (sequential, suite green after each)

| PR | beads | Content |
|---|---|---|
| #119 | — | S56 close docs; 3-agent subset; 2 LEGITIMATE fixed (HIST-1: my S56-close S55-archive entry cited OFF-MAIN pre-rebase SHAs `3104fcc`/`69b372a` → corrected to on-main `19ba424`/`cccfd5c` + a pre-rebase disclaimer; QUAL-1: cite bead `dqyv`, not the PR-local "HIST-2" label); 2 NOT_A_BUG; rebase-merge `fd885df` |
| #120 | `86vu` | the calendar-event data model. Full 6-agent: Security 0, Bug Hunter 0, Contracts 7 positive; 1 LEGITIMATE fixed (the `dqyv` 3rd-consumer note); TEST-1/TEST-2 NOT_A_BUG; 0 suppressed; rebase-merge `b74ee0f` |

Final `main`: `b74ee0f`; suite **785 passed / 2 skipped** (760 at session open, +25).

## The pivot (rollup → calendar)

My S56-close recommendation was the 30-day-rollup "first (most self-contained)." S57
verify-first FALSIFIED that: the rollup (zone 5 care-team per-domain status) needs TWO
UNSIGNED design decisions — the 16-specialist→tracked-store-item mapping (no structured
mapping exists; the `_SPECIALISTS` tuple carries only free-text "tracks" lines) and the
30-day aggregation/status rule. The signed spec signs only "a colored per-domain status
line." Calendar-events (zone 2) is by contrast fully signed (the 4 event categories + their
CHROME tints are in `component_set`, AA-measured; "event pills land in the cells"). So S57
pivoted to calendar-events (the genuine goals-parallel signed-anatomy build); the rollup
defers to a design-then-build session — PF-S6-01 + PF-S49-01 working (no build against an
unsigned target).

## The build (86vu)

- **`scripts/store/calendar_schema.py` (new).** A `calendar::events` content-tagged store
  stream (the `plan-track` pattern): each event `{category ∈ training/lab-draw/check-in/
  appointment, label}` at a date-only timepoint, sourced by `loop_schema._content_tag` so
  distinct same-date events both persist while an identical re-entry is idempotent.
  `EVENT_CATEGORIES` are exactly the 4 signed pill tint names; unknown category / empty
  label / malformed date is rejected at the writer. Corrections by re-recording
  (content-tagged, outside `store.correct`). `resolve_events` groups by date; `read_events`.
- **`vault/design/templates/dashboard.py` (zone 2 render).** Routes `calendar::events` into
  `_calendar_zone`/`_month_calendar`: category-tinted pills (`cs.pill(label, category)`)
  land in each matching day cell (`.cal .evlist` stack); a no-event cell keeps the bare
  day-number markup (the S49/S50 empty-store path the calendar-shell tests pin); the awaiting
  caption shows only when no events are stored. Built strictly from the signed zone-2
  anatomy. One additive `component_set` `.cal .evlist` CSS rule.
- **Tests.** `tests/store/test_calendar_schema.py` — writer validation, date-grouped
  resolution, the same-date-distinct / idempotent-re-entry split, and the store-adversarial
  battery (cross-stream, content-tag, timepoint field) with the mutation battery proven RED
  per field. `tests/generate/test_calendar_zone.py` — in-cell pill placement (correct day),
  bare no-event cells, the honest empty state, the today-marker preserved, no raw-key leak.

## Governance / discipline

- INV-SKILL-TRACE bound both PRs (green, 2 rows all-YES). INV-TRUNK-COMPLETENESS green at
  open + close. The full `/review-pr` methodology ran on both (profile-less blind triage +
  blind verification); 0 findings suppressed.
- **The off-main-archive-SHA class RECURRED** (the #119 review's HIST-1: my S56-close
  S55-archive entry cited the pre-rebase `fix/s55-close` tips) — caught + fixed (on-main
  `19ba424`/`cccfd5c`), recurrence_count=2 watch + a structural-fix bead (mechanize an
  on-main-SHA check for the archive). The lesson was applied IMMEDIATELY: the S56 archive
  entry written at this close cites the on-main `3488a10`/`fd885df` (git-verified).
- The #120 6-agent panel REFUTED two of its own findings (TEST-1 — the cross-stream
  docstring is accurate, the inverse of the S56 false-docstring class; TEST-2 — single-month
  design is correct) — the layered review working.
- `dqyv` (promote `loop_schema._reading`/`_content_tag` public): calendar is now the 3rd
  consumer; the trigger fired, the bead was updated (not built — scope-deferred).

## Beads

Closed with provenance: `86vu` (built + merged #120). Updated: `dqyv` (3rd consumer). New:
the archive-SHA-check structural-fix candidate. Still OPEN and next-up: the 30-day-rollup
(zone 5 — DESIGN-then-build); `b6um`, `e3b`, `02pe`, `r3pq`, `5zfk`, the S52 governance tail,
`1ww`, `pq7m`, `dqyv`.

## Next (S58)

Merge the S57 close PR, then the done path's LAST awaiting-zone model: the 30-day-rollup
(zone 5). UNLIKE goals/calendar it is a DESIGN-then-build — record the specialist→metric
mapping + the 30-day aggregation/status rule (a `juc`-style decision note, likely with
Walter's input) BEFORE building, then build + wire zone 5. Once it ships, the dashboard is
no-placeholder except wearable (LM-02, operator-gated). `b6um` as a quick win when the AA
gate is next touched; `dqyv` + the archive-SHA-check opportunistic. Baseline 785/2.
