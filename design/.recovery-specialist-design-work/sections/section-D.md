# Section D — Safety architecture, red-flags & boundary discipline

This section is the safety backbone of the `recovery-specialist` agent. It enumerates the
signals that mandate escalation rather than self-managed recovery advice, the
contraindications to recovery modalities the agent might otherwise recommend, the boundary
discipline that keeps this agent inside its lane, and the principle that a wearable number is
not a diagnosis. Each red-flag below is mapped to one of three escalation tiers:

- **EMERGENCY** — call emergency services / same-day acute care; agent does not "advise," it routes.
- **URGENT-REFERRAL** — stop self-management, refer to the medical-liaison / a clinician within days.
- **ROUTINE-MONITOR** — track over weeks; escalate to URGENT-REFERRAL if the trend persists or worsens.

## Red-flags & escalation tiers

### Persistent unexplained fatigue / sustained performance decline

A sustained, unexplained drop in training performance with disproportionate fatigue is the
single most common presentation the recovery agent will see, and it is **the one most likely
to hide organic disease**. The ECSS/ACSM joint consensus on overtraining is explicit that
overtraining syndrome (OTS) is a **diagnosis of exclusion**: organic disease, infection, and
nutritional deficiency (iron, magnesium, carbohydrate/protein insufficiency, energy
restriction) must be ruled out *before* fatigue is attributed to training load
[5, regulatory]. The differential for unexplained fatigue plus performance decline spans
iron-deficiency anemia, hypothyroidism, depression, occult infection, low energy
availability (RED-S), sleep disorder, and cardiac disease [5, regulatory]. Iron deficiency is
common in athletes (15–35% of females, 3–11% of males), and hypothyroidism presents with the
same fatigue/cold-intolerance/performance-decline picture [5, regulatory]. **Tier:
URGENT-REFERRAL** — the agent must never label sustained unexplained decline as "just
overtraining"; it routes to the medical-liaison for bloodwork (CBC, ferritin/iron studies,
TSH) and clinical exclusion.

### Resting tachycardia (sustained elevated RHR)

A sustained resting trend upward of roughly 5–10 bpm over weeks is a recognized (if
imperfect and inconsistent) early marker of overtraining, illness, or poor sleep
[5, regulatory]. That is a ROUTINE-MONITOR signal. The escalation-relevant fact is
different: a **resting heart rate above 100 bpm (sinus tachycardia) at rest always warrants
medical evaluation** [6, mechanism_review]. Its differential is broad and includes
escalation-worthy causes — fever/infection (including myocarditis), anemia, hyperthyroidism,
hypovolemia/dehydration, pulmonary embolism, hypoxia, acute coronary syndrome, and drug
effects [6, mechanism_review]. The agent cannot disambiguate these; sustained resting
tachycardia is therefore **Tier: URGENT-REFERRAL** (workup per the cardiovascular-specialist /
clinician: ECG, Holter, echo, CBC, TSH as indicated). Resting tachycardia *with* chest pain,
syncope, or breathlessness is **Tier: EMERGENCY** [6, mechanism_review].

### Suspected illness/infection + training — the myocarditis question

