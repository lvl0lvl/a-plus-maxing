---
title: Session 58 — the care-team rollup shipped (zone 5); the dashboard "done" path is complete
type: note
owner: Walter McGivney
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
permalink: a-plus-maxing/sessions/session-58
---

# Session 58 (2026-06-13)

## What happened

Merged the owed S57 close PR, then built the THIRD and LAST of the three remaining "done"-path
dashboard data models — the 30-day care-team rollup (zone 5 "Your Care Team") — through a full
6-agent review/merge lifecycle. With it the dashboard is no-placeholder except the wearable
surface (LM-02, operator-gated). Two PR lifecycles, every gated skill invoked fresh.

## Merged (sequential, suite green after each)

| PR | beads | Content |
|---|---|---|
| #121 | — | S57 close docs; 3-agent subset; 0 findings (all three agents git-verified the rotation completeness + on-main/off-main SHA classification + counts); rebase-merge `93c4f1c` |
| #122 | `ektw` | the care-team rollup. Full 6-agent: Security 0, Contracts 0; 3 LEGITIMATE fixed + blind-verified, 1 NOT_ACTIONABLE, BUG-1 DECISION-by-rule elected-refined for honesty; 0 suppressed; rebase-merge `afd40a8` |

Final `main`: `afd40a8`; suite **821 passed / 2 skipped** (785 at session open, +36).

## The design-then-build (ektw)

Unlike goals (S56) and calendar (S57), zone 5 was a DESIGN-then-build: the signed visual spec signs
only the card anatomy + "the colored per-domain status," NOT which data drives each specialist nor
what the color means. At session open I surfaced the one genuinely-open product question — given only
~6 of 16 specialists have any store stream, should zone 5 show all 16 (honest grey on the empty
domains) or only the streamed few? Walter: **"'a' sounds right"** (all 16, honest grey). The two
decisions were recorded in `vault/decisions/2026-06-13-care-team-rollup-zone5-mapping.md` BEFORE
building (PF-S49-01):

- **Decision 1 — mapping.** Each specialist's status derives from the streams already attributed to
  it (the `_PLAN_CARDS` `default_specialist` wiring, the labs streams, the physician-note stream) +
  calendar event categories by natural owner. 6 of 16 mapped; 10 streamless → honest grey.
- **Decision 2 — the 30-day freshness rule.** Status = recency of the latest RECORDED-DATA timepoint
  (green ≤30d / amber 31–60d / grey >60d / grey none). NOT "on track / off track" (that needs unsigned
  per-domain targets — overreach). Future scheduled events are EXCLUDED (the #122-review refinement —
  see below).
- **Decision 3 — sparse-domain honesty.** Option (a): all 16 cards, honest grey "no data yet" on the
  streamless. Walter-confirmed.

## The build

- **`scripts/store/care_team_rollup.py` (new).** A pure READ-MODEL (no new store stream, no write
  path): `resolve_rollup(store_read, today)` attributes each reading by prefix / calendar category and
  reduces each specialist to a `{state, days}` freshness from its latest recorded-data timepoint.
  Timepoints (date-only plan/calendar OR full-datetime loop streams) reduce via the house
  `datetime.date.fromisoformat(timepoint[:10])` tolerant parser (mirroring `component_set.reading_date`
  — store-layer-local to avoid a template-import inversion). Store-layer module, imports only `datetime`.
- **`vault/design/templates/dashboard.py` (zone 5 render).** `_care_team_zone(rollup)` carries a
  data-state status dot (`.sdot-*` = PALETTE good/watch/muted — non-text chrome, separate from the
  name's category glyph dot; ADR-0009 D3) + a muted recency caption; honest "no data yet" grey on the
  streamless; an all-empty store keeps the static "no rollup yet". One additive `component_set` block
  of four `.sdot` CSS rules.
- **Tests.** `tests/store/test_care_team_rollup.py` — mapping, the 30/60-day band boundaries,
  calendar-category routing, future-exclusion, order-independent latest-wins, cross-stream isolation
  (constructed + real `store.read_all` end-to-end), unparseable-timepoint skip; the store-adversarial
  battery's applicable categories (cross-stream + threshold-boundary + mutation-RED per the per-test
  docstrings; dedupe categories N/A for a read-model). `tests/generate/test_care_team_zone.py` — the
  colored status render, streamless grey, the all-empty static fallback, exact recency captions,
  no-accent-leak, no-raw-key-leak.

## The #122 review caught a real honesty defect in my own same-session design

The 6-agent review's BUG-1: a future-dated calendar event became a specialist's `latest` timepoint and
rendered "updated today" — a false data-update claim (an upcoming appointment is scheduled, not
recorded data). The blind triage correctly classified it DECISION (it relitigated my just-signed
decision note, which had tabulated "updated today" for the future/today case). But that note was MY
same-session artifact, and the defect is real on a doctor-visit honesty-focused dashboard — so I
elected to REFINE the note's freshness rule to exclude future events (recorded-data recency only; a
future-only specialist reads "no data yet"), updated the code + tests, proved the new tests mutation-RED,
and flagged the refinement to Walter. The layered review working as designed on a self-authored design.
Three further nits fixed + blind-verified: stale source line-anchors in the note (→ symbol names),
an order-blind latest-wins test (→ added a reversed-order case), and a module-docstring mutation-scope
overclaim (the S56 #118 false-mutation-docstring class).

## Governance / discipline

- INV-SKILL-TRACE bound both PRs (green, 2 rows all-YES). INV-TRUNK-COMPLETENESS green at open + close.
  Full `/review-pr` methodology on both (profile-less blind triage + blind verification); 0 suppressed.
- **Observed (PF-S51-01 shape, not promoted):** the 6 Phase-1 review agents ran mutation batteries in
  the SHARED working tree; one reviewer momentarily observed another's un-reverted mutation. The tree
  was verified pristine afterward (no harm). Watch: worktree-isolate or read-only the mutation-running
  reviewers; the blind triage + verification WERE told read-only and stayed clean.
- **PF-S13-01/PF-S37-01 held this close** — DOCUMENT_RUBRIC was RUN for real at step 8 (the exact S57
  failure), with cited evidence. The off-main-archive-SHA discipline HELD (S57 archive entry cites the
  on-main `55a1ab0`/`93c4f1c`, git-verified; count stays 2).
- **Verify-first catch:** the rollup first assumed date-only timepoints; the loop streams use full
  datetimes — corrected to the house `[:10]` parser before the suite caught it.

## Beads

Closed with provenance: `ektw` (built + merged #122). Still OPEN and next-up: the correctness/governance
tail (`b6um`, `e3b`, `02pe`, `r3pq`, `5zfk`, `rn3v`, `imev`, `tdre`, `vjsw`, `dt0t`, `1ww`); `pq7m`
(store-schema-gated); `dqyv` (3-consumer promotion); the archive-SHA-check follow-up.

## Next (S59)

Merge the S58 close PR. The done-path dashboard is COMPLETE (all 3 awaiting zones shipped; the wearable
surface is LM-02-gated on Walter's data). Forward work shifts to the correctness/governance tail +
the deferred follow-ups (`dqyv`, the archive-SHA-check), each through a full review/merge lifecycle;
verify-first each bead against the live code (bead text can name pre-refactor paths). Baseline 821/2.
