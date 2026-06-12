---
title: Session 50 — the two owed PR lifecycles landed (#95, #94 merged)
type: note
owner: Walter McGivney
created: 2026-06-11
last_reviewed: 2026-06-11
status: active
permalink: a-plus-maxing/sessions/session-50
---

# Session 50 (2026-06-11)

A pure PR-lifecycle session per the confirmed contract ("keep S50 to the two PRs"): the
S49 close PR and the deferred calendar-zone review, both reviewed and rebase-merged.
`main` ends at the #94 merge with the suite at **451 passed / 2 skipped**.

## PR #95 — S49 close (docs 3-agent subset)

- Agents: Code Quality, Contracts, Historical Context (the docs-PR subset). 5 findings →
  blind triage: 4 LEGITIMATE, 1 NOT_A_BUG (the "fitness-demo constraint lives only in a
  volatile section" claim was refuted with cited evidence — the constraint is durable in
  ADR-0009 lines 25-27 + 115).
- The substantive catch (contracts agent): the S49 vision-drift attestation claimed `main`
  renders "a real month calendar (in-place reveal pending #94)" when BOTH calendar
  iterations lived on unmerged #94 — the overstate-built-state class (PF-S48-01/PF-S49-01
  family) inside the durable close record itself. Fixed identically in both declared-
  transcription copies (HANDOFF + PF log). Plus: archive-range bump (5-47 → 5-48),
  PF-S49-01 recurrence count, a dropped blank line.
- 4/4 blind-verified RESOLVED. Rebase-merged (`a7e0c39`); branch deleted.

## PR #94 — calendar in-place month reveal (full 6-agent review)

- 6 agents → 11 raw findings, 8 after dedup (2 cross-agent merges). Security: 0 findings
  with full blast-radius attestation (no store value reaches the calendar markup; pill
  tints frozenset-guarded; zero-script verified on the rendered artifact). Bug Hunter
  swept the date math over 1,827 consecutive days (2024-2028) — zero failures.
- Blind triage: 8/8 LEGITIMATE; the triage agent independently re-ran all three reviewer
  mutation claims and confirmed each.
- The two Important findings:
  1. **The month-reveal control was keyboard/AT-inoperable** — `.calx { display: none; }`
     removed the checkbox from the tab order and accessibility tree; labels are not
     focusable. The artifact's first genuinely functional control failed WCAG 2.1.1
     (Level A, inside ADR-0004's unqualified AA commitment). Fixed: focusable
     visually-hidden pattern (`position:absolute; 1px; opacity:0`) + a
     `.calx:focus-visible ~ .evlegend .calbtn` outline. Zero-script intact.
  2. **The reveal test could not detect its own feature dying** — wrapping the checkbox
     in a `<div>` (killing every `~` sibling rule) passed all 7 calendar tests; the test
     asserted string-index ordering, not structure. Fixed with verbatim structural-
     adjacency pins, RED-proven by the div-wrap mutation.
- Also fixed (all RED-proven where tests): caret flip rules + `aria-label` pinned;
  datetime-derived whole-grid day-sequence oracle (a row-swap now fails); 4 new month-
  shape params (6-row Aug 2026, 4-row/zero-lead/zero-trail Feb 2027, leap Feb 2028,
  trail-0/today-on-last-day May 2026 — the dead `if trail else True` branch now
  exercised); explicit `.cal .dout` pair in the AA gate (resolved through `var(--page-bg)`,
  6.77:1); stale "today column" comments → day-cell vocabulary; the spec's Sunday-start
  example `‹ Jun 7 – 13 ›` → Monday-start `‹ Jun 8 – 14 ›`.
- 8/8 blind-verified RESOLVED. Suite 447 → 451. Rebase-merged (`ec58580`); branch deleted.
- Note: the bd pre-commit hook auto-staged a pre-existing benign `.beads/issues.jsonl`
  flush into the first fix commit (the documented `eb1` blind spot; diff inspected —
  S49-close bead notes, placeholder owner email, PII-safe).

## State at close

- Calendar zone COMPLETE on `main`: real month table (the visible week IS one month row),
  keyboard-accessible zero-script in-place reveal, structurally pinned tests, AA gate
  measuring every rendered pair (11 tints + the other-month cell).
- Zones still awaiting data models (unchanged): plans `1oh` (+ nutrition card content),
  wearable scoring LM-02, calendar events, goals, per-specialist rollup. `y0h0`/`i2yw`
  residuals and the report design-pass bead open.
- No beads created or closed this session (both reviews produced 0 deferred/out-of-scope
  findings).
- Next (S51): merge the S50 close PR, then the `1oh` slice — visual work, PF-S49-01
  discipline applies (request the mock content / sign-off before building).
