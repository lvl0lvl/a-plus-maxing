# Section C — Return-to-Training After Injury/Illness & MSK Rehabilitation (SAFETY-WEIGHTED)

Domain-science grounding for a `personal-trainer` medical-specialist agent. This section is the SAFETY-CRITICAL one: return-to-training carries real harm potential (re-injury, contraindicated loading, exertional cardiac events). It maps the boundary structure the agent must respect — what constrains loading, what is established vs contested, and which presentations must ROUTE OUT of coaching to urgent medical evaluation rather than to a progression plan. The agent consumes this; it does not author rehab plans for any operator.

A recurring epistemic theme: tissue-healing timeframes are **RANGES, not guarantees**, and they are modifiers of, not substitutes for, criteria-based readiness. The agent should treat any "X weeks and you're cleared" framing as a category error.

---

## C1. Tissue-healing timelines that CONSTRAIN loading (RANGES, not guarantees)

### C1.1 Muscle strain — grading drives prognosis
The British Athletics Muscle Injury Classification (BAMIC) grades muscle injury 0–4 from MRI features, sub-classified a/b/c by anatomical site (myofascial, musculotendinous, intratendinous), and the intratendinous ("c") injuries carry the worst prognosis [1, practitioner_protocol]. In elite-athlete hamstring cohorts, time to return to full training scaled with grade — broadly on the order of ~2 weeks for the mildest classes rising to ~6+ weeks for grade-2c — and these are **observational ranges in elite athletes, not guaranteed timelines** [1, cohort]. (ESTABLISHED that grade/site predict prognosis; PROVISIONAL that any specific day-count generalises to a recreational trainee — population-mismatch flag: BAMIC was derived in elite track-and-field/football, NOT recreational lifters.)

### C1.2 Tendon — the pathology continuum and the mechanotransduction timeline
Cook & Purdam's continuum model frames load-induced tendinopathy as a progression: **reactive tendinopathy → tendon dysrepair → degenerative tendinopathy**, with the early reactive stage a non-inflammatory proliferative response to acute overload/compression, and the model assigns load strategy by stage [2, mechanism_review]. This is the dominant clinical staging framework but remains a *model*, not a validated diagnostic test (PROVISIONAL as a precise stager; ESTABLISHED as the organising concept).

The collagen-turnover timeline that constrains how often a tendon can be loaded: in **human patellar tendon** (Miller et al.), exercise raised fractional collagen synthetic rate, detectable by 6 h, peaking ~24 h post-exercise and **still elevated at 72 h** [3, mechanism_review — human in-vivo]. CRITICAL CAVEAT carried from the source itself: this measured *synthesis rate only, not net accretion* — the authors state net protein balance was not measured. So the agent must NOT translate "synthesis elevated to 72 h" into "tendon is stronger after 3 days"; early net collagen balance can be neutral or negative. This timeline supports the rationale for spacing heavy tendon-loading sessions ~48–72 h apart, but the strength gain is a slow remodelling process over months, not days (no extrapolation beyond the synthesis-rate finding).

### C1.3 Bone stress injury (BSI) — weeks-to-months, MRI grade and site set the range
A systematic review and meta-analysis (Hoenig et al.) found mean return-to-sport scaling cleanly with MRI grade: **~41.7 days (grade 1), ~70.1 (grade 2), ~84.3 (grade 3), ~98.5 days (grade 4)** — i.e., roughly **6 to 14 weeks**, widening further for high-risk anatomical sites [4, meta_analysis]. High-risk sites (e.g., anterior tibial cortex, femoral neck, navicular, base of 2nd metatarsal, tarsal) demand markedly more conservative management — and are *referral* situations, not self-progression scenarios (see C5) — because they are prone to non-union/progression to complete fracture; this site distinction is ESTABLISHED clinical practice even though the meta-analytic day-counts are means with wide confidence intervals (RANGES). Established loading principle: restore **volume before intensity**, because impact intensity drives bone-stress risk disproportionately, and progress only from a pain-free baseline (commonly several pain-free days in daily activities before graded loading).

