# Phase 2 PLAN — gi-specialist domain research (mode=standard)

## Research question (goal-agnostic, library-knowledge)
What domain knowledge must ground the design of a `gi-specialist` medical sub-agent in the
a-plus-maxing project — across GI/microbiome physiology, the evidence-maturity + safety landscape
of GI compounds, GI/inflammation biomarker validity, GI clinical red-flags, consumer GI-test
validity, and the inherited agent-design safety contracts — such that the agent produces
goal-agnostic vetted GI-library knowledge and performs personalized GI reasoning without crossing
the project's medical-safety boundaries?

## Sections (3 paired retrieval+judge dispatches; threshold 92/100; ≥8 primaries each, ≥15 total)
- **Section A — GI physiology + microbiome + biomarker validity.** Microbiome composition/function;
  gut-barrier ("intestinal permeability"/zonulin science + controversy); digestion + motility;
  food sensitivity vs allergy vs intolerance taxonomy; validity of GI/inflammation biomarkers
  (fecal calprotectin, fecal occult blood/FIT, zonulin assay validity, secretory IgA, hs-CRP for
  GI, breath tests for SIBO/lactose/fructose).
- **Section B — GI compounds: evidence maturity, safety, regulatory, prescribing.** Probiotics
  (strain/indication specificity; AAD; IBS; the PROPATRIA critically-ill-pancreatitis mortality
  signal), prebiotics/fiber (inulin/FOS/GOS, psyllium), digestive enzymes (PERT vs OTC), betaine
  HCl, gut-barrier agents (L-glutamine, zinc-carnosine, colostrum), motility/symptom agents
  (peppermint oil, ginger, prokinetics). Evidence tier, OTC/Rx status, risk_tier, AEs,
  contraindications (immunocompromised), prescribing-practice conventions, concentration-audit.
- **Section C — Clinical red-flags + consumer-test validity + safety architecture.** GI alarm
  features requiring urgent clinician (GI bleeding/melena, dysphagia, unintentional weight loss,
  iron-deficiency anemia, age>50 new-onset, FHx CRC) per ACG/BSG/Rome IV; IBS vs IBD vs celiac vs
  colorectal-cancer distinction and why an LLM must not diagnose; validity of consumer
  food-sensitivity (IgG) panels (AAAAI/EAACI/CSACI position statements), at-home microbiome tests,
  SIBO-testing controversy, elimination-diet risks. Non-English survey + confirmed-absence note.
- **Section D — agent-design contracts (synthesis-only, no new retrieval).** Inherited refusal
  taxonomy, H-class, GRADE two-axis, R7 operator-profile precondition, medical-liaison escalation,
  wiki-consumption contract — grounded by name in the project contract pack, no external evidence.

## Gate plan (standard mode)
2.75 SCOPE (done, PASS) → 3 paired dispatches → 3.5 JUDGE (≥92) → 4 TRIANGULATE →
4.25 ID-RECONCILE (attested) → 4.5 OUTLINE → 4.75 INTEGRITY (attested) → 5 SYNTHESIZE →
7.5 RISK-FLOOR (attested; folded for design-research) → 8.5 LAYERS (attested; prescribing+non-English
folded into Section B/C per peptide precedent). Phase 6 CRITIQUE skipped (deep+ only).

## Adaptation note (PF-S2-04 / peptide precedent)
Design-research dispatch, not single-compound vault ingest. All artifacts → design-work; NO writes to
vault/compounds, vault/library, vault/biomarkers, protocols/. Phase-8 vault packaging replaced by the
`domain-research.md` synthesis. Mandatory standard+ layers (prescribing-practice + non-English) are
satisfied IN-SECTION (B = prescribing/regulatory; C = non-English survey) rather than as separate
vault layer files, matching the deployed peptide-specialist design-work.
