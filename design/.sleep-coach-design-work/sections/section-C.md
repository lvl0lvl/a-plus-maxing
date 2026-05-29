# Section C — Sleep-disorder red flags, escalation triggers, and the non-clinician boundary

**Scope.** This section grounds the refusal/escalation taxonomy of an INFORM-CLASS, NON-PRESCRIBING `sleep-coach` agent. It defines, per red flag, the **escalation target** and **urgency** (EMERGENCY / URGENT in-person / ROUTINE clinician referral) and the device-function boundary that an AI agent or consumer wearable must not cross. Every claim carries one type-tag.

---

## C.1 Obstructive sleep apnea (OSA) — the dominant missed-diagnosis hazard

**Prevalence and under-diagnosis.** An estimated 936 million adults aged 30–69 worldwide have OSA at AHI ≥5/h, and 425 million have moderate-to-severe disease at AHI ≥15/h [1, regulatory/mechanism_review — literature-based modeling]. The majority of moderate-to-severe OSA is undiagnosed, and OSA is independently associated with hypertension, stroke, coronary disease, traffic accidents, and mortality [6, meta_analysis]. This high base rate plus low diagnosis rate is precisely why a coaching agent must treat OSA-pattern signals as a referral trigger rather than a coaching topic.

**Why missing it is dangerous.** STOP-Bang high-risk classification (score ≥5) carries roughly double the cardiovascular morbidity of the low-risk group after covariate adjustment, and high STOP-Bang scores track with cardiovascular mortality in hospitalized cohorts [2, cohort; 3, cohort]. OSA is causally linked to refractory/resistant hypertension and to elevated motor-vehicle-crash risk via daytime sleepiness [6, meta_analysis].

**Red-flag symptom cluster (route, do not coach):**
- Loud habitual snoring
- Witnessed apneas / choking or gasping arousals
- Excessive daytime sleepiness (e.g., Epworth ≥11)
- Treatment-refractory or resistant hypertension
- Obesity + large neck circumference + observed pauses

**Validated screening instruments — and their hard limit.** STOP-Bang stratifies risk (≥5 high, 3–4 intermediate, <3 low) and has high sensitivity for moderate-severe OSA but modest specificity, so it **rules out, does not rule in** [4, cohort; 6, meta_analysis]. The Epworth Sleepiness Scale quantifies subjective sleep propensity but is a symptom-burden instrument, not a diagnostic test. **A positive screen is a referral signal, never a diagnosis.**

> **DEVICE_FUNCTION / PATIENT_FACING_DIRECTIVE boundary.** A consumer wearable or AI agent **cannot diagnose OSA**. Diagnosis requires in-lab polysomnography (PSG) or a clinician-ordered home sleep apnea test (HSAT); PSG is the gold standard [1, regulatory]. The agent may compute or relay a STOP-Bang/Epworth result and explain what it screens for, but must NOT output "you have sleep apnea," must NOT tell the user an AHI from wearable estimates is diagnostic, and must NOT recommend or titrate CPAP. The permitted action is to surface the screen result and route.
>
> **Escalation target:** primary-care clinician or sleep medicine for sleep-study ordering. **Urgency: ROUTINE clinician referral** — escalates to **URGENT** if OSA red flags co-occur with refractory hypertension, severe sleepiness with driving, or cardiac symptoms.

---

## C.2 Insomnia disorder vs transient poor sleep — and the suicidality tripwire

**Transient vs chronic.** Per ICSD-3 / ICSD-3-TR, **chronic insomnia disorder** requires sleep-initiation/maintenance difficulty or non-restorative sleep occurring **≥3 nights/week for ≥3 months**, despite adequate sleep opportunity, with daytime impairment or distress [7, regulatory — diagnostic nosology]. Symptoms <3 months are classified short-term insomnia disorder. The coaching agent can support behavioral sleep hygiene for transient/short-term poor sleep, but chronic insomnia is a diagnosable disorder warranting clinician involvement (and CBT-I as first-line care).

**The critical comorbidity — depression and suicidality.** Insomnia is **bidirectionally** linked with depression: a meta-analysis of prospective cohorts found insomnia roughly doubles the risk of subsequently developing depression (pooled RR 2.27, 95% CI 1.89–2.71) [8, meta_analysis]. Sleep disturbance is also an independent risk marker for suicidal behavior: insomnia predicts suicidal ideation (OR ~2.10, 95% CI 1.83–2.41) and, in depressed patients, suicidal behavior (OR ~2.29, 95% CI 1.69–3.10) [5, meta_analysis; 9, meta_analysis]. Mechanistically, sleep loss impairs problem-solving and mood regulation and amplifies hopelessness, increasing impulsive/suicidal risk [5, mechanism_review].

