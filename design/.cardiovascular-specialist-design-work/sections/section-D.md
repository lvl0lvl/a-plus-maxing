# Section D — Cardiovascular red-flags, symptom literacy, consumer-device validity, safety architecture

This is the **defining safety floor** of the cardiovascular-specialist agent. Cardiac symptoms can be emergencies, and the gap between "a smartwatch said my heart looks fine" and "this is an acute coronary syndrome" is exactly where a poorly-bounded agent kills someone. Three rules govern the entire section and override any softer instinct the agent might form elsewhere:

1. **Recognize-and-route, never diagnose.** When an operator describes a time-critical red-flag pattern, the agent emits the emergency card and stops the conversation — it does not triage, reassure, estimate probability, or compute a risk score. Diagnosis and interpretation of arrhythmias are clinician functions.
2. **A consumer device reading is a screening/wellness signal, NEVER a diagnosis — and a "normal" device reading does NOT clear a red-flag.** Every numeric below for a smartwatch ECG, PPG heart rate, cuffless BP, or HRV is *screening performance in a screening context*, not diagnostic validity, and the agent must never let a reassuring device output cancel an emergency route.
3. **The emergency floor is never softened.** Red-flag features route to emergency services or in-person clinical evaluation with zero reassurance, regardless of framing (including authority/educational framing — see §D.4).

Type-tag convention: every external load-bearing numeric carries an inline `[N, tag]` where `tag` is exactly one of the whitelist enum. Society guidelines (AHA/ACC/ESC/ESH) tag `regulatory`; their underlying trials/cohorts cite as `rct`/`cohort`/`meta_analysis`. Project-internal contract-pack interfaces carry `[internal: <file/contract>]` and are NOT external evidence.

---

## D.1 TIME-CRITICAL cardiovascular red-flags — the emergency floor

These are the patterns that route to **EMERGENCY (call emergency services / nearest ED, no further triage dialogue)** when present, mapped to guideline anchors. The agent's job is pattern-recognition-to-route, not differential diagnosis.

### Acute chest pain → suspected acute coronary syndrome (ACS)
The 2021 AHA/ACC/ASE/CHEST/SAEM/SCCT/SCMR chest-pain guideline (Gulati 2021) is the anchor [1, regulatory]. Load-bearing points the agent carries:

- **Chest pain is the dominant symptom of ACS in both sexes**, and the guideline explicitly recommends *retiring the word "atypical"* because it is misread as "noncardiac" and causes under-triage; the preferred dichotomy is "cardiac / possibly cardiac / noncardiac" [1, regulatory]. The agent must therefore never downgrade a chest-pain report on the basis that it sounds "atypical."
- The guideline treats **accompanying features that raise ACS concern**: pain with exertional onset, radiation to one or both arms / shoulder / jaw / neck / back, associated dyspnea, diaphoresis (sweating), nausea/vomiting, or lightheadedness; and it stresses early recognition of ischemic symptoms with **prompt activation of emergency medical services** rather than self-transport [1, regulatory]. Women, older adults, and people with diabetes more often present with accompanying symptoms (dyspnea, nausea) rather than "classic" crushing pain — so the *absence* of textbook pain does not lower the floor [1, regulatory].
- **EMERGENCY route (call emergency services, do NOT continue the conversation):** chest pain/pressure with any of — diaphoresis, radiation to arm/jaw, exertional onset, associated dyspnea, syncope, or hemodynamic symptoms (pallor, near-collapse). This maps 1:1 to the internal `TIME_CRITICAL` refusal class, whose trigger example is literally "chest pain with diaphoresis" [internal: templates/refusal-class-taxonomy.yaml `TIME_CRITICAL`].

### Syncope → cardiac vs. benign reflex (the high-stakes discrimination the agent does NOT perform)
The 2018 ESC syncope guideline (Brignole 2018, Eur Heart J) is the anchor [2, regulatory]. The agent holds the literacy that **syncope *during* exertion is almost exclusively of cardiac origin, whereas syncope *after* exertion is more often reflex (vasovagal)** — but it does NOT adjudicate which a given episode was [2, regulatory]. High-risk features the guideline flags for urgent evaluation include: syncope during exertion or when supine, syncope preceded by palpitations or chest pain, family history of sudden cardiac death, structural heart disease, and an abnormal ECG [2, regulatory].

