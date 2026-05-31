# Section C — Conditions (Literacy) + Red-Flags + Image/Test Validity

> GOAL-AGNOSTIC library research for the `dermatologist` sub-agent safety boundary. No operator/patient referenced.
> Type-tag legend (tag ∈ EXACTLY): `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`.
> Retrieved 2026-05-31. Every citation below was confirmed against its abstract/record (first author + year) before inclusion.

---

## C.1 Common conditions at literacy level (acne, rosacea, atopic dermatitis, seb derm)

These are management-PRINCIPLE summaries from guideline bodies. They are NOT diagnostic criteria and NOT prescription instructions. The agent uses them to recognize "this is a chronic OTC-adjacent dermatosis" vs "this needs a clinician," not to assign a diagnosis or a regimen.

**Acne vulgaris.** Literacy-level "what this is": a chronic inflammatory disorder of the pilosebaceous unit producing comedones, papules, pustules, and (in inflammatory forms) nodules/scarring. The AAD 2024 guideline issued 18 evidence-based recommendations + 5 good-practice statements using GRADE [4, regulatory]. **OTC-manageable layer:** topical benzoyl peroxide and adapalene (a retinoid now available OTC) carry STRONG recommendations; benzoyl peroxide + salicylic-acid washes are first-line self-care [4, regulatory]. **Needs-a-clinician layer:** oral antibiotics (doxycycline strong rec), hormonal therapy (combined oral contraceptives, spironolactone — conditional), topical clascoterone (Rx), and especially **oral isotretinoin** for severe/scarring/psychosocially-burdensome or treatment-refractory acne — isotretinoin is teratogenic and iPLEDGE-regulated and is categorically a prescriber decision [4, regulatory]. Boundary principle: the agent may name OTC categories at a literacy level but routes systemic-therapy and refractory/scarring presentations to a clinician.

**Rosacea.** Literacy-level "what this is": a chronic facial disorder presenting as transient/persistent centrofacial erythema, flushing, papulopustules, telangiectasia, and phymatous change; ocular involvement occurs. The global ROSacea COnsensus (ROSCO) 2019 panel (21 dermatologists/ophthalmologists, modified Delphi) endorses a **phenotype-based** rather than subtype-based approach — manage by presenting feature (erythema, papulopustules, phyma, ocular) [6, practitioner_protocol]. **OTC/self-care layer:** trigger avoidance (sun, heat, alcohol, spicy food), gentle skincare, photoprotection. **Needs-a-clinician layer:** topical brimonidine/oxymetazoline (erythema), topical ivermectin/metronidazole/azelaic acid, oral doxycycline (sub-antimicrobial dose), and ocular rosacea (ophthalmology) are prescriber-managed [6, practitioner_protocol]. Boundary principle: phymatous and ocular rosacea are explicit referral triggers.

**Atopic dermatitis / eczema.** Literacy-level "what this is": a chronic, relapsing, intensely pruritic inflammatory dermatosis with an impaired skin barrier; flexural distribution in adults. The AAD 2023 adult topical-therapy guideline (Sidbury et al., GRADE) makes **moisturizers/emollients and topical corticosteroids first-line**, recommends twice-weekly proactive topical-corticosteroid maintenance to reduce flares, and recommends AGAINST topical antihistamines, antimicrobials, and antiseptics for routine AD [5, regulatory]. **OTC-manageable layer:** bland emollients, fragrance-free moisturizers, and short courses of low-potency OTC hydrocortisone for mild flares. **Needs-a-clinician layer:** mid/high-potency corticosteroids, topical calcineurin inhibitors, topical PDE-4 (crisaborole/roflumilast) and JAK inhibitors, and systemic/biologic therapy (dupilumab, etc.) are prescriber-managed [5, regulatory]. Boundary principle: weeping/secondarily-infected eczema and failure of OTC measures are referral triggers.

