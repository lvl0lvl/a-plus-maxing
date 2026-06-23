---
title: FOXO4-DRI
type: compound
permalink: a-plus-maxing/compounds/foxo4-dri
class: peptide
evidence_tier: D
risk_tier: experimental
status: researching
created: 2026-06-20
last_verified: 2026-06-20
provenance_dir: design/.foxo4-dri-design-work
provenance_slug: labs-specialist
---

# FOXO4-DRI

## Metadata
- class: peptide (D-retro-inverso senolytic peptidomimetic; ~48 aa, ~5,382 Da; derived from the forkhead domain of the FOXO4 transcription factor + appended HIV-TAT cell-penetrating sequence; the TAT CPP participates directly in the binding interface with p53 TAD2 rather than being mechanistically inert; designed by Baar and de Keizer at Erasmus MC Rotterdam; first published Baar 2017 *Cell*)
- evidence_tier: D — see [[library/methodology/evidence-tiers]] (ALL human evidence is absent; there is no published human clinical trial, no published human pharmacokinetics, and no human safety database for FOXO4-DRI or any Cleara Biotech next-generation analog; the entire efficacy base is preclinical: three mouse models in the founding Baar 2017 Cell paper plus five to six independent rodent or cell-culture extensions; no lifespan endpoint in any study, including mice; materially behind dasatinib+quercetin [human pilot, n=9] and fisetin [Phase 2 RCTs active] in the senolytic translation pipeline; de Keizer's group holds lead authorship on 1 of 8 primary papers [12.5%], below the 70% single-lab concentration flag, with genuine multi-continental independence — but the clinical-translation path remains in de Keizer's orbit via Cleara Biotech B.V.)
- risk_tier: experimental — FDA-unapproved; no IND on public record; not on FDA 503A/503B bulk substance lists; not nominated to PCAC; WADA-prohibited in- and out-of-competition (S0 — Non-Approved Substances); on-target p53-apoptosis activation risk in non-senescent tissues formally flagged in published literature; FOXO4 expressed in heart and testis with cardiotoxicity concern unresolved and uncharacterized in any species; grey-market product only; D-retro-inverso chirality unverifiable by standard HPLC CoA
- status: researching
- last_verified: 2026-06-20

> **Read this first — three facts that cannot be buried.** (1) **Zero human data.** No human clinical trial exists at any phase for FOXO4-DRI. Not Phase 1 safety; not PK; not anything. The D+Q pilot (n=9) and fisetin Phase 2 RCTs are ahead of it. (2) **p53/cardiotoxicity safety flag is unresolved.** The peptide directly activates p53-driven mitochondrial apoptosis. FOXO4 is expressed in normal heart and testis; the Zhang 2020 study authors explicitly flagged cardiotoxicity concern as uncharacterized. No cardiac biomarker (troponin, CK-MB) or histopathology has been reported at any time point in any published study. Additionally, Born/Adnot 2023 (*Circulation*) found that FOXO4-DRI senolysis **worsened** pulmonary hypertension by clearing protective senescent pulmonary endothelial cells — a concrete adverse finding, not a theoretical caveat. (3) **Unverifiable identity.** The D-retro-inverso chirality essential for proteolytic stability and senolytic activity cannot be confirmed by standard reversed-phase HPLC or mass spectrometry — only chiral HPLC or NMR can confirm configuration. Consumer-grade CoAs confirm purity of a species of approximately the right molecular weight; they do not confirm the compound is correctly chiral. Full depth + citations: [[library/peptides/foxo4-dri/research-report]].

