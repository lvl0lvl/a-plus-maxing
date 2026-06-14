---
title: System Overview
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-06-14
depends_on: []
superseded_by: null
review_cadence: monthly
permalink: a-plus-maxing/meta/overview
---

# A+ Maxing — System Overview

## Purpose
Personal health agent focused on longevity + body composition. Bryan Johnson Blueprint-inspired but low-budget. Sleep, diet, training, supplementation, biomarker tracking — all in one agent-driven system. Walter is the first operator; Claude is the agent.

**Distribution (load-bearing):** V1 is **shared with others to alpha-test it** — each tester clones the repo into their own independent local instance and fills it with their own data (the operator-agnostic clonable distribution, ADR-0005). Because the shared artifact is cloned by real people, **no operator PII may live in tracked source or git history** — enforced by the PII boundary (ADR-0001), the registered `block-pii-commit` hook, and the `pre-push-pii-scan` backstop. See `design/vision.md` "Who it is for".

## Architecture
- **Markdown vault** = single source of truth (this directory)
- **LLM agent (Claude)** = reasoner, planner, course-corrector — reads vault, proposes adjustments
- **HTML artifacts** = generated on demand for rich consumption (weekly reviews, monthly recommendations, doctor handouts)
- **Scheduled jobs** = daily/weekly/monthly agent runs that produce artifacts
- **Custom interface** = deferred (Phase C) until friction patterns inform design

## Phases
- **A: Conversational agent** (active) — Walter interacts with Claude directly via this project
- **B: Scheduled artifact generation** (next) — daily/weekly/monthly automated runs produce artifacts in the vault
- **C: Custom interface** (later, ~6 months out) — designed from interaction-log evidence

## Knowledge Layers
- `protocols/` — Walter's current state (what he eats, takes, does)
- `daily/`, `weekly/`, `reviews/` — Walter's outcome data over time
- `library/` — research corpus on peptides, supplements, interventions, biomarkers (cited evidence, tier-rated); base source whitelist at `library/_source-whitelist.md`
- `compounds/` — canonical compound entries (peptides, supplements, hormones, etc.) — flat folder, class is metadata
- `biomarkers/` — canonical biomarker entries — populated as labs / wearable data ingested
- `experiments/` — Walter's structured n=1 trials linking library evidence to his data
- `dna/` — genetic context
- `labs/` — biomarker history
- `decisions/` — why protocol changes were made (cites library + experiments)
- `interactions/` — friction log informing Phase C
- `design/` — HTML artifact design protocol (cross-session consistency)
- `meta/` — system-level orientation: this file + `targets.md` + `operator-profile.md` (slow-changing Walter context) + `current-state.md` (fast-changing snapshot) + `goals.md` (hard limits + doctor-handout queue) + `contradictions.md` (active contradictions log) + `index.md` (catalog of every wiki entity page) + `log.md` (append-only wiki operation log)

## Wiki Schema (added S2 2026-05-23)
`vault/WIKI.md` defines the queryable knowledge-base layer:
- **Entity types** with templates: compounds, biomarkers, protocols, parameters, decisions
- **Agent consumer roster** — 14 specialist agents (personal-trainer, labs-specialist, nutritionist, supplement-specialist, peptide-specialist, endocrine-specialist, lymphatic-specialist, gi-specialist, cardiovascular-specialist, sleep-coach, recovery-specialist, longevity-strategist, mental-performance-coach, medical-liaison) — agent profiles drafted on-demand, not speculatively
- **Source whitelist** with 5 standard tiers + Tier 2.7 (practitioner_protocol for prescribing-practice claims) + Tier NE (non-English literature) + 12-tag type enum + admissibility matrix
- Distinction between **library research** (goal-agnostic canonical entries) and **specialist-agent dispatches** (operator-personalized queries against the wiki)

## Research Pipeline (added S2 2026-05-23)
`.claude/skills/aplus-research/` wraps the global `deep-research` with mechanically enforced gates. Six blocking gates with JSON-schema-validated verdicts: 2.75 SCOPE, 3.5 JUDGE (paired retrieval+judge), 4.75 INTEGRITY (incl IC-13 per-citation corpus scoping), 6 CRITIQUE (deep+), 7.5 RISK-FLOOR (compounds), 8.5 LAYERS (standard+ compounds). Three health-specific gates not in deep-research: population-mismatch, risk-floor, concentration-audit. Use `/aplus-research` for any wiki-bound research from S3 forward.

## Data Sources
- Apple Health (Watch + iPhone) — HR, HRV, steps, workouts, weight
- Oura Ring (incoming, ~mid May 2026) — sleep stages, HRV, body temp
- Smart scale (TBD, optional) — daily weight trend
- 23andMe raw genotype — Walter has the file; pending drop into `vault/dna/raw/`
- Bloodwork — first panel via new doctor July 2026

## User Context (durable)
- 20 years of consistent training history
- Returning from a January 2026 health issue; currently rebuilding base fitness
- Full home gym: weight cage, dumbbells, TRX, fan bike, treadmill, infrared sauna
- New doctor in July 2026 — sports-nutrition / exercise-oriented; possibly data-friendly

