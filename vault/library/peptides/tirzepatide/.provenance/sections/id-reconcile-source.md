# Phase 4.25 — ID-RECONCILE (cross-section consistency)

Report: Tirzepatide. Sections audited: A, B, C, D, E, F.
Method: For each entity class, identified entities appearing in >1 section and verified agreement. A fact present in only one section is NOT treated as a mismatch. Only genuine cross-section disagreements are flagged.

## Citations (PMID → author / year / journal / trial)

Shared citations appearing across sections all agree:

- **SURMOUNT-1 — Jastreboff, 2022, NEJM, PMID 35658024.** Asserted in B[1] (Jastreboff AM, 2022, NEJM, PMID 35658024). Referenced descriptively in C and D ("SURMOUNT-1 body-composition substudy") without a conflicting PMID. No disagreement.
- **SURPASS-2 — Frías, 2021, NEJM, PMID 34170647.** B[2] (Frías JP, 2021, NEJM, PMID 34170647). Cross-referenced in A's narrative (vs semaglutide) without a conflicting attribution. Consistent.
- **SURMOUNT-OSA — Malhotra, 2024, NEJM, PMID 38912654.** C[1] (Malhotra A, 2024, NEJM, PMID 38912654). C prose says "2024" / bibliography "2024 Oct 3" — same year, not a mismatch. Referenced in E (SURMOUNT-OSA program) with no conflicting PMID. Consistent.
- **SURMOUNT-4 — Aronne, 2024, JAMA, PMID 38078870.** Cited in BOTH B[9] (Aronne LJ, 2024, JAMA, PMID 38078870) and D[3] (Aronne LJ, JAMA 2024, PMID 38078870, DOI 10.1001/jama.2023.24945). Same author, year, journal, and PMID in both sections. Consistent — this is the strongest cross-section citation match.
- **FDA labels (setids).** Mounjaro setid d2d7da5d-ad07-4228-955f-cf7e355c8cc0 appears in D[1] and F[1] — identical. Zepbound setid 487cd7e7-434c-4925-99fa-aa80b1cc776b appears in D[2], E[6], and F[2]/F[3] — identical across all three sections. Consistent.

No PMID is mapped to two different author/year/title pairs anywhere. Scanned: 5 shared-citation entities.

## Institutions / sponsor

**Eli Lilly** is the named manufacturer/sponsor in A (marketed by Eli Lilly as Mounjaro/Zepbound), C (every pivotal trial explicitly tagged "sponsor: Eli Lilly"; dulaglutide noted as also a Lilly product), D (marketed as Mounjaro/Zepbound), E (marketed by Eli Lilly; Lilly investor releases; LillyDirect), and F (LillyDirect pricing). No competing manufacturer attribution. Scanned: 1 entity. Consistent.

## Compound identifiers

- **Dual GIP + GLP-1 receptor agonist** ("twincretin"): stated in A, B, C, D, E, F. Uniform.
- **Once-weekly subcutaneous**: A, B, D, E, F. Uniform. (C does not restate dosing frequency; not a mismatch.)
- **39-amino-acid peptide** and **~5-day (≈5.4 d) elimination half-life**: stated only in A. Single-section facts → not cross-section mismatches.
- **Not conflated with semaglutide**: A explicitly distinguishes tirzepatide (dual GIP+GLP-1) from semaglutide (GLP-1-only); B treats SURPASS-2 as tirzepatide vs semaglutide 1 mg and flags the indirect-comparison caveat. No section treats tirzepatide as GLP-1-only or as a semaglutide co-formulation. Consistent.
- **Brand → indication split**: Mounjaro = type 2 diabetes; Zepbound = obesity/chronic weight management + OSA. Stated consistently in D, E, and F. E adds the explicit "same molecule, two NDAs" framing; F and D align. No section reverses the brand/indication mapping. Consistent.

Scanned: 4 shared compound-identifier entities (dual-agonist class; dosing route/frequency; semaglutide non-conflation; brand→indication mapping).

## Regulatory dates / facts

