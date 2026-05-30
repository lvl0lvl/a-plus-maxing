# Section D — Overtraining, Monitoring, Population Modifiers & Pre-participation Safety

Goal-agnostic domain science for a personal-trainer specialist agent: the fatigue/monitoring/population-safety layer, with explicit ESTABLISHED-vs-PROVISIONAL flags and recognize-and-route boundaries. No claim is personalized; the specialist consumes this layer, it does not author it.

---

## 1. The Overtraining Continuum (FOR → NFOR → OTS)

The governing reference is the joint consensus statement of the European College of Sport Science (ECSS) and the American College of Sports Medicine (ACSM) [1, regulatory].

- **Functional overreaching (FOR):** intensified training causes a short-term performance decrement, but after adequate recovery performance **supercompensates** above baseline — the intended outcome of a planned overload block. ESTABLISHED concept [1, regulatory].
- **Non-functional overreaching (NFOR):** the training/recovery balance is not respected; the decrement persists for weeks-to-months with stagnation and psychological/neuroendocrine disturbance and **no performance gain**. NFOR shares clinical and biological markers with OTS [1, regulatory].
- **Overtraining syndrome (OTS):** **prolonged maladaptation** of the athlete plus multiple biological, neurochemical, and hormonal regulation mechanisms, recovery taking months or longer [1, regulatory].

**Critical epistemic flags:**
- The NFOR/OTS distinction is, per the consensus authors, **"very difficult"** and rests on **clinical outcome and exclusion diagnosis** — OTS is a **diagnosis of exclusion**, not positively confirmable, and **no single biomarker** meets criteria for a definitive diagnosis [1, regulatory]. PROVISIONAL / poorly operationalized. The agent treats "overtraining" as a hypothesis requiring exclusion of organic disease, infection, dietary deficiency (notably iron), and **low energy availability** (§2), and routes the exclusion work to a clinician.
- Stage thresholds are **not crisply defined**; the agent should resist labeling a trainee "overtrained," instead describing observable signs (unexplained performance decrement, persistent fatigue, mood disturbance, sleep disruption) and recommending load reduction + clinical exclusion [1, regulatory].

---

## 2. RED-S / REDs and the Female & Male Athlete Triad (recognize-and-route)

This domain **overlaps the nutritionist's territory**. The agent's role is to **recognize the low-energy-availability (LEA) signal and route** the energy-availability / disordered-eating question; it does not own ED management or RED-S treatment.

**Root cause (ESTABLISHED consensus):** Low energy availability — intake insufficient to cover exercise expenditure, leaving too little for normal physiological function — is the **root cause**, reported as established consensus across the IOC and Triad Coalition statements [2, regulatory; 3, regulatory; 4, regulatory].

- **2023 IOC REDs consensus** [2, regulatory]: reframes LEA as a **spectrum from adaptable to problematic** (moderated by individual factors), broadens outcomes (bone, endocrine, immune, cardiovascular, metabolic, hematological, psychological, plus performance), and explicitly notes **overlap between REDs and overtraining syndrome** — relevant to §1's exclusion logic. (Acronym changed RED-S → REDs.)
- **Female Athlete Triad** [3, regulatory]: (1) LEA ± disordered eating, (2) menstrual dysfunction, (3) low bone mineral density — LEA the driver; endpoints include clinical eating disorders, functional amenorrhea, osteoporosis.
- **Male Athlete Triad** [4, regulatory]: (1) energy deficiency/LEA ± disordered eating, (2) functional **hypothalamic hypogonadism**, (3) low BMD/osteoporosis ± bone stress injury — most documented in adolescent/young-adult endurance and weight-class males. The agent must **not** treat LEA risk as female-only.

**Route trigger:** signs of LEA (unexplained performance plateau/decline, recurrent bone stress injuries, menstrual disturbance in females, low libido / hypogonadism in males, rapid unintended weight loss, fatigue not explained by load) → recognize-and-route to the nutritionist and/or a clinician; do **not** prescribe an energy-deficit program into that picture.

---

## 3. Monitoring Tools and Their Validity

