# ADR DAG — Plan-Generation Engine (Phase 3, 2026-06-23)

**Pipeline phase:** 3 (DAG). Builds the dependency graph + implementation tiers for the 6 approved
engine ADRs (0020–0025), grounded against the live tree and the touched existing ADRs (0001/0004/
0005/0006/0015/0016) + the design doc ADR-0022 supersedes. Does NOT author the ADRs.

**Decision set (final fold applied — both fold-candidates folded, per the discovery gate):**

| ID | Title | Status | Fold |
|----|-------|--------|------|
| ADR-0020 | Model-backed API de-id boundary (de-id IN) [LOAD-BEARING] | Proposed | — |
| ADR-0021 | Deterministic PII re-insertion (de-id OUT) [LOAD-BEARING] | Proposed | — |
| ADR-0022 | Programmatic subscription orchestrator (runtime supersession) | Proposed | folds D-H model-substitution seam |
| ADR-0023 | Post-assembly plan-quality judge | Proposed | folds D-F revise loop (judge-driven) |
| ADR-0024 | Multi-agent safety review of the assembled plan | Proposed | folds D-F revise loop (safety-driven) |
| ADR-0025 | Unified maintained HTML output format | Proposed | folds tracking/testing output sub-surfaces |

The topological sort is over the **NEW set only** (0020–0025). Edges to existing ADRs (§Cross-Refs)
are recorded for the authors' Related Decisions tables; they do not enter the new-set tier sort
(the existing ADRs are all accepted and in lower tiers already).

---

## §1 · Pairwise analysis (15 ordered pairs among the new set)

Strongest-applicable rule (depends-on > enables > constrains for asymmetric; tensions-with >
complements for symmetric). Each verdict is grounded in the decision semantics + the live tree.

