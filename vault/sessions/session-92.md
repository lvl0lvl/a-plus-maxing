---
title: Session 92 — the plan-generation engine, designed + built end-to-end via the full autonomous build pipeline
type: session
date: 2026-06-24
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-92
---

# Session 92 — the plan-generation engine (full autonomous build pipeline)

**Shape:** the operator directed running the FULL autonomous build pipeline to design + build the plan-generation engine end-to-end (`/create-adr` → `/create-spec` → `/create-build-plan` → `/create-task-plan` → `/execute-plan`), with extra-engaged monitoring (the pipeline is the live reference model for how the health-plan pipeline gets organized) + beading new-skill/command rough edges. Continuous, autonomous; all mock/fixture-tested (0 live-API spend). 8 PRs merged.

## What was built — the engine (main @ `a47c664`)

The plan-generation engine, end-to-end, mirroring the operator's S91 architecture (a multi-agent pipeline with the health specialists as agents):

- **de-id IN** — `scripts/plan/deid_in.py` + a new `ModelClient.deidentify(raw)->summary` method: a model-backed de-identification boundary, fail-closed, with a `SUMMARY_FIELD_SET` whitelist (raw PII never past the boundary).
- **the orchestrator** — `scripts/plan/plan_orchestrator.py` `run_orchestrated`: the programmatic subscription orchestrator (superseding the S68 interactive-session runtime), the bounded revise loop that composes the gates, wrapping the existing inner engine unchanged.
- **the gates** — `scripts/plan/quality_judge.py` (post-assembly plan-quality judge; structural auto-fails run regardless of the model's scores → no rubber-stamp) ∥ `scripts/plan/safety_review.py` (multi-agent whole-plan safety review wrapping the per-finding adjudicate gate; catches emergent cross-domain issues).
- **the cap** — `scripts/plan/dispatch_budget.py`: a configurable fail-closed dispatch cap.
- **de-id OUT** — `scripts/plan/reinsert_out.py`: DETERMINISTIC PII re-insertion (model off the OUT path), gitignored-only + realpath-containment.
- **maintained output** — `scripts/generate/maintained.py`: the unified maintained HTML, store-mediated, render-then-fill.
- **the scan-scope fix** — `.claude/hooks/lib/pii-scan-scope.sh`: `vault/artifacts/generated/` added to `DATA_BEARING_PREFIXES` so a re-inserted name is denied at commit + pre-push.

The keystone (Wave 4) is the **fail-closed bounded revise loop**: `safety_passed is True` is the ONLY surface path; safety is checked first (terminal); a quality REVISE re-dispatches via the orchestrator's `dispatch` seam (not the `reauthor` energy-bounce hook); bounded N=3 → honest-no-plan; INV-CRITICAL-NON-OVERRIDABLE holds; **scratch-and-promote** keeps the real store clean on any block. Full runtime-stage-order E2E proven on synthetic fixtures.

## The pipeline (8 PRs)

| Stage | PR | merged |
|-------|----|--------|
| `/create-adr` — ADRs 0020–0025 (8-phase; judge ≥9/dim + a 10th PII-boundary dim; red-teamed) | #238 | `293d930` |
| `/create-spec` — engine spec (11/11 judge, live-repo-grounding re-measured) | #239 | `0cdaf08` |
| `/create-build-plan` — 4-wave plan (24/24 + judge 10/10) | #240 | `4cc0741` |
| Wave-1 prep (the de-id-seam fix + recipes) | #241 | `e30b677` |
| Wave 1 — PII envelope | #242 | `fdad236` |
| Wave 2 — orchestrator + outage + de-id-OUT | #243 | `9de123d` |
| Wave 3 — gates + cap + maintained output | #244 | `d99e219` |
| Wave 4 — keystone revise loop + E2E | #245 | `a47c664` |

## The layered review caught a real defect at every layer (the headline)

**Recipe-review (the design-defect gate, PRE-CODE):** the de-id-seam misnaming (ADR named `author` as the de-id seam, but `author` consumes an already-de-identified summary — W1); the tautological gate-idle-seam trap (W2 spied a not-yet-built seam); the convergent gate-wiring-ownership conflict (W3 — Architect binding: 0022-T2/Wave-4 owns the invocation); the 2 HIGH fail-open safety paths (W4 — ambiguous-verdict default-allow + no-op-gate-surfaces-unreviewed).

**6-agent `/review-pr` (PRE-MERGE), independence INTACT (profile-less blind-triage + EXECUTED blind-verify):** the crown-jewel field-set-whitelist leak (W1 — `deid_in` only checked `isinstance(dict)`, dropping the whitelist the persisted path enforces; empirically reproduced); the silently-defeated quality gate (W3 — scored `sections` but the real `run_generation` result has no `sections` key → the rubber-stamping floor no-ops); the 2 fail-closed-completeness gaps (W4 — a promote-OSError + an unknown-revise-domain KeyError escaped the loop uncaught). All mutation-proven + executed-blind-verified before merge.

The convergent multi-agent findings (3 reviewers independently on the W3 gate-wiring + the W4 fail-open paths) are the pipeline working as designed.

## Two refinements that improve on the literal brief (both adopted under "more rigorous path")

1. The de-id OUT re-insertion is **deterministic** (model off the OUT PII path; the model's adaptive role lives in the maintained-format step) — a safer crown-jewel posture than literal model-backed re-insertion.
2. The de-id IN seam is a **new `ModelClient.deidentify` method**, not the `author` seam (`author` can't de-identify raw).

## State at close

- pytest **1611 passed / 2 skipped**; governance floor 15/0; EXTEND-NOT-REBUILD held every wave (the S70–S91 inner engine byte-unchanged; the engine WRAPS it). 0 live-API spend; 0 real operator PII in the test tree.
- **`run_orchestrated` has no production caller yet** (bead `71s4`; core-capability-audit still pins `generate_plan.py`) — the LIVE run (real backends + operator data) is the operator-present next step.
- **One new PF — PF-S92-01** (stopped mid-autonomous-loop to ask a false binary; operator-corrected; recurrence ≥5 of the autonomous-loop-violation class; captured PF + bead `gnko` + harvest).
- New beads: `gnko`, the `.pipeline/`-namespace-collision + `/run-pipeline`-fresh-start-rigor-mismatch (skill rough edges), the 2 SEC-01 ADR-0025-T1 caller-preconditions.

## Next (S93)

Wire `run_orchestrated` to a production front door (bead `71s4`; pass a real composed `gate_dispatch`; repoint `core-capability-audit.sh`); light the live `ModelClient` backends + the operator-present LIVE run; reconcile the stale plan-gen docs to the built programmatic orchestrator; the chat-elicitation wiring (`f0gh`).