## Near-Term Goal
Arrive at the July 2026 doctor visit with a structured baseline: meal template, supplement stack, training plan, genetic-actionable summary, target biomarker order list. The visit becomes high-leverage (real data, productive conversation) instead of generic.

## Key Decisions
- See `decisions/` for individual records
- No diet app — LLM computes macros/micros from `protocols/meal-template.md`
- Markdown substrate, HTML output (per Thariq's HTML-effectiveness argument)
- A → B → C phased build; C designed from observed friction, not speculation

## Status as of 2026-06-14 (S63) — WHOOP/noop ingestion adapter built + wired (read-only sqlite) + model-eval noop-AI-Coach prior art

S63 ran one substantive PR lifecycle (#136) + the close PR, merged to `main` (`9cfbfef`; suite 833/2,
+10 net new whoop tests). Walter: "build the whoop. also, update the model-eval plan to consider
noop's local AI Coach approach." (1) **The WHOOP/noop ingestion adapter is BUILT + WIRED** (`mdzq`
build half) — `scripts/ingest/adapters/whoop.py` replaces the fabricated JSON scaffold with a
read-only (`sqlite3` `mode=ro`) read of noop's documented `whoop.sqlite` `dailyMetric` table, mapping
each non-null metric → `source: whoop` store readings (recovery / strain[0–21] / hrv / rhr /
sleep-efficiency / spo2 / resp-rate / skin-temp-dev). **Mechanism (OQ-2/OQ-3) = read-only sqlite, NOT
MCP** (the file-based `read_readings` contract fits with 0 edits to the ADR-0003 shared
routine/scheduler — the first live-source adapter). Wired by removing the `UNWIRED` marker.
(2) **The model-eval plan** gained §3.5 (+ §4b/§8 pointers): noop's AI Coach (BYO-provider protocol +
OpenAI-compatible local endpoint à la Ollama + consent-gated compact-summary context) as integration
prior art, license-honest (reference, not vendor). (3) **The #136 6-agent review was LOAD-BEARING** —
it caught a real read-only-bypass (URI `mode=ro` defeated by a `?`/`#` in the path; a `#` opened the
wrong file) + two mutation-survive-green test holes (a transposed column→item mapping; the untested
`is None` NULL-skip), all 7 LEGITIMATE fixed + blind-verified, both new guards mutation-proven.
**`mdzq` stays OPEN** — the real-data E2E validation tail (gated on the operator bonding the strap to
noop + a sample) remains; the build + fixture tests + adversarial battery are merged. Beads `crgz`
(doc-freshness: supersede stale whoop-unwired gates) + `ienx` (multi-device fail-loud) created; `1uav`
closed. Next: the adapter's real-data validation, the review beads, the remaining S61 plans, or the
correctness/governance tail. Session detail: `vault/sessions/session-63.md`.

## Status as of 2026-06-14 (S62) — owed S61 close + ADR-0011 D3/D4 propagated + D2 re-decided (noop-source review)

