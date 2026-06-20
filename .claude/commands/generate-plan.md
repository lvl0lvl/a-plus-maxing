---
description: "Generate a followable, safety-gated health plan end-to-end (the closed loop's GENERATE leg): dispatch each plan-domain specialist (full profile) over the de-identified summary + gated wiki, run the reconciled multi-domain pipeline (energy bounce + additive-AE / conflict / Rx-BPMH holds + the medical-liaison adjudication gate), record the survivors, collate the doctor-visit queue, and render. Synthetic-only until real operator data is ingested."
argument-hint: "[--date=YYYY-MM-DD] [--domains=workout,nutrition,supplements,peptides] [--render=dashboard,handout,report]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, mcp__basic-memory__search_notes, mcp__basic-memory__read_note
---

# /generate-plan

Invoke the `generate-plan` skill to produce a plan for a date. Skill is project-local at
`.claude/skills/generate-plan/`.

## Usage

```
/generate-plan [--date=YYYY-MM-DD] [--domains=workout,nutrition,supplements,peptides] [--render=dashboard,handout,report]
```

- `--date` — the plan date (default: today).
- `--domains` — which `PLAN_DOMAINS` to generate (default: all four).
- `--render` — which artifacts to render after recording (default: `dashboard`).

## What it does (read the SKILL for the full process)

1. **Inputs** — the de-identified `router.summarize` summary (0-raw-PII) + the gated wiki + the active
   gates (`clearance_granted`, `red_s_lea_screen`, wearable presence, hard-limits).
2. **Dispatch** each domain specialist (full profile inlined per INV-ROLE-INLINING) over the summary →
   capture the `{specialist, recommendations[], reconciliation{}}` envelope → build `authors`.
3. **Run** `scripts/plan/pipeline.py` `run_generation(authors, …, reauthor=<2nd-PT-dispatch hook>,
   adjudicator=<medical-liaison hook>)` — the reconciled pass + the doctor-visit-queue collation.
4. **Render** via `python -m scripts.generate.generate <artifact>`.
5. **Report** what recorded, what HELD (the honest no-plan states), and the dvq entries for the MD.

The plan + safety reasoning is the specialists' / medical-liaison's (runtime A) — never invented in
code or in the orchestrator's own voice. A held finding records nothing unless the liaison gate releases
it on content; that is the honest state, never bypassed. Synthetic-only until real operator data lands.

Read `.claude/skills/generate-plan/SKILL.md` IN FULL before invoking, plus its authoritative references
(`docs/plan-generation/author-dispatch-process.md` for the per-domain dispatch + the contracts).