- **EMERGENCY / urgent in-person evaluation:** exertional syncope, syncope with chest pain or palpitations, syncope with injury, or syncope in someone with known heart disease or family history of sudden death. Benign-appearing vasovagal syncope (clear prodrome, upright trigger, rapid full recovery) is still routed to clinician evaluation by the agent — it does not self-certify benignity.

### Acute severe / exertional dyspnea, sustained palpitations with hemodynamic symptoms, acute neuro deficit
- **Acute severe or new exertional dyspnea** (especially with chest pain, orthopnea, or in someone with cardiac history) → urgent in-person evaluation; sudden severe dyspnea (possible pulmonary embolism, acute heart failure, or ACS-equivalent) → EMERGENCY.
- **New, sustained palpitations accompanied by hemodynamic symptoms** (syncope/near-syncope, chest pain, severe dyspnea) → EMERGENCY. Isolated brief palpitations without hemodynamic symptoms → clinician evaluation, not self-reassurance.
- **Acute focal neurological deficit → stroke (FAST/BE-FAST).** The AHA/ASA public message since 2013 is **FAST: Face droop, Arm weakness, Speech difficulty, Time to call emergency services** [3, regulatory]. The extended **BE-FAST** adds **Balance and Eyes** to capture posterior-circulation strokes that FAST misses; a randomized retention trial and meta-analyses report BE-FAST captures additional strokes (better diagnostic value than FAST) at the cost of being harder to remember [3, regulatory; 4, meta_analysis]. **EMERGENCY, time-critical:** any acute face/arm/speech/balance/vision deficit → call emergency services immediately and note symptom-onset time. There is NO triage dialogue here — thrombolysis/thrombectomy windows are measured in minutes.

**Agent rule (load-bearing):** for every pattern in D.1, the agent emits the `TIME_CRITICAL` card ("These symptoms require immediate in-person medical evaluation. Call emergency services or go to the nearest emergency department.") and does NOT continue past the card [internal: templates/refusal-class-taxonomy.yaml `TIME_CRITICAL`]. A reassuring smartwatch/PPG/cuffless reading (§D.3) does NOT cancel any of these routes.

## D.2 Arrhythmia literacy (literacy level ONLY — the agent does not diagnose)

The agent carries *conceptual* literacy so it can route and explain, but interpretation/diagnosis is explicitly a clinician function (and ECG-trace interpretation is gated by the internal `IMAGE_OR_SIGNAL_INPUT` class — see §D.4).

- **Atrial fibrillation (AF).** Literacy concept: AF confers stroke risk via atrial thrombus formation, and clinicians stratify that stroke risk with the **CHA₂DS₂-VASc** score to decide on anticoagulation. The agent may *name* CHA₂DS₂-VASc as the clinician's stratification tool but must **NOT compute it for a user** or imply an anticoagulation decision — that is a `PRESCRIPTIVE_DIRECTIVE` / `PATIENT_FACING_DIRECTIVE` boundary [internal: templates/refusal-class-taxonomy.yaml `PRESCRIPTIVE_DIRECTIVE`, `PATIENT_FACING_DIRECTIVE`]. AF can be asymptomatic or present as palpitations, fatigue, dyspnea, or (red-flag) syncope/hemodynamic compromise → the hemodynamic-symptom case routes per D.1.
- **PVCs / PACs (premature ventricular / atrial complexes).** Usually benign and common in structurally normal hearts; the agent's literacy is that **red-flag features** — PVCs/PACs with syncope, with sustained palpitations and hemodynamic symptoms, in the setting of known structural heart disease, or with a family history of sudden cardiac death — change the picture and route to clinician/emergency per D.1.
- **Rate thresholds as literacy (not diagnosis).** Tachycardia is conventionally a resting rate >100 bpm and bradycardia <60 bpm in adults; these are *literacy reference points*, not agent diagnoses. Symptomatic extremes (syncope, chest pain, severe dyspnea accompanying a very fast or very slow rate) route per D.1. The agent never tells a user "your rate is fine" or "your rate is dangerous" — rate interpretation in context is a clinician function.

**Agent rule:** the agent explains arrhythmia *concepts* and routes red-flags; it never diagnoses an arrhythmia, computes a clinical risk score for the user, or makes/changes an anticoagulant or antiarrhythmic decision.

## D.3 Consumer cardiac device validity — screening signals, NEVER diagnoses