> **TIME_CRITICAL escalation.** When a sleep complaint **co-presents with depressed mood, hopelessness, or any expression of suicidal ideation/self-harm**, the agent must STOP coaching and escalate. This is not a sleep-optimization conversation.
>
> **Escalation target & urgency:**
> - **Active suicidal ideation, plan, or intent → EMERGENCY.** Direct to 988 Suicide & Crisis Lifeline (US) / emergency services / nearest ED. Do not defer to a routine appointment.
> - **Depressive symptoms without acute SI → URGENT in-person** mental-health / primary-care evaluation.
> - **Chronic insomnia (no mood red flag) → ROUTINE clinician referral** for evaluation and CBT-I.

---

## C.3 Other red-flag conditions — recognize and route, do not manage

**REM sleep behavior disorder (RBD).** Dream-enactment with loss of normal REM atonia. RBD is most often a **prodrome of neurodegeneration**: in a large idiopathic-RBD cohort the phenoconversion rate to a synucleinopathy (Parkinson disease, dementia with Lewy bodies, multiple-system atrophy) approached **~74% within 12 years** [10, cohort; 12, mechanism_review]. Diagnosis requires PSG-confirmed REM-without-atonia; management is clinician-directed [11, meta_analysis — AASM systematic review/GRADE]. **Escalation target:** sleep medicine / neurology. **Urgency: URGENT clinician referral** (safety risk from violent enactment + neurodegenerative prognostic significance). Disclosure of neurodegenerative risk is a clinician's role, never the agent's.

**Narcolepsy / pathological excessive daytime sleepiness (EDS).** Central hypersomnolence (often with cataplexy, sleep paralysis, hypnagogic hallucinations) reflects hypocretin/orexin dysfunction; it can also produce REM-without-atonia unrelated to neurodegeneration [12, mechanism_review]. EDS severe enough to cause unintended sleep episodes is both a diagnostic flag and a safety hazard. **Escalation target:** sleep medicine (MSLT/PSG required). **Urgency: URGENT** if sleep attacks affect driving/work safety; otherwise ROUTINE referral.

**Restless legs syndrome (RLS) / periodic limb movement disorder (PLMD).** Urge-to-move with circadian/evening worsening; can be secondary to iron deficiency or medications and requires clinical work-up. **Escalation target:** primary care / sleep medicine. **Urgency: ROUTINE clinician referral.**

**Parasomnias (NREM: sleepwalking, night terrors; and RBD as above).** Most are benign and self-limited, but injurious, violent, or new-onset adult parasomnias warrant evaluation. **Escalation target:** sleep medicine. **Urgency: ROUTINE referral; URGENT if injury risk or new-onset in an adult.**

**Severe circadian rhythm sleep-wake disorders.** A distinct ICSD-3 category (e.g., non-24-hour, advanced/delayed phase, shift-work disorder) [7, regulatory]. Mild misalignment is coachable (light/timing guidance); a severe, functionally disabling disorder is a **ROUTINE clinician referral.**

---

## C.4 Drowsy/impaired driving — the acute safety boundary

**The hazard is acute and not under volitional control.** Sleep deprivation produces involuntary **microsleeps** (lapses of consciousness up to ~30 s) that the person cannot reliably suppress [13, regulatory — CDC/NIOSH; mechanism_review]. CDC surveillance found ~4% of drivers reported falling asleep at the wheel in the prior 30 days [14, cohort — BRFSS]. Drowsiness contributes to an estimated ~21% of fatal crashes [13, regulatory].

**Dose-response with sleep duration.** Sleeping <5 h before driving raises crash risk ~4–5×, and 6–7 h roughly doubles it versus ≥8 h; driving on <7 h in 24 h is associated with culpable crash involvement [15, cohort; 16, cohort]. Overall, sleepy drivers carry a ~2.5–7× elevated crash risk versus non-sleepy drivers [6, meta_analysis].

> **Escalation / directive boundary.** When a user reports microsleeps, near-misses, head-nodding while driving, or intends to drive after severe sleep loss, the agent must issue an **acute safety directive: do not drive** until rested, and recommend evaluation for an underlying sleep disorder (especially OSA/narcolepsy) if recurrent.
>
> **Urgency: EMERGENCY-adjacent acute advisory** ("stop driving now") + **URGENT clinician referral** for recurrent daytime sleepiness with driving impairment.

