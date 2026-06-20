# ID-Reconcile Source — DHEA-S Phase 4.25 (Iteration 2)

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table (Iteration 2)

| Entity Class | Instances Scanned | Mismatches | Notes |
|---|---|---|---|
| citations | 0 | 0 | No shared citation identifiers (PMIDs, DOIs) appear in conflicting forms across sections |
| institutions | 0 | 0 | No institution names appear in conflicting forms across sections |
| compound_identifiers | 0 | 0 | DHEA-S spelled consistently; half-life now harmonized to ~7–10 h across A and C; unit conversion ×0.02714 consistent across B and C |
| regulatory_dates | 0 | 0 | No regulatory dates appear in conflicting forms |
| trial_registrations | 0 | 0 | No trial registration numbers appear across sections |

**Tally:** 0 mismatches across all 5 entity classes.

---

## Prior HALT Resolution

| Entity | Section A (prior) | Section C (prior) | Section C (current) | Status |
|---|---|---|---|---|
| DHEA-S plasma half-life | ~7–10 hours | ~10–20 hours | approximately 7–10 hours | RESOLVED |

The sole HALT from iteration 1 was the half-life disagreement. Section C now reads "on the order of approximately 7–10 hours," matching Section A's "approximately 7–10 hours." The mismatch is closed.

---

## Supplementary Shared-Entity Review

These entities span sections and were reviewed for completeness; none fall within the five enumerated ID-class checks.

| Entity | Sections | Values | Assessment |
|---|---|---|---|
| >700 µg/dL adrenal tumor flag | B, D | B: "above approximately 700 µg/dL (19.0 µmol/L)"; D: "above approximately 700 µg/dL" | AGREE |
| Unit conversion ×0.02714 | B, C | B: "µg/dL × 0.02714 = µmol/L"; C: "1 µg/dL = 0.02714 µmol/L" | AGREE |
| No diurnal variation | A, C | A: "minimal diurnal fluctuation"; C: "no clinically significant diurnal variation" | AGREE — consistent framing |
| Old-age DHEA-S as % of peak | A, B | A: "10–20% of the young adult peak"; B: "10–20% of youthful peak concentrations" | AGREE |
| Hyperandrogenism adrenal-source localization | B, D | Both: DHEA-S near-exclusive adrenal origin; adrenal vs. ovarian differential logic consistent | AGREE |
| Age-decline rate | A, B, D | A: "~2–3% per year"; B: "approximately 2–5% per year"; D: "approximately 2–5% per year" | Pre-existing minor range variation; B and D internally consistent; A's narrower estimate is not contradictory in the clinical literature. Falls outside the five enumerated ID-class checks. Not introduced by this iteration. |

---

## Summary

The prior HALT is resolved: Section C now reads "approximately 7–10 hours," agreeing with Section A. All five enumerated entity classes scan at zero mismatches across Sections A–D. The supplementary review finds agreement on all clinically load-bearing figures. The pre-existing 2–3% vs 2–5%/year rate-of-decline spread between Section A and Sections B/D is a minor numeric range present before this iteration, outside the enumerated ID classes, and does not constitute a reconcile failure.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":0,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":0,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
