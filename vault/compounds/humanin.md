---
title: Humanin
type: compound
permalink: a-plus-maxing/compounds/humanin
class: peptide
evidence_tier: C
risk_tier: experimental
status: researching
created: 2026-06-20
last_verified: 2026-06-20
provenance_dir: design/.humanin-design-work
provenance_slug: labs-specialist
---

# Humanin

## Metadata
- class: peptide (mitochondrial-derived peptide, MDP; 24-aa sequence MAPRGFSCLLLLTSEIDLPVKRRA; encoded by a short ORF within MT-RNR2, the mitochondrial 16S rRNA gene; **first MDP ever discovered**, Hashimoto 2001; founding member predating MOTS-c, SHLP2, and all other MDPs)
- evidence_tier: C — see [[library/methodology/evidence-tiers]] (all human evidence is observational biomarker: circulating humanin declines with age and associates with cognitive aging [HRS n=15,620], coronary endothelial dysfunction, impaired fasting glucose, and CV mortality in independent cohort studies; the causal direction of these associations is entirely unresolved; NO human administration trial of exogenous humanin or any humanin analog has been published, registered, or completed as of 2026-06-20; efficacy evidence is preclinical — HNG analog in rodent/porcine models, not native humanin — from two historically dominant research groups [Keio ~30–35%, USC ~25–30%, combined ~55–65%, below the ≥70% single-lab flag]; longevity link is associative, not causal)
- risk_tier: experimental — FDA-unapproved for any indication; no 503A compounding pathway (not a July 2026 PCAC nominee; not on Category 1 or 2 active lists); WADA-prohibited in- and out-of-competition (S0 — Non-Approved Substances); anti-apoptotic mechanism documented as pro-tumor in two independent preclinical models (TNBC + GBM); human PK entirely uncharacterized; native plasma half-life ~20–30 min in rodents; grey-market product only
- status: researching
- last_verified: 2026-06-20

> **Read this first — biomarker signal is NOT therapeutic evidence.** Humanin is the founding mitochondrial-derived peptide, a historically significant discovery with a mechanistically rich profile. Its endogenous biomarker signal is real: lower circulating humanin consistently associates with cognitive decline, coronary endothelial dysfunction, and impaired fasting glucose in independent cohort studies. What this entry is NOT: evidence that exogenous humanin supplementation produces those outcomes. **No human administration trial of humanin or any humanin analog has ever been published.** The dominant preclinical efficacy evidence is for the S14G-HNG analog (~1,000-fold more potent than native humanin) — not the native 24-mer sold by grey-market vendors. The causal direction of the biomarker associations is entirely unresolved (disease may drive humanin down, not the reverse). **The single most load-bearing safety fact: humanin is pro-apoptotic in cancer models** — exogenous humanin promoted tumor growth, metastasis, and chemotherapy resistance in TNBC, and enhanced glioblastoma invasion and shortened survival in GBM xenografts. Active malignancy or cancer history = precautionary contraindication. Full depth + citations: [[library/peptides/humanin/research-report]].

## Mechanism
Humanin (HN) is translated from a short open reading frame within **MT-RNR2** (mitochondrial 16S rRNA gene) — the founding member of the MDP class, identified in 2001 via a neuronal "death-trap" screen at Keio University. Its cytoprotective mechanism operates through two parallel arms: (i) **intracellular direct sequestration** of pro-apoptotic proteins Bax and truncated Bid (tBid), blocking their translocation to the outer mitochondrial membrane and preventing cytochrome c release and caspase activation; and (ii) **extracellular receptor-mediated signaling** via two independent receptor systems — the G protein-coupled receptor **FPR2 (FPRL1)**, whose humanin binding mode has been characterized at atomic resolution by cryo-EM (Zhu 2022, *Nat Commun*), activating ERK1/2 and also competitively blocking Aβ42 at FPR2; and a trimeric cytokine receptor complex of **CNTFRα / WSX-1 / gp130**, which activates **JAK2 → STAT3** and downstream AKT/ERK1/2 in neuronal contexts. Humanin additionally binds **IGFBP-3** at its C-terminal heparin domain (blocking IGFBP-3 nuclear import and its independent pro-apoptotic program), with IGFBP-3 binding accelerating humanin clearance — a PK corollary exploited in analog design. Metabolic evidence: central (ICV) humanin activates hypothalamic STAT3 to modulate peripheral insulin sensitivity; the HNGF6A analog enhances β-cell glucose-stimulated insulin secretion via mitochondrial ATP coupling. Cardioprotective evidence (rodent/porcine, HNG): AMPK → eNOS phosphorylation reduces ischemia-reperfusion injury. **All mechanistic evidence is in-vitro or animal; no mechanism has been directly demonstrated in controlled human in-vivo studies.**

