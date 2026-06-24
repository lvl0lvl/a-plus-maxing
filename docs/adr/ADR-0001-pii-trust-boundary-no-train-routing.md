## ADR-0001: No-Train PII Trust-Boundary Routing and Guard (Threat-Model B)

> **Y-Statement:** In the context of a local-first single-operator health system reasoning over the operator's labs, DNA, and health history, facing the fact that Claude Code agents transmit their context to the Anthropic API while V1 forbids that private data from being retained or used to train the model, we decided to adopt threat-model B — keep store, ingestion, and generation local, route only plan reasoning to the model over summaries on a no-train, non-retained commercial API path, and write zero operator PII to any tracked file — to achieve a transient-processing-only PII boundary without HIPAA/BAA infrastructure, accepting bounded (not zero) retention, two mechanically separate API paths, and reasoning over summaries rather than raw PII.

```yaml
id: ADR-0001
title: "No-Train PII Trust-Boundary Routing and Guard"
status: accepted
date: 2026-06-03
decision-makers: [Walter McGivney]
tags: [pii, trust-boundary, privacy, routing, foundation]
```

### Context

The system reasons over the operator's private health data — labs, DNA, the January-2026 issue, medications, profile, goals, and current state — to produce a personalized multi-domain plan ([PRD-v1, US-9, L111-117](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]). A hard technical fact constrains that reasoning: Claude Code agents run by sending their context to the Anthropic API, so anything an agent reads is transmitted to a vendor (`bd show hil`, description [VERIFIED]). The system cannot both reason over PII and keep that PII off the model — unless the architecture separates *what the model reasons over* from *where PII lives*.

Two forces pull against each other. The vision commits, as a load-bearing principle, that the operator's private data "may be transiently processed by the model but is never retained by Anthropic and never used for training" ([vision.md, L15, L52-53](../../design/vision.md) [VERIFIED]). Against that, V1 must stay a clonable, single-operator, local capability with no HIPAA controls, no Business Associate Agreement, and no per-tenant isolation — the North-Star ceiling, deferred ([PRD-v1, NG-2 L278, NG-9 L285](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]; [vision.md, boundary table L40-48](../../design/vision.md) [VERIFIED]).