### 3.1 Session-RPE / training load — relatively well-supported
Session-RPE (sRPE = perceived exertion on a modified CR-10 scale × session duration) is a validated, low-cost internal-load measure. A review summarizing ~36 validation studies reports good validity, reliability, and internal consistency across sports and across men and women of different ages, with sRPE correlating strongly with HR-based TRIMP indices [5, mechanism_review]. ESTABLISHED as a practical internal-load tool, with the caveat that it is **subjective**; authors recommend combining it with objective markers [5, mechanism_review].

### 3.2 HRV-guided training — modest and CONTESTED, NOT settled
The single most important "do not oversell" flag in the section.

- A 2021 systematic review with meta-analysis (8 studies, 198 participants) found HRV-guided endurance training gave a **medium effect on submaximal physiological parameters (g ≈ 0.30, p = 0.028)** but only **small, non-significant effects on performance (g ≈ 0.08, p = 0.60)** and **VO₂peak (g ≈ 0.17, p = 0.13)** versus predefined training; a possible advantage was **fewer non-responders** [6, meta_analysis].
- A separate methodological systematic review with meta-analysis concurred: HRV-guided training was superior for vagal-related HRV indices but showed **consistently small, non-significant** advantages for aerobic capacity and endurance performance [7, meta_analysis].

PROVISIONAL / CONTESTED: present HRV-guided autoregulation as **plausibly-helpful-but-modest**, performance benefit **not statistically established** — not a proven optimizer. Most evidence is in trained endurance athletes — **population-mismatch flag** for novices/general trainees, in whom it is largely unstudied (no extrapolation without flag).

### 3.3 Subjective wellness vs objective measures
Self-report wellness/readiness questionnaires (fatigue, sleep, soreness, stress, mood) are inexpensive and respond to load, but the supporting literature is largely observational/practitioner-level; treat them as **trend signals**, not diagnostic instruments [1, regulatory; 5, mechanism_review]. ESTABLISHED only as low-cost trends; PROVISIONAL as anything decision-grade in isolation.

### 3.4 Wearable "recovery"/"readiness" composite scores — non-validated composites
A 2025 evaluation catalogued **14 composite health scores across 10 manufacturers** (Fitbit Daily Readiness, Garmin Body Battery/Training Readiness, Oura Readiness/Resilience, WHOOP Recovery/Strain/Stress, Polar Nightly Recharge, Samsung Energy Score, Suunto Body Resources, Ultrahuman Dynamic Recovery, Coros) and concluded the **proprietary algorithms are undisclosed "black boxes"** whose validity, transparency, and physiological relevance **remain unclear and cannot be independently replicated** [8, mechanism_review]. The **underlying inputs** (resting heart rate, HRV) are individually evidence-supported, but the **derived composites are not** — cited examples show a device recovery score failing to track perceived recovery even where its HRV did [8, mechanism_review].

ESTABLISHED: RHR and HRV as raw inputs. PROVISIONAL/UNVALIDATED: the branded composite scores. The agent should treat them as **non-validated heuristics**, prefer raw metrics plus subjective trend, and never present a wearable readiness number as clinical or definitively-actionable.

---

## 4. Detraining / Deconditioning Physiology and the Resumption Risk Window

**Detraining time course (ESTABLISHED):** Mujika & Padilla's two-part review is canonical [9, mechanism_review; 10, mechanism_review].
- Short-term (<4 wk): VO₂max falls rapidly in highly trained athletes, driven largely by **reduced blood/plasma volume** (~4–6% loss within ~2–3 weeks) [9, mechanism_review].
- Long-term (>4 wk): progressive VO₂max decline (~10% by ~5 weeks, larger over months in the reviewed athlete data) [10, mechanism_review]. **Strength is far better retained** — force production declines slowly and often stays above untrained levels for weeks-to-months [10, mechanism_review]. Population note: magnitudes are from **highly-trained athlete** cohorts; absolute numbers do not transfer to recreational trainees (no extrapolation without flag).