## Evidence Summary
Strongest sources (weight order):

- Yen et al. 2018 (*Sci Rep*, PMID 30242290) — human cohort: BVAIT n=146 + HRS n=15,620; lower circulating humanin associated with accelerated cognitive aging (~2 years by epigenetic clock in African Americans with SNP rs2854128 ↓ humanin ~14%); observational only. `cohort` — USC/CohBar COI disclosed.
- Widmer et al. 2013 (*Am J Physiol Heart Circ Physiol*, PMID 23220334) — human cross-sectional n=40; direct intracoronary acetylcholine challenge (gold-standard); lower plasma humanin in patients with coronary endothelial dysfunction (1.3 vs 2.2 ng/mL, p=0.03); correlates with coronary blood flow response (p=0.0091). `cohort` — observational, not interventional.
- Sharp et al. 2020 (*JACC: Basic to Translational Science*, PMID 32760857) — female Yucatan minipigs; HNG (2 mg/kg IV) reduced infarct size by 41% and apoptosis by 50% at 60-min ischemia (n=14); at 75-min ischemia the same dose failed (p=0.541) — dose-duration sensitivity is a key translational warning. `animal` — HNG analog; LSU/Pittsburgh group (independent of USC/Keio).
- Lee et al. 2014 (*Aging Cell*, PMID 25040290) — mouse models (n=3–11/group): GH/IGF-1-deficient long-lived mice +40–45% humanin; GH-transgenic short-lived mice −70%; Laron syndrome humans (n=6/group) +80% vs controls; GH therapy in GH-deficient children (n=11) −20% humanin. `animal` + human observational — establishes regulated GH/IGF-1–humanin axis, not exogenous administration efficacy.
- Bolignano et al. 2024 (*J Nephrol*, PMID 39102184) — prospective human cohort n=94 hemodialysis patients, 30-month follow-up: **U-shaped** relationship — both very low (<450.7 pg/mL) and very high (>759.5 pg/mL) humanin predicted worse CV outcomes; intermediate range most favorable. `cohort` — independent Italian/Greek consortium; the U-shape is an important caution against assuming more humanin is uniformly better.

Counter-evidence and limits:
- **No human administration trial exists** — the translational gap is entirely unbridged (ClinicalTrials.gov search 2026-06-20: zero registered interventional trials).
- Moreno Ayala et al. 2020 (*Sci Rep*, PMID 32444831) — syngeneic TNBC model: exogenous humanin significantly accelerated tumor growth, promoted spontaneous lung metastases, and impaired doxorubicin efficacy. `animal` — pro-tumor counter-signal, independent of USC/Keio.
- Ha et al. 2024 (*Cell Death Dis*, PMID 38942749) — GBM cell lines + orthotopic xenograft: humanin activated integrin αV–TGFβ → invasion, angiogenesis, shorter survival. `animal` — second independent pro-tumor finding, distinct signaling mechanism.
- Bolignano 2024 U-shape (above): very high circulating humanin tracked excess CV mortality — consistent with stress-response compensation, not simply protection; challenges the "more is better" biomarker narrative.
- Most in-vivo efficacy evidence uses HNG (~1,000× more potent than native humanin); consumer-available product is native 24-mer — analog-to-native conflation is the most common interpretive error in this literature.
- Causal direction of all biomarker associations is unresolved: disease may drive humanin downward (reverse causation), not the reverse.