## Mechanism
FOXO4-DRI is a synthetic **D-retro-inverso (DRI) peptidomimetic** designed to disrupt the FOXO4–p53 protein–protein interaction that keeps senescent cells alive. Its mechanism operates in three steps. First, in senescent cells specifically, FOXO4 protein expression is markedly elevated; FOXO4 physically binds p53 and tethers it to nuclear DNA-damage foci (DNA-SCARs), preventing p53 from initiating mitochondrial apoptosis and locking the cell in its characteristic "zombie" state despite an intracellular milieu primed for death [Baar 2017 *Cell*]. Second, FOXO4-DRI enters the cell via its appended HIV-TAT cell-penetrating sequence, occupies the same binding surface on the p53 second transactivation subdomain (p53 TAD2) as the native FOXO4 forkhead domain, and displaces it — with approximately five-fold higher affinity than the native FOXO4-FH fragment (Kd ~400 ± 280 nM vs. ~2.5 µM) [Bourgeois 2025 *Nat Commun*]. Both partners — FOXO4 forkhead domain and p53 TAD2 — are intrinsically disordered in isolation and undergo coupled folding upon complex formation; p53 phosphorylation at Ser46 and Thr55, events associated with the senescent state, further enhance binding affinity and competitive displacement — a second layer of senolytic selectivity on top of differential FOXO4 expression. Third, freed from its nuclear tether, p53 translocates to mitochondria and activates the intrinsic apoptosis pathway via BAX/BAK-dependent outer-membrane permeabilization, cytochrome c release, and downstream caspase-3 cleavage — selectively in the senescent population that elevated FOXO4 in the first place. Non-senescent cells, which have low FOXO4, do not form the FOXO4–p53 nuclear complex and are largely spared. The D-retro-inverso backbone renders the peptide essentially invisible to endogenous L-stereospecific proteases, extending its functional persistence relative to native L-peptides, though no formal PK study in any species has been published. **All mechanistic and efficacy evidence is preclinical — mouse models and cell culture.**

## Evidence Summary
Strongest sources (weight order):

- Baar et al. 2017 (*Cell*, PMID 28340339) — founding paper; three mouse models: naturally aged C57BL/6 (n=7–8/group), XpdTTD progeroid, and doxorubicin-chemotoxicity young mice; 5 mg/kg IP or IV × 3 doses every other day; outcomes: restored fur density, locomotor fitness, renal function (BUN/creatinine), ~30% reduction in p16-positive renal cortex cells; in vitro: 11.73-fold greater senescent vs. proliferating IMR90 selectivity at 50 µM; scrambled DRI control lacked differential activity. `in_vitro/animal` — founding, not yet independently replicated end-to-end. [[library/peptides/foxo4-dri/research-report]]
- Bourgeois et al. 2025 (*Nat Commun*, PMID 40593617) — NMR structural characterization: FOXO4-FH and p53 TAD2 are intrinsically disordered and undergo coupled folding; FOXO4-DRI Kd ~400 ± 280 nM vs. ~2.5 µM for native FOXO4-FH; HIV-TAT participates in binding interface; p53 Ser46/Thr55 phosphorylation enhances FOXO4-DRI displacement. `in_vitro` — mechanism-only; de Keizer is non-lead co-author (Graz/Utrecht led). [[library/peptides/foxo4-dri/research-report]]
- Zhang et al. 2020 (*Aging Albany NY*, PMID 31959736) — naturally aged male C57BL/6 mice (20–24 mo, n=6/group); 5 mg/kg IP × 3 doses; restored serum testosterone; reduced testicular p53/p21/p16 and SASP (IL-1β, IL-6, TGF-β); nuclear p53 exclusion confirmed as proximal event; authors explicitly flagged cardiotoxicity as uncharacterized in their system. `animal` — Sun Yat-sen University, independent of de Keizer. [[library/peptides/foxo4-dri/research-report]]
- Huang et al. 2021 (*Front Bioeng Biotechnol*, PMID 33996787) — human articular chondrocytes, 8 non-OA donors; 25 µM × 5 days; passage-9 (high senescent fraction) reduced >50%; passage-3 (minimally expanded) not significantly affected; **cautionary finding: FOXO4-DRI increased p21 even in senescent cultures, suggesting a stressor effect beyond selective apoptosis.** `in_vitro` — University of Pittsburgh, independent. [[library/peptides/foxo4-dri/research-report]]

