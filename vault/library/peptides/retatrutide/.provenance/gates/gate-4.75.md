# Gate 4.75 — Citation-Integrity Verifier — Retatrutide (LY3437943)

Phase 4.75 mechanical citation-integrity pass over the six-section corpus
(`section-A.md`…`section-F.md`) plus the Phase-2.5 rubric. Calibration: HALT only
on genuine integrity violations; paywall / bot-block / honest gaps = WARN.

---

## IC-1 Type-Tag Presence

Every inline citation carries a type-tag from the canonical enum. Two tag dialects
are used and both resolve to enum values:
- bracketed backtick form `` `[rct]` `` / `` `[regulatory]` `` / `` `[mechanism_review]` `` / `` `[animal]` `` / `` `[anecdote_aggregate]` ``
- inline `[type: rct]` / `[type: rct/PK-PD]` / `[type: rct, cross-trial/indirect]` / `[type: regulatory]`

Tally of distinct inline tags: `rct` (28 bracket + 12 `[type:rct]` + 3 `rct/PK-PD` + 1 cross-trial), `regulatory` (49), `mechanism_review` (23), `animal` (1), `anecdote_aggregate` (1). No tag token outside the enum was found (`vendor_label` and `practitioner_protocol` appear only as italic parenthetical annotations in §F, not as the formal cite-tag — see IC-3/IC-5). **PASS.**

## IC-2 Bibliography Type-Tag Presence

All six section bibliographies annotate every entry. §A uses combined tags where an entry serves two roles (Coskun `mechanism_review / animal`). §D entries [5]/[6] carry `anecdote_aggregate` / `mechanism_review`. §E/§F entries use `[regulatory]` / journalistic-context / `vendor_label` / `practitioner_protocol` / secondary annotations. Every entry has at least one enum tag or an explicit admissibility annotation. **PASS.**

## IC-3 Vendor-Not-Numerical

`vendor_label` appears only in §F (lines 20, 21, 23, 26), all in gray-market access context. Mechanically checked each sentence for efficacy/AE/dose numerical tokens (µg/kg, mg/kg, %reduction, fold, p-values): **none present**. The only number near a vendor cite is the `$100M+` market-scale figure (journalistic-context, not efficacy/AE/dose) and "far cheaper per milligram" (qualitative, no value). No vendor cite grounds a therapeutic number. **PASS.**

## IC-4 Anecdote-Not-Numerical

One `anecdote_aggregate` cite: §D [5] (SeekPeptides clinical-data summary). It appears in the §D line-21 heart-rate sentence alongside a numerical effect-size magnitude — "secondary clinical summaries… place the mean peak increase at roughly **5–10 bpm**, with the largest mean rise (~6–7 bpm) in the 12-mg group at week 24 [5]." This is a numerical effect-size token co-located with an `anecdote_aggregate` cite, which IC-4 nominally restricts.