**The elevated-risk resumption window (ESTABLISHED hazard):** When a deconditioned person resumes intense — especially unaccustomed **eccentric** — training, rapid early gains coincide with heightened susceptibility to muscle damage and **exertional rhabdomyolysis (ERM)**. The Sports Medicine ERM review identifies **unaccustomed exercise as the primary determinant**, with high-force eccentric (lengthening) contractions causing the greatest fiber damage, and documents clustering in **fitness novices, returning exercisers, and military recruits / new high-intensity-class participants**; heat, dehydration, certain medications, and genetic predisposition are additive [11, mechanism_review]. ERM can progress to myoglobinuria and **acute kidney injury** [11, mechanism_review].

**Agent implication:** for a returning/deconditioned trainee, apply conservative initial load and **gradual progression of eccentric volume**; warning signs (severe disproportionate soreness, dark urine, marked weakness/swelling) are a **route-to-emergency-care** signal, not a coaching adjustment.

---

## 5. Older / Masters Trainee Considerations

**Sarcopenia & anabolic resistance (ESTABLISHED):** aging muscle shows **anabolic resistance** — a blunted muscle-protein-synthesis response to a given protein dose — so older adults need **more** protein than the 0.8 g/kg/d RDA for equivalent anabolic signaling [12, regulatory; 13, regulatory].
- **PROT-AGE Study Group:** ≥**1.0–1.2 g/kg/d** for healthy older adults (>65 y), rising to **1.2–1.5 g/kg/d** with acute/chronic illness [12, regulatory].
- **ESPEN Expert Group:** converges on the same range and emphasizes protein **paired with resistance/physical activity**, which raises muscle sensitivity to dietary protein [13, regulatory]. (Overlaps the nutritionist's domain — the trainer recognizes the higher-protein need and routes the prescription detail.)

**Resistance training is the primary countermeasure (ESTABLISHED):** the most effective single intervention for muscle strength/mass, gait speed, and function in older adults; protein + resistance training outperform either alone [12, regulatory; 13, regulatory].

**Recovery in older adults (PROVISIONAL — magnitude uncertain):** A 2023 systematic scoping review found the evidence **variable and inconsistent**: in **men**, older males may sustain **less** exercise-induced muscle damage than younger men (4/5 studies showed smaller strength reductions) yet recovery was often **prolonged and incomplete even at 240 h**; sparse data hinted older **women** may recover **more slowly** (hypothesized post-menopausal estrogen effect) [14, mechanism_review]. The review flags protocol heterogeneity, eccentric-protocol reliance, and sparse female data [14, mechanism_review]. The **commonly-asserted "masters athletes recover much slower" claim is only weakly/inconsistently supported** for strength loss — the agent should treat recovery individualization and conservative inter-session spacing as prudent while flagging the deficit **magnitude as not well-established**. Tendon stiffness / slower connective-tissue adaptation with age inform conservative progression but are not quantified here from a verified primary (see Self-check).

---

## 6. Pre-participation Safety Screening Before (Re)starting Vigorous Exercise

### 6.1 ACSM pre-participation screening algorithm (ESTABLISHED consensus)
The 2015 update (Riebe et al.) is the current ACSM logic [15, regulatory]. Referral decisions hinge on **three variables**:
1. **Current physical-activity level** (does the person already exercise regularly?),
2. **Presence of known cardiovascular, metabolic, or renal disease (CMRD) and/or signs/symptoms** suggestive of such disease,
3. **Desired exercise intensity** (light/moderate vs vigorous).

Crucially, ACSM **deliberately moved away from routine medical clearance for everyone** and **de-emphasized routine CV risk-factor profiling** as a screening gate, because the prior model generated excessive physician referrals that became a **barrier to becoming active**; the rationale is that exercise is safe for most people and exercise-related cardiac events are frequently preceded by warning signs/symptoms [15, regulatory].

**Triggers for medical evaluation BEFORE vigorous exercise (synthesizing [15, regulatory]):**
- **Known CMRD** — even if currently active, medical guidance is advised before progressing, especially to vigorous intensity.
- **Signs/symptoms** suggestive of CMRD (chest discomfort/angina-type symptoms, unexplained dyspnea, syncope/dizziness, palpitations, ankle edema, claudication) — discontinue/avoid exercise and seek evaluation **regardless** of current activity.
- **Inactive + known CMRD** wishing to begin → medical clearance recommended.
- **Active, asymptomatic, no known CMRD** → may continue and progress without routine clearance.

### 6.2 AHA / ACC pre-exercise evaluation (ESTABLISHED, concordant)
Concordant: asymptomatic individuals **without** known CMRD — active or inactive — may begin/continue and **progress gradually without mandatory clearance**, provided they **remain asymptomatic**; symptom onset is the trigger to stop and seek evaluation [16, regulatory]. The shared AHA/ACSM philosophy is to **identify symptomatic / known-disease individuals**, not gate everyone behind a physician visit [16, regulatory].

### 6.3 PAR-Q+ self-screen (ESTABLISHED validated self-screen)
The **PAR-Q+** (with online ePARmed-X+) is the evidence-based successor to the original PAR-Q, built from systematic reviews of exercise-related risk and designed to **reduce barriers** (including for stable chronic conditions) while flagging those needing further evaluation [17, regulatory]. It is a **self-administered first-pass**; "yes" answers route to ePARmed-X+ / a qualified professional or physician. The agent can reason over PAR-Q+-style items as structured intake, but a positive flag is a **route signal, not a clearance**.

---

## 7. The Coaching ↔ Clinical Boundary (the core route-fidelity rule)

The agent operates in the **coaching layer** and recognizes-and-routes the **clinical layer**:

- **Coaching (in-scope):** load/volume/intensity programming, exercise selection and technique cueing, progressive overload and deload planning, autoregulation via sRPE / subjective wellness / (cautiously) HRV trends, conservative re-entry programming for deconditioned trainees, protein-and-resistance-training guidance for masters trainees (with nutritionist coordination).
- **Clinical (route out — NOT in-scope):** diagnosing injury/disease; diagnosing OTS/NFOR (a diagnosis of **exclusion** requiring clinical workup, §1); prescribing rehab for a **diagnosed** condition; **medical clearance after a cardiac/serious-illness event**; eating-disorder / RED-S treatment (route to nutritionist + clinician, §2); any acute red flag (suspected rhabdomyolysis, exertional chest pain/syncope, dark urine) → **urgent/emergency care**.

The §6 screening logic is the formal hinge: when ACSM/AHA criteria or a PAR-Q+ flag warrant medical evaluation before vigorous exercise, the agent **defers programming until clearance** rather than coaching through an un-evaluated risk.

---

## Bibliography

1. Meeusen R, Duclos M, Foster C, Fry A, Gleeson M, Nieman D, Raglin J, Rietjens G, Steinacker J, Urhausen A. Prevention, diagnosis, and treatment of the overtraining syndrome: joint consensus statement of the European College of Sport Science and the American College of Sports Medicine. *Med Sci Sports Exerc.* 2013;45(1):186–205. PMID 23247672. DOI 10.1249/MSS.0b013e318279a10a. [regulatory — consensus statement]
2. Mountjoy M, Ackerman KE, Bailey DM, Burke LM, Constantini N, Hackney AC, Heikura IA, Melin A, Pensgaard AM, Stellingwerff T, Sundgot-Borgen JK, Torstveit MK, Jacobsen AU, Verhagen E, Budgett R, Engebretsen L, Erdener U. 2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs). *Br J Sports Med.* 2023;57(17):1073–1097. PMID 37752011. DOI 10.1136/bjsports-2023-106994. [regulatory — consensus statement]
3. De Souza MJ, Nattiv A, Joy E, et al. 2014 Female Athlete Triad Coalition Consensus Statement on Treatment and Return to Play of the Female Athlete Triad. *Br J Sports Med.* 2014;48(4):289. PMID 24463911 (also indexed PMID 25014387 for the co-published version). DOI 10.1136/bjsports-2013-093218. [regulatory — consensus statement]
4. Nattiv A, De Souza MJ, Koltun KJ, et al. The Male Athlete Triad — A Consensus Statement From the Female and Male Athlete Triad Coalition Part 1: Definition and Scientific Basis. *Clin J Sport Med.* 2021;31(4):335–348. DOI 10.1097/JSM.0000000000000946. (PMID not independently re-verified in this session — cited bibliographically; see Self-check.) [regulatory — consensus statement]
5. Haddad M, Stylianides G, Djaoui L, Dellal A, Chamari K. Session-RPE method for training load monitoring: validity, ecological usefulness, and influencing factors. *Front Neurosci.* 2017;11:612. PMID 29163016. DOI 10.3389/fnins.2017.00612. [mechanism_review]
6. Düking P, Zinner C, Trabelsi K, Reed JL, Holmberg HC, Kunz P, Sperlich B. Monitoring and adapting endurance training on the basis of heart rate variability monitored by wearable technologies: a systematic review with meta-analysis. *J Sci Med Sport.* 2021;24(11):1180–1192. PMID 34489178. DOI 10.1016/j.jsams.2021.04.012. [meta_analysis]
7. Granero-Gallegos A, González-Quílez A, Plews D, Carrasco-Poyatos M. (HRV-guided training meta-analysis) — Heart Rate Variability-Guided Training for Enhancing Cardiac-Vagal Modulation, Aerobic Fitness, and Endurance Performance: A Methodological Systematic Review with Meta-Analysis. *Int J Environ Res Public Health.* 2020 (PMC8507742). DOI 10.3390/ijerph17217999. (Author order/identifiers reconstructed from PMC record; see Self-check.) [meta_analysis]
8. Doherty C, Baldwin M, Lambe R, Burke D, Altini M. Readiness, recovery, and strain: an evaluation of composite health scores in consumer wearables. *Transl Exerc Biomed.* 2025;2(2):128–144. DOI 10.1515/teb-2025-0001. [mechanism_review]
9. Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations. Part I: short term insufficient training stimulus. *Sports Med.* 2000;30(2):79–87. PMID 10966148. DOI 10.2165/00007256-200030020-00002. [mechanism_review]
10. Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations. Part II: long term insufficient training stimulus. *Sports Med.* 2000;30(3):145–154. PMID 10999420. DOI 10.2165/00007256-200030030-00001. (Page/DOI for Part II reconstructed from indexing; PMID verified.) [mechanism_review]
11. Rawson ES, Clarkson PM, Tarnopolsky MA. Perspectives on exertional rhabdomyolysis. *Sports Med.* 2017;47(Suppl 1):33–49. PMID 28332112. DOI 10.1007/s40279-017-0689-z. [mechanism_review]
12. Bauer J, Biolo G, Cederholm T, Cesari M, Cruz-Jentoft AJ, Morley JE, Phillips S, Sieber C, Stehle P, Teta D, Visvanathan R, Volpi E, Boirie Y. Evidence-based recommendations for optimal dietary protein intake in older people: a position paper from the PROT-AGE Study Group. *J Am Med Dir Assoc.* 2013;14(8):542–559. PMID 23867520. DOI 10.1016/j.jamda.2013.05.021. [regulatory — position paper]
13. Deutz NE, Bauer JM, Barazzoni R, Biolo G, Boirie Y, Bosy-Westphal A, Cederholm T, Cruz-Jentoft A, Krznariç Z, Nair KS, Singer P, Teta D, Tipton K, Calder PC. Protein intake and exercise for optimal muscle function with aging: recommendations from the ESPEN Expert Group. *Clin Nutr.* 2014;33(6):929–936. PMID 24814383. DOI 10.1016/j.clnu.2014.04.007. (PMID/DOI reconstructed from journal record; see Self-check.) [regulatory — expert-group recommendations]
14. Hayes EJ, Stevenson E, Sayer AA, Granic A, Hurst C. Recovery from resistance exercise in older adults: a systematic scoping review. *Sports Med Open.* 2023;9(1):51. PMID 37395837. DOI 10.1186/s40798-023-00597-1. [mechanism_review]
15. Riebe D, Franklin BA, Thompson PD, Garber CE, Whitfield GP, Magal M, Pescatello LS. Updating ACSM's recommendations for exercise preparticipation health screening. *Med Sci Sports Exerc.* 2015;47(11):2473–2479. PMID 26473759. DOI 10.1249/MSS.0000000000000664. [regulatory — position update]
16. American Heart Association scientific statement on exercise standards / preparticipation evaluation for asymptomatic adults (AHA/ACC-aligned guidance; e.g., Fletcher et al., Exercise Standards for Testing and Training, *Circulation*). Cited bibliographically — exact statement identifiers not re-verified this session; see Self-check. [regulatory — scientific statement]
17. Warburton DER, Jamnik VK, Bredin SSD, Gledhill N. The Physical Activity Readiness Questionnaire for Everyone (PAR-Q+) and electronic Physical Activity Readiness Medical Examination (ePARmed-X+). *Health Fit J Can.* 2011;4(2):3–17. (Validated self-screen tool; journal is the official PAR-Q+ publication venue. Identifiers per eparmedx.com / journal record; see Self-check.) [regulatory — validated screening instrument]

