# Phase 2 — PLAN (recovery-specialist Pass-3 domain research)

**Mode:** standard (risk_class `protocol-low`, mode_floor `standard`, target_class `protocol` per `templates/specialist-risk-class.yaml`).
**Target:** `{class: other, slug: recovery-specialist, type: reference}` — this is *domain research to build the specialist agent*, not a single vault protocol entry (mirrors the merged gi-specialist precedent). Output → `design/.recovery-specialist-design-work/domain-research.md`. **No vault writes** (PF-S2-04; goal-agnostic library/domain research).
**Compound-only gates N/A:** 7.5 RISK-FLOOR + 8.5 LAYERS + mandatory prescribing/non-English layers fire only for `target_type=compound`. This is reference/protocol → those are SKIP. Cross-section identity reconciliation (4.25) is folded into the Phase-4.75 integrity verifier's IC-10 (gi precedent).

## Domain scope (from kickoff)
Training recovery, HRV/RHR/sleep-derived readiness, overtraining/overreaching, autonomic balance, recovery modalities (sauna/cold/compression/massage/active recovery — each evidence-graded). **Scope boundary with deployed `sleep-coach`** (sleep-coach owns sleep behavior/insomnia/disorder-screening; recovery owns training-recovery + autonomic balance — cross-read, don't duplicate). Red-flags: persistent unexplained fatigue, resting tachycardia, suspected illness → medical-liaison. Oura wearable: design for it (operator purchase pending).

## Section decomposition (4 parallel paired retrieval+judge dispatches)

- **Section A — Recovery metrics & autonomic interpretation.** HRV (rMSSD/lnRMSSD, time- vs frequency-domain, what vagal tone means), RHR, sleep-derived "readiness" scores. Measurement confounds (alcohol, illness, hydration, body position, measurement time, age, training load). Individual baseline + rolling-average/CV interpretation vs single-value over-reading. Wearable validity vs ECG/PSG gold standard — **Oura ring specifically**, plus WHOOP / Apple Watch / chest straps. The proprietary "readiness/recovery score" black-box problem. HRV-guided training: what the evidence supports and its limits.
- **Section B — Overtraining, overreaching & load management.** Functional overreaching (FOR) vs non-functional overreaching (NFOR) vs overtraining syndrome (OTS); OTS as a diagnosis of exclusion with **no validated standalone biomarker**. Autonomic markers (parasympathetic vs sympathetic OTS subtypes). Monitoring: session-RPE, acute:chronic workload ratio (ACWR) **and the methodological controversy around it**, TQR, POMS/mood, daily wellness questionnaires. Deload programming (evidence vs convention). Detraining timelines.
- **Section C — Recovery modalities (evidence-graded; resist hype).** Sauna/heat (separate the CV-mortality cohort evidence from training-recovery claims), cold-water immersion / cold plunge (perceived-recovery & DOMS benefit **vs the interference effect blunting strength/hypertrophy adaptation**), contrast therapy, compression garments, massage / foam rolling / percussive devices, active recovery, photobiomodulation. Each graded **established vs provisional**. Sleep + nutrition as recovery foundations referenced as boundary pointers, not duplicated.
- **Section D — Safety architecture, red-flags & boundary discipline.** Red-flags → escalation: persistent unexplained fatigue, resting tachycardia, suspected illness/infection (**myocarditis risk of training through febrile illness**), unexplained sustained performance decline, RED-S / low energy availability, mood/sleep disturbance masking pathology (anemia, hypothyroid, depression, infection). Modality contraindications (sauna/cold + uncontrolled hypertension / cardiac disease / pregnancy / recent cardiac event). Boundary discipline (sleep-coach / nutritionist / cardiovascular-specialist / personal-trainer / medical-liaison). Wearable-data-is-not-diagnosis principle. Refusal-class mapping for this agent.

## Search angles (per section, real WebSearch/tavily + WebFetch of primaries)
- A: HRV validity meta-analyses; Oura/WHOOP validation studies (vs ECG/PSG); HRV-guided training RCTs; rMSSD reliability; readiness-score validation literature.
- B: OTS consensus statements (ECSS/ACSM 2013 Meeurusen joint position), FOR/NFOR/OTS taxonomy, ACWR original + critique papers, RED-S / IOC consensus, monitoring-tool validity reviews.
- C: CWI interference-effect RCTs + meta-analyses (Roberts, Fyfe), sauna recovery vs Laukkanen CV cohorts, compression/massage/foam-rolling meta-analyses, photobiomodulation reviews.
- D: myocarditis/exercise-and-infection guidance, sauna/cold contraindication guidance, RED-S red-flags, resting-tachycardia significance.

## Triangulation rule (Phase 4)
Any numerical claim (validity correlation r, effect size, prevalence, threshold) appearing in ≥2 sections must agree; single-source numerics flagged. Concentration audit: dedup primaries across sections; flag if ≥70% from a single lab/group. Population-mismatch: any animal/in-vitro claim carries `[population-mismatch: <species>]`.

## Quality gates (standard mode)
- Source floor: ≥15 unique admissible sources (target ≥25 across 4 sections).
- Judge threshold: 92/100 per section (standard).
- Type-tag discipline: every inline `[N, tag]` from the `_source-whitelist` enum; vendor/anecdote never ground numerics.
- Report floor: ~4,000 words synthesized domain-research.md.

## Dispatch plan
4 retrieval agents (A–D) in parallel → 4 paired judge agents in parallel (Phase 3) → judge gate (Phase 3.5, judges authoritative + gate-3.5-summary.md) → orchestrator triangulation (Phase 4) → integrity verifier dispatch (Phase 4.75, gate_attest.py attested) → orchestrator synthesis (Phase 5) → verify-chain.
