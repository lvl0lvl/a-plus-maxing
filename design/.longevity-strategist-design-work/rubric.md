# Phase 2.5 Rubric — longevity-strategist domain-research (DEEP mode)

Target: agent-design substrate (`domain-research.md`) for the `longevity-strategist` specialist.
Mode: **deep**. Source floor: **25+** distinct Tier-1/2 primaries (across sections A/B/C). Report floor: **10,000w** synthesis. Judge threshold: **99/100**.

## Per-section judge dimensions (0–100 each; rounded mean = total; <99 → HALT)
- `evidence_quality` — claims grounded in admissible-tier sources at the right design.
- `citation_fidelity` — first-author/year/PMID-DOI resolve; no fabrication (PF-S2-02).
- `type_tag_discipline` — every cite carries exactly one enum type-tag.
- `population_annotation` — every animal/in-vitro numerical claim carries species (+n) and `[population-mismatch:<species>]`.
- `route_fidelity` — no route extrapolation without `[route-extrapolation]`.
- `concentration_audit_handling` — single-group dominance (≥~70% of a compound's primaries from one lab/ITP cohort) surfaced, not buried.
- `risk_floor_readiness` — for compounds expected at `risk_tier: experimental` (rapamycin/NMN/senolytics/metformin-off-label), contraindications + monitoring + stopping criteria are fillable from retrieved sources. (null for pure-protocol/biomarker findings.)
- `reasoning_integrity` — established vs provisional vs experimental kept distinct; correlation ≠ causation; mouse ≠ human.
- `completeness_vs_brief` — section scope covered; agent-design lens present (AGENT_TEMPLATE section + discipline per finding).

## Health-specific dimensions (SKILL Phase 2.5)
- **Concentration audit** — count distinct primaries by lab affiliation; flag ≥70% single-group.
- **Population annotation** — animal cite ⇒ species + n.
- **Route fidelity** — explicit `[route-extrapolation]` tag.
- **Risk-floor readiness** — experimental-compound safety scaffolding present.

## Domain-specific gates (longevity)
- Established-vs-provisional-vs-experimental grading present for every compound (Section C) and every clock (Section B).
- **Lead-with-established**: Section-A established levers carry HIGHER GRADE certainty than Section-C experimental compounds; the agent must foreground the former.
- **Biological-age over-claim**: every clock carries what-it-measures vs what-it-does-NOT-establish; intervention-induced clock change → outcome benefit flagged UNPROVEN.

## Auto-fails — SUB-AGENT (per-section)
AF-S1 fabricated/unresolvable citation; AF-S2 `vendor_label`/`anecdote_aggregate` grounding a numerical claim; AF-S3 untagged animal/in-vitro numerical claim; AF-S4 <9 distinct Tier-1/2 primaries in the section; AF-S5 no GRADE certainty on a major claim.

## Auto-fails — SYNTHESIS
AF-Y1 <25 distinct primaries total; AF-Y2 <10,000w; AF-Y3 placeholder strings (TBD/TODO/"research suggests"); AF-Y4 body↔bibliography asymmetry; AF-Y5 a compound presented as established on animal-only evidence.