**Seborrheic dermatitis.** Literacy-level "what this is": a common chronic relapsing dermatitis of sebaceous-rich areas (scalp, nasolabial folds, brows, chest) linked to *Malassezia* yeast; "dandruff" is its mild scalp form. A 2024 narrative review (Tynes et al.) aggregates RCT-level evidence that topical azole antifungals are effective; FDA approval of ketoconazole is for dandruff [11, mechanism_review]. **OTC-manageable layer:** OTC antifungal/antiseborrheic shampoos — **ketoconazole 1%** (the 2% is Rx-only), selenium sulfide, zinc pyrithione, ciclopirox — are first-line self-care; RCT data within the review show ketoconazole markedly outperforming placebo (e.g., 89% vs 44% improvement in one double-blind trial) [11, mechanism_review]. **Needs-a-clinician layer:** facial/widespread or treatment-resistant disease, and distinguishing seb derm from look-alikes (psoriasis, lupus, tinea), are clinician tasks. Boundary principle: the agent treats "scalp/dandruff self-care" as the OTC envelope and refers facial/refractory disease and any diagnostic uncertainty.

**C.1 boundary statement.** For all four conditions the agent's permitted output is the literacy-level "what this is" + the OTC-vs-clinician *category* split. It does NOT prescribe, dose, or select an agent, and it does NOT assert a diagnosis — any of these conditions can be mimicked by something requiring biopsy (the seb derm/lupus, the eczema/cutaneous-T-cell-lymphoma overlaps), so "looks like X" is itself outside the boundary.

---

## C.2 Skin-cancer red-flag: ABCDE, BCC/SCC, non-healing lesions; not-remotely-diagnosable evidence

**This is the load-bearing section.** The conclusion the agent enforces: skin cancer is NOT reliably diagnosable without an in-person exam plus dermoscopy and, where indicated, biopsy. A remote agent must REFER, never reassure ("probably benign" is a prohibited output).

### C.2.1 The criteria a layperson can apply (recognition, not diagnosis)

- **Melanoma — ABCDE** (Tsao et al., *JAAD* 2015, review of the ABCDE rule): **A**symmetry, **B**order irregularity, **C**olor variegation, **D**iameter >6 mm, **E**volving/changing [8, mechanism_review]. The review explicitly flags that the diameter criterion misses small (<6 mm) melanomas and that sensitivity/specificity depend heavily on whether criteria are used singly vs combined and on examiner experience — i.e., ABCDE is a **prompt to seek evaluation, not a diagnostic test** [8, mechanism_review].
- **"Ugly duckling" sign:** a nevus that looks different from the patient's other nevi warrants evaluation; complements ABCDE because some melanomas are ABCDE-negative [8, mechanism_review].
- **Basal cell carcinoma (BCC):** the most common human cancer (Bichakjian et al., AAD 2018 guideline); warning presentations include a pearly/translucent papule with telangiectasia, a non-healing sore that bleeds/crusts and recurs, and a scar-like waxy plaque [7, regulatory].
- **Squamous cell carcinoma (SCC):** a firm scaly/crusted or ulcerated lesion on sun-exposed skin, a non-healing sore, or a new growth on a scar/chronic wound; tender or rapidly growing lesions are concerning [7, regulatory].
- **Universal red flags (any lesion):** new, changing, non-healing, bleeding, ulcerating, or symptomatic (itch/pain) lesions [7, regulatory; 8, mechanism_review].

### C.2.2 Diagnosis requires histopathology / dermoscopy by a clinician — the evidence

- **BCC/SCC guideline (Bichakjian, AAD 2018):** the diagnostic pathway is **biopsy of the clinically suspicious lesion with histopathologic confirmation** — diagnosis is established on tissue, not on visual impression, and definitive treatment (excision, Mohs micrographic surgery) follows histology [7, regulatory]. There is no guideline-sanctioned remote/visual route to a BCC/SCC diagnosis.
- **Dermoscopy vs naked eye (Dinnes et al., Cochrane 2018):** the largest diagnostic-accuracy synthesis — 26 in-person evaluations (23,169 lesions; 1,664 melanomas), plus a large image-based body. In-person dermoscopy added to visual inspection was **more accurate than visual inspection alone** (relative diagnostic odds ratio 4.7, 95% CI 3.0–7.5; P<0.001), with a predicted sensitivity gain of 16% (92% vs 76%) at fixed 80% specificity, and a 20% specificity gain (95% vs 75%) at fixed 80% sensitivity [2, meta_analysis]. Critically for the remote boundary: **in-person diagnosis was more accurate than image-based interpretation** (relative DOR 4.6, 95% CI 2.4–9.0, P<0.001) — i.e., evaluating a photo is measurably worse than examining the patient [2, meta_analysis]. The authors' lay summary states the **naked eye alone is not enough** for accurate skin-cancer diagnosis.

