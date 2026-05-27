---
title: AQ-001 — Per-specialist operator-profile field enumeration
type: architecture-question
status: open
created: 2026-05-27
session: S10
phase: Phase 5 (Role 2 design-doc finalize)
source_finding: F-014 (Adversarial review); also WG-4 watch-list disposition
routed_to: Role 1 (health-specialist-architect) post-deployment OR orchestrator pre-architect-deployment per Role 1 §18 OQ-2
blocker: non-blocking for Role 2 design-doc finalize; affects specialist authoring at Session B
---

# AQ-001 — Per-specialist operator-profile field enumeration

## The gap

Role 2 §10.3 lists `vault/meta/operator-profile.md` as NOT-auto-loaded by the implementer (correct — operator binds at specialist runtime, not implementer authoring). Role 2 §4.1 INBOUND row 5 inherits Role 1's R7 contract: "Implementer encodes the read-order into specialist Context Loading."

Neither location specifies **which operator-profile fields each specialist class is expected to read at runtime**:

- cardiovascular-specialist needs `medications`, `cardiovascular_history`, `allergies`
- sleep-coach needs `sleep_baseline`, `caffeine_intake`, `medications`
- gi-specialist needs `dietary_restrictions`, `medications`, `gi_history`
- peptide-specialist needs `medications`, `allergies`, `hard_limits`, `current_compounds`
- ... and so on for 14 specialists

Without per-specialist-class field enumeration, specialists may diverge silently in what they consult. The §13 row 6.6 schema-drift audit catches DRIFT (specialist references a field that no longer exists in operator-profile schema) but does NOT catch UNDER-COVERAGE (specialist failing to read fields it should have read for the role's domain).

## Possible interpretations

**Interpretation A.** Role 1 owns operator-profile field schema (per §4 row 5 contract). Role 1 should enumerate per-specialist-class which fields are mandatory READS. The per-specialist enumeration becomes a YAML mirror similar to `templates/specialist-risk-class.yaml` — call it `templates/specialist-operator-profile-reads.yaml`.

**Interpretation B.** Role 2 owns it. Role 1 only owns the schema; Role 2 (the implementer) decides what each specialist reads as part of authoring the Context Loading prose. Role 2 adds a §10 sub-table with per-specialist-class field enumeration.

**Interpretation C.** Defer to per-specialist authoring with no central enumeration. Implementer reads WIKI.md row + role domain and authors Context Loading per specialist independently. Cross-specialist consistency is enforced by Role 3 (health-edge-case-reviewer) coverage-gap detection.

## Recommendation (orchestrator)

**Interpretation A**, on the grounds that:
- Operator-profile schema IS Role 1's contract (per §4 row 5)
- Per-specialist field enumeration is a Role-1-design-decision; downstream Role 3 coverage-gap detection should NOT have to discover under-coverage from prose — it should grep against a canonical mapping
- Mirror pattern matches `templates/refusal-class-taxonomy.yaml` and `templates/specialist-risk-class.yaml`: Role 1 owns canonical schemas; Role 2 implements specialists against them

Pending architect adjudication.

## Until resolved

§10.3 carries a placeholder note pointing at this AQ. Specialist authoring at Session B for any specialist whose operator-profile field enumeration is unspecified HALTs that specialist's authoring until AQ-001 resolves. The first specialist authored will surface the gap concretely.

## Resolution log

- 2026-05-27 S10 Phase 5: AQ created. Orchestrator recommendation = Interpretation A. Routed to orchestrator queue (pre-architect-deployment per Role 1 §18 OQ-2).
