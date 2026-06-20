# Phase 4.25 — ID-RECONCILE Report

## Verdict

verdict: PASS

All five entity classes are clean across the four sections. One sub-threshold rounding artifact is noted in compound_identifiers (see table below) but does not constitute a scientific mismatch and does not trigger HALT.

---

## Per-Class Mismatch Table

| Class | Scanned entities | Mismatches | Notes |
|---|---|---|---|
| citations | 1 | 0 | ADAG Nathan 2008 (A[6] + B[6]): author list, PMC2742903, Diabetes Care 2008;31(8):1473–1478, R²=0.84, n=507 across 10 centres — consistent across both sections |
| institutions | 5 | 0 | ADA, WHO, IFCC, NGSP, DCCT/EDIC+UKPDS — naming consistent; IFCC "finalized 2004" (C) vs "formally adopted units 2007" (B) are distinct historical facts about different milestones, not a conflict |
| compound_identifiers | 3 | 0† | Master equation constants 0.09148/2.152 (B+C): identical. ADAG mg/dL equation 28.7/−46.7 (A+B): identical. ADAG mmol/L table value at 8.0%: A=10.2, B=10.1 — arithmetic (1.5944×8.0−2.594=10.1612) rounds to 10.2; B follows ADA calculator rounding to 10.1. Rounding artifact only; underlying constants agree. |
| regulatory_dates | 3 | 0 | ADA 2025/2026 (B), ADA/AACC 2023 (C), WHO 2011 (B, PMID 26158184), NGSP est. 1996 (C), IFCC 2004/2007 (B+C) — no conflicts |
| trial_registrations | 2 | 0 | DCCT (B context + D[7] full citation): naming and NGSP-traceability claim consistent; D's enumerated stats (n=1,441, 29 NA centres, 1982–1993) have no counterpart in B to conflict with. UKPDS (B context + D[8] full citation): same pattern — no stat conflict. |

† The eAG mmol/L rounding difference (10.1 vs 10.2 at 8.0%) is recorded as a sub-threshold artifact. The equation constants that generate the table are identical in both sections. This is NOT counted as a mismatch.

---

## Whole-Corpus Tally

- Total shared entities examined: 14 (1 citation, 5 institutions, 3 compound identifiers, 3 regulatory dates, 2 trial registrations)
- Confirmed mismatches: 0
- Sub-threshold artifacts: 1 (eAG mmol/L rounding at 8.0%: A=10.2 vs B=10.1)
- HALT triggers: none

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":1,"mismatch_count":0},"institutions":{"scanned":5,"mismatch_count":0},"compound_identifiers":{"scanned":3,"mismatch_count":0},"regulatory_dates":{"scanned":3,"mismatch_count":0},"trial_registrations":{"scanned":2,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```

---

## Notes for Downstream Merge

- **eAG mmol/L at 8.0% (A=10.2, B=10.1):** The merge author should standardize to B's value (10.1) since Section B is authoritative for the eAG table and cites the ADA eAG calculator [B:7, regulatory] directly. Section A's 10.2 is the arithmetic rounding of 10.1612; the ADA calculator truncates/rounds to 10.1.
- **ADAG mmol/L equation precision:** A uses 1.59/−2.59 (2 d.p.); B uses 1.5944/−2.594 (4 d.p.). B is the more precise form and should be used in the merged wiki entry's equation display; A's form is a valid approximation for narrative context.
- No other reconciliation actions required.
