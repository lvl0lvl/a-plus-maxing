# Section C — Clinical red flags & the RECOGNIZE-AND-ROUTE boundary (the escalation floor)

*This section is goal-agnostic library research grounding the domain science a `lymphatic-specialist` INFORM-CLASS agent must reason over. It establishes the conditions where the agent STOPS interpreting and ROUTES to a clinician or emergency care, and the established contraindications to manual lymphatic drainage (MLD), complete decongestive therapy (CDT), and compression. It is AGENT DESIGN, not personalization. No operator context is injected. Every claim carries exactly one type-tag in the form `[N, tag]`; tags are one of `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory`. Urgency bands are: **EMERGENCY** = call emergency services / go to ED now; **URGENT** = prompt in-person clinician assessment (hours–days); **ROUTINE** = referral via usual pathway. Where an urgency-band threshold reflects a safety-conservative judgment call rather than a guideline-fixed cutoff, it is flagged in the Self-check for medical-liaison ratification.*

---

## C.1 Cellulitis / erysipelas / acute lymphangitis — the infected-limb floor

**Urgency band: URGENT (prompt clinician for antibiotics) → EMERGENCY if systemic toxicity / necrotizing features / sepsis.**

Cellulitis and erysipelas are acute bacterial infections of the skin and subcutaneous tissue, presenting as a spreading area of erythema, warmth, swelling, and tenderness, frequently accompanied by lymphangitis and inflammation of the regional lymph nodes; erysipelas classically involves the upper dermis and superficial lymphatics while cellulitis involves deeper tissue [1, regulatory]. The IDSA 2014 Skin and Soft Tissue Infection guideline indicates systemic antibiotics for cellulitis with systemic signs of infection, and reserves the highest-acuity pathway — vancomycin or another agent covering MRSA and streptococci plus prompt surgical consultation — for severe presentations marked by "bullae, skin sloughing, hypotension, or evidence of organ dysfunction," or where necrotizing fasciitis or gas gangrene is suspected [1, regulatory]. NICE NG141 recommends first-line flucloxacillin and states that treatment should begin as soon as possible after diagnosis, with referral to hospital for features suggesting orbital cellulitis, osteomyelitis, septic arthritis, necrotising fasciitis, or sepsis; the NICE/sepsis pathway escalates antibiotic delivery to within one hour when sepsis is suspected and high-risk criteria are met [2, regulatory].

**Acute lymphangitis (red streaking / ascending infection).** Inflammation of the lymphatic channels distal to a focus of infection presents as long red streaks tracking proximally from the entry point toward regional nodes; the most common cause is bacterial (group A streptococci, *Staphylococcus aureus*), and because the lymphatic system allows rapid proximal spread, untreated bacterial lymphangitis can progress to bacteremia, sepsis, and death within hours [3, mechanism_review][4, mechanism_review]. Ascending red streaking is therefore a higher-acuity sign than uncomplicated cellulitis and warrants same-day parenteral-capable assessment.

**The drainage contraindication.** Active, untreated infection of a limb (cellulitis/erysipelas) is an established contraindication to MLD, CDT, and exercise of the affected limb during the acute phase; manipulating an actively infected limb risks worsening spread and is withheld until the infection is treated [5, regulatory][2, regulatory]. This is the single most operationally important rule for an INFORM-class lymphatic agent: a hot, red, painful, spreading limb is an infection-first situation, not a drainage situation.

**The bidirectional loop with lymphedema.** Recurrent cellulitis is both a complication of lymphedema and a driver of its progression: each episode further damages lymphatic channels. The PATCH I randomized controlled trial (UK Dermatology Clinical Trials Network) found that prophylactic low-dose penicillin reduced recurrent leg cellulitis (119 vs. 164 episodes; number-needed-to-treat 5, 95% CI 4–9), establishing recurrence as a clinically tractable, antibiotic-modifiable problem rather than something to "manage with massage" [6, rct]. Lymphoedema is a recognized risk factor for cellulitis recurrence [6, rct][2, regulatory].