### C1.4 Ligament / post-surgical (ACL) — time is necessary but NOT sufficient
After ACL reconstruction, the Delaware-Oslo cohort (Grindem et al.) found reinjury rate **39.5% for return before 9 months vs 19.4% at ≥9 months**, that **each month of delay up to 9 months cut reinjury risk ~51%** (plateauing after 9 months), and that **quadriceps strength symmetry <90% carried 33.3% reinjury vs 12.5% at ≥90%** [5, cohort]. The load-bearing inference for the agent: 9 months is a *floor*, and time alone does not clear an athlete — functional/strength criteria do (criteria-based, not time-based; see C4). ESTABLISHED.

---

## C2. Tendinopathy rehab evidence — what's established vs contested

### C2.1 Progressive mechanotherapy is the backbone (ESTABLISHED)
Tendon adapts to graded mechanical load via increased collagen synthesis/turnover and improved mechanical properties [3, mechanism_review — human]; progressive loading (not rest) is the established core of tendinopathy management. The *flavour* of loading is where the contest lives.

### C2.2 Eccentric (Alfredson) vs Heavy Slow Resistance (HSR) — broadly equivalent
The original Alfredson protocol (3×15 eccentric heel-drops, straight + bent knee, twice daily, 7 d/wk, 12 wk) established eccentric loading for midportion Achilles tendinopathy [6, rct]. The Beyer et al. RCT (n=58, chronic midportion Achilles) directly compared 12-week eccentric vs HSR and found **clinical and structural outcomes did not differ at 52 weeks**, with HSR showing higher compliance (92% vs 78%) and greater 12-week satisfaction [6, rct]. Inference: eccentric-vs-HSR superiority is **CONTESTED/UNRESOLVED — they are broadly equivalent**, so the agent should treat protocol choice as a tolerance/adherence decision, not an efficacy hierarchy. (Single-RCT evidence for direct head-to-head; flag as not yet meta-analytically settled.)

### C2.3 Isometrics for pain — CONTESTED (the headline analgesia claim did not replicate)
The widely-cited claim originates from Rio et al.'s **n=6** crossover in patellar tendinopathy reporting large immediate isometric analgesia (single-leg decline-squat pain 7.0±2.0 → 0.17±0.41 after isometrics, vs a smaller drop after isotonics) [7, rct — very small n]. This **did NOT robustly replicate**: a systematic review and meta-analysis of randomised trials (Clifford et al.) concluded isometric exercise is **NOT superior to isotonic exercise** for chronic tendinopathy and **no more effective than ice** short-term for rotator-cuff tendinopathy, with a **variable ("responder/non-responder") response within and across populations** [8, meta_analysis]. So: isometric analgesia for tendinopathy is **CONTESTED** — the agent must not present it as a reliable pain-relief lever; it may be tried but with explicitly uncertain individual response. (This is exactly the established-vs-provisional flag the brief demands.)

---

## C3. Load management & re-injury — ACWR is NOT settled injury-prevention science

This is a designated HALT-risk claim: the agent must NOT present the acute:chronic workload ratio (ACWR) as validated injury-prevention science.

**Original hypothesis (Gabbett).** Gabbett's "training–injury prevention paradox" popularised ACWR, proposing a low-risk "sweet spot" of ~0.8–1.3 and ~2–4× injury risk when the weekly (acute) load spikes to ≥1.5× the chronic baseline, arguing high *chronic* loads are protective if reached gradually [9, mechanism_review]. This narrative paradigm paper (a synthesis of prior cohort data, not itself a primary cohort) drove near-universal adoption in athletic monitoring c.2016–2019.

**Strong methodological critique (Impellizzeri, Lolli, et al., ~2019–2021) — CONTESTED→largely repudiated.** Subsequent work showed the apparent ACWR–injury association is substantially a **statistical artifact**: the ratio rescales the acute-load numerator, magnifying its apparent effect and shrinking its variance **without adding predictive value**; "contrived" fixed or randomly-generated chronic-load denominators reproduced similar inflated odds ratios, and predictive performance was negligible (c-statistic ≈0.57 — barely above chance) [10, meta_analysis]. This methodological re-analysis's explicit conclusion was to **dismiss ACWR and its underlying theory** [10]. Ratio-based indices are also criticised for spurious correlation and arbitrary time-window choices [10].

**Agent rule:** report BOTH the original hypothesis AND the repudiation; treat "keep ACWR in 0.8–1.3" as historical/contested, not as a safety guarantee. The *general* principle that abrupt large load spikes after a layoff are risky is plausible and consistent with deconditioning/rhabdo risk (C6), but it does NOT license presenting the ACWR number as evidence-based injury prevention. ESTABLISHED that ACWR-as-predictor is methodologically discredited; PROVISIONAL that any specific load-progression cap prevents injury.

