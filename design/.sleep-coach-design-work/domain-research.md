# sleep-coach — Pass-3 Phase-0 Domain Research (synthesis digest)

**Role slug:** `sleep-coach`  ·  **Role class:** specialist  ·  **Risk class:** `protocol-low` (mode floor `standard`, target-class `protocol`, per `templates/specialist-risk-class.yaml`)
**Pipeline:** aplus-research standard-mode discipline run at orchestrator level (CONTINUATION_BRIEF Lesson 1: parallel-dispatch phases run where Agent-tool access lives). Output routed to `design/.sleep-coach-design-work/` — NOT the wiki (PF-S2-04: the specialist consumes the wiki, it does not author it; this is agent-design research, not a wiki-bound protocol entry).
**Corpus:** four paired (retrieval + independent judge) section dispatches. Judge gate (Phase 3.5) PASS at standard threshold 92/100: Section A 94, Section B 96 (iter-2 after a citation-fidelity HALT remediation), Section C 94, Section D 94. Per-section files + bibliographies live alongside this digest at `sections/section-{A,B,C,D}.md`; per-section judge verdicts at `judges/judge-{A,B,C,D}.json`. ~10,200 words, 67 distinct sources, every claim type-tagged per `vault/library/_source-whitelist.md`.

This digest lifts the load-bearing structural conclusions into `### Finding` headings + `R1–R15` recommendations so the design doc §3 can anchor against them without paraphrase drift. Citations resolve to the named section's bibliography (e.g. "A[9]" = Section A reference [9]).

---

## Findings

### Finding 1 — sleep-coach is an inform-class interpreter, not a diagnostician or prescriber

The domain divides cleanly into a coachable layer (behavioral/circadian sleep optimization, risk_tier low) and a clinical layer (disorder diagnosis, prescription management). Section C establishes that the clinical layer carries hard statutory and safety boundaries the agent must not cross: OSA diagnosis requires PSG/HSAT [C1, regulatory]; prescription hypnotics require a licensed prescriber [C5, regulatory]; "diagnose me / prescribe for me" is a patient-facing directive even when framed educationally [C5]. The agent's posture must mirror the deployed `labs-specialist` (inform-class, basis-reviewable, escalation-over-interpretation) rather than any directive posture.
**Informs:** AGENT_TEMPLATE Identity, Role Boundaries, Anti-Patterns.

### Finding 2 — the established-vs-provisional evidence boundary is the agent's central epistemic discipline

Sleep science is a field where popular messaging routinely states as *proven* what the literature holds as *mechanistic/associational*. Section A documents the sharpest case: the glymphatic "deep sleep detoxes the brain / prevents Alzheimer's" narrative rests on a single-species mouse study (Xie 2013, A[4], animal) whose very *direction of effect* is now in active 2024–2025 dispute (A[5], mechanism_review). Memory-consolidation is well-supported in direction but specific stage→memory-type mappings are provisional (A[3]). The agent must preserve the established/provisional boundary in every user-facing statement.
**Informs:** Core Rules, Anti-Patterns, Negative Examples.

### Finding 3 — timing, not dose or amount, is the active ingredient in circadian intervention

The two-process model (Process S homeostatic × Process C circadian; A[2], mechanism_review) and the light phase-response curve (A[6]) establish that the *same* stimulus advances or delays the clock depending on biological time: morning light advances, evening light delays, with a mid-day dead zone. DLMO is the most accurate human circadian-phase marker (A[6]). Chronobiotic melatonin works at low physiological doses (0.5–1 mg) timed to circadian phase, distinct from 3–10 mg hypnotic megadoses; mistimed melatonin shifts the clock the *wrong* way (D3, D[5] Cochrane meta_analysis).
**Informs:** Core Rules, Modes, Communication.

### Finding 4 — sleep need is a population floor (≥7 h), not a personal "8 hours"; norms are wide and age/sex-dependent

The AASM/SRS consensus recommends ≥7 h for most adults as a population floor with no fixed upper target and no universal single number (A[8], regulatory). Ohayon 2004 (A[10], meta_analysis, 65 studies, n=3,577) is the canonical lifespan-norms source: TST, sleep efficiency, %SWS, %REM, and REM latency all decline with age while latency, WASO, and %N1/N2 rise — SWS shows the steepest decline (≈50% reduction in older vs younger men), far less marked in women. A 70-year-old with little N3 is age-typical, not "broken."
**Informs:** Core Rules, Anti-Patterns (the "everyone needs 8 h" anti-pattern), Edge Cases.

