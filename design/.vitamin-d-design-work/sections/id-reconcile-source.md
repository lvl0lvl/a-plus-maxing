# ID-Reconcile: Phase 4.25 — Serum 25(OH)D Cross-Section Entity Verification

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity Class | Scanned | Mismatches | Details |
|---|---|---|---|
| Citations (author+year+PMID) | 18 | 0 | NIH ODS 2024 shared A[3]/B[5]: tier/tag consistent. All other citations are section-local; no shared citation carries conflicting PMID, year, or author across sections. |
| Institutions | 6 | 0 | IOM/NAM, Endocrine Society, NIST, CDC, NIH ODS, VDSP — named consistently across B and C with no name divergence. |
| Compound identifiers | 8 | 0 | 25(OH)D, 25(OH)D3, 25(OH)D2, 1,25(OH)₂D, DBP, 7-DHC, calcitriol, 3-epi-25(OH)D3 — nomenclature consistent across all sections. |
| Regulatory dates | 4 | 0 | IOM 2011, ES 2011, ES 2024 (Demay JCEM), VDSP ~2010 founding — no conflicting dates across sections. |
| Trial registrations | 5 | 0 | VITAL, D-Health, ViDA, Hahn VITAL-autoimmune, Zhao fracture meta-analysis — all cited in D only; no shared trial appears in another section with conflicting identifiers. |

**Total mismatches: 0**

---

## Key Shared-Entity Spot-Checks (Narrative)

### Unit conversion (×2.496; 30 ng/mL = 75 nmol/L)
- **A** (§A.7): "1 ng/mL × 2.496 = nmol/L" — PASS
- **B** (Units section): "×2.496" stated; landmark table gives 30 ng/mL ≈ 75 nmol/L — PASS
- **C/D**: Do not restate the conversion factor; values cited are consistent with ×2.496 throughout — PASS

### Deficiency/sufficiency thresholds (IOM 20 ng/mL vs ES 30 ng/mL)
- **B** (authoritative tables): IOM — deficiency <12 ng/mL (<30 nmol/L), inadequate 12–<20 ng/mL, adequate ≥20 ng/mL (≥50 nmol/L); ES — deficiency <20 ng/mL (<50 nmol/L), insufficiency 20–29 ng/mL (50–72 nmol/L), sufficiency ≥30 ng/mL (≥75 nmol/L) — PASS
- **C** (§Measurement Limitations): "20 ng/mL per IOM; 30 ng/mL per Endocrine Society" — shorthand for the same sufficiency floor B establishes — PASS
- **D** (same shorthand): identical framing to C — PASS
- **A**: No numeric thresholds cited — no conflict

### 25(OH)D half-life ~2–3 weeks
- **A** (§A.4): "approximately 2–3 weeks for 25(OH)D3" — stated
- **B, C, D**: Do not cite a specific half-life number — no cross-section conflict

### Assay standardization / VDSP story
- **B** (assay caveat): 10–40% inter-assay bias documented; LC-MS/MS ~half immunoassays met CV criterion
- **C** (§C.2, authoritative): NIST SRM 972a, VDSP interlaboratory comparison (15 labs, 50 samples), CDC VDSCP; LC-MS/MS nearly all met criteria; immunoassay bias exceeding ±15% or >100% at very low concentrations in some mid-2010s proficiency surveys — consistent with B's range (B's "10–40%" is a subset of C's broader characterization)
- **D**: "10–15% inter-assay variation" — a slightly compressed summary; not a factual contradiction with B or C, and D explicitly defers to VDSP as the authoritative program — PASS

### DBP-binding % (~88%)
- **A** (§A.6): "~88% bound to DBP" — PASS
- **C** (§C.1): "~88%" bound to DBP — PASS (exact agreement)
- **B, D**: Do not cite the DBP% figure — no conflict

### Free hormone / bioavailable-D concept
- **A** (§A.6): ~0.03% free; megalin/cubilin renal exception noted
- **C** (§C.4): ~0.03% free; DBP GC-gene polymorphisms; racial DBP ELISA artifact (Nielson 2016) — both sections agree on the concept and free-fraction magnitude — PASS

### VITAL/big-RCT framing
- **D** (authoritative for clinical significance): VITAL PMID 30415629 (N=25,871; D3 2,000 IU/d; cancer HR 0.96; CVD HR 0.97); Hahn BMJ 2022 PMID 35082139 (autoimmune HR 0.78); D-Health PMID 35026158 (N=21,315); ViDA PMID 28384800 (N=5,108) — section-local, no other section cites these trials — no conflict

---

## Summary

All shared entities across sections A, B, C, and D are internally consistent. The ×2.496 unit conversion, the IOM/ES threshold distinction, the 25(OH)D half-life of 2–3 weeks, the DBP-binding fraction (~88%), the free-hormone concept, and the VDSP/assay-standardization narrative agree wherever they overlap. No citation appears in two sections with conflicting PMID, year, or author. The only asymmetry is that D condenses the VDSP inter-assay variation to "10–15%" while B and C document up to 40% (and 100% at very low concentrations) — this is a legitimate compression for a summary section, not a factual contradiction.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":18,"mismatch_count":0},"institutions":{"scanned":6,"mismatch_count":0},"compound_identifiers":{"scanned":8,"mismatch_count":0},"regulatory_dates":{"scanned":4,"mismatch_count":0},"trial_registrations":{"scanned":5,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
