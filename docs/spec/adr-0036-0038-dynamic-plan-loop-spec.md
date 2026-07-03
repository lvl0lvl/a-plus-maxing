---
scope: "ADR-0036 ADR-0037 ADR-0038 (dynamic, personalized, time-horizon plan loop)"
adrs: [ADR-0036, ADR-0037, ADR-0038]
tier: 4
created: 2026-07-03
status: draft
---

# Spec: Dynamic Plan-Evolution Loop + Time Horizons + Care-Agent Tailoring (ADR-0036/0037/0038)

## Component Overview

This spec implements the three dynamic-plan-loop ADRs that close the `plan → act → measure → adjust` loop `design/vision.md` names and personalize the plan against the operator's real data. It delivers three composable capabilities in the design's build order (`design/dynamic-plan-loop-design.md` §5: loop → horizons → tailoring): (1) an automated plan-evolution loop that RE-ENTERS the front-door generation on a debounced trigger — `run_orchestrated` → `plan_driver.drive` → the composed `gate_dispatch` + `orchestrate.generate_plans` cross-domain reconciliation ([plan_orchestrator.py:127](../../scripts/plan/plan_orchestrator.py), [plan_driver.py:144](../../scripts/plan/plan_driver.py)) — producing a NEW dated plan for ALL domains that passed the FULL safety composition (ADR-0036); (2) time horizons COMPOSED over the three existing schema owners (`goal_schema`, `calendar_schema`, the ADR-0010 D2 open-on-extras seam) with a date-range query over the dated `plan::` history, introducing zero new store schema (ADR-0038); and (3) a care-lane tailoring pass that personalizes each cleared, non-held plan with the operator's raw data and renders ONLY into the gitignored `maintained` artifact through five mechanical gates (ADR-0037).

The architectural rationale is fixed by the ADRs. ADR-0036 re-runs the front door instead of the per-domain `adjust.py` ([adjust.py:52,144](../../scripts/plan/adjust.py)) so every evolved plan sees the same ADR-0028 composed `gate_dispatch` (judge + safety lenses + fail-closed `safety_passed is True` + liaison adjudication) AND the five `orchestrate` cross-domain holds as the first plan — closing the per-domain safety gap (finding A). Re-entering the driver re-summarizes the store, which re-derives `recent-trend-direction` from the `biomarker::` polarity feed ([router.py:464,326](../../scripts/plan/router.py)) so a wearable/lab trend reaches the re-generation with no bridge to `plan-track::` (finding B). The free-text trigger routes only through the care agent's gated capture ([care_chat.py:284](../../scripts/serve/care_chat.py) → [capture.py:320](../../scripts/serve/capture.py)) so raw operator text is structurally incapable of reaching the specialist dispatch (finding C). ADR-0038 composes horizons rather than storing a `plan-arc::` stream, keeping each fact in its one owner. ADR-0037 amends ADR-0001's raw-egress list with a named, mechanically-floored tailoring carve-out rendered only to the local artifact.

How it fits: the loop CONSUMES built infrastructure and extends it without rebuilding the inner engine. The A′ subscription driver (ADR-0026) and the composed `gate_dispatch` (ADR-0028) are the front door the loop re-enters; the maintained re-emit lifecycle (ADR-0025, [maintained.py:245](../../scripts/generate/maintained.py)) is the single writer the tailoring pass reuses; the care-lane gated capture (ADR-0034/0035, [capture.py:80-99](../../scripts/serve/capture.py)) is the de-id boundary the free-text trigger rides. Today the serve layer's only plan-generation path is `_do_generate_plan` ([server.py:592](../../scripts/serve/server.py)), which calls `orchestrate.generate_plans` DIRECTLY at [server.py:678](../../scripts/serve/server.py) with NO reauthor/adjudicator hook (the screened-only, held-stays-held path) — so wiring the automated serve trigger to the driver front door (NOT that screened route) is a stated BUILD PREREQUISITE (ADR-0036 OQ-3 / RT-06), realized as the entry task everything else depends on.

Every task is mock/fixture-satisfiable at 0 live spend, driven through the SERVE entry point with a fixture `dispatch`; the reasoning-quality of the de-load/tailoring prose is a PR-documented manual live dispatch, never a CI assertion (the `test_adjust.py` convention, `design/dynamic-plan-loop-design.md` §4). The operator-present LIVE subscription run — real key + real data + spend — is the downstream operator-gated attestation AFTER this build, recorded in the Unresolved Concerns table, not a task.

