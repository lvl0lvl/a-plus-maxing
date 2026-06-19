# ID-Reconcile Source — hs-CRP (Phase 4.25, iteration 2)

Independent cross-section identity reconciliation over `section-A.md` + `section-B.md`
(excluding each file's `## Post-fix grep audit` + `## Self-check`).
Re-run after the remediation that retagged the Pearson AHA/CDC 2003 source (PMID
12551878) from `mechanism_review` → `regulatory` in Section A to agree with Section B.

## Verdict

verdict: PASS

The iteration-1 mismatch is RESOLVED. The Pearson AHA/CDC 2003 scientific statement
(PMID 12551878, DOI 10.1161/01.cir.0000052939.59093.45, *Circulation* 107(3):499–511)
is now tagged `regulatory` in BOTH sections:
- Section A — inline `[4, regulatory]` (risk-category cutpoints) + bibliography ref 4
  `Tag: regulatory`. No residual `mechanism_review` tag on the Pearson source.
- Section B — `[1, regulatory]` (tertiles, >10 mg/L rule, measurement best-practice) +
  bibliography ref 1 `[regulatory — AHA/CDC scientific statement]`.

JUPITER and CANTOS tags remain consistent (`rct`). All other shared-entity values
(author+year, PMID, DOI, journal locus, institutions, compound IDs, dates) agree.
Entities present in only one section (CANTOS/Elliott/PROVE-IT/PRINCE, FDA K053603, NCT
registrations) are not cross-comparable and carry no mismatch.

## Per-class reconciliation

### citations

| entity_id | A | B | match? |
|---|---|---|---|
| Pearson AHA/CDC 2003 | PMID 12551878; DOI 10.1161/01.cir.0000052939.59093.45; *Circulation* 107(3):499–511; tag `regulatory` | PMID 12551878; DOI 10.1161/01.cir.0000052939.59093.45; *Circulation* 107(3):499–511; tag `regulatory` | MATCH (tag RESOLVED) |
| JUPITER / Ridker 2008 | PMID 18997196; DOI 10.1056/NEJMoa0807646; *NEJM* 2008; tag `rct` | PMID 18997196; DOI 10.1056/NEJMoa0807646; *NEJM* 2008;359(21):2195–2207; tag `rct` | MATCH |
| CANTOS / Ridker 2017 | PMID 28845751; DOI 10.1056/NEJMoa1707914; tag `rct` | absent | not comparable (B absent) |

### institutions

| entity_id | A | B | match? |
|---|---|---|---|
| AHA/CDC (statement co-authorship) | CDC + AHA | CDC + American Heart Association | MATCH |
| NEJM (publication venue, JUPITER) | *N Engl J Med* | *N Engl J Med* | MATCH |

### compound_identifiers

| entity_id | A | B | match? |
|---|---|---|---|
| rosuvastatin | "rosuvastatin 20 mg" (JUPITER); hs-CRP −37% | "rosuvastatin 20 mg" (JUPITER); hs-CRP −37% (4.2→2.2 mg/L) | MATCH |
| canakinumab | anti-IL-1β mAb (CANTOS) | absent | not comparable (B absent) |
| CRP / hs-CRP nomenclature | CRP = hs-CRP same analyte; pentameric ~115 kDa | CRP/hs-CRP same; mg/L units | MATCH |
| IL-6 | IL-6 driver of hepatic CRP | IL-6 driver of hepatic CRP | MATCH |
| IL-1β | IL-1β upstream cytokine | IL-1 (+ TNF-α) upstream | MATCH |

### regulatory_dates

| entity_id | A | B | match? |
|---|---|---|---|
| AHA/CDC statement year | 2003 | 2003 | MATCH |
| JUPITER publication year | 2008 | 2008 | MATCH |
| FDA 510(k) K053603 (Roche CRP HS) | absent | K053603 | not comparable (A absent) |

### trial_registrations

| entity_id | A | B | match? |
|---|---|---|---|
| JUPITER (PMID 18997196) | PMID 18997196; n=17,802 | PMID 18997196 | MATCH (identity consistent) |
| CANTOS NCT | absent | absent | not comparable |

## Determination

The previously divergent Pearson AHA/CDC citation now matches on author+year, PMID, DOI,
journal locus AND type-tag (`regulatory` in both). The shared JUPITER citation matches on
all fields including tag (`rct`). No remaining cross-section type-tag, PMID, DOI, or
identity disagreement exists in any entity class. halt_reasons is empty; verdict PASS.

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 3, "mismatch_count": 0},
    "institutions": {"scanned": 2, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 6, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 3, "mismatch_count": 0},
    "trial_registrations": {"scanned": 2, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 2
}
```
