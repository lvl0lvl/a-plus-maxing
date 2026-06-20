# ID-Reconcile Phase 4.25 — Resting Heart Rate
<!-- iteration: 2 -->

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

### Citations (shared entities appearing in 2+ sections)

| Citation | Sections | Verdict | Detail |
|----------|----------|---------|--------|
| D'Souza 2014 — PMID 24825544 | A, B, D | CONSISTENT | All three tag: `animal` — iteration-1 mismatch (D had `mechanism_review`) is resolved |
| Bent 2020 — PMID 32047863 | A, C | CONSISTENT | Both tag: `cohort` — iteration-1 mismatch (C had `mechanism_review`) is resolved |
| D'Ambrosio 2026 — PMID 41410046 | B, D | CONSISTENT | Both `cohort` tier-1; 38% HR≤40 figure stated in B, consistent framing in D |
| Dial 2025 — PMID 40834291 | A, B | CONSISTENT | Both `cohort`; Oura CCC 0.97–0.98 figure agrees in both sections |
| Strüven 2025 — PMID 40362779 | B, D | CONSISTENT | Baseline 63.6 bpm → 66.6 bpm, p<0.001, PMID, DOI identical in both sections |
| Hunter 2023 (ILI / B) + Mishra 2020 (COVID / D) | B, D | CONSISTENT | Different studies, same directional framing; no shared citation to conflict |
| Woodward (B) + Zhang/Aune (D) — mortality | B, D | CONSISTENT | Different studies, same direction (elevated RHR → higher mortality); no shared citation misquoted |

### Institutions

| Entity | Sections | Verdict |
|--------|----------|---------|
| No institution name appears in 2+ sections under different names | — | CONSISTENT |

### Compound Identifiers

| Entity | Sections | Verdict |
|--------|----------|---------|
| HCN4 channel ("funny current", If) | A, B, D | CONSISTENT — same name, same mechanism described |
| PPG (photoplethysmography) | A, C | CONSISTENT — same acronym, same physics description |
| 60–100 bpm normal range | A, B, D | CONSISTENT |
| 40–55 bpm athlete RHR range | A, B | CONSISTENT |
| Alcohol delta (63.6 → 66.6 bpm, +3.0 bpm) | B, D | CONSISTENT — identical figures |
| D'Ambrosio 38% ≤40 bpm Holter figure | B | Appears in B only; not repeated in D — no conflict |
| Mortality direction (elevated RHR = higher risk) | B, D | CONSISTENT — same direction and magnitude framing |

### Regulatory Dates

| Entity | Sections | Verdict |
|--------|----------|---------|
| 2018 ACC/AHA/HRS Guideline on Bradycardia | B | Only cited in B — no cross-section conflict |
| Apple Watch ECG De Novo clearance 2018 | C | Only cited in C — no cross-section conflict |

### Trial Registrations

| Entity | Sections | Verdict |
|--------|----------|---------|
| SIGNIFY trial (Fox 2014) | D only | Only cited in D — no cross-section conflict |
| Pro@Heart Consortium | B, D | CONSISTENT — same consortium name and study |

---

## Tally

| Class | Scanned | Mismatches |
|-------|---------|------------|
| Citations | 7 shared entities checked | 0 |
| Institutions | 0 cross-section shared names | 0 |
| Compound identifiers | 7 | 0 |
| Regulatory dates | 0 cross-section | 0 |
| Trial registrations | 1 cross-section | 0 |
| **Total** | **15** | **0** |

---

## Summary

Both iteration-1 HALT mismatches are now resolved: D'Souza 2014 (PMID 24825544) is tagged `animal` in sections A, B, and D; Bent 2020 (PMID 32047863) is tagged `cohort` in both sections A and C. All other shared entities — numerical figures (alcohol delta, Oura CCC, D'Ambrosio 38%), normal and athlete bpm ranges, mortality direction, compound identifiers, regulatory dates, and trial registrations — are consistent across sections with zero cross-section conflicts.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":7,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":7,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":1,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
