# ID-Reconcile — GlycA (Phase 4.25, iteration 2)

Independent cross-section identity reconciliation of `section-A.md` vs `section-B.md`
(post-fix grep audit + self-check blocks excluded from scan). Only entities appearing
in BOTH sections were compared. RE-reconcile after the remediation that retagged
Otvos 2015 (PMID 25779987) in Section A from `mechanism_review` → `cohort`.

## Verdict

verdict: PASS

Otvos 2015 (PMID 25779987 / DOI 10.1373/clinchem.2014.232918) now carries `cohort`
in BOTH sections — at every inline citation and in the bibliography. The iteration-1
citation-type-tag mismatch is RESOLVED. Full re-scan finds 0 mismatches across all
five entity classes. iterations = 2.

### Otvos 2015 retag — RESOLVED

| Site | Section A | Section B |
|---|---|---|
| Inline citations | `[1, cohort]` at lines 8, 11, 28, 35 | `[1, cohort]` at lines 7, 20 |
| Bibliography | line 93 — `cohort` — Tier 1 | line 46 — `[cohort / analytical validation]` |

The former `mechanism_review` tag on Otvos 2015 in Section A is gone. The remaining
`mechanism_review` inline hits in Section A (lines 13, 31, 37, 80, 82, 87, 89) all
belong to ref 8 (Connelly 2017, J Transl Med 15:219 — a genuinely different
narrative-review source), correctly tagged and NOT in conflict.

## Per-class reconciliation

| Entity class | Scanned | Mismatch | Detail |
|---|---|---|---|
| citations | 5 | 0 | **Otvos2015** (PMID 25779987 / DOI 10.1373/clinchem.2014.232918) = `cohort` in BOTH (A bib line 93; B bib line 46) — RESOLVED. Connelly appears in both as two DIFFERENT papers (A ref8 = J Transl Med 2017, PMID 29078787; B ref2 = PMC8315361) — distinct entities, both `mechanism_review`, no disagreement. Akinkuolie (A-ref2 25249300 / A-ref3 25908766), Lawler (A-ref7 26951635), Ritchie (A-ref6 27136058) are Section-A-only — each internally `cohort`, consistent, nothing to cross-reconcile. |
| institutions | 4 | 0 | Nightingale Health (Finland) + LabCorp NMR LipoProfile named only in Section B and described consistently within B (Nightingale = mmol/L scale, LabCorp = μmol/L scale, non-interchangeable). MESA / Women's Health Study cohort group names carry no institution-identity conflict across sections. No shared institution entity diverges. |
| compound_identifiers | 6 | 0 | GlycA nomenclature consistent — "glycoprotein acetylation" (A) / "glycoprotein acetyls" (B) are accepted equivalent expansions; composite-NMR signal description (N-acetyl methyl protons of glycan side chains; same five acute-phase glycoproteins — α1-acid glycoprotein, haptoglobin, α1-antitrypsin, α1-antichymotrypsin, transferrin) identical in both. Platform names (Nightingale, LabCorp NMR LipoProfile) consistent. Unit systems mmol/L vs μmol/L described consistently and explicitly as platform-specific / non-interchangeable (B §Units; 1230 μmol/L ≡ 1.23 mmol/L). CVs 1.9%/2.6%/4.3% and correlations 0.56/0.46/0.35 identical across A and B. |
| regulatory_dates | 0 | 0 | No FDA/EMA approval or guideline-endorsement dates asserted in either section (both state GlycA is research/emerging-grade, NOT guideline-endorsed). Nothing to reconcile. |
| trial_registrations | 0 | 0 | No NCT/ISRCTN trial-registration identifiers in either section. Cohorts (WHS, MESA, PREVEND, FINRISK, JUPITER, UK Biobank, TwinsUK) named by study, not registration ID. Nothing to reconcile. |

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 5, "mismatch_count": 0},
    "institutions": {"scanned": 4, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 6, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 0, "mismatch_count": 0},
    "trial_registrations": {"scanned": 0, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 2
}
```
