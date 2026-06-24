# ADR Discovery — Plan-Generation Engine (full-target architecture, operator-confirmed S91)

**Pipeline phase:** 1 (DISCOVERY). This list identifies and scopes the architecture decisions the
plan-generation ENGINE's full-target architecture needs ADRs for. It does NOT author them.

> **PATH NOTE (live-tree contradiction flagged per the grounding mandate):** the dispatch prompt named
> the output `docs/adr/.pipeline/discovery.md`, but that path ALREADY HOLDS the COMPLETED V1 ADR-0001..0007
> discovery list (`# ADR Discovery List — V1 Local-First Health Tracking & Planning`, Phase 8 complete per
> `.pipeline/state.md`). Overwriting it would destroy a load-bearing pipeline artifact. This engine
> discovery is therefore written to a distinct, clearly-named file in the same directory. The authoring
> phase should run the engine pipeline in its own `.pipeline/` namespace (e.g. a per-feature subdir) so it
> does not collide with the V1 ADR pipeline state.

**Provenance of the target:** operator clarification S91 (HANDOFF Top-3 #1; `vault/meta/overview.md`
S91 status; the ADR-0017-T2 re-scope). The target SUPERSEDES the S68 runtime-A "interactive
agent-dispatch session, not a standalone API client" model recorded in
`vault/design/plan-generation-pipeline-v1.md` §"Runtime model".

---

## Current engine state vs target (grounded against the live tree)

**What the engine ALREADY does in code (verified — do NOT re-decide these):**

- **The inner reconciliation+adjudication stage is fully built and wired** on synthetic data. The
  closed loop plan→act→measure→adjust runs end-to-end:
  - `scripts/plan/generate_plan.py` `compute_plan`/`generate_plan` — the single-domain production
    caller of `assemble`. **The `ModelClient` seam is ALREADY wired here** (`client=` parameter,
    `_author_callable`, `_FixedEnvelopeClient`) per ADR-0015 — `compute_plan` authors the envelope
    THROUGH `client.author(domain, summary)`, fail-closed on `ModelCallError` (`reason ==
    AUTHOR_CALL_FAILED`). The captured-envelope path is the backward-compat adapter.
  - `scripts/plan/orchestrate.py` `generate_plans`/`reconcile`/`collate_doctor_visit_queue` — the
    cross-domain reconciler (energy bounce + RED-S/LEA short-circuit + overlap/conflict +
    supplement↔peptide additive-AE + supplement↔Rx BPMH), the `adjudicator` hook, the dvq collation.
  - `scripts/plan/adjudicate.py` `adjudicate`/`audit_adjudication_envelope` — the medical-liaison
    terminal gate (INV-OVERRIDE-RECORD-SCHEMA + INV-CRITICAL-NON-OVERRIDABLE).
  - `scripts/plan/pipeline.py` `run_generation` — the GENERATE-leg production caller (the
    `/generate-plan` seam).
  - `scripts/plan/{adjust,track}.py` — the ADJUST + MEASURE legs.
  - `.claude/skills/generate-plan/SKILL.md` — the front-door dispatch lifecycle (runtime A:
    interactive agent-dispatch, full profiles inlined). `docs/plan-generation/{author,adjust}-dispatch-process.md`
    are the dispatch contracts + the reconciliation/override-record schemas.
- **The de-id IN boundary today is DETERMINISTIC, not model-backed.** `scripts/plan/router.py`
  `summarize` derives a 0-raw-PII name-addressable summary over the closed `SUMMARY_FIELD_SET`;
  `dispatch` enforces the whitelist. This is the boundary every plan author reads through.
- **The model client exists** (`scripts/model/client.py` `ModelClient`, two methods `converse` +
  `author`, injectable backend, fail-closed) — but the live `_ClaudeNoTrainBackend.author` /
  `.converse` are still `NotImplementedError` (wired at the operator checkpoint; tests inject a
  fixture backend). The conversational-intake foundation (`scripts/serve/{chat,extract,capture}.py`)
  is built + merged — the de-id token layer + the single-egress `/chat` seam.
