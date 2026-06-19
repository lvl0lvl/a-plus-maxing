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

- **workout** — `{name (str), sets (int 1–100), reps? (str|int), detail? (str), load? (str)}`. 1 rec → 1 exercise. WIRED (S70).
- **nutrition** — the plan is `{calorie_goal (int>0), macros {protein,carbs,fat ints>0}, meals[{name, contents?, kcal?}], water_l?}`. The author emits ONE day-target rec (payload carries `calorie_goal`/`macros`/`water_l?`) plus one rec per `meal` (payload `{meal: {...}}`); `_to_nutrition_plan` **AGGREGATES** the surviving payloads into one plan (day-target fields last-wins, meals accumulate). Absent targets OR no surviving meal → records nothing (the honest no-plan state). WIRED (S71).
- **supplements** — `{items: [{name, dose (str), timing?}]}`. 1 rec → 1 item (`_to_supplements_plan`). WIRED (S71).
- **peptides** — `{compound (str), dose (str), route (str), cycle_week?, cycle_length_weeks?, tags?, evidence?}`. SINGLE compound per plan: `_to_peptides_plan` takes the first surviving rec's payload (a multi-compound stack is the deferred compound-band). WIRED (S71).

## Adding the next author (the small per-domain delta)

1. Add a translator `_to_<domain>_plan(recommendations, gates) -> dict | None` to
   `scripts/plan/generate_plan.py` and register it in `_PLAN_TRANSLATORS`. It lifts the surviving
   recs' payloads into the domain's `plan_schema` shape (workout is 1:1; nutrition aggregates).
2. Wire the domain's safety gate(s). A single-author OWNED screen is a pre-translation veto in
   `_DOMAIN_GATES` (runs BEFORE translation, returns a distinct honest reason): **nutrition owns the
   0.5 critical-floor RED-S/LEA screen** (`gates["red_s_lea_screen"]` `True`/`"tripped"` →
   `red-s-lea-clinical-routing`, records no energy plan). A per-exercise/per-item gate runs inside the
   translator (workout = `clearance_granted` drops `load`). The cross-compound supplement↔peptide
   two-pass additive-AE screen and the nutrition→workout energy bounce are NOT per-author gates — they
   run in the cross-domain layer (the step-4 reconciler, both WIRED: bounce S72, additive-AE screen S73).
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
  card. Captured real-dispatch runs (PII-free synthetic operator) at `docs/plan-generation/examples/`:
  `workout-author-output.example.json` (S70), and `nutrition-` / `supplements-` / `peptides-author-output.example.json` (S71).
- **Verification means running the production path, not just unit tests** (the integration mandate).
- **Clinician-gated compounds (learned S71).** Dispatched faithfully, the supplement-specialist and
  peptide-specialist are INFORM-class — their single-author output is a DRAFT pre-medical-liaison, not
  an operator-approved directive. The peptide-specialist anchored BPC-157 at H2 (angiogenic auto-block)
  and surfaced it as a decision-support draft with the H2 block + `clinician-clearance:NOT_GRANTED`
  caveat RENDERED on the card (verified in the E2E). "Four authors wired" is NOT "operator-usable":
  the cross-compound additive-AE screen is WIRED (S73, the compound band); the **medical-liaison
  terminal gate** (S74) is the remaining gate between build-complete and operator-usable. The build
  runs on synthetic fixtures (no real operator data).

## The cross-domain layer (orchestrator + reconciler) — WIRED S72

The four single-author plans are computed and recorded INDEPENDENTLY by `generate_plan`. The
cross-domain reconciler (`scripts/plan/orchestrate.py`, the step-4 "two terminal functions" of the
design) runs them as ONE reconciled pass so a cross-domain check can stop an unsafe / un-fuelable plan
BEFORE it is written. The refactor that enables this: `generate_plan.compute_plan(domain, author_output,
store_read, *, gates)` does everything `generate_plan` does EXCEPT the `record_plan` write (it returns a
candidate `{plan, reason, meta, ...}`); `generate_plan` = `compute_plan` + record (its contract is
unchanged); the orchestrator computes every candidate, reconciles, then records the survivors.

```
generate_plans(authors, store_read, root, *, plan_date, gates, reauthor)
  authors = {domain: envelope}  →  compute_plan each  →  reconcile  →  record survivors
```