### C.2.3 Why delay is harmful — melanoma prognosis by stage

- **SEER 21 (2016–2022) 5-year relative survival by stage** [3, cohort]: **localized 99.6–100%** (≈77% of cases diagnosed here), **regional ~76%**, **distant ~34%**; all-stages combined ≈94.7%. The cliff from localized to distant survival is the entire reason early in-person evaluation matters — and the reason a false "probably benign" reassurance that delays a referral is a high-harm error [3, cohort].
- **Diagnostic-delay/Breslow-thickness literature** (cohort evidence, multiple series): risk of melanoma death tracks Breslow thickness, and longer patient/diagnostic delay associates with thicker tumors at presentation (e.g., series reporting ~94% of patients evaluated within 3 months presenting Breslow <1.5 mm vs ~53% of those waiting >12 months presenting >1.5 mm; COVID-era lockdown delays produced documented Breslow upstaging) [see C.5/Bibliography note; cohort]. The directional, guideline-consistent signal — delay → thicker tumor → worse stage → worse survival — is robust even though the delay-to-thickness correlation is statistically weak in some series. This grounds the rule: **the cost of a missed/late melanoma is catastrophic and irreversible; the cost of an unnecessary referral is low. The agent must asymmetrically favor referral.**

### C.2.4 Boundary statement (reasoning_integrity)

Skin cancer is not remotely diagnosable: definitive diagnosis is histopathologic (biopsy), best clinical triage is in-person dermoscopy, and image-based assessment is empirically inferior to in-person assessment [2, meta_analysis; 7, regulatory]. The agent therefore must NOT diagnose lesions, must NOT interpret photos, and must NOT reassure — any pigmented/non-healing/changing/bleeding lesion gets a **refer-to-in-person-clinician** output. "Probably benign" is prohibited because its false-negative cost (a delayed distant-stage melanoma, ~34% 5-yr survival) is not recoverable.

---

## C.3 Clinical-image-input + AI/teledermatology validity (grounds IMAGE_OR_SIGNAL_INPUT refusal)

Skin is the most photo-pasted clinical domain, so this is the empirical backbone of the agent's refusal to interpret an uploaded skin photo.

### C.3.1 Smartphone "skin-check" apps — the regulatory + accuracy verdict

- **Freeman et al., *BMJ* 2020** (systematic review of diagnostic-accuracy studies; 9 studies, 6 algorithm-based apps) [1, meta_analysis]: across AI-based apps, **sensitivity ranged from ~7% to 73% and specificity from ~37% to 94%** — wildly inconsistent and frequently missing most cancers. The most-studied app (SkinVision) achieved sensitivity 80% (95% CI 63–92%) / specificity 78% (67–87%). Authors' conclusion verbatim: **"current algorithm based smartphone apps cannot be relied on to detect all cases of melanoma or other skin cancers,"** and real-world performance is "likely to be poorer than reported here when used in clinically relevant populations" [1, meta_analysis].
- **Regulatory status (from the same review):** at publication **no such app had US FDA approval**; the available apps carried only a CE mark, and the authors stated the **CE-marking process "does not provide adequate protection to the public"** [1, regulatory]. This is the explicit basis for treating skin-lesion classification as **Software-as-a-Medical-Device (SaMD)** subject to regulatory clearance — and for treating a general LLM, which has NO such clearance, as definitively not a diagnostic device.

### C.3.2 AI/CNN classifiers — "dermatologist-level" headlines vs the fine print

- **Esteva et al., *Nature* 2017** (the foundational CNN paper; 129,450 clinical images, 2,032 diseases) reported CNN performance "on par with" 21 board-certified dermatologists on two binary tasks (keratinocyte carcinoma vs benign; melanoma vs nevus) [9, open_label]. **Fine print that bounds the headline:** the test set was **biopsy-proven** images (curated, confirmed-diagnosis cases), not the noisy, uncurated, mixed-quality photos a consumer uploads — so it validated against an idealized distribution, not real-world screening [9, open_label]. Headline "dermatologist-level" accuracy does NOT transfer to an LLM ingesting a phone snapshot.

