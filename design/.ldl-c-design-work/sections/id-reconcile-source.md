# Phase 4.25 — Cross-Section ID Reconcile (LDL-C)

Independent reconciliation of cross-section identity agreement between
`section-A.md` (Identity, Physiology & Causal Significance) and
`section-B.md` (Reference Ranges, Measurement & Determinants). Each file's
`## Self-check` block was excluded from the scan (neither file carries a
`## Post-fix grep audit` block). Only entities appearing in BOTH sections were
compared.

## Verdict

verdict: PASS

No cross-section identity disagreements were found. The two sections draw on
disjoint bibliographies (no shared PMID/DOI/author+year), so no citation-identity
collisions are possible; the entities that DO appear in both sections
(institutions, named measurement methods, the cholesterol conversion factor)
agree.

## Per-Class Reconciliation

### Citations

| Shared fact / entity | Section A | Section B | Status |
|----------------------|-----------|-----------|--------|
| Cholesterol unit conversion factor | 1 mmol/L ≈ 38.7 mg/dL — Ference 2012 MR [3, meta_analysis] | mg/dL ÷ 38.67 = mmol/L — equations review [4, mechanism_review] | Same numeric value (38.7 ≈ 38.67, rounding); attributed to two DIFFERENT, internally-correct sources — not the same citation entity, so no identity collision |
| Society-guideline type-tag rule | EAS 2017 consensus → `mechanism_review` [4] | ESC/EAS 2019 + AHA/ACC 2018 → `mechanism_review` [1, 2] | Consistent — society guidelines tagged `mechanism_review` in both |
| NHLBI/NCEP type-tag rule | (not cited in A) | NCEP ATP III (NHLBI) → `regulatory` [3] | Consistent with the regulatory rule (single-section, no conflict) |
| CTT / Ference type-tag rule | CTT 2010/2012, Ference 2012 MR → `meta_analysis` [1, 2, 3] | (not cited in B) | Consistent with the meta_analysis rule (single-section, no conflict) |

No identifier (PMID/DOI/author+year) appears in both bibliographies, so 0
citation-identity comparisons were possible across the two reference lists; the
4 shared FACTS/rules above were checked and all agree.

scanned: 4 — mismatch_count: 0

### Institutions

| Institution | Section A | Section B | Status |
|-------------|-----------|-----------|--------|
| EAS (European Atherosclerosis Society) | "European Atherosclerosis Society Consensus Panel" | "European … Atherosclerosis Society" (ESC/EAS) | Consistent |
| ESC (European Society of Cardiology) | (implicit, ESC/EAS consensus) | "European Society of Cardiology" | Consistent |
| AHA/ACC | (n/a) | "AHA/ACC Multisociety" | Single-section; no conflict |
| NHLBI / NIH | (n/a) | "NHLBI/NIH" (NCEP ATP III) | Single-section; no conflict |
| NLA (US National Lipid Association) | (n/a) | "US National Lipid Association (NLA)" | Single-section; no conflict |

Two institutions (EAS, ESC) appear in both sections; both spelled/expanded
consistently.

scanned: 2 — mismatch_count: 0

### Compound Identifiers

| Compound | Section A | Section B | Status |
|----------|-----------|-----------|--------|
| Statin (atorvastatin, rosuvastatin) | "statin" (generic) | atorvastatin, rosuvastatin | Consistent nomenclature; A generic, B specific — no contradiction |
| Ezetimibe | (n/a) | "ezetimibe" | Single-section |
| PCSK9i (evolocumab, alirocumab) | (n/a) | evolocumab, alirocumab | Single-section |
| Bempedoic acid | (n/a) | "bempedoic acid" | Single-section |
| Inclisiran | (n/a) | "inclisiran (siRNA against PCSK9)" | Single-section |

Only the statin class is named in both sections; nomenclature is consistent
(A's generic "statin" subsumes B's named atorvastatin/rosuvastatin).

scanned: 1 — mismatch_count: 0

### Regulatory Dates

| Date | Section A | Section B | Status |
|------|-----------|-----------|--------|
| (none shared) | — | 2019 ESC/EAS, 2018 AHA/ACC, ATP III | No regulatory date appears in both sections |

scanned: 0 — mismatch_count: 0

### Trial Registrations

| Registration | Section A | Section B | Status |
|--------------|-----------|-----------|--------|
| (none) | trial COUNTS only (26/27 trials), no NCT/registry IDs | no NCT/registry IDs | No trial-registration identifier in either section |

scanned: 0 — mismatch_count: 0

## Machine-readable result

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 4, "mismatch_count": 0},
    "institutions": {"scanned": 2, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 1, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 0, "mismatch_count": 0},
    "trial_registrations": {"scanned": 0, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 1
}
```
