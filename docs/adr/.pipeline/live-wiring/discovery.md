# ADR Discovery — Plan-Generation Engine LIVE-WIRING (S93)

**Pipeline phase:** 1 (DISCOVERY). This list identifies and scopes the architecture decisions the
plan-generation engine's **live-wiring** needs ADRs for — connecting the S92-built (mock/fixture-
tested, 0 live spend) engine to REAL clients so the only remaining step is the operator-present LIVE
test (S94). It does NOT author the ADRs. Numbering continues from the engine set (ADR-0001..0025) at
**ADR-0026**.

> **PATH NOTE:** written to a per-feature subdir (`.pipeline/live-wiring/`) so it does not collide
> with the V1 (`.pipeline/`) or engine (`.pipeline/engine/`) pipeline state — the namespace
> discipline the engine discovery flagged (PF/`/run-pipeline` rough edge, S92).

---

## What the engine ALREADY is (verified against the live tree — do NOT re-decide)

The S92 build landed every engine PIECE; the gap is that the pieces have **no production caller**
that composes them over real clients. Verified by `rg` over `scripts/`:

- **`run_orchestrated`** (`scripts/plan/plan_orchestrator.py:136`) — the programmatic runtime
  surface. Signature `run_orchestrated(raw_intake, deid_client, dispatch, store_read, root, *,
  plan_date, domains, on_date, gates, gate_dispatch, reauthor, adjudicator, dispatch_cap,
  revise_cap)`. It (1) calls `deid_in(raw_intake, deid_client)`; (2) halts to honest-no-plan on the
  de-id sentinel; (3) for each domain builds a full-profile-inlined prompt and issues it through the
  injected **`dispatch(domain, prompt, summary) -> author envelope`** seam; (4) drives
  `pipeline.run_generation`; and, when a real **`gate_dispatch`** is injected, runs the bounded
  revise loop with scratch-and-promote. **NO production caller** — `rg run_orchestrated` finds only
  its own definition + docstrings ([plan_orchestrator.py:136-305] [VERIFIED]).
- The **`dispatch` seam is SYNCHRONOUS and Python-shaped** — `authors[domain] = dispatch(domain,
  prompt, summary)` ([plan_orchestrator.py:369] [VERIFIED]). It expects a structured envelope back
  in the call stack. This is the keystone tension: a subscription specialist is a Claude Code AGENT,
  and Python cannot synchronously `Task`-dispatch a subscription agent and get its output back.
- The **`gate_dispatch` seam** — `gate_dispatch(result) -> disposition`, where the loop reads
  `disposition.get("safety_passed") is True` (the only surface path), then `disposition.get("accept")`
  / `disposition.get("revise_domains")` ([plan_orchestrator.py:261-294] [VERIFIED]). Default `None`
  → a no-op (the legacy non-loop path).
- The **gate callables exist but are NOT composed**: `quality_judge(plan, judge_client) ->
  {"verdict": ACCEPT|REVISE, "dimensions", "deductions"}` ([quality_judge.py:206-253] [VERIFIED]);
  `review_plan(assembled_plan, dispatch, *, lenses) -> {"findings", "passed", "lenses"}`
  ([safety_review.py:110-169] [VERIFIED]). Both modules' headers explicitly say **ADR-0022-T2 owns
  adapting each native verdict to the loop's common disposition** — and `rg` confirms **no composer
  exists** in `scripts/` (no caller of `quality_judge(`/`review_plan(` outside their own defs)
  ([VERIFIED]).
- **`deid_in(raw_intake, client)`** routes through `client.deidentify` ([deid_in.py:30-73]
  [VERIFIED]); the live backend **`_ClaudeNoTrainBackend.deidentify` is a `NotImplementedError`
  stub** ("live deidentify is wired at the Wave-B operator checkpoint") ([client.py:156-160]
  [VERIFIED]). The only `ModelClient()` constructions in `scripts/` are the intake server
  ([server.py:225]) and a TEST fixture ([generate_plan.py:521]) — **no plan-generation front door
  constructs a live de-id client** ([VERIFIED]).
- **`reinsert_out`** (de-id OUT, deterministic, model-free) and **`reemit_maintained`** (the
  maintained render that runs `reinsert_out` as its final pass) are built ([reinsert_out.py],
  [maintained.py:245-326] [VERIFIED]). De-id OUT stays deterministic — **not in scope as an ADR**
  (already decided, ADR-0021).
- **`core-capability-audit.sh`** pins `CALLER=scripts/plan/generate_plan.py`, greps for `assemble(`
  + `record_plan(`, and runs `generate_plan --self-test` ([core-capability-audit.sh:47-72]
  [VERIFIED]). It does NOT exercise the engine path (`run_orchestrated`).

