---
source-specs: [docs/spec/adr-0036-0038-dynamic-plan-loop-spec.md]
adrs: [ADR-0036, ADR-0037, ADR-0038]
created: 2026-07-03
status: draft
total-waves: 7
critical-path-length: 7 tasks
estimated-effort: 17 task-days
---

# Build Plan: Dynamic Plan-Evolution Loop + Time Horizons + Care-Agent Tailoring (ADR-0036/0037/0038)

Scope: the approved three-ADR spec (10 tasks — ADR-0036 T1..T4, ADR-0038 T1..T3, ADR-0037 T1..T3) that closes the `plan → act → measure → adjust` loop and personalizes the plan against the operator's real data, in the design's build order (loop → horizons → tailoring). The build EXTENDS the built A′ inner engine, it does not rebuild it: the loop RE-ENTERS the composed front door (`run_orchestrated` → `plan_driver.drive` → the composed `gate_dispatch` + the five `orchestrate` cross-domain holds), horizons COMPOSE over three existing schema owners with zero new store schema, and tailoring renders ONLY into the gitignored `maintained` artifact through five mechanical gates.

The RT-06 safety prerequisite governs the whole build: today the serve layer's only plan-generation path is the screened-only `_do_generate_plan` ([server.py:592](../../scripts/serve/server.py)), which calls `orchestrate.generate_plans` DIRECTLY at [server.py:678](../../scripts/serve/server.py) with NO reauthor/adjudicator hook (held-stays-held, per-domain, no composition). **ADR-0036-T1 binds the automated trigger to the full-composition front door and forbids the screened-only path + `adjust.py` on the loop path; it is Wave 1 and it gates everything downstream — no loop or tailoring task starts until its checkpoint is green.** Finding-A safety-parity FAILS outright if any trigger reaches the screened-only route, so the anti-degradation guard is the earliest, highest-risk work.

Grounded live against `main @ 144c8e0` (HEAD, 2026-07-03). The manifest facts were re-confirmed by reading the live tree, not the spec prose: all seven Create targets (`scripts/serve/plan_loop.py`, `scripts/plan/horizons.py`, `scripts/plan/tailoring.py`, `tests/serve/test_plan_loop.py`, `tests/serve/test_plan_loop_regen.py`, `tests/plan/test_horizons.py`, `tests/plan/test_tailoring.py`) are ABSENT; all Modify targets are present; `_do_generate_plan` calls `generate_plans` directly at [server.py:678]; `run_orchestrated` is at [plan_orchestrator.py:127], `drive` at [plan_driver.py:144]; `adjust_plan` at [adjust.py:52]; the trigger sites `mirror_registered` ([route.py:166], [confirm.py:78]) + `respond` ([care_chat.py:239]) are present; `_percent`/`resolve_goal` ([goal_schema.py:122,189]), `EVENT_CATEGORIES`/`read_events` ([calendar_schema.py:44,138]), `TRACKED_DOMAINS`=`("workout","nutrition","supplements")` (peptides excluded) + `NO_PLAN_TODAY` ([plan_schema.py:50,46]) present; `reemit_maintained`/`_preserve_prior_content`/`_assert_contained` ([maintained.py:245,180,61]) present; the `SUMMARY_FIELD_SET` disjointness tripwire precedent ([router.py:668], [capture.py]) present; `scan_text_full` at [pii_scan.py:334]; `DATA_BEARING_PREFIXES` includes `vault/artifacts/generated/` ([.claude/hooks/lib/pii-scan-scope.sh:34] — design finding J closed). The `.venv` suite baseline is **2150 passed, 2 failed, 7 skipped** — the two failures (`tests/serve/test_bind.py::test_port_collision_exits_nonzero_fail_loud`, `tests/serve/test_server.py::test_main_reads_no_stdin`) are PRE-EXISTING and environment-sensitive (OS port-binding + stdin capture), unrelated to this scope; they are the known-red floor the wave checkpoints must not regress past, NOT this build's to fix.

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| `.venv` Python 3.14 test runtime (pytest + jsonschema, per `requirements.txt`) at the captured baseline | Every task runs `pytest`; the captured baseline (`2150 passed, 2 failed, 7 skipped` at `main @ 144c8e0`, the 2 failures pre-existing/env-sensitive) is the behavior-preservation precondition for every wave's suite-green gate. Capture the exact live counts at Wave-1 entry; the gate is "no NEW failure introduced", not an absolute number. | `.venv/bin/python -m pytest -q 2>&1 \| tail -1` (expect `… passed, 2 failed, 7 skipped`; a 3rd failure = regression) |
| Screened-only `_do_generate_plan` present + calling `generate_plans` directly (the path ADR-0036-T1 must NOT bind to) | ADR-0036-T1's anti-degradation guard (AC-3) asserts 0 calls to `_do_generate_plan` on the loop path; the target must exist to be excluded | `grep -q "def _do_generate_plan" scripts/serve/server.py && grep -q "generate_plans" scripts/serve/server.py && echo OK` |
| Composed front door `run_orchestrated` + `plan_driver.drive` + `SAFETY_BLOCKED` surface halt | ADR-0036-T1's `regenerate` drives `run_orchestrated` ([plan_orchestrator.py:127]) → `drive` ([plan_driver.py:144]); AC-6 asserts a not-True gate → `SAFETY_BLOCKED`/0 promoted | `grep -q "def run_orchestrated" scripts/plan/plan_orchestrator.py && grep -q "def drive" scripts/plan/plan_driver.py && grep -q "SAFETY_BLOCKED" scripts/plan/plan_driver.py && echo OK` |
| Per-domain `adjust.adjust_plan` present (the path the loop must NOT take) | ADR-0036-T1 AC-4 asserts 0 calls to `adjust.adjust_plan` ([adjust.py:52]) on the loop path (finding-A guard); the target must exist to be excluded | `grep -q "def adjust_plan" scripts/plan/adjust.py && echo OK` |
| The three serve trigger sites: `mirror_registered` (wearable + lab) + care-chat `respond` | ADR-0036-T2 wires `route.py`/`confirm.py` post-`mirror_registered` ([route.py:166], [confirm.py:78]) + `care_chat.respond` ([care_chat.py:239]) through one debounce gate | `grep -q "mirror_registered" scripts/serve/route.py && grep -q "mirror_registered" scripts/serve/confirm.py && grep -q "def respond" scripts/serve/care_chat.py && echo OK` |
| Care-lane derived-token gate `WIRED_TOKENS` (the finding-C de-id boundary) | ADR-0036-T3 AC-5 asserts the free-text trigger carries only the care-agent gate's derived tokens ([capture.py]); the crown-jewel non-egress rests on this being the only path | `grep -q "WIRED_TOKENS" scripts/serve/capture.py && echo OK` |
| Store schema owners: `goal_schema._percent`/`resolve_goal`, `calendar_schema.EVENT_CATEGORIES`/`read_events`, `plan_schema.TRACKED_DOMAINS`/`NO_PLAN_TODAY`/`record_plan` | ADR-0038-T1/T2/T3 compose the derived milestone percent, dated cadences, peptides-untracked guard, and the today-by-date-equality read over these single owners with zero new schema | `grep -q "def _percent" scripts/store/goal_schema.py && grep -q "EVENT_CATEGORIES" scripts/store/calendar_schema.py && grep -q "TRACKED_DOMAINS" scripts/store/plan_schema.py && grep -q "NO_PLAN_TODAY" scripts/store/plan_schema.py && echo OK` |
| ADR-0010 D2 open-on-extras seam: `plan_schema._check_fields` permits unknown keys by omission | ADR-0038-T2 rides the D2 seam to enrich `plan::<domain>` values with horizon-extra keys (`phase`/`week_intent`/`week_expectation`) with NO schema edit (AC-3 numstat=0 on `plan_schema.py`) | `grep -q "def _check_fields" scripts/store/plan_schema.py && grep -q "def record_plan" scripts/store/plan_schema.py && echo OK` |
| Single maintained writer: `reemit_maintained` + `_preserve_prior_content` + `_assert_contained` | ADR-0037-T1 renders tailored sections ONLY through `reemit_maintained` ([maintained.py:245]), reuses `_preserve_prior_content` ([:180]) for `(plan,date)` idempotency + `_assert_contained` ([:61]); no second name-bearing writer | `grep -q "def reemit_maintained" scripts/generate/maintained.py && grep -q "def _preserve_prior_content" scripts/generate/maintained.py && grep -q "def _assert_contained" scripts/generate/maintained.py && echo OK` |
| Interaction-class basis: `router.rx_interaction_class_set` + the additive-AE / Rx-BPMH lens sites | ADR-0037-T2 grounds the deterministic fail-closed interaction screen on `rx_interaction_class_set` ([router.py:198]) + the existing lens logic ([orchestrate.py:168,262]) | `grep -q "def rx_interaction_class_set" scripts/plan/router.py && echo OK` |
| PII value-scan `scan_text_full` + `SUMMARY_FIELD_SET` disjointness tripwire precedent + `DATA_BEARING_PREFIXES` covers `vault/artifacts/generated/` | ADR-0037-T3's load-time tripwire mirrors the `router`/`capture` disjointness asserts ([router.py:668]); the reinserted-name pre-ship check (AC-5) rests on the generated-artifact scan scope being closed | `grep -q "def scan_text_full" scripts/guard/pii_scan.py && grep -q "SUMMARY_FIELD_SET" scripts/plan/router.py && grep -q "vault/artifacts/generated/" .claude/hooks/lib/pii-scan-scope.sh && echo OK` |
| Seven Create targets ABSENT (Create-only, no duplicate/stale artifact) | ADR-0036-T1/T3, ADR-0038-T1, ADR-0037-T1 create the loop/horizons/tailoring modules + their tests; a pre-existing file would mean a duplicate (BP-06 / RGC-4) | `for f in scripts/serve/plan_loop.py scripts/plan/horizons.py scripts/plan/tailoring.py tests/serve/test_plan_loop.py tests/serve/test_plan_loop_regen.py tests/plan/test_horizons.py tests/plan/test_tailoring.py; do test -e "$f" && { echo "PRESENT $f"; exit 1; }; done && echo "ABSENT (Create OK)"` |
| Deployed specialist + safety-lens agents (`.claude/agents/{personal-trainer,nutritionist,supplement-specialist,peptide-specialist,medical-safety-reviewer,health-edge-case-reviewer,medical-liaison}`) | The loop's front-door re-gen dispatches each as a SUBSCRIPTION agent fulfilling an AUTHOR/GATE/lens request; the build is fixture-tested, the live dispatch is the downstream operator-present run | `for a in personal-trainer nutritionist supplement-specialist peptide-specialist medical-safety-reviewer health-edge-case-reviewer medical-liaison; do test -d .claude/agents/$a \|\| { echo "MISSING $a"; exit 1; }; done && echo OK` |

