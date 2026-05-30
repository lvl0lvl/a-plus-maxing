---
title: "GI-Specialist Medical Agent — Domain Research (Pass-3 Synthesis)"
type: research-report
mode: standard
role_slug: gi-specialist
role_class: specialist
research_question: "What goal-agnostic domain knowledge — GI/microbiome physiology, the evidence-maturity and safety landscape of GI compounds (probiotics, prebiotics, digestive enzymes, gut-barrier agents, motility/digestive aids), GI/inflammation biomarker validity, GI clinical red-flags and the validity of food-sensitivity/microbiome consumer testing, plus the inherited a-plus-maxing agent-design safety contracts — must ground the design of a gi-specialist medical sub-agent that consumes the project wiki and dispatches gated research on microbiome+GI gaps?"
sub_agents_dispatched:
  - "Section A (GI physiology / microbiome / gut barrier / biomarker validity) — paired retrieval+judge, iter-1 PASS 97/100"
  - "Section B (GI compounds: evidence / safety / regulatory / prescribing) — paired retrieval+judge, iter-3 PASS 96/100 (2 citation defects caught+fixed iter-1; 1 byline defect caught+fixed iter-2/3)"
  - "Section C (clinical red-flags / consumer-test validity / safety architecture) — paired retrieval+judge, iter-3 PASS 97/100 (1 mistagged source + 1 DOI defect caught+fixed)"
  - "Phase 4.75 Integrity Verifier — gate-attested PASS (11 IC PASS, IC-13 SKIP-mode standard; concentration share 0.05); attestation_chain intact"
  - "Synthesis (this file) — corpus-read-only, no new retrieval"
judge_gate: "PASS — all 3 sections at standard threshold 92 (A 97 / B 96 / C 97)"
integrity_gate: "PASS (gate-4.75.json, gate_attest-produced, verify-chain intact)"
sources_total: 54
distinct_admissible_primaries: ">40 (Section A ≥12, Section B 25+, Section C 14; deduplicated >40)"
generated: 2026-05-30
adaptation_note: "Design-research dispatch (peptide-specialist precedent), NOT a single-compound vault ingest. All artifacts in design/.gi-specialist-design-work/; NO writes to vault/ (PF-S2-04). Phase-8 vault packaging replaced by this synthesis; standard-mode mandatory prescribing-practice + non-English layers folded into Section B (prescribing conventions) + Section C-5 (non-English survey)."
---

# GI-Specialist Medical Agent — Domain Research (Pass-3 Synthesis)

## Executive Summary

A `gi-specialist` agent must be, above all, **an over-claim circuit-breaker for a domain where the marketing is decades ahead of the evidence**. Three structural facts dominate the GI/microbiome space and force the agent's design: (1) the microbiome literature is overwhelmingly *correlational* — diversity and short-chain-fatty-acid associations are real but rarely causal, and the field's own reviews warn of "pseudoscientific commercialization" `[A: 3, mechanism_review]`; (2) the most-sold consumer GI tests are *invalid as labeled* — the commercial zonulin ELISA does not measure zonulin, IgG/IgG4 "food sensitivity" panels are affirmatively contraindicated by four independent allergy societies, and direct-to-consumer microbiome kits show inter-provider variability "on the scale of biological variability between different donors" `[A: 8/9, in_vitro/mechanism_review]` `[C: 3/7, regulatory/mechanism_review]`; and (3) the one compound family the agent owns — probiotics/prebiotics/digestive aids — is strain- and indication-specific (class membership is *not* evidence of effect) and carries a genuine mortality landmine, the PROPATRIA trial, where probiotics raised mortality from 6% to 16% (RR 2.53) and caused fatal bowel ischaemia in predicted-severe acute pancreatitis `[B: 8, rct]`.

The agent therefore exists to hold several pairs of facts apart that the surrounding ecosystem constantly conflates: *correlation vs causation* (microbiome), *mechanism vs human outcome* (gut-barrier agents), *a validated assay vs a commercial test that borrows its name* (zonulin, IgG panels, microbiome kits), *class membership vs compound-level evidence* (probiotics), *malabsorption vs symptomatic intolerance* (breath tests), and *a benign functional label vs an undiagnosed organic disease* (IBS-anchoring in the presence of alarm features). It also exists to recognize a hard floor it must never cross: GI alarm/red-flag features (hemorrhage, perforation, obstruction, dysphagia, weight loss, iron-deficiency anemia, new-onset symptoms at age ≥45) route to in-person clinical care or emergency services — the agent never diagnoses IBS/IBD/celiac/CRC, because that requires examination, serology, and endoscopy it cannot perform.