- **The data-out boundary today is INITIALS-ONLY.** `vault/design/templates/{handout,report,
  component_set}.py` render the operator as **INITIALS only — never the full name** (ADR-0004-T1
  data-out PII rule, ADR-0009 D2). `scripts/generate/generate.py` `run` reads ONLY de-identified
  `store_read` state. **No PII re-insertion onto any rendered artifact exists in code.**

**What the operator's full target ADDS (verified ABSENT from `scripts/` — genuinely new):**

A `rg` over `scripts/` for `judge|safety.review|re.?insert|reinsert|revise.loop|subscription|
maintained|unified.format|re.?identif` finds NONE of these as plan-engine surfaces. The seven
target layers (numbered per the prompt) decompose as:

1. A **model-backed (API, no-train) de-identification BOUNDARY** that ingests raw operator PII and
   emits a de-identified summary IN, then RE-INSERTS necessary PII OUT onto the rendered artifact —
   superseding the deterministic-gate-only de-id (`router.summarize`) on the PLAN path, while the
   persisted/committed store stays de-identified.
2. A **programmatic SUBSCRIPTION-PLAN ORCHESTRATOR** that runs the plan-domain specialists as agents
   (mirroring the autonomous build pipeline) — superseding the S68 interactive-dispatch runtime.
3. A **post-assembly plan-quality JUDGE** verify step.
4. A **`/review-pr`-style MULTI-AGENT SAFETY REVIEW** of the whole assembled plan (distinct from, and
   wrapping, the existing per-finding medical-liaison adjudication + reconciliation holds).
5. A **REVISE loop** after the safety review.
6. The API agent builds the reviewed **TRACKING/TESTING artifacts** on PII re-insertion.
7. A unified **MAINTAINED output format (HTML)** the API agent adjusts as wearables/labs/new data
   arrive; the seam must not foreclose all-API or local-model substitution.

**KEY CONTRADICTION WITH THE OPERATOR'S DESCRIPTION (high-value):** the description implies the
plan-author dispatch is "still a captured agent output fed in as data" (ADR-0015 Context). That was
true at the S68 design but is **no longer true in code** — ADR-0015 was BUILT (S90): the `client=`
seam is wired into `compute_plan`/`generate_plan` and the captured-envelope path is now the
backward-compat adapter, not the production posture. The new orchestrator (decision 2) supersedes the
*runtime/control surface* (interactive session → programmatic), NOT the `ModelClient`-already-wired
author seam. Decisions 2 and 1 build ON the existing `ModelClient`, they do not introduce it.

---

## Existing ADRs touched (cross-reference table)

| Decision (working title) | ADR action | Existing ADRs touched | Nature |
|---|---|---|---|
| D-A · API de-id boundary (IN) | NEW ADR-0020 | ADR-0001, ADR-0005, ADR-0016, ADR-0006, ADR-0015, ADR-0017 | **tensions-with** ADR-0001/0005 (raw PII transits an API before de-id — crown-jewel relaxation on the PLAN path); **amends/extends** ADR-0016 carve-out (live conversation → ALSO the plan-intake raw read); **supersedes** `router.summarize` as the SOLE de-id-IN on the plan path |
| D-B · PII re-insertion boundary (OUT) | NEW ADR-0021 | ADR-0001, ADR-0004, ADR-0005, ADR-0009(D2) | **supersedes** the INITIALS-ONLY data-out posture (`handout`/`report`/`component_set`); **tensions-with** ADR-0005 (re-inserted PII must NEVER reach a committed artifact) |
| D-C · programmatic subscription orchestrator (runtime supersession) | NEW ADR-0022 | supersedes `plan-generation-pipeline-v1.md` §"Runtime model"; **relates-to** ADR-0006, ADR-0015 | supersedes S68 runtime A; wraps the existing inner engine (extend, not rebuild) |
| D-D · post-assembly plan-quality judge | NEW ADR-0023 | **relates-to** ADR-0006 (the assembled plan it judges) | new verify stage |
| D-E · multi-agent safety review of the assembled plan | NEW ADR-0024 | **relates-to** ADR-0006, ADR-0023; **distinct-from** the per-finding `adjudicate` gate (ADR-0006-stage) | new whole-plan review tier |
| D-F · post-review REVISE loop | candidate fold into ADR-0024 [UNCERTAIN] | ADR-0023, ADR-0024 | the closed control loop the judge/review tiers gate |
| D-G · unified maintained HTML output format | NEW ADR-0025 | **amends** ADR-0004 (single-file on-demand → maintained/re-emitted) | new output lifecycle |
| D-H · substitutability seam (all-API / local-model / combo) | candidate fold into ADR-0022 [UNCERTAIN] | ADR-0015 (the swap seam), ADR-0001 (North-Star local model) | cross-cutting seam constraint |

