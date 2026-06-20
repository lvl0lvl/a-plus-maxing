# ID-Reconcile Phase 4.25 — eGFR / Creatinine (Iteration 2)

## Verdict

verdict: PASS

## Per-Class Mismatch Table

| Entity class | Instances scanned | Mismatches | Notes |
|---|---|---|---|
| citations | 6 | 0 | Inker 2021 PMID 34554658 consistent A[6]/B[3]; Lepist 2014 consistent A[10]/C[8]; KDIGO editions differ appropriately by content scope (2012 vs 2024) — no conflict |
| institutions | 3 | 0 | CKD-EPI Collaboration, KDIGO, CKD-PC — named consistently across all sections |
| compound_identifiers | 5 | 0 | OAT2/SLC22A7, OCT2/SLC22A2, OCT3/SLC22A3, MATE1/SLC47A1, MATE2-K/SLC47A2 — hierarchy consistent across A, C, D; B out of scope for transporter content |
| regulatory_dates | 3 | 0 | KDIGO 2012 (AKI, D only), KDIGO 2024 (CKD staging, B+D consistent), NKDEP 2006 (C only) — no cross-section conflict |
| trial_registrations | 0 | 0 | None present in any section |

**Total mismatches: 0**

## Harmonization Confirmation

**Transporter hierarchy (the prior HALT item):** Sections A, C, and D now present an identical hierarchy — basolateral OAT2 (SLC22A7) / OCT2 (SLC22A2) / OCT3 (SLC22A3), apical MATE1 (SLC47A1) / MATE2-K (SLC47A2) — with OAT2 highest in-vitro per Lepist 2014 (hedged, not settled in-vivo primacy), and OCT2 as the clinically cited drug-inhibition locus. Section A now cites Lepist [10] for transporter mechanism; Thompson [3] is scoped to the quantitative secreted-fraction and CKD-amplification claims only. Section B does not cover tubular secretion transporters (equations/staging scope); no omission conflict.

**Other shared entities reviewed and confirmed consistent:** Inker 2021 PMID 34554658 (journal, volume, pages, PMID match across A and B); KDIGO G1–G5 staging thresholds (B and D identical — G1 ≥90, G2 60–89, G3a 45–59, G3b 30–44, G4 15–29, G5 <15); creatinine-blind range (A and D descriptions complementary, not contradictory; no entity-class conflict); units ×88.4 (B defines, A's µmol/L conversions verify arithmetically: 0.9 mg/dL → 80 µmol/L ✓, 1.8 mg/dL → 159 µmol/L ✓); Matsushita 2010 PMID 20483451 (internally consistent within D, not cross-cited — no conflict); Lepist 2014 full citation (A[10] and C[8] agree on all bibliographic fields — same authors, title, journal, volume, issue, pages, DOI).

**Out-of-scope observations (not halt-triggering):** Cystatin C molecular weight reported as 13.3 kDa (A) vs 13 kDa (C) — rounding difference in a physical property, not a compound-identifier class mismatch. Secreted fraction range 10–15% (A/Thompson) vs 10–40% (C/Lepist) — different sources cited for different quantitative claims; each cites its own source, no citation conflict.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":3,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":3,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
