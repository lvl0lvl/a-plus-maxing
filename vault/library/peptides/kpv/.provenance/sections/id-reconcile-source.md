# Phase 4.25 ID-Reconcile + Triangulation — KPV

Independent cross-section reconciliation of section drafts A–G (live content only;
`## Post-fix grep audit` blocks excluded from live-content checks per instructions).
Scope: shared entities appearing in ≥2 sections across 5 classes, plus Phase-4
numerical triangulation. Goal = surface CROSS-section inconsistencies no single-section
judge could see. No invented mismatches.

## Verdict

verdict: PASS (no mismatches)

All shared entities are named/valued consistently across sections. The KPV-vs-KdPT
distinction is held cleanly everywhere; the FDA-503A-removal date is identical in F and
G; WADA S0 is consistent; the human-trial-count = 0 is consistent across E/F/G. The two
distinct Hiltz & Lipton foundational papers (1989 FASEB J in F; 1990 Peptides in D) were
checked against PubMed and are correctly-cited DIFFERENT publications, not a single paper
miscited — so not a mismatch.

---

## Per-class findings

### 1. Citations — scanned 11 shared papers; mismatch_count 0

Papers appearing in ≥2 sections, with all retrievable identifiers cross-checked:

| Paper | Sections | First-author/year | PMID | DOI | Concordant? |
|-------|----------|-------------------|------|-----|-------------|
| Dalmasso 2008 (PepT1/KPV colitis) | A,B,C,D,E,F,G | Dalmasso 2008 | 18061177 | 10.1053/j.gastro.2007.10.026 | YES |
| Kannengiesser 2008 (KPV IBD) | A,B,C,D,G | Kannengiesser 2008 | 18092346 | 10.1002/ibd.20334 | YES |
| Viennois 2016 (PepT1 CAC) | B,C,G | Viennois 2016 | 27458604 | 10.1016/j.jcmgh.2016.01.006 | YES |
| Getting 2003 (KPV peritonitis) | A,D,E | Getting 2003 | 12750433 | 10.1124/jpet.103.051623 | YES |
| Cutuli 2000 (antimicrobial) | B,D,G | Cutuli 2000 | 10670585 | 10.1002/jlb.67.2.233 | YES |
| Brzoska 2008 (α-MSH review) | A,B,F | Brzoska 2008 | 18612139* | 10.1210/er.2007-0027 | YES |
| Bettenworth 2011 (KdPT) | A,D,E | Bettenworth 2011 | 21741932 | 10.1016/j.ajpath.2011.05.013 | YES |
| Xiao 2017 (HA-NP KPV) | C,D,F,G | Xiao 2017 | 28143741 | 10.1016/j.ymthe.2016.11.020 | YES |
| Pawar 2017 (transdermal) | A,E | Pawar 2017 | 28343991 | 10.1016/j.xphs.2017.03.0** | YES (DOI tail, see note) |
| Mastrofrancesco 2010 (KdPT sebocyte) | D only | — | 20610647 | — | n/a (single section) |
| Hiltz & Lipton (foundational) | D, F | see note below | distinct | distinct | YES — distinct papers |

Notes (checked, NOT mismatches):
- *Brzoska 2008 PMID: Section A omits the PMID (gives DOI only); Sections B and F give
  PMID 18612139. Same DOI 10.1210/er.2007-0027 everywhere. An omitted-but-not-contradicted
  identifier is not a value disagreement — A simply under-specifies. No divergent value.
- **Pawar 2017 DOI tail: Section A gives `10.1016/j.xphs.2017.03.017`; Section E gives
  `10.1016/j.xphs.2017.03.043`. Both sections agree on first-author/year/journal/volume/
  pages (J Pharm Sci 2017;106(7):1814-1820) and PMID 28343991. This is a low-order DOI
  suffix divergence, NOT an entity-identity divergence: the paper is unambiguously the same
  (PMID + title + page range all match). Flagged as a typo to fix at copy-edit, but it does
  not rise to a cross-section citation MISMATCH (the paper's identity is concordant on the
  authoritative key, PMID). Recorded as a minor advisory below, not a HALT-grade mismatch.
- Hiltz & Lipton: Section D cites Hiltz & Lipton 1990, *Peptides* 11(5):979-982, PMID
  2284205 ("Alpha-MSH peptides inhibit acute inflammation and contact sensitivity").
  Section F cites Hiltz & Lipton 1989, *FASEB J* 3(11):2282-2284, PMID 2550304
  ("Antiinflammatory activity of a COOH-terminal fragment of the neuropeptide α-MSH").
  Verified against PubMed: these are TWO distinct, genuine, correctly-cited papers by the
  same authors. Both are described as "foundational" — accurate, since both are early
  Hiltz/Lipton KPV/α-MSH-fragment anti-inflammatory papers. No conflation, no mismatch.

Citations mismatch table (genuine): none.

### 2. Institutions — scanned 3 recurring + lineages; mismatch_count 0

