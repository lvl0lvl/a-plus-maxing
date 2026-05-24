---
title: "BPC-157 — Canonical Library Entry"
type: research-report
permalink: a-plus-maxing/library/peptides/bpc-157/research-report
status: active
created: 2026-05-23
last_reviewed: 2026-05-23
review_cadence: phase (re-rotate after FDA PCAC July 23-24, 2026 outcome)
research_dispatch_mode: deep
research_question: "Build a goal-agnostic canonical library entry for the peptide BPC-157 per the project's evidence-tier and source-whitelist methodology."
supplementary_layers:
  - vault/library/peptides/bpc-157/practitioner-layer.md (prescribing-practice; compounding pharmacies, named-physician protocols, consensus dose)
  - vault/library/peptides/bpc-157/non-english-layer.md (Croatian/Pliva-era, Chinese, Russian, Korean coverage)
revisions:
  - 2026-05-23 — initial deep-mode dispatch (5 parallel agents A-E)
  - 2026-05-23 — supplementary dispatch added Prescribing-Practice Layer + Non-English Layer; attribution error fixed ([A-11] PK paper: He L 2022 — was misattributed to "Xu et al. 2022"); two new indication signals added (antinociception, psoriasis); one new drug-interaction signal (clopidogrel)
---

# BPC-157 — Canonical Library Entry

## 1. Executive Summary

BPC-157 (Body Protection Compound 157, also PL 14736, PLD-116, bepecin) is a synthetic 15-amino-acid peptide (Gly-Glu-Pro-Pro-Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val; MW ≈ 1419 Da) reported to derive from a fragment of a ~40 kDa protein isolated from human gastric juice. The preclinical literature is large (~150+ rodent in-vivo studies) and consistently positive across musculoskeletal, gastrointestinal, neurological, wound, cardiovascular, and other models. Two structural features dominate the evidence base: (a) ~76-80% of distinct primary studies originate from a single research group (Sikiric and Seiwerth at the University of Zagreb, formerly with Pliva); in-vivo MSK efficacy is 100% Sikiric-affiliated. (b) Published human evidence totals approximately n=31 across three small open-label studies, plus one completed Phase 1 PK/safety registration with no results posted (NCT02637284) and one Phase 2 hamstring trial currently recruiting (NCT07437547). A Pliva-sponsored Phase II ulcerative colitis trial of PL 14736 was completed approximately twenty years ago and has never been primary-published — the single most important evidence-integrity flag for the entire literature. Per the project's evidence-tier methodology, every indication maps to tier **C** (animal/preclinical only with sparse independent replication). Risk-tier is **experimental** (gray-market sourcing dominant, regulatory status restricted across jurisdictions: WADA-banned 2022 S0, TGA Schedule 4 + Appendix D Nov 2023, Medsafe NZ prescription-only May 2023, FDA 503A pathway pending July 2026 PCAC consultation, EU/UK/Canada unapproved).

## 2. How to Use This Entry

This is a goal-agnostic library entry. It documents what is known about BPC-157 across mechanism, pharmacokinetics, indications, dosing, sourcing, regulation, and safety. **It is not a recommendation, a contraindication, or a treatment plan.** Decisions about whether to trial BPC-157, in whom, and at what dose are downstream of this entry and must combine: (a) the operator's profile and goals, (b) the indication-specific evidence-tier per Section 7, (c) the risk-tier of `experimental` (which per `library/methodology/evidence-tiers.md` requires explicit doctor involvement at any risk-tier above `low`), (d) the regulatory posture in the operator's jurisdiction, and (e) an n=1 trial design per `library/methodology/n-of-1-trial-design.md`. When citing from this entry, preserve the type tag attached to each claim — vendor and anecdote sources never ground numerical claims and the report's value depends on that discipline being preserved downstream.

## 3. Identity

| Field | Value | Source |
|---|---|---|
| Common name | BPC-157 (Body Protection Compound 157) | [4, 9] |
| Synonyms | bepecin; PL 14736; PLD-116; PL-10; "stable gastric pentadecapeptide BPC 157" | [9, D-1] |
| Amino acid sequence | Gly-Glu-Pro-Pro-Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val (GEPPPGKPADDAGLV) | [9] |
| Length | 15 amino acids (pentadecapeptide) | [9] |
| Molecular weight | ≈1419 Da | [9] |
| Origin claim | Fragment of a ~40 kDa protein in human gastric juice | [9, A-12] |
| Salt forms in compounding nominations | BPC-157 acetate; BPC-157 free base; BPC-157 arginate (stabilized form) | [D-15, E-23] |
| CAS number | 137525-51-0 (commonly cited for the free peptide) | identity references |
| Regulatory status (synopsis) | Not approved by any major regulator for human use. WADA S0 (2022). TGA Schedule 4 + App D (2023). Medsafe NZ prescription-only (2023). FDA 503A pending PCAC review (July 2026). | Section 15 |

## 4. Evidence Landscape and Concentration Risk

The structural feature of the BPC-157 evidence base is concentration of primary research in a single laboratory.

| Section | Distinct primaries | Sikiric-affiliated | Sikiric share |
|---|---|---|---|
| Mechanism + PK | 14 | 6 | ≈43% |
| MSK (tendon/ligament/muscle/bone) | 12 | 10 | ≈83%; in-vivo specifically 10/10 = 100% |
| Non-MSK indications | 26 | 22 | ≈85% |
| Adverse-effect literature | bulk Sikiric (Xu 2020 is principal independent-ish) | — | high |
| Aggregate (deduped estimate) | ~50 distinct primaries | ~38-40 | ≈76-80% |

The Chang Gung Memorial Hospital / Chang Gung University group in Taiwan (Hsieh, Chang, Tsai, Pang and colleagues) has independently replicated **in-vitro** mechanism findings for VEGFR2-Akt-eNOS angiogenesis, FAK-paxillin tendon-fibroblast migration, GHR upregulation, and Src-Caveolin-1-eNOS vasomotor modulation. These are the most robust mechanism claims in the literature precisely because they have independent replication.

Independent in-vivo replications outside Zagreb (Sikiric) and Taiwan (Chang Gung) are sparse and scattered:
- Veljaca et al. 1994 — Pliva industrial pharmacology — TNBS colitis (animal)
- Xue et al. 2004 — Fourth Military Medical University, China — gastric ulcer (animal)
- Huang et al. 2015 — same Chinese group — alkali-burn wound (animal)
- Keremi et al. 2009 — Hungarian dental group — periodontitis (animal)
- Demirtaş et al. 2025 — Turkish surgery group — skeletal muscle I/R remote organ damage (animal)
- Lee et al. (multiple, 2021/2024/2025) — US, three small open-label human pilots

No independent group has replicated any in-vivo MSK efficacy finding. The single recent independent systematic review (Vasireddi et al. 2025, HSS Journal, n=36 studies through June 2024) explicitly identifies the Sikiric-lab concentration and the absence of controlled human trials as principal limitations of the MSK evidence base [B-7].

**Why this matters for downstream queries:** an indication tier of "C" combined with single-lab concentration is materially different from "C" combined with multi-lab replication. Specialist agents reading this entry should weigh the concentration risk in any decision; this section is the first thing they read.

## 5. Mechanism

### 5.1 Replicated pathways (mechanism described at protein/transcript level, present in independent labs)

- **VEGFR2-Akt-eNOS angiogenesis axis.** BPC-157 increases VEGFR2 expression and internalization in HUVECs, activating downstream Akt and eNOS phosphorylation; in a rat hind-limb ischemia model, histology confirmed increased vascular density and elevated VEGFR2 expression. [A-1, in_vitro + animal] Hsieh et al. 2017, Chang Gung Memorial Hospital — non-Sikiric.
- **FAK-paxillin pathway in tendon fibroblasts.** BPC-157 accelerated tendon explant outgrowth ex vivo, improved fibroblast survival under H2O2 stress, increased transwell migration, and produced phosphorylation of focal adhesion kinase and paxillin with F-actin reorganization. [A-2, in_vitro + ex_vivo animal] Chang et al. 2011, Chang Gung — non-Sikiric.
- **Growth hormone receptor (GHR) upregulation in tendon fibroblasts.** Dose- and time-dependent (0.1–0.5 µg/mL) increase in GHR mRNA and protein; pretreatment sensitized cells to growth-hormone-driven proliferation. [A-3, in_vitro] Chang et al. 2014, Molecules — non-Sikiric.
- **Src-Caveolin-1-eNOS vasomotor pathway.** In isolated rat aorta, BPC-157 modulated vasomotor tone concentration- and NO-dependently with activation of Src and Cav-1 phosphorylation upstream of eNOS. [A-7, in_vitro animal tissue] Hsieh et al. 2020, Sci Rep — non-Sikiric.

### 5.2 NO-system bidirectional modulation (Sikiric-only, mechanistically partially supported)

- Co-administration studies show BPC-157 preserves stomach mucosa integrity and blood pressure regardless of whether NO synthesis is blocked (L-NAME) or substrate-loaded (L-arginine); effect is bidirectional rather than agonist-like. [A-4, animal] Sikiric et al. 1997. Replicated across many Sikiric-lab papers; the Chang Gung Src-Cav-1-eNOS work [A-7] provides partial mechanistic support but uses different assays.

### 5.3 Hypothesized / under-investigation

- **ERK1/2 and Egr-1 / NAB2 / JAK-2 transcriptional cascades** — proposed explanation for therapeutic effects outlasting the <30 min plasma window. Asserted in Sikiric-group reviews; primary single-pathway papers sparse. [A-5, mechanism_review]
- **Dopamine-system interactions.** Counteraction of haloperidol-induced catalepsy and gastric lesions from complete dopamine-system failure; described as "modulatory" — no published receptor binding assay. [A-8, animal]
- **Serotonin-system interactions.** Reduces severity of serotonin syndrome in rats; mechanism unspecified beyond behavioral counteraction. [A-8, animal]
- **Brain-gut axis / vagal mediation.** Persistence of effect after vagotomy is inconsistent across Sikiric-group reports. [A-10, mechanism_review]

### 5.4 No identified canonical receptor

Despite ~30 years of research, no specific membrane receptor has been identified. Observed effects are described as pleiotropic / multi-pathway. [A-9, mechanism_review] Vasireddi et al. 2025.

### 5.5 Open mechanism questions

1. What is the proximal molecular target/receptor?
2. How does a peptide with t½ <30 min produce effects lasting days-weeks (gene-expression cascade timing, epigenetic effects, metabolite contributions)?
3. Are the angiogenic and migration effects driven by the same upstream event or independent?
4. Is dopamine/serotonin counteraction mediated centrally, or secondary to gut/vagal pathways?
5. Are NO-modulatory effects direct (binding to a NOS regulator) or downstream (e.g., via Src-Cav-1)?
6. Why has no third lab (outside Zagreb and Chang Gung) replicated the mechanism findings?

## 6. Pharmacokinetics

The single dedicated multi-route PK paper is He et al. 2022, *Frontiers in Pharmacology* (DOI 10.3389/fphar.2022.1026182, PMC9794587) [A-11] — non-Sikiric (Fourth Military Medical University Department of Biopharmaceutics, China). *Attribution corrected 2026-05-23 from "Xu et al."; co-author overlap (Zhang, Li) ties the group to Xue 2004 [C-4] and Huang 2015 [C-17].* All multi-species/multi-route PK numbers below derive from that paper unless noted. Flagged as `open-access lower-trust` per the project whitelist, but it is the only dedicated multi-route study in the published literature.

### 6.1 By route

