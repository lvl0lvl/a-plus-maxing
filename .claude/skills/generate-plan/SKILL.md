---
name: generate-plan
description: Generate a followable, safety-gated health plan end-to-end (the closed loop's GENERATE leg, the A′ subscription-driver path). De-identifies the raw intake, then dispatches each plan-domain specialist + each safety lens as a SUBSCRIPTION agent (full profile) over the de-identified summary + the gated wiki, and DRIVES the ONE shared driver (`plan_driver.drive`) that runs assemble / the composed gate_dispatch / the bounded revise loop (energy bounce, additive-AE / cross-domain-conflict / Rx-BPMH holds, the medical-liaison adjudication gate) — the skill never re-hosts the safety loop (the no-fork constraint). Records the survivors, collates the doctor-visit queue, and renders the plan. Reasoning is the specialists' (runtime A), never invented in code. Synthetic-only until real operator data is ingested (operator-gated).
argument-hint: "[--date=YYYY-MM-DD] [--domains=workout,nutrition,supplements,peptides] [--render=dashboard,handout,report]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, mcp__basic-memory__search_notes, mcp__basic-memory__read_note
---

# generate-plan

The operator-facing INVOCATION path for the closed loop's GENERATE leg (the **A′ subscription-driver**
path). The pipeline is wired in code (`scripts/plan/`); this skill is its front door — it de-identifies
the raw intake, dispatches each plan-domain specialist + each safety lens as a SUBSCRIPTION agent over
the de-identified summary, and DRIVES the ONE shared driver (`plan_driver.drive`) that runs
assemble/gates/revise via the composed `gate_dispatch`. The skill DRIVES the driver — it does NOT
re-implement the safety loop (the no-fork-at-the-skill-level constraint, below).

**This skill does not re-decide the plan.** Under runtime A (`vault/design/plan-generation-pipeline-v1.md`,
operator decision S68) the plan + safety reasoning is the dispatched specialists' / medical-liaison's;
`scripts/` holds the wiring + the gates. The orchestrator (you) dispatches each specialist with its full
profile over the de-identified summary, captures the structured output, and feeds each captured envelope
to the shared driver per yielded dispatch-request. Originating plan content in code or in the
orchestrator's own voice is the failure this skill exists to prevent.

**No fork at the skill level (the crown-jewel constraint).** The autonomous bounded revise loop — the
scratch-store lifecycle, the gate→branch→re-dispatch sequencing, the `safety_passed is True` surface
gate, the bounded cap, the scratch-and-promote — lives in EXACTLY ONE definition, `plan_driver.drive`.
This skill DRIVES that one driver (the consumer advances it and SENDs back the captured authors per
yielded request); it NEVER re-hosts a copy of the loop. A skill-prose copy of the safety loop is the
A-naive forked-safety-loop failure class ADR-0026 rejects.

**Authoritative references (read, do not restate):**
- `docs/plan-generation/author-dispatch-process.md` — the per-domain author dispatch, the universal
  recommendation contract + per-domain `payload` shapes, the `reconciliation` envelope keys, the
  five reconcile behaviors, the medical-liaison adjudication envelope + the override-record schema.
- `docs/plan-generation/adjust-dispatch-process.md` — the ADJUST leg (a DIFFERENT flow; do not use
  this skill to adjust an existing plan — `adjust_plan` is the adjust caller).
- `scripts/plan/plan_step.py` `step` — the per-round STEP-HARNESS this skill DRIVES THROUGH (the pause
  boundary, skill → harness → driver; a `plan_driver.drive` generator cannot pause for the Agent tool);
  `scripts/plan/plan_driver.py` `drive` — the ONE shared driver the harness advances (the no-fork crown
  jewel); `scripts/plan/gate_dispatch.py` `compose_gate_dispatch` — the composed quality+safety gate the
  driver gates through; `scripts/plan/deid_in.py` `deid_in` / `scripts/model/client.py`
  `ModelClient.deidentify` — the de-id-IN boundary.

## When to Use

- Producing a NEW dated plan across one or more `PLAN_DOMAINS` (workout / nutrition / supplements /
  peptides) for the operator.
- Re-running generation for a date after the operator's state or the wiki changed.

## When NOT to Use

- ADJUSTING an existing plan from tracked actuals → that is the ADJUST leg (`adjust_plan` +
  `adjust-dispatch-process.md`), a separate progression flow.
- Rendering an already-recorded plan with no new generation → `python -m scripts.generate.generate
  <artifact>` directly.
- Researching a compound/biomarker for the wiki → `/aplus-research`.

## The path (what runs)

