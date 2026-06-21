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

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
