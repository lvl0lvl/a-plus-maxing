# Phase 2 PLAN — dermatologist domain research (mode=standard)

## Research question (goal-agnostic, library-knowledge)
What domain knowledge must ground the design of a `dermatologist` medical sub-agent in the
a-plus-maxing project — across skin-barrier/photoaging topical actives, androgenetic-alopecia
(hair) compounds, common dermatologic conditions at a literacy level, the skin-cancer / changing-
lesion red-flag boundary, clinical-image-input validity, consumer skin-test validity, and the
inherited agent-design safety contracts — such that the agent produces goal-agnostic vetted
dermatology-library knowledge and performs personalized skin/hair reasoning without crossing the
project's medical-safety boundaries (it does NOT diagnose lesions, interpret photos, or reassure
on skin cancer)?

## Sections (3 paired retrieval+judge dispatches; threshold 92/100; ≥8 primaries each, ≥15 total)
- **Section A — Photoaging + skin-barrier topical actives.** Topical retinoids (tretinoin,
  adapalene, tazarotene, retinaldehyde, OTC retinol) — RCT/meta evidence for photoaging/acne,
  mechanism, AEs (retinoid dermatitis, photosensitivity), pregnancy handling (topical-retinoid
  teratogenicity evidence + precautionary labeling). Photoprotection (broad-spectrum sunscreen,
  UVA/UVB, SPF, the Hughes 2013 RCT on photoaging prevention; FDA sunscreen systemic-absorption
  studies). Evidence-graded actives: niacinamide, vitamin C (L-ascorbic acid), alpha-hydroxy
  (glycolic/lactic) + beta-hydroxy (salicylic) acids, barrier/moisturization (ceramides, urea,
  glycerin). GRADE per active; OTC vs Rx status; concentration-audit on single-source actives.
- **Section B — Hair (androgenetic alopecia) + topical/systemic compounds.** Minoxidil (topical
  2%/5%, low-dose oral) — RCT evidence, mechanism, AEs (hypertrichosis; oral-minoxidil
  cardiovascular/fluid profile). Finasteride / dutasteride (systemic 5-alpha-reductase
  inhibitors) — RCT efficacy, AE profile (sexual dysfunction incidence, post-finasteride-syndrome
  controversy, pregnancy/teratogenicity handling, PCPT high-grade-prostate-cancer signal),
  topical-finasteride emerging evidence; **cross-read boundary to endocrine-specialist for
  systemic hormonal effects**. Adjuncts (evidence maturity): ketoconazole shampoo, microneedling,
  low-level laser therapy, PRP. Topical peptides (copper-peptide GHK-Cu) — **overlap boundary with
  peptide-specialist** (experimental-tier; disjoint at build).
- **Section C — Common conditions (literacy) + RED-FLAGS + consumer-test/image validity.** Acne,
  rosacea, atopic dermatitis/eczema, seborrheic dermatitis at a MANAGEMENT-PRINCIPLE level (not
  diagnosis, not Rx). The skin-cancer red-flag: ABCDE melanoma criteria, changing/bleeding/non-
  healing lesion, the evidence that skin cancer is NOT remotely diagnosable and that reassurance
  is harmful (missed-melanoma literature); teledermatology + AI/SaMD skin-lesion-classifier
  accuracy + FDA/regulatory status (why an LLM is not a validated diagnostic device); DTC
  "skin-analysis" app / unvalidated consumer-test validity. Non-English survey + confirmed-absence
  note.
- **Section D — agent-design contracts (synthesis-only, no new retrieval).** Inherited refusal
  taxonomy (with `IMAGE_OR_SIGNAL_INPUT` load-bearing — skin is the most photo-pasted domain),
  H-class, GRADE two-axis, R7 operator-profile precondition, medical-liaison escalation
  (`BLOCK_WITH_OVERRIDE_PATH`), wiki-consumption contract — grounded by name in the project
  contract pack, no external evidence.

## Gate plan (standard mode)
2.75 SCOPE (done, PASS) → 3 paired dispatches → 3.5 JUDGE (≥92) → 4 TRIANGULATE →
4.25 ID-RECONCILE (folded into 4.75 IC-10 cross-section identifier reconciliation per gi precedent)
→ 4.5 OUTLINE → 4.75 INTEGRITY (attested via gate_attest.py) → 5 SYNTHESIZE →
7.5 RISK-FLOOR (folded for design-research; no single vault compound entry) → 8.5 LAYERS
(prescribing-practice + non-English folded into Section B/C briefs per peptide/gi precedent).
Phase 6 CRITIQUE skipped (deep+ only).

## Adaptation note (PF-S2-04 / peptide+gi precedent)
Design-research dispatch, not single-compound vault ingest. All artifacts → design-work; NO writes
to vault/compounds, vault/library, vault/biomarkers, protocols/. Phase-8 vault packaging replaced
by the `domain-research.md` synthesis. Mandatory standard+ layers (prescribing-practice + non-
English) satisfied IN-SECTION (B = prescribing/regulatory conventions; C = non-English survey)
rather than as separate vault layer files, matching deployed peptide-/gi-specialist design-work.
Dermatologist is ABSENT from `specialist-risk-class.yaml`; classed `compound-medium`/mode_floor
`standard` by analogy to the three sibling compound-medium specialists (cardiovascular/gi/
lymphatic) — surfaced as an integrator bead. Experimental-tier topical peptides remain peptide-
specialist's; systemic hormonal effects of 5ARIs remain endocrine-specialist's (cross-reads).