### C.3.3 Skin-tone validity gap — the equity failure mode

- **Patel Housley et al., *Cureus* 2025** evaluated **ChatGPT-4o** on 324 biopsy-confirmed images from the Diverse Dermatology Images dataset (3 ranked differentials + malignancy call vs histopathology) [10, cohort]. Melanoma sensitivity (top differential): **100% for Fitzpatrick I–II but collapsed to 29% (FST III–IV) and 43% (FST V–VI)** — a statistically significant accuracy decline in darker skin [10, cohort]. This is direct evidence that a general-purpose LLM is unsafe as a skin-lesion classifier, with the failure concentrated exactly where melanoma is already under-detected.
- **Dataset root cause (corroborating, off-whitelist literature):** public training sets (ISIC) are ~82% Fitzpatrick I–III; FST V/VI together ~8%, with as few as ~8 melanoma images for FST V — so models "learn" light skin and degrade on dark skin [anecdote_aggregate, off-whitelist arXiv/preprint corroboration only].

### C.3.4 Teledermatology — even WITH a clinician in the loop, remote is bounded

- Teledermatology systematic reviews report ~76% diagnostic concordance across all conditions and improved performance with **teledermoscopy** + expert reading; concordance scaled with image quality (≈79% patient-acquired, 84% assisted, 87% resident-acquired images) [meta_analysis-level synthesis; see Bibliography]. The benefit of dermoscopy is **attenuated in remote settings** vs in-person [consistent with 2, meta_analysis]. Key inference for the agent: teledermatology works **because a licensed clinician interprets dermoscopic-quality images within a care pathway** — it is NOT a license for an un-credentialed LLM to read a consumer photo.

### C.3.5 Boundary statement

An un-validated LLM is not a SaMD diagnostic device: skin-lesion classifiers are regulated devices (FDA/CE), the best consumer apps miss a large fraction of cancers (sensitivity as low as 7%) [1, meta_analysis/regulatory], "dermatologist-level" CNN results were obtained on curated biopsy-proven images not consumer photos [9, open_label], and a frontier LLM's melanoma sensitivity collapses to 29–43% in darker skin [10, cohort]. Therefore the agent REFUSES `IMAGE_OR_SIGNAL_INPUT` for skin lesions and routes to in-person evaluation — it does not "take a look."

---

## C.4 Consumer / DTC skin-test validity

- **DTC skin/oral microbiome kits:** A 2025 regulatory/legal analysis (*Journal of Law and the Biosciences*, Oxford) concludes DTC microbiome tests — including skin-microbiome kits — **lack analytical and clinical validity**, produce false positives/negatives, are marketed misleadingly, and the current regulatory framework is insufficient to protect consumers from medical/economic/dignitary harm [12, regulatory]. There is no validated DTC skin-microbiome test that supports a skincare or disease decision.
- **At-home "skin sensitivity"/IgG allergy panels:** The AAAAI (with EAACI and CSACI) advises AGAINST at-home food/skin **IgG "sensitivity" tests** — IgG presence reflects normal exposure, not a clinically meaningful trigger, and the supporting literature is old and in non-reputable venues [AAAAI/EAACI position; practitioner_protocol]. These panels do not establish skin-disease causation.
- **At-home "skin-analysis"/AI-scan apps** (cosmetic camera apps rating wrinkles/pores/"skin age"): no clinical-grade validation as diagnostic tools; they fall under the same SaMD-vs-cosmetic-claim distinction as the lesion apps in C.3 — cosmetic scoring is not a medical test.

**C.4 boundary statement.** No DTC skin test (microbiome, IgG "sensitivity," AI skin-scan) is validated to drive a diagnostic or treatment decision. The agent treats DTC skin-test results as non-evidentiary and does not interpret them as findings.

---

## C.5 Non-English literature survey (+ confirmed-absence note)

