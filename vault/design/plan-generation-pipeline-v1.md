---
title: Plan-Generation Pipeline v1 — topology, tiers, and ordering (design spec for 71s4)
type: design
status: approved
owner: walter
created: 2026-06-16
last_reviewed: 2026-06-19
review_cadence: phase
permalink: a-plus-maxing/design/plan-generation-pipeline-v1
---

# Plan-Generation Pipeline v1

**What this is:** the approved design spec for the plan-generation orchestration layer (bead `71s4`) — the target topology, with the **Build status** section below the live tracker of what is wired. As of S76 the layer is substantially built: the four plan-domain authors (S70–S71), the step-4 orchestrator reconciler (S72), the supplement↔peptide additive-AE screen (S73), the medical-liaison terminal adjudication gate for the held additive-AE finding (S74), the author-conflict adjudication (`cfaj`, S75), and the supplement↔Rx BPMH axis (`rxbp`, S76) all run through the production path (`scripts/plan/{generate_plan,orchestrate,adjudicate,router}.py`), mechanically guarded by `scripts/core-capability-audit.sh` (INV-CORE-CAPABILITY). What remains is runtime A's interactive-dispatch convenience surface (`/generate-plan`), the doctor-visit-queue/SBAR handout artifact, and the measure/adjust legs. The earlier "unbuilt / no production caller" framing held only through S68 (PF-S63-02 — the drift this build closed).

**Provenance (how the order + tiers were derived, not guessed):** the `plan-pipeline-order` multi-agent workflow (S68, run `wf_eda67138-e95`). 16 specialists each elicited their own input/output dependencies + tier self-classification → the health-specialist-architect synthesized a dependency DAG → 6 adversarial reviewers (the 4 planners + medical-safety-reviewer + architect) tried to break it → a reconcile pass produced the final. The adversarial pass **rejected the first synthesis's fabricated edge-provenance** (it had claimed specialists "self-reported" ordering metadata that did not exist) and forced every edge to be re-derived from `vault/WIKI.md` Reads/Owns contracts: an edge X→Y holds iff Y *Reads* an entity-class X *Owns*. Final confidence: high.

## Runtime model (operator decision, S68)

Plan generation runs as an **interactive Claude-Code / agent-dispatch session**, not a standalone API client. The orchestrator dispatches specialists against the wiki + the de-identified `router.summarize` summary, composes via `assemble`, writes the store via `record_plan`, and renders via `generate.run`. The no-train PII guarantee rides two things, not an API client: (a) the session runs under the no-train commercial-API profile (threat-model B), and (b) `summarize`'s 0-raw-PII de-identification + `dispatch`'s whitelist gate as in-code defense-in-depth. A standalone `scripts/` API client is a later North-Star option the seam must not foreclose.

## The five decisions (operator-confirmed, S68)