The tension extends past the operator. The data subject needs assurance their DNA and labs do not leak into training or open-ended retention. A second operator who clones the repository must inherit none of the first's PII ([PRD-v1, NFR-2 L231-236, Goal 3 L38-43](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]). The vendor's terms govern which path is permissible. And the build is constrained: this path is decided but unbuilt, the highest-risk dependency gating the personalized-plan deliverable for the July-2026 physician visit ([PRD-v1, A-6 L317-320, Dependencies row 1 L331](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).

### Decision

Adopt threat-model B for V1. The local time-series store, the import/ingestion routine, and dashboard/report generation run locally and model-independently, sending zero operator PII to any model. Only plan reasoning touches the model, over summaries rather than raw PII, on an individual commercial no-train, non-retained API path distinct from the consumer/subscription path used for PII-free library and research work. No operator PII is ever written to a tracked (committed) file.

### Rationale

Threat-model B was evaluated against four alternatives across four criteria — training exposure, retention exposure, V1 capability, and V1-fit (the no-HIPAA, clonable, local constraint) — and is the only option satisfying all four.

On **training exposure**, the commercial path is contractually exempt: Anthropic states "By default, we will not use your inputs or outputs from our commercial products (e.g. Claude for Work, Anthropic API...) to train our models" ([Anthropic privacy](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) [VERIFIED]) and the Commercial Terms state "Anthropic may not train models on Customer Content from Services" ([Anthropic Commercial Terms, §B](https://www.anthropic.com/legal/commercial-terms) [VERIFIED]) — the posture the vision records as the trust boundary's realization ([vision.md, principle 2 L52-53](../../design/vision.md) [VERIFIED]; `bd show hil`, notes [VERIFIED, settled in-session S24]). On **retention exposure**, the commercial path carries bounded retention, not zero; the project records "30-day" ([vision.md, boundary table L45](../../design/vision.md) [VENDOR-CLAIM]), but the precise window could not be confirmed against Anthropic's published policy this run, which directs retention specifics to the Trust Center and DPA ([Anthropic privacy](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) [UNVERIFIED: specific retention number]). On **V1 capability**, a full commercial model preserves the specialist reasoning the plan requires, which a local-only model could not match at V1. On **V1-fit**, the commercial path needs no BAA, no multi-tenant isolation, and no hosted surface — fitting the clonable single-operator constraint the regulated-PHI alternatives violate ([PRD-v1, NG-2 L278, NFR-3 L238-243](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).

The decision keeps ZDR, HIPAA, and the BAA as the documented North-Star ceiling, not a V1 burden — the boundary table records the GP product raising the trust model to "HIPAA + Anthropic BAA + per-tenant isolation" ([vision.md, L45, L53](../../design/vision.md) [VERIFIED]). Reversing it later (e.g., to a fully-local model) would force re-plumbing every data path, since the decision fixes which lane every dispatch runs on.

### Consequences

**Positive:**
- 100% of plan-reasoning dispatches over operator data are contractually exempt from training, eliminating training exposure for PII-bearing dispatch ([Anthropic Commercial Terms §B](https://www.anthropic.com/legal/commercial-terms) [VERIFIED]; [PRD-v1, NFR-1 AC L228](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- Store, ingestion, and generation emit 0 PII bytes to any model, so Goal 2 (the tracking loop) can ship before the plan-reasoning path is built ([PRD-v1, A-6 L320, NFR-1 AC L227](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- The PII-free/PII-bearing split makes library and research work (subscription path) fully separable from personalization, so the bulk of the system never touches the regulated lane ([PRD-v1, NFR-1 AC L229, US-9 AC L116](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).

**Negative:**
- Retention is bounded, not zero: PII sent for plan reasoning persists in vendor systems for a bounded window rather than being purged immediately; true zero-retention is deferred to the North Star, so V1 accepts a non-zero retention exposure ([vision.md, boundary table L45](../../design/vision.md) [VENDOR-CLAIM]; window [UNVERIFIED] this run).
- Split-path complexity is a permanent operational burden: the two API paths must be kept mechanically separate; a single mis-routed dispatch sends PII to a training-eligible path, and no enforcement mechanism is built yet (the highest-risk dependency, [PRD-v1, A-6 L317-320, OQ-1 L342](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- Summaries-not-raw is a standing discipline cost: it constrains how rich and operator-specific the model's input can be and requires a summarization step on every PII-touching dispatch ([PRD-v1, US-9 AC L115, NFR-1 L223](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- It constrains four downstream decisions (store, ingestion, generation, lab-flow) by eliminating any model-egress option, narrowing their design space ([dag.md §8 constraint-propagation](.pipeline/dag.md) [VERIFIED]).

**Neutral:**
- The commercial API becomes a V1 runtime dependency for plan reasoning specifically; the rest of the system stays vendor-independent.
- "Summary" becomes a shared contract the store/generation side and the plan-reasoning side must agree on.

### Alternatives Considered

#### Alternative A: Subscription / consumer-only path
Route all dispatches — including PII-bearing plan reasoning — through the single consumer/subscription path already used for library work.
- **Supporting evidence:** Operationally simplest — one path, nothing to mis-route. The subscription path is already in use for PII-free library and research work.
- **Trade-offs:** That path is training-eligible and carries longer retention, so it would route operator PII into a training-eligible lane — directly violating the vision's anchor principle and NFR-1 ([vision.md, L15, L52-53](../../design/vision.md) [VERIFIED]; [PRD-v1, NFR-1 L223](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]). Rejected because it fails the load-bearing privacy force entirely.
- **When this becomes the right choice:** Only if a future operator's data were not PII, or if the consumer terms changed to a no-train, bounded-retention posture matching the commercial path.

#### Alternative B: Zero-data-retention / Enterprise tier now
Adopt the enterprise zero-retention (ZDR) tier plus HIPAA controls and a BAA for V1, so PII processing is both no-train and zero-retention.
- **Supporting evidence:** Strictly stronger privacy than B — it closes the bounded-retention gap B accepts, and is the eventual North-Star target ([vision.md, boundary table L45](../../design/vision.md) [VERIFIED]).
- **Trade-offs:** ZDR/BAA/HIPAA is explicitly the North-Star ceiling and out of V1 scope; V1 is a single-operator clonable instance that must not build regulated-PHI infrastructure ([PRD-v1, NG-2 L278, NG-9 L285](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]; [vision.md, L46-48, L53](../../design/vision.md) [VERIFIED]). Whether ZDR is available outside an enterprise/special-arrangement tier could not be confirmed this run ([Anthropic privacy](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) [UNVERIFIED]). Rejected as scope violation, not as inferior privacy.
- **When this becomes the right choice:** At the North-Star transition to a multi-tenant GP product handling others' regulated PHI, where HIPAA + BAA + per-tenant isolation become mandatory.

#### Alternative C: Fully-local model only
Run a local open-weight model for plan reasoning so PII never leaves the machine and no vendor path is touched.
- **Supporting evidence:** Maximal privacy — zero training and zero retention exposure because nothing is transmitted; aligns with the no-egress posture of the store and generation layers.
- **Trade-offs:** A local model at V1 cannot match the specialist reasoning the multi-domain plan requires, and the specialist roster is built against the Anthropic-hosted model; switching would forfeit the physician-ready bar's reasoning depth and re-plumb the entire roster. The commercial-no-train upgrade is reversible; rebuilding on a local model is not, at V1 cost. Rejected because it sacrifices V1 capability to over-solve a force already satisfied.
- **When this becomes the right choice:** If local open-weight models reach parity for clinical-reasoning tasks AND hardware cost is acceptable, making the no-egress benefit free of a capability penalty.

#### Alternative D: No-model plan reasoning (deterministic templates only)
Produce the plan with deterministic local tooling and pre-written templates, applying operator PII via local code with no model reasoning over PII.
- **Supporting evidence:** Eliminates the PII-to-model question entirely — if the model never reasons over PII, no no-train path is needed; one of the candidate patterns the `hil` bead listed (local non-LLM tooling applying PII to model-produced templates) (`bd show hil`, description [VERIFIED]).
- **Trade-offs:** A template-filler cannot perform the multi-domain, evidence-graded, personalized reasoning a physician-ready plan requires (route each domain to a specialist, reason over the operator's situation, surface contraindications). It reduces the plan to mail-merge over fixed templates, failing Goal 1 and the physician-ready bar ([PRD-v1, Goal 1 L24-29, FR-1/FR-2 L123-136](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]; [vision.md, physician-ready bar L21-28](../../design/vision.md) [VERIFIED]). Rejected because it removes the capability the product exists to deliver.
- **When this becomes the right choice:** For the subset of generation that is genuinely deterministic (dashboards, the biomarker matrix, projections) — which indeed run model-independently under this decision. Rejected only as the path for *plan reasoning*.

### Related Decisions

| Decision | Relationship | Description |
|----------|-------------|-------------|
| [ADR-0002 (Local-First Time-Series Store Substrate)](ADR-0002-local-first-time-series-store.md) | constrains | Eliminates any store option with a hosted/egress surface; the store holds PII and must sit on the local/no-egress side. |
| [ADR-0003 (Source-Extensible Ingestion Interface)](ADR-0003-source-extensible-ingestion-interface.md) | constrains | Forbids any ingestion path that routes raw operator readings through a model step; ingestion writes only to the local store. |
| [ADR-0004 (On-Demand Single-File Artifact Generation)](ADR-0004-on-demand-single-file-artifact-generation.md) | constrains | Eliminates any generation design that ships PII to an external asset/CDN/server; forces local-only render. |
| [ADR-0007 (Lab-Loop / Biomarker-Matrix / Projection Data-Flow)](ADR-0007-lab-loop-biomarker-matrix-projection-data-flow.md) | constrains | Lab values and symptom answers are PII; forced onto the local-store side, off any model-egress projection step. |
| [ADR-0006 (Multi-Domain Plan Assembly via Roster Specialists)](ADR-0006-multi-domain-plan-assembly-via-roster.md) | is-prerequisite-of | Plan assembly is the PII-touching dispatch; it depends on this routing decision and cannot be authored until the lane is fixed. |
| [ADR-0005 (Operator-Agnostic Clonable PII-Free Trunk)](ADR-0005-operator-agnostic-clonable-pii-free-trunk.md) | complements | Two halves of the PII posture on orthogonal leak vectors: this decision keeps PII off the model; ADR-0005 keeps PII out of version-control history. Neither is a prerequisite. |
| [ADR-0013 (Operator-Started Loopback Intake Server)](ADR-0013-operator-started-loopback-intake-server.md) | constrains | ADR-0013's loopback-only, zero-egress posture realizes this decision's no-egress boundary on the new intake-server network surface. |
| [ADR-0014 (Web-Form Capture and Persistence of Operator Input)](ADR-0014-web-form-capture-operator-input-persistence.md) | constrains | ADR-0014's captured raw values stay off the model — they reach specialists only via `router.summarize`'s closed `SUMMARY_FIELD_SET` de-identification gate. |
| [ADR-0015 (Swappable No-Train Model Client)](ADR-0015-swappable-no-train-model-client.md) | amended-by | ADR-0015 adds the programmatic-client MECHANISM this ADR never specified, plus a SECOND model-touching path (the intake conversation) alongside "Only plan reasoning touches the model"; the no-train-lane routing and summaries-not-raw discipline for the store read survive unchanged. |
| [ADR-0016 (Intake-Conversation Egress Relaxation)](ADR-0016-intake-conversation-egress-relaxation.md) | amended-by | ADR-0016 scopes this ADR's zero-egress boundary so the live intake conversation may egress raw on the no-train lane while every persisted fact stays de-identified; it does not supersede wholesale — the store-side `summarize`/`dispatch` discipline is untouched. |
| [ADR-0020 (Model-Backed API De-Id Boundary — De-Id IN)](ADR-0020-model-backed-api-deid-boundary-in.md) | tensions-with | ADR-0020 routes raw plan-intake PII to the API BEFORE de-identification — the surface this ADR's summaries-not-raw falsification forbade. The boundary is defined in ADR-0020's Consequences; this ADR's persisted-side-de-identified invariant is honored (the boundary RELOCATES de-id, it does not remove the de-identified store). Inverse of ADR-0020 → 0001 `tensions-with` (engine dag.md §7). |
| [ADR-0021 (Deterministic PII Re-Insertion — De-Id OUT)](ADR-0021-pii-reinsertion-local-artifact-out.md) | relates | ADR-0021 is the OUT half of the crown-jewel relaxation, pairing with ADR-0020's IN half. This ADR's persisted-side-de-identified invariant is honored — re-insertion is render-time-only onto a gitignored artifact, off the persisted store. Inverse of ADR-0021 → 0001 `relates` (engine dag.md §7). |

Note on [2026-05-16-system-architecture.md](../../vault/decisions/2026-05-16-system-architecture.md): this ADR reframes the conversational-only threat posture that decision assumed ("LLM-driven agent, not a tracker"), but it is not a formal superseder of any specific 2026-05-16 decision — the threat-model-B boundary is a new decision, not a reversal of one. The formal supersession of 2026-05-16 is carried by ADR-0002, ADR-0004, and ADR-0006 per the discovery Supersession map; it is therefore a prose reframing note here, not a Related Decisions edge.

Cross-reference authority: [.pipeline/dag.md §6](.pipeline/dag.md) is the canonical bidirectional reference map for the V1-DAG edges above.

### Validation Approach

**Confirmation criteria:**
- During an ingestion run and a generation run, 0 PII bytes from the store leave the local machine — verified by a network-egress check (expected: 0 outbound calls carrying store content) ([PRD-v1, NFR-1 AC L227](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- 100% of operator-data dispatches run on the no-train commercial path over summaries, 0% on a training-eligible path — verified by routing inspection of every PII-touching dispatch ([PRD-v1, NFR-1 AC L228](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).
- A content scan of all tracked files for operator PII tokens returns 0 hits on a fresh clone ([PRD-v1, NFR-2 AC L235](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]).

**Falsification criteria:**
- ≥1 PII byte observed leaving the machine to a training-eligible (subscription/consumer) path means the routing guard failed; halt PII-bearing generation and repair the routing split.
- ≥1 plan-reasoning dispatch sending raw (non-summary) PII to the model means the summaries-not-raw discipline failed; block the path and re-introduce summarization.
- ≥1 operator-PII hit in git history on a fresh-clone scan over any release means the no-committed-PII guarantee failed; history cannot be cleanly scrubbed, so treat as a release-blocking incident (also a D6 concern).
- Time horizon: re-run all three checks at every release and before the July-2026 physician-visit deliverable ships.

**Review triggers:**
- A change to Anthropic's commercial-API no-train terms or retention policy (re-verify the [VERIFIED] no-train claim and [UNVERIFIED] retention window).
- The first enforcement mechanism (OQ-1) lands — re-validate that routing is mechanically, not manually, enforced.
- The North-Star transition is initiated — threat-model B is superseded by HIPAA + BAA + per-tenant isolation.
- A second operator clones the repository (re-run the tracked-file PII scan on the fresh clone).

### Open Questions

| # | Question | Owner | Target Date | Impact on This Decision |
|---|----------|-------|-------------|------------------------|
| OQ-1 | What is the concrete enforcement-mechanism shape — which plan-reasoning dispatches route to the PII no-train path, and how is the PII-free/PII-bearing split mechanically (not manually) enforced so a dispatch cannot be mis-routed? | Walter McGivney | 2026-06-30 | Resolved downstream by the enforcement build; shapes how NFR-1/FR-2 are realized but does not change the decision. Until resolved, the split-path complexity negative consequence stands unmitigated by mechanism. ([PRD-v1, OQ-1 L342](../prd/PRD-v1-local-first-health-tracking-planning.md) [VERIFIED]) |
| OQ-2 | What is the precise commercial-API retention window, and is true zero-retention (ZDR) available outside an enterprise/special-arrangement tier? | Walter McGivney | 2026-06-30 | Sets the exact size of the accepted bounded-retention exposure; could not be confirmed against published Anthropic policy this run ([UNVERIFIED]). Does not change the decision (B accepts bounded retention), but quantifies the negative consequence. |

### Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-06-03 | Initial draft (v1.0) — accepted | Walter McGivney |
| 2026-06-23 | Added inverse edge(s) to ADR-0020 (tensions-with) and ADR-0021 (relates) (plan-generation engine set, S92 backfill). | Walter McGivney |
| 2026-06-04 | v1.1 — backfilled cross-references to the completed ADR set. | Walter McGivney |
| 2026-06-04 | v1.2 — Phase-8 red-team fixes (RT-01). | Walter McGivney |
| 2026-06-21 | v1.3 — Phase-5 verify: added inverse `constrains` edges to ADR-0013 (intake-server no-egress surface) and ADR-0014 (capture stays off the model). | Walter McGivney |
| 2026-06-22 | v1.4 — Phase-8 backfill: inverse `amended-by` edges to the conversational-intake set (ADR-0015 programmatic-client mechanism + second model-touching path; ADR-0016 egress scoping). | Walter McGivney |
