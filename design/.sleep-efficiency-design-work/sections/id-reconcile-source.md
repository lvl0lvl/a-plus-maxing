# ID-Reconcile Phase 4.25 — Sleep Efficiency (Iteration 2)

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

*(empty — no mismatches)*

| Entity Class | Scanned | Mismatches | Notes |
|---|---|---|---|
| Citations | 12 | 0 | — |
| Institutions | 4 | 0 | — |
| Compound identifiers | 0 | 0 | — |
| Regulatory dates | 3 | 0 | — |
| Trial registrations | 0 | 0 | — |

**Total mismatches: 0**

---

## Entities Checked

**AASM Scoring Manual version** (was the iteration-1 HALT reason):
- Section A ref 1: "Version 3. Darien, IL: AASM, 2023" — PASS
- Section C ref 1: "Version 3. Darien, IL: AASM, 2023" — PASS
- Iteration-1 mismatch (A=v2.6/2020 vs C=v3/2023) is resolved. Both sections now cite Version 3, 2023.

**Chinoy 2021 (PMID 33378539) — cohort — wake-specificity ranges:**
- Section A: 7 devices, wake specificity 0.18–0.54, Fitbit Alta HR best at 0.54, Garmin worst at 0.18–0.19.
- Section C: identical range, Garmin Fenix 5S 0.18, Fitbit Alta HR 0.54.
- Section D: cites "seven consumer devices" and SE overestimation direction consistently.
- MATCH across all three sections.

**de Zambotti 2024 Sleep (PMID 38149978) — mechanism_review:**
- Section A ref 9: *Sleep* 2024;47(4):zsad325, PMID 38149978, tag mechanism_review.
- Section C ref 5: *Sleep* 2024 Apr 12;47(4):zsad325, PMID 38149978, tag mechanism_review.
- MATCH.

**≥85% SE norm:**
- Section B: NSF consensus (Ohayon 2017, PMID 28346153), SE >85% = "appropriate". Tagged regulatory.
- Section D: AASM guideline (Sateia 2017, PMID 27998379), SE <85% = continuity concern. Tagged regulatory.
- Different source documents; the 85% threshold is concordant. MATCH.

**CBT-I / SRT raises SE:**
- Section B: Altena 2023 (ref 5), Stanyer 2026 (ref 7) — mechanistic and SRT-focused.
- Section D: Maurer 2021 meta-analysis (Hedges' g = 0.91), Edinger 2021 AASM guideline.
- Consistent direction and magnitude. MATCH.

---

## Summary

The single iteration-1 HALT reason — AASM Scoring Manual version conflict (Section A v2.6/2020 vs Section C v3/2023) — is resolved: Section A now cites Version 3 (2023), matching Section C. All other shared entities (Chinoy 2021 cohort, de Zambotti 2024 mechanism review, the ≥85% SE norm, CBT-I/SRT claim) are consistent across sections. No new mismatches detected.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":12,"mismatch_count":0},"institutions":{"scanned":4,"mismatch_count":0},"compound_identifiers":{"scanned":0,"mismatch_count":0},"regulatory_dates":{"scanned":3,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