**The runtime split (operator decision, S93 — captured, NOT re-litigated):** PII-related work →
the **no-train API** (the de-id-IN boundary, the one model call ingesting raw operator PII);
everything else (plan-domain specialists, quality judge, safety-review lenses, orchestrator control
flow) → **subscription** Claude Code agents (like the autonomous build pipeline); de-id OUT stays
**deterministic** (already built); the seam must not foreclose an all-API or local-model swap later.

---

## The decisions

### 1. Select the V1 subscription-runtime driver model (the keystone) — ADR-0026 [LOAD-BEARING]

- **Decision title:** Select the V1 subscription-runtime driver model for the programmatic
  orchestrator (skill-as-orchestrator vs Python-driven adapter vs hybrid).
- **Why it is an architecture decision (not implementation):** it resolves a genuine structural
  impossibility with lasting consequences and real, materially-different alternatives. `run_orchestrated`
  is Python and its `dispatch(domain, prompt, summary)` seam expects a structured specialist envelope
  back **synchronously** ([plan_orchestrator.py:369] [VERIFIED]); a subscription specialist is a
  Claude Code Task AGENT, and Python cannot synchronously dispatch a subscription Task agent and pull
  its output back into the call stack. HOW the programmatic orchestrator drives subscription
  specialist/gate dispatch fixes where the live runtime lives, which half is Python and which half is
  agent-driven, and what a future all-API/local-model cutover must re-validate. ADR-0022 explicitly
  deferred exactly this (its OQ-1 "how does the autonomous orchestrator spawn the plan-domain
  specialist agents", OQ-3 "where does the orchestrator's drive layer live — a new `scripts/plan/`
  driver vs the skill harness") to build-planning ([ADR-0022, OQ-1, OQ-3] [VERIFIED]). It is NOT an
  implementation detail (it is not reversible without cross-component impact — it re-shapes the
  production entry point and the substitution seam) and NOT externally imposed (three real options).
- **The three candidate models (the substance of the ADR):**
  - **(A) SKILL-AS-ORCHESTRATOR** — a `/generate-plan` skill IS the live runtime: the session
    de-ids via the API client (a Python call), dispatches each specialist + gate lens as subscription
    Task agents, collects their envelopes, and feeds them to the engine's DETERMINISTIC Python
    substrate. `run_orchestrated`'s Python loop becomes the API-mode driver + control-flow SPEC +
    test harness; the skill replicates the control flow at the agent-dispatch level.
  - **(B) PYTHON-DRIVEN dispatch adapter** — `dispatch` wired to a Python adapter that
    programmatically invokes a subscription agent (Agent SDK = metered/API-ish, conflicts with
    "subscription"; headless `claude` CLI subprocess = subscription but complex/fragile).
  - **(C) HYBRID** — deterministic substrate stays Python (`run_orchestrated`); agent REASONING is
    dispatched by the skill and fed in. The ADR must resolve which half is which.
- **Suspected dependencies:**
  - On existing ADRs: **amends/extends ADR-0022** — ADR-0022 decided the runtime is "a programmatic
    subscription orchestrator … mirroring the autonomous build pipeline" but explicitly left the
    DRIVE MECHANISM as OQ-1/OQ-3 for build-planning to resolve ([ADR-0022, OQ-1/OQ-3] [VERIFIED]).
    This ADR-0026 RESOLVES those OQs. **relates ADR-0015** (the substitution seam it must not
    foreclose) and **relates ADR-0006** (the roster-assembly architecture it drives, unchanged).
  - On the other live-wiring decisions: it is the parent of #3 (the composed `gate_dispatch` adapter
    is the gate-side of whichever driver model wins) and #5 (the subscription specialist/safety-lens
    dispatch wiring is the specialist-side of the same model). #2 (the live de-id API backend) is the
    PII-side counterpart it dispatches over.
- **NEW vs UPDATE:** **NEW ADR-0026** that **amends/extends ADR-0022** (resolves its OQ-1/OQ-3) and
  carries the D-H model-substitution-seam constraint forward to the DRIVE layer. ADR-0022 already
  decided "subscription, mirroring the build pipeline"; this ADR does NOT reverse that — it picks the
  concrete DRIVER among A/B/C. Distinct from "ADR-0022 needs a revision-history note": ADR-0026 is a
  standalone decision with its own alternatives + trade-offs (the A/B/C selection ADR-0022 never
  made), and ADR-0022 receives an inverse Related-Decisions row + a revision-history note pointing at
  it.