```
Phase 0  de-id IN ── deid_in(raw_intake, ModelClient.deidentify) [0-raw-PII] + the gated wiki + active gates
Phase 1  per-domain author dispatch (runtime A, full profile inlined) ── one SUBSCRIPTION specialist per
            domain over the de-identified summary
            → capture {specialist, recommendations[], reconciliation{}} → build  authors = {domain: envelope}
Phase 2  drive the ONE shared driver THROUGH the step-harness ── plan_step.step(serialized_state, …)
            advances plan_driver.drive ONE yield + returns (pending Request(kind, payload), serialized_state);
            fulfil each AUTHOR / GATE / REAUTHOR / ADJUDICATOR request via a SUBSCRIPTION agent dispatch and
            re-call step with the appended envelope (skill → harness → driver). The driver runs assemble /
            the composed gate_dispatch / the bounded revise loop; the skill never re-hosts it. The harness
            value-scans each DERIVED yield payload (GATE assembled-plan payload[0] / ADJUDICATOR finding /
            REAUTHOR constraint) before it leaves the process — 0 raw-PII, fails closed on a hit.
            ├─ GATE          → dispatch the judge + each safety lens → return the raw {judge, review} verdicts
            ├─ energy bounce → REAUTHOR(domain, constraint)  = a 2nd personal-trainer dispatch
            └─ held finding  → ADJUDICATOR(safety_finding)   = a medical-liaison dispatch (the gate)
Phase 3  render ── reinsert_out (deterministic de-id OUT) → reemit_maintained / scripts.generate.generate
Phase 4  report ── what recorded, what HELD (the honest no-plan states), the dvq entries for the MD
```

## Phase 0 — de-id IN (the PII boundary)

