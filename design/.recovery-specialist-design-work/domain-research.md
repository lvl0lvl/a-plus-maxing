---
title: recovery-specialist — Domain Research (Pass-3 Synthesis)
type: domain-research
slug: recovery-specialist
mode: standard
target_class: protocol
target_type: reference
created: 2026-05-31
provenance: design/.recovery-specialist-design-work/{gates,judges,sections}/
gate_chain: gate-2.75 PASS · gate-3.5 PASS (4/4 judges) · gate-4.75 PASS (verify-chain intact)
---

# recovery-specialist — Domain Research (Pass-3 Synthesis)

## Executive Summary

The `recovery-specialist` agent owns training recovery, autonomic-balance interpretation (HRV/RHR/sleep-derived readiness), the overtraining/overreaching continuum, and recovery modalities (sauna, cold, compression, massage, active recovery). The dominant finding across all four research sections is that **this domain is saturated with confidently-marketed numbers that the evidence does not support**: proprietary "readiness scores" are unvalidated black boxes, wearable frequency-domain HRV is not trustworthy, the acute:chronic workload ratio is methodologically contested, overtraining syndrome has no validated biomarker, and most recovery modalities have a small perceptual kernel wrapped in overstated marketing. The agent's defining posture is therefore **hype-resistance + circuit-breaking**: interpret HRV/RHR/readiness against the user's own rolling baseline (never a single absolute value, never a cross-brand score), grade every modality honestly (the cold-water-immersion *interference effect* — blunted hypertrophy — is the headline goal-conditional trade-off), and treat any wearable number as a trend prompt, never a diagnosis.

