# Phase 2.5 Rubric — dermatologist domain research (mode=standard, threshold 92/100)

Goal-agnostic dermatology-domain library knowledge to ground the `dermatologist` agent design.
This is a **design-research** dispatch (peptide-/gi-specialist precedent), NOT a single-compound
vault ingest — output lands in `design/.dermatologist-design-work/`, never `vault/` (PF-S2-04).

## Dimensions (each scored 0–100; total = rounded mean of non-null)

1. **evidence_quality** — claims grounded in Tier-1/2 primaries per `_source-whitelist.md`;
   RCT/meta-analysis (Cochrane skin group preferred where it exists) over mechanism/animal for
   human-outcome claims (efficacy of an active, AGA treatment response, AE rates).
2. **citation_fidelity** — every numerical claim has a resolvable citation (author/year + PMID/DOI/
   registry or regulator doc); first-author + year match the cited source.
3. **type_tag_discipline** — every claim carries exactly ONE type-tag from the enum (`rct|
   meta_analysis|cohort|open_label|animal|in_vitro|mechanism_review|regulatory|
   compounding_data_sheet|vendor_label|practitioner_protocol|anecdote_aggregate`). Vendor/anecdote
   NEVER ground numbers (cosmetic-brand marketing claims are `vendor_label`, never efficacy).
4. **population_annotation** — every `animal`/`in_vitro` numerical claim carries
   `[population-mismatch: <species>]`; sex/age-restricted human cohorts flagged (e.g.,
   finasteride male-pattern cohorts; sunscreen photoaging trial demographics).
5. **route_fidelity** — any dose/concentration claim whose cited primary used a different route
   than stated carries `[route-extrapolation]` (e.g., topical vs oral minoxidil; oral vs topical
   finasteride; in-vitro active concentration vs formulated topical %).
6. **concentration_audit_handling** — for any active/topic where ≥70% of distinct primaries cluster
   in one lab/group/industry sponsor, a dominance caveat + certainty downgrade is surfaced (not
   buried) — relevant for cosmeceutical actives with manufacturer-funded literature.
7. **risk_floor_readiness** — for any dermatology compound likely to land `risk_tier: medium+/
   experimental` (systemic finasteride/dutasteride, oral minoxidil, prescription tretinoin in
   pregnancy context, off-label topical peptides), contraindications + monitoring + stopping-
   criteria are FILLABLE from retrieved sources. (null only if a section carries no compound content.)
8. **reasoning_integrity** — mechanism vs human-outcome kept distinct; no in-vitro active potency
   read as topical efficacy; consumer/AI skin-test + teledermatology claims judged against actual
   evidence (sensitivity/specificity, FDA status), not marketing; the skin-cancer-not-remotely-
   diagnosable boundary stated with evidence (missed-melanoma harm), never softened.
9. **completeness_vs_brief** — the section covers its assigned scope; the skin-cancer red-flag /
   changing-lesion clinical boundary present where in scope (Section C); ≥ the per-section source
   floor.

## GRADE two-axis (carried into every recommendation in synthesis)
`certainty: high|moderate|low|very-low` AND `strength: strong|weak|conditional`.
A strong-with-low or strong-with-very-low pairing → HALT (downgrade or override-log).

## Standard-mode source floor
≥15 distinct admissible primaries across sections (deduplicated). Each section targets ≥8.

## Health-specific gates carried (per references/health-gates.md)
- Population-mismatch (Phase 4.75): animal/in-vitro numerics flagged.
- Concentration-audit (Phase 4.75): single-lab/sponsor ≥70% surfaced first-class.
- Risk-floor (Phase 7.5): experimental/medium+ dermatology compounds carry the safety scaffold
  (folded for design-research — fillability, not a vault write).
- Mandatory layers (8.5, standard+ compound): prescribing-practice + non-English coverage — folded
  into Section B/C retrieval briefs for this design-research dispatch (peptide/gi precedent), with
  explicit non-English survey + practitioner-convention coverage required.

## Dermatologist-specific judging notes
- **Image-input is the dominant safety surface.** Skin is the most photo-pasted domain; the design
  must treat a pasted lesion/rash photo as `IMAGE_OR_SIGNAL_INPUT` refusal, and a non-
  interpretation must NOT read as "looks benign" that clears the ABCDE/skin-cancer floor. A section
  that omits this fails completeness_vs_brief + reasoning_integrity.
- **Skin cancer is not remotely diagnosable.** Any source or claim implying remote
  reassurance/diagnosis of a pigmented or non-healing lesion is a reasoning_integrity failure; the
  evidence base is the missed-melanoma + teledermatology-limits literature.