### Finding 5 — sleep debt accumulates dose-dependently, single-night recovery is incomplete, and self-report is unreliable

Van Dongen 2003 (A[9], rct) showed chronic restriction to 4 h/6 h produces cumulative dose-dependent cognitive deficits, that a single recovery night does NOT return subjects to baseline, and — load-bearing for an agent receiving self-report — that restricted subjects were *largely unaware* of their mounting impairment. The agent must not accept "I feel fine on 6 hours" as evidence of adequacy.
**Informs:** Core Rules, Negative Examples.

### Finding 6 — consumer wearable data is validated for epoch sleep/wake + RHR but POORLY validated for auto-staging and proprietary "readiness" scores

Section B establishes the validity gradient with concrete numbers: high sleep-detection sensitivity (≥0.93) but poor wake specificity (0.18–0.54) → devices overestimate sleep [B, multiple]; auto-staging agreement is moderate at best (Oura Gen3 OSSA 2.0 4-stage κ≈0.65, vendor-reported and contested — B[4] Svensson 2024 + peer comment B[4b]); proprietary readiness/recovery composites are unvalidated clinical constructs. Wrist/finger PPG HRV diverges from ECG RMSSD under motion/arrhythmia/low-HR. The agent must tier wearable-derived claims by what is actually validated and must never treat a readiness score as a clinical measure.
**Informs:** Core Rules, Tools, Modes, Communication.

### Finding 7 — single-night wearable metrics are noise; trend + intra-individual baseline is mandatory

Night-to-night variability means a single night's HRV/sleep-efficiency number is noise; interpretation requires rolling averages and intra-individual baselining over population norms (Section B). This is the direct sleep analog of the labs-specialist RCV-gate (trend only against the operator's own comparator, not a population range).
**Informs:** Core Rules, Loop-Breaking, Modes.

### Finding 8 — over-interpreting consumer sleep data is itself a documented harm (orthosomnia)

Baron 2017 (B, cohort/case) documents "orthosomnia" — wearable data worsening sleep and anxiety. This is a design constraint on the agent's communication layer: surfacing alarming single-night numbers, or treating an unvalidated score as a verdict, can cause the harm the agent is meant to prevent.
**Informs:** Anti-Patterns, Communication, Negative Examples.

### Finding 9 — wearable data is ABSENT today (Oura purchase pending, LM-02); the empty-wearable-state is the dominant boundary case

Per `vault/meta/current-state.md` the Wearable section is empty and `operator-profile.md` is a scaffold. The agent will eventually consume HRV/RHR/sleep-efficiency/body-temp/readiness, but none exists at deploy time. The agent must operate correctly with NO wearable data (behavioral/circadian coaching from operator self-report and established science) and must be designed so that the *interpretation discipline* of Finding 6/7 binds the moment data appears — without fabricating data in the interim (mirrors labs-specialist empty-state Mode).
**Informs:** Modes (empty-state), Edge Cases, Context Loading.

### Finding 10 — OSA is the dominant missed-diagnosis hazard: screen-and-route, never diagnose; wearable "AHI" is not diagnostic

OSA affects ~936M adults (AHI≥5) / 425M (AHI≥15) worldwide, mostly undiagnosed, and is independently linked to hypertension, stroke, CAD, MVA, and mortality (C[1] regulatory; C[6] meta_analysis). STOP-Bang (≥5 high / 3–4 intermediate / <3 low) and Epworth (≥11) are screening, not diagnostic instruments — they rule out, not in (C[4], C[6]). A consumer wearable / AI agent CANNOT diagnose OSA or relay a wearable "AHI" as diagnostic and must not recommend/titrate CPAP — this is the DEVICE_FUNCTION boundary. A positive screen → ROUTINE clinician referral (URGENT with cardiac/driving comorbidity).
**Informs:** Role Boundaries (DEVICE_FUNCTION), Loop-Breaking (escalation floor), Negative Examples.

### Finding 11 — insomnia↔depression↔suicidality is a TIME_CRITICAL escalation, not a coaching topic

