# ID-Reconcile Phase 4.25 — SHBG Biomarker Report

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity Class | Scanned | Mismatches | Notes |
|---|---|---|---|
| Citations (author+year+PMID) | 5 | 0 | Goldman 2017 / PMID 28673039 (A[4], C[1]): CONSISTENT — same authors, same PMID, same journal. Vermeulen 1999 / PMID 10523012 (B[8], C[6]): CONSISTENT — identical bibliographic entry in both sections. |
| Institutions | 0 | 0 | No institution names appear as shared entities across sections. |
| Compound identifiers | 6 | 0 | DHT, testosterone, estradiol, SHBG, HNF-4α/HNF4α (minor notation variant, not a conflict), FAI — all consistently named and defined. |
| Regulatory dates | 0 | 0 | No regulatory dates are shared across sections. |
| Trial registrations | 0 | 0 | No trial registration numbers appear in any section. |

**Total mismatches: 0**

---

## Detailed Entity-by-Entity Reconciliation

### 1. Affinity hierarchy DHT > T > E2
- **Section A** (physiology): explicit — "5α-dihydrotestosterone (DHT) > testosterone > 17β-estradiol" (line 33).
- **Section D** (determinants): implicit only — mentions androgen suppression of SHBG without restating the hierarchy. No contradiction.
- **Verdict:** CONSISTENT.

### 2. Insulin-suppresses-SHBG mechanism (A + D)
- **Section A**: "Insulin — the dominant acute suppressor; directly decreases HNF-4α activity and SHBG promoter transcription."
- **Section D**: "Insulin directly suppresses hepatic SHBG synthesis in a dose-dependent fashion by downregulating hepatic nuclear factor 4-alpha (HNF4α)."
- Minor notation variant: A uses "HNF-4α", D uses "HNF4α" — same protein, typographic difference only.
- **Verdict:** CONSISTENT.

### 3. ~44% testosterone-SHBG-bound figure (A + D)
- **Section A**: "SHBG-bound (~44%)" as a representative point estimate.
- **Section D**: "Approximately 44–65% of circulating testosterone is tightly bound to SHBG." Range includes A's value.
- **Section B**: "~40–60% in most adults." Also includes A's value.
- These represent different citation sources and population contexts giving ranges vs. point estimates; no section asserts a fact that another section contradicts.
- **Verdict:** CONSISTENT (overlapping ranges, not contradictory).

### 4. FAI formula (B + D)
- **Section B**: `FAI = (Total Testosterone [nmol/L] / SHBG [nmol/L]) × 100`
- **Section D**: `FAI = 100 × total T / SHBG`
- Mathematically identical; notation difference only.
- **Verdict:** CONSISTENT.

### 5. No SHBG harmonization / assay variation (C + D)
- **Section C (C.2)**: "SHBG has no equivalent widely-adopted reference-method standardization program." Inter-assay bias ±10–25%.
- **Section D (Limitations)**: "There is no international harmonisation standard for SHBG immunoassays; inter-laboratory CVs up to 15–25% have been reported."
- The CV ranges cited (C: ±10–25%; D: up to 15–25%) are sourced from different sub-studies and are overlapping, not contradictory.
- **Verdict:** CONSISTENT.

### 6. Goldman 2017 / PMID 28673039
- **Section A [4]**: "Goldman AL, Bhasin S, Wu FCW, Krishna M, Matsumoto AM, Jasuja R. (2017). A reappraisal of testosterone's binding in circulation: physiological and clinical implications. *Endocr Rev*. 2017 Aug 1;38(4):302–324. PMID: 28673039."
- **Section C [1]**: "Goldman AL, Bhasin S, Wu FCW, Krishna M, Matsumoto AM, Jasuja R. A reappraisal of testosterone's binding in circulation: physiological and clinical implications. *Endocr Rev.* 2017;38(4):302–324. PMID: 28673039."
- **Verdict:** CONSISTENT — identical authorship, PMID, volume/issue/pages.

### 7. Vermeulen 1999 / PMID 10523012
- **Section B [8]**: "Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012."
- **Section C [6]**: "Vermeulen A, Verdonck L, Kaufman JM. A critical evaluation of simple methods for the estimation of free testosterone in serum. *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012."
- **Verdict:** CONSISTENT — character-for-character match on all bibliographic fields.

### 8. Regulation lists (A) vs. Determinants lists (D)
- **Section A suppressors**: insulin, androgens, dietary monosaccharides, prolactin.
- **Section D "What Lowers SHBG"**: insulin resistance/hyperinsulinemia, obesity, T2D/MetS, NAFLD, androgens/AAS, glucocorticoids, hypothyroidism, GH excess/acromegaly, progestins, nephrotic syndrome.
- D is a superset of A with additional clinical detail; no item in A contradicts D.
- **Section A stimulators**: estrogens, thyroid hormone (T3/T4), tamoxifen/genistein/mitotane.
- **Section D "What Raises SHBG"**: aging, estrogens/OCPs/pregnancy, hyperthyroidism, hepatic cirrhosis, caloric restriction, anticonvulsants, HIV.
- Again D is broader; A's items appear consistently in D without contradiction.
- **Verdict:** CONSISTENT.

### 9. Reference intervals (B only)
- Men: 12.6–92.4 nmol/L (NHANES), 10–50 nmol/L (Quest), mean 31.8 ± 15.2 nmol/L.
- Women: 18.4–211.5 nmol/L (NHANES).
- Only B covers reference intervals; no cross-section conflict possible.

---

## Summary

Zero genuine cross-section disagreements found across all entity classes. Shared citations (Goldman 2017, Vermeulen 1999) are consistent in both PMID and bibliographic details. The affinity hierarchy, insulin-suppression mechanism, FAI formula, and no-harmonization point are all stated consistently across the relevant sections. Percentage ranges for SHBG-bound testosterone fraction vary across sections (reflecting different cited populations and sources) but are mutually inclusive, not contradictory.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":5,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":6,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
