---
title: Peptide Research Triage
type: note
permalink: a-plus-maxing/library/peptides/triage
status: active
created: 2026-05-23
last_reviewed: 2026-05-23
review_cadence: per research session
---

# Peptide Research Triage

The closed surface area for peptide research. Updates as Walter's goals shift and as research narrows the field.

Two passes:
1. **Triage pass** — shallow scan per class (~30 min `deep-research` standard mode) → rank candidates within the class against Walter's goals.
2. **Deep pass** — full `deep-research` deep mode on the top-1 candidate per relevant class → populates `compounds/<name>.md`.

Cap: 2 deep passes per session. Triage passes are cheaper and can batch.

---

## Class taxonomy

### Healing / soft tissue
- BPC-157
- TB-500 (Thymosin Beta-4 fragment)
- GHK-Cu
- KPV
- LL-37

**Goal anchor:** post-illness deconditioning recovery, tendon/joint resilience for return to training. Likely top class for first deep pass.

### GH secretagogues
- Ipamorelin
- CJC-1295 (no-DAC and DAC variants)
- Tesamorelin
- Sermorelin
- Hexarelin
- MK-677 (Ibutamoren — small molecule, not strictly a peptide, but indexed here)

**Goal anchor:** body composition, recovery, sleep depth. Higher risk-tier; requires labs (IGF-1) for monitoring.

### Metabolic / weight
- Semaglutide (Ozempic, Wegovy)
- Tirzepatide (Mounjaro, Zepbound)
- Retatrutide (investigational)
- AOD-9604

**Goal anchor:** body composition only if needed. Highest regulatory/cost considerations.

### Cognitive / neuro
- Selank
- Semax
- Cerebrolysin
- Dihexa
- N-Acetyl Selank Amidate

**Goal anchor:** post-illness cognitive recovery if applicable, sustained focus. Mostly Russian literature — translation provenance is a research consideration.

### Sexual / dopaminergic
- PT-141 (Bremelanotide — FDA approved as Vyleesi)
- Melanotan II
- Kisspeptin-10

**Goal anchor:** libido, dopaminergic tone. Generally lower priority unless flagged by labs.

### Immune / longevity
- Thymosin Alpha-1
- Epitalon
- FOXO4-DRI
- Humanin

**Goal anchor:** post-illness immune restoration (Tα1 is the strongest candidate here), longevity-class interventions deferred until baseline established.

### Mitochondrial
- SS-31 (Elamipretide)
- MOTS-c
- Humanin

**Goal anchor:** energy / recovery / longevity. Largely experimental at consumer access points.

---

## Triage scoring rubric

For each peptide in a triage pass, score 1-5:

| Dimension | Anchor question |
|---|---|
| **Goal-fit** | Does this serve a P0/P1 goal in `meta/goals.md`? |
| **Evidence strength** | Highest evidence tier achievable per `evidence-tiers.md`? (S=5, A=4, B=3, C=2, D=1) |
| **Risk fit** | Does risk-tier match Walter's risk posture and current MD access? |
| **Sourcing realism** | Can Walter actually obtain it (Rx or vetted compounder)? |
| **Monitorability** | Are required monitoring biomarkers things Walter can/will measure? |

Score ≤ 12/25 → exclude from this cycle. Score ≥ 18/25 → eligible for deep pass.

---

## Current ranked queue

Populated after triage passes. Format: `<peptide> | <class> | <triage-score> | <next action>`.

> **Track ownership (2026-06-18).** This is the **peptide-library research track**. The
> plan-generation pipeline is a *separate* track (a-plus sessions S72–S73); its S73
> "supplement↔peptide additive-AE screen" *consumes* compound entries but does not
> author them — so it does not claim anything in this queue. No collision.

**Done so far (2026-06-18):** BPC-157 (re-research) · Tesamorelin (21/25) · **Thymosin Alpha-1 (19/25)** —
all deep-passed → Done. Healing class fully triaged (4 Excluded); Ipamorelin held (16/25).
Triage scores: `tesamorelin/.provenance/triage-scores.md`.

Ranked queue (deep-pass-eligible, not yet deep-passed): _(empty — metabolic class fully done; next round triages a new class)_
- `Retatrutide | metabolic | 18/25 | deep pass (with hard sourcing caveat)` — triple agonist, strong Phase-2/3
  but INVESTIGATIONAL (not approved → sourcing 2/5; entry must gate toward "wait for approval", not acquisition).

**Metabolic class triaged 2026-06-18:** Semaglutide 24, Tirzepatide 24, Retatrutide 18 (eligible); AOD-9604 12 → Excluded.