Counter-evidence and limits:
- **Born, Adnot et al. 2023 (*Circulation*, PMID 36515093) — ADVERSE FINDING.** Mouse pulmonary hypertension models; eliminating senescent pulmonary endothelial cells (with FOXO4-DRI among strategies tested) worsened pulmonary hemodynamics rather than improving them. Senescent cells in the pulmonary vascular niche appear to perform a protective or compensatory function. Independent INSERM/Hôpital Henri Mondor group. Published in a high-impact cardiovascular journal — this is a concrete adverse outcome, not a theoretical concern. `animal`
- **No human trial.** ClinicalTrials.gov search June 2026: zero registered interventional trials at any phase.
- **No lifespan endpoint** in any study, including mice. Baar 2017 assessed healthspan-adjacent markers over a five-day window. Cleara's claim of "29% geriatric-mouse survival increase" for CL04183 is an unpublished corporate relay of third-party data — not peer-reviewed.
- **No ADME/PK data** in any species; no immunogenicity data for the all-D scaffold in humans.
- **Chondrocyte p21 signal** (Huang 2021): elevation of p21 in FOXO4-DRI-treated senescent cultures suggests the compound may act as a cellular stressor beyond the three-step mechanism; mechanistic basis uncharacterized and unresolved.
- D+Q (human pilot, measurable senolytic biomarker reduction demonstrated) and fisetin (Phase 2 RCTs active) are both ahead of FOXO4-DRI in translation — the senolytic hypothesis remains preclinical even for these more advanced compounds.

## Non-English Literature Coverage
Surveyed; see [[library/peptides/foxo4-dri/research-report]] bibliography.
- Chinese: Four fully independent groups confirmed; Zhang 2020 + Li 2024 (Sun Yat-sen University, Guangzhou — Leydig cell/spermatogenesis), Han 2022 (Peking Union Medical College — pulmonary fibrosis), Kong 2025 (Chinese Academy of Medical Sciences/Peking Union Medical College — keloid fibroblast senescence), Hu 2026 (Wenzhou Medical University — endothelial senescence). All published in English-language international journals. Genuine multi-group coverage.
- French: Born/Adnot 2023 (*Circulation*) from INSERM U955 / Hôpital Henri Mondor, Créteil — the adverse pulmonary hypertension finding; fully independent. Published in English.
- Dutch: de Keizer group at Erasmus MC Rotterdam (founding paper); Cleara Biotech B.V. (Utrecht). Academic papers published in English.
- Austrian: Bourgeois/Madl group at Medical University of Graz (2018 FEBS Letters mechanism review + 2025 Nature Communications structural paper). Published in English.
- American: Huang et al. 2021 (University of Pittsburgh + Central South University — chondrocytes); independent. Published in English.
- Russian / Soviet / Croatian / Japanese / Korean: no admissible primaries specific to FOXO4-DRI identified.
- Translation notes: all admissible primaries are English-language; non-English language searches conducted; no abstract-only translations used.

## Prescribing-Practice Layer
See [[library/peptides/foxo4-dri/research-report]] §§4.2, 4.6 for full detail. No admissible prescribing-practice sources exist — FOXO4-DRI cannot be lawfully compounded or prescribed in any jurisdiction.

- **Compounding pharmacy data sheets:** none admissible. FOXO4-DRI is absent from the FDA 503A Category 1 and Category 2 active lists; it has not been nominated to the PCAC. No 503A or 503B pathway exists. No Empower, Tailormade, Hallandale, Belmar, or other licensed pharmacy data sheet exists or could legally exist.
- **Practitioner reference texts:** no A4M/IFM/Seeds/International Peptide Society monograph for FOXO4-DRI located. No licensed prescriber has a framework for clinical administration — there is no human PK, no human dose-finding, no human safety database.
- **Originator-group dose:** Baar 2017 used 5 mg/kg IP or IV in mice × 3 doses every other day. Allometric conversion to a 70 kg human yields approximately 175–350 mg per dose — at grey-market pricing of $8–32/mg, approximately $1,400–$11,200 per three-dose cycle, and that assumes the product is correctly synthesized and chiral, which cannot be verified. Grey-market self-experimenter community protocols cite 2–10 mg subQ every other day — far below any allometric equivalent of the mouse dose and therefore operating at concentrations likely to be pharmacologically irrelevant even if correctly synthesized.
- **Consensus practitioner dose:** none exists. No licensed prescriber has a clinical protocol grounded in any human data.
- **Gap:** the prescribing-practice layer is entirely absent for FOXO4-DRI. There is no dose to recommend.