Mandatory at standard mode. Databases/indexes searched: PubMed/PMC, Cochrane, and open web via Spanish- and German-language query strings (`dermatoscopia melanoma precisión diagnóstica`, `Dermoskopie Melanom diagnostische Genauigkeit`), plus a Chinese-melanoma-delay query.

- **Spanish-language corroboration found, but secondary/off-whitelist:** *Actas Dermo-Sifiliográficas* (the Spanish AEDV journal) carries descriptive series and reviews on dermoscopy of melanoma (e.g., dermoscopy to infer Breslow thickness; descriptive series of 45 and 200 melanoma lesions). These **corroborate** the C.2 boundary — they report that dermoscopic accuracy depends on an experienced in-person examiner and cite the Dinnes Cochrane review as authority — but they are descriptive/review series, off the admissible primary whitelist, and would type-tag `anecdote_aggregate`. They do not change any boundary.
- **Chinese-language:** a cross-sectional study of diagnostic delay in Chinese melanoma patients (MDPI, English-published) corroborates the delay→thickness signal but is English-language and registry/cohort-descriptive.
- **Confirmed-absence note:** **No admissible non-English PRIMARY (Tier-1 pubmed/PMC RCT/meta-analysis/cohort or Tier-2 regulatory/guideline) that alters the C.1–C.4 conclusions was located in PubMed/PMC or Cochrane.** The anchoring evidence (Dinnes Cochrane, Freeman BMJ, AAD guidelines, SEER, ROSCO) is English-language and already admissible; non-English literature is corroborative only. Recorded as confirmed-absence per standard-mode requirement.

---

## C.6 GRADE / clinical-boundary summary

| Boundary the agent enforces | Strength of evidence | Anchor |
|---|---|---|
| Skin cancer is NOT remotely diagnosable; biopsy/in-person dermoscopy required | High — Cochrane meta-analysis + AAD guideline | Dinnes 2018 [2]; Bichakjian 2018 [7] |
| Image-based assessment is empirically inferior to in-person | High — within-review comparison, relative DOR 4.6 | Dinnes 2018 [2] |
| Consumer skin-cancer apps miss cancers (sens. as low as 7%); no FDA approval | High — BMJ systematic review | Freeman 2020 [1] |
| General LLM unsafe as lesion classifier; collapses in darker skin (29–43% melanoma sens.) | Moderate–High — biopsy-confirmed eval | Patel Housley 2025 [10] |
| "Dermatologist-level" CNN claims were on curated biopsy-proven images, not consumer photos | High — primary methods | Esteva 2017 [9] |
| Delay → thicker tumor → worse survival (localized ~100% vs distant ~34%) | High — registry + cohort | SEER 21 [3]; cohort delay literature |
| Common dermatoses have an OTC self-care envelope + a clinician-only layer | High — AAD/consensus guidelines | Reynolds 2024 [4]; Sidbury 2023 [5]; Schaller 2020 [6]; Tynes 2024 [11] |
| No validated DTC skin test (microbiome/IgG/AI-scan) | Moderate–High — regulatory/legal analysis + allergy-society position | Oxford J Law Biosci 2025 [12]; AAAAI |

**Net clinical-boundary rule for the agent:** (1) literacy-level condition education + OTC-vs-clinician category split is permitted; (2) NO lesion diagnosis, NO photo interpretation, NO "probably benign" reassurance — any red-flag (new/changing/non-healing/bleeding/asymmetric/ugly-duckling) → in-person referral; (3) `IMAGE_OR_SIGNAL_INPUT` for skin is REFUSED because lesion classification is regulated SaMD an LLM has not cleared and consumer/LLM accuracy is inadequate and skin-tone-biased; (4) DTC skin-test results are treated as non-evidentiary.

---

## Bibliography

[1] Freeman K, et al. "Algorithm based smartphone apps to assess risk of skin cancer in adults: systematic review of diagnostic accuracy studies." *The BMJ* 2020;368:m127. PMID: 32041693. DOI: 10.1136/bmj.m127. [meta_analysis / regulatory] (Retrieved: 2026-05-31)

