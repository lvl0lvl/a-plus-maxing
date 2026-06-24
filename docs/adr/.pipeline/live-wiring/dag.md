# ADR DAG — Plan-Generation Engine LIVE-WIRING (Phase 3, 2026-06-24)

**Pipeline phase:** 3 (DAG). Builds the dependency graph + implementation tiers for the 2 approved
live-wiring ADRs (0026, 0027), grounded against the live tree and the touched existing ADRs
(0001/0005/0015/0016/0020/0022/0023/0024/0025). Does NOT author the ADRs. Mirrors the S92 engine DAG
(`docs/adr/.pipeline/engine/dag.md`) — same 5-type vocabulary, same inverse-edge-backfill discipline,
same reciprocation requirement, same dependency-tier-vs-runtime-stage split.

**Decision set (final fold applied at the Discovery gate — both fold-candidates resolved):**

| ID | Title | Status | Fold |
|----|-------|--------|------|
| ADR-0026 | Select the V1 subscription-runtime driver model (skill-as-orchestrator A / Python-driven adapter B / hybrid C) [LOAD-BEARING] | Proposed | folds the composed `gate_dispatch` topology (discovery #3) + the subscription specialist/safety-lens dispatch wiring (discovery #5) |
| ADR-0027 | Wire the live no-train API de-identification backend (`_ClaudeNoTrainBackend.deidentify`) [LOAD-BEARING] | Proposed | — |

The topological sort is over the **NEW set only** ({0026, 0027}). Edges to existing ADRs (§2 + §7)
are recorded for the authors' Related-Decisions tables + the inverse-backfill list (§3); they do not
enter the new-set tier sort (the existing ADRs are all proposed/accepted and sit in lower tiers
already).

**Vocabulary discipline.** Only the closed 5 types are used as Related-Decisions edge types:
`depends-on` / `enables` / `constrains` / `complements` / `tensions-with`. The discovery's "ADR-0026
**amends** ADR-0022" and "ADR-0027 **implements** ADR-0020" are documentation relationships — the
engine set's own convention is that `amends`/`supersedes`/`implements` are NOT among the 5 DAG types
(e.g. ADR-0016 `amends` ADR-0001 is recorded as "not a DAG edge"). This DAG maps each to the closest
of the 5 (`depends-on`, since each new ADR is a hard prerequisite-consumer of the amended/implemented
decision) and carries the `amends`/`implements` documentation character in the Notes column + a
Revision-History note on the amended ADR (§4). No new edge type is invented.

---

## §1 · Pairwise analysis (the 1 ordered pair within the NEW set)

Strongest-applicable rule (depends-on > enables > constrains for asymmetric; tensions-with >
complements for symmetric). Grounded in the decision semantics + the live tree.

| Pair | Verdict | Grounding |
|------|---------|-----------|
| 0026 ↔ 0027 | **0026 depends-on 0027** | These are the two halves of the ONE S93 runtime split — 0026 is the subscription half (the driver that dispatches specialists/gate-lenses), 0027 is the PII-API half (the live no-train de-id backend). The question is whether they `complement` (each authorable + buildable independently) or `depend-on` (one is a hard prerequisite of the other). **Resolved to a one-way `depends-on`, not a complement**, on the runtime-stage order: de-id IN is the FIRST runtime stage, and the driver dispatches every specialist over the de-identified summary the backend emits — that summary IS the driver's input contract, the SAME input-contract dependency the engine DAG recorded as `ADR-0022 depends-on ADR-0020` (`docs/adr/.pipeline/engine/dag.md §2` [VERIFIED]). A driver that runs end-to-end cannot dispatch a single specialist until the de-id backend that produces its input is wired and fail-closed; the driver's own Validation Approach (a live end-to-end run with 0 raw-PII in any dispatch) cannot pass without 0027. The reverse does NOT hold — 0027 wires `_ClaudeNoTrainBackend.deidentify` and emits the `SUMMARY_FIELD_SET`-shaped summary with no knowledge of which driver model (A/B/C) consumes it (`deid_in(raw_intake, client)` routes through `client.deidentify` and returns a summary string; `scripts/serve/server.py:225` already constructs a `ModelClient` for the intake path with no driver present, [client.py:78-95](../../../scripts/model/client.py), [deid_in.py:30-73](../../../scripts/plan/deid_in.py) [VERIFIED]). So the dependency is asymmetric: 0026 → 0027. **Distinguished from a complement:** a complement would require each to stand without the other; the driver's end-to-end capability does NOT stand without the live backend (the de-id sentinel halts the driver to honest-no-plan, [plan_orchestrator.py:136-305](../../../scripts/plan/plan_orchestrator.py) [VERIFIED]), so the asymmetric prerequisite is the correct, stronger edge. |

**Why not `0026 ↔ 0027` BOTH-ways (the cycle the task flagged):** a candidate reverse edge
"0027 depends-on 0026" was tested — does the live de-id backend need the driver to exist? No. The
backend's decision surface (no-train model-id, the prompt→summary contract, the fail-closed-to-
`ModelCallError` posture) is fixed entirely by ADR-0020's already-decided boundary + the existing
`ModelClient.deidentify` seam; it is wired and unit-testable with an injected backend and NO driver
in the call stack (the intake server already does exactly this). The reverse edge does not exist, so
there is no 2-cycle to break — the edge is one-way `0026 depends-on 0027` by construction (§3
confirms acyclicity).

---

## §2 · Edge table