**CLAIMED — next round (reserved 2026-06-19, peptide-library track) — THE FINAL TRIAGE:**
**Immune/longevity remainder + Mitochondrial class triage** — Epitalon, FOXO4-DRI, Humanin, SS-31 (Elamipretide),
MOTS-c — then deep-pass any eligible (SS-31/Elamipretide has real Stealth-BioTherapeutics human RCTs — watch for
eligibility). **This is the last untriaged set; after it the taxonomy is fully Done/Excluded** and the standing goal is met.
(COMPLETE: Healing; Metabolic; GH-secretagogue; Cognitive; **Sexual/dopaminergic** [PT-141 + Kisspeptin-10 Held; Melanotan II Excluded].
Immune/longevity: Thymosin Alpha-1 already Done — only Epitalon/FOXO4-DRI/Humanin remain.)

## Excluded (do not re-research without trigger)

Peptides actively excluded with reason. Trigger column = what would warrant reopening.

| Peptide | Reason | Re-open trigger |
|---|---|---|
| TB-500 | Triage 12/25 (2026-06-18). All human data are on a DIFFERENT molecule (topical/ophthalmic full-length Tβ4, RGN-259); the TB-500 fragment has zero human trials; gray-market-only sourcing. | A human RCT of the TB-500 fragment (or injectable Tβ4) on a tendon/joint/recovery endpoint. |
| GHK-Cu | Triage 11/25 (2026-06-18). Human evidence is topical-cosmetic only; the sole systemic-recovery data is one transient-effect rat ACL study; injectable use is gray-market + unmonitored copper load. | A human RCT of systemic/injectable GHK-Cu for a musculoskeletal-recovery endpoint. |
| KPV | Triage 12/25 (2026-06-18). Gut/inflammation (α-MSH) indicated; animal+in-vitro only; no tendon/joint data; zero human trials. | A verified human safety/efficacy study, or an explicit soft-tissue/recovery study. |
| LL-37 | Triage 12/25 (2026-06-18). Real topical-wound RCTs but off-goal; a larger Phase-IIb VLU trial reportedly failed; unresolved oncology dual-role; gray-market systemic sourcing. | A human RCT for a recovery/systemic indication with the oncology risk addressed. |
| Ipamorelin | Triage 16/25 → HOLD (2026-06-18). Only human RCT (post-op ileus) was negative on an off-goal endpoint; ZERO human body-composition/recovery/sleep data; no clean Rx pathway. | A human RCT on a body-composition / recovery / sleep endpoint. |
| AOD-9604 | Triage 12/25 (2026-06-18). The goal-defining human fat-loss claim is a non-indexed 2005 conference abstract (NO PMID/DOI — the circulating "2.6 kg" figure is unverifiable); the one large Phase-2b obesity trial FAILED; development abandoned 2007; FDA 503A Category-2 (nomination withdrawn 2024); WADA S2. Good short-term safety but evidentially hollow for weight loss. | A published, indexed human RCT showing a real weight-loss effect. |
| Sermorelin | Triage 16/25 → HOLD (2026-06-19). GHRH(1-29), was FDA-approved (Geref, discontinued ~2008 commercial). Adult body-comp RCT thin/mixed: Khorram 1997 (PMID 9141536) +1.26 kg LBM in men only (single-blind, n≈18) vs Vittone 1997 (PMID 9005976) NULL. Well-tolerated, IGF-1-monitorable, but compounded-only + WADA S2. The evidence-backed GHRH analog in this class = Tesamorelin (Done). | A modern adult body-composition/sleep RCT, or operator request for a full entry. |
| MK-677 (Ibutamoren) | Triage 15/25 → HOLD (2026-06-19). Real multi-year RCTs (evidence_tier A) reliably raise GH/IGF-1 + FFM +1.6 kg (Nass 2008, PMID 18981485) — BUT repeatedly FAILED to convert the surrogate to clinical benefit (Alzheimer's PMID 19015485; hip-fracture PMID 21067829 terminated early for a CHF safety signal), and causes insulin resistance + raised fasting glucose + edema. Never approved; gray-market; WADA S2. High-interest compound — revisit if operator wants a full entry. | New positive clinical-outcome RCT, or operator request for a full entry. |
| CJC-1295 (±DAC) | Triage 11/25 (2026-06-19). Surrogate PK/PD only — DAC form raised GH/IGF-1 (Teichman 2006, PMID 16352683); NO body-comp/sleep outcome RCT; no-DAC form essentially undocumented. Phase-2 HIV-lipodystrophy trial halted 2006 after a participant death (causality unadjudicated); DAC half-life 6–8 d (slow to clear AEs). Gray-market; WADA S2. | A clinical-outcome RCT + a resolved safety record. |
| Hexarelin | Triage 9/25 (2026-06-19). GHRP with real GH pharmacodynamics but the GH response DESENSITIZES with continued use (PMID 10990150) — undermining chronic use; no body-comp/outcome RCT; distinct CD36 cardiac activity (unquantified in humans); never approved; gray-market; WADA S2. | A clinical-outcome RCT overcoming the desensitization problem. |
| Semax | Triage 15/25 → HOLD (2026-06-19). Russian ACTH(4-10) analog, approved in Russia (stroke/cognitive). Efficacy evidence is Russian open-label (PMID 29798983, 110 stroke pts, Barthel/BDNF) + animal mechanism; the rigorous English data (PMID 30225715) is fMRI biomarker only — no blinded English cognitive RCT. Intranasal (fits no-clinic limit); gray-market in US (PCAC review ~2026). | A blinded English-language human cognitive RCT, or regulated US supply. |
| Selank | Triage 15/25 → HOLD (2026-06-19). Russian tuftsin-analog anxiolytic (approved Russia 2009, GAD). Small Russian active-comparator trials (PMID 18454096 vs medazepam; PMID 25176261 vs phenazepam, n=60) + animal GABAergic mechanism; no English RCT/meta. Good reported tolerability, intranasal; gray-market in US. **N-Acetyl-Selank-Amidate: NO admissible distinct evidence — not scored separately.** | A blinded English human RCT, or regulated supply. |
| Cerebrolysin | Triage 14/25 → HOLD (2026-06-19). Porcine brain-derived peptide mix; LARGE RCT base (CARS stroke PMID 26564102 positive) BUT Cochrane reviews null/weak with bias + a non-fatal-SAE signal (stroke PMID 37818733 "no further trials"; vascular dementia PMID 31710397). **IV/IM course administration conflicts with the no-clinic-visit limit**; approved in 50+ countries, NOT FDA. | A low-risk-of-bias positive RCT + a non-parenteral route, or operator request. |
| Dihexa | Triage 10/25 (2026-06-19). Ang-IV-derived c-Met/HGF activator — PRECLINICAL ONLY, no human data. Cornerstone evidence compromised: McCoy 2013 (PMID 23055539) carries a 2021 Notice of Concern; the mechanism paper Benoist 2014 was RETRACTED 2025 (PMID 40312093). Real oncogenic concern (c-Met activation); same-class clinical drug fosgonimeton failed Phase 2/3 (2024). Gray-market. evidence_tier D. | A clean human safety + efficacy trial resolving the oncogenic concern (unlikely). |
| N-Acetyl-Selank-Amidate | Triage (2026-06-19) — folded into Selank: **NO ADMISSIBLE DISTINCT PRIMARY EVIDENCE** (vendor/encyclopedia pages only); a gray-market Selank derivative. Excluded pending any distinct human data. | A distinct human study on the amidate variant specifically. |
| Kisspeptin-10 | Triage 17/25 → HOLD (2026-06-19). Real A-tier academic human evidence (Dhillo group: sexual brain processing + penile tumescence PMID 36735255 [KP-54]; LH/testosterone PMID 21632808 [KP-10]) — but KP-10's **~4-min half-life means it only works as a monitored IV infusion**; gray-market self-dosed "Kisspeptin-10" is a sourcing mismatch. Investigational, not approved. | A realistic monitored administration route + a libido-treatment RCT. |
| PT-141 (Bremelanotide) | Triage 16/25 → HOLD (2026-06-19). FDA-approved as **Vyleesi (2019) — but for FEMALE premenopausal HSDD** (RECONNECT Phase-3 PMID 31599840); **male use is off-label** with thin evidence. Lower-priority class for this user; cardiovascular-gated (transient BP rise — contraindicated in uncontrolled HTN/CVD; nausea 40%; focal hyperpigmentation). | A lab/clinical flag elevating the sexual-health goal + a BP-clean baseline; or male-specific evidence. |
| Melanotan II | Triage 8/25 (2026-06-19). Non-selective melanocortin agonist (tanning + erectile); NOT approved anywhere. Verified MELANOMA / mole-change case reports (PMID 21564053, 22724573) + ischemic priapism (PMID 33460908); MHRA warning (inaccurate dosing in every sample tested). evidence_tier D / risk HIGH (oncologic + urologic-emergency). The approved analog bremelanotide is the rigorous alternative. | (Effectively permanent exclude — superseded by bremelanotide; would need a wholly new safety profile.) |

## Done (compound page exists)

| Peptide | Compound page | Status |
|---|---|---|
| BPC-157 | [[compounds/bpc-157]] | **re-researched 2026-06-18 (deep mode, all gates attested PASS; prior 2026-05-23 entry archived — suspected fabricated citations). evidence_tier C / risk_tier experimental; no completed human RCT; ~85% single-lab (Sikiric/Zagreb) + 1 corroborating lab; FDA removed from Cat-2 ~Apr 2026 (FR 2026-07361) but unapproved + WADA-S0.** |
| Retatrutide | [[compounds/retatrutide]] | **deep pass 2026-06-19 (triage 18/25). evidence_tier B / risk_tier moderate. Triple GIP/GLP-1/glucagon agonist (LY3437943); highest-efficacy in class (Phase 2 −24.2%/48wk not plateaued; TRIUMPH-1 topline ~−28% but NOT peer-reviewed). FIRST-CLASS CAVEAT = SOURCING: INVESTIGATIONAL, not approved anywhere, NO legitimate prescription/compounding pathway → gray-market only; posture = WAIT FOR APPROVAL. Also incretin goal mismatch (lean −6.5 kg, no muscle RCT); thin long-term safety; dose-dependent HR rise (~+6.7 bpm). NOT separately WADA-listed. Review: PASS-with-fixes (applied).** |
| Tirzepatide | [[compounds/tirzepatide]] | **deep pass 2026-06-18 (triage 24/25). evidence_tier S / risk_tier moderate. Dual GIP/GLP-1 (GIP-biased); FDA-approved Mounjaro (T2D)/Zepbound (obesity + first-ever OSA drug, Dec 2024); most potent in class (SURMOUNT-1 −20.9%, beats semaglutide head-to-head SURMOUNT-5 −20.2% vs −13.7%). SAME FIRST-CLASS CAVEAT as semaglutide — GOAL MISMATCH: ~25% of mass lost is lean, reverses on stopping, NO muscle-building RCT (lean-sparing only via add-on anti-myostatin). Boxed thyroid-C-cell; GI AEs; NOT WADA-prohibited (Monitoring). Compounding wound down (shortage resolved Dec 2024). Review: PASS-with-fixes (applied).** |
| Semaglutide | [[compounds/semaglutide]] | **deep pass 2026-06-18 (triage 24/25). evidence_tier S / risk_tier moderate. GLP-1 RA, FDA-approved (Ozempic/Wegovy/Rybelsus); huge RCT base (STEP −14.9%, SELECT MACE HR 0.80, SUSTAIN-6, FLOW, STEP-HFpEF, ESSENCE). FIRST-CLASS CAVEAT: GOAL MISMATCH — a weight-loss drug that reduces lean mass + reverses on stopping; NO RCT for recovery/lean-building. Boxed thyroid-C-cell warning; GI AEs; NAION/pancreatitis signals. NOT WADA-prohibited (Monitoring Program). Compounded salt-forms not approved API; gray market winding down (shortage resolved Feb 2025). Review: clean PASS.** |
| Thymosin Alpha-1 | [[compounds/thymosin-alpha-1]] | **deep pass 2026-06-18 (triage 19/25). evidence_tier B / risk_tier low. Immune rebalancer (TLR→DC→Th1 + IDO/Treg); approved abroad ~30+ countries (NOT FDA-approved). FIRST-CLASS CAVEAT: the efficacy story shifted — best sepsis trial (TESTS, BMJ 2025, n=1089) is NEGATIVE; positive meta is a small-trial artifact. Goal-fit gap: NO RCT for general recovery in healthy adults. Removed from US 503A Cat-2 (Sept 2024). NOT WADA-prohibited (contrast TB-500). Very clean safety.** |
| Tesamorelin | [[compounds/tesamorelin]] | **deep pass 2026-06-18 (triage 21/25). evidence_tier A for HIV-lipodystrophy (Falutz NEJM 2007, Stanley JAMA 2014 / Lancet HIV 2019, Badran meta 2026) but effectively D for the operator's goal — population transfer: NO RCT in non-HIV/general/post-illness adults for body comp. FDA-approved (NDA 022505) HIV-only; EMA withdrawn 2012; WADA S2.2.4; 503A Cat-2. risk_tier moderate (IGF-1 + glucose monitoring; malignancy contraindication). Belongs on the doctor-handout queue, not a self-sourced protocol.** |

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