---

## C4. Return-to-sport / return-to-play (RTS/RTP) decision frameworks — criteria-based, shared

**Criteria-based, not purely time-based (ESTABLISHED).** The 2016 Bern consensus (Ardern et al., First World Congress in Sports Physical Therapy) frames RTS as a **continuum** paralleling rehab — not a single end-point decision — made via **shared decision-making** among clinician, athlete and coach, and supported by the **StARRT framework** (Strategic Assessment of Risk and Risk Tolerance): clear RTS only when assessed risk falls below the acceptable risk-tolerance threshold, integrated through a biopsychosocial lens [11, regulatory]. The ACL data (C1.4) operationalise this: passing a battery of strength/function criteria, not merely elapsed time, is what reduces reinjury [5, cohort]. **Agent rule:** progress on demonstrated criteria (pain-free loading, strength symmetry, functional tests), with time-since-injury as a *floor* not a *trigger*; final RTS/RTP clearance for a managed injury is a clinician-shared decision, not an autonomous coaching call.

---

## C5. Musculoskeletal "red flags" — refer, do NOT progress load

Established clinical practice (spinal/MSK red-flag literature, a review of current clinical guidelines) routes the following AWAY from load progression and TO medical referral [12, regulatory]:

- **Cauda equina features** — saddle (perineal) anaesthesia, new bladder/bowel dysfunction (retention/incontinence), bilateral sciatica or bilateral leg weakness → **EMERGENCY referral** (surgical timeline).
- **Suspected fracture / high-risk bone stress injury** — significant trauma mechanism, focal bony tenderness, high-risk BSI site (C1.3) → imaging/referral, NOT loading.
- **Progressive neurological deficit** — worsening weakness, numbness, or reflex change → referral.
- **Possible malignancy/infection (systemic features)** — history of cancer, unexplained weight loss, fever, unrelenting/progressive pain, night pain especially with other features → referral. (Note from source: *isolated* night pain or age alone is a weak/false-positive-prone flag; it is the *cluster* that matters [12].)

**Agent rule:** any of these short-circuits the coaching workflow to "stop progressing, seek medical assessment." These are ESTABLISHED referral triggers.

---

## C6. EXERTIONAL RED FLAGS — STOP exercise, urgent medical evaluation (ESTABLISHED, safety-critical)

These are the highest-stakes items in this section. The agent's correct action is to STOP exercise and route to emergency/clinician — NOT to deload, substitute exercises, or "monitor." Drawn from sports-cardiology guidance [13, regulatory] and COVID/post-illness pathways [14,15, regulatory]:

- **Exertional chest pain/pressure or tightness** — possible ischaemia, anomalous coronary artery, myocarditis, aortic pathology → STOP, urgent evaluation [13].
- **Syncope or near-syncope on exertion** — a sentinel symptom for malignant arrhythmia / structural disease; exertional (vs post-exertional/vasovagal) syncope is especially concerning → STOP, urgent cardiology evaluation [13].
- **Disproportionate dyspnea** (breathlessness out of proportion to effort) → evaluation [13,14].
- **Palpitations** (especially sustained/irregular with exertion) → evaluation [13,14].
- The cardiac "triad" workup these symptoms trigger is ECG + cardiac troponin + echocardiogram, by a clinician [14].

**Exertional rhabdomyolysis (ER) warning cluster** — the agent must recognise this in exactly the population it will most often serve (deconditioned individuals doing unaccustomed, high-volume **eccentric** work): **severe muscle pain beyond normal DOMS + marked swelling + dark/tea-/cola-coloured urine (myoglobinuria) + disproportionate weakness** [16, mechanism_review]. Eccentric and unaccustomed/high-repetition exercise, return after a layoff, heat, and dehydration are recognised precipitants; ER is confirmed by markedly elevated creatine kinase (the hallmark, classically ≥5× upper limit of normal) and myoglobinuria, and risks acute kidney injury [16, mechanism_review]. **Agent rule:** dark urine + severe post-exercise muscle pain/swelling = **STOP, urgent medical evaluation/ED** (IV-fluid territory), never "push through" or "more protein/foam-rolling." ESTABLISHED, safety-critical.