This is the highest-consequence escalation in the section because the failure mode is sudden
cardiac death. The convention many sports physicians use is the **"neck check"**: exercise
permitted if symptoms are confined above the neck (rhinorrhea, sore throat), stop if symptoms
are below the neck (fever, body aches, productive cough, chest involvement). The primary
literature is clear the neck check is **nonscientific but partly useful** — it fails because
adenoviral tonsillitis, enteroviral pharyngitis, and streptococcal tonsillopharyngitis are
"above-the-neck" presentations that are nonetheless dangerous in athletes [1, mechanism_review].
The same review tempers the alarm: systematic data show myocarditis is a *rare* cause of
sports-related sudden cardiac death, and there is a lack of evidence that exercising through a
common cold causes significant harm [1, mechanism_review]. The load-bearing rule the agent
should encode is therefore narrow and firm: **systemic features — fever, myalgia, resting
tachycardia, malaise — are a stop-and-escalate signal, not a "push through" signal**
[1, mechanism_review]. And the symptom triad that mandates immediate cessation and cardiac
evaluation is **chest pain, syncope, shortness of breath, or palpitations during or after
illness** [1, mechanism_review]. **Tier: fever/systemic illness → URGENT-REFERRAL (do not
train, defer to clinician); the chest-pain/syncope/palpitations triad → EMERGENCY.** Confirmed
or suspected myocarditis is managed by cardiology — return-to-play guidance recommends
**abstention from exercise for 3–6 months** and return-to-play only after normalization of
systolic function and cardiac biomarkers and absence of arrhythmia on Holter/exercise ECG
[2, mechanism_review]. The agent owns none of that adjudication.

### RED-S / Relative Energy Deficiency in Sport (low energy availability)

RED-S is dangerous precisely because it **masquerades as "poor recovery."** Low energy
availability degrades performance, recovery, mood, bone health, endocrine function, and
immunity — the exact symptom cluster a recovery agent is built to address — and the 2023 IOC
consensus explicitly documents the overlap and intertwining of REDs with overtraining
syndrome [3, regulatory]. If the agent "treats the recovery symptoms" (more sleep, more cold
plunge, deload) without recognizing under-fueling, it entrenches the underlying deficit.
Markers associated with low energy availability include suppressed triiodothyronine (T3),
reduced resting metabolic rate, low total testosterone, menstrual dysfunction
(amenorrhea/oligomenorrhea), low bone mineral density on DXA, elevated cortisol, and
suppressed IGF-1 [4, mechanism_review]. **Tier: URGENT-REFERRAL** — RED-S suspicion is owned
by the nutritionist (energy-availability assessment/prescription) and the medical-liaison
(IOC REDs CAT2 severity/risk stratification and diagnosis) [3, regulatory]; the recovery
agent's job is to *recognize and route*, not to prescribe fueling.

### Mood / sleep disturbance — NFOR/OTS marker vs primary psychiatric pathology

Mood disturbance and disrupted sleep are core features of non-functional overreaching (NFOR)
and OTS, and are reported as more severe in OTS — though the consensus notes there is no
evidence to confirm or refute that gradation [5, regulatory]. The agent must not assume
mood/sleep symptoms are "training-derived." They can equally signal primary depression, an
anxiety disorder, or a sleep disorder — and depression sits squarely in the
unexplained-fatigue differential [5, regulatory]. **Tier: ROUTINE-MONITOR for mild
training-correlated mood/sleep dips; URGENT-REFERRAL when mood disturbance is persistent,
severe, functionally impairing, or accompanied by any safety concern** (the latter, e.g.
self-harm ideation, is EMERGENCY and routes to crisis care, not to a recovery agent).
Sleep-behavior screening is owned by the sleep-coach; psychiatric evaluation is owned by an MD.

## Modality contraindications

The recovery agent may suggest heat (sauna) and cold (cold-water immersion / cold plunge).
Both carry real cardiovascular risk and have populations for whom they are contraindicated.

### Sauna / heat

Sauna produces a hemodynamic load that "closely resembles moderate-intensity exercise":
heart rate and cardiac output rise, peripheral vasodilation drops systemic vascular
resistance, and core temperature rises [8, mechanism_review]. Large prospective cohorts
(Laukkanen) show frequent sauna use is *associated with reduced* cardiovascular and
sudden-cardiac-death risk and is safe for most people, including those with stable coronary
disease — **but explicitly recommend physician clearance first for at-risk individuals**
[8, mechanism_review]. **Contraindications** (do not advise sauna; route to clinician):
unstable angina, recent myocardial infarction (within ~3–6 months), severe aortic stenosis
(heat-induced vasodilation can precipitate dangerous hypotension), decompensated heart
failure, and uncontrolled hypertension [8, mechanism_review]. Pregnancy is a heat-exposure
caution (hyperthermia risk) and alcohol before/during sauna sharply raises risk
[8, mechanism_review]. **Tier: any of the above present → URGENT-REFERRAL (no sauna
recommendation until cleared).**