[2] Dinnes J, et al. "Dermoscopy, with and without visual inspection, for diagnosing melanoma in adults." *Cochrane Database of Systematic Reviews* 2018, Issue 12: CD011902. DOI: 10.1002/14651858.CD011902.pub2. PMC6517096. [meta_analysis] (Retrieved: 2026-05-31)

[3] National Cancer Institute SEER Program. "Cancer Stat Facts: Melanoma of the Skin" (SEER 21, 2016–2022 5-year relative survival by stage). https://seer.cancer.gov/statfacts/html/melan.html [cohort] (Retrieved: 2026-05-31)

[4] Reynolds RV, Yeung H, Cheng CE, et al. "Guidelines of care for the management of acne vulgaris." *J Am Acad Dermatol* 2024;90(5):1006.e1–1006.e30. PMID: 38300170. DOI: 10.1016/j.jaad.2023.12.017. [regulatory] (Retrieved: 2026-05-31)

[5] Sidbury R, Alikhan A, Bercovitch L, et al. "Guidelines of care for the management of atopic dermatitis in adults with topical therapies." *J Am Acad Dermatol* 2023;89(1):e1–e20. DOI: 10.1016/j.jaad.2022.12.029. [regulatory] (Retrieved: 2026-05-31)

[6] Schaller M, Almeida LMC, Bewley A, et al. "Recommendations for rosacea diagnosis, classification and management: update from the global ROSacea COnsensus 2019 panel." *Br J Dermatol* 2020;182(5):1269–1276. PMID: 31392722. DOI: 10.1111/bjd.18420. PMC7317217. [practitioner_protocol] (Retrieved: 2026-05-31)

[7] Bichakjian CK, Olencki T, Aasi SZ, et al. "Guidelines of care for the management of basal cell carcinoma." *J Am Acad Dermatol* 2018;78(3):540–559. PMID: 29331385. DOI: 10.1016/j.jaad.2017.10.006. [regulatory] (Retrieved: 2026-05-31)

[8] Tsao H, Olazagasti JM, Cordoro KM, et al. "Early detection of melanoma: reviewing the ABCDEs." *J Am Acad Dermatol* 2015;72(4):717–723. PMID: 25698455. DOI: 10.1016/j.jaad.2015.01.025. [mechanism_review] (Retrieved: 2026-05-31)

[9] Esteva A, Kuprel B, Novoa RA, et al. "Dermatologist-level classification of skin cancer with deep neural networks." *Nature* 2017;542(7639):115–118. PMID: 28117445. DOI: 10.1038/nature21056. [open_label] (Retrieved: 2026-05-31)

[10] Patel Housley P, et al. "Performance Evaluation of ChatGPT-4o in Dermatological Diagnoses Across Fitzpatrick Skin Types." *Cureus* 2025. PMID: 40765600. PMC12323556. [cohort] (Retrieved: 2026-05-31)

[11] Tynes BE, et al. "Ketoconazole Shampoo for Seborrheic Dermatitis of the Scalp: A Narrative Review." *Cureus* 2024. PMID: 39310465. PMC11416180. [mechanism_review] (Retrieved: 2026-05-31)

[12] "Is the current regulatory framework for direct-to-consumer microbiome-based tests sufficient to protect consumers from medical, economic, and dignitary harms?" *Journal of Law and the Biosciences* (Oxford) 2025;12(2):lsaf024. PMC12728816. [regulatory] (Retrieved: 2026-05-31)

Supporting (corroborative, NOT counted as the ≥8 admissible primaries):
- AAAAI / EAACI / CSACI position against at-home IgG food/skin "sensitivity" tests (society practitioner guidance). [practitioner_protocol]
- Teledermatology diagnostic-accuracy systematic review/meta-analysis (Frontiers in Medicine 2026; ~76% concordance, image-quality gradient). [meta_analysis]
- Diagnostic-delay / Breslow-thickness cohort series (PMC4979809; MDPI Cancers 2026 screening cohort; COVID-delay Breslow-upstaging series PMC9779520). [cohort]
- *Actas Dermo-Sifiliográficas* Spanish-language dermoscopy series (non-English corroboration only). [anecdote_aggregate]

