# ID-RECONCILE — Phase 4.25
Recovery/Strain Composite-Score Wearable Report
Sections scanned: A, B, C, D — iteration 2 (prior iteration HALTed on 4 cross-section COI-disclosure inconsistencies)

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

(empty — no mismatches)

| Entity class | Entity | Sections | Mismatch | Status |
|---|---|---|---|---|
| _(none)_ | — | — | — | PASS |

---

## Reconciliation Detail (informational)

### The 4 previously-HALTing COI disclosures — re-checked, now consistent

| Study | PMID | Required COI note | A | B | C | D | Result |
|---|---|---|---|---|---|---|---|
| Bellenger 2021 | 34065516 | independent validation; ARC/AIS-funded (NOT WHOOP-funded) | [10] ✓ | [5] ✓ | not cited | [11] ✓ | consistent |
| Bellenger 2022 | 36146073 | WHOOP-funded ("authors received research support from WHOOP Inc.") | [7] ✓ | [6] ✓ | [3] ✓ | [12] ✓ | consistent |
| Miller 2022 | 36016077 | WHOOP-funded ("WHOOP Inc. research support") | [4] ✓ | not cited | [4] ✓ | not cited | consistent |
| Spetz 2025 | 41369808 | svexa-equity COI, tier 3 | not cited | [3] ✓ tier 3 | [8] ✓ tier 3 | not cited | consistent |

Iteration-1 HALT-1..HALT-4 are all resolved. The prior mischaracterization of Bellenger 2021 as WHOOP-funded is corrected via full-text everywhere it appears (now uniformly the independent ARC/AIS-funded validation). Bellenger 2022 carries the WHOOP-funded note in all four sections; Miller 2022 in both A and C; Spetz 2025 carries the svexa-equity COI and tier 3 in both B and C (the iteration-1 B-was-tier-2 divergence is gone).

### Two distinct Dial papers (correctly separated)

| Paper | PMID | Title stem | tag | tier | Appears in |
|---|---|---|---|---|---|
| Dial — validation | 40834291 | "Validation of nocturnal resting heart rate and heart rate variability…" | cohort | 2 | A[3], C[10] |
| Dial — transparency | 41399178 | "Contextual equivalence … requires transparency" | mechanism_review | 2 | C[5] |

A[3] and C[10] both point to 40834291 (validation); C[5] is the distinct 41399178 (transparency). Never conflated. The WHOOP/Polar/Oura concordance numerics (WHOOP CCC 0.94 MAPE 8.17%; Polar CCC 0.82 MAPE 16.32%) appear only in Section A and are attributed there to the Dial validation paper [3]=40834291. Section B's Bellenger 2021 [5] carries only the qualitative WHOOP-PPG "smallest worthwhile change" claim and no Polar/MAPE figures, so no cross-section numeric collision exists.

### Tag/tier consistency across all shared PMIDs

| PMID | A | B | C | D | Consistent |
|---|---|---|---|---|---|
| 34065516 (Bellenger 2021) | cohort/2 | cohort/2 | — | cohort/2 | ✓ |
| 36146073 (Bellenger 2022) | cohort/2 | cohort/2 | cohort/2 | cohort/2 | ✓ |
| 36016077 (Miller 2022) | cohort/2 | — | cohort/2 | — | ✓ |
| 41369808 (Spetz 2025) | — | cohort/3 | cohort/3 | — | ✓ |
| 40834291 (Dial validation) | cohort/2 | — | cohort/2 | — | ✓ |
| 41399178 (Dial transparency) | — | — | mechanism_review/2 | — | ✓ (single appearance) |
| 39860902 (Nuuttila 2025) | cohort/2 | cohort/2 | — | — | ✓ |

---

## Mismatch Tally

| Class | Scanned | Mismatch count |
|---|---|---|
| Citations (shared entities) | 6 | 0 |
| Institutions / funders | 3 (WHOOP Inc., ARC/AIS, svexa) | 0 |
| Compound identifiers | 0 | 0 |
| Regulatory dates | 0 | 0 |
| Trial registrations | 0 | 0 |

---

## Advisory Flags (non-halting, carried from iteration 1)

**Buchheit 2014 tier divergence** — cited as `mechanism_review / tier 2` in C[1] and `mechanism_review / tier 3` in D[5] (no PMID in either entry; DOI 10.3389/fphys.2014.00073 consistent in D). This does not meet a defined `halt_reason` enum category (it is a tier annotation difference on a non-vendor, COI-free review cited for different sub-claims), so it does not block PASS — but should be tiered consistently in synthesis or annotated for the deviation.

---

## Summary

All four cross-section COI-disclosure inconsistencies that HALTed iteration 1 are fixed: Bellenger 2021 (34065516) reads "independent; ARC/AIS-funded (not WHOOP-funded)" in A/B/D, Bellenger 2022 (36146073) reads WHOOP-funded in A/B/C/D, Miller 2022 (36016077) reads WHOOP-funded in A/C, and Spetz 2025 (41369808) reads svexa-equity tier 3 in B/C; the two Dial papers (40834291 validation, 41399178 transparency) stay distinct and every shared tag/tier/numeric reconciles. The only residual is the non-halting Buchheit 2014 tier-annotation advisory.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":0,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
