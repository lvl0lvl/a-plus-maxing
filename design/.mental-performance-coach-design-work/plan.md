# Phase 2 PLAN + Phase 2.5 RUBRIC — mental-performance-coach domain research

**Dispatch type:** design-research (peptide/gi precedent), NOT a single-entity vault ingest.
**Mode:** `standard` · **target_class:** `protocol` · **target_type:** `reference` · **slug:** `mental-performance-coach`
**risk_class:** `protocol-medium` (`templates/specialist-risk-class.yaml`) → `mode_floor: standard`.
**Gates that fire (standard):** 2.75 SCOPE (done, PASS) · 3.5 JUDGE (thr 92) · 4.25 ID-RECONCILE · 4.75 INTEGRITY. Compound-only gates 7.5 RISK-FLOOR + 8.5 LAYERS + the mandatory prescribing-practice/non-English LAYERS are **N/A** for protocol research; the non-English survey is folded into Section C-5 (gi precedent). Phase-6 CRITIQUE is skipped at standard.
**Provenance:** gates committed under canonical bare `gates/` (bead 0be — NO `research-` prefix). NO writes to `vault/` (PF-S2-04: meta files loaded for linkage, NOT injected into the goal-agnostic research question; operator-profile is a scaffold).

## Research question (goal-agnostic)

What goal-agnostic domain knowledge — the evidence-graded landscape of cognition/focus/working-memory and its established lifestyle levers (exercise-, sleep-, nutrition-cognition links), stress physiology and resilience under load, the nootropic / cognitive-enhancer compound landscape (evidence maturity, regulatory status, safety, prescribing conventions), the validity of consumer cognitive-performance products, AND — load-bearing — the mental-health safety boundary (depression/anxiety/burnout screening, suicidality detection + escalation) that separates a PERFORMANCE coach from a mental-health PROVIDER, plus the inherited a-plus-maxing agent-design safety contracts — must ground the design of a `mental-performance-coach` sub-agent that consumes the project wiki, writes cognitive/stress PROTOCOLS + mental PARAMETERS, reads the cognitive COMPOUND class, escalates compound authoring to supplement-specialist, and never crosses the mental-health-care boundary?

## Section partition (3 paired retrieval+judge dispatches)

**Section A — Cognition + stress physiology + the established lifestyle levers.**
- Focus / working memory / processing speed / executive function — construct definitions, what is trainable vs trait.
- LEAD WITH THE ESTABLISHED LEVERS (kickoff directive): exercise→cognition (aerobic + resistance; executive-function meta-analyses; BDNF mechanism), sleep→cognition (deprivation effects on attention/working memory; consolidation), nutrition→cognition (Mediterranean diet, omega-3, glucose/hydration acute effects).
- Stress physiology: HPA axis, cortisol, acute vs chronic stress, allostatic load, Yerkes-Dodson / arousal-performance curve, performance under load.
- Resilience: psychophysiological recovery, HRV↔stress link, recovery practices (overlap recovery-specialist — cross-read).
- Cognitive-training TRANSFER validity: working-memory training (n-back) far-transfer debate; the field's own skepticism.

**Section B — Nootropic / cognitive-enhancer compound landscape (evidence-graded, hype-resistant).**
- Caffeine (alertness/vigilance, dose-response, tolerance, withdrawal), L-theanine (+caffeine synergy), creatine-for-cognition (sleep-deprivation + vegetarian subgroups; recent meta-analyses), omega-3/DHA.
- Adaptogens / herbals: Rhodiola rosea, Bacopa monnieri, L-tyrosine (acute stressor cognition), Panax ginseng — evidence maturity, heterogeneity, AE.
- Prescription cognitive enhancers off-label in HEALTHY adults: modafinil, methylphenidate, amphetamine — the actual effect-size evidence, the safety/dependence/legal boundary, why this routes to PRESCRIPTIVE_DIRECTIVE + medical-liaison.
- Regulatory status, AE profiles, prescribing-practice conventions.
- **Boundary discipline:** coach READS `compounds` (cognitive class) but ESCALATES compound-entry authoring to supplement-specialist via Architecture Question (risk-class worked-example-B). Section B documents the landscape goal-agnostically; it does NOT make the coach a compound author.

**Section C — Mental-health safety boundary + consumer-product validity + non-English survey (LOAD-BEARING SAFETY).**
- The PERFORMANCE-coach vs mental-health-PROVIDER boundary — the single most important design fact.
- Depression / anxiety / burnout: screening instruments (PHQ-9, GAD-7, Maslach burnout, ICD-11 burnout) and why a performance coach must NOT screen/diagnose but ESCALATE.
- Suicidality: detection of active AND passive/oblique/masked ideation; C-SSRS framing; 988 Suicide & Crisis Lifeline; the imperative to escalate (EMERGENCY) not coach; benign-trailing-request-never-cancels; minimization-never-downgrades (mirror + intensify sleep-coach).
- Stimulant/nootropic MISUSE → mental-health risk (anxiety, induced psychosis, dependence, withdrawal).
- Consumer cognitive-product validity: "brain training" (Lumosity FTC $2M settlement 2016; the scientific consensus statement); wearable "stress/readiness/focus" score validity.
- Overtraining/burnout-syndrome boundary (cross-read recovery-specialist).
- §C-5 NON-ENGLISH SURVEY (folded mandatory layer): Russian nootropic literature (Semax, Selank, Noopept — Institute of Molecular Genetics RAS / Zakusov Institute) — evidence-quality + concentration-of-source caveat.

