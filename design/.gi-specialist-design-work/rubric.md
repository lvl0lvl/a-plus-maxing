# Phase 2.5 Rubric — gi-specialist domain research (mode=standard, threshold 92/100)

Goal-agnostic GI-domain library knowledge to ground the `gi-specialist` agent design.
This is a **design-research** dispatch (peptide-specialist precedent), NOT a single-compound
vault ingest — output lands in `design/.gi-specialist-design-work/`, never `vault/` (PF-S2-04).

## Dimensions (each scored 0–100; total = rounded mean of non-null)

1. **evidence_quality** — claims grounded in Tier-1/2 primaries per `_source-whitelist.md`; RCT/meta-analysis preferred over mechanism/animal for human-outcome claims.
2. **citation_fidelity** — every numerical claim has a resolvable citation (author/year + PMID/DOI/registry or regulator doc); first-author + year match the cited source.
3. **type_tag_discipline** — every claim carries exactly ONE type-tag from the enum (`rct|meta_analysis|cohort|open_label|animal|in_vitro|mechanism_review|regulatory|compounding_data_sheet|vendor_label|practitioner_protocol|anecdote_aggregate`). Vendor/anecdote NEVER ground numbers.
4. **population_annotation** — every `animal`/`in_vitro` numerical claim carries `[population-mismatch: <species>]`; sex/age-restricted human cohorts flagged.
5. **route_fidelity** — any dose claim whose cited primary used a different route than stated carries `[route-extrapolation]`.
6. **concentration_audit_handling** — for any compound/topic where ≥70% of distinct primaries cluster in one lab/group, a dominance caveat + certainty downgrade is surfaced (not buried).
7. **risk_floor_readiness** — for any GI compound likely to land `risk_tier: medium+/experimental`, contraindications + monitoring biomarker + stopping-criteria are FILLABLE from retrieved sources. (null only if a section carries no compound content.)
8. **reasoning_integrity** — mechanism vs human-outcome kept distinct; no class-membership-as-efficacy; consumer-test validity claims (IgG food sensitivity, microbiome kits) judged against the actual evidence, not marketing.
9. **completeness_vs_brief** — the section covers its assigned scope; GI red-flag/clinical-boundary content present where in scope; ≥ the per-section source floor.

## GRADE two-axis (carried into every recommendation in synthesis)
`certainty: high|moderate|low|very-low` AND `strength: strong|weak|conditional`.
A strong-with-low or strong-with-very-low pairing → HALT (downgrade or override-log).

## Standard-mode source floor
≥15 distinct admissible primaries across sections (deduplicated). Each section targets ≥8.

## Health-specific gates carried (per references/health-gates.md)
- Population-mismatch (Phase 4.75): animal numerics flagged.
- Concentration-audit (Phase 4.75): single-lab ≥70% surfaced first-class.
- Risk-floor (Phase 7.5): experimental-tier GI compounds carry the safety scaffold.
- Mandatory layers (8.5, standard+ compound): prescribing-practice + non-English coverage — folded into Section B/C retrieval briefs for this design-research dispatch (peptide precedent), with explicit non-English survey + practitioner-convention coverage required.
