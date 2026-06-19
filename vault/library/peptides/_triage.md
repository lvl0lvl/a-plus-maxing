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

**CLAIMED — next session (reserved 2026-06-18, peptide-library track):**
`Healing / soft-tissue triage pass` — shallow-scan + score the remaining four of the
flagged top class against `meta/goals.md`: **TB-500, GHK-Cu, KPV, LL-37** (BPC-157 is
already deep-passed → Done). Then deep-pass the top scorer (cap: 2 deep passes/session;
triage batches). **Do NOT** re-run BPC-157 or start a different class until this triage
pass lands. See `_research-log.md` for the prep checklist + the run invocation.

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

---

## How the agent uses this file

Per dispatch:
1. Agent reads `meta/goals.md` + this file → picks the next candidate from the queue (or runs a triage pass on the next class if queue is empty).
2. Refuses to research a peptide already in "Excluded" without explicit user override.
3. On report completion, moves the peptide to "Done" and notes the compound page link.
4. If a deep pass concludes "insufficient evidence," peptide moves to "Excluded" with reason `evidence-tier-D` and a re-open trigger of `new RCT published`.