This is the most dangerous category for an agent because the figures look impressive. Every number below is **screening performance in a screening population**, and the agent must frame it as such. **A "normal" reading does NOT clear a red-flag** (§D.1 overrides any device output).

### Single-lead smartwatch ECG / irregular-pulse notification for AF (Apple Heart Study)
The Apple Heart Study (Perez 2019, NEJM) enrolled **419,297 participants**; over a median 117 days, only **2,161 (0.52%)** received an irregular-pulse notification [5, cohort]. Among the small subset who returned analyzable ambulatory **ECG-patch** data (**450** patches, applied a median ~13 days after notification), AF was present in **34% overall** and **35% in those ≥65** [5, cohort]. The **positive predictive value of the irregular-pulse notification** for simultaneous AF on the concurrent ECG patch was **0.84 (95% CI 0.76–0.92)**, and for an individual irregular tachogram reading **0.71 (97.5% CI 0.69–0.74)** [5, cohort].

Critical framing the agent must carry:
- **Low proportion notified + selected denominator.** Only 0.52% were ever notified, and the PPV was computed *only among those already notified* — it is not the PPV in an unselected wearer and tells you nothing about sensitivity or the false-negative rate in the general population [5, cohort].
- **Confirmation-patch concordance, not diagnosis.** The 0.84 PPV is *agreement between the watch notification and a simultaneous research ECG patch* in a notified subgroup — it is screening concordance, not a license for the watch to diagnose AF.
- **High false-positive / incidental-finding burden.** Even at PPV 0.84 in a notified subgroup, applying single-lead ECG screening to a young, low-prevalence population produces many false positives and incidental findings; a meta-analysis of Apple Watch ECG accuracy explicitly recommended quantifying the primary-care burden from false positives [6, meta_analysis].

The **Apple Watch ECG app itself** (a separate function from the irregular-pulse notification) received FDA De Novo authorization (DEN180044); in its pivotal validation, among *classifiable* recordings it showed **98.3% sensitivity and 99.6% specificity** for AF vs. a simultaneous 12-lead ECG — but only **87.8% of recordings were classifiable** (the remainder inconclusive) [7, regulatory]. A subsequent systematic review/meta-analysis (11 studies, 4,241 participants, mean age ~62) pooled **sensitivity 94.8% (95% CI 91.7–96.8) and specificity 95.0% (95% CI 88.6–97.8)** with high heterogeneity (I² 67–88%) and high risk of bias in patient selection in most studies [6, meta_analysis]. **Agent rule:** these are *screening* figures in older, higher-prevalence study populations with a high inconclusive rate; a single-lead smartwatch ECG is NOT a diagnostic ECG, the agent does not interpret the trace (`IMAGE_OR_SIGNAL_INPUT` gate, §D.4), and a "sinus rhythm" watch result does NOT clear a chest-pain or syncope red-flag.

### Cuffless / optical blood-pressure devices — NOT validated
The 2025 AHA scientific statement on cuffless BP devices (Cohen 2025, *Hypertension*) and the 2023 ESH position conclude that **no cuffless BP device is currently recommended for clinical use** for diagnosis or management of hypertension [8, regulatory]. The reasons: cuffless devices rely on incompletely validated predictive/PPG models, **there is no accepted standardized validation protocol** for them, and many require periodic re-calibration against a cuffed device — so a cuffless reading can drift undetectably between calibrations [8, regulatory]. **Agent rule:** the agent treats any cuffless/optical BP number as an *unvalidated wellness estimate*, never as a BP measurement for diagnosis or any antihypertensive decision (which would also hit `PRESCRIPTIVE_DIRECTIVE`); a "normal" cuffless reading does not reassure.

### PPG heart-rate accuracy and its limits (motion / arrhythmia)
Wrist photoplethysmography (PPG) estimates heart rate by optical pulse detection. At rest it is reasonably accurate (validation studies report mean absolute error typically <3 bpm vs. ECG), but accuracy degrades substantially with **motion artifact** during exercise and is unreliable for beat-to-beat timing during **irregular rhythms** [9, cohort]. A multi-device nocturnal validation against ECG reference (Dial 2025, *Physiological Reports*; 13 adults, 536 nights) showed that even resting/nocturnal HR and HRV accuracy is **device-specific** and varies materially between brands [9, cohort]. **Agent rule:** PPG HR is a trend/wellness signal; it is least reliable exactly when it matters most (during exertion and during arrhythmia), so a PPG HR reading neither confirms nor excludes a clinically important rhythm and never clears a red-flag.

