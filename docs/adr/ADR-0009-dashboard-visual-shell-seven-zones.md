# ADR-0009 — Dashboard visual shell: 7-zone in-place template with honest zone states

**Status:** Accepted (2026-06-10, S49)
**Owner:** Walter McGivney
**Relates to:** ADR-0004 (single-file artifact generation), ADR-0008 (biomarker metadata + type-routed dashboard), `vault/design/dashboard-v1-design.md` (the frozen, Walter-approved target)

## Context

S48 (ADR-0008) built the dashboard DATA LAYER: a type-routed template where no
string value reaches numeric viz, registered markers carry real units/state/
polarity-aware trend, and mixed streams render without crashing. But the built
`dashboard.py` is a plain at-a-glance value list — it looks nothing like the
approved design (PF-S48-01). The design is a plan-forward "Today" command
center: 7 zones (hero readiness, week calendar, today's plan, performance &
trends, care team, goals, labs strip), a category-accent color set, plan-as-
spine cards.

Most of the design's zones depend on data models that do not exist yet: wearable
recovery/strain/sleep scoring (LM-02-gated), plan-content schemas (`1oh`),
calendar/event and goal-progress models, per-specialist rollup. The design doc
itself scopes these as separate efforts. The question this ADR answers: how does
the VISUAL ship before those models exist, without faking data and without
forking render surfaces?

Operational constraint (Walter, S49): demo/sample data for visual verification
is fitness-domain only (bodyweight, RHR, HRV, sleep, est. 1RM, steps) — no lab
chemistry, compounds, doses, or protocols in rendered demo artifacts.

## Decision

**D1 — Grow `dashboard.py` in place; one dashboard surface.** The 7-zone visual
replaces the flat row list inside the existing template module.
`generate.run("dashboard")` IS the designed dashboard — no second "visual"
artifact name, no parallel template. Two disjoint surfaces was the `i2yw`
failure the design explicitly retired; we do not reintroduce it. The ADR-0008
type-routed row primitives become zone content (D5). `report.py` (physician
report) is untouched.

**D2 — Zone-state honesty rule.** Every zone renders exactly one of: (a) real
data, when its data model exists and the store carries it; (b) an explicit
awaiting-state card naming WHAT is missing (e.g. "Awaiting wearable data — no
recovery scoring yet"), when the model does not exist or the store is empty.
A zone never renders an invented number, a placeholder percentage, or sample
content presented as data. This extends the design's "honesty caveats are part
of the design" clause from specialist captions to zone scaffolding, and is the
structural guard against PF-S48-01's class (presenting a partial as the whole):
the artifact itself now states which parts are built and which await data.

Zone mapping at this slice:

| Zone | State at this slice |
|---|---|
| 1 Hero readiness | Awaiting state (wearable scoring is LM-02-gated; ring scaffold renders with explicit "awaiting wearable baseline" copy, no fake %) |
| 2 Week calendar | Real 7-day strip (date math), today highlighted; events row renders "no scheduled events — calendar model pending" |
| 3 Today's plan | Four specialist-attributed cards, each an awaiting-state ("no plan on file") until the `1oh` plan-content schemas land |
| 4 Performance & trends | REAL — the ADR-0008 biomarker rows: metric cells, units, state, bar sparklines, trend chips |
| 5 Care team | Real roster (16 domain specialists, static tuple mirroring the deployed roster), per-card "what it tracks"; status neutral "no rollup yet" until a rollup model exists |
| 6 Goals & progress | Awaiting state (`vault/meta/goals.md` is scaffold; no goal-progress model) |
| 7 Labs & bloodwork strip | REAL — compact strip: panel state markers, watch-out answers, latest physician note (the ADR-0008 panel/watch-out/feedback routes) |

**D3 — Category accents are a separate `ACCENTS` constant.** The design's
surface-category colors (training `#1F6FEB`, nutrition `#E8833A`, supplements
`#0E9AA3`, peptides `#7C3AED`, sleep `#5B5BD6`) land in `component_set.ACCENTS`,
distinct from the decision-pinned semantic `PALETTE` (which the accessibility
gate reads from `vault/decisions/2026-06-05-render-colorblind-safe-palette.md`
and which MUST NOT change). Accents color zone/card chrome (headers, card
borders) only — never data state. Data state stays exclusively
good/watch/concern/neutral.

**D4 — Fitness-domain registry extension.** `biomarker_meta.METADATA` gains
the fitness markers the demo constraint names: `bodyweight` (lb), `sleep-hours`
(h), `est-1rm` (lb), `steps` (count). Units always; `reference_range` only where
a general-adult range is defensible (none of these four — all goal- or
person-dependent → `None`, so state reads neutral); `good_direction` only where
physiologically unambiguous (`sleep-hours` up; the others `None` → direction-only
arrow per the ADR-0008 honesty caveat). No invented ranges.

**D5 — Type-routing stays total.** The router contract from ADR-0008 D3 is
preserved verbatim: biomarker/unprefixed-numeric → zone 4; `panel::` +
`feedback::` + `watch-out::` → zone 7; unknown `::` prefix still raises
`KeyError`. The zones change WHERE routed content renders, not HOW routing
decides. The existing mixed-stream test's invariants (no crash, no `::` leak in
labels, correct type placement, units) must keep passing against the new layout.