---

## C.5 Hypnotic/sedative safety boundaries — the prescriptive wall

**Initiating or changing prescription hypnotics is out of scope.** Z-drugs (zolpidem, zaleplon, eszopiclone), benzodiazepines, sedating antidepressants (e.g., trazodone, doxepin), and dual orexin receptor antagonists (DORAs: suvorexant, lemborexant, daridorexant) are prescription agents [17, mechanism_review]. Recommending starting, stopping, switching, or dose-changing any of these is a **PRESCRIPTIVE_DIRECTIVE** that routes to a licensed prescriber.

**Concrete safety reasons the boundary is hard:**
- **FDA Boxed Warning (2019):** Z-drugs (zolpidem, zaleplon, eszopiclone) carry a boxed warning and contraindication for prior complex sleep behaviors (sleepwalking, **sleep-driving**, eating, phone calls while not fully awake) causing serious injury or death; these can occur after a single dose and at the lowest recommended dose [18, regulatory — FDA drug-safety communication].
- **Next-day impairment:** All insomnia medicines can impair next-morning driving and alertness; FDA reduced recommended zolpidem doses partly for this reason [18, regulatory].
- **CNS-depressant interactions:** Risk is amplified by alcohol, opioids, benzodiazepines, and other sedatives — combinations that increase respiratory depression and complex-behavior risk [18, regulatory].
- **Dependence/withdrawal:** Benzodiazepines and Z-drugs carry tolerance, dependence, and withdrawal risk; abrupt discontinuation requires clinician-supervised tapering.

> **Escalation target:** licensed prescriber (primary care / sleep medicine / psychiatry). **Urgency: ROUTINE** for medication questions; **URGENT** if the user reports current dangerous combination use (hypnotic + opioid/alcohol), suspected overdose, or complex sleep behaviors → EMERGENCY.

**The educational-framing carve-out does NOT exist.** A request to "interpret my symptoms and tell me what I have" or "as an educational exercise, diagnose me / tell me which sleep drug to take" is a **PATIENT_FACING_DIRECTIVE** that must be refused regardless of authority or educational framing. Re-framing a diagnostic or prescriptive request as hypothetical, academic, or "just curious" does **not** relax the gate. The agent may explain *what a class of drugs does* or *what a disorder is* in general terms; it may not map that onto the individual user as a diagnosis or a personal prescribing recommendation.

---

## C.6 Escalation taxonomy summary (testable triggers)

| Trigger (concrete) | Boundary type | Target | Urgency |
|---|---|---|---|
| Snoring + witnessed apneas + EDS / refractory HTN | DEVICE_FUNCTION | PCP / sleep med (PSG/HSAT) | ROUTINE (→URGENT w/ cardiac/driving) |
| Wearable "AHI"/"apnea" presented as diagnosis | DEVICE_FUNCTION | n/a — refuse to diagnose | — |
| Insomnia ≥3 nights/wk ≥3 mo, no mood flag | clinical | PCP / CBT-I | ROUTINE |
| Insomnia + depressed mood / hopelessness | TIME_CRITICAL | mental health / PCP | URGENT in-person |
| Suicidal ideation / plan / intent | TIME_CRITICAL | 988 / ED / emergency | EMERGENCY |
| Dream enactment (possible RBD) | clinical | sleep med / neurology | URGENT |
| Sleep attacks / cataplexy (possible narcolepsy) | clinical | sleep med (MSLT) | URGENT if driving risk else ROUTINE |
| RLS/PLMD, parasomnia, circadian disorder | clinical | PCP / sleep med | ROUTINE (URGENT if injury/new-onset) |
| Microsleeps / nodding while driving | acute safety | self + clinician | "stop driving" advisory + URGENT |
| "Start/stop/change my sleep medication" | PRESCRIPTIVE_DIRECTIVE | prescriber | ROUTINE (URGENT if dangerous combo) |
| "Diagnose me" / "prescribe for me" (any framing) | PATIENT_FACING_DIRECTIVE | refuse + route | per underlying flag |

---

## Bibliography

