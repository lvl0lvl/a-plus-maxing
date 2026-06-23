## Verdict

verdict: PASS

```json
{"phase":"4.25","verdict":"PASS","iterations":3,"entity_classes":{"citations":{"scanned":28,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":8,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":12,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":10,"mismatch_count":0,"mismatches":[]}},"halt_reasons":[]}
```

## Per-class prose tables (Iteration 3 — Final PASS)

### Citations (28 scanned, 0 mismatches)

| PMID | Lead Author | Journal | Year | Tag(s) by section | Status |
|------|-------------|---------|------|-------------------|--------|
| 15178689 | Zhao K | J Biol Chem | 2004 | A:`in_vitro` / E:`in_vitro` | PASS — iter-2 residual CONFIRMED RESOLVED |
| 23813215 | Birk AV | JASN | 2013 | A:`animal` / C:`animal` / E:`animal` | PASS |
| 38602181 | Thompson WR | Genet Med | 2024 | A:`open_label` / B:`open_label` / D:`open_label` / E:`open_label` | PASS |
| 37268435 | Karaa A | Neurology | 2023 | B:`rct` / C:`rct` / D:`rct` / E:`rct` | PASS |
| 26586786 | Gibson CM | Eur Heart J | 2016 | B:`rct` / C:`rct` | PASS — n=300 and NCT01572909 consistent in B and C |
| 29500292 | Karaa A | Neurology | 2018 | B:`rct` / E:`rct` | PASS — iter-2 residual CONFIRMED RESOLVED (NCT02367014 in both B and E; NCT02367729 absent from all 5 sections) |
| 32273339 | Mitchell W | J Biol Chem | 2020 | A:`in_vitro` | PASS (single section) |
| 32554501 | Chavez JD | PNAS | 2020 | A:`in_vitro` | PASS (single section) |
| 35913044 | Mitchell W | eLife | 2022 | A:`mechanism_review` | PASS (single section) |
| 24117165 | Szeto HH | Br J Pharmacol | 2014 | A:`mechanism_review` / C:`mechanism_review` | PASS |
| 16796378 | Szeto HH | AAPS J | 2006 | A:`mechanism_review` | PASS (single section) |
| 41260682 | Zhao C | Drug Discov Ther | 2026 | A:`regulatory` | PASS (single section) |
| 32641818 | Allen ME | Commun Biol | 2020 | C:`animal` | PASS (single section) |
| 36934127 | Patel N | Sci Rep | 2023 | C:`animal` | PASS (single section) |
| 23692570 | Siegel MP | Aging Cell | 2013 | C:`animal` | PASS (single section) |
| 32574516 | Chiao YA | eLife | 2020 | C:`animal` | PASS (single section) |
| 36250163 | Nickel K | Aging Pathobiol Ther | 2022 | C:`animal` | PASS (single section) |
| 36400945 | Russo S | Sci Rep | 2022 | C:`animal` | PASS (single section) |
| 32068002 | Butler J | J Card Fail | 2020 | C:`rct` | PASS (single section) |
| 36056411 | Thompson WR | Orphanet J Rare Dis | 2022 | B:`cohort` / E:`cohort` | PASS — tag consistent; tier delta (B=2, E=1) is informational only |
| 36246181 | Mettu PS | Ophthalmol Sci | 2022 | B:`open_label` | PASS (single section) |
| 36246187 | Allingham MJ | Ophthalmol Sci | 2022 | B:`open_label` | PASS (single section) |
| 39605874 | Cousins SW | Ophthalmol Sci | 2024 | B:`rct` / D:`rct` | PASS — tag consistent; tier delta (B=2, D=1) is informational only |
| 29217757 | Daubert MA | Circ Heart Fail | 2017 | E:`rct` | PASS (single section) |
| 28916603 | Saad A | Circ Cardiovasc Interv | 2017 | E:`rct` | PASS (single section) |
| 37923251 | Karanjia R | Ophthalmology | 2024 | E:`rct` | PASS (single section) |
| 31727138 | Li J | J Neuroinflammation | 2019 | E:`animal` | PASS (single section) |
| 33077895 | Thompson WR | Genet Med | 2021 | E:`rct` | PASS (single section) — Section B cites NCT03098797 registry for the same trial; not a divergence, different citation form |

**Note on Sadhwani 2021 (Section D[9], Genet Med 2021;23(3):645–652, PMC7935714):** Distinct paper from Thompson 2021 (PMID 33077895, pp 471–478). Both describe the TAZPOWER population; D uses Sadhwani for ISR safety data, B/E use Thompson for efficacy. These are separate publications from the same trial — not a shared-entity divergence.

