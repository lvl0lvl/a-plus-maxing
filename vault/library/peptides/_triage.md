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
Order (BPC-157 done): **TB-500 ✅** → **GHK-Cu ✅** → **KPV ✅** → **LL-37 ✅ (PR #181)** → **Ipamorelin ✅** → CJC-1295 → Tesamorelin
→ Sermorelin → Hexarelin → MK-677 → Semaglutide → Tirzepatide → Retatrutide → AOD-9604 → Selank
→ Semax → Cerebrolysin → Dihexa → N-Acetyl-Selank-Amidate → PT-141 → Melanotan-II → Kisspeptin-10
→ Thymosin-α1 → Epitalon → FOXO4-DRI → Humanin → SS-31 → MOTS-c.
**Next (my/primary lane): CJC-1295.** (Sweep split across two sessions 2026-06-20 — primary session: top 12 incl. Ipamorelin✅; `feature/wiki-peptides`: bottom 13 [MOTS-c…Semax]. Neither deep-passes the other's set.) This sweep is the peptide-library track only — disjoint from the biomarker
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
| BPC-157 | [[compounds/bpc-157]] | **re-researched 2026-06-18 (deep mode, all gates attested PASS; prior 2026-05-23 entry archived — suspected fabricated citations). evidence_tier C / risk_tier experimental; no completed human RCT; ~85% single-lab (Sikiric/Zagreb) + 1 corroborating lab; FDA removed from Cat-2 ~Apr 2026 (FR 2026-07361) but unapproved + WADA-S0.** |
| TB-500 (Tβ4) | [[compounds/tb-500]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; marketed product is the Ac-LKKTETQ fragment ≠ studied full-length Tβ4; no human RCT met a primary endpoint; zero athletic human evidence; bidirectional (net solid-tumor pro-metastatic) cancer signal; single-lab share ~20% but 100% of clinical-translation in Goldstein/RegeneRx nexus; FDA removed from 503A Cat-2 ~Apr 2026 (FR 2026-07361, NOT approval); WADA-S2.3.** |
| GHK-Cu | [[compounds/ghk-cu]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; human evidence TOPICAL-only (1 pos [Mulder] + 1 neg [Miller] RCT; no injectable/systemic human study); review-layer ~70-85% Pickart/Skin-Biology COI (efficacy-primary ~0.11); gene-reset/anti-cancer = cMap predictions; topical CIR-safe vs injectable copper-overload (Wilson's contraindication); WADA not-named (S0/S2 caveat).** |
| KPV | [[compounds/kpv]] | **deep-passed 2026-06-19 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact). evidence_tier C / risk_tier experimental; α-MSH(11-13) anti-inflammatory tripeptide, MC-receptor-independent / PepT1; ENTIRELY preclinical — zero human studies; ~75% gut-IBD primaries single-lab (Merlin/GSU); antimicrobial contested; acne/gout = KdPT/(CKPV)₂ analogues not monomer; KPV≠KdPT; FDA removed from Cat-2 ~Apr 2026 (NOT approval); WADA not-named (S0).** |
| LL-37 | [[compounds/ll-37]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib re-audit: 61/80 verified, 0 fabrications, 4 nits fixed). evidence_tier C / risk_tier experimental; human cathelicidin, genuinely DUAL-NATURED — antimicrobial/wound-healing AND psoriasis autoantigen / self-DNA→pDC→type-I-IFN disease driver + context-dependent cancer; 4 small human trials incl. Mahlapuu Phase IIb PRIMARY-NEGATIVE; FDA removed from Cat-2 ~Apr 2026 (NOT approval); WADA not-named (S0).** |
| Ipamorelin | [[compounds/ipamorelin]] | **deep-passed 2026-06-20 (deep mode, all 7 gates attested PASS 2.75→8.5, chain intact; + independent full-bib audit 18/18 verified, 0 fabrications, 1 PMID fixed). evidence_tier C / risk_tier experimental; NNC 26-0161 selective GH-secretagogue (no cortisol/prolactin — ANIMAL-grounded); only human efficacy program (postop-ileus Phase 2, Beck 2014) FAILED → development discontinued; no approval, zero human efficacy for marketed uses; ~80% Novo-Nordisk single-lineage; FDA never approved / PCAC voted against Oct 2024 / NOT in Apr-2026 action; WADA S2.2 prohibited.** |

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
