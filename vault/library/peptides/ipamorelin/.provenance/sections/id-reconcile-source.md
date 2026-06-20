# Phase 4.25 ID-Reconcile + Triangulation — Ipamorelin

## Verdict
verdict: PASS

All shared entities across the 6 section drafts are concordant. Zero cross-section value disagreements found in any of the 5 entity classes. The two flagged risk areas (the Apr-2026 12-peptide list MK-677↔PEG-MGF, and ipamorelin's own E↔F regulatory status) are clean. Numerical triangulation matches across sections and the aggregate Novo Nordisk concentration share independently recomputes to F's ~80%.

(Note: per instructions, Section E's `## Post-fix grep audit` block was excluded from live-content cross-checks; it was read only to confirm the live body of E already carries the corrected PEG-MGF value.)

## Per-class findings (scanned + mismatch count per class)

### citations — scanned 5 shared papers; 0 mismatches
- **Raun 1998** (foundational): PMID 9849822, Eur J Endocrinol 1998;139(5):552-561, DOI 10.1530/eje.0.1390552 — identical in A[1], B[1], C[1], F[1]. ✓
- **Gobburu 1999** (human PK/PD): PMID 10496658, Pharm Res 1999;16(9):1412-1416, DOI 10.1023/A:1018955126402 — identical in A[4], B[2], D[2]. ✓
- **Beck 2014** (POI RCT): PMID 25331030, Int J Colorectal Dis 2014;29(12):1527-34, DOI 10.1007/s00384-014-2030-8, NCT00672074 — identical in D[1], E[1], F[5]. ✓
- **Svensson 2000** (BMC): PMID 10828840, J Endocrinol 2000;165(3):569(-77), DOI 10.1677/joe.0.1650569 — C[2] and F[3] concordant (F omits PMID/DOI but no conflicting value). ✓
- **Johansen 1999** (longitudinal bone growth): PMID 10373343, Growth Horm IGF Res 1999;9(2):106-13, DOI 10.1054/ghir.1999.9998 — C[3] and F[2] concordant, both Johansen PB et al. ✓
- Disambiguation confirmed OK: the *other* Johansen paper (A[10], Johansen PB 1998, Xenobiotica, PMID 9879640, nasal-absorption PK) is a DISTINCT paper from Johansen 1999 above — correctly kept separate; A explicitly resolved an "Agersø vs Johansen" first-author discrepancy in favor of PubMed. No collision.

### institutions — scanned 4 shared entities; 0 mismatches
- **Novo Nordisk** (originator; Måløv, DK) — consistent in A, C, D, F (and implied B). ✓
- **Helsinn Therapeutics** (clinical sponsor, POI) — consistent in C, D, F. ✓
- **Aarhus University** (Flyvbjerg/Ørskov/Andreassen) — consistent in C, F. ✓
- **Gothenburg/Göteborg University** (Svensson/Jansson/Ohlsson bone group) — C "Univ. of Gothenburg/Sahlgrenska," F "Göteborg University." English vs Swedish name for the same institution; NOT a divergence. ✓

### compound_identifiers — scanned 5; 0 substantive mismatches
- **Sequence** Aib-His-D-2-Nal-D-Phe-Lys-NH2 — identical in A, B, C, F. ✓
- **Molecular formula** C38H49N9O5 — identical in A, F. ✓
- **CAS** 170851-70-4 — identical in A, D, F. ✓
- **Dev code** NNC 26-0161 — identical in A, D. ✓
- **Average MW**: A=711.9 (PubChem), C=711.85 (used for mg/kg↔µmol/kg dose math), F=711.86 (vendor label). All three are the same compound's average MW differing only by source/rounding (range 711.85–711.9; spread <0.05 g/mol, ~0.007%). Within rounding tolerance; not a value disagreement. ✓

### regulatory_dates — scanned 6; 0 mismatches
- **PCAC meeting Oct 29 2024** (FDA recommended against; committee voted NOT to add ipamorelin acetate+free base to 503A bulks) — E and F agree exactly. ✓
- **Removed from interim Cat-2 ~Sept 27 2024** — E states it explicitly; F refers to the "2024 FDA action"/delisting (less specific, not contradictory). ✓
- **Apr-2026 FR action (FR Doc 2026-07361, 91 FR 20465, Apr 16 2026) excludes ipamorelin** — asserted in E; F does not contradict (F never claims ipamorelin is in any Apr-2026 list). ✓
- **12-peptide list = PEG-MGF, NOT MK-677** — E's live body (line 32) carries the corrected PEG-MGF version. **F never enumerates the 12-peptide list at all**, so there is NO conflicting MK-677 version in F. Special-attention check: CLEAN. ✓
- **July 23–24 2026 PCAC follow-on meeting** — E and F agree on the date. (Minor framing nuance: E ties it to the Apr-2026 12-peptide action; F ties it to Evexias/Farmakeio Category-2 litigation — same scheduled meeting date, no contradictory fact about ipamorelin; not a mismatch.) ✓
- **WADA S2.2 — PROHIBITED AT ALL TIMES, non-specified** — stated in E[8]; not contradicted by any section. ✓
- **Ipamorelin's own status E↔F** (never FDA-approved; removed from Cat-2; PCAC-rejected; not on 503A bulks list; not part of Apr-2026 action) — fully concordant. Special-attention check: CLEAN. ✓

### trial_registrations — scanned 2; 0 mismatches
- **NCT00672074** (Beck 2014 "Ipamorelin 201"; Phase II; Helsinn; n=117 enrolled / 114 safety-mITT; quadruple-blind; primary endpoint NOT met; Completed Dec 2009) — D (n=117 enrolled, 114 mITT), E (n=114 safety/mITT — the safety-analysis subset, consistent), F (n=117 enrolled/114 mITT) all concordant; the 117/114 distinction is enrolled-vs-mITT, used correctly in every section. ✓
- **NCT01280344** (Phase II; Helsinn; n=320; 4 arms incl. 0.03/0.06 mg/kg BID + 0.06 TID + placebo; no posted results; discontinued) — D primary, F context; phase/n/sponsor/status concordant. ✓

## Triangulation (numerical concordance; aggregate concentration share + method)

Numerical claims appearing in 2+ sections all match:
- **Human terminal t½ ~2 h (IV)** — A, B, D identical. ✓
- **Clearance 0.078 L/h/kg; Vss 0.22 L/kg; SC50 214 nmol/L; max GH rate 694 mIU/L/h; GH peak ~0.67 h; n=40 (8/dose × 5); dose range 4.21–140.45 nmol/kg** — A, B, D all identical. ✓
- **Selectivity** (no ACTH/cortisol/prolactin/FSH/LH/TSH co-release even at ~200-fold / ~200× the GH ED50) — A, B, C concordant on the "200" multiple. ✓
- **In-vitro EC50 1.3 ± 0.4 nmol/L; Emax 85 ± 5%** — A, B, C identical. ✓
- **Rat in-vivo ED50 80 ± 42 nmol/kg; Emax 1545 ± 250 ng/mL** — A, B, C identical. ✓
- **Swine ED50 2.3 (± 0.03) nmol/kg; Emax 65 ± 0.2 ng/mL** — A, B, C, F concordant. ✓
- **Beck n=114/117 + primary-endpoint FAILED** — D, E, F concordant (F adds 25.3h vs 32.6h, p=0.15; not contradicted elsewhere). ✓
- **MW ~711.9** — see compound_identifiers (711.85–711.9, rounding-equivalent). ✓

**Aggregate single-lab (Novo Nordisk) concentration share — independent recompute:**
Method: enumerate the in-vivo efficacy primaries (animal anabolic/bone + the human efficacy RCT) cited across the corpus, then classify each by originating-lab lineage. Union set = {Raun 1998 (Novo, all authors), Johansen 1999 (Novo+Aarhus), Svensson 2000 (Göteborg+Novo, Novo-supplied compound), glucocorticoid/bone 2001 (Novo-supplied compound), Beck 2014 (Helsinn, independent licensee — FAILED)}. Novo-Nordisk-lineage = 4 of 5 = **80%**. The Venkova gut-motility papers (C[4], C[5]) are GI-functional, outside the GH/bone anabolic-efficacy audit scope; adding them would not drop the share below the ≥70% single-lineage flag. **Aggregate share = ~80%, matching Section F exactly; ≥70% single-lineage-dominance flag confirmed.** ✓

## Structured verdict
```json
{"phase":"4.25","entity_classes":{"citations":{"scanned":5,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":4,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":5,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":2,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