## Y-statement

In the context of shipping the approved dashboard visual while most zone data
models are still unbuilt, facing the choice between waiting for all models,
faking zone content, or forking a second "visual" surface, we decided to grow
the single type-routed template into the 7-zone layout with mechanically honest
awaiting-states per zone, accepting a dashboard that visibly says "not yet" in
five of seven zones, to achieve the designed product surface now, one render
path, and zero fabricated data — so each later slice (plans `1oh`, wearable
LM-02, calendar, goals, rollup) fills its zone in place.

## Consequences

- Positive: the operator opens THE designed dashboard from this slice forward;
  later slices are zone fills, not layout rewrites. PF-S48-01's class is
  structurally guarded — the artifact self-describes its built/awaiting split.
- Positive: palette gate untouched (semantic PALETTE unchanged); accents are
  additive chrome.
- Negative: five zones ship as awaiting-states — the dashboard is visually
  complete but informationally partial until the follow-on slices land
  (`1oh` plans, LM-02 wearable, calendar, goals, rollup — tracked beads).
- Negative: the care-team roster is a static tuple in the template (16 entries
  mirroring `.claude/agents/`); a roster change requires a template edit until a
  rollup model owns it. Recorded as acceptable v1 debt.
- The S48 mixed-stream test is updated for zone placement (per CLAUDE.md:
  later-phase behavior changes update earlier-phase E2E tests); its routing
  invariants are preserved, not weakened.
- Demo verification artifacts use fitness-domain data only (Walter, S49);
  health-domain zones demo as their awaiting states.

## Alternatives considered

- **New `today.py` template alongside `dashboard.py`** — rejected: recreates the
  two-surfaces problem (`i2yw`) the design retired; "dashboard" must mean one
  thing.
- **Wait for zone data models before any visual** — rejected: serializes the
  highest-value deliverable behind 4+ unbuilt models; the design is explicitly
  zone-fillable.
- **Placeholder/sample numbers in unbuilt zones** — rejected outright: violates
  the honesty floor (and the no-tautological-output discipline); a fake recovery
  ring is worse than an explicit awaiting state.
- **Add accents into PALETTE** — rejected: PALETTE is decision-pinned and
  gate-measured; mixing chrome colors into the semantic set muddies the
  data-state vocabulary.

## Review triggers

- The `1oh` plan-schema slice lands → zone 3 fills; revisit the card contract.
- LM-02 (wearable baseline) → zone 1 scoring; revisit hero ring inputs.
- A per-specialist rollup model → zone 5 statuses; retire the static tuple.
- Any change to `vault/design/dashboard-v1-design.md` (it is frozen; a v2
  design supersedes rather than edits).