1. The author's ONLY operator-state source on the A′ path is the **de-identified summary** the de-id-IN
   boundary `deid_in(raw_intake, client)` returns — a synchronous Python `ModelClient.deidentify` call
   (the ADR-0027 no-train backend, via `deid_in`) over the raw intake, producing the de-identified
   band/class summary the dispatches author over. It is the 0-raw-PII token state. Never hand a specialist
   raw operator data (ADR-0006-T0). **Disambiguation:** `router.summarize` is NOT the A′ de-id-IN /
   operator-state source — it survives ONLY as the persisted-side store-read gate (the deterministic
   store-summarizer the persisted path uses, unchanged, per `scripts/plan/deid_in.py`: "`router.summarize`
   SURVIVES UNCHANGED as the persisted-side de-id (the store-read gate)").
2. Name the **active gates**: `clearance_granted` (the LM-01 July-13 clinician clearance unlock for
   workout `load`), `red_s_lea_screen` (the nutrition critical-floor screen), wearable presence,
   hard-limits. These flow to every domain's `compute_plan` via `gates`.
3. Determine the **domains** to generate (default: all four `PLAN_DOMAINS`; `--domains` narrows).
4. The gated **wiki** (`vault/library/`, `vault/compounds/`, `vault/biomarkers/`) is the specialists'
   evidence surface — canonical, vetted, goal-agnostic (the specialist personalizes at dispatch).

## Phase 1 — dispatch each domain author as a SUBSCRIPTION agent (the load-bearing step)

For each domain, dispatch the specialist as a SUBSCRIPTION Claude Code agent over the de-identified
summary (never the raw intake — the dispatch payload carries the summary only, 0 raw PII), following
`author-dispatch-process.md` "Dispatching an author":
- **Inline the full role profile verbatim** (`~/Documents/Projects/skills_library/roles/<role>/agent.md`
  or `.claude/agents/<role>/agent.md`) — INV-ROLE-INLINING + the `enforce-role-inlining` hook + the
  Agent Role Profile Mandate. Roles: `personal-trainer` (workout), `nutritionist` (nutrition),
  `supplement-specialist` (supplements), `peptide-specialist` (peptides).
- Provide the de-identified summary + the active gates + the universal recommendation contract; require
  the exact JSON envelope `{specialist, recommendations[], reconciliation{}}` (or the thin-library
  sentinel). The dispatch is **read-only reasoning** — the specialist returns JSON, never writes the store.
- Carry the **CLAIM-PHRASING RULE** (author-dispatch-process.md): a `claim` must not contain a hard-limit
  subject term even negated (assemble's fail-closed HALT strikes it). Describe avoidance positively.
- The `reconciliation` envelope is what makes the cross-domain pass work — workout `energy_cost_kcal`,
  nutrition `energy_budget`, supplement/peptide `ae_profile` (the canonical AE-class vocabulary), and any
  declared `conflicts`. Brief each specialist to populate it (see the doc's envelope table).

Collect the captured envelopes into `authors = {domain: envelope}`.

## Phase 2 — drive the ONE shared driver THROUGH the step-harness (the no-fork crown jewel + the gates)

DRIVE the shared driver THROUGH the `plan_step.py` step-harness. Do NOT hold a live `plan_driver.drive`
generator object across Agent-tool dispatches (a generator cannot pause for the Agent tool), do NOT call
`pipeline.run_generation` directly, and do NOT re-host the loop. The harness is the PAUSE BOUNDARY
(skill → harness → driver):

- `plan_step.step(serialized_state, …)` advances `plan_driver.drive` EXACTLY ONE yield from the
  serialized memo-cache state and returns `(pending_request, serialized_state)`. On the FIRST call pass
  `serialized_state=None`.
- The `pending_request` is a typed `Request(kind, payload)` with `kind` one of `AUTHOR` / `GATE` /
  `REAUTHOR` / `ADJUDICATOR`. FULFIL it via a SUBSCRIPTION agent dispatch (full role profile inlined per
  INV-ROLE-INLINING), then re-call `plan_step.step(serialized_state, fulfilled_envelope=<envelope>, …)`
  with the just-fulfilled envelope appended. Repeat until `step` returns `pending_request = None` — the
  run completed (read its result via `plan_step.result_of`). The `run_orchestrated` consumer
  (`scripts/plan/plan_orchestrator.py`) is the reference in-process driver of the SAME drive-protocol.

Per-kind fulfilment (each a SUBSCRIPTION agent dispatch, then a `step` re-call with the envelope):

- **`AUTHOR` (`payload = (domains, summary, gates)`)** — dispatch each domain's specialist (Phase 1),
  capture its envelope, and send back the `{domain: envelope}` authors fragment.
- **`GATE` (`payload = (assembled_plan, gate_producer)`)** — dispatch the QUALITY judge AND each SAFETY
  LENS (`medical-safety-reviewer`, `health-edge-case-reviewer`, full profile inlined) as SUBSCRIPTION
  agents over the `assembled_plan` and return the RAW `{judge, review}` verdicts. Return the raw verdicts
  ONLY — the driver composes them via `compose_disposition` (the ONE composition site) and applies the
  fail-closed `safety_passed is True` surface gate; the skill builds NO disposition and re-derives no
  release. (`gate_producer`, the `payload[1]` callable, is the `compose_gate_dispatch`-built RAW-VERDICT
  producer — the in-process test producer; on the LIVE path the skill dispatches the judge + lens agents
  itself and returns the raw verdicts.)
- **`REAUTHOR` (`payload = (domain, constraint)`)** — the energy bounce: fires when nutrition's
  `energy_budget` says the workout is un-fuelable. `constraint` is `{"sustainable_training_kcal":
  <ceiling>}`. Dispatch a SECOND personal-trainer (full profile) under that ceiling → return the new
  workout envelope (it MUST carry `reconciliation.energy_cost_kcal` ≤ ceiling, or the workout is HELD —
  never an un-fuelable load).
- **`ADJUDICATOR` (`payload = (safety_finding,)`)** — fires for every held finding (additive-AE /
  cross-domain-conflict / Rx-BPMH). Dispatch the `medical-liaison` (full profile) over the
  `safety_finding` → return the adjudication envelope (author-dispatch-process.md "the liaison
  adjudication envelope"). The driver's inner engine validates it on CONTENT (INV-OVERRIDE-RECORD-SCHEMA)
  and never builds an override path for a CRITICAL / H1-H2 finding (INV-CRITICAL-NON-OVERRIDABLE); a
  content-valid override RELEASES the hold, anything else leaves the block standing (the safe no-plan
  default). The skill returns ONLY the raw envelope — the release stays in the inner engine's `adjudicate`.

**The NEW value-scan (the crown-jewel 0-leak over the DERIVED yields).** The harness value-scans every
DERIVED yield payload BEFORE it leaves the process to a subscription agent — the GATE assembled-plan
(`payload[0]`), the ADJUDICATOR safety-finding, and the REAUTHOR constraint — reusing
`pii_scan.scan_text_full` (the same value-scan the `deid_in` boundary uses). These artifacts are DERIVED
from the engine, so their PII-freeness is transitive-but-unverified (the AUTHOR seam is structurally
clean — the orchestrator holds only the de-identified summary, so it is NOT re-scanned). 0 raw-PII; on a
hit the harness FAILS CLOSED (the payload does NOT reach the agent) — the first-ever scan over those
derived artifacts.

**No fork at the skill.** The autonomous bounded revise loop — the scratch-store lifecycle, the
gate→branch→re-dispatch sequencing, the `safety_passed is True` surface gate, the bounded cap, the
scratch-and-promote — lives in EXACTLY ONE definition (`plan_driver.drive`); the composition is
`compose_disposition` (the ONE site); the adjudication release stays in the inner engine's `adjudicate`.
This skill DRIVES that one driver via the harness — it NEVER re-hosts the loop, re-composes the
disposition, or re-derives the release.

**Do not bypass a hold.** A held finding with no adjudicator dispatch stays held (records nothing) —
that is the honest, correct state, not a failure to route around.

For a synthetic/test run, the dispatch seam + hooks return pre-captured fixture envelopes (see
`tests/plan/test_generate_plan_skill_glue.py` for the glue contract + `tests/plan/test_plan_step.py` for
the harness drive + `tests/plan/test_revise_loop.py`); for a real run they are live SUBSCRIPTION agent
dispatches.

## Phase 3 — render (de-id OUT)

Render the recorded store, then re-insert the operator identity OUT under the gitignored boundary:
`reinsert_out(html, target_path)` (deterministic, model-free — the de-id OUT pass, gated on a
confirmable-gitignored target) → `reemit_maintained(...)` / `python -m scripts.generate.generate
<dashboard|handout|report>`. The renderers read ONLY `store_read` (the data-out PII boundary) and show
the followable plan + the honest awaiting states for un-generated/held domains.

## Phase 4 — report

State plainly: which domains RECORDED, which were HELD and why (`energy-bounce-held` /
`additive-ae-held` / `cross-domain-conflict-held` / `rx-bpmh-held` / `red-s-lea-clinical-routing`), and
the `dvq_entries` collated for the MD (each carrying the adjudicated outcome — cleared-with-override or
block-stands). A held domain is the honest no-plan state, surfaced, never silently dropped.

## Running + verifying (what IS vs ISN'T mock-testable)

- **Mock-tested (the glue contract — 0 live spend):** `tests/plan/test_generate_plan_skill_glue.py`
  exercises the A′ glue over the merged seams with FIXTURE dispatch — the de-id-IN routes through
  `ModelClient.deidentify` (not `router.summarize`), the glue DRIVES the shared driver THROUGH
  `plan_step.step` to a promoted synthetic run (0 synchronous agent calls inside `drive` — every
  dispatch is a yielded-request fulfilment), the FULL serialized dispatch payload carries 0 raw-PII
  tokens, AND the NEW harness value-scan over the DERIVED GATE / ADJUDICATOR / REAUTHOR yield payloads
  catches a planted leak (fails closed) while a clean payload passes. The harness drive itself is covered
  by `tests/plan/test_plan_step.py`, the driver loop by `tests/plan/test_plan_driver.py` /
  `tests/plan/test_revise_loop.py`, the inner engine by `tests/plan/test_pipeline.py`. `bash
  scripts/core-capability-audit.sh` (it runs the A′ `--self-test` internally; the shell audit takes no
  flags) proves the wired path stays green.
- **NOT mock-testable — the S94 operator-present attestation (the live dispatch deferral):** the LIVE
  subscription dispatch over REAL specialist + lens agents — the skill dispatching real agents per
  harness round, real key, real spend — is the S94 operator-present LIVE-test attestation, NOT a
  mock-test target. The glue test drives the harness with a FIXTURE `dispatch`, never a real agent; it
  STRUCTURALLY only ever holds the `deid_in` summary + the harness's serialized state. Whether a REAL
  subscription agent receives only a PII-free payload on the LIVE path — the residual
  0-raw-PII-to-a-REAL-agent property (SEC-6) — is now ENFORCED at the harness boundary by the value-scan
  (the build verifies the scan fires + fails closed on a planted leak); the LIVE 0-raw-PII-to-a-REAL-
  agent end-to-end run is observed at the S94 operator-present checkpoint, not in this mock-tested build.

## What is deliberately NOT here

- **The ADJUST leg** — adjusting an existing plan from tracked actuals is `adjust_plan` (a separate
  progression flow); this skill GENERATES.
- **A re-hosted safety loop** — the autonomous bounded revise loop lives in EXACTLY ONE definition
  (`plan_driver.drive`); this skill DRIVES that one driver, it never re-implements the loop (the
  no-fork-at-the-skill-level constraint). The reasoning is the specialists' (runtime A); the skill is
  agent-in-the-loop by design over the de-identified summary, not a scripted pipeline that invents plan
  content.
- **Real operator data** — populated locally (gitignored) per ADR-0005, never committed. Until then,
  runs are on synthetic fixtures.
