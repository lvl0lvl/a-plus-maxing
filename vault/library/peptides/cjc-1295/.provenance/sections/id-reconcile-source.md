# Phase 4.25 — ID-RECONCILE cross-section consistency audit (CJC-1295) — iteration 2

Re-verification after the iteration-1 HALT on a single regulatory_dates contradiction:
Sections D and F asserted CJC-1295 was "removed from Category 2 ~Sept 2024," which
contradicted Section E (the regulatory-owner section, establishing CJC-1295 was NOT
removed — absent from the Apr-2026 removed-twelve; interim Cat-2 since 2023; PCAC voted
against positive-list addition Dec 4 2024). D and F were remediated to match E. This
pass re-checks all five entity classes across sections A–F. Detection only.

## Citations

- **Teichman 2006, PMID 16352683, DOI 10.1210/jc.2005-1536** — A [1], B [1], D [1].
  Identical PMID, DOI, author list (Teichman SL, Neale A, Lawrence B, Gagnon C,
  Castaigne J-P, Frohman LA), journal/year/vol/pages (JCEM 2006;91(3):799-805), and
  half-life (5.8-8.1 d). CONSISTENT.
- **Jetté 2005, PMID 15817669, DOI 10.1210/en.2004-1286** — A [2], B [4], C [1].
  Identical PMID, DOI, author list, journal (Endocrinology 2005;146(7):3052-3058).
  CONSISTENT.
- **Alba 2006, PMID 16822960, DOI 10.1152/ajpendo.00201.2006** — A [7], C [2] (and C
  self-check ledger line 58). Identical PMID 16822960 in both, DOI/journal/authors
  match (Am J Physiol Endocrinol Metab 2006;291(6):E1290-E1294). CONSISTENT.
- **Ionescu/Frohman 2006 (PMID 17018654)** — Section A only; single-section, not a
  cross-check entity.

Citations scanned (multi-section): 3 (Teichman, Jetté, Alba). Mismatches: 0.

## Institutions

- **ConjuChem** (developer / DAC:GRF program sponsor) — B (ConjuChem Biotechnologies,
  Montreal; program "DAC:GRF"), C (all Jetté authors ConjuChem Inc., Montreal;
  Castaigne ConjuChem co-author on Alba), D (ConjuChem CJC-1295 with DAC), E (developed
  by ConjuChem, mid-2000s, program discontinued). B and C correctly disambiguate and
  exclude the CJC-1134-PC ConjuChem records (different molecule). Spelling, role, and
  discontinuation all consistent. CONSISTENT.

Institutions scanned (multi-section): 1 (ConjuChem). Mismatches: 0.

## Compound identifiers

- **DAC vs no-DAC ("Mod GRF 1-29") distinction** — defined in all six sections; every
  section keeps WITH-DAC (albumin-binding, multi-day) separate from WITHOUT-DAC and
  states PK is never cross-attributed. CONSISTENT.
- **The four substitutions (D-Ala2 / Gln8 / Ala15 / Leu27)** — enumerated in A (lines
  18-23) and C (line 7); referenced as "four substitutions (D-Ala²/Gln⁸/Ala¹⁵/Leu²⁷)"
  in B (line 53). Identical positions/residues; matches the "tetrasubstituted"
  descriptor. CONSISTENT.
- **Two half-lives** — WITH-DAC 5.8-8.1 d (A line 45, B line 28, C line 10, D line 3),
  ~6-8 d narrative framing (A, C, E) consistent with the measured value; no-DAC ~30 min
  (A line 8, B flagged line 83, C line 12, D line 3, E line 5, F line 15); rat
  conjugate plasma-detectable >72 h (A, C). Every section attributes ~30 min to no-DAC
  ONLY and the multi-day value to DAC ONLY; no cross-attribution. CONSISTENT.

Compound_identifiers scanned (multi-section): 3 (DAC/no-DAC distinction; four-
substitution set; the two half-lives). Mismatches: 0.

## Regulatory dates — RECONCILED (iteration-1 mismatch resolved)

