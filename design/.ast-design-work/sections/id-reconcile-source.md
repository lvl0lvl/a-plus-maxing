# ID-Reconcile: Phase 4.25 — AST Biomarker Report

## Verdict

verdict: PASS

All cross-section shared entities agree. The macro-AST PEG-precipitation threshold that caused the HALT in iteration 1 is now harmonized: both section B and section C cite van Wijk 2016 (Clin Chim Acta) and state the identical threshold — post-precipitation AST recovery ≤40% (drop ≥60%) confirms macro-AST. No remaining mismatches detected across any entity class.

---

## Per-Class Mismatch Table

| Entity Class | Entities Scanned | Mismatches | Detail |
|---|---|---|---|
| Citations | 4 shared-citation candidates checked (van Wijk 2016 in B+C; De Ritis origin refs in A+B+D; Sherman half-life in A+D directional; Williams/Hoofnagle in B+D) | 0 | B [8] and C [6] both resolve to van Wijk 2016 Clin Chim Acta DOI 10.1016/j.cca.2016.10.011; different local ref numbers are expected per-section bibliography numbering, not a mismatch |
| Institutions | 0 shared institutional claims | 0 | No institution names appear across sections |
| Compound identifiers / diagnostic thresholds | 5 checked (macro-AST PEG threshold, De Ritis >2, De Ritis <1, De Ritis >1, RBC:serum 40×) | 0 | Previously halted macro-AST PEG threshold now harmonized to ≤40%/≥60% in both B and C |
| Regulatory dates | 1 checked (ACG 2017 guideline) | 0 | Cited in B only; no cross-section conflict |
| Trial registrations | 0 | 0 | No trial registrations cited in any section |

**Mismatch tally: 0**

---

## Cross-Section Agreement Summary

| Entity | Sections | Status |
|---|---|---|
| Macro-AST PEG threshold: ≤40% recovery / ≥60% drop (van Wijk 2016) | B, C | AGREE — harmonized in iteration 2 |
| GOT1 (cytosolic, chr 10q24.2) / GOT2 (mitochondrial, chr 16q21) | A, C | AGREE — consistent gene names and subcellular compartments |
| mAST ~80% of total intrahepatic AST | C, D | AGREE — C: "hepatocytes contain approximately 80% mAST"; D: "m-AST constitutes roughly 80% of total intrahepatic AST" |
| De Ritis ratio: >2 / ≥2 → ALD | A, B, D | AGREE |
| De Ritis ratio: <1 → MASLD / acute viral hepatitis | A, B, D | AGREE |
| De Ritis ratio: >1 in chronic liver disease → advancing fibrosis/cirrhosis | B, D | AGREE |
| PLP/B6 depletion preferentially suppresses ALT, widening AST:ALT in ALD | A, B, D | AGREE |
| mAST release from mitochondrial disruption drives ratio >2 in ALD | A, B, C, D | AGREE |
| RBC:serum AST ~40× concentration ratio | C | Single-section numeric; D describes RBCs as "AST-rich" without competing figure — no contradiction |
| Units: U/L throughout | A, B, C, D | AGREE |
| AST half-life shorter than ALT half-life | A (numeric: ~15.8 h vs ~34.6 h via Sherman 2024), D (directional) | AGREE — A holds the only numeric value, D does not contradict it |
| Macro-AST: IgG (primary) or IgA complex; benign; PEG precipitation method | B, C, D | AGREE on mechanism, immunoglobulin class, benign nature, and now on numeric cut-off |

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":4,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":1,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