Informing artifacts (downstream workers load on demand): the three source ADRs (`docs/adr/ADR-0036-automated-plan-evolution-loop.md`, `ADR-0037-care-agent-plan-tailoring.md`, `ADR-0038-plan-time-horizons.md`), the vetted design (`design/dynamic-plan-loop-design.md`), the set DAG (`docs/adr/.pipeline/dag.md`), and the format-exemplar specs (`docs/spec/adr-0028-gate-dispatch-control-inversion-spec.md`, `docs/spec/adr-0020-0025-plan-gen-engine-spec.md`).

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0036 OQ-3 (RT-06) | Open Question (BUILD PREREQUISITE) | The automated serve trigger MUST bind to the full-composition front door (`run_orchestrated` → `plan_driver.drive` → `gate_dispatch` + `orchestrate.generate_plans`), NOT the screened-only `_do_generate_plan` route that calls `generate_plans` with no reauthor/adjudicator hook ([server.py:678](../../scripts/serve/server.py)). | **Block** | Finding-A safety-parity FAILS outright if the trigger reaches the screened-only path. Prerequisite task **ADR-0036-T1** builds the serve-trigger→driver front-door binding + the mechanical anti-degradation guard; every other ADR-0036 task and both ADR-0037 hook tasks depend on it. Direction is decided in the ADR; this is a build task, not a spike. |
| ADR-0036 OQ-1 | Open Question | Concrete debounce parameters — the minimum re-generation interval, the sustained-signal window/threshold over the `biomarker::` series (n readings, span, directional-consistency bar), and the free-text rate limit. | **Proceed** (T2 pins the numbers) | The DECISION (re-run the front door on a debounced sustained signal, never a single reading) is fixed. The concrete thresholds are a spec-stage mechanic set as ADR-0036-T2's binary ACs (min interval, window n/span, rate limit) and pinned by a deterministic unit test of the threshold/window function. |
| ADR-0036 OQ-5 (RT-08) | Open Question | Where the debounce STATE lives (last-re-gen marker + the sustained-signal window buffer) and through what seam MEASURE-leg adherence reaches the re-gen. | **Proceed** (T2 state; T4 adherence seam) | The debounce state introduces NO new stored stream: the last-re-gen date is DERIVED from the dated `plan::` history ([plan_schema.py:462](../../scripts/store/plan_schema.py)) and the window is a query over the `biomarker::` series — T2 states and tests this. The `plan-track::` → re-gen adherence bridge (`resolve_plan_progress`, [track.py:81](../../scripts/plan/track.py)) is NAMED as a separate additional input in T4, so the "separate, additional input" claim is not left dangling. |
| ADR-0036 OQ-2 | Open Question | The concrete runnable trigger surface at the serve layer (cadence timer, `biomarker::` write-event hook, care-chat capture completion) and how each converges on the single driver call without duplicating the debounce. | **Proceed** (T1 route + T2 convergence) | The firing SITE (serve entry point) and the single action (re-enter the driver) are fixed. T1 adds the serve route; T2 wires the three call-sites (`route.route_upload` [route.py:166](../../scripts/serve/route.py), `confirm.land_confirmed` [confirm.py:78](../../scripts/serve/confirm.py), care-chat capture completion) through ONE shared debounce gate. |
| ADR-0036 OQ-4 | Open Question | How a large re-generation surfaces for operator confirmation vs swaps silently — the "what changed and why" rationale + large-change confirmation. | **Proceed** (T4) | The decision requires a plain-language rationale per re-gen and large changes to surface for confirmation rather than silent swap; T4 records the rationale and routes a large-change to the confirmation surface (reusing the `confirm.py` request-shape precedent). The large-change threshold is a T4 binary AC. |
| ADR-0036 Consequences-Negative-1 | Unmitigated Risk | Re-running the full front door every trigger is materially more expensive than a per-domain patch. | **Proceed** (debounce bounds frequency) | The debounce (T2 min interval + sustained-signal window) is the bound on trigger frequency. The per-trigger cost is real and permanent; the subscription rate/concurrency ceiling is an operator/billing fact confirmed at the downstream live run (a Review trigger), not a build blocker. |
| ADR-0036 Consequences-Negative-3 (RT-09) | Unmitigated Risk | Whole-plan re-gen densifies the day-keyed `plan::` history ADR-0038's date-range query reads (several same-window dated plans). | **Proceed** (ADR-0038-T3) | ADR-0038-T3's date-range query resolves same-window selection by latest-in-window (mirroring the today-by-date-equality rule at [plan_schema.py:486](../../scripts/store/plan_schema.py)); the debounce bounds the density. Handled by construction in the horizon query. |
| ADR-0036 Consequences-Negative-2 | Unmitigated Risk | Whole-plan re-gen day-keys every domain (including unchanged ones); the operator sees a full re-plan rather than a targeted per-domain delta. | **Proceed** (accepted cost) | Inherent to the front-door re-entry chosen over per-domain `adjust.py` (the deliberate finding-A safety-parity trade): re-running the whole composition is what re-derives clearance for every domain each re-gen, so a whole-plan re-key is unavoidable. The operator-facing "full re-plan, not a delta" surface is softened by ADR-0036-T4's plain-language rationale (what changed and why) + the large-change confirmation gate, but the whole-plan re-key itself is accepted, not erased. No task removes it. |
| ADR-0038 OQ-2 | Open Question | Date-range window boundaries (fixed calendar week/month vs rolling window) AND which reading is "the block" when the loop leaves multiple dated plans in one window. | **Proceed** (T3) | Both are the same date-predicate widened from the equality resolution; ADR-0038-T3 fixes the boundary definition and the latest-in-window selection as binary ACs. |
| ADR-0038 OQ-1 / OQ-3 / OQ-4 | Open Question | Horizon-extra key set/naming; per-week expectation sourcing; open-ended-goal cycle length. | **Proceed** (T1/T2/T3) | All ride the D2 open-on-extras seam or a derivation with no new stored stream, so the no-new-schema decision holds regardless. T2 names the enrichment keys; T3 sources the expectation via the D2 seam; T1 presents rolling cycles for a deadline-less goal. |
| ADR-0038 Consequences-Negative-2 | Unmitigated Risk | No single materialized `plan-arc`/horizon object exists; the four-horizon view is composed at read time from three schema owners + the date-range query. | **Proceed** (accepted cost) | The deliberate no-new-store-schema decision (Alternative C rejected): each horizon fact stays in its one owner (`goal_schema` / `calendar_schema` / the D2-enriched `plan::` history) rather than duplicated into a materialized arc that could drift out of sync. The read-time composition cost (ADR-0038-T3's date-range query) is accepted as the price of zero schema duplication; no task materializes an arc object. |
| ADR-0037 OQ-1 / OQ-4 | Open Question | Where the tailoring pass hooks in the driver→`reemit_maintained` lifecycle; idempotency per `(plan, date)` under the loop re-run. | **Proceed** (T1 hook + emit-gate) | RESOLVED-IN-PRINCIPLE: the pass hooks post-`record_plan`/post-promote and renders only through `reemit_maintained` ([maintained.py:245](../../scripts/generate/maintained.py)); idempotency per `(plan, date)` is provided by the emit-gate reading recorded state (§1) + degrade-to-safe (§4), reusing `_preserve_prior_content` ([maintained.py:180](../../scripts/generate/maintained.py)). |
| ADR-0037 OQ-2 | Open Question | The concrete dosing-token lexicon (§2) + the deterministic interaction rule (§3) and its sync with ADR-0034's `rx-interaction-classes`. | **Proceed** (T2) | The lexicon is a curated keyword set and the rule is deterministic, both testable via the paired control; ADR-0037-T2 grounds the rule on `router.rx_interaction_class_set` ([router.py:198](../../scripts/plan/router.py)) + the existing BPMH/additive-AE lenses ([orchestrate.py:168,262](../../scripts/plan/orchestrate.py)). |
| ADR-0037 OQ-3 / RT-01 | Open Question (corpus/scan) | The ADR-0021/0025 operator-NAME scan-scope hole on the tailoring-enriched artifact (`vault/artifacts/generated/`). | **Proceed** (with note — do NOT re-block) | The gross hole is CLOSED in code: `vault/artifacts/generated/` IS in `DATA_BEARING_PREFIXES` (design finding J OUTDATED; the ADR-0021-T0-SCANSCOPE task landed). Residual: ADR-0037-T3 adds a pre-ship check that the commit/push PII scan detects the reinserted NAME (not only contact tokens) in the enriched artifact — a check, not a gating blocker. Not re-blocked. |
| ADR-0037 Consequences-Negative-1/2 | Unmitigated Risk | A second raw-egress surface to audit; the tailored plan lives only in the local artifact, not the shareable dashboard. | **Proceed** (documented + T3 audited) | Accepted as the deliberate cost of keeping raw PII off every tracked surface. The second surface is audited by ADR-0037-T3's wire-scan + load-time tripwire; the local-artifact-only limitation is documented, not erased. |
| ADR-0036/0037/0038 Validation (LIVE run) | Open Question (downstream) | The operator-present LIVE subscription run — real key + real data + spend; clinical reasoning-quality of the de-load + tailoring prose. | **Defer** | Operator-present, operator-gated (a spend decision), AFTER this build. Every AC here is mock/fixture-satisfiable at 0 live spend; reasoning-quality is a PR-documented manual live dispatch, never a CI test. Recorded; no task. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/serve/plan_loop.py` | Create | The automated loop: the debounced trigger convergence + the front-door binding (`run_orchestrated`/`plan_driver.drive`, NOT `_do_generate_plan`) + the anti-degradation guard + the post-promote rationale/confirmation/tailoring-hook/adherence-input seams. |
| `scripts/serve/server.py` | Modify | Add the serve route entry that fires the loop tick (cadence/manual) into `plan_loop`, dispatched from the `do_POST` string-equality chain ([server.py:159](../../scripts/serve/server.py)); the loop route drives the driver front door, never `_do_generate_plan` ([server.py:592](../../scripts/serve/server.py)). |
| `scripts/serve/route.py` | Modify | On the wearable-land path, after `biomarker_mirror.mirror_registered` ([route.py:166](../../scripts/serve/route.py)), notify `plan_loop`'s debounced entry (the `biomarker::` write-event trigger). |
| `scripts/serve/confirm.py` | Modify | On the confirmed lab-land path, after `biomarker_mirror.mirror_registered` ([confirm.py:78](../../scripts/serve/confirm.py)), notify `plan_loop`'s debounced entry (the `biomarker::` write-event trigger). |
| `scripts/serve/care_chat.py` | Modify | On care-chat capture completion (`respond`, [care_chat.py:239](../../scripts/serve/care_chat.py)), notify `plan_loop`'s debounced entry with the derived tokens only (the free-text trigger, rate-limited). |
| `scripts/plan/horizons.py` | Create | The horizon composition read/query layer over `goal_schema` (derived milestone %) + `calendar_schema` (dated cadences) + the D2-enriched `plan::` history (date-range week/month query + expectation-vs-actual classifier); writes no new store stream. |
| `scripts/plan/tailoring.py` | Create | The care-lane tailoring pass: emit-gate on recorded/non-held domains, dosing-token reject, the deterministic fail-closed drug×supplement×peptide interaction screen, presentation-failure degrade-to-safe, and the load-time `SUMMARY_FIELD_SET`-disjointness tripwire; renders only through `reemit_maintained`. |
| `scripts/generate/maintained.py` | Modify | Accept tailored per-domain sections at the `reemit_maintained` boundary ([maintained.py:245](../../scripts/generate/maintained.py)) via a keyword injector, reusing `_assert_contained` + `reinsert_out` (no second name-bearing writer). |
| `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` | Modify | Backfill the `amended-by (from ADR-0037)` edge + add the tailoring presentation carve-out to ADR-0001's raw-egress list (the ADR-0016/0032/0035 discipline). |
| `tests/serve/test_plan_loop.py` | Create | Front-door binding, anti-degradation guard, debounce (single-reading / sustained / absent-data), trigger convergence, rationale/large-change, adherence-input seam. |
| `tests/serve/test_plan_loop_regen.py` | Create | The end-to-end re-gen through the serve entry point: finding-B trend re-derivation, mutation control (behind→de-load AND on-track→NOT), held-domain-stays-held, crown-jewel non-egress wire-scan (finding C). |
| `tests/plan/test_horizons.py` | Create | Four-horizon composition, derived single-source progress, no-new-stream probe, peptides-untracked, open-ended degradation, date-range + latest-in-window, today-by-date-equality, expectation-vs-actual classifier. |
| `tests/plan/test_tailoring.py` | Create | Personalized output, emit-gate on held domain, dosing-token reject, paired interaction-screen control, fail-closed-on-model-error, wire-scan non-egress, load-time tripwire, idempotency per `(plan, date)`. |

## Tasks

### ADR-0036-T1: Serve-Trigger → Driver Front-Door Binding + Anti-Degradation Guard (BUILD PREREQUISITE)
**Status:** TODO
**ADR Source:** ADR-0036, Decision ("Fired through the SERVE entry point — the full-composition front door (BUILD PREREQUISITE)": the loop invokes `run_orchestrated` → `plan_driver.drive` → composed `gate_dispatch` + `orchestrate.generate_plans`, NOT `_do_generate_plan`); OQ-3 (RESOLVED direction + build task); Validation confirmation #1 (loop fires through the serve entry point via the full-composition front door)
**Files to create/modify:**
- `scripts/serve/plan_loop.py` (Create) — a `regenerate(root, *, dispatch, deid_client, plan_date=None, trigger=None)` entry that drives the front door `run_orchestrated` ([plan_orchestrator.py:127](../../scripts/plan/plan_orchestrator.py)) — which enters the ONE shared `plan_driver.drive` ([plan_driver.py:144](../../scripts/plan/plan_driver.py)) running the composed `gate_dispatch` + the five `orchestrate` cross-domain holds — producing a NEW dated plan for ALL domains. It never imports or calls `_do_generate_plan` / a bare `orchestrate.generate_plans`.
- `scripts/serve/server.py` (Modify) — add a `/plan-loop` (or equivalent) POST branch in the `do_POST` string-equality chain ([server.py:159](../../scripts/serve/server.py)) that fires the cadence/manual loop tick into `plan_loop.regenerate`; the loop branch is distinct from and does not reuse `_do_generate_plan` ([server.py:592](../../scripts/serve/server.py)).
- `tests/serve/test_plan_loop.py` (Create) — front-door binding + anti-degradation tests (fixture `dispatch`, 0 live spend).
**Acceptance Criteria:**
1. Firing the loop through the serve route with a fixture `dispatch` produces exactly one NEW dated `plan::<domain>` set for the current date across all `PLAN_DOMAINS` ([plan_schema.py:49](../../scripts/store/plan_schema.py)) — count of new dated `plan::` domain sets for the trigger date == 1.
2. The re-gen runs the composed path: the driver enters `plan_driver.drive` and the run passes through `compose_disposition` ([gate_dispatch.py:118](../../scripts/plan/gate_dispatch.py)) and the `orchestrate` reconciler ([orchestrate.py:337](../../scripts/plan/orchestrate.py)) — asserted by spying that `run_orchestrated` was entered and the disposition composition site fired (count of `drive` entries on the loop path ≥ 1).
3. **Anti-degradation guard:** a spy over the loop path records 0 calls to `server._do_generate_plan` AND 0 direct calls to `orchestrate.generate_plans` that bypass `plan_driver.drive` — count of screened-only-path invocations on the loop path == 0.
4. **No `adjust.py` on the loop path:** a grep/spy over `scripts/serve/plan_loop.py` and the loop call path finds 0 calls to `adjust.adjust_plan` ([adjust.py:52](../../scripts/plan/adjust.py)) — the loop re-enters the driver, it never per-domain-adjusts (finding-A guard).
5. **Held-domain-stays-held on re-gen:** a fixture whose new data holds a domain (an additive-AE / conflict / Rx-BPMH hold, [orchestrate.py:459](../../scripts/plan/orchestrate.py) records `recorded: False, plan: None`) → that domain is NOT recorded on the re-gen; clearance is re-derived per re-gen, never inherited from a prior plan — count of held domains recorded past the hold == 0.
6. **Fail-closed surface gate preserved:** a fixture whose GATE disposition returns `safety_passed` not-True → the run returns `SAFETY_BLOCKED` ([plan_driver.py:128](../../scripts/plan/plan_driver.py)) with 0 promoted plans — count of `plan::` rows promoted to `root` == 0.
7. `.venv/bin/python -m pytest tests/serve/test_plan_loop.py` passes against fixture clients (0 live-API calls).
**Risk Mitigations:** ADR-0036 finding-A safety gap (a trigger reaching the screened-only path skips the composition) — AC-2 + AC-3 + AC-4. ADR-0036 Validation "held-domain persistence" — AC-5. PF-S63-02 / INV-CORE-CAPABILITY (drive the assembled system through the serve entry point, not a hand-configured module) — AC-1 + AC-2.
**Dependencies:** None (entry point)

---

### ADR-0036-T2: Debounce + Three-Trigger Convergence (Derived State, No New Store Stream)
**Status:** TODO
**ADR Source:** ADR-0036, Decision ("Trigger → one action"; "Debounce (mechanical)"; "Absent data → hold + prompt"); OQ-1 (concrete debounce parameters); OQ-2 (the three trigger surfaces converge on one driver call through one shared debounce gate); OQ-5 (debounce state derived from the dated `plan::` history + a `biomarker::` window query, no new stored stream)
**Files to create/modify:**
- `scripts/serve/plan_loop.py` (Modify) — add the shared debounce gate: a minimum re-generation interval (the last-re-gen date DERIVED from the dated `plan::` history via `plan_schema` read, [plan_schema.py:462](../../scripts/store/plan_schema.py)) PLUS a sustained-signal requirement (a window/threshold query over the `biomarker::` series, [biomarker_meta.py:45](../../scripts/store/biomarker_meta.py) / [router.py:326](../../scripts/plan/router.py)) — a second trigger inside the window is dropped; free-text is rate-limited; absent signal in the window → hold + prompt, never re-generate. All three trigger kinds pass through this one gate before the T1 `regenerate` call.
- `scripts/serve/route.py` (Modify) — after `biomarker_mirror.mirror_registered` ([route.py:166](../../scripts/serve/route.py)) notify `plan_loop`'s debounced entry (wearable write-event).
- `scripts/serve/confirm.py` (Modify) — after `biomarker_mirror.mirror_registered` ([confirm.py:78](../../scripts/serve/confirm.py)) notify `plan_loop`'s debounced entry (lab write-event).
- `scripts/serve/care_chat.py` (Modify) — on capture completion in `respond` ([care_chat.py:239,284](../../scripts/serve/care_chat.py)) notify `plan_loop`'s debounced entry with the derived tokens only (rate-limited free-text trigger).
- `tests/serve/test_plan_loop.py` (Modify) — add the debounce + convergence + absent-data cases.
**Acceptance Criteria:**
1. **Single-reading → NO re-gen:** a trigger fired with a single new `biomarker::` reading inside the window produces 0 new dated plans — count of new dated `plan::` sets == 0.
2. **Sustained signal → re-gen:** a trigger fired after a sustained signal over the window (≥ the pinned n readings across the pinned span meeting the directional-consistency bar) produces exactly 1 new dated plan set — count == 1. AC-1 and AC-2 form a falsifiable pair.
3. **Absent data → hold + prompt:** the cadence trigger fired with NO new signal in the window produces 0 new plans and surfaces a hold+prompt payload — count of new dated `plan::` sets == 0 AND the returned payload carries a log-prompt flag.
4. **Debounce parameters pinned (binary):** a deterministic unit test of the threshold/window function asserts the concrete min-interval value, the window n and span, the directional-consistency bar, and the free-text rate limit — each a fixed number the test reads, not a runtime default.
5. **No new store stream (OQ-5 state):** the debounce state is derived — a grep over `scripts/serve/plan_loop.py` + a store scan finds 0 new `::`-prefixed item ids (no `loop::`, `debounce::`, `regen-marker::`) and 0 `store.append` of a debounce/last-re-gen record; the last-re-gen date is read from the dated `plan::` history and the window from the `biomarker::` series.
6. **Three triggers, one gate:** a second trigger of a DIFFERENT kind inside the same window is dropped by the shared gate — firing a wearable-land trigger then a care-chat trigger inside the window produces at most 1 re-gen (count of new dated `plan::` sets ≤ 1); each of the three call-sites reaches `plan_loop`'s debounced entry (asserted by spying the entry from `route`, `confirm`, and `care_chat`).
7. `.venv/bin/python -m pytest tests/serve/test_plan_loop.py` passes (0 live calls).
**Risk Mitigations:** ADR-0036 Consequences-Negative-1 (per-trigger cost) — the debounce bounds trigger frequency, AC-1 + AC-4 + AC-6. ADR-0036 Validation "debounce (single reading → NO re-gen)" — AC-1 + AC-2. ADR-0036 Validation "absent-data" — AC-3. ADR-0038 no-new-store-schema rule (OQ-5 reconciliation) — AC-5.
**Dependencies:** ADR-0036-T1

---

### ADR-0036-T3: Trend-Reaches-Regen (Finding B) + Mutation Control + Crown-Jewel Non-Egress Through the Serve Entry Point
**Status:** TODO
**ADR Source:** ADR-0036, Decision ("Re-summarize for free (finding B)"; "De-identified / derived tokens only (finding C)"); Validation falsification criteria (mutation control behind→de-load AND on-track→NOT; crown-jewel non-egress wire-scan; held-domain persistence)
**Files to create/modify:**
- `scripts/serve/plan_loop.py` (Modify) — ensure the re-gen path re-summarizes the current store (`router.summarize`, [router.py:707](../../scripts/plan/router.py)) so `recent-trend-direction` ([router.py:464](../../scripts/plan/router.py)) is re-derived from the `biomarker::` feed with no bridge to `plan-track::`; the free-text trigger carries only the derived tokens the care-agent gate produced ([capture.py:80-99](../../scripts/serve/capture.py)).
- `tests/serve/test_plan_loop_regen.py` (Create) — the mutation-control pair, the non-egress wire-scan, and the held-domain persistence probe, all driven through the serve entry point with fixture dispatch + synthetic raw-PII seeds.
**Acceptance Criteria:**
1. **Trend reaches re-gen (finding B):** seed a `biomarker::` series that changes `recent-trend-direction`, fire the loop through the serve route, and assert the re-summarized `summary` handed to the dispatch carries the updated `recent-trend-direction` value — the trend arrives via `router.summarize`, with 0 reads of `plan-track::` required to carry it.
2. **Mutation control — behind → de-load:** seed a series trending BEHIND goal, fire the loop, and assert the re-gen expresses a de-load-or-hold branch for the affected domain.
3. **Mutation control — on-track → NOT de-load:** seed a series ON-TRACK/AHEAD, fire the loop, and assert the re-gen does NOT express the de-load branch. AC-2 and AC-3 differ (a falsifiable pair) — a test asserting the two dispositions are not equal.
4. **Crown-jewel non-egress (finding C):** seed a synthetic raw identifier (a legal name) + raw meds into the raw intake, fire the loop through the free-text trigger, dump the specialist-lane dispatch payload, and assert 0 raw-PII tokens are present — count of raw-PII hits in any specialist dispatch payload == 0.
5. **Raw free-text cannot reach the specialist dispatch:** a spy asserts the free-text trigger's payload to the dispatch contains only tokens from the care-agent gate's derived set ([capture.py:80-94](../../scripts/serve/capture.py)) and 0 raw free-text strings.
6. **Held-domain persistence on re-gen:** a domain held on the prior plan with no clearing signal on the new data stays held on the re-gen — count of silently un-held still-unsafe domains == 0.
7. `.venv/bin/python -m pytest tests/serve/test_plan_loop_regen.py` passes against fixtures + synthetic PII seeds (0 live calls).
**Risk Mitigations:** ADR-0036 Validation "mutation control" — AC-2 + AC-3. ADR-0036 Validation "crown-jewel non-egress (wire-scan)" — AC-4 + AC-5. ADR-0036 Validation "held-domain persistence" — AC-6. Constraint ADR-0001/0034 (finding-C de-id boundary) — AC-4 + AC-5.
**Dependencies:** ADR-0036-T1, ADR-0036-T2

---

### ADR-0036-T4: Re-Gen Rationale + Large-Change Confirmation + Post-Promote Tailoring/Adherence Seams
**Status:** TODO
**ADR Source:** ADR-0036, Decision ("Rationale + control": each re-gen records a plain-language "what changed and why"; large changes surface for confirmation; "Tailoring on an automated (non-operator) re-gen": the loop invokes the tailoring pass directly after `record_plan`); OQ-4 (large-change confirmation vs silent swap); OQ-5 (the `plan-track::` adherence bridge named as a separate, additional input)
**Files to create/modify:**
- `scripts/serve/plan_loop.py` (Modify) — after the front-door promote, (a) record a plain-language rationale string for the re-gen; (b) route a large-change re-gen (over the pinned change threshold) to the confirmation surface rather than a silent swap, reusing the `confirm.py` request-shape precedent ([confirm.py:33](../../scripts/serve/confirm.py)); (c) add the post-promote tailoring-hook seam (a pass-through call that ADR-0037-T1 fills — `promote → tailoring pass → reemit_maintained`); (d) read `resolve_plan_progress` ([track.py:81](../../scripts/plan/track.py)) as a SEPARATE, additional adherence input into the re-gen context (not the trigger's carrier).
- `scripts/serve/confirm.py` (Modify) — accept the loop's large-change confirmation request shape (a distinct branch from the existing reading-land `land_confirmed`).
- `tests/serve/test_plan_loop.py` (Modify) — rationale, large-change confirmation, tailoring-hook seam, adherence-input tests.
**Acceptance Criteria:**
1. **Rationale recorded:** every automated re-gen produces a non-empty plain-language rationale string describing what changed — asserted the returned re-gen payload carries a non-empty `rationale` field.
2. **Large change → confirmation, not silent swap:** a re-gen whose change magnitude exceeds the pinned threshold routes to the confirmation surface and does NOT swap the standing plan until confirmed — count of large-change silent swaps == 0; a below-threshold change swaps without a confirmation prompt.
3. **Large-change threshold pinned (binary):** the change-magnitude threshold is a fixed value a deterministic test reads (not a runtime default).
4. **Post-promote tailoring-hook seam present:** the loop calls a post-promote tailoring hook after the plan is promoted — asserted by spying that the seam fires once per re-gen with the promoted plan + the render target; the seam is a pass-through (no tailored content) until ADR-0037 fills it (count of hook invocations per re-gen == 1).
5. **Adherence is a separate input, not the carrier:** the loop reads `resolve_plan_progress` and threads it as an additional input distinct from the `recent-trend-direction` trend — asserted the trend re-derivation (T3 AC-1) succeeds with `resolve_plan_progress` returning `has_tracking=False` (adherence absent does not block the trend-driven re-gen).
6. **No new store stream for rationale/adherence:** a store scan finds 0 new `::`-prefixed item ids written by the rationale/adherence path.
7. `.venv/bin/python -m pytest tests/serve/test_plan_loop.py` passes (0 live calls).
**Risk Mitigations:** ADR-0036 OQ-4 (silent swap of a materially different plan) — AC-2 + AC-3. ADR-0036 Decision (automated tailoring invocation) — AC-4 (the seam ADR-0037-T1 fills). ADR-0036 OQ-5 (dangling adherence claim) — AC-5. ADR-0038 no-new-store-schema — AC-6.
**Dependencies:** ADR-0036-T1, ADR-0036-T2, ADR-0036-T3 (T2/T3 order the shared `scripts/serve/plan_loop.py` + `scripts/serve/confirm.py` writes — this task writes them after both)

---

### ADR-0038-T1: Horizon Reads Over goal_schema + calendar_schema (Single-Source Progress, Peptides Untracked, Open-Ended Degradation)
**Status:** TODO
**ADR Source:** ADR-0038, Decision #1 (milestone-progress = `goal_schema` derived percent), #2 (dated cadences = `calendar_schema`), #5 (peptides carries no cadence/tracking), #6 (open-ended goals degrade to rolling maintenance cycles)
**Files to create/modify:**
- `scripts/plan/horizons.py` (Create) — the read layer: `resolve_goal` ([goal_schema.py:189](../../scripts/store/goal_schema.py)) for the derived milestone percent (`_percent`, [goal_schema.py:122](../../scripts/store/goal_schema.py), the ONLY progress site), `resolve_events`/`read_events` ([calendar_schema.py:119,138](../../scripts/store/calendar_schema.py)) for the next dated cadence, the peptides-untracked guard (peptides ∉ `TRACKED_DOMAINS`, [plan_schema.py:50](../../scripts/store/plan_schema.py)), and the open-ended-goal rolling-cycle presentation (no fabricated deadline).
- `tests/plan/test_horizons.py` (Create) — progress, cadence, peptides, open-ended cases.
**Acceptance Criteria:**
1. **Derived single-source progress:** for a seeded goal `{baseline, current, target}`, the horizon milestone percent EQUALS `goal_schema._percent(baseline, current, target)` exactly — no second progress computation exists (a grep asserts the only `_percent` caller feeding a horizon reading is via `resolve_goal`, [goal_schema.py:212](../../scripts/store/goal_schema.py)).
2. **Dated cadence read:** the next recheck/check-in is read from `calendar::events` ([calendar_schema.py:37](../../scripts/store/calendar_schema.py)) over the four `EVENT_CATEGORIES` ([calendar_schema.py:44](../../scripts/store/calendar_schema.py)) — a seeded lab-draw/check-in event surfaces as the next cadence; no new schedule object is created.
3. **Peptides-untracked:** a store with a `plan::peptides` document yields NO cadence and NO `plan-track::` horizon for peptides (it is not in `TRACKED_DOMAINS`) — count of peptide cadences emitted == 0.
4. **Open-ended goal degrades:** a goal with no deadline resolves an honest progress percent and the horizon view presents rolling maintenance cycles — a scan of the horizon output finds 0 fabricated target-dates.
5. **No new store stream:** a store scan after the horizon read finds 0 new `::`-prefixed item ids — the read writes nothing.
6. `.venv/bin/python -m pytest tests/plan/test_horizons.py` passes (0 live calls).
**Risk Mitigations:** ADR-0038 Consequences-Negative-1 (horizon state spread across three owners) — each read hits the single owner (AC-1); no duplication introduced. ADR-0038 Validation "peptides-untracked probe" — AC-3. ADR-0038 Validation "open-ended-goal degradation probe" — AC-4.
**Dependencies:** None (entry point)

---

### ADR-0038-T2: ADR-0010 D2 Extras-Seam Enrichment on plan:: Values (Zero Schema Change)
**Status:** TODO
**ADR Source:** ADR-0038, Decision #3 (weekly/monthly framing = the ADR-0010 D2 "open on extras" seam — enrich the dated `plan::<domain>` values with horizon-extra keys, permitted by omission from the required/optional dicts); OQ-1 (the horizon-extra key set/naming)
**Files to create/modify:**
- `scripts/plan/horizons.py` (Modify) — define the horizon-extra key convention (`phase`, `week_intent`, `week_expectation`) written onto the dated `plan::<domain>` values, which `_check_fields` permits by omission ([plan_schema.py:113-139](../../scripts/store/plan_schema.py), docstring [plan_schema.py:116-118](../../scripts/store/plan_schema.py)); read the extras back for the week/month framing. No edit to `plan_schema.py`. [AMENDED 2026-07-03]: Modifying horizons.py trips the ADR-0032 EXTEND-NOT-REBUILD frozen glob. Sanctioned resolution: horizons.py carved out of the frozen glob in BOTH copies (test_route.py + test_pdf_ingestion_e2e.py) as a NEW post-ADR-0032 read-layer module, NOT crown-jewel spine — invariants guarded by tests/plan/test_horizons.py, not the byte-freeze. Architect ruling. Same carve-out covers T3's horizons.py modify.
- `tests/plan/test_horizons.py` (Modify) — enrichment validation cases (with and without the extras).
**Acceptance Criteria:**
1. **Enriched plan validates unchanged:** a `plan::<domain>` document carrying the horizon extras (`phase`/`week_intent`/`week_expectation`) validates through `record_plan` ([plan_schema.py:371](../../scripts/store/plan_schema.py)) — it passes `_check_fields`.
2. **Flat plan still validates (graceful floor):** a `plan::<domain>` document WITHOUT the extras also validates — the flat day-plan is the floor, the enriched plan the horizon-aware view.
3. **Zero schema change:** `git diff --numstat <base>..HEAD` shows 0 changed lines on `scripts/store/plan_schema.py` — the enrichment rides the D2 seam with no writer/schema edit.
4. **Extras read back:** the week/month framing reads the `phase`/`week_intent`/`week_expectation` extras off the dated plan values — a seeded enriched plan surfaces its `week_intent` in the horizon view.
5. **Unknown extra ignored (no raise):** a plan document with a typo'd horizon key still validates and the typo'd key is ignored (no raise) — the standing D2 tradeoff, asserted.
6. `.venv/bin/python -m pytest tests/plan/test_horizons.py` passes (0 live calls).
**Risk Mitigations:** ADR-0038 Alternative C rejection (no periodization rewrite of the flat schema) — AC-3 (zero schema change). ADR-0038 Validation "enrichment rides D2 with zero schema change" — AC-1 + AC-2 + AC-3.
**Dependencies:** ADR-0038-T1

---

### ADR-0038-T3: Date-Range Week/Month Query + Latest-in-Window Selection + Expectation-vs-Actual Classifier
**Status:** TODO
**ADR Source:** ADR-0038, Decision #4 ("this week's block / the month arc" = a date-range query over the dated plan history, not a second stored schedule); Consequences-Negative-3 (the loop densifies the history: select latest-in-window among multiple same-window plans); OQ-2 (window boundaries + same-window selection); OQ-3 (per-week expectation sourcing); ADR-0036 Validation (machine-comparable expectation vs actual → behind/on-track/ahead)
**Files to create/modify:**
- `scripts/plan/horizons.py` (Modify) — a date-range query over the dated `plan::<domain>` history (the same date semantics `resolve_plan` uses, [plan_schema.py:462-498](../../scripts/store/plan_schema.py), equality at [plan_schema.py:486](../../scripts/store/plan_schema.py)) widened to a 7-day / month window, with latest-in-window selection when the loop leaves multiple same-window dated plans; and a deterministic expectation-vs-actual classifier (declared per-week expectation via the D2 `week_expectation` extra vs the actual trend from the goal/`biomarker::` reads → behind/on-track/ahead, a pure comparison, no model call).
- `tests/plan/test_horizons.py` (Modify) — date-range, latest-in-window, today-by-date-equality, and classifier cases.
**Acceptance Criteria:**
1. **Four-horizon composition:** for one render date over a seeded store, the composition yields today's action (the `plan::<domain>` reading whose `timepoint` EQUALS the render date), this-week's block (the 7-day range set), the month arc (the month range set), and a milestone (a `resolve_goal` percent) — all four present from the same store, with 0 new store keys (a store scan for `plan-arc::`/`horizon::`/`periodization::` returns 0 hits).
2. **Latest-in-window selection:** with multiple `plan::<domain>` dated plans inside one window (the loop-densified case), the range query selects the latest-in-window reading as "the block" — a two-same-window fixture returns the later-dated plan.
3. **Today-by-date-equality preserved:** with a plan dated yesterday and a plan dated the render date on file, the today slot returns the render-date plan; with NO render-date plan the today slot reads `NO_PLAN_TODAY` ([plan_schema.py:46](../../scripts/store/plan_schema.py)), never the nearest date.
4. **Expectation-vs-actual classifier (deterministic):** given a declared per-week expectation (e.g. `-0.4 kg/wk` via the `week_expectation` extra) and an actual trend (e.g. `-0.1 kg/wk`), the classifier returns "behind"; an equal/faster actual returns "on-track"/"ahead" — the (expectation, actual) pair maps to a fixed verdict with no model call.
5. **No second progress site / no new stream:** a grep asserts the classifier reads the derived goal percent and the date-range plan history and writes no new `::`-prefixed store item — 0 new stored streams, 0 second progress-derivation sites.
6. `.venv/bin/python -m pytest tests/plan/test_horizons.py` passes (0 live calls).
**Risk Mitigations:** ADR-0038 Consequences-Negative-3 / RT-09 (loop-densified history) — AC-2. ADR-0038 Validation "no-new-stream probe" — AC-1 + AC-5. ADR-0038 Validation "today-by-date-equality probe" — AC-3. ADR-0036 Validation "machine-comparable expectation vs actual" — AC-4.
**Dependencies:** ADR-0038-T1, ADR-0038-T2

---

### ADR-0037-T1: Care-Lane Tailoring Pass — Placement, Emit-Gate, Degrade-to-Safe, Artifact-Only, Automated Invocation
**Status:** TODO
**ADR Source:** ADR-0037, Decision (§1 emit-gate on recorded, non-held domains; §4 presentation failure degrades to the un-tailored plan; artifact-only via `reemit_maintained`); ADR-0036 Decision ("Tailoring on an automated (non-operator) re-gen": the loop invokes the pass after `record_plan`, idempotent per `(plan, date)`, fail-safe to the un-tailored plan)
**Files to create/modify:**
- `scripts/plan/tailoring.py` (Create) — the pass: it emits a tailored section for a domain ONLY when `plan::<domain>` exists in the promoted store AND that domain was in NO hold set (`holds`/`conflict_held`/`rx_bpmh_held`, [orchestrate.py:365-367](../../scripts/plan/orchestrate.py); a held candidate carries `recorded: False, plan: None`, [orchestrate.py:459-463](../../scripts/plan/orchestrate.py)); the presentation is a model call, and on its failure/empty return the domain degrades to its un-tailored recorded plan (mirroring the care turn's `ModelCallError` posture, [care_chat.py:279-281](../../scripts/serve/care_chat.py)); it reads the operator's raw detail from the care lane (`_care_profile`, [care_chat.py:165](../../scripts/serve/care_chat.py)) and renders only through `reemit_maintained`.
- `scripts/generate/maintained.py` (Modify) — accept tailored per-domain sections at the `reemit_maintained` boundary ([maintained.py:245](../../scripts/generate/maintained.py)) via a keyword injector, reusing `_assert_contained` ([maintained.py:61](../../scripts/generate/maintained.py)) + `reinsert_out` + `_preserve_prior_content` ([maintained.py:180](../../scripts/generate/maintained.py)); no second name-bearing writer, no store key.
- `scripts/serve/plan_loop.py` (Modify) — fill the ADR-0036-T4 post-promote hook with the tailoring pass on the automated (no-care-chat) re-gen path.
- `tests/plan/test_tailoring.py` (Create) — placement, emit-gate, degrade, idempotency cases.
**Acceptance Criteria:**
1. **Personalized output:** run the pass over a fixture with a recorded, non-held `plan::<domain>` and raw care-lane detail (a peptide + a supplement); the maintained artifact's tailored section for that domain references the operator's actual raw specifics — the tailored section is present.
2. **Emit-gate on held domain:** a domain HELD (an additive-AE / conflict / Rx-BPMH hold so `_held_result` records `recorded: False`, [orchestrate.py:459-463](../../scripts/plan/orchestrate.py)) gets NO tailored content — count of tailored sections for a held domain == 0; other domains may still tailor.
3. **Degrade-to-safe on model error:** inject a `ModelCallError`/empty return on the presentation call; the affected domain renders its un-tailored, de-identified, safety-cleared recorded plan — the un-tailored plan is present and the run does not crash.
4. **Artifact-only via `reemit_maintained`:** the pass writes only through `reemit_maintained` and opens no store stream — a grep over `scripts/plan/tailoring.py` finds 0 `store.append`/store-key definitions and 0 second name-bearing writer.
5. **Fires on the automated path (no care-chat turn):** firing the loop via the cadence/`biomarker::` trigger with NO operator care-chat turn runs the tailoring pass after the promote — count of tailoring-pass invocations on the automated re-gen == 1.
6. **Idempotent per `(plan, date)`:** firing the pass twice for the same `(plan, date)` produces no duplicate/stale tailored section (reusing `_preserve_prior_content`, [maintained.py:180](../../scripts/generate/maintained.py)) — count of duplicate tailored sections == 0.
7. `.venv/bin/python -m pytest tests/plan/test_tailoring.py` passes against fixtures (0 live calls, 0 real operator PII in the test tree).
**Risk Mitigations:** ADR-0037 finding D (shadow-prescribe a held domain) — AC-2. ADR-0037 §4 (presentation failure fail-open) — AC-3. ADR-0036 constraint (idempotent per `(plan, date)`, fail-safe) — AC-3 + AC-5 + AC-6. ADR-0021/0025 (artifact-only, no second writer) — AC-4.
**Dependencies:** ADR-0036-T1, ADR-0036-T3, ADR-0036-T4 (T3 orders the shared `scripts/serve/plan_loop.py` write; the tailoring pass attaches at ADR-0036-T4's post-promote seam — T4 AC-4 establishes the pass-through hook this task fills)

---

### ADR-0037-T2: Dosing-Token Reject + Deterministic Fail-Closed Interaction Screen (Paired Control)
**Status:** TODO
**ADR Source:** ADR-0037, Decision (§2 dosing-token reject on compound-domain output; §3 a deterministic drug×supplement×peptide interaction screen built on ADR-0034's curated `rx-interaction-classes` + the existing BPMH/additive-AE lenses that FAILS CLOSED to "see your doctor", split off the presentation model call); OQ-2 (the dosing lexicon + the rule's sync with ADR-0034)
**Files to create/modify:**
- `scripts/plan/tailoring.py` (Modify) — scan a compound domain's (supplements/peptides) tailored output for a dosing token; on a hit REJECT (degrade the domain to its un-tailored recorded plan). Add the deterministic interaction rule: screen the operator's raw meds × raw supplements × raw peptides on `router.rx_interaction_class_set` ([router.py:198](../../scripts/plan/router.py)) + the BPMH/additive-AE lens logic ([orchestrate.py:168,262](../../scripts/plan/orchestrate.py)); on a match SURFACE "see your doctor" (never silently drop). The screen is deterministic code that does NOT ride the presentation model call.
- `tests/plan/test_tailoring.py` (Modify) — dosing-reject + paired interaction-screen cases.
**Acceptance Criteria:**
1. **Dosing-token reject:** a dosing token in the tailored output for a compound domain is REJECTED and the domain degrades to the un-tailored recorded plan — count of compound-domain tailored sections carrying a dosing token == 0.
2. **Interaction screen fires on a known combo:** raw meds × supplements × peptides that intersect a curated `rx-interaction-class` produce a "see your doctor" referral in the tailored output for the affected compound domain — the referral text is present.
3. **Interaction screen does NOT fire on a safe combo:** a med × supplement × peptide set with no curated-class intersection produces no referral — fires-on-known == True AND fires-on-safe == False (a paired control; a rule that fires on both or neither fails).
4. **Screen is deterministic and split off the model call:** the interaction screen runs as deterministic code independent of the presentation call — with the presentation call injected to fail, the screen's verdict is unchanged (the screen does not depend on the presentation call).
5. **Fail-closed, never silent drop:** on an interaction match the concern SURFACES; it is never dropped — a match with a suppressed/empty presentation still surfaces the referral.
6. `.venv/bin/python -m pytest tests/plan/test_tailoring.py` passes against fixtures (0 live calls).
**Risk Mitigations:** ADR-0037 finding D (dose an investigational compound) — AC-1. ADR-0037 §3 (deterministic fail-closed screen) — AC-2 + AC-3 + AC-4 + AC-5. ADR-0037 Validation "interaction-screen PAIRED control" — AC-2 + AC-3.
**Dependencies:** ADR-0037-T1

---

### ADR-0037-T3: Load-Time Tripwire + Crown-Jewel Wire-Scan Non-Egress + ADR-0001 Egress Amendment
**Status:** TODO
**ADR Source:** ADR-0037, Decision (§5 a load-time tripwire that no tailoring key is a `SUMMARY_FIELD_SET` member); Decision (the tailoring egress amends ADR-0001's list on the ADR-0016/0032/0035 discipline); Validation (wire-scan non-egress probe; load-time tripwire probe); OQ-3/RT-01 (the reinserted-name scan residual — a pre-ship check, not a re-block)
**Files to create/modify:**
- `scripts/plan/tailoring.py` (Modify) — add an import-time assert that no tailoring-artifact key is a `SUMMARY_FIELD_SET` member (mirroring `capture.WIRED_TOKENS ⊆ SUMMARY_FIELD_SET`, [capture.py:283-285](../../scripts/serve/capture.py); the router disjointness asserts, [router.py:667-668](../../scripts/plan/router.py)).
- `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` (Modify) — add the tailoring presentation carve-out to ADR-0001's raw-egress list and backfill the `amended-by (from ADR-0037)` edge.
- `tests/plan/test_tailoring.py` (Modify) — the wire-scan non-egress probe + the tripwire probe + the reinserted-name pre-ship check.
**Acceptance Criteria:**
1. **Load-time tripwire:** if any tailoring-artifact key is added to `SUMMARY_FIELD_SET` ([router.py:23](../../scripts/plan/router.py)), the import-time assert REDs — asserted by a test that adds a tailoring key to a `SUMMARY_FIELD_SET` copy and confirms the assert raises.
2. **Wire-scan non-egress (crown-jewel):** seed a synthetic raw-PII token (a legal name + a raw drug name) into the raw intake, run the full tailoring path, dump BOTH the store streams and the de-identified dashboard payload, and assert the raw tokens AND every tailoring-artifact key are ABSENT from both — count of raw-PII hits AND tailoring-key hits in any store stream or the dashboard == 0.
3. **Tailored content stays in the gitignored artifact:** the tailored sections appear ONLY in the `maintained` artifact under `vault/artifacts/generated/` (via `reemit_maintained`, [maintained.py:245](../../scripts/generate/maintained.py)) — count of tailored sections in any tracked/committed render == 0.
4. **ADR-0001 egress list amended:** ADR-0001 carries the tailoring presentation carve-out entry and the `amended-by (from ADR-0037)` edge — asserted by a grep over `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` finding the ADR-0037 carve-out reference.
5. **Reinserted-name pre-ship check:** a maintained artifact carrying the reinserted operator NAME (not only contact tokens) under `vault/artifacts/generated/` is denied by the commit/push PII scan (the `DATA_BEARING_PREFIXES` coverage, design finding J closed) — count of committed reinserted-name artifacts that pass the scan == 0.
6. `.venv/bin/python -m pytest tests/plan/test_tailoring.py` passes against synthetic PII seeds (0 live calls, 0 real operator PII in the test tree).
**Risk Mitigations:** ADR-0037 §5 (a tailoring key masquerading as a planner token) — AC-1. ADR-0037 Consequences-Negative-1 (a second raw-egress surface to audit) — AC-2 + AC-3. ADR-0037 finding E/F (no raw store stream; named egress) — AC-2 + AC-4. ADR-0037 OQ-3/RT-01 (reinserted-name scan residual) — AC-5.
**Dependencies:** ADR-0037-T1, ADR-0037-T2

---

## Dependency Map

```
ADR-0036-T1 --> ADR-0036-T2      (front-door binding → the debounce gate wraps the same regenerate entry)
ADR-0036-T1 --> ADR-0036-T3      (mutation-control/non-egress drive the front-door re-gen)
ADR-0036-T1 --> ADR-0036-T4      (rationale/hook seams sit on the front-door promote)
ADR-0036-T2 --> ADR-0036-T3      (a sustained-signal fire is needed to drive the mutation-control re-gen)
ADR-0036-T2 --> ADR-0036-T4      (serialize the shared plan_loop.py/confirm.py writers: T2 establishes the serve-trigger/front-door binding that T4's measure-bridge writes alongside)
ADR-0036-T3 --> ADR-0036-T4      (serialize the shared plan_loop.py writers: T4's re-gen rationale reports the trend T3's re-summarize establishes)
ADR-0038-T1 --> ADR-0038-T2      (the extras-seam enrichment layers on the goal/calendar read layer)
ADR-0038-T1 --> ADR-0038-T3      (the date-range/classifier consume the goal read + cadence)
ADR-0038-T2 --> ADR-0038-T3      (the date-range query reads the D2-enriched plan values + week_expectation)
ADR-0036-T1 --> ADR-0037-T1      (tailoring runs after the driver records/promotes the plan)
ADR-0036-T3 --> ADR-0037-T1      (serialize the shared plan_loop.py writers; the tailoring pass fills ADR-0036-T4's post-promote pass-through seam)
ADR-0036-T4 --> ADR-0037-T1      (tailoring fills the post-promote hook seam T4 established)
ADR-0037-T1 --> ADR-0037-T2      (dosing-reject + interaction screen extend the pass)
ADR-0037-T1 --> ADR-0037-T3      (the tripwire/wire-scan audit the pass's egress)
ADR-0037-T2 --> ADR-0037-T3      (the wire-scan runs the full tailoring path incl. the screen)
```

Topological order (Kahn's algorithm; parallel groups). The shared-file writers on `scripts/serve/plan_loop.py` (T1→T2→T3→T4→ADR-0037-T1) and `scripts/serve/confirm.py` (T2→T4) are serialized into a chain, so no parallel group holds two writers of the same mutable file:

1. **ADR-0036-T1, ADR-0038-T1** (parallel — entry points; ADR-0036-T1 is the BUILD PREREQUISITE, ADR-0038-T1 is independent since ADR-0038 `enables` ADR-0036 SOFTLY — horizons build in parallel with the loop; distinct files: `server.py`/`plan_loop.py` vs `horizons.py`)
2. **ADR-0036-T2, ADR-0038-T2** (parallel — T2 depends only on ADR-0036-T1; ADR-0038-T2 depends only on ADR-0038-T1; distinct files: `plan_loop.py`/`route.py`/`confirm.py`/`care_chat.py` vs `horizons.py`)
3. **ADR-0036-T3, ADR-0038-T3** (parallel — T3 depends on T1+T2; ADR-0038-T3 depends on ADR-0038-T1+T2; distinct files: `plan_loop.py`/`test_plan_loop_regen.py` vs `horizons.py`)
4. **ADR-0036-T4** (after ADR-0036-T1+T2+T3 — the sole writer of `plan_loop.py`/`confirm.py` in this group)
5. **ADR-0037-T1** (after ADR-0036-T1+T3+T4 — the sole writer of `plan_loop.py` in this group)
6. **ADR-0037-T2** (after ADR-0037-T1)
7. **ADR-0037-T3** (after ADR-0037-T1 + ADR-0037-T2)

Entry points: ADR-0036-T1, ADR-0038-T1
Critical path: ADR-0036-T1 → ADR-0036-T2 → ADR-0036-T3 → ADR-0036-T4 → ADR-0037-T1 → ADR-0037-T2 → ADR-0037-T3 (the loop-prereq → the debounce gate → the trend/mutation re-summarize → the post-promote rationale/hook → the tailoring pass → the screen → the egress audit — the fully-serialized `plan_loop.py` writer chain plus the tailoring tail)

These parallel groups map to the build-plan waves in the design's build order (loop → horizons → tailoring): **Wave 1** = the loop front-door prerequisite + debounce + trend/mutation + rationale/hook (ADR-0036-T1..T4) ∥ the horizon reads (ADR-0038-T1..T3); **Wave 2** = the tailoring pass + screen + egress audit (ADR-0037-T1..T3). Horizons author-parallel with the loop (the loop works on the coarse `recent-trend-direction` without formal horizons since `enables` is soft); tailoring is last (highest-risk raw egress, constrained by the loop's re-run contract).

## Test Strategy

All tasks are satisfiable with fixture consumers (a programmatic `dispatch` fulfilling each yield class + fixture GATE verdicts + fixture care-lane detail) and synthetic PII-free fixtures. **No task makes a live API call (0 live-API spend); the LIVE end-to-end subscription run + the clinical reasoning-quality of the de-load/tailoring prose are the operator-present downstream attestation AFTER the build (a PR-documented manual live dispatch, never a CI assertion — the `test_adjust.py` convention).** The crown-jewel probes use synthetic raw-PII tokens (a legal name + a raw drug name + a lab value) seeded into the raw intake.

### Unit Tests
- **Scope:** `scripts/serve/plan_loop.py` (the debounce threshold/window function, the front-door binding, the anti-degradation guard, the rationale/large-change/adherence seams), `scripts/plan/horizons.py` (the derived progress, the D2 enrichment, the date-range/latest-in-window query, the expectation-vs-actual classifier), `scripts/plan/tailoring.py` (the emit-gate, the dosing-reject, the deterministic interaction rule, the degrade-to-safe, the load-time tripwire).
- **Approach:** pytest with a fixture `dispatch` + fixture GATE verdicts + fixture care-lane raw detail; no live dependencies, no real PII; seeded `biomarker::`/`goal::`/`calendar::events`/`plan::` fixtures.
- **Criteria covered:** ADR-0036-T2 1-4, ADR-0036-T4 1-6, ADR-0038-T1 1-6, ADR-0038-T2 1-6, ADR-0038-T3 1-5, ADR-0037-T1 1-6, ADR-0037-T2 1-5, ADR-0037-T3 1.

### Integration Tests
- **Scope:** the loop end-to-end through the SERVE entry point — trigger → debounce → `run_orchestrated` → `plan_driver.drive` → composed `gate_dispatch` + `orchestrate` reconciliation → promote → (rationale/tailoring hook) — over synthetic fixtures with a fixture dispatch. Exercises a file created by one task consumed by another (ADR-0036-T1's `regenerate` → T2's debounce → T4's post-promote hook → ADR-0037-T1's tailoring pass; ADR-0038-T2's enriched plan → T3's date-range query).
- **Approach:** drive the loop through the serve route; assert exactly one new dated all-domain plan via the composed path, the finding-B trend re-derivation, the debounce single-vs-sustained pair, and the tailoring pass firing on the automated path.
- **Criteria covered:** ADR-0036-T1 1-6, ADR-0036-T2 1-3+6, ADR-0036-T3 1-6, ADR-0036-T4 4, ADR-0038-T3 1-3, ADR-0037-T1 5.

### Risk-Specific Tests
- **Scope:** the anti-degradation guard (ADR-0036-T1 AC-3/AC-4 — 0 screened-only-path / 0 `adjust.py` on the loop path), the held-domain persistence (ADR-0036-T1 AC-5 + T3 AC-6), the mutation-control pair (ADR-0036-T3 AC-2/AC-3), the crown-jewel non-egress wire-scan (ADR-0036-T3 AC-4/AC-5 + ADR-0037-T3 AC-2/AC-3), the debounce single-reading-no-thrash + absent-data (ADR-0036-T2 AC-1/AC-3), the no-new-store-stream probes (ADR-0036-T2 AC-5, T4 AC-6, ADR-0038-T1 AC-5, T3 AC-5), the emit-gate on a held domain (ADR-0037-T1 AC-2), the dosing-token reject (ADR-0037-T2 AC-1), the paired interaction-screen control (ADR-0037-T2 AC-2/AC-3), the fail-closed-on-model-error (ADR-0037-T1 AC-3 + T2 AC-4/AC-5), the load-time tripwire (ADR-0037-T3 AC-1), and the reinserted-name pre-ship check (ADR-0037-T3 AC-5).
- **Approach:** seed each adversarial condition (a trigger routed at the screened-only path; a held domain on new data; a behind vs on-track series; a synthetic raw-PII token in the raw intake AND a planted tailoring key; a single reading vs a sustained window; a dosing token in compound output; a known vs safe interaction combo; a failing presentation call; a tailoring key added to `SUMMARY_FIELD_SET`; a reinserted-name artifact staged) and assert the 0-threshold / fail-closed / falsifiable-pair outcome.
- **Store-adversarial battery:** NO task adds a NEW write to `scripts/store/`. The loop's only store write is the existing front-door `_promote_plans` → `store.append` ([plan_driver.py:452](../../scripts/plan/plan_driver.py), [store.py:134](../../scripts/store/store.py)), unchanged; the tailoring pass and the horizon reads write NO store stream (ADR-0037-T3 AC-2/AC-3, ADR-0038-T1 AC-5 / T3 AC-5); the debounce state is derived (ADR-0036-T2 AC-5). The full suite staying green re-runs the existing store-adversarial battery across the change; no new battery is authored (the store surface did not change).
- **Criteria covered:** ADR-0036-T1 3-6, ADR-0036-T2 1+3+5, ADR-0036-T3 2-6, ADR-0036-T4 2+6, ADR-0038-T1 3-5, ADR-0038-T2 3+5, ADR-0038-T3 2-5, ADR-0037-T1 2-4+6, ADR-0037-T2 1-5, ADR-0037-T3 1-5.

## Repo-Grounding Ledger

Grounded against the worktree-authoritative checkout at `main @ ad8afd7` (HEAD). The extend-not-rebuild fact, the screened-only `_do_generate_plan` premise, the no-trigger/no-debounce/no-tailoring-hook/no-date-range-query greenfield premises, the D2 open-on-extras premise, the `TRACKED_DOMAINS`-excludes-peptides premise, and the `plan-arc::`-absent premise were confirmed by reading the live files directly (not the ADR prose). Corrections carried into the manifest: `run_orchestrated` is in `plan_orchestrator.py:127` (not `plan_driver`); `record_plan` is in `plan_schema.py:371`; `_safe_gate` does not exist (the `safety_passed is True` surface gate is inline in `drive`, `SAFETY_BLOCKED` at [plan_driver.py:128](../../scripts/plan/plan_driver.py)); `drive` reaches the engine via `pipeline.run_generation` ([pipeline.py:28](../../scripts/plan/pipeline.py)) → `orchestrate.generate_plans` ([orchestrate.py:482](../../scripts/plan/orchestrate.py)); `plan-track::` is `_PREFIX_TRACK` at [plan_schema.py:57](../../scripts/store/plan_schema.py); `_assert_contained` is at [maintained.py:61](../../scripts/generate/maintained.py) (not ~312).

| Task | RGC-1 (manifest action) | RGC-2 (premise freshness) | RGC-3 (cited input) | RGC-4 (no duplication) | Disposition |
|------|-------------------------|---------------------------|---------------------|------------------------|-------------|
| ADR-0036-T1 | pass — `plan_loop.py` ABSENT (Create); `server.py` present (Modify); `test_plan_loop.py` ABSENT (Create) | pass — `_do_generate_plan` ([server.py:592](../../scripts/serve/server.py)) calls `orchestrate.generate_plans` DIRECTLY at [server.py:678](../../scripts/serve/server.py) with no reauthor/adjudicator hook (comment [server.py:675-677](../../scripts/serve/server.py)); `run_orchestrated` present ([plan_orchestrator.py:127](../../scripts/plan/plan_orchestrator.py)); `drive` present ([plan_driver.py:144](../../scripts/plan/plan_driver.py)); `SAFETY_BLOCKED` [plan_driver.py:128](../../scripts/plan/plan_driver.py) | pass — `run_orchestrated(raw_intake, deid_client, dispatch, store_read, root, *, plan_date, ...)` signature confirmed; `adjust.adjust_plan` at [adjust.py:52](../../scripts/plan/adjust.py); `_held_result` recorded:False at [orchestrate.py:459-463](../../scripts/plan/orchestrate.py) | pass — NO existing serve loop trigger / front-door binding (grep: plan generation fires only via the synchronous `/generate-plan` POST); it is new | Grounded |
| ADR-0036-T2 | pass — `plan_loop.py` (Modify, created T1); `route.py`/`confirm.py`/`care_chat.py` present (Modify); test (Modify) | pass — `biomarker_mirror.mirror_registered` called at [route.py:166](../../scripts/serve/route.py) + [confirm.py:78](../../scripts/serve/confirm.py); care-chat capture at [care_chat.py:284](../../scripts/serve/care_chat.py); NO debounce/cadence/last-re-gen state anywhere in serve (grep clean); `resolve_plan`/dated `plan::` history at [plan_schema.py:462](../../scripts/store/plan_schema.py); `biomarker::` feed at [router.py:326](../../scripts/plan/router.py) | pass — `mirror_registered(readings, root)` at [biomarker_mirror.py:20](../../scripts/serve/biomarker_mirror.py); `respond(...)` [care_chat.py:239](../../scripts/serve/care_chat.py); `land_confirmed(readings, *, root)` [confirm.py:33](../../scripts/serve/confirm.py); `route_upload(...)` [route.py:102](../../scripts/serve/route.py) | pass — NO existing debounce/window function; it is new (derived, no store stream) | Grounded |
| ADR-0036-T3 | pass — `plan_loop.py` (Modify); `test_plan_loop_regen.py` ABSENT (Create) | pass — `router.summarize` at [router.py:707](../../scripts/plan/router.py); `_recent_trend_direction` at [router.py:464](../../scripts/plan/router.py) over the `biomarker::` polarity feed [router.py:326](../../scripts/plan/router.py); care-agent derived tokens `WIRED_TOKENS` [capture.py:80-94](../../scripts/serve/capture.py); rx-interaction-classes absent from WIRED_TOKENS [capture.py:95-99](../../scripts/serve/capture.py) | pass — `summarize(store_read, ...)` signature confirmed; `SUMMARY_FIELD_SET` incl `recent-trend-direction` [router.py:41](../../scripts/plan/router.py); disjointness asserts [router.py:667-668](../../scripts/plan/router.py) | pass — NO existing mutation-control / wire-scan test over the loop path; it is new | Grounded |
| ADR-0036-T4 | pass — `plan_loop.py` (Modify); `confirm.py` present (Modify); test (Modify) | pass — `confirm.land_confirmed` [confirm.py:33](../../scripts/serve/confirm.py) is the reading-land confirmation (NOT plan/large-change) — the request-shape precedent to reuse; `resolve_plan_progress` at [track.py:81](../../scripts/plan/track.py); NO post-record tailoring hook exists today (grep 'tailor' = 0 in plan_driver/serve) | pass — `resolve_plan_progress(domain, on_date, root)` signature confirmed; `_care_profile`/`_maybe_care_review` fire-after-save precedent at [server.py:316](../../scripts/serve/server.py) | pass — NO existing rationale/large-change/adherence seam; the tailoring hook is greenfield (grep 'tailor' = 0 hits) | Grounded |
| ADR-0038-T1 | pass — `horizons.py` ABSENT (Create); `test_horizons.py` ABSENT (Create) | pass — `resolve_goal(readings)` [goal_schema.py:189](../../scripts/store/goal_schema.py) (NO on_date param — derives it) returns `{label, percent, baseline, current, target, unit, on_date}`; `_percent` [goal_schema.py:122](../../scripts/store/goal_schema.py); `TRACKED_DOMAINS` excludes peptides [plan_schema.py:50](../../scripts/store/plan_schema.py) | pass — `EVENT_CATEGORIES` [calendar_schema.py:44](../../scripts/store/calendar_schema.py); `resolve_events`/`read_events` [calendar_schema.py:119,138](../../scripts/store/calendar_schema.py) confirmed | pass — NO existing horizon read layer; `goal_schema`/`calendar_schema` are the single owners it composes over, not duplicates | Grounded |
| ADR-0038-T2 | pass — `horizons.py` (Modify); test (Modify) | pass — `_check_fields` permits unknown keys by omission ([plan_schema.py:113-139](../../scripts/store/plan_schema.py), docstring [plan_schema.py:116-118](../../scripts/store/plan_schema.py)); NO existing `phase`/`week_intent` keys on plan values (grep clean) | pass — `record_plan(domain, plan, plan_date, specialist, root)` [plan_schema.py:371](../../scripts/store/plan_schema.py) validates enriched + flat | pass — the enrichment rides the D2 seam (no schema edit); it is not a `plan_schema` duplication | Grounded |
| ADR-0038-T3 | pass — `horizons.py` (Modify); test (Modify) | pass — `resolve_plan` date-equality [plan_schema.py:486](../../scripts/store/plan_schema.py); `NO_PLAN_TODAY` [plan_schema.py:46](../../scripts/store/plan_schema.py); NO existing date-range/week/month query (grep clean); NO `plan-arc::`/`horizon::`/`periodization::` stream (grep: 0 hits) | pass — `store.read` sorts by timepoint but exposes no range filter (confirmed) — the range query is new over the same date predicate | pass — NO existing range query / classifier; it is new, single-progress-site | Grounded |
| ADR-0037-T1 | pass — `tailoring.py` ABSENT (Create); `maintained.py` present (Modify); `plan_loop.py` (Modify); `test_tailoring.py` ABSENT (Create) | pass — `reemit_maintained(*, root=None, ...)` [maintained.py:245](../../scripts/generate/maintained.py) keyword-only; `_assert_contained` [maintained.py:61](../../scripts/generate/maintained.py); `_preserve_prior_content` [maintained.py:180](../../scripts/generate/maintained.py); `_care_profile` raw read [care_chat.py:165](../../scripts/serve/care_chat.py); hold sets [orchestrate.py:365-367](../../scripts/plan/orchestrate.py); `_held_result` recorded:False [orchestrate.py:459-463](../../scripts/plan/orchestrate.py) | pass — `_care_profile`/`_CARE_HEALTH_DETAIL` [care_chat.py:125-131,165](../../scripts/serve/care_chat.py); `reinsert_out` imported from `scripts.plan` at [maintained.py:49](../../scripts/generate/maintained.py) | pass — NO existing tailoring pass (grep 'tailor' = 0); it reuses `reemit_maintained` (the single writer), adds no second name-bearing writer | Grounded |
| ADR-0037-T2 | pass — `tailoring.py` (Modify); test (Modify) | pass — `rx_interaction_class_set` [router.py:198](../../scripts/plan/router.py); the additive-AE lens [orchestrate.py:168](../../scripts/plan/orchestrate.py) + the rx-BPMH screen [orchestrate.py:262](../../scripts/plan/orchestrate.py); the curated `rx-interaction-classes` token [router.py:171,218](../../scripts/plan/router.py) | pass — `rx_interaction_class_set(summary)` parses the `;`-joined scalar (confirmed); the lenses' logic is readable to build the deterministic rule on | pass — the screen is a NEW deterministic rule over the curated classes; it does not duplicate the reconciler's lenses (it re-uses their class basis) | Grounded |
| ADR-0037-T3 | pass — `tailoring.py` (Modify); `ADR-0001-...md` present (Modify); test (Modify) | pass — `capture.WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` tripwire [capture.py:283-285](../../scripts/serve/capture.py); router disjointness asserts [router.py:667-668](../../scripts/plan/router.py); `vault/artifacts/generated/` IS in `DATA_BEARING_PREFIXES` (design finding J closed — verified) | pass — `SUMMARY_FIELD_SET` [router.py:23](../../scripts/plan/router.py); ADR-0001 egress list present with the ADR-0016/0032/0035 sibling entries | pass — the load-time tripwire mirrors the existing `capture`/`router` asserts (a NEW assert over tailoring keys, not a duplicate enforcer of an existing capability) | Grounded |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter has ≥1 task (ADR-0036 → T1/T2/T3/T4; ADR-0038 → T1/T2/T3; ADR-0037 → T1/T2/T3)
- [x] All ADR IDs resolve to actual ADR files on disk (ADR-0036/0037/0038 present in `docs/adr/`)

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (all have ≥6)
- [x] All acceptance criteria are binary (pass/fail) — each names a function/command/condition with a 0-threshold, an exact count/equality, a present/absent check, a falsifiable pair, a numstat=0 probe, or a pinned numeric value
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in ≥1 task block
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (verified by topo sort — 7 groups, all edges forward within and across ADRs; no reciprocal edge; the `plan_loop.py`/`confirm.py` shared-file writers serialized T1→T2→T3→T4→ADR-0037-T1 so no parallel group holds two writers of one mutable file)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed with Dependencies "None (entry point)" (ADR-0036-T1, ADR-0038-T1)

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream constraints in their ACs (ADR-0036 constrains ADR-0037 idempotency/fail-safe → ADR-0037-T1 AC-3/AC-5/AC-6; ADR-0038 no-new-store-schema → ADR-0036-T2 AC-5 + ADR-0038-T1 AC-5/T3 AC-5; ADR-0001/0034 de-id boundary → ADR-0036-T3 AC-4/AC-5 + ADR-0037-T3 AC-2/AC-4; the front-door safety-parity prerequisite → ADR-0036-T1 AC-2/AC-3/AC-4)
- [x] Constraint Propagation Table entries have corresponding ACs (the ADRs' mechanical guarantees carried verbatim into ACs: front-door-not-screened-route, debounce single-vs-sustained pair, mutation-control pair, crown-jewel 0-raw-PII wire-scan, held-domain-stays-held, deterministic paired interaction screen, load-time tripwire, zero-schema-change)

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section present (ADR-0036 OQ-1..OQ-5 + Negatives-1/2/3; ADR-0038 OQ-1..OQ-4 + Negative-2; ADR-0037 OQ-1..OQ-4 + Negatives-1/2; the LIVE-run downstream)
- [x] Every open question/pending tension/unmitigated risk has a disposition (1 Block → ADR-0036-T1; the rest Proceed with ACs; 1 Defer → the LIVE run)
- [x] Block dispositions have corresponding tasks (ADR-0036-T1 is the OQ-3/RT-06 front-door prerequisite every loop task depends on)
- [x] Defer dispositions have justifications (the operator-present LIVE run — operator-gated, after the build; every AC mock/fixture-satisfiable at 0 spend)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in the in-scope ADRs is covered (ADR-0036 N1 → T2; N2 → explicit disposition row (accepted cost, softened by ADR-0036-T4 rationale/confirmation); N3/RT-09 → ADR-0038-T3; ADR-0038 N1 → ADR-0038-T1; N2 → explicit disposition row (accepted cost, read-time composition); N3 → ADR-0038-T3; ADR-0037 N1 → ADR-0037-T3; N2 documented; findings A/B/C/D/E/F traced to ADR-0036-T1/T3 + ADR-0037-T1/T2/T3)

### Test Coverage
- [x] Every acceptance criterion appears in ≥1 Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (anti-degradation, held-domain, mutation-control pair, non-egress wire-scan, debounce, no-new-stream, emit-gate, dosing-reject, paired interaction screen, fail-closed, tripwire, reinserted-name)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the exemplar's structure (for machine parsing)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists at `main @ ad8afd7` (`server.py`, `route.py`, `confirm.py`, `care_chat.py`, `maintained.py`, `ADR-0001-...md` — all confirmed present)
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`scripts/serve/plan_loop.py`, `scripts/plan/horizons.py`, `scripts/plan/tailoring.py`, `tests/serve/test_plan_loop.py`, `tests/serve/test_plan_loop_regen.py`, `tests/plan/test_horizons.py`, `tests/plan/test_tailoring.py` — all confirmed absent)
- [x] Every ADR premise a task relies on was re-verified against the live tree and is still true (the screened-only `_do_generate_plan` path; no serve trigger/debounce/tailoring-hook/date-range-query today; D2 open-on-extras permits unknown keys; `TRACKED_DOMAINS` excludes peptides; no `plan-arc::` stream; `vault/artifacts/generated/` in `DATA_BEARING_PREFIXES`)
- [x] Every cited input declares its structural assumption AND the live file satisfies it (no phantom inputs — `run_orchestrated`, `plan_driver.drive`, `compose_disposition`, `orchestrate.reconcile`/`generate_plans`/`_held_result`, `router.summarize`/`_recent_trend_direction`/`rx_interaction_class_set`, `resolve_plan`/`record_plan`/`_check_fields`, `resolve_goal`/`_percent`, `read_events`/`EVENT_CATEGORIES`, `reemit_maintained`/`_assert_contained`/`_preserve_prior_content`, `mirror_registered`, `resolve_plan_progress`, `WIRED_TOKENS` all confirmed at the cited lines)
- [x] No task proposes an artifact that duplicates an existing capability (no existing loop trigger/debounce, no horizon read layer / date-range query, no tailoring pass, no `plan-arc::` stream — all ABSENT, which is why they are new/extended)
- [x] Repo-Grounding Ledger present, one row per task, all Grounded (no stale-premise / phantom-input / duplicate / action-mismatch found)
