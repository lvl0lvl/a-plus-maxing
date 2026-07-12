---
scope: "ADR-0041 ADR-0042 ADR-0043 ADR-0044 ADR-0045 ADR-0046 (Comprehensive Plan-Platform Re-Architecture, Tiers 1-3)"
adrs: [ADR-0041, ADR-0042, ADR-0043, ADR-0044, ADR-0045, ADR-0046]
tier: 3
created: 2026-07-11
status: approved
---

# Spec: Comprehensive Plan-Platform Re-Architecture (ADR-0041…0046)

## Component Overview

This spec implements the six-ADR plan-platform re-architecture that fixes the two root causes the set names (`docs/adr/.pipeline/discovery.md`): **DATA-COLLAPSE** (the plan path collapses the operator's full record to `router.summarize`'s closed ~18-token `SUMMARY_FIELD_SET` band before any specialist sees it) and **NO-LOOP** (a one-shot generator with no plan-compiled monitoring tier). It delivers, in tier order, the full authoring→monitoring spine: a uniform seven-field **DOMAIN PROGRAM** schema (ADR-0041), a **Context Assembler** that feeds specialists the identity-stripped full record (ADR-0042), a care-agent **Orchestrator** that decompose→brief→collect→reconcile→synthesizes one plan (ADR-0043), a **comprehensive Plan Model** that stores it intact (ADR-0044), a **plan-compiled monitoring config + four-tier deterministic executor** (ADR-0045), and a **dispatch scale-up** from 4 to the 15+-specialist roster with progressive activation (ADR-0046).

Tier ordering is fixed by `docs/adr/.pipeline/dag.md`: **Tier 1** = {ADR-0041 schema, ADR-0042 assembler} (peer foundations); **Tier 2** = {ADR-0043 orchestrator, ADR-0044 model, ADR-0046 dispatch}; **Tier 3** = {ADR-0045 monitoring}. The constraint-propagation is transitive: ADR-0041's uniform shape constrains the orchestrator (reconciles it), the model (stores it), the monitoring compiler (compiles fields 3-4), and the dispatch scale-up (each dispatched specialist emits it); ADR-0043 redefines the loop's re-entry front door (constrains ADR-0036); ADR-0044's model is where ADR-0045's compiled config must live (`constrains` ADR-0045). This spec's tasks are dependency-ordered to that DAG, and each downstream task's acceptance criteria carry the upstream constraint.

Four of the six ADRs break the ADR-0032 EXTEND-NOT-REBUILD freeze on the plan spine (the load-bearing operator-adjudication point that has held byte-frozen for ~15 sessions): ADR-0041 supersedes the four thin translators + `assemble._is_complete`; ADR-0042 supersedes the plan-path `router.summarize` collapse; ADR-0043 generalizes the SAFETY-CRITICAL `orchestrate.reconcile` five holds; ADR-0044 supersedes the `plan_schema.py` record spine. The set-wide frozen-spine operator sign-off was OBTAINED at the Phase-1 gate (`discovery.md`); this spec does not re-gate it. Every freeze break is verified by a **per-ADR-scoped numstat probe** (each ADR's `git diff --numstat` scoped to its OWN commit delta, excluding sibling-superseded files, so the probes never forbid each other's intended supersession), and the **crown-jewel genetics carve-out** is preserved: raw rsID+allele genotypes NEVER cross to the planner — genetics reaches the assembled record ONLY as ADR-0032's derived, de-id-by-construction coarse `genetic-trait-classes` token (RT-008). The HARD record WRITE primitive `store.append` / `keying.py` plus `pipeline.py` and `adjudicate.py` stay **byte-frozen** (the comprehensive plan rides `store.append` unchanged as a richer VALUE — disposition #14).