### Cold-water immersion / cold plunge

Cold immersion is more acutely dangerous than heat. Sudden skin cooling triggers the **cold
shock response** — an involuntary gasp, hyperventilation, tachycardia, and a hypertensive
surge that peaks within ~30 seconds and adapts over ~3 minutes; the gasp and hyperventilation
are a drowning risk and the cardiovascular surge loads the heart [7, mechanism_review]. More
specifically, Shattock & Tipton describe **"autonomic conflict"**: cold shock drives a
sympathetic tachycardia while simultaneous facial/oronasal cooling evokes the vagally-mediated
diving-reflex bradycardia, and this opposing input to the heart can provoke arrhythmias and
deaths previously misattributed to drowning — with **inherited long QT syndrome and underlying
cardiac electrophysiologic disease as the vulnerable populations** [7, mechanism_review].
**Contraindications** (do not advise cold immersion; route to clinician): uncontrolled
hypertension, known cardiac disease or arrhythmia (atrial fibrillation/flutter, long QT,
Brugada, hypertrophic cardiomyopathy, significant coronary disease, prior MI with reduced LV
function), recent cardiac event, and pregnancy [7, mechanism_review]. **Tier: any of
the above present → URGENT-REFERRAL; collapse/syncope/chest pain during immersion → EMERGENCY.**

## Boundary discipline (who owns what)

This agent **defers, it does not duplicate.** It recognizes signals and routes them to the
owning role. The ownership matrix below is the agent's escalation routing table.

| Concern | Owning role | Recovery-specialist action |
|---------|-------------|----------------------------|
| Sleep behavior, insomnia, sleep-disorder screening | sleep-coach | Flag sleep red-flags; defer behavior/screening |
| Fueling, energy-availability prescription, RED-S nutrition | nutritionist | Recognize under-fueling/RED-S; route, do not prescribe macros |
| HR / HRV pathology, arrhythmia, blood pressure | cardiovascular-specialist | Surface abnormal HR/BP/rhythm; defer interpretation |
| Training-load prescription (volume/intensity/deload) | personal-trainer | Advise *recovery*; do not write the training plan |
| Escalation, adjudication, REDs CAT2 risk-staging | medical-liaison | Route every URGENT-REFERRAL/EMERGENCY here |
| Diagnosis (anemia, hypothyroidism, myocarditis, depression) | MD | Never diagnose; describe findings and route |

The discipline rule: when a signal sits at a boundary (e.g. low HRV trend + poor sleep + mood
dip), the agent names the candidate owners and escalates to the medical-liaison for
adjudication rather than picking a lane itself.

## Wearable-is-not-diagnosis

A low HRV reading or a poor "readiness" score is **not a medical conclusion.** HRV is a
non-invasive monitoring signal whose interpretation is confounded by motion artifact (PPG
wearables), breathing pattern, posture, hydration, and large between-individual variability;
the mechanisms linking a single low reading to a specific cause remain unclear at the
individual level [9, mechanism_review]. The validated use of HRV in athletes is **trend
monitoring of an individual against their own baseline**, not point-diagnosis
[9, mechanism_review]. The hard rule the agent must encode: **never convert a wearable number
into a medical conclusion.** A low HRV or bad readiness score is a prompt to *ask questions
and, if a red-flag is corroborated, route* — it is never itself a diagnosis of overtraining,
infection, or cardiac disease. Diagnosis requires clinical correlation owned by an MD.

## Key claims for the agent design

- **Sustained unexplained fatigue + performance decline → URGENT-REFERRAL (medical-liaison/MD).**
  OTS is a diagnosis of *exclusion*; organic disease (anemia, thyroid, infection, depression,
  cardiac, RED-S) must be ruled out first [5, regulatory]. The agent never labels it "overtraining."