### New-set edges (enter the tier sort)

| From | To | Type | Notes |
|------|-----|------|-------|
| ADR-0026 | ADR-0027 | depends-on | The runtime driver dispatches every plan-domain specialist + safety lens over the de-identified summary 0027's live backend emits — that summary is the driver's input contract, so the live de-id backend must be wired before the driver can run end-to-end (mirrors `ADR-0022 depends-on ADR-0020`, the same input-contract prerequisite). One-way; the backend has no reverse dependency on the driver (§1). |

### Edges from each new ADR to EXISTING ADRs (recorded for Related-Decisions tables; NOT in the new-set tier sort)

| From | To | Type | Notes |
|------|-----|------|-------|
| ADR-0026 | ADR-0022 | depends-on | ADR-0026 RESOLVES ADR-0022's deferred OQ-1 (how the orchestrator spawns the plan-domain specialist agents with full role profiles inlined) + OQ-3 (where the drive layer lives — a new `scripts/plan/` driver vs the skill harness) by selecting driver model A/B/C; it extends, does not reverse, ADR-0022's "programmatic subscription orchestrator, mirroring the build pipeline" decision. The `amends` documentation character (0026 resolves 0022's OQs) is carried here + as a Revision-History note on ADR-0022 (§4). 0026 cannot be authored until the orchestrator runtime decision (0022) is fixed — hard prerequisite. |
| ADR-0026 | ADR-0023 | depends-on | The composed `gate_dispatch` adapter ADR-0026 folds (discovery #3) consumes the ADR-0023 quality-judge callable (`quality_judge(plan, judge_client) -> {verdict: ACCEPT\|REVISE}`, [quality_judge.py:206-253](../../../scripts/plan/quality_judge.py) [VERIFIED]); 0026's drive layer composes that verdict into the loop's `{accept, safety_passed, revise_domains}` disposition. The judge tier (ADR-0023) must be decided before the driver that composes its verdict — prerequisite. Documentation character: 0026 resolves ADR-0023/0024's SHARED OQ-2 (the revise-loop composition topology). |
| ADR-0026 | ADR-0024 | depends-on | Symmetric to the 0023 edge: 0026's folded `gate_dispatch` composes the ADR-0024 safety-review callable (`review_plan(assembled_plan, dispatch, *, lenses) -> {passed, findings}`, [safety_review.py:110-169](../../../scripts/plan/safety_review.py) [VERIFIED]) into the loop disposition (deriving `safety_passed` from `passed`), and 0026's drive layer dispatches each safety lens as a subscription agent (discovery #5). The safety-review tier must be decided before the driver that composes it — prerequisite + resolves the SHARED OQ-2. |
| ADR-0026 | ADR-0015 | depends-on | The driver dispatches through the already-wired `ModelClient` seam (`scripts/model/client.py`); whichever of A/B/C is chosen, the model boundary stays the single ADR-0015 swap point, and 0026 must NOT foreclose the all-API / local-model cutover (ADR-0015's swap-seam-or-it-ossifies discipline, extended to the drive layer). Documentation character: 0026 carries forward the D-H model-substitution-seam constraint ADR-0022 folded. Prerequisite — the swap seam must exist before the driver built on it is decided. |
| ADR-0026 | ADR-0006 | relates | The driver DRIVES the ADR-0006 roster-assembly architecture (it runs the plan-domain specialists whose envelopes feed `assemble`); ADR-0006's routing/composition/attribution/safety-filter architecture is unchanged — the driver WRAPS `orchestrate.generate_plans` / `pipeline.run_generation` (extend, not rebuild). No ordering prerequisite beyond what 0022 already carries; `relates`, not `depends-on` (the discovery's "suspected relates ADR-0006"). |
| ADR-0027 | ADR-0020 | depends-on | ADR-0027 is the LIVE wiring of the model-backed de-id-IN boundary ADR-0020 DECIDED — it fills `_ClaudeNoTrainBackend.deidentify` (today a `NotImplementedError` stub, [client.py:156-160](../../../scripts/model/client.py) [VERIFIED]) with the real no-train API call honoring 0020's fail-closed + persisted-side-de-identified contract. The `implements` documentation character is carried here; 0027 cannot be authored until 0020's boundary architecture is fixed — hard prerequisite. |
| ADR-0027 | ADR-0015 | depends-on | ADR-0027 fills the swappable `ModelClient`'s `deidentify(raw_intake) -> summary` backend method — the third seam method ADR-0015 added alongside `converse`/`author` (ADR-0015 Revision History 2026-06-24, sanctioned by ADR-0020) — and must keep that method swappable (local-model North Star not foreclosed). The seam must exist before the live backend that fills it is decided — prerequisite. |
| ADR-0027 | ADR-0001 | tensions-with | The live backend makes raw operator PII actually transit the no-train API before de-identification — the concrete realization of the surface ADR-0001's "Only plan reasoning touches the model, over summaries rather than raw PII" falsification forbade. Boundary defined in 0027's Consequences; ADR-0001's persisted-side-de-identified invariant is honored (the live de-id RELOCATES de-id to a model boundary, it does not remove the de-identified store — `router.summarize` survives as the persisted-side gate). Inherits ADR-0020's already-resolved 0020↔0001 tension; 0027 carries the LIVE form of it. |
| ADR-0027 | ADR-0005 | tensions-with | The live backend's raw plan-intake input must never reach a committed/tracked file; ADR-0005 keeps operator PII out of git history. Boundary: raw residue lands ONLY on gitignored surfaces (`vault/scaffold/filled/`, `vault/store/`), denied at commit by `block-pii-commit.sh` + `pre-push-pii-scan.sh`; the persisted store (the backend's de-identified output) stays at 0 tracked-PII hits. Inherits ADR-0020's 0020↔0005 tension; 0027 is the live form. |
| ADR-0027 | ADR-0016 | constrains | ADR-0016's raw-egress carve-out (no-train lane, conversation-only, extended by ADR-0020 to the de-id class) BOUNDS the live backend: the de-id call runs on the no-train lane ONLY, and is the bounded second raw-egress class — never a third unbounded class. ADR-0016 narrows 0027's option space (no general/training-eligible lane permitted). Documentation note: ADR-0020 already `amends` ADR-0016 to admit this class; 0027 is constrained to stay within that bound. |

**Asymmetric edges entering the new-set tier sort:** `0026 → 0027` (the only intra-new-set edge).
**Edges to existing ADRs (do NOT enter the new-set sort):** all rows in the second table above.

No `enables` or `complements` edges exist within the new set (the two halves are an asymmetric
prerequisite, not a reinforcing pair — §1). The `constrains` edges into the new set originate from
the EXISTING crown-jewel ADRs (0001/0005/0016 → 0027, transitively → 0026; see §5).

---

## §3 · Reciprocal-edge backfill list (existing-ADR → new edge to append)

Every new edge that touches an EXISTING ADR requires the inverse Related-Decisions row backfilled
into that existing ADR when the new ADR lands (integrity Check 5 / Check 2; the S92 run did exactly
this, RT-01 Phase-8 backfill). The cross-reference authority for the live-wiring set is THIS file
(`docs/adr/.pipeline/live-wiring/dag.md §2`), mirroring how the engine set names its `dag.md §7`.
Each row below is the exact inverse edge the AUTHOR/FINAL-FIX phase appends to the named existing
ADR's Related-Decisions table.

| Existing ADR | Inverse edge to append | Type (in the existing ADR) | Note for the backfill |
|--------------|------------------------|----------------------------|------------------------|
| ADR-0022 | `→ ADR-0026` | depends-on (inbound) | "ADR-0026 selects the V1 subscription-runtime driver model, RESOLVING this ADR's deferred OQ-1 (specialist-agent spawn mechanism) + OQ-3 (drive-layer location); the inverse of ADR-0026's outbound `depends-on ADR-0022`." PLUS a **Revision-History row** on ADR-0022: "Amended by ADR-0026 — OQ-1/OQ-3 resolved by the driver-model selection (skill-as-orchestrator vs Python adapter vs hybrid); this ADR's 'subscription orchestrator mirroring the build pipeline' decision is unchanged, the DRIVE mechanism is now fixed." (§4 details the amendment posture.) |
| ADR-0020 | `→ ADR-0027` | depends-on (inbound) | "ADR-0027 wires the LIVE `_ClaudeNoTrainBackend.deidentify` that IMPLEMENTS this ADR's model-backed de-id-IN boundary (fail-closed, no-train-lane-only, persisted-side-de-identified); the inverse of ADR-0027's outbound `depends-on ADR-0020`." The `implements` documentation character is recorded in the Note; no edge-type invention. |
| ADR-0015 | `→ ADR-0026` and `→ ADR-0027` | enables (×2) — pattern-match the existing ADR-0015 `enables ADR-0020` row | ADR-0015 already records `enables` for its consumers (ADR-0020 `enables`, ADR-0022 `relates`). Append: "ADR-0026 — relates: the driver dispatches through this client's `ModelClient` seam, extending the swap-seam discipline to the drive layer (inverse of ADR-0026 → 0015 `depends-on`)." and "ADR-0027 — enables: ADR-0027's live de-id backend fills this client's `deidentify` seam method (the third method added 2026-06-24); the boundary builds ON this client and does not re-introduce it (inverse of ADR-0027 → 0015 `depends-on`)." Use `relates` for 0026 and `enables` for 0027 to match ADR-0015's existing convention (`relates` for the orchestrator-runtime consumer ADR-0022; `enables` for the boundary-filling consumer ADR-0020). |
| ADR-0001 | `→ ADR-0027` | relates | "ADR-0027 is the LIVE form of the crown-jewel de-id-IN relaxation ADR-0020 introduced; this ADR's summaries-not-raw + persisted-side-de-identified invariant is honored (the live de-id RELOCATES de-id to a model boundary, the persisted store stays de-identified). Pairs with the existing `tensions-with ADR-0020` / `relates ADR-0021` rows." (ADR-0001 already carries the 0020 tension; 0027's LIVE form `relates`, the tension itself stays anchored on 0020 to avoid double-counting — see §6.) |
| ADR-0005 | `→ ADR-0027` | relates | "ADR-0027's live de-id backend transits raw plan-intake PII off-device (the egress exposure, not a commit exposure); raw residue lands only on gitignored surfaces, denied at commit by `block-pii-commit.sh` + `pre-push-pii-scan.sh`. Pairs with the existing `tensions-with ADR-0020`. The tension itself stays anchored on ADR-0020 (the boundary DECISION); 0027 `relates` as its live implementation — §6." |
| ADR-0016 | `→ ADR-0027` | constrained (inbound) — record as `constrains` from ADR-0016's side | "ADR-0016's no-train-lane / bounded-raw-egress carve-out (extended by ADR-0020 to the de-id class) BOUNDS ADR-0027's live backend to the no-train lane only; the inverse of ADR-0027's outbound `constrains`-from-0016 dependency. No THIRD raw-egress class is opened." |
| ADR-0006 | `→ ADR-0026` | relates | "ADR-0026's runtime driver DRIVES this ADR's roster-assembly architecture (runs the plan-domain specialists whose envelopes feed `assemble`); ADR-0006's routing/composition/attribution/safety-filter architecture is unchanged. Pairs with the existing `relates ADR-0022/0023/0024` rows." |
| ADR-0023 | `→ ADR-0026` | depends-on (inbound) | "ADR-0026's folded `gate_dispatch` adapter composes this ADR's quality-judge verdict (`{ACCEPT\|REVISE}`) into the orchestrator loop's `{accept, safety_passed, revise_domains}` disposition, resolving the SHARED OQ-2 (revise-loop composition topology) this ADR carries; the inverse of ADR-0026 → 0023 `depends-on`." |
| ADR-0024 | `→ ADR-0026` | depends-on (inbound) | "ADR-0026's folded `gate_dispatch` adapter composes this ADR's safety-review result (`{passed, findings}`) into the loop disposition (deriving `safety_passed` from `passed`) and dispatches each safety lens as a subscription agent, resolving the SHARED OQ-2 this ADR carries; the inverse of ADR-0026 → 0024 `depends-on`." |

**Backfill timing.** Per the engine-set discipline, the inverse rows are appended at the AUTHOR /
FINAL-FIX phase once both new ADRs exist (a Tier-1 ADR may not forward-reference a not-yet-authored
Tier-2 ADR in its body). The `0026 ↔ 0027` intra-new-set edge is recorded in BOTH new ADRs at author
time (0027 in Tier 1 carries the inbound `depends-on (from ADR-0026)`; 0026 in Tier 2 carries the
outbound `depends-on ADR-0027`).

**Reasoned exclusion — ADR-0025 (RT-09).** ADR-0025 takes NO edge to the live-wiring set — it renders
`run_orchestrated`'s output and re-emits on new data REGARDLESS of who drives the loop; A′ does not
change the rendered output's shape, so ADR-0025's existing `depends-on ADR-0022` (the producer-runtime)
needs no ADR-0026 reciprocation. Recorded so the absence is a decision, not an omission.

---

## §4 · Tier assignments + the amendment-vs-tension resolution

### Cycle detection

Asymmetric edges within the new set: `0026 → 0027` (only). Adjacency (X depends-on Y, i.e. Y must
precede X): `0026 → {0027}`; `0027 → {}`. ADR-0027 is the dependency sink (nothing in the new set
precedes it). No node reaches itself. **No cycle.** A valid topological sort exists; no edge needs
removal. (The candidate reverse `0027 → 0026` was tested and rejected in §1 — it does not exist, so
there is no 2-cycle to break.)

### Topological sort → tiers (Kahn's algorithm on the asymmetric depends-on edge, new set only)

1. Zero inbound depends-on/constrains from WITHIN the new set → **Tier 1:** ADR-0027.
   (0027's only inbound is `0026 → 0027`, which is OUTBOUND from 0027's perspective; 0027 itself
   depends on nothing in the new set — its other `depends-on` edges all point at EXISTING lower-tier
   ADRs 0020/0015/0016, already accepted/proposed.)
2. Remove Tier 1 + its outgoing edges. Now ADR-0026's only intra-new-set dependency (0027) is
   satisfied → **Tier 2:** ADR-0026.

| Tier | ADRs | Author in parallel? |
|------|------|---------------------|
| **1 — PII-API half (the live de-id backend)** | ADR-0027 (live no-train `_ClaudeNoTrainBackend.deidentify`) | Single ADR. Depends only on EXISTING ADRs (0020 boundary decision, 0015 client seam, 0016 lane bound) — all accepted/proposed, lower tier. Carries the rubric's dim-10 PII-Boundary Integrity axis (it is the crown-jewel raw-PII egress) + the LIVE form of the 0020↔0001 / 0020↔0005 tensions. Author first, VERIFY + JUDGE, then Tier 2. |
| **2 — Subscription half (the runtime driver + folded gate/specialist dispatch)** | ADR-0026 (driver model A/B/C; folds `gate_dispatch` composition + specialist/lens dispatch) | Single ADR. Depends on ADR-0027 (consumes the de-identified summary the live backend emits) + the EXISTING 0022/0023/0024/0015/0006. Author after Tier 1 validated. Resolves ADR-0022's OQ-1/OQ-3 + ADR-0023/0024's SHARED OQ-2; must not foreclose the ADR-0015 all-API / local-model swap. |

**Tier-assignment consistency (integrity Check 6).** Tier 1 (0027): zero inbound depends-on/constrains
from within the new set — valid. Tier 2 (0026): exactly one inbound-from-lower-tier dependency
(`0026 → 0027`, 0027 in Tier 1), none same-or-higher — valid. Consistent with the §2 edge table.

### The ADR-0026-amends-ADR-0022 question: depends-on, NOT tensions-with

The task asks whether ADR-0026 amending ADR-0022 is a `tensions-with` (0026 supersedes part of
0022's deferred design) or a `depends-on`/`enables`. **Resolved: `depends-on` (with an `amends`
documentation character), NOT `tensions-with`.** The reasoning:

- A `tensions-with` requires the two decisions to pull in DIFFERENT directions — both valid, but
  their coexistence needs a managed boundary (dag-methodology §5). ADR-0026 and ADR-0022 do NOT pull
  in different directions: ADR-0026 RESOLVES the exact OQs ADR-0022 explicitly DEFERRED (OQ-1
  specialist-spawn, OQ-3 drive-layer location). ADR-0022 said "subscription orchestrator mirroring
  the build pipeline, drive mechanism = OQ-1/OQ-3 for build-planning"; ADR-0026 picks the concrete
  drive mechanism. That is a parent→child resolution (a hard prerequisite-and-completion), the
  signature of `depends-on`, not opposing pulls. There is no boundary to manage between them — there
  is a deferred decision being made.
- It is NOT a `supersession`: ADR-0026 does not REVERSE ADR-0022's "subscription, mirroring the build
  pipeline" decision (the discovery is explicit — "this ADR does NOT reverse that"). A supersession
  would replace 0022; instead 0026 EXTENDS it by filling its deferred OQs. The engine set uses
  `amends` (documentation) for exactly this "extends-not-reverses" relationship (ADR-0016 `amends`
  ADR-0001).
- Therefore the DAG edge is `ADR-0026 depends-on ADR-0022` (0026 cannot be authored until 0022's
  runtime decision is fixed), and the `amends` character is documentation, carried in §2's Notes +
  the Revision-History note below.

**How ADR-0022's Revision History should note the amendment** (the §3 backfill spells the exact row):

> | 2026-06-24 | Amended by ADR-0026 (live-wiring set Tier 2) — the deferred OQ-1 (how the
> orchestrator spawns plan-domain specialist agents with full profiles inlined) and OQ-3 (where the
> drive layer lives: a new `scripts/plan/` driver vs the skill harness) are RESOLVED by ADR-0026's
> selection of the V1 subscription-runtime driver model (A skill-as-orchestrator / B Python-driven
> adapter / C hybrid). This ADR's core decision — a programmatic subscription orchestrator mirroring
> the autonomous build pipeline, riding the ADR-0015 swap seam — is UNCHANGED; only the deferred
> drive MECHANISM is now fixed. ADR-0026 also resolves the SHARED OQ-2 (revise-loop composition
> topology across ADR-0023/0024) this ADR owns the control flow for. | Walter McGivney |

ADR-0022 also gains the inbound `depends-on (from ADR-0026)` Related-Decisions row (§3). ADR-0022's
OQ-1, OQ-3, and the OQ-2 pointer should be marked RESOLVED-BY-ADR-0026 (not deleted — the OQ history
is preserved, the resolution is annotated), mirroring how the engine set annotated resolved OQs.

---

## §5 · Constraint-propagation table

The `constrains` relationships originate from the EXISTING crown-jewel ADRs (0001, 0005, 0016) and
propagate INTO the new set — directly into ADR-0027 (the raw-PII egress) and TRANSITIVELY into
ADR-0026 through the `0026 → 0027` input-contract edge (the driver dispatches only over the
de-identified summary the constrained backend emits). No new-set→new-set `constrains` edge exists
(the intra-new-set ordering is pure `depends-on`).

| Source constraint (From) | Direct target | Transitive target | Constraint description (options eliminated) |
|--------------------------|---------------|-------------------|---------------------------------------------|
| ADR-0001 (summaries-not-raw; no-train lane) | ADR-0027 | ADR-0026 (via 0026→0027) | The live de-id backend MUST emit ONLY `SUMMARY_FIELD_SET`-bounded de-identified fields — raw PII is NEVER returned past the boundary into the summary the pipeline consumes. Eliminates any backend option that returns raw/partial PII in its output, or that fabricates a summary on a failed call. Reaches the driver (0026): every subscription specialist/lens dispatch is over exactly that de-identified summary, so the summaries-not-raw property rides through to the driver — the driver cannot dispatch raw PII because the only input it receives is the de-identified summary. |
| ADR-0005 (no committed/tracked operator PII; gitignored-only) | ADR-0027 | ADR-0026 (via 0026→0027) | The no-train API key the live backend uses is NEVER tracked, printed, or committed — it is runtime-injected (env / gitignored config), the same posture `block-pii-commit.sh` enforces. The backend's raw plan-intake input lands ONLY on gitignored surfaces; the `block-pii-commit.sh` + `pre-push-pii-scan.sh` hooks deny any committed filled-value/PII path. Eliminates any option that writes the key or raw residue to a tracked file. Reaches the driver transitively: the driver records plans + the doctor-visit queue, and those records carry only the de-identified-summary-derived content (0 raw PII), so the no-committed-PII bound holds at the driver's `record_plan` surface too. |
| ADR-0016 (raw-egress carve-out: no-train lane, bounded class) | ADR-0027 | ADR-0026 (via 0026→0027) | The live API de-id is the BOUNDED SECOND raw-egress class (ADR-0020 extended ADR-0016 to admit it). Eliminates any backend option that egresses raw on a training-eligible/general lane, or that opens a THIRD unbounded raw-egress class. The de-id call runs no-train-lane-only. Reaches the driver only as the standing bound (the driver itself egresses nothing raw — it dispatches over the de-identified summary), so the constraint is ABSORBED at 0027 for the egress concern; it propagates to 0026 only as the documentation invariant "no new raw-egress class is opened by the driver." |
| ADR-0020 (de-id-IN boundary shape — what raw the API sees / what summary it emits) | ADR-0027 | ADR-0026 (via 0026→0027) | ADR-0020's already-DECIDED boundary shape (fail-closed to honest-no-plan; persisted-side `router.summarize` retained; the no-train lane) narrows ADR-0027's live-wiring option space to: the live backend must be fail-closed (a failed/partial de-id → `ModelCallError` → the de-id sentinel halts the driver to honest-no-plan, never a raw leak or fabricated summary), and the persisted store stays de-identified. Reaches the driver: the driver's de-id-sentinel halt path ([plan_orchestrator.py:136-305](../../../scripts/plan/plan_orchestrator.py) [VERIFIED]) is the consumer of 0027's fail-closed contract. |

**Transitivity check (integrity Check 4).** ADR-0001's summaries-not-raw constraint is verified to
reach ADR-0026: the driver dispatches every specialist/lens over the de-identified summary 0027
emits, so the reasons-over-summaries-not-raw property is preserved at the driver (not absorbed at
0027 — 0027 only RELOCATES de-id to the live model boundary; the de-identified-summary invariant
rides through to the driver's dispatches). ADR-0005's no-committed-PII reaches 0026 at its
`record_plan` surface (records carry only de-identified content). ADR-0016's lane bound is ABSORBED
at 0027 for the egress concern (the driver egresses nothing raw) — documented why propagation stops
there. No constraint silently dropped.

---

## §6 · Tension-resolution requirements

Two crown-jewel tensions, both ADR-0027 ↔ an EXISTING PII ADR (no new-set↔new-set tensions — the one
intra-new-set edge `0026 → 0027` is a `depends-on`, not a tension; and ADR-0026 ↔ ADR-0022 is a
`depends-on`/amends, not a tension, per §4). Each requires a documented resolution before ADR-0027
proceeds to implementation (integrity Check 3): the trade-off accepted, the mitigation, the
reconsideration trigger. Both INHERIT the resolution ADR-0020 already authored (the engine DAG §6) —
ADR-0027 is the LIVE form of the boundary ADR-0020 decided, so the tension is anchored on ADR-0020
(the DECISION) and ADR-0027 carries the live-wiring confirmation that the mitigation holds against
the real API call.

| ADR-A | ADR-B | Tension description | Resolution strategy (trade-off accepted · mitigation · reconsideration trigger) | Status |
|-------|-------|---------------------|----------------------------------------------------------------------------------|--------|
| ADR-0027 | ADR-0001 | The LIVE backend makes raw operator PII ACTUALLY transit the no-train API before de-identification (where ADR-0020 DECIDED the boundary, ADR-0027 turns the `NotImplementedError` stub into the real call) — the concrete realization of the surface ADR-0001's "summaries-not-raw" falsification forbade. | **Trade-off accepted:** bounded no-train retention on raw plan-intake PII at the live call — the SAME exposure class ADR-0020 already adopted (which itself extended ADR-0016's conversation egress). **Mitigation:** (a) the live call runs no-train-lane-only; (b) it is FAIL-CLOSED — a failed/partial/empty de-id call raises `ModelCallError`, the de-id sentinel halts the driver to honest-no-plan ([client.py:78-95](../../../scripts/model/client.py), [plan_orchestrator.py:136-305](../../../scripts/plan/plan_orchestrator.py) [VERIFIED]), never a raw leak or fabricated summary; (c) the deterministic `router.summarize` is NOT deleted — the persisted/committed store stays de-identified, the live backend's OUTPUT still feeds the de-identified store. **Reconsideration trigger:** the no-train provider's no-train/retention terms degrade (raw plan PII becoming training-eligible or indefinitely retained), OR the local-model North Star (ADR-0001 Alt C) reaches parity (the raw-egress retracts to zero by swapping the ADR-0015 backend). | Pending — INHERITS the ADR-0020↔0001 resolution (engine dag.md §6); ADR-0027 records the LIVE-form confirmation (the real call honors the fail-closed + whitelist contract). Becomes an Open Question in ADR-0027 + a prerequisite build task (the raw-PII-leak probe MUST pass against the live call before release). |
| ADR-0027 | ADR-0005 | The LIVE backend's raw plan-intake input + the no-train API KEY it uses must never reach a committed/tracked file; ADR-0005's falsification is "≥1 operator-PII value in a tracked file … release-blocking." | **Trade-off accepted:** raw plan-intake PII exists transiently at the live boundary (off-device, no-train, bounded retention) — the egress exposure, not a commit exposure — and the API key is a runtime secret. **Mitigation:** (a) raw residue lands ONLY on gitignored surfaces (`vault/scaffold/filled/`, `vault/store/`); (b) the API key is runtime-injected (env / gitignored config), NEVER tracked/printed/committed — the `block-pii-commit.sh` PreToolUse hook + `pre-push-pii-scan.sh` backstop deny any committed filled-value/PII/secret path; (c) the persisted store (the backend's de-identified output) stays at 0 tracked-PII hits. **Reconsideration trigger:** ≥1 raw-PII hit OR ≥1 API-key hit in a committed file / git history on a fresh-clone scan (release-blocking, halt + revert the leaking path). | Pending — INHERITS the ADR-0020↔0005 resolution (engine dag.md §6); ADR-0027 records the LIVE-form confirmation (the live key handling + raw-residue routing honor the no-committed-PII invariant). Becomes an Open Question in ADR-0027 + a prerequisite build task. |

**No tension on the ADR-0026 ↔ ADR-0022 amendment** (§4): they do not pull in different directions —
0026 resolves 0022's deferred OQs (a `depends-on`/amends parent→child resolution), so there is no
boundary to manage, only a deferred decision being made. Recorded here explicitly so a reviewer does
not mistake the amendment for an unresolved tension.

**Both ADR-0027 tensions are Pending** because the mitigation rests on enforcement that must be
RE-VERIFIED against the LIVE call path (the real no-train API request, the runtime key handling, and
the raw-residue routing OQ-3 ADR-0020 carries) — not yet exercised against a real backend. Per
dag-methodology, Pending resolutions become Open Questions in ADR-0027 AND prerequisite build tasks
(the raw-PII-leak probe + the key-never-committed scan + the fail-closed-on-live-error test MUST pass
against the live backend BEFORE ADR-0027 implements). This is the dim-10 PII-Boundary Integrity axis
the rubric makes non-negotiable for this run.

---

## §7 · Runtime stage order (control flow — distinct from the dependency tiers in §4)

**The §4 dependency tiers are NOT the runtime execution order.** §4 gives the AUTHOR/BUILD order
(what must be decided before what — a partial order over `depends-on` edges); this section pins the
RUNTIME order (the control-flow sequence the live-wired driver executes a single plan through). They
DIFFER — the canonical engine-set divergence is that ADR-0021's de-id OUT is authored Tier-1 by
dependency but runs LAST at render (engine dag.md §"Runtime Stage Order"). For the live-wiring set,
the divergence is that **ADR-0027 (live de-id IN) is Tier-1 by dependency AND runs FIRST at runtime**
(the input-contract producer), while **ADR-0026 (the driver) is Tier-2 by dependency but is the
ORCHESTRATOR of the whole runtime sequence** — it does not occupy a single stage, it DRIVES stages
2-4. Verified against the live wired path: `deid_in(raw_intake, client)` is the front 0-raw-PII
boundary, `run_orchestrated` drives the dispatch + revise loop, `reinsert_out` (deterministic) +
`reemit_maintained` are the terminal render ([deid_in.py:30-73](../../../scripts/plan/deid_in.py),
[plan_orchestrator.py:136-305](../../../scripts/plan/plan_orchestrator.py),
[reinsert_out.py](../../../scripts/plan/reinsert_out.py),
[maintained.py:245 `reemit_maintained`](../../../scripts/generate/maintained.py) [VERIFIED]).

**Canonical runtime sequence (one plan, end to end — the live-wiring spec needs this):**

1. **de-id IN (ADR-0027 backend, via the ADR-0020 boundary)** — the live `_ClaudeNoTrainBackend.deidentify`
   no-train API call ingests raw operator plan-intake PII and emits the de-identified
   `SUMMARY_FIELD_SET`-shaped summary; the 0-raw-PII input contract for everything downstream.
   Fail-closed: a failed/partial call → `ModelCallError` → the de-id sentinel halts to honest-no-plan
   (no stage 2 runs).
2. **subscription specialist dispatch + orchestrate/assemble (ADR-0026 driver + the inner engine)** —
   the driver dispatches each plan-domain specialist (full profile inlined per INV-ROLE-INLINING) as
   a SUBSCRIPTION agent over the de-identified summary, captures each envelope, and drives
   `pipeline.run_generation` (the built reconciler + per-finding `adjudicate` gate composes the
   reconciled, per-finding-safety-cleared assembled plan). This is discovery #5 (the specialist-side
   of the driver model), folded into ADR-0026.
3. **{quality judge (ADR-0023) ∥ safety review (ADR-0024)} composed via `gate_dispatch` (ADR-0026)** —
   the driver's folded `gate_dispatch` adapter (discovery #3) composes the ADR-0023 quality-judge
   verdict (`{ACCEPT|REVISE}`) and the ADR-0024 safety-review result (`{passed, findings}`, each
   lens dispatched as a subscription agent) into the loop's single
   `{accept, safety_passed, revise_domains}` disposition. The `∥` denotes "both gate at this stage";
   the one-combined-vs-two + ordering is the SHARED OQ-2 ADR-0026 resolves.
4. **bounded revise loop (ADR-0026 control flow)** — judge/safety findings drive the bounded
   scratch-and-promote revise loop (re-author failing domains through the `reauthor` seam, re-gate,
   halt at `revise_cap` then escalate). The loop topology + joint cap is the SHARED OQ-2.
5. **de-id OUT re-insertion (ADR-0021, deterministic, model-free)** — at render time only, the
   deterministic OUT boundary re-inserts the operator's real PII onto the gitignored operator-facing
   artifact (what stage 1 stripped, restored exactly). Already built + decided (ADR-0021); NOT in the
   live-wiring ADR set — it is the model-FREE terminal pass.
6. **maintained render (ADR-0025)** — `reemit_maintained` renders the PII-re-inserted plan as the
   gitignored single-file maintained artifact, re-emitting on new wearable/lab data. Already built +
   decided (ADR-0025); the live-wiring renders THROUGH it.

Stages 1-2 and 5-6 are pinned; the 3-4 internal ordering (quality-vs-safety, single-vs-dual loop, the
re-trigger rule, the joint cap) is the SHARED OQ-2 ADR-0026 owns the control flow for — the
spec/build-plan stage resolves it. The live-wiring ADRs author stages 1 (ADR-0027) and 2-4 (ADR-0026);
stages 5-6 are the already-decided deterministic-OUT + maintained-render the wiring runs through
unchanged.

---

## §8 · Integrity check results

| # | Check | Result |
|---|-------|--------|
| 1 | No cycles in asymmetric edges | **PASS** — §4: `0026 → 0027` is the only intra-new-set asymmetric edge; 0027 is the dependency sink; the candidate reverse `0027 → 0026` was tested + rejected (§1). No node reaches itself. Valid topological sort exists; no edge removed. |
| 2 | Bidirectional recording of symmetric edges | **N/A → PASS** — no `complements`/`tensions-with` edges WITHIN the new set (the intra-new-set edge is a `depends-on`). The ADR-0027↔0001 and ADR-0027↔0005 `tensions-with` edges are to EXISTING ADRs; both partners' tables carry them via the §3 backfill (the existing ADRs gain a `relates` row, the tension anchored on ADR-0020 per §6 to avoid double-counting). |
| 3 | Tension resolution completeness | **PASS (strategy) / PENDING (status)** — both §6 tensions have a documented resolution strategy + reconsideration trigger (inherited from the ADR-0020 engine resolution, with a live-form confirmation); both are Pending (the mitigation must be re-verified against the LIVE call) and become Open Questions in ADR-0027 + prerequisite build tasks. |
| 4 | Constraint propagation transitivity | **PASS** — §5: ADR-0001's summaries-not-raw + ADR-0005's no-committed-PII verified to reach ADR-0026 through the `0026→0027` input-contract edge (the driver dispatches only over the de-identified summary; records only de-identified content); ADR-0016's lane bound documented as ABSORBED at 0027 for the egress concern. No constraint silently dropped. |
| 5 | Edge table ↔ Related Decisions consistency | **PENDING (AUTHOR phase)** — every §2 edge must appear in the corresponding new ADR's Related-Decisions table, and every §3 inverse edge must be backfilled into the named existing ADR, with matching type, when authored. The §3 list is the exact backfill roster. |
| 6 | Tier assignment validity | **PASS** — §4: Tier 1 (0027) zero inbound depends-on/constrains from within the new set; Tier 2 (0026) exactly one inbound `depends-on` from Tier 1 (→0027), none same-or-higher. Consistent with the §2 edge table. |

---

## §9 · Handoff to Phase 4 (AUTHOR)

- **Author tier-by-tier:** Tier 1 first (ADR-0027, the live de-id backend — carries the dim-10
  PII-Boundary Integrity axis + the LIVE form of the 0020↔0001 / 0020↔0005 tensions), VERIFY + JUDGE,
  then Tier 2 (ADR-0026, the driver model A/B/C resolving 0022's OQ-1/OQ-3 + 0023/0024's OQ-2).
- **Cross-references to later-tier ADRs are invalid during authoring** (skill DAG rule): ADR-0027
  (Tier 1) may NOT forward-reference ADR-0026's body; the inbound `depends-on (from ADR-0026)` row is
  recorded in THIS dag.md §2 and backfilled into ADR-0027 once ADR-0026 lands. ADR-0026 (Tier 2) may
  reference ADR-0027 (already authored + validated).
- **The §3 inverse-backfill roster is mandatory at FINAL FIX:** append the 9 inverse rows into
  0022 / 0020 / 0015 (×2) / 0001 / 0005 / 0016 / 0006 / 0023 / 0024, AND the ADR-0022 Revision-History
  amendment note (§4). The cross-reference authority for the live-wiring set is THIS file
  (`docs/adr/.pipeline/live-wiring/dag.md §2`).
- **The 2 Pending tensions (§6) become prerequisite build tasks:** the raw-PII-leak probe + the
  key-never-committed scan + the fail-closed-on-live-error test MUST pass against the LIVE backend
  BEFORE ADR-0027 implements (the dim-10 floor).
- **Extend-not-rebuild is a hard grounding fact** (HANDOFF S93 "Files I will NOT touch"): both new
  ADRs WRAP the built engine — ADR-0027 fills `_ClaudeNoTrainBackend.deidentify` against the existing
  `ModelClient.deidentify` seam + `deid_in`; ADR-0026 wires the existing `run_orchestrated` /
  `dispatch` / `gate_dispatch` seams + the built `quality_judge` / `review_plan` callables. State it
  explicitly so the build phase does not re-author the orchestrator, the seams, or the gate callables.
- **The core-capability-audit repoint** (discovery #4) rides ADR-0026's Validation Approach as a
  confirmation criterion (the audit's `CALLER` pin + grep/self-test targets move onto the A′ Python
  SPINE — `plan_orchestrator.py` / the new shared driver, NOT `generate_plan.py`), NOT a new ADR.
  NOTE (RT-01/RT-02 coherence): the repoint is NOT a pure mechanical relabel and `run_orchestrated` is
  NOT byte-frozen — ADR-0026 resolves both as Open Questions (OQ-1: the no-fork loop is a
  behavior-preserving control-inversion REFACTOR of the S92-authored `run_orchestrated` WRAPPER, the
  byte-frozen constraint being the INNER ENGINE only; OQ-4: the audit STRUCTURALLY + BEHAVIORALLY
  asserts the deterministic spine is wired but CANNOT assert the live skill-driven subscription
  dispatch, which is the S94 operator-present LIVE-test attestation). The authoritative resolution
  lives in ADR-0026's OQ-1/OQ-4 + Validation Approach; this is the brief pointer, not the resolution.
