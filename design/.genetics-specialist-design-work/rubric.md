# Phase 2.5 — RUBRIC (genetics-specialist domain research, deep mode)

Deep-mode judge threshold: **99/100**. Each Phase-3 retrieval section is scored by its paired judge against the dimensions below. `verdict: PASS` requires `total ≥ 99` AND `findings: []`. Any dimension that materially fails → HALT with specific findings → remediation iteration (≤3).

## Per-section dimensions (judge scores each 0–100; total = rounded mean of non-null)

| Dimension | What it measures | HALT triggers |
|---|---|---|
| evidence_quality | Claims grounded in Tier-1/Tier-2 sources or authoritative consortia (CPIC/PharmGKB/ClinGen/ACMG/FDA); appropriate study designs cited | wellness-blog or vendor sourcing of a clinical claim; missing primary for a load-bearing claim |
| citation_fidelity | Every inline `[N, tag]` resolves to a bibliography entry with a REAL, resolvable URL (PMID/DOI/guideline URL); author/year/identifier match the source | fabricated or unresolvable citation; attribution error (PF-S2-02) |
| type_tag_discipline | Each citation carries exactly one enum tag; FDA→`regulatory`; consensus guideline/knowledgebase→`mechanism_review`; studies by design | untagged citation; vendor/anecdote tag grounding a numerical claim |
| population_annotation | Every animal/in_vitro numerical claim carries `[population-mismatch: <species>]` (unless species is sentence subject within 100 chars) | unflagged animal/in_vitro numerical claim |
| route_fidelity | N/A for most genetics claims (not dose-routed); applies only where a PGx dosing claim extrapolates route | route extrapolation without `[route-extrapolation]` tag |
| concentration_audit_handling | Evidence base spans multiple independent groups/consortia (genetics is broad: gnomAD, CPIC, ClinGen, many cohorts); no single-lab dominance ≥70% | single-group dominance ≥70% not surfaced |
| risk_floor_readiness | **null (N/A)** — reference target, not an experimental compound entry | n/a |
| reasoning_integrity | Safety floors stated accurately and not overclaimed: DTC-raw≠diagnostic, PGx-informs-not-authorizes, risk-variant≠disease, penetrance/expressivity nuance; no determinism overreach | presenting a raw-genotype call as a diagnosis; PGx authorizing a dose change; conflating risk allele with disease |
| completeness_vs_brief | Section covers all scoped topics from plan.md for this section; ≥6 distinct primary/authoritative sources | missing a scoped subtopic; <6 sources |

## Health-specific gate readiness (checked at Phase 4.75, previewed here)
- **Population-mismatch:** animal/in_vitro numerical → inline species tag. (Genetics is mostly human; flag any rodent/cell mechanistic numbers.)
- **Concentration-audit:** compute distinct-source group share; genetics evidence is consortium-distributed, expect <70%. If ≥70%, surface as first-class section.
- **No vendor/anecdote numerical grounding:** DTC company marketing pages are NOT admissible to ground clinical/numerical claims (treat as `anecdote_aggregate` at most; 23andMe FDA authorizations are `regulatory`).

## Safety-floor accuracy (load-bearing — domain-specific)
Every section that touches actionable findings MUST state the relevant floor verbatim-in-spirit:
1. DTC raw SNP calls are NOT diagnostic; clinically-actionable variants require clinical-grade confirmation.
2. A risk variant is not a disease (penetrance/expressivity/polygenic context); disease-risk findings → genetic counselor + MD.
3. PGx metabolizer status informs the prescriber conversation; it does NOT authorize the agent to change drug/dose.
4. Genetic data is uniquely sensitive/immutable (genetic exceptionalism); reference knowledge is goal-agnostic.