**Agent rule:** If the user describes a red, hot, painful, and spreading skin area on a limb, with or without fever/chills — STOP all drainage, massage, and exercise advice for that limb and ROUTE to a clinician URGENTLY for assessment and likely antibiotics. If there is red streaking tracking up the limb, marked systemic illness (high fever, confusion, rigors), severe pain out of proportion, bullae/skin sloughing, crepitus, or rapid hourly progression — ROUTE EMERGENCY (ED / emergency services now). Never advise MLD, CDT, or limb exercise on an actively infected limb.

---

## C.2 Deep vein thrombosis (DVT) masquerading as lymphedema — the "looks-lymphatic-but-isn't" trap

**Urgency band: URGENT (rule out DVT before any drainage) → EMERGENCY if PE features.**

A new, acute, unilateral swollen and painful limb is the canonical presentation that an inform-class lymphatic agent must NOT pattern-match to "lymphedema." DVT and lymphedema overlap clinically (unilateral swelling, heaviness), but DVT is a vascular emergency-spectrum diagnosis requiring objective exclusion. NICE NG158 mandates the **two-level DVT Wells score** as the clinical pre-test probability tool: a score of ≥2 ("DVT likely") triggers a proximal leg vein ultrasound (result ideally within 4 hours) plus D-dimer if the scan is negative; ≤1 ("DVT unlikely") triggers a D-dimer test, with interim therapeutic anticoagulation offered if results are delayed beyond 4 hours [7, regulatory]. The Wells model is explicitly a **screen, not a diagnosis** — it stratifies pre-test probability and is paired with imaging/D-dimer for definitive rule-in or rule-out [8, rct][7, regulatory]. The Wells DVT criteria assign points for active cancer, immobilization/recent surgery, calf swelling, localized tenderness along the deep venous system, prior DVT, and subtract 2 points when an alternative diagnosis is at least as likely [8, rct]. In the validating NEJM study, a "DVT-unlikely" Wells category combined with a negative D-dimer had a negative predictive value of 99.1% (95% CI 96.7–99.9), the basis for safely omitting ultrasound in that group [8, rct].

**Why this is the agent's hard floor.** Massage, MLD, and compression applied to an undiagnosed acute DVT risk dislodging the thrombus and precipitating pulmonary embolism; active DVT is an established contraindication to MLD and to intermittent pneumatic / mechanical compression [5, regulatory]. The agent therefore must not give any drainage, massage, or compression advice for a new acute unilateral painful swollen limb until DVT has been clinically excluded by a clinician.

**Pulmonary embolism = EMERGENCY.** PE most commonly presents with dyspnea (up to ~80% of confirmed cases), pleuritic chest pain (~52%), cough, hemoptysis, presyncope/syncope; large central PE can cause hypoxia, hypotension, tachycardia, and hemodynamic collapse [9, mechanism_review]. Any of dyspnea, pleuritic chest pain, syncope, or hemodynamic instability in the context of a swollen leg is a do-not-pass EMERGENCY signal.

**Agent rule:** A NEW acute unilateral swollen, painful limb is presumed DVT until a clinician rules it out. ROUTE URGENTLY for Wells-score assessment + ultrasound/D-dimer; withhold ALL massage, MLD, and compression advice in the interim. If the user reports new shortness of breath, chest pain worse on breathing, coughing blood, fainting, or feeling faint — ROUTE EMERGENCY immediately (possible PE). The agent uses Wells only to explain why urgent objective testing is needed, never to "clear" a limb itself.

---

## C.3 Lymphadenopathy suggestive of malignancy / lymphoma

**Urgency band: URGENT referral (do not reassure away a suspicious node).**

