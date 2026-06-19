# Phase 4.25 — Cross-Section Identity Reconciliation (ApoB), iteration 2

Independent RE-reconcile pass over `section-A.md` (Identity/Physiology/Causal) and `section-B.md` (Reference Ranges/Measurement/Determinants), after the iteration-1 remediation that retagged Section A's EAS society source (ref [7], Ference 2017 EAS consensus, *Eur Heart J*) from `regulatory` → `mechanism_review`. Bodies + bibliographies scanned; each file's `## Post-fix grep audit` and `## Self-check` excluded per spec. For each entity class, instances were extracted from EITHER section; entities present in BOTH (2+) were value-compared. A disagreement on a shared entity's identity is a mismatch.

## Verdict

verdict: PASS

The iteration-1 cross-section type-tag divergence is **RESOLVED**. Every professional-society / clinical-guideline source is now tagged `mechanism_review` consistently in BOTH sections; no `regulatory` tag remains on any society source — or on any citation/bibliography entry — in either file's substantive body. Re-scan of all five entity classes found zero shared-entity divergences.

### Society-tag confirmation (the divergence under test)
- Section A ref [7] — EAS Consensus Panel statement (Ference 2017, PMID 28444290) → `mechanism_review` (inline L11 ×2, L21, L29; bib L39). No `[7, regulatory]` variant remains.
- Section B ref [7] — 2019 ESC/EAS Guidelines (Mach 2020) → `mechanism_review` (inline L17, L22, L62).
- Section B ref [1] — NLA 2024 Expert Clinical Consensus → `mechanism_review` (the prior 6 in-text `[1, regulatory]` + bib tag fully converted).
- No government/regulator (FDA/EMA/TGA/Health Canada/NIH/WHO/CDC) source is cited directly in either section, so `regulatory` is correctly absent from both bodies. Society guidelines (EAS/ESC/NLA) carry `mechanism_review` in both — consistent. Residual `regulatory` tokens exist only in the excluded `## Self-check` / `## Post-fix grep audit` sections (descriptive prose + old→new remediation logs).

## Per-class summary

| Entity class | Scanned (instances; compared where in BOTH) | Mismatches | Notes |
|---|---|---|---|
| citations | 4 | 0 | Society-source class (EAS / ESC-EAS / NLA) now uniformly `mechanism_review` across both sections — divergence resolved. FOURIER/IMPROVE-IT cited via DIFFERENT valid refs per section: Section A via pooled Marston cohort [3] (PMID 34550306, `cohort`); Section B via primary trial reports [8]/[9]/[10] (PMIDs 26039521/28304224/30403574, `rct`). Distinct papers, no conflicting per-citation metadata. |
| institutions | 4 | 0 | European Atherosclerosis Society (EAS), ESC, NLA / National Lipid Association, WHO/IFCC — canonical names + attribution consistent. ESC in B is additive (ESC/EAS joint), not contradictory. |
| compound_identifiers | 6 | 0 | apoB-100, apoB-48 nomenclature identical (A L5,7; B L3,35). statin/ezetimibe/evolocumab/alirocumab/inclisiran consistent: A (physiology) names isoforms + statin; B names the full agent list. No divergent value. |
| regulatory_dates | 3 | 0 | SP3-07 / WHO-IRP October 1992 / assigned 1.22 g/L (Section B only); trial pub years 2015/2017/2018 consistent with PMIDs. No conflict. |
| trial_registrations | 3 | 0 | NCT00202878 (IMPROVE-IT), NCT01764633 (FOURIER), NCT01663402 (ODYSSEY OUTCOMES) — Section B only, each correctly mapped. Section A names FOURIER/IMPROVE-IT but assigns NO NCT (it cites the pooled Marston analysis), so no NCT value in A diverges from B. |

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 4, "mismatch_count": 0},
    "institutions": {"scanned": 4, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 6, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 3, "mismatch_count": 0},
    "trial_registrations": {"scanned": 3, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 2
}
```
