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

**ACTIVE SWEEP (operator directive 2026-06-19, peptide-library track) — DEEP-PASS EVERY PEPTIDE:**
Operator override of the two-pass triage model: **every peptide in the taxonomy gets a full
`/aplus-research --mode=deep` run** (no triage/ranking gate). Each finished entry ships via the
PR cycle. Deep-mode baselines (25+ sources / 10k words / 99 judge) hold; lower a ceiling ONLY
with a documented evidence reason in `_research-log.md` (e.g. "total admissible Tier-1/2
literature = N after exhaustive search"), never a guess.
Order (BPC-157 done): **TB-500 ✅** → **GHK-Cu ✅** → **KPV ✅** → **LL-37 ✅ (#181)** → **Ipamorelin ✅ (#185)** → **CJC-1295 ✅ (#186)** → **Tesamorelin ✅ (#188)** → **Sermorelin ✅ (#193)** → **Hexarelin ✅ (#194)** → **MK-677 ✅ (#195)** → **Semaglutide ✅ (#196)** → **Tirzepatide ✅ (#198)** → **Retatrutide ✅ (#200)** → **AOD-9604 ✅** → **Selank ✅ (PRIMARY LANE COMPLETE)**
→ Sermorelin → Hexarelin → MK-677 → Semaglutide → Tirzepatide → Retatrutide → AOD-9604 → Selank ✅
→ Semax → Cerebrolysin → Dihexa → N-Acetyl-Selank-Amidate → PT-141 → Melanotan-II → Kisspeptin-10
→ Thymosin-α1 → Epitalon → FOXO4-DRI → Humanin → SS-31 → MOTS-c.
**PRIMARY LANE COMPLETE (2026-06-20): Selank ✅ shipped — all top-12/primary-lane peptides done.** (Sweep split across two sessions 2026-06-20 — primary session: top 12 incl. LL-37/…/Retatrutide/AOD-9604/Selank✅; `feature/wiki-peptides`: bottom 13 [MOTS-c…Semax]. Neither deep-passes the other's set.) This sweep is the peptide-library track only — disjoint from the biomarker
wiki-research session (`feature/wiki-research`) and the plan-generation track
(`feature/compound-ae-screen`). See `_research-log.md` for per-entry DONE/CLAIMED status.

_(no scored rows yet — the reserved triage pass above produces the first ones.)_

## Excluded (do not re-research without trigger)

Peptides actively excluded with reason. Trigger column = what would warrant reopening.

| Peptide | Reason | Re-open trigger |
|---|---|---|
| _(none yet)_ | | |

## Done (compound page exists)

| Peptide | Compound page | Status |
|---|---|---|
| BPC-157 | [[compounds/bpc-157]] | **re-researched 2026-06-18 (deep mode, all gates attested PASS; prior 2026-05-23 entry archived — suspected fabricated citations). evidence_tier C / risk_tier experimental; no completed human RCT; ~85% single-lab (Sikiric/Zagreb) + 1 corroborating lab; FDA removed from interim §503A Cat-2 ~Apr 2026 (parallel FDA Cat-2 action; FR Doc 2026-07361 = the July-2026 PCAC meeting notice, not the removal action) but unapproved + WADA-S0.** |
| TB-500 (Tβ4) | [[compounds/tb-500]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; marketed product is the Ac-LKKTETQ fragment ≠ studied full-length Tβ4; no human RCT met a primary endpoint; zero athletic human evidence; bidirectional (net solid-tumor pro-metastatic) cancer signal; single-lab share ~20% but 100% of clinical-translation in Goldstein/RegeneRx nexus; FDA removed from interim §503A Cat-2 ~Apr 2026 (parallel FDA Cat-2 action, NOT approval; FR Doc 2026-07361 = the July-2026 PCAC meeting notice, not the removal action); WADA-S2.3.** |
| GHK-Cu | [[compounds/ghk-cu]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; human evidence TOPICAL-only (1 pos [Mulder] + 1 neg [Miller] RCT; no injectable/systemic human study); review-layer ~70-85% Pickart/Skin-Biology COI (efficacy-primary ~0.11); gene-reset/anti-cancer = cMap predictions; topical CIR-safe vs injectable copper-overload (Wilson's contraindication); WADA not-named (S0/S2 caveat).** |
| KPV | [[compounds/kpv]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; α-MSH(11-13) anti-inflammatory tripeptide, MC-receptor-independent / PepT1; ENTIRELY preclinical — zero human studies; ~75% gut-IBD primaries single-lab (Merlin/GSU); antimicrobial contested; acne/gout = KdPT/(CKPV)₂ analogues not monomer; KPV≠KdPT; FDA removed from Cat-2 ~Apr 2026 (NOT approval); WADA not-named (S0).** |
| LL-37 | [[compounds/ll-37]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib re-audit: 61/80 verified, 0 fabrications, 4 nits fixed). evidence_tier C / risk_tier experimental; human cathelicidin, genuinely DUAL-NATURED — antimicrobial/wound-healing AND psoriasis autoantigen / self-DNA→pDC→type-I-IFN disease driver + context-dependent cancer; 4 small human trials incl. Mahlapuu Phase IIb PRIMARY-NEGATIVE; FDA removed from Cat-2 ~Apr 2026 (NOT approval); WADA not-named (S0).** |
| Ipamorelin | [[compounds/ipamorelin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 18/18 verified, 0 fabrications, 1 PMID fixed). evidence_tier C / risk_tier experimental; NNC 26-0161 selective GH-secretagogue (no cortisol/prolactin — ANIMAL-grounded); only human efficacy program (postop-ileus Phase 2, Beck 2014) FAILED → development discontinued; no approval, zero human efficacy for marketed uses; ~80% Novo-Nordisk single-lineage; FDA never approved / PCAC voted against Oct 2024 / NOT in Apr-2026 action; WADA S2.2 prohibited.** |
| CJC-1295 | [[compounds/cjc-1295]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 16/16 verified, 0 fabrications, 0 fixes). evidence_tier C / risk_tier experimental; tetrasubstituted GRF(1-29) GHRH analogue = TWO molecules: WITH DAC (albumin-bound, t½ ~5.8–8.1 d, Teichman 2006) vs WITHOUT DAC = "Mod GRF 1-29" (~30 min, ipamorelin-stack partner) — never cross-attributed; only human efficacy program (ConjuChem with-DAC Phase II, NCT00267527) TERMINATED July 2006 after a participant death (causation NOT established); zero human efficacy endpoint ever met; ConjuChem single-lineage ~100% of efficacy/PK primaries; never approved / interim Cat-2 2023 / PCAC voted against Dec 4 2024 / NOT in the Apr-2026 removed-12; WADA S2.2.4 named.** |
| Tesamorelin | [[compounds/tesamorelin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 24/24 verified, 0 fabrications, 0 fixes). evidence_tier B / risk_tier medium — the ONLY FDA-APPROVED GHRH analogue (Egrifta/SV/WR, Theratechnologies); GHRH(1-44)+trans-3-hexenoyl; approved 2010 for HIV-lipodystrophy visceral-fat ONLY (Falutz Phase 3: ~15→18% VAT, visceral-selective, weight-neutral, reverses on stop); NAFLD/cognition INVESTIGATIONAL (mostly HIV+); general anti-aging/bodybuilding/fat-loss = ZERO human data (off-label); ~100% Theratechnologies single-sponsor; EMA withdrawn; WADA S2.2.4 named.** |
| Sermorelin | [[compounds/sermorelin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 17/17 verified, 0 fabrications, 0 fixes). evidence_tier B / risk_tier medium; GRF(1-29)NH2 = prototype GHRH fragment (CJC-1295 no-DAC is its analogue); WAS FDA-approved as Geref (diagnostic 1990 + pediatric-GHD 1997), WITHDRAWN ~2008 for COMMERCIAL reasons (FR 2013: NOT safety/effectiveness — "withdrawn"≠unsafe); evidenced use = pediatric-GHD + diagnostic; adult anti-aging = OFF-LABEL, 4 small old aging-adult studies (biomarker-level); §503A-compounded via component-of-formerly-approved-drug pathway; NOT in Apr-2026 removed-12; WADA S2.2.4 named. Baker-2012-is-tesamorelin guard held.** |
| Hexarelin | [[compounds/hexarelin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 22/23 verified, 1 author fixed, 0 fabrications). evidence_tier C / risk_tier experimental; GHRP = ghrelin-receptor (GHS-R1a) agonist + CD36 binder, NOT a GHRH analogue; DEFINING LIMITATION = tachyphylaxis (Rahim/Shalet 1998: ~45% GH-AUC decline over 16 wk, IGF-1 unchanged, reversible — acute GH ≠ durable effect); less selective than ipamorelin (cortisol/ACTH/prolactin); CD36 cardiac line GH-independent but mostly PRECLINICAL (human = acute inotropy only); body-comp/anti-aging/athletic = ZERO robust human data; never approved (Mediolanum Phase II discontinued); NOT in Apr-2026 removed-12; WADA S2.2.4 named.** |
| MK-677 (Ibutamoren) | [[compounds/mk-677]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 16/16 verified, 0 fabrications, 0 mismatches). evidence_tier B / risk_tier medium; ORAL non-peptidic small-molecule ghrelin-receptor (GHS-R1a) agonist — NOT a peptide, NOT a GHRH analogue; most-studied GH-secretagogue in long-term human RCTs; durably raises GH/IGF-1/lean mass (Nass 2008 FFM +1.1 kg) but NO strength/function gain; two disease programs FAILED (Alzheimer's Sevigny 2008 n=563; hip-fracture Adunsky 2011 + CHF signal ~6.5% vs 1.7%); biomarker↑≠benefit; DOMINANT risk = metabolic (glucose/insulin/HbA1c) + CHF; ~75% Merck-lineage; never approved / NOT a lawful dietary ingredient (FDA Dec-2025 letters); small-molecule NOT in the §503A peptide action; WADA S2 named.** |
| Semaglutide | [[compounds/semaglutide]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 19/19 verified, 0 fabrications, 0 mismatches). evidence_tier A / risk_tier medium — FIRST A-tier entry; acylated long-acting GLP-1 receptor agonist (Ozempic/Wegovy SC weekly + Rybelsus oral daily, Novo Nordisk); REAL benefits: glycemic (SUSTAIN), ~14.9% weight loss non-diabetic obesity (STEP-1) vs ~9.6% T2D, CV MACE −20% (SELECT, non-diabetic+CVD), renal (FLOW); REAL caveats: GI-dominant AEs, ~2/3 regain on stop, lean-mass loss, gallbladder/pancreatitis, rodent thyroid-C-cell boxed warning (not human-demonstrated), suicidality investigated-not-confirmed; SURMOUNT-OSA=tirzepatide (not miscredited); ~76% Novo single-sponsor; FDA-approved (2017/2019/2021); WADA NOT prohibited.** |
| Tirzepatide | [[compounds/tirzepatide]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 23/23 verified, 0 fabrications, 0 mismatches). evidence_tier A / risk_tier medium; dual GIP + GLP-1 agonist "twincretin" (Mounjaro T2D / Zepbound obesity+OSA, Eli Lilly) — distinct from semaglutide (GLP-1-only); REAL benefits: SURPASS-2 beat semaglutide 1 mg, ~20.9% weight loss non-diabetic obesity (SURMOUNT-1) vs ~14.7% T2D, OSA APPROVED (SURMOUNT-OSA, first FDA OSA drug), SURPASS-CVOT non-inferior (NOT superior); REAL caveats: GI-dominant AEs, ~14% regain on stop (SURMOUNT-4), lean-mass loss, gallbladder/pancreatitis, rodent thyroid-C-cell boxed warning (not human-demonstrated); ~95% Lilly single-sponsor; FDA-approved (2022/2023/2024); WADA NOT prohibited.** |
| Retatrutide | [[compounds/retatrutide]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 11/11 verified, 0 fabrications, 0 mismatches). evidence_tier B / risk_tier experimental; TRIPLE GIP+GLP-1+glucagon agonist (LY3437943, Eli Lilly), INVESTIGATIONAL — NOT approved; the LARGEST weight-loss signal yet (~24.2% Phase-2, Jastreboff 2023) but Phase-2-only, Phase 3 TRIUMPH ongoing (topline press-release-only, not verified); glucagon arm → dose-dependent heart-rate increase; Phase-2 signals cutaneous hyperesthesia ~7%/transient eGFR; MASH liver-fat −86% (imaging surrogate); ~100% Lilly single-sponsor; gray-market especially premature (no approved product); WADA NOT prohibited.** |
| AOD-9604 | [[compounds/aod-9604]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 6/6 verified, 0 fabrications, 0 mismatches). evidence_tier C / risk_tier experimental; synthetic hGH(176-191) "lipolytic fragment" (Metabolic Pharmaceuticals/Monash) marketed for fat loss; does NOT raise IGF-1/activate GH receptor (verified) BUT its pivotal Phase-2b obesity RCT FAILED placebo → obesity dev discontinued ~2007; lipolysis evidence preclinical-only, NO proven human fat loss; well-tolerated short-term but no long-term/SC-human data; OA pivot preclinical-only (Paradigm-OA=pentosan-NOT-AOD conflation excluded); ~100% single-lineage; never approved / self-affirmed-GRAS≠lawful-dietary-ingredient / NOT in Apr-2026 removed-12; WADA PROHIBITED (S0/S2, Essendon).** |
| Selank | [[compounds/selank]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 21/21 PMIDs verified, 0 fabrications, 0 fixes). evidence_tier C / risk_tier experimental; synthetic Tuftsin-analogue heptapeptide Thr-Lys-Pro-Arg-Pro-Gly-Pro (IMG RAS/Zakusov), Russia-REGISTERED intranasal anxiolytic (ЛСР-003338/09, 0.15%) but NOT FDA/EMA-approved; mechanism = enkephalinase inhibition + BDNF/monoamine/GABAergic modulation + Tuftsin-lineage immunomodulation; the no-sedation/no-dependence-vs-benzodiazepines claim is a Russian-clinical claim, honestly scoped (NOT Western-validated, no dedicated dependence trial); evidence predominantly Russian-language + ~100% single-lineage (IMG RAS/Zakusov) — limited independent Western replication surfaced first-class; Western counterweight Doyno & White 2021; §503A Selank-acetate removed from Cat-2 Sept 27 2024 → PCAC (NOT Cat-1, not lawfully compoundable); WADA NOT prohibited; kept DISTINCT from Semax and N-Acetyl-Selank-Amidate (the other session's). LAST primary-lane entry — primary lane COMPLETE.** |
| Dihexa | [[compounds/dihexa]] | **deep-passed 2026-06-22 (deep mode, all 9 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 11). evidence_tier D / risk_tier experimental — THE SWEEP'S MOST INTEGRITY-COMPROMISED ENTRY. N-hexanoyl-Tyr-Ile-(6)-aminohexanoic acid amide / PNB-0408 (PubChem CID 129010512, C₂₇H₄₄N₄O₅ MW 504.7); oral AngIV-derived peptidomimetic (WSU, Harding/Wright) marketed as an ultra-potent procognitive HGF/c-Met synaptogen. THE FOUNDATIONAL MECHANISM PAPERS ARE RETRACTED — Benoist 2014 (PMID 25187433) + Kawas 2012 (PMID 22129598), both retracted April 2025; McCoy 2013 (the dosing anchor, PMID 23055539) under a 2021 Expression of Concern — and the marketed "~100-million-times / 7-orders-more-potent-than-BDNF" figure traces to the RETRACTED paper (an in-vitro assay, originating-group). The only INDEPENDENT replication (Sun 2021, China Pharm Univ, APP/PS1 mice) found cognition via PI3K/AKT — NOT HGF/c-Met → the proposed mechanism has ZERO non-retracted, non-WSU support; a NULL result also exists (Wells 2024, 3-NP Huntington's rat). ZERO human efficacy/safety data (ClinicalTrials.gov 0 for dihexa). The related-but-DISTINCT clinical compound fosgonimeton/ATH-1017 (Athira→LeonaBio) FAILED ALL its trials (LIFT-AD n=554, ACT-AD, SHAPE) — its data do NOT transfer to grey-market Dihexa. LOAD-BEARING SAFETY tension: HGF/c-Met POTENTIATION is the exact pathway FDA-approved c-Met INHIBITORS (capmatinib/tepotinib) target as cancer drugs → a theoretical TUMOR-PROMOTION risk (no Dihexa carcinogenicity study; absence ≠ safety; concurrent c-Met-inhibitor use an ABSOLUTE contraindication; personal/family cancer history a precaution). Concentration ~67% WSU/Harding-Wright by headcount but the mechanism evidence is effectively single-group-AND-retracted; the Kawas data-integrity story carries a $4M DOJ False-Claims settlement (Jan 2025) + image-manipulation in the dissertation + ≥4 papers. Not-FDA-approved/not-compoundable; WADA NOT explicitly named (S0 Non-Approved catch-all — verify NADO). IRAP/AT4 (Albiston 2001, unretracted) a parallel candidate that does NOT establish the synaptogenic claims. Primary monitoring = clinical oncologic surveillance + [[biomarkers/igf-1]]/[[biomarkers/hs-crp]]/[[biomarkers/alt]]/[[biomarkers/ast]]; stop on any new/suspicious lesion. 3 languages surveyed (ZH/JP/RU) — 0 genuine non-English Dihexa primaries (Sun-2021 is English-published). Gate work: all 5 sections HALTed iter-1 (the documented-evidence-ceiling — fixed with explicit Tier-D ceiling declarations + handling-not-field re-judge — + integrity-completeness); 4.25 reconciled the LIFT-AD n (549→554) + the chemical name (hexanoic→hexanoyl); the layer-hygiene pass caught FABRICATED layer authors (a hallucinated 'Bhatt' author-list), off-enum retraction/eoc tags, a 4-notice-cite fold; iter-2 re-judges weathered a sustained ~25-min API overload with all state preserved on disk.** |
| Cerebrolysin | [[compounds/cerebrolysin]] | **deep-passed 2026-06-22 (deep mode, all 9 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 12). evidence_tier B / risk_tier medium — a nationally-approved (~50-country) porcine-brain peptide preparation (Ever Neuro Pharma, Austria; ~85% free AAs / ~15% <10kDa peptides; IV/IM) whose INDEPENDENT synthesis is null/cautious. COMPOSITION: 638 peptides by LC-MS but NO BDNF/GDNF/NGF/CNTF fragments → "neurotrophic mimicry" = functional analogy NOT growth-factor delivery (pharmacophore undefined). EFFICACY: a LARGE RCT corpus BUT CASTA (n=1070) NULL on primary + the independent 2023 Cochrane (7 RCTs n=1773) null on death/total-SAE AND a SIGNIFICANT non-fatal-SAE increase (RR 2.39, CI 1.10-5.23) at 30mL; VaD Cochrane positive-but-very-low-certainty; TBI CAPTAIN small-medium-unreplicated. TWO INTEGRITY AXES: (a) ~60-70% manufacturer (Ever-Pharma)-sponsored/affiliated (43-50% direct funding in the Cochrane sets), geography exclusively E-Europe+Asia, ZERO independent NA/UK/Scandinavian trials, the death-or-dependency primary endpoint absent from all 7 Cochrane stroke trials (selective-outcome-reporting); (b) RESEARCH MISCONDUCT — the EVER-cluster author Eliezer Masliah got an NIH ORI misconduct finding (Sept 2024, figure fabrication across 132 papers, 8 Cerebrolysin-specific) + 2 Rockenstein AD-model papers RETRACTED (PMID 25047000 ret-41382024 Dec-2025; 26611895 ret-40065222 Mar-2025) → the anti-amyloid/anti-tau AD-mechanism evidence substantially compromised (a Masliah-authored review's claims flagged provisional); EVER ex-GM Moessler co-authored 57 Cerebrolysin papers + co-founded a company w/ Masliah. REGULATORY: approved ~50 countries via NATIONAL procedures but NOT FDA-approved + NOT EMA-centrally-authorized; safety data sponsor-associated + from ELDERLY disease populations → a HEALTHY-ADULT population-mismatch (no controlled healthy-adult data); the non-fatal-SAE signal + hypersensitivity/anaphylactoid + the porcine-CNS prion-theoretical; WADA not-explicitly-prohibited (reasoned inference); grey-market injectable (no US/UK pathway, cold-chain/counterfeit/prion). monitoring clinical-infusion-hypersensitivity (primary) + [[biomarkers/egfr]] (renal). 3 non-English literatures surveyed (RU/ZH/DE — MANY primaries but REINFORCE-not-RESOLVE the concentration). THE GATES' BIGGEST CATCH OF THE SWEEP: the iter-2 D judge caught FABRICATED + misattributed citations (a fabricated porcine-prion paper resolving to a butterfly-genetics + a tsetse-fly paper; 4 author-misattributions; a Cureus entry) the iter-1 judge missed — repaired to eutils-verified real sources (the prion claim re-grounded on the REAL Wells 2003 J Gen Virol), then 4.75 IC-10 independently re-verified 12 PMIDs. THE BOTTOM LINE: a genuine nationally-approved drug, NOT a validated neuro-regenerative therapy for healthy-adult cognitive enhancement.** |
| Semax | [[compounds/semax]] | **deep-passed 2026-06-22 (deep mode, all 9 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 13 — THE FINAL ENTRY; SWEEP COMPLETE). evidence_tier C / risk_tier experimental. Met-Glu-His-Phe-Pro-Gly-Pro / MEHFPGP — a synthetic ACTH(4-7)-analog heptapeptide + a C-terminal Pro-Gly-Pro tail for proteolytic stability (IMG-RAS, Ashmarin/Myasoedov; intranasal 0.1%/1%); ACTH-derived but NON-corticotropic. The proposed BDNF/NGF-TrkB neurotrophin-cascade + melanocortin + neuroprotection mechanism is evidence_tier C (preclinical, predominantly rodent); the "regulatory peptide" paradigm is a Russian-school framework NOT Western-mainstream-accepted. Russia-registered for acute ischemic stroke + studied for cognitive/optic-neuropathy/ADHD, BUT every human study is OPEN-LABEL/non-randomized/inventor-affiliated/single-lineage — NO RCTs, NO Western trials, NO systematic reviews; the sole human BDNF signal (Gusev 2018, n=110) is a single open-label study (effect size + pre-registration NOT reported); the ADHD use traces to a single Medical Hypotheses paper. THE LOAD-BEARING SINGLE-LINEAGE CONCENTRATION — ~78-89% (8/9 verifiable English pubs) / ~90-95% of the mechanistic BDNF corpus traces to the IMG-RAS/Zakusov/Myasoedov-Ashmarin inventor cluster; 0/9 genuinely independent non-Russian; ZERO independent replication of the BDNF-induction mechanism (the only 2 Western papers = copper-chelation-chemistry + forensic-ID, no pharmacology); no confirmed receptor target; no human CNS bioavailability data; Peptogen (the manufacturer) is an IMG-RAS spinout → the science-producer = commercial-beneficiary (a BPC-157/Sikiric-parallel closed network — a STRUCTURAL concentration concern, NOT fraud/misconduct, unlike Cerebrolysin's Masliah axis or Dihexa's retractions). Russia-registered (ЖНВЛП/Vital&Essential, maintained by the Russian Ministry of Health NOT an independent HTA; approval ~09.08.2008) but NOT FDA + NOT EMA; the registration facts are author-reported (via the in-apparatus Deigin review) NOT a primary Russian filing; non-corticotropic safety; safety data single-lineage Russian open-label (no RCT/PK/long-term) → a HEALTHY-ADULT population-mismatch (no controlled healthy-adult data); WADA S0-catch-all-likely (reasoned inference); grey-market intranasal + the N-Acetyl-Semax-Amidate (NASA) analog (NEAR-ZERO independent evidence of its own; N-acetylation may ABOLISH the copper-chelation neuroprotection — worse, not better). monitoring cognitive-scale-primary (MoCA; no validated efficacy biomarker) + [[biomarkers/hs-crp]]. 4 non-English literatures surveyed (RU 10 primaries / UK 1 / ZH 0 / DE 0) — the 86-item Russian corpus REINFORCES rather than RESOLVES the single-lineage (only near-independent = Kurysheva-2001 ophthalmology; no placebo-controlled trial in any language). EVERY PMID eutils-verified at the source (the Cerebrolysin-fabrication lesson applied; a retrieval discarded a wrong perovskite-chemistry PMID proactively). THE BOTTOM LINE: a biologically-plausible Russia-registered neuropeptide with a 20-yr preclinical signal almost entirely single-lineage/open-label/unreplicated outside its inventor network — NOT a Western-validated nootropic.** |
| MOTS-c | [[compounds/mots-c]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` parallel-session bottom-13 sweep entry 1). evidence_tier C / risk_tier experimental; 16-aa mitochondrial-derived peptide (MT-RNR1), AMPK activator; efficacy ~entirely MOUSE (exogenous, n≤10); human data observational biomarker only, NO native-MOTS-c human trial (Phase-2a recruiting NCT07505745); foundational literature 100% single-group (Cohen/Lee USC) + CohBar COI; only human program = CB4211 analog (≠native, company-reported, discontinued 2023); WADA-prohibited (S4.4 AMPK class); FDA-unapproved + not 503A-compoundable (PCAC pending Jul 2026).** |
| SS-31 (Elamipretide) | [[compounds/ss-31]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 2). evidence_tier C / risk_tier experimental (off-label); Szeto-Schiller cardiolipin-binding mitochondrial tetrapeptide (FORZINITY/MTP-131/Bendavia). FDA accelerated approval Oct 30 2025 (NDA 215244) for BARTH SYNDROME ONLY — first approved mitochondria-targeting drug — but on uncontrolled OLE knee-strength (+63 N, n=8) while EVERY controlled trial missed its primary (MMPOWER-3/EMBRACE-STEMI/SPIHF-201/ReCLAIM-2/TAZPOWER-crossover); experimental for all off-label uses; ≥90% single-sponsor (Stealth→Mighty) + Szeto/Cornell COI; strong-preclinical/failed-clinical translation gap; well-tolerated (ISRs dominant); WADA exits S0 on approval. 5 Chinese-language primaries.** |
| Humanin | [[compounds/humanin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 3). evidence_tier C / risk_tier experimental; first-discovered mitochondrial-derived peptide (24-aa, MT-RNR2/16S rRNA, Hashimoto 2001); anti-apoptotic (Bax/IGFBP-3; FPR2 + CNTFR/WSX-1/gp130 — in-vitro/animal). Human evidence ENTIRELY OBSERVATIONAL biomarker (age-decline + CV/cognitive[HRS n=15,620]/MELAS associations) — NO human administration trial (any analog); causal direction unresolved (possible stress-marker). Efficacy mostly the S14G-HNG analog (~1000× native), not native. LOAD-BEARING: anti-apoptotic→PRO-TUMOR contraindication (TNBC + glioblastoma) → active/history malignancy precautionary contraindication. FDA-unapproved, never on 503A, WADA-S0. Concentration ~59% Keio+USC (largest single ~32%) — BELOW the 70% flag, genuine independent breadth. 8 non-English primaries (JP/ZH/RU).** |
| FOXO4-DRI | [[compounds/foxo4-dri]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 4). evidence_tier D / risk_tier experimental; senolytic D-retro-inverso peptide (~48-aa, FOXO4-forkhead + TAT CPP) disrupting FOXO4–p53 → releases p53 → selective senescent-cell apoptosis (Baar 2017 Cell). ALL efficacy PRECLINICAL (mouse + cell) — NO human trial, no human PK, no mouse lifespan endpoint (evidence_tier D, zero human data); behind D+Q/fisetin in translation. LOAD-BEARING: on-target off-tumor p53-activation (cardiotox flagged-but-unassessed, FOXO4 in heart/testis) + Born/Adnot 2023 Circulation ADVERSE finding (senolysis WORSENED pulmonary hypertension by clearing protective senescent endothelial cells); senescence has beneficial roles. FDA-unapproved/no-IND, never on 503A, WADA-S0. Concentration ~12.5% (de Keizer 1/8 primaries) — WELL BELOW flag, multi-continental independence; Cleara Biotech next-gen analogs, no registered trial. D-chirality UNVERIFIABLE by HPLC CoA; grey-market doses ~700-1400× below mouse-allometric equiv.** |
| Epitalon | [[compounds/epitalon]] | **deep-passed 2026-06-21 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 5). evidence_tier D / risk_tier experimental; AEDG tetrapeptide (Ala-Glu-Asp-Gly), synthetic analog of the Epithalamin pineal EXTRACT (Khavinson/St. Petersburg). Telomerase/telomere claim IN-VITRO-ONLY (Khavinson 2003 + independent Brunel 2025 — hTERT-in-normal vs ALT-pathway-in-cancer; no controlled in-vivo/human). Human longevity claims (1.6-4.1× mortality reduction) rest ENTIRELY on single-group Khavinson open-label/non-randomized studies, ZERO independent replication, AND used crude EPITHALAMIN EXTRACT ≠ synthetic AEDG. Concentration ≥80% Khavinson+Anisimov — ABOVE 70% flag; cytomedine paradigm not Western-accepted. LOAD-BEARING: telomerase→ONCOGENIC tension (telomerase = cancer hallmark; ALT finding deepens it) → active/prior malignancy contraindication. FDA-unapproved, 503A-removed-pending-PCAC (FR 91 FR 20465); Russian MoH approval = Epithalamin extract ONLY; WADA S0. 10 Russian-language primaries.** |
| Thymosin Alpha-1 | [[compounds/thymosin-alpha-1]] | **deep-passed 2026-06-21 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 6). evidence_tier B / risk_tier MEDIUM — the bottom-13's HIGHEST-evidence + ONLY non-experimental entry. Tα1/thymalfasin/Zadaxin, 28-aa prothymosin-α fragment; bidirectional immunomodulator (TLR9/TLR2 DC → Th1 + IDO/Treg). APPROVED in >35 countries (HBV/HCV/immunomodulation); genuine RCT evidence (HBV ~40% vs ~9%; vaccine-adjuvant immunogenicity); exceptional approved-drug safety (zero drug-related SAEs, >25-yr post-market). SEPSIS hype DEFLATED — ETASS (n=361) signal extinguished by the 2025 TESTS phase-3 (n~1100, SciClone, HR 0.99 p=0.93); COVID observational-only; NSCLC meta-analytic-only. NOT FDA-approved-US (orphan melanoma+HCC only; Dec-2024 PCAC 4-17-0 AGAINST 503A → off-limits for US compounders); WADA Tβ4-prohibited but Tα1-not-named. Concentration ~15-20% (≥8 independent groups) — BELOW flag, genuinely replicated. Anti-aging use = extrapolation. Tα1≠Tβ4 sourcing hazard. 18 non-English primaries (ZH 9/IT 3/RU 6).** |
| Kisspeptin-10 | [[compounds/kisspeptin-10]] | **deep-passed 2026-06-21 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact, bda 0-violation; `feature/wiki-peptides` bottom-13 sweep entry 7). evidence_tier C / risk_tier experimental. KP-10/YNWNSFGLRF-NH₂ (~1302 Da), the minimal active decapeptide of the KISS1 product; KISS1R/GPR54 agonist → GnRH → LH/FSH (master HPG-axis regulator). KP-10's OWN human data THIN (3 studies n≤10) — the substantial HPG/hypothalamic-amenorrhea/IVF evidence is KP-54 (distinct, longer t½ ~28-32min vs KP-10 ~4min), KP-10 efficacy EXTRAPOLATED (do not credit KP-54's evidence to KP-10). Sexual/limbic/HSDD evidence (the libido basis) = 5 high-quality RCTs but ALL single-center (Comninos/Dhillo Imperial), NOT independently replicated, surrogate endpoints (fMRI/tumescence/psychometric, no validated composite score; ~20% dropout women's IV-crossover). Bolus-stimulates / continuous-or-high-dose-DESENSITIZES (β-arrestin) — naive continuous grey-market dosing paradoxically SUPPRESSES the HPG axis (tachyphylaxis day-14, LH 24→2.5 IU/L). WADA S2.2.1 EXPLICITLY prohibited (testosterone-stimulating peptides, at all times); FDA-unapproved, 503A CLOSED (Oct-2024 PCAC 11-0 against KP-10). Concentration: broad field ~50% Imperial across 4 verified groups (BELOW flag) but the sexual sub-literature ~100% Imperial. PT-141/Vyleesi is the FDA-approved HSDD peptide (MC4R) — NOT KP-10. 18 non-English entries (JP 4/ZH 8/RU 6). Gate work: 4.25 caught a copy-pasted wrong author list (PMID 24517142) + transposed JAMA article number; added Ohtaki 2001 metastin source; removed unattested Monash group.** |

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