## Protocol
- dose:               # no established human dose; mouse studies used 5 mg/kg IP or IV × 3 doses every other day; allometric scaling to humans is highly uncertain for an all-D peptide with unknown PK; grey-market protocols are unvalidated and pharmacologically irrelevant at commonly cited doses
- route:              IP/IV in all published animal studies; subcutaneous not evaluated in any published study; oral bioavailability nil (large peptide, GI proteolysis despite D-chirality); no human route validated
- timing:             n/a (library entry)
- cycle:              no validated cycle for humans; five-day course in Baar 2017; up to one month in Hu 2026 aged mice
- stack:              n/a
- source:             grey-market research-chemical only ("For Research Use Only / Not For Human Use"); no FDA-approved product; no 503A/503B pathway; no legitimate clinical source; D-chirality unverifiable by standard CoA
- regulated status:   not FDA-approved; no IND on public record; not 503A/503B-compoundable; no PCAC nomination; WADA-prohibited S0 in- and out-of-competition; no regulatory approval in any jurisdiction
- cost:               grey-market ~$8–32/mg; allometric-equivalent human dose would be $1,400–$11,200 per three-dose cycle at correctly-scaled doses

## Reconstitution (peptides only)
- supplied as:        lyophilized powder, grey-market, ~48 aa D-retro-inverso peptide; Bourgeois 2025 notes effective net peptide content (one supplier: 69.92% net peptide vs. 98.03% HPLC purity — the gap is TFA counter-ion and water)
- diluent:            bacteriostatic water (grey-market convention; no clinical data)
- final concentration / dose volume / storage: per vendor label only; no independently validated protocol
- **CRITICAL IDENTITY NOTE:** D-retro-inverso chirality is unverifiable by standard reversed-phase HPLC or mass spectrometry — both yield the same result for a correctly chiral and an incorrectly chiral (L-substituted) peptide of the same sequence length. Only chiral-specific HPLC or 2D NMR can confirm D-amino acid configuration. Standard consumer CoAs confirm a dominant species of approximately the right molecular weight; they do not confirm the compound is correctly synthesized, correctly chiral, or the same compound Baar 2017 used.

## Risk Profile

> **WARNING — ON-TARGET P53/CARDIOTOXICITY AND ADVERSE PULMONARY FINDING.** FOXO4-DRI directly activates p53-driven mitochondrial apoptosis — a master regulator of apoptosis, cell-cycle arrest, DNA damage response, and wound healing. FOXO4 is expressed in normal human heart and testis; cardiotoxicity is explicitly flagged in the published literature (Zhang 2020) and completely uncharacterized — no troponin, CK-MB, or cardiac histopathology data exist in any published study. Separately, Born/Adnot 2023 (*Circulation*) found that senolytic clearance using FOXO4-DRI WORSENED pulmonary hypertension by eliminating protective senescent pulmonary endothelial cells. Senescence is not uniformly harmful — beneficial roles in wound healing, tumor suppression, and vascular maintenance mean indiscriminate senolysis carries documented costs.

