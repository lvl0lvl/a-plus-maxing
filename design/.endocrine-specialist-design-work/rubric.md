# Phase 0 Deep-Research Rubric — endocrine-specialist domain research (design substrate)

**Mode:** deep (risk class `compound-medium-or-experimental` per `templates/specialist-risk-class.yaml`).
**Deliverable purpose:** research SUBSTRATE for the endocrine-specialist *agent design doc* (`design/endocrine-specialist-design.md` §3 Pass-1 Deliverable Digest). It is NOT a wiki compound entry — no `vault/compounds/*` is authored (PF-S2-04: this build consumes the wiki, it does not author it).
**Source floor (deep):** ≥25 unique sources across the synthesized report; each retrieval section ≥6 sources.
**Judge threshold:** 99/100 (deep). A section scoring <99 OR carrying any `critical`/`major` finding → HALT → remediation iteration (max 3). Loop-break: after 3 iterations without convergence, deliver at best state with residual gaps named in the section's `## Open gaps`.

## Type-tag enum (every source carries exactly one — from `vault/library/_source-whitelist.md`)
`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`
Vendor/anecdote tags NEVER ground a numerical claim (dose, effect size, n, AE rate, half-life).

## Scoring dimensions (0–100 each; `total` = rounded mean of non-null dimensions)

1. **evidence_quality** — Sources are Tier 1/2 primary literature or regulatory per the whitelist; claims grounded in admissible tiers; lower-trust open-access (Frontiers/MDPI) and preprints flagged.
2. **citation_fidelity** — Author/year/PMID/DOI match the cited source; no fabricated or anomalous URLs (medRxiv DOI prefix `10.1101/`; no future-dated arXiv; no fictitious TLDs); PMIDs resolve.
3. **type_tag_discipline** — Every source carries exactly one enum tag; vendor/anecdote never grounds a numerical claim.
4. **population_annotation** — Every animal/in-vitro cite carries `[population-mismatch: <species>]` and species+n; no animal safety/efficacy presented as human-applicable without the tag; route-extrapolation tagged.
5. **concentration_audit** — Distinct primaries counted by lab/author group; any single-group share ≥70% surfaced as a first-class caveat with downgraded certainty (not buried).
6. **domain_coverage_vs_brief** — The assigned angle is covered comprehensively against the brief's enumerated sub-questions.
7. **agent_design_relevance** — Findings translate into concrete agent-design substance: behavioral rules, refusal-class triggers, role boundaries, escalation paths, edge cases, anti-patterns — not a generic literature review. Each Finding states what it implies for the deployed `agent.md`.
8. **safety_sensitivity (H-class)** — For this highest-safety-sensitivity specialist: hormone-axis interpretation hazards and hormone-affecting-compound harms are correctly placed on the H1–H8 ordinal scale (H1 death most severe → H8 least; H1/H2 auto-block), composed-harm and authority-framing vectors identified.
9. **reasoning_integrity** — No overclaiming; mechanism vs human-outcome evidence kept distinct; GRADE two-axis (certainty × strength) applied; uncertainty surfaced; counter-evidence included.

## Output-format requirement (every retrieval section)
- `## Section <X> — <title>`
- Numbered prose findings, each grounded by `[n, tag]` inline cites.
- `## Sources` — numbered list: `[n] First-Author YYYY — title — venue — PMID/DOI/URL — [tag]`.
- `## Open gaps` — what could not be grounded to an admissible source.
- `## Verdict` (judge writes the paired `judges/judge-<X>.json`, NOT the retrieval agent).

## Synthesis-level requirement (domain-research.md)
- `### Finding N` headings (one per load-bearing structural conclusion) — count is the row count for design-doc §3.1.
- `R1`–`R<N>` recommendations, each tagged for the AGENT_TEMPLATE.md section it informs (Core Rules / Role Boundaries / Anti-Patterns / Tools / Communication / Edge Cases).
- Body↔bibliography symmetry verified before critique dispatch (CONTINUATION_BRIEF Lesson 3): `set(body [n]) == set(bibliography [n])`.