S62 ran four PR lifecycles, all merged to `main` (`d2ec74c`; suite 823/2 + 16/16 wiki-ingest).
Walter: "merge #131 and proceed with (b)", "clear the e64j bead", then a first-party noop-repo review.
(1) **#131** — the owed S61 close docs (3-agent subset; 1 LEGITIMATE quality fix blind-verified).
(2) **#132 — ADR-0011 D3/D4 propagation**: the biomarker `source` enum is now device-agnostic
`wearable` (was `oura`) across all three lockstep sites (`scripts/wiki-ingest-lint.sh` gate +
`vault/biomarkers/_template.md` + `vault/WIKI.md` schema doc), mutation-proven RED→GREEN; LM-02 +
`current-state.md` re-anchored Oura→Whoop; the Oura *adapter* preserved. (3) **#134 — cleared `e64j`**:
the research plan reconciled to the ADR-0011 D4 enum. (4) **#135 — ADR-0011 v2 (D2 RE-DECIDED)**: Walter
flagged that ADR-0011 v1 was authored from noop's README only; a first-party review (noop@`a3f5e39`; 3
critique agents + adjudication) found noop ships a documented schema + a first-party **read-only MCP
server** (`NoopLocalAccess`) the README missed — so **D2 flipped from "manual CSV export" → "consume
noop's read-only MCP server"** (CSV = fallback) + 10 corrected facts (0–21 strain scale, license a/b/c,
single-device bond, fabricated `whoop.py`); the real adapter is beaded. **Process headline: the
PF-S39-01 gated-skill window HELD** — all four PRs got both `/review-pr` AND `/merge` fresh via the
Skill tool (the disclosed S61 recurrence did NOT recur). A prior PF-S6-01-family miss (the
ADR-from-README authoring) was surfaced + remediated, recorded honestly. Next: execute one of the 3 S61
plans (wiki research [resolve §8 D3], local-model eval [operator inputs D2/D3/D5]) or **build the
WHOOP/noop adapter** (beaded — consume noop's read-only MCP, gated on a real noop data sample) or the
correctness/governance tail. Session detail:
`vault/sessions/session-62.md`.

## Status as of 2026-06-14 (S61) — three forward plans recorded (wiki research, Whoop/noop ADR, local-model eval)

S61 was a PLANNING session (no production code) — Walter directed three forward artifacts, each
reviewed + merged to `main` (`0aed727`, which also carries the S60 close; suite 823/2 unchanged):
(1) `docs/research-plan/wiki-population-research-plan.md` — the executable wiki-population plan
(wave-ordered backlog + `/aplus-research` methodology + ingestion contract + per-entry verification
gate) for a parallel session to run; (2) **ADR-0011** — WHOOP ingestion via `noop` (subscription-free,
fully-local; the adapter reads noop's CSV export, plugging into ADR-0003's adapter seam), Accepted;
(3) `docs/model-eval/local-model-evaluation-plan.md` — choose/train the local model for the off-cloud
PII personalization, framed as a **supersession of ADR-0001** (which routes PII to a no-train commercial
API over summaries + explicitly rejected fully-local for V1). The #130 review was LOAD-BEARING — it caught
the eval plan misframing `hil` as an open gap (it is CLOSED by ADR-0001); reframed + blind-verified 5/5.
The #128 review caught 3 accuracy gaps (fixed). The owed S60 close (#127) merged. **Skill-trace deviation
disclosed** (PF-S39-01 recurrence: #129 + #127 merged without a `/review-pr` panel; some merges REST-direct
without a fresh `Skill(merge)` — recorded honestly, not over-attested). Next: execute one of the three
plans (the wiki research [a parallel session], the ADR-0011 D3/D4 propagation build, or the local-model
eval [gated on operator inputs]) or the correctness/governance tail. Session detail:
`vault/sessions/session-61.md`.

## Status as of 2026-06-14 (S60) — the clone-init bd contract documented (vjsw); the correctness tail advances

Two PR lifecycles merged (#125 S59-close docs, #126 the `vjsw` clone-init bd contract; `main` at
`2c49ea8`, suite 823 passed / 2 skipped, +2 from the two new clone tests), every gated skill invoked
fresh (ninth full session under INV-SKILL-TRACE, green). With the dashboard "done" path complete (S58),
forward work continues on the correctness/governance tail; Walter redirected from the governance item
`d3w` to "the correctness tail", and `vjsw` was the one unconditional, cleanly-buildable item
(verify-first deferred `10h`/`1ww`/`e3b` as deferred-by-design). `vjsw`: a fresh clone shipped `.beads/`
without a database (`*.db` gitignored) and the clone contract had zero bd references. Verify-first
against live bd 0.49.0 found the bead's `bd-init-step`/`no-db` fork both wrong — bd self-heals via
auto-import on normal commands (only `bd sync --flush-only` fails first-command), clone commits are
already safe (the PR #107 hook flush-skip), bd is dev-tooling, and `init_instance` is a THIN LEAF
(ADR-0005-T2). So **Option C** (operator-confirmed "C sounds right"): DOCUMENT that `.beads/` is
db-less-by-design dev-tooling (the operator ignores it; a contributor runs `bd init --from-jsonl`);
`init_instance` deliberately leaves bd alone (docstring-only, no subprocess). Recorded in
`docs/clone-init.md`, the `init_instance` docstring, and `decisions/2026-06-14-clone-init-bd-contract.md`;
2 non-tautological tests (mutation-proven RED). The #125 review caught a real residue (the S59
close-correction had missed `session-59.md`, leaving it claiming the close "HELD" while HANDOFF + the
PF log recorded the soft PF-S13-01/S37-01 recurrence) — 3 LEGITIMATE fixed + blind-verified; the #126
review's 5 agents independently verified the Option-C contract's claims against live bd + the hook
source (0 legitimate). The S57/S59 close-step-8/8.7 from-memory miss did NOT recur (this close re-opened
DOCUMENT_RUBRIC + landmarks from the files). Bead `vjsw` closed. Next: the correctness/governance tail
(`d3w` mechanize-close-step-8, `02pe` plan-track revert, `dqyv` 3-consumer promotion, `ofn0`
archive-SHA-check) + P3s; the July-visit prep (LM-01) is date-fixed (visit 2026-07-13; 14-day window
opens 2026-06-29). Session detail: `vault/sessions/session-60.md`.

## Status as of 2026-06-14 (S59) — the sub-AA legend (b6um) FIXED; the render AA gate hardened

Two PR lifecycles merged (#123 S58-close docs, #124 the `b6um` AA fix; `main` at `7253af7`, suite
821 passed / 2 skipped, unchanged — a CSS-token + test change), every gated skill invoked fresh
(eighth full session under INV-SKILL-TRACE, green). With the dashboard "done" path complete (S58),
forward work shifted to the correctness/governance tail, starting with `b6um`: the semantic legend's
`.state-watch` text was `watch #DDAA33` on white = 2.13:1 — sub-AA, violating ADR-0004's unqualified
WCAG-AA commitment. It now renders the AA-dark `watch-text #8A6D1F` (4.90:1) via a new `--watch-text`
`:root` var (= the existing `CHROME["watch-text"]`, no new colour); the legend SWATCH keeps the true
`--watch` amber (the data-state colour cue), pinned by a new positive+negative test assertion pair. The render AA gate
(`test_render.py::test_contrast_and_colorblind`) was extended from `good`-only to all three
state-text-on-paper pairs (mutation-proven RED) so the sub-AA-state-text class cannot reship.
`PALETTE`/`SERIES`/`ACCENTS` byte-unchanged. Verify-first found the bead's "the gate does not measure
state-text pairs" partially stale (it measured `good`-only by deliberate design). The #124 6-agent
review (Security/Bug/Quality/Contracts/Historical 0) confirmed the locked-set immutability + ADR-0004/
ADR-0009-D3 consistency; the test-coverage reviewer caught 2 real coverage gaps (the swatch true-colour
unpinned; a gate-comment failure-mode error) — both fixed + blind-verified. The S58 PF-S51-01
concurrent-mutation watch was MITIGATED (Phase-1 review agents dispatched read-only; the tree stayed
pristine). Bead `b6um` closed. Next: the correctness/governance tail (`d3w` mechanize-close-step-8,
`10h` HALT-filter, `1ww` append-race, `e3b` Wave-5 wiring) + the deferred follow-ups; the July-visit
prep (LM-01) is date-fixed (visit 2026-07-13; 14-day window opens 2026-06-29). Session detail: `vault/sessions/session-59.md`.

## Status as of 2026-06-13 (S58) — the care-team rollup SHIPPED (zone 5); the dashboard "done" path is COMPLETE

Two PR lifecycles merged (#121 S57-close docs, #122 the care-team rollup; `main` at `afd40a8`,
suite 821 passed / 2 skipped, +36 from session open), every gated skill invoked fresh (seventh full
session under INV-SKILL-TRACE, green). The THIRD and LAST of the three remaining "done"-path
dashboard data models shipped: `scripts/store/care_team_rollup.py` is a READ-MODEL (no new store
stream) attributing each store reading to a specialist (by stream prefix or calendar event category)
and reducing it to a per-specialist 30-day RECORDED-DATA freshness status (green ≤30d / amber 31–60d /
grey >60d-or-none; future scheduled events excluded — they are activity in Zone 2, not recorded data).
The dashboard `_care_team_zone` renders a data-state status dot (PALETTE good/watch/muted, never an
accent — ADR-0009 D3) + a muted recency caption; all 16 specialist cards render, the ~10 streamless
read the honest grey "no data yet", an all-empty store keeps the static "no rollup yet". Built from the
signed zone-5 anatomy + the new decision note `decisions/2026-06-13-care-team-rollup-zone5-mapping.md`
(the design-then-build recorded the unsigned specialist→stream mapping + the 30-day rule BEFORE
building); Walter confirmed option (a) — all-16, honest grey. **With this the dashboard is
no-placeholder except the wearable surface (LM-02, operator-gated on Walter's Oura data).** The #122
6-agent review (Security 0, Contracts 0) caught a real HONESTY defect in the orchestrator's own
same-session decision note (a future event made a specialist read "updated today") → refined to exclude
future from freshness + flagged to Walter; 3 doc/test nits fixed + blind-verified. PII boundary
unchanged; `PALETTE`/`SERIES`/`ACCENTS` byte-identical. Bead `ektw` closed. Next: the
correctness/governance tail + the deferred follow-ups (`dqyv`, the archive-SHA-check) — the done-path
dashboard is complete. Session detail: `vault/sessions/session-58.md`.

## Status as of 2026-06-13 (S57) — the calendar-event data model SHIPPED (zone 2 This Week)

Two PR lifecycles merged (#119 S56-close docs, #120 the calendar-event data model; `main` at
`b74ee0f`, suite 785 passed / 2 skipped, +25 from session open), every gated skill invoked fresh
(sixth full session under INV-SKILL-TRACE, green). The second of the three remaining "done"-path
dashboard data models shipped: `scripts/store/calendar_schema.py` is a new `calendar::events`
content-tagged store stream (`{category ∈ training/lab-draw/check-in/appointment, label}`, date-keyed;
distinct same-date events persist, identical re-entry idempotent; corrections by re-recording; the
store-adversarial battery proven RED per dedupe field), and the dashboard routes `calendar::events`
into zone 2 — category-tinted event pills land in each matching month-calendar day cell, the honest
awaiting caption shows only when no events are stored — built strictly from the signed
`dashboard-v1-visual-spec.md` zone-2 anatomy. The awaiting-zone count dropped by one (calendar events
now render from data). The session PIVOTED from the operator-recommended 30-day-rollup to
calendar-events after verify-first found the rollup needs UNSIGNED design (the specialist→metric
mapping + aggregation rule; the spec signs only "a colored per-domain status line") — PF-S6-01 +
PF-S49-01 working. The #119 review caught + fixed an off-main-archive-SHA recurrence (count=2 watch +
a structural-fix bead); the #120 6-agent panel (Security 0, Bug Hunter 0, Contracts 7 positive)
correctly REFUTED two of its own findings. PII boundary unchanged; `PALETTE`/`SERIES`/`ACCENTS`
byte-identical. Bead `86vu` closed; `dqyv` updated (calendar = 3rd `_reading` consumer, the trigger
fired); the archive-SHA-check bead filed. Next: the 30-day-rollup (zone 5 — a DESIGN-then-build), then
the correctness/governance tail. Session detail: `vault/sessions/session-57.md`.

## Status as of 2026-06-13 (S56) — the goal data model SHIPPED (zone 6 Goals & Progress)

Two PR lifecycles merged (#117 S55-close docs, #118 the goal data model; `main` at
`8455608`, suite 760 passed / 2 skipped, +38 from session open), every gated skill invoked
fresh (fifth full session under INV-SKILL-TRACE, green). The first of the three remaining
"done"-path dashboard data models shipped: `scripts/store/goal_schema.py` is a new
`goal::<slug>` store stream (label/baseline/current/target[/unit]; a read-derived
direction-agnostic percent clamped 0-100 and never rounding up to a false "100%";
append/correct split; the store-adversarial battery proven RED per dedupe-identity field),
and the dashboard routes `goal::` into zone 6 — populated rows (label / percent /
good-green fill) + the July-visit landmark note card, the honest empty state otherwise —
built strictly from the signed `dashboard-v1-visual-spec.md` zone-6 anatomy (no new Pencil
round). The awaiting-zone count dropped by one (goals now populates from data). The #118
6-agent review was load-bearing: it raised an impact-5 BUG-1 (render-crash on a
malformed-conformant store line) that the blind triage REFUTED (plan_schema crashes
identically — the shared store-trusts-writer posture; the fix would be unapproved
defensive programming) and caught two false mutation-RED test docstrings (the source-field
dedupe contribution was untested) — fixed + re-proven RED. PII boundary unchanged
(`SUMMARY_FIELD_SET`+`EXCLUDED_RAW_PII` byte-identical); `PALETTE`/`SERIES`/`ACCENTS`
byte-identical. Bead `1oag` closed; HIST-2 filed (bead `dqyv` — promote `loop_schema._reading` to a
public store constructor — the two-consumer trigger). Next: the calendar-event (zone 2) +
30-day-rollup (zone 5) data models, then the correctness/governance tail. Session detail:
`vault/sessions/session-56.md`.

## Status as of 2026-06-13 (S55) — the #112 architecture debt PAID DOWN (y91q/z2d0/smei)

Two PR lifecycles merged (#115 S54-close docs, #116 the #112 architecture debt + the `juc`
validity pin; `main` at `b0e1a52`, suite 722 passed / 2 skipped, +12 from session open), every
gated skill invoked fresh (fourth full session under INV-SKILL-TRACE, green). The
report↔dashboard↔loop_schema coupling debt (Top-3 #1 for two sessions) is PAID DOWN: `report.py`
no longer imports five private cross-module symbols — `dashboard.py`'s four formatters
(+ `MONTH_ABBR`) are now the PUBLIC `component_set` API and `loop_schema.panel_pending` is the
published pending predicate, both pinned by a regression test (`y91q`). `read_panel`/
`panel_pending` are recurrence-aware — a re-recommended panel reads `pending` again — via the
both-sides timepoint bracket single-sourced through `_latest_result`+`_re_recommended`; all 5
pinned `read_panel` contracts preserved (`z2d0`). A load-time tripwire pins that every in-range
`_POLARITY_FEED` marker carries a `reference_range` (`smei`). The #116 6-agent review found
BUG-001 — a backdated-second-result false-pending in z2d0, PROVEN unfixable by any read-model
heuristic (the store sorts by timepoint and drops append order) — blind-triaged DEFERRED, beaded
`pq7m`, documented as the z2d0 decision note's second known limitation; LATENT (the panel data-in
loop has no production writer). PII boundary unchanged (`SUMMARY_FIELD_SET`+`EXCLUDED_RAW_PII`
byte-identical); `PALETTE`/`SERIES`/`ACCENTS` byte-identical. Beads `y91q`/`z2d0`/`smei` closed;
`pq7m` filed. Next: the correctness/governance tail + the goal / calendar-event / 30-day-rollup
data models (the remaining "awaiting" dashboard zones).

## Status as of 2026-06-13 (S54) — the juc worst-wins recent-trend-direction router SHIPPED

Two PR lifecycles merged (#113 S53-close docs, #114 the `juc` router; `main` at `13f5814`,
suite 710 passed / 2 skipped, +13 from session open), every gated skill invoked fresh (third
full session under INV-SKILL-TRACE, green). The one decided-but-unbuilt mechanism carried out
of S53 is now built: the plan-reasoning summary's `recent-trend-direction` is derived
registry-driven WORST-WINS (regressing > improving > flat) over the `biomarker::` polarity
feed — `_POLARITY_FEED` = every `biomarker_meta.METADATA` marker with a non-None
`good_direction` — via `router._recent_trend_direction` reusing `_trend_token` untouched, with
a load-time juc tripwire (feed within the registry-polarity set, disjoint from
`SUMMARY_FIELD_SET` + `EXCLUDED_RAW_PII`, output pinned to `TREND_DIRECTIONS`). This unblocks
plan-reasoning over changing labs (the S39 fail-closed raise). The PII boundary is unchanged in
posture: `SUMMARY_FIELD_SET` + `EXCLUDED_RAW_PII` byte-identical, `_trend_token` AST
byte-identical, `raw-lab-values` de-plumbed from `_RAW_TO_FIELD` but retained as a
named-excluded class. The registry is now DUAL-SURFACE — a `good_direction` edit changes both
the dashboard chips and the model-bound summary token. Bead `juc` closed; follow-up `smei`
(in-range feed-marker `reference_range` validity pin) filed. Built EXACTLY from the signed
decision note `vault/decisions/2026-06-12-juc-trend-polarity-design.md`; ADR-0008 D4 +
Consequences amended `[2026-06-13]`; `vault/components/plan-layer.md` reconciled. Next:
the `y91q`/`z2d0` architecture debt + the correctness/governance tail.

## Status as of 2026-06-13 (S53) — all three visual packages SHIPPED; stats+plans+tracking completion bar met

Five PR lifecycles merged (#108-#112; `main` at `a148316`, suite 697 passed / 2 skipped,
+208 from session open), every gated skill invoked fresh (second full session under
INV-SKILL-TRACE, green). The three signed visual packages shipped: **Package A** (`1oh`) —
`scripts/store/plan_schema.py` per-domain `plan::`/`plan-track::` day-keyed plan + tracking
schemas (ADR-0010) feeding the populated zone-3 plan cards (workout/nutrition/supplements/
peptides); **Package B** (`y0h0`+`i2yw`) — zone-4 trend cards carrying reading date,
ref-range/state caption, numeric polarity-tinted delta, and a dashboard-only naive
projection (derivation single-sourced as `biomarker_meta.projection_values`); **Package C**
(`nsxy`) — `report.py` redesigned as the standalone physician face sheet on the v3
standardized token set. The design system gained additive SYSTEM tokens (`SECTION_ACCENTS`
biomarkers/goals + CHROME `watch-text`/`watch-tint`) — locked `PALETTE`/`SERIES`/`ACCENTS`
byte-identical, dashboard + report unified on one token vocabulary, AA gate extended to
non-text WCAG 1.4.11 pairs. The `juc` per-marker trend-polarity design was adjudicated and
recorded (`vault/decisions/2026-06-12-juc-trend-polarity-design.md`); the worst-wins router
mechanism it specifies is DECIDED, not yet built (S54). **Walter's completion bar — a
dashboard that presents stats AND plans AND tracking, plus a physician handout — is met.**
Remaining: the `juc` router mechanism, the 30-day-aggregate/goal/wearable data models, the
architecture-debt beads (`y91q`/`z2d0`), the correctness/governance tail, and the
library-population track. Session detail: `vault/sessions/session-53.md`.

## Status as of 2026-06-12 (S52) — all visual targets signed; hooks worktree-aware; skill-trace audit live

Six PR lifecycles merged (#102-#107; `main` at `e8b0dd8`, suite 489 passed / 2 skipped),
every gated skill invoked fresh (first mechanically-audited attestation under the new
INV-SKILL-TRACE + `scripts/skill-trace-audit.sh`, registered this session by operator
ritual). Landed: router clone-isolation pin (`e3b` T1; T2 wiring verification keeps the
bead open); store correction path (`store.correct` superseding-append + latest-wins
`_resolve_latest`, ADR-0002 v1.4); the skill-trace close audit + store-adversarial
checklist; the 9-entry negative-example denylist default-wired into deploy-gate row 10
fail-closed — content-reviewed by the deployed Role 4 and adjudicated `conditions-met`
by Role 7, the first end-to-end run of the three-gate medical pipeline (provenance:
`vault/decisions/2026-06-12-denylist-role4-review-provenance.md`); and worktree-aware
commit hooks (`lib/resolve-target-repo.sh` — trunk-scoped gates, db-gated PII
flush-before-scan closing the `ycqo` pending-text window for main-checkout commits).
**The S51 design-input debt is cleared: all four visual targets are operator-signed and
recorded** — `1oh` plan zone + `y0h0`/`i2yw` trend-card v2 in
`vault/design/dashboard-v1-visual-spec.md` `[AMENDED 2026-06-12]` (projection readout
dashboard-only by operator decision), and the `nsxy` physician face sheet as
`vault/design/physician-facesheet-v1-spec.md`. Visual packages A/B/C build S53 from
those targets. Session detail: `vault/sessions/session-52.md`.

## Status as of 2026-06-12 (S51) — data/correctness layer hardened (ultracode build fan-out)

Five build units merged through full review lifecycles (PRs #97-#101; `main` at `f0c54ff`,
suite 461 passed / 2 skipped): the scheduler's wired-set membership is a typed `UNWIRED`
attribute contract; the store publishes `items()`/`read_all()` (single enumeration owner,
empty-item round-trip fixed, exception propagation pinned); the PII commit boundary scans
bd bead content (with precisely-scoped headers — the pending-in-db window remains until
bead `ycqo`, operator-approved for S52) and `scan`/`scan_text` use `token_config` with a
guarded deprecation alias; the ADR-0007 panel loop has its result side (`record_panel_result` +
source-tag-provenance `read_panel`, landed results render as escaped value rows); fail-fast
storage contracts are docstring+test pinned (`r5l`/`u8u` convention defaults). Eleven build
beads closed + `2kk` adjudicated closed; operator adjudications recorded on `1vi`/`pka`/
`pmp`/`e3b`/`juc`/`1ww`. Dashboard zones still awaiting data models (unchanged): plans
(`1oh` + nutrition content), wearable LM-02, calendar events, goals, rollup; `y0h0`/`i2yw`
residuals + the `nsxy` report design pass open — all gated on the S52 design-input batch
(PF-S49-01). Session detail: `vault/sessions/session-51.md`.

## Status as of 2026-06-11 (S50) — dashboard DESIGNED SURFACE complete incl. calendar zone

The dashboard (S46-S50 arc) now renders the signed-off designed app surface from `generate.run("dashboard")`: ADR-0008 data layer (S48), ADR-0009 7-zone visual shell + the mock's visual language (S49, PRs #92/#93, build target `vault/design/dashboard-v1-visual-spec.md` — the PII-safe transcription of the operator-held mock), and the finished calendar zone (S49 build / S50 review, PR #94): a real month-calendar table where the visible week IS one month row, with a zero-script, keyboard/AT-operable in-place month reveal. Honest awaiting states (digit-free, mechanically guarded) hold in the five zones whose data models are unbuilt: plans (`1oh`, next slice — includes the nutrition card's meals/water/macro content), wearable scoring (LM-02), calendar events, goals, per-specialist rollup. Suite 451 passed / 2 skipped on `main`; the render AA gate measures every tint pair plus the base ink/muted-on-paper and calendar today/other-month cell pairs (state-colored legend text is outside the gate). Remaining dashboard residuals: `y0h0` (dates/ranges/deltas on trend cards), `i2yw` (projection readout), the physician-report design pass. Session detail: `vault/sessions/session-48.md` … `session-50.md`.

## Status as of 2026-06-10 (S45) — V1 BUILD COMPLETE (18/18); Track-1 PII/safety COMPLETE

The V1 build is complete (18/18, see the S42 block below). Post-build, the **Track-1 PII/safety boundary is now complete end-to-end**: the runtime value scanner (`pii_scan.scan_text`, fed by `router.summarize`) detects every `EXCLUDED_RAW_PII` class incl. postal (S44 `g5x` email/phone/NFKC; S45 `nue` precise ZIP/state-anchored postal); and that boundary is ENFORCED at the commit layer (`block-pii-commit.sh` REGISTERED in `settings.json`, S45 `3lv`) and the push layer (`pre-push-pii-scan.sh` backstop, installed for clones by `init_instance`, S45 `dv3`). Contact detection is operator-specific + config-driven (gitignored `vault/meta/operator-contact.txt`; the generic `@gmail.com` trunk pattern that flooded on fixtures/beads was removed), so the trunk stays clone-portable. Suite 340 passed / 2 skipped; shell suites green (block-pii 53 / commit-matcher 30 / settings-hook-paths 15 / pre-push 14 / commit-main 30 / ungated 14); branch-completeness 0 (20 agents). **Deferred to S46:** `am4` (ADR-0005 v1.5 freshness sweep), the dashboard demo with synthetic data (toward Walter's "great dashboard" goal), Track-2 V1 data-surface correctness beads, and the email-in-history remediation (`46m`). No artifact generates until `generate.run` is fed real operator data (LM-04, Walter-pending).

## Status as of 2026-06-07 (S42) — V1 BUILD COMPLETE (18/18)

The V1 build executed `docs/build-plan/build-plan-v1-full.md` (18 tasks across 7 topological waves) — **all 18 leaves built + merged; the build plan is fully drained.** Verified sound against every build-plan checkpoint (full suite 272 passed / 2 skipped; Wave 2→3 + 3→4 + 4→5 + 5→6 + 6→7 + 7→Done checkpoint gates green; 0 dangling references). S42 completed Wave 7 (the terminal DAG sink) via `/execute-plan` WAVE mode (Phase C) — the three-tier review caught + fixed a **dishonest mid-series projection** (mislabeled "naive projection from recent trend" — safety-adjacent) + a **tautological size-cap assertion** + a degenerate render row + missing projection-value/escaping safety tests the builder's tests + all of Tier-2 missed, before the W7→Done checkpoint gate (the SIXTH consecutive wave a safety/honesty surface was caught only by the layered Tier-3 review). No artifact generates until `generate.run` is fed real operator data (LM-04, Walter-pending).

- **Wave 1** — PII-boundary / store-keying / render-size spikes — ✅ complete (`394`, `bez`, `qbb`)
- **Wave 2** — NDJSON store + egress/PII guard — ✅ complete (`89a`, `e9m`)
- **Wave 3** — ingest routine, render engine, gitignore-hook, router spike — ✅ complete: `6be`+`gu4` (prior) + `xlu` (0005-T1) + `br1` (0006-T0 spike) built S38
- **Wave 4** — adapters, matrix render, cron entry, clone-init, router impl — ✅ complete: `n9h`+`3gp` (prior) + `yo6` (0004-T2 matrix render) + `ml1` (0005-T2 clone-init) + `ftm` (0006-T1 no-train router) built S39 (PR #66)
- **Wave 5** — scheduler + plan assembly — ✅ complete: `oaf` (0003-T3 scheduler) + `8cv` (0006-T2 multi-domain plan assembly — reasons over the `ftm` router summary; fail-closed class-aware HALT) built S40 (PR #69). Tier-3 caught + fixed a Critical HALT compound-limit fail-open; residuals `8j6` P1 / `10h` / `7lt` / `e3b` / `20d` beaded (LM-04-gated)
- **Wave 6** — lab-loop store schemas — ✅ complete: `1aa` (0007-T1 `loop_schema`) built S41 (PR #71); publishes the 4+1-state contract (`pending`/`not-yet-answered`/`no-prior`/`answered-over-time`/`no-data`) W7 reads 1:1; Tier-3 caught + fixed a cross-stream collision + a same-timepoint dedupe-drop; residuals `s38` P2 (result-writer) / `r5l` P3 / `pka` P2 / W7 None-sentinel beaded
- **Wave 7** — biomarker matrix/projection views — ✅ complete: `1ih` (0007-T2 `render_views`) built S42 (PR #73 → **V1 18/18**); the terminal DAG sink — recomputes matrix + naive projections from `store.read`, maps the `loop_schema` 5-state contract 1:1, paginates under the cap; Tier-3 caught + fixed a dishonest mid-series projection + a tautological size-cap; residuals `5q5` P2 (render.py reconciliation) / `byj` P2 (resulted-panel render) beaded

Execute-stage protocol: `/execute-plan` in wave mode, adopted S36 after **PF-S36-01** (the build had been hand-rolled per-task off the wave schedule from S32 — outputs verified undamaged, but the wave-checkpoint discipline lapsed). Re-entry completes the open waves in order; Phase B (S37) cleared `5wo`/`qwj` (the W3/W4 design blockers — `5wo`→caller-orchestrated pagination preserving `emit -> Path`, `qwj`/`ko5`→ADR-0005 "PII-free = health-data-free" clarification); Phase C built W3 (`br1`+`xlu`) at S38, W4 (`yo6`+`ml1`+`ftm`) at S39, W5 (`oaf`+`8cv`) at S40, W6 (`1aa` `loop_schema`) at S41, and W7 (`1ih` `render_views`, the terminal sink) at S42 via `/execute-plan` wave runs (three-tier review + checkpoint gate each) — **the V1 build is now COMPLETE (18/18); the wave loop is finished, there is no Wave 8.** Forward work is the post-build residual-bead group (`pka` prioritized) + LM-04 + the library-population `/aplus-research` track, not another `/execute-plan` wave. The no-train router PII boundary (`ftm`) AND the multi-domain plan assembly (`8cv`, the V1 PII-trust + fail-closed class-aware HALT task) are now BUILT before any further plan-reasoning task; the in-summary pass-through PII value-gate (`8j6` P1) is the tracked LM-04-gated residual. No actual artifact generates until `generate.run` is fed real operator data (LM-04 pending). Prior session titles (S32-S35) use the old ADR-family wave labels and are NOT retro-corrected — cross-reference the build-plan wave numbers here, not the archived session titles. The S2/S1 snapshots below are historical.

## Status as of 2026-05-23 (S2 close)
- Wiki schema layered onto operational vault (`vault/WIKI.md`)
- Agent-shared context layer in place: operator-profile, current-state, goals, contradictions, index, log
- Source whitelist + entity templates (compounds, biomarkers) authored
- `aplus-research` project-local skill built with 6 mechanically enforced gates; never invoked end-to-end yet
- First compound library entry (BPC-157) exists at `vault/library/peptides/bpc-157/` + `vault/compounds/bpc-157.md` — **suspect**, scheduled for re-run via `aplus-research` next session (the original deep-research dispatch did not follow protocol; entry may contain hallucinations/fabrications)
- All `protocols/` files still placeholders awaiting Walter's input (unchanged from S1)
- 23andMe analysis pending raw file (unchanged from S1)
- Oura purchase pending (unchanged from S1)
- No bloodwork yet (none ordered until July 2026 visit)

## Status as of 2026-05-16 (S1 close)
See `vault/sessions/session-1.md` for the initial vault-skeleton + project-identity work.