## Non-English Literature Coverage
Surveyed; see [[library/peptides/humanin/research-report]] bibliography.
- Japanese: Foundational discovery papers by Hashimoto/Niikura/Nishimoto at Keio University (2001–2011, approximately 30–35% of primary papers); Kariya et al. 2005 MELAS biopsy study (Acta Neuropathol); Keio contribution to receptor characterization. All published in English-language journals.
- Chinese: Multiple independent groups identified: Chai et al. 2014 (Neurosci Bull, Huazhong University — native humanin in Aβ-injected rats); Zhao et al. 2023 (Heliyon, Chongqing Medical University — HNG in heart failure); Shi et al. 2024 (BBRC, Southern Medical University — HNG in septic AKI); Ren et al. 2020 (J Cell Mol Med, Soochow — platelet thrombus). Genuine independent breadth; all published in English-language journals.
- Estonian: NCT03431844 (University of Tartu) — completed observational human study of humanin isoforms around cardiac surgery; independent European program.
- Italian / Greek: Bolignano et al. 2024 (*J Nephrol*) prospective hemodialysis cohort, multi-center Italian/Greek consortium; most independent large prospective humanin biomarker study in the corpus.
- Russian / Soviet / Croatian / Korean: no admissible primaries specific to humanin identified.
- Translation notes: all admissible primaries are English-language; non-English language searches conducted via PubMed affiliation/journal tags and CNKI keyword scan; no abstract-only translations used.

## Prescribing-Practice Layer
See [[library/peptides/humanin/research-report]] §7 for full detail. No `compounding_data_sheet` sources are admissible — humanin is not currently lawfully compoundable under 503A and no licensed U.S. compounding pharmacy can legally produce it for human administration.

- **Compounding pharmacy data sheets:** none admissible. Humanin is absent from the FDA 503A Category 1 and Category 2 active lists; it is not among the seven July 2026 PCAC nominees (BPC-157, KPV, TB-500, MOTS-c, Emideltide, Semax, Epitalon). No Empower, Tailormade, Hallandale, Belmar, or other 503A pharmacy data sheet located.
- **Practitioner reference texts:** no A4M/IFM/Seeds monograph specifically for humanin or HNG located. No human administration trial has produced dosing guidance from any licensed prescriber framework.
- **Consensus practitioner convention (NOT efficacy-grounded):** grey-market vendor labeling and forum aggregates cite ~100–500 µg/day SC or IM for HNG, extrapolated from rodent dosing. `[vendor_label]` / `[anecdote_aggregate]`. No basis in human PK data; unvalidated; may not ground any numerical claim.
- **Gap:** the prescribing-practice layer is entirely absent for humanin. No human PK data, no human dose-finding, no compounding pathway, no practitioner clinical experience grounded in any human administration data. The HNG analog dominating animal efficacy studies is not what grey-market vendors sell. There is no dose to recommend.

## Protocol
- dose:               # no established human dose — animal studies used HNG at 2 mg/kg IV (porcine I/R), 0.16 µg/kg/min ICV infusion (rats); native humanin doses in rodents are proportionally larger due to ~1,000× lower potency; no human dose-finding data exist for native humanin or HNG
- route:              subQ or IM per grey-market convention (no human PK supports any route); ICV used for central metabolic effects in rodents (impractical for human use); native humanin oral bioavailability expected nil (peptide, GI proteolysis); SC daily dosing at native humanin's 20–30 min plasma half-life would produce brief peaks with rapid clearance
- timing:             n/a (library entry)
- cycle:              no validated cycle
- stack:              n/a
- source:             grey-market research-chemical only (no FDA-approved product; not 503A-compoundable); Bachem synthesizes research-grade reference standard (laboratory use only, not for human administration)
- regulated status:   not FDA-approved; not lawfully compoundable (no 503A/503B pathway; not a PCAC July 2026 nominee); WADA-prohibited S0 in- and out-of-competition (non-specified substance, no contamination-defense reduction)
- cost:               # not assessed

## Reconstitution (peptides only)
- supplied as:        lyophilized powder, grey-market, native 24-mer (MAPRGFSCLLLLTSEIDLPVKRRA); identity/purity unverified without independent mass spectrometry; at least 13 nuclear paralog peptides (MTRNR2L1–13) share 92–95% amino-acid identity — sequence accuracy from vendors is unverifiable by the buyer; no FDA manufacturing oversight
- diluent:            bacteriostatic water (vendor convention; no clinical data)
- final concentration / dose volume / storage: per vendor label only (`vendor_label`); no independently validated protocol exists
- note:               consumer product is native 24-mer; most published in-vivo efficacy data used HNG (S14G) or HNGF6A — these are NOT the same compound as native humanin; equating vendor product to HNG animal-study outcomes is an analog-substitution error

## Risk Profile

