## Verdict

verdict: PASS

All shared entities across sections A, B, C, and D are consistent. The previously flagged Marcovina 2007 sub-analysis denominator mismatch (B said "9 of 12", C said "9 of 10") is resolved: every sub-analysis count in section B now uses "of 10", matching section C and the paper's structure (12-method headline, 10-method sub-analyses).

---

## Per-Class Mismatch Table

| Entity class | Shared entities scanned | Mismatches | Detail |
|---|---|---|---|
| **Citations** | 6 | 0 | B[2] and C[1] both cite Marcovina 2007 Clin Chem 53(4):711-716 identically. D[15] is a distinct 2010 Diabetes Care paper — not a conflict. Brazilian reference paper cited consistently (A uses PMID 39529982, B uses PMC11554367 — same article). |
| **Institutions** | 3 (ADA in B+C+D; IFCC in C; JCTLM in C) | 0 | All used consistently within section scope; no cross-section name divergence. |
| **Compound identifiers** | 4 (HOMA-IR denominators 22.5/405 in A+B; ×6.0 conversion in A+B; inter/within-assay CVs in B+C+D; des-(64,65) cross-reactivity denominator in B+C) | 0 | des-(64,65) denominator now "9 of 10" in both B and C. HOMA-IR 22.5/405 are the same formula in different glucose units (explicitly noted in B). 6.0 vs 6.00 is notation equivalence. |
| **Regulatory dates** | 0 | 0 | No datestamped regulatory milestones appear as shared entities across sections. |
| **Trial/cohort registrations** | 1 (NHANES referenced in B+D) | 0 | B and D reference different NHANES cycles for different outcomes; no numerical conflict. |

---

## Tally

- Entity classes scanned: 5
- Total shared entity instances examined: 14
- Mismatches: **0**
- Halt reasons: none

---

## Marcovina Sub-Count Reconciliation Detail

Prior iteration (1) HALT reason: B had "9 of 12" for des-(64,65) proinsulin cross-reactivity, while C had "9 of 10".

Current state (iteration 2, post-correction):

| Sub-analysis | Section B | Section C | Agreement |
|---|---|---|---|
| Within-assay CV (≤10.6%) | 7 of 10 | 7 of 10 | ✓ |
| Clinical acceptability (total error ≤32%) | 6 of 10 | (not repeated in C) | ✓ |
| Des-(64,65) proinsulin cross-reactivity >40% | **9 of 10** | 9 of 10 | ✓ — RESOLVED |
| Intact proinsulin <2% | 9 of 10 (C.4 only) | 9 of 10 | ✓ |
| Split (32,33) proinsulin <3% | 8 of 10 (C.4 only) | 8 of 10 | ✓ |

No "of 12" fragment remains in any sub-analysis count across either section.

---

## Brazilian Reference Values Cross-Check

| Value | Section A | Section B |
|---|---|---|
| Overall range (µIU/mL) | 2.52–13.14 | 2.52–13.14 |
| Overall range (pmol/L) | 15.1–78.8 | 15.1–78.8 |
| Conversion check | 2.52 × 6.0 = 15.12 ✓; 13.14 × 6.0 = 78.84 ✓ | — |

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":3,"mismatch_count":0},"compound_identifiers":{"scanned":4,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":1,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
