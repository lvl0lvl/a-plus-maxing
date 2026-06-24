---
title: plan-quality-rubric
type: note
permalink: a-plus-maxing/design/plan-quality-rubric-1
---

# Plan-Quality Rubric (V1)

The maintained quality bar the post-assembly **quality judge** (`scripts/plan/quality_judge.py`,
ADR-0023-T1) scores an assembled plan against. The judge is producer-independent: it receives
the assembled plan (`{"sections": [...]}`, the `assemble`/`run_generation` output) and THIS
rubric — never the specialists' self-assessments nor the orchestrator's notes. It scores QUALITY
(followability, coherence, internal consistency, completeness); it is DISTINCT from the
clinical-SAFETY review (ADR-0024-T1), which screens clinical risk over the composed plan. Both
wire into the orchestrator's `gate_dispatch=` seam; neither re-implements the other.

This rubric is DATA the judge scores against — revisable as the quality bar evolves, without a
code change. Each dimension carries band anchors (0-3 / 4-6 / 7-8 / 9-10) and at least one
auto-fail. The judge follows the produce->judge discipline: score each dimension against its
anchor, return ACCEPT (every dimension at the minimum, default >=9) or REVISE (specific, fixable
gaps captured as deductions).

## Verdicts

- **ACCEPT** — every scored dimension at or above the minimum band (default >=9) AND no auto-fail
  fired. The plan is followable, coherent, internally consistent, and complete.
- **REVISE** — at least one dimension below the minimum band, OR an auto-fail fired. The verdict
  cites the failing dimension(s) as deductions the revise loop (ADR-0022-T2) hands back. A seeded
  quality defect MUST land here, never ACCEPT.

## Dimensions

### Followability

Can the operator actually act on the plan as written? Each surfaced recommendation is concrete and
executable (a named intervention with the parameters needed to do it), not an abstraction.

- **9-10** — every actionable recommendation is concrete and executable as written.
- **7-8** — recommendations are mostly executable; a few need the operator to infer a parameter.
- **4-6** — several recommendations are abstract or under-specified to act on.
- **0-3** — the plan is not actionable; recommendations are vague directives, not followable steps.
- **Auto-fail** — an in-scope domain section surfaces 0 actionable recommendations (the
  `assemble._coverage_gap` empty-output shape, `coverage_gap == "no-recommendations"`). The gap
  disclosure makes it HONEST, not followable: the operator got nothing to act on for that domain,
  so the plan is sent to REVISE to fill it (re-dispatch the specialist), never surfaced ACCEPT.

### Coherence

Do the sections read as one plan with a single through-line, not a stapled-together set of
disconnected domain outputs? Each section reflects the same operator goals/state.

- **9-10** — sections form one coherent plan; each ties back to the operator's stated goals.
- **7-8** — coherent overall; one section's framing drifts slightly from the others.
- **4-6** — sections read as loosely related; the through-line is weak.
- **0-3** — sections are disconnected; no shared operator-goal through-line.
- **Auto-fail** — a section is empty/incoherent: it carries an in-scope coverage-gap with neither
  a vetted recommendation nor a usable disclosure (the `assemble._coverage_gap` empty-output
  shape with nothing the operator can read as a plan).

### Internal consistency

Do the recommendations agree with each other? No two sections (or two recommendations) assert
mutually-contradictory targets the operator cannot satisfy at once.

- **9-10** — all targets and recommendations are mutually consistent.
- **7-8** — consistent; one pair of recommendations is in mild tension, easily reconciled.
- **4-6** — a real tension exists between two recommendations that needs reconciling.
- **0-3** — the plan is internally contradictory; following one recommendation violates another.
- **Auto-fail** — two sections set mutually-contradictory targets (e.g. one section's
  recommendation targets X and another targets not-X for the same axis) — a plan the operator
  cannot follow without violating itself.

### Completeness

Does every in-scope domain get an honest section — a vetted recommendation set OR an explicit
coverage-gap disclosure — with no in-scope domain silently dropped?

- **9-10** — every in-scope domain has an honest section (recommendations or a disclosed gap).
- **7-8** — every domain present; one section's disclosure is thinner than ideal.
- **4-6** — a domain's section is present but materially under-developed.
- **0-3** — an in-scope domain is missing or its section is empty without disclosure.
- **Auto-fail** — an in-scope domain section is empty (0 recommendations) and lacks the honest
  coverage-gap disclosure that would make the gap legible to the operator.