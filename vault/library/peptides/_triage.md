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

**Done this cycle (2026-06-18):** Healing/soft-tissue triage pass (all 4 ≤12 → Excluded) +
a GH-secretagogue/metabolic/immune triage round, then a **deep pass on the winner, Tesamorelin
(21/25) → Done.** Full scores: `tesamorelin/.provenance/triage-scores.md`.

Ranked queue (deep-pass-eligible, not yet deep-passed):
- `Thymosin Alpha-1 | immune/longevity | 19/25 | NEXT deep pass` — approved-abroad immunomodulator
  with real RCT/meta evidence for post-illness immune restoration; deep pass must flag (a) the
  negative pivotal sepsis trial (TESTS, BMJ 2025) and (b) uncertain US sourcing post-2024 FDA 503A removal.

**CLAIMED — next session (reserved 2026-06-18, peptide-library track):**
Deep pass on **Thymosin Alpha-1** (the ranked-queue top). Do NOT re-run BPC-157 or Tesamorelin.
See `_research-log.md` for the prep checklist + run invocation.

## Excluded (do not re-research without trigger)

Peptides actively excluded with reason. Trigger column = what would warrant reopening.

| Peptide | Reason | Re-open trigger |
|---|---|---|
| TB-500 | Triage 12/25 (2026-06-18). All human data are on a DIFFERENT molecule (topical/ophthalmic full-length Tβ4, RGN-259); the TB-500 fragment has zero human trials; gray-market-only sourcing. | A human RCT of the TB-500 fragment (or injectable Tβ4) on a tendon/joint/recovery endpoint. |
| GHK-Cu | Triage 11/25 (2026-06-18). Human evidence is topical-cosmetic only; the sole systemic-recovery data is one transient-effect rat ACL study; injectable use is gray-market + unmonitored copper load. | A human RCT of systemic/injectable GHK-Cu for a musculoskeletal-recovery endpoint. |
| KPV | Triage 12/25 (2026-06-18). Gut/inflammation (α-MSH) indicated; animal+in-vitro only; no tendon/joint data; zero human trials. | A verified human safety/efficacy study, or an explicit soft-tissue/recovery study. |
| LL-37 | Triage 12/25 (2026-06-18). Real topical-wound RCTs but off-goal; a larger Phase-IIb VLU trial reportedly failed; unresolved oncology dual-role; gray-market systemic sourcing. | A human RCT for a recovery/systemic indication with the oncology risk addressed. |
| Ipamorelin | Triage 16/25 → HOLD (2026-06-18). Only human RCT (post-op ileus) was negative on an off-goal endpoint; ZERO human body-composition/recovery/sleep data; no clean Rx pathway. | A human RCT on a body-composition / recovery / sleep endpoint. |

## Done (compound page exists)

| Peptide | Compound page | Status |
|---|---|---|
| BPC-157 | [[compounds/bpc-157]] | **re-researched 2026-06-18 (deep mode, all gates attested PASS; prior 2026-05-23 entry archived — suspected fabricated citations). evidence_tier C / risk_tier experimental; no completed human RCT; ~85% single-lab (Sikiric/Zagreb) + 1 corroborating lab; FDA removed from Cat-2 ~Apr 2026 (FR 2026-07361) but unapproved + WADA-S0.** |
| Tesamorelin | [[compounds/tesamorelin]] | **deep pass 2026-06-18 (triage 21/25). evidence_tier A for HIV-lipodystrophy (Falutz NEJM 2007, Stanley JAMA 2014 / Lancet HIV 2019, Badran meta 2026) but effectively D for the operator's goal — population transfer: NO RCT in non-HIV/general/post-illness adults for body comp. FDA-approved (NDA 022505) HIV-only; EMA withdrawn 2012; WADA S2.2.4; 503A Cat-2. risk_tier moderate (IGF-1 + glucose monitoring; malignancy contraindication). Belongs on the doctor-handout queue, not a self-sourced protocol.** |

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