This synthesis carries **13 Findings** (12 domain findings from the three validated sections + 1 agent-design finding grounded in the inherited project contract pack) and **15 Recommendations** that become the design-doc §3.2 directive list. The single most important risk is **probiotic safety in compromised hosts** (Finding 6): the PROPATRIA mortality signal plus immunocompromised bacteremia/fungemia is exactly the shape of a `risk_tier: medium+` compound write that must trigger the R7 operator-profile precondition and a medical-liaison escalation — and it maps directly onto the agent's owned-write discipline and the mandatory `AUTHORITY_FRAMING_BYPASS` refusal class.

---

## §0 Introduction

**Research question.** What goal-agnostic domain knowledge must ground the design of a `gi-specialist` medical sub-agent in the a-plus-maxing project — across GI/microbiome physiology, the evidence-maturity and safety landscape of GI compounds, GI/inflammation biomarker validity, GI clinical red-flags, consumer GI-test validity, and the inherited agent-design safety contracts — such that the agent produces goal-agnostic vetted GI-library knowledge and performs personalized GI reasoning without crossing the project's medical-safety boundaries?

**Scope.** Three domains were researched as goal-agnostic library knowledge (the GI domain as a class, not pre-filtered for any operator): (A) GI/microbiome physiology, the gut barrier, motility, the food-reaction taxonomy, and the validity of GI/inflammation biomarkers; (B) the GI compound families the agent owns — probiotics, prebiotics/fiber, digestive enzymes, betaine HCl, gut-barrier agents, and motility/symptom agents — with evidence maturity, regulatory status, risk tier, and prescribing-practice conventions; and (C) GI clinical red-flags, the validity of direct-to-consumer GI testing, the elimination-diet/disordered-eating cascade, and the non-English literature survey. A fourth domain (D), agent design, is synthesized here by grounding each agent-behavior conclusion in a named contract from the inherited project pack rather than introducing new external evidence.

**Methodology.** Three paired retrieval+judge sub-agent dispatches were run at `standard` mode (the gi-specialist `risk_class` is `compound-medium`, whose mode floor is `standard` per `templates/specialist-risk-class.yaml`), each iterated to a judge PASS at the standard threshold of 92/100 (A 97 iter-1; B 96 iter-3; C 97 iter-3). The judge gate worked as designed — it caught three real citation-fidelity defects across Sections B and C (an effect-size misattribution, a comment-letter-vs-primary PMID error, a non-primary aggregator mistagged `cohort`, plus a falsified byline and a wrong DOI surfaced during remediation) and iterated each to clean convergence with *fresh independent judges*, never orchestrator self-attestation (PF-S2-02 / PF-S3-01 discipline). A Phase-4.75 integrity verifier then independently swept the corpus (13 IC checks + population-mismatch + concentration-audit), returning PASS with a gate_attest-produced verdict and an intact attestation chain. This document is a **corpus-read-only synthesis**: no new web retrieval was performed, and every numerical claim carried forward already appears, type-tagged, in section A/B/C, with its `[population-mismatch: <species>]` annotation preserved for any animal/in-vitro number.

**Key assumptions.** (1) The three section files passed their judge gates and their type-tags are authoritative — this synthesis preserves, never re-derives, them. (2) The contract-pack documents (refusal taxonomy, H-class scheme, GRADE two-axis, anti-sycophancy mechanisms, R7 operator-profile precondition, escalation routes to the live medical-liaison, the wiki-consumption contract) are the binding project-internal interfaces the specialist inherits; Section-D findings reference them by name and do not invent contract semantics. (3) Biomarker performance figures (sensitivities/specificities) and effect sizes are reported as of the section files' May-2026 retrieval window. (4) Per PF-S2-04, this is goal-agnostic library knowledge: operator-profile/current-state/goals were loaded as context for linkage but were NOT injected into the research question; the meta files are presently scaffolds, so any later personalization happens at dispatch, not here.

