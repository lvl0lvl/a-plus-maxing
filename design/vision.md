---
title: Product Vision — a-plus-maxing
type: vision
status: active
created: 2026-06-03
last_reviewed: 2026-06-10
review_cadence: every-5-sessions
permalink: a-plus-maxing/design/vision
---

# Product Vision — a-plus-maxing

## What it is

**a-plus-maxing is a source-grounded health-intelligence system that helps an operator build physician-ready health plans from vetted research and their own private data, and track the progress and outcomes of those plans over time — without that private data ever being retained by, or used to train, the model that reasons over it.**

It pairs a goal-agnostic, gated knowledge wiki (compounds, biomarkers, protocols — each entry source-grounded and provenance-checked) with a roster of specialist agents that personalize against the operator's real data (labs, DNA, current state, goals). The operator owns the plans; the system closes the loop — **plan → act → measure → adjust** — tracking interventions, biomarkers, and outcomes over time so each plan, and each physician conversation, is backed by what actually happened.

### Physician-ready, defined

The operator authors and owns the plans; the physician is the collaborator they are **shared with, validated against, and refined with** (lab orders, prescriptions, clinical judgment) — not the author or addressee. A plan is *physician-ready* when:

1. **Sourced** — every recommendation traces to primary evidence, evidence-graded (the wiki's tiers); a clinician can verify, not take it on faith.
2. **Safety-surfaced** — contraindications, interactions, and the biomarkers they imply monitoring are explicit and up front.
3. **Honestly uncertain** — confidence tiers shown; animal/in-vitro evidence flagged (population-mismatch discipline); no overclaiming.
4. **Decision-framed** — states what the operator is doing/considering and the specific asks of the physician.
5. **Clinician-legible** — structured and skimmable for a time-constrained doctor; backed by tracked progress data.

It is NOT a diagnosis, a prescription, or a substitute for clinical judgment.

## Who it is for

- **V1 (now) — single operator, distributed to alpha testers.** Walter is the first operator: he **builds his own plans** with the specialist roster + the gated wiki, tracks progress and outcomes over time, and **shares + refines them with his physician** (validation, lab orders, prescriptions; first physician touchpoint: the July 2026 visit, LM-01). **V1 is also shared with others to alpha-test it** — each alpha tester `git clone`s the repository into their own fully independent local instance and fills it with *their own* data. This is the load-bearing reason the trunk must carry **zero operator PII**: the shared artifact is cloned by real people, so no operator's personal data (contact details, name on data-bearing paths, health data) may live in tracked source or git history. The operator-agnostic clonable distribution (ADR-0005) and the PII boundary (ADR-0001; the registered commit hook + pre-push backstop) exist precisely to make this safe.
- **North Star (later) — a product for general practitioners.** The same engine, extended so a GP can track and interact with *their patients* — each patient's data isolated, the output a clinician-facing plan/report surface.

## The V1 / North-Star boundary (load-bearing)

V1 and the product are the *same engine* at *different scale and trust models*. The boundary is deliberate and must not blur:

| | V1 (single-operator) | North Star (GP product) |
|---|---|---|
| Users | Walter + his doctor | GPs + their patients (multi-tenant) |
| Data | Walter's own PII | Other people's PHI (regulated) |
| Interface | Self-contained HTML plans/reports, opened locally | Hosted surface with per-account login |
| PII trust | Threat-model B; individual commercial API (no-train, 30-day) | HIPAA + Anthropic BAA + per-tenant isolation |
| Build now? | Yes | No — architected-for, not built |

**V1 must not prematurely build multi-tenant infrastructure, hosting, or accounts.** The first deliverable is a single-operator HTML artifact a physician can read (LM-04 is still unstarted). The product scale is the North Star that *constrains V1's architecture* (don't foreclose it) but is an explicitly later milestone.

## Enduring principles (true across V1 and the product)

1. **Source-grounded, gated knowledge.** The wiki is canonical, vetted, goal-agnostic; every entry passes the ingestion gate (provenance + structure, `INV-WIKI-INGESTION-GATED`). Personalization happens at dispatch, never by corrupting the library.
2. **PII trust boundary.** The operator's private data may be *transiently processed* by the model but is **never retained by Anthropic and never used for training** (threat-model B). V1 achieves this with an individual commercial-API (no-train, 30-day) profile for PII-bearing dispatch and the subscription for PII-free library work. The GP product raises this to HIPAA + a Business Associate Agreement + per-tenant isolation — a documented upgrade, not a V1 burden.
3. **Physician-credible output.** The deliverable is a plan/report a doctor can act on: claims sourced, risks surfaced, contraindications mapped. The system informs a clinical relationship; it does not replace one.
4. **Compounding rigor.** The project runs the Rigor Framework (session lifecycle, invariants-get-scripts, mechanical gates, failure-mode discipline). Product work flows through the PRD → ADR → spec → build-plan → task-plan → execute pipeline.
5. **Closed-loop outcome tracking.** The system is a longitudinal record, not a one-shot generator: it tracks interventions, biomarkers, and outcomes over time and feeds them back into the next plan and the next physician conversation. Progress and attribution — "did X move Y?" — are first-class.

## What this is NOT

- Not a consumer wellness/biohacking app — output is physician-facing and evidence-graded.
- Not a substitute for medical care — it produces material *for* a doctor, not diagnoses.
- Not multi-tenant in V1 — one operator, local artifacts.
- Not a system that ships private data into model training or open-ended retention — ever.

## Trajectory

V1 = the single-operator engine + outcome tracking + a simple HTML report/plan surface + the PII controls. The product phase adds multi-tenancy, hosting, accounts, and the regulated-PHI trust model. The PRD (S24) defines V1 concretely; subsequent ADRs / specs / build-plans detail it.

## Cross-references

- `HANDOFF.md` — S24 scope contract (this pivot)
- `INVARIANTS.md` — `INV-WIKI-INGESTION-GATED`, `INV-RESEARCH-PROVENANCE-DISJOINT` (the gated-knowledge principle)
- `bd show hil` — the PII trust-boundary decision (threat-model B), formal ADR pending the pipeline's ADR phase
- `vault/meta/landmarks.md` — LM-01 (MD visit, first consumer), LM-04 (first HTML artifact)
- `.claude/agents/genetics-specialist/` — genetic-exceptionalism / privacy floor (ties into the PII boundary)
- `vault/decisions/2026-05-16-system-architecture.md` — **partially superseded by this pivot.** That ADR's original decisions ("LLM-driven agent, *not* a tracker"; "no diet app"; defer a custom interface to phase C until friction-log evidence) are reversed by the Walter-directed product trajectory here. Formal supersession ADR pending at the ADR stage (`bd show fm4`).