Mitigating facts (why WARN, not HALT): (a) the load-bearing claim — the dose-dependent pattern and week-24 peak — is sourced to [1] (the RCT) in the same and preceding sentence; (b) [5] grounds only a contextual *magnitude estimate* (a mean change, not an AE *rate*), explicitly framed as "secondary clinical summaries… roughly"; (c) the §D bibliography states [5] is "not used to ground any AE rate." Per the genuine-violation calibration this is an honestly-subordinated secondary magnitude, not a fabricated/anecdote-grounded AE rate. **WARN** (recommend either dropping the bpm figure or re-grounding to [1]'s reported HR data). Not a HALT.

## IC-5 Practitioner-Protocol-Not-Efficacy

One `practitioner_protocol` cite: §F [6] (Hormachea RD blog). It grounds only qualitative no-standardized-dosing / no-oversight / no-supervision claims and advice to steer to approved therapy — no effect size, response rate, or mechanism. The annotation explicitly labels it "opinion/advice, not an efficacy/safety dataset." No efficacy claim rests on it. **PASS.**

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` cite exists in the corpus (consistent with §F's finding that there is no approved product and therefore no legitimate compounding pathway / data sheet). Vacuously **PASS.**

## IC-7 Population-Mismatch

One `animal`-tagged inline cite: §A line 29, the Coskun obese-mouse quote ("Body weight loss was augmented by GCGR-mediated increases in energy expenditure…"). Mechanical scan of that sentence for a numerical token (dose/effect-size/n/%/fold) returned **none** — it is a qualitative mechanism statement, and the species ("obese mice"; "mouse; diet-induced-obese models") is the explicit subject within the sentence. Override per health-gates §1 applies; `[population-mismatch]` not required. All quantitative efficacy/AE figures elsewhere are grounded in human RCT sources (`rct`), correctly. **PASS.** (See `population_mismatch` block.)

## IC-8 Route-Extrapolation

Every dose/administration claim specifies subcutaneous once-weekly (10× "once-weekly", 3× "once weekly", 6× "subcutaneous", 1× "SC"). The cited primaries (Jastreboff, Rosenstock, Sanyal, Urva) are all SC-weekly trials; claim route matches source route. No oral/IM/IV/intranasal route appears, so no cross-route extrapolation exists. No `[route-extrapolation]` tag needed. **PASS.**

## IC-9 Concentration-Surfacing

Single-sponsor share = 100% (≥70% threshold triggered). The corpus surfaces this as a first-class, explicitly-headed subsection — §C "### Concentration / sponsor audit" — opening "This is the defining integrity feature of the retatrutide evidence base and must be stated plainly… Sponsor concentration: 100% Eli Lilly and Company… zero independent-sponsor replication." It is not buried in a bibliography. The §C section title itself names "concentration audit," and the investigational/single-sponsor frame is repeated in every section header banner. Surfaced as required. **PASS.** (See `concentration_audit` block.)

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a same-section bibliography entry (checked §A–§F; numbering is per-section, internally consistent). Load-bearing PMIDs spot-verified live via NCBI E-utilities — all 8 resolve with matching first-author + title + journal + year:

| PMID | Cited as | E-utilities result | Match |
|------|----------|--------------------|-------|
| 37366315 | Jastreboff 2023 NEJM | Jastreboff AM, NEJM, 2023 Aug 10 | ✓ |
| 37385280 | Rosenstock 2023 Lancet | Rosenstock J, Lancet, 2023 Aug 12 | ✓ |
| 38858523 | Sanyal 2024 Nat Med | Sanyal AJ, Nat Med, 2024 Jul | ✓ |
| 35985340 | Coskun 2022 Cell Metab | Coskun T, Cell Metab, 2022 Sep 6 | ✓ |
| 36354040 | Urva 2022 Lancet | Urva S, Lancet, 2022 Nov 26 | ✓ |
| 39019866 | Li/Wang 2024 Cell Discov | Li W, Cell Discov, 2024 Jul 17 | ✓ |
| 40630318 | Heerspink 2025 Kidney Int Rep | Heerspink HJL, Kidney Int Rep, 2025 Jun | ✓ |
| 41090431 | Giblin TRIUMPH design 2026 DOM | Giblin K, Diabetes Obes Metab, 2026 | ✓ |

URL HEAD-checks: PMC11271400, ClinicalTrials.gov (NCT05929066, NCT06383390), lilly.com, fda.gov drug-alert all returned **200**. drugs.com returned **403** (bot-block — corpus-missing WARN, not a dead/fabricated link; the §F [4] claims are journalistic-context, not load-bearing numerals). **PASS** (one bot-block noted as WARN).

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, "according to some reports", "research suggests", "experts believe" → **zero matches** across all six sections. **PASS.**

## IC-12 No Wikipedia Citations

Grep for `wikipedia` (any subdomain) across the entire corpus → **zero matches**. No Wikipedia URL in any bibliography or inline. **PASS.** (Rubric self-check #6 satisfied.)

## IC-13 Per-Citation Corpus Scoping

Deep-mode sample: load-bearing numerical claims grep-verified against retrieved primary text (PubMed efetch abstracts). All checked numbers matched the source exactly:
- **Jastreboff 2023 [obesity]:** 24-wk −7.2/−12.9/−17.3/−17.5/−1.6%; 48-wk −8.7/−17.1/−22.8/−24.2/−2.1%; responder 92/75/60, 100/91/75, 100/93/83; N=338; 51.8% men; BMI 27–<30 — **all verbatim-confirmed** in abstract.
- **Sanyal 2024 [MASLD]:** LF −42.9/−57.0/−81.4/−82.4/+0.3% (P<0.001); normal-LF 27/52/79/86%; n=98 — **confirmed.**
- **Rosenstock 2023 [T2D]:** HbA1c −0.43%…−2.02%; dulaglutide −1.41%; weight −16.94%/−16.34%; N=281; no severe hypoglycemia, no deaths — **confirmed.**
- **Heerspink 2025 [kidney]:** eGFR +5.3 (CI 1.9–8.7) and +8.5 (CI 4.9–12.1); UACR −37.0% (36 wk / T2D) and −31.5% (48 wk / obesity) — **confirmed** (the report's population/timepoint mapping matches the abstract exactly).

corpus-missing (WARN, not HALT): drugs.com §F[4] (403 bot-block); Rosenstock §D[2] full text paywalled (but abstract-verified for the numbers used); PR-Newswire toplines (§C[5][6]) and WADA PDFs / practitioner blog not re-fetched — those numbers are either honestly labeled press-release-not-verified or non-numerical regulatory facts, so no numerical claim is left ungrounded. **PASS** (corpus gaps are paywall/bot-block only). (See `corpus_scoping` block.)

---

## Investigational-Discipline Confirmation (CRITICAL for this entry)

- **NOT approved:** every section banner states investigational/not-approved (investigational keyword 1/5/4/3/5/5 across A–F; "not approved" explicit in A/B/E, with E §"NOT APPROVED anywhere"). §E enumerates FDA/EMA/other = not approved, no marketed product. Held.
- **TRIUMPH topline = press-release / not peer-reviewed, NOT treated as verified efficacy:** §B excludes the TRIUMPH-1 topline from grounding numbers ("press-release topline data are NOT a Tier-1 admissible source"); §C labels both TRIUMPH-1 (28.3%/12 mg) and TRIUMPH-4 toplines `[regulatory]` sponsor press release with "must not be treated as verified efficacy." All Phase-3 numbers are quarantined to the pipeline-status subsection. Held.
- **FDA Fast Track = unverified, not asserted:** §C and §E both state it could not be verified against any primary source and is "not asserted"; tirzepatide's (different molecule) Fast Track is correctly attributed and explicitly *not* conflated as a retatrutide designation. Held.
- **Population annotation:** obesity (Jastreboff, no-diabetes), T2D (Rosenstock), MASLD (Sanyal, excl. diabetes) each annotated, all flagged Phase-2/2a. Held.
- **WADA:** §E confirms NOT on the 2026 Prohibited List (verified against S0/S2/S4 enumeration), with the class only on the Monitoring Program via sema/tirzepatide markers (retatrutide not individually named). Correct discipline (not asserted prohibited).

---

## Verdict

verdict: PASS

halt_reasons: none.
warnings: IC-4 (one anecdote_aggregate cite [§D-5] co-located with a 5–10 bpm secondary magnitude — load-bearing pattern is RCT-grounded; recommend dropping/re-grounding the bpm figure); IC-10/IC-13 corpus-missing (drugs.com §F[4] 403 bot-block; Rosenstock §D[2] paywalled full text — abstract-verified); concentration 100% single-sponsor (Eli Lilly) — honestly surfaced as required for an investigational single-sponsor drug.

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":117,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":4,"count_flagged":0},"IC-4":{"status":"WARN","count_checked":1,"count_flagged":1},"IC-5":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":0},"IC-7":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":15,"count_flagged":0},"IC-11":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-12":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":1,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":6,"largest_cluster_name":"Eli Lilly (sponsor)","largest_cluster_count":6,"share":1.0,"threshold_triggered":true,"surfaced_section_heading":"Concentration / sponsor audit (Section C)"},"corpus_scoping":{"verdict":"PASS","claims_checked":15,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-4: anecdote_aggregate cite (Section D ref 5, SeekPeptides) co-located with 5-10 bpm secondary magnitude estimate; load-bearing dose-dependent HR pattern is RCT-grounded [1]; recommend dropping or re-grounding the bpm figure","IC-10/IC-13 corpus-missing: drugs.com (Section F ref 4) returned HTTP 403 bot-block; Rosenstock 2023 (Section D ref 2) full text paywalled but abstract-verified for cited numbers","concentration_audit: 100% single-sponsor (Eli Lilly) — expected for an investigational single-sponsor drug; honestly surfaced as a first-class Section C subsection"]}
```
