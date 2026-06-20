# Phase 4.25 — ID-Reconcile Verifier: Serum Potassium

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity class | Instances scanned | Mismatches | Detail |
|---|---|---|---|
| Citations (shared across sections) | 1 (Huang-Kuo JASN PMID 17804670 in B + D) | 0 | Author, year, PMID, journal agree exactly |
| Institutions | 0 | 0 | No institution names shared across sections |
| Compound identifiers | 0 | 0 | No CAS/INN/drug-registration IDs present |
| Regulatory dates | 0 | 0 | No regulatory dates cited |
| Trial registrations | 0 | 0 | No ClinicalTrials.gov or EudraCT numbers present |

**Total mismatches: 0**

---

## Shared-Entity Reconciliation Narrative

### 1. Reference interval 3.5–5.0 mmol/L (A + B + D)

All three sections state the canonical adult serum K⁺ reference interval as **3.5–5.0 mmol/L**. Section B notes some laboratories report the upper bound as 5.2 mmol/L (citing RCPA); Section C cites 3.5–5.1 mmol/L in the context of indirect ISE on fasting specimens. These variations are method/lab-specific qualifications of the same canonical interval, not cross-section disagreements. **No mismatch.**

### 2. Serum-vs-plasma offset (B + C + D)

- B: "~0.2–0.5 mmol/L" in healthy individuals
- C: "0.2–0.4 mmol/L" physiological offset at normal platelet counts
- D: "0.1–0.4 mmol/L normally"

Ranges overlap substantially across sections (0.2–0.4 is common to all three). The minor boundary variation (B upper 0.5; D lower 0.1) reflects slightly different study populations and phlebotomy conditions in the underlying literature — not a factual disagreement between sections. **No mismatch.**

### 3. Pseudohyperkalemia — hemolysis as #1 cause (B + C + D)

All three sections identify hemolysis as the most frequent cause of pseudohyperkalemia and consistently state it must be excluded before treating an elevated result. Mechanism (K⁺ leaks from lysed RBCs) is described consistently. **No mismatch.**

Minor note: the diagnostic serum-plasma discrepancy threshold used as the pseudohyperkalemia cutoff differs slightly — B states >0.4 mmol/L, C states >0.5 mmol/L. Both thresholds appear in the published literature (B and C cite different supporting sources); this reflects real variation across references, not an internal inconsistency in the report. No HALT warranted.

### 4. Transcellular shift regulation — insulin / β₂ / acid-base (A + D)

Both sections describe the same four effectors:
- Insulin → activates Na-K ATPase → K⁺ into cells (A §A.4; D hypokalemia section)
- β₂-adrenergic agonists → activate Na-K ATPase via cAMP → K⁺ into cells (A §A.4; D hypokalemia section)
- Metabolic acidosis → K⁺ out of cells (A §A.4; D hyperkalemia section)
- Metabolic alkalosis → K⁺ into cells (A §A.4; D hypokalemia section)

Directionality, mechanism, and magnitude descriptions are consistent. **No mismatch.**

### 5. Aldosterone / ENaC / ROMK (A + D)

Section A (§A.5) and Section D both describe aldosterone acting on principal cells of the CCD/CNT to upregulate ENaC (apical sodium channel) and ROMK (apical K⁺ secretion channel), with ENaC-driven Na⁺ reabsorption creating the electro-negative lumen that drives K⁺ secretion. Section D further lists ENaC-blocking drugs (amiloride, triamterene, trimethoprim) and ROMK in the hypomagnesemia mechanism. **No mismatch.**

### 6. Hypomagnesemia → ROMK → refractory hypokalemia (B + D)

- B (§Hypokalemia–Hypomagnesemia): cites Huang CL, Kuo E. JASN 2007. PMID 17804670. Mechanism: falling intracellular Mg²⁺ releases ROMK channel pore inhibition → unrestrained K⁺ secretion.
- D (§Hypomagnesemia → Refractory Hypokalemia): cites Huang C-L, Kuo E. JASN 2007. PMID 17804670. Mechanism: "intracellular magnesium tonically blocks the apical ROMK channel … When intracellular Mg²⁺ falls … ROMK channel pore inhibition is lifted."

Author, year, journal, PMID, and mechanistic description are identical across B and D. **No mismatch.**

### 7. ECG changes / cardiac danger (B + D)

Both sections describe the same progressive hyperkalemia ECG sequence (peaked T-waves → PR prolongation → P-wave loss → QRS widening → sine-wave → VF/asystole) and the same hypokalemia changes (T-wave flattening, U-waves, QT/QU prolongation, torsades de pointes, digoxin potentiation). The U-shaped mortality curve is cited in D with primary cohort references (Goyal, Núñez, Kovesdy) consistent with the physiological basis established in A and B. **No mismatch.**

### 8. Units mmol/L = mEq/L

Section B explicitly states the numeric equivalence (monovalent ion, charge +1). All sections use mmol/L consistently. **No mismatch.**

### 9. Shared citation — Huang CL, Kuo E. JASN 2007. PMID 17804670

Present in:
- Section B, bibliography ref 7: "Huang CL, Kuo E. Mechanism of hypokalemia in magnesium deficiency. *J Am Soc Nephrol.* 2007;18(10):2649–2652. doi: 10.1681/ASN.2007070792. PMID: 17804670"
- Section D, bibliography ref 5: "Huang C-L, Kuo E. Mechanism of hypokalemia in magnesium deficiency. *J Am Soc Nephrol*. 2007;18(10):2649–2652. PMID 17804670"

Author (name format variant C-L vs CL is typographic, not substantive), title, journal, year, volume, issue, pages, and PMID are identical. **No citation mismatch.**

---

## Tally

| Check | Result |
|---|---|
| Reference interval agreement | PASS |
| Serum-plasma offset agreement | PASS (ranges overlap; minor boundary variation, not a contradiction) |
| Pseudohyperkalemia / hemolysis #1 agreement | PASS |
| Transcellular shift mechanism agreement | PASS |
| Aldosterone/ENaC/ROMK agreement | PASS |
| Hypomagnesemia-ROMK mechanism agreement | PASS |
| ECG-danger description agreement | PASS |
| Units agreement | PASS |
| Shared citation (PMID 17804670) agreement | PASS |

**Genuine cross-section disagreements: 0**

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":1,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":0,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