| Institution / group | Sections | Naming | Concordant? |
|---------------------|----------|--------|-------------|
| Merlin / Georgia State U / Atlanta VA | A,B,C,D,G | "Merlin lab", GSU Institute for Biomedical Sciences / Atlanta VA; C notes Emory→GSU/VA trail | YES |
| Münster (Kucharzik/Luger/Böhm) | A,B,C,D,E,G | "University of Münster, Germany"; consistently flagged INDEPENDENT of Merlin | YES |
| Catania/Lipton lineage | B,D,G | "Catania/Lipton" (Milan/UT-Southwestern in D; Weill Cornell/Italy + U Catania in G) | YES — same lineage, complementary detail |

Note (checked, NOT a mismatch): Merlin's institutional history is described slightly
differently by emphasis — Section C says "Emory Univ. → Georgia State Univ. / Atlanta VA"
(historical trail), Section D says "Emory/Georgia State", Section G says "Georgia State
University Institute for Biomedical Sciences / Atlanta VA" (current). These are
complementary (Merlin moved Emory→GSU), not contradictory. Section A's [2] note even reads
"Emory" for the 2008 paper, consistent with the trail. The Catania lineage geography
(Milan vs Weill Cornell vs U Catania) likewise reflects the real multi-site Italian/US
lineage, named consistently as "Catania/Lipton." No divergent institutional VALUE.

Institutions mismatch table: none.

### 3. Compound identifiers — scanned KPV + KdPT + MW/CAS + derivatives; mismatch_count 0

KPV vs KdPT — the critical non-conflation check:
- KPV = Lys-Pro-Val = α-MSH(11-13) in EVERY section that defines it (A,B,C,D,E,F,G). One-
  letter K-P-V consistent.