---

## §1 Findings

### Finding 1 — The microbiome literature is correlational, not causal; the agent must be an over-claim circuit-breaker, never converting a profile into a personalized directive

**Claim.** Most microbiome–disease links are *correlative*; the field's own methods reviews flag over-reliance on correlation, weak reproducibility, publication bias, and "pseudoscientific commercialization" `[A: 3, mechanism_review]`. The strongest causal signal is a bidirectional Mendelian-randomization study (genetic instruments, not an RCT) tying butyrate production to insulin response and impaired propionate handling to T2D risk `[A: 4, cohort]`; high-level controlled-trial evidence that SCFAs *regulate* human metabolism is "largely lacking" `[A: 1, mechanism_review]`. Country-of-origin out-explained adiposity for SCFA/diversity differences `[A: 5, cohort]` — effects are strain-, dose-, host- and population-specific.

**Maps to:** Identity (the agent IS an over-claim circuit-breaker); Core Rules (no "microbiome shows X → do Y" without an interventional human trial of the *specific* strain/exposure); Anti-Patterns (correlation-as-causation; diversity-as-individual-diagnostic).
**Mechanical check:** any agent output that converts a microbiome/diversity reading into a personalized intervention must cite an interventional human trial of the specific strain/exposure or carry `certainty: low|very-low` + an explicit correlational caveat.

### Finding 2 — Intestinal permeability is a validated mechanism in *specific* diseases, but "leaky gut" as a consumer diagnosis — and the commercial zonulin ELISA — is invalid; the agent must refuse the zonulin number as a permeability measurement