### 2. Wire the live no-train API de-identification backend — ADR-0027 [LOAD-BEARING]

- **Decision title:** Wire the live no-train API de-identification backend
  (`_ClaudeNoTrainBackend.deidentify`).
- **Why it is an architecture decision (not implementation):** this is the ONE model call that
  ingests RAW operator PII — the de-id-IN crown-jewel boundary going from a `NotImplementedError`
  stub to a real no-train API call. The decisions it fixes are structural and lasting: the no-train
  model id + profile (the contractual training-exemption posture ADR-0001 rests on), the prompt →
  `SUMMARY_FIELD_SET`-shaped-summary CONTRACT (the de-id-IN output the whole pipeline consumes), and
  the fail-closed-to-`ModelCallError` behavior on any failure (the boundary that must never leak raw
  PII or fabricate a summary). A reviewer WILL question whether the live backend honors the
  fail-closed + whitelist contract ADR-0020 demands ([ADR-0020, Falsification "raw-PII-leak probe"]
  [VERIFIED]). The RETRY/BACKOFF mechanics are impl (ADR-0015 OQ-3); the model-id + no-train-profile
  + summary-contract + fail-closed POSTURE are the decision.
- **Suspected dependencies:**
  - On existing ADRs: **implements ADR-0020** (the model-backed de-id-IN boundary decision) — this
    is the LIVE wiring of the seam ADR-0020 decided; **depends-on ADR-0015** (it fills the swappable
    `ModelClient` backend's `deidentify` method, the seam ADR-0015-amended for ADR-0020); honors
    **ADR-0001/0016/0005** (no-train lane only; the second raw-egress class; raw residue never
    committed).
  - On the other live-wiring decisions: #1 dispatches the specialists over the de-identified summary
    THIS backend emits (the same input-contract dependency as ADR-0022 depends-on ADR-0020). It is
    the PII-API counterpart to the subscription-side #1/#3/#5.
- **NEW vs UPDATE — and the fold question:** **[UNCERTAIN] whether a DISTINCT ADR or folded into the
  runtime split (#1/ADR-0026).** Argument to FOLD: the S93 operator decision is ONE split ("PII →
  API, everything else → subscription"); the live de-id backend is the API half of that single
  runtime split, and #1 is the subscription half — one ADR could carry the whole split. Argument to
  SPLIT (lean): ADR-0020 already DECIDED the model-backed de-id-IN architecture; wiring the live
  backend is the narrow act of making `_ClaudeNoTrainBackend.deidentify` real, with its OWN trade-off
  surface (model-id selection, the summary contract, the fail-closed test) DISTINCT from the
  subscription-driver A/B/C question #1 resolves — bundling them risks AP-08 (Mega-ADR) since they
  are two decisions (the PII-API boundary's live shape vs the subscription driver model). **Lean:
  DISTINCT ADR-0027 that implements ADR-0020**, with #1/ADR-0026 carrying the runtime SPLIT framing
  and #2/ADR-0027 carrying the live de-id-backend specifics. The author should consciously decide
  fold-vs-split (the discovery gate), not default. If the live backend is judged to add no NEW
  architecture trade-off beyond ADR-0020's already-settled decision (it is "just implementation of an
  already-decided boundary"), it collapses to a build TASK under ADR-0020 with no new ADR — flagged
  so it is not lost.

### 3. Build the composed `gate_dispatch` adapter — folds into ADR-0026 [UNCERTAIN]

- **Decision title:** Compose the quality-judge + safety-review gates into the orchestrator's
  `gate_dispatch(assembled_result) -> {accept, safety_passed, revise_domains}` adapter.
- **Why it is (or is not) an architecture decision:** the composition is genuinely UNBUILT and
  load-bearing — `quality_judge` emits `{verdict: ACCEPT|REVISE}` and `review_plan` emits
  `{passed: bool, findings}`, and the loop reads a SINGLE `{safety_passed, accept, revise_domains}`
  disposition; both modules' headers explicitly defer "adapting each verdict to the revise-loop's
  common disposition" to ADR-0022-T2 ([quality_judge.py:28], [safety_review.py:32] [VERIFIED]). The
  ADR-WORTHY core is the **shared-loop composition topology** ADR-0022 named as its #1 build-blocking
  control-flow question — the SHARED OQ-2 (one combined gate vs two; ordering; the re-trigger rule;
  how a REVISE verdict maps to `revise_domains`; how `safety_passed` is derived from `passed`)
  ([ADR-0022 closing §, "the revise-loop composition topology … is the #1 build-blocking control-flow
  decision … carried as the SHARED OQ-2"] [VERIFIED]). That topology IS an architecture decision (it
  fixes the safety/quality gate ordering + the fail-closed mapping). The ADAPTER CODE that mechanically
  joins the two native shapes, given a resolved topology, is implementation.
- **Suspected dependencies:** depends-on #1/ADR-0026 (the adapter is the gate-side of whichever driver
  model wins — under (A) the skill composes the lens envelopes; under (B) a Python composer does);
  consumes the two built gate callables (`quality_judge`/`review_plan`); is the resolution of
  ADR-0022/0023/0024's shared OQ-2.
- **NEW vs UPDATE:** **[UNCERTAIN] — most likely FOLDS into #1/ADR-0026 (the runtime-driver ADR owns
  the control flow, per ADR-0022's "This ADR owns the orchestrator control flow")**, recorded as the
  resolution of ADR-0022's SHARED OQ-2 rather than a standalone ADR — UNLESS the composition carries
  its own genuine trade-off worth a separate record (quality-before-safety vs safety-before-quality
  ordering; whether a safety BLOCK short-circuits the quality verdict; the joint iteration cap). Who
  BUILDS/OWNS it is the driver model's owner (the skill under A, a Python composer under B/C). Flagged
  INCLUDE so the author decides fold-vs-split consciously. If split, it is **NEW ADR-0028** resolving
  the OQ-2 topology; if folded, ADR-0026 carries it.

### 4. Repoint the core-capability audit to the engine path — NOT an ADR (mechanical task)

- **Decision title:** Repoint `core-capability-audit.sh` from `generate_plan.py` to the live-wired
  engine front door.
- **Why it is NOT an architecture decision:** it is a MECHANICAL consequence of the front door
  landing, not a structural choice with alternatives. The audit pins
  `CALLER=scripts/plan/generate_plan.py` and asserts the wired path (`assemble` → `record_plan` →
  render); once the live front door composes de-id → subscription dispatch → `run_orchestrated` →
  `reinsert_out` → maintained render, the audit's `CALLER` pin + its grep/self-test targets move to
  that path so INV-CORE-CAPABILITY guards the REAL core capability (the PF-S63-02 close the project
  CLAUDE.md says "lands WITH the `71s4` build"). There is no trade-off to record — the only question
  is which file/function the pin names, an implementation detail the front-door build owns. The
  CLAUDE.md core-capability gate already says "The MECHANICAL form of this gate … lands WITH the
  `71s4` build, since its checks depend on the path's shape" ([CLAUDE.md, PF-S63-02 §] [VERIFIED]).
- **Disposition:** RIDES the front-door build (a build task under #1/ADR-0026's acceptance criteria,
  per "DAG + Validation criteria → acceptance criteria"), recorded as a Validation-Approach
  confirmation criterion of ADR-0026 (the audit asserts the engine path is wired), NOT a new ADR.
  Excluded per the ADR decision-tree ("Implementation details reversible without cross-team impact").

### 5. Wire the subscription specialist + safety-lens dispatch — part of ADR-0026 [UNCERTAIN]

- **Decision title:** Wire the subscription specialist + safety-lens dispatch (runtime-A's "the
  reasoning is the specialists'/lenses'" agent-dispatch piece).
- **Why it is (or is not) an architecture decision:** the "the reasoning is the specialists'" piece —
  how the orchestrator spawns each plan-domain specialist (full profile inlined per INV-ROLE-INLINING)
  and each safety lens as a SUBSCRIPTION agent and captures its envelope back — is exactly ADR-0022's
  OQ-1 ("how does the autonomous orchestrator spawn the plan-domain specialist agents with their full
  role profiles inlined") ([ADR-0022, OQ-1] [VERIFIED]). But this is the SAME structural question #1
  answers: under driver-model (A) the skill spawns the agents; under (B) a Python adapter does; under
  (C) the skill spawns reasoning agents and feeds them in. The specialist-dispatch wiring is NOT a
  decision SEPARATE from the driver model — it IS the specialist-side instance of the driver model #1
  selects. The role-inlining CONSTRAINT (full profile verbatim) is non-negotiable and already fixed
  (INV-ROLE-INLINING + the `enforce-role-inlining` hook); only the MECHANISM is open, and the
  mechanism is what #1 decides.
- **Suspected dependencies:** is the specialist-side of #1/ADR-0026 (and the lens-side feeds #3's
  composed gate); over the de-identified summary #2/ADR-0027 emits; honors INV-ROLE-INLINING.
- **NEW vs UPDATE:** **[UNCERTAIN] — NOT a distinct ADR; PART of #1/ADR-0026.** The specialist +
  safety-lens dispatch wiring is the concrete realization of the driver model ADR-0026 selects (it
  resolves ADR-0022's OQ-1 as ADR-0026 resolves OQ-3 — the same drive layer). Recording it as a
  separate ADR would split one runtime-driver decision across two records (AP-08 risk in reverse —
  fragmenting one decision). Flagged INCLUDE so the author confirms it is absorbed into ADR-0026's
  Decision/Consequences (the drive layer dispatches BOTH specialists and gate lenses through the same
  mechanism), not dropped.

---

## Decisions considered and EXCLUDED (with reason)

- **The de-id OUT re-insertion (`reinsert_out`) staying deterministic** — already decided (ADR-0021,
  built, model-free). The operator decision reaffirms "de-id OUT stays deterministic (no model)";
  there is no new trade-off. NOT an ADR.
- **The `dispatch`/`gate_dispatch`/`reauthor`/`adjudicator` SEAM SHAPES** — already built + frozen in
  `run_orchestrated` (S92, ADR-0022-T1..T3). The live-wiring CONSUMES these seams; it does not
  re-decide them. Implementation, not a new architecture decision.
- **The retry/backoff/timeout mechanics of the live de-id call** — ADR-0015 OQ-3 spec-stage concern,
  explicitly "kept out of the ADR per the no-blueprint constraint." Impl, not architecture.
- **Operator data ingestion into the gitignored store** — operator-side (the intake captures it);
  an OUT-OF-SCOPE dependency, not a live-wiring architecture decision (recorded per the dispatch
  mandate as out-of-scope, not an ADR).
- **The SEC-01 ADR-0025-T1 caller-preconditions** (realpath-resolve-before-write; explicit
  `_repo_root` pass) — implementation the production caller owns, beaded; the `maintained.py`
  `_assert_contained` guard is already built ([maintained.py:61-106] [VERIFIED]). An OUT-OF-SCOPE
  implementation dependency, not an ADR.
- **The de-id token VOCABULARY (`SUMMARY_FIELD_SET`)** — governed by ADR-0019 + router.py
  change-control. The live de-id backend emits into the existing field-set; it does not redraw the
  vocabulary. Settled mechanism, not a new decision.
- **The role-inlining CONSTRAINT** (full profile verbatim on every dispatch) — INV-ROLE-INLINING +
  the `enforce-role-inlining` hook already fix it. A standing invariant the live-wiring honors, not a
  decision to author.
- **A dashboard / maintained-render redesign** — the dashboard is design-locked (Clinical Light);
  `reemit_maintained` is built. The live-wiring renders THROUGH the built path; no design decision.

---

## Notes for the DAG / authoring phase

- **The keystone (#1/ADR-0026) is the spine.** It resolves ADR-0022's OQ-1 + OQ-3 (the drive
  mechanism + where it lives) by selecting among A/B/C. #3 (composed gate) and #5 (specialist/lens
  dispatch) are the gate-side and specialist-side of WHATEVER driver model #1 picks — they most
  likely FOLD into ADR-0026 (which "owns the orchestrator control flow," per ADR-0022) rather than
  standing alone. The author should resolve the fold consciously at the discovery gate.
- **#2/ADR-0027 (live de-id backend) is the PII-API half of the S93 runtime split; #1/ADR-0026 is
  the subscription half.** Whether they are ONE ADR (the whole split) or TWO (the PII boundary's live
  shape vs the subscription driver) is the load-bearing fold question — lean TWO (distinct trade-off
  surfaces; AP-08 avoidance), but the author decides.
- **Extend-not-rebuild is a hard grounding fact** (HANDOFF S93 "Files I will NOT touch"): every
  live-wiring ADR WRAPS the built inner engine + the built seams + the built gate callables. The
  ADRs must state this so the build phase does not re-author `run_orchestrated`/the gates.
- **The substitution seam (ADR-0015 / ADR-0022's folded D-H) must reach the DRIVE layer.** ADR-0026
  picks the subscription driver for V1 WITHOUT foreclosing all-API/local-model — ADR-0022's
  subscription-coupling negative ("an all-API or local-model cutover requires re-validating that
  drive layer") is precisely what ADR-0026 sizes by choosing A vs B vs C (the skill harness under A
  vs a Python adapter under B re-validate differently).
- **Suggested provisional numbering:** ADR-0026 (runtime driver / subscription half + control flow,
  folds #3 + #5), ADR-0027 (live no-train de-id backend / PII-API half). If #3 splits out, ADR-0028.
  Final fold + numbering is the DAG phase's job; this is the discovery hypothesis.