**Section D — agent design (synthesized in domain-research.md, NOT a retrieval section).** Each agent-behavior conclusion grounded in a NAMED inherited contract: refusal taxonomy (8 classes; AUTHORITY_FRAMING_BYPASS mandatory; TIME_CRITICAL the load-bearing SI floor), GRADE two-axis, H-class scheme, anti-sycophancy mechanisms A/B/C, R7 operator-profile precondition, escalation to the LIVE medical-liaison (`BLOCK_WITH_OVERRIDE_PATH`), the wiki-consumption contract, WIKI Agent-Consumers row (reads operator-profile/current-state/compounds[cognitive]; writes cognitive protocols + mental parameters).

## Triangulation rule
A numerical claim appearing in 2+ sections must match (else `meta/contradictions` note). Each section ≥15 admissible primaries (standard floor 15+); deduplicated corpus target >35 distinct primaries. Cross-section shared entities (PMID/DOI, instruments like PHQ-9/GAD-7/C-SSRS, the 988 line, the Lumosity FTC case, named institutes) reconciled at Phase 4.25.

## Search angles per section
- A: "aerobic exercise executive function meta-analysis", "resistance training cognition older adults", "sleep deprivation working memory", "Mediterranean diet cognitive decline RCT", "HPA axis cortisol cognitive performance", "Yerkes-Dodson arousal performance evidence", "working memory training far transfer meta-analysis".
- B: "caffeine cognitive performance dose response", "L-theanine caffeine attention RCT", "creatine cognition meta-analysis sleep deprivation", "modafinil healthy adults cognitive enhancement systematic review", "methylphenidate healthy non-ADHD cognition", "Rhodiola rosea fatigue RCT", "Bacopa monnieri memory meta-analysis", "tyrosine stress cognition".
- C: "performance coach vs mental health provider scope", "PHQ-9 GAD-7 screening validity primary care", "passive suicidal ideation detection", "Columbia suicide severity rating scale", "988 suicide crisis lifeline", "stimulant misuse psychosis healthy adults", "Lumosity FTC settlement brain training", "consensus brain training claims Stanford", "wearable stress score validity HRV", "Semax Selank Noopept clinical evidence review".

## Quality gates (Phase 2.5 RUBRIC dimensions — judge scores each 0-100; standard threshold 92)
1. `evidence_quality` — study-design appropriateness; human RCT/meta-analysis lead for human-outcome claims.
2. `citation_fidelity` — first-author/year/PMID/DOI match the cited source (PF-S2-02).
3. `type_tag_discipline` — every `[N, tag]` carries exactly one whitelist enum tag; vendor/anecdote never ground numerical.
4. `population_annotation` — every animal/in-vitro claim carries species + `[population-mismatch: <species>]`; human-vs-animal generalization explicit (esp. Russian-nootropic animal data, BDNF mechanism).
5. `route_fidelity` — no route/formulation extrapolation without `[route-extrapolation]` (e.g., intranasal Semax vs oral).
6. `concentration_audit_handling` — single-lab/single-group share flagged if ≥70% for any compound (Russian nootropics = canonical risk: Institute of Molecular Genetics RAS dominance).
7. `risk_floor_readiness` — N/A for protocol research (null); BUT the SAFETY-BOUNDARY readiness (escalation fields fillable: SI detection, screening-instrument escalation, stimulant-misuse contraindication) is scored under reasoning_integrity + completeness.
8. `reasoning_integrity` — correlation-vs-causation held apart; mechanism-vs-human-outcome held apart; performance-vs-clinical-care boundary never blurred; hype resisted (brain-training, nootropic over-claims).
9. `completeness_vs_brief` — section covers its assigned scope incl. the load-bearing safety items (Section C: SI detection active+passive, escalation, FTC, non-English).

### Health-specific rubric additions (per aplus-research Phase 2.5)
- **Concentration audit:** count distinct primaries by lab/group affiliation; flag ≥70% single-cluster (Russian nootropic literature is the watch item).
- **Population annotation:** every animal cite carries species + n; mechanism-from-animal never upgraded to human-outcome certainty.
- **Route fidelity:** no route extrapolation without explicit tag.
- **Safety-boundary readiness (protocol-domain analog of risk-floor):** the agent's escalation surface (active/passive SI → EMERGENCY/URGENT; depression/anxiety/burnout → medical-liaison; stimulant misuse → contraindication + escalation) must be fillable from retrieved sources — Section C must carry it.
