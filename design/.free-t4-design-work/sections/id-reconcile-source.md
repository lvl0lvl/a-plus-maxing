# ID-RECONCILE Phase 4.25 — Free T4 Report
<!-- iteration 2 -->

## Verdict

verdict: PASS

## Per-Class Mismatch Table

| Entity Class | Entities Scanned | Mismatches |
|---|---|---|
| citations | 14 | 0 |
| institutions | 3 (IFCC, ATA, NACB) | 0 |
| compound_identifiers | 8 (fT4, TBG, TTR, T3, T4, rT3, unit conversion ×12.87, PMID tokens) | 0 |
| regulatory_dates | 3 (2017 ATA pregnancy guidelines, 2014 ATA hypothyroidism guidelines, 2016 ATA hyperthyroidism guidelines) | 0 |
| trial_registrations | 0 | 0 |

## Mismatch Detail

None. All entity classes are clean.

## Tally

- Total entities scanned: 28
- Total mismatches: 0
- Halt reasons: none

## Reconciliation Notes

**Khoo 2020 (PMID 32213658) — resolved from iteration 1 HALT.**
Section C [ref 9] and Section D [ref 6] now read identically: "Khoo S, Lyons G, McGowan A, et al. Familial dysalbuminaemic hyperthyroxinaemia interferes with current free thyroid hormone immunoassay methods. *Eur J Endocrinol.* 2020;182(6):533–538. PMID: 32213658. DOI: 10.1530/EJE-19-1021." The volume/issue/pages discrepancy that triggered the iteration-1 HALT is gone.

**×12.87 conversion:** Section A ("ng/dL × 12.87 = pmol/L") and Section B ("1 ng/dL = 12.87 pmol/L") agree. Sections C and D use both units without restating the factor; no conflict.

**Reference intervals:** Section A's broader physiological range "0.7–1.9 ng/dL (9–24 pmol/L)" and the immunoassay-specific "12–22 pmol/L (0.93–1.71 ng/dL)" are presented as distinct concepts within Section A itself. Sections B, C, and D's "0.8–1.8 ng/dL (10–23 pmol/L)" is the method-specific immunoassay interval; this is consistent with — not contradictory to — Section A.

**Koulouri PMID 24275187:** Author list, journal, year, volume, issue, pages, PMID, and DOI identical in Sections A [ref 6] and C [ref 11].

**Lee PMID 19114271:** Author list, title, journal, year, volume, issue, and pages identical in Sections C [ref 13] and D [ref 12]. Section D omits the DOI; no conflicting data present.

**TSH/fT4 diagnostic grid:** Section B five-row table and Section D prose descriptions agree on all five patterns (overt primary hypothyroidism, subclinical hypothyroidism, overt hyperthyroidism, subclinical hyperthyroidism, central hypothyroidism).

**Central hypothyroidism framing:** Sections A, B, and D agree: low fT4 with low-to-normal TSH; TSH unreliable in this setting; fT4 is the primary monitor for levothyroxine therapy in central hypothyroidism.

**Method-dependence:** All four sections agree that fT4 immunoassay results are method-specific, non-transferable across platforms, and that equilibrium dialysis + ID-LC-MS/MS is the IFCC reference procedure.

## Machine-Readable Block

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":14,"mismatch_count":0},"institutions":{"scanned":3,"mismatch_count":0},"compound_identifiers":{"scanned":8,"mismatch_count":0},"regulatory_dates":{"scanned":3,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```

## Summary

All shared cross-section entities pass. The Khoo 2020 (PMID 32213658) citation that halted iteration 1 now reads identically in Sections C and D. No new mismatches were found across any entity class. The report is clear for ingestion.