---

## Self-check

**Claims NOT fully ground to an independently re-verified whitelisted primary this session (honest flags — none fabricated; each cited bibliographically with uncertainty stated):**

- **[4] Male Athlete Triad (Nattiv 2021, Clin J Sport Med):** journal, year, content confirmed via search; **PMID not independently pulled** (DOI 10.1097/JSM.0000000000000946 from publisher record). Confidence: HIGH content, MEDIUM identifier.
- **[7] Second HRV meta-analysis (PMC8507742):** PMC record and verdict (small, non-significant performance/VO₂ effect; vagal-index benefit) confirmed; **author order and DOI reconstructed**, not line-verified. Directional conclusion corroborated by fully-verified [6].
- **[10] Mujika & Padilla Part II:** **PMID 10999420 verified**; **volume/page/DOI reconstructed** from indexing. Numeric trajectory from a verified WebFetch summary of the review series.
- **[13] ESPEN Expert Group (Deutz 2014, Clin Nutr):** title, body, year, journal confirmed; **PMID/DOI reconstructed** from journal record, not line-verified.
- **[16] AHA/ACC pre-exercise evaluation:** position (asymptomatic, no-CMRD adults may begin/progress without mandatory clearance; symptoms are the trigger) **confirmed** and concordant with [15]; **no single canonical AHA statement locked with verified PMID/DOI** — cited as institutional statement, no fabricated identifier. Confidence: HIGH position, LOW citation handle.
- **[17] PAR-Q+ (Warburton 2011, Health Fit J Can):** existence, role as validated PAR-Q successor, journal/volume confirmed; journal off Tier-1 host list but the **instrument is the validated screen** (Tier-2 by function), tagged `regulatory`. No fabricated identifier.
- **Tendon stiffness / connective-tissue aging (§5):** stated as established background physiology, **not grounded to a specific verified primary** here — flagged for the design layer to source if load-bearing.