ADR numbering starts at **0020** (existing set is ADR-0001..0019). Firm new ADRs: 0020 (de-id IN),
0021 (re-insert OUT), 0022 (orchestrator/runtime-supersession), 0023 (judge), 0024 (safety-review),
0025 (maintained-HTML) = **6 firm**, + 2 fold-candidates (D-F revise, D-H seam).

---

## The decisions

### 1. Adopt a model-backed API de-identification boundary for raw plan-intake PII (de-id IN) — ADR-0020 [LOAD-BEARING]

- **Why this is an architecture decision:** it relaxes the system's crown-jewel invariant — it routes
  RAW operator PII across a (no-train) API boundary BEFORE de-identification on the PLAN path,
  superseding the deterministic, in-process, 0-raw-PII `router.summarize` gate as the sole de-id-IN.
  It constrains every downstream plan dispatch, has real fail-closed-vs-fail-open trade-offs, and a
  reviewer WILL question it. This is THE load-bearing decision.
- **Suspected dependencies:** is the upstream of D-C (the orchestrator runs specialists over whatever
  this boundary emits) and D-B (the OUT side re-inserts what this side stripped). Depends on the
  `ModelClient` seam (ADR-0015, built).
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0020**, and it **amends/extends ADR-0016** rather than
  superseding it cleanly. ADR-0016 already opened a SCOPED raw-egress carve-out — "the LIVE intake
  conversation may egress raw over the no-train lane while every persisted fact stays de-identified."
  This decision EXTENDS that carve-out to a SECOND raw-egress class: the model-backed de-id of raw
  plan-intake state. Per ADR-0016's own review trigger — "Any proposal to add a second raw-egress
  class (beyond the live conversation) — re-open this decision against the conversation-only bound" —
  this re-opening is mandatory, not optional. The deterministic `summarize` is NOT deleted (the
  persisted/committed store stays de-identified; the boundary's OUTPUT still feeds the de-identified
  store), but it is no longer the SOLE de-id-IN on the plan path.