The agent is a **non-diagnostic recovery monitor with a hard safety floor**. It does not diagnose overtraining syndrome (a diagnosis of exclusion that demands a clinician's organic-disease workup), and it routes a tight set of red-flags — persistent unexplained fatigue/performance decline, sustained resting tachycardia, fever/systemic illness + training (myocarditis risk), RED-S, severe mood/sleep disturbance — to the live medical-liaison, escalating the chest-pain/syncope/palpitations cluster as an EMERGENCY. It defers sleep behavior to `sleep-coach`, fueling/energy-availability to `nutritionist`, HR/HRV/BP pathology to `cardiovascular-specialist`, and training-load prescription to `personal-trainer`, never duplicating them.

Mode: standard (risk_class `protocol-low`). 4 paired retrieval+judge dispatches; 2 sections (A, D) HALTed at iter-1 on real citation-fidelity defects and converged clean at iter-2; integrity gate PASS (6/6 spot-verifications matched, concentration share 6.5%, attestation chain intact).

## §0 Introduction

This deliverable is the Pass-3 substrate for the `recovery-specialist` design doc. It synthesizes four independently-retrieved, independently-judged research sections:

- **Section A** — recovery metrics & autonomic interpretation (17 sources)
- **Section B** — overtraining/overreaching & load management (12 sources)
- **Section C** — recovery modalities, evidence-graded (13 sources)
- **Section D** — safety architecture, red-flags & boundary discipline (9 sources)

It is **goal-agnostic** library/domain research (PF-S2-04): the operator-profile / current-state / goals files were loaded as Phase-1 context for linkage but were NOT injected into the research question, and no operator personalization appears here. Personalization happens at the agent's runtime, against this substrate. Findings (§1) map to design-doc §3.1; recommendations (§2) map to design-doc §3.2; gate dispositions (§3) and the concentration audit (§4) document the standard-mode gate trail; §5 is the provenance pointer for the integrator.

## §1 Findings

### Finding 1 — HRV is a vagal index only; "sympathovagal balance" (LF/HF) is unvalidated
rMSSD/lnRMSSD (and HF power) index cardiac *vagal* modulation; HRV does NOT directly measure sympathetic activity, and the LF/HF "sympathovagal balance" reading has unclear physiological basis and low predictive value [A: 1, mechanism_review]. The agent interprets only the vagal index and attaches no meaning to any "sympathetic" number a consumer device reports.

### Finding 2 — Trend-over-absolute against an individual baseline + CV is the only defensible interpretive unit
A single day's HRV is nearly uninterpretable: between-day reliability of linear HRV metrics is only moderate-to-good (ICC ~0.56–0.88), lnRMSSD between-day CV is tight (~4.4–5.1%) but raw rMSSD wobbles ~17%, and ratio indices are far less reliable still [A: 11, cohort; 17, cohort]. The defensible unit is a rolling baseline (e.g., 7-day lnRMSSD) plus its CV; the canonical maladaptation signal is a *falling rolling HRV together with a collapsing CV* (Plews two-triathlete case) [A: 8, open_label]. The agent requires ≥1–2 weeks of personal baseline before any reading is actionable and weights trend + CV over absolute value.

### Finding 3 — Wearable HRV/RHR is trend-grade, not clinical-grade
Against ECG, Oura nocturnal HR (r≈0.99) and time-domain rMSSD (r 0.94–0.98) are trend-accurate, but frequency-domain HRV is not (LF r≈0.42, LF/HF r≈0.36); WHOOP 4-stage sleep agreement is only 64%; a Polar H10 chest strap (RR r≈0.95) is the closest practical ECG proxy [A: 10, cohort; 12, cohort; 13, cohort; 15, cohort]. PPG wearables measure pulse-rate variability, not true RR intervals. The agent uses wearable RHR/rMSSD for trend, never for diagnosis, and never over-reads frequency-domain or stage-level numbers.

### Finding 4 — Readiness/recovery scores are unvalidated proprietary black boxes
No wearable manufacturer discloses its readiness/recovery scoring formula, few provide peer-reviewed validation, and none demonstrates the score predicts hard outcomes (injury, illness, performance); same-night cross-brand scores can diverge 20+ points [A: 9, mechanism_review]. The agent treats a readiness score as a coarse *within-device* trend, never a cross-brand truth and never a clinical signal, and explains the proprietary-algorithm caveat to the user.

### Finding 5 — Confound-first triage precedes any overtraining inference
Day-to-day HRV/RHR is dominated by confounds unrelated to training adaptation: alcohol (dose-dependent nocturnal rMSSD suppression; HRV-recovery fell ~9/24/39 percentage units at low/moderate/high intake) [A: 2, rct; 3, cohort], acute illness/infection (RHR up, HRV down pre-symptom) [A: 4, cohort], body position, time-of-day, breathing, age, acute load, and menstrual-cycle phase [A: 5, cohort; 6, mechanism_review; 7, cohort]. Before flagging "overtraining," the agent checks alcohol, illness, short/poor sleep, posture, and (if applicable) cycle phase.

### Finding 6 — OTS has no validated biomarker; it is a diagnosis of exclusion the agent must NOT make
The ECSS/ACSM joint consensus is unambiguous that *no* marker (creatine kinase, cortisol, the testosterone:cortisol ratio, etc.) meets the criteria for an OTS diagnostic test; recognition *requires* exclusion of organic disease, infection, and nutritional deficiency [B: 1, regulatory; 2, mechanism_review]. FOR vs NFOR vs OTS is separated retrospectively by recovery time and performance rebound, not by any prospective test [B: 1, regulatory]. The agent flags load/recovery-imbalance patterns and routes suspected cases to the medical-liaison for organic-disease workup; it never issues a biomarker-based "you have OTS" call.

### Finding 7 — HRV cannot reliably detect overreaching
A systematic review/meta-analysis found resting HRV is *largely unaffected* by overreaching, and post-exercise HRV rises with *both* positive and negative adaptation — so an isolated HRV change cannot distinguish healthy adaptation from harmful overreaching [B: 4, meta_analysis]. NFOR/OTS do show autonomic dysregulation (sympathetic-dominant early, broad "autonomic dystonia" advanced) [B: 3, cohort], but only as a retrospective pattern. The agent uses HRV solely as a triangulated trend signal, never as an overreaching detector.

### Finding 8 — Subjective self-report tracks load better than objective measures
A 56-study systematic review found subjective self-report (wellness, mood, perceived recovery) reflects acute/chronic training load with *superior* sensitivity and consistency than objective measures, and that subjective and objective measures generally do not correlate [B: 10, meta_analysis]. Daily subjective questionnaires (wellness, sleep, soreness, mood/POMS-style, TQR [B: 8, practitioner_protocol; 9, mechanism_review]) are the evidence-supported *primary* monitoring layer; objective devices are adjuncts.

### Finding 9 — ACWR is methodologically contested; sRPE is valid but confound-modulated
The acute:chronic workload ratio is disputed on mathematical-coupling/spurious-correlation grounds, and a strong conceptual critique concludes "there is no evidence supporting the use of ACWR" for load management or injury-risk reduction [B: 6, cohort; 7, mechanism_review]. Session-RPE is a valid internal-load metric but is modulated by personality, fitness, environment, caffeine, and glycemia; monotony + high load tracks overtraining onset [B: 5, mechanism_review]. The agent may display ACWR at most as a descriptive trend and must never present the "0.8–1.3 sweet spot" as a validated injury threshold.

### Finding 10 — Taper is evidence-supported; deload is convention; detraining is slow for strength
A ~2-week, 41–60% volume-reduction taper with maintained intensity improves performance [B: 11, meta_analysis]; routine within-block deloads are reasonable convention, not RCT-validated dose-response [B: practitioner_protocol]. Detraining is intensity-sensitive: short layoffs (≤~2–4 weeks) are physiologically low-cost for trained individuals, especially for strength, and loss is limited by maintaining intensity while cutting volume/frequency [B: 12, mechanism_review]. The agent reassures (rather than alarms) on brief breaks and prescribes intensity-preserving maintenance.

### Finding 11 — The CWI interference effect is the headline goal-conditional trade-off
Post-resistance-training cold-water immersion reliably blunts hypertrophy (type II fibre CSA and myonuclei gains attenuated; anabolic signalling reduced) [C: 1, rct; 4, rct; 2, meta_analysis] and attenuates strength gains (SMD ≈ −0.23) [C: 3, meta_analysis], while reliably reducing DOMS and improving perceived recovery short-term [C: 5, meta_analysis]. These point in opposite directions: CWI "helps soreness today, hurts adaptation over weeks." The agent surfaces this trade-off whenever a strength/hypertrophy goal is in play, while noting CWI remains defensible for endurance contexts and acute perform-again-soon situations — it is NOT "cold is always bad."

### Finding 12 — Recovery modalities are evidence-graded; most are perceptual; sauna CV-data is not a recovery claim
The Laukkanen sauna mortality association (SCD HR 0.37) is observational, single-cohort, healthy-user-biased, and *cardiovascular* — never a muscle-recovery claim [C: 6, cohort]; sauna's training relevance is heat-acclimation/plasma-volume expansion for endurance, provisional [C: 7, rct]. Compression has the most consistent (still modest, g ≈ 0.40–0.49) effects [C: 9, meta_analysis]; massage > foam rolling ("minor and partly negligible") > percussion, all largely perceptual with near-zero force-recovery effect [C: 13, meta_analysis; 10, meta_analysis; 12-PT, mechanism_review]; active recovery clears lactate but lactate clearance ≠ performance recovery [C: 12-AR, mechanism_review]; contrast therapy beats passive rest but not the simpler options [C: 8, meta_analysis]; photobiomodulation is provisional with a single-research-group concentration flag (Leal-Junior cluster) [C: 11-PBM, meta_analysis]. Vendor device claims ground no effect size [C: 12, vendor_label].

### Finding 13 — Sleep and nutrition outrank every modality and are owned by other agents
Sleep behavior/extension/circadian timing (sleep-coach) and protein/energy-availability/fueling (nutritionist) dwarf every modality in effect size and are deliberately out of scope to avoid duplication [C: boundary]. The agent orders advice foundations-first ("fix sleep and fueling before optimizing modalities") and defers sleep/fueling *content* to the owning agents while still recognizing and routing their red-flags.

### Finding 14 — Safety architecture: red-flags map to escalation tiers; modality contraindications are cardiovascular; a wearable number is never a diagnosis
A tight red-flag set maps to tiers: persistent unexplained fatigue/performance decline → URGENT-REFERRAL (OTS is exclusion-diagnosis; differential includes anemia/thyroid/infection/depression/RED-S/cardiac) [D: 5, regulatory]; sustained RHR trend +5–10 bpm → ROUTINE-MONITOR, resting HR >100 bpm → URGENT-REFERRAL, + chest pain/syncope/dyspnea → EMERGENCY [D: 6, mechanism_review]; fever/systemic illness + training → stop + URGENT-REFERRAL, and chest pain/syncope/SOB/palpitations during-or-after illness → EMERGENCY (myocarditis; cardiology owns return-to-play, 3–6 mo abstention) [D: 1, mechanism_review; 2, mechanism_review]; RED-S → URGENT-REFERRAL (nutritionist + medical-liaison) [D: 3, regulatory; 4, mechanism_review]. Sauna and cold-immersion carry real cardiovascular contraindications (uncontrolled hypertension, cardiac disease/arrhythmia incl. long QT/Brugada/HCM, recent cardiac event, severe aortic stenosis/decompensated HF for heat, pregnancy; cold-shock + "autonomic conflict" can be fatal in vulnerable hearts) → URGENT-REFERRAL, collapse during exposure → EMERGENCY [D: 7, mechanism_review; 8, mechanism_review]. The hard rule: **never convert a wearable number into a medical conclusion** [D: 9, mechanism_review]; boundaries route to sleep-coach / nutritionist / cardiovascular-specialist / personal-trainer / medical-liaison / MD; the agent recognizes and routes, it never diagnoses or duplicates.

## §2 Recommendations (→ design-doc §3.2 directive list)

| # | Recommendation | Verdict |
|---|---|---|
| R1 | Identity = non-diagnostic training-recovery monitor + autonomic-data interpreter with a hard safety floor; anti-sycophancy + hype-resistance anchor. | ACCEPTED |
| R2 | Core rule: interpret HRV/RHR/readiness against the user's own rolling baseline + CV (≥1–2 wk baseline), never a single absolute value, never a "sympathetic" or cross-brand score (Findings 1–4). | ACCEPTED |
| R3 | Core rule: confound-first triage (alcohol, illness, sleep, posture, cycle phase) before any overtraining inference (Finding 5). | ACCEPTED |
| R4 | Core rule: NEVER diagnose OTS — flag load/recovery-imbalance patterns and route to medical-liaison for organic-disease exclusion (Finding 6). | ACCEPTED |
| R5 | Core rule: subjective daily monitoring is the primary layer; wearables are adjunct trend signals; HRV is not an overreaching detector (Findings 7–8). | ACCEPTED |
| R6 | Core rule: present ACWR (if at all) as a descriptive trend only, never a validated injury threshold; sRPE noted as confound-modulated (Finding 9). | ACCEPTED |
| R7 | Core rule: grade every modality honestly (established/provisional/equivocal); always surface the CWI interference trade-off when a strength/hypertrophy goal is in play (Findings 11–12). | ACCEPTED |
| R8 | Core rule: foundations-first ordering — defer sleep behavior to sleep-coach and fueling/RED-S nutrition to nutritionist; never duplicate (Finding 13). | ACCEPTED |
| R9 | Refusal/escalation: encode the red-flag → tier map (URGENT-REFERRAL / EMERGENCY) with TIME_CRITICAL floor for chest-pain/syncope/palpitations + fever-and-train myocarditis rule (Finding 14). | ACCEPTED |
| R10 | Refusal: ≥4 refusal classes incl. mandatory AUTHORITY_FRAMING_BYPASS + TIME_CRITICAL; PATIENT_FACING_DIRECTIVE / BASIS_NOT_REVIEWABLE for diagnosis/treatment requests; wearable-is-not-diagnosis hard rule (Finding 14). | ACCEPTED |
| R11 | Modality safety: encode sauna + cold-immersion cardiovascular contraindications → URGENT-REFERRAL, collapse-during → EMERGENCY (Finding 14). | ACCEPTED |
| R12 | Boundary table: sleep-coach / nutritionist / cardiovascular-specialist / personal-trainer / medical-liaison / MD ownership; at boundary, name candidate owners + escalate to medical-liaison (Findings 13–14). | ACCEPTED |
| R13 | Tools: aplus-research floor `--mode=standard --target-class=protocol`; consume the wiki goal-agnostically; no diagnosis, no training-plan authoring, no fueling prescription. | ACCEPTED |
| R14 | Reassure-don't-alarm on short layoffs; prescribe intensity-preserving maintenance; taper is evidence-based, deload is convention (Finding 10). | ACCEPTED |
| R15 | Escalation routes to the LIVE medical-liaison (`BLOCK_WITH_OVERRIDE_PATH`); inherit project safety architecture verbatim, never redefine it. | ACCEPTED |

## §3 Standard-mode gate dispositions

- **Phase 2.75 SCOPE GATE:** PASS — 4 context files loaded + sha256-recorded; target `{class: other, slug: recovery-specialist, type: reference}`; output → `design/.recovery-specialist-design-work/domain-research.md`; update_mode false. (`gates/gate-2.75.json`, schema-valid.)
- **Phase 3.5 JUDGE GATE:** PASS — 4 paired retrieval+judge dispatches; A & D HALTed at iter-1 on real citation-fidelity defects, converged clean at iter-2 (A 96, B 96, C 96, D 95). Authoritative artifacts: `judges/judge-{A,B,C,D}.json` (+ iter-1 HALT copies). (`gates/gate-3.5-summary.md`.)
- **Phase 4.25 ID-RECONCILE:** folded into Phase-4.75 IC-10 (gi precedent) — Meeusen 2013 shared B[1]/D[5] with concordant identifiers; Plews 2012/2013 and Laukkanen 2015/2018 are distinct works, not collisions.
- **Phase 4.75 INTEGRITY GATE:** PASS — 12 IC checks PASS, IC-13 SKIP-mode (standard), 0 HALT, 3 non-blocking warnings; population-mismatch N/A (no animal/in_vitro primaries); 6/6 independent spot-verifications matched. `gate_attest.py`-attested; `verify-chain --up-to 4.75` intact. (`gates/gate-4.75.json` + `gates/gate-4.75.md`.)
- **Phase 7.5 RISK-FLOOR + Phase 8.5 LAYERS:** N/A — compound-only gates; this is `target_type=reference`/`protocol` research (no risk_tier=experimental compound, no mandatory prescribing/non-English layers).

## §4 Concentration audit (corpus-level)

31 distinct primary citations across the 4 sections. Largest single-group cluster = Buchheit/Laursen HRV group (Plews 2012 + Al Haddad 2011), count 2, **share 0.065 (6.5%)** — far below the 0.70 first-class-surfacing threshold. Two sub-topic concentrations are surfaced first-class in-body per IC-9: the **Leal-Junior cluster** dominates favourable photobiomodulation evidence (flagged, graded provisional), and the **Laukkanen single-cohort** is the source of the sauna-mortality association (flagged as observational/healthy-user-biased and walled off from recovery claims). No buried-only dominant cluster. Concentration risk: LOW.

## §5 Provenance & gate trail (for the integrator)

```
design/.recovery-specialist-design-work/
├── plan.md                     # Phase 2 PLAN (4-section decomposition, search angles)
├── rubric.md                   # Phase 2.5 RUBRIC (9 dimensions, standard threshold 92)
├── dispatch-ledger.jsonl       # 6 retrieve + 6 judge dispatch records (incl. iter-2 remediations)
├── gates/
│   ├── gate-2.75.json          # SCOPE gate (mechanical; schema-valid)
│   ├── gate-3.5-summary.md     # JUDGE gate summary (judges are authoritative artifact)
│   ├── gate-4.75.json          # INTEGRITY gate (gate_attest.py-attested; attestation_chain)
│   ├── gate-4.75.md            # integrity verifier agent source (sha256 in chain)
│   └── _iter-state.json        # gate_attest iteration state
├── judges/
│   ├── judge-{A,B,C,D}.json    # final per-section judge verdicts (all PASS, findings:[])
│   └── judge-{A,D}-iter1.json  # preserved iter-1 HALT verdicts (provenance trail)
└── sections/
    └── section-{A,B,C,D}.md    # dispatched retrieval outputs (inline [N,tag] + bibliography + self-check)
```

- `gate_attest.py verify-chain --up-to 4.75` → **attestation chain intact** (exit 0).
- Canonical provenance layout: bare `gates/` / `judges/` / `sections/` (NO `research-` prefix) per BOARD bead 0be — bda-ready.
- No vault writes (PF-S2-04 goal-agnostic library research). No orchestrator self-attestation (PF-S3-01): every gate verdict is dispatched-agent-produced; the judge gate caught 4 real defects and iterated to convergence with fresh verifiers.