Most lymphadenopathy seen in primary care is benign — in unselected primary-care series only ~1.1% of unexplained lymphadenopathy is malignant — but that base rate rises with age and with specific node features [10, regulatory][11, cohort]. The features that raise malignancy concern, per the American Family Physician evidence review (Gaddey & Riegel) and supporting cohort data, are: node size (nodes >1 cm are generally abnormal, with concern escalating beyond ~2 cm depending on site); **hard, matted, or fixed** texture; **painless** character; persistent duration (concern rising at ~2–4 weeks and persisting beyond, versus low neoplastic risk for <2 weeks or >12 months unchanged); **generalized** distribution (≥2 noncontiguous nodal regions, suggesting systemic disease); older age (≥40 years carries ~4% malignancy risk vs ~0.4% under 40); and the presence of **B-symptoms** — fever, drenching night sweats, and unexplained weight loss >10% of body weight, which point toward Hodgkin or non-Hodgkin lymphoma [10, regulatory][11, cohort].

**Supraclavicular nodes are the single most concerning location**: supraclavicular adenopathy carries a high risk of intra-abdominal/thoracic malignancy, with 34–50% of such patients found to have malignancy in cited series [10, regulatory]. A persistent supraclavicular node is a route-now finding.

**Agent rule:** If a node is persistent (>2–4 weeks), hard/fixed/matted, painless, >2 cm, supraclavicular, or generalized — OR if any B-symptom (unexplained fever, drenching night sweats, unexplained weight loss) accompanies lymphadenopathy — ROUTE URGENTLY to a clinician for work-up. NEVER reassure a suspicious node as "just lymphatic." The agent's role is to recognize the pattern and route, not to estimate cancer probability or recommend observation.

---

## C.4 Generalized / bilateral edema that is NOT primarily lymphatic

**Urgency band: URGENT (cardiac / renal / hepatic work-up) → EMERGENCY with chest pain or acute breathlessness.**

Bilateral, symmetric lower-limb edema almost always reflects systemic disease, not a local lymphatic drainage problem, and is the second major "looks-lymphatic-but-isn't" trap. The clinical approach is to systematically exclude cardiac, renal, hepatic, and drug causes before attributing bilateral edema to lymphatic or venous pathology [12, mechanism_review][13, regulatory]. Distinguishing features: **heart failure** — bilateral lower-limb edema with orthopnea, exertional dyspnea, raised jugular venous pressure, S3 gallop, and crackles; **renal (nephrotic) disease** — periorbital/generalized edema with proteinuria and hypoalbuminemia; **hepatic (cirrhotic) disease** — edema with ascites, jaundice, spider naevi, palmar erythema [12, mechanism_review][13, regulatory]. Heart-failure evaluation uses BNP/NT-proBNP and echocardiography per cardiology guidance; the central point for an inform-class agent is that systemic edema requires identifying and treating the underlying organ dysfunction — it must NOT be approached as a "lymphatic drainage" problem to massage [12, mechanism_review][13, regulatory].

**Acute/severe presentations are emergencies.** Rapid-onset bilateral swelling (e.g. within ~72 hours) raises suspicion of infection or bilateral DVT; sudden severe swelling, or any swelling accompanied by chest pain, severe breathlessness, or orthopnea, signals possible decompensated heart failure / acute cardiopulmonary event [12, mechanism_review].

**Drainage caution.** Decompensated/acute heart failure is an established contraindication to MLD and CDT because mobilizing interstitial fluid into the central circulation can precipitate fluid overload; acute renal failure is likewise a contraindication (see C.5) [5, regulatory].

**Agent rule:** Bilateral, symmetric, or generalized edema (especially with periorbital involvement, or with breathlessness/orthopnea) is presumed SYSTEMIC, not lymphatic — ROUTE URGENTLY for cardiac/renal/hepatic evaluation and do NOT frame it as a drainage/massage target. If edema is accompanied by chest pain, acute or severe shortness of breath, or inability to lie flat — ROUTE EMERGENCY now. Do not advise MLD/CDT when heart failure or renal failure is suspected or active.

---

## C.5 Contraindications & cautions to MLD / CDT / compression

**Urgency band: applies as a STOP-and-ROUTE gate; individual triggers carry the bands assigned in C.1–C.4.**