**Stated assumptions (the 30 PROCEED dispositions, resolved in-spec — `docs/spec/.pipeline/dispositions.md`):** the ADR-0041 migration uses a **transitional additive adapter**, not a big-bang cutover (#2); required fields are `prescription`/`rationale`/`monitoring_signals`/`adjustment_rules`, conditional are `required_labs`/`refusal-escalation`/`cross_domain_seams` (#3); the assembler strips **name/contact/exact-DOB only**, reusing the `pii_scan` / `_care_profile` identity-strip precedent, designing no new de-id scheme (#5); `router.summarize` **persists** for its non-plan roles (#7); the orchestrator keeps the SAFETY holds (RED-S/LEA, additive-AE, Rx-BPMH) as **always-on floors**, softer reconciliations become specialist-authored seams (#9); the comprehensive plan **rides the frozen `store.append`** (#14); a **mixed-history-tolerant reader** over forward migration (#16); the daily deterministic pass hosts in the **built ADR-0039 runner** (#20); gate at **DISPATCH** (#24); `LARGE_CHANGE_THRESHOLD_DOMAINS` re-bases as a **FRACTION** of the active set before the scaled loop runs (#36). Every build task is mock/fixture-satisfiable at **0 live-API spend and 0 real operator PII**; the six DEFER items are the operator-present LIVE runs (real specialist dispatches spend model budget), recorded in the Unresolved-Concerns table below, uniform with the ADR-0032 / ADR-0039 pattern.

Informing artifacts (downstream workers load on demand): the six source ADRs (`docs/adr/ADR-004{1..6}-*.md`); the extraction + DAG (`docs/spec/.pipeline/context.md`, `docs/adr/.pipeline/{dag,discovery}.md`); the roster + per-specialist plan contracts (`design/specialist-plan-contracts.md`, the 18-agent roster: 13 card-emitting domain specialists §1-§13, genetics-specialist §14 + labs-specialist §15 as cross-cutting inputs); the store-adversarial mandate (`docs/checklists/store-adversarial-tests.md`); the built ADR-0039 runner host (`scripts/runner/`); and the format-exemplar (`docs/spec/adr-0039-scheduled-agent-runner-spec.md`).

## Unresolved Concerns Disposition

The full 36-concern roster is dispositioned in `docs/spec/.pipeline/dispositions.md` (orchestrator-dispositioned per the S128 standing directive: resolve in-spec, surface only operator-owned decisions; NONE of the 36 required operator adjudication). The **30 PROCEED** items are resolved in-spec — folded into the stated assumptions above and the task acceptance criteria below (each PROCEED disposition maps to a task or an AC, cited per-task). The **6 DEFER** items are the operator-gated LIVE runs, recorded here:

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0041 OQ-4 | Open Question (LIVE) | Operator-present LIVE run: real specialist dispatches author DOMAIN PROGRAMs end-to-end; spends model budget. | **Defer** | Operator-gated real spend AFTER the build (the ADR-0032/0039 pattern). Every ADR-0041 build AC is fixture-satisfiable at 0 spend; the metered form is the LIVE attestation. No task. |
| ADR-0042 OQ-4 | Open Question (LIVE) | Operator-present LIVE run: the full identity-stripped record reaches a live specialist; spends money. | **Defer** | Operator-gated real spend (post-build). The crown-jewel identity-leak + no-collapse probes are fixture-satisfiable; the live egress is the operator-present attestation. No task. |
| ADR-0043 OQ-4 | Open Question (LIVE) | Operator-present LIVE run: the orchestrator dispatches over live specialists; spends model budget. | **Defer** | Operator-gated real spend (post-build). The emit-N-briefs + synthesize-reconciled-plan probes run on fixtures. No task. |
| ADR-0044 OQ-5 | Open Question (LIVE) | Operator-present LIVE run: comprehensive plans authored end-to-end; spends money. | **Defer** | Operator-gated real spend (post-build). The round-trip-fidelity + standing-resolution + ADR-0040-re-base probes run on fixtures. No task. |
| ADR-0045 OQ-4 | Open Question (LIVE) | Operator-present LIVE run: a real Tier-2 escalation spends model budget + fires the metered de-id-IN call. | **Defer** | Operator-gated real spend (post-build). The no-event-day 0-model-call + finding-A-parity + human-gate-hold probes run deterministically on fixtures. No task. |
| ADR-0046 OQ-4 | Open Question (LIVE) | Operator-present LIVE run: multi-domain dispatch spends model budget per active domain. | **Defer** | Operator-gated real spend (post-build). The empty-state-no-card + data-present-dispatch + fan-out-bound probes run on fixtures. No task. |

**Resolved-in-spec (the 30 PROCEED, verification pointer):** OQ items 1/2/3/5/6/7/9/10/11/13/14/15/16/18/19/20/22/23/24/25 and tension-resolutions 27/28/29/30/31 and negative-consequences 32/33/34/35/36 are each resolved by a task or a stated assumption — see the per-task **ADR Source** + **Risk Mitigations** fields and the Component Overview stated-assumptions paragraph. No open question, pending tension, or unmitigated risk from the six in-scope ADRs is left undispositioned.

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/plan/domain_program.py` | Create | The uniform seven-field DOMAIN PROGRAM contract + its field-level sub-schema (GRADE rationale structure, `monitoring_signals` validity-tier vocabulary, `cross_domain_seams` edge shape, `prescription` periodization) + the conformance validator (required vs conditional fields). ADR-0041-T1. |
| `scripts/plan/generate_plan.py` | Modify | **SUPERSEDES** the four thin translators + `_PLAN_TRANSLATORS` (123-291) via the transitional additive adapter (ADR-0041-T2); the plan-path `router.summarize` call at :356 swaps to the Context Assembler (ADR-0042-T1); the 58z0 `prescription→renderable` projection over the existing four translators (ADR-0046-T1); `_PLAN_TRANSLATORS`+`_DOMAIN_KIND` grow 4→§1-§13 **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C): at ADR-0043-T3 (Wave 4), NOT ADR-0046-T1; see ruling-0046-t1-sequencing.md]**. Four disjoint regions, serialized. |
| `scripts/plan/assemble.py` | Modify | **SUPERSEDES** the `_is_complete` completeness filter (116-124) + `_compose_claim` (250-275) to accept the uniform DOMAIN PROGRAM (transitional adapter). ADR-0041-T2. |
| `scripts/plan/context_assembler.py` | Create | The Context Assembler: feeds a dispatched specialist the operator's FULL record with pure identity stripped (name/contact/exact-DOB via the `pii_scan` precedent), generalizing `_care_profile`'s full-record access onto the plan hand-off; carries the genetics `genetic-trait-classes` token (raw genotypes never cross). Replaces `router.summarize`'s plan-path collapse. ADR-0042-T1. |
| `scripts/serve/care_chat.py` | Modify | **SUPERSEDES** the reply-only `{task:"care-conversation"}` `_care_messages` prompt (203-219) with the orchestration decompose→brief system prompt + control flow (ADR-0043-T1); adds collect+reconcile+synthesize control flow (ADR-0043-T2/T3). `_care_profile` (166-200) + the capture path (286-289) are UNCHANGED. |
| `scripts/plan/orchestrate.py` | Modify | **SUPERSEDES** `reconcile`'s five hard-coded pair-specific holds (337-456) with one uniform `cross_domain_seams` pass; the safety-critical subset (RED-S/LEA, additive-AE, Rx-BPMH) is retained as always-on floors (re-based, not deleted). ADR-0043-T2. |
| `scripts/serve/plan_loop.py` | Modify | **SUPERSEDES** the flat `run_orchestrated` composition `regenerate` re-runs (130,177-180) → the orchestrator front door + the closed-`PLAN_DOMAINS` entry-point iteration (77,407) → `activation.active_domains` (ADR-0043-T3); the `LARGE_CHANGE_THRESHOLD_DOMAINS` constant (51) + its check (203) re-base to a fraction of the active set (ADR-0046-T2). Disjoint regions, serialized. |
| `scripts/serve/server.py` | Modify | Replaces the closed-`PLAN_DOMAINS` iteration at the `/generate-plan` front door (≈784) with the computed active-domain set. ADR-0043-T3. |
| `scripts/store/plan_model.py` | Create | The comprehensive Plan Model (per active domain: the seven-field DOMAIN PROGRAM intact + integrated narrative + dated milestones + compiled monitoring config + plan-level adjustment rules), one composite object per plan version; the comprehensive resolver; the record path (value RIDES the frozen `store.append`/`keying.py` unchanged). ADR-0044-T1. Mixed-history reader added T2; confirm-hold skip added T4. |
| `scripts/store/plan_schema.py` | Modify | **SUPERSEDES** the four thin validators (178-275), `record_plan`→`store.append` (371-396), `resolve_plan` (462-498), and `PLAN_DOMAINS`'s stored-plan-domain-KEY role (49) — routed to `plan_model` (ADR-0044-T1); `PLAN_DOMAINS`'s surviving dispatch-roster-REGISTRY role grows 4→§1-§13 **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C): at ADR-0043-T3 (Wave 4), co-landing with the front-door dispatch + record re-point — NOT ADR-0046-T1; see ruling-0046-t1-sequencing.md]** (RT-009 — different role). Disjoint regions, serialized. |
| `scripts/plan/track.py` | Modify | Re-points `resolve_plan_progress` (81) off the superseded thin `resolve_plan` onto `plan_model`'s mixed-history reader. ADR-0044-T2. |
| `scripts/plan/horizons.py` | Modify | Re-bases the ADR-0038 horizon date-range composition: `window_block` (132) reads the comprehensive model's first-class periodization, not the flat `plan::<domain>` history. ADR-0044-T3. |
| `scripts/plan/activation.py` | Create | The progressive-activation gate: `active_domains(operator_surface)` computes the active-domain set from the operator's stated goals / tracked-stream data / care-conversation mentions / lab or genetic-trait-class touches; the §1-§13 card-emitting vs §14-genetics/§15-labs cross-cutting-input partition. Gate at DISPATCH. ADR-0046-T1. |
| `scripts/plan/plan_driver.py` | Modify | Grows `_ROLE_OF_DOMAIN` (117-122) from the four hard-wired domains to the 15+-specialist roster (each maps to its inlined role profile). **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C): the `_ROLE_OF_DOMAIN` roster growth is ADR-0043-T3 (Wave 4), NOT ADR-0046-T1 — plan_driver.py's sole writer becomes 0043-T3; see ruling-0046-t1-sequencing.md]** |
| `scripts/plan/monitoring_compiler.py` | Create | Compiles a plan's specialist-authored `monitoring_signals` + `adjustment_rules` (ADR-0041 fields 3-4) into a deterministic config: the Tier-1-auto-apply-safe rule grammar (bounded, in-domain, monotone) vs the must-escalate rules. Its output lives in the ADR-0044 model. ADR-0045-T1. |
| `scripts/plan/tiered_executor.py` | Create | The four-tier deterministic executor + the escalation predicate: Tier-1 auto-apply (0 model calls), Tier-2 specialist re-plan THROUGH the composition (finding-A), Tier-3 care-agent cross-domain reconcile (calls the ADR-0043 reconciler), Tier-4 medical-liaison human-gate (reuses ADR-0040's confirm hold). Fail-closed-by-direction. ADR-0045-T2. |
| `scripts/runner/daily_monitor.py` | Create | The daily deterministic pass hosted in the built ADR-0039 runner: reads the compiled config from the comprehensive model, runs the tiered executor's Tier-1 + escalation classification with 0 model calls on a no-event day; disabled-by-default, mirroring the runner's activation pattern. ADR-0045-T3. |
| `scripts/runner/schedule/activate.py` | Modify | Registers the daily deterministic-pass cadence (disabled by default) alongside the existing weekly cadence entry. ADR-0045-T3. |
| `scripts/plan/pipeline.py` | **Frozen-untouched** | ADR-0032 HARD-frozen inner engine, superseded by NO ADR in the set; `git diff --numstat` == 0 across all commits. |
| `scripts/plan/adjudicate.py` | **Frozen-untouched** | ADR-0032 HARD-frozen inner engine, superseded by no ADR in the set; `numstat` == 0. |
| `scripts/store/store.py` | **Frozen-untouched** | The record WRITE primitive (`store.append` / `_write_atomic`); the comprehensive plan rides it unchanged as a richer VALUE (disposition #14); `numstat` == 0. |
| `scripts/store/keying.py` | **Frozen-untouched** | The dedupe identity `(item, timepoint, source)`; unchanged (the plan VALUE grows, the key does not); `numstat` == 0. |
| `scripts/plan/adjust.py` | **Frozen-untouched** | The bare single-domain re-author leg; ADR-0045 Tier-2 routes re-plans THROUGH the composition (finding-A), never editing the bare leg — `adjust.py` `numstat` == 0. |
| `scripts/plan/router.py` | **Frozen-untouched (plan-path role superseded)** | `router.summarize` / `SUMMARY_FIELD_SET` / `EXCLUDED_RAW_PII` persist for their non-plan roles (`_care_profile` base, ADR-0027 de-id-IN shared summary — disposition #7); only the plan-path USE is superseded (at the call site in `generate_plan.py`/`plan_loop.py`), not `router.py` itself; `numstat` == 0. |
| `tests/plan/test_domain_program.py` | Create | ADR-0041-T1: seven-field conformance, required-vs-conditional rejection, autoregulation-required. |
| `tests/plan/test_generate_plan_uniform.py` | Create | ADR-0041-T2: transitional-adapter migration, non-uniform rejection, per-ADR freeze-break numstat. |
| `tests/plan/test_context_assembler.py` | Create | ADR-0042-T1: no-collapse, identity-strip, crown-jewel identity-leak + genetics carve-out probes. |
| `tests/serve/test_orchestrator_brief.py` | Create | ADR-0043-T1: decompose→brief emits N briefs carrying the assembled record. |
| `tests/serve/test_orchestrator_reconcile.py` | Create | ADR-0043-T2: collect + reconcile `cross_domain_seams`, always-on safety floors, un-reconciled-conflict probe, per-ADR freeze-break numstat. |
| `tests/serve/test_orchestrator_synthesize.py` | Create | ADR-0043-T3: single integrated plan + milestones, front-door redefinition. |
| `tests/store/test_plan_model.py` | Create | ADR-0044-T1: comprehensive round-trip fidelity, standing resolution, freeze-break numstat, store-adversarial battery. |
| `tests/store/test_plan_model_reader.py` | Create | ADR-0044-T2: mixed-history reader, store-adversarial battery. |
| `tests/plan/test_horizons_rebase.py` | Create | ADR-0044-T3: horizon range-query reads the comprehensive periodization. |
| `tests/store/test_plan_model_confirm_hold.py` | Create | ADR-0044-T4: ADR-0040 confirm-hold re-base on the comprehensive resolver. |
| `tests/plan/test_activation.py` | Create | ADR-0046-T1: data-driven active set, empty-state-no-card, data-present-dispatch, fan-out-bound. |
| `tests/serve/test_large_change_fraction.py` | Create | ADR-0046-T2: `LARGE_CHANGE_THRESHOLD_DOMAINS` re-based as a fraction of the active set. |
| `tests/plan/test_monitoring_compiler.py` | Create | ADR-0045-T1: Tier-1-safe vs must-escalate rule grammar, out-of-bounds rejection. |
| `tests/plan/test_tiered_executor.py` | Create | ADR-0045-T2: no-event-day 0-model-call, finding-A parity, human-gate hold, out-of-bounds no-auto-apply. |
| `tests/runner/test_daily_monitor.py` | Create | ADR-0045-T3: daily deterministic pass in the runner host, disabled-by-default, 0 model calls on a no-event day. |

## Tasks

### ADR-0041-T1: The Uniform Seven-Field DOMAIN PROGRAM Schema + Conformance Validator
**Status:** TODO
**ADR Source:** ADR-0041, Decision (the uniform seven-field DOMAIN PROGRAM — `prescription`, `rationale`, `monitoring_signals` each with a VALIDITY TIER, `adjustment_rules`, `required_labs`, `refusal/escalation`, `cross_domain_seams` — same shape every domain, plus the conformance validator); OQ-1 (field-level sub-schema — resolved in-spec, disposition #1); OQ-3 (required vs conditional fields — resolved in-spec, disposition #3); Validation confirmation #1 + falsification #1/#3
**Files to create/modify:**
- `scripts/plan/domain_program.py` (Create) — the seven-field contract + its sub-schema (the GRADE rationale structure = certainty-of-evidence × strength-of-recommendation + causal-vs-associational per claim; the `monitoring_signals` validity-tier vocabulary; the `cross_domain_seams` edge shape; the `prescription` periodization representation) + `validate(program) -> None|raises` (required: `prescription`, `rationale`, `monitoring_signals`, `adjustment_rules`; conditional: `required_labs` empty-OK for pure training / mandatory for compound, `refusal/escalation`, `cross_domain_seams`).
- `tests/plan/test_domain_program.py` (Create) — conformance (≥2 domains), required-field rejection, autoregulation-required.

**Acceptance Criteria:**
1. A fixture DOMAIN PROGRAM authored for ≥2 domains (a training domain program AND a compound domain program), each carrying all seven fields, validates: `domain_program.validate(program)` returns without raising and **missing-required-field count == 0** for each conformant program.
2. A program omitting any ONE of the four REQUIRED fields (`prescription`, `rationale`, `monitoring_signals`, `adjustment_rules`) is REJECTED: `validate` raises a typed error naming the missing field — **missing-required-field count ≥1 → reject** (an incomplete program is never admitted).
3. Required vs conditional partition holds (disposition #3): a pure-training program with `required_labs` empty VALIDATES (empty is legitimate there); a compound program with `required_labs` absent is REJECTED — the per-domain required-vs-conditional table drives the validator.
4. Autoregulation-required (falsification #3): a compound domain program with **0 `monitoring_signals` OR 0 `adjustment_rules` → rejected/flagged**, not admitted as a static plan.
5. Each `monitoring_signals` entry carries a VALIDITY TIER token from the fixed vocabulary; an entry missing its validity tier is rejected (a signal with no tier is not admitted).
6. `.venv/bin/python -m pytest tests/plan/test_domain_program.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0041 Consequences-Negative-4 (richer/costlier author call; under-delivery fails closed) — AC-2/AC-4 fail-closed rejection makes under-delivery an honest no-plan state, not a degraded plan. ADR-0041 Consequences (schema not usably shipped until consumers exist) — the DAG orders the consumers (0043/0044/0045/0046) after this task.
**Dependencies:** None (entry point)

---

### ADR-0041-T2: Transitional Additive Adapter — Migrate the Four Translators + `assemble._is_complete` to the Uniform Shape
**Status:** TODO
**ADR Source:** ADR-0041, Decision (SUPERSEDES the four thin translators `_to_workout/nutrition/supplements/peptides_plan` + `_PLAN_TRANSLATORS`, `generate_plan.py:123-291`, and `assemble._is_complete` + `_compose_claim`, `assemble.py:116-124,250-275`); OQ-2 (migration sequencing — resolved in-spec as a transitional additive adapter, disposition #2); Validation falsification #2 (non-uniform output breaks reconciliation); the per-ADR freeze-break probe (tension-resolution #27)
**Files to create/modify:**
- `scripts/plan/generate_plan.py` (Modify) — the four translators + `_PLAN_TRANSLATORS` accept/emit the uniform DOMAIN PROGRAM via a TRANSITIONAL ADAPTER (both the legacy payload and the uniform shape valid during migration; the adapter lifts today's `payload` into `prescription` while the other six fields ramp), bounded by the fail-closed validator — a partial program is rejected, never a silent thin fallback. Disjoint from the :356 assembler swap (ADR-0042-T1) and the `_PLAN_TRANSLATORS` roster growth (ADR-0046-T1).
- `scripts/plan/assemble.py` (Modify) — `_is_complete` + `_compose_claim` accept the uniform program (the seven-field completeness check supersedes the `source/confidence_tier/reversibility` thin check).
- `tests/plan/test_generate_plan_uniform.py` (Create) — adapter migration, non-uniform rejection, freeze-break numstat.

**Acceptance Criteria:**
1. A specialist emitting the uniform DOMAIN PROGRAM flows through the migrated translator → `assemble` → a recorded plan: the round-trip records a plan with **0 fields dropped** from the seven-field program.
2. During migration, the transitional adapter accepts BOTH shapes: a legacy thin payload lifts into `prescription` and validates; a full uniform program validates — **0 conformant inputs rejected** across the two shapes.
3. Non-uniform-output rejection (falsification #2): feeding the OLD bespoke non-uniform shape that is NOT adapter-liftable is rejected at the collection boundary, never silently adapted — **0 non-uniform outputs reach the reconcile step**; ≥1 silently reconciled → the test goes RED.
4. **Per-ADR freeze-break numstat (scoped to ADR-0041-T2's own commit):** `git diff --numstat <base> -- scripts/plan/generate_plan.py scripts/plan/assemble.py` shows the intended supersession; `git diff --numstat <base> -- scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/store/store.py scripts/store/keying.py scripts/store/plan_schema.py scripts/plan/orchestrate.py scripts/plan/router.py` returns EMPTY (0 changed lines) in THIS commit's delta — the HARD-frozen four + the sibling-superseded surfaces (0044's `plan_schema.py`, 0043's `orchestrate.py`, 0042's `router.py`) are untouched by ADR-0041-T2.
5. `.venv/bin/python -m pytest tests/plan/test_generate_plan_uniform.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0041 Consequences-Negative-2 (migration cost of the four translators + `_is_complete`) — AC-2 transitional additive adapter bounds it (no big-bang). ADR-0041 Consequences-Negative-1 (breaks the ADR-0032 freeze on the specialist-output surface) — AC-4 per-ADR-scoped numstat proves the break is deliberate + bounded; the set-wide sign-off covers it. Tension-resolution #27 — AC-4.
**Dependencies:** ADR-0041-T1 (the schema + validator the translators emit against), ADR-0042-T1 (both modify `generate_plan.py` in disjoint regions; the :356 assembler swap lands first, then the translator migration rebases on it)

---

### ADR-0042-T1: The Context Assembler — Identity-Stripped Full Record with the Genetics Carve-Out
**Status:** TODO
**ADR Source:** ADR-0042, Decision (adopt a Context Assembler feeding each dispatched specialist the operator's FULL record with pure identity stripped only, replacing `router.summarize`'s coarse-band collapse; SUPERSEDES the plan-path use of `router.summarize` + the `SUMMARY_FIELD_SET` gate at `generate_plan.py:356`; generalizes `_care_profile`'s full-record access, `care_chat.py:166-200`); OQ-1 (identity-strip mechanism — resolved in-spec via the `pii_scan`/`_care_profile` precedent, disposition #5); OQ-3 (`router.summarize` persists for non-plan roles, disposition #7); genetics carve-out (RT-008); Validation confirmation #1/#3 + falsification (crown-jewel)
**Files to create/modify:**
- `scripts/plan/context_assembler.py` (Create) — `assemble_context(store_read, ...) -> specialist_input` that reads the operator's FULL record and strips ONLY pure identity (legal name, exact DOB, contact, address — the identity members of `EXCLUDED_RAW_PII`, `router.py:65-108`), reusing `scripts/guard/pii_scan.py`'s `DEFAULT_IDENTITY_CONFIG` identity-strip precedent (designs NO new de-id scheme — parked). Genetics carve-out: raw rsID+allele genotypes are NEVER read into the context; genetics reaches it ONLY as the derived coarse `genetic-trait-classes` token (`router.py:59`), carried like any other health-substance field. Does NOT edit `care_chat.py` (mirrors the `_care_profile` pattern in the new module).
- `scripts/plan/generate_plan.py` (Modify) — the plan-path `summary = router.summarize(store_read)` at :356 swaps to `context_assembler.assemble_context(store_read)`; `router.summarize` PERSISTS for its non-plan consumers (unchanged).
- `tests/plan/test_context_assembler.py` (Create) — no-collapse, identity-strip, crown-jewel identity-leak + genetics carve-out.

**Acceptance Criteria:**
1. No-collapse (confirmation #1): seed a store with a GENERIC rich free-text program (a multi-day training split + a multi-item supplement stack); the specialist input carries the substantive free-text detail — **0 rich sources collapsed to a `SUMMARY_FIELD_SET`-only band**; if the input is byte-identical to `router.summarize`'s output, the test goes RED.
2. Real detail present (confirmation #2): the assembled input carries **≥1 operator-specific detail** that `router.summarize` would have discarded (a specific split parameter / a specific stack item), not a `low`/`moderate`/`high`-derived generic.
3. Identity strip (confirmation #3): scanning the specialist input for pure-identity tokens (legal name, exact DOB, contact, address) yields **0 identity tokens in any specialist input**.
4. Crown-jewel identity-leak (falsification, load-bearing): seed a SYNTHETIC legal name + a synthetic contact string; scan every specialist payload — **0 pure-identity tokens**; ≥1 → the test goes RED (halt-and-repair before release).
5. Genetics carve-out (RT-008): seed a raw rsID+allele genotype into the store; scan the assembled specialist input — **0 raw rsID/allele tokens** reach it, AND the derived `genetic-trait-classes` token IS present (the carve-out carries the coarse token, never the raw genotype). A de-id-bypass mutation (embedding a raw genotype into a carried field) drives the scan RED (observe RED, revert).
6. No-collapse falsification: if the assembler output equals `router.summarize`'s ~18-token band for a rich source, the test goes RED (DATA-COLLAPSE unfixed).
7. `.venv/bin/python -m pytest tests/plan/test_context_assembler.py` passes against synthetic fixtures (0 live-API calls, 0 real operator PII in the test tree).

**Risk Mitigations:** ADR-0042 Consequences-Negative-1 (redraws the crown-jewel PII boundary) — AC-4 identity-leak probe + AC-5 genetics carve-out are the load-bearing falsifiers. ADR-0042 Consequences-Negative-3 (the strip becomes the load-bearing seam) — AC-3/AC-4 enforce the strip is complete. ADR-0042 Consequences-Negative-4 (larger prompts/cost/latency, disposition #32) — accepted standing cost, documented; the full-record-first default (#6) is correct, the per-specialist slice is a tasked follow-on (out of this spec's build scope). Tension-resolution #27 (freeze break on the `router.summarize` plan-path surface) — the :356 swap supersedes the USE, `router.py` itself `numstat` == 0 (AC via the shared numstat probe in ADR-0041-T2 AC-4 and this task's grounding: `router.py` untouched).
**Dependencies:** None (entry point)

---

### ADR-0043-T1: Care Agent Decompose→Brief — Rewrite `_care_messages` to the Orchestration System Prompt
**Status:** TODO
**ADR Source:** ADR-0043, Decision §1 + §6 (the care agent becomes the Orchestrator; decompose the operator's goals + assembled state into N per-specialist briefs, each brief = that specialist's ADR-0042 input contract; SUPERSEDES the reply-only `{task:"care-conversation"}` `_care_messages` prompt, `care_chat.py:214-219`; extends the existing agent, not a second full-record reader — capture unchanged, `care_chat.py:286-289`); OQ-2 (full record vs slice — full record first, disposition #10); Validation confirmation #1 (emit N briefs) + falsification (under-briefed)
**Files to create/modify:**
- `scripts/serve/care_chat.py` (Modify) — `_care_messages`'s `{task:"care-conversation"}` reply-only context is superseded by the orchestration decompose→brief system prompt + the brief-builder control flow: `decompose(goals, assembled_state, active_domains) -> [brief, ...]` where each brief carries that specialist's ADR-0042 assembled record (the full record — the per-specialist slice is deferred, #10), NOT a coarse `router.summarize` band. The `active_domains` set is an INJECTED input (wired at the front door, ADR-0043-T3), so this task does not bake in a second activation gate. `_care_profile` (166-200) + the capture path (286-289) are UNCHANGED.
- `tests/serve/test_orchestrator_brief.py` (Create) — emit-N-briefs, each carries the assembled record, under-briefed falsifier.

**Acceptance Criteria:**
1. Emit-N-briefs (confirmation #1, load-bearing): seed goals + an assembled state spanning ≥2 domains (a training-domain + a compound-domain) and an injected active-domain set; the orchestrator produces **brief count == active-specialist count**, one brief per active specialist.
2. Each brief carries the specialist's required inputs — the ADR-0042 assembled record (the full record), NOT a coarse band: **0 briefs collapse to a `SUMMARY_FIELD_SET` band**.
3. Under-briefed falsifier (falsification): a brief that omits a required input (collapses to a coarse band / drops a domain-relevant field) drives the test RED — **0 briefs missing a required input**; ≥1 → RED.
4. No un-briefed active specialist: every domain in the injected active set gets exactly one brief — **0 active specialists un-briefed**.
5. The capture responsibility is unchanged: `persist_capture` / `persist_extraction` (`care_chat.py:286-289`) still routes proposed facts through the same de-identify-by-data-class gate — a grep asserts the capture call site is byte-unchanged (the orchestration is additive to the existing agent).
6. `.venv/bin/python -m pytest tests/serve/test_orchestrator_brief.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0043 Consequences-Negative-1 (MODERATE prompt + control-flow rework, disposition #33) — accepted build cost, documented; the rewrite is bounded to `_care_messages` (the highest-leverage first task). ADR-0043 Consequences-Negative-5 (longer/costlier orchestrator call, disposition #34) — accepted standing cost; the per-specialist slice (#10) mitigates later. Constraint-propagation (ADR-0042 → briefs carry the assembled record) — AC-2.
**Dependencies:** ADR-0042-T1 (the assembled record each brief carries)

---

### ADR-0043-T2: Collect + Reconcile the `cross_domain_seams` — Generalize the Five Holds, Safety Floors Always-On
**Status:** TODO
**ADR Source:** ADR-0043, Decision §2 + §3 (collect each returned ADR-0041 DOMAIN PROGRAM; reconcile by reading each program's `cross_domain_seams`, generalizing `orchestrate.reconcile`'s five hard-coded pair-specific holds, `orchestrate.py:337-456`, into one uniform-field pass); OQ-1 (which holds become always-on floors vs specialist-authored seams — resolved in-spec: SAFETY holds always-on, disposition #9); Validation confirmation #2 (synthesize a reconciled plan) + falsification #1 (un-reconciled conflict); the per-ADR freeze-break probe (tension-resolution #27)
**Files to create/modify:**
- `scripts/serve/care_chat.py` (Modify) — the collect step gathers each dispatched specialist's DOMAIN PROGRAM; the reconcile step reads each program's `cross_domain_seams` through ONE code path. Disjoint from ADR-0043-T1's decompose region.
- `scripts/plan/orchestrate.py` (Modify) — `reconcile` (337-456) generalizes the five pair-specific holds into one uniform `cross_domain_seams` pass; the SAFETY-CRITICAL subset — RED-S/LEA short-circuit, additive-AE, Rx-BPMH — is RETAINED as always-on reconciliation FLOORS (re-based, not deleted); the softer reconciliations (energy bounce, overlap+conflict) become specialist-authored seams.
- `tests/serve/test_orchestrator_reconcile.py` (Create) — reconcile-through-one-path, always-on floors, un-reconciled-conflict falsifier, freeze-break numstat.

**Acceptance Criteria:**
1. Mechanical reconciliation through ONE code path (ADR-0041 constraint): seed two domains whose programs declare a seam in `cross_domain_seams`; the reconcile step detects + holds/adjusts/routes the seam reading the UNIFORM field — **0 new per-domain-pair hard-coded branches** required; a pair-specific branch still needed → the test goes RED.
2. Un-reconciled-conflict falsifier (falsification #1, deterministic): seed two DOMAIN PROGRAMs declaring a `cross_domain_seams` conflict; **0 declared-seam conflicts reach the synthesized output un-reconciled**; ≥1 un-reconciled → RED.
3. Always-on safety floors (disposition #9): a RED-S/LEA, additive-AE, or Rx-BPMH condition is held even when NOT declared in a program's `cross_domain_seams` — the safety-critical subset fires as an always-on floor (a program that omits the seam does NOT escape the floor); removing a floor drives the corresponding safety test RED (observe RED, revert).
4. Safety content re-based, not deleted: the five holds' safety CONTENT (RED-S/LEA, energy bounce, overlap+conflict, additive-AE, Rx-BPMH) is present post-generalization — a coverage test asserts each of the five prior behaviors still reconciles its case.
5. **Per-ADR freeze-break numstat (scoped to ADR-0043-T2's own commit):** `git diff --numstat <base> -- scripts/plan/orchestrate.py` shows the intended reconcile generalization; `git diff --numstat <base> -- scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/store/store.py scripts/store/keying.py scripts/plan/generate_plan.py scripts/plan/assemble.py scripts/store/plan_schema.py` returns EMPTY in THIS commit's delta (the HARD-frozen four + the sibling-superseded surfaces untouched by 0043-T2).
6. `.venv/bin/python -m pytest tests/serve/test_orchestrator_reconcile.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0043 Consequences-Negative-2 (breaks the ADR-0032 freeze on the SAFETY-CRITICAL `orchestrate.reconcile`) — AC-5 per-ADR-scoped numstat; set-wide sign-off covers it. ADR-0043 Consequences-Negative-3/Negative-4 (reconciliation-generalization risk — coverage depends on what specialists declare) — AC-3 always-on safety floors bound it (the safety subset does not depend on a declaration) + AC-2 un-reconciled-conflict probe. Tension-resolution #27 — AC-5.
**Dependencies:** ADR-0041-T1 (the seven-field `cross_domain_seams` shape it reconciles), ADR-0043-T1 (the brief/dispatch it collects from; both modify `care_chat.py` in disjoint regions, serialized)

---

### ADR-0043-T3: Synthesize One Integrated Plan + Front-Door Redefinition
**Status:** TODO
**ADR Source:** ADR-0043, Decision §4 + §5 (synthesize ONE coherent plan + dated milestones across the reconciled programs; the orchestrator becomes the loop's re-entry front door, replacing the flat `run_orchestrated` composition `regenerate` re-runs, `plan_loop.py:130,177-180`); OQ-3 (dated-milestone representation — defined by the ADR-0044 model, disposition #11); tension-resolution #31 (front-door redefinition, `constrains` ADR-0036); Validation confirmation #2 (single integrated plan carrying milestones)
**Files to create/modify:**
- `scripts/serve/care_chat.py` (Modify) — the synthesize step composes ONE integrated plan + dated milestones from the reconciled programs (an integrated program, not four disjoint per-domain plans); milestones are emitted in the ADR-0044 model's representation (0043 emits, 0044 stores). Disjoint from T1/T2 regions.
- `scripts/serve/plan_loop.py` (Modify) — `regenerate` (130,177-180) re-enters the orchestrator decompose→brief→collect→reconcile→synthesize instead of the flat `run_orchestrated` composition; the closed-`PLAN_DOMAINS` entry-point iteration (77,407) is replaced with `activation.active_domains(...)` (wires the ADR-0046 gate into the front door). Disjoint from the `LARGE_CHANGE_THRESHOLD_DOMAINS` region (ADR-0046-T2).
- `scripts/serve/server.py` (Modify) — the `/generate-plan` front-door iteration over `plan_schema.PLAN_DOMAINS` (≈784) is replaced with the computed active-domain set.
- **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** the roster growth (relocated from ADR-0046-T1): `scripts/store/plan_schema.py` (Modify — grow `PLAN_DOMAINS`'s dispatch-roster role 4→§1-§13), `scripts/plan/plan_driver.py` (Modify — grow `_ROLE_OF_DOMAIN` 4→§1-§13), `scripts/plan/generate_plan.py` (Modify — grow `_PLAN_TRANSLATORS`+`_DOMAIN_KIND` 4→§1-§13). ATOMIC with the front-door re-point (`server.py:784`, `plan_loop.py:77,407` → `active_domains`) and the record re-point (the synthesize step records via `plan_model.record_plan_version`; the thin `orchestrate._recorded_result → record_plan` per-domain path is retired from the re-entry). See ruling-0046-t1-sequencing.md §A4.
- `tests/serve/test_orchestrator_synthesize.py` (Create) — single-integrated-plan, front-door redefinition.

**Acceptance Criteria:**
1. Single integrated plan (confirmation #2): seed two programs declaring a seam; the output is **ONE integrated plan carrying dated milestones**, NOT a per-domain `results` map with no synthesis — a per-domain map with no synthesis → the test goes RED.
2. Milestones are first-class: the synthesized plan carries dated milestones in the ADR-0044 model's representation (stored by ADR-0044-T1) — **milestone count ≥1** on a multi-domain plan.
3. Front-door redefinition (tension-resolution #31): `regenerate` re-enters the orchestrator (decompose→brief→collect→reconcile→synthesize), not the flat `run_orchestrated` composition — a grep asserts `regenerate`'s call graph reaches the orchestrator front door; the flat-composition re-run is retired from the loop's re-entry.
4. Active-set wiring: the front door dispatches `activation.active_domains(operator_surface)`, not the closed `plan_schema.PLAN_DOMAINS` tuple — a data-driven surface changes the dispatched set (composes with ADR-0046 without a double-gate).
5. **Per-ADR freeze-break numstat (scoped to ADR-0043-T3's own commit):** `git diff --numstat <base> -- scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/store/store.py scripts/store/keying.py` returns EMPTY in THIS commit's delta (the front-door rewrite edits `plan_loop.py`/`server.py`/`care_chat.py`, never the HARD-frozen four).
6. `.venv/bin/python -m pytest tests/serve/test_orchestrator_synthesize.py` passes against fixtures (0 live-API calls, 0 real operator PII).
7. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** Roster growth (relocated from ADR-0046-T1's former AC-2): a rich domain D beyond the original four DISPATCHES via `activation.active_domains` AND records first-class via `plan_model.record_plan_version`→`read_plan_version` — RED against the un-grown tree (PF-S130-01 production-path).
8. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** `len(PLAN_DOMAINS) >= 13` (the roster is grown in THIS commit).
9. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** The roster-coupled front-door tests are UPDATED to the active-domains contract: assert the active SUBSET dispatches + records via `plan_model`, NOT `set(results) == set(PLAN_DOMAINS)` all-recorded.
10. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** §1-§13 coherence gate: `set(PLAN_DOMAINS) <= set(_PLAN_TRANSLATORS) ∩ set(_ROLE_OF_DOMAIN) ∩ set(_DOMAIN_KIND)` (0 orphan) over the grown roster.
11. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** Single source of truth: `set(activation.CARD_DOMAINS) == set(PLAN_DOMAINS card-emitting)` (never two hand-maintained lists).

**Risk Mitigations:** ADR-0043 Consequences-Negative-1 (control-flow rework, #33) — accepted, bounded to the `regenerate` front door + the entry-point iteration. Tension-resolution #31 (front-door redefinition) — AC-3/AC-4. Constraint-propagation (ADR-0044 stores the synthesized plan + milestones) — AC-2.
**Dependencies:** ADR-0043-T2 (the reconciled programs it synthesizes), ADR-0044-T1 (the model that stores the synthesized plan + milestones), ADR-0046-T1 (the `active_domains` gate the front door dispatches)

---

### ADR-0044-T1: The Comprehensive Plan Model + Resolver — Value Rides the Frozen `store.append`
**Status:** TODO
**ADR Source:** ADR-0044, Decision (a comprehensive Plan Model storing per active domain: the full seven-field DOMAIN PROGRAM intact + integrated narrative + dated milestones + compiled monitoring config + plan-level adjustment rules; SUPERSEDES the thin `plan_schema.py` — the four validators `178-275`, `record_plan`→`store.append` `371-396`, `resolve_plan` `462-498`, and `PLAN_DOMAINS`'s stored-plan-domain-KEY role `49`); OQ-1 (container — one composite object per plan version, disposition #13); OQ-2 (the value RIDES the frozen `store.append`/`keying.py` unchanged, disposition #14); Validation confirmation #1/#2/#3 + falsification #1/#2; the per-ADR freeze-break probe (tension-resolution #27); store-adversarial mandate
**Files to create/modify:**
- `scripts/store/plan_model.py` (Create) — the comprehensive model (ONE composite object per plan version with a version key: per-domain seven-field DOMAIN PROGRAM + integrated narrative + dated milestones + compiled monitoring config + plan-level adjustment rules) + the comprehensive resolver + the record path. The record path RIDES the frozen `store.append(item, _reading(...), root)` unchanged — the comprehensive plan is a richer VALUE, the store WRITE primitive + the `(item, timepoint, source)` dedupe key are unchanged.
- `scripts/store/plan_schema.py` (Modify) — supersede the four thin validators, `record_plan`, `resolve_plan`, and `PLAN_DOMAINS`'s stored-plan-domain-key role — routed to `plan_model`. `PLAN_DOMAINS`'s dispatch-roster-registry role survives (RT-009; grown by ADR-0046-T1). Disjoint from the tuple-growth region.
- `tests/store/test_plan_model.py` (Create) — round-trip fidelity, standing resolution, freeze-break numstat, store-adversarial battery.

**Acceptance Criteria:**
1. Comprehensive round-trip (confirmation #1): store a fixture plan for ≥2 active domains (each with its seven-field program) + narrative + milestones + monitoring config; load it back — **missing-element count == 0** on load (every domain program field, the narrative, the milestones, the config present + well-typed).
2. Round-trip fidelity (falsification #1): a plan whose prescription carries dated periodization blocks + dated milestones + a compiled monitoring config loses **0** of periodization, milestones, or monitoring across store→load; any of the three dropped/flattened → the test goes RED.
3. Standing resolution (confirmation #2, load-bearing): store a comprehensive plan dated the render date; the comprehensive resolver resolves it as **standing** (the periodized program + narrative + milestones + config), NOT `NO_PLAN`/`NO_PLAN_TODAY`; an absence state on a dated plan → RED.
4. **Per-ADR freeze-break numstat (scoped to ADR-0044-T1's own commit, verbatim ADR threshold):** `git diff --numstat <base> -- scripts/plan/pipeline.py scripts/plan/adjudicate.py` == **0 changed lines**, AND `git diff --numstat <base> -- scripts/store/store.py scripts/store/keying.py` == **0 changed lines** (the value rides the primitive unchanged, disposition #14); the superseded set == exactly the four named `plan_schema.py` surfaces; **0 unnamed frozen edits** in this delta. EXPLICITLY EXCLUDED from ADR-0044's forbidden set (sibling supersessions, so probes don't contradict): `generate_plan.py`+`assemble.py` (0041), `orchestrate.py` (0043), `adjust.py`/`track.py` (0045/consumer).
5. **Store-adversarial battery** (per `docs/checklists/store-adversarial-tests.md`, all four categories over the `plan_model` record/read surface): (a) cross-stream namespace collision — a `plan_model` read for one plan-version stream never returns another stream's value; (b) same-timepoint dedupe — two distinct plan versions sharing a timepoint both persist, identical re-writes stay idempotent (0 duplicate lines on re-run); (c) dedupe-key boundary — the model introduces NO new dedupe key (a grep asserts 0 new keying logic; identity stays `keying`'s frozen `(item, timepoint, source)`); (d) mutation-style — widening the dedupe key to include `value` drives a battery test RED (observe RED, revert).
6. `.venv/bin/python -m pytest tests/store/test_plan_model.py` passes against scratch stores (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0044 Consequences-Negative-1 (breaks the ADR-0032 record-spine freeze, the biggest one-way door) — AC-4 per-ADR-scoped numstat proves it deliberate + bounded; store WRITE primitive `numstat` == 0. ADR-0044 Consequences-Negative-4 (larger stored plans / denser store, disposition #35) — accepted standing cost, documented. Tension-resolution #27 — AC-4. Store-adversarial mandate — AC-5.
**Dependencies:** ADR-0041-T1 (the seven-field DOMAIN PROGRAMs the model stores)

---

### ADR-0044-T2: Mixed-History-Tolerant Reader + Consumer Re-point
**Status:** TODO
**ADR Source:** ADR-0044, Decision (SUPERSEDES the append-only store's thin readers); OQ-4 (append-only store migration — resolved in-spec as a mixed-history-tolerant reader over a forward migration, disposition #16); Consequences (migration of every thin-schema consumer — `track.resolve_plan_progress`, dashboard); store-adversarial mandate
**Files to create/modify:**
- `scripts/store/plan_model.py` (Modify) — a mixed-history-tolerant READER: reads BOTH pre-existing thin `plan::<domain>` readings AND comprehensive plan versions; resolves the latest comprehensive plan as standing while thin history coexists (the append-only store is never rewritten — history is immutable).
- `scripts/plan/track.py` (Modify) — `resolve_plan_progress` (81) re-points off the superseded thin `resolve_plan` onto the mixed-history reader.
- `tests/store/test_plan_model_reader.py` (Create) — mixed-history read, consumer re-point, store-adversarial battery.

**Acceptance Criteria:**
1. Mixed-history read (disposition #16): a store carrying BOTH thin `plan::<domain>` readings and comprehensive plan versions resolves the **latest comprehensive** plan as standing — **0 thin readings rewritten** (append-only preserved) AND the comprehensive plan wins.
2. Thin-only fallback: a store with ONLY thin `plan::<domain>` readings (no comprehensive version yet) still resolves without error — the reader tolerates a pre-migration history (0 crashes on a thin-only store).
3. Consumer re-point: `track.resolve_plan_progress` reads through the mixed-history reader — a plan-vs-actual read over a comprehensive plan returns the comprehensive prescription, not a `NO_PLAN` on a stored plan.
4. **Store-adversarial battery** (all four categories over the reader surface): (a) cross-stream collision — a reader for one domain never returns another domain's plan; (b) same-timepoint — two same-date plan versions both readable, latest resolves; (c) dedupe-key boundary — 0 new keying logic (grep); (d) mutation — removing the comprehensive-precedence rule drives the mixed-history test RED (observe RED, revert).
5. `.venv/bin/python -m pytest tests/store/test_plan_model_reader.py` passes against scratch stores (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0044 Consequences-Negative-3 (migration of the append-only store contract + every thin-schema consumer) — AC-1/AC-2 mixed-history reader (respects append-only, no forced forward migration) + AC-3 consumer re-point. Store-adversarial mandate — AC-4.
**Dependencies:** ADR-0044-T1 (the comprehensive model + resolver the reader extends)

---

### ADR-0044-T3: Re-base the ADR-0038 Horizon Composition onto the Comprehensive Periodization
**Status:** TODO
**ADR Source:** ADR-0044, Decision (`complements`/`tensions-with` ADR-0038 — periodization becomes first-class); tension-resolution #28 (re-base ADR-0038's horizon date-range composition onto the comprehensive model's first-class periodization)
**Files to create/modify:**
- `scripts/plan/horizons.py` (Modify) — `window_block` (132) and the horizon date-range query read the comprehensive model's first-class stored periodization instead of the flat `plan::<domain>` dated-history range-query; `read_horizons`/`assess_pace` re-source from the comprehensive plan.
- `tests/plan/test_horizons_rebase.py` (Create) — horizon range-query reads the comprehensive periodization.

**Acceptance Criteria:**
1. Horizon re-base (tension-resolution #28): a horizon window query over a comprehensive plan carrying dated periodization blocks returns the periodization from the comprehensive model — **0 reads of the retired flat `plan::<domain>` dated history** for periodization.
2. Window membership holds: `window_block(domain, root, on_date, span_days)` over the comprehensive periodization keeps the blocks whose dates fall in the window — the window-membership semantics are preserved across the re-base (a block dated in-window is kept, out-of-window dropped).
3. Back-compat: a horizon query over a store with only thin `plan::<domain>` history (pre-migration) still resolves via the mixed-history reader — 0 crashes.
4. `.venv/bin/python -m pytest tests/plan/test_horizons_rebase.py` passes against scratch stores (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0044 Consequences-Negative-2 (forces re-basing ADR-0038 onto the comprehensive resolver) — AC-1/AC-2 the explicit re-base. Tension-resolution #28 — AC-1.
**Dependencies:** ADR-0044-T1 (the comprehensive model's first-class periodization it reads), ADR-0044-T2 (AC-3 thin-only back-compat resolves a pre-migration store via T2's mixed-history reader)

---

### ADR-0044-T4: Re-base the ADR-0040 Confirmation-Pointer Hold onto the Comprehensive Resolver
**Status:** TODO
**ADR Source:** ADR-0044, Decision (`tensions-with` ADR-0040 — resolver re-base); OQ-3 (re-base sequencing — resolved in-spec as an explicit re-base task, disposition #15); tension-resolution #29 (re-base ADR-0040's hold + `resolve_plan` skip onto the comprehensive resolver; ADR-0045's Tier-4 reuses ADR-0040's confirm hold); Validation falsification #3 (the ADR-0040 hold re-base holds)
**Files to create/modify:**
- `scripts/store/plan_model.py` (Modify) — the comprehensive resolver honors the ADR-0040 confirmation-pointer skip: an unconfirmed large-change comprehensive plan resolves NOT-standing (re-basing the current thin-reader skip that reads `plan_confirm`'s `plan-confirm::<domain>` pending pointers, `plan_loop.py:198-208`). The `plan_confirm.mark_pending` pointer MECHANISM is unchanged; the RESOLVER re-bases. Disjoint from ADR-0044-T2's reader region.
- `tests/store/test_plan_model_confirm_hold.py` (Create) — unconfirmed-large-change-not-standing, confirmed-stands.

**Acceptance Criteria:**
1. Confirm-hold re-base (falsification #3, deterministic): store a HELD (unconfirmed) large-change comprehensive re-gen with a pending `plan-confirm::` pointer; the comprehensive resolver does **NOT** stand it — **unconfirmed large-change comprehensive plan → not standing**; if it stands pre-confirm → the test goes RED.
2. Confirmed stands: a large-change comprehensive plan whose `plan-confirm::` pointer reads `confirmed` resolves as standing — the hold releases on confirm (0 false holds on a confirmed plan).
3. No-pointer default: a comprehensive plan with NO confirm pointer (a non-large-change re-gen) resolves as standing — the hold fires only on a pending-pointer large-change, never a default hold.
4. Pointer mechanism unchanged: a grep asserts `plan_confirm.py`'s `mark_pending`/pointer stream is byte-unchanged — the re-base is in the resolver, not the pointer mechanism.
5. `.venv/bin/python -m pytest tests/store/test_plan_model_confirm_hold.py` passes against scratch stores (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0044 Consequences-Negative-2 (forces re-basing ADR-0040 onto the comprehensive resolver) — AC-1/AC-2 the explicit re-base with the falsifier. Tension-resolution #29 — AC-1 (ADR-0045's Tier-4 reuses this re-based confirm hold — consumed by ADR-0045-T2).
**Dependencies:** ADR-0044-T2 (both modify `plan_model.py`'s resolver in disjoint regions; the mixed-history reader lands first, the confirm-hold skip rebases on it)

---

### ADR-0046-T1: Progressive-Activation Gate at Dispatch + the 58z0 Periodized-Prescription Reconciliation
**Status:** TODO
**ADR Source:** ADR-0046, Decision (scale dispatch from the four hard-wired domains to the 15+-specialist roster gated by PROGRESSIVE ACTIVATION; the active-domain set is computed from the operator's surface at plan time, not the closed 4-tuple; **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C): the roster GROWTH of `PLAN_DOMAINS`'s dispatch-roster role `plan_schema.py:49`, `_ROLE_OF_DOMAIN` `plan_driver.py:117-122`, and `_PLAN_TRANSLATORS`/`_DOMAIN_KIND` `generate_plan.py:286-291` relocates to ADR-0043-T3 (Wave 4); ADR-0046-T1 now ships the `active_domains` contract + the 58z0 `prescription→renderable` projection over the existing four translators, NOT the growth — see ruling-0046-t1-sequencing.md]**; RT-009 — the dispatch-registry role, distinct from ADR-0044's stored-key role); OQ-1 (activation signal — resolved in-spec, disposition #23); OQ-2 (gate at DISPATCH, disposition #24); OQ-3 (§1-13 card-emitting vs §14-genetics/§15-labs partition, disposition #25); Validation confirmation #1/#2 + falsification (all three)
**Files to create/modify:**
- `scripts/plan/activation.py` (Create) — `active_domains(operator_surface) -> frozenset` computing the active set from: an explicit operator goal in a domain, OR data/a reading in it, OR a care-conversation mention, OR a lab value / genetic-trait-class touching it (the activation signal, #23). Gates at DISPATCH (don't brief an inactive specialist, #24). Partitions the §1-§13 card-emitting domain specialists from the §14 genetics / §15 labs cross-cutting INPUTS (per `design/specialist-plan-contracts.md`, #25).
- `scripts/plan/generate_plan.py` (Modify) — the 58z0 `prescription→renderable` projection in the shared translator path ONLY (deep-strip `load` over the full periodized structure; derive the flat renderable else honest-no-plan; ride the seven-field program additively via `_with_program`). **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C): re-scoped from the `_PLAN_TRANSLATORS` roster growth to the 58z0 projection ONLY; the `scripts/store/plan_schema.py` (`PLAN_DOMAINS` dispatch-roster growth) and `scripts/plan/plan_driver.py` (`_ROLE_OF_DOMAIN` growth) manifest rows are DROPPED from 0046-T1 and relocate to ADR-0043-T3 (Wave 4) — see ruling-0046-t1-sequencing.md]**
- `tests/plan/test_activation.py` (Create) — data-driven active set, empty-state-no-card, data-present-dispatch, fan-out-bound.

**Acceptance Criteria:**
1. Data-driven active set (confirmation #2, load-bearing): seed two distinct operator surfaces — one with active domains {A, B}, one with {A, C, E, G, I}; **dispatched-set == computed-active-set for EACH surface AND the two dispatched sets differ**; the same closed four regardless of surface → the test goes RED.
2. **[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]:** `active_domains(surface)` RETURNS a §1-§13 card domain D beyond the original four when D is active on the surface — the gate's data-driven reach over the full card roster, a pure-function test needing no dispatch and no growth; a closed-four `active_domains` (or a `CARD_DOMAINS` missing D) never returns D → RED. The former AC-2 (a rich D DISPATCHES via the grown registries + records first-class via `plan_model`, PF-S130-01 production-path) MOVES to ADR-0043-T3.
3. Empty-state-no-card (falsification, deterministic): an operator with NO goal and NO data in D; **dispatch-for-D == 0 AND personalized-card-for-D == 0** (at most the goal-agnostic "nothing operator-specific" reference); a personalized card → RED.
4. Data-present-dispatch (falsification, deterministic): a domain D with a goal or data present is in the computed active set and IS dispatched — **data-present D → dispatch-for-D == 1**; a missed active domain (false negative) → RED.
5. Fan-out bound (falsification, deterministic): for a narrow-surface operator, **dispatch-count == |active set| < |roster|**; dispatch-count == |roster| on a narrow surface → RED.
6. Roster partition (#25): the §14 genetics / §15 labs cross-cutting inputs do NOT emit domain cards (they feed inputs); a grep/test asserts they are partitioned from the §1-§13 card-emitting set.
7. `.venv/bin/python -m pytest tests/plan/test_activation.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)] — AC scope re-grounding (ruling-0046-t1-sequencing.md §A3):**
- AC-1/AC-3/AC-4/AC-5/AC-6/AC-7 are unchanged in intent, but `active_domains` is computed over an `activation.CARD_DOMAINS` constant (the §1-§13 card-emitting slugs, grounded against `design/specialist-plan-contracts.md`), DECOUPLED from `plan_schema.PLAN_DOMAINS` (which stays the closed four until Wave 4); the roster-size floor is asserted as `len(activation.CARD_DOMAINS) >= 13`, not on `PLAN_DOMAINS`.
- The three 58z0 `prescription→renderable` assertions stay, exercised over the EXISTING workout translator (the periodized-prescription surface today).
- Coherence gate re-scoped to the CURRENT four: `set(PLAN_DOMAINS) <= set(_PLAN_TRANSLATORS) ∩ set(_ROLE_OF_DOMAIN) ∩ set(_DOMAIN_KIND)` (still a real check); the §1-§13 growth-coherence assertion moves to Wave 4 / ADR-0043-T3.
- Contract constraint (new): `activation.CARD_DOMAINS` and the Wave-4-grown `PLAN_DOMAINS` MUST derive from ONE source of truth (a shared card-roster constant), never two hand-maintained lists — the Wave-4 growth asserts `set(PLAN_DOMAINS card-emitting) == set(activation.CARD_DOMAINS)`.

**Risk Mitigations:** ADR-0046 Consequences-Negative-1 (dispatch fan-out cost scales with active count) — AC-5 progressive activation caps at the active set. ADR-0046 Consequences-Negative-2 (activation mis-fire either direction) — AC-3 false-positive + AC-4 false-negative probes. ADR-0046 Consequences-Negative-4 (roster >4 trips `LARGE_CHANGE_THRESHOLD_DOMAINS`, disposition #36) — the explicit threshold re-base is ADR-0046-T2 (a hard sequencing precondition before the scaled loop runs live). Constraint-propagation (ADR-0041 — each dispatched specialist emits the uniform shape) — the grown `_PLAN_TRANSLATORS` emit the migrated uniform shape (ADR-0041-T2 dependency).
**Dependencies:** ADR-0041-T1 (each dispatched specialist emits the uniform DOMAIN PROGRAM), ADR-0041-T2 (both grow `_PLAN_TRANSLATORS` in `generate_plan.py`; the shape migration lands first, the roster growth rebases), ADR-0044-T1 (retires `PLAN_DOMAINS`'s stored-key role before this grows its dispatch-registry role; both modify `plan_schema.py` in disjoint regions, serialized)

---

### ADR-0046-T2: Re-base `LARGE_CHANGE_THRESHOLD_DOMAINS` as a Fraction of the Active-Domain Set
**Status:** TODO
**ADR Source:** ADR-0046, Consequences-Negative-4 + Validation Review-trigger (`PLAN_DOMAINS` grows beyond four → ADR-0040's `LARGE_CHANGE_THRESHOLD_DOMAINS = 3` majority-of-four turns into a minority; re-decide the threshold as a FRACTION before the loop runs against the scaled set, resolving the external ADR-0040 OQ-2); disposition #36 (explicit threshold-re-base task, sequenced BEFORE the scaled loop runs)
**Files to create/modify:**
- `scripts/serve/plan_loop.py` (Modify) — `LARGE_CHANGE_THRESHOLD_DOMAINS` (51) + the `_change_magnitude(...) >= LARGE_CHANGE_THRESHOLD_DOMAINS` check (203) re-base to a FRACTION of the ACTIVE-domain set (`activation.active_domains`), so the large-change hold fires on a majority-of-active-domains swap, not a fixed count-of-3 that is a minority on a 15+ roster. Disjoint from the `regenerate` front-door region (ADR-0043-T3).
- `tests/serve/test_large_change_fraction.py` (Create) — fraction-of-active-set threshold, majority-swap hold on scaled + narrow surfaces.

**Acceptance Criteria:**
1. Fraction re-base (#36): the large-change hold fires when the changed-domain count reaches a MAJORITY FRACTION of the ACTIVE set — on a 4-active-domain surface a 3-of-4 swap holds (parity with the retired constant), on a 10-active-domain surface a 3-of-10 swap does **NOT** hold (3 is a minority of 10) while a 6-of-10 swap DOES.
2. Narrow-surface parity: a 2-active-domain surface holds on a majority (2-of-2) swap — the fraction adapts to the active-set size, never a fixed count.
3. No fixed-3 residue: a grep asserts the hold check is computed against `|active set|`, not a hardcoded `3` — the constant is superseded by the fraction.
4. Sequencing: the re-base is a documented hard precondition BEFORE the scaled loop runs against the 15+ roster (the ADR-0046 activation must not go live with the count-of-4 threshold on a scaled active set).
5. `.venv/bin/python -m pytest tests/serve/test_large_change_fraction.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0046 Consequences-Negative-4 (roster >4 trips the count-of-3 majority-of-four, disposition #36) — AC-1/AC-2/AC-3 re-base the threshold as a fraction; AC-4 pins the sequencing. Resolves external ADR-0040 OQ-2 for the scaled roster.
**Dependencies:** ADR-0046-T1 (the `active_domains` set the fraction is computed against), ADR-0043-T3 (both modify `plan_loop.py` in disjoint regions; the front-door rewrite lands first, the threshold re-base rebases on the settled file)

---

### ADR-0045-T1: The Monitoring Compiler — Rule Grammar for Tier-1-Safe vs Must-Escalate
**Status:** TODO
**ADR Source:** ADR-0045, Decision (the plan's `monitoring_signals` + `adjustment_rules` COMPILE into a config a daily loop runs DETERMINISTICALLY; consumes ADR-0041 fields 3-4, the config lives in the ADR-0044 model); OQ-1 (compiler rule grammar — resolved in-spec, disposition #18); Validation falsification #3 (out-of-bounds rule)
**Files to create/modify:**
- `scripts/plan/monitoring_compiler.py` (Create) — `compile_config(domain_programs) -> monitoring_config` compiling each program's `monitoring_signals` + `adjustment_rules` into a deterministic config: the Tier-1-auto-apply-safe rule grammar (bounded, in-domain, monotone specialist-pre-authored rules) vs the must-escalate rules (material, cross-domain, or safety-threshold). Rejects an out-of-domain-bounds or safety-crossing rule at COMPILE time. The compiled config is stored in the ADR-0044 model.
- `tests/plan/test_monitoring_compiler.py` (Create) — Tier-1-safe grammar, must-escalate classification, out-of-bounds compile rejection.

**Acceptance Criteria:**
1. Tier-1-safe grammar (disposition #18): a bounded, in-domain, monotone `adjustment_rule` compiles to a Tier-1-auto-apply-safe config entry — a deterministic, in-bounds rule is marked auto-apply-safe.
2. Must-escalate classification: a material-in-domain / cross-domain / safety-threshold rule compiles to a must-escalate config entry — **0 material/cross-domain/safety rules marked Tier-1-auto-apply-safe**.
3. Out-of-bounds compile rejection (falsification #3): an `adjustment_rule` that would drive an out-of-domain-bounds or safety-crossing change is REJECTED at compile time (or marked escalate-only) — **0 out-of-bounds rules compiled to auto-apply**; an out-of-bounds rule compiling to Tier-1 → the test goes RED.
4. Config lives in the model: the compiled config is a field of the ADR-0044 comprehensive plan model (stored there, not a side stream) — a compiled config round-trips through `plan_model` store→load.
5. `.venv/bin/python -m pytest tests/plan/test_monitoring_compiler.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0045 Consequences-Negative-2 (a mis-compiled rule auto-applying is a live risk) — AC-3 out-of-bounds compile rejection (bounded: auto-apply confined to in-domain specialist-authored bounded rules). Constraint-propagation (ADR-0044 — the config MUST live in the model) — AC-4.
**Dependencies:** ADR-0041-T1 (the `monitoring_signals`/`adjustment_rules` source fields it compiles), ADR-0044-T1 (the model home the compiled config lives in)

---

### ADR-0045-T2: The Four-Tier Deterministic Executor + Escalation Predicate
**Status:** TODO
**ADR Source:** ADR-0045, Decision (a TIERED executor escalates cheapest-and-safest first: Tier-1 auto-apply 0 model calls, Tier-2 specialist re-plan THROUGH the safety composition NOT the bare `adjust.py` leg — finding A, Tier-3 care-agent reconcile calls ADR-0043's `cross_domain_seams` reconciler, Tier-4 medical-liaison human-gate reuses ADR-0040's confirm hold; fail-closed BY DIRECTION — an unclassifiable event escalates UP); OQ-2 (the escalation predicate — resolved in-spec, disposition #19); tension-resolution #30 (the daily-cadence boundary; Tier-2 honors ADR-0036 finding-A); Validation confirmation #1/#2/#3 + falsification #1/#2/#3
**Files to create/modify:**
- `scripts/plan/tiered_executor.py` (Create) — the four-tier executor + the escalation predicate (classify in-domain-deterministic → Tier-1 auto-apply; material-in-domain → Tier-2 specialist re-plan through the composition; cross-domain → Tier-3 care-agent reconcile; safety-threshold → Tier-4 human-gate; a signal implicating more than one tier fail-closes to the HIGHER tier). Tier-2 routes the re-plan through the composed gate (the existing composition), never the bare `adjust.py` leg (finding-A parity — `adjust.py` untouched). Tier-3 calls ADR-0043's reconciler; Tier-4 reuses ADR-0044-T4's re-based confirm hold.
- `tests/plan/test_tiered_executor.py` (Create) — no-event-day 0-model-call, finding-A parity, human-gate hold, out-of-bounds no-auto-apply, fail-closed-up.

**Acceptance Criteria:**
1. No-event-day determinism (confirmation #1, load-bearing): run the executor over a compiled config on a day where NO `monitoring_signal` crosses a material threshold — **model-call-count == 0 AND de-id-IN-count == 0 AND 0 front-door re-entries**; ANY model or de-id-IN call on a no-event day → the test goes RED.
2. Finding-A parity (confirmation #2): a material in-domain event escalates to Tier-2 and the re-plan runs the composed gate + the per-domain safety floor, NOT the bare `adjust.py` leg — **0 material re-plans bypass the safety composition**; a Tier-2 re-plan without the composition → RED.
3. Cross-domain to Tier-3 (confirmation #3): an adjustment whose `cross_domain_seams` reach another domain escalates to Tier-3 (the `orchestrate` reconciler), never auto-applied — **0 cross-domain adjustments auto-applied at Tier-1**.
4. Human-gate hold (falsification #1, deterministic): a safety-threshold event (a `refusal/escalation` condition or a medical-liaison watchlist match) HOLDS at Tier-4 on ADR-0040's confirm hold and does **NOT** auto-advance — **held (0 auto-advance)**; if it advances past the human-gate → RED.
5. Out-of-bounds no-auto-apply (falsification #3): a mis-compiled out-of-bounds rule ESCALATES or is rejected — **0 out-of-bounds auto-applies** at Tier-1.
6. Fail-closed-by-direction: an unclassifiable event escalates UP (to a higher tier), never applies a guess — an ambiguous signal implicating Tier-1 + Tier-3 resolves to Tier-3.
7. `.venv/bin/python -m pytest tests/plan/test_tiered_executor.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0045 Consequences-Negative-1 (mis-classification escalating too little/too much) — AC-6 fail-closed-by-direction + AC-2/AC-3/AC-4 the per-tier probes. ADR-0045 Consequences-Negative-2 (deterministic tier must be provably safe un-modelled) — AC-1 no-event-day 0-model-call + AC-5 out-of-bounds no-auto-apply + AC-4 safety-threshold human-gate. Tension-resolution #30 (Tier-2 routes through the composition, honors finding-A) — AC-2.
**Dependencies:** ADR-0045-T1 (the compiled config it runs), ADR-0043-T2 (the Tier-3 care-agent `cross_domain_seams` reconciler it calls), ADR-0044-T4 (the Tier-4 re-based ADR-0040 confirm hold it reuses)

---

### ADR-0045-T3: The Daily Deterministic Pass Hosted in the Built ADR-0039 Runner
**Status:** TODO
**ADR Source:** ADR-0045, Decision (a daily loop runs the compiled config DETERMINISTICALLY, 0 model calls; REFINES ADR-0036's "re-enter the full front door on every debounced trigger" → "run the compiled config daily with 0 model calls, escalate on material events"); OQ-3 (daily-tier cadence + host — resolved in-spec: hosts in the ADR-0039 scheduled runner, disposition #20); OQ-5 (Tier-1 auto-apply recording — resolved in-spec: recorded in the ADR-0044 model as a bounded adjustment, does NOT reach ADR-0040's large-change threshold, disposition #22); Validation confirmation #1 + falsification #2 (no-event-day 0-model-call)
**Files to create/modify:**
- `scripts/runner/daily_monitor.py` (Create) — the daily deterministic pass in the built ADR-0039 runner host: reads the compiled config from the comprehensive model, runs the tiered executor's Tier-1 + escalation classification with 0 model calls on a no-event day; a Tier-1 auto-apply records in the ADR-0044 model as a bounded adjustment (never reaching ADR-0040's large-change threshold — only a model re-plan can, #22). Disabled by default, mirroring `scripts/runner/`'s activation pattern.
- `scripts/runner/schedule/activate.py` (Modify) — registers the daily deterministic-pass cadence (disabled by default) alongside the existing weekly cadence entry.
- `tests/runner/test_daily_monitor.py` (Create) — daily pass in the runner, disabled-by-default, no-event-day 0-model-call.

**Acceptance Criteria:**
1. Daily pass hosts in the runner (disposition #20): the daily deterministic pass runs in the built `scripts/runner/` host — a fixture daily tick invokes `daily_monitor` over a seeded compiled config; the weekly model re-plan cadence is unchanged (both coexist).
2. No-event-day 0-model-call (falsification #2): on a day no signal crosses a material threshold, **model-call-count == 0** — the daily tier is deterministic (≥1 model call on a no-event day → the test goes RED).
3. Disabled by default: a fresh runner install has the daily-pass entry DISABLED — the count of active daily-monitor schedule entries == 0 before an explicit operator enable (mirrors the ADR-0039 disabled-by-default posture).
4. Tier-1 recording (#22): a Tier-1 auto-apply on a material-in-bounds event records in the ADR-0044 model as a bounded adjustment AND does **NOT** reach ADR-0040's large-change threshold (a single in-domain deterministic change is not a majority-of-active-domains swap).
5. Metered-spend reduction: the daily deterministic pass fires **0 metered de-id-IN calls** on a no-event day (reduces ADR-0039's metered spend — `complements` ADR-0039).
6. `.venv/bin/python -m pytest tests/runner/test_daily_monitor.py` passes against fixtures (0 live-API calls, 0 real operator PII).

**Risk Mitigations:** ADR-0045 Consequences-Negative-1 (net-new tiering complexity) — AC-2 no-event-day determinism proves the daily tier is un-modelled. ADR-0039 `complements` (reduces metered de-id spend) — AC-5. Disposition #20 (host) — AC-1; disposition #22 (Tier-1 recording) — AC-4.
**Dependencies:** ADR-0045-T2 (the tiered executor the daily pass runs)

---

## Dependency Map

```
ADR-0041-T1 --> ADR-0041-T2      (the schema/validator the migrated translators emit against)
ADR-0042-T1 --> ADR-0041-T2      (shared generate_plan.py; the :356 assembler swap lands before the translator migration)
ADR-0041-T1 --> ADR-0044-T1      (the seven-field DOMAIN PROGRAMs the model stores)
ADR-0042-T1 --> ADR-0043-T1      (the assembled record each brief carries)
ADR-0041-T1 --> ADR-0043-T2      (the cross_domain_seams shape it reconciles)
ADR-0043-T1 --> ADR-0043-T2      (shared care_chat.py; the brief step it collects from)
ADR-0043-T2 --> ADR-0043-T3      (the reconciled programs it synthesizes)
ADR-0044-T1 --> ADR-0043-T3      (the model that stores the synthesized plan + milestones)
ADR-0046-T1 --> ADR-0043-T3      (the active_domains gate the front door dispatches)
ADR-0044-T1 --> ADR-0044-T2      (the comprehensive model/resolver the reader extends)
ADR-0044-T1 --> ADR-0044-T3      (the first-class periodization horizons reads)
ADR-0044-T2 --> ADR-0044-T3      (AC-3 thin-only back-compat resolves via T2's mixed-history reader)
ADR-0044-T2 --> ADR-0044-T4      (shared plan_model.py resolver; reader before confirm-hold skip)
ADR-0041-T1 --> ADR-0046-T1      (each dispatched specialist emits the uniform shape)
ADR-0041-T2 --> ADR-0046-T1      (shared generate_plan.py _PLAN_TRANSLATORS; shape migration before roster growth)
ADR-0044-T1 --> ADR-0046-T1      (shared plan_schema.py; stored-key role retired before dispatch-registry role grows)
ADR-0046-T1 --> ADR-0046-T2      (the active_domains set the fraction is computed against)
ADR-0043-T3 --> ADR-0046-T2      (shared plan_loop.py; front-door rewrite before the threshold re-base)
ADR-0041-T1 --> ADR-0045-T1      (the monitoring_signals/adjustment_rules source fields)
ADR-0044-T1 --> ADR-0045-T1      (the model home the compiled config lives in)
ADR-0045-T1 --> ADR-0045-T2      (the compiled config the executor runs)
ADR-0043-T2 --> ADR-0045-T2      (the Tier-3 cross_domain_seams reconciler)
ADR-0044-T4 --> ADR-0045-T2      (the Tier-4 re-based ADR-0040 confirm hold)
ADR-0045-T2 --> ADR-0045-T3      (the tiered executor the daily pass runs)
```

**[AMENDED 2026-07-12 — Architect, 0046-T1 re-sequence (Option C)]** (ruling-0046-t1-sequencing.md §A5 — the 0046-T1 growth split): `ADR-0046-T1 --> ADR-0043-T3` (the `active_domains` contract the front door dispatches) is UNCHANGED, as are `ADR-0043-T2 --> ADR-0043-T3` and `ADR-0044-T1 --> ADR-0043-T3`. The `PLAN_DOMAINS`/`_ROLE_OF_DOMAIN`/`_PLAN_TRANSLATORS`/`_DOMAIN_KIND` roster growth is now a clause OF ADR-0043-T3 (it needs 0043-T3's own front-door + record re-point to be safe; it consumes 0046-T1's `active_domains` + 0041-T2's migrated `_PLAN_TRANSLATORS` shape + 0044-T1's `plan_model` record path — all Wave≤3, so 0043-T3 stays a valid Wave-4 node). ADR-0046-T2's fraction-threshold (edge `ADR-0043-T3 --> ADR-0046-T2`) now computes against the grown active set produced in the same wave. Kahn re-check: 0043-T3 remains at depth 4 (all predecessors depth ≤3); the DAG stays acyclic; the six-wave structure is unchanged.

Topological order (Kahn's algorithm; parallel groups — verified acyclic by BFS, 15 nodes all processed, 0 remaining):

1. **ADR-0041-T1, ADR-0042-T1** (entry points — no dependencies)
2. **ADR-0041-T2** (←0041-T1, 0042-T1), **ADR-0044-T1** (←0041-T1), **ADR-0043-T1** (←0042-T1)
3. **ADR-0044-T2** (←0044-T1), **ADR-0046-T1** (←0041-T1, 0041-T2, 0044-T1), **ADR-0045-T1** (←0041-T1, 0044-T1), **ADR-0043-T2** (←0041-T1, 0043-T1)
4. **ADR-0044-T4** (←0044-T2), **ADR-0044-T3** (←0044-T1, 0044-T2), **ADR-0043-T3** (←0043-T2, 0044-T1, 0046-T1)
5. **ADR-0046-T2** (←0046-T1, 0043-T3), **ADR-0045-T2** (←0045-T1, 0043-T2, 0044-T4)
6. **ADR-0045-T3** (←0045-T2)

Entry points: **ADR-0041-T1, ADR-0042-T1**
Critical path: **ADR-0041-T1 → ADR-0044-T1 → ADR-0045-T1 → ADR-0045-T2 → ADR-0045-T3** (the schema foundation → the comprehensive model → the monitoring compiler → the tiered executor → the daily deterministic pass; 6-node depth, the longest-risk chain — the monitoring loop).

**Tier consistency:** every dependency edge points down-tier or within-tier — Tier-1 tasks (0041/0042) are in groups 1-2; Tier-2 tasks (0043/0044/0046) span groups 2-5; Tier-3 tasks (0045) span groups 3-6, each depending on its Tier-1/Tier-2 predecessors (0045-T1 ← 0041-T1 + 0044-T1; 0045-T2 ← 0043-T2 + 0044-T4). No Tier-3 task precedes a Tier-2 dependency. **Intra-group file-writer check:** no parallel group holds two writers of one mutable file — group 3's `plan_schema.py` writer (0046-T1) is ordered after group 2's `plan_schema.py` writer (0044-T1); group 3's `care_chat.py` writer (0043-T2) is ordered after group 2's (0043-T1); the three `plan_model.py` writers (0044-T1/T2/T4) are chained across groups 2→3→4; the two `plan_loop.py` writers (0043-T3 group 4, 0046-T2 group 5) are ordered; the three `generate_plan.py` writers (0042-T1 group 2, 0041-T2 group 2, 0046-T1 group 3) touch disjoint regions and are serialized 0042-T1 → 0041-T2 → 0046-T1.

These groups map to the build-plan waves (tier-ordered): **Tier-1 wave** = groups 1-2's 0041/0042 tasks (the uniform schema + the assembler); **Tier-2 wave** = the 0043/0044/0046 tasks (orchestrator + model + dispatch); **Tier-3 wave** = the 0045 tasks (the monitoring compiler + executor + daily pass). Each wave's checkpoint Go/No-Go is the cross-spec integration gate.

## Test Strategy

All tasks are satisfiable with fixture consumers (fixture DOMAIN PROGRAMs, a fixture `dispatch`/de-id client, synthetic PII-free stores) at **0 live-API spend and 0 real operator PII in the test tree**. The six operator-present LIVE runs (real specialist dispatches spend model budget + fire the metered de-id-IN call) are DEFERRED (Unresolved-Concerns table), never a CI assertion. Crown-jewel probes use synthetic tokens (a synthetic legal name + a synthetic contact + a synthetic raw rsID+allele genotype).

### Unit Tests
- **Scope:** `domain_program.py` (seven-field conformance + required-vs-conditional + validity-tier), `context_assembler.py` (no-collapse + identity-strip + genetics carve-out), `care_chat.py` orchestration (decompose→brief + collect+reconcile + synthesize), `orchestrate.py` (`cross_domain_seams` reconciliation + always-on floors), `plan_model.py` (round-trip + resolver + mixed-history reader + confirm-hold skip), `horizons.py` (periodization re-base), `activation.py` (data-driven active set + roster partition), `plan_loop.py` (fraction threshold), `monitoring_compiler.py` (rule grammar), `tiered_executor.py` (four-tier predicate), `daily_monitor.py` (daily deterministic pass).
- **Approach:** pytest with fixture DOMAIN PROGRAMs, a fixture `dispatch` + fixture de-id client, scratch stores, synthetic identity/genetics tokens; no live dependencies, no real PII.
- **Criteria covered:** ADR-0041-T1 1-6; ADR-0041-T2 1-3, 5; ADR-0042-T1 1-3, 6-7; ADR-0043-T1 1-6; ADR-0043-T2 1-4, 6; ADR-0043-T3 1-4, 6; ADR-0044-T1 1-3, 6; ADR-0044-T2 1-3, 5; ADR-0044-T3 1-4; ADR-0044-T4 1-3, 5; ADR-0046-T1 1-7; ADR-0046-T2 1-3, 5; ADR-0045-T1 1-5; ADR-0045-T2 1-7; ADR-0045-T3 1-6.

### Integration Tests
- **Scope:** the authoring spine end-to-end on fixtures — the assembler (0042) feeds the orchestrator's brief (0043-T1), the orchestrator collects fixture DOMAIN PROGRAMs (0041) + reconciles seams (0043-T2) + synthesizes one plan (0043-T3) stored in the comprehensive model (0044-T1) + read back by the mixed-history reader (0044-T2); the monitoring compiler (0045-T1) compiles the stored config, the tiered executor (0045-T2) runs it, the daily pass (0045-T3) hosts it; the front door dispatches the active set (0046-T1) with the re-based fraction threshold (0046-T2). Exercises files created by one task consumed by another (0044-T1's model stored by 0043-T3; 0043-T2's reconciler called by 0045-T2's Tier-3; 0044-T4's confirm hold reused by 0045-T2's Tier-4).
- **Approach:** drive the spine over a seeded synthetic store; assert the assembled record reaches the brief (not a band), one integrated plan + milestones stores + resolves standing, the daily pass runs 0-model-call on a no-event day, and the active set drives dispatch.
- **Criteria covered:** ADR-0042-T1 1-2; ADR-0043-T1 1-2; ADR-0043-T2 1-2; ADR-0043-T3 1-4; ADR-0044-T1 1-3; ADR-0044-T2 1-3; ADR-0045-T2 1-3; ADR-0045-T3 1-2, 4; ADR-0046-T1 1-2.

### Risk-Specific Tests
- **Crown-jewel non-egress (ADR-0042):** synthetic legal name + contact + raw genotype seeded; scan every specialist payload for 0 identity/raw-genotype tokens; a de-id-bypass mutation drives the scan RED (0042-T1 AC-4/AC-5).
- **Per-ADR-scoped freeze-break numstat probes (each scoped to its OWN commit, excluding sibling-superseded files):** 0041-T2 AC-4 (generate_plan.py+assemble.py; frozen four + siblings EMPTY); 0042-T1 (router.py EMPTY, the plan-path USE superseded not router.py); 0043-T2 AC-5 (orchestrate.py; frozen four + siblings EMPTY); 0043-T3 AC-5 (frozen four EMPTY); 0044-T1 AC-4 (pipeline.py+adjudicate.py+store.py+keying.py == 0; four named plan_schema.py surfaces superseded; siblings excluded); 0046-T1 (frozen four EMPTY, grows plan_schema.py); 0045-T1/T2/T3 (net-new, frozen four EMPTY — no freeze break of its own). The probes are scoped per-commit so they do not forbid each other's intended supersession.
- **Store-adversarial battery (the ADR-0044 store-surface tasks, per `docs/checklists/store-adversarial-tests.md`, all four categories with a mutation-RED):** 0044-T1 AC-5 (the `plan_model` record surface) + 0044-T2 AC-4 (the mixed-history reader surface) — cross-stream namespace collision, same-timepoint dedupe, dedupe-key boundary (0 new keying — identity stays `keying`'s frozen `(item, timepoint, source)`), and category-4 mutation-style verification (a widened dedupe key / removed precedence rule drives a battery test RED, observe RED, revert).
- **Always-on safety floors (ADR-0043):** removing a RED-S/LEA / additive-AE / Rx-BPMH floor drives the corresponding safety test RED (0043-T2 AC-3).
- **Deterministic-tier safety (ADR-0045):** no-event-day 0-model-call (0045-T2 AC-1, 0045-T3 AC-2), safety-threshold human-gate hold (0045-T2 AC-4), out-of-bounds no-auto-apply (0045-T1 AC-3, 0045-T2 AC-5), fail-closed-by-direction (0045-T2 AC-6).
- **Activation mis-fire (ADR-0046):** empty-state-no-card false-positive (0046-T1 AC-3) + data-present-dispatch false-negative (0046-T1 AC-4) + fan-out-bound (0046-T1 AC-5); the fraction-threshold re-base on scaled + narrow surfaces (0046-T2 AC-1/AC-2).
- **Criteria covered:** ADR-0041-T2 3-4; ADR-0042-T1 4-6; ADR-0043-T2 3, 5; ADR-0043-T3 5; ADR-0044-T1 4-5; ADR-0044-T2 4; ADR-0044-T4 4; ADR-0046-T1 3-6; ADR-0046-T2 1-4; ADR-0045-T1 3; ADR-0045-T2 4-6; ADR-0045-T3 5.

## Repo-Grounding Ledger

Grounded against the worktree-authoritative checkout at **HEAD 191ccb7e** (branch `feature/comprehensive-plan-adr`). Every task premise, cited input, and manifest action was confirmed by reading the live files directly (not the ADR prose). **Discrepancies reconciled into the manifest/ACs:** (1) `router.summarize` is at `router.py:738` and `dispatch`'s `set(payload) <= set(SUMMARY_FIELD_SET)` gate at `router.py:893` — the context's `561-623` range are the de-id derivation helpers, not `summarize` itself (shapes intact; `SUMMARY_FIELD_SET` 23-60, `EXCLUDED_RAW_PII` 65-108, `genetic-trait-classes` :59 all confirmed); (2) the `/generate-plan` front-door `PLAN_DOMAINS` iteration is at `server.py:784` (the `for domain in plan_schema.PLAN_DOMAINS` statement; :788 is an in-loop comment); (3) `plan_loop.py`'s `PLAN_DOMAINS` iteration is at :77 + the derived-marker (the `_last_regen_date` loop) at :407 (:400 is the docstring line), the ADR-0040 hold at :198-208 + `LARGE_CHANGE_THRESHOLD_DOMAINS=3` at :51 / the check at :203; (4) the **ADR-0039 runner IS built** (`scripts/runner/{__init__,cadence_runner,auth_isolation,store_lock,subscription_dispatch}.py` + `schedule/` present) — ADR-0045-T3's daily-pass host is a real surface, not a planned one; (5) `monitoring_signals`/`adjustment_rules`/`cross_domain_seams` return **0 hits across `scripts/`** — the thin schema carries none of the DOMAIN PROGRAM fields (ADR-0044 premise confirmed; these fields are genuinely net-new); (6) all seven NEW modules (`domain_program.py`, `context_assembler.py`, `plan_model.py`, `activation.py`, `monitoring_compiler.py`, `tiered_executor.py`, `daily_monitor.py`) are confirmed ABSENT (Create actions); the four HARD-frozen files (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`) + `adjust.py` + `router.py` are confirmed present (Frozen-untouched).

| Task | RGC-1 (manifest action) | RGC-2 (premise freshness) | RGC-3 (cited input) | RGC-4 (no duplication) | Disposition |
|------|-------------------------|---------------------------|---------------------|------------------------|-------------|
| ADR-0041-T1 | pass — `domain_program.py` ABSENT (Create); `tests/plan/test_domain_program.py` ABSENT (Create) | pass — the uniform seven-field contract is net-new (`monitoring_signals`/`adjustment_rules`/`cross_domain_seams` grep = 0 hits in `scripts/`) | pass — no cited input parsed (a fresh schema module) | pass — no existing DOMAIN PROGRAM schema/validator; `generate_plan.py`'s universal recommendation contract (24-38) is the thin shape this supersedes, not a duplicate | Grounded |
| ADR-0041-T2 | pass — `generate_plan.py` + `assemble.py` present (Modify); `test_generate_plan_uniform.py` ABSENT (Create) | pass — the four translators + `_PLAN_TRANSLATORS` at `generate_plan.py:123-291`; `_is_complete` at `assemble.py:116-124`, `_compose_claim` 250-275 — all confirmed at the cited lines | pass — the translators emit against `domain_program.validate` (created ADR-0041-T1) | pass — supersedes the existing translators in place (no duplicate) | Grounded |
| ADR-0042-T1 | pass — `context_assembler.py` ABSENT (Create); `generate_plan.py` present (Modify at :356); `test_context_assembler.py` ABSENT (Create) | pass — `summary = router.summarize(store_read)` at `generate_plan.py:356`; `_care_profile` at `care_chat.py:166-200`; `EXCLUDED_RAW_PII` identity members + `genetic-trait-classes` at `router.py:59,65-108`; `pii_scan.DEFAULT_IDENTITY_CONFIG` present | pass — `router.summarize` signature confirmed at :738; `pii_scan.py` present (`DEFAULT_IDENTITY_CONFIG` = `vault/meta/operator-identity.txt`) | pass — no existing context assembler; generalizes `_care_profile`'s pattern into a new module (not a second full-record reader edit) | Grounded |
| ADR-0043-T1 | pass — `care_chat.py` present (Modify); `test_orchestrator_brief.py` ABSENT (Create) | pass — `_care_messages` `{task:"care-conversation"}` prompt at `care_chat.py:203-219`; the capture path at 286-289; `_care_profile` at 166-200 | pass — briefs carry `context_assembler.assemble_context` output (ADR-0042-T1) | pass — no existing orchestrator; extends the existing care agent (capture unchanged) | Grounded |
| ADR-0043-T2 | pass — `care_chat.py` (Modify, disjoint from T1) + `orchestrate.py` present (Modify); `test_orchestrator_reconcile.py` ABSENT (Create) | pass — `orchestrate.reconcile`'s five holds at `orchestrate.py:337-456`; the `meta` side-channel (`_ae_profile`) at 101-124 | pass — reconciles the `cross_domain_seams` field of the ADR-0041 program (ADR-0041-T1) | pass — generalizes the existing reconciler in place (no duplicate) | Grounded |
| ADR-0043-T3 | pass — `care_chat.py` (Modify, disjoint) + `plan_loop.py` + `server.py` present (Modify); `test_orchestrator_synthesize.py` ABSENT (Create) | pass — the flat `run_orchestrated` composition `regenerate` re-runs at `plan_loop.py:130,177-180`; the `PLAN_DOMAINS` iteration at :77,:407 + `server.py:784` | pass — stores the synthesized plan + milestones via `plan_model` (ADR-0044-T1); dispatches `activation.active_domains` (ADR-0046-T1) | pass — no existing orchestrator front door; replaces the flat composition in place | Grounded |
| ADR-0044-T1 | pass — `plan_model.py` ABSENT (Create); `plan_schema.py` present (Modify); `test_plan_model.py` ABSENT (Create) | pass — `PLAN_DOMAINS` at `plan_schema.py:49`; the four validators 178-275; `record_plan`→`store.append` 371-396 (store.append at :394); `resolve_plan` 462-498 — all confirmed; `store.append`/`keying` present (frozen) | pass — the record path rides `store.append(item, _reading(...), root)` (`store.py`, `plan_schema.py:394` pattern); `keying`'s `(item, timepoint, source)` identity confirmed | pass — no existing comprehensive plan model; supersedes the thin `plan_schema.py` surfaces (RT-009 — `PLAN_DOMAINS` dispatch role survives) | Grounded |
| ADR-0044-T2 | pass — `plan_model.py` (Modify, created T1) + `track.py` present (Modify); `test_plan_model_reader.py` ABSENT (Create) | pass — the append-only store (history immutable, `store.append` frozen); `track.resolve_plan_progress` at `track.py:81` reads `resolve_plan` | pass — `resolve_plan_progress` signature + `plan_schema` import at `track.py:26,81` confirmed | pass — no existing mixed-history reader; extends `plan_model` (T1) | Grounded |
| ADR-0044-T3 | pass — `horizons.py` present (Modify); `test_horizons_rebase.py` ABSENT (Create) | pass — `window_block` at `horizons.py:132` reads `store.read("plan::<domain>")` (154); `read_horizons`/`assess_pace` present | pass — `window_block(domain, root, on_date, span_days)` signature + the `plan::<domain>` range-query confirmed at 132-154 | pass — re-bases the existing horizon composition in place onto the comprehensive periodization | Grounded |
| ADR-0044-T4 | pass — `plan_model.py` (Modify, disjoint from T2) present; `test_plan_model_confirm_hold.py` ABSENT (Create) | pass — the ADR-0040 hold at `plan_loop.py:198-208` writes `plan_confirm.mark_pending` pending pointers; `plan_confirm.py` `plan-confirm::<domain>` pointer stream present | pass — `plan_confirm.mark_pending(domain, plan_date, root)` + the pointer stream confirmed | pass — re-bases the existing confirm-hold skip onto the comprehensive resolver; pointer mechanism (`plan_confirm.py`) unchanged | Grounded |
| ADR-0046-T1 | pass — `activation.py` ABSENT (Create); `plan_schema.py` (Modify, disjoint from 0044-T1) + `plan_driver.py` + `generate_plan.py` (Modify, disjoint) present; `test_activation.py` ABSENT (Create) | pass — `PLAN_DOMAINS` (dispatch role) at `plan_schema.py:49`; `_ROLE_OF_DOMAIN` at `plan_driver.py:117-122`; `_PLAN_TRANSLATORS` at `generate_plan.py:286-291`; `_dispatch_domains` at `plan_orchestrator.py:358-383`; `server.py:784`/`plan_loop.py:77` iterations | pass — the 18-agent roster + §1-13/§14-15 partition confirmed in `design/specialist-plan-contracts.md` (§14 genetics + §15 labs cross-cutting) | pass — no existing activation gate; grows the existing registries (RT-009 dispatch role, distinct from 0044's stored-key role) | Grounded |
| ADR-0046-T2 | pass — `plan_loop.py` (Modify, disjoint from 0043-T3) present; `test_large_change_fraction.py` ABSENT (Create) | pass — `LARGE_CHANGE_THRESHOLD_DOMAINS = 3` at `plan_loop.py:51`; the `_change_magnitude(...) >= LARGE_CHANGE_THRESHOLD_DOMAINS` check at :203; the comment (:49) confirms "3 with a closed 4-domain universe = a 3-of-4 majority" | pass — the constant + the check + `_change_magnitude` signature confirmed | pass — re-bases the existing threshold in place (computed against `active_domains`, ADR-0046-T1) | Grounded |
| ADR-0045-T1 | pass — `monitoring_compiler.py` ABSENT (Create); `test_monitoring_compiler.py` ABSENT (Create) | pass — `monitoring_signals`/`adjustment_rules` are net-new ADR-0041 fields (0 hits in `scripts/` — genuinely source-fields, not existing) | pass — compiles the ADR-0041 program's fields 3-4 (ADR-0041-T1); config stored in `plan_model` (ADR-0044-T1) | pass — no existing monitoring compiler | Grounded |
| ADR-0045-T2 | pass — `tiered_executor.py` ABSENT (Create); `test_tiered_executor.py` ABSENT (Create) | pass — the bare `adjust.py` leg (finding-A) at `adjust.py:15-23`; the composed gate (`run_orchestrated`/`compose_gate_dispatch`) present; `adjust.py` untouched (routes THROUGH the composition) | pass — runs the compiled config (ADR-0045-T1); calls the ADR-0043 reconciler (0043-T2) + the ADR-0040 confirm hold (0044-T4) | pass — no existing tiered executor; the only automated adjustment today is the debounced full-composition re-gen (`plan_loop.py:130-180`) it refines | Grounded |
| ADR-0045-T3 | pass — `daily_monitor.py` ABSENT (Create); `scripts/runner/schedule/activate.py` present (Modify); `test_daily_monitor.py` ABSENT (Create) | pass — the ADR-0039 runner IS built (`scripts/runner/` present with `cadence_runner.py` + `schedule/activate.py`); the weekly cadence + disabled-by-default posture present | pass — `scripts/runner/schedule/activate.py` present; the runner's activation pattern confirmed | pass — no existing daily deterministic pass; hosts in the built ADR-0039 runner (extends, does not duplicate the cadence runner) | Grounded |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section (all 15 cite Decision + the specific OQ/Validation/Consequences)
- [x] Every ADR ID in the `adrs` frontmatter has ≥1 task (0041→T1/T2; 0042→T1; 0043→T1/T2/T3; 0044→T1/T2/T3/T4; 0045→T1/T2/T3; 0046→T1/T2)
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-004{1..6}-*.md` all present)

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (all have 4-7)
- [x] All acceptance criteria are binary (each names a function/command/condition with a 0-threshold, an exact count/equality, a present/absent check, a mutation-RED pair, or a numstat=EMPTY probe — the quantitative thresholds copied verbatim from the ADR Validation sections)
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in ≥1 task block (or is a Frozen-untouched row with an explicit no-edit rationale)
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (verified by Kahn's BFS — 15 nodes, 6 groups, all processed, 0 remaining)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed with Dependencies "None (entry point)" (ADR-0041-T1, ADR-0042-T1)
- [x] No parallel group holds two writers of one mutable file (the shared-file writers — `generate_plan.py`, `care_chat.py`, `plan_model.py`, `plan_schema.py`, `plan_loop.py` — are serialized across groups via ordering edges; disjoint regions documented)

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream constraints in their ACs (ADR-0041 uniform shape → 0043-T2 AC-1 reconciles it / 0044-T1 AC-1 stores it / 0045-T1 AC-1 compiles fields 3-4 / 0046-T1 AC via the grown `_PLAN_TRANSLATORS` emitting the migrated shape; ADR-0043 front-door → 0043-T3 AC-3; ADR-0044 config-home → 0045-T1 AC-4)
- [x] Constraint Propagation Table entries have corresponding ACs (dag.md's three constraint rows each map to a task AC)

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section present (the 6 DEFER LIVE-run OQs explicit; the 30 PROCEED resolved-in-spec with a verification pointer)
- [x] Every open question, pending tension, and unmitigated risk has a disposition (26 OQs + 5 tensions + 5 negatives = 36; 30 PROCEED as in-spec tasks/assumptions, 6 DEFER LIVE — per `dispositions.md`)
- [x] Block dispositions have corresponding tasks (none — no concern required a research spike; every PROCEED is a build task or a stated assumption, the decisions are fixed by the ADRs)
- [x] Defer dispositions have justifications (each of the 6 LIVE-run rows states operator-gated real spend AFTER the build, every build AC 0-spend-satisfiable)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in the six in-scope ADRs is covered (0041 Neg-1/2/4 → 0041-T2 AC-4 / 0041-T1 AC-2/AC-4; 0042 Neg-1/3/4 → 0042-T1 AC-4/AC-5/AC-3 + #32 accepted; 0043 Neg-1/2/3/4/5 → 0043-T1/T2/T3 + #33/#34 accepted; 0044 Neg-1/2/3/4 → 0044-T1 AC-4 / 0044-T3+T4 / 0044-T2 / #35 accepted; 0045 Neg-1/2 → 0045-T2 AC-6/AC-1; 0046 Neg-1/2/4 → 0046-T1 AC-5/AC-3/AC-4 + 0046-T2)

### Test Coverage
- [x] Every acceptance criterion appears in ≥1 Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (crown-jewel non-egress, per-ADR freeze-break numstat probes, the store-adversarial battery on the 0044 store-surface tasks, always-on safety floors, deterministic-tier safety, activation mis-fire)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the exemplar's structure (for machine parsing)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists at HEAD 191ccb7e (generate_plan.py, assemble.py, care_chat.py, orchestrate.py, plan_loop.py, server.py, plan_schema.py, track.py, horizons.py, plan_driver.py, scripts/runner/schedule/activate.py — all present; plan_model.py Modify-by-a-prior-task is Created by 0044-T1)
- [x] Every File Manifest `Create` row names a path that does NOT already exist (the 7 new modules + the test files — all confirmed absent)
- [x] Every ADR premise a task relies on was re-verified against the live tree and is still true (the four translators + `_is_complete`; `router.summarize` plan-path use at :356; the five holds at orchestrate.py:337-456; PLAN_DOMAINS/validators/record_plan/resolve_plan; the ADR-0040 hold + LARGE_CHANGE_THRESHOLD_DOMAINS=3; the built ADR-0039 runner; the 0-hits net-new DOMAIN PROGRAM fields — all confirmed, line drifts recorded in the ledger header)
- [x] Every cited input declares its structural assumption AND the live file satisfies it (no phantom inputs — `PLAN_DOMAINS`, `_ROLE_OF_DOMAIN`, `_PLAN_TRANSLATORS`, `store.append`/`keying`, `plan_confirm.mark_pending`, `window_block`'s `plan::<domain>` query, `_dispatch_domains`, `pii_scan.DEFAULT_IDENTITY_CONFIG`, the specialist-plan-contracts roster all confirmed at the cited lines)
- [x] No task proposes an artifact that duplicates an existing capability (no existing DOMAIN PROGRAM schema / context assembler / orchestrator / comprehensive model / activation gate / monitoring compiler / tiered executor / daily pass — all ABSENT; each supersedes or extends an existing surface, never duplicates)
- [x] Repo-Grounding Ledger present, one row per task (15 rows), all Grounded (0 stale-premise / phantom-input / duplicate / action-mismatch; line-drift discrepancies reconciled in the ledger header)