---

## C7. Return-to-exercise AFTER ILLNESS — the MYOCARDITIS contraindication (ESTABLISHED, load-bearing)

**Acute myocarditis is a contraindication to exercise (ESTABLISHED).** Guideline-level consensus is that individuals with myocarditis (any evidence of active myocardial involvement, *regardless of LV systolic function*) should **abstain from exercise during the acute phase**, conventionally **~3–6 months**, and return only after **cardiology clearance** [13,14,15, regulatory]. Clearance conditions in the consensus pathways: normalised systolic function, normalised cardiac injury biomarkers, and absence of relevant arrhythmias on Holter and exercise testing (CMR/echo + 24-h ECG + exercise stress test before resuming strenuous exercise) [13,14]. Rationale stated by the guidelines: exercise during active myocardial inflammation can worsen the inflammatory response with potentially fatal arrhythmic consequences [14]. The 2022 ACC pathway notes evolving evidence may allow *reassessment* of inflammation resolution somewhat earlier (no sooner than ~1 month) but does not abolish the abstain-then-clear structure [14]. **Agent rule:** confirmed/suspected acute myocarditis ⇒ exercise OFF, return is a cardiology decision — this is non-negotiable and must never be overridden by a training goal.

**Post-COVID / post-viral graded return-to-activity (GRTP) (ESTABLISHED framework).** Elliott et al.'s BJSM graduated-return-to-play guidance structures resumption after COVID-19 as **staged progression** with a minimum rest period and symptom-free interval before starting, advancing one stage at a time only if asymptomatic, and **dropping back a stage (≥24 h symptom-free) if symptoms recur** [15, regulatory]. Crucially, **development of cardiopulmonary red-flag symptoms during GRTP — chest pain/tightness, palpitations, lightheadedness/syncope, disproportionate breathlessness — halts progression and triggers cardiac evaluation** (links directly to C6) [14,15]. This graded, symptom-gated structure generalises as the agent's post-illness return template: rest → asymptomatic baseline → stepwise reintroduction → drop back on any symptom → escalate on any red flag. (PROVISIONAL on exact day-counts for a recreational trainee — the protocols were framed for athletes; the *structure* is the ESTABLISHED, transferable part.)

---

## C8. Composing the boundaries — route-fidelity for the agent

The sections above describe three qualitatively different boundary types the agent must keep separate, because they have different correct *routes*:

1. **STOP-and-escalate (emergency/urgent clinician).** The exertional cardiac red flags (C6: chest pain/pressure, exertional syncope/near-syncope, disproportionate dyspnea, palpitations), the exertional-rhabdomyolysis cluster (C6: dark urine + severe pain + swelling), and the emergency MSK red flags (C5: cauda equina) belong here. The agent must NOT deload, substitute, or "monitor over the next session" — these route OUT of the coaching loop entirely. Misclassifying any of these as a programming problem is the most dangerous failure mode in this domain.

2. **Refer-then-defer (clinician decides return).** Acute/suspected myocarditis (C7), high-risk-site BSI (C1.3), suspected fracture, progressive neurological deficit, and possible malignancy/infection (C5) are contraindications to *autonomous* load progression. The agent surfaces the concern and hands the return decision to a clinician; it does not author the clearance. Final RTS/RTP clearance for a managed serious injury (e.g., post-ACL, post-myocarditis) is likewise a shared clinician decision (C4), not an agent call.