## Self-check
- **Distinct admissible primaries: 12** ([1]–[12]; anchors present = Freeman BMJ app review [1], Dinnes Cochrane dermoscopy [2], SEER staging-prognosis [3], AAD guidelines [4][5][7], Esteva/Patel Housley AI-accuracy [9][10]).
- **Type-tag coverage:** every numbered claim carries a tag from the exact-set; tags used: meta_analysis, cohort, regulatory, practitioner_protocol, mechanism_review, open_label, anecdote_aggregate (off-whitelist corroboration only).
- **Red-flag boundary evidenced:** YES — not-remotely-diagnosable stated WITH evidence (Dinnes image<in-person relative DOR 4.6 [2]; biopsy-required Bichakjian [7]; SEER localized~100% vs distant~34% [3]; Freeman app sensitivity as low as 7% [1]; Patel Housley LLM 29–43% melanoma sens. in darker skin [10]). No softening to "probably benign" — prohibited output explicitly named.
- **AI/app claims judged on sensitivity/specificity, not marketing:** YES (C.3.1–C.3.3).
- **Population-mismatch / route note:** Esteva [9] curated-biopsy-proven test set ≠ consumer-photo distribution (distribution-mismatch flagged); ISIC skin-tone imbalance flagged as the dark-skin failure mechanism.
- **Non-English survey present:** YES — confirmed-absence of admissible non-English primary recorded; Spanish/Chinese corroboration noted as non-admissible.
- **No Wikipedia, no placeholders:** confirmed. Every primary has a resolvable identifier (PMID/DOI/PMC/URL) verified against its abstract/record.

---

## Post-fix grep audit (iter-2, citation_fidelity remediation of [2] Dinnes 2018)

Re-fetched the Dinnes 2018 Cochrane record (PMC6517096, DOI 10.1002/14651858.CD011902.pub2) and corrected the [2] figures to the verified-as-published values.

| Value | OLD (reported iter-1) | NEW (verified against PMC6517096) |
|---|---|---|
| In-person evaluations | 27 datasets | 26 evaluations |
| In-person lesions | 23,487 | 23,169 |
| In-person melanomas | 1,737 | 1,664 |
| RDOR dermoscopy vs visual inspection (in-person) | 4.8 (95% CI 3.1–7.4) | 4.7 (95% CI 3.0–7.5; P<0.001) |
| RDOR in-person vs image-based | 4.5 (95% CI 2.3–8.5) | 4.6 (95% CI 2.4–9.0; P<0.001) |

Grep command run across the whole artifact (OLD values + OLD CIs):

```
grep -inE '4\.8|23,?487|1,?737|27 dataset|4\.5|2\.3|8\.5|3\.1.{0,2}7\.4' section-C.md
42:### C.2.3 Why delay is harmful — melanoma prognosis by stage
```

**Disposition of the single hit (line 42):** legitimately unchanged. It is the section header `### C.2.3 …`; the regex matched the `2.3` substring inside the heading number "C.2.3", NOT a Dinnes figure. No OLD Dinnes numeric (4.8, 23,487, 1,737, "27 dataset", 4.5, CI 2.3–8.5, CI 3.1–7.4) survives anywhere in the artifact — all return zero hits. Three call sites of the OLD RDOR-4.5 were corrected: C.2.2 body (line 40), C.6 table row "Image-based … inferior" (line 106), and the self-check red-flag line (line 153) — all now read 4.6.

**Other load-bearing numerics re-confirmed against source records (no change needed):**
- Freeman 2020 BMJ [1]: AI-app sensitivity range and SkinVision sensitivity 80% (95% CI 63–92%) / specificity 78% (67–87%) re-confirmed verbatim against PMC7190019; low-sensitivity floor (e.g., MelApp 25–50%; SkinVision pigmented-lesion melanoma revision 88%, 70–98%) consistent. Retained as written.
- SEER 21 (2016–2022) [3]: localized ≈100% / regional ~76% / distant ~34% / all-stages ≈94.7% re-confirmed against the SEER stat-facts record. Retained.
- Patel Housley 2025 Cureus [10]: melanoma sensitivity 100% (FST I–II) vs 29% (FST III–IV) / 43% (FST V–VI) re-confirmed against PMC12323556. Retained.
