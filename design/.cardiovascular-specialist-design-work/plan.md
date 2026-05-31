# Phase 2 — PLAN (cardiovascular-specialist domain research, mode=standard)

**Dispatch type.** Design-research dispatch (peptide/gi-specialist precedent), NOT a single-compound vault ingest. Output is `domain-research.md` synthesis + gate trail in `design/.cardiovascular-specialist-design-work/`; NO writes to `vault/` (PF-S2-04). Phase-8 vault packaging is replaced by the synthesis; standard-mode mandatory prescribing-practice + non-English layers are FOLDED into Section B (prescribing conventions) + Section D-5 (non-English survey), per gi/peptide precedent.

**Target.** class=`other` (domain reference, not single compound), slug=`cardiovascular-specialist`, type=`reference`. The agent's runtime research-dispatch floor is `aplus-research --mode=standard --target-class=compound` (cardiovascular compounds land at risk_tier medium); this design-research dispatch is reference-type.

**Mode floor.** `compound-medium` → `standard` (judge threshold 92/100) per `templates/specialist-risk-class.yaml`. Standard-mode gates fire: 2.75 SCOPE, 3.5 JUDGE, 4.25 ID-RECONCILE, 4.75 INTEGRITY, 7.5 RISK-FLOOR (folded), 8.5 LAYERS (folded).

## Search angles → 4 paired (retrieval + judge) sections

Cardiovascular is the broadest + highest-safety-weight specialist (cardiac symptoms can be emergencies). 4 sections (mirrors lymphatic 4-section breadth):

- **Section A — Cardiovascular biomarkers, risk markers & CVD risk scoring (validity-focused).** BP measurement standards (auscultatory/oscillometric/ABPM/HBPM; white-coat & masked HTN) + thresholds (ACC/AHA 2017 ≥130/80 vs ESC/ESH ≥140/90) + SPRINT intensive-vs-standard. Lipids: LDL-C vs **ApoB** (particle-count superiority / discordance), **Lp(a)** (Mendelian-randomization causal, ~20% pop elevated, monogenic), HDL (U-shaped, non-causal by MR), triglycerides/remnants (causal by MR). CVD risk scoring: Pooled Cohort Equations/ASCVD, SCORE2/SCORE2-OP, calibration limits; **CAC** (coronary artery calcium, MESA; CAC=0 de-risker). Inflammation: hs-CRP (JUPITER), residual inflammatory risk (CANTOS, LoDoCo2 colchicine). HRV/RHR as prognostic autonomic markers. Search: PubMed/PMC, AHA/ACC + ESC guidelines, MESA/UK-Biobank/MR studies.
- **Section B — Cardiovascular compounds: evidence / safety / regulatory / prescribing.** Statins (CTT per-mmol/L LDL → ~21–22% RR major vascular events; primary vs secondary; SAMS + nocebo SAMSON/StatinWISE; modest new-onset T2D; intensity tiers). Ezetimibe (IMPROVE-IT). PCSK9i (FOURIER evolocumab, ODYSSEY alirocumab), inclisiran (siRNA), bempedoic acid (CLEAR Outcomes, statin-intolerant). Antihypertensives (thiazide/ACEi/ARB/CCB first-line; contraindications). Antiplatelets (aspirin primary-prevention reversal: ASPREE/ARRIVE/ASCEND; secondary still indicated). Omega-3 (REDUCE-IT icosapent vs STRENGTH/VITAL null + mineral-oil-placebo controversy). FOLDS the prescribing-practice layer (guideline-directed dosing = practitioner_protocol/regulatory). Search: CTT/Cochrane meta, landmark RCTs, FDA labels, ACC/AHA + ESC guidelines.
- **Section C — Cardiorespiratory fitness as a CVD-risk modifier.** VO2max as mortality predictor (Mandsager JAMA Netw Open 2018; Kodama 2009 meta — per-MET HR). Zone-2 / polarized training + lactate-threshold + mitochondrial/fat-ox rationale (mechanism_review). HR-based zones (max-HR estimation error, %HRR/Karvonen, threshold-based) + measurement validity. Exercise dose-response (PA guidelines 150/75 min; exercise BP ~5–8 mmHg, lipids, insulin sensitivity). Exercise as CVD prevention + cardiac rehab. Athlete's-heart-vs-pathology literacy (defer screening to clinician). Search: cohort + meta + ACSM/AHA PA guidelines.
- **Section D — Cardiovascular red-flags, symptom literacy, consumer-device validity, safety architecture + non-English survey.** TIME-CRITICAL red-flags (chest pain ± diaphoresis/radiation/exertion → ACS; syncope esp. exertional/cardiac; exertional dyspnea; new severe palpitations; stroke FAST) → EMERGENCY (ACC/AHA 2021 chest-pain guideline, ESC 2018 syncope). Arrhythmia literacy (AF + CHA₂DS₂-VASc literacy-only, PVCs/PACs, brady/tachy). Consumer cardiac device validity (smartwatch single-lead ECG: Apple Heart Study sens/spec + false positives, not diagnostic; cuffless/optical BP AHA-statement validation concerns; PPG-HR accuracy; HRV consumer variability). Safety architecture: inherited contract pack (refusal taxonomy incl TIME_CRITICAL + AUTHORITY_FRAMING_BYPASS mandatory, GRADE two-axis, H-class, anti-sycophancy A/B/C, R7 operator-profile precondition, live medical-liaison escalation, wiki-consumption). Non-English survey (ESC European; China-PAR risk model; Japanese/Russian CV cohorts) — explicit presence/absence. Search: guideline societies, device-validation studies, contract-pack docs (internal).

## Triangulation rule

A numerical claim appearing in ≥2 sections must agree (else → contradictions). Aggregate concentration audit across sections (single-group share; cardiovascular literature is large + multi-group → expect « 0.70). Shared entities (landmark-trial names/registrations, guideline bodies, PMIDs) reconciled at Phase 4.25.

## Quality gates (per mode=standard)

- Source floor ≥15 distinct admissible primaries (target >40 across 4 sections — cardiovascular has a deep RCT base).
- Judge threshold 92/100; every section iterates to PASS with FRESH dispatched judges (no orchestrator self-attestation; PF-S3-01).
- Phase-4.75 integrity verifier: 13 IC checks + population-mismatch + concentration-audit, gate_attest-attested, verify-chain intact.
- Every claim type-tagged from the `_source-whitelist.md` enum; vendor/anecdote never ground a numeric.

## Parallel agent plan

4 retrieval agents dispatched (parallel), each paired with a judge (dispatched after its retrieval returns). Re-dispatch any HALT section with judge findings injected (max 3 iters). Then 1 ID-Reconcile agent (4.25), 1 Integrity Verifier (4.75), then orchestrator corpus-read-only synthesis (Phase 5 → domain-research.md). Phases 7.5/8.5 folded as synthesis dispositions.
