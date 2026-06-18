# Plan-Author Dispatch Process (V1, runtime A)

**What this is.** The repeatable process for generating one plan domain end-to-end: dispatch a
plan-author specialist, run its output through the safety composer, record the plan, and render it
on the dashboard. `personal-trainer` / `workout` is the first wired instance (S70, the PF-S63-02
core-capability proof); **the other three plan-domain authors plug into the IDENTICAL machinery** —
this doc is what lets them run with a known, small per-domain delta.

**Authoritative design:** `vault/design/plan-generation-pipeline-v1.md`. **Code:**
`scripts/plan/generate_plan.py`. **Mechanical gate:** `scripts/core-capability-audit.sh`.

## The path (what runs)

```
author dispatch (runtime A)          generate_plan(domain, author_output, store_read, root, ...)
   |  full profile inlined           ┌───────────────────────────────────────────────────────┐
   |  + de-identified summary         │ router.summarize(store_read)  → the 0-raw-PII summary  │
   v  + output contract               │ assemble([domain], summary, roster) → 4 safety filters │
{specialist, recommendations[]}  ───► │ translate surviving recs → plan_schema domain plan     │
                                       │ plan_schema.record_plan(domain, plan, date, who, root) │
                                       └───────────────────────────────────────────────────────┘
                                                  │  store:  plan::<domain>
                                                  v
                                   generate.run("dashboard", _root, _today)  → followable plan card
```

Runtime A (operator decision, S68): the author is an **interactively dispatched agent**, not a
scripted API client. The orchestrator dispatches the specialist, captures its structured output, and
feeds it to `generate_plan`. `scripts/` holds no model client by design.

## The universal recommendation contract (every author emits this)

`assemble` filters on these fields; `generate_plan` lifts the domain `payload` of the SURVIVING
recommendations into the plan. The envelope is `{"specialist": <slug>, "recommendations": [rec, ...]}`,
or the thin-library sentinel `{"specialist": <slug>, "thin_library": true}`.

| field | required | role |
|---|---|---|
| `claim` | yes | one sentence; assemble's HALT filter text-matches the operator's hard-limits against it |
| `source` | yes | citation / wiki provenance — an unsourced rec is dropped (sourcing-completeness) |
| `confidence_tier` | yes | evidence tier |
| `reversibility` | yes | reversibility note |
| `category` | yes | intervention-class — assemble's class-aware HALT keys on it; **missing/None fails CLOSED** when a hard-limit is present |
| `grounding` | no | `"animal"`/`"in-vitro"` → population-mismatch flag |
| `numbers` | no | each `{units, reference_range, ...}`; present-but-incomplete numbers drop the rec |
| `payload` | yes | the domain-structured renderable content (per-domain shape below) |

### Per-domain `payload` shapes (the `plan_schema` plan schemas)

- **workout** — `{name (str), sets (int 1–100), reps? (str|int), detail? (str), load? (str)}`. WIRED.
- **nutrition** — the plan is `{calorie_goal (int>0), macros {protein,carbs,fat ints>0}, meals[{name, contents?, kcal?}], water_l?}`. A nutrition author emits recs whose payloads compose to that plan; **a per-domain translator must aggregate** (the workout translator is 1 rec → 1 exercise; nutrition is N recs → one macro/meals plan). TODO.
- **supplements** — `{items: [{name, dose (str), timing?}]}`. 1 rec → 1 item. TODO.
- **peptides** — `{compound (str), dose (str), route (str), cycle_week?, cycle_length_weeks?, tags?, evidence?}`. TODO.

## Adding the next author (the small per-domain delta)

1. Add a translator `_to_<domain>_plan(recommendations, gates) -> dict | None` to
   `scripts/plan/generate_plan.py` and register it in `_PLAN_TRANSLATORS`. It lifts the surviving
   recs' payloads into the domain's `plan_schema` shape (workout is 1:1; nutrition aggregates).
2. Wire the domain's safety gate(s) through `gates` if it has one (workout = `clearance_granted`;
   **nutrition = the 0.5 critical-floor RED-S/LEA screen** per the pipeline spec — that author
   short-circuits energy-deficit content; supplements/peptides = the compound-band two-pass screen).
3. Add `tests/plan/test_generate_plan.py`-style coverage: happy path, the gate mutation-proven RED,
   struck-rec exclusion, the honest no-plan states, and the store-adversarial four (cross-stream /
   dedupe-idempotent / dedupe-key boundary / changed-value no-op).
4. Dispatch the author for real (below) and run the E2E (below).

## Dispatching an author (runtime A)

1. **Read the deployed profile in full** (`~/Documents/Projects/skills_library/roles/<role>/agent.md`
   or `.claude/agents/<role>/agent.md`) and **inline it verbatim** into the dispatch (INV-ROLE-INLINING
   + the `enforce-role-inlining` hook + the Agent Role Profile Mandate — no abbreviation).
2. Provide the **de-identified summary** as the author's only operator-state source (PII-free token
   state — the same fields `router.summarize` produces). Name the active gates (clearance status,
   wearable presence, hard-limits).
3. Provide the **output contract** above and require the author return exactly the JSON envelope.
4. The dispatch is **read-only reasoning** — the author returns JSON; it does NOT write the store or
   run git (`generate_plan` does the write).

### CLAIM-PHRASING RULE (learned S70 — load-bearing)

`assemble`'s fail-closed HALT filter strikes any rec whose `claim` ASSERTS a hard-limit subject. Its
negation check only inspects the word IMMEDIATELY before the subject, so **"without any overhead
pressing"** still strikes (the intervening "any" defeats the `without` negation) — fail-closed dropped
a legitimate exercise in the S70 E2E (6 recs in, 5 recorded). The fix is NOT to weaken the filter (it
must stay conservative): **author claims must not contain a hard-limit subject term at all, even
negated.** Describe the avoidance positively instead — e.g. "horizontal pulling, elbows to the hips"
rather than "rowing without any overhead pressing". A struck rec is excluded from the plan, never
silently shipped.

## Running + verifying

- **Build/CI proof (deterministic, no agent):** `core-capability-audit.sh` runs
  `python -m scripts.plan.generate_plan --self-test` (seeds a synthetic store, runs the path, asserts
  the dashboard renders the plan). Negative test: `scripts/tests/test_core_capability_audit.sh`.
- **Real-author E2E (the production-path verification — integration mandate):** dispatch the author,
  capture its JSON, then `generate_plan(domain, author_output, store_read, root, plan_date=..., gates=...)`
  against a temp store, then `generate.run("dashboard", _root=..., _today=...)` and inspect the rendered
  card. The S70 workout run is captured at `docs/plan-generation/examples/workout-author-output.example.json`.
- **Verification means running the production path, not just unit tests** (the integration mandate).

## What is deliberately NOT here yet (deferred per the build sequence)

- The other three domain translators + their author dispatches (nutrition / supplements / peptides).
- The step-4 orchestrator reconciler (cross-domain overlap/contradiction + plan-bounce) and the
  medical-liaison terminal safety gate — the `/generate-plan` main agent that wraps `assemble`.
- A standalone full-plan render screen (the dashboard plan card is Slice 1's surface; the operator is
  drafting the dedicated specialist-output screen separately).
- Real operator data: populated locally (gitignored) per ADR-0005; never committed (public repo).
