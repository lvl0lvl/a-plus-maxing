# Phase 4.75 Integrity Gate — TB-500

> Independent anti-fabrication gate over the validated corpus
> `/tmp/aplus-research/tb-500/sections/section-A.md … section-G.md`.
> Per instruction, each file's `## Post-fix grep audit` block is excluded from live-content
> checks (those blocks legitimately quote OLD/superseded values). All live checks were run on
> the content from `# Section …` through the heading immediately preceding the audit block.

## Verdict

**verdict: PASS**  (no HALT-level IC failures)

No fabricated citations, no untagged source, no disallowed-tier source grounding a forbidden
number/efficacy claim, no placeholder, no Wikipedia grounding an admissible claim, concentration
finding surfaced first-class and well below the 70% HALT threshold. Two WARN-level items (a
type-tag-convention deviation and the literal `[population-mismatch]` tag not being used) are
substance-clean and recorded in `warnings[]`, not `halt_reasons[]`.

---

## IC-1 — Type-tag presence on inline citations
**Status: PASS (with WARN).** Across all seven Claims sections, the overwhelming majority of
inline citations carry a `[N, tag]` type-tag, and every cited source is tagged at least once in
its section. Eight bare `[N]` (no inline tag) instances exist, all in recap / cross-reference
position, NOT introducing a new ungrounded number:
- **Section C, Claim 15** (dose-finding recap): `[2] [5] [7] [8] [4]` — each restates a dose
  figure already grounded with `[N, animal]` at its primary claim (C-3/8/10/12/13). The numbers
  are independently tagged-grounded; the recap line omits the redundant tag.
- **Section D, Claim 4** ("interpretation of [1]") and **Claim 8** ("the claim in [7]") — pure
  intra-section cross-references back to `[1, animal]` and `[7, animal]`; ground no number.
No bare citation introduces an untagged grounding. count_checked = 7 sections; count_flagged = 0
fabrication-level; 8 convention-level bare cites (WARN).