| Pair | Verdict | Grounding |
|------|---------|-----------|
| 0020 ↔ 0021 | **complements** | The IN/OUT halves of ONE PII envelope, authored as a pair. Neither is a prerequisite: the IN boundary stands without re-insertion (the persisted store stays de-identified regardless), and the OUT side could re-insert from the gitignored identity config without the model-de-id IN existing (0021 approach (b)). They reinforce (the envelope is coherent only with both) and pull in the SAME direction (redraw the boundary together). The IN/OUT symmetry — what 0020 strips, 0021 must restore exactly — is the load-bearing coupling, recorded as a complement, not a tension (they do not contradict each other; each contradicts ADR-0005 separately). |
| 0020 → 0022 | **0022 depends-on 0020** | The orchestrator runs the plan-domain specialists over whatever the de-id-IN boundary emits — that de-identified summary IS the orchestrator's input contract. The orchestrator cannot dispatch specialists until the de-id-IN boundary (deterministic-only vs model-backed vs hybrid) is resolved. Hard prerequisite on the input contract. |
| 0020 → 0023 | no direct edge | Mediated through 0022 (the judge gates the orchestrator's output, not the de-id boundary directly). 0020's constraint reaches 0023 transitively via 0022 (see §5). |
| 0020 → 0024 | no direct edge | Mediated through 0022 (same as 0023). |
| 0020 → 0025 | no direct edge | Mediated through 0022 + 0021. The output renders the orchestrator's plan with 0021's re-inserted PII; 0020's de-id constraint reaches 0025 transitively (see §5). |
| 0021 → 0022 | no direct edge **[resolved-UNCERTAIN]** | Candidate "0021 depends-on 0022" (re-insertion needs a produced plan to render onto). RESOLVED to no direct edge: the OUT-boundary DECISION (model re-inserts vs deterministic local pass) is a render-surface property authorable without the orchestrator runtime being fixed — the existing inner engine already produces plan content to render onto, so the new orchestrator is not a prerequisite of the re-insertion DECISION. The real coupling is 0021 → 0025 (re-insertion feeds the maintained HTML) + the 0020↔0021 envelope complement. Keeps 0021 and 0022 in the same tier. |
| 0021 → 0023 | no direct edge | Orthogonal: the judge gates de-identified plan content; re-insertion happens at render, after review. No prerequisite either way. |
| 0021 → 0024 | no direct edge | Orthogonal (same as 0023): safety review operates on de-identified content; re-insertion is post-review render. |
| 0021 → 0025 | **0025 depends-on 0021** | The maintained HTML is the artifact 0021 re-inserts real PII onto (and the tracking/testing sub-surfaces 0025 folds are fed by 0021's re-inserted PII per discovery §7/decision-6). The output format's render contract consumes the re-insertion boundary's output; the re-insertion posture (what PII lands, gitignored-only) must be fixed before the maintained render lifecycle is decided. |
| 0022 → 0023 | **0023 depends-on 0022** | The judge is a verify gate over the ASSEMBLED plan the orchestrator produces; it wraps the orchestrator's output and cannot gate a plan no orchestrator produces. The orchestrator is the control surface the judge attaches to. |
| 0022 → 0024 | **0024 depends-on 0022** | The whole-plan multi-agent safety review wraps the orchestrator's assembled output (same shape as the judge). The review tier attaches to the orchestrator's control surface. |
| 0022 → 0025 | **0025 depends-on 0022** | The maintained HTML renders the orchestrator's (reviewed) plan; the orchestrator is the producer whose output the output-format lifecycle re-emits on new data. |
| 0023 ↔ 0024 | **complements** | Quality gate (judge) + safety gate (whole-plan review) both wrap the orchestrator's output and both gate into the folded revise loop. Neither is a prerequisite (either could ship without the other). They reinforce — quality + safety together is a stronger release gate than either alone — and the discovery-flagged open question (one combined review tier vs two distinct gates, and their ordering) is a compose-the-seam concern, the reinforce-and-define-boundary character of complements, not opposing pulls. |
| 0023 → 0025 | no direct edge | The "reviewed" qualifier on the rendered plan is a content property, not a structural prerequisite of the output-format LIFECYCLE decision (maintained/re-emit vs single-file). 0025 depends on 0022 (a plan to render) + 0021 (PII to re-insert); the judge gate is transitive through 0022. |
| 0024 → 0025 | no direct edge | Same as 0023→0025 — the safety-review gate is a content property on the plan, transitive through 0022, not a direct prerequisite of the render-lifecycle decision. |

**Symmetric edges (recorded once, alphabetical From/To):** 0020 complements 0021; 0023 complements
0024. Both must appear in BOTH partners' Related Decisions tables (integrity Check 2).

---

## §2 · Edge table (new-set)

| From | To | Type | Notes |
|------|-----|------|-------|
| 0022 | 0020 | depends-on | The orchestrator dispatches specialists over the de-id-IN boundary's emitted summary; that de-identified summary is the orchestrator's input contract, so the de-id-IN boundary must be resolved first. |
| 0023 | 0022 | depends-on | The plan-quality judge is a verify gate over the orchestrator's ASSEMBLED plan; it wraps the orchestrator's output and cannot gate a plan no orchestrator produces. |
| 0024 | 0022 | depends-on | The whole-plan multi-agent safety review wraps the orchestrator's assembled output; the review tier attaches to the orchestrator's control surface. |
| 0025 | 0022 | depends-on | The maintained HTML renders the orchestrator's (reviewed) plan; the orchestrator is the producer whose output the output-format re-emits on new data. |
| 0025 | 0021 | depends-on | The maintained HTML (+ its folded tracking/testing sub-surfaces) is the artifact 0021 re-inserts real PII onto; the re-insertion posture must be fixed before the maintained render lifecycle is decided. |
| 0020 | 0021 | complements | IN/OUT halves of one PII envelope authored as a pair; what 0020 strips, 0021 restores (the symmetry is load-bearing). Neither is a prerequisite. Recorded once (alphabetical). |
| 0023 | 0024 | complements | Quality gate + whole-plan safety gate both wrap the orchestrator output and gate the folded revise loop; together a stronger release gate than either. Neither is a prerequisite. The combined-vs-two-tiers + ordering question is the compose-the-seam concern. Recorded once (alphabetical). |

**Asymmetric edges (enter the tier sort):** 0022→0020, 0023→0022, 0024→0022, 0025→0022, 0025→0021.
**Symmetric edges (no ordering):** 0020–0021, 0023–0024.

No `enables` or `constrains` edges exist WITHIN the new set — every asymmetric inter-new-set
relationship is a hard `depends-on`. (The `constrains` relationships in this ADR set run from the
EXISTING crown-jewel ADRs INTO the new set — see §5.)

---

## §3 · Cycle detection

Asymmetric edges only: 0022→0020, 0023→0022, 0024→0022, 0025→0022, 0025→0021.

Adjacency (X depends-on Y, i.e. Y must precede X):
- 0022 → {0020}
- 0023 → {0022}
- 0024 → {0022}
- 0025 → {0022, 0021}
- 0020 → {} · 0021 → {}

No node reaches itself by following depends-on edges (0020 and 0021 are sinks of the
dependency arrows — nothing they depend on; everything flows toward them). **No cycle.** A valid
topological sort exists; no edge needs removal. (The two symmetric edges carry no ordering and
cannot form cycles by definition.)

---

## §4 · Topological sort → implementation tiers

Kahn's algorithm on the asymmetric (depends-on) edges, over the NEW set only:

1. Zero inbound depends-on/constrains among the new set → **Tier 1:** 0020, 0021.
   (0020: nothing in the new set precedes it. 0021: its only inbound is 0025→0021, which is
   OUTBOUND from 0021's perspective; 0021 itself depends on nothing in the new set.)
2. Remove Tier 1 + outgoing edges. Now 0022 has its only dependency (0020) satisfied →
   **Tier 2:** 0022.
3. Remove 0022. Now 0023 (dep 0022 ✓), 0024 (dep 0022 ✓), and 0025 (deps 0022 ✓ + 0021 ✓, 0021
   already in Tier 1) all have dependencies satisfied → **Tier 3:** 0023, 0024, 0025.

### Tier map

| Tier | ADRs | Author in parallel? |
|------|------|---------------------|
| **1 — Foundations (the PII envelope)** | ADR-0020 (de-id IN), ADR-0021 (de-id OUT) | YES — no depends-on between them (complement only). **Author as a pair** per discovery (the IN/OUT symmetry is load-bearing) — parallel-but-coordinated, not independent-and-isolated. Both carry the crown-jewel PII tensions + the rubric's dim-10 PII-Boundary Soundness axis. |
| **2 — Runtime control surface** | ADR-0022 (orchestrator) | Single ADR. Depends on 0020 (consumes its de-identified summary). Author after Tier 1 validated. Folds the D-H model-substitution seam (must not foreclose all-API / local-model / combo — extends ADR-0015). |
| **3 — Review + output layers** | ADR-0023 (judge), ADR-0024 (safety review), ADR-0025 (maintained HTML) | YES with one coordination: 0023 ∥ 0024 are a complement pair (resolve the quality-vs-safety seam together — one combined tier vs two gates). 0025 is independent of 0023/0024 (its only deps are 0022 + 0021, both lower-tier). All three depend only on Tiers 1–2 → parallel-OK once 0022 is validated. 0023/0024 fold the D-F revise loop. |

**Determination vs the discovery hypothesis.** Discovery suggested `0020 → 0022 → {0023 ∥ 0024} →
revise → {0021 → 0025}`. The derived DAG CORRECTS this in two places: (a) **0021 is Tier 1, not a
late stage** — the OUT-boundary DECISION does not depend on the orchestrator/judge/review (it is a
render-surface property; the existing inner engine already produces content to re-insert onto), so
0021 sits in the foundation tier paired with 0020, not gated behind the review tiers. The
discovery's `{0021 → 0025}` placed re-insertion late by conflating "re-insertion RENDERS the
reviewed plan" (a data-flow truth) with "the re-insertion DECISION depends on the review" (false —
the decision is authorable up front). (b) **the revise loop is not a node** — it folded into
0023/0024, so it is a mechanism inside those ADRs, not a DAG stage. The spine 0020 → 0022 →
{0023 ∥ 0024} is confirmed; the envelope-pairing of 0020+0021 at Tier 1 and 0025 at Tier 3 (deps
0022+0021) is the corrected shape.

### Runtime Stage Order (distinct from the dependency-tier order above)

**The dependency tiers (§4) are NOT the runtime execution order.** §4 gives the AUTHOR/BUILD order
(what must be decided/built before what — a partial order over `depends-on` edges); this subsection
pins the RUNTIME order (the sequence the ADR-0022 orchestrator executes a single plan through). They
DIFFER, and a builder following the tier sort as if it were the runtime sequence would mis-place the
de-id OUT stage. The load-bearing divergence: **ADR-0021 (de-id OUT) is Tier-1 by dependency** (its
decision depends on nothing in the new set — it is a render-surface property authorable up front, so
it pairs with 0020 in the foundation tier) **but executes LAST at runtime** (re-insertion is
render-time-only, off the persisted/committed store). Verified against the live wired path:
`scripts/plan/generate_plan.py` documents the production caller as `author → assemble → store →
render`, with the de-identified `router.summarize` summary as the front 0-raw-PII boundary and the
render as the terminal step ([generate_plan.py:1-17](../../../scripts/plan/generate_plan.py) [VERIFIED]).

**Canonical runtime sequence (one plan, end to end):**

1. **de-id IN (ADR-0020)** — the model-backed de-id boundary emits the de-identified summary; the
   0-raw-PII input contract for everything downstream.
2. **orchestrate / assemble (ADR-0022 + the inner engine)** — the programmatic subscription
   orchestrator dispatches the plan-domain specialists over that summary, and the inner engine
   (`generate_plans` / `assemble` / the reconciler + per-finding `adjudicate` gate) composes the
   reconciled, per-finding-safety-cleared assembled plan.
3. **{quality judge (ADR-0023) ∥ safety review (ADR-0024)}** — the post-assembly quality judge and the
   whole-plan multi-agent safety review gate the assembled plan. Their composition (one combined tier
   vs two; parallel vs ordered) is the OPEN shared OQ-2 (ADR-0023/0024) — the `∥` here denotes
   "both gate at this stage," not a resolved parallel/sequential ordering.
4. **revise loop** — judge/safety findings drive the bounded revise loop (re-author/revise failing
   sections through the orchestrator's `reauthor` seam, re-gate, halt at the cap then escalate). The
   loop's topology and joint cap are the OPEN shared OQ-2.
5. **de-id OUT re-insertion (ADR-0021)** — at render time only, the deterministic OUT boundary
   re-inserts the operator's real PII onto the gitignored operator-facing artifact (what step 1
   stripped, restored exactly). Authored Tier-1, executed here, LAST-but-one.
6. **maintained-format render (ADR-0025)** — the unified maintained-HTML output renders the
   PII-re-inserted plan as the gitignored single-file artifact, and re-emits it on new wearable/lab data.

Steps 1–2 and 6 are pinned; the 3–4 internal ordering (quality vs safety, single vs dual loop,
re-trigger rule) is the OPEN shared OQ-2 ADR-0022 owns the control flow for — the spec/build-plan
stage resolves it. Step 5 (de-id OUT) running after the gates and before/within the render is the
dependency-vs-runtime divergence this subsection exists to make explicit.

---

## §5 · Constraint propagation table

The `constrains` relationships in this set originate from the EXISTING crown-jewel ADRs (0001, 0005)
and propagate INTO and THROUGH the new set. (No new-set→new-set constrains edges exist; the new-set
ordering is pure depends-on.) Plus 0020's de-id-IN boundary constrains the downstream layers
transitively through 0022.

| Source constraint (From) | Direct target | Transitive targets | Constraint description (options eliminated) |
|--------------------------|---------------|---------------------|---------------------------------------------|
| ADR-0001 (summaries-not-raw; no-train lane) | ADR-0020 | 0022, 0023, 0024, 0025 (via 0020→0022) | Eliminates any de-id-IN option that routes raw PII to a TRAINING-ELIGIBLE lane, or that fabricates/silently-partials a summary on a failed call. 0020 MUST run on the no-train lane and MUST be fail-closed (mirror `compute_plan`'s `AUTHOR_CALL_FAILED`). Reaches the orchestrator (it dispatches over 0020's output) and the downstream review/output layers (they operate on the same de-identified-summary-derived plan). |
| ADR-0005 (no committed operator PII; gitignored-only) | ADR-0020, ADR-0021 | 0025 (via 0021→0025) | Eliminates any option where raw plan-intake PII (0020) or re-inserted real PII (0021) reaches a COMMITTED/tracked file. Forces: 0020's raw residue lands only on gitignored surfaces; 0021's re-inserted-PII artifact is a gitignored output the `block-pii-commit.sh` + `pre-push-pii-scan.sh` hooks deny on commit. Propagates to 0025: the maintained HTML carrying re-inserted PII must itself be a gitignored output, never a tracked artifact. |
| ADR-0020 (de-id-IN boundary shape — what raw text the API sees / what summary it emits) | ADR-0022 | 0023, 0024, 0025 (via 0022) | The de-id-IN boundary's emitted-summary shape narrows the orchestrator's input (specialists reason over exactly that summary), which in turn bounds what the judge (0023) and safety review (0024) can assess and what the output (0025) can render — the constraint is absorbed at each stage but the de-identified-summary content ceiling is the upstream limit. |
| ADR-0016 (raw-egress carve-out: conversation-only) | ADR-0020 | — | 0020 ADDS a SECOND raw-egress class (model-backed de-id of raw plan-intake state) beyond ADR-0016's conversation-only bound — per ADR-0016's own review trigger ("Any proposal to add a second raw-egress class … re-open this decision"), 0020's option space is bounded to: the new raw-egress is no-train-lane-only AND persisted-side-de-identified, the same bound ADR-0016 fixed for the conversation. Eliminates any unbounded/multi-lane raw-egress option. |
| ADR-0004 (single-file on-demand render lifecycle) | ADR-0025 | — | 0025 AMENDS ADR-0004; the constraint is the inherited offline / self-contained / <500KB / WCAG-AA / no-external-request budget — the maintained/re-emit lifecycle must keep each emitted artifact within ADR-0004's single-file portability budget (the maintained format is a new lifecycle ON TOP of, not a replacement of, the single-file render). |

**Transitivity check (integrity Check 4).** ADR-0001's no-train/summaries constraint is verified to
reach 0022/0023/0024/0025: each operates on the de-identified-summary-derived plan, so the
"reasons-over-summaries-not-raw" property is preserved at every stage (not absorbed at 0020 —
0020 only RELOCATES de-id to a model-backed boundary; the persisted-side-de-identified invariant
still rides through to the renderers). ADR-0005's no-committed-PII constraint reaches 0025 through
0021 (the maintained HTML inherits the gitignored-only bound). No constraint is silently dropped.

---

## §6 · Tension resolution requirements

Three crown-jewel tensions, all with the EXISTING PII ADRs (no new-set↔new-set tensions — 0020↔0021
and 0023↔0024 are complements, not tensions). Each requires a documented resolution before the
tensioned ADR proceeds to implementation (integrity Check 3): the accepted trade-off, the
mitigation, and the condition forcing reconsideration.

| ADR-A | ADR-B | Tension description | Resolution strategy (trade-off accepted · mitigation · reconsideration trigger) | Status |
|-------|-------|---------------------|----------------------------------------------------------------------------------|--------|
| ADR-0020 | ADR-0001 | 0020 routes RAW operator PII across the (no-train) API BEFORE de-identification on the plan path — exactly the surface ADR-0001's "Only plan reasoning touches the model, OVER SUMMARIES rather than raw PII" anchor + its falsification ("≥1 plan-reasoning dispatch sending raw (non-summary) PII to the model means the summaries-not-raw discipline failed") forbade. | **Trade-off accepted:** bounded no-train retention on raw plan-intake PII, the SAME exposure class ADR-0016 already accepted for the live conversation, now extended to plan-intake de-id (threat-model B's bounded-not-zero retention). **Mitigation:** (a) the boundary runs no-train-lane-only; (b) it is FAIL-CLOSED — a failed/partial de-id call yields the honest no-plan state (mirroring `compute_plan`'s `AUTHOR_CALL_FAILED`), NEVER a raw-PII leak downstream and never a fabricated summary; (c) the deterministic `router.summarize` is NOT deleted — the persisted/committed store stays de-identified, the boundary's OUTPUT still feeds the de-identified store. Frame as ADR-0001's summaries-not-raw being scoped (model-backed de-id boundary RELOCATES the de-id step, it does not remove the persisted-side-de-identified invariant), mirroring how ADR-0016 scoped zero-egress. **Reconsideration trigger:** the no-train provider's no-train/retention terms degrade (raw plan PII becoming training-eligible or indefinitely retained), OR the local-model North Star (ADR-0001 Alt C) reaches parity (then the raw-egress retracts to zero). | Pending — resolution authored in ADR-0020 Consequences; both ADR-0020 and ADR-0001 record it. |
| ADR-0020 | ADR-0005 | Raw plan-intake PII transits the API boundary; ADR-0005 keeps operator PII out of committed history (a leak cannot be cleanly scrubbed once landed). The risk: raw-PII residue from the de-id boundary reaching a tracked file. | **Trade-off accepted:** raw plan-intake PII exists transiently at the boundary (off-device, no-train, bounded retention) — the egress exposure, not a commit exposure. **Mitigation:** raw residue lands ONLY on gitignored surfaces (`vault/scaffold/filled/`, `vault/store/` are gitignored; the de-id boundary's raw input is never written to a tracked path); the registered `block-pii-commit.sh` PreToolUse hook + `pre-push-pii-scan.sh` backstop deny any committed filled-value/PII path — the SAME enforcement ADR-0016 leans on for the conversation transcript. The persisted store (the boundary's OUTPUT) is de-identified, so the tracked-side scan stays at 0 hits. **Reconsideration trigger:** ≥1 raw-PII hit in a committed file / git history on a fresh-clone scan (release-blocking, halt + revert the leaking path). | Pending — resolution authored in ADR-0020 Consequences; both ADR-0020 and ADR-0005 record it. |
| ADR-0021 | ADR-0005 | 0021 re-inserts the operator's REAL PII (full name, not initials) onto the rendered artifact, reversing the standing initials-only data-out posture; ADR-0005's falsification is "≥1 operator-PII value in a tracked file … release-blocking." The re-inserted PII must NEVER reach a committed file. | **Trade-off accepted:** the rendered artifact carries real PII for the LOCAL/UNCOMMITTED operator-facing output (the operator needs a name-bearing handout for their physician), reversing initials-only FOR THE GITIGNORED ARTIFACT ONLY. **Mitigation:** the re-inserted-PII artifact is a local, GITIGNORED output (the ADR-0005 `vault/scaffold/filled/` / artifacts surface); the `block-pii-commit.sh` + `pre-push-pii-scan.sh` hooks MUST continue to deny it on commit — the persisted/committed store + every tracked file stay de-identified (initials-only survives for any tracked render). 0021's OUT side re-inserts what 0020's IN side stripped (the envelope symmetry), and the re-insertion source is the gitignored identity config (mirroring how `component_set.read_profile` already reads initials from a gitignored source). **Reconsideration trigger:** ≥1 re-inserted-PII value found in a tracked/committed file (release-blocking, halt + restore the gitignored boundary); OR the hooks' coverage of the new maintained-HTML output path is found incomplete (extend the hook scope before the format ships). | Pending — resolution authored in ADR-0021 Consequences; both ADR-0021 and ADR-0005 record it. |

All three are **Pending** (resolution strategy defined, but the mitigation rests on enforcement that
must be RE-VERIFIED against the NEW output path — the maintained-HTML render surface 0025 introduces
is not yet covered by the existing hook test fixtures). Per dag-methodology, Pending resolutions
become Open Questions in BOTH tensioned ADRs and **prerequisite tasks** in the build plan (verify
the `block-pii-commit`/`pre-push` hooks deny a committed maintained-HTML artifact carrying
re-inserted PII, and deny raw plan-intake residue, BEFORE 0020/0021/0025 implement).

---

## §7 · Cross-references to EXISTING ADRs (for the authors' Related Decisions tables)

These edges are NOT in the new-set tier sort, but each new ADR's Related Decisions table must carry
them (and the inverse edge backfilled into the existing ADR per integrity Check 5). Relationship
types: `amends`/`supersedes` are documentation relationships (as the existing set uses them — e.g.
ADR-0016 `amends` ADR-0001 is "not a DAG edge"); `tensions-with`/`relates`/`constrains` follow the
5-type vocabulary.

| New ADR | → | Existing ADR | Type | Notes |
|---------|---|--------------|------|-------|
| ADR-0020 | → | ADR-0016 | amends | Extends ADR-0016's raw-egress carve-out to a SECOND raw-egress class (model-backed de-id of raw plan-intake state). Mandatory re-opening per ADR-0016's "second raw-egress class" review trigger. |
| ADR-0020 | → | ADR-0001 | tensions-with | Routes raw PII to the API before de-id — the surface ADR-0001's summaries-not-raw falsification forbade (see §6). |
| ADR-0020 | → | ADR-0005 | tensions-with | Raw plan-intake PII must never reach a committed file (see §6). |
| ADR-0020 | → | ADR-0015 | depends-on / relates | Runs through the already-wired `ModelClient.author`/`.converse` seam (`generate_plan` `client=`, `_FixedEnvelopeClient`); 0020 BUILDS ON the existing client, does not re-introduce it. Supersedes `router.summarize` as the SOLE de-id-IN on the plan path (summarize survives as the persisted-side de-id). |
| ADR-0021 | → | ADR-0005 | tensions-with | Re-inserted real PII must never reach a committed artifact (see §6) — the crown-jewel OUT tension. |
| ADR-0021 | → | ADR-0004 | supersedes-posture | Supersedes the data-out portion of ADR-0004 / ADR-0009-D2's INITIALS-ONLY rule for the gitignored operator-facing artifact (`handout.py`/`report.py`/`component_set.read_profile` render initials only today). Initials-only survives for any TRACKED render. |
| ADR-0021 | → | ADR-0001 | relates | The OUT half of the crown-jewel relaxation; pairs with 0020's IN half. Persisted-side-de-identified (ADR-0001) is honored — re-insertion is render-time-only, off the persisted store. |
| ADR-0022 | → | (design doc §Runtime model) | supersedes | Supersedes `vault/design/plan-generation-pipeline-v1.md` §"Runtime model (operator decision, S68)" — the "interactive Claude-Code / agent-dispatch session, not a standalone API client" model → a programmatic orchestrator. The design-doc section gets a `superseded_by: ADR-0022` pointer; the tier model + ordered-pipeline DAG + inner reconciler survive. |
| ADR-0022 | → | ADR-0006 | relates | Drives the ADR-0006 roster-assembly architecture (the orchestrator runs the plan-domain specialists); ADR-0006's routing/composition/attribution/safety-filter architecture is unchanged — the orchestrator WRAPS `orchestrate.generate_plans` / `pipeline.run_generation` (extend, not rebuild). |
| ADR-0022 | → | ADR-0015 | relates | Dispatches through the `ModelClient` ADR-0015 wired (already in production via `generate_plan`'s `client=`); folds the D-H model-substitution seam — extends ADR-0015's swap-seam discipline to the engine runtime so all-API / local-model / combo is not foreclosed (ADR-0015's "swap seam kept honest or it ossifies" falsification, extended). |
| ADR-0023 | → | ADR-0006 | relates | A verify gate over the ADR-0006 assembled plan; mirrors the build pipeline's judge. Distinct from the existing per-finding `adjudicate` medical-liaison gate (quality vs safety). Folds the D-F revise loop (judge-driven iteration). |
| ADR-0024 | → | ADR-0006 | relates | A whole-plan review tier WRAPPING (not replacing) the existing per-finding medical-liaison `adjudicate` gate (`scripts/plan/adjudicate.py`, INV-OVERRIDE-RECORD-SCHEMA / INV-CRITICAL-NON-OVERRIDABLE) + the reconciliation holds. The ADR must state how whole-plan review + per-finding adjudication compose without double-gating or gap. Folds the D-F revise loop (safety-driven iteration). |
| ADR-0024 | → | (ADR-0006-stage `adjudicate`) | distinct-from | Explicitly distinct from the per-finding medical-liaison terminal gate — a NEW whole-plan tier on top, not a redraw of the inner per-finding safety gate. |
| ADR-0025 | → | ADR-0004 | amends | Amends ADR-0004's on-demand single-file render: a MAINTAINED / re-emit-on-new-data lifecycle the API agent adjusts as wearables/labs arrive, on top of (not replacing) the single-file render. Inherits ADR-0004's offline/self-contained/<500KB/WCAG-AA budget. Folds the tracking/testing output sub-surfaces. |

**Inverse-edge backfill required (integrity Check 5, deferred to AUTHOR/VERIFY phase).** Each
existing ADR above must receive the inverse Related-Decisions row when the new ADR lands (e.g.
ADR-0001 gains `tensions-with ADR-0020`/`relates ADR-0021`; ADR-0016 gains `amended-by ADR-0020`;
ADR-0004 gains `amended-by ADR-0025` + `superseded-posture-by ADR-0021`; ADR-0006 gains
`relates ADR-0022/0023/0024`; ADR-0015 gains `relates ADR-0020/0022`). The cross-reference authority
is this `.pipeline/engine/dag.md` §7 (mirroring how the V1 set names `.pipeline/dag.md §6` as
canonical). Backfill is a Tier-by-tier AUTHOR-phase action, not a Phase-3 write.

---

## §8 · Integrity check results

| # | Check | Result |
|---|-------|--------|
| 1 | No cycles in asymmetric edges | **PASS** — §3: 0020/0021 are dependency sinks; no node reaches itself. Valid topological sort exists. |
| 2 | Bidirectional recording of symmetric edges | **PENDING (AUTHOR phase)** — 0020↔0021 and 0023↔0024 each recorded once here; both partners' Related Decisions tables must carry the complement when the ADRs are authored. |
| 3 | Tension resolution completeness | **PASS (strategy) / PENDING (status)** — all 3 tensions (§6) have a documented resolution strategy + reconsideration trigger; all 3 are Pending (enforcement must be re-verified against the new maintained-HTML output path) and become Open Questions in both tensioned ADRs + prerequisite build tasks. |
| 4 | Constraint propagation transitivity | **PASS** — §5: ADR-0001's no-train/summaries constraint verified to reach 0022/0023/0024/0025 (not absorbed at 0020 — 0020 relocates de-id, the persisted-side-de-identified property rides through); ADR-0005's no-committed-PII reaches 0025 via 0021. No constraint silently dropped. |
| 5 | Edge table ↔ Related Decisions consistency | **PENDING (AUTHOR phase)** — every §2 + §7 edge must appear in the corresponding ADR's Related Decisions table (and inverse), with matching type, when authored; no orphaned references. |
| 6 | Tier assignment validity | **PASS** — Tier 1 (0020, 0021): zero inbound depends-on/constrains among the new set. Tier 2 (0022): one inbound depends-on from Tier 1 (→0020). Tier 3 (0023→0022, 0024→0022, 0025→{0022,0021}): every inbound depends-on from a lower tier, none same-or-higher. |

---

## §9 · Handoff to Phase 4 (AUTHOR)

- **Author tier-by-tier:** Tier 1 first (0020 + 0021 as a coordinated PAIR — the IN/OUT envelope
  symmetry is load-bearing; both carry the rubric's dim-10 PII-Boundary Soundness axis + the
  crown-jewel tensions), VERIFY + JUDGE, then Tier 2 (0022), then Tier 3 (0023 ∥ 0024 as a complement
  pair resolving the quality-vs-safety seam; 0025 independent).
- **Cross-references to later-tier ADRs are invalid during authoring** (skill DAG rule): a Tier-1
  ADR cannot reference a not-yet-authored Tier-2/3 ADR in its body; `enables`/`complements`/inverse
  edges to later tiers are recorded in THIS dag.md and backfilled into the ADR body once the
  referenced ADR is complete. (0020's body may NOT forward-reference 0022's text; 0021↔0025 backfills
  when 0025 lands.)
- **The 3 Pending tensions (§6) become prerequisite build tasks:** re-verify `block-pii-commit.sh`
  + `pre-push-pii-scan.sh` deny (a) a committed maintained-HTML artifact carrying re-inserted PII and
  (b) raw plan-intake de-id residue, BEFORE 0020/0021/0025 implement.
- **Extend-not-rebuild is a hard grounding fact** for every new ADR's Context: each layer
  (0022/0023/0024/0025) WRAPS the built inner engine (`generate_plans` / `run_generation` /
  `adjudicate` / `assemble` / the closed loop) — state it explicitly so the build phase does not
  re-author the reconciler. The `ModelClient` `client=` seam is ALREADY wired (ADR-0015, S90) — 0020
  and 0022 BUILD ON it, they do not re-introduce the model client.