---

### Institutions (8 scanned, 0 mismatches)

| Institution | Sections | Status |
|---|---|---|
| Weill Cornell Medicine | A, E | PASS — A: "Weill Cornell Medicine"; E: "Weill Cornell Medicine, Department of Pharmacology" — consistent |
| IRCM Montreal | A, E | PASS — A: "IRCM, Montreal"; E: "Institut de Recherches Cliniques de Montréal / IRCM" — same institution |
| Stealth BioTherapeutics / Mighty Therapeutics | B, D, E | PASS — all note same sponsor trajectory |
| University of Washington (Rabinovitch/Marcinek lab) | C | PASS (single section) |
| Mayo Clinic | E | PASS (single section) |
| Chinese PLA General Hospital / Beijing Institute of Pharmacology | E | PASS (single section) |
| Cornell Research Foundation | E | PASS (single section) |
| FDA / DailyMed (issuing body) | A, B, D, E | PASS — same issuing body cited consistently |

---

### Compound identifiers (12 scanned, 0 mismatches)

| Identifier | Sections | Status |
|---|---|---|
| SS-31 / elamipretide (INN) | A, B, C, D, E | PASS — universal and synonymous |
| MTP-131 (Stealth internal code) | A, B | PASS — consistent in both sections |
| Bendavia (cardiac trial brand) | A, B | PASS |
| Forzinity / FORZINITY (approved brand) | A, B, D, E | PASS — consistent spelling and context |
| NDA 215244 | A, B, D, E | PASS — identical |
| DailyMed setid 146bf34c-76f2-48db-ac07-fb29cce2cd75 | A, B, D, E | PASS — identical URL/setid in all four |
| CAS 736992-21-5 | A only | PASS (single section) |
| MW 639.8 g/mol; formula C₃₂H₄₉N₉O₅ | A only | PASS (single section) |
| Sequence D-Arg–Dmt–Lys–Phe–NH₂ | A only | PASS (single section) |
| SS-20 (family member) | A only | PASS (single section) |
| SS-02 (family member) | A only | PASS (single section) |
| 40 mg SC once daily (approved dose) | A, B, C, D, E | PASS — consistent dose in all sections |

---

### Regulatory dates (6 scanned, 0 mismatches)

| Event | Sections | Value | Status |
|---|---|---|---|
| FDA accelerated approval date | A, B, D, E | October 30, 2025 | PASS — identical in all four sections |
| NDA number | A, B, D, E | NDA 215244 | PASS — identical in all four sections |
| DailyMed setid | A, B, D, E | 146bf34c-76f2-48db-ac07-fb29cce2cd75 | PASS — identical in all four sections |
| CRL date | D, E | Not primary-verified (both state this explicitly) | PASS — consistent uncertainty framing |
| NDA resubmission accepted | D, E | January 29, 2024 | PASS |
| NuPOWER primary completion | E | September 30, 2024 | PASS (single section) |

---

### Trial registrations (10 scanned, 0 mismatches)

| Trial | NCT | Sections | Status |
|---|---|---|---|
| MMPOWER Phase 1/2 / SPIMM-201 | NCT02367014 | B, E | PASS — iter-2 residual CONFIRMED RESOLVED (NCT02367729 absent from all 5 sections) |
| MMPOWER-2 | NCT02805790 | B | PASS (single section) |
| MMPOWER-3 | NCT03323749 | B, C, E | PASS — all sections consistent |
| TAZPOWER | NCT03098797 | B, E | PASS |
| EMBRACE-STEMI | NCT01572909 | B, C | PASS — n=300 consistent in both |
| SPIHF-201 / HFrEF Phase 2 | NCT02788747 | B | PASS (single section) |
| ReCLAIM-2 | NCT03891875 | B, D | PASS |
| ReNEW Phase 3 AMD | NCT06373731 | B | PASS (single section) |
| NuPOWER | NCT05162768 | E | PASS (single section) |
| 4TAZPower confirmatory | NCT07531251 | D | PASS (single section) |

---

## Iter-2 Residuals — Final Confirmed Resolved

1. **PMID 15178689 (Zhao 2004 JBC) — tag:** Section A line 157: `in_vitro`. Section E line 88: `in_vitro`. Tag is consistent across both sections. **RESOLVED.**

2. **PMID 29500292 / NCT for Karaa 2018 Neurology — NCT number:** Section B line 9: NCT02367014. Section E line 17: NCT02367014. The erroneous NCT02367729 is absent from all five sections (grep across A–E returned zero hits). **RESOLVED.**