All prerequisites verified live against `main @ 144c8e0` on 2026-07-03. No Wave-1 task depends on an unlisted prerequisite (BP-08 clear): ADR-0036-T1 → `.venv` baseline + the screened-only `_do_generate_plan` (to exclude) + `run_orchestrated`/`drive`/`SAFETY_BLOCKED` + `adjust_plan` (to exclude) + the Create-absent probe; ADR-0038-T1 → `.venv` baseline + the store schema owners + the Create-absent probe.

## Wave Schedule

Seven waves are the spec's seven Kahn levels over the verified-acyclic dependency map (Dependency Map §; the loop chain ADR-0036-T1→T2→T3→T4→ADR-0037-T1→T2→T3 is fully serial because it is one continuously-mutated `scripts/serve/plan_loop.py` writer chain, and the horizon chain ADR-0038-T1→T2→T3 rides alongside in Waves 1-3). A wave's wall-clock is the max single-task estimate (tasks in a wave run in parallel); effort proxy = files-touched × criteria-count with the new-artifact / security-review / test-only modifiers. Every wave checkpoint carries four constraint invariants: front-door-binding (never the screened-only `_do_generate_plan` / `adjust.py` on the loop path), no-new-store-schema (0 new `::`-prefixed streams; `plan_schema.py` numstat=0 for the D2 enrichment), crown-jewel PII 0-leak (0 raw-PII past the de-id boundary into any dispatch payload or committed render), and MOCK/FIXTURE (0 live-API spend).

### Wave 1: Loop Front-Door Prerequisite (Anti-Degradation) ∥ Horizon Read Layer

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0036-T1 | Serve-trigger → driver front-door binding + anti-degradation guard (BUILD PREREQUISITE) | SE + Architect review + Security review | 2-3 days |
| ADR-0038-T1 | Horizon reads over `goal_schema` + `calendar_schema` (single-source progress, peptides-untracked, open-ended degradation) | SE + Architect review | 1-2 days |

**Entry Criteria:**
- All 13 Infrastructure Prerequisites verified (commands above return 0 / print OK).
- `.venv/bin/python -m pytest -q` baseline captured at `main @ 144c8e0` (`… passed, 2 failed, 7 skipped`; the 2 known env-sensitive serve failures are the floor, not a regression).
- `plan-integrity` has grounded the plan: every task's inputs confirmed against the LIVE tree (`stat`/`grep`, not the plan prose), the dependency map confirmed an acyclic DAG with artifact-named edges, each wave's checkpoint confirmed runnable.

**Exit Criteria / Checkpoint (Wave 1 → Wave 2):** see Checkpoint Protocol § Wave 1. The loop fires through the serve route producing exactly one NEW dated all-domain `plan::` set via the composed path (`run_orchestrated`→`drive`→`compose_disposition`+`orchestrate` reconciler); the anti-degradation guard records 0 `_do_generate_plan`, 0 bypass-`drive` `generate_plans`, 0 `adjust.adjust_plan` on the loop path; a held domain stays held; a not-True gate disposition returns `SAFETY_BLOCKED`/0 promoted; the horizon read derives the single-source milestone percent (`_percent` via `resolve_goal`), emits 0 peptide cadences, degrades an open-ended goal with 0 fabricated target-dates, and writes 0 new store streams. **This wave gates the entire loop + tailoring build — no downstream loop/tailoring task starts until this checkpoint RAN green.**

---

### Wave 2: Debounce + Three-Trigger Convergence ∥ D2 Extras-Seam Enrichment

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0036-T2 | Debounce + three-trigger convergence (derived state, no new store stream) | SE + Architect review | 2-3 days |
| ADR-0038-T2 | ADR-0010 D2 extras-seam enrichment on `plan::` values (zero schema change) | SE | 1 day |