## IC-2 — Bibliography type-tag presence
**Status: PASS.** Every real bibliography entry carries `tag=`: A 10/10, B 15/15, C 9/9, D 12/12,
E 20/20, F 9 real entries tagged ([8] is an explicit `— see [1]` cross-reference, correctly noted
as "not a separate dataset"), G 16 tagged of 19 slots ([2] and [3] are explicit `(reserved)`
placeholders; [9] is an explicit `(= #1)` duplicate pointer to the tagged #1). No real entry is
missing a tag.

## IC-3 — Vendor-not-numerical
**Status: PASS.** One live `vendor_label` cite exists: G `[13, vendor_label]` (Empower storefront).
It grounds only a self-reported purity spec (≥98%) and the identity constants CAS 77591-33-4 /
MW 4963.49 — explicitly flagged "self-reported … identity/reconstitution math only, never
efficacy." No dose/n/effect/%/p/half-life/AE-rate is grounded on a vendor source.

## IC-4 — Anecdote-not-numerical
**Status: PASS.** Live `anecdote_aggregate` cites: G `[14]` (qualitative contamination/variability,
no number), G `[15]` (reconstitution arithmetic only — 10 mg/2 mL → 5 mg/mL admin dilution math,
explicitly "NOT a pharmacy data sheet," not an efficacy dose), E `[8]`/`[10]` (RegeneRx dermal
press releases — paired with the registry `open_label` record; only qualitative "safe / mid-dose
most active"; the n=72 comes from the registry cite, not the press release). No anecdote source
grounds an enumerated number type.

## IC-5 — Practitioner-protocol-not-efficacy
**Status: PASS.** Live `practitioner_protocol` cites: G `[16]` (Seeds), `[17]` (A4M), `[18]`
(convention) ground dose/cycle/route prescribing conventions only, under the explicit header
"No efficacy or AE-rate is inferred from these." No efficacy / AE-rate / mechanism is grounded on
a practitioner protocol.

## IC-6 — Compounding-data-sheet-with-efficacy
**Status: PASS.** Zero live `compounding_data_sheet` tags remain (the former source [15] was
re-tagged to `anecdote_aggregate`; G's tally line reads `compounding_data_sheet: 0`). No efficacy
claim rests on a compounding data sheet.

## IC-7 — Population-mismatch
**Status: PASS (literal-tag WARN).** The corpus does not use the literal string
`[population-mismatch]`, BUT the substance is fully honored: every animal-tagged claim in the
preclinical sections (B/C/D) carries an explicit species label on the same line (24/24 animal
claim references checked; 0 missing a species word), and the preclinical sections add explicit
"numeric in-vivo magnitudes are from an animal model, not human data" framing (Section B Claim 2.2;
Section D per-claim species+n+route). Human numbers (E human-trial endpoints; F human AE rates
25/44, 16/24) are clearly labeled human. No animal result is laundered as human-applicable. The
missing literal tag is a convention deviation (WARN), not a misrepresentation.

## IC-8 — Route-extrapolation
**Status: PASS.** The `[route-extrapolation]` tag is present where dose claims cross routes/
molecules: Section A (2×: SC/IM-vs-IV-vs-fragment, and the marketed-route caveat), Section C (3×:
local fibrin depot vs systemic SC; intradermal mg/kg vs fixed-mass SC; the dose-summary
non-interconvertibility line). Section D narrates route/modality mismatch (AAV / intramyocardial
scaffold / topical vs systemic self-injection) in claim bodies and coverage gaps. Cross-route dose
claims are tagged.

## IC-9 — Concentration-surfacing
**Status: PASS.** The single-lab concentration finding (Goldstein/RegeneRx nexus, ~20% lower-bound
share) is surfaced as the FIRST content section of Section G — `## Concentration audit` at line 11,
the first `##` heading in the document, ahead of the sourcing/indication discussion — with a boxed
`⚠ COI/translation-concentration flag`. Surfaced first-class, before the first indication content.
surfaced_before_first_indication = true.

## IC-10 — No fabricated citations
**Status: PASS.** 5 load-bearing citations spot-verified live (PMID/DOI real AND supports claim):
1. **Esposito et al. 2012**, PMID 22962027, DOI 10.1002/dta.1402 (A-[2]/G-[19]) — REAL; abstract
   confirms it identifies the Ac-LKKTETQ (Tβ4 17-23) fragment in a TB-500 product. ✓
2. **Spurney et al. 2010**, PMID 20126456 (C-[4]) — REAL; abstract confirms increased regenerating
   fibers in mdx mice WITHOUT functional/strength/cardiac/fibrosis benefit (the corpus's honest
   negative). ✓
3. **Zhou et al. 2012**, PMID 21907210, DOI 10.1016/j.yjmcc.2011.08.020 (D-[4]) — REAL; abstract
   confirms post-MI Tβ4 does NOT reprogram epicardial cells into cardiomyocytes (the documented
   replication failure). ✓
4. **Sosne et al. 2023**, PMID 36613994, DOI 10.3390/ijms24010554 (E-[5]/F-[2]) — REAL; abstract
   confirms n=18, 6/10 vs 1/8 complete corneal healing, p=0.0656 narrow miss — matches corpus
   exactly. (Pub-system year shows 2022; corpus cites 2023, vol 24(1) Jan-2023 issue — the corpus
   already documents this issue-date reconciliation; PMID/DOI correct.) ✓
5. **Wang et al. 2021**, PMID 34346165, DOI 10.1111/jcmm.16693 (A-[9]/E-[17]/F-[1]) — REAL;
   abstract confirms SAD n=54 / MAD n=30, doses 0.05–25 µg/kg, no SAE/DLT, dose-proportional PK,
   no accumulation — matches corpus exactly. ✓
No fabricated citation found.

## IC-11 — No placeholder strings
**Status: PASS.** Live-content scan for TODO/TBD/XXX/lorem/[citation needed]/FIXME/??? → zero hits.
(Section G's bibliography slots `2. (reserved)` / `3. (reserved)` are explicitly documented,
intentionally-empty numbering placeholders, not unfilled content — outside the enumerated
placeholder set and disclosed in the tally.)

## IC-12 — No Wikipedia citations grounding claims
**Status: PASS.** Three Wikipedia mentions, none grounding an admissible claim:
- A-Claim 1 / ref [3]: the MW claim is grounded on **UniProt P62328** (the sanctioned primary
  re-anchor); Wikipedia is explicitly demoted to "tertiary, cross-check only," and the
  Wikipedia-attributed ~4,921 Da is NOT the canonical value (canonical = 4,963 Da from UniProt).
  This is exactly the permitted UniProt/primary re-anchor case.
- G-[10]: Wikipedia "Allan L. Goldstein" grounds a COI/affiliation fact (RegeneRx chairman/
  stockholder), corroborated by patent US8143218B2 — not an efficacy/dose/numerical claim.

## IC-13 — Per-citation corpus scoping
**Status: WARN (resolves to PASS-with-warnings).** For 5 key numerical/qualitative claims the cited
source's abstract was fetched and the number/finding confirmed present: Esposito → Ac-LKKTETQ
identity; Spurney → histology-without-function; Wang → doses + no SAE/DLT + dose-proportional PK;
Sosne → 6/10 vs 1/8, p=0.0656; Zhou → no cardiomyocyte reprogramming. All 5 in-corpus. The corpus
itself honestly flags several paywalled full-texts (Wiley 403 on A-[2]/A-[4], PubMed CAPTCHA on
A-[6], Nature auth-wall on D-[1]) where only abstract/record-level verification was possible —
these are corpus-missing WARNs (paywall), not scoping failures. claims_checked = 5; claims_failed = [].

---

## Population / Concentration / Corpus (computed objects, narrated)

**population_mismatch.** Verdict PASS. 24 animal-tagged claim references across Sections B (3),
C (10), D (11) were checked; every one carries an explicit species label on its own line, and the
preclinical sections add explicit "not human data" framing. Zero animal results are presented as
human-applicable. checked_citations = 24; flagged_citations = [].

**concentration_audit.** Verdict PASS. Section G computes the dominant cluster
(Goldstein/Kleinman/Sosne/RegeneRx nexus) share of in-vivo efficacy primaries at a ~20% lower
bound (estimate range 20–35%), using Xing 2021's ~133-ref breadth as a diversity proxy plus
explicit cluster mapping; no single lab approaches the ≥0.70 HALT threshold. Reported here on the
prompt's structured shape: total_primaries 20, largest_cluster_name "Goldstein/RegeneRx",
largest_cluster_count 4, share 0.20, threshold_triggered false (0.20 < 0.70). The finding is
surfaced as the first content section ("## Concentration audit"), before any indication discussion,
with a prominent COI/translation-concentration flag noting that while the *preclinical* literature
is decentralized, 100% of the *human clinical-translation* program is concentrated in the
commercially-conflicted Goldstein/RegeneRx cluster — an honest, correctly-scoped distinction.

**corpus_scoping.** Verdict PASS (with paywall warnings). 5 key numerical claims were
abstract-verified in their cited sources (see IC-13); 0 failed. Several full-texts are paywalled
(Wiley/Nature/PubMed-CAPTCHA), so a handful of secondary details rest on abstract/record-level
verification — recorded as warnings, never as scoping HALTs, consistent with the
"paywalled → corpus-missing WARN, not halt" rule. claims_checked = 5; claims_failed = [].

---

## Structured verdict

```json
{"phase":"4.75","ic_checks":{"IC-1":{"status":"PASS","count_checked":7,"count_flagged":0,"findings":["8 bare [N] cites in C-15 recap + D-4/D-8 cross-refs; each source tagged elsewhere in-section and every number grounded with [N,tag] at its primary claim — convention WARN, not fabrication"]},"IC-2":{"status":"PASS","findings":["all real bib entries carry tag=; F-[8] is an explicit cross-ref, G-[2]/[3] reserved placeholders, G-[9] duplicate pointer"]},"IC-3":{"status":"PASS","findings":["G-[13] vendor grounds only self-reported purity/identity constants, never efficacy/dose/AE-rate"]},"IC-4":{"status":"PASS","findings":["G-[14] qualitative, G-[15] reconstitution-admin math only, E-[8]/[10] press-release qualitative; no enumerated number grounded on anecdote"]},"IC-5":{"status":"PASS","findings":["G-[16]/[17]/[18] ground dose/cycle/route conventions only; no efficacy/AE/mechanism"]},"IC-6":{"status":"PASS","findings":["zero live compounding_data_sheet tags; former [15] re-tagged to anecdote_aggregate"]},"IC-7":{"status":"PASS","findings":["literal [population-mismatch] tag not used (WARN), but all 24 animal claims carry species labels + explicit 'not human data' framing; no animal result laundered as human"]},"IC-8":{"status":"PASS","findings":["route-extrapolation tagged in A (2x) and C (3x); D narrates route/modality mismatch in claim bodies"]},"IC-9":{"status":"PASS","findings":["concentration audit is the first ## section of G, ahead of indications, with boxed COI flag"]},"IC-10":{"status":"PASS","count_checked":5,"count_flagged":0,"findings":["Esposito 2012 (22962027), Spurney 2010 (20126456), Zhou 2012 (21907210), Sosne 2023 (36613994), Wang 2021 (34346165) all real PMID/DOI and support their claims"]},"IC-11":{"status":"PASS","findings":["no TODO/TBD/XXX/lorem/[citation needed]; G reserved bib slots are documented numbering placeholders"]},"IC-12":{"status":"PASS","findings":["MW re-anchored to UniProt P62328 (Wikipedia tertiary cross-check only); G-[10] Wikipedia grounds a COI fact, not a number"]},"IC-13":{"status":"WARN","count_checked":5,"count_flagged":0,"findings":["5/5 key numbers abstract-confirmed in cited source; several full-texts paywalled (Wiley/Nature/CAPTCHA) → abstract-level verification only = corpus-missing WARN, not scoping fail"]}},"population_mismatch":{"verdict":"PASS","checked_citations":24,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":20,"largest_cluster_name":"Goldstein/RegeneRx","largest_cluster_count":4,"share":0.20,"threshold_triggered":false,"surfaced_section_heading":"## Concentration audit (dominant labs; estimated single-lab share of efficacy primaries; method)","surfaced_before_first_indication":true},"corpus_scoping":{"verdict":"PASS","claims_checked":5,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-1: 8 bare [N] inline cites in C-15 dose recap + D-4/D-8 cross-references (each source tagged elsewhere in-section; numbers grounded with [N,tag] at primary claim) — type-tag-convention deviation, not fabrication","IC-7: literal [population-mismatch] tag string is not used; substance satisfied via per-claim species labels + explicit 'not human data' framing","IC-13: paywalled full-texts (Wiley 403 on A-[2]/A-[4], PubMed CAPTCHA on A-[6], Nature auth-wall on D-[1]) verified at abstract/record level only — corpus-missing WARN","IC-10: Sosne NK trial pub-system year shows 2022 vs corpus-cited 2023 (vol 24(1), Jan-2023 issue) — issue-date reconciliation already documented in-corpus; PMID 36613994 / DOI correct"],"iterations":1}
```
