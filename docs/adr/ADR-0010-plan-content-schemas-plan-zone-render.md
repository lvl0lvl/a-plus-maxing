# ADR-0010 — Plan-content schemas + plan-zone render: day-keyed per-domain plans with slot-level honesty

**Status:** Accepted (2026-06-12, S53) · Superseded-in-part (2026-07-11, Phase-8 backfill) — specialist-OUTPUT half by ADR-0041; plan-content STORAGE half (D1/D2/D3/D4/D6) by ADR-0044; **D5 render contract NOT superseded** (re-based as build tasks under ADR-0044's model / ADR-0046 progressive activation, RT-010).
**Owner:** Walter McGivney
**Relates to:** ADR-0002 (local-first time-series store), ADR-0004 (single-file artifact generation; inert controls), ADR-0006 (multi-domain plan assembly via roster — the T2 seam), ADR-0008 (type-routed dashboard), ADR-0009 (7-zone visual shell + honesty rule), ADR-0041 (uniform specialist domain-program schema — supersedes ADR-0010's specialist-OUTPUT half), ADR-0044 (comprehensive plan model — supersedes ADR-0010's plan-content STORAGE half D1/D2/D3/D4/D6; D5 render NOT superseded), `vault/design/dashboard-v1-visual-spec.md` (zone 3 as amended 2026-06-12, bead `1oh`)

## Context

The S49-S52 dashboard arc shipped the signed 7-zone visual with zone 3 (Today's
Plan) rendering only designed empty states — the `1oh` plan-content schemas were
the named missing slice, and the operator's completion bar requires plans +
tracking on the dashboard. The signed visual spec's amended zone-3 block defines
the populated card anatomy (workout stat boxes / dots / rest timer, nutrition
arithmetic / macro tracks / meals checklist, supplements counter / checklist,
peptides protocol line / watch-out rows). Meanwhile ADR-0006's T2 (orchestrated
roster plan assembly) is unbuilt: the tension is between waiting for T2's
producer and persisting plans NOW in a shape T2 can adopt without schema change.

## Decision

**D1 — Per-domain plan items, day-keyed, specialist-attributed.** Item
`plan::<domain>` over a closed domain set (workout / nutrition / supplements /
peptides); timepoint = the plan's declared ISO date (date-only); source =
`plan::<specialist-slug>` — the attribution home, rendered as the card's `via`
caption; value = the structured JSON plan content. Every write goes through
`scripts.store.store` keyed by the one keying Line Field Set. Revisions go
through `store.correct`: an append never silently overwrites.

**D2 — Content schemas closed on required fields, open on extras.** Each domain
has a closed required-field table; unknown extra keys are permitted and ignored
— the ADR-0006 T2 forward-compatibility seam: the future producer enriches plan
values with zero schema change.

**D3 — Tracking is a separate `plan-track::<domain>` day-snapshot stream.**
Workout / nutrition / supplements carry coarse day-snapshots with content-tagged
sources (loop_schema's derivation, imported — no second tag) and
latest-appended-for-date reads. Peptide tracking IS the existing watch-out
stream — no fourth tracked domain.

**D4 — Two published absence states; presence is a value + attribution.**
`no-plan` (zero stored plans) and `no-plan-today` (plans on file, none dated
today). "Today" = the artifact generation-date seam compared by date equality;
resolution is pure functions over readings (`resolve_plan` /
`resolve_tracking`).

**D5 — Render contract: deliberate routing + slot-level honesty.** Plan and
tracking items route to zone 3 only (an unknown domain suffix KeyErrors — no
silent fallthrough, the ADR-0008 D3 discipline). Slot-level honesty extends
ADR-0009 D2 into the card: an absent tracked value renders em-dash / unfilled,
never zero; derived values (Remaining, sets-done totals) render only when ALL
operands exist; interactive-looking controls are inert per ADR-0004; the report
renders plan items as verbatim readings tables (no numeric viz); awaiting copy
names the missing data. Accent chrome extends to in-card track fills and
progress dots (non-text chrome on existing hexes); zero new color tokens.
[AMENDED 2026-06-12 (#109 review)]: recorded as built — the inert button fills
render the card accent's CHROME `*-text` shade carrying paper text,
computed-contrast gated >= 4.5 (zero new tokens); the supplements counter rides
the measured supplements tint pair whenever a snapshot exists (the muted
em-dash pill only with NO snapshot); the Sets-done numerator counts
plan-intersecting snapshot keys only (the supplements counter's taken ∩ plan
rule — an unknown key never inflates the claim); the domain-keyed readers
(`read_plan` AND `read_plan_tracking`) ValueError on a domain outside their
published set; and tracking renders only against a RESOLVED plan — an orphaned
snapshot stays visible through the report's verbatim table, never the zone-3
card.

**D6 — The v1 writer is the manual path.** `plan_schema.record_plan` /
`record_plan_tracking` / `correct_plan` follow the `correction.py` precedent
(operator-invoked, store-primitive-only). ADR-0006 T2 adopts the same surface.

## Y-statement

In the context of a plan zone rendering only designed empty states while the
completion bar requires plans + tracking on the dashboard, facing the tension
between waiting for ADR-0006 T2 orchestration and persisting plans now in a
shape T2 can adopt, we chose per-domain day-keyed plan documents with
specialist-slug attribution plus a content-tagged tracking snapshot stream,
read through two published absence states and rendered with slot-level honesty,
accepting manual v1 recording, coarse day-snapshot tracking, and em-dash
derived slots until operands exist, to get a populated plan zone today and a
schema-stable seam for roster assembly tomorrow.

## Consequences

- Positive: the operator records a plan today and the signed zone-3 anatomy
  fills in place; T2 later swaps the producer, not the schema (D2's open-extras
  seam) or the render.
- Positive: the absence states are published vocabulary, so the card never
  fakes presence — the PF-S48-01 class stays structurally guarded.
- Negative (accepted): recording is manual until T2 — no orchestrated assembly.
- Negative (accepted): tracking is a coarse day-snapshot, not an event log; an
  intra-day correction story is re-recording (content-tagged identities).
- Negative (accepted) [recorded 2026-06-12, #109 review]: the snapshot revert
  hole — after recording snapshot A then B, re-recording A verbatim is a
  store-dedupe no-op (A's content-tagged identity already exists) and the read
  keeps serving B; reverting requires re-recording with any differing content.
- Negative (accepted): derived slots (Remaining, sets-done) read em-dash until
  every operand exists — visibly partial cards are the honest default.

## Alternatives considered

- **Single `plan::today` document** — rejected: per-domain absence/revision
  would need value surgery; misaligned with per-specialist assembly.
- **Tracking inside the plan value** — rejected: every tick would be a plan
  correction.
- **Per-slot items** — rejected: destroys plan-version atomicity.
- **Defer all tracking** — rejected: the majority of the signed anatomy is
  tracking-dependent.

## Review triggers

- An input surface lands (event logs vs snapshots).
- ADR-0006 T2 is built (writer adoption + extras render).
- A fifth plan domain.
- Intra-day or recurring plans.