| Route | Species | Half-life | Bioavailability | Notes |
|---|---|---|---|---|
| IV | Rat | t½ ≈ 15.2 min (single 20 µg/kg) | 100% (reference) | Linear PK across dose range |
| IV | Beagle dog | t½ ≈ 5.27 min (6 µg/kg) | 100% (reference) | Linear PK |
| IM | Rat | <30 min across all dose levels | ≈14–19% absolute (vs IV) | Tmax ~9 min; 7-day 100 µg/kg/day: no major accumulation |
| IM | Beagle dog | <30 min | ≈45–51% absolute | Species gap large and unexplained |
| subQ | — | — | — | **No admissible primary evidence.** Route widely used in rodent efficacy studies (typical 10 µg/kg/day) and in practitioner protocols, but He 2022 covered only IV and IM |
| Oral | — | — | — | **Disputed.** See 6.2 |
| Intranasal | — | — | — | **No admissible primary evidence.** Cited only in vendor/practitioner copy |
| Sublingual | — | — | — | **No admissible primary evidence** |
| Topical | — | — | — | Applied in rat skin/burn/eye-injury models; no published systemic-absorption PK |

### 6.2 Oral bioavailability — disputed

The originator group states BPC-157 is "not destroyed in human gastric juice for more than 24 h," citing in-vitro incubation experiments from their own earlier work [A-12, mechanism_review] (Sikiric et al. 2020, PMC7096228; restated in PMC11053547, 2024). The Sikiric-group oral-dosing rationale rests on this claim.

Independent reviews of oral peptide delivery treat peptide survival of gastric acid + pepsin + intestinal peptidases as the dominant barrier to oral peptide bioavailability and do not list BPC-157 as a documented exception [A-13, mechanism_review] (Brown et al. 2025, PMC12030352). The 2025 HSS Journal narrative review notes the >24h gastric stability claim is sourced primarily to Sikiric-group assays and that independent replication of oral systemic bioavailability is absent [A-9, mechanism_review] (Vasireddi et al. 2025). **No quantified oral %F has been published in any species.** Rat drinking-water dosing (0.16 µg/mL ≈ ~10 µg/kg/day) is widely reported as efficacious, but PK was not measured.

### 6.3 Stability

- **In gastric juice (in vitro):** Sikiric-group claim >24 h stability in human gastric juice. No independent replication. [A-12, in_vitro]
- **In plasma (in vivo):** very short — prototype t½ <30 min in rats and dogs across all routes tested. [A-11, animal]
- **Lyophilized:** ~24-36 months sealed at -20 °C per vendor specifications. No independent peer-reviewed stability dossier. [D-13, D-14, vendor_label]
- **Reconstituted in bacteriostatic water:** ~4 weeks at 2-8 °C per vendor/community heuristic; avoid freeze-thaw. No independent peer-reviewed stability dossier. [D-14, vendor_label]

### 6.4 Metabolism / clearance

- Excretion via urine and bile, per [3H]-labeled rat tracer study. [A-11, animal] Confirmed in editorial summary [A-14, mechanism_review].
- Rapid proteolytic degradation consistent with general short-peptide PK; no named CYP pathway (peptide, not small molecule).
- Wide tissue distribution per He 2022.

### 6.5 PK-PD disconnect (open question)

All admissible PK shows t½ <30 min; plasma returns to baseline within 24 h. Animal efficacy studies routinely report effects persisting days, weeks, or up to 360 days after single-dose treatment. The proposed reconciliation — that BPC-157 triggers durable gene-expression cascades within minutes — is **not directly demonstrated by any PK-PD time-matched study**. This is the central unresolved PK question. [A-9, mechanism_review]

## 7. Evidence Base by Indication

Every indication subsection below maps to evidence-tier **C** per `library/methodology/evidence-tiers.md` (animal/preclinical only, with sparse independent replication, or single uncontrolled human case series at best). Tier justifications appear at the end of each subsection.

### 7.1 MSK — Tendon

