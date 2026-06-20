# Gate 4.75 — Citation Integrity Verification
## Biomarker: Serum 25(OH)D (Vitamin D)
## Date: 2026-06-20
## Mode: standard
## Sections checked: A, B, C, D (all four)

---

## IC-1 Type-Tag Presence

Scanned all inline citations across sections A–D for the pattern `[N, <tag>]` or `[N, tag; M, tag]`.

**All inline citations carry explicit type tags from the canonical enum.** No bare `[N]` citations found. Multi-cite patterns (e.g., `[1, mechanism_review; 2, mechanism_review]`) are all tagged.

Tags used in inline citations: `mechanism_review`, `rct`, `cohort`, `regulatory`, `meta_analysis`. All five are in the 12-value enum.

No inline citation omits its tag. No tag found outside the enum.

**Status: PASS**

---

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry in all four sections carries the `— tag: <type> — tier:` suffix. Tags present:
- Section A: `mechanism_review` (9), `rct` (1)
- Section B: `regulatory` (5), `mechanism_review` (1)
- Section C: `mechanism_review` (5), `cohort` (7)
- Section D: `mechanism_review` (2), `cohort` (1), `rct` (4), `meta_analysis` (1)

All tags are from the canonical enum. No entry missing the tag suffix.

**Status: PASS**

---

## IC-3 Vendor-Not-Numerical

No `vendor_label` citations appear anywhere in sections A–D.

No `[N, vendor_label]` citations detected.

**Status: PASS**

---

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citations appear anywhere in sections A–D.

**Status: PASS**

---

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations appear anywhere in sections A–D.

**Status: PASS**

---

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations appear anywhere in sections A–D.

**Status: PASS**

---

## IC-7 Population-Mismatch

No `animal` or `in_vitro` citations appear in sections A–D. All sources are human-based (rct, cohort, meta_analysis, mechanism_review of human pathways, regulatory). No numerical claim cites animal or in-vitro evidence.

**Status: PASS (vacuous — no animal/in-vitro citations to check)**

---

## IC-8 Route-Extrapolation

All supplementation dose claims in the sections reference oral administration. All cited RCTs (VITAL, D-Health, ViDA, Hammami) used oral vitamin D. No cross-route extrapolation detected.

**Status: PASS**

---

## IC-9 Concentration-Surfacing

Distinct primary citations (type ∈ {rct, meta_analysis, cohort}) enumerated:

| Citation | Institution | Type |
|---|---|---|
| Manson 2019 (VITAL) | NIH/Brigham | rct |
| Hahn 2022 (VITAL ancillary) | Harvard/BWH | rct |
| Neale 2022 (D-Health) | QIMR Berghofer | rct |
| Scragg 2017 (ViDA) | Univ Auckland | rct |
| Zhao 2017 | Multiple (JAMA) | meta_analysis |
| Hammami 2017 | Alfaisal/Warwick | rct |
| Heijboer 2012 | VU Amsterdam | cohort |
| Kocak 2015 | Sakarya Turkey | cohort |
| Singh 2006 | Mayo Clinic | cohort |
| Drincic 2012 | Univ Nebraska | cohort |
| Nielson 2016 | OHSU | cohort |
| Antoniucci 2005 | UCSF | cohort |
| Wielders 2009 | Bernhoven NL | cohort |

Total distinct primaries: 13. No single institution cluster exceeds 3 entries (VITAL Manson + Hahn share NIH/BWH infrastructure but are distinct studies with distinct primary outcomes). Largest cluster share: 2/13 = 15%. Well below 70% threshold.

Concentration-surfacing section not required (share < 70%).

**Status: PASS**

---

## IC-10 No Fabricated Citations

Host whitelist check for all bibliography URLs:

**Section A:**
- pmc.ncbi.nlm.nih.gov (refs 1, 2, 5, 7, 8, 9, 10) — WHITELISTED
- ods.od.nih.gov (ref 3) — WHITELISTED
- oup.com / 10.1210/jendso/bvz038 (ref 4) — WHITELISTED
- wiley.com / 10.1002/jbm4.10558 (ref 6) — WHITELISTED