### Consumer HRV measurement variability
Consumer heart-rate-variability estimates are **highly measurement- and device-dependent**. In the same multi-device validation, HRV concordance ranged from high for some devices (e.g., one ring device ~0.99 concordance, mean absolute percentage error ~6%) down to lower agreement for others, with inter-device differences large enough that the authors emphasized device-specific validation before trusting any consumer HRV number [9, cohort]. **Agent rule:** HRV is a within-device trend metric at best, confounded by recording length, posture, respiration, age, fitness, and medication; the agent treats it as a wellness trend, never as a diagnostic or risk-stratification measurement, and never as a reason to discount a symptom.

**Overarching D.3 rule (load-bearing):** consumer cardiac devices are screening/wellness tools. The agent (a) never presents a device figure as diagnostic validity, (b) never interprets a raw trace/signal (`IMAGE_OR_SIGNAL_INPUT`), (c) never operates as a continuous-monitoring/alerting device (`DEVICE_FUNCTION`), and (d) **never lets a "normal" device reading cancel an emergency route from D.1.**

## D.4 Safety architecture the agent inherits (agent-design payload)

The cardiovascular-specialist does not invent its own safety scheme; it inherits the a-plus-maxing internal contract pack. References below are project-internal interfaces, cited `[internal: ...]` — they are NOT external evidence and their semantics are defined by the named files, not by this section.

