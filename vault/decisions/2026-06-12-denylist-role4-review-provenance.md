---
title: Denylist Role-4 content-review provenance (PR #106 merge record)
type: decision
status: active
owner: walter
created: 2026-06-12
last_reviewed: 2026-06-12
permalink: a-plus-maxing/decisions/2026-06-12-denylist-role4-review-provenance
---

# Denylist content-review provenance — PR #106 (bead `pmp`)

The merge-time record the denylist's header promises ("review provenance is
recorded at merge"). Satisfies the PR #106 review's T20 disposition.

- **Artifact:** `templates/negative-example-denylist.yaml` (row-10 deploy-gate BLOCK
  content), merged via PR #106 at branch head `7a6ad7f`
  (content sha256 `6edf464d217555ac0ec4f3a0657576ef119c26582afa426c124136c4cab70585`).
- **Reviewer (content owner per Pass-1 R10/OQ-6):** the DEPLOYED
  `medical-safety-reviewer` (Role 4), dispatched S52 with its full profile inlined.
- **Verdict (canonical Role-4 vocabulary):** `composite_band: MEDIUM`,
  `deploy_verdict: BLOCK_WITH_OVERRIDE_PATH`,
  `override_path: {adjudicator: medical-liaison, conditions: fix F1 (+ optionally F2)
  before flipping row-10 to BLOCK, OR accept as documented v1-starter residuals}`.
  No CRITICAL/H1-H2 (content review; no runtime agent).
- **Findings + dispositions (applying commit `01938c8`, hardened in `5c21a86`):**
  F1 unit right-boundary (MEDIUM, gating) — APPLIED + RED-proven; F2 taxonomy noun
  alignment (MEDIUM borderline) — APPLIED + mechanical sync test (`7a6ad7f`);
  F3 `\b` removal (LOW) — APPLIED; F4 whole-body coverage residual (LOW) — ROUTED to
  bead `rn3v` (open); F5 valproate (LOW advisory) — APPLIED; F6 nitrate×PDE5 (LOW
  advisory) — APPLIED; F7 mycophenolate category-D precision (LOW info) — APPLIED.
- **Adjudication (Role 7 `medical-liaison`, deployed, dispatched S52 2026-06-12):**
  `severity_final: {set_by: medical-liaison, verdict: conditions-met, content may
  merge}` — the first disjunct of the override conditions satisfied and exceeded;
  band NOT lowered; no operator override occurred and the override literal was not
  invoked; every F1-F7 disposition mechanically re-verified against the artifact at
  head (per-finding GRADE-tagged evidence in the liaison's S52 return).
- **Mechanics hardening (same PR, post-review):** the gate's own fail-open seams
  closed fail-closed (malformed-ERE, non-canonical heading, fence parity, extractor
  shape lint, tracked-file absence) per the PR #106 6-agent review — 17/17 findings
  blind-verified; suite 55/0; roster sweep 0 row-10 BLOCKs across all 20 deployed
  profiles.

The rebase-merge strategy produces no merge commit; this note + the PR #106 body +
the `pmp` bead close reason are the citation chain.