**Claim.** Barrier defects are validated and temporally causal in celiac disease, IBD (permeability precedes Crohn's relapse; raised leak-pathway permeability in first-degree relatives is an independent IBD risk factor), and critical illness `[A: 6/7, mechanism_review]`. But the widely sold commercial zonulin ELISA **does not detect pre-haptoglobin-2** (the purported zonulin); it recognizes properdin and cross-reacts with C3/albumin `[A: 8, in_vitro]`, measures "zonulin family peptides" not zonulin, correlates poorly with functional permeability `[A: 9, mechanism_review]`, and commercial-kit serum zonulin failed to correlate with the lactulose/mannitol gold standard in Crohn's first-degree relatives `[A: 10, cohort]` `[C: 13, cohort]`. The disconfirming evidence comes from *independent* groups, so the "ELISA invalid" verdict is not single-lab-dependent.

**Maps to:** Core Rules (affirm permeability-in-celiac/IBD; refuse zonulin-as-readout); Refusal class `BASIS_NOT_REVIEWABLE` / invalid-test refusal; Anti-Patterns (relaying a zonulin number as a permeability measurement).
**Mechanical check:** any output referencing a commercial zonulin/"leaky gut" test result states the assay-validity problem and does not assign it a quantitative permeability meaning.

### Finding 3 — GI/inflammation biomarkers stratify by validity; the agent must carry per-marker validity and never treat a number as a diagnosis

**Claim.** Validity is marker-specific: **fecal calprotectin** discriminates IBD from IBS well (pooled sens ~93% / spec ~94% at 50 µg/g; a 2023 meta gives 85.8%/91.7%) but is non-specific to a diagnosis `[A: 18/19, meta_analysis]`; **FIT** outperforms gFOBT (sens 0.79 / spec 0.94 for CRC) but is a colonoscopy-*referral* trigger, not a diagnosis `[A: 21, meta_analysis]`; **hs-CRP** and **fecal sIgA** are non-specific and must never decision-drive alone `[A: 23/24, mechanism_review/meta_analysis]`; **breath tests** — lactose-H₂ is well-validated (sens 90–100%), SIBO breath testing is contested (sens 20–93%, lactulose controversy, ~45% control positivity), fructose adds little over a dietary trial, and malabsorption ≠ symptomatic intolerance `[A: 25/26/27, mechanism_review]` `[C: 11, mechanism_review]`; **DTC microbiome/stool kits** lack analytic and clinical validity and have no regulator-approved diagnostic status `[A: 28/29, in_vitro/regulatory]`.

**Maps to:** Core Rules (per-marker validity discipline; biomarker writes carry validity confidence); Communication (biomarker readouts reported with their non-specificity); Anti-Patterns (number-as-diagnosis; single-marker decisions).
**Mechanical check:** a biomarker output names what the marker validly measures AND what it does NOT establish; a "rule-in diagnosis" claim from a single non-specific marker is refused.

### Finding 4 — The food-reaction taxonomy is load-bearing; IgE allergy ≠ enzymatic intolerance ≠ FODMAP ≠ NCGS (a diagnosis of exclusion), and IgG/IgG4 panels are the wrong assay class

**Claim.** Adverse food reactions split cleanly by mechanism: IgE-mediated allergy (skin-prick/specific-IgE + oral challenge), non-IgE/mixed immune (celiac, FPIES, EoE), enzymatic intolerance (lactase deficiency), pharmacologic/chemical, FODMAP/fermentable-carb intolerance, and non-celiac gluten/wheat sensitivity — **NCGS being explicitly a diagnosis of exclusion** requiring negative celiac serology/biopsy AND negative wheat-IgE first `[A: 15/16, mechanism_review]`. The validated allergy assay is specific *IgE*; commercial IgG "food sensitivity" panels are outside this taxonomy entirely.

**Maps to:** Core Rules (hold the taxonomy; never conflate allergy with intolerance); the invalid-test refusal class; Context Loading (food-reaction taxonomy is a static grammar).
**Mechanical check:** any "food sensitivity" claim is classified into the validated taxonomy or refused; an IgG/IgG4 panel is never accepted as evidence for any category.

### Finding 5 — Probiotics are strain- AND indication-specific; class membership is not evidence of effect, and the strongest indications are narrow

**Claim.** The 2020 AGA technical review's 55 RCTs tested 44 different species/strains/combinations — for most products the evidence base is a single trial, so class membership ("it's a probiotic") is not evidence `[B: 1, meta_analysis]`. The strongest indications are narrow and effect-sized: antibiotic-associated-diarrhea prevention (RR ~0.62; concordant Hempel RR 0.58) `[B: 2/2b, meta_analysis]`, *C. difficile*-associated-diarrhea prevention (RR 0.36, NNT ≈ 12, concentrated in high-risk patients) `[B: 3, meta_analysis]`, and chronic-pouchitis maintenance with the specific VSL#3 formulation (relapse RR ~0.17) `[B: 4/5, rct/meta_analysis]`. The 2020 AGA and 2021 ACG guidelines recommend *against* routine probiotics for IBS and acute gastroenteritis `[B: 6/7, practitioner_protocol]`.

**Maps to:** Core Rules (strain×indication specificity; mirror guideline restraint); Anti-Patterns (class-membership-as-efficacy); owned-write discipline for `compounds` (probiotic class).
**Mechanical check:** a probiotic recommendation names the specific strain/formulation AND indication with a matching trial; a "good for gut health" generic probiotic claim is downgraded/refused.

### Finding 6 — PROPATRIA is the canonical safety landmine: probiotics are `risk_tier: medium+` in compromised hosts and trigger the R7 precondition + medical-liaison escalation

**Claim.** In predicted-severe acute pancreatitis, an enteral multispecies probiotic raised mortality to 16% vs 6% placebo (RR 2.53, 95% CI 1.22–5.25) and caused bowel ischaemia in 9 patients (8 fatal) vs 0 (p=0.004) `[B: 8, rct]`. Probiotic organisms translocate and cause invasive infection in compromised hosts — *S. boulardii* fungemia in ICU patients (pooled ~93% had a central line, ~88% on broad-spectrum antibiotics) `[B: 11, cohort]`. Risk is `low` in healthy immunocompetent adults but escalates to **`medium→high`** in the critically ill, immunocompromised, central-line, or predicted-severe-pancreatitis context.

**Maps to:** Ask-vs-Proceed (compound write while operator hard-limit field unpopulated → HALT, R7); Loop-Breaking (medium+ compound → medical-liaison route); Core Rules (probiotic safety contraindication carried explicitly); risk-floor scaffold.
**Mechanical check:** a probiotic write at `risk_tier: medium+` (immunocompromised/critically-ill/central-line) carries the contraindication + monitoring + stopping-criterion fields AND routes to the live medical-liaison; an unpopulated operator immune/critical-illness field HALTs the write.

### Finding 7 — GI compounds stratify by evidence maturity and regulatory status; the agent keeps mechanism distinct from clinical outcome and the Rx boundary distinct from OTC

**Claim.** The owned families span: strong-evidence-for-a-defined-indication Rx (PERT for exocrine pancreatic insufficiency — improves coefficient of fat absorption `[B: 16/17, regulatory/meta_analysis]`); good-evidence OTC for a specific indication (lactase for lactose intolerance, ~55% breath-H₂ reduction `[B: 18, rct]`); weak-evidence OTC with a real safety profile (betaine HCl — a transient pharmacodynamic effect only in drug-induced hypochlorhydria, `medium` tier `[B: 20/21, rct/mechanism_review]`); and mechanism-heavy, small-RCT gut-barrier agents (glutamine has a permeability-defined-subgroup RCT `[B: 22, rct]`; zinc-carnosine a single n=10 crossover `[B: 23, rct]`; colostrum `experimental`; SBI a Rx medical food on a sponsor-linked cluster `[B: 24/25, regulatory/rct]`). Peppermint oil has the best symptom-agent IBS evidence (global RR ~2.2–2.4 `[B: 27/28, meta_analysis]`); prokinetics are Rx and must be named-and-routed, never dosed `[B: 32, regulatory]`.

**Maps to:** Core Rules (mechanism ≠ outcome; Rx-boundary refusal); Role Boundaries (owns OTC/supplement digestive aids, NOT Rx prokinetics/PERT dosing); GRADE two-axis tagging.
**Mechanical check:** a gut-barrier/enzyme efficacy claim separates `mechanism` from `human_outcome` and carries a GRADE certainty tag; a prescription prokinetic/PERT dose directive is refused and routed.

### Finding 8 — Prescribing-practice conventions exist but are `practitioner_protocol`/`regulatory`, never efficacy; cycling claims are marketing

**Claim.** Documented dosing conventions (probiotic CFU 1–50 billion/day strain-specific; psyllium titrated >10 g/day with fluid; inulin/FOS/GOS started low to limit gas; peppermint enteric-coated ~180–225 mg TID; ginger ≤1–1.5 g/day) are `practitioner_protocol`/`regulatory` and may ground dose/route/cycle but never efficacy `[B: 6/13/14/7/29, practitioner_protocol]`. No robust evidence mandates cycling for any of these families — cycling is convention/marketing `[B: 21, mechanism_review]`.

**Maps to:** Tools (the `compounds` prescribing-practice scaffold); Core Rules (practitioner/compounding cites ground dose only); Anti-Patterns (cycling-as-efficacy).
**Mechanical check:** any dose/cycle convention carries a `practitioner_protocol`/`compounding_data_sheet`/`regulatory` tag and is not used to ground an efficacy claim.

### Finding 9 — GI alarm/red-flag features split TIME-CRITICAL vs urgent-referral and are floor behaviors that fire regardless of how benign the rest looks

**Claim.** Per the ACG/CAG dyspepsia and ACG IBS guidelines `[C: 1/2, regulatory]`: TIME-CRITICAL (emergency, no triage dialogue) = hematemesis/coffee-ground emesis, melena, hematochezia with hemodynamic change, acute severe/peritoneal abdominal pain, intractable vomiting with obstruction signs, jaundice-with-fever (cholangitis). Urgent-referral (in-person clinician before further self-management) = dysphagia/odynophagia, unintentional weight loss, iron-deficiency anemia/occult bleeding, palpable mass, new-onset symptoms at age ≥45 (CRC; USPSTF lowered screening to 45 `[C: 9, regulatory]`) or ≥60 (dyspepsia endoscopy), nocturnal symptoms, family history of CRC/IBD.

**Maps to:** Loop-Breaking (TIME-CRITICAL → `TIME_CRITICAL` refusal card, stop; urgent-referral → clinician-routing gate); Ask-vs-Proceed (critical floor); Refusal classes (`TIME_CRITICAL`, `PATIENT_FACING_DIRECTIVE`).
**Mechanical check:** a presented alarm feature produces the matching floor behavior (emergency redirect or urgent-referral gate) with zero self-management content before it.

### Finding 10 — An LLM must not diagnose; IBS is a clinician's positive diagnosis reachable only after alarm-feature exclusion the agent cannot perform

**Claim.** IBS is defined by Rome IV symptom criteria and is a *positive* diagnosis made **after** alarm features are excluded — not a default label applied when tests are normal `[C: 1, regulatory]`. A positive-diagnostic strategy is non-inferior to exhaustive exclusion *only* once alarm features are screened out `[C: 10, rct]`. Distinguishing IBS from early IBD/celiac/CRC requires examination, serology/calprotectin, and often endoscopy with biopsy — none of which an LLM can perform. Anchoring on a benign functional label in the presence of an alarm feature is the named failure mode.

**Maps to:** Role Boundaries (no diagnosis; recognize-and-route); Refusal classes (`PATIENT_FACING_DIRECTIVE`, `HIGH_RISK_SAMD` for diagnose/treat); Anti-Patterns (functional-label anchoring).
**Mechanical check:** the agent never assigns/confirms an IBS/IBD/celiac/CRC/functional-dyspepsia label; a request to diagnose maps to a refusal class + clinician routing.

### Finding 11 — Consumer/DTC GI tests (IgG/IgG4 panels, microbiome kits, SIBO breath, zonulin) are invalid; the agent refuses to relay them as meaningful

**Claim.** IgG/IgG4 food panels are affirmatively not recommended by four independent allergy societies (EAACI, AAAAI, CSACI, ASCIA) — IgG4 reflects tolerance, not hypersensitivity `[C: 3/4/5/6, regulatory]`; DTC microbiome kits show inter-provider variability on the scale of inter-donor biological variability and "lack analytical and clinical validity" `[C: 7/8, mechanism_review]`; SIBO breath tests have no gold standard and ~45% control-positivity `[C: 11, mechanism_review]`; commercial zonulin ELISA is invalid `[C: 12/13, mechanism_review/cohort]`. The four-society convergence makes the IgG/IgG4 refusal the strongest anchor.

**Maps to:** Refusal classes (invalid-test refusal; `BASIS_NOT_REVIEWABLE`); Core Rules (state the validity problem, do not relay the result); Modes (refusal-escalation).
**Mechanical check:** an IgG/IgG4 panel, DTC microbiome kit, standalone SIBO breath result, or zonulin number is met with the validity refusal, never interpreted as actionable.

### Finding 12 — Invalid testing ignites an elimination → orthorexia/restrictive-ED cascade; the agent refuses the ignition source and DEFERS the ED critical floor to the nutritionist

**Claim.** Unsupervised elimination driven by invalid testing is a documented vector into disordered eating: in a food-allergy cohort, 74% of those with food allergy + an eating disorder used elimination diets, only 15% medically supervised, and ED-symptom prevalence was ~50% vs ~6.7% in healthy peers `[C: 14, cohort]`. The loop — invalid IgG panel → "reactive food" list → food-fear elimination → orthorexia/ARFID — is blocked at the ignition source (refuse the invalid panel). The **eating-disorder critical floor is owned by the `nutritionist` agent**; the gi-specialist defers to it, never re-implements or independently prescribes elimination diets.

**Maps to:** Role Boundaries (ED floor owned by nutritionist; do NOT prescribe elimination diets); cross-role escalation; Anti-Patterns (validating invalid food-sensitivity testing).
**Mechanical check:** the agent does not validate an invalid food-sensitivity panel or prescribe an unsupervised elimination diet; an ED signal routes to the nutritionist's owned floor.

### Finding 13 (agent-design) — The specialist inherits the project safety architecture verbatim and never redefines it

**Claim.** The gi-specialist inherits, by reference, the project contract pack: the 8-class refusal taxonomy with `AUTHORITY_FRAMING_BYPASS` mandatory (operator classed A3; the 81.8%-of-successful-attacks vector) `[templates/refusal-class-taxonomy.yaml]`; the GRADE two-axis (`certainty` × `strength`) with the strong-with-low HALT; the H-class harm scheme (`max(nominal, worst_case_reachable)`, H1/H2 auto-block); the three-mechanism anti-sycophancy scaffold (Role 1); the R7 operator-profile precondition for compound-class writes; escalation to the **live** medical-liaison via `BLOCK_WITH_OVERRIDE_PATH` (the pre-Role-7 operator-self-override fallback is deprecated); and the wiki-consumption contract (consume, never author — PF-S2-04). The specialist dispatches research only via `aplus-research --mode=standard --target-class=compound` (its risk-class floor), never bare `deep-research`, and never self-attests a gate (PF-S2-01 / PF-S3-01).

**Maps to:** Role Boundaries (inherit-not-redefine; ≥4 refusal classes incl. AUTHORITY_FRAMING_BYPASS); Tools (`aplus-research --mode=standard --target-class=compound` floor); Context Loading (auto-load the contract pack); Anti-Patterns (self-attestation, writing from memory).
**Mechanical check:** `scripts/audit-specialist-profile.sh` — refusal-classes ≥4 incl. AUTHORITY_FRAMING_BYPASS, mode-floor=standard, GRADE-halt present, anti-sycophancy A/B/C, ≥3 resolving PF ids, no operator-content leak.

---

## §2 Recommendations (→ design-doc §3.2 directive list)

| # | Recommendation | Verdict | Maps to agent.md |
|---|---|---|---|
| R1 | Frame the agent's Identity as an over-claim circuit-breaker for the microbiome/GI domain (correlation ≠ causation; mechanism ≠ outcome; commercial-test-name ≠ validated assay). | ACCEPTED | Identity |
| R2 | Encode the validated food-reaction taxonomy (IgE allergy / non-IgE / enzymatic / pharmacologic / FODMAP / NCGS-by-exclusion) as a static grammar the agent holds. | ACCEPTED | Core Rules, Context Loading |
| R3 | Carry per-marker biomarker validity (calprotectin, FIT, hs-CRP, sIgA, breath tests, DTC kits) — every biomarker output names what it validly measures AND what it does not establish. | ACCEPTED | Core Rules, Communication |
| R4 | Refuse to relay invalid consumer GI tests as meaningful: IgG/IgG4 food panels, DTC microbiome kits, standalone SIBO breath, zonulin/"leaky gut" — invalid-test refusal class. | ACCEPTED | Role Boundaries (refusal), Modes |
| R5 | Hold probiotic reasoning to strain × indication specificity; mirror AGA/ACG guideline restraint; reject class-membership-as-efficacy. | ACCEPTED | Core Rules, Anti-Patterns |
| R6 | Carry the PROPATRIA + immunocompromised probiotic safety contraindication; a `risk_tier: medium+` probiotic write triggers the R7 operator-profile precondition + medical-liaison route. | ACCEPTED | Ask-vs-Proceed, Loop-Breaking, Core Rules |
| R7 | Keep mechanism distinct from human outcome for gut-barrier/enzyme agents; GRADE-tag every recommendation; permeability ≠ clinical outcome. | ACCEPTED | Core Rules, Communication |
| R8 | Encode the Rx boundary: name-and-route prescription prokinetics, PERT dosing, and SBI medical-food — never dose them; the agent owns OTC/supplement digestive aids only. | ACCEPTED | Role Boundaries, Tools (restrictions) |
| R9 | Encode the GI alarm-feature floor: TIME-CRITICAL → emergency redirect (no triage); urgent-referral → clinician gate; both fire unconditionally. | ACCEPTED | Loop-Breaking, Ask-vs-Proceed |
| R10 | No-diagnosis floor: never assign/confirm IBS/IBD/celiac/CRC/functional-dyspepsia; recognize-and-route only. | ACCEPTED | Role Boundaries, Negative Examples |
| R11 | Defer the eating-disorder critical floor to the `nutritionist`; refuse the invalid-test ignition source; never prescribe unsupervised elimination diets. | ACCEPTED | Role Boundaries, Anti-Patterns |
| R12 | Encode ≥4 refusal classes incl. mandatory `AUTHORITY_FRAMING_BYPASS`; route `BLOCK_WITH_OVERRIDE_PATH` to the live medical-liaison. | ACCEPTED | Role Boundaries |
| R13 | Declare the research dispatch floor `aplus-research --mode=standard --target-class=compound`; never bare `deep-research`; never self-attest a gate. | ACCEPTED | Tools, Anti-Patterns |
| R14 | Consume the wiki, never author it during design; owned runtime writes are `biomarkers` (GI), `protocols` (gut), `compounds` (probiotics/prebiotics/digestive aids) + `meta/contradictions.md`; cross-read `protocols/meal-template` (nutritionist) read-only. | ACCEPTED | Role Boundaries, Context Loading |
| R15 | Three-mechanism anti-sycophancy + GRADE strong-with-low HALT + H-class auto-block carried verbatim from Role 1; never redefine. | ACCEPTED | Core Rules, Loop-Breaking |

(No DEFERRED/REJECTED recommendations — all 15 are directly implementable in the agent.md from the validated corpus + contract pack.)

---

## §3 Standard-mode gate dispositions (Phase 7.5 + 8.5)

This is a **design-research dispatch** (peptide-specialist precedent), not a single-compound vault ingest, so the Phase-8 vault-write packaging does not apply (PF-S2-04). The two standard-mode compound gates are satisfied in-corpus:

- **Phase 7.5 RISK-FLOOR (folded, PASS-by-fillability).** No single `risk_tier: experimental` vault compound entry is being written. The risk-floor *readiness* requirement — that for every medium+/experimental GI compound family the contraindications + monitoring (named biomarker/sign) + stopping-criteria fields are fillable from retrieved sources — is satisfied by Section B's risk-tier table: probiotics-in-critically-ill (`medium→high`), betaine HCl (`medium`), colostrum (`experimental`), SBI (`low–medium`), and prokinetics (`clinician-only`) each carry adverse effects + contraindication + monitoring + stopping criterion. The judge gate scored Section B's `risk_floor_readiness` dimension explicitly (part of the 96/100 PASS).
- **Phase 8.5 LAYERS (folded, PASS-in-section).** The standard-mode mandatory prescribing-practice layer is folded into Section B's "Prescribing-practice conventions" subsection (AGA 2020 / ACG 2021 `practitioner_protocol` + regulatory dosing references). The mandatory non-English literature layer is folded into Section C-5, which documents the survey scope (Japanese LcS/Yakult, European Nestlé/Danone, Russian bioregulator clusters), the databases searched, and an explicit confirmed-absence statement (no admissible non-English Section-C primary beyond English-indexed work). This matches the deployed peptide-specialist design-work, which carried prescribing/regulatory + non-English coverage in its section retrievals rather than as separate vault layer files.

---

## §4 Concentration audit (corpus-level)

The Phase-4.75 integrity verifier computed an aggregate single-cluster share of **0.05** across ~38 distinct primaries — far below the 0.70 threshold; the GI corpus is multi-group and diverse. Two localized single-source flags were surfaced and handled in-section rather than buried: (1) the **zonulin construct** originates with the Fasano group, but the *disconfirming* evidence (Scheffler/Schulzke; Massier; the Crohn's-FDR cohort) is from independent groups, so the "ELISA invalid" verdict is not single-lab-dependent (Section A); (2) the **SBI** gut-barrier evidence rests on a narrow sponsor-linked cluster, flagged first-class with low certainty (Section B-5). Neither triggers the ≥70% first-class-section requirement.

---

## §5 Provenance & gate trail (for the integrator)

- `sections/section-A.md`, `section-B.md`, `section-C.md` — real dispatched retrieval, type-tagged, with `## Bibliography` + `## Self-check` (+ `## Post-fix grep audit` for B/C).
- `judges/judge-A.json` (PASS 97, iter-1), `judge-B.json` (PASS 96, iter-3), `judge-C.json` (PASS 97, iter-3) — fresh dispatched judges; iteration-stamped copies preserved (`judge-{A-iter1,B-iter3,C-iter3}.json`).
- `gates/gate-2.75.json` (scope, schema-valid PASS), `gates/gate-3.5-summary.md` (judge-gate outcome record), `gates/gate-4.75.json` + `gate-4.75.md` (integrity gate, **gate_attest-produced**, attestation_chain intact, `verify-chain` PASS).
- `dispatch-ledger.jsonl`, `plan.md`, `rubric.md`.

The judge gate caught and converged 3 real citation-fidelity defects with independent verifiers (PF-S2-02 / PF-S3-01 discipline working) — this is dispatched-agent provenance, not orchestrator self-attestation or prose-only.