3. **Coach-with-constraints (the agent's actual operating zone).** Established tendinopathy/strain/BSI rehabilitation by progressive, criteria-gated loading (C1–C2), graded symptom-gated return after uncomplicated illness (C7), and load progression that respects tissue-healing ranges and avoids abrupt post-layoff spikes (C3, with the caveat that the *specific* ACWR number is not a validated safety device). This is where the agent does its work — but always with the two prior gates upstream of it.

The single most important cross-cutting rule: **time-since-injury is a floor, not a clearance trigger.** Criteria — pain-free loading, strength symmetry, functional-test performance, symptom-free progression — drive return; elapsed weeks only set the earliest plausible window. Any reasoning that clears a trainee purely because "enough weeks have passed" is a category error the agent must avoid (ESTABLISHED, per C1.4/C4).

---

## Bibliography

1. Pollock N, James SLJ, Lee JC, Chakraverty R. British athletics muscle injury classification: a new grading system. *Br J Sports Med*. 2014;48(18):1347–51. PMID: 25031367. DOI: 10.1136/bjsports-2013-093302.
2. Cook JL, Purdam CR. Is tendon pathology a continuum? A pathology model to explain the clinical presentation of load-induced tendinopathy. *Br J Sports Med*. 2009;43(6):409–16. PMID: 18812414. DOI: 10.1136/bjsm.2008.051193.
3. Miller BF, Olesen JL, Hansen M, et al. Coordinated collagen and muscle protein synthesis in human patella tendon and quadriceps muscle after exercise. *J Physiol*. 2005;567(Pt 3):1021–33. PMID: 16002437. DOI: 10.1113/jphysiol.2005.093690.
4. Hoenig T, Tenforde AS, Strahl A, Rolvien T, Hollander K. Does magnetic resonance imaging grading correlate with return to sports after bone stress injuries? A systematic review and meta-analysis. *Am J Sports Med*. 2022;50(3):834–44. PMID: 33720786. DOI: 10.1177/0363546521993807. (Mean time to return to sport by MRI grade: 41.7 / 70.1 / 84.3 / 98.5 days for grades 1/2/3/4 — confirmed by direct fetch.)
5. Grindem H, Snyder-Mackler L, Moksnes H, Engebretsen L, Risberg MA. Simple decision rules can reduce reinjury risk by 84% after ACL reconstruction: the Delaware-Oslo ACL cohort study. *Br J Sports Med*. 2016;50(13):804–8. PMID: 27162233. DOI: 10.1136/bjsports-2016-096031.
6. Beyer R, Kongsgaard M, Hougs Kjær B, Øhlenschlæger T, Kjær M, Magnusson SP. Heavy slow resistance versus eccentric training as treatment for Achilles tendinopathy: a randomized controlled trial. *Am J Sports Med*. 2015;43(7):1704–11. PMID: 26018970. DOI: 10.1177/0363546515584760. (Alfredson eccentric protocol referenced within; original: Alfredson H et al., *Am J Sports Med* 1998;26(3):360–6, PMID: 9617396 — see Self-check.)
7. Rio E, Kidgell D, Purdam C, et al. Isometric exercise induces analgesia and reduces inhibition in patellar tendinopathy. *Br J Sports Med*. 2015;49(19):1277–83. PMID: 25979840. DOI: 10.1136/bjsports-2014-094386. (n=6 crossover.)
8. Clifford C, Challoumas D, Paul L, Syme G, Millar NL. Effectiveness of isometric exercise in the management of tendinopathy: a systematic review and meta-analysis of randomised trials. *BMJ Open Sport Exerc Med*. 2020;6(1):e000760. PMID: 32818059. DOI: 10.1136/bmjsem-2020-000760.
9. Gabbett TJ. The training–injury prevention paradox: should athletes be training smarter and harder? *Br J Sports Med*. 2016;50(5):273–80. PMID: 26758673. DOI: 10.1136/bjsports-2015-095788.
10. Impellizzeri FM, Woodcock S, Coutts AJ, Fanchini M, McCall A, Vigotsky AD. What role do chronic workloads play in the acute to chronic workload ratio? Time to dismiss ACWR and its underlying theory. *Sports Med*. 2021;51(3):581–92. PMID: 33332011. DOI: 10.1007/s40279-020-01378-6.
11. Ardern CL, Glasgow P, Schneiders A, et al. 2016 consensus statement on return to sport from the First World Congress in Sports Physical Therapy, Bern. *Br J Sports Med*. 2016;50(14):853–64. PMID: 27226389. DOI: 10.1136/bjsports-2016-096278.
12. Verhagen AP, Downie A, Popal N, Maher C, Koes BW. Red flags presented in current low back pain guidelines: a review. *Eur Spine J*. 2016;25(9):2788–802. PMID: 27376890. DOI: 10.1007/s00586-016-4684-0.
13. Pelliccia A, Sharma S, Gati S, et al. 2020 ESC Guidelines on sports cardiology and exercise in patients with cardiovascular disease. *Eur Heart J*. 2021;42(1):17–96. PMID: 32860412. DOI: 10.1093/eurheartj/ehaa605.
14. Gluckman TJ, Bhave NM, Allen LA, et al. 2022 ACC expert consensus decision pathway on cardiovascular sequelae of COVID-19 in adults: myocarditis and other myocardial involvement, post-acute sequelae of SARS-CoV-2 infection, and return to play. *J Am Coll Cardiol*. 2022;79(17):1717–56. PMID: 35307156. DOI: 10.1016/j.jacc.2022.02.003. (Identity + PMID + DOI confirmed by direct fetch of both the ACC summary page and the PubMed record.)
15. Elliott N, Martin R, Heron N, Elliott J, Grimstead D, Biswas A. Infographic. Graduated return to play guidance following COVID-19 infection. *Br J Sports Med*. 2020;54(19):1174–5. PMID: 32571796. DOI: 10.1136/bjsports-2020-102637.
16. Sayers SP, Clarkson PM. Exercise-induced rhabdomyolysis. *Curr Sports Med Rep*. 2002;1(2):59–60. PMID: 12831713. DOI: 10.1249/00149619-200204000-00001. (Eccentric/unaccustomed exercise as precipitant; CK/myoglobinuria; AKI risk — confirmed by direct fetch.) Corroborated for the full warning-sign cluster by: Rout P, Chippa V, Adigun R. Rhabdomyolysis. *StatPearls* [Internet]. Treasure Island (FL): StatPearls Publishing; Bookshelf ID NBK448168 — confirmed by direct fetch to state dark/reddish urine (myoglobinuria), muscle weakness/pain/myalgia/local swelling, strenuous/unaccustomed exercise as precipitant, elevated CPK (hallmark, ~≥5× ULN) for diagnosis, and AKI as a major complication.

---

## Self-check

**Claims fully grounded to a verified whitelisted primary/regulatory source (identifier confirmed by direct fetch):**
- BAMIC grading system and grade→prognosis (Pollock 2014, PMID 25031367 — confirmed) [1].
- Tendon continuum model stages (Cook & Purdam 2009, PMID 18812414 — confirmed) [2].
- Human patellar-tendon collagen synthesis time-course (6 h→peak 24 h→elevated 72 h) AND the explicit "synthesis-only, not net accretion" caveat (Miller 2005, PMID 16002437 — confirmed; caveat quoted from source) [3].
- ACL: 39.5% vs 19.4% reinjury, 51%/month reduction to 9 months, quad-symmetry <90% → 33.3% vs 12.5% (Grindem 2016, PMID 27162233 — confirmed) [5].
- Eccentric vs HSR equivalence at 52 weeks; compliance 92% vs 78% (Beyer 2015, PMID 26018970 — confirmed) [6].
- Isometric analgesia not superior to isotonic / not better than ice; variable response (Clifford 2020, PMID 32818059 — confirmed by direct fetch) [8].
- ACWR original sweet-spot 0.8–1.3 and ≥1.5 spike → 2–4× risk (Gabbett 2016, PMID 26758673) [9]; ACWR statistical-artifact repudiation, c-statistic ≈0.57, "dismiss ACWR" (Impellizzeri 2021, PMID 33332011 — confirmed) [10].
- Bern RTS consensus: continuum, shared decision-making, StARRT (Ardern 2016, PMID 27226389 — confirmed) [11].
- ESC 2020 sports cardiology guideline identity (Pelliccia, PMID 32860412 — confirmed by direct fetch) [13].
- Post-COVID GRTP staged structure and symptom-drop-back rule (Elliott 2020, PMID 32571796 — confirmed) [15].
- BSI mean return-to-sport by MRI grade (41.7/70.1/84.3/98.5 days, grades 1–4) (Hoenig 2022, PMID 33720786 — confirmed by direct fetch) [4].
- Rio isometric-analgesia finding, n=6, decline-squat pain 7.0→0.17 (Rio 2015, PMID 25979840 — confirmed by direct fetch) [7].
- 2022 ACC COVID pathway: symptom-triggered cardiac-triad testing, 3–6-month myocarditis abstention, reassessment-no-sooner-than-1-month (Gluckman 2022, PMID 35307156, JACC 79(17):1717–56 — confirmed by direct fetch of both the ACC summary and the PubMed record) [14].

**Claims I could NOT fully ground to a single verified primary identifier (honestly flagged, NOT fabricated):**
- **[6] Alfredson 1998 original (PMID 9617396):** the Alfredson eccentric protocol is described from within the Beyer 2015 RCT (confirmed) which references it; the standalone 1998 identifier is cited from knowledge of the canonical reference and was NOT directly fetched this session — verify the 1998 PMID before wiki ingestion. (The protocol *content* and the eccentric-vs-HSR comparison are source-confirmed via [6].)
- **[12] Verhagen 2016 low-back red-flag review (PMID 27376890 / DOI 10.1007/s00586-016-4684-0):** the Eur Spine J review was surfaced in search (Springer link confirmed the article exists with that DOI); the PMID was NOT independently fetched this session — verify the PMID specifically. The red-flag clinical content (cauda equina, fracture, malignancy cluster, weak isolated-night-pain caveat) is consistent across multiple guideline sources and is not in doubt; only the precise identifier needs confirmation.
- **[16] Exertional rhabdomyolysis — NOW HARDENED (iter-2):** anchored to two directly-fetched, resolvable sources: Sayers & Clarkson 2002 (*Curr Sports Med Rep* 1(2):59–60, **PMID 12831713**, DOI 10.1249/00149619-200204000-00001) and StatPearls "Rhabdomyolysis" (**NBK448168**, Rout/Chippa/Adigun). Direct fetch of the StatPearls chapter confirms all five clinical clauses verbatim: dark/reddish urine (myoglobinuria), muscle weakness/pain/myalgia/local swelling, strenuous/unaccustomed exercise as precipitant, elevated CPK (hallmark, ~≥5× ULN), and AKI as a major complication. The earlier soft placeholder (Tietze & Borchers) is removed. No residual identifier flag.

**Evidence-strength summary:**

*ESTABLISHED (high confidence):*
- Acute myocarditis = exercise contraindication; abstain (~3–6 mo) + cardiology clearance before return [13,14]. **SAFETY-CRITICAL.**
- Exertional red flags (chest pain, exertional syncope/near-syncope, disproportionate dyspnea, palpitations) → STOP + urgent evaluation [13,14]. **SAFETY-CRITICAL.**
- Exertional rhabdomyolysis cluster (severe pain + dark urine + swelling, esp. unaccustomed eccentric/post-layoff) → STOP + urgent evaluation [16]. **SAFETY-CRITICAL.**
- MSK red flags (cauda equina, fracture, progressive neuro deficit, malignancy/infection cluster) → refer, not load [12]. **SAFETY-CRITICAL.**
- ACWR-as-injury-predictor is methodologically discredited [10] (report alongside original hypothesis [9]) — **designated HALT-risk: must not be presented as settled prevention science.**
- RTS is criteria-based + shared decision (Bern/StARRT) [11]; ACL 9-month floor + strength criteria [5].
- Progressive loading is the core of tendinopathy management [2,3,6].
- Healing timeframes are RANGES, not guarantees [1,4,5].

*PROVISIONAL / CONTESTED:*
- Isometric analgesia for tendinopathy — CONTESTED; not reliably superior; responder/non-responder [7 vs 8].
- Eccentric vs HSR superiority — UNRESOLVED/broadly equivalent (single direct RCT) [6].
- Specific day/week counts for any recreational (non-elite) trainee — PROVISIONAL (population-mismatch: BAMIC/ACL/COVID-GRTP data are elite-athlete-derived).
- BSI specific week-range [4] — RANGE from secondary synthesis (see flag above).

**Distinct admissible sources cited: 16 primary refs + 1 corroborating StatPearls anchor on [16]. Directly-verified resolvable identifiers this session: refs 1,2,3,4,5,6,7,8,10,11,13,14,15,16 (incl. the iter-2-hardened ER anchor: Sayers & Clarkson PMID 12831713 + StatPearls NBK448168). Gabbett [9] PMID 26758673 surfaced in PubMed listing, content confirmed. Residual identifier-verification flags now limited to two non-safety refs: [6-Alfredson-1998 standalone PMID] and [12-Verhagen PMID] (clinical content confirmed; precise PMIDs to confirm before wiki ingestion). All four SAFETY-CRITICAL claim clusters (myocarditis contraindication, exertional cardiac red flags, exertional rhabdomyolysis, MSK red flags) are now content-grounded to regulatory/guideline or directly-fetched clinical sources with resolvable identifiers.**