1. **3-tier roster model** (not 2-tier) — classify every specialist by what it OWNS (see Tier model below). Flattening the protocol/parameter authors into "advisors" would discard the content surface the dashboard's per-specialist drill-down + chat depends on.
2. **No 5th plan domain yet** — the 3-tier model already gives sleep-coach (and the other protocol-authors) a stored protocol surface + a dashboard card without a 5th `plan_schema` PLAN_DOMAINS slot. A 5th domain is an ADR-0010 one-way door; defer until the protocol-author tier exists and the need is demonstrated.
3. **Clearance hard-gate (conservative)** — the workout author ships a useful *deferred* state (coaching from established science, no load prescription) until a real clinician clearance arrives; the **July 13 visit (LM-01) is that unlock**. No biomarker-derived self-clearance shipping a provisional load prescription (the operator's documented health-issue recovery context makes the downside asymmetric).
4. **Distinct orchestrator reconciler** — the step-4 "find overlaps/contradictions, bounce plans back, integrate" job is the orchestrator's (the `/generate-plan` main agent wrapping `assemble`), kept separate from medical-liaison's clinical safety adjudication. Two terminal functions, not one.
5. **Minimal end-to-end path first** — build a single vertical slice that proves the loop, then grow to the full topology (see Build sequence). The first slice IS the PF-S63-02 core-capability proof.

## Tier model

- **Plan-domain authors (4)** — own a `plan_schema` PLAN_DOMAINS slot, mechanically forced by `assemble()`'s domain routing:
  - `personal-trainer` → workout · `nutritionist` → nutrition · `supplement-specialist` → supplements · `peptide-specialist` → peptides.
  - They also vet incoming info (operator-confirmed).
- **Protocol / parameter authors (~7)** — own a `protocols/*`, `parameters`, or `compounds` write surface but NO PLAN_DOMAINS slot: `sleep-coach`, `recovery-specialist`, `cardiovascular-specialist`, `endocrine-specialist`, `gi-specialist`, `dermatologist`, `longevity-strategist` (plus `genetics-specialist` PGx annotation). Their content threads into the 4 plan sections as advisory input AND surfaces as their own dashboard card + drill-down/chat.
- **Pure collate (1)** — `medical-liaison`: collates Rx / BPMH / contraindications + the doctor-visit queue; authors no content of its own.

## Ordered pipeline (the derived DAG)

| Phase | Who | What |
|---|---|---|
| **−1 Precondition gate** | (no agent) | Pipeline cannot start until intake has ingested documents AND hard-limit / contraindication fields are populated-or-explicitly-UNKNOWN. An empty field = UNKNOWN, fails closed (mirrors `assemble()`'s HALT_INDETERMINATE), never silently "no contraindication." |
| **0 Ingestion (parallel)** | labs, cardiovascular, endocrine, gi, lymphatic, dermatologist, genetics, sleep-coach, **medical-liaison (early: Rx/clearance queue)** | All read intake substrate; none reads another's *output* → one parallel constraint-supply layer. Each emits a constraint/contraindication surface — NOT a clinical clearance (clearance is a clinician decision the liaison coordinates). labs owns biomarkers (feeds every biomarker-reader). |
| **0.5 Critical-floor screen** | nutritionist (owned, non-overridable) | Fail-safe RED-S / LEA / disordered-eating screen BEFORE any energy-prescribing author. If tripped, short-circuits all energy-deficit content (workout AND nutrition) to clinical-care routing. |
| **1 Workout author** | personal-trainer | First plan domain. **Clearance-conditional**: ACTIVE/UNKNOWN contraindication status → deferred/empty-state coaching plan, no load prescription; full prescription gated on the clinician clearance via the liaison's queue. |
| **2 Nutrition author + recovery advisor** | nutritionist, recovery-specialist | Nutrition consumes the workout plan's energy-expenditure to set its *owned* protein/energy targets, and may BOUNCE the workout plan if the energy budget can't sustain the load (joint constraint). Recovery emits monitoring markers (empty-wearable-state until Whoop lands). |
| **3 Compound band** | peptide + supplement (+ longevity, mental-performance cross-read) | Peptide & supplement DRAFT → **joint two-pass mutual interaction/additive-AE screen** (bidirectional, not a one-way dedupe) → finalize. Supplements finalize last, against the whole settled compound surface + the Rx list. No downstream output may raise a peptide evidence grade. |
| **4 Terminal adjudication** | medical-liaison (late) | Collates the doctor-visit queue (populated incrementally by every `risk_tier:medium+` write, not a single terminal pull) + every risk HALT, runs BPMH reconciliation, adjudicates blocks before operator approval. The step-4 safety gate. |

The step-4 *integration/reconciliation* (overlaps, contradictions, plan-bounce) is the **orchestrator's** job, distinct from this medical-liaison safety adjudication.

## Build sequence (minimal-path-first)

1. **Slice 1 — core-capability proof:** intake → `summarize` → `personal-trainer` (workout, clearance-conditional) → `assemble` (1 domain) → `record_plan` → dashboard + review/approve. Lands the mechanical core-capability gate (asserts the path is wired).
2. **+ nutrition** — the one real build edge (workout energy-expenditure → nutrition targets).
3. **+ compound band** — peptide/supplement two-pass mutual screen.
4. **+ Phase-0 ingestion / advisory layer** — the protocol/parameter authors + monitoring markers.
5. **+ step-4 reconciler** (orchestrator, with plan-bounce) **+ medical-liaison terminal safety gate.**

**Build status:** Slice 1 WIRED (S70, workout); slices 2–3 single-author translators WIRED (S71, nutrition/supplements/peptides). The step-4 **orchestrator reconciler** is WIRED (S72, `scripts/plan/orchestrate.py`): the nutrition→workout energy bounce (Phase 2), the RED-S/LEA cross-domain short-circuit (Phase 0.5), and cross-domain overlap/conflict DETECTION. The **supplement↔peptide two-pass additive-AE screen** (slice-3 compound-band, Phase 3) is WIRED (S73): a shared author-declared additive-AE class or a pairwise interaction holds the supplement before recording, bidirectional, verified E2E over real supplement-specialist + peptide-specialist dispatches. The **medical-liaison terminal adjudication gate** (Phase 4) for the held additive-AE finding is WIRED (S74, `scripts/plan/adjudicate.py`): the deployed medical-liaison adjudicates the held finding into a content-validated override record (HIGH/MEDIUM → the hold releases and the supplement records) or a non-overridable auto-block (CRITICAL / H1-H2 → the block stands), enforcing INV-OVERRIDE-RECORD-SCHEMA + INV-CRITICAL-NON-OVERRIDABLE; verified E2E over real medical-liaison dispatches (an informed-refusal override clears the hold; a vacuous override is refused → block stands). The **author-conflict adjudication** (`cfaj`) is WIRED (S75, `scripts/plan/orchestrate.py`): an author-declared cross-domain conflict (`report["conflicts"]`) HOLDS the declaring (`from`) domain by default and routes it through the SAME gate (`adjudicate`) — a content-valid override releases it, a non-overridable / invalid adjudication holds it. The conflict hold is tracked INDEPENDENTLY of the other holds (a domain can carry both an additive-AE/bounce/RED-S-LEA hold AND a conflict, each cleared on its own — clearing one never releases a domain whose other concern is open); verified E2E over a real medical-liaison conflict dispatch. The **supplement↔Rx BPMH axis** (`rxbp`) is WIRED (S76, `scripts/plan/{router,orchestrate}.py`): the operator's PRESENT medication interaction classes are read de-identified through the `router.summarize` PII boundary (a new `rx-interaction-classes` field carrying operator/liaison-curated class tokens — never the raw drug names, which stay a named-excluded raw-PII class dropped at the boundary; no pharmacology DB enters `scripts/`), and a compound (supplement OR peptide) whose author-declared additive-AE class stacks against a present Rx-class is HELD in an INDEPENDENT `rx_bpmh_held` set and routed through the SAME gate (`adjudicate`). Verified E2E over real medical-liaison BPMH dispatches that genuinely DISCRIMINATE on the specific medication: aspirin + fish oil → HIGH/H3 overridable (clears via a content-valid informed-refusal override); warfarin + fish oil → CRITICAL/H2, the vitamin-K/warfarin watchlist, non-overridable auto-block (the block stands, the informed-refusal does not lower the band). The **remaining Phase-4 surface** REUSES this gate and is the beaded follow-on: the doctor-visit-queue collation + SBAR handout. Until it lands, the additive-AE screen + a conflict-declaring domain + a BPMH-matched compound HOLD unless the liaison gate clears them, and the OVERLAP output stays detect-only.

## Deferred to build-out

- 5th plan domain (sleep / recovery) — ADR-0010 one-way door; revisit once the protocol-author tier is built.
- The orchestrator reconciler's energy-bounce capability is BUILT (S72); the compound-band additive-AE screen is BUILT (S73); the medical-liaison terminal adjudication gate for the held additive-AE finding is BUILT (S74); the author-conflict adjudication (`cfaj`) is BUILT (S75); the supplement↔Rx BPMH axis (`rxbp`) is BUILT (S76). What remains deferred is the Phase-4 surface that REUSES the gate: the doctor-visit-queue/SBAR handout artifact (see Build status above).

## Cross-references

- `design/vision.md` — closed-loop principle (plan → act → measure → adjust)
- `docs/adr/ADR-0006-multi-domain-plan-assembly-via-roster.md` — `assemble` roster seam
- `docs/adr/ADR-0010-plan-content-schemas-plan-zone-render.md` — plan schema (4 domains; the 5th-domain review trigger)
- `docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md` — no-train boundary (`summarize`/`dispatch`)
- `vault/WIKI.md` — the Reads/Owns contracts the dependency edges are derived from
- bead `71s4` — the build of this pipeline + the mechanical core-capability gate
