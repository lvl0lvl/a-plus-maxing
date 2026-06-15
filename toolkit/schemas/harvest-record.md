---
title: "Harvest Record Schema — the machine-readable evidence layer"
type: reference
owner: framework
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
review_cadence: manual
---

# Harvest Record Schema

The **machine-readable evidence layer** of the self-improvement loop (F-017). One
append-only JSONL file per deployment (`harvest.jsonl`), one record per failure or
promotable practice. The PF log is for *humans* (narrative, root-cause); this is
for *machines* — it is the substrate the cross-deployment harvest (and the eventual
automation) reads. Beads are the tracking handle and point at these records; they
do not replace them (a bead title is too lossy to harvest).

**Append-only.** Never rewrite a record; supersede it with a new one citing the
predecessor's `id`. Records are emitted by `toolkit/scripts/pf-ingest.sh` and
validated by `toolkit/scripts/harvest-gate.sh` at session close.

## FAIL record (a failure)
```json
{
  "kind": "fail",
  "id": "FAIL-<DEPLOY>-<NNN>",
  "ts": "YYYY-MM-DD",
  "deployment": "<project/library/role/skill name>",
  "artifact": "<the role/skill/discipline implicated, or n/a>",
  "class": "enforcement-gap | rotation-continuity-drift | verification-skip | scope-drift | memory-hygiene | role-dispatch | dead-wire | inconsistency | deploy-parity | other",
  "pattern": "<one-line: what went wrong>",
  "source_refs": ["<PF-id>", "<file:line>", "<bead-id>"],
  "recurrence_count": 1,
  "detection_mode": "user-catch | spot-check | red-team | mechanical-audit | gate-trip | self",
  "surfaced_by": "self | gate | user",
  "promised_mitigation": "<the forward fix, or null>",
  "built": "true | false | partial",
  "adjudication": "should-have-fixed | rightfully-deferred | negligently-unfixed | rightfully-fixed | UNCERTAIN",
  "bead_ref": "<tracking bead id>",
  "supersedes": "<prior FAIL id, or null>"
}
```
Required to pass `harvest-gate.sh`: `kind, id, class, pattern, source_refs, detection_mode, built, bead_ref`.
`detection_mode: user-catch` / `surfaced_by: user` is the worst case — no automated
discipline caught it; a class that surfaces `user` in ≥2 sessions auto-nominates a gate.

## PRAC record (a promotable practice)
```json
{
  "kind": "prac",
  "id": "PRAC-<DEPLOY>-<NNN>",
  "ts": "YYYY-MM-DD",
  "deployment": "<source>",
  "cdm_ref": "<canonical practice id, or NONE>",
  "relation": "adopted-as-is | mutated | added | dropped | absent",
  "title": "<one line>",
  "evidence": ["<file:line>"],
  "convergence": "convergent | divergent | convergent-absence | unique-to-one",
  "rubric": { "generality": 0, "evidence": 0, "enforceability": 0, "composability": 0, "maturity": 0, "cost": 0, "convergence": 0, "sum": 0, "band": "" },
  "skeptic": "upheld | downgrade | reject | unreviewed",
  "action": "promote | cross-pollinate | keep-local | backlog | reject"
}
```

## Why this exact shape graduates to automation (F-017)
These fields ARE the future automation's interface contract. `pf-ingest` writes them
manually-but-enforced today; an automated harvester writes the same records tomorrow
with no schema change. The accumulating JSONL is simultaneously the automation's
training data and its spec. Don't add fields the automation can't populate; don't
omit fields the harvest needs to cluster (`class`, `recurrence_count`, `convergence`).
