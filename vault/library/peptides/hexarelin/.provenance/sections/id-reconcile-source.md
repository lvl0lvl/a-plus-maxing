# Phase 4.25 — ID-RECONCILE (shared-entity cross-section consistency)

Scope: cross-check shared entities appearing in >1 of sections A–F for cross-section
agreement. Detect mismatches only; do not fix content. A fact appearing in a single
section is out of scope and is NOT a mismatch.

---

## Citations

Eight PMIDs/papers are cited in more than one section. Each was checked for
author/year/title/journal/volume/page agreement across the sections that cite it.

- **Ghigo 1994 — PK / multiroute (PMID 8126144).** A[1] and B[1]. Both give
  "Ghigo E, Arvat E, Gianotti L, Imbimbo BP, Lenaerts V, Deghenghi R, Camanni F. 1994,
  JCEM 78(3):693–698, PMID 8126144." **Agree.**
- **Bodart 2002 — CD36 cardiac (PMID 11988484).** A[7] and C[6]. A gives PMID 11988484 +
  DOI 10.1161/01.RES.0000016164.02525.B4, Circ Res 90(8):844–849; C[6] gives the same DOI,
  same volume/pages, same author list (C omits the bare PMID but is otherwise identical).
  **Agree.**
- **Massoud 1996 — dose-response (PMID 8954038).** B[2] and D[2]. Both "Massoud AF,
  Hindmarsh PC, Brook CGD, JCEM 1996, PMID 8954038" (D adds 81(12):4338–4341).
  **Agree.**
- **Arvat 1997 Peptides — GHRP-2/hexarelin comparison (PMID 9285939).** B[6] and D[1].
  Both "Arvat E, di Vito L, Maccagno B, Broglio F, Boghen MF, Deghenghi R, Camanni F,
  Ghigo E, Peptides 1997;18(6):885–891." **Agree.**