**Entry Criteria:**
- Wave 1 checkpoint passed (the front-door binding + anti-degradation guard RAN green; the `regenerate` entry is the stable seam T2's shared debounce gate wraps; the horizon read layer T2's enrichment layers onto).
- The loop path confirmed screened-only-free at the Wave-1 boundary (T2's three trigger wirings must each reach the SAME `regenerate` front door, never the screened path).

**Exit Criteria / Checkpoint (Wave 2 → Wave 3):** see Checkpoint Protocol § Wave 2. A single-reading trigger produces 0 new plans while a sustained-signal trigger produces exactly 1 (a falsifiable pair); an absent-data cadence trigger surfaces a hold+prompt with 0 new plans; the debounce parameters (min-interval, window n/span, directional bar, free-text rate limit) are pinned numbers a deterministic test reads; a store scan finds 0 new `::`-prefixed ids (derived state); the three trigger call-sites (`route`/`confirm`/`care_chat`) each reach the one debounce gate and a second cross-kind trigger inside the window is dropped; the D2-enriched `plan::` document validates through `record_plan` AND a flat plan still validates, with `git diff --numstat` = 0 on `scripts/store/plan_schema.py`.

---

### Wave 3: Trend-Reaches-Regen + Mutation Control + Crown-Jewel Non-Egress ∥ Date-Range Query + Classifier

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0036-T3 | Trend-reaches-regen (finding B) + mutation control + crown-jewel non-egress through the serve entry point | SE + Security review | 1.5-2 days |
| ADR-0038-T3 | Date-range week/month query + latest-in-window selection + expectation-vs-actual classifier | SE | 1-2 days |

**Entry Criteria:**
- Wave 2 checkpoint passed (a sustained-signal fire is needed to drive the T3 mutation-control re-gen; the debounce gate is the stable entry the re-summarize path re-enters).
- The D2-enriched `plan::` values + the `week_expectation` extra confirmed at the Wave-2 boundary (ADR-0038-T3's date-range query reads them + the classifier compares against them).

**Exit Criteria / Checkpoint (Wave 3 → Wave 4):** see Checkpoint Protocol § Wave 3. A `biomarker::` series that changes `recent-trend-direction` reaches the re-gen via `router.summarize` with 0 reads of `plan-track::`; the behind→de-load and on-track→NOT-de-load dispositions differ (a falsifiable pair); a synthetic raw-PII token seeded into the raw intake and fired through the free-text trigger yields 0 raw-PII hits in any specialist dispatch payload; the free-text payload carries only care-agent derived tokens; a held domain with no clearing signal stays held; the four-horizon composition yields today/week/month/milestone from the same store with 0 new store keys, selects latest-in-window among same-window plans, preserves today-by-date-equality (`NO_PLAN_TODAY` when no render-date plan), and the deterministic (expectation, actual) classifier maps to a fixed behind/on-track/ahead verdict with no model call.

---

### Wave 4: Re-Gen Rationale + Large-Change Confirmation + Post-Promote Seams

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0036-T4 | Re-gen rationale + large-change confirmation + post-promote tailoring/adherence seams | SE + Architect review | 1.5-2 days |

**Entry Criteria:**
- Wave 3 checkpoint passed (T4's re-gen rationale reports the trend T3's re-summarize establishes; T4 is the sole remaining writer of `scripts/serve/plan_loop.py` + `scripts/serve/confirm.py` before the tailoring tail).
- The trend re-derivation (T3 AC-1) confirmed green (T4 AC-5 threads adherence as a SEPARATE input, verified against the trend re-derivation still succeeding with adherence absent).

**Exit Criteria / Checkpoint (Wave 4 → Wave 5):** see Checkpoint Protocol § Wave 4. Every automated re-gen produces a non-empty plain-language `rationale`; a change over the pinned magnitude threshold routes to the confirmation surface (0 large-change silent swaps) while a below-threshold change swaps without a prompt; the threshold is a fixed value a deterministic test reads; the post-promote tailoring-hook seam fires exactly once per re-gen (a pass-through until ADR-0037-T1 fills it); `resolve_plan_progress` is read as a separate adherence input (adherence absent does not block the trend-driven re-gen); a store scan finds 0 new `::`-prefixed ids on the rationale/adherence path.

---

### Wave 5: Care-Lane Tailoring Pass — Placement, Emit-Gate, Degrade-to-Safe, Artifact-Only

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0037-T1 | Care-lane tailoring pass — placement, emit-gate, degrade-to-safe, artifact-only, automated invocation | SE + Architect review + Security review | 2-3 days |

**Entry Criteria:**
- Wave 4 checkpoint passed (the tailoring pass fills the post-promote hook seam T4 established; it attaches at the post-record re-emit hook on the front-door promote).
- The front-door binding + held-domain-stays-held (Wave-1) + the post-promote seam (Wave-4) confirmed green (the pass emits ONLY on recorded, non-held domains and degrades to the un-tailored recorded plan on presentation failure).

**Exit Criteria / Checkpoint (Wave 5 → Wave 6):** see Checkpoint Protocol § Wave 5. The pass emits a tailored section referencing the operator's raw specifics for a recorded, non-held domain; a HELD domain gets 0 tailored sections; an injected `ModelCallError`/empty return degrades the affected domain to its un-tailored, de-identified, safety-cleared plan without crashing; a grep finds 0 `store.append`/store-key definitions and 0 second name-bearing writer (renders only through `reemit_maintained`); firing the loop on the automated cadence/`biomarker::` path with NO care-chat turn runs the pass exactly once after the promote; firing twice for the same `(plan, date)` produces 0 duplicate tailored sections.

---

### Wave 6: Dosing-Token Reject + Deterministic Fail-Closed Interaction Screen

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0037-T2 | Dosing-token reject + deterministic fail-closed interaction screen (paired control) | SE + Security review | 1-2 days |

**Entry Criteria:**
- Wave 5 checkpoint passed (the dosing-reject + interaction screen extend the tailoring pass; the pass's emit-gate + degrade posture are the stable base they add to).
- The compound-domain tailored output surface confirmed at the Wave-5 boundary (the dosing-token scan targets supplements/peptides output; the screen reads the operator's raw meds × supplements × peptides).

**Exit Criteria / Checkpoint (Wave 6 → Wave 7):** see Checkpoint Protocol § Wave 6. A dosing token in a compound domain's tailored output is REJECTED and the domain degrades to its un-tailored plan (0 compound-domain tailored sections carry a dosing token); a raw meds × supplements × peptides set intersecting a curated `rx-interaction-class` produces a "see your doctor" referral while a non-intersecting set produces none (a paired control — fires-on-known True AND fires-on-safe False); the screen runs as deterministic code whose verdict is unchanged when the presentation call is injected to fail; on a match the concern surfaces even with a suppressed/empty presentation (fail-closed, never silent drop).

---

### Wave 7: Load-Time Tripwire + Crown-Jewel Wire-Scan Non-Egress + ADR-0001 Egress Amendment

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0037-T3 | Load-time tripwire + crown-jewel wire-scan non-egress + ADR-0001 egress amendment | SE + Security review | 1-2 days |

**Entry Criteria:**
- Wave 6 checkpoint passed (the wire-scan runs the FULL tailoring path incl. the interaction screen; the tripwire audits the pass's egress keys).
- The interaction screen + dosing-reject confirmed green (the wire-scan dumps store streams + the de-identified dashboard payload after the full path runs).

**Exit Criteria / Checkpoint (Wave 7 → Done):** see Checkpoint Protocol § Wave 7. Adding any tailoring-artifact key to a `SUMMARY_FIELD_SET` copy REDs the import-time assert; a synthetic raw-PII token + every tailoring-artifact key are ABSENT from both the store streams and the de-identified dashboard payload after the full tailoring path (0 hits); the tailored sections appear ONLY in the gitignored `vault/artifacts/generated/` maintained artifact (0 in any tracked/committed render); ADR-0001's raw-egress list carries the tailoring carve-out + the `amended-by (from ADR-0037)` edge; a maintained artifact carrying the reinserted operator NAME is denied by the commit/push PII scan. **This is the terminal wave; the LIVE operator-present subscription run (real key + real data + spend; clinical reasoning-quality of the de-load/tailoring prose) is the downstream operator-gated attestation AFTER this build, NOT a wave.**

## Agent Assignment Matrix

SE implements every task (TDD per recipe). Security review is assigned per the crown-jewel/egress risk surface: ADR-0036-T1 (the front-door binding moves a safety disposition onto the automated trigger + adds the anti-degradation fail-closed guard), ADR-0036-T3 (the crown-jewel non-egress wire-scan over the specialist dispatch payloads — the finding-C de-id boundary), ADR-0037-T1 (the tailoring pass is a second raw-egress surface reading the operator's raw care-lane detail), ADR-0037-T2 (the deterministic fail-closed drug×supplement×peptide interaction screen — a shadow-prescribe safety vector), and ADR-0037-T3 (the load-time tripwire + crown-jewel wire-scan + the ADR-0001 egress amendment). Architect review is assigned on the contract/interface tasks: ADR-0036-T1 (the `regenerate` front-door binding is the shared seam every loop task consumes), ADR-0036-T2 (three-trigger cross-module wiring — `route`/`confirm`/`care_chat` converge on one debounce gate), ADR-0036-T4 (the post-promote seam contract — the tailoring-hook + adherence-input + confirm.py request shape that ADR-0037-T1 fills), ADR-0038-T1 (the horizon read-layer composition contract over three schema owners that T2/T3 consume), and ADR-0037-T1 (the tailoring-pass placement/lifecycle-hook contract in the driver→`reemit_maintained` lifecycle). ADR-0038-T2/T3 and ADR-0037-T2/T3 consume already-Architect-reviewed contracts (the D2 seam, the read layer, the tailoring pass) — implementation/audit work, no new cross-module contract, so no Architect review (BP-03 clear). QA verifies at every checkpoint. The `plan-integrity` role grounds the plan before the build and gates each wave transition (a wave advances only when its checkpoint Go/No-Go RAN green — executed, not reasoned); it is a read-only verification lens, not a deployed agent (correctly absent from `branch-completeness-audit`'s roster).

| Task ID | Agent | Reviewer(s) | Rationale |
|---------|-------|-------------|-----------|
| ADR-0036-T1 | SE | Architect, Security | Cross-module wire-shape break + crown-jewel: the `regenerate` front-door binding is the shared `drive`↔serve seam every downstream loop/tailoring task consumes → Architect; the anti-degradation guard (0 screened-only-path, 0 `adjust.py`) + the fail-closed `SAFETY_BLOCKED` surface is the finding-A safety-parity gate → Security. New-module + multi-AC + safety-guard modifiers raise the estimate. |
| ADR-0038-T1 | SE | Architect | Interface/contract: the horizon read-layer composition over `goal_schema`/`calendar_schema`/`plan_schema` (single-source progress, peptides-untracked, open-ended degradation) is the read contract ADR-0038-T2/T3 consume → Architect validates the composition seam. No PII/egress surface → no Security. |
| ADR-0036-T2 | SE | Architect | Cross-module wiring: three trigger sites (`route`/`confirm`/`care_chat`) converge on ONE shared debounce gate → Architect validates the convergence contract + the derived-state (no-new-store-stream) mechanism. Fixture-tested, no raw-egress surface → no Security. New-mechanism modifier raises the estimate. |
| ADR-0038-T2 | SE | — | Implementation: the D2 extras-seam enrichment writes `phase`/`week_intent`/`week_expectation` onto `plan::` values, permitted by omission — no schema edit, no new contract, no egress. Test-only-decrease offset by the zero-schema-change discipline. |
| ADR-0036-T3 | SE | Security | Crown-jewel non-egress: the finding-C de-id boundary — a synthetic raw-PII seed must not reach any specialist dispatch payload (the wire-scan) + the finding-B trend re-derivation via `router.summarize` + the mutation-control pair → Security. Drives the Wave-1 front-door contract (no new contract) → no Architect. |
| ADR-0038-T3 | SE | — | Implementation: the date-range week/month query + latest-in-window selection + the deterministic expectation-vs-actual classifier over the D2-enriched history — consumes the ADR-0038-T1 read contract + the ADR-0038-T2 extras, no new cross-module contract, no egress → SE only. |
| ADR-0036-T4 | SE | Architect | Interface/contract: the post-promote seams (the tailoring-hook pass-through + the adherence input + the confirm.py large-change request shape) are the contract ADR-0037-T1 fills → Architect validates the seam. Rationale/confirmation are internal serve-layer surfaces, not a raw-egress surface → no Security. |
| ADR-0037-T1 | SE | Architect, Security | Placement contract + crown-jewel raw egress: the pass hooks the driver→`reemit_maintained` lifecycle (the placement/idempotency contract ADR-0037-T2/T3 extend) → Architect; it reads the operator's RAW care-lane detail and renders a second raw-egress surface (artifact-only, emit-gate, degrade-to-safe) → Security. New-module + lifecycle-hook modifiers raise the estimate. |
| ADR-0037-T2 | SE | Security | Fail-closed safety screen: the dosing-token reject + the deterministic drug×supplement×peptide interaction screen that FAILS CLOSED to "see your doctor" is a shadow-prescribe safety vector (finding D) → Security per the crown-jewel rule (security wins ties). Extends the ADR-0037-T1 pass (no new contract) → no Architect. |
| ADR-0037-T3 | SE | Security | Crown-jewel wire-scan + egress amendment: the load-time `SUMMARY_FIELD_SET`-disjointness tripwire + the raw-PII/tailoring-key wire-scan over store + dashboard + the ADR-0001 raw-egress-list amendment + the reinserted-name pre-ship check are the terminal crown-jewel audit → Security. Audits the ADR-0037-T1/T2 surface (no new contract) → no Architect. |

**Multi-agent coordination flags:**
- **The loop chain ADR-0036-T1→T2→T3→T4→ADR-0037-T1→T2→T3 is one continuously-mutated `scripts/serve/plan_loop.py` writer chain**, serialized across Waves 1-7 so no two tasks co-occupy a wave writing that file (no BP-07 on it). The Architect-reviewed `regenerate` front-door seam from ADR-0036-T1 is the stable interface T2's debounce gate wraps, T3's re-summarize re-enters, T4's post-promote seams sit on, and ADR-0037-T1's tailoring pass attaches to; a later edit changing that seam triggers a contract-update notice to the Architect.
- **ADR-0036-T4's post-promote tailoring-hook seam is a pass-through that ADR-0037-T1 fills.** The seam (T4 AC-4: fires once per re-gen with the promoted plan + render target, no tailored content) is the Architect-reviewed contract; ADR-0037-T1's pass is the fulfilment. The deferral is a hard dependency: ADR-0037-T1's acceptance verifies the seam actually invokes the pass on the automated path (T1 AC-5), not merely that the pass exists.
- **The horizon chain ADR-0038-T1→T2→T3 rides parallel to the loop in Waves 1-3 on a DISJOINT file (`scripts/plan/horizons.py`, plus `test_horizons.py`).** In each of Waves 1/2/3 the horizon task and the loop task have disjoint manifests (Wave 1: `plan_loop.py`/`server.py` vs `horizons.py`; Wave 2: `plan_loop.py`/`route.py`/`confirm.py`/`care_chat.py` vs `horizons.py`; Wave 3: `plan_loop.py`/`test_plan_loop_regen.py` vs `horizons.py`) — true parallel execution, no intra-wave collision (BP-07 clear). ADR-0038 `enables` ADR-0036 SOFTLY (the loop works on the coarse `recent-trend-direction` without formal horizons), so no cross-chain dependency edge is required.

## Checkpoint Protocol

Each criterion is a SPECIFIC command / grep / numstat / count with an expected result and a verifier role. These gates are EXECUTED at `/execute-plan` time, not reasoned. The four constraint invariants (front-door-binding, no-new-store-schema, crown-jewel 0-leak, MOCK/FIXTURE 0-live-spend) are checkpoint invariants on every wave — no test opens a network socket or makes a live model/Agent-tool call. `<wave-base>` is the merge-base of the wave's branch with `main`; the store-adversarial obligation (bead `pka`) is satisfied by the suite-green gate re-running the existing battery across the change, since NO task adds a new `scripts/store/` write.

### Wave 1 → Wave 2 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/serve/test_plan_loop.py -q` → all pass, 0 failures [ADR-0036-T1 crit 7]
  - `.venv/bin/python -m pytest tests/plan/test_horizons.py -q` → all pass, 0 failures [ADR-0038-T1 crit 6]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline (still `2 failed` — the known env-sensitive `test_bind`/`test_server`; a 3rd failure = regression, HALT)
- **Front-door binding — exactly one composed re-gen (go/no-go):** firing the loop through the serve route with a fixture `dispatch` produces exactly one NEW dated `plan::<domain>` set across all `PLAN_DOMAINS` for the trigger date (count of new dated domain sets == 1), and a spy shows `run_orchestrated` entered + `compose_disposition` ([gate_dispatch.py]) + the `orchestrate` reconciler fired (count of `drive` entries on the loop path ≥ 1) [ADR-0036-T1 crit 1,2]
- **Anti-degradation guard (go/no-go):** a spy over the loop path records 0 `server._do_generate_plan`, 0 direct `orchestrate.generate_plans` that bypass `plan_driver.drive`, AND 0 `adjust.adjust_plan` — count of screened-only-path + per-domain-adjust invocations on the loop path == 0 [ADR-0036-T1 crit 3,4]
- **Held-domain-stays-held on re-gen (go/no-go):** a fixture whose new data holds a domain (additive-AE/conflict/Rx-BPMH) → that domain is NOT recorded on the re-gen (clearance re-derived per re-gen, never inherited) — count of held domains recorded past the hold == 0 [ADR-0036-T1 crit 5]
- **Fail-closed surface gate preserved (go/no-go):** a fixture whose GATE disposition returns `safety_passed` not-True → the run returns `SAFETY_BLOCKED` with 0 promoted plans — count of `plan::` rows promoted into `root` == 0 [ADR-0036-T1 crit 6]
- **Horizon derived single-source progress (go/no-go):** the horizon milestone percent EQUALS `goal_schema._percent(baseline, current, target)` for a seeded goal, and a grep confirms the only `_percent` caller feeding a horizon reading is via `resolve_goal` (no second progress site) [ADR-0038-T1 crit 1]
- **Peptides-untracked + open-ended degradation (go/no-go):** a `plan::peptides` fixture yields 0 peptide cadences (peptides ∉ `TRACKED_DOMAINS`); an open-ended goal resolves an honest percent with 0 fabricated target-dates in the horizon output [ADR-0038-T1 crit 3,4]
- **No-new-store-stream (go/no-go):** a store scan after the horizon read + after the loop re-gen finds 0 NEW `::`-prefixed item ids beyond the existing `plan::` promote (the loop re-uses the front-door `_promote_plans`→`store.append`, unchanged; the horizon read writes nothing) [ADR-0038-T1 crit 5]
- **Artifacts Present:** `scripts/serve/plan_loop.py` (created), `scripts/serve/server.py` (modified: `/plan-loop` POST branch), `scripts/plan/horizons.py` (created), `tests/serve/test_plan_loop.py` (created), `tests/plan/test_horizons.py` (created).
- **0-live-spend invariant:** every test runs against a fixture `dispatch` + seeded `biomarker::`/`goal::`/`calendar::events`/`plan::` fixtures (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the front-door-binding + anti-degradation + held-domain + fail-closed + horizon-progress + peptides/open-ended + no-new-stream gates all green, suite has no NEW failure, no blocking defect. **This is the gating checkpoint — the loop/tailoring build does not proceed until it RAN green.**
- **Verifier:** Architect (the `regenerate` front-door seam + the horizon read-layer contract) + Security (the anti-degradation guard + the fail-closed surface) + QA (test execution) + `plan-integrity` (gates the transition: confirms the checkpoint RAN green, executed not reasoned).

### Wave 2 → Wave 3 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/serve/test_plan_loop.py -q` → all pass, 0 failures [ADR-0036-T2 crit 7]
  - `.venv/bin/python -m pytest tests/plan/test_horizons.py -q` → all pass, 0 failures [ADR-0038-T2 crit 6]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Debounce single-vs-sustained pair (go/no-go):** a trigger with a single new `biomarker::` reading inside the window produces 0 new dated plans; a trigger after a sustained signal (≥ the pinned n readings across the pinned span meeting the directional-consistency bar) produces exactly 1 — count == 0 AND count == 1 (a falsifiable pair) [ADR-0036-T2 crit 1,2]
- **Absent data → hold + prompt (go/no-go):** the cadence trigger with NO new signal in the window produces 0 new plans AND returns a payload carrying a log-prompt flag [ADR-0036-T2 crit 3]
- **Debounce parameters pinned — binary (go/no-go):** a deterministic unit test reads the concrete min-interval, window n, span, directional-consistency bar, and free-text rate limit as fixed numbers (not runtime defaults) [ADR-0036-T2 crit 4]
- **No-new-store-stream — derived state (go/no-go):** a grep over `scripts/serve/plan_loop.py` + a store scan finds 0 new `::`-prefixed ids (no `loop::`/`debounce::`/`regen-marker::`) and 0 `store.append` of a debounce/last-re-gen record — the last-re-gen date is read from the dated `plan::` history, the window from the `biomarker::` series [ADR-0036-T2 crit 5]
- **Three triggers, one gate (go/no-go):** a spy confirms `route`/`confirm`/`care_chat` each reach the shared debounce entry, and a second cross-kind trigger inside the same window is dropped — count of new dated plan sets from two in-window triggers ≤ 1 [ADR-0036-T2 crit 6]
- **D2 enrichment rides the seam — zero schema change (go/no-go):** a `plan::<domain>` document carrying `phase`/`week_intent`/`week_expectation` validates through `record_plan`; a flat plan WITHOUT the extras also validates; `git diff --numstat <wave-base>..HEAD -- scripts/store/plan_schema.py` → 0 changed lines; a typo'd horizon key still validates and is ignored (no raise) [ADR-0038-T2 crit 1,2,3,5]
- **Artifacts Present:** `scripts/serve/plan_loop.py` (modified: debounce gate), `scripts/serve/route.py` + `scripts/serve/confirm.py` + `scripts/serve/care_chat.py` (modified: notify the debounced entry), `scripts/plan/horizons.py` (modified: D2 extras), `tests/serve/test_plan_loop.py` + `tests/plan/test_horizons.py` (modified).
- **0-live-spend invariant:** debounce + enrichment tests run against fixtures (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the single-vs-sustained pair + absent-data + pinned-params + derived-state + three-triggers-one-gate + zero-schema-change gates all green, suite has no NEW failure, no blocking defect.
- **Verifier:** Architect (the three-trigger convergence contract + the D2-seam-no-schema-edit) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 3 → Wave 4 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/serve/test_plan_loop_regen.py -q` → all pass, 0 failures [ADR-0036-T3 crit 7]
  - `.venv/bin/python -m pytest tests/plan/test_horizons.py -q` → all pass, 0 failures [ADR-0038-T3 crit 6]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Trend reaches re-gen — finding B (go/no-go):** a `biomarker::` series that changes `recent-trend-direction`, fired through the serve route, hands the re-summarized `summary` (via `router.summarize`) carrying the updated `recent-trend-direction` to the dispatch — with 0 reads of `plan-track::` required to carry it [ADR-0036-T3 crit 1]
- **Mutation-control pair (go/no-go):** a series trending BEHIND goal → the re-gen expresses a de-load-or-hold branch; a series ON-TRACK/AHEAD → the re-gen does NOT express the de-load branch — a test asserts the two dispositions are not equal (a falsifiable pair) [ADR-0036-T3 crit 2,3]
- **Crown-jewel non-egress — finding C (go/no-go):** a synthetic raw identifier (legal name) + raw meds seeded into the raw intake, fired through the free-text trigger → the specialist-lane dispatch payload carries 0 raw-PII tokens (count == 0) AND a spy confirms the free-text trigger's dispatch payload contains only care-agent-gate derived tokens + 0 raw free-text strings [ADR-0036-T3 crit 4,5]
- **Held-domain persistence on re-gen (go/no-go):** a domain held on the prior plan with no clearing signal stays held on the re-gen — count of silently un-held still-unsafe domains == 0 [ADR-0036-T3 crit 6]
- **Four-horizon composition + latest-in-window + today-by-equality (go/no-go):** for one render date the composition yields today's action (`timepoint` == render date), this-week's 7-day block, the month arc, and a `resolve_goal` milestone — all from the same store with 0 new store keys (a scan for `plan-arc::`/`horizon::`/`periodization::` == 0 hits); with multiple same-window dated plans the range query selects the latest-in-window; with no render-date plan the today slot reads `NO_PLAN_TODAY`, never the nearest date [ADR-0038-T3 crit 1,2,3]
- **Expectation-vs-actual classifier — deterministic (go/no-go):** a declared per-week `week_expectation` and an actual trend map to a fixed behind/on-track/ahead verdict with no model call; a grep confirms the classifier reads the derived goal percent + the date-range history and writes 0 new `::`-prefixed store item [ADR-0038-T3 crit 4,5]
- **Artifacts Present:** `scripts/serve/plan_loop.py` (modified: re-summarize path), `tests/serve/test_plan_loop_regen.py` (created), `scripts/plan/horizons.py` (modified: date-range query + classifier), `tests/plan/test_horizons.py` (modified).
- **0-live-spend invariant:** the mutation-control + wire-scan tests run against fixture dispatch + synthetic raw-PII seeds (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the finding-B trend + mutation-control pair + crown-jewel non-egress + held-domain persistence + four-horizon/latest-in-window/today-by-equality + deterministic classifier gates all green, suite has no NEW failure, no blocking defect.
- **Verifier:** Security (the crown-jewel non-egress wire-scan + the finding-C de-id boundary + the mutation-control safety branch) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 4 → Wave 5 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/serve/test_plan_loop.py -q` → all pass, 0 failures [ADR-0036-T4 crit 7]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Rationale recorded (go/no-go):** every automated re-gen returns a non-empty plain-language `rationale` field [ADR-0036-T4 crit 1]
- **Large change → confirmation, not silent swap (go/no-go):** a re-gen over the pinned change threshold routes to the confirmation surface and does NOT swap the standing plan until confirmed (count of large-change silent swaps == 0); a below-threshold change swaps without a confirmation prompt; the threshold is a fixed value a deterministic test reads [ADR-0036-T4 crit 2,3]
- **Post-promote tailoring-hook seam present (go/no-go):** a spy confirms the loop calls the post-promote tailoring hook exactly once per re-gen with the promoted plan + render target — the seam is a pass-through (no tailored content) until ADR-0037-T1 fills it (count of hook invocations per re-gen == 1) [ADR-0036-T4 crit 4]
- **Adherence a separate input, not the carrier (go/no-go):** the loop reads `resolve_plan_progress` as an additional input distinct from the trend — the trend re-derivation (Wave-3 T3 AC-1) still succeeds with `resolve_plan_progress` returning `has_tracking=False` (adherence absent does not block the trend-driven re-gen) [ADR-0036-T4 crit 5]
- **No-new-store-stream (go/no-go):** a store scan finds 0 new `::`-prefixed ids written by the rationale/adherence path [ADR-0036-T4 crit 6]
- **Artifacts Present:** `scripts/serve/plan_loop.py` (modified: rationale + large-change route + tailoring-hook seam + adherence input), `scripts/serve/confirm.py` (modified: large-change confirmation request shape), `tests/serve/test_plan_loop.py` (modified).
- **0-live-spend invariant:** rationale/large-change/adherence tests run against fixtures (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the rationale + large-change-confirmation + pinned-threshold + tailoring-hook-seam + adherence-separate-input + no-new-stream gates all green, suite has no NEW failure, no blocking defect.
- **Verifier:** Architect (the post-promote seam contract ADR-0037-T1 fills) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 5 → Wave 6 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_tailoring.py -q` → all pass, 0 failures [ADR-0037-T1 crit 7]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Personalized output (go/no-go):** the pass over a recorded, non-held `plan::<domain>` with raw care-lane detail (a peptide + a supplement) produces a maintained-artifact tailored section referencing the operator's actual raw specifics — the section is present [ADR-0037-T1 crit 1]
- **Emit-gate on held domain (go/no-go):** a HELD domain (additive-AE/conflict/Rx-BPMH so `_held_result` records `recorded: False`) gets 0 tailored sections; other domains may still tailor [ADR-0037-T1 crit 2]
- **Degrade-to-safe on model error (go/no-go):** an injected `ModelCallError`/empty return → the affected domain renders its un-tailored, de-identified, safety-cleared recorded plan and the run does not crash [ADR-0037-T1 crit 3]
- **Artifact-only via `reemit_maintained` (go/no-go):** a grep over `scripts/plan/tailoring.py` finds 0 `store.append`/store-key definitions and 0 second name-bearing writer (renders only through `reemit_maintained`) [ADR-0037-T1 crit 4]
- **Fires on the automated path (go/no-go):** firing the loop via the cadence/`biomarker::` trigger with NO care-chat turn runs the tailoring pass exactly once after the promote — count of tailoring-pass invocations on the automated re-gen == 1 (fills the Wave-4 seam) [ADR-0037-T1 crit 5]
- **Idempotent per `(plan, date)` (go/no-go):** firing the pass twice for the same `(plan, date)` produces 0 duplicate/stale tailored sections (reusing `_preserve_prior_content`) [ADR-0037-T1 crit 6]
- **Artifacts Present:** `scripts/plan/tailoring.py` (created), `scripts/generate/maintained.py` (modified: tailored-section keyword injector at the `reemit_maintained` boundary), `scripts/serve/plan_loop.py` (modified: fill the post-promote hook), `tests/plan/test_tailoring.py` (created).
- **0-live-spend invariant:** the pass runs against fixtures with fixture care-lane detail, 0 real operator PII in the test tree (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the personalized-output + emit-gate + degrade-to-safe + artifact-only + fires-on-automated-path + idempotency gates all green, suite has no NEW failure, no blocking defect.
- **Verifier:** Architect (the tailoring-pass placement/lifecycle-hook contract) + Security (the second raw-egress surface: emit-gate + artifact-only + degrade-to-safe) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 6 → Wave 7 Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_tailoring.py -q` → all pass, 0 failures [ADR-0037-T2 crit 6]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Dosing-token reject (go/no-go):** a dosing token in the tailored output for a compound domain (supplements/peptides) is REJECTED and the domain degrades to the un-tailored recorded plan — count of compound-domain tailored sections carrying a dosing token == 0 [ADR-0037-T2 crit 1]
- **Interaction screen — paired control (go/no-go):** a raw meds × supplements × peptides set intersecting a curated `rx-interaction-class` produces a "see your doctor" referral for the affected compound domain, AND a non-intersecting set produces no referral — fires-on-known == True AND fires-on-safe == False (a rule that fires on both or neither FAILS) [ADR-0037-T2 crit 2,3]
- **Deterministic + split off the model call (go/no-go):** with the presentation call injected to fail, the interaction screen's verdict is unchanged (the screen runs as deterministic code independent of the presentation call) [ADR-0037-T2 crit 4]
- **Fail-closed, never silent drop (go/no-go):** on an interaction match with a suppressed/empty presentation the referral still surfaces — it is never dropped [ADR-0037-T2 crit 5]
- **Artifacts Present:** `scripts/plan/tailoring.py` (modified: dosing-reject + deterministic interaction screen), `tests/plan/test_tailoring.py` (modified).
- **0-live-spend invariant:** the dosing-reject + paired-control tests run against fixtures (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the dosing-reject + the paired interaction-screen control + deterministic-split-off-model + fail-closed-never-silent-drop gates all green, suite has no NEW failure, no blocking defect.
- **Verifier:** Security (the fail-closed shadow-prescribe safety screen + the paired-control non-tautology) + QA (test execution) + `plan-integrity` (gates the transition).

### Wave 7 → Done Boundary

- **Tests:**
  - `.venv/bin/python -m pytest tests/plan/test_tailoring.py -q` → all pass, 0 failures [ADR-0037-T3 crit 6]
  - `.venv/bin/python -m pytest -q` → no NEW failure vs the captured baseline
- **Load-time tripwire (go/no-go):** adding a tailoring-artifact key to a `SUMMARY_FIELD_SET` copy makes the import-time assert RED — asserted by a test that adds a tailoring key and confirms the assert raises [ADR-0037-T3 crit 1]
- **Crown-jewel wire-scan non-egress (go/no-go):** a synthetic raw-PII token (legal name + raw drug name) seeded into the raw intake, the full tailoring path run, both the store streams AND the de-identified dashboard payload dumped → the raw tokens AND every tailoring-artifact key are ABSENT from both (count of raw-PII + tailoring-key hits in any store stream or the dashboard == 0) [ADR-0037-T3 crit 2]
- **Tailored content in the gitignored artifact only (go/no-go):** the tailored sections appear ONLY in the `maintained` artifact under `vault/artifacts/generated/` (via `reemit_maintained`) — count of tailored sections in any tracked/committed render == 0 [ADR-0037-T3 crit 3]
- **ADR-0001 egress list amended (go/no-go):** a grep over `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` finds the tailoring presentation carve-out entry AND the `amended-by (from ADR-0037)` edge [ADR-0037-T3 crit 4]
- **Reinserted-name pre-ship check (go/no-go):** a maintained artifact carrying the reinserted operator NAME (not only contact tokens) under `vault/artifacts/generated/` is DENIED by the commit/push PII scan (the `DATA_BEARING_PREFIXES` coverage) — count of committed reinserted-name artifacts that pass the scan == 0 [ADR-0037-T3 crit 5]
- **Artifacts Present:** `scripts/plan/tailoring.py` (modified: import-time `SUMMARY_FIELD_SET`-disjointness assert), `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` (modified: the tailoring carve-out + the `amended-by` edge), `tests/plan/test_tailoring.py` (modified: wire-scan + tripwire + reinserted-name checks).
- **0-live-spend invariant:** the wire-scan + tripwire tests run against synthetic PII seeds, 0 real operator PII in the test tree (0 live calls).
- **Go/No-Go:** all tests pass, all artifacts present, the load-time-tripwire + crown-jewel-wire-scan + artifact-only + ADR-0001-amendment + reinserted-name gates all green, suite has no NEW failure, no blocking defect. **The LIVE operator-present subscription run (real key + real data + spend; clinical reasoning-quality of the de-load/tailoring prose) is the downstream operator-gated attestation AFTER this build (out of plan scope); the live 0-raw-PII-to-a-REAL-agent property is the one residual crown-jewel property flagged for that checkpoint.**
- **Verifier:** Security (the load-time tripwire + the crown-jewel wire-scan over the DERIVED artifact + the egress amendment) + QA (full E2E + the reinserted-name pre-ship check) + `plan-integrity` (final gate: confirms the wire-scan RAN 0-hit on the wired path).

## Critical Path

```
ADR-0036-T1 → ADR-0036-T2 → ADR-0036-T3 → ADR-0036-T4 → ADR-0037-T1 → ADR-0037-T2 → ADR-0037-T3
```

- Length: 7 tasks (Waves 1→2→3→4→5→6→7 — one loop/tailoring task per wave boundary on the path; 6 wave boundaries).
- Zero-slack tasks: ADR-0036-T1, ADR-0036-T2, ADR-0036-T3, ADR-0036-T4, ADR-0037-T1, ADR-0037-T2, ADR-0037-T3.
- The path is the actual longest chain: it is one fully-serialized `scripts/serve/plan_loop.py` writer chain (T1 binds the front door → T2's debounce gate wraps it → T3's re-summarize re-enters it → T4's post-promote seams sit on it → ADR-0037-T1's tailoring pass fills T4's seam → T2's screen extends the pass → T3's audit scans the pass). Each of ADR-0036-T1..T4 and ADR-0037-T1..T3 is the sole loop/tailoring task in its wave, so the topological depth is exactly 7 and the path length equals it. No task on the path has an alternative shorter route (the chain is strictly serial by the shared-file writer ordering + the tailoring-hook `enables` edge).
- Non-critical tasks with slack (the ADR-0038 horizon chain, which rides parallel in Waves 1-3):
  - **ADR-0038-T1: ~1 day within-wave slack** — in Wave 1 alongside ADR-0036-T1 (the wave's 2-3d critical task); ADR-0038-T1's 1-2d estimate can slip within the wave without moving the Wave-1 checkpoint. Its downstream (ADR-0038-T2/T3) is a self-contained chain terminating at ADR-0038-T3 (a leaf — horizons `enable` the loop softly, no hard downstream consumer), so the chain has large total float, operationally bounded to complete by the Wave-3 checkpoint.
  - **ADR-0038-T2: ~2 days slack** — in Wave 2 alongside ADR-0036-T2 (the wave's 2-3d critical task); its 1d estimate is the least-constrained on the schedule (rides the D2 seam, test-only-adjacent).
  - **ADR-0038-T3: off the named longest chain** — in Wave 3 alongside ADR-0036-T3; both complete by the Wave-3 checkpoint. ADR-0038-T3 is a leaf (its four-horizon view is composed at read time, consumed by the render, not by the loop), so it carries slack until plan end but is gated to the Wave-3 boundary; it is NOT on the critical path because the loop/tailoring chain extends four more waves past it.

## Risk Schedule

- **Spikes:**
  - NONE. This build has no `T0`-suffixed research task. The highest-risk entries — the front-door binding + anti-degradation guard (ADR-0036-T1) and the crown-jewel non-egress wire-scan (ADR-0036-T3) — are BOTH full build tasks placed as early as the strict topological chain permits (Wave 1 and Wave 3), not spikes; their open questions (OQ-1 debounce numbers, OQ-2/OQ-4/OQ-5 convergence/confirmation/state mechanics) are resolved in-task during TDD, bounded by their ACs (the debounce numbers are ADR-0036-T2 binary ACs). Stated explicitly per wave-scheduling Rule-1 exception: where the high-risk work is a build task rather than knowledge-gathering, "spikes-in-Wave-1" is satisfied by placing the front-door prerequisite (ADR-0036-T1) in Wave 1 — the earliest the chain permits — as the gate on everything downstream.
- **Risk-mitigating tasks (risk-mitigating-before-mitigated):**
  - **ADR-0036-T1 (Wave 1, the front-door binding + anti-degradation guard)** mitigates the finding-A safety-parity gap (a trigger reaching the screened-only `_do_generate_plan` skips the composition) via the anti-degradation ACs (0 screened-only-path, 0 `adjust.py`, held-domain-stays-held, fail-closed `SAFETY_BLOCKED`) — scheduled BEFORE every task that drives the loop (T2 Wave 2, T3 Wave 3, T4 Wave 4, ADR-0037-T1/T2/T3 Waves 5-7). It is the gate on the whole build.
  - **ADR-0036-T2 (Wave 2, the debounce)** mitigates the per-trigger-cost risk (ADR-0036 Consequence-Negative-1: re-running the full front door is more expensive than a per-domain patch) via the min-interval + sustained-signal-window bound on trigger frequency — in place BEFORE the mutation-control re-gen (T3) and the tailoring pass (ADR-0037-T1) that each ride a fired re-gen.
  - **ADR-0036-T3 (Wave 3, the crown-jewel non-egress + mutation control)** mitigates the finding-C de-id-boundary breach (raw operator text reaching the specialist dispatch) via the wire-scan (0 raw-PII in any dispatch payload) + the derived-tokens-only assertion — BEFORE the tailoring pass (ADR-0037-T1) reads raw care-lane detail. It also mitigates the finding-B bridge risk (a trend needing a `plan-track::` bridge) via the free re-summarize.
  - **ADR-0037-T1 (Wave 5, the tailoring pass)** mitigates the shadow-prescribe-a-held-domain risk (finding D) via the emit-gate (0 tailored sections for a held domain) + the degrade-to-safe posture — BEFORE ADR-0037-T2 adds the dosing-reject/interaction screen and ADR-0037-T3 audits the egress.
  - **ADR-0037-T2 (Wave 6, the fail-closed interaction screen)** mitigates the dose-an-investigational-compound risk (finding D) via the dosing-token reject + the deterministic fail-closed drug×supplement×peptide screen — BEFORE the terminal wire-scan (ADR-0037-T3) runs the full path.
  - **ADR-0037-T3 (Wave 7, the load-time tripwire + wire-scan)** mitigates the second-raw-egress-surface-to-audit risk (ADR-0037 Consequence-Negative-1) via the `SUMMARY_FIELD_SET`-disjointness tripwire + the crown-jewel wire-scan over the derived artifact + the ADR-0001 egress amendment + the reinserted-name pre-ship check — the terminal crown-jewel audit, fail-closed on a planted leak.
- **Security-sensitive / crown-jewel ordering:**
  - The front-door binding + anti-degradation guard (ADR-0036-T1, Wave 1) — which forbids the screened-only path + `adjust.py` on the loop path and preserves the `SAFETY_BLOCKED` surface — is built FIRST, before any task that drives the loop. Finding-A safety-parity is locked at Wave 1; it is the gate on the whole build.
  - The crown-jewel non-egress wire-scan (ADR-0036-T3, Wave 3) — the finding-C de-id boundary (0 raw-PII in any specialist dispatch payload) — precedes the tailoring pass (ADR-0037-T1, Wave 5) that reads raw care-lane detail. The raw-egress surface is audited from both directions: the dispatch-payload wire-scan (T3) before the artifact wire-scan (ADR-0037-T3, Wave 7).
  - The tailoring raw-egress chain is ordered emit-gate/degrade (ADR-0037-T1) → dosing-reject/fail-closed screen (ADR-0037-T2) → load-time tripwire/wire-scan/egress-amendment (ADR-0037-T3): each safety gate precedes the audit that verifies it, and the ADR-0001 egress-list amendment lands with the terminal audit that scopes it.
  - Security review is assigned on every crown-jewel/egress task (ADR-0036-T1/T3, ADR-0037-T1/T2/T3) and is NOT deferred past the wave where the implementation occurs.
  - **Build-vs-runtime divergence must be PRESERVED at execute time (verifier watch-item):** every build task drives a FIXTURE `dispatch` + fixture GATE verdicts + fixture care-lane detail + synthetic PII seeds, never a live raw intake; at RUNTIME only the serve front door feeds a real raw intake into the de-id boundary, and only the de-identified summary reaches the specialist dispatch. The `plan-integrity` verifier + Security MUST confirm at execute time that the build tasks' drivers are fed ONLY fixtures (no live de-id-IN or live Agent-tool dispatch enters the build path) — a watch-item, not a one-time check.

## Cross-Spec Coordination

Single-spec plan (one source spec: `docs/spec/adr-0036-0038-dynamic-plan-loop-spec.md`, covering ADR-0036/0037/0038). No cross-spec coordination required.

**Intra-spec shared-file sequencing** (within-spec, dependency-ordered — not a BP-07 violation because each co-modified file is touched in dependency-ordered waves, never two tasks sharing a file in one wave):

| Shared File | Tasks (wave) | Resolution |
|-------------|--------------|------------|
| `scripts/serve/plan_loop.py` | ADR-0036-T1 (W1, Create) ; ADR-0036-T2 (W2, Modify) ; ADR-0036-T3 (W3, Modify) ; ADR-0036-T4 (W4, Modify) ; ADR-0037-T1 (W5, Modify — fill the post-promote hook) | Five modifiers in strictly dependency-ordered waves (W1<W2<W3<W4<W5). Each builds on the prior wire shape; no two share a wave → no collision. |
| `scripts/serve/confirm.py` | ADR-0036-T2 (W2, Modify — notify the debounced entry) ; ADR-0036-T4 (W4, Modify — large-change confirmation request shape) | Two modifiers in dependency-ordered waves (W2<W4). No co-occupied wave → no collision. |
| `scripts/plan/horizons.py` | ADR-0038-T1 (W1, Create) ; ADR-0038-T2 (W2, Modify) ; ADR-0038-T3 (W3, Modify) | Create-then-extend across W1→W2→W3, dependency-ordered. Disjoint from the loop file in every wave. No co-occupied wave → no collision. |
| `scripts/plan/tailoring.py` | ADR-0037-T1 (W5, Create) ; ADR-0037-T2 (W6, Modify) ; ADR-0037-T3 (W7, Modify) | Create-then-extend across W5→W6→W7, dependency-ordered. No co-occupied wave → no collision. |

Within-wave shared-file check (parallel-execution safety): Waves 4, 5, 6, 7 are single-task waves (no intra-wave collision possible). Waves 1/2/3 each pair one loop task with one horizon task on DISJOINT manifests (W1: `plan_loop.py`/`server.py` vs `horizons.py`; W2: `plan_loop.py`/`route.py`/`confirm.py`/`care_chat.py` vs `horizons.py`; W3: `plan_loop.py`/`test_plan_loop_regen.py` vs `horizons.py`) — no intra-wave collision (BP-07 clear).

## Feedback Protocol

| Issue Type | Action | Blocks Plan? |
|-----------|--------|-------------|
| Spec defect (untestable criteria) | Flag for spec revision, log in `docs/build-plan/.pipeline/adr-0036-0038/deviations.md`; halt the affected wave | Yes — checkpoint cannot verify the criterion |
| Missing dependency discovered | Add the edge, re-run wave generation (Kahn), re-validate topological ordering; log the adjusted schedule | No — plan self-corrects in place |
| Acceptance criteria untestable | Flag for spec revision with the specific task-ID + criterion number | Yes — cannot verify completion |
| Scope change needed | Halt execution, escalate to user (the scope is fixed by ADR-0036/0037/0038; a new requirement is a new spec/ADR) | Yes — plan scope is fixed |
| File manifest conflict (two tasks co-modify a file in one wave with no ordering) | Flag for spec revision, identify the conflicting tasks, apply non-overlap verification or add a dependency edge | Yes — execution order unclear until resolved |
| Task too large for a single wave | Split recommendation in the deviations log, adjust the wave schedule | No — plan accommodates the split |
| Missing task (coverage gap — an in-scope ADR section with no task) | Flag for spec revision naming the uncovered ADR section | Yes — plan would be incomplete |
| **Front-door-binding violation (a trigger reaches `_do_generate_plan` / `adjust.py` on the loop path)** | HALT the wave immediately; the screened-only route skips the composition (finding-A safety-parity failure); route to the responsible task's SE to re-bind to `run_orchestrated`→`drive`; re-run the anti-degradation guard before resuming | Yes — a screened-only re-gen is the ADR-0036 RT-06 failure class |
| **Crown-jewel 0-leak gate RED at a checkpoint** | HALT the wave; do NOT advance; route to the responsible task's SE; re-run the full 0-leak gate (the dispatch-payload wire-scan (ADR-0036-T3) + the artifact wire-scan + tripwire (ADR-0037-T3)) before resuming | Yes — a leak past the de-id boundary or into a committed render is release-blocking (ADR-0005 falsification) |
| **No-new-store-schema violation (a new `::`-prefixed stream, or non-zero numstat on `plan_schema.py`)** | HALT; the debounce state must be DERIVED (dated `plan::` history + `biomarker::` window) and the horizon extras must ride the D2 seam; route back to SE to remove the new stream / schema edit | Yes — a materialized loop/horizon stream is the ADR-0038 no-new-store-schema failure class |
| **Emit-gate / fail-closed violation (a held domain gets tailored content, or an interaction match is silently dropped)** | HALT; the tailoring pass must emit ONLY on recorded, non-held domains and the interaction screen must FAIL CLOSED to "see your doctor"; route back to SE to fix the gate/screen | Yes — shadow-prescribing a held/interacting domain is the ADR-0037 finding-D failure class |
| **0-live-spend violation (a test makes a live API or Agent-tool call)** | HALT; replace the live call with the fixture-`dispatch` / fixture-GATE / fixture-care-detail seam; the live run is the post-build operator checkpoint only | Yes — live spend in a build test breaks the mock-tested-posture invariant |

Blocking issues halt the pipeline with: "Spec revision needed before build-plan execution can continue. Issues: [list]. Run `/create-spec` to update the spec, then re-run `/create-build-plan`." Non-blocking issues are logged in `docs/build-plan/.pipeline/adr-0036-0038/deviations.md` (issue, original plan state, adjusted state, justification) and execution continues.

## Validation Checklist

### Wave Integrity
- [x] Every task appears in exactly one wave (all 10 spec tasks: W1×2, W2×2, W3×2, W4×1, W5×1, W6×1, W7×1 = 10).
- [x] No task is scheduled in a wave before its dependency's wave (0036-T2 dep T1: W2>W1; T3 dep T1+T2: W3>W1,W2; T4 dep T1+T2+T3: W4>W1,W2,W3; 0037-T1 dep 0036-T1+T3+T4: W5>W1,W3,W4; 0037-T2 dep 0037-T1: W6>W5; 0037-T3 dep 0037-T1+T2: W7>W5,W6; 0038-T2 dep 0038-T1: W2>W1; 0038-T3 dep 0038-T1+T2: W3>W1,W2 — all strictly earlier).
- [x] Topological ordering respected across all waves (the seven waves are the spec's seven Kahn levels, verified against the spec Dependency Map).

### Checkpoint Quality
- [x] Every wave boundary has at least one verifiable exit criterion (7 boundaries, each with named test commands + numstat/grep/count 0-threshold gates).
- [x] Every checkpoint names specific test commands or conditions (exact `pytest`/`git diff --numstat`/`grep`/count/falsifiable-pair invocations, not "run tests").
- [x] Every checkpoint identifies a verifier role (Architect/Security + QA + `plan-integrity` per boundary).

### Agent Assignment
- [x] Every spec task appears in the Agent Assignment Matrix (all 10).
- [x] No implementation task assigned to Architect (SE is primary on all 10; Architect is reviewer only on 0036-T1/T2/T4, 0038-T1, 0037-T1).
- [x] No interface/contract task assigned to SE without Architect review (0036-T1 front-door seam, 0036-T2 three-trigger convergence, 0036-T4 post-promote seam, 0038-T1 read-layer contract, 0037-T1 placement contract — all carry Architect review; the consuming tasks 0038-T2/T3, 0037-T2/T3 have no new contract).
- [x] Security-sensitive tasks have Security review assigned (the five crown-jewel/egress tasks: 0036-T1 front-door binding + anti-degradation, 0036-T3 non-egress wire-scan, 0037-T1 raw-egress tailoring pass, 0037-T2 fail-closed interaction screen, 0037-T3 wire-scan + egress amendment).

### Critical Path
- [x] Critical path is the actual longest chain (0036-T1→T2→T3→T4→0037-T1→T2→T3, length 7 = total loop/tailoring wave depth; verified by counting — each is the sole loop/tailoring task in its wave).
- [x] Zero-slack tasks identified (the 7 chain tasks; the ADR-0038 horizon chain carries slack, documented).
- [x] No task on the critical path has an alternative shorter route (the chain is strictly serial by the shared `plan_loop.py` writer ordering + the tailoring-hook `enables` edge; no shorter route).

### Risk Ordering
- [x] All spike tasks are in Wave 1 (NONE exist — stated explicitly; the front-door prerequisite 0036-T1 is in Wave 1 per the Rule-1 exception, gating the whole build).
- [x] Risk-mitigating tasks precede the tasks they protect (0036-T1 before T2/T3/T4 + all tailoring; 0036-T3 non-egress before 0037-T1 raw read; 0037-T1 emit-gate before T2 screen before T3 audit; documented in Risk Schedule).
- [x] Security ordering correct (the front-door binding + anti-degradation in Wave 1; the crown-jewel non-egress wire-scan in Wave 3 before the raw-egress tailoring pass in Wave 5; the terminal artifact wire-scan + egress amendment in Wave 7 — each before/at the surface it protects; Security review through the terminal wave).

### Spec Traceability
- [x] Every spec task appears in the wave schedule (10/10; no orphan).
- [x] No task in the plan is absent from the source spec (every plan task ID traces to a spec task block).
- [x] `source-specs` frontmatter lists the consumed spec.

### Infrastructure
- [x] Every prerequisite has a verification command (12 prerequisites, each with a runnable command verified live 2026-07-03).
- [x] Wave 1 tasks do not depend on an unlisted prerequisite (0036-T1 → .venv baseline + screened-only `_do_generate_plan` (exclude) + `run_orchestrated`/`drive`/`SAFETY_BLOCKED` + `adjust_plan` (exclude) + Create-absent probe; 0038-T1 → .venv baseline + store schema owners + Create-absent probe — all listed; BP-08 clear).

### Feedback Protocol
- [x] Feedback protocol section is present.
- [x] Protocol covers: spec defect, missing dep, untestable criteria, scope change, file conflict, oversized task, missing task (+ five project-specific front-door-binding / crown-jewel-leak / no-new-store-schema / emit-gate-fail-closed / live-spend categories).
- [x] Each issue type has a blocking/non-blocking classification.

All 24 base checklist items pass. No BP-01..BP-08 anti-pattern present: BP-01 no dependency violation (strict topological waves); BP-02 every checkpoint has commands + verifier (no empty checkpoint); BP-03 SE-primary with correct reviewers, no contract task without Architect review; BP-04 seven waves = topological depth 7, no over-serialization (the loop chain is a genuine serial writer chain, the horizon chain rides parallel in Waves 1-3, not padded); BP-05 no deferred spike/risk-mitigating task (the front-door prerequisite is Wave 1; each mitigating task precedes the mitigated); BP-06 no orphan (10 spec tasks ↔ 10 plan tasks); BP-07 no intra-wave file collision (the co-modified `plan_loop.py`/`confirm.py`/`horizons.py`/`tailoring.py` are touched in dependency-ordered waves; Waves 1-3 pair disjoint loop/horizon manifests); BP-08 no phantom infrastructure (every Wave-1 requirement is a listed prerequisite).