**The author `reconciliation` envelope key** (top-level, sibling of `recommendations`; `compute_plan`
lifts it into the candidate's `meta`, so the recorded plan shape is unchanged):

- **workout** — `{"reconciliation": {"energy_cost_kcal": <int>}}` (the session's estimated training cost).
- **nutrition** — `{"reconciliation": {"energy_budget": {"sustains": <bool>, "sustainable_training_kcal":
  <int>, "maintenance_kcal": <int>, "bounce_reason"?: <str>}}}` (the nutritionist's verdict, given the
  workout cost). `bounce_reason` is an OPTIONAL human-readable note a `sustains:false` verdict may carry;
  the reconciler reads only `sustains` + `sustainable_training_kcal`, so it is annotation, not a contract key.
- any author — `{"reconciliation": {"conflicts": [{"with_domain": ..., "with": ..., "reason": ...}]}}`
  declares a known cross-domain conflict for the report.
- **supplements / peptides** — `{"reconciliation": {"ae_profile": {"additive_classes": [<token>, ...],
  "interactions": [{"with": <other compound>, "mechanism": <str>, "severity": "low|moderate|high"}]}}}`
  declares the compound's adverse-event profile for the additive-AE screen. `additive_classes` are the
  AE-class tokens the compound CONTRIBUTES (a SHARED token across the supplement + peptide is an additive
  finding); `interactions` are author-declared pairwise interactions whose `with` NAMES the other
  compound by its plan name (the supplement item `name` / the peptide `compound`). **Canonical AE-class
  vocabulary** (so cross-author matching works): `bleeding-risk`, `serotonergic`, `hepatotoxicity`,
  `nephrotoxicity`, `malignancy-risk`, `thrombotic`, `igf-elevation`, `cyp3a4-pgp`, `qt-prolongation`,
  `hypoglycemia`, `immunomodulation`, `sedation`, `stimulant-load` (grounded in the supplement Core-Rule-5
  interaction screen + the peptide Rule-6 H-class axes). `with` matching is exact (normalized
  lowercase/strip): name the compound as the other domain records it; a parenthetical qualifier
  (`fish oil (EPA/DHA)`) is a known V1 precision gap (the shared-class path still catches it).

**`reconcile(candidates)` — four behaviors (no recording):**

1. **RED-S/LEA cross-domain short-circuit** (pipeline Phase 0.5). When nutrition tripped its
   critical-floor screen (`gates["red_s_lea_screen"]` → nutrition reason `red-s-lea-clinical-routing`),
   the reconciler ALSO holds the energy-prescribing WORKOUT plan to clinical-care routing — the screen
   short-circuits workout AND nutrition. Precedence over the bounce.
2. **The nutrition→workout energy BOUNCE** (Phase 2 joint constraint). When nutrition's `energy_budget`
   verdict is `sustains: false`, the reconciler emits a bounce DIRECTIVE; `generate_plans` re-authors the
   workout ONCE via the `reauthor(domain, {"sustainable_training_kcal": ceiling})` hook (runtime A: a
   second personal-trainer dispatch under the energy ceiling). The re-authored plan is recorded only if
   its `energy_cost_kcal` ≤ the ceiling; otherwise the workout is HELD (`energy-bounce-unresolved`), and
   with no `reauthor` hook it is HELD (`energy-bounce-held`) — never an un-fuelable load on the dashboard.
3. **Overlap + conflict detection** (the step-4 integration). An intervention identity surfacing in 2+
   domains (a compound recommended as both a supplement and a peptide) and any author-declared conflict
   are surfaced in the returned report. V1 DETECTS + REPORTS; the medical-liaison contradiction
   adjudication is the deferred S74 clinical slice.
4. **Supplement↔peptide additive-AE screen** (pipeline Phase 3, the compound band, WIRED S73). Runs only
   when BOTH a supplement and a peptide candidate carry a plan. A SHARED author-declared additive-AE class
   (`ae_profile.additive_classes`) or an author-declared pairwise interaction naming the other compound
   (`ae_profile.interactions`) is an additive-AE finding — surfaced in `report["additive_ae"]` AND HOLDING
   the SUPPLEMENT (`additive-ae-held`; it finalizes last against the settled compound surface). The honest
   no-stack state, never an un-screened additive-AE combination written. Bidirectional (either author's
   declaration fires it; "component tolerability does not compose to combination safety"). The
   medical-liaison terminal gate (S74) adjudicates the held finding + the supplement↔Rx axis. Real-dispatch
   E2E (S73, PII-free synthetic operator): `compound-screen-supplement-{fishoil,creatine}-author-output`
   + `compound-screen-peptide-bpc157-author-output.example.json` (the additive fish-oil↔BPC-157 hold via a
   shared `bleeding-risk` axis, and the clean creatine↔BPC-157 pair that records both).

The reconciliation report is RETURNED (`generate_plans(...)["reconciliation"]`), never persisted — no new
store stream; plans record via the existing `record_plan` (the store-adversarial battery surface is
unchanged). Tests: `tests/plan/test_orchestrate.py` (bounce + RED-S/LEA mutation-proven RED, overlap /
conflict detection, the four-domain cross-stream + dedupe battery, the deterministic E2E render).
Real-dispatch E2E (S72, both paths, PII-free synthetic operator):
`cross-domain-{workout,nutrition}-author-output.example.json` (the no-bounce sustainable path) +
`cross-domain-bounce-{workout-initial,workout-reauthored,nutrition-author-output}.example.json` (the
real bounce: a 700-kcal cleared session → the nutritionist's real `sustains:false` (ceiling 300) →
re-author to a 260-kcal reduced session, recorded; the bounced 700-kcal load never reaches the store).

## What is deliberately NOT here yet (deferred per the build sequence)

- All four plan-domain authors are WIRED (workout S70; nutrition / supplements / peptides S71); the
  step-4 orchestrator reconciler — the nutrition→workout energy bounce + the RED-S/LEA cross-domain
  short-circuit + cross-domain overlap/conflict detection — is WIRED (S72); the supplement↔peptide
  additive-AE screen (Phase-3 compound band) is WIRED (S73, behavior 4 above).
- The **clinical-adjudication slice (S74)** — the held line's closer: the **medical-liaison terminal
  safety gate** (Phase-4 — collates the doctor-visit queue + every risk HALT, runs BPMH reconciliation,
  adjudicates the held additive-AE findings + author-declared conflicts + the supplement↔Rx axis before
  operator approval). This is the gate that turns the clinician-gated compound DRAFTS (and the held
  supplement) into operator-approvable plans. Until it lands, the reconciler's additive-AE screen HOLDS
  (the safe no-stack state) and the overlap/conflict output is DETECT+REPORT.
- The `/generate-plan` slash-command/skill wrapper (the orchestrator is wired as the `generate_plans`
  callable the interactive main agent invokes; the command surface is a later convenience).
- A standalone full-plan render screen (the dashboard plan card is Slice 1's surface; the operator is
  drafting the dedicated specialist-output screen separately).
- Real operator data: populated locally (gitignored) per ADR-0005; never committed (public repo).
