---
title: Session 24 — product pivot; vision doc + V1 PRD via the prd-development pipeline
type: session
permalink: a-plus-maxing/sessions/session-24
created: 2026-06-03
session: S24
---

# Session 24 (2026-06-03)

## Goal (as contracted, revised in-session)

Opened on `hil` (architect the secure PII vault). Walter answered the PII question with **threat-model B** (private data may be transiently processed by the model but never retained or used for training → V1 routes PII-bearing plan reasoning through an individual commercial **no-train API**; the subscription handles PII-free library work). He then redirected to a **product pivot**: the system should be physician-shareable now and a GP-facing product later, needing the Rigor-Framework vision doc the project never had + the V1 product PRD. Scope re-contracted to: author `design/vision.md` + the V1 PRD via the skills-library `prd-development` pipeline.

## What happened

1. **Confirmed the Rigor Framework is already adopted.** Read `skills_library/frameworks/rigor/RIGOR_FRAMEWORK.md` — a-plus-maxing is a near-textbook instantiation (session lifecycle, rotation rule, invariants-get-scripts, PF discipline, role inlining). The one thing the framework names that the project lacked: `design/vision.md`. The genuinely-new machinery is the **product pipeline** (PRD→ADR→spec→build-plan→task-plan→execute), which exists in skills_library and had never been used here.

2. **Authored `design/vision.md`** — the vision-drift anchor. First sentence = what the system IS; the load-bearing **V1 / North-Star boundary** (V1 single-operator local app → GP multi-tenant product); the **"physician-ready, defined"** 5-point bar; enduring principles (gated wiki, PII trust boundary, physician-credible output, compounding rigor, closed-loop outcome tracking). Refined with Walter: physician-ready = the operator OWNS the plan, the physician is collaborator/validator; and the system **tracks progress + outcomes**, not just generates plans.

3. **Ran the `prd-development` pipeline in full** (read SKILL.md + create-prd.md before invoking — PF-S17-01). 7 phases: Intake → Discovery → Draft (Problem Statement first) → Validate (12 gates) → Judge (8-dim rubric) → Review → Finalize. `AskUserQuestion` substituted with prose throughout (Walter override); all PRD content produced by **dispatched worker agents** (create-prd Hard Rule 1), never freelanced.

4. **V1 scope expanded twice via Walter clarifications** — each surfaced, draft revised, re-Validated + re-Judged: (a) operator-agnostic/clonable (friends clone + run their own local instance) + the deliverable is a multi-domain operating plan (peptides/training/nutrition/sleep/supplements); (b) **the big one** — V1 is a local-first **tracking app** (Whoop-style, deeper), not a static handout: local time-series store + import/export ingestion (HealthKit/Watch/Whoop/Garmin/Oura, source-extensible, cron-able) + on-demand template-generated dashboards/reports + lab-recommendation→matrix loop + watch-out questionnaire + projections. My initial "lightweight tracking" default under-scoped him; corrected at the review gate.

5. **PRD finalized** → `docs/prd/PRD-v1-local-first-health-tracking-planning.md` (V2.0, status: Approved). Final gates: Validate 10 Pass / 2 Warning / 0 Fail (COMPLETE); Judge ACCEPT, all 8 dimensions 10/10; 0 Blocking OQ. 9 US, 12 FR, 7 NFR, 10 NG, 7 A, 6 OQ (OQ-3/4/5/6 resolved with Walter; OQ-1/OQ-2 non-blocking).

6. **Pipeline-arc beads filed** `fm4`(ADR)→`rg2`(spec)→`hv6`(build-plan)→`mo4`(task-plan), dep-chained; `hil` recorded (decision settled, formal ADR produced in `fm4`) + blocked on `fm4`, kept OPEN. Wiki-ingestion ADR-backfill bead filed (P2 — the S23 gate was built but never got a `vault/decisions/` ADR).

## Discipline notes

- **Read-before-invoke held** (PF-S17-01): read the full PRD pipeline before running it; flagged that each downstream stage (create-adr/spec/build-plan/task-plan) gets the same treatment.
- **Hard-Rule-1 held**: orchestrator coordinated; every PRD draft/validate/judge/revise was a dispatched worker. Two false-economy temptations resisted ("I've read the skill, I'll write it myself").
- **The pivot is an INTENTIONAL vision change**, not drift — `design/vision.md` authored this session to be the new anchor. The old `project_overview` memory ("NOT a tracker or SaaS; logging minimized") directly contradicted the pivot → corrected.
- **API vs subscription, verified not asserted**: confirmed Anthropic's data-handling (commercial API = no-train + 30-day; consumer = up-to-5yr + training-eligible; ZDR = Enterprise-only) against current docs before recommending the threat-model-B / individual-no-train-API posture.

## State at close

- `design/vision.md` + the Approved V1 PRD shipped on `feature/product-vision-prd`. No code built — design only.
- Next = the ADR stage (`fm4`, READY); then spec/build-plan/task-plan; library-population runs in parallel (gated).
- `hil` decision settled (threat-model B); its formal ADR is the `fm4` deliverable.

See [[design/vision]], `docs/prd/PRD-v1-local-first-health-tracking-planning.md`, HANDOFF S24 (contract + evaluation + What Is Next).