- **Rahim/O'Neill/Shalet 1998 JCEM — long-term GH status (the 19.1→10.5 dataset).**
  B[7] and C[2]. Both "Rahim A, O'Neill PA, Shalet SM, JCEM 1998;83(5):1644–1649."
  **Agree.** (Note D cites a *different* Rahim/O'Neill/Shalet paper — see below.)
- **Rahim/Shalet 1998 "Does desensitization to hexarelin occur?" (PMID 10990150).**
  B[8], C[3], D[5]. All three: "Rahim A, Shalet SM, Growth Horm IGF Res 1998, PMID 10990150."
  **Agree across all three.**
- **Bowers 1990 (PMID 2108187), Deghenghi 1994 (PMID 7910650), Devesa 2021, Colldén 2017,
  Giustina 1995 (7561633), Korbonits 1999, Arvat 1997 EJE (9437229), Bisi 1999 (10528131),
  Laron 1995 (8548949), Locatelli 1999, Agbo 2019, Reed 2013, Murphy 2020.** Each cited
  in exactly one section → out of scope (not cross-checked, not a mismatch).

**Disambiguation — the two Broglio cardiac papers.** These are distinct citations, not a
mismatch: C[5] = Broglio **2001** Endocrine, PMID 11322491, n=7+7+12, acute IV 2.0 µg/kg
(LVEF rise in normal/GHD, none in dilated CMP). D[4] = Broglio **2002** Eur J Pharmacol,
PMID 12144941, n=24 CAD during bypass (↑LVEF/CI/CO, ↑MAP). Different year/journal/PMID/
population — correctly treated as two separate papers, no cross-attribution.

**Disambiguation — the three Rahim/Shalet chronic-dosing papers.** Also distinct, not a
mismatch: (a) Rahim/O'Neill/Shalet 1998 JCEM "GH status during long-term therapy" (B[7]/C[2]);
(b) Rahim/Shalet 1998 GH IGF Res "Does desensitization occur?" (B[8]/C[3]/D[5]); (c)
Rahim/O'Neill/Shalet **1999** Clin Endocrinol "effect of chronic hexarelin on the
pituitary-adrenal axis and prolactin," PMID 10341859 (D[3] only). All three describe the
same 16-wk 1.5 µg/kg SC BID elderly cohort but are three separate publications with distinct
journals/PMIDs — handled consistently.

**Judge-flagged ED50 0.39-vs-0.48 — SINGLE-SECTION / non-mismatch, confirmed.** Both
numbers trace to one paper (Massoud 1996) but to two *different endpoints*: GH ED50 ≈ 0.48
µg/kg and prolactin ED50 ≈ 0.39 µg/kg. B keeps them correctly paired (B.1 GH 0.48 ± 0.02;
B.3 prolactin 0.39 ± 0.02). D keeps them correctly paired (D.1 prolactin 0.39; bib[2] GH
0.48). So across B and D the two figures **agree by endpoint** — there is no cross-section
disagreement. The "0.39 vs 0.48" appearance is a within-Section-B reading nit (two figures
side by side), not a cross-section mismatch.

**Judge-flagged Bisi "n=7+7 vs 7+9" — SINGLE-SECTION, confirmed.** Bisi 1999 is cited only
in Section C. The discrepancy is internal to C: the EVIDENCED heading line reads
"(human, acute, n=7+7)" while C's prose ("7 GH-deficient … + 9 healthy male controls") and
C's bibliography tag ("n=7 GHD + 9 controls") read 7+9. Because Bisi appears in no other
section, this is a within-Section-C nit, **not** a cross-section mismatch. (Out of ID-RECONCILE
scope to fix; flagged here only to confirm classification per the prompt.)

Scanned: 8 multi-section citations. Mismatches: 0.

---

## Institutions / developer

- **University of Turin / Ghigo–Arvat–Broglio–Bisi group** — A ("Turin endocrine group of
  Ezio Ghigo"), C (table rows "Ghigo/Broglio (Turin)", "University of Turin"), D ("the Turin
  group — Ghigo, Arvat, Broglio"), F ("Mediolanum Farmaceutici (Milan/Turin)"). **Consistent.**
- **Developer = Deghenghi + Mediolanum Farmaceutici (Europeptides co-developer).** A
  ("Romano Deghenghi … Europeptides / the Italian research lineage"), C ("Mediolanum/Deghenghi
  (developer)"), E ("developed under codes MF-6003 / EP-23905 by Mediolanum Farmaceutici, with
  Europeptides as co-developer"), F ("Mediolanum Farmaceutici (Milan/Turin), with R. Deghenghi
  as principal investigator, early 1990s"). **Consistent** — same developer entity and lineage
  across A/C/E/F.
- **Developmental code.** A "EP 23905"; E "MF-6003 / EP-23905." E adds the MF code but the
  shared EP-23905/EP 23905 identifier agrees. **Consistent.**

Scanned: 3 shared institution/developer entities. Mismatches: 0.

---

## Compound identifiers

- **Class: GHRP / GHS-R1a (ghrelin-receptor) agonist, NOT a GHRH analogue.** Stated
  explicitly and identically in A, B (compound-class note), C (class note), D (defining fact),
  E, and F. No section ever frames hexarelin as a GHRH analogue or cross-attributes its dosing/
  mechanism to GHRH analogues (CJC-1295/sermorelin/tesamorelin are consistently named as the
  *separate* GHRH-analogue partners). **Consistent.**
- **Second receptor CD36 (cardiac, GH-independent).** A, C, D agree CD36 is the cardiac
  target; A and C both attribute the photoaffinity identification to Bodart. **Consistent.**
- **Sequence His-D-2-methyl-Trp-Ala-Trp-D-Phe-Lys-NH₂.** Identical in A, B, C, E (F vendor
  consistent). **Consistent.**
- **INN examorelin; CAS 140703-51-1; MW ≈ 887 / C₄₇H₅₈N₁₂O₆.** A, E, F agree on examorelin;
  CAS 140703-51-1 matches A[5] and F[12]; formula/MW appear only in A (single-section).
  **Consistent** where shared.
- **Half-life ("tens of minutes").** Section A only — single-section, no conflict.

Scanned: 5 shared compound-identifier facts. Mismatches: 0.

---

## Regulatory dates / facts

- **Never approved (FDA/EMA/any jurisdiction).** C, D, E, F all assert this. **Consistent.**
- **NOT among the April-2026 removed-12.** E enumerates the 12 (BPC-157, TB-500, KPV, MOTS-c,
  DSIP/Emideltide, Semax, Epitalon, GHK-Cu, Melanotan-II, Dihexa, PEG-MGF, LL-37) and states
  hexarelin is not among them; F independently states hexarelin "appears on none of these
  lists." The removed-12 / July-2026-agenda partition matches between E and F. **Consistent.**
- **FR Doc 2026-07361 = PCAC Notice of Meeting (July 23–24, 2026), not the removal action.**
  E states this explicitly with the agenda (Day 1 BPC-157/KPV/TB-500/MOTS-c; Day 2 DSIP/Semax/
  Epitalon); F[4][5] describes the same April-2026 action + PCAC July-2026 agenda with the same
  compound split (though F cites the FDA-law-blog/Orrick rather than the FR doc number). Agenda
  contents agree. **Consistent.**
- **WADA S2.2.4, examorelin/hexarelin named.** Stated in E only (full detail). F does not
  restate the decimal; no conflict. Single authoritative statement.

**Soft framing note (NOT a fact mismatch).** On §503A *mechanism*, E flags genuine
uncertainty ("could not confirm Category 2 vs never-nominated … should not be over-stated"),
whereas F leans "apparently never nominated … not among the Sept-2023/2024 Category-2 cohort."
Both sections reach the identical factual end-state — hexarelin is not on the eligible bulks
list and is not §503A-compoundable. This is a difference in stated confidence about an
unresolved sub-question, not a contradiction of any asserted fact, so it does not rise to a
cross-section mismatch.

Scanned: 4 shared regulatory facts. Mismatches: 0.

---

## Trial registrations

No clinical-trial registry identifiers (NCT / EudraCT) are cited in any section; E explicitly
notes the Phase-II-then-discontinued narrative was not confirmable against a primary trials
registry. Nothing shared to reconcile.

Scanned: 0. Mismatches: 0.

---

## Dose figures (cross-class spot-check)

- **Chronic paradigm 1.5 µg/kg SC BID × 16 wk (elderly).** B, C, D agree on dose, route,
  frequency, duration, and population. **Consistent.**
- **Acute IV/SC PD doses (1–2 µg/kg IV; 1.5–3 µg/kg SC; IV 1 µg/kg ≈ 2× GHRH).** A and B
  agree. **Consistent.**
- **SC bioavailability ≈ 77%; intranasal ≈ 4.8%; oral ≈ 0.3%.** A and B match. **Consistent.**
- **Practitioner ~100 mcg SC convention.** Section F only, explicitly demarcated as practice
  convention and kept distinct from the µg/kg PD doses — not conflated, not cross-attributed.
  **Consistent (no conflation).**

---

## Key numbers (cross-class spot-check)

- **Desensitization GH AUC 19.1 → 10.5 µg/L·h over 16 wk; recovery to 19.4 ± 3.7.** B
  (19.1±2.4 → 10.5±1.8 → 19.4±3.7), C (19.1±2.4 → 10.5±1.8 → ~19.4), D (19.1 → 13.1 → 12.3 →
  10.5 → recovery). All agree on endpoints and recovery. **Consistent.**
- **Cortisol ~+40% at 0.5 µg/kg; prolactin peak ~+180%.** B.3 and D.1 agree. **Consistent.**
- **ED50 GH 0.48 / prolactin 0.39.** B and D agree by endpoint (see Citations). **Consistent.**
- **No significant IGF-1 / IGFBP-3 change over the chronic course.** B, C, D agree.
  **Consistent.**

---

## Verdict

verdict: PASS

All shared entities appearing in more than one section agree across sections. The two
judge-flagged items were confirmed to be SINGLE-SECTION nits (Bisi n=7+7-vs-7+9 internal to
Section C; ED50 0.39-vs-0.48 a within-section two-endpoint reading, with B and D agreeing by
endpoint) and therefore are not cross-section mismatches. The only inter-section divergence
found (E vs F on §503A nomination *mechanism*) is a difference in stated confidence over an
explicitly-unresolved sub-question, with identical factual end-state — not a fact mismatch.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":8,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":3,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":5,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":4,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":0,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