- **Resting tachycardia: RHR-trend +5–10 bpm over weeks → ROUTINE-MONITOR [5, regulatory];
  resting HR >100 bpm → URGENT-REFERRAL (cardiovascular-specialist); + chest pain/syncope →
  EMERGENCY** [6, mechanism_review].
- **Fever / systemic viral illness → stop training, URGENT-REFERRAL.** The "neck check" is
  nonscientific and partly useful at best; chest pain, syncope, shortness of breath, or
  palpitations during/after illness → **EMERGENCY** (myocarditis rule-out) [1, mechanism_review].
  Suspected myocarditis is cardiology-owned: 3–6 month exercise abstention + cleared workup
  before return [2, mechanism_review].
- **RED-S masquerades as poor recovery → URGENT-REFERRAL (nutritionist + medical-liaison).**
  Markers: low T3, low RMR, low testosterone, menstrual dysfunction, low BMD [4, mechanism_review];
  IOC documents REDs↔overtraining overlap [3, regulatory]. The agent recognizes, it does not
  prescribe fueling.
- **Mood/sleep disturbance → ROUTINE-MONITOR if mild/training-correlated; URGENT-REFERRAL if
  persistent/severe/impairing; safety concern → EMERGENCY.** Owned by sleep-coach (behavior)
  and MD (psychiatric) [5, regulatory].
- **Sauna contraindications → URGENT-REFERRAL, no recommendation until cleared:** unstable
  angina, recent MI (~3–6 mo), severe aortic stenosis, decompensated HF, uncontrolled
  hypertension; pregnancy/alcohol cautions [8, mechanism_review].
- **Cold immersion contraindications → URGENT-REFERRAL:** uncontrolled hypertension, known
  cardiac disease/arrhythmia (incl. long QT, Brugada, HCM), recent cardiac event, pregnancy.
  Cold-shock + autonomic conflict can cause fatal arrhythmia in vulnerable hearts; collapse
  during immersion → EMERGENCY [7, mechanism_review].
- **Boundary discipline:** sleep→sleep-coach, fueling→nutritionist, HR/HRV/BP/arrhythmia→
  cardiovascular-specialist, training-load→personal-trainer, escalation→medical-liaison,
  diagnosis→MD. The agent routes; it never duplicates or diagnoses.
- **Wearable-is-not-diagnosis:** a low HRV / bad readiness score is a trend prompt to ask and
  (if corroborated) route — never a medical conclusion [9, mechanism_review]. No wearable number
  is ever converted into a diagnosis.

## Bibliography

[1] Ruuskanen O, Valtonen M, Waris M, Luoto R, Heinonen OJ. 2023. Sport and exercise during viral acute respiratory illness—Time to revisit. Journal of Sport and Health Science. PMID: 38072364. DOI: 10.1016/j.jshs.2023.12.002. (Retrieved: 2026-05-31) [mechanism_review]

[2] Bryde RE, Cooper LT Jr, Fairweather D, Di Florio DN, Martinez MW. 2023. Exercise After Acute Myocarditis: When and How to Return to Sports. Cardiology Clinics. PMID: 36368807. DOI: 10.1016/j.ccl.2022.08.009. (Retrieved: 2026-05-31) [mechanism_review]

[3] Mountjoy M, Ackerman KE, Bailey DM, et al. 2023. 2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs). British Journal of Sports Medicine. 57(17):1073–1097. PMID: 37752011. DOI: 10.1136/bjsports-2023-106994. (Retrieved: 2026-05-31) [regulatory]

[4] Dvořáková K, Paludo AC, Wagner A, Puda D, Gimunová M, Kumstát M. 2024. A literature review of biomarkers used for diagnosis of relative energy deficiency in sport. Frontiers in Sports and Active Living. PMID: 39070233. DOI: 10.3389/fspor.2024.1375740. (Retrieved: 2026-05-31) [mechanism_review]

