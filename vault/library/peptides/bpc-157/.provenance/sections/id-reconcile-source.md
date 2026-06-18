# ID-Reconcile Source — BPC-157 (Phase 4.25, final)

ID-Reconcile verifier re-confirmation over the 5 sections
(`section-{A,B,C,D,E}.md`). Iter-2 had already reached 0 mismatches; this
final pass re-scans all five shared-entity classes and re-confirms
convergence. The three previously remediated targets — NCT02637284 registry
status (B vs E, "UNKNOWN"), the Hsieh-2017 lead-author affiliation
(A[3] vs C[13]), and the FDA 503A Category-2 regulatory status (B vs D) —
all remain reconciled. No new cross-section divergence introduced.

## Verdict

verdict: PASS

All five entity classes scanned; every entity shared across 2+ sections
agrees on its canonical value. Total mismatch_count = 0. No halt reasons.

### Per-class scan summary

| Entity class | Scanned (shared 2+) | Mismatches |
|---|---|---|
| citations | 9 | 0 |
| institutions | 4 | 0 |
| compound_identifiers | 3 | 0 |
| regulatory_dates | 3 | 0 |
| trial_registrations | 2 | 0 |

---

## Re-check of the three prior reconcile targets

**(a) NCT02637284 registry overall-status — B vs E: RESOLVED.**
- B (prose L9, bib [1] L33, summary L49) and E (prose L9, dose table L67) both
  use the verbatim API value **"UNKNOWN"** + "no results posted." Prior E
  divergence ("Active, not recruiting") is gone (`grep` = 0 hits in both).
  Matches ClinicalTrials.gov v2 API `overallStatus` = "UNKNOWN".

**(b) Hsieh-2017 affiliation — A[3] vs C[13]: RESOLVED.**
- A[3] L47 and C[13] L66 both read **"Chang Gung University / Chang Gung
  Memorial Hospital, Taiwan"** (canonical lead-author string per PMID
  27847966 efetch). "Taipei Medical University" survives only as a
  group-level descriptor at C L5 / C L81 (legitimate, not the per-paper
  field); 0 hits in Section A.

**(c) FDA regulatory status — B vs D: RESOLVED.**
- B L19 and D L46 both state the documented authoritative status **remains
  FDA 503A Category 2 (placed 2023-09-29)**, PCAC review 23 July 2026, and
  demote the purported **2026-04-15 HHS removal** to low-trust/unverified
  (agemd.com, traced to an RFK Jr. podcast; not an FDA/HHS primary). No blog
  grounds the regulatory status in either section.

---

## Shared-entity inventory (2+ sections) — re-verified

### citations (9 shared; all consistent)
1. Jozwiak 2025, *Pharmaceuticals* (PMC11859134 / DOI 10.3390/ph18020185 / PMID 40005999) — A[1], D[2]
2. Sikiric 2020, *Gut and Liver* (PMC7096228 / PMID 31158953 / DOI 10.5009/gnl18490) — A[6], E[4]
3. Hsieh 2017, *J Mol Med* (DOI 10.1007/s00109-016-1488-y / PMID 27847966) — A[3], C[13], D[4]
4. Chang 2011, *J Appl Physiol* (PMID 21030672 / DOI 10.1152/japplphysiol.00945.2010) — A[5], C[1]
5. Chang 2014, *Molecules* (PMID 25415472 / DOI 10.3390/molecules191119066) — A[8], C[5]
6. FDA 503A "Certain Bulk Drug Substances…" Category-2 doc — B[4], D[3]
7. agemd.com longevity blog (low-trust, demoted in both) — B (prose), D[6]
8. NCT02637284 registry record — B[1], D (prose), E[1]
9. NCT07437547 registry record — B[2], E[2]

### institutions (4 shared; all consistent)
1. "Chang Gung University / Chang Gung Memorial Hospital, Taiwan" (Hsieh group, canonical lead-author string) — A, C, D
2. University of Zagreb / Sikiric originating group — A, B, C, E
3. U.S. FDA — B, D
4. WADA (S0 Non-Approved Substances) — A, B

### compound_identifiers (3 shared; all consistent)
1. 15-aa sequence GEPPPGKPADDAGLV (= Gly-Glu-Pro-Pro-Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val) — A, C
2. Molecular weight ~1419 Da (A "~1419.55 Da" ⊇ E "1419 Da") — A, E
3. Pentadecapeptide / 15-amino-acid designation — A, C, E

### regulatory_dates (3 shared; all consistent)
1. FDA Category-2 placement 2023-09-29 — B, D
2. PCAC review 23 July 2026 — B, D
3. Purported 2026-04-15 HHS removal — demoted to low-trust/unverified in both — B, D

### trial_registrations (2 shared; all consistent)
1. NCT02637284 — "UNKNOWN", oral, ~42 healthy volunteers, PharmaCotherapia, no results — B, D, E
2. NCT07437547 — "RECRUITING", Phase 2, ~120, subcutaneous, Hudson Biotech, no results — B, E

---

## Mismatch table

| # | Class | Shared entity | Sections | Divergent values | Status |
|---|---|---|---|---|---|
| — | — | (none) | — | — | — |

(empty — no cross-section mismatch detected in any of the 5 classes)

---

## Gate scaffold (conforms to gate-4.25.schema.json)

The fenced JSON block below is the gate scaffold consumed by the attest step.
Per schema, `verdict`, `timestamp`, and `attestation_chain` are intentionally
omitted here (attest adds them); `entity_classes` carries all 5 required
classes, each `{scanned, mismatch_count}`; `halt_reasons` is empty (PASS).

```json
{
  "phase": "4.25",
  "iterations": 2,
  "entity_classes": {
    "citations": {
      "scanned": 9,
      "mismatch_count": 0
    },
    "institutions": {
      "scanned": 4,
      "mismatch_count": 0
    },
    "compound_identifiers": {
      "scanned": 3,
      "mismatch_count": 0
    },
    "regulatory_dates": {
      "scanned": 3,
      "mismatch_count": 0
    },
    "trial_registrations": {
      "scanned": 2,
      "mismatch_count": 0
    }
  },
  "halt_reasons": []
}
```