Insomnia roughly doubles subsequent-depression risk (C[8], meta_analysis, RR 2.27) and independently predicts suicidal ideation (OR ~2.10) and behavior (OR ~2.29) (C[5], C[9], meta_analysis). When a sleep complaint co-presents with depressed mood/hopelessness/suicidal ideation the agent STOPS coaching and escalates: active SI/plan/intent → EMERGENCY (988/ED); depressive symptoms without acute SI → URGENT in-person; chronic insomnia without mood flag → ROUTINE referral + CBT-I.
**Informs:** Role Boundaries (TIME_CRITICAL), Loop-Breaking (fail-safe escalation), Negative Examples.

### Finding 12 — a cluster of red-flag conditions are recognize-and-route, never manage

REM behavior disorder (≈74% phenoconversion to synucleinopathy within 12 yr — C[10] cohort, C[12]; URGENT), narcolepsy/pathological EDS (URGENT if driving/work safety; MSLT required), RLS/PLMD (ROUTINE, may be iron/medication-secondary), parasomnias (ROUTINE; URGENT if injurious/new-onset adult), and severe circadian rhythm sleep-wake disorders (ICSD-3 category C[7]; mild misalignment coachable, severe → referral). Disclosure of neurodegenerative prognosis is a clinician's role, never the agent's.
**Informs:** Role Boundaries, Edge Cases, Loop-Breaking.

### Finding 13 — drowsy-driving microsleep is an acute, non-volitional safety directive

Sleep deprivation produces involuntary microsleeps the person cannot suppress; drowsiness contributes to ~21% of fatal crashes (C[13], regulatory); <5 h before driving raises crash risk ~4–5× (C[15], C[16], cohort). On reports of microsleeps/nodding/near-misses while driving or intent to drive after severe sleep loss, the agent issues an acute "do not drive until rested" advisory + URGENT referral for recurrent EDS. This is the one place the agent issues a directive — a safety stop, not a clinical instruction.
**Informs:** Core Rules, Edge Cases, Communication.

### Finding 14 — prescription hypnotics and risk_tier medium+ compounds route OUT; CBT-I is first-line and the canonical GRADE two-axis HALT case; weak interventions must not be over-sold

CBT-I is the AASM/ACP first-line treatment for chronic insomnia — a STRONG recommendation resting on LOW-to-MODERATE certainty (D[1] regulatory + meta_analysis; D[2] Trauer meta_analysis SOL −19 min, SE +9.9%) — the canonical strong-rec-on-low-certainty GRADE HALT pairing: the agent privileges CBT-I (strength governs action) but surfaces the certainty gap rather than laundering it into false confidence. Sleep hygiene is adjunct-not-treatment (AASM recommends *against* it standalone — D[1]). Sleep-relevant compounds are mostly weak/very-low certainty (melatonin hypnotic effect ~7 min latency, D[13]; magnesium/valerian/L-theanine/glycine/apigenin low-to-very-low) and OTC melatonin has documented label-integrity failures (−83% to +478% of label — D[14] regulatory; D[15] JAMA). Prescription hypnotics (Z-drugs with FDA boxed warning D[18], benzodiazepines, DORAs, sedating antidepressants) are PRESCRIPTIVE_DIRECTIVE → prescriber; any compound at risk_tier medium+ routes OUT to supplement/endocrine/peptide specialists. Ungrounded efficacy/dose claims are BASIS_NOT_REVIEWABLE.
**Informs:** Core Rules (GRADE two-axis + HALT), Role Boundaries (cross-role routing, PRESCRIPTIVE_DIRECTIVE, BASIS_NOT_REVIEWABLE), Communication.

---

## Recommendations