[5] Meeusen R, Duclos M, Foster C, Fry A, Gleeson M, Nieman D, Raglin J, Rietjens G, Steinacker J, Urhausen A. 2013. Prevention, diagnosis, and treatment of the overtraining syndrome: joint consensus statement of the European College of Sport Science and the American College of Sports Medicine. Medicine & Science in Sports & Exercise. 45(1):186–205. PMID: 23247672. DOI: 10.1249/MSS.0b013e318279a10a. (Retrieved: 2026-05-31) [regulatory]

[6] Henning A, Krawiec C. 2023. Sinus Tachycardia. StatPearls [Internet], NCBI Bookshelf. NBK553128. (Retrieved: 2026-05-31) [mechanism_review]

[7] Shattock MJ, Tipton MJ. 2012. 'Autonomic conflict': a different way to die during cold water immersion? The Journal of Physiology. 590(14):3219–3230. PMID: 22547634. DOI: 10.1113/jphysiol.2012.229864. (Retrieved: 2026-05-31) [mechanism_review]

[8] Laukkanen JA, Laukkanen T, Kunutsor SK. 2018. Cardiovascular and Other Health Benefits of Sauna Bathing: A Review of the Evidence. Mayo Clinic Proceedings. 93(8):1111–1121. PMID: 30077204. DOI: 10.1016/j.mayocp.2018.04.008. (Retrieved: 2026-05-31) [mechanism_review]

[9] Plews DJ, Laursen PB, Stanley J, Kilding AE, Buchheit M. 2013. Training adaptation and heart rate variability in elite endurance athletes: opening the door to effective monitoring. Sports Medicine. 43(9):773–781. PMID: 23852425. DOI: 10.1007/s40279-013-0071-8. (Retrieved: 2026-05-31) [mechanism_review]

## Self-check

(a) **Inline ↔ bibliography symmetry.** Every inline citation is in numbered `[N, tag]` form
keyed to the bibliography, and every numbered source is cited inline at least once. The map:
[1] Ruuskanen — neck-check/myocarditis rule, systemic-features stop signal, chest-pain triad;
[2] Bryde — return-to-play 3–6 mo myocarditis abstention; [3] Mountjoy/IOC REDs —
REDs↔overtraining overlap + CAT2 staging ownership; [4] Dvořáková — RED-S biomarkers;
[5] Meeusen/ECSS-ACSM — OTS diagnosis of exclusion, fatigue differential, iron/thyroid
prevalence, 5–10 bpm RHR trend, mood/sleep gradation; [6] Henning StatPearls — >100 bpm sinus
tachycardia threshold + differential + tachycardia-with-symptoms emergency; [7] Shattock &
Tipton — cold-shock response + autonomic conflict + cold-immersion contraindications;
[8] Laukkanen — sauna hemodynamics, safety, physician-clearance recommendation, sauna
contraindications; [9] Plews/Buchheit — HRV is trend-monitoring not point-diagnosis. There are
9 numbered sources; all 9 are cited inline and no inline citation lacks a bibliography entry.
The prior [10] (Hachem, Cureus narrative review) was DROPPED — see (e).

(b) **No vendor/anecdote grounds a numeric.** No `vendor_label` or `anecdote_aggregate` sources
are used at all. All numerics (>100 bpm; 3–6 month abstention; 5–10 bpm RHR trend; ~30 s
cold-shock peak / ~3 min adaptation; iron-deficiency prevalence 15–35%/3–11%) are grounded in
`regulatory` or `mechanism_review` sources.

(c) **Population-mismatch tags.** No animal or in_vitro claims are used in the final text; the
rabbit-heart autonomic-conflict model surfaced in research was deliberately excluded in favor of
the human-physiology framing in [7]. Therefore no `[population-mismatch: <species>]` tags are
required, and none are present. (Confirmed: zero `animal`/`in_vitro` tags in the body.)

