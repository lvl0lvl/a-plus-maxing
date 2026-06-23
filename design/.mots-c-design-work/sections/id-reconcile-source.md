## Phase 4.25 — Cross-Section ID Reconciliation Gate (Iteration 3 — FINAL)

**Run date:** 2026-06-20
**Scope:** Sections A–E; final scan verifying iter-2 fixes (WADA date in §C removed; NCT07505745 tag in §D corrected to regulatory)

## Verdict

verdict: PASS

```json
{"phase":"4.25","verdict":"PASS","iterations":3,"entity_classes":{"citations":{"scanned":10,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":3,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":4,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":4,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":2,"mismatch_count":0,"mismatches":[]}},"halt_reasons":[]}
```

---

## Iter-2 Fix Verification

| Fix | Expected state after iter-2 | Observed | Verified? |
|-----|---------------------------|----------|-----------|
| WADA date — Section C's erroneous "January 2024" sentence removed + cross-reference to §D added | Section C body: no "January 2024" date claim; §D carries authoritative "effective January 1, 2026" | Confirmed: Section C line 39 defers to §D ("MOTS-c's WADA status — prohibited as an AMPK-activator metabolic modulator — is covered authoritatively in §D"); no "January 2024" appears anywhere in §C | YES |
| NCT07505745 tag in Section D [12] corrected from `open_label` to `regulatory` | D bib [12]: `tag: regulatory` | Section D bib [12]: "tag: regulatory — tier: 1" | YES |

Both iter-2 fixes confirmed resolved.

---

## Per-Class Prose Tables

### Citations (10 entities scanned, 0 mismatches)

| PMID / ID | Entity | Sections | Tag (all) | Tier (all) | Consistent? | Notes |
|---|---|---|---|---|---|---|
| 25738459 | Lee 2015, Cell Metab | A[1], B[1], C[4], D[3], E[1] | animal | 1 | YES | All 5 sections agree; author abbreviation in B/D acceptable |
| 29983246 | Kim KH 2018, Cell Metab | A[2], E[3] | in_vitro | 1 | YES | — |
| 33473109 | Reynolds 2021, Nat Commun | A[3], C[1], E[4] | animal | 1 | YES | §C prose uses [1, cohort] inline for human exercise data subset — intra-section dual-tagging of a paper containing both human observational and animal treatment data; bibliography entry tagged animal in all three sections. Not a cross-section conflict. |
| 26289118 | Fuku 2015, Aging Cell | A[4], C[6] | mechanism_review | 3 | YES | Page range "921–923" (A) vs "921-3" (C) — abbreviation variant only |
| 33468709 | Zempo 2021, Aging (Albany NY) | A[5], C[7] | cohort | 2 | YES | Issue number "(3)" present in A, absent in C — formatting variant; year/PMID/vol/pages/DOI match |
| 31293078 | Kim SJ 2019, Physiol Rep | B[2] only | animal | 2 | N/A | Single-section; no cross-section comparison |
| NCT03998514 | CB4211 Phase 1a/1b | D[6], E.3 body+[10][11] | open_label | 1 (D registry); 3 (E via press release) | YES | D holds standalone registry entry (tier-1); E references via corporate documents. Structural difference in citation format, not a metadata conflict. Design details (Phase 1a: 65 healthy adults; Phase 1b: 20 NAFLD/NASH subjects, 25 mg SC × 4 weeks) consistent across D and E. |
| NCT07505745 | MOTS-c Phase 2a | B[10], D[12] | regulatory | 1 | YES — iter-2 fix CONFIRMED | Both sections: regulatory/tier-1; design (12-week DBPC, prediabetes/overweight-obesity, OGTT primary endpoint) matches |
| WADA 2026 Prohibited List | D[11] | regulatory | 1 | YES | Single-section primary citation; §C defers to §D without re-citing |
| FR 2026-07361 (FDA PCAC) | D[10] | regulatory | 1 | YES | Single-section primary citation; §E.5 defers to §D |

### Institutions (3 entities scanned, 0 mismatches)

| Institution | Sections | Status |
|---|---|---|
| USC Leonard Davis School of Gerontology / Cohen–Lee group | A (implied), E (explicit: P1–P4 enumerated) | CONSISTENT — E explicitly names; A cites consistently |
| CohBar, Inc. | D, E | CONSISTENT — both: CB4211 developer, Cohen co-founder, dissolution 2023. E.4 specifies "October 30–31, 2023"; D says "2023" — complementary. |
| ClinicalTrials.gov | B, D, E | CONSISTENT as registry source across all sections |

### Compound identifiers (4 entities scanned, 0 mismatches)

| Identifier | Sections | Status |
|---|---|---|
| MOTS-c native sequence (MRWQEMGYIFYPRKLR, 16 aa, ~2174.6 Da) | A only | Not repeated; not contradicted |
| CB4211 (engineered analog) | D, E | CONSISTENT — both describe as stabilized/modified analog; neither conflates with native peptide |
| AICAR | A, B, D | CONSISTENT — role as AMPK activator and folate-cycle intermediate uniform |
| K14Q / Lys14Gln (m.1382A>C) | A (full: Grantham 53, PROVEAN –4.0), C (brief) | CONSISTENT — A holds full characterization; C references correctly |

### Regulatory dates (4 entities scanned, 0 mismatches)

| Entity | Sections | Status |
|---|---|---|
| WADA 2026 Prohibited List effective date (January 1, 2026) | D[11]: "Effective January 1, 2026"; C: defers to §D, no date stated | CONSISTENT — iter-2 fix CONFIRMED. §C's "January 2024" sentence removed. |
| FDA FR 2026-07361 (April 16, 2026 publication; July 23, 2026 PCAC meeting) | D[10]: full citation with dates; E.5: July 2026 meeting reference only | CONSISTENT — complementary specificity levels, not contradictory |
| CohBar dissolution 2023 | D: "2023"; E.4: "October 30–31, 2023" | CONSISTENT |
| CB4211 Phase 1 topline (August 10, 2021) | D: "2021 topline"; E[11]: "August 10, 2021" | CONSISTENT |

### Trial registrations (2 entities scanned, 0 mismatches)

| NCT | Sections | Tag | Design details | Status |
|---|---|---|---|---|
| NCT03998514 | D[6], E.3 body | open_label | Phase 1a: 65 healthy adults, 1-week SMAD; Phase 1b: 20 NAFLD/NASH subjects (11/9), 25 mg SC × 4 weeks. Consistent D and E. | CONSISTENT |
| NCT07505745 | B[10], D[12] | regulatory | Phase 2a, DBPC, 12-week + 4-week safety follow-up, prediabetes/overweight-obesity, OGTT-derived insulin sensitivity. Consistent B and D. | CONSISTENT — iter-2 fix CONFIRMED |