Section E is the regulatory-owner section and the canonical timeline:
- **Sept 2023** — CJC-1295 placed into interim 503A **Category 2**.
- **Dec 4 2024** — PCAC **voted AGAINST** adding CJC-1295 to the positive 503A Bulks
  List (anchored to FR Doc 2024-24828 + FDA meeting page [9]).
- **Apr 16 2026 — FR Doc 2026-07361** — schedules the July 23–24 2026 PCAC meeting (7
  peptides) and parallels FDA's removal of **12** peptides from Category 2.
  **CJC-1295 is NOT among the removed twelve** and is not mentioned in the FR notice —
  i.e. it was **NOT removed**.

Re-check of the remediated sections:
- **Section D** ([3], line 56) now reads: "§503A interim Category 2 list, 2023; at the
  Dec 4 2024 PCAC meeting the committee voted AGAINST adding CJC-1295 to the positive
  503A Bulks List; CJC-1295 is NOT among the 12 peptides removed from Category 2 by FR
  Doc 2026-07361 [Apr 16 2026] — i.e. it was NOT removed," and defers to §E for primary
  anchors. Consistent with E. The previous "removed Sept 2024" claim is **gone**.
- **Section F** (line 19 + [6]) now reads: "voted AGAINST adding CJC-1295 to the
  positive 503A Bulks List; CJC-1295 was NOT among the 12 peptides removed from
  Category 2 by the April 16 2026 FDA action (FR Doc 2026-07361) and remains
  non-compoundable (see §E)"; [6]: "interim Category 2 placement (2023); NOT among the
  12 peptides removed by FR Doc 2026-07361." Consistent with E. The "September 2024
  removal" claim is **gone**.

A full A–F scan finds **no surviving "Sept 2024 / September 2024 removal" claim** and
no section now asserts CJC-1295 was removed from Category 2. The three sections that
touch the 503A timeline (D, E, F) agree: 2023 Cat-2 placement → Dec 4 2024 PCAC vote
against → NOT in the Apr 2026 removed-12. The earlier soft "PCAC review pending"
characterization in D is also gone (now "voted AGAINST"), so the D/F-vs-E disagreement
is fully resolved at both the hard (removal-date) and soft (PCAC-status) levels. WADA
S2.2.4 status (prohibited at all times, 2026 List) sits in E only, no conflict.

Regulatory_dates scanned (multi-section): Sept-2023 Cat-2 placement; Dec-4-2024 PCAC
vote; Apr-16-2026 FR Doc 2026-07361 / removed-12 exclusion; NCT00267527 halt 17-Jul-2006
= 4. Mismatches: 0.

## Trial registrations

- **NCT00267527** — B [2] cites the NCT explicitly (Phase 2, HIV visceral obesity,
  ConjuChem, status Terminated, enrollment 120, no results); D describes the identical
  trial (ConjuChem CJC-1295 with DAC, Phase II, HIV visceral obesity, halted 17 July
  2006, Argentina death) without printing the NCT number. Same trial, sponsor,
  indication, and halt date (17 July 2006 in both). The enrollment discrepancy (registry
  120 vs press ~192) is acknowledged WITHIN each section as a registry-vs-press note —
  identical treatment in both, so a documented caveat, not a cross-section contradiction.
  Other ConjuChem NCTs (NCT00638716/00674466/01514149) correctly excluded as
  CJC-1134-PC. CONSISTENT.

Trial_registrations scanned (multi-section): 1 (NCT00267527). Mismatches: 0.

## Verdict
verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 3, "mismatch_count": 0, "mismatches": []},
    "institutions": {"scanned": 1, "mismatch_count": 0, "mismatches": []},
    "compound_identifiers": {"scanned": 3, "mismatch_count": 0, "mismatches": []},
    "regulatory_dates": {"scanned": 4, "mismatch_count": 0, "mismatches": []},
    "trial_registrations": {"scanned": 1, "mismatch_count": 0, "mismatches": []}
  },
  "iterations": 2,
  "halt_reasons": []
}
```