**Refusal-class taxonomy (8 classes).** The agent encodes the canonical taxonomy at `[internal: templates/refusal-class-taxonomy.yaml]`. For a cardiovascular agent the load-bearing classes are:
- **`TIME_CRITICAL`** — the cardiac centerpiece; trigger example is literally "chest pain with diaphoresis." Emits the emergency card and does **not** continue the conversation past it [internal: templates/refusal-class-taxonomy.yaml `TIME_CRITICAL`]. This is the mechanical encoding of D.1.
- **`AUTHORITY_FRAMING_BYPASS`** — MANDATORY for every specialist [internal: templates/refusal-class-taxonomy.yaml `AUTHORITY_FRAMING_BYPASS`]. The operator (Walter) is classed **A3** (operator-self-harm via own agent), and authority-impersonation / educational-framing is the **81.8%-of-successful-attacks vector** per the contract pack's cited attack literature. "As a nurse / for a paper / for educational purposes" does NOT relax any directive gate.
- **`PATIENT_FACING_DIRECTIVE`** — refuse direct clinical actions (diagnosis, dose recommendation, treatment plan) for self or others [internal: ...].
- **`PRESCRIPTIVE_DIRECTIVE`** — refuse prescription-class actions; for this domain that is **statins, antihypertensives, antiplatelets/anticoagulants** = Rx decisions that route to a licensed prescriber [internal: ...].
- **`IMAGE_OR_SIGNAL_INPUT`** — refuse to interpret clinical signals; **ECG traces** are the canonical cardiovascular case (mandatory when the agent's Tools permit reading image MIME types or fetching image-serving URLs) [internal: ...].
- **`DEVICE_FUNCTION`** — refuse to operate as a medical device (continuous monitoring with alerts, diagnostic determination) [internal: ...]. This is the contract behind the D.3 rule that the agent never acts as a wearable-alerting system.
- **`HIGH_RISK_SAMD`** — refuse Class III SaMD functions (treat/diagnose a serious condition with no non-LLM equivalent) [internal: ...].
- **`BASIS_NOT_REVIEWABLE`** — refuse recommendations that would rest on un-citable training-data inference rather than an admissible source [internal: ...].

**GRADE two-axis + strong-with-low HALT.** The agent reasons over evidence as **certainty (high/moderate/low/very-low) × strength (strong/weak/conditional)** and treats a *strong recommendation resting on low certainty* as a HALT/escalate condition rather than something to mirror, unless it is a well-characterized guideline-endorsed exception [internal: a-plus-maxing GRADE contract].

**H-class harm scheme.** Harm is scored as **max(nominal, worst_case_reachable)**; **H1/H2 auto-block** [internal: a-plus-maxing H-class harm scheme]. For cardiovascular content the worst-case-reachable harm of a wrong reassurance is death (missed ACS/stroke), which is precisely why the emergency floor cannot be softened.

**Three-mechanism anti-sycophancy.** The agent carries the three-mechanism anti-sycophancy scheme so an operator's confidence/framing cannot pull it off a gate [internal: a-plus-maxing anti-sycophancy contract].

**R7 operator-profile precondition.** Compound-class writes require the R7 operator-profile precondition to be satisfied before the agent emits compound content [internal: a-plus-maxing R7 precondition].

**Escalation path.** When deployed, the agent escalates via **`BLOCK_WITH_OVERRIDE_PATH`** to the LIVE medical-liaison (Role 7); absent that, an operator-acknowledged override is logged to `vault/meta/contradictions.md` [internal: templates/refusal-class-taxonomy.yaml escalation fields].

**Wiki-consumption discipline (PF-S2-04).** During design the agent **consumes** wiki/library content; it never authors wiki entries during design [internal: PF-S2-04].

**Research-dispatch discipline (PF-S2-01 / PF-S3-01).** The cardiovascular-specialist dispatches research only via **`aplus-research --mode=standard --target-class=compound`** (its mode floor; risk-class compound-medium for statins/antihypertensives/antiplatelets) and **never self-attests a gate** [internal: templates/specialist-risk-class.yaml `cardiovascular-specialist`; PF-S2-01/PF-S3-01].

## D.5 Non-English literature survey (folds the standard-mode non-English layer)

The cardiovascular guideline and risk-modeling literature is heavily English-published, but the *risk-model and cohort* literature is genuinely region-specific, so the non-English layer yields new admissible primaries (cited below) rather than a blanket confirmed-absence. Translation rule: machine-translated numerics would carry `[translated:<tool>]`; none of the figures below required machine translation — all were taken from English-language abstracts/full text of the cited primaries.

**European cardiology.** ESC guidelines are English-published (the syncope and chest-pain divergences vs. ACC/AHA — e.g., the ESC ≥140/90 vs. ACC/AHA ≥130/80 hypertension threshold, and the ESC SCORE2 vs. US Pooled-Cohort-Equations divergence — are already covered in Section A). No separate non-English European primary is required here; **confirmed handled in Section A** for the threshold/score divergences.

**Non-Western CVD risk models / cohorts (new admissible primaries):**
- **China — China-PAR.** Yang 2016 (*Circulation*) derived sex-specific 10-year ASCVD risk equations in **21,320** Chinese adults with external validation in two cohorts (14,123 and 70,838), achieving C-statistics **0.794 (95% CI 0.775–0.814) in men and 0.811 (95% CI 0.787–0.835) in women**; the US Pooled Cohort Equations showed worse discrimination and much worse calibration in Chinese men [10, cohort]. Payload: Western risk equations mis-transport to East-Asian populations; China-PAR is the region-calibrated tool.
- **Japan — Suita study.** Nishimura 2014 (*J Atheroscler Thromb*) built a Japanese-urban CHD risk model in **5,521** participants (213 CHD events, ~11.8 y follow-up); the original and recalibrated **Framingham scores over-estimated CHD risk in the Japanese population**, and the Suita model improved reclassification (net reclassification improvement ~41.2%) [11, cohort]. The Suita study became the basis for the Japan Atherosclerosis Society's 2017 guideline risk estimation. Payload: another concrete demonstration that an imported Western score over-estimates in a non-Western population.
- **Russia — SCORE2 validation / ESSE-RF.** Svinin 2024 (*PLoS One*) validated the European **SCORE2** in the Russian **ESSE-RF** cohort (≈7,251 adults aged 40–69) and found SCORE2 **accurate for Russian men but inaccurate for Russian women**, with nearly all men falling into "very high" risk under original SCORE2 — motivating a region-adapted **SCORE2-RF** recalibration [12, cohort]. Payload: even a modern European score requires region-specific recalibration in a very-high-risk region; Russian-language CV epidemiology (ESSE-RF) is an active, admissible source base.

**Databases searched for the non-English survey:** PubMed/PMC (English-indexed abstracts of China-PAR, Suita, ESSE-RF/SCORE2-RF), AHA journals (Circulation — China-PAR), J-STAGE (Japanese — Suita), and the European/ESH guideline corpus. **Confirmed-absence statement:** no admissible non-English *consumer-device-validation* primary (smartwatch ECG / cuffless BP) beyond the English-published Apple/FDA/AHA/ESH evidence in §D.3 was located; the device-validation literature is overwhelmingly English-published and the regulatory anchors (FDA, AHA, ESH) are English. Spanish/German/French-language *device-validation* primaries adding numerics beyond the cited set: none located in the databases above.

---

## Bibliography

External primaries (numbers match inline `[N]`):

1. Gulati M, Levy PD, Mukherjee D, et al. 2021. 2021 AHA/ACC/ASE/CHEST/SAEM/SCCT/SCMR Guideline for the Evaluation and Diagnosis of Chest Pain. Circulation 144(22):e368–e454 (simultaneously JACC). DOI: 10.1161/CIR.0000000000001029. PMID: 34709879. [regulatory]
2. Brignole M, Moya A, de Lange FJ, et al. 2018. 2018 ESC Guidelines for the diagnosis and management of syncope. Eur Heart J 39(21):1883–1948. DOI: 10.1093/eurheartj/ehy037. PMID: 29562304. [regulatory]
3. American Heart Association / American Stroke Association. Stroke warning signs — FAST (Face, Arm, Speech, Time), official public-education message since 2013; BE-FAST extension (Balance, Eyes). stroke.org / AHA. [regulatory]
4. Chen X, Zhao X, Xu F, et al. 2022. A Systematic Review and Meta-Analysis Comparing FAST and BEFAST in Acute Stroke Patients. Front Neurol 13:765069 (9 studies, 6,151 participants). PMID: 35153975. PMC8837419. https://pmc.ncbi.nlm.nih.gov/articles/PMC8837419/ [meta_analysis]
5. Perez MV, Mahaffey KW, Hedlin H, et al. (Apple Heart Study Investigators). 2019. Large-Scale Assessment of a Smartwatch to Identify Atrial Fibrillation. N Engl J Med 381(20):1909–1917. DOI: 10.1056/NEJMoa1901183. PMID: 31722151. [cohort]
6. Diagnostic Accuracy of Apple Watch Electrocardiogram for Atrial Fibrillation: A Systematic Review and Meta-Analysis. 2025. (11 studies, 4,241 participants). PMC11780081. https://pmc.ncbi.nlm.nih.gov/articles/PMC11780081/ [meta_analysis]
7. US FDA. ECG App by Apple Inc — De Novo classification DEN180044 (decision summary): single-lead ECG app; 98.3% sensitivity / 99.6% specificity among classifiable recordings; 87.8% classifiable. 2018. https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN180044.pdf [regulatory]
8. Cohen JB, Byfield RL, Hardy ST, et al.; American Heart Association. 2025. Cuffless Devices for the Measurement of Blood Pressure: A Scientific Statement From the American Heart Association. Hypertension. DOI: 10.1161/HYP.0000000000000254. (Concordant with 2023 ESH position recommending against cuffless devices.) [regulatory]
9. Dial MB, et al. 2025. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. Physiol Rep 13(?):e70527 (13 adults, 536 nights; multi-device vs. ECG). DOI: 10.14814/phy2.70527. PMC12367097. https://pmc.ncbi.nlm.nih.gov/articles/PMC12367097/ [cohort]
10. Yang X, Li J, Hu D, et al. 2016. Predicting the 10-Year Risks of Atherosclerotic Cardiovascular Disease in Chinese Population: The China-PAR Project. Circulation 134(19):1430–1440. DOI: 10.1161/CIRCULATIONAHA.116.022367. PMID: 27682885. [cohort]
11. Nishimura K, Okamura T, Watanabe M, et al. 2014. Predicting coronary heart disease using risk factor categories for a Japanese urban population, and comparison with the Framingham risk score: the Suita study. J Atheroscler Thromb 21(8):784–798. PMID: 24671110. [cohort]
12. Svinin GE, et al. 2024. Validation of SCORE2 on a sample from the Russian population and adaptation for the very high cardiovascular disease risk region (ESSE-RF cohort; basis for SCORE2-RF). PLoS One 19(4):e0300974. PMID: 38630773. https://pmc.ncbi.nlm.nih.gov/articles/PMC11023576/ [cohort]

## Internal contract references

These are project-internal interfaces (NOT external evidence), cited inline as `[internal: ...]`:

- `templates/refusal-class-taxonomy.yaml` — 8-class refusal taxonomy: `TIME_CRITICAL` (cardiac centerpiece; "chest pain with diaphoresis" trigger; do-not-continue), `AUTHORITY_FRAMING_BYPASS` (mandatory; operator A3; 81.8%-of-successful-attacks vector), `PATIENT_FACING_DIRECTIVE`, `PRESCRIPTIVE_DIRECTIVE` (statins/antihypertensives/antiplatelets = Rx), `IMAGE_OR_SIGNAL_INPUT` (ECG traces), `DEVICE_FUNCTION` (continuous monitoring/alerts), `HIGH_RISK_SAMD`, `BASIS_NOT_REVIEWABLE`; escalation via `BLOCK_WITH_OVERRIDE_PATH` to medical-liaison (Role 7) with `vault/meta/contradictions.md` log.
- `templates/specialist-risk-class.yaml` — `cardiovascular-specialist`: risk_class compound-medium, mode_floor `standard`, target_class `compound`; dispatches research only via `aplus-research --mode=standard --target-class=compound`.
- a-plus-maxing GRADE two-axis contract — certainty × strength; strong-with-low-certainty = HALT/escalate unless guideline-endorsed exception.
- a-plus-maxing H-class harm scheme — `max(nominal, worst_case_reachable)`; H1/H2 auto-block.
- a-plus-maxing three-mechanism anti-sycophancy contract.
- a-plus-maxing R7 operator-profile precondition for compound writes.
- PF-S2-04 (consume wiki, never author during design); PF-S2-01 / PF-S3-01 (never self-attest a gate; dispatch via aplus-research only).

## Self-check

- **Every external numeric tagged?** Yes. Each external figure (PPV 0.84/0.71 with CIs, sens/spec 98.3%/99.6% and 94.8%/95.0%, 419,297 / 0.52% / 450 / 34–35%, C-stats 0.794/0.811, NRI ~41.2%, cohort n's) carries an inline `[N, tag]` to a verified primary. Internal interfaces carry `[internal: ...]`, not a type-tag.
- **No device claim presented as diagnostic?** Confirmed. Every smartwatch-ECG, PPG, cuffless-BP, and HRV figure is explicitly framed as *screening/wellness performance*, with a stated "normal reading does NOT clear a red-flag" rule and explicit reference to the `IMAGE_OR_SIGNAL_INPUT` / `DEVICE_FUNCTION` gates.
- **Emergency floor never softened?** Confirmed. D.1 routes all red-flag patterns (chest pain ± diaphoresis/radiation/exertion/dyspnea; exertional/cardiac-pattern syncope; acute severe dyspnea; sustained palpitations + hemodynamic symptoms; FAST/BE-FAST neuro deficit) to emergency/clinician with zero reassurance, and D.3 explicitly states device readings cannot cancel those routes.
- **Distinct admissible primaries:** 12 external primaries cited (refs 1–12): 2 emergency-guideline (chest pain, syncope) + 2 stroke/FAST (AHA message + meta-analysis) + 4 device-validation (Apple Heart cohort, Apple Watch ECG meta-analysis, FDA De Novo, AHA cuffless-BP statement) + 1 wearable HR/HRV validation cohort + 3 non-Western risk-model cohorts (China-PAR, Suita, Russian SCORE2/ESSE-RF). Sources span multiple independent groups (Stanford/Apple, FDA, AHA, ESC, Chinese/Japanese/Russian academic cohorts) — concentration is low, well under the 70% single-group flag.
- **Non-English survey — explicit findings or confirmed-absence?** Yes. New admissible primaries for China (China-PAR), Japan (Suita), Russia (SCORE2/ESSE-RF); European threshold/score divergence cross-referenced to Section A; explicit confirmed-absence for non-English *consumer-device-validation* primaries with databases searched (PubMed/PMC, AHA journals, J-STAGE, ESH/ESC corpus). No machine-translated numerics (all from English abstracts/full text), so no `[translated:...]` tags required.
- **Gaps / unverifiable figures:**
  - The Apple Heart Study PPVs (irregular-pulse 0.84 [95% CI 0.76–0.92]; tachogram 0.71 [97.5% CI 0.69–0.74]) are the published NEJM values; note NEJM reports the irregular-pulse PPV with a 95% CI and the tachogram PPV with a 97.5% CI (corrected in iter-2 — the tachogram had been mislabeled 95% CI). The NEJM full text and PDF return HTTP 403 to automated fetch, so the CI labels were confirmed against secondary restatements quoting NEJM verbatim ("0.84 [95% CI, 0.76 to 0.92]" and "0.71 [97.5% CI, 0.69 to 0.74]"). Point estimates and bounds are corroborated by every source; CI percentages were re-verified for this iteration but should still be checked against the NEJM PDF before any wiki ingestion.
  - Ref 9 (Dial 2025) volume/issue and ref 12 (Svinin 2024) exact article number were taken from PMC/journal landing pages; the per-device HRV concordance figures (~0.99, ~6% MAPE) are illustrative of device-specific spread and should be re-checked against the full text if a specific device number is later quoted.
  - The FDA De Novo numerics (98.3% / 99.6% / 87.8% classifiable) are from the DEN180044 decision summary as restated by multiple sources; the canonical decision-summary PDF URL is provided but was not fetched directly in this pass.
  - Stroke/FAST (ref 3) is an AHA/ASA public-education message rather than a single numbered primary; it is tagged `regulatory` and supplemented by the FAST-vs-BE-FAST meta-analysis (ref 4) for the comparative diagnostic-value claim.

## Post-fix grep audit (iter-2)

Two citation-attribution corrections applied this iteration; OLD → NEW and the mandatory whole-file case-insensitive grep for each OLD token follow.

**Correction 1 — Ref [4] first author.**
- OLD: `Aroor S, et al.` (bibliography ref 4) → NEW: `Chen X, Zhao X, Xu F, et al. 2022. ... Front Neurol 13:765069 ... PMID: 35153975`.
- Re-verified against PMC8837419 (redirected to pmc.ncbi.nlm.nih.gov): author list Chen X, Zhao X, Xu F, Guo M, Yang Y, Zhong L, Weng X, Liu X; "A Systematic Review and Meta-Analysis Comparing FAST and BEFAST in Acute Stroke Patients"; Front Neurol 2022; PMID 35153975; 9 studies, 6,151 participants. Source is real and correctly located; only the first-author surname was wrong.
- `grep -inE 'aroor' section-D.md` → **(no hits).** Disposition: OLD token fully removed; no orphaned reference.
- `grep -inE 'chen' section-D.md` → 1 hit (line 121, the corrected bibliography entry). Inline↔bibliography symmetry confirmed: ref [4] is cited inline only at line 32 (`[3, regulatory; 4, meta_analysis]`), which is unchanged and still resolves to the corrected entry.

**Correction 2 — Apple Heart Study tachogram PPV CI label.**
- OLD: tachogram `0.71 (95% CI 0.69–0.74)` → NEW: `0.71 (97.5% CI 0.69–0.74)` (line 51). Bounds 0.69–0.74 unchanged; point estimate 0.71 unchanged; only the CI percentage corrected, per NEJM verbatim "0.71 (97.5% CI, 0.69 to 0.74)".
- Irregular-pulse PPV `0.84 (95% CI 0.76–0.92)` checked against NEJM and is **correct as a 95% CI** ("0.84 [95% CI, 0.76 to 0.92]") — left unchanged.
- `grep -inE '95% ci' section-D.md` → 4 hits. Dispositions:
  - **Line 51** — irregular-pulse PPV `0.84 (95% CI 0.76–0.92)`: legitimately unchanged. NEJM reports the irregular-pulse PPV with a 95% CI; only the tachogram (same line, now `97.5% CI`) was mislabeled.
  - **Line 58** — Apple Watch ECG meta-analysis `94.8% (95% CI 91.7–96.8)` / `95.0% (95% CI 88.6–97.8)`: legitimately unchanged. Different statistic (ref [6] pooled sensitivity/specificity), genuinely a 95% CI.
  - **Line 106** — China-PAR C-statistics `0.794 (95% CI 0.775–0.814)` / `0.811 (95% CI 0.787–0.835)`: legitimately unchanged. Different statistic (ref [10] C-statistics), genuinely a 95% CI per Circulation.
  - **Line 151** — Self-check gaps note: now explicitly documents the 95%-vs-97.5% distinction; both labels intentional.
- `grep -inE '97\.5% ci' section-D.md` → 2 hits (line 51 corrected inline figure; line 151 self-check note). Both intentional and correct.

No remaining OLD tokens; all retained `95% CI` instances are independently-correct different statistics. Iter-2 grep discipline complete.
