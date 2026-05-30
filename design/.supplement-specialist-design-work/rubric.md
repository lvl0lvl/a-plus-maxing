# Rubric — supplements-landscape (deep mode, threshold 99/100)

Target: design substrate `domain-research.md` for the supplement-specialist agent. Goal-agnostic landscape research across OTC supplements / herbals / nootropics.

## Plan (Phase 2)
Search angles, one paired retrieve+judge dispatch per section:
- **Section A** — landscape & evidence-maturity stratification (RCT-strong vs preclinical/anecdote; mechanism-vs-outcome; concentration/funding dominance; bioavailability/formulation).
- **Section B** — safety hazards (toxicity ceilings/ULs; hepatotoxicity cluster; herb/supplement–drug interactions; adulteration/contamination base rate; stimulant/dependence gray zone; anti-doping contamination).
- **Section C** — regulatory surface (DSHEA; GRAS/NDI/structure-function vs approved/effective/safe; banned/enforcement ingredients, time-sensitive; international divergence) + agent contract-inheritance mapping.
- **Section D (mandatory layer, Hard Rule 3)** — prescribing-practice / practitioner-convention layer for the supplement/nootropic space (`practitioner_protocol` / `compounding_data_sheet` tier; convention ≠ trial-validated).
- **Section E (mandatory layer, Hard Rule 3)** — non-English literature coverage (Russian/Soviet nootropics: Semax/Selank/noopept/Cerebrolysin; Chinese/TCM herbals; originator-country lit).

Triangulation rule: a numerical claim appearing in 2+ sections must agree (else contradictions entry). Cross-section identity reconciliation (Phase 4.25) on compound IDs, regulatory dates, citations.

## Scoring dimensions (per judge, 0-100, total = rounded mean of non-null)
- evidence_quality — Tier-1/2 primary literature weight; no leaning on Tier 4/5.
- citation_fidelity — author/year/identifier match the source.
- type_tag_discipline — every claim exactly one whitelist tag; vendor/anecdote never ground numerical.
- population_annotation — every animal/in_vitro numerical claim carries `[population-mismatch: <species>]` in-sentence.
- route_fidelity — no route extrapolation without `[route-extrapolation]`.
- concentration_audit_handling — ≥70% single-lab OR single-funder/manufacturer share surfaced as first-class caveat + downgraded certainty.
- risk_floor_readiness — for experimental-tier compounds (e.g. MK-677, novel nootropics, phenibut/tianeptine), contraindications + monitoring + stopping-criteria fillable from sources.
- reasoning_integrity — mechanism never upgrades human-outcome certainty; class never substitutes for compound-level evidence.
- completeness_vs_brief — covers the section brief.

## Health-specific rubric additions (Phase 2.5)
- Sikiric-style concentration audit (+ supplement-specific manufacturer-funded-study dominance).
- Population annotation (species + n on every animal cite).
- Route fidelity (`[route-extrapolation]` tag).
- Risk-floor readiness for experimental-tier supplements/nootropics.
- Goal-agnosticism: no operator personalization injected (PF-S2-04).

Deep threshold: 99. HALT < 99 or any hard-rule violation → re-dispatch with findings (iter max in skill).
