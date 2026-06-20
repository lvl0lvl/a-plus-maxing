---
name: generate-plan
description: Generate a followable, safety-gated health plan end-to-end (the closed loop's GENERATE leg). Dispatches each plan-domain specialist (full profile) over the de-identified operator summary + the gated wiki, runs their output through the reconciled multi-domain pipeline (energy bounce, additive-AE / cross-domain-conflict / Rx-BPMH holds, the medical-liaison adjudication gate), records the survivors, collates the doctor-visit queue, and renders the plan. Use to produce a plan for a date; reasoning is the specialists' (runtime A), never invented in code. Synthetic-only until real operator data is ingested (operator-gated).
argument-hint: "[--date=YYYY-MM-DD] [--domains=workout,nutrition,supplements,peptides] [--render=dashboard,handout,report]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, mcp__basic-memory__search_notes, mcp__basic-memory__read_note
---

# generate-plan

The operator-facing INVOCATION path for the closed loop's GENERATE leg. The pipeline is wired in
code (`scripts/plan/`) but had no front door: `orchestrate.generate_plans` (the cross-domain
terminal) had no production caller until `scripts/plan/pipeline.py` `run_generation`, and nothing
walked the orchestrator through the live specialist dispatches that produce its `authors` input.
This skill is that front door — it codifies the dispatch lifecycle around the existing functions
with the safety gates inline.

**This skill does not re-decide the plan.** Under runtime A (`vault/design/plan-generation-pipeline-v1.md`,
operator decision S68) the plan + safety reasoning is the dispatched specialists' / medical-liaison's;
`scripts/` holds the wiring + the gates, never a model client. The orchestrator (you) dispatches each
specialist with its full profile, captures the structured output, and feeds it to the seam. Originating
plan content in code or in the orchestrator's own voice is the failure this skill exists to prevent.

**Authoritative references (read, do not restate):**
- `docs/plan-generation/author-dispatch-process.md` — the per-domain author dispatch, the universal
  recommendation contract + per-domain `payload` shapes, the `reconciliation` envelope keys, the
  five reconcile behaviors, the medical-liaison adjudication envelope + the override-record schema.
- `docs/plan-generation/adjust-dispatch-process.md` — the ADJUST leg (a DIFFERENT flow; do not use
  this skill to adjust an existing plan — `adjust_plan` is the adjust caller).
- `scripts/plan/pipeline.py` `run_generation` — the seam this skill invokes.

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
Phase 0  gather inputs ── router.summarize(store_read) [0-raw-PII] + the gated wiki + active gates
Phase 1  per-domain author dispatch (runtime A, full profile inlined) ── one specialist per domain
            → capture {specialist, recommendations[], reconciliation{}} → build  authors = {domain: envelope}
Phase 2  run the reconciled pass ── pipeline.run_generation(authors, store_read, root, plan_date=…,
            on_date=…, gates=…, reauthor=<hook>, adjudicator=<hook>)
            ├─ energy bounce  → reauthor(domain, constraint)  = a 2nd personal-trainer dispatch
            └─ held finding   → adjudicator(safety_finding)   = a medical-liaison dispatch (the gate)
Phase 3  render ── python -m scripts.generate.generate <dashboard|handout|report>
Phase 4  report ── what recorded, what HELD (the honest no-plan states), the dvq entries for the MD
```

## Phase 0 — inputs (the PII boundary)

1. The author's ONLY operator-state source is the **de-identified summary** (`router.summarize(store_read)`)
   — the 0-raw-PII token state. Never hand a specialist raw operator data (ADR-0006-T0).
2. Name the **active gates**: `clearance_granted` (the LM-01 July-13 clinician clearance unlock for
   workout `load`), `red_s_lea_screen` (the nutrition critical-floor screen), wearable presence,
   hard-limits. These flow to every domain's `compute_plan` via `gates`.
3. Determine the **domains** to generate (default: all four `PLAN_DOMAINS`; `--domains` narrows).
4. The gated **wiki** (`vault/library/`, `vault/compounds/`, `vault/biomarkers/`) is the specialists'
   evidence surface — canonical, vetted, goal-agnostic (the specialist personalizes at dispatch).

## Phase 1 — dispatch each domain author (the load-bearing step)

For each domain, follow `author-dispatch-process.md` "Dispatching an author":
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

## Phase 2 — run the reconciled pass (the seam + the two hooks)

Call `pipeline.run_generation(authors, store_read, root, plan_date=…, on_date=…, gates=…,
reauthor=…, adjudicator=…)`. It runs `generate_plans` (compute → reconcile → adjudicate-held → record)
then `collate_doctor_visit_queue`, returning the results + `dvq_entries`. The two hooks are live
re-dispatches you supply:

- **`reauthor(domain, constraint)`** — fires when nutrition's `energy_budget` says the workout is
  un-fuelable. `constraint` is `{"sustainable_training_kcal": <ceiling>}`. Dispatch a SECOND
  personal-trainer (full profile) under that ceiling → return the new workout envelope (it MUST carry
  `reconciliation.energy_cost_kcal` ≤ ceiling, or the workout is HELD — never an un-fuelable load).
- **`adjudicator(safety_finding)`** — fires for every held finding (additive-AE / cross-domain-conflict /
  Rx-BPMH). Dispatch the `medical-liaison` (full profile) over the `safety_finding` → return the
  adjudication envelope (author-dispatch-process.md "the liaison adjudication envelope"). The gate
  validates it on CONTENT (INV-OVERRIDE-RECORD-SCHEMA) and never builds an override path for a
  CRITICAL / H1-H2 finding (INV-CRITICAL-NON-OVERRIDABLE). A content-valid override RELEASES the hold;
  anything else leaves the block standing — the safe no-plan default.

**Do not bypass a hold.** A held finding with no adjudicator dispatch stays held (records nothing) —
that is the honest, correct state, not a failure to route around.

For a synthetic/test run, the hooks may return pre-captured fixture envelopes (see
`tests/plan/test_pipeline.py`); for a real run they are live agent dispatches.

## Phase 3 — render

`python -m scripts.generate.generate dashboard` (and `handout` / `report` as `--render` requests) over
the recorded store. The renderers read ONLY `store_read` (the data-out PII boundary) and show the
followable plan + the honest awaiting states for un-generated/held domains.

## Phase 4 — report

State plainly: which domains RECORDED, which were HELD and why (`energy-bounce-held` /
`additive-ae-held` / `cross-domain-conflict-held` / `rx-bpmh-held` / `red-s-lea-clinical-routing`), and
the `dvq_entries` collated for the MD (each carrying the adjudicated outcome — cleared-with-override or
block-stands). A held domain is the honest no-plan state, surfaced, never silently dropped.

## Running + verifying

- **Deterministic (no agent):** `tests/plan/test_pipeline.py` exercises `run_generation` over fixture
  authors + fixture hooks — a clean pass, the cleared-held-finding stitch (mutation-proven against the
  no-adjudicator control), block-stands queuing, the `on_date` default, and the store-surface battery.
  `scripts/core-capability-audit.sh --self-test` proves the wired path stays green.
- **Real-dispatch E2E (the integration mandate — verification means running the production path):**
  dispatch ≥1 real specialist (full profile) over a PII-free SYNTHETIC summary, feed the captured
  envelope through `run_generation`, render, and inspect the plan. Captured runs live under
  `docs/plan-generation/examples/` (the per-domain author outputs, the bounce pair, the liaison
  adjudication/conflict/BPMH envelopes — see author-dispatch-process.md).

## What is deliberately NOT here

- **The ADJUST leg** — adjusting an existing plan from tracked actuals is `adjust_plan` (a separate
  progression flow); this skill GENERATES.
- **A non-interactive auto-dispatch CLI** — the reasoning is the specialists' (runtime A); the skill is
  agent-in-the-loop by design, not a scripted pipeline that invents plan content.
- **Real operator data** — populated locally (gitignored) per ADR-0005, never committed. Until then,
  runs are on synthetic fixtures.
