---
title: Session 74 — medical-liaison terminal adjudication gate (Phase 4, the held-line closer)
type: session
status: complete
created: 2026-06-19
last_reviewed: 2026-06-19
permalink: a-plus-maxing/sessions/session-74
---

# Session 74 (2026-06-19)

## Goal

Wire the **medical-liaison terminal adjudication gate** (pipeline Phase 4, bead `71s4`) over the
reconciler's held supplement↔peptide additive-AE finding — the held-line closer. The operator
delegated the two scope judgment calls at session open ("do what makes the platform more robust and
do it with rigor"): scope to the additive-AE axis with the gate built to generalize; promote both
candidate invariants.

## What shipped

- **`scripts/plan/adjudicate.py` (new)** — the terminal gate. `adjudicate(safety_finding, envelope)`
  applies the deployed medical-liaison's adjudication: a content-valid HIGH/MEDIUM override record
  RELEASES the held supplement (records via the existing `record_plan`); a `composite_band==CRITICAL`
  or `harm_class∈{H1,H2}` auto-block, or any invalid/malformed adjudication, leaves the block
  STANDING. `validate_override_record` (content-not-presence: canonical literal, content-bearing
  `operator_reason`, `evidence_provided.rung ≥ evidence_tier_required`, risks-of-proceeding,
  contradictions-log ref), `is_non_overridable`, `audit_adjudication_envelope` (the shared validation
  source), and a `--audit-envelope` CLI (stdlib-only).
- **`scripts/plan/orchestrate.py`** — `generate_plans(..., adjudicator=...)` routes a held additive-AE
  supplement through the gate; a cleared outcome releases the hold; the override record rides the
  returned `adjudication` key. No new store stream; `plan_schema` untouched.
- **`scripts/audit-medical-liaison-override.sh` (new)** + its negative test (13/13, in the floor) —
  the mechanical verification for the two invariants, delegating to the same `adjudicate.py` validator.
- **INVARIANTS.md** — INV-OVERRIDE-RECORD-SCHEMA + INV-CRITICAL-NON-OVERRIDABLE promoted (bead `mdv`)
  via the change-discipline ritual (operator delegation + change-log rows), built-then-promoted.
- **Docs** — `author-dispatch-process.md` (the liaison adjudication envelope + the 10-field
  override-record schema, WIRED S74), `vault/design/plan-generation-pipeline-v1.md` (Build status:
  Phase 4 wired), 2 captured real-dispatch example envelopes.

## Verification (the integration mandate)

Two REAL deployed `medical-liaison` dispatches (full profile inlined per INV-ROLE-INLINING) over the
held fish-oil↔BPC-157 `bleeding-risk` finding:

- **Informed-refusal request** → the liaison assigned MEDIUM/H3, built a content-valid override at the
  `clear-choice` rung → the gate CLEARED → the supplement records (`liaison-adjudication-cleared.example.json`).
- **Vacuous "just want to try both" request** → the liaison held at HIGH/H3 and REFUSED the override
  (vacuous reason on its stop-list, rung unmet) → block stands (`liaison-adjudication-blocked.example.json`).

Both gate invariants mutation-proven RED (neuter content-validation → vacuous tests RED; neuter the
non-overridable gate → 11+ RED), independently re-confirmed by QA + the profile-less blind verifier.
Final: pytest **977/3**, floor **15/0**, core-capability gate green.

## Review (three-tier)

- **Tier-2:** plan-integrity INTEGRITY-CLEAN (factory→component wiring, single validation source, the
  INVARIANTS rows grounded, spec fresh, fixtures grounded, scope honest — all stat/run-verified). QA:
  2 SHOULD-FIX (malformed-JSON CLI exit-code → exit 2; an adjudicator-returns-None integration test) —
  both fixed.
- **Tier-3 `/review-pr`** (6-agent, local diff under GraphQL exhaustion): 6 LEGITIMATE (blind-triaged) +
  1 NOT_ACTIONABLE, all 6 fixed + blind-verified 6/6 RESOLVED. The 2 CRITICAL: a `harm_class` casing
  variance ("h1" vs "H1") released a non-overridable block (SEC-1); a non-dict `severity_final` crashed
  the pass instead of block-standing (BUG-1). Root: the gate validated record CONTENT but trusted the
  routing-key types/casing. Fix: fail-SAFE to block-stands on any malformed routing key.

## Decisions

- **Scope** (operator-delegated): the additive-AE adjudication is the held-line closer; the supplement↔Rx
  BPMH axis (`rxbp`), the author-conflict adjudication (`cfaj`), and the doctor-visit-queue/SBAR artifact
  are Phase-4 follow-ons that REUSE this gate (the Rx axis adds the operator-medication read through the
  PII de-identification boundary — earns its own adversarial verification, hence the split).
- **Fail-loud on a raising adjudicator** (pinned by test): a liaison dispatch that errors propagates out
  of `generate_plans` (matching the unguarded `reauthor` hook) and records nothing — the safe no-release
  direction.

## Process note

The blind verifier's mutation-restore used `git checkout -- adjudicate.py`, which reverted the
UNCOMMITTED working-tree fix to HEAD; it reconstructed the file + I independently re-verified (markers +
suite + mutation-proof) before committing. Lesson (now in HANDOFF Top-3 + the bd-commit memory): commit
fixes promptly; `git checkout` is unsafe on an uncommitted working-tree fix.

## Next (S75)

The Phase-4 follow-on axes (`rxbp`/`cfaj` + the doctor-visit-queue artifact) + the measure/adjust legs —
all reusing the S74 gate. See HANDOFF "What Is Next".