**Evidence-strength summary:**

- **ESTABLISHED (high-confidence, verified primaries):** the FOR/NFOR/OTS continuum vocabulary and OTS-as-diagnosis-of-exclusion [1]; LEA as the root cause of REDs/Triad and the male triad's existence [2,3,4]; sRPE validity as an internal-load tool [5]; detraining time course (rapid VO₂max loss, strength better retained) [9,10]; unaccustomed/eccentric exercise + deconditioning as the dominant ERM risk window [11]; anabolic resistance and the elevated older-adult protein target (1.0–1.2, up to 1.5 g/kg/d) with resistance training as primary countermeasure [12,13]; ACSM 2015 screening logic and its deliberate move away from universal medical clearance [15]; AHA-concordant asymptomatic-adult guidance [16]; PAR-Q+ as a validated self-screen [17].
- **PROVISIONAL / CONTESTED (explicitly flagged for the agent):** OTS operationalization — poorly defined, no confirmatory biomarker [1]; **HRV-guided-training performance benefit — modest and not statistically established** [6,7]; **wearable composite readiness/recovery scores — non-validated, undisclosed black-box composites** (raw RHR/HRV inputs are the only validated layer) [8]; **magnitude of masters-athlete recovery deficit — inconsistent and population/sex-dependent** [14].
- **HALT-risk note:** No fabricated PMIDs/DOIs. The principal residual citation-fidelity risk is concentrated in [16] (no single locked AHA statement identifier) and the reconstructed-identifier items [7], [10], [13], [17] — all flagged above rather than asserted as verified. Every numeric claim is attributed to a source whose content was retrieved this session; no number is attached to a non-supporting source.