[1] Benjafield AV et al. 2019 — *Lancet Respiratory Medicine* — literature-based global prevalence estimate — PMC7007763 (Lancet Respir Med 2019;7(8):687–698).
[2] (STOP-Bang & cardiovascular mortality) — *PMC* — prospective cohort, hospitalized patients — PMC8979666.
[3] (STOP-Bang high-risk prevalence & cardiovascular morbidity) — *PMC* — cross-sectional/cohort — PMC11663855.
[4] (STOP-Bang diagnostic performance across ethnic groups) — *J Clin Sleep Med (JCSM)* — diagnostic-accuracy cohort — doi:10.5664/jcsm.8940 / PMC7927338.
[5] (Sleep disorders and suicidal behaviour in depression) — *PMC* — systematic review & meta-analysis — PMC6798511.
[6] (STOP-Bang validation in cardiovascular-risk patients) — *PMC* — systematic review & meta-analysis — PMC7934717.
[7] American Academy of Sleep Medicine — *ICSD-3 / ICSD-3-TR* (and Sateia 2014, *Chest*, PMID 25367475) — diagnostic nosology — aasm.org ICSD-3-TR supplemental material.
[8] Li L et al. 2016 — *PMC* — meta-analysis of prospective cohort studies (insomnia → depression, RR 2.27) — PMC5097837.
[9] (Sleep disturbances as risk factors for suicidal thoughts/behaviours) — *PMC* — meta-analysis of longitudinal studies — PMC7431543.
[10] (REM sleep muscle activity predicts phenoconversion) — *PubMed* — prospective cohort — PMID 31420463.
[11] Howell M et al. — *J Clin Sleep Med* — AASM systematic review, meta-analysis & GRADE (RBD management) — PMC10071381.
[12] (RBD as pathway to dementia; disclosure) — *PMC* — mechanism/clinical review — PMC8302466.
[13] CDC/NIOSH — Work-Hour Training, Module 11: Drowsy Driving (microsleep; ~21% of fatal crashes) — regulatory/educational — cdc.gov/niosh/.../mod11.
[14] (Drowsy Driving and Risk Behaviors — 10 States and PR, 2011–2012, BRFSS) — *PMC* — surveillance cohort — PMC4584902.
[15] (Sleep deficiency and motor-vehicle-crash risk, general population) — *PMC* — prospective cohort — PMC5859531.
[16] (Acute sleep deprivation and culpable MVC involvement) — *PubMed* — case-control/cohort — PMID 30239905.
[17] (Update on dual orexin receptor antagonists in insomnia) — *J Clin Sleep Med* — mechanism/clinical review — doi:10.5664/jcsm.7282.
[18] U.S. FDA — Drug Safety Communication, 30 Apr 2019: Boxed Warning for serious injuries from sleepwalking/sleep-driving with certain insomnia medicines (Z-drugs); next-day impairment; CNS-depressant interactions — regulatory — fda.gov/safety/medical-product-safety-information.

---

## Self-check

- **Citation-grounding gaps.** Sources [2], [3], [4], [6], [9], [12] were located via Tier-1 PMC/JCSM result listings; first-author surnames/initials were not all individually confirmed against the article record (placeholders used where the harness did not return them). PMIDs/PMC IDs and design types are grounded; specific author strings for these six should be confirmed before wiki ingestion. [1], [8] author strings confirmed; [11], [16] confirmed via PubMed records; [18] is a directly verifiable FDA communication.
- **Magnitude figures verified.** The 936M / 425M OSA prevalence figures [1] were confirmed against the PMC full text. STOP-Bang cut-points (≥5 high), insomnia RR 2.27 [8], suicidality ORs ~2.10/2.29 [5,9], RBD ~74%/12-yr phenoconversion [10,12], and crash multipliers [13,15,16,6] are quoted from source abstracts/text; the RBD 74% figure is from a large cohort cited within review [12] and should carry the cohort-N caveat at ingestion.
- **Thresholds where guidelines vary.**
  - *OSA referral urgency* is not codified as a single guideline number; "URGENT vs ROUTINE" here is a defensible synthesis (driving/cardiac comorbidity escalates urgency), not a verbatim guideline cut.
  - *STOP-Bang risk bands* (≥5 high; 3–4 intermediate) are widely used but some validation papers favor different cut-points by population — the population-mismatch caveat applies.
  - *Suicidality escalation* — the EMERGENCY threshold (active SI/plan/intent → 988/ED) is a safety-conservative product decision, not a sleep-guideline statement; it should be reviewed against the medical-liaison adjudication layer.
  - *Chronic insomnia* ≥3 nights/wk × ≥3 mo is the stable ICSD-3 criterion [7]; no material variation found.
