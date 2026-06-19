# Tesamorelin — Deep-Pass Method (honest provenance)

How this entry was produced, stated plainly so it is not mistaken for the full mechanical
`gate_attest` CLI chain that produced the BPC-157 entry.

## What this run WAS
A deep pass executed by the orchestrating session via **dispatched research agents**, not the
literal `aplus-research` skill registered as a slash command (the skill is a-plus-project-local
and was not registered in the orchestrating session). The gate *logic* was applied; the gate
*CLI* (`gate_attest.py start-iteration/attest/verify-chain`) was not run, so there are no
machine-signed `gate-N.json` files here. This is the faithful-reporting distinction.

## Pipeline actually run
1. **Triage (two rounds, parallel dispatch).** Round 1 scored the remaining Healing/soft-tissue
   class (TB-500, GHK-Cu, KPV, LL-37) — all ≤12/25, excluded. Round 2 scored the strongest
   goal-relevant candidates (Thymosin Alpha-1 19/25, **Tesamorelin 21/25**, Ipamorelin 16/25).
   Tesamorelin won. Scores + rationale: `triage-scores.md`.
2. **Retrieve (5 parallel section agents).** Mechanism · Efficacy-by-population · Safety ·
   PK/dosing · Regulatory/sourcing/prescribing/non-English. Each agent was bound by the
   anti-fabrication mandate (verify every PMID/NCT/DOI/regulatory URL; report absences as
   "NO ADMISSIBLE PRIMARY FOUND"; type-tag every claim; vendor/anecdote may never ground a
   numerical claim; animal cites need species + n).
3. **Integrity logic applied at synthesis** (orchestrator): every numerical claim in the entry
   traces to a Tier-1/2 source in `sources-ledger.md`; the population-mismatch (HIV → general)
   is surfaced as the first-class caveat (§4 of the report); no vendor/anecdote source grounds
   any number; `VERIFIED:partial` items are flagged, not overstated.
4. **Adversarial review gate (PR cycle).** An independent review agent checked every citation and
   grounding before merge — see `review-verdict.md`.

## Evidence grade
- evidence_tier **A** for the STUDIED indication (HIV-associated lipodystrophy): multiple Phase-3
  RCTs + a 2026 meta-analysis.
- evidence_tier **effectively D** for the operator's intended use (non-HIV / general / post-illness
  body composition): zero direct randomized evidence — a verified absence, not an omission.

## Honest limitations of this pass
- No machine-signed gate chain (see above). The verification is the agent-level citation checks +
  the source ledger + the independent review, which is strong but is not the cryptographic
  attestation chain.
- Retrieval depth was triage-plus, not exhaustive: the focus was the decision-relevant evidence
  (does efficacy exist for THIS operator's population) + the regulatory/safety floor. A future pass
  could deepen the dose-response and the extension-phase reversibility magnitude.