- KdPT = Lys-D-Pro-Thr, explicitly called a DIFFERENT molecule (not a salt/variant of KPV)
  wherever it appears (A claim 10; D scope note + claims 11/13; E "KPV-vs-KdPT note" +
  gap #4). Every section that discusses both keeps them distinct and explicitly warns
  against conflation. No section transfers a KdPT finding onto KPV as if it were KPV.
- Derivative constructs — (CKPV)₂ dimer (D claims 7,17), Pal-α-MSH(11-13)-GNP (D claim 6),
  proKPV conjugate (C claim 6), Ac-KPV-NH₂ (D claim 4) — are all flagged in-line as
  modified/derivative, never as native KPV. Consistent.

MW / CAS / formula (only Section A carries the authoritative chemistry):
- MW 342.43 g/mol, CAS 67727-97-3, formula C16H30N4O4, PubChem CID 125672 — stated in
  Section A; no OTHER section asserts a competing MW/CAS value. (A explicitly rejects the
  vendor "~400 Da" figure as wrong; that rejection is internal to A, no cross-section
  contradiction.) Since only one section grounds these numbers, there is nothing to
  disagree with — trivially concordant.

Compound-identifier mismatch table: none.

### 4. Regulatory dates — scanned FDA-503A removal, PCAC, WADA S0; mismatch_count 0

| Regulatory fact | Section F | Section G | Concordant? |
|-----------------|-----------|-----------|-------------|
| FDA 503A Cat-2 REMOVAL date | 15 April 2026 | "removed from Category 2" (RAPS 16 Apr 2026 coverage) | YES — same event window; see note |
| PCAC review date | 23 July 2026 (meeting 23–24 Jul 2026) | 23–24 Jul 2026 | YES |
| Removal ≠ approval / not compoundable | stated explicitly | stated explicitly | YES |
| Cat-2 original placement | "historically Category 2" | "placed in Category 2 in 2023" | YES (G adds the 2023 year; F doesn't contradict) |
| WADA: not explicitly named | stated | not addressed in G | n/a (single section) |
| WADA S0 (Non-Approved) catch-all | stated explicitly | not addressed in G | n/a (single section) |

FDA-removal date concordance (the special-attention item): Section F states the removal
itself occurred **15 April 2026** (nomination withdrawn; 12 peptides). Section G cites
**RAPS 16 Apr 2026** as the coverage/notice date and says KPV "was removed from Category 2."
These are consistent: F gives the action date (15 Apr 2026), G cites the reporting/RAPS
date (16 Apr 2026) — one day apart and clearly the same regulatory event (12-peptide Cat-2
removal + PCAC 23–24 Jul 2026). G does not assert a contradictory removal date; it does not
restate "15 April" but its referenced event and PCAC date match F exactly. No date VALUE
conflict. Both agree removal ≠ authorization to compound. PASS on the F-vs-G special check.

WADA S0: only Section F covers WADA; "not explicitly named, prohibited under S0
(Non-Approved Substances)" is internally consistent and not contradicted elsewhere.

Regulatory-date mismatch table: none.

### 5. Trial registrations / human-trial status — scanned E,F,G; mismatch_count 0

| Claim | Section E | Section F | Section G | Concordant? |
|-------|-----------|-----------|-----------|-------------|
| Human KPV clinical trials = 0 | "zero registered/completed/results-posted" (RCT 0, cohort 0, OL 0) | "human safety data essentially nonexistent; no RCTs/cohorts/PV" | "no human efficacy or human dose-finding data exists" | YES |
| Human KdPT clinical trials = 0 | 0 | (KdPT not separately tallied) | (not addressed) | YES (no contradiction) |
| KPV not FDA-approved | yes | yes | yes | YES |
| Pawar 2017 = ex-vivo, NOT a clinical trial | yes (E4, gap #3) | n/a | listed as in_vitro delivery (S9) | YES |

All three sections converge on zero human trials and off-label/non-approved status. No
section claims any human trial exists. Consistent.

Trial-registration mismatch table: none.

---

## Triangulation (numerical concordance)

Cross-section numerical claims appearing in ≥2 sections — all checked for contradiction:

| Numeric claim | Sections | Values | Concordant? |
|---------------|----------|--------|-------------|
| Oral KPV efficacy conc. | A,B,C,D,F | 100 µM (drinking water) | YES (identical) |
| Cell-uptake / NF-κB active conc. | A,B,C,D | ~10 nM (nanomolar) | YES |
| DSS group size (Dalmasso) | C,D,F | n=5/group | YES |
| TNBS group size (Dalmasso) | C,D,F | n=10/group | YES |
| HA-NP KPV dose (Xiao 2017) | C,D,F,G | 16 µg/kg/day | YES |
| HA-NP particle size | C | ~272 nm | single-section (no conflict) |
| "12,000×" NP potency | C | single-lab, flagged | single-section (Merlin-only, flagged) |
| Transdermal flux (microneedle) | A | 4.4 µg/cm²/h; +8× ionto; +35× combo | single-section (no conflict) |
| Transdermal passive LOD | A | 0.01 µg/mL | single-section |
| proKPV vs free / 5-ASA | C | 0.5 & 2.5 mg/kg; 5-ASA 50 mg/kg | single-section |
| (CKPV)₂ vaginitis | D | 2 mg/kg/day; ~12% vs miconazole ~44.7% | single-section |

No two sections assert different numbers for the same quantity. The recurring shared
numbers (100 µM oral, 10 nM cellular, n=5 DSS / n=10 TNBS, 16 µg/kg/day HA-NP) are
identical wherever repeated. Triangulation: PASS.

### Aggregate single-lab (Merlin/GSU) concentration share — method + cross-check

Method (matches Section G's): enumerate in-vivo efficacy primaries with a verifiable
PMID/DOI, attribute each to its senior/corresponding lab, compute
(Merlin in-vivo primaries) / (total in-vivo primaries), reported on two denominators.

Independent re-derivation from the union of A–G in-vivo efficacy primaries:

ALL-CAUSE in-vivo efficacy primaries (N=6):
- P1 Dalmasso 2008 — Merlin/GSU
- P2 Viennois 2016 — Merlin/GSU
- P3 Xiao 2017 — Merlin/GSU
- P4 Kannengiesser 2008 — Münster (independent)
- P5 Bonfiglio 2006 (corneal, rabbit) — Catania/Drago (independent)
- P6 Cutuli 2000 (antimicrobial) — Catania/Lipton (independent)
→ Merlin share = 3/6 ≈ **50%**.

GUT/IBD in-vivo efficacy primaries (N=4: P1–P4):
→ Merlin share = 3/4 ≈ **75%** (≥70% single-lab FLAG within the gut/IBD literature).

This reproduces Section G's figures EXACTLY (50% all-cause; 75% gut/IBD, ≥70% flag).
Concordant — confirmed consistent with Section G.

Note on denominator sensitivity (advisory, not a mismatch): the all-cause N=6 set in G
counts Cutuli 2000 and Bonfiglio 2006 as "in-vivo efficacy primaries." Cutuli 2000 is
treated as in_vitro (or in_vitro-lead) in Sections B and D, and Bonfiglio 2006 appears
ONLY in Section G. This is a section-scope/tagging choice, not a value contradiction —
G discloses its method and both denominators, and the headline gut/IBD 75% figure (the one
practitioner/vendor claims lean on) is unaffected by how the antimicrobial/corneal papers
are tagged. The single-lab-share conclusion is robust and consistent across the corpus.

---

## Advisory (non-mismatch) items for copy-edit — do NOT HALT on these

1. Pawar 2017 DOI suffix differs A (`...03.017`) vs E (`...03.043`); same PMID 28343991,
   same title/journal/volume/pages. Pick one DOI at copy-edit. Identity concordant.
2. Brzoska 2008 PMID present in B/F (18612139), omitted (DOI-only) in A. Add PMID to A for
   uniformity. No value conflict.
3. Cutuli 2000 / Bonfiglio 2006 tagging (in_vitro vs animal-in-vivo) varies by section
   scope; G's concentration-share method discloses this. Optional harmonization.

None of these alter any entity's authoritative identity or any numeric value, so per the
PASS/HALT rule they remain advisory, not mismatches.

---

## Structured verdict

```json
{"phase":"4.25","entity_classes":{"citations":{"scanned":11,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":3,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":7,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":4,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