> **WARNING — PRO-TUMOR SIGNAL.** The anti-apoptotic mechanism that underlies all of humanin's neuroprotective and cytoprotective effects — Bax/tBid sequestration, caspase suppression — is the same mechanism that protects malignant cells from programmed death and chemotherapy. This is not a theoretical concern: two independent animal studies in two separate tumor types document exogenous humanin promoting tumor growth and metastasis. Active malignancy or cancer history is a precautionary contraindication pending human safety data.

- adverse effects (literature): no published human safety data exist for any route or dose of exogenous humanin or HNG — direct human safety evidence is entirely absent; animal efficacy studies at pharmacological doses report no overt dose-limiting toxicity, but formal toxicology (repeat-dose, genotoxicity, carcinogenicity) has not been conducted
- adverse effects (anecdotal): injection-site reactions reported in peptide forums (`anecdote_aggregate`; qualitative only; no validated prevalence data)
- contraindications:
  - Active malignancy (any type) — anti-apoptotic mechanism documented to protect TNBC tumor cells from chemotherapy and promote lung metastasis [Moreno Ayala 2020, animal]
  - Personal history of cancer where recurrence risk is active — same mechanistic concern
  - Glioblastoma or aggressive CNS tumor history — humanin activates pro-invasive integrin αV–TGFβ axis, shortening survival in GBM xenograft model [Ha 2024, animal]
  - First-degree family history of breast cancer or GBM — precautionary; insufficient data to rule out risk potentiation
  - Active antitumor immunotherapy (checkpoint inhibitors, CAR-T, bispecific antibodies) — the anti-apoptotic mechanism could blunt treatment-mediated tumor-cell killing; strong relative contraindication pending any human data
  - WADA-tested athletes — S0 prohibited substance; no contamination-defense reduction available
  - Pregnancy / lactation — no human data; mitogenic and anti-apoptotic activity; theoretical risk
- monitoring:           [[biomarkers/fasting-glucose]] (baseline + periodic — humanin has documented metabolic effects on glucose regulation in rodents; pharmacodynamic monitoring warranted) (no validated humanin-specific pharmacodynamic biomarker exists in humans; fasting glucose is a mechanistic SAFETY monitor, NOT a confirmed PD proxy for humanin activity); CBC with differential (malignancy surveillance — baseline before initiation and during extended use; given pro-tumor signal); oncology consultation if any cancer history; relevant tumor markers at baseline per personal risk; unexplained lymphadenopathy, weight loss, or constitutional symptoms → stop and evaluate
- known interactions:   no characterized human interactions; theoretical: additive glucose-lowering with insulin, sulfonylureas, GLP-1 agonists, metformin (hypothalamic STAT3 / metabolic axis); IGFBP-3–modulating therapies may alter humanin clearance (uncharacterized in vivo in humans)

## Trial Status
- linked experiment:    none
- baseline biomarkers:  n/a (library entry)
- expected response window: unknown in humans; rodent efficacy experiments used pharmacological doses by IP/IV with acute effects in hours to days; human timeline cannot be inferred
- stopping criteria:    stop on any new cancer diagnosis — alert treating oncologist to anti-apoptotic mechanism; unexplained lymphadenopathy, weight loss, or B-symptoms → stop and evaluate; systemic allergic reaction; confirmed unexplained hypoglycemic episode (in the absence of another identified cause) → stop; any regulatory change classifying humanin as an explicitly prohibited or controlled substance

## Decision Notes
Per [[library/methodology/evidence-tiers]], Humanin at evidence_tier=C / risk_tier=experimental → **doctor-required / avoid for any therapeutic or longevity use**: the human evidence base is entirely observational biomarker data from endogenous circulating humanin; zero human administration trials exist; the efficacy evidence that does exist is preclinical — and for the HNG analog (~1,000× more potent) rather than the native peptide available commercially. The pro-tumor counter-signal (two independent animal models, two distinct tumor types, two distinct signaling mechanisms) is the single most clinically consequential fact in this entry — it is not a theoretical risk but a documented preclinical effect of the same anti-apoptotic mechanism that makes humanin attractive for neuroprotection. The biomarker associations with cognitive aging, coronary endothelial function, and impaired fasting glucose are replicated across independent cohorts and constitute a real biological signal, but they do not establish that supplementing exogenous humanin reproduces those protective states — the causal direction of the associations is unresolved. Operator-specific fields intentionally blank — goal-agnostic library entry.

## Relations
- [[library/peptides/humanin/research-report]]
- [[biomarkers/fasting-glucose]]
- [[compounds/mots-c]]
- [[compounds/ss-31]]