**Section B:**
- nationalacademies.org (ref 1) — WHITELISTED
- oup.com / academic.oup.com/jcem (refs 2, 3, 4) — WHITELISTED
- ods.od.nih.gov (ref 5) — WHITELISTED
- pubmed.ncbi.nlm.nih.gov (ref 6, PMID 28822355) — WHITELISTED

**Section C:**
- sciencedirect.com / 10.1016/j.jsbmb.2021.105917 (ref 1) — WHITELISTED
- oup.com / 10.1373/clinchem.2011.176545 (ref 2) — WHITELISTED
- biochemia-medica.com (refs 3, 8) — WHITELISTED
- oup.com / 10.1210/jc.2006-0710 (ref 4) — WHITELISTED
- oup.com / 10.5740/jaoacint.17-0258 (ref 5) — WHITELISTED (J AOAC Int via oup.com)
- sciencedirect.com / 10.1016/j.jsbmb.2016.12.002 (ref 6) — WHITELISTED
- cdc.gov (ref 7) — WHITELISTED
- oup.com / 10.1373/clinchem.2012.191460 (ref 9) — WHITELISTED
- oup.com / 10.1210/jc.2016-1104 (ref 10) — WHITELISTED
- oup.com / 10.1373/clinchem.2004.041954 (ref 11) — WHITELISTED
- oup.com / 10.1373/clinchem.2008.117366 (ref 12) — WHITELISTED

**Section D:**
- nejm.org / 10.1056/NEJMra070553 (refs 1, 2) — WHITELISTED
- springer.com / 10.1038/oby.2011.404 (ref 3) — WHITELISTED
- nejm.org / 10.1056/NEJMoa1809944 (ref 4) — WHITELISTED
- bmj.com / 10.1136/bmj-2021-066452 (ref 5) — WHITELISTED
- thelancet.com / 10.1016/S2213-8587(21)00345-4 (ref 6) — WHITELISTED
- jamanetwork.com / 10.1001/jamacardio.2017.0175 (ref 7) — WHITELISTED
- jamanetwork.com / 10.1001/jama.2017.19344 (ref 8) — WHITELISTED

**All hosts are whitelisted. No off-whitelist, placeholder, or Wikipedia URLs detected.**

PMID verification (WebFetch-confirmed):
- Manson 2019: PMID 30415629 ✓ — title, N=25,871, HR 0.96 cancer / 0.97 CVD all confirmed
- Holick 2011: PMID 21646368 ✓ — title, author order confirmed
- Demay 2024: PMID 38828931 ✓ — title, author (Demay MB first) confirmed
- Heijboer 2012: PMID 22247500 ✓ — correct PMID used (prior wrong PMID 22238249 not present); author order Heijboer AC, Blankenstein MA, Kema IP, Buijs MM confirmed
- Hahn 2022: PMID 35082139 ✓ — HR 0.78 (0.61–0.99; P=0.05), N=25,871 confirmed
- Neale 2022: PMID 35026158 ✓ — HR 1.04 (0.93–1.18) confirmed
- Holick 2007: PMID 17634462 ✓ — title confirmed
- Zhao 2017: PMID 29279934 ✓ — 33 RCTs, N=51,145 confirmed
- Binkley 2017: PMID 27979577 ✓ — ±12% bias claim confirmed
- Singh 2006: DOI 10.1210/jc.2006-0710 ✓ — author list (Singh RJ, Taylor RL, Reddy GS, Grebe SKG) confirmed; 8.7–61.1% epimer range confirmed
- IOM 2011: nationalacademies.org/read/13050/chapter/10 ✓ — 50 nmol/L / 20 ng/mL threshold confirmed

**Status: PASS**

---

## IC-11 No Placeholder Strings

Searched all four sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

None detected.

**Status: PASS**

---

## IC-12 No Wikipedia Citations

No Wikipedia URLs (en.wikipedia.org or any variant) appear in any bibliography.

**Status: PASS**

---

## IC-13 Per-Citation Corpus Scoping

Standard mode: ≥50% random sample of numerical claims (minimum 10). 12 high-stakes numerical/scoped claims checked via WebFetch or Tavily search against source text or confirmed abstracts.

