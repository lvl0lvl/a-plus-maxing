# Document Freshness Rubric

Rules for managing documents so that stale content and conflicting contexts do not interfere with the current project state.

---

## Document Registry

Every document in the project must declare its metadata in YAML frontmatter:

---
title: "Document Title"
type: spec | decision | handoff | rubric | reference | guide
owner: <who maintains this>
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
status: active | draft | stale | archived
depends_on: []
superseded_by: ""
review_cadence: session | weekly | phase | manual
---

### Field Definitions

| Field | Purpose |
|-------|---------|
| `type` | Category for filtering. Specs define what to build; decisions record why; handoffs pass context between sessions. |
| `status` | Lifecycle state. Only `active` docs are authoritative. `draft` is WIP. `stale` needs review. `archived` is kept for history but ignored. |
| `depends_on` | Explicit dependency chain. If a parent doc changes, dependents must be reviewed. |
| `superseded_by` | When archiving, point to the replacement. Prevents following outdated instructions. |
| `review_cadence` | How often the doc should be checked: every session, weekly, per build phase, or only manually. |

## Freshness Rules

### Rule 1: Single Source of Truth
Each concept, decision, or specification lives in exactly ONE document. If two documents describe the same thing, one must be archived with `superseded_by` pointing to the survivor.

### Rule 2: Staleness Detection
A document is stale when:
- `last_reviewed` is older than its `review_cadence` allows
- A file it `depends_on` has been modified since `last_reviewed`
- The code it describes has changed but the doc has not
- It references beads issues that are now closed

Action: Mark `status: stale`. Review within the current or next session. Update or archive.

### Rule 3: Conflict Resolution
When two documents disagree:
1. Check `last_reviewed` dates -- more recently reviewed wins by default
2. Check `type` hierarchy: decision > spec > guide > reference
3. If still ambiguous, escalate to the user
4. Losing doc gets `status: archived` and `superseded_by` set

### Rule 4: Session Review Gate
At session close:
1. List all docs modified this session (`git diff --name-only -- '*.md'`)
2. For each modified doc, update `last_reviewed` to today
3. For each doc with `review_cadence: session`, check if it was reviewed
4. Flag any doc where `depends_on` targets were modified but the dependent was not

### Rule 5: Archive, Don't Delete
Never delete a document. Instead:
1. Set `status: archived`
2. Set `superseded_by` to replacement path (or "N/A")
3. Move to `_archive/` if root gets cluttered

### Rule 6: Vault Consistency
Vault notes follow the same rules. When a vault note becomes stale, update it or archive and replace it.

### Rule 7: Budget Overage Triggers a Load-Bearing Review
When a document exceeds its stated word / line / token budget (e.g., an agent profile over the `/upgrade-agent` ~2,000-token target, a design-doc section over its per-section line budget), the overage **triggers a review, not a blind trim**. The review:
1. Classifies every element as **load-bearing** (a mechanical binary, a safety threshold, a required teaching example, a cross-role contract) or **reducible** (duplication, restated rationale, illustrative-but-not-required prose). The `/adversarial-review` token-economics verdict format — `REDUCIBLE: <list + savings> | LOAD-BEARING: <rationale>` — is the template.
2. Focuses all edits on the **reducible** components only.
3. If the residual still exceeds budget after removing all reducible content, **records the overage as a documented, justified exception** (e.g., against a characterization bead) with the load-bearing rationale — rather than cutting a load-bearing element to hit the number.

Never blind-trim to satisfy a budget number; never cut a load-bearing element to fit. The budget is a trigger for scrutiny, not a cap that overrides correctness. Worked example: S13 `health-implementer` profile (5,007 tokens vs ~2,000 target) — reducible tranche cut, residual documented against bead `2qq`, zero safety binaries removed. Candidate for promotion to INVARIANTS.md (mechanical trigger: `wc`/`tiktoken` over budget) via the change-discipline ritual.

## Review Checklist (Run at Session Close)

- [ ] All modified .md files have updated last_reviewed dates
- [ ] No two active docs describe the same concept
- [ ] No active doc references a closed beads issue as "in progress"
- [ ] No active doc's depends_on targets were modified without reviewing the dependent
- [ ] HANDOFF.md reflects the actual session outcome
- [ ] Vault notes match the current code state
