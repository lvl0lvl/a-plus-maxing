# Cross-Section Identity Reconciliation — Lp(a) (Phase 4.25)

Mode: standard. Inputs scanned: `section-A.md`, `section-B.md` (body + bibliography; `## Self-check` and `## Post-fix grep audit` excluded per protocol).

## Verdict

verdict: PASS

No cross-section identity disagreements found. The single citation shared by both sections (the EAS 2022 consensus statement) carries identical author, year, journal, PMID, DOI, and source-type tag in both. The two shared institutions (Copenhagen City Heart Study / Copenhagen General Population Study) are named consistently. The RNA-agent compound identifiers and the named trials appear in Section B only, so there is no second instance to disagree with.

## Per-class summaries

### citations — scanned: 1 shared (compared)
| Entity | Sections | Section A value | Section B value | Canonical | Match? |
|--------|----------|-----------------|-----------------|-----------|--------|
| Kronenberg/EAS 2022 consensus | A[4], B[5] | Kronenberg F, Mora S, Stroes ESG, et al. Eur Heart J 2022;43(39):3925-3946. PMID 36036785. DOI 10.1093/eurheartj/ehac361. tag: mechanism_review | Kronenberg F, Mora S, Stroes ESG, et al. Eur Heart J 2022;43(39):3925-3946. PMID 36036785. DOI 10.1093/eurheartj/ehac361. tag: mechanism_review | (identical) | YES |

Non-shared citations (no cross-section pair; not a mismatch): A-only — Erqou/ERFC 2009 (PMID 19622820), Clarke/PROCARDIS 2009 (PMID 20032323), Kamstrup AVS 2014 (PMID 24161338), Volgman 2024 (PMID 38879448), Kamstrup genetic 2009 (PMID 19509380), van der Valk 2016 (PMID 27496857), Thanassoulis 2013 (PMID 23388002), Kamstrup CCHS 2008 (PMID 18086931). B-only — Koschinsky/NLA statement, PMC11607505, PMC10945898, Marcovina 2018 (PMID 30100157), Nissen/lepodisiran 2025, Tsimikas pelacarsen 2020 + O'Donoghue olpasiran 2022, EAS-FAQ/ACC thresholds compilation (PMID 37188555). No author/PMID/DOI/journal/tag appears under two different identities across sections.

### institutions — scanned: 2 shared (compared)
| Entity | Sections | Section A value | Section B value | Canonical | Match? |
|--------|----------|-----------------|-----------------|-----------|--------|
| Copenhagen City Heart Study | A §2/§3 ("CCHS") | "Copenhagen City Heart Study (CCHS)" | (referenced via study lineage) | Copenhagen City Heart Study (CCHS) | YES |
| Copenhagen General Population Study | A §2, B §risk-thresholds | "Copenhagen General Population Study" | "Copenhagen General Population Study" | Copenhagen General Population Study | YES |

Both Danish general-population cohort names spelled and abbreviated consistently; no divergence.

### compound_identifiers — scanned: 0 shared (compared)
RNA-agent nomenclature (pelacarsen, olpasiran, lepodisiran) and Lp(a)/apo(a)/apoB-100 nomenclature appear consistently within each section. Pelacarsen/olpasiran/lepodisiran are Section-B-only (Section A is identity/physiology and does not cite the RNA agents), so no cross-section pair exists. Shared nomenclature Lp(a), apo(a), apoB-100, KIV-2 is rendered identically in both. No second-section instance disagrees → 0 compared pairs in conflict.

### regulatory_dates — scanned: 0
No FDA/EMA approval dates in either section (the RNA agents are explicitly investigational/not approved). Nothing to compare.

### trial_registrations — scanned: 0 shared (compared)
Trials named in Section B only (Lp(a)HORIZON, OCEAN(a)-DOSE / OCEAN(a)-Outcomes, ALPACA, ACCLAIM-Lp(a)); no NCT numbers given in either section and Section A names no trials. No cross-section identifier pair.

## Gate scaffold

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 1, "mismatch_count": 0},
    "institutions": {"scanned": 2, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 0, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 0, "mismatch_count": 0},
    "trial_registrations": {"scanned": 0, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 1
}
```
