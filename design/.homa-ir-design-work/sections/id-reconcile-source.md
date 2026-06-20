# ID-Reconcile Verification — Phase 4.25
# HOMA-IR Biomarker Report

## Verdict

verdict: PASS

All shared entities across sections A, B, C, and D are internally consistent. The previously halting mismatch (Wallace 2004 PMID in Section C) is resolved: all three citing sections (A, C, D) now carry PMID 15161807 with DOI 10.2337/diacare.27.6.1487.

---

## Per-Class Mismatch Table

| Entity Class | Entities Scanned | Mismatches | Detail |
|---|---|---|---|
| **Citations** | 9 (Matthews 1985 ×3, Levy 1998 ×2, Wallace 2004 ×3, Bonora 2000 ×1) | 0 | All PMIDs and DOIs agree within and across sections |
| **Institutions** | 3 (Oxford DTU references in A, B, C) | 0 | Naming varies in form but refers to the same unit consistently |
| **Compound identifiers** | 2 (formula constants 22.5, 405) | 0 | A and B agree; 22.5 × 18.0 = 405 confirmed algebraically in B |
| **Regulatory dates** | 0 | 0 | None present |
| **Trial registrations** | 0 | 0 | None present |

**Total mismatches: 0**

---

## Cross-Section Verification Detail

| Shared Entity | Sections | Result |
|---|---|---|
| Wallace 2004 — PMID 15161807, DOI 10.2337/diacare.27.6.1487 | A [3], C [3], D [6] | PASS (corrected from iteration 1) |
| Matthews 1985 — PMID 3899825, DOI 10.1007/BF00280883 | A [1], B [1], C [1] | PASS |
| Levy 1998 — PMID 9839117, DOI 10.2337/diacare.21.12.2191 | A [4], B [2] | PASS |
| Formula constant 22.5 (SI: 5 µIU/mL × 4.5 mmol/L) | A, B | PASS |
| Formula constant 405 (US: 22.5 × 18.0) | A, B | PASS |
| Oxford DTU as HOMA2 calculator source | A, B, C | PASS |
| No-universal-cutpoint stance | B, C, D | PASS |
| Hepatic IR selectivity of HOMA-IR | A, C, D | PASS |
| Assay non-standardization as core limitation | B, C, D | PASS |

---

## Summary

Iteration 2 finds zero mismatches. The sole Iteration 1 halt reason (`citation-mismatch`: Wallace 2004 PMID 15220194 in Section C) is resolved — Section C bibliography entry [3] now reads PMID 15161807, matching Sections A and D. All other shared entities (Matthews 1985, Levy 1998, formula constants 22.5/405, Oxford DTU, no-cutpoint stance) were consistent in Iteration 1 and remain so. Report is clear to proceed.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":9,"mismatch_count":0},"institutions":{"scanned":3,"mismatch_count":0},"compound_identifiers":{"scanned":2,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
