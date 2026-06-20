# ID-Reconcile Phase 4.25 — RBC Magnesium (Iteration 2)

## Verdict

verdict: PASS

Both iteration-1 HALT triggers are re-verified as fixed, and a fresh scan of all five entity classes plus every shared content entity finds zero remaining identifier-class mismatches.

---

## Per-Class Mismatch Table

(Empty — PASS. All prior mismatches resolved; no new mismatch found.)

| Class | Entity / Citation | Sections | Detail | Verdict |
|---|---|---|---|---|
| — | — | — | No mismatches remain | PASS |

---

## Prior-Iteration Fixes — Re-Verification

| Fix target | Iteration-1 state | Iteration-2 state | Resolved |
|---|---|---|---|
| Bithi et al. 2024 DOI (PMID 39469428) | B `…2024.09.003` vs C `…2024.10.003` (month segment differed) | B and C both `10.1016/j.jmsacl.2024.10.003`; PMID 39469428 in both | YES |
| Loading-test retention threshold | A >27%, B >20–27%, C ≥20%, **D >50% (uncited outlier)** | D corrected to **>27% retention (Gullestad 1992, PMID 1439510)**, consistent with A (>27%) and B (>20–27% band, Gullestad-attributed) | YES |

---

## Shared-Entity Agreement Scan

| Class | Entity | Sections | Detail | Verdict |
|---|---|---|---|---|
| citations | Bithi et al. 2024 (PMID 39469428) | B (ref 2), C (ref 4) | DOI now identical: `10.1016/j.jmsacl.2024.10.003`; PMID identical. | PASS |
| citations | Gullestad et al. 1992 (PMID 1439510) | A (ref 5 context), B (ref 8), D (Limitations) | PMID 1439510 identical wherever cited. | PASS |
| citations | Workinger et al. 2018 (PMID 30200431) | A (ref 4), B (ref 4), C (ref 3) | PMID identical; DOI `10.3390/nu10091202` in B and C. | PASS |
| citations | Razzaque MS 2018 (PMID 30513803) | A (ref 3), B (ref 9) | Author + year + PMID consistent. | PASS |
| citations | Touyz RM et al. 2024 (PMID 38838313) | B (ref 3) | Single-section; no cross-section conflict. | PASS |
| citations | Romani AMP 2011 (NBK507258) | A (ref 5) | Single-section; no cross-section conflict. | PASS |
| institutions | ARUP Laboratories | B (ref 1), C (context) | Name consistent; no divergence. | PASS |
| compound_identifiers | No CAS/CID/registry IDs present | — | Nothing to reconcile. | PASS |
| regulatory_dates | FDA PPI Drug Safety Communication (March 2, 2011) | D (ref 2) | Single-section; no cross-section conflict. | PASS |
| trial_registrations | No NCT/registry entries present | — | Nothing to reconcile. | PASS |

### Shared content entities re-checked (per directive)

- **Body distribution %:** A bone 50–60% / intracellular 34–40% / serum 0.3–1%; B bone ~60% / ECF <1% (B within A's ranges). Consistent.
- **RBC-Mg & serum reference intervals:** B and C agree on Bithi 4.2–6.7 mg/dL and ARUP 3.6–7.5 mg/dL. A's "~4.2–6.8" is the conventional (Romani-sourced) range, not the Bithi citation. Serum: A/D 0.75–0.95 mmol/L (NIH ODS) vs B 0.70–1.00 mmol/L (Touyz 2024) — different attributed sources, not one citation used inconsistently.
- **Serum-poor-marker concept:** A, B, C, D all assert serum reflects <1% of body Mg and is insensitive to intracellular depletion. Consistent.
- **No-universal-reference:** B ("no harmonised reference interval"), C ("no universal reference interval … no international standardization"), D ("no universally accepted reference range"). Consistent.
- **Hemolysis:** B and C agree hemolysis falsely elevates serum Mg (RBC 2–3× serum) and invalidates RBC-Mg wash. Consistent.
- **Units:** A and B agree mg/dL ÷ 2.43 ≈ mmol/L. Consistent.

These reference-interval and threshold deltas are internally attributed content claims (different sources), not identifier-class mismatches, and are outside the gating scope of Phase 4.25.

---

## Tally

| Class | Scanned | Mismatches |
|---|---|---|
| citations | 6 | 0 |
| institutions | 1 | 0 |
| compound_identifiers | 0 | 0 |
| regulatory_dates | 1 | 0 |
| trial_registrations | 0 | 0 |

**Total mismatches: 0 — PASS.** Prior HALT triggers re-verified resolved: 2 / 2. Iterations: 2.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":1,"mismatch_count":0},"compound_identifiers":{"scanned":0,"mismatch_count":0},"regulatory_dates":{"scanned":1,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```

**Summary:** Both iteration-1 HALT triggers are fixed — Bithi 2024 carries the single verified DOI `10.1016/j.jmsacl.2024.10.003` (PMID 39469428) in both B and C, and the Mg-loading retention threshold now agrees at >27% (Gullestad 1992, PMID 1439510) across A, B, and D. No identifier-class mismatch remains in any of the five entity classes, so Phase 4.25 converges to PASS at iteration 2.