- **Strongest evidence:** Staresinic et al. 2003, *J Orthop Res* 21:976-983, PMID 14554208 [B-1, animal]. Rat Achilles transection 5 mm proximal to calcaneal insertion. 10 µg/kg, 10 ng/kg, or 10 pg/kg BPC-157 i.p. once daily; first dose 30 min post-op. Biomechanical (load to failure, Young's modulus), Achilles Functional Index, histology, macroscopy assessed days 1, 4, 7, 10, 14. "Fully improves recovery" across all endpoint families vs saline controls who showed "severely compromised healing." In-vitro reversed 4-HNE inhibition of cultured tendocyte growth. Sikiric lab.
- **Other primaries:** Krivic 2006 (Achilles detachment to bone, AFI improvement through day 21; opposed methylprednisolone aggravation) [B-2, animal]; Krivic 2008 (n=72 Wistar, Achilles-to-bone transection, AFI improvement, MPO and inflammatory-cell reduction, vascular index increase) [B-3, animal]; Chang 2011 (in-vitro tendon-fibroblast outgrowth/migration/FAK-paxillin) [B-4, in_vitro, **non-Sikiric Chang Gung**]; Tsai/Pang 2018 (in-vitro GHR upregulation) [B-5, in_vitro, **non-Sikiric Chang Gung**].
- **Independent systematic review:** Vasireddi et al. 2025 (PRISMA, 36 studies through June 2024) confirms tendon biomechanical/structural improvements across preclinical models and notes Sikiric-lab dominance. [B-7, mechanism_review]
- **Human evidence:** Lee & Padgett 2021 (PMID 34324435) — uncontrolled retrospective chart review of intra-articular knee injection, n=16, mixed knee pain etiologies (not tendon-specific). 87.5% subjective pain relief at 6-12 mo; no objective tendon imaging endpoint. [B-19, open_label]
- **Counter-evidence:** No null/negative animal studies located in admissible literature.
- **Evidence tier: C** — animal/preclinical with the only human datum being a single uncontrolled retrospective chart review with subjective endpoints. Tendon is the canonical "BPC-157 → tendon healing (mostly rodent)" example in `evidence-tiers.md`.

### 7.2 MSK — Ligament

- **Strongest evidence:** Cerovecki et al. 2010, *J Orthop Res* 28(9):1155-1161, PMID 20225319 [B-8, animal]. Rat MCL transection. 10 µg/kg or 10 ng/kg i.p. once daily, OR 1.0 µg local in distilled water. Biomechanical + microscopic + macroscopic improvement vs saline controls; systemic and local routes comparable. Sikiric lab.
- **Other primaries:** None. Bechara 2025 [B-10] and Vasireddi 2025 [B-7] reviews recapitulate Cerovecki — no additional ligament primaries identified.
- **Human evidence:** None.
- **Counter-evidence:** None located.
- **Evidence tier: C (leaning C-low)** — entire ligament case rests on a single Sikiric-lab paper. No independent replication. No human data.

### 7.3 MSK — Muscle

- **Strongest evidence:** Staresinic et al. 2006, *J Orthop Res* 24(5):1109-1117, PMID 16609979 [B-11, animal]. Complete rat quadriceps transection (defect does not compensate spontaneously in controls). 10 µg/kg, 10 ng/kg, or 10 pg/kg i.p. once daily; first dose 30 min post-transection. Sustained functional restoration through 72 days vs uncompensated control defect. Sikiric lab.
- **Other primaries:** Novinscak 2008 (rat gastrocnemius crush) [B-12, animal]; Mihovil 2009 (denervated gracilis) [B-13, animal]; Pevec 2010 (corticosteroid-impaired healing reversed) [B-14, animal]; Matek 2025 (per-oral BPC-157 muscle-to-bone reattachment after surgical detachment) [B-15, animal]. All Sikiric or Sikiric-affiliated.
- **Human evidence:** None muscle-specific.
- **Counter-evidence:** None located.
- **Evidence tier: C** — entirely rodent, entirely Sikiric. Multiple injury models (transection, crush, denervation, corticosteroid-impaired, muscle-to-bone) converge but do not substitute for human or independent-lab evidence.

### 7.4 MSK — Bone

- **Strongest evidence:** Sebecic et al. 1999, *Bone* 24(3):195-202, PMID 10071911 [B-17, animal]. Rabbit 0.8 cm segmental osteoperiosteal defect in left radius (incompletely healed in all saline controls at 6 weeks). 10 µg/kg local percutaneous OR i.m. (intermittent days 7/9/14/16 OR continuous days 7-21 at 10 µg or 10 ng/kg). Active comparators: autologous bone marrow + autologous cortical graft. BPC-157 i.m. 14 days at 10 µg/kg or 10 ng/kg, or local, produced healing comparable to bone marrow or autologous cortical graft. Callus surface roughly 2x control by 2 weeks. Sikiric lab.
- **Other primaries:** None bone-specific. Vasireddi 2025 [B-7] and Bechara 2025 [B-10] restate Sebecic.
- **Human evidence:** None.
- **Counter-evidence:** None located.
- **Evidence tier: C (leaning C-low)** — single rabbit study, single Sikiric lab, no independent replication, no human data. Methodologically the strongest single MSK animal study (radiographic + histomorphometric + active-comparator), but n=1 study at the bibliographic level.

### 7.5 GI / Ulcer / IBD / Esophageal

GI is the historical core of the BPC-157 program. The peptide was isolated from human gastric juice [C-1, mechanism_review] and developed by Pliva (Croatia) as PL 14736 / PLD-116 specifically for ulcerative colitis. Animal evidence spans gastric ulcer, NSAID/ethanol/restraint cytoprotection, colitis (cysteamine, TNBS), short bowel syndrome, anastomosis/fistula healing, and esophagitis.

- **Strongest preclinical evidence:** Xue et al. 2004, *World J Gastroenterol* 10(7):1032-1036 [C-4, animal, **non-Sikiric** — Fourth Military Medical University, China] — acute and chronic gastric ulcer in rats, BPC-157 i.p. dose-dependent reduction in ulcer area; Sikiric et al. 1996, *Dig Dis Sci* 41:1604-1614 [C-2, animal] — rat, 10 µg/kg and 10 ng/kg i.p., cytoprotection across restraint/ethanol/indomethacin/capsaicin models; Veljaca et al. 1994, *J Pharmacol Exp Ther* 272:417-422 [C-3, animal, **non-Sikiric** — Pliva industrial pharmacology] — TNBS colitis; Klicek et al. 2013 [C-6, animal] — cysteamine-colitis + colon-colon anastomosis, BPC-157 healed vs sulfasalazine (moderate) and methylprednisolone (worsened); Klicek et al. 2008 [C-5, animal] — colocutaneous fistula closure as PL 14736.
- **Clinical trial program (PL 14736):**
  - Veljaca et al. — Phase I rectal PL 14736 in healthy male volunteers, "safe and well tolerated" [C-11, open_label] — abstract only; no widely-available primary publication.
  - **PL 14736 Phase II multicenter randomized double-blind placebo-controlled enema study in mild-to-moderate UC** (Pliva sponsor). Cited in Klicek 2008 reference list and Karger book chapter. **Full results never published in a major peer-reviewed journal as a standalone trial report.** [C-12, rct — unpublished]
  - NCT02637284 (PharmaCotherapia, Phase 1 healthy-volunteer safety/PK; completion 2016; no results posted) [C-13, regulatory/registry]
  - NCT07437547 (Hudson Biotech, Phase 2 hamstring; recruiting; est. completion 2028) [C-14, regulatory/registry]
- **No completed, peer-reviewed Phase II/III BPC-157 trial in any GI indication has published efficacy results in a Tier 1 journal as of May 2026.**
- **Evidence tier: C.** Large rodent literature with consistent direction of effect but >80% from Sikiric lab; PL 14736 reached Phase II ~20 years ago and was never primary-published.

### 7.6 Wound Healing (skin, surgical anastomosis)

- **Strongest evidence:** Huang et al. 2015, *Drug Des Devel Ther* [C-17, animal, **non-Sikiric** — Fourth Military Medical University] — alkali-burn rat model, topical BPC-157, accelerated wound closure, better granulation, re-epithelialization, dermal remodeling, increased collagen at day 18.
- **Other primaries:** Mikus et al. 2001 (Sikiric lab) — burn-wound healing in mice with BPC-157 outperforming silver sulfadiazine in some endpoints [C-16, animal]; Tkalcevic 2007 (Pliva) — granulation/collagen organization with egr-1 mechanism [C-18, animal]; Bilic 2005 (CO2 laser wound) [C-19, animal]. Anastomosis: ileoileal (Vuksic 2007 [C-7]), esophagogastric (Djakovic 2016 [C-10]) — all Sikiric.
- **Human evidence:** None. No registered or published human wound-healing trial.
- **Evidence tier: C** — consistent rodent burn/skin/anastomosis data with one independent replication (Huang 2015). Zero human data.

### 7.7 Neuroprotection / TBI / Nerve / Spinal

- **Strongest evidence:** Tudor et al. 2010, *Regul Pept* [C-20, animal] — closed-head TBI in mice, BPC-157 reduced mortality and injury scores at 10 µg/kg and 10 ng/kg. Perovic et al. 2019, *J Orthop Surg Res* 14:199 [C-21, animal] — rat compression spinal cord injury, BPC-157 10 µg/kg i.p. restored motor function vs persistent paralysis in controls. Vukojevic 2020 [C-22, animal] — hippocampal I/R, reduced neuronal damage. Gjurasin 2010 [C-23, animal] — rat sciatic nerve transection, improved EMG and axonal regeneration. Klicek 2013 [C-6, animal] — cuprizone (MS demyelination model) motor disability counteracted.
- **Human evidence:** None registered or published.
- **Evidence tier: C** — multiple rodent models (TBI, SCI, sciatic, hippocampal I/R, cuprizone) consistently positive; effectively all Sikiric or close collaborators. No human evidence.

### 7.8 Cardiovascular

- **Strongest evidence:** Sikiric et al. 2022, *World J Gastroenterol* 28(1):23-46 [C-24, animal] — rat major-vessel (vena cava, portal vein, mesenteric) occlusion; BPC-157 recruited collateral circulation, reduced multiorgan-failure markers; Pringle maneuver I/R and Budd-Chiari models. Barisic et al. 2013 [C-26, animal] — mortal hyperkalemia in rats, BPC-157 life-saving via NO system. Konosic et al. 2019 [C-27, animal] — aspirin/clopidogrel/cilostazol + BPC-157, platelet aggregation and clot modulation without coagulation cascade disturbance.
- **Other:** Sikiric 2022 [C-25, mechanism_review] — comprehensive review summarizing ~40+ rodent studies across MI, arrhythmia, thrombosis, HF, pulmonary HT models. Demirtaş 2025 [C-28, animal, **non-Sikiric, Turkish**] — skeletal-muscle I/R with remote organ damage (kidney, liver, lung) protected.
- **Human evidence:** None.
- **Evidence tier: C** — rodent-only, heavy Sikiric dominance; breadth across CV models; one recent independent replication.

### 7.9 Other (Liver / Kidney / Eye / Periodontal / Pancreas)

- **Liver:** Ilic 2009 (insulin-overdose multiorgan rescue) [C-30, animal]; Sikiric ~2010 paracetamol-induced acute hepatic failure (5 g/kg i.p. paracetamol; BPC-157 reduced AST/ALT, hyperammonemia, seizures, mortality whether prophylactic or 3 h after) [C-31, animal]; CCl4 hepatotoxicity protection in earlier Sikiric work.
- **Kidney:** Demirtaş 2025 [C-28, animal, non-Sikiric] — remote-organ kidney damage from hindlimb I/R attenuated.
- **Eye:** Lazic 2015 [C-32, animal] — rat perforating corneal injury, 2 µg and 2 ng BPC-157 eye drops accelerated corneal healing, fluorescein/Seidel turned negative at 24 h, aqueous cell clearance by 96-120 h. Kralj 2021 [C-33, animal] — retinal ischemia from retrobulbar L-NAME (Frontiers — flagged).
- **Periodontal:** Keremi 2009 [C-29, animal, non-Sikiric Hungarian] — ligature-induced periodontitis, chronic BPC-157 10 µg/kg reduced gingival inflammation, alveolar bone loss (microCT), blood-flow disturbances.
- **Pancreas:** Multiple Sikiric-lab studies — cerulein-induced acute pancreatitis and bile-duct-ligation pancreatitis attenuated.
- **Evidence tier (collectively): C.**

### 7.10 Anti-inflammatory (downstream, brief)

Anti-inflammatory effect (myeloperoxidase reduction, TNF-α and IL-6 downregulation) is downstream of essentially every model surveyed in 7.5-7.9 and is reported consistently. It has never been studied as a standalone human indication. Tier C by inheritance from the underlying models.

### 7.12 Pain / Nociception (Korean primaries, added 2026-05-23 supplementary dispatch)

- **Strongest evidence:** Park et al. 2021, *Kosin Medical Journal* 36(1):1-13 [NE-13, animal]. Rat formalin-test pain model with immunohistochemistry. First study of BPC-157 in a nociception model. Korean authors (Department of Anesthesiology and Pain Medicine, Dong-A University). DOI 10.7180/kmj.2021.36.1.1. http://www.kosinmedj.org/journal/view.php?doi=10.7180%2Fkmj.2021.36.1.1
- **Partial replication:** Jung et al. 2022, *Journal of Dental Anesthesia and Pain Medicine* 22(2):97, PMC8995671 [NE-14, animal]. Korean follow-up using incisional (post-surgical) pain model rather than formalin. Within-group partial replication.
- **Human evidence:** None.
- **Evidence tier: C** — animal-only, single research line (Korean), within-group replication across two pain models. Independent of the Sikiric corpus.

### 7.13 Dermatology / Anti-inflammatory skin (signal — added 2026-05-23 supplementary dispatch)

- **Signal:** Vraneš et al. 2023, *Liječnički vjesnik* 145(Supp 2):44 [NE-1, in_vitro conference abstract]. In-vitro keratinocyte study; BPC-157 inhibited pro-inflammatory effects of IL-17A on keratinocytes. Croatian conference abstract; not yet full peer-reviewed paper. New psoriasis-relevant signal not previously in indication map.
- **Evidence tier: C (low, signal-only)** — single in-vitro conference abstract; no follow-up paper yet located. Flagged for future-work tracking.

### 7.14 Updated MSK porcine corroboration (added 2026-05-23 supplementary dispatch)

- Section 7.6 (Wound healing) is extended: Xue et al. 2004b, *Chinese Journal of New Drugs* 13:602-605 [NE-9, animal] — porcine ("small type pigs") skin-cut wound model from the Fourth Military Medical University group. Distinct second Xue-group 2004 paper from the WJG gastric ulcer paper currently cited as [C-4]. Provides **larger-animal corroboration** of the rodent skin-wound work, which strengthens the wound-healing case marginally above other tier-C indications.

### 7.11 Summary table — evidence tier by indication

| Indication | Evidence tier | Independent replications |
|---|---|---|
| Tendon | C | In-vitro only (Chang Gung) |
| Ligament | C-low | None |
| Muscle | C | None (in-vivo) |
| Bone | C-low | None |
| GI / IBD / ulcer | C | 2 (Veljaca 1994 Pliva, Xue 2004 China) |
| Wound healing | C | 1 (Huang 2015 China) |
| Neuroprotection | C | None |
| Cardiovascular | C | 1 (Demirtaş 2025 Turkey) |
| Liver / Kidney / Eye / Pancreas | C | 1 (Demirtaş 2025 kidney) |
| Periodontal | C | Keremi 2009 itself is the independent (Hungarian) |
| Anti-inflammatory | C | Inherited from above |
| Pain / nociception (added 2026-05-23) | C | Korean within-group only (Park 2021, Jung 2022) |
| Dermatology / psoriasis (signal, added 2026-05-23) | C-low (signal) | Single Croatian conf abstract |

## 8. Dose and Protocol Conventions

### 8.1 Literature reference doses (rodent IP/SC — workhorse)

The Sikiric "high/medium/low" dosing triplet appears across most rodent efficacy work [D-5, D-6, animal]:

- **10 µg/kg** (high)
- **10 ng/kg** (medium)
- **10 pg/kg** (low)

Administration is most commonly daily i.p. (rodent route, not used in humans) or SC. Effects are reported across the full three-log dose range in many models — interpreted by the Sikiric group as evidence of a flat dose-response curve, which is also a feature often associated with assay artifacts (open question).

### 8.2 PK-validated rodent/canine doses (He 2022 [D-4, animal])

- Rats IV: 20 µg/kg single
- Rats IM: 20 / 100 / 500 µg/kg single; 100 µg/kg/day × 7 days
- Beagles IV: 6 µg/kg single
- Beagles IM: 6 / 30 / 150 µg/kg single; 30 µg/kg/day × 7 days
- Linear PK across the studied dose ranges in both species.

### 8.3 Practitioner protocols (compounding pharmacy data sheets, Tier 3)

Tailor Made Compounding's peptide catalog suggests **"inject 0.25 mL SC once daily for 20 days"** of a reconstituted BPC-157 vial, plus a 375 mg oral capsule format dosed daily [D-10, compounding_data_sheet]. Translating 0.25 mL of a standard 5 mg / 2 mL reconstitution yields **~625 µg/dose**, which scales to roughly **8-10 µg/kg in an 80 kg adult** — within the rodent 10 µg/kg literature reference when scaled mg/kg with no inter-species allometric adjustment. Many practitioner clinic protocols cite **250-500 µg SC once or twice daily for 4-6 weeks**; these dose figures are not supported by Tier 1 human studies.

### 8.4 Cycle conventions

- Animal: single-dose to 90-day daily, depending on injury model [D-3, mechanism_review].
- Practitioner: commonly **4-week on / 4-week off** or **20-30 day** cycles.
- **No human cycle-length evidence.**

### 8.5 Route conventions

- **Systemic SC** dominates practitioner use; **local SC near lesion** (e.g., peri-tendinous to an injured Achilles) is described by clinic protocols.
- Animal data support local administration at similar µg/kg doses to systemic [D-3, mechanism_review].
- **No human comparative data** for systemic vs local routing.

### 8.6 Literature vs practitioner gap (named flag)

The gap between literature-validated doses (rodent µg/kg) and practitioner doses (absolute µg/dose extrapolated by mg/kg) is the principal dose-uncertainty in the field. Human PK studies that would justify a specific human SC dose do not exist.

## 9. Reconstitution

Standard supplied form: **5 mg lyophilized powder per vial** (also sold as 10 mg) [D-11, D-12, vendor_label]. Diluent: **bacteriostatic water (0.9% benzyl alcohol)**, typical 2 mL for a 5 mg vial [D-11, D-13, vendor_label]. Resulting concentration: **2.5 mg/mL = 2,500 µg/mL = 25 µg per U-100 unit**.

### 9.1 U-100 insulin-syringe conversion (5 mg / 2 mL standard reconstitution)

| Target dose | Volume | U-100 units |
|---|---|---|
| 100 µg | 0.04 mL | 4 |
| 200 µg | 0.08 mL | 8 |
| 250 µg | 0.10 mL | 10 |
| 500 µg | 0.20 mL | 20 |
| 625 µg | 0.25 mL | 25 |
| 1000 µg | 0.40 mL | 40 |

### 9.2 Alternate reconstitutions

- **5 mg / 1 mL** → 5 mg/mL → 50 µg per U-100 unit (halves unit count for each target dose)
- **5 mg / 5 mL** → 1 mg/mL → 10 µg per U-100 unit (fine-grained dosing)

### 9.3 Storage

- **Lyophilized:** -20 °C long-term; refrigerated short-term acceptable; ~24-36 months sealed [D-13, D-14, vendor_label].
- **Reconstituted:** 2-8 °C refrigerated; use within ~4 weeks; avoid freeze-thaw cycles [D-14, vendor_label].
- **There is no independent peer-reviewed stability study** for BPC-157 reconstituted in bac water. The "4 weeks" figure is a vendor/community heuristic, not a regulatory stability dossier.

## 10. Adverse Effect Profile

### 10.1 Human evidence

Total formally studied n ≈ 31 across three small open-label studies, plus an unpublished Pliva Phase I (Veljaca volunteer abstract) and an unpublished Phase II UC (PL 14736).

- **Lee & Burgess 2025 — IV pilot, n=2 healthy adults** [E-1, open_label]. Day 1: 10 mg BPC-157 in 250 mL saline IV over 1 h; Day 2: 20 mg in 250 mL saline IV over 1 h. Monitoring: CMP, CBC, CPK + isoenzymes, BNP, TSH, RBC indices, vitals. **No AEs reported**; no clinically meaningful changes; plasma returned to baseline within 24 h. **n=2 and both subjects had received IV BPC-157 prior** (selection bias).
- **Lee et al. 2024 — intravesicular instillation for interstitial cystitis, n=12** [E-2, open_label]. Screening for fever, rash, nausea, vomiting, worsening urinary symptoms, dyspareunia, hematuria, acute cystitis. **0/12 screened AEs.**
- **Lee & Padgett 2021 — intra-articular knee, n=17** [E-3, open_label]. No AEs reported; **no systematic AE screening protocol described** — absence-of-evidence caveat applies.
- **PL 14736 / PLD-116 (Pliva) IBD trials** — described in Sikiric narrative reviews as "phase II UC, well-tolerated, no SAEs" [E-4, E-5, mechanism_review]. **The phase II results have not been independently published in a peer-reviewed primary source** publicly retrievable; the safety claim is sponsor- and Sikiric-attributed. The 2026 FDA PCAC agenda lists BPC-157 for review with "ulcerative colitis" as the evaluated use — implying the PL 14736 data package was submitted but has not been finalized by FDA [E-6, regulatory].

**No published case reports of serious adverse events from research-chemical use have been located in PubMed as of search date (2026-05).**

### 10.2 Animal evidence

- **Xu et al. 2020 (preclinical safety eval, the canonical paper)** [E-8, animal]. Single-dose toxicity in mice, rats, rabbits, dogs. **Minimum toxic dose and lethal dose could not be identified** at the doses tested. No teratogenicity, no genotoxicity, no anaphylaxis, no local toxicity. Repeated-dose toxicity in rats and dogs: same. Limit test of 2 g/kg i.v. or i.g. without adverse effects cited in Sikiric reviews [E-5, mechanism_review].
- **LD50: not formally reportable** — neither Xu et al. nor Sikiric corpus reached an LD50. "No LD50" reflects testing limits (highest doses given, no deaths), not proven absence of an LD50.
- **Organ-specific toxicity signals:** none reported across the typical organ panel (heart, liver, kidney, brain, GI). Consistent across the literature.

### 10.3 The "no toxicity" caveat (load-bearing)

The Sikiric group has published the bulk of the BPC-157 corpus (hundreds of papers) and is the strongest advocate of the "complete absence of toxicity" framing. Many of these papers test 10 ng/kg and 10 µg/kg only — doses orders of magnitude below typical research-chemical user injection doses (250-500 µg/day ≈ 3-7 µg/kg in a 70-kg human). The "no toxicity" finding is therefore **dose-narrow and group-narrow; independent replications outside the Sikiric lab are limited.** Xu 2020 is the principal independent-ish safety paper but is also from a synthesis lab advocating IND.

### 10.4 Theoretical concerns

#### Cancer / tumor / proliferation
- Mechanism basis: BPC-157 upregulates VEGFR2 expression and internalization, activates VEGFR2-Akt-eNOS signaling, promotes angiogenesis in CAM and tube-formation assays, increases blood-flow recovery in hindlimb ischemia [E-10, E-11, mechanism_review; animal/in_vitro]. VEGF/VEGFR2 signaling is a primary tumor-angiogenesis pathway expressed in ≈50% of human cancers studied (ovarian, melanoma, thyroid, etc.) [E-12, mechanism_review]. EGR-1 (also upregulated by BPC-157) implicated in prostate cancer angiogenic/osteoclastogenic factors and metastasis [E-13, mechanism_review]. Vasireddi 2025 "Regeneration or Risk?" explicitly catalogs pathologic angiogenesis, NO overproduction, and proline-metabolite-mediated oxidative cascades as the three principal theoretical AE channels [E-2, mechanism_review].
- Tumor-model studies:
  - **Radeljak, Seiwerth, Sikiric 2004 (in vitro)** [E-14, in_vitro] — BPC-157 inhibited cell growth and VEGF signaling via MAPK in a human melanoma cell line. Conference abstract; not a full peer-reviewed paper.
  - **Kang et al. 2018 (in vivo)** [E-15, animal] — BPC-157 in C26 colon adenocarcinoma-bearing mice (cancer cachexia model). Attenuated cachexia (reduced IL-6, TNF-α, preserved body weight); did NOT produce meaningful tumor size reduction; also did NOT produce meaningful tumor acceleration at tested doses. One tumor cell line in one species.
- Literature consensus: Sikiric interprets the in-vitro melanoma data + absent corneal neovascularization promotion as evidence of "angiogenesis-modulatory" rather than "angiogenesis-driving" effect [E-16, mechanism_review]. Non-Sikiric reviewers (Vasireddi 2025, Józwiak 2025) characterize the **cancer-risk question as open** because (a) only one tumor-bearing in-vivo model published, (b) the in-vitro anti-tumor signal is single-source and old, (c) human safety surveillance does not exist [E-2, E-12, mechanism_review].

#### Coagulation
- BPC-157 reduced bleeding time and reversed thrombocytopenia after amputation in rats treated with heparin, warfarin, aspirin, L-NAME, or L-arginine [E-19, E-20, animal]. Counteracted aspirin/clopidogrel/cilostazol inhibition of platelet aggregation activated by arachidonic acid, ADP, collagen, ristocetin — without itself disturbing coagulation pathways [E-21, animal]. Reviews summarize as "maintains thrombocyte function" rather than pro-coagulant per se [E-5, mechanism_review].
- **Practical implication:** in patients on therapeutic anticoagulation, BPC-157 may functionally antagonize the antithrombotic intent. Animal-only evidence; no human PK/PD interaction studies.

#### Immune
- Described as modulating multiple immune functions in the gut and participating in "immune homeostasis" [E-22, mechanism_review]. Downregulates TNF-α and IL-6 in multiple inflammation models [E-15, E-22, animal]. No published evidence of immunosuppression sufficient to predispose to infection; no published evidence of autoimmune flare induction; **no targeted human immunogenicity studies.** Lutchman 2025 calls out **immunogenicity monitoring** as an outstanding need for peptide therapeutics including BPC-157 [E-23, mechanism_review].

#### Pregnancy / lactation
- **No human pregnancy or lactation data.** Xu 2020 reported no embryo-fetal toxicity, no teratogenicity in animal reproductive toxicology [E-8, animal]. No FDA pregnancy category (not an approved drug). Default precautionary recommendation in narrative reviews: avoid in pregnancy and lactation.

#### Pediatric
- **No pediatric data exist in any species or any indication.** No safety or efficacy basis for use under 18.

### 10.5 Anecdote-derived patterns (qualitative, no rates)

The following AE PATTERNS appear in user-aggregate Tier 5 sources [E-34, E-35, E-36, anecdote_aggregate]. **Numerical incidence rates from these sources are inadmissible and not reproduced.** Patterns reported across r/bpc_157, r/Peptides, r/TBI, r/eds, and peptide-user forums:
- **Injection-site reactions** — local swelling, itching, induration, sometimes after multiple symptom-free days (sensitization pattern)
- **Fatigue, lethargy, "brain fog," lack of motivation** following dosing initiation
- **Anhedonia / mood blunting / depressive shift** — distinct subset reports loss of pleasure; consistent enough across reports to flag for monitoring; mechanistic basis unestablished but possibly serotonergic given animal dopamine/serotonin modulation
- **Acute anxiety, dizziness, panic-attack-like episodes** shortly after injection — described as transient but jarring
- **"Growing pains" / ache during reported regenerative periods**
- **Transient nausea and headache** — typically with injectable forms

These patterns suggest empirical screening targets for any future human safety study; they are not a basis for incidence estimates.

## 11. Drug / Compound Interactions

- **NSAIDs (ibuprofen, diclofenac, indomethacin, naproxen, aspirin):** BPC-157 protects against NSAID-induced gastric, intestinal, liver, and brain lesions in rats; stabilizes intestinal permeability; enhances cytoprotection [E-24, animal; E-25, mechanism_review; E-26, animal]. Most consistently documented "interaction" — Sikiric framing is "use case" not contraindication. Human relevance untested.
- **Anticoagulants / antiplatelets (heparin, warfarin, aspirin, clopidogrel, cilostazol):** BPC-157 functionally antagonizes the antithrombotic effect on platelet aggregation and bleeding time in rats [E-19, E-20, E-21, animal]. Adverse interaction in any patient who NEEDS therapeutic anticoagulation (mechanical valve, recent VTE, AFib with high stroke score).
- **Clopidogrel-induced gastric injury (added 2026-05-23):** Wu et al. 2020, *Drug Design, Development and Therapy* 14:5599-5610 [NE-12, animal]. Independent Chinese-author group; BPC-157 attenuated clopidogrel-induced gastric injury in rats. Direction is GI-protective (similar pattern to NSAID interaction). Note this is the opposite-side mechanism from the platelet-aggregation reversal above: BPC-157 may both (a) functionally antagonize the antithrombotic effect of clopidogrel and (b) protect against clopidogrel's gastric-mucosal toxicity. Both effects animal-only.
- **Corticosteroids:** BPC-157 counteracted muscle-healing impairment from systemic corticosteroids in rats [E-27, animal]. Direction framed as beneficial in source paper.
- **Cyclophosphamide:** reduced cyclophosphamide-induced gastric, duodenal, and bladder toxicity in rats [E-5, mechanism_review]. Animal-only, single-lab data.
- **Anthracyclines (doxorubicin):** in chronic HF rat model, BPC-157 reversed doxorubicin cardiac biomarker elevations (BNP, CK, AST, ALT) [E-28, animal]. Sikiric framing: "cardioprotective without reducing anti-tumor efficacy" — but the preservation of anti-tumor effect is asserted, not measured against tumor outcomes in the same study.
- **Monoamine modulators (pargyline + L-tryptophan, neuroleptics, amphetamine, ethanol):** BPC-157 counteracts serotonin syndrome induction, dopamine supersensitivity, neuroleptic catalepsy, ethanol intoxication in rodents [E-29, animal/mechanism_review]. **Important caution:** SSRI/SNRI/MAOI co-administration in humans has not been studied; rodent serotonin-syndrome counteraction is mechanistically interesting but does not establish human safety.

## 12. Contraindications

No formal regulatory contraindication list exists (BPC-157 is not an approved drug). Compiled from cautions raised in admissible reviews:

- **Active malignancy or known dysplastic tissue** — theoretical, VEGFR2/Akt/eNOS angiogenic mechanism; pentadecapeptide arginate literature explicitly raises "aberrant tumorigenesis in dysplastic tissues" [E-23, mechanism_review]
- **Pregnancy and lactation** — no human data; precautionary avoidance
- **Pediatric** — no data at all
- **Therapeutic anticoagulation** where bleeding-time normalization would be hazardous — based on rat platelet/bleeding-time reversal data [E-19, E-20, E-21, animal]
- **Concurrent serotonergic polypharmacy (MAOI + SSRI/SNRI)** — extrapolation from rodent serotonin-syndrome work; precautionary [E-29, animal]
- **Athletes subject to anti-doping** — WADA S0 (Non-Approved Substances), prohibited at all times in- and out-of-competition [E-30, E-31, regulatory]; US DoD Operation Supplement Safety prohibited list [E-32, regulatory]
- **United States legal/regulatory status** — see Section 15; compounded BPC-157 is not within scope of the 503A protective policy pending PCAC consultation [E-6, E-33, regulatory]

## 13. Monitoring Biomarkers

Drawn from the only published human monitoring protocol (Lee & Burgess 2025) and animal-toxicology endpoints:

- **CBC** (RBC indices, platelets) [E-1, open_label]
- **Comprehensive metabolic panel (CMP)** — hepatic (AST, ALT, ALP), renal (BUN, creatinine), electrolytes, glucose [E-1, open_label]. Animal models flag AST/ALT/CK/LDH as relevant injury panel in doxorubicin/HF models [E-28, animal]
- **CPK with isoenzymes** [E-1, open_label]
- **BNP** (cardiac strain) [E-1, open_label]
- **TSH** (thyroid baseline) [E-1, open_label]
- **Coagulation panel (PT/INR, PTT, platelet aggregation)** — recommended on theoretical basis given rodent platelet/bleeding-time data; not in any published protocol [E-19, E-20, E-21, animal]
- **Immunogenicity / anti-drug antibody monitoring** — flagged as needed in orthopaedic-peptide review [E-23, mechanism_review]; no standard assay exists
- **Cancer surveillance markers / age-appropriate screening** (colonoscopy, mammography, PSA, skin exam) — not in any BPC-157 monitoring protocol but theoretical precaution given angiogenesis mechanism and absent long-term human safety [E-2, mechanism_review]
- **GH-axis panel (IGF-1)** — flagged in broader peptide-therapeutics monitoring framework [E-23, mechanism_review]; BPC-157 increases GHR expression in tendon cells

## 14. Sourcing

### 14.1 Tier 3 — US compounding pharmacies (as of 2026-05-23)

| Pharmacy | Forms historically offered | Notes |
|---|---|---|
| Tailor Made Compounding (KY) | Injectable vial (SC), oral capsules, nasal spray | TMC catalog circulated 2020-2023 [D-10, compounding_data_sheet] |
| Empower Pharmacy (TX) | Historically dispensed BPC-157 injectable; product lines pruned to reflect FDA 503A constraints [D-15, regulatory] | empowerpharmacy.com |
| Hallandale, Belmar, Strive, APS | Have variously offered BPC-157 injectable or oral; current public product pages no longer list BPC-157 following category-2 placement and 2024 PCAC posture [D-15, regulatory] | individual pharmacy sites |

**Practical status:** US 503A availability is restricted and provider-dependent pending the **July 23-24, 2026 PCAC consultation** on BPC-157 (free base + acetate) inclusion on the 503A bulks list, evaluated for ulcerative colitis [D-15, regulatory].

### 14.2 Tier 4 — Research-chemical vendors (gray-market)

Vendors supplying BPC-157 labeled "for in-vitro research, not for human consumption" [D-11, D-12, vendor_label]:

| Vendor | Note |
|---|---|
| peptidesciences.com | 5 mg vials, terms-of-use disclaim human use |
| corepeptides.com | 5 mg / 10 mg, BPC-157 + TB-500 blends, explicit "chemical supplier, not 503A/503B" disclaimer |
| swisschems.is, limitlesslifenootropics.com | On project whitelist; gray-market disclaimer pattern |

Vendor purity COAs (Tier 4) are admissible only for reconstitution math. Vendor efficacy or "therapeutic dose" claims are excluded per the project source whitelist and were excluded from this report.

### 14.3 Country variance

- **US:** legal status of compounded BPC-157 contested; pending PCAC review. Research-chemical purchase is gray-market.
- **Australia, NZ, EU/UK, Canada:** prescription-only or unapproved. Personal-import for unapproved-medicines pathways is jurisdiction-specific.

## 15. Regulatory Status — as of 2026-05-23

> **Re-rotation flag:** Section requires update after FDA PCAC July 23-24, 2026 meeting minutes publish.

### 15.1 United States (FDA)

- Placed in **Category 2** of FDA 503A interim policies (bulk substances that may present significant safety risks) [D-15, regulatory].
- Following nomination withdrawals, **removed from Category 2** because nominators withdrew.
- FDA to consult **Pharmacy Compounding Advisory Committee (PCAC) on July 23-24, 2026** regarding inclusion of BPC-157-related bulk drug substances (BPC-157 acetate and BPC-157 free base) on the 503A bulks list, evaluated for ulcerative colitis [D-15, E-6, regulatory].
- **Practical 2026 status:** no FDA-approved BPC-157 drug product; no straightforward 503A pathway pending PCAC consultation.

### 15.2 European Union (EMA)

No EMA marketing authorization. Peptide has not progressed through Centralized or any National pathway. **Unapproved medicinal substance EU-wide**; member-state enforcement via national medicines authorities.

### 15.3 United Kingdom (MHRA)

Not licensed by MHRA. MHRA opened an investigation into UK peptide clinics making medicinal claims about BPC-157 and related compounds in April 2026 [D-17, regulatory]. Supply for human therapeutic use without MHRA marketing authorization is unlawful under Human Medicines Regulations 2012. (Primary MHRA citation weak in this dispatch; recorded as a gap.)

### 15.4 Australia (TGA)

**Schedule 4 (Prescription Only Medicine) + Appendix D, clause 5** of the Poisons Standard following November 2023 ACMS/ACCS joint meeting (ACMS #43 / ACCS #37 / Joint ACMS-ACCS #35) [D-18, D-19, regulatory]. Final decision rationale: limited safety/efficacy evidence; prior history of importation (48 referrals to TGA between July 2022 and meeting date); insufficient deterrence from "not for therapeutic use" online vendor labeling. Effective date codified in Poisons Standard amendment published May 2024.

### 15.5 Canada (Health Canada)

Not approved as prescription, non-prescription, or natural health product. **No Drug Identification Number (DIN)** for any BPC-157 product. No notice of consultation to add BPC-157 to the Prescription Drug List as of this review [D-20, regulatory]. Practical status: unapproved drug; import, sale, advertising for therapeutic use subject to the Food and Drugs Act.

### 15.6 New Zealand (Medsafe)

Medicines Classification Committee 70th meeting (25 May 2023) recommended addition to NZ schedule as **prescription medicine** [D-21, regulatory]. MCC 74th meeting extended to group entry covering BPC-157 and its analogues (naturally occurring and synthetic) to capture derivatives such as NL-BPC-157 hexadecapeptide intercepted at the border [D-22, regulatory]. Sport Integrity NZ describes BPC-157 as banned in sport at all times [D-23, regulatory].

### 15.7 WADA

Added to **2022 Prohibited List, S0 (Non-approved substances)**, effective **1 January 2022**. First substance ever included by name as an example in S0 [D-24, D-25, E-30, E-31, regulatory]. Prohibition in- and out-of-competition for all athletes subject to the Code.

### 15.8 US DoD

US Department of Defense Operation Supplement Safety (OPSS) Prohibited Dietary Supplement Ingredients List includes BPC-157 [E-32, regulatory].

## 16. Open Questions and Knowledge Gaps

1. **Receptor identity.** No specific membrane receptor has been identified in ~30 years of research.
2. **PK-PD disconnect.** Plasma t½ <30 min vs animal-reported effects persisting days to weeks to 360 days post-single-dose. The proposed gene-expression-cascade reconciliation has not been directly demonstrated by a time-matched PK-PD study.
3. **Oral bioavailability.** Sikiric group claims >24 h gastric stability; independent oral-peptide reviews do not list BPC-157 as an exception. No quantified oral %F published in any species.
4. **subQ PK.** No published primary PK for the most common practitioner route in any species.
5. **Intranasal / sublingual PK.** No published primary evidence.
6. **Independent replication of in-vivo MSK efficacy.** Zero. The Chang Gung group has replicated in-vitro mechanism work but has not published in-vivo replications.
7. **Human cycle length.** No data.
8. **Human SC dose justification.** No human PK or dose-finding to justify the practitioner 250-500 µg/dose conventions.
9. **Cancer risk.** Only one in-vivo tumor-bearing study (Kang 2018, C26 cachexia) — neither acceleration nor reduction. No human cancer-surveillance data exist for chronic use.
10. **Long-term human safety.** No human study has follow-up beyond ~24 h post-single-IV (Lee & Burgess 2025) or beyond the 6-12 mo subjective follow-up of Lee & Padgett 2021. Chronic-use safety is unknown.
11. **Sikiric "no toxicity" claim ceiling.** Most "no toxicity" findings are at 10 ng/kg and 10 µg/kg. Practitioner doses are several-fold higher. The dose ceiling for "no toxicity" is undetermined at clinical-practice doses.
12. **Reconstitution stability dossier.** No independent peer-reviewed stability study for BPC-157 in bacteriostatic water. The "4 weeks refrigerated" figure is community/vendor heuristic.
13. **Pregnancy / lactation / pediatric.** Zero human data; rodent reproductive toxicology negative (Xu 2020) but extrapolation uncertain.
14. **Drug interaction studies.** No human interaction data with NSAIDs, anticoagulants, corticosteroids, cyclophosphamide, anthracyclines, serotonergics — only rodent.
15. **PL 14736 unpublished Phase II.** A completed Pliva Phase II UC trial has never been primary-published. Whether the result was positive, null, or mixed is not publicly verifiable.
16. **Receptor-binding assay for dopamine/serotonin claims.** Counteraction effects in rodent behavioral models are reported; no binding-assay paper has been published.

## 17. Limitations of This Report

1. **Search depth.** This dispatch retrieved ~80 distinct citations across 5 parallel search agents using Tavily (advanced) + WebSearch fallback. Comprehensive Cochrane-style database coverage was not performed. PubMed indexing was the primary navigation; Embase, CINAHL, AMED were not separately searched.
2. **Date range.** Sources from BPC-157 discovery (~1991-1993) through May 2026. The FDA PCAC consultation scheduled for July 23-24, 2026 will produce a material regulatory update; this report carries a re-rotation flag for that date.
3. **Language coverage.** English-language sources primarily. Croatian-language Pliva-era trial documentation may exist beyond the indexed English summaries; not retrieved.
4. **Known bias — Sikiric-lab concentration.** ~76-80% of distinct primaries originate from one lab. This is the single most important contextual flag for any future query against this entry. It is documented in Section 4 and surfaced again per-indication in Section 7.
5. **Publication-bias signal — PL 14736.** The Pliva Phase II UC trial (~20 years ago) was completed but never primary-published. This is the single most important integrity flag for the entire literature.
6. **Sources that could not be accessed.**
   - Pliva-era Phase II UC trial primary report (not located in PubMed; cited in narrative reviews).
   - NCT02637284 Phase 1 PK/safety results (completed 2016, no results posted on ClinicalTrials.gov).
   - Direct MHRA enforcement notice (Guardian was used as discovery source; primary MHRA URL not surfaced — recorded as a gap in Section D).
   - Original Veljaca PL 14736 Phase I human PK/safety abstract — accessed via Semantic Scholar index; no widely-available full-text.
7. **Open-access lower-trust flags applied.** Frontiers and MDPI sources cited where used; downstream queries should weight these per `library/_source-whitelist.md` rules.
8. **No URL liveness audit at full scale.** Spot-check of 5 URLs confirmed valid patterns; comprehensive HEAD-check of all ~80 URLs was not performed. Future hardening point if this corpus becomes load-bearing for downstream decisions.
9. **No translation of foreign-language primaries.** Demirtaş 2025 (Turkish), Keremi 2009 (Hungarian), Veljaca 1994 (Pliva/Croatian) were accessed via English-language abstract/full text where available.
10. **No symbolic verification of dose equivalents.** Inter-species allometric scaling (rodent µg/kg to human µg/kg) is a known PK-modeling subject; this report does not perform that calculation. Practitioner-protocol doses are presented as practitioner conventions, with the gap from rodent literature flagged.

## 18. Bibliography

Sources are grouped by type tag for scanability. Section codes: A = Mechanism + PK; B = MSK; C = Non-MSK indications; D = Dose/Sourcing/Regulatory; E = AEs/Interactions/Monitoring.

### Primary literature (rct / open_label / animal / in_vitro)

[A-1] Hsieh M-J, Liu H-T, Wang C-N, et al. 2017. "Therapeutic potential of pro-angiogenic BPC157 is associated with VEGFR2 activation and up-regulation." *J Mol Med (Berl)* 95(3):323-333. DOI: 10.1007/s00109-016-1488-y. PMID: 27847966. https://pubmed.ncbi.nlm.nih.gov/27847966 [animal + in_vitro] — accessed 2026-05-23.

[A-2 / B-4] Chang C-H, Tsai W-C, Lin M-S, Hsu Y-H, Pang JHS. 2011. "The promoting effect of pentadecapeptide BPC 157 on tendon healing involves tendon outgrowth, cell survival, and cell migration." *J Appl Physiol* 110(3):774-780. DOI: 10.1152/japplphysiol.00945.2010. PMID: 21030672. https://pubmed.ncbi.nlm.nih.gov/21030672 [in_vitro + animal ex vivo] — accessed 2026-05-23.

[A-3 / B-5] Chang C-H, Tsai W-C, Hsu Y-H, Pang JHS. 2014. "Pentadecapeptide BPC 157 enhances the growth hormone receptor expression in tendon fibroblasts." *Molecules* 19(11):19066-19077. DOI: 10.3390/molecules191119066. PMID: 25415472. PMC6271067. https://pmc.ncbi.nlm.nih.gov/articles/PMC6271067 [in_vitro] — accessed 2026-05-23.

[A-4] Sikiric P, Seiwerth S, Grabarevic Z, et al. 1997. "The influence of a novel pentadecapeptide, BPC 157, on N(G)-nitro-L-arginine methylester and L-arginine effects on stomach mucosa integrity and blood pressure." *Eur J Pharmacol* 332(1):23-33. PMID: 9298922. https://pubmed.ncbi.nlm.nih.gov/9298922 [animal] — accessed 2026-05-23.

[A-7] Hsieh M-J, Lee C-H, Chueh H-Y, et al. 2020. "Modulatory effects of BPC 157 on vasomotor tone and the activation of Src-Caveolin-1-endothelial nitric oxide synthase pathway." *Sci Rep* / PMC7555539. https://pmc.ncbi.nlm.nih.gov/articles/PMC7555539 [animal + in_vitro] — accessed 2026-05-23.

[A-8] Boban Blagaic A, Blagaic V, et al. 2005. "Gastric pentadecapeptide BPC 157 effective against serotonin syndrome in rats." *Eur J Pharmacol* 512(2-3):173-179. PMID: 15840401. https://pubmed.ncbi.nlm.nih.gov/15840401 [animal] — accessed 2026-05-23.

[A-11 / D-4 / E-9] He L, Feng D, Guo H, Zhou Y, Li Z, Zhang K, Zhang W, Wang S, Wang Z, Hao Q, Zhang C, Gao Y, Gu J, Zhang Y, Li W, Li M. 2022. "Pharmacokinetics, distribution, metabolism, and excretion of body-protective compound 157, a potential drug for treating various wounds, in rats and dogs." *Front Pharmacol* 13:1026182. DOI: 10.3389/fphar.2022.1026182. PMID: 36588717. PMC9794587. https://pmc.ncbi.nlm.nih.gov/articles/PMC9794587 [animal] — accessed 2026-05-23. *Frontiers — open-access flag.* *Attribution corrected 2026-05-23: prior dispatch labeled this paper "Xu et al. 2022" in error; correct first-author is He L. Same paper, same DOI, same PMC.*

[B-1] Staresinic M, Sebecic B, Patrlj L, et al. 2003. "Gastric pentadecapeptide BPC 157 accelerates healing of transected rat Achilles tendon and in vitro stimulates tendocytes growth." *J Orthop Res* 21(6):976-983. PMID: 14554208. https://pubmed.ncbi.nlm.nih.gov/14554208 [animal + in_vitro] — accessed 2026-05-23.

[B-2] Krivic A, Anic T, Seiwerth S, Huljev D, Sikiric P. 2006. *J Orthop Res* 24(5):982-989. PMID: 16583442. https://pubmed.ncbi.nlm.nih.gov/16583442 [animal] — accessed 2026-05-23.

[B-3] Krivic A, Majerovic M, Jelic I, Seiwerth S, Sikiric P. 2008. *Inflamm Res* 57(5):205-210. PMID: 18594781. https://pubmed.ncbi.nlm.nih.gov/18594781 [animal] — accessed 2026-05-23.

[B-8] Cerovecki T, Bojanic I, Brcic L, Radic B, Vukoja I, Seiwerth S, Sikiric P. 2010. "Pentadecapeptide BPC 157 (PL 14736) improves ligament healing in the rat." *J Orthop Res* 28(9):1155-1161. PMID: 20225319. https://pubmed.ncbi.nlm.nih.gov/20225319 [animal] — accessed 2026-05-23.

[B-11] Staresinic M, Petrovic I, Novinscak T, et al. 2006. "Effective therapy of transected quadriceps muscle in rat: gastric pentadecapeptide BPC 157." *J Orthop Res* 24(5):1109-1117. PMID: 16609979. https://pubmed.ncbi.nlm.nih.gov/16609979 [animal] — accessed 2026-05-23.

[B-12] Novinscak T, Brcic L, Staresinic M, et al. 2008. *Surg Today* 38(8):716-725. PMID: 18668315. https://pubmed.ncbi.nlm.nih.gov/18668315 [animal] — accessed 2026-05-23.

[B-13] Mihovil I, et al. 2009. *J Physiol Pharmacol* 60(Suppl 7):69 [animal].

[B-14] Pevec D, Novinscak T, Brcic L, et al. 2010. *Med Sci Monit* 16(3):BR81-88 [animal].

[B-15] Matek D, Matek I, Staresinic E, et al. 2025. *Pharmaceutics* 17. PMC11768438. https://pmc.ncbi.nlm.nih.gov/articles/PMC11768438 [animal] — accessed 2026-05-23.

[B-17] Sebecic B, Nikolic V, Sikiric P, Seiwerth S, Sosa T, Patrlj L, et al. 1999. "Osteogenic effect of a gastric pentadecapeptide, BPC-157, on the healing of segmental bone defect in rabbits: a comparison with bone marrow and autologous cortical bone implantation." *Bone* 24(3):195-202. PMID: 10071911. https://pubmed.ncbi.nlm.nih.gov/10071911 [animal] — accessed 2026-05-23.

[B-19 / E-3] Lee E, Padgett B. 2021. "Intra-Articular Injection of BPC 157 for Multiple Types of Knee Pain." *Altern Ther Health Med* 27(4):8-13. PMID: 34324435. https://pubmed.ncbi.nlm.nih.gov/34324435 [open_label] — accessed 2026-05-23.

[C-2] Sikiric P et al. 1996. "Beneficial effect of BPC 157 on gastric lesions induced by restraint stress, ethanol, indomethacin, and capsaicin neurotoxicity." *Dig Dis Sci* 41:1604-1614 [animal].

[C-3] Veljaca M et al. 1994. "BPC-15 reduces TNBS-induced colonic damage in rats." *J Pharmacol Exp Ther* 272:417-422 [animal, **non-Sikiric Pliva**].

[C-4] Xue XC et al. 2004. "Protective effects of pentadecapeptide BPC 157 on gastric ulcer in rats." *World J Gastroenterol* 10(7):1032-1036 [animal, **non-Sikiric**].

[C-5] Klicek R et al. 2008. *J Pharmacol Sci* 108(1):7-17 [animal].

[C-6] Klicek R et al. 2013. *J Physiol Pharmacol* 64(5):597-612 [animal].

[C-7] Vuksic T et al. 2007. *Surg Today* 37:768-777 [animal].

[C-10] Djakovic Z et al. 2016. *World J Gastroenterol* 22:9127-9140 [animal].

[C-16] Mikus D et al. 2001. *Burns*. PMID: 11718984 [animal].

[C-17] Huang T et al. 2015. "BPC-157 enhances alkali-burn wound healing in vivo." *Drug Des Devel Ther* [animal, **non-Sikiric**].

[C-18] Tkalcevic VI et al. 2007. *Eur J Pharmacol* 570:212-221 [animal, **Pliva**].

[C-19] Bilic M et al. 2005. *Burns* 31:310-315 [animal].

[C-20] Tudor M, Sikiric P et al. 2010. *Regul Pept* [animal].

[C-21] Perovic D et al. 2019. *J Orthop Surg Res* 14:199 [animal].

[C-22] Vukojevic J et al. 2020. *Brain Behav* 10(8):e01726 [animal].

[C-23] Gjurasin M et al. 2010. *Regul Pept* [animal].

[C-24] Sikiric P et al. 2022. *World J Gastroenterol* 28(1):23-46 [animal].

[C-26] Barisic I et al. 2013. *Regul Pept* 181:50-66 [animal].

[C-27 / E-21] Konosic S et al. 2019. *Oxid Med Cell Longev* 2019:9084643. PMC6955135. https://pmc.ncbi.nlm.nih.gov/articles/PMC6955135 [animal] — accessed 2026-05-23.

[C-28] Demirtaş H et al. 2025. *Biomedicines*. PMC11857380. https://pmc.ncbi.nlm.nih.gov/articles/PMC11857380 [animal, **non-Sikiric Turkish**] — accessed 2026-05-23.

[C-29] Keremi B et al. 2009. *J Physiol Pharmacol* 60(Suppl 7):115-122 [animal, **non-Sikiric Hungarian**].

[C-30] Ilic S et al. 2009. *J Physiol Pharmacol* 60(Suppl 7):107-114 [animal].

[C-31] Sikiric P et al. ~2010. *J Physiol Pharmacol* (jpp 0410_15) [animal].

[C-32] Lazic R et al. 2015. *Exp Eye Res*. PMID: 25912999 [animal].

[C-33] Kralj T et al. 2021. *Front Pharmacol* [animal] *Frontiers — open-access flag*.

[E-1] Lee EJ, Burgess D. 2025. "Safety of Intravenous Infusion of BPC157 in Humans: A Pilot Study." *Altern Ther Health Med*. PMID: 40131143. https://pubmed.ncbi.nlm.nih.gov/40131143 [open_label] — accessed 2026-05-23.

[E-2 / A-9 / B-7] Vasireddi N, Hahamyan H, Salata MJ, Karns M, Calcei JG, Voos JE, Apostolakos JM. 2025. "Emerging Use of BPC-157 in Orthopaedic Sports Medicine: A Systematic Review." (also published as "Regeneration or Risk?") *HSS Journal* 21:15563316251355551. PMID: 40756949. PMC12446177. https://pubmed.ncbi.nlm.nih.gov/40756949 [mechanism_review] — accessed 2026-05-23. *Independent PRISMA systematic review.*

[E-8] Xu C, Sun L, Ren FL, et al. 2020. "Preclinical safety evaluation of body protective compound-157, a potential drug for treating various wounds." *Regulatory Toxicology and Pharmacology* 114:104665. https://www.sciencedirect.com/science/article/abs/pii/S027323002030091X [animal] — accessed 2026-05-23.

[E-14] Radeljak S, Seiwerth S, Sikiric P. 2004. *Melanoma Res* 14:A14-A15 [in_vitro conference abstract].

[E-15] Kang EA et al. 2018. "BPC157 as potential agent rescuing from cancer cachexia." *Curr Pharm Des* 24:1947-1956 [animal].

[E-19] Stupnisek M et al. 2012. "Pentadecapeptide BPC 157 reduces bleeding time and thrombocytopenia after amputation in rats treated with heparin, warfarin or aspirin." *Thromb Res* 129:652-659. https://www.sciencedirect.com/science/article/abs/pii/S0049384811004075 [animal] — accessed 2026-05-23.

[E-20] Stupnisek M et al. 2015. *PLoS ONE* 10:e0123454. PMC4405609. https://pmc.ncbi.nlm.nih.gov/articles/PMC4405609 [animal] — accessed 2026-05-23.

[E-24] Park JM, Lee HJ, Sikiric P, Hahm KB. 2020. *Curr Pharm Des* 26:2971-2981 [animal/mechanism_review].

[E-26] Ilic S et al. 2011. *Life Sci* 88:535-542 [animal].

[E-27 / B-14] Pevec D et al. 2010. *Med Sci Monit* 16:BR81-88 [animal].

### Mechanism reviews and independent syntheses

[A-5] Seiwerth S, Sikiric P et al. 2021. "Stable Gastric Pentadecapeptide BPC 157 and Wound Healing." *Front Pharmacol* 12:627533. PMC8275860. https://pmc.ncbi.nlm.nih.gov/articles/PMC8275860 [mechanism_review] *Frontiers — open-access flag*.

[A-6] Sikiric P, Seiwerth S, Rucman R, et al. 2014. *Curr Pharm Des* 20(7):1126-1135. PMID: 23782146. https://pubmed.ncbi.nlm.nih.gov/23782146 [mechanism_review].

[A-10 / E-16] Sikiric P, Boban Blagaic A, Strbe S, et al. 2024. *Pharmaceuticals* 17(4):461. PMC11053547. https://pmc.ncbi.nlm.nih.gov/articles/PMC11053547 [mechanism_review] *MDPI — open-access flag*.

[A-12] Sikiric P, Seiwerth S, et al. 2020. PMC7096228. https://pmc.ncbi.nlm.nih.gov/articles/PMC7096228 [mechanism_review].

[A-13] Brown TD, Whitehead KA, Mitragotri S, et al. 2025. "Barriers and Strategies for Oral Peptide and Protein Therapeutics Delivery: Update on Clinical Advances." PMC12030352. https://pmc.ncbi.nlm.nih.gov/articles/PMC12030352 [mechanism_review].

[A-14] Editorial. 2023. *Front Pharmacol*. PMC10364635. https://pmc.ncbi.nlm.nih.gov/articles/PMC10364635 [mechanism_review].

[B-6] McGuire FP, Martinez R, Lenz A, Skinner L, Cushman DM. 2025. "Regeneration or Risk? A Narrative Review of BPC-157 for Musculoskeletal Healing." *Curr Rev Musculoskelet Med* 18(12):611-619. PMC12446177. https://pmc.ncbi.nlm.nih.gov/articles/PMC12446177 [mechanism_review].

[B-10] Bechara et al. 2025. PMC13026520. https://pmc.ncbi.nlm.nih.gov/articles/PMC13026520 [mechanism_review].

[B-16] Staresinic M, Japjec M, Vranes H, et al. 2022. *Biomedicines* 10(12):3221. PMC9775659. https://pmc.ncbi.nlm.nih.gov/articles/PMC9775659 [mechanism_review].

[B-18] Gwyer D, Wragg NM, Wilson SL. 2019. *Cell Tissue Res* 377:153-159. https://link.springer.com/article/10.1007/s00441-019-03016-8 [mechanism_review].

[C-1] Sikiric P et al. 1993. *J Physiol Paris* 87:313-327 [mechanism_review/animal].

[C-11] Veljaca M et al. *Safety, tolerability and pharmacokinetics of PL 14736 in healthy male volunteers* [open_label — abstract only, primary publication not widely indexed].

[C-12] PL 14736 Phase II UC enema study (Pliva). **Primary publication not located** [rct — unpublished].

[C-15] Seiwerth S, Sikiric P et al. 2021 — see [A-5].

[C-25] Sikiric P et al. 2022. *Biomedicines* 10(11):2696 [mechanism_review] *MDPI — open-access flag*.

[C-34] Sikiric P et al. 2024. *Inflammopharmacology* 32:3119-3161 [mechanism_review].

[C-35 / E-12] Józwiak M, Bauer M, Kamysz W, Kleczkowska P. 2025. "Multifunctionality and Possible Medical Application of the BPC 157 Peptide — Literature and Patent Review." *Pharmaceuticals (Basel)* 18(2):185 (also PMC11859134). https://pmc.ncbi.nlm.nih.gov/articles/PMC11859134 [mechanism_review] *MDPI — open-access flag. Independent of Sikiric.*

[C-36] Sikiric P et al. 2025. *Pharmaceuticals* 18(10):1450 (reply to Józwiak 2025) [mechanism_review] *MDPI — open-access flag*.

[D-3 / E-2] Vasireddi 2025 — see [E-2 / A-9 / B-7].

[E-4] Sikiric P et al. 2020. *ScienceDirect S1347861319313696* [mechanism_review].

[E-5] Sikiric P et al. 2022. PMC9687817. https://pmc.ncbi.nlm.nih.gov/articles/PMC9687817 [mechanism_review].

[E-7] InpharmD pharmacist query: "Is BPC-157 safe for use in humans?" https://inpharmd.com/inquiries/13701 [mechanism_review].

[E-10] Sikiric P et al. 2025. *Pharmaceuticals* 18:1450. PMC12567428. https://pmc.ncbi.nlm.nih.gov/articles/PMC12567428 [mechanism_review].

[E-11] Hsieh MJ et al. 2017 — see [A-1].

[E-13] Li L et al. 2019. *Oncogene* 38:6241-6255 [mechanism_review].

[E-17] *Tendon, Ligament, and Muscle Injury... Review*. PMC12944561, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12944561 [mechanism_review].

[E-18] *Columbia Undergraduate Science Journal — BPC-157 risk-benefit*. https://journals.library.columbia.edu/index.php/cusj/blog/view/720 [mechanism_review — lower trust, secondary].

[E-22] *BPC 157 as Potential Treatment for COVID-19*. PMC8575535, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8575535 [mechanism_review].

[E-23] *Therapeutic Peptides in Orthopaedics: Applications, Challenges*. PMC12753158, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12753158 [mechanism_review].

[E-25] Sikiric P et al. 2013. *Curr Pharm Des* 19:76-83 [mechanism_review].

[D-1] Sikiric P et al. 2012. "Focus on ulcerative colitis: stable gastric pentadecapeptide BPC 157." *Curr Med Chem*. PMID: 22300085 [open_label].

[D-2] Sikiric P et al. 2011. *Curr Pharm Des*. PMID: 21548867 [mechanism_review].

[D-5] Sikiric P et al. 2007. *J Physiol Pharmacol*. PMID: 17713731 [animal].

[D-6] Seiwerth/Sikiric 2021 — see [A-5].

[D-7] Stable gastric pentadecapeptide BPC 157 in colitis/IR. PMC5752708. https://pmc.ncbi.nlm.nih.gov/articles/PMC5752708 [animal].

[D-8] *Nose-to-Brain Delivery of Therapeutic Peptides as Nasal Aerosols*. PMC9502087 [mechanism_review].

[D-9] *Reply to Sikiric et al. BPC 157 Therapy: Targeting Angiogenesis and Vascular Recovery*. PMC12567171 [mechanism_review].

### Regulatory / institutional

[D-15] FDA. *Bulk Drug Substances Nominated for Use in Compounding* (PDF, updated April 22, 2026). https://www.fda.gov/media/94155/download [regulatory].

[D-16] FDA. *Certain Bulk Drug Substances for Use in Compounding that May Present Significant Safety Risks*. https://www.fda.gov/drugs/human-drug-compounding/certain-bulk-drug-substances-use-compounding-may-present-significant-safety-risks [regulatory].

[D-17] *The Guardian — Medicines watchdog to investigate UK peptide clinics over health claims*. April 2026. https://www.theguardian.com/society/2026/apr/04/medicines-watchdog-to-investigate-uk-peptide-clinics-over-health-claims [regulatory — discovery source for MHRA action; primary MHRA URL not surfaced this dispatch].

[D-18] TGA. *Notice of interim decisions to amend (or not amend) the current Poisons Standard — ACMS #43 / ACCS #37 / Joint ACMS-ACCS #35*. https://www.tga.gov.au/sites/default/files/2024-04/public-notice-of-interim-decisions-acms-43-accs-37-joint-acms-accs-35.pdf [regulatory].

[D-19] TGA. *Notice of final decisions to amend the current Poisons Standard (November 2023)*. Published May 2024. https://www.tga.gov.au/sites/default/files/2024-05/notice-final-decisions-amend-not-amend-current-poisons-standard-november-2023.pdf [regulatory].

[D-20] Health Canada. *About the Prescription Drug List / Drug Product Database*. https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/prescription-drug-list.html [regulatory — used to confirm no DIN].

[D-21] Medsafe. *Minutes of the 70th Medicines Classification Committee meeting, 25 May 2023*, item 5.2. https://medsafe.govt.nz/profs/class/Minutes/2021-2025/mccMin25May2023.htm [regulatory].

[D-22] Medsafe. *Classification of Unscheduled Peptides*, Agenda item 5.7, MCC 74th meeting. https://medsafe.govt.nz/profs/class/Agendas/Agen74/5.7Peptides.pdf [regulatory].

[D-23] Sport Integrity NZ. *Athlete sanctioned for trafficking banned substances*. https://sportintegrity.nz/news/athlete-sanctioned-for-trafficking-banned-substances [regulatory].

[D-24 / E-30] WADA. *WADA publishes 2022 Prohibited List* (news release). https://www.wada-ama.org/en/news/wada-publishes-2022-prohibited-list [regulatory].

[D-25] WADA. *The 2022 Prohibited List* (PDF). https://www.wada-ama.org/sites/default/files/2022-01/2022list_final_en_0.pdf [regulatory].

[E-6] FDA Pharmacy Compounding Advisory Committee Meeting, July 23-24, 2026. https://www.fda.gov/advisory-committees/advisory-committee-calendar/july-23-24-2026-meeting-pharmacy-compounding-advisory-committee-07232026 [regulatory].

[E-31] WADA. *2026 Prohibited List* (PDF). https://www.wada-ama.org/sites/default/files/2025-09/2026list_en_final_clean_september_2025.pdf [regulatory].

[E-32] US DoD Operation Supplement Safety. *BPC-157 — A prohibited peptide and an unapproved drug*. https://www.opss.org/article/bpc-157-prohibited-peptide-and-unapproved-drug-found-health-and-wellness-products [regulatory].

[E-33] FDA. *Bulk Drug Substances Nominated for Use in Compounding — withdrawn list* (Apr 2026 update). https://www.fda.gov/media/94155/download [regulatory].

### Compounding pharmacy data sheets (Tier 3)

[D-10] Tailor Made Compounding peptide catalog. https://www.scribd.com/document/495397628/TMC-Catalog [compounding_data_sheet] — admissible for SC 0.25 mL × 20 days protocol and oral capsule format; admin protocol only.

### Vendor labels (Tier 4 — reconstitution math only)

[D-11] Peptide Sciences product page, BPC-157 5mg. https://www.peptidesciences.com/bpc-157-5mg [vendor_label].

[D-12] Core Peptides product page, BPC-157 5mg/10mg. https://www.corepeptides.com/peptides/bpc-157 [vendor_label].

[D-13] Sigma-Aldrich handling/storage guidelines for peptides. https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/research-and-disease-areas/cell-and-developmental-biology-research/handling-and-storage [vendor_label].

[D-14] AdonyxBio. Understanding BPC-157 and Why Shelf Life Matters. https://adonyxbio.com/understanding-bpc-157-and-why-shelf-life-matters [vendor_label].

### Anecdote aggregates (Tier 5 — qualitative patterns only)

[E-34] r/bpc_157 — "BPC-157 & TB-500 injection site reactions suddenly after 10 days." https://www.reddit.com/r/bpc_157/comments/1nl663v/ [anecdote_aggregate].

[E-35] Amino Innovations Reddit-experience aggregation. https://aminoinnovations.com/bpc-157-reddit-reviews [anecdote_aggregate].

[E-36] r/eds — BPC-157 peptide experience ("growing pains"). https://www.reddit.com/r/eds/comments/1afrxql/bpc157_peptide [anecdote_aggregate].

## 19. Methodology Appendix

### 19.1 Process

This entry was produced via the `/deep-research` skill (--mode=deep) on 2026-05-23. The dispatch was structured as a goal-agnostic library-entry build with a custom orchestrator prompt enforcing project source-whitelist and type-tag rules per `vault/library/_source-whitelist.md`. The 8-phase deep-research pipeline executed as follows:

- **Phase 1 — Scope.** 12-section scope authored from the dispatch prompt. Goal-agnostic; no operator context.
- **Phase 2 — Plan.** 10 parallelizable search angles; triangulation rule of ≥3 sources per indication (or explicit "single primary, awaiting replication" flag); 4 evidence-tier dimensions added to standard rubric.
- **Phase 2.5 — Rubric.** 10-dimension, 100-pt rubric saved to `/tmp/deep-research/rubric_bpc-157.md`. 8 auto-fail conditions defined. Threshold 99/100. Each sub-agent given a 5-point self-check.
- **Phase 3 — Retrieve (parallel).** 5 sub-agents dispatched concurrently, each with whitelist + type-tag enforcement: (A) Mechanism + PK, (B) MSK indications, (C) Non-MSK indications, (D) Dose / Reconstitution / Sourcing / Regulatory, (E) AEs / Contraindications / Monitoring. Each sub-agent ran self-judge before returning. All five passed self-check.
- **Phase 4 — Triangulate & verify.** Cross-section concordance check; auto-fail audit; spot-check of 5 random URLs; aggregate Sikiric-share calculation (~76-80% across deduplicated primaries). No auto-fail triggered. Findings saved to `/tmp/deep-research/phase4_triangulation.md`.
- **Phase 4.5 — Outline refinement.** Initial 12-section outline expanded to 19-section structure to elevate concentration-risk as a first-class section and to split MSK into per-tissue subsections; restructuring < 50%. Saved to `/tmp/deep-research/phase4_5_outline.md`.
- **Phase 5 — Synthesize.** This report. Each section assembled from sub-agent output with cross-section deduplication and concordance reconciliation.
- **Phase 6/7 — Critique + refine.** **NOT EXECUTED AS DEFINED.** Deep mode specifies separate critique and refine agent dispatches; neither ran. Findings that would normally emerge in Phase 6 (PL 14736 publication-bias signal; PK-PD disconnect; Sikiric concentration as a structural concern) were written into Section 17 (Limitations) during Phase 5 synthesis rather than via a separate red-team pass. This is a material deviation from deep-mode rigor — see §19.4.1.
- **Phase 8 — Package.** Final report written to `vault/library/peptides/bpc-157/research-report.md`. Compound entry populated at `vault/compounds/bpc-157.md` from this report per `vault/compounds/_template.md`.

### 19.1.1 Deviations from declared deep mode (self-audit, added 2026-05-23)

The dispatch was declared `--mode=deep` but several deep-mode requirements were not executed. The rigor of this report is closer to **standard mode (8 phases minus 6/7)** plus a custom triangulation pass + supplementary dispatch (practitioner-layer + non-English-layer), than to true deep mode.

Deep-mode requirements NOT executed:

1. **Paired judge agents (Phase 3 spec).** Skill specifies a concurrent judge agent for each retrieval sub-agent, applying the Phase 2.5 rubric at the mode-appropriate threshold. **Zero judges dispatched.** Each retrieval agent ran a 5-question self-check at the end — that is self-judging, not independent audit.
2. **99/100 judge threshold.** The 10-dimension rubric written in Phase 2.5 was never scored against by any agent. Threshold never tested.
3. **Iteration loops.** Skill allows up to 3 iterations to threshold. None ran because no judge ran.
4. **Phase 6 CRITIQUE.** No separate red-team agent dispatched.
5. **Phase 7 REFINE.** No separate refine pass with additional targeted research.
6. **Comprehensive URL liveness HEAD-check.** Only 5 URLs spot-checked (§17 limitation #8); deep mode would HEAD-check the full ~80.

**What functioned as ad-hoc verification:** the supplementary non-English literature dispatch (Agent G, 2026-05-23) caught the He L 2022 author-attribution error — a fortunate byproduct of language-survey methodology, not deliberate verification.

**Re-rotation should include the missing phases.** When this report is re-rotated (e.g., after FDA PCAC July 23-24, 2026), the dispatch should re-execute as true deep mode with paired judges per Phase 3, plus separate critique and refine agents per Phase 6/7. Alternatively, this report should be re-flagged as standard-mode output.

### 19.2 Source counts

- Total distinct citations: ~80
- Tier 1 (peer-reviewed primary): ~55
- Tier 2 (regulatory): ~12
- Tier 2.5 (curated practitioner): 0 used as primary; Examine.com referenced once in liveness probe only, not cited
- Tier 3 (compounding pharmacy data sheets): 1
- Tier 4 (vendor labels): 4 — all for reconstitution math or gray-market availability disclosure
- Tier 5 (anecdote aggregates): 3 — qualitative AE-pattern surfacing only
- Sikiric-affiliated share of distinct primaries: ~76-80%
- Independent in-vivo MSK replications: 0

### 19.3 Verification summary

- Wikipedia not cited as primary in any section.
- Vendor / anecdote sources do not ground any numerical claim.
- All animal cites carry species annotation.
- Sikiric-lab concentration audit performed per section and aggregated.
- Spot-check of 5 random URLs (Hsieh 2017, He 2022 [originally cited as Xu 2022 — author attribution corrected in 2026-05-23 supplementary dispatch], Chang 2011, WADA 2022 PDF, TGA 2023 PDF) confirmed valid patterns; comprehensive HEAD-check not performed (recorded as Section 17 limitation).
- Auto-fail conditions: 0 triggered.

### 19.4 Re-rotation triggers

This entry should be re-rotated when any of the following occur:
- **FDA PCAC July 23-24, 2026** meeting minutes publish (Sections 14, 15)
- **NCT07437547** (Phase 2 hamstring) completes or reports interim results
- **PL 14736 Phase II UC** primary publication surfaces (would materially change Sections 7.5 and 17)
- Any independent in-vivo MSK efficacy study publishes (would materially change Section 7.1-7.4 evidence tiers)
- Any human RCT publishes in any indication
- Any case report of serious adverse event publishes

### 19.5 Supplementary dispatch (2026-05-23) — two layers added

Two follow-up agents were dispatched after the primary report to fill structural gaps:

**Agent F — Prescribing-Practice Layer.** Output: `vault/library/peptides/bpc-157/practitioner-layer.md`. Documents what licensed prescribers actually use to make dose decisions (compounding pharmacy data sheets, practitioner reference texts, named-physician stated protocols, originator-group dose, consensus dose). Key findings: (a) only one dose-explicit current compounding-pharmacy data sheet locatable — Australian Compounding Lab (Feb 2024, 2-10 µg/kg BID, 200-400 µg BID commonly). (b) US 503A landscape structurally hollowed out by FDA Category 2 placement (Sep 2023) and TMC enforcement (2020-2022). (c) Named-physician protocols anchor on Edwin Lee (IV 5 mg-20 mg outlier vs. subQ norm), Kent Holtorf (acetylated form for CIRS/mold), Seeds book (250-500 µg subQ daily baseline), Paulvin, Gapin, Attia (conservative). (d) Sikiric reviews do NOT state a specific human dose. (e) Consensus subQ dose 250-500 µg/day, 4-6 wk cycles — confirms what was in §8.3. (f) Practitioner consensus runs ~1.5-3× the Examine rodent-to-human extrapolation; Lee IV is ~30-100×. (g) Divergent schools: standard subQ vs Lee IV; free-base vs acetylated salt forms; conservative (Attia) vs enthusiastic (Holtorf/Lee/Seeds/Paulvin/Gapin) adoption.

**Agent G — Non-English Literature Coverage.** Output: `vault/library/peptides/bpc-157/non-english-layer.md`. Surveyed Croatian, Chinese, Russian, Korean, Japanese. Key findings: (a) **author-attribution correction:** the PK paper at PMC9794587 is **He L et al. 2022**, not "Xu et al. 2022" — fixed throughout the primary report. (b) Xue 2004b (Chinese J New Drugs 13:602-605) — second Fourth Military Medical paper, porcine skin-wound, distinct from C-4. (c) Park 2021 + Jung 2022 — two Korean primaries opening a new indication: antinociception (formalin and incisional pain models). New §7.12. (d) Wu 2020 (DDDT) — clopidogrel-induced gastric injury attenuation. Added to §11 interactions. (e) Croatian conference abstracts (Vraneš 2023 psoriasis IL-17A; Linarić-Lipnjak 2024 tracheocutaneous fistula; Dulčić 2024 aminoglycoside nephrotoxicity) — extends indication map; new §7.13 (dermatology signal). (f) Pliva/Diagen patent estate catalogued — WO 1992/004368 through US 9,850,282 + Slovenian SI 23928. (g) **Confirmed absences:** zero Russian-language primaries in eLibrary.ru, CyberLeninka, or Springer-translated Bulletin of Experimental Biology and Medicine; PL 14736 Phase II UC primary not located in any language — strengthens publication-bias flag. (h) No contradictions with existing English-language report claims.

### 19.6 Files generated by this dispatch

- `/tmp/deep-research/scope_bpc-157.md` (Phase 1)
- `/tmp/deep-research/plan_bpc-157.md` (Phase 2)
- `/tmp/deep-research/rubric_bpc-157.md` (Phase 2.5)
- `/tmp/deep-research/section_a_mechanism_pk.md` (Phase 3 — sub-agent A)
- `/tmp/deep-research/section_b_msk.md` (Phase 3 — sub-agent B)
- `/tmp/deep-research/section_c_other_indications.md` (Phase 3 — sub-agent C)
- `/tmp/deep-research/section_d_dose_sourcing.md` (Phase 3 — sub-agent D)
- `/tmp/deep-research/section_e_ae.md` (Phase 3 — sub-agent E)
- `/tmp/deep-research/phase4_triangulation.md` (Phase 4)
- `/tmp/deep-research/phase4_5_outline.md` (Phase 4.5)
- `vault/library/peptides/bpc-157/research-report.md` (Phase 8 — this file)
- `vault/compounds/bpc-157.md` (Phase 8 — derived compound entry)
- `vault/library/peptides/bpc-157/practitioner-layer.md` (supplementary 2026-05-23)
- `vault/library/peptides/bpc-157/non-english-layer.md` (supplementary 2026-05-23)