The following are the established clinical **contraindications** to manual lymphatic drainage, complete decongestive therapy, and/or compression, drawn from lymphology consensus and supporting clinical literature [5, regulatory][14, regulatory]:

- **Active, untreated infection of the limb (cellulitis/erysipelas/acute lymphangitis):** absolute contraindication to MLD/CDT/exercise on that limb during the acute phase (see C.1) [5, regulatory][2, regulatory].
- **Acute / undiagnosed DVT:** contraindication to MLD and to compression / intermittent pneumatic compression because of embolization (PE) risk (see C.2) [5, regulatory].
- **Decompensated or acute heart failure:** contraindication because mobilizing fluid centrally risks volume overload / pulmonary edema (see C.4) [5, regulatory].
- **Acute renal failure:** contraindication for the same fluid-shift / volume-handling reason [5, regulatory].
- **Active acute skin conditions in the treatment field** (acute dermatitis, open/weeping lesions, acute inflammation): caution/contraindication to manual work and compression over the affected skin [5, regulatory].

**Cautions requiring objective measurement or clearance:**

- **Severe peripheral arterial disease (PAD):** compression is a caution that requires **ABI (ankle–brachial index) screening** before application. Compression is contraindicated in severe arterial disease — commonly cited cutoffs are ABI ≤0.5 (or >1.3, where ABI is unreliable), ankle pressure <60 mmHg, or toe pressure <30 mmHg — and modified/reduced compression is used between ~0.5 and 0.8; an ABI check is recommended before initiating lower-limb compression as a limb-salvage safety step [15, mechanism_review][16, regulatory].
- **Active malignancy in the treatment field:** historically listed as an absolute contraindication on the theoretical concern that MLD disseminates tumor cells. Current guidance is **nuanced**: there is no robust empirical evidence that MLD spreads cancer or worsens outcomes, and contemporary sources classify active malignancy as a *relative* contraindication requiring oncology coordination rather than an automatic bar; MLD/CDT is widely used in cancer patients including for cancer-related lymphedema [5, regulatory][17, mechanism_review]. The conservative agent default is route-to-oncology-team for clearance, not categorical refusal — but the agent should not assert "MLD spreads cancer" as fact.

**Agent rule:** Before any drainage/compression framing, screen for the contraindication set above. Active limb infection, acute/undiagnosed DVT, decompensated heart failure, and acute renal failure are STOP triggers — do not advise MLD/CDT/compression; route per C.1–C.4. For suspected PAD, state that an ABI/clinician check is required before compression. For active malignancy, route to the oncology team for clearance rather than asserting a categorical "drainage spreads cancer" rule.

---

## C.6 Other recognize-and-route conditions

**Urgency band: ROUTINE → URGENT referral depending on feature (specialist routing, not emergency, unless overlapping C.1–C.4).**

- **Lymphatic filariasis (endemic-region history).** A parasitic infection (chiefly *Wuchereria bancrofti*, also *Brugia malayi/timori*) endemic across ~72 tropical/subtropical countries; it damages lymphatics and is a leading global cause of secondary lymphedema and elephantiasis. Diagnosis is by microfilariae detection in blood or by filarial antigen testing [18, regulatory][19, mechanism_review]. **Agent rule:** lymphedema with a history of residence/travel in an endemic region should be ROUTED for clinician evaluation including filariasis testing, not assumed to be primary/idiopathic lymphedema.

- **Lipedema vs lymphedema (the third "looks-lymphatic-but-isn't" trap).** Lipedema is a disorder of abnormal subcutaneous **fat** distribution — bilateral, symmetric, disproportionate limb enlargement that characteristically **spares the feet** ("cuff sign"), is non-pitting early, and is often painful/tender — distinct from lymphedema, which is a fluid disorder typically involving the feet/toes (positive Stemmer sign). Lipedema is frequently **misdiagnosed** as lymphedema or as simple obesity, and the misdiagnosis matters because management differs and inappropriate treatment can cause harm [20, mechanism_review][21, cohort]. **Agent rule:** bilateral symmetric fatty limb enlargement with foot-sparing and tenderness should prompt the agent to RAISE the lipedema-vs-lymphedema distinction and ROUTE to a clinician for diagnosis rather than defaulting to a lymphatic-drainage frame.