- **Mounjaro T2D approval 2022**: D ("U.S. approval 2022"), E ("May 13, 2022"), F (implicit; label "Initial U.S. Approval 2022" via E[6]). Consistent.
- **Zepbound obesity approval Nov 2023**: E ("November 8, 2023"). Not contradicted elsewhere. Consistent.
- **Zepbound OSA approval Dec 2024**: C ("December 2024"), E ("December 20, 2024"), F (OSA indication present). C's "December 2024" and E's "December 20, 2024" agree (same month/year). Consistent.
- **Shortage resolved 2024**: E (FDA removed from shortage list Oct 3 2024; reaffirmed Dec 19 2024) and F (Dec 19 2024 determination; 503A 60-day to ~Feb 18 2025; 503B 90-day to ~Mar 19 2025). E and F agree on dates and wind-down windows. Consistent.
- **WADA — NOT prohibited; 2026 Monitoring Program**: stated in E only. A and C do not address WADA/sport status (the task anticipated possible A/C/E spread, but only E carries it). A single-section fact is not a mismatch; no contradicting sport-status claim exists in A or C. Consistent (no disagreement).
- **OSA dose = 10/15 mg only** (2.5 mg not approved for OSA): C (10–15 mg), E (10/15 mg, lowest dose not approved for OSA), F (10 or 15 mg for OSA). Consistent.

Scanned: 6 shared regulatory-fact entities.

## Trial registrations / efficacy figures / doses

(Reported under trial_registrations in the JSON block; covers efficacy magnitudes, population labels, and dose ladder — the cross-section trial-anchored facts.)

- **SURMOUNT-1 −20.9% at 15 mg, NON-DIABETIC obesity**: B states −20.9% (15 mg) in "obesity but WITHOUT diabetes." A and D reference SURMOUNT-1 (mechanism / body-composition) without contradicting the magnitude or population. No conflation with the T2D population. Consistent.
- **SURPASS-2 superiority vs semaglutide 1 mg**: B states all three tirzepatide doses noninferior and SUPERIOR to semaglutide 1 mg on HbA1c. A's narrative agrees tirzepatide adds GIPR engagement beyond GLP-1-only semaglutide. No section claims semaglutide superiority or equivalence. Consistent.
- **SURMOUNT-OSA AHI reduction**: C states AHI fell ~20–24 events/hr more than placebo (Trial 1 −20.0; Trial 2 −23.8). E describes "statistically significant reductions in AHI versus placebo" without a conflicting number. Consistent.
- **SURMOUNT-4 regain +14% / lead-in −20.9%**: B (lead-in mean −20.9%; placebo-switch REGAINED +14.0%; continued −5.5%; between-group −19.4%; 89.5% vs 16.6% maintained ≥80%) and D (regained 14.0%; continued lost additional 5.5%; −19.4% [95% CI −21.2 to −17.7]; total 25.3% vs 9.9%; 89.5% vs 16.6%) match on every shared figure. Consistent.
- **Population labels NOT conflated**: B carefully separates SURPASS (T2D, glycemic), SURMOUNT-1 (obesity, non-diabetic, −20.9%), and SURMOUNT-2 (obesity + T2D, −14.7%), and explicitly attributes the SURMOUNT-1 vs SURMOUNT-2 gap to a population effect, not a dose difference. No other section asserts a figure under the wrong population. Consistent — no population conflation detected.
- **Dose ladder / titration 2.5 → 15 mg**: D (start 2.5 mg, 2.5-mg steps no faster than q4wk), E (maintenance 5/10/15 weight; 10/15 OSA), F (full ladder 2.5→5→7.5→10→12.5→15; max 15; pediatric T2D max 10). B's maintenance doses (5/10/15) sit on the same ladder. All agree; no dose/date mismatch. Consistent.

Scanned: 6 shared trial-anchored / efficacy / dose entities.

## Verdict

verdict: PASS

No genuine cross-section disagreement was found in any entity class. Shared PMIDs map to a single author/year/title each (notably SURMOUNT-4 PMID 38078870 in both B and D, and the two FDA label setids across D/E/F); Eli Lilly is the uniform sponsor; the dual GIP+GLP-1 / once-weekly-SC / brand→indication identifiers are uniform and not conflated with semaglutide; regulatory dates (Mounjaro 2022, Zepbound 2023, OSA Dec 2024, shortage resolved 2024, WADA not-prohibited/2026-monitoring) agree wherever they co-occur; and the efficacy figures and 2.5→15 mg dose ladder agree across sections with no population conflation.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":5,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":1,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":4,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":6,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