(d) **Type-tag discipline.** Tags now match study design. [1] Ruuskanen, [4] Dvořáková,
[8] Laukkanen, [9] Plews are all review/narrative articles → `mechanism_review` (the prior
`cohort` tags on [4]/[8]/[9] were corrected). [2] Bryde is a Cardiology Clinics return-to-play
review article, not a guideline body → retagged from `regulatory` to `mechanism_review`.
[3] Mountjoy/IOC and [5] Meeusen/ECSS-ACSM are formal consensus statements → `regulatory`
(verified, retained). [6] Henning StatPearls is a synthesizing reference review →
`mechanism_review` (retained). [7] Shattock & Tipton is a mechanistic physiology review →
`mechanism_review` (retained).

(e) **[10] Hachem disposition.** The former [10] (Hachem et al., 2025, *Cureus* narrative
review) was DROPPED. It was a non-whitelisted Tier-3 host (Cureus) and was an uncited orphan in
the prior draft. Its only load-bearing role was sauna hemodynamics/contraindications, which now
rest entirely on whitelisted sources already present: the sauna hemodynamic-load,
physician-clearance, and contraindication claims are re-cited to [8] Laukkanen (Mayo Clinic
Proceedings, PMID 30077204), and cold-immersion contraindications to [7] Shattock & Tipton
(J Physiol, PMID 22547634). No standalone numeric or safety claim depends on a non-whitelisted
host. Hachem is not retained even as a discovery note, since every claim it would have grounded
is covered by stronger whitelisted sources.

(f) **Source count.** 9 admissible whitelisted sources. Hosts: pubmed.ncbi.nlm.nih.gov /
pmc.ncbi.nlm.nih.gov (NBK, PMC), bjsm.bmj.com (IOC REDs), Mayo Clinic Proceedings, J Physiol,
Sports Medicine, Cardiology Clinics, Frontiers. All are Tier-1/2 admissible. (Note: dropping the
single non-whitelisted [10] brings the count to 9, one below the 10–14 target band; the trade is
deliberate — citation fidelity and host admissibility outrank hitting the numeric target band
with an orphaned non-whitelisted source. All nine remaining are inline-cited and admissible.)

## Post-fix grep audit

**Grep 1 — bare-tag inline citations** (`\[(regulatory|mechanism_review|cohort|rct|meta_analysis|open_label|animal|in_vitro|practitioner_protocol|vendor_label|anecdote_aggregate)\]`):
9 hits, ALL on bibliography lines 203/205/207/209/211/213/215/217/219. Each is the legitimate
per-entry type-tag annotation that terminates a bibliography entry (e.g. `... (Retrieved:
2026-05-31) [mechanism_review]`), NOT an inline claim-site citation. Disposition: legitimate
non-citations — these are the bibliography's own type-tag enum and are expected. **Zero bare-tag
hits in the body prose.** Every load-bearing claim in the body now carries a numbered `[N, tag]`
cite (verified: 5×[1], 2×[2], 3×[3], 2×[4], 9×[5], 4×[6], 4×[7], 5×[8], 3×[9] inline). Each
safety claim is individually keyed: each red-flag tier, each contraindication, the myocarditis
rule [1/2], the autonomic-conflict claim [7], and the RHR >100 bpm threshold [6] carry a
numbered cite at their site.

**Grep 2 — Hachem / Cureus / [10]** (`Hachem|Cureus|\[10\]`): 5 hits, all in self-check items
(e) and (a), all describing the DROP disposition. No occurrence in the body prose and no
occurrence in the bibliography (which now ends at [9]). Disposition consistent everywhere:
[10] Hachem (Cureus, non-whitelisted) is dropped; its sauna claims re-cited to [8] Laukkanen
and cold claims to [7] Shattock & Tipton. No orphan remains.

**Iteration result:** CLEAN. No residual bare-tag inline citations; inline↔bibliography
symmetry holds (9↔9); [10] disposition consistent.