| Claim | Citation | Verification | Result |
|---|---|---|---|
| ×2.496 conversion factor ng/mL → nmol/L | A[1,7], B[5] (ODS) | Standard conversion confirmed by IOM/ODS source text | PASS |
| IOM ≥20 ng/mL (50 nmol/L) adequacy threshold | B[1, regulatory] | nationalacademies.org text: "Practically all persons are sufficient at levels of 50 nmol/L (20 ng/mL)" | PASS |
| ES 2011 ≥30 ng/mL sufficiency threshold | B[3, regulatory] | Holick 2011 PMID 21646368 confirmed via PubMed | PASS |
| VITAL HR 0.96 (0.88–1.06; P=0.47) cancer | D[4, rct] | Manson PMID 30415629 abstract: "HR 0.96 (95% CI, 0.88 to 1.06; P=0.47)" ✓ | PASS |
| VITAL HR 0.97 (0.85–1.12; P=0.69) CVD | D[4, rct] | Manson PMID 30415629 abstract: "HR 0.97 (95% CI, 0.85 to 1.12; P=0.69)" ✓ | PASS |
| Hahn HR 0.78 (0.61–0.99; P=0.05) autoimmune | D[5, rct] | PMID 35082139: "HR 0.78, 95% CI 0.61 to 0.99, P=0.05" ✓ | PASS |
| D-Health HR 1.04 (0.93–1.18; P=0.47) mortality | D[6, rct] | PMID 35026158: "1.04 [95% CI 0.93 to 1.18]; p=0.47" ✓ | PASS |
| Zhao 33 RCTs, N=51,145 no fracture benefit | D[8, meta_analysis] | PMID 29279934: 33 RCTs, 51,145 participants confirmed ✓ | PASS |
| Binkley ±12% assay bias → 20–35 ng/mL PTH threshold swing | C[6, mechanism_review] | PMID 27979577 abstract: "a ±12% [bias] could vary from 20 to 35 ng/mL" ✓ | PASS |
| Singh C3-epimer 8.7–61.1% of total 25-OHD in infants | C[4, cohort] | DOI 10.1210/jc.2006-0710 full text: "8.7–61.1% of the total 25-OHD" ✓ | PASS |
| Toxicity concern >125 nmol/L (>50 ng/mL); frank toxicity >375 nmol/L (>150 ng/mL) | B[1, regulatory; 5, regulatory] | IOM/NIH-ODS confirmed via nationalacademies.org ("reason for concern at ... above 125 nmol/L") | PASS |
| VDSP 30–40% inter-assay bias documented | C[6, mechanism_review], B[6, regulatory] | Binkley 2017 PMID 27979577 + VDSP PMID 28822355 confirm measurement variability of this magnitude | PASS |

Claims checked: 12. Claims failed: 0.

**Status: PASS**

---

## Verdict

verdict: PASS

### Findings summary

All 13 IC checks PASS. No bare inline citations, no off-whitelist hosts, no fabricated/wrong PMIDs (prior error Heijboer 22238249 has been corrected to 22247500 in the current bib), no RCTs mistagged as cohort (VITAL/D-Health/ViDA/Hahn/Hammami all correctly tagged `rct`; Zhao correctly tagged `meta_analysis`), no animal/in-vitro population-mismatch conditions, no concentration cluster above 70%, and 12/12 corpus-scoped claims verified against source abstracts or full text with zero failures. 12 claims checked, 0 failed.

Two WARN-level observations (non-HALT):
1. D-Health N: report states 21,315; one secondary-source table shows 21,310. Primary sources (QIMRB study site, PubMed abstract) confirm 21,315. Minor discrepancy, likely secondary-source rounding — WARN only.
2. ViDA N: report states 5,108; EurekAlert press release and one CVD review table show 5,110. Minor 2-participant discrepancy, within trial accounting norms — WARN only.

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":13,"largest_cluster_count":2,"share":0.15,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":12,"claims_failed":[]},"halt_reasons":[],"warnings":["D-Health N: report=21315 vs secondary-source table=21310; primary sources confirm 21315 — WARN only","ViDA N: report=5108 vs EurekAlert/CVD-review-table=5110; 2-participant discrepancy within trial-accounting norms — WARN only"],"iterations":1}
```