- **GROUNDING NOTE:** the current de-id-IN is `scripts/plan/router.py:summarize` (0-raw-PII,
  `SUMMARY_FIELD_SET` whitelist, the `dispatch` gate) + the 8j6 `pii_scan` backstop; the model seam
  it would run through is `scripts/model/client.py:ModelClient.author` (live backend still
  `NotImplementedError`). ADR-0016 §Decision + §"Review triggers" (the second-raw-egress-class
  trigger) and ADR-0001 §Falsification ("≥1 plan-reasoning dispatch sending raw (non-summary) PII to
  the model means the summaries-not-raw discipline failed") are the invariants this tensions-with.
- **The PII tension (captured explicitly per the mandate):** ADR-0001's anchor is "Only plan reasoning
  touches the model, OVER SUMMARIES rather than raw PII" and its falsification names raw (non-summary)
  PII to the model as a boundary breach. ADR-0005 keeps PII out of committed history. This decision
  routes raw PII to an API BEFORE de-id — exactly the surface ADR-0001's summaries-not-raw discipline
  forbade — accepting bounded no-train retention on raw plan PII (the same exposure ADR-0016 accepted
  for the live conversation, now extended). It MUST be fail-closed: a failed/partial de-id call yields
  the honest no-plan state (mirroring `compute_plan`'s `AUTHOR_CALL_FAILED`), never a raw-PII leak
  downstream and never a fabricated summary.
- **Genuine viable approaches (the real ADR trade-off):**
  (a) **API-model de-id IN** (operator's stated target) — full model de-id of raw state; richest, but
      raw PII transits the API.
  (b) **Keep the deterministic `summarize` gate for de-id-IN; add the model only for the OUT
      re-insertion** (D-B) — preserves the 0-raw-PII-IN invariant entirely, accepts that the IN side
      stays as lossy as today's closed field-set.
  (c) **Hybrid** — deterministic gate strips named-excluded raw PII first, the model de-id's only the
      residual free-text the field-set can't structure (narrows what raw text the API sees).
  These are materially different privacy/capability postures and are the substance of the ADR.

### 2. Adopt the programmatic subscription-plan orchestrator (supersede runtime A) — ADR-0022

- **Why this is an architecture decision:** it changes the engine's RUNTIME/control surface from an
  interactive Claude-Code agent-dispatch session (S68 runtime A) to a programmatic orchestrator that
  runs the plan-domain specialists as agents autonomously (mirroring the build pipeline). It fixes how
  every plan is produced and is the layer the new judge/review/revise tiers attach to.
- **Suspected dependencies:** consumes D-A's de-id-IN output; is wrapped by D-D (judge) + D-E (safety
  review) + D-F (revise); is the producer D-B re-inserts onto. WRAPS the existing
  `orchestrate.generate_plans` / `pipeline.run_generation` inner engine (extend, not rebuild).
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0022 that SUPERSEDES the runtime-A section of
  `vault/design/plan-generation-pipeline-v1.md`** (§"Runtime model" + §"The five decisions" item that
  pins "interactive … not a standalone API client"). This is the clean answer to the prompt's key
  question: it is NOT an update to an existing ADR-0001..0019 (the runtime-A decision lives in the
  vault DESIGN DOC, not an ADR), and it is NOT a wholesale rebuild — it **relates-to ADR-0006** (the
  roster-assembly architecture it drives, unchanged) and **relates-to ADR-0015** (the `ModelClient`
  it dispatches through, already wired). The design doc's runtime-model section gets a
  `superseded_by` pointer to ADR-0022; the tier model + DAG + the inner reconciler survive.
- **GROUNDING NOTE:** `plan-generation-pipeline-v1.md` §"Runtime model (operator decision, S68)"
  states "Plan generation runs as an interactive Claude-Code / agent-dispatch session, not a
  standalone API client … A standalone `scripts/` API client is a later North-Star option the seam
  must not foreclose." `.claude/skills/generate-plan/SKILL.md` §"What is deliberately NOT here"
  reaffirms "A non-interactive auto-dispatch CLI … the skill is agent-in-the-loop by design." The
  inner engine the new orchestrator wraps: `scripts/plan/pipeline.py:run_generation` →
  `orchestrate.generate_plans` (with the `reauthor`/`adjudicator` hooks).
- **Genuine viable approaches (flagged):** (a) orchestrator as a programmatic *subscription* Claude-Code
  session that drives the agents (the operator's "subscription orchestrator … like the autonomous
  build pipeline"); (b) orchestrator as a standalone `scripts/` no-train **API** client. The S68
  design explicitly held (b) as a deferred North-Star option whose seam must not be foreclosed; the
  operator's "at some later date it can all be API or a local model or some combo" (decision 7 /
  D-H) means the ADR must pick the V1 runtime WITHOUT foreclosing the other. Real trade-off.

### 3. Adopt a model-backed PII re-insertion boundary for rendered artifacts (de-id OUT) — ADR-0021 [LOAD-BEARING]

- **Why this is an architecture decision:** it introduces a NEW data-out surface that re-inserts the
  operator's real PII onto the rendered (HTML) artifact, superseding the standing INITIALS-ONLY data-
  out posture. It is the OUT half of the crown-jewel relaxation and constrains every renderer + the
  commit/push PII hooks. A reviewer will question whether re-inserted PII can leak to a committed file.
- **Suspected dependencies:** the inverse of D-A (re-inserts what D-A stripped — the two define the
  IN/OUT PII envelope together); consumes the reviewed plan from D-C/D-E; feeds D-F's tracking/testing
  artifacts (decision 6) and D-G's maintained HTML (decision 7).
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0021**, and it **supersedes the data-out portion of
  ADR-0004 / ADR-0009-D2's initials-only rule** and **tensions-with ADR-0005**. Today
  `vault/design/templates/{handout,report,component_set}.py` render the operator as "INITIALS only —
  never the full name" and `generate.run` reads only de-identified `store_read`. Re-inserting PII OUT
  is a real reversal of that posture FOR THE LOCAL/UNCOMMITTED artifact. The non-negotiable bound: the
  re-inserted-PII artifact is a local, gitignored output (ADR-0005 `vault/scaffold/filled/` /
  artifacts surface) the `block-pii-commit`/`pre-push-pii-scan` hooks must continue to deny on commit.
- **GROUNDING NOTE:** `vault/design/templates/handout.py:1-30` ("the operator renders as INITIALS only
  — never the full name … a public-repo health-tool" rule, `component_set.py:709-767`
  `read_profile`); `scripts/generate/generate.py:run` (reads only `store.read_all(root)`, no
  identity source). ADR-0005 §Falsification ("≥1 operator-PII value in a tracked file … release-
  blocking") is the invariant this tensions-with.
- **Genuine viable approaches (flagged):** (a) the API/model agent re-inserts PII at render time
  (operator target); (b) a deterministic local re-insertion pass (read the gitignored identity config,
  template-substitute — no model needed for OUT, mirroring how `component_set.read_profile` already
  reads initials from a gitignored source). (b) keeps the model off the OUT path entirely and is a
  materially simpler privacy story; whether the OUT side NEEDS a model is itself the decision.

### 4. Adopt a post-assembly plan-quality judge — ADR-0023

- **Why this is an architecture decision:** it adds a verify GATE between assembly and the operator
  (mirroring the build pipeline's judge), with pass/revise authority over the assembled plan. It fixes
  a quality bar and a control-flow gate the orchestrator must honor; it is distinct from the existing
  per-finding safety adjudication.
- **Suspected dependencies:** wraps D-C's assembled output; gates into D-F (revise). Distinct from the
  D-E safety review (quality vs safety) — their ordering/relationship is part of this + ADR-0024.
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0023**, **relates-to ADR-0006** (it judges the
  ADR-0006 assembled plan). No existing ADR defines a plan-quality judge.
- **GROUNDING NOTE:** no judge exists in `scripts/plan/` (verified by `rg`). The nearest prior art is
  the `aplus-research` paired-judge gates (`.claude/skills/aplus-research/`) and the build pipeline's
  judge (`/execute-plan`, `rubric`) — references for the SHAPE, not existing plan-engine code.
- **[UNCERTAIN] scope boundary:** whether "judge" (quality) and "safety review" (D-E) are ONE
  combined review tier or TWO distinct gates is a genuine open question — the operator listed them
  separately ("a judge verify" THEN "a /review-pr-style safety review"), which argues for two ADRs,
  but a reviewer could argue they fold into one multi-dimension review. Listed as two; the boundary
  itself is a sub-decision the author must resolve (and may collapse).

### 5. Adopt a multi-agent safety review of the assembled plan — ADR-0024

- **Why this is an architecture decision:** it applies the `/review-pr` blind-triage/verified-fix
  PATTERN to the whole assembled plan — a NEW whole-plan review tier that WRAPS (does not replace) the
  existing per-finding medical-liaison adjudication + the reconciliation holds. It fixes a review
  topology (how many lenses, blind triage, the release gate) and has real "is this redundant with the
  inner gates?" trade-offs a reviewer will press.
- **Suspected dependencies:** wraps D-C's output; coordinates with D-D (judge); gates into D-F
  (revise). Explicitly **distinct-from** the `adjudicate` per-finding gate (ADR-0006-stage) — the ADR
  must state how the whole-plan review and the per-finding adjudication compose without double-gating
  or gap.
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0024**, **relates-to ADR-0006** and **distinct-from**
  the existing `scripts/plan/adjudicate.py` medical-liaison terminal gate. The inner engine already
  has a per-FINDING safety gate (the additive-AE / conflict / Rx-BPMH adjudication, INV-OVERRIDE-
  RECORD-SCHEMA / INV-CRITICAL-NON-OVERRIDABLE); this is a whole-PLAN review tier on top.
- **GROUNDING NOTE:** `scripts/plan/adjudicate.py` (the per-finding gate that exists); the `/review-pr`
  skill (`review-pr`) is the PATTERN reference, not plan-engine code. The medical-liaison +
  health-safety-reviewer / medical-safety-reviewer roles in `.claude/agents/` are the candidate
  review lenses.

### 6. Adopt a post-review revise loop — fold-candidate into ADR-0024 (or NEW ADR) [UNCERTAIN]

- **Why this is (or is not) an architecture decision:** a bounded revise loop after the judge/safety
  review is the closed control loop that makes the judge/review gates meaningful (a gate with no
  revise path is just a halt). Whether it is ADR-WORTHY on its own or is the natural CONSEQUENCE of
  decisions D-D/D-E is the open question.
- **Suspected dependencies:** gated by D-D + D-E; re-invokes D-C.
- **NEW ADR vs EXISTING-ADR-UPDATE:** **[UNCERTAIN] — most likely a CONSEQUENCE/mechanism folded into
  ADR-0023 + ADR-0024**, not a standalone ADR, UNLESS the revise loop carries its own genuine
  trade-off (bounded iteration count, who authors the revision — the same specialist vs a fresh
  dispatch, the halt-on-non-convergence policy). The `rubric` skill's "bounded revise loop" is the
  prior-art shape. Flagged INCLUDE so the author consciously decides fold-vs-split rather than
  dropping it.
- **GROUNDING NOTE:** the `rubric`/`/execute-plan` bounded-revise pattern is the reference; no
  revise loop exists in `scripts/plan/`.

### 7. Adopt a unified maintained HTML output format — ADR-0025

- **Why this is an architecture decision:** it changes the artifact LIFECYCLE from ADR-0004's
  on-demand, single-file, render-to-completion-and-exit model to a unified, MAINTAINED format the API
  agent re-adjusts as wearables/labs/new data arrive. It fixes the output contract + the update
  mechanism and amends an accepted ADR. (Decision 6 of the prompt — the API agent building the
  reviewed tracking/testing artifacts on PII re-insertion — is a SUB-SURFACE of this maintained
  format, not a separate ADR: the tracking/testing artifacts are outputs of the same maintained
  render lifecycle, fed by D-B's re-inserted PII.)
- **Suspected dependencies:** consumes D-C/D-E (the reviewed plan) + D-B (PII re-insertion).
- **NEW ADR vs EXISTING-ADR-UPDATE:** **NEW ADR-0025 that AMENDS ADR-0004** (on-demand single-file
  artifact generation). ADR-0004 today is "the SAME code path serves interactive + cron; run-to-
  completion-and-exit; one `render.emit`." A "maintained" format that the agent ADJUSTS over time as
  new data lands is a new lifecycle on top of (not a replacement of) the single-file render.
- **GROUNDING NOTE:** `scripts/generate/generate.py:run` ("THIN entry point … drives ONE `render.emit`
  … run-to-completion-and-exit") + `_TEMPLATES` (dashboard/handout/intake/report — the existing
  single-file artifacts). ADR-0004 is the on-demand-single-file decision this amends.
- **[UNCERTAIN]:** whether "unified maintained HTML" is one architecture decision or partly an
  implementation detail (HTML-specifically, the template structure) — the ADR-WORTHY core is the
  MAINTAINED/re-emit-on-new-data LIFECYCLE; the specific markup is impl. Author should scope to the
  lifecycle, not the format details (ADR decision-tree: exclude impl detail).

### 8. Preserve the all-API / local-model / combo substitution seam — fold-candidate into ADR-0022 [UNCERTAIN]

- **Why this is (or is not) an architecture decision:** the operator's "at some later date it can all
  be API or a local model or some combo — the seam must NOT foreclose all-API or local-model
  substitution" is a cross-cutting CONSTRAINT on D-A (de-id), D-C (orchestrator), and D-G (output). It
  is the same swappability property ADR-0015 fixed for the model client, now extended to the engine's
  runtime + de-id + output surfaces.
- **Suspected dependencies:** constrains D-A, D-C, D-G; extends ADR-0015's swap seam.
- **NEW ADR vs EXISTING-ADR-UPDATE:** **[UNCERTAIN] — most likely a cross-cutting CONSTRAINT recorded
  as a Consequence/seam-falsification IN ADR-0022** (the runtime ADR is where "which runtime, without
  foreclosing the others" lives) rather than a standalone ADR. ADR-0015 already carries the
  "swap-seam-must-be-kept-honest-or-it-ossifies" falsification; this extends that discipline to the
  engine. Flagged INCLUDE so it is not lost — it is the constraint that keeps the North-Star
  local-model path (ADR-0001 Alternative C) reachable.
- **GROUNDING NOTE:** ADR-0015 §Decision (swappable at the seam) + §Falsification ("if swapping the
  provider requires editing more than 1 file outside the client … the seam has ossified"); ADR-0001
  Alternative C (the deferred local model). The `ModelClient` injectable backend
  (`scripts/model/client.py`) is the existing seam this generalizes.

---

## Excluded as implementation detail / already-decided (not ADR-worthy)

- **The author dispatch contract / per-domain payload shapes / override-record schema** — already
  fixed in `docs/plan-generation/author-dispatch-process.md` + `scripts/plan/adjudicate.py`; impl, not
  a new architecture trade-off.
- **The `ModelClient` introduction + swappability + fail-closed posture** — already ADR-0015 (BUILT).
  The engine ADRs CONSUME it; they do not re-decide it.
- **The reconciler's five cross-domain behaviors** (energy bounce / RED-S-LEA / overlap-conflict /
  additive-AE / Rx-BPMH) — built + ADR-0006-stage; the new safety review WRAPS them, does not redraw
  them.
- **The de-id token VOCABULARY** (`SUMMARY_FIELD_SET` membership) — governed by ADR-0019 +
  router.py change-control tripwires; an engine decision may consume new tokens but the vocabulary
  mechanism is settled.
- **Retry/backoff mechanics of the model calls** — ADR-0015 OQ-3 spec-stage concern; impl.

---

## Notes for the DAG / authoring phase

- **The PII envelope (D-A + D-B) is the spine.** D-A (de-id IN) and D-B (re-insert OUT) together
  redraw the crown-jewel boundary for the plan path; they are the two highest-risk ADRs and should be
  authored as a pair (the IN/OUT symmetry — what D-A strips, D-B restores — is load-bearing, and the
  persisted/committed store staying de-identified is the invariant BOTH must honor).
- **Extend-not-rebuild is a hard grounding fact.** Every "new" engine layer (D-C..D-G) WRAPS the
  built inner engine (`generate_plans` / `run_generation` / `adjudicate` / `assemble` / the closed
  loop). The ADRs must state this explicitly so the build phase does not re-author the reconciler.
- **The ADR-0015 already-wired finding** (the `client=` seam is in production code, not "still
  captured-data") corrects the operator's description and should be stated in D-C's Context so the
  author does not re-decide the model-client introduction (already ADR-0015, built).
- **Suggested DAG order** (topological, by dependency): D-A → D-C → {D-D ∥ D-E} → D-F → {D-B → D-G},
  with D-H as a cross-cutting constraint on D-A/D-C/D-G. Final ordering is Phase-2's job; this is the
  discovery-stage hypothesis.
- **The runtime supersession (D-C/ADR-0022) is the clean answer to the prompt's key question:** a NEW
  ADR superseding the design doc's runtime-A section + relating to ADR-0006/0015, NOT an update to an
  existing ADR-0001..0019.