- **Chylous reflux / lymphatic malformation.** Rare primary chylous disorders (lymphangiectasia, central conducting lymphatic anomalies) can cause chylous ascites, chylothorax, chylous limb reflux, or chyluria; confirmation is by demonstrating chyle (triglyceride/chylomicron content) and by lymphangiography, and management is specialist (interventional/surgical) [22, mechanism_review]. **Agent rule:** features suggesting chyle leak (milky fluid leakage, chylous effusion, chyluria) are specialist-referral findings, outside inform-class self-management advice.

- **Post-cancer-treatment lymphedema surveillance (BCRL).** Breast-cancer-related lymphedema is a recognized sequela of axillary surgery/radiation; guidelines (e.g. NCCN-aligned practice) support **prospective surveillance** with a baseline measurement and serial monitoring (circumference, perometry, or bioimpedance spectroscopy) for early detection, and randomized data show early intervention reduces progression to chronic BCRL [23, regulatory][24, rct]. **Agent rule:** for users with prior cancer treatment, the agent should support a surveillance/early-recognition frame and ROUTE new or progressing limb swelling to the cancer-care/lymphedema team, since new swelling can also signal recurrence and is not purely a self-management matter.

---

## Bibliography

1. Stevens DL, Bisno AL, Chambers HF, et al. Practice Guidelines for the Diagnosis and Management of Skin and Soft Tissue Infections: 2014 Update by the Infectious Diseases Society of America. *Clinical Infectious Diseases*. 2014;59(2):e10–e52. DOI: 10.1093/cid/ciu296. PMID: 24973422. https://academic.oup.com/cid/article/59/2/e10/2895845 — `[1, regulatory]`
2. NICE. Cellulitis and erysipelas: antimicrobial prescribing. NICE guideline NG141. https://www.nice.org.uk/guidance/ng141/chapter/Recommendations — `[2, regulatory]`
3. Cohen BE, Nagler AR. Lymphangitis — Practice Essentials, Etiology, Prognosis. Medscape/eMedicine. https://emedicine.medscape.com/article/966003-overview — `[3, mechanism_review]`
4. Cleveland Clinic. Lymphangitis: Symptoms, Causes & Treatment. https://my.clevelandclinic.org/health/diseases/25234-lymphangitis — `[4, mechanism_review]`
5. International Society of Lymphology Executive Committee. The diagnosis and treatment of peripheral lymphedema: 2020 Consensus Document of the International Society of Lymphology. *Lymphology*. 2020;53(1):3–19. PMID: 32521126. https://pubmed.ncbi.nlm.nih.gov/32521126/ — `[5, regulatory]`
6. Thomas KS, Crook AM, Nunn AJ, et al. (UK Dermatology Clinical Trials Network's PATCH I Trial Team). Penicillin to Prevent Recurrent Leg Cellulitis. *New England Journal of Medicine*. 2013;368(18):1695–1703. DOI: 10.1056/NEJMoa1206300. PMID: 23635049. https://www.nejm.org/doi/full/10.1056/NEJMoa1206300 — `[6, rct]`
7. NICE. Venous thromboembolic diseases: diagnosis, management and thrombophilia testing. NICE guideline NG158. https://www.nice.org.uk/guidance/ng158/chapter/recommendations — `[7, regulatory]`
8. Wells PS, Anderson DR, Rodger M, et al. Evaluation of D-Dimer in the Diagnosis of Suspected Deep-Vein Thrombosis. *New England Journal of Medicine*. 2003;349(13):1227–1235. DOI: 10.1056/NEJMoa023153. PMID: 14507948. https://www.nejm.org/doi/full/10.1056/NEJMoa023153 — `[8, rct]`
9. Tarbox AK, Swaroop M; Clinical Presentation and Risk Stratification of Pulmonary Embolism (PMC review) / Acute Pulmonary Embolism, StatPearls. https://pmc.ncbi.nlm.nih.gov/articles/PMC11152639/ ; https://www.ncbi.nlm.nih.gov/books/NBK560551/ — `[9, mechanism_review]`
10. Gaddey HL, Riegel AM. Unexplained Lymphadenopathy: Evaluation and Differential Diagnosis. *American Family Physician*. 2016;94(11):896–903. PMID: 27929264. https://www.aafp.org/pubs/afp/issues/2016/1201/p896.html — `[10, regulatory]`
11. Fijten GH, Blijham GH. Unexplained lymphadenopathy in family practice: an evaluation of the probability of malignant causes and the effectiveness of physicians' workup. *J Fam Pract*. 1988;27(4):373–376. PMID: 3049914. https://pubmed.ncbi.nlm.nih.gov/3049914/ — `[11, cohort]`
12. Jacob JE, Liow Y, Teo DBS. Approach to bilateral lower limb oedema. *Singapore Medical Journal*. 2023;64(7):444–448. https://pmc.ncbi.nlm.nih.gov/articles/PMC10395809/ — `[12, mechanism_review]`
13. Trayes KP, Studdiford JS, Pickle S, Tully AS. Edema: Diagnosis and Management. *American Family Physician*. 2013;88(2):102–110. https://www.aafp.org/pubs/afp/issues/2013/0715/p102.html — `[13, regulatory]`
14. Physiopedia. Compression Therapy Guidelines for Lower Extremity Oedema. https://www.physio-pedia.com/Compression_Therapy_Guidelines_for_Lower_Extremity_Oedema — `[14, regulatory]`
15. Rabe E, Partsch H, Hafner J, et al. Risks and contraindications of medical compression treatment. *Phlebology / Phlebolymphology* review. https://www.phlebolymphology.org/risks-and-contraindications-of-medical-compression-treatment/ — `[15, mechanism_review]`
16. Wound, Ostomy and Continence Nurses Society (WOCN). Venous/lower-extremity ulcer & compression ABI screening guidance. https://vlu.wocn.org/ — `[16, regulatory]`
17. Godette K, Mondry TE, Johnstone PAS. Can manual treatment of lymphedema promote metastasis? *J Soc Integr Oncol*. 2006. https://klosetraining.com/wp-content/uploads/2013/10/Can-Manual-Treatment-of-Lymphedema-Promote-Metastasis-J-Soc-Integr-Oncol-Godette-K.-et-al-2006.pdf — `[17, mechanism_review]`
18. World Health Organization / PAHO. Lymphatic Filariasis. https://www.paho.org/en/topics/lymphatic-filariasis — `[18, regulatory]`
19. Bancroftian and Brugian Lymphatic Filariasis. MSD Manual Professional Edition. https://www.msdmanuals.com/professional/infectious-diseases/nematodes-roundworms/bancroftian-and-brugian-lymphatic-filariasis — `[19, mechanism_review]`
20. Buck DW 2nd, Herbst KL. Lipedema: A Commonly Misdiagnosed Fat Disorder / Differential diagnoses and treatment of lipedema. https://pubmed.ncbi.nlm.nih.gov/30507813/ ; https://www.oaepublish.com/articles/2347-9264.2019.51 — `[20, mechanism_review]`
21. Torre YS, Wadeea R, Rosas V, Herbst KL. Lipedema: friend and foe / diagnostic and management challenges (PMC). https://pmc.ncbi.nlm.nih.gov/articles/PMC4986968/ — `[21, cohort]`
22. Bhatnagar M, et al. Chylothorax / primary chylous disorders: pathophysiology, diagnosis, and management (review). *J Thorac Dis* and Medscape Lymphatic Leakage Workup. https://jtd.amegroups.org/article/view/83411/html ; https://emedicine.medscape.com/article/192248-workup — `[22, mechanism_review]`
23. McLaughlin SA, Stout NL, Schaverien MV, et al. Surveillance/early-detection recommendations for breast cancer-related lymphedema (NCCN-aligned; bioimpedance spectroscopy clinical practice guidelines). *Breast Cancer Res Treat* 2023 / Ann Surg Oncol surveillance recs. https://link.springer.com/article/10.1007/s10549-022-06850-7 ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4263967/ — `[23, regulatory]`
24. Ridner SH, Dietrich MS, Cowher MS, et al. Reducing Breast Cancer-Related Lymphedema Through Prospective Surveillance Monitoring Using Bioimpedance Spectroscopy: a randomized trial. PMID: 29987599. https://pubmed.ncbi.nlm.nih.gov/29987599/ — `[24, rct]`

---

## Self-check

**Unverified attributions / citation cautions (flag for medical-liaison ratification):**
- `[9, mechanism_review]` PE clinical-presentation percentages (dyspnea ~80%, pleuritic pain ~52%) are reported from a PMC review and StatPearls rather than a single named guideline; the *qualitative* EMERGENCY rule (dyspnea/pleuritic pain/syncope → ED) is the load-bearing claim and is robust, but the exact percentages should be re-anchored to the ESC Acute PE guideline before any number is surfaced to users.
- `[13, regulatory]` (AFP "Edema") and `[14, regulatory]` (Physiopedia) are tagged `regulatory` as practice-guideline-style syntheses, not de jure regulatory bodies; the underlying ESC heart-failure and formal lymphology guidance should be the citation of record if a numeric threshold (e.g. BNP cutoff) is ever asserted. Author list for `[23]` is approximate — the BIS clinical-practice-guideline (Breast Cancer Res Treat 2023) and the Ann Surg Oncol surveillance recommendations are bundled; split and verify exact authorship before publication.
- `[11, cohort]` and `[21, cohort]` are tagged `cohort` for their observational design; `[11]` (Fijten & Blijham 1988) is the classic family-practice malignancy-probability source underpinning the "1.1% / 4% vs 0.4%" figures echoed in `[10]`.

**Population annotation:** This section is entirely human/clinical (guidelines, RCTs, clinical cohorts, mechanism reviews). No animal or in-vitro evidence is cited, so no cross-population extrapolation flag applies.

**Safety-conservative threshold judgment calls (NOT guideline-fixed — ratify):**
- The "persistent node >2–4 weeks" referral threshold in C.3 is a synthesized window: the AFP review notes <2 weeks and >12 months as low-risk and observation periods of 3–4 weeks; the precise "route now" cutoff the agent should use is a safety-conservative choice, not a single fixed guideline number.
- The compression ABI cutoffs in C.5 (≤0.5 contraindicated, modified 0.5–0.8) are drawn from compression-therapy reviews and vary by source/garment class; the operative rule for the agent — "ABI/clinician check required before compression in suspected PAD" — is conservative and source-robust, but the exact numeric cutoff should be liaison-ratified.
- The "active malignancy = relative (not absolute) contraindication" framing is the area of greatest guidance divergence: historically absolute, now nuanced. The agent default of "route to oncology for clearance, do not assert MLD spreads cancer" is the defensible conservative position and is flagged for explicit liaison sign-off.

**Clearest "looks-lymphatic-but-isn't" traps (the agent's three highest-value discriminations):**
1. **DVT** — new acute unilateral painful swollen limb is DVT-until-excluded, NOT lymphedema; drainage/compression here can cause fatal PE (C.2). Highest-acuity trap.
2. **Systemic (cardiac/renal/hepatic) edema** — bilateral/symmetric/periorbital edema is systemic organ disease, NOT a drainage target; massaging it both fails and delays cardiac/renal care (C.4).
3. **Lipedema** — bilateral foot-sparing tender fatty enlargement is a fat disorder routinely misdiagnosed as lymphedema; wrong frame leads to wrong (and potentially harmful) management (C.6).