| # | Recommendation | Verdict | Grounding |
|---|---|---|---|
| R1 | Adopt an inform-class, basis-reviewable, escalation-over-interpretation posture mirroring `labs-specialist`; never diagnose, dose, or prescribe. | ACCEPTED | F1 |
| R2 | Encode the established-vs-provisional boundary as a Core Rule; never state mechanism (glymphatic, stage→memory mappings) as proven; tag certainty. | ACCEPTED | F2 |
| R3 | Treat circadian-intervention TIMING (relative to the operator's phase) as the active ingredient; distinguish chronobiotic (0.5–1 mg timed) from hypnotic melatonin dosing. | ACCEPTED | F3 |
| R4 | Anchor guidance to "≥7 h for most adults" as a population floor; never assert "8 hours" as a personal requirement; apply age/sex-adjusted norms, never young-adult norms to older adults. | ACCEPTED | F4 |
| R5 | Treat self-reported sleep adequacy ("fine on 6 h") as unreliable; cumulative debt is real and single-night recovery is incomplete. | ACCEPTED | F5 |
| R6 | Tier every wearable-derived claim by validation status: epoch sleep/wake + RHR are usable; auto-staging is low-confidence; proprietary readiness/recovery scores are NOT clinical measures. Declare this in Tools + Communication. | ACCEPTED | F6 |
| R7 | Interpret wearable metrics only as trends against the operator's own rolling baseline (sleep analog of the RCV-gate); a single night is noise. | ACCEPTED | F7 |
| R8 | Build the communication layer to avoid orthosomnia: do not surface alarming single-night numbers or treat a score as a verdict. | ACCEPTED | F8 |
| R9 | Make the empty-wearable-state the dominant Mode; operate from established science + operator self-report when no device data exists; never fabricate data; bind the F6/F7 discipline the moment data appears. | ACCEPTED | F9 |
| R10 | Encode a DEVICE_FUNCTION refusal for OSA/diagnostic determination and continuous-monitoring requests; surface STOP-Bang/Epworth as screen-and-route, never as diagnosis; refuse wearable-"AHI"-as-diagnosis. | ACCEPTED | F10 |
| R11 | Encode a TIME_CRITICAL escalation for sleep-complaint + mood/suicidality co-presentation with the EMERGENCY/URGENT/ROUTINE urgency bands; fail-safe toward escalation. | ACCEPTED | F11 |
| R12 | Encode a recognize-and-route boundary for RBD/narcolepsy/RLS/parasomnia/severe-circadian disorders; never disclose neurodegenerative prognosis. | ACCEPTED | F12 |
| R13 | Issue an acute "do not drive" safety advisory + URGENT referral on microsleep/drowsy-driving reports — the single sanctioned directive (a safety stop, not a clinical instruction). | ACCEPTED | F13 |
| R14 | Privilege CBT-I as first-line; instantiate the GRADE two-axis discipline with CBT-I as the strong-rec-on-low/moderate-certainty HALT case; do not over-sell sleep hygiene or weak supplements; route prescription hypnotics (PRESCRIPTIVE_DIRECTIVE) + risk_tier medium+ compounds OUT to compound specialists/prescriber; ungrounded claims → BASIS_NOT_REVIEWABLE. | ACCEPTED | F14 |
| R15 | Mandate AUTHORITY_FRAMING_BYPASS: educational/credential/hypothetical framing never relaxes any directive gate (operator is A3); inherit the three-mechanism anti-sycophancy scaffold from Role 1 verbatim. | ACCEPTED | F1, F11, F14; refusal-class-taxonomy.yaml (mandatory_for_every_specialist) |

**Recommendation-count rationale:** N=15, matching the foundation-deliverable convention. All ACCEPTED — no DEFERRED/REJECTED (this digest is design substrate; deferrals surface at design-doc §3.2/§18, not here).

---

## Self-check (synthesis level)

- **No orchestrator self-attestation (PF-S2-01/PF-S3-01).** Every Phase-3.5 judge verdict is a dispatched independent judge agent (judges/judge-{A,B,C,D}.json); Section B's iter-1 HALT was remediated by the retrieval agent and re-judged by a *fresh* independent judge (iter-2 PASS 96), never self-cleared.
- **Goal-agnostic (PF-S2-04).** Findings ground AGENT DESIGN (how the specialist reasons), not operator personalization; no operator-specific state is baked in. Operator-profile/current-state are scaffolds and were read as linkage context only.
- **Citation fidelity.** The one fidelity defect surfaced (Section B [4] placeholder DOI on the load-bearing Oura validation) was caught by the judge gate and resolved to a real resolving citation (Svensson 2024, PMID 38382312) with the vendor-reported numbers flagged; residual unconfirmed author initials ([5],[6]) are honestly marked, not fabricated.
- **Type-tag discipline.** Every claim in every section carries exactly one whitelist type-tag; vendor/anecdote tags ground no numerical claim.
- **Population/concentration handling.** Animal evidence (Xie 2013) is explicitly flagged single-species and contested; no single-lab dominance present in this protocol-domain corpus (orthogonal to the compound-class concentration audit).
- **Residual caveats forwarded to design-doc §18.** Section self-checks flag author-string and threshold-variation items (STOP-Bang cut-points, suicidality escalation threshold as a safety-conservative product decision to be reviewed against the medical-liaison adjudication layer) for verification before any wiki ingestion downstream.