- adverse effects (literature): no published human safety data exist for any route or dose; acute mouse tolerance at 5 mg/kg IP/IV (five-day to one-month courses) reported without overt gross toxicity in all published studies; no formal repeat-dose toxicology, no genotoxicity, no carcinogenicity study published; Born/Adnot 2023 documented worsened pulmonary hemodynamics in mouse pulmonary hypertension models with senolytic clearance
- adverse effects (anecdotal): injection-site reactions and fatigue reported in peptide forums (`anecdote_aggregate`; no validated prevalence data)
- contraindications:
  - Active malignancy — p53 pathway manipulation in oncology settings is unpredictable; on-target p53 apoptosis activation carries uncharacterized risk in cancer cells with altered p53
  - History of treated malignancy with active recurrence risk — same mechanistic concern
  - Pulmonary arterial hypertension or significant pulmonary vascular disease — Born/Adnot 2023 (*Circulation*) documents worsened pulmonary hemodynamics with senolytic clearance in mouse PH models
  - Significant cardiac disease — cardiotoxicity concern explicitly flagged in published literature (FOXO4 expressed in heart); entirely uncharacterized; no troponin/CK-MB data in any study
  - Known germline TP53 mutations (Li-Fraumeni syndrome) — mechanistic interaction with p53 pathway is direct and consequential
  - Active infection or systemic inflammatory state — p53 is an active effector in immune-cell apoptosis and inflammation
  - Pregnancy / lactation — FOXO4 expressed in placenta; embryotoxic risk uncharacterized; no data
  - WADA-tested athletes — S0 prohibited substance, in- and out-of-competition
  - Thrombocytopenia or active bleeding disorder — acute p53 apoptosis affecting platelet precursors uncharacterized
- monitoring:           [[biomarkers/egfr]] (renal function — Baar 2017 measured BUN/creatinine as primary safety and efficacy readout; eGFR/creatinine at baseline, day 7, and day 30 post-dose); cardiac biomarkers: troponin I/T and CK-MB (baseline, 48 hours, and 7 days post-dose — specifically to address the uncharacterized cardiotoxicity concern flagged in published literature); CBC with differential (baseline + monitoring — p53 effects on platelet precursors uncharacterized); hepatic function (ALT, AST, bilirubin — baseline + day 7 + day 30); anti-drug antibody assay (day 30 and 90 — all-D-amino acid immunogenicity entirely unknown in humans)
- known interactions:   no characterized human interactions; theoretical: any concurrent cytotoxic chemotherapy or radiation therapy (additive p53 stress); any concurrent p53-pathway-modifying agent

## Trial Status
- linked experiment:    none
- baseline biomarkers:  n/a (library entry)
- expected response window: unknown in humans; Baar 2017 assessed healthspan-adjacent markers over five days; no lifespan endpoint in any species; human timeline cannot be inferred
- stopping criteria:    ALT/AST greater than 3× upper limit of normal; creatinine rise greater than 1.5-fold from baseline; any troponin elevation above the upper limit of normal; platelet count fall exceeding 30% from baseline; any sign of systemic immunogenic reaction; new diagnosis of pulmonary hypertension; worsening dyspnea or cardiorespiratory symptoms

## Decision Notes
Per [[library/methodology/evidence-tiers]], FOXO4-DRI at evidence_tier=D / risk_tier=experimental → **avoid / do not self-experiment outside a clinical trial framework**: this is the lowest evidence tier — zero human data of any kind, including Phase 1 safety. FOXO4-DRI sits behind the small-molecule senolytics that themselves remain preclinical in the key respects: D+Q has a human pilot (n=9, measurable senolytic biomarker reduction) and fisetin has Phase 2 RCTs active; neither approach has proven human lifespan or healthspan benefit. For FOXO4-DRI, the question is not "does the mechanism translate to humans" — that requires a Phase 1 trial that does not exist. The on-target p53/cardiotoxicity safety concern is formally acknowledged in the published scientific literature by researchers within the field, has not been addressed by any subsequent study, and involves one of the most consequential and broadly active proteins in the human cell. The Born/Adnot 2023 *Circulation* finding is a concrete adverse outcome — not a theoretical caveat — demonstrating that senolytic clearance can worsen disease by eliminating beneficial senescent cell populations. The grey-market product's D-chirality is unverifiable by standard CoA. Cleara Biotech's next-generation CL04183 is progressing through IND-enabling work but no Phase I trial is registered as of mid-2026. Operator-specific fields intentionally blank — goal-agnostic library entry.

## Relations
- [[library/peptides/foxo4-dri/research-report]]
- [[biomarkers/egfr]]
- [[compounds/humanin]]
- [[compounds/mots-c]]
