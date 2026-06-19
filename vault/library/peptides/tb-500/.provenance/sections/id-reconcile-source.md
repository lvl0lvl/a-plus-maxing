# Phase 4.25 ID-Reconcile — TB-500 (iteration 2)

## Verdict

verdict: PASS   (no remaining mismatches)

All 3 hard cross-section mismatches and the 2 softer items (full-length Tβ4 MW; intra-E phase label) flagged in iteration 1 are confirmed RESOLVED. A fresh scan of the 5 shared-entity classes across sections A–G surfaced NO new cross-section numerical/identity contradiction. The only residual occurrences of the OLD divergent values are inside the sections' own `## Post-fix grep audit` blocks (qualified negations / OLD→NEW edit ledgers), which are out of scope for live-content checks per the task.

## Per-class findings

| Entity class | scanned | mismatch_count | remaining mismatches |
|---|---|---|---|
| citations | 8 | 0 | (none) |
| institutions | 4 | 0 | (none) |
| compound_identifiers | 5 | 0 | (none) |
| regulatory_dates | 3 | 0 | (none) |
| trial_registrations | 5 | 0 | (none) |

No remaining-mismatch table is required — every class is clean.

**Scan detail (what was triangulated):**

- **citations** (8 shared records re-checked): PMID 36613994 (Sosne NK Ph III) — E[5]+E-table line 46 and F[2] both `Int J Mol Sci 2023;24(1):554`, DOI 10.3390/ijms24010554 ✓; PMID 17495250 (Guarnera 2007) — A[6] and E[13] both `Ann N Y Acad Sci 2007;1112:407-412`, DOI 10.1196/annals.1415.003 ✓; PMID 20536470 (Guarnera 2010) — E[12] `Ann N Y Acad Sci 2010;1194:207-212` ✓; PMID 34346165 (Wang/NL005 2021) — A[9], E[17], F[1] all `J Cell Mol Med 2021;25(17):8222-8228` ✓ (A tags it `open_label`, E/F tag `rct`; this is an explicitly-disclosed framing choice in A's note, not an identity/numeric conflict); PMID 22962027 (Esposito 2012) — A[2] and G[19] both `Drug Testing and Analysis 2012`, DOI 10.1002/dta.1402 ✓; PMID 15565145 (Bock-Marquette Nature 2004) — B[13] and G[4] both `Nature 2004;432(7016):466-72`, DOI 10.1038/nature03000 ✓; Smart/Riley Nature 2007 — D[1] and G[6] both `Nature 2007;445:177-182`, DOI 10.1038/nature05383 ✓; PMID 10469335 (Malinda 1999) — B[3] and C[5] both `J Invest Dermatol 1999;113(3):364-8` ✓.
- **institutions** (4): Goldstein/RegeneRx COI nexus (C, D, E, G) — concordant; Chopp/Henry Ford neuro cluster (D) — internal-consistent; Riley/Smart — D says "UCL / UCL Institute of Child Health" and "UCL/Oxford"; G says "Oxford" in the cluster header and "UK (Riley) group" in the bib. This is a minor narrative descriptor variance (Riley's lab is associated with both UCL and Oxford over time) — all the load-bearing identity data (PMID/DOI/vol/pages/"independent UK group") agree, so it is NOT scored as a reconcilable-class mismatch; noted for awareness only. ReGenTree/Northland/Hudson Biotech sponsors (E, F, G) — concordant.
- **compound_identifiers** (5): full-length Tβ4 MW — A canonicalizes `~4,963 Da (average, acetylated; UniProt P62328 / Kelleher 4,963.50)`, G uses `~4963 Da` / `4963.49 g/mol` — now MATCHED ✓ (A's 4,982 and 4,921 appear only inside the explicit three-value convention map, correctly attributed; G has 0 occurrences of 4,982); CAS 77591-33-4 (A, G) ✓; Ac-LKKTETQ 17–23 fragment identity (A, C, D, G) ✓; molecular formula C212H350N56O78S (A) — internal; sequence 43-aa Ac-SDKP… (A) — internal.
- **regulatory_dates** (3): FDA 503A status — F and G both state placed on interim Cat-2 Sept 2023, **REMOVED from Cat-2 April 2026** (FR doc 2026-07361), still non-compoundable, PCAC July 23–24 2026 for possible Category-1 — MATCHED ✓; WADA S2.3 prohibited-at-all-times, 2026 list valid 1 Jan 2026 (F) — internal-consistent; no other cross-section regulatory date in conflict.
- **trial_registrations** (5): NCT00743769 = Phase 1, Withdrawn n=0 — E table + E[15] agree; header/gap now say "RGN-352 records (one Phase 1, one Phase 2)" — MATCHED ✓; NCT01311518 = Phase 2, Withdrawn n=0 (E, F, G) ✓; NCT02600429/SEER-1 Phase 3, n=18, Terminated, p=0.0656 (E, F) ✓; NCT04555824/NCT04555850 (NL005 Ph1, n=54/30) (A, E) ✓; NCT07487363 (Hudson TB-500 fragment, Ph1/2, recruiting) (E) — internal.

## Resolution confirmation (the 5 prior items)

1. **FDA 503A status (G matches F) — RESOLVED.** Both F (Claim 11, line 21; table line 44; gap line 100) and G (line 34; ref [12] line 74; gap #2/#7; reconciliation block) state REMOVED from interim Category 2 ~April 2026, Cat-2 since Sept 2023, still non-compoundable, PCAC July 23–24 2026 for Category-1. No live assertion that TB-500 is currently on Cat-2; "churning" survives only inside G's qualified reconciliation note.
2. **PMID 36613994 year (2023 in E and F) — RESOLVED.** E[5] and F[2] both read `Int J Mol Sci 2023;24(1):554`. No live `2022` attached to this citation in either section (F has 0 `2022` hits; E's only `2022` is the unrelated NCT05984134 registry span).
3. **PMID 17495250 journal (Ann N Y Acad Sci in A and E) — RESOLVED.** A[6] and E[13] both `Ann N Y Acad Sci 2007;1112:407-412`, DOI 10.1196/annals.1415.003. The only `Int Angiol` string in E is the qualified negation "NOT Int Angiol" in [13]'s note.
4. **Full-length Tβ4 MW (~4,963 Da canonical in A and G) — RESOLVED.** A Claim 1 canonicalizes ~4,963 Da (UniProt P62328); G uses ~4963 Da / 4963.49 g/mol. The 4,982/4,921 values in A appear only as the documented convention map (original-1982-paper figure and unmodified-peptide figure, both correctly attributed); G has zero `4,982` occurrences.
5. **NCT00743769 phase (Phase 1, intra-E) — RESOLVED.** E table line 53 and bib [15] list it Phase 1; Claim 10 header and coverage-gap #3 now read "RGN-352 records (one Phase 1, one Phase 2)" / explicitly tag NCT00743769 as Phase 1. `phase 2 record` → 0 live hits.

**New cross-section contradiction check:** none found. Re-triangulated SEER-1 numbers (n=18, 60% vs 12.5%, p=0.0656), ARISE n=317/601/700, the 317-subject figure echoed in F's pooled ~425-subject statement, NL005 SAD/MAD n=54/30, Malinda re-epithelialization 42%/61%, and the Cha melanoma (46.7 vs 10.9) / Caers myeloma figures — all internally and cross-sectionally consistent. The Riley UCL-vs-Oxford descriptor is the only divergence observed and is a non-scoring narrative variance (identity fields concordant).

## Structured verdict

```json
{"phase":"4.25","entity_classes":{"citations":{"scanned":8,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":4,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":5,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":3,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":5,"mismatch_count":0,"mismatches":[]}},"iterations":2,"halt_reasons":[]}
```
