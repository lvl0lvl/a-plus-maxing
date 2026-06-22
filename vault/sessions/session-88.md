---
title: Session 88 — the conversational-intake foundation (ADR-0015–0019 + design + vision)
type: session
date: 2026-06-22
owner: Walter McGivney
status: complete
---

# Session 88 — conversational-intake foundation (autonomous)

**Shape:** the first AUTONOMOUS session — set up at the S87 close, it wrote + self-confirmed its own scope contract and drove continuously through the pipeline (ADR → vision → design → review → merge → close) without pausing for operator status, per the operator's standing directive (2026-06-22). The deliverable: the architectural FOUNDATION for the S87 conversational-intake pivot. The BUILD is S89+.

## What happened

1. **The ADR set (0015–0019) via the full `/create-adr` pipeline.** Discovery → rubric → DAG (acyclic, 4 tiers) → tier-by-tier author/verify/judge (all 5 judged ACCEPT) → whole-set red-team → final-fix → final-verify `OVERALL: PASS`. The 5 ADRs:
   - **0015** — a swappable no-train model client, the codebase's FIRST programmatic model client (default: a Claude no-train API, swappable for the local-model North Star); fail-closed on model-call failure; closes the core-capability gap (no model client existed — `rg` over `scripts/` confirmed zero, and the plan-author was a captured *agent* output, not a programmatic call).
   - **0016** — scoped relaxation of ADR-0001's zero-egress crown-jewel boundary: the raw *live* intake conversation egresses to the no-train API; everything persisted + committed stays de-identified. Operator-signed-off.
   - **0017** — the conversation→de-identified-store extraction contract, "model proposes, gate disposes": the model's extraction output passes through `capture`'s value gates before any store write.
   - **0018** — split intake into an objective form (demographics + content uploads) and a conversational agent (the rich sections); the kept demographic layer is activated so the 4 orphan tokens get working inputs.
   - **0019** — extend the closed `SUMMARY_FIELD_SET` so chat-sourced nutrition/supplement/peptide/training facts reach the planner. **ADDED autonomously during discovery** as the "most robust path" call — without it the pivot recreates the exact PF-S87-01 gap (rich capture that never feeds the plan).
   Plus a **16-edge inverse backfill** into 6 existing ADRs (0001/0002/0005/0006/0013/0014), append-only, no accepted Decision mutated.

2. **The vision update** (`design/vision.md`) — first sentence + PII-boundary principle + trajectory + cross-refs to the conversational direction; the rigid-form direction superseded with pointers. Corrected twice for PII-boundary precision after the design review.

3. **The design pass** (`vault/design/conversational-intake-design.md`) — an architect-authored interface-contract design (question strategy, chat transport, extraction mechanism, PII flow), grounded against the live planner/capture/store code, the crown-jewel boundary stated PER-PATH. An **independent adversarial critique** caught a Critical the create-adr pipeline missed: the `summarize` 8j6 PII gate runs only on the pass-through token path, NOT the raw-backed-derived path — so the new ADR-0019 tokens are de-identified by their derivation's coarseness (proven by a per-token output scan, now a spec acceptance criterion), not the gate. Corrected in the design doc + ADR-0019 + ADR-0017.

4. **`/review-pr` (3-agent docs subset) → `/merge`.** PR #216; 4 Suggestion findings (2 missing inverse edges, 16 broken citation paths, 1 un-annotated egress criterion), all blind-triaged LEGITIMATE → fixed → blind-verified RESOLVED. Rebase-merged → `main` @ `6d1d85f` (REST throughout; GraphQL exhausted). The `block-commit-main` worktree false-block was handled (twice) via the park-the-main-checkout maneuver, the operator's WIP verified byte-identical each time.

## PF this session

No new PF. The layered review system worked as designed — each independent gate (create-adr pipeline → adversarial design review → `/review-pr`) caught what the prior missed, all before merge, 0 reaching the operator. The defining positive: choosing to run the adversarial design review (rather than fold it into the PR review) caught a real behavioral inaccuracy in the crown-jewel boundary description. Full attestation + skill-trace + disclosure ledger in `memory/process-failures.md` Session 88.

## Next (S89 — the build)

Build the conversational intake agent via the V1 pipeline (spec → build-plan → task-plan → `/execute-plan` + 3-tier review). Per PF-S87-01 the acceptance MUST verify END-TO-END capability (a usable plan), not just chat plumbing. First surface the foundation for operator review (the autonomously-added ADR-0019 + the fail-closed contract + the no-train provider default). The spec carries the deferred design-stage requirements (`docs/adr/.pipeline/design-review.md` + design doc §7): the per-token coarseness proof; the `identity_config` wiring (H-2); CONCERN-1/2; M-3.